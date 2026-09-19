"""Final launch-seam focused suites (CR-EBS-S1-004 + CR-EBS-S1-005 +
CR-EBS-S1-006).

Every credential byte here is SYNTHETIC and INERT; every executed child
is a repository test fixture; the "auditor executable" is the inert
synthetic fixture tests/fixtures/inert_auditor_executable.py, NEVER
executed and NEVER a provider client.  No provider, no network, no real
event package, no canonical event id.

S1-004 matrix (tasking §26): the ONE public authority operation
run_attempt(credential_source_fd, launcher_path,
auditor_executable_path) accepts a credential SOURCE fd — never a
CredentialCustody, never a role — and ingests sealed custody BEFORE any
gate and BEFORE consumption with the role derived ONLY from the binding;
every credential-source / sealing / non-dumpable / role failure is
PREEXEC with authority unconsumed, no dynamic gate executed, no
CONSUMED_PRE_EXEC, no fork, no same-attempt retry; the SAME held custody
serves the child's CRED_FD and the report leak screen; custody closes on
every terminal path.

S1-005 matrix (tasking §27): no LaunchGrant / consume() / execute()
split exists; no public operation returns in GATES_PASSED or
CONSUMED_PRE_EXEC; the successful operation records PREPARED ->
GATES_PASSED -> CONSUMED_PRE_EXEC -> EXEC_ATTEMPTED before returning;
NETWORK_READINESS executes once and RESOURCE_GATE once LAST; the
CONSUMED_PRE_EXEC durable append happens BEFORE the boundary fork
inside the same call; an injected boundary-fork failure after
consumption is terminal and cannot retry; a second run_attempt is
refused.

S1-006 matrix (tasking §28): V4 is required (V1/V2/V3 refused — see
test_eventpackage.py); executable_version and the exact
auditor_invocation are digest- and projection-covered (see test_binding
.py / test_eventpackage.py); the LIVE auditor executable is verified
against the binding SHA before the dynamic gates and before consumption
and HELD; drift and substitution fail closed preexec (gate interval) or
terminally (post-consumption); the held fd reaches the boundary launcher
under the fixed fd contract (CRED_FD=3, FAIL_FD=4, AUDITOR_EXEC_FD=5,
AUDITOR_INVOCATION_FD=6); the child observes exactly the binding-frozen
argv; no caller argv tail / environment override exists anywhere; and
credential bytes never appear in argv, environment, or accounting.
"""
import ctypes
import inspect as pyinspect
import json
import os

import pytest

from ebs.accounting import AccountingStore, inspect_accounting_record
from ebs.binding import parse_binding
from ebs.custody import CustodyError, CredentialCustody
from ebs.launch import (RUNTIME_GATES, LaunchError, LaunchRefused,
                        Supervisor)
from ebs.statemachine import EXEC_ATTEMPTED, TERMINAL

from conftest import (SYNTH_CRED, binding_for, make_event_package,
                      nr_paths, pipe_source, rg_paths, sealed_memfd_source,
                      sha_hex, clear_nr_tracks, clear_rg_tracks,
                      write_nr_state)

ATTEMPT = "evt-0011223344556677-A-01"


@pytest.fixture(autouse=True)
def clean_gate_tracks():
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    yield
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)


def build(cust_dir, binding_doc, event_package):
    binding = parse_binding(json.dumps(binding_doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    return Supervisor(binding, store, event_package)


def run(sup, launcher, auditor_exe):
    return sup.run_attempt(pipe_source(), str(launcher[0]),
                           str(auditor_exe[0]))


def gate_count(paths):
    _, _, count = paths(ATTEMPT)
    if not os.path.exists(count):
        return 0
    with open(count) as handle:
        return int(handle.read().strip() or 0)


def states_of(cust_dir, sup):
    return inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)["states"]


def custody_is_closed(sup) -> bool:
    if sup._custody is None:
        return True
    try:
        sup._custody.fd
        return False
    except CustodyError:
        return True


# ============================ S1-004 ====================================

def test_s1_004_public_api_ingests_source_fd_never_custody(
        launcher, auditor_exe, cust_dir, binding_doc, event_package):
    """The public authority operation's exact parameter set is the
    credential SOURCE fd plus the two byte-identity locator paths; a
    CredentialCustody object (or any non-fd) is refused before the
    attempt advances."""
    params = list(pyinspect.signature(
        Supervisor.run_attempt).parameters)
    assert params == ["self", "credential_source_fd", "launcher_path",
                      "auditor_executable_path"]
    sup = build(cust_dir, binding_doc, event_package)
    custody = CredentialCustody.ingest(pipe_source(), "AUDITOR_A")
    try:
        with pytest.raises(LaunchError,
                           match="RUN_ATTEMPT_REQUIRES_CREDENTIAL_SOURCE"):
            sup.run_attempt(custody, str(launcher[0]),
                            str(auditor_exe[0]))
    finally:
        custody.close()
    assert sup.state == "PREPARED"        # refusal spent nothing
    assert gate_count(nr_paths) == 0
    # the unspent attempt still runs (a custody OBJECT is not a source):
    result = run(sup, launcher, auditor_exe)
    assert not result.exec_failed


def test_s1_004_role_derived_only_from_binding(launcher, auditor_exe,
                                               cust_dir, binding_doc,
                                               event_package, tmp_path):
    """The custody role label is derived ONLY from binding.auditor_role:
    AUDITOR_A and AUDITOR_B bindings both succeed with their OWN role,
    and no role parameter exists anywhere on the public surface."""
    sup = build(cust_dir, binding_doc, event_package)
    run(sup, launcher, auditor_exe)
    assert sup._custody.role == "AUDITOR_A"
    from conftest import valid_binding_document
    doc_b = valid_binding_document(
        event_id="evt-0011223344556688", role="AUDITOR_B",
        launcher_sha256=launcher[1], executable_sha256=auditor_exe[1])
    pkg_b = make_event_package(doc_b, tmp_path, name="pkg-role-b")
    sup_b = build(cust_dir, doc_b, pkg_b)
    sup_b.run_attempt(pipe_source(), str(launcher[0]),
                      str(auditor_exe[0]))
    assert sup_b._custody.role == "AUDITOR_B"
    assert sup_b.state == EXEC_ATTEMPTED


def test_s1_004_defense_in_depth_role_check_trips(cust_dir, binding_doc,
                                                  event_package, launcher,
                                                  auditor_exe,
                                                  monkeypatch):
    """Runtime proof the internal exact-role assertion exists: a
    monkeypatched ingest returning a WRONG-role custody is refused
    PREEXEC with authority unconsumed, no gate executed, no fork."""
    class WrongRoleCustody:
        role = "AUDITOR_B"

        def close(self):
            pass

    monkeypatch.setattr(
        "ebs.launch.CredentialCustody",
        type("Stub", (), {"ingest": staticmethod(
            lambda fd, role: WrongRoleCustody())}))
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match="CUSTODY_ROLE_MISMATCH"):
        run(sup, launcher, auditor_exe)
    monkeypatch.undo()
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert states_of(cust_dir, sup) == ["PREPARED",
                                        "TERMINAL_PREEXEC_STOP"]
    assert gate_count(nr_paths) == 0      # custody BEFORE the gates
    assert gate_count(rg_paths) == 0


def _socket_source(_tmp_path=None):
    pair = (ctypes.c_int * 2)()
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.socketpair(ctypes.c_int(1), ctypes.c_int(1), ctypes.c_int(0),
                       pair) != 0:
        pytest.skip("socketpair syscall unavailable")
    return pair[0]


def _file_source(tmp_path):
    target = tmp_path / "cred.txt"
    target.write_bytes(SYNTH_CRED)
    return os.open(target, os.O_RDONLY)


def _oversized_sealed_memfd_source(_tmp_path=None):
    """A fully sealed memfd holding MORE than MAX_CREDENTIAL_BYTES (a
    pipe cannot carry this without a concurrent reader, so the oversized
    source is a sealed memfd)."""
    import fcntl
    from ebs.custody import F_ADD_SEALS, MFD_ALLOW_SEALING, MFD_CLOEXEC, \
        memfd_create
    fd = memfd_create("ebs-test-oversized", MFD_CLOEXEC | MFD_ALLOW_SEALING)
    os.write(fd, b"x" * 65537)
    fcntl.fcntl(fd, F_ADD_SEALS, 0x0F)
    return fd


S1_004_BAD_SOURCES = [
    ("ordinary-file", "ORDINARY_FILE", _file_source),
    ("unsupported-socket", "KIND_UNSUPPORTED", _socket_source),
    ("unsealed-memfd", "NOT_FULLY_SEALED",
     lambda tmp_path: sealed_memfd_source(seals=0)),
    ("empty-pipe", "LENGTH_INVALID", lambda tmp_path: pipe_source(b"")),
    ("oversized-memfd", "LENGTH_INVALID", _oversized_sealed_memfd_source),
]


@pytest.mark.parametrize("name,refusal,make_source", S1_004_BAD_SOURCES,
                         ids=[case[0] for case in S1_004_BAD_SOURCES])
def test_s1_004_bad_credential_source_blocks_preexec(
        name, refusal, make_source, cust_dir, binding_doc, event_package,
        launcher, auditor_exe, tmp_path):
    """Every malformed/invalid credential SOURCE fails PREEXEC: wrapped
    refusal, authority unconsumed, NO dynamic gate executed, NO
    GATES_PASSED/CONSUMED record, no fork, and no same-attempt retry."""
    source = make_source(tmp_path)
    try:
        sup = build(cust_dir, binding_doc, event_package)
        with pytest.raises(LaunchRefused, match=refusal):
            sup.run_attempt(source, str(launcher[0]), str(auditor_exe[0]))
    finally:
        try:
            os.close(source)
        except OSError:
            pass
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert states_of(cust_dir, sup) == ["PREPARED", "TERMINAL_PREEXEC_STOP"]
    assert gate_count(nr_paths) == 0        # custody admission BEFORE gates
    assert gate_count(rg_paths) == 0
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run(sup, launcher, auditor_exe)     # no same-attempt retry
    assert custody_is_closed(sup)


def test_s1_004_seal_failure_blocks_preexec(cust_dir, binding_doc,
                                            event_package, launcher,
                                            auditor_exe, monkeypatch):
    """A custody memfd/sealing infrastructure failure is PREEXEC."""
    def broken_memfd(name, flags):
        raise CustodyError("CUSTODY_MEMFD_UNAVAILABLE: injected")

    monkeypatch.setattr("ebs.custody.memfd_create", broken_memfd)
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match="MEMFD_UNAVAILABLE"):
        run(sup, launcher, auditor_exe)
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert gate_count(nr_paths) == 0


def test_s1_004_nondumpable_failure_blocks_preexec(cust_dir, binding_doc,
                                                   event_package, launcher,
                                                   auditor_exe,
                                                   monkeypatch):
    """Non-dumpable unavailability is PREEXEC (it precedes any read)."""
    def broken_dumpable():
        raise CustodyError("NON_DUMPABLE_NOT_ESTABLISHED: injected")

    monkeypatch.setattr("ebs.custody.establish_non_dumpable",
                        broken_dumpable)
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match="NON_DUMPABLE"):
        run(sup, launcher, auditor_exe)
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert gate_count(nr_paths) == 0


def test_s1_004_gate_failure_after_custody_closes_custody(
        cust_dir, binding_doc, event_package, launcher, auditor_exe):
    """A custody that WAS established closes when a later preexec step
    (here: a dynamic gate) terminalizes."""
    write_nr_state(ATTEMPT, "route-fail")
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused):
        run(sup, launcher, auditor_exe)
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert custody_is_closed(sup)          # held fd released terminal-side


def test_s1_004_same_custody_serves_child_and_report_screen(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        tmp_path, out_dir):
    """The ONE Supervisor-held custody serves BOTH the child's CRED_FD
    and the report credential-leak screen: a planted staging report
    carrying the synthetic credential marker is screened by the SAME
    custody (REPORT_SCREEN_FAIL, boolean only, nothing persisted), and
    the custody is closed once the attempt is terminal."""
    staging = tmp_path / "staging"
    staging.mkdir()
    stage = staging / "stage.json"
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe)
    assert result.metadata["credential_fd3_len"] == len(SYNTH_CRED)
    assert not custody_is_closed(sup)       # alive for the report screen
    stage.write_bytes(b'{"report": "clean-prefix"}' + SYNTH_CRED +
                      b'{"report": "contaminated"}')
    outcome = sup.adopt_report(str(stage), str(out_dir))
    assert outcome["state"] == "REPORT_SCREEN_FAIL"
    assert not (out_dir / sup._binding.output_identity["name"]).exists()
    assert not stage.exists()               # contaminated staging removed
    assert custody_is_closed(sup)           # closed at terminal
    assert sup.state == TERMINAL            # adopt_report finishes
    assert "REPORT_SCREEN_FAIL" in states_of(cust_dir, sup)


def test_s1_004_clean_report_freezes_and_closes_custody(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        tmp_path, out_dir):
    """Positive report path: clean report freezes 0444 under operator
    custody and the attempt (with its custody) terminalizes."""
    staging = tmp_path / "staging"
    staging.mkdir()
    stage = staging / "stage.json"
    report = b'{"synthetic": "inert first-pass double"}\n'
    stage.write_bytes(report)
    sup = build(cust_dir, binding_doc, event_package)
    run(sup, launcher, auditor_exe)
    outcome = sup.adopt_report(str(stage), str(out_dir))
    assert outcome["state"] == "REPORT_FROZEN"
    frozen = out_dir / sup._binding.output_identity["name"]
    assert frozen.read_bytes() == report
    assert outcome["sha256"] == sha_hex(report)
    assert custody_is_closed(sup)
    assert sup.state == TERMINAL
    assert "REPORT_FROZEN" in states_of(cust_dir, sup)


def test_s1_004_adopt_report_has_no_custody_parameter():
    """adopt_report takes no caller-supplied CredentialCustody."""
    params = list(pyinspect.signature(
        Supervisor.adopt_report).parameters)
    assert params == ["self", "staging_path", "output_root", "size_limit"]


def test_s1_004_custody_closed_on_post_consumption_terminal(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch):
    """Post-consumption terminal failure (boundary fork) also closes the
    held custody."""
    calls = {"n": 0}
    real_fork = os.fork

    def broken_boundary_fork():
        calls["n"] += 1
        if calls["n"] > 2:
            raise OSError(11, "injected fork failure")
        return real_fork()

    sup = build(cust_dir, binding_doc, event_package)
    monkeypatch.setattr(os, "fork", broken_boundary_fork)
    with pytest.raises(LaunchError, match="FORK"):
        run(sup, launcher, auditor_exe)
    monkeypatch.undo()
    assert sup.state == TERMINAL
    assert custody_is_closed(sup)


# ============================ S1-005 ====================================

def test_s1_005_consumption_precedes_fork_in_the_same_call(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch):
    """THE immediacy proof: at the moment of the BOUNDARY fork, the
    durable record's last state is ALREADY CONSUMED_PRE_EXEC (the fsync'd
    append happened before the fork) and the in-process state is
    CONSUMED_PRE_EXEC (EXEC_ATTEMPTED is recorded only after the fork);
    the first two forks are the two gate children, proving all forks
    happen inside the ONE public call."""
    captured = {}
    calls = {"n": 0}
    real_fork = os.fork

    def spy_fork():
        calls["n"] += 1
        captured.setdefault("at_fork", []).append(
            (calls["n"], sup.state, sup.store.last_state))
        return real_fork()

    sup = build(cust_dir, binding_doc, event_package)
    monkeypatch.setattr(os, "fork", spy_fork)
    result = run(sup, launcher, auditor_exe)
    monkeypatch.undo()
    assert not result.exec_failed
    assert calls["n"] == 3                     # 2 gate forks + 1 boundary
    boundary = captured["at_fork"][-1]
    assert boundary[1] == "CONSUMED_PRE_EXEC"  # in-process state at fork
    assert boundary[2] == "CONSUMED_PRE_EXEC"  # DURABLE record at fork
    assert states_of(cust_dir, sup) == ["PREPARED", "GATES_PASSED",
                                        "CONSUMED_PRE_EXEC",
                                        "EXEC_ATTEMPTED"]


def test_s1_005_gate_order_and_exactly_once_inside_one_call(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch):
    """NETWORK_READINESS executes exactly once FIRST and RESOURCE_GATE
    exactly once LAST, both inside the single public call."""
    order = []
    original = Supervisor._execute_runtime_gate

    def recording_gate(self, gate):
        order.append(gate)
        return original(self, gate)

    monkeypatch.setattr(Supervisor, "_execute_runtime_gate", recording_gate)
    run(build(cust_dir, binding_doc, event_package), launcher, auditor_exe)
    monkeypatch.undo()
    assert order == list(RUNTIME_GATES)
    assert gate_count(nr_paths) == 1
    assert gate_count(rg_paths) == 1


def test_s1_005_fork_failure_after_consumption_is_terminal_no_retry(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch):
    """Injected BOUNDARY fork failure after consumption: terminal
    (consumed semantics — never relabeled unconsumed), no retry."""
    calls = {"n": 0}
    real_fork = os.fork

    def broken_boundary_fork():
        calls["n"] += 1
        if calls["n"] > 2:
            raise OSError(11, "injected fork failure")
        return real_fork()

    sup = build(cust_dir, binding_doc, event_package)
    monkeypatch.setattr(os, "fork", broken_boundary_fork)
    with pytest.raises(LaunchError, match="FORK"):
        run(sup, launcher, auditor_exe)
    monkeypatch.undo()
    assert sup.state == TERMINAL
    assert states_of(cust_dir, sup)[-1] == TERMINAL
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run(sup, launcher, auditor_exe)
    assert gate_count(nr_paths) == 1          # gates never re-executed
    assert gate_count(rg_paths) == 1


def test_s1_005_no_authority_shaped_public_object(launcher, auditor_exe,
                                                  cust_dir, binding_doc,
                                                  event_package):
    """After a successful run there is no public authority object at all:
    the returned ChildResult is plain outcome data, the Supervisor exposes
    no grant/capability/token attribute, and re-running is refused by
    state (authority was process state, already spent)."""
    import ebs.launch as launch_mod
    assert not hasattr(launch_mod, "LaunchGrant")
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe)
    assert set(type(result).__dataclass_fields__) == \
        {"returncode", "exec_failed", "metadata"}
    for name, value in vars(sup).items():
        assert not isinstance(value, launch_mod.Supervisor)
        assert value is not result
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run(sup, launcher, auditor_exe)


# ============================ S1-006 ====================================

def test_s1_006_child_observes_held_auditor_executable_identity(
        launcher, auditor_exe, cust_dir, binding_doc, event_package):
    """The boundary launcher observes the HELD verified auditor
    executable under the fixed fd contract: the fd-5 byte SHA equals the
    binding's executable_sha256 and the live fixture bytes."""
    sup = build(cust_dir, binding_doc, event_package)
    md = run(sup, launcher, auditor_exe).metadata
    binding = parse_binding(json.dumps(binding_doc).encode())
    assert md["auditor_exec_fd5_sha256"] == \
        binding.auditor_identity["executable_sha256"]
    assert md["auditor_exec_fd5_sha256"] == auditor_exe[1]
    assert md["auditor_exec_fd5_len"] == \
        os.stat(auditor_exe[0]).st_size


def test_s1_006_exact_frozen_argv_reaches_child_unchanged(
        launcher, auditor_exe, cust_dir, binding_doc, event_package):
    """The boundary launcher parses the sealed invocation spec and sees
    EXACTLY the binding-frozen auditor argv, byte-for-byte (canonical
    digest equality), with ordering preserved."""
    sup = build(cust_dir, binding_doc, event_package)
    md = run(sup, launcher, auditor_exe).metadata
    binding = parse_binding(json.dumps(binding_doc).encode())
    assert md["invocation_fd6_argv"] == binding.auditor_invocation
    assert md["invocation_fd6_sha256"] == sha_hex(json.dumps(
        binding.auditor_invocation, sort_keys=True,
        separators=(",", ":")).encode())


def test_s1_006_child_argv_and_env_are_entirely_ebs_defined(
        launcher, auditor_exe, cust_dir, binding_doc, event_package):
    """The launcher's OWN argv is exactly the EBS-bound context (no
    caller tail can extend it) and the child environment is exactly the
    minimal EBS-defined PATH/LANG class (no caller override surface)."""
    sup = build(cust_dir, binding_doc, event_package)
    md = run(sup, launcher, auditor_exe).metadata
    binding = parse_binding(json.dumps(binding_doc).encode())
    assert md["argv"] == ["--role", binding.auditor_role,
                          "--attempt", binding.attempt_id,
                          "--event", binding.event_id]
    assert set(md["env"]) <= {"PATH", "LANG", "LC_CTYPE"}


def _remake_package(doc, tmp_path):
    make_event_package(doc, tmp_path, name="pkg-sha-mismatch")
    return doc, tmp_path / "pkg-sha-mismatch"


def test_s1_006_live_auditor_sha_mismatch_blocks_preexec(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        tmp_path):
    """A binding pinning a DIFFERENT auditor-executable SHA is refused at
    live verification BEFORE the dynamic gates and BEFORE consumption:
    PREEXEC_EXECUTABLE_IDENTITY_FAIL, both gate counts 0, no fork, no
    retry."""
    doc = json.loads(json.dumps(binding_doc))
    doc["auditor_identity"]["executable_sha256"] = "f" * 64
    # build a package CONSISTENT with the mutated binding (projection
    # matches) so the ONLY mismatch is the LIVE executable bytes:
    doc, pkg_root = _remake_package(doc, tmp_path)
    binding = parse_binding(json.dumps(doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    sup = Supervisor(binding, store, pkg_root)
    with pytest.raises(LaunchRefused,
                       match="PREEXEC_EXECUTABLE_IDENTITY_FAIL"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]))
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert states_of(cust_dir, sup) == ["PREPARED",
                                        "TERMINAL_PREEXEC_STOP"]
    assert gate_count(nr_paths) == 0
    assert gate_count(rg_paths) == 0


def test_s1_006_auditor_symlink_refused(launcher, auditor_exe, cust_dir,
                                        binding_doc, event_package,
                                        tmp_path):
    """No-final-symlink discipline: a symlinked auditor executable is
    refused PREEXEC."""
    link = tmp_path / "auditor_link.py"
    link.symlink_to(auditor_exe[0])
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match="OPEN_REFUSED"):
        sup.run_attempt(pipe_source(), str(launcher[0]), str(link))
    assert sup.state == "TERMINAL_PREEXEC_STOP"


def test_s1_006_auditor_non_executable_refused(launcher, auditor_exe,
                                               cust_dir, binding_doc,
                                               event_package, tmp_path):
    """A non-executable-mode auditor executable is refused PREEXEC."""
    static_copy = tmp_path / "static_auditor.py"
    static_copy.write_bytes(auditor_exe[0].read_bytes())
    os.chmod(static_copy, 0o644)
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match="NOT_EXECUTABLE"):
        sup.run_attempt(pipe_source(), str(launcher[0]), str(static_copy))
    assert sup.state == "TERMINAL_PREEXEC_STOP"


def test_s1_006_auditor_non_regular_refused(launcher, auditor_exe,
                                            cust_dir, binding_doc,
                                            event_package, tmp_path):
    """A non-regular auditor 'executable' (directory) is refused
    PREEXEC."""
    directory = tmp_path / "not-a-file"
    directory.mkdir()
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match="NOT_REGULAR"):
        sup.run_attempt(pipe_source(), str(launcher[0]), str(directory))
    assert sup.state == "TERMINAL_PREEXEC_STOP"


def _drift_during_gates(monkeypatch, target_path):
    """Inject same-inode content drift on target_path while the FIRST
    runtime gate executes (inside the single run_attempt call)."""
    original = Supervisor._execute_runtime_gate

    def drifting_gate(self, gate):
        if gate == RUNTIME_GATES[0]:
            with open(target_path, "ab") as handle:
                handle.write(b"\n# drift-during-gates\n")
        return original(self, gate)

    monkeypatch.setattr(Supervisor, "_execute_runtime_gate", drifting_gate)


def test_s1_006_auditor_fd_drift_during_gates_is_preexec(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch):
    """Held-fd re-hash BEFORE gate acceptance: auditor-executable drift
    during the gate interval is PREEXEC — authority unconsumed, no
    GATES_PASSED record, no fork, no retry."""
    _drift_during_gates(monkeypatch, auditor_exe[0])
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused,
                       match="AUDITOR_EXECUTABLE_IDENTITY_FAIL"):
        run(sup, launcher, auditor_exe)
    monkeypatch.undo()
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert "GATES_PASSED" not in states_of(cust_dir, sup)
    assert gate_count(nr_paths) == 1
    assert gate_count(rg_paths) == 1


def test_s1_006_launcher_fd_drift_during_gates_is_preexec(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch):
    """The same re-hash covers the HELD launcher fd preexec."""
    _drift_during_gates(monkeypatch, launcher[0])
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match="LAUNCHER_DIGEST_MISMATCH"):
        run(sup, launcher, auditor_exe)
    monkeypatch.undo()
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert "GATES_PASSED" not in states_of(cust_dir, sup)


def test_s1_006_auditor_drift_after_consumption_is_terminal(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch):
    """Defense-in-depth post-consumption re-hash: auditor-executable
    drift injected immediately after the durable CONSUMED_PRE_EXEC append
    terminalizes with CONSUMED semantics (no unconsumed relabeling, no
    retry)."""
    original = AccountingStore.append

    def drift_after_consume(self, state, **extra):
        record = original(self, state, **extra)
        if state == "CONSUMED_PRE_EXEC":
            with open(auditor_exe[0], "ab") as handle:
                handle.write(b"\n# drift-after-consumption\n")
        return record

    sup = build(cust_dir, binding_doc, event_package)
    monkeypatch.setattr(AccountingStore, "append", drift_after_consume)
    with pytest.raises(LaunchRefused,
                       match="AUDITOR_EXECUTABLE_IDENTITY_FAIL"):
        run(sup, launcher, auditor_exe)
    monkeypatch.undo()
    assert sup.state == TERMINAL
    assert states_of(cust_dir, sup)[-1] == TERMINAL
    with pytest.raises(LaunchError):
        run(sup, launcher, auditor_exe)


def test_s1_006_auditor_path_substitution_cannot_change_identity(
        cust_dir, binding_doc, event_package, launcher, launcher_b,
        auditor_exe, tmp_path, monkeypatch):
    """Same-path REPLACEMENT after the verified fd is held cannot alter
    the delivered auditor-executable identity: the child observes the
    ORIGINAL binding SHA even though the pathname now holds different
    bytes."""
    original_gate = Supervisor._execute_runtime_gate

    def substituting_gate(self, gate):
        if gate == RUNTIME_GATES[0]:
            attacker = tmp_path / "attacker_auditor.py"
            attacker.write_text(launcher_b[0].read_text())
            os.chmod(attacker, 0o755)
            os.replace(attacker, auditor_exe[0])
        return original_gate(self, gate)

    monkeypatch.setattr(Supervisor, "_execute_runtime_gate",
                        substituting_gate)
    sup = build(cust_dir, binding_doc, event_package)
    md = run(sup, launcher, auditor_exe).metadata
    monkeypatch.undo()
    binding = parse_binding(json.dumps(binding_doc).encode())
    assert md["auditor_exec_fd5_sha256"] == \
        binding.auditor_identity["executable_sha256"]   # held fd won
    assert md["auditor_exec_fd5_sha256"] == auditor_exe[1]


def test_s1_006_fixed_fd_contract_observed(launcher, auditor_exe,
                                           cust_dir, binding_doc,
                                           event_package):
    """The child inherits EXACTLY the fixed contract: fd 3 sealed
    credential memfd, fd 4 nothing (CLOEXEC), fd 5 the held regular
    auditor executable, fd 6 the sealed invocation memfd."""
    from ebs.launch import AUDITOR_EXEC_FD, AUDITOR_INVOCATION_FD, CRED_FD
    sup = build(cust_dir, binding_doc, event_package)
    md = run(sup, launcher, auditor_exe).metadata
    fd_map = {int(k): v for k, v in md["fd_map"].items()}
    assert "memfd:" in fd_map[CRED_FD]
    assert "memfd:" in fd_map[AUDITOR_INVOCATION_FD]
    assert not fd_map[AUDITOR_EXEC_FD].startswith(("pipe:", "memfd:"))
    pipes = {fd for fd, target in fd_map.items()
             if target.startswith("pipe:")}
    assert pipes == {1}    # ONLY stdout; the exec-fail pipe CLOEXEC'd at
                           # exec (slot 4 itself may be reused later by the
                           # interpreter, but never by the fail pipe)


def test_s1_006_credential_absent_from_argv_env_and_accounting(
        launcher, auditor_exe, cust_dir, binding_doc, event_package):
    """The synthetic credential bytes never appear in the child argv, the
    invocation argv, the child environment, or ANY durable accounting
    record (including the invocation digest and gate evidence)."""
    sup = build(cust_dir, binding_doc, event_package)
    md = run(sup, launcher, auditor_exe).metadata
    assert SYNTH_CRED not in json.dumps(md).encode()
    for arg in md["argv"] + md["invocation_fd6_argv"]:
        assert SYNTH_CRED not in arg.encode()
    for value in md["env"].values():
        assert SYNTH_CRED not in value.encode()
    view = inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)
    assert SYNTH_CRED not in json.dumps(view["records"]).encode()
