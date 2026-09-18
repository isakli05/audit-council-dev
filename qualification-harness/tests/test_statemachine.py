"""C-2 preexec attempt lifecycle state machine — deterministic unit tests."""
from __future__ import annotations

import pytest

from qh.statemachine import (AttemptState, AttemptStateMachine,
                             InvalidTransition)


def test_full_valid_lifecycle():
    m = AttemptStateMachine()
    m.transition(AttemptState.BOUND, "bind")
    m.transition(AttemptState.PREEXEC_CHECKING, "gates")
    m.transition(AttemptState.CONSUMED_FOR_LAUNCH, "consume")
    m.transition(AttemptState.LAUNCHED, "exec")
    m.transition(AttemptState.TERMINAL, "done")
    assert m.state == AttemptState.TERMINAL
    assert m.is_terminal
    assert not m.launchable


def test_preexec_stop_terminal_absorbing():
    m = AttemptStateMachine()
    m.transition(AttemptState.BOUND, "bind")
    m.transition(AttemptState.PREEXEC_CHECKING, "gates")
    m.transition(AttemptState.TERMINAL_PREEXEC_STOP, "gate failure")
    assert m.is_terminal_preexec_stop
    assert not m.launchable
    with pytest.raises(InvalidTransition):
        m.transition(AttemptState.PREEXEC_CHECKING, "cannot resume")
    with pytest.raises(InvalidTransition):
        m.transition(AttemptState.CONSUMED_FOR_LAUNCH, "cannot consume")
    # force stop is idempotent on the terminal state
    m.force_terminal_preexec_stop("again")
    assert m.state == AttemptState.TERMINAL_PREEXEC_STOP


def test_invalid_transition_fails_closed():
    m = AttemptStateMachine()
    with pytest.raises(InvalidTransition):
        m.transition(AttemptState.CONSUMED_FOR_LAUNCH, "skip states")
    assert m.state == AttemptState.MINTED  # unchanged by the refusal


def test_skip_from_bound_to_consume_invalid():
    m = AttemptStateMachine()
    m.transition(AttemptState.BOUND, "bind")
    with pytest.raises(InvalidTransition):
        m.transition(AttemptState.CONSUMED_FOR_LAUNCH, "skip checking")


def test_force_terminal_preexec_stop_from_prestates():
    for reason_state in (AttemptState.MINTED, AttemptState.BOUND,
                         AttemptState.PREEXEC_CHECKING):
        m = AttemptStateMachine()
        if reason_state != AttemptState.MINTED:
            m.transition(AttemptState.BOUND, "bind")
        if reason_state == AttemptState.PREEXEC_CHECKING:
            m.transition(AttemptState.PREEXEC_CHECKING, "gates")
        m.force_terminal_preexec_stop("fail closed")
        assert m.is_terminal_preexec_stop
        assert not m.launchable


def test_force_stop_after_consumption_is_invalid():
    m = AttemptStateMachine()
    m.transition(AttemptState.BOUND, "bind")
    m.transition(AttemptState.PREEXEC_CHECKING, "gates")
    m.transition(AttemptState.CONSUMED_FOR_LAUNCH, "consume")
    with pytest.raises(InvalidTransition):
        m.force_terminal_preexec_stop("retroactive preexec stop")
    m.transition(AttemptState.LAUNCHED, "exec")
    m.transition(AttemptState.TERMINAL, "done")
    with pytest.raises(InvalidTransition):
        m.force_terminal_preexec_stop("after terminal")
