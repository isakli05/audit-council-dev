"""C-1 — pre-controller scope provenance + C4' verification tests."""
from __future__ import annotations

import json
import os

from qh.bootstrap import (ControllerBinding, capture_bootstrap_manifest,
                          load_manifest, manifest_integrity,
                          verify_c4p, walk_scope)


def _mk_config(base, name="controller-config"):
    d = os.path.join(str(base), name)
    os.makedirs(d, exist_ok=True)
    return d


# ------------------------------------------------------------ capture ----

def test_capture_clean_pass(tmp_path):
    cfg = _mk_config(tmp_path)
    res = capture_bootstrap_manifest(cfg, str(tmp_path / "op"))
    assert res.ok, res.reason
    assert res.manifest_id
    assert os.path.isfile(res.manifest_path)


def test_capture_deterministic_content_address(tmp_path):
    cfg = _mk_config(tmp_path)
    with open(os.path.join(cfg, "settings.json"), "w") as fh:
        fh.write("{}\n")
    r1 = capture_bootstrap_manifest(cfg, str(tmp_path / "op1"))
    r2 = capture_bootstrap_manifest(cfg, str(tmp_path / "op2"))
    assert r1.manifest_id == r2.manifest_id
    with open(os.path.join(cfg, "settings.json"), "w") as fh:
        fh.write('{"changed": true}\n')
    r3 = capture_bootstrap_manifest(cfg, str(tmp_path / "op3"))
    assert r3.manifest_id != r1.manifest_id


def test_capture_rejects_preexisting_skills(tmp_path):
    cfg = _mk_config(tmp_path)
    os.makedirs(os.path.join(cfg, "skills", "some-skill"))
    res = capture_bootstrap_manifest(cfg, str(tmp_path / "op"))
    assert not res.ok
    assert "PRE_EXISTING_SKILLS_PRESENT" in res.reason


def test_capture_rejects_preexisting_projects(tmp_path):
    cfg = _mk_config(tmp_path)
    os.makedirs(os.path.join(cfg, "projects", "foreign-project"))
    res = capture_bootstrap_manifest(cfg, str(tmp_path / "op"))
    assert not res.ok
    assert "PRE_EXISTING_PROJECTS_STATE_PRESENT" in res.reason


def test_capture_sensitive_file_never_hashed(tmp_path):
    cfg = _mk_config(tmp_path)
    cred = os.path.join(cfg, ".credentials.json")
    with open(cred, "w") as fh:
        fh.write('{"token":"SYNTHETIC-VALUE"}')
    res = capture_bootstrap_manifest(cfg, str(tmp_path / "op"))
    assert res.ok
    doc = load_manifest(str(tmp_path / "op"), res.manifest_id)
    entry = doc["entries"][".credentials.json"]
    assert entry["sha256"] is None and entry["sensitive"] is True
    raw = open(res.manifest_path, "rb").read()
    assert b"SYNTHETIC-VALUE" not in raw


# --------------------------------------------------------------- C4' ----

def test_c4p_own_current_session_tree_pass(tmp_path, live_controller):
    """The controller's own current-session slug tree (created AFTER
    capture) is allowed — the accepted  current tree ⊆ manifest ∪ {own
    current-session slug}  rule."""
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    assert res.ok
    # controller runtime auto-creates its own session slug tree
    slug = os.path.join(cfg, "projects", "own-slug")
    os.makedirs(slug)
    with open(os.path.join(slug, "session-x.jsonl"), "w") as fh:
        fh.write("{}\n")
    proc, pid, starttime = live_controller(cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)
    assert out.passed, out.failures


def test_c4p_foreign_project_state_fail(tmp_path, live_controller):
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    assert res.ok
    # TWO new project slugs = unbound extra project/session state
    for slug in ("slug-a", "slug-b"):
        os.makedirs(os.path.join(cfg, "projects", slug))
    proc, pid, starttime = live_controller(cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)
    assert not out.passed
    assert "SCOPE_CONSISTENCY" in out.failures


def test_c4p_new_top_level_state_fail(tmp_path, live_controller):
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    with open(os.path.join(cfg, "unbound-new.txt"), "w") as fh:
        fh.write("x")
    proc, pid, starttime = live_controller(cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)
    assert not out.passed


def test_c4p_new_skills_fail(tmp_path, live_controller):
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    os.makedirs(os.path.join(cfg, "skills", "injected"))
    proc, pid, starttime = live_controller(cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)
    assert "NO_NEW_SKILLS" in out.failures


def test_c4p_peer_pid_mismatch_fail(tmp_path, live_controller):
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    proc, pid, starttime = live_controller(cfg)
    other_proc, other_pid, _ = live_controller(cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=other_pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)  # peer != bound
    assert "PEER_PID_MATCH" in out.failures


def test_c4p_env_claude_config_dir_mismatch_fail(tmp_path, live_controller):
    cfg = _mk_config(tmp_path)
    other_cfg = _mk_config(tmp_path, "other-config")
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    # the ACTUAL controller process env points elsewhere
    proc, pid, starttime = live_controller(other_cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)
    assert "ENV_CLAUDE_CONFIG_DIR" in out.failures


def test_c4p_starttime_mismatch_fail(tmp_path, live_controller):
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    proc, pid, starttime = live_controller(cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime="999999999",  # forged/relaunched starttime
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)
    assert "PID_STARTTIME_MATCH" in out.failures


def test_c4p_manifest_tamper_fail(tmp_path, live_controller):
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    doc = load_manifest(op, res.manifest_id)
    doc["entries"]["injected-entry"] = {"type": "file", "sha256": "0" * 64}
    assert manifest_integrity(doc) is not None
    proc, pid, starttime = live_controller(cfg)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)
    assert "MANIFEST_INTEGRITY" in out.failures


def test_c4p_scope_modification_is_tamper(tmp_path, live_controller):
    cfg = _mk_config(tmp_path)
    with open(os.path.join(cfg, "settings.json"), "w") as fh:
        fh.write("{}\n")
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    # controller-side modification of a manifest-recorded file
    with open(os.path.join(cfg, "settings.json"), "w") as fh:
        fh.write('{"tampered": true}\n')
    proc, pid, starttime = live_controller(cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(doc, binding, peer_pid=pid)
    assert not out.passed
    assert "SCOPE_CONSISTENCY" in out.failures


def test_c4p_absent_session_tree_also_passes(tmp_path, live_controller):
    """Evidence boundary: no universal assumption that the runtime always
    creates a session tree — a still-clean scope also passes."""
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    proc, pid, starttime = live_controller(cfg)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=pid, starttime=starttime,
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    assert verify_c4p(doc, binding, peer_pid=pid).passed


def test_c4p_fixture_reader_injection(tmp_path):
    """Deterministic fixture path: env/stat readers injected, no live
    process needed."""
    cfg = _mk_config(tmp_path)
    op = str(tmp_path / "op")
    res = capture_bootstrap_manifest(cfg, op)
    doc = load_manifest(op, res.manifest_id)
    binding = ControllerBinding(
        attempt_id="a1", root=str(tmp_path), manifest_id=res.manifest_id,
        pid=4242, starttime="12345",
        env_claims={"CLAUDE_CONFIG_DIR": cfg})
    out = verify_c4p(
        doc, binding, peer_pid=4242,
        env_reader=lambda pid: {"CLAUDE_CONFIG_DIR": cfg, "HOME": "/tmp"},
        stat_reader=lambda pid: "12345",
        walker=lambda d: doc["entries"])
    assert out.passed, out.failures
