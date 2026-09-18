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
# Authority-state holding (IR-001 remediation).  The four-seal
# representation is REQUIRED in strict mode and callers fail closed when
# the host cannot produce it; the default posture keeps bytes in an
# anonymous process-bound memfd with the seal outcome RECORDED (the
# demonstrated G-1 mechanism on hosts where the sealed representation is
# unavailable — never a silent downgrade).

F_ADD_SEALS = 1033
F_GET_SEALS = 1034
F_SEAL_WRITE = 0x0008
F_SEAL_GROW = 0x0010
F_SEAL_SHRINK = 0x0020
F_SEAL_SEAL = 0x0040
_ALL_FOUR_SEALS = F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL
MFD_CLOEXEC = 0x0001
MFD_ALLOW_SEALING = 0x0004

_seal_capability: str | None = None


class SealUnavailableError(RuntimeError):
    """Strict-mode authority hold: the four-seal representation is
    unavailable on this host (fail closed — never downgrade silently)."""


def memfd_create(name: str, flags: int) -> int:
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
    raise SealUnavailableError("MEMFD_CREATE_UNAVAILABLE")


def memfd_seal_capability() -> str:
    """Characterize whether a POPULATED memfd can carry all four seals on
    this host ("sealed" / "unavailable_kernel") — recorded, never silently
    assumed either way."""
    global _seal_capability
    if _seal_capability is not None:
        return _seal_capability
    import fcntl
    fd = memfd_create("qh-seal-capability-probe",
                      MFD_CLOEXEC | MFD_ALLOW_SEALING)
    try:
        try:
            os.write(fd, b"probe")
        except OSError:
            _seal_capability = "unavailable_kernel"
            return _seal_capability
        try:
            fcntl.fcntl(fd, F_ADD_SEALS, _ALL_FOUR_SEALS)
            _seal_capability = "sealed"
        except (OSError, ValueError):
            _seal_capability = "unavailable_kernel"
        return _seal_capability
    finally:
        os.close(fd)


def hold_bytes_memfd(data: bytes, *, name: str,
                     require_seals: bool = False) -> tuple[int, str]:
    """Hold bytes in an anonymous process-bound memfd.  Strict mode
    requires all four seals to succeed or raises SealUnavailableError."""
    import fcntl
    cap = memfd_seal_capability()
    if require_seals and cap != "sealed":
        raise SealUnavailableError(
            "SEALED_REPRESENTATION_UNAVAILABLE_ON_THIS_HOST: authority-"
            "critical state requires F_SEAL_WRITE|F_SEAL_GROW|F_SEAL_SHRINK|"
            "F_SEAL_SEAL and the host cannot produce a populated sealed "
            "memfd (strict mode refuses to downgrade the boundary)")
    if cap == "sealed":
        fd = memfd_create(name, MFD_CLOEXEC | MFD_ALLOW_SEALING)
        os.write(fd, data)
        fcntl.fcntl(fd, F_ADD_SEALS, _ALL_FOUR_SEALS)
        status = "sealed"
    else:
        fd = memfd_create(name, MFD_CLOEXEC)
        os.write(fd, data)
        status = "unavailable_kernel"
    os.lseek(fd, 0, os.SEEK_SET)
    return fd, status
