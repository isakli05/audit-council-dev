#!/usr/bin/env python3
"""Mocked end-to-end tests for codex_runner.py and render_report.py.

No real codex, no quota. Uses tests/fixtures/fake_codex.py as the codex binary.

If the sibling scripts/state_store.py and validate_artifact.py do not exist yet
(pre-integration), minimal stub modules are generated in a temp dir OUTSIDE the
skill tree and put on sys.path/PYTHONPATH; the shipped code imports the real
modules unconditionally once they exist.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

PYTHON = "python3"

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
FIXTURES = os.path.join(HERE, "fixtures")
RUNNER = os.path.join(SCRIPTS_DIR, "codex_runner.py")
FAKE_CODEX = os.path.join(FIXTURES, "fake_codex.py")

STUB_STATE_STORE = '''
import json, os

def load_state(run_dir):
    with open(os.path.join(run_dir, "state.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(run_dir, state):
    path = os.path.join(run_dir, "state.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
'''

STUB_VALIDATE_ARTIFACT = '''
def validate(instance, schema):
    # minimal: type + required + enum at top level (sufficient for stubs)
    if schema.get("type") == "object" and not isinstance(instance, dict):
        raise ValueError("instance is not an object")
    for key in schema.get("required", []):
        if key not in instance:
            raise ValueError("missing required key: %s" % key)
    if "enum" in schema and instance not in schema["enum"]:
        raise ValueError("not in enum")
    return True
'''

_STUB_DIR = None


def _ensure_stub_modules():
    """Create stub state_store/validate_artifact outside the skill tree when
    the real ones are not present yet."""
    global _STUB_DIR
    if os.path.isfile(os.path.join(SCRIPTS_DIR, "state_store.py")) and \
       os.path.isfile(os.path.join(SCRIPTS_DIR, "validate_artifact.py")):
        return None
    _STUB_DIR = tempfile.mkdtemp(prefix="audit-council-stubs-")
    with open(os.path.join(_STUB_DIR, "state_store.py"), "w") as f:
        f.write(STUB_STATE_STORE)
    with open(os.path.join(_STUB_DIR, "validate_artifact.py"), "w") as f:
        f.write(STUB_VALIDATE_ARTIFACT)
    sys.path.insert(0, _STUB_DIR)
    return _STUB_DIR


_ensure_stub_modules()
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import codex_runner  # noqa: E402
import render_report  # noqa: E402


def make_state(repo_root, run_id="20260903T000000Z-ab01cd"):
    return {
        "schema_version": 1,
        "run_id": run_id,
        "phase": "CONTRACT_FROZEN",
        "completeness_state": "RUNNING",
        "created_at": "2026-09-03T00:00:00Z",
        "timestamps": {},
        "repo_fingerprint_sha256": "deadbeefdeadbeef",
        "repo_root": repo_root,
        "codex": {
            "session_id": None,
            "jobs": [],
            "stage_counts": {"independent": 0, "cross_examination": 0,
                             "adjudication": 0},
        },
        "phase_attempts": {},
        "failure_reason": None,
    }


class Harness(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="audit-council-test-")
        self.repo = os.path.join(self.tmp, "repo")
        self.run = os.path.join(self.repo, "audit-output", "audit-council",
                                "20260903T000000Z-ab01cd")
        os.makedirs(os.path.join(self.run, "prompts"))
        os.makedirs(os.path.join(self.run, "logs"))
        with open(os.path.join(self.repo, "audit-brief.md"), "w") as f:
            f.write("# brief\ncheck things\n")
        with open(os.path.join(self.run, "prompts", "codex-independent.md"), "w") as f:
            f.write("Independent audit prompt. Do the audit.\n")
        with open(os.path.join(self.run, "prompts",
                               "codex-cross-examination-opus.md"), "w") as f:
            f.write("Cross-examination prompt.\n")
        with open(os.path.join(self.run, "prompts",
                               "codex-targeted-adjudication.md"), "w") as f:
            f.write("Adjudication prompt.\n")
        with open(os.path.join(self.run, "state.json"), "w") as f:
            json.dump(make_state(self.repo), f)
        self.base_env = dict(os.environ)
        self.base_env["FAKE_CODEX_MODE"] = "ok"
        # test-only fast polling; production default (2s) is unchanged
        self.base_env["CODEX_RUNNER_POLL_INTERVAL"] = "0.02"
        if _STUB_DIR:
            self.base_env["PYTHONPATH"] = _STUB_DIR

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- CLI helpers -------------------------------------------------------
    def cli(self, *args, mode="ok", extra_env=None, timeout=60):
        env = dict(self.base_env)
        env["FAKE_CODEX_MODE"] = mode
        if extra_env:
            env.update(extra_env)
        return subprocess.run([PYTHON, RUNNER] + list(args),
                              capture_output=True, text=True, env=env,
                              timeout=timeout)

    def start(self, phase="independent", mode="ok", session=None, expect=0):
        args = ["start", "--run", self.run, "--phase", phase,
                "--codex-bin", FAKE_CODEX]
        if session:
            args += ["--session", session]
        proc = self.cli(*args, mode=mode)
        self.assertEqual(proc.returncode, expect, proc.stderr)
        if expect == 0:
            return proc.stdout.strip()
        return proc

    def wait(self, job_path, timeout=30):
        return self.cli("wait", job_path, "--timeout", str(timeout))

    def job_json(self, job_path):
        with open(job_path) as f:
            return json.load(f)

    def state(self):
        with open(os.path.join(self.run, "state.json")) as f:
            return json.load(f)


# ---------------------------------------------------------------------------
# happy path + telemetry (also scenario O argv checks)
# ---------------------------------------------------------------------------

class TestComplete(Harness):
    def test_ok_complete_metrics_session(self):
        job_path = self.start()
        # scenario O/N: fresh argv checks
        argv = self.job_json(job_path)["argv"]
        self.assertIn("--sandbox", argv)
        self.assertEqual(argv[argv.index("--sandbox") + 1], "read-only")
        self.assertNotIn("--last", argv)
        for bad in ("--dangerously-bypass-approvals-and-sandbox", "danger-full-access"):
            self.assertNotIn(bad, argv)
        self.assertIn('model_reasoning_effort="xhigh"',
                      [a for a in argv if a.startswith("model_reasoning_effort")])

        proc = self.wait(job_path)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("COMPLETE", proc.stdout)

        job = self.job_json(job_path)
        self.assertEqual(job["status"], "COMPLETE")

        # session id persisted to state.json
        state = self.state()
        self.assertEqual(state["codex"]["session_id"], "fake-session-123")
        self.assertEqual(state["codex"]["stage_counts"]["independent"], 1)

        # metrics written with token aggregates
        with open(os.path.join(self.run, "99-run-metrics.json")) as f:
            metrics = json.load(f)
        agg = metrics["aggregates"]
        self.assertEqual(agg["invocation_count"], 1)
        self.assertEqual(agg["fresh_count"], 1)
        self.assertEqual(agg["resumed_count"], 0)
        self.assertEqual(agg["tokens"]["input_tokens"], 100)
        self.assertEqual(agg["tokens"]["cached_input_tokens"], 50)
        self.assertEqual(agg["tokens"]["output_tokens"], 200)
        self.assertEqual(agg["tokens"]["reasoning_output_tokens"], 80)
        self.assertEqual(agg["turns_total"], 1)

    def test_codex_schema_self_contained(self):
        self.start()
        p = os.path.join(self.run, "schemas", "independent-audit-codex.schema.json")
        self.assertTrue(os.path.isfile(p))
        with open(p) as f:
            text = f.read()
        self.assertNotIn("$ref", text)
        self.assertNotIn("$id", text)
        schema = json.loads(text)
        self.assertIn("finding", json.dumps(schema["properties"]["findings"]))

    def test_result_command(self):
        job_path = self.start()
        self.wait(job_path)
        proc = self.cli("result", job_path)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data["model"], "gpt-5.6-sol")

    def test_status_command(self):
        job_path = self.start()
        proc = self.cli("status", job_path)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("alive", json.loads(proc.stdout))


# ---------------------------------------------------------------------------
# failure classification scenarios G,H,I,J,K,L
# ---------------------------------------------------------------------------

class TestClassification(Harness):
    def test_g_exit0_missing_output_invalid(self):
        job_path = self.start(mode="exit0_no_output")
        proc = self.wait(job_path)
        self.assertEqual(proc.returncode, 6)
        self.assertEqual(self.job_json(job_path)["status"], "INVALID_OUTPUT")

    def test_h_malformed_json_invalid_then_repair_once(self):
        job_path = self.start(mode="malformed_json")
        job = json.load(open(job_path))
        raw = job["output_path"]  # per-job raw wire output (v1.0.3)
        proc = self.wait(job_path)
        self.assertEqual(proc.returncode, 6)
        # raw preserved
        self.assertTrue(os.path.isfile(raw))
        with open(raw) as f:
            self.assertIn("broken", f.read())

        # repair once: resumes same session, ok mode this time
        rep = self.cli("repair", job_path)
        self.assertEqual(rep.returncode, 0, rep.stderr)
        repair_job = rep.stdout.strip()
        rj = self.job_json(repair_job)
        self.assertIn("exec", rj["argv"])
        self.assertEqual(rj["argv"][rj["argv"].index("resume") + 1], "fake-session-123")
        proc = self.wait(repair_job)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        # repair output is a new file
        self.assertTrue(os.path.isfile(rj["output_path"]))

        # second repair for the same phase refused (exit 3), stage reuse:
        # no additional stage count
        before = self.state()["codex"]["stage_counts"]
        rep2 = self.cli("repair", job_path)
        self.assertEqual(rep2.returncode, 3)
        self.assertEqual(self.state()["codex"]["stage_counts"], before)

    def test_i_partial_jsonl_complete_degraded(self):
        job_path = self.start(mode="partial_jsonl")
        proc = self.wait(job_path)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        with open(os.path.join(self.run, "99-run-metrics.json")) as f:
            metrics = json.load(f)
        inv = metrics["invocations"][0]
        self.assertTrue(inv["degraded_telemetry"])
        self.assertEqual(inv["turns"], 0)
        self.assertEqual(metrics["aggregates"]["degraded_telemetry_count"], 1)

    def test_j_crash_failed(self):
        job_path = self.start(mode="crash")
        proc = self.wait(job_path)
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(self.job_json(job_path)["status"], "FAILED")

    def test_k_quota(self):
        job_path = self.start(mode="quota")
        proc = self.wait(job_path)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(self.job_json(job_path)["status"], "QUOTA")

    def test_l_auth(self):
        job_path = self.start(mode="auth")
        proc = self.wait(job_path)
        self.assertEqual(proc.returncode, 3)
        self.assertEqual(self.job_json(job_path)["status"], "AUTH_ERROR")

    def test_wait_timeout_running(self):
        job_path = self.start(mode="slow")
        proc = self.wait(job_path, timeout=1)
        self.assertEqual(proc.returncode, 7)
        self.assertIn("RUNNING", proc.stdout)
        # cleanup
        self.cli("cancel", job_path)


# ---------------------------------------------------------------------------
# resume semantics (M, N, O)
# ---------------------------------------------------------------------------

class TestResume(Harness):
    def test_m_explicit_session_resume(self):
        job_path = self.start(phase="cross_examination", session="SESS-42")
        job = self.job_json(job_path)
        # v2: argv may be the bwrap-wrapped invocation; the exact codex
        # argv (what the assertions are about) is preserved separately
        argv = job.get("codex_argv") or job["argv"]
        self.assertEqual(argv[1:4], ["exec", "resume", "SESS-42"])
        self.assertNotIn("--last", argv)
        self.assertNotIn("--sandbox", argv)
        # O: resume uses -c sandbox_mode="read-only"
        self.assertIn('sandbox_mode="read-only"', argv)
        self.assertIn('model_reasoning_effort="xhigh"', argv)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", argv)
        self.assertNotIn("danger-full-access", argv)

    def test_n_no_argv_ever_contains_last(self):
        for phase, session in (("independent", None),
                               ("cross_examination", "S1"),
                               ("adjudication", "S1")):
            self._free_stage(phase)
            job_path = self.start(phase=phase, session=session)
            argv = self.job_json(job_path)["argv"]
            self.assertNotIn("--last", argv, "%s: %s" % (phase, argv))
            self.cli("cancel", job_path)

    def test_session_default_from_state_for_later_phases(self):
        state = self.state()
        state["codex"]["session_id"] = "STATE-SESS"
        with open(os.path.join(self.run, "state.json"), "w") as f:
            json.dump(state, f)
        job_path = self.start(phase="cross_examination")
        argv = self.job_json(job_path)["argv"]
        self.assertEqual(argv[argv.index("resume") + 1], "STATE-SESS")

    def _free_stage(self, phase):
        state = self.state()
        state["codex"]["stage_counts"][phase] = 0
        with open(os.path.join(self.run, "state.json"), "w") as f:
            json.dump(state, f)


# ---------------------------------------------------------------------------
# budget governor (W)
# ---------------------------------------------------------------------------

class TestFingerprintRejection(Harness):
    """v1.0.1 Issue 1: a codex output claiming a wrong repository fingerprint
    (syntactically valid) must be INVALID_OUTPUT, raw preserved, and must not
    bump the budget-governor stage count."""

    def test_wrong_fingerprint_invalid_output(self):
        self.base_env["FAKE_CODEX_FINGERPRINT"] = "a" * 64
        job_path = self.start()
        proc = self.cli("wait", job_path, "--timeout", "30")
        self.assertEqual(proc.returncode, 6, proc.stdout + proc.stderr)
        job = json.load(open(job_path))
        self.assertEqual(job["status"], "INVALID_OUTPUT")
        self.assertIn("INVALID_ARTIFACT", job.get("error", ""))
        self.assertTrue(job.get("raw_output_preserved"))
        self.assertTrue(os.path.getsize(job["output_path"]) > 0)
        # failed stage not counted -> retry remains possible
        self.assertEqual(self.state()["codex"]["stage_counts"]
                         ["independent"], 0)

    def test_matching_fingerprint_completes(self):
        self.base_env["FAKE_CODEX_FINGERPRINT"] = "deadbeefdeadbeef"
        job_path = self.start()
        self.wait(job_path)
        self.assertEqual(self.state()["codex"]["stage_counts"]
                         ["independent"], 1)


class TestGovernor(Harness):
    def test_w_second_stage_same_phase_refused(self):
        job = self.start()  # independent used...
        self.wait(job)      # ...and COMPLETED (governor counts successes)
        proc = self.start(expect=3, phase="independent")
        self.assertIn("budget governor", (proc.stderr + proc.stdout))

    def test_w_total_cap_three(self):
        state = self.state()
        state["codex"]["stage_counts"] = {"independent": 1,
                                          "cross_examination": 1,
                                          "adjudication": 1}
        with open(os.path.join(self.run, "state.json"), "w") as f:
            json.dump(state, f)
        proc = self.start(expect=3, phase="adjudication")
        self.assertIn("budget governor", (proc.stderr + proc.stdout))

    def test_stage_counted_on_success_not_start(self):
        # governor counts SUCCESSFUL stages; a failed stage may be retried on
        # resume (quota semantics), bounded by the per-phase attempts cap
        job_path = self.start(mode="crash")
        self.wait(job_path)  # FAILED — stage NOT counted, retry allowed
        self.assertEqual(self.state()["codex"]["stage_counts"]["independent"], 0)
        job_path = self.start(mode="ok")   # retry permitted
        self.wait(job_path)
        self.assertEqual(self.state()["codex"]["stage_counts"]["independent"], 1)
        self.start(mode="ok", expect=3)   # successful stage never repeated


# ---------------------------------------------------------------------------
# cancel + hygiene
# ---------------------------------------------------------------------------

class TestLifecycle(Harness):
    def test_cancel(self):
        job_path = self.start(mode="slow")
        proc = self.cli("cancel", job_path)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(self.job_json(job_path)["status"], "CANCELLED")

    def test_missing_prompt_refused(self):
        os.remove(os.path.join(self.run, "prompts", "codex-independent.md"))
        proc = self.cli("start", "--run", self.run, "--phase", "independent",
                        "--codex-bin", FAKE_CODEX)
        self.assertEqual(proc.returncode, 3)

    def test_no_temp_files_left(self):
        job_path = self.start()
        self.wait(job_path)
        leftovers = [f for f in os.listdir(os.path.join(self.run, "logs"))
                     if ".tmp" in f]
        self.assertEqual(leftovers, [])
        leftovers_all = []
        for root, _dirs, files in os.walk(self.run):
            leftovers_all += [os.path.join(root, f) for f in files if ".tmp" in f]
        self.assertEqual(leftovers_all, [])


# ---------------------------------------------------------------------------
# render_report
# ---------------------------------------------------------------------------

class TestRender(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="audit-council-render-")
        finding = {
            "id": "CODEX-001", "origin": "CODEX-001", "title": "No divide-by-zero guard",
            "category": "correctness", "severity": "HIGH", "confidence": "HIGH",
            "claim": "divide() crashes on b=0", "status": "CONFIRMED",
            "evidence": [{"kind": "OBSERVED_FACT", "path": "src/app.py",
                          "line_ranges": [{"start": 1, "end": 2}],
                          "description": "no zero check"}],
            "provenance": {"discovered_by": "CODEX"},
        }
        self.independent = {
            "model": "gpt-5.6-sol", "repository_fingerprint_sha256": "deadbeef",
            "audit_summary": "One finding.", "findings": [finding],
            "limitations": ["time-boxed"],
        }
        self.ledger = {
            "clusters": [{
                "cluster_id": "CLUSTER-001",
                "initial_classification": "CONSENSUS_CANDIDATE",
                "status": "CONSENSUS",
                "member_finding_ids": ["OPUS-001", "CODEX-001"],
                "positions": {
                    "opus": {"position": "valid", "severity": "HIGH"},
                    "codex": {"position": "valid", "severity": "HIGH"},
                },
                "notes": "both agree",
            }]
        }
        self.final = {
            "completeness_state": "COMPLETE",
            "repository_fingerprint_sha256": "deadbeef",
            "executive_summary": "One confirmed finding.",
            "methodology": "council",
            "findings": [{
                "cluster_id": "CLUSTER-001", "title": "No divide-by-zero guard",
                "severity": "HIGH", "final_status": "CONFIRMED",
                "claim": "divide() crashes on b=0", "root_cause": "missing guard",
                "evidence": [], "provenance": {
                    "origin": ["CODEX-001"], "opus_challenge": "CONFIRMED",
                    "codex_challenge": "CONFIRMED", "adjudication": None,
                    "final_status": "CONSENSUS"},
            }],
            "rejected_appendix": [{"cluster_id": "CLUSTER-002",
                                   "title": "style nit", "reason": "out of scope"}],
            "unresolved_risks": [], "residual_risks": ["none"],
            "coverage_gaps": ["REQ-2 untested"],
            "limitations": ["time-boxed"],
            "claims_lacking_second_model": [],
        }
        with open(os.path.join(self.tmp, "20-codex-independent.json"), "w") as f:
            json.dump(self.independent, f)
        with open(os.path.join(self.tmp, "40-disagreement-ledger.json"), "w") as f:
            json.dump(self.ledger, f)
        with open(os.path.join(self.tmp, "90-final-findings.json"), "w") as f:
            json.dump(self.final, f)
        with open(os.path.join(self.tmp, "99-run-metrics.json"), "w") as f:
            json.dump({"invocations": [], "aggregates": {
                "invocation_count": 3, "fresh_count": 1, "resumed_count": 2,
                "turns_total": 5, "elapsed_sec_total": 120.5,
                "tokens": {"input_tokens": 300, "cached_input_tokens": 150,
                           "output_tokens": 600, "reasoning_output_tokens": 240}}}, f)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_render_independent(self):
        md = render_report.render(self.tmp, "20-codex-independent")
        self.assertIn("Independent Audit — gpt-5.6-sol", md)
        self.assertIn("CODEX-001", md)
        self.assertIn("src/app.py", md)
        self.assertIn("OBSERVED_FACT", md)
        self.assertIn("L1-2", md)  # v2 compact line_ranges citation

    def test_render_ledger(self):
        md = render_report.render(self.tmp, "40-disagreement-ledger")
        self.assertIn("CLUSTER-001", md)
        self.assertIn("CONSENSUS_CANDIDATE", md)
        self.assertIn("OPUS-001", md)

    def test_render_final_all_sections(self):
        md = render_report.render(self.tmp, "90-final-findings")
        for section in render_report.FINAL_SECTION_ORDER:
            self.assertIn(section, md)
        self.assertIn("Origin: CODEX-001 | Opus challenge: CONFIRMED | "
                      "Codex re-evaluation: CONFIRMED | Final: CONSENSUS", md)
        self.assertIn("REQ-2 untested", md)
        self.assertIn("style nit", md)
        self.assertIn("missing guard", md)
        self.assertIn("input: 300", md)
        self.assertNotIn("best", md.lower().replace("best-effort", ""))

    def test_main_writes_default_final_path(self):
        out = os.path.join(self.tmp, "90-final-audit.md")
        proc = subprocess.run(
            [PYTHON, os.path.join(SCRIPTS_DIR, "render_report.py"),
             "--run", self.tmp, "--artifact", "90-final-findings"],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(os.path.isfile(out))


if __name__ == "__main__":
    unittest.main()
