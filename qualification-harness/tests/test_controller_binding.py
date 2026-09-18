"""CR-REMED-004 — the authorized controller is PRE-BOUND in trusted-root
state (operator-authored into the trusted launch spec: uid + PID +
/proc/<pid>/stat starttime), and BOTH the authority root (mint trigger)
and the supervisor (request acceptance) enforce the SAME pre-bound
identity.  The first compatible same-UID peer must NOT become the
controller merely by connecting first.

Wrong-peer arrivals may terminally consume the one-shot root (acceptable
fail-closed DoS, recorded) — but never gain authority."""
from __future__ import annotations

import json
import os
import signal

import pytest

from conftest import requires_bwrap, requires_userns

from qh.compose import CompositionEnv
from qh.trusted_spec import canonical_spec_bytes, spec_id


@requires_bwrap
@requires_userns
def test_wrong_pid_same_uid_refused_at_root(env):
    """Wrong PID, same UID, compatible knowledge (attempt id + socket
    name): REFUSED before mint."""
    env.author_spec("bind-0001")
    root = env.spawn_root()
    try:
        # a raw socket mint from the TEST process: same UID, wrong PID
        resp = env.raw_root_mint("bind-0001")
        assert not resp.get("ok")
        assert "AUTHORIZED_CONTROLLER_MISMATCH" in json.dumps(resp)
    finally:
        env.cleanup_procs()
    rc, err = env.root_outcome(root, timeout=60)
    assert rc != 0
    recs = env.ledger_records()
    assert not any(r["event"] == "MINTED" and
                   r.get("attempt_id") == "bind-0001" for r in recs)
    assert not any(r["event"] == "ROOT_SPAWNED_SUPERVISOR" for r in recs)


@requires_bwrap
@requires_userns
def test_correct_pid_wrong_starttime_refused(env):
    """Correct PID but wrong starttime: REFUSED (pid-reuse defense against
    a late clone of the controller identity).  Phase-B shape: the operator
    finalization delta binds the controller's pid with a WRONG starttime —
    even the real controller process is refused at the trigger."""
    env.author_spec("bind-0002")
    ctrl = env.controller
    wrong_starttime = str(int(ctrl.starttime) + 1)
    root = env.spawn_authority()
    from qh.trusted_spec import finalize_spec, template_id
    env.finalize(delta={
        "template_id": template_id(env.template),
        "authorized_controller": {"uid": ctrl.uid, "pid": ctrl.pid,
                                  "starttime": wrong_starttime}},
        expect_ready=True)
    # the trigger socket name embeds the FINAL spec id — derive it from
    # the wrong-starttime finalization the authority actually bound
    env._spec = finalize_spec(env.template, controller_uid=ctrl.uid,
                              controller_pid=ctrl.pid,
                              controller_starttime=wrong_starttime)
    try:
        # the bound controller itself mints (correct pid, but the bound
        # starttime does not match the ACTUAL /proc starttime)
        resp = env.root_mint("bind-0002")
        assert not resp.get("ok")
        assert "AUTHORIZED_CONTROLLER_MISMATCH" in json.dumps(resp)
        assert "starttime" in json.dumps(resp)
    finally:
        env.cleanup_procs()
    rc, err = env.root_outcome(root, timeout=60)
    assert rc != 0
    recs = env.ledger_records()
    assert not any(r["event"] == "MINTED" and
                   r.get("attempt_id") == "bind-0002" for r in recs)


@requires_bwrap
@requires_userns
def test_wrong_env_same_uid_compatible_peer_refused(env):
    """A same-UID unrelated process that reproduces the expected
    CLAUDE_CONFIG_DIR tree and knows the attempt id + socket name is STILL
    refused: knowledge is not the capability."""
    env.author_spec("bind-0003")
    root = env.spawn_root()
    try:
        # attacker reproducing the controller's env surface exactly
        attacker = env.spawn_controller(
            claude_config_dir=str(env.config_dir))
        resp = env.raw_root_mint("bind-0003")
        assert not resp.get("ok")
        assert "AUTHORIZED_CONTROLLER_MISMATCH" in json.dumps(resp)
    finally:
        env.cleanup_procs()
    rc, err = env.root_outcome(root, timeout=60)
    assert rc != 0


@requires_bwrap
@requires_userns
def test_exact_authorized_controller_accepted(env):
    """The exact operator-authorized controller instance (uid+pid+
    starttime bound in the spec) IS accepted at the root trigger."""
    result = env.run_attempt("bind-0004")
    assert result["ok"], result
    recs = env.ledger_records()
    verified = [r for r in recs
                if r["event"] == "AUTHORIZED_CONTROLLER_VERIFIED"]
    assert verified, "root must record the pre-bound controller verification"
    assert verified[0].get("pid") == env.controller.pid


@requires_bwrap
@requires_userns
def test_authorized_controller_exited_pid_no_longer_matches(env):
    """The authorized controller exits and its PID identity no longer
    matches (no live process / reuse): the root trigger is refused."""
    env.author_spec("bind-0005")
    ctrl = env.controller
    ctrl.stop()
    root = env.spawn_root()
    try:
        resp = env.raw_root_mint("bind-0005")
        assert not resp.get("ok")
        assert "AUTHORIZED_CONTROLLER_MISMATCH" in json.dumps(resp)
    finally:
        env.cleanup_procs()
    env.root_outcome(root, timeout=60)


@requires_bwrap
@requires_userns
def test_supervisor_enforces_same_prebound_controller(env):
    """The supervisor verifies the SAME pre-bound controller identity at
    request acceptance: a same-UID peer other than the bound controller
    (even with correct attempt id and full claim shape) is refused."""
    env.author_spec("bind-0006")
    root = env.spawn_root()
    mint = env.root_mint("bind-0006")
    assert mint.get("ok"), mint
    # wrong peer at the SUPERVISOR socket (the test process itself)
    request = env.build_request("bind-0006")
    request["env_claims"] = {"CLAUDE_CONFIG_DIR": str(env.config_dir)}
    resp = env.raw_controller_request(mint["supervisor_socket"], request)
    env.root_outcome(root, timeout=300)
    assert not resp.get("ok")
    assert "AUTHORIZED_CONTROLLER_MISMATCH" in json.dumps(resp)
    assert resp.get("state") == "TERMINAL_PREEXEC_STOP"
    # no launch occurred
    assert not (env.auditor_output / "launch-sim-marker.txt").exists()


@requires_bwrap
@requires_userns
def test_wrong_peer_first_consumes_root_fail_closed_dos_recorded(env):
    """A wrong same-UID peer arriving first terminally consumes the
    one-shot root: acceptable fail-closed DoS, recorded — no mint, no
    custody delivery, no provider-capable launch, no auto-recovery."""
    env.author_spec("bind-0007")
    root = env.spawn_root()
    resp = env.raw_root_mint("bind-0007")
    assert not resp.get("ok")
    rc, err = env.root_outcome(root, timeout=60)
    assert rc != 0
    recs = env.ledger_records()
    assert any(r["event"] == "ROOT_FAIL_CLOSED"
               and "AUTHORIZED_CONTROLLER_MISMATCH" in str(r.get("reason"))
               for r in recs), "wrong-peer refusal must be recorded"
    assert not any(r["event"] == "MINTED" and
                   r.get("attempt_id") == "bind-0007" for r in recs)
    assert not any(r["event"] == "ROOT_SPAWNED_SUPERVISOR" for r in recs)
    # the synthetic custody value was never delivered anywhere
    from qh.compose import SYNTHETIC_CREDENTIAL
    for r in recs:
        assert SYNTHETIC_CREDENTIAL not in json.dumps(r)


# ------------------------------------------- spec binding semantics (§13) ----

def test_controller_identity_change_changes_spec_id(env):
    """Changing the authorized controller PID or starttime changes the
    canonical spec identity (the binding is inside the spec digest)."""
    env.author_spec("bind-spec-0001")
    s1 = spec_id(env.spec)
    bad = json.loads(json.dumps(env.spec))
    bad["authorized_controller"]["pid"] += 1
    assert spec_id(bad) != s1
    bad2 = json.loads(json.dumps(env.spec))
    st = int(bad2["authorized_controller"]["starttime"])
    bad2["authorized_controller"]["starttime"] = str(st + 1)
    assert spec_id(bad2) != s1


def test_spec_requires_operator_bound_controller(tmp_path):
    """validate_spec fails closed without the operator-authored
    authorized_controller identity (uid/pid/starttime)."""
    from qh.trusted_spec import validate_spec, SpecError
    env = CompositionEnv(str(tmp_path / "env-spec"))
    env.author_spec("bind-spec-0002")
    spec = json.loads(canonical_spec_bytes(env.spec))
    ac = spec.pop("authorized_controller")
    with pytest.raises(SpecError, match="authorized_controller"):
        validate_spec(spec)
    spec["authorized_controller"] = {"uid": ac["uid"], "pid": ac["pid"]}
    with pytest.raises(SpecError):
        validate_spec(spec)


def test_controller_request_cannot_supply_authorized_identity(env):
    """The claim-only request schema does not gain controller-supplied
    authority fields: authorized-controller identity supplied as a claim
    is an UNKNOWN_CLAIM_FIELD terminal refusal (§14 preserved)."""
    env.author_spec("bind-spec-0003")
    result = env.run_attempt(
        "bind-spec-0003",
        overrides={"authorized_controller": {"pid": 1, "uid": 0,
                                             "starttime": "1"}})
    assert not result["ok"]
    assert "UNKNOWN_CLAIM_FIELD" in result["response"].get("reason", "")
    assert "authorized_controller" in result["response"].get("reason", "")
