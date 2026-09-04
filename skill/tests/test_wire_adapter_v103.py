"""v1.0.3 Defect 1 — strict-wire/canonical adapter regression tests.

The canonical schema is authoritative; the OpenAI/Codex strict wire schema is
a mechanical projection. Canonically OPTIONAL properties are nullable on the
wire (null = absent); wire_to_canonical is schema-aware, never a blind
strip-nulls pass; canonical validation remains the final authority.
"""
from __future__ import annotations

import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
SCHEMAS = os.path.join(HERE, "..", "schemas")
sys.path.insert(0, SCRIPTS)

import wire_adapter as wa  # noqa: E402

import validate_artifact as va  # noqa: E402


def canon(name):
    with open(os.path.join(SCHEMAS, name)) as f:
        return json.load(f)


def validate(instance, schema_name):
    return va.validate(instance, canon(schema_name))


EVIDENCE_ITEMS = {"items": canon("finding.schema.json")["properties"]
                  ["evidence"]["items"]}


def wire_of(schema_doc):
    return wa.canonical_to_wire(schema_doc, SCHEMAS)


def normalize(instance, schema_doc):
    return wa.wire_to_canonical(instance, schema_doc, SCHEMAS)


class TestWireProjection(unittest.TestCase):
    """canonical -> wire projection shape."""

    def test_optional_string_nullable_and_required_on_wire(self):
        wire = wire_of(canon("finding.schema.json"))
        ev = wire["properties"]["evidence"]["items"]
        # v2: typed line_ranges array (minimum/maxItems dropped on the
        # wire; canonical validation re-imposes them)
        self.assertEqual(
            ev["properties"]["line_ranges"],
            {"anyOf": [
                {"type": "array",
                 "items": {"type": "object",
                           "additionalProperties": False,
                           "required": ["end", "start"],
                           "properties": {"start": {"type": "integer"},
                                          "end": {"type": "integer"}}}},
                {"type": "null"}]})
        self.assertIn("line_ranges", ev["required"])  # strict outputs demand it
        self.assertFalse(ev.get("additionalProperties", True) is not False)
        self.assertNotIn("lines", ev["properties"])  # legacy key gone in v2

    def test_required_non_nullable_stays_non_nullable(self):
        wire = wire_of(canon("finding.schema.json"))
        self.assertEqual(wire["properties"]["id"]["type"], "string")
        self.assertIn("id", wire["required"])
        self.assertNotIn("anyOf", wire["properties"]["id"])

    def test_adjudication_wire_keeps_required_cluster_id(self):
        # v1.0.3 review F1: the cluster_id drop must be scoped to finding
        # containers; rounds[].cluster_id is canonically REQUIRED. Mirror
        # the runner's build_codex_schema projection (projection + scoped
        # drop) rather than the bare canonical_to_wire output.
        wire = wire_of(canon("adjudication.schema.json"))
        wa.drop_wire_property_under(
            wire, "cluster_id", ("findings", "late_findings"))
        item = wire["properties"]["rounds"]["items"]
        self.assertIn("cluster_id", item["properties"])
        self.assertIn("cluster_id", item["required"])
        # ...while findings/late_findings containers drop it
        fw = wire_of(canon("independent-audit.schema.json"))
        wa.drop_wire_property_under(
            fw, "cluster_id", ("findings", "late_findings"))
        finding = fw["properties"]["findings"]["items"]
        self.assertNotIn("cluster_id", finding["properties"])
        self.assertNotIn("cluster_id", finding.get("required", []))
        # cross-examination late_findings also drop it
        cw = wire_of(canon("cross-examination.schema.json"))
        wa.drop_wire_property_under(
            cw, "cluster_id", ("findings", "late_findings"))
        lf_branch = cw["properties"]["late_findings"]["anyOf"][0]
        lf = lf_branch["items"]
        self.assertNotIn("cluster_id", lf["properties"])

    def test_canonically_nullable_enum_stays_nullable(self):
        wire = wire_of(canon("finding.schema.json"))
        prov = wire["properties"]["provenance"]["properties"]["challenge_result"]
        self.assertIn({"type": "null"}, prov["anyOf"])


class TestWireToCanonical(unittest.TestCase):

    def _ev(self, **over):
        d = {"kind": "OBSERVED_FACT", "path": "a.py",
             "line_ranges": [{"start": 1, "end": 2}],
             "description": "d"}
        d.update(over)
        return d

    def _finding(self, evidence):
        return {"id": "CODEX-001", "origin": "CODEX-001", "title": "t",
                "category": "c", "severity": "LOW", "confidence": "LOW",
                "claim": "c", "status": "PROVISIONAL", "evidence": evidence,
                "provenance": {"discovered_by": "CODEX"}}

    def _audit(self, evidence):
        return {"model": "gpt-5.6-sol",
                "repository_fingerprint_sha256": "d" * 64,
                "audit_summary": "s",
                "findings": [self._finding(evidence)]}

    def test_optional_null_omitted_and_canonical_passes(self):
        doc = self._audit([self._ev(line_ranges=None)])  # requirement-only evidence
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        self.assertNotIn("line_ranges", cand["findings"][0]["evidence"][0])
        self.assertEqual(validate(cand, "independent-audit.schema.json"), [])

    def test_optional_valid_non_null_value_preserved(self):
        doc = self._audit([self._ev(line_ranges=[{"start": 40, "end": 52}])])
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        self.assertEqual(cand["findings"][0]["evidence"][0]["line_ranges"],
                         [{"start": 40, "end": 52}])
        self.assertEqual(validate(cand, "independent-audit.schema.json"), [])

    def test_empty_string_sentinel_fails_canonical(self):
        # Benchmark-001 empty sentinel: still invalid in v2 — differently,
        # the legacy `lines` key itself is rejected (zero ranges are
        # expressed by omitting line_ranges or emitting null)
        doc = self._audit([self._ev(lines="")])
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])  # normalization is not the judge...
        errors = validate(cand, "independent-audit.schema.json")
        self.assertTrue(any("lines" in e for e in errors), errors)

    def test_malformed_range_fails_canonical(self):
        doc = self._audit([self._ev(lines="325-343, 488-547")])  # benchmark case
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        errors = validate(cand, "independent-audit.schema.json")
        self.assertTrue(any("additional property" in e for e in errors),
                        errors)

    def test_required_non_null_receiving_null_fails_closed(self):
        doc = self._audit([self._ev()])
        doc["findings"][0]["id"] = None  # id is required non-nullable
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertTrue(any("required non-nullable" in e for e in errs), errs)
        # kept in the candidate so canonical validation also rejects it
        self.assertIsNone(cand["findings"][0]["id"])
        self.assertTrue(validate(cand, "independent-audit.schema.json"))

    def test_canonically_nullable_required_null_preserved(self):
        # state.codex.session_id is REQUIRED and nullable (type incl. null)
        state = {"schema_version": 1, "run_id": "20260903T000000Z-ab01cd",
                 "phase": "CREATED", "completeness_state": "RUNNING",
                 "created_at": "2026-09-03T00:00:00Z", "timestamps": {},
                 "repo_fingerprint_sha256": "d" * 64,
                 "codex": {"session_id": None, "jobs": [],
                           "stage_counts": {"independent": 0,
                                            "cross_examination": 0,
                                            "adjudication": 0}},
                 "phase_attempts": {}, "failure_reason": None,
                 "adjudication_skipped": False}
        cand, errs = normalize(state, canon("state.schema.json"))
        self.assertEqual(errs, [])
        self.assertIsNone(cand["codex"]["session_id"])  # preserved, not dropped
        self.assertEqual(validate(cand, "state.schema.json"), [])

    def test_nested_optional_null_in_object(self):
        prov = {"discovered_by": "CODEX", "challenged_by": None,
                "challenge_result": None}
        doc = self._audit([self._ev()])
        doc["findings"][0]["provenance"] = prov
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        p = cand["findings"][0]["provenance"]
        self.assertNotIn("challenged_by", p)
        self.assertNotIn("challenge_result", p)
        self.assertEqual(validate(cand, "independent-audit.schema.json"), [])

    def test_optional_null_inside_array_item(self):
        doc = self._audit([self._ev(symbol=None, test_ref=None)])
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        ev = cand["findings"][0]["evidence"][0]
        self.assertNotIn("symbol", ev)
        self.assertNotIn("test_ref", ev)
        self.assertEqual(validate(cand, "independent-audit.schema.json"), [])

    def test_multiple_nesting_levels(self):
        doc = self._audit([self._ev(), self._ev(line_ranges=None, symbol=None)])
        doc["requirement_coverage"] = [{"requirement": "r", "covered": True,
                                        "note": None}]
        doc["limitations"] = None  # optional top-level array
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        self.assertNotIn("limitations", cand)
        self.assertNotIn("note", cand["requirement_coverage"][0])
        self.assertNotIn("line_ranges", cand["findings"][0]["evidence"][1])
        self.assertEqual(validate(cand, "independent-audit.schema.json"), [])

    def test_additional_properties_false_still_enforced(self):
        doc = self._audit([self._ev(bogus_extra="x")])
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])  # unknown keys pass through untouched...
        self.assertIn("bogus_extra", cand["findings"][0]["evidence"][0])
        # ...and the canonical validator rejects them
        self.assertTrue(validate(cand, "independent-audit.schema.json"))

    def test_no_defaults_invented(self):
        doc = self._audit([self._ev(line_ranges=None, symbol=None,
                                    requirement_refs=None,
                                    counter_evidence=None)])
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        f = cand["findings"][0]
        self.assertNotIn("symbol", f["evidence"][0])
        self.assertNotIn("requirement_refs", f)
        self.assertNotIn("counter_evidence", f)
        # no fabricated "", [], {}, 0, false anywhere for the omitted keys
        dumped = json.dumps(cand)
        self.assertNotIn('"line_ranges": []', dumped)

    def test_wire_null_on_required_non_nullable_not_silently_removed(self):
        doc = self._audit([self._ev()])
        doc["findings"][0]["claim"] = None
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertTrue(any("claim" in e for e in errs))
        self.assertIsNone(cand["findings"][0]["claim"])

    def test_cross_examination_requirement_evidence_canonicalizes(self):
        crossex = {"examiner": "CODEX", "examined": "OPUS", "challenges": [
            {"target_finding_id": "OPUS-001", "verdict": "CONFIRMED",
             "counter_evidence": [{"kind": "REQUIREMENT_CLAIM",
                                   "path": "spec.md", "line_ranges": None,
                                   "description": "requirement"}],
             "reasoning_summary": "r",
             "severity_recalibration": None}]}
        cand, errs = normalize(crossex, canon("cross-examination.schema.json"))
        self.assertEqual(errs, [])
        ch = cand["challenges"][0]
        self.assertNotIn("line_ranges", ch["counter_evidence"][0])
        self.assertNotIn("severity_recalibration", ch)  # optional null dropped
        self.assertEqual(validate(cand, "cross-examination.schema.json"), [])

    def test_non_null_invalid_value_still_rejected_after_wire_drop(self):
        # wire schema omits `minimum`; canonical validator re-imposes it
        # (zero start: valid on the strict wire, invalid canonically)
        doc = self._audit([self._ev(line_ranges=[{"start": 0, "end": 3}])])
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        self.assertTrue(validate(cand, "independent-audit.schema.json"))

    def test_canonical_fixtures_unaffected_by_round_trip(self):
        # a canonical-valid document must survive normalization unchanged
        doc = self._audit([self._ev()])
        cand, errs = normalize(doc, canon("independent-audit.schema.json"))
        self.assertEqual(errs, [])
        self.assertEqual(cand, doc)


if __name__ == "__main__":
    unittest.main()
