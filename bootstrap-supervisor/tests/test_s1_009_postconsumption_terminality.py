"""Focused S1-009 suite (AUCDEV023-CR-EBS-S1-009
POST_CONSUMPTION_EXCEPTION_TERMINALIZATION_CAN_ESCAPE_PROCESS_BOUND_CLEANUP).

Every credential byte here is SYNTHETIC and INERT; every launched child
is a repository test fixture (inert boundary launcher / inert hanging
boundary launcher); the auditor executable is the inert synthetic
fixture and is NEVER executed.  No provider, no network, no real event
package, no canonical event id.

Deterministic fault-injection matrix (tasking §14/§15/§16): parent-side
failures AFTER the durable EXEC_ATTEMPTED transition (os.set_blocking /
non-BlockingIOError os.read / waitpid(WNOHANG) injections), the
timeout-path TERMINAL append failure, a TERMINAL transition failure
fallback, report-path terminal/outcome-state append failures, the
original+accounting double failure, and the normal consumed failure with
successful terminal persistence — each proving the centralized
post-consumption settlement: durable accounting attempted honestly
(first failure preserves the existing record exactly, nothing
fabricated), in-process TERMINAL guaranteed even when the durable
TERMINAL is absent, custody and EVERY held fd closed in a guaranteed
path, the attempt child/process group cleaned before caller control, no
same-attempt retry, and exact returned-vs-raised outcomes — a durable
accounting failure raises POSTCONSUMPTION_TERMINAL_ACCOUNTING_FAILED
and never yields a success/timed-out/conforming AttemptResult.
"""
import errno
import os
import time

import pytest

from ebs.accounting import inspect_accounting_record
from ebs.launch import LaunchError
from ebs.statemachine import (CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, GATES_PASSED,
                              InvalidTransition, PREPARED, REPORT_FROZEN,
                              REPORT_INVALID, REPORT_MISSING,
                              REPORT_SCREEN_FAIL, StateMachine, TERMINAL,
                              TERMINAL_PREEXEC_STOP)

from conftest import (binding_for, clear_nr_tracks, clear_rg_tracks,
                      clear_val_tracks, hang_track, make_event_package,
                      nr_paths, pipe_source, rg_paths, sha_hex)
from test_final_execution_lifecycle import (ATTEMPT, CLEAN_REPORT, build,
                                            custody_is_closed, gate_count,
                                            hanging_scenario,
                                            held_fds_closed, pid_alive, run,
                                            states_of)

ACCOUNTING_TOKEN = "POSTCONSUMPTION_TERMINAL_ACCOUNTING_FAILED"
POST_CONSUMPTION_MACHINE_STATES = (CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
                                   REPORT_FROZEN, REPORT_MISSING,
                                   REPORT_INVALID, REPORT_SCREEN_FAIL)


def accounting_error_type():
    """The exact settlement-failure classification (absent on the RED
    base; the LaunchError fallback keeps collection clean while every
    accounting assertion REDs against the base behavior)."""
    from ebs import launch as launch_mod
    return getattr(launch_mod, "PostConsumptionTerminalAccountingError",
                   LaunchError)


@pytest.fixture(autouse=True)
def clean_tracks():
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    clear_val_tracks(ATTEMPT)
    yield
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    clear_val_tracks(ATTEMPT)


def record_view(cust_dir, sup):
    return inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)


def exec_attempted_child_pid(cust_dir, sup) -> int:
    return [r for r in record_view(cust_dir, sup)["records"]
            if r["state"] == EXEC_ATTEMPTED][-1]["child_pid"]


def refuse_second_run(sup) -> None:
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        sup.run_attempt(pipe_source(), "/x", "/x", "/x", "/x")


def assert_fail_closed_settled(sup, cust_dir, durable_last,
                               reason_sub=None) -> None:
    """Shared §16 block: exact in-process state, exact durable last
    state, custody closure, held-fd closure, retry refusal."""
    assert sup.state == TERMINAL
    view = record_view(cust_dir, sup)
    assert view["states"][-1] == durable_last
    if reason_sub is not None:
        assert reason_sub in view["records"][-1].get("terminal_reason", "")
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)
    refuse_second_run(sup)


def inject_once(monkeypatch, obj, name, guard):
    """One-shot fault injection: the FIRST call whose arguments satisfy
    guard raises an exact injected OSError; every other call delegates
    to the real function (deterministic, no timing dependence)."""
    real = getattr(obj, name)
    fired = []

    def wrapper(*args, **kwargs):
        if not fired and guard(*args, **kwargs):
            fired.append(True)
            raise OSError(errno.EIO,
                          f"S1-009-INJECTED-{name.upper()}")
        return real(*args, **kwargs)

    monkeypatch.setattr(obj, name, wrapper)


def inject_append(monkeypatch, sup, target_state):
    """Inject durable-append failure for exactly one target state,
    reached from a post-consumption machine state only."""
    store = sup._store
    real = store.append

    def wrapper(state, extra=None):
        if state == target_state and sup._machine.state in \
                POST_CONSUMPTION_MACHINE_STATES:
            raise OSError(errno.ENOSPC,
                          f"S1-009-INJECTED-APPEND-{target_state}")
        return real(state, extra=extra)

    monkeypatch.setattr(store, "append", wrapper)


def inject_terminal_transition(monkeypatch, sup):
    """Inject a TERMINAL *transition* failure (class-level patch — the
    slotted machine forbids instance attribute assignment)."""
    machine_type = type(sup._machine)
    real = machine_type.transition

    def wrapper(self, next_state):
        if next_state == TERMINAL:
            raise InvalidTransition("S1-009-INJECTED-TERMINAL-TRANSITION")
        return real(self, next_state)

    monkeypatch.setattr(machine_type, "transition", wrapper)


def wait_pid_gone(pid: int, seconds: float = 5.0) -> None:
    until = time.monotonic() + seconds
    while pid_alive(pid) and time.monotonic() < until:
        time.sleep(0.05)
    assert not pid_alive(pid), f"pid {pid} survived the settlement cleanup"


# ===== RED-009-A/B/C/D + GREEN matrix: parent-side failures ===========

@pytest.mark.parametrize("inject", [
    ("os", "set_blocking",
     lambda sup: (lambda fd, flag: sup._machine.state == EXEC_ATTEMPTED)),
    ("os", "waitpid",
     lambda sup: (lambda pid, options: options == os.WNOHANG
                  and sup._machine.state == EXEC_ATTEMPTED)),
    ("os", "read",
     lambda sup: (lambda fd, count: sup._machine.state == EXEC_ATTEMPTED)),
], ids=["set_blocking", "waitpid-wnohang", "nonblocking-read"])
def test_s1_009_parent_failure_after_exec_attempted_settles_fail_closed(
        inject, launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out, monkeypatch):
    """RED-009-A/B: a parent-side failure AFTER the durable
    EXEC_ATTEMPTED transition (set_blocking / waitpid(WNOHANG) /
    non-BlockingIOError read) settles fail-closed INSIDE the call —
    in-process TERMINAL, durable TERMINAL with the exact reason, the
    attempt child killed/reaped, custody + every held fd closed, no
    retry, and the ORIGINAL failure re-raised (durable settlement
    succeeded)."""
    where, name, guard_of = inject
    sup = build(cust_dir, binding_doc, event_package)
    inject_once(monkeypatch, os if where == "os" else sup, name, guard_of(sup))
    with pytest.raises(OSError, match="S1-009-INJECTED"):
        run(sup, launcher, auditor_exe, stage, cust_out)
    assert_fail_closed_settled(
        sup, cust_dir, TERMINAL, "PARENT_FAILURE_AFTER_EXEC_ATTEMPTED")
    wait_pid_gone(exec_attempted_child_pid(cust_dir, sup))
    assert gate_count(nr_paths) == 1      # both gates still exactly once
    assert gate_count(rg_paths) == 1


def test_s1_009_pre_fork_failure_after_consumption_settles(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out, monkeypatch):
    """Regression: a failure while still CONSUMED_PRE_EXEC (here the
    defense-in-depth post-consumption re-hash) keeps the distinct
    PRE_EXEC_FAILURE_AFTER_CONSUMPTION durable reason under the SAME
    centralized settlement."""
    from ebs import launch as launch_mod
    sup = build(cust_dir, binding_doc, event_package)
    inject_once(monkeypatch, launch_mod.Supervisor, "_rehash_held",
                lambda *args: args and args[-1] == "AFTER_CONSUMPTION")
    with pytest.raises(OSError, match="S1-009-INJECTED"):
        run(sup, launcher, auditor_exe, stage, cust_out)
    assert_fail_closed_settled(
        sup, cust_dir, TERMINAL, "PRE_EXEC_FAILURE_AFTER_CONSUMPTION")


# ===== timeout path ====================================================

def test_s1_009_timeout_terminal_append_failure_raises_incomplete(
        launcher, auditor_exe, cust_dir, tmp_path, stage, cust_out,
        monkeypatch):
    """RED-009-C: the timeout path's TERMINAL append failure raises the
    exact accounting-incompleteness error (never a timed-out
    AttemptResult), leaves in-process TERMINAL with custody/fds closed,
    does NOT fabricate a durable TERMINAL (last durable state stays
    EXEC_ATTEMPTED), kills/reaps the whole hanging attempt tree, and
    refuses any retry."""
    sup, hang = hanging_scenario(cust_dir, tmp_path, auditor_exe,
                                 auditor_timeout=1)
    inject_append(monkeypatch, sup, TERMINAL)
    with pytest.raises(accounting_error_type(),
                       match=ACCOUNTING_TOKEN) as excinfo:
        sup.run_attempt(pipe_source(), str(hang[0]), str(auditor_exe[0]),
                        str(stage), str(cust_out))
    error = excinfo.value
    assert "S1-009-INJECTED-APPEND" in str(error)
    assert getattr(error, "accounting_error", None) is not None
    assert sup.state == TERMINAL            # in-process death regardless
    view = record_view(cust_dir, sup)
    assert view["states"] == [PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC,
                              EXEC_ATTEMPTED]   # nothing fabricated
    assert not any(cust_out.iterdir())      # no report accepted/frozen
    track = hang_track(ATTEMPT)
    assert track is not None
    for pid in (track["launcher_pid"], track["descendant_pid"]):
        wait_pid_gone(pid)
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)
    refuse_second_run(sup)


def test_s1_009_timeout_transition_failure_falls_back_fail_closed(
        launcher, auditor_exe, cust_dir, tmp_path, stage, cust_out,
        monkeypatch):
    """RED-009-D: a TERMINAL *transition* failure after a SUCCESSFUL
    TERMINAL append (durable chain complete) does not skip cleanup —
    the narrow fail-closed primitive lands in-process TERMINAL, the
    normal timed-out AttemptResult is returned, custody/fds close, no
    retry."""
    sup, hang = hanging_scenario(cust_dir, tmp_path, auditor_exe,
                                 auditor_timeout=1)
    inject_terminal_transition(monkeypatch, sup)
    result = sup.run_attempt(pipe_source(), str(hang[0]),
                             str(auditor_exe[0]), str(stage), str(cust_out))
    assert result.timed_out is True
    terminal = record_view(cust_dir, sup)["records"][-1]
    assert terminal["state"] == TERMINAL
    assert terminal["terminal_reason"] == "TIMEOUT_AFTER_CONSUMPTION"
    assert sup.state == TERMINAL
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)
    refuse_second_run(sup)


# ===== report lifecycle settlement =====================================

def test_s1_009_report_frozen_terminal_append_failure(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out, monkeypatch):
    """A TERMINAL append failure after a successful REPORT_FROZEN
    append raises the exact incompleteness error — the already-frozen
    artifact REMAINS operator-custodied evidence (never deleted), the
    durable record keeps REPORT_FROZEN as its last state (no fabricated
    TERMINAL), in-process state is TERMINAL, custody/fds closed, no
    conforming AttemptResult is returned, no retry."""
    sup = build(cust_dir, binding_doc, event_package)
    stage.write_bytes(CLEAN_REPORT)
    inject_append(monkeypatch, sup, TERMINAL)
    with pytest.raises(accounting_error_type(), match=ACCOUNTING_TOKEN):
        run(sup, launcher, auditor_exe, stage, cust_out)
    assert sup.state == TERMINAL
    assert record_view(cust_dir, sup)["states"][-1] == REPORT_FROZEN
    frozen = cust_out / sup._binding.output_identity["name"]
    assert frozen.read_bytes() == CLEAN_REPORT   # evidence preserved
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)
    refuse_second_run(sup)


def test_s1_009_report_outcome_append_failure(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out, monkeypatch):
    """A report-outcome-state append failure (here REPORT_MISSING)
    raises the exact incompleteness error, preserves the durable record
    exactly as it exists (last durable state stays EXEC_ATTEMPTED —
    neither the outcome state nor TERMINAL is fabricated), leaves
    in-process TERMINAL with custody/fds closed, and returns nothing."""
    sup = build(cust_dir, binding_doc, event_package)
    inject_append(monkeypatch, sup, REPORT_MISSING)
    with pytest.raises(accounting_error_type(), match=ACCOUNTING_TOKEN):
        run(sup, launcher, auditor_exe, stage, cust_out)
    assert sup.state == TERMINAL
    view = record_view(cust_dir, sup)
    assert view["states"] == [PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC,
                              EXEC_ATTEMPTED]
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)
    refuse_second_run(sup)


def test_s1_009_normal_consumed_failure_settles_with_terminal(
        cust_dir, tmp_path, launcher, auditor_exe, stage, cust_out):
    """Regression: the normal exec-failed consumed path settles through
    the SAME primitive with successful durable persistence — a normal
    (non-conforming-report) AttemptResult is returned only because the
    terminal chain completed."""
    bogus = tmp_path / "bogus_launcher_s1_009.py"
    bogus.write_text("this is not an executable image\n")
    doc = binding_for(sha_hex(bogus.read_bytes()),
                      auditor_sha256=auditor_exe[1])
    pkg = make_event_package(doc, tmp_path, name="pkg-s1-009-bogus")
    sup = build(cust_dir, doc, pkg)
    result = sup.run_attempt(pipe_source(), str(bogus),
                             str(auditor_exe[0]), str(stage), str(cust_out))
    assert result.exec_failed and result.report_state == ""
    assert_fail_closed_settled(
        sup, cust_dir, TERMINAL, "EXEC_FAILED_AFTER_CONSUMPTION")


# ===== original + settlement double failure ============================

def test_s1_009_original_and_accounting_failures_both_recoverable(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out, monkeypatch):
    """§9: when an original post-consumption failure AND a terminal
    accounting failure both occur, the raised incompleteness error
    carries BOTH mechanically recoverable — in the message, in chained
    attributes, and on the exception chain — with no silent
    replacement."""
    sup = build(cust_dir, binding_doc, event_package)
    inject_once(monkeypatch, os, "set_blocking",
                lambda fd, flag: sup._machine.state == EXEC_ATTEMPTED)
    inject_append(monkeypatch, sup, TERMINAL)
    with pytest.raises(accounting_error_type(),
                       match=ACCOUNTING_TOKEN) as excinfo:
        run(sup, launcher, auditor_exe, stage, cust_out)
    error = excinfo.value
    assert "S1-009-INJECTED-SET_BLOCKING" in str(error)   # original
    assert "S1-009-INJECTED-APPEND" in str(error)         # accounting
    assert isinstance(getattr(error, "original_error", None), OSError)
    assert isinstance(getattr(error, "accounting_error", None), OSError)
    assert isinstance(error.__cause__, OSError)           # chained
    assert sup.state == TERMINAL
    assert record_view(cust_dir, sup)["states"][-1] == EXEC_ATTEMPTED
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)
    refuse_second_run(sup)


# ===== preexec semantics unchanged =====================================

def test_s1_009_fail_closed_terminal_primitive_bounds():
    """§7/§13: the narrow state-machine primitive accepts ONLY
    post-consumption sources (plus idempotent TERMINAL), refuses
    PREPARED / GATES_PASSED / TERMINAL_PREEXEC_STOP, never leaves
    TERMINAL, and creates no reset/retry/resume surface."""
    assert hasattr(StateMachine, "fail_closed_terminal")
    for state in (PREPARED, GATES_PASSED, TERMINAL_PREEXEC_STOP):
        with pytest.raises(InvalidTransition):
            StateMachine(state).fail_closed_terminal()
    for state in POST_CONSUMPTION_MACHINE_STATES:
        machine = StateMachine(state)
        assert machine.fail_closed_terminal() == TERMINAL
        assert machine.state == TERMINAL
        with pytest.raises(InvalidTransition):    # TERMINAL absorbing
            machine.transition(PREPARED)
        with pytest.raises(InvalidTransition):
            machine.transition(EXEC_ATTEMPTED)
    assert StateMachine(TERMINAL).fail_closed_terminal() == TERMINAL
    assert not hasattr(StateMachine, "reset")
    assert not hasattr(StateMachine, "retry")


def test_s1_009_preexec_refusal_stays_terminal_preexec_stop(
        cust_dir, tmp_path, launcher, auditor_exe, stage, cust_out):
    """§13: a preexec refusal is NOT converted into consumed TERMINAL
    semantics — TERMINAL_PREEXEC_STOP with authority unconsumed, both
    gate counts zero, custody closed, no retry."""
    bogus = tmp_path / "bogus_auditor_s1_009.py"
    bogus.write_text("not an executable image\n")
    doc = binding_for(launcher[1], auditor_sha256=sha_hex(
        bogus.read_bytes()))
    pkg = make_event_package(doc, tmp_path, name="pkg-s1-009-preexec")
    sup = build(cust_dir, doc, pkg)
    with pytest.raises(LaunchError, match="EXECUTABLE_IDENTITY_FAIL"):
        sup.run_attempt(pipe_source(), str(launcher[0]), str(bogus),
                        str(stage), str(cust_out))
    assert sup.state == TERMINAL_PREEXEC_STOP
    assert states_of(cust_dir, sup) == [PREPARED, TERMINAL_PREEXEC_STOP]
    assert gate_count(nr_paths) == 0
    assert gate_count(rg_paths) == 0
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)
    refuse_second_run(sup)
