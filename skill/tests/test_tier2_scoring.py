#!/usr/bin/env python3
"""Tier-2 FAKE-MODEL scoring (deterministic): scripted artifacts derived
from sealed truth, executed through the REAL pipeline. Proves the scoring
machinery + pipeline honesty end to end; no model calls."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

EVAL = Path(__file__).resolve().parent.parent / "eval"
SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(EVAL))
sys.path.insert(0, str(SCRIPTS))

import tier2_scoring  # noqa: E402


class TestTier2FakeModelScoring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tempfile.mkdtemp(prefix="t2s-", dir=str(
            Path(__file__).resolve().parent / "fixtures"))
        cls.card = tier2_scoring.tier2_score(cls.root)

    @classmethod
    def tearDownClass(cls):
        import shutil
        shutil.rmtree(cls.root, ignore_errors=True)

    def test_all_fixtures_scored_without_errors(self):
        self.assertEqual(self.card["overall"]["errors"], [])
        self.assertEqual(len(self.card["fixtures"]), 10)

    def test_recall_precision_perfect_on_scripted_truth(self):
        for f in self.card["fixtures"]:
            self.assertEqual(f["recall"], 1.0, f)
            self.assertEqual(f["precision"], 1.0, f)

    def test_protected_controls_never_flagged_in_primary(self):
        self.assertEqual(
            self.card["overall"]["protected_control_violations_total"], 0)

    def test_false_positive_rejected_by_pipeline(self):
        # the seeded fabricated finding must be in SOME rejected appendix
        fp_fixture = next(f for f in self.card["fixtures"]
                          if f["fixture"] != "clean-idioms")
        import json
        final = json.load(open(
            f"{fp_fixture['run_dir']}/90-final-findings.json"))
        rejected = " ".join(r["title"] for r in
                            final.get("rejected_appendix", []))
        self.assertIn("FP-1", rejected)

    def test_clean_idioms_protected_candidate_rejected(self):
        ci = next(f for f in self.card["fixtures"]
                  if f["fixture"] == "clean-idioms")
        import json
        final = json.load(open(f"{ci['run_dir']}/90-final-findings.json"))
        rejected = " ".join(r["title"] for r in
                            final.get("rejected_appendix", []))
        self.assertIn("NEG-1", rejected)
        self.assertEqual(final["findings"], [])


if __name__ == "__main__":
    unittest.main()
