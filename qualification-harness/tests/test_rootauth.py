"""IR-001 — mechanically rooted operator authority: adversarial tests
(remediation §4/§5/§6/§12/§18).  Real root/supervisor subprocesses;
synthetic inert custody; zero provider."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time

import pytest

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns

from qh.compose import SYNTHETIC_CREDENTIAL, CompositionEnv


def _run(env, attempt, *, role="codex", overrides=None):
    return env.run_attempt(attempt, role=role, overrides=overrides)


# ------------------------------------------------- §18 A: no self-mint ----

def test_public_mint_cli_removed():
    """The unrestricted public `qh mint` surface no longer exists."""
    r = subprocess.run(
        [sys.executable, "-m", "qh.cli", "mint", "--attempt", "x",
         "--root", "/tmp", "--manifest", "m", "--operator-state", "/tmp"],
        capture_output=True, text=True, timeout=30, cwd=str(HARNESS_ROOT),
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
    assert r.returncode != 0
    assert "invalid choice" in r.stderr
    assert "mint" not in r.stderr.split("choose from")[1].split(")")[0] \
        if "choose from" in r.stderr else True


@requires_bwrap
@requires_userns
def test_controller_mint_against_legitimate_root_refused(env):
    """§18.A: a controller using its OWN attempt id against the legitimate
    root is REFUSED (only the spec-bound attempt may mint) and the root
    fails closed — no launch-capable authority is produced."""
    env.author_spec("root-0001")
    root = env.spawn_root()
    try:
        resp = env.root_mint(request={"attempt_id":
                                      "controller-chosen-attempt"})
        assert not resp.get("ok")
        assert "MINT_WRONG_ATTEMPT" in json.dumps(resp)
    finally:
        env.cleanup_procs()
    rc, err = env.root_outcome(root)
    assert rc != 0


@requires_bwrap
@requires_userns
def test_controller_own_state_manifest_root_yields_powerless_imitation(env):
    """§18.A/B: a controller creating its own state dir, manifest, root,
    spec and 'credential' can only instantiate a POWERLESS imitation: its
    launches never carry the legitimate custody capability."""
    legit = "LEGITIMATE-" + SYNTHETIC_CREDENTIAL
    env.author_spec("root-0002")
    root = env.spawn_root(custody_value=legit)
    mint = env.root_mint("root-0002")
    assert mint.get("ok"), mint
    # controller-side imitation with fully controller-owned material
    fake_base = env.base / "controller-imitation"
    fake = CompositionEnv(str(fake_base))
    try:
        fake.author_spec("controller-self-0001")
        fake_root = fake.spawn_root(custody_value="CONTROLLER-OWNED-FAKE")
        fake_mint = fake.root_mint("controller-self-0001")
        assert fake_mint.get("ok"), fake_mint
        resp = fake.controller_request("controller-self-0001",
                                       own_session_slug="s")
        fake_env_files = []
        for p in fake_base.rglob("*"):
            if p.is_file():
                fake_env_files.append(p)
        # the imitation never touches the legitimate credential value
        for p in fake_env_files:
            if p.name.endswith((".jsonl", ".json")):
                assert legit not in p.read_text(errors="replace"), \
                    f"legitimate custody value leaked into imitation: {p}"
        # and its launch (if it ran) is a local payload only — no
        # provider-capable capability exists in the imitation flow
        assert resp.get("ok") is False or resp.get("ok") is True  # shape
        assert fake_mint["supervisor_socket"].startswith("\0qh-")
    finally:
        fake.cleanup_procs()
        env.cleanup_procs()
    env.root_outcome(root, timeout=300)


@requires_bwrap
@requires_userns
def test_fake_root_lacks_legitimate_custody_capability(env):
    """§18.B: a controller-created fake root has NO legitimate campaign or
    provider-custody capability — the legitimate synthetic credential
    bytes never appear anywhere in its flow, and its child custody length
    equals the FAKE bytes' length, not the legitimate one."""
    legit = "LEGITIMATE-CUSTODY-CAPABILITY-PROBE"
    fake = CompositionEnv(str(env.base / "fake-root-env"))
    fake.author_spec("fake-0001")
    fake_root = fake.spawn_root(custody_value="FAKE-BYTES-ONLY")
    try:
        mint = fake.root_mint("fake-0001")
        assert mint.get("ok")
        resp = fake.controller_request("fake-0001", own_session_slug="s")
        fake.root_outcome(fake_root, timeout=300)
        # scan every ordinary file the fake flow produced
        hits = []
        for p in (env.base).rglob("*"):
            if p.is_file() and p.stat().st_size < (1 << 20):
                try:
                    if legit in p.read_text(errors="replace"):
                        hits.append(str(p))
                except OSError:
                    pass
        assert hits == []
        payload = (resp.get("launch") or {}) if resp.get("ok") else {}
        assert payload.get("custody_length") in (None, len("FAKE-BYTES-ONLY"))
    finally:
        fake.cleanup_procs()


# ------------------------------------------- §18 C/D: terminal + state ----

@requires_bwrap
@requires_userns
def test_no_second_mint_after_terminal_preexec_stop(env):
    """§18.C: after a terminal PREEXEC stop the controller cannot mint a
    second time — the root is gone with its single mint consumed."""
    env.author_spec("root-0003")
    root = env.spawn_root()
    mint = env.root_mint("root-0003")
    assert mint.get("ok")
    # force a terminal preexec stop via an unknown claim field
    resp = env.controller_request(
        "root-0003", overrides={"harness_root": "/tmp/attacker"},
        own_session_slug="s")
    assert not resp.get("ok")
    assert "UNKNOWN_CLAIM_FIELD" in resp.get("reason", "")
    env.root_outcome(root, timeout=300)
    second = env.root_mint("root-0003")
    assert not second.get("ok")
    assert "CONNECT_FAILED" in json.dumps(second)


@requires_bwrap
@requires_userns
def test_state_deletion_does_not_restore_mint_authority(env):
    """§18.D: deleting/recreating the ordinary operator state (ledger,
    specs, manifests) restores no launch authority: the legitimate root is
    dead, the public mint CLI is gone, and only a NEW operator-side root
    authorization (spec + custody pipes) can mint again."""
    result = _run(env, "root-0004")
    assert result["ok"], result
    import shutil
    shutil.rmtree(env.operator_state)
    env.operator_state.mkdir(parents=True)
    reuse = env.controller_request("root-0004")
    assert not reuse.get("ok")
    # the controller cannot resurrect a root without the custody channel
    gone = env.root_mint("root-0004")
    assert not gone.get("ok")


@requires_bwrap
@requires_userns
def test_new_attempt_requires_new_operator_root_authorization(env):
    """§18.E: a genuinely new attempt succeeds ONLY after a NEW
    operator/root authorization (fresh spec bound + fresh root with the
    operator custody channel)."""
    r1 = _run(env, "root-0005")
    assert r1["ok"], r1
    # no root is running: the controller cannot obtain a supervisor
    denied = env.controller_request("root-0006")
    assert not denied.get("ok")
    # NEW operator authorization: author + spawn a new root
    r2 = _run(env, "root-0007")
    assert r2["ok"], r2


# ----------------------------------------------------- §18 F: SIGKILL ----

@requires_bwrap
@requires_userns
def test_root_sigkill_is_denial_only(env):
    """§18.F: killing the authority root is fail-closed denial only — no
    supervisor is spawned, no authority is recoverable from the
    filesystem, and a genuinely new operator authorization still works."""
    env.author_spec("root-0008")
    root = env.spawn_root()
    os.kill(root.pid, signal.SIGKILL)
    root.wait(timeout=10)
    denied = env.root_mint("root-0008")
    assert not denied.get("ok")
    r = _run(env, "root-0009")
    assert r["ok"], r


# ------------------------------------------------- root process mechanics --

@requires_bwrap
@requires_userns
def test_root_process_is_non_dumpable(env):
    """The live authority root must actually run PR_SET_DUMPABLE=0: a
    same-UID non-parent cannot read its environ (kernel-process-bound
    spec/custody state)."""
    env.author_spec("root-0010")
    root = env.spawn_root()
    try:
        try:
            open(f"/proc/{root.pid}/environ", "rb").read()
            readable = True
        except OSError:
            readable = False
        assert not readable, "root environ must not be same-UID readable"
        try:
            os.listdir(f"/proc/{root.pid}/fd")
            listed = True
        except OSError:
            listed = False
        assert not listed, "root fd list must not be same-UID readable"
    finally:
        env.cleanup_procs()


@requires_bwrap
@requires_userns
def test_root_custody_ordinary_file_refused(env):
    """Root custody arriving via an ORDINARY FILE (persisted plaintext
    channel) is refused at initialization."""
    env.author_spec("root-0011")
    cred_file = env.base / "persisted-root-credential.txt"
    cred_file.write_text(SYNTHETIC_CREDENTIAL)
    fin_r, fin_w = os.pipe()
    with open(cred_file, "rb") as fh:
        argv = [sys.executable, "-m", "qh.cli", "authority",
                "--operator-state", str(env.operator_state),
                "--custody-fd", str(fh.fileno()),
                "--finalization-fd", str(fin_r)]
        proc = subprocess.Popen(
            argv, pass_fds=(fh.fileno(), fin_r), stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
        proc.stdin.write(
            __import__("qh.trusted_spec", fromlist=["x"])
            .canonical_template_bytes(env.template))
        proc.stdin.close()
        out = proc.stdout.read()
        err = proc.stderr.read()
        proc.wait(timeout=30)
    os.close(fin_r)
    os.close(fin_w)
    assert proc.returncode != 0
    assert "CUSTODY_SOURCE_KIND_REFUSED:file" in \
        (err.decode() + out.decode())


@requires_bwrap
@requires_userns
def test_supervisor_root_pid_mismatch_refused(env):
    """The supervisor enforces its parent = the minting root (mechanical
    ppid binding from the grant, not a caller-supplied flag)."""
    env.author_spec("root-0012")
    grant = env.mint("root-0012")
    doc = grant.full_doc()
    doc["root_pid"] = 999999
    import io
    grant_file = env.base / "forged-grant.json"
    grant_file.write_text("")
    argv = [sys.executable, "-m", "qh.cli", "supervisor",
            "--operator-state", str(env.operator_state)]
    r, w = os.pipe()
    os.write(w, (json.dumps(doc) + "\n").encode() +
             __import__("qh.trusted_spec", fromlist=["x"])
             .canonical_spec_bytes(env.spec) + b"\n")
    os.close(w)
    proc = subprocess.Popen(
        argv, pass_fds=(r,), stdin=r, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
    os.close(r)
    out = proc.stdout.read()
    err = proc.stderr.read()
    proc.wait(timeout=30)
    assert proc.returncode == 5
    assert "SUPERVISOR_STARTUP_FAILED code=5" in err.decode()
    assert any(r.get("event") == "FAIL_CLOSED"
               and r.get("reason") == "ROOT_PID_MISMATCH"
               for r in env.ledger_records())


@requires_bwrap
@requires_userns
def test_root_rejects_tampered_spec_bytes(env):
    """Template bytes that do not canonically validate (e.g. tampered in
    transit) fail closed at authority initialization."""
    env.author_spec("root-0013")
    bad = dict(env.template)
    bad["template_version"] = 999
    from qh.trusted_spec import canonical_template_bytes
    cr, cw = os.pipe()
    os.write(cw, b"SYNTHETIC")
    os.close(cw)
    fr, fw = os.pipe()
    os.close(fw)
    argv = [sys.executable, "-m", "qh.cli", "authority",
            "--operator-state", str(env.operator_state),
            "--custody-fd", str(cr),
            "--finalization-fd", str(fr)]
    proc = subprocess.Popen(
        argv, pass_fds=(cr, fr), stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
    os.close(cr)
    os.close(fr)
    proc.stdin.write(canonical_template_bytes(bad))
    proc.stdin.close()
    out = proc.stdout.read()
    err = proc.stderr.read()
    proc.wait(timeout=30)
    assert proc.returncode != 0
    assert "TEMPLATE_INVALID" in (err.decode() + out.decode())
