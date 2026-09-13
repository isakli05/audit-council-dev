#!/usr/bin/env python3
"""Tests for env_binding (PKG-A0 Tasks A0.1, A0.2, A0.5).

Covers AuditEnvironmentBinding capture/verify (A0.1), the zero-inference
brief consistency gate (A0.2), and worktree-aware discovery via git plumbing
only (A0.5).

PROGRAM-SPEC MANDATORY REGRESSION MATRIX — case -> test mapping. Cases 2-7,
13-18 live in test_path_guard.py (see the mirrored checklist there).

 1. stale live-repo path in brief cannot redirect
      -> TestBriefGate.test_declared_root_mismatch_raises
         TestBriefGate.test_brief_prose_absolute_paths_inert
 8. quoted historical path as inert evidence allowed (no raise)
      -> TestBriefGate.test_brief_prose_absolute_paths_inert
 9. HEAD mismatch -> gate raises
      -> TestBriefGate.test_declared_head_mismatch_raises
         TestBriefGate.test_expected_head_mismatch_raises
10. root mismatch -> gate raises
      -> TestBriefGate.test_declared_root_mismatch_raises
11. correct detached worktree passes
      -> TestWorktree.test_detached_worktree_gate_passes
12. root moved/replaced during audit fails
      -> TestVerifyFrozen.test_root_missing_detected
         TestVerifyFrozen.test_root_recreated_detected
19. worktree identity stable across reconstruct
      -> TestReconstruct.test_reconstruct_worktree_identity_stable
20. binding reconstructs identically after restart (two processes)
      -> TestReconstruct.test_reconstruct_equals_frozen_except_frozen_at
         TestReconstruct.test_reconstruct_after_restart_same_digest
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
sys.path.insert(0, str(SCRIPTS))

import env_binding  # noqa: E402
import repo_fingerprint  # noqa: E402
from state_store import sha256_file  # noqa: E402

RUN_ID = "20260904T000000Z-a0a0a0"
SANDBOX = TESTS / "fixtures" / "a0-sandbox"  # disposable, gitignore-safe
FROZEN_TOOL_VERSIONS = {"git": "git-version-test"}

BINDING_FIELDS = {
    "binding_version", "binding_digest", "frozen_at", "repo_root_realpath",
    "git_toplevel_realpath", "git_dir_realpath", "git_common_dir_realpath",
    "head_sha", "detached_head", "worktree_identity",
    "source_repository_identity", "brief_sha256", "brief_target",
    "expected_head", "allowed_disposable_roots", "repo_fingerprint_sha256",
    # B-004: new bindings record the content-aware fingerprint algorithm
    "fingerprint_algorithm",
}


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
    git(repo, "config", "user.email", "a0@example.com")
    git(repo, "config", "user.name", "A0 Test")
    with open(os.path.join(repo, "app.py"), "w") as fh:
        fh.write("print('hello')\n")
    with open(os.path.join(repo, "README.md"), "w") as fh:
        fh.write("# repo\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "init")
    return repo


def make_worktree(repo: str, path: str, detach: bool = True) -> str:
    if detach:
        git(repo, "worktree", "add", "--detach", path, "HEAD")
    else:
        git(repo, "worktree", "add", path, "-b", "feature-branch")
    return path


def write_brief(base: str, text: str = "# audit brief\n") -> str:
    brief = os.path.join(base, "brief.md")
    with open(brief, "w") as fh:
        fh.write(text)
    return brief


def commit_file(repo: str, name: str, text: str, message: str) -> str:
    with open(os.path.join(repo, name), "w") as fh:
        fh.write(text)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD").strip()


# Child script used for the two-process restart tests (matrix case 20).
# Tool versions are pinned to the same frozen value as the parent so the
# fingerprint component of the digest is identical across processes.
CHILD_SCRIPT = """
import json, sys
sys.path.insert(0, sys.argv[1])
import repo_fingerprint
repo_fingerprint.tool_versions = lambda: {"git": "git-version-test"}
import env_binding
if sys.argv[2] == "reconstruct":
    doc = env_binding.reconstruct(sys.argv[3])
else:
    doc = env_binding.capture(sys.argv[3], sys.argv[4], sys.argv[5],
                              None, [])
print(json.dumps({"binding_digest": doc["binding_digest"],
                  "worktree_identity": doc["worktree_identity"],
                  "frozen_at": doc["frozen_at"]}))
"""


class A0TestCase(unittest.TestCase):
    """Shared fixture: sandbox tmp dir + a committed repo + a brief."""

    def setUp(self):
        SANDBOX.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="a0-", dir=SANDBOX)
        self.base = os.path.realpath(self.tmp.name)
        self.repo = make_repo(self.base)
        self.brief = write_brief(self.base)
        # pin tool versions for deterministic, fast fingerprints
        self._orig_versions = repo_fingerprint.tool_versions
        repo_fingerprint.tool_versions = lambda: dict(FROZEN_TOOL_VERSIONS)

    def tearDown(self):
        repo_fingerprint.tool_versions = self._orig_versions
        self.tmp.cleanup()

    def capture(self, repo: str | None = None, brief: str | None = None,
                brief_target: dict | None = None,
                allowed: list[str] | None = None) -> dict:
        return env_binding.capture(
            repo or self.repo, RUN_ID, brief or self.brief,
            brief_target, allowed if allowed is not None else [])

    def write_run_dir(self, binding: dict, run_name: str = "run") -> str:
        run_dir = os.path.join(self.base, run_name)
        os.makedirs(os.path.join(run_dir, "inputs"))
        shutil.copyfile(self.brief,
                        os.path.join(run_dir, "inputs",
                                     "original-audit-brief.md"))
        with open(os.path.join(run_dir, "01-environment-binding.json"),
                  "w") as fh:
            json.dump(binding, fh)
        return run_dir


class TestCapture(A0TestCase):
    def test_capture_plain_repo_fields(self):
        b = self.capture()
        self.assertEqual(set(b), BINDING_FIELDS)
        self.assertEqual(b["binding_version"], 2)
        self.assertEqual(b["repo_root_realpath"], os.path.realpath(self.repo))
        self.assertEqual(b["git_toplevel_realpath"],
                         os.path.realpath(self.repo))
        self.assertEqual(b["git_dir_realpath"],
                         os.path.realpath(os.path.join(self.repo, ".git")))
        self.assertEqual(b["git_common_dir_realpath"],
                         b["git_dir_realpath"])
        self.assertRegex(b["head_sha"], r"^[0-9a-f]{40}$")
        self.assertFalse(b["detached_head"])
        self.assertEqual(
            b["worktree_identity"],
            env_binding._identity(b["git_dir_realpath"],
                                  b["repo_root_realpath"]))
        self.assertEqual(b["brief_sha256"], sha256_file(self.brief))
        self.assertEqual(b["brief_target"],
                         {"declared_repository_root": None,
                          "declared_expected_head": None})
        self.assertEqual(b["expected_head"], b["head_sha"])
        self.assertEqual(b["allowed_disposable_roots"], [])
        self.assertEqual(b["source_repository_identity"]["remote_url"], None)
        self.assertEqual(b["source_repository_identity"]["common_dir_realpath"],
                         b["git_dir_realpath"])
        self.assertEqual(b["binding_digest"], env_binding.digest(b))

    def test_digest_excludes_frozen_at_and_binding_digest(self):
        b = self.capture()
        d = b["binding_digest"]
        b2 = dict(b, frozen_at="1999-01-01T00:00:00Z")
        self.assertEqual(env_binding.digest(b2), d)
        b3 = dict(b, head_sha="0" * 40)
        self.assertNotEqual(env_binding.digest(b3), d)

    def test_two_captures_produce_identical_digest(self):
        b1 = self.capture()
        b2 = self.capture()
        b2["frozen_at"] = "2030-01-01T00:00:00Z"  # injected, differs
        self.assertEqual(b1["binding_digest"], b2["binding_digest"])
        self.assertEqual(env_binding.digest(b1), env_binding.digest(b2))

    def test_capture_brief_target_normalized(self):
        target = {"declared_repository_root": os.path.realpath(self.repo),
                  "declared_expected_head": "f" * 40, "extra": "dropped"}
        b = self.capture(brief_target=target)
        self.assertEqual(b["brief_target"],
                         {"declared_repository_root":
                          os.path.realpath(self.repo),
                          "declared_expected_head": "f" * 40})
        self.assertEqual(b["expected_head"], b["head_sha"])

    def test_capture_remote_url_null_and_set(self):
        b = self.capture()
        self.assertIsNone(b["source_repository_identity"]["remote_url"])
        git(self.repo, "remote", "add", "origin",
            "https://example.com/proj.git")
        b2 = self.capture()
        self.assertEqual(b2["source_repository_identity"]["remote_url"],
                         "https://example.com/proj.git")

    def test_capture_missing_brief_raises(self):
        with self.assertRaises(env_binding.EnvironmentBindingError) as ctx:
            env_binding.capture(self.repo, RUN_ID,
                                os.path.join(self.base, "nope.md"), None, [])
        self.assertEqual(ctx.exception.reason, "BRIEF_UNREADABLE")

    def test_capture_not_a_repository_raises(self):
        plain = os.path.join(self.base, "plain")
        os.makedirs(plain)
        # the sandbox lives inside the dev tree (itself a git repo); the
        # ceiling stops git's upward walk so `plain` is genuinely repo-less
        with unittest.mock.patch.dict(
                os.environ, {"GIT_CEILING_DIRECTORIES": self.base}):
            with self.assertRaises(env_binding.EnvironmentBindingError) as ctx:
                self.capture(repo=plain)
        self.assertEqual(ctx.exception.reason, "NOT_A_REPOSITORY")

    def test_allowed_disposable_roots_canonicalized(self):
        fixture = os.path.join(self.base, "fixture")
        os.makedirs(fixture)
        b = self.capture(allowed=[fixture + os.sep + "." + os.sep,
                                  fixture])
        self.assertEqual(b["allowed_disposable_roots"],
                         [os.path.realpath(fixture)])

    def test_schema_validates_captured_binding(self):
        from validate_artifact import validate
        schema = json.loads(
            (SCHEMAS / "env-binding.schema.json").read_text())
        b = self.capture(allowed=[os.path.realpath(self.base)])
        self.assertEqual(validate(b, schema, base_dir=SCHEMAS), [])
        bad = dict(b)
        del bad["head_sha"]
        self.assertNotEqual(validate(bad, schema, base_dir=SCHEMAS), [])
        bad2 = dict(b, binding_version=1)
        self.assertNotEqual(validate(bad2, schema, base_dir=SCHEMAS), [])


class TestWorktree(A0TestCase):
    def test_detached_worktree_capture_identity_differs(self):
        wt = make_worktree(self.repo, os.path.join(self.base, "wt"))
        b_main = self.capture(self.repo)
        b_wt = self.capture(wt)
        self.assertTrue(b_wt["detached_head"])
        self.assertFalse(b_main["detached_head"])
        self.assertEqual(b_main["head_sha"], b_wt["head_sha"])  # SAME head
        # HEAD alone is NOT identity: same commit, different worktree
        self.assertNotEqual(b_main["worktree_identity"],
                            b_wt["worktree_identity"])
        self.assertEqual(b_wt["git_dir_realpath"], os.path.realpath(
            os.path.join(self.repo, ".git", "worktrees", "wt")))
        self.assertEqual(b_wt["git_common_dir_realpath"],
                         b_main["git_dir_realpath"])

    def test_detached_worktree_gate_passes(self):
        # matrix 11: correct detached worktree passes end to end
        wt = make_worktree(self.repo, os.path.join(self.base, "wt"))
        b = self.capture(wt, brief_target={
            "declared_repository_root": wt,
            "declared_expected_head": None})
        self.assertTrue(b["detached_head"])
        env_binding.assert_consistent(b)  # no raise

    def test_linked_worktree_source_repository_identity(self):
        wt = make_worktree(self.repo, os.path.join(self.base, "wt"))
        b = self.capture(wt)
        self.assertEqual(b["source_repository_identity"][
            "common_dir_realpath"], b["git_common_dir_realpath"])
        self.assertEqual(b["source_repository_identity"]["remote_url"], None)

    def test_branch_worktree_detached_head_false(self):
        wt = make_worktree(self.repo, os.path.join(self.base, "wtbr"),
                           detach=False)
        b = self.capture(wt)
        self.assertFalse(b["detached_head"])
        env_binding.assert_consistent(b)


class TestVerifyFrozen(A0TestCase):
    def test_verify_ok(self):
        b = self.capture()
        res = env_binding.verify_frozen(b)
        self.assertTrue(res["ok"], msg=str(res["reason"]))
        self.assertIsNone(res["reason"])
        self.assertEqual(res["live"]["binding_digest"],
                         b["binding_digest"])

    def test_root_missing_detected(self):
        # matrix 12 (moved): stored root no longer exists
        b = self.capture()
        shutil.move(self.repo, os.path.join(self.base, "repo-moved"))
        res = env_binding.verify_frozen(b)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "REPO_ROOT_REPLACED")

    def test_root_recreated_detected(self):
        # matrix 12 (replaced): delete + fresh `git init` at the same path
        b = self.capture()
        shutil.rmtree(self.repo)
        os.makedirs(self.repo)
        git(self.repo, "init", "-q", "-b", "main")
        res = env_binding.verify_frozen(b)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "REPO_ROOT_REPLACED")

    def test_root_replaced_by_symlink_detected(self):
        b = self.capture()
        shutil.move(self.repo, os.path.join(self.base, "repo-real"))
        os.symlink(os.path.join(self.base, "repo-real"), self.repo)
        res = env_binding.verify_frozen(b)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "REPO_ROOT_REPLACED")

    def test_head_moved_pure_movement_reason(self):
        # pure HEAD movement since freeze -> WORKTREE_IDENTITY_CHANGED
        b = self.capture()
        commit_file(self.repo, "new.py", "x = 1\n", "second")
        res = env_binding.verify_frozen(b)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "WORKTREE_IDENTITY_CHANGED")

    def test_head_moved_with_declared_head_reason(self):
        # a DECLARED expected head that no longer matches -> BRIEF_HEAD_MISMATCH
        b = self.capture(brief_target={
            "declared_repository_root": self.repo,
            "declared_expected_head": None})
        b["brief_target"]["declared_expected_head"] = b["head_sha"]
        b["binding_digest"] = env_binding.digest(b)
        commit_file(self.repo, "new.py", "x = 1\n", "second")
        res = env_binding.verify_frozen(b)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "BRIEF_HEAD_MISMATCH")

    def test_worktree_identity_changed_detected(self):
        # frozen linked worktree W from repo; W is re-created at the same
        # path but owned by a DIFFERENT repository -> identity change
        wt = make_worktree(self.repo, os.path.join(self.base, "wt"))
        b = self.capture(wt)
        git(self.repo, "worktree", "remove", "--force", wt)
        other = make_repo(self.base, name="other-repo")
        git(other, "worktree", "add", "--detach", wt, "HEAD")
        res = env_binding.verify_frozen(b)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "WORKTREE_IDENTITY_CHANGED")

    def test_tampered_binding_digest_detected(self):
        b = self.capture()
        bad = dict(b, head_sha="0" * 40)  # tamper without recomputing digest
        res = env_binding.verify_frozen(bad)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "BINDING_DIGEST_MISMATCH")


class TestBriefGate(A0TestCase):
    def test_gate_passes_with_matching_targets(self):
        b = self.capture(brief_target={
            "declared_repository_root": self.repo,
            "declared_expected_head": None})
        env_binding.assert_consistent(b)  # no raise

    def test_gate_passes_null_brief_target(self):
        b = self.capture()
        env_binding.assert_consistent(b)

    def test_declared_root_mismatch_raises(self):
        # matrix 1 + 10: the brief declares a DIFFERENT live repository as
        # the target root; the gate must refuse before any inference
        stale = make_repo(self.base, name="stale-live-repo")
        b = self.capture(brief_target={
            "declared_repository_root": stale,
            "declared_expected_head": None})
        with self.assertRaises(env_binding.EnvironmentBindingError) as ctx:
            env_binding.assert_consistent(b)
        self.assertEqual(ctx.exception.reason, "BRIEF_ROOT_MISMATCH")

    def test_declared_root_symlink_resolves_to_realpath_ok(self):
        # REALPATHS are compared, not strings: a symlinked declared root
        # that resolves to the frozen root passes
        link = os.path.join(self.base, "declared-link")
        os.symlink(self.repo, link)
        b = self.capture(brief_target={
            "declared_repository_root": link,
            "declared_expected_head": None})
        env_binding.assert_consistent(b)  # no raise

    def test_declared_head_mismatch_raises(self):
        # matrix 9
        b = self.capture(brief_target={
            "declared_repository_root": self.repo,
            "declared_expected_head": "e" * 40})
        with self.assertRaises(env_binding.EnvironmentBindingError) as ctx:
            env_binding.assert_consistent(b)
        self.assertEqual(ctx.exception.reason, "BRIEF_HEAD_MISMATCH")

    def test_expected_head_mismatch_raises(self):
        # matrix 9: expected_head must equal head_sha inside the frozen doc
        b = self.capture()
        b["expected_head"] = "e" * 40
        b["binding_digest"] = env_binding.digest(b)
        with self.assertRaises(env_binding.EnvironmentBindingError) as ctx:
            env_binding.assert_consistent(b)
        self.assertEqual(ctx.exception.reason, "BRIEF_HEAD_MISMATCH")

    def test_brief_prose_absolute_paths_inert(self):
        # matrix 8 (the exact Fifth failure mode): prose absolute paths —
        # even quoted historical ones — never affect the gate
        brief = write_brief(
            self.base,
            "# Fifth release audit\n"
            "Target repository was /home/isa/projects/llm_council_orchestrator\n"
            "See also '/home/isa/projects/llm_council_orchestrator/src'\n"
            "and /home/isa/audits/older/target paths in history.\n")
        b = self.capture(brief=brief, brief_target=None)
        env_binding.assert_consistent(b)  # no raise


class TestReconstruct(A0TestCase):
    def test_reconstruct_equals_frozen_except_frozen_at(self):
        # matrix 20
        b = self.capture()
        run_dir = self.write_run_dir(b)
        rec = env_binding.reconstruct(run_dir)
        self.assertEqual(rec["binding_digest"], b["binding_digest"])
        for key in BINDING_FIELDS - {"frozen_at"}:
            self.assertEqual(rec[key], b[key], key)

    def test_reconstruct_after_restart_same_digest(self):
        # matrix 20: a SECOND PROCESS reconstructs the same digest
        b = self.capture()
        run_dir = self.write_run_dir(b)
        proc = subprocess.run(
            [PYTHON, "-c", CHILD_SCRIPT, str(SCRIPTS), "reconstruct",
             run_dir],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        child = json.loads(proc.stdout)
        self.assertEqual(child["binding_digest"], b["binding_digest"])
        # and a fresh capture in another process yields the same identity
        proc2 = subprocess.run(
            [PYTHON, "-c", CHILD_SCRIPT, str(SCRIPTS), "capture",
             self.repo, RUN_ID, self.brief],
            capture_output=True, text=True)
        self.assertEqual(proc2.returncode, 0, proc2.stderr)
        child2 = json.loads(proc2.stdout)
        self.assertEqual(child2["binding_digest"], b["binding_digest"])
        self.assertEqual(child2["worktree_identity"], b["worktree_identity"])

    def test_reconstruct_worktree_identity_stable(self):
        # matrix 19: detached linked worktree reconstructs identically
        wt = make_worktree(self.repo, os.path.join(self.base, "wt"))
        b = self.capture(wt)
        run_dir = self.write_run_dir(b)
        rec = env_binding.reconstruct(run_dir)
        self.assertEqual(rec["worktree_identity"], b["worktree_identity"])
        self.assertEqual(rec["git_dir_realpath"], b["git_dir_realpath"])
        self.assertEqual(rec["binding_digest"], b["binding_digest"])

    def test_reconstruct_tampered_binding_raises(self):
        b = self.capture()
        run_dir = self.write_run_dir(b)
        path = os.path.join(run_dir, "01-environment-binding.json")
        doc = json.loads(Path(path).read_text())
        doc["head_sha"] = "0" * 40
        Path(path).write_text(json.dumps(doc))
        with self.assertRaises(env_binding.EnvironmentBindingError) as ctx:
            env_binding.reconstruct(run_dir)
        self.assertEqual(ctx.exception.reason, "BINDING_DIGEST_MISMATCH")


class TestDiscovery(A0TestCase):
    def test_repo_root_from_main_worktree(self):
        self.assertEqual(env_binding.repo_root_from(self.repo),
                         os.path.realpath(self.repo))

    def test_repo_root_from_linked_worktree(self):
        wt = make_worktree(self.repo, os.path.join(self.base, "wt"))
        self.assertEqual(env_binding.repo_root_from(wt),
                         os.path.realpath(wt))

    def test_repo_root_from_detached_linked_worktree(self):
        wt = make_worktree(self.repo, os.path.join(self.base, "wt"))
        self.assertEqual(env_binding.repo_root_from(wt),
                         os.path.realpath(wt))

    def test_repo_root_from_nested_cwd(self):
        nested = os.path.join(self.repo, "a", "b", "c")
        os.makedirs(nested)
        self.assertEqual(env_binding.repo_root_from(nested),
                         os.path.realpath(self.repo))

    def test_repo_root_from_non_repo_raises(self):
        plain = os.path.join(self.base, "plain")
        os.makedirs(plain)
        with unittest.mock.patch.dict(
                os.environ, {"GIT_CEILING_DIRECTORIES": self.base}):
            with self.assertRaises(env_binding.EnvironmentBindingError) as ctx:
                env_binding.repo_root_from(plain)
        self.assertEqual(ctx.exception.reason, "NOT_A_REPOSITORY")

    def test_no_git_directory_sniffing_in_source(self):
        # pre-freeze clarification 2: discovery uses git plumbing only
        source = Path(env_binding.__file__).read_text(encoding="utf-8")
        for banned in ('".git"', "'.git'", "/.git"):
            self.assertNotIn(banned, source)


class TestCacheRoot(unittest.TestCase):
    def test_cache_home_override(self):
        with unittest.mock.patch.dict(
                os.environ, {"AUDIT_COUNCIL_CACHE_HOME": "/x/cache-home"}):
            self.assertEqual(env_binding.cache_root(), "/x/cache-home")

    def test_cache_root_xdg(self):
        env = {k: v for k, v in os.environ.items()
               if k != "AUDIT_COUNCIL_CACHE_HOME"}
        env["XDG_CACHE_HOME"] = "/x/xdg"
        with unittest.mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(env_binding.cache_root(),
                             os.path.join("/x/xdg", "audit-council"))

    def test_cache_root_default_home(self):
        SANDBOX.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="a0-home-",
                                         dir=SANDBOX) as home:
            env = {k: v for k, v in os.environ.items()
                   if k not in ("AUDIT_COUNCIL_CACHE_HOME", "XDG_CACHE_HOME")}
            env["HOME"] = home
            with unittest.mock.patch.dict(os.environ, env, clear=True):
                self.assertEqual(
                    env_binding.cache_root(),
                    os.path.join(home, ".cache", "audit-council"))


if __name__ == "__main__":
    unittest.main()
