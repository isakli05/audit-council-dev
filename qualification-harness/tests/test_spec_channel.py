"""CR-REMED-003 — production trusted-spec input MUST be capability-bound.

The production root may accept the trusted launch spec ONLY through an
operator-held capability channel: a PIPE, or a mechanically identified,
FULLY SEALED memfd.  Ordinary-file input (including stdin redirected from
an ordinary file and ``--spec-fd <regular-file-fd>``) is REFUSED."""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns


def _custody_fd_pair():
    r, w = os.pipe()
    os.write(w, b"SYNTHETIC-INERT-CUSTODY")
    os.close(w)
    return r


def _run_root(*, argv, pass_fds=(), stdin=None, cwd=None, timeout=60):
    env = {**os.environ, "PYTHONPATH": str(HARNESS_ROOT)}
    proc = subprocess.run(
        argv, pass_fds=tuple(pass_fds), stdin=stdin,
        capture_output=True, text=True, timeout=timeout,
        cwd=cwd or str(HARNESS_ROOT), env=env)
    return proc


def test_stdin_redirected_from_ordinary_file_refused(tmp_path):
    """stdin redirected from an ordinary file => REFUSED (an ordinary
    user-owned file is not a trust boundary under the same-UID model)."""
    from qh.compose import CompositionEnv
    base = tmp_path / "env"
    env = CompositionEnv(str(base))
    env.author_spec("specchan-0001")
    from qh.trusted_spec import canonical_spec_bytes
    spec_file = tmp_path / "spec.json"
    spec_file.write_bytes(canonical_spec_bytes(env.spec) + b"\n")
    custody = _custody_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "root",
            "--operator-state", str(tmp_path / "op"),
            "--custody-fd", str(custody)]
    with open(spec_file, "rb") as fh:
        proc = _run_root(argv=argv, pass_fds=(custody,), stdin=fh)
    os.close(custody)
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_SOURCE_KIND_REFUSED" in blob, blob
    assert "file" in blob


def test_spec_fd_regular_file_refused(tmp_path):
    """`qh root --spec-fd <regular-file-fd>` => REFUSED."""
    from qh.compose import CompositionEnv
    base = tmp_path / "env"
    env = CompositionEnv(str(base))
    env.author_spec("specchan-0002")
    from qh.trusted_spec import canonical_spec_bytes
    spec_file = tmp_path / "spec2.json"
    spec_file.write_bytes(canonical_spec_bytes(env.spec) + b"\n")
    custody = _custody_fd_pair()
    fd = os.open(spec_file, os.O_RDONLY)
    argv = [sys.executable, "-m", "qh.cli", "root",
            "--operator-state", str(tmp_path / "op2"),
            "--spec-fd", str(fd),
            "--custody-fd", str(custody)]
    try:
        proc = _run_root(argv=argv, pass_fds=(fd, custody))
    finally:
        os.close(fd)
        os.close(custody)
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_SOURCE_KIND_REFUSED" in blob, blob


def test_spec_fd_unsealed_memfd_refused(tmp_path):
    """An unsealed memfd is a memory object but NOT a sealed capability:
    refused (its content is mutable after binding)."""
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    libc.memfd_create.restype = ctypes.c_int
    libc.memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
    fd = libc.memfd_create(b"unsealed-spec", 0x0001 | 0x0002)
    os.write(fd, b'{"spec_version": 2}')
    custody = _custody_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "root",
            "--operator-state", str(tmp_path / "op3"),
            "--spec-fd", str(fd),
            "--custody-fd", str(custody)]
    try:
        proc = _run_root(argv=argv, pass_fds=(fd, custody))
    finally:
        os.close(fd)
        os.close(custody)
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_MEMFD" in blob or "SPEC_SOURCE_KIND_REFUSED" in blob, blob


def test_spec_fd_partially_sealed_memfd_refused(tmp_path):
    """A memfd carrying only SOME of the four required seals is refused:
    the spec channel requires the complete required seal set."""
    import fcntl
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    libc.memfd_create.restype = ctypes.c_int
    libc.memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
    fd = libc.memfd_create(b"partial-spec", 0x0001 | 0x0002)
    os.write(fd, b'{"spec_version": 2}')
    fcntl.fcntl(fd, 1033, 0x0008)  # only F_SEAL_WRITE
    custody = _custody_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "root",
            "--operator-state", str(tmp_path / "op4"),
            "--spec-fd", str(fd),
            "--custody-fd", str(custody)]
    try:
        proc = _run_root(argv=argv, pass_fds=(fd, custody))
    finally:
        os.close(fd)
        os.close(custody)
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_MEMFD" in blob, blob


@requires_bwrap
@requires_userns
def test_pipe_spec_input_accepted(tmp_path):
    """A proper operator PIPE delivering the spec is ACCEPTED (root reaches
    READY)."""
    from qh.compose import CompositionEnv
    from qh.trusted_spec import canonical_spec_bytes
    base = tmp_path / "env-pipe"
    env = CompositionEnv(str(base))
    env.author_spec("specchan-pipe")
    r, w = os.pipe()
    os.write(w, canonical_spec_bytes(env.spec))
    os.close(w)
    custody = _custody_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "root",
            "--operator-state", str(base / "op"),
            "--custody-fd", str(custody),
            "--mint-timeout", "2"]
    env._spawned_procs = getattr(env, "_spawned_procs", [])
    proc = subprocess.Popen(
        argv, pass_fds=(r, custody), stdin=r,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(HARNESS_ROOT),
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
    os.close(r)
    os.close(custody)
    try:
        line = proc.stdout.readline()
        assert line.startswith("READY"), (line, proc.stderr.read())
    finally:
        proc.kill()
        proc.wait(timeout=10)
        env.cleanup_procs()


@requires_bwrap
@requires_userns
def test_sealed_memfd_spec_input_accepted(tmp_path):
    """A mechanically identified, FULLY SEALED memfd is an accepted
    operator capability channel for the trusted spec."""
    from qh.compose import CompositionEnv
    from qh.trusted_spec import canonical_spec_bytes
    from qh.util import hold_bytes_memfd
    base = tmp_path / "env-memfd"
    env = CompositionEnv(str(base))
    env.author_spec("specchan-memfd")
    fd, status = hold_bytes_memfd(canonical_spec_bytes(env.spec),
                                  name="sealed-spec-channel")
    assert status == "sealed"
    custody = _custody_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "root",
            "--operator-state", str(base / "op"),
            "--spec-fd", str(fd),
            "--custody-fd", str(custody),
            "--mint-timeout", "2"]
    proc = subprocess.Popen(
        argv, pass_fds=(fd, custody),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(HARNESS_ROOT),
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
    os.close(fd)
    os.close(custody)
    try:
        line = proc.stdout.readline()
        assert line.startswith("READY"), (line, proc.stderr.read())
    finally:
        proc.kill()
        proc.wait(timeout=10)
        env.cleanup_procs()
