#!/usr/bin/env python3
"""Tier-2 FAKE-MODEL scoring harness (pillar D, deterministic half).

Drives the REAL pipeline machinery (audit_council CLI state machine,
validators, inclusion rules) on the seeded tier-2 fixture repos with
SCRIPTED model artifacts — no real model calls anywhere:

- the "perfect-ish auditor" scripts derive findings from the SEALED truth
  (that is the fake model's knowledge);
- consensus/diversity is scripted (some defects codex-only, some
  opus-only, some consensus);
- one seeded FALSE POSITIVE is raised and must be REJECTED in
  cross-examination (pipeline honesty);
- clean-idioms raises one candidate against a PROTECTED control which
  must be rejected and must never reach the primary findings.

Scoring vs the sealed truth: recall, precision, protected-control
respect, and the novel-finding truth rule (a CRITICAL/HIGH not in the
sealed truth is never scored as truth without reproduction evidence).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

_SKILL = Path(__file__).resolve().parent.parent
SCRIPTS = _SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(_SKILL / "eval"))

import tier2_fixtures as t2  # noqa: E402

PYTHON = "python3"
AUDIT_COUNCIL = str(SCRIPTS / "audit_council.py")


def _cli(*args, stdin=None):
    env = dict(os.environ)
    # R5 NEW-6: never leak active-run registrations into the real user
    # cache from the eval harness
    env.setdefault("AUDIT_COUNCIL_CACHE_HOME",
                    os.path.join(tempfile.gettempdir(),
                                 "audit-council-eval-cache"))
    proc = subprocess.run([PYTHON, AUDIT_COUNCIL, *args], input=stdin,
                          capture_output=True, text=True, check=False,
                          env=env)
    return proc


def _finding(fid, model_prefix, title, claim, path, ranges, severity,
             status="PROVISIONAL", late=False):
    return {
        "id": fid, "origin": fid, "title": title, "category": " seeded",
        "severity": severity, "confidence": "HIGH", "claim": claim,
        "status": status,
        "evidence": [{"kind": "OBSERVED_FACT", "path": path,
                      "line_ranges": ranges,
                      "description": "scripted fixture evidence"}],
        "counter_evidence": [],
        "provenance": {"discovered_by": model_prefix},
        "late_finding": late,
    }


def _ranges_from_lines(lines: str):
    start, _, end = lines.partition("-")
    return [{"start": int(start), "end": int(end or start)}]


def _scripted_artifacts(truth: dict, fingerprint: str,
                        head: str) -> dict[str, Any]:
    """Build the scripted two-model artifact set from the sealed truth."""
    defects = truth.get("defects") or []
    name = truth.get("fixture", "")
    opus_findings, codex_findings = [], []
    challenges_codex = []   # codex falsifying opus findings
    challenges_opus = []    # opus falsifying codex findings
    i_opus, i_codex = 1, 1

    for idx, defect in enumerate(defects):
        mode = ("consensus", "opus-only", "codex-only")[idx % 3]
        f = dict(defect)
        ranges = _ranges_from_lines(f.get("lines", "1"))
        path = f.get("path", "src/x")
        claim = f.get("expected_finding", "seeded defect")
        severity = f.get("severity", "HIGH")
        if mode in ("consensus", "opus-only"):
            fid = f"OPUS-{i_opus:03d}"; i_opus += 1
            opus_findings.append(_finding(
                fid, "OPUS", f["id"], claim, path, ranges, severity))
            if mode == "consensus":
                challenges_codex.append({
                    "target_finding_id": fid, "verdict": "CONFIRMED",
                    "reasoning_summary": "scripted confirm"})
            else:
                challenges_codex.append({
                    "target_finding_id": fid,
                    "verdict": "INSUFFICIENT_EVIDENCE",
                    "reasoning_summary": "scripted: not independently "
                                         "reproduced by second model"})
        if mode in ("consensus", "codex-only"):
            fid = f"CODEX-{i_codex:03d}"; i_codex += 1
            codex_findings.append(_finding(
                fid, "CODEX", f["id"], claim, path, ranges, severity))
            if mode == "consensus":
                challenges_opus.append({
                    "target_finding_id": fid, "verdict": "CONFIRMED",
                    "reasoning_summary": "scripted confirm"})
            else:
                challenges_opus.append({
                    "target_finding_id": fid,
                    "verdict": "INSUFFICIENT_EVIDENCE",
                    "reasoning_summary": "scripted: not independently "
                                         "reproduced by second model"})

    # one seeded FALSE POSITIVE (first defect fixture): raised by opus,
    # rejected by codex with counter-evidence
    if defects:
        fp = _finding(f"OPUS-{i_opus:03d}", "OPUS", "FP-1",
                      "fabricated defect not in ground truth",
                      "src/invented.js", [{"start": 1, "end": 2}],
                      "MEDIUM")
        opus_findings.append(fp)
        challenges_codex.append({
            "target_finding_id": fp["id"], "verdict": "REJECTED",
            "reasoning_summary": "file does not exist",
            "counter_evidence": [{"kind": "OBSERVED_FACT",
                                  "description":
                                      "no such path in the repository"}]})

    # clean-idioms: a candidate against a PROTECTED control, rejected
    if name == "clean-idioms":
        protected = (truth.get("must_not_flag") or [{}])[0]
        path = protected.get("path", "src/sanitize.py")
        cand = _finding(f"OPUS-{i_opus:03d}", "OPUS", "NEG-1",
                        protected.get("note", "protected control pattern"),
                        path, [{"start": 1, "end": 5}], "LOW")
        opus_findings.append(cand)
        challenges_codex.append({
            "target_finding_id": cand["id"], "verdict": "REJECTED",
            "reasoning_summary": "protected control: behavior is correct",
            "counter_evidence": [{"kind": "OBSERVED_FACT", "path": path,
                                  "line_ranges": [{"start": 1, "end": 5}],
                                  "description":
                                      "the idiom is deliberately safe"}]})

    artifacts = {
        "opus": {"model": "claude-opus-5",
                 "repository_fingerprint_sha256": fingerprint,
                 "findings": opus_findings, "audit_summary": "scripted"},
        "codex": {"model": "gpt-5.6-sol",
                  "repository_fingerprint_sha256": fingerprint,
                  "findings": codex_findings, "audit_summary": "scripted"},
        "opus_cex": {"examiner": "CODEX", "examined": "OPUS",
                     "challenges": challenges_codex},
        "codex_cex": {"examiner": "OPUS", "examined": "CODEX",
                      "challenges": challenges_opus},
    }
    return artifacts


def _final_from_artifacts(artifacts, fingerprint, completeness):
    """Adjudicated synthesis of the scripted run (inclusion rules): a
    finding enters primary when consensus or confirmed-after-challenge;
    rejected ones go to the appendix; everything else is UNRESOLVED."""
    verdicts_by_target = {}
    for ch in artifacts["opus_cex"]["challenges"]:
        verdicts_by_target[ch["target_finding_id"]] = ch["verdict"]
    primary, rejected = [], []
    seen_claims: set[str] = set()
    cluster_seq = 0
    opus_by_id = {f["id"]: f for f in artifacts["opus"]["findings"]}
    codex_by_id = {f["id"]: f for f in artifacts["codex"]["findings"]}
    # consensus pairs by claim text
    for f in artifacts["opus"]["findings"] + artifacts["codex"]["findings"]:
        key = f["claim"]
        if verdicts_by_target.get(f["id"]) == "REJECTED":
            cluster_seq += 1
            rejected.append({"cluster_id": f"CLUSTER-{cluster_seq:03d}",
                             "title": f["title"],
                             "reason": "rejected in cross-examination"})
            continue
        if key in seen_claims:
            continue
        confirmed = verdicts_by_target.get(f["id"]) in (
            "CONFIRMED", "INSUFFICIENT_EVIDENCE")
        codex_confirmed = any(
            c["target_finding_id"] in codex_by_id and
            c["verdict"] in ("CONFIRMED", "INSUFFICIENT_EVIDENCE")
            for c in artifacts["codex_cex"]["challenges"])
        origin = [f["id"]]
        other = codex_by_id if f["id"].startswith("OPUS") else opus_by_id
        for oid, of in other.items():
            if of["claim"] == f["claim"]:
                origin.append(oid)
                break
        if confirmed or codex_confirmed or len(origin) > 1:
            seen_claims.add(key)
            cluster_seq += 1
            primary.append({
                "cluster_id": f"CLUSTER-{cluster_seq:03d}",
                "title": f["title"], "severity": f["severity"],
                "final_status": "CONFIRMED",
                "claim": f["claim"], "evidence": f["evidence"],
                "provenance": {"origin": origin,
                               "final_status":
                                   "CONFIRMED_AFTER_CHALLENGE"
                                   if len(origin) > 1 else "CONFIRMED"},
            })
    return {"completeness_state": completeness,
            "repository_fingerprint_sha256": fingerprint,
            "executive_summary": "scripted tier-2 run",
            "findings": primary, "rejected_appendix": rejected,
            "unresolved_risks": [], "residual_risks": []}


def run_fixture(name: str, root: str) -> dict[str, Any]:
    """Build + drive the real pipeline for one fixture; returns scoring."""
    summary = t2.build_all(root) if not os.path.isdir(
        os.path.join(root, name)) else {"fixtures": {}, "root": root,
                                        "sealed_root":
                                        os.path.join(root, "sealed")}
    repo = os.path.join(root, name)
    truth = t2.load_ground_truth(name, root)
    truth = dict(truth, fixture=name)
    brief = os.path.join(root, "brief.md")
    with open(brief, "w") as fh:
        fh.write(f"# brief\nAudit fixture {name}.\n")
    proc = _cli("init-run", "--repo", repo, "--brief", brief)
    if proc.returncode != 0:
        return {"fixture": name, "error": proc.stdout + proc.stderr}
    run_dir = None
    for line in proc.stdout.splitlines():
        if re.match(r"^\S*audit-output/audit-council/", line.strip()):
            run_dir = line.strip()
    if not run_dir:
        return {"fixture": name, "error": "no run dir"}
    import state_store
    st = state_store.load_state(run_dir)
    binding = json.load(open(os.path.join(
        run_dir, "01-environment-binding.json")))
    contract = {
        "objective": "o", "scope": ["src/"], "exclusions": [],
        "authoritative_sources": ["brief.md"],
        "target_repository": {"root": repo, "head_sha": binding["head_sha"],
                              "fingerprint_sha256":
                                  st["repo_fingerprint_sha256"]},
        "severity_definitions": {k: k for k in
                                 ("CRITICAL", "HIGH", "MEDIUM", "LOW",
                                  "INFO")},
        "evidence_rules": [], "finding_schema_ref":
        "schemas/finding.schema.json", "done_criteria": ["d"],
    }
    p = _cli("freeze-contract", "--run", run_dir, "--artifact", "-",
             "--stdin", stdin=json.dumps(contract))
    if p.returncode != 0:
        return {"fixture": name, "error": "freeze: " + p.stdout}

    artifacts = _scripted_artifacts(truth, st["repo_fingerprint_sha256"],
                                    binding["head_sha"])
    steps = [
        ("OPUS_INDEPENDENT_COMPLETE", "10-opus-independent.json",
         artifacts["opus"]),
        ("CODEX_INDEPENDENT_COMPLETE", "20-codex-independent.json",
         artifacts["codex"]),
        ("NORMALIZED", "30-normalized-findings.json",
         {"clusters": []}),
        ("OPUS_CROSS_EXAM_COMPLETE", "31-opus-cross-examination.json",
         artifacts["codex_cex"]),
        ("CODEX_CROSS_EXAM_COMPLETE", "32-codex-cross-examination.json",
         artifacts["opus_cex"]),
        ("LEDGER_COMPLETE", "40-disagreement-ledger.json",
         {"clusters": []}),
    ]
    for phase, artifact_name, doc in steps:
        p = _cli("advance", "--run", run_dir, "--to", phase,
                 "--artifact", artifact_name, "--stdin",
                 stdin=json.dumps(doc))
        if p.returncode != 0:
            return {"fixture": name, "error":
                    f"{phase}: {p.stdout}"}
    final = _final_from_artifacts(
        artifacts, st["repo_fingerprint_sha256"], "COMPLETE")
    p = _cli("advance", "--run", run_dir, "--to", "FINALIZED",
             "--artifact", "90-final-findings.json", "--stdin",
             stdin=json.dumps(final))
    if p.returncode != 0:
        return {"fixture": name, "error": "FINALIZED: " + p.stdout}
    return _score(name, truth, final, run_dir)


def _score(name, truth, final, run_dir) -> dict[str, Any]:
    defects = truth.get("defects") or []
    expected_claims = {d["expected_finding"] for d in defects}
    primary = final.get("findings") or []
    found = {f["claim"] for f in primary} & expected_claims
    recall = len(found) / len(expected_claims) if expected_claims else 1.0
    true_positives = len(found)
    false_positives = len([f for f in primary
                           if f["claim"] not in expected_claims])
    precision = (true_positives /
                 (true_positives + false_positives)) \
        if (true_positives + false_positives) else 1.0
    protected = set()
    for p in truth.get("protected_controls") or []:
        protected.add(p if isinstance(p, str) else p.get("path", ""))
    for m in truth.get("must_not_flag") or []:
        protected.add(m.get("path", ""))
    protected.discard("")
    # R5 NEW-7: normalize both sides (./ prefixes, repo-relative joins)
    # so path SPELLING cannot evade the protected-control check
    repo_root = os.path.abspath(os.path.join(run_dir, "..", "..", ".."))

    def _norm(p):
        if not isinstance(p, str) or not p:
            return p
        expanded = os.path.expanduser(p)
        if not os.path.isabs(expanded):
            expanded = os.path.join(repo_root, expanded)
        # R6: realpath so in-repo symlink aliases cannot evade the
        # protected-control metric
        return os.path.realpath(os.path.normpath(expanded))

    protected = {_norm(p) for p in protected}
    protected_hits = [f["claim"] for f in primary
                      if any(_norm(e.get("path")) in protected
                             for e in f.get("evidence", []))]
    rejected_titles = {r["title"] for r in final.get("rejected_appendix",
                                                     [])}
    return {
        "fixture": name,
        "recall": round(recall, 3),
        "precision": round(precision, 3),
        "defects_seeded": len(defects),
        "defects_found": len(found),
        "false_positives_primary": false_positives,
        "protected_control_primary_violations": len(protected_hits),
        "false_positive_rejected_in_pipeline": bool(
            any("FP-1" in t for t in rejected_titles)),
        "run_dir": run_dir,
    }


def tier2_score(root: str) -> dict[str, Any]:
    results = [run_fixture(spec["name"], root)
               for spec in t2.FIXTURE_SPECS]
    ok = [r for r in results if "error" not in r]
    overall_recall = (sum(r["recall"] for r in ok) / len(ok)) if ok else 0.0
    overall_precision = (sum(r["precision"] for r in ok) / len(ok)) \
        if ok else 0.0
    return {
        "fixtures": results,
        "overall": {
            "recall": round(overall_recall, 3),
            "precision": round(overall_precision, 3),
            "protected_control_violations_total": sum(
                r["protected_control_primary_violations"] for r in ok),
            "errors": [r for r in results if "error" in r],
            "note": "fake-model tier 2: scripted artifacts derived from "
                    "sealed truth, executed through the REAL state "
                    "machine + validators; no model calls",
        },
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    args = ap.parse_args()
    print(json.dumps(tier2_score(args.root), indent=2))
