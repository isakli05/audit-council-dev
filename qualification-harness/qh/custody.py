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
from dataclasses import dataclass

from . import util as _util
from .util import (MFD_ALLOW_SEALING, MFD_CLOEXEC, REQUIRED_SEALS,
                   Redactor, SealUnavailableError, fd_source_kind,
                   memfd_create)

# Canonical Linux UAPI memfd/seal constants are centralized in qh/util.py
# (CR-REMED-001): this module holds NO numeric seal definitions of its
# own — every name above is the one canonical util definition.

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
    """Canonical fd classification (delegates to util.fd_source_kind —
    pipe/memfd/file/other; memfds discriminated by their /proc/self/fd
    link target, never by an fcntl value)."""
    return fd_source_kind(fd)


def _memfd_create(name: str) -> int:
    """Sealable memfd: created with MFD_CLOEXEC|MFD_ALLOW_SEALING (the
    CORRECT UAPI flags — the historical 0x4 was MFD_HUGETLB, which
    mechanically explains the old populate-EINVAL observations)."""
    return memfd_create(name, MFD_CLOEXEC | MFD_ALLOW_SEALING)


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
        exactly what custody exists to prevent), copy them into a memfd
        and apply the REQUIRED four-seal set — MANDATORY (CR-REMED-001
        corrected semantics): establishment FAILS CLOSED when the sealed
        representation cannot be produced; there is no best-effort
        unsealed hold."""
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
        except (AttributeError, OSError, SealUnavailableError) as exc:
            raise CustodyError(f"CUSTODY_MEMFD_UNAVAILABLE: {exc!r}") from exc
        try:
            os.write(memfd, data)
            os.lseek(memfd, 0, os.SEEK_SET)
            # MANDATORY sealing with the corrected UAPI constants (called
            # through the util module so the ONE seal-backend seam
            # util._apply_seals governs every consumer): the custody
            # representation either carries all four required seals or
            # establishment fails closed.
            _util._apply_seals(memfd)
            seals = _util.memfd_seals(memfd)
            if seals & REQUIRED_SEALS != REQUIRED_SEALS:
                raise CustodyError(
                    f"CUSTODY_SEAL_INCOMPLETE: F_GET_SEALS=0x{seals:04x}")
        except CustodyError:
            try:
                os.close(memfd)
            except OSError:
                pass
            raise
        except (OSError, ValueError, SealUnavailableError) as exc:
            try:
                os.close(memfd)
            except OSError:
                pass
            raise CustodyError(
                f"CUSTODY_SEAL_FAILED: authority-critical credential "
                f"custody requires the four-seal representation and it "
                f"could not be established: {exc!r}") from exc
        redactor.register(data.decode("utf-8", "surrogateescape"),
                          label)
        custody = cls(memfd, label, len(data), redactor)
        custody.seal_status = "sealed"
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
