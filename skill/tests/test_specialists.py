#!/usr/bin/env python3
"""Tests for PKG-SPEC (pillar C) — eval-gated domain specialists, DEFAULT OFF.

Task C.1: registry, pre-frozen activation gating (timestamp ordering,
reason-grounding proxy, model-found rejection, caps mirroring budgets),
independence-barrier start gate, blind context construction (scrubbing),
budget turn integration, the specialist-review output schema (SPECIALIST
attribution on candidate findings, no verdict field), and the neutral
prompt template. All tests deterministic: no model calls, no writes.
"""
from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "scripts"
SCHEMAS = TESTS.parent / "schemas"
PROMPTS = TESTS.parent / "prompts"
sys.path.insert(0, str(SCRIPTS))

import budgets  # noqa: E402
import specialists  # noqa: E402
from specialists import (DOMAINS, SpecialistError, activation_gate,  # noqa: E402
                         blind_context, budget_turn_check, registry,
                         scrub_findings, start_gate)
from validate_artifact import validate  # noqa: E402

# Fixed ISO timestamps: strictly-early, the barrier itself, strictly-late.
EARLY = "2026-09-04T09:00:00Z"
BARRIER = "2026-09-04T10:00:00Z"
LATE = "2026-09-04T11:00:00Z"

RISK_REASON = ("risk: cross-tenant data exposure in scope per contract "
               "scope[1]")
MODEL_FOUND_REASON = ("opus already found the auth bug; scope re-check "
                      "requested per contract scope[1]")

SCRUB_KEYS = {"findings", "late_findings", "challenges", "verdicts",
              "challenges_summary", "provenance"}

SCHEMA_PATH = SCHEMAS / "specialist-review.schema.json"
PROMPT_PATH = PROMPTS / "specialist-domain-review.md"
DECLARED_PLACEHOLDERS = {"contract", "repo_facts", "domain_charter",
                         "evidence_refs"}


def make_state(entries: list[dict], elevated: bool = False) -> dict:
    specialists_block: dict = {"activation": entries}
    if elevated:
        specialists_block["operator_elevated"] = True
    return {"specialists": specialists_block}


def entry(domain: str, reason: str = RISK_REASON,
          recorded_at: str = EARLY) -> dict:
    return {"domain": domain, "reason": reason, "recorded_at": recorded_at}


CONTRACT = {
    "schema_version": 2,
    "scope": ["authentication", "tenant isolation", "session handling"],
    "objective": "verify auth enforcement matches the declared contract",
    "exclusions": ["style", "docs prose"],
    "authoritative_sources": [{"id": "REQ-1", "statement": "tokens signed"}],
}


def all_keys(node) -> set:
    keys: set = set()
    if isinstance(node, dict):
        for key, value in node.items():
            keys.add(key)
            keys |= all_keys(value)
    elif isinstance(node, list):
        for item in node:
            keys |= all_keys(item)
    return keys


class RegistryTests(unittest.TestCase):
    def test_registry_nine_domains_all_default_off(self):
        reg = registry()
        self.assertEqual(len(reg), 9)
        self.assertEqual([r["domain"] for r in reg], DOMAINS)
        for item in reg:
            self.assertEqual(set(item),
                             {"domain", "charter", "default_off",
                              "eval_gated"})
            self.assertIs(item["default_off"], True)
            self.assertIs(item["eval_gated"], True)
            self.assertIsInstance(item["charter"], str)
            self.assertGreaterEqual(len(item["charter"]), 20)
            self.assertNotIn("\n", item["charter"])  # one-line charters

    def test_domains_match_architecture_section_3_4_7(self):
        self.assertEqual(DOMAINS, [
            "security-trust", "concurrency-state",
            "authorization-multitenancy", "data-integrity-migrations",
            "api-contracts", "release-supply-chain", "test-eval-quality",
            "performance-resources", "frontend-accessibility"])


class ActivationGateTests(unittest.TestCase):
    def test_no_prefrozen_reason_rejected(self):
        state = make_state([])  # nothing on record
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(state, CONTRACT, ["security-trust"], BARRIER)
        self.assertEqual(ctx.exception.rejected, ["security-trust"])
        self.assertEqual(ctx.exception.approved, [])

    def test_reason_recorded_after_first_pass_rejected(self):
        state = make_state([entry("security-trust", recorded_at=LATE)])
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(state, CONTRACT, ["security-trust"], BARRIER)
        self.assertIn("security-trust", ctx.exception.rejected)
        self.assertIn("pre-frozen", str(ctx.exception))

    def test_reason_recorded_exactly_at_barrier_rejected(self):
        # equal is NOT before — strict ordering required
        state = make_state([entry("security-trust", recorded_at=BARRIER)])
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(state, CONTRACT, ["security-trust"], BARRIER)
        self.assertIn("security-trust", ctx.exception.rejected)

    def test_reason_recorded_strictly_before_approved(self):
        state = make_state([entry("security-trust", recorded_at=EARLY)])
        self.assertEqual(
            activation_gate(state, CONTRACT, ["security-trust"], BARRIER),
            ["security-trust"])

    def test_none_barrier_accepts_any_recording_time(self):
        # pre-freezing before the barrier exists is legal at any time
        for when in (EARLY, BARRIER, LATE):
            state = make_state([entry("security-trust", recorded_at=when)])
            self.assertEqual(
                activation_gate(state, CONTRACT, ["security-trust"], None),
                ["security-trust"])

    def test_model_found_reason_rejected_regardless_of_timing(self):
        for when in (EARLY, LATE):
            state = make_state(
                [entry("security-trust", reason=MODEL_FOUND_REASON,
                       recorded_at=when)])
            with self.assertRaises(SpecialistError) as ctx:
                activation_gate(state, CONTRACT, ["security-trust"], BARRIER)
            self.assertIn("security-trust", ctx.exception.rejected)
            self.assertIn("primary model", str(ctx.exception))

    def test_model_found_variants_rejected(self):
        for reason in ("codex revealed the race in the worker pool per "
                       "contract scope[0]",
                       "the auditor reported drift already, objective "
                       "recheck wanted",
                       "Model found the bug already; scope recheck per "
                       "exclusions[0]"):
            state = make_state(
                [entry("concurrency-state", reason=reason)])
            with self.assertRaises(SpecialistError):
                activation_gate(state, CONTRACT, ["concurrency-state"],
                                BARRIER)

    def test_short_generic_reason_rejected(self):
        state = make_state([entry("security-trust", reason="just in case")])
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(state, CONTRACT, ["security-trust"], BARRIER)
        self.assertIn("security-trust", ctx.exception.rejected)
        self.assertIn("short", str(ctx.exception))

    def test_long_but_ungrounded_reason_rejected(self):
        reason = "a second pair of eyes generally improves audit outcomes"
        self.assertGreaterEqual(len(reason), 40)
        state = make_state([entry("security-trust", reason=reason)])
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(state, CONTRACT, ["security-trust"], BARRIER)
        self.assertIn("grounded", str(ctx.exception))

    def test_risk_reason_with_early_timestamp_approved(self):
        state = make_state(
            [entry("authorization-multitenancy", reason=RISK_REASON)])
        self.assertEqual(
            activation_gate(state, CONTRACT,
                            ["authorization-multitenancy"], BARRIER),
            ["authorization-multitenancy"])

    def test_normal_cap_two_without_elevation(self):
        two = make_state([entry("security-trust"),
                          entry("concurrency-state")])
        self.assertEqual(
            activation_gate(two, CONTRACT,
                            ["security-trust", "concurrency-state"], BARRIER),
            ["security-trust", "concurrency-state"])

        three = make_state([entry("security-trust"),
                            entry("concurrency-state"),
                            entry("api-contracts")])
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(three, CONTRACT,
                            ["security-trust", "concurrency-state",
                             "api-contracts"], BARRIER)
        self.assertIn("normal cap", str(ctx.exception))
        self.assertEqual(len(ctx.exception.approved), 3)  # would-be subset

    def test_elevation_honored_three_approved(self):
        state = make_state([entry("security-trust"),
                            entry("concurrency-state"),
                            entry("api-contracts")], elevated=True)
        self.assertEqual(
            activation_gate(state, CONTRACT,
                            ["security-trust", "concurrency-state",
                             "api-contracts"], BARRIER),
            ["security-trust", "concurrency-state", "api-contracts"])

    def test_hard_cap_three_enforced_even_with_elevation(self):
        state = make_state([entry("security-trust"),
                            entry("concurrency-state"),
                            entry("api-contracts"),
                            entry("release-supply-chain")], elevated=True)
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(state, CONTRACT,
                            ["security-trust", "concurrency-state",
                             "api-contracts", "release-supply-chain"],
                            BARRIER)
        self.assertIn("hard cap", str(ctx.exception))

    def test_unknown_domain_rejected(self):
        state = make_state([entry("security-trust")])
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(state, CONTRACT, ["nostalgia-romanticism"],
                            BARRIER)
        self.assertIn("nostalgia-romanticism", ctx.exception.rejected)
        self.assertIn("unknown", str(ctx.exception))

    def test_rejected_and_approved_carried_on_error(self):
        state = make_state([entry("security-trust"),
                            entry("concurrency-state")])
        with self.assertRaises(SpecialistError) as ctx:
            activation_gate(state, CONTRACT,
                            ["security-trust", "concurrency-state",
                             "frontend-accessibility"], BARRIER)
        self.assertEqual(ctx.exception.rejected, ["frontend-accessibility"])
        self.assertEqual(ctx.exception.approved,
                         ["security-trust", "concurrency-state"])


class StartGateTests(unittest.TestCase):
    def test_start_gate_closed_raises(self):
        with self.assertRaises(SpecialistError) as ctx:
            start_gate(False)
        self.assertEqual(str(ctx.exception),
                         "specialists run only after the independence barrier")

    def test_start_gate_open_ok(self):
        start_gate(True)  # must not raise


class BlindContextTests(unittest.TestCase):
    def test_scrubs_primary_model_output_keys_deep(self):
        dirty_contract = copy.deepcopy(CONTRACT)
        dirty_contract["findings"] = [
            {"id": "OPUS-001", "severity": "HIGH", "claim": "leak"}]
        dirty_contract["auditor_notes"] = {
            "late_findings": [{"id": "OPUS-009"}],
            "challenges": [{"id": "X-001"}],
            "verdicts": ["CONFIRMED"],
            "challenges_summary": "opus was right",
            "provenance": {"discovered_by": "OPUS"},
            "keep": "neutral material",
        }
        dirty_facts = {
            "root": "/repo", "head": "0" * 40,
            "files": [{"path": "a.py",
                       "findings": [{"claim": "cross-contamination"}]}],
        }
        ctx = blind_context(dirty_contract, dirty_facts, "security-trust",
                            ["ev-" + "0" * 16])
        self.assertEqual(all_keys(ctx) & SCRUB_KEYS, set())  # deep check
        self.assertEqual(ctx["domain"], "security-trust")
        self.assertEqual(ctx["domain_charter"],
                         registry()[0]["charter"])
        self.assertEqual(ctx["evidence_refs"], ["ev-" + "0" * 16])
        # neutral material survives the scrub
        self.assertEqual(ctx["contract"]["scope"], CONTRACT["scope"])
        self.assertEqual(ctx["contract"]["auditor_notes"]["keep"],
                         "neutral material")
        self.assertEqual(ctx["repo_facts"]["root"], "/repo")

    def test_non_ev_evidence_ref_refused(self):
        with self.assertRaises(SpecialistError):
            blind_context(CONTRACT, {"root": "/repo"}, "security-trust",
                          ["doc-123"])
        with self.assertRaises(SpecialistError):
            blind_context(CONTRACT, {"root": "/repo"}, "security-trust",
                          ["ev-ok", "raw-path"])

    def test_unknown_domain_refused(self):
        with self.assertRaises(SpecialistError):
            blind_context(CONTRACT, {"root": "/repo"}, "not-a-domain", [])

    def test_input_not_mutated(self):
        dirty = copy.deepcopy(CONTRACT)
        dirty["findings"] = [{"id": "OPUS-001"}]
        snapshot = copy.deepcopy(dirty)
        blind_context(dirty, {"root": "/repo"}, "api-contracts", [])
        self.assertEqual(dirty, snapshot)

    def test_scrub_findings_direct(self):
        obj = {"keep": 1, "findings": [1],
               "nested": [{"provenance": {"a": 1}, "keep2": [2,
                                                             {"verdicts": []}]}],
               "late_findings": None}
        self.assertEqual(scrub_findings(obj),
                         {"keep": 1, "nested": [{"keep2": [2, {}]}]})
        self.assertEqual(obj["findings"], [1])  # original untouched


class BudgetTurnCheckTests(unittest.TestCase):
    def test_zero_and_one_turns_ok_under_default_budget(self):
        self.assertEqual(
            budgets.DEFAULT_BUDGETS["max_specialist_turns"], 2)
        state = make_state([entry("security-trust")])
        budget_turn_check(state, 0)
        budget_turn_check(state, 1)

    def test_two_turns_raises(self):
        state = make_state([entry("security-trust")])
        with self.assertRaises(budgets.BudgetExceeded):
            budget_turn_check(state, 2)

    def test_unactivated_state_raises(self):
        for state in (make_state([]), {"specialists": {}}, {}):
            with self.assertRaises(budgets.BudgetExceeded):
                budget_turn_check(state, 1)


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    @staticmethod
    def candidate(discovered_by: str) -> dict:
        # id/origin intentionally keep the shared finding-id shape: they are
        # provisional placeholders re-assigned at H-phase normalization (the
        # schema documents this); discovered_by carries the attribution.
        return {
            "id": "OPUS-001",
            "origin": "OPUS-001",
            "title": "Unsigned session cookie accepted by auth middleware",
            "category": "security",
            "severity": "HIGH",
            "confidence": "MEDIUM",
            "claim": "verify_session accepts cookies without a signature "
                     "check",
            "status": "PROVISIONAL",
            "evidence": [{"kind": "OBSERVED_FACT", "path": "src/auth.py",
                          "symbol": "verify_session",
                          "line_ranges": [{"start": 40, "end": 52}],
                          "description": "no signature verification call"}],
            "counter_evidence": [],
            "provenance": {"discovered_by": discovered_by},
        }

    @classmethod
    def review(cls, discovered_by="SPECIALIST-security-trust") -> dict:
        return {
            "schema_version": 2,
            "domain": "security-trust",
            "reviewer": "SPECIALIST-security-trust",
            "coverage": [{"area": "session token verification",
                          "covered": True,
                          "note": "inspected middleware paths"}],
            "candidate_findings": [cls.candidate(discovered_by)],
            "negative_evidence": [{"kind": "SEARCH_RESULT",
                                   "description": "no secrets logged in "
                                                  "scope"}],
            "unresolved_questions": ["rotation enforced cluster-wide?"],
            "evidence_refs": ["ev-0123456789abcdef"],
            "notes": "blind pass; no other auditor output consulted",
        }

    def _errors(self, doc):
        return validate(doc, self.schema, base_dir=SCHEMAS)

    def test_full_valid_instance_validates(self):
        self.assertEqual(self._errors(self.review()), [])

    def test_candidate_discovered_by_opus_fails_pattern(self):
        errors = self._errors(self.review(discovered_by="OPUS"))
        self.assertTrue(errors)
        self.assertTrue(any("pattern" in e or "OPUS" in e
                            for e in errors), errors)

    def test_candidate_discovered_by_specialist_passes(self):
        doc = self.review(discovered_by="SPECIALIST-security-trust")
        self.assertEqual(self._errors(doc), [])
        doc2 = self.review(discovered_by="SPECIALIST-authorization-"
                                          "multitenancy")
        self.assertEqual(self._errors(doc2), [])

    def test_schema_domain_enum_matches_domains(self):
        enum = self.schema["properties"]["domain"]["enum"]
        self.assertEqual(enum, DOMAINS)

    def test_schema_has_no_verdict_field(self):
        top = self.schema["properties"]
        self.assertNotIn("verdict", top)
        self.assertNotIn("verdict", top["candidate_findings"]["items"]
                         ["properties"])
        self.assertNotIn("go_no_go", top)


class PromptTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PROMPT_PATH.read_text(encoding="utf-8")
        cls.tokens = set(re.findall(r"\{\{([a-zA-Z_]+)\}\}", cls.text))

    def test_placeholders_exactly_the_four_declared(self):
        self.assertEqual(self.tokens, DECLARED_PLACEHOLDERS)
        # no primary-findings-style placeholder of any shape
        for banned in ("opus_findings", "codex_findings", "findings",
                       "primary_findings", "verdicts", "challenges"):
            self.assertNotIn(banned, self.tokens)

    def test_prompt_declares_blindness(self):
        lowered = self.text.lower()
        self.assertIn("no other auditor's findings", lowered)

    def test_prompt_forbids_verdict_ownership(self):
        lowered = self.text.lower()
        self.assertIn("you do not issue verdicts", lowered)
        self.assertIn("go/no-go", lowered)

    def test_prompt_mandates_output_schema(self):
        self.assertIn("specialist-review.schema.json", self.text)


if __name__ == "__main__":
    unittest.main()
