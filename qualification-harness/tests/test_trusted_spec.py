"""TRUSTED LAUNCH SPEC — canonicalization, completeness and launch-time
identity verification (IR-002 core, remediation §7/§9/§10/§19)."""
from __future__ import annotations

import json
import os
import shutil

import pytest

from conftest import HARNESS_ROOT

from qh.codex_profile import ProfileSpec, render_config_toml
from qh.trusted_spec import (SPEC_SCHEMA_VERSION, build_spec,
                             canonical_spec_bytes, dir_tree_digest, spec_id,
                             validate_spec, verify_spec)
from qh.util import sha256_bytes


def _make_env(tmp_path, *, harness_root: str = str(HARNESS_ROOT)):
    """A minimal operator-side environment (dirs + synthetic codex exe)."""
    root = tmp_path / "attempt-root"
    cfg = tmp_path / "controller-config"
    ev = tmp_path / "evidence"
    ao = tmp_path / "auditor-output"
    tg = tmp_path / "target"
    for d in (root, cfg, ev, ao, tg):
        d.mkdir(parents=True)
    (ev / "evidence.md").write_text("ev\n", encoding="utf-8")
    (tg / "t.txt").write_text("t\n", encoding="utf-8")
    exe = tmp_path / "codex-like"
    exe.write_text("#!/bin/sh\necho codex-fixture\n", encoding="utf-8")
    exe.chmod(0o755)
    profile = ProfileSpec(profile_name="audit", model_name="probe")
    config = render_config_toml(profile)
    spec = build_spec(
        attempt_id="spec-0001", attempt_root=str(root),
        config_dir=str(cfg), manifest_id="a" * 64,
        evidence_src=str(ev), auditor_output_src=str(ao),
        target_src=str(tg), codex_exe=str(exe),
        codex_version="codex-cli synthetic-fixture",
        profile={"profile_name": profile.profile_name,
                 "description": profile.description,
                 "model_name": profile.model_name,
                 "workspace_role": profile.workspace_role,
                 "evidence_read_paths": list(profile.evidence_read_paths),
                 "target_read_paths": list(profile.target_read_paths),
                 "system_read_paths": list(profile.system_read_paths),
                 "extra_read_paths": list(profile.extra_read_paths),
                 "network_enabled": profile.network_enabled},
        config_sha256=sha256_bytes(config.encode()),
        credential_adapter={"id": "codex_chatgpt_oauth_v1",
                            "provider_role": "codex_chatgpt_oauth",
                            "version": 1},
        harness_root=harness_root,
        controller_pid=4242, controller_starttime="999888777")
    return spec, {"root": root, "cfg": cfg, "ev": ev, "ao": ao, "tg": tg,
                  "exe": exe}


def test_spec_is_canonical_and_deterministic(tmp_path):
    spec, _ = _make_env(tmp_path)
    b1 = canonical_spec_bytes(spec)
    assert canonical_spec_bytes(json.loads(b1)) == b1
    assert spec_id(spec) == spec_id(json.loads(b1))
    assert len(spec_id(spec)) == 64


def test_spec_completeness_covers_every_security_critical_field(tmp_path):
    """Every §7 minimum field is present in a built spec."""
    spec, _ = _make_env(tmp_path)
    for key in ("spec_version", "attempt_id", "attempt_root",
                "bootstrap_manifest", "controller_scope",
                "authorized_controller", "harness",
                "boundary_child", "sources", "codex",
                "credential_adapter", "noegress", "mount_roles", "payload"):
        assert key in spec
    assert spec["spec_version"] == SPEC_SCHEMA_VERSION
    assert spec["codex"]["exe"]["sha256"]
    assert spec["codex"]["config_sha256"]
    assert spec["harness"]["tree_digest"]
    ac = spec["authorized_controller"]
    assert set(ac) == {"uid", "pid", "starttime"}
    for src in ("evidence", "auditor_output", "target"):
        for f in ("dev", "ino", "tree_digest"):
            assert spec["sources"][src][f] is not None


def test_missing_field_fails_validation(tmp_path):
    spec, _ = _make_env(tmp_path)
    broken = dict(spec)
    del broken["credential_adapter"]
    with pytest.raises(Exception):
        validate_spec(broken)
    broken2 = json.loads(canonical_spec_bytes(spec))
    broken2["codex"]["exe"].pop("sha256")
    with pytest.raises(Exception):
        validate_spec(broken2)


def test_verify_passes_on_untouched_environment(tmp_path):
    spec, _ = _make_env(tmp_path)
    assert verify_spec(spec) == []
    assert verify_spec(spec, expected_spec_id=spec_id(spec)) == []


def test_spec_id_mismatch_refused(tmp_path):
    spec, _ = _make_env(tmp_path)
    assert verify_spec(spec, expected_spec_id="0" * 64) == \
        ["SPEC_ID_MISMATCH"]


def test_dir_digest_is_path_independent(tmp_path):
    """The digest input carries entries only, so the SAME digest can be
    recomputed INSIDE the boundary at the mounted path (in-child source
    verification depends on this)."""
    a = tmp_path / "a"
    b = tmp_path / "nested" / "b"
    a.mkdir()
    b.mkdir(parents=True)
    for d in (a, b):
        (d / "f.txt").write_text("same\n", encoding="utf-8")
    assert dir_tree_digest(str(a)) == dir_tree_digest(str(b))


# ---- §19: mutate each security-critical source individually → REFUSED ----

def _harness_copy(tmp_path):
    dest = tmp_path / "harness-copy"
    shutil.copytree(str(HARNESS_ROOT), str(dest),
                    ignore=shutil.ignore_patterns(
                        "__pycache__", "test-outputs", "*.pyc"))
    return str(dest)


def test_mutation_harness_code_refused(tmp_path):
    hroot = _harness_copy(tmp_path)
    spec, paths = _make_env(tmp_path, harness_root=hroot)
    assert verify_spec(spec) == []
    # in-place code change between authorization and launch
    p = os.path.join(hroot, "qh", "boundary_child.py")
    with open(p, "a", encoding="utf-8") as fh:
        fh.write("# attacker mutation\n")
    assert "HARNESS_TREE_DRIFT" in verify_spec(spec)


def test_mutation_boundary_child_replaced_refused(tmp_path):
    hroot = _harness_copy(tmp_path)
    spec, paths = _make_env(tmp_path, harness_root=hroot)
    # delete + recreate the boundary child with attacker-modified bytes
    p = os.path.join(hroot, "qh", "boundary_child.py")
    os.unlink(p)
    with open(p, "wb") as fh:
        fh.write(b"#!/usr/bin/env python3\n# attacker boundary child\n")
    assert "HARNESS_TREE_DRIFT" in verify_spec(spec)


def test_byte_identical_recreation_is_contentneutral(tmp_path):
    """Code identity is CONTENT identity: recreating a code file with
    byte-identical content substitutes nothing (and the launch executes
    the verified memfd snapshot, never the host path)."""
    hroot = _harness_copy(tmp_path)
    spec, paths = _make_env(tmp_path, harness_root=hroot)
    p = os.path.join(hroot, "qh", "boundary_child.py")
    content = open(p, "rb").read()
    os.unlink(p)
    with open(p, "wb") as fh:
        fh.write(content)
    assert verify_spec(spec) == []


def test_mutation_evidence_content_refused(tmp_path):
    spec, paths = _make_env(tmp_path)
    (paths["ev"] / "evidence.md").write_text("tampered\n",
                                             encoding="utf-8")
    failures = verify_spec(spec)
    assert any(f.startswith("EVIDENCE_CONTENT_DRIFT") for f in failures)


def test_mutation_evidence_recreate_refused(tmp_path):
    spec, paths = _make_env(tmp_path)
    shutil.rmtree(paths["ev"])
    paths["ev"].mkdir()
    (paths["ev"] / "evidence.md").write_text("ev\n", encoding="utf-8")
    failures = verify_spec(spec)
    assert any("EVIDENCE_OBJECT_IDENTITY_CHANGED" in f for f in failures)


def test_mutation_target_recreate_refused(tmp_path):
    spec, paths = _make_env(tmp_path)
    shutil.rmtree(paths["tg"])
    paths["tg"].mkdir()
    (paths["tg"] / "t.txt").write_text("t\n", encoding="utf-8")
    failures = verify_spec(spec)
    assert any("TARGET_OBJECT_IDENTITY_CHANGED" in f for f in failures)


def test_mutation_auditor_output_recreate_refused(tmp_path):
    """The RW bind host source is spec-bound: a controller-selected or
    substituted auditor-output directory is refused."""
    spec, paths = _make_env(tmp_path)
    shutil.rmtree(paths["ao"])
    paths["ao"].mkdir()
    failures = verify_spec(spec)
    assert any("AUDITOR_OUTPUT_OBJECT_IDENTITY_CHANGED" in f
               for f in failures)


def test_mutation_codex_exe_bytes_refused(tmp_path):
    """Trusted executable changed after spec creation => REFUSED."""
    spec, paths = _make_env(tmp_path)
    paths["exe"].write_text("#!/bin/sh\necho tampered\n", encoding="utf-8")
    failures = verify_spec(spec)
    assert any("CODEX_EXE_CONTENT_DRIFT" in f for f in failures)


def test_mutation_codex_exe_replaced_refused(tmp_path):
    spec, paths = _make_env(tmp_path)
    content = paths["exe"].read_bytes()
    os.unlink(paths["exe"])
    paths["exe"].write_bytes(content)
    paths["exe"].chmod(0o755)
    failures = verify_spec(spec)
    assert any("CODEX_EXE_OBJECT_IDENTITY_CHANGED" in f
               for f in failures)


def test_mutation_attempt_root_recreate_refused(tmp_path):
    spec, paths = _make_env(tmp_path)
    shutil.rmtree(paths["root"])
    paths["root"].mkdir()
    failures = verify_spec(spec)
    assert any("ATTEMPT_ROOT_OBJECT_IDENTITY_CHANGED" in f
               for f in failures)


def test_boundary_child_outside_pinned_set_refused(tmp_path):
    spec, _ = _make_env(tmp_path)
    spec = json.loads(canonical_spec_bytes(spec))
    spec["boundary_child"]["relpath"] = "qh/attacker_child.py"
    failures = verify_spec(spec)
    assert any("BOUNDARY_CHILD_NOT_IN_PINNED_SET" in f for f in failures)
