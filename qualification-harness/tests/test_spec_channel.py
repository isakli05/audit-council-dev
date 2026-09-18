"""CR-REMED-003 — production trusted input MUST be capability-bound.

The production authority may accept its trusted inputs ONLY through
operator-held capability channels: a PIPE, or a mechanically identified,
FULLY SEALED memfd.  Ordinary-file input (including stdin redirected from
an ordinary file and ``--template-fd <regular-file-fd>``) is REFUSED —
and the SAME gate applies to the pre-controller template channel and the
controller-binding finalization channel (CR-HARDEN-001 §11)."""
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


def _fin_fd_pair():
    """The operator-held finalization pipe (write end retained)."""
    return os.pipe()


def _run_authority(*, argv, pass_fds=(), stdin=None, cwd=None, timeout=60):
    env = {**os.environ, "PYTHONPATH": str(HARNESS_ROOT)}
    proc = subprocess.run(
        argv, pass_fds=tuple(pass_fds), stdin=stdin,
        capture_output=True, text=True, timeout=timeout,
        cwd=cwd or str(HARNESS_ROOT), env=env)
    return proc


def _template_file(tmp_path, env, name="template.json"):
    from qh.trusted_spec import canonical_template_bytes
    spec_file = tmp_path / name
    spec_file.write_bytes(canonical_template_bytes(env.template) + b"\n")
    return spec_file


def test_stdin_redirected_from_ordinary_file_refused(tmp_path):
    """stdin redirected from an ordinary file => REFUSED (an ordinary
    user-owned file is not a trust boundary under the same-UID model)."""
    from qh.compose import CompositionEnv
    base = tmp_path / "env"
    env = CompositionEnv(str(base))
    env.author_template("specchan-0001")
    template_file = _template_file(tmp_path, env)
    custody = _custody_fd_pair()
    fin_r, fin_w = _fin_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "authority",
            "--operator-state", str(tmp_path / "op"),
            "--custody-fd", str(custody),
            "--finalization-fd", str(fin_r)]
    try:
        with open(template_file, "rb") as fh:
            proc = _run_authority(argv=argv, pass_fds=(custody, fin_r),
                                  stdin=fh)
    finally:
        os.close(custody)
        os.close(fin_r)
        os.close(fin_w)
        env.cleanup_procs()
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_SOURCE_KIND_REFUSED" in blob, blob
    assert "file" in blob


def test_template_fd_regular_file_refused(tmp_path):
    """`qh authority --template-fd <regular-file-fd>` => REFUSED."""
    from qh.compose import CompositionEnv
    base = tmp_path / "env"
    env = CompositionEnv(str(base))
    env.author_template("specchan-0002")
    template_file = _template_file(tmp_path, env, "template2.json")
    custody = _custody_fd_pair()
    fin_r, fin_w = _fin_fd_pair()
    fd = os.open(template_file, os.O_RDONLY)
    argv = [sys.executable, "-m", "qh.cli", "authority",
            "--operator-state", str(tmp_path / "op2"),
            "--template-fd", str(fd),
            "--custody-fd", str(custody),
            "--finalization-fd", str(fin_r)]
    try:
        proc = _run_authority(argv=argv, pass_fds=(fd, custody, fin_r))
    finally:
        os.close(fd)
        os.close(custody)
        os.close(fin_r)
        os.close(fin_w)
        env.cleanup_procs()
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_SOURCE_KIND_REFUSED" in blob, blob


def test_template_fd_unsealed_memfd_refused(tmp_path):
    """An unsealed memfd is a memory object but NOT a sealed capability:
    refused (its content is mutable after binding)."""
    import ctypes
    from qh.compose import CompositionEnv
    base = tmp_path / "env"
    env = CompositionEnv(str(base))
    env.author_template("specchan-0003")
    libc = ctypes.CDLL(None, use_errno=True)
    libc.memfd_create.restype = ctypes.c_int
    libc.memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
    fd = libc.memfd_create(b"unsealed-template", 0x0001 | 0x0002)
    os.write(fd, b'{"template_version": 1}')
    custody = _custody_fd_pair()
    fin_r, fin_w = _fin_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "authority",
            "--operator-state", str(tmp_path / "op3"),
            "--template-fd", str(fd),
            "--custody-fd", str(custody),
            "--finalization-fd", str(fin_r)]
    try:
        proc = _run_authority(argv=argv, pass_fds=(fd, custody, fin_r))
    finally:
        os.close(fd)
        os.close(custody)
        os.close(fin_r)
        os.close(fin_w)
        env.cleanup_procs()
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_MEMFD" in blob or "SPEC_SOURCE_KIND_REFUSED" in blob, blob


def test_template_fd_partially_sealed_memfd_refused(tmp_path):
    """A memfd carrying only SOME of the four required seals is refused:
    the template channel requires the complete required seal set."""
    import fcntl
    import ctypes
    from qh.compose import CompositionEnv
    base = tmp_path / "env"
    env = CompositionEnv(str(base))
    env.author_template("specchan-0004")
    libc = ctypes.CDLL(None, use_errno=True)
    libc.memfd_create.restype = ctypes.c_int
    libc.memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
    fd = libc.memfd_create(b"partial-template", 0x0001 | 0x0002)
    os.write(fd, b'{"template_version": 1}')
    fcntl.fcntl(fd, 1033, 0x0008)  # only F_SEAL_WRITE
    custody = _custody_fd_pair()
    fin_r, fin_w = _fin_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "authority",
            "--operator-state", str(tmp_path / "op4"),
            "--template-fd", str(fd),
            "--custody-fd", str(custody),
            "--finalization-fd", str(fin_r)]
    try:
        proc = _run_authority(argv=argv, pass_fds=(fd, custody, fin_r))
    finally:
        os.close(fd)
        os.close(custody)
        os.close(fin_r)
        os.close(fin_w)
        env.cleanup_procs()
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_MEMFD" in blob, blob


def test_finalization_fd_regular_file_refused(tmp_path):
    """CR-HARDEN-001 §11: the FINALIZATION channel is equally
    capability-bound — an ordinary-file finalization fd is REFUSED before
    any byte is read."""
    from qh.compose import CompositionEnv
    from qh.trusted_spec import canonical_template_bytes
    base = tmp_path / "env"
    env = CompositionEnv(str(base))
    env.author_template("specchan-fin-file")
    fin_file = tmp_path / "fin.json"
    fin_file.write_text("{}")
    fin_fd = os.open(fin_file, os.O_RDONLY)
    custody = _custody_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "authority",
            "--operator-state", str(base / "op"),
            "--custody-fd", str(custody),
            "--finalization-fd", str(fin_fd)]
    try:
        proc = _run_authority(argv=argv, pass_fds=(custody, fin_fd),
                              stdin=subprocess.PIPE)
    finally:
        os.close(custody)
        os.close(fin_fd)
        env.cleanup_procs()
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "SPEC_SOURCE_KIND_REFUSED" in blob, blob


@requires_bwrap
@requires_userns
def test_pipe_template_input_accepted(tmp_path):
    """A proper operator PIPE delivering the template is ACCEPTED (the
    authority completes Phase A and reports PRECONTROLLER_READY)."""
    from qh.compose import CompositionEnv
    from qh.trusted_spec import canonical_template_bytes
    base = tmp_path / "env-pipe"
    env = CompositionEnv(str(base))
    env.author_template("specchan-pipe")
    r, w = os.pipe()
    os.write(w, canonical_template_bytes(env.template))
    os.close(w)
    custody = _custody_fd_pair()
    fin_r, fin_w = _fin_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "authority",
            "--operator-state", str(base / "op"),
            "--custody-fd", str(custody),
            "--finalization-fd", str(fin_r),
            "--mint-timeout", "2"]
    env._spawned_procs = getattr(env, "_spawned_procs", [])
    proc = subprocess.Popen(
        argv, pass_fds=(r, custody, fin_r), stdin=r,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(HARNESS_ROOT),
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
    os.close(r)
    os.close(custody)
    os.close(fin_r)
    os.close(fin_w)
    env._spawned_procs.append(proc)
    try:
        line = proc.stdout.readline()
        assert line.strip() == "PRECONTROLLER_READY", \
            (line, proc.stderr.read())
    finally:
        env.cleanup_procs()


@requires_bwrap
@requires_userns
def test_sealed_memfd_template_input_accepted(tmp_path):
    """A mechanically identified, FULLY SEALED memfd is an accepted
    operator capability channel for the pre-controller template."""
    from qh.compose import CompositionEnv
    from qh.trusted_spec import canonical_template_bytes
    from qh.util import hold_bytes_memfd
    base = tmp_path / "env-memfd"
    env = CompositionEnv(str(base))
    env.author_template("specchan-memfd")
    fd, status = hold_bytes_memfd(canonical_template_bytes(env.template),
                                  name="sealed-template-channel")
    assert status == "sealed"
    custody = _custody_fd_pair()
    fin_r, fin_w = _fin_fd_pair()
    argv = [sys.executable, "-m", "qh.cli", "authority",
            "--operator-state", str(base / "op"),
            "--template-fd", str(fd),
            "--custody-fd", str(custody),
            "--finalization-fd", str(fin_r),
            "--mint-timeout", "2"]
    proc = subprocess.Popen(
        argv, pass_fds=(fd, custody, fin_r),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(HARNESS_ROOT),
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})
    os.close(fd)
    os.close(custody)
    os.close(fin_r)
    os.close(fin_w)
    env._spawned_procs = getattr(env, "_spawned_procs", [])
    env._spawned_procs.append(proc)
    try:
        line = proc.stdout.readline()
        assert line.strip() == "PRECONTROLLER_READY", \
            (line, proc.stderr.read())
    finally:
        env.cleanup_procs()
