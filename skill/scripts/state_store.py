#!/usr/bin/env python3
"""Run state management, atomic writes, checksums for audit-council.

Library + CLI. Python 3.14, stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

# ---------------------------------------------------------------------------
# Run dir layout
# ---------------------------------------------------------------------------
MANIFEST_NAME = "00-run-manifest.json"
REPO_STATE_NAME = "01-repository-state.json"
CONTRACT_NAME = "02-audit-contract.json"
CONTRACT_SIDECAR_NAME = "02-audit-contract.sha256"
STATE_NAME = "state.json"
CHECKSUMS_NAME = "checksums.sha256"
RUNS_PARENT = os.path.join("audit-output", "audit-council")

# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------
PHASE_CHAIN = [
    "CREATED",
    "PREFLIGHT_COMPLETE",
    "CONTRACT_FROZEN",
    "OPUS_INDEPENDENT_COMPLETE",
    "CODEX_INDEPENDENT_COMPLETE",
    "NORMALIZED",
    "OPUS_CROSS_EXAM_COMPLETE",
    "CODEX_CROSS_EXAM_COMPLETE",
    "LEDGER_COMPLETE",
    "ADJUDICATION_COMPLETE",
    "FINALIZED",
    "COMPLETE",
]
PHASE_INDEX = {p: i for i, p in enumerate(PHASE_CHAIN)}
ADJUDICATION_PHASE = "ADJUDICATION_COMPLETE"
# Phases whose meaning depends on a phase artifact being checkpointed. v2
# (pillar H): a forward transition may pass one of these over ONLY with an
# explicit, reason-carrying phase_skips record — never by silent timestamp
# filling (the v1 Fifth run jumped CODEX_CROSS_EXAM_COMPLETE with no 32-
# artifact and no record of why).
ARTIFACT_PHASES = frozenset(PHASE_CHAIN[2:-1])  # CONTRACT_FROZEN .. FINALIZED
# The only intermediate phase that may be skipped, and only under these rules:
#   - the run is at LEDGER_COMPLETE
#   - the target is FINALIZED or COMPLETE
#   - adjudication_skipped=True is recorded in state.json
ADJUDICATION_SKIP_TARGETS = {"FINALIZED", "COMPLETE"}

RUN_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}$")

STATE_REQUIRED_TOP_KEYS = (
    "schema_version", "run_id", "phase", "completeness_state", "created_at",
    "timestamps", "repo_fingerprint_sha256", "codex", "phase_attempts",
)


class StateError(Exception):
    """Raised on invalid state operations."""


# ---------------------------------------------------------------------------
# Atomic write / JSON helpers
# ---------------------------------------------------------------------------
def atomic_write_bytes(path: str | os.PathLike[str], data: bytes) -> None:
    """Write bytes atomically: temp file in same dir, fsync, os.replace."""
    path = os.fspath(path)
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-" + os.path.basename(path) + "-",
                               dir=directory)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def atomic_write_text(path: str | os.PathLike[str], text: str) -> None:
    atomic_write_bytes(path, text.encode("utf-8"))


def atomic_write_json(path: str | os.PathLike[str], doc: Any) -> None:
    atomic_write_text(path, json.dumps(doc, indent=2, sort_keys=False,
                                       ensure_ascii=False) + "\n")


def load_json(path: str | os.PathLike[str]) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | os.PathLike[str]) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ---------------------------------------------------------------------------
# Run ID
# ---------------------------------------------------------------------------
def new_run_id(existing: "set[str] | None" = None,
               _tries: int = 64) -> str:
    """Generate `YYYYMMDDTHHMMSSZ-<6hex>` (UTC); regenerate suffix on collision."""
    existing = existing if existing is not None else set()
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    for _ in range(_tries):
        run_id = f"{stamp}-{secrets.token_hex(3)}"
        if run_id not in existing:
            return run_id
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    raise StateError("could not allocate a collision-free run id")


def runs_root(repo_root: str | os.PathLike[str]) -> str:
    return os.path.join(os.fspath(repo_root), RUNS_PARENT)


# ---------------------------------------------------------------------------
# state.json
# ---------------------------------------------------------------------------
def state_path(run_dir: str | os.PathLike[str]) -> str:
    return os.path.join(os.fspath(run_dir), STATE_NAME)


def new_state(run_id: str, repo_root: str,
              repo_fingerprint_sha256: str,
              env_binding_digest: str | None = None) -> dict[str, Any]:
    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "phase": "CREATED",
        "completeness_state": "RUNNING",
        "created_at": utc_now_iso(),
        "timestamps": {"CREATED": utc_now_iso()},
        "repo_fingerprint_sha256": repo_fingerprint_sha256,
        "repo_root": os.path.abspath(repo_root),
        "codex": {
            "session_id": None,
            "jobs": [],
            "stage_counts": {
                "independent": 0,
                "cross_examination": 0,
                "adjudication": 0,
            },
        },
        "phase_attempts": {},
        "failure_reason": None,
        "adjudication_skipped": False,
    }
    if env_binding_digest is not None:
        state["env_binding_digest"] = env_binding_digest
    return state


def sanity_check_state(state: Any) -> None:
    if not isinstance(state, dict):
        raise StateError("state.json is not a JSON object")
    missing = [k for k in STATE_REQUIRED_TOP_KEYS if k not in state]
    if missing:
        raise StateError(f"state.json missing required keys: {missing}")
    if state.get("schema_version") != SCHEMA_VERSION:
        raise StateError(f"unsupported schema_version {state.get('schema_version')!r}")
    if state.get("phase") not in PHASE_INDEX:
        raise StateError(f"unknown phase {state.get('phase')!r}")
    if not RUN_ID_RE.match(str(state.get("run_id", ""))):
        raise StateError(f"malformed run_id {state.get('run_id')!r}")


def load_state(run_dir: str | os.PathLike[str]) -> dict[str, Any]:
    path = state_path(run_dir)
    try:
        state = load_json(path)
    except FileNotFoundError:
        raise StateError(f"state.json not found in {path}") from None
    sanity_check_state(state)
    return state


def save_state(run_dir: str | os.PathLike[str], state: dict[str, Any]) -> None:
    sanity_check_state(state)
    atomic_write_json(state_path(run_dir), state)
    # keep the checksum ledger consistent with the mutated state file
    cpath = checksums_path(run_dir)
    if os.path.exists(cpath):
        with open(cpath, "r", encoding="utf-8") as fh:
            recorded = any(
                line.split("  ", 1)[-1].strip() == STATE_NAME
                for line in fh if line.strip())
        if recorded:
            record_checksum(run_dir, state_path(run_dir))


def bump_phase_attempt(run_dir: str | os.PathLike[str], phase: str) -> None:
    """Record an attempt (successful or not) at reaching `phase`."""
    state = load_state(run_dir)
    state["phase_attempts"][phase] = int(
        state["phase_attempts"].get(phase, 0)) + 1
    save_state(run_dir, state)


def transition(state: dict[str, Any], target: str, *,
               adjudication_skipped: bool | None = None,
               now: str | None = None) -> dict[str, Any]:
    """Apply a forward-only phase transition to a state dict (returns a copy).

    Rules:
      - target must be a known phase further along the chain than the current
        phase (backward or same-phase transitions are errors);
      - ADJUDICATION_COMPLETE may be passed over only when the skip rules hold
        (current phase == LEDGER_COMPLETE, target in {FINALIZED, COMPLETE},
        adjudication_skipped recorded);
      - intermediate phases get timestamps filled in.
    """
    if target not in PHASE_INDEX:
        raise StateError(f"unknown target phase {target!r}")
    cur = state["phase"]
    ci, ti = PHASE_INDEX[cur], PHASE_INDEX[target]
    if ti <= ci:
        raise StateError(
            f"phase {cur} is already at or beyond {target}; completed phases "
            f"are immutable (forward-only state machine)")

    new = json.loads(json.dumps(state))  # deep copy
    now = now or utc_now_iso()

    skips_adjudication = (ci < PHASE_INDEX[ADJUDICATION_PHASE] < ti)
    if skips_adjudication:
        already = bool(new.get("adjudication_skipped"))
        allowed = (cur == "LEDGER_COMPLETE"
                   and target in ADJUDICATION_SKIP_TARGETS)
        if adjudication_skipped is True:
            if not allowed:
                raise StateError(
                    "adjudication may be skipped only from LEDGER_COMPLETE to "
                    "FINALIZED/COMPLETE (no eligible disputes)")
            new["adjudication_skipped"] = True
        elif not already:
            raise StateError(
                f"transition {cur} -> {target} would skip ADJUDICATION_COMPLETE "
                f"without adjudication_skipped being recorded")

    # LEDGER_COMPLETE may never be silently passed over.
    if ci < PHASE_INDEX["LEDGER_COMPLETE"] < ti and cur != "LEDGER_COMPLETE":
        raise StateError(
            f"transition {cur} -> {target} would skip LEDGER_COMPLETE; "
            f"the disagreement ledger must complete first")

    # v2 (pillar H): every OTHER passed-over artifact phase needs an explicit
    # skip record carrying a reason (ADJUDICATION keeps its own dedicated
    # adjudication_skipped rule above; COMPLETE's artifact is written by
    # finalize itself).
    if ti > ci + 1:
        recorded = {s.get("skipped_phase")
                    for s in new.get("phase_skips", [])}
        missing = [p for p in PHASE_CHAIN[ci + 1:ti]
                   if p != ADJUDICATION_PHASE and p != "COMPLETE"
                   and p in ARTIFACT_PHASES and p not in recorded]
        if missing:
            raise StateError(
                f"transition {cur} -> {target} would pass over "
                f"{missing} without an explicit skip record; record each "
                f"with `advance --skip PHASE='reason'`")

    new["phase"] = target
    for p in PHASE_CHAIN[ci + 1: ti + 1]:
        if p == ADJUDICATION_PHASE and skips_adjudication:
            continue
        new["timestamps"][p] = now
    new["phase_attempts"][target] = int(
        new["phase_attempts"].get(target, 0)) + 1
    return new


def apply_transition(run_dir: str | os.PathLike[str], target: str, *,
                     adjudication_skipped: bool | None = None) -> dict[str, Any]:
    state = load_state(run_dir)
    new = transition(state, target,
                     adjudication_skipped=adjudication_skipped)
    save_state(run_dir, new)
    return new


def check_transition(run_dir: str | os.PathLike[str], target: str, *,
                     adjudication_skipped: bool | None = None,
                     prospective_skips: list[dict[str, Any]] | None = None,
                     ) -> dict[str, Any]:
    """Pure eligibility preview for apply_transition (B-001 ordering fix).

    Applies the SAME authoritative transition rules — forward-only phase
    order, adjudication-skip rules, LEDGER_COMPLETE, explicit artifact-
    phase skip records — without writing anything: no state save, no
    attempt accounting, no skip persistence. `prospective_skips` are
    validated exactly like record_phase_skips entries and admitted into
    the in-memory state copy only, so a multi-phase jump can be previewed
    before its skip records are persisted. Raises StateError iff
    apply_transition would reject the same request; returns the state
    apply_transition would commit.
    """
    state = load_state(run_dir)
    if prospective_skips:
        state["phase_skips"] = _merged_skip_entries(state, prospective_skips)
    return transition(state, target, adjudication_skipped=adjudication_skipped)


def _merged_skip_entries(state: dict[str, Any],
                         entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate `entries` against the skip records already in `state` and
    return the combined skip list. Pure: raises the same StateError
    record_phase_skips raises for a bad entry; mutates nothing."""
    skips = list(state.get("phase_skips", []))
    known = {s.get("skipped_phase") for s in skips}
    for e in entries:
        phase = e.get("skipped_phase")
        if phase not in PHASE_INDEX:
            raise StateError(f"unknown skip phase {phase!r}")
        if not isinstance(e.get("reason"), str) or not e["reason"].strip():
            raise StateError("phase skip requires a non-empty reason")
        if phase in known:
            raise StateError(f"skip already recorded for {phase}")
        skips.append({"skipped_phase": phase,
                      "reason": e["reason"],
                      "recorded_at": e.get("recorded_at") or utc_now_iso()})
        known.add(phase)
    return skips


def record_phase_skips(run_dir: str | os.PathLike[str],
                       entries: list[dict[str, Any]]) -> None:
    """Persist explicit skip records (validated shape) BEFORE the transition
    that passes over those phases; the transition then admits them."""
    state = load_state(run_dir)
    state["phase_skips"] = _merged_skip_entries(state, entries)
    save_state(run_dir, state)


def set_completeness(run_dir: str | os.PathLike[str], value: str,
                     failure_reason: str | None = None) -> None:
    state = load_state(run_dir)
    state["completeness_state"] = value
    if failure_reason is not None:
        state["failure_reason"] = failure_reason
    save_state(run_dir, state)
    # keep the checksum ledger consistent with the mutated state file
    cpath = checksums_path(run_dir)
    if os.path.exists(cpath):
        with open(cpath, "r", encoding="utf-8") as fh:
            if any(line.split("  ", 1)[-1].strip() == STATE_NAME
                   for line in fh if line.strip()):
                record_checksum(run_dir, state_path(run_dir))


# ---------------------------------------------------------------------------
# checksums.sha256
# ---------------------------------------------------------------------------
def checksums_path(run_dir: str | os.PathLike[str]) -> str:
    return os.path.join(os.fspath(run_dir), CHECKSUMS_NAME)


def record_checksum(run_dir: str | os.PathLike[str],
                    path: str | os.PathLike[str]) -> str:
    """Append/replace a `sha256  name` line for path (relative to run dir)."""
    run_dir = os.fspath(run_dir)
    digest = sha256_file(path)
    name = os.path.relpath(os.path.abspath(path), os.path.abspath(run_dir))
    lines: list[str] = []
    cpath = checksums_path(run_dir)
    if os.path.exists(cpath):
        with open(cpath, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if line and line.split("  ", 1)[-1] != name:
                    lines.append(line)
    lines.append(f"{digest}  {name}")
    atomic_write_text(cpath, "\n".join(lines) + "\n")
    return digest


def verify_all(run_dir: str | os.PathLike[str]) -> list[dict[str, str]]:
    """Verify every recorded checksum. Returns list of mismatch records."""
    run_dir = os.fspath(run_dir)
    cpath = checksums_path(run_dir)
    mismatches: list[dict[str, str]] = []
    if not os.path.exists(cpath):
        return mismatches
    with open(cpath, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("  ", 1)
            if len(parts) != 2:
                mismatches.append({"file": line, "error": "malformed line",
                                   "line": str(lineno)})
                continue
            expected, name = parts
            full = os.path.join(run_dir, name)
            if not os.path.isfile(full):
                mismatches.append({"file": name, "error": "missing"})
                continue
            actual = sha256_file(full)
            if actual != expected:
                mismatches.append({"file": name, "error": "checksum mismatch",
                                   "expected": expected, "actual": actual})
    return mismatches


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _cli() -> int:
    ap = argparse.ArgumentParser(prog="state_store")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_new = sub.add_parser("new-run-id", help="print a fresh run id")
    ap_new.add_argument("--parent", help="runs parent dir for collision checks")

    sub.add_parser("verify-checksums", help="verify checksums.sha256") \
        .add_argument("--run", required=True)

    args = ap.parse_args()
    if args.cmd == "new-run-id":
        existing: set[str] = set()
        if args.parent and os.path.isdir(args.parent):
            existing = set(os.listdir(args.parent))
        print(new_run_id(existing))
        return 0
    if args.cmd == "verify-checksums":
        mism = verify_all(args.run)
        if mism:
            print(json.dumps({"ok": False, "mismatches": mism}, indent=2))
            return 8
        print(json.dumps({"ok": True}))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(_cli())
