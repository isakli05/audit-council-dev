#!/usr/bin/env python3
"""Scenarios C, X, Y (+ interruption): CLI lifecycle, resume-check, checksum
tampering, and run-dir collision handling."""
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


def cli(*args: str, stdin: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([PYTHON, AUDIT_COUNCIL, *args],
                          input=stdin, capture_output=True, check=False)


def init_run(repo: str, tmp: str) -> str:
    brief = os.path.join(tmp, "brief.md")
    with open(brief, "w") as fh:
        fh.write("# brief\nAudit everything.\n")
    proc = cli("init-run", "--repo", repo, "--brief", brief)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout.decode()
    pat = re.compile(
        r"^\S*audit-output/audit-council/"
        r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}\s*$")
    for line in out.splitlines():
        if pat.match(line):
            return line.strip()
    raise AssertionError(f"no run dir in stdout: {out!r}")


def resume_check(run_dir: str) -> tuple[int, dict]:
    proc = cli("resume-check", "--run", run_dir)
    return proc.returncode, json.loads(proc.stdout)


class TestResumeLifecycle(unittest.TestCase):
    """Scenario C: end-to-end lifecycle up to OPUS_INDEPENDENT_COMPLETE."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(self._tmp.name)
        self.run_dir = init_run(self.repo, self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _run_fingerprint(self):
        return json.load(open(os.path.join(
            self.run_dir, "state.json")))["repo_fingerprint_sha256"]

    def _freeze_contract_stdin(self):
        head = git(self.repo, "rev-parse", "HEAD").strip()
        doc = contract()
        doc["target_repository"] = {
            "root": self.repo, "head_sha": head, "branch": "main",
            "fingerprint_sha256": self._run_fingerprint(), "dirty": False,
        }
        proc = cli("freeze-contract", "--run", self.run_dir,
                   "--contract", "-", "--stdin",
                   stdin=json.dumps(doc).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return json.loads(proc.stdout)

    def _advance_opus_stdin(self):
        doc = independent_audit()
        doc["repository_fingerprint_sha256"] = self._run_fingerprint()
        proc = cli("advance", "--run", self.run_dir,
                   "--to", "OPUS_INDEPENDENT_COMPLETE",
                   "--artifact", "-", "--stdin",
                   stdin=json.dumps(doc).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return json.loads(proc.stdout)

    def test_full_lifecycle_and_resume_point(self):
        frozen = self._freeze_contract_stdin()
        self.assertTrue(frozen["ok"])
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["phase"], "CONTRACT_FROZEN")
        self.assertIn("PREFLIGHT_COMPLETE", state["timestamps"])
        self.assertIn("CONTRACT_FROZEN", state["timestamps"])

        advanced = self._advance_opus_stdin()
        self.assertTrue(advanced["ok"])
        self.assertEqual(advanced["phase"], "OPUS_INDEPENDENT_COMPLETE")

        # staged stdin artifact landed at its canonical name + checksummed
        art = os.path.join(self.run_dir, "10-opus-independent.json")
        self.assertTrue(os.path.isfile(art))
        with open(os.path.join(self.run_dir, "checksums.sha256")) as fh:
            self.assertIn("10-opus-independent.json", fh.read())

        code, doc = resume_check(self.run_dir)
        self.assertEqual(code, 0, doc)
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["problems"], [])
        # next unit of work after the Opus independent stage
        self.assertIn(doc["earliest_incomplete_phase"],
                      ("OPUS_INDEPENDENT_COMPLETE",
                       "CODEX_INDEPENDENT_COMPLETE"))
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["phase"], "OPUS_INDEPENDENT_COMPLETE")
        self.assertEqual(state["completeness_state"], "RUNNING")
        # state intact: the recorded phases are still timestamped
        self.assertIn("CONTRACT_FROZEN", state["timestamps"])
        self.assertIn("OPUS_INDEPENDENT_COMPLETE", state["timestamps"])

    def test_interrupt_simulation_resume_ok(self):
        """Interruption mid-run = state left at an intermediate phase;
        resume-check must still succeed and point at the resume point."""
        self._freeze_contract_stdin()
        # "crash" here: nothing further happens.
        code, doc = resume_check(self.run_dir)
        self.assertEqual(code, 0, doc)
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["problems"], [])
        self.assertIn(doc["earliest_incomplete_phase"],
                      ("CONTRACT_FROZEN", "OPUS_INDEPENDENT_COMPLETE"))
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["phase"], "CONTRACT_FROZEN")

        # resuming works: the next advance succeeds from the mid-state
        advanced = self._advance_opus_stdin()
        self.assertTrue(advanced["ok"])

    def test_resume_check_right_after_init(self):
        code, doc = resume_check(self.run_dir)
        self.assertEqual(code, 0, doc)
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["earliest_incomplete_phase"], "CREATED")

    def test_advance_rejects_backward_transition(self):
        """Completed phases are immutable: re-advancing an already satisfied
        phase must fail without rewriting artifacts."""
        self._freeze_contract_stdin()
        self._advance_opus_stdin()
        art_before = open(os.path.join(
            self.run_dir, "10-opus-independent.json"), "rb").read()
        proc = cli("advance", "--run", self.run_dir,
                   "--to", "CONTRACT_FROZEN",
                   "--artifact", os.path.join(
                       self.run_dir, "02-audit-contract.json"))
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(json.loads(proc.stdout)["ok"])
        self.assertEqual(
            open(os.path.join(self.run_dir, "10-opus-independent.json"),
                 "rb").read(), art_before)
        state = json.load(open(os.path.join(self.run_dir, "state.json")))
        self.assertEqual(state["phase"], "OPUS_INDEPENDENT_COMPLETE")


class TestTamperDetected(unittest.TestCase):
    """Scenario X: byte-tampering an artifact after its checksum was
    recorded must fail resume-check with exit 8."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(self._tmp.name)
        self.run_dir = init_run(self.repo, self._tmp.name)
        doc = contract()
        binding = json.load(open(os.path.join(
            self.run_dir, "01-environment-binding.json")))
        doc["target_repository"]["root"] = binding["repo_root_realpath"]
        doc["target_repository"]["head_sha"] = binding["head_sha"]
        doc["target_repository"]["fingerprint_sha256"] = \
            json.load(open(os.path.join(
                self.run_dir, "state.json")))["repo_fingerprint_sha256"]
        proc = cli("freeze-contract", "--run", self.run_dir,
                   "--contract", "-", "--stdin",
                   stdin=json.dumps(doc).encode())
        assert proc.returncode == 0, proc.stdout + proc.stderr

    def tearDown(self):
        self._tmp.cleanup()

    def test_tampered_artifact_exit_8(self):
        code, _ = resume_check(self.run_dir)
        self.assertEqual(code, 0)
        target = os.path.join(self.run_dir, "02-audit-contract.json")
        with open(target, "rb") as fh:
            data = fh.read()
        # flip the final byte (single-byte tamper after checksum recorded)
        self.assertGreater(len(data), 0)
        tampered = data[:-1] + (b" " if data[-1:] != b" " else b"~")
        with open(target, "wb") as fh:
            fh.write(tampered)
        proc = cli("resume-check", "--run", self.run_dir)
        self.assertEqual(proc.returncode, 8, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout)
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["stage"], "checksums")
        mism = doc["mismatches"]
        self.assertTrue(any(m["file"] == "02-audit-contract.json"
                            and m["error"] == "checksum mismatch"
                            for m in mism), mism)
        # the tampered bytes are still on disk (nothing reset/deleted)
        with open(target, "rb") as fh:
            self.assertEqual(fh.read(), tampered)


class TestRunIdCollision(unittest.TestCase):
    """Scenario Y: run-dir collisions regenerate the suffix and never
    overwrite an existing run dir."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(self._tmp.name)
        self.brief = os.path.join(self._tmp.name, "brief.md")
        with open(self.brief, "w") as fh:
            fh.write("# brief\n")

    def tearDown(self):
        self._tmp.cleanup()

    def test_new_run_id_regenerates_suffix_on_collision(self):
        import time as _time
        real_token = state_store.secrets.token_hex
        calls = {"n": 0}

        def fake_token_hex(n=3):
            calls["n"] += 1
            return "aaaaaa" if calls["n"] == 1 else real_token(n)

        state_store.secrets.token_hex = fake_token_hex
        try:
            stamp = _time.strftime("%Y%m%dT%H%M%SZ", _time.gmtime())
            colliding = f"{stamp}-aaaaaa"
            rid = state_store.new_run_id({colliding})
        finally:
            state_store.secrets.token_hex = real_token
        self.assertNotEqual(rid, colliding)
        self.assertRegex(rid, r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}$")
        self.assertGreaterEqual(calls["n"], 2)  # retry happened

    def test_init_run_never_overwrites_colliding_dir(self):
        import audit_council
        import contextlib
        import io
        parent = state_store.runs_root(self.repo)
        os.makedirs(parent, exist_ok=True)
        colliding = "20260903T170000Z-dead00"
        existing_dir = os.path.join(parent, colliding)
        os.makedirs(existing_dir)
        sentinel = os.path.join(existing_dir, "sentinel.txt")
        with open(sentinel, "w") as fh:
            fh.write("do not clobber\n")

        real = state_store.new_run_id
        state_store.new_run_id = lambda existing=None, **kw: colliding
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rc = audit_council.main(
                    ["init-run", "--repo", self.repo, "--brief", self.brief])
        finally:
            state_store.new_run_id = real
        self.assertEqual(rc, 1)  # refused
        self.assertIn("do not clobber", open(sentinel).read())
        self.assertEqual(os.listdir(existing_dir), ["sentinel.txt"])

    def test_init_run_retries_to_fresh_dir_when_generator_respects_existing(self):
        import audit_council
        import contextlib
        import io
        parent = state_store.runs_root(self.repo)
        os.makedirs(parent, exist_ok=True)
        colliding = "20260903T170000Z-beef00"
        os.makedirs(os.path.join(parent, colliding))
        with open(os.path.join(parent, colliding, "keep.txt"), "w") as fh:
            fh.write("keep\n")

        real = state_store.new_run_id
        state_store.new_run_id = real  # honors `existing` (listdir-based)
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            rc = audit_council.main(
                ["init-run", "--repo", self.repo, "--brief", self.brief])
        self.assertTrue(captured.getvalue().strip(), "run dir not printed")
        self.assertEqual(rc, 0)
        dirs = os.listdir(parent)
        self.assertEqual(dirs.count(colliding), 1)
        new_dirs = [d for d in dirs if d != colliding]
        self.assertEqual(len(new_dirs), 1)
        self.assertRegex(new_dirs[0], r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}$")
        # colliding dir untouched
        self.assertEqual(os.listdir(os.path.join(parent, colliding)),
                         ["keep.txt"])

    def test_two_init_runs_create_distinct_dirs(self):
        d1 = init_run(self.repo, self._tmp.name)
        d2 = init_run(self.repo, self._tmp.name)
        self.assertNotEqual(d1, d2)
        self.assertTrue(os.path.isdir(d1) and os.path.isdir(d2))


if __name__ == "__main__":
    unittest.main()
