"""C-2 / G-1 — process-bound one-shot launch authority tests over the
remediated authority-root flow (real root/supervisor subprocesses;
synthetic inert custody; zero provider).  Yama-failure simulation uses a
monkeypatched REAL-reader seam in-process (no production override
exists)."""
from __future__ import annotations

import json
import os
import signal

import pytest

from conftest import requires_bwrap, requires_userns


def _run_attempt(env, attempt, *, own_slug="own-slug", overrides=None):
    return env.run_attempt(attempt, overrides=overrides)


@requires_bwrap
@requires_userns
def test_single_use_pass(env):
    result = _run_attempt(env, "c2-0001")
    assert result["ok"], result
    assert result["marker_present"]
    assert result["response"]["state"] == "TERMINAL"


@requires_bwrap
@requires_userns
def test_second_use_and_replay_fail(env):
    result = _run_attempt(env, "c2-0002")
    assert result["ok"], result
    reuse = env.controller_request("c2-0002", own_session_slug="s2")
    assert not reuse.get("ok")
    assert "CONNECT_FAILED" in json.dumps(reuse)


@requires_bwrap
@requires_userns
def test_wrong_attempt_fail(env):
    env.author_spec("c2-0003-real")
    root = env.spawn_root()
    mint = env.root_mint("c2-0003-real")
    assert mint.get("ok")
    response = env.controller_request(
        "c2-0003-real", overrides={"attempt_id": "c2-0003-wrong"},
        own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert not response.get("ok")
    assert response.get("reason") == "WRONG_ATTEMPT"
    assert response["state"] == "TERMINAL_PREEXEC_STOP"
    assert rc == 9


@requires_bwrap
@requires_userns
def test_root_identity_change_fail(env):
    """The grant-bound attempt ROOT (not a request claim): delete +
    recreate the root directory object => refusal."""
    env.author_spec("c2-0004")
    root = env.spawn_root()
    mint = env.root_mint("c2-0004")
    assert mint.get("ok")
    import shutil
    shutil.rmtree(env.root)
    env.root.mkdir(parents=True)
    response = env.controller_request("c2-0004", own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert not response.get("ok")
    assert "ROOT_IDENTITY_CHANGED" in response.get("reason", "")
    assert rc == 9


@requires_bwrap
@requires_userns
def test_root_recreation_does_not_restore_authority(env):
    """Terminal stop, then the attempt root is deleted and recreated:
    no relaunch is possible (authority was never in the filesystem)."""
    env.author_spec("c2-0005")
    root = env.spawn_root()
    mint = env.root_mint("c2-0005")
    assert mint.get("ok")
    response = env.controller_request(
        "c2-0005", overrides={"controller_starttime": "1"},
        own_session_slug="s")
    rc, _err = env.root_outcome(root, timeout=300)
    assert rc == 9
    assert not response.get("ok")
    assert response["state"] == "TERMINAL_PREEXEC_STOP"
    import shutil
    shutil.rmtree(env.root)
    env.root.mkdir(parents=True)
    reuse = env.controller_request("c2-0005")
    assert not reuse.get("ok")


@requires_bwrap
@requires_userns
def test_preexec_stop_is_terminal(env):
    """C4′ binding mismatch (claimed starttime) → terminal PREEXEC_STOP;
    the same bound grant cannot return to launchable."""
    env.author_spec("c2-0006")
    root = env.spawn_root()
    mint = env.root_mint("c2-0006")
    assert mint.get("ok")
    response = env.controller_request(
        "c2-0006", overrides={"controller_starttime": "1"},
        own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert not response.get("ok")
    assert response["state"] == "TERMINAL_PREEXEC_STOP"
    assert rc == 9
    assert "STARTTIME_MISMATCH" in response["reason"]
    reuse = env.controller_request("c2-0006")
    assert not reuse.get("ok")


@requires_bwrap
@requires_userns
def test_ledger_deletion_cannot_restore_authority(env):
    """After a completed launch, deleting/recreating the observability
    ledger and every state file restores nothing: the authority root is
    dead and nothing listens."""
    result = _run_attempt(env, "c2-0007")
    assert result["ok"], result
    op = env.operator_state
    ledger = op / "ledger.jsonl"
    assert ledger.is_file()
    ledger.unlink()
    ledger.write_text("")
    reuse = env.controller_request("c2-0007")
    assert not reuse.get("ok")
    assert "CONNECT_FAILED" in json.dumps(reuse)


@requires_bwrap
@requires_userns
def test_sigkill_fail_closed_denial_only(env):
    """Supervisor SIGKILL => denial (DoS) only; no authority recovery;
    a genuinely NEW attempt with a fresh root authorization works."""
    env.author_spec("c2-0008")
    root = env.spawn_root()
    mint = env.root_mint("c2-0008")
    assert mint.get("ok")
    sup_pid = mint["supervisor_pid"]
    os.kill(sup_pid, signal.SIGKILL)
    denied = env.controller_request("c2-0008")
    assert not denied.get("ok")
    env.root_outcome(root, timeout=60)
    # same attempt cannot be re-minted (ledger append discipline)
    from qh.authority import AuthorityError
    with pytest.raises(AuthorityError):
        env.mint("c2-0008")
    # a NEW attempt mints and runs fine
    result = _run_attempt(env, "c2-0009")
    assert result["ok"], result


@requires_bwrap
@requires_userns
def test_campaign_engagement_accounting_untouched(env):
    """Pre-inference PREEXEC stop and attempt-grant consumption never
    consume campaign auditor/model authority."""
    before = env.engagements.snapshot()
    # terminal preexec stop flow (unknown claim field)
    result = _run_attempt(env, "c2-0010",
                          overrides={"harness_root": "/tmp/x"})
    assert not result["ok"]
    assert result["response"]["state"] == "TERMINAL_PREEXEC_STOP"
    mid = env.engagements.snapshot()
    assert before == mid
    # happy path (consumed grant + protected local launch)
    result = _run_attempt(env, "c2-0011")
    assert result["ok"], result
    after = env.engagements.snapshot()
    assert before == after
    assert result["response"]["engagements"] == before


@requires_bwrap
@requires_userns
def test_copied_grant_file_refused(env):
    """A grant carried in an ordinary FILE (a copied grant) is refused
    by the supervisor — authority only travels via pipes."""
    env.author_spec("c2-0012")
    grant = env.mint("c2-0012")
    f = env.base / "copied-grant.json"
    from qh.trusted_spec import canonical_spec_bytes
    f.write_text(json.dumps(grant.full_doc()) + "\n")
    proc = env.spawn_supervisor(grant, grant_stdin_file=str(f))
    rc, err = env.supervisor_outcome(proc)
    assert rc == 3
    assert "not a pipe" in err


@requires_bwrap
@requires_userns
def test_yama_failure_simulation_terminal(monkeypatch, env):
    """Yama ptrace_scope < 1 => fail-closed terminal stop at startup
    (simulated by monkeypatching the REAL reader — the production CLI
    has no override)."""
    from qh import authority
    monkeypatch.setattr(authority, "read_yama_ptrace_scope", lambda: 0)
    from qh.authority import Supervisor
    from qh.trusted_spec import spec_id
    env.author_spec("c2-0013")
    grant = env.mint("c2-0013")
    grant.root_pid = None
    cr, cw = os.pipe()
    os.write(cw, b"SYNTHETIC-INERT")
    os.close(cw)
    sup = Supervisor(grant=grant, spec=env.spec, spec_id=spec_id(env.spec),
                     operator_state_dir=str(env.operator_state),
                     custody_fd=cr, policy=authority.SupervisorPolicy(
                         set_dumpable=False))
    sup.startup()
    assert sup.exit_code == 6
    recs = [r for r in env.ledger_records()
            if r.get("reason") == "YAMA_PTRACE_SCOPE_LT_1"]
    assert recs, "terminal preexec stop must be recorded"
    denied = env.controller_request("c2-0013")
    assert not denied.get("ok")


@requires_bwrap
@requires_userns
def test_custody_file_source_terminal_stop(env):
    """Custody arriving via an ordinary file (controller-readable
    persisted plaintext channel) => establishment fails closed."""
    env.author_spec("c2-0014")
    grant = env.mint("c2-0014")
    from qh.compose import SYNTHETIC_CREDENTIAL
    cred_file = env.base / "persisted-credential.txt"
    cred_file.write_text(SYNTHETIC_CREDENTIAL)
    proc = env.spawn_supervisor(grant, custody_value=None,
                                custody_file=str(cred_file))
    line = proc.stdout.readline().decode()
    assert line.startswith("READY")
    response = env.controller_request("c2-0014", own_session_slug="s")
    rc, err = env.supervisor_outcome(proc)
    assert not response.get("ok")
    assert "CUSTODY_ESTABLISH_FAILED" in response.get("reason", "")
    assert response["state"] == "TERMINAL_PREEXEC_STOP"


@requires_bwrap
@requires_userns
def test_no_custody_fd_terminal_stop(env):
    env.author_spec("c2-0015")
    grant = env.mint("c2-0015")
    proc = env.spawn_supervisor(grant, custody_value=None)
    line = proc.stdout.readline().decode()
    assert line.startswith("READY")
    response = env.controller_request("c2-0015", own_session_slug="s")
    rc, err = env.supervisor_outcome(proc)
    assert not response.get("ok")
    assert "CUSTODY_FD_NOT_PROVIDED" in response.get("reason", "")
    assert rc == 9


@requires_bwrap
@requires_userns
def test_supervisor_process_is_non_dumpable(env):
    """The live supervisor must actually run PR_SET_DUMPABLE=0
    (kernel-process-bound authority)."""
    env.author_spec("c2-0017")
    root = env.spawn_root()
    mint = env.root_mint("c2-0017")
    assert mint.get("ok")
    sup_pid = mint["supervisor_pid"]
    try:
        try:
            open(f"/proc/{sup_pid}/environ", "rb").read()
            readable = True
        except OSError:
            readable = False
        assert not readable, "supervisor environ must not be same-uid " \
            "readable (dumpable=0)"
    finally:
        env.cleanup_procs()
