#!/usr/bin/env python3
"""codex_runner.py — Codex subprocess lifecycle manager for the audit-council skill.

Commands:
  start   --run DIR --phase {independent|cross_examination|adjudication}
         [--session ID] [--prompt FILE] [--codex-bin PATH]
  wait    <job-path> [--timeout SEC]
  status  <job-path>
  result  <job-path>
  cancel  <job-path>
  repair  <job-path>

Exit codes (wait): 0 COMPLETE, 1 FAILED, 2 QUOTA, 3 AUTH_ERROR,
6 INVALID_OUTPUT, 7 still-RUNNING-after-timeout.
`start` exits 3 on budget-governor violation (or forbidden repair repeat).

Stdlib only. No secrets are ever read, logged, or persisted.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
import uuid

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import state_store  # noqa: E402  (sibling module; always present at integration)
import validate_artifact  # noqa: E402  (sibling module; always present at integration)

SCHEMAS_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), "schemas")

MODEL = "gpt-5.6-sol"
REASONING_EFFORT = "xhigh"

PHASE_PROMPT_NAME = {
    "independent": "codex-independent",
    "cross_examination": "codex-cross-examination-opus",
    "adjudication": "codex-targeted-adjudication",
}
PHASE_CANON_SCHEMA = {
    "independent": "independent-audit.schema.json",
    "cross_examination": "cross-examination.schema.json",
    "adjudication": "adjudication.schema.json",
}
PHASE_REQUIRED_KEYS = {
    "independent": ("model", "repository_fingerprint_sha256", "findings", "audit_summary"),
    "cross_examination": ("examiner", "examined", "challenges"),
    "adjudication": ("rounds",),
}

# NEVER permitted on any codex invocation (audit is read-only).
FORBIDDEN_FLAGS = ("--last", "--dangerously-bypass-approvals-and-sandbox", "danger-full-access")

QUOTA_PATTERN = re.compile(
    r"rate limit|usage limit|quota|too many requests|plan limit|429", re.IGNORECASE
)
AUTH_PATTERN = re.compile(
    r"\bauth\b|login|log in|401|403|unauthorized|not logged in", re.IGNORECASE
)

REPAIR_INSTRUCTION = (
    "\n\n---\n\nREPAIR INSTRUCTION: Your previous structured response did not "
    "conform to the required JSON output schema (it was missing, empty, or "
    "malformed). Re-emit the COMPLETE corrected result as a single JSON object "
    "conforming exactly to the output schema. Do not include commentary, "
    "markdown fencing, or any text outside the JSON object.\n"
)


# ---------------------------------------------------------------------------
# state_store / validate_artifact interop (duck-typed; contract-tolerant)
# ---------------------------------------------------------------------------

def _first_attr(module, names):
    for n in names:
        fn = getattr(module, n, None)
        if callable(fn):
            return fn
    return None


def load_state(run_dir: str) -> dict:
    fn = _first_attr(state_store, ("load_state", "read_state", "load"))
    if fn is not None:
        return fn(run_dir)
    with open(os.path.join(run_dir, "state.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(run_dir: str, state: dict) -> None:
    fn = _first_attr(state_store, ("save_state", "write_state", "save"))
    if fn is not None:
        fn(run_dir, state)
        return
    atomic_write_json(os.path.join(run_dir, "state.json"), state)


def validate_vs_schema(instance, schema: dict, phase: str):
    """Return (ok, error_message_or_None)."""
    fn = _first_attr(validate_artifact, ("validate", "validate_instance", "validate_json"))
    if fn is not None:
        try:
            result = fn(instance, schema)
        except Exception as exc:  # validator signals failure via exception
            return False, str(exc)
        if isinstance(result, list):
            # validate_artifact.validate returns a list of error strings
            return (not result), ("; ".join(result) or None)
        if result is False:
            return False, "schema validation failed"
        return True, None
    # Minimal structural fallback (pre-integration only).
    if not isinstance(instance, dict):
        return False, "output is not a JSON object"
    missing = [k for k in PHASE_REQUIRED_KEYS.get(phase, ()) if k not in instance]
    if missing:
        return False, "missing required keys: %s" % ", ".join(missing)
    return True, None


# ---------------------------------------------------------------------------
# atomic IO helpers
# ---------------------------------------------------------------------------

def atomic_write_json(path: str, data) -> None:
    tmp = path + ".tmp-%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ---------------------------------------------------------------------------
# codex schema builder: canonical schema -> self-contained run-local copy
# ---------------------------------------------------------------------------

def build_codex_schema(canon_path: str, out_path: str) -> str:
    """Canonical schema -> strict Codex wire schema, via the deterministic
    wire_adapter boundary (v1.0.3): inlines local $refs, drops unsupported
    keywords, makes canonically OPTIONAL properties nullable (null is the
    wire representation of 'absent'), and drops finding.cluster_id
    (clustering is Opus Phase-3 work; the strict wire subset cannot express
    its pattern). Canonical validation after wire_to_canonical remains the
    final authority for every dropped constraint."""
    import wire_adapter
    canon = read_json(canon_path)
    wire = wire_adapter.canonical_to_wire(
        canon, os.path.dirname(os.path.abspath(canon_path)))
    # finding.cluster_id is dropped ONLY inside finding containers; the
    # adjudication rounds[].cluster_id is canonically REQUIRED and must
    # stay representable on the wire (v1.0.3 review F1)
    wire_adapter.drop_wire_property_under(
        wire, "cluster_id", ("findings", "late_findings"))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    atomic_write_json(out_path, wire)
    return out_path


def assert_safe_argv(argv: list) -> None:
    for bad in FORBIDDEN_FLAGS:
        if bad in argv:
            raise SystemExit("refusing to launch codex: forbidden flag %r present" % bad)


def compose_argv(codex_bin: str, phase: str, repo_root: str, schema_path: str,
                 out_path: str, session_id) -> list:
    if session_id:
        argv = [
            codex_bin, "exec", "resume", session_id,
            "--model", MODEL,
            "--json",
            "--output-schema", schema_path,
            "-c", 'model_reasoning_effort="%s"' % REASONING_EFFORT,
            "-c", 'sandbox_mode="read-only"',  # DIVERGENCE D1: resume has no -s flag
            "-o", out_path,
            "-",
        ]
    else:
        argv = [
            codex_bin, "exec",
            "-C", repo_root,
            "--model", MODEL,
            "--sandbox", "read-only",
            "--json",
            "--output-schema", schema_path,
            "-c", 'model_reasoning_effort="%s"' % REASONING_EFFORT,
            "-o", out_path,
            "-",
        ]
    assert_safe_argv(argv)
    return argv


def detect_repo_root(run_dir: str) -> str:
    """Worktree-aware repository discovery via git plumbing ONLY (v2 A0.5/
    A0.6): `git rev-parse --show-toplevel`. Never sniffs for a .git directory
    — a linked/detached worktree keeps a .git FILE, which defeated the old
    directory walk."""
    import env_binding
    try:
        return env_binding.repo_root_from(run_dir)
    except env_binding.EnvironmentBindingError as exc:
        raise SystemExit("cannot detect repo root from %s: %s"
                         % (run_dir, exc.reason))


def _env_gate_errors(run_dir: str) -> list:
    """A0.2/A0.6: refuse to LAUNCH codex when the audit environment is
    inconsistent — zero model calls on environment failure. v1-era runs
    without a binding are ungated (migration path). A v2 run whose binding
    file is missing fails CLOSED (H.4 review F6); the state-pinned digest
    anchors the binding against substitution (R2 NEW-6)."""
    try:
        state = load_state(run_dir)
    except Exception:
        return ["INVALID_AUDIT_ENVIRONMENT:BINDING_UNREADABLE: "
                "run state unreadable"]
    path = os.path.join(run_dir, "01-environment-binding.json")
    if not os.path.isfile(path):
        if state.get("env_binding_digest"):
            return ["INVALID_AUDIT_ENVIRONMENT:BINDING_UNREADABLE: v2 run "
                    "is missing its frozen environment binding file"]
        return []
    import env_binding
    try:
        binding = read_json(path)
    except (ValueError, OSError) as exc:
        return ["INVALID_AUDIT_ENVIRONMENT:BINDING_UNREADABLE: %s" % exc]
    pinned = state.get("env_binding_digest")
    if pinned and binding.get("binding_digest") != pinned:
        return ["INVALID_AUDIT_ENVIRONMENT:BINDING_DIGEST_MISMATCH: "
                "on-disk binding digest does not match the digest pinned "
                "in state.json at freeze time"]
    expected_root = os.path.realpath(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(run_dir)))))
    if binding.get("repo_root_realpath") != expected_root:
        return ["INVALID_AUDIT_ENVIRONMENT:WORKTREE_IDENTITY_CHANGED: run "
                "directory no longer lives inside the frozen audit root"]
    try:
        env_binding.assert_consistent(binding)
    except env_binding.EnvironmentBindingError as exc:
        return ["INVALID_AUDIT_ENVIRONMENT:%s: refusing to launch codex: %s"
                % (exc.reason, exc)]
    return []


# ---------------------------------------------------------------------------
# budget governor (v2 pillar E: configurable via budgets.py; v1 defaults)
# ---------------------------------------------------------------------------

def governor_check(state: dict, phase: str, run_dir: str | None = None) -> None:
    import budgets
    try:
        budgets.check(phase, budgets.load(run_dir), state)
    except budgets.BudgetExceeded as exc:
        raise SystemExit(str(exc))


def bump_stage(state: dict, phase: str) -> dict:
    state.setdefault("codex", {}).setdefault("stage_counts", {})
    state["codex"]["stage_counts"][phase] = state["codex"]["stage_counts"].get(phase, 0) + 1
    return state


# ---------------------------------------------------------------------------
# start / launch
# ---------------------------------------------------------------------------

WRAP_SCRIPT = '"$@"; rc=$?; printf %s "$rc" > "$0"; exit "$rc"'
# The codex process is launched through a minimal /bin/sh wrapper whose only
# job is to persist the real exit code for later `wait` re-attachment
# (a detached Popen's exit code is otherwise unrecoverable). The persisted
# job argv remains the exact codex argv; stdin/stdout/stderr are the run-owned
# files passed to Popen.


def launch(run_dir: str, phase: str, argv: list, prompt_path: str, out_path: str,
           schema_path: str, session_id, job_id: str, extra_job: dict) -> str:
    logs_dir = os.path.join(run_dir, "logs")
    jobs_dir = os.path.join(logs_dir, "jobs")
    os.makedirs(jobs_dir, exist_ok=True)

    # per-job log paths: no attempt may overwrite another attempt's evidence
    stdout_path = os.path.join(logs_dir, "%s.%s.jsonl" % (phase, job_id))
    stderr_path = os.path.join(logs_dir, "%s.%s.stderr.log" % (phase, job_id))
    exit_code_path = os.path.join(jobs_dir, "%s.exitcode" % job_id)
    if os.path.exists(exit_code_path):
        os.remove(exit_code_path)

    stdin_fh = open(prompt_path, "rb")
    stdout_fh = open(stdout_path, "wb")
    stderr_fh = open(stderr_path, "wb")
    try:
        proc = subprocess.Popen(
            ["/bin/sh", "-c", WRAP_SCRIPT, exit_code_path] + argv,
            stdin=stdin_fh,
            stdout=stdout_fh,
            stderr=stderr_fh,
            start_new_session=True,  # own process group for group-signal cancel
            close_fds=True,
        )
    finally:
        stdin_fh.close()
        stdout_fh.close()
        stderr_fh.close()

    job = {
        "job_id": job_id,
        "run_dir": run_dir,
        "phase": phase,
        "pid": proc.pid,
        "argv": argv,  # exact codex argv; contains no secrets
        "session": session_id,
        "resumed": bool(session_id),
        "fresh_or_resumed": "resumed" if session_id else "fresh",
        "model": MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "attempt_number": 1,  # cmd_start overrides via extra_job
        "started_at": utc_now(),
        "started_at_monotonic": time.monotonic(),
        "status": "RUNNING",
        "artifact_status": "NOT_PRODUCED",
        "successful_stage_counted": False,
        "prompt_path": os.path.abspath(prompt_path),
        "output_path": os.path.abspath(out_path),
        "schema_path": os.path.abspath(schema_path),
        "stdout_path": os.path.abspath(stdout_path),
        "stderr_path": os.path.abspath(stderr_path),
        "exit_code_path": os.path.abspath(exit_code_path),
    }
    job.update(extra_job)
    atomic_write_json(os.path.join(jobs_dir, "%s.json" % job_id), job)
    return job


def cmd_sandbox_preflight(args) -> int:
    """Manual entry point for the da27c0 zero-inference preflight."""
    run_dir = os.path.abspath(args.run)
    state = load_state(run_dir)
    repo = state.get("repo_root") or detect_repo_root(run_dir)
    allowed = []
    binding_path = os.path.join(run_dir, "01-environment-binding.json")
    if os.path.isfile(binding_path):
        try:
            allowed = read_json(binding_path).get(
                "allowed_disposable_roots") or []
        except (ValueError, OSError):
            allowed = []
    import codex_sandbox
    result = codex_sandbox.sandbox_preflight(repo, run_dir, allowed)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 3


def _sandbox_preflight_errors(run_dir: str, repo_root: str,
                              allowed_roots: list) -> list:
    """da27c0 hardening: zero-inference viability proof through the exact
    production bubblewrap wrapper, BEFORE any attempt is counted or any
    process launched. Failure = Audit Council environment/harness
    failure (never a model attempt, never a product verdict)."""
    import codex_sandbox
    if not codex_sandbox.bwrap_available():
        return []  # degraded posture (AC_CODEX_BWRAP=0/absent), recorded
        # per job as sandbox.active=false; preflight cannot apply
    result = codex_sandbox.sandbox_preflight(repo_root, run_dir,
                                             allowed_roots)
    if result["ok"]:
        return []
    return ["INVALID_AUDIT_ENVIRONMENT:SANDBOX_PREFLIGHT: "
            + ", ".join(result["failures"])
            + " — refusing to launch (no model attempt consumed); "
              "details: " + json.dumps(result["details"])]


def cmd_start(args) -> int:
    run_dir = os.path.abspath(args.run)
    phase = args.phase
    # da27c0: sandbox preflight BEFORE attempt accounting (a dead
    # execution environment must never consume a paid attempt)
    pre_state = load_state(run_dir)
    pre_repo = pre_state.get("repo_root") or detect_repo_root(run_dir)
    pre_allowed = []
    _binding_path = os.path.join(run_dir, "01-environment-binding.json")
    if os.path.isfile(_binding_path):
        try:
            pre_allowed = read_json(_binding_path).get(
                "allowed_disposable_roots") or []
        except (ValueError, OSError):
            pre_allowed = []
    preflight_errors = _sandbox_preflight_errors(run_dir, pre_repo,
                                                 pre_allowed)
    if preflight_errors:
        print(preflight_errors[0], file=sys.stderr)
        return 3
    state = load_state(run_dir)
    governor_check(state, phase, run_dir)  # SystemExit(3-ish msg) on violation; mapped below
    env_errors = _env_gate_errors(run_dir)
    if env_errors:
        print(env_errors[0], file=sys.stderr)
        return 3

    prompt_path = args.prompt or os.path.join(
        run_dir, "prompts", "%s.md" % PHASE_PROMPT_NAME[phase]
    )
    if prompt_path == "-":
        # rendered prompt piped on stdin; stage it in the run prompts dir
        staged = os.path.join(run_dir, "prompts",
                              "%s.md" % PHASE_PROMPT_NAME[phase])
        tmp = staged + ".tmp-%d" % os.getpid()
        with open(tmp, "wb") as f:
            f.write(sys.stdin.buffer.read())
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, staged)
        prompt_path = staged
    if not os.path.isfile(prompt_path):
        print("error: prompt file not found: %s" % prompt_path, file=sys.stderr)
        return 3

    canon = os.path.join(SCHEMAS_DIR, PHASE_CANON_SCHEMA[phase])
    if not os.path.isfile(canon):
        print("error: canonical schema not found: %s" % canon, file=sys.stderr)
        return 3
    canon_name = PHASE_CANON_SCHEMA[phase]
    codex_name = canon_name.replace(".schema.json", "-codex.schema.json")
    schema_path = build_codex_schema(
        canon, os.path.join(run_dir, "schemas", codex_name)
    )

    repo_root = state.get("repo_root") or detect_repo_root(run_dir)
    codex_bin = args.codex_bin or "codex"

    session_id = args.session
    if session_id is None and phase != "independent":
        session_id = state.get("codex", {}).get("session_id")
    job_id = "%s-%s" % (phase, uuid.uuid4().hex[:8])
    out_path = os.path.join(run_dir, "logs",
                            "%s.%s.final.json" % (phase, job_id))
    argv = compose_argv(codex_bin, phase, repo_root, schema_path, out_path, session_id)
    # A0 confinement spike (docs/A0-CODEX-CONFINEMENT.md): wrap every
    # launch (fresh AND resume) in the bubblewrap OS boundary — repo ro,
    # run dir rw, ~/.codex rw, toolchain+system ro, /tmp tmpfs, authorized
    # fixture roots ro. Reads outside the bind set become OS-BLOCKED.
    # job["codex_argv"] preserves the exact codex argv; job["argv"] is what
    # actually executes. AC_CODEX_BWRAP=0 or missing bwrap → inactive.
    import codex_sandbox
    _allowed_roots = []
    _binding_path = os.path.join(run_dir, "01-environment-binding.json")
    if os.path.isfile(_binding_path):
        try:
            _allowed_roots = read_json(_binding_path).get(
                "allowed_disposable_roots") or []
        except (ValueError, OSError):
            _allowed_roots = []
    try:
        argv_exec, sandbox_active = codex_sandbox.wrap_codex_argv(
            argv, repo_root, run_dir, _allowed_roots)
    except RuntimeError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 3

    attempt_number = 1 + sum(
        1 for j in state.get("codex", {}).get("jobs", [])
        if j.get("phase") == phase)
    job = launch(run_dir, phase, argv_exec, prompt_path, out_path,
                 schema_path,
                 session_id, job_id,
                 {"attempt_number": attempt_number,
                  "codex_argv": argv,  # exact codex argv (unwrapped)
                  "sandbox": {"wrapper": "bwrap" if sandbox_active else None,
                              "active": sandbox_active,
                              "doc": "docs/A0-CODEX-CONFINEMENT.md"}})
    job_path = os.path.join(run_dir, "logs", "jobs", "%s.json" % job_id)

    # stage_counts is bumped only when the stage COMPLETES successfully (in
    # _update_state_after_wait); failed/quota attempts may be retried on
    # resume, bounded by governor_check's per-phase attempts cap
    state.setdefault("codex", {}).setdefault("jobs", [])
    state["codex"]["jobs"].append({
        "job_id": job_id,
        "phase": phase,
        "pid": job["pid"],
        "resumed": job["resumed"],
        "status": "RUNNING",
        "started_at": job["started_at"],
    })
    if session_id and not state["codex"].get("session_id"):
        state["codex"]["session_id"] = session_id
    save_state(run_dir, state)

    print(job_path)
    return 0


# ---------------------------------------------------------------------------
# wait / classification
# ---------------------------------------------------------------------------

def proc_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def tail_text(path: str, nbytes: int = 8192) -> str:
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            if size > nbytes:
                f.seek(-nbytes, os.SEEK_END)
            return f.read().decode("utf-8", "replace")
    except OSError:
        return ""


def read_exit_code(job: dict):
    """Grace-loop read for a process that is already gone: the wrapper may
    still be flushing the exit-code file. Returns int or None."""
    path = job["exit_code_path"]
    for _ in range(20):  # grace: wrapper writes before exiting
        code = read_exit_code_once(job)
        if code is not None:
            return code
        if not proc_alive(job["pid"]):
            time.sleep(0.2)
        else:
            break
    return None


def read_exit_code_once(job: dict):
    """Single non-blocking read of the wrapper-persisted exit code.

    This is the PRIMARY completion signal: a terminated-but-unreaped (zombie)
    process still satisfies os.kill(pid, 0), so process liveness must never
    gate reading this file. Returns int or None."""
    path = job["exit_code_path"]
    if not os.path.isfile(path):
        return None
    try:
        return int(open(path, "r", encoding="utf-8").read().strip())
    except (ValueError, OSError):
        return None


def extract_session_id(jsonl_path: str):
    """Best-effort thread/session id from a JSONL log (None if absent)."""
    try:
        sid, _t, _tok, _deg = parse_jsonl_metrics(jsonl_path)
    except (OSError, ValueError):
        return None
    return sid


def parse_jsonl_metrics(jsonl_path: str):
    """Returns (session_id, turns, tokens, degraded)."""
    session_id = None
    turns = 0
    tokens = {"input_tokens": 0, "cached_input_tokens": 0,
              "output_tokens": 0, "reasoning_output_tokens": 0}
    degraded = False

    def find_usage(obj):
        if isinstance(obj, dict):
            if isinstance(obj.get("input_tokens"), int) or isinstance(obj.get("output_tokens"), int):
                for k in tokens:
                    v = obj.get(k)
                    if isinstance(v, int):
                        tokens[k] += v
                return True
            return any(find_usage(v) for v in obj.values())
        if isinstance(obj, list):
            return any(find_usage(v) for v in obj)
        return False

    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except ValueError:
                    degraded = True
                    continue
                etype = str(ev.get("type") or ev.get("event") or "")
                if "thread.started" in etype:
                    sid = ev.get("thread_id") or ev.get("session_id") or ev.get("id")
                    if isinstance(sid, str) and sid:
                        session_id = sid
                if "turn.completed" in etype:
                    turns += 1
                    found = find_usage(ev)
                    if not found:
                        degraded = True
    except OSError:
        degraded = True
    return session_id, turns, tokens, degraded


def _record_usage(job: dict, parsed=None) -> None:
    """Persist turn/usage telemetry on the job record for EVERY terminal
    outcome (COMPLETE, INVALID_OUTPUT, QUOTA, AUTH_ERROR, FAILED). Usage that
    the JSONL does not expose is recorded as null (unknown), never zero."""
    if parsed is None:
        sid, turns, tokens, degraded = parse_jsonl_metrics(job["stdout_path"])
    else:
        turns, tokens, degraded = parsed
    job["turns"] = turns
    job["degraded_telemetry"] = degraded
    has_usage = turns > 0 or any(v for v in tokens.values())
    job["tokens"] = tokens if has_usage else None  # None = unknown/unavailable
    job["usage_unknown"] = not has_usage


def _finalize_elapsed(job: dict) -> None:
    """Compute elapsed ONCE for ANY terminal classification (v2 pillar E:
    every terminal attempt with started_at and completed_at has a stable
    elapsed). Null ONLY with a documented clock-data reason; repeated waits
    can never inflate it."""
    if job.get("elapsed_sec") is not None:
        return
    mono = job.get("started_at_monotonic")
    if mono is None:
        job["elapsed_sec"] = None
        job["elapsed_unknown_reason"] = "monotonic_start_missing"
        return
    job["elapsed_sec"] = round(
        max(0.0, time.monotonic() - float(mono)), 3)


def rebuild_metrics(run_dir: str) -> dict:
    """Rebuild 99-run-metrics.json from the persisted per-attempt job
    records in logs/jobs/. Naturally idempotent (derived state, dedup by
    job_id) and reconstructible after process exit/restart. Every real
    inference attempt is counted — including INVALID_OUTPUT, QUOTA,
    AUTH_ERROR, FAILED, CANCELLED, and still-RUNNING jobs."""
    jobs_dir = os.path.join(run_dir, "logs", "jobs")
    records = []
    if os.path.isdir(jobs_dir):
        for name in os.listdir(jobs_dir):
            if not name.endswith(".json"):
                continue
            try:
                with open(os.path.join(jobs_dir, name),
                          "r", encoding="utf-8") as fh:
                    records.append(json.load(fh))
            except (ValueError, OSError):
                continue
    seen = set()
    invocations = []
    for rec in sorted(records, key=lambda r: r.get("started_at") or ""):
        jid = rec.get("job_id")
        if jid in seen or not jid:
            continue  # dedup key: stable job identity
        seen.add(jid)
        invocations.append({
            "job_id": jid,
            "phase": rec.get("phase"),
            "attempt_number": rec.get("attempt_number", 1),
            "resumed": bool(rec.get("resumed")),
            "fresh_or_resumed": rec.get("fresh_or_resumed")
            or ("resumed" if rec.get("resumed") else "fresh"),
            "repair_of": rec.get("repair_of"),
            "session_id": rec.get("session_id"),
            "thread_id": rec.get("session_id"),
            "started_at": rec.get("started_at"),
            "completed_at": rec.get("completed_at"),
            "elapsed_sec": rec.get("elapsed_sec"),
            "status": rec.get("status", "RUNNING"),
            "artifact_status": rec.get("artifact_status", "NOT_PRODUCED"),
            "successful_stage_counted":
                bool(rec.get("successful_stage_counted")),
            "tokens": rec.get("tokens"),  # None = unknown/unavailable
            "turns": rec.get("turns", 0),
            "degraded_telemetry": bool(rec.get("degraded_telemetry")),
            "model": rec.get("model", MODEL),
            "reasoning_effort": rec.get("reasoning_effort",
                                        REASONING_EFFORT),
        })
    usage_known = [i for i in invocations if i["tokens"] is not None]
    agg = {
        "invocation_count": len(invocations),
        "fresh_count": sum(1 for i in invocations if not i["resumed"]),
        "resumed_count": sum(1 for i in invocations if i["resumed"]),
        "turns_total": sum(i["turns"] for i in invocations),
        "elapsed_sec_total": round(sum(i["elapsed_sec"] or 0.0
                                       for i in invocations), 3),
        "usage_unknown_count": sum(1 for i in invocations
                                   if i["tokens"] is None),
        "degraded_telemetry_count": sum(
            1 for i in invocations if i["degraded_telemetry"]),
        "successful_stage_counted_total": sum(
            1 for i in invocations if i["successful_stage_counted"]),
        "tokens": {k: sum((i["tokens"] or {}).get(k, 0)
                          for i in usage_known)
                   for k in ("input_tokens", "cached_input_tokens",
                             "output_tokens", "reasoning_output_tokens")},
    }
    metrics = {
        "invocations": invocations,
        "aggregates": agg,
        "budget_omissions": _load_budget_omissions(run_dir),
        "note": "rebuilt from logs/jobs/*.json; usage null = unknown",
    }
    atomic_write_json(os.path.join(run_dir, "99-run-metrics.json"), metrics)
    return metrics


def _load_budget_omissions(run_dir: str) -> list[dict]:
    """Explicit budget-driven omissions (v2 pillar E); re-derived with the
    metrics so the record is idempotent and restart-reconstructible."""
    try:
        import budgets
        return budgets.load_omissions(run_dir)
    except Exception:
        return []


def _update_state_after_wait(run_dir: str, job: dict, session_id) -> None:
    state = load_state(run_dir)
    codex = state.setdefault("codex", {})
    if session_id:
        codex["session_id"] = session_id
    if job.get("status") == "COMPLETE":
        # budget governor counts successful stages; failures/quota may retry
        counts = codex.setdefault("stage_counts", {})
        phase = job["phase"]
        counts[phase] = min(1, counts.get(phase, 0) + 1)
    for entry in codex.get("jobs", []):
        if entry.get("job_id") == job["job_id"]:
            entry["status"] = job["status"]
            if session_id:
                entry["session_id"] = session_id
    save_state(run_dir, state)


def classify_and_finalize(run_dir: str, job: dict, exit_code) -> tuple:
    """Returns (status, exit_code_for_cli)."""
    phase = job["phase"]
    if exit_code is None or exit_code != 0:
        haystack = tail_text(job["stderr_path"]) + "\n" + tail_text(job["stdout_path"])
        if QUOTA_PATTERN.search(haystack):
            status, cli = "QUOTA", 2
        elif AUTH_PATTERN.search(haystack):
            status, cli = "AUTH_ERROR", 3
        else:
            status, cli = "FAILED", 1
        job["status"] = status
        job["exit_code"] = exit_code
        job["completed_at"] = utc_now()
        _finalize_elapsed(job)  # every terminal attempt has stable elapsed
        job["artifact_status"] = "NOT_PRODUCED"
        _record_usage(job)  # a paid attempt's usage must never vanish
        atomic_write_json(os.path.join(run_dir, "logs", "jobs", "%s.json" % job["job_id"]), job)
        rebuild_metrics(run_dir)
        # persist any thread id already emitted before the failure so a later
        # resume can still target the explicit original session (spec §8)
        _update_state_after_wait(run_dir, job, extract_session_id(job["stdout_path"]))
        return status, cli

    # exit 0: output must exist, parse, wire->canonical normalize, validate
    out_path = job["output_path"]
    raw_preserved = True
    problem = None
    artifact_status = "NOT_PRODUCED"
    instance = None
    if not os.path.isfile(out_path) or os.path.getsize(out_path) == 0:
        problem = "final output file missing or empty: %s" % out_path
    else:
        try:
            instance = read_json(out_path)
            artifact_status = "WIRE_VALID"  # produced + parses as JSON
        except ValueError as exc:
            problem = "final output is not valid JSON: %s" % exc
        raw_preserved = os.path.isfile(out_path)
    if problem is None:
        # deterministic adapter boundary (v1.0.3): wire instance + canonical
        # schema -> canonical candidate. Canonically OPTIONAL properties with
        # wire null are omitted; REQUIRED non-nullable nulls fail closed.
        import wire_adapter
        canon_path = os.path.join(SCHEMAS_DIR, PHASE_CANON_SCHEMA[phase])
        if not os.path.isfile(canon_path):
            # fail-closed: never validate against the weaker WIRE schema
            problem = "canonical schema missing: %s" % canon_path
            canon_schema = None
        else:
            canon_schema = read_json(canon_path)
        if problem is None:
            instance, norm_errors = wire_adapter.wire_to_canonical(
                instance, canon_schema, SCHEMAS_DIR)
        if norm_errors:
            problem = "wire->canonical normalization failed: %s" % \
                "; ".join(norm_errors)
            artifact_status = "CANONICAL_INVALID"
    if problem is None and canon_schema is not None:
        # validate the CANONICAL CANDIDATE against the ORIGINAL canonical
        # schema — the final authority for every constraint the wire format
        # could not express (patterns, minLength, ...)
        ok, err = validate_vs_schema(instance, canon_schema, phase)
        if not ok:
            problem = "final output failed schema validation: %s" % err
            artifact_status = "SCHEMA_INVALID"
    if problem is None:
        # semantic repository-identity invariant (v1.0.1 Issue 1): a model
        # claiming a different repository fingerprint than the frozen run
        # must not be classified COMPLETE; raw output stays preserved above
        claimed = instance.get("repository_fingerprint_sha256") \
            if isinstance(instance, dict) else None
        if claimed is not None:
            try:
                frozen = load_state(run_dir).get("repo_fingerprint_sha256")
            except Exception:
                frozen = None
            if claimed != frozen:
                problem = ("INVALID_ARTIFACT: output claims repository "
                           "fingerprint %r but the frozen run fingerprint "
                           "is %r" % (claimed, frozen))
                artifact_status = "FINGERPRINT_MISMATCH"
    if problem is None:
        # canonical artifact: persisted SEPARATELY from the raw wire output
        # so neither leaks into the other; `result` serves this copy
        atomic_write_json(out_path + ".canonical.json", instance)
        artifact_status = "CANONICAL_VALID"
    if problem is not None:
        # INVALID_OUTPUT: raw output preserved untouched for diagnosis. The
        # session id from the JSONL log is still captured so the one-shot
        # repair can resume the same codex thread.
        session_id, _turns, _tok, _deg = parse_jsonl_metrics(job["stdout_path"])
        job["status"] = "INVALID_OUTPUT"
        job["exit_code"] = exit_code
        job["error"] = problem
        job["raw_output_preserved"] = raw_preserved
        job["artifact_status"] = artifact_status
        _record_usage(job)  # inference happened; usage must be accounted
        if session_id:
            job["session_id"] = session_id
        job["completed_at"] = utc_now()
        _finalize_elapsed(job)  # invalid output still consumed wall time
        atomic_write_json(os.path.join(run_dir, "logs", "jobs", "%s.json" % job["job_id"]), job)
        rebuild_metrics(run_dir)
        _update_state_after_wait(run_dir, job, session_id or None)
        return "INVALID_OUTPUT", 6

    session_id, turns, tokens, degraded = parse_jsonl_metrics(job["stdout_path"])
    _finalize_elapsed(job)  # computed once; repeated waits cannot inflate it
    job["status"] = "COMPLETE"
    job["exit_code"] = exit_code
    job["session_id"] = session_id
    job["completed_at"] = utc_now()
    job["artifact_status"] = artifact_status
    job["successful_stage_counted"] = True  # via _update_state_after_wait
    _record_usage(job, (turns, tokens, degraded))
    atomic_write_json(os.path.join(run_dir, "logs", "jobs", "%s.json" % job["job_id"]), job)
    rebuild_metrics(run_dir)
    _update_state_after_wait(run_dir, job, session_id)
    return "COMPLETE", 0


def _poll_interval() -> float:
    """Production polls every 2s; tests may set CODEX_RUNNER_POLL_INTERVAL
    to a fraction of a second to avoid real-time sleeps. Always bounded."""
    try:
        poll = float(os.environ.get("CODEX_RUNNER_POLL_INTERVAL", "2.0"))
    except ValueError:
        poll = 2.0
    return min(max(poll, 0.01), 2.0)


# terminal status -> CLI exit code (for idempotent re-wait/re-status)
_TERMINAL_CLI = {"COMPLETE": 0, "INVALID_OUTPUT": 6, "QUOTA": 2,
                 "AUTH_ERROR": 3, "FAILED": 1, "CANCELLED": 0}


def cmd_wait(args) -> int:
    job = read_json(args.job)
    run_dir = job["run_dir"]
    if job.get("status") in _TERMINAL_CLI:
        # already finalized: idempotent re-wait must never relabel the job
        # (e.g. CANCELLED -> FAILED) nor inflate elapsed/counts
        print(json.dumps({"job_id": job["job_id"], "status": job["status"],
                          "exit_code": job.get("exit_code")}))
        return _TERMINAL_CLI[job["status"]]
    deadline = time.monotonic() + args.timeout
    poll = _poll_interval()
    while True:
        # PRIMARY completion signal: the wrapper-persisted exit-code file.
        # A zombie process still "passes" os.kill(pid, 0), so liveness must
        # never gate this read; an exit code here means FINISHED, not RUNNING.
        exit_code = read_exit_code_once(job)
        if exit_code is not None:
            status, cli = classify_and_finalize(run_dir, job, exit_code)
            print(json.dumps({"job_id": job["job_id"], "status": status,
                              "exit_code": exit_code}))
            return cli
        # SECONDARY signal: process fully gone (reaped) — allow the existing
        # short grace period for an in-flight exit-code write, then finalize
        # (a missing code classifies via the failure paths).
        if not proc_alive(job["pid"]):
            exit_code = read_exit_code(job)
            status, cli = classify_and_finalize(run_dir, job, exit_code)
            print(json.dumps({"job_id": job["job_id"], "status": status,
                              "exit_code": exit_code}))
            return cli
        if time.monotonic() >= deadline:
            print(json.dumps({"job_id": job["job_id"], "status": "RUNNING",
                              "pid": job["pid"]}))
            return 7
        time.sleep(min(poll, max(0.01, deadline - time.monotonic())))


# ---------------------------------------------------------------------------
# status / result / cancel / repair
# ---------------------------------------------------------------------------

def cmd_status(args) -> int:
    job = read_json(args.job)
    # idempotent metrics reconstruction point (derived from job records,
    # so repeated status calls can never double-count)
    if job.get("status") != "RUNNING":
        rebuild_metrics(job["run_dir"])
    print(json.dumps({**job, "alive": proc_alive(job["pid"])}, indent=2))
    return 0


def cmd_result(args) -> int:
    job = read_json(args.job)
    # serve the CANONICAL (wire->canonical normalized) artifact when present;
    # the raw wire output stays separately preserved at output_path itself
    canonical = job["output_path"] + ".canonical.json"
    path = canonical if os.path.isfile(canonical) else job["output_path"]
    if not os.path.isfile(path):
        print("error: no final output at %s" % path, file=sys.stderr)
        return 6
    try:
        print(json.dumps(read_json(path), indent=2))
        return 0
    except ValueError as exc:
        print("error: final output not valid JSON: %s" % exc, file=sys.stderr)
        return 6


def cmd_cancel(args) -> int:
    job = read_json(args.job)
    if job.get("status") in _TERMINAL_CLI:
        # never overwrite a terminal record (e.g. COMPLETE -> CANCELLED)
        print(json.dumps({"job_id": job["job_id"], "status": job["status"],
                          "note": "already terminal; not modified"}))
        return 0
    pid = job["pid"]
    try:
        pgid = os.getpgid(pid)
        os.killpg(pgid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError, OSError):
        pass
    for _ in range(25):  # up to 5s
        # wrapper-persisted exit code means the process tree is finished
        # (a zombie still "passes" proc_alive); stop signaling a dead process
        if read_exit_code_once(job) is not None or not proc_alive(pid):
            break
        time.sleep(0.2)
    if proc_alive(pid):
        try:
            os.killpg(os.getpgid(pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            pass
    job["status"] = "CANCELLED"
    job["completed_at"] = utc_now()
    _finalize_elapsed(job)  # a cancelled attempt still consumed wall time
    _record_usage(job)  # a cancelled attempt may still have consumed a turn
    atomic_write_json(os.path.join(job["run_dir"], "logs", "jobs",
                                   "%s.json" % job["job_id"]), job)
    rebuild_metrics(job["run_dir"])  # after the job record is persisted
    _update_state_after_wait(job["run_dir"], job, None)
    print(json.dumps({"job_id": job["job_id"], "status": "CANCELLED"}))
    return 0


def cmd_repair(args) -> int:
    """One-shot schema-repair: resume the SAME codex session with a repair
    instruction. Reuses the SAME budget stage (does not bump stage_counts);
    allowed at most once per phase. H.4 review F4: repair CONSUMES an
    attempt under the same governor caps and is refused on COMPLETE jobs —
    it may never become a fourth paid attempt past the cap."""
    job = read_json(args.job)
    run_dir = job["run_dir"]
    phase = job["phase"]
    state = load_state(run_dir)

    # da27c0: identical sandbox preflight for repair — same valid
    # execution environment as fresh/resume, before attempt accounting
    pre_repo = state.get("repo_root") or detect_repo_root(run_dir)
    pre_allowed = []
    _binding_path = os.path.join(run_dir, "01-environment-binding.json")
    if os.path.isfile(_binding_path):
        try:
            pre_allowed = read_json(_binding_path).get(
                "allowed_disposable_roots") or []
        except (ValueError, OSError):
            pre_allowed = []
    preflight_errors = _sandbox_preflight_errors(run_dir, pre_repo,
                                                 pre_allowed)
    if preflight_errors:
        print(preflight_errors[0], file=sys.stderr)
        return 3

    if job.get("status") == "COMPLETE":
        print("error: repair is not permitted on a completed job (the "
              "stage is already successfully counted)",
              file=sys.stderr)
        return 3
    governor_check(state, phase, run_dir)

    for entry in state.get("codex", {}).get("jobs", []):
        if entry.get("phase") == phase and entry.get("repair_used"):
            print("error: repair already used for phase %s (max 1)" % phase, file=sys.stderr)
            return 3

    session_id = job.get("session") or job.get("session_id") \
        or state.get("codex", {}).get("session_id")
    if not session_id:
        print("error: no codex session id available; cannot resume for repair", file=sys.stderr)
        return 3

    base_prompt = job["prompt_path"]
    repair_prompt = os.path.join(run_dir, "prompts", "%s.repair.md" % phase)
    with open(base_prompt, "r", encoding="utf-8") as f:
        body = f.read()
    with open(repair_prompt + ".tmp-%d" % os.getpid(), "w", encoding="utf-8") as f:
        f.write(body + REPAIR_INSTRUCTION)
        f.flush()
        os.fsync(f.fileno())
    os.replace(repair_prompt + ".tmp-%d" % os.getpid(), repair_prompt)

    job_id = "%s-repair-%s" % (phase, uuid.uuid4().hex[:8])
    out_path = os.path.join(run_dir, "logs",
                            "%s.%s.final.json" % (phase, job_id))
    attempt_number = 1 + sum(
        1 for j in state.get("codex", {}).get("jobs", [])
        if j.get("phase") == phase)
    # v2: job["argv"] may be the WRAPPED (bwrap) invocation; the exact
    # codex argv lives in job["codex_argv"]. Repair re-wraps identically.
    codex_bin = (job.get("codex_argv") or job.get("argv") or ["codex"])[0]
    base_argv = compose_argv(codex_bin, phase, "", job["schema_path"],
                             out_path, session_id)
    import codex_sandbox
    _binding_path = os.path.join(run_dir, "01-environment-binding.json")
    _allowed_roots = []
    if os.path.isfile(_binding_path):
        try:
            _allowed_roots = read_json(_binding_path).get(
                "allowed_disposable_roots") or []
        except (ValueError, OSError):
            _allowed_roots = []
    _repo_root = state.get("repo_root") or detect_repo_root(run_dir)
    try:
        argv_exec, sandbox_active = codex_sandbox.wrap_codex_argv(
            base_argv, _repo_root, run_dir, _allowed_roots)
    except RuntimeError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 3
    new_job = launch(run_dir, phase, argv_exec,
                     repair_prompt, out_path, job["schema_path"], session_id, job_id,
                     {"repair_of": job["job_id"], "repair": True,
                      "attempt_number": attempt_number,
                      "codex_argv": base_argv,
                      "sandbox": {"wrapper": "bwrap" if sandbox_active else None,
                                  "active": sandbox_active,
                                  "doc": "docs/A0-CODEX-CONFINEMENT.md"}})
    job_path = os.path.join(run_dir, "logs", "jobs", "%s.json" % job_id)

    # same stage: no stage_counts bump; mark original stage entry as repaired
    for entry in state.get("codex", {}).get("jobs", []):
        if entry.get("job_id") == job["job_id"]:
            entry["repair_used"] = True
        if entry.get("phase") == phase:
            entry.setdefault("repair_used", False)
    state["codex"]["jobs"].append({
        "job_id": job_id,
        "phase": phase,
        "pid": new_job["pid"],
        "resumed": True,
        "status": "RUNNING",
        "started_at": new_job["started_at"],
        "repair": True,
        "repair_of": job["job_id"],
    })
    # guard: exactly one repair_used flag for this phase
    flags = [e for e in state["codex"]["jobs"] if e.get("phase") == phase and e.get("repair_used")]
    for e in flags[1:]:
        e.pop("repair_used", None)
    save_state(run_dir, state)
    print(job_path)
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("sandbox-preflight")
    p.add_argument("--run", required=True,
                   help="zero-inference viability proof of the production "
                        "bwrap environment (no model attempt consumed)")
    p.set_defaults(func=cmd_sandbox_preflight)

    p = sub.add_parser("start")
    p.add_argument("--run", required=True)
    p.add_argument("--phase", required=True,
                   choices=["independent", "cross_examination", "adjudication"])
    p.add_argument("--session", default=None)
    p.add_argument("--prompt", default=None)
    p.add_argument("--codex-bin", default=None)
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("wait")
    p.add_argument("job")
    p.add_argument("--timeout", type=int, default=540)
    p.set_defaults(func=cmd_wait)

    p = sub.add_parser("status")
    p.add_argument("job")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("result")
    p.add_argument("job")
    p.set_defaults(func=cmd_result)

    p = sub.add_parser("cancel")
    p.add_argument("job")
    p.set_defaults(func=cmd_cancel)

    p = sub.add_parser("repair")
    p.add_argument("job")
    p.set_defaults(func=cmd_repair)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except SystemExit as exc:
        # governor violations must exit 3 with a message
        if exc.code and isinstance(exc.code, str) and exc.code.startswith("budget governor"):
            print(exc.code, file=sys.stderr)
            return 3
        raise
    except FileNotFoundError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
