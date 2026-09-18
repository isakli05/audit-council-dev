"""Controllerless one-shot verified boundary child execution.

Primary launch authority is NON-EXPORTABLE EBS PROCESS STATE plus
state-machine control flow: a single-use in-process grant object created
only by the durably recorded GATES_PASSED -> CONSUMED_PRE_EXEC transition.
No bearer token exists in any file, argv, environment, or IPC surface;
there is no controller on this path.

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
    """Single-use, non-exportable, in-process capability.

    Holds no token bytes: it is alive only inside the EBS process that
    performed the durable consumption transition, and it dies on first
    use.  Nothing serializable ever represents it.
    """

    __slots__ = ("_live", "_supervisor")

    def __init__(self, supervisor: "Supervisor") -> None:
        self._live = True
        self._supervisor = supervisor


@dataclass(frozen=True)
class ChildResult:
    returncode: int
    exec_failed: bool
    metadata: dict


class Supervisor:
    """One-shot controllerless EBS orchestrator for a single attempt."""

    def __init__(self, binding, store: AccountingStore) -> None:
        if not isinstance(store, AccountingStore):
            raise LaunchError("SUPERVISOR_REQUIRES_ACCOUNTING_STORE")
        self._binding = binding
        self._store = store
        self._machine = StateMachine(store.last_state or PREPARED)
        self._launcher_fd = None

    @property
    def state(self) -> str:
        return self._machine.state

    @property
    def store(self) -> AccountingStore:
        return self._store

    @property
    def launcher_fd(self):
        return self._launcher_fd

    @classmethod
    def attach(cls, binding, accounting_root) -> "Supervisor":
        store = AccountingStore.attach(accounting_root, binding.attempt_id,
                                       binding.digest)
        return cls(binding, store)

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
        """Durable atomic consumption BEFORE any exec path exists."""
        if self._machine.state != GATES_PASSED:
            raise LaunchError(
                f"CONSUME_REFUSED_STATE_{self._machine.state}: gates must "
                "pass first")
        if self._launcher_fd is None:
            raise LaunchError("CONSUME_REFUSED_NO_VERIFIED_LAUNCHER")
        self._store.append(CONSUMED_PRE_EXEC)   # fsync'd inside append
        self._machine.transition(CONSUMED_PRE_EXEC)
        return LaunchGrant(self)

    def execute(self, grant: LaunchGrant, custody: CredentialCustody,
                argv_tail=(), env: dict = None) -> ChildResult:
        if not isinstance(grant, LaunchGrant) or not grant._live:
            raise LaunchError("LAUNCH_REFUSED_GRANT_NOT_LIVE")
        if not isinstance(custody, CredentialCustody) or custody._closed:
            raise LaunchError("LAUNCH_REFUSED_NO_CUSTODY")
        if self._machine.state != CONSUMED_PRE_EXEC:
            raise LaunchError(
                f"LAUNCH_REFUSED_STATE_{self._machine.state}")
        if self._launcher_fd is None:
            raise LaunchError("LAUNCH_REFUSED_NO_LAUNCHER_FD")
        grant._live = False   # single use begins; no second attempt exists
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
            pid = os.fork()
        except OSError as exc:
            for fd in (md_r, md_w, fail_r, fail_w, devnull):
                os.close(fd)
            raise LaunchError(f"FORK_FAILED: {exc!r}") from exc
        if pid == 0:
            _child_setup(self._launcher_fd, md_w, fail_w, devnull,
                         custody.fd, argv, child_env)
        os.close(md_w)
        os.close(fail_w)
        os.close(devnull)
        fail_byte = b""
        metadata_raw = b""
        try:
            self._store.append(EXEC_ATTEMPTED, extra={"child_pid": pid})
            self._machine.transition(EXEC_ATTEMPTED)
            fail_byte = os.read(fail_r, 1)
            os.close(fail_r)
            fail_r = -1
            _, status = os.waitpid(pid, 0)
            while len(metadata_raw) < METADATA_MAX:
                chunk = os.read(md_r, 65536)
                if not chunk:
                    break
                metadata_raw += chunk
        finally:
            for fd in (md_r, fail_r):
                if fd >= 0:
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
        """Generic report custody + leak screen; records the outcome and
        finishes the attempt (one-shot process exits after TERMINAL)."""
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
