"""Credential custody tests (task §27) - Linux kernel observable, synthetic only."""
import fcntl
import gc
import os

import pytest

import ebs.custody as custody_mod
from ebs.custody import (CustodyError, CredentialCustody, REQUIRED_SEALS,
                         establish_non_dumpable, get_dumpable)

from conftest import SYNTH_CRED, pipe_source, scan_tree_for, sealed_memfd_source


def test_pipe_source_accepted():
    c = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    assert c.role == "AUDITOR_A"
    assert c.length == len(SYNTH_CRED)
    assert c.seal_bits & REQUIRED_SEALS == REQUIRED_SEALS
    c.close()


def test_fully_sealed_memfd_source_accepted():
    c = CredentialCustody.ingest(sealed_memfd_source(), "AUDITOR_A")
    assert c.length == len(SYNTH_CRED)
    c.close()


def test_ordinary_credential_file_refused(tmp_path):
    p = tmp_path / "cred.txt"
    p.write_bytes(SYNTH_CRED)
    with pytest.raises(CustodyError, match="ORDINARY_FILE"):
        CredentialCustody.ingest(os.open(p, os.O_RDONLY), "AUDITOR_A")


def test_unsealed_memfd_source_refused():
    with pytest.raises(CustodyError, match="SEALED"):
        CredentialCustody.ingest(sealed_memfd_source(seals=0), "AUDITOR_A")


def test_partially_sealed_memfd_source_refused():
    # only F_SEAL_WRITE|F_SEAL_SEAL applied; F_SEAL_SHRINK|F_SEAL_GROW missing
    with pytest.raises(CustodyError, match="SEALED"):
        CredentialCustody.ingest(
            sealed_memfd_source(seals=0x08 | 0x01), "AUDITOR_A")


def test_socket_source_refused():
    # AF_UNIX/SOCK_STREAM socketpair via raw syscall: no socket module is
    # imported anywhere under bootstrap-supervisor (zero-network rule).
    import ctypes
    pair = (ctypes.c_int * 2)()
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.socketpair(ctypes.c_int(1), ctypes.c_int(1), ctypes.c_int(0),
                       pair) != 0:
        pytest.skip("socketpair syscall unavailable")
    try:
        with pytest.raises(CustodyError):
            CredentialCustody.ingest(pair[0], "AUDITOR_A")
    finally:
        os.close(pair[0])
        os.close(pair[1])


def test_directory_source_refused(tmp_path):
    fd = os.open(tmp_path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        with pytest.raises(CustodyError):
            CredentialCustody.ingest(fd, "AUDITOR_A")
    finally:
        os.close(fd)


def test_empty_source_refused():
    r, w = os.pipe()
    os.close(w)
    with pytest.raises(CustodyError, match="LENGTH"):
        CredentialCustody.ingest(r, "AUDITOR_A")


def test_oversize_source_refused():
    with pytest.raises(CustodyError, match="LENGTH"):
        CredentialCustody.ingest(sealed_memfd_source(b"x" * 65537), "AUDITOR_A")


def test_mandatory_four_seals_present_on_custody_memfd():
    c = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    seals = fcntl.fcntl(c.fd, 1034)  # F_GET_SEALS, raw kernel query
    assert seals & REQUIRED_SEALS == REQUIRED_SEALS
    c.close()


def test_custody_memfd_write_is_sealed():
    c = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    with pytest.raises(OSError):
        os.write(c.fd, b"more")  # F_SEAL_WRITE blocks writes
    with pytest.raises(OSError):
        os.ftruncate(c.fd, 0)  # F_SEAL_SHRINK blocks shrink
    c.close()


def test_non_dumpable_established_kernel_observable():
    establish_non_dumpable()
    assert get_dumpable() == 0  # PR_GET_DUMPABLE kernel state


def test_non_dumpable_failure_fails_closed(monkeypatch):
    def boom():
        raise CustodyError("PR_SET_DUMPABLE unavailable")
    monkeypatch.setattr(custody_mod, "establish_non_dumpable", boom)
    with pytest.raises(CustodyError):
        CredentialCustody.ingest(pipe_source(), "AUDITOR_A")


def test_non_dumpable_established_before_read(monkeypatch):
    events = []
    real_nd = custody_mod.establish_non_dumpable
    real_read = os.read
    monkeypatch.setattr(custody_mod, "establish_non_dumpable",
                        lambda: (events.append("nondumpable"), real_nd())[1])
    monkeypatch.setattr(os, "read",
                        lambda fd, n: (events.append("read"),
                                       real_read(fd, n))[1])
    c = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    c.close()
    assert events.index("nondumpable") < events.index("read")


def test_teardown_closes_custody_fd():
    c = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    fd = c.fd
    c.close()
    with pytest.raises(CustodyError):
        c.fd
    with pytest.raises(OSError):
        os.fstat(fd)  # kernel confirms the descriptor is gone


def test_custody_retains_no_plaintext_attribute():
    c = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    try:
        for name in CredentialCustody.__slots__:
            value = getattr(c, name)
            assert value != SYNTH_CRED
            assert not isinstance(value, (bytes, bytearray))
        assert c.role == "AUDITOR_A" and c.length == len(SYNTH_CRED)
    finally:
        c.close()
    del gc.garbage[:]


def test_credential_absent_from_ordinary_outputs(tmp_path):
    c = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    try:
        (tmp_path / "note.txt").write_text("ordinary output")
        (tmp_path / "acc.jsonl").write_text('{"state": "PREPARED"}\n')
        assert scan_tree_for(tmp_path, SYNTH_CRED) == []
        assert not c.contains(b"unrelated bytes")
        assert c.contains(SYNTH_CRED + b"-suffix")  # screen API is boolean-only
    finally:
        c.close()
