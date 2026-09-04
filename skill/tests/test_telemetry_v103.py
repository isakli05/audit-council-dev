"""v1.0.3 Defect 2 — inference-attempt telemetry and log-preservation tests.

An inference attempt is NOT the same event as a successful stage or a
canonical artifact acceptance. Every real attempt (COMPLETE, INVALID_OUTPUT,
QUOTA, AUTH_ERROR, FAILED, CANCELLED) must appear in 99-run-metrics.json with
its usage when exposed; metrics are rebuilt from persisted job records and
are therefore idempotent and resume-safe; per-job logs can never overwrite
one another.
"""
from __future__ import annotations

import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

from test_codex_runner_mock import Harness  # noqa: E402


def metrics(run_dir):
    with open(os.path.join(run_dir, "99-run-metrics.json")) as f:
        return json.load(f)


class TestAttemptAccounting(Harness):

    def test_complete_canonical_valid_counts_stage_and_invocation(self):
        job_path = self.start(mode="ok")
        self.wait(job_path)
        m = metrics(self.run)
        self.assertEqual(m["aggregates"]["invocation_count"], 1)
        self.assertEqual(m["aggregates"]["successful_stage_counted_total"], 1)
        inv = m["invocations"][0]
        self.assertEqual(inv["status"], "COMPLETE")
        self.assertEqual(inv["artifact_status"], "CANONICAL_VALID")
        self.assertTrue(inv["successful_stage_counted"])
        self.assertEqual(inv["model"], "gpt-5.6-sol")
        self.assertEqual(inv["reasoning_effort"], "xhigh")
        self.assertEqual(inv["fresh_or_resumed"], "fresh")
        self.assertEqual(inv["attempt_number"], 1)
        self.assertIsNotNone(inv["tokens"])  # usage exposed by fake codex

    def test_complete_process_invalid_output_counts_invocation_not_stage(self):
        job_path = self.start(mode="malformed_json")
        proc = self.cli("wait", job_path, "--timeout", "30")
        self.assertEqual(proc.returncode, 6)
        m = metrics(self.run)
        self.assertEqual(m["aggregates"]["invocation_count"], 1)
        self.assertEqual(m["aggregates"]["successful_stage_counted_total"], 0)
        inv = m["invocations"][0]
        self.assertEqual(inv["status"], "INVALID_OUTPUT")
        # usage from turn.completed retained even though artifact rejected
        self.assertEqual(inv["tokens"]["input_tokens"], 100)
        self.assertEqual(self.state()["codex"]["stage_counts"]
                         ["independent"], 0)

    def test_fingerprint_mismatch_usage_counted_stage_not(self):
        self.base_env["FAKE_CODEX_FINGERPRINT"] = "a" * 64
        job_path = self.start()
        self.wait(job_path)
        m = metrics(self.run)
        inv = m["invocations"][0]
        self.assertEqual(inv["artifact_status"], "FINGERPRINT_MISMATCH")
        self.assertEqual(inv["tokens"]["output_tokens"], 200)
        self.assertFalse(inv["successful_stage_counted"])

    def test_quota_with_usage_retains_usage_no_stage(self):
        self.base_env["FAKE_CODEX_USAGE_FIRST"] = "1"
        job_path = self.start(mode="quota")
        proc = self.cli("wait", job_path, "--timeout", "30")
        self.assertEqual(proc.returncode, 2)
        m = metrics(self.run)
        inv = m["invocations"][0]
        self.assertEqual(inv["status"], "QUOTA")
        self.assertEqual(inv["tokens"]["input_tokens"], 100)
        self.assertFalse(inv["successful_stage_counted"])

    def test_auth_error_invocation_retained_no_stage(self):
        job_path = self.start(mode="auth")
        proc = self.cli("wait", job_path, "--timeout", "30")
        self.assertEqual(proc.returncode, 3)
        m = metrics(self.run)
        self.assertEqual(m["aggregates"]["invocation_count"], 1)
        self.assertEqual(m["aggregates"]["successful_stage_counted_total"], 0)
        self.assertEqual(m["invocations"][0]["status"], "AUTH_ERROR")

    def test_failed_invocation_retained_no_stage(self):
        job_path = self.start(mode="crash")
        self.wait(job_path)
        m = metrics(self.run)
        self.assertEqual(m["invocations"][0]["status"], "FAILED")
        self.assertEqual(m["aggregates"]["invocation_count"], 1)
        self.assertEqual(m["aggregates"]["successful_stage_counted_total"], 0)

    def test_repair_counts_both_attempts_unique_logs_one_stage(self):
        job_path = self.start(mode="malformed_json")
        self.wait(job_path)  # INVALID_OUTPUT
        repair = self.cli("repair", job_path)
        self.assertEqual(repair.returncode, 0, repair.stderr)
        repair_job = repair.stdout.strip()
        # repair runs with mode ok (fake default env per cli())
        self.wait(repair_job)
        m = metrics(self.run)
        ids = [i["job_id"] for i in m["invocations"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(m["aggregates"]["invocation_count"], 2)
        by_id = {i["job_id"]: i for i in m["invocations"]}
        orig = by_id[json.load(open(job_path))["job_id"]]
        rep = by_id[json.load(open(repair_job))["job_id"]]
        self.assertEqual(orig["status"], "INVALID_OUTPUT")
        self.assertEqual(rep["status"], "COMPLETE")
        self.assertEqual(rep["repair_of"], orig["job_id"])
        self.assertEqual(m["aggregates"]["successful_stage_counted_total"], 1)
        # unique log files per attempt
        self.assertNotEqual(orig["job_id"], rep["job_id"])
        logs = os.listdir(os.path.join(self.run, "logs"))
        jsonls = [l for l in logs if l.endswith(".jsonl")]
        self.assertEqual(len(jsonls), 2)
        finals = [l for l in logs if l.endswith(".final.json")]
        self.assertEqual(len(finals), 2)

    def test_resumed_cross_examination_counted_separately(self):
        job_path = self.start()
        self.wait(job_path)
        sid = self.state()["codex"]["session_id"]
        self.assertTrue(sid)
        job2 = self.start(phase="cross_examination", session=sid)
        self.wait(job2)
        m = metrics(self.run)
        self.assertEqual(m["aggregates"]["invocation_count"], 2)
        self.assertEqual(m["aggregates"]["fresh_count"], 1)
        self.assertEqual(m["aggregates"]["resumed_count"], 1)
        resumed = [i for i in m["invocations"] if i["resumed"]][0]
        self.assertEqual(resumed["fresh_or_resumed"], "resumed")

    def test_repeated_wait_and_status_do_not_double_count(self):
        job_path = self.start()
        self.wait(job_path)
        self.wait(job_path)          # idempotent re-wait
        self.cli("status", job_path)
        self.cli("status", job_path)
        m = metrics(self.run)
        self.assertEqual(m["aggregates"]["invocation_count"], 1)
        self.assertEqual(m["aggregates"]["tokens"]["input_tokens"], 100)

    def test_restart_reconstructs_identical_metrics(self):
        job_path = self.start()
        self.wait(job_path)
        before = metrics(self.run)
        os.remove(os.path.join(self.run, "99-run-metrics.json"))
        self.cli("status", job_path)  # reconstruction point
        after = metrics(self.run)
        self.assertEqual(before, after)

    def test_unknown_usage_is_explicitly_unknown_not_zero(self):
        job_path = self.start(mode="crash")  # no JSONL usage events at all
        self.wait(job_path)
        m = metrics(self.run)
        inv = m["invocations"][0]
        self.assertIsNone(inv["tokens"])  # unknown, not fabricated zeros
        self.assertEqual(m["aggregates"]["usage_unknown_count"], 1)
        self.assertEqual(m["aggregates"]["tokens"]["input_tokens"], 0)

    def test_totals_equal_sum_of_usage_bearing_attempts(self):
        job_path = self.start(mode="ok")
        self.wait(job_path)
        job2 = self.start(phase="cross_examination",
                          session=self.state()["codex"]["session_id"])
        self.wait(job2)
        m = metrics(self.run)
        known = [i for i in m["invocations"] if i["tokens"] is not None]
        for k in ("input_tokens", "cached_input_tokens", "output_tokens",
                  "reasoning_output_tokens"):
            self.assertEqual(m["aggregates"]["tokens"][k],
                             sum(i["tokens"][k] for i in known))

    def test_per_job_logs_cannot_overwrite(self):
        job1 = self.start(mode="crash")
        self.wait(job1)
        job2 = self.start(mode="crash")  # retry allowed (failure)
        self.wait(job2)
        logs = os.listdir(os.path.join(self.run, "logs"))
        jsonls = sorted(l for l in logs if l.endswith(".jsonl"))
        errs = sorted(l for l in logs if l.endswith(".stderr.log"))
        self.assertEqual(len(jsonls), 2)
        self.assertEqual(len(errs), 2)
        j1 = json.load(open(job1)); j2 = json.load(open(job2))
        self.assertNotEqual(j1["stdout_path"], j2["stdout_path"])
        self.assertNotEqual(j1["stderr_path"], j2["stderr_path"])
        self.assertNotEqual(j1["output_path"], j2["output_path"])

    def test_cancel_preserves_logs_and_counts_invocation(self):
        job_path = self.start(mode="slow")
        self.cli("cancel", job_path)
        logs = os.listdir(os.path.join(self.run, "logs"))
        j = json.load(open(job_path))
        self.assertTrue(os.path.isfile(j["stdout_path"]))
        self.assertIn(os.path.basename(j["stdout_path"]), logs)
        m = metrics(self.run)
        self.assertEqual(m["invocations"][0]["status"], "CANCELLED")

    def test_repeated_wait_does_not_inflate_elapsed(self):
        # v1.0.3 review F3: elapsed is computed once at first finalize
        job_path = self.start()
        self.wait(job_path)
        first = json.load(open(job_path))["elapsed_sec"]
        import time as _t
        _t.sleep(0.3)
        self.wait(job_path)  # idempotent re-wait
        again = json.load(open(job_path))["elapsed_sec"]
        self.assertEqual(first, again)

    def test_wait_after_cancel_returns_cancelled(self):
        # v1.0.3 review F4: re-wait must never relabel CANCELLED -> FAILED
        job_path = self.start(mode="slow")
        self.cli("cancel", job_path)
        proc = self.cli("wait", job_path, "--timeout", "30")
        out = json.loads(proc.stdout.strip().splitlines()[-1])
        self.assertEqual(out["status"], "CANCELLED")
        m = metrics(self.run)
        self.assertEqual(m["invocations"][0]["status"], "CANCELLED")

    def test_cancel_after_complete_does_not_relabel(self):
        # v1.0.3 review F5: terminal records are immutable
        job_path = self.start()
        self.wait(job_path)
        proc = self.cli("cancel", job_path)
        out = json.loads(proc.stdout.strip().splitlines()[-1])
        self.assertEqual(out["status"], "COMPLETE")
        j = json.load(open(job_path))
        self.assertEqual(j["status"], "COMPLETE")
        self.assertEqual(self.state()["codex"]["stage_counts"]
                         ["independent"], 1)

    def test_attempt_numbers_increment_per_phase(self):
        job1 = self.start(mode="crash")
        self.wait(job1)
        job2 = self.start(mode="crash")
        self.wait(job2)
        m = metrics(self.run)
        nums = sorted(i["attempt_number"] for i in m["invocations"])
        self.assertEqual(nums, [1, 2])


if __name__ == "__main__":
    unittest.main()
