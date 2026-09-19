"""Controllerless one-shot verified boundary child execution.

Primary launch authority is NON-EXPORTABLE EBS PROCESS STATE plus
state-machine control flow: a single-use in-process grant minted only by
the durably recorded GATES_PASSED -> CONSUMED_PRE_EXEC transition of
THIS supervisor, spendable exactly once (identity-compared object;
irreversible in-process spend; every post-consumption failure
terminalizes the attempt — never retried, never relabeled unconsumed).
No bearer token exists in any file, argv, environment, or IPC surface;
no controller; no attach/revival path.  Before any authority exists the
supervisor FAIL-CLOSED VERIFIES ITS OWN LIVE PACKAGE BYTES against the
identities pinned by the frozen binding (verify_package_identity;
construction + full semantics in README.md) — mandatory, in the startup
path, with no flag and no environment override — and then verifies the
supplied FROZEN EVENT PACKAGE (verify_event_package, CR-EBS-REM-001):
package identity against the binding's independently pinned event_package
pair PLUS exact transport-projection equality with the binding, before
any gate is reachable; the event-package root is a MANDATORY supervisor
input with no default and no bypass of any kind.

The frozen boundary-launcher executable is verified by opening it ONCE,
hashing the ALREADY-OPEN file, and executing THAT OPEN FILE DESCRIPTOR
via execveat(AT_EMPTY_PATH) (fexecve fallback).  A pathname re-open is
never used after verification; unavailability of the identity-preserving
exec method fails closed.  The held fd is re-hashed immediately before
fork so same-inode drift after consumption also fails closed.

Gate-timing remediation (CR-EBS-S1-001) + preexec-gate remediation
(CR-EBS-S1-002/-003): the DYNAMIC runtime gates are NOT frozen evidence.
Every Supervisor construction holds the VERIFIED OPEN fd of BOTH runtime
gate artifacts bound by the frozen descriptors (identity/path/SHA-256/
result schema, digest- and projection-covered).  The externally
separable preexec sequence validate_gates() -> verify_launcher() ->
consume() NO LONGER EXISTS: the ONE public preexec authority operation
`consume(launcher_path)` (see Supervisor.consume) verifies the launcher,
executes both gates fresh in the required order, and durably records
GATES_PASSED -> CONSUMED_PRE_EXEC without returning control to the
caller in between — GATES_PASSED is an INTERNAL TRANSIENT state in which
no caller ever regains control, so no caller-controlled pause can sit
between the fresh RESOURCE_GATE PASS and durable consumption.  Each gate
executes with a bounded fail-closed timeout, no credential fd inherited,
a clean minimal environment, and strict result-envelope validation
against the binding; any failure terminalizes the attempt with
authority unconsumed and no same-attempt retry.
"""
from __future__ import annotations

import ctypes
import errno
import hashlib
import json
import os
import platform
import stat
import time
from dataclasses import dataclass

from .accounting import AccountingStore
from .binding import (EVENT_MANIFEST_KEYS, EVENT_MANIFEST_SCHEMA,
                      NETWORK_READINESS_RESULT_SCHEMA,
                      RESOURCE_GATE_RESULT_SCHEMA, RUNTIME_GATES,
                      BindingError, binding_projection, canonical_bytes,
                      strict_loads)
from .custody import CredentialCustody, establish_non_dumpable
from .reportcustody import DEFAULT_SIZE_LIMIT, collect
from .statemachine import (CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, GATES_PASSED,
                           PREPARED, REPORT_FROZEN, REPORT_MISSING,
                           REPORT_SCREEN_FAIL, TERMINAL,
                           TERMINAL_PREEXEC_STOP, StateMachine)

CRED_FD = 3                    # fixed inherited-fd contract for the sealed
                               # credential memfd; the ONLY credential channel
FAIL_FD = 4                    # exec-failure signal pipe (CLOEXEC: EOF = ok)
CHILD_EXIT_EXEC_FAIL = 98
METADATA_MAX = 65536

# Runtime-gate execution bounds (CR-EBS-S1-001; shared by BOTH dynamic
# gates under S1-002): a hung gate must never create an unbounded
# authority process, and the accepted result is size-bounded before
# parsing.
RUNTIME_GATE_TIMEOUT = 10.0             # seconds; deterministic fail-closed
RUNTIME_GATE_RESULT_MAX = 65536         # accepted result bytes (bound first)
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


def open_verified_launcher(path, expected_sha256: str) -> int:
    """Open (no symlink following), verify regular-file identity, hash the
    ALREADY-OPEN file, and return the verified open fd."""
    try:
        fd = os.open(os.fspath(path), os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise LaunchRefused(
            f"LAUNCHER_OPEN_REFUSED (symlink/unreadable?): {exc!r}") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise LaunchRefused("LAUNCHER_NOT_REGULAR_FILE")
        got = _hash_fd(fd)
        if got != expected_sha256:
            raise LaunchRefused(
                f"LAUNCHER_DIGEST_MISMATCH: expected {expected_sha256} "
                f"got {got}")
    except Exception:
        os.close(fd)
        raise
    os.lseek(fd, 0, os.SEEK_SET)
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


def open_runtime_gate(event_package_root, binding, event_manifest,
                      gate: str) -> int:
    """Open (no symlink following) + verify ONE frozen runtime-gate
    artifact (by gate name) from the ALREADY-VERIFIED event-package tree
    and return the verified open fd (held for exactly-once live
    execution).  The path is binding-validated as a safe package-relative
    path; the artifact must additionally be a manifest row of the
    verified package, a regular executable file, and byte-identical to
    the descriptor's exact SHA-256."""
    descriptor = binding.runtime_gates[gate]
    rows = {row["path"] for row in event_manifest["files"]}
    if descriptor["path"] not in rows:
        raise LaunchRefused(
            f"{gate}_NOT_PACKAGE_MANIFEST_ROW: {descriptor['path']!r}")
    path = os.path.join(os.fspath(event_package_root), descriptor["path"])
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise LaunchRefused(f"{gate}_OPEN_REFUSED: {exc!r}") from exc
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise LaunchRefused(f"{gate}_NOT_REGULAR_FILE")
        if not info.st_mode & 0o111:
            raise LaunchRefused(f"{gate}_NOT_EXECUTABLE")
        if _hash_fd(fd) != descriptor["sha256"]:
            raise LaunchRefused(f"{gate}_ARTIFACT_DIGEST_MISMATCH: live "
                                "artifact differs from the bound descriptor "
                                "SHA-256")
    except Exception:
        os.close(fd)
        raise
    os.lseek(fd, 0, os.SEEK_SET)
    return fd


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


def _gate_child(gate_fd: int, result_w: int, devnull: int,
                argv, env: dict) -> None:
    """Child-side preparation for a runtime gate: stdout is the bounded
    result pipe, stdin/stderr are devnull, NO credential fd is inherited
    (custody never enters this path and the gate receives no launch
    authority), every other fd is closed, and the ALREADY-VERIFIED open
    gate fd is exec'd (identity-preserving; no pathname re-open).
    Never returns."""
    import fcntl
    try:
        os.dup2(devnull, 0)
        os.dup2(result_w, 1)
        os.dup2(devnull, 2)
        keep = {0, 1, 2, gate_fd}
        for entry in os.listdir("/proc/self/fd"):
            fd = int(entry)
            if fd not in keep:
                try:
                    os.close(fd)
                except OSError:
                    pass
        fcntl.fcntl(gate_fd, fcntl.F_SETFD, 0)  # survives exec (script fd)
        establish_non_dumpable()
        fd_exec(gate_fd, argv, env)
    except BaseException:
        os._exit(CHILD_EXIT_EXEC_FAIL)


def _run_runtime_gate(gate: str, gate_fd: int, argv, env: dict) -> bytes:
    """Execute the verified runtime-gate fd EXACTLY ONCE with a bounded
    fail-closed timeout; return the raw result bytes (size-bounded).  Any
    fork/exec failure, hang past the deadline, oversized output, or
    non-zero child exit refuses."""
    result_r, result_w = os.pipe()
    devnull = os.open(os.devnull, os.O_RDONLY)
    child_pid = None
    try:
        try:
            child_pid = os.fork()
        except OSError as exc:
            raise LaunchError(f"{gate}_FORK_FAILED: {exc!r}") from exc
        if child_pid == 0:
            _gate_child(gate_fd, result_w, devnull, argv, env)
        os.close(result_w)
        result_w = None
        os.close(devnull)
        devnull = None
        os.set_blocking(result_r, False)
        deadline = time.monotonic() + RUNTIME_GATE_TIMEOUT
        output = b""
        eof = False
        exitcode = None
        while True:
            if time.monotonic() >= deadline:
                _kill_and_reap(child_pid)
                raise LaunchRefused(
                    f"{gate}_TIMEOUT: gate did not finish within "
                    f"{RUNTIME_GATE_TIMEOUT}s; failing closed")
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
                                f"{gate}_OUTPUT_TOO_LARGE: gate emitted "
                                f"more than {RUNTIME_GATE_RESULT_MAX} "
                                f"result bytes")
            if exitcode is None:
                waited_pid, status = os.waitpid(child_pid, os.WNOHANG)
                if waited_pid == child_pid:
                    exitcode = os.waitstatus_to_exitcode(status)
                    progressed = True
            if eof and exitcode is not None:
                break
            if not progressed:
                time.sleep(0.01)               # bounded poll, no busy spin
        if exitcode != 0:
            reason = ("EXEC_FAILED" if exitcode == CHILD_EXIT_EXEC_FAIL
                      else "NONZERO_EXIT")
            raise LaunchRefused(f"{gate}_{reason}: gate exited {exitcode}")
        if not output:
            raise LaunchRefused(f"{gate}_OUTPUT_MISSING: gate produced no "
                                "result bytes")
        return output
    finally:
        for fd in (result_r, result_w, devnull):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass


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


def _child_setup(launcher_fd: int, metadata_w: int, fail_w: int,
                 devnull: int, custody_fd: int, argv, env: dict) -> None:
    """Child-side preparation: fixed fd contract, hygiene, then exec of
    the verified open fd.  Never returns."""
    import fcntl
    try:
        os.dup2(devnull, 0)
        os.dup2(metadata_w, 1)
        os.dup2(devnull, 2)
        if custody_fd != CRED_FD:
            os.dup2(custody_fd, CRED_FD)
        if fail_w != FAIL_FD:
            os.dup2(fail_w, FAIL_FD)
        fcntl.fcntl(FAIL_FD, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
        keep = {0, 1, 2, CRED_FD, FAIL_FD, launcher_fd}
        for entry in os.listdir("/proc/self/fd"):
            fd = int(entry)
            if fd not in keep:
                try:
                    os.close(fd)
                except OSError:
                    pass
        for survivor in (launcher_fd, CRED_FD):
            fcntl.fcntl(survivor, fcntl.F_SETFD, 0)  # fd contract survives
        establish_non_dumpable()
        fd_exec(launcher_fd, argv, env)
    except BaseException:
        try:
            os.write(FAIL_FD, b"E")
        except OSError:
            pass
        os._exit(CHILD_EXIT_EXEC_FAIL)


class LaunchGrant:
    """Single-use, non-exportable, in-process capability: carries NO
    state.  Authority lives entirely in the issuing Supervisor, which
    accepts ONLY the exact object its consume() returned while unspent;
    any other object (fresh, copied, re-created) is refused."""

    __slots__ = ()


@dataclass(frozen=True)
class ChildResult:
    returncode: int
    exec_failed: bool
    metadata: dict


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
        self._binding = binding
        self._store = store
        self._machine = StateMachine(store.last_state or PREPARED)
        self._launcher_fd = None
        self._issued_grant = None    # single issuance: consume() -> grant
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
                 "auditor_executable_sha256":
                     b.auditor_identity["executable_sha256"]}
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

    def consume(self, launcher_path) -> LaunchGrant:
        """THE single public preexec authority operation (CR-EBS-S1-003):
        PREPARED -> (GATES_PASSED) -> CONSUMED_PRE_EXEC with NO return of
        control to the caller between the steps.  In order, without ever
        yielding to the caller: require an unspent/unissued PREPARED
        attempt; verify and HOLD the exact boundary launcher fd (static
        byte identity, BEFORE the dynamic gates); execute
        NETWORK_READINESS exactly once, then RESOURCE_GATE exactly once
        LAST (the final live environmental gate); strictly validate both
        fresh results; durably append GATES_PASSED carrying BOTH fresh
        evidence sets; transition in-process (internal transient);
        IMMEDIATELY durably append CONSUMED_PRE_EXEC with the complete
        binding facts; transition; mint exactly one LaunchGrant and only
        then return it.  Any failure — launcher identity, either gate, or
        either durable append — terminalizes fail-closed with no grant
        and NO same-attempt retry; GATES_PASSED is never a
        caller-visible state."""
        if self._machine.state != PREPARED:
            raise LaunchError(
                f"CONSUME_REFUSED_STATE_{self._machine.state}: the single "
                "preexec-consumption operation requires PREPARED")
        if self._launcher_fd is not None or self._issued_grant is not None \
                or self._spent or self._gates_executed:
            raise LaunchError("CONSUME_REFUSED_ATTEMPT_ALREADY_ADVANCED: "
                              "no second preexec consumption exists")
        self._gates_executed = True
        try:
            # Launcher identity FIRST (static byte check, not a dynamic
            # environmental gate): held before the dynamic gates run, so
            # launcher verification precedes gate freshness and launcher
            # exec remains impossible before CONSUMED_PRE_EXEC.
            self._launcher_fd = open_verified_launcher(
                launcher_path, self._binding.boundary_launcher["sha256"])
            evidence = {}
            for gate in RUNTIME_GATES:   # NETWORK_READINESS, then the
                evidence.update(self._execute_runtime_gate(gate))
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
        grant = LaunchGrant()
        self._issued_grant = grant
        return grant

    def _terminalize_after_consumption(self, reason: str) -> None:
        """Best-effort durable TERMINAL after a post-consumption failure;
        the spent guard forbids a second launch even if this fails."""
        try:
            self._store.append(TERMINAL, extra={"terminal_reason":
                                                reason[:256]})
            self._machine.transition(TERMINAL)
        except Exception:
            pass    # medium unavailable: spent guard holds

    def execute(self, grant: LaunchGrant, custody: CredentialCustody,
                argv_tail=(), env: dict = None) -> ChildResult:
        if not isinstance(grant, LaunchGrant) or \
                grant is not self._issued_grant:
            raise LaunchError("LAUNCH_REFUSED_GRANT_NOT_ISSUED_BY_THIS_"
                              "SUPERVISOR: only the exact object returned "
                              "by this supervisor's consume() authorizes "
                              "a launch")
        if self._spent:
            raise LaunchError("LAUNCH_REFUSED_AUTHORITY_ALREADY_SPENT")
        if not isinstance(custody, CredentialCustody) or custody._closed:
            raise LaunchError("LAUNCH_REFUSED_NO_CUSTODY")
        if self._machine.state != CONSUMED_PRE_EXEC:
            raise LaunchError(
                f"LAUNCH_REFUSED_STATE_{self._machine.state}")
        if self._launcher_fd is None:
            raise LaunchError("LAUNCH_REFUSED_NO_LAUNCHER_FD")
        # IRREVERSIBLE SPEND: authority is dead in this process from here
        # on even if the re-hash/fork/setup/EXEC-record fails; no second
        # execute() can ever pass and no replacement grant exists.
        self._spent = True
        self._issued_grant = None
        child_pid = None
        waited = False
        md_r = md_w = fail_r = fail_w = devnull = None
        fail_byte = b""
        metadata_raw = b""
        try:
            got = _hash_fd(self._launcher_fd)
            if got != self._binding.boundary_launcher["sha256"]:
                raise LaunchRefused(
                    "LAUNCHER_DIGEST_MISMATCH_AFTER_CONSUMPTION")
            argv = [self._binding.boundary_launcher["identity"],
                    "--role", self._binding.auditor_role,
                    "--attempt", self._binding.attempt_id,
                    "--event", self._binding.event_id] + list(argv_tail)
            child_env = {"PATH": "/usr/bin:/bin", "LANG": "C"}
            if env:
                child_env.update(env)
            md_r, md_w = os.pipe()
            fail_r, fail_w = os.pipe()
            devnull = os.open(os.devnull, os.O_RDONLY)
            try:
                child_pid = os.fork()
            except OSError as exc:
                raise LaunchError(f"FORK_FAILED: {exc!r}") from exc
            if child_pid == 0:
                _child_setup(self._launcher_fd, md_w, fail_w, devnull,
                             custody.fd, argv, child_env)
            os.close(md_w)
            os.close(fail_w)
            os.close(devnull)
            md_w = fail_w = devnull = None
            self._store.append(EXEC_ATTEMPTED, extra={"child_pid":
                                                      child_pid})
            self._machine.transition(EXEC_ATTEMPTED)
            fail_byte = os.read(fail_r, 1)
            os.close(fail_r)
            fail_r = None
            _, status = os.waitpid(child_pid, 0)
            waited = True
            while len(metadata_raw) < METADATA_MAX:
                chunk = os.read(md_r, 65536)
                if not chunk:
                    break
                metadata_raw += chunk
        except BaseException as exc:
            # Post-consumption failure: close remaining parent fds (a
            # metadata-blocked child unblocks and dies), reap the child,
            # record TERMINAL best-effort; never relabeled unconsumed.
            for fd in (md_r, md_w, fail_r, fail_w, devnull):
                if fd is not None:
                    try:
                        os.close(fd)
                    except OSError:
                        pass
            if child_pid and not waited:
                try:
                    os.waitpid(child_pid, 0)
                except OSError:
                    pass
            if self._machine.state == CONSUMED_PRE_EXEC:
                self._terminalize_after_consumption(
                    f"PRE_EXEC_FAILURE_AFTER_CONSUMPTION: {exc!r}")
            raise
        finally:
            for fd in (md_r, fail_r):
                if fd is not None:
                    try:
                        os.close(fd)
                    except OSError:
                        pass
        metadata = None
        if metadata_raw:
            try:
                metadata = json.loads(metadata_raw.decode())
            except (UnicodeDecodeError, json.JSONDecodeError):
                metadata = None
        return ChildResult(os.waitstatus_to_exitcode(status),
                           fail_byte == b"E", metadata)

    def adopt_report(self, staging_path, output_root,
                     custody: CredentialCustody,
                     size_limit: int = DEFAULT_SIZE_LIMIT) -> dict:
        """Report custody + leak screen; records the outcome and finishes
        the attempt (one-shot process exits after TERMINAL)."""
        if self._machine.state != EXEC_ATTEMPTED:
            raise LaunchError(
                f"REPORT_CUSTODY_REFUSED_STATE_{self._machine.state}")
        outcome = collect(staging_path, output_root,
                          self._binding.output_identity["name"],
                          custody=custody, size_limit=size_limit)
        self._store.append(outcome["state"])
        self._machine.transition(outcome["state"])
        self.finish()
        return outcome

    def finish(self) -> None:
        if self._machine.state in (TERMINAL, TERMINAL_PREEXEC_STOP):
            return
        self._store.append(TERMINAL)
        self._machine.transition(TERMINAL)

    def _preexec_stop(self) -> None:
        """Fail-closed terminalization of a refused pre-exec attempt: the
        in-process transition to the absorbing TERMINAL_PREEXEC_STOP
        ALWAYS happens (authority is dead even if the medium is
        unavailable); the durable append is best-effort alongside it —
        never a relabeling of the attempt as resumable."""
        try:
            self._store.append(TERMINAL_PREEXEC_STOP)
        except Exception:
            pass    # medium unavailable: the spent/issued guards hold
        if self._machine.state in (PREPARED, GATES_PASSED):
            self._machine.transition(TERMINAL_PREEXEC_STOP)
