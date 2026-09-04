#!/usr/bin/env python3
"""PKG-SCHEMA (pillar G) — typed multi-range evidence model v2 (schema_version 2).

Replaces the single-range string evidence field `lines` with typed
multi-range `line_ranges` in all five finding-bearing canonical schemas
(8 inline evidence-shaped locations), plus the deterministic v1->v2
migration reader (evidence_migration).

Authority split (ARCHITECTURE §3.4.3): the minimal validator's keyword
subset cannot express `end >= start`, so canonical validation and
normalize_ranges TOGETHER are the authority for range semantics; the
schema itself enforces integer type, minimum 1, maxItems 32, strict
range objects (additionalProperties: false), and rejection of the legacy
`lines` key (removed from every v2 evidence location).
"""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
SCHEMAS = HERE.parent / "schemas"
FIXTURES = HERE / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import render_report  # noqa: E402
import validate_artifact  # noqa: E402
import wire_adapter  # noqa: E402

import evidence_migration as em  # noqa: E402

FIFTH_WIRE = FIXTURES / "fifth-cross-exam-wire.json"
FIFTH_OPUS_V1 = FIXTURES / "fifth-opus-independent-v1.json"

# The exact Fifth-run disjoint pair (ARCHITECTURE §2.1).
DISJOINT = [{"start": 184, "end": 185}, {"start": 240, "end": 273}]

LINE_RANGES_DEF = {
    "type": "array",
    "maxItems": 32,
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["start", "end"],
        "properties": {
            "start": {"type": "integer", "minimum": 1},
            "end": {"type": "integer", "minimum": 1},
        },
    },
}


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def validate(instance, schema_name: str) -> list[str]:
    return validate_artifact.validate(
        instance, load_schema(schema_name), base_dir=SCHEMAS)


# ---------------------------------------------------------------------------
# minimal valid documents per schema, parameterized at the evidence location
# under test
# ---------------------------------------------------------------------------
def finding_doc(evidence=None, counter_evidence=None):
    doc = {
        "id": "OPUS-001", "origin": "OPUS-001", "title": "t",
        "category": "c", "severity": "HIGH", "confidence": "MEDIUM",
        "claim": "c", "status": "PROVISIONAL",
        "evidence": [{"kind": "OBSERVED_FACT"}] if evidence is None
        else evidence,
        "provenance": {"discovered_by": "OPUS"},
    }
    if counter_evidence is not None:
        doc["counter_evidence"] = counter_evidence
    return doc


def cross_exam_doc(counter_evidence):
    return {"examiner": "CODEX", "examined": "OPUS", "challenges": [
        {"target_finding_id": "OPUS-001", "verdict": "CONFIRMED",
         "counter_evidence": counter_evidence,
         "reasoning_summary": "r"}]}


def ledger_doc(counter_evidence):
    return {"clusters": [{
        "cluster_id": "CLUSTER-001",
        "initial_classification": "CONSENSUS_CANDIDATE",
        "status": "CONSENSUS",
        "member_finding_ids": ["OPUS-001", "CODEX-001"],
        "positions": {"opus": {"position": "p"},
                      "codex": {"position": "p"}},
        "counter_evidence": counter_evidence}]}


def adjudication_doc(evidence=None, counter_evidence=None):
    packet = {"claim": "c"}
    if evidence is not None:
        packet["evidence"] = evidence
    if counter_evidence is not None:
        packet["counter_evidence"] = counter_evidence
    return {"rounds": [{
        "cluster_id": "CLUSTER-001", "evidence_packet": packet,
        "opus_verdict": "CONFIRMED", "codex_verdict": "CONFIRMED",
        "final_status": "CONFIRMED", "rationale": "r"}]}


def final_doc(evidence=None, counter_evidence=None):
    f = {
        "cluster_id": "CLUSTER-001", "title": "t", "severity": "HIGH",
        "final_status": "CONFIRMED", "claim": "c",
        "provenance": {"origin": ["OPUS-001"], "final_status": "CONSENSUS"},
        "evidence": [] if evidence is None else evidence,
    }
    if counter_evidence is not None:
        f["counter_evidence"] = counter_evidence
    return {
        "completeness_state": "COMPLETE",
        "repository_fingerprint_sha256": "ab" * 32,
        "executive_summary": "s",
        "findings": [f],
    }


def all_five_locations(item):
    """(schema, instance, human path) pairs placing `item` at each schema's
    respective evidence/counter_evidence location."""
    return [
        ("finding.schema.json", finding_doc(evidence=[item]),
         "finding.evidence"),
        ("finding.schema.json", finding_doc(counter_evidence=[item]),
         "finding.counter_evidence"),
        ("cross-examination.schema.json",
         cross_exam_doc(counter_evidence=[item]),
         "challenges[].counter_evidence"),
        ("disagreement-ledger.schema.json",
         ledger_doc(counter_evidence=[item]),
         "clusters[].counter_evidence"),
        ("adjudication.schema.json",
         adjudication_doc(evidence=[item]),
         "evidence_packet.evidence"),
        ("adjudication.schema.json",
         adjudication_doc(counter_evidence=[item]),
         "evidence_packet.counter_evidence"),
        ("final-findings.schema.json", final_doc(evidence=[item]),
         "findings[].evidence"),
        ("final-findings.schema.json", final_doc(counter_evidence=[item]),
         "findings[].counter_evidence"),
    ]


# ---------------------------------------------------------------------------
# Task G.1 — typed line_ranges in all five schemas
# ---------------------------------------------------------------------------
class TestLineRangesSchemas(unittest.TestCase):

    def test_line_ranges_definition_present_at_all_eight_locations(self):
        for name in ("finding.schema.json", "cross-examination.schema.json",
                     "disagreement-ledger.schema.json",
                     "adjudication.schema.json", "final-findings.schema.json"):
            raw = (SCHEMAS / name).read_text(encoding="utf-8")
            with self.subTest(schema=name):
                self.assertNotIn('"lines"', raw,
                                 "legacy lines property must be gone")
                self.assertIn('"line_ranges"', raw)

    def test_zero_ranges_valid(self):
        # requirement-level evidence: no line_ranges at all
        errors = validate(finding_doc(evidence=[
            {"kind": "REQUIREMENT_CLAIM", "requirement_ref": "REQ-1"}]),
            "finding.schema.json")
        self.assertEqual(errors, [])
        # explicit empty array is the same zero-range statement
        errors = validate(finding_doc(evidence=[
            {"kind": "REQUIREMENT_CLAIM", "line_ranges": []}]),
            "finding.schema.json")
        self.assertEqual(errors, [])

    def test_one_range_valid(self):
        one = [{"start": 184, "end": 184}]
        for schema, instance, loc in all_five_locations(
                {"kind": "OBSERVED_FACT", "line_ranges": one}):
            with self.subTest(schema=schema, location=loc):
                self.assertEqual(validate(instance, schema), [])

    def test_many_disjoint_valid(self):
        # the exact Fifth-run disjoint pair must validate in ALL FIVE
        # schemas at their respective evidence locations
        for schema, instance, loc in all_five_locations(
                {"kind": "OBSERVED_FACT", "line_ranges": DISJOINT}):
            with self.subTest(schema=schema, location=loc):
                self.assertEqual(validate(instance, schema), [])

    def test_reversed_rejected(self):
        # end >= start is NOT expressible in the validator's keyword subset:
        # canonical validation alone stays silent (documented limitation) and
        # normalize_ranges is the second half of the authority.
        reversed_range = [{"start": 5, "end": 3}]
        errors = validate(finding_doc(evidence=[
            {"kind": "OBSERVED_FACT", "line_ranges": reversed_range}]),
            "finding.schema.json")
        self.assertEqual(
            errors, [],
            "schema alone cannot express end>=start; normalization is "
            "the co-authority (ARCHITECTURE §3.4.3)")
        with self.assertRaises(em.MigrationError):
            em.normalize_ranges(reversed_range)

    def test_zero_start_rejected(self):
        errors = validate(finding_doc(evidence=[
            {"kind": "OBSERVED_FACT",
             "line_ranges": [{"start": 0, "end": 3}]}]),
            "finding.schema.json")
        self.assertTrue(errors, "start below minimum 1 must be rejected")
        self.assertTrue(any("minimum" in e for e in errors), errors)
        with self.assertRaises(em.MigrationError):
            em.normalize_ranges([{"start": 0, "end": 3}])

    def test_float_rejected(self):
        errors = validate(finding_doc(evidence=[
            {"kind": "OBSERVED_FACT",
             "line_ranges": [{"start": 1.5, "end": 2}]}]),
            "finding.schema.json")
        self.assertTrue(any("expected type integer" in e for e in errors),
                        errors)
        with self.assertRaises(em.MigrationError):
            em.normalize_ranges([{"start": 1.5, "end": 2}])

    def test_extra_key_rejected(self):
        for schema, instance, loc in all_five_locations(
                {"kind": "OBSERVED_FACT",
                 "line_ranges": [{"start": 1, "end": 2, "note": "x"}]}):
            with self.subTest(schema=schema, location=loc):
                errors = validate(instance, schema)
                self.assertTrue(
                    any("additional property" in e for e in errors), errors)
        with self.assertRaises(em.MigrationError):
            em.normalize_ranges([{"start": 1, "end": 2, "note": "x"}])

    def test_over_maxitems_rejected(self):
        thirty_three = [{"start": i, "end": i} for i in range(1, 34)]
        self.assertEqual(len(thirty_three), 33)
        errors = validate(finding_doc(evidence=[
            {"kind": "OBSERVED_FACT", "line_ranges": thirty_three}]),
            "finding.schema.json")
        self.assertTrue(any("more than 32 items" in e for e in errors),
                        errors)

    def test_legacy_lines_string_rejected_in_v2(self):
        # v2 accepts only line_ranges; a legacy lines string is an unknown
        # property (additionalProperties: false on the evidence item)
        for schema, instance, loc in all_five_locations(
                {"kind": "OBSERVED_FACT", "lines": "184-185"}):
            with self.subTest(schema=schema, location=loc):
                errors = validate(instance, schema)
                self.assertTrue(
                    any("lines" in e and "additional property" in e
                        for e in errors), errors)


# ---------------------------------------------------------------------------
# Task G.2 — migration reader (lines_to_ranges / normalize_ranges)
# ---------------------------------------------------------------------------
class TestLinesToRanges(unittest.TestCase):

    def test_single_line(self):
        self.assertEqual(em.lines_to_ranges("184"),
                         [{"start": 184, "end": 184}])

    def test_single_range(self):
        self.assertEqual(em.lines_to_ranges("184-185"),
                         [{"start": 184, "end": 185}])

    def test_error_on_exact_fifth_multi_range(self):
        # the Fifth-run value that killed cross-examination stays an error:
        # comma-separated parsing is forbidden, ever
        with self.assertRaises(em.MigrationError):
            em.lines_to_ranges("184-185, 240-273")

    def test_error_on_other_shapes(self):
        for bad in ("325-343, 488-547",  # benchmark comma list
                    "",                  # Benchmark-001 empty sentinel
                    "185-184",           # reversed
                    "0-3", "0",          # zero
                    " 184", "184 ", "1 -2",  # whitespace
                    "garbage", "-5", "5-", "184-185-190", "1,2", "L14"):
            with self.subTest(value=bad):
                with self.assertRaises(em.MigrationError):
                    em.lines_to_ranges(bad)

    def test_migration_error_is_value_error(self):
        self.assertTrue(issubclass(em.MigrationError, ValueError))


class TestNormalizeRanges(unittest.TestCase):

    def test_sorts_by_start_then_end(self):
        self.assertEqual(
            em.normalize_ranges([{"start": 240, "end": 273},
                                 {"start": 184, "end": 185}]),
            [{"start": 184, "end": 185}, {"start": 240, "end": 273}])
        # same start, different end: narrower first
        self.assertEqual(
            em.normalize_ranges([{"start": 1, "end": 9},
                                 {"start": 1, "end": 2}]),
            [{"start": 1, "end": 2}, {"start": 1, "end": 9}])

    def test_returns_new_list_and_dicts(self):
        src = [{"start": 240, "end": 273}, {"start": 184, "end": 185}]
        snapshot = [dict(r) for r in src]
        out = em.normalize_ranges(src)
        self.assertIsNot(out, src)
        self.assertEqual(src, snapshot)  # input untouched
        self.assertIsNot(out[0], src[1])

    def test_empty_list_ok(self):
        self.assertEqual(em.normalize_ranges([]), [])

    def test_rejects_invalid_members(self):
        for bad in ([{"start": 5, "end": 3}],          # reversed
                    [{"start": 0, "end": 3}],          # below 1
                    [{"start": 1.5, "end": 2}],        # float
                    [{"start": True, "end": 2}],       # bool is not int
                    [{"start": "1", "end": 2}],        # string
                    [{"start": 1}],                    # missing end
                    [{"start": 1, "end": 2, "x": 0}],  # extra key
                    ["not-a-dict"], "not-a-list"):
            with self.subTest(value=bad):
                with self.assertRaises(em.MigrationError):
                    em.normalize_ranges(bad)


# ---------------------------------------------------------------------------
# Task G.2 — migrate_artifact + is_v1_artifact (Fifth fixture)
# ---------------------------------------------------------------------------
class TestMigrateArtifact(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.raw_v1 = FIFTH_OPUS_V1.read_bytes()
        cls.doc_v1 = json.loads(cls.raw_v1)

    def test_fifth_opus_v1_converts_all_evidence_items(self):
        migrated = em.migrate_artifact(self.doc_v1)
        self.assertFalse(em.is_v1_artifact(migrated))
        converted = []

        def count(node):
            if isinstance(node, dict):
                if "line_ranges" in node:
                    converted.append(node["line_ranges"])
                for v in node.values():
                    count(v)
            elif isinstance(node, list):
                for x in node:
                    count(x)

        count(migrated)
        # every one of the Fifth's 19 legacy `lines` fields became typed
        self.assertEqual(len(converted), 19)
        self.assertTrue(all(isinstance(r, list) and r for r in converted))

    def test_migrate_returns_new_dict_source_unchanged(self):
        snapshot = json.loads(self.raw_v1)
        migrated = em.migrate_artifact(self.doc_v1)
        self.assertIsNot(migrated, self.doc_v1)
        self.assertEqual(self.doc_v1, snapshot)
        # and the on-disk copy's bytes are never rewritten by any API
        self.assertEqual(FIFTH_OPUS_V1.read_bytes(), self.raw_v1)

    def test_migrated_fifth_doc_is_canonically_valid(self):
        migrated = em.migrate_artifact(self.doc_v1)
        self.assertEqual(
            validate(migrated, "independent-audit.schema.json"), [])

    def test_idempotent(self):
        once = em.migrate_artifact(self.doc_v1)
        twice = em.migrate_artifact(once)
        self.assertEqual(twice, once)
        self.assertIsNot(twice, once)

    def test_walks_nested_dicts_and_lists(self):
        doc = {"findings": [{"evidence": [{"lines": "7"}],
                             "counter_evidence": [{"lines": "8-9"}]}],
               "extra": [{"deep": {"lines": "10"}}]}
        migrated = em.migrate_artifact(doc)
        self.assertEqual(migrated["findings"][0]["evidence"][0],
                         {"line_ranges": [{"start": 7, "end": 7}]})
        self.assertEqual(migrated["findings"][0]["counter_evidence"][0],
                         {"line_ranges": [{"start": 8, "end": 9}]})
        self.assertEqual(migrated["extra"][0]["deep"],
                         {"line_ranges": [{"start": 10, "end": 10}]})
        # unknown keys around the walk are preserved
        self.assertIn("findings", migrated)

    def test_multi_range_string_raises(self):
        doc = {"challenges": [{"counter_evidence": [
            {"lines": "184-185, 240-273"}]}]}
        with self.assertRaises(em.MigrationError):
            em.migrate_artifact(doc)

    def test_non_string_lines_raises(self):
        with self.assertRaises(em.MigrationError):
            em.migrate_artifact({"evidence": [{"lines": None}]})


class TestIsV1Artifact(unittest.TestCase):

    def test_fifth_fixture_is_v1(self):
        self.assertTrue(
            em.is_v1_artifact(json.loads(FIFTH_OPUS_V1.read_bytes())))

    def test_migrated_is_not_v1(self):
        doc = em.migrate_artifact(
            json.loads(FIFTH_OPUS_V1.read_bytes()))
        self.assertFalse(em.is_v1_artifact(doc))

    def test_nested_and_empty(self):
        self.assertTrue(em.is_v1_artifact({"a": [{"b": {"lines": "1"}}]}))
        self.assertFalse(em.is_v1_artifact({"a": [{"b": {"line_ranges": [
            {"start": 1, "end": 1}]}}]}))
        self.assertFalse(em.is_v1_artifact({}))


# ---------------------------------------------------------------------------
# Task G.3 — wire path end-to-end (exact Fifth regression)
# ---------------------------------------------------------------------------
def _to_wire_value(value):
    """Manual lines->line_ranges conversion for the fixture copy: single
    ranges via lines_to_ranges semantics; the one exact Fifth multi-range
    value becomes the two-range list per ARCHITECTURE §2.1/§3.4.3."""
    if value is None:
        return None
    if value == "184-185, 240-273":
        return [{"start": 184, "end": 185}, {"start": 240, "end": 273}]
    if value.isdigit():
        return [{"start": int(value), "end": int(value)}]
    left, dash, right = value.partition("-")
    assert dash and left.isdigit() and right.isdigit(), value
    return [{"start": int(left), "end": int(right)}]


def _converted_wire_doc():
    doc = json.loads(FIFTH_WIRE.read_bytes())
    replaced = []

    def walk(node):
        if isinstance(node, dict):
            out = {}
            for k, v in node.items():
                if k == "lines":
                    replaced.append(v)
                    out["line_ranges"] = _to_wire_value(v)
                else:
                    out[k] = walk(v)
            return out
        if isinstance(node, list):
            return [walk(x) for x in node]
        return node

    return walk(doc), replaced


class TestFifthWireRegression(unittest.TestCase):

    def test_wire_schema_contains_strict_line_ranges(self):
        wire = wire_adapter.canonical_to_wire(
            load_schema("cross-examination.schema.json"), str(SCHEMAS))
        counter_ev = (wire["properties"]["challenges"]["items"]
                      ["properties"]["counter_evidence"])
        # counter_evidence is canonically optional -> nullable on the wire
        ev = counter_ev["anyOf"][0]["items"]["properties"]
        self.assertIn("line_ranges", ev)
        self.assertNotIn("lines", ev)
        lr = ev["line_ranges"]
        # optional canonical property -> nullable on the wire
        self.assertEqual(lr["anyOf"][1], {"type": "null"})
        branch = lr["anyOf"][0]
        self.assertEqual(branch["type"], "array")
        item = branch["items"]
        self.assertEqual(item["type"], "object")
        self.assertIs(item["additionalProperties"], False)
        self.assertEqual(sorted(item["required"]), ["end", "start"])
        self.assertEqual(
            item["properties"],
            {"start": {"type": "integer"}, "end": {"type": "integer"}})

    def test_fifth_multi_range_document_now_validates_end_to_end(self):
        # this exact document failed v1 (comma string rejected by the
        # single-range pattern); with typed line_ranges it must PASS
        doc, replaced = _converted_wire_doc()
        self.assertEqual(len(replaced), 43)
        self.assertIn("184-185, 240-273", replaced)  # the killer value
        self.assertIn(None, replaced)                # wire nulls present
        candidate, errs = wire_adapter.wire_to_canonical(
            doc, load_schema("cross-examination.schema.json"), str(SCHEMAS))
        self.assertEqual(errs, [])
        self.assertEqual(
            validate_artifact.validate(
                candidate, load_schema("cross-examination.schema.json"),
                base_dir=SCHEMAS),
            [],
            "the Fifth cross-examination payload with typed line_ranges "
            "must be canonically valid end-to-end")

    def test_doc_still_carrying_legacy_lines_fails_v2_canonical(self):
        doc, _ = _converted_wire_doc()
        doc["challenges"][0]["counter_evidence"][0]["lines"] = "507-514"
        candidate, errs = wire_adapter.wire_to_canonical(
            doc, load_schema("cross-examination.schema.json"), str(SCHEMAS))
        self.assertEqual(errs, [])
        errors = validate_artifact.validate(
            candidate, load_schema("cross-examination.schema.json"),
            base_dir=SCHEMAS)
        self.assertTrue(
            any("lines" in e and "additional property" in e
                for e in errors), errors)


# ---------------------------------------------------------------------------
# Task G.4 — render citations from line_ranges
# ---------------------------------------------------------------------------
class TestRenderLineRanges(unittest.TestCase):

    def test_compact_citation(self):
        md = render_report.render_independent({
            "model": "claude-opus-5",
            "repository_fingerprint_sha256": "ab" * 32,
            "audit_summary": "s",
            "findings": [finding_doc(evidence=[
                {"kind": "OBSERVED_FACT", "path": "src/app.py",
                 "line_ranges": DISJOINT}])],
        })
        self.assertIn("L184-185, 240-273", md)

    def test_single_line_citation(self):
        md = render_report.render_independent({
            "model": "claude-opus-5",
            "repository_fingerprint_sha256": "ab" * 32,
            "audit_summary": "s",
            "findings": [finding_doc(evidence=[
                {"kind": "OBSERVED_FACT", "path": "src/app.py",
                 "line_ranges": [{"start": 184, "end": 184}]}])],
        })
        self.assertIn("L184", md)
        self.assertNotIn("L184-", md)


if __name__ == "__main__":
    unittest.main()
