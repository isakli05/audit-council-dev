#!/usr/bin/env python3
"""Audit Council run lifecycle CLI.

Python 3.14, stdlib only. Never mutates the audited repository outside
`audit-output/audit-council/<run-id>/`. Never prints env var values.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import env_binding
import repo_fingerprint
import state_store
import validate_artifact
from state_store import StateError, atomic_write_bytes, atomic_write_json, \
    load_json, sha256_file, utc_now_iso

SCRIPTS_DIR = Path(__file__).resolve().parent
SCHEMAS_DIR = SCRIPTS_DIR.parent / "schemas"

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_STALE = 4
EXIT_WRITE_GUARD = 5
EXIT_CHECKSUM = 8
EXIT_INVALID_ARTIFACT = 9

# canonical artifacts that claim repository identity and must semantically
# match the frozen run fingerprint (top-level or nested field path)
FINGERPRINT_FIELDS: dict[str, tuple[str, ...]] = {
    "02-audit-contract.json": ("target_repository", "fingerprint_sha256"),
    "10-opus-independent.json": ("repository_fingerprint_sha256",),
    "20-codex-independent.json": ("repository_fingerprint_sha256",),
    "90-final-findings.json": ("repository_fingerprint_sha256",),
}

# artifact basename -> schema filename (None = structural check only)
ARTIFACT_SCHEMAS: dict[str, str | None] = {
    "02-audit-contract.json": "audit-contract.schema.json",
    "10-opus-independent.json": "independent-audit.schema.json",
    "20-codex-independent.json": "independent-audit.schema.json",
    "30-normalized-findings.json": None,
    "31-opus-cross-examination.json": "cross-examination.schema.json",
    "32-codex-cross-examination.json": "cross-examination.schema.json",
    "40-disagreement-ledger.json": "disagreement-ledger.schema.json",
    "50-targeted-adjudication.json": "adjudication.schema.json",
    "90-final-findings.json": "final-findings.schema.json",
    "99-run-metrics.json": None,
}

# target phase -> artifact that justifies the transition
PHASE_ARTIFACT: dict[str, str] = {
    "CONTRACT_FROZEN": "02-audit-contract.json",
    "OPUS_INDEPENDENT_COMPLETE": "10-opus-independent.json",
    "CODEX_INDEPENDENT_COMPLETE": "20-codex-independent.json",
    "NORMALIZED": "30-normalized-findings.json",
    "OPUS_CROSS_EXAM_COMPLETE": "31-opus-cross-examination.json",
    "CODEX_CROSS_EXAM_COMPLETE": "32-codex-cross-examination.json",
    "LEDGER_COMPLETE": "40-disagreement-ledger.json",
    "ADJUDICATION_COMPLETE": "50-targeted-adjudication.json",
    "FINALIZED": "90-final-findings.json",
    "COMPLETE": "99-run-metrics.json",
}

CODEX_EXEC_REQUIRED_FLAGS = ("--model", "--sandbox", "--json",
                             "--output-schema", "--output-last-message",
                             "-C", "-c")

# v2 (A0.6): environment trust layer --------------------------------------
ENV_BINDING_NAME = "01-environment-binding.json"
EXIT_ENV = 10
# phases that authorize frontier-model inference: the environment gate must
# pass immediately BEFORE any of these may advance or launch
INFERENCE_PHASES = {
    "OPUS_INDEPENDENT_COMPLETE",
    "CODEX_INDEPENDENT_COMPLETE",
    "OPUS_CROSS_EXAM_COMPLETE",
    "CODEX_CROSS_EXAM_COMPLETE",
    "ADJUDICATION_COMPLETE",
}

INSTRUCTION_FILE_NAMES = ("CLAUDE.md", "AGENTS.md")
README_GLOB = "README*"


def _emit(doc: Any) -> None:
    print(json.dumps(doc, indent=2, ensure_ascii=False))


def _fail(msg: str) -> None:
    _emit({"ok": False, "error": msg})


# ---------------------------------------------------------------------------
# environment binding gate (v2 A0.2/A0.6)
# ---------------------------------------------------------------------------
def parse_brief_target(text: str) -> dict | None:
    """Extract the explicit brief target metadata block — the ONLY brief text
    that ever becomes execution authority. A fenced ```json block shaped
    {"target": {"repository_root": ..., "expected_head": ...}}. All other
    brief prose — including absolute paths — is inert evidence text."""
    for m in re.finditer(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL):
        try:
            doc = json.loads(m.group(1))
        except ValueError:
            continue
        if isinstance(doc, dict) and isinstance(doc.get("target"), dict):
            t = doc["target"]
            root = t.get("repository_root")
            head = t.get("expected_head")
            return {
                "declared_repository_root":
                    root if isinstance(root, str) else None,
                "declared_expected_head":
                    head if isinstance(head, str) else None,
            }
    return None


def _active_runs_dir() -> str:
    return os.path.join(env_binding.cache_root(), "active-runs")


def _prune_dead_active_runs() -> int:
    """R5 NEW-6: registrations whose run dir no longer exists are dead —
    remove them so the path-guard hook never goes fail-closed-for-nothing.
    Called before every registration; returns the number pruned."""
    d = _active_runs_dir()
    if not os.path.isdir(d):
        return 0
    pruned = 0
    for name in os.listdir(d):
        entry = os.path.join(d, name)
        try:
            with open(entry, "r", encoding="utf-8") as fh:
                run_dir = fh.read().strip().splitlines()[0].strip()
        except (OSError, IndexError):
            run_dir = ""
        if not run_dir or not os.path.isdir(run_dir):
            try:
                os.unlink(entry)
                pruned += 1
            except OSError:
                pass
    return pruned


def _register_active_run(run_id: str, run_dir: str,
                         pinned_digest: str | None = None) -> None:
    d = _active_runs_dir()
    os.makedirs(d, exist_ok=True)
    _prune_dead_active_runs()
    # R3-N3: line 2 pins the binding digest OUTSIDE the frozen root so a
    # confined session cannot rewrite the hook's policy source
    payload = os.path.abspath(run_dir)
    if pinned_digest:
        payload += "\n" + pinned_digest
    atomic_write_bytes(os.path.join(d, run_id), payload.encode("utf-8"))


def _unregister_active_run(run_id: str) -> None:
    try:
        os.unlink(os.path.join(_active_runs_dir(), run_id))
    except OSError:
        pass


def _env_gate_errors(run_dir: str) -> list[str]:
    """A0.2 consistency gate: empty list = environment consistent. A v1-era
    run (no env_binding_digest in state) is ungated (migration path). A v2
    run whose binding file is MISSING fails closed (H.4 review F6: binding
    deletion must not fail the gate open)."""
    path = os.path.join(run_dir, ENV_BINDING_NAME)
    try:
        state = state_store.load_state(run_dir)
    except StateError as exc:
        return [f"INVALID_AUDIT_ENVIRONMENT:BINDING_UNREADABLE: {exc}"]
    if not os.path.isfile(path):
        if state.get("env_binding_digest"):
            return ["INVALID_AUDIT_ENVIRONMENT:BINDING_UNREADABLE: v2 run "
                    "is missing its frozen environment binding file"]
        return []  # v1-era run without a binding: gate inert
    try:
        binding = load_json(path)
    except (json.JSONDecodeError, OSError) as exc:
        return [f"INVALID_AUDIT_ENVIRONMENT:BINDING_UNREADABLE: {exc}"]
    # R2 NEW-6: the state-pinned digest anchors the binding — a substituted
    # (otherwise valid) binding from ANOTHER run must not pass the gate
    pinned = state.get("env_binding_digest")
    if pinned and binding.get("binding_digest") != pinned:
        return ["INVALID_AUDIT_ENVIRONMENT:BINDING_DIGEST_MISMATCH: on-disk "
                "binding digest does not match the digest pinned in "
                "state.json at freeze time"]
    # location check: the run dir must live inside the root its binding
    # froze (a copied/stolen run dir in an alternate same-HEAD worktree
    # must not verify)
    expected_root = os.path.realpath(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(run_dir)))))
    if binding.get("repo_root_realpath") != expected_root:
        return ["INVALID_AUDIT_ENVIRONMENT:WORKTREE_IDENTITY_CHANGED: run "
                "directory no longer lives inside the frozen audit root "
                f"({binding.get('repo_root_realpath')!r})"]
    try:
        env_binding.assert_consistent(binding)
    except env_binding.EnvironmentBindingError as exc:
        return [f"INVALID_AUDIT_ENVIRONMENT:{exc.reason}: {exc}"]
    return []


def _env_fail(run_dir: str, errors: list[str]) -> int:
    try:
        state_store.set_completeness(
            run_dir, "INVALID_AUDIT_ENVIRONMENT", failure_reason=errors[0])
    except StateError:
        pass
    _fail(errors[0])
    return EXIT_ENV


# ---------------------------------------------------------------------------
# preflight
# ---------------------------------------------------------------------------
def _preflight_codex(failures: list[dict[str, str]]) -> None:
    if shutil.which("codex") is None:
        failures.append({"check": "codex-on-path",
                         "reason": "`codex` executable not found on PATH"})
        return
    try:
        proc = subprocess.run(["codex", "login", "status"], capture_output=True,
                              text=True, timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        failures.append({"check": "codex-login-status",
                         "reason": f"codex login status failed to run: {exc}"})
        proc = None
    if proc is not None:
        out = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode != 0:
            failures.append({"check": "codex-login-status",
                             "reason": "`codex login status` exited non-zero"})
        elif "API key" in out or "api key" in out.lower():
            failures.append({
                "check": "codex-login-status",
                "reason": "codex login status indicates API-key mode; "
                          "ChatGPT-subscription login is required"})
    try:
        help_proc = subprocess.run(["codex", "exec", "--help"],
                                   capture_output=True, text=True, timeout=60,
                                   check=False)
    except (OSError, subprocess.TimeoutExpired):
        help_proc = None
    if help_proc is None:
        failures.append({"check": "codex-exec-flags",
                         "reason": "`codex exec --help` failed to run"})
    else:
        text = (help_proc.stdout or "") + (help_proc.stderr or "")
        missing = [f for f in CODEX_EXEC_REQUIRED_FLAGS if f not in text]
        if missing:
            failures.append({"check": "codex-exec-flags",
                             "reason": f"`codex exec --help` missing required "
                                       f"flags: {missing}"})
    # best-effort model resolvability check (non-inference): the runner always
    # passes --model explicitly, so this is advisory unless clearly wrong
    models_cache = Path.home() / ".codex" / "models_cache.json"
    if models_cache.is_file():
        try:
            if "gpt-5.6-sol" not in models_cache.read_text(errors="replace"):
                failures.append({
                    "check": "codex-model",
                    "reason": "gpt-5.6-sol not found in codex models cache"})
        except OSError:
            pass


def cmd_preflight(args: argparse.Namespace) -> int:
    failures: list[dict[str, str]] = []
    repo = os.path.abspath(args.repo)

    if repo_fingerprint._is_git_worktree(repo) is False:
        failures.append({"check": "git-repo",
                         "reason": f"{repo} is not a git worktree"})
    else:
        head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=False)
        if head.returncode != 0:
            failures.append({"check": "git-repo",
                             "reason": "git repository has no HEAD commit"})

    brief = args.brief
    if getattr(args, "brief_inline", False):
        if brief:
            failures.append({"check": "brief-args",
                             "reason": "pass either --brief FILE or "
                                       "--brief-inline, not both"})
        else:
            data = sys.stdin.buffer.read()
            if not data.strip():
                failures.append({"check": "brief-nonempty",
                                 "reason": "inline brief is empty"})
    elif not brief:
        failures.append({"check": "brief-args",
                         "reason": "a brief is required: pass --brief FILE "
                                   "or --brief-inline"})
    elif not os.path.isfile(brief):
        failures.append({"check": "brief-exists",
                         "reason": f"brief {brief!r} does not exist "
                                   f"(use --brief-inline to pass brief text "
                                   f"on stdin)"})
    else:
        try:
            with open(brief, "rb") as fh:
                data = fh.read()
        except OSError as exc:
            failures.append({"check": "brief-readable",
                             "reason": f"brief not readable: {exc}"})
        else:
            if not data.strip():
                failures.append({"check": "brief-nonempty",
                                 "reason": "brief is empty"})

    out_parent = os.path.join(repo, "audit-output")
    try:
        os.makedirs(out_parent, exist_ok=True)
    except OSError as exc:
        failures.append({"check": "output-creatable",
                         "reason": f"cannot create {out_parent}: {exc}"})

    # Auth checks: presence booleans only — values are never read or printed.
    if "ANTHROPIC_API_KEY" in os.environ:
        failures.append({
            "check": "claude-auth-mode",
            "reason": "ANTHROPIC_API_KEY is present in the environment; "
                      "unexpected PAYG Claude billing mode "
                      "(INVALID_AUDIT_INPUT)"})
    for var in ("OPENAI_API_KEY", "CODEX_API_KEY"):
        if var in os.environ:
            failures.append({
                "check": "codex-auth-mode",
                "reason": f"{var} is present in the environment; this could "
                          f"silently select PAYG for Codex"})

    if not args.skip_codex:
        _preflight_codex(failures)

    _emit({"ok": not failures, "failures": failures})
    return EXIT_OK if not failures else EXIT_FAIL


# ---------------------------------------------------------------------------
# init-run
# ---------------------------------------------------------------------------
def _scan_instruction_files(repo: str) -> list[dict[str, Any]]:
    """Names only; flagged untrusted (prompt-injection surface, spec §31)."""
    found: list[dict[str, Any]] = []
    roots = [repo] + [os.path.join(repo, d) for d in sorted(
        e for e in os.listdir(repo)
        if os.path.isdir(os.path.join(repo, e))
        and not e.startswith("."))] if os.path.isdir(repo) else [repo]
    for root in roots:
        for name in (*INSTRUCTION_FILE_NAMES, ".codex"):
            if os.path.exists(os.path.join(root, name)):
                found.append({
                    "name": name,
                    "location": os.path.relpath(root, repo) or ".",
                    "untrusted": True,
                })
        import glob as _glob
        for match in _glob.glob(os.path.join(root, README_GLOB)):
            found.append({
                "name": os.path.basename(match),
                "location": os.path.relpath(root, repo) or ".",
                "untrusted": True,
            })
    # dedupe by (name, location)
    seen: set[tuple[str, str]] = set()
    out = []
    for e in found:
        key = (e["name"], e["location"])
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


def cmd_init_run(args: argparse.Namespace) -> int:
    repo = os.path.abspath(args.repo)
    if not repo_fingerprint._is_git_worktree(repo):
        _fail(f"{repo} is not a git worktree")
        return EXIT_FAIL
    brief_source = "file"
    inline_content = None
    if getattr(args, "brief_inline", False):
        if args.brief:
            _fail("pass either --brief FILE or --brief-inline, not both")
            return EXIT_FAIL
        brief_source = "inline"
        # read and validate BEFORE creating anything, so a bad inline brief
        # leaves no stray run-dir skeleton behind
        inline_content = sys.stdin.buffer.read()
        if not inline_content.strip():
            _fail("inline brief is empty")
            return EXIT_FAIL
    else:
        if not args.brief:
            _fail("a brief is required: pass --brief FILE or --brief-inline")
            return EXIT_FAIL
        if not os.path.isfile(args.brief) or os.path.getsize(args.brief) == 0:
            # never silently reinterpret a missing path as inline text
            _fail(f"brief {args.brief!r} missing or empty (use --brief-inline "
                  f"to pass brief text on stdin)")
            return EXIT_FAIL
    return _init_run_core(repo, args.brief, brief_source, inline_content)


def _init_run_core(repo: str, brief_arg: str | None, brief_source: str,
                   inline_content: bytes | None = None,
                   run_id: str | None = None,
                   quiet: bool = False) -> int:
    parent = state_store.runs_root(repo)
    os.makedirs(parent, exist_ok=True)
    existing = set(os.listdir(parent)) if os.path.isdir(parent) else set()
    if run_id is None:
        run_id = state_store.new_run_id(existing)
    elif run_id in existing:
        _fail(f"run dir already exists: {os.path.join(parent, run_id)}")
        return EXIT_FAIL
    run_dir = os.path.join(parent, run_id)
    if os.path.exists(run_dir):  # refuse to overwrite an existing run dir
        _fail(f"run dir already exists: {run_dir}")
        return EXIT_FAIL
    for sub in ("prompts", os.path.join("logs", "jobs")):
        os.makedirs(os.path.join(run_dir, sub), exist_ok=True)

    fingerprint = repo_fingerprint.capture(repo)
    if brief_source == "inline":
        # materialize the immutable run-owned input BEFORE any expensive
        # inference; state/resume reference this copy, not the shell argument
        inputs_dir = os.path.join(run_dir, "inputs")
        os.makedirs(inputs_dir, exist_ok=True)
        brief = os.path.join(inputs_dir, "original-audit-brief.md")
        atomic_write_bytes(brief, inline_content)
        brief_sha = sha256_file(brief)
    else:
        brief = os.path.abspath(brief_arg)
        brief_sha = sha256_file(brief)

    # v2 A0.1/A0.6: freeze the environment binding BEFORE any inference can
    # happen. The ONLY brief text with execution authority is the explicit
    # ```json target block; all prose (including absolute paths) is inert.
    try:
        with open(brief, "rb") as fh:
            brief_text = fh.read().decode("utf-8", "replace")
    except OSError:
        brief_text = ""
    try:
        binding = env_binding.capture(repo, run_id, brief,
                                      parse_brief_target(brief_text), [])
    except env_binding.EnvironmentBindingError as exc:
        _fail(f"INVALID_AUDIT_ENVIRONMENT:{exc.reason}: {exc}")
        return EXIT_FAIL

    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "repo_root": repo,
        "brief_path": brief,
        "brief_source": brief_source,
        "brief_sha256": brief_sha,
        "created_at": utc_now_iso(),
        "tool_versions": fingerprint.get("tool_versions", {}),
        "instruction_files": _scan_instruction_files(repo),
    }
    atomic_write_json(os.path.join(run_dir, state_store.MANIFEST_NAME),
                      manifest)

    repo_state = {
        "schema_version": 1,
        "run_id": run_id,
        "captured_at": utc_now_iso(),
        "repo_root": repo,
        "brief_sha256": brief_sha,
        "contract_sha256": None,  # placeholder until freeze-contract
        "fingerprint": fingerprint,
    }
    atomic_write_json(os.path.join(run_dir, state_store.REPO_STATE_NAME),
                      repo_state)

    atomic_write_json(os.path.join(run_dir, ENV_BINDING_NAME), binding)

    state = state_store.new_state(
        run_id, repo, fingerprint["fingerprint_sha256"],
        env_binding_digest=binding["binding_digest"])
    atomic_write_json(os.path.join(run_dir, state_store.STATE_NAME), state)

    open(os.path.join(run_dir, state_store.CHECKSUMS_NAME), "a").close()
    for name in (state_store.MANIFEST_NAME, state_store.REPO_STATE_NAME,
                 ENV_BINDING_NAME, state_store.STATE_NAME):
        state_store.record_checksum(run_dir,
                                    os.path.join(run_dir, name))
    if brief_source == "inline":
        state_store.record_checksum(run_dir, brief)

    # register the active run for the path-guard PreToolUse hook (A0.4),
    # pinning the binding digest in the out-of-root registry (R3-N3)
    _register_active_run(run_id, run_dir,
                         pinned_digest=binding["binding_digest"])

    if not quiet:
        print(run_dir)
    return EXIT_OK


# ---------------------------------------------------------------------------
# prepare (v2 A1: user-facing environment preparation)
# ---------------------------------------------------------------------------
def cmd_prepare(args: argparse.Namespace) -> int:
    """One command for isolated audits (operator flow: source repo -> detached
    worktree -> frozen binding for THAT worktree -> authorized evidence ->
    validated brief -> inference). Prints the run dir."""
    import environment_manager as em
    repo = os.path.abspath(args.repo)
    if not repo_fingerprint._is_git_worktree(repo):
        _fail(f"{repo} is not a git worktree")
        return EXIT_FAIL
    brief = args.brief
    inline = bool(getattr(args, "brief_inline", False))
    if not inline:
        if not brief or not os.path.isfile(brief) \
                or os.path.getsize(brief) == 0:
            _fail(f"brief {brief!r} missing or empty (or use --brief-inline)")
            return EXIT_FAIL
    allow = [s.strip() for s in (args.evidence_allow or "").split(",")
             if s.strip()] or None
    brief_meta = {
        "mode": args.mode or "AUTO",
        "historical": bool(allow) or args.mode == "HISTORICAL",
        "target_ref": args.ref,
    }
    try:
        mode = em.resolve_mode({}, brief_meta)
        run_id = state_store.new_run_id(set(os.listdir(em.env_root()))
                                        if os.path.isdir(em.env_root())
                                        else set())
        record = em.prepare(mode, repo, run_id, target_ref=args.ref,
                            evidence_allowlist=allow)
    except em.EnvironmentManagerError as exc:
        _fail(f"environment preparation failed: {exc}")
        return EXIT_FAIL
    target_root = record.get("worktree_root") or repo
    rc = _init_run_core(target_root, brief, "inline" if inline else "file",
                        sys.stdin.buffer.read() if inline else None,
                        run_id=run_id, quiet=True)
    if rc != EXIT_OK:
        return rc
    run_dir = os.path.join(state_store.runs_root(target_root), run_id)
    # da27c0 fix 3: copy staged evidence into the RUN-OWNED location so
    # both Opus and the bubblewrapped Codex (run dir is its only writable
    # repo subtree) receive identical authorized evidence
    staged = record.get("staged_evidence") or []
    if staged:
        env_staged_root = em.staged_evidence_dir(run_id)
        run_staged_root = os.path.join(run_dir, "staged-evidence")
        for entry in staged:
            src = os.path.join(env_staged_root, entry["path"])
            dest = os.path.join(run_staged_root, entry["path"])
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(src, dest)
        record["staged_evidence_run_dir"] = "staged-evidence"
    # da27c0 fix 5: the environment record REFERENCES the run's frozen
    # binding — prepare() captures a preliminary binding (preparation
    # brief) whose digest legitimately differs from the run binding
    # (frozen with the operator's brief). The run binding is the
    # authority; link all three identities to it and keep the
    # preparation digest as explicit provenance.
    run_binding = load_json(os.path.join(run_dir, ENV_BINDING_NAME))
    record["preparation_binding_digest"] = record.get("binding_digest")
    record["binding_digest"] = run_binding["binding_digest"]
    # link the environment record into the run (provenance: which worktree,
    # which source, what was staged)
    atomic_write_json(os.path.join(run_dir, em.RECORD_NAME), record)
    state_store.record_checksum(run_dir, os.path.join(run_dir, em.RECORD_NAME))
    _emit({"ok": True, "run": run_dir, "mode": mode,
           "worktree_root": record.get("worktree_root"),
           "source_repository": record.get("source_repo_realpath"),
           "staged_evidence": len(record.get("staged_evidence") or [])})
    return EXIT_OK


# ---------------------------------------------------------------------------
# freeze-contract
# ---------------------------------------------------------------------------
def _range_order_errors(doc) -> list[str]:
    """Gate-level canonical-ordering check (H.4 review F5): reversed
    line_ranges (start > end) are INVALID everywhere; the schema keyword
    subset cannot express end >= start, so the gate enforces it."""
    errors: list[str] = []

    def walk(node, path):
        if isinstance(node, dict):
            ranges = node.get("line_ranges")
            if isinstance(ranges, list):
                for i, r in enumerate(ranges):
                    if isinstance(r, dict) \
                            and isinstance(r.get("start"), int) \
                            and isinstance(r.get("end"), int) \
                            and r["start"] > r["end"]:
                        errors.append(
                            f"{path}line_ranges[{i}]: reversed range "
                            f"({r['start']} > {r['end']})")
            for k, v in node.items():
                walk(v, f"{path}{k}.")
        elif isinstance(node, list):
            for i, x in enumerate(node):
                walk(x, f"{path}[{i}].")
    walk(doc, "")
    return errors


def _validate_artifact_file(path: str, schema_name: str | None,
                            name: str | None = None,
                            run_dir: str | None = None) -> list[str]:
    if schema_name is None:
        try:
            doc = load_json(path)
        except (json.JSONDecodeError, OSError) as exc:
            return [f"artifact does not parse as JSON: {exc}"]
        errors: list[str] = []
        if not isinstance(doc, dict):
            errors.append("artifact must be a JSON object")
        elif name == "99-run-metrics.json":
            pass  # metrics: any JSON object
        elif "clusters" not in doc or not isinstance(doc.get("clusters"), list):
            errors.append("structural check failed: expected object with a "
                          "`clusters` array")
        return errors
    errors = validate_artifact.validate_file(
        path, str(SCHEMAS_DIR / schema_name))
    doc = None
    try:
        doc = load_json(path)
    except (json.JSONDecodeError, OSError):
        doc = None
    if errors and doc is not None and run_dir is not None:
        # v1-compat reader (pillar H/G), scoped to v1-ERA RUNS ONLY (H.4
        # review F5): only a run predating environment bindings (no
        # env_binding_digest in state) may present legacy `lines` artifacts;
        # a v2 run introducing them is rejected. Validation is IN-MEMORY;
        # on-disk bytes are NEVER rewritten.
        try:
            import evidence_migration
            if evidence_migration.is_v1_artifact(doc):
                try:
                    state = state_store.load_state(run_dir)
                except StateError:
                    state = {}
                if not state.get("env_binding_digest"):
                    migrated = evidence_migration.migrate_artifact(doc)
                    schema = load_json(str(SCHEMAS_DIR / schema_name))
                    if not validate_artifact.validate(
                            migrated, schema, base_dir=SCHEMAS_DIR):
                        errors = []
                        doc = migrated
        except (OSError, json.JSONDecodeError,
                evidence_migration.MigrationError):
            pass
    if not errors and doc is not None:
        errors = _range_order_errors(doc)
    return errors


def cmd_freeze_contract(args: argparse.Namespace) -> int:
    run_dir = os.path.abspath(args.run)
    if not args.contract:
        _fail("freeze-contract requires --contract FILE or '--contract - --stdin'")
        return EXIT_FAIL
    # B-001: establish transition eligibility BEFORE any canonical
    # checkpoint byte is staged or replaced. check_transition applies the
    # authoritative forward-only rules purely; a rejected request writes
    # nothing and only the normal failed-attempt accounting happens.
    try:
        state_store.check_transition(run_dir, "CONTRACT_FROZEN")
    except StateError as exc:
        try:
            state_store.bump_phase_attempt(run_dir, "CONTRACT_FROZEN")
        except StateError:
            pass  # unusable state cannot be accounted; rejection stands
        _fail(str(exc))
        return EXIT_FAIL
    if args.contract == "-" or getattr(args, "stdin", False):
        try:
            contract = _read_stdin_artifact(
                run_dir, state_store.CONTRACT_NAME)
        except OSError as exc:
            _fail(f"could not stage stdin contract: {exc}")
            return EXIT_FAIL
    else:
        contract = os.path.abspath(args.contract)
    try:
        state = state_store.load_state(run_dir)
    except StateError as exc:
        _fail(str(exc))
        return EXIT_FAIL
    if not os.path.isfile(contract):
        _fail(f"contract file not found: {contract}")
        return EXIT_FAIL
    errors = _validate_artifact_file(contract, "audit-contract.schema.json",
                                    run_dir=run_dir)
    if not errors:
        errors = _fingerprint_mismatches(
            run_dir, state_store.CONTRACT_NAME, load_json(contract))
    if not errors:
        errors = _contract_target_mismatches(run_dir, load_json(contract))
    if errors:
        _fail(f"contract invalid against audit-contract.schema.json: {errors}")
        return EXIT_FAIL

    dest = os.path.join(run_dir, state_store.CONTRACT_NAME)
    with open(contract, "rb") as fh:
        data = fh.read()
    atomic_write_bytes(dest, data)
    digest = state_store.record_checksum(run_dir, dest)
    # contract checksum sidecar (state.json/manifest stay schema-pure)
    atomic_write_bytes(
        os.path.join(run_dir, state_store.CONTRACT_SIDECAR_NAME),
        f"{digest}  {state_store.CONTRACT_NAME}\n".encode())
    # record the contract sha in the (mutable only until first phase read)
    # 01-repository-state.json contract placeholder
    rs_path = os.path.join(run_dir, state_store.REPO_STATE_NAME)
    try:
        repo_state = load_json(rs_path)
        if repo_state.get("contract_sha256") is None:
            repo_state["contract_sha256"] = digest
            atomic_write_json(rs_path, repo_state)
            state_store.record_checksum(run_dir, rs_path)
    except (OSError, json.JSONDecodeError):
        pass

    try:
        state_store.apply_transition(run_dir, "CONTRACT_FROZEN")
    except StateError as exc:
        state_store.bump_phase_attempt(run_dir, "CONTRACT_FROZEN")
        _fail(str(exc))
        return EXIT_FAIL
    _emit({"ok": True, "run": run_dir, "contract_sha256": digest})
    return EXIT_OK


# ---------------------------------------------------------------------------
# advance
# ---------------------------------------------------------------------------
def _inside_run_dir(run_dir: str, path: str) -> bool:
    rd = os.path.realpath(run_dir)
    p = os.path.realpath(path)
    return p == rd or p.startswith(rd + os.sep)


def _read_stdin_artifact(run_dir: str, name: str) -> str:
    """Read artifact content from stdin and atomically stage it in the run dir."""
    dest = os.path.join(run_dir, name)
    atomic_write_bytes(dest, sys.stdin.buffer.read())
    return dest


def _contract_target_mismatches(run_dir: str, contract: dict) -> list[str]:
    """A0.2: the contract's declared target must resolve to the frozen audit
    environment (root by realpath, head exactly)."""
    path = os.path.join(run_dir, ENV_BINDING_NAME)
    if not os.path.isfile(path) or not isinstance(contract, dict):
        return []
    try:
        binding = load_json(path)
    except (json.JSONDecodeError, OSError):
        return []
    target = contract.get("target_repository") or {}
    root = target.get("root")
    if isinstance(root, str) and os.path.realpath(root) != \
            binding.get("repo_root_realpath"):
        return [f"INVALID_AUDIT_ENVIRONMENT:BRIEF_ROOT_MISMATCH: contract "
                f"target_repository.root {root!r} does not resolve to the "
                f"frozen audit root "
                f"{binding.get('repo_root_realpath')!r}"]
    head = target.get("head_sha")
    if isinstance(head, str) and head != binding.get("head_sha"):
        return [f"INVALID_AUDIT_ENVIRONMENT:BRIEF_HEAD_MISMATCH: contract "
                f"target_repository.head_sha {head!r} != frozen "
                f"{binding.get('head_sha')!r}"]
    return []


def _fingerprint_mismatches(run_dir: str, name: str, doc: dict) -> list[str]:
    """Semantic repository-identity invariant: any canonical artifact that
    claims a repository fingerprint must match the frozen run fingerprint.
    JSON Schema alone only checks SHA syntax, not equality with run state."""
    field_path = FINGERPRINT_FIELDS.get(name)
    if not field_path or not isinstance(doc, dict):
        return []
    node = doc
    for key in field_path:
        if not isinstance(node, dict):
            return []
        node = node.get(key)
    claimed = node if isinstance(node, str) else None
    try:
        frozen = state_store.load_state(run_dir).get("repo_fingerprint_sha256")
    except StateError:
        frozen = None
    if claimed is None:
        return [f"INVALID_ARTIFACT: {name} is missing its repository "
                f"fingerprint field {'.'.join(field_path)!r}"]
    if claimed != frozen:
        return [f"INVALID_ARTIFACT: {name} claims repository fingerprint "
                f"{claimed!r} but the frozen run fingerprint is {frozen!r}; "
                f"a model-provided fingerprint may not override run state"]


def cmd_advance(args: argparse.Namespace) -> int:
    run_dir = os.path.abspath(args.run)
    target = args.to
    if target not in PHASE_ARTIFACT:
        _fail(f"unknown target phase {target!r}")
        return EXIT_FAIL
    # A0.2 gate BEFORE anything else (before stdin is even consumed): an
    # inconsistent environment refuses inference with zero staging side
    # effects. Never yields a product verdict.
    if target in INFERENCE_PHASES:
        env_errors = _env_gate_errors(run_dir)
        if env_errors:
            return _env_fail(run_dir, env_errors)
    # B-001: establish transition eligibility BEFORE canonical checkpoint
    # bytes are staged, checksum entries are recorded, or skip records
    # persist. Everything the state machine needs is available now:
    # current phase, target, and the requested skip/adjudication
    # semantics (prospective skips are previewed, not persisted).
    try:
        cur_phase = state_store.load_state(run_dir)["phase"]
    except StateError as exc:
        _fail(str(exc))
        return EXIT_FAIL
    # v2 (pillar H): explicit, reason-carrying skip records for any
    # artifact phase this transition passes over (e.g. a partial run
    # finalizing past a quota-deferred Codex stage). Recorded BEFORE
    # the transition; the state machine refuses silent skips.
    skip_entries = []
    for raw in getattr(args, "skip", None) or []:
        phase, sep, reason = raw.partition("=")
        if not sep or phase not in state_store.PHASE_INDEX \
                or not reason.strip():
            _fail(f"invalid --skip {raw!r}: expected PHASE='reason' "
                  f"with a known phase and a non-empty reason")
            return EXIT_FAIL
        skip_entries.append({"skipped_phase": phase,
                             "reason": reason.strip()})
    if target == "COMPLETE" and cur_phase != "FINALIZED":
        # closing a run requires the honest finalize path (completeness
        # state + metrics); FINALIZED must not be jumped over
        _fail("advance to COMPLETE is only permitted from FINALIZED; "
              "use `finalize --run ... --completeness <STATE>` instead")
        return EXIT_FAIL
    # the prospective artifact name (stdin stages at the canonical phase
    # artifact; a file argument keeps its own basename) drives the same
    # adjudication-skip semantics apply_transition will later be given
    if args.artifact == "-" or getattr(args, "stdin", False):
        prospective_name = PHASE_ARTIFACT[target]
    else:
        prospective_name = os.path.basename(os.path.abspath(args.artifact))
    ci = state_store.PHASE_INDEX[cur_phase]
    ti = state_store.PHASE_INDEX[target]
    skips_adj = (ti > state_store.PHASE_INDEX[state_store.ADJUDICATION_PHASE]
                 > ci)
    skip_flag = True if (skips_adj
                         and cur_phase == "LEDGER_COMPLETE"
                         and target in state_store.ADJUDICATION_SKIP_TARGETS
                         and prospective_name != "50-targeted-adjudication.json") \
        else None
    try:
        state_store.check_transition(
            run_dir, target, adjudication_skipped=skip_flag,
            prospective_skips=skip_entries or None)
    except StateError as exc:
        try:
            state_store.bump_phase_attempt(run_dir, target)
        except StateError:
            pass  # unusable state cannot be accounted; rejection stands
        _fail(str(exc))
        return EXIT_FAIL

    # eligibility established: canonical staging may begin
    if args.artifact == "-" or getattr(args, "stdin", False):
        # content piped on stdin; filename derives from the target phase
        try:
            artifact = _read_stdin_artifact(run_dir, PHASE_ARTIFACT[target])
        except OSError as exc:
            _fail(f"could not stage stdin artifact: {exc}")
            return EXIT_FAIL
    else:
        artifact = os.path.abspath(args.artifact)
    if skip_entries:
        try:
            state_store.record_phase_skips(run_dir, skip_entries)
        except StateError as exc2:
            _fail(str(exc2))
            return EXIT_FAIL
    if not _inside_run_dir(run_dir, artifact):
        _fail(f"artifact must live inside the run dir: {artifact}")
        return EXIT_FAIL
    if not os.path.isfile(artifact):
        _fail(f"artifact not found: {artifact}")
        return EXIT_FAIL

    name = os.path.basename(artifact)
    schema_name = ARTIFACT_SCHEMAS.get(name, "__unknown__")
    if schema_name == "__unknown__":
        _fail(f"unrecognized artifact name {name!r}; expected one of: "
              f"{sorted(ARTIFACT_SCHEMAS)}")
        return EXIT_FAIL
    expected = PHASE_ARTIFACT.get(target)
    if target == "COMPLETE" and name == "90-final-findings.json":
        expected = "90-final-findings.json"
    if expected is not None and name != expected:
        _fail(f"phase {target} expects artifact {expected!r}, got {name!r}")
        return EXIT_FAIL

    errors = _validate_artifact_file(artifact, schema_name, name,
                                     run_dir=run_dir)
    if not errors and name == "40-disagreement-ledger.json":
        errors = validate_artifact.check_ledger_invariants(load_json(artifact))
    if not errors and name == "90-final-findings.json":
        final_doc = load_json(artifact)
        errors = validate_artifact.check_final_invariants(final_doc)
        if not errors:
            # spec §23: late findings may not be promoted without independent
            # validation by the other model (or staying UNRESOLVED)
            for crossex_name in ("31-opus-cross-examination.json",
                                 "32-codex-cross-examination.json"):
                cx_path = os.path.join(run_dir, crossex_name)
                if os.path.isfile(cx_path):
                    errors.extend(validate_artifact.check_late_findings(
                        load_json(cx_path), final_doc))
    if not errors:
        # semantic repository-identity invariant (v1.0.1 Issue 1)
        errors = _fingerprint_mismatches(run_dir, name, load_json(artifact))
    if errors:
        state_store.bump_phase_attempt(run_dir, target)
        _fail(f"artifact invalid: {errors}")
        return EXIT_FAIL

    state_store.record_checksum(run_dir, artifact)

    cur = state_store.load_state(run_dir)["phase"]
    ci = state_store.PHASE_INDEX[cur]
    ti = state_store.PHASE_INDEX[target]
    skips_adj = (ti > state_store.PHASE_INDEX[state_store.ADJUDICATION_PHASE]
                 > ci)
    skip_flag = True if (skips_adj
                         and cur == "LEDGER_COMPLETE"
                         and target in state_store.ADJUDICATION_SKIP_TARGETS
                         and name != "50-targeted-adjudication.json") \
        else None
    try:
        new_state = state_store.apply_transition(
            run_dir, target, adjudication_skipped=skip_flag)
    except StateError as exc:
        state_store.bump_phase_attempt(run_dir, target)
        _fail(str(exc))
        return EXIT_FAIL
    _emit({"ok": True, "phase": new_state["phase"],
           "adjudication_skipped": new_state.get("adjudication_skipped",
                                                 False)})
    return EXIT_OK


# ---------------------------------------------------------------------------
# verify-env (v2 A0.6)
# ---------------------------------------------------------------------------
def cmd_verify_env(args: argparse.Namespace) -> int:
    """A0.2 consistency gate: binding digest + brief root/HEAD + live
    environment. Exit 0 ok / 10 INVALID_AUDIT_ENVIRONMENT (never a product
    verdict; zero model calls happen through this gate)."""
    run_dir = os.path.abspath(args.run)
    errors = _env_gate_errors(run_dir)
    if errors:
        return _env_fail(run_dir, errors)
    _emit({"ok": True})
    return EXIT_OK


# ---------------------------------------------------------------------------
# verify-repo
# ---------------------------------------------------------------------------
def cmd_verify_repo(args: argparse.Namespace) -> int:
    run_dir = os.path.abspath(args.run)
    repo_state_path = os.path.join(run_dir, state_store.REPO_STATE_NAME)
    if not os.path.isfile(repo_state_path):
        _fail(f"missing {repo_state_path}")
        return EXIT_FAIL
    repo_state = load_json(repo_state_path)
    repo = repo_state.get("repo_root") or os.path.dirname(
        os.path.dirname(os.path.dirname(run_dir)))
    try:
        ok, diff = repo_fingerprint.verify(repo, repo_state_path)
    except (repo_fingerprint.FingerprintError, OSError,
            json.JSONDecodeError) as exc:
        _fail(str(exc))
        return EXIT_FAIL
    if not ok:
        try:
            state_store.set_completeness(
                run_dir, "STALE_REPOSITORY",
                failure_reason="repository changed during audit")
        except StateError:
            pass
        diff["ok"] = False
        diff["completeness_state"] = "STALE_REPOSITORY"
        _emit(diff)
        return EXIT_STALE
    _emit({"ok": True})
    return EXIT_OK


# ---------------------------------------------------------------------------
# write-guard
# ---------------------------------------------------------------------------
def _write_guard_violations(run_dir: str) -> list[dict[str, str]]:
    repo_state = load_json(os.path.join(run_dir, state_store.REPO_STATE_NAME))
    repo = repo_state.get("repo_root")
    baseline = repo_state.get("fingerprint", {})
    current = repo_fingerprint.capture(repo)
    diff = repo_fingerprint.diff_fingerprints(baseline, current)

    run_prefix = os.path.join("audit-output", "audit-council")
    violations: list[dict[str, str]] = []
    for kind, key in (
        ("modified", "changed_tracked"),
        ("added", "added_tracked"),
        ("removed", "removed_tracked"),
    ):
        for path in diff[key]:
            if path.startswith(run_prefix):
                continue
            violations.append({"path": path, "kind": kind})
    for path in diff["added_untracked"] + diff["removed_untracked"]:
        if path.startswith(run_prefix):
            continue
        violations.append({"path": path, "kind": "untracked-change"})
    for path in diff["porcelain_status_changes"]:
        if path.startswith(run_prefix):
            continue
        violations.append({"path": path, "kind": "status-change"})
    return violations


def cmd_write_guard(args: argparse.Namespace) -> int:
    run_dir = os.path.abspath(args.run)
    try:
        violations = _write_guard_violations(run_dir)
    except (repo_fingerprint.FingerprintError, StateError, OSError,
            json.JSONDecodeError) as exc:
        _fail(str(exc))
        return EXIT_FAIL
    if violations:
        _emit({"ok": False, "violations": violations,
               "note": "source write guard violation: repository modified "
                       "outside the run directory; nothing was deleted or "
                       "reset"})
        return EXIT_WRITE_GUARD
    _emit({"ok": True})
    return EXIT_OK


# ---------------------------------------------------------------------------
# resume-check
# ---------------------------------------------------------------------------
def _artifact_for_phase(phase: str) -> str | None:
    return PHASE_ARTIFACT.get(phase)


def cmd_resume_check(args: argparse.Namespace) -> int:
    run_dir = os.path.abspath(args.run)
    try:
        state = state_store.load_state(run_dir)
    except StateError as exc:
        _fail(str(exc))
        return EXIT_FAIL

    # 1. state schema validation
    schema_errors = validate_artifact.validate_file(
        os.path.join(run_dir, state_store.STATE_NAME),
        str(SCHEMAS_DIR / "state.schema.json"))
    if schema_errors:
        _fail(f"state.json invalid: {schema_errors}")
        return EXIT_FAIL

    # 2. checksums
    mismatches = state_store.verify_all(run_dir)
    if mismatches:
        _emit({"ok": False, "stage": "checksums", "mismatches": mismatches})
        return EXIT_CHECKSUM

    # 2.5 environment binding (v2 A0.6): gate + identical reconstruction;
    # re-register the active run so the path-guard hook protects a resumed
    # session
    env_binding_status = None
    if os.path.isfile(os.path.join(run_dir, ENV_BINDING_NAME)):
        env_errors = _env_gate_errors(run_dir)
        if env_errors:
            _emit({"ok": False, "stage": "environment-binding",
                   "error": env_errors[0],
                   "completeness_state": "INVALID_AUDIT_ENVIRONMENT"})
            return EXIT_ENV
        try:
            env_binding.reconstruct(run_dir)
            env_binding_status = "ok"
        except env_binding.EnvironmentBindingError as exc:
            _emit({"ok": False, "stage": "environment-binding",
                   "error": f"INVALID_AUDIT_ENVIRONMENT:{exc.reason}: {exc}"})
            return EXIT_ENV
        if state.get("phase") != "COMPLETE":
            _register_active_run(
                state["run_id"], run_dir,
                pinned_digest=state.get("env_binding_digest")
                or load_json(os.path.join(run_dir, ENV_BINDING_NAME)
                             ).get("binding_digest"))

    # 3. repository fingerprint
    ok, diff = repo_fingerprint.verify(
        state.get("repo_root") or os.path.dirname(
            os.path.dirname(os.path.dirname(run_dir))),
        os.path.join(run_dir, state_store.REPO_STATE_NAME))
    if not ok:
        try:
            state_store.set_completeness(
                run_dir, "STALE_REPOSITORY",
                failure_reason="repository changed during audit")
        except StateError:
            pass
        _emit({"ok": False, "stage": "repo-fingerprint", "diff": diff,
               "completeness_state": "STALE_REPOSITORY"})
        return EXIT_STALE

    # 4. completed artifacts exist + validate (H.4 review F3: phases with an
    # explicit recorded phase_skip are legitimately artifact-less)
    problems: list[str] = []
    cur = state_store.PHASE_INDEX[state["phase"]]
    skipped_phases = {s.get("skipped_phase")
                      for s in state.get("phase_skips", [])}
    for phase in state_store.PHASE_CHAIN[1:cur + 1]:
        if state.get("adjudication_skipped") and phase == \
                state_store.ADJUDICATION_PHASE:
            continue
        if phase in skipped_phases:
            continue  # explicitly skipped with a recorded reason
        name = _artifact_for_phase(phase)
        if name is None:  # PREFLIGHT_COMPLETE has no artifact
            continue
        path = os.path.join(run_dir, name)
        if not os.path.isfile(path):
            problems.append(f"{phase}: missing artifact {name}")
            continue
        errors = _validate_artifact_file(path, ARTIFACT_SCHEMAS.get(name),
                                          name, run_dir=run_dir)
        if not errors:
            # semantic repository-identity check on completed artifacts
            try:
                errors = _fingerprint_mismatches(run_dir, name,
                                                 load_json(path))
            except (json.JSONDecodeError, OSError) as exc:
                errors = [f"{name} unreadable: {exc}"]
        if errors:
            problems.append(f"{phase}: {name} invalid: {errors}")

    # earliest incomplete phase: if the CURRENT phase's artifact is present
    # and valid, that phase is effectively satisfied and the resume point is
    # the NEXT phase. (H.4 review F8: the old block attempted a same-phase
    # transition — always refused by the forward-only machine — and its
    # attempt bump leaked; no transition side effects happen here.)
    earliest = state["phase"]
    if not problems and earliest != "COMPLETE":
        name = _artifact_for_phase(earliest)
        if name:
            path = os.path.join(run_dir, name)
            if os.path.isfile(path) and not (
                    _validate_artifact_file(path, ARTIFACT_SCHEMAS.get(name),
                                            name, run_dir=run_dir)
                    or _fingerprint_mismatches(run_dir, name,
                                               load_json(path))):
                nxt = state_store.PHASE_INDEX[earliest] + 1
                if nxt < len(state_store.PHASE_CHAIN):
                    earliest = state_store.PHASE_CHAIN[nxt]

    _emit({
        "ok": not problems,
        "problems": problems,
        "earliest_incomplete_phase": earliest,
        "codex_session_id": state.get("codex", {}).get("session_id"),
        "phase_attempts": state.get("phase_attempts", {}),
        "completeness_state": state.get("completeness_state"),
        "environment_binding": env_binding_status,
    })
    if not problems:
        return EXIT_OK
    # fingerprint-integrity problems get their own machine-readable code so
    # callers can distinguish repository-identity corruption (INVALID_ARTIFACT)
    # from other artifact validation failures
    if any("INVALID_ARTIFACT" in p for p in problems):
        return EXIT_INVALID_ARTIFACT
    return EXIT_FAIL


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------
def _import_render_report():
    path = SCRIPTS_DIR / "render_report.py"
    if not path.is_file():
        raise ImportError("render_report.py not found next to audit_council.py")
    spec = importlib.util.spec_from_file_location("render_report", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cmd_render(args: argparse.Namespace) -> int:
    run_dir = os.path.abspath(args.run)
    name = args.artifact
    if name.endswith(".json"):
        name = name[: -len(".json")]
    if name.endswith(".md"):
        name = name[: -len(".md")]
    try:
        render_report = _import_render_report()
    except ImportError as exc:
        _fail(f"render unavailable: {exc}")
        return EXIT_FAIL
    fn = getattr(render_report, "render", None)
    if not callable(fn):
        _fail("render_report.py exposes no render entry point")
        return EXIT_FAIL
    try:
        md = fn(run_dir, name)
        out_path = render_report.default_out_path(run_dir, name)
        atomic_write_bytes(out_path, md.encode("utf-8"))
    except Exception as exc:
        _fail(f"render failed: {exc}")
        return EXIT_FAIL
    _emit({"ok": True, "artifact": name, "output": out_path})
    return EXIT_OK


# ---------------------------------------------------------------------------
# finalize
# ---------------------------------------------------------------------------
COMPLETENESS_STATES = {
    "COMPLETE", "COMPLETE_WITH_RESIDUAL_UNCERTAINTY", "PARTIAL_CODEX_QUOTA",
    "PARTIAL_CODEX_FAILURE", "PARTIAL_CLAUDE_INTERRUPTION",
    "INVALID_AUDIT_INPUT",
}


def cmd_finalize(args: argparse.Namespace) -> int:
    """Record the honest completeness state and close the run at COMPLETE."""
    run_dir = os.path.abspath(args.run)
    if args.completeness not in COMPLETENESS_STATES:
        _fail(f"unknown completeness state {args.completeness!r}")
        return EXIT_FAIL
    try:
        state = state_store.load_state(run_dir)
    except StateError as exc:
        _fail(str(exc))
        return EXIT_FAIL
    if state["phase"] != "FINALIZED":
        _fail(f"finalize requires phase FINALIZED (current: {state['phase']})")
        return EXIT_FAIL
    # R4 bootstrap hardening: unregistering the active run disarms the
    # path-guard hook — a forged state.json must not reach that point.
    # Checksum integrity is the gate (tampering state without recomputing
    # the ledger fails here; full-ledger forgery is a documented residual).
    mismatches = state_store.verify_all(run_dir)
    if mismatches:
        _fail(f"refusing to finalize: run integrity failures {mismatches}")
        return EXIT_CHECKSUM
    metrics = os.path.join(run_dir, "99-run-metrics.json")
    if not os.path.isfile(metrics):
        # partial runs (e.g. quota failure before any completed Codex stage)
        # still deserve an honest close-out: synthesize empty metrics
        atomic_write_json(metrics, {
            "invocations": [],
            "aggregates": {"invocation_count": 0, "fresh_count": 0,
                           "resumed_count": 0, "turns_total": 0,
                           "elapsed_sec_total": 0.0,
                           "degraded_telemetry_count": 0},
            "note": "no codex_runner metrics found; synthesized at finalize",
        })
    state_store.record_checksum(run_dir, metrics)
    try:
        state_store.apply_transition(run_dir, "COMPLETE")
    except StateError as exc:
        state_store.bump_phase_attempt(run_dir, "COMPLETE")
        _fail(str(exc))
        return EXIT_FAIL
    state_store.set_completeness(
        run_dir, args.completeness,
        failure_reason=args.failure_reason or None)
    # a closed run no longer constrains the path-guard hook (A0.4)
    _unregister_active_run(state["run_id"])
    # v2 A1/A2: an isolated run archives its artifacts BEFORE the ephemeral
    # worktree is removed (git worktree remove only). On archive failure the
    # worktree is KEPT (nothing is lost); the operator is told.
    cleanup = {"archived": False, "worktree_removed": False}
    record_path = os.path.join(run_dir, "environment-record.json")
    worktree_root = None
    if os.path.isfile(record_path):
        try:
            import environment_manager as em
            record = load_json(record_path)
            worktree_root = record.get("worktree_root")
            if worktree_root:
                em.archive_run(run_dir, worktree_root)
                cleanup["archived"] = True
                em.remove_worktree(worktree_root)
                cleanup["worktree_removed"] = True
                cleanup["archive_root"] = record.get("archive_root")
        except Exception as exc:  # noqa: BLE001 — report, never destroy
            cleanup["error"] = (f"worktree KEPT (artifacts preserved): "
                                f"{exc}")
    _emit({"ok": True, "phase": "COMPLETE",
           "completeness_state": args.completeness,
           "environment_cleanup": cleanup})
    return EXIT_OK


# ---------------------------------------------------------------------------
# describe (v2 F: public audit contract)
# ---------------------------------------------------------------------------
# Single machine-readable definition of the public contract (pillar F).
# PUBLIC-CONTRACT.md mirrors this document for humans; tests enforce the
# mirror for enum/list facts (completeness states, budgets, failure
# taxonomy, artifact inventory). Compatibility policy: additive changes
# keep protocol 2.x; any change to a documented field's meaning or any
# removal bumps the major version.
PUBLIC_CONTRACT: dict[str, Any] = {
    "protocol_version": "2.0",
    "compatibility_policy": (
        "additive changes keep 2.x; any change to a documented field's "
        "meaning or removal bumps the major version"),
    "environment_modes": ["AUTO", "CURRENT", "RELEASE", "HISTORICAL"],
    "model_roles": {
        "opus": {
            "model": "claude-opus-5",
            "role": "primary interactive orchestrator + independent auditor",
            "independent_pass": True,
        },
        "codex": {
            "model": "gpt-5.6-sol",
            "reasoning_effort": "xhigh",
            "role": "independent second auditor via codex exec",
            "read_only_sandbox": True,
            "independent_pass": True,
        },
    },
    "independence_rules": [
        "first-pass independence barrier: neither auditor sees the other's "
        "findings before both independent audits complete",
        "cross-examination is falsification, not validation",
        "no forced consensus; disagreements preserved in the ledger",
    ],
    "artifact_semantics": {
        "canonical_artifacts": [
            "00-run-manifest.json",
            "01-environment-binding.json",
            "02-audit-contract.json",
            "10-opus-independent.json",
            "20-codex-independent.json",
            "30-normalized-findings.json",
            "31-opus-cross-examination.json",
            "32-codex-cross-examination.json",
            "40-disagreement-ledger.json",
            "50-targeted-adjudication.json",
            "90-final-findings.json",
            "99-run-metrics.json",
        ],
        "evidence_model": (
            "typed line_ranges: [{start,end}] integers >=1, up to 32 "
            "disjoint ranges, deterministic ordering"),
        "raw_outputs_preserved": True,
    },
    "completeness_states": [
        "RUNNING",
        "COMPLETE",
        "COMPLETE_WITH_RESIDUAL_UNCERTAINTY",
        "PARTIAL_CODEX_QUOTA",
        "PARTIAL_CODEX_FAILURE",
        "PARTIAL_CLAUDE_INTERRUPTION",
        "STALE_REPOSITORY",
        "INVALID_AUDIT_INPUT",
        "INVALID_AUDIT_ENVIRONMENT",
    ],
    "environment_integrity": {
        "binding": ("AuditEnvironmentBinding frozen at init; "
                    "digest excludes frozen_at"),
        "failure_taxonomy": [
            "BRIEF_ROOT_MISMATCH",
            "BRIEF_HEAD_MISMATCH",
            "WORKTREE_IDENTITY_CHANGED",
            "CWD_OUTSIDE_FROZEN_ROOT",
            "PATH_ESCAPE_ATTEMPT",
            "ALTERNATE_WORKTREE_ACCESS",
            "UNAUTHORIZED_TMP_ACCESS",
            "REPO_ROOT_REPLACED",
            "SYMLINK_ESCAPE",
        ],
        "environment_failure_yields_product_verdict": False,
        "zero_model_calls_on_environment_failure": True,
    },
    "governor_constraints": {
        "max_successful_stages_per_phase": 1,
        "max_total_successful_stages": 3,
        "max_attempts_per_phase": 3,
        "max_repairs_per_phase": 1,
        "specialists_default": 0,
        "specialists_normal_cap": 2,
        "specialists_hard_cap": 3,
        "max_specialist_turns": 2,
        "max_dynamic_probes": 4,
        "cached_evidence_policy": "REUSE_WHEN_VALID",
        "force_fresh_release_gates": True,
        "omissions": ("every budget-driven omission is recorded explicitly "
                      "in run metrics"),
    },
    "brief_target_metadata": {
        "format": ('fenced ```json block containing {"target": '
                   '{"repository_root": <abs path>, "expected_head": '
                   "<40-hex>}}"),
        "prose_paths_are": "inert text — never execution authority",
    },
    "runtime_capabilities": {
        "codex_invocation": ("direct codex exec (fresh) / codex exec resume "
                             "<explicit-id>"),
        "auth": "subscription only; PAYG keys fail preflight",
        "claude_path_confinement": (
            "pre-tool mechanically denied: skill-scoped PreToolUse hook "
            "(Bash/Read/Grep/Glob) registered AUTOMATICALLY when "
            "/audit-council is invoked, active for the session, inert when "
            "no run is active; runner-enforced (not OS)"),
        "codex_write_confinement": (
            "OS-enforced: codex read-only sandbox AND bubblewrap read-only "
            "repo bind on every launch (fresh + resume)"),
        "codex_read_confinement": (
            "OS-enforced EXCLUSION outside the bwrap bind set (repo ro, run "
            "dir rw, ~/.codex, resolved toolchain roots, system dirs "
            "/etc+/usr+/lib, authorized fixture roots; /tmp is a fresh "
            "tmpfs). System directories remain readable by design. Without "
            "bubblewrap (AC_CODEX_BWRAP=0 or missing): not enforced / "
            "accepted residual — runner validates argv and output only"),
        "resumable": True,
        "write_scope": "audit-output/audit-council/<run-id>/ only",
        "sandbox_preflight": (
            "zero-inference viability proof (codex exec, intended node, "
            "login, chatgpt.com DNS, repo read, repo-write-denied, "
            "outside-read-denied, run-dir write) through the exact "
            "production bubblewrap wrapper BEFORE any model attempt is "
            "counted; failure = INVALID_AUDIT_ENVIRONMENT:SANDBOX_PREFLIGHT"),
        "evidence_staging": (
            "RELEASE and HISTORICAL both stage allow-listed evidence "
            "(realpath-resolved; containment + deny-list re-applied) into "
            "the run-owned staged-evidence/ dir, visible identically to "
            "Opus and the bubblewrapped Codex"),
    },
    "known_limitations": [
        "without bubblewrap, codex repo-read confinement is not enforced "
        "(accepted residual): the codex read-only sandbox prevents writes "
        "but does not scope reads to the frozen root; with bubblewrap, "
        "reads outside the enumerated bind set are OS-blocked but system "
        "directories (/etc, /usr) remain readable inside",
        "accepted auth-boundary residual: the bwrap bind set exposes "
        "~/.codex (read-write) to the codex process because subscription "
        "auth + explicit-session resume require it; a model command "
        "inside codex can read codex's own auth/session material — same "
        "access the codex process legitimately has on the host",
        "the Claude path-confinement hook is a no-inference lexical layer: "
        "encoded/dynamically-constructed payloads are beyond it; it "
        "hardens on top of detection (fingerprint + write-guard + binding "
        "verification), not a sandbox",
        "specialists are default-off until eval-proven; activation requires "
        "a pre-frozen documented reason recorded before first-pass "
        "completion",
        "historical replay is approval-gated; finalized benchmark runs are "
        "never re-run implicitly",
    ],
}


def cmd_describe(args: argparse.Namespace) -> int:
    """Print the versioned public audit contract (pillar F).

    `describe --json` prints the machine-readable contract (source of
    truth; PUBLIC-CONTRACT.md mirrors it). Without --json prints a short
    pointer summary. Deterministic: no environment reads, no model calls.
    """
    if getattr(args, "json", False):
        _emit(PUBLIC_CONTRACT)
        return EXIT_OK
    _emit({
        "ok": True,
        "protocol_version": PUBLIC_CONTRACT["protocol_version"],
        "human_readable_contract": "PUBLIC-CONTRACT.md",
        "machine_readable_contract": "audit_council.py describe --json",
    })
    return EXIT_OK


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="audit_council")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("preflight")
    p.add_argument("--repo", required=True)
    p.add_argument("--brief", required=False)
    p.add_argument("--brief-inline", action="store_true",
                   help="read the audit brief text from stdin and "
                        "materialize it as the run-owned immutable copy")
    p.add_argument("--skip-codex", action="store_true")
    p.set_defaults(func=cmd_preflight)

    p = sub.add_parser("init-run")
    p.add_argument("--repo", required=True)
    p.add_argument("--brief", required=False)
    p.add_argument("--brief-inline", action="store_true",
                   help="read the audit brief text from stdin and "
                        "materialize it as the run-owned immutable copy")
    p.set_defaults(func=cmd_init_run)

    p = sub.add_parser(
        "prepare",
        help="prepare an isolated audit environment and create the run in "
             "one step (RELEASE/HISTORICAL: detached worktree at --ref, "
             "frozen binding, authorized evidence staging)")
    p.add_argument("--repo", required=True,
                   help="SOURCE repository (its live tree is never touched)")
    p.add_argument("--brief", required=False)
    p.add_argument("--brief-inline", action="store_true")
    p.add_argument("--mode", default="AUTO",
                   choices=["AUTO", "CURRENT", "RELEASE", "HISTORICAL"])
    p.add_argument("--ref", default=None,
                   help="exact commit/HEAD to audit (detached worktree)")
    p.add_argument("--evidence-allow", default=None,
                   metavar="PATH[,PATH...]",
                   help="HISTORICAL: repo-relative evidence files to stage "
                        "(deny-listed paths are always refused)")
    p.set_defaults(func=cmd_prepare)

    p = sub.add_parser("freeze-contract")
    p.add_argument("--run", required=True)
    p.add_argument("--contract", required=False)
    p.add_argument("--artifact", dest="contract", help=argparse.SUPPRESS)
    p.add_argument("--stdin", action="store_true",
                   help="read content from stdin (with '--contract -')")
    p.set_defaults(func=cmd_freeze_contract)

    p = sub.add_parser("advance")
    p.add_argument("--run", required=True)
    p.add_argument("--to", required=True, dest="to")
    p.add_argument("--artifact", required=True)
    p.add_argument("--skip", action="append", default=None,
                   metavar="PHASE=REASON",
                   help="record an explicit skip for an artifact phase this "
                        "transition passes over (repeatable; required for "
                        "any passed-over artifact phase)")
    p.add_argument("--stdin", action="store_true",
                   help="read content from stdin (with '--artifact -')")
    p.set_defaults(func=cmd_advance)

    p = sub.add_parser("verify-env")
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_verify_env)

    p = sub.add_parser("verify-repo")
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_verify_repo)

    p = sub.add_parser("write-guard")
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_write_guard)

    p = sub.add_parser("finalize")
    p.add_argument("--run", required=True)
    p.add_argument("--completeness", required=True,
                   choices=sorted(COMPLETENESS_STATES))
    p.add_argument("--failure-reason", default=None)
    p.set_defaults(func=cmd_finalize)

    p = sub.add_parser("resume-check")
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_resume_check)

    p = sub.add_parser("render")
    p.add_argument("--run", required=True)
    p.add_argument("--artifact", required=True)
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("describe",
                       help="print the public audit contract")
    p.add_argument("--json", action="store_true",
                   help="print the machine-readable public contract "
                        "(source of truth; PUBLIC-CONTRACT.md mirrors it)")
    p.set_defaults(func=cmd_describe)

    return ap


def main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)
    try:
        return args.func(args)
    except BrokenPipeError:
        return EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main())
