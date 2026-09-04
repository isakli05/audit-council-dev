#!/usr/bin/env python3
"""Tests for the source write guard (scenarios F/P) via audit_council.py."""
from __future__ import annotations

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

AUDIT_COUNCIL = str(SCRIPTS / "audit_council.py")


def git(repo: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(f"git {args} failed: {proc.stderr}")
    return proc.stdout


def make_repo(tmp: str) -> str:
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    with open(os.path.join(repo, "src.py"), "w") as fh:
        fh.write("VALUE = 1\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "init")
    return repo


def init_run(repo: str, tmp: str) -> str:
    brief = os.path.join(tmp, "brief.md")
    with open(brief, "w") as fh:
        fh.write("# brief\nAudit everything.\n")
    proc = subprocess.run(
        [PYTHON, AUDIT_COUNCIL, "init-run", "--repo", repo,
         "--brief", brief],
        capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    pat = re.compile(r"^\S*audit-output/audit-council/"
                     r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}\s*$")
    for line in proc.stdout.splitlines():
        if pat.match(line):
            return line.strip()
    raise AssertionError(f"no run dir in stdout: {proc.stdout!r}")


def write_guard(run_dir: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, AUDIT_COUNCIL, "write-guard", "--run", run_dir],
        capture_output=True, text=True, check=False)


class TestSourceWriteGuard(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(self._tmp.name)
        self.run_dir = init_run(self.repo, self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_run_dir_layout(self):
        for name in ("00-run-manifest.json", "01-repository-state.json",
                     "state.json", "checksums.sha256", "prompts", "logs",
                     os.path.join("logs", "jobs")):
            self.assertTrue(
                os.path.exists(os.path.join(self.run_dir, name)),
                f"missing {name}")
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["phase"], "CREATED")
        self.assertEqual(state["completeness_state"], "RUNNING")

    def test_no_changes_exit_0(self):
        proc = write_guard(self.run_dir)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(json.loads(proc.stdout)["ok"])

    def test_modified_source_exit_5_and_not_reset(self):
        # scenarios F and P: violation detected, file left untouched
        target = os.path.join(self.repo, "src.py")
        with open(target, "w") as fh:
            fh.write("VALUE = 2  # mutated by something during the audit\n")
        proc = write_guard(self.run_dir)
        self.assertEqual(proc.returncode, 5)
        doc = json.loads(proc.stdout)
        self.assertFalse(doc["ok"])
        paths = [v["path"] for v in doc["violations"]]
        self.assertIn("src.py", paths)
        # guard must not delete/reset the mutation
        with open(target) as fh:
            self.assertIn("VALUE = 2", fh.read())
        # still violating on re-run
        self.assertEqual(write_guard(self.run_dir).returncode, 5)

    def test_run_dir_writes_are_not_violations(self):
        # writing artifacts inside the run dir must be allowed
        with open(os.path.join(self.run_dir, "30-normalized-findings.json"),
                  "w") as fh:
            fh.write('{"clusters": []}')
        proc = write_guard(self.run_dir)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_pre_existing_dirty_file_not_a_violation(self):
        # dirty BEFORE the audit baseline is part of the audited state
        with open(os.path.join(self.repo, "src.py"), "a") as fh:
            fh.write("# pre-existing dirt\n")
        run_dir2 = init_run(self.repo, self._tmp.name)  # baseline includes dirt
        proc = write_guard(run_dir2)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_new_untracked_source_is_violation(self):
        with open(os.path.join(self.repo, "evil.py"), "w") as fh:
            fh.write("x = 1\n")
        proc = write_guard(self.run_dir)
        self.assertEqual(proc.returncode, 5)
        paths = [v["path"] for v in json.loads(proc.stdout)["violations"]]
        self.assertIn("evil.py", paths)


if __name__ == "__main__":
    unittest.main()
