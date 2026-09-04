#!/usr/bin/env python3
"""Tests for repo_fingerprint: capture/verify, stale detection (scenarios D,
E), audit-output exclusion, dirty-tree preservation."""
from __future__ import annotations

import os
import subprocess
import sys

PYTHON = "python3"  # NOT sys.executable (may be an embedded app host)
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import repo_fingerprint  # noqa: E402
import state_store  # noqa: E402


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
    with open(os.path.join(repo, "app.py"), "w") as fh:
        fh.write("print('hello')\n")
    with open(os.path.join(repo, "README.md"), "w") as fh:
        fh.write("# repo\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "init")
    return repo


def write_state(tmp: str, repo: str, fingerprint: dict) -> str:
    state_file = os.path.join(tmp, "01-repository-state.json")
    state_store.atomic_write_json(
        state_file,
        {"schema_version": 1, "captured_at": "now", "repo_root": repo,
         "brief_sha256": "0" * 64, "contract_sha256": None,
         "fingerprint": fingerprint})
    return state_file


class TestCaptureVerify(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(self._tmp.name)
        self.fp = repo_fingerprint.capture(self.repo)
        self.state_file = write_state(self._tmp.name, self.repo, self.fp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_capture_shape(self):
        self.assertRegex(self.fp["head_sha"], r"^[0-9a-f]{40}$")
        self.assertEqual(self.fp["branch"], "main")
        self.assertIn("app.py", self.fp["tracked_inventory"])
        self.assertIn("README.md", self.fp["tracked_inventory"])
        self.assertEqual(self.fp["fingerprint_sha256"],
                         repo_fingerprint.fingerprint_digest(self.fp))

    def test_verify_match(self):
        ok, diff = repo_fingerprint.verify(self.repo, self.state_file)
        self.assertTrue(ok)
        self.assertFalse(diff["changed"])

    def test_modified_tracked_file_is_stale(self):
        # scenario D
        with open(os.path.join(self.repo, "app.py"), "a") as fh:
            fh.write("print('modified')\n")
        ok, diff = repo_fingerprint.verify(self.repo, self.state_file)
        self.assertFalse(ok)
        self.assertIn("app.py", diff["porcelain_status_changes"])

    def test_new_untracked_file_outside_audit_output_is_stale(self):
        with open(os.path.join(self.repo, "scratch.txt"), "w") as fh:
            fh.write("x")
        ok, diff = repo_fingerprint.verify(self.repo, self.state_file)
        self.assertFalse(ok)
        self.assertIn("scratch.txt", diff["added_untracked"])

    def test_new_file_under_run_dir_is_not_stale(self):
        run_dir = os.path.join(self.repo, "audit-output", "audit-council",
                               "20260903T170000Z-a1b2c3")
        os.makedirs(run_dir)
        with open(os.path.join(run_dir, "state.json"), "w") as fh:
            fh.write("{}")
        ok, diff = repo_fingerprint.verify(self.repo, self.state_file)
        self.assertTrue(ok, msg=str(diff))

    def test_head_change_is_stale(self):
        with open(os.path.join(self.repo, "app.py"), "a") as fh:
            fh.write("# more\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "second")
        ok, diff = repo_fingerprint.verify(self.repo, self.state_file)
        self.assertFalse(ok)
        self.assertNotEqual(diff["head_sha"]["old"], diff["head_sha"]["new"])

    def test_dirty_tree_preserved_no_git_mutations(self):
        # scenario E: dirty state captured, verify runs, tree untouched
        with open(os.path.join(self.repo, "app.py"), "a") as fh:
            fh.write("# dirty\n")
        with open(os.path.join(self.repo, "untracked.txt"), "w") as fh:
            fh.write("u")
        dirty_fp = repo_fingerprint.capture(self.repo)
        dirty_state = write_state(self._tmp.name + "-dirty", self.repo,
                                  dirty_fp)
        before = git(self.repo, "status", "--porcelain")
        ok, _ = repo_fingerprint.verify(self.repo, dirty_state)
        after = git(self.repo, "status", "--porcelain")
        self.assertTrue(ok)
        self.assertEqual(before, after)
        # content still dirty, never reset
        with open(os.path.join(self.repo, "app.py")) as fh:
            self.assertIn("# dirty", fh.read())

    def test_cli_verify_exit_codes(self):
        rc0 = subprocess.run(
            [PYTHON, str(SCRIPTS / "repo_fingerprint.py"), "verify",
             "--repo", self.repo, "--state", self.state_file],
            capture_output=True, text=True)
        self.assertEqual(rc0.returncode, 0)
        with open(os.path.join(self.repo, "app.py"), "a") as fh:
            fh.write("# change\n")
        rc4 = subprocess.run(
            [PYTHON, str(SCRIPTS / "repo_fingerprint.py"), "verify",
             "--repo", self.repo, "--state", self.state_file],
            capture_output=True, text=True)
        self.assertEqual(rc4.returncode, 4)
        self.assertIn("app.py", rc4.stdout)


if __name__ == "__main__":
    unittest.main()
