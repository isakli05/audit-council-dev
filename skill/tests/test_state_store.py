#!/usr/bin/env python3
"""Tests for state_store: atomic writes, transitions, checksums."""
from __future__ import annotations

import json
import os
import sys

PYTHON = "python3"  # NOT sys.executable (may be an embedded app host)
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import state_store  # noqa: E402


def make_run(tmp: str) -> str:
    run_dir = os.path.join(tmp, "run")
    os.makedirs(run_dir)
    state = state_store.new_state("20260903T170000Z-a1b2c3", tmp,
                                  "0" * 64)
    state_store.save_state(run_dir, state)
    return run_dir


class TestAtomicWrite(unittest.TestCase):
    def test_atomic_write_leaves_no_temp_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "artifact.json")
            state_store.atomic_write_text(path, '{"a": 1}\n')
            state_store.atomic_write_text(path, '{"a": 2}\n')
            self.assertEqual(os.listdir(tmp), ["artifact.json"])
            with open(path) as fh:
                self.assertEqual(json.load(fh), {"a": 2})

    def test_atomic_write_json_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "x.json")
            state_store.atomic_write_json(path, {"k": [1, 2]})
            self.assertEqual(state_store.load_json(path), {"k": [1, 2]})


class TestRunId(unittest.TestCase):
    def test_run_id_format(self):
        rid = state_store.new_run_id()
        self.assertRegex(rid, r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}$")

    def test_run_id_collision_safe(self):
        existing = set()
        first = state_store.new_run_id(existing)
        existing.add(first)
        # freeze time by pre-filling many ids is impractical; just assert a
        # fresh id differs from the recorded one.
        self.assertNotEqual(state_store.new_run_id(existing), first)


class TestTransitions(unittest.TestCase):
    @staticmethod
    def scaffold_skips(run_dir, *phases):
        # v2: jumping over artifact phases requires explicit skip records
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": p, "reason": "test scaffold jump"}
            for p in phases])

    def test_forward_chain_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            for phase in ("PREFLIGHT_COMPLETE", "CONTRACT_FROZEN",
                          "OPUS_INDEPENDENT_COMPLETE"):
                state_store.apply_transition(run_dir, phase)
            state = state_store.load_state(run_dir)
            self.assertEqual(state["phase"], "OPUS_INDEPENDENT_COMPLETE")
            self.assertIn("PREFLIGHT_COMPLETE", state["timestamps"])
            self.assertEqual(state["phase_attempts"]["CONTRACT_FROZEN"], 1)

    def test_backward_and_same_phase_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            state_store.apply_transition(run_dir, "CONTRACT_FROZEN")
            with self.assertRaises(state_store.StateError):
                state_store.apply_transition(run_dir, "CREATED")
            with self.assertRaises(state_store.StateError):
                state_store.apply_transition(run_dir, "CONTRACT_FROZEN")

    def test_unknown_phase_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            with self.assertRaises(state_store.StateError):
                state_store.apply_transition(run_dir, "NOT_A_PHASE")

    def test_skip_adjudication_requires_flag_and_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            self.scaffold_skips(
                run_dir, "CONTRACT_FROZEN", "OPUS_INDEPENDENT_COMPLETE",
                "CODEX_INDEPENDENT_COMPLETE", "NORMALIZED",
                "OPUS_CROSS_EXAM_COMPLETE", "CODEX_CROSS_EXAM_COMPLETE")
            state_store.apply_transition(run_dir, "LEDGER_COMPLETE")
            # skipping without the flag -> error
            with self.assertRaises(state_store.StateError):
                state_store.apply_transition(run_dir, "FINALIZED")
            # legal skip: LEDGER_COMPLETE -> FINALIZED
            state_store.apply_transition(run_dir, "FINALIZED",
                                         adjudication_skipped=True)
            state = state_store.load_state(run_dir)
            self.assertTrue(state["adjudication_skipped"])
            self.assertNotIn("ADJUDICATION_COMPLETE", state["timestamps"])
            # continue forward after the skip
            state_store.apply_transition(run_dir, "COMPLETE")

    def test_skip_from_wrong_phase_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            self.scaffold_skips(
                run_dir, "CONTRACT_FROZEN", "OPUS_INDEPENDENT_COMPLETE",
                "CODEX_INDEPENDENT_COMPLETE", "NORMALIZED",
                "OPUS_CROSS_EXAM_COMPLETE")
            state_store.apply_transition(run_dir, "CODEX_CROSS_EXAM_COMPLETE")
            # would skip LEDGER_COMPLETE and ADJUDICATION_COMPLETE
            with self.assertRaises(state_store.StateError):
                state_store.apply_transition(run_dir, "FINALIZED",
                                             adjudication_skipped=True)

    def test_normal_adjudication_path_no_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            self.scaffold_skips(
                run_dir, "CONTRACT_FROZEN", "OPUS_INDEPENDENT_COMPLETE",
                "CODEX_INDEPENDENT_COMPLETE", "NORMALIZED",
                "OPUS_CROSS_EXAM_COMPLETE", "CODEX_CROSS_EXAM_COMPLETE")
            state_store.apply_transition(run_dir, "LEDGER_COMPLETE")
            state_store.apply_transition(run_dir, "ADJUDICATION_COMPLETE")
            state_store.apply_transition(run_dir, "FINALIZED")
            state = state_store.load_state(run_dir)
            self.assertFalse(state["adjudication_skipped"])
            self.assertIn("ADJUDICATION_COMPLETE", state["timestamps"])

    def test_state_sanity_rejects_garbage(self):
        with self.assertRaises(state_store.StateError):
            state_store.sanity_check_state({"phase": "CREATED"})
        with self.assertRaises(state_store.StateError):
            state_store.sanity_check_state(
                {**state_store.new_state("bad", "/", "0" * 64)})


class TestCheckTransition(unittest.TestCase):
    """B-001: check_transition is a pure eligibility preview that applies
    the SAME authoritative rules as apply_transition — forward-only order,
    adjudication-skip rules, LEDGER_COMPLETE, explicit artifact-phase skip
    records — with zero mutation and zero attempt accounting."""

    def test_preview_agrees_with_apply_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            state_store.apply_transition(run_dir, "CONTRACT_FROZEN")
            before = open(state_store.state_path(run_dir), "rb").read()
            for bad in ("CONTRACT_FROZEN", "CREATED", "NOT_A_PHASE"):
                with self.assertRaises(state_store.StateError):
                    state_store.check_transition(run_dir, bad)
            previewed = state_store.check_transition(
                run_dir, "OPUS_INDEPENDENT_COMPLETE")
            self.assertEqual(previewed["phase"],
                             "OPUS_INDEPENDENT_COMPLETE")
            # pure: state.json byte-identical, no attempt accounting
            self.assertEqual(
                open(state_store.state_path(run_dir), "rb").read(), before)
            state = state_store.load_state(run_dir)
            self.assertEqual(state["phase"], "CONTRACT_FROZEN")
            self.assertNotIn("OPUS_INDEPENDENT_COMPLETE",
                             state["phase_attempts"])

    def test_preview_evaluates_prospective_skips_without_persisting(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            entries = [{"skipped_phase": p, "reason": "test jump"}
                       for p in ("CONTRACT_FROZEN",
                                 "OPUS_INDEPENDENT_COMPLETE")]
            # the multi-phase jump is rejected without skip records — the
            # preview enforces the same explicit-skip requirement
            with self.assertRaises(state_store.StateError):
                state_store.check_transition(
                    run_dir, "CODEX_INDEPENDENT_COMPLETE")
            # ...previews clean with the prospective skips admitted...
            state_store.check_transition(run_dir, "CODEX_INDEPENDENT_COMPLETE",
                                         prospective_skips=entries)
            # ...and persisted nothing
            state = state_store.load_state(run_dir)
            self.assertNotIn("phase_skips", state)
            # recording the same skips for real then lets the authoritative
            # commit path accept the identical transition
            state_store.record_phase_skips(run_dir, entries)
            state_store.apply_transition(
                run_dir, "CODEX_INDEPENDENT_COMPLETE")

    def test_preview_rejects_invalid_prospective_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            with self.assertRaises(state_store.StateError):
                state_store.check_transition(
                    run_dir, "CODEX_INDEPENDENT_COMPLETE",
                    prospective_skips=[
                        {"skipped_phase": "NOT_A_PHASE", "reason": "x"}])
            with self.assertRaises(state_store.StateError):
                state_store.check_transition(
                    run_dir, "CODEX_INDEPENDENT_COMPLETE",
                    prospective_skips=[
                        {"skipped_phase": "CONTRACT_FROZEN",
                         "reason": "   "}])
            # duplicates of already-recorded skips are rejected identically
            state_store.record_phase_skips(run_dir, [
                {"skipped_phase": "CONTRACT_FROZEN", "reason": "recorded"}])
            with self.assertRaises(state_store.StateError):
                state_store.check_transition(
                    run_dir, "CODEX_INDEPENDENT_COMPLETE",
                    prospective_skips=[
                        {"skipped_phase": "CONTRACT_FROZEN",
                         "reason": "duplicate"}])


class TestChecksums(unittest.TestCase):
    def test_record_and_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            art = os.path.join(run_dir, "40-disagreement-ledger.json")
            state_store.atomic_write_text(art, '{"clusters": []}')
            state_store.record_checksum(run_dir, art)
            self.assertEqual(state_store.verify_all(run_dir), [])

    def test_tamper_detection(self):
        # scenario X (partial): checksum failure must be detectable
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            art = os.path.join(run_dir, "40-disagreement-ledger.json")
            state_store.atomic_write_text(art, '{"clusters": []}')
            state_store.record_checksum(run_dir, art)
            # tamper
            state_store.atomic_write_text(art, '{"clusters": [], "x": 1}')
            mismatches = state_store.verify_all(run_dir)
            self.assertEqual(len(mismatches), 1)
            self.assertEqual(mismatches[0]["error"], "checksum mismatch")

    def test_missing_file_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            art = os.path.join(run_dir, "30-normalized-findings.json")
            state_store.atomic_write_text(art, "{}")
            state_store.record_checksum(run_dir, art)
            os.unlink(art)
            mismatches = state_store.verify_all(run_dir)
            self.assertEqual(mismatches[0]["error"], "missing")


class TestStateCli(unittest.TestCase):
    def test_verify_checksums_cli_exit_codes(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(tmp)
            rc = subprocess.run(
                [PYTHON, str(SCRIPTS / "state_store.py"),
                 "verify-checksums", "--run", run_dir],
                capture_output=True, text=True)
            self.assertEqual(rc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
