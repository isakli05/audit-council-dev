"""C-2 / G-1 — process-bound one-shot launch authority tests (real
supervisor subprocesses; synthetic inert custody; zero provider)."""
from __future__ import annotations

import json
import os
import signal
import time

import pytest

from conftest import requires_bwrap, requires_userns


def _run_attempt(env, attempt, *, own_slug="own-slug", overrides=None,
                 env_claims=None, **sup_kwargs):
    grant = env.mint(attempt)
    sup = env.start_supervisor(grant, **sup_kwargs)
    response = env.controller_request(attempt, overrides=overrides,
                                      env_claims=env_claims,
                                      own_session_slug=own_slug)
    rc, err = env.supervisor_outcome(sup)
    return response, rc, err


@requires_bwrap
@requires_userns
def test_single_use_pass(env):
    response, rc, err = _run_attempt(env, "c2-0001")
    assert response.get("ok"), (response, err)
    assert rc == 0
    assert (env.auditor_output / "launch-sim-marker.txt").is_file()
    assert response["state"] == "TERMINAL"


@requires_bwrap
@requires_userns
def test_second_use_and_replay_fail(env):
    response, rc, err = _run_attempt(env, "c2-0002")
    assert response.get("ok"), (response, err)
    reuse = env.controller_request("c2-0002", own_session_slug="s2")
    assert not reuse.get("ok")
    assert "CONNECT_FAILED" in json.dumps(reuse)


@requires_bwrap
@requires_userns
def test_wrong_attempt_fail(env):
    grant = env.mint("c2-0003-real")
    sup = env.start_supervisor(grant)
    response = env.controller_request("c2-0003-real",
                                      overrides={"attempt_id":
                                                 "c2-0003-wrong"},
                                      own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
    assert not response.get("ok")
    assert "WRONG_ATTEMPT" in response.get("reason", "")
    assert response["state"] == "TERMINAL_PREEXEC_STOP"
    assert rc == 9


@requires_bwrap
@requires_userns
def test_wrong_root_fail(env):
    grant = env.mint("c2-0004")
    sup = env.start_supervisor(grant)
    fake_root = env.base / "not-the-root"
    fake_root.mkdir(exist_ok=True)
    response = env.controller_request(
        "c2-0004", overrides={"root": str(fake_root)},
        own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
    assert not response.get("ok")
    assert "WRONG_ROOT" in response.get("reason", "")
    assert rc == 9


@requires_bwrap
@requires_userns
def test_root_recreation_does_not_restore_authority(env):
    """Terminal stop, then the attempt root is deleted and recreated:
    no relaunch is possible (authority was never in the filesystem)."""
    grant = env.mint("c2-0005")
    sup = env.start_supervisor(grant)
    # force a terminal preexec stop: manifest the grant never bound
    response = env.controller_request(
        "c2-0005", overrides={"manifest_id": "0" * 64},
        own_session_slug="s")
    rc, _err = env.supervisor_outcome(sup)
    assert rc == 9
    assert not response.get("ok")
    assert response["state"] == "TERMINAL_PREEXEC_STOP"
    # delete + recreate the root directory: nothing restores authority
    import shutil
    shutil.rmtree(env.root)
    env.root.mkdir(parents=True)
    reuse = env.controller_request("c2-0005")
    assert not reuse.get("ok")


@requires_bwrap
@requires_userns
def test_preexec_stop_is_terminal(env):
    """C4' failure (actual controller env points elsewhere) → terminal
    PREEXEC_STOP; the same bound grant cannot return to launchable."""
    grant = env.mint("c2-0006")
    sup = env.start_supervisor(grant)
    # the synthetic controller's env claims match the manifest, but we
    # sabotage via a wrong claimed starttime (binding mismatch path)
    response = env.controller_request(
        "c2-0006",
        overrides={"controller_starttime": "1"},
        own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
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
    ledger and every state file restores nothing: the supervisor is dead
    and nothing listens."""
    response, rc, err = _run_attempt(env, "c2-0007")
    assert response.get("ok"), (response, err)
    op = env.operator_state
    ledger = op / "ledger.jsonl"
    assert ledger.is_file()
    ledger.unlink()
    # forge a fresh-looking ledger (no MINTED record for our attempt)
    ledger.write_text("")
    reuse = env.controller_request("c2-0007")
    assert not reuse.get("ok")
    assert "CONNECT_FAILED" in json.dumps(reuse)


@requires_bwrap
@requires_userns
def test_sigkill_fail_closed_denial_only(env):
    """Supervisor SIGKILL => denial (DoS) only; no authority recovery;
    a genuinely NEW attempt with a fresh mint works independently."""
    grant = env.mint("c2-0008")
    sup = env.start_supervisor(grant)
    os.kill(sup.pid, signal.SIGKILL)
    sup.wait(timeout=10)
    denied = env.controller_request("c2-0008")
    assert not denied.get("ok")
    # same attempt cannot be re-minted (ledger append discipline)
    from qh.authority import AuthorityError
    with pytest.raises(AuthorityError):
        env.mint("c2-0008")
    # a NEW attempt mints and runs fine
    response, rc, err = _run_attempt(env, "c2-0009")
    assert response.get("ok"), (response, err)
    assert rc == 0


@requires_bwrap
@requires_userns
def test_campaign_engagement_accounting_untouched(env):
    """Pre-inference PREEXEC stop and attempt-grant consumption never
    consume campaign auditor/model authority."""
    before = env.engagements.snapshot()
    # terminal preexec stop flow
    response, rc, _ = _run_attempt(env, "c2-0010",
                                   faults=["gatew"])
    assert not response.get("ok")
    assert response["state"] == "TERMINAL_PREEXEC_STOP"
    mid = env.engagements.snapshot()
    assert before == mid
    # happy path (consumed grant + protected local launch)
    response, rc, err = _run_attempt(env, "c2-0011")
    assert response.get("ok"), (response, err)
    after = env.engagements.snapshot()
    assert before == after
    assert response["engagements"] == before


@requires_bwrap
@requires_userns
def test_copied_grant_file_refused(env):
    """A grant carried in an ordinary FILE (a copied grant) is refused
    by the supervisor — authority only travels via pipes."""
    grant = env.mint("c2-0012")
    f = env.base / "copied-grant.json"
    f.write_text(json.dumps(grant.full_doc()) + "\n")
    proc = env.spawn_supervisor(grant, grant_stdin_file=str(f))
    rc, err = env.supervisor_outcome(proc)
    assert rc == 3
    assert "not a pipe" in err


@requires_bwrap
@requires_userns
def test_yama_failure_simulation_terminal(env):
    """Yama ptrace_scope < 1 => fail-closed terminal stop at startup."""
    grant = env.mint("c2-0013")
    proc = env.spawn_supervisor(grant, yama_override=0)
    rc, err = env.supervisor_outcome(proc)
    assert rc == 6
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
    cred_file = env.base / "persisted-credential.txt"
    from qh.compose import SYNTHETIC_CREDENTIAL
    cred_file.write_text(SYNTHETIC_CREDENTIAL)
    grant = env.mint("c2-0014")
    proc = env.spawn_supervisor(grant, custody_value=None,
                                custody_file=str(cred_file))
    # the supervisor will start, refuse at the custody gate during the
    # request; drive the request to observe the terminal stop
    line = proc.stdout.readline().decode()
    if line.startswith("READY"):
        response = env.controller_request("c2-0014",
                                          own_session_slug="s")
        rc, err = env.supervisor_outcome(proc)
        assert not response.get("ok")
        assert "CUSTODY_ESTABLISH_FAILED" in response.get("reason", "")
        assert response["state"] == "TERMINAL_PREEXEC_STOP"
    else:
        rc, err = env.supervisor_outcome(proc)
        assert rc != 0
        assert "custody" in err.lower() or "pipe" in err.lower()


@requires_bwrap
@requires_userns
def test_no_custody_fd_terminal_stop(env):
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
def test_operator_pid_mismatch_refused(env):
    grant = env.mint("c2-0016")
    proc = env.spawn_supervisor(grant, operator_pid=999999)
    rc, err = env.supervisor_outcome(proc)
    assert rc == 5
    assert "SUPERVISOR_STARTUP_FAILED" in err
    assert any(r["event"] == "FAIL_CLOSED"
               and r.get("reason") == "OPERATOR_PID_MISMATCH"
               for r in env.ledger_records())


@requires_bwrap
@requires_userns
def test_supervisor_process_is_non_dumpable(env):
    """The live supervisor must actually run PR_SET_DUMPABLE=0
    (kernel-process-bound authority)."""
    grant = env.mint("c2-0017")
    sup = env.start_supervisor(grant)
    try:
        dumpable = open(f"/proc/{sup.pid}/stat").read()
        # /proc/<pid> access itself is the proof: same-uid non-parent
        # cannot read environ of a non-dumpable process
        try:
            open(f"/proc/{sup.pid}/environ", "rb").read()
            readable = True
        except OSError:
            readable = False
        assert not readable, "supervisor environ must not be same-uid " \
            "readable (dumpable=0)"
    finally:
        sup.kill()
        sup.wait(timeout=10)
