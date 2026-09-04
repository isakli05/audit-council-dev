#!/usr/bin/env python3
"""Tests for artifact_layout (PKG-ENV Task ENV.2 — A2 artifact roots).

Covers: default root resolution (XDG injection, project-local run artifacts
preserved), config-file overrides, and category_of classification.

Determinism: every runtime root is injected to a disposable sandbox under
tests/fixtures via XDG_* / AUDIT_COUNCIL_* variables — the real user home is
never written.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

PYTHON = "/usr/bin/python3"  # NEVER sys.executable (AppImage shim on this host)

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import artifact_layout  # noqa: E402
import env_binding  # noqa: E402


def git(repo: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(f"git {args} failed: {proc.stderr}")
    return proc.stdout


def make_repo(base: str, name: str = "repo") -> str:
    repo = os.path.join(base, name)
    os.makedirs(repo)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "env@example.com")
    git(repo, "config", "user.name", "ENV Test")
    with open(os.path.join(repo, "app.py"), "w") as fh:
        fh.write("VALUE = 1\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "init")
    return repo


class ArtifactLayoutBase(unittest.TestCase):
    """Sandbox + injected XDG/env roots; real home never touched."""

    def setUp(self):
        sandbox = TESTS / "fixtures"
        sandbox.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="env-layout-",
                                                dir=str(sandbox))
        self.base = os.path.realpath(self.tmp.name)
        self.env_patch = unittest.mock.patch.dict(os.environ, {
            "AUDIT_COUNCIL_ENV_ROOT": os.path.join(self.base, "env-root"),
            "AUDIT_COUNCIL_CACHE_HOME": os.path.join(self.base, "cache-home"),
            "XDG_DATA_HOME": os.path.join(self.base, "xdg", "data"),
            "XDG_CACHE_HOME": os.path.join(self.base, "xdg", "cache"),
        })
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)
        self.repo = make_repo(self.base)
        self._cwd = os.getcwd()
        self.addCleanup(os.chdir, self._cwd)

    def tearDown(self):
        self.tmp.cleanup()


class TestResolveRootsDefaults(ArtifactLayoutBase):
    def test_xdg_defaults(self):
        # AUDIT_COUNCIL_ENV_ROOT cleared so the XDG default path is exercised
        saved = os.environ.pop("AUDIT_COUNCIL_ENV_ROOT")
        try:
            roots = artifact_layout.resolve_roots()
        finally:
            os.environ["AUDIT_COUNCIL_ENV_ROOT"] = saved
        self.assertEqual(roots["ephemeral_worktrees"], os.path.join(
            self.base, "xdg", "cache", "audit-council", "worktrees"))
        self.assertEqual(roots["benchmark_corpus"], os.path.join(
            self.base, "xdg", "data", "audit-council", "benchmark"))
        self.assertEqual(roots["long_term_history"], os.path.join(
            self.base, "xdg", "data", "audit-council", "history"))

    def test_env_root_injection_wins_for_worktrees(self):
        roots = artifact_layout.resolve_roots()
        self.assertEqual(roots["ephemeral_worktrees"],
                         os.path.join(self.base, "env-root"))

    def test_run_artifacts_stay_project_local_by_default(self):
        os.chdir(self.repo)
        roots = artifact_layout.resolve_roots()
        self.assertEqual(roots["run_artifacts_policy"], "project_local")
        self.assertEqual(roots["run_artifacts"], os.path.join(
            self.repo, "audit-output", "audit-council"))
        self.assertEqual(roots["project_evidence"],
                         os.path.join(self.repo, "audit-output"))

    def test_no_repo_means_no_project_roots(self):
        plain = os.path.join(self.base, "plain")
        os.makedirs(plain)
        with unittest.mock.patch.dict(
                os.environ, {"GIT_CEILING_DIRECTORIES": self.base}):
            os.chdir(plain)
            roots = artifact_layout.resolve_roots()
        self.assertIsNone(roots["project_evidence"])
        self.assertIsNone(roots["run_artifacts"])
        self.assertEqual(roots["run_artifacts_policy"], "project_local")

    def test_all_five_categories_present(self):
        os.chdir(self.repo)
        roots = artifact_layout.resolve_roots()
        for cat in artifact_layout.CATEGORIES:
            self.assertIn(cat, roots)
        # resolution is pure: nothing is created on disk
        self.assertFalse(os.path.exists(roots["long_term_history"]))


class TestResolveRootsConfig(ArtifactLayoutBase):
    def test_config_overrides_any_root(self):
        cfg = os.path.join(self.base, "layout.json")
        with open(cfg, "w") as fh:
            json.dump({"roots": {
                "long_term_history": os.path.join(self.base, "custom-hist"),
                "benchmark_corpus": os.path.join(self.base, "custom-bench"),
                "ephemeral_worktrees": os.path.join(self.base, "custom-wt"),
            }}, fh)
        os.chdir(self.repo)
        roots = artifact_layout.resolve_roots(cfg)
        self.assertEqual(roots["long_term_history"],
                         os.path.join(self.base, "custom-hist"))
        self.assertEqual(roots["benchmark_corpus"],
                         os.path.join(self.base, "custom-bench"))
        self.assertEqual(roots["ephemeral_worktrees"],
                         os.path.join(self.base, "custom-wt"))
        # untouched categories keep their defaults
        self.assertEqual(roots["run_artifacts"], os.path.join(
            self.repo, "audit-output", "audit-council"))
        self.assertEqual(roots["run_artifacts_policy"], "project_local")

    def test_config_run_artifacts_override_changes_policy(self):
        cfg = os.path.join(self.base, "layout2.json")
        with open(cfg, "w") as fh:
            json.dump({"run_artifacts": os.path.join(self.base, "runs")},
                      fh)
        os.chdir(self.repo)
        roots = artifact_layout.resolve_roots(cfg)
        self.assertEqual(roots["run_artifacts"],
                         os.path.join(self.base, "runs"))
        self.assertEqual(roots["run_artifacts_policy"], "config_override")

    def test_config_repo_key_pins_project_roots(self):
        # no chdir: the repo comes from the config, not the cwd
        os.chdir(self.base)
        cfg = os.path.join(self.base, "layout3.json")
        with open(cfg, "w") as fh:
            json.dump({"repo": self.repo}, fh)
        roots = artifact_layout.resolve_roots(cfg)
        self.assertEqual(roots["project_evidence"],
                         os.path.join(self.repo, "audit-output"))
        self.assertEqual(roots["run_artifacts"], os.path.join(
            self.repo, "audit-output", "audit-council"))

    def test_config_unreadable_raises(self):
        bad = os.path.join(self.base, "bad.json")
        with open(bad, "w") as fh:
            fh.write("{not json")
        with self.assertRaises(artifact_layout.ArtifactLayoutError):
            artifact_layout.resolve_roots(bad)
        with self.assertRaises(artifact_layout.ArtifactLayoutError):
            artifact_layout.resolve_roots(os.path.join(self.base, "gone.json"))


class TestCategoryOf(ArtifactLayoutBase):
    def roots(self) -> dict:
        os.chdir(self.repo)
        return artifact_layout.resolve_roots()

    def test_classifies_each_category(self):
        r = self.roots()
        cases = [
            (os.path.join(self.repo, "audit-output", "audit-council",
                          "RUN", "state.json"), "run_artifacts"),
            (os.path.join(self.repo, "audit-output", "other.txt"),
             "project_evidence"),
            (os.path.join(r["ephemeral_worktrees"], "RUN", "worktree",
                          "src.py"), "ephemeral_worktrees"),
            (os.path.join(r["benchmark_corpus"], "sealed.json"),
             "benchmark_corpus"),
            (os.path.join(r["long_term_history"], "RUN", "state.json"),
             "long_term_history"),
            ("/elsewhere/outside.txt", None),
        ]
        for path, expected in cases:
            self.assertEqual(artifact_layout.category_of(path, r), expected,
                             msg=path)

    def test_category_boundaries_are_componentwise(self):
        r = self.roots()
        # a sibling directory that shares a string prefix is NOT inside
        sibling = os.path.join(self.repo, "audit-output-extra")
        os.makedirs(sibling, exist_ok=True)
        self.assertIsNone(artifact_layout.category_of(
            os.path.join(sibling, "x.txt"), r))
        # the root itself belongs to its category
        self.assertEqual(artifact_layout.category_of(
            r["long_term_history"], r), "long_term_history")

    def test_none_roots_tolerated(self):
        r = {"project_evidence": None, "run_artifacts": None,
             "ephemeral_worktrees": os.path.join(self.base, "env-root"),
             "benchmark_corpus": None, "long_term_history": None}
        self.assertIsNone(artifact_layout.category_of(
            os.path.join(self.repo, "audit-output", "x"), r))
        self.assertEqual(artifact_layout.category_of(
            os.path.join(self.base, "env-root", "RUN"), r),
            "ephemeral_worktrees")


if __name__ == "__main__":
    unittest.main()
