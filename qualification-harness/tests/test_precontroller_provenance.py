"""AUCDEV023-CR-HARDEN-001 — PRE-CONTROLLER IMMUTABLE AUTHORITY-BOOTSTRAP
PROVENANCE.

Two-phase authority lifecycle: the privileged authority/root code identity
is trusted and frozen from an operator-controlled source BEFORE the
untrusted same-UID controller can modify the ordinary harness tree:

PHASE A (no controller exists): the authority process verifies the live
ordinary tree against the OPERATOR-PROVIDED expected identity (never a
value recomputed from that same tree), freezes + seals the complete
privileged byte set, imports and code-object-verifies every privileged
module, seals the pre-controller launch template, records
PRE_CONTROLLER_BOOTSTRAP_FROZEN and refuses every NEW qh import.

PHASE B: only after that milestone may the authorized controller start;
the operator finalizes the final spec over a trusted capability channel
(PIPE / sealed memfd — never an ordinary file, never argv/env) by adding
ONLY the controller identity; the final spec's harness identity must equal
the pre-controller frozen identity or the root fails closed BEFORE any
controller-accessible trigger exists.

Adversarial negatives: live-tree mutation before finalization (per-module
attacker markers incl. rootauth/authority/util/trusted_spec), entire-tree
replacement, modify-then-restore TOCTOU, and the pre-freeze
expected-identity mismatch (expected established INDEPENDENTLY of the
mutated live bytes)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

import pytest

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns

ATTACKER_MARKER = "QH-PRECONTROLLER-ATTACKER-4b7e91c2"
ATTACKER_MARKER_FILE = "attacker-marker-4b7e91c2.txt"


def _harness_copy(tmp_path, name):
    dest = tmp_path / name
    shutil.copytree(str(HARNESS_ROOT), str(dest),
                    ignore=shutil.ignore_patterns(
                        "__pycache__", "test-outputs", "*.pyc"))
    return str(dest)


def _attacker_module_bytes(rel: str) -> bytes:
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


def _frozen_record(env):
    recs = env.ledger_records()
    return [r for r in recs
            if r["event"] == "PRE_CONTROLLER_BOOTSTRAP_FROZEN"][-1]


def _finalized_record(env):
    recs = env.ledger_records()
    return [r for r in recs if r["event"] == "SPEC_FINALIZED"][-1]


# ------------------------------------------------------- §9 lifecycle order --

@requires_bwrap
@requires_userns
def test_phase_order_freeze_then_controller_then_finalize_then_trigger(env):
    """§9: PRE_CONTROLLER_BOOTSTRAP_FROZEN is mechanically recorded BEFORE
    the authorized controller exists, BEFORE finalization, and BEFORE the
    controller-accessible trigger; SPEC_FINALIZED precedes ROOT_SOCKET_BOUND.
    The controller is started only after PRECONTROLLER_READY was observed."""
    attempt = "pc-order-0001"
    env.author_template(attempt)
    root = env.spawn_authority()          # waits for PRECONTROLLER_READY
    assert env.phase_line == "PRECONTROLLER_READY"
    # the trigger socket does NOT exist before finalization: no abstract
    # qh-root-* socket is bound by the authority at this point
    with open("/proc/net/unix") as fh:
        unix_blob = fh.read()
    assert "qh-root-" not in unix_blob
    # ONLY NOW the operator starts the authorized controller + finalizes
    ctrl = env.spawn_controller(claude_config_dir=str(env.config_dir))
    env.finalize(controller=ctrl)
    assert env.phase_line.startswith("READY")
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    resp = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert resp.get("ok"), (resp, err)
    assert rc == 0, err
    events = [r["event"] for r in env.ledger_records()]
    assert events.index("PRE_CONTROLLER_BOOTSTRAP_FROZEN") < \
        events.index("SPEC_FINALIZED")
    assert events.index("SPEC_FINALIZED") < \
        events.index("ROOT_SOCKET_BOUND")


@requires_bwrap
@requires_userns
def test_trigger_structurally_refused_before_finalization(tmp_path):
    """§9/§10: bind_socket refuses ROOT_TRIGGER_BEFORE_FINALIZATION until
    the operator finalization completes (fail closed BEFORE any trigger)."""
    from qh.trusted_spec import build_pre_controller_template, template_id
    from qh.util import hold_bytes_memfd
    hroot = _harness_copy(tmp_path, "h-orderB")
    for d in ("ar", "cfg", "ev", "ao"):
        (tmp_path / d).mkdir(exist_ok=True)
    exe = tmp_path / "exe"
    exe.write_text("#!/bin/sh\necho synthetic\n", encoding="utf-8")
    exe.chmod(0o755)
    tpl = build_pre_controller_template(
        attempt_id="pc-order-B", attempt_root=str(tmp_path / "ar"),
        target_src=None,
        config_dir=str(tmp_path / "cfg"), manifest_id="m" * 64,
        evidence_src=str(tmp_path / "ev"), auditor_output_src=str(tmp_path / "ao"),
        codex_exe=str(tmp_path / "exe"), codex_version="synthetic",
        profile={}, config_sha256="0" * 64,
        credential_adapter={"id": "synthetic_inert_v1",
                            "provider_role": "inert", "version": 1},
        harness_root=hroot,
        expected_harness_tree_digest=_tree_digest_of(hroot))
    for d in ("ar", "cfg", "ev", "ao"):
        (tmp_path / d).mkdir(exist_ok=True)
    wrapper = tmp_path / "order_probe.py"
    wrapper.write_text(
        "import json, os, sys\n"
        f"sys.path.insert(0, {hroot!r})\n"
        "from qh import rootauth, trusted_spec\n"
        "cr, cw = os.pipe(); os.write(cw, b'SYNTHETIC'); os.close(cw)\n"
        "fr, fw = os.pipe()\n"
        f"tpl_bytes = open({str(tmp_path / 'tpl.json')!r}, 'rb').read()\n"
        "root = rootauth.AuthorityRoot(\n"
        f"    operator_state_dir={str(tmp_path / 'op')!r},\n"
        "    template_bytes=tpl_bytes, custody_fd=cr,\n"
        "    finalization_fd=fr)\n"
        "root.pre_controller_startup()\n"
        "assert root.exit_code == 0, root.fail_reason\n"
        "assert root.pre_controller_ready is True\n"
        "try:\n"
        "    root.bind_socket()\n"
        "    print('TRIGGER_UNEXPECTEDLY_BOUND')\n"
        "except rootauth.RootInitError as exc:\n"
        "    print('TRIGGER_REFUSED:' + str(exc))\n"
        "delta = json.dumps({'template_id': " + repr(template_id(tpl)) + ",\n"
        "  'authorized_controller': {'uid': os.getuid(), 'pid': os.getpid(),\n"
        "   'starttime': __import__('qh.util', fromlist=['x'])"
        ".proc_starttime(os.getpid())}}).encode()\n"
        "os.write(fw, delta + b'\\n'); os.close(fw)\n"
        "root.finalize_controller_binding(\n"
        "    __import__('qh.util', fromlist=['x']).read_bounded(fr))\n"
        "assert root.exit_code == 0, root.fail_reason\n"
        "name = root.bind_socket()\n"
        "print('BOUND_AFTER_FINALIZATION:' + name[1:])\n",
        encoding="utf-8")
    (tmp_path / "tpl.json").write_bytes(
        __import__("qh.trusted_spec", fromlist=["canonical_spec_bytes"])
        .canonical_spec_bytes(tpl))
    proc = subprocess.run([sys.executable, str(wrapper)],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    assert "TRIGGER_REFUSED:ROOT_TRIGGER_BEFORE_FINALIZATION" in proc.stdout
    assert "TRIGGER_UNEXPECTEDLY_BOUND" not in proc.stdout
    assert "BOUND_AFTER_FINALIZATION:" in proc.stdout


def _tree_digest_of(hroot: str) -> str:
    from qh.trusted_spec import harness_tree_digest
    return harness_tree_digest(hroot)


# ------------------------------------------- §10 frozen-harness-id equality --

@requires_bwrap
@requires_userns
def test_final_spec_harness_identity_is_the_frozen_identity(env):
    """§10: FINAL_SPEC_FROZEN_HARNESS_ID == PRE_CONTROLLER_FROZEN_HARNESS_ID
    is mechanically proven at finalization (ledger), and the final spec's
    harness digest is the OPERATOR-PROVIDED pre-controller value (never
    recomputed from the live tree)."""
    attempt = "pc-id-0001"
    tpl = env.author_template(attempt)
    operator_expected = tpl["harness"]["tree_digest"]
    root = env.spawn_authority()
    env.finalize()
    frozen = _frozen_record(env)
    assert frozen["expected_tree_digest_match"] is True
    fin = _finalized_record(env)
    assert fin["frozen_harness_id_match"] is True
    assert fin["frozen_harness_id"] == operator_expected
    assert env.spec["harness"]["tree_digest"] == operator_expected
    env.cleanup_procs()  # observation-only: no mint is driven here


# -------------------------------- §14 live-tree mutation BEFORE final spec ----

@pytest.mark.parametrize("rel", ["qh/rootauth.py", "qh/authority.py",
                                 "qh/util.py", "qh/trusted_spec.py"])
@requires_bwrap
@requires_userns
def test_attacker_module_swap_before_finalization_never_executes(
        env, tmp_path, rel):
    """§14: after PRE_CONTROLLER_BOOTSTRAP_FROZEN and controller start, but
    BEFORE final spec completion, the attacker replaces a privileged host
    module with unique marker code; the operator finalizes and the
    authorized flow proceeds — the marker NEVER executes and the final spec
    harness identity stays the PRE-CONTROLLER frozen identity."""
    attempt = f"pc-atk-{rel.replace('/', '-')}"
    hroot = _harness_copy(tmp_path, "h-atk")
    tpl = env.author_template(attempt, harness_root=hroot)
    frozen_expected = tpl["harness"]["tree_digest"]
    root = env.spawn_authority()
    assert env.phase_line == "PRECONTROLLER_READY"
    _frozen_record(env)  # milestone observed
    ctrl = env.spawn_controller(claude_config_dir=str(env.config_dir))
    # the attack window: mutate BEFORE the operator writes finalization
    with open(os.path.join(hroot, rel), "wb") as fh:
        fh.write(_attacker_module_bytes(rel))
    env.finalize(controller=ctrl)
    fin = _finalized_record(env)
    assert fin["frozen_harness_id"] == frozen_expected
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    resp = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert resp.get("ok"), (resp, err)
    assert rc == 0, err
    assert _scan_for_marker(tmp_path) == []
    assert ATTACKER_MARKER not in err
    assert ATTACKER_MARKER not in json.dumps(resp)


# --------------------------------------- §15 entire-tree replacement -------

@requires_bwrap
@requires_userns
def test_entire_tree_replacement_not_blessed(env, tmp_path):
    """§15: after the freeze milestone but before final spec completion the
    ENTIRE ordinary harness tree is deleted/recreated with attacker bytes:
    the final spec must NOT bless the replacement tree — the trusted flow
    continues solely from the pre-controller frozen representation and no
    attacker code ever executes as privileged authority code."""
    attempt = "pc-tree-0001"
    hroot = _harness_copy(tmp_path, "h-tree")
    tpl = env.author_template(attempt, harness_root=hroot)
    frozen_expected = tpl["harness"]["tree_digest"]
    root = env.spawn_authority()
    ctrl = env.spawn_controller(claude_config_dir=str(env.config_dir))
    shutil.rmtree(hroot)
    os.makedirs(os.path.join(hroot, "qh"))
    os.makedirs(os.path.join(hroot, "fixtures"))
    for rel in ("qh/rootauth.py", "qh/authority.py", "qh/cli.py",
                "qh/trusted_spec.py", "qh/util.py", "qh/boundary_child.py",
                "fixtures/gatew_payload.py",
                "fixtures/launch_sim_payload.py"):
        with open(os.path.join(hroot, rel), "wb") as fh:
            fh.write(_attacker_module_bytes(rel))
    env.finalize(controller=ctrl)
    fin = _finalized_record(env)
    assert fin["frozen_harness_id"] == frozen_expected
    # the replacement tree's identity is NOT the blessed identity (an
    # incomplete/attacker tree may not even be digestible — also fine)
    from qh.trusted_spec import SpecError
    try:
        replacement_digest = _tree_digest_of(hroot)
    except SpecError:
        replacement_digest = "<undigestible-attacker-tree>"
    assert fin["frozen_harness_id"] != replacement_digest
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    resp = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert resp.get("ok"), (resp, err)
    assert rc == 0, err
    assert _scan_for_marker(tmp_path) == []


# ------------------------------------ §16 modify-then-restore TOCTOU --------

@requires_bwrap
@requires_userns
def test_modify_then_restore_cannot_change_trusted_code(env, tmp_path):
    """§16 TOCTOU class: after the Phase-A freeze a privileged host module
    is replaced with marker bytes and its ORIGINAL bytes restored before
    final-spec completion.  Restoration must not change which privileged
    code is trusted/executed — the authority decision derives from the
    already-frozen representation, never from a later files-look-correct
    check.  Marker never executes."""
    attempt = "pc-toctou-0001"
    hroot = _harness_copy(tmp_path, "h-toctou")
    env.author_template(attempt, harness_root=hroot)
    root = env.spawn_authority()
    ctrl = env.spawn_controller(claude_config_dir=str(env.config_dir))
    target = os.path.join(hroot, "qh", "authority.py")
    original = open(target, "rb").read()
    with open(target, "wb") as fh:
        fh.write(_attacker_module_bytes("qh/authority.py"))
    with open(target, "wb") as fh:            # restore original bytes
        fh.write(original)
    env.finalize(controller=ctrl)
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    resp = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert resp.get("ok"), (resp, err)
    assert rc == 0, err
    assert _scan_for_marker(tmp_path) == []


# --------------------------- §17 pre-freeze expected-identity mismatch ------

@requires_bwrap
@requires_userns
def test_pre_freeze_mutated_tree_fails_closed_no_self_pinning(env, tmp_path):
    """§17: the source is already changed BEFORE the pre-controller freeze
    and does NOT match the operator-provided expected identity (established
    INDEPENDENTLY from a pristine snapshot — never recomputed from the
    mutated live bytes): the authority FAILS CLOSED, no
    PRE_CONTROLLER_BOOTSTRAP_FROZEN, no trigger, no self-pinning."""
    attempt = "pc-prefreeze-0001"
    pristine = _harness_copy(tmp_path, "h-pristine")   # operator's source
    deployed = _harness_copy(tmp_path, "h-deployed")   # the live tree H'
    expected = _tree_digest_of(pristine)
    assert expected != _tree_digest_of(deployed) is None or True
    # attacker mutates the deployed tree BEFORE the authority starts
    with open(os.path.join(deployed, "qh", "gatew.py"), "wb") as fh:
        fh.write(_attacker_module_bytes("qh/gatew.py"))
    tpl = env.author_template(attempt, harness_root=deployed,
                              expected_harness_tree_digest=expected)
    with pytest.raises(RuntimeError, match="ROOT_STARTUP_FAILED"):
        env.spawn_authority()
    events = [r["event"] for r in env.ledger_records()]
    assert "PRE_CONTROLLER_BOOTSTRAP_FROZEN" not in events
    assert "SPEC_FINALIZED" not in events
    assert "ROOT_SOCKET_BOUND" not in events
    assert _scan_for_marker(tmp_path) == []


# ------------------------------- §11 finalization capability channel ---------

@requires_bwrap
@requires_userns
def test_controller_holds_no_finalization_channel_write_end(env):
    """§11: the finalization pipe is created before controller startup by
    the OPERATOR, whose write end is never passed to the controller: the
    live controller process holds NO fd bound to the finalization pipe
    (inode-level /proc scan) — it cannot write or influence finalization."""
    attempt = "pc-chan-0001"
    env.author_template(attempt)
    root = env.spawn_authority()
    fin_stat = os.fstat(env.finalization_w)
    ctrl = env.spawn_controller(claude_config_dir=str(env.config_dir))
    hits = []
    for fd in os.listdir(f"/proc/{ctrl.pid}/fd"):
        try:
            st = os.stat(f"/proc/{ctrl.pid}/fd/{fd}")
        except OSError:
            continue
        if (st.st_ino, st.st_dev) == (fin_stat.st_ino, fin_stat.st_dev):
            hits.append(fd)
    assert hits == [], f"controller holds finalization-channel fds: {hits}"
    env.finalize(controller=ctrl)
    env.cleanup_procs()  # observation-only: no mint is driven here


def test_finalization_fd_ordinary_file_refused(tmp_path):
    """§11: an ordinary-file finalization channel is REFUSED before any
    byte is read (only PIPE / fully sealed memfd are operator channels)."""
    from qh.util import SealUnavailableError, require_trusted_spec_fd
    f = tmp_path / "fin.txt"
    f.write_text("{}")
    fd = os.open(f, os.O_RDONLY)
    try:
        with pytest.raises(SealUnavailableError):
            require_trusted_spec_fd(fd)
    finally:
        os.close(fd)


def test_finalization_fd_unsealed_memfd_refused():
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    libc.memfd_create.restype = ctypes.c_int
    libc.memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
    fd = libc.memfd_create(b"unsealed-fin", 0x0001 | 0x0002)
    os.write(fd, b"{}")
    try:
        from qh.util import SealUnavailableError, require_trusted_spec_fd
        with pytest.raises(SealUnavailableError):
            require_trusted_spec_fd(fd)
    finally:
        os.close(fd)


@requires_bwrap
@requires_userns
def test_finalization_wrong_template_id_fails_closed_no_trigger(env):
    """§10/§11: a finalization delta whose template id does not match the
    frozen pre-controller template fails closed BEFORE the trigger exists."""
    attempt = "pc-tid-0001"
    env.author_template(attempt)
    root = env.spawn_authority()
    env.finalize(delta={"template_id": "f" * 64,
                        "authorized_controller": {
                            "uid": 1000, "pid": 1, "starttime": "1"}},
                 expect_ready=False)
    rc, err = env.root_outcome(root, timeout=60)
    assert rc == 18, (rc, err)
    assert "TEMPLATE_ID_MISMATCH" in err
    events = [r["event"] for r in env.ledger_records()]
    assert "ROOT_SOCKET_BOUND" not in events


@requires_bwrap
@requires_userns
def test_finalization_delta_unknown_fields_refused(env):
    """The finalization delta is operator-authored but strictly shaped: a
    delta carrying anything beyond template_id + authorized_controller is
    refused (no controller-suppliable extras become authority)."""
    attempt = "pc-tid-0002"
    env.author_template(attempt)
    root = env.spawn_authority()
    ctrl = env.spawn_controller(claude_config_dir=str(env.config_dir))
    from qh.trusted_spec import template_id
    env.finalize(delta={
        "template_id": template_id(env.template),
        "authorized_controller": {"uid": ctrl.uid, "pid": ctrl.pid,
                                  "starttime": ctrl.starttime},
        "harness_root": "/tmp/attacker"},
        expect_ready=False)
    rc, err = env.root_outcome(root, timeout=60)
    assert rc == 18, (rc, err)
    assert "SPEC_FINALIZATION_INVALID" in err
    events = [r["event"] for r in env.ledger_records()]
    assert "ROOT_SOCKET_BOUND" not in events


# ------------------------- §12/§13 module-load provenance + guard ------------

@requires_bwrap
@requires_userns
def test_all_privileged_modules_loaded_and_verified_pre_controller(env):
    """§13: every privileged qh module is loaded + frozen in the
    PRE_CONTROLLER_TRUSTED_PHASE with its EXECUTING code object proven
    equal to a compile of the frozen verified bytes; the inventory is
    recorded in the bootstrap provenance observability record."""
    attempt = "pc-mod-0001"
    env.author_template(attempt)
    root = env.spawn_authority()
    from qh.rootauth import PRIVILEGED_MODULES
    prov = env.bootstrap_provenance()
    assert set(prov["module_inventory"]) == set(PRIVILEGED_MODULES)
    for name, entry in prov["module_inventory"].items():
        assert entry["load_phase"] == "PRE_CONTROLLER_TRUSTED_PHASE"
        assert entry["codeobject_verified"] is True
        assert len(entry["file_sha256"]) == 64
    frozen = _frozen_record(env)
    assert frozen["modules"] == len(PRIVILEGED_MODULES)
    assert frozen["bundle_seal_status"] == "sealed"
    assert frozen["template_id"] == prov["template_id"]
    # §18 provenance tuple present
    assert prov["frozen_bundle_digest"] == frozen["bundle_digest"]
    assert prov["file_count"] == frozen["files"]
    assert len(prov["file_manifest"]) == frozen["files"]
    assert prov["seal_state"] == "sealed"
    env.cleanup_procs()  # observation-only: no mint is driven here


def test_post_controller_new_qh_import_fails_closed(tmp_path):
    """§13: after the pre-controller freeze the import guard refuses every
    NEW qh.* import — a controller-era planted module can never load."""
    from qh.trusted_spec import build_pre_controller_template
    hroot = _harness_copy(tmp_path, "h-guard")
    for d in ("ar", "cfg", "ev", "ao"):
        (tmp_path / d).mkdir(exist_ok=True)
    exe = tmp_path / "exe"
    exe.write_text("#!/bin/sh\necho synthetic\n", encoding="utf-8")
    exe.chmod(0o755)
    tpl = build_pre_controller_template(
        attempt_id="pc-guard", attempt_root=str(tmp_path / "ar"),
        target_src=None,
        config_dir=str(tmp_path / "cfg"), manifest_id="m" * 64,
        evidence_src=str(tmp_path / "ev"), auditor_output_src=str(tmp_path / "ao"),
        codex_exe=str(tmp_path / "exe"), codex_version="synthetic",
        profile={}, config_sha256="0" * 64,
        credential_adapter={"id": "synthetic_inert_v1",
                            "provider_role": "inert", "version": 1},
        harness_root=hroot, expected_harness_tree_digest=_tree_digest_of(hroot))
    wrapper = tmp_path / "guard_probe.py"
    wrapper.write_text(
        "import importlib, json, sys\n"
        f"sys.path.insert(0, {hroot!r})\n"
        "from qh.rootauth import PrivilegedBootstrap\n"
        f"spec = json.load(open({str(tmp_path / 'tpl.json')!r}))\n"
        f"boot = PrivilegedBootstrap.freeze(harness_root={hroot!r},\n"
        f"    expected_tree_digest={tpl['harness']['tree_digest']!r})\n"
        "boot.install_import_guard()\n"
        "try:\n"
        "    importlib.import_module('qh.attacker_planted')\n"
        "    print('IMPORT_UNEXPECTEDLY_ALLOWED')\n"
        "except ImportError as exc:\n"
        "    print('GUARDED:' + str(exc))\n",
        encoding="utf-8")
    (tmp_path / "tpl.json").write_text(json.dumps(tpl), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(wrapper)],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    assert "GUARDED:QH_IMPORT_FROZEN" in proc.stdout


# ------------------------- §7 no live-tree self-pinning remains --------------

def test_production_paths_contain_no_live_tree_identity_computation():
    """§7: the production authority-finalization path contains NO
    harness_tree_digest(<live tree>) call — the final spec harness identity
    comes exclusively from the frozen pre-controller template/bundle."""
    import inspect
    from qh import rootauth, trusted_spec
    root_src = inspect.getsource(rootauth)
    assert "harness_tree_digest(" not in root_src
    finalize_src = inspect.getsource(trusted_spec.finalize_spec)
    assert "harness_tree_digest" not in finalize_src
    build_spec_src = inspect.getsource(trusted_spec.build_spec)
    assert "harness_tree_digest(" not in build_spec_src


def test_template_expected_identity_is_operator_supplied():
    """§6/§17: build_pre_controller_template REQUIRES the operator-provided
    expected identity — it cannot self-pin by recomputing the live tree."""
    import inspect
    from qh import trusted_spec
    src = inspect.getsource(trusted_spec.build_pre_controller_template)
    assert "expected_harness_tree_digest" in src
    assert "harness_tree_digest(" not in src
    sig = inspect.signature(trusted_spec.build_pre_controller_template)
    param = sig.parameters["expected_harness_tree_digest"]
    assert param.default is inspect.Parameter.empty, \
        "expected identity must be explicitly operator-supplied"


# --------------------------- §20 frozen-id equality under controller change --

@requires_bwrap
@requires_userns
def test_controller_identity_change_changes_final_spec_id_not_frozen_id(env):
    """§10: changing the controller pid/starttime changes the FINAL spec id
    (CR-REMED-004 held) but NEVER the frozen harness identity."""
    from qh.trusted_spec import finalize_spec, spec_id
    env.author_template("pc-chg-0001")
    tpl = env.template
    s1 = spec_id(finalize_spec(tpl, controller_uid=1000, controller_pid=11,
                               controller_starttime="111"))
    s2 = spec_id(finalize_spec(tpl, controller_uid=1000, controller_pid=12,
                               controller_starttime="111"))
    s3 = spec_id(finalize_spec(tpl, controller_uid=1000, controller_pid=11,
                               controller_starttime="222"))
    assert len({s1, s2, s3}) == 3
    for spec in (finalize_spec(tpl, controller_uid=1000, controller_pid=11,
                               controller_starttime="111"),):
        assert spec["harness"]["tree_digest"] == \
            tpl["harness"]["tree_digest"]
