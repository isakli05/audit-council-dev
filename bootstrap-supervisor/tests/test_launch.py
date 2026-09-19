"""Verified-open-fd launch tests - inert local fixtures ONLY.

Every exec'd child here is bootstrap-supervisor/tests/fixtures/* — an
unmistakably synthetic local double.  No provider client, no network.

This file also carries the CR-EBS-002 one-shot structural-closure
regression matrix and the CR-EBS-001 complete-binding regression under
the CR-EBS-S1-004/-005/-006 single public authority operation
run_attempt(credential_source_fd, launcher_path,
auditor_executable_path): custody admission, launcher + LIVE auditor
executable verification, both dynamic gates, durable GATES_PASSED ->
CONSUMED_PRE_EXEC, the irreversible spend, and the IMMEDIATE fork/exec
all happen inside that ONE caller-uninterruptible call; no authority
revival from durable records, no grant/consume/execute split, no
post-consumption retry, and supervisor/store mechanical binding.
"""
import copy
import json
import os

import pytest

from ebs.accounting import (AccountingError, AccountingStore,
                            inspect_accounting_record)
from ebs.binding import parse_binding
from ebs.launch import (AUDITOR_EXEC_FD, AUDITOR_INVOCATION_FD, CRED_FD,
                        LaunchError, LaunchRefused, Supervisor,
                        open_verified_auditor_executable,
                        open_verified_launcher)
from ebs.statemachine import EXEC_ATTEMPTED, TERMINAL

from conftest import (SYNTH_CRED, binding_for, make_event_package,
                      pipe_source, sha_hex, write_rg_state,
                      clear_rg_tracks, clear_nr_tracks)

MARKER = "EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER"
ATTEMPT = "evt-0011223344556677-A-01"


@pytest.fixture(autouse=True)
def clean_gate_tracks():
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    yield
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)


def build_supervisor(cust_dir, binding_doc, pkg_root):
    binding = parse_binding(json.dumps(binding_doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id, binding.digest)
    return Supervisor(binding, store, pkg_root)


def run_once(sup, launcher, auditor_exe, stage, cust_out):
    return sup.run_attempt(pipe_source(), str(launcher[0]),
                           str(auditor_exe[0]), stage, cust_out)


def test_verified_open_fd_launcher_identity(launcher, auditor_exe, cust_dir,
                                            binding_doc, event_package, stage, cust_out):
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    result = run_once(sup, launcher, auditor_exe, stage, cust_out)
    assert not result.exec_failed
    md = result.metadata
    assert md["synthetic_marker"] == MARKER
    assert md["variant"] == "INERT-FIXTURE-A"
    assert md["credential_fd3_len"] == len(SYNTH_CRED)
    assert sup.state == TERMINAL            # S1-007: single call settles
    assert sup.store.last_state == TERMINAL   # (no staging -> REPORT_MISSING)


def test_child_receives_only_synthetic_nonsecret_metadata(launcher,
                                                          auditor_exe,
                                                          cust_dir,
                                                          binding_doc,
                                                          event_package, stage, cust_out):
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    md = run_once(sup, launcher, auditor_exe, stage, cust_out).metadata
    assert SYNTH_CRED not in json.dumps(md).encode()
    # EBS-controlled env only (LC_CTYPE may be added by the interpreter's
    # C-locale coercion, PEP 538 — still non-secret and NO EBS-uncontrolled
    # content ever enters env: there is no caller env parameter at all).
    assert set(md["env"]) <= {"PATH", "LANG", "LC_CTYPE"}
    for arg in md["argv"]:
        assert SYNTH_CRED not in arg.encode()
    for value in md["env"].values():
        assert SYNTH_CRED not in value.encode()
    for arg in md["invocation_fd6_argv"]:
        assert SYNTH_CRED not in arg.encode()


def test_credential_and_auditor_fds_inherited_unintended_closed(
        launcher, auditor_exe, cust_dir, binding_doc, event_package, stage, cust_out):
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    junk = [os.open("/dev/null", os.O_RDONLY) for _ in range(8)]
    try:
        md = run_once(sup, launcher, auditor_exe, stage, cust_out).metadata
    finally:
        for fd in junk:
            os.close(fd)
    fd_map = {int(k): v for k, v in md["fd_map"].items()}
    assert CRED_FD in fd_map and "memfd:" in fd_map[CRED_FD]
    assert AUDITOR_EXEC_FD in fd_map and \
        not fd_map[AUDITOR_EXEC_FD].startswith("pipe:")
    assert AUDITOR_INVOCATION_FD in fd_map and \
        "memfd:" in fd_map[AUDITOR_INVOCATION_FD]
    pipes = {fd for fd, target in fd_map.items()
             if target.startswith("pipe:")}
    assert pipes == {1}            # stdout metadata pipe only; the exec-fail
                                   # pipe was CLOEXEC-closed at exec
    assert len(fd_map) <= 8        # no junk/unintended fd inheritance


def test_consumed_record_durable_before_child_begins(launcher, auditor_exe,
                                                     cust_dir,
                                                     binding_doc,
                                                     event_package,
                                                     monkeypatch, stage, cust_out):
    """CR-EBS-002: the CONSUMED_PRE_EXEC record is durable BEFORE any
    child can begin — and under S1-005 the append failure inside the
    single operation returns NO ChildResult and terminalizes fail-closed
    (no authority object exists that could be forged and presented)."""
    original = AccountingStore.append

    def refusing_append(self, state, **extra):
        if state == "CONSUMED_PRE_EXEC":
            raise AccountingError("injected durability failure")
        return original(self, state, **extra)

    sup = build_supervisor(cust_dir, binding_doc, event_package)
    monkeypatch.setattr(AccountingStore, "append", refusing_append)
    with pytest.raises(LaunchRefused,
                       match="PREEXEC_CONSUME_RECORD_FAILED"):
        run_once(sup, launcher, auditor_exe, stage, cust_out)
    monkeypatch.undo()
    assert sup.state == "TERMINAL_PREEXEC_STOP"   # never left consumable
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run_once(sup, launcher, auditor_exe, stage, cust_out)      # no retry, no forgery


def test_consumed_record_persists_full_binding_facts(launcher, auditor_exe,
                                                     cust_dir,
                                                     binding_doc,
                                                     event_package, stage, cust_out):
    """CR-EBS-001 complete transport-binding inventory: CONSUMED_PRE_EXEC
    durably records the complete non-secret binding identity set (V4 adds
    the executable version and the exact-invocation digest/count), not
    merely an opaque digest."""
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    run_once(sup, launcher, auditor_exe, stage, cust_out)
    view = inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)
    rec = [r for r in view["records"]
           if r["state"] == "CONSUMED_PRE_EXEC"][-1]
    doc = binding_doc
    assert rec["event_id"] == doc["event_id"]
    assert rec["auditor_role"] == doc["auditor_role"]
    assert rec["target_commit"] == doc["target"]["commit"]
    assert rec["target_qh_tree"] == doc["target"]["qh_tree"]
    assert rec["target_skill_tree"] == doc["target"]["skill_tree"]
    assert rec["event_package_manifest_sha256"] == \
        doc["event_package"]["manifest_sha256"]
    assert rec["event_package_sha256"] == \
        doc["event_package"]["package_sha256"]
    assert rec["boundary_launcher_identity"] == \
        doc["boundary_launcher"]["identity"]
    assert rec["boundary_launcher_sha256"] == \
        doc["boundary_launcher"]["sha256"]
    assert rec["auditor_executable_identity"] == \
        doc["auditor_identity"]["executable_identity"]
    assert rec["auditor_executable_version"] == \
        doc["auditor_identity"]["executable_version"]
    assert rec["auditor_executable_sha256"] == \
        doc["auditor_identity"]["executable_sha256"]
    assert rec["auditor_invocation_argc"] == \
        len(doc["auditor_invocation"])
    assert rec["auditor_invocation_sha256"] == sha_hex(json.dumps(
        doc["auditor_invocation"], sort_keys=True,
        separators=(",", ":")).encode())
    assert rec["provider_role"] == doc["auditor_identity"]["provider_role"]
    assert rec["adapter_id"] == doc["auditor_identity"]["adapter_id"]
    assert rec["prompt_contract_digest"] == doc["prompt_contract_digest"]
    assert rec["common_evidence_manifest_digest"] == \
        doc["common_evidence_manifest_digest"]
    assert rec["sandbox_profile_id"] == doc["sandbox_profile_id"]
    assert rec["tool_wrapper_identity"] == doc["tool_wrapper"]["identity"]
    assert rec["tool_wrapper_sha256"] == doc["tool_wrapper"]["sha256"]
    assert rec["output_identity_name"] == doc["output_identity"]["name"]
    assert rec["ebs_package_manifest_sha256"] == \
        doc["ebs_package"]["manifest_sha256"]
    assert rec["ebs_package_sha256"] == doc["ebs_package"]["package_sha256"]
    assert rec["binding_digest"] == sup._binding.digest
    assert SYNTH_CRED not in json.dumps(rec).encode()   # no secrets


def test_wrong_digest_refused_before_fork(launcher, auditor_exe, cust_dir,
                                          binding_doc, tmp_path, stage, cust_out):
    """Launcher identity verification happens INSIDE the single
    run_attempt operation, BEFORE the dynamic gates: disk bytes differing
    from the bound digest refuse with no fork, no gate execution, and a
    durable fail-closed terminalization."""
    doc = copy.deepcopy(binding_doc)
    doc["boundary_launcher"] = {"identity": "INERT-LOCAL-FIXTURE-LAUNCHER-V1",
                                "sha256": "e" * 64}
    pkg = make_event_package(doc, tmp_path, name="pkg-mutated-launcher")
    sup = build_supervisor(cust_dir, doc, pkg)
    with pytest.raises(LaunchRefused, match="DIGEST"):
        run_once(sup, launcher, auditor_exe, stage, cust_out)
    assert sup.state == "TERMINAL_PREEXEC_STOP"   # no fork, unconsumed
    assert sup.launcher_fd is None
    with pytest.raises(LaunchRefused, match="DIGEST"):
        open_verified_launcher(str(launcher[0]), "0" * 64)


def test_post_consumption_drift_spends_authority_permanently(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        monkeypatch, stage, cust_out):
    """CR-EBS-002 regression: held-launcher drift AFTER consumption
    (injected right after the durable CONSUMED_PRE_EXEC append, before
    the pre-fork re-hash) permanently spends the one-shot authority
    (terminalized; a second run_attempt is refused — never relabeled
    unconsumed)."""
    original = AccountingStore.append

    def drift_after_consume(self, state, **extra):
        record = original(self, state, **extra)
        if state == "CONSUMED_PRE_EXEC":
            with open(launcher[0], "ab") as handle:  # same-inode drift
                handle.write(b"\n# drift\n")
        return record

    sup = build_supervisor(cust_dir, binding_doc, event_package)
    monkeypatch.setattr(AccountingStore, "append", drift_after_consume)
    with pytest.raises(LaunchRefused, match="LAUNCHER_DIGEST_MISMATCH"):
        run_once(sup, launcher, auditor_exe, stage, cust_out)
    monkeypatch.undo()
    assert sup.state == TERMINAL       # terminalized, not unconsumed
    assert inspect_accounting_record(
        cust_dir, sup._binding.attempt_id,
        sup._binding.digest)["last_state"] == TERMINAL
    with pytest.raises(LaunchError):   # no retry path exists at all
        run_once(sup, launcher, auditor_exe, stage, cust_out)


def test_injected_fork_failure_spends_authority_permanently(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        monkeypatch, stage, cust_out):
    """CR-EBS-002 regression: a pre-child failure (fork) after
    consumption permanently spends the authority; no retry path exists.
    The injection is BOUNDARY-only: the first two forks inside
    run_attempt are the two runtime-gate children (allowed through to
    the real fork), the third is the boundary launch fork (injected
    failure) — also proving all three forks happen inside the ONE call."""

    calls = {"n": 0}
    real_fork = os.fork

    def broken_boundary_fork():
        calls["n"] += 1
        if calls["n"] > 2:
            raise OSError(11, "injected fork failure")
        return real_fork()

    sup = build_supervisor(cust_dir, binding_doc, event_package)
    monkeypatch.setattr(os, "fork", broken_boundary_fork)
    with pytest.raises(LaunchError, match="FORK"):
        run_once(sup, launcher, auditor_exe, stage, cust_out)
    monkeypatch.undo()
    assert calls["n"] == 3   # two gate forks + the failing boundary fork
    assert sup.state == TERMINAL
    with pytest.raises(LaunchError):
        run_once(sup, launcher, auditor_exe, stage, cust_out)
    assert inspect_accounting_record(
        cust_dir, sup._binding.attempt_id,
        sup._binding.digest)["last_state"] == TERMINAL


def test_exec_record_failure_after_fork_spends_authority(launcher,
                                                         auditor_exe,
                                                         cust_dir,
                                                         binding_doc,
                                                         event_package,
                                                         monkeypatch, stage, cust_out):
    """CR-EBS-002 E: even when the EXEC_ATTEMPTED record cannot be
    reached, the authority is spent (in-process guard)."""
    from ebs.accounting import AccountingStore as Store
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    original = Store.append

    def refusing_exec_record(self, state, **extra):
        if state == EXEC_ATTEMPTED:
            raise AccountingError("injected exec-record failure")
        return original(self, state, **extra)

    monkeypatch.setattr(Store, "append", refusing_exec_record)
    with pytest.raises(AccountingError):
        run_once(sup, launcher, auditor_exe, stage, cust_out)
    monkeypatch.undo()
    with pytest.raises(LaunchError):
        run_once(sup, launcher, auditor_exe, stage, cust_out)


def test_launcher_substitution_cannot_change_executed_program(
        launcher, launcher_b, auditor_exe, cust_dir, binding_doc,
        event_package, tmp_path, monkeypatch, stage, cust_out):
    """The launcher fd is verified and HELD inside run_attempt; a PATH
    SUBSTITUTION (attacker payload replacing the launcher path on disk
    during the gate interval) cannot change the executed program."""
    from ebs.launch import RUNTIME_GATES
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    original = Supervisor._execute_runtime_gate

    def substituting_gate(self, gate):
        if gate == RUNTIME_GATES[0]:     # substitute DURING the gates
            attacker = tmp_path / "attacker_payload.py"
            attacker.write_text(launcher_b[0].read_text())
            os.chmod(attacker, 0o755)
            os.replace(attacker, launcher[0])
        return original(self, gate)

    monkeypatch.setattr(Supervisor, "_execute_runtime_gate",
                        substituting_gate)
    result = run_once(sup, launcher, auditor_exe, stage, cust_out)
    monkeypatch.undo()
    assert result.metadata["variant"] == "INERT-FIXTURE-A"  # verified fd won


def test_same_ebs_cannot_run_twice(launcher, auditor_exe, cust_dir,
                                   binding_doc, event_package, stage, cust_out):
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    run_once(sup, launcher, auditor_exe, stage, cust_out)
    with pytest.raises(LaunchError):                      # spent authority
        run_once(sup, launcher, auditor_exe, stage, cust_out)


def test_run_attempt_refused_after_terminal_preexec_stop(
        launcher, auditor_exe, cust_dir, binding_doc, event_package, stage, cust_out):
    """From a non-PREPARED state the single authority operation is
    refused (here: after a dynamic-gate failure left the absorbing
    TERMINAL_PREEXEC_STOP)."""
    write_rg_state(ATTEMPT, "fail-status")
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused):
        run_once(sup, launcher, auditor_exe, stage, cust_out)
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run_once(sup, launcher, auditor_exe, stage, cust_out)


def test_supervisor_requires_matching_store_attempt(cust_dir, binding_doc,
                                                    event_package, tmp_path):
    """CR-EBS-002 regression 4 (C): a store for a DIFFERENT attempt id
    cannot be paired with this binding."""
    binding = parse_binding(json.dumps(binding_doc).encode())
    other_dir = tmp_path / "other-accounting"
    other_dir.mkdir(mode=0o700)
    other = "evt-0011223344556677-B-01"
    store = AccountingStore.create(other_dir, other, binding.digest)
    with pytest.raises(LaunchError, match="STORE_ATTEMPT_MISMATCH"):
        Supervisor(binding, store, event_package)


def test_supervisor_requires_matching_store_binding_digest(cust_dir,
                                                           binding_doc,
                                                           event_package):
    """CR-EBS-002 regression 5 (C): a differently-bound store cannot be
    paired with this binding (filename convention is not authority)."""
    binding = parse_binding(json.dumps(binding_doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id, "c" * 64)
    with pytest.raises(LaunchError, match="STORE_BINDING_DIGEST_MISMATCH"):
        Supervisor(binding, store, event_package)


def test_existing_record_blocks_new_authority_process(launcher, auditor_exe,
                                                      cust_dir, binding_doc,
                                                      event_package, stage, cust_out):
    """CR-EBS-002 regressions 1-3: an existing same-attempt record can
    never revive authority in a new process; the history stays read-only
    inspectable."""
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    run_once(sup, launcher, auditor_exe, stage, cust_out)
    binding = sup._binding
    with pytest.raises(AccountingError):
        AccountingStore.create(cust_dir, binding.attempt_id, binding.digest)
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["last_state"] == TERMINAL  # inspectable, not revivable


def test_exec_failure_after_consumption_is_honest(launcher, auditor_exe,
                                                  cust_dir, tmp_path, stage, cust_out):
    bogus = tmp_path / "bogus_launcher.py"
    bogus.write_text("this is not an executable image\n")
    doc = binding_for(sha_hex(bogus.read_bytes()),
                      auditor_sha256=auditor_exe[1])
    pkg = make_event_package(doc, tmp_path, name="pkg-bogus-launcher")
    sup = build_supervisor(cust_dir, doc, pkg)
    result = sup.run_attempt(pipe_source(), str(bogus), str(auditor_exe[0]), stage, cust_out)
    assert result.exec_failed
    assert result.returncode != 0
    assert sup.state == TERMINAL  # exec-fail settles consumed-terminal


def test_launcher_symlink_refused(launcher, auditor_exe, cust_dir,
                                  binding_doc, event_package, tmp_path, stage, cust_out):
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    link = tmp_path / "link.py"
    link.symlink_to(launcher[0])
    with pytest.raises(LaunchRefused):
        sup.run_attempt(pipe_source(), str(link), str(auditor_exe[0]), stage, cust_out)
    assert sup.state == "TERMINAL_PREEXEC_STOP"


def test_open_verified_launcher_checks(launcher, auditor_exe, stage, cust_out):
    fd = open_verified_launcher(str(launcher[0]), launcher[1])
    try:
        assert os.fstat(fd).st_size > 0
    finally:
        os.close(fd)
    with pytest.raises(LaunchRefused):
        open_verified_launcher(str(launcher[0]), "0" * 64)
    fd = open_verified_auditor_executable(str(auditor_exe[0]),
                                          auditor_exe[1])
    try:
        assert os.fstat(fd).st_size > 0
    finally:
        os.close(fd)
    with pytest.raises(LaunchRefused):
        open_verified_auditor_executable(str(auditor_exe[0]), "0" * 64)
