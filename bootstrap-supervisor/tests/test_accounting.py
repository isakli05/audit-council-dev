"""Durable accounting store tests (task §25 restart/replay + §26 negatives)."""
import json
import os
import stat

import pytest

from ebs.accounting import (AccountingError, AccountingStore, ReuseRefused,
                            TamperRefused, UnsafeStore)
from ebs.binding import parse_binding
from ebs.statemachine import CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, GATES_PASSED, \
    PREPARED, REPORT_FROZEN, TERMINAL

from conftest import binding_for, sha_hex

DIGEST = "a" * 64
OTHER_DIGEST = "b" * 64
ATTEMPT = "evt-0011223344556677-A-01"


def make(cust_dir, digest=DIGEST, attempt=ATTEMPT):
    return AccountingStore.create(cust_dir, attempt, digest)


def test_create_writes_first_record_and_is_durable(cust_dir):
    store = make(cust_dir)
    assert store.last_state == PREPARED
    assert store.binding_digest == DIGEST
    raw = (cust_dir / f"{ATTEMPT}.jsonl").read_bytes()
    assert raw.endswith(b"\n")
    rec = json.loads(raw)
    assert rec["seq"] == 1 and rec["state"] == PREPARED and rec["prev"] == "0" * 64


def test_append_builds_hash_chain(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    store.append(CONSUMED_PRE_EXEC)
    lines = (cust_dir / f"{ATTEMPT}.jsonl").read_text().splitlines()
    assert len(lines) == 3
    prev = "0" * 64
    for i, line in enumerate(lines):
        rec = json.loads(line)
        assert rec["seq"] == i + 1
        assert rec["prev"] == prev
        prev = sha_hex(line.encode())
    assert store.last_state == CONSUMED_PRE_EXEC


def test_append_is_append_only(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    before = (cust_dir / f"{ATTEMPT}.jsonl").read_bytes()
    store.append(CONSUMED_PRE_EXEC)
    after = (cust_dir / f"{ATTEMPT}.jsonl").read_bytes()
    assert after.startswith(before)  # earlier bytes untouched


def test_append_refuses_invalid_state_sequence(cust_dir):
    store = make(cust_dir)
    with pytest.raises(AccountingError):
        store.append(TERMINAL)  # PREPARED -> TERMINAL is illegal


def test_duplicate_attempt_record_creation_refused(cust_dir):
    make(cust_dir)
    with pytest.raises(AccountingError):
        make(cust_dir)


def test_attach_restart_ok_before_consumption(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    again = AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)
    assert again.last_state == GATES_PASSED
    again.append(CONSUMED_PRE_EXEC)


def test_restart_with_consumed_attempt_refused(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    store.append(CONSUMED_PRE_EXEC)
    with pytest.raises(ReuseRefused):
        AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)


def test_restart_with_exec_attempt_refused(cust_dir):
    store = make(cust_dir)
    for s in (GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED):
        store.append(s)
    with pytest.raises(ReuseRefused):
        AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)


def test_restart_with_terminal_attempt_refused(cust_dir):
    store = make(cust_dir)
    for s in (GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
              REPORT_FROZEN, TERMINAL):
        store.append(s)
    with pytest.raises(ReuseRefused):
        AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)


def test_binding_mismatch_against_existing_record_refused(cust_dir):
    make(cust_dir)
    with pytest.raises(AccountingError):
        AccountingStore.attach(cust_dir, ATTEMPT, OTHER_DIGEST)


def test_tampered_chain_refused(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    path = cust_dir / f"{ATTEMPT}.jsonl"
    lines = path.read_text().splitlines()
    rec = json.loads(lines[1])
    rec["state"] = CONSUMED_PRE_EXEC  # forged, breaks hash chain
    lines[1] = json.dumps(rec, sort_keys=True, separators=(",", ":"))
    path.write_text("\n".join(lines) + "\n")
    with pytest.raises(TamperRefused):
        AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)


def test_truncated_jsonl_refused(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    path = cust_dir / f"{ATTEMPT}.jsonl"
    raw = path.read_bytes()
    path.write_bytes(raw[: len(raw) - 5])  # cut mid-line, no trailing \n
    with pytest.raises(TamperRefused):
        AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)


def test_seq_gap_refused(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    path = cust_dir / f"{ATTEMPT}.jsonl"
    lines = path.read_text().splitlines()
    rec = json.loads(lines[1])
    rec["seq"] = 9  # re-canonicalized below; digest chain still self-consistent
    lines[1] = json.dumps(rec, sort_keys=True, separators=(",", ":"))
    path.write_text("\n".join(lines) + "\n")
    with pytest.raises(TamperRefused):
        AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)


def test_symlink_record_refused(cust_dir):
    real = cust_dir / "real.jsonl"
    real.write_text("x")
    link = cust_dir / f"{ATTEMPT}.jsonl"
    link.symlink_to(real)
    with pytest.raises(AccountingError):
        AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)


def test_non_regular_record_refused(cust_dir):
    os.mkfifo(cust_dir / f"{ATTEMPT}.jsonl")
    with pytest.raises(AccountingError):
        AccountingStore.attach(cust_dir, ATTEMPT, DIGEST)


@pytest.mark.parametrize("mode", [0o777, 0o770, 0o772])
def test_world_or_group_writable_custody_directory_refused(cust_dir, mode):
    os.chmod(cust_dir, mode)
    with pytest.raises(UnsafeStore):
        make(cust_dir)


def test_non_owner_directory_refused(tmp_path, cust_dir):
    st = os.stat(cust_dir)
    if st.st_uid == 0:
        pytest.skip("running as root: uid check not distinguishable")
    os.chmod(cust_dir, 0o707)  # other-writable also caught by mode rule
    with pytest.raises(UnsafeStore):
        make(cust_dir)


def test_record_mode_restrictive(cust_dir):
    make(cust_dir)
    mode = os.stat(cust_dir / f"{ATTEMPT}.jsonl").st_mode & 0o777
    assert mode == 0o600
    assert mode & 0o077 == 0


def test_file_and_directory_fsync_are_on_pre_launch_path(cust_dir, monkeypatch):
    calls = []
    real_fsync = os.fsync
    dir_fd = os.open(cust_dir, os.O_RDONLY | os.O_DIRECTORY)

    def spy(fd):
        calls.append(fd)
        return real_fsync(fd)

    monkeypatch.setattr(os, "fsync", spy)
    store = make(cust_dir)
    calls.clear()
    store.append(GATES_PASSED)
    store.append(CONSUMED_PRE_EXEC)
    os.close(dir_fd)
    assert calls.count(store._file_fd) >= 1
    assert any(fd != store._file_fd for fd in calls)  # directory fsync happened


def test_missing_directory_refused(tmp_path):
    with pytest.raises(AccountingError):
        AccountingStore.create(tmp_path / "nope", ATTEMPT, DIGEST)
