#!/usr/bin/env python3
"""PKG-PUB — public audit contract tests (pillar F).

`audit_council.py describe --json` is the machine-readable source of truth
(module-level PUBLIC_CONTRACT); PUBLIC-CONTRACT.md mirrors it for humans.
These tests pin the contract's shape (schema), its protocol version, the
mirror for enum/list facts, drift against the real schema/budget constants,
the absence of internal module names on the public surface, and one
regression smoke proving the rest of the CLI is untouched.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PYTHON = "python3"  # NOT sys.executable (may be an embedded app host)

TESTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TESTS_DIR.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
SCHEMAS_DIR = SKILL_DIR / "schemas"
AUDIT_COUNCIL = str(SCRIPTS_DIR / "audit_council.py")
MD_PATH = SKILL_DIR / "PUBLIC-CONTRACT.md"
PUBLIC_SCHEMA = SCHEMAS_DIR / "public-contract.schema.json"
STATE_SCHEMA = SCHEMAS_DIR / "state.schema.json"

sys.path.insert(0, str(SCRIPTS_DIR))

import budgets  # noqa: E402
import validate_artifact  # noqa: E402

# ARCHITECTURE §3.4.2 (frozen taxonomy — exactly nine reasons)
EXPECTED_FAILURE_TAXONOMY = (
    "BRIEF_ROOT_MISMATCH", "BRIEF_HEAD_MISMATCH", "WORKTREE_IDENTITY_CHANGED",
    "CWD_OUTSIDE_FROZEN_ROOT", "PATH_ESCAPE_ATTEMPT",
    "ALTERNATE_WORKTREE_ACCESS", "UNAUTHORIZED_TMP_ACCESS",
    "REPO_ROOT_REPLACED", "SYMLINK_ESCAPE",
)

REQUIRED_CANONICAL_ARTIFACTS = (
    "02-audit-contract.json",
    "10-opus-independent.json",
    "20-codex-independent.json",
    "90-final-findings.json",
    "99-run-metrics.json",
)

BANNED_INTERNAL_MODULES = ("codex_runner.py", "wire_adapter.py",
                           "state_store.py")


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PYTHON, AUDIT_COUNCIL, *args],
                          capture_output=True, check=False)


class PublicContractBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = run_cli("describe", "--json")
        cls.doc = json.loads(cls.proc.stdout.decode("utf-8"))
        cls.md = MD_PATH.read_text(encoding="utf-8")


class TestDescribeJson(PublicContractBase):
    def test_exits_zero_and_prints_pretty_json(self):
        self.assertEqual(self.proc.returncode, 0)
        text = self.proc.stdout.decode("utf-8")
        self.assertTrue(text.startswith("{\n"))
        self.assertIn('\n  "protocol_version"', text)  # indent=2 pretty JSON

    def test_doc_validates_against_public_contract_schema(self):
        schema = json.loads(PUBLIC_SCHEMA.read_text(encoding="utf-8"))
        errors = validate_artifact.validate(self.doc, schema,
                                            base_dir=SCHEMAS_DIR)
        self.assertEqual(errors, [])

    def test_default_mode_points_at_the_human_mirror(self):
        proc = run_cli("describe")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(b"PUBLIC-CONTRACT.md", proc.stdout)


class TestProtocolVersion(PublicContractBase):
    def test_version_is_2_0_and_appears_in_public_contract_md(self):
        self.assertEqual(self.doc["protocol_version"], "2.0")
        self.assertIn("2.0", self.md)


class TestDriftAgainstSources(PublicContractBase):
    def test_completeness_states_equal_state_schema_enum(self):
        schema = json.loads(STATE_SCHEMA.read_text(encoding="utf-8"))
        enum = schema["properties"]["completeness_state"]["enum"]
        self.assertEqual(sorted(self.doc["completeness_states"]),
                         sorted(enum))

    def test_every_completeness_state_appears_in_md(self):
        for state in self.doc["completeness_states"]:
            self.assertIn(state, self.md)

    def test_governor_constraints_mirror_default_budgets(self):
        gc = self.doc["governor_constraints"]
        for key, value in budgets.DEFAULT_BUDGETS.items():
            self.assertIn(key, gc, f"budget {key!r} missing from contract")
            self.assertEqual(gc[key], value)
        # exactly the budget keys plus the documented omissions statement
        self.assertEqual(set(gc) - set(budgets.DEFAULT_BUDGETS),
                         {"omissions"})
        self.assertTrue(gc["omissions"])

    def test_failure_taxonomy_exactly_the_nine_reasons(self):
        taxonomy = self.doc["environment_integrity"]["failure_taxonomy"]
        self.assertEqual(len(taxonomy), 9)
        self.assertEqual(sorted(taxonomy), sorted(EXPECTED_FAILURE_TAXONOMY))

    def test_canonical_artifacts_include_required(self):
        artifacts = self.doc["artifact_semantics"]["canonical_artifacts"]
        for name in REQUIRED_CANONICAL_ARTIFACTS:
            self.assertIn(name, artifacts)


class TestPublicSurface(PublicContractBase):
    def test_no_internal_module_references(self):
        payload = json.dumps(self.doc, ensure_ascii=False)
        for banned in BANNED_INTERNAL_MODULES:
            self.assertNotIn(banned, payload)
            self.assertNotIn(banned, self.md)

    def test_compatibility_policy_present(self):
        policy = self.doc["compatibility_policy"]
        self.assertTrue(policy.strip())
        self.assertIn("additive", policy)
        self.assertIn("major", policy)
        self.assertIn("## Compatibility policy", self.md)
        self.assertIn("Additive changes keep protocol 2.x", self.md)

    def test_evidence_model_documented_with_both_example_ranges(self):
        evidence_model = self.doc["artifact_semantics"]["evidence_model"]
        self.assertIn("line_ranges", evidence_model)
        self.assertIn("line_ranges", self.md)
        for number in ("184", "185", "240", "273"):
            self.assertIn(number, self.md)

    def test_environment_modes_documented_in_md(self):
        modes = self.doc["environment_modes"]
        self.assertEqual(sorted(modes),
                         sorted(["AUTO", "CURRENT", "RELEASE", "HISTORICAL"]))
        for mode in modes:
            self.assertIn(mode, self.md)


class TestUntouchedRegression(unittest.TestCase):
    def test_preflight_missing_brief_still_fails(self):
        """Sanity smoke: the preflight path is byte-for-byte untouched by
        the describe addition — a missing brief still fails the same way."""
        with tempfile.TemporaryDirectory(prefix="pub-preflight-") as tmp:
            proc = run_cli("preflight", "--repo", tmp,
                           "--brief", os.path.join(tmp, "missing-brief.md"),
                           "--skip-codex")
        self.assertEqual(proc.returncode, 1)
        out = json.loads(proc.stdout.decode("utf-8"))
        self.assertFalse(out["ok"])
        self.assertIn("brief-exists",
                      {f["check"] for f in out["failures"]})


if __name__ == "__main__":
    unittest.main()


class TestSkillScopedHooksAndConfinementClaims(unittest.TestCase):
    """Release-qualification: skill-scoped AUTOMATIC PreToolUse hooks and
    honest enforcement taxonomy (no 'session-opt-in' overclaim, no
    'runner-enforced read confinement' overclaim)."""

    SKILL_MD = Path(__file__).resolve().parent.parent / "SKILL.md"

    def test_frontmatter_declares_pretooluse_hook(self):
        text = self.SKILL_MD.read_text()
        fm = text.split("---", 2)[1]
        self.assertIn("hooks:", fm)
        self.assertIn("PreToolUse:", fm)
        self.assertIn('matcher: "Bash|Read|Grep|Glob"', fm)
        self.assertIn("type: command", fm)
        self.assertIn("path_guard_hook.py", fm)
        # the hook file exists at the referenced location
        self.assertTrue((self.SKILL_MD.parent / "hooks" /
                         "path_guard_hook.py").is_file())

    def test_contract_claude_confinement_not_opt_in(self):
        doc = json.loads(subprocess.run(
            ["python3", AUDIT_COUNCIL,
             "describe", "--json"],
            capture_output=True, text=True, check=True).stdout)
        claim = doc["runtime_capabilities"]["claude_path_confinement"]
        self.assertIn("pre-tool mechanically denied", claim)
        self.assertIn("AUTOMATICALLY", claim)
        self.assertNotIn("opt-in", claim.lower())
        self.assertNotIn("session-opt-in", claim.lower())

    def test_contract_codex_claims_use_exact_taxonomy(self):
        doc = json.loads(subprocess.run(
            ["python3", AUDIT_COUNCIL,
             "describe", "--json"],
            capture_output=True, text=True, check=True).stdout)
        caps = doc["runtime_capabilities"]
        self.assertIn("OS-enforced", caps["codex_write_confinement"])
        read_claim = caps["codex_read_confinement"]
        self.assertIn("OS-enforced EXCLUSION", read_claim)
        self.assertIn("not enforced", read_claim)  # the no-bwrap branch
        # no overclaim of blanket "runner-enforced read confinement"
        self.assertNotIn("read confinement runner-enforced", read_claim)
        lim = " ".join(doc["known_limitations"])
        self.assertNotIn("session-opt-in", lim)

    def test_public_contract_md_has_enforcement_map(self):
        md = (Path(__file__).resolve().parent.parent /
              "PUBLIC-CONTRACT.md").read_text()
        self.assertIn("Runtime enforcement map", md)
        for phrase in ("OS-enforced", "pre-tool mechanically denied",
                       "not enforced / accepted residual",
                       "runner policy/detection"):
            self.assertIn(phrase, md)
        self.assertNotIn("runner-enforced, not OS-enforced", md)
        self.assertNotIn("session-opt-in", md)
