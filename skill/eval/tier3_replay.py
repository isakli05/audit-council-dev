#!/usr/bin/env python3
"""Tier-3 historical replay (pillar D, Task D.2) — approval-gated.

Replays harness decisions against the preserved raw outputs of the two
frozen historical runs (Benchmark 001, Fifth), READ-ONLY: state.json,
99-run-metrics.json and logs/jobs/*.json are parsed, classifications are
re-derived with wire_adapter + evidence_migration + validate_artifact
(imported from skill/scripts via sys.path), and PROCESS / HARNESS /
ECONOMICS / DIVERSITY are scored from the recorded artifacts.

Hard invariants:
  * REFUSES without an explicit operator approval record — on refusal the
    module performs ZERO reads of the run dir (not even an existence stat).
  * NEVER invokes codex/claude (no model calls, no subprocesses).
  * NEVER writes anywhere, and in particular never inside the historical
    run directories; the scorecard exists only as the returned dict /
    whatever the caller prints.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import pathlib
import sys
from typing import Any

if __package__ in (None, "") or __package__ == "eval":  # direct execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.realpath(__file__))))
    from eval import scoring
else:  # pragma: no cover - alternate import spelling
    from . import scoring

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_SCRIPTS_DIR = os.path.join(_SKILL_DIR, "scripts")
_SCHEMAS_DIR = os.path.join(_SKILL_DIR, "schemas")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import wire_adapter  # noqa: E402
import evidence_migration  # noqa: E402
from validate_artifact import validate  # noqa: E402

GATE_TEXT = "historical replay requires explicit operator approval"

TIER3_SEEDS: dict[str, dict[str, str]] = {
    "benchmark-001": {
        "run_dir": ("/home/isa/benchmarks/lco-audit-council-001/target/"
                    "audit-output/audit-council/20260904T014146Z-f3384a"),
        "target_head": "0a5cee799f1c6ee0027183a8b36121e6f02d3156",
    },
    "fifth": {
        "run_dir": ("/home/isa/audits/lco-fifth-independent-release-audit/"
                    "target/audit-output/audit-council/"
                    "20260904T081903Z-60651d"),
        "target_head": "f8c2b2c6955d19df7902cf2efc140ba558af044e",
    },
}

# canonical schema per codex phase (mirrors codex_runner.PHASE_CANON_SCHEMA)
_PHASE_CANON_SCHEMA = {
    "independent": "independent-audit.schema.json",
    "cross_examination": "cross-examination.schema.json",
    "adjudication": "adjudication.schema.json",
}

_APPROVAL_KEYS = ("operator_approval", "approver", "approved_at")


def _iso_ok(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        _dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def approval_is_valid(approval: Any) -> bool:
    """Approval must carry operator_approval True, a non-empty approver
    and a parseable ISO-8601 approved_at."""
    if not isinstance(approval, dict):
        return False
    if any(k not in approval for k in _APPROVAL_KEYS):
        return False
    if approval.get("operator_approval") is not True:
        return False
    approver = approval.get("approver")
    if not isinstance(approver, str) or not approver.strip():
        return False
    return _iso_ok(approval.get("approved_at"))


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _strip_legacy_null_lines(node: Any) -> Any:
    """Drop `lines: None` keys left behind by the v1 wire format (a null
    optional line citation). String `lines` values are kept for
    evidence_migration; this shim never weakens a non-null value."""
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            if key == "lines" and value is None:
                continue
            out[key] = _strip_legacy_null_lines(value)
        return out
    if isinstance(node, list):
        return [_strip_legacy_null_lines(item) for item in node]
    return node


def rederive_classification(job: dict, frozen_fingerprint: str | None
                            ) -> dict[str, Any]:
    """Re-derive a historical job's artifact classification from its
    preserved raw output, using the CURRENT harness decision chain:
    wire_to_canonical -> v1->v2 migration -> canonical validation ->
    repository-fingerprint invariant. Pure computation, read-only."""
    phase = job.get("phase")
    out_path = job.get("output_path")
    recorded = job.get("artifact_status") or "UNKNOWN"
    derived = "NOT_RUN"
    reason = None
    if phase not in _PHASE_CANON_SCHEMA:
        return {"recorded": recorded, "derived": "UNSUPPORTED_PHASE",
                "matches": False}
    if not out_path or not os.path.isfile(out_path):
        derived, reason = "NOT_PRODUCED", "raw output file absent"
    else:
        try:
            raw = _read_json(out_path)
            derived = "WIRE_VALID"
        except (OSError, ValueError) as exc:
            derived, reason = "WIRE_INVALID", str(exc)[:200]
            raw = None
        if raw is not None:
            schema_path = os.path.join(_SCHEMAS_DIR,
                                       _PHASE_CANON_SCHEMA[phase])
            schema = _read_json(schema_path)
            try:
                candidate, _errs = wire_adapter.wire_to_canonical(
                    raw, schema, _SCHEMAS_DIR)
                candidate = _strip_legacy_null_lines(candidate)
                if evidence_migration.is_v1_artifact(candidate):
                    candidate = evidence_migration.migrate_artifact(candidate)
                errors = validate(candidate, schema,
                                  base_dir=pathlib.Path(_SCHEMAS_DIR))
            except evidence_migration.MigrationError as exc:
                errors = [str(exc)]
            except Exception as exc:  # fail closed, never crash replay
                errors = ["rederivation error: %s" % exc]
            if errors:
                derived, reason = "SCHEMA_INVALID", errors[0][:200]
            else:
                claimed = candidate.get("repository_fingerprint_sha256") \
                    if isinstance(candidate, dict) else None
                if (claimed is not None and frozen_fingerprint is not None
                        and claimed != frozen_fingerprint):
                    derived, reason = "FINGERPRINT_MISMATCH", \
                        "claimed fingerprint differs from frozen run"
                else:
                    derived = "CANONICAL_VALID"
    return {"recorded": recorded, "derived": derived,
            "matches": derived == recorded, "reason": reason}


def _fraction(checks: dict[str, bool]) -> tuple[float, list[str]]:
    if not checks:
        return 0.0, []
    passing = sum(1 for v in checks.values() if v)
    failing = sorted(k for k, v in checks.items() if not v)
    return passing / len(checks), failing


def _economics(state: dict, metrics: dict, jobs: list[dict]
               ) -> dict[str, Any]:
    invocations = metrics.get("invocations") or []
    agg = metrics.get("aggregates") or {}
    agg_tokens = agg.get("tokens")
    # recompute token totals from the per-job records (never from the
    # aggregate alone); unknown usage stays unknown, never fabricated 0
    totals = {"input_tokens": 0, "cached_input_tokens": 0,
              "output_tokens": 0, "reasoning_output_tokens": 0}
    known = {"input_tokens": 0, "cached_input_tokens": 0,
             "output_tokens": 0, "reasoning_output_tokens": 0}
    for job in jobs:
        toks = job.get("tokens")
        if not isinstance(toks, dict):
            continue
        for key in totals:
            value = toks.get(key)
            if isinstance(value, (int, float)):
                totals[key] += value
                known[key] += 1
    usage_unknown = sum(1 for job in jobs
                        if not isinstance(job.get("tokens"), dict))
    checks: dict[str, bool] = {}
    if isinstance(agg_tokens, dict):
        checks["aggregates_match_job_records"] = all(
            agg_tokens.get(k) == totals[k] for k in totals)
    elapsed_jobs = [j.get("elapsed_sec") for j in invocations
                    + jobs
                    if isinstance(j.get("elapsed_sec"), (int, float))]
    wall = None
    stamps = state.get("timestamps") or {}
    try:
        wall = (_dt.datetime.fromisoformat(stamps["COMPLETE"].replace("Z", "+00:00"))
                - _dt.datetime.fromisoformat(stamps["CREATED"].replace("Z", "+00:00"))
                ).total_seconds()
    except (KeyError, ValueError, TypeError):
        pass
    checks["invocation_count_consistent"] = (
        agg.get("invocation_count") in (len(invocations), len(jobs)))
    score, failing = _fraction(checks)
    return {
        "status": "scored", "score": score,
        "details": {
            "tokens": agg_tokens if isinstance(agg_tokens, dict) else {
                k: (v if known[k] else None) for k, v in totals.items()},
            "recomputed_from_jobs": dict(totals),
            "usage_unknown_count": usage_unknown,
            "elapsed_sec_total": (
                agg.get("elapsed_sec_total")
                if isinstance(agg.get("elapsed_sec_total"), (int, float))
                else (sum(elapsed_jobs) if elapsed_jobs else None)),
            "wall_clock_sec": wall,
            "invocation_count": agg.get("invocation_count",
                                        len(invocations) or len(jobs)),
            "successful_stage_counted_total":
                agg.get("successful_stage_counted_total"),
            "failing_checks": failing,
        },
    }


def _process(run_dir: str, state: dict, jobs: list[dict]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    checks["opus_independent_artifact"] = os.path.isfile(
        os.path.join(run_dir, "10-opus-independent.json"))
    checks["codex_independent_artifact"] = os.path.isfile(
        os.path.join(run_dir, "20-codex-independent.json"))
    codex_ind_raw = any(j.get("phase") == "independent"
                        and j.get("raw_output_preserved") is not False
                        and os.path.isfile(str(j.get("output_path") or ""))
                        for j in jobs)
    checks["codex_independent_raw_or_artifact"] = (
        checks["codex_independent_artifact"] or codex_ind_raw)
    checks["normalization_artifact"] = os.path.isfile(
        os.path.join(run_dir, "30-normalized-findings.json"))
    checks["cross_examination_explicit"] = (
        os.path.isfile(os.path.join(run_dir, "31-opus-cross-examination.json"))
        or os.path.isfile(
            os.path.join(run_dir, "32-codex-cross-examination.json")))
    # a missing codex cross-exam must be EXPLICIT: failure_reason recorded
    # AND the raw invalid output preserved
    has_31 = os.path.isfile(os.path.join(run_dir,
                                         "31-opus-cross-examination.json"))
    codex_xam_raw = [j for j in jobs
                     if j.get("phase") == "cross_examination"]
    explicit_partial = (
        has_31
        or (bool(state.get("failure_reason"))
            and all(os.path.isfile(str(j.get("output_path") or ""))
                    for j in codex_xam_raw)))
    checks["cross_examination_or_explicit_partial"] = explicit_partial
    checks["disagreement_ledger"] = os.path.isfile(
        os.path.join(run_dir, "40-disagreement-ledger.json"))
    checks["adjudication"] = os.path.isfile(
        os.path.join(run_dir, "50-targeted-adjudication.json"))
    checks["final_findings"] = os.path.isfile(
        os.path.join(run_dir, "90-final-findings.json"))
    # first-pass independence: normalization strictly after BOTH first
    # passes completed
    stamps = state.get("timestamps") or {}
    try:
        opus_done = _dt.datetime.fromisoformat(
            stamps["OPUS_INDEPENDENT_COMPLETE"].replace("Z", "+00:00"))
        norm = _dt.datetime.fromisoformat(
            stamps["NORMALIZED"].replace("Z", "+00:00"))
        checks["first_pass_independence"] = norm >= opus_done
    except (KeyError, ValueError, TypeError):
        checks["first_pass_independence"] = False
    score, failing = _fraction(checks)
    return {"status": "scored", "score": score,
            "details": {"checks": checks, "failing_checks": failing}}


def _harness(state: dict, metrics: dict, jobs: list[dict],
             rederived: list[dict]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    checks["classifications_reproduce"] = all(r["matches"] for r in rederived)
    stage_counts = ((state.get("codex") or {}).get("stage_counts")) or {}
    counted = sum(v for v in stage_counts.values()
                  if isinstance(v, (int, float)))
    agg = metrics.get("aggregates") or {}
    successful_total = agg.get("successful_stage_counted_total")
    checks["stage_counts_consistent"] = (
        successful_total in (counted, None) if successful_total is not None
        else True)
    checks["attempts_accounted"] = agg.get("invocation_count") in (
        len(jobs), None)
    checks["completeness_state_recorded"] = bool(
        state.get("completeness_state"))
    checks["metrics_note_recorded"] = bool(metrics.get("note"))
    score, failing = _fraction(checks)
    return {"status": "scored", "score": score,
            "details": {"checks": checks, "failing_checks": failing,
                        "rederived_classifications": rederived}}


def _diversity(run_dir: str) -> dict[str, Any]:
    path = os.path.join(run_dir, "90-final-findings.json")
    counts = {"consensus": 0, "opus_only": 0, "codex_only": 0,
              "unattributed": 0}
    final_status: dict[str, int] = {}
    rejected = 0
    total = 0
    if os.path.isfile(path):
        final = _read_json(path)
        rejected = len(final.get("rejected_appendix") or [])
        for finding in final.get("findings") or []:
            total += 1
            status = str(finding.get("final_status"))
            final_status[status] = final_status.get(status, 0) + 1
            origins = [str(o).split("-")[0] for o in
                       ((finding.get("provenance") or {}).get("origin")
                        or [])]
            families = {("OPUS" if o.startswith("OPUS") else
                         "CODEX" if o.startswith("CODEX") else o)
                        for o in origins}
            if len(families) >= 2:
                counts["consensus"] += 1
            elif families == {"OPUS"}:
                counts["opus_only"] += 1
            elif families == {"CODEX"}:
                counts["codex_only"] += 1
            else:
                counts["unattributed"] += 1
    checks = {
        "final_findings_present": total > 0,
        "per_finding_attribution": counts["unattributed"] == 0,
    }
    score, failing = _fraction(checks)
    return {"status": "scored", "score": score,
            "details": {"finding_count": total,
                        "attribution": counts,
                        "final_status": final_status,
                        "rejected_appendix": rejected,
                        "failing_checks": failing}}


def replay(seed: str, approval: dict) -> dict[str, Any]:
    """Approval-gated, READ-ONLY historical replay.

    Refuses (zero filesystem access to the run dir) unless approval is
    {"operator_approval": True, "approver": <nonempty str>,
    "approved_at": <ISO-8601 str>}. With a valid approval the historical
    run dir is read strictly read-only and a tier-3 scorecard is returned.
    """
    if seed not in TIER3_SEEDS:
        return {"status": "refused", "seed": seed,
                "gate": "unknown tier3 seed: %r" % (seed,)}
    if not approval_is_valid(approval):
        return {"status": "refused", "seed": seed, "gate": GATE_TEXT}

    run_dir = TIER3_SEEDS[seed]["run_dir"]
    if not os.path.isdir(run_dir):
        return {"status": "error", "seed": seed,
                "error": "historical run dir not found: %s" % run_dir}

    state = _read_json(os.path.join(run_dir, "state.json"))
    metrics = _read_json(os.path.join(run_dir, "99-run-metrics.json"))
    jobs_dir = os.path.join(run_dir, "logs", "jobs")
    jobs = []
    if os.path.isdir(jobs_dir):
        for name in sorted(os.listdir(jobs_dir)):
            if name.endswith(".json"):
                jobs.append(_read_json(os.path.join(jobs_dir, name)))

    repo_state_path = os.path.join(run_dir, "01-repository-state.json")
    head_ok = None
    if os.path.isfile(repo_state_path):
        recorded_head = ((_read_json(repo_state_path)
                          .get("fingerprint") or {}).get("head_sha"))
        head_ok = recorded_head == TIER3_SEEDS[seed]["target_head"]

    frozen_fp = state.get("repo_fingerprint_sha256")
    rederived = [rederive_classification(job, frozen_fp) for job in jobs]

    dimensions = {
        "FINAL_QUALITY": dict(scoring.NOT_RUN),
        "PROCESS": _process(run_dir, state, jobs),
        "HARNESS": _harness(state, metrics, jobs, rederived),
        "ECONOMICS": _economics(state, metrics, jobs),
        "DIVERSITY": _diversity(run_dir),
        "ENVIRONMENT": {"status": "not-run",
                        "details": {"note": "v1 historical runs predate the "
                                    "A0 environment matrix; no environment "
                                    "observations exist to score"}},
    }
    return {
        "schema_version": 2,
        "tier": 3,
        "status": "replayed",
        "seed": seed,
        "run_dir": run_dir,
        "target_head": TIER3_SEEDS[seed]["target_head"],
        "target_head_matches_recorded": head_ok,
        "approval": {"approver": approval["approver"],
                     "approved_at": approval["approved_at"]},
        "job_count": len(jobs),
        "completeness_state": state.get("completeness_state"),
        "dimensions": {d: dimensions[d] for d in scoring.DIMENSIONS},
        # environment integrity is a hard gate: with no environment
        # observations a historical replay can never assert READY by itself
        "environment_integrity_pass": False,
        "overall": "NOT_READY",
        "read_only": True,
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] != "tier3" or len(argv) < 2:
        print("usage: tier3_replay.py tier3 <seed> "
              "[--i-have-operator-approval --approver NAME "
              "--approved-at ISO]", file=sys.stderr)
        return 2
    seed = argv[1]
    approved = "--i-have-operator-approval" in argv

    def _flag(name: str) -> str | None:
        try:
            i = argv.index(name)
            return argv[i + 1]
        except (ValueError, IndexError):
            return None

    approval = ({"operator_approval": True,
                 "approver": _flag("--approver") or "",
                 "approved_at": _flag("--approved-at") or ""}
                if approved else {})
    result = replay(seed, approval)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result.get("status") == "refused":
        print(GATE_TEXT, file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
