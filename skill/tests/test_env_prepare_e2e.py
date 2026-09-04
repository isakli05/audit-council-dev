#!/usr/bin/env python3
"""v2 A1 user-facing environment preparation — end-to-end proofs.

The operator's required evidence, all through the real CLI, deterministic,
no model calls:
  RELEASE prepares a detached worktree at the EXACT requested HEAD;
  the live source tree is never touched; a same-HEAD alternate worktree
  cannot substitute; the environment record is linked into the run;
  archive-before-remove happens at finalize; resume keeps the same frozen
  worktree identity; HISTORICAL evidence allow/deny lists are enforced.
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
SCHEMAS_DIR = SCRIPTS.parent / "schemas"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_schema_validation import contract, independent_audit  # noqa: E402

import state_store  # noqa: E402
import validate_artifact  # noqa: E402


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


class PrepareE2E(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="prep-", dir=str(FIXTURES))
        os.environ["AUDIT_COUNCIL_CACHE_HOME"] = os.path.join(
            self.base, "cache")
        os.environ["AUDIT_COUNCIL_ENV_ROOT"] = os.path.join(
            self.base, "envroot")
        # source repo with TWO commits; we will audit the FIRST
        self.src = os.path.join(self.base, "src")
        os.makedirs(os.path.join(self.src, "docs"))
        git(self.src, "init", "-q", "-b", "main")
        git(self.src, "config", "user.email", "t@e.com")
        git(self.src, "config", "user.name", "t")
        with open(os.path.join(self.src, "docs", "notes.md"), "w") as fh:
            fh.write("release notes for A\n")
        with open(os.path.join(self.src, "a.py"), "w") as fh:
            fh.write("VALUE = 1\n")
        git(self.src, "add", "-A")
        git(self.src, "commit", "-q", "-m", "A")
        self.head_a = git(self.src, "rev-parse", "HEAD").strip()
        with open(os.path.join(self.src, "a.py"), "w") as fh:
            fh.write("VALUE = 2\n")
        git(self.src, "add", "-A")
        git(self.src, "commit", "-q", "-m", "B")
        self.head_b = git(self.src, "rev-parse", "HEAD").strip()
        self.brief = os.path.join(self.base, "brief.md")
        with open(self.brief, "w") as fh:
            fh.write("# brief\nAudit release A.\n")

    def tearDown(self):
        for var in ("AUDIT_COUNCIL_CACHE_HOME", "AUDIT_COUNCIL_ENV_ROOT"):
            os.environ.pop(var, None)
        # prune any worktrees our tests created so rmtree succeeds
        if os.path.isdir(self.src):
            subprocess.run(["git", "-C", self.src, "worktree", "prune"],
                           capture_output=True, check=False)
        shutil.rmtree(self.base, ignore_errors=True)

    # -- helpers -----------------------------------------------------------
    def ac(self, *args, stdin=None):
        return subprocess.run([PYTHON, AUDIT_COUNCIL, *args], input=stdin,
                              capture_output=True, check=False,
                              env=dict(os.environ))

    def prepare(self, *extra):
        proc = self.ac("prepare", "--repo", self.src,
                       "--brief", self.brief, *extra)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return json.loads(proc.stdout.decode())

    def run_dir_of(self, doc):
        return doc["run"]

    # -- proofs ------------------------------------------------------------
    def test_release_detached_worktree_exact_head_live_unchanged(self):
        porcelain_before = git(self.src, "status", "--porcelain")
        doc = self.prepare("--mode", "RELEASE", "--ref", self.head_a)
        run_dir = self.run_dir_of(doc)
        self.assertTrue(doc["worktree_root"])
        binding = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))
        # EXACT requested HEAD is the audited environment
        self.assertEqual(binding["head_sha"], self.head_a)
        self.assertNotEqual(binding["head_sha"], self.head_b)
        self.assertTrue(binding["detached_head"])
        # worktree is detached at A
        self.assertEqual(
            git(doc["worktree_root"], "rev-parse", "HEAD").strip(),
            self.head_a)
        # the LIVE tree is untouched: HEAD still B, porcelain unchanged
        self.assertEqual(
            git(self.src, "rev-parse", "HEAD").strip(), self.head_b)
        self.assertEqual(git(self.src, "status", "--porcelain"),
                         porcelain_before)
        # no branch was checked out in the live worktree
        self.assertIn("main", git(self.src, "branch",
                                  "--show-current"))

    def test_environment_record_linked_into_run(self):
        doc = self.prepare("--mode", "RELEASE", "--ref", self.head_a)
        run_dir = self.run_dir_of(doc)
        record_path = os.path.join(run_dir, "environment-record.json")
        self.assertTrue(os.path.isfile(record_path))
        record = json.load(open(record_path))
        errors = validate_artifact.validate(
            record, json.load(open(os.path.join(
                SCHEMAS_DIR, "environment-record.schema.json"))),
            base_dir=SCHEMAS_DIR)
        self.assertEqual(errors, [])
        self.assertEqual(record["mode"], "RELEASE")
        self.assertEqual(record["source_repo_realpath"],
                         os.path.realpath(self.src))
        self.assertEqual(state_store.verify_all(run_dir), [])

    def test_same_head_alternate_worktree_cannot_substitute(self):
        doc = self.prepare("--mode", "RELEASE", "--ref", self.head_a)
        run_dir = self.run_dir_of(doc)
        # attacker-style substitution: same HEAD, different worktree
        wt2 = os.path.join(self.base, "wt2")
        git(self.src, "worktree", "add", "--detach", wt2, self.head_a)
        stolen = os.path.join(wt2, os.path.relpath(
            run_dir, doc["worktree_root"]))
        os.makedirs(os.path.dirname(stolen), exist_ok=True)
        shutil.copytree(run_dir, stolen)
        proc = self.ac("verify-env", "--run", stolen)
        self.assertEqual(proc.returncode, 10,
                         "alternate same-HEAD worktree substituted the "
                         f"audit environment: {proc.stdout}")
        # the original run still verifies fine
        proc = self.ac("verify-env", "--run", run_dir)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_resume_uses_same_frozen_worktree_identity(self):
        doc = self.prepare("--mode", "RELEASE", "--ref", self.head_a)
        run_dir = self.run_dir_of(doc)
        binding = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))
        self.ac("resume-check", "--run", run_dir)
        binding2 = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))
        self.assertEqual(binding2["binding_digest"],
                         binding["binding_digest"])
        proc = self.ac("resume-check", "--run", run_dir)
        doc2 = json.loads(proc.stdout.decode())
        self.assertEqual(doc2.get("environment_binding"), "ok")

    def test_historical_evidence_allow_and_deny_enforced(self):
        doc = self.prepare("--mode", "HISTORICAL", "--ref", self.head_a,
                           "--evidence-allow", "docs/notes.md")
        record = json.load(open(os.path.join(
            doc["run"], "environment-record.json")))
        staged = [e["path"] for e in record.get("staged_evidence") or []]
        self.assertEqual(staged, ["docs/notes.md"])
        # deny-listed paths are always refused, allow-list or not
        proc = self.ac("prepare", "--repo", self.src, "--brief", self.brief,
                       "--mode", "HISTORICAL", "--ref", self.head_a,
                       "--evidence-allow", ".git/config")
        self.assertNotEqual(proc.returncode, 0, proc.stdout)
        proc = self.ac("prepare", "--repo", self.src, "--brief", self.brief,
                       "--mode", "HISTORICAL", "--ref", self.head_a,
                       "--evidence-allow", "audit-output/x")
        self.assertNotEqual(proc.returncode, 0, proc.stdout)

    def test_finalize_archives_before_removing_worktree(self):
        doc = self.prepare("--mode", "RELEASE", "--ref", self.head_a)
        run_dir = self.run_dir_of(doc)
        wt = doc["worktree_root"]
        st = state_store.load_state(run_dir)
        c = contract()
        binding = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))
        c["target_repository"] = {
            "root": wt, "head_sha": binding["head_sha"],
            "fingerprint_sha256": st["repo_fingerprint_sha256"],
            "branch": "HEAD", "dirty": False,
        }
        self.ac("freeze-contract", "--run", run_dir, "--artifact", "-",
                "--stdin", stdin=json.dumps(c).encode())
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        self.ac("advance", "--run", run_dir, "--to",
                "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                "10-opus-independent.json", "--stdin",
                stdin=json.dumps(ia).encode())
        self.ac("advance", "--run", run_dir, "--to", "LEDGER_COMPLETE",
                "--artifact", "40-disagreement-ledger.json", "--stdin",
                "--skip", "CODEX_INDEPENDENT_COMPLETE=deferred (t)",
                "--skip", "NORMALIZED=none (t)",
                "--skip", "OPUS_CROSS_EXAM_COMPLETE=deferred (t)",
                "--skip", "CODEX_CROSS_EXAM_COMPLETE=deferred (t)",
                stdin=json.dumps({"clusters": []}).encode())
        final = {"completeness_state": "PARTIAL_CODEX_QUOTA",
                 "repository_fingerprint_sha256":
                     st["repo_fingerprint_sha256"],
                 "executive_summary": "s", "findings": []}
        self.ac("advance", "--run", run_dir, "--to", "FINALIZED",
                "--artifact", "90-final-findings.json", "--stdin",
                stdin=json.dumps(final).encode())
        proc = self.ac("finalize", "--run", run_dir, "--completeness",
                       "PARTIAL_CODEX_QUOTA")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        out = json.loads(proc.stdout.decode())
        cleanup = out.get("environment_cleanup") or {}
        self.assertTrue(cleanup.get("archived"),
                        f"archive-before-remove failed: {out}")
        self.assertTrue(cleanup.get("worktree_removed"))
        # the ephemeral worktree is gone (git worktree remove, not rmtree)
        self.assertFalse(os.path.exists(wt))
        listing = git(self.src, "worktree", "list")
        self.assertNotIn(wt, listing)
        # the ARCHIVE preserves the run artifacts
        archive = os.path.join(cleanup["archive_root"],
                               st["run_id"])
        self.assertTrue(os.path.isfile(os.path.join(archive,
                                                    "state.json")))

    def test_brief_target_validation_against_prepared_environment(self):
        # a brief declaring the LIVE source root against a prepared
        # worktree environment is the Fifth-run failure mode: root
        # mismatch fires (the stale declaration cannot redirect anything)
        brief2 = os.path.join(self.base, "brief-target.md")
        with open(brief2, "w") as fh:
            fh.write('# brief\n```json\n{"target": {"repository_root": "'
                     + self.src + '", "expected_head": "'
                     + self.head_b + '"}}\n```\nAudit.\n')
        proc = self.ac("prepare", "--repo", self.src, "--brief", brief2,
                       "--mode", "RELEASE", "--ref", self.head_a)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        run_dir = json.loads(proc.stdout.decode())["run"]
        proc = self.ac("verify-env", "--run", run_dir)
        self.assertEqual(proc.returncode, 10)
        self.assertIn("BRIEF_ROOT_MISMATCH", proc.stdout.decode())
        # head-mismatch precedence (declared root matching the frozen root)
        # is proven in test_env_lifecycle.test_head_mismatch_blocks_all_

    def test_auto_safety_current_with_ref_refused(self):
        proc = self.ac("prepare", "--repo", self.src, "--brief", self.brief,
                       "--mode", "CURRENT", "--ref", self.head_a)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("AUTO-safety", proc.stdout.decode())


if __name__ == "__main__":
    unittest.main()
