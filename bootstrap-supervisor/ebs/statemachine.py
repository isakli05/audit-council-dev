"""EBS-native one-shot attempt state machine (independently implemented).

TERMINAL_PREEXEC_STOP and TERMINAL are absorbing.  No reset, retry, or
mint interface exists on purpose: after consumption a replacement attempt
requires new operator authority and a NEW EBS process (adopted R1).
"""
from __future__ import annotations

PREPARED = "PREPARED"
GATES_PASSED = "GATES_PASSED"
CONSUMED_PRE_EXEC = "CONSUMED_PRE_EXEC"
EXEC_ATTEMPTED = "EXEC_ATTEMPTED"
REPORT_FROZEN = "REPORT_FROZEN"
REPORT_MISSING = "REPORT_MISSING"
REPORT_INVALID = "REPORT_INVALID"
REPORT_SCREEN_FAIL = "REPORT_SCREEN_FAIL"
TERMINAL_PREEXEC_STOP = "TERMINAL_PREEXEC_STOP"
TERMINAL = "TERMINAL"

STATES = frozenset({
    PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
    REPORT_FROZEN, REPORT_MISSING, REPORT_INVALID, REPORT_SCREEN_FAIL,
    TERMINAL_PREEXEC_STOP, TERMINAL,
})

ABSORBING = frozenset({TERMINAL_PREEXEC_STOP, TERMINAL})

TRANSITIONS = {
    PREPARED: frozenset({GATES_PASSED, TERMINAL_PREEXEC_STOP}),
    GATES_PASSED: frozenset({CONSUMED_PRE_EXEC, TERMINAL_PREEXEC_STOP}),
    CONSUMED_PRE_EXEC: frozenset({EXEC_ATTEMPTED, TERMINAL}),
    EXEC_ATTEMPTED: frozenset({REPORT_FROZEN, REPORT_MISSING,
                               REPORT_INVALID, REPORT_SCREEN_FAIL,
                               TERMINAL}),
    REPORT_FROZEN: frozenset({TERMINAL}),
    REPORT_MISSING: frozenset({TERMINAL}),
    REPORT_INVALID: frozenset({TERMINAL}),
    REPORT_SCREEN_FAIL: frozenset({TERMINAL}),
    TERMINAL_PREEXEC_STOP: frozenset(),
    TERMINAL: frozenset(),
}


class InvalidTransition(RuntimeError):
    """An illegal transition attempt; the caller must fail closed."""


class StateMachine:
    """In-memory machine for one EBS attempt (one process, one attempt)."""

    __slots__ = ("_state",)

    def __init__(self, state: str = PREPARED) -> None:
        if state not in STATES:
            raise InvalidTransition(f"UNKNOWN_STATE: {state}")
        self._state = state

    @property
    def state(self) -> str:
        return self._state

    def transition(self, next_state: str) -> str:
        if next_state not in TRANSITIONS[self._state]:
            raise InvalidTransition(
                f"ILLEGAL_TRANSITION {self._state} -> {next_state}; "
                "failing closed")
        self._state = next_state
        return next_state


def valid_path(sequence) -> bool:
    """True iff the recorded state sequence is a legal machine path."""
    seq = list(sequence)
    if not seq or seq[0] != PREPARED:
        return False
    return all(nxt in TRANSITIONS[cur]
               for cur, nxt in zip(seq, seq[1:]))
