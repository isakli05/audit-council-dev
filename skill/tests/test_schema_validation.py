#!/usr/bin/env python3
"""Scenario A: schema-shape checks + representative valid/invalid instances
for every schema in schemas/*.json, via validate_artifact.validate."""
from __future__ import annotations

import json
import os
import re
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import state_store  # noqa: E402
import validate_artifact  # noqa: E402

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"
SCHEMA_NAMES = sorted(p.name for p in SCHEMAS_DIR.glob("*.json"))
assert len(SCHEMA_NAMES) == 13, SCHEMA_NAMES  # v2: + env-binding, environment-record, evidence-record, public-contract, specialist-review

_KNOWN_TYPES = {"object", "array", "string", "integer", "number",
                "boolean", "null"}


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS_DIR / name).read_text(encoding="utf-8"))


def check_schema_shape(node, path: str, errors: list[str],
                       seen_refs: list[str]) -> None:
    """Recursive structural check: JSON-Schema-shaped using only keywords the
    minimal validator supports, with resolvable local refs."""
    if isinstance(node, bool):
        return
    if not isinstance(node, dict):
        errors.append(f"{path}: schema fragment is not object/bool")
        return
    unknown = set(node) - validate_artifact.SUPPORTED_KEYWORDS
    if unknown:
        errors.append(f"{path}: unsupported keywords {sorted(unknown)}")
    if "type" in node:
        t = node["type"]
        types = t if isinstance(t, list) else [t]
        for tt in types:
            if tt not in _KNOWN_TYPES:
                errors.append(f"{path}: unknown type {tt!r}")
    if "pattern" in node:
        try:
            re.compile(node["pattern"])
        except re.error as exc:
            errors.append(f"{path}: bad pattern {node['pattern']!r}: {exc}")
    if "$ref" in node:
        ref = node["$ref"]
        seen_refs.append(f"{path} -> {ref}")
        try:
            validate_artifact._resolve_ref(ref, node, SCHEMAS_DIR)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: unresolvable ref {ref!r}: {exc}")
    for key in ("properties",):
        for k, v in (node.get(key) or {}).items():
            check_schema_shape(v, f"{path}.{k}", errors, seen_refs)
    for key in ("items", "additionalProperties"):
        if isinstance(node.get(key), dict):
            check_schema_shape(node[key], f"{path}.{key}", errors, seen_refs)
    for k, v in (node.get("$defs") or {}).items():
        check_schema_shape(v, f"{path}/$defs/{k}", errors, seen_refs)


# ---------------------------------------------------------------------------
# Shared instance builders (also asserted schema-valid for reuse by other
# test modules' artifacts)
# ---------------------------------------------------------------------------
def finding(**over):
    doc = {
        "id": "OPUS-001",
        "origin": "OPUS-001",
        "title": "Unsafe arithmetic",
        "category": "correctness",
        "severity": "HIGH",
        "confidence": "MEDIUM",
        "claim": "divide() does not guard against zero",
        "status": "PROVISIONAL",
        "evidence": [
            {"kind": "OBSERVED_FACT", "path": "src/app.py",
             "line_ranges": [{"start": 1, "end": 2}]}
        ],
        "provenance": {"discovered_by": "OPUS", "validated_by": None},
        "late_finding": False,
    }
    doc.update(over)
    return doc


def contract(**over):
    doc = {
        "objective": "Audit arithmetic helpers",
        "scope": ["src/"],
        "exclusions": ["tests/"],
        "authoritative_sources": ["audit-brief.md"],
        "target_repository": {
            "root": "/tmp/repo",
            "head_sha": "0" * 40,
            "branch": "main",
            "fingerprint_sha256": "1" * 64,
            "dirty": False,
        },
        "severity_definitions": {
            "CRITICAL": "c", "HIGH": "h", "MEDIUM": "m", "LOW": "l",
            "INFO": "i",
        },
        "evidence_rules": ["every claim cites evidence"],
        "finding_schema_ref": "schemas/finding.schema.json",
        "done_criteria": ["all requirements covered"],
    }
    doc.update(over)
    return doc


def independent_audit(**over):
    doc = {
        "model": "claude-opus-5",
        "repository_fingerprint_sha256": "ab" * 32,
        "findings": [finding()],
        "audit_summary": "one finding",
    }
    doc.update(over)
    return doc


def cross_examination():
    return {
        "examiner": "CODEX",
        "examined": "OPUS",
        "challenges": [
            {
                "target_finding_id": "OPUS-001",
                "verdict": "CONFIRMED",
                "reasoning_summary": "evidence checks out",
                "counter_evidence": [],
                "severity_recalibration": {
                    "original": "HIGH", "revised": "MEDIUM",
                    "justification": "impact limited",
                },
            }
        ],
        "late_findings": [
            finding(id="CODEX-005", origin="CODEX-005",
                    provenance={"discovered_by": "CODEX"},
                    late_finding=True)
        ],
    }


def ledger():
    return {
        "clusters": [
            {
                "cluster_id": "CLUSTER-001",
                "initial_classification": "CONSENSUS_CANDIDATE",
                "status": "CONSENSUS",
                "member_finding_ids": ["OPUS-001", "CODEX-001"],
                "positions": {
                    "opus": {"position": "real bug", "severity": "HIGH"},
                    "codex": {"position": "real bug", "severity": "HIGH"},
                },
                "adjudication_eligible": False,
            }
        ]
    }


def adjudication():
    return {
        "rounds": [
            {
                "cluster_id": "CLUSTER-001",
                "evidence_packet": {"claim": "divide() unsafe"},
                "opus_verdict": "CONFIRMED",
                "codex_verdict": "PARTIALLY_CONFIRMED",
                "final_status": "CONFIRMED",
                "rationale": "evidence preponderates",
            }
        ]
    }


def final_findings():
    return {
        "completeness_state": "COMPLETE",
        "repository_fingerprint_sha256": "ab" * 32,
        "executive_summary": "one confirmed finding",
        "findings": [
            {
                "cluster_id": "CLUSTER-001",
                "title": "Unsafe arithmetic",
                "severity": "HIGH",
                "final_status": "CONFIRMED",
                "claim": "divide() does not guard against zero",
                "provenance": {
                    "origin": ["OPUS-001", "CODEX-001"],
                    "final_status": "CONSENSUS",
                },
                "evidence": [
                    {"kind": "OBSERVED_FACT", "path": "src/app.py"}
                ],
            }
        ],
        "rejected_appendix": [
            {"cluster_id": "CLUSTER-002", "title": "style nit",
             "reason": "rejected in cross-examination"}
        ],
        "unresolved_risks": [],
    }


def state_doc():
    return state_store.new_state("20260903T170000Z-a1b2c3", "/tmp/repo",
                                 "0" * 64)


def env_binding_doc():
    return {
        "binding_version": 2,
        "binding_digest": "0" * 64,
        "frozen_at": "2026-09-04T00:00:00Z",
        "repo_root_realpath": "/home/isa/audit-council-dev/repro/tmp/r3-target-repo",
        "git_toplevel_realpath": "/home/isa/audit-council-dev/repro/tmp/r3-target-repo",
        "git_dir_realpath": "/home/isa/audit-council-dev/repro/tmp/r3-target-repo/.git",
        "git_common_dir_realpath": "/home/isa/audit-council-dev/repro/tmp/r3-target-repo/.git",
        "head_sha": "0" * 40,
        "detached_head": True,
        "worktree_identity": "1" * 64,
        "source_repository_identity": {
            "common_dir_realpath": "/home/isa/audit-council-dev/repro/tmp/r3-target-repo/.git",
            "remote_url": None,
        },
        "brief_sha256": "2" * 64,
        "brief_target": {
            "declared_repository_root": None,
            "declared_expected_head": None,
        },
        "expected_head": "0" * 40,
        "allowed_disposable_roots": [],
        "repo_fingerprint_sha256": "3" * 64,
    }


def environment_record_doc():
    return {"schema_version": 2, "mode": "RELEASE",
            "run_id": "20260904T000000Z-a0a0a0",
            "created_at": "2026-09-04T00:00:00Z",
            "source_repo_realpath":
                "/home/isa/audit-council-dev/repro/tmp/r3-target-repo",
            "worktree_root": "/home/isa/audit-council-dev/repro/tmp/wt",
            "worktree_detached": True, "target_ref": "v1",
            "binding_digest": "0" * 64,
            "staged_evidence": [{"path": "docs/notes.md",
                                 "sha256": "1" * 64, "allowed": True}],
            "archive_root": "/home/isa/audit-council-dev/repro/tmp/history",
            "notes": "representative instance"}


def evidence_record_doc():
    return {"schema_version": 2,
            "evidence_id": "ev-0123456789abcdef",
            "kind": "FILE_EXCERPT",
            "repository_fingerprint_sha256": "2" * 64,
            "environment_binding_digest": "0" * 64,
            "input_digest": "3" * 64,
            "tool": {"name": "rg", "version": "14.0"},
            "command_or_query": "rg -n pattern src/",
            "produced_at": "2026-09-04T00:00:00Z",
            "freshness_policy": {"class": "CACHEABLE", "ttl_sec": 3600,
                                 "invalidated_by": ["tracked_change"]},
            "result_digest": "4" * 64,
            "result_location": "evidence/objects/x.json",
            "producer": "OPUS",
            "visibility": "SHARED_MECHANICAL",
            "validity_scope": "RUN",
            "deterministic": True, "reproducible": True}


def public_contract_doc():
    # PKG-PUB: the real machine-readable contract; single definition lives
    # in audit_council.PUBLIC_CONTRACT (deep-copied — callers mutate)
    import copy

    import audit_council
    return copy.deepcopy(audit_council.PUBLIC_CONTRACT)


def specialist_review_doc():
    return {
        "schema_version": 2,
        "domain": "security-trust",
        "reviewer": "SPECIALIST-security-trust",
        "coverage": [{"area": "session token verification", "covered": True,
                      "note": "inspected middleware paths"}],
        "candidate_findings": [{
            "id": "OPUS-001", "origin": "OPUS-001",
            "title": "Unsigned session cookie accepted by auth middleware",
            "category": "security", "severity": "HIGH",
            "confidence": "MEDIUM",
            "claim": "verify_session accepts cookies without a signature "
                     "check",
            "status": "PROVISIONAL",
            "evidence": [{"kind": "OBSERVED_FACT", "path": "src/auth.py",
                          "symbol": "verify_session",
                          "line_ranges": [{"start": 40, "end": 52}],
                          "description": "no signature verification call"}],
            "counter_evidence": [],
            "provenance": {"discovered_by": "SPECIALIST-security-trust"},
        }],
        "negative_evidence": [{"kind": "SEARCH_RESULT",
                               "description": "no secrets logged in scope"}],
        "unresolved_questions": ["rotation enforced cluster-wide?"],
        "evidence_refs": ["ev-0123456789abcdef"],
        "notes": "representative instance",
    }


BUILDERS = {
    "finding.schema.json": finding,
    "audit-contract.schema.json": contract,
    "independent-audit.schema.json": independent_audit,
    "cross-examination.schema.json": cross_examination,
    "disagreement-ledger.schema.json": ledger,
    "adjudication.schema.json": adjudication,
    "env-binding.schema.json": env_binding_doc,
    "environment-record.schema.json": environment_record_doc,
    "evidence-record.schema.json": evidence_record_doc,
    "final-findings.schema.json": final_findings,
    "public-contract.schema.json": public_contract_doc,
    "specialist-review.schema.json": specialist_review_doc,
    "state.schema.json": state_doc,
}


class TestSchemaShape(unittest.TestCase):
    def test_every_schema_file_is_json_schema_shaped(self):
        for name in SCHEMA_NAMES:
            with self.subTest(schema=name):
                doc = load_schema(name)
                self.assertIsInstance(doc, dict)
                errors: list[str] = []
                seen: list[str] = []
                check_schema_shape(doc, name, errors, seen)
                self.assertEqual(errors, [])
                self.assertTrue(seen or True)  # refs optional

    def test_expected_schema_set(self):
        self.assertEqual(SCHEMA_NAMES, [
            "adjudication.schema.json", "audit-contract.schema.json",
            "cross-examination.schema.json", "disagreement-ledger.schema.json",
            "env-binding.schema.json", "environment-record.schema.json",
            "evidence-record.schema.json", "final-findings.schema.json",
            "finding.schema.json", "independent-audit.schema.json",
            "public-contract.schema.json", "specialist-review.schema.json",
            "state.schema.json",
        ])


class TestRepresentativeInstances(unittest.TestCase):
    def assertValid(self, schema_name, instance):
        errors = validate_artifact.validate(
            instance, load_schema(schema_name), base_dir=SCHEMAS_DIR)
        self.assertEqual(errors, [])

    def assertInvalid(self, schema_name, instance, needle: str):
        errors = validate_artifact.validate(
            instance, load_schema(schema_name), base_dir=SCHEMAS_DIR)
        self.assertTrue(errors, f"expected errors containing {needle!r}")
        self.assertTrue(any(needle in e for e in errors),
                        f"no error mentions {needle!r}: {errors}")

    def test_valid_instance_for_every_schema(self):
        for name in SCHEMA_NAMES:
            with self.subTest(schema=name):
                self.assertValid(name, BUILDERS[name]())

    def test_finding_enums_and_patterns(self):
        self.assertInvalid("finding.schema.json",
                           finding(severity="EXTREME"), "enum")
        self.assertInvalid("finding.schema.json",
                           finding(confidence="CERTAIN"), "enum")
        self.assertInvalid("finding.schema.json",
                           finding(status="MAYBE"), "enum")
        self.assertInvalid("finding.schema.json",
                           finding(provenance={"discovered_by": "SONNET"}),
                           "pattern")  # v2: pattern, not enum (specialists)
        self.assertValid("finding.schema.json",
                         finding(provenance={
                             "discovered_by":
                                 "SPECIALIST-security-trust"}))
        self.assertInvalid("finding.schema.json",
                           finding(id="X-1", origin="X-1"), "pattern")
        self.assertInvalid("finding.schema.json",
                           finding(evidence=[{"kind": "GUESS"}]), "enum")
        self.assertInvalid("finding.schema.json",
                           finding(evidence=[{"lines": "line one"}]),
                           "additional property")  # legacy key gone in v2
        self.assertInvalid("finding.schema.json",
                           {k: v for k, v in finding().items()
                            if k != "claim"}, "missing required property")
        self.assertInvalid("finding.schema.json",
                           finding(bogus_key=1), "additional property")

    def test_state_phases_and_run_id(self):
        self.assertInvalid("state.schema.json",
                           dict(state_doc(), phase="HALFWAY"), "enum")
        self.assertInvalid("state.schema.json",
                           dict(state_doc(), completeness_state="ALMOST"),
                           "enum")
        self.assertInvalid("state.schema.json",
                           dict(state_doc(), run_id="not-a-run-id"),
                           "pattern")
        self.assertInvalid("state.schema.json",
                           dict(state_doc(), schema_version=2), "const")
        bad_codex = state_doc()
        bad_codex["codex"]["stage_counts"]["independent"] = 2
        self.assertInvalid("state.schema.json", bad_codex, "maximum")
        missing = state_doc()
        del missing["timestamps"]
        self.assertInvalid("state.schema.json", missing,
                           "missing required property")

    def test_contract_required_fields_and_const(self):
        bad = contract()
        del bad["objective"]
        self.assertInvalid("audit-contract.schema.json", bad,
                           "missing required property")
        self.assertInvalid("audit-contract.schema.json",
                           contract(finding_schema_ref="other.json"), "const")
        bad = contract()
        del bad["severity_definitions"]["HIGH"]
        self.assertInvalid("audit-contract.schema.json", bad,
                           "missing required property")
        self.assertInvalid("audit-contract.schema.json",
                           contract(scope=[]), "fewer than 1 items")
        self.assertInvalid("audit-contract.schema.json",
                           contract(done_criteria=[]), "fewer than 1 items")

    def test_independent_audit(self):
        self.assertInvalid("independent-audit.schema.json",
                           independent_audit(model="gpt-4o"), "enum")
        bad = independent_audit()
        bad["repository_fingerprint_sha256"] = "short"
        self.assertInvalid("independent-audit.schema.json", bad,
                           "shorter than 8")
        bad = independent_audit()
        del bad["audit_summary"]
        self.assertInvalid("independent-audit.schema.json", bad,
                           "missing required property")
        bad = independent_audit()
        bad["findings"][0]["severity"] = "BLOCKER"
        self.assertInvalid("independent-audit.schema.json", bad, "enum")

    def test_cross_examination(self):
        bad = cross_examination()
        bad["challenges"][0]["verdict"] = "DISPUTED"
        self.assertInvalid("cross-examination.schema.json", bad, "enum")
        bad = cross_examination()
        del bad["challenges"][0]["reasoning_summary"]
        self.assertInvalid("cross-examination.schema.json", bad,
                           "missing required property")
        bad = cross_examination()
        bad["examiner"] = "SONNET"
        self.assertInvalid("cross-examination.schema.json", bad, "enum")
        bad = cross_examination()
        bad["late_findings"][0]["id"] = "NEW-1"
        self.assertInvalid("cross-examination.schema.json", bad, "pattern")
        bad = cross_examination()
        bad["challenges"][0]["severity_recalibration"]["original"] = "BAD"
        self.assertInvalid("cross-examination.schema.json", bad, "enum")

    def test_disagreement_ledger(self):
        bad = ledger()
        bad["clusters"][0]["cluster_id"] = "CLUSTER-1"
        self.assertInvalid("disagreement-ledger.schema.json", bad, "pattern")
        bad = ledger()
        bad["clusters"][0]["status"] = "DISPUTED-ish"
        self.assertInvalid("disagreement-ledger.schema.json", bad, "enum")
        bad = ledger()
        bad["clusters"][0]["initial_classification"] = "CONFLICT"
        self.assertInvalid("disagreement-ledger.schema.json", bad, "enum")
        bad = ledger()
        bad["clusters"][0]["member_finding_ids"] = ["F-1"]
        self.assertInvalid("disagreement-ledger.schema.json", bad, "pattern")
        bad = ledger()
        bad["clusters"][0]["member_finding_ids"] = []
        self.assertInvalid("disagreement-ledger.schema.json", bad,
                           "fewer than 1 items")
        bad = ledger()
        del bad["clusters"][0]["positions"]["codex"]
        self.assertInvalid("disagreement-ledger.schema.json", bad,
                           "missing required property")
        bad = ledger()
        bad["clusters"][0]["positions"]["opus"]["severity"] = "MEH"
        self.assertInvalid("disagreement-ledger.schema.json", bad, "enum")

    def test_adjudication(self):
        bad = adjudication()
        bad["rounds"][0]["final_status"] = "DISPUTED"
        self.assertInvalid("adjudication.schema.json", bad, "enum")
        bad = adjudication()
        bad["rounds"][0]["cluster_id"] = "C-1"
        self.assertInvalid("adjudication.schema.json", bad, "pattern")
        bad = adjudication()
        bad["rounds"] = adjudication()["rounds"] * 2
        self.assertInvalid("adjudication.schema.json", bad,
                           "more than 1 items")
        bad = adjudication()
        del bad["rounds"][0]["evidence_packet"]["claim"]
        self.assertInvalid("adjudication.schema.json", bad,
                           "missing required property")

    def test_final_findings(self):
        bad = final_findings()
        bad["completeness_state"] = "ALMOST_DONE"
        self.assertInvalid("final-findings.schema.json", bad, "enum")
        bad = final_findings()
        bad["findings"][0]["final_status"] = "REJECTED"  # not in primary enum
        self.assertInvalid("final-findings.schema.json", bad, "enum")
        bad = final_findings()
        del bad["rejected_appendix"][0]["reason"]  # appendix shape
        self.assertInvalid("final-findings.schema.json", bad,
                           "missing required property")
        bad = final_findings()
        bad["rejected_appendix"][0]["cluster_id"] = 7
        self.assertInvalid("final-findings.schema.json", bad, "expected type")
        bad = final_findings()
        bad["findings"][0]["provenance"]["origin"] = []
        self.assertInvalid("final-findings.schema.json", bad,
                           "fewer than 1 items")
        bad = final_findings()
        bad["findings"][0]["provenance"]["origin"] = ["OPUS-1"]
        self.assertInvalid("final-findings.schema.json", bad, "pattern")
        bad = final_findings()
        del bad["findings"][0]["provenance"]
        self.assertInvalid("final-findings.schema.json", bad,
                           "missing required property")
        bad = final_findings()
        bad["unresolved_risks"] = [{"cluster_id": "CLUSTER-009",
                                    "severity": "MAJOR"}]
        self.assertInvalid("final-findings.schema.json", bad, "enum")

    def test_cannot_add_undeclared_top_level_keys(self):
        for name in SCHEMA_NAMES:
            with self.subTest(schema=name):
                instance = BUILDERS[name]()
                if not isinstance(instance, dict):
                    continue
                instance["zz_undeclared"] = 1
                self.assertInvalid(name, instance, "additional property")


if __name__ == "__main__":
    unittest.main()
