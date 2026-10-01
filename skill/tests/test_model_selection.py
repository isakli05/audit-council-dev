#!/usr/bin/env python3
"""AUCDEV-024 — auditor model-selection policy tests (objective §8 A..M).

Zero-provider: no real claude/codex inference is ever invoked. The policy
module, the run-state freeze, the artifact identity gate, the ambient
Claude-redirect conflict gate and the public-contract agreement are all
exercised deterministically.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PYTHON = "python3"  # NOT sys.executable (may be an embedded app host)

TESTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TESTS_DIR.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(TESTS_DIR))

import model_selection  # noqa: E402
from test_schema_validation import contract, independent_audit  # noqa: E402

AUDIT_COUNCIL = str(SCRIPTS_DIR / "audit_council.py")

# hermetic default: no ambient Claude redirect leaks into these tests, and
# no ambient effective-effort observation leaks either (the CR-IMPL-002
# gate has dedicated tests that set/remove this surface explicitly)
_CLEAN_ENV = {k: v for k, v in os.environ.items()
              if k not in model_selection.CLAUDE_SELECTION_ENV_VARS
              and k != "CLAUDE_EFFORT"}


def clean_env(**over) -> dict:
    env = dict(_CLEAN_ENV)
    env.update(over)
    return {k: v for k, v in env.items() if v is not None}


def git(repo: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(f"git {args} failed: {proc.stderr}")
    return proc.stdout


class TestAuditDefaultAndPrecedence(unittest.TestCase):
    def test_audit_default_exact_pair(self):
        opus = model_selection.resolve("opus")
        codex = model_selection.resolve("codex")
        self.assertEqual((opus["model"], opus["effort"]),
                         ("claude-opus-5-5", "high"))
        self.assertEqual((codex["model"], codex["effort"]),
                         ("gpt-6.1-sol", "high"))
        for sel in (opus, codex):
            self.assertEqual(sel["mode"], "audit-default")
            self.assertEqual(sel["source"], "audit-default")
            self.assertIsNone(sel["requested_model"])
            self.assertIsNone(sel["requested_effort"])

    def test_no_request_means_no_inherit(self):
        # inherit ONLY when explicitly requested: with ambient sources set
        # but no explicit request, the mode is still audit-default
        sel = model_selection.resolve(
            "opus", environ={"ANTHROPIC_MODEL": "claude-opus-5",
                             "CLAUDE_CODE_EFFORT_LEVEL": "high"})
        self.assertEqual(sel["mode"], "audit-default")

    def test_precedence_explicit_beats_inherit(self):
        env = {"ANTHROPIC_MODEL": "claude-opus-5",
               "CLAUDE_CODE_EFFORT_LEVEL": "high"}
        sel = model_selection.resolve("opus",
                                      explicit_model="claude-opus-5-5",
                                      explicit_effort="low",
                                      inherit_requested=True, environ=env)
        self.assertEqual(sel["mode"], "explicit")
        self.assertEqual((sel["model"], sel["effort"]),
                         ("claude-opus-5-5", "low"))

    def test_precedence_inherit_beats_default(self):
        env = {"ANTHROPIC_MODEL": "claude-opus-5",
               "CLAUDE_CODE_EFFORT_LEVEL": "medium"}
        sel = model_selection.resolve("opus", inherit_requested=True,
                                      environ=env)
        self.assertEqual(sel["mode"], "inherit")
        self.assertEqual((sel["model"], sel["effort"]),
                         ("claude-opus-5", "medium"))
        self.assertEqual(sel["source"], "claude-ambient-env")


class TestExplicitMode(unittest.TestCase):
    def test_explicit_supported_selection_frozen(self):
        sel = model_selection.resolve("codex", explicit_model="gpt-5.6-sol",
                                      explicit_effort="xhigh")
        self.assertEqual(sel["mode"], "explicit")
        self.assertEqual((sel["model"], sel["effort"]), ("gpt-5.6-sol",
                                                         "xhigh"))
        self.assertEqual(sel["requested_model"], "gpt-5.6-sol")

    def test_explicit_unsupported_model_fails_no_fallback(self):
        with self.assertRaises(model_selection.ModelSelectionError) as ctx:
            model_selection.resolve("codex", explicit_model="gpt-4o",
                                    explicit_effort="high")
        self.assertEqual(ctx.exception.reason, "UNSUPPORTED_MODEL")
        # and nothing was silently substituted — resolve raised

    def test_explicit_unsupported_effort_fails(self):
        with self.assertRaises(model_selection.ModelSelectionError) as ctx:
            model_selection.resolve("opus", explicit_model="claude-opus-5-5",
                                    explicit_effort="ultra")
        self.assertEqual(ctx.exception.reason, "UNSUPPORTED_EFFORT")

    def test_explicit_symbolic_value_fails(self):
        for symbolic in ("current", "default", "auto", "inherit", ""):
            with self.assertRaises(model_selection.ModelSelectionError) as ctx:
                model_selection.resolve("codex", explicit_model="gpt-6.1-sol",
                                        explicit_effort=symbolic)
            self.assertEqual(ctx.exception.reason, "SYMBOLIC_EFFORT",
                             symbolic)

    def test_partial_explicit_fails_closed(self):
        with self.assertRaises(model_selection.ModelSelectionError) as ctx:
            model_selection.resolve("codex", explicit_model="gpt-6.1-sol")
        self.assertEqual(ctx.exception.reason, "EXPLICIT_PARTIAL")
        with self.assertRaises(model_selection.ModelSelectionError):
            model_selection.resolve("opus", explicit_effort="high")

    def test_non_string_value_fails(self):
        with self.assertRaises(model_selection.ModelSelectionError) as ctx:
            model_selection.resolve("codex", explicit_model=42,
                                    explicit_effort="high")
        self.assertEqual(ctx.exception.reason, "UNSUPPORTED_MODEL")

    def test_legacy_identities_remain_supported(self):
        self.assertEqual(
            model_selection.resolve("opus", explicit_model="claude-opus-5",
                                    explicit_effort="high")["model"],
            "claude-opus-5")
        self.assertEqual(
            model_selection.resolve("codex", explicit_model="gpt-5.6-sol",
                                    explicit_effort="xhigh")["effort"],
            "xhigh")


class TestInheritMode(unittest.TestCase):
    def _config(self, tmp, doc: dict) -> str:
        path = os.path.join(tmp, "config.toml")
        with open(path, "w") as fh:
            for key, value in doc.items():
                fh.write('%s = "%s"\n' % (key, value))
        return path

    def test_codex_inherit_resolves_concrete(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._config(tmp, {"model": "gpt-6.1-sol",
                                      "model_reasoning_effort": "high"})
            sel = model_selection.resolve("codex", inherit_requested=True,
                                          codex_config_path=path)
        self.assertEqual(sel["mode"], "inherit")
        self.assertEqual(sel["source"], "codex-config-toml")
        self.assertEqual((sel["model"], sel["effort"]),
                         ("gpt-6.1-sol", "high"))

    def test_codex_inherit_missing_effort_key_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._config(tmp, {"model": "gpt-6.1-sol"})
            with self.assertRaises(model_selection.ModelSelectionError) as ctx:
                model_selection.resolve("codex", inherit_requested=True,
                                        codex_config_path=path)
        self.assertEqual(ctx.exception.reason, "INHERIT_UNRESOLVED")

    def test_codex_inherit_symbolic_model_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._config(tmp, {"model": "default",
                                      "model_reasoning_effort": "high"})
            with self.assertRaises(model_selection.ModelSelectionError) as ctx:
                model_selection.resolve("codex", inherit_requested=True,
                                        codex_config_path=path)
        self.assertEqual(ctx.exception.reason, "SYMBOLIC_MODEL")

    def test_codex_inherit_absent_config_fails_closed(self):
        with self.assertRaises(model_selection.ModelSelectionError) as ctx:
            model_selection.resolve("codex", inherit_requested=True,
                                    codex_config_path="/nonexistent/config.toml")
        self.assertEqual(ctx.exception.reason, "INHERIT_UNRESOLVED")

    def test_claude_inherit_resolves_concrete(self):
        sel = model_selection.resolve(
            "opus", inherit_requested=True,
            environ={"ANTHROPIC_MODEL": "claude-opus-5-5",
                     "CLAUDE_CODE_EFFORT_LEVEL": "high"})
        self.assertEqual(sel["mode"], "inherit")
        self.assertEqual((sel["model"], sel["effort"]),
                         ("claude-opus-5-5", "high"))

    def test_claude_inherit_missing_effort_fails_closed(self):
        # an ambient model redirect alone does not satisfy the effort half
        with self.assertRaises(model_selection.ModelSelectionError) as ctx:
            model_selection.resolve("opus", inherit_requested=True,
                                    environ={"ANTHROPIC_MODEL":
                                             "claude-opus-5-5"})
        self.assertEqual(ctx.exception.reason, "INHERIT_UNRESOLVED")

    def test_claude_inherit_alias_redirect_fails_closed(self):
        # the live host redirect value is NOT a supported exact identity
        with self.assertRaises(model_selection.ModelSelectionError) as ctx:
            model_selection.resolve(
                "opus", inherit_requested=True,
                environ={"ANTHROPIC_MODEL": "glm-5.3[1m]",
                         "CLAUDE_CODE_EFFORT_LEVEL": "max"})
        self.assertEqual(ctx.exception.reason, "UNSUPPORTED_MODEL")


class TestProvenanceFreezeAndTamper(unittest.TestCase):
    def test_freeze_record_shape_and_digest(self):
        sel = model_selection.resolve("codex")
        record = model_selection.freeze_record(sel, client_version="x",
                                               frozen_at="2026-10-01T00:00:00Z")
        for key in ("auditor", "mode", "source", "requested_model",
                    "requested_effort", "model", "effort", "client_version",
                    "frozen_at", "selection_digest"):
            self.assertIn(key, record)
        self.assertRegex(record["selection_digest"], "^[0-9a-f]{64}$")

    def test_verify_frozen_roundtrip(self):
        record = model_selection.freeze_record(
            model_selection.resolve("opus"), frozen_at="2026-10-01T00:00:00Z")
        sel = model_selection.verify_frozen(record)
        self.assertEqual((sel["model"], sel["effort"]),
                         ("claude-opus-5-5", "high"))

    def test_tampered_resolved_model_rejected(self):
        record = model_selection.freeze_record(
            model_selection.resolve("codex"), frozen_at="t")
        record["model"] = "gpt-5.6-sol"  # silent-migration attempt
        with self.assertRaises(model_selection.ModelSelectionError) as ctx:
            model_selection.verify_frozen(record)
        self.assertEqual(ctx.exception.reason, "FROZEN_RECORD_TAMPERED")

    def test_tampered_mode_rejected(self):
        record = model_selection.freeze_record(
            model_selection.resolve("codex"), frozen_at="t")
        record["mode"] = "explicit"
        with self.assertRaises(model_selection.ModelSelectionError):
            model_selection.verify_frozen(record)

    def test_frozen_selection_accessor(self):
        state = {"model_selection": {"codex": {"auditor": "codex"}}}
        self.assertEqual(model_selection.frozen_selection(state, "codex"),
                         {"auditor": "codex"})
        self.assertIsNone(model_selection.frozen_selection(state, "opus"))
        self.assertIsNone(model_selection.frozen_selection({}, "codex"))
        self.assertIsNone(model_selection.frozen_selection(None, "codex"))


class TestAmbientConflictGate(unittest.TestCase):
    def test_no_ambient_vars_no_conflict(self):
        self.assertEqual(
            model_selection.claude_ambient_conflicts(
                "claude-opus-5-5", "high", environ={}), [])

    def test_matching_ambient_vars_pass(self):
        env = {"ANTHROPIC_MODEL": "claude-opus-5-5",
               "CLAUDE_CODE_EFFORT_LEVEL": "high"}
        self.assertEqual(
            model_selection.claude_ambient_conflicts(
                "claude-opus-5-5", "high", environ=env), [])

    def test_conflicting_model_redirect_detected(self):
        conflicts = model_selection.claude_ambient_conflicts(
            "claude-opus-5-5", "high",
            environ={"ANTHROPIC_MODEL": "glm-5.3[1m]"})
        self.assertEqual(conflicts, ["ANTHROPIC_MODEL"])

    def test_conflicting_default_and_subagent_redirects_detected(self):
        conflicts = model_selection.claude_ambient_conflicts(
            "claude-opus-5-5", "high",
            environ={"ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.3[1m]",
                     "CLAUDE_CODE_SUBAGENT_MODEL": "glm-5.3[1m]"})
        self.assertEqual(conflicts, ["ANTHROPIC_DEFAULT_OPUS_MODEL",
                                     "CLAUDE_CODE_SUBAGENT_MODEL"])

    def test_conflicting_effort_detected(self):
        # the live host pins CLAUDE_CODE_EFFORT_LEVEL=max — not `high`
        conflicts = model_selection.claude_ambient_conflicts(
            "claude-opus-5-5", "high",
            environ={"CLAUDE_CODE_EFFORT_LEVEL": "max"})
        self.assertEqual(conflicts, ["CLAUDE_CODE_EFFORT_LEVEL"])

    def test_legacy_generation_is_still_a_conflict_for_new_selection(self):
        conflicts = model_selection.claude_ambient_conflicts(
            "claude-opus-5-5", "high",
            environ={"ANTHROPIC_MODEL": "claude-opus-5"})
        self.assertEqual(conflicts, ["ANTHROPIC_MODEL"])

    def test_gate_reports_names_only_never_values(self):
        # the helper returns variable NAMES; values never leak
        conflicts = model_selection.claude_ambient_conflicts(
            "claude-opus-5-5", "high",
            environ={"ANTHROPIC_MODEL": "SECRETVALUE"})
        self.assertEqual(conflicts, ["ANTHROPIC_MODEL"])
        self.assertNotIn("SECRETVALUE", conflicts)


# ---------------------------------------------------------------------------
# CLI-level gates (audit_council.py): preflight / init-run / resume-check /
# artifact identity
# ---------------------------------------------------------------------------

class TestEffectiveEffortGateUnit(unittest.TestCase):
    """AUCDEV024-CR-IMPL-002: the observable per-turn EFFECTIVE Claude
    effort (readiness-probe surface CLAUDE_EFFORT, reflecting the effort
    the session ACTUALLY runs at after any client downgrade/clamp) must
    mechanically equal the resolved/frozen Auditor-A effort. Absent or
    mismatched fails closed; the observed value is never echoed back."""

    def test_effective_effort_equal_passes(self):
        self.assertIsNone(model_selection.claude_effective_effort_violation(
            "high",
            environ={model_selection.CLAUDE_EFFECTIVE_EFFORT_ENV: "high"}))

    def test_effective_effort_mismatch_fails_closed(self):
        violation = model_selection.claude_effective_effort_violation(
            "high",
            environ={model_selection.CLAUDE_EFFECTIVE_EFFORT_ENV: "medium"})
        self.assertEqual(violation, "EFFECTIVE_EFFORT_MISMATCH")
        self.assertNotIn("medium", violation)  # tokens only, never the value

    def test_effective_effort_missing_fails_closed(self):
        self.assertEqual(
            model_selection.claude_effective_effort_violation(
                "high", environ={}),
            "EFFECTIVE_EFFORT_UNOBSERVABLE")

    def test_blank_surface_is_unobservable(self):
        self.assertEqual(
            model_selection.claude_effective_effort_violation(
                "high",
                environ={model_selection.CLAUDE_EFFECTIVE_EFFORT_ENV: "  "}),
            "EFFECTIVE_EFFORT_UNOBSERVABLE")

    def test_comparison_is_case_normalized(self):
        self.assertIsNone(model_selection.claude_effective_effort_violation(
            "high",
            environ={model_selection.CLAUDE_EFFECTIVE_EFFORT_ENV: "HIGH"}))


class CliBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cache = os.path.join(self._tmp.name, "cache")
        self.repo = os.path.join(self._tmp.name, "repo")
        os.makedirs(self.repo)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "t@e.com")
        git(self.repo, "config", "user.name", "t")
        with open(os.path.join(self.repo, "a.py"), "w") as fh:
            fh.write("1\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "c")
        self.brief = os.path.join(self._tmp.name, "b.md")
        with open(self.brief, "w") as fh:
            fh.write("# brief\nAudit.\n")

    def tearDown(self):
        self._tmp.cleanup()

    def cli(self, *args, stdin=None, env=None):
        # default session surface: the sanctioned audit posture (audit-
        # default Auditor A = claude-opus-5-5/high with effective high)
        return subprocess.run(
            [PYTHON, AUDIT_COUNCIL, *args], input=stdin,
            capture_output=True, check=False,
            env=env or clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                 CLAUDE_EFFORT="high"))

    def init_run(self, *extra, env=None):
        proc = self.cli("init-run", "--repo", self.repo,
                        "--brief", self.brief, *extra, env=env)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        run_dir = [l.strip() for l in proc.stdout.decode().splitlines()
                   if "audit-output/audit-council/" in l][0]
        return run_dir

    def freeze_contract(self, run_dir):
        head = git(self.repo, "rev-parse", "HEAD").strip()
        with open(os.path.join(run_dir, "state.json")) as fh:
            fp = json.load(fh)["repo_fingerprint_sha256"]
        doc = contract()
        doc["target_repository"] = {"root": self.repo, "head_sha": head,
                                    "branch": "main",
                                    "fingerprint_sha256": fp,
                                    "dirty": False}
        proc = self.cli("freeze-contract", "--run", run_dir,
                        "--contract", "-", "--stdin",
                        stdin=json.dumps(doc).encode())
        assert proc.returncode == 0, proc.stdout + proc.stderr

    def state(self, run_dir):
        with open(os.path.join(run_dir, "state.json")) as fh:
            return json.load(fh)


class TestPreflightGate(CliBase):
    def test_clean_environment_passes_with_audit_default(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout)
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["claude_selection"]["model"], "claude-opus-5-5")
        self.assertEqual(doc["claude_selection"]["effort"], "high")
        self.assertEqual(doc["claude_selection"]["mode"], "audit-default")

    def test_ambient_redirect_fails_closed(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex",
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT="high",
                                      ANTHROPIC_MODEL="glm-5.3[1m]"))
        self.assertEqual(proc.returncode, 1)
        doc = json.loads(proc.stdout)
        self.assertFalse(doc["ok"])
        checks = {f["check"] for f in doc["failures"]}
        self.assertIn("claude-model-environment", checks)
        # names only — the ambient VALUE never appears in the output
        self.assertNotIn("glm-5.3[1m]", proc.stdout.decode())

    def test_ambient_effort_mismatch_fails_closed(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex",
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT="high",
                                      CLAUDE_CODE_EFFORT_LEVEL="max"))
        self.assertEqual(proc.returncode, 1)
        checks = {f["check"] for f in json.loads(proc.stdout)["failures"]}
        self.assertIn("claude-model-environment", checks)

    def test_matching_ambient_passes(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex",
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT="high",
                                      ANTHROPIC_MODEL="claude-opus-5-5",
                                      CLAUDE_CODE_EFFORT_LEVEL="high"))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_explicit_legacy_selection_resolves(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex",
                        "--claude-model", "claude-opus-5",
                        "--claude-effort", "high")
        doc = json.loads(proc.stdout)
        self.assertEqual(doc["claude_selection"]["model"], "claude-opus-5")
        self.assertEqual(doc["claude_selection"]["mode"], "explicit")

    def test_unsupported_explicit_selection_fails_closed(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex",
                        "--claude-model", "claude-opus-4",
                        "--claude-effort", "high")
        self.assertEqual(proc.returncode, 1)
        checks = {f["check"] for f in json.loads(proc.stdout)["failures"]}
        self.assertIn("claude-model-selection", checks)

    def test_inherit_without_effort_source_fails_closed(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex",
                        "--inherit-claude-model",
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      ANTHROPIC_MODEL="claude-opus-5-5"))
        self.assertEqual(proc.returncode, 1)
        checks = {f["check"] for f in json.loads(proc.stdout)["failures"]}
        self.assertIn("claude-model-selection", checks)


class TestInitRunFreeze(CliBase):
    def test_init_freezes_audit_default_opus_selection(self):
        run_dir = self.init_run()
        frozen = self.state(run_dir)["model_selection"]["opus"]
        self.assertEqual(frozen["auditor"], "opus")
        self.assertEqual(frozen["mode"], "audit-default")
        self.assertEqual((frozen["model"], frozen["effort"]),
                         ("claude-opus-5-5", "high"))
        self.assertRegex(frozen["selection_digest"], "^[0-9a-f]{64}$")
        self.assertEqual(model_selection.selection_digest(frozen),
                         frozen["selection_digest"])
        # resume-check passes in the clean environment
        proc = self.cli("resume-check", "--run", run_dir)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_init_explicit_selection_frozen(self):
        run_dir = self.init_run("--claude-model", "claude-opus-5",
                                "--claude-effort", "low",
                                env=clean_env(
                                    AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                    CLAUDE_EFFORT="low"))
        frozen = self.state(run_dir)["model_selection"]["opus"]
        self.assertEqual(frozen["mode"], "explicit")
        self.assertEqual((frozen["model"], frozen["effort"]),
                         ("claude-opus-5", "low"))

    def test_init_ambient_conflict_refuses_before_creation(self):
        before = os.listdir(os.path.join(self.repo, "audit-output")) \
            if os.path.isdir(os.path.join(self.repo, "audit-output")) else []
        proc = self.cli("init-run", "--repo", self.repo, "--brief", self.brief,
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      ANTHROPIC_MODEL="glm-5.3[1m]"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("AMBIENT_CONFLICT", proc.stdout.decode())
        after = os.listdir(os.path.join(self.repo, "audit-output")) \
            if os.path.isdir(os.path.join(self.repo, "audit-output")) else []
        self.assertEqual(after, before)  # zero side effects

    def test_resume_check_ambient_conflict_fails_closed(self):
        run_dir = self.init_run()
        proc = self.cli("resume-check", "--run", run_dir,
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT="high",
                                      CLAUDE_CODE_SUBAGENT_MODEL="glm-5.3[1m]"))
        self.assertEqual(proc.returncode, 10, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout)
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["stage"], "model-selection")
        self.assertIn("AMBIENT_CONFLICT", doc["error"])
        self.assertNotIn("glm-5.3[1m]", doc["error"])  # names only


class TestEffectiveEffortGate(CliBase):
    """AUCDEV024-CR-IMPL-002 at the CLI surfaces: preflight, init-run (and
    thereby prepare) and resume-check refuse inference-readiness unless the
    observable effective Claude effort equals the resolved/frozen effort —
    never a value faked from requested CLI flags, SKILL frontmatter, the
    frozen state itself or provider defaults."""

    def test_preflight_effective_high_passes(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout)
        self.assertTrue(doc["ok"])

    def test_preflight_effective_medium_fails_closed(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex",
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT="medium"))
        self.assertEqual(proc.returncode, 1)
        doc = json.loads(proc.stdout)
        self.assertFalse(doc["ok"])
        checks = {f["check"] for f in doc["failures"]}
        self.assertIn("claude-effective-effort", checks)
        reasons = " ".join(f["reason"] for f in doc["failures"])
        self.assertIn("EFFECTIVE_EFFORT_MISMATCH", reasons)
        self.assertNotIn("medium", reasons)  # observed value never printed

    def test_preflight_effective_missing_fails_closed(self):
        proc = self.cli("preflight", "--repo", self.repo,
                        "--brief", self.brief, "--skip-codex",
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT=None))
        self.assertEqual(proc.returncode, 1)
        doc = json.loads(proc.stdout)
        checks = {f["check"] for f in doc["failures"]}
        self.assertIn("claude-effective-effort", checks)
        reasons = " ".join(f["reason"] for f in doc["failures"])
        self.assertIn("EFFECTIVE_EFFORT_UNOBSERVABLE", reasons)

    def test_init_run_effective_mismatch_refuses_before_creation(self):
        out_parent = os.path.join(self.repo, "audit-output")
        before = os.listdir(out_parent) if os.path.isdir(out_parent) else []
        proc = self.cli("init-run", "--repo", self.repo, "--brief", self.brief,
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT="medium"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("MODEL_SELECTION:EFFECTIVE_EFFORT_MISMATCH",
                      proc.stdout.decode())
        after = os.listdir(out_parent) if os.path.isdir(out_parent) else []
        self.assertEqual(after, before)  # zero side effects

    def test_init_run_explicit_effort_bound_to_effective(self):
        # the gate is exact equality against the RESOLVED effort (not a
        # high-only rule): an explicit low selection runs at effective low
        run_dir = self.init_run("--claude-model", "claude-opus-5-5",
                                "--claude-effort", "low",
                                env=clean_env(
                                    AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                    CLAUDE_EFFORT="low"))
        frozen = self.state(run_dir)["model_selection"]["opus"]
        self.assertEqual((frozen["model"], frozen["effort"]),
                         ("claude-opus-5-5", "low"))

    def test_resume_check_effective_mismatch_fails_closed(self):
        run_dir = self.init_run()
        proc = self.cli("resume-check", "--run", run_dir,
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT="medium"))
        self.assertEqual(proc.returncode, 10, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout)
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["stage"], "model-selection")
        self.assertIn("EFFECTIVE_EFFORT_MISMATCH", doc["error"])
        self.assertEqual(doc["completeness_state"],
                         "INVALID_MODEL_SELECTION")

    def test_resume_frozen_legacy_high_effective_mismatch_fails_closed(self):
        run_dir = self.init_run("--claude-model", "claude-opus-5",
                                "--claude-effort", "high",
                                env=clean_env(
                                    AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                    CLAUDE_EFFORT="high"))
        frozen = self.state(run_dir)["model_selection"]["opus"]
        self.assertEqual((frozen["model"], frozen["effort"]),
                         ("claude-opus-5", "high"))
        proc = self.cli("resume-check", "--run", run_dir,
                        env=clean_env(AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                      CLAUDE_EFFORT="medium"))
        self.assertEqual(proc.returncode, 10, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout)
        self.assertFalse(doc["ok"])
        self.assertIn("EFFECTIVE_EFFORT_MISMATCH", doc["error"])
        # the frozen legacy identity is never migrated by the failure
        frozen_after = self.state(run_dir)["model_selection"]["opus"]
        self.assertEqual((frozen_after["model"], frozen_after["effort"]),
                         ("claude-opus-5", "high"))


class TestResumeWithoutFrozenSelection(CliBase):
    """AUCDEV024-CR-IMPL-003: a run that can resume inference MUST carry
    its frozen Auditor-A selection — an old resumable run without frozen
    model/effort provenance FAILS CLOSED (never guessed, never silently
    migrated). Schema compatibility for historical state files and
    operational resume permission are separate concerns."""

    def _strip_model_selection(self, run_dir):
        with open(os.path.join(run_dir, "state.json")) as fh:
            state = json.load(fh)
        state.pop("model_selection", None)
        with open(os.path.join(run_dir, "state.json"), "w") as fh:
            json.dump(state, fh)

    def test_resumable_state_without_frozen_opus_fails_closed(self):
        run_dir = self.init_run()
        self._strip_model_selection(run_dir)
        proc = self.cli("resume-check", "--run", run_dir)
        self.assertEqual(proc.returncode, 10, proc.stdout + proc.stderr)
        doc = json.loads(proc.stdout)
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["stage"], "model-selection")
        self.assertIn("MODEL_SELECTION:RESUME_WITHOUT_FROZEN_SELECTION",
                      doc["error"])
        self.assertEqual(doc["completeness_state"],
                         "INVALID_MODEL_SELECTION")
        # nothing was rewritten: the state stays exactly as history left it
        with open(os.path.join(run_dir, "state.json")) as fh:
            self.assertNotIn("model_selection", fh.read())

    def test_historical_state_without_model_selection_remains_schema_valid(self):
        import validate_artifact
        run_dir = self.init_run()
        self._strip_model_selection(run_dir)
        errors = validate_artifact.validate_file(
            os.path.join(run_dir, "state.json"),
            str(SKILL_DIR / "schemas" / "state.schema.json"))
        self.assertEqual(errors, [])  # historical artifact, still valid

    def test_terminal_complete_state_without_frozen_selection_not_gated(self):
        # a COMPLETE run cannot resume inference: the fail-closed gate must
        # not fire (other completeness problems are a separate concern)
        import state_store
        run_dir = self.init_run()
        with open(os.path.join(run_dir, "state.json")) as fh:
            state = json.load(fh)
        state.pop("model_selection", None)
        state["phase"] = "COMPLETE"
        state_store.save_state(run_dir, state)  # ledger kept consistent
        proc = self.cli("resume-check", "--run", run_dir)
        self.assertNotEqual(proc.returncode, 10, proc.stdout + proc.stderr)
        self.assertNotIn("RESUME_WITHOUT_FROZEN_SELECTION",
                         proc.stdout.decode())

    def test_frozen_legacy_opus_run_resumes_exactly_as_frozen(self):
        run_dir = self.init_run("--claude-model", "claude-opus-5",
                                "--claude-effort", "high",
                                env=clean_env(
                                    AUDIT_COUNCIL_CACHE_HOME=self.cache,
                                    CLAUDE_EFFORT="high"))
        proc = self.cli("resume-check", "--run", run_dir)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        frozen = self.state(run_dir)["model_selection"]["opus"]
        # resumed exactly as frozen — no generation migration ever
        self.assertEqual((frozen["model"], frozen["effort"]),
                         ("claude-opus-5", "high"))


class TestArtifactIdentityGate(CliBase):
    def opus_audit(self, run_dir, model):
        with open(os.path.join(run_dir, "state.json")) as fh:
            fp = json.load(fh)["repo_fingerprint_sha256"]
        doc = independent_audit(model=model)
        doc["repository_fingerprint_sha256"] = fp
        return self.cli("advance", "--run", run_dir,
                        "--to", "OPUS_INDEPENDENT_COMPLETE",
                        "--artifact", "-", "--stdin",
                        stdin=json.dumps(doc).encode())

    def test_artifact_claiming_other_generation_rejected(self):
        run_dir = self.init_run()  # freezes claude-opus-5-5/high
        self.freeze_contract(run_dir)
        proc = self.opus_audit(run_dir, model="claude-opus-5")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("run-frozen opus selection", proc.stdout.decode())

    def test_artifact_claiming_frozen_identity_accepted(self):
        run_dir = self.init_run()
        self.freeze_contract(run_dir)
        proc = self.opus_audit(run_dir, model="claude-opus-5-5")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_legacy_run_without_frozen_selection_is_inert(self):
        # a run predating AUCDEV-024 has no frozen selection: the identity
        # gate must NOT fire (legacy identities are valid historical values)
        run_dir = self.init_run()
        state = self.state(run_dir)
        state.pop("model_selection", None)
        with open(os.path.join(run_dir, "state.json"), "w") as fh:
            json.dump(state, fh)
        self.freeze_contract(run_dir)
        proc = self.opus_audit(run_dir, model="claude-opus-5")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


class TestPublicContractAgreement(unittest.TestCase):
    """K: runtime policy constants, machine contract, schema and docs agree."""

    def setUp(self):
        import audit_council
        self.doc = audit_council.PUBLIC_CONTRACT
        self.md = (SKILL_DIR / "PUBLIC-CONTRACT.md").read_text()

    def test_model_roles_mirror_audit_defaults(self):
        self.assertEqual(self.doc["model_roles"]["opus"]["model"],
                         model_selection.DEFAULT_MODEL["opus"])
        self.assertEqual(self.doc["model_roles"]["opus"]["effort"],
                         model_selection.DEFAULT_EFFORT["opus"])
        self.assertEqual(self.doc["model_roles"]["codex"]["model"],
                         model_selection.DEFAULT_MODEL["codex"])
        self.assertEqual(self.doc["model_roles"]["codex"]["reasoning_effort"],
                         model_selection.DEFAULT_EFFORT["codex"])

    def test_model_selection_section_mirrors_policy_module(self):
        section = self.doc["model_selection"]
        self.assertEqual(section["modes"], list(model_selection.MODES))
        self.assertEqual(section["precedence"],
                         "explicit > explicitly requested inherit > "
                         "audit-default")
        self.assertTrue(section["no_silent_fallback"])
        self.assertEqual(section["supported_models"]["opus"],
                         list(model_selection.SUPPORTED_MODELS["opus"]))
        self.assertEqual(section["supported_models"]["codex"],
                         list(model_selection.SUPPORTED_MODELS["codex"]))
        self.assertEqual(section["supported_efforts"]["opus"],
                         list(model_selection.SUPPORTED_EFFORTS["opus"]))
        self.assertEqual(section["supported_efforts"]["codex"],
                         list(model_selection.SUPPORTED_EFFORTS["codex"]))

    def test_human_contract_mirrors_machine_contract(self):
        for needle in ("claude-opus-5-5", "gpt-6.1-sol",
                       "explicit > explicitly requested inherit > "
                       "audit-default", "MODEL_MISMATCH",
                       "never relabelled"):
            self.assertIn(needle, self.md)
        # legacy identities remain documented as historical values
        self.assertIn("claude-opus-5", self.md)
        self.assertIn("gpt-5.6-sol", self.md)

    def test_skill_frontmatter_pins_new_model(self):
        fm = (SKILL_DIR / "SKILL.md").read_text().split("---", 2)[1]
        self.assertIn("model: claude-opus-5-5", fm)


if __name__ == "__main__":
    unittest.main()
