"""CR-REMED-002 — immutable privileged supervisor bootstrap.

The authority root must preload and freeze the COMPLETE privileged code
byte set (verified against the operator-selected trusted identity) into a
sealed authority-held representation BEFORE exposing the controller
trigger; the supervisor is then created from the FROZEN representation
(fork of the already-loaded root process) and NEVER re-imports privileged
code from the ordinary mutable host harness tree.

Adversarial reproduction of the previous vulnerability: after root-ready,
an attacker modifies (or delete/recreates) the ordinary host harness tree
BEFORE supervisor creation — the attacker's code must NEVER execute."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

import pytest

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns

ATTACKER_MARKER = "QH-ATTACKER-CODE-EXECUTED-9c1f7ad2"
ATTACKER_MARKER_FILE = "attacker-marker-9c1f7ad2.txt"


def _harness_copy(tmp_path, name="harness-H"):
    dest = tmp_path / name
    shutil.copytree(str(HARNESS_ROOT), str(dest),
                    ignore=shutil.ignore_patterns(
                        "__pycache__", "test-outputs", "*.pyc"))
    return str(dest)


def _attacker_module_bytes(rel: str) -> bytes:
    """Hostile replacement for a privileged module: if these bytes are ever
    IMPORTED/EXECUTED by the authority flow they drop a unique marker."""
    return (
        "#!/usr/bin/env python3\n"
        f"ATTACKER_MARKER = {ATTACKER_MARKER!r}\n"
        "import os, sys\n"
        "for d in ('/tmp', os.path.dirname(os.path.abspath(__file__))):\n"
        "    try:\n"
        f"        open(os.path.join(d, {ATTACKER_MARKER_FILE!r}), 'w')"
        ".write('executed: ' + __file__ + chr(10))\n"
        "    except OSError:\n"
        "        pass\n"
        f"print({ATTACKER_MARKER!r}, file=sys.stderr)\n"
    ).encode("utf-8")


def _scan_for_marker(base) -> list[str]:
    hits = []
    for path, _dirs, files in os.walk(base):
        for name in files:
            if name == ATTACKER_MARKER_FILE:
                hits.append(os.path.join(path, name))
    return hits


@requires_bwrap
@requires_userns
def test_host_harness_mutation_after_root_ready_cannot_alter_supervisor(env,
                                                                        tmp_path):
    """§10 A: root completes the privileged bootstrap freeze and exposes
    its trigger; the attacker then REPLACES privileged harness modules on
    the ordinary host tree; the authorized controller proceeds — the
    protected flow uses the FROZEN trusted bytes and the attacker marker
    is NEVER executed."""
    hroot = _harness_copy(tmp_path)
    env.author_spec("boot-0001", harness_root=hroot)
    root = env.spawn_root()
    # root is READY: the attacker now swaps privileged modules on the host
    for rel in ("qh/authority.py", "qh/gatew.py", "qh/custody.py",
                "qh/boundary_child.py", "qh/util.py"):
        with open(os.path.join(hroot, rel), "wb") as fh:
            fh.write(_attacker_module_bytes(rel))
    mint = env.root_mint("boot-0001")
    assert mint.get("ok"), mint
    resp = env.controller_request("boot-0001", own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert resp.get("ok"), (resp, err)
    assert rc == 0, err
    # the attacker's module bytes were NEVER imported/executed anywhere
    assert _scan_for_marker(tmp_path) == []
    assert ATTACKER_MARKER not in err
    assert ATTACKER_MARKER not in json.dumps(resp)
    # the protected launch produced its normal artifact
    assert (env.auditor_output / "launch-sim-marker.txt").is_file()


@requires_bwrap
@requires_userns
def test_host_harness_delete_recreate_cannot_substitute(env, tmp_path):
    """§10 delete/recreate: the ordinary host harness path is DELETED and
    recreated with attacker bytes after root-ready — supervisor creation
    must still never execute attacker code (frozen representation, or
    fail-closed refuse; never attacker execution)."""
    hroot = _harness_copy(tmp_path, name="harness-H2")
    env.author_spec("boot-0002", harness_root=hroot)
    root = env.spawn_root()
    shutil.rmtree(hroot)
    os.makedirs(os.path.join(hroot, "qh"), exist_ok=True)
    os.makedirs(os.path.join(hroot, "fixtures"), exist_ok=True)
    for rel in ("qh/authority.py", "qh/cli.py", "qh/boundary_child.py",
                "fixtures/gatew_payload.py", "fixtures/launch_sim_payload.py"):
        with open(os.path.join(hroot, rel), "wb") as fh:
            fh.write(_attacker_module_bytes(rel))
    mint = env.root_mint("boot-0002")
    assert mint.get("ok"), mint
    resp = env.controller_request("boot-0002", own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert _scan_for_marker(tmp_path) == []
    assert ATTACKER_MARKER not in json.dumps(resp)
    # either the frozen flow completed, or the root/supervisor failed
    # closed — in BOTH cases no attacker execution occurred
    assert resp.get("ok") is True or resp.get("ok") is False


@requires_bwrap
@requires_userns
def test_bootstrap_freeze_evidenced_before_trigger(env, tmp_path):
    """§9: the frozen bootstrap bytes/loaded-code identity is mechanically
    evidenced in the observability ledger BEFORE the root trigger is
    exposed (ROOT_SOCKET_BOUND) and before any controller request."""
    hroot = _harness_copy(tmp_path, name="harness-H3")
    env.author_spec("boot-0003", harness_root=hroot)
    root = env.spawn_root()
    try:
        events = [r["event"] for r in env.ledger_records()]
        assert "PRE_CONTROLLER_BOOTSTRAP_FROZEN" in events
        frozen = [r for r in env.ledger_records()
                  if r["event"] == "PRE_CONTROLLER_BOOTSTRAP_FROZEN"][0]
        assert frozen.get("bundle_digest")
        assert frozen.get("files") == 21  # 19 qh modules + 2 fixtures
        assert frozen.get("expected_tree_digest_match") is True
        assert frozen.get("bundle_seal_status") == "sealed"
        assert frozen.get("template_id")
        assert events.index("PRE_CONTROLLER_BOOTSTRAP_FROZEN") < \
            events.index("ROOT_SOCKET_BOUND")
    finally:
        env.cleanup_procs()
    env.root_outcome(root, timeout=60)


@requires_bwrap
@requires_userns
def test_supervisor_spawned_from_frozen_bytes_not_host_import(env, tmp_path):
    """§8: after mint acceptance the supervisor is created from the frozen
    trusted representation — the ledger records that the supervisor used
    the frozen bootstrap (and NO host-tree Python re-import occurs)."""
    hroot = _harness_copy(tmp_path, name="harness-H4")
    env.author_spec("boot-0004", harness_root=hroot)
    root = env.spawn_root()
    mint = env.root_mint("boot-0004")
    assert mint.get("ok"), mint
    resp = env.controller_request("boot-0004", own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert resp.get("ok"), resp
    recs = env.ledger_records()
    spawn = [r for r in recs if r["event"] == "ROOT_SPAWNED_SUPERVISOR"]
    assert spawn, "expected supervisor spawn record"
    assert spawn[0].get("channel") == "fork-frozen-bootstrap"


def test_post_freeze_import_guard_blocks_host_qh_imports(env, tmp_path):
    """The import guard: after the privileged bootstrap freeze, any NEW
    qh.* import from the ordinary host path fails closed (an attacker
    cannot introduce code by planting modules post-freeze)."""
    from qh.trusted_spec import build_pre_controller_template
    hroot = _harness_copy(tmp_path, name="harness-H5")
    for d in ("ar", "cfg", "ev", "ao"):
        (tmp_path / d).mkdir(exist_ok=True)
    exe = tmp_path / "exe"
    exe.write_text("#!/bin/sh\necho synthetic\n", encoding="utf-8")
    exe.chmod(0o755)
    tpl = build_pre_controller_template(
        attempt_id="boot-guard", attempt_root=str(tmp_path / "ar"),
        target_src=None,
        config_dir=str(tmp_path / "cfg"), manifest_id="m" * 64,
        evidence_src=str(tmp_path / "ev"),
        auditor_output_src=str(tmp_path / "ao"),
        codex_exe=str(exe), codex_version="synthetic",
        profile={}, config_sha256="0" * 64,
        credential_adapter={"id": "synthetic_inert_v1",
                            "provider_role": "inert", "version": 1},
        harness_root=hroot,
        expected_harness_tree_digest=__import__(
            "qh.trusted_spec", fromlist=["harness_tree_digest"])
        .harness_tree_digest(hroot))
    spec_file = tmp_path / "guard-spec.json"
    spec_file.write_text(json.dumps(tpl), encoding="utf-8")
    wrapper = tmp_path / "guard_probe.py"
    wrapper.write_text(
        "import importlib, importlib.util, json, sys\n"
        f"sys.path.insert(0, {hroot!r})\n"
        "from qh.rootauth import PrivilegedBootstrap\n"
        f"tpl = json.load(open({str(spec_file)!r}))\n"
        f"boot = PrivilegedBootstrap.freeze(harness_root={hroot!r},"
        " expected_tree_digest=tpl['harness']['tree_digest'])\n"
        "boot.install_import_guard()\n"
        "try:\n"
        "    importlib.import_module('qh.attacker_planted_module')\n"
        "    print('IMPORT_UNEXPECTEDLY_ALLOWED')\n"
        "except ImportError as exc:\n"
        "    print('GUARDED:' + str(exc))\n"
        "assert importlib.util.find_spec  # stdlib still importable\n",
        encoding="utf-8")
    proc = subprocess.run([sys.executable, str(wrapper)],
                          capture_output=True, text=True, timeout=120,
                          cwd=str(HARNESS_ROOT))
    assert proc.returncode == 0, proc.stderr
    assert "GUARDED:QH_IMPORT_FROZEN" in proc.stdout, proc.stdout
    assert "IMPORT_UNEXPECTEDLY_ALLOWED" not in proc.stdout


def test_freeze_verifies_bundle_against_operator_expected_digest(tmp_path):
    """§9/§17: the frozen byte set is COMPARED to the OPERATOR-PROVIDED
    expected identity — a host tree that drifted from that identity fails
    closed at freeze time (before the trigger is exposed, and the drifted
    tree is never self-pinned as its own expected value)."""
    from qh.compose import CompositionEnv
    from qh.rootauth import PrivilegedBootstrap, RootInitError
    hroot = _harness_copy(tmp_path, name="harness-H6")
    base = tmp_path / "env6"
    env = CompositionEnv(str(base))
    tpl = env.author_spec("boot-0005", harness_root=hroot)
    # attacker mutates the host tree BEFORE the authority starts
    with open(os.path.join(hroot, "qh", "gatew.py"), "wb") as fh:
        fh.write(_attacker_module_bytes("qh/gatew.py"))
    with pytest.raises(RootInitError) as exc:
        PrivilegedBootstrap.freeze(
            harness_root=hroot,
            expected_tree_digest=tpl["harness"]["tree_digest"])
    assert "HARNESS_TREE_DRIFT" in str(exc.value)


@requires_bwrap
@requires_userns
def test_root_startup_fails_closed_on_harness_drift(env, tmp_path):
    """Full-root proof: a host harness tree that drifted from the
    operator-selected identity refuses at startup — no trigger is
    exposed."""
    hroot = _harness_copy(tmp_path, name="harness-H7")
    env.author_spec("boot-0006", harness_root=hroot)
    with open(os.path.join(hroot, "qh", "util.py"), "ab") as fh:
        fh.write(b"# drift\n")
    with pytest.raises(RuntimeError, match="ROOT_STARTUP_FAILED"):
        env.spawn_root()


@requires_bwrap
@requires_userns
def test_no_pythonpath_reimport_after_mint(env, tmp_path):
    """Structural: the production root spawns the supervisor WITHOUT a
    host-tree PYTHONPATH re-import (the previous defect shape
    `python -m qh.cli supervisor` + PYTHONPATH=<host harness root>)."""
    src = open(os.path.join(str(HARNESS_ROOT), "qh", "rootauth.py"),
               encoding="utf-8").read()
    # the CLI-spawn defect shape is GONE from the authority root
    assert "_spawn_supervisor_cli" not in src
    assert "PYTHONPATH" not in src
    # the fork-based path exists and is the production default
    assert "_fork_supervisor" in src
    assert "os.fork" in src
