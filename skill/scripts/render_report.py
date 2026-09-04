#!/usr/bin/env python3
"""render_report.py — deterministic markdown rendering of audit-council artifacts.

Library API (used by audit_council.py):
    render(run_dir, artifact_name) -> str   (markdown)

Artifact names supported:
    10-opus-independent | 20-codex-independent   (independent audits)
    40-disagreement-ledger
    90-final-findings                            (full §25 final report)

__main__ convenience:
    python3 render_report.py --run DIR --artifact NAME [--out FILE] [--stdout]
"""

from __future__ import annotations

import argparse
import json
import os
import sys

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
EVIDENCE_HIERARCHY = [
    ("OBSERVED_FACT", "Directly verifiable repository state: code, tests, commands, artifacts."),
    ("REQUIREMENT_CLAIM", "Explicit requirement from the audit brief/contract under test."),
    ("INFERENCE", "Derived conclusion from observed facts; reproducible reasoning chain."),
    ("HYPOTHESIS", "Unverified supposition; requires evidence before relying on it."),
]

FINAL_SECTION_ORDER = [
    "Executive summary",
    "Audit scope and repository identity",
    "Audit completeness status",
    "Methodology",
    "Evidence hierarchy",
    "Confirmed findings (ordered by severity)",
    "Systemic / root-cause findings",
    "Requirement coverage gaps",
    "Rejected findings and high-value false positives",
    "Unresolved disputes",
    "Residual risks",
    "Audit limitations",
    "Model provenance",
    "Run metrics",
]


def _read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_optional(path):
    if os.path.isfile(path):
        try:
            return _read_json(path)
        except (ValueError, OSError):
            return None
    return None


def _escape(text) -> str:
    return str(text if text is not None else "").replace("|", "\\|").replace("\n", " ")


def _bullet_ev_item(ev: dict) -> str:
    bits = []
    if ev.get("kind"):
        bits.append("`%s`" % ev["kind"])
    loc = []
    if ev.get("path"):
        loc.append(ev["path"])
    if ev.get("symbol"):
        loc.append(ev["symbol"])
    if loc:
        bits.append("`%s`" % ":".join(loc))
    if ev.get("lines"):
        bits.append("lines %s" % ev["lines"])
    for ref in ("requirement_ref", "test_ref", "command_ref"):
        if ev.get(ref):
            bits.append("%s=%s" % (ref, ev[ref]))
    if ev.get("artifact_hash"):
        bits.append("hash `%s`" % ev["artifact_hash"])
    if ev.get("description"):
        bits.append(ev["description"])
    return "- " + " — ".join(bits) if bits else "- (evidence item without fields)"


# ---------------------------------------------------------------------------
# independent audits (10 / 20)
# ---------------------------------------------------------------------------

def render_independent(data: dict) -> str:
    lines = []
    model = data.get("model", "unknown model")
    lines.append("# Independent Audit — %s" % model)
    lines.append("")
    lines.append("- Repository fingerprint: `%s`" % data.get("repository_fingerprint_sha256", "n/a"))
    lines.append("- Findings: %d" % len(data.get("findings", [])))
    lines.append("")
    if data.get("audit_summary"):
        lines.append("## Summary")
        lines.append("")
        lines.append(data["audit_summary"])
        lines.append("")

    findings = data.get("findings", [])
    if findings:
        lines.append("## Findings")
        lines.append("")
        lines.append("| ID | Severity | Confidence | Status | Title |")
        lines.append("|---|---|---|---|---|")
        for f in findings:
            lines.append("| %s | %s | %s | %s | %s |" % (
                _escape(f.get("id")), _escape(f.get("severity")),
                _escape(f.get("confidence")), _escape(f.get("status")),
                _escape(f.get("title"))))
        lines.append("")
        for f in findings:
            lines.append("### %s — %s" % (f.get("id"), f.get("title", "")))
            lines.append("")
            lines.append("- Category: %s" % f.get("category", "n/a"))
            lines.append("- Severity: %s | Confidence: %s | Status: %s" % (
                f.get("severity"), f.get("confidence"), f.get("status")))
            if f.get("claim"):
                lines.append("")
                lines.append("**Claim.** %s" % f["claim"])
            if f.get("failure_scenario"):
                lines.append("")
                lines.append("**Failure scenario.** %s" % f["failure_scenario"])
            if f.get("impact"):
                lines.append("")
                lines.append("**Impact.** %s" % f["impact"])
            if f.get("root_cause"):
                lines.append("")
                lines.append("**Root cause.** %s" % f["root_cause"])
            if f.get("evidence"):
                lines.append("")
                lines.append("**Evidence.**")
                lines.extend(_bullet_ev_item(e) for e in f["evidence"])
            if f.get("counter_evidence"):
                lines.append("")
                lines.append("**Counter-evidence.**")
                lines.extend(_bullet_ev_item(e) for e in f["counter_evidence"])
            prov = f.get("provenance") or {}
            if prov:
                lines.append("")
                extras = []
                if prov.get("independently_confirmed_by"):
                    extras.append("confirmed_by=%s" % ",".join(prov["independently_confirmed_by"]))
                if f.get("cluster_id"):
                    extras.append("cluster=%s" % f["cluster_id"])
                suffix = ("; " + "; ".join(extras)) if extras else ""
                lines.append("**Provenance.** discovered_by=%s%s" % (
                    prov.get("discovered_by", "n/a"), suffix))
            if f.get("requirement_refs"):
                lines.append("- Requirement refs: %s" % ", ".join(f["requirement_refs"]))
            if f.get("residual_uncertainty"):
                lines.append("")
                lines.append("**Residual uncertainty.** %s" % f["residual_uncertainty"])
            lines.append("")

    cov = data.get("requirement_coverage") or []
    if cov:
        lines.append("## Requirement coverage")
        lines.append("")
        lines.append("| Requirement | Covered | Note |")
        lines.append("|---|---|---|")
        for c in cov:
            lines.append("| %s | %s | %s |" % (
                _escape(c.get("requirement")),
                "yes" if c.get("covered") else "NO",
                _escape(c.get("note", ""))))
        lines.append("")

    lims = data.get("limitations") or []
    if lims:
        lines.append("## Limitations")
        lines.append("")
        lines.extend("- %s" % l for l in lims)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# disagreement ledger (40)
# ---------------------------------------------------------------------------

def render_ledger(data: dict) -> str:
    lines = ["# Disagreement Ledger", ""]
    clusters = data.get("clusters", [])
    lines.append("- Clusters: %d" % len(clusters))
    lines.append("")
    if clusters:
        lines.append("| Cluster | Classification | Status | Members | Opus | Codex |")
        lines.append("|---|---|---|---|---|---|")
        for c in clusters:
            pos = c.get("positions", {})
            lines.append("| %s | %s | %s | %s | %s | %s |" % (
                _escape(c.get("cluster_id")),
                _escape(c.get("initial_classification")),
                _escape(c.get("status")),
                _escape(", ".join(c.get("member_finding_ids", []))),
                _escape((pos.get("opus") or {}).get("position", "n/a")),
                _escape((pos.get("codex") or {}).get("position", "n/a"))))
        lines.append("")
        for c in clusters:
            lines.append("## %s" % c.get("cluster_id"))
            lines.append("")
            lines.append("- Classification: %s" % c.get("initial_classification"))
            lines.append("- Status: %s" % c.get("status"))
            lines.append("- Members: %s" % ", ".join(c.get("member_finding_ids", [])))
            pos = c.get("positions", {})
            for side in ("opus", "codex"):
                p = pos.get(side) or {}
                bits = ["%s position: %s" % (side.upper(), p.get("position", "n/a"))]
                if p.get("severity"):
                    bits.append("severity=%s" % p["severity"])
                if "challenge_result" in p:
                    bits.append("challenge_result=%s" % p.get("challenge_result"))
                lines.append("- %s" % " | ".join(bits))
            if c.get("evidence_overlap"):
                lines.append("- Evidence overlap: %s" % c["evidence_overlap"])
            if c.get("severity_divergence") is not None:
                lines.append("- Severity divergence: %s" % c["severity_divergence"])
            if c.get("causal_divergence") is not None:
                lines.append("- Causal divergence: %s" % c["causal_divergence"])
            if c.get("adjudication_eligible") is not None:
                lines.append("- Adjudication eligible: %s" % c["adjudication_eligible"])
            if c.get("counter_evidence"):
                lines.append("")
                lines.append("Counter-evidence:")
                lines.extend(_bullet_ev_item(e) for e in c["counter_evidence"])
            if c.get("notes"):
                lines.append("")
                lines.append("Notes: %s" % c["notes"])
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# final report (90)
# ---------------------------------------------------------------------------

def _provenance_line(f: dict) -> str:
    prov = f.get("provenance") or {}
    origin = ", ".join(prov.get("origin", [])) or "n/a"

    def val(x):
        return x if x else "—"

    parts = ["Origin: %s" % origin]
    if prov.get("opus_challenge"):
        parts.append("Opus challenge: %s" % prov["opus_challenge"])
    if prov.get("codex_challenge"):
        parts.append("Codex re-evaluation: %s" % prov["codex_challenge"])
    if prov.get("adjudication"):
        parts.append("Adjudication: %s" % prov["adjudication"])
    parts.append("Final: %s" % prov.get("final_status", f.get("final_status", "n/a")))
    return "%s — %s" % (f.get("cluster_id"), " | ".join(parts))


def _render_final(data: dict, run_dir: str) -> str:
    lines = ["# Audit Council — Final Audit Report", ""]
    add = lines.append

    def section(title):
        if lines != ["# Audit Council — Final Audit Report", ""]:
            add("")
        add("## %s" % title)
        add("")

    # 1 Executive summary
    section(FINAL_SECTION_ORDER[0])
    add(data.get("executive_summary", "(no executive summary provided)"))

    # 2 Audit scope and repository identity
    section(FINAL_SECTION_ORDER[1])
    contract = _load_optional(os.path.join(run_dir, "02-audit-contract.json"))
    repo_state = _load_optional(os.path.join(run_dir, "01-repository-state.json"))
    add("- Repository fingerprint: `%s`" % data.get("repository_fingerprint_sha256", "n/a"))
    for src, label in ((repo_state, "repository state"), (contract, "audit contract")):
        if not src:
            continue
        for key in ("repo_root", "head_sha", "branch", "brief_path", "scope"):
            if isinstance(src, dict) and src.get(key) is not None:
                add("- %s (%s): %s" % (key, label, src[key]))
        for key in ("audit_scope", "requirements"):
            if isinstance(src, dict) and src.get(key):
                add("- %s: %s" % (key, json.dumps(src[key], ensure_ascii=False)))
    if contract is None and repo_state is None:
        add("(scope and identity artifacts not present in run directory)")

    # 3 Audit completeness status
    section(FINAL_SECTION_ORDER[2])
    add("- Completeness state: **%s**" % data.get("completeness_state", "n/a"))
    if data.get("claims_lacking_second_model"):
        add("")
        add("Claims lacking second-model adjudication:")
        lines.extend("- %s" % c for c in data["claims_lacking_second_model"])

    # 4 Methodology
    section(FINAL_SECTION_ORDER[3])
    add(data.get("methodology") or
        "Two independent full audits (Claude Opus 5 and Codex GPT-5.6 Sol, read-only), "
        "normalization and clustering into a disagreement ledger, mutual cross-examination, "
        "and at most one bounded targeted adjudication round for materially disputed "
        "HIGH/CRITICAL clusters.")

    # 5 Evidence hierarchy
    section(FINAL_SECTION_ORDER[4])
    lines.extend("%d. **%s** — %s" % (i + 1, k, d) for i, (k, d) in enumerate(EVIDENCE_HIERARCHY))

    # 6 Confirmed findings ordered by severity
    section(FINAL_SECTION_ORDER[5])
    findings = list(data.get("findings", []))
    findings.sort(key=lambda f: SEVERITY_ORDER.index(f["severity"])
                  if f.get("severity") in SEVERITY_ORDER else len(SEVERITY_ORDER))
    if not findings:
        add("(no confirmed findings)")
    else:
        add("| Cluster | Severity | Final status | Title |")
        add("|---|---|---|---|")
        for f in findings:
            add("| %s | %s | %s | %s |" % (
                _escape(f.get("cluster_id")), _escape(f.get("severity")),
                _escape(f.get("final_status")), _escape(f.get("title"))))
        add("")
        for f in findings:
            add("### %s — %s" % (f.get("cluster_id"), f.get("title", "")))
            add("")
            add("- Severity: %s | Final status: %s" % (f.get("severity"), f.get("final_status")))
            if f.get("category"):
                add("- Category: %s" % f["category"])
            if f.get("claim"):
                add("")
                add("**Claim.** %s" % f["claim"])
            if f.get("impact"):
                add("")
                add("**Impact.** %s" % f["impact"])
            if f.get("evidence"):
                add("")
                add("**Evidence.**")
                lines.extend(_bullet_ev_item(e) for e in f["evidence"])
            if f.get("counter_evidence"):
                add("")
                add("**Counter-evidence.**")
                lines.extend(_bullet_ev_item(e) for e in f["counter_evidence"])
            if f.get("residual_uncertainty"):
                add("")
                add("**Residual uncertainty.** %s" % f["residual_uncertainty"])
            add("")

    # 7 Systemic / root-cause findings
    section(FINAL_SECTION_ORDER[6])
    systemic = [f for f in findings if f.get("root_cause")]
    if not systemic:
        add("(no systemic/root-cause findings recorded)")
    else:
        for f in systemic:
            add("- **%s (%s)** — root cause: %s" % (
                f.get("cluster_id"), f.get("severity"), f["root_cause"]))

    # 8 Requirement coverage gaps
    section(FINAL_SECTION_ORDER[7])
    gaps = data.get("coverage_gaps") or []
    if not gaps:
        add("(no requirement coverage gaps recorded)")
    else:
        lines.extend("- %s" % g for g in gaps)

    # 9 Rejected findings / high-value false positives
    section(FINAL_SECTION_ORDER[8])
    rejected = data.get("rejected_appendix") or []
    if not rejected:
        add("(no rejected findings)")
    else:
        for r in rejected:
            add("- **%s** — %s" % (r.get("cluster_id"), _escape(r.get("title"))))
            add("  - Reason: %s" % r.get("reason"))
            if r.get("origin"):
                add("  - Origin: %s" % ", ".join(r["origin"]))

    # 10 Unresolved disputes
    section(FINAL_SECTION_ORDER[9])
    unresolved = data.get("unresolved_risks") or []
    unresolved += [f for f in findings if f.get("final_status") == "UNRESOLVED"]
    if not unresolved:
        add("(no unresolved disputes)")
    else:
        for u in unresolved:
            if isinstance(u, dict):
                add("- **%s** (%s)%s" % (
                    u.get("cluster_id"), u.get("severity"),
                    ": %s" % u["note"] if u.get("note") else ""))
            else:
                add("- %s" % u)

    # 11 Residual risks
    section(FINAL_SECTION_ORDER[10])
    rr = data.get("residual_risks") or []
    if not rr:
        add("(no residual risks recorded)")
    else:
        lines.extend("- %s" % r for r in rr)

    # 12 Audit limitations
    section(FINAL_SECTION_ORDER[11])
    lims = data.get("limitations") or []
    if not lims:
        add("(no limitations recorded)")
    else:
        lines.extend("- %s" % l for l in lims)

    # 13 Model provenance
    section(FINAL_SECTION_ORDER[12])
    if not findings:
        add("(no findings)")
    else:
        lines.extend("- %s" % _provenance_line(f) for f in findings)

    # 14 Run metrics
    section(FINAL_SECTION_ORDER[13])
    metrics = _load_optional(os.path.join(run_dir, "99-run-metrics.json"))
    if not metrics:
        add("(no run metrics recorded)")
    else:
        agg = metrics.get("aggregates", {})
        add("- Codex invocations: %s (fresh: %s, resumed: %s)" % (
            agg.get("invocation_count", "n/a"), agg.get("fresh_count", "n/a"),
            agg.get("resumed_count", "n/a")))
        tokens = agg.get("tokens", {})
        add("- Codex tokens — input: %s, cached input: %s, output: %s, reasoning output: %s" % (
            tokens.get("input_tokens", "n/a"), tokens.get("cached_input_tokens", "n/a"),
            tokens.get("output_tokens", "n/a"),
            tokens.get("reasoning_output_tokens", "n/a")))
        add("- Codex turns: %s | total elapsed: %ss" % (
            agg.get("turns_total", "n/a"), agg.get("elapsed_sec_total", "n/a")))
        add("- Codex quota-saving note: architecture reuses one Codex session across "
            "cross-examination and adjudication via `codex exec resume`.")

    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------

def render(run_dir: str, artifact_name: str) -> str:
    run_dir = os.path.abspath(run_dir)
    json_path = os.path.join(run_dir, artifact_name + ".json")
    data = _read_json(json_path)
    if artifact_name in ("10-opus-independent", "20-codex-independent"):
        return render_independent(data)
    if artifact_name == "40-disagreement-ledger":
        return render_ledger(data)
    if artifact_name == "90-final-findings":
        return _render_final(data, run_dir)
    raise ValueError("unsupported artifact: %s" % artifact_name)


def default_out_path(run_dir: str, artifact_name: str) -> str:
    if artifact_name == "90-final-findings":
        return os.path.join(run_dir, "90-final-audit.md")
    return os.path.join(run_dir, artifact_name + ".md")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render audit-council artifacts to markdown")
    p.add_argument("--run", required=True)
    p.add_argument("--artifact", required=True)
    p.add_argument("--out", default=None)
    p.add_argument("--stdout", action="store_true")
    args = p.parse_args(argv)
    md = render(args.run, args.artifact)
    if args.stdout:
        sys.stdout.write(md)
    else:
        out = args.out or default_out_path(args.run, args.artifact)
        with open(out, "w", encoding="utf-8") as f:
            f.write(md)
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
