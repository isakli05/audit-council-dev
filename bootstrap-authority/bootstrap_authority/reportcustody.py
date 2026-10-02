"""Report snapshot custody: one immutable snapshot, credential leak
screen, and operator-custody freeze.

Exact pre-target EBS blob DERIVATIVE (BA-PREP-RB2-002): the unchanged
freeze semantics plus the authority-created held-fd report sink
primitives (create_report_sink / snapshot_held_sink /
discard_held_sink), which REPLACE the pre-target pathname-based
snapshot/discard staging primitives (superseded dead surface removed).

The post-exec report lifecycle (CR-EBS-S1-007) is process-bound inside
the single authority operation: the authority CREATES the attempt-owned
report sink (O_CREAT|O_EXCL|O_NOFOLLOW under the held custody fd), the
auditor writes into that exact object, the HELD object is snapshotted
ONCE (regular-file check, size bound, one exact read of the
ALREADY-HELD fd — never a pathname re-open), and THAT SAME immutable
byte sequence is then credential-screened, structurally validated, and
frozen — no validate-one-sequence/freeze-another (TOCTOU) gap exists.
An empty sink stays REPORT_MISSING — stdout/stderr are NEVER
reconstructed as a report.  Screening happens BEFORE any persistence,
hashing or publication (only a boolean classification is ever recorded
for a contaminated report), and the freeze creates the artifact
read-only (0444) with O_EXCL no-overwrite semantics through the
PRE-OPENED held custody fd.  Cleanup unlinks ONLY the exact held sink
object, never a replacement at the sink pathname.
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

def create_report_sink(dir_fd: int, sink_name: str) -> int:
    """Create the authority-owned attempt report sink EXACTLY ONCE
    (RB2-002): O_CREAT|O_EXCL|O_NOFOLLOW relative to the PRE-OPENED
    held custody directory fd; a pre-existing object at the frozen sink
    name refuses.  Returns the HELD O_RDWR fd of the exact created
    object (the auditor child writes through the frozen pathname; the
    authority reads the same object through this fd)."""
    if "/" in sink_name or sink_name in (".", ".."):
        raise ReportRefused(f"SINK_NAME_UNSAFE: {sink_name!r}")
    try:
        fd = os.open(sink_name, os.O_RDWR | os.O_CREAT | os.O_EXCL
                     | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            raise ReportRefused(
                "REPORT_SINK_PREEXISTING: an object already exists at "
                "the binding-frozen report source; only an "
                "authority-created sink can become the first pass"
            ) from exc
        raise ReportRefused(f"REPORT_SINK_CREATE_REFUSED: {exc!r}") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ReportRefused("REPORT_SINK_NOT_REGULAR")
    except Exception:
        os.close(fd)
        raise
    return fd

def snapshot_held_sink(fd: int,
                       size_limit: int = DEFAULT_SIZE_LIMIT):
    """ONE immutable bounded snapshot of the HELD authority-created
    sink OBJECT (never a pathname re-open; RB2-002): empty means the
    auditor produced NO report (None -> REPORT_MISSING); otherwise the
    exact bytes of the ALREADY-HELD fd are read once and every later
    phase operates on exactly these bytes."""
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode):
        raise ReportRefused("SINK_NOT_REGULAR")
    if info.st_size == 0:
        return None
    if info.st_size > size_limit:
        raise ReportRefused(
            f"REPORT_SIZE_LIMIT: {info.st_size} > {size_limit}")
    os.lseek(fd, 0, os.SEEK_SET)
    data = _read_all(fd, size_limit)
    if len(data) > size_limit:
        raise ReportRefused("REPORT_SIZE_LIMIT_AT_READ")
    return data

def discard_held_sink(dir_fd: int, sink_name: str, held_fd: int) -> None:
    """Best-effort removal of the attempt-owned sink OBJECT — never a
    replacement: the name is resolved relative to the held custody fd
    and unlinked ONLY when it still names the EXACT held object (same
    st_dev/st_ino); a replaced or vanished name is left untouched."""
    try:
        named = os.stat(sink_name, dir_fd=dir_fd, follow_symlinks=False)
    except OSError:
        return
    held = os.fstat(held_fd)
    if (named.st_dev, named.st_ino) != (held.st_dev, held.st_ino):
        return
    try:
        os.unlink(sink_name, dir_fd=dir_fd)
    except OSError:
        pass

def freeze_snapshot(snapshot: bytes, out_dir_fd: int,
                    artifact_name: str) -> dict:
    """Freeze the EXACT screened+validated snapshot bytes read-only
    (0444) under operator custody through the PRE-OPENED held output
    directory fd, with O_EXCL no-overwrite semantics and full fsync
    durability; the artifact name is ALWAYS binding-derived."""
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
