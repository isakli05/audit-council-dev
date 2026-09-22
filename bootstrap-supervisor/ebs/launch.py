"""Controllerless one-shot verified boundary child execution.

Primary launch authority is NON-EXPORTABLE EBS PROCESS STATE plus
state-machine control flow (adopted R1): the whole launch lifecycle —
custody admission, static byte identities, both fresh runtime gates,
durable GATES_PASSED -> CONSUMED_PRE_EXEC, the irreversible in-process
spend, and the IMMEDIATE fork/exec attempt — happens inside ONE public
authority operation `Supervisor.run_attempt(credential_source_fd,
launcher_path, auditor_executable_path, report_staging_path,
output_root)` (final launch-seam remediation CR-EBS-S1-004/-005/-006 +
final execution-lifecycle remediation CR-EBS-S1-007/-008, which extend
the SAME call through the process-bound report lifecycle and the
timeout-bounded child wait).  There is NO grant, NO consume()/execute()
split, and NO public object whose possession separates consumption from
exec; GATES_PASSED and CONSUMED_PRE_EXEC are internal transients in
which no caller ever regains control (S1-005; no TTL, no timestamp
window, no second resource gate, no retry).  No bearer token exists in
any file, argv, environment, or IPC surface; no controller; no attach or
revival path.  Before any authority exists the supervisor FAIL-CLOSED
VERIFIES ITS OWN LIVE PACKAGE BYTES against the identities pinned by the
frozen binding (verify_package_identity; construction + full semantics
in README.md) — mandatory, in the startup path, with no flag and no
environment override — and then verifies the supplied FROZEN EVENT
PACKAGE (verify_event_package, CR-EBS-REM-001): package identity against
the binding's independently pinned event_package pair PLUS exact
transport-projection equality with the binding, before any gate is
reachable; the event-package root is a MANDATORY supervisor input with
no default and no bypass of any kind.

CR-EBS-S1-004: the Supervisor OWNS the sealed credential custody.  The
public authority operation accepts a CREDENTIAL SOURCE FD (never a
CredentialCustody, never a role); ingest runs non-dumpable, source
discipline, bounded read, and four-seal establishment BEFORE any gate
and BEFORE CONSUMED_PRE_EXEC, with the custody role derived ONLY from
binding.auditor_role (plus a defense-in-depth exact-role re-check).  The
SAME held custody serves the child's CRED_FD and the report leak screen,
and is closed on every terminal path.

The frozen boundary-launcher executable is verified by opening it ONCE,
hashing the ALREADY-OPEN file, and executing THAT OPEN FILE DESCRIPTOR
via execveat(AT_EMPTY_PATH) (fexecve fallback).  A pathname re-open is
never used after verification; unavailability of the identity-preserving
exec method fails closed.  The held fd is re-hashed before gate
acceptance and again immediately before fork so same-inode drift fails
closed (pre-consumption PREEXEC; post-consumption terminal).

CR-EBS-S1-006: the live AUDITOR EXECUTABLE gets the SAME discipline —
opened once with no-final-symlink, required regular + executable, hashed
as the ALREADY-OPEN fd against binding.auditor_identity's exact SHA-256
(a mismatch is PREEXEC_EXECUTABLE_IDENTITY_FAIL: PREEXEC, authority
unconsumed, no same-attempt retry), HELD, re-hashed before gate
acceptance and again post-consumption, and passed to the boundary
launcher as the fixed inherited AUDITOR_EXEC_FD.  The EXACT frozen
auditor argv travels ONLY as canonical binding bytes on the sealed
read-only AUDITOR_INVOCATION_FD — no caller argv tail, no caller
environment override, and no caller string can reach the auditor client.

Final execution-lifecycle remediation (CR-EBS-S1-007/-008): the ONE
public operation run_attempt(credential_source_fd, launcher_path,
auditor_executable_path, report_staging_path, output_root) ->
AttemptResult covers the WHOLE attempt; the separate public
adopt_report()/finish() surface NO LONGER EXISTS.  After the bounded
child wait the SAME call takes ONE immutable report snapshot
(no-final-symlink, regular, size-bounded, single read of the
already-open fd), screens THAT snapshot with the SAME held custody
(contaminated -> REPORT_SCREEN_FAIL terminal, validator never run),
runs the FROZEN STRUCTURAL VALIDATOR on exactly that snapshot (V5
output_validator descriptor; verified/HELD from the frozen event
package, re-hashed before execution, NO credential fd, sealed-memfd
delivery, strict AUCDEV-023-REPORT-VALIDATOR-RESULT-V1 envelope,
frozen validator_timeout_seconds bound) and only then freezes the exact
screened+validated bytes 0444 through the pre-opened held
output-custody fd before TERMINAL and custody/held-fd closure.  Missing
stays REPORT_MISSING (stdout/stderr never reconstruct a report);
validator FAIL/non-zero/malformed/mismatch/timeout is REPORT_INVALID;
every refusal terminalizes fail-closed inside the call; no report
retry exists.  CR-EBS-S1-008: the boundary child runs in its OWN
session under a MONOTONIC deadline from frozen
execution_limits.auditor_timeout_seconds (BOTH parent pipes NONBLOCKING
in the deadline loop — nothing blocks past the deadline); a timeout
SIGKILLs the EXACT attempt process group (descendants included, never
an unrelated process), reaps the direct child, and terminalizes with
consumed semantics (TIMEOUT_AFTER_CONSUMPTION; authority CONSUMED,
model engagement CONSUMED FAIL-CLOSED, no report accepted, replacement
= new operator authority only).

S1-009 post-consumption fail-closed terminality: ONE centralized
settlement primitive (_settle_post_consumption) separates the durable
accounting attempt (report-outcome record when one applies, then
TERMINAL; first durable failure preserves the record exactly, never
counted as durable success) from a guaranteed in-process fail-closed
death (fail_closed_terminal + custody/held-fd closure in a
never-raising finally); durable accounting failure raises
PostConsumptionTerminalAccountingError chaining any concurrent failure
(never a success/timed-out/conforming AttemptResult), and parent-side
exceptions after EXEC_ATTEMPTED re-raise only when the durable
settlement completed.

Gate-timing remediation (CR-EBS-S1-001) + preexec-gate remediation
(CR-EBS-S1-002/-003): the DYNAMIC runtime gates are NOT frozen evidence.
Every Supervisor construction holds the VERIFIED OPEN fd of BOTH runtime
gate artifacts bound by the frozen descriptors (identity/path/SHA-256/
result schema, digest- and projection-covered).  The externally
separable preexec sequence validate_gates() -> verify_launcher() ->
consume() NO LONGER EXISTS: the ONE public authority operation executes
both gates fresh in the required order (NETWORK_READINESS once, then
RESOURCE_GATE once LAST) and durably records GATES_PASSED ->
CONSUMED_PRE_EXEC without returning control to the caller in between.
Each gate executes with a bounded fail-closed timeout, no credential fd
inherited, a clean minimal environment, and strict result-envelope
validation against the binding; any failure terminalizes the attempt
with authority unconsumed and no same-attempt retry.
"""
from __future__ import annotations

import ctypes
import errno
import fcntl
import hashlib
import json
import os
import platform
import stat
import time
from dataclasses import dataclass

from .accounting import AccountingStore, open_custody_dir
from .binding import (EVENT_MANIFEST_KEYS, EVENT_MANIFEST_SCHEMA,
                      NETWORK_READINESS_RESULT_SCHEMA,
                      RESOURCE_GATE_RESULT_SCHEMA, RUNTIME_GATES,
                      VALIDATOR_RESULT_SCHEMA, BindingError,
                      binding_projection, canonical_bytes, strict_loads)
from .custody import (F_ADD_SEALS, F_GET_SEALS, MFD_ALLOW_SEALING,
                      MFD_CLOEXEC, REQUIRED_SEALS, CredentialCustody,
                      establish_non_dumpable, memfd_create)
from .reportcustody import (ReportRefused, discard_staging, freeze_snapshot,
                            snapshot_staging)
from .statemachine import (CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, GATES_PASSED,
                           PREPARED, REPORT_FROZEN, REPORT_INVALID,
                           REPORT_MISSING, REPORT_SCREEN_FAIL, TERMINAL,
                           TERMINAL_PREEXEC_STOP, StateMachine)

CRED_FD = 3                    # fixed inherited-fd contract for the sealed
                               # credential memfd; the ONLY credential channel
FAIL_FD = 4                    # exec-failure signal pipe (CLOEXEC: EOF = ok)
AUDITOR_EXEC_FD = 5            # HELD verified live auditor-executable fd
AUDITOR_INVOCATION_FD = 6      # sealed read-only canonical frozen-argv fd
VALIDATOR_REPORT_FD = 3        # validator child: sealed snapshot memfd
CHILD_EXIT_EXEC_FAIL = 98
METADATA_MAX = 65536
METADATA_GRACE = 0.5           # bounded post-reap metadata drain (seconds)

# Runtime-gate execution bounds (CR-EBS-S1-001; shared by BOTH dynamic
# gates under S1-002): a hung gate must never create an unbounded
# authority process, and the accepted result is size-bounded before
# parsing.
RUNTIME_GATE_TIMEOUT = 10.0             # seconds; deterministic fail-closed
RUNTIME_GATE_RESULT_MAX = 65536         # accepted result bytes (bound first)

# EXEC-03 structural remediation (AUCDEV023-CR-S1-EXEC03-001): the
# structural output validator's ONLY failure-diagnostic channel is the
# frozen stderr emission `VALIDATION_ERROR: <detail>` (its stdout
# envelope carries no error field), so the validator child receives a
# WRITABLE bounded stderr pipe (every other gate child keeps the exact
# historical read-only /dev/null fd 2) and the captured bytes are
# reduced — fail-closed — to a bounded STRUCTURAL-ONLY token before any
# durable use: never validator prose, report text, credentials or
# arbitrary child output.
VALIDATOR_STDERR_MAX = 4096
STRUCTURAL_TOKEN_PREFIX = "VALIDATION_ERROR: "
STRUCTURAL_TOKEN_CHARS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")

RESOURCE_GATE_SAMPLES = 3
RESOURCE_GATE_RESULT_FIELDS = ("schema", "status", "event_id",
                               "auditor_role", "attempt_id", "samples")
RESOURCE_GATE_SAMPLE_FIELDS = ("status", "detail")
NETWORK_READINESS_RESULT_FIELDS = ("schema", "status", "event_id",
                                   "auditor_role", "attempt_id",
                                   "provider_role",
                                   "boundary_launcher_sha256",
                                   "sandbox_profile_id", "checks")
NETWORK_READINESS_CHECKS = ("route", "resolver")
NETWORK_READINESS_CHECK_FIELDS = ("status", "detail")
SIGKILL = 9                              # POSIX constant (no signal import)

AT_EMPTY_PATH = 0x1000
SYS_EXECVEAT = {"x86_64": 322, "aarch64": 281, "armv7l": 387, "i686": 358}

PACKAGE_MANIFEST = "MANIFEST.json"


class LaunchError(RuntimeError):
    """Refused or failed launch-path operation (fail closed)."""


class LaunchRefused(LaunchError):
    """Identity/verification refusal before any exec attempt."""


class PostConsumptionTerminalAccountingError(LaunchError):
    """(S1-009) The durable post-consumption terminal accounting chain
    did NOT complete: the attempt is already in-process TERMINAL with
    the custody and every held fd closed and NO retry exists, but the
    durable record must be treated as INCOMPLETE; accounting_error /
    original_error / related_error carry the exact failures.  Never
    returned or swallowed as a success/timed-out/conforming result."""

    def __init__(self, durable_error, original_error=None,
                 related_error=None, last_state=None) -> None:
        concurrent = original_error if original_error is not None \
            else related_error
        super().__init__(
            "POSTCONSUMPTION_TERMINAL_ACCOUNTING_FAILED: the durable "
            f"terminal accounting chain did not complete "
            f"({durable_error!r}); last durable recorded state "
            f"{last_state!r}; the attempt is in-process TERMINAL with "
            "the custody and every held fd closed and NO retry exists — "
            "treat the durable record as INCOMPLETE"
            + ("" if concurrent is None
               else f"; concurrent failure: {concurrent!r}"))
        self.accounting_error = durable_error
        self.original_error = original_error
        self.related_error = related_error


def _char_array(items) -> "ctypes.Array":
    array = (ctypes.c_char_p * (len(items) + 1))()
    for index, item in enumerate(items):
        array[index] = item.encode() if isinstance(item, str) else item
    return array


def _execveat(fd: int, argv, envp) -> None:
    number = SYS_EXECVEAT.get(platform.machine())
    if number is None:
        raise LaunchError(
            f"EXECVEAT_UNSUPPORTED_ARCH: {platform.machine()}")
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    result = libc.syscall(ctypes.c_long(number), ctypes.c_int(fd),
                          ctypes.c_char_p(b""), _char_array(argv),
                          _char_array(envp), ctypes.c_uint(AT_EMPTY_PATH))
    if result != 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))


def _fexecve(fd: int, argv, envp) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    entry = getattr(libc, "fexecve", None)
    if entry is None:
        raise LaunchError("FEXECVE_UNAVAILABLE: identity-preserving exec "
                          "method absent; failing closed")
    entry.restype = ctypes.c_int
    result = entry(ctypes.c_int(fd), _char_array(argv), _char_array(envp))
    if result != 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))


def fd_exec(fd: int, argv, env: dict) -> None:
    """Exec the ALREADY-OPEN verified fd.  No pathname fallback exists."""
    envp = [f"{key}={value}" for key, value in sorted(env.items())]
    try:
        _execveat(fd, argv, envp)
    except OSError as exc:
        if exc.errno == errno.ENOSYS:
            _fexecve(fd, argv, envp)
        raise


def _hash_fd(fd: int) -> str:
    digest = hashlib.sha256()
    os.lseek(fd, 0, os.SEEK_SET)
    while True:
        chunk = os.read(fd, 65536)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def _open_verified(path, expected_sha256: str, kind: str,
                   require_executable: bool) -> int:
    """Shared verified-open core: open with NO final-symlink following,
    require a regular file (plus executable mode when required), hash
    the ALREADY-OPEN fd, require exact equality with expected_sha256,
    rewind, and return the verified open HELD fd (a pathname re-open is
    never used after verification)."""
    try:
        fd = os.open(os.fspath(path), os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise LaunchRefused(f"{kind}_OPEN_REFUSED (symlink/unreadable?): "
                            f"{exc!r}") from exc
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise LaunchRefused(f"{kind}_NOT_REGULAR_FILE")
        if require_executable and not info.st_mode & 0o111:
            raise LaunchRefused(f"{kind}_NOT_EXECUTABLE")
        got = _hash_fd(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        if got != expected_sha256:
            raise LaunchRefused(f"{kind}_DIGEST_MISMATCH: expected "
                                f"{expected_sha256} got {got}")
    except Exception:
        os.close(fd)
        raise
    return fd


def open_verified_launcher(path, expected_sha256: str) -> int:
    """Verify and hold the frozen boundary-launcher executable."""
    return _open_verified(path, expected_sha256, "LAUNCHER", False)


def open_verified_auditor_executable(path, expected_sha256: str) -> int:
    """CR-EBS-S1-006: verify and HOLD the LIVE auditor executable —
    regular + EXECUTABLE + exact SHA-256 of the ALREADY-OPEN fd; every
    refusal carries the PREEXEC_EXECUTABLE_IDENTITY_FAIL contract
    (PREEXEC, authority unconsumed, no same-attempt retry)."""
    return _open_verified(path, expected_sha256,
                          "PREEXEC_EXECUTABLE_IDENTITY_FAIL", True)


def make_invocation_fd(argv_list) -> int:
    """CR-EBS-S1-006 exact-invocation transfer: a sealed read-only memfd
    carrying the EXACT frozen auditor argv as canonical binding bytes
    (canonical_bytes of the validated list).  The boundary launcher reads
    THIS fd (AUDITOR_INVOCATION_FD); no caller string, argv tail, or
    environment override can enter the auditor client's argv."""
    fd = memfd_create("ebs-auditor-invocation",
                      MFD_CLOEXEC | MFD_ALLOW_SEALING)
    try:
        os.write(fd, canonical_bytes(list(argv_list)))
        os.lseek(fd, 0, os.SEEK_SET)
        fcntl.fcntl(fd, F_ADD_SEALS, REQUIRED_SEALS)
        if fcntl.fcntl(fd, F_GET_SEALS) & REQUIRED_SEALS != REQUIRED_SEALS:
            raise LaunchRefused("INVOCATION_SPEC_SEAL_INCOMPLETE")
    except Exception:
        os.close(fd)
        raise
    return fd


# Runtime EBS self-identity verification (design §6.2; remediation of
# AUCDEV023-CR-EBS-003).  NON-CIRCULAR construction (documented in
# README.md + remediation report): package_sha256 lives INSIDE the
# manifest and covers the manifest document EXCLUDING its own field;
# manifest_sha256 covers the raw manifest bytes; the binding pins BOTH
# independently, so a regenerated manifest cannot bless modified source.


def verify_package_identity(root, expected_manifest_sha256: str,
                            expected_package_sha256: str) -> dict:
    """Fail-closed verification of the package at root: BOTH pinned
    identities, per-file size/SHA-256, exact payload-set equality (unsafe
    row paths cannot match the walked set), int-typed non-negative row
    byte counts (bool refused).  Strict JSON parse (duplicate keys and
    non-finite refused); returned as "document" for cross-binding."""
    try:
        fd = os.open(os.path.join(os.fspath(root), PACKAGE_MANIFEST),
                     os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise LaunchRefused(f"PACKAGE_MANIFEST_UNOPENABLE: {exc!r}") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise LaunchRefused("PACKAGE_MANIFEST_NOT_REGULAR_FILE")
        data = b""
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            data += chunk
    finally:
        os.close(fd)
    try:
        doc = strict_loads(data)   # duplicate keys / non-finite refused
    except BindingError as exc:
        raise LaunchRefused(f"PACKAGE_MANIFEST_MALFORMED: {exc}") from exc
    if not isinstance(doc, dict):
        raise LaunchRefused("PACKAGE_MANIFEST_NOT_AN_OBJECT")
    live_manifest = hashlib.sha256(data).hexdigest()
    declared = doc.get("package_sha256")
    if not isinstance(declared, str) or len(declared) != 64:
        raise LaunchRefused("PACKAGE_IDENTITY_FIELD_ABSENT_OR_MALFORMED")
    identity_source = dict(doc)
    del identity_source["package_sha256"]
    if hashlib.sha256(json.dumps(identity_source, sort_keys=True,
                                 separators=(",", ":")).encode()
                      ).hexdigest() != declared:
        raise LaunchRefused("PACKAGE_IDENTITY_NOT_SELF_CONSISTENT: the "
                            "manifest package_sha256 does not match the "
                            "digest of the manifest excluding that field")
    if live_manifest != expected_manifest_sha256:
        raise LaunchRefused(f"LIVE_MANIFEST_IDENTITY_MISMATCH: binding "
                            f"pins {expected_manifest_sha256} but live "
                            f"manifest is {live_manifest}")
    if declared != expected_package_sha256:
        raise LaunchRefused(f"EBS_PACKAGE_IDENTITY_MISMATCH: binding pins "
                            f"{expected_package_sha256} but live package "
                            f"identity is {declared}")
    rows = doc.get("files")
    if not isinstance(rows, list) or not rows:
        raise LaunchRefused("PACKAGE_MANIFEST_FILES_INVALID")
    recorded = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != \
                {"path", "bytes", "sha256"} or \
                not isinstance(row["path"], str) or row["path"] in recorded:
            raise LaunchRefused(f"PACKAGE_MANIFEST_ROW_INVALID: {row!r}")
        size = row["bytes"]
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise LaunchRefused(f"PACKAGE_MANIFEST_ROW_BYTES_TYPE_INVALID: "
                                f"{size!r} for row {row['path']!r}")
        recorded[row["path"]] = row
    # Walk the LIVE tree: every regular file must be a manifest row with
    # exactly the recorded size/SHA-256; unrecorded files/rows refused.
    root = os.fspath(root)
    total_bytes = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in dirnames[:]:
            if name == "__pycache__":
                dirnames.remove(name)
            elif os.path.islink(os.path.join(dirpath, name)):
                raise LaunchRefused(f"PACKAGE_TREE_SYMLINK_DIR: {name}")
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if rel == PACKAGE_MANIFEST:
                continue    # the manifest itself is byte-pinned above
            row = recorded.pop(rel, None)
            if row is None or not stat.S_ISREG(os.lstat(full).st_mode):
                raise LaunchRefused(f"PACKAGE_PAYLOAD_UNRECORDED_OR_NOT_"
                                    f"REGULAR: {rel}")
            try:
                fd = os.open(full, os.O_RDONLY | os.O_NOFOLLOW)
            except OSError as exc:
                raise LaunchRefused(f"PACKAGE_PAYLOAD_OPEN_REFUSED: {rel}: "
                                    f"{exc!r}") from exc
            try:
                if os.fstat(fd).st_size != row["bytes"] or \
                        _hash_fd(fd) != row["sha256"]:
                    raise LaunchRefused(f"PACKAGE_PAYLOAD_MISMATCH: {rel} "
                                        f"recorded size/hash does not "
                                        f"match the live file")
            finally:
                os.close(fd)
            total_bytes += row["bytes"]
    if recorded:
        raise LaunchRefused(f"PACKAGE_PAYLOAD_MISSING_FROM_LIVE_TREE: "
                            f"{sorted(recorded)}")
    return {"files": len(rows), "bytes": total_bytes,
            "manifest_sha256": live_manifest, "package_sha256": declared,
            "document": doc}


def verify_live_package_identity(binding) -> dict:
    """Production self-verification entry: verifies THE EXECUTING EBS
    PACKAGE against the binding pins; takes no root/flag/env argument,
    and every Supervisor construction runs it before gates/authority."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return verify_package_identity(
        root, binding.ebs_package["manifest_sha256"],
        binding.ebs_package["package_sha256"])


def verify_event_package(root, binding) -> dict:
    """(CR-EBS-REM-001) Fail-closed verification of the frozen event
    package at root against the binding, BEFORE gates are reachable.
    Reuses verify_package_identity (no second package verifier) for the
    pinned identities and per-file/payload-set checks; then enforces the
    strict versioned event-manifest contract (exact key set + schema
    tag) and transport_binding == the binding's own projection compared
    as canonical JSON bytes — so an internally-valid binding with
    substituted component identities under the SAME frozen package
    identity, or a regenerated self-consistent package with updated
    pins, both fail closed here."""
    result = verify_package_identity(
        os.fspath(root), binding.event_package["manifest_sha256"],
        binding.event_package["package_sha256"])
    manifest = result["document"]
    keys = set(manifest)
    if keys != EVENT_MANIFEST_KEYS:
        raise LaunchRefused(
            f"EVENT_MANIFEST_KEYS_INVALID: "
            f"unknown={sorted(keys - EVENT_MANIFEST_KEYS)} "
            f"missing={sorted(EVENT_MANIFEST_KEYS - keys)}")
    if manifest["schema"] != EVENT_MANIFEST_SCHEMA:
        raise LaunchRefused(
            f"EVENT_MANIFEST_SCHEMA_UNEXPECTED: {manifest['schema']!r}")
    if canonical_bytes(manifest["transport_binding"]) != canonical_bytes(
            binding_projection(binding)):
        raise LaunchRefused(
            "EVENT_PACKAGE_PROJECTION_MISMATCH: the frozen event package "
            "declares component identities that differ from this binding")
    return result


# --- dynamic runtime gates (CR-EBS-S1-001; S1-002 adds the second) -----
# Each gate is an EVENT-PACKAGE-SIDE trusted component: the EBS implements
# NO resource thresholds, route/DNS policy, or networking — it binds the
# exact frozen artifact, verifies/opens it safely, executes the verified
# fd at the correct lifecycle point, binds the invocation to the attempt
# context, validates the result envelope, records it, and fails closed.
# No subprocess, no networking, no daemon: the SAME low-level fork +
# verified-fd exec primitives the launcher path already uses.


def _open_bound_artifact(event_package_root, descriptor, rows,
                         label: str) -> int:
    """Shared verified-open core for a frozen EVENT-PACKAGE-SIDE
    executable artifact (runtime gate or structural validator): the
    descriptor path must be a manifest row of the ALREADY-VERIFIED
    package, the artifact is opened with NO final-symlink following,
    required regular + executable, hashed as the ALREADY-OPEN fd against
    the descriptor's exact SHA-256, rewound, and the verified open fd is
    returned (held for exactly-once live execution)."""
    if descriptor["path"] not in rows:
        raise LaunchRefused(
            f"{label}_NOT_PACKAGE_MANIFEST_ROW: {descriptor['path']!r}")
    path = os.path.join(os.fspath(event_package_root), descriptor["path"])
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise LaunchRefused(f"{label}_OPEN_REFUSED: {exc!r}") from exc
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise LaunchRefused(f"{label}_NOT_REGULAR_FILE")
        if not info.st_mode & 0o111:
            raise LaunchRefused(f"{label}_NOT_EXECUTABLE")
        if _hash_fd(fd) != descriptor["sha256"]:
            raise LaunchRefused(f"{label}_ARTIFACT_DIGEST_MISMATCH: live "
                                "artifact differs from the bound descriptor "
                                "SHA-256")
    except Exception:
        os.close(fd)
        raise
    os.lseek(fd, 0, os.SEEK_SET)
    return fd


def open_runtime_gate(event_package_root, binding, event_manifest,
                      gate: str) -> int:
    """Open + verify ONE frozen runtime-gate artifact (by gate name)
    from the ALREADY-VERIFIED event-package tree and return the verified
    open fd (held for exactly-once live execution)."""
    return _open_bound_artifact(
        event_package_root, binding.runtime_gates[gate],
        {row["path"] for row in event_manifest["files"]}, gate)


def open_output_validator(event_package_root, binding,
                          event_manifest) -> int:
    """CR-EBS-S1-007: open + verify the frozen STRUCTURAL OUTPUT
    VALIDATOR artifact from the ALREADY-VERIFIED event-package tree and
    return the verified open fd, HELD at Supervisor construction — the
    SAME no-final-symlink / regular + executable / exact descriptor
    SHA-256 discipline as a runtime gate.  There is NO public API to
    supply a validator path: caller substitution after package freeze is
    impossible."""
    return _open_bound_artifact(
        event_package_root, binding.output_validator,
        {row["path"] for row in event_manifest["files"]},
        "OUTPUT_VALIDATOR")


def _kill_and_reap(child_pid: int) -> None:
    """Bounded-failure cleanup: SIGKILL the gate child and reap it so no
    unbounded authority process survives a refusal."""
    try:
        os.kill(child_pid, SIGKILL)
    except OSError:
        pass
    try:
        os.waitpid(child_pid, 0)
    except OSError:
        pass


def _close_all_except(keep) -> None:
    """Close every open fd not in keep (child-side hygiene)."""
    for entry in os.listdir("/proc/self/fd"):
        fd = int(entry)
        if fd not in keep:
            try:
                os.close(fd)
            except OSError:
                pass


def _close_fds(*fds) -> None:
    """Close every non-None fd, absorbing close failures: bounded
    parent-side cleanup paths (gate/validator runner, attempt pipes,
    held authority fds) must never raise on the way out."""
    for fd in fds:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass


def _sanitize_structural_diagnostic(stderr: bytes) -> str:
    """(EXEC03-001) Bounded STRUCTURAL-ONLY diagnostic grammar for the
    frozen first-pass output validator: accept the captured stderr ONLY
    when its first line is the frozen VALIDATION_ERROR emission, reduce
    it to the pre-colon structural token, and keep that token ONLY when
    it is a short uppercase [A-Z0-9_] identifier.  Everything else —
    parser prose, repr'd report values, duplicate-key names, codec
    messages, arbitrary child output, oversize or non-UTF-8 channels —
    yields "" (the caller falls back to the generic bounded refusal).
    A returned token therefore can never contain report prose,
    credentials, paths or any model/auditor text."""
    if not stderr or len(stderr) > VALIDATOR_STDERR_MAX:
        return ""
    try:
        first = stderr.decode("utf-8").splitlines()[0].strip()
    except (UnicodeDecodeError, IndexError):
        return ""
    if not first.startswith(STRUCTURAL_TOKEN_PREFIX):
        return ""
    token = first[len(STRUCTURAL_TOKEN_PREFIX):].split(":", 1)[0].strip()
    if not 1 <= len(token) <= 128:
        return ""
    if not all(ch in STRUCTURAL_TOKEN_CHARS for ch in token):
        return ""
    return token


def _gate_child(gate_fd: int, result_w: int, devnull: int,
                argv, env: dict, report_fd: int = None,
                stderr_w: int = None) -> None:
    """Child-side preparation for a runtime gate or the structural
    validator: stdout is the bounded result pipe, stdin/stderr are
    devnull (stderr EXCEPT the structural validator, whose writable
    bounded stderr_w pipe replaces the read-only devnull on fd 2 —
    EXEC03-001), NO credential fd is inherited (custody never enters
    this path and the child receives no launch authority), every other
    fd is closed, and the ALREADY-VERIFIED open gate fd is exec'd
    (identity-preserving; no pathname re-open).  When report_fd is given
    (validator only) the sealed immutable report snapshot is inherited at
    the fixed VALIDATOR_REPORT_FD slot.  Never returns."""
    try:
        os.dup2(devnull, 0)
        os.dup2(result_w, 1)
        os.dup2(stderr_w if stderr_w is not None else devnull, 2)
        exec_target = gate_fd
        keep = {0, 1, 2, gate_fd}
        if report_fd is not None:
            # alias-safe slot remap (the _child_setup discipline): take
            # DISTINCT fresh copies of BOTH the exec target and the
            # report, then remap the report into VALIDATOR_REPORT_FD —
            # the dup2 can only ever clobber a copy or an unrelated
            # inherited fd, never the exec target (which falls back to
            # the still-open original when its copy occupies the slot).
            exec_copy = os.dup(gate_fd)
            report_second = os.dup(os.dup(report_fd))
            os.dup2(report_second, VALIDATOR_REPORT_FD)
            exec_target = exec_copy if exec_copy != VALIDATOR_REPORT_FD \
                else gate_fd
            keep = {0, 1, 2, exec_target, VALIDATOR_REPORT_FD}
        _close_all_except(keep)
        fcntl.fcntl(exec_target, fcntl.F_SETFD, 0)  # survives exec
        if report_fd is not None:
            fcntl.fcntl(VALIDATOR_REPORT_FD, fcntl.F_SETFD, 0)
        establish_non_dumpable()
        fd_exec(exec_target, argv, env)
    except BaseException:
        os._exit(CHILD_EXIT_EXEC_FAIL)


def _run_runtime_gate(gate: str, gate_fd: int, argv, env: dict,
                      timeout: float = RUNTIME_GATE_TIMEOUT,
                      report_bytes: bytes = None,
                      capture_stderr: bool = False) -> bytes:
    """Execute the verified gate/validator fd EXACTLY ONCE with a
    bounded fail-closed timeout; return the raw result bytes
    (size-bounded).  Any fork/exec failure, hang past the deadline,
    oversized output, or non-zero child exit refuses.  report_bytes (the
    structural validator only) is delivered to the child as a sealed
    read-only memfd at VALIDATOR_REPORT_FD — the validator sees exactly
    the immutable clean snapshot, never a pathname, never a credential.
    capture_stderr (EXEC03-001, the structural validator only) gives
    the child a WRITABLE bounded stderr pipe instead of the read-only
    /dev/null fd 2 every other gate keeps, reads it under the same
    deadline/size bounds (oversize refuses fail-closed), and on a
    non-zero exit appends ONLY the sanitized structural token
    (_sanitize_structural_diagnostic) to the bounded refusal detail —
    never arbitrary child output."""
    report_fd = None
    if report_bytes is not None:
        # the EXACT immutable clean snapshot on a sealed read-only memfd
        # (DISTINCT name from every EBS-held authority memfd; the child
        # inherits ONLY this report channel)
        report_fd = memfd_create("ebs-report-snapshot",
                                 MFD_CLOEXEC | MFD_ALLOW_SEALING)
        try:
            os.write(report_fd, report_bytes)
            os.lseek(report_fd, 0, os.SEEK_SET)
            fcntl.fcntl(report_fd, F_ADD_SEALS, REQUIRED_SEALS)
            if fcntl.fcntl(report_fd, F_GET_SEALS) & REQUIRED_SEALS != \
                    REQUIRED_SEALS:
                raise LaunchRefused("REPORT_SNAPSHOT_SEAL_INCOMPLETE")
        except Exception:
            os.close(report_fd)
            raise
    err_r = err_w = None
    if capture_stderr:
        err_r, err_w = os.pipe()
        os.set_blocking(err_r, False)
    result_r, result_w = os.pipe()
    devnull = os.open(os.devnull, os.O_RDONLY)
    child_pid = None
    try:
        try:
            child_pid = os.fork()
        except OSError as exc:
            raise LaunchError(f"{gate}_FORK_FAILED: {exc!r}") from exc
        if child_pid == 0:
            _gate_child(gate_fd, result_w, devnull, argv, env, report_fd,
                        err_w)
        os.close(result_w)
        result_w = None
        if err_w is not None:
            os.close(err_w)
            err_w = None
        os.close(devnull)
        devnull = None
        if report_fd is not None:
            os.close(report_fd)     # parent copy: only the child holds it
            report_fd = None
        os.set_blocking(result_r, False)
        deadline = time.monotonic() + timeout
        output = b""
        stderr_out = b""
        eof = False
        exitcode = None
        while True:
            if time.monotonic() >= deadline:
                _kill_and_reap(child_pid)
                raise LaunchRefused(
                    f"{gate}_TIMEOUT: did not finish within "
                    f"{timeout}s; failing closed")
            progressed = False
            if not eof:
                try:
                    chunk = os.read(result_r, 65536)
                except BlockingIOError:
                    chunk = None
                if chunk is not None:
                    progressed = True
                    if not chunk:
                        eof = True
                    else:
                        output += chunk
                        if len(output) > RUNTIME_GATE_RESULT_MAX:
                            _kill_and_reap(child_pid)
                            raise LaunchRefused(
                                f"{gate}_OUTPUT_TOO_LARGE: emitted more "
                                f"than {RUNTIME_GATE_RESULT_MAX} result "
                                f"bytes")
            if err_r is not None:
                try:
                    chunk = os.read(err_r, 65536)
                except BlockingIOError:
                    chunk = None
                if chunk is not None and chunk:
                    progressed = True
                    stderr_out += chunk
                    if len(stderr_out) > VALIDATOR_STDERR_MAX:
                        _kill_and_reap(child_pid)
                        raise LaunchRefused(
                            f"{gate}_STDERR_TOO_LARGE: emitted more "
                            f"than {VALIDATOR_STDERR_MAX} stderr bytes; "
                            f"failing closed")
            if exitcode is None:
                waited_pid, status = os.waitpid(child_pid, os.WNOHANG)
                if waited_pid == child_pid:
                    exitcode = os.waitstatus_to_exitcode(status)
                    progressed = True
            if eof and exitcode is not None:
                break
            if not progressed:
                time.sleep(0.01)               # bounded poll, no busy spin
        if err_r is not None and exitcode is not None:
            # the child is reaped: its writes are complete — one final
            # bounded nonblocking drain of the stderr channel
            while True:
                try:
                    chunk = os.read(err_r, 65536)
                except BlockingIOError:
                    break
                if not chunk:
                    break
                stderr_out += chunk
                if len(stderr_out) > VALIDATOR_STDERR_MAX:
                    raise LaunchRefused(
                        f"{gate}_STDERR_TOO_LARGE: emitted more than "
                        f"{VALIDATOR_STDERR_MAX} stderr bytes; failing "
                        f"closed")
        if exitcode != 0:
            reason = ("EXEC_FAILED" if exitcode == CHILD_EXIT_EXEC_FAIL
                      else "NONZERO_EXIT")
            detail = f"{gate}_{reason}: exited {exitcode}"
            if capture_stderr:
                token = _sanitize_structural_diagnostic(stderr_out)
                if token:
                    detail += f"; structural_error={token}"
            raise LaunchRefused(detail)
        if not output:
            raise LaunchRefused(f"{gate}_OUTPUT_MISSING: no result bytes")
        return output
    finally:
        _close_fds(result_r, result_w, devnull, report_fd, err_r, err_w)


def _strict_gate_envelope(output: bytes, binding, gate: str, fields,
                          schema: str) -> dict:
    """Common strict fail-closed envelope core shared by BOTH runtime
    gates: strict JSON (duplicate keys and non-finite refused), object
    shape, exact top-level key set, exact schema tag, exact
    event/role/attempt match with the binding, and top-level status PASS.
    PASS is never inferred from the exit code.  Returns the parsed
    result; per-gate payload validation continues in the caller."""
    try:
        result = strict_loads(output)
    except BindingError as exc:
        raise LaunchRefused(f"{gate}_RESULT_MALFORMED: {exc}") from exc
    if not isinstance(result, dict):
        raise LaunchRefused(f"{gate}_RESULT_NOT_AN_OBJECT")
    keys = set(result)
    expected = set(fields)
    if keys != expected:
        raise LaunchRefused(
            f"{gate}_RESULT_KEYS_INVALID: "
            f"unknown={sorted(keys - expected)} "
            f"missing={sorted(expected - keys)}")
    if result["schema"] != schema:
        raise LaunchRefused(f"{gate}_RESULT_SCHEMA_UNEXPECTED: "
                            f"{result['schema']!r}")
    if result["event_id"] != binding.event_id or \
            result["auditor_role"] != binding.auditor_role or \
            result["attempt_id"] != binding.attempt_id:
        raise LaunchRefused(f"{gate}_RESULT_CONTEXT_MISMATCH: result "
                            "event/role/attempt differ from the binding")
    if result["status"] != "PASS":
        raise LaunchRefused(f"{gate}_RESULT_NOT_PASS: {result['status']!r}")
    return result


def _result_evidence(prefix: str, result: dict) -> dict:
    """Durable fresh-evidence fields for one validated gate result: the
    canonical result JSON string plus its exact SHA-256 and byte size."""
    canonical = canonical_bytes(result).decode()
    return {f"{prefix}_result": canonical,
            f"{prefix}_result_sha256": hashlib.sha256(
                canonical.encode()).hexdigest(),
            f"{prefix}_result_size": len(canonical.encode())}


def _validate_resource_gate_result(output: bytes, binding) -> dict:
    """Strict fail-closed validation of the FRESH resource-gate result
    envelope (AUCDEV-023-RESOURCE-GATE-RESULT-V1): the shared envelope
    core plus EXACTLY three samples each explicitly PASS with an object
    detail.  A top-level PASS never overrides a failed sample."""
    result = _strict_gate_envelope(output, binding, "RESOURCE_GATE",
                                   RESOURCE_GATE_RESULT_FIELDS,
                                   RESOURCE_GATE_RESULT_SCHEMA)
    samples = result["samples"]
    if not isinstance(samples, list) or len(samples) != RESOURCE_GATE_SAMPLES:
        raise LaunchRefused(
            f"RESOURCE_GATE_SAMPLE_COUNT_INVALID: expected exactly "
            f"{RESOURCE_GATE_SAMPLES} samples, got "
            f"{len(samples) if isinstance(samples, list) else samples!r}")
    for index, sample in enumerate(samples):
        if not isinstance(sample, dict) or \
                set(sample) != set(RESOURCE_GATE_SAMPLE_FIELDS):
            raise LaunchRefused(
                f"RESOURCE_GATE_SAMPLE_INVALID_AT_{index}")
        if sample["status"] != "PASS":
            raise LaunchRefused(
                f"RESOURCE_GATE_SAMPLE_NOT_PASS_AT_{index}: "
                f"{sample['status']!r}")
        if not isinstance(sample["detail"], dict):
            raise LaunchRefused(
                f"RESOURCE_GATE_SAMPLE_DETAIL_INVALID_AT_{index}")
    return _result_evidence("resource_gate", result)


def _validate_network_readiness_result(output: bytes, binding) -> dict:
    """Strict fail-closed validation of the FRESH network-readiness
    result envelope (AUCDEV-023-NETWORK-READINESS-RESULT-V1): the shared
    envelope core plus the exact transport-binding context (provider
    role, boundary launcher SHA-256, sandbox profile id — all from the
    binding) and the EXACT checks key set route + resolver, each check
    an exact {status, detail} object with status PASS and a bounded
    JSON-object detail.  A top-level PASS never overrides a failed
    route/resolver check."""
    result = _strict_gate_envelope(output, binding, "NETWORK_READINESS",
                                   NETWORK_READINESS_RESULT_FIELDS,
                                   NETWORK_READINESS_RESULT_SCHEMA)
    if result["provider_role"] != \
            binding.auditor_identity["provider_role"] or \
            result["boundary_launcher_sha256"] != \
            binding.boundary_launcher["sha256"] or \
            result["sandbox_profile_id"] != binding.sandbox_profile_id:
        raise LaunchRefused("NETWORK_READINESS_RESULT_CONTEXT_MISMATCH: "
                            "result provider/launcher/profile differ from "
                            "the binding")
    checks = result["checks"]
    if not isinstance(checks, dict) or set(checks) != \
            set(NETWORK_READINESS_CHECKS):
        raise LaunchRefused(
            f"NETWORK_READINESS_CHECKS_INVALID: expected exactly "
            f"{sorted(NETWORK_READINESS_CHECKS)}, got "
            f"{sorted(checks) if isinstance(checks, dict) else checks!r}")
    for name in NETWORK_READINESS_CHECKS:
        check = checks[name]
        if not isinstance(check, dict) or \
                set(check) != set(NETWORK_READINESS_CHECK_FIELDS) or \
                not isinstance(check["detail"], dict):
            raise LaunchRefused(f"NETWORK_READINESS_CHECK_INVALID: {name} "
                                "must be an object with exactly status and "
                                "an object detail")
        if check["status"] != "PASS":
            raise LaunchRefused(f"NETWORK_READINESS_CHECK_NOT_PASS: "
                                f"{name} {check['status']!r}")
    return _result_evidence("network_readiness", result)


_RUNTIME_GATE_VALIDATORS = {
    "NETWORK_READINESS": _validate_network_readiness_result,
    "RESOURCE_GATE": _validate_resource_gate_result,
}


VALIDATOR_RESULT_FIELDS = ("schema", "status", "event_id", "auditor_role",
                           "attempt_id", "output_name", "report_sha256",
                           "report_size")


def _validate_validator_result(output: bytes, binding, digest: str,
                               size: int) -> None:
    """Strict fail-closed validation of the structural-validator result
    envelope (AUCDEV-023-REPORT-VALIDATOR-RESULT-V1; the CR-EBS-S1-007
    §25 barrier): the shared envelope core PLUS exact match of
    output_name/report_sha256/report_size with the EXACT screened
    immutable snapshot that was validated; PASS is never inferred from
    the exit code."""
    result = _strict_gate_envelope(output, binding, "OUTPUT_VALIDATOR",
                                   VALIDATOR_RESULT_FIELDS,
                                   VALIDATOR_RESULT_SCHEMA)
    if result["output_name"] != binding.output_identity["name"] or \
            result["report_sha256"] != digest or \
            result["report_size"] != size:
        raise LaunchRefused(
            "OUTPUT_VALIDATOR_RESULT_SNAPSHOT_MISMATCH: result output/"
            "digest/size differ from the exact screened snapshot")


def _child_setup(launcher_fd: int, metadata_w: int, fail_w: int,
                 devnull: int, custody_fd: int, auditor_fd: int,
                 invocation_fd: int, argv, env: dict) -> None:
    """Child-side preparation: session isolation, fixed fd contract,
    hygiene, then exec of the verified open fd.  Never returns.  The
    boundary child first establishes its OWN SESSION (CR-EBS-S1-008:
    setsid before exec, so the attempt's whole descendant tree is
    killable as one exact process group on timeout — never an unrelated
    host process).  The fixed inherited contract (S1-004/-006):
    CRED_FD=3 sealed custody, FAIL_FD=4 CLOEXEC exec-fail pipe,
    AUDITOR_EXEC_FD=5 the HELD verified auditor executable,
    AUDITOR_INVOCATION_FD=6 the sealed canonical frozen-argv spec.  The
    remap is alias-safe: every source is first duplicated to fresh fds
    (os.dup never returns an open descriptor, so the phase-one copies are
    distinct and disjoint from every original), which guarantees every
    slot 3-6 is occupied, so the phase-two copies land outside 3-6 and
    the final dup2s can only clobber originals."""
    try:
        os.setsid()
        os.dup2(devnull, 0)
        os.dup2(metadata_w, 1)
        os.dup2(devnull, 2)
        phase_one = [os.dup(src) for src in
                     (custody_fd, fail_w, auditor_fd, invocation_fd)]
        phase_two = [os.dup(copy) for copy in phase_one]
        os.dup2(phase_two[0], CRED_FD)
        os.dup2(phase_two[1], FAIL_FD)
        os.dup2(phase_two[2], AUDITOR_EXEC_FD)
        os.dup2(phase_two[3], AUDITOR_INVOCATION_FD)
        fcntl.fcntl(FAIL_FD, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
        _close_all_except({0, 1, 2, CRED_FD, FAIL_FD, launcher_fd,
                           AUDITOR_EXEC_FD, AUDITOR_INVOCATION_FD})
        for survivor in (launcher_fd, CRED_FD, AUDITOR_EXEC_FD,
                         AUDITOR_INVOCATION_FD):
            fcntl.fcntl(survivor, fcntl.F_SETFD, 0)  # fd contract survives
        establish_non_dumpable()
        fd_exec(launcher_fd, argv, env)
    except BaseException:
        try:
            os.write(FAIL_FD, b"E")
        except OSError:
            pass
        os._exit(CHILD_EXIT_EXEC_FAIL)


@dataclass(frozen=True)
class AttemptResult:
    """Outcome DATA ONLY — never authority (CR-EBS-S1-007).  Returned
    strictly AFTER the attempt reached a terminal outcome:
    returncode/exec_failed/metadata describe the boundary child;
    timed_out marks the EBS-enforced auditor deadline;
    report_state carries the terminal report outcome (REPORT_FROZEN /
    REPORT_MISSING / REPORT_SCREEN_FAIL / REPORT_INVALID, or "" when no
    report phase was semantically appropriate) with the frozen artifact
    digest/size."""
    returncode: int
    exec_failed: bool
    metadata: dict
    timed_out: bool
    report_state: str
    report_sha256: str
    report_size: int


class Supervisor:
    """One-shot controllerless EBS orchestrator for a single attempt.
    Startup ordering (fail closed at every step, before any gate or
    authority operation): (1) runtime EBS package self-identity
    verification; (2) mechanical binding to THIS store (attempt id AND
    binding digest); (3) frozen event-package identity verification
    against the binding's event_package pins; (4) event-package
    transport-projection equality; (5) BOTH runtime-gate artifacts
    (NETWORK_READINESS + RESOURCE_GATE) identity-verified from the
    already-verified package tree and the verified open fds HELD
    (CR-EBS-S1-001/-002); only then does a supervisor capable of the
    single preexec-consumption operation exist.  The event-package root
    is a MANDATORY constructor input — no default, no flag, no
    environment bypass.  No attach/revival constructor exists; an
    existing same-attempt record fails closed at store creation
    (replacement = new operator authority + new attempt id + new EBS
    process + new accounting)."""

    def __init__(self, binding, store: AccountingStore,
                 event_package_root) -> None:
        if not isinstance(store, AccountingStore):
            raise LaunchError("SUPERVISOR_REQUIRES_ACCOUNTING_STORE")
        if not isinstance(event_package_root, (str, os.PathLike)):
            raise LaunchError(
                "SUPERVISOR_REQUIRES_EVENT_PACKAGE_ROOT: a frozen event "
                "package root is mandatory — no default, no bypass")
        verify_live_package_identity(binding)          # (1) live EBS bytes
        if store.attempt_id != binding.attempt_id:     # (2) store binding
            raise LaunchError(
                f"STORE_ATTEMPT_MISMATCH: store holds {store.attempt_id!r} "
                f"but binding declares {binding.attempt_id!r}")
        if store.binding_digest != binding.digest:
            raise LaunchError("STORE_BINDING_DIGEST_MISMATCH: the store "
                              "was not created from this exact binding "
                              "document")
        event_result = verify_event_package(event_package_root, binding)
        self._gate_fds = {              # (5) hold BOTH verified fds
            gate: open_runtime_gate(event_package_root, binding,
                                    event_result["document"], gate)
            for gate in RUNTIME_GATES}
        # (6) CR-EBS-S1-007: hold the verified structural-validator fd
        # from the SAME already-verified package tree (no public API can
        # supply a validator path — no post-freeze substitution exists).
        self._validator_fd = open_output_validator(
            event_package_root, binding, event_result["document"])
        self._binding = binding
        self._store = store
        self._machine = StateMachine(store.last_state or PREPARED)
        self._launcher_fd = None
        self._custody = None       # Supervisor-owned sealed custody (S1-004)
        self._auditor_fd = None    # held verified live auditor executable
        self._invocation_fd = None  # sealed canonical frozen-argv spec
        self._out_dir_fd = None    # pre-opened operator custody dir (S1-007)
        self._staging_path = None
        self._spent = False          # irreversible launch-spent guard
        self._gates_executed = False   # exactly-once runtime gate pair

    @property
    def state(self) -> str:
        return self._machine.state

    @property
    def store(self) -> AccountingStore:
        return self._store

    @property
    def launcher_fd(self):
        return self._launcher_fd

    def _binding_facts(self) -> dict:
        """Complete adopted non-secret binding identity set, durably
        recorded at CONSUMED_PRE_EXEC (design §10; no credential ever
        enters accounting)."""
        b = self._binding
        facts = {"event_id": b.event_id, "auditor_role": b.auditor_role,
                 "target_commit": b.target["commit"],
                 "target_root_tree": b.target["root_tree"],
                 "target_qh_tree": b.target["qh_tree"],
                 "target_skill_tree": b.target["skill_tree"],
                 "prompt_contract_digest": b.prompt_contract_digest,
                 "common_evidence_manifest_digest":
                     b.common_evidence_manifest_digest,
                 "sandbox_profile_id": b.sandbox_profile_id,
                 "provider_role": b.auditor_identity["provider_role"],
                 "adapter_id": b.auditor_identity["adapter_id"],
                 "output_identity_name": b.output_identity["name"],
                 "auditor_executable_identity":
                     b.auditor_identity["executable_identity"],
                 "auditor_executable_version":
                     b.auditor_identity["executable_version"],
                 "auditor_executable_sha256":
                     b.auditor_identity["executable_sha256"],
                 "auditor_invocation_argc": len(b.auditor_invocation),
                 "auditor_invocation_sha256": hashlib.sha256(
                     canonical_bytes(list(b.auditor_invocation))).hexdigest(),
                 "output_validator_identity":
                     b.output_validator["identity"],
                 "output_validator_sha256": b.output_validator["sha256"],
                 "auditor_timeout_seconds":
                     b.execution_limits["auditor_timeout_seconds"],
                 "validator_timeout_seconds":
                     b.execution_limits["validator_timeout_seconds"]}
        for prefix, ident in (("boundary_launcher", b.boundary_launcher),
                              ("tool_wrapper", b.tool_wrapper)):
            facts[f"{prefix}_identity"] = ident["identity"]
            facts[f"{prefix}_sha256"] = ident["sha256"]
        for prefix, pkg in (("event_package", b.event_package),
                            ("ebs_package", b.ebs_package)):
            facts[f"{prefix}_manifest_sha256"] = pkg["manifest_sha256"]
            facts[f"{prefix}_sha256"] = pkg["package_sha256"]
        return facts

    def _execute_runtime_gate(self, gate: str) -> dict:
        """Execute ONE frozen runtime-gate artifact (by gate name) ONCE,
        NOW (all startup identity checks already passed); strictly
        validate the fresh result; return the durable fresh-evidence
        fields for the GATES_PASSED record.  The invocation is bound to
        this attempt's event/role/attempt (NETWORK_READINESS additionally
        receives the binding's non-secret provider/launcher/profile
        transport context) with a clean minimal environment and NO
        credential fd or launch authority exposed to the gate."""
        descriptor = self._binding.runtime_gates[gate]
        fd = self._gate_fds[gate]
        got = _hash_fd(fd)            # held-fd drift check immediately
        os.lseek(fd, 0, os.SEEK_SET)
        if got != descriptor["sha256"]:
            raise LaunchRefused(f"{gate}_FD_DRIFT: the held gate fd no "
                                "longer matches the bound artifact")
        argv = [descriptor["identity"], self._binding.event_id,
                self._binding.auditor_role, self._binding.attempt_id]
        if gate == "NETWORK_READINESS":
            argv += [self._binding.auditor_identity["provider_role"],
                     self._binding.boundary_launcher["sha256"],
                     self._binding.sandbox_profile_id]
        output = _run_runtime_gate(gate, fd, argv,
                                   {"PATH": "/usr/bin:/bin", "LANG": "C"})
        evidence = _RUNTIME_GATE_VALIDATORS[gate](output, self._binding)
        prefix = gate.lower()
        evidence.update({f"{prefix}_identity": descriptor["identity"],
                         f"{prefix}_sha256": descriptor["sha256"],
                         f"{prefix}_result_schema":
                             descriptor["result_schema"]})
        return evidence

    def run_attempt(self, credential_source_fd: int, launcher_path,
                    auditor_executable_path, report_staging_path,
                    output_root) -> AttemptResult:
        """THE single public authority operation (CR-EBS-S1-004/-005/
        -006/-007/-008): the COMPLETE one-shot attempt lifecycle in ONE
        caller-uninterruptible call — custody (role derived ONLY from
        the binding) -> sealed frozen-argv spec -> launcher + LIVE
        auditor executable verified/HELD -> NETWORK_READINESS once ->
        RESOURCE_GATE once LAST -> held-fd re-hash -> durable
        GATES_PASSED -> CONSUMED_PRE_EXEC -> irreversible spend ->
        IMMEDIATE fork/exec (own session) -> EXEC_ATTEMPTED ->
        deadline-bounded wait -> report snapshot -> SAME-custody screen
        -> frozen structural validator on the exact clean snapshot ->
        freeze of the exact screened+validated bytes -> report outcome
        -> TERMINAL -> custody and held fds closed -> AttemptResult.
        No public operation ever returns control in GATES_PASSED,
        CONSUMED_PRE_EXEC, EXEC_ATTEMPTED or any report outcome state;
        no grant, no consume()/execute() split, no adopt_report, no
        finish-later API, no caller surface for a custody object, role,
        argv tail, environment override, timeout, or validator path.
        Inputs: the credential SOURCE fd; the two NON-AUTHORITATIVE
        byte-identity locator paths (each opened once, hashed against
        the binding's exact SHA-256, and HELD); the two NON-AUTHORITATIVE
        report locators (supplied BEFORE any authority is consumed; the
        artifact name derives ONLY from binding.output_identity; the
        output custody directory is pre-opened fail-closed PREEXEC and
        held).  Any pre-consumption failure terminalizes fail-closed
        with authority unconsumed and no same-attempt retry."""
        if not isinstance(credential_source_fd, int) or \
                isinstance(credential_source_fd, bool):
            raise LaunchError(
                "RUN_ATTEMPT_REQUIRES_CREDENTIAL_SOURCE_FD: the public "
                "authority operation ingests a credential SOURCE fd, "
                "never a CredentialCustody or any other object")
        for name, value in (("report_staging_path", report_staging_path),
                            ("output_root", output_root)):
            if not isinstance(value, (str, os.PathLike)):
                raise LaunchError(
                    f"RUN_ATTEMPT_REQUIRES_{name.upper()}: the report "
                    "locators are mandatory path inputs — no default, "
                    "no bypass")
        if self._machine.state != PREPARED:
            raise LaunchError(
                f"RUN_ATTEMPT_REFUSED_STATE_{self._machine.state}: the "
                "single authority operation requires PREPARED")
        if self._launcher_fd is not None or self._custody is not None \
                or self._spent or self._gates_executed:
            raise LaunchError("RUN_ATTEMPT_REFUSED_ALREADY_ADVANCED: "
                              "no second authority operation exists")
        self._gates_executed = True
        try:
            # (S1-007 §21) output custody PRE-OPENED and HELD before any
            # authority is consumed: unsafe/absent custody directories
            # fail closed PREEXEC, and the freeze later happens through
            # THIS fd (no post-exec pathname re-interpretation).
            self._out_dir_fd = open_custody_dir(output_root)
            self._staging_path = os.fspath(report_staging_path)
            # (S1-004) CUSTODY FIRST — non-dumpable ingest, source
            # discipline, bounded read, four seals — BEFORE any gate and
            # BEFORE CONSUMED_PRE_EXEC; the role label comes ONLY from
            # the binding (defense-in-depth re-checked below it).
            self._custody = CredentialCustody.ingest(
                credential_source_fd, self._binding.auditor_role)
            if self._custody.role != self._binding.auditor_role:
                raise LaunchRefused(
                    "CUSTODY_ROLE_MISMATCH: defense-in-depth check — the "
                    "custody role does not equal binding.auditor_role")
            # (S1-006) the exact frozen argv leaves the binding ONLY as
            # canonical bytes on a sealed read-only spec fd.
            self._invocation_fd = make_invocation_fd(
                self._binding.auditor_invocation)
            # Static byte identities BEFORE the dynamic gates (S1-003
            # ordering preserved; S1-006 adds the live auditor
            # executable under the same discipline).
            self._launcher_fd = open_verified_launcher(
                launcher_path, self._binding.boundary_launcher["sha256"])
            self._auditor_fd = open_verified_auditor_executable(
                auditor_executable_path,
                self._binding.auditor_identity["executable_sha256"])
            evidence = {}
            for gate in RUNTIME_GATES:   # NETWORK_READINESS, then the
                evidence.update(self._execute_runtime_gate(gate))
            self._rehash_held("BEFORE_GATES_PASSED")  # gate-interval drift
            self._store.append(GATES_PASSED,       # fsync'd inside append
                               extra=evidence)
            self._machine.transition(GATES_PASSED)   # internal transient
            self._store.append(CONSUMED_PRE_EXEC,   # fsync'd inside append
                               extra=self._binding_facts())
            self._machine.transition(CONSUMED_PRE_EXEC)
        except Exception as exc:
            self._preexec_stop()   # PREPARED/GATES_PASSED -> fail-closed
            if isinstance(exc, LaunchRefused):
                raise
            raise LaunchRefused(f"PREEXEC_CONSUME_RECORD_FAILED: {exc!r}") \
                from exc
        # IRREVERSIBLE SPEND (S1-005): authority is dead in this process
        # from here on; consumption is IMMEDIATELY followed by the fork
        # attempt inside the SAME public call — control never returns to
        # the caller between CONSUMED_PRE_EXEC and the exec attempt.
        self._spent = True
        return self._fork_and_launch()

    def _rehash_held(self, phase: str) -> None:
        """Re-hash the HELD launcher + auditor-executable fds (S1-006):
        before gate acceptance (gate-interval drift stays PREEXEC and
        authority-unconsumed) and again post-consumption inside
        _fork_and_launch (consumed fail-closed semantics)."""
        got = _hash_fd(self._launcher_fd)
        os.lseek(self._launcher_fd, 0, os.SEEK_SET)
        if got != self._binding.boundary_launcher["sha256"]:
            raise LaunchRefused(
                f"LAUNCHER_DIGEST_MISMATCH_{phase}: expected "
                f"{self._binding.boundary_launcher['sha256']} got {got}")
        got = _hash_fd(self._auditor_fd)
        os.lseek(self._auditor_fd, 0, os.SEEK_SET)
        if got != self._binding.auditor_identity["executable_sha256"]:
            raise LaunchRefused(
                f"AUDITOR_EXECUTABLE_IDENTITY_FAIL_{phase}: expected "
                f"{self._binding.auditor_identity['executable_sha256']} "
                f"got {got}")

    def _fork_and_launch(self) -> AttemptResult:
        """Post-consumption continuation (S1-005/-007/-008), called ONLY
        from run_attempt after the irreversible spend: defense-in-depth
        re-hash, IMMEDIATE fork/exec into a DEDICATED SESSION,
        EXEC_ATTEMPTED accounting, the MONOTONIC-deadline bounded wait
        (all parent pipes NONBLOCKING), timeout kill of the EXACT
        attempt process group with consumed terminal accounting, and the
        process-bound report lifecycle — all before any return.  The
        launcher's argv carries only EBS-bound non-secret context; the
        auditor argv travels on the sealed AUDITOR_INVOCATION_FD; the
        child environment is entirely EBS-defined (S1-006)."""
        child_pid = None
        waited = False
        md_r = md_w = fail_r = fail_w = devnull = None
        fail_byte = b""
        metadata_raw = b""
        timeout = self._binding.execution_limits["auditor_timeout_seconds"]
        timed_out = False
        status = 0
        try:
            self._rehash_held("AFTER_CONSUMPTION")
            argv = [self._binding.boundary_launcher["identity"],
                    "--role", self._binding.auditor_role,
                    "--attempt", self._binding.attempt_id,
                    "--event", self._binding.event_id]
            child_env = {"PATH": "/usr/bin:/bin", "LANG": "C"}
            md_r, md_w = os.pipe()
            fail_r, fail_w = os.pipe()
            devnull = os.open(os.devnull, os.O_RDONLY)
            try:
                child_pid = os.fork()
            except OSError as exc:
                raise LaunchError(f"FORK_FAILED: {exc!r}") from exc
            if child_pid == 0:
                _child_setup(self._launcher_fd, md_w, fail_w, devnull,
                             self._custody.fd, self._auditor_fd,
                             self._invocation_fd, argv, child_env)
            os.close(md_w)
            os.close(fail_w)
            os.close(devnull)
            md_w = fail_w = devnull = None
            self._store.append(EXEC_ATTEMPTED, extra={"child_pid":
                                                      child_pid})
            self._machine.transition(EXEC_ATTEMPTED)
            # (S1-008) bounded wait: BOTH pipes nonblocking, WNOHANG
            # reap, monotonic deadline from the FROZEN binding — no
            # parent-side child interaction can block past it.
            os.set_blocking(fail_r, False)
            os.set_blocking(md_r, False)
            deadline = time.monotonic() + timeout
            fail_eof = False
            md_eof = False
            exitcode = None
            grace_deadline = None
            while True:
                if time.monotonic() >= deadline:
                    # deadline boundary race: one final nonblocking reap
                    # decides timeout-vs-completed honestly
                    wpid, wstatus = os.waitpid(child_pid, os.WNOHANG)
                    if wpid == child_pid:
                        waited = True
                        status = wstatus
                        exitcode = os.waitstatus_to_exitcode(status)
                        break
                    timed_out = True
                    break
                progressed = False
                if not fail_eof:
                    try:
                        chunk = os.read(fail_r, 1)
                    except BlockingIOError:
                        chunk = None
                    if chunk is not None:
                        progressed = True
                        if chunk:
                            fail_byte = chunk
                        else:
                            fail_eof = True
                if exitcode is None:
                    wpid, wstatus = os.waitpid(child_pid, os.WNOHANG)
                    if wpid == child_pid:
                        waited = True
                        status = wstatus
                        exitcode = os.waitstatus_to_exitcode(status)
                        progressed = True
                if not md_eof and len(metadata_raw) < METADATA_MAX:
                    try:
                        chunk = os.read(md_r, 65536)
                    except BlockingIOError:
                        chunk = None
                    if chunk is not None:
                        progressed = True
                        if chunk:
                            metadata_raw += chunk
                        else:
                            md_eof = True
                if fail_eof and exitcode is not None:
                    if md_eof:
                        break                    # complete: reaped + EOFs
                    if grace_deadline is None:
                        # bounded final metadata drain (a descendant may
                        # still hold the write end; never an unbounded
                        # read — the overall deadline still bounds it)
                        grace_deadline = time.monotonic() + METADATA_GRACE
                    elif time.monotonic() >= grace_deadline:
                        break
                if not progressed:
                    time.sleep(0.01)               # bounded poll, no spin
        except BaseException as exc:
            # (S1-009) ANY post-consumption parent-side failure —
            # including failures AFTER the durable EXEC_ATTEMPTED
            # transition — gets the SAME centralized fail-closed
            # settlement (remaining parent fds closed, the EXACT attempt
            # process group killed and reaped, then
            # _settle_post_consumption); the original failure re-raises
            # only when the durable settlement completed, else the exact
            # accounting-incompleteness error chaining it; never
            # relabeled unconsumed, no same-attempt retry.
            _close_fds(md_r, md_w, fail_r, fail_w, devnull)
            md_r = fail_r = None
            if child_pid and not waited:
                self._kill_attempt_group(child_pid)
                try:
                    os.waitpid(child_pid, 0)   # deterministic post-kill reap
                except OSError:
                    pass
            reason = ("PRE_EXEC_FAILURE_AFTER_CONSUMPTION"
                      if self._machine.state == CONSUMED_PRE_EXEC
                      else "PARENT_FAILURE_AFTER_EXEC_ATTEMPTED")
            self._settle_post_consumption(
                None, None,
                {"terminal_reason": f"{reason}: {exc!r}"[:256]},
                original_error=exc)
            raise   # backstop: settlement re-raises with original_error
        finally:
            _close_fds(md_r, fail_r)
        if timed_out:
            # (S1-008 §16/§17 semantics under the S1-009 centralized
            # settlement): timeout is AFTER durable CONSUMED_PRE_EXEC —
            # authority CONSUMED, model engagement CONSUMED FAIL-CLOSED,
            # no report accepted; the exact process group is killed and
            # the direct child reaped BEFORE the settlement, and a
            # TERMINAL-accounting failure raises the exact
            # incompleteness error — never a timed-out AttemptResult.
            self._kill_attempt_group(child_pid)
            if not waited:
                _, status = os.waitpid(child_pid, 0)
                waited = True
            self._settle_post_consumption(None, None, {
                "terminal_reason": "TIMEOUT_AFTER_CONSUMPTION",
                "auditor_timeout_seconds": timeout,
                "child_pid": child_pid})
            return AttemptResult(os.waitstatus_to_exitcode(status), False,
                                 {}, True, "", "", 0)
        metadata = None
        if metadata_raw:
            try:
                metadata = json.loads(metadata_raw.decode())
            except (UnicodeDecodeError, json.JSONDecodeError):
                metadata = None
        core = (os.waitstatus_to_exitcode(status), fail_byte == b"E",
                metadata or {})
        return self._report_and_terminalize(core)

    def _kill_attempt_group(self, child_pid: int) -> None:
        """SIGKILL the EXACT attempt process group (the child called
        setsid, so pgid == child_pid covers the whole descendant tree
        and NEVER an unrelated process; the pgid guard falls back to the
        direct child only) and reap the direct child (a SIGKILLed
        process cannot block)."""
        try:
            if os.getpgid(child_pid) == child_pid:
                os.killpg(child_pid, SIGKILL)
            else:
                os.kill(child_pid, SIGKILL)
        except OSError:
            pass          # already dead: the caller reaps deterministically

    def _close_authority_holds(self) -> None:
        """Close the Supervisor-held sealed custody and EVERY held fd
        (launcher/auditor-executable/invocation/validator fds plus the
        pre-opened output-custody directory fd; S1-004 custody lifetime
        — closed on EVERY terminal path).  Each close absorbs its own
        failure so the guaranteed settlement path can never raise."""
        try:
            if self._custody is not None:
                self._custody.close()
        except Exception:
            pass
        for fd in (self._launcher_fd, self._auditor_fd,
                   self._invocation_fd, self._validator_fd,
                   self._out_dir_fd):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass
        self._launcher_fd = self._auditor_fd = None
        self._invocation_fd = None
        self._validator_fd = None
        self._out_dir_fd = None

    def _settle_post_consumption(self, report_state, report_extra,
                                 terminal_extra=None, original_error=None,
                                 related_error=None) -> None:
        """(S1-009) THE single centralized post-consumption terminal
        settlement — replaces every earlier duplicated terminalization
        path (_settle, _terminalize_after_consumption, the timeout and
        exceptional-cleanup sequences).  Concept A, durable accounting
        ATTEMPT: the report-outcome record (when one applies) and then
        TERMINAL, each with its normal transition while the chain still
        advances; the FIRST durable failure stops further appends — the
        existing record is preserved exactly, never counted as durable
        success.  Concept B, guaranteed in-process fail-closed death
        (the finally): whether or not the durable accounting completed,
        the already-consumed attempt lands on TERMINAL with the custody
        and every held fd closed; this path can never raise nor mask an
        outcome.  A durable failure raises the exact incompleteness
        error chaining the original/related failure; durable success
        re-raises original_error when present; otherwise the caller
        returns through only on a durably complete settlement."""
        durable_error = None
        if terminal_extra is None:
            terminal_extra = report_extra if report_state is None \
                else {"terminal_reason": "ATTEMPT_SETTLED"}
        try:
            if report_state is not None:
                self._store.append(report_state, extra=report_extra)
                self._machine.transition(report_state)
            self._store.append(TERMINAL, extra=terminal_extra)
            try:
                self._machine.transition(TERMINAL)
            except Exception:
                pass    # the fallback primitive below still lands TERMINAL
        except Exception as exc:
            durable_error = exc
        finally:
            try:
                self._machine.fail_closed_terminal()   # no-op iff there
            except Exception:
                pass    # unreachable from legal settlement source states
            self._close_authority_holds()
        if durable_error is not None:
            raise PostConsumptionTerminalAccountingError(
                durable_error, original_error, related_error,
                self._store.last_state) from (original_error
                                              or related_error
                                              or durable_error)
        if original_error is not None:
            raise original_error

    def _run_validator(self, snapshot: bytes) -> None:
        """Execute the HELD frozen structural validator ONCE on the EXACT
        clean immutable snapshot (CR-EBS-S1-007): held fd re-hashed
        immediately before execution; only frozen non-secret binding
        context in the argv; minimal EBS-defined environment; NO
        credential fd; sealed-memfd snapshot delivery; the frozen
        validator_timeout_seconds bounds the run.  EXEC03-001: the
        validator child receives a WRITABLE bounded stderr channel so a
        structural validation failure surfaces its bounded safe token
        instead of the historical read-only-fd rc-120 masking.  Any
        refusal is classified REPORT_INVALID by the caller; never a
        second execution."""
        descriptor = self._binding.output_validator
        got = _hash_fd(self._validator_fd)
        os.lseek(self._validator_fd, 0, os.SEEK_SET)
        if got != descriptor["sha256"]:
            raise LaunchRefused(
                "OUTPUT_VALIDATOR_FD_DRIFT: the held validator fd no "
                "longer matches the bound artifact")
        digest = hashlib.sha256(snapshot).hexdigest()
        b = self._binding
        output = _run_runtime_gate(
            "OUTPUT_VALIDATOR", self._validator_fd,
            [descriptor["identity"], b.event_id, b.auditor_role,
             b.attempt_id, b.output_identity["name"], digest,
             str(len(snapshot))],
            {"PATH": "/usr/bin:/bin", "LANG": "C"},
            timeout=b.execution_limits["validator_timeout_seconds"],
            report_bytes=snapshot, capture_stderr=True)
        _validate_validator_result(output, b, digest, len(snapshot))

    def _report_and_terminalize(self, core) -> AttemptResult:
        """Process-bound post-exec report lifecycle (CR-EBS-S1-007): ONE
        immutable snapshot -> SAME-custody screen (contaminated =
        REPORT_SCREEN_FAIL terminal, validator NEVER run) -> frozen
        structural validator on exactly that snapshot -> freeze of the
        EXACT screened+validated bytes 0444 under the pre-opened custody
        fd -> TERMINAL -> custody and held fds closed.  Every refusal
        terminalizes fail-closed inside THIS call; no second report
        attempt.  Digest/size are recorded only AFTER the screen passes."""
        returncode, exec_failed, metadata = core
        outcome = {"report_state": "", "report_sha256": "",
                   "report_size": 0}
        try:
            if exec_failed:
                # the boundary never exec'd: no report phase is
                # semantically appropriate — direct consumed terminal
                self._settle_post_consumption(
                    None, None,
                    {"terminal_reason": "EXEC_FAILED_AFTER_CONSUMPTION"})
            else:
                snapshot = snapshot_staging(self._staging_path)
                if snapshot is None:
                    self._settle_post_consumption(
                        REPORT_MISSING,
                        {"terminal_reason": "REPORT_MISSING"})
                    outcome["report_state"] = REPORT_MISSING
                elif self._custody.contains(snapshot):
                    discard_staging(self._staging_path)
                    self._settle_post_consumption(
                        REPORT_SCREEN_FAIL,
                        {"terminal_reason": "REPORT_SCREEN_FAIL"})
                    outcome["report_state"] = REPORT_SCREEN_FAIL
                else:
                    try:
                        self._run_validator(snapshot)
                    except (LaunchError, LaunchRefused) as exc:
                        # (EXEC03-004) durably pin the EXACT immutable
                        # snapshot identity that was supplied to the
                        # validator — hash/size ONLY; the invalid report
                        # bytes themselves are never retained as
                        # mechanical evidence, and REPORT_INVALID stays
                        # terminal and nonconforming (no freeze, no
                        # acceptance, no retry).
                        invalid_sha = hashlib.sha256(snapshot).hexdigest()
                        self._settle_post_consumption(
                            REPORT_INVALID,
                            {"terminal_reason":
                             f"REPORT_INVALID: {exc}"[:256],
                             "report_sha256": invalid_sha,
                             "report_size": len(snapshot)})
                        outcome["report_state"] = REPORT_INVALID
                        outcome["report_sha256"] = invalid_sha
                        outcome["report_size"] = len(snapshot)
                    else:
                        frozen = freeze_snapshot(
                            snapshot, self._out_dir_fd,
                            self._binding.output_identity["name"])
                        discard_staging(self._staging_path)
                        # (S1-009 §12) a settlement failure here raises
                        # the exact incompleteness error: the already
                        # frozen artifact REMAINS operator-custodied
                        # evidence (never deleted) and is NEVER returned
                        # as a conforming first pass.
                        self._settle_post_consumption(
                            REPORT_FROZEN,
                            {"terminal_reason": "REPORT_FROZEN",
                             "report_sha256": frozen["sha256"],
                             "report_size": frozen["size"],
                             "report_mode": frozen["mode"]})
                        outcome.update(report_state=REPORT_FROZEN,
                                       report_sha256=frozen["sha256"],
                                       report_size=frozen["size"])
        except ReportRefused as exc:
            # operational report-custody refusal (invalid staging object,
            # oversize, unsafe output, no-overwrite collision): terminal
            # fail-closed with the exact durable reason, no retry; a
            # settlement accounting failure raises the exact
            # incompleteness error chaining this refusal.
            self._settle_post_consumption(
                None, None,
                {"terminal_reason": f"REPORT_CUSTODY_REFUSED: {exc}"[:256]},
                related_error=exc)
        except PostConsumptionTerminalAccountingError:
            raise   # already settled in-process; custody/fds closed; the
                    # durable incompleteness is surfaced honestly
        except Exception as exc:
            self._settle_post_consumption(
                None, None,
                {"terminal_reason":
                 f"REPORT_LIFECYCLE_FAILURE_AFTER_CONSUMPTION: "
                 f"{exc!r}"[:256]},
                related_error=exc)
        return AttemptResult(returncode, exec_failed, metadata, False,
                             outcome["report_state"],
                             outcome["report_sha256"],
                             outcome["report_size"])

    def _preexec_stop(self) -> None:
        """Fail-closed terminalization of a refused pre-exec attempt: the
        in-process transition to the absorbing TERMINAL_PREEXEC_STOP
        ALWAYS happens (authority is dead even if the medium is
        unavailable); the durable append is best-effort alongside it —
        never a relabeling of the attempt as resumable.  The held custody
        and every held fd are closed (S1-004 custody lifetime)."""
        try:
            self._store.append(TERMINAL_PREEXEC_STOP)
        except Exception:
            pass    # medium unavailable: the spent/issued guards hold
        if self._machine.state in (PREPARED, GATES_PASSED):
            self._machine.transition(TERMINAL_PREEXEC_STOP)
        self._close_authority_holds()
