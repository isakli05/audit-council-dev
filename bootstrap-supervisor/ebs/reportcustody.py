"""Report snapshot custody: one immutable snapshot, credential leak
screen, and operator-custody freeze.

The post-exec report lifecycle (CR-EBS-S1-007) is process-bound inside
the single authority operation: the staged artifact is snapshotted ONCE
(no-final-symlink open, regular-file check, size bound, one exact read
of the ALREADY-OPEN fd), and THAT SAME immutable byte sequence is then
credential-screened, structurally validated, and frozen — the bytes are
never re-read, so no validate-one-sequence/freeze-another (TOCTOU) gap
exists.  A missing staging report stays REPORT_MISSING — stdout/stderr
are NEVER reconstructed as a report.  Screening happens BEFORE any
persistence, hashing, or publication (only a boolean classification is
ever recorded for a contaminated report; the contaminated staging bytes
are removed where possible), and the freeze creates the artifact
read-only (0444) under operator custody with O_EXCL no-overwrite
semantics through a PRE-OPENED held custody directory fd (validated
before any authority is consumed; a pathname re-open is never used).
"""
from __future__ import annotations

import errno
import hashlib
import os
import stat

FROZEN_MODE = 0o444
DEFAULT_SIZE_LIMIT = 16 * 1024 * 1024


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


def snapshot_staging(staging_path,
                     size_limit: int = DEFAULT_SIZE_LIMIT):
    """Take the ONE immutable bounded snapshot of the staged report:
    open without symlink following, require a regular file, enforce the
    size bound, read the exact bytes of the ALREADY-OPEN fd once, and
    return them — or None when no staging report exists (REPORT_MISSING;
    stdout/stderr are never a substitute).  Every later phase (screen,
    validator, freeze) operates on exactly these bytes."""
    try:
        st = os.stat(os.fspath(staging_path), follow_symlinks=False)
    except FileNotFoundError:
        return None
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
    return data


def discard_staging(staging_path) -> None:
    """Best-effort removal of contaminated ephemeral staging bytes."""
    try:
        os.unlink(os.fspath(staging_path))
    except OSError:
        pass


def freeze_snapshot(snapshot: bytes, out_dir_fd: int,
                    artifact_name: str) -> dict:
    """Freeze the EXACT screened+validated snapshot bytes read-only
    (0444) under operator custody through the PRE-OPENED held output
    directory fd, with O_EXCL no-overwrite semantics and full fsync
    durability.  The artifact name is ALWAYS binding-derived (checked by
    the caller); no caller filename can replace it."""
    if "/" in artifact_name or artifact_name in (".", ".."):
        raise ReportRefused(f"ARTIFACT_NAME_UNSAFE: {artifact_name!r}")
    try:
        dest = os.open(artifact_name, os.O_WRONLY | os.O_CREAT
                       | os.O_EXCL | os.O_NOFOLLOW, 0o600,
                       dir_fd=out_dir_fd)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            raise ReportRefused(
                "OUTPUT_EXISTS_NO_OVERWRITE") from exc
        raise ReportRefused(f"OUTPUT_CREATE_REFUSED: {exc!r}") from exc
    try:
        view = memoryview(snapshot)
        while view:
            view = view[os.write(dest, view):]
        os.fsync(dest)
        os.fchmod(dest, FROZEN_MODE)
        os.fsync(dest)
    finally:
        os.close(dest)
    os.fsync(out_dir_fd)
    return {"sha256": hashlib.sha256(snapshot).hexdigest(),
            "size": len(snapshot),
            "mode": f"{FROZEN_MODE:04o}"}
