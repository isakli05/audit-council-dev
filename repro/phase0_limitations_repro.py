#!/usr/bin/env python3
"""Phase 0 deterministic reproduction of known v1.0.3 limitations.

Reproduces, against the EXACT production code paths and the EXACT historical
payloads, the three limitations the v2 program targets:

  R1 (pillar G): the Fifth run's real cross-examination wire output
      (`184-185, 240-273` multi-range evidence lines, run 20260904T081903Z-60651d,
      READ-ONLY input) is classified INVALID_OUTPUT by codex_runner's production
      wire->canonical->canonical-validation path, while the same evidence with a
      single range validates. Deterministic; no model calls.

  R2 (pillar E): terminal attempts classified QUOTA / INVALID_OUTPUT get
      completed_at + tokens persisted but NO elapsed_sec (the Fifth telemetry
      gap), unlike COMPLETE attempts.

  R3 (pillar A0): preflight + init-run succeed with a brief whose declared
      repository root points at a DIFFERENT live repository (the Fifth run's
      stale-absolute-path failure mode). No brief/root/HEAD consistency gate
      and no environment binding exist in v1.0.3.

Writes only under repro/tmp/ (disposable). Historical runs are opened
read-only. Exits 0 iff all three limitations reproduce as described.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DEV = Path(__file__).resolve().parent.parent
SKILL = DEV / "skill"
sys.path.insert(0, str(SKILL / "scripts"))

import audit_council  # noqa: E402
import codex_runner  # noqa: E402
import state_store  # noqa: E402
import validate_artifact  # noqa: E402
import wire_adapter  # noqa: E402

FIFTH_RUN = Path("/home/isa/audits/lco-fifth-independent-release-audit/"
                 "target/audit-output/audit-council/20260904T081903Z-60651d")
FIFTH_FAILED_WIRE = FIFTH_RUN / "logs" / \
    "cross_examination.cross_examination-repair-86eeb1ee.final.json"

TMP = DEV / "repro" / "tmp"
RESULTS: list[dict] = []

# NOTE: in this environment `python3` may be a ZCode AppImage wrapper whose
# sys.executable is the AppImage itself (spawning it runs the desktop app, not
# the script). Always spawn the real system CPython for child script runs.
PY = "/usr/bin/python3" if os.path.exists("/usr/bin/python3") else sys.executable


def result(name: str, reproduced: bool, detail: dict) -> None:
    RESULTS.append({"limitation": name, "reproduced": reproduced, **detail})
    print(f"[{'REPRODUCED' if reproduced else 'NOT-REPRODUCED'}] {name}")
    for k, v in detail.items():
        print(f"    {k}: {v}")


def sandbox_run_dir(label: str) -> str:
    """A minimal valid run dir (state.json + logs) inside repro/tmp."""
    rd = TMP / label
    if rd.exists():
        shutil.rmtree(rd)
    (rd / "logs" / "jobs").mkdir(parents=True)
    state = state_store.new_state("20260904T000000Z-abc123", str(rd),
                                  "0" * 64)
    state_store.atomic_write_json(rd / state_store.STATE_NAME, state)
    return str(rd)


def fake_job(run_dir: str, phase: str) -> dict:
    return {
        "job_id": f"{phase}-repro000",
        "run_dir": run_dir,
        "phase": phase,
        "pid": os.getpid(),
        "argv": ["codex", "exec"],
        "session": "sess-repro",
        "resumed": True,
        "fresh_or_resumed": "resumed",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
        "attempt_number": 1,
        "started_at": codex_runner.utc_now(),
        "started_at_monotonic": time.monotonic() - 30.0,
        "status": "RUNNING",
        "artifact_status": "NOT_PRODUCED",
        "successful_stage_counted": False,
        "prompt_path": os.path.join(run_dir, "prompts", f"{phase}.md"),
        "output_path": os.path.join(run_dir, "logs", f"{phase}.repro000.final.json"),
        "schema_path": "unused",
        "stdout_path": os.path.join(run_dir, "logs", f"{phase}.repro000.jsonl"),
        "stderr_path": os.path.join(run_dir, "logs", f"{phase}.repro000.stderr.log"),
        "exit_code_path": os.path.join(run_dir, "logs", "jobs",
                                       f"{phase}-repro000.exitcode"),
    }


# ---------------------------------------------------------------------------
# R1 — multi-range evidence lines rejected (pillar G), exact Fifth payload
# ---------------------------------------------------------------------------
def repro_r1() -> None:
    assert FIFTH_FAILED_WIRE.is_file(), f"missing historical payload: {FIFTH_FAILED_WIRE}"
    wire_doc = json.loads(FIFTH_FAILED_WIRE.read_text())

    # collect the exact offending values present in the real payload
    def collect(node, acc):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "lines" and isinstance(v, str) and "," in v:
                    acc.add(v)
                collect(v, acc)
        elif isinstance(node, list):
            for x in node:
                collect(x, acc)
    offenders: set[str] = set()
    collect(wire_doc, offenders)

    canon = json.loads((SKILL / "schemas" / "cross-examination.schema.json").read_text())

    # production path, step by step (same code classify_and_finalize uses)
    candidate, norm_errors = wire_adapter.wire_to_canonical(
        wire_doc, canon, str(SKILL / "schemas"))
    errors = validate_artifact.validate(
        candidate, canon, base_dir=SKILL / "schemas") if not norm_errors else norm_errors
    line_errors = [e for e in errors if "lines" in e or "pattern" in e]

    # control: same doc with the multi-range values replaced by their first range
    def patch(node):
        if isinstance(node, dict):
            return {k: (v.split(",")[0].strip() if k == "lines"
                        and isinstance(v, str) and "," in v else patch(v))
                    for k, v in node.items()}
        if isinstance(node, list):
            return [patch(x) for x in node]
        return node
    control_candidate, control_errs = wire_adapter.wire_to_canonical(
        patch(wire_doc), canon, str(SKILL / "schemas"))
    control_errors = validate_artifact.validate(
        control_candidate, canon, base_dir=SKILL / "schemas")

    result(
        "R1 multi-range 'lines' rejected (Fifth exact payload)",
        reproduced=bool(offenders) and bool(line_errors) and not control_errors,
        detail={
            "offending_values_in_real_payload": sorted(offenders),
            "canonical_errors_on_lines": line_errors[:2],
            "control_single_range_validates": not control_errors,
            "control_error_count": len(control_errors),
        })

    # and through the FULL production classifier (exit 0, real payload)
    rd = sandbox_run_dir("r1-classifier")
    job = fake_job(rd, "cross_examination")
    Path(job["output_path"]).write_text(FIFTH_FAILED_WIRE.read_text())
    Path(job["stdout_path"]).write_text("")  # no JSONL: telemetry degraded only
    status, cli = codex_runner.classify_and_finalize(rd, job, 0)
    persisted = json.loads(Path(rd, "logs", "jobs", f"{job['job_id']}.json").read_text())
    result(
        "R1b full classifier: exit-0 real payload -> INVALID_OUTPUT",
        reproduced=(status == "INVALID_OUTPUT" and cli == 6
                    and persisted["artifact_status"] == "SCHEMA_INVALID"),
        detail={"status": status, "cli_exit": cli,
                "artifact_status": persisted["artifact_status"]})


# ---------------------------------------------------------------------------
# R2 — terminal attempts without elapsed_sec (pillar E)
# ---------------------------------------------------------------------------
def repro_r2() -> None:
    rd = sandbox_run_dir("r2-quota")
    job = fake_job(rd, "cross_examination")
    Path(job["stderr_path"]).write_text(
        "codex: error: you've hit your usage limit; try again later\n")
    Path(job["stdout_path"]).write_text("")
    status, cli = codex_runner.classify_and_finalize(rd, job, 1)
    rec = json.loads(Path(rd, "logs", "jobs", f"{job['job_id']}.json").read_text())
    quota_gap = (status == "QUOTA" and rec.get("completed_at")
                 and rec.get("elapsed_sec") is None)

    # COMPLETE control: elapsed IS recorded
    rd2 = sandbox_run_dir("r2-complete")
    job2 = fake_job(rd2, "independent")
    canon_doc = {
        "model": "gpt-5.6-sol",
        "repository_fingerprint_sha256": "0" * 64,
        "audit_summary": "s",
        "findings": [],
    }
    Path(job2["output_path"]).write_text(json.dumps(canon_doc))
    Path(job2["stdout_path"]).write_text(
        '{"type":"thread.started","thread_id":"t1"}\n'
        '{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":5}}\n')
    status2, _ = codex_runner.classify_and_finalize(rd2, job2, 0)
    rec2 = json.loads(Path(rd2, "logs", "jobs", f"{job2['job_id']}.json").read_text())

    result(
        "R2 QUOTA attempt: completed_at set, elapsed_sec missing",
        reproduced=quota_gap,
        detail={"status": status, "completed_at": rec.get("completed_at"),
                "elapsed_sec": rec.get("elapsed_sec", "<absent>"),
                "COMPLETE_control_elapsed_sec": rec2.get("elapsed_sec"),
                "COMPLETE_control_status": status2})


# ---------------------------------------------------------------------------
# R3 — no brief/root/HEAD consistency gate, no environment binding (pillar A0)
# ---------------------------------------------------------------------------
def _git_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(path), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email",
                    "repro@example.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "repro"],
                   check=True)
    (path / "src").mkdir()
    (path / "src" / "app.py").write_text("def f():\n    return 1\n")
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-qm", "repro fixture"],
                   check=True)


def repro_r3() -> None:
    target = TMP / "r3-target-repo"       # the REAL frozen target
    legacy = TMP / "r3-legacy-repo"       # the STALE path the brief talks about
    for p in (target, legacy):
        if p.exists():
            shutil.rmtree(p)
    _git_repo(target)
    _git_repo(legacy)

    brief = TMP / "r3-brief.md"
    brief.write_text(
        "# Release audit brief\n\n"
        f"Repository root: {legacy}\n\n"          # stale/wrong declared root
        "Audit the src/app.py module for release readiness.\n")

    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "CODEX_API_KEY")}

    def last_json(stdout: str):
        # return the LAST parseable JSON object in child stdout (robust to any
        # prepended launcher noise; _emit prints pretty JSON ending the stream)
        dec = json.JSONDecoder()
        last: dict = {}
        idx = stdout.find("{")
        while idx != -1:
            try:
                obj, end = dec.raw_decode(stdout, idx)
                if isinstance(obj, dict):
                    last = obj
                idx = stdout.find("{", idx + end)
            except ValueError:
                idx = stdout.find("{", idx + 1)
        return last

    def last_path(stdout: str):
        for line in reversed(stdout.strip().splitlines()):
            if line.startswith("/"):
                return line.strip()
        return None

    pre = subprocess.run(
        [PY, str(SKILL / "scripts" / "audit_council.py"), "preflight",
         "--repo", str(target), "--brief", str(brief), "--skip-codex"],
        capture_output=True, text=True, env=env, cwd=str(DEV))
    preflight_ok = pre.returncode == 0 and last_json(pre.stdout).get("ok") is True

    init = subprocess.run(
        [PY, str(SKILL / "scripts" / "audit_council.py"), "init-run",
         "--repo", str(target), "--brief", str(brief)],
        capture_output=True, text=True, env=env, cwd=str(DEV))
    init_ok = init.returncode == 0
    run_dir = last_path(init.stdout) if init_ok else None

    manifest = json.loads(Path(run_dir, "00-run-manifest.json").read_text()) \
        if run_dir else {}
    repo_state = json.loads(Path(run_dir, "01-repository-state.json").read_text()) \
        if run_dir else {}
    fingerprint = repo_state.get("fingerprint", {})
    binding_keys = sorted(k for k in fingerprint
                          if k in ("git_dir", "git_common_dir", "worktree_identity",
                                   "detached_head", "brief_root", "expected_head"))

    result(
        "R3 stale brief root accepted; no binding fields (Fifth A0 failure mode)",
        reproduced=preflight_ok and init_ok and not binding_keys,
        detail={
            "preflight_ok_with_wrong_declared_root": preflight_ok,
            "init_run_ok": init_ok,
            "frozen_repo_root": repo_state.get("repo_root"),
            "brief_declared_root": str(legacy),
            "environment_binding_fields_present": binding_keys,
            "fingerprint_fields": sorted(fingerprint.keys()),
        })
    # NOTE (also true in the Fifth run): nothing compares the brief's declared
    # root to the frozen root; the harness stayed on target only by reasoning.


def main() -> int:
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    repro_r1()
    repro_r2()
    repro_r3()
    out = TMP / "phase0-repro-results.json"
    out.write_text(json.dumps(RESULTS, indent=2) + "\n")
    print(f"\nresults written to {out}")
    all_repro = all(r["reproduced"] for r in RESULTS)
    print(f"ALL REPRODUCED: {all_repro}")
    return 0 if all_repro else 1


if __name__ == "__main__":
    sys.exit(main())
