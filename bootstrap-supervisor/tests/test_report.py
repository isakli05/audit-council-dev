"""Report custody / leak-screen tests (task §29) - synthetic reports only."""
import json
import os
import stat

import pytest

from ebs.custody import CredentialCustody
from ebs.reportcustody import (REPORT_FROZEN, REPORT_MISSING,
                               REPORT_SCREEN_FAIL, ReportRefused, collect)

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


def test_clean_report_freezes_0444_with_hash_size(staging, out_dir, custody):
    staging.write_bytes(CLEAN_REPORT)
    out = collect(str(staging), str(out_dir), "attempt.report.json",
                  custody=custody)
    assert out["state"] == REPORT_FROZEN
    frozen = out_dir / "attempt.report.json"
    assert out["sha256"] == sha_hex(CLEAN_REPORT)
    assert out["size"] == len(CLEAN_REPORT)
    assert out["mode"] == "0444"
    assert stat.S_IMODE(os.stat(frozen).st_mode) == 0o444
    assert frozen.read_bytes() == CLEAN_REPORT
    assert not staging.exists()  # moved out of staging


def test_missing_report_stays_missing_and_stdout_never_substitutes(
        staging, out_dir, custody, capsys):
    print("stdout is NOT a report")
    out = collect(str(staging), str(out_dir), "attempt.report.json",
                  custody=custody)
    assert out["state"] == REPORT_MISSING
    assert not (out_dir / "attempt.report.json").exists()
    assert "sha256" not in out


def test_existing_output_path_cannot_be_overwritten(staging, out_dir, custody):
    staging.write_bytes(CLEAN_REPORT)
    dest = out_dir / "attempt.report.json"
    dest.write_text("operator already holds this slot")
    with pytest.raises(ReportRefused, match="EXISTS"):
        collect(str(staging), str(out_dir), "attempt.report.json",
                custody=custody)
    assert dest.read_text() == "operator already holds this slot"


def test_symlink_staging_report_refused(staging, out_dir, custody, tmp_path):
    real = tmp_path / "real.json"
    real.write_bytes(CLEAN_REPORT)
    staging.symlink_to(real)
    with pytest.raises(ReportRefused):
        collect(str(staging), str(out_dir), "attempt.report.json",
                custody=custody)


def test_credential_containing_report_rejected_before_publish(staging,
                                                              out_dir,
                                                              custody):
    poisoned = b'{"note": "' + SYNTH_CRED + b'"}\n'
    staging.write_bytes(poisoned)
    out = collect(str(staging), str(out_dir), "attempt.report.json",
                  custody=custody)
    assert out["state"] == REPORT_SCREEN_FAIL
    assert "sha256" not in out           # contaminated bytes never hashed
    assert not (out_dir / "attempt.report.json").exists()
    assert not staging.exists()          # ephemeral staging removed
    # only the boolean classification is recorded anywhere:
    assert set(out) == {"state"}


def test_report_size_limit_fail_closed(staging, out_dir, custody):
    staging.write_bytes(b"x" * (1024 * 1024 + 1))
    with pytest.raises(ReportRefused, match="SIZE"):
        collect(str(staging), str(out_dir), "attempt.report.json",
                custody=custody, size_limit=1024 * 1024)
    assert not (out_dir / "attempt.report.json").exists()


def test_no_custody_screen_still_freezes(staging, out_dir):
    staging.write_bytes(CLEAN_REPORT)
    out = collect(str(staging), str(out_dir), "attempt.report.json")
    assert out["state"] == REPORT_FROZEN


def test_unsafe_output_directory_refused(staging, out_dir, custody):
    staging.write_bytes(CLEAN_REPORT)
    os.chmod(out_dir, 0o777)
    try:
        with pytest.raises(ReportRefused):
            collect(str(staging), str(out_dir), "attempt.report.json",
                    custody=custody)
    finally:
        os.chmod(out_dir, 0o700)


def test_frozen_report_is_durable(staging, out_dir, custody, monkeypatch):
    staging.write_bytes(CLEAN_REPORT)
    import ebs.reportcustody as rc
    calls = []
    real = os.fsync
    monkeypatch.setattr(os, "fsync", lambda fd: (calls.append(fd), real(fd))[1])
    out = collect(str(staging), str(out_dir), "attempt.report.json",
                  custody=custody)
    assert out["state"] == REPORT_FROZEN
    assert len(calls) >= 2  # file fsync before publication + directory fsync
