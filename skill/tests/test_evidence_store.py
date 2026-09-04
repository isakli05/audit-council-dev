#!/usr/bin/env python3
"""Tests for evidence_store (PKG-EVID Tasks B.1-B.3).

Covers the provenance-bound EvidenceRecord cache: record shape +
anti-conclusion guard (B.1), visibility classes across the independence
barrier + access log (B.2), freshness / FRESH_REQUIRED / TTL invalidation +
run scoping (B.3), per AUDIT-COUNCIL-V2-ARCHITECTURE §3.4.4.

All tests are deterministic: the barrier is a plain flag object, the clock is
an injected mutable value, produced_at is caller-supplied — no sleeps.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

PYTHON = "/usr/bin/python3"  # NEVER sys.executable (AppImage shim on this host)

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "scripts"
SCHEMAS = TESTS.parent / "schemas"
sys.path.insert(0, str(SCRIPTS))

import evidence_store  # noqa: E402
from evidence_store import EvidenceStore, EvidenceStoreError  # noqa: E402
from state_store import sha256_bytes  # noqa: E402
from validate_artifact import validate  # noqa: E402

SANDBOX = TESTS / "fixtures" / "evid-sandbox"  # disposable, cleaned in tearDown

T0 = "2026-09-04T00:00:00Z"
FP = "a" * 64
BINDING = "b" * 64

REF_KEYS = {"evidence_id", "kind", "result_digest", "freshness_policy",
            "visibility"}


def make_record(**overrides) -> dict:
    rec = {
        "kind": "TEST_RESULT",
        "repository_fingerprint_sha256": FP,
        "environment_binding_digest": BINDING,
        "tool": {"name": "pytest", "version": "8.0.0"},
        "command_or_query": "pytest -q",
        "produced_at": T0,
        "freshness_policy": {"class": "CACHEABLE", "ttl_sec": None,
                             "invalidated_by": ["tracked_change",
                                                "head_change",
                                                "binding_change"]},
        "producer": "HARNESS",
        "visibility": "SHARED_MECHANICAL",
        "validity_scope": "RUN",
        "deterministic": True,
        "reproducible": True,
        "result": {"summary": {"passed": 3, "failed": 0},
                   "tests": [{"nodeid": "test_a", "outcome": "passed"}]},
    }
    rec.update(overrides)
    return rec


class Flag:
    """Zero-arg barrier_state callable, flipped by the test."""

    def __init__(self, initial: bool = False):
        self.open = initial

    def __call__(self) -> bool:
        return self.open


class Clock:
    """Injectable now() for the store (deterministic — never time.time)."""

    def __init__(self, now: str = "2026-09-04T00:00:00Z"):
        self.now = now

    def __call__(self) -> str:
        return self.now


class EvidenceStoreTestCase(unittest.TestCase):
    def setUp(self):
        SANDBOX.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="evid-", dir=SANDBOX)
        self.base = os.path.realpath(self.tmp.name)
        self.run_dir = os.path.join(self.base, "run")
        os.makedirs(self.run_dir)
        self.barrier = Flag()
        self.clock = Clock(T0)
        self.store = EvidenceStore(self.run_dir, self.barrier,
                                   now=self.clock)

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, **overrides) -> tuple[str, dict]:
        record = make_record(**overrides)
        return self.store.put(record), record

    def stored_record(self, evidence_id: str) -> dict:
        """The canonical stored record (index view, no payload)."""
        rec = self.store.get(evidence_id, "HARNESS", include_content=True)
        self.assertIsNotNone(rec)
        rec.pop("result", None)
        return rec

    def index_lines(self, run_dir: str | None = None) -> list[dict]:
        path = os.path.join(run_dir or self.run_dir, "evidence",
                            "index.jsonl")
        if not os.path.isfile(path):
            return []
        with open(path, encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]


# ---------------------------------------------------------------------------
# B.1 — record shape + anti-conclusion guard
# ---------------------------------------------------------------------------
class TestPutGetRoundtrip(EvidenceStoreTestCase):
    def test_put_returns_content_addressed_id(self):
        ev_id, _ = self.put()
        self.assertRegex(ev_id, r"^ev-[0-9a-f]{16}$")

    def test_get_returns_ref_only_by_default(self):
        ev_id, record = self.put()
        ref = self.store.get(ev_id, "OPUS")
        self.assertIsNotNone(ref)
        self.assertEqual(set(ref), REF_KEYS)
        self.assertEqual(ref["evidence_id"], ev_id)
        self.assertEqual(ref["kind"], "TEST_RESULT")
        self.assertEqual(ref["visibility"], "SHARED_MECHANICAL")
        self.assertEqual(ref["freshness_policy"], record["freshness_policy"])
        # just-in-time refs: NO payload leaks into the default ref
        self.assertNotIn("result", ref)
        self.assertNotIn("command_or_query", ref)
        self.assertNotIn("producer", ref)
        self.assertNotIn(str(record["result"]), json.dumps(ref))

    def test_get_content_only_with_include_content(self):
        ev_id, record = self.put()
        full = self.store.get(ev_id, "OPUS", include_content=True)
        self.assertIsNotNone(full)
        self.assertEqual(full["result"], record["result"])
        self.assertEqual(full["result_location"],
                         "evidence/objects/%s.json"
                         % sha256_bytes(evidence_store._canonical_json(
                             record["result"]).encode("utf-8")))
        # payload object is content-addressed on disk
        obj_path = os.path.join(self.run_dir, full["result_location"])
        self.assertTrue(os.path.isfile(obj_path))
        with open(obj_path, encoding="utf-8") as fh:
            self.assertEqual(json.load(fh), record["result"])

    def test_kind_enum_enforced(self):
        with self.assertRaises(EvidenceStoreError):
            self.store.put(make_record(kind="FINDING"))
        # fail-closed: nothing was stored
        self.assertEqual(self.index_lines(), [])
        objects = os.path.join(self.run_dir, "evidence", "objects")
        self.assertTrue(not os.path.isdir(objects)
                        or os.listdir(objects) == [])

    def test_missing_required_field_rejected(self):
        rec = make_record()
        del rec["produced_at"]
        with self.assertRaises(EvidenceStoreError):
            self.store.put(rec)
        self.assertEqual(self.index_lines(), [])

    def test_finding_shaped_payload_rejected_fail_closed(self):
        payload = {"id": "OPUS-001", "severity": "CRITICAL",
                   "claim": "auth bypass in login", "status": "PROVISIONAL"}
        with self.assertRaises(EvidenceStoreError) as ctx:
            self.store.put(make_record(result=payload))
        self.assertIn("conclusions are not evidence", str(ctx.exception))
        # nothing stored: no index entry, no payload object
        self.assertEqual(self.index_lines(), [])
        objects = os.path.join(self.run_dir, "evidence", "objects")
        self.assertTrue(not os.path.isdir(objects)
                        or os.listdir(objects) == [])
        self.assertIsNone(self.store.get("ev-doesnotmatter", "OPUS"))

    def test_findings_array_payload_rejected_fail_closed(self):
        payload = {"run": "ok", "findings": [
            {"id": "OPUS-001", "severity": "HIGH", "claim": "x",
             "verdict": "CONFIRMED", "final_status": "CONFIRMED"}]}
        with self.assertRaises(EvidenceStoreError) as ctx:
            self.store.put(make_record(result=payload))
        self.assertIn("conclusions are not evidence", str(ctx.exception))
        self.assertEqual(self.index_lines(), [])

    def test_nested_finding_shaped_payload_rejected(self):
        payload = {"data": {"probe": {"id": "CODEX-009", "claim": "c",
                                      "verdict": "DISPUTED"}}}
        with self.assertRaises(EvidenceStoreError):
            self.store.put(make_record(result=payload))
        self.assertEqual(self.index_lines(), [])

    def test_legitimate_evidence_payload_with_id_field_accepted(self):
        # one marker alone (e.g. a bare "id") is NOT a conclusion —
        # evidence payloads routinely carry single identifying keys
        ev_id, _ = self.put(result={"id": "run-42", "rows": 7})
        self.assertRegex(ev_id, r"^ev-[0-9a-f]{16}$")
        self.assertEqual(len(self.index_lines()), 1)

    def test_id_stability_and_idempotent_double_put(self):
        ev1, _ = self.put()
        ev2, _ = self.put()  # equal content (fresh dicts) -> equal id
        self.assertEqual(ev1, ev2)
        self.assertEqual(self.store.put(make_record()), ev1)
        # idempotent: exactly one index line, no duplicate
        self.assertEqual(len(self.index_lines()), 1)
        self.assertIsNotNone(self.store.get(ev1, "OPUS"))

    def test_different_content_different_id(self):
        ev1, _ = self.put()
        ev2, _ = self.put(command_or_query="pytest -q -k web")
        self.assertNotEqual(ev1, ev2)
        self.assertEqual(len(self.index_lines()), 2)

    def test_put_fills_input_digest_consistently(self):
        ev_id, _ = self.put()
        stored = self.stored_record(ev_id)
        self.assertEqual(stored["input_digest"],
                         evidence_store.compute_input_digest(
                             "pytest -q", {"name": "pytest",
                                           "version": "8.0.0"}))

    def test_put_rejects_inconsistent_input_digest(self):
        rec = make_record(input_digest="c" * 64)
        with self.assertRaises(EvidenceStoreError):
            self.store.put(rec)
        self.assertEqual(self.index_lines(), [])

    def test_put_rejects_inconsistent_result_digest(self):
        rec = make_record(result_digest="d" * 64)
        with self.assertRaises(EvidenceStoreError):
            self.store.put(rec)
        self.assertEqual(self.index_lines(), [])

    def test_stored_record_validates_against_schema(self):
        ev_id, _ = self.put()
        stored = self.stored_record(ev_id)
        schema = json.loads(
            (SCHEMAS / "evidence-record.schema.json").read_text())
        self.assertEqual(validate(stored, schema, base_dir=SCHEMAS), [])
        # negative control: broken record must NOT validate
        broken = dict(stored)
        del broken["environment_binding_digest"]
        self.assertNotEqual(validate(broken, schema, base_dir=SCHEMAS), [])

    def test_store_reloads_index_from_disk(self):
        ev_id, _ = self.put()
        reopened = EvidenceStore(self.run_dir, self.barrier, now=self.clock)
        self.assertIsNotNone(reopened.get(ev_id, "OPUS"))
        self.assertEqual(len(self.index_lines()), 1)


# ---------------------------------------------------------------------------
# B.2 — visibility classes + independence barrier + access log
# ---------------------------------------------------------------------------
class TestBarrierVisibility(EvidenceStoreTestCase):
    def test_private_opus_not_served_to_codex_pre_barrier(self):
        ev_id, _ = self.put(visibility="AUDITOR_PRIVATE", producer="OPUS")
        self.assertIsNone(self.store.get(ev_id, "CODEX"))
        log = self.store.access_log("CODEX")
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["evidence_id"], ev_id)
        self.assertFalse(log[0]["served"])
        self.assertTrue(log[0]["reason"])

    def test_private_opus_served_to_codex_post_barrier(self):
        ev_id, _ = self.put(visibility="AUDITOR_PRIVATE", producer="OPUS")
        self.assertIsNone(self.store.get(ev_id, "CODEX"))
        self.barrier.open = True
        ref = self.store.get(ev_id, "CODEX")
        self.assertIsNotNone(ref)
        self.assertEqual(set(ref), REF_KEYS)
        self.assertEqual([e["served"] for e in self.store.access_log("CODEX")],
                         [False, True])

    def test_private_opus_served_to_producer_family_pre_barrier(self):
        ev_id, _ = self.put(visibility="AUDITOR_PRIVATE", producer="OPUS")
        self.assertIsNotNone(self.store.get(ev_id, "OPUS"))
        self.assertIsNone(self.store.get(ev_id, "CODEX"))

    def test_private_codex_not_served_to_opus_pre_barrier(self):
        ev_id, _ = self.put(visibility="AUDITOR_PRIVATE", producer="CODEX")
        self.assertIsNone(self.store.get(ev_id, "OPUS"))
        self.assertIsNotNone(self.store.get(ev_id, "CODEX"))

    def test_private_specialist_producer_is_harness_only(self):
        ev_id, _ = self.put(visibility="AUDITOR_PRIVATE",
                            producer="SPECIALIST-security")
        self.assertIsNone(self.store.get(ev_id, "SPECIALIST-security"))
        self.assertIsNone(self.store.get(ev_id, "OPUS"))
        self.assertIsNotNone(self.store.get(ev_id, "HARNESS"))

    def test_shared_mechanical_served_to_everyone_pre_barrier(self):
        ev_id, _ = self.put(visibility="SHARED_MECHANICAL",
                            producer="HARNESS")
        for consumer in ("OPUS", "CODEX", "HARNESS", "SPECIALIST-concurrency"):
            self.assertIsNotNone(self.store.get(ev_id, consumer), consumer)

    def test_post_barrier_shared_only_after_barrier(self):
        ev_id, _ = self.put(visibility="POST_BARRIER_SHARED",
                            producer="OPUS")
        self.assertIsNone(self.store.get(ev_id, "CODEX"))
        self.assertIsNone(self.store.get(ev_id, "OPUS"))
        self.barrier.open = True
        self.assertIsNotNone(self.store.get(ev_id, "CODEX"))
        self.assertIsNotNone(self.store.get(ev_id, "OPUS"))

    def test_every_get_logged_served_or_denied(self):
        ev_shared, _ = self.put()
        ev_priv, _ = self.put(visibility="AUDITOR_PRIVATE", producer="OPUS")
        self.store.get(ev_shared, "OPUS")
        self.store.get(ev_priv, "OPUS")
        self.store.get(ev_priv, "CODEX")
        self.store.get("ev-0000000000000000", "OPUS")
        log = self.store.access_log()
        self.assertEqual(len(log), 4)
        self.assertEqual([e["served"] for e in log],
                         [True, True, False, False])
        for entry in log:
            self.assertIn(entry["evidence_id"], {ev_shared, ev_priv,
                                                 "ev-0000000000000000"})
            self.assertIn("consumer", entry)
            self.assertIn("at", entry)
            self.assertEqual(entry["at"], T0)  # injected clock
        self.assertEqual([e["reason"] for e in log if not e["served"]],
                         ["barrier_closed", "not_found"])

    def test_which_evidence_each_model_saw_cross_check(self):
        """The audit-history invariant: access_log(consumer) lists exactly
        the evidence ids that consumer received (post-hoc cross-check for
        artifacts citing evidence_id refs)."""
        ev_shared, _ = self.put()
        ev_opus_priv, _ = self.put(visibility="AUDITOR_PRIVATE",
                                   producer="OPUS")
        ev_codex_priv, _ = self.put(visibility="AUDITOR_PRIVATE",
                                    producer="CODEX")
        ev_post, _ = self.put(visibility="POST_BARRIER_SHARED",
                              producer="HARNESS")

        received = {"OPUS": set(), "CODEX": set()}
        for ev in (ev_shared, ev_opus_priv):
            if self.store.get(ev, "OPUS") is not None:
                received["OPUS"].add(ev)
        for ev in (ev_shared, ev_codex_priv, ev_opus_priv, ev_post):
            if self.store.get(ev, "CODEX") is not None:
                received["CODEX"].add(ev)
        # barrier opens; post-barrier evidence flows to everyone
        self.barrier.open = True
        for consumer in ("OPUS", "CODEX"):
            if self.store.get(ev_post, consumer) is not None:
                received[consumer].add(ev_post)

        self.assertEqual(received["OPUS"], {ev_shared, ev_opus_priv,
                                            ev_post})
        # post-barrier evidence flows to CODEX as well once the barrier opens
        self.assertEqual(received["CODEX"], {ev_shared, ev_codex_priv,
                                             ev_post})

        for consumer, expected in received.items():
            logged = {e["evidence_id"] for e in
                      self.store.access_log(consumer) if e["served"]}
            self.assertEqual(logged, expected, consumer)

    def test_access_log_consumer_filter_partitions(self):
        ev_id, _ = self.put()
        self.store.get(ev_id, "OPUS")
        self.store.get(ev_id, "CODEX")
        self.store.get(ev_id, "CODEX")
        self.assertEqual([e["consumer"] for e in self.store.access_log()],
                         ["OPUS", "CODEX", "CODEX"])
        self.assertEqual(len(self.store.access_log("OPUS")), 1)
        self.assertEqual(len(self.store.access_log("CODEX")), 2)

    def test_visible_to_is_pure_policy_check(self):
        ev_id, _ = self.put(visibility="AUDITOR_PRIVATE", producer="OPUS")
        self.assertFalse(self.store.visible_to(ev_id, "CODEX"))
        # strict family equality: even HARNESS cannot read an OPUS-private
        # record pre-barrier through the consumer API
        self.assertFalse(self.store.visible_to(ev_id, "HARNESS"))
        self.assertTrue(self.store.visible_to(ev_id, "OPUS"))
        self.barrier.open = True
        self.assertTrue(self.store.visible_to(ev_id, "CODEX"))
        # pure check: nothing was logged
        self.assertEqual(self.store.access_log(), [])

    def test_visible_to_unknown_id_false(self):
        self.assertFalse(self.store.visible_to("ev-0000000000000000", "OPUS"))

    def test_private_harness_producer_not_served_to_auditors(self):
        ev_id, _ = self.put(visibility="AUDITOR_PRIVATE", producer="HARNESS")
        self.assertIsNone(self.store.get(ev_id, "OPUS"))
        self.assertIsNone(self.store.get(ev_id, "CODEX"))
        self.assertIsNotNone(self.store.get(ev_id, "HARNESS"))


# ---------------------------------------------------------------------------
# B.3 — freshness, FRESH_REQUIRED gates, run scoping
# ---------------------------------------------------------------------------
class TestFreshness(EvidenceStoreTestCase):
    def test_revalidate_true_when_all_match(self):
        ev_id, _ = self.put()
        record = self.stored_record(ev_id)
        self.assertTrue(self.store.revalidate(record, FP, BINDING))

    def test_revalidate_fingerprint_mismatch(self):
        ev_id, _ = self.put()
        record = self.stored_record(ev_id)
        self.assertFalse(self.store.revalidate(record, "f" * 64, BINDING))

    def test_revalidate_binding_mismatch(self):
        ev_id, _ = self.put()
        record = self.stored_record(ev_id)
        self.assertFalse(self.store.revalidate(record, FP, "e" * 64))

    def test_revalidate_tampered_input_digest(self):
        ev_id, _ = self.put()
        record = self.stored_record(ev_id)
        record["input_digest"] = "0" * 64
        self.assertFalse(self.store.revalidate(record, FP, BINDING))

    def test_revalidate_command_drift(self):
        ev_id, _ = self.put()
        record = self.stored_record(ev_id)
        record["command_or_query"] = "pytest -q -k web"
        self.assertFalse(self.store.revalidate(record, FP, BINDING))

    def test_revalidate_tool_version_drift(self):
        ev_id, _ = self.put()
        record = self.stored_record(ev_id)
        record["tool"] = {"name": "pytest", "version": "8.1.0"}
        self.assertFalse(self.store.revalidate(record, FP, BINDING))

    def test_revalidate_tool_name_drift(self):
        ev_id, _ = self.put()
        record = self.stored_record(ev_id)
        record["tool"] = {"name": "unittest", "version": "8.0.0"}
        self.assertFalse(self.store.revalidate(record, FP, BINDING))

    def test_fresh_required_never_served_from_cache_but_retained(self):
        """Release-gate case: a stored green TEST_RESULT under a
        FRESH_REQUIRED policy can NEVER satisfy a get() — yet the record is
        retained in the index for audit history (retention != reuse)."""
        ev_id, record = self.put(freshness_policy={
            "class": "FRESH_REQUIRED", "ttl_sec": None,
            "invalidated_by": ["tracked_change", "head_change",
                               "binding_change"]},
            result={"summary": {"passed": 1, "failed": 0}, "green": True})
        self.clock.now = "2026-09-04T00:00:01Z"
        self.assertIsNone(self.store.get(ev_id, "OPUS"))
        self.assertIsNone(self.store.get(ev_id, "HARNESS"))
        log = self.store.access_log()
        self.assertEqual([e["reason"] for e in log],
                         ["fresh_required", "fresh_required"])
        # retained: still in the index with its payload on disk (read the
        # index directly — get() correctly refuses to serve it)
        indexed = self.index_lines()
        self.assertEqual([r["evidence_id"] for r in indexed], [ev_id])
        obj = os.path.join(self.run_dir, "evidence", "objects",
                           "%s.json" % indexed[0]["result_digest"])
        self.assertTrue(os.path.isfile(obj))
        # and NEVER reusable via revalidate either
        self.assertFalse(self.store.revalidate(indexed[0], FP, BINDING))

    def test_ttl_unexpired_allows_reuse(self):
        ev_id, _ = self.put(freshness_policy={
            "class": "CACHEABLE", "ttl_sec": 3600,
            "invalidated_by": []})
        record = self.stored_record(ev_id)
        self.clock.now = "2026-09-04T00:30:00Z"  # age 1800s < 3600s
        self.assertTrue(self.store.revalidate(record, FP, BINDING))

    def test_ttl_expiry_flips_revalidate_false(self):
        ev_id, _ = self.put(freshness_policy={
            "class": "CACHEABLE", "ttl_sec": 3600,
            "invalidated_by": []})
        record = self.stored_record(ev_id)
        self.clock.now = "2026-09-04T01:00:01Z"  # age 3601s > 3600s
        self.assertFalse(self.store.revalidate(record, FP, BINDING))

    def test_ttl_null_means_no_time_limit(self):
        ev_id, _ = self.put()  # ttl_sec: None
        record = self.stored_record(ev_id)
        self.clock.now = "2031-01-01T00:00:00Z"
        self.assertTrue(self.store.revalidate(record, FP, BINDING))

    def test_invalidated_by_tracked_change_trigger(self):
        ev_id, _ = self.put(freshness_policy={
            "class": "CACHEABLE", "ttl_sec": None,
            "invalidated_by": ["tracked_change"]})
        record = self.stored_record(ev_id)
        self.assertTrue(self.store.revalidate(record, FP, BINDING))
        self.assertFalse(self.store.revalidate(record, FP, BINDING,
                                               changes=["tracked_change"]))
        # a change NOT in invalidated_by does not invalidate
        self.assertTrue(self.store.revalidate(record, FP, BINDING,
                                              changes=["head_change"]))

    def test_invalidated_by_binding_change_trigger(self):
        ev_id, _ = self.put(freshness_policy={
            "class": "CACHEABLE", "ttl_sec": None,
            "invalidated_by": ["binding_change"]})
        record = self.stored_record(ev_id)
        self.assertFalse(self.store.revalidate(record, FP, BINDING,
                                               changes=["binding_change"]))

    def test_revalidate_malformed_record_false(self):
        self.assertFalse(self.store.revalidate({}, FP, BINDING))
        self.assertFalse(self.store.revalidate(None, FP, BINDING))

    def test_run_scoped_isolation_between_run_dirs(self):
        """validity_scope RUN: a second store in another run dir never
        serves the first run's records."""
        ev_id, _ = self.put(visibility="SHARED_MECHANICAL")
        other_dir = os.path.join(self.base, "run2")
        os.makedirs(other_dir)
        other = EvidenceStore(other_dir, Flag(), now=self.clock)
        self.assertIsNone(other.get(ev_id, "OPUS"))
        self.assertFalse(other.visible_to(ev_id, "OPUS"))
        self.assertEqual(other.access_log("OPUS")[0]["reason"], "not_found")
        self.assertEqual(len(self.index_lines(other_dir)), 0)
        # the original store still serves its own record
        self.assertIsNotNone(self.store.get(ev_id, "OPUS"))


if __name__ == "__main__":
    unittest.main()
