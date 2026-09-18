"""Generic report custody and credential leak screen.

A boundary child may stage ONE first-pass report artifact.  A missing
staging report stays REPORT_MISSING — stdout/stderr are NEVER
reconstructed as a report.  Staging is opened without symlink following,
size-bounded, screened for credential plaintext BEFORE any persistence,
hashing, or publication (only a boolean classification is ever recorded
for a contaminated report), and a clean report is frozen read-only
(0444) under operator custody with O_EXCL no-overwrite semantics.
"""
from __future__ import annotations

import errno
import hashlib
import os
import stat

from .accounting import open_custody_dir
from .statemachine import REPORT_FROZEN, REPORT_MISSING, REPORT_SCREEN_FAIL

DEFAULT_SIZE_LIMIT = 16 * 1024 * 1024
FROZEN_MODE = 0o444


class ReportError(RuntimeError):
    """Refused report custody operation (fail closed)."""


class ReportRefused(ReportError):
    """Hard refusal: symlink, non-regular, oversize, or unsafe output."""


def _read_all(fd: int, limit: int) -> bytes:
    data = b""
    while len(data) <= limit:
        chunk = os.read(fd, 65536)
        if not chunk:
            break
        data += chunk
    return data


def collect(staging_path, output_root, artifact_name,
            custody=None, size_limit: int = DEFAULT_SIZE_LIMIT) -> dict:
    """Collect, screen, and freeze one staged first-pass report."""
    if "/" in artifact_name or artifact_name in (".", ".."):
        raise ReportRefused(f"ARTIFACT_NAME_UNSAFE: {artifact_name!r}")
    try:
        st = os.stat(os.fspath(staging_path), follow_symlinks=False)
    except FileNotFoundError:
        return {"state": REPORT_MISSING}
    if stat.S_ISLNK(st.st_mode):
        raise ReportRefused("STAGING_IS_SYMLINK")
    if not stat.S_ISREG(st.st_mode):
        raise ReportRefused("STAGING_NOT_REGULAR")
    if st.st_size > size_limit:
        raise ReportRefused(f"REPORT_SIZE_LIMIT: {st.st_size} > {size_limit}")
    try:
        fd = os.open(os.fspath(staging_path), os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise ReportRefused(f"STAGING_OPEN_REFUSED: {exc!r}") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ReportRefused("STAGING_NOT_REGULAR_AT_OPEN")
        data = _read_all(fd, size_limit)
    finally:
        os.close(fd)
    if len(data) > size_limit:
        raise ReportRefused("REPORT_SIZE_LIMIT_AT_READ")

    if custody is not None and custody.contains(data):
        try:  # remove the contaminated ephemeral staging where possible
            os.unlink(os.fspath(staging_path))
        except OSError:
            pass
        return {"state": REPORT_SCREEN_FAIL}

    out_dir = None
    try:
        try:
            out_dir = open_custody_dir(output_root)
        except ReportError:
            raise
        except Exception as exc:
            raise ReportRefused(f"OUTPUT_DIR_UNSAFE: {exc!r}") from exc
        try:
            dest = os.open(artifact_name, os.O_WRONLY | os.O_CREAT
                           | os.O_EXCL | os.O_NOFOLLOW, 0o600,
                           dir_fd=out_dir)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                raise ReportRefused(
                    "OUTPUT_EXISTS_NO_OVERWRITE") from exc
            raise ReportRefused(
                f"OUTPUT_CREATE_REFUSED: {exc!r}") from exc
    except Exception:
        if out_dir is not None:
            os.close(out_dir)
        raise
    try:
        view = memoryview(data)
        while view:
            view = view[os.write(dest, view):]
        os.fsync(dest)
        os.fchmod(dest, FROZEN_MODE)
        os.fsync(dest)
    finally:
        os.close(dest)
    os.fsync(out_dir)
    os.close(out_dir)
    try:
        os.unlink(os.fspath(staging_path))
    except OSError:
        pass
    return {"state": REPORT_FROZEN,
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
            "mode": f"{FROZEN_MODE:04o}"}
