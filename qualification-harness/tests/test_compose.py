"""Integrated C1 -> C2 -> C3 composition over the AUTHORITY-ROOT flow
(§22): the mandated ORDER, every fail-closed branch, reuse refusal and
controller-imitation powerlessness — all zero-provider.  Test fault
injection uses ONLY in-process reader/launcher seams (never a production
CLI flag; the production surface has none)."""
from __future__ import annotations

import json
import os
import subprocess

import pytest

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns

from qh.boundary import BoundaryResult

COMPOSITION_EVENTS = [
    "SUPERVISOR_UP", "REQUEST_RECEIVED", "CONTROLLER_BINDING_ESTABLISHED",
    "C4P_RESULT", "TRUSTED_SPEC_VERIFY", "AUTHORITY_BOUND",
    "CREDENTIAL_ADAPTER_BOUND", "CUSTODY_ESTABLISHED",
    "TRUSTED_BYTES_SNAPSHOTTED", "NOEGRESS_GATE", "PROFILE_FROZEN",
    "GATEW_RESULT", "CONSUMED_FOR_LAUNCH", "LAUNCHED", "TERMINAL",
]


@requires_bwrap
@requires_userns
def test_full_composition_happy_path_order(env):
    """§22: the recorded composition order over the authority-root flow,
    read off the observability ledger of ONE integrated attempt."""
    attempt = "compose-0001"
    env.author_spec(attempt)
    eng_before = env.engagements.snapshot()
    root = env.spawn_root()
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    response = env.controller_request(attempt,
                                      own_session_slug="own-slug")
    rc, err = env.root_outcome(root, timeout=300)
    assert response.get("ok"), (response, err)
    assert rc == 0, err
    assert (env.auditor_output / "launch-sim-marker.txt").is_file()

    events = [r["event"] for r in env.ledger_records()]
    for expected in COMPOSITION_EVENTS:
        assert expected in events, f"missing composition event {expected}"
    idx = {e: events.index(e) for e in COMPOSITION_EVENTS if e in events}
    assert idx["CONTROLLER_BINDING_ESTABLISHED"] < idx["C4P_RESULT"]
    assert idx["C4P_RESULT"] < idx["TRUSTED_SPEC_VERIFY"]
    assert idx["TRUSTED_SPEC_VERIFY"] < idx["AUTHORITY_BOUND"]
    assert idx["AUTHORITY_BOUND"] < idx["CUSTODY_ESTABLISHED"]
    assert idx["CUSTODY_ESTABLISHED"] < idx["TRUSTED_BYTES_SNAPSHOTTED"]
    assert idx["TRUSTED_BYTES_SNAPSHOTTED"] < idx["NOEGRESS_GATE"]
    assert idx["NOEGRESS_GATE"] < idx["PROFILE_FROZEN"]
    assert idx["PROFILE_FROZEN"] < idx["GATEW_RESULT"]
    assert idx["GATEW_RESULT"] < idx["CONSUMED_FOR_LAUNCH"]
    assert idx["CONSUMED_FOR_LAUNCH"] < idx["LAUNCHED"]
    # the root records the operator-only initialization BEFORE any
    # controller request
    assert events.index("ROOT_UP") < events.index("REQUEST_RECEIVED")
    assert events.index("SPEC_BOUND") < events.index("REQUEST_RECEIVED")
    assert events.index("ROOT_CUSTODY_ESTABLISHED") < \
        events.index("REQUEST_RECEIVED")
    # C4' actually passed inside the integrated flow
    c4 = [r for r in env.ledger_records()
          if r["event"] == "C4P_RESULT"][0]
    assert c4["passed"] is True and c4["failures"] == []
    # engagement accounting untouched by the whole lifecycle
    assert eng_before == env.engagements.snapshot()
    # reuse fails closed
    reuse = env.controller_request(attempt)
    assert not reuse.get("ok")


def _assert_terminal(env, attempt, response, rc, needle):
    assert not response.get("ok"), response
    assert response["state"] == "TERMINAL_PREEXEC_STOP"
    assert rc == 9, rc
    assert needle in response.get("reason", "")
    recs = env.ledger_records()
    stops = [r for r in recs if r["event"] == "TERMINAL_PREEXEC_STOP"
             and r.get("attempt_id") == attempt]
    assert stops


@requires_bwrap
@requires_userns
def test_negative_c4p_failure(env):
    """REAL C4' failure: the bound controller's ACTUAL environ carries a
    different CLAUDE_CONFIG_DIR than the manifest scope (the operator
    authorized a controller instance whose real scope env mismatches the
    captured manifest)."""
    attempt = "compose-neg-c4p"
    other_cfg = env.base / "other-config"
    other_cfg.mkdir(exist_ok=True)
    # operator binds a controller whose ACTUAL CLAUDE_CONFIG_DIR differs
    # from the manifest scope dir
    bad_ctrl = env.spawn_controller(claude_config_dir=str(other_cfg))
    env.author_spec(attempt, controller=bad_ctrl)
    root = env.spawn_root()
    mint = env.root_mint(attempt)
    assert mint.get("ok")
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    _assert_terminal(env, attempt, response, rc, "C4P_FAIL")


def _failing_launcher(kind: str):
    """Deterministic TEST launcher seam (dependency injection at the
    policy seam — mechanically unreachable from the production CLI):
    simulates REAL observed gate failures by returning failing REAL-SHAPE
    records (it can only ever make gates fail, never pass)."""
    from qh.boundary import launch as real_launch

    def launcher(spec, *, timeout=60.0):
        if kind == "noegress":
            return BoundaryResult(
                returncode=78, records=[{
                    "phase": "noegress", "passed": False,
                    "failures": ["TEST_SEAM_OBSERVED_FAILURE"]}])
        if kind == "gatew":
            return BoundaryResult(returncode=3, records=[{
                "phase": "noegress", "passed": True, "failures": [],
            }, {
                "phase": "payload_result", "kind": "gatew",
                "all_expected": False,
                "ops": [{"name": "auditor-output create",
                         "path": "/auditor-output/x", "action": "create",
                         "expect": "allowed", "actual": "refused:13"}],
            }])
        return real_launch(spec, timeout=timeout)
    return launcher


def _run_inprocess_attempt(env, attempt, policy):
    """Drive an IN-PROCESS supervisor (test seam: readers/launcher only)
    with the claim-only request protocol."""
    from qh.authority import Supervisor
    from qh.trusted_spec import spec_id
    env.author_spec(attempt)
    grant = env.mint(attempt)
    # in-process TEST-fabricated grant (operator in-memory channel): the
    # ppid binding does not apply to the test process itself
    grant.root_pid = None
    grant.spec_id = spec_id(env.spec)
    cr, cw = os.pipe()
    os.write(cw, b"SYNTHETIC-INERT-SEAM")
    os.close(cw)
    sup = Supervisor(grant=grant, spec=env.spec, spec_id=spec_id(env.spec),
                     operator_state_dir=str(env.operator_state),
                     custody_fd=cr, policy=policy)
    sup.startup()
    assert sup.exit_code == 0
    sup.bind_socket()
    import threading
    thread = threading.Thread(target=sup.serve_once)
    thread.start()
    response = env.controller_request(attempt, own_session_slug="s")
    thread.join(timeout=300)
    os.close(cr)
    return response, sup.exit_code


@requires_bwrap
@requires_userns
def test_negative_noegress_failure(env):
    """No-egress gate failure (observed-failure shape injected at the
    TEST launcher seam — no production flag exists)."""
    from qh.authority import SupervisorPolicy
    policy = SupervisorPolicy(set_dumpable=False,
                              boundary_launcher=_failing_launcher("noegress"))
    response, rc = _run_inprocess_attempt(env, "compose-neg-noegress",
                                          policy)
    _assert_terminal(env, "compose-neg-noegress", response, rc,
                     "NOEGRESS_FAIL")


@requires_bwrap
@requires_userns
def test_negative_gatew_failure(env):
    """GATE-W failure (observed-failure shape injected at the TEST
    launcher seam)."""
    from qh.authority import SupervisorPolicy
    policy = SupervisorPolicy(set_dumpable=False,
                              boundary_launcher=_failing_launcher("gatew"))
    response, rc = _run_inprocess_attempt(env, "compose-neg-gatew", policy)
    _assert_terminal(env, "compose-neg-gatew", response, rc, "GATEW_FAIL")


@requires_bwrap
@requires_userns
def test_negative_real_codex_identity_drift(env):
    """REAL drift: the executable on disk changed bytes after the trusted
    spec was authorized — the spec-bound identity gate observes it."""
    attempt = "compose-neg-real-identity"
    env.author_spec(attempt)
    root = env.spawn_root()
    mint = env.root_mint(attempt)
    assert mint.get("ok")
    with open(env.codex_bin, "w") as fh:
        fh.write("#!/bin/sh\n# tampered binary\nexit 3\n")
    os.chmod(env.codex_bin, 0o755)
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    _assert_terminal(env, attempt, response, rc, "CODEX_EXE")


@requires_bwrap
@requires_userns
def test_negative_real_policy_config_drift(env):
    """REAL policy drift: the spec-bound config digest does not match the
    profile parameters (config tampered between authorization and
    freeze)."""
    attempt = "compose-neg-real-policy"
    spec = env.author_spec(attempt)
    bad = json.loads(json.dumps(spec))
    bad["codex"]["config_sha256"] = "0" * 64
    env._spec = bad
    root = env.spawn_root(bad)
    mint = env.root_mint(attempt, spec=bad)
    assert mint.get("ok")
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    _assert_terminal(env, attempt, response, rc,
                     "PROFILE_CONFIG_DIGEST_MISMATCH")


@requires_bwrap
@requires_userns
def test_negative_custody_failure(env):
    attempt = "compose-neg-custody"
    env.author_spec(attempt)
    grant = env.mint(attempt)
    cred_file = env.base / "persisted.txt"
    from qh.compose import SYNTHETIC_CREDENTIAL
    cred_file.write_text(SYNTHETIC_CREDENTIAL)
    proc = env.spawn_supervisor(grant, custody_value=None,
                                custody_file=str(cred_file))
    line = proc.stdout.readline().decode()
    assert line.startswith("READY")
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.supervisor_outcome(proc)
    _assert_terminal(env, attempt, response, rc,
                     "CUSTODY_ESTABLISH_FAILED")


@requires_bwrap
@requires_userns
def test_no_provider_launch_by_construction(env):
    """The protected launch and GATE-W run LOCAL deterministic scripts:
    the composition never references a real provider binary."""
    result = env.run_attempt("compose-provider-zero")
    assert result["ok"], result
    response = result["response"]
    launch = response.get("launch", {})
    assert launch.get("kind") == "launch_sim"
    ledger_blob = json.dumps(env.ledger_records())
    assert "codex exec" not in ledger_blob  # no codex process launched
