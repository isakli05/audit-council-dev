#!/usr/bin/env python3
"""Eval framework self-tests (PKG-EVAL pillar D, Tasks D.1/D.2).

Deterministic, fast (<20 s total), zero model calls:
  * scoring semantics (hard ENVIRONMENT gate, not-run tiers, merge,
    novel-finding truth rule);
  * tier-1 matrix discovery + LIVE run of the three env regression
    modules (this doubles as the standing gate for the landed A0 work);
  * harness-suite result parsing against a real subprocess;
  * tier-2 fixture builds (sealed truth outside the repos, loader
    containment, seeded defects present, git validity);
  * tier-3 approval gate (refusal touches NOTHING on disk) + READ-ONLY
    replay of the Fifth historical run (byte/mtime preservation).
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
import unittest.mock
from pathlib import Path

PYTHON = "/usr/bin/python3"  # NEVER sys.executable (AppImage shim here)

TESTS = Path(__file__).resolve().parent
SKILL = TESTS.parent
EVAL = SKILL / "eval"
if str(SKILL) not in sys.path:
    sys.path.insert(0, str(SKILL))

from eval import scoring, tier1_harness, tier2_fixtures, tier3_replay  # noqa: E402

FIFTH_RUN_DIR = tier3_replay.TIER3_SEEDS["fifth"]["run_dir"]
VALID_APPROVAL = {"operator_approval": True, "approver": "eval-test",
                  "approved_at": "2026-09-04T00:00:00Z"}


class TestScoringSemantics(unittest.TestCase):
    DIMENSIONS = ("FINAL_QUALITY", "PROCESS", "HARNESS", "ECONOMICS",
                  "DIVERSITY", "ENVIRONMENT")

    def test_environment_below_one_not_ready_even_with_harness_pass(self):
        card = scoring.score_tier1({"case-1": True, "case-2": False},
                                   True, 422)
        self.assertEqual(card["overall"], "NOT_READY")
        self.assertFalse(card["environment_integrity_pass"])
        self.assertEqual(
            card["dimensions"]["ENVIRONMENT"]["score"], 0.5)
        self.assertEqual(
            card["dimensions"]["ENVIRONMENT"]["details"]["failing_cases"],
            ["case-2"])

    def test_environment_empty_matrix_is_not_ready(self):
        card = scoring.score_tier1({}, True, 10)
        self.assertEqual(card["overall"], "NOT_READY")
        self.assertEqual(card["dimensions"]["ENVIRONMENT"]["score"], 0.0)

    def test_environment_full_and_harness_pass_is_ready(self):
        card = scoring.score_tier1({"a": True, "b": True}, True, 422)
        self.assertEqual(card["overall"], "READY")
        self.assertTrue(card["environment_integrity_pass"])
        self.assertEqual(card["dimensions"]["ENVIRONMENT"]["score"], 1.0)
        self.assertEqual(card["dimensions"]["HARNESS"]["score"], 1.0)
        self.assertEqual(
            card["dimensions"]["HARNESS"]["details"]["tests_run"], 422)

    def test_harness_fail_forces_not_ready(self):
        card = scoring.score_tier1({"a": True}, False, 7)
        self.assertEqual(card["overall"], "NOT_READY")
        self.assertEqual(card["dimensions"]["HARNESS"]["score"], 0.0)

    def test_later_tier_dimensions_not_run_at_tier1(self):
        card = scoring.score_tier1({"a": True}, True, 3)
        for dim in ("FINAL_QUALITY", "PROCESS", "ECONOMICS", "DIVERSITY"):
            self.assertEqual(card["dimensions"][dim],
                             {"status": "not-run"}, dim)
        self.assertEqual(tuple(card["dimensions"]), self.DIMENSIONS)

    def test_merge_fills_later_dimensions_keeps_environment_hard_gate(self):
        tier1 = scoring.score_tier1({"a": True, "b": True}, True, 10)
        later = {"dimensions": {
            "FINAL_QUALITY": {"status": "scored", "score": 0.9,
                              "details": {"recall": 0.9}},
            "PROCESS": {"status": "scored", "score": 0.8, "details": {}},
            "ENVIRONMENT": {"status": "scored", "score": 1.0,
                            "details": {"failing_cases": []}}},
            "overall": "READY"}
        merged = scoring.merge_scores(tier1, later)
        self.assertEqual(merged["dimensions"]["FINAL_QUALITY"]["score"],
                         0.9)
        self.assertEqual(merged["dimensions"]["PROCESS"]["score"], 0.8)
        self.assertEqual(merged["dimensions"]["ENVIRONMENT"]["score"], 1.0)
        self.assertTrue(merged["environment_integrity_pass"])
        self.assertEqual(merged["overall"], "READY")
        # a tier that observed an environment failure poisons the merge
        broken_env = {"dimensions": {
            "ENVIRONMENT": {"status": "scored", "score": 0.5,
                            "details": {"failing_cases": ["2"]}}},
            "overall": "READY"}
        merged2 = scoring.merge_scores(tier1, later, broken_env)
        self.assertFalse(merged2["environment_integrity_pass"])
        self.assertEqual(merged2["overall"], "NOT_READY")
        self.assertIn("2", merged2["dimensions"]["ENVIRONMENT"]
                      ["details"]["failing_cases"])

    def test_novel_finding_truth_rule(self):
        # model agreement alone is NEVER truth
        self.assertFalse(scoring.novel_finding_is_truth(
            True, {"model_agreement": 2}))
        self.assertFalse(scoring.novel_finding_is_truth(
            True, {"model_agreement": 5, "consensus": True}))
        # each truth evidence flag alone suffices
        self.assertTrue(scoring.novel_finding_is_truth(
            True, {"deterministic_reproduction": True}))
        self.assertTrue(scoring.novel_finding_is_truth(
            True, {"human_confirmation": True}))
        self.assertTrue(scoring.novel_finding_is_truth(
            True, {"independent_evaluator": True}))
        self.assertTrue(scoring.novel_finding_is_truth(
            True, {"predefined_runtime_evidence": True}))
        # truthy-looking non-bools, absent evidence, unclaimed findings
        self.assertFalse(scoring.novel_finding_is_truth(
            True, {"independent_evaluator": "yes"}))
        self.assertFalse(scoring.novel_finding_is_truth(True, {}))
        self.assertFalse(scoring.novel_finding_is_truth(
            False, {"human_confirmation": True}))


class TestTier1Discovery(unittest.TestCase):
    def test_discovers_at_least_15_matrix_cases(self):
        mapping = tier1_harness.discover_env_matrix_tests()
        self.assertGreaterEqual(len(mapping), 15)
        for case, test_name in mapping.items():
            self.assertIsInstance(case, str)
            self.assertIsInstance(test_name, str)
            self.assertRegex(test_name, r"^test_env_(binding|lifecycle)\."
                                        r"\w+\.test_\w+$|^test_path_guard"
                                        r"\.\w+\.test_\w+$")
        # the numbered program-spec matrix (cases 1-20) is fully mapped
        for n in range(1, 21):
            self.assertIn(str(n), mapping,
                          "spec matrix case %d unmapped" % n)

    def test_discovery_reports_unmapped(self):
        full = tier1_harness.discover_env_matrix()
        self.assertIn("unmapped", full)
        self.assertIn("case_tests", full)
        self.assertEqual(full["unmapped"], [])  # current tree: complete

    def test_tier1_assembly_uses_injected_runners(self):
        result = tier1_harness.tier1(
            run_env_matrix_fn=lambda: {"1": True, "2": True},
            run_harness_fn=lambda: (True, 12))
        self.assertEqual(result["scorecard"]["overall"], "READY")
        self.assertEqual(result["env_matrix"]["pass_fraction"], 1.0)
        self.assertEqual(result["harness_suite"]["tests_run"], 12)


class TestTier1LiveMatrix(unittest.TestCase):
    """LIVE gate: runs the three env regression modules (~10 s)."""

    def test_run_env_matrix_all_true_on_current_tree(self):
        results = tier1_harness.run_env_matrix()
        self.assertGreaterEqual(len(results), 15)
        failing = sorted(k for k, v in results.items() if not v)
        self.assertEqual(failing, [],
                         "environment matrix regressions: %s" % failing)


class TestHarnessSuiteParsing(unittest.TestCase):
    """Parses REAL unittest subprocess output against a tiny suite."""

    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="eval-harness-")
        with open(os.path.join(self.dir, "test_tiny.py"), "w") as fh:
            fh.write("import unittest\n"
                     "class T(unittest.TestCase):\n"
                     "    def test_ok(self):\n        self.assertTrue(1)\n")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_parses_ran_and_ok(self):
        passed, total = tier1_harness.run_harness_suite(tests_dir=self.dir)
        self.assertTrue(passed)
        self.assertEqual(total, 1)

    def test_failing_suite_reports_not_passed(self):
        with open(os.path.join(self.dir, "test_bad.py"), "w") as fh:
            fh.write("import unittest\n"
                     "class B(unittest.TestCase):\n"
                     "    def test_bad(self):\n"
                     "        self.assertEqual(1, 2)\n")
        passed, total = tier1_harness.run_harness_suite(tests_dir=self.dir)
        self.assertFalse(passed)
        self.assertEqual(total, 2)


class TestTier2Fixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # disposable root via tempfile: nothing persists (no committed
        # fixture repos, no skill/eval/fixtures-out/ leftovers)
        cls.root = tempfile.mkdtemp(prefix="fixtures-out-")
        cls.summary = tier2_fixtures.build_all(cls.root)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, ignore_errors=True)

    def test_all_ten_fixtures_built_with_sealed_truth_outside_repos(self):
        self.assertEqual(
            sorted(self.summary["fixtures"]),
            sorted(tier2_fixtures.FIXTURE_NAMES))
        self.assertEqual(len(self.summary["fixtures"]), 10)
        sealed_root = self.summary["sealed_root"]
        for name, info in self.summary["fixtures"].items():
            repo = info["repo"]
            # sealed truth exists and is NOT inside the fixture repo
            sealed = os.path.join(sealed_root, name + ".json")
            self.assertTrue(os.path.isfile(sealed), sealed)
            self.assertFalse(os.path.commonpath(
                [os.path.realpath(sealed), os.path.realpath(repo)])
                == os.path.realpath(repo),
                "sealed truth leaked into fixture repo %s" % name)
            # the repo itself contains no sealed/ directory
            self.assertFalse(os.path.exists(os.path.join(repo, "sealed")))
            self.assertEqual(info["git_head"],
                             subprocess.run(
                                 ["git", "-C", repo, "rev-parse", "HEAD"],
                                 capture_output=True, text=True,
                                 check=True).stdout.strip())

    def test_fixture_repos_are_minimal(self):
        for name, info in self.summary["fixtures"].items():
            self.assertGreaterEqual(info["files"], 3, name)
            self.assertLessEqual(info["files"], 15, name)
            self.assertLess(info["lines"], 200, name)

    def test_sealed_loader_refuses_outside_sealed_root(self):
        # path-escape names are rejected outright
        for bad in ("../auth-bypass", "..", "auth-bypass/../../etc/passwd",
                    "", None, "sub/dir/name"):
            with self.assertRaises((ValueError, PermissionError),
                                   msg=repr(bad)):
                tier2_fixtures.load_ground_truth(bad, self.root)
        # a symlink planted in the sealed root must not escape it
        outside = os.path.join(self.root, "outside-secret.json")
        with open(outside, "w") as fh:
            fh.write('{"defects": [{"id": "LIE"}]}')
        evil = os.path.join(self.summary["sealed_root"], "evil.json")
        os.symlink(outside, evil)
        try:
            with self.assertRaises(PermissionError):
                tier2_fixtures.load_ground_truth("evil", self.root)
        finally:
            os.unlink(evil)
        # the legitimate load still works and carries the truth shape
        truth = tier2_fixtures.load_ground_truth("auth-bypass", self.root)
        self.assertEqual(truth["fixture"], "auth-bypass")
        self.assertEqual(truth["defects"][0]["id"], "AUTH-BYPASS-1")

    def test_auth_bypass_fixture_actually_contains_the_defect(self):
        truth = tier2_fixtures.load_ground_truth("auth-bypass", self.root)
        self.assertEqual(len(truth["defects"]), 1)
        defect = truth["defects"][0]
        path = os.path.join(self.summary["fixtures"]["auth-bypass"]["repo"],
                            defect["path"])
        with open(path) as fh:
            content = fh.read()
        # grep-level: the cited defective snippet is verbatim in the file
        self.assertIn(defect["snippet"], content)
        get_handler = content[content.index("router.get('/:id'"):]
        get_handler = get_handler[:get_handler.index("});") + 3]
        self.assertNotIn("requireOwnership", get_handler,
                         "seeded bypass repaired itself")
        # the ownership control exists and IS used by the sibling route
        self.assertIn("requireOwnership", content)
        delete_handler = content[content.index("router.delete('/:id'"):]
        self.assertIn("requireOwnership", delete_handler)

    def test_negative_controls_protected_pattern_and_no_defect(self):
        truth = tier2_fixtures.load_ground_truth("negative-controls",
                                                 self.root)
        self.assertEqual(truth["defects"], [])
        self.assertGreaterEqual(len(truth["must_not_flag"]), 4)
        repo = self.summary["fixtures"]["negative-controls"]["repo"]
        with open(os.path.join(repo, "src", "legacy.py")) as fh:
            legacy = fh.read()
        self.assertIn("hmac.compare_digest", legacy)  # protected pattern
        self.assertIn("# def legacy_check", legacy)   # dead-code pattern
        # the dead insecure line is commented out, i.e. no live defect
        for line in legacy.splitlines():
            if "token == expected" in line:
                self.assertTrue(line.lstrip().startswith("#"))

    def test_each_seeded_fixture_carries_exactly_its_defects(self):
        expected = {spec["name"]: 0 if spec["name"] == "negative-controls"
                    else 1 for spec in tier2_fixtures.FIXTURE_SPECS}
        for name, defect_count in expected.items():
            truth = tier2_fixtures.load_ground_truth(name, self.root)
            self.assertEqual(len(truth["defects"]), defect_count, name)
            for defect in truth["defects"]:
                repo = self.summary["fixtures"][name]["repo"]
                cited = os.path.join(repo, defect["path"])
                self.assertTrue(os.path.isfile(cited),
                                "%s cites missing %s" % (name, cited))
                with open(cited) as fh:
                    self.assertIn(defect["snippet"], fh.read())


def snapshot_tree(root: str) -> dict[str, tuple[int, int]]:
    snap: dict[str, tuple[int, int]] = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            st = os.stat(p)
            snap[p] = (st.st_size, st.st_mtime_ns)
    return snap


class TestTier3ApprovalGate(unittest.TestCase):
    def test_replay_without_approval_refuses_and_never_touches_disk(self):
        calls = []
        real_exists = os.path.exists

        def counting_exists(path, *a, **kw):
            if isinstance(path, str) and path.startswith(
                    ("/home/isa/audits", "/home/isa/benchmarks")):
                calls.append(path)
            return real_exists(path, *a, **kw)

        with unittest.mock.patch("os.path.exists", side_effect=counting_exists):
            for bad in ({},
                        {"operator_approval": False, "approver": "x",
                         "approved_at": "2026-09-04T00:00:00Z"},
                        {"operator_approval": True, "approver": "",
                         "approved_at": "2026-09-04T00:00:00Z"},
                        {"operator_approval": True, "approver": "x",
                         "approved_at": "not-a-date"},
                        {"operator_approval": "yes", "approver": "x",
                         "approved_at": "2026-09-04T00:00:00Z"},
                        None):
                result = tier3_replay.replay("fifth", bad)
                self.assertEqual(result["status"], "refused", repr(bad))
                self.assertEqual(
                    result["gate"],
                    "historical replay requires explicit operator approval")
        self.assertEqual(calls, [],
                         "refusal performed filesystem probes: %s" % calls)

    def test_cli_gate_refuses_without_approval_flags(self):
        proc = subprocess.run(
            [PYTHON, str(EVAL / "eval_cli.py"), "tier3", "fifth"],
            capture_output=True, text=True, cwd=str(SKILL))
        self.assertEqual(proc.returncode, 3)
        self.assertIn("historical replay requires explicit operator "
                      "approval", proc.stderr)
        refusal = json.loads(proc.stdout)
        self.assertEqual(refusal["status"], "refused")
        # partial flags still refuse
        proc = subprocess.run(
            [PYTHON, str(EVAL / "eval_cli.py"), "tier3", "fifth",
             "--i-have-operator-approval", "--approver", "x"],
            capture_output=True, text=True, cwd=str(SKILL))
        self.assertEqual(proc.returncode, 3)


@unittest.skipUnless(os.path.isdir(FIFTH_RUN_DIR),
                     "Fifth historical run not present on this host")
class TestTier3FifthReplayReadOnly(unittest.TestCase):
    """Approved replay: scorecard correctness + strict read-only."""

    @classmethod
    def setUpClass(cls):
        cls.before = snapshot_tree(FIFTH_RUN_DIR)
        cls.card = tier3_replay.replay("fifth", VALID_APPROVAL)

    @classmethod
    def tearDownClass(cls):
        # belt and braces: nothing may appear or change after the class
        after = snapshot_tree(FIFTH_RUN_DIR)
        assert after == cls.before, "historical run dir mutated by replay"

    def test_status_and_shape(self):
        self.assertEqual(self.card["status"], "replayed")
        self.assertEqual(self.card["tier"], 3)
        self.assertTrue(self.card["target_head_matches_recorded"])
        self.assertEqual(self.card["completeness_state"],
                         "PARTIAL_CODEX_FAILURE")
        self.assertEqual(tuple(self.card["dimensions"]),
                         scoring.DIMENSIONS)
        self.assertFalse(self.card["environment_integrity_pass"])
        self.assertEqual(self.card["overall"], "NOT_READY")
        self.assertEqual(
            self.card["dimensions"]["FINAL_QUALITY"]["status"], "not-run")

    def test_economics_tokens_match_recorded_run_metrics(self):
        econ = self.card["dimensions"]["ECONOMICS"]
        tokens = econ["details"]["tokens"]
        self.assertEqual(tokens["input_tokens"], 11692279)
        self.assertEqual(tokens["output_tokens"], 59170)
        self.assertEqual(tokens["cached_input_tokens"], 10603008)
        self.assertEqual(tokens["reasoning_output_tokens"], 22544)
        # independently recomputed from the per-job records
        self.assertEqual(econ["details"]["recomputed_from_jobs"]
                         ["input_tokens"], 11692279)
        self.assertEqual(econ["details"]["usage_unknown_count"], 0)
        self.assertEqual(econ["score"], 1.0)

    def test_process_derived_from_artifacts(self):
        proc = self.card["dimensions"]["PROCESS"]
        self.assertEqual(proc["status"], "scored")
        checks = proc["details"]["checks"]
        self.assertTrue(checks["opus_independent_artifact"])
        self.assertTrue(checks["codex_independent_artifact"])
        self.assertTrue(checks["first_pass_independence"])
        # the codex cross-exam gap is EXPLICIT: failure_reason + raw kept
        self.assertTrue(checks["cross_examination_or_explicit_partial"])
        self.assertEqual(proc["score"], 1.0)

    def test_harness_classifications_reproduce(self):
        harness = self.card["dimensions"]["HARNESS"]
        rederived = harness["details"]["rederived_classifications"]
        self.assertEqual(len(rederived), 4)
        self.assertTrue(all(r["matches"] for r in rederived),
                        rederived)
        self.assertEqual(harness["score"], 1.0)

    def test_diversity_attribution_from_provenance(self):
        div = self.card["dimensions"]["DIVERSITY"]["details"]
        self.assertEqual(div["finding_count"], 9)
        self.assertEqual(sum(div["attribution"].values()), 9)
        self.assertEqual(div["attribution"]["unattributed"], 0)
        self.assertGreater(div["final_status"].get("CONFIRMED", 0), 0)

    def test_historical_dir_unchanged(self):
        after = snapshot_tree(FIFTH_RUN_DIR)
        self.assertEqual(after, self.before,
                         "replay wrote into the historical run dir")
        self.assertEqual(set(after), set(self.before))


if __name__ == "__main__":
    unittest.main()
