"""Authority-state sealing — kernel capability + fail-closed policy (IR-001
supporting mechanics, remediation §6).

The four-seal representation (F_SEAL_WRITE|GROW|SHRINK|SEAL) is MANDATED for
authority-critical sealed state; when the host cannot produce it, the strict
mode must FAIL CLOSED (never silently downgrade).  These tests establish the
demonstrated host's actual capability and the fail-closed behavior."""
from __future__ import annotations

import fcntl
import os

import pytest

from conftest import HARNESS_ROOT

F_ADD_SEALS = 1033
F_GET_SEALS = 1034
ALL_FOUR_SEALS = 0x0008 | 0x0010 | 0x0020 | 0x0040


def test_kernel_seal_capability_is_characterized():
    """OBSERVED host fact, recorded either way (never silently assumed):
    can a POPULATED memfd carry all four seals on this host class?"""
    from qh.rootauth import memfd_seal_capability
    cap = memfd_seal_capability()
    assert cap in ("sealed", "unavailable_kernel")
    # The capability probe must be internally consistent with a live attempt.
    fd = None
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    libc.memfd_create.restype = ctypes.c_int
    libc.memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
    fd = libc.memfd_create(b"cap-probe", 0x0001 | 0x0004)
    try:
        os.write(fd, b"x")
        populated = True
    except OSError:
        populated = False
    if populated:
        try:
            fcntl.fcntl(fd, F_ADD_SEALS, ALL_FOUR_SEALS)
            sealed = True
        except OSError:
            sealed = False
        assert cap == ("sealed" if sealed else "unavailable_kernel")
    else:
        # Cannot even populate an ALLOW_SEALING memfd: seals unavailable.
        assert cap == "unavailable_kernel"
    if fd is not None and fd >= 0:
        os.close(fd)


def test_strict_mode_fails_closed_without_four_seals(monkeypatch):
    """STRICT authority-state policy: root initialization MUST fail closed
    when the four-seal representation cannot be established — the boundary is
    never silently downgraded (remediation §6)."""
    from qh import rootauth
    cap = rootauth.memfd_seal_capability()
    if cap == "unavailable_kernel":
        with pytest.raises(rootauth.RootInitError) as exc:
            rootauth.hold_authority_bytes(
                b"authority-critical-bytes", name="strict-probe",
                require_seals=True)
        assert "SEALED_REPRESENTATION_UNAVAILABLE" in str(exc.value)
    else:
        fd, status = rootauth.hold_authority_bytes(
            b"authority-critical-bytes", name="strict-probe",
            require_seals=True)
        assert status == "sealed"
        os.close(fd)


def test_default_hold_records_status_and_is_memory_only():
    """Default (G-1 demonstrated posture): authority bytes live ONLY in a
    process-bound anonymous memfd — never a file — with the seal outcome
    RECORDED, and the bytes readable back only through the fd."""
    from qh.rootauth import hold_authority_bytes
    data = b"SYNTHETIC-AUTHORITY-HOLD-probe"
    fd, status = hold_authority_bytes(data, name="hold-probe")
    assert status in ("sealed", "unavailable_kernel")
    st = os.fstat(fd)
    assert st.st_size == len(data)
    os.lseek(fd, 0, os.SEEK_SET)
    assert os.read(fd, len(data)) == data
    # anonymous memfd: no ordinary filesystem path
    link = os.readlink(f"/proc/self/fd/{fd}")
    assert link.startswith("/memfd:")
    os.close(fd)


def test_root_cli_strict_seal_flag_fails_closed_on_this_host(tmp_path):
    """`qh root --require-seals` must fail closed at initialization when the
    host cannot seal (this demonstrated host class)."""
    from qh.rootauth import memfd_seal_capability
    if memfd_seal_capability() != "unavailable_kernel":
        pytest.skip("host can seal; strict flag succeeds there")
    import subprocess, sys, json
    spec_path = tmp_path / "spec.json"
    spec_path.write_text("{}")
    r, w = os.pipe()
    os.write(w, b"{}\n")
    os.close(w)
    cred_r, cred_w = os.pipe()
    os.write(cred_w, b"SYNTHETIC-INERT")
    os.close(cred_w)
    proc = subprocess.run(
        [sys.executable, "-m", "qh.cli", "root",
         "--operator-state", str(tmp_path / "op"),
         "--custody-fd", str(cred_r), "--require-seals"],
        pass_fds=(r, cred_r), stdin=r, capture_output=True, text=True,
        timeout=30, cwd=str(HARNESS_ROOT),
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
    os.close(r)
    os.close(cred_r)
    assert proc.returncode != 0
    assert "SEALED_REPRESENTATION_UNAVAILABLE" in (proc.stderr + proc.stdout)
