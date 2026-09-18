"""C-3 / G-2 — Codex application write policy tests (zero provider)."""
from __future__ import annotations

import os

import pytest

from qh.codex_profile import (CodexIdentity, IdentityDrift, PolicyDrift,
                              ProfileSpec, build_exec_cli,
                              generate_codex_home, parse_profile,
                              render_config_toml, validate_profile_semantics,
                              verify_codex_identity, verify_frozen_profile)
from qh.util import sha256_file


def _spec() -> ProfileSpec:
    return ProfileSpec(profile_name="audit",
                       description="auditor-b restricted",
                       model_name="probe")


def test_exact_config_generation(tmp_path):
    spec = _spec()
    art = generate_codex_home(spec, str(tmp_path / "ch"))
    doc = parse_profile(art["config_path"])
    assert doc["default_permissions"] == "audit"
    prof = doc["permissions"]["audit"]
    assert list(prof["workspace_roots"]) == ["/auditor-output"]
    fs = prof["filesystem"]
    assert fs["/auditor-output"] == "write"
    assert fs["/evidence"] == "read"
    for p in ("/usr", "/bin", "/lib", "/lib64", "/sbin", "/etc"):
        assert fs[p] == "read"
    assert "/" not in fs                      # no root-wide read entry
    assert prof["network"]["enabled"] is False
    assert doc["projects"]["/auditor-output"]["trust_level"] == "trusted"


def test_render_is_byte_stable():
    assert render_config_toml(_spec()) == render_config_toml(_spec())


def test_only_one_persistent_write_root(tmp_path):
    spec = _spec()
    art = generate_codex_home(spec, str(tmp_path / "ch"))
    assert validate_profile_semantics(art["config_path"], spec) == []
    doc = parse_profile(art["config_path"])
    writes = [k for k, v in doc["permissions"]["audit"]["filesystem"].items()
              if v == "write"]
    assert writes == ["/auditor-output"]


def test_root_read_entry_rejected(tmp_path):
    spec = _spec()
    art = generate_codex_home(spec, str(tmp_path / "ch"))
    cfg = art["config_path"]
    text = open(cfg).read().replace(
        '"/auditor-output" = "write"', '"/auditor-output" = "write"\n"/" = "read"')
    open(cfg, "w").write(text)
    failures = validate_profile_semantics(cfg, spec)
    assert "ROOT_WIDE_READ_ENTRY_PRESENT" in failures


def test_second_write_root_rejected(tmp_path):
    spec = _spec()
    art = generate_codex_home(spec, str(tmp_path / "ch"))
    cfg = art["config_path"]
    text = open(cfg).read().replace(
        '"/auditor-output" = "write"',
        '"/auditor-output" = "write"\n"/target" = "write"')
    with open(cfg, "w") as fh:
        fh.write(text)
    failures = validate_profile_semantics(cfg, spec)
    assert any("WRITE_ROOTS" in f for f in failures), failures


def test_network_must_be_disabled_in_profile(tmp_path):
    spec = _spec()
    art = generate_codex_home(spec, str(tmp_path / "ch"))
    cfg = art["config_path"]
    text = open(cfg).read().replace(
        "[permissions.audit.network]\nenabled = false",
        "[permissions.audit.network]\nenabled = true")
    with open(cfg, "w") as fh:
        fh.write(text)
    failures = validate_profile_semantics(cfg, spec)
    assert "NETWORK_NOT_DISABLED_IN_PROFILE" in failures


def test_cli_shape_no_add_dir_no_sandbox_flag():
    argv = build_exec_cli("codex", "/auditor-output")
    assert argv[:4] == ["codex", "exec", "-C", "/auditor-output"]
    assert "--add-dir" not in argv
    assert "-s" not in argv and "--sandbox" not in argv
    with pytest.raises(PolicyDrift):
        build_exec_cli("codex", "/auditor-output",
                       extra_args=("--add-dir", "/x"))
    with pytest.raises(PolicyDrift):
        build_exec_cli("codex", "/auditor-output",
                       extra_args=("--sandbox", "workspace-write"))


def test_generated_codex_home_has_no_auth_material(tmp_path):
    spec = _spec()
    art = generate_codex_home(spec, str(tmp_path / "ch"))
    files = []
    for root, _d, fs in os.walk(art["codex_home"]):
        files.extend(fs)
    assert "auth.json" not in files
    assert set(files) == {"config.toml"}  # + empty sessions dir


def test_codex_home_auth_entry_in_profile_rejected(tmp_path):
    spec = _spec()
    art = generate_codex_home(spec, str(tmp_path / "ch"))
    cfg = art["config_path"]
    text = open(cfg).read().replace(
        '"/evidence" = "read"',
        '"/evidence" = "read"\n"/codex-home/auth.json" = "read"')
    open(cfg, "w").write(text)
    failures = validate_profile_semantics(cfg, spec)
    assert any("CODEX_HOME_OR_AUTH" in f for f in failures)


def test_identity_pin_and_drift(tmp_path):
    exe = tmp_path / "codex-like"
    exe.write_text("#!/bin/sh\nexit 0\n")
    exe.chmod(0o755)
    ident = CodexIdentity(version="codex-cli synthetic",
                          sha256=sha256_file(str(exe)),
                          exe_path=str(exe))
    assert verify_codex_identity(ident)["actual_sha256"] == ident.sha256
    # drift: binary replaced after pinning
    exe.write_text("#!/bin/sh\nexit 1\n# tampered\n")
    with pytest.raises(IdentityDrift):
        verify_codex_identity(ident)
    with pytest.raises(IdentityDrift):
        verify_codex_identity(CodexIdentity(
            version="v", sha256="0" * 64, exe_path=str(exe)))


def test_frozen_profile_drift_rejected(tmp_path):
    spec = _spec()
    art = generate_codex_home(spec, str(tmp_path / "ch"))
    exe = tmp_path / "codex-like"
    exe.write_text("#!/bin/sh\nexit 0\n")
    exe.chmod(0o755)
    ident = CodexIdentity(version="v", sha256=sha256_file(str(exe)),
                          exe_path=str(exe))
    from qh.codex_profile import freeze_profile
    frozen = freeze_profile(art, ident)
    verify_frozen_profile(frozen, art, ident)  # no drift
    # mutate the config AFTER freeze
    open(art["config_path"], "a").write(
        "\n# policy drift injected\n[drift]\nx = 1\n")
    art2 = {"config_sha256": sha256_file(art["config_path"])}
    with pytest.raises(PolicyDrift):
        verify_frozen_profile(frozen, art2, ident)


def test_demonstrated_fixture_data_loads():
    import json
    data = json.load(open(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "fixtures", "demonstrated-profile.json")))
    ident = data["codex_identity"]
    assert ident["version"] == "codex-cli 0.154.0"
    assert ident["sha256"] == (
        "3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022")
    assert data["profile"]["network_enabled"] is False
    # data drives a spec end to end
    spec = ProfileSpec(
        profile_name=data["profile"]["profile_name"],
        description=data["profile"]["description"],
        model_name=data["profile"]["model_name"])
    assert render_config_toml(spec)  # renders cleanly
