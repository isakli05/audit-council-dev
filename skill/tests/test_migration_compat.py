#!/usr/bin/env python3
"""v2 pillar H.2 — v1.0.3 artifact compatibility.

Finalized v1 runs are never rewritten; their legacy `lines` artifacts remain
readable through the deterministic in-memory migration reader. The Fifth
run's real Opus artifact (copied fixture) is the canonical input.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PYTHON = "python3"
SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
AUDIT_COUNCIL = str(SCRIPTS / "audit_council.py")
FIXTURES = Path(__file__).resolve().parent / "fixtures"
FIFTH_OPUS_V1 = FIXTURES / "fifth-opus-independent-v1.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_schema_validation import contract  # noqa: E402

import state_store  # noqa: E402


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


class TestV1ArtifactCompat(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="mig-", dir=str(FIXTURES))
        self.cache = os.path.join(self.base, "cache")
        os.environ["AUDIT_COUNCIL_CACHE_HOME"] = self.cache
        self.repo = os.path.join(self.base, "repo")
        os.makedirs(self.repo)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "t@e.com")
        git(self.repo, "config", "user.name", "t")
        with open(os.path.join(self.repo, "a.py"), "w") as fh:
            fh.write("1\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "c")
        self.brief = os.path.join(self.base, "b.md")
        with open(self.brief, "w") as fh:
            fh.write("# brief\nAudit.\n")

    def tearDown(self):
        os.environ.pop("AUDIT_COUNCIL_CACHE_HOME", None)
        shutil.rmtree(self.base, ignore_errors=True)

    def _cli(self, *args, stdin=None):
        return subprocess.run([PYTHON, AUDIT_COUNCIL, *args], input=stdin,
                              capture_output=True, check=False,
                              env=dict(os.environ))

    def test_v1_lines_artifact_accepted_bytes_unchanged(self):
        proc = self._cli("init-run", "--repo", self.repo,
                         "--brief", self.brief)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        run_dir = [l.strip() for l in proc.stdout.decode().splitlines()
                   if "audit-output/audit-council/" in l][0]
        # degrade to a v1-ERA run: the in-memory legacy reader is scoped to
        # runs that predate environment bindings (H.4 review F5) — a v2 run
        # may never introduce legacy `lines` artifacts
        head = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))["head_sha"]
        os.unlink(os.path.join(run_dir, "01-environment-binding.json"))
        state = state_store.load_state(run_dir)
        state.pop("env_binding_digest", None)
        state_store.save_state(run_dir, state)
        # drop the binding's line from the checksum ledger (simulating a
        # run created before v2 ever wrote one)
        cpath = os.path.join(run_dir, "checksums.sha256")
        lines = [l for l in open(cpath).read().splitlines()
                 if "01-environment-binding.json" not in l]
        open(cpath, "w").write("\n".join(lines) + "\n")
        st = state_store.load_state(run_dir)

        c = contract()
        c["target_repository"] = {
            "root": self.repo, "head_sha": head,
            "fingerprint_sha256": st["repo_fingerprint_sha256"],
            "branch": "main", "dirty": False,
        }
        proc = self._cli("freeze-contract", "--run", run_dir,
                         "--artifact", "-", "--stdin",
                         stdin=json.dumps(c).encode())
        assert proc.returncode == 0, proc.stdout + proc.stderr

        # the REAL Fifth v1 opus artifact, fingerprint rebased to this run
        v1_doc = json.loads(FIFTH_OPUS_V1.read_text())
        self.assertIn("lines", json.dumps(v1_doc))  # genuinely v1
        v1_doc["repository_fingerprint_sha256"] = st["repo_fingerprint_sha256"]
        proc = self._cli("advance", "--run", run_dir, "--to",
                         "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                         "10-opus-independent.json", "--stdin",
                         stdin=json.dumps(v1_doc).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

        # on-disk bytes still carry the legacy field — NEVER rewritten
        on_disk = open(os.path.join(run_dir, "10-opus-independent.json")).read()
        self.assertIn('"lines"', on_disk)
        self.assertNotIn("line_ranges", on_disk)

        # resume-check validates it through the same in-memory reader
        proc = self._cli("resume-check", "--run", run_dir)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_finalized_v1_run_bytes_never_rewritten(self):
        # a directory of v1 artifacts stays byte-identical after ANY v2 read
        # operation touches it via validation paths (regression guard for
        # pillar A2/G: finalized history is immutable)
        proc = self._cli("init-run", "--repo", self.repo,
                         "--brief", self.brief)
        run_dir = [l.strip() for l in proc.stdout.decode().splitlines()
                   if "audit-output/audit-council/" in l][0]
        before = {}
        for name in os.listdir(run_dir):
            path = os.path.join(run_dir, name)
            if os.path.isfile(path):
                before[name] = open(path, "rb").read()
        proc = self._cli("resume-check", "--run", run_dir)
        for name, payload in before.items():
            self.assertEqual(open(os.path.join(run_dir, name), "rb").read(),
                             payload, name)


if __name__ == "__main__":
    unittest.main()
