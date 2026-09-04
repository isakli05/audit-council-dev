#!/usr/bin/env python3
"""H.4 adversarial-review hardening regressions (F1, F3, F4, F5, F6, F8).

Each test here is the permanent form of an attack the independent reviewer
successfully executed against the RC — the attack must now fail.
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

PYTHON = "python3"
SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
CODEX_RUNNER = str(SCRIPTS / "codex_runner.py")
AUDIT_COUNCIL = str(SCRIPTS / "audit_council.py")
FIXTURES = Path(__file__).resolve().parent / "fixtures"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_schema_validation import contract, independent_audit  # noqa: E402

import path_guard  # noqa: E402
import state_store  # noqa: E402


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


class TestF1InterpreterAndFlagSmuggling(unittest.TestCase):
    """The reviewer's exact escapes must be denied; benign usage allowed."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="f1-", dir=str(FIXTURES))
        self.root = os.path.join(self.base, "root")
        os.makedirs(os.path.join(self.root, "src"))
        self.outside = os.path.join(self.base, "outside")
        os.makedirs(self.outside)
        self.root = path_guard.canonicalize(self.root)
        self.outside = path_guard.canonicalize(self.outside)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def _deny(self, cmd):
        reasons = path_guard.scan_bash_command(cmd, self.root, self.root, [])
        self.assertTrue(reasons, f"expected denial for: {cmd}")

    def _allow(self, cmd):
        reasons = path_guard.scan_bash_command(cmd, self.root, self.root, [])
        self.assertEqual(reasons, [], f"false positive for: {cmd}")

    def test_interpreter_payload_escapes_denied(self):
        self._deny("bash -c 'cat /etc/passwd'")
        self._deny("sh -c 'cat /etc/passwd'")
        self._deny("python3 -c 'print(open(\"/etc/passwd\").read())'")
        self._deny(f"python3 -c 'open(\"{self.outside}/pwned\",\"w\")'")
        self._deny("eval 'cat /etc/passwd'")
        self._deny("env bash -c 'cat /etc/passwd'")
        self._deny("nohup cat /etc/passwd")
        self._deny("xargs cat < /etc/passwd")

    def test_joined_git_flag_escapes_denied(self):
        self._deny(f"git -C{self.outside}/repo log")
        self._deny("git --git-dir=/outside/.git log")
        self._deny("git --work-tree=/outside status")

    def test_quoted_absolute_path_argument_denied(self):
        self._deny('cat "prefix /etc/passwd suffix"')

    def test_benign_interpreter_and_flag_usage_allowed(self):
        self._allow("python3 -c 'print(1+1)'")
        self._allow(f"bash -c 'cd {self.root}/src && pytest -q'")
        self._allow(f"git -C {self.root} log --oneline")
        self._allow(f"python3 {self.root}/src/tool.py --flag")
        self._allow("echo hello && echo world")


class TestReviewFixLifecycle(unittest.TestCase):
    """F3/F5/F6/F8 end-to-end through the real CLI."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="rf-", dir=str(FIXTURES))
        os.environ["AUDIT_COUNCIL_CACHE_HOME"] = os.path.join(
            self.base, "cache")
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

    def _init(self):
        proc = self._cli("init-run", "--repo", self.repo,
                         "--brief", self.brief)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return [l.strip() for l in proc.stdout.decode().splitlines()
                if "audit-output/audit-council/" in l][0]

    def _freeze(self, run_dir):
        st = state_store.load_state(run_dir)
        c = contract()
        binding = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))
        c["target_repository"] = {
            "root": self.repo, "head_sha": binding["head_sha"],
            "fingerprint_sha256": st["repo_fingerprint_sha256"],
            "branch": "main", "dirty": False,
        }
        proc = self._cli("freeze-contract", "--run", run_dir,
                         "--artifact", "-", "--stdin",
                         stdin=json.dumps(c).encode())
        assert proc.returncode == 0, proc.stdout + proc.stderr

    def test_f3_resume_check_accepts_recorded_skips(self):
        run_dir = self._init()
        self._freeze(run_dir)
        st = state_store.load_state(run_dir)
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        proc = self._cli("advance", "--run", run_dir, "--to",
                         "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                         "10-opus-independent.json", "--stdin",
                         stdin=json.dumps(ia).encode())
        assert proc.returncode == 0, proc.stdout + proc.stderr
        proc = self._cli("advance", "--run", run_dir, "--to",
                         "LEDGER_COMPLETE", "--artifact",
                         "40-disagreement-ledger.json", "--stdin",
                         "--skip", "CODEX_INDEPENDENT_COMPLETE=quota (t)",
                         "--skip", "NORMALIZED=none (t)",
                         "--skip", "OPUS_CROSS_EXAM_COMPLETE=deferred (t)",
                         "--skip", "CODEX_CROSS_EXAM_COMPLETE=quota (t)",
                         stdin=json.dumps({"clusters": []}).encode())
        assert proc.returncode == 0, proc.stdout + proc.stderr
        proc = self._cli("resume-check", "--run", run_dir)
        self.assertEqual(proc.returncode, 0,
                         f"F3 regression: {proc.stdout + proc.stderr}")
        doc = json.loads(proc.stdout.decode())
        self.assertEqual(doc["problems"], [])

    def test_f5_v2_run_rejects_legacy_lines_artifact(self):
        run_dir = self._init()
        self._freeze(run_dir)
        st = state_store.load_state(run_dir)
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        ia["findings"][0]["evidence"][0]["lines"] = "7"  # legacy smuggle
        proc = self._cli("advance", "--run", run_dir, "--to",
                         "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                         "10-opus-independent.json", "--stdin",
                         stdin=json.dumps(ia).encode())
        self.assertNotEqual(proc.returncode, 0,
                            "F5 regression: v2 run accepted legacy lines")

    def test_f5_v1_era_run_still_accepts_legacy_lines_artifact(self):
        run_dir = self._init()
        head = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))["head_sha"]
        # degrade to a v1-era run: drop binding + digest, fix checksums
        os.unlink(os.path.join(run_dir, "01-environment-binding.json"))
        state = state_store.load_state(run_dir)
        state.pop("env_binding_digest", None)
        state_store.save_state(run_dir, state)
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
        st = state_store.load_state(run_dir)
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        ia["findings"][0]["evidence"][0]["lines"] = "7"
        proc = self._cli("advance", "--run", run_dir, "--to",
                         "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                         "10-opus-independent.json", "--stdin",
                         stdin=json.dumps(ia).encode())
        self.assertEqual(proc.returncode, 0,
                         f"F5 over-fix: v1-era run rejected: "
                         f"{proc.stdout + proc.stderr}")

    def test_f5_reversed_ranges_rejected_at_gate(self):
        run_dir = self._init()
        self._freeze(run_dir)
        st = state_store.load_state(run_dir)
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        ia["findings"][0]["evidence"][0]["line_ranges"] = [
            {"start": 9, "end": 4}]
        proc = self._cli("advance", "--run", run_dir, "--to",
                         "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                         "10-opus-independent.json", "--stdin",
                         stdin=json.dumps(ia).encode())
        self.assertNotEqual(proc.returncode, 0,
                            "F5 regression: reversed range accepted")
        self.assertIn("reversed", proc.stdout.decode())

    def test_f6_env_gate_fails_closed_on_binding_deletion(self):
        run_dir = self._init()
        os.unlink(os.path.join(run_dir, "01-environment-binding.json"))
        proc = self._cli("verify-env", "--run", run_dir)
        self.assertEqual(proc.returncode, 10,
                         "F6 regression: gate failed open on deletion")
        # and codex start refuses too
        proc = subprocess.run(
            [PYTHON, CODEX_RUNNER, "start", "--run", run_dir,
             "--phase", "independent", "--prompt", "-"],
            input=b"p", capture_output=True, check=False,
            env=dict(os.environ))
        self.assertEqual(proc.returncode, 3)

    def test_f8_resume_check_does_not_phantom_bump_attempts(self):
        run_dir = self._init()
        self._freeze(run_dir)
        st = state_store.load_state(run_dir)
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        proc = self._cli("advance", "--run", run_dir, "--to",
                         "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                         "10-opus-independent.json", "--stdin",
                         stdin=json.dumps(ia).encode())
        assert proc.returncode == 0
        before = state_store.load_state(run_dir)["phase_attempts"].get(
            "OPUS_INDEPENDENT_COMPLETE", 0)
        # stage a valid 20- artifact so the "current phase satisfied" branch
        # fires with the phase pointer still at OPUS_INDEPENDENT_COMPLETE
        codex_doc = dict(ia, model="gpt-5.6-sol")
        with open(os.path.join(run_dir, "20-codex-independent.json"),
                  "w") as fh:
            json.dump(codex_doc, fh)
        self._cli("resume-check", "--run", run_dir)
        after = state_store.load_state(run_dir)["phase_attempts"].get(
            "OPUS_INDEPENDENT_COMPLETE", 0)
        self.assertEqual(before, after,
                         "F8 regression: phantom attempt bump on resume")


class TestF4RepairGovernor(unittest.TestCase):
    def test_repair_refused_when_attempts_exhausted_and_on_complete(self):
        with tempfile.TemporaryDirectory(prefix="f4-", dir=str(FIXTURES)) \
                as base:
            rd = os.path.join(base, "run")
            os.makedirs(os.path.join(rd, "logs", "jobs"))
            state = state_store.new_state(
                "20260904T000000Z-abc123", rd, "0" * 64)
            state["codex"]["jobs"] = [
                {"job_id": f"independent-{i}", "phase": "independent",
                 "status": "QUOTA"} for i in range(3)]  # attempts exhausted
            state_store.atomic_write_json(
                os.path.join(rd, "state.json"), state)
            job = {"job_id": "independent-2", "run_dir": rd,
                   "phase": "independent", "status": "INVALID_OUTPUT",
                   "session_id": "s", "session": "s",
                   "argv": ["codex"], "prompt_path": "/dev/null",
                   "schema_path": "/dev/null", "output_path": "/dev/null",
                   "pid": 1}
            job_path = os.path.join(rd, "logs", "jobs", "independent-2.json")
            state_store.atomic_write_json(job_path, job)
            import argparse
            rc = codex_runner_cmd(["repair", job_path])
            self.assertEqual(rc, 3,
                             "F4 regression: repair bypassed the governor")
            # repair on a COMPLETE job refused outright
            job["status"] = "COMPLETE"
            state_store.atomic_write_json(job_path, job)
            rc = codex_runner_cmd(["repair", job_path])
            self.assertEqual(rc, 3)


def codex_runner_cmd(argv):
    proc = subprocess.run([PYTHON, CODEX_RUNNER, *argv],
                          capture_output=True, check=False)
    return proc.returncode


if __name__ == "__main__":
    unittest.main()


class TestRound2Hardening(unittest.TestCase):
    """R2 re-verification regressions: NEW-1 (relative paths), NEW-2
    (harness operands), NEW-4 (bare $VAR/~), NEW-6 (binding substitution)."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="r2-", dir=str(FIXTURES))
        self.root = path_guard.canonicalize(
            os.path.join(self.base, "root"))
        os.makedirs(os.path.join(self.root, "src", "pkg"))
        self.outside = path_guard.canonicalize(
            os.path.join(self.base, "outside"))
        os.makedirs(self.outside)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def _scan(self, cmd):
        return path_guard.scan_bash_command(cmd, self.root, self.root, [])

    def test_new1_relative_multi_component_paths_allowed(self):
        for cmd in ("cat src/pkg/a.py", "ls src/pkg", "rg pattern src/pkg",
                    "git diff -- src/pkg", "echo a/b/c",
                    "echo https://example.com/x"):
            self.assertEqual(self._scan(cmd), [], cmd)
        # and the quoted-payload denial still holds
        self.assertTrue(self._scan('cat "prefix /etc/passwd suffix"'))

    def test_new2_harness_operands_allowed(self):
        scripts = path_guard._HARNESS_DIRS[0]
        ok, reason = path_guard.check_tool_call(
            "Bash",
            {"command": f"/usr/bin/python3 {scripts}/audit_council.py "
                        f"advance --run {self.root}/audit-output/audit-"
                        f"council/x --to OPUS_INDEPENDENT_COMPLETE "
                        f"--artifact - --stdin"},
            self.root, [])
        self.assertTrue(ok, reason)
        # ...but unrelated outside paths stay denied in the same command
        ok, reason = path_guard.check_tool_call(
            "Read", {"file_path": "/etc/passwd"}, self.root, [])
        self.assertFalse(ok)

    def test_new4_bare_env_var_and_tilde_denied(self):
        with unittest.mock.patch.dict(
                os.environ, {"SECRET": os.path.join(self.outside, "s")}):
            self.assertTrue(self._scan("cat $SECRET"),
                            "bare $VAR outside path must be denied")
        self.assertTrue(self._scan("ls ~"), "bare ~ must be denied")

    def test_new6_substituted_binding_rejected(self):
        # two runs: copy run B's VALID binding over run A's binding → the
        # state-pinned digest must catch the substitution
        run_a = self._make_run("a")
        run_b = self._make_run("b")
        shutil.copy(os.path.join(run_b, "01-environment-binding.json"),
                    os.path.join(run_a, "01-environment-binding.json"))
        proc = subprocess.run(
            [PYTHON, AUDIT_COUNCIL, "verify-env", "--run", run_a],
            capture_output=True, check=False, env=dict(os.environ))
        self.assertEqual(proc.returncode, 10,
                         "NEW-6 regression: substituted binding accepted")
        self.assertIn("BINDING_DIGEST_MISMATCH", proc.stdout.decode())

    def _make_run(self, label):
        repo = os.path.join(self.base, label)
        os.makedirs(repo)
        git(repo, "init", "-q", "-b", "main")
        git(repo, "config", "user.email", "t@e.com")
        git(repo, "config", "user.name", "t")
        with open(os.path.join(repo, "a.py"), "w") as fh:
            fh.write("1\n")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "c")
        brief = os.path.join(self.base, f"{label}.md")
        with open(brief, "w") as fh:
            fh.write("# b\n")
        proc = subprocess.run(
            [PYTHON, AUDIT_COUNCIL, "init-run", "--repo", repo,
             "--brief", brief], capture_output=True, check=False,
            env=dict(os.environ))
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return [l.strip() for l in proc.stdout.decode().splitlines()
                if "audit-output/audit-council/" in l][0]
