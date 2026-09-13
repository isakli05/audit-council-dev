#!/usr/bin/env python3
"""AUCDEV-010 qualification-exit stabilization regressions (QX-1..QX-5).

Every test names the finding(s) whose invariant it holds. The mechanically
reproducible subset was demonstrated RED against the audited base
(c8dda1d0 skill tree) before the fixes; see the stabilization record for
the captured RED output.
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

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

import audit_council  # noqa: E402
import codex_runner  # noqa: E402
import codex_sandbox  # noqa: E402
import repo_fingerprint  # noqa: E402
import state_store  # noqa: E402

FAKE_CODEX = os.path.join(HERE, "fixtures", "fake_codex.py")
HAVE_BWRAP = codex_sandbox.bwrap_available()


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def make_repo(path):
    os.makedirs(path, exist_ok=True)
    git(path, "init", "-q", "-b", "main")
    git(path, "config", "user.email", "t@e.com")
    git(path, "config", "user.name", "T")
    with open(os.path.join(path, "a.py"), "w") as fh:
        fh.write("x = 1\n")
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "init")
    return path


def make_run(tmp, repo, phase="OPUS_INDEPENDENT_COMPLETE"):
    run_dir = os.path.join(repo, "audit-output", "audit-council",
                           "20260913T000000Z-aa0001")
    os.makedirs(os.path.join(run_dir, "logs", "jobs"), exist_ok=True)
    os.makedirs(os.path.join(run_dir, "prompts"), exist_ok=True)
    state = state_store.new_state("20260913T000000Z-aa0001", repo, "0" * 64)
    state["phase"] = phase
    state_store.atomic_write_json(os.path.join(run_dir, "state.json"), state)
    with open(os.path.join(run_dir, "prompts", "codex-independent.md"),
              "w") as fh:
        fh.write("prompt\n")
    return run_dir


# ===========================================================================
# QX-1 — isolation / preflight / independence
# ===========================================================================
@unittest.skipUnless(HAVE_BWRAP, "bubblewrap not available")
class TestNamespaceAndEnvIsolation(unittest.TestCase):
    """F-A-01 + B-001: PID/IPC/UTS unshare + cleared environment."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="qx1-", dir=os.path.join(
            HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.base, "repo"))
        self.run_dir = make_run(self.base, self.repo)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_argv_unshares_namespaces_and_clears_env(self):
        argv = codex_sandbox.build_sandbox_argv(
            ["codex", "--version"], self.repo, self.run_dir)
        for flag in ("--unshare-pid", "--unshare-ipc", "--unshare-uts",
                     "--clearenv"):
            self.assertIn(flag, argv, f"missing {flag}")
        self.assertIn("--proc", argv)
        # network is deliberately NOT unshared (subscription API)
        self.assertNotIn("--unshare-net", argv)

    def test_procfs_shows_no_host_processes(self):
        # F-A-01/B-001 RED: on the base (no PID namespace) the sandbox's
        # /proc lists HOST processes — including other processes'
        # /proc/<pid>/environ and cwd; with --unshare-pid only sandbox
        # processes exist
        argv = codex_sandbox.build_sandbox_argv(
            ["sh", "-c",
             "ls -d /proc/[0-9]* 2>/dev/null | wc -l; "
             "cat /proc/1/comm 2>/dev/null"],
            self.repo, self.run_dir)
        proc = subprocess.run(argv, capture_output=True, text=True)
        lines = proc.stdout.strip().splitlines()
        pid_count = int(lines[0]) if lines else -1
        self.assertLess(pid_count, 10,
                        f"sandbox /proc exposes {pid_count} processes — "
                        f"host PID namespace visible (procfs not isolated)")
        comm = lines[1].strip() if len(lines) > 1 else ""
        self.assertNotEqual(comm, "systemd",
                            "PID 1 inside the sandbox is the host init")

    def test_proc_root_escape_blocked(self):
        # defense-in-depth: /proc/1/root must not reach host files even
        # though the mount-namespace tmpfs root already blocks the common
        # traversal
        outside = os.path.join(self.base, "outside-secret.txt")
        with open(outside, "w") as fh:
            fh.write("host-secret\n")
        argv = codex_sandbox.build_sandbox_argv(
            ["/usr/bin/cat", "/proc/1/root" + outside], self.repo,
            self.run_dir)
        proc = subprocess.run(argv, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0,
                            "host file readable through /proc/1/root")
        self.assertNotIn("host-secret", proc.stdout)

    def test_host_environment_does_not_leak(self):
        # B-001 RED: on the base the child inherits the whole environment
        env = dict(os.environ, AC_QX_SECRET_MARKER="leaky-token")
        argv = codex_sandbox.build_sandbox_argv(
            ["/usr/bin/env"], self.repo, self.run_dir)
        proc = subprocess.run(argv, capture_output=True, text=True, env=env)
        self.assertNotIn("AC_QX_SECRET_MARKER", proc.stdout,
                         "host environment variable leaked into sandbox")
        for expected in ("HOME=", "PATH=", "TERM=dumb", "LANG=C.UTF-8"):
            self.assertIn(expected, proc.stdout)


@unittest.skipUnless(HAVE_BWRAP, "bubblewrap not available")
class TestFirstPassBlindness(unittest.TestCase):
    """B-003: peer first-pass artifact masked for the codex independent
    stage."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="qx1b-", dir=os.path.join(
            HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.base, "repo"))
        self.run_dir = make_run(self.base, self.repo)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_peer_artifact_unreadable_and_blind_paths_recorded(self):
        peer = os.path.join(self.run_dir, "10-opus-independent.json")
        with open(peer, "w") as fh:
            fh.write('{"findings": [{"claim": "PEER-SECRET"}]}')
        blind = codex_runner._independence_blind_paths(
            self.run_dir, "independent")
        self.assertEqual(blind, [peer])
        # post-barrier stages are NOT masked
        self.assertEqual(codex_runner._independence_blind_paths(
            self.run_dir, "cross_examination"), [])
        self.assertEqual(codex_runner._independence_blind_paths(
            self.run_dir, "adjudication"), [])
        argv = codex_sandbox.build_sandbox_argv(
            ["/usr/bin/cat", peer], self.repo, self.run_dir,
            blind_paths=blind)
        proc = subprocess.run(argv, capture_output=True, text=True)
        self.assertNotIn("PEER-SECRET", proc.stdout,
                         "peer first-pass findings readable inside the "
                         "codex independent sandbox")
        # the mask is visible in the built argv (recorded mechanically)
        i = argv.index("/dev/null")
        self.assertEqual(argv[i + 1], peer)

    def test_absent_peer_artifact_masks_nothing(self):
        self.assertEqual(codex_runner._independence_blind_paths(
            self.run_dir, "independent"), [])


@unittest.skipUnless(HAVE_BWRAP, "bubblewrap not available")
class TestPreflightHostHygiene(unittest.TestCase):
    """F-A-02 + B-002 + F-A-03: no host/repo-root probe writes; argv-vector
    probes survive whitespace paths."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="qx1c-", dir=os.path.join(
            HERE, "fixtures"))
        # F-A-03: whitespace in every path the probes touch
        self.repo = make_repo(os.path.join(self.base, "my repo"))
        self.run_dir = make_run(self.base, self.repo)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def _preflight(self):
        return codex_sandbox.sandbox_preflight(
            self.repo, self.run_dir, [], codex_bin=FAKE_CODEX,
            dns_probe_host="localhost")

    def test_preflight_passes_without_host_writes(self):
        home = tempfile.mkdtemp(prefix="qx-home-", dir=self.base)
        old = os.environ.get("HOME")
        os.environ["HOME"] = home
        repo_before = sorted(os.listdir(self.repo))
        home_before = sorted(os.listdir(home))
        try:
            result = self._preflight()
            self.assertEqual(result["failures"], [],
                             json.dumps(result["details"])[:300])
            self.assertTrue(result["ok"])
        finally:
            os.environ["HOME"] = old if old is not None else ""
            if old is None:
                os.environ.pop("HOME", None)
        # F-A-02 RED: base created .ac-sbx-probe in the repo and
        # ~/.audit-council-sbx-probe-secret in the home
        self.assertEqual(sorted(os.listdir(self.repo)), repo_before,
                         "preflight mutated the frozen repo root")
        self.assertEqual(sorted(os.listdir(home)), home_before,
                         "preflight mutated the operator home")

    def test_probes_are_argv_vectors(self):
        # F-A-03 static: no shell string concatenation survives in the
        # preflight source
        src = Path(codex_sandbox.__file__).read_text(encoding="utf-8")
        preflight_src = src[src.index("def sandbox_preflight"):]
        self.assertNotIn('"echo x >> "', preflight_src)
        self.assertNotIn('"echo x > "', preflight_src)
        self.assertIn('["touch", repo_write_probe]', preflight_src)
        self.assertIn('["tee", run_file]', preflight_src)


# ===========================================================================
# QX-3 — state / concurrency / model-launch integrity
# ===========================================================================
class TestSkipVocabularyAgreement(unittest.TestCase):
    """F-A-04: CLI skip vocabulary == state.schema.json enum, and a valid
    CLI operation can never persist a schema-invalid skip record."""

    def test_skippable_phases_equal_schema_enum(self):
        schema = json.load(open(os.path.join(
            SKILL_DIR, "schemas", "state.schema.json")))
        enum = schema["properties"]["phase_skips"]["items"]["properties"][
            "skipped_phase"]["enum"]
        self.assertEqual(sorted(state_store.SKIPPABLE_PHASES), sorted(enum))
        # the over-broad phases the old CLI accepted are excluded
        for phase in ("CREATED", "PREFLIGHT_COMPLETE", "COMPLETE"):
            self.assertNotIn(phase, state_store.SKIPPABLE_PHASES)

    def test_record_phase_skips_rejects_non_enum_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(os.path.join(tmp, "repo"))
            run_dir = make_run(tmp, repo, phase="CREATED")
            with self.assertRaises(state_store.StateError):
                state_store.record_phase_skips(run_dir, [
                    {"skipped_phase": "CREATED", "reason": "x"}])

    def test_save_state_refuses_schema_invalid_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(os.path.join(tmp, "repo"))
            run_dir = make_run(tmp, repo, phase="CREATED")
            state = state_store.load_state(run_dir)
            state["phase_skips"] = [{"skipped_phase": "CREATED",
                                     "reason": "x",
                                     "recorded_at": "t"}]
            with self.assertRaises(state_store.StateError):
                state_store.save_state(run_dir, state)
            # nothing was persisted
            self.assertNotIn("phase_skips", state_store.load_state(run_dir))


class TestSkipRecordBinding(unittest.TestCase):
    """F-A-10: skip records are bound to the consuming transition and
    consumed on use; stale authorization cannot survive."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="qx3-", dir=os.path.join(
            HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.tmp, "repo"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, phase="CREATED"):
        return make_run(self.tmp, self.repo, phase=phase)

    def test_bound_skip_authorizes_only_its_transition(self):
        run_dir = self._run()
        # recorded for CREATED -> CODEX_INDEPENDENT_COMPLETE but the
        # attempted transition goes elsewhere: refused
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "CONTRACT_FROZEN", "reason": "r"}],
            from_phase="CREATED",
            to_phase="CODEX_INDEPENDENT_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.apply_transition(run_dir, "NORMALIZED")

    def test_stale_record_from_aborted_transition_authorizes_nothing(self):
        run_dir = self._run()
        state_store.apply_transition(run_dir, "CONTRACT_FROZEN")
        # a skip recorded for CONTRACT_FROZEN -> CODEX_INDEPENDENT_COMPLETE
        # whose transition never happened (aborted attempt)
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "OPUS_INDEPENDENT_COMPLETE", "reason": "r"}],
            from_phase="CONTRACT_FROZEN",
            to_phase="CODEX_INDEPENDENT_COMPLETE")
        # the run instead advances one step at a time to OPUS_INDEPENDENT_
        # COMPLETE: the stale record (bound to a different from/to) must
        # not let a later transition jump past artifact phases
        state_store.apply_transition(run_dir, "OPUS_INDEPENDENT_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.apply_transition(run_dir, "CODEX_CROSS_EXAM_COMPLETE")

    def test_consumed_record_cannot_authorize_again(self):
        run_dir = self._run()
        state_store.apply_transition(run_dir, "CONTRACT_FROZEN")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "OPUS_INDEPENDENT_COMPLETE", "reason": "r"}],
            from_phase="CONTRACT_FROZEN",
            to_phase="CODEX_INDEPENDENT_COMPLETE")
        state_store.apply_transition(run_dir, "CODEX_INDEPENDENT_COMPLETE")
        state = state_store.load_state(run_dir)
        self.assertTrue(state["phase_skips"][0]["consumed"])
        # the record is spent: a later multi-phase jump over the same
        # phase is refused even though a record naming it exists
        state_store.apply_transition(run_dir, "NORMALIZED")
        with self.assertRaises(state_store.StateError):
            state_store.apply_transition(run_dir, "CODEX_CROSS_EXAM_COMPLETE")

    def test_legacy_unbound_record_authorizes_no_new_transition(self):
        run_dir = self._run()
        # simulate a v1-era record written by old tooling: no from/to
        state = state_store.load_state(run_dir)
        state["phase_skips"] = [{"skipped_phase": "CONTRACT_FROZEN",
                                 "reason": "legacy",
                                 "recorded_at": "2026-01-01T00:00:00Z"}]
        state_store.save_state(run_dir, state)
        with self.assertRaises(state_store.StateError):
            state_store.apply_transition(run_dir, "OPUS_INDEPENDENT_COMPLETE")


class TestStageLaunchGate(unittest.TestCase):
    """B-005: model-stage launch mechanically tied to the state-machine
    phase via the authoritative state layer."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="qx3b-", dir=os.path.join(
            HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.tmp, "repo"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_launch_refused_before_contract_frozen(self):
        run_dir = make_run(self.tmp, self.repo, phase="CREATED")
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "independent")

    def test_launch_refused_at_wrong_phase(self):
        run_dir = make_run(self.tmp, self.repo, phase="CONTRACT_FROZEN")
        for stage in ("independent", "cross_examination", "adjudication"):
            with self.assertRaises(state_store.StateError):
                state_store.check_stage_launch(run_dir, stage)

    def test_launch_admitted_at_entry_phase(self):
        for stage, entry in state_store.STAGE_ENTRY_PHASE.items():
            run_dir = make_run(self.tmp, self.repo, phase=entry)
            state = state_store.check_stage_launch(run_dir, stage)
            self.assertEqual(state["phase"], entry)

    def test_launch_refused_once_stage_complete(self):
        run_dir = make_run(self.tmp, self.repo, phase="CODEX_INDEPENDENT_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "independent")

    def test_runner_start_enforces_gate(self):
        run_dir = make_run(self.tmp, self.repo, phase="CREATED")
        env = dict(os.environ, AC_CODEX_BWRAP="0",
                   CODEX_RUNNER_POLL_INTERVAL="0.02")
        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, "codex_runner.py"),
             "start", "--run", run_dir, "--phase", "independent",
             "--codex-bin", FAKE_CODEX],
            capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(proc.returncode, 3)
        self.assertIn("audit contract must be frozen", proc.stderr)


class TestConcurrentStateMutation(unittest.TestCase):
    """F-A-05: concurrent run-state writers serialize; no lost updates."""

    def test_concurrent_bumps_all_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(os.path.join(tmp, "repo"))
            run_dir = make_run(tmp, repo)
            script = (
                "import sys; sys.path.insert(0, %r);\n"
                "import state_store\n"
                "for _ in range(10):\n"
                "    state_store.bump_phase_attempt(%r, 'P')\n"
                % (SCRIPTS, run_dir))
            procs = [subprocess.Popen([sys.executable, "-c", script],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
                     for _ in range(6)]
            for p in procs:
                self.assertEqual(p.wait(timeout=120), 0)
            state = state_store.load_state(run_dir)
            self.assertEqual(state["phase_attempts"]["P"], 60,
                             "lost update under concurrent writers")

    def test_lock_file_is_run_owned_scratch_not_checksummed(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(os.path.join(tmp, "repo"))
            run_dir = make_run(tmp, repo)
            state_store.bump_phase_attempt(run_dir, "P")
            self.assertTrue(os.path.isfile(os.path.join(run_dir,
                                                        ".state.lock")))
            mismatches = state_store.verify_all(run_dir)
            self.assertEqual(mismatches, [])


# ===========================================================================
# QX-2 — target identity / freshness / completeness
# ===========================================================================
class TestContentAwareFingerprint(unittest.TestCase):
    """F-A-08 + B-004: dirty and untracked byte changes drift."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="qx2-", dir=os.path.join(
            HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.tmp, "repo"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_same_size_untracked_replacement_drifts(self):
        # B-004 RED on base: name+size only -> identical inventory
        with open(os.path.join(self.repo, "notes.txt"), "wb") as fh:
            fh.write(b"AAAAAAAAAA")
        base = repo_fingerprint.capture(self.repo)
        with open(os.path.join(self.repo, "notes.txt"), "wb") as fh:
            fh.write(b"BBBBBBBBBB")
        diff = repo_fingerprint.diff_fingerprints(
            base, repo_fingerprint.capture(self.repo))
        self.assertTrue(diff["changed"], "same-size untracked replacement "
                                         "evaded freshness detection")
        self.assertIn("notes.txt", diff["changed_untracked"])

    def test_untracked_directory_content_change_drifts(self):
        # F-A-08 RED on base: the collapsed `?? dir/` entry was a directory
        # inode size; inner byte edits were invisible
        d = os.path.join(self.repo, "newdir")
        os.makedirs(d)
        with open(os.path.join(d, "inner.txt"), "wb") as fh:
            fh.write(b"one")
        base = repo_fingerprint.capture(self.repo)
        self.assertIn(os.path.join("newdir", "inner.txt"),
                      base["untracked_inventory"],
                      "untracked directory collapsed; per-file entry absent")
        with open(os.path.join(d, "inner.txt"), "wb") as fh:
            fh.write(b"two")
        diff = repo_fingerprint.diff_fingerprints(
            base, repo_fingerprint.capture(self.repo))
        self.assertTrue(diff["changed"])
        self.assertIn(os.path.join("newdir", "inner.txt"),
                      diff["changed_untracked"])

    def test_dirty_tracked_byte_change_drifts(self):
        # B-004 RED on base: index blob sha unchanged while file is dirty
        with open(os.path.join(self.repo, "a.py"), "a") as fh:
            fh.write("y = 2\n")
        base = repo_fingerprint.capture(self.repo)
        self.assertIn("a.py", base["dirty_worktree"])
        first = base["dirty_worktree"]["a.py"]
        with open(os.path.join(self.repo, "a.py"), "a") as fh:
            fh.write("z = 3\n")
        fresh = repo_fingerprint.capture(self.repo)
        self.assertNotEqual(fresh["dirty_worktree"]["a.py"], first)
        diff = repo_fingerprint.diff_fingerprints(base, fresh)
        self.assertTrue(diff["changed"])
        self.assertIn("a.py", diff["changed_dirty_worktree"])

    def test_unchanged_tree_verifies_clean(self):
        base = repo_fingerprint.capture(self.repo)
        ok, diff = repo_fingerprint.verify(
            self.repo, _state_file_for(base))
        self.assertTrue(ok, diff)

    def test_v1_document_back_compat(self):
        # a v1-shaped stored fingerprint (int untracked entries, collapsed
        # porcelain, real blob shas) compares by exactly what it recorded
        with open(os.path.join(self.repo, "u.txt"), "wb") as fh:
            fh.write(b"old")
        collapsed = subprocess.run(
            ["git", "-C", self.repo, "status", "--porcelain"],
            capture_output=True, text=True, check=True).stdout
        tracked = {}
        for line in git(self.repo, "ls-files", "-s").splitlines():
            meta, _, path = line.partition("\t")
            mode, sha, _stage = meta.split()
            tracked[path] = {"mode": mode, "sha": sha}
        v1 = {"fingerprint_version": 1,
              "captured_at": "2026-01-01T00:00:00Z",
              "repo_root": self.repo,
              "head_sha": git(self.repo, "rev-parse", "HEAD").strip(),
              "branch": "main",
              "porcelain": collapsed,
              "tracked_inventory": tracked,
              "untracked_inventory": {"u.txt": 3},
              "tool_versions": {}}
        ok, diff = repo_fingerprint.verify(
            self.repo, _state_file_for(v1))
        self.assertTrue(ok, diff)


def _state_file_for(fingerprint):
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as fh:
        json.dump({"fingerprint": fingerprint}, fh)
    return path


class TestBindingFingerprintAlgorithm(unittest.TestCase):
    """B-004: new bindings are content-aware; legacy bindings verify under
    the algorithm they were frozen with."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="qx2b-", dir=os.path.join(
            HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.tmp, "repo"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_new_binding_records_algorithm_and_drifts_on_untracked_bytes(self):
        import env_binding
        with open(os.path.join(self.repo, "u.txt"), "wb") as fh:
            fh.write(b"AAAA")
        brief = os.path.join(self.tmp, "b.md")
        open(brief, "w").write("# b\n")
        binding = env_binding.capture(self.repo, "r", brief, None, [])
        self.assertEqual(binding.get("fingerprint_algorithm"), 2)
        # same-size untracked replacement flips the binding digest input
        with open(os.path.join(self.repo, "u.txt"), "wb") as fh:
            fh.write(b"BBBB")
        live = env_binding._capture_live(binding)
        self.assertNotEqual(live["repo_fingerprint_sha256"],
                            binding["repo_fingerprint_sha256"],
                            "binding identity blind to untracked byte "
                            "replacement")

    def test_legacy_binding_without_algorithm_field_verifies(self):
        import env_binding
        brief = os.path.join(self.tmp, "b.md")
        open(brief, "w").write("# b\n")
        with open(os.path.join(self.repo, "u.txt"), "wb") as fh:
            fh.write(b"AAAA")
        binding = env_binding.capture(self.repo, "r", brief, None, [])
        # simulate a pre-algorithm-2 binding: drop the field, recompute
        # the digest under the legacy algorithm
        legacy = {k: v for k, v in binding.items()
                  if k not in ("fingerprint_algorithm", "binding_digest")}
        legacy["repo_fingerprint_sha256"] = \
            env_binding._repo_fingerprint_digest(self.repo, algorithm=1)
        legacy["binding_digest"] = env_binding.digest(legacy)
        result = env_binding.verify_frozen(legacy)
        self.assertTrue(result["ok"], result)
        self.assertNotIn("fingerprint_algorithm", result["live"])


class TestIdentityManifest(unittest.TestCase):
    """F-A-11 + B-007: files-only-verifiable full-target identity."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="qx2c-", dir=os.path.join(
            HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.tmp, "repo"))
        with open(os.path.join(self.repo, "extra.txt"), "w") as fh:
            fh.write("untracked content\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_manifest_covers_every_tracked_file_and_is_deterministic(self):
        m1 = repo_fingerprint.identity_manifest(self.repo)
        m2 = repo_fingerprint.identity_manifest(self.repo)
        self.assertEqual(m1["manifest_sha256"], m2["manifest_sha256"])
        tracked_paths = git(self.repo, "ls-files").split()
        self.assertEqual(m1["tracked_count"], len(tracked_paths))
        for path in tracked_paths:
            self.assertIn(path, m1["tracked"])
            self.assertTrue(re.fullmatch(
                r"[0-9a-f]{64}", m1["tracked"][path]["worktree_sha256"]))

    def test_isolated_auditor_verification(self):
        # B-007: hand off ONLY the files (a plain copy, no .git) plus the
        # manifest — the isolated identity check must succeed on the copy
        # and fail on a tampered one
        manifest = repo_fingerprint.identity_manifest(self.repo)
        clean = os.path.join(self.tmp, "handoff-clean")
        tampered = os.path.join(self.tmp, "handoff-tampered")
        for dest in (clean, tampered):
            shutil.copytree(self.repo, dest,
                            ignore=shutil.ignore_patterns(".git"))
        with open(os.path.join(tampered, "a.py"), "a") as fh:
            fh.write("# tampered\n")
        self.assertEqual(repo_fingerprint.verify_files_against_manifest(
            clean, manifest), [])
        errors = repo_fingerprint.verify_files_against_manifest(
            tampered, manifest)
        self.assertTrue(errors and any("a.py" in e for e in errors), errors)

    def test_head_and_tree_recorded(self):
        m = repo_fingerprint.identity_manifest(self.repo)
        self.assertEqual(m["head_sha"],
                         git(self.repo, "rev-parse", "HEAD").strip())
        self.assertEqual(m["tree_sha"],
                         git(self.repo, "rev-parse", "HEAD^{tree}").strip())


# ===========================================================================
# QX-4 — protocol / schema / evidence plumbing
# ===========================================================================
class TestV2EvidenceFieldAlignment(unittest.TestCase):
    """B-006: active executable instructions cite the v2 typed shape."""

    FILES = ("protocols/evidence-policy.md",
             "prompts/codex-independent.md",
             "prompts/codex-cross-examine-opus.md")

    def test_no_legacy_lines_instruction(self):
        for rel in self.FILES:
            text = open(os.path.join(SKILL_DIR, rel), encoding="utf-8").read()
            # an instruction of the legacy shape (field list containing
            # `lines` as a sibling of path/symbol) must not appear
            for m in re.finditer(r"\{kind,[^}]*\}", text):
                self.assertNotIn(" lines,", m.group(0).replace(
                    "line_ranges", ""),
                    f"legacy `lines` field in {rel}: {m.group(0)[:80]}")
            self.assertNotIn("symbol + `lines`", text, rel)
            self.assertNotIn("`lines` (format", text, rel)

    def test_schema_uses_line_ranges_exclusively(self):
        schema = json.load(open(os.path.join(
            SKILL_DIR, "schemas", "finding.schema.json")))
        props = schema["properties"]["evidence"]["items"]["properties"]
        self.assertIn("line_ranges", props)
        self.assertNotIn("lines", props)
        self.assertTrue(schema["properties"]["evidence"]["items"][
            "additionalProperties"] is False)


class TestFingerprintMismatchReturnContract(unittest.TestCase):
    """F-A-13: the helper returns a list on every path."""

    def test_success_path_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(os.path.join(tmp, "repo"))
            run_dir = make_run(tmp, repo)
            state = state_store.load_state(run_dir)
            doc = {"target_repository": {
                "fingerprint_sha256": state["repo_fingerprint_sha256"]}}
            result = audit_council._fingerprint_mismatches(
                run_dir, "02-audit-contract.json", doc)
            self.assertEqual(result, [])
            self.assertIsInstance(result, list)


class TestGenericFirstPassValidator(unittest.TestCase):
    """B-008: product-shipped validator is generic by construction."""

    # tokens that must NEVER appear in the shipped validator's own bytes
    PRIOR_IDENTITY_TOKENS = (
        "0CCF9A82", "C4F14256", "c8dda1d0", "c114afe6", "d88d4692",
        "21d701b3", "8ae33444", "opus-v5", "Opus-V5", "run-9", "run9",
        "BRQ-001", "AUCDEV-010", "f8a403a7", "6be8cd62",
    )

    def _source(self):
        return open(os.path.join(SCRIPTS, "first_pass_validator.py"),
                    encoding="utf-8").read()

    def test_no_prior_event_identity_in_validator_bytes(self):
        src = self._source()
        for token in self.PRIOR_IDENTITY_TOKENS:
            self.assertNotIn(token, src,
                             f"stale prior-event identity {token!r} baked "
                             f"into the generic validator")

    def test_validation_behavior_is_parameter_driven(self):
        import first_pass_validator as fpv
        spec = {"required_headings": ["# First pass"],
                "required_literals": {"c8dda1d0": 1},
                "forbidden_literals": ["PEER-LEAK"],
                "max_bytes": 10000}
        good = "# First pass\n\ntarget c8dda1d0\n"
        self.assertEqual(fpv.validate_first_pass(good, spec), [])
        bad = "# wrong heading\ntarget c8dda1d0\nPEER-LEAK\n"
        errors = fpv.validate_first_pass(bad, spec)
        self.assertTrue(any("heading" in e for e in errors))
        self.assertTrue(any("forbidden" in e for e in errors))
        count_wrong = "# First pass\nc8dda1d0 c8dda1d0\n"
        self.assertTrue(any("occurs 2 times" in e for e in
                            fpv.validate_first_pass(count_wrong, spec)))


# ===========================================================================
# QX-5 — reproducibility / runtime guards
# ===========================================================================
class TestHookCommandFailClosed(unittest.TestCase):
    """F-A-07: mechanically resolved interpreter/skill path; fail-closed
    registration; install docs include hooks/."""

    def _frontmatter(self):
        text = open(os.path.join(SKILL_DIR, "SKILL.md"),
                    encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        assert m, "SKILL.md frontmatter missing"
        return m.group(1)

    def test_command_resolves_and_fails_closed(self):
        fm = self._frontmatter()
        try:
            import yaml
            doc = yaml.safe_load(fm)
            command = doc["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        except ImportError:
            m = re.search(r"command: '(.+)'$", fm, re.MULTILINE)
            command = m.group(1).replace("''", "'")
        # no machine-specific interpreter hard-code remains
        self.assertNotIn("/usr/bin/python3", command)
        self.assertIn("command -v python3", command)
        self.assertIn("${CLAUDE_SKILL_DIR", command)
        # fail closed: both failure branches deny (exit 2)
        self.assertEqual(command.count("exit 2"), 2)
        # behavior: broken skill dir denies
        proc = subprocess.run(
            ["sh", "-c", command], input=b"{}",
            capture_output=True,
            env=dict(os.environ, CLAUDE_SKILL_DIR="/nonexistent-qx"))
        self.assertEqual(proc.returncode, 2, proc.stderr)

    def test_readme_install_contents_include_hooks(self):
        readme = open(os.path.join(SKILL_DIR, "README.md"),
                      encoding="utf-8").read()
        install = readme[readme.index("## Installation"):
                         readme.index("## Requirements")]
        self.assertIn("hooks/", install)


class TestHermeticFakeCodex(unittest.TestCase):
    """F-A-06: the fixture codex serves the preflight probes and takes its
    control knobs from the run-dir control file (sandbox-safe)."""

    def test_version_and_login_probes_served(self):
        env = dict(os.environ)
        env.pop("FAKE_CODEX_MODE", None)
        for argv, expect in (
                (["--version"], b"codex-cli"),
                (["login", "status"], b"Logged in")):
            proc = subprocess.run(
                [sys.executable, FAKE_CODEX] + argv,
                capture_output=True, env=env, timeout=30)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn(expect, proc.stdout)

    def test_control_file_drives_mode_without_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "logs", "quota.final.json")
            os.makedirs(os.path.dirname(out))
            ctrl = os.path.join(tmp, "fake-codex-control")
            with open(ctrl, "w") as fh:
                fh.write("MODE=quota\n")
            env = {k: v for k, v in os.environ.items()
                   if not k.startswith("FAKE_CODEX")}
            proc = subprocess.run(
                [sys.executable, FAKE_CODEX, "exec", "-o", out, "-"],
                input=b"prompt", capture_output=True, env=env, timeout=30)
            self.assertEqual(proc.returncode, 1)
            self.assertIn(b"usage limit", proc.stderr)


if __name__ == "__main__":
    unittest.main()
