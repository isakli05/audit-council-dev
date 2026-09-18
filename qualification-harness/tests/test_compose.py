"""Integrated C1 -> C2 -> C3 composition: the mandated ORDER, every
fail-closed branch, and reuse refusal — all zero-provider."""
from __future__ import annotations

import json
import os

import pytest

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns

COMPOSITION_EVENTS = [
    "SUPERVISOR_UP", "REQUEST_RECEIVED", "CONTROLLER_BINDING_ESTABLISHED",
    "C4P_RESULT", "AUTHORITY_BOUND", "CUSTODY_ESTABLISHED",
    "NOEGRESS_GATE", "PROFILE_FROZEN", "GATEW_RESULT",
    "CONSUMED_FOR_LAUNCH", "LAUNCHED", "TERMINAL",
]


@requires_bwrap
@requires_userns
def test_full_composition_happy_path_order(env):
    """The recorded composition order, read off the observability ledger
    of ONE integrated attempt."""
    attempt = "compose-0001"
    grant = env.mint(attempt)
    eng_before = env.engagements.snapshot()
    sup = env.start_supervisor(grant)
    response = env.controller_request(attempt,
                                      own_session_slug="own-slug")
    rc, err = env.supervisor_outcome(sup)
    assert response.get("ok"), (response, err)
    assert rc == 0
    assert (env.auditor_output / "launch-sim-marker.txt").is_file()

    events = [r["event"] for r in env.ledger_records()]
    for expected in COMPOSITION_EVENTS:
        assert expected in events, f"missing composition event {expected}"
    idx = {e: events.index(e) for e in COMPOSITION_EVENTS if e in events}
    assert idx["CONTROLLER_BINDING_ESTABLISHED"] < idx["C4P_RESULT"]
    assert idx["C4P_RESULT"] < idx["AUTHORITY_BOUND"]
    assert idx["AUTHORITY_BOUND"] < idx["CUSTODY_ESTABLISHED"]
    assert idx["CUSTODY_ESTABLISHED"] < idx["NOEGRESS_GATE"]
    assert idx["NOEGRESS_GATE"] < idx["PROFILE_FROZEN"]
    assert idx["PROFILE_FROZEN"] < idx["GATEW_RESULT"]
    assert idx["GATEW_RESULT"] < idx["CONSUMED_FOR_LAUNCH"]
    assert idx["CONSUMED_FOR_LAUNCH"] < idx["LAUNCHED"]
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
    assert rc == 9
    assert needle in response.get("reason", "")
    recs = env.ledger_records()
    stops = [r for r in recs if r["event"] == "TERMINAL_PREEXEC_STOP"
             and r.get("attempt_id") == attempt]
    assert stops


@requires_bwrap
@requires_userns
def test_negative_c4p_failure(env):
    """REAL C4' failure: the controller's ACTUAL environ carries a
    different CLAUDE_CONFIG_DIR than the manifest scope."""
    attempt = "compose-neg-c4p"
    grant = env.mint(attempt)
    other_cfg = env.base / "other-config"
    other_cfg.mkdir(exist_ok=True)
    sup = env.start_supervisor(grant)
    # spawn the controller whose real env points at other_cfg while the
    # request claims the manifest scope
    from qh.compose import PY
    import subprocess
    request = env.build_request(attempt)
    request["env_claims"] = {"CLAUDE_CONFIG_DIR": str(env.config_dir)}
    req_path = env.base / "req-neg-c4p.json"
    req_path.write_text(json.dumps(request))
    # fake controller spawned with the WRONG actual CLAUDE_CONFIG_DIR
    argv = [PY, str(HARNESS_ROOT / "fixtures" / "fake_controller.py"),
            "--request", str(req_path), "--attempt", attempt]
    proc = subprocess.run(argv, capture_output=True, text=True,
                          timeout=180,
                          env=dict(os.environ,
                                   CLAUDE_CONFIG_DIR=str(other_cfg)))
    rc, err = env.supervisor_outcome(sup)
    response = json.loads(proc.stdout.strip().splitlines()[-1])
    _assert_terminal(env, attempt, response, rc, "C4P_FAIL")


@requires_bwrap
@requires_userns
def test_negative_noegress_failure(env):
    attempt = "compose-neg-noegress"
    grant = env.mint(attempt)
    sup = env.start_supervisor(grant, faults=["noegress"])
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
    _assert_terminal(env, attempt, response, rc, "NOEGRESS_FAIL")


@requires_bwrap
@requires_userns
def test_negative_gatew_failure(env):
    attempt = "compose-neg-gatew"
    grant = env.mint(attempt)
    sup = env.start_supervisor(grant, faults=["gatew"])
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
    _assert_terminal(env, attempt, response, rc, "GATEW_FAIL")


@requires_bwrap
@requires_userns
def test_negative_identity_drift(env):
    attempt = "compose-neg-identity"
    grant = env.mint(attempt)
    sup = env.start_supervisor(grant, faults=["identity"])
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
    _assert_terminal(env, attempt, response, rc, "IDENTITY_DRIFT")


@requires_bwrap
@requires_userns
def test_negative_policy_drift(env):
    attempt = "compose-neg-policy"
    grant = env.mint(attempt)
    sup = env.start_supervisor(grant, faults=["policy"])
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
    _assert_terminal(env, attempt, response, rc, "DRIFT")


@requires_bwrap
@requires_userns
def test_negative_real_codex_identity_drift(env):
    """REAL drift (no fault flag): the request pins the ORIGINAL binary
    sha, but the executable on disk changed bytes."""
    attempt = "compose-neg-real-identity"
    grant = env.mint(attempt)
    pinned_sha = env.identity["sha256"]
    sup = env.start_supervisor(grant)
    # swap the synthetic codex-like binary BEFORE the request carries
    # the original pinned sha — the identity gate observes real drift
    with open(env.codex_bin, "w") as fh:
        fh.write("#!/bin/sh\n# tampered binary\nexit 3\n")
    os.chmod(env.codex_bin, 0o755)
    response = env.controller_request(
        attempt, own_session_slug="s",
        overrides={"identity_sha256": pinned_sha})
    rc, err = env.supervisor_outcome(sup)
    _assert_terminal(env, attempt, response, rc, "IDENTITY_DRIFT")


@requires_bwrap
@requires_userns
def test_negative_real_policy_config_drift(env):
    """REAL policy drift: the generated config.toml is mutated after
    generation, before the supervisor validates it."""
    attempt = "compose-neg-real-policy"
    grant = env.mint(attempt)
    cfg = env.codex_artifact["config_path"]
    text = open(cfg).read().replace(
        '"/auditor-output" = "write"',
        '"/auditor-output" = "write"\n"/" = "read"')
    with open(cfg, "w") as fh:
        fh.write(text)
    sup = env.start_supervisor(grant)
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
    _assert_terminal(env, attempt, response, rc, "PROFILE_POLICY_DRIFT")


@requires_bwrap
@requires_userns
def test_negative_custody_failure(env):
    attempt = "compose-neg-custody"
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
    attempt = "compose-provider-zero"
    grant = env.mint(attempt)
    sup = env.start_supervisor(grant)
    response = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.supervisor_outcome(sup)
    assert response.get("ok"), (response, err)
    launch = response.get("launch", {})
    assert launch.get("kind") == "launch_sim"
    # the pinned "codex" executable in the composition is the synthetic
    # fixture; the payload argv used by gates are harness-local scripts
    ledger_blob = json.dumps(env.ledger_records())
    assert "codex exec" not in ledger_blob  # no codex process launched
