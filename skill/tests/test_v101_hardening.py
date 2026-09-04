"""v1.0.1 hardening-pass regression tests.

Issue 1 — repository fingerprint semantic equality against frozen run state.
Issue 2 — smoke documentation consistency with the canonical artifact.
Issue 3 — inline audit brief support (--brief-inline materialization).
Issue 4 — documentation distinguishes Codex sandbox PREVENTION from Claude
          mutation DETECTION.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
SKILL_ROOT = os.path.join(os.path.dirname(__file__), "..")
PYTHON = "python3"
AC = [PYTHON, os.path.join(SCRIPTS, "audit_council.py")]
FROZEN = "f" * 64
WRONG = "a" * 64  # syntactically valid, semantically wrong


def run_cli(args, stdin_text=None, env=None):
    return subprocess.run(AC + args, input=stdin_text, capture_output=True,
                          text=True, env=env, cwd=SCRIPTS)


class Fixture(unittest.TestCase):
    """Synthetic git repo + a run whose state carries a known fingerprint."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="v101-")
        # R6: keep active-run registrations out of the real user cache
        self._prev_cache = os.environ.get("AUDIT_COUNCIL_CACHE_HOME")
        os.environ["AUDIT_COUNCIL_CACHE_HOME"] = os.path.join(
            self.tmp, "cache")
        self.repo = os.path.join(self.tmp, "repo")
        os.makedirs(self.repo)
        for c in (["git", "init", "-q", "."],
                  ["git", "config", "user.email", "t@t"],
                  ["git", "config", "user.name", "t"]):
            subprocess.run(c, cwd=self.repo, check=True)
        with open(os.path.join(self.repo, "a.txt"), "w") as f:
            f.write("hi\n")
        subprocess.run(["git", "add", "-A"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "x"], cwd=self.repo,
                       check=True)
        with open(os.path.join(self.repo, "brief.md"), "w") as f:
            f.write("# brief\naudit a.txt\n")

    def tearDown(self):
        if self._prev_cache is None:
            os.environ.pop("AUDIT_COUNCIL_CACHE_HOME", None)
        else:
            os.environ["AUDIT_COUNCIL_CACHE_HOME"] = self._prev_cache
        shutil.rmtree(self.tmp, ignore_errors=True)

    def init_run(self, extra=None, stdin_text=None):
        args = ["init-run", "--repo", self.repo, "--brief",
                os.path.join(self.repo, "brief.md")]
        if extra:
            args = ["init-run", "--repo", self.repo] + extra
        proc = run_cli(args, stdin_text=stdin_text)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        run_dir = proc.stdout.strip()
        # pin the frozen fingerprint to a known value for these tests
        spath = os.path.join(run_dir, "state.json")
        state = json.load(open(spath))
        state["repo_fingerprint_sha256"] = FROZEN
        with open(spath, "w") as f:
            json.dump(state, f)
        return run_dir

    def freeze_contract(self, run_dir, fingerprint=FROZEN):
        # v2 A0.6: contract root/head must match the frozen environment
        # binding (placeholder values are now rejected)
        head = json.load(open(os.path.join(
            run_dir, "01-environment-binding.json")))["head_sha"]
        contract = {
            "objective": "o", "scope": ["a.txt"], "exclusions": [],
            "authoritative_sources": ["brief.md"],
            "target_repository": {"root": self.repo, "head_sha": head,
                                  "fingerprint_sha256": fingerprint},
            "severity_definitions": {k: k for k in
                                     ("CRITICAL", "HIGH", "MEDIUM", "LOW",
                                      "INFO")},
            "evidence_rules": [], "finding_schema_ref":
                "schemas/finding.schema.json", "done_criteria": ["d"],
        }
        proc = run_cli(["freeze-contract", "--run", run_dir, "--artifact",
                        "-", "--stdin"], stdin_text=json.dumps(contract))
        return proc

    def opus_audit(self, run_dir, fingerprint=FROZEN):
        finding = {
            "id": "OPUS-001", "origin": "OPUS-001", "title": "t",
            "category": "c", "severity": "HIGH", "confidence": "HIGH",
            "claim": "cl", "status": "PROVISIONAL",
            "evidence": [{"kind": "OBSERVED_FACT", "path": "a.txt"}],
            "provenance": {"discovered_by": "OPUS"},
        }
        art = {"model": "claude-opus-5",
               "repository_fingerprint_sha256": fingerprint,
               "findings": [finding], "audit_summary": "s"}
        return run_cli(["advance", "--run", run_dir, "--to",
                        "OPUS_INDEPENDENT_COMPLETE", "--artifact", "-",
                        "--stdin"], stdin_text=json.dumps(art))


# ---------------------------------------------------------------------------
# Issue 1 — semantic repository-fingerprint invariant
# ---------------------------------------------------------------------------

class TestFingerprintInvariant(Fixture):

    def test_wrong_but_valid_sha_rejected(self):
        run_dir = self.init_run()
        self.assertEqual(self.freeze_contract(run_dir).returncode, 0)
        proc = self.opus_audit(run_dir, fingerprint=WRONG)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("INVALID_ARTIFACT", proc.stderr + proc.stdout)
        state = json.load(open(os.path.join(run_dir, "state.json")))
        self.assertNotEqual(state["phase"], "OPUS_INDEPENDENT_COMPLETE")

    def test_correct_frozen_sha_accepted(self):
        run_dir = self.init_run()
        self.assertEqual(self.freeze_contract(run_dir).returncode, 0)
        proc = self.opus_audit(run_dir, fingerprint=FROZEN)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        state = json.load(open(os.path.join(run_dir, "state.json")))
        self.assertEqual(state["phase"], "OPUS_INDEPENDENT_COMPLETE")

    def test_contract_fingerprint_mismatch_rejected(self):
        run_dir = self.init_run()
        proc = self.freeze_contract(run_dir, fingerprint=WRONG)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("INVALID_ARTIFACT", proc.stderr + proc.stdout)

    def test_resume_refuses_mismatched_completed_artifact(self):
        run_dir = self.init_run()
        self.assertEqual(self.freeze_contract(run_dir).returncode, 0)
        # accept with correct fingerprint, then tamper semantically:
        # rewrite the artifact with a wrong (but valid) SHA and refresh its
        # checksum so ONLY the semantic check can catch it
        self.assertEqual(self.opus_audit(run_dir, fingerprint=FROZEN).returncode, 0)
        art_path = os.path.join(run_dir, "10-opus-independent.json")
        doc = json.load(open(art_path))
        doc["repository_fingerprint_sha256"] = WRONG
        with open(art_path, "w") as f:
            json.dump(doc, f)
        cs = os.path.join(run_dir, "checksums.sha256")
        lines = [l for l in open(cs) if not l.endswith(
            " 10-opus-independent.json\n")]
        digest = hashlib.sha256(open(art_path, "rb").read()).hexdigest()
        lines.append("%s  10-opus-independent.json\n" % digest)
        open(cs, "w").writelines(lines)
        proc = run_cli(["resume-check", "--run", run_dir])
        self.assertEqual(proc.returncode, 9)  # EXIT_INVALID_ARTIFACT
        self.assertIn("INVALID_ARTIFACT", proc.stdout + proc.stderr)

    def test_finalize_cannot_consume_mismatched_final_artifact(self):
        run_dir = self.init_run()
        self.assertEqual(self.freeze_contract(run_dir).returncode, 0)
        self.assertEqual(self.opus_audit(run_dir).returncode, 0)
        final = {
            "completeness_state": "COMPLETE",
            "repository_fingerprint_sha256": WRONG,
            "executive_summary": "s",
            "findings": [],
        }
        proc = run_cli(["advance", "--run", run_dir, "--to", "FINALIZED",
                        "--artifact", "-", "--stdin"],
                       stdin_text=json.dumps(final))
        # rejected before any finalize can consume it
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("INVALID_ARTIFACT", proc.stderr + proc.stdout)

    def test_invalid_output_diagnosable_not_canonical(self):
        run_dir = self.init_run()
        self.assertEqual(self.freeze_contract(run_dir).returncode, 0)
        proc = self.opus_audit(run_dir, fingerprint=WRONG)
        self.assertNotEqual(proc.returncode, 0)
        # staged file remains on disk for diagnosis, but the phase did not
        # advance and the artifact was never recorded as canonical checksum
        staged = os.path.join(run_dir, "10-opus-independent.json")
        self.assertTrue(os.path.isfile(staged))
        state = json.load(open(os.path.join(run_dir, "state.json")))
        self.assertEqual(state["phase"], "CONTRACT_FROZEN")
        cs = open(os.path.join(run_dir, "checksums.sha256")).read()
        self.assertNotIn("10-opus-independent.json", cs)


# ---------------------------------------------------------------------------
# Issue 2 — smoke documentation consistency (canonical artifact wins)
# ---------------------------------------------------------------------------

SMOKE_ARTIFACT = os.path.join(
    os.path.expanduser("~"), "audit-council-dev", "smoke-fixture",
    "audit-output", "audit-council", "20260903T180532Z-bbc9b3", "logs",
    "independent.final.json")
SMOKE_RECORD = os.path.join(os.path.expanduser("~"), "audit-council-dev",
                            "SMOKE_TEST_RECORD.md")


class TestSmokeDocConsistency(unittest.TestCase):

    @unittest.skipUnless(os.path.isfile(SMOKE_ARTIFACT)
                         and os.path.isfile(SMOKE_RECORD),
                         "smoke artifacts not present on this machine")
    def test_record_finding_count_matches_canonical_artifact(self):
        doc = json.load(open(SMOKE_ARTIFACT))
        ids = [f["id"] for f in doc.get("findings", [])]
        text = open(SMOKE_RECORD).read()
        # every canonical finding id is mentioned, and the record states the
        # canonical count; the canonical artifact wins over any prose claim
        for cid in ids:
            self.assertIn(cid, text)
        self.assertIn("%d finding" % len(ids), text,
                      "record must state the canonical finding count (%d)"
                      % len(ids))


# ---------------------------------------------------------------------------
# Issue 3 — inline audit brief
# ---------------------------------------------------------------------------

class TestInlineBrief(Fixture):

    def test_file_brief_still_works(self):
        run_dir = self.init_run()
        self.assertTrue(os.path.isdir(run_dir))
        man = json.load(open(os.path.join(run_dir, "00-run-manifest.json")))
        self.assertEqual(man["brief_source"], "file")
        self.assertEqual(man["brief_path"],
                         os.path.join(self.repo, "brief.md"))

    def test_inline_brief_works_and_materialized(self):
        text = 'Audit "quoted" `code`\nline two\n'
        proc = run_cli(["init-run", "--repo", self.repo, "--brief-inline"],
                       stdin_text=text)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        run_dir = proc.stdout.strip()
        mat = os.path.join(run_dir, "inputs", "original-audit-brief.md")
        self.assertTrue(os.path.isfile(mat), "materialized brief missing")
        self.assertEqual(open(mat).read(), text)

    def test_inline_brief_checksum_persisted(self):
        text = "# inline\nbody\n"
        run_dir = run_cli(["init-run", "--repo", self.repo,
                           "--brief-inline"], stdin_text=text).stdout.strip()
        mat = os.path.join(run_dir, "inputs", "original-audit-brief.md")
        digest = hashlib.sha256(open(mat, "rb").read()).hexdigest()
        man = json.load(open(os.path.join(run_dir, "00-run-manifest.json")))
        self.assertEqual(man["brief_sha256"], digest)
        self.assertEqual(man["brief_source"], "inline")
        cs = open(os.path.join(run_dir, "checksums.sha256")).read()
        self.assertIn(digest, cs)

    def test_resume_references_materialized_copy(self):
        run_dir = run_cli(["init-run", "--repo", self.repo,
                           "--brief-inline"], stdin_text="b\n").stdout.strip()
        man = json.load(open(os.path.join(run_dir, "00-run-manifest.json")))
        self.assertTrue(man["brief_path"].startswith(run_dir))
        # resume-check validates checksums incl. the materialized brief
        proc = run_cli(["resume-check", "--run", run_dir])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_multiline_quoted_content_handled_safely(self):
        text = 'brief with "quotes" and $shell and \\backslash\n---\n``` fences\n'
        run_dir = run_cli(["init-run", "--repo", self.repo, "--brief-inline"],
                          stdin_text=text).stdout.strip()
        mat = os.path.join(run_dir, "inputs", "original-audit-brief.md")
        self.assertEqual(open(mat, encoding="utf-8").read(), text)

    def test_nonexistent_path_not_silently_inline(self):
        proc = run_cli(["init-run", "--repo", self.repo, "--brief",
                        os.path.join(self.tmp, "no-such-brief.md")])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("missing or empty", proc.stderr + proc.stdout)
        # and nothing was created
        runs_root = os.path.join(self.repo, "audit-output", "audit-council")
        if os.path.isdir(runs_root):
            self.assertEqual(os.listdir(runs_root), [])

    def test_inline_and_file_are_mutually_exclusive(self):
        proc = run_cli(["init-run", "--repo", self.repo, "--brief",
                        os.path.join(self.repo, "brief.md"), "--brief-inline"],
                       stdin_text="x")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("not both", proc.stderr + proc.stdout)

    def test_preflight_inline(self):
        proc = run_cli(["preflight", "--repo", self.repo, "--brief-inline",
                        "--skip-codex"], stdin_text="valid brief")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        proc = run_cli(["preflight", "--repo", self.repo, "--brief-inline",
                        "--skip-codex"], stdin_text="   ")
        self.assertNotEqual(proc.returncode, 0)


# ---------------------------------------------------------------------------
# Issue 4 — documentation distinguishes prevention from detection
# ---------------------------------------------------------------------------

class TestWriteGuaranteeDocs(unittest.TestCase):

    def test_readme_distinguishes_prevention_from_detection(self):
        text = open(os.path.join(SKILL_ROOT, "README.md")).read()
        self.assertIn("mechanically PREVENTED", text)
        self.assertIn("DETECT", text)
        self.assertIn("detection, not an", text)

    def test_skill_md_distinguishes_prevention_from_detection(self):
        text = open(os.path.join(SKILL_ROOT, "SKILL.md")).read()
        self.assertIn("mechanically PREVENTED", text)
        self.assertIn("DETECT", text)

    def test_no_os_sandbox_claim_for_claude(self):
        for name in ("README.md", "SKILL.md"):
            text = open(os.path.join(SKILL_ROOT, name)).read()
            self.assertNotIn("Claude has an OS-level read-only sandbox",
                             text)
            self.assertNotIn("Claude runs in a read-only sandbox", text)


if __name__ == "__main__":
    unittest.main()
