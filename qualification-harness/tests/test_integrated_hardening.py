"""§20 — ONE integrated zero-provider synthetic attempt proving the
complete TWO-PHASE pre-controller authority-bootstrap composition
(CR-HARDEN-001 + held CR-REMED-001/002/003/004 closures):

 1. trusted pre-controller source identity selected (operator template
    with the operator-computed expected harness digest);
 2. privileged authority code bundle frozen against that identity;
 3. mandatory seals verified (template bytes, custody, frozen bundle);
 4. PRE_CONTROLLER_BOOTSTRAP_FROZEN (all privileged modules loaded with
    code-object provenance);
 5. controller starts ONLY afterward (post-PRECONTROLLER_READY);
 6. operator obtains controller uid/pid/starttime;
 7. final spec finalized over the trusted capability channel (operator-
    held finalization pipe; the controller holds no write end);
 8. frozen harness identity equality verified (FINAL_SPEC_FROZEN_HARNESS_ID
    == PRE_CONTROLLER_FROZEN_HARNESS_ID);
 9. controller trigger exposed;
10. root authorized-controller verification passes (SO_PEERCRED +
    actual /proc starttime);
11. supervisor forked from frozen authority state;
12. supervisor repeats authorized-controller verification;
13. C4' passes; 14. custody established; 15. hard no-egress passes;
16. profile freezes; 17. GATE-W passes;
18. synthetic protected launch succeeds;
19. reuse refused; 20. engagement accounting untouched.

Provider/model/auditor execution: ZERO."""
from __future__ import annotations

import json
import os

import pytest

from conftest import requires_bwrap, requires_userns

from qh.compose import SYNTHETIC_CREDENTIAL


@requires_bwrap
@requires_userns
def test_integrated_pre_controller_provenance_composition(env):
    attempt = "hard-int-0001"

    # [1] operator selects the trusted pre-controller source identity
    #     (template authored in the trusted phase; the expected digest is
    #     computed from the harness source by the operator)
    tpl = env.author_template(attempt)
    from qh.trusted_spec import template_id
    expected_digest = tpl["harness"]["tree_digest"]
    assert tpl["harness"].get("provenance") is not None

    # [8]-pre: a wrong peer cannot mint (fail-closed DoS on a first root)
    root0 = env.spawn_authority()
    env.finalize()
    wrong = env.raw_root_mint(attempt)
    assert not wrong.get("ok")
    assert "AUTHORIZED_CONTROLLER_MISMATCH" in json.dumps(wrong)
    rc0, _ = env.root_outcome(root0, timeout=60)
    assert rc0 != 0

    # [2]-[7] fresh authority: Phase A (freeze) BEFORE the controller
    eng_before = env.engagements.snapshot()
    root = env.spawn_authority()
    recs = env.ledger_records()
    events = [r["event"] for r in recs]
    # [3] mandatory seals (template + custody) with the corrected UAPI
    sealed = [r for r in recs
              if r["event"] == "ROOT_CUSTODY_ESTABLISHED"][-1]
    assert sealed["seal_status"] == "sealed"
    tpl_seal = [r for r in recs
                if r["event"] == "TEMPLATE_BYTES_SEALED"]
    assert tpl_seal and tpl_seal[-1]["seal_status"] == "sealed"
    # [4] frozen bootstrap with module provenance BEFORE the controller
    frozen = [r for r in recs
              if r["event"] == "PRE_CONTROLLER_BOOTSTRAP_FROZEN"][-1]
    assert frozen["expected_tree_digest_match"] is True
    assert frozen["bundle_seal_status"] == "sealed"
    assert frozen["files"] == 21 and frozen["modules"] == 19
    prov = env.bootstrap_provenance()
    assert all(e["load_phase"] == "PRE_CONTROLLER_TRUSTED_PHASE"
               and e["codeobject_verified"] is True
               for e in prov["module_inventory"].values())
    # the controller does not exist yet: it is started only now
    ctrl = env.spawn_controller(claude_config_dir=str(env.config_dir))
    # [6] operator obtains the actual controller identity and [7]
    # finalizes over the trusted capability channel
    fin_stat = os.fstat(env.finalization_w)
    hits = []
    for fd in os.listdir(f"/proc/{ctrl.pid}/fd"):
        try:
            st = os.stat(f"/proc/{ctrl.pid}/fd/{fd}")
        except OSError:
            continue
        if (st.st_ino, st.st_dev) == (fin_stat.st_ino, fin_stat.st_dev):
            hits.append(fd)
    assert hits == []
    env.finalize(controller=ctrl)
    # [8] frozen harness identity equality proven at finalization
    fin = [r for r in env.ledger_records()
           if r["event"] == "SPEC_FINALIZED"][-1]
    assert fin["frozen_harness_id_match"] is True
    assert fin["frozen_harness_id"] == expected_digest
    # [9] trigger exposed only now
    events = [r["event"] for r in env.ledger_records()]
    assert events.index("PRE_CONTROLLER_BOOTSTRAP_FROZEN") < \
        events.index("SPEC_FINALIZED") < \
        events.index("ROOT_SOCKET_BOUND")

    # [10] the correct controller trigger is accepted at the root
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    assert mint["supervisor_pid"] > 0
    # [11] supervisor created from the frozen bootstrap representation
    spawn = [r for r in env.ledger_records()
             if r["event"] == "ROOT_SPAWNED_SUPERVISOR"][-1]
    assert spawn["channel"] == "fork-frozen-bootstrap"

    # [12]-[18] the controller request runs the full preexec pipeline
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
    # [18] the local synthetic protected launch produced its marker
    assert (env.auditor_output / "launch-sim-marker.txt").is_file()

    # [19] reuse fails closed
    reuse = env.controller_request(attempt)
    assert not reuse.get("ok")

    # [20] engagement accounting untouched
    assert eng_before == env.engagements.snapshot()
    ledger_blob = json.dumps(recs)
    assert "codex exec" not in ledger_blob  # ZERO provider process


@requires_bwrap
@requires_userns
def test_integrated_template_arrives_via_sealed_memfd_channel(env):
    """The permitted capability channels include the fully sealed memfd:
    an integrated attempt whose pre-controller TEMPLATE arrives by SEALED
    MEMFD completes the full two-phase flow."""
    attempt = "hard-int-memfd"
    env.author_template(attempt)
    from qh.trusted_spec import canonical_template_bytes
    from qh.util import hold_bytes_memfd
    fd, status = hold_bytes_memfd(canonical_template_bytes(env.template),
                                  name="int-template-channel")
    assert status == "sealed"
    root = env.spawn_root(template_fd=fd)
    os.close(fd)
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    resp = env.controller_request(attempt, own_session_slug="s")
    rc, err = env.root_outcome(root, timeout=300)
    assert resp.get("ok"), (resp, err)
    assert rc == 0, err
