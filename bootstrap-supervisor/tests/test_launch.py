"""Verified-open-fd launch tests - inert local fixtures ONLY.

Every exec'd child here is bootstrap-supervisor/tests/fixtures/* — an
unmistakably synthetic local double.  No provider client, no network.

This file also carries the CR-EBS-002 one-shot structural-closure
regression matrix: no authority revival from durable records, exact-
object single-issuance grants, irreversible spend, terminalization of
every post-consumption failure, and supervisor/store mechanical binding.
"""
import copy
import json
import os

import pytest

from ebs.accounting import (AccountingError, AccountingStore,
                            inspect_accounting_record)
from ebs.binding import parse_binding
from ebs.custody import CredentialCustody
from ebs.launch import (CRED_FD, LaunchError, LaunchGrant, LaunchRefused,
                        Supervisor, open_verified_launcher)
from ebs.statemachine import CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, GATES_PASSED, \
    TERMINAL

from conftest import (SYNTH_CRED, binding_for, make_event_package,
                      pipe_source, sha_hex)

MARKER = "EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER"


def build_supervisor(cust_dir, binding_doc, pkg_root):
    binding = parse_binding(json.dumps(binding_doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id, binding.digest)
    return Supervisor(binding, store, pkg_root)


def full_prepare(cust_dir, binding_doc, launcher_path, pkg_root):
    sup = build_supervisor(cust_dir, binding_doc, pkg_root)
    sup.validate_gates()
    sup.verify_launcher(str(launcher_path))
    return sup, sup.consume()


def run_once(sup, grant):
    custody = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    try:
        return sup.execute(grant, custody=custody)
    finally:
        custody.close()


def test_verified_open_fd_launcher_identity(launcher, cust_dir, binding_doc,
                                            event_package):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0],
                              event_package)
    result = run_once(sup, grant)
    assert not result.exec_failed
    md = result.metadata
    assert md["synthetic_marker"] == MARKER
    assert md["variant"] == "INERT-FIXTURE-A"
    assert md["credential_fd3_len"] == len(SYNTH_CRED)
    assert sup.state == EXEC_ATTEMPTED
    assert sup.store.last_state == EXEC_ATTEMPTED


def test_child_receives_only_synthetic_nonsecret_metadata(launcher, cust_dir,
                                                          binding_doc,
                                                          event_package):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0],
                              event_package)
    md = run_once(sup, grant).metadata
    assert SYNTH_CRED not in json.dumps(md).encode()
    # EBS-controlled env only (LC_CTYPE may be added by the interpreter's
    # C-locale coercion, PEP 538 — still non-secret and EBS-uncontrolled
    # content never enters env).
    assert set(md["env"]) <= {"PATH", "LANG", "LC_CTYPE"}
    for arg in md["argv"]:
        assert SYNTH_CRED not in arg.encode()
    for value in md["env"].values():
        assert SYNTH_CRED not in value.encode()


def test_credential_fd_inherited_and_unintended_fds_closed(launcher, cust_dir,
                                                           binding_doc,
                                                           event_package):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0],
                              event_package)
    junk = [os.open("/dev/null", os.O_RDONLY) for _ in range(8)]
    try:
        md = run_once(sup, grant).metadata
    finally:
        for fd in junk:
            os.close(fd)
    fd_map = {int(k): v for k, v in md["fd_map"].items()}
    assert CRED_FD in fd_map and "memfd:" in fd_map[CRED_FD]
    pipes = {fd for fd, target in fd_map.items()
             if target.startswith("pipe:")}
    assert pipes == {1}            # stdout metadata pipe only; the exec-fail
                                   # pipe was CLOEXEC-closed at exec
    assert len(fd_map) <= 7        # no junk/unintended fd inheritance


def test_consume_record_durable_before_child_begins(launcher, cust_dir,
                                                    binding_doc,
                                                    event_package,
                                                    monkeypatch):
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    sup.validate_gates()
    sup.verify_launcher(str(launcher[0]))
    original = AccountingStore.append

    def refusing_append(self, state, **extra):
        if state == CONSUMED_PRE_EXEC:
            raise AccountingError("injected durability failure")
        return original(self, state, **extra)

    monkeypatch.setattr(AccountingStore, "append", refusing_append)
    with pytest.raises(AccountingError):
        sup.consume()
    assert sup.state == GATES_PASSED  # consumption did not complete
    grant = LaunchGrant()             # even a forged grant cannot launch
    monkeypatch.undo()
    with pytest.raises(LaunchError):
        sup.execute(grant, custody=CredentialCustody.ingest(
            pipe_source(), "AUDITOR_A"))


def test_consume_record_persists_full_binding_facts(launcher, cust_dir,
                                                    binding_doc,
                                                    event_package):
    """CR-EBS-001 E: CONSUMED_PRE_EXEC durably records the complete
    non-secret binding identity set, not merely an opaque digest."""
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    sup.validate_gates()
    sup.verify_launcher(str(launcher[0]))
    sup.consume()
    view = inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)
    rec = view["records"][-1]
    assert rec["state"] == CONSUMED_PRE_EXEC
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
    assert rec["auditor_executable_sha256"] == \
        doc["auditor_identity"]["executable_sha256"]
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


def test_wrong_digest_refused_before_fork(launcher, cust_dir, binding_doc,
                                          tmp_path):
    doc = copy.deepcopy(binding_doc)
    doc["boundary_launcher"] = {"identity": "INERT-LOCAL-FIXTURE-LAUNCHER-V1",
                                "sha256": "e" * 64}
    pkg = make_event_package(doc, tmp_path, name="pkg-mutated-launcher")
    sup = build_supervisor(cust_dir, doc, pkg)
    sup.validate_gates()
    with pytest.raises(LaunchRefused, match="DIGEST"):
        sup.verify_launcher(str(launcher[0]))  # disk bytes != bound digest
    assert sup.state == GATES_PASSED   # no fork, authority not consumed
    assert sup.launcher_fd is None
    with pytest.raises(LaunchRefused, match="DIGEST"):
        open_verified_launcher(str(launcher[0]), "0" * 64)


def test_post_consumption_rehash_failure_spends_authority_permanently(
        launcher, cust_dir, binding_doc, event_package):
    """CR-EBS-002 regression 8+10: held-fd re-hash failure after
    consumption permanently spends the one-shot authority (terminalized;
    the same grant, a fresh grant, and a re-execute are all refused)."""
    path, _ = launcher
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    sup.validate_gates()
    sup.verify_launcher(str(path))
    grant = sup.consume()
    with open(path, "ab") as handle:   # same inode, content drift
        handle.write(b"\n# drift\n")
    with pytest.raises(LaunchRefused, match="DIGEST"):
        run_once(sup, grant)
    assert sup.state == TERMINAL       # terminalized, not unconsumed
    assert inspect_accounting_record(
        cust_dir, sup._binding.attempt_id,
        sup._binding.digest)["last_state"] == TERMINAL
    with pytest.raises(LaunchError):   # same (dead) grant
        run_once(sup, grant)
    with pytest.raises(LaunchError):   # freshly forged grant
        run_once(sup, LaunchGrant())


def test_injected_fork_failure_spends_authority_permanently(
        launcher, cust_dir, binding_doc, event_package, monkeypatch):
    """CR-EBS-002 regression 9+10: a pre-child failure (fork) after
    consumption permanently spends the authority; no retry path exists."""

    def broken_fork():
        raise OSError(11, "injected fork failure")

    path, _ = launcher
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    sup.validate_gates()
    sup.verify_launcher(str(path))
    grant = sup.consume()
    monkeypatch.setattr(os, "fork", broken_fork)
    with pytest.raises(LaunchError, match="FORK"):
        run_once(sup, grant)
    monkeypatch.undo()
    assert sup.state == TERMINAL
    with pytest.raises(LaunchError):
        run_once(sup, grant)
    with pytest.raises(LaunchError):
        run_once(sup, LaunchGrant())
    assert inspect_accounting_record(
        cust_dir, sup._binding.attempt_id,
        sup._binding.digest)["last_state"] == TERMINAL


def test_exec_record_failure_after_fork_spends_authority(launcher, cust_dir,
                                                         binding_doc,
                                                         event_package,
                                                         monkeypatch):
    """CR-EBS-002 E: even when the EXEC_ATTEMPTED record cannot be
    reached, the authority is spent (in-process guard)."""
    from ebs.accounting import AccountingStore as Store
    path, _ = launcher
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    sup.validate_gates()
    sup.verify_launcher(str(path))
    grant = sup.consume()
    original = Store.append

    def refusing_exec_record(self, state, **extra):
        if state == EXEC_ATTEMPTED:
            raise AccountingError("injected exec-record failure")
        return original(self, state, **extra)

    monkeypatch.setattr(Store, "append", refusing_exec_record)
    with pytest.raises(AccountingError):
        run_once(sup, grant)
    monkeypatch.undo()
    with pytest.raises(LaunchError):
        run_once(sup, grant)
    with pytest.raises(LaunchError):
        run_once(sup, LaunchGrant())


def test_substitution_race_cannot_change_executed_program(launcher,
                                                          launcher_b,
                                                          cust_dir,
                                                          binding_doc,
                                                          event_package,
                                                          tmp_path):
    path, _ = launcher
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    sup.validate_gates()
    sup.verify_launcher(str(path))      # open fd verified against fixture A
    # PATH SUBSTITUTION after verification: swap the DIRECTORY ENTRY to a
    # different inode holding fixture B
    attacker = tmp_path / "attacker_payload.py"
    attacker.write_text(launcher_b[0].read_text())
    os.chmod(attacker, 0o755)
    os.replace(attacker, path)
    grant = sup.consume()
    result = run_once(sup, grant)
    assert result.metadata["variant"] == "INERT-FIXTURE-A"  # verified fd won


def test_same_ebs_cannot_launch_twice(launcher, cust_dir, binding_doc,
                                        event_package):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0],
                              event_package)
    run_once(sup, grant)
    with pytest.raises(LaunchError):                      # spent authority
        run_once(sup, grant)
    with pytest.raises(LaunchError):                      # forged grant
        run_once(sup, LaunchGrant())


def test_second_consume_cannot_issue_second_live_grant(launcher, cust_dir,
                                                       binding_doc,
                                                       event_package):
    """CR-EBS-002 regression 7: consume() is single-issuance."""
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0],
                              event_package)
    run_once(sup, grant)
    with pytest.raises(LaunchError):
        sup.consume()


def test_freshly_constructed_grant_cannot_execute(launcher, cust_dir,
                                                  binding_doc,
                                                  event_package):
    """CR-EBS-002 regression 6: only the exact object issued by THIS
    supervisor's consume() authorizes a launch — a copy or look-alike is
    structurally refused."""
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0],
                              event_package)
    forged = LaunchGrant()
    with pytest.raises(LaunchError):
        sup.execute(forged, custody=CredentialCustody.ingest(
            pipe_source(), "AUDITOR_A"))
    # the REAL grant still works — pre-condition refusals spend nothing
    result = run_once(sup, grant)
    assert not result.exec_failed


def test_execute_without_real_grant_refused(launcher, cust_dir,
                                              binding_doc, event_package):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0],
                              event_package)
    with pytest.raises(LaunchError):
        sup.execute("not-a-grant", custody=None)
    with pytest.raises(LaunchError):
        sup.execute(grant, custody=None)  # custody is mandatory


def test_consume_requires_gates_passed(cust_dir, binding_doc,
                                        event_package):
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchError):
        sup.consume()  # still PREPARED


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


def test_existing_record_blocks_new_authority_process(launcher, cust_dir,
                                                      binding_doc,
                                                      event_package):
    """CR-EBS-002 regressions 1-3: an existing same-attempt record (at
    PREPARED or GATES_PASSED) can never revive authority in a new
    process; the history stays read-only inspectable."""
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    sup.validate_gates()                      # record now GATES_PASSED
    binding = sup._binding
    with pytest.raises(AccountingError):
        AccountingStore.create(cust_dir, binding.attempt_id, binding.digest)
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["last_state"] == GATES_PASSED   # inspectable, not revivable


def test_exec_failure_after_consumption_is_honest(launcher, cust_dir,
                                                  tmp_path):
    bogus = tmp_path / "bogus_launcher.py"
    bogus.write_text("this is not an executable image\n")
    doc = binding_for(sha_hex(bogus.read_bytes()))
    pkg = make_event_package(doc, tmp_path, name="pkg-bogus-launcher")
    sup = build_supervisor(cust_dir, doc, pkg)
    sup.validate_gates()
    sup.verify_launcher(str(bogus))
    grant = sup.consume()
    result = run_once(sup, grant)
    assert result.exec_failed
    assert result.returncode != 0
    assert sup.state == EXEC_ATTEMPTED  # attempt honestly recorded


def test_launcher_symlink_refused(launcher, cust_dir, binding_doc,
                                    event_package, tmp_path):
    sup = build_supervisor(cust_dir, binding_doc, event_package)
    sup.validate_gates()
    link = tmp_path / "link.py"
    link.symlink_to(launcher[0])
    with pytest.raises(LaunchRefused):
        sup.verify_launcher(str(link))


def test_open_verified_launcher_checks(launcher):
    fd = open_verified_launcher(str(launcher[0]), launcher[1])
    try:
        assert os.fstat(fd).st_size > 0
    finally:
        os.close(fd)
    with pytest.raises(LaunchRefused):
        open_verified_launcher(str(launcher[0]), "0" * 64)
