"""Operator-custodied durable attempt accounting (hash-chained JSONL).

The accounting record is NOT launch authority and can NEVER reconstruct
it (adopted R1: controllerless / process-bound / one-shot / no revival).
A writable store exists ONLY via `create` in the ONE authority process
for an attempt; an existing same-attempt record makes `create` fail
closed (O_EXCL), so no second EBS process can obtain authority for the
same attempt.  Historical records are inspectable READ-ONLY via
`inspect_accounting_record` (a view with no file descriptor, no append
path, no resumable state).  The record provides durable crash/restart
evidence, mechanically checked tamper semantics, and the complete
non-secret binding identity set at CONSUMED_PRE_EXEC.  Narrow claim: no
audited-target/boundary-child mutation path exists; no protection
against operator/root rewrite is claimed.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import time

from .statemachine import PREPARED, TRANSITIONS, valid_path

GENESIS = "0" * 64
RECORD_MODE = 0o600
ATTEMPT_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


class AccountingError(RuntimeError):
    """Refused accounting operation (fail closed)."""


class UnsafeStore(AccountingError):
    """Custody directory or record fails the safety validation."""


class TamperRefused(AccountingError):
    """Record history is malformed, truncated, or hash-inconsistent."""


def open_custody_dir(path) -> int:
    """Open an operator-custodied directory (no symlink following) and
    enforce same-uid ownership plus restrictive mode."""
    try:
        fd = os.open(os.fspath(path), os.O_RDONLY | os.O_DIRECTORY
                     | os.O_NOFOLLOW)
    except OSError as exc:
        raise UnsafeStore(f"CUSTODY_DIR_UNOPENABLE: {exc!r}") from exc
    try:
        st = os.fstat(fd)
        if not stat.S_ISDIR(st.st_mode):
            raise UnsafeStore("CUSTODY_DIR_NOT_A_DIRECTORY")
        if st.st_uid != os.geteuid():
            raise UnsafeStore("CUSTODY_DIR_NOT_OWNER_UID")
        if st.st_mode & 0o022:
            raise UnsafeStore(
                f"CUSTODY_DIR_GROUP_OR_WORLD_WRITABLE: "
                f"{stat.S_IMODE(st.st_mode):o}")
    except Exception:
        os.close(fd)
        raise
    return fd


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


class AccountingStore:
    """One append-only attempt record file inside an operator-custodied
    directory.  Every append is fsync'd (file, then directory)."""

    def __init__(self, dir_fd: int, file_fd: int, records, digests,
                 attempt_id: str, binding_digest: str) -> None:
        self._dir_fd = dir_fd
        self._file_fd = file_fd
        self._records = list(records)
        self._digests = list(digests)
        self._attempt_id = attempt_id
        self._binding_digest = binding_digest

    @property
    def attempt_id(self) -> str:
        return self._attempt_id

    @property
    def last_state(self):
        return self._records[-1]["state"] if self._records else None

    @property
    def binding_digest(self) -> str:
        return self._binding_digest

    @classmethod
    def create(cls, root, attempt_id: str, binding_digest: str,
               first_state: str = PREPARED) -> "AccountingStore":
        if not ATTEMPT_NAME_RE.match(str(attempt_id)):
            raise AccountingError(f"ATTEMPT_ID_UNSAFE_NAME: {attempt_id!r}")
        if not binding_digest or not isinstance(binding_digest, str):
            raise AccountingError("BINDING_DIGEST_REQUIRED")
        dir_fd = open_custody_dir(root)
        name = f"{attempt_id}.jsonl"
        try:
            file_fd = os.open(name,
                              os.O_WRONLY | os.O_APPEND | os.O_CREAT
                              | os.O_EXCL | os.O_NOFOLLOW,
                              RECORD_MODE, dir_fd=dir_fd)
        except OSError as exc:
            os.close(dir_fd)
            raise AccountingError(
                f"RECORD_CREATE_REFUSED (duplicate attempt?): "
                f"{exc!r}") from exc
        mode = stat.S_IMODE(os.fstat(file_fd).st_mode)
        if mode & 0o077 or not mode & 0o600:
            os.close(file_fd)
            os.close(dir_fd)
            raise UnsafeStore(f"RECORD_MODE_UNSAFE: {mode:o}")
        store = cls(dir_fd, file_fd, [], [], attempt_id, binding_digest)
        store.append(first_state)
        return store

    def append(self, state: str, extra: dict = None) -> dict:
        if self._records:
            if state not in TRANSITIONS[self._records[-1]["state"]]:
                raise AccountingError(
                    f"ILLEGAL_STATE_SEQUENCE "
                    f"{self._records[-1]['state']} -> {state}")
            prev = self._digests[-1]
        elif state != PREPARED:
            raise AccountingError("FIRST_RECORD_MUST_BE_PREPARED")
        else:
            prev = GENESIS
        record = {
            "seq": len(self._records) + 1,
            "state": state,
            "binding_digest": self._binding_digest,
            "prev": prev,
            "ts": int(time.time()),
            "pid": os.getpid(),
        }
        if extra:
            for key, value in extra.items():
                if not isinstance(value, (str, int, float, bool)) or None:
                    raise AccountingError(
                        f"RECORD_EXTRA_NOT_SCALAR: {key}")
                record[key] = value
        line = _canonical(record).encode() + b"\n"
        view = memoryview(line)
        while view:
            written = os.write(self._file_fd, view)
            view = view[written:]
        os.fsync(self._file_fd)     # file durable...
        os.fsync(self._dir_fd)      # ...then directory metadata durable
        self._records.append(record)
        self._digests.append(hashlib.sha256(line.rstrip(b"\n")).hexdigest())
        return dict(record)

    def close(self) -> None:
        for fd in (self._file_fd, self._dir_fd):
            if fd is not None and fd >= 0:
                try:
                    os.close(fd)
                except OSError:
                    pass
        self._file_fd = self._dir_fd = -1


def inspect_accounting_record(root, attempt_id: str,
                              binding_digest: str) -> dict:
    """Open, fully validate, return a READ-ONLY summary dict (keys:
    attempt_id, binding_digest, records, states, last_state) of one
    historical record.  Inspection only: nothing is opened for write, no
    AccountingStore is returned, no state — including PREPARED or
    GATES_PASSED — becomes resumable or revivable by it."""
    if not ATTEMPT_NAME_RE.match(str(attempt_id)):
        raise AccountingError(f"ATTEMPT_ID_UNSAFE_NAME: {attempt_id!r}")
    dir_fd = open_custody_dir(root)
    name = f"{attempt_id}.jsonl"
    try:
        try:
            st = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
        except FileNotFoundError as exc:
            raise AccountingError("RECORD_ABSENT") from exc
        if stat.S_ISLNK(st.st_mode):
            raise AccountingError("RECORD_IS_SYMLINK")
        if not stat.S_ISREG(st.st_mode):
            raise AccountingError("RECORD_NOT_REGULAR")
        if stat.S_IMODE(st.st_mode) & 0o077:
            raise UnsafeStore("RECORD_MODE_UNSAFE")
        read_fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
    except OSError as exc:
        os.close(dir_fd)
        raise AccountingError(f"RECORD_OPEN_REFUSED: {exc!r}") from exc
    try:
        data = b""
        while True:
            chunk = os.read(read_fd, 65536)
            if not chunk:
                break
            data += chunk
    finally:
        os.close(read_fd)
        os.close(dir_fd)
    if not data:
        raise TamperRefused("RECORD_EMPTY")
    if not data.endswith(b"\n"):
        raise TamperRefused("RECORD_TRUNCATED")

    records, states = [], []
    prev = GENESIS
    for index, line in enumerate(data.splitlines(), start=1):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TamperRefused(f"RECORD_LINE_{index}_MALFORMED") from exc
        if not isinstance(rec, dict) or _canonical(rec).encode() != line:
            raise TamperRefused(f"RECORD_LINE_{index}_NOT_CANONICAL")
        if rec.get("seq") != index:
            raise TamperRefused(f"RECORD_SEQ_MISMATCH_AT_{index}")
        if rec.get("prev") != prev:
            raise TamperRefused(f"RECORD_CHAIN_MISMATCH_AT_{index}")
        if rec.get("binding_digest") != binding_digest:
            raise AccountingError(f"RECORD_BINDING_MISMATCH_AT_{index}")
        records.append(rec)
        states.append(rec.get("state"))
        prev = hashlib.sha256(line).hexdigest()
    if not valid_path(states):
        raise TamperRefused(
            f"RECORD_STATE_SEQUENCE_ILLEGAL: {states}")
    return {"attempt_id": attempt_id, "binding_digest": binding_digest,
            "records": records, "states": states,
            "last_state": states[-1] if states else None}
