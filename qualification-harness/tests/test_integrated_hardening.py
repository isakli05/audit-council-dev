"""§18 — ONE integrated synthetic attempt proving the complete hardened
authority-bootstrap composition (zero provider/model/auditor execution):

 1. operator-authorized controller identity established;
 2. trusted launch spec delivered via a permitted capability channel;
 3. authority root starts;
 4. correct UAPI seals established;
 5. authority-critical state sealed;
 6. privileged bootstrap bytes frozen BEFORE the controller trigger;
 7. root exposes the controller trigger;
 8. wrong peer cannot mint;
 9. correct controller trigger accepted;
10. supervisor uses only the trusted frozen bootstrap;
11. C4' passes; 12. custody established; 13. no-egress passes;
14. profile freezes; 15. GATE-W passes;
16. local synthetic protected launch succeeds;
17. reuse fails; 18. engagement accounting untouched."""
from __future__ import annotations

import json
import os

import pytest

from conftest import requires_bwrap, requires_userns

from qh.compose import SYNTHETIC_CREDENTIAL


@requires_bwrap
@requires_userns
def test_integrated_hardened_composition(env):
    attempt = "hard-int-0001"

    # [1] operator-authorized controller identity (live process, dedicated
    # CLAUDE_CONFIG_DIR captured pre-controller by the C-1 manifest)
    ctrl = env.controller
    assert ctrl.pid > 0 and ctrl.starttime
    assert env.manifest.ok

    # [2] spec constructed + delivered through the operator PIPE channel
    spec = env.author_spec(attempt)
    from qh.trusted_spec import spec_id
    assert spec["authorized_controller"]["pid"] == ctrl.pid
    assert spec["authorized_controller"]["starttime"] == ctrl.starttime

    # [8] FIRST: a wrong peer cannot mint (fail-closed DoS on this root)
    root0 = env.spawn_root()
    wrong = env.raw_root_mint(attempt)
    assert not wrong.get("ok")
    assert "AUTHORIZED_CONTROLLER_MISMATCH" in json.dumps(wrong)
    rc0, _ = env.root_outcome(root0, timeout=60)
    assert rc0 != 0

    # [3]-[7] fresh root: startup, seals, freeze, THEN trigger exposure
    eng_before = env.engagements.snapshot()
    root = env.spawn_root()
    recs = env.ledger_records()
    events = [r["event"] for r in recs]
    # [4]/[5] correct UAPI seals + sealed authority-critical state
    sealed = [r for r in recs
              if r["event"] == "ROOT_CUSTODY_ESTABLISHED"][-1]
    assert sealed["seal_status"] == "sealed"
    spec_seal = [r for r in recs if r["event"] == "SPEC_BYTES_SEALED"]
    assert spec_seal and spec_seal[-1]["seal_status"] == "sealed"
    # [6] frozen bootstrap BEFORE [7] trigger exposure
    frozen = [r for r in recs if r["event"] == "BOOTSTRAP_FROZEN"][-1]
    assert frozen["spec_tree_digest_match"] is True
    assert frozen["bundle_seal_status"] == "sealed"
    assert events.index("BOOTSTRAP_FROZEN") < \
        events.index("ROOT_SOCKET_BOUND")

    # [9] the correct controller trigger is accepted at the root
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    assert mint["supervisor_pid"] > 0
    # [10] supervisor created from the frozen bootstrap representation
    spawn = [r for r in env.ledger_records()
             if r["event"] == "ROOT_SPAWNED_SUPERVISOR"][-1]
    assert spawn["channel"] == "fork-frozen-bootstrap"

    # [11]-[16] the controller request runs the full preexec pipeline
    resp = env.controller_request(attempt, own_session_slug="own")
    rc, err = env.root_outcome(root, timeout=300)
    assert resp.get("ok"), (resp, err)
    assert rc == 0, err

    recs = env.ledger_records()
    events = [r["event"] for r in recs]
    for expected in ("C4P_RESULT", "TRUSTED_SPEC_VERIFY", "CUSTODY_"
                     "ESTABLISHED", "TRUSTED_BYTES_SNAPSHOTTED",
                     "NOEGRESS_GATE", "PROFILE_FROZEN", "GATEW_RESULT",
                     "CONSUMED_FOR_LAUNCH", "LAUNCHED"):
        assert expected in events, f"missing {expected}"
    c4 = [r for r in recs if r["event"] == "C4P_RESULT"][-1]
    assert c4["passed"] is True and c4["failures"] == []
    gatew = [r for r in recs if r["event"] == "GATEW_RESULT"][-1]
    assert gatew["passed"] is True
    # [16] the local synthetic protected launch produced its marker
    assert (env.auditor_output / "launch-sim-marker.txt").is_file()

    # [17] reuse fails closed
    reuse = env.controller_request(attempt)
    assert not reuse.get("ok")

    # [18] engagement accounting untouched
    assert eng_before == env.engagements.snapshot()
    ledger_blob = json.dumps(recs)
    assert "codex exec" not in ledger_blob  # ZERO provider process


@requires_bwrap
@requires_userns
def test_integrated_spec_arrives_via_sealed_memfd_channel(env):
    """The permitted capability channels include the fully sealed memfd:
    an integrated attempt whose spec arrives by SEALED MEMFD completes."""
    attempt = "hard-int-memfd"
    env.author_spec(attempt)
    from qh.trusted_spec import canonical_spec_bytes
    from qh.util import hold_bytes_memfd
    fd, status = hold_bytes_memfd(canonical_spec_bytes(env.spec),
                                  name="int-spec-channel")
    assert status == "sealed"
    root = env.spawn_root(spec_fd=fd)
    os.close(fd)
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    resp = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert resp.get("ok"), (resp, err)
    assert rc == 0, err
