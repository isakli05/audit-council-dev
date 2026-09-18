"""Shared mechanical helpers: hashing, canonical JSON, /proc access, redaction."""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj) -> bytes:
    """Deterministic serialization used for every content address in the
    harness (sorted keys, compact separators, UTF-8)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def content_id(obj) -> str:
    return sha256_bytes(canonical_json(obj))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


# ---------------------------------------------------------------- /proc ----

def proc_starttime(pid: int) -> str | None:
    """Field 22 of /proc/<pid>/stat (process start time) — pid-reuse defense.

    Comm may contain spaces/parens; parse after the LAST ')'.
    """
    try:
        with open(f"/proc/{pid}/stat", "rb") as fh:
            data = fh.read().decode("utf-8", "replace")
    except OSError:
        return None
    idx = data.rfind(")")
    if idx < 0:
        return None
    fields = data[idx + 1:].split()
    # fields[0] is state (field 3); starttime is field 22 -> index 19
    if len(fields) < 20:
        return None
    return fields[19]


def proc_environ(pid: int) -> dict[str, str] | None:
    """Initial environment of a live process (immutable after exec)."""
    try:
        with open(f"/proc/{pid}/environ", "rb") as fh:
            raw = fh.read()
    except OSError:
        return None
    env: dict[str, str] = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        k, _, v = item.partition(b"=")
        env[k.decode("utf-8", "replace")] = v.decode("utf-8", "replace")
    return env


def proc_exe(pid: int) -> str | None:
    try:
        return os.path.realpath(f"/proc/{pid}/exe")
    except OSError:
        return None


def read_yama_ptrace_scope() -> int | None:
    """Yama ptrace_scope value, None when the knob is absent."""
    try:
        with open("/proc/sys/kernel/yama/ptrace_scope") as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return None


# -------------------------------------------------------------- redaction --

class Redactor:
    """Registry of secret VALUES that must never appear in any harness log,
    report, ledger or artifact.  Every synthetic credential registers here;
    ``scrub`` replaces occurrences with a label.  Only the label/length ever
    reach output — never the value and never a hash of it."""

    def __init__(self) -> None:
        self._secrets: dict[str, str] = {}

    def register(self, value: str, label: str) -> None:
        if value:
            self._secrets[value] = label

    def scrub(self, text: str) -> str:
        for value, label in self._secrets.items():
            text = text.replace(value, f"<REDACTED:{label}>")
        return text

    def contains_any(self, text: str) -> str | None:
        for value in self._secrets:
            if value in text:
                return value
        return None

    def known_labels(self) -> list[str]:
        return sorted(self._secrets.values())


def assert_no_secrets(text: str, redactor: Redactor, what: str) -> None:
    hit = redactor.contains_any(text)
    if hit is not None:
        raise AssertionError(
            f"secret material present in {what} (registered value matched); "
            "harness contract forbids credential values in any output")


_SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def safe_token(name: str) -> bool:
    return bool(_SAFE_NAME.match(name))


# ------------------------------------------------------- memfd + seals ----
# Authority-state holding (CR-REMED-001 corrected).  The ONE canonical
# constant set for the whole harness lives HERE (custody and every other
# module import these — no duplicate definitions anywhere).
#
# Authoritative values are the Linux UAPI definitions
# (usr/include/linux/memfd.h, usr/include/linux/fcntl.h):
#
#   MFD_CLOEXEC       = 0x0001      F_SEAL_SEAL     = 0x0001
#   MFD_ALLOW_SEALING = 0x0002      F_SEAL_SHRINK   = 0x0002
#   MFD_HUGETLB       = 0x0004      F_SEAL_GROW     = 0x0004
#                                   F_SEAL_WRITE    = 0x0008
#
# The historical defect (source 0x0004 as MFD_ALLOW_SEALING — actually
# MFD_HUGETLB — and seal values 0x0010/0x0020/0x0040) is corrected here;
# tests/test_seal_uapi.py pins these to the UAPI values deterministically
# and re-establishes the REAL host capability with this corrected API.
#
# Platform constants are preferred where Python exposes them (os.MFD_*
# exist on Linux since 3.8); the fallback numerics are exactly the UAPI
# values above and are asserted equal to os.* whenever available.

MFD_CLOEXEC: int = getattr(os, "MFD_CLOEXEC", 0x0001)
MFD_ALLOW_SEALING: int = getattr(os, "MFD_ALLOW_SEALING", 0x0002)
F_ADD_SEALS = 1033          # F_LINUX_SPECIFIC_BASE(1024) + 9
F_GET_SEALS = 1034          # F_LINUX_SPECIFIC_BASE(1024) + 10
F_SEAL_SEAL = 0x0001
F_SEAL_SHRINK = 0x0002
F_SEAL_GROW = 0x0004
F_SEAL_WRITE = 0x0008
REQUIRED_SEALS = F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE

_seal_capability: str | None = None


class SealUnavailableError(RuntimeError):
    """Authority-critical seal failure: the required four-seal
    representation could not be established (fail closed — never
    downgrade silently)."""


def memfd_create(name: str, flags: int) -> int:
    """memfd_create(2): prefer the authoritative stdlib binding, then the
    libc symbol, then the raw syscall (x86_64/aarch64)."""
    if hasattr(os, "memfd_create"):
        return os.memfd_create(name, flags)
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    if hasattr(libc, "memfd_create"):
        fn = libc.memfd_create
        fn.restype = ctypes.c_int
        fn.argtypes = [ctypes.c_char_p, ctypes.c_uint]
        fd = fn(name.encode(), flags)
        if fd < 0:
            e = ctypes.get_errno()
            raise OSError(e, os.strerror(e))
        return fd
    import platform
    nr = {"x86_64": 319, "aarch64": 279}.get(platform.machine())
    if nr is None:
        raise SealUnavailableError("MEMFD_CREATE_UNAVAILABLE")
    libc.syscall.restype = ctypes.c_long
    fd = libc.syscall(nr, name.encode(), flags)
    if fd < 0:
        e = ctypes.get_errno()
        raise OSError(e, os.strerror(e))
    return fd


def _apply_seals(fd: int) -> None:
    """Apply the REQUIRED four-seal set (the one production seal backend).

    Deterministic TEST fault injection monkeypatches exactly this seam to
    a failing function and proves the production callers fail closed; no
    production CLI/input can disable or downgrade it."""
    import fcntl
    fcntl.fcntl(fd, F_ADD_SEALS, REQUIRED_SEALS)


def memfd_seals(fd: int) -> int:
    """Current seal set of a memfd (F_GET_SEALS)."""
    import fcntl
    return fcntl.fcntl(fd, F_GET_SEALS)


def has_required_seals(fd: int) -> bool:
    try:
        return memfd_seals(fd) & REQUIRED_SEALS == REQUIRED_SEALS
    except (OSError, ValueError):
        return False


def memfd_seal_capability() -> str:
    """Recompute whether a POPULATED memfd can carry all four seals on
    this host ("sealed" / "unavailable_kernel") using the CORRECT UAPI
    API: create with MFD_CLOEXEC|MFD_ALLOW_SEALING, write, apply the four
    seals, F_GET_SEALS must contain every required bit, and a post-seal
    write must be REFUSED.  The historical `unavailable_kernel` conclusion
    (an artifact of the MFD_HUGETLB misidentification) is never carried
    forward — it is recomputed from this corrected implementation."""
    global _seal_capability
    if _seal_capability is not None:
        return _seal_capability
    try:
        fd = memfd_create("qh-seal-capability-probe",
                          MFD_CLOEXEC | MFD_ALLOW_SEALING)
    except (OSError, SealUnavailableError):
        _seal_capability = "unavailable_kernel"
        return _seal_capability
    try:
        try:
            os.write(fd, b"probe")
        except OSError:
            _seal_capability = "unavailable_kernel"
            return _seal_capability
        try:
            _apply_seals(fd)
            seals = memfd_seals(fd)
            if seals & REQUIRED_SEALS != REQUIRED_SEALS:
                _seal_capability = "unavailable_kernel"
                return _seal_capability
            os.lseek(fd, 0, os.SEEK_SET)
            try:
                os.write(fd, b"x")
                _seal_capability = "unavailable_kernel"  # not enforced!
                return _seal_capability
            except OSError:
                pass  # EPERM — exactly the required refusal
            _seal_capability = "sealed"
        except (OSError, ValueError):
            _seal_capability = "unavailable_kernel"
        return _seal_capability
    finally:
        os.close(fd)


def hold_bytes_memfd(data: bytes, *, name: str) -> tuple[int, str]:
    """Hold bytes in an anonymous process-bound memfd, MANDATORILY sealed
    with the four required seals.  Authority-critical sealing is never
    optional and never downgraded: when the required sealed representation
    cannot be established the caller FAILS CLOSED
    (SealUnavailableError).  Returns (fd, "sealed")."""
    cap = memfd_seal_capability()
    if cap != "sealed":
        raise SealUnavailableError(
            "AUTHORITY_CRITICAL_SEALING_UNAVAILABLE: the required "
            "F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE "
            "representation cannot be established on this host (probed "
            "with the corrected Linux UAPI API); authority-critical "
            "state is never held unsealed")
    fd = memfd_create(name, MFD_CLOEXEC | MFD_ALLOW_SEALING)
    try:
        os.write(fd, data)
        _apply_seals(fd)
        seals = memfd_seals(fd)
        if seals & REQUIRED_SEALS != REQUIRED_SEALS:
            raise SealUnavailableError(
                "AUTHORITY_CRITICAL_SEALING_INCOMPLETE: "
                f"F_GET_SEALS=0x{seals:04x}")
        os.lseek(fd, 0, os.SEEK_SET)
        return fd, "sealed"
    except SealUnavailableError:
        os.close(fd)
        raise
    except OSError as exc:
        try:
            os.close(fd)
        except OSError:
            pass
        raise SealUnavailableError(
            f"AUTHORITY_CRITICAL_SEALING_FAILED:{exc!r}") from exc


# ------------------------------------------------- fd source discrimination --

def fd_source_kind(fd: int) -> str:
    """Robust Linux-specific classification of an fd's backing object:
    "pipe" | "memfd" | "file" (ordinary regular file, incl. tmpfs) |
    "other".

    memfds are discriminated by their /proc/self/fd link target
    ("/memfd:<name>") — an anonymous in-memory object with NO ordinary
    filesystem path.  fcntl(F_GET_SEALS) is deliberately NOT used for
    classification: on some kernel classes it returns a value even for
    ordinary files (observed mechanically), so it can never prove an fd
    is a memfd."""
    import stat
    st = os.fstat(fd)
    if stat.S_ISFIFO(st.st_mode):
        return "pipe"
    if stat.S_ISREG(st.st_mode):
        try:
            target = os.readlink(f"/proc/self/fd/{fd}")
        except OSError:
            return "file"
        return "memfd" if target.startswith("/memfd:") else "file"
    return "other"


def require_trusted_spec_fd(fd: int) -> str:
    """CR-REMED-003: the production trusted-spec input channel must be an
    operator-held capability — a PIPE, or a mechanically identified memfd
    carrying the COMPLETE required seal set.  Ordinary regular files
    (including stdin redirected from a file) are refused."""
    kind = fd_source_kind(fd)
    if kind == "pipe":
        return "pipe"
    if kind == "memfd":
        seals = memfd_seals(fd)
        if seals & REQUIRED_SEALS != REQUIRED_SEALS:
            raise SealUnavailableError(
                f"SPEC_MEMFD_SEALS_INCOMPLETE: F_GET_SEALS=0x{seals:04x} "
                f"does not carry the required 0x{REQUIRED_SEALS:04x}")
        return "sealed-memfd"
    raise SealUnavailableError(f"SPEC_SOURCE_KIND_REFUSED:{kind}")
