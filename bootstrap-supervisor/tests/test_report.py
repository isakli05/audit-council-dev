"""Report snapshot custody / leak-screen / freeze tests (S1-007
process-bound lifecycle units) - synthetic reports only."""
import hashlib
import os
import stat
from pathlib import Path

import pytest

from ebs.accounting import open_custody_dir
from ebs.custody import CredentialCustody
from ebs.reportcustody import (ReportRefused, discard_staging,
                               freeze_snapshot, snapshot_staging)

from conftest import SYNTH_CRED, pipe_source, sha_hex

CLEAN_REPORT = b'{"synthetic": true, "content": "inert first-pass double"}\n'


@pytest.fixture
def custody():
    c = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    yield c
    c.close()


@pytest.fixture
def staging(tmp_path):
    d = tmp_path / "staging"
    d.mkdir()
    return d / "stage.json"


@pytest.fixture
def held_out(out_dir):
    """A PRE-OPENED operator custody directory fd (the S1-007 freeze
    channel — same discipline run_attempt uses)."""
    fd = open_custody_dir(out_dir)
    yield fd
    os.close(fd)


def tree_of(dir_fd) -> Path:
    """Caller-visible path of the held directory (for assertions)."""
    return Path(f"/proc/self/fd/{dir_fd}")


def test_clean_snapshot_freezes_0444_with_hash_size(staging, held_out,
                                                    custody):
    staging.write_bytes(CLEAN_REPORT)
    snapshot = snapshot_staging(str(staging))
    assert snapshot == CLEAN_REPORT
    assert not custody.contains(snapshot)       # clean: screen passes
    out = freeze_snapshot(snapshot, held_out, "attempt.report.json")
    frozen = tree_of(held_out) / "attempt.report.json"
    assert out["sha256"] == sha_hex(CLEAN_REPORT)
    assert out["size"] == len(CLEAN_REPORT)
    assert out["mode"] == "0444"
    assert stat.S_IMODE(os.stat(frozen).st_mode) == 0o444
    assert frozen.read_bytes() == CLEAN_REPORT
    discard_staging(str(staging))
    assert not staging.exists()          # moved out of staging


def test_missing_snapshot_is_none_and_stdout_never_substitutes(staging,
                                                               held_out):
    assert snapshot_staging(str(staging)) is None   # REPORT_MISSING
    assert os.listdir(held_out) == []


def test_existing_output_path_cannot_be_overwritten(staging, held_out,
                                                    custody):
    staging.write_bytes(CLEAN_REPORT)
    dest = tree_of(held_out) / "attempt.report.json"
    dest.write_text("operator already holds this slot")
    with pytest.raises(ReportRefused, match="EXISTS"):
        freeze_snapshot(snapshot_staging(str(staging)), held_out,
                        "attempt.report.json")
    assert dest.read_text() == "operator already holds this slot"


def test_symlink_staging_snapshot_refused(staging, held_out, custody,
                                          tmp_path):
    real = tmp_path / "real.json"
    real.write_bytes(CLEAN_REPORT)
    staging.symlink_to(real)
    with pytest.raises(ReportRefused):
        snapshot_staging(str(staging))


def test_non_regular_staging_snapshot_refused(staging, held_out, custody):
    staging.mkdir()
    with pytest.raises(ReportRefused):
        snapshot_staging(str(staging))


def test_credential_containing_snapshot_screened_before_freeze(staging,
                                                               held_out,
                                                               custody):
    poisoned = b'{"note": "' + SYNTH_CRED + b'"}\n'
    staging.write_bytes(poisoned)
    snapshot = snapshot_staging(str(staging))
    assert custody.contains(snapshot)    # contaminated: screen fails
    discard_staging(str(staging))
    assert not staging.exists()          # ephemeral staging removed
    assert os.listdir(held_out) == []    # nothing persisted, no digest


def test_snapshot_size_limit_fail_closed(staging, held_out, custody):
    staging.write_bytes(b"x" * (1024 * 1024 + 1))
    with pytest.raises(ReportRefused, match="SIZE"):
        snapshot_staging(str(staging), size_limit=1024 * 1024)
    assert os.listdir(held_out) == []


def test_no_custody_screen_still_freezes(staging, held_out):
    staging.write_bytes(CLEAN_REPORT)
    out = freeze_snapshot(snapshot_staging(str(staging)), held_out,
                          "attempt.report.json")
    assert out["sha256"] == sha_hex(CLEAN_REPORT)


def test_unsafe_output_directory_refused(staging, out_dir):
    staging.write_bytes(CLEAN_REPORT)
    os.chmod(out_dir, 0o777)
    try:
        with pytest.raises(Exception):
            open_custody_dir(out_dir)
    finally:
        os.chmod(out_dir, 0o700)


def test_frozen_snapshot_is_durable(staging, held_out, custody,
                                    monkeypatch):
    staging.write_bytes(CLEAN_REPORT)
    calls = []
    real = os.fsync
    monkeypatch.setattr(os, "fsync", lambda fd: (calls.append(fd),
                                                 real(fd))[1])
    out = freeze_snapshot(snapshot_staging(str(staging)), held_out,
                          "attempt.report.json")
    assert out["sha256"] == sha_hex(CLEAN_REPORT)
    assert len(calls) >= 2  # file fsync before publication + directory fsync


def test_same_snapshot_is_screened_validated_and_frozen(staging, held_out,
                                                        custody):
    """TOCTOU discipline: the EXACT bytes returned by snapshot_staging
    are the bytes screened and frozen — the staging file is never
    re-read after the snapshot (here proven by mutating the file after
    the snapshot: the frozen artifact still carries the ORIGINAL
    snapshot bytes)."""
    staging.write_bytes(CLEAN_REPORT)
    snapshot = snapshot_staging(str(staging))
    staging.write_bytes(b'{"attacker": "post-snapshot mutation"}')
    assert not custody.contains(snapshot)
    out = freeze_snapshot(snapshot, held_out, "attempt.report.json")
    frozen = tree_of(held_out) / "attempt.report.json"
    assert frozen.read_bytes() == CLEAN_REPORT      # the ORIGINAL bytes
    assert out["sha256"] == hashlib.sha256(CLEAN_REPORT).hexdigest()
