#!/usr/bin/env python3
"""Tier-4 production regression — run 20260904T222609Z-da27c0 (READ-ONLY
authoritative evidence, preserved under ~/.local/share/audit-council/
history/). Deterministic regressions for every observed harness failure:

  F1  bwrap: execvp codex — toolchain bound but missing from PATH
  F2  stale/system node selected (broken /usr/bin/node, libada.so.3)
  F3  DNS failure inside bwrap (resolv.conf symlink into /run dangling)
  F4  RELEASE evidence allow-list ignored (HISTORICAL-only) — now staged
      into the RUN dir, visible to the bubblewrapped second model
  F5  skill-owned protocols/schemas/prompts unreadable mid-run
  F6  binding linkage: record vs binding digest divergence
  F7  zero-inference sandbox preflight before attempt accounting
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

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
CODEX_RUNNER = str(SCRIPTS / "codex_runner.py")
AUDIT_COUNCIL = str(SCRIPTS / "audit_council.py")
HOOKS = Path(__file__).resolve().parent.parent / "hooks"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
RUN_DA27C0 = Path.home() / ".local/share/audit-council/history/20260904T222609Z-da27c0"

import codex_sandbox  # noqa: E402
import path_guard  # noqa: E402
import state_store  # noqa: E402

PYTHON = "python3"


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


@unittest.skipUnless(codex_sandbox.bwrap_available(), "bwrap not available")
class TestWrapperExecutionEnvironment(unittest.TestCase):
    """F1/F2/F3 — the exact three production stderr failures."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="t4-", dir=str(FIXTURES))
        self.repo = os.path.join(self.base, "repo")
        self.run_dir = os.path.join(self.repo, "audit-output", "run")
        os.makedirs(os.path.join(self.repo, "src"))
        os.makedirs(self.run_dir)
        with open(os.path.join(self.repo, "src", "a.py"), "w") as fh:
            fh.write("x = 1\n")

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def _wrap(self, payload):
        argv = codex_sandbox.build_sandbox_argv(
            payload, self.repo, self.run_dir, [])
        return subprocess.run(argv, capture_output=True, text=True,
                              timeout=90)

    def test_f1_bare_codex_executes(self):
        # production: "bwrap: execvp codex: No such file or directory"
        p = self._wrap(["codex", "--version"])
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("codex-cli", p.stdout)

    def test_f2_intended_node_runtime_selected(self):
        # production: system node + "libada.so.3: cannot open shared
        # object file". The resolved toolchain node must lead PATH.
        p = self._wrap(["sh", "-c", "command -v node && node --version"])
        self.assertEqual(p.returncode, 0, p.stderr)
        resolved = p.stdout.splitlines()[0].strip()
        self.assertNotEqual(resolved, "/usr/bin/node",
                            "stale system node shadowed the toolchain")
        real_node = os.path.realpath(shutil_which("node"))
        self.assertEqual(os.path.realpath(resolved), real_node)

    def test_f3_dns_resolution_works(self):
        # production: codex_models_manager refresh timeouts (dangling
        # resolv.conf). Zero-inference: a DNS lookup, not a model call.
        p = self._wrap(["/usr/bin/python3", "-c",
                        "import socket;"
                        "print(socket.gethostbyname('chatgpt.com'))"])
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertRegex(p.stdout.strip(), r"^\d+\.\d+\.\d+\.\d+$")

    def test_resolver_bind_is_minimal(self):
        binds = codex_sandbox._resolver_binds()
        for src, _dst in binds:
            # only the resolv.conf target file — never broad /run exposure
            self.assertTrue(os.path.isfile(src))
            self.assertEqual(os.path.basename(src),
                             os.path.basename(os.path.realpath(
                                 "/etc/resolv.conf")))

    def test_confinement_preserved_after_fixes(self):
        outside = os.path.join(self.base, "user-secret.txt")
        with open(outside, "w") as fh:
            fh.write("s\n")
        self.assertNotEqual(
            self._wrap(["cat", outside]).returncode, 0,
            "outside-root user-data read escaped")
        self.assertEqual(
            self._wrap(["cat", os.path.join(self.repo, "src",
                                            "a.py")]).returncode, 0)
        self.assertNotEqual(
            self._wrap(["sh", "-c",
                        "echo x > " + os.path.join(self.repo,
                                                   "evil.txt")]).returncode,
            0, "repo write escaped")
        self.assertEqual(
            self._wrap(["sh", "-c",
                        "echo x > " + os.path.join(self.run_dir,
                                                   "o.json")]).returncode,
            0, "run-dir output write failed")


def shutil_which(name):
    return shutil.which(name)


@unittest.skipUnless(codex_sandbox.bwrap_available(), "bwrap not available")
class TestSandboxPreflight(unittest.TestCase):
    """F7 — zero-inference preflight, before attempt accounting."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="t4p-", dir=str(FIXTURES))
        self.repo = os.path.join(self.base, "repo")
        self.run_dir = os.path.join(self.repo, "audit-output",
                                    "audit-council",
                                    "20260905T000000Z-abc123")
        os.makedirs(os.path.join(self.run_dir, "logs", "jobs"))
        os.makedirs(os.path.join(self.run_dir, "prompts"))
        os.makedirs(os.path.join(self.repo, "src"))
        with open(os.path.join(self.repo, "src", "a.py"), "w") as fh:
            fh.write("x = 1\n")
        state = state_store.new_state("20260905T000000Z-abc123", self.repo,
                                      "0" * 64)
        state_store.atomic_write_json(
            os.path.join(self.run_dir, "state.json"), state)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_preflight_passes_on_healthy_environment(self):
        result = codex_sandbox.sandbox_preflight(self.repo, self.run_dir)
        self.assertEqual(result["failures"], [], result["details"])
        self.assertTrue(result["ok"])

    def test_start_refuses_without_consuming_attempt_when_dead_env(self):
        # simulate a dead execution environment: no codex resolvable
        import unittest.mock
        env = dict(os.environ)
        env["PATH"] = "/usr/bin:/bin"  # broken-node land, no toolchain
        with unittest.mock.patch.object(
                codex_sandbox, "sandbox_preflight",
                return_value={"ok": False,
                              "failures": ["codex_executable",
                                           "dns_resolution"],
                              "details": {}}) as mocked:
            # ensure cmd_start calls the (mocked) preflight via its module
            proc = subprocess.run(
                [PYTHON, "-c",
                 "import sys; sys.path.insert(0, %r);" % str(SCRIPTS)
                 + "import unittest.mock as m, codex_runner, codex_sandbox;"
                   "p = m.patch.object(codex_sandbox, 'sandbox_preflight',"
                   " return_value={'ok': False,"
                   "'failures': ['codex_executable'], 'details': {}});"
                   "p.start();"
                   "sys.exit(codex_runner.main(['start', '--run', %r,"
                   "'--phase', 'independent', '--prompt', '-']))"
                 % self.run_dir],
                input=b"prompt", capture_output=True, check=False,
                env=dict(os.environ, CODEX_RUNNER_POLL_INTERVAL="0.05"))
        self.assertEqual(proc.returncode, 3)
        self.assertIn("SANDBOX_PREFLIGHT", proc.stderr.decode())
        self.assertIn("no model attempt consumed",
                      proc.stderr.decode())
        # attempt accounting UNTOUCHED: no job record was created
        jobs = os.listdir(os.path.join(self.run_dir, "logs", "jobs"))
        self.assertEqual(jobs, [])
        st = state_store.load_state(self.run_dir)
        self.assertEqual(st["codex"]["jobs"], [])
        self.assertEqual(st["phase_attempts"], {})

    def test_preflight_subcommand_reports(self):
        proc = subprocess.run(
            [PYTHON, CODEX_RUNNER, "sandbox-preflight",
             "--run", self.run_dir],
            capture_output=True, text=True, check=False,
            env=dict(os.environ))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout)
        self.assertTrue(doc["ok"], doc)


class TestReleaseStagingAndBindingLinkage(unittest.TestCase):
    """F4 + F6 — RELEASE staging into the run dir (second-model
    visibility, proven through the real bwrap wrapper) and the
    three-identity binding linkage."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="t4r-", dir=str(FIXTURES))
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
            fh.write("authorized evidence payload\n")
        with open(os.path.join(self.src, "a.py"), "w") as fh:
            fh.write("1\n")
        git(self.src, "add", "-A")
        git(self.src, "commit", "-q", "-m", "A")
        self.head = git(self.src, "rev-parse", "HEAD").strip()
        self.brief = os.path.join(self.base, "brief.md")
        with open(self.brief, "w") as fh:
            fh.write("# brief\nAudit A.\n")

    def tearDown(self):
        for var in ("AUDIT_COUNCIL_CACHE_HOME",
                    "AUDIT_COUNCIL_ENV_ROOT"):
            os.environ.pop(var, None)
        if os.path.isdir(self.src):
            subprocess.run(["git", "-C", self.src, "worktree", "prune"],
                           capture_output=True, check=False)
        shutil.rmtree(self.base, ignore_errors=True)

    def _prepare(self, *extra):
        proc = subprocess.run(
            [PYTHON, AUDIT_COUNCIL, "prepare", "--repo", self.src,
             "--brief", self.brief, *extra],
            capture_output=True, text=True, check=False,
            env=dict(os.environ))
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return json.loads(proc.stdout)

    def test_release_stages_authorized_evidence_into_run_dir(self):
        doc = self._prepare("--mode", "RELEASE", "--ref", self.head,
                            "--evidence-allow", "docs/notes.md")
        run_dir = doc["run"]
        staged = os.path.join(run_dir, "staged-evidence", "docs",
                              "notes.md")
        self.assertTrue(os.path.isfile(staged),
                        "RELEASE staged evidence missing from run dir")
        content = open(staged).read()
        self.assertIn("authorized evidence payload", content)

    @unittest.skipUnless(codex_sandbox.bwrap_available(),
                         "bwrap not available")
    def test_second_model_sees_staged_evidence_through_wrapper(self):
        doc = self._prepare("--mode", "RELEASE", "--ref", self.head,
                            "--evidence-allow", "docs/notes.md")
        run_dir = doc["run"]
        staged = os.path.join(run_dir, "staged-evidence", "docs",
                              "notes.md")
        argv = codex_sandbox.build_sandbox_argv(
            ["/usr/bin/cat", staged], doc["worktree_root"], run_dir, [])
        p = subprocess.run(argv, capture_output=True, text=True,
                           timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("authorized evidence payload", p.stdout)

    def test_denylist_enforced_for_release_staging(self):
        proc = subprocess.run(
            [PYTHON, AUDIT_COUNCIL, "prepare", "--repo", self.src,
             "--brief", self.brief, "--mode", "RELEASE", "--ref",
             self.head, "--evidence-allow", ".git/config"],
            capture_output=True, text=True, check=False,
            env=dict(os.environ))
        self.assertNotEqual(proc.returncode, 0, proc.stdout)

    def test_binding_linkage_all_three_identities_equal(self):
        # production divergence: binding d7b0498f… vs record f2f59adc…
        doc = self._prepare("--mode", "RELEASE", "--ref", self.head)
        run_dir = doc["run"]
        binding = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))
        state = state_store.load_state(run_dir)
        record = json.load(open(os.path.join(
            run_dir, "environment-record.json")))
        self.assertEqual(binding["binding_digest"],
                         state["env_binding_digest"])
        self.assertEqual(binding["binding_digest"],
                         record["binding_digest"],
                         "record binding digest diverged from the frozen "
                         "run binding")
        # the preparation capture survives as explicit provenance
        self.assertTrue(record.get("preparation_binding_digest"))


class TestSkillOwnedReadAccess(unittest.TestCase):
    """F5 — protocols/schemas/prompts readable; mutation still denied."""

    SKILL = Path(__file__).resolve().parent.parent

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="t4s-", dir=str(FIXTURES))
        self.root = os.path.join(self.base, "repo")
        os.makedirs(self.root)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_protocol_schema_prompt_reads_allowed(self):
        for tool, tool_input in (
                ("Read", {"file_path": str(
                    self.SKILL / "protocols" / "evidence-policy.md")}),
                ("Read", {"file_path": str(
                    self.SKILL / "schemas" / "finding.schema.json")}),
                ("Grep", {"path": str(self.SKILL / "prompts")}),
                ("Glob", {"path": str(self.SKILL / "schemas"),
                          "pattern": "*.json"}),
                ("Bash", {"command": "cat " + str(
                    self.SKILL / "prompts" / "codex-independent.md")})):
            ok, reason = path_guard.check_tool_call(
                tool, tool_input, self.root, [])
            self.assertTrue(ok, f"{tool} {tool_input}: {reason}")

    def test_skill_owned_mutation_denied(self):
        for cmd in ("echo x > " + str(self.SKILL / "protocols" / "x.md"),
                    "rm " + str(self.SKILL / "schemas" /
                                "finding.schema.json"),
                    "sed -i s/a/b/ " + str(self.SKILL / "SKILL.md"),
                    "chmod 000 " + str(self.SKILL / "prompts")):
            ok, reason = path_guard.check_tool_call(
                "Bash", {"command": cmd}, self.root, [])
            self.assertFalse(ok, cmd)

    def test_tests_tree_still_confined(self):
        ok, _ = path_guard.check_tool_call(
            "Read", {"file_path": str(
                self.SKILL / "tests" / "fixtures" / "fake_codex.py")},
            self.root, [])
        self.assertFalse(ok)


@unittest.skipUnless(RUN_DA27C0.is_dir(), "da27c0 archive not present")
class TestProductionArchivePreserved(unittest.TestCase):
    """The archive stays read-only; its divergence is understood."""

    def test_digest_divergence_documented(self):
        binding = json.load(open(RUN_DA27C0 / "01-environment-binding.json"))
        record = json.load(open(RUN_DA27C0 / "environment-record.json"))
        # pre-fix divergence (the defect this patch closes for new runs);
        # the historical run itself is never rewritten
        self.assertNotEqual(binding["binding_digest"],
                            record["binding_digest"])


if __name__ == "__main__":
    unittest.main()


class TestV201VerifierFindings(unittest.TestCase):
    """Focused-verifier N1-N3 hardening regressions."""

    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="t4n-", dir=str(FIXTURES))
        self.repo = os.path.join(self.base, "repo")
        os.makedirs(os.path.join(self.repo, "src"))

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_n1_conflicting_probe_path_fails_sanctioned(self):
        # a planted symlink at the outside-probe secret path must not
        # crash the preflight — it must return a sanctioned failure
        probe = os.path.expanduser("~/.audit-council-sbx-probe-secret")
        os.symlink("/proc/self/mem", probe)  # unwritable target
        try:
            result = codex_sandbox.sandbox_preflight(
                self.repo, self.repo)
            self.assertFalse(result["ok"])
            self.assertIn("preflight_probe_conflict",
                          result["failures"])
        finally:
            try:
                os.unlink(probe)  # preflight's own cleanup may beat us
            except FileNotFoundError:
                pass

    def test_n2_node_bindir_always_bound(self):
        argv = codex_sandbox.build_sandbox_argv(
            ["codex", "--version"], self.repo, self.repo, [])
        node = shutil.which("node")
        if node:
            nb = os.path.realpath(os.path.dirname(node))
            # the node bin dir appears as a bind (its own or via an
            # ancestor tool dir) — never only as a PATH entry
            bound = any(nb == os.path.realpath(a) or
                        nb.startswith(os.path.realpath(a) + os.sep)
                        for i, a in enumerate(argv)
                        if i > 0 and a.startswith("/") and
                        os.path.isdir(a) and
                        argv[i - 1] in ("--ro-bind", "--ro-bind-try"))
            self.assertTrue(bound, "node bin dir not bound")

    def test_n3_toolchain_binds_after_tmpfs(self):
        argv = codex_sandbox.build_sandbox_argv(
            ["codex", "--version"], self.repo, self.repo, [])
        tmpfs_at = argv.index("--tmpfs")
        for i, a in enumerate(argv):
            if a == "--ro-bind" and i > tmpfs_at:
                break
        else:
            self.fail("no toolchain bind found after --tmpfs")
