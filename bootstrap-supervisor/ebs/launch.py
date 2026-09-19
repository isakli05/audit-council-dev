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
path, with no flag and no environment override.

The frozen boundary-launcher executable is verified by opening it ONCE,
hashing the ALREADY-OPEN file, and executing THAT OPEN FILE DESCRIPTOR
via execveat(AT_EMPTY_PATH) (fexecve fallback).  A pathname re-open is
never used after verification; unavailability of the identity-preserving
exec method fails closed.  The held fd is re-hashed immediately before
fork so same-inode drift after consumption also fails closed.
"""
from __future__ import annotations

import ctypes
import errno
import hashlib
import json
import os
import platform
import stat
from dataclasses import dataclass

from .accounting import AccountingStore
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
    identities, every per-file size/SHA-256, and exact payload-set
    equality (unsafe row paths cannot match the walked set — refused
    structurally)."""
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
        doc = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LaunchRefused(f"PACKAGE_MANIFEST_MALFORMED: {exc!r}") from exc
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
        recorded[row["path"]] = row
    # Walk the LIVE tree; every regular file must be a manifest row with
    # exactly the recorded size/SHA-256 (verified in the same pass); any
    # unrecorded file or any manifest row with no live file is refused.
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
            "manifest_sha256": live_manifest, "package_sha256": declared}


def verify_live_package_identity(binding) -> dict:
    """Production self-verification entry: verifies THE EXECUTING EBS
    PACKAGE against the binding pins.  No root argument, no CLI flag,
    no environment variable; every Supervisor construction runs it
    before gates/authority are reachable."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return verify_package_identity(
        root, binding.ebs_package["manifest_sha256"],
        binding.ebs_package["package_sha256"])


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
    Startup (before any gate/authority operation): runtime package
    self-identity verification, then mechanical binding to THIS store
    (attempt id AND binding digest).  No attach/revival constructor
    exists; an existing same-attempt record fails closed at store
    creation (replacement = new operator authority + new attempt id +
    new EBS process + new accounting)."""

    def __init__(self, binding, store: AccountingStore) -> None:
        if not isinstance(store, AccountingStore):
            raise LaunchError("SUPERVISOR_REQUIRES_ACCOUNTING_STORE")
        verify_live_package_identity(binding)
        if store.attempt_id != binding.attempt_id:
            raise LaunchError(
                f"STORE_ATTEMPT_MISMATCH: store holds {store.attempt_id!r} "
                f"but binding declares {binding.attempt_id!r}")
        if store.binding_digest != binding.digest:
            raise LaunchError("STORE_BINDING_DIGEST_MISMATCH: the store "
                              "was not created from this exact binding "
                              "document")
        self._binding = binding
        self._store = store
        self._machine = StateMachine(store.last_state or PREPARED)
        self._launcher_fd = None
        self._issued_grant = None    # single issuance: consume() -> grant
        self._spent = False          # irreversible launch-spent guard

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

    def validate_gates(self) -> None:
        """PREPARED -> GATES_PASSED (binding + all gate evidence were
        fully validated at parse; this records the durable passage)."""
        if self._machine.state != PREPARED:
            raise LaunchError(
                f"GATES_ALREADY_EVALUATED: {self._machine.state}")
        try:
            self._store.append(GATES_PASSED)
        except Exception as exc:
            self._preexec_stop()
            raise LaunchRefused(f"GATES_RECORD_FAILED: {exc!r}") from exc
        self._machine.transition(GATES_PASSED)

    def verify_launcher(self, path) -> int:
        if self._machine.state not in (PREPARED, GATES_PASSED):
            raise LaunchError("LAUNCHER_VERIFICATION_LATE")
        if self._launcher_fd is not None:
            os.close(self._launcher_fd)
        self._launcher_fd = open_verified_launcher(
            path, self._binding.boundary_launcher["sha256"])
        return self._launcher_fd

    def consume(self) -> LaunchGrant:
        """Durable atomic consumption BEFORE any exec path exists; single
        issuance; the record persists the complete binding identity set."""
        if self._machine.state != GATES_PASSED:
            raise LaunchError(
                f"CONSUME_REFUSED_STATE_{self._machine.state}: gates must "
                "pass first")
        if self._launcher_fd is None:
            raise LaunchError("CONSUME_REFUSED_NO_VERIFIED_LAUNCHER")
        if self._issued_grant is not None:
            raise LaunchError("CONSUME_REFUSED_GRANT_ALREADY_ISSUED")
        self._store.append(CONSUMED_PRE_EXEC,   # fsync'd inside append
                           extra=self._binding_facts())
        self._machine.transition(CONSUMED_PRE_EXEC)
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
        if self._machine.state in (PREPARED, GATES_PASSED):
            self._store.append(TERMINAL_PREEXEC_STOP)
            self._machine.transition(TERMINAL_PREEXEC_STOP)
