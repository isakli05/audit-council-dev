#!/usr/bin/env python3
"""model_selection.py — AUCDEV-024 auditor model-selection policy.

Single canonical definition of HOW an Audit Council run selects each
auditor's exact model identity and effort, and of the immutable
pre-inference provenance record that freezes the resolved selection.

Modes and precedence (objective §3/§8-D):

    explicit > explicitly requested inherit > audit-default

- audit-default: Auditor A (opus/Claude) = claude-opus-5-5 / high;
  Auditor B (codex/Codex) = gpt-6.1-sol / high.
- inherit: ONLY when explicitly requested. Must resolve to CONCRETE exact
  identities BEFORE any inference; unresolved / ambiguous / unobservable /
  symbolic inheritance FAILS CLOSED with zero inference (readiness blocker
  AUCDEV024-ZP-B1 routing). Codex source: top-level `model` +
  `model_reasoning_effort` keys of ~/.codex/config.toml. Claude source:
  ANTHROPIC_MODEL + CLAUDE_CODE_EFFORT_LEVEL environment variables.
- explicit: caller supplies BOTH a concrete supported model AND a concrete
  supported effort; partial explicit selection fails closed (filling the
  missing half from defaults would be a silent fallback).

NO silent fallback anywhere: an unsupported, unavailable or symbolic value
raises ModelSelectionError — it is never swapped for another generation,
alias or effort level (objective §8-H).

Legacy identities (claude-opus-5, gpt-5.6-sol, xhigh) remain valid values —
selectable explicitly and required when resuming runs frozen with them — but
historical artifacts are never relabelled and resumes never migrate
generations (objective §7).

The Auditor-A (Claude) selection is additionally bound to the OBSERVABLE
per-turn effective effort (CLAUDE_EFFORT, after any client downgrade/clamp;
AUCDEV024-CR-IMPL-002): an absent or mismatched effective effort fails
closed before preflight, run creation or resume accepts inference-readiness
— never silently downgraded, never faked from requested values.

Stdlib only. Values of environment variables are never logged by this
module (callers surface variable NAMES only).
"""
from __future__ import annotations

import hashlib
import json
import os

# ---------------------------------------------------------------------------
# Policy constants (mirrored by audit_council.PUBLIC_CONTRACT["model_selection"]
# and by drift tests — keep the three in agreement)
# ---------------------------------------------------------------------------

MODES = ("audit-default", "inherit", "explicit")

AUDITORS = ("opus", "codex")

SUPPORTED_MODELS = {
    "opus": ("claude-opus-5-5", "claude-opus-5"),
    "codex": ("gpt-6.1-sol", "gpt-5.6-sol"),
}
SUPPORTED_EFFORTS = {
    "opus": ("high", "medium", "low"),
    # xhigh is the LEGACY gpt-5.6-sol reasoning level: kept selectable so a
    # frozen legacy run can be resumed exactly, never a new-generation default
    "codex": ("high", "medium", "low", "minimal", "xhigh"),
}

DEFAULT_MODEL = {"opus": "claude-opus-5-5", "codex": "gpt-6.1-sol"}
DEFAULT_EFFORT = {"opus": "high", "codex": "high"}

# Symbolic / unresolved tokens that may NEVER reach inference (objective §3-2)
SYMBOLIC_TOKENS = frozenset({
    "", "current", "default", "auto", "latest", "inherit", "none", "null",
    "undefined", "opus", "sonnet", "haiku", "codex", "gpt", "claude",
})

# Ambient Claude-side model-selection inputs (readiness blocker ZP-B2): in
# audit-default/explicit mode every one of these must be UNSET or exactly
# equal the resolved selection, or the run fails closed before inference.
# Values are compared but never printed.
CLAUDE_MODEL_ENV_VARS = (
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "ANTHROPIC_DEFAULT_FABLE_MODEL",
    "CLAUDE_CODE_MAIN_MODEL",
    "CLAUDE_CODE_SUBAGENT_MODEL",
)
CLAUDE_EFFORT_ENV_VARS = ("CLAUDE_CODE_EFFORT_LEVEL",)
CLAUDE_SELECTION_ENV_VARS = CLAUDE_MODEL_ENV_VARS + CLAUDE_EFFORT_ENV_VARS

# inherit-mode resolution sources (explicitly defined per objective §3-2)
CLAUDE_INHERIT_MODEL_ENV = "ANTHROPIC_MODEL"
CLAUDE_INHERIT_EFFORT_ENV = "CLAUDE_CODE_EFFORT_LEVEL"
CODEX_INHERIT_CONFIG = os.path.join("~", ".codex", "config.toml")

_SELECTION_CORE_FIELDS = (
    "auditor", "mode", "source", "requested_model", "requested_effort",
    "model", "effort",
)


class ModelSelectionError(Exception):
    """Fail-closed selection violation. `reason` is a stable machine token."""

    def __init__(self, reason: str, detail: str = ""):
        self.reason = reason
        super().__init__("MODEL_SELECTION:%s%s" % (reason,
                                                   (": " + detail) if detail else ""))


# ---------------------------------------------------------------------------
# value validation
# ---------------------------------------------------------------------------

def _check_concrete(auditor: str, kind: str, value) -> str:
    """Validate one concrete identity value; returns it unchanged or raises."""
    supported = (SUPPORTED_MODELS if kind == "model" else SUPPORTED_EFFORTS)[auditor]
    token = "MODEL" if kind == "model" else "EFFORT"
    if not isinstance(value, str) or isinstance(value, bool):
        raise ModelSelectionError(
            "UNSUPPORTED_%s" % token,
            "%s selection for %s must be a concrete string, got %r"
            % (kind, auditor, value))
    if value.strip().lower() in SYMBOLIC_TOKENS:
        raise ModelSelectionError(
            "SYMBOLIC_%s" % token,
            "symbolic/unresolved %s value %r may never reach inference "
            "(no silent resolution)" % (kind, value))
    if value not in supported:
        raise ModelSelectionError(
            "UNSUPPORTED_%s" % token,
            "%s selection %r for %s is not supported (no fallback); "
            "supported: %s" % (kind, value, auditor, list(supported)))
    return value


# ---------------------------------------------------------------------------
# inherit sources
# ---------------------------------------------------------------------------

def codex_inherit_source(config_path: str | None = None) -> tuple:
    """Resolve the codex inherit source to (model, effort) concrete values.

    Top-level `model` and `model_reasoning_effort` keys of the codex user
    config ONLY: profile-derived or otherwise nested values are not
    pre-inference resolvable and therefore fail closed."""
    path = os.path.expanduser(config_path or CODEX_INHERIT_CONFIG)
    if not os.path.isfile(path):
        raise ModelSelectionError(
            "INHERIT_UNRESOLVED",
            "codex inherit requested but config %s is absent" % path)
    try:
        import tomllib
        with open(path, "rb") as fh:
            doc = tomllib.load(fh)
    except (OSError, ValueError, ImportError) as exc:
        raise ModelSelectionError(
            "INHERIT_UNRESOLVED", "codex config unreadable: %s" % exc)
    model = doc.get("model")
    effort = doc.get("model_reasoning_effort")
    if model is None or effort is None:
        missing = [k for k, v in (("model", model),
                                  ("model_reasoning_effort", effort))
                   if v is None]
        raise ModelSelectionError(
            "INHERIT_UNRESOLVED",
            "codex inherit requires BOTH top-level config keys; missing %s"
            % missing)
    return model, effort


def claude_inherit_source(environ=None) -> tuple:
    """Resolve the Claude inherit source to (model, effort) concrete values."""
    env = os.environ if environ is None else environ
    model = env.get(CLAUDE_INHERIT_MODEL_ENV)
    effort = env.get(CLAUDE_INHERIT_EFFORT_ENV)
    if model is None or effort is None:
        missing = [n for n, v in ((CLAUDE_INHERIT_MODEL_ENV, model),
                                  (CLAUDE_INHERIT_EFFORT_ENV, effort))
                   if v is None]
        raise ModelSelectionError(
            "INHERIT_UNRESOLVED",
            "claude inherit requires BOTH %s and %s; missing %s (an ambient "
            "model redirect alone does not satisfy the effort requirement)"
            % (CLAUDE_INHERIT_MODEL_ENV, CLAUDE_INHERIT_EFFORT_ENV, missing))
    return model, effort


# ---------------------------------------------------------------------------
# resolution
# ---------------------------------------------------------------------------

def resolve(auditor: str, *, explicit_model=None, explicit_effort=None,
            inherit_requested: bool = False,
            environ=None, codex_config_path: str | None = None) -> dict:
    """Resolve the selection for `auditor` ("opus" | "codex").

    Returns {auditor, mode, source, requested_model, requested_effort,
    model, effort}. Raises ModelSelectionError on ANY non-concrete,
    unsupported, partial or ambiguous request — never falls back."""
    if auditor not in AUDITORS:
        raise ModelSelectionError("UNKNOWN_AUDITOR", repr(auditor))

    if explicit_model is not None or explicit_effort is not None:
        if explicit_model is None or explicit_effort is None:
            raise ModelSelectionError(
                "EXPLICIT_PARTIAL",
                "explicit selection requires BOTH model and effort (a "
                "missing half must not silently fall back to the default)")
        return {
            "auditor": auditor,
            "mode": "explicit",
            "source": "cli",
            "requested_model": explicit_model,
            "requested_effort": explicit_effort,
            "model": _check_concrete(auditor, "model", explicit_model),
            "effort": _check_concrete(auditor, "effort", explicit_effort),
        }

    if inherit_requested:
        if auditor == "codex":
            raw_model, raw_effort = codex_inherit_source(codex_config_path)
            source = "codex-config-toml"
        else:
            raw_model, raw_effort = claude_inherit_source(environ)
            source = "claude-ambient-env"
        return {
            "auditor": auditor,
            "mode": "inherit",
            "source": source,
            "requested_model": raw_model,
            "requested_effort": raw_effort,
            "model": _check_concrete(auditor, "model", raw_model),
            "effort": _check_concrete(auditor, "effort", raw_effort),
        }

    return {
        "auditor": auditor,
        "mode": "audit-default",
        "source": "audit-default",
        "requested_model": None,
        "requested_effort": None,
        "model": DEFAULT_MODEL[auditor],
        "effort": DEFAULT_EFFORT[auditor],
    }


# ---------------------------------------------------------------------------
# immutable pre-inference provenance (objective §8-E)
# ---------------------------------------------------------------------------

def selection_core(selection: dict) -> dict:
    return {k: selection.get(k) for k in _SELECTION_CORE_FIELDS}


def selection_digest(selection: dict) -> str:
    """Mutation-detecting digest over the canonical selection core."""
    payload = json.dumps(selection_core(selection), sort_keys=True,
                         separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def freeze_record(selection: dict, client_version=None,
                  frozen_at: str | None = None) -> dict:
    """The immutable provenance record frozen BEFORE first inference."""
    import time
    record = dict(selection_core(selection))
    record["client_version"] = client_version
    record["frozen_at"] = frozen_at or time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    record["selection_digest"] = selection_digest(selection)
    return record


def verify_frozen(record) -> dict:
    """Verify a frozen record (shape + digest + concrete supported values).

    Returns the selection core on success; raises ModelSelectionError on any
    tampering, drift or non-concrete value. A forged-but-self-consistent
    record is caught by the run's checksum ledger over state.json (same
    residual posture as the environment binding digest)."""
    if not isinstance(record, dict):
        raise ModelSelectionError("FROZEN_RECORD_INVALID", "not an object")
    missing = [k for k in _SELECTION_CORE_FIELDS + ("frozen_at",
                                                     "selection_digest")
               if k not in record]
    if missing:
        raise ModelSelectionError("FROZEN_RECORD_INVALID",
                                  "missing fields %s" % missing)
    recomputed = selection_digest(record)
    if record.get("selection_digest") != recomputed:
        raise ModelSelectionError(
            "FROZEN_RECORD_TAMPERED",
            "selection digest mismatch (recorded %r, recomputed %r)"
            % (record.get("selection_digest"), recomputed))
    if record["auditor"] not in AUDITORS:
        raise ModelSelectionError("FROZEN_RECORD_INVALID",
                                  "auditor %r" % record["auditor"])
    if record["mode"] not in MODES:
        raise ModelSelectionError("FROZEN_RECORD_INVALID",
                                  "mode %r" % record["mode"])
    _check_concrete(record["auditor"], "model", record["model"])
    _check_concrete(record["auditor"], "effort", record["effort"])
    return {k: record[k] for k in _SELECTION_CORE_FIELDS}


def frozen_selection(state: dict, auditor: str) -> dict | None:
    """The run-frozen selection record for `auditor`, or None."""
    block = (state or {}).get("model_selection")
    if not isinstance(block, dict):
        return None
    record = block.get(auditor)
    return record if isinstance(record, dict) else None


# ---------------------------------------------------------------------------
# Claude ambient-conflict gate (readiness blocker ZP-B2 routing)
# ---------------------------------------------------------------------------

def claude_ambient_conflicts(model: str, effort: str,
                             environ=None) -> list[str]:
    """Names of ambient Claude selection env vars that could silently
    override the resolved selection. Empty list = consistent.

    Exact-equality only: unset-or-equal passes; any other value (alias,
    other generation, redirect) is a conflict and the caller must FAIL
    CLOSED before inference. Values are compared but NEVER returned."""
    env = os.environ if environ is None else environ
    conflicts = []
    for var in CLAUDE_MODEL_ENV_VARS:
        value = env.get(var)
        if value is not None and value != model:
            conflicts.append(var)
    for var in CLAUDE_EFFORT_ENV_VARS:
        value = env.get(var)
        if value is not None and value != effort:
            conflicts.append(var)
    return conflicts


# ---------------------------------------------------------------------------
# Claude effective-effort gate (AUCDEV024-CR-IMPL-002)
# ---------------------------------------------------------------------------

# The per-turn EFFECTIVE Claude effort surface established for the installed
# client (Claude Code 2.1.281) by the AUCDEV-024 zero-provider readiness
# probe (gate CLAUDE-07): CLAUDE_EFFORT is "the active effort level for the
# current turn ... after any silent downgrade for the selected model",
# exposed to hook commands and Bash. It is the ONLY mechanically honored
# effective-effort evidence — requested CLI values, SKILL frontmatter, the
# frozen state itself and provider defaults are never accepted (using any
# of those would FAKE the observation, not make it).
CLAUDE_EFFECTIVE_EFFORT_ENV = "CLAUDE_EFFORT"


def claude_effective_effort(environ=None) -> str | None:
    """The observable effective effort token (normalized); None if the
    surface is absent/blank (unobservable). Values are never logged."""
    env = os.environ if environ is None else environ
    value = env.get(CLAUDE_EFFECTIVE_EFFORT_ENV)
    if value is None:
        return None
    value = value.strip().lower()
    return value or None


def claude_effective_effort_violation(effort: str,
                                      environ=None) -> str | None:
    """CR-IMPL-002 gate: None when the observable effective effort equals
    `effort`; otherwise a stable reason token.

    "EFFECTIVE_EFFORT_UNOBSERVABLE" — the surface is absent, so nothing
        mechanically establishes the effective effort (fail closed).
    "EFFECTIVE_EFFORT_MISMATCH"    — the session observably runs at a
        different effort (silent downgrade/clamp); never accepted and
        never silently downgraded to.
    The observed value is compared but NEVER returned (names-only policy,
    same as the ambient-conflict gate)."""
    effective = claude_effective_effort(environ)
    if effective is None:
        return "EFFECTIVE_EFFORT_UNOBSERVABLE"
    if effective != effort.strip().lower():
        return "EFFECTIVE_EFFORT_MISMATCH"
    return None
