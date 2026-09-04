"""v1.0.2 runner-robustness regression tests (detached-process lifecycle).

Defect: cmd_wait gated completion on proc_alive(pid) == False, but a
terminated-but-unreaped (zombie) process still satisfies os.kill(pid, 0).
The wrapper-persisted exit-code file is now the PRIMARY completion signal.

All tests mock liveness for the zombie-like condition; no real zombies,
no real model calls.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
sys.path.insert(0, SCRIPTS)

import codex_runner  # noqa: E402

PYTHON = "python3"
FIXTURES = os.path.join(HERE, "fixtures")


class ZombieLifecycle(unittest.TestCase):
    """Drive cmd_wait in-process with proc_alive forced True (zombie-like),
    so only the persisted exit-code file can produce completion."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="v102-")
        self.repo = os.path.join(self._tmp, "repo")
        self.run_dir = os.path.join(self.repo, "audit-output",
                                    "audit-council", "20260903T000000Z-aa01bb")
        for sub in ("prompts", os.path.join("logs", "jobs")):
            os.makedirs(os.path.join(self.run_dir, sub), exist_ok=True)
        self.state = {
            "schema_version": 1, "run_id": "20260903T000000Z-aa01bb",
            "phase": "CONTRACT_FROZEN", "completeness_state": "RUNNING",
            "created_at": "2026-09-03T00:00:00Z", "timestamps": {},
            "repo_fingerprint_sha256": "deadbeefdeadbeef",
            "repo_root": self.repo,
            "codex": {"session_id": None, "jobs": [],
                      "stage_counts": {"independent": 0,
                                       "cross_examination": 0,
                                       "adjudication": 0}},
            "phase_attempts": {}, "failure_reason": None,
            "adjudication_skipped": False,
        }
        self._write_state()

    def _write_state(self):
        with open(os.path.join(self.run_dir, "state.json"), "w") as f:
            json.dump(self.state, f)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _load_job(self, job: dict) -> dict:
        with open(self._job_path(job)) as f:
            return json.load(f)

    def _launch_fake(self, mode: str, wait_for_completion=True) -> dict:
        """Launch the shipped fake codex through the runner, then wait for the
        wrapper's exit-code file with the REAL liveness check, so the job is
        genuinely finished before we simulate the zombie condition."""
        prompt = os.path.join(self.run_dir, "prompts", "codex-independent.md")
        with open(prompt, "w") as f:
            f.write("prompt\n")
        env = dict(os.environ, FAKE_CODEX_MODE=mode,
                   CODEX_RUNNER_POLL_INTERVAL="0.02",
                   FAKE_CODEX_SLEEP="5")
        proc = subprocess.run(
            [PYTHON, os.path.join(SCRIPTS, "codex_runner.py"),
             "start", "--run", self.run_dir, "--phase", "independent",
             "--codex-bin", os.path.join(FIXTURES, "fake_codex.py")],
            input="prompt\n", capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        job_path = proc.stdout.strip()
        with open(job_path) as f:
            job = json.load(f)
        if wait_for_completion:
            # wait for real completion of the detached wrapper
            for _ in range(500):
                if os.path.isfile(job["exit_code_path"]):
                    break
                if not codex_runner.proc_alive(job["pid"]):
                    break
                time.sleep(0.02)
        return job

    def _wait_zombie(self, job: dict, timeout=5):
        """Run cmd_wait with liveness pinned True — the OS-level zombie
        condition (kill(pid,0) succeeds on unreaped dead processes)."""
        ns = mock.Mock(job=self._job_path(job), timeout=timeout)
        out = io.StringIO()
        with mock.patch.object(codex_runner, "proc_alive",
                               return_value=True), \
                contextlib.redirect_stdout(out):
            rc = codex_runner.cmd_wait(ns)
        return rc, json.loads(out.getvalue().strip().splitlines()[-1])

    def _job_path(self, job: dict) -> str:
        return os.path.join(self.run_dir, "logs", "jobs",
                            "%s.json" % job["job_id"])

    def test_exit_code_file_with_alive_pid_finalizes_not_running(self):
        job = self._launch_fake("ok")
        self.assertTrue(os.path.isfile(job["exit_code_path"]),
                        "wrapper exit-code file missing")
        rc, out = self._wait_zombie(job)
        self.assertEqual(out["status"], "COMPLETE", out)
        self.assertEqual(out["exit_code"], 0)
        self.assertEqual(rc, 0)

    def test_quota_zombie_classifies_quota(self):
        job = self._launch_fake("quota")
        rc, out = self._wait_zombie(job)
        self.assertEqual(out["status"], "QUOTA", out)
        self.assertEqual(rc, 2)
        # failed stage not counted as successful
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["codex"]["stage_counts"]["independent"], 0)

    def test_auth_zombie_classifies_auth_error(self):
        job = self._launch_fake("auth")
        rc, out = self._wait_zombie(job)
        self.assertEqual(out["status"], "AUTH_ERROR", out)
        self.assertEqual(rc, 3)
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["codex"]["stage_counts"]["independent"], 0)

    def test_failed_zombie_classifies_failed(self):
        job = self._launch_fake("crash")
        rc, out = self._wait_zombie(job)
        self.assertEqual(out["status"], "FAILED", out)
        self.assertEqual(rc, 1)

    def test_genuinely_running_returns_running_after_timeout(self):
        job = self._launch_fake("slow", wait_for_completion=False)
        rc, out = self._wait_zombie(job, timeout=1)
        self.assertEqual(out["status"], "RUNNING", out)
        self.assertEqual(rc, 7)
        # cleanup: cancel for real
        ns = mock.Mock(job=self._job_path(job))
        with mock.patch.object(codex_runner, "proc_alive",
                               return_value=False):
            codex_runner.cmd_cancel(ns)

    def test_gone_process_missing_exit_file_classifies_failed(self):
        """Secondary signal, failure side: process reaped (proc_alive False)
        and the exit-code file never appears -> the bounded grace loop
        exhausts and the job finalizes FAILED with exit_code null."""
        job = self._launch_fake("ok")
        os.remove(job["exit_code_path"])  # simulate the lost-wrapper race
        ns = mock.Mock(job=self._job_path(job), timeout=10)
        buf = io.StringIO()
        with mock.patch.object(codex_runner, "proc_alive",
                               return_value=False), \
                contextlib.redirect_stdout(buf):
            rc = codex_runner.cmd_wait(ns)
        last = json.loads(buf.getvalue().strip().splitlines()[-1])
        self.assertEqual(last["status"], "FAILED", last)
        self.assertIsNone(last["exit_code"])
        self.assertEqual(rc, 1)
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["codex"]["stage_counts"]["independent"], 0)

    def test_zombie_without_exit_file_stays_running(self):
        """Zombie-pinned liveness + no exit-code file: no authoritative
        signal exists, so the bounded timeout must yield RUNNING."""
        job = self._launch_fake("ok")
        os.remove(job["exit_code_path"])
        rc, out = self._wait_zombie(job, timeout=1)
        self.assertEqual(out["status"], "RUNNING", out)
        self.assertEqual(rc, 7)

    def test_gone_process_with_persisted_exit_file_finalizes(self):
        """Secondary signal: reaped process (proc_alive False) with an
        already-persisted exit code finalizes through the grace path."""
        job = self._launch_fake("ok")
        ns = mock.Mock(job=self._job_path(job), timeout=5)
        out = io.StringIO()
        with mock.patch.object(codex_runner, "proc_alive",
                               return_value=False), \
                contextlib.redirect_stdout(out):
            rc = codex_runner.cmd_wait(ns)
        last = json.loads(out.getvalue().strip().splitlines()[-1])
        self.assertEqual(last["status"], "COMPLETE", last)
        self.assertEqual(rc, 0)

    def test_grace_loop_recovers_late_written_exit_code(self):
        """The race the grace loop exists for: process reaped, exit-code
        file NOT yet visible when cmd_wait starts, wrapper-equivalent writer
        creates it ~0.5s later -> the grace loop must find it and finalize
        (FAILED for a non-zero code) rather than exhaust or run forever."""
        job = self._launch_fake("crash")
        code = open(job["exit_code_path"]).read().strip()
        os.remove(job["exit_code_path"])
        timer = threading.Timer(0.5, lambda: open(
            job["exit_code_path"], "w").write(code))
        timer.start()
        ns = mock.Mock(job=self._job_path(job), timeout=10)
        buf = io.StringIO()
        try:
            with mock.patch.object(codex_runner, "proc_alive",
                                   return_value=False), \
                    contextlib.redirect_stdout(buf):
                rc = codex_runner.cmd_wait(ns)
        finally:
            timer.join()
        last = json.loads(buf.getvalue().strip().splitlines()[-1])
        self.assertEqual(last["status"], "FAILED", last)
        self.assertEqual(str(last["exit_code"]), code)
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
