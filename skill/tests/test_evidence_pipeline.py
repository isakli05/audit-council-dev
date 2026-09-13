#!/usr/bin/env python3
"""F-A-12 / AUCDEV-017 — production EvidenceStore wiring proofs.

These are PRODUCTION-PATH tests, not standalone library tests: staged
evidence records are produced by the real `prepare` CLI, first-pass
manifests by the real `advance` checkpoint, stage-launch consumption by the
real `codex_runner start` (fake codex fixture), and every serve goes
through the production serve path (visibility + freshness law + access
log). Deterministic; zero model calls.
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
HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
SCRIPTS = SKILL_DIR / "scripts"
FIXTURES = HERE / "fixtures"
AUDIT_COUNCIL = str(SCRIPTS / "audit_council.py")
RUNNER = str(SCRIPTS / "codex_runner.py")
FAKE_CODEX = str(FIXTURES / "fake_codex.py")

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(HERE))

from test_schema_validation import contract, independent_audit  # noqa: E402

import evidence_store  # noqa: E402
import state_store  # noqa: E402


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def _read_jsonl(path):
    entries = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def _read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


FP_A = "a" * 64
FP_B = "b" * 64
BINDING_A = "c" * 64
BINDING_B = "d" * 64


def synthetic_bound_run(tmp, *, phase="CODEX_INDEPENDENT_COMPLETE",
                        fingerprint=FP_A, binding=BINDING_A):
    """Minimal run dir with the identity fields the production wiring
    reads (state.json + 01-environment-binding.json)."""
    run_dir = os.path.join(tmp, "run")
    os.makedirs(run_dir)
    with open(os.path.join(run_dir, "state.json"), "w") as fh:
        json.dump({"phase": phase, "repo_fingerprint_sha256": fingerprint,
                   "run_id": "20260913T000000Z-aa0001"}, fh)
    with open(os.path.join(run_dir, "01-environment-binding.json"), "w") as fh:
        json.dump({"binding_digest": binding}, fh)
    return run_dir


# ---------------------------------------------------------------------------
# production serve-path law (synthetic bound runs, real helpers)
# ---------------------------------------------------------------------------
class TestServeRunEvidenceLaw(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="evpipe-serve-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _put_stage_input(self, run_dir, manifest=None):
        store = evidence_store.open_run_store(run_dir)
        record = evidence_store.stage_input_record(
            "independent", manifest or {"phase": "independent"},
            fingerprint=FP_A, binding_digest=BINDING_A,
            tool={"name": "codex_runner.stage-input", "version": "2.0"},
            produced_at="2026-09-13T00:00:00Z")
        return store, store.put(record)

    def test_barrier_identity_owned_by_state_machine(self):
        for phase, expected in (
                ("CREATED", False), ("CONTRACT_FROZEN", False),
                ("OPUS_INDEPENDENT_COMPLETE", False),
                ("CODEX_INDEPENDENT_COMPLETE", True),
                ("NORMALIZED", True), ("COMPLETE", True)):
            with open(os.path.join(self.tmp, "state.json"), "w") as fh:
                json.dump({"phase": phase,
                           "repo_fingerprint_sha256": FP_A}, fh)
            self.assertEqual(evidence_store.run_barrier_state(self.tmp),
                             expected, phase)
        # unreadable state fails CLOSED
        os.remove(os.path.join(self.tmp, "state.json"))
        self.assertFalse(evidence_store.run_barrier_state(self.tmp))

    def test_valid_cacheable_record_served_with_access_log(self):
        run_dir = synthetic_bound_run(self.tmp)
        store, evidence_id = self._put_stage_input(run_dir)
        ref = evidence_store.serve_run_evidence(store, run_dir, evidence_id,
                                                "HARNESS")
        self.assertIsNotNone(ref)
        self.assertEqual(ref["evidence_id"], evidence_id)
        log = store.access_log()
        self.assertEqual(log[-1]["served"], True)
        self.assertEqual(log[-1]["consumer"], "HARNESS")

    def test_changed_fingerprint_denies_reuse(self):
        run_dir = synthetic_bound_run(self.tmp)
        store, evidence_id = self._put_stage_input(run_dir)
        with open(os.path.join(run_dir, "state.json"), "w") as fh:
            json.dump({"phase": "CODEX_INDEPENDENT_COMPLETE",
                       "repo_fingerprint_sha256": FP_B}, fh)
        store2 = evidence_store.open_run_store(run_dir)
        self.assertIsNone(evidence_store.serve_run_evidence(
            store2, run_dir, evidence_id, "HARNESS"))
        self.assertEqual(store2.access_log()[-1]["reason"],
                         "stale_not_reusable")

    def test_changed_binding_denies_reuse(self):
        run_dir = synthetic_bound_run(self.tmp)
        store, evidence_id = self._put_stage_input(run_dir)
        with open(os.path.join(run_dir, "01-environment-binding.json"),
                  "w") as fh:
            json.dump({"binding_digest": BINDING_B}, fh)
        store2 = evidence_store.open_run_store(run_dir)
        self.assertIsNone(evidence_store.serve_run_evidence(
            store2, run_dir, evidence_id, "HARNESS"))
        self.assertEqual(store2.access_log()[-1]["reason"],
                         "stale_not_reusable")

    def test_unprovable_identity_denies_all_cacheable_reuse(self):
        run_dir = synthetic_bound_run(self.tmp)
        store, evidence_id = self._put_stage_input(run_dir)
        os.remove(os.path.join(run_dir, "01-environment-binding.json"))
        store2 = evidence_store.open_run_store(run_dir)
        self.assertIsNone(evidence_store.serve_run_evidence(
            store2, run_dir, evidence_id, "HARNESS"))

    def test_private_record_barriers_pre_and_serves_post(self):
        run_dir = synthetic_bound_run(self.tmp,
                                      phase="OPUS_INDEPENDENT_COMPLETE")
        store = evidence_store.open_run_store(run_dir)
        evidence_id = store.put(evidence_store.first_pass_manifest_record(
            "10-opus-independent.json", "OPUS", fingerprint=FP_A,
            binding_digest=BINDING_A,
            tool={"name": "audit_council.run", "version": "2.0"},
            sha256=FP_A, size=17, produced_at="2026-09-13T00:00:00Z"))
        # pre-barrier: CODEX denied (the cache cannot bypass the barrier),
        # OPUS (producer family) served
        self.assertIsNone(evidence_store.serve_run_evidence(
            store, run_dir, evidence_id, "CODEX"))
        self.assertEqual(store.access_log()[-1]["reason"], "barrier_closed")
        ref = evidence_store.serve_run_evidence(store, run_dir, evidence_id,
                                                "OPUS")
        self.assertIsNotNone(ref)
        # post-barrier: CODEX served
        with open(os.path.join(run_dir, "state.json"), "w") as fh:
            json.dump({"phase": "CODEX_INDEPENDENT_COMPLETE",
                       "repo_fingerprint_sha256": FP_A}, fh)
        store2 = evidence_store.open_run_store(run_dir)
        served = evidence_store.serve_run_evidence(store2, run_dir,
                                                   evidence_id, "CODEX",
                                                   include_content=True)
        self.assertIsNotNone(served)
        self.assertEqual(served["result"],
                         {"path": "10-opus-independent.json",
                          "sha256": FP_A, "bytes": 17})

    def test_fresh_required_never_served_through_production_path(self):
        run_dir = synthetic_bound_run(self.tmp)
        store = evidence_store.open_run_store(run_dir)
        evidence_id = store.put(evidence_store.staged_evidence_record(
            {"path": "docs/notes.md", "sha256": FP_A, "bytes": 3},
            fingerprint=FP_A, binding_digest=BINDING_A,
            tool={"name": "audit_council.run", "version": "2.0"},
            produced_at="2026-09-13T00:00:00Z"))
        for consumer in ("OPUS", "CODEX", "HARNESS"):
            self.assertIsNone(evidence_store.serve_run_evidence(
                store, run_dir, evidence_id, consumer))
        reasons = {e.get("reason") for e in store.access_log()}
        self.assertEqual(reasons, {"fresh_required"})

    def test_repeated_put_of_same_content_deduplicates(self):
        run_dir = synthetic_bound_run(self.tmp)
        store = evidence_store.open_run_store(run_dir)
        first = store.put(evidence_store.stage_input_record(
            "independent", {"phase": "independent"}, fingerprint=FP_A,
            binding_digest=BINDING_A,
            tool={"name": "codex_runner.stage-input", "version": "2.0"},
            produced_at="2026-09-13T00:00:00Z"))
        # same content, different production stamp, SAME store → one record
        again = store.put(evidence_store.stage_input_record(
            "independent", {"phase": "independent"}, fingerprint=FP_A,
            binding_digest=BINDING_A,
            tool={"name": "codex_runner.stage-input", "version": "2.0"},
            produced_at="2026-09-13T09:00:00Z"))
        self.assertEqual(first, again)
        # and a store REOPENED from the index deduplicates too
        reopened = evidence_store.open_run_store(run_dir)
        third = reopened.put(evidence_store.stage_input_record(
            "independent", {"phase": "independent"}, fingerprint=FP_A,
            binding_digest=BINDING_A,
            tool={"name": "codex_runner.stage-input", "version": "2.0"},
            produced_at="2026-09-13T12:00:00Z"))
        self.assertEqual(first, third)
        self.assertEqual(len(_read_jsonl(os.path.join(
            run_dir, "evidence", "index.jsonl"))), 1)


# ---------------------------------------------------------------------------
# real prepare / advance flow (production producers)
# ---------------------------------------------------------------------------
class TestRealPrepareAdvance(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="evpipe-e2e-", dir=str(FIXTURES))
        os.environ["AUDIT_COUNCIL_CACHE_HOME"] = os.path.join(
            self.base, "cache")
        os.environ["AUDIT_COUNCIL_ENV_ROOT"] = os.path.join(
            self.base, "envroot")
        self.src = os.path.join(self.base, "src")
        os.makedirs(os.path.join(self.src, "docs"))
        git(self.src, "init", "-q", "-b", "main")
        git(self.src, "config", "user.email", "t@e.com")
        git(self.src, "config", "user.name", "t")
        with open(os.path.join(self.src, "docs", "notes.md"), "w") as fh:
            fh.write("release notes\n")
        with open(os.path.join(self.src, "a.py"), "w") as fh:
            fh.write("VALUE = 1\n")
        git(self.src, "add", "-A")
        git(self.src, "commit", "-q", "-m", "A")
        self.head = git(self.src, "rev-parse", "HEAD").strip()
        self.brief = os.path.join(self.base, "brief.md")
        with open(self.brief, "w") as fh:
            fh.write("# brief\nAudit A.\n")
        self.base_env = dict(os.environ)

    def tearDown(self):
        for var in ("AUDIT_COUNCIL_CACHE_HOME", "AUDIT_COUNCIL_ENV_ROOT"):
            os.environ.pop(var, None)
        if os.path.isdir(self.src):
            subprocess.run(["git", "-C", self.src, "worktree", "prune"],
                           capture_output=True, check=False)
        shutil.rmtree(self.base, ignore_errors=True)

    def ac(self, *args, stdin=None):
        return subprocess.run([PYTHON, AUDIT_COUNCIL, *args], input=stdin,
                              capture_output=True, check=False,
                              env=dict(self.base_env))

    def prepared_run(self):
        proc = self.ac("prepare", "--repo", self.src, "--brief", self.brief,
                       "--mode", "HISTORICAL", "--ref", self.head,
                       "--evidence-allow", "docs/notes.md")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return json.loads(proc.stdout.decode())["run"]

    def freeze_and_advance_opus(self, run_dir):
        st = state_store.load_state(run_dir)
        c = contract()
        binding = _read_json(os.path.join(run_dir,
                                          "01-environment-binding.json"))
        env_record = _read_json(os.path.join(run_dir,
                                             "environment-record.json"))
        c["target_repository"] = {
            "root": env_record.get("worktree_root", self.src),
            "head_sha": binding["head_sha"],
            "fingerprint_sha256": st["repo_fingerprint_sha256"],
            "branch": "HEAD", "dirty": False,
        }
        self.ac("freeze-contract", "--run", run_dir, "--artifact", "-",
                "--stdin", stdin=json.dumps(c).encode())
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        proc = self.ac("advance", "--run", run_dir, "--to",
                       "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                       "10-opus-independent.json", "--stdin",
                       stdin=json.dumps(ia).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return json.loads(proc.stdout.decode())

    def test_prepare_records_staged_evidence_provenance(self):
        run_dir = self.prepared_run()
        index = _read_jsonl(os.path.join(run_dir, "evidence",
                                         "index.jsonl"))
        self.assertEqual(len(index), 1)
        rec = index[0]
        st = state_store.load_state(run_dir)
        binding = _read_json(os.path.join(run_dir,
                                          "01-environment-binding.json"))
        self.assertEqual(rec["kind"], "FILE_EXCERPT")
        self.assertEqual(rec["producer"], "HARNESS")
        self.assertEqual(rec["visibility"], "SHARED_MECHANICAL")
        self.assertEqual(rec["freshness_policy"]["class"], "FRESH_REQUIRED")
        self.assertEqual(rec["command_or_query"],
                         "staged-evidence:docs/notes.md")
        self.assertEqual(rec["repository_fingerprint_sha256"],
                         st["repo_fingerprint_sha256"])
        self.assertEqual(rec["environment_binding_digest"],
                         binding["binding_digest"])
        # payload is the identity manifest, never the file content
        obj = _read_json(os.path.join(run_dir, rec["result_location"]))
        self.assertEqual(sorted(obj), ["bytes", "path", "sha256"])
        self.assertNotIn("release notes", json.dumps(obj))

    def test_advance_records_first_pass_manifest_with_privacy(self):
        run_dir = self.prepared_run()
        out = self.freeze_and_advance_opus(run_dir)
        self.assertEqual(out.get("evidence_store"), "recorded")
        store = evidence_store.open_run_store(run_dir)
        ids = store.find_records(producer="OPUS")
        self.assertEqual(len(ids), 1)
        record = store.get(ids[0], "OPUS", include_content=True)
        self.assertEqual(record["visibility"], "AUDITOR_PRIVATE")
        self.assertEqual(record["freshness_policy"]["class"], "CACHEABLE")
        artifact = os.path.join(run_dir, "10-opus-independent.json")
        with open(artifact, "rb") as fh:
            digest = state_store.sha256_bytes(fh.read())
        self.assertEqual(record["result"]["sha256"], digest)
        # pre-barrier: CODEX consumer denied through the production path
        self.assertIsNone(evidence_store.serve_run_evidence(
            store, run_dir, ids[0], "CODEX"))

    def test_advance_post_barrier_serves_peer_manifest(self):
        run_dir = self.prepared_run()
        self.freeze_and_advance_opus(run_dir)
        st = state_store.load_state(run_dir)
        codex_audit = independent_audit(
            model="gpt-5.6-sol",
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        proc = self.ac("advance", "--run", run_dir, "--to",
                       "CODEX_INDEPENDENT_COMPLETE", "--artifact",
                       "20-codex-independent.json", "--stdin",
                       stdin=json.dumps(codex_audit).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        store = evidence_store.open_run_store(run_dir)
        opus_ids = store.find_records(producer="OPUS")
        served = evidence_store.serve_run_evidence(store, run_dir,
                                                   opus_ids[0], "CODEX")
        self.assertIsNotNone(served)  # post-barrier: identity ref served

    def test_unbound_run_advances_with_honest_note(self):
        # v1-era fixture run (no binding file, non-hex fingerprint): the
        # wiring records absence instead of touching any store
        tmp = tempfile.mkdtemp(prefix="evpipe-unbound-", dir=str(FIXTURES))
        try:
            run_dir = os.path.join(tmp, "audit-output", "audit-council",
                                   "20260913T000000Z-bb0002")
            os.makedirs(os.path.join(run_dir, "prompts"))
            os.makedirs(os.path.join(run_dir, "logs"))
            with open(os.path.join(run_dir, "state.json"), "w") as fh:
                json.dump({"schema_version": 1,
                           "run_id": "20260913T000000Z-bb0002",
                           "phase": "CONTRACT_FROZEN",
                           "completeness_state": "RUNNING",
                           "created_at": "2026-09-13T00:00:00Z",
                           "timestamps": {},
                           "repo_fingerprint_sha256": "deadbeef",
                           "codex": {"session_id": None, "jobs": [],
                                     "stage_counts": {}},
                           "phase_attempts": {}, "failure_reason": None},
                          fh)
            doc = independent_audit(repository_fingerprint_sha256="deadbeef")
            proc = self.ac("advance", "--run", run_dir, "--to",
                           "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                           "10-opus-independent.json", "--stdin",
                           stdin=json.dumps(doc).encode())
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual(json.loads(proc.stdout.decode()).get(
                "evidence_store"), "unbound_run_no_record")
            self.assertFalse(os.path.exists(os.path.join(run_dir,
                                                         "evidence")))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# real stage launch (fake codex) — consumer + reuse-when-valid
# ---------------------------------------------------------------------------
class TestRealStageLaunch(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="evpipe-launch-", dir=str(FIXTURES))
        os.environ["AUDIT_COUNCIL_CACHE_HOME"] = os.path.join(
            self.base, "cache")
        os.environ["AUDIT_COUNCIL_ENV_ROOT"] = os.path.join(
            self.base, "envroot")
        self.src = os.path.join(self.base, "src")
        os.makedirs(os.path.join(self.src, "docs"))
        git(self.src, "init", "-q", "-b", "main")
        git(self.src, "config", "user.email", "t@e.com")
        git(self.src, "config", "user.name", "t")
        with open(os.path.join(self.src, "a.py"), "w") as fh:
            fh.write("VALUE = 1\n")
        git(self.src, "add", "-A")
        git(self.src, "commit", "-q", "-m", "A")
        self.head = git(self.src, "rev-parse", "HEAD").strip()
        self.brief = os.path.join(self.base, "brief.md")
        with open(self.brief, "w") as fh:
            fh.write("# brief\nAudit A.\n")
        self.env = dict(os.environ)
        self.env["FAKE_CODEX_MODE"] = "ok"
        self.env["CODEX_RUNNER_POLL_INTERVAL"] = "0.02"
        self.env["AC_SANDBOX_DNS_PROBE_HOST"] = "localhost"

    def tearDown(self):
        for var in ("AUDIT_COUNCIL_CACHE_HOME", "AUDIT_COUNCIL_ENV_ROOT"):
            os.environ.pop(var, None)
        if os.path.isdir(self.src):
            subprocess.run(["git", "-C", self.src, "worktree", "prune"],
                           capture_output=True, check=False)
        shutil.rmtree(self.base, ignore_errors=True)

    def ac(self, *args, stdin=None):
        return subprocess.run([PYTHON, AUDIT_COUNCIL, *args], input=stdin,
                              capture_output=True, check=False,
                              env=dict(self.env))

    def prepared_run_at_opus_complete(self):
        proc = self.ac("prepare", "--repo", self.src, "--brief", self.brief,
                       "--mode", "RELEASE", "--ref", self.head)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        run_dir = json.loads(proc.stdout.decode())["run"]
        st = state_store.load_state(run_dir)
        binding = _read_json(os.path.join(run_dir,
                                          "01-environment-binding.json"))
        env_record = _read_json(os.path.join(run_dir,
                                             "environment-record.json"))
        c = contract()
        c["target_repository"] = {
            "root": env_record.get("worktree_root", self.src),
            "head_sha": binding["head_sha"],
            "fingerprint_sha256": st["repo_fingerprint_sha256"],
            "branch": "HEAD", "dirty": False,
        }
        self.ac("freeze-contract", "--run", run_dir, "--artifact", "-",
                "--stdin", stdin=json.dumps(c).encode())
        ia = independent_audit(
            repository_fingerprint_sha256=st["repo_fingerprint_sha256"])
        proc = self.ac("advance", "--run", run_dir, "--to",
                       "OPUS_INDEPENDENT_COMPLETE", "--artifact",
                       "10-opus-independent.json", "--stdin",
                       stdin=json.dumps(ia).encode())
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        # the orchestrator renders the stage prompt into the run prompts
        # dir before launch (the runner's expected input location)
        prompt_dir = os.path.join(run_dir, "prompts")
        os.makedirs(prompt_dir, exist_ok=True)
        with open(os.path.join(prompt_dir, "codex-independent.md"),
                  "w") as fh:
            fh.write("Independent audit prompt. Do the audit.\n")
        return run_dir

    def start(self, run_dir):
        with open(os.path.join(run_dir, "fake-codex-control"), "w") as fh:
            fh.write("MODE=ok\n")
        return subprocess.run(
            [PYTHON, RUNNER, "start", "--run", run_dir,
             "--phase", "independent", "--codex-bin", FAKE_CODEX],
            capture_output=True, text=True, env=dict(self.env),
            timeout=90)

    def test_launch_denies_peer_manifest_and_records_stage_input(self):
        run_dir = self.prepared_run_at_opus_complete()
        proc = self.start(run_dir)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        job_path = proc.stdout.strip()
        with open(job_path) as fh:
            job = json.load(fh)
        note = job.get("evidence") or {}
        self.assertEqual(note.get("status"), "ok")
        self.assertEqual(note.get("peer_firstpass_store_access"),
                         "denied_pre_barrier")
        stage_input = note.get("stage_input_evidence") or {}
        self.assertFalse(stage_input.get("reused"))
        # the store: peer denial logged for consumer CODEX; record present
        store = evidence_store.open_run_store(run_dir)
        denial = [e for e in store.access_log()
                  if e.get("consumer") == "CODEX" and not e.get("served")]
        self.assertTrue(denial)
        self.assertEqual(denial[-1]["reason"], "barrier_closed")
        self.assertTrue(store.find_records(
            command_or_query="stage-input:independent"))
        # reap the fake process
        subprocess.run([PYTHON, RUNNER, "wait", job_path, "--timeout", "10"],
                       capture_output=True, text=True, env=dict(self.env),
                       timeout=30)

    def test_retry_with_identical_inputs_reuses_valid_manifest(self):
        run_dir = self.prepared_run_at_opus_complete()
        proc = self.start(run_dir)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        first_job = proc.stdout.strip()
        subprocess.run([PYTHON, RUNNER, "wait", first_job, "--timeout",
                        "10"], capture_output=True, text=True,
                       env=dict(self.env), timeout=30)
        proc = self.start(run_dir)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with open(proc.stdout.strip()) as fh:
            note = json.load(fh).get("evidence") or {}
        stage_input = note.get("stage_input_evidence") or {}
        self.assertTrue(stage_input.get("reused"))
        self.assertEqual(stage_input.get("evidence_id"),
                         self.first_stage_input_id(run_dir))
        subprocess.run([PYTHON, RUNNER, "wait", proc.stdout.strip(),
                        "--timeout", "10"], capture_output=True,
                       text=True, env=dict(self.env), timeout=30)

    def test_changed_prompt_is_not_reused(self):
        run_dir = self.prepared_run_at_opus_complete()
        proc = self.start(run_dir)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        first_job = proc.stdout.strip()
        subprocess.run([PYTHON, RUNNER, "wait", first_job, "--timeout",
                        "10"], capture_output=True, text=True,
                       env=dict(self.env), timeout=30)
        old_id = self.first_stage_input_id(run_dir)
        with open(os.path.join(run_dir, "prompts", "codex-independent.md"),
                  "a") as fh:
            fh.write("changed prompt bytes\n")
        proc = self.start(run_dir)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with open(proc.stdout.strip()) as fh:
            note = json.load(fh).get("evidence") or {}
        stage_input = note.get("stage_input_evidence") or {}
        self.assertFalse(stage_input.get("reused"))
        self.assertNotEqual(stage_input.get("evidence_id"), old_id)
        subprocess.run([PYTHON, RUNNER, "wait", proc.stdout.strip(),
                        "--timeout", "10"], capture_output=True,
                       text=True, env=dict(self.env), timeout=30)

    @staticmethod
    def first_stage_input_id(run_dir):
        store = evidence_store.open_run_store(run_dir)
        ids = store.find_records(command_or_query="stage-input:independent")
        assert ids
        return ids[0]


# ---------------------------------------------------------------------------
# report provenance + public-contract reconciliation
# ---------------------------------------------------------------------------
class TestReportAndContractClaims(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="evpipe-render-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_final_report_carries_evidence_provenance(self):
        sys.path.insert(0, str(SCRIPTS))
        import render_report
        run_dir = synthetic_bound_run(self.tmp)
        store = evidence_store.open_run_store(run_dir)
        store.put(evidence_store.stage_input_record(
            "independent", {"phase": "independent"}, fingerprint=FP_A,
            binding_digest=BINDING_A,
            tool={"name": "codex_runner.stage-input", "version": "2.0"},
            produced_at="2026-09-13T00:00:00Z"))
        evidence_store.serve_run_evidence(
            store, run_dir,
            store.find_records(command_or_query="stage-input:independent")[0],
            "HARNESS")
        final = {"completeness_state": "COMPLETE",
                 "repository_fingerprint_sha256": FP_A,
                 "executive_summary": "s", "findings": []}
        with open(os.path.join(run_dir, "90-final-findings.json"),
                  "w") as fh:
            json.dump(final, fh)
        md = render_report.render(run_dir, "90-final-findings")
        self.assertIn("Evidence store provenance", md)
        self.assertIn("stage-input:independent", md)
        self.assertIn("1 served", md)
        self.assertIn("CACHEABLE", md)

    def test_final_report_states_absence_honestly(self):
        sys.path.insert(0, str(SCRIPTS))
        import render_report
        final = {"completeness_state": "COMPLETE",
                 "repository_fingerprint_sha256": FP_A,
                 "executive_summary": "s", "findings": []}
        with open(os.path.join(self.tmp, "90-final-findings.json"),
                  "w") as fh:
            json.dump(final, fh)
        md = render_report.render(self.tmp, "90-final-findings")
        self.assertIn("(no evidence-store records for this run)", md)

    def test_describe_and_md_reconciled_to_wired_state(self):
        doc = json.loads(subprocess.run(
            [PYTHON, AUDIT_COUNCIL, "describe", "--json"],
            capture_output=True, text=True, check=True).stdout)
        lim = " ".join(doc["known_limitations"])
        self.assertIn("wired into the production stage path", lim)
        self.assertNotIn("not yet wired into the production stage "
                         "pipeline", lim)
        md = (SKILL_DIR / "PUBLIC-CONTRACT.md").read_text()
        self.assertIn("wired into the production stage path", md)
        self.assertNotIn("not yet wired", md)
        # the governor claim now names its enforcement point
        self.assertIn("enforced at stage-launch consumption", md)
        staging = doc["runtime_capabilities"]["evidence_staging"]
        self.assertIn("FRESH_REQUIRED evidence-store record", staging)


if __name__ == "__main__":
    unittest.main()
