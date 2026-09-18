"""EBS-native one-shot state machine tests (task §25)."""
import pytest

from ebs.statemachine import (CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, GATES_PASSED,
                              PREPARED, REPORT_FROZEN, REPORT_MISSING,
                              REPORT_SCREEN_FAIL, TERMINAL,
                              TERMINAL_PREEXEC_STOP, InvalidTransition,
                              StateMachine, valid_path)


def test_valid_full_lifecycle():
    m = StateMachine()
    m.transition(GATES_PASSED)
    m.transition(CONSUMED_PRE_EXEC)
    m.transition(EXEC_ATTEMPTED)
    m.transition(REPORT_FROZEN)
    m.transition(TERMINAL)
    assert m.state == TERMINAL


def test_valid_lifecycle_report_missing():
    m = StateMachine()
    m.transition(GATES_PASSED)
    m.transition(CONSUMED_PRE_EXEC)
    m.transition(EXEC_ATTEMPTED)
    m.transition(REPORT_MISSING)
    m.transition(TERMINAL)


def test_valid_lifecycle_report_screen_fail():
    m = StateMachine()
    m.transition(GATES_PASSED)
    m.transition(CONSUMED_PRE_EXEC)
    m.transition(EXEC_ATTEMPTED)
    m.transition(REPORT_SCREEN_FAIL)
    m.transition(TERMINAL)


def test_valid_lifecycle_preexec_stop():
    m = StateMachine()
    m.transition(TERMINAL_PREEXEC_STOP)
    assert m.state == TERMINAL_PREEXEC_STOP


def test_invalid_transition_fails_closed():
    m = StateMachine()
    with pytest.raises(InvalidTransition):
        m.transition(CONSUMED_PRE_EXEC)  # cannot skip GATES_PASSED
    assert m.state == PREPARED  # unchanged by the refusal


def test_consume_cannot_occur_before_gates_pass():
    m = StateMachine(PREPARED)
    with pytest.raises(InvalidTransition):
        m.transition(CONSUMED_PRE_EXEC)


@pytest.mark.parametrize("resume", [PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC,
                                    REPORT_FROZEN])
def test_post_consumption_cannot_return_pre_consumption(resume):
    m = StateMachine()
    m.transition(GATES_PASSED)
    m.transition(CONSUMED_PRE_EXEC)
    with pytest.raises(InvalidTransition):
        m.transition(resume)


def test_terminal_preexec_stop_is_absorbing():
    m = StateMachine()
    m.transition(TERMINAL_PREEXEC_STOP)
    for target in (PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
                   REPORT_FROZEN, TERMINAL):
        with pytest.raises(InvalidTransition):
            m.transition(target)
    assert m.state == TERMINAL_PREEXEC_STOP


def test_terminal_is_absorbing():
    m = StateMachine()
    for step in (GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
                 REPORT_MISSING, TERMINAL):
        m.transition(step)
    for target in (PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
                   REPORT_FROZEN, TERMINAL_PREEXEC_STOP):
        with pytest.raises(InvalidTransition):
            m.transition(target)
    assert m.state == TERMINAL


def test_no_reset_retry_or_mint_interface_exists():
    forbidden = [name for name in dir(StateMachine)
                 if any(word in name.lower() for word in
                        ("reset", "retry", "mint", "restart", "rollback"))]
    assert forbidden == []


def test_valid_path_accepts_legal_sequence():
    assert valid_path([PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC,
                       EXEC_ATTEMPTED, REPORT_FROZEN, TERMINAL])


@pytest.mark.parametrize("seq", [
    [PREPARED, CONSUMED_PRE_EXEC],                       # skip gates
    [PREPARED, GATES_PASSED, EXEC_ATTEMPTED],            # skip consumption
    [PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC, PREPARED],  # backwards
    [GATES_PASSED],                                      # wrong start
    [PREPARED, TERMINAL],                                # illegal jump
    [],                                                  # empty
])
def test_valid_path_refuses_illegal_sequences(seq):
    assert not valid_path(seq)
