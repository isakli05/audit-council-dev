"""Controllerless one-shot target-independent bootstrap authority core.

NEW authority-specific source for the AUCDEV-023 PCH6-B PATH-B wholly
NEW lineage (Control Room design readback 2026-10-02); shares NO code
with, and imports NOTHING from, the audit target
`730d2b29:bootstrap-supervisor/**` (AUDIT SUBJECT: never authority here)
or the legacy EBS at `068f5e2` (REFERENCE_ONLY).  The pre-target EBS
lineage provides the state machine and the sealed credential custody as
EXACT reused blobs and the hash-chained O_EXCL accounting and the
report snapshot/freeze discipline as bounded RB2 derivatives (held-fd
object custody; MANIFEST.json source_provenance); else NEW.

Primary launch authority is NON-EXPORTABLE AUTHORITY PROCESS STATE
plus state-machine control flow: the whole attempt lifecycle —
package/event identity verification, static byte identities,
custody-OBJECT identity gate (BA-PREP-RB2-001), the THREE fresh
dynamic gates in frozen order, durable GATES_PASSED, the
authority-created report sink (BA-PREP-RB2-002), credential custody
strictly AFTER those gates (BA-RB-002), durable CONSUMED_PRE_EXEC, the
irreversible spend and the IMMEDIATE fork/exec — happens inside ONE
public authority operation `BootstrapAuthority.run_attempt(...)`: no
grant/consume/resume/retry/adopt_report/finish/mint_attempt/
create_event surface exists, and no caller ever regains control
between GATES_PASSED, CONSUMED_PRE_EXEC and the exec.  Every
construction fail-closed-verifies ITS OWN live package bytes and the
frozen event package against the binding pins.  The authority OWNS the sealed
credential custody (SOURCE fd only; ingest strictly AFTER every
required pre-inference gate has durably passed; role ONLY from the
binding; no credential byte is ever logged, hashed, persisted or
returned — custody.py); the launcher and LIVE auditor executable are
verified-opened ONCE and HELD, exec'd identity-preserving with NO
pathname re-open, the frozen argv travelling ONLY as sealed canonical
bytes on AUDITOR_INVOCATION_FD; after the bounded child wait the
process-bound report lifecycle (snapshot of the HELD sink -> screen ->
validator -> semantic binding -> 0444 O_EXCL freeze under the SAME
held custody fd) runs in the SAME call.  A durable terminal-accounting
failure raises the distinct PostConsumptionTerminalAccountingError,
NEVER a successful AttemptResult.  NO substantive audit verdict logic
lives here.
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
from .binding import (AUTHORITY_MANIFEST_KEYS, AUTHORITY_MANIFEST_SCHEMA,
                      AUTHORITY_STATUS, AUTHORITY_QUALIFICATION_CLAIM,
                      DYNAMIC_GATE_ORDER, EVENT_MANIFEST_KEYS,
                      EVENT_MANIFEST_SCHEMA, EVENT_ID, FROZEN_TARGET,
                      POLICY_ID, RESERVED_ATTEMPT_IDS, Binding, BindingError,
                      binding_projection, canonical_bytes, strict_loads,
                      REPORT_ATTEMPT_ID_MISMATCH, REPORT_AUDITOR_ROLE_MISMATCH,
                      REPORT_BINDING_UNPARSEABLE, REPORT_EVENT_ID_MISMATCH,
                      REPORT_TARGET_COMMIT_MISMATCH)
from .custody import (F_ADD_SEALS, F_GET_SEALS, MFD_ALLOW_SEALING,
                      MFD_CLOEXEC, REQUIRED_SEALS, CredentialCustody,
                      establish_non_dumpable, memfd_create)
from .reportcustody import (ReportRefused, create_report_sink,
                            discard_held_sink, freeze_snapshot,
                            snapshot_held_sink)
from .statemachine import (CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, GATES_PASSED,
                           PREPARED, REPORT_FROZEN, REPORT_INVALID,
                           REPORT_MISSING, REPORT_SCREEN_FAIL, TERMINAL,
                           TERMINAL_PREEXEC_STOP, StateMachine)

CRED_FD = 3                    # sealed credential memfd (ONLY channel)
FAIL_FD = 4                    # exec-fail signal pipe (CLOEXEC; EOF = ok)
AUDITOR_EXEC_FD = 5            # HELD verified live auditor executable
AUDITOR_INVOCATION_FD = 6      # sealed read-only frozen-argv spec
VALIDATOR_REPORT_FD = 3        # validator child: sealed report memfd
CHILD_EXIT_EXEC_FAIL = 98
METADATA_MAX = 65536
METADATA_GRACE = 0.5           # bounded post-reap metadata drain (seconds)
VALIDATOR_STDERR_MAX = 4096
STRUCTURAL_TOKEN_PREFIX = "VALIDATION_ERROR: "
STRUCTURAL_TOKEN_CHARS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
SIGKILL = 9                    # POSIX constant (no signal import)

AT_EMPTY_PATH = 0x1000
SYS_EXECVEAT = {"x86_64": 322, "aarch64": 281, "armv7l": 387, "i686": 358}

PACKAGE_MANIFEST = "MANIFEST.json"
MANIFEST_ROW_FIELDS = ("path", "bytes", "sha256")

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
CLIENT_SELECTION_RESULT_FIELDS = ("schema", "status", "event_id",
                                  "auditor_role", "attempt_id",
                                  "provider_role", "client_family",
                                  "model", "effort",
                                  "client_executable_identity",
                                  "client_executable_version",
                                  "client_executable_sha256")
VALIDATOR_RESULT_FIELDS = ("schema", "status", "event_id", "auditor_role",
                           "attempt_id", "output_name", "report_sha256",
                           "report_size")

# The exact per-file source provenance of every production module,
# verified against the live authority package at every construction:
# statemachine.py and custody.py are EXACT pre-target blobs from
# 068f5e29904f446bf832138fd64c8833b9037cb7; accounting.py and
# reportcustody.py are bounded RB2 derivatives (the narrow held-fd
# object-custody primitives ONLY); the rest are NEW.
PRETARGET_REUSE_SOURCE_COMMIT = \
    "068f5e29904f446bf832138fd64c8833b9037cb7"
PRETARGET_REUSE = {
    f"bootstrap_authority/{name}": (f"bootstrap-supervisor/ebs/{name}", blob)
    for name, blob in (
        ("statemachine.py", "cf563d2178907e7666ce661b81ab1bf16fb71201"),
        ("custody.py", "37e6b5bb4365c7b29ba3632fe95362d5a7e16c09"),
    )}
PRETARGET_DERIVED = {
    f"bootstrap_authority/{name}": (f"bootstrap-supervisor/ebs/{name}", blob)
    for name, blob in (
        ("accounting.py", "03de6f663db283cf99f6a98e26e752a24457c52a"),
        ("reportcustody.py", "18f1cc600c684e520b72026e0b4cdf8ba6287cb9"),
    )}
DERIVATION_KIND = "EXACT_PRETARGET_BLOB_DERIVATIVE_RB2"
DERIVATION_REASON = ("AUCDEV-023-PCH6B-BA-PREP-RB2-001-002-BOUNDED-"
                     "HELD-FD-OBJECT-CUSTODY")
EXPECTED_PROVENANCE = dict(PRETARGET_REUSE, **{
    f"bootstrap_authority/{name}": {"kind": "NEW_AUTHORITY_SPECIFIC",
                                    "origin": "THIS_BOUNDED_IMPLEMENTATION"}
    for name in ("__init__.py", "binding.py", "runtime.py")})
for _path, (_src, _blob) in PRETARGET_REUSE.items():
    EXPECTED_PROVENANCE[_path] = {
        "kind": "EXACT_PRETARGET_BLOB_REUSE",
        "source_commit": PRETARGET_REUSE_SOURCE_COMMIT,
        "source_path": _src, "source_git_blob": _blob}
for _path, (_src, _blob) in PRETARGET_DERIVED.items():
    EXPECTED_PROVENANCE[_path] = {
        "kind": DERIVATION_KIND,
        "source_commit": PRETARGET_REUSE_SOURCE_COMMIT,
        "source_path": _src, "source_git_blob": _blob,
        "derivation": DERIVATION_REASON}

class AuthorityError(RuntimeError):
    """Refused or failed authority-path operation (fail closed)."""

class AuthorityRefused(AuthorityError):
    """Identity/verification refusal before any exec attempt."""

class PostConsumptionTerminalAccountingError(AuthorityError):
    """The durable post-consumption terminal accounting chain did NOT
    complete: the attempt is already in-process TERMINAL, custody and
    held fds closed, NO retry exists, the record is INCOMPLETE — never
    a successful AttemptResult."""
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

def accounting_name(binding) -> str:
    """Attempt-GLOBAL O_EXCL authority-claim name (BA-RB-001): ONE
    reserved attempt id = ONE global claim, independent of the binding
    digest (which stays durable, inspection-bound in-record evidence)."""
    return binding.attempt_id

def _char_array(items) -> "ctypes.Array":
    array = (ctypes.c_char_p * (len(items) + 1))()
    for index, item in enumerate(items):
        array[index] = item.encode() if isinstance(item, str) else item
    return array

def _execveat(fd: int, argv, envp) -> None:
    number = SYS_EXECVEAT.get(platform.machine())
    if number is None:
        raise AuthorityError(
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
        raise AuthorityError("FEXECVE_UNAVAILABLE: identity-preserving "
                             "exec method absent; failing closed")
    entry.restype = ctypes.c_int
    result = entry(ctypes.c_int(fd), _char_array(argv), _char_array(envp))
    if result != 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))

def fd_exec(fd: int, argv, env: dict) -> None:
    """Exec the ALREADY-OPEN verified fd; no pathname fallback."""
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
    """Verified-open core: no final symlink, regular (+executable when
    required), exact hash of the ALREADY-OPEN fd, rewind, HELD fd."""
    try:
        fd = os.open(os.fspath(path), os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise AuthorityRefused(f"{kind}_OPEN_REFUSED (symlink/unreadable?): "
                               f"{exc!r}") from exc
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise AuthorityRefused(f"{kind}_NOT_REGULAR_FILE")
        if require_executable and not info.st_mode & 0o111:
            raise AuthorityRefused(f"{kind}_NOT_EXECUTABLE")
        got = _hash_fd(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        if got != expected_sha256:
            raise AuthorityRefused(f"{kind}_DIGEST_MISMATCH: expected "
                                   f"{expected_sha256} got {got}")
    except Exception:
        os.close(fd)
        raise
    return fd

def open_verified_launcher(path, expected_sha256: str) -> int:
    """Verify and hold the frozen boundary-launcher executable."""
    return _open_verified(path, expected_sha256, "LAUNCHER", False)

def open_verified_auditor_executable(path, expected_sha256: str) -> int:
    """Verify and HOLD the LIVE auditor executable (regular +
    executable + exact SHA-256; PREEXEC refusal, no same-attempt
    retry)."""
    return _open_verified(path, expected_sha256,
                          "PREEXEC_EXECUTABLE_IDENTITY_FAIL", True)

def make_invocation_fd(argv_list) -> int:
    """Sealed read-only memfd carrying the EXACT frozen auditor argv;
    no caller string, argv tail, or environment override enters it."""
    fd = memfd_create("bootstrap-authority-auditor-invocation",
                      MFD_CLOEXEC | MFD_ALLOW_SEALING)
    try:
        os.write(fd, canonical_bytes(list(argv_list)))
        os.lseek(fd, 0, os.SEEK_SET)
        fcntl.fcntl(fd, F_ADD_SEALS, REQUIRED_SEALS)
        if fcntl.fcntl(fd, F_GET_SEALS) & REQUIRED_SEALS != REQUIRED_SEALS:
            raise AuthorityRefused("INVOCATION_SPEC_SEAL_INCOMPLETE")
    except Exception:
        os.close(fd)
        raise
    return fd

def verify_package_bytes(root, expected_package_sha256: str,
                         expected_manifest_sha256: str = None) -> dict:
    """Fail-closed package verification: non-circular package_sha256,
    pinned raw-manifest/package identities, per-file size/SHA-256 rows,
    EXACT payload-set equality with the walked live tree; manifest
    returned as "document"."""
    try:
        fd = os.open(os.path.join(os.fspath(root), PACKAGE_MANIFEST),
                     os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise AuthorityRefused(
            f"PACKAGE_MANIFEST_UNOPENABLE: {exc!r}") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise AuthorityRefused("PACKAGE_MANIFEST_NOT_REGULAR_FILE")
        data = b""
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            data += chunk
    finally:
        os.close(fd)
    try:
        doc = strict_loads(data)
    except BindingError as exc:
        raise AuthorityRefused(
            f"PACKAGE_MANIFEST_MALFORMED: {exc}") from exc
    if not isinstance(doc, dict):
        raise AuthorityRefused("PACKAGE_MANIFEST_NOT_AN_OBJECT")
    live_manifest = hashlib.sha256(data).hexdigest()
    declared = doc.get("package_sha256")
    if not isinstance(declared, str) or len(declared) != 64:
        raise AuthorityRefused("PACKAGE_IDENTITY_FIELD_ABSENT_OR_MALFORMED")
    identity_source = dict(doc)
    del identity_source["package_sha256"]
    if hashlib.sha256(json.dumps(identity_source, sort_keys=True,
                                 separators=(",", ":")).encode()
                      ).hexdigest() != declared:
        raise AuthorityRefused(
            "PACKAGE_IDENTITY_NOT_SELF_CONSISTENT: the manifest "
            "package_sha256 does not match the digest of the manifest "
            "excluding that field")
    if expected_manifest_sha256 is not None \
            and live_manifest != expected_manifest_sha256:
        raise AuthorityRefused(
            f"LIVE_MANIFEST_IDENTITY_MISMATCH: binding pins "
            f"{expected_manifest_sha256} but live manifest is "
            f"{live_manifest}")
    if declared != expected_package_sha256:
        raise AuthorityRefused(
            f"PACKAGE_IDENTITY_MISMATCH: binding pins "
            f"{expected_package_sha256} but live package identity is "
            f"{declared}")
    rows = doc.get("files")
    if not isinstance(rows, list) or not rows:
        raise AuthorityRefused("PACKAGE_MANIFEST_FILES_INVALID")
    recorded = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != \
                set(MANIFEST_ROW_FIELDS) or \
                not isinstance(row["path"], str) or row["path"] in recorded:
            raise AuthorityRefused(f"PACKAGE_MANIFEST_ROW_INVALID: {row!r}")
        size = row["bytes"]
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise AuthorityRefused(
                f"PACKAGE_MANIFEST_ROW_BYTES_TYPE_INVALID: {size!r} "
                f"for row {row['path']!r}")
        recorded[row["path"]] = row
    root = os.fspath(root)
    total_bytes = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in dirnames[:]:
            if name == "__pycache__":
                dirnames.remove(name)
            elif os.path.islink(os.path.join(dirpath, name)):
                raise AuthorityRefused(
                    f"PACKAGE_TREE_SYMLINK_DIR: {name}")
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if rel == PACKAGE_MANIFEST:
                continue    # the manifest itself is identity-pinned above
            row = recorded.pop(rel, None)
            if row is None or not stat.S_ISREG(os.lstat(full).st_mode):
                raise AuthorityRefused(
                    f"PACKAGE_PAYLOAD_UNRECORDED_OR_NOT_REGULAR: {rel}")
            try:
                fd = os.open(full, os.O_RDONLY | os.O_NOFOLLOW)
            except OSError as exc:
                raise AuthorityRefused(
                    f"PACKAGE_PAYLOAD_OPEN_REFUSED: {rel}: {exc!r}") from exc
            try:
                if os.fstat(fd).st_size != row["bytes"] or \
                        _hash_fd(fd) != row["sha256"]:
                    raise AuthorityRefused(
                        f"PACKAGE_PAYLOAD_MISMATCH: {rel} recorded "
                        "size/hash does not match the live file")
            finally:
                os.close(fd)
            total_bytes += row["bytes"]
    if recorded:
        raise AuthorityRefused(
            f"PACKAGE_PAYLOAD_MISSING_FROM_LIVE_TREE: {sorted(recorded)}")
    return {"files": len(rows), "bytes": total_bytes,
            "manifest_sha256": live_manifest, "package_sha256": declared,
            "document": doc}

def verify_own_package(binding) -> dict:
    """MANDATORY self-identity of THE EXECUTING authority package at
    EVERY construction: pinned identities + per-file/payload-set
    verification of the LIVE bytes at THIS module's own package root
    (never caller-provided), then the strict authority-manifest
    semantic checks (keys/schema/policy/target/ids/status/provenance)."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = verify_package_bytes(
        root, binding.authority_package["package_sha256"],
        binding.authority_package["manifest_sha256"])
    manifest = result["document"]
    keys = set(manifest)
    if keys != set(AUTHORITY_MANIFEST_KEYS):
        raise AuthorityRefused(
            f"AUTHORITY_MANIFEST_KEYS_INVALID: "
            f"unknown={sorted(keys - set(AUTHORITY_MANIFEST_KEYS))} "
            f"missing={sorted(set(AUTHORITY_MANIFEST_KEYS) - keys)}")
    if manifest["schema"] != AUTHORITY_MANIFEST_SCHEMA:
        raise AuthorityRefused(
            f"AUTHORITY_MANIFEST_SCHEMA_UNEXPECTED: "
            f"{manifest['schema']!r}")
    if manifest["package"] != "bootstrap-authority":
        raise AuthorityRefused(
            f"AUTHORITY_MANIFEST_PACKAGE_UNEXPECTED: "
            f"{manifest['package']!r}")
    if manifest["policy_id"] != POLICY_ID:
        raise AuthorityRefused(
            f"AUTHORITY_MANIFEST_POLICY_UNEXPECTED: "
            f"{manifest['policy_id']!r}")
    if manifest["target"] != FROZEN_TARGET:
        raise AuthorityRefused(
            "AUTHORITY_MANIFEST_TARGET_MISMATCH: the manifest target is "
            "not the exact frozen fresh-audit target")
    if manifest["design_event_id"] != EVENT_ID:
        raise AuthorityRefused("AUTHORITY_MANIFEST_EVENT_ID_UNEXPECTED")
    if manifest["design_attempt_ids"] != RESERVED_ATTEMPT_IDS:
        raise AuthorityRefused(
            "AUTHORITY_MANIFEST_ATTEMPT_IDS_UNEXPECTED: the manifest does "
            "not carry exactly the design-reserved attempt identities")
    if manifest["status"] != AUTHORITY_STATUS:
        raise AuthorityRefused(
            f"AUTHORITY_MANIFEST_STATUS_UNEXPECTED: "
            f"{manifest['status']!r}")
    if manifest["qualification_claim"] != AUTHORITY_QUALIFICATION_CLAIM:
        raise AuthorityRefused(
            "AUTHORITY_MANIFEST_QUALIFICATION_CLAIM_UNEXPECTED")
    if not isinstance(manifest["runtime_dependencies"], list) or \
            not all(isinstance(item, str) for item in
                    manifest["runtime_dependencies"]):
        raise AuthorityRefused("AUTHORITY_MANIFEST_RUNTIME_DEPS_INVALID")
    if manifest["source_provenance"] != EXPECTED_PROVENANCE:
        raise AuthorityRefused(
            "AUTHORITY_MANIFEST_PROVENANCE_INVALID: every production "
            "source path must carry the EXACT expected provenance (four "
            "EXACT_PRETARGET_BLOB_REUSE entries pinned to "
            f"{PRETARGET_REUSE_SOURCE_COMMIT} plus NEW_AUTHORITY_SPECIFIC)")
    return result

def verify_event_package(root, binding) -> dict:
    """Fail-closed verification of the frozen event package BEFORE any
    gate: pinned identity plus exact transport-projection equality with
    the binding (canonical JSON bytes)."""
    result = verify_package_bytes(
        os.fspath(root), binding.event_package["package_sha256"])
    manifest = result["document"]
    keys = set(manifest)
    if keys != set(EVENT_MANIFEST_KEYS):
        raise AuthorityRefused(
            f"EVENT_MANIFEST_KEYS_INVALID: "
            f"unknown={sorted(keys - set(EVENT_MANIFEST_KEYS))} "
            f"missing={sorted(set(EVENT_MANIFEST_KEYS) - keys)}")
    if manifest["schema"] != EVENT_MANIFEST_SCHEMA:
        raise AuthorityRefused(
            f"EVENT_MANIFEST_SCHEMA_UNEXPECTED: {manifest['schema']!r}")
    if canonical_bytes(manifest["transport_binding"]) != canonical_bytes(
            binding_projection(binding)):
        raise AuthorityRefused(
            "EVENT_PACKAGE_PROJECTION_MISMATCH: the frozen event package "
            "declares component identities that differ from this binding")
    return result

def _open_bound_artifact(event_package_root, descriptor, rows,
                         label: str) -> int:
    """Verified-open for an event-package artifact (gate/validator):
    descriptor path must be a manifest row of the ALREADY-VERIFIED
    package; no final symlink, regular + executable, exact SHA-256,
    rewind, HELD fd."""
    if descriptor["path"] not in rows:
        raise AuthorityRefused(
            f"{label}_NOT_PACKAGE_MANIFEST_ROW: {descriptor['path']!r}")
    path = os.path.join(os.fspath(event_package_root), descriptor["path"])
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise AuthorityRefused(f"{label}_OPEN_REFUSED: {exc!r}") from exc
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise AuthorityRefused(f"{label}_NOT_REGULAR_FILE")
        if not info.st_mode & 0o111:
            raise AuthorityRefused(f"{label}_NOT_EXECUTABLE")
        if _hash_fd(fd) != descriptor["sha256"]:
            raise AuthorityRefused(
                f"{label}_ARTIFACT_DIGEST_MISMATCH: live artifact differs "
                "from the bound descriptor SHA-256")
    except Exception:
        os.close(fd)
        raise
    os.lseek(fd, 0, os.SEEK_SET)
    return fd

def open_dynamic_gate(event_package_root, binding, event_manifest,
                      gate: str) -> int:
    """Open + verify ONE frozen dynamic-gate artifact (by gate name)
    from the ALREADY-VERIFIED event-package tree; HELD for its
    exactly-once live execution."""
    return _open_bound_artifact(
        event_package_root, binding.dynamic_gates[gate],
        {row["path"] for row in event_manifest["files"]}, gate)

def open_output_validator(event_package_root, binding,
                          event_manifest) -> int:
    """Open + verify the frozen STRUCTURAL OUTPUT VALIDATOR from the
    ALREADY-VERIFIED tree; HELD at construction; no public API supplies
    a validator path."""
    return _open_bound_artifact(
        event_package_root, binding.output_validator,
        {row["path"] for row in event_manifest["files"]},
        "OUTPUT_VALIDATOR")

def _kill_and_reap(child_pid: int) -> None:
    """SIGKILL + reap the child (best effort)."""
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
    """Close every non-None fd, absorbing failures."""
    for fd in fds:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass

def _sanitize_structural_diagnostic(stderr: bytes) -> str:
    """Bounded STRUCTURAL-ONLY diagnostic grammar: accepted ONLY when the
    first stderr line is the frozen VALIDATION_ERROR emission, reduced
    to a short uppercase [A-Z0-9_] token; a returned token can never
    contain report prose, credentials, paths or auditor text."""
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
    """Child-side prep for a dynamic gate / the validator: bounded
    result pipe on stdout, devnull stdin/stderr (the validator gets a
    bounded writable stderr_w on fd 2), NO credential fd inherited,
    every other fd closed, the verified open gate fd exec'd; report_fd
    (validator only) is the sealed snapshot.  Never returns."""
    try:
        os.dup2(devnull, 0)
        os.dup2(result_w, 1)
        os.dup2(stderr_w if stderr_w is not None else devnull, 2)
        exec_target = gate_fd
        keep = {0, 1, 2, gate_fd}
        if report_fd is not None:
            # alias-safe slot remap: DISTINCT fresh copies of BOTH the
            # exec target and the report — the dup2 can only clobber a
            # copy or an unrelated fd, never the exec target.
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

def _run_child_once(label: str, gate_fd: int, argv, env: dict,
                    timeout: float, max_result: int,
                    report_bytes: bytes = None,
                    capture_stderr: bool = False) -> bytes:
    """Execute the verified gate/validator fd EXACTLY ONCE with a
    bounded fail-closed timeout; return the raw size-bounded result
    bytes (fork/exec failure, hang, oversize or non-zero exit
    refuses).  report_bytes (validator only) is the sealed immutable
    snapshot memfd; capture_stderr yields a bounded STRUCTURAL-ONLY
    token from the validator's stderr."""
    report_fd = None
    if report_bytes is not None:
        report_fd = memfd_create("bootstrap-authority-report-snapshot",
                                 MFD_CLOEXEC | MFD_ALLOW_SEALING)
        try:
            os.write(report_fd, report_bytes)
            os.lseek(report_fd, 0, os.SEEK_SET)
            fcntl.fcntl(report_fd, F_ADD_SEALS, REQUIRED_SEALS)
            if fcntl.fcntl(report_fd, F_GET_SEALS) & REQUIRED_SEALS != \
                    REQUIRED_SEALS:
                raise AuthorityRefused("REPORT_SNAPSHOT_SEAL_INCOMPLETE")
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
            raise AuthorityError(f"{label}_FORK_FAILED: {exc!r}") from exc
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
            os.close(report_fd)
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
                raise AuthorityRefused(
                    f"{label}_TIMEOUT: did not finish within "
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
                        if len(output) > max_result:
                            _kill_and_reap(child_pid)
                            raise AuthorityRefused(
                                f"{label}_OUTPUT_TOO_LARGE: emitted more "
                                f"than {max_result} result bytes")
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
                        raise AuthorityRefused(
                            f"{label}_STDERR_TOO_LARGE: emitted more than "
                            f"{VALIDATOR_STDERR_MAX} stderr bytes; failing "
                            "closed")
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
            while True:
                try:
                    chunk = os.read(err_r, 65536)
                except BlockingIOError:
                    break
                if not chunk:
                    break
                stderr_out += chunk
                if len(stderr_out) > VALIDATOR_STDERR_MAX:
                    raise AuthorityRefused(
                        f"{label}_STDERR_TOO_LARGE: emitted more than "
                        f"{VALIDATOR_STDERR_MAX} stderr bytes; failing "
                        "closed")
        if exitcode != 0:
            reason = ("EXEC_FAILED" if exitcode == CHILD_EXIT_EXEC_FAIL
                      else "NONZERO_EXIT")
            detail = f"{label}_{reason}: exited {exitcode}"
            if capture_stderr:
                token = _sanitize_structural_diagnostic(stderr_out)
                if token:
                    detail += f"; structural_error={token}"
            raise AuthorityRefused(detail)
        if not output:
            raise AuthorityRefused(f"{label}_OUTPUT_MISSING: no result "
                                   "bytes")
        return output
    finally:
        _close_fds(result_r, result_w, devnull, report_fd, err_r, err_w)

def _strict_envelope(output: bytes, binding, label: str, fields,
                     schema: str) -> dict:
    """Strict fail-closed envelope core shared by ALL gate/validator
    results: strict JSON, object shape, exact key set and schema tag,
    exact event/role/attempt match, top-level status PASS (never
    inferred from the exit code)."""
    try:
        result = strict_loads(output)
    except BindingError as exc:
        raise AuthorityRefused(f"{label}_RESULT_MALFORMED: {exc}") from exc
    if not isinstance(result, dict):
        raise AuthorityRefused(f"{label}_RESULT_NOT_AN_OBJECT")
    keys = set(result)
    expected = set(fields)
    if keys != expected:
        raise AuthorityRefused(
            f"{label}_RESULT_KEYS_INVALID: "
            f"unknown={sorted(keys - expected)} "
            f"missing={sorted(expected - keys)}")
    if result["schema"] != schema:
        raise AuthorityRefused(f"{label}_RESULT_SCHEMA_UNEXPECTED: "
                               f"{result['schema']!r}")
    if result["event_id"] != binding.event_id or \
            result["auditor_role"] != binding.auditor_role or \
            result["attempt_id"] != binding.attempt_id:
        raise AuthorityRefused(f"{label}_RESULT_CONTEXT_MISMATCH: result "
                               "event/role/attempt differ from the binding")
    if result["status"] != "PASS":
        raise AuthorityRefused(f"{label}_RESULT_NOT_PASS: "
                               f"{result['status']!r}")
    return result

def _result_evidence(prefix: str, result: dict) -> dict:
    """Durable fresh-evidence fields for one validated gate result."""
    canonical = canonical_bytes(result).decode()
    return {f"{prefix}_result": canonical,
            f"{prefix}_result_sha256": hashlib.sha256(
                canonical.encode()).hexdigest(),
            f"{prefix}_result_size": len(canonical.encode())}

def _validate_client_selection_result(output: bytes, binding) -> dict:
    """Strict validation of the FRESH client-selection preflight
    envelope: the shared core PLUS exact equality of the bound provider
    role, client family, model, effort and client-executable identity/
    version/SHA-256 — the NO-FALLBACK enforcement point."""
    result = _strict_envelope(output, binding, "CLIENT_SELECTION_PREFLIGHT",
                              CLIENT_SELECTION_RESULT_FIELDS,
                              binding.dynamic_gates[
                                  "CLIENT_SELECTION_PREFLIGHT"][
                                  "result_schema"])
    selection = binding.auditor_selection
    client = selection["client_executable"]
    bound = {**{k: selection[k] for k in
                ("provider_role", "client_family", "model", "effort")},
             "client_executable_identity": client["identity"],
             "client_executable_version": client["version"],
             "client_executable_sha256": client["sha256"]}
    for key, want in bound.items():
        if result[key] != want:
            raise AuthorityRefused(
                f"CLIENT_SELECTION_PREFLIGHT_BOUND_MISMATCH: {key} "
                "differs from the governance-frozen binding selection; "
                "failing closed pre-inference with NO fallback")
    return _result_evidence("client_selection", result)

def _validate_network_readiness_result(output: bytes, binding) -> dict:
    """Strict validation of the FRESH network-readiness envelope: the
    shared core plus the exact transport-binding context and the EXACT
    checks key set route + resolver, each an exact {status, detail}
    PASS object; a top-level PASS never overrides a failed check."""
    result = _strict_envelope(output, binding, "NETWORK_READINESS",
                              NETWORK_READINESS_RESULT_FIELDS,
                              binding.dynamic_gates["NETWORK_READINESS"][
                                  "result_schema"])
    if result["provider_role"] != \
            binding.auditor_selection["provider_role"] or \
            result["boundary_launcher_sha256"] != \
            binding.boundary_launcher["sha256"] or \
            result["sandbox_profile_id"] != binding.sandbox_profile_id:
        raise AuthorityRefused(
            "NETWORK_READINESS_RESULT_CONTEXT_MISMATCH: result "
            "provider/launcher/profile differ from the binding")
    checks = result["checks"]
    if not isinstance(checks, dict) or set(checks) != \
            set(NETWORK_READINESS_CHECKS):
        raise AuthorityRefused(
            f"NETWORK_READINESS_CHECKS_INVALID: expected exactly "
            f"{sorted(NETWORK_READINESS_CHECKS)}, got "
            f"{sorted(checks) if isinstance(checks, dict) else checks!r}")
    for name in NETWORK_READINESS_CHECKS:
        check = checks[name]
        if not isinstance(check, dict) or \
                set(check) != set(NETWORK_READINESS_CHECK_FIELDS) or \
                not isinstance(check["detail"], dict):
            raise AuthorityRefused(
                f"NETWORK_READINESS_CHECK_INVALID: {name} must be an "
                "object with exactly status and an object detail")
        if check["status"] != "PASS":
            raise AuthorityRefused(
                f"NETWORK_READINESS_CHECK_NOT_PASS: {name} "
                f"{check['status']!r}")
    return _result_evidence("network_readiness", result)

def _validate_resource_gate_result(output: bytes, binding) -> dict:
    """Strict validation of the FRESH resource-gate envelope: the
    shared core plus EXACTLY three samples each explicitly PASS with
    an object detail."""
    result = _strict_envelope(output, binding, "RESOURCE_GATE",
                              RESOURCE_GATE_RESULT_FIELDS,
                              binding.dynamic_gates["RESOURCE_GATE"][
                                  "result_schema"])
    samples = result["samples"]
    if not isinstance(samples, list) or \
            len(samples) != RESOURCE_GATE_SAMPLES:
        raise AuthorityRefused(
            f"RESOURCE_GATE_SAMPLE_COUNT_INVALID: expected exactly "
            f"{RESOURCE_GATE_SAMPLES} samples, got "
            f"{len(samples) if isinstance(samples, list) else samples!r}")
    for index, sample in enumerate(samples):
        if not isinstance(sample, dict) or \
                set(sample) != set(RESOURCE_GATE_SAMPLE_FIELDS):
            raise AuthorityRefused(
                f"RESOURCE_GATE_SAMPLE_INVALID_AT_{index}")
        if sample["status"] != "PASS":
            raise AuthorityRefused(
                f"RESOURCE_GATE_SAMPLE_NOT_PASS_AT_{index}: "
                f"{sample['status']!r}")
        if not isinstance(sample["detail"], dict):
            raise AuthorityRefused(
                f"RESOURCE_GATE_SAMPLE_DETAIL_INVALID_AT_{index}")
    return _result_evidence("resource_gate", result)

_DYNAMIC_GATE_VALIDATORS = {
    "CLIENT_SELECTION_PREFLIGHT": _validate_client_selection_result,
    "NETWORK_READINESS": _validate_network_readiness_result,
    "RESOURCE_GATE": _validate_resource_gate_result,
}

def _validate_validator_result(output: bytes, binding, digest: str,
                               size: int) -> None:
    """Strict validation of the structural-validator result: the shared
    core PLUS exact match of output_name/report_sha256/report_size with
    the EXACT screened snapshot (SHAPE-ONLY for target_commit;
    check_report_binding is the authority)."""
    result = _strict_envelope(output, binding, "OUTPUT_VALIDATOR",
                              VALIDATOR_RESULT_FIELDS,
                              binding.output_validator["result_schema"])
    if result["output_name"] != binding.output_identity["name"] or \
            result["report_sha256"] != digest or \
            result["report_size"] != size:
        raise AuthorityRefused(
            "OUTPUT_VALIDATOR_RESULT_SNAPSHOT_MISMATCH: result output/"
            "digest/size differ from the exact screened snapshot")

def check_report_binding(snapshot: bytes, binding) -> None:
    """THE authority's OWN semantic report binding (readback 6.6) on
    the SAME screened snapshot AFTER validator PASS and BEFORE freeze,
    WITHOUT calling candidate target code: strict reparse then EXACT
    equality of target_commit (frozen 730d2b29) and event/role/attempt
    ids; a mismatch FAILS CLOSED with the FIXED safe token only."""
    try:
        report = strict_loads(snapshot)
    except BindingError:
        raise AuthorityRefused(REPORT_BINDING_UNPARSEABLE) from None
    if not isinstance(report, dict):
        raise AuthorityRefused(REPORT_BINDING_UNPARSEABLE)
    for key, want, token in (
            ("target_commit", binding.target["commit"],
             REPORT_TARGET_COMMIT_MISMATCH),
            ("event_id", binding.event_id, REPORT_EVENT_ID_MISMATCH),
            ("auditor_role", binding.auditor_role,
             REPORT_AUDITOR_ROLE_MISMATCH),
            ("attempt_id", binding.attempt_id, REPORT_ATTEMPT_ID_MISMATCH)):
        got = report.get(key)
        if got != want or isinstance(got, bool):
            raise AuthorityRefused(token)

def _child_setup(launcher_fd: int, metadata_w: int, fail_w: int,
                 devnull: int, custody_fd: int, auditor_fd: int,
                 invocation_fd: int, argv, env: dict) -> None:
    """Child-side preparation: session isolation (setsid BEFORE exec so
    the whole descendant tree is killable as one exact process group on
    timeout — never an unrelated host process), the fixed fd contract
    (CRED_FD=3 sealed custody, FAIL_FD=4 CLOEXEC exec-fail pipe,
    AUDITOR_EXEC_FD=5 HELD verified auditor, AUDITOR_INVOCATION_FD=6
    sealed frozen argv), then exec of the verified open fd (alias-safe
    remap).  Never returns."""
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
    """Outcome DATA ONLY — never authority.  Returned strictly AFTER the
    terminal outcome: returncode/exec_failed/metadata describe the
    boundary child, timed_out marks the authority-enforced deadline, and
    report_state carries the terminal report outcome with the frozen
    artifact digest/size."""
    returncode: int
    exec_failed: bool
    metadata: dict
    timed_out: bool
    report_state: str
    report_sha256: str
    report_size: int

class BootstrapAuthority:
    """One-shot controllerless target-independent authority for a single
    attempt of the wholly NEW PATH-B lineage.  Startup (fail closed at
    every step): (1) self-identity of THE EXECUTING authority package;
    (2) frozen event-package identity + exact transport-projection
    equality; (3) all three dynamic-gate artifacts and the structural
    validator identity-verified, fds HELD.  The event-package root is a
    MANDATORY constructor input; no attach/revival constructor exists;
    the attempt's accounting record is created O_EXCL inside run_attempt
    (attempt-GLOBAL, reserved-attempt-id key per BA-RB-001, RELATIVE TO
    the held verified binding-FROZEN custody OBJECT), so no second
    authority process can obtain authority for the same reserved
    attempt under ANY other binding, root or pathname replacement."""
    def __init__(self, binding, event_package_root) -> None:
        if not isinstance(binding, Binding):
            raise AuthorityError(
                "BOOTSTRAP_AUTHORITY_REQUIRES_A_PARSED_BINDING")
        if not isinstance(event_package_root, (str, os.PathLike)):
            raise AuthorityError(
                "BOOTSTRAP_AUTHORITY_REQUIRES_EVENT_PACKAGE_ROOT: a "
                "frozen event package root is mandatory — no default, "
                "no bypass")
        verify_own_package(binding)             # (1) own live bytes
        event_result = verify_event_package(event_package_root, binding)
        self._gate_fds = {              # (3) hold ALL verified gate fds
            gate: open_dynamic_gate(event_package_root, binding,
                                    event_result["document"], gate)
            for gate in DYNAMIC_GATE_ORDER}
        self._validator_fd = open_output_validator(
            event_package_root, binding, event_result["document"])
        self._binding = binding
        self._event_manifest = event_result["document"]
        self._machine = StateMachine(PREPARED)
        self._store = None
        self._launcher_fd = None
        self._custody = None
        self._auditor_fd = None
        self._invocation_fd = None
        self._out_dir_fd = None
        self._sink_fd = None
        self._spent = False
        self._gates_executed = False
    @property
    def state(self) -> str:
        return self._machine.state
    @property
    def store(self):
        return self._store
    def _binding_facts(self) -> dict:
        """Complete non-secret binding identity set durably recorded at
        CONSUMED_PRE_EXEC (no credential ever enters)."""
        b = self._binding
        facts = {"event_id": b.event_id, "auditor_role": b.auditor_role,
                 "attempt_id": b.attempt_id,
                 "prompt_contract_digest": b.prompt_contract_digest,
                 "common_evidence_manifest_digest":
                     b.common_evidence_manifest_digest,
                 "sandbox_profile_id": b.sandbox_profile_id,
                 "auditor_invocation_argc": len(b.auditor_invocation),
                 "auditor_invocation_sha256": hashlib.sha256(
                     canonical_bytes(list(b.auditor_invocation))).hexdigest(),
                 "output_identity_name": b.output_identity["name"],
                 "output_custody_root": b.output_identity["custody_root"],
                 "output_custody_dev": b.output_identity["custody_dev"],
                 "output_custody_ino": b.output_identity["custody_ino"],
                 "report_source": b.output_identity["report_source"],
                 "binding_digest": b.digest}
        for key in ("commit", "root_tree", "bootstrap_supervisor_tree",
                    "qualification_harness_tree", "skill_tree",
                    "remediation_parent"):
            facts[f"target_{key}"] = b.target[key]
        for key in ("provider_role", "client_family", "model", "effort"):
            facts[key] = b.auditor_selection[key]
        for key in ("identity", "version", "sha256"):
            facts[f"client_executable_{key}"] = \
                b.auditor_selection["client_executable"][key]
        for key in ("identity", "sha256"):
            facts[f"output_validator_{key}"] = b.output_validator[key]
        for key in ("auditor_timeout_seconds", "validator_timeout_seconds",
                    "max_report_bytes"):
            facts[key] = b.execution_limits[key]
        for prefix, ident in (("boundary_launcher", b.boundary_launcher),
                              ("tool_wrapper", b.tool_wrapper)):
            facts[f"{prefix}_identity"] = ident["identity"]
            facts[f"{prefix}_sha256"] = ident["sha256"]
        for prefix, pkg in (("event_package", b.event_package),):
            facts[f"{prefix}_package_sha256"] = pkg["package_sha256"]
        facts["authority_package_manifest_sha256"] = \
            b.authority_package["manifest_sha256"]
        facts["authority_package_sha256"] = \
            b.authority_package["package_sha256"]
        for gate, descriptor in b.dynamic_gates.items():
            prefix = gate.lower()
            facts[f"{prefix}_identity"] = descriptor["identity"]
            facts[f"{prefix}_sha256"] = descriptor["sha256"]
        return facts
    def _execute_dynamic_gate(self, gate: str) -> dict:
        """Execute ONE frozen dynamic-gate artifact ONCE, NOW; strictly
        validate the fresh result; return the durable fresh-evidence
        fields for GATES_PASSED.  NO credential fd or launch authority
        is ever exposed to a gate."""
        descriptor = self._binding.dynamic_gates[gate]
        fd = self._gate_fds[gate]
        got = _hash_fd(fd)            # held-fd drift check immediately
        os.lseek(fd, 0, os.SEEK_SET)
        if got != descriptor["sha256"]:
            raise AuthorityRefused(f"{gate}_FD_DRIFT: the held gate fd no "
                                   "longer matches the bound artifact")
        b = self._binding
        argv = [descriptor["identity"], b.event_id, b.auditor_role,
                b.attempt_id]
        if gate == "CLIENT_SELECTION_PREFLIGHT":
            client = b.auditor_selection["client_executable"]
            argv += [b.auditor_selection["provider_role"],
                     b.auditor_selection["client_family"],
                     b.auditor_selection["model"],
                     b.auditor_selection["effort"],
                     client["identity"], client["version"],
                     client["sha256"]]
        elif gate == "NETWORK_READINESS":
            argv += [b.auditor_selection["provider_role"],
                     b.boundary_launcher["sha256"],
                     b.sandbox_profile_id]
        output = _run_child_once(
            gate, fd, argv, {"PATH": "/usr/bin:/bin", "LANG": "C"},
            timeout=descriptor["timeout_seconds"],
            max_result=descriptor["max_result_bytes"])
        evidence = _DYNAMIC_GATE_VALIDATORS[gate](output, self._binding)
        prefix = gate.lower()
        evidence.update({f"{prefix}_identity": descriptor["identity"],
                         f"{prefix}_sha256": descriptor["sha256"],
                         f"{prefix}_result_schema":
                             descriptor["result_schema"]})
        return evidence
    def run_attempt(self, credential_source_fd: int, launcher_path,
                    auditor_executable_path, report_staging_path,
                    output_root) -> AttemptResult:
        """THE single public authority operation: the COMPLETE one-shot
        attempt lifecycle in ONE caller-uninterruptible call: frozen
        custody-root/report-source + custody OBJECT identity gates
        (BA-PREP-001/002 + RB2-001: held fd == the frozen st_dev/st_ino
        directory object, opened ONCE); attempt-global O_EXCL accounting
        RELATIVE TO THAT SAME HELD object (PREPARED); sealed frozen-argv
        spec; launcher/auditor verified HELD; the THREE dynamic gates
        fresh in frozen order (RESOURCE_GATE LAST); held-fd re-hash;
        durable GATES_PASSED; the authority-CREATED attempt-owned report
        sink O_EXCL under the SAME held object (BA-PREP-RB2-002);
        credential custody (BA-RB-002); durable CONSUMED_PRE_EXEC;
        irreversible spend; IMMEDIATE fork/exec; bounded wait; HELD-sink
        report lifecycle; TERMINAL; custody/fds closed -> AttemptResult.
        No caller surface for a custody object, role, argv tail, env
        override, timeout or validator path."""
        if not isinstance(credential_source_fd, int) or \
                isinstance(credential_source_fd, bool):
            raise AuthorityError(
                "RUN_ATTEMPT_REQUIRES_CREDENTIAL_SOURCE_FD: the public "
                "authority operation ingests a credential SOURCE fd, "
                "never a CredentialCustody or any other object")
        for name, value in (("launcher_path", launcher_path),
                            ("auditor_executable_path",
                             auditor_executable_path),
                            ("report_staging_path", report_staging_path),
                            ("output_root", output_root)):
            if not isinstance(value, (str, os.PathLike)):
                raise AuthorityError(
                    f"RUN_ATTEMPT_REQUIRES_{name.upper()}: a mandatory "
                    "path input — no default, no bypass")
        if self._machine.state != PREPARED:
            raise AuthorityError(
                f"RUN_ATTEMPT_REFUSED_STATE_{self._machine.state}: the "
                "single authority operation requires PREPARED")
        if self._launcher_fd is not None or self._custody is not None \
                or self._spent or self._gates_executed \
                or self._store is not None:
            raise AuthorityError("RUN_ATTEMPT_REFUSED_ALREADY_ADVANCED: "
                                 "no second authority operation exists")
        # BA-PREP-001/002: the caller arguments must name EXACTLY the
        # binding-frozen custody root / report source (normpath identity;
        # refused BEFORE any custody open, claim, gate or credential
        # read); all actions below use the FROZEN values exclusively.
        frozen_output = self._binding.output_identity["custody_root"]
        frozen_source = self._binding.output_identity["report_source"]
        if os.path.normpath(os.fspath(output_root)) != frozen_output:
            raise AuthorityRefused(
                "OUTPUT_CUSTODY_ROOT_MISMATCH: the caller-supplied output "
                "root is not the binding-frozen attempt output custody "
                "root; refusing fail-closed before any authority action")
        if os.path.normpath(os.fspath(report_staging_path)) != frozen_source:
            raise AuthorityRefused(
                "REPORT_SOURCE_MISMATCH: the caller-supplied report "
                "staging path is not the binding-frozen attempt report "
                "source; refusing fail-closed before any authority action")
        # BA-PREP-RB2-001: open the frozen custody pathname EXACTLY ONCE
        # and verify the HELD fd IS the binding-frozen directory OBJECT
        # (st_dev/st_ino): a pathname now resolving to a DIFFERENT
        # directory object (rename + replacement at the exact frozen
        # pathname) is refused BEFORE any claim, gate or credential read
        # (pre-advance: the authority stays PREPARED, nothing acquired).
        self._out_dir_fd = open_custody_dir(frozen_output)
        try:
            held_stat = os.fstat(self._out_dir_fd)
            if (held_stat.st_dev, held_stat.st_ino) != (
                    self._binding.output_identity["custody_dev"],
                    self._binding.output_identity["custody_ino"]):
                raise AuthorityRefused(
                    "OUTPUT_CUSTODY_OBJECT_MISMATCH: the frozen custody "
                    "pathname no longer resolves to the binding-frozen "
                    "custody directory OBJECT; refusing fail-closed "
                    "before any authority action")
        except Exception:
            fd, self._out_dir_fd = self._out_dir_fd, None
            try:
                os.close(fd)
            except OSError:
                pass
            raise
        self._gates_executed = True
        try:
            sink_name = os.path.basename(frozen_source)
            # A (BA-RB-001 + RB2-001): attempt-GLOBAL O_EXCL claim keyed
            # by the reserved attempt id ALONE, created RELATIVE TO THE
            # SAME HELD verified directory OBJECT — never a pathname
            # re-open, so a mid-run rebind cannot split accounting
            # custody from output custody.
            self._store = AccountingStore.create_at(
                self._out_dir_fd, accounting_name(self._binding),
                self._binding.digest)
            # B: the frozen argv leaves the binding ONLY as sealed bytes.
            self._invocation_fd = make_invocation_fd(
                self._binding.auditor_invocation)
            # C: static identities BEFORE the gates — launcher + LIVE auditor, HELD.
            self._launcher_fd = open_verified_launcher(
                launcher_path, self._binding.boundary_launcher["sha256"])
            self._auditor_fd = open_verified_auditor_executable(
                auditor_executable_path,
                self._binding.auditor_selection["client_executable"][
                    "sha256"])
            # D: the THREE fresh gates exactly once each, frozen order (RESOURCE_GATE LAST); then E: drift re-hash.
            evidence = {}
            for gate in DYNAMIC_GATE_ORDER:   # frozen order, last gate
                evidence.update(self._execute_dynamic_gate(gate))
            self._rehash_held("BEFORE_GATES_PASSED")  # gate-interval drift
            # F: durable GATES_PASSED BEFORE any credential read.
            self._store.append(GATES_PASSED,          # fsync'd inside append
                               extra=evidence)
            self._machine.transition(GATES_PASSED)
            # BA-PREP-RB2-002: the authority CREATES the attempt-owned
            # report sink NOW — after the gates, BEFORE any credential
            # read — O_CREAT|O_EXCL|O_NOFOLLOW relative to the SAME held
            # custody object; the frozen invocation designates this
            # exact sink (parser-enforced); a pre-existing object at the
            # frozen sink name refuses.
            try:
                self._sink_fd = create_report_sink(self._out_dir_fd,
                                                   sink_name)
            except ReportRefused as exc:
                raise AuthorityRefused(
                    f"REPORT_SINK_CREATE_REFUSED: {exc}") from exc
            # G+H (BA-RB-002): ONLY NOW custody ingest reads the credential; role ONLY from the binding.
            self._custody = CredentialCustody.ingest(
                credential_source_fd, self._binding.auditor_role)
            if self._custody.role != self._binding.auditor_role:
                raise AuthorityRefused(
                    "CUSTODY_ROLE_MISMATCH: defense-in-depth check — the "
                    "custody role does not equal binding.auditor_role")
            # I: durable CONSUMED_PRE_EXEC immediately after custody.
            self._store.append(CONSUMED_PRE_EXEC,      # fsync'd inside append
                               extra=self._binding_facts())
            self._machine.transition(CONSUMED_PRE_EXEC)
        except Exception as exc:
            if self._sink_fd is not None:
                # the sink is authority-created (O_EXCL): safe-discard
                # the EXACT held object on the way out; a replacement
                # name is never unlinked (identity-checked).
                try:
                    discard_held_sink(
                        self._out_dir_fd,
                        os.path.basename(frozen_source), self._sink_fd)
                except Exception:
                    pass
            self._preexec_stop()   # PREPARED/GATES_PASSED -> fail-closed
            if isinstance(exc, AuthorityRefused):
                raise
            raise AuthorityRefused(f"PREEXEC_ATTEMPT_FAILED: "
                                   f"{exc!r}") from exc
        # IRREVERSIBLE SPEND: consumption is IMMEDIATELY followed by the
        # fork attempt inside the SAME public call — control never
        # returns to the caller between CONSUMED_PRE_EXEC and exec.
        self._spent = True
        return self._fork_and_launch()
    def _rehash_held(self, phase: str) -> None:
        """Re-hash the HELD launcher + auditor fds before gate
        acceptance and again post-consumption (drift refuses)."""
        b = self._binding
        got = _hash_fd(self._launcher_fd)
        os.lseek(self._launcher_fd, 0, os.SEEK_SET)
        if got != b.boundary_launcher["sha256"]:
            raise AuthorityRefused(
                f"LAUNCHER_DIGEST_MISMATCH_{phase}: expected "
                f"{b.boundary_launcher['sha256']} got {got}")
        got = _hash_fd(self._auditor_fd)
        os.lseek(self._auditor_fd, 0, os.SEEK_SET)
        expected = b.auditor_selection["client_executable"]["sha256"]
        if got != expected:
            raise AuthorityRefused(
                f"PREEXEC_EXECUTABLE_IDENTITY_FAIL_{phase}: expected "
                f"{expected} got {got}")
    def _fork_and_launch(self) -> AttemptResult:
        """Post-consumption continuation (ONLY from run_attempt after
        the irreversible spend): re-hash, IMMEDIATE fork/exec into a
        DEDICATED SESSION, EXEC_ATTEMPTED accounting, the bounded
        MONOTONIC-deadline wait, timeout kill of the EXACT attempt
        process group with consumed terminal accounting, and the
        process-bound report lifecycle — all before any return."""
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
                raise AuthorityError(f"FORK_FAILED: {exc!r}") from exc
            if child_pid == 0:
                _child_setup(self._launcher_fd, md_w, fail_w, devnull,
                             self._custody.fd, self._auditor_fd,
                             self._invocation_fd, argv, child_env)
            os.close(md_w)
            os.close(fail_w)
            os.close(devnull)
            md_w = fail_w = devnull = None
            self._store.append(EXEC_ATTEMPTED,
                               extra={"child_pid": child_pid})
            self._machine.transition(EXEC_ATTEMPTED)
            # bounded wait: nonblocking pipes + WNOHANG reap under the
            # monotonic frozen deadline.
            os.set_blocking(fail_r, False)
            os.set_blocking(md_r, False)
            deadline = time.monotonic() + timeout
            fail_eof = False
            md_eof = False
            exitcode = None
            grace_deadline = None
            while True:
                if time.monotonic() >= deadline:
                    # boundary race: one final nonblocking reap decides
                    # timeout-vs-completed honestly
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
                        grace_deadline = time.monotonic() + METADATA_GRACE
                    elif time.monotonic() >= grace_deadline:
                        break
                if not progressed:
                    time.sleep(0.01)               # bounded poll, no spin
        except BaseException as exc:
            # ANY post-consumption parent-side failure gets the SAME
            # centralized fail-closed settlement (fds closed, the EXACT
            # process group killed and reaped, then settlement); the
            # original failure re-raises only when the durable
            # settlement completed, else the incompleteness error.
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
            raise   # settlement re-raises with original_error
        finally:
            _close_fds(md_r, fail_r)
        if timed_out:
            # timeout is AFTER durable CONSUMED_PRE_EXEC — authority
            # CONSUMED, engagement CONSUMED FAIL-CLOSED, no report
            # accepted; the process group is killed and the direct child
            # reaped BEFORE the settlement.
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
        setsid, so pgid == child_pid covers the whole descendant tree,
        never an unrelated process) and reap the direct child."""
        try:
            if os.getpgid(child_pid) == child_pid:
                os.killpg(child_pid, SIGKILL)
            else:
                os.kill(child_pid, SIGKILL)
        except OSError:
            pass          # already dead: the caller reaps deterministically
    def _close_authority_holds(self) -> None:
        """Close the authority-held sealed custody and EVERY held fd
        (launcher/auditor/invocation/validator/gates, the pre-opened
        output-custody dir fd, the held report sink fd) on EVERY
        terminal path; each close absorbs its own failure."""
        try:
            if self._custody is not None:
                self._custody.close()
        except Exception:
            pass
        held = [self._launcher_fd, self._auditor_fd,
                self._invocation_fd, self._validator_fd,
                self._out_dir_fd, self._sink_fd]
        held.extend(self._gate_fds.values())
        for fd in held:
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass
        self._launcher_fd = self._auditor_fd = None
        self._invocation_fd = None
        self._validator_fd = None
        self._out_dir_fd = None
        self._sink_fd = None
        self._gate_fds = {}
    def _settle_post_consumption(self, report_state, report_extra,
                                 terminal_extra=None, original_error=None,
                                 related_error=None) -> None:
        """THE single centralized post-consumption terminal settlement.
        Concept A, durable accounting ATTEMPT: the report-outcome record
        (when one applies) then TERMINAL; the FIRST durable failure
        stops further appends (the record is preserved, never success).
        Concept B (the finally), guaranteed fail-closed death: the
        consumed attempt lands TERMINAL, custody/fds closed, never
        raising nor masking an outcome; a durable failure raises the
        incompleteness error, success re-raises original_error."""
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
                pass
        except Exception as exc:
            durable_error = exc
        finally:
            try:
                self._machine.fail_closed_terminal()   # no-op iff there
            except Exception:
                pass
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
        clean immutable snapshot: held fd re-hashed immediately before
        execution; only frozen non-secret binding context in the argv;
        minimal environment; NO credential fd; sealed-memfd snapshot
        delivery; frozen validator timeout; a WRITABLE bounded stderr
        channel surfaces a structural failure's bounded safe token; any
        refusal is classified REPORT_INVALID by the caller (never a
        second execution; the PASS is NEVER sufficient)."""
        descriptor = self._binding.output_validator
        got = _hash_fd(self._validator_fd)
        os.lseek(self._validator_fd, 0, os.SEEK_SET)
        if got != descriptor["sha256"]:
            raise AuthorityRefused(
                "OUTPUT_VALIDATOR_FD_DRIFT: the held validator fd no "
                "longer matches the bound artifact")
        digest = hashlib.sha256(snapshot).hexdigest()
        b = self._binding
        output = _run_child_once(
            "OUTPUT_VALIDATOR", self._validator_fd,
            [descriptor["identity"], b.event_id, b.auditor_role,
             b.attempt_id, b.output_identity["name"], digest,
             str(len(snapshot))],
            {"PATH": "/usr/bin:/bin", "LANG": "C"},
            timeout=b.execution_limits["validator_timeout_seconds"],
            max_result=descriptor["max_result_bytes"],
            report_bytes=snapshot, capture_stderr=True)
        _validate_validator_result(output, b, digest, len(snapshot))
    def _report_and_terminalize(self, core) -> AttemptResult:
        """Process-bound post-exec report lifecycle: ONE immutable
        snapshot of the HELD authority-created sink OBJECT (never a
        pathname re-open; RB2-002: empty sink = honest REPORT_MISSING)
        -> SAME-custody screen (contaminated = REPORT_SCREEN_FAIL) ->
        frozen structural validator -> the authority's OWN semantic
        report binding (fixed safe tokens only) -> 0444 O_EXCL freeze
        under the SAME held custody fd -> TERMINAL.  Every refusal
        terminalizes fail-closed inside THIS call; digest/size recorded
        only AFTER the screen passes; cleanup unlinks ONLY the exact
        held sink object, never a replacement at the sink pathname."""
        returncode, exec_failed, metadata = core
        outcome = {"report_state": "", "report_sha256": "",
                   "report_size": 0}
        sink_name = os.path.basename(
            self._binding.output_identity["report_source"])
        try:
            if exec_failed:
                # the boundary never exec'd: no report phase applies —
                # direct consumed terminal
                self._settle_post_consumption(
                    None, None,
                    {"terminal_reason": "EXEC_FAILED_AFTER_CONSUMPTION"})
            else:
                snapshot = snapshot_held_sink(
                    self._sink_fd,
                    size_limit=self._binding.execution_limits[
                        "max_report_bytes"])
                if snapshot is None:
                    discard_held_sink(self._out_dir_fd, sink_name,
                                      self._sink_fd)
                    self._settle_post_consumption(
                        REPORT_MISSING,
                        {"terminal_reason": "REPORT_MISSING"})
                    outcome["report_state"] = REPORT_MISSING
                elif self._custody.contains(snapshot):
                    discard_held_sink(self._out_dir_fd, sink_name,
                                      self._sink_fd)
                    self._settle_post_consumption(
                        REPORT_SCREEN_FAIL,
                        {"terminal_reason": "REPORT_SCREEN_FAIL"})
                    outcome["report_state"] = REPORT_SCREEN_FAIL
                else:
                    try:
                        self._run_validator(snapshot)
                        check_report_binding(snapshot, self._binding)
                    except AuthorityError as exc:
                        # durably pin ONLY the snapshot hash/size that
                        # reached validation (the invalid bytes are
                        # never retained); REPORT_INVALID stays
                        # terminal/nonconforming — no freeze, no
                        # acceptance, no retry; a semantic-binding
                        # refusal carries its FIXED safe token.
                        invalid_sha = hashlib.sha256(snapshot).hexdigest()
                        token = (str(exc) if str(exc) in
                                 (REPORT_BINDING_UNPARSEABLE,
                                  REPORT_TARGET_COMMIT_MISMATCH,
                                  REPORT_EVENT_ID_MISMATCH,
                                  REPORT_AUDITOR_ROLE_MISMATCH,
                                  REPORT_ATTEMPT_ID_MISMATCH)
                                 else f"REPORT_INVALID: {exc}"[:180])
                        discard_held_sink(self._out_dir_fd, sink_name,
                                          self._sink_fd)
                        self._settle_post_consumption(
                            REPORT_INVALID,
                            {"terminal_reason": token,
                             "report_sha256": invalid_sha,
                             "report_size": len(snapshot)})
                        outcome["report_state"] = REPORT_INVALID
                        outcome["report_sha256"] = invalid_sha
                        outcome["report_size"] = len(snapshot)
                    else:
                        frozen = freeze_snapshot(
                            snapshot, self._out_dir_fd,
                            self._binding.output_identity["name"])
                        discard_held_sink(self._out_dir_fd, sink_name,
                                          self._sink_fd)
                        # a settlement failure raises the exact
                        # incompleteness error; the frozen artifact
                        # REMAINS operator-custodied evidence (never
                        # deleted, never a conforming first pass)
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
            # operational report-custody refusal (invalid sink object,
            # oversize, unsafe output, no-overwrite collision): terminal
            # fail-closed with the bounded durable reason, no retry; a
            # settlement accounting failure raises the exact
            # incompleteness error chaining this refusal.
            self._settle_post_consumption(
                None, None,
                {"terminal_reason": f"REPORT_CUSTODY_REFUSED: {exc}"[:256]},
                related_error=exc)
        except PostConsumptionTerminalAccountingError:
            raise
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
        ALWAYS happens (authority dead even if the medium is
        unavailable); the durable append is best-effort; held
        custody/fds closed."""
        try:
            if self._store is not None:
                self._store.append(TERMINAL_PREEXEC_STOP)
        except Exception:
            pass
        if self._machine.state in (PREPARED, GATES_PASSED):
            self._machine.transition(TERMINAL_PREEXEC_STOP)
        self._close_authority_holds()
