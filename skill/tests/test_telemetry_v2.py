#!/usr/bin/env python3
"""v2 pillar E — Telemetry Governor 2.0.

Promotes the Phase-0 reproduction R2 to permanent regressions: every terminal
attempt (QUOTA / AUTH_ERROR / FAILED / INVALID_OUTPUT / CANCELLED) gets a
stable elapsed_sec; INVALID_OUTPUT contributes invocation + tokens + elapsed
but never a successful stage; budgets are configurable with v1-identical
defaults; budget omissions are explicit and idempotently re-derived.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import budgets  # noqa: E402
import codex_runner  # noqa: E402
import state_store  # noqa: E402

SCHEMAS = SCRIPTS.parent / "schemas"


def make_run_dir(base: str, label: str) -> str:
    rd = os.path.join(base, label)
    os.makedirs(os.path.join(rd, "logs", "jobs"))
    state = state_store.new_state("20260904T000000Z-abc123", rd, "0" * 64)
    state_store.atomic_write_json(os.path.join(rd, "state.json"), state)
    return rd


def fake_job(run_dir: str, phase: str, age_s: float = 30.0) -> dict:
    return {
        "job_id": f"{phase}-tele0001",
        "run_dir": run_dir,
        "phase": phase,
        "pid": os.getpid(),
        "argv": ["codex", "exec"],
        "session": "s1",
        "resumed": False,
        "fresh_or_resumed": "fresh",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
        "attempt_number": 1,
        "started_at": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - age_s)),
        "started_at_monotonic": codex_runner.time.monotonic() - age_s,
        "status": "RUNNING",
        "artifact_status": "NOT_PRODUCED",
        "successful_stage_counted": False,
        "prompt_path": os.path.join(run_dir, "prompts", f"{phase}.md"),
        "output_path": os.path.join(
            run_dir, "logs", f"{phase}.tele0001.final.json"),
        "schema_path": "unused",
        "stdout_path": os.path.join(
            run_dir, "logs", f"{phase}.tele0001.jsonl"),
        "stderr_path": os.path.join(
            run_dir, "logs", f"{phase}.tele0001.stderr.log"),
        "exit_code_path": os.path.join(
            run_dir, "logs", "jobs", f"{phase}-tele0001.exitcode"),
    }


class TestElapsedOnEveryTerminal(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(
            prefix="tele-v2-", dir=str(Path(__file__).resolve().parent /
                                       "fixtures"))

    def tearDown(self):
        self._tmp.cleanup()

    def _classify_failure(self, stderr_text: str, exit_code: int):
        rd = make_run_dir(self._tmp.name, "rd")
        job = fake_job(rd, "cross_examination")
        with open(job["stderr_path"], "w") as fh:
            fh.write(stderr_text)
        with open(job["stdout_path"], "w") as fh:
            fh.write("")
        status, cli = codex_runner.classify_and_finalize(rd, job, exit_code)
        rec = json.load(open(os.path.join(
            rd, "logs", "jobs", f"{job['job_id']}.json")))
        return status, cli, rec

    def test_quota_attempt_has_stable_elapsed(self):
        status, cli, rec = self._classify_failure(
            "codex: usage limit reached for your plan (429)\n", 1)
        self.assertEqual((status, cli), ("QUOTA", 2))
        self.assertTrue(rec.get("completed_at"))
        self.assertIsInstance(rec.get("elapsed_sec"), float)
        self.assertGreaterEqual(rec["elapsed_sec"], 0.0)

    def test_auth_attempt_has_elapsed(self):
        status, _, rec = self._classify_failure(
            "codex: not logged in (401)\n", 1)
        self.assertEqual(status, "AUTH_ERROR")
        self.assertIsInstance(rec.get("elapsed_sec"), float)

    def test_failed_attempt_has_elapsed(self):
        status, _, rec = self._classify_failure("boom\n", 1)
        self.assertEqual(status, "FAILED")
        self.assertIsInstance(rec.get("elapsed_sec"), float)

    def test_invalid_output_attempt_has_elapsed_not_stage(self):
        rd = make_run_dir(self._tmp.name, "rd-inv")
        job = fake_job(rd, "cross_examination")
        with open(job["output_path"], "w") as fh:
            fh.write('{"examiner": "CODEX", "examined": "OPUS", '
                     '"challenges": [], "bogus": 1}')  # unknown key → invalid
        with open(job["stdout_path"], "w") as fh:
            fh.write('{"type":"thread.started","thread_id":"t"}\n'
                     '{"type":"turn.completed","usage":{"input_tokens":10,'
                     '"output_tokens":5}}\n')
        status, cli = codex_runner.classify_and_finalize(rd, job, 0)
        self.assertEqual((status, cli), ("INVALID_OUTPUT", 6))
        rec = json.load(open(os.path.join(
            rd, "logs", "jobs", f"{job['job_id']}.json")))
        self.assertIsInstance(rec.get("elapsed_sec"), float)
        self.assertFalse(rec["successful_stage_counted"])
        # tokens + invocation + elapsed counted, stage not
        metrics = json.load(open(os.path.join(rd, "99-run-metrics.json")))
        inv = metrics["invocations"][0]
        self.assertEqual(inv["status"], "INVALID_OUTPUT")
        self.assertEqual(inv["tokens"]["input_tokens"], 10)
        self.assertIsInstance(inv.get("elapsed_sec"), float)
        self.assertEqual(metrics["aggregates"]["successful_stage_counted_total"], 0)
        self.assertEqual(metrics["aggregates"]["invocation_count"], 1)

    def test_cancelled_attempt_has_elapsed(self):
        rd = make_run_dir(self._tmp.name, "rd-cancel")
        job = fake_job(rd, "independent")
        # a dead (reaped) pid: cancel must not signal a live process — and
        # most definitely must never use OUR pid (that once killed the test
        # runner itself)
        dead = subprocess.Popen(["/bin/true"])
        dead.wait()
        job["pid"] = dead.pid if dead.pid != os.getpid() else 999999
        # simulate a launched job record on disk, then cancel via library call
        codex_runner.atomic_write_json(
            os.path.join(rd, "logs", "jobs", f"{job['job_id']}.json"), job)
        import argparse
        codex_runner.cmd_cancel(argparse.Namespace(job=os.path.join(
            rd, "logs", "jobs", f"{job['job_id']}.json")))
        rec = json.load(open(os.path.join(
            rd, "logs", "jobs", f"{job['job_id']}.json")))
        self.assertEqual(rec["status"], "CANCELLED")
        self.assertIsInstance(rec.get("elapsed_sec"), float)

    def test_rewait_never_inflates_elapsed(self):
        status, _, rec = self._classify_failure("usage limit\n", 1)
        first = rec["elapsed_sec"]
        # simulate a re-wait re-running finalize on the persisted record
        codex_runner._finalize_elapsed(rec)
        self.assertEqual(rec["elapsed_sec"], first)

    def test_unknown_clock_documented(self):
        job = {"started_at": "2026-09-04T00:00:00Z"}  # no monotonic anchor
        codex_runner._finalize_elapsed(job)
        self.assertIsNone(job["elapsed_sec"])
        self.assertEqual(job["elapsed_unknown_reason"],
                         "monotonic_start_missing")

    def test_wall_clock_matches_elapsed(self):
        # completed_at - started_at within ±2 s of elapsed for every attempt
        status, _, rec = self._classify_failure("usage limit\n", 1)
        import datetime as dt
        started = dt.datetime.strptime(
            rec["started_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=dt.timezone.utc)
        completed = dt.datetime.strptime(
            rec["completed_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=dt.timezone.utc)
        wall = (completed - started).total_seconds()
        self.assertLessEqual(abs(wall - rec["elapsed_sec"]), 2.0)


class TestBudgets(unittest.TestCase):
    def test_defaults_match_v1_governor(self):
        b = budgets.DEFAULT_BUDGETS
        self.assertEqual(b["max_successful_stages_per_phase"], 1)
        self.assertEqual(b["max_total_successful_stages"], 3)
        self.assertEqual(b["max_attempts_per_phase"], 3)
        self.assertEqual(b["max_repairs_per_phase"], 1)
        self.assertEqual(b["specialists_default"], 0)
        self.assertEqual(b["specialists_normal_cap"], 2)
        self.assertEqual(b["specialists_hard_cap"], 3)

    def test_manifest_override_respected(self):
        with tempfile.TemporaryDirectory() as rd:
            with open(os.path.join(rd, "00-run-manifest.json"), "w") as fh:
                json.dump({"budgets": {"max_attempts_per_phase": 2}}, fh)
            self.assertEqual(budgets.load(rd)["max_attempts_per_phase"], 2)
            # unknown keys ignored, others default
            self.assertEqual(budgets.load(rd)["max_total_successful_stages"], 3)

    def _state(self, stage_counts=None, jobs=(), specialists=None):
        return {
            "codex": {
                "stage_counts": stage_counts or {"independent": 0,
                                                 "cross_examination": 0,
                                                 "adjudication": 0},
                "jobs": list(jobs),
            },
            "specialists": specialists,
        }

    def test_governor_refusals(self):
        b = budgets.DEFAULT_BUDGETS
        # 2nd successful stage of a phase
        with self.assertRaises(budgets.BudgetExceeded):
            budgets.check("independent", b,
                          self._state({"independent": 1,
                                       "cross_examination": 0,
                                       "adjudication": 0}))
        # 4th total successful stage
        with self.assertRaises(budgets.BudgetExceeded):
            budgets.check("adjudication", b,
                          self._state({"independent": 1,
                                       "cross_examination": 1,
                                       "adjudication": 1}))
        # 4th attempt in a phase
        jobs = [{"phase": "independent"}] * 3
        with self.assertRaises(budgets.BudgetExceeded):
            budgets.check("independent", b, self._state(jobs=jobs))
        # healthy state passes
        budgets.check("independent", b, self._state(jobs=[{"phase":
                                                           "independent"}] * 2))

    def test_specialist_default_zero_refuses(self):
        with self.assertRaises(budgets.BudgetExceeded):
            budgets.check("specialist", budgets.DEFAULT_BUDGETS,
                          self._state(specialists={"count": 0}))
        # activated (count>0 recorded, e.g. pre-frozen reason present) →
        # allowed up to the normal cap
        budgets.check("specialist", budgets.DEFAULT_BUDGETS,
                      self._state(specialists={"count": 1}))
        with self.assertRaises(budgets.BudgetExceeded):
            budgets.check("specialist", budgets.DEFAULT_BUDGETS,
                          self._state(specialists={"count": 2}))
        # hard cap (3) requires operator elevation past the normal cap
        with self.assertRaises(budgets.BudgetExceeded):
            budgets.check("specialist", budgets.DEFAULT_BUDGETS,
                          self._state(specialists={"count": 2}))
        budgets.check("specialist", budgets.DEFAULT_BUDGETS,
                      self._state(specialists={"count": 2,
                                               "operator_elevated": True}))
        with self.assertRaises(budgets.BudgetExceeded):
            budgets.check("specialist", budgets.DEFAULT_BUDGETS,
                          self._state(specialists={"count": 3,
                                                   "operator_elevated": True}))

    def test_omissions_recorded_and_rebuilt(self):
        with tempfile.TemporaryDirectory() as rd:
            budgets.record_omission(rd, {
                "stage": "adjudication",
                "decision": "declined",
                "reason": "no eligible disputes; verdict unaffected",
                "recorded_at": "2026-09-04T00:00:00Z",
            })
            entries = budgets.load_omissions(rd)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["stage"], "adjudication")
            # metrics re-derives omissions (idempotent, restart-safe)
            metrics = codex_runner.rebuild_metrics(rd)
            self.assertEqual(len(metrics["budget_omissions"]), 1)
            metrics2 = codex_runner.rebuild_metrics(rd)
            self.assertEqual(metrics2["budget_omissions"],
                             metrics["budget_omissions"])

    def test_metrics_reconstruct_identically_after_delete(self):
        with tempfile.TemporaryDirectory() as rd:
            os.makedirs(os.path.join(rd, "logs", "jobs"), exist_ok=True)
            job = fake_job(rd, "independent")
            job["status"] = "QUOTA"
            job["completed_at"] = codex_runner.utc_now()
            job["elapsed_sec"] = 12.5
            job["tokens"] = {"input_tokens": 5, "cached_input_tokens": 0,
                             "output_tokens": 1,
                             "reasoning_output_tokens": 0}
            job["turns"] = 1
            codex_runner.atomic_write_json(
                os.path.join(rd, "logs", "jobs", f"{job['job_id']}.json"),
                job)
            m1 = codex_runner.rebuild_metrics(rd)
            raw1 = open(os.path.join(rd, "99-run-metrics.json")).read()
            os.unlink(os.path.join(rd, "99-run-metrics.json"))
            codex_runner.rebuild_metrics(rd)
            raw2 = open(os.path.join(rd, "99-run-metrics.json")).read()
            self.assertEqual(raw1, raw2)
            self.assertEqual(m1["aggregates"]["invocation_count"], 1)


if __name__ == "__main__":
    unittest.main()
