#!/usr/bin/env python3
"""Lead Task A0.6 — environment gate wired into the run lifecycle.

The A0.6 regression matrix from the program spec (environment integrity is a
hard 100% requirement):
  - stale live-repo path in brief cannot redirect        -> root_mismatch tests
  - HEAD mismatch -> zero model calls                    -> head_mismatch test
  - correct detached worktree passes end-to-end          -> fake_codex e2e
  - quoted historical path as inert evidence allowed     -> inert prose test
  - binding reconstructs identically after restart       -> resume-check test
  - root/HEAD consistency gate before ANY inference      -> advance/start refusals
  - no .git-directory sniffing in repository discovery   -> grep test
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

PYTHON = "python3"  # NOT sys.executable (may be an embedded app host)

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

AUDIT_COUNCIL = str(SCRIPTS / "audit_council.py")
CODEX_RUNNER = str(SCRIPTS / "codex_runner.py")
FIXTURES = Path(__file__).resolve().parent / "fixtures"
FAKE_CODEX = str(FIXTURES / "fake_codex.py")
SCHEMAS_DIR = SCRIPTS.parent / "schemas"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_schema_validation import contract, independent_audit  # noqa: E402

import state_store  # noqa: E402
import validate_artifact  # noqa: E402


def git(repo: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(f"git {args} failed: {proc.stderr}")
    return proc.stdout


def make_repo(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    git(path, "init", "-q", "-b", "main")
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    with open(os.path.join(path, "src.py"), "w") as fh:
        fh.write("VALUE = 1\n")
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "init")
    return path


def cli(script: str, *args: str, stdin: bytes | None = None,
        env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([PYTHON, script, *args], input=stdin,
                          capture_output=True, check=False, env=env)


class EnvLifecycleBase(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="a0-lifecycle-",
                                     dir=str(FIXTURES))
        self.cache_root = os.path.join(self.base, "cache-home")
        os.environ["AUDIT_COUNCIL_CACHE_HOME"] = self.cache_root
        self.repo = make_repo(os.path.join(self.base, "repo"))
        self.legacy = make_repo(os.path.join(self.base, "legacy"))
        self.legacy_head = git(self.legacy, "rev-parse", "HEAD").strip()
        self.brief = os.path.join(self.base, "brief.md")
        with open(self.brief, "w") as fh:
            fh.write("# brief\nAudit everything.\n")

    def tearDown(self):
        os.environ.pop("AUDIT_COUNCIL_CACHE_HOME", None)
        shutil.rmtree(self.base, ignore_errors=True)

    # -- helpers -----------------------------------------------------------
    def ac(self, *args, stdin=None):
        return cli(AUDIT_COUNCIL, *args, stdin=stdin,
                   env=dict(os.environ))

    def cr(self, *args, stdin=None):
        return cli(CODEX_RUNNER, *args, stdin=stdin,
                   env=dict(os.environ))

    def init_run(self, brief: str | None = None) -> str:
        proc = self.ac("init-run", "--repo", self.repo,
                       "--brief", brief or self.brief)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        for line in proc.stdout.decode().splitlines():
            if re.match(r"^\S*audit-output/audit-council/"
                        r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}$", line):
                return line.strip()
        raise AssertionError(f"no run dir in stdout: {proc.stdout!r}")

    def state(self, run_dir):
        return state_store.load_state(run_dir)

    def active_run_files(self):
        # cache_root() == AUDIT_COUNCIL_CACHE_HOME verbatim (the override IS
        # the audit-council cache root); active-runs lives directly under it
        d = os.path.join(self.cache_root, "active-runs")
        return sorted(os.listdir(d)) if os.path.isdir(d) else []


class TestBindingLifecycle(EnvLifecycleBase):
    def test_init_run_persists_binding_and_registers_active_run(self):
        run_dir = self.init_run()
        binding_path = os.path.join(run_dir, "01-environment-binding.json")
        self.assertTrue(os.path.isfile(binding_path))
        binding = json.load(open(binding_path))
        errors = validate_artifact.validate(
            binding, json.load(open(os.path.join(
                SCHEMAS_DIR, "env-binding.schema.json"))),
            base_dir=SCHEMAS_DIR)
        self.assertEqual(errors, [])
        self.assertEqual(binding["repo_root_realpath"],
                         os.path.realpath(self.repo))
        self.assertIsNone(binding["brief_target"]["declared_repository_root"])
        # state carries the binding digest
        self.assertEqual(self.state(run_dir).get("env_binding_digest"),
                         binding["binding_digest"])
        # active-run registry under the INJECTED cache root (never ~/.cache)
        self.assertEqual(len(self.active_run_files()), 1)
        # the active-run registry file carries the run dir path
        reg = os.path.join(self.cache_root, "active-runs",
                           self.active_run_files()[0])
        lines = open(reg).read().strip().splitlines()
        self.assertEqual(lines[0], run_dir)
        self.assertEqual(lines[1], binding["binding_digest"])
        # binding is checksummed
        mismatches = state_store.verify_all(run_dir)
        self.assertEqual(mismatches, [])

    def test_root_mismatch_blocks_all_inference(self):
        brief = os.path.join(self.base, "brief-target.md")
        with open(brief, "w") as fh:
            # NOTE: plain concatenation — f-string '}}' would collapse to '}'
            fh.write('# brief\n```json\n{"target": {"repository_root": "'
                     + self.legacy + '", "expected_head": "'
                     + self.legacy_head + '"}}\n```\nAudit.\n')
        run_dir = self.init_run(brief)
        binding = json.load(open(os.path.join(run_dir,
                                              "01-environment-binding.json")))
        self.assertEqual(binding["brief_target"]["declared_repository_root"],
                         self.legacy)

        # verify-env fails closed with the precise reason
        proc = self.ac("verify-env", "--run", run_dir)
        self.assertEqual(proc.returncode, 10)
        self.assertIn("BRIEF_ROOT_MISMATCH", proc.stdout.decode())

        # advance to an inference phase refuses (env gate before staging)
        artifact = json.dumps(independent_audit(
            repository_fingerprint_sha256=self.state(
                run_dir)["repo_fingerprint_sha256"]))
        proc = self.ac("advance", "--run", run_dir,
                       "--to", "OPUS_INDEPENDENT_COMPLETE",
                       "--artifact", "-", "--stdin",
                       stdin=artifact.encode())
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("INVALID_AUDIT_ENVIRONMENT", proc.stdout.decode())
        self.assertEqual(self.state(run_dir)["completeness_state"],
                         "INVALID_AUDIT_ENVIRONMENT")

        # codex start refuses at the governor level: ZERO launches
        proc = self.cr("start", "--run", run_dir, "--phase", "independent",
                       "--prompt", "-", "--codex-bin", FAKE_CODEX,
                       stdin=b"prompt")
        self.assertEqual(proc.returncode, 3)
        self.assertIn("INVALID_AUDIT_ENVIRONMENT", proc.stderr.decode())
        jobs_dir = os.path.join(run_dir, "logs", "jobs")
        self.assertEqual(os.listdir(jobs_dir), [])

    def test_head_mismatch_blocks_all_inference(self):
        wrong_head = "0" * 40
        brief = os.path.join(self.base, "brief-head.md")
        with open(brief, "w") as fh:
            fh.write('# brief\n```json\n{"target": {"repository_root": "'
                     + self.repo + '", "expected_head": "'
                     + wrong_head + '"}}\n```\nAudit.\n')
        run_dir = self.init_run(brief)
        proc = self.ac("verify-env", "--run", run_dir)
        self.assertEqual(proc.returncode, 10)
        self.assertIn("BRIEF_HEAD_MISMATCH", proc.stdout.decode())
        proc = self.cr("start", "--run", run_dir, "--phase", "independent",
                       "--prompt", "-", "--codex-bin", FAKE_CODEX,
                       stdin=b"prompt")
        self.assertEqual(proc.returncode, 3)

    def test_inert_prose_paths_do_not_block(self):
        brief = os.path.join(self.base, "brief-prose.md")
        with open(brief, "w") as fh:
            fh.write("# brief\nHistorical context: the old repository at "
                     f"{self.legacy} was audited yesterday.\nAudit.\n")
        run_dir = self.init_run(brief)
        proc = self.ac("verify-env", "--run", run_dir)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout.decode()), {"ok": True})

    def test_finalize_unregisters_active_run(self):
        run_dir = self.init_run()
        self.assertEqual(len(self.active_run_files()), 1)
        # drive to FINALIZED via contract + artifacts (fast path: contract +
        # opus artifact + final), then finalize
        st = self.state(run_dir)
        c = contract()
        c["target_repository"] = {
            "root": self.repo,
            "head_sha": json.load(open(os.path.join(
                run_dir, "01-environment-binding.json")))["head_sha"],
            "fingerprint_sha256": st["repo_fingerprint_sha256"],
            "branch": "main", "dirty": False,
        }
        proc = self.ac("freeze-contract", "--run", run_dir, "--artifact", "-",
                       "--stdin", stdin=json.dumps(c).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        self.ac("advance", "--run", run_dir, "--to",
                "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                "10-opus-independent.json", "--stdin",
                stdin=json.dumps(ia).encode())
        # the ledger must exist before FINALIZED (never silently passed
        # over); the jump past the Codex stages carries EXPLICIT skip
        # records (v2 H.1)
        proc = self.ac("advance", "--run", run_dir, "--to", "LEDGER_COMPLETE",
                       "--artifact", "40-disagreement-ledger.json", "--stdin",
                       "--skip", "CODEX_INDEPENDENT_COMPLETE=quota: stage "
                                "deferred (test scaffold)",
                       "--skip", "NORMALIZED=no second-model findings to "
                                 "normalize (test scaffold)",
                       "--skip", "OPUS_CROSS_EXAM_COMPLETE=deferred with "
                                 "codex stage (test scaffold)",
                       "--skip", "CODEX_CROSS_EXAM_COMPLETE=quota: stage "
                                 "deferred (test scaffold)",
                       stdin=json.dumps({"clusters": []}).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        st2 = self.state(run_dir)
        self.assertEqual(len(st2.get("phase_skips", [])), 4)
        final = {
            "completeness_state": "PARTIAL_CLAUDE_INTERRUPTION",
            "repository_fingerprint_sha256":
                st["repo_fingerprint_sha256"],
            "executive_summary": "s",
            "findings": [],
        }
        self.ac("advance", "--run", run_dir, "--to", "FINALIZED",
                "--artifact", "90-final-findings.json", "--stdin",
                stdin=json.dumps(final).encode())
        proc = self.ac("finalize", "--run", run_dir, "--completeness",
                       "PARTIAL_CLAUDE_INTERRUPTION")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(self.active_run_files(), [])

    def test_freeze_contract_root_mismatch_rejected(self):
        run_dir = self.init_run()
        st = self.state(run_dir)
        c = contract()
        c["target_repository"] = {
            "root": self.legacy,  # points at the WRONG repository
            "head_sha": json.load(open(os.path.join(
                run_dir, "01-environment-binding.json")))["head_sha"],
            "fingerprint_sha256": st["repo_fingerprint_sha256"],
            "branch": "main", "dirty": False,
        }
        proc = self.ac("freeze-contract", "--run", run_dir, "--artifact", "-",
                       "--stdin", stdin=json.dumps(c).encode())
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("BRIEF_ROOT_MISMATCH", proc.stdout.decode())
        # control: correct root passes the env check (freeze succeeds)
        c["target_repository"]["root"] = self.repo
        proc = self.ac("freeze-contract", "--run", run_dir, "--artifact", "-",
                       "--stdin", stdin=json.dumps(c).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


class TestResumeBinding(EnvLifecycleBase):
    def test_resume_check_reconstructs_binding(self):
        run_dir = self.init_run()
        # simulate restart: registry entry lost; resume-check must re-register
        # and confirm the binding reconstructs identically
        reg = os.path.join(self.cache_root, "active-runs")
        for name in os.listdir(reg):
            os.unlink(os.path.join(reg, name))
        proc = self.ac("resume-check", "--run", run_dir)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout.decode())
        self.assertEqual(doc.get("environment_binding"), "ok")
        self.assertEqual(len(self.active_run_files()), 1)


class TestDetachedWorktreeE2E(EnvLifecycleBase):
    def test_detached_worktree_fake_codex_completes(self):
        wt = os.path.join(self.base, "wt")
        git(self.repo, "worktree", "add", "--detach", wt)
        brief = os.path.join(self.base, "brief-wt.md")
        with open(brief, "w") as fh:
            fh.write("# brief\nAudit the worktree.\n")
        proc = self.ac("init-run", "--repo", wt, "--brief", brief)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        run_dir = [line.strip() for line in proc.stdout.decode().splitlines()
                   if "audit-output/audit-council/" in line][0]
        binding = json.load(open(os.path.join(run_dir,
                                              "01-environment-binding.json")))
        self.assertTrue(binding["detached_head"])

        # environment gate passes for the correct detached worktree
        proc = self.ac("verify-env", "--run", run_dir)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

        # full fake-codex stage: launch + wait COMPLETE inside the worktree
        os.environ["FAKE_CODEX_FINGERPRINT"] = self.state(run_dir)[
            "repo_fingerprint_sha256"]
        os.environ["CODEX_RUNNER_POLL_INTERVAL"] = "0.05"
        try:
            proc = self.cr("start", "--run", run_dir, "--phase", "independent",
                           "--prompt", "-", "--codex-bin", FAKE_CODEX,
                           stdin=b"prompt")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            job_path = proc.stdout.decode().strip().splitlines()[-1]
            proc = self.cr("wait", job_path, "--timeout", "30")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual(
                self.state(run_dir)["codex"]["stage_counts"]["independent"],
                1)
        finally:
            os.environ.pop("FAKE_CODEX_FINGERPRINT", None)
            os.environ.pop("CODEX_RUNNER_POLL_INTERVAL", None)


class TestNoGitDirSniffing(unittest.TestCase):
    def test_no_isdir_git_discovery_in_scripts(self):
        offenders = []
        for path in sorted((SCRIPTS).glob("*.py")):
            for i, line in enumerate(path.read_text().splitlines(), 1):
                if "isdir" in line and '".git"' in line:
                    offenders.append(f"{path.name}:{i}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
