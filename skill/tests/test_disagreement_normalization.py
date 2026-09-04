#!/usr/bin/env python3
"""Scenarios Q,R,S,T,U,V: disagreement normalization / ledger / final
invariants via validate_artifact (library-level + one CLI integration)."""
from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys

PYTHON = "python3"  # NOT sys.executable (may be an embedded app host)
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_artifact  # noqa: E402

SCHEMAS_DIR = SCRIPTS.parent / "schemas"
AUDIT_COUNCIL = str(SCRIPTS / "audit_council.py")

from test_schema_validation import (  # noqa: E402
    cross_examination, final_findings, finding, independent_audit,
    ledger, load_schema,
)


def assert_schema_valid(testcase, doc, schema_name):
    errors = validate_artifact.validate(
        doc, load_schema(schema_name), base_dir=SCHEMAS_DIR)
    testcase.assertEqual(errors, [],
                         f"{schema_name} instance should validate: {errors}")


def cluster(cid="CLUSTER-001", members=("OPUS-001", "CODEX-001"),
            classification="CONSENSUS_CANDIDATE", status="CONSENSUS",
            **over):
    doc = {
        "cluster_id": cid,
        "initial_classification": classification,
        "status": status,
        "member_finding_ids": list(members),
        "positions": {
            "opus": {"position": "p"},
            "codex": {"position": "p"},
        },
    }
    doc.update(over)
    return doc


def final_finding(cid="CLUSTER-001", final_status="CONFIRMED",
                  origin=("OPUS-001", "CODEX-001"), prov_final="CONSENSUS",
                  adjudication=None, severity="HIGH"):
    return {
        "cluster_id": cid,
        "title": "finding",
        "severity": severity,
        "final_status": final_status,
        "claim": "c",
        "provenance": {
            "origin": list(origin),
            "final_status": prov_final,
            "adjudication": adjudication,
        },
        "evidence": [],
    }


class TestClusterDedup(unittest.TestCase):
    """Q/R: cluster + member dedup invariants (check_ledger_invariants)."""

    def test_valid_ledger_passes_invariants_and_schema(self):
        doc = ledger()
        assert_schema_valid(self, doc, "disagreement-ledger.schema.json")
        self.assertEqual(validate_artifact.check_ledger_invariants(doc), [])

    def test_same_finding_id_in_two_clusters_rejected(self):
        doc = {"clusters": [
            cluster("CLUSTER-001", members=("OPUS-001", "CODEX-001")),
            cluster("CLUSTER-002", members=("OPUS-001",)),
        ]}
        assert_schema_valid(self, doc, "disagreement-ledger.schema.json")
        errors = validate_artifact.check_ledger_invariants(doc)
        self.assertTrue(any("OPUS-001 appears in both" in e for e in errors),
                        errors)

    def test_duplicate_cluster_id_rejected(self):
        doc = {"clusters": [
            cluster("CLUSTER-001", members=("OPUS-001",)),
            cluster("CLUSTER-001", members=("CODEX-001",)),
        ]}
        errors = validate_artifact.check_ledger_invariants(doc)
        self.assertTrue(any("duplicate cluster id" in e for e in errors),
                        errors)

    def test_distinct_failure_modes_kept_separate_member_ids_unique(self):
        """Distinct failure modes must NOT be merged into one cluster; the
        enforceable structural form of that is: every member id unique across
        clusters (one origin finding lives in exactly one cluster)."""
        doc = {"clusters": [
            cluster("CLUSTER-001", members=("OPUS-001",),
                    classification="OPUS_ONLY", status="CONFIRMED_AFTER_CHALLENGE"),
            cluster("CLUSTER-002", members=("CODEX-001", "CODEX-002"),
                    classification="CODEX_ONLY", status="NARROWED"),
            cluster("CLUSTER-003", members=("OPUS-002", "CODEX-003"),
                    classification="CLAIM_CONFLICT", status="DISPUTED",
                    adjudication_eligible=True),
        ]}
        assert_schema_valid(self, doc, "disagreement-ledger.schema.json")
        self.assertEqual(validate_artifact.check_ledger_invariants(doc), [])


class TestDisagreementPreservation(unittest.TestCase):
    """S: a DISPUTED cluster survives into the final report as UNRESOLVED."""

    def test_disputed_cluster_survives_as_unresolved(self):
        led = {"clusters": [
            cluster("CLUSTER-001",
                    classification="CLAIM_CONFLICT", status="DISPUTED",
                    adjudication_eligible=True),
        ]}
        fin = final_findings()
        fin["findings"] = [
            final_finding("CLUSTER-001", final_status="UNRESOLVED",
                          prov_final="UNRESOLVED", adjudication="UNRESOLVED"),
        ]
        fin["unresolved_risks"] = [
            {"cluster_id": "CLUSTER-001", "severity": "HIGH",
             "note": "positions irreconcilable within budget"},
        ]
        assert_schema_valid(self, led, "disagreement-ledger.schema.json")
        assert_schema_valid(self, fin, "final-findings.schema.json")
        self.assertEqual(validate_artifact.check_final_invariants(fin), [])
        self.assertEqual(
            validate_artifact.check_late_findings(led, fin), [])
        # not silently dropped: the DISPUTED cluster is present in the final
        self.assertIn("CLUSTER-001",
                      [f["cluster_id"] for f in fin["findings"]])


class TestRejectedPlacement(unittest.TestCase):
    """T: REJECTED findings live only in the rejected appendix."""

    def test_rejected_only_in_appendix_passes(self):
        fin = final_findings()
        fin["findings"] = [final_finding("CLUSTER-001")]
        fin["rejected_appendix"] = [
            {"cluster_id": "CLUSTER-002", "title": "unfounded claim",
             "reason": "counter-evidence disproved the claim",
             "origin": ["CODEX-002"]},
        ]
        assert_schema_valid(self, fin, "final-findings.schema.json")
        self.assertEqual(validate_artifact.check_final_invariants(fin), [])

    def test_rejected_in_primary_findings_detected(self):
        fin = final_findings()
        fin["findings"] = [
            final_finding("CLUSTER-001"),
            # NOTE: provenance.final_status REJECTED is outside the schema
            # enum for primary findings; the invariant check still catches it
            # for defensively-handled inputs.
            dict(final_finding("CLUSTER-002", final_status="CONFIRMED"),
                 provenance={"origin": ["CODEX-002"],
                             "final_status": "REJECTED"}),
        ]
        errors = validate_artifact.check_final_invariants(fin)
        self.assertTrue(any("REJECTED in primary findings" in e
                            for e in errors), errors)

    def test_adjudication_rejected_without_appendix_entry_detected(self):
        fin = final_findings()
        fin["findings"] = [
            final_finding("CLUSTER-001", adjudication="REJECTED"),
        ]
        fin["rejected_appendix"] = []
        assert_schema_valid(self, fin, "final-findings.schema.json")
        errors = validate_artifact.check_final_invariants(fin)
        self.assertTrue(any("adjudication REJECTED" in e for e in errors),
                        errors)

    def test_cluster_in_both_primary_and_appendix_detected(self):
        fin = final_findings()
        fin["rejected_appendix"] = [
            {"cluster_id": "CLUSTER-001", "title": "dup", "reason": "r"},
        ]
        assert_schema_valid(self, fin, "final-findings.schema.json")
        errors = validate_artifact.check_final_invariants(fin)
        self.assertTrue(any("both primary findings and rejected_appendix"
                            in e for e in errors), errors)


class TestUnresolvedRisks(unittest.TestCase):
    """U: UNRESOLVED CRITICAL/HIGH clusters must surface as risks."""

    def test_unresolved_high_cluster_listed_passes(self):
        fin = final_findings()
        fin["findings"] = [
            final_finding("CLUSTER-001", final_status="UNRESOLVED",
                          prov_final="UNRESOLVED", severity="CRITICAL"),
        ]
        fin["unresolved_risks"] = [
            {"cluster_id": "CLUSTER-001", "severity": "CRITICAL"},
        ]
        assert_schema_valid(self, fin, "final-findings.schema.json")
        self.assertEqual(validate_artifact.check_final_invariants(fin), [])

    def test_risk_entry_without_unresolved_finding_detected(self):
        # implemented direction: a CRITICAL/HIGH unresolved_risks entry must
        # map to an UNRESOLVED finding
        fin = final_findings()
        fin["findings"] = [final_finding("CLUSTER-001")]
        fin["unresolved_risks"] = [
            {"cluster_id": "CLUSTER-009", "severity": "HIGH"},
        ]
        assert_schema_valid(self, fin, "final-findings.schema.json")
        errors = validate_artifact.check_final_invariants(fin)
        self.assertTrue(any("CLUSTER-009" in e for e in errors), errors)

    def test_medium_risk_entry_needs_no_unresolved_finding(self):
        fin = final_findings()
        fin["unresolved_risks"] = [
            {"cluster_id": "CLUSTER-009", "severity": "MEDIUM"},
        ]
        assert_schema_valid(self, fin, "final-findings.schema.json")
        self.assertEqual(validate_artifact.check_final_invariants(fin), [])

    def test_unresolved_high_finding_missing_from_risks_detected(self):
        # Forward direction of (U): an UNRESOLVED CRITICAL/HIGH finding
        # that is ABSENT from unresolved_risks must be rejected —
        # unresolved high-risk issues must stay explicitly visible.
        fin = final_findings()
        fin["findings"] = [
            final_finding("CLUSTER-001", final_status="UNRESOLVED",
                          prov_final="UNRESOLVED", severity="HIGH"),
        ]
        fin["unresolved_risks"] = []  # omission
        assert_schema_valid(self, fin, "final-findings.schema.json")
        errors = validate_artifact.check_final_invariants(fin)
        self.assertTrue(any("unresolved_risks" in e for e in errors),
                        msg=f"expected unresolved-risk omission error, got: {errors}")


class TestLateFindings(unittest.TestCase):
    """V: late findings must be validated by the other model or stay
    UNRESOLVED (check_late_findings)."""

    def _crossex_with_late(self, prov):
        doc = cross_examination()
        late = finding(id="CODEX-005", origin="CODEX-005",
                       status="PROVISIONAL", late_finding=True,
                       provenance=prov)
        doc["late_findings"] = [late]
        return doc

    def _final_promoting(self, final_status="CONFIRMED"):
        fin = final_findings()
        fin["findings"] = [
            final_finding("CLUSTER-004", final_status=final_status,
                          origin=("OPUS-001", "CODEX-005")),
        ]
        return fin

    def test_unvalidated_late_finding_promoted_detected(self):
        cex = self._crossex_with_late({"discovered_by": "CODEX"})
        fin = self._final_promoting("CONFIRMED")
        assert_schema_valid(self, cex, "cross-examination.schema.json")
        assert_schema_valid(self, fin, "final-findings.schema.json")
        errors = validate_artifact.check_late_findings(cex, fin)
        self.assertTrue(any("without" in e and "validated_by" in e
                            for e in errors), errors)

    def test_late_finding_validated_by_other_model_passes(self):
        cex = self._crossex_with_late({"discovered_by": "CODEX",
                                       "validated_by": "OPUS"})
        fin = self._final_promoting("CONFIRMED")
        assert_schema_valid(self, cex, "cross-examination.schema.json")
        assert_schema_valid(self, fin, "final-findings.schema.json")
        self.assertEqual(validate_artifact.check_late_findings(cex, fin), [])

    def test_late_finding_left_unresolved_passes(self):
        cex = self._crossex_with_late({"discovered_by": "CODEX"})
        fin = self._final_promoting("UNRESOLVED")
        fin["unresolved_risks"] = [
            {"cluster_id": "CLUSTER-004", "severity": "MEDIUM"},
        ]
        assert_schema_valid(self, fin, "final-findings.schema.json")
        self.assertEqual(validate_artifact.check_late_findings(cex, fin), [])

    def test_self_validated_late_finding_detected(self):
        # validated_by == discovered_by is NOT independent validation
        cex = self._crossex_with_late({"discovered_by": "CODEX",
                                       "validated_by": "CODEX"})
        fin = self._final_promoting("CONFIRMED")
        errors = validate_artifact.check_late_findings(cex, fin)
        self.assertTrue(any("equals discovered_by" in e for e in errors),
                        errors)

    def test_non_late_origins_untouched(self):
        cex = self._crossex_with_late({"discovered_by": "CODEX"})
        fin = final_findings()  # promotes only OPUS-001/CODEX-001
        assert_schema_valid(self, fin, "final-findings.schema.json")
        self.assertEqual(validate_artifact.check_late_findings(cex, fin), [])


class TestLedgerAdvanceIntegration(unittest.TestCase):
    """End-to-end: advance --to LEDGER_COMPLETE runs the dedup invariant."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        repo = os.path.join(self._tmp.name, "repo")
        os.makedirs(repo)
        for args in (["init", "-q", "-b", "main"],
                     ["config", "user.email", "t@example.com"],
                     ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", repo, *args], check=True,
                           capture_output=True)
        with open(os.path.join(repo, "src.py"), "w") as fh:
            fh.write("VALUE = 1\n")
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True,
                       capture_output=True)
        subprocess.run(["git", "-C", repo, "commit", "-q", "-m", "i"],
                       check=True, capture_output=True)
        self.repo = repo
        brief = os.path.join(self._tmp.name, "brief.md")
        with open(brief, "w") as fh:
            fh.write("# brief\n")
        proc = self._cli("init-run", "--repo", repo, "--brief", brief)
        assert proc.returncode == 0, proc.stdout
        pat = re.compile(r"audit-output/audit-council/"
                         r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}\s*$")
        self.run_dir = next(line for line in proc.stdout.decode().splitlines()
                            if pat.search(line)).strip()

    def tearDown(self):
        self._tmp.cleanup()

    def _cli(self, *args, stdin_doc=None):
        data = None if stdin_doc is None else json.dumps(stdin_doc).encode()
        return subprocess.run([PYTHON, AUDIT_COUNCIL, *args], input=data,
                              capture_output=True, check=False)

    def _opus_cex(self):
        doc = cross_examination()
        doc["examiner"], doc["examined"] = "OPUS", "CODEX"
        doc["late_findings"] = [
            finding(id="OPUS-009", origin="OPUS-009", late_finding=True,
                    provenance={"discovered_by": "OPUS"})
        ]
        return doc

    def _run_fingerprint(self):
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        return state["repo_fingerprint_sha256"]

    def _walk_to_cross_exam_complete(self):
        from test_schema_validation import contract
        fp = self._run_fingerprint()
        c = contract()
        # v2 A0.6: contract root/head must match the frozen binding
        binding = json.load(open(os.path.join(
            self.run_dir, "01-environment-binding.json")))
        c["target_repository"]["root"] = binding["repo_root_realpath"]
        c["target_repository"]["head_sha"] = binding["head_sha"]
        c["target_repository"]["fingerprint_sha256"] = fp
        opus = independent_audit()
        opus["repository_fingerprint_sha256"] = fp
        codex = independent_audit(model="gpt-5.6-sol")
        codex["repository_fingerprint_sha256"] = fp
        steps = [
            ("freeze-contract", ["--contract", "-", "--stdin"], c),
            ("advance", ["--to", "OPUS_INDEPENDENT_COMPLETE",
                         "--artifact", "-", "--stdin"],
             opus),
            ("advance", ["--to", "CODEX_INDEPENDENT_COMPLETE",
                         "--artifact", "-", "--stdin"],
             codex),
            ("advance", ["--to", "NORMALIZED", "--artifact", "-", "--stdin"],
             {"clusters": []}),
            ("advance", ["--to", "OPUS_CROSS_EXAM_COMPLETE",
                         "--artifact", "-", "--stdin"], self._opus_cex()),
            ("advance", ["--to", "CODEX_CROSS_EXAM_COMPLETE",
                         "--artifact", "-", "--stdin"],
             cross_examination()),
        ]
        for cmd, extra, doc in steps:
            proc = self._cli(cmd, "--run", self.run_dir, *extra,
                             stdin_doc=doc)
            assert proc.returncode == 0, (cmd, proc.stdout, proc.stderr)

    def test_ledger_with_duplicate_member_rejected_by_advance(self):
        self._walk_to_cross_exam_complete()
        bad = {"clusters": [
            cluster("CLUSTER-001", members=("OPUS-001", "CODEX-001")),
            cluster("CLUSTER-002", members=("OPUS-001",)),
        ]}
        proc = self._cli("advance", "--run", self.run_dir,
                          "--to", "LEDGER_COMPLETE",
                          "--artifact", "-", "--stdin", stdin_doc=bad)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("OPUS-001 appears in both", proc.stdout.decode())

    def test_valid_ledger_advances(self):
        self._walk_to_cross_exam_complete()
        proc = self._cli("advance", "--run", self.run_dir,
                         "--to", "LEDGER_COMPLETE",
                         "--artifact", "-", "--stdin", stdin_doc=ledger())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["phase"], "LEDGER_COMPLETE")


if __name__ == "__main__":
    unittest.main()
