#!/usr/bin/env python3
"""Tests for path_guard + hooks/path_guard_hook (PKG-A0 Tasks A0.3, A0.4).

Mechanical confinement: component-wise containment, symlink/tmp/alternate-
worktree detection, compound-command segmentation (in-root compounds stay
allowed; escapes are denied fail-closed), and the PreToolUse hook.

PROGRAM-SPEC MANDATORY REGRESSION MATRIX — case -> test mapping. Cases
1, 8-12, 19-20 live in test_env_binding.py (see the mirrored checklist
there); the A0.5 discovery cases are also in test_env_binding.py.

 2. same-HEAD alternate worktree denied
      -> TestAlternateWorktree.test_same_head_worktree_denied
 3. outside-root Read denied   -> TestCheckToolCall.test_read_outside_denied
 4. outside-root Bash denied   -> TestCheckToolCall.test_bash_outside_denied
 5. ../ denied                 -> TestCheckToolCall.test_dotdot_escape_denied
 6. repo symlink -> live repo denied
      -> TestSymlinks.test_repo_symlink_to_live_repo_denied
 7. fixture symlink -> outside denied
      -> TestSymlinks.test_fixture_symlink_outside_denied
13. git -C escape denied       -> TestScanBashEscapes.test_git_dash_C_outside_denied
14. subshell outside cd denied -> TestScanBashEscapes.test_subshell_outside_cd_denied
15. env-var outside path denied
      -> TestScanBashEscapes.test_env_var_outside_denied
16. multi-root search denied   -> TestScanBashEscapes.test_multi_root_search_denied
17. authorized fixture works   -> TestCheckToolCall.test_authorized_fixture_allowed
18. sibling fixture denied     -> TestCheckToolCall.test_sibling_fixture_denied
"""
from __future__ import annotations

import importlib.util
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
HOOKS = TESTS.parent / "hooks"
sys.path.insert(0, str(SCRIPTS))

import env_binding  # noqa: E402
import path_guard  # noqa: E402

_hook_spec = importlib.util.spec_from_file_location(
    "path_guard_hook", HOOKS / "path_guard_hook.py")
path_guard_hook = importlib.util.module_from_spec(_hook_spec)
_hook_spec.loader.exec_module(path_guard_hook)

RUN_ID = "20260904T000000Z-a0a0a0"
SANDBOX = TESTS / "fixtures" / "a0-sandbox"  # disposable, gitignore-safe


def git(repo: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(f"git {args} failed: {proc.stderr}")
    return proc.stdout


def make_repo(base: str, name: str) -> str:
    repo = os.path.join(base, name)
    os.makedirs(repo)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "a0@example.com")
    git(repo, "config", "user.name", "A0 Test")
    with open(os.path.join(repo, "app.py"), "w") as fh:
        fh.write("print('hello')\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "init")
    return repo


class GuardTestCase(unittest.TestCase):
    """Fixture root R (git repo), live repo L, same-HEAD worktree W,
    authorized fixture dir F, sibling fixture F2."""

    def setUp(self):
        SANDBOX.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="a0-pg-",
                                               dir=SANDBOX)
        self.base = os.path.realpath(self.tmp.name)
        self.root = make_repo(self.base, "root-repo")
        self.live = make_repo(self.base, "live-repo")  # unrelated outside repo
        self.worktree = os.path.join(self.base, "wt-same-head")
        git(self.root, "worktree", "add", "--detach", self.worktree, "HEAD")
        self.fixture = os.path.join(self.base, "fixtures", "fx1")
        os.makedirs(self.fixture)
        with open(os.path.join(self.fixture, "data.txt"), "w") as fh:
            fh.write("fixture data\n")
        self.fixture2 = os.path.join(self.base, "fixtures", "fx2")
        os.makedirs(self.fixture2)
        # working files inside the frozen root
        os.makedirs(os.path.join(self.root, "sub"))
        for name in ("a.txt", "b.txt", "f.txt"):
            with open(os.path.join(self.root, name), "w") as fh:
                fh.write(name + "\n")
        self.allowed = [self.fixture]

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, tool: str, tool_input: dict):
        return path_guard.check_tool_call(tool, tool_input, self.root,
                                          self.allowed)

    def scan(self, cmd: str, cwd: str | None = None):
        return path_guard.scan_bash_command(
            cmd, cwd or self.root, self.root, self.allowed)


class TestIsWithin(GuardTestCase):
    def test_is_within_componentwise_not_string_prefix(self):
        self.assertFalse(path_guard.is_within("/a/bc/x", "/a/b"))
        self.assertTrue(path_guard.is_within("/a/b/x", "/a/b"))
        self.assertTrue(path_guard.is_within("/a/b", "/a/b"))

    def test_is_within_symlink_escape_false(self):
        link = os.path.join(self.root, "to-live")
        os.symlink(self.live, link)
        self.assertFalse(path_guard.is_within(link, self.root))
        self.assertTrue(path_guard.is_within(
            os.path.join(self.root, "app.py"), self.root))

    def test_canonicalize_resolves_and_normalizes(self):
        self.assertEqual(path_guard.canonicalize("/a/./b/../c"), "/a/c")
        rel = "x/../app.py"
        with tempfile.TemporaryDirectory(prefix="a0-cwd-",
                                         dir=SANDBOX) as d:
            real = os.path.realpath(d)
            cwd = os.getcwd()
            os.chdir(d)
            try:
                self.assertEqual(path_guard.canonicalize(rel),
                                 os.path.join(real, "app.py"))
            finally:
                os.chdir(cwd)

    def test_is_within_relative_path(self):
        cwd = os.getcwd()
        os.chdir(self.root)
        try:
            self.assertTrue(path_guard.is_within("sub", self.root))
            self.assertFalse(path_guard.is_within("../evil", self.root))
        finally:
            os.chdir(cwd)


class TestCheckToolCall(GuardTestCase):
    def test_read_outside_denied(self):
        # matrix 3
        ok, reason = self.check("Read", {"file_path": "/outside/secret"})
        self.assertFalse(ok)
        self.assertEqual(reason, "PATH_ESCAPE_ATTEMPT")

    def test_read_unrelated_repo_denied(self):
        ok, reason = self.check(
            "Read", {"file_path": os.path.join(self.live, "app.py")})
        self.assertFalse(ok)
        self.assertEqual(reason, "PATH_ESCAPE_ATTEMPT")

    def test_read_inside_allowed(self):
        ok, reason = self.check(
            "Read", {"file_path": os.path.join(self.root, "app.py")})
        self.assertTrue(ok)
        self.assertIsNone(reason)

    def test_dotdot_escape_denied(self):
        # matrix 5
        evil = os.path.join(self.root, "sub", "..", "..", "evil.txt")
        ok, reason = self.check("Read", {"file_path": evil})
        self.assertFalse(ok)
        self.assertEqual(reason, "PATH_ESCAPE_ATTEMPT")

    def test_grep_and_glob_mapping(self):
        ok, reason = self.check("Grep", {"path": "/outside"})
        self.assertFalse(ok)
        self.assertEqual(reason, "PATH_ESCAPE_ATTEMPT")
        ok, reason = self.check("Glob", {"path": self.live})
        self.assertFalse(ok)
        ok, reason = self.check(
            "Grep", {"path": os.path.join(self.root, "sub")})
        self.assertTrue(ok)
        ok, reason = self.check(
            "Glob", {"path": os.path.join(self.root, "sub")})
        self.assertTrue(ok)

    def test_grep_default_path_allowed(self):
        ok, reason = self.check("Grep", {"pattern": "x"})
        self.assertTrue(ok)
        self.assertIsNone(reason)

    def test_read_missing_file_path_denied(self):
        ok, reason = self.check("Read", {})
        self.assertFalse(ok)
        self.assertEqual(reason, "PATH_ESCAPE_ATTEMPT")

    def test_unknown_tool_denied(self):
        ok, reason = self.check("Write", {"file_path": "/outside/x"})
        self.assertFalse(ok)
        self.assertEqual(reason, "PATH_ESCAPE_ATTEMPT")

    def test_authorized_fixture_allowed(self):
        # matrix 17
        ok, reason = self.check(
            "Read", {"file_path": os.path.join(self.fixture, "data.txt")})
        self.assertTrue(ok)
        self.assertIsNone(reason)

    def test_sibling_fixture_denied(self):
        # matrix 18: sibling fixture root was never authorized
        ok, reason = self.check(
            "Read", {"file_path": os.path.join(self.fixture2, "data.txt")})
        self.assertFalse(ok)

    def test_authorized_tmp_capability_root_allowed(self):
        allowed = ["/tmp/audit-council/" + RUN_ID + "/fx1"]
        ok, reason = path_guard.check_tool_call(
            "Read",
            {"file_path": "/tmp/audit-council/" + RUN_ID + "/fx1/d.bin"},
            self.root, allowed)
        self.assertTrue(ok)

    def test_sibling_fixture_under_tmp_denied(self):
        # matrix 18 (tmp layout): sibling under /tmp not in allowed roots
        allowed = ["/tmp/audit-council/" + RUN_ID + "/fx1"]
        ok, reason = path_guard.check_tool_call(
            "Read",
            {"file_path": "/tmp/audit-council/" + RUN_ID + "/fx2/d.bin"},
            self.root, allowed)
        self.assertFalse(ok)
        self.assertEqual(reason, "UNAUTHORIZED_TMP_ACCESS")

    def test_tmp_outside_allowed_roots_denied(self):
        for p in ("/tmp/evil/x", "/tmp", "/var/tmp/evil"):
            ok, reason = self.check("Read", {"file_path": p})
            self.assertFalse(ok, p)
            self.assertEqual(reason, "UNAUTHORIZED_TMP_ACCESS", p)

    def test_bash_outside_denied(self):
        # matrix 4
        ok, reason = self.check("Bash", {"command": "cat /outside/secret"})
        self.assertFalse(ok)
        self.assertEqual(reason, "PATH_ESCAPE_ATTEMPT")

    def test_bash_inside_allowed(self):
        ok, reason = self.check("Bash", {"command": "ls -la"})
        self.assertTrue(ok)
        ok, reason = self.check(
            "Bash", {"command": f"cat {self.root}/a.txt"})
        self.assertTrue(ok)

    def test_bash_cwd_outside_denied(self):
        ok, reason = self.check("Bash", {"command": "ls", "cwd": "/outside"})
        self.assertFalse(ok)
        self.assertEqual(reason, "CWD_OUTSIDE_FROZEN_ROOT")

    def test_bash_cwd_in_allowed_root_ok(self):
        ok, reason = self.check(
            "Bash", {"command": "ls", "cwd": self.fixture})
        self.assertTrue(ok)

    def test_bash_missing_command_denied(self):
        ok, reason = self.check("Bash", {})
        self.assertFalse(ok)
        self.assertEqual(reason, "PATH_ESCAPE_ATTEMPT")


class TestSymlinks(GuardTestCase):
    def test_repo_symlink_to_live_repo_denied(self):
        # matrix 6: link inside the frozen root pointing at the live repo
        link = os.path.join(self.root, "link")
        os.symlink(self.live, link)
        ok, reason = self.check("Read",
                                {"file_path": os.path.join(link, "app.py")})
        self.assertFalse(ok)
        self.assertEqual(reason, "SYMLINK_ESCAPE")

    def test_nested_symlink_escape_denied(self):
        link = os.path.join(self.root, "link")
        os.symlink(self.live, link)
        nested = os.path.join(self.root, "nested-link")
        os.symlink(link, nested)
        ok, reason = self.check(
            "Read", {"file_path": os.path.join(nested, "app.py")})
        self.assertFalse(ok)
        self.assertEqual(reason, "SYMLINK_ESCAPE")

    def test_fixture_symlink_outside_denied(self):
        # matrix 7: symlink inside an AUTHORIZED fixture root
        link = os.path.join(self.fixture, "escape")
        os.symlink(self.live, link)
        ok, reason = self.check(
            "Read", {"file_path": os.path.join(link, "app.py")})
        self.assertFalse(ok)
        self.assertEqual(reason, "SYMLINK_ESCAPE")

    def test_bash_symlink_escape_denied(self):
        link = os.path.join(self.root, "link")
        os.symlink(self.live, link)
        reasons = self.scan(f"cat {link}/app.py")
        self.assertIn("SYMLINK_ESCAPE", reasons)


class TestAlternateWorktree(GuardTestCase):
    def test_same_head_worktree_denied(self):
        # matrix 2: W is at the SAME HEAD as the frozen root
        self.assertEqual(
            git(self.root, "rev-parse", "HEAD").strip(),
            git(self.worktree, "rev-parse", "HEAD").strip())
        ok, reason = self.check(
            "Read", {"file_path": os.path.join(self.worktree, "app.py")})
        self.assertFalse(ok)
        self.assertEqual(reason, "ALTERNATE_WORKTREE_ACCESS")

    def test_worktree_via_bash_denied(self):
        reasons = self.scan(f"cat {self.worktree}/app.py")
        self.assertIn("ALTERNATE_WORKTREE_ACCESS", reasons)


class TestScanBashAllowed(GuardTestCase):
    """Pre-freeze clarification 4: ordinary in-root compound usage MUST
    stay allowed. Blanket rejection of &&, |, (), $(), ; is a FAILED
    implementation."""

    def test_compound_and_in_root_allowed(self):
        self.assertEqual(self.scan(f"cd {self.root}/sub && pytest -q"), [])

    def test_pipe_in_root_allowed(self):
        self.assertEqual(self.scan(f"cat {self.root}/a.txt | grep x"), [])

    def test_subshell_in_root_allowed(self):
        self.assertEqual(
            self.scan(f"(cd {self.root}/sub; grep y {self.root}/b.txt)"), [])

    def test_command_substitution_in_root_allowed(self):
        self.assertEqual(self.scan(f"echo $(cat {self.root}/f.txt)"), [])

    def test_semicolon_sequence_in_root_allowed(self):
        self.assertEqual(self.scan(f"cd {self.root}/sub; pwd"), [])

    def test_relative_cd_in_root_allowed(self):
        self.assertEqual(self.scan("cd sub && ls"), [])

    def test_cd_dash_in_root_allowed(self):
        self.assertEqual(self.scan("cd sub; cd -; pwd"), [])

    def test_redirect_in_root_allowed(self):
        self.assertEqual(
            self.scan(f"cat {self.root}/a.txt > {self.root}/out.txt"), [])

    def test_redirect_attached_in_root_allowed(self):
        self.assertEqual(
            self.scan(f"cat {self.root}/a.txt >{self.root}/out.txt"), [])

    def test_fd_merge_redirect_in_root_allowed(self):
        self.assertEqual(self.scan(f"grep x {self.root}/a.txt 2>&1"), [])

    def test_backtick_in_root_allowed(self):
        self.assertEqual(self.scan(f"echo `cat {self.root}/f.txt`"), [])

    def test_relative_paths_without_slash_allowed(self):
        self.assertEqual(self.scan("python -m pytest tests -q"), [])


class TestScanBashEscapes(GuardTestCase):
    def test_absolute_outside_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan("cat /outside/secret"))

    def test_dotdot_denied(self):
        reasons = self.scan(
            f"cat {os.path.join(self.root, 'sub', '..', '..', 'evil')}")
        self.assertIn("PATH_ESCAPE_ATTEMPT", reasons)

    def test_cd_outside_and_denied(self):
        self.assertIn("CWD_OUTSIDE_FROZEN_ROOT",
                      self.scan("cd /outside && cat secret"))

    def test_relative_cd_outside_denied(self):
        self.assertIn("CWD_OUTSIDE_FROZEN_ROOT",
                      self.scan("cd ../../outside && ls"))

    def test_pipe_redirect_outside_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan(f"cat {self.root}/a.txt | cat > /outside/f"))

    def test_subshell_outside_cd_denied(self):
        # matrix 14
        self.assertIn("CWD_OUTSIDE_FROZEN_ROOT",
                      self.scan("(cd /outside; cat /outside/secret)"))

    def test_command_substitution_outside_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan("echo $(cat /outside/secret)"))

    def test_backtick_outside_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan("echo `cat /outside/secret`"))

    def test_redirect_append_outside_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan(f"cat {self.root}/a.txt >> /outside/f"))

    def test_redirect_read_from_outside_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan("cat < /outside/secret"))

    def test_fd_redirect_outside_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan(f"grep x {self.root}/a.txt 2> /outside/f"))

    def test_git_dash_C_outside_denied(self):
        # matrix 13
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan("git -C /outside log"))

    def test_git_dash_C_alternate_worktree_denied(self):
        self.assertIn("ALTERNATE_WORKTREE_ACCESS",
                      self.scan(f"git -C {self.worktree} log"))

    def test_multi_root_search_denied(self):
        # matrix 16
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan(f"rg pattern /outside/evil {self.root}"))

    def test_env_var_outside_denied(self):
        # matrix 15
        with unittest.mock.patch.dict(
                os.environ, {"A0_OUTSIDE": "/outside/evil"}):
            self.assertIn("PATH_ESCAPE_ATTEMPT",
                          self.scan("cat $A0_OUTSIDE/x"))
            self.assertIn("PATH_ESCAPE_ATTEMPT",
                          self.scan("cat ${A0_OUTSIDE}/x"))

    def test_env_var_in_root_allowed(self):
        with unittest.mock.patch.dict(
                os.environ, {"A0_ROOT": self.root}):
            self.assertEqual(self.scan("cat $A0_ROOT/a.txt"), [])

    def test_env_var_unresolvable_path_denied(self):
        # UNKNOWN env form carrying a path: fail closed
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan("cat $A0_NO_SUCH_VAR/x"))

    def test_env_var_unresolvable_bare_allowed(self):
        # no path shape -> cannot be an escape; must not break normal use
        self.assertEqual(self.scan("pytest $EXTRA_FLAGS"), [])

    def test_env_assignment_outside_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan("FOO=/outside/x printenv FOO"))

    def test_unparseable_quotes_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT", self.scan('cat "unclosed'))

    def test_unclosed_substitution_denied(self):
        self.assertIn("PATH_ESCAPE_ATTEMPT",
                      self.scan("echo $(cat /outside/x"))


class HookTestCase(GuardTestCase):
    """PreToolUse hook against an isolated AUDIT_COUNCIL_CACHE_HOME."""

    def setUp(self):
        super().setUp()
        self.cache = os.path.join(self.base, "cache-home")
        self.active_dir = os.path.join(self.cache, "active-runs")
        os.makedirs(self.active_dir)
        patcher = unittest.mock.patch.dict(
            os.environ, {"AUDIT_COUNCIL_CACHE_HOME": self.cache})
        patcher.start()
        self.addCleanup(patcher.stop)

    def register_run(self, run_id: str, allowed: list[str] | None = None,
                     name: str = "run") -> str:
        brief = os.path.join(self.base, name + "-brief.md")
        with open(brief, "w") as fh:
            fh.write("# brief\n")
        binding = env_binding.capture(self.root, run_id, brief, None,
                                      allowed if allowed is not None
                                      else self.allowed)
        run_dir = os.path.join(self.base, name)
        os.makedirs(run_dir)
        with open(os.path.join(run_dir, "01-environment-binding.json"),
                  "w") as fh:
            json.dump(binding, fh)
        with open(os.path.join(self.active_dir, run_id), "w") as fh:
            fh.write(run_dir + "\n")
        return run_dir

    def hook(self, tool: str, tool_input: dict):
        return path_guard_hook.process(
            {"tool_name": tool, "tool_input": tool_input})


class TestHook(HookTestCase):
    def test_no_active_run_exit_zero(self):
        code, message = self.hook(
            "Read", {"file_path": "/etc/passwd"})
        self.assertEqual(code, 0)
        self.assertIsNone(message)

    def test_allows_within_run(self):
        self.register_run(RUN_ID)
        code, message = self.hook(
            "Read", {"file_path": os.path.join(self.root, "app.py")})
        self.assertEqual(code, 0)
        self.assertIsNone(message)

    def test_denies_outside(self):
        self.register_run(RUN_ID)
        code, message = self.hook("Read", {"file_path": "/outside/secret"})
        self.assertEqual(code, 2)
        self.assertEqual(message, "PATH_ESCAPE_ATTEMPT")

    def test_denies_bash_escape(self):
        self.register_run(RUN_ID)
        code, message = self.hook("Bash", {"command": "cat /outside/x"})
        self.assertEqual(code, 2)
        self.assertEqual(message, "PATH_ESCAPE_ATTEMPT")

    def test_allows_authorized_fixture(self):
        self.register_run(RUN_ID)
        code, message = self.hook(
            "Read", {"file_path": os.path.join(self.fixture, "data.txt")})
        self.assertEqual(code, 0)

    def test_malformed_doc_exit_two(self):
        self.register_run(RUN_ID)
        for bad in ("string", 42, None, {"no_tool": True},
                    {"tool_name": "Read"},
                    {"tool_name": "Read", "tool_input": "not-a-dict"}):
            code, _ = path_guard_hook.process(bad)
            self.assertEqual(code, 2, repr(bad))

    def test_missing_binding_exit_two(self):
        run_dir = self.register_run(RUN_ID)
        os.unlink(os.path.join(run_dir,
                               "01-environment-binding.json"))
        code, message = self.hook("Read",
                                  {"file_path": os.path.join(self.root,
                                                             "app.py")})
        self.assertEqual(code, 2)

    def test_tampered_binding_exit_two(self):
        run_dir = self.register_run(RUN_ID)
        path = os.path.join(run_dir, "01-environment-binding.json")
        doc = json.loads(Path(path).read_text())
        doc["allowed_disposable_roots"] = ["/"]
        Path(path).write_text(json.dumps(doc))
        code, message = self.hook(
            "Read", {"file_path": "/etc/passwd"})
        self.assertEqual(code, 2)

    def test_multiple_active_runs_most_restrictive(self):
        # fixture access authorized by run A but NOT run B -> denied
        self.register_run("20260904T000000Z-runa000", allowed=[self.fixture],
                          name="run-a")
        self.register_run("20260904T000000Z-runb000",
                          allowed=[self.fixture2], name="run-b")
        code, message = self.hook(
            "Read", {"file_path": os.path.join(self.fixture, "data.txt")})
        self.assertEqual(code, 2)

    def test_hook_via_subprocess(self):
        # end-to-end over stdin with /usr/bin/python3 (real hook contract)
        self.register_run(RUN_ID)
        hook_path = str(HOOKS / "path_guard_hook.py")
        env = dict(os.environ)
        deny = subprocess.run(
            [PYTHON, hook_path], input=json.dumps(
                {"tool_name": "Read",
                 "tool_input": {"file_path": "/outside/secret"},
                 "hook_event_name": "PreToolUse"}),
            capture_output=True, text=True, env=env)
        self.assertEqual(deny.returncode, 2)
        self.assertIn("PATH_ESCAPE_ATTEMPT", deny.stderr)
        allow = subprocess.run(
            [PYTHON, hook_path], input=json.dumps(
                {"tool_name": "Read",
                 "tool_input": {"file_path": os.path.join(self.root,
                                                          "app.py")}}),
            capture_output=True, text=True, env=env)
        self.assertEqual(allow.returncode, 0)
        self.assertEqual(allow.stderr, "")
        malformed = subprocess.run(
            [PYTHON, hook_path], input="not json",
            capture_output=True, text=True, env=env)
        self.assertEqual(malformed.returncode, 2)

    def test_hook_subprocess_no_active_run_zero_impact(self):
        hook_path = str(HOOKS / "path_guard_hook.py")
        proc = subprocess.run(
            [PYTHON, hook_path],
            input=json.dumps({"tool_name": "Bash",
                              "tool_input": {"command": "cat /etc/passwd"}}),
            capture_output=True, text=True,
            env=dict(os.environ))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(proc.stderr, "")


if __name__ == "__main__":
    unittest.main()
