"""BA-26..BA-50 + the BA-RB-001/BA-RB-002 remediation regressions:
dynamic-gate execution, one-shot attempt-global accounting across
binding variants, gates-BEFORE-credential-materialization ordering,
credential/exec boundary, and the report lifecycle incl. the authority
plane's own independent semantic report binding.  All synthetic,
zero-provider, zero-network; the REAL executing authority package is
verified in place by every construction (self-identity)."""
from __future__ import annotations

import inspect
import json
import os
import stat
from pathlib import Path

import pytest

from bootstrap_authority import runtime as bar
from bootstrap_authority.accounting import (AccountingError, AccountingStore,
                                            inspect_accounting_record)
from bootstrap_authority.custody import get_dumpable
from bootstrap_authority.statemachine import (CONSUMED_PRE_EXEC,
                                              EXEC_ATTEMPTED, GATES_PASSED,
                                              PREPARED, REPORT_FROZEN,
                                              REPORT_INVALID,
                                              REPORT_MISSING,
                                              REPORT_SCREEN_FAIL,
                                              TERMINAL,
                                              TERMINAL_PREEXEC_STOP)
from conftest import build_world, make_report, make_report_for_role

WRONG_TARGET = "0123456789abcdef0123456789abcdef01234567"


# --- full success path (also BA-30/36/37/39/42/43 evidence) -------------


def test_full_success_pipe(world_a):
    result = world_a.run()
    assert result.report_state == REPORT_FROZEN
    assert not result.timed_out and not result.exec_failed
    frozen = world_a.output_root / world_a.binding.output_identity["name"]
    expected = make_report_for_role("AUDITOR_A")
    assert frozen.read_bytes() == expected                  # BA-43
    assert stat.S_IMODE(frozen.stat().st_mode) == 0o444
    assert result.report_sha256 == __import__("hashlib").sha256(
        expected).hexdigest()
    record = world_a.inspect_record()
    # BA-30: GATES_PASSED -> CONSUMED_PRE_EXEC durably BEFORE EXEC
    assert record["states"] == [PREPARED, GATES_PASSED,
                                CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
                                REPORT_FROZEN, TERMINAL]
    gates_record = record["records"][1]
    for gate in ("client_selection", "network_readiness",
                 "resource_gate"):
        assert f"{gate}_result" in gates_record
    facts = record["records"][2]
    assert facts["target_commit"] == world_a.binding.target["commit"]
    assert facts["model"] == "claude-opus-5-5"
    # BA-37: non-dumpable established before the credential read
    assert get_dumpable() == 0
    # BA-39: no caller argv/model/environment override reached the child
    meta = result.metadata
    # the kernel rewrites argv[0] for shebang launchers (script path);
    # the no-override property is argv[1:] + the exact environment
    assert meta["argv"][1:] == ["--role", "AUDITOR_A",
                                "--attempt",
                                world_a.binding.attempt_id,
                                "--event", world_a.binding.event_id]
    # the authority passed EXACTLY PATH+LANG; LC_CTYPE is injected by
    # the CPython interpreter itself under the C locale, and NOTHING
    # from the caller (PYTHONPATH, model vars, overrides) may appear
    assert set(meta["env"]) <= {"PATH", "LANG", "LC_CTYPE"}
    assert meta["env"]["PATH"] == "/usr/bin:/bin"
    assert meta["env"]["LANG"] == "C"
    assert "PYTHONPATH" not in meta["env"]
    assert meta["invocation"] == world_a.binding.auditor_invocation
    assert meta["auditor_fd_sha256"] == world_a.binding.auditor_selection[
        "client_executable"]["sha256"]
    assert meta["cred_fd_link"].startswith("/memfd:")
    # BA-36 (pipe): no credential persistence anywhere in the output tree
    for path in world_a.output_root.rglob("*"):
        if path.is_file():
            assert world_a.credential not in path.read_bytes(), path



def test_full_success_role_b_memfd(world_b):
    result = world_b.run(source="memfd")
    assert result.report_state == REPORT_FROZEN
    assert get_dumpable() == 0


# --- BA-26: exact dynamic gate order, each exactly once -----------------


def test_ba26_gate_order_and_once(world_a):
    world_a.run()
    lines = world_a.order_file.read_text().splitlines()
    assert lines == ["CLIENT_SELECTION_PREFLIGHT", "NETWORK_READINESS",
                     "RESOURCE_GATE"]


def test_ba26_tampered_gate_artifact_refused_at_open(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A")
    gate_path = world.event_root / "gates" / "resource_gate.py"
    gate_path.write_bytes(gate_path.read_bytes() + b"# drift\n")
    with pytest.raises(bar.AuthorityRefused, match="resource_gate"):
        world.authority()          # construction fails closed: the walk
        # refusal fires first (the tampered artifact no longer matches
        # its manifest row) before the gate descriptor is even opened


# --- BA-27: preflight mismatch fails BEFORE consumption ------------------


def test_ba27_preflight_model_mismatch(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A",
                        preflight_tweak={"model": "claude-haiku-4-5"})
    with pytest.raises(bar.AuthorityRefused,
                       match="CLIENT_SELECTION_PREFLIGHT_BOUND_MISMATCH"):
        world.run()
    record = world.inspect_record()
    assert record["last_state"] == TERMINAL_PREEXEC_STOP
    assert CONSUMED_PRE_EXEC not in record["states"]


# --- BA-28: gates receive no credential fd ------------------------------


def test_ba28_no_credential_fd_to_gates(world_a):
    world_a.run()
    record = world_a.inspect_record()
    gates_record = record["records"][1]
    network = json.loads(gates_record["network_readiness_result"])
    for link in network["checks"]["route"]["detail"]["fd_inventory"]:
        assert "/memfd:" not in link, link


# --- BA-RB-002: gates BEFORE credential materialization -----------------


def test_ba_rb002_failing_preflight_leaves_credential_unread(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A",
                        preflight_tweak={"model": "claude-haiku-4-5"})
    r, w = os.pipe()
    os.write(w, world.credential)
    os.close(w)
    try:
        with pytest.raises(bar.AuthorityRefused,
                           match="CLIENT_SELECTION_PREFLIGHT_BOUND_MISMATCH"):
            world.authority().run_attempt(
                r, world.launcher_path, world.auditor_path,
                world.staging, world.output_root)
        # NO credential materialization occurred: every synthetic byte
        # remains readable from the source pipe
        assert os.read(r, 65536) == world.credential
    finally:
        os.close(r)
    record = world.inspect_record()
    assert record["last_state"] == TERMINAL_PREEXEC_STOP
    assert CONSUMED_PRE_EXEC not in record["states"]
    assert EXEC_ATTEMPTED not in record["states"]
    assert world.order_file.read_text().splitlines() == [
        "CLIENT_SELECTION_PREFLIGHT"]      # stopped at the FIRST gate
    assert not world.staging.exists()      # no launcher/auditor execution
    assert not list(world.output_root.glob("*.json"))
    assert world.credential not in json.dumps(record).encode()


def test_ba_rb002_custody_only_after_all_gates_and_durable_gates_passed(
        world_a, monkeypatch):
    observed = []
    real_ingest = bar.CredentialCustody.ingest

    @staticmethod
    def observing_ingest(source_fd, role):
        observed.append((
            world_a.order_file.read_text().splitlines(),
            inspect_accounting_record(
                world_a.output_root,
                bar.accounting_name(world_a.binding),
                world_a.binding.digest)["states"]))
        return real_ingest(source_fd, role)

    monkeypatch.setattr(bar.CredentialCustody, "ingest",
                        observing_ingest)
    result = world_a.run()
    assert result.report_state == REPORT_FROZEN
    assert len(observed) == 1               # custody ingest exactly once
    gate_order, durable_states = observed[0]
    assert gate_order == ["CLIENT_SELECTION_PREFLIGHT", "NETWORK_READINESS",
                          "RESOURCE_GATE"]
    assert durable_states == [PREPARED, GATES_PASSED]
    record = world_a.inspect_record()
    assert record["states"] == [PREPARED, GATES_PASSED,
                                CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
                                REPORT_FROZEN, TERMINAL]
    assert world_a.credential not in json.dumps(record).encode()


# --- BA-29 (BA-RB-001): attempt-global O_EXCL authority claim ----------


def test_ba29_same_binding_second_authority_process_refused(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A",
                        launcher_mode="none")
    assert world.run().report_state == REPORT_MISSING
    with pytest.raises(bar.AuthorityRefused,
                       match="RECORD_CREATE_REFUSED"):
        world.run()                      # a SECOND process would refuse
    assert sorted(p.name for p in world.output_root.glob("*.jsonl")) == \
        [bar.accounting_name(world.binding) + ".jsonl"]


def test_ba29_rb001_cross_binding_same_attempt_refused(tmp_path):
    # BA-RB-001: ONE reserved attempt id -> ONE GLOBAL authority claim.
    # Two INDEPENDENTLY valid AUDITOR_A bindings (different digests,
    # each with its own self-consistent synthetic event package) with
    # the SAME reserved attempt id and the SAME operator custody (the
    # shared root is FROZEN into BOTH bindings' output_identity): the
    # second claim must fail closed at the attempt-global O_EXCL name,
    # BEFORE any dynamic gate and BEFORE any credential read.
    first = build_world(tmp_path / "first", "AUDITOR_A",
                        launcher_mode="none")
    second = build_world(tmp_path / "second", "AUDITOR_A",
                         launcher_mode="none",
                         output_root=first.output_root)
    assert second.binding.attempt_id == first.binding.attempt_id
    assert second.binding.digest != first.binding.digest
    assert second.output_root == first.output_root  # the SAME custody dir
    assert first.run().report_state == REPORT_MISSING
    authority_b = second.authority()           # valid on its OWN terms
    r, w = os.pipe()
    os.write(w, second.credential)
    os.close(w)
    try:
        with pytest.raises(bar.AuthorityRefused,
                           match="RECORD_CREATE_REFUSED"):
            authority_b.run_attempt(
                r, second.launcher_path, second.auditor_path,
                second.staging, second.output_root)
        # the refusal PRECEDES any credential read: every synthetic
        # byte is still readable from the source pipe
        assert os.read(r, 65536) == second.credential
    finally:
        os.close(r)
    # the second binding executed ZERO dynamic gates
    assert not second.order_file.exists()
    assert first.order_file.read_text().splitlines() == [
        "CLIENT_SELECTION_PREFLIGHT", "NETWORK_READINESS",
        "RESOURCE_GATE"]
    # the ORIGINAL durable record retains the FIRST binding's digest
    # on EVERY record (the digest stays durable in-record evidence)
    record = first.inspect_record()
    assert record["states"] == [PREPARED, GATES_PASSED,
                                CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
                                REPORT_MISSING, TERMINAL]
    assert all(rec["binding_digest"] == first.binding.digest
               for rec in record["records"])
    # inspection stays digest-bound: the second binding's digest
    # refuses against the first binding's record
    with pytest.raises(AccountingError, match="RECORD_BINDING_MISMATCH"):
        inspect_accounting_record(
            second.output_root, bar.accounting_name(second.binding),
            second.binding.digest)
    # NO second same-attempt accounting record exists (under the old
    # composite name a second <attempt>.<digest>.jsonl WOULD exist)
    assert sorted(p.name for p in second.output_root.glob("*.jsonl")) == \
        [bar.accounting_name(first.binding) + ".jsonl"]


def test_ba29_rb001_distinct_reserved_attempts_stay_distinct(tmp_path):
    # the distinct AUDITOR_A / AUDITOR_B reserved attempt ids remain
    # independent accounting namespaces under one operator custody
    # (the shared root frozen into BOTH bindings' output_identity).
    a = build_world(tmp_path / "a", "AUDITOR_A", launcher_mode="none")
    b = build_world(tmp_path / "b", "AUDITOR_B", launcher_mode="none",
                    output_root=a.output_root)
    assert a.run().report_state == REPORT_MISSING
    assert b.run().report_state == REPORT_MISSING
    assert sorted(p.name for p in a.output_root.glob("*.jsonl")) == sorted(
        [bar.accounting_name(a.binding) + ".jsonl",
         bar.accounting_name(b.binding) + ".jsonl"])


# --- BA-PREP-001 / BA-PREP-002 remediation: the attempt output custody
# root and report source are BINDING-FROZEN authority dimensions; caller
# path substitution fails closed BEFORE any custody open, attempt-global
# O_EXCL claim, dynamic gate or credential read, and every authority
# action then uses the FROZEN binding values exclusively -------------


def test_ba_prep001_alternate_output_root_refused_fail_closed(tmp_path):
    # BA-PREP-001: ONE reserved attempt -> ONE mechanically authorized
    # process-bound one-shot authority.  A caller selecting a DIFFERENT
    # otherwise-valid operator-custodied root for the SAME reserved
    # attempt under the SAME binding/package must fail closed BEFORE the
    # alternate root can acquire any authority namespace.
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="none")
    alt = tmp_path / "attacker-custody"
    alt.mkdir(parents=True, exist_ok=True)
    os.chmod(alt, 0o700)
    authority = world.authority()
    r, w = os.pipe()
    os.write(w, world.credential)
    os.close(w)
    try:
        with pytest.raises(bar.AuthorityRefused,
                           match="OUTPUT_CUSTODY_ROOT_MISMATCH"):
            authority.run_attempt(r, world.launcher_path,
                                  world.auditor_path, world.staging, alt)
        # the refusal PRECEDES any credential read: every synthetic byte
        # remains readable from the source pipe
        assert os.read(r, 65536) == world.credential
    finally:
        try:
            os.close(r)
        except OSError:
            pass
    # the alternate root acquired NO authority namespace at all
    assert list(alt.iterdir()) == []
    # no dynamic gate executed; no claim; no staging anywhere
    assert not world.order_file.exists()
    assert not list(world.output_root.glob("*.jsonl"))
    # pre-advance refusal: the SAME authority object stays PREPARED and
    # the FROZEN root then succeeds under normal synthetic execution
    assert authority.state == PREPARED
    assert world.run().report_state == REPORT_MISSING
    assert sorted(p.name for p in world.output_root.glob("*.jsonl")) == \
        [world.attempt_name() + ".jsonl"]
    # SAME-root duplicate-attempt semantics unchanged: a SECOND authority
    # process for the SAME attempt still refuses at the attempt-global
    # O_EXCL claim
    with pytest.raises(bar.AuthorityRefused, match="RECORD_CREATE_REFUSED"):
        world.run()


def test_ba_prep001_symlink_alias_output_root_refused(tmp_path):
    # documented identity semantics: the caller argument must equal the
    # binding-frozen path after os.path.normpath — a symlink ALIAS of
    # the frozen custody root is a different name and is refused
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="none")
    alias = tmp_path / "custody-alias"
    alias.symlink_to(world.output_root, target_is_directory=True)
    r, w = os.pipe()
    os.write(w, world.credential)
    os.close(w)
    try:
        with pytest.raises(bar.AuthorityRefused,
                           match="OUTPUT_CUSTODY_ROOT_MISMATCH"):
            world.authority().run_attempt(
                r, world.launcher_path, world.auditor_path,
                world.staging, alias)
        assert os.read(r, 65536) == world.credential
    finally:
        try:
            os.close(r)
        except OSError:
            pass
    assert not world.order_file.exists()
    assert not list(world.output_root.glob("*.jsonl"))


def test_ba_prep002_report_source_substitution_refused(tmp_path):
    # BA-PREP-002: report acceptance is mechanically bound to the exact
    # binding-frozen attempt-owned report source.  A DIFFERENT
    # pre-existing regular file whose bytes are otherwise a structurally
    # AND semantically VALID first-pass report for the SAME
    # target/event/role/attempt must NOT be acceptable by substitution.
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="none")
    substitute_bytes = make_report_for_role("AUDITOR_A")
    substitute = tmp_path / "attacker" / "substituted-report.json"
    substitute.parent.mkdir(parents=True, exist_ok=True)
    substitute.write_bytes(substitute_bytes)
    authority = world.authority()
    r, w = os.pipe()
    os.write(w, world.credential)
    os.close(w)
    try:
        with pytest.raises(bar.AuthorityRefused,
                           match="REPORT_SOURCE_MISMATCH"):
            authority.run_attempt(r, world.launcher_path,
                                  world.auditor_path, substitute,
                                  world.output_root)
        assert os.read(r, 65536) == world.credential
    finally:
        try:
            os.close(r)
        except OSError:
            pass
    # the substituted file was NOT accepted, NOT frozen and NOT
    # discarded; nothing executed; no stdout/stderr fallback; no output
    # artifacts of any kind
    assert substitute.read_bytes() == substitute_bytes
    assert not world.order_file.exists()
    assert not list(world.output_root.glob("*.json"))
    assert not list(world.output_root.glob("*.jsonl"))
    # the frozen-source REPORT_MISSING semantics are retained: with a
    # "none" launcher the frozen staging file is never written and the
    # honest outcome stays REPORT_MISSING (no reconstruction)
    assert authority.state == PREPARED
    result = world.run()
    assert result.report_state == REPORT_MISSING
    assert not list(world.output_root.glob("*.json"))


def test_ba_prep002_symlink_alias_report_source_refused(tmp_path):
    # a symlink alias of the frozen report source is a different name
    # and is refused; the normal path through the EXACT frozen source
    # still freezes (RB2 adaptation: the authority now CREATES the sink
    # itself O_EXCL, so the pre-fix fixture pre-write of the frozen
    # staging file is gone — a pre-existing object at the frozen sink
    # name is refused by test_rb2_002 below)
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="ok")
    alias = tmp_path / "staging-alias.json"
    alias.symlink_to(world.staging)
    r, w = os.pipe()
    os.write(w, world.credential)
    os.close(w)
    try:
        with pytest.raises(bar.AuthorityRefused,
                           match="REPORT_SOURCE_MISMATCH"):
            world.authority().run_attempt(
                r, world.launcher_path, world.auditor_path,
                alias, world.output_root)
        assert os.read(r, 65536) == world.credential
    finally:
        try:
            os.close(r)
        except OSError:
            pass
    assert not world.order_file.exists()
    result = world.run()
    assert result.report_state == REPORT_FROZEN


# --- BA-PREP-RB2-001 / BA-PREP-RB2-002 follow-up remediation: the
# binding freezes the custody directory OBJECT identity (st_dev/st_ino)
# and run_attempt (a) verifies the HELD custody fd IS that object before
# any claim and (b) creates the attempt report sink itself O_EXCL under
# the SAME held object after the gates and before any credential read;
# acceptance snapshots ONLY the held sink object -----------------------


def test_rb2_001_replacement_directory_same_pathname_refused(tmp_path):
    # RB2-001 Case A: an authorized custody directory renamed away and a
    # NEW otherwise-valid same-UID 0700 directory created at the EXACT
    # frozen pathname must NOT provide a fresh O_EXCL namespace for the
    # SAME reserved attempt: the pathname matches, the OBJECT does not.
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="none")
    root = world.output_root
    moved = tmp_path / "custody-moved-away"
    os.rename(root, moved)
    os.makedirs(root, mode=0o700)
    os.chmod(root, 0o700)
    authority = world.authority()
    r, w = os.pipe()
    os.write(w, world.credential)
    os.close(w)
    try:
        with pytest.raises(bar.AuthorityRefused,
                           match="OUTPUT_CUSTODY_OBJECT_MISMATCH"):
            authority.run_attempt(r, world.launcher_path,
                                  world.auditor_path, world.staging, root)
        # the refusal PRECEDES any credential read: every synthetic byte
        # remains readable from the source pipe
        assert os.read(r, 65536) == world.credential
    finally:
        try:
            os.close(r)
        except OSError:
            pass
    # ZERO dynamic gates; ZERO accounting records in EITHER object; the
    # replacement directory acquired NO authority namespace at all
    assert not world.order_file.exists()
    assert list(root.iterdir()) == []
    assert list(moved.iterdir()) == []
    # pre-advance refusal: the SAME authority object stays PREPARED and
    # succeeds once the frozen pathname names the frozen object again
    assert authority.state == PREPARED
    os.rmdir(root)
    os.rename(moved, root)
    assert world.run(authority=authority).report_state == REPORT_MISSING
    # BA-RB-001 semantics retained: a SECOND process for the SAME
    # attempt under the SAME frozen root still refuses at the
    # attempt-global O_EXCL claim
    with pytest.raises(bar.AuthorityRefused, match="RECORD_CREATE_REFUSED"):
        world.run()
    assert sorted(p.name for p in root.glob("*.jsonl")) == \
        [world.attempt_name() + ".jsonl"]


def test_rb2_001_single_run_rebind_accounting_uses_held_object(
        tmp_path, monkeypatch):
    # RB2-001 Case B: rebinding the frozen pathname to a DIFFERENT
    # directory object between the custody open and the accounting
    # create cannot split custody: the O_EXCL claim is created RELATIVE
    # TO THE SAME HELD verified directory object, never a pathname
    # re-open (the rebind is made deterministic by wrapping the store's
    # held-fd create primitive; no production test hook exists).
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="ok")
    root = world.output_root
    moved = tmp_path / "custody-moved-away"
    original = AccountingStore.create_at.__func__

    def rebinding_create_at(cls, dir_fd, attempt_id, binding_digest,
                            first_state="PREPARED"):
        os.rename(root, moved)          # rebind the pathname NOW
        os.makedirs(root, mode=0o700)
        os.chmod(root, 0o700)
        return original(cls, dir_fd, attempt_id, binding_digest,
                        first_state)

    monkeypatch.setattr(
        AccountingStore, "create_at",
        classmethod(rebinding_create_at))
    result = world.run()
    assert result.report_state == REPORT_MISSING
    # the attempt-global claim and the sink live in the HELD (moved)
    # object; the frozen output would freeze there too (held fd)
    assert sorted(p.name for p in moved.glob("*.jsonl")) == \
        [world.attempt_name() + ".jsonl"]
    assert not list(root.glob("*.jsonl"))
    # the launcher wrote its report through the REBOUND pathname into
    # the replacement object: those bytes were NEVER acceptable (honest
    # REPORT_MISSING above) and cleanup NEVER deleted the replacement
    replacement_report = root / world.staging.name
    assert replacement_report.read_bytes() == \
        make_report_for_role("AUDITOR_A")
    # the authority-owned sink object (in the HELD moved directory) was
    # safely discarded on the honest REPORT_MISSING terminal
    assert not (moved / world.staging.name).exists()


def test_rb2_002_preexisting_exact_frozen_report_refused(tmp_path):
    # RB2-002 B: a structurally AND semantically VALID report that
    # already exists at the EXACT frozen report pathname BEFORE the
    # attempt must NEVER become the accepted first pass: only an
    # authority-created sink object can (the authority fails closed
    # after the gates, BEFORE any credential read or model execution).
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="none")
    preexisting = make_report_for_role("AUDITOR_A")
    world.staging.write_bytes(preexisting)
    r, w = os.pipe()
    os.write(w, world.credential)
    os.close(w)
    try:
        with pytest.raises(bar.AuthorityRefused,
                           match="REPORT_SINK_PREEXISTING"):
            world.authority().run_attempt(
                r, world.launcher_path, world.auditor_path,
                world.staging, world.output_root)
        assert os.read(r, 65536) == world.credential
    finally:
        try:
            os.close(r)
        except OSError:
            pass
    # the pre-existing object was NOT accepted, NOT frozen, NOT
    # discarded (it is not the authority's object); no frozen artifact
    assert world.staging.read_bytes() == preexisting
    assert not list(world.output_root.glob("*.first-pass-report.json"))
    record = world.inspect_record()
    assert record["last_state"] == TERMINAL_PREEXEC_STOP
    assert CONSUMED_PRE_EXEC not in record["states"]
    assert EXEC_ATTEMPTED not in record["states"]


def test_rb2_002_sink_replacement_during_execution_not_accepted(tmp_path):
    # RB2-002 B: after the authority has created and HELD the sink, the
    # synthetic auditor UNLINKS the sink pathname and writes a fresh
    # otherwise-valid replacement object at the exact same pathname.
    # Acceptance reads ONLY the held original sink (empty -> honest
    # REPORT_MISSING); the replacement bytes are never accepted and
    # cleanup never deletes the replacement object.
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="replace")
    result = world.run()
    assert result.report_state == REPORT_MISSING
    assert not list(world.output_root.glob("*.first-pass-report.json"))
    # the replacement object survives untouched (never unlinked by the
    # authority's cleanup)
    assert world.staging.read_bytes() == make_report_for_role("AUDITOR_A")
    record = world.inspect_record()
    assert record["last_state"] == TERMINAL
    assert record["records"][-2]["terminal_reason"] == "REPORT_MISSING"


# --- BA-31: no public consume/resume/retry split -------------------------


def test_ba31_no_public_split_surface():
    forbidden = ("grant", "consume", "resume", "retry", "adopt_report",
                 "finish", "mint_attempt", "create_event")
    for name in forbidden:
        assert not hasattr(bar.BootstrapAuthority, name), name
    params = list(inspect.signature(
        bar.BootstrapAuthority.run_attempt).parameters)
    assert params == ["self", "credential_source_fd", "launcher_path",
                      "auditor_executable_path", "report_staging_path",
                      "output_root"]


# --- BA-32: exec failure remains spent/terminal ---------------------------


def test_ba32_exec_failure_spent(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="broken")
    result = world.run()
    assert result.exec_failed is True
    record = world.inspect_record()
    assert record["states"] == [PREPARED, GATES_PASSED,
                                CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
                                TERMINAL]
    terminal_reason = record["records"][-1]["terminal_reason"]
    assert terminal_reason.startswith("EXEC_FAILED_AFTER_CONSUMPTION")
    with pytest.raises(bar.AuthorityError):
        world.run()                       # no second operation exists


# --- BA-33: timeout kills the exact attempt process group -----------------


def test_ba33_timeout_kills_group(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="sleep",
                        wall_timeout=3)
    result = world.run()
    assert result.timed_out is True
    assert result.report_state == ""
    record = world.inspect_record()
    assert record["last_state"] == TERMINAL
    assert record["records"][-1]["terminal_reason"] == \
        "TIMEOUT_AFTER_CONSUMPTION"
    sleep_child = int(world.sleep_pid_file.read_text())
    # a SIGKILLed-but-not-yet-reaped process is still signalable, so
    # poll a bounded window for the actual reap (reparented to init)
    import time
    deadline = time.monotonic() + 3.0
    alive = True
    while time.monotonic() < deadline:
        try:
            os.kill(sleep_child, 0)
        except OSError:
            alive = False
            break
        time.sleep(0.05)
    assert alive is False, \
        "the spawned attempt-group member survived the timeout kill"


# --- BA-34: post-consumption accounting failure never success --------------


def test_ba34_accounting_failure_not_success(world_a, monkeypatch):
    original = AccountingStore.append

    def failing_append(self, state, extra=None):
        if state == TERMINAL:
            raise RuntimeError("SYNTHETIC-DURABLE-FAILURE")
        return original(self, state, extra)

    monkeypatch.setattr(AccountingStore, "append", failing_append)
    with pytest.raises(
            bar.PostConsumptionTerminalAccountingError):
        world_a.run()
    monkeypatch.undo()
    record = world_a.inspect_record()
    assert record["last_state"] == REPORT_FROZEN   # honest incompleteness
    assert TERMINAL not in record["states"]


# --- BA-35: ordinary credential file refused -------------------------------


def test_ba35_ordinary_file_credential_refused(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A")
    cred = tmp_path / "cred.txt"
    cred.write_bytes(world.credential)
    fd = os.open(cred, os.O_RDONLY)
    try:
        with pytest.raises(bar.AuthorityRefused, match="PREEXEC"):
            world.authority().run_attempt(fd, world.launcher_path,
                                          world.auditor_path,
                                          world.staging,
                                          world.output_root)
    finally:
        os.close(fd)
    record = world.inspect_record()
    assert record["last_state"] == TERMINAL_PREEXEC_STOP
    assert cred.read_bytes() == world.credential     # never consumed


# --- BA-38: launcher/auditor identity mismatch fails pre-consumption ------


def test_ba38_launcher_mismatch(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A")
    tampered = tmp_path / "tampered-launcher"
    tampered.write_bytes(b"#!/bin/sh\nexit 0\n")
    os.chmod(tampered, 0o755)
    with pytest.raises(bar.AuthorityRefused,
                       match="LAUNCHER_DIGEST_MISMATCH"):
        world.run(launcher_path=tampered)
    record = world.inspect_record()
    assert record["last_state"] == TERMINAL_PREEXEC_STOP
    assert CONSUMED_PRE_EXEC not in record["states"]


def test_ba38_auditor_mismatch(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A")
    tampered = tmp_path / "tampered-auditor"
    tampered.write_bytes(b"#!/bin/sh\nexit 0\n")
    os.chmod(tampered, 0o755)
    with pytest.raises(bar.AuthorityRefused,
                       match="PREEXEC_EXECUTABLE_IDENTITY_FAIL"):
        world.run(auditor_path=tampered)
    assert world.inspect_record()["last_state"] == \
        TERMINAL_PREEXEC_STOP


# --- BA-40: missing report stays REPORT_MISSING -----------------------------


def test_ba40_missing_report(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="none")
    result = world.run()
    assert result.report_state == REPORT_MISSING
    assert not list(world.output_root.glob("*.json"))
    record = world.inspect_record()
    assert record["last_state"] == TERMINAL


# --- BA-41: credential-contaminated report screened before persistence -----


def test_ba41_screen_fail(tmp_path):
    world = build_world(tmp_path, "AUDITOR_A", launcher_mode="contam")
    result = world.run()
    assert result.report_state == REPORT_SCREEN_FAIL
    assert not world.staging.exists()               # discarded staging
    assert not list(world.output_root.glob("*.json"))  # never persisted
    record = world.inspect_record()
    assert world.credential not in json.dumps(record).encode()


# --- BA-42..BA-50: report binding outcomes ----------------------------------


def _binding_mismatch_world(tmp_path, report_kwargs, token):
    world = build_world(tmp_path, "AUDITOR_A",
                        report=make_report(None, **report_kwargs))
    result = world.run()
    assert result.report_state == REPORT_INVALID
    record = world.inspect_record()
    terminal = record["records"][-2]
    assert terminal["state"] == REPORT_INVALID
    assert terminal["terminal_reason"] == token       # BA-49: token only
    assert record["last_state"] == TERMINAL           # BA-50
    assert not list(world.output_root.glob("*.json"))  # no freeze
    with pytest.raises(bar.AuthorityError):
        world.run()                                   # no retry (BA-50)
    return record


def test_ba44_wrong_target(tmp_path):
    from bootstrap_authority.binding import EVENT_ID, FROZEN_TARGET, \
        RESERVED_ATTEMPT_IDS
    record = _binding_mismatch_world(
        tmp_path,
        {"target_commit": WRONG_TARGET,
         "event_id": EVENT_ID, "auditor_role": "AUDITOR_A",
         "attempt_id": RESERVED_ATTEMPT_IDS["AUDITOR_A"]},
        "REPORT_TARGET_COMMIT_MISMATCH")
    # BA-49: the submitted wrong value never enters the record
    assert WRONG_TARGET not in json.dumps(record)


def test_ba45_wrong_event(tmp_path):
    from bootstrap_authority.binding import FROZEN_TARGET, \
        RESERVED_ATTEMPT_IDS
    record = _binding_mismatch_world(
        tmp_path,
        {"event_id": "AUCDEV-023-OTHER-EVENT-01",
         "target_commit": FROZEN_TARGET["commit"],
         "auditor_role": "AUDITOR_A",
         "attempt_id": RESERVED_ATTEMPT_IDS["AUDITOR_A"]},
        "REPORT_EVENT_ID_MISMATCH")
    assert "AUCDEV-023-OTHER-EVENT-01" not in json.dumps(record)


def test_ba46_wrong_role(tmp_path):
    from bootstrap_authority.binding import EVENT_ID, FROZEN_TARGET, \
        RESERVED_ATTEMPT_IDS
    _binding_mismatch_world(
        tmp_path,
        {"auditor_role": "AUDITOR_B",
         "target_commit": FROZEN_TARGET["commit"], "event_id": EVENT_ID,
         "attempt_id": RESERVED_ATTEMPT_IDS["AUDITOR_A"]},
        "REPORT_AUDITOR_ROLE_MISMATCH")


def test_ba47_wrong_attempt(tmp_path):
    from bootstrap_authority.binding import EVENT_ID, FROZEN_TARGET
    _binding_mismatch_world(
        tmp_path,
        {"attempt_id": "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01"
                       "-AUDITOR-Z-99",
         "target_commit": FROZEN_TARGET["commit"], "event_id": EVENT_ID,
         "auditor_role": "AUDITOR_A"},
        "REPORT_ATTEMPT_ID_MISMATCH")


def test_ba48_unparseable_dup_key_report(tmp_path):
    # a duplicate-key report passes the SHAPE-ONLY synthetic validator
    # (permissive json) but the authority's OWN strict reparse refuses
    from bootstrap_authority.binding import EVENT_ID, FROZEN_TARGET, \
        RESERVED_ATTEMPT_IDS
    body = ('{"attempt_id": "%s", "attempt_id": "%s", '
            '"auditor_role": "AUDITOR_A", "event_id": "%s", '
            '"findings": "[]", "target_commit": "%s"}\n'
            % (RESERVED_ATTEMPT_IDS["AUDITOR_A"],
               RESERVED_ATTEMPT_IDS["AUDITOR_A"], EVENT_ID,
               FROZEN_TARGET["commit"]))
    world = build_world(tmp_path, "AUDITOR_A",
                        report=body.encode())
    result = world.run()
    assert result.report_state == REPORT_INVALID
    record = world.inspect_record()
    assert record["records"][-2]["terminal_reason"] == \
        "REPORT_BINDING_UNPARSEABLE"
    assert not list(world.output_root.glob("*.json"))
