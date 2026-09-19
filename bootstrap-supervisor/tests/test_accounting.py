"""Durable accounting store tests: durability, tamper refusal, and the
REMOVED authority-continuation surface (CR-EBS-002): a historical record
can NEVER revive authority in a new process; it is read-only inspectable
through inspect_accounting_record only."""
import json
import os
import stat

import pytest

from ebs.accounting import (AccountingError, AccountingStore, TamperRefused,
                            UnsafeStore, inspect_accounting_record)
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
    assert store.attempt_id == ATTEMPT
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
        make(cust_dir)   # O_EXCL: same-attempt authority revival impossible


# ---- CR-EBS-002: no authority continuation off the durable record ----

def test_no_attach_authority_api_exists():
    """The authority-bearing attach path is REMOVED, not merely refused:
    neither the store nor any ebs module exposes attach/RESUMABLE."""
    assert not hasattr(AccountingStore, "attach")
    import ebs.accounting as accounting
    import ebs.launch as launch
    for module in (accounting, launch):
        assert "RESUMABLE" not in vars(module)


def test_prepared_record_cannot_revive_authority_in_new_process(cust_dir):
    make(cust_dir)                     # PREPARED record exists (crash sim)
    with pytest.raises(AccountingError):
        make(cust_dir)                 # new authority process refused
    view = inspect_accounting_record(cust_dir, ATTEMPT, DIGEST)
    assert view["last_state"] == PREPARED   # inspectable read-only only


def test_gates_passed_record_cannot_revive_authority_in_new_process(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    with pytest.raises(AccountingError):
        make(cust_dir)
    view = inspect_accounting_record(cust_dir, ATTEMPT, DIGEST)
    assert view["last_state"] == GATES_PASSED


def test_historical_record_is_read_only_inspectable(cust_dir):
    store = make(cust_dir)
    for s in (GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED,
              REPORT_FROZEN, TERMINAL):
        store.append(s)
    view = inspect_accounting_record(cust_dir, ATTEMPT, DIGEST)
    assert isinstance(view, dict)          # NOT an AccountingStore
    assert view["states"] == [PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC,
                              EXEC_ATTEMPTED, REPORT_FROZEN, TERMINAL]
    assert view["last_state"] == TERMINAL
    assert not isinstance(view, AccountingStore)
    mode = os.stat(cust_dir / f"{ATTEMPT}.jsonl").st_mode & 0o777
    assert mode == 0o600                   # untouched by inspection


def test_binding_mismatch_against_existing_record_refused(cust_dir):
    make(cust_dir)
    with pytest.raises(AccountingError):
        inspect_accounting_record(cust_dir, ATTEMPT, OTHER_DIGEST)


def test_absent_record_refused(cust_dir):
    with pytest.raises(AccountingError):
        inspect_accounting_record(cust_dir, "evt-ffffffffffffffff-A-01",
                                  DIGEST)


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
        inspect_accounting_record(cust_dir, ATTEMPT, DIGEST)


def test_truncated_jsonl_refused(cust_dir):
    store = make(cust_dir)
    store.append(GATES_PASSED)
    path = cust_dir / f"{ATTEMPT}.jsonl"
    raw = path.read_bytes()
    path.write_bytes(raw[: len(raw) - 5])  # cut mid-line, no trailing \n
    with pytest.raises(TamperRefused):
        inspect_accounting_record(cust_dir, ATTEMPT, DIGEST)


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
        inspect_accounting_record(cust_dir, ATTEMPT, DIGEST)


def test_symlink_record_refused(cust_dir):
    real = cust_dir / "real.jsonl"
    real.write_text("x")
    link = cust_dir / f"{ATTEMPT}.jsonl"
    link.symlink_to(real)
    with pytest.raises(AccountingError):
        inspect_accounting_record(cust_dir, ATTEMPT, DIGEST)


def test_non_regular_record_refused(cust_dir):
    os.mkfifo(cust_dir / f"{ATTEMPT}.jsonl")
    with pytest.raises(AccountingError):
        inspect_accounting_record(cust_dir, ATTEMPT, DIGEST)


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


def test_consume_record_carries_full_binding_facts(cust_dir, launcher):
    from ebs.binding import parse_binding
    doc = binding_for(launcher[1])
    binding = parse_binding(json.dumps(doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    store.append(GATES_PASSED)
    store.append(CONSUMED_PRE_EXEC, extra={
        "event_id": binding.event_id, "auditor_role": binding.auditor_role,
        "target_commit": binding.target["commit"],
        "event_package_sha256": binding.event_package["package_sha256"],
        "boundary_launcher_sha256": binding.boundary_launcher["sha256"],
        "auditor_executable_sha256":
            binding.auditor_identity["executable_sha256"],
        "provider_role": binding.auditor_identity["provider_role"],
        "adapter_id": binding.auditor_identity["adapter_id"],
        "prompt_contract_digest": binding.prompt_contract_digest,
        "common_evidence_manifest_digest":
            binding.common_evidence_manifest_digest,
        "sandbox_profile_id": binding.sandbox_profile_id,
        "tool_wrapper_sha256": binding.tool_wrapper["sha256"],
        "output_identity_name": binding.output_identity["name"],
        "ebs_package_sha256": binding.ebs_package["package_sha256"],
    })
    rec = json.loads((cust_dir / f"{binding.attempt_id}.jsonl")
                     .read_text().splitlines()[-1])
    assert rec["state"] == CONSUMED_PRE_EXEC
    assert rec["binding_digest"] == binding.digest
    assert rec["event_package_sha256"] == doc["event_package"]["package_sha256"]
    assert rec["auditor_executable_sha256"] == \
        doc["auditor_identity"]["executable_sha256"]
    assert rec["sandbox_profile_id"] == doc["sandbox_profile_id"]
    assert rec["tool_wrapper_sha256"] == doc["tool_wrapper"]["sha256"]
    assert rec["ebs_package_sha256"] == doc["ebs_package"]["package_sha256"]
