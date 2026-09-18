"""C-2 preexec attempt lifecycle state machine (mechanically terminal).

States (mandated model):

    MINTED -> BOUND -> PREEXEC_CHECKING -> CONSUMED_FOR_LAUNCH -> LAUNCHED
                                   \                 \
                                    -> TERMINAL_PREEXEC_STOP
                                                      (post-consumption
                                                       failure) -> TERMINAL
    LAUNCHED -> TERMINAL

Fail-closed rules:

* an INVALID transition attempt raises (and the caller must treat the
  attempt as terminal — ``force_terminal_preexec_stop`` implements the
  fail-closed forcing for pre-consumption states);
* TERMINAL_PREEXEC_STOP and TERMINAL are absorbing: no transition out;
* a failed mandatory preexec gate before provider/model execution forces
  TERMINAL_PREEXEC_STOP — the same bound grant can never return to a
  launchable state;
* attempt-grant consumption is NOT campaign model-engagement consumption
  (see qh/campaign.py — separate accounting, never touched by this machine).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .util import utc_now_iso


class AttemptState:
    MINTED = "MINTED"
    BOUND = "BOUND"
    PREEXEC_CHECKING = "PREEXEC_CHECKING"
    CONSUMED_FOR_LAUNCH = "CONSUMED_FOR_LAUNCH"
    TERMINAL_PREEXEC_STOP = "TERMINAL_PREEXEC_STOP"
    LAUNCHED = "LAUNCHED"
    TERMINAL = "TERMINAL"


class InvalidTransition(RuntimeError):
    """Raised on any transition not in the allowed table — the caller must
    fail closed (stop the attempt); never continue on this exception."""


_ALLOWED = {
    (AttemptState.MINTED, AttemptState.BOUND),
    (AttemptState.BOUND, AttemptState.PREEXEC_CHECKING),
    (AttemptState.PREEXEC_CHECKING, AttemptState.CONSUMED_FOR_LAUNCH),
    (AttemptState.PREEXEC_CHECKING, AttemptState.TERMINAL_PREEXEC_STOP),
    (AttemptState.CONSUMED_FOR_LAUNCH, AttemptState.LAUNCHED),
    (AttemptState.CONSUMED_FOR_LAUNCH, AttemptState.TERMINAL),
    (AttemptState.LAUNCHED, AttemptState.TERMINAL),
}

_TERMINAL_STATES = (AttemptState.TERMINAL_PREEXEC_STOP, AttemptState.TERMINAL)

# states from which a fail-closed forced preexec stop is legal
_FORCE_STOPPABLE = (AttemptState.MINTED, AttemptState.BOUND,
                    AttemptState.PREEXEC_CHECKING)


@dataclass
class TransitionRecord:
    from_state: str
    to_state: str
    reason: str
    at: str


@dataclass
class AttemptStateMachine:
    state: str = AttemptState.MINTED
    history: list[TransitionRecord] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.history.append(
            TransitionRecord("", self.state, "machine-initialized",
                             utc_now_iso()))

    @property
    def is_terminal(self) -> bool:
        return self.state in _TERMINAL_STATES

    @property
    def is_terminal_preexec_stop(self) -> bool:
        return self.state == AttemptState.TERMINAL_PREEXEC_STOP

    @property
    def launchable(self) -> bool:
        """True only while a protected launch may still legally proceed."""
        return self.state in (AttemptState.BOUND, AttemptState.PREEXEC_CHECKING)

    def transition(self, to_state: str, reason: str) -> "AttemptStateMachine":
        key = (self.state, to_state)
        if key not in _ALLOWED:
            raise InvalidTransition(
                f"illegal transition {self.state} -> {to_state} ({reason}); "
                "failing closed")
        self.history.append(
            TransitionRecord(self.state, to_state, reason, utc_now_iso()))
        self.state = to_state
        return self

    def force_terminal_preexec_stop(self, reason: str) -> None:
        """Fail-closed forced stop for pre-consumption states.  Terminal
        states are already dead (idempotent for TERMINAL_PREEXEC_STOP).
        Post-consumption states cannot retroactively become preexec stops —
        that attempt raises."""
        if self.state == AttemptState.TERMINAL_PREEXEC_STOP:
            return
        if self.state not in _FORCE_STOPPABLE:
            raise InvalidTransition(
                f"cannot force preexec stop from {self.state} ({reason}); "
                "post-consumption outcomes are terminal, never preexec")
        self.history.append(
            TransitionRecord(self.state, AttemptState.TERMINAL_PREEXEC_STOP,
                             reason, utc_now_iso()))
        self.state = AttemptState.TERMINAL_PREEXEC_STOP
