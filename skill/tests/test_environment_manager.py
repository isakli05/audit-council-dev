#!/usr/bin/env python3
"""Tests for environment_manager (PKG-ENV Tasks ENV.1 + ENV.2 — A1/A2).

Required regression coverage:
  - AUTO never silently downgrades isolation (head/root mismatch, target_ref,
    historical flag); an explicit CURRENT that violates isolation raises
    "AUTO-safety violation".
  - prepare RELEASE/HISTORICAL creates a DETACHED git worktree under the
    injected AUDIT_COUNCIL_ENV_ROOT, freezes an env_binding binding (digest
    present and reproducible), and leaves the SOURCE working tree
    byte-identical (porcelain snapshot before/after).
  - HISTORICAL stages ONLY explicitly allow-listed evidence (copied + sha256
    recorded); deny-listed paths raise; unlisted paths are not staged.
  - archive_run copies run artifacts to the long-term-history root BEFORE any
    worktree removal and then clears them out of the worktree; remove_worktree
    refuses on unarchived audit-output artifacts, uses `git worktree remove`
    only, and afterwards the source repo lists no leftover worktree.
  - kill -9 resilience: a crash inside the copy helper leaves the original run
    dir untouched and no partial archive visible (tmp-dir naming); a second
    call succeeds.
  - cleanup is dry-run by default; worktrees land under AUDIT_COUNCIL_ENV_ROOT
    in tests and nothing is written under the real user home.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

PYTHON = "/usr/bin/python3"  # NEVER sys.executable (AppImage shim on this host)

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "scripts"
SCHEMAS = TESTS.parent / "schemas"
FIXTURES = TESTS / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import artifact_layout  # noqa: E402
import environment_manager  # noqa: E402
import env_binding  # noqa: E402
import repo_fingerprint  # noqa: E402
import validate_artifact  # noqa: E402
from state_store import sha256_file  # noqa: E402

FROZEN_TOOL_VERSIONS = {"git": "git-version-test"}

RUN_A = "20260904T010101Z-a11cea"
RUN_B = "20260904T020202Z-b22ceb"
RUN_C = "20260904T030303Z-c33fec"
RUN_D = "20260904T040404Z-d44dec"
RUN_E = "20260904T050505Z-e55e1e"
RUN_F = "20260904T060606Z-f66f2f"
RUN_G = "20260904T070707Z-a77b3b"
RUN_H = "20260904T080808Z-b88c4c"
RUN_I = "20260904T090909Z-c99d5d"
RUN_Z = "20200101T000000Z-deadbe"


def git(repo: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(f"git {args} failed: {proc.stderr}")
    return proc.stdout


def make_repo(base: str, name: str = "repo") -> tuple[str, str]:
    """Fixture repo with two commits; returns (path, first-commit-sha)."""
    repo = os.path.join(base, name)
    os.makedirs(repo)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "env@example.com")
    git(repo, "config", "user.name", "ENV Test")
    with open(os.path.join(repo, "app.py"), "w") as fh:
        fh.write("VALUE = 1\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "first")
    first = git(repo, "rev-parse", "HEAD").strip()
    git(repo, "tag", "v1")
    os.makedirs(os.path.join(repo, "docs"))
    with open(os.path.join(repo, "docs", "notes.md"), "w") as fh:
        fh.write("# release notes\nstable evidence\n")
    with open(os.path.join(repo, "docs", "internal.md"), "w") as fh:
        fh.write("# internal scratch\nNOT allow-listed\n")
    with open(os.path.join(repo, "stray.txt"), "w") as fh:
        fh.write("unlisted\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "second")
    return repo, first


def snapshot_tree(root: str) -> dict:
    """(size, mtime_ns) per file under root; empty when root is absent."""
    snap: dict = {}
    if not os.path.isdir(root):
        return snap
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                st = os.lstat(path)
            except OSError:
                continue
            snap[path] = (st.st_size, st.st_mtime_ns)
    return snap


class EnvManagerBase(unittest.TestCase):
    """Sandbox repo + injected env/cache/XDG roots; real home never written."""

    def setUp(self):
        FIXTURES.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="env-mgr-",
                                                dir=str(FIXTURES))
        self.base = os.path.realpath(self.tmp.name)
        self.env_patch = unittest.mock.patch.dict(os.environ, {
            "AUDIT_COUNCIL_ENV_ROOT": os.path.join(self.base, "env-root"),
            "AUDIT_COUNCIL_CACHE_HOME": os.path.join(self.base, "cache-home"),
            "XDG_DATA_HOME": os.path.join(self.base, "xdg", "data"),
            "XDG_CACHE_HOME": os.path.join(self.base, "xdg", "cache"),
        })
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)
        self.repo, self.first_sha = make_repo(self.base)
        self.other, _ = make_repo(self.base, name="other-repo")
        self.head = git(self.repo, "rev-parse", "HEAD").strip()
        # deterministic, fast fingerprints inside the binding capture
        self._orig_versions = repo_fingerprint.tool_versions
        repo_fingerprint.tool_versions = lambda: dict(FROZEN_TOOL_VERSIONS)
        self.addCleanup(setattr, repo_fingerprint, "tool_versions",
                        self._orig_versions)
        self._cwd = os.getcwd()
        self.addCleanup(os.chdir, self._cwd)

    def tearDown(self):
        self.tmp.cleanup()

    # -- helpers -----------------------------------------------------------
    @property
    def env_root(self) -> str:
        return os.path.join(self.base, "env-root")

    @property
    def history_root(self) -> str:
        return os.path.join(self.base, "xdg", "data", "audit-council",
                            "history")

    def porcelain(self, repo: str | None = None) -> str:
        return git(repo or self.repo, "status", "--porcelain")

    def worktree_list(self, repo: str | None = None) -> str:
        return git(repo or self.repo, "worktree", "list")

    def record_schema(self) -> dict:
        return json.loads(
            (SCHEMAS / "environment-record.schema.json").read_text())

    def assert_record_valid(self, record: dict) -> None:
        errors = validate_artifact.validate(
            record, self.record_schema(), base_dir=SCHEMAS)
        self.assertEqual(errors, [], msg=str(errors))

    def contract(self, root: str | None = None, head: str | None = None,
                 **extra) -> dict:
        return {"objective": "audit", "target_repository": {
            "root": root if root is not None else self.repo,
            "head_sha": head if head is not None else self.head,
            "fingerprint_sha256": "0" * 64,
        }, **extra}

    def make_run_dir(self, worktree: str, run_id: str,
                     filename: str = "state.json") -> str:
        run_dir = os.path.join(worktree, "audit-output", "audit-council",
                               run_id)
        os.makedirs(run_dir)
        with open(os.path.join(run_dir, filename), "w") as fh:
            fh.write('{"phase": "CREATED"}\n')
        return run_dir

    def register_active(self, run_id: str, run_dir: str) -> str:
        reg = os.path.join(self.base, "cache-home", "active-runs")
        os.makedirs(reg, exist_ok=True)
        path = os.path.join(reg, run_id)
        with open(path, "w") as fh:
            fh.write(run_dir)
        return path


class TestResolveMode(EnvManagerBase):
    def setUp(self):
        super().setUp()
        os.chdir(self.repo)  # the "live" repo for AUTO derivation

    def test_auto_current_when_contract_matches_live(self):
        c = self.contract()
        self.assertEqual(environment_manager.resolve_mode(c), "CURRENT")
        self.assertEqual(environment_manager.resolve_mode(c, {"mode": "AUTO"}),
                         "CURRENT")

    def test_auto_release_when_contract_expects_different_head(self):
        c = self.contract(head="0" * 40)
        self.assertEqual(environment_manager.resolve_mode(c), "RELEASE")

    def test_auto_release_when_contract_declares_different_root(self):
        c = self.contract(root=self.other, head=self.head)
        # the other repo IS at that head; the mismatch is the ROOT vs live
        self.assertEqual(environment_manager.resolve_mode(c), "RELEASE")

    def test_auto_release_when_brief_has_target_ref(self):
        self.assertEqual(
            environment_manager.resolve_mode(self.contract(),
                                             {"target_ref": "v1"}),
            "RELEASE")

    def test_auto_release_when_contract_requires_isolation(self):
        c = self.contract(requires_isolation=True)
        self.assertEqual(environment_manager.resolve_mode(c), "RELEASE")

    def test_auto_historical_when_historical_flag(self):
        self.assertEqual(
            environment_manager.resolve_mode(self.contract(),
                                             {"historical": True}),
            "HISTORICAL")
        # historical wins over the release-only signals
        self.assertEqual(
            environment_manager.resolve_mode(
                self.contract(head="0" * 40),
                {"historical": True, "target_ref": "v1"}),
            "HISTORICAL")

    def test_requested_current_violating_isolation_raises(self):
        for meta in ({"mode": "CURRENT"},
                     {"mode": "CURRENT", "historical": True}):
            with self.assertRaises(environment_manager.EnvironmentManagerError
                                   ) as ctx:
                environment_manager.resolve_mode(
                    self.contract(head="0" * 40), meta)
            self.assertIn("AUTO-safety violation", str(ctx.exception))

    def test_requested_current_rejected_for_target_ref(self):
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.resolve_mode(
                self.contract(), {"mode": "CURRENT", "target_ref": "v1"})

    def test_requested_current_allowed_when_safe(self):
        self.assertEqual(
            environment_manager.resolve_mode(self.contract(),
                                             {"mode": "CURRENT"}),
            "CURRENT")

    def test_explicit_release_and_historical_honored(self):
        self.assertEqual(
            environment_manager.resolve_mode(self.contract(),
                                             {"mode": "RELEASE"}),
            "RELEASE")
        self.assertEqual(
            environment_manager.resolve_mode(self.contract(),
                                             {"mode": "HISTORICAL"}),
            "HISTORICAL")

    def test_unknown_mode_raises(self):
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.resolve_mode(self.contract(),
                                             {"mode": "SPURIOUS"})
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.resolve_mode(self.contract(),
                                             {"mode": "auto"})


class TestPrepareCurrent(EnvManagerBase):
    def test_prepare_current_record(self):
        before = self.porcelain()
        rec = environment_manager.prepare("CURRENT", self.repo, RUN_A)
        self.assert_record_valid(rec)
        self.assertEqual(rec["schema_version"], 2)
        self.assertEqual(rec["mode"], "CURRENT")
        self.assertEqual(rec["run_id"], RUN_A)
        self.assertIsNone(rec["worktree_root"])
        self.assertFalse(rec["worktree_detached"])
        self.assertIsNone(rec["target_ref"])
        self.assertEqual(rec["staged_evidence"], [])
        self.assertEqual(rec["archive_root"], self.history_root)
        self.assertEqual(rec["source_repo_realpath"],
                         os.path.realpath(self.repo))
        # binding digest is a real env_binding digest of the live tree
        self.assertRegex(rec["binding_digest"], r"^[0-9a-f]{64}$")
        placeholder = os.path.join(self.env_root, RUN_A,
                                   "preparation-brief.md")
        binding = env_binding.capture(self.repo, RUN_A, placeholder, None, [])
        self.assertEqual(rec["binding_digest"], binding["binding_digest"])
        # source working tree byte-identical
        self.assertEqual(self.porcelain(), before)
        # record persisted under the env root, equal to the return value
        persisted = json.loads(Path(os.path.join(
            self.env_root, RUN_A,
            environment_manager.RECORD_NAME)).read_text())
        self.assertEqual(persisted, rec)

    def test_prepare_current_refuses_target_ref(self):
        with self.assertRaises(environment_manager.EnvironmentManagerError
                               ) as ctx:
            environment_manager.prepare("CURRENT", self.repo, RUN_A,
                                        target_ref="v1")
        self.assertIn("AUTO-safety violation", str(ctx.exception))

    def test_prepare_rejects_auto_and_unknown_modes(self):
        for mode in ("AUTO", "SPURIOUS", ""):
            with self.assertRaises(environment_manager.EnvironmentManagerError):
                environment_manager.prepare(mode, self.repo, RUN_A)

    def test_prepare_rejects_malformed_run_id_and_reuse(self):
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.prepare("CURRENT", self.repo, "not-a-run-id")
        environment_manager.prepare("CURRENT", self.repo, RUN_A)
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.prepare("CURRENT", self.repo, RUN_A)

    def test_prepare_rejects_non_repo_source(self):
        plain = os.path.join(self.base, "plain")
        os.makedirs(plain)
        with unittest.mock.patch.dict(
                os.environ, {"GIT_CEILING_DIRECTORIES": self.base}):
            with self.assertRaises(environment_manager.EnvironmentManagerError):
                environment_manager.prepare("CURRENT", plain, RUN_A)


class TestPrepareRelease(EnvManagerBase):
    def test_prepare_release_detached_worktree(self):
        before = self.porcelain()
        wt_list_before = self.worktree_list()
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_B,
                                          target_ref="v1")
        self.assert_record_valid(rec)
        wt = rec["worktree_root"]
        self.assertIsNotNone(wt)
        self.assertNotEqual(wt, self.repo)
        # worktree lands under the INJECTED env root, never the real home
        self.assertTrue(wt.startswith(self.env_root + os.sep), wt)
        # DETACHED at the requested ref
        self.assertEqual(git(wt, "rev-parse", "--abbrev-ref", "HEAD").strip(),
                         "HEAD")
        self.assertEqual(git(wt, "rev-parse", "HEAD").strip(), self.first_sha)
        self.assertTrue(rec["worktree_detached"])
        self.assertEqual(rec["target_ref"], "v1")
        self.assertEqual(rec["staged_evidence"], [])
        # binding frozen ON the worktree; digest reproducible
        placeholder = os.path.join(self.env_root, RUN_B, "preparation-brief.md")
        binding = env_binding.capture(wt, RUN_B, placeholder, None, [])
        self.assertEqual(rec["binding_digest"], binding["binding_digest"])
        self.assertEqual(binding["source_repository_identity"]
                         ["common_dir_realpath"],
                         os.path.realpath(os.path.join(self.repo, ".git")))
        # source working tree byte-identical; source untouched by checkout
        self.assertEqual(self.porcelain(), before)
        # git now knows about the worktree
        self.assertIn(wt, self.worktree_list())
        self.assertNotEqual(self.worktree_list(), wt_list_before)

    def test_prepare_release_defaults_to_head(self):
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_G)
        self.assertEqual(git(rec["worktree_root"], "rev-parse", "HEAD").strip(),
                         self.head)
        self.assertIsNone(rec["target_ref"])

    def test_prepare_release_bad_ref_cleans_up(self):
        wt_list_before = self.worktree_list()
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.prepare("RELEASE", self.repo, RUN_B,
                                        target_ref="no-such-ref")
        # no half-prepared env dir, no registered worktree
        self.assertFalse(os.path.exists(os.path.join(self.env_root, RUN_B)))
        self.assertEqual(self.worktree_list(), wt_list_before)

    def test_prepare_release_stages_allowlist(self):
        # da27c0 fix 3: the public contract promises RELEASE staging —
        # the old behavior ("allow-list ignored, HISTORICAL-only") was
        # the production defect
        rec = environment_manager.prepare(
            "RELEASE", self.repo, RUN_B, target_ref="v1",
            evidence_allowlist=["docs/notes.md"])
        self.assertEqual([e["path"] for e in rec["staged_evidence"]],
                         ["docs/notes.md"])
        self.assertTrue(os.path.isfile(os.path.join(
            self.env_root, RUN_B, "staged-evidence", "docs",
            "notes.md")))


class TestPrepareHistorical(EnvManagerBase):
    def test_stages_only_allowlisted_evidence(self):
        rec = environment_manager.prepare(
            "HISTORICAL", self.repo, RUN_C, target_ref="v1",
            evidence_allowlist=["docs/notes.md"])
        self.assert_record_valid(rec)
        self.assertEqual(rec["mode"], "HISTORICAL")
        staged_dir = os.path.join(self.env_root, RUN_C, "staged-evidence")
        copied = os.path.join(staged_dir, "docs", "notes.md")
        self.assertTrue(os.path.isfile(copied))
        self.assertEqual(
            Path(copied).read_text(),
            Path(os.path.join(self.repo, "docs", "notes.md")).read_text())
        self.assertEqual(rec["staged_evidence"], [
            {"path": "docs/notes.md",
             "sha256": sha256_file(os.path.join(self.repo, "docs",
                                                "notes.md")),
             "allowed": True}])
        # unlisted files are NOT staged
        self.assertFalse(os.path.exists(
            os.path.join(staged_dir, "docs", "internal.md")))
        self.assertFalse(os.path.exists(os.path.join(staged_dir, "stray.txt")))
        # the worktree itself stays pristine (staging is outside it)
        self.assertEqual(git(rec["worktree_root"], "status", "--porcelain"),
                         "")

    def test_denylisted_paths_raise(self):
        for bad in (".git/config", "audit-output/99-metrics.json",
                    ".git"):
            with self.assertRaises(environment_manager.EnvironmentManagerError
                                   ) as ctx:
                environment_manager.prepare(
                    "HISTORICAL", self.repo, RUN_C, target_ref="v1",
                    evidence_allowlist=[bad])
            self.assertIn("deny-list", str(ctx.exception))
        self.assertFalse(os.path.exists(os.path.join(self.env_root, RUN_C)))

    def test_absolute_paths_resolved_within_source_only(self):
        rec = environment_manager.prepare(
            "HISTORICAL", self.repo, RUN_C, target_ref="v1",
            evidence_allowlist=[os.path.join(self.repo, "docs", "notes.md")])
        self.assertEqual([e["path"] for e in rec["staged_evidence"]],
                         ["docs/notes.md"])
        outside = os.path.join(self.base, "outside.txt")
        with open(outside, "w") as fh:
            fh.write("x\n")
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.prepare(
                "HISTORICAL", self.repo, RUN_D, target_ref="v1",
                evidence_allowlist=[outside])
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.prepare(
                "HISTORICAL", self.repo, RUN_D, target_ref="v1",
                evidence_allowlist=["../escape.txt"])
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.prepare(
                "HISTORICAL", self.repo, RUN_D, target_ref="v1",
                evidence_allowlist=["docs/missing.md"])


class TestArchiveAndRemoveWorktree(EnvManagerBase):
    def test_archive_before_remove(self):
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_D,
                                          target_ref="v1")
        wt = rec["worktree_root"]
        run_dir = self.make_run_dir(wt, RUN_D)

        # unarchived audit-output artifacts block removal
        with self.assertRaises(environment_manager.EnvironmentManagerError
                               ) as ctx:
            environment_manager.remove_worktree(wt)
        self.assertIn("unarchived artifacts present", str(ctx.exception))
        self.assertTrue(os.path.isdir(wt))

        # archive copies BEFORE removal, then clears the worktree copy
        dest = environment_manager.archive_run(run_dir, wt)
        self.assertEqual(dest, os.path.join(self.history_root, RUN_D))
        archived_file = os.path.join(dest, "state.json")
        self.assertTrue(os.path.isfile(archived_file))
        self.assertFalse(os.path.exists(run_dir))

        # plain `git worktree remove` now succeeds
        environment_manager.remove_worktree(wt)
        self.assertFalse(os.path.exists(wt))
        self.assertNotIn(wt, self.worktree_list())

    def test_remove_worktree_uses_git_only(self):
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_E,
                                          target_ref="v1")
        wt = rec["worktree_root"]
        run_dir = self.make_run_dir(wt, RUN_E)
        environment_manager.archive_run(run_dir, wt)
        # any raw recursive deletion must fail the test
        with unittest.mock.patch.object(
                environment_manager.shutil, "rmtree",
                side_effect=AssertionError("raw rm -rf attempted")):
            environment_manager.remove_worktree(wt)
        self.assertFalse(os.path.exists(wt))
        self.assertNotIn(wt, self.worktree_list())

    def test_remove_missing_worktree_raises(self):
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.remove_worktree(
                os.path.join(self.base, "no-such-worktree"))

    def test_archive_run_outside_worktree_keeps_original(self):
        # a run dir that does NOT live inside the worktree is archived but
        # never deleted from its original location
        run_dir = os.path.join(self.base, "loose-run")
        os.makedirs(run_dir)
        with open(os.path.join(run_dir, "state.json"), "w") as fh:
            fh.write("{}\n")
        dest = environment_manager.archive_run(run_dir, None)
        self.assertTrue(os.path.isfile(os.path.join(dest, "state.json")))
        self.assertTrue(os.path.isdir(run_dir))

    def test_archive_run_replaces_existing_archive(self):
        run_dir = os.path.join(self.base, "loose-run")
        os.makedirs(run_dir)
        with open(os.path.join(run_dir, "state.json"), "w") as fh:
            fh.write('{"v": 1}\n')
        environment_manager.archive_run(run_dir, None)
        with open(os.path.join(run_dir, "state.json"), "w") as fh:
            fh.write('{"v": 2}\n')
        dest = environment_manager.archive_run(run_dir, None)
        self.assertEqual(json.loads(
            Path(os.path.join(dest, "state.json")).read_text()), {"v": 2})
        # no stale swap dirs left behind
        leftovers = [n for n in os.listdir(self.history_root)
                     if ".tmp-" in n or ".old-" in n]
        self.assertEqual(leftovers, [])

    def test_archive_missing_run_dir_raises(self):
        with self.assertRaises(environment_manager.EnvironmentManagerError):
            environment_manager.archive_run(
                os.path.join(self.base, "gone"), None)


class TestKillNineResilience(EnvManagerBase):
    def test_crash_mid_archive_leaves_original_and_no_partial(self):
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_F,
                                          target_ref="v1")
        wt = rec["worktree_root"]
        run_dir = self.make_run_dir(wt, RUN_F, filename="90-final.json")
        original_bytes = Path(os.path.join(run_dir,
                                           "90-final.json")).read_bytes()

        # simulate kill -9 inside the copy helper on the first call
        real_copy = environment_manager._copy_tree
        calls = {"n": 0}

        def crashing_copy(src, dst):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("SIGKILL")
            return real_copy(src, dst)

        with unittest.mock.patch.object(environment_manager, "_copy_tree",
                                        crashing_copy):
            with self.assertRaises(RuntimeError):
                environment_manager.archive_run(run_dir, wt)

        # original run dir untouched, nothing removed from the worktree yet
        self.assertTrue(os.path.isdir(run_dir))
        self.assertEqual(
            Path(os.path.join(run_dir, "90-final.json")).read_bytes(),
            original_bytes)
        # no partial archive is visible under the final name, and no stale
        # tmp/swap directories linger next to it
        self.assertFalse(os.path.exists(
            os.path.join(self.history_root, RUN_F)))
        leftovers = [n for n in os.listdir(self.history_root)
                     if n.startswith(RUN_F + ".")]
        self.assertEqual(leftovers, [])

        # second call succeeds and the archive is complete
        dest = environment_manager.archive_run(run_dir, wt)
        self.assertEqual(
            Path(os.path.join(dest, "90-final.json")).read_bytes(),
            original_bytes)
        self.assertFalse(os.path.exists(run_dir))
        environment_manager.remove_worktree(wt)
        self.assertFalse(os.path.exists(wt))


class TestListRunsAndCleanup(EnvManagerBase):
    def test_list_runs_scans_env_and_archive_roots(self):
        rec_f = environment_manager.prepare("RELEASE", self.repo, RUN_F,
                                            target_ref="v1")
        run_dir = self.make_run_dir(rec_f["worktree_root"], RUN_F)
        environment_manager.archive_run(run_dir, rec_f["worktree_root"])
        environment_manager.remove_worktree(rec_f["worktree_root"])

        environment_manager.prepare("CURRENT", self.repo, RUN_G)
        rec_h = environment_manager.prepare("RELEASE", self.repo, RUN_H,
                                            target_ref="v1")
        self.make_run_dir(rec_h["worktree_root"], RUN_H)  # unarchived

        # an archive without an env record (historic run) is still listed
        os.makedirs(os.path.join(self.history_root, RUN_Z))

        runs = {r["run_id"]: r for r in environment_manager.list_runs()}
        self.assertEqual(set(runs), {RUN_F, RUN_G, RUN_H, RUN_Z})
        self.assertEqual(runs[RUN_F]["mode"], "RELEASE")
        self.assertTrue(runs[RUN_F]["archived"])
        # worktree was removed; list_runs reports on-disk reality
        self.assertIsNone(runs[RUN_F]["worktree_root"])
        self.assertEqual(runs[RUN_G]["mode"], "CURRENT")
        self.assertIsNone(runs[RUN_G]["worktree_root"])
        self.assertFalse(runs[RUN_G]["archived"])
        self.assertFalse(runs[RUN_H]["archived"])
        self.assertIsNotNone(runs[RUN_H]["worktree_root"])
        self.assertEqual(runs[RUN_Z]["archived"], True)
        self.assertIsNone(runs[RUN_Z]["repo"])
        self.assertIsNone(runs[RUN_Z]["mode"])

    def test_cleanup_is_dry_run_by_default(self):
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_I,
                                          target_ref="v1")
        wt = rec["worktree_root"]
        result = environment_manager.cleanup()
        self.assertEqual(result["removed"], [])
        self.assertIn(wt, result["would_remove"])
        self.assertTrue(os.path.isdir(wt))  # nothing removed

    def test_cleanup_executes_only_with_dry_run_false(self):
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_I,
                                          target_ref="v1")
        wt = rec["worktree_root"]
        result = environment_manager.cleanup(dry_run=False)
        self.assertIn(wt, result["removed"])
        self.assertFalse(os.path.exists(wt))
        self.assertNotIn(wt, self.worktree_list())
        # the env record dir itself is kept (it is history, not ephemeral)
        self.assertTrue(os.path.isfile(os.path.join(
            self.env_root, RUN_I, environment_manager.RECORD_NAME)))

    def test_cleanup_never_removes_active_runs(self):
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_I,
                                          target_ref="v1")
        wt = rec["worktree_root"]
        run_dir = self.make_run_dir(wt, RUN_I)
        reg = self.register_active(RUN_I, run_dir)
        result = environment_manager.cleanup(dry_run=False)
        self.assertTrue(os.path.isdir(wt))
        self.assertIn(wt, result["kept"])
        os.unlink(reg)
        # still protected while the run artifacts are unarchived
        result = environment_manager.cleanup(dry_run=False)
        self.assertTrue(os.path.isdir(wt))
        environment_manager.archive_run(run_dir, wt)
        result = environment_manager.cleanup(dry_run=False)
        self.assertFalse(os.path.exists(wt))

    def test_cleanup_keeps_unarchived_and_history(self):
        # a worktree with UNARCHIVED artifacts is never removed, even when
        # cleanup executes for real
        rec = environment_manager.prepare("RELEASE", self.repo, RUN_H,
                                          target_ref="v1")
        wt = rec["worktree_root"]
        self.make_run_dir(wt, RUN_H)  # unarchived artifacts remain
        os.makedirs(os.path.join(self.history_root, RUN_Z))
        result = environment_manager.cleanup(dry_run=False)
        self.assertTrue(os.path.isdir(wt))
        self.assertIn(wt, result["kept"])
        # history is NEVER removed by cleanup — dry-run by default and policy
        self.assertTrue(os.path.isdir(os.path.join(self.history_root, RUN_Z)))
        self.assertIn(os.path.join(self.history_root, RUN_Z),
                      result["kept"])
        # once archived (and thereby cleared from the worktree) it is removable
        run_dir = os.path.join(wt, "audit-output", "audit-council", RUN_H)
        result2 = environment_manager.cleanup()  # dry-run: still protected
        self.assertNotIn(wt, result2["would_remove"])
        environment_manager.archive_run(run_dir, wt)
        result2b = environment_manager.cleanup()  # dry-run now lists it
        self.assertIn(wt, result2b["would_remove"])
        result3 = environment_manager.cleanup(dry_run=False)
        self.assertFalse(os.path.exists(wt))
        self.assertIn(wt, result3["removed"])


class TestNothingWrittenToRealHome(EnvManagerBase):
    def test_full_flow_leaves_real_home_untouched(self):
        real_local = os.path.expanduser(
            os.path.join("~", ".local", "share", "audit-council"))
        real_cache = os.path.expanduser(
            os.path.join("~", ".cache", "audit-council"))
        before = (snapshot_tree(real_local), snapshot_tree(real_cache))

        rec = environment_manager.prepare("HISTORICAL", self.repo, RUN_A,
                                          target_ref="v1",
                                          evidence_allowlist=["docs/notes.md"])
        run_dir = self.make_run_dir(rec["worktree_root"], RUN_A)
        environment_manager.archive_run(run_dir, rec["worktree_root"])
        environment_manager.remove_worktree(rec["worktree_root"])
        environment_manager.list_runs()
        environment_manager.cleanup(dry_run=False)

        after = (snapshot_tree(real_local), snapshot_tree(real_cache))
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
