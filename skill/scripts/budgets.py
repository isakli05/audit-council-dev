#!/usr/bin/env python3
"""Budget Governor 2.0 (v2 pillar E).

Configurable budgets with v1-compatible defaults, plus EXPLICIT recording of
every budget-driven omission. The governor may decline optional work
(specialists, dynamic probes, adjudication that cannot affect the verdict)
but may NEVER: skip mandatory independent passes, skip required fresh gates,
hide material disputes, silently downgrade model/reasoning, or promote
PARTIAL to COMPLETE. Attempt-vs-successful-stage semantics are preserved.
"""
from __future__ import annotations

import json
import os
from typing import Any

# Defaults preserve the v1.0.3 governor exactly (successful stages per phase
# <= 1, total <= 3, attempts/phase <= 3, repair/phase <= 1).
DEFAULT_BUDGETS: dict[str, Any] = {
    "max_successful_stages_per_phase": 1,
    "max_total_successful_stages": 3,
    "max_attempts_per_phase": 3,
    "max_repairs_per_phase": 1,
    "specialists_default": 0,
    "specialists_normal_cap": 2,
    "specialists_hard_cap": 3,
    "max_specialist_turns": 2,
    "max_dynamic_probes": 4,
    "cached_evidence_policy": "REUSE_WHEN_VALID",
    "force_fresh_release_gates": True,
}

OMISSIONS_NAME = os.path.join("logs", "budget-omissions.jsonl")


class BudgetExceeded(Exception):
    """Raised when a budget would be exceeded. Never retried silently."""


def load(run_dir: str | None) -> dict[str, Any]:
    """Budgets for a run: manifest['budgets'] override, else defaults.
    None/missing manifest → defaults."""
    if not run_dir:
        return dict(DEFAULT_BUDGETS)
    manifest_path = os.path.join(run_dir, "00-run-manifest.json")
    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, ValueError):
        return dict(DEFAULT_BUDGETS)
    budgets = manifest.get("budgets")
    if not isinstance(budgets, dict):
        return dict(DEFAULT_BUDGETS)
    merged = dict(DEFAULT_BUDGETS)
    merged.update({k: v for k, v in budgets.items() if k in merged})
    return merged


def check(stage: str, budgets: dict[str, Any], state: dict) -> None:
    """Raise BudgetExceeded when `stage` may not start under `budgets`.

    stage ∈ {independent, cross_examination, adjudication, specialist,
    dynamic_probe}. Successful-stage semantics identical to the v1 governor;
    specialists are extra: count comes from state['specialists']['count'] and
    the default budget of 0 means any unactivated specialist is refused.
    """
    if stage == "specialist":
        current = (state.get("specialists") or {}).get("count", 0)
        default = budgets["specialists_default"]
        cap = budgets["specialists_hard_cap"]
        if default == 0 and current == 0:
            raise BudgetExceeded(
                "budget governor: specialists are disabled by default; "
                "activation requires a pre-frozen documented reason "
                "(pillar C) and eval-proven value")
        if current >= cap:
            raise BudgetExceeded(
                "budget governor: specialist hard cap %d reached" % cap)
        if current >= budgets["specialists_normal_cap"]:
            # allowed only with an explicit operator elevation on record
            elevated = (state.get("specialists") or {}).get(
                "operator_elevated", False)
            if not elevated:
                raise BudgetExceeded(
                    "budget governor: specialist normal cap %d reached "
                    "(hard cap %d requires operator elevation)"
                    % (budgets["specialists_normal_cap"], cap))
        return
    if stage == "dynamic_probe":
        used = (state.get("dynamic_probes") or {}).get("count", 0)
        if used >= budgets["max_dynamic_probes"]:
            raise BudgetExceeded(
                "budget governor: dynamic probe budget %d exhausted"
                % budgets["max_dynamic_probes"])
        return

    counts = (state.get("codex") or {}).get("stage_counts", {})
    per = counts.get(stage, 0)
    total = sum(counts.get(k, 0) for k in
                ("independent", "cross_examination", "adjudication"))
    if per >= budgets["max_successful_stages_per_phase"]:
        raise BudgetExceeded(
            "budget governor: stage %s already completed successfully "
            "(max %d successful run(s) per phase; completed stages are "
            "never repeated)" % (stage,
                                 budgets["max_successful_stages_per_phase"]))
    if total >= budgets["max_total_successful_stages"]:
        raise BudgetExceeded(
            "budget governor: total codex stages already used (max %d)"
            % budgets["max_total_successful_stages"])
    attempts = sum(1 for j in (state.get("codex") or {}).get("jobs", [])
                   if j.get("phase") == stage)
    if attempts >= budgets["max_attempts_per_phase"]:
        raise BudgetExceeded(
            "budget governor: stage %s already attempted %d times "
            "(quota/failure retry cap reached)"
            % (stage, budgets["max_attempts_per_phase"]))


def record_omission(run_dir: str, entry: dict[str, Any]) -> None:
    """Append an explicit budget-omission record (source of truth:
    logs/budget-omissions.jsonl; 99-run-metrics.json re-derives from it).
    Every budget-driven omission MUST be recorded — silence is a violation."""
    path = os.path.join(run_dir, OMISSIONS_NAME)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = json.dumps({
        "stage": entry.get("stage"),
        "decision": entry.get("decision"),
        "reason": entry.get("reason"),
        "recorded_at": entry.get("recorded_at"),
    }, sort_keys=True, ensure_ascii=False) + "\n"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())


def load_omissions(run_dir: str) -> list[dict[str, Any]]:
    path = os.path.join(run_dir, OMISSIONS_NAME)
    entries: list[dict[str, Any]] = []
    if not os.path.isfile(path):
        return entries
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except ValueError:
                continue
    return entries
