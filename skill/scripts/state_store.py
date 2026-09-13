#!/usr/bin/env python3
"""Run state management, atomic writes, checksums for audit-council.

Library + CLI. Python 3.14, stdlib only.
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import secrets
import sys
import tempfile
import threading
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
# F-A-04: the ONLY phases an explicit skip record may name — this set is the
# single source of truth and MUST equal the phase_skips[].skipped_phase enum
# in schemas/state.schema.json (a drift test enforces the equality). The CLI
# and the library both validate against this set so a valid CLI operation can
# never persist a schema-invalid skip record.
SKIPPABLE_PHASES = ARTIFACT_PHASES
# B-005: the authoritative state-machine phase at which each model stage may
# LAUNCH. The gate lives here, in the authoritative state layer — the runner
# consults it and never re-implements phase-order policy.
STAGE_ENTRY_PHASE = {
    "independent": "OPUS_INDEPENDENT_COMPLETE",
    "cross_examination": "OPUS_CROSS_EXAM_COMPLETE",
    "adjudication": "LEDGER_COMPLETE",
}
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
# Cross-process run-state lock (F-A-05)
# ---------------------------------------------------------------------------
# Every read-modify-write of state.json / checksums.sha256 happens under an
# exclusive flock on <run_dir>/.state.lock. Cross-process writers serialize;
# nested acquisition inside ONE process (public entry points call save_state
# and record_checksum, which are themselves lock-aware) is reentrant via the
# depth counter, so no public helper can deadlock against another.
_LOCK_REGISTRY: dict[str, int] = {}
_LOCK_MUTEX = threading.RLock()


@contextlib.contextmanager
def run_state_lock(run_dir: str | os.PathLike[str]):
    """Serialize run-state mutation across processes (reentrant per process).

    Acquires an exclusive flock on <run_dir>/.state.lock. The lock file is
    run-owned scratch (never part of the checksummed canonical record) and is
    left in place — flock does not require deletion and deleting it would
    itself race.
    """
    key = os.path.realpath(os.fspath(run_dir))
    with _LOCK_MUTEX:
        if key in _LOCK_REGISTRY:
            _LOCK_REGISTRY[key] += 1
            try:
                yield
            finally:
                _LOCK_REGISTRY[key] -= 1
                if _LOCK_REGISTRY[key] <= 0:
                    del _LOCK_REGISTRY[key]
            return
    lock_path = os.path.join(os.fspath(run_dir), ".state.lock")
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        with _LOCK_MUTEX:
            _LOCK_REGISTRY[key] = _LOCK_REGISTRY.get(key, 0) + 1
        try:
            yield
        finally:
            with _LOCK_MUTEX:
                _LOCK_REGISTRY[key] -= 1
                if _LOCK_REGISTRY[key] <= 0:
                    _LOCK_REGISTRY.pop(key, None)
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _update_state_ledger(run_dir: str, state_path: str) -> None:
    """Re-record state.json in the checksum ledger if it is tracked there.

    Caller must hold run_state_lock (every caller does)."""
    cpath = checksums_path(run_dir)
    if os.path.exists(cpath):
        with open(cpath, "r", encoding="utf-8") as fh:
            recorded = any(
                line.split("  ", 1)[-1].strip() == STATE_NAME
                for line in fh if line.strip())
        if recorded:
            record_checksum(run_dir, state_path)


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
    # F-A-04: enforce the canonical phase_skips item shape at every save, so
    # NO code path (CLI or library) can persist a state document that
    # state.schema.json would reject on resume.
    skips = state.get("phase_skips", [])
    if not isinstance(skips, list):
        raise StateError("phase_skips must be an array")
    for i, entry in enumerate(skips):
        if not isinstance(entry, dict):
            raise StateError(f"phase_skips[{i}] is not an object")
        phase = entry.get("skipped_phase")
        if phase not in SKIPPABLE_PHASES:
            raise StateError(
                f"phase_skips[{i}].skipped_phase {phase!r} is not a "
                f"skippable artifact phase (state.schema.json enum)")
        reason = entry.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise StateError(f"phase_skips[{i}].reason must be a non-empty "
                             f"string")
        if not isinstance(entry.get("recorded_at"), str):
            raise StateError(f"phase_skips[{i}].recorded_at must be a string")
        for key in ("from_phase", "to_phase"):
            val = entry.get(key)
            if val is not None and val not in PHASE_INDEX:
                raise StateError(f"phase_skips[{i}].{key} {val!r} is not a "
                                 f"known phase")
        consumed = entry.get("consumed")
        if consumed is not None and not isinstance(consumed, bool):
            raise StateError(f"phase_skips[{i}].consumed must be a boolean")


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
    # F-A-05: state write + ledger re-record are one serialized mutation
    with run_state_lock(run_dir):
        atomic_write_json(state_path(run_dir), state)
        # keep the checksum ledger consistent with the mutated state file
        _update_state_ledger(os.fspath(run_dir), state_path(run_dir))


def bump_phase_attempt(run_dir: str | os.PathLike[str], phase: str) -> None:
    """Record an attempt (successful or not) at reaching `phase`."""
    with run_state_lock(run_dir):
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
    # F-A-10: a skip record authorizes exactly the transition context it was
    # recorded for (from_phase == cur AND to_phase == target) and exactly
    # once (consumed != True). A record from an aborted or different
    # transition — or a legacy unbound record — authorizes NOTHING, so stale
    # skip authorization cannot silently survive.
    admitted: dict[str, dict[str, Any]] = {}
    if ti > ci + 1:
        missing = []
        for p in PHASE_CHAIN[ci + 1:ti]:
            if p == ADJUDICATION_PHASE or p == "COMPLETE" \
                    or p not in ARTIFACT_PHASES:
                continue
            match = None
            for s in new.get("phase_skips", []):
                if s.get("skipped_phase") != p or s.get("consumed") is True:
                    continue
                if s.get("from_phase") == cur and s.get("to_phase") == target:
                    match = s
                    break
            if match is None:
                missing.append(p)
            else:
                admitted[p] = match
        if missing:
            raise StateError(
                f"transition {cur} -> {target} would pass over "
                f"{missing} without an explicit unconsumed skip record bound "
                f"to this exact transition; record each with `advance --skip "
                f"PHASE='reason'` (bound to {cur} -> {target})")

    new["phase"] = target
    for p in PHASE_CHAIN[ci + 1: ti + 1]:
        if p == ADJUDICATION_PHASE and skips_adjudication:
            continue
        new["timestamps"][p] = now
    new["phase_attempts"][target] = int(
        new["phase_attempts"].get(target, 0)) + 1
    # F-A-10: the successful transition CONSUMES the skip records that
    # authorized it — they can never authorize a later transition.
    for entry in admitted.values():
        entry["consumed"] = True
        entry["consumed_at"] = now
    return new


def apply_transition(run_dir: str | os.PathLike[str], target: str, *,
                     adjudication_skipped: bool | None = None) -> dict[str, Any]:
    # F-A-05: eligibility check + committed write are one serialized mutation
    with run_state_lock(run_dir):
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
        state["phase_skips"] = _merged_skip_entries(
            state, prospective_skips,
            from_phase=state["phase"], to_phase=target)
    return transition(state, target, adjudication_skipped=adjudication_skipped)


def _merged_skip_entries(state: dict[str, Any],
                         entries: list[dict[str, Any]],
                         from_phase: str | None = None,
                         to_phase: str | None = None) -> list[dict[str, Any]]:
    """Validate `entries` against the skip records already in `state` and
    return the combined skip list. Pure: raises the same StateError
    record_phase_skips raises for a bad entry; mutates nothing.

    F-A-04: only SKIPPABLE_PHASES (the state.schema.json enum) may be named.
    F-A-10: each entry is bound to the transition context that will consume
    it (from_phase/to_phase) whenever that context is known."""
    skips = list(state.get("phase_skips", []))
    known = {s.get("skipped_phase") for s in skips}
    for e in entries:
        phase = e.get("skipped_phase")
        if phase not in SKIPPABLE_PHASES:
            raise StateError(
                f"invalid skip phase {phase!r}: only artifact phases may be "
                f"skipped (the state.schema.json phase_skips enum)")
        if not isinstance(e.get("reason"), str) or not e["reason"].strip():
            raise StateError("phase skip requires a non-empty reason")
        if phase in known:
            raise StateError(f"skip already recorded for {phase}")
        entry = {"skipped_phase": phase,
                 "reason": e["reason"],
                 "recorded_at": e.get("recorded_at") or utc_now_iso()}
        if from_phase is not None:
            entry["from_phase"] = from_phase
        if to_phase is not None:
            entry["to_phase"] = to_phase
        skips.append(entry)
        known.add(phase)
    return skips


def record_phase_skips(run_dir: str | os.PathLike[str],
                       entries: list[dict[str, Any]],
                       *,
                       from_phase: str | None = None,
                       to_phase: str | None = None) -> None:
    """Persist explicit skip records (validated shape) BEFORE the transition
    that passes over those phases; the transition then admits them."""
    with run_state_lock(run_dir):
        state = load_state(run_dir)
        state["phase_skips"] = _merged_skip_entries(
            state, entries, from_phase=from_phase, to_phase=to_phase)
        save_state(run_dir, state)


def check_stage_launch(run_dir: str | os.PathLike[str], stage: str) -> dict:
    """B-005: mechanical launch gate for model stages, authoritative in the
    state layer. A stage may launch only when the state machine is at the
    stage's entry phase (STAGE_ENTRY_PHASE), or earlier with every passed
    artifact phase covered by an explicit unconsumed skip record — and never
    once the stage's completion phase is already reached. Returns the loaded
    state; raises StateError on refusal (nothing is written)."""
    if stage not in STAGE_ENTRY_PHASE:
        raise StateError(f"unknown model stage {stage!r}; expected one of "
                         f"{sorted(STAGE_ENTRY_PHASE)}")
    state = load_state(run_dir)
    cur = state["phase"]
    entry = STAGE_ENTRY_PHASE[stage]
    ci, ei = PHASE_INDEX[cur], PHASE_INDEX[entry]
    done = PHASE_CHAIN[ei + 1]  # the phase this stage completes into
    if PHASE_INDEX[cur] >= PHASE_INDEX[done]:
        raise StateError(
            f"refusing to launch stage {stage!r}: the state machine is at "
            f"{cur}, at or beyond the stage's completion phase {done}")
    if ci == ei:
        return state
    if ci < PHASE_INDEX["CONTRACT_FROZEN"]:
        raise StateError(
            f"refusing to launch stage {stage!r}: the audit contract must be "
            f"frozen first (current phase {cur})")
    recorded = {s.get("skipped_phase")
                for s in state.get("phase_skips", [])
                if s.get("consumed") is not True}
    uncovered = [p for p in PHASE_CHAIN[ci + 1:ei + 1]
                 if p in ARTIFACT_PHASES and p not in recorded]
    if uncovered:
        raise StateError(
            f"refusing to launch stage {stage!r}: the state machine is at "
            f"{cur}, before the stage entry phase {entry}, and phases "
            f"{uncovered} lack explicit unconsumed skip records")
    return state


def set_completeness(run_dir: str | os.PathLike[str], value: str,
                     failure_reason: str | None = None) -> None:
    with run_state_lock(run_dir):
        state = load_state(run_dir)
        state["completeness_state"] = value
        if failure_reason is not None:
            state["failure_reason"] = failure_reason
        save_state(run_dir, state)


# ---------------------------------------------------------------------------
# checksums.sha256
# ---------------------------------------------------------------------------
def checksums_path(run_dir: str | os.PathLike[str]) -> str:
    return os.path.join(os.fspath(run_dir), CHECKSUMS_NAME)


def record_checksum(run_dir: str | os.PathLike[str],
                    path: str | os.PathLike[str]) -> str:
    """Append/replace a `sha256  name` line for path (relative to run dir)."""
    # F-A-05: the ledger rewrite is a read-modify-write — serialize it
    with run_state_lock(run_dir):
        run_dir = os.fspath(run_dir)
        digest = sha256_file(path)
        name = os.path.relpath(os.path.abspath(path),
                               os.path.abspath(run_dir))
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
