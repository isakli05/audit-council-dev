"""Authority-state sealing — corrected characterization (CR-REMED-001).

The four-seal representation (F_SEAL_SEAL|SHRINK|GROW|WRITE — the CORRECT
Linux UAPI values, centralized in qh/util.py) is MANDATORY for
authority-critical sealed state: the root fails closed when it cannot be
established and there is no optional downgrade flag anywhere.

The UAPI-constant pins, the real host capability proof (write → seal →
F_GET_SEALS → post-seal write/grow/shrink refusals), the failing-backend
fail-closed proofs and the fd type discrimination live in
tests/test_seal_uapi.py; this module characterizes the ROOT posture."""
from __future__ import annotations

import fcntl
import os

import pytest

from conftest import HARNESS_ROOT


def test_kernel_seal_capability_is_characterized():
    """OBSERVED host fact via the CORRECTED probe (never silently assumed,
    never carried forward from the invalid-constant era): on this host
    class a POPULATED memfd carries all four seals."""
    from qh.rootauth import memfd_seal_capability
    cap = memfd_seal_capability()
    assert cap in ("sealed", "unavailable_kernel")
    # live cross-check with the authoritative UAPI values
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    libc.memfd_create.restype = ctypes.c_int
    libc.memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
    fd = libc.memfd_create(b"cap-probe", 0x0001 | 0x0002)  # CLOEXEC|ALLOW
    try:
        os.write(fd, b"x")
        fcntl.fcntl(fd, 1033, 0x000F)  # the four required seals
        seals = fcntl.fcntl(fd, 1034)
        assert (seals & 0x000F) == 0x000F
        assert cap == "sealed"
    finally:
        os.close(fd)


def test_authority_hold_is_sealed_and_memory_only():
    """Authority bytes live ONLY in a process-bound, MANDATORILY SEALED
    anonymous memfd — never a file — with the bytes readable back only
    through the fd."""
    from qh.rootauth import hold_authority_bytes
    data = b"SYNTHETIC-AUTHORITY-HOLD-probe"
    fd, status = hold_authority_bytes(data, name="hold-probe")
    try:
        assert status == "sealed"
        st = os.fstat(fd)
        assert st.st_size == len(data)
        os.lseek(fd, 0, os.SEEK_SET)
        assert os.read(fd, len(data)) == data
        link = os.readlink(f"/proc/self/fd/{fd}")
        assert link.startswith("/memfd:")
    finally:
        os.close(fd)


def test_root_startup_records_sealed_custody(env):
    """The production root startup (subprocess) MANDATORILY seals the
    authority-critical state: the observability ledger records
    seal_status=sealed for both the spec bytes and the custody hold."""
    env.author_spec("seal-root-0001")
    root = env.spawn_root()
    try:
        recs = env.ledger_records()
        assert any(r["event"] == "SPEC_BYTES_SEALED"
                   and r["seal_status"] == "sealed" for r in recs)
        assert any(r["event"] == "ROOT_CUSTODY_ESTABLISHED"
                   and r["seal_status"] == "sealed" for r in recs)
        assert not any(r.get("seal_status") == "unavailable_kernel"
                       for r in recs)
    finally:
        env.cleanup_procs()
    env.root_outcome(root, timeout=60)
