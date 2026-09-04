#!/usr/bin/env python3
"""A0 codex-confinement wrapper regressions (docs/A0-CODEX-CONFINEMENT.md).

Real bubblewrap invocations, deterministic payloads, NO model calls:
outside-bind-set reads must be OS-BLOCKED; repo reads, run-dir writes,
auth/toolchain access must keep working; the wiring must cover fresh AND
resume argv; opt-out must be honest.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import codex_sandbox  # noqa: E402

HAVE_BWRAP = codex_sandbox.bwrap_available()


@unittest.skipUnless(HAVE_BWRAP, "bubblewrap not available")
class TestBwrapBoundary(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="sbx-", dir=os.path.join(
            Path(__file__).resolve().parent, "fixtures"))
        self.repo = os.path.join(self.base, "repo")
        self.run_dir = os.path.join(self.repo, "audit-output", "run")
        os.makedirs(os.path.join(self.repo, "src"))
        os.makedirs(self.run_dir)
        with open(os.path.join(self.repo, "src", "a.py"), "w") as fh:
            fh.write("x = 1\n")

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def _run(self, payload_argv, allowed=None):
        argv = codex_sandbox.build_sandbox_argv(
            payload_argv, self.repo, self.run_dir, allowed or [])
        return subprocess.run(argv, capture_output=True, text=True,
                              check=False)

    def test_outside_read_os_blocked(self):
        # a file OUTSIDE the bind set (sibling of the repo)
        outside = os.path.join(self.base, "outside-secret.txt")
        with open(outside, "w") as fh:
            fh.write("secret\n")
        proc = self._run(["/usr/bin/cat", outside])
        self.assertNotEqual(proc.returncode, 0,
                            "outside read escaped the OS boundary")

    def test_repo_read_ok(self):
        proc = self._run(["/usr/bin/cat",
                          os.path.join(self.repo, "src", "a.py")])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_run_dir_write_ok(self):
        target = os.path.join(self.run_dir, "out.json")
        proc = self._run(["/usr/bin/sh", "-c", "echo '{}' > " + target])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(os.path.isfile(target))

    def test_repo_source_write_os_blocked(self):
        src = os.path.join(self.repo, "src", "evil.txt")
        proc = self._run(["/usr/bin/sh", "-c", "echo x > " + src])
        self.assertNotEqual(proc.returncode, 0,
                            "repo write escaped the OS boundary")
        self.assertFalse(os.path.isfile(src))

    def test_unauthorized_tmp_absent_authorized_fixture_bound(self):
        probe = tempfile.mkdtemp(prefix="sbx-fx-")  # NOT under allowed roots
        try:
            with open(os.path.join(probe, "f.txt"), "w") as fh:
                fh.write("x\n")
            proc = self._run(["/usr/bin/cat",
                              os.path.join(probe, "f.txt")])
            self.assertNotEqual(proc.returncode, 0,
                                "unauthorized /tmp path readable")
            # authorized fixture root IS readable
            proc = self._run(["/usr/bin/cat",
                              os.path.join(probe, "f.txt")],
                             allowed=[probe])
            self.assertEqual(proc.returncode, 0, proc.stderr)
        finally:
            shutil.rmtree(probe, ignore_errors=True)

    def test_wrapper_shape_fresh_and_resume(self):
        fresh = ["codex", "exec", "-C", self.repo, "--sandbox",
                 "read-only", "-o", os.path.join(self.run_dir, "o.json"),
                 "-"]
        resume = ["codex", "exec", "resume", "sess-1", "-o",
                  os.path.join(self.run_dir, "o2.json"), "-"]
        for base in (fresh, resume):
            wrapped = codex_sandbox.build_sandbox_argv(
                base, self.repo, self.run_dir, [])
            self.assertEqual(wrapped[0], HAVE_BWRAP)  # resolved bwrap path
            self.assertIn("--ro-bind", wrapped)
            self.assertIn(self.repo, wrapped)
            # the payload argv is preserved verbatim at the tail
            self.assertEqual(wrapped[-len(base):], base)

    def test_opt_out_honest(self):
        env = dict(os.environ, AC_CODEX_BWRAP="0")
        import importlib
        old = os.environ.get("AC_CODEX_BWRAP")
        os.environ["AC_CODEX_BWRAP"] = "0"
        try:
            argv, active = codex_sandbox.wrap_codex_argv(
                ["codex", "exec"], self.repo, self.run_dir, [])
            self.assertFalse(active)
            self.assertEqual(argv, ["codex", "exec"])
        finally:
            if old is None:
                os.environ.pop("AC_CODEX_BWRAP", None)
            else:
                os.environ["AC_CODEX_BWRAP"] = old

    def test_capability_probe(self):
        result = codex_sandbox.probe()
        self.assertTrue(result["available"])
        self.assertTrue(result["repo_read_ok"])
        self.assertTrue(result["outside_read_blocked"])


if __name__ == "__main__":
    unittest.main()
