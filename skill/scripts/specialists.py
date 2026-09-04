#!/usr/bin/env python3
"""Eval-gated domain specialists (audit-council v2, pillar C) — DEFAULT OFF.

Additive plumbing only, per AUDIT-COUNCIL-V2-ARCHITECTURE §3.4.7: a static
domain registry, pre-frozen activation gating, blind context construction,
an output schema (../schemas/specialist-review.schema.json) and budget
integration. While specialist counts are 0 this module changes no behavior:
nothing in the v2 lifecycle imports it yet, it never invokes a model, and it
is deterministic (pure functions over caller-supplied state).

Design decisions (mechanical, fail-closed):
  - Activation law: a specialist may run only when its reason was frozen in
    state BEFORE first-pass completion (strict ISO string ordering — equal
    is NOT before), is grounded in the contract/repo/risk, and never leans
    on "a primary model already found it". Any single rejection fails the
    whole request: SpecialistError carries .rejected / .approved so the
    caller may retry with the legal subset explicitly.
  - Reason grounding is a deliberately mechanical proxy (see
    _GROUNDING_KEYWORDS / _MIN_REASON_LENGTH / _MODEL_FOUND_RE), not a
    semantic judgement: length >= 40 AND a contract-field keyword or a
    "risk:" marker, AND not model-found phrasing. The `contract` argument
    is accepted (and type-checked) for signature stability and future
    deeper grounding; the proxy alone decides today.
  - Caps mirror budgets.check("specialist", ...) semantics using
    budgets.DEFAULT_BUDGETS numbers (imported, never re-implemented). The
    default-off branch of budgets.check is intentionally NOT duplicated
    here: this module's pre-freeze activation law IS the activation path
    that budgets.check's error message demands; budget_turn_check
    re-asserts it at turn time.
  - Blindness: blind_context() is the only context a specialist may see
    pre-verdict, and scrub_findings() strips every primary-model output
    key (findings/late_findings/challenges/verdicts/challenges_summary/
    provenance) recursively from every input before the context is built.
"""
from __future__ import annotations

import re
from typing import Any

import budgets

__all__ = [
    "DOMAINS",
    "SpecialistError",
    "registry",
    "activation_gate",
    "start_gate",
    "blind_context",
    "scrub_findings",
    "budget_turn_check",
]

# The nine eval-gated domains (ARCHITECTURE §3.4.7 — order is normative).
DOMAINS = [
    "security-trust",
    "concurrency-state",
    "authorization-multitenancy",
    "data-integrity-migrations",
    "api-contracts",
    "release-supply-chain",
    "test-eval-quality",
    "performance-resources",
    "frontend-accessibility",
]

# One-line charter per domain (what the specialist covers, never what it
# decides — specialists own coverage and candidates, never verdicts).
_CHARTERS = {
    "security-trust":
        "Authentication, session handling, secrets, trust boundaries, and "
        "injection or sanitizer-escape vectors.",
    "concurrency-state":
        "Race conditions, atomicity, ordering, deadlock, and stale-state "
        "recovery under concurrency.",
    "authorization-multitenancy":
        "Access-control enforcement, tenant isolation, privilege "
        "boundaries, and cross-tenant data exposure.",
    "data-integrity-migrations":
        "Schema and data migrations, backfills, transactional integrity, "
        "and destructive-change safety.",
    "api-contracts":
        "Drift between declared API contracts, implementation, and "
        "consumers; validation and compatibility discipline.",
    "release-supply-chain":
        "Build, packaging, release integrity, dependency provenance, and "
        "supply-chain attack surface.",
    "test-eval-quality":
        "Whether tests and evals actually assert the requirement: coverage "
        "honesty, fixture validity, false assurance.",
    "performance-resources":
        "Resource exhaustion, unbounded work, latency cliffs, and "
        "degradation under load.",
    "frontend-accessibility":
        "Frontend correctness, rendering and interaction states, and "
        "accessibility conformance within product scope.",
}

# Primary-model output keys that must never leak into specialist context.
SCRUB_KEYS = frozenset({
    "findings",
    "late_findings",
    "challenges",
    "verdicts",
    "challenges_summary",
    "provenance",
})

# Reason-grounding proxy (§3.4.7: based on contract/repo/risk — never "a
# primary model already revealed the bug").
_MIN_REASON_LENGTH = 40
_GROUNDING_KEYWORDS = (
    "scope",
    "objective",
    "exclusion",
    "authoritative_source",
    "authoritative source",
    "risk:",
)
_MODEL_FOUND_RE = re.compile(
    r"(opus|codex|model|auditor)\s+(already\s+)?(found|revealed|report)",
    re.IGNORECASE)


class SpecialistError(Exception):
    """Raised on specialist-contract violations (unknown domain, missing or
    non-pre-frozen activation reason, ungrounded reason, cap violations,
    blindness violations). Carries .rejected (domains refused, with causes
    folded into the message) and .approved (the would-be-legal subset) so a
    caller can retry explicitly with the legal part — never silently."""

    def __init__(self, message: str, *, rejected: list[str] | None = None,
                 approved: list[str] | None = None):
        super().__init__(message)
        self.rejected: list[str] = list(rejected or [])
        self.approved: list[str] = list(approved or [])


def registry() -> list[dict[str, Any]]:
    """Static domain registry: every domain is default_off and eval_gated.
    Pure data, no environment reads — the eval suite (pillar D) is the only
    thing that may ever flip these postures, and it does so by producing
    measured evidence, not by editing this list."""
    return [
        {"domain": domain,
         "charter": _CHARTERS[domain],
         "default_off": True,
         "eval_gated": True}
        for domain in DOMAINS
    ]


def _entry_cause(entry: dict[str, Any],
                 first_pass_complete_at: str | None) -> str | None:
    """Why this activation entry is illegal, or None when it is legal.
    Check order matters: model-found phrasing is rejected regardless of
    timing, pre-freeze ordering next, grounding proxy last."""
    reason = entry.get("reason")
    recorded_at = entry.get("recorded_at")
    if not isinstance(reason, str) or not isinstance(recorded_at, str):
        return "malformed activation entry (reason/recorded_at must be strings)"
    if _MODEL_FOUND_RE.search(reason):
        return ("reason references a primary model's findings — activation "
                "must be grounded in contract/repo/risk, never in what a "
                "model already found")
    if first_pass_complete_at is not None \
            and not recorded_at < first_pass_complete_at:
        return ("activation reason not pre-frozen: recorded_at %s is not "
                "strictly before first-pass completion %s"
                % (recorded_at, first_pass_complete_at))
    if len(reason) < _MIN_REASON_LENGTH:
        return ("reason too short/generic (min %d chars): activation "
                "reasons must be documented, not boilerplate"
                % _MIN_REASON_LENGTH)
    if not any(keyword in reason.lower() for keyword in _GROUNDING_KEYWORDS):
        return ("reason not grounded in the contract (scope/objective/"
                "exclusions/authoritative_sources) or a recorded risk:")
    return None


def _ordered_unique(items: list[Any]) -> list[Any]:
    seen: set[Any] = set()
    out: list[Any] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def activation_gate(state: dict[str, Any], contract: dict[str, Any],
                    requested: list[str],
                    first_pass_complete_at: str | None) -> list[str]:
    """Return the APPROVED subset of `requested`; raise SpecialistError on
    ANY violation (fail-closed: nothing runs on a violation).

    Rules (all mechanical, §3.4.7 + budgets):
      1. every requested domain must be a registered domain;
      2. each must have a pre-frozen {domain, reason, recorded_at} entry in
         state["specialists"]["activation"] recorded STRICTLY before
         first_pass_complete_at (ISO string compare; equal is not before);
         when first_pass_complete_at is None (barrier not yet reached) any
         recording time is legal — that is the pre-freezing window;
      3. the reason must be grounded (see _entry_cause) and must never
         reference a primary model having already found something;
      4. caps from budgets.DEFAULT_BUDGETS: at most specialists_hard_cap
         domains, and more than specialists_normal_cap only when
         state["specialists"]["operator_elevated"] is true (mirrors
         budgets.check("specialist", ...) semantics on its numbers).
    """
    if not isinstance(state, dict):
        raise SpecialistError("activation_gate: state must be an object")
    if not isinstance(contract, dict):
        raise SpecialistError("activation_gate: contract must be an object")
    if not isinstance(requested, list):
        raise SpecialistError("activation_gate: requested must be a list "
                              "of domain strings")

    specialists_state = state.get("specialists") or {}
    if not isinstance(specialists_state, dict):
        raise SpecialistError(
            "activation_gate: state['specialists'] must be an object")
    raw_entries = specialists_state.get("activation") or []
    if not isinstance(raw_entries, list):
        raise SpecialistError(
            "activation_gate: state['specialists']['activation'] must be "
            "a list")

    approved: list[str] = []
    causes: list[tuple[str, str]] = []
    for domain in _ordered_unique(requested):
        if not isinstance(domain, str) or domain not in DOMAINS:
            causes.append((str(domain), "unknown specialist domain"))
            continue
        entries = [e for e in raw_entries
                   if isinstance(e, dict) and e.get("domain") == domain]
        if not entries:
            causes.append((domain,
                           "no pre-frozen activation reason on record"))
            continue
        first_cause: str | None = None
        legal = False
        for entry in entries:
            cause = _entry_cause(entry, first_pass_complete_at)
            if cause is None:
                legal = True
                break
            if first_cause is None:
                first_cause = cause
        if legal:
            approved.append(domain)
        else:
            assert first_cause is not None
            causes.append((domain, first_cause))

    hard_cap = budgets.DEFAULT_BUDGETS["specialists_hard_cap"]
    normal_cap = budgets.DEFAULT_BUDGETS["specialists_normal_cap"]
    elevated = bool(specialists_state.get("operator_elevated"))
    cap_violation: str | None = None
    if len(approved) > hard_cap:
        cap_violation = (
            "specialist hard cap %d exceeded by %d valid domains — the "
            "hard cap is absolute; operator elevation only lifts the "
            "normal cap" % (hard_cap, len(approved)))
    elif len(approved) > normal_cap and not elevated:
        cap_violation = (
            "specialist normal cap %d exceeded by %d valid domains without "
            "operator_elevated=true (hard cap %d requires elevation)"
            % (normal_cap, len(approved), hard_cap))

    if causes or cap_violation is not None:
        parts = ["%s: %s" % (domain, cause) for domain, cause in causes]
        if cap_violation is not None:
            parts.append(cap_violation)
        raise SpecialistError(
            "specialist activation refused: " + "; ".join(parts),
            rejected=[domain for domain, _ in causes],
            approved=list(approved))
    return approved


def start_gate(barrier_open: bool) -> None:
    """The run may only START specialists after the first-pass independence
    barrier is open. Pre-freezing an activation reason before the barrier is
    fine (that is rule 2 of activation_gate); starting work is not."""
    if not barrier_open:
        raise SpecialistError(
            "specialists run only after the independence barrier")


def scrub_findings(obj: Any) -> Any:
    """Recursively drop every primary-model output key (SCRUB_KEYS) from
    dicts, recursing through remaining values and lists. Returns a new
    structure; the input is never mutated."""
    if isinstance(obj, dict):
        return {key: scrub_findings(value)
                for key, value in obj.items() if key not in SCRUB_KEYS}
    if isinstance(obj, list):
        return [scrub_findings(item) for item in obj]
    return obj


def _assert_blind(node: Any, path: str = "$") -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in SCRUB_KEYS:
                raise SpecialistError(
                    "blindness violation: primary-model output key %r "
                    "survived at %s.%s" % (key, path, key))
            _assert_blind(value, "%s.%s" % (path, key))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _assert_blind(item, "%s[%d]" % (path, index))


def blind_context(contract: dict[str, Any], repo_facts: dict[str, Any],
                  domain: str, evidence_refs: list[str]) -> dict[str, Any]:
    """Build the ONLY context a specialist may receive pre-verdict:
    contract (full, scrubbed), repo_facts (neutral inventory, scrubbed),
    the domain charter, and evidence_refs (evidence-store ids). Contains no
    primary-model findings by construction — every input passes
    scrub_findings and the result is re-asserted blind before returning."""
    if not isinstance(domain, str) or domain not in DOMAINS:
        raise SpecialistError(
            "unknown specialist domain %r (registry: %s)"
            % (domain, ", ".join(DOMAINS)))
    if not isinstance(evidence_refs, list):
        raise SpecialistError("evidence_refs must be a list of ev- ids")
    for ref in evidence_refs:
        if not isinstance(ref, str) or not ref.startswith("ev-"):
            raise SpecialistError(
                "evidence ref %r is not an evidence-store id "
                "(must be ev-prefixed)" % (ref,))

    context = {
        "domain": domain,
        "domain_charter": _CHARTERS[domain],
        "contract": scrub_findings(contract),
        "repo_facts": scrub_findings(repo_facts),
        "evidence_refs": list(evidence_refs),
    }
    _assert_blind(context)
    return context


def budget_turn_check(state: dict[str, Any], turns_used: int) -> None:
    """Raise budgets.BudgetExceeded when specialist turn accounting is
    illegal: turn count must stay under DEFAULT_BUDGETS
    ["max_specialist_turns"], and with specialists_default==0 an
    UNACTIVATED specialist turn is always refused (there must be a
    non-empty state["specialists"]["activation"] on record)."""
    if not isinstance(state, dict):
        raise SpecialistError("budget_turn_check: state must be an object")
    if isinstance(turns_used, bool) or not isinstance(turns_used, int):
        raise TypeError("turns_used must be an int")

    specialists_state = state.get("specialists") or {}
    activation = (specialists_state.get("activation")
                  if isinstance(specialists_state, dict) else None) or []
    if budgets.DEFAULT_BUDGETS["specialists_default"] == 0 and not activation:
        raise budgets.BudgetExceeded(
            "budget governor: specialist turn refused — no activated "
            "specialist on record (specialists_default=0; activation "
            "requires a pre-frozen documented reason, pillar C)")
    if turns_used >= budgets.DEFAULT_BUDGETS["max_specialist_turns"]:
        raise budgets.BudgetExceeded(
            "budget governor: max_specialist_turns %d exhausted"
            % budgets.DEFAULT_BUDGETS["max_specialist_turns"])
