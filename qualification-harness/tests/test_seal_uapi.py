"""CR-REMED-001 — correct Linux UAPI memfd/seal constants, real host seal
capability, and MANDATORY authority-critical sealing.

The prior constants were invalid (``MFD_ALLOW_SEALING=0x0004`` is actually
``MFD_HUGETLB``; the seal values 0x0010/0x0020/0x0040 are actually
F_SEAL_FUTURE_WRITE / F_SEAL_EXEC / unused).  These tests pin the harness
to the AUTHORITATIVE Linux UAPI values and prove the real host capability
with the corrected API."""
from __future__ import annotations

import errno
import fcntl
import os

import pytest

from conftest import HARNESS_ROOT

# Authoritative Linux UAPI (usr/include/linux/memfd.h, usr/include/linux/fcntl.h)
UAPI_MFD_CLOEXEC = 0x0001
UAPI_MFD_ALLOW_SEALING = 0x0002
UAPI_MFD_HUGETLB = 0x0004
UAPI_F_ADD_SEALS = 1033
UAPI_F_GET_SEALS = 1034
UAPI_F_SEAL_SEAL = 0x0001
UAPI_F_SEAL_SHRINK = 0x0002
UAPI_F_SEAL_GROW = 0x0004
UAPI_F_SEAL_WRITE = 0x0008
UAPI_FOUR_SEALS = (UAPI_F_SEAL_SEAL | UAPI_F_SEAL_SHRINK
                   | UAPI_F_SEAL_GROW | UAPI_F_SEAL_WRITE)


# ---------------------------------------------- constants are UAPI-exact ----

def test_util_constants_equal_authoritative_uapi():
    from qh import util
    assert util.MFD_CLOEXEC == UAPI_MFD_CLOEXEC
    assert util.MFD_ALLOW_SEALING == UAPI_MFD_ALLOW_SEALING
    assert util.MFD_ALLOW_SEALING != UAPI_MFD_HUGETLB
    assert util.F_ADD_SEALS == UAPI_F_ADD_SEALS
    assert util.F_GET_SEALS == UAPI_F_GET_SEALS
    assert util.F_SEAL_SEAL == UAPI_F_SEAL_SEAL
    assert util.F_SEAL_SHRINK == UAPI_F_SEAL_SHRINK
    assert util.F_SEAL_GROW == UAPI_F_SEAL_GROW
    assert util.F_SEAL_WRITE == UAPI_F_SEAL_WRITE
    assert util.REQUIRED_SEALS == UAPI_FOUR_SEALS == 0x000F


def test_platform_os_constants_agree_when_available():
    """Prefer authoritative platform constants: when Python's ``os`` exposes
    the MFD_* flags they MUST agree with the UAPI values (and the harness
    must use them, not contradictory duplicates)."""
    from qh import util
    if hasattr(os, "MFD_CLOEXEC"):
        assert os.MFD_CLOEXEC == UAPI_MFD_CLOEXEC
        assert util.MFD_CLOEXEC == os.MFD_CLOEXEC
    if hasattr(os, "MFD_ALLOW_SEALING"):
        assert os.MFD_ALLOW_SEALING == UAPI_MFD_ALLOW_SEALING
        assert util.MFD_ALLOW_SEALING == os.MFD_ALLOW_SEALING


def test_constants_are_centralized_no_contradictory_duplicates():
    """custody must import the ONE canonical constant set from util — no
    divergent duplicate definitions may exist in custody modules."""
    from qh import custody, util
    assert custody.MFD_CLOEXEC == util.MFD_CLOEXEC
    assert custody.MFD_ALLOW_SEALING == util.MFD_ALLOW_SEALING
    assert custody.REQUIRED_SEALS == util.REQUIRED_SEALS
    src = open(os.path.join(str(HARNESS_ROOT), "qh", "custody.py"),
               encoding="utf-8").read()
    assert "MFD_ALLOW_SEALING = 0x" not in src, \
        "custody.py must not redefine numeric seal constants"
    assert "F_SEAL_WRITE = 0x" not in src


# ------------------------------------- real host capability (correct API) ----

def _libc_memfd(name: bytes, flags: int) -> int:
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    libc.memfd_create.restype = ctypes.c_int
    libc.memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
    fd = libc.memfd_create(name, flags)
    if fd < 0:
        e = ctypes.get_errno()
        raise OSError(e, os.strerror(e))
    return fd


def test_populated_memfd_seals_on_supported_host():
    """The REAL capability test with the corrected API: create with
    MFD_CLOEXEC|MFD_ALLOW_SEALING, write, apply the four seals, read
    F_GET_SEALS, prove all four bits — recording exact results."""
    fd = _libc_memfd(b"uapi-capability-probe",
                     UAPI_MFD_CLOEXEC | UAPI_MFD_ALLOW_SEALING)
    try:
        n = os.write(fd, b"populated-probe")
        assert n > 0
        fcntl.fcntl(fd, UAPI_F_ADD_SEALS, UAPI_FOUR_SEALS)
        seals = fcntl.fcntl(fd, UAPI_F_GET_SEALS)
        assert seals & UAPI_FOUR_SEALS == UAPI_FOUR_SEALS, \
            f"F_GET_SEALS=0x{seals:04x} missing required bits"
    finally:
        os.close(fd)


def test_write_after_sealing_refused():
    fd = _libc_memfd(b"uapi-write-refusal", UAPI_MFD_CLOEXEC
                     | UAPI_MFD_ALLOW_SEALING)
    try:
        os.write(fd, b"sealed-content")
        fcntl.fcntl(fd, UAPI_F_ADD_SEALS, UAPI_FOUR_SEALS)
        os.lseek(fd, 0, os.SEEK_SET)
        with pytest.raises(OSError) as exc:
            os.write(fd, b"x")
        assert exc.value.errno in (errno.EPERM, errno.EACCES), \
            f"unexpected errno {exc.value.errno}"
    finally:
        os.close(fd)


def test_grow_and_shrink_after_sealing_refused():
    fd = _libc_memfd(b"uapi-size-refusal", UAPI_MFD_CLOEXEC
                     | UAPI_MFD_ALLOW_SEALING)
    try:
        os.write(fd, b"0123456789")
        fcntl.fcntl(fd, UAPI_F_ADD_SEALS, UAPI_FOUR_SEALS)
        with pytest.raises(OSError):
            os.ftruncate(fd, 4096)   # grow
        with pytest.raises(OSError):
            os.ftruncate(fd, 4)      # shrink
    finally:
        os.close(fd)


def test_capability_probe_reports_sealed_on_this_host():
    """With the CORRECT constants the historical `unavailable_kernel`
    conclusion must be recomputed: on this host class the four-seal
    populated memfd is mechanically ESTABLISHED."""
    from qh import util
    util._seal_capability = None  # recompute — never carry stale conclusions
    assert util.memfd_seal_capability() == "sealed"


# ------------------------------------------ mandatory sealed authority hold --

def test_hold_bytes_memfd_is_always_sealed():
    """Authority-critical holds are MANDATORILY sealed — there is no
    optional downgrade path; the returned status is `sealed` and the memfd
    refuses further writes."""
    from qh import util
    fd, status = util.hold_bytes_memfd(b"authority-critical", name="t-hold")
    try:
        assert status == "sealed"
        st = os.fstat(fd)
        assert st.st_size == len(b"authority-critical")
        os.lseek(fd, 0, os.SEEK_SET)
        assert os.read(fd, 64) == b"authority-critical"
        seals = fcntl.fcntl(fd, util.F_GET_SEALS)
        assert seals & util.REQUIRED_SEALS == util.REQUIRED_SEALS
        os.lseek(fd, 0, os.SEEK_SET)
        with pytest.raises(OSError):
            os.write(fd, b"tamper")
        link = os.readlink(f"/proc/self/fd/{fd}")
        assert link.startswith("/memfd:")
    finally:
        os.close(fd)


def test_hold_fails_closed_when_seal_backend_fails(monkeypatch):
    """A mechanically separate FAILING seal backend (test injection) proves
    fail-closed behavior: authority-critical bytes are never held unsealed."""
    from qh import util

    def failing_seal(fd: int) -> None:
        raise OSError(errno.EPERM, "TEST SEAM: seal backend failure")

    monkeypatch.setattr(util, "_apply_seals", failing_seal)
    monkeypatch.setattr(util, "_seal_capability", None)
    with pytest.raises(util.SealUnavailableError):
        util.hold_bytes_memfd(b"authority-critical", name="t-fail")


def test_root_authority_hold_fails_closed_on_seal_failure(monkeypatch):
    """The production authority root fails closed when authority-critical
    state cannot be sealed (no optional downgrade; no `--require-seals`)."""
    from qh import rootauth, util

    def failing_seal(fd: int) -> None:
        raise OSError(errno.EPERM, "TEST SEAM: seal backend failure")

    monkeypatch.setattr(util, "_apply_seals", failing_seal)
    monkeypatch.setattr(util, "_seal_capability", None)
    root = rootauth.AuthorityRoot(
        operator_state_dir="/tmp/qh-none-seal-fail", template_bytes=b"{}",
        custody_fd=-1, finalization_fd=-1)
    # startup reaches the seal gate before template parsing is meaningful;
    # a template of {} fails validation anyway, so drive the hold directly
    with pytest.raises(rootauth.RootInitError):
        rootauth.hold_authority_bytes(b"x", name="t-root-fail")


def test_root_cli_has_no_optional_require_seals_flag():
    """The optional `--require-seals` shape is REMOVED: production always
    enforces authority-critical sealing — the CLI must not carry a flag
    that suggests sealing is conditional."""
    from qh import cli
    parser = cli._build_parser()
    for action in parser._actions:
        for opt in action.option_strings:
            assert "require-seals" not in opt, opt
        for sub in (getattr(action, "choices", None) or {}).values():
            for sub_action in sub._actions:
                for opt in sub_action.option_strings:
                    assert "require-seals" not in opt, opt


def test_root_cli_fails_closed_when_seal_backend_fails(tmp_path):
    """Subprocess proof: the PRODUCTION CLI root fails closed (no READY,
    no socket) when the seal backend cannot seal — deterministic failing
    backend injected by a test wrapper process (no production flag)."""
    import subprocess
    import sys
    wrapper = tmp_path / "failing_seal_root.py"
    op_state = tmp_path / "op-state"
    wrapper.write_text(
        "import os, sys, errno\n"
        f"sys.path.insert(0, {str(HARNESS_ROOT)!r})\n"
        "cr, cw = os.pipe(); os.write(cw, b'SYNTHETIC'); os.close(cw)\n"
        "fr, fw = os.pipe(); os.close(fw)\n"
        "from qh import util\n"
        "def failing_seal(fd):\n"
        "    raise OSError(errno.EPERM, 'TEST SEAM: seal backend failure')\n"
        "util._apply_seals = failing_seal\n"
        "from qh import cli\n"
        "rc = cli.main(['authority', '--operator-state', " + repr(str(op_state)) + ", "
        "'--custody-fd', str(cr), '--finalization-fd', str(fr)])\n"
        "os.close(cr); os.close(fr)\n"
        "sys.exit(rc)\n",
        encoding="utf-8")
    r, w = os.pipe()
    os.write(w, b"SYNTHETIC")
    os.close(w)
    spec_r, spec_w = os.pipe()
    os.write(spec_w, b"{}")
    os.close(spec_w)
    proc = subprocess.run(
        [sys.executable, str(wrapper)], pass_fds=(r,), stdin=spec_r,
        capture_output=True, text=True, timeout=60)
    os.close(r)
    os.close(spec_r)
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "READY" not in blob.split("\n")[0]
    assert ("AUTHORITY_CRITICAL_SEAL" in blob
            or "SEALED_REPRESENTATION_UNAVAILABLE" in blob), blob


def test_custody_establish_is_mandatory_sealed():
    """Supervisor-side custody uses the same corrected seal semantics: the
    custody memfd is ALWAYS sealed or establishment fails closed."""
    from qh.custody import CredentialCustody
    from qh.util import Redactor
    r, w = os.pipe()
    os.write(w, b"SYNTHETIC-INERT-CUSTODY-PROBE")
    os.close(w)
    custody = CredentialCustody.establish(r, label="t-cust",
                                          redactor=Redactor())
    try:
        assert custody.seal_status == "sealed"
        seals = fcntl.fcntl(custody.fd, 1034)
        assert seals & 0x000F == 0x000F
    finally:
        custody.teardown()


def test_custody_establish_fails_closed_on_seal_failure(monkeypatch):
    from qh import util
    from qh.custody import CredentialCustody, CustodyError
    from qh.util import Redactor

    def failing_seal(fd: int) -> None:
        raise OSError(errno.EPERM, "TEST SEAM: seal backend failure")

    monkeypatch.setattr(util, "_apply_seals", failing_seal)
    monkeypatch.setattr(util, "_seal_capability", None)
    r, w = os.pipe()
    os.write(w, b"SYNTHETIC-INERT-CUSTODY-PROBE")
    os.close(w)
    with pytest.raises(CustodyError):
        CredentialCustody.establish(r, label="t-cust-fail",
                                    redactor=Redactor())


# ------------------------------------- sealed-memfd type discrimination -----

def test_fd_source_kind_discriminates_pipe_file_memfd(tmp_path):
    from qh.util import fd_source_kind
    r, w = os.pipe()
    try:
        assert fd_source_kind(r) == "pipe"
    finally:
        os.close(r)
        os.close(w)
    f = tmp_path / "ordinary.txt"
    f.write_text("x")
    fd = os.open(f, os.O_RDONLY)
    try:
        assert fd_source_kind(fd) == "file"
    finally:
        os.close(fd)
    # tmpfs regular file is an ORDINARY FILE, not a memfd
    import subprocess
    tdir = "/dev/shm/qh-test-tmpfs-dir"
    os.makedirs(tdir, exist_ok=True)
    tf = os.path.join(tdir, "tmpfs-file.txt")
    with open(tf, "w") as fh:
        fh.write("x")
    fd = os.open(tf, os.O_RDONLY)
    try:
        assert fd_source_kind(fd) == "file"
    finally:
        os.close(fd)
        os.unlink(tf)
    # a directory fd is OTHER
    fd = os.open(str(tmp_path), os.O_RDONLY)
    try:
        assert fd_source_kind(fd) == "other"
    finally:
        os.close(fd)


def test_fd_source_kind_discriminates_memfd_seal_states():
    from qh.util import fd_source_kind, hold_bytes_memfd
    # unsealed memfd
    fd = _libc_memfd(b"unsealed-probe", UAPI_MFD_CLOEXEC
                     | UAPI_MFD_ALLOW_SEALING)
    try:
        os.write(fd, b"unsealed")
        assert fd_source_kind(fd) == "memfd"
    finally:
        os.close(fd)
    # partially sealed memfd (only F_SEAL_WRITE)
    fd = _libc_memfd(b"partial-probe", UAPI_MFD_CLOEXEC
                     | UAPI_MFD_ALLOW_SEALING)
    try:
        os.write(fd, b"partial")
        fcntl.fcntl(fd, UAPI_F_ADD_SEALS, UAPI_F_SEAL_WRITE)
        assert fd_source_kind(fd) == "memfd"
        seals = fcntl.fcntl(fd, UAPI_F_GET_SEALS)
        assert seals & UAPI_FOUR_SEALS != UAPI_FOUR_SEALS
    finally:
        os.close(fd)
    # fully sealed memfd
    fd, status = hold_bytes_memfd(b"full", name="full-probe")
    try:
        assert status == "sealed"
        assert fd_source_kind(fd) == "memfd"
        seals = fcntl.fcntl(fd, UAPI_F_GET_SEALS)
        assert seals & UAPI_FOUR_SEALS == UAPI_FOUR_SEALS
    finally:
        os.close(fd)


def test_ordinary_file_fcntl_value_does_not_make_memfd(tmp_path):
    """Regression for the observed kernel behavior that F_GET_SEALS returns
    a value even for ordinary files: classification must NOT trust fcntl —
    an ordinary file is an ordinary file regardless."""
    from qh.util import fd_source_kind
    f = tmp_path / "not-a-memfd.txt"
    f.write_text("x")
    fd = os.open(f, os.O_RDONLY)
    try:
        try:
            _ = fcntl.fcntl(fd, UAPI_F_GET_SEALS)  # may "succeed" on file
        except OSError:
            pass
        assert fd_source_kind(fd) == "file"
    finally:
        os.close(fd)
