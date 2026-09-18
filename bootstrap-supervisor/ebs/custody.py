"""Credential custody: source discipline, non-dumpable ingestion, sealed
memfd hold, and boolean-only screening.

Plaintext sources accepted: operator-controlled PIPE or FULLY sealed memfd.
Ordinary files, directories, sockets, and unsealed/partially sealed memfds
are refused.  The EBS makes itself non-dumpable BEFORE reading plaintext,
copies the bytes into a new EBS-owned memfd sealed with the mandatory
four-seal set, and retains ONLY the role label and byte length as
metadata.  Plaintext is never printed, logged, or hashed into evidence.

Numeric Linux UAPI constants, defined exactly once, sourced from
include/uapi/linux/fcntl.h (stable since Linux 3.17):
    F_ADD_SEALS = 1024 + 9  = 1033
    F_GET_SEALS = 1024 + 10 = 1034
    F_SEAL_SEAL = 0x01, F_SEAL_SHRINK = 0x02,
    F_SEAL_GROW = 0x04, F_SEAL_WRITE = 0x08
Actual kernel seal behavior is verified at runtime via F_GET_SEALS and by
the deterministic tests; the historical wrong-UAPI-constant failure is
deliberately not repeated.
"""
from __future__ import annotations

import ctypes
import fcntl
import os
import platform
import stat

PR_GET_DUMPABLE = 3
PR_SET_DUMPABLE = 4

F_ADD_SEALS = 1033
F_GET_SEALS = 1034
F_SEAL_SEAL = 0x01
F_SEAL_SHRINK = 0x02
F_SEAL_GROW = 0x04
F_SEAL_WRITE = 0x08
REQUIRED_SEALS = F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE

# memfd_create(2) UAPI (include/uapi/linux/memfd.h): flags and per-arch
# syscall numbers.  Not exposed by the Python 3.11 os module, so the raw
# syscall is used; actual kernel behavior (seals via F_GET_SEALS) is
# verified at runtime and by tests.
MFD_CLOEXEC = 0x01
MFD_ALLOW_SEALING = 0x02
SYS_MEMFD_CREATE = {"x86_64": 319, "aarch64": 279}

MAX_CREDENTIAL_BYTES = 65536
MIN_CREDENTIAL_BYTES = 1
READ_CHUNK = 4096


class CustodyError(RuntimeError):
    """Fail-closed custody failure (no downgrade path)."""


def _prctl(option: int, arg2: int = 0) -> int:
    libc = ctypes.CDLL(None, use_errno=True)
    result = libc.prctl(ctypes.c_int(option), ctypes.c_ulong(arg2),
                        ctypes.c_ulong(0), ctypes.c_ulong(0),
                        ctypes.c_ulong(0))
    if result == -1:
        err = ctypes.get_errno()
        raise CustodyError(
            f"PRCTL_{option}_FAILED: {os.strerror(err)}")
    return result


def get_dumpable() -> int:
    """Kernel-observable dumpable state (PR_GET_DUMPABLE)."""
    return _prctl(PR_GET_DUMPABLE)


def establish_non_dumpable() -> None:
    """Set PR_SET_DUMPABLE=0 and verify via PR_GET_DUMPABLE; mandatory
    before any credential plaintext is read."""
    _prctl(PR_SET_DUMPABLE, 0)
    if get_dumpable() != 0:
        raise CustodyError("NON_DUMPABLE_NOT_ESTABLISHED")


def seals_of(fd: int) -> int:
    try:
        return fcntl.fcntl(fd, F_GET_SEALS)
    except OSError as exc:
        raise CustodyError(f"SEALS_UNREADABLE: {exc!r}") from exc


def memfd_create(name: str, flags: int) -> int:
    """memfd_create(2) via the raw syscall (os.memfd_create is absent on
    the pinned Python); fails closed on unsupported architectures."""
    number = SYS_MEMFD_CREATE.get(platform.machine())
    if number is None:
        raise CustodyError(
            f"MEMFD_CREATE_UNSUPPORTED_ARCH: {platform.machine()}")
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    result = libc.syscall(ctypes.c_long(number),
                          ctypes.c_char_p(name.encode()),
                          ctypes.c_uint(flags))
    if result < 0:
        err = ctypes.get_errno()
        raise CustodyError(
            f"MEMFD_CREATE_FAILED: {os.strerror(err)}")
    return result


def _fd_source_kind(fd: int) -> str:
    st = os.fstat(fd)
    if stat.S_ISFIFO(st.st_mode):
        return "pipe"
    if stat.S_ISREG(st.st_mode):
        target = os.readlink(f"/proc/self/fd/{fd}")
        if target.startswith("/memfd:"):
            return "memfd"
        return "file"
    return "other"


def _read_bounded(fd: int) -> bytes:
    data = b""
    while len(data) <= MAX_CREDENTIAL_BYTES:
        chunk = os.read(fd, READ_CHUNK)
        if not chunk:
            break
        data += chunk
    if not MIN_CREDENTIAL_BYTES <= len(data) <= MAX_CREDENTIAL_BYTES:
        raise CustodyError(f"CUSTODY_SOURCE_LENGTH_INVALID: {len(data)}")
    return data


class CredentialCustody:
    """Sealed in-memory hold for one credential blob.

    Attributes retained: the sealed fd, the role label, the byte length,
    and the observed seal mask.  No plaintext attribute exists; screening
    compares bytes in memory and reports ONLY a boolean.
    """

    __slots__ = ("_fd", "role", "length", "_seal_bits", "_closed")

    def __init__(self, fd: int, role: str, length: int, seal_bits: int):
        self._fd = fd
        self.role = role
        self.length = length
        self._seal_bits = seal_bits
        self._closed = False

    @property
    def fd(self) -> int:
        if self._closed:
            raise CustodyError("CUSTODY_ALREADY_CLOSED")
        return self._fd

    @property
    def seal_bits(self) -> int:
        return self._seal_bits

    @classmethod
    def ingest(cls, source_fd: int, role: str) -> "CredentialCustody":
        """Read a permitted source into sealed custody.  Non-dumpable is
        established BEFORE any read; any failure fails closed."""
        establish_non_dumpable()
        kind = _fd_source_kind(source_fd)
        if kind == "file":
            raise CustodyError(
                "CUSTODY_SOURCE_IS_ORDINARY_FILE: persisted plaintext "
                "is refused")
        if kind == "other":
            raise CustodyError(f"CUSTODY_SOURCE_KIND_UNSUPPORTED: {kind}")
        if kind == "memfd":
            have = seals_of(source_fd)
            if have & REQUIRED_SEALS != REQUIRED_SEALS:
                raise CustodyError(
                    f"CUSTODY_SOURCE_NOT_FULLY_SEALED: 0x{have:04x}")
            os.lseek(source_fd, 0, os.SEEK_SET)  # read from the start
        data = _read_bounded(source_fd)
        if kind == "pipe":
            os.close(source_fd)  # operator channel fully consumed
        try:
            fd = memfd_create(f"ebs-credential-custody-{role}",
                              MFD_CLOEXEC | MFD_ALLOW_SEALING)
        except (AttributeError, OSError) as exc:
            raise CustodyError(f"CUSTODY_MEMFD_UNAVAILABLE: {exc!r}") from exc
        try:
            os.write(fd, data)
            os.lseek(fd, 0, os.SEEK_SET)
            fcntl.fcntl(fd, F_ADD_SEALS, REQUIRED_SEALS)
            bits = seals_of(fd)
            if bits & REQUIRED_SEALS != REQUIRED_SEALS:
                raise CustodyError(
                    f"CUSTODY_SEAL_INCOMPLETE: 0x{bits:04x}")
        except CustodyError:
            os.close(fd)
            raise
        except OSError as exc:
            os.close(fd)
            raise CustodyError(f"CUSTODY_SEAL_FAILED: {exc!r}") from exc
        return cls(fd, role, len(data), bits)

    def contains(self, blob: bytes) -> bool:
        """In-memory screen of arbitrary output bytes against the held
        plaintext; records nothing, returns ONLY a boolean."""
        held = os.pread(self._fd, self.length, 0)
        return held in blob

    def close(self) -> None:
        if not self._closed:
            os.close(self._fd)
            self._closed = True
            self._fd = -1
