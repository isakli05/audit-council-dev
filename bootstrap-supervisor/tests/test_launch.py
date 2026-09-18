"""Verified-open-fd launch tests (task §28) - inert local fixtures ONLY.

Every exec'd child here is bootstrap-supervisor/tests/fixtures/* — an
unmistakably synthetic local double.  No provider client, no network.
"""
import json
import os

import pytest

from ebs.accounting import AccountingError, AccountingStore
from ebs.binding import parse_binding
from ebs.custody import CredentialCustody
from ebs.launch import (CRED_FD, LaunchError, LaunchGrant, LaunchRefused,
                        Supervisor, open_verified_launcher)
from ebs.statemachine import CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, GATES_PASSED

from conftest import SYNTH_CRED, binding_for, pipe_source, sha_hex

MARKER = "EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER"


def build_supervisor(cust_dir, binding_doc):
    binding = parse_binding(json.dumps(binding_doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id, binding.digest)
    return Supervisor(binding, store)


def full_prepare(cust_dir, binding_doc, launcher_path):
    sup = build_supervisor(cust_dir, binding_doc)
    sup.validate_gates()
    sup.verify_launcher(str(launcher_path))
    return sup, sup.consume()


def run_once(sup, grant):
    custody = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    try:
        return sup.execute(grant, custody=custody)
    finally:
        custody.close()


def test_verified_open_fd_launcher_identity(launcher, cust_dir, binding_doc):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0])
    result = run_once(sup, grant)
    assert not result.exec_failed
    md = result.metadata
    assert md["synthetic_marker"] == MARKER
    assert md["variant"] == "INERT-FIXTURE-A"
    assert md["credential_fd3_len"] == len(SYNTH_CRED)
    assert sup.state == EXEC_ATTEMPTED
    assert sup.store.last_state == EXEC_ATTEMPTED


def test_child_receives_only_synthetic_nonsecret_metadata(launcher, cust_dir,
                                                          binding_doc):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0])
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
                                                           binding_doc):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0])
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
                                                    monkeypatch):
    sup = build_supervisor(cust_dir, binding_doc)
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
    grant = LaunchGrant(sup)          # even a forged grant cannot launch
    monkeypatch.undo()
    with pytest.raises(LaunchError):
        sup.execute(grant, custody=CredentialCustody.ingest(
            pipe_source(), "AUDITOR_A"))


def test_wrong_digest_refused_before_fork(launcher, cust_dir, binding_doc,
                                          tmp_path):
    doc = dict(binding_doc)
    doc["boundary_launcher"] = {"identity": "INERT-LOCAL-FIXTURE-LAUNCHER-V1",
                                "sha256": "e" * 64}
    sup = build_supervisor(cust_dir, doc)
    sup.validate_gates()
    with pytest.raises(LaunchRefused, match="DIGEST"):
        sup.verify_launcher(str(launcher[0]))  # disk bytes != bound digest
    assert sup.state == GATES_PASSED   # no fork, authority not consumed
    assert sup.launcher_fd is None
    with pytest.raises(LaunchRefused, match="DIGEST"):
        open_verified_launcher(str(launcher[0]), "0" * 64)


def test_post_consumption_same_inode_drift_refused_before_fork(
        launcher, cust_dir, binding_doc):
    path, _ = launcher
    sup = build_supervisor(cust_dir, binding_doc)
    sup.validate_gates()
    sup.verify_launcher(str(path))
    grant = sup.consume()
    with open(path, "ab") as handle:   # same inode, content drift
        handle.write(b"\n# drift\n")
    with pytest.raises(LaunchRefused, match="DIGEST"):
        run_once(sup, grant)
    assert sup.state == CONSUMED_PRE_EXEC  # consumed, never silently retried


def test_substitution_race_cannot_change_executed_program(launcher,
                                                          launcher_b,
                                                          cust_dir,
                                                          binding_doc,
                                                          tmp_path):
    path, _ = launcher
    sup = build_supervisor(cust_dir, binding_doc)
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


def test_same_ebs_cannot_launch_twice(launcher, cust_dir, binding_doc):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0])
    run_once(sup, grant)
    with pytest.raises(LaunchError):                      # dead grant
        run_once(sup, grant)
    with pytest.raises(LaunchError):                      # forged grant
        run_once(sup, LaunchGrant(sup))


def test_execute_without_real_grant_refused(launcher, cust_dir, binding_doc):
    sup, grant = full_prepare(cust_dir, binding_doc, launcher[0])
    with pytest.raises(LaunchError):
        sup.execute("not-a-grant", custody=None)
    with pytest.raises(LaunchError):
        sup.execute(grant, custody=None)  # custody is mandatory


def test_consume_requires_gates_passed(cust_dir, binding_doc):
    sup = build_supervisor(cust_dir, binding_doc)
    with pytest.raises(LaunchError):
        sup.consume()  # still PREPARED


def test_exec_failure_after_consumption_is_honest(launcher, cust_dir,
                                                  tmp_path):
    bogus = tmp_path / "bogus_launcher.py"
    bogus.write_text("this is not an executable image\n")
    doc = binding_for(sha_hex(bogus.read_bytes()))
    sup = build_supervisor(cust_dir, doc)
    sup.validate_gates()
    sup.verify_launcher(str(bogus))
    grant = sup.consume()
    result = run_once(sup, grant)
    assert result.exec_failed
    assert result.returncode != 0
    assert sup.state == EXEC_ATTEMPTED  # attempt honestly recorded


def test_launcher_symlink_refused(launcher, cust_dir, binding_doc, tmp_path):
    sup = build_supervisor(cust_dir, binding_doc)
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
