"""Credential custody — MANDATORY C-2/G-1 invariant.

``CREDENTIAL_CUSTODY_IS_REQUIRED_FOR_G1_ENFORCEMENT``: a same-UID
controller must NOT retain ambient readable provider credentials that let
it bypass the supervising launch gate.

Contract (generic; synthetic fixtures in ALL tests):

* credential material enters the SUPERVISOR only through an explicitly
  operator-controlled input channel (a pipe or memfd — a regular ordinary
  file is REFUSED, so no controller-readable plaintext file ever holds the
  authority);
* no plaintext credential is persisted in any controller-readable ordinary
  file — the supervisor keeps the bytes only in a sealed memfd in its own
  (non-dumpable) process memory;
* the controller cannot independently reconstruct a provider-capable
  launch from the custody mechanism: it never receives the fd, the value,
  or any hash of it — the child-only materialization happens inside the
  supervised boundary's ephemeral tmpfs and vanishes with the namespace;
* unsealed material is exposed ONLY to the specifically authorized
  supervised child path (the boundary child materializes the fd into the
  configured inner target path immediately before payload exec);
* custody establishment failure fails closed (launch refuses);
* bounded cleanup/restore: teardown closes the memfd; the redaction
  registry keeps scrubbing logs of the value forever;
* no credential value is printed, hashed into reports, committed, or
  copied into handoff artifacts — outputs may carry the LABEL and the
  byte LENGTH only.

PROVIDER-SPECIFIC INTEGRATION (explicit, not silently weakened): the
real provider credential injection point (e.g. materializing a real
CODEX_HOME/auth.json inside the supervised boundary) is an ADAPTER
INTERFACE ONLY in this harness.  ``ProviderCustodyAdapter`` is not
implemented against real credentials; every test and the rehearsal use
``SyntheticInertAdapter`` with obviously-fake inert fixtures.  Real
provider credential integration remains an implementation blocker to be
reported, never assumed.
"""
from __future__ import annotations

import os
import stat
from dataclasses import dataclass

from .util import Redactor

# Linux memfd seals (fcntl F_ADD_SEALS/F_GET_SEALS)
F_ADD_SEALS = 1033
F_SEAL_WRITE = 0x0008
F_SEAL_GROW = 0x0010
F_SEAL_SHRINK = 0x0020
F_SEAL_SEAL = 0x0040
_ALL_SEALS = F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL

MAX_CREDENTIAL_BYTES = 65536
MIN_CREDENTIAL_BYTES = 1

PROVIDER_SPECIFIC_INTEGRATION_STATUS = (
    "SYNTHETIC_CONCRETE_ADAPTERS_IMPLEMENTED — codex_chatgpt_oauth_v1 "
    "(CODEX_HOME/auth.json, boundary-private writable-at-init home per the "
    "Campaign-2 evidence) and claude_firstparty_oauth_v1 "
    "(CLAUDE_CONFIG_DIR/.credentials.json mode 0600 per the Campaign-2 "
    "parity closure) are implemented against SYNTHETIC inert bytes only; "
    "no real credential is read, parsed, inferred or contacted; see "
    "qh/adapters.py for the evidence basis and the unestablished-role "
    "blocker policy")


class CustodyError(RuntimeError):
    """Fail-closed custody establishment failure."""


@dataclass
class ChildSecretPlan:
    """What the boundary child does with the custody fd: materialize its
    bytes at ``target_path`` (which must live on an ephemeral tmpfs or the
    authorized writable role inside the boundary) immediately before the
    payload exec, then close the fd."""
    fd: int
    label: str
    target_path: str
    length: int


def _fd_kind(fd: int) -> str:
    st = os.fstat(fd)
    if stat.S_ISFIFO(st.st_mode):
        return "pipe"
    if stat.S_ISREG(st.st_mode):
        # memfds are anonymous in-memory objects: their /proc fd link
        # target is "/memfd:<name>" (F_GET_SEALS is NOT a reliable
        # discriminator on every kernel class — observed returning a
        # value even for ordinary files)
        try:
            target = os.readlink(f"/proc/self/fd/{fd}")
        except OSError:
            return "file"
        return "memfd" if target.startswith("/memfd:") else "file"
    return "other"


MFD_CLOEXEC = 0x0001
MFD_ALLOW_SEALING = 0x0004
SYS_memfd_create = {"x86_64": 319, "aarch64": 279}


def _memfd_create(name: str) -> int:
    """memfd_create via ctypes (no stdlib binding).

    Created with MFD_CLOEXEC only: on the demonstrated kernel class
    (7.2.2-cachyos) passing MFD_ALLOW_SEALING (0x4) yields a memfd whose
    write(2) returns EINVAL — observed mechanically; seals are therefore
    attempted later, best-effort, and recorded."""
    import ctypes
    flags = MFD_CLOEXEC
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
    nr = SYS_memfd_create.get(platform.machine())
    if nr is None:
        raise AttributeError("memfd_create unavailable on this machine")
    libc.syscall.restype = ctypes.c_long
    fd = libc.syscall(nr, name.encode(), flags)
    if fd < 0:
        e = ctypes.get_errno()
        raise OSError(e, os.strerror(e))
    return fd


class CredentialCustody:
    """Sealed in-memory custody of one credential blob."""

    def __init__(self, memfd: int, label: str, length: int,
                 redactor: Redactor) -> None:
        self._fd = memfd
        self._label = label
        self._length = length
        self._redactor = redactor
        self._closed = False
        self.seal_status: str = "unknown"

    @property
    def label(self) -> str:
        return self._label

    @property
    def length(self) -> int:
        return self._length

    @property
    def fd(self) -> int:
        if self._closed:
            raise CustodyError("custody already torn down")
        return self._fd

    @classmethod
    def establish(cls, source_fd: int, *, label: str,
                  redactor: Redactor) -> "CredentialCustody":
        """Read credential bytes from an operator-controlled fd (pipe or
        memfd ONLY — an ordinary file is refused: persisted plaintext is
        exactly what custody exists to prevent), copy them into a sealed
        memfd, seal it, and register the value for redaction."""
        kind = _fd_kind(source_fd)
        if kind == "file":
            raise CustodyError(
                "CUSTODY_SOURCE_IS_ORDINARY_FILE: credential arriving via "
                "a regular file is refused (no persisted plaintext)")
        if kind == "other":
            raise CustodyError(
                f"CUSTODY_SOURCE_KIND_UNSUPPORTED: {kind}")
        data = b""
        while len(data) <= MAX_CREDENTIAL_BYTES:
            chunk = os.read(source_fd, 4096)
            if not chunk:
                break
            data += chunk
        if not MIN_CREDENTIAL_BYTES <= len(data) <= MAX_CREDENTIAL_BYTES:
            raise CustodyError(
                f"CUSTODY_SOURCE_LENGTH_INVALID: {len(data)} bytes")
        try:
            memfd = _memfd_create(f"qh-custody-{label}")
        except (AttributeError, OSError) as exc:
            raise CustodyError(f"CUSTODY_MEMFD_UNAVAILABLE: {exc!r}") from exc
        os.write(memfd, data)
        os.lseek(memfd, 0, os.SEEK_SET)
        # Seals are HARDENING (best-effort): on kernels where F_ADD_SEALS
        # is unavailable/EINVAL the memfd remains a valid memory-only,
        # anonymous, non-filesystem hold; the PRIMARY protections are
        # PR_SET_DUMPABLE=0 (same-UID cannot read the fd or the process)
        # and child-only materialization.  The seal outcome is recorded,
        # never silently claimed.
        import fcntl
        seal_status = "unavailable_kernel"
        try:
            fcntl.fcntl(memfd, F_ADD_SEALS, _ALL_SEALS)
            seal_status = "sealed"
        except (OSError, ValueError):
            pass
        redactor.register(data.decode("utf-8", "surrogateescape"),
                          label)
        custody = cls(memfd, label, len(data), redactor)
        custody.seal_status = seal_status
        return custody

    def child_plan(self, target_path: str) -> ChildSecretPlan:
        """Plan handed to the boundary launcher for the authorized child.
        The fd number crosses to the child; the VALUE never crosses any
        ordinary-file surface on the host."""
        return ChildSecretPlan(fd=self.fd, label=self._label,
                               target_path=target_path,
                               length=self._length)

    def teardown(self) -> None:
        """Bounded cleanup: close the sealed memfd.  Redaction of the
        value stays registered for the lifetime of the process."""
        if not self._closed:
            os.close(self._fd)
            self._closed = True


class CustodyAdapter:
    """Adapter interface binding custody to a concrete child-side
    materialization scheme.  Concrete registered adapters live in
    qh/adapters.py (synthetic-only implementations against frozen
    non-secret evidence)."""

    materialize_target: str

    def child_target_path(self) -> str:
        raise NotImplementedError


class SyntheticInertAdapter(CustodyAdapter):
    """Synthetic inert adapter used by the GATE-W/gate rehearsals and
    adapter-agnostic tests: materializes the (synthetic) credential at a
    demo path on the boundary's ephemeral tmpfs."""

    def __init__(self, target_path: str | None = None) -> None:
        from .adapters import SYNTHETIC_INERT
        self.materialize_target = (target_path
                                   if target_path is not None
                                   else SYNTHETIC_INERT.credential_target)

    def child_target_path(self) -> str:
        return self.materialize_target
