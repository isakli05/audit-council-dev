#!/usr/bin/env python3
"""Scoring semantics for the Audit Council eval suite (pillar D).

Dimensions (ARCHITECTURE §3.4.8), reported separately:
  FINAL_QUALITY / PROCESS / HARNESS / ECONOMICS / DIVERSITY / ENVIRONMENT

Tier-1 (deterministic harness eval) scores only HARNESS + ENVIRONMENT; the
later-tier dimensions report {"status": "not-run"} until a tier fills them.
ENVIRONMENT is a HARD requirement: the overall verdict is NOT_READY unless
the environment matrix pass rate is exactly 1.0 AND the harness suite
passed. This module is pure computation — no I/O, no models.
"""
from __future__ import annotations

from typing import Any

DIMENSIONS = ("FINAL_QUALITY", "PROCESS", "HARNESS", "ECONOMICS",
              "DIVERSITY", "ENVIRONMENT")

# Dimensions that only tiers 2-4 fill in.
LATER_TIER_DIMENSIONS = ("FINAL_QUALITY", "PROCESS", "ECONOMICS",
                         "DIVERSITY")

NOT_RUN = {"status": "not-run"}

# Novel-finding truth rule (ARCHITECTURE §3.4.8): a claimed novel
# CRITICAL/HIGH finding counts as truth ONLY with at least one of these
# truth evidence flags. Model agreement alone (e.g. {"model_agreement": 2})
# is NEVER truth.
TRUTH_EVIDENCE_KEYS = (
    "deterministic_reproduction",
    "independent_evaluator",
    "human_confirmation",
    "predefined_runtime_evidence",
)


def _scored(score: float, details: dict[str, Any]) -> dict[str, Any]:
    return {"status": "scored", "score": float(score), "details": details}


def environment_fraction(env_matrix_results: dict[str, bool]
                         ) -> tuple[float, list[str]]:
    """Pass fraction of the environment regression matrix.

    An empty/absent matrix is 0.0 (environment integrity is never assumed
    without evidence — fail-closed).
    """
    if not isinstance(env_matrix_results, dict) or not env_matrix_results:
        return 0.0, []
    total = len(env_matrix_results)
    passing = sum(1 for v in env_matrix_results.values() if v)
    failing = sorted(str(k) for k, v in env_matrix_results.items() if not v)
    return passing / total, failing


def score_tier1(env_matrix_results: dict[str, bool],
                harness_suite_passed: bool,
                harness_suite_total: int | None = None) -> dict[str, Any]:
    """Tier-1 scorecard: HARNESS + ENVIRONMENT only; later tiers not-run.

    overall == "READY" iff ENVIRONMENT fraction is exactly 1.0 AND the
    harness suite passed. environment_integrity_pass mirrors the env gate.
    """
    fraction, failing = environment_fraction(env_matrix_results)
    env_pass = fraction == 1.0
    harness_ok = bool(harness_suite_passed)
    dimensions: dict[str, Any] = {d: dict(NOT_RUN) for d in
                                  LATER_TIER_DIMENSIONS}
    dimensions["HARNESS"] = _scored(
        1.0 if harness_ok else 0.0,
        {"suite_passed": harness_ok,
         "tests_run": harness_suite_total,
         "note": "full unittest discovery over skill/tests"})
    dimensions["ENVIRONMENT"] = _scored(
        fraction,
        {"matrix_cases": len(env_matrix_results) if
         isinstance(env_matrix_results, dict) else 0,
         "failing_cases": failing,
         "hard_requirement": "100% pass rate required for READY"})
    return {
        "schema_version": 2,
        "tier": 1,
        "dimensions": {d: dimensions[d] for d in DIMENSIONS},
        "overall": "READY" if (env_pass and harness_ok) else "NOT_READY",
        "environment_integrity_pass": env_pass,
    }


def merge_scores(*scorecards: dict[str, Any]) -> dict[str, Any]:
    """Merge scorecards as later tiers fill in dimensions.

    FINAL_QUALITY/PROCESS/ECONOMICS/DIVERSITY/HARNESS: averaged over every
    scorecard that scored them (not-run leaves stay until some tier runs
    them). ENVIRONMENT stays hard-gated: every ENVIRONMENT observation in
    every scorecard must be exactly 1.0 (and at least one must exist) or
    the merged environment_integrity_pass is False and overall is
    NOT_READY. The merged overall is the conjunction of the environment
    gate and every input scorecard's own overall verdict.
    """
    merged: dict[str, Any] = {d: dict(NOT_RUN) for d in DIMENSIONS}
    env_observations: list[float] = []
    env_failing: list[str] = []
    overall_votes: list[str] = []

    for card in scorecards:
        if not isinstance(card, dict):
            continue
        if card.get("overall") is not None:
            overall_votes.append(str(card["overall"]))
        dims = card.get("dimensions")
        if not isinstance(dims, dict):
            continue
        for dim in LATER_TIER_DIMENSIONS + ("HARNESS",):
            entry = dims.get(dim)
            if (isinstance(entry, dict)
                    and entry.get("status") == "scored"
                    and isinstance(entry.get("score"), (int, float))):
                if merged[dim]["status"] == "not-run":
                    merged[dim] = _scored(
                        float(entry["score"]),
                        {"contributions": [
                            {"score": float(entry["score"]),
                             "details": entry.get("details")}]})
                else:
                    merged[dim]["details"]["contributions"].append(
                        {"score": float(entry["score"]),
                         "details": entry.get("details")})
        env = dims.get("ENVIRONMENT")
        if (isinstance(env, dict)
                and env.get("status") == "scored"
                and isinstance(env.get("score"), (int, float))):
            env_observations.append(float(env["score"]))
            for f in (env.get("details") or {}).get("failing_cases") or []:
                env_failing.append(str(f))

    for dim in LATER_TIER_DIMENSIONS + ("HARNESS",):
        if merged[dim]["status"] == "scored":
            contributions = merged[dim]["details"]["contributions"]
            merged[dim]["score"] = (
                sum(c["score"] for c in contributions) / len(contributions))

    env_pass = bool(env_observations) and all(o == 1.0 for o in
                                              env_observations)
    merged["ENVIRONMENT"] = _scored(
        (sum(env_observations) / len(env_observations))
        if env_observations else 0.0,
        {"observations": env_observations,
         "failing_cases": sorted(set(env_failing)),
         "hard_requirement": "every observation must be exactly 1.0"})
    others_ready = all(v == "READY" for v in overall_votes)
    return {
        "schema_version": 2,
        "dimensions": {d: merged[d] for d in DIMENSIONS},
        "overall": "READY" if (env_pass and others_ready) else "NOT_READY",
        "environment_integrity_pass": env_pass,
    }


def novel_finding_is_truth(claimed_new_critical_or_high: bool,
                           evidence: dict[str, Any]) -> bool:
    """Enforce the novel-finding truth rule.

    True ONLY when a novel CRITICAL/HIGH finding is claimed AND the
    evidence carries at least one truth flag (deterministic_reproduction,
    independent_evaluator, human_confirmation,
    predefined_runtime_evidence) that is literally True. Model agreement
    alone — any other key such as {"model_agreement": 2} — is NEVER truth.
    An unclaimed finding is not a truth claim, so it returns False.
    """
    if not claimed_new_critical_or_high:
        return False
    if not isinstance(evidence, dict):
        return False
    return any(evidence.get(key) is True for key in TRUTH_EVIDENCE_KEYS)
