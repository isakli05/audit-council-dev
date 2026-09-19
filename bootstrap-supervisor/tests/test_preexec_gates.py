"""Combined preexec-gate ordering/failure tests (CR-EBS-S1-002 +
CR-EBS-S1-003; regressed under the CR-EBS-S1-004/-005/-006 single-call
final launch-seam authority operation).

Every gate executed here is a repository test fixture —
tests/fixtures/inert_network_readiness.py (NO network access of any kind;
an unmistakably synthetic local double for the FUTURE event-package-side
route/resolver preflight artifact, to be built only under the separately
authorized S1 event-package preparation) and
tests/fixtures/inert_resource_gate.py — each driven by an EXTERNAL /tmp
live-state file keyed by attempt id (absent = honest PASS).  No provider,
no network, no real credential, no real event package.

S1-002 matrix (tasking §19): NETWORK_READINESS is the SECOND mandatory
DYNAMIC runtime gate (frozen executable-artifact descriptor, executed
fresh by the EBS BEFORE RESOURCE_GATE); every malformed/failed/oversized/
wrong-context result blocks with authority unconsumed and a durable
TERMINAL_PREEXEC_STOP; a NETWORK_READINESS failure leaves the RESOURCE
gate execution count at exactly 0; there is no same-attempt retry.

S1-003 matrix (tasking §20): the externally separable preexec sequence
validate_gates() -> verify_launcher() -> consume() NO LONGER EXISTS — the
ONE public authority operation run_attempt(credential_source_fd,
launcher_path, auditor_executable_path) verifies the launcher and the
live auditor executable, executes NETWORK_READINESS then RESOURCE_GATE
exactly once each, durably records GATES_PASSED with BOTH fresh evidence
sets, IMMEDIATELY durably records CONSUMED_PRE_EXEC, and proceeds
straight through the fork/exec attempt inside the SAME call; GATES_PASSED
is an INTERNAL TRANSIENT state in which no caller ever regains control;
every failure (either gate, either durable append, launcher/auditor
identity, custody admission) terminalizes fail-closed with no ChildResult
and no same-attempt retry (S1-004/-005/-006 single-call shape).
"""
import ast
import copy
import json
import os

import pytest

from ebs.accounting import AccountingStore, inspect_accounting_record
from ebs.binding import parse_binding
from ebs.launch import LaunchError, LaunchRefused, Supervisor

from conftest import binding_for, make_event_package, nr_paths, \
    pipe_source, rg_paths, sha_hex, write_nr_state, write_rg_state, \
    clear_nr_tracks, clear_rg_tracks

ATTEMPT = "evt-0011223344556677-A-01"


@pytest.fixture(autouse=True)
def clean_gate_tracks():
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    yield
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)


def binding_and_store(cust_dir, doc):
    binding = parse_binding(json.dumps(doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    return binding, store


def build(cust_dir, binding_doc, event_package):
    binding, store = binding_and_store(cust_dir, binding_doc)
    return Supervisor(binding, store, event_package)


def fresh_run(cust_dir, binding_doc, event_package, launcher, auditor_exe, stage, cust_out):
    sup = build(cust_dir, binding_doc, event_package)
    result = sup.run_attempt(pipe_source(), str(launcher[0]),
                             str(auditor_exe[0]), stage, cust_out)
    return sup, result


def gate_count(paths):
    _, _, count = paths(ATTEMPT)
    if not os.path.exists(count):
        return 0
    with open(count) as handle:
        return int(handle.read().strip() or 0)


def rewrite_manifest(pkg_root, doc, mutate):
    """Apply mutate(manifest_dict), recompute the non-circular package
    identity, rewrite MANIFEST.json, and re-pin doc."""
    manifest = json.loads((pkg_root / "MANIFEST.json").read_bytes())
    mutate(manifest)
    manifest.pop("package_sha256", None)
    manifest["package_sha256"] = sha_hex(json.dumps(
        manifest, sort_keys=True, separators=(",", ":")).encode())
    raw = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    (pkg_root / "MANIFEST.json").write_bytes(raw)
    doc["event_package"] = {"manifest_sha256": sha_hex(raw),
                            "package_sha256": manifest["package_sha256"]}


# ---------------- S1-002: the mandatory route-readiness gate ------------

def test_s1_002_network_readiness_descriptor_is_mandatory(binding_doc):
    """A binding without the NETWORK_READINESS runtime-gate descriptor is
    refused at parse: exactly TWO dynamic gates are mandatory."""
    doc = copy.deepcopy(binding_doc)
    del doc["runtime_gates"]["NETWORK_READINESS"]
    with pytest.raises(Exception, match="RUNTIME_GATES_KEYS_INVALID"):
        parse_binding(json.dumps(doc).encode())


def test_s1_002_network_gate_executes_exactly_once_with_fresh_evidence(
        cust_dir, binding_doc, event_package, launcher, auditor_exe, stage, cust_out):
    """A successful single run executes NETWORK_READINESS exactly ONCE
    and the durable GATES_PASSED record carries its full fresh evidence
    set (identity, sha, schema, canonical validated result + digest +
    size) alongside the RESOURCE_GATE evidence."""
    sup, _ = fresh_run(cust_dir, binding_doc, event_package, launcher,
                       auditor_exe, stage, cust_out)
    assert sup.state == "TERMINAL"
    assert gate_count(nr_paths) == 1
    binding = parse_binding(json.dumps(binding_doc).encode())
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    record = [r for r in view["records"]
              if r["state"] == "GATES_PASSED"][-1]
    descriptor = binding.runtime_gates["NETWORK_READINESS"]
    assert record["network_readiness_identity"] == descriptor["identity"]
    assert record["network_readiness_sha256"] == descriptor["sha256"]
    assert record["network_readiness_result_schema"] == \
        descriptor["result_schema"]
    result = json.loads(record["network_readiness_result"])
    assert result["schema"] == descriptor["result_schema"]
    assert result["status"] == "PASS"
    assert result["event_id"] == binding.event_id
    assert result["auditor_role"] == binding.auditor_role
    assert result["attempt_id"] == binding.attempt_id
    assert result["provider_role"] == \
        binding.auditor_identity["provider_role"]
    assert result["boundary_launcher_sha256"] == \
        binding.boundary_launcher["sha256"]
    assert result["sandbox_profile_id"] == binding.sandbox_profile_id
    assert set(result["checks"]) == {"route", "resolver"}
    canonical = json.dumps(result, sort_keys=True,
                           separators=(",", ":")).encode()
    assert record["network_readiness_result_size"] == len(canonical)
    assert record["network_readiness_result_sha256"] == sha_hex(canonical)
    # BOTH gates' evidence is mechanically present in the same record.
    for prefix in ("resource_gate", "network_readiness"):
        for suffix in ("identity", "sha256", "result_schema", "result",
                       "result_sha256", "result_size"):
            assert f"{prefix}_{suffix}" in record


S1_002_MODES = [
    ("exit-nonzero", "NETWORK_READINESS_NONZERO_EXIT"),
    ("malformed", "NETWORK_READINESS_RESULT_MALFORMED"),
    ("dup-key", "NETWORK_READINESS_RESULT_MALFORMED"),
    ("wrong-schema", "NETWORK_READINESS_RESULT_SCHEMA_UNEXPECTED"),
    ("wrong-event", "NETWORK_READINESS_RESULT_CONTEXT_MISMATCH"),
    ("wrong-role", "NETWORK_READINESS_RESULT_CONTEXT_MISMATCH"),
    ("wrong-attempt", "NETWORK_READINESS_RESULT_CONTEXT_MISMATCH"),
    ("wrong-provider", "NETWORK_READINESS_RESULT_CONTEXT_MISMATCH"),
    ("wrong-launcher-sha", "NETWORK_READINESS_RESULT_CONTEXT_MISMATCH"),
    ("wrong-profile", "NETWORK_READINESS_RESULT_CONTEXT_MISMATCH"),
    ("fail-status", "NETWORK_READINESS_RESULT_NOT_PASS"),
    ("route-fail", "NETWORK_READINESS_CHECK_NOT_PASS"),
    ("resolver-fail", "NETWORK_READINESS_CHECK_NOT_PASS"),
    ("check-status-nonpass", "NETWORK_READINESS_CHECK_NOT_PASS"),
    ("check-missing", "NETWORK_READINESS_CHECKS_INVALID"),
    ("check-extra", "NETWORK_READINESS_CHECKS_INVALID"),
    ("detail-not-object", "NETWORK_READINESS_CHECK_INVALID"),
    ("detail-missing", "NETWORK_READINESS_CHECK_INVALID"),
    ("empty-output", "NETWORK_READINESS_OUTPUT_MISSING"),
    ("oversized", "NETWORK_READINESS_OUTPUT_TOO_LARGE"),
]


@pytest.mark.parametrize("mode,refusal", S1_002_MODES,
                         ids=[case[0] for case in S1_002_MODES])
def test_s1_002_mode_matrix_blocks_before_any_authority(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        mode, refusal, stage, cust_out):
    """Every malformed / failed / wrong-context fresh NETWORK_READINESS
    result blocks: no GATES_PASSED, no CONSUMED_PRE_EXEC, no ChildResult,
    durable TERMINAL_PREEXEC_STOP, exactly one network-gate execution, and
    — the ordering proof — a RESOURCE_GATE execution count of EXACTLY 0
    (the resource gate never runs when route readiness fails)."""
    write_nr_state(ATTEMPT, mode)
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match=refusal):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    binding = parse_binding(json.dumps(binding_doc).encode())
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["last_state"] == "TERMINAL_PREEXEC_STOP"
    assert "GATES_PASSED" not in view["states"]
    assert "CONSUMED_PRE_EXEC" not in view["states"]
    assert "EXEC_ATTEMPTED" not in view["states"]
    assert gate_count(nr_paths) == 1        # network gate ran exactly once
    assert gate_count(rg_paths) == 0        # resource gate NEVER executed


def test_s1_002_hang_is_bounded_and_blocks(cust_dir, binding_doc,
                                           event_package, launcher,
                                           auditor_exe, stage, cust_out):
    """A hung network-readiness gate is NOT an unbounded authority
    process: the deterministic bounded timeout kills it fail-closed, the
    resource gate never executes, and the attempt terminalizes."""
    import time
    write_nr_state(ATTEMPT, "hang")
    sup = build(cust_dir, binding_doc, event_package)
    started = time.monotonic()
    with pytest.raises(LaunchRefused, match="NETWORK_READINESS_TIMEOUT"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    assert time.monotonic() - started < 60
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert gate_count(rg_paths) == 0


def test_s1_002_no_same_attempt_retry_after_network_failure(
        cust_dir, binding_doc, event_package, launcher, auditor_exe, stage, cust_out):
    """After a NETWORK_READINESS failure there is NO same-attempt retry:
    the second run_attempt is refused by state and both execution counts
    stay fixed (network 1, resource 0)."""
    write_nr_state(ATTEMPT, "route-fail")
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    assert gate_count(nr_paths) == 1
    assert gate_count(rg_paths) == 0


def test_s1_002_network_gate_path_not_a_manifest_row_refused(
        cust_dir, binding_doc, tmp_path):
    """A NETWORK_READINESS descriptor path that is no manifest row of the
    verified package is refused at startup: the executed artifact must be
    package-manifest-covered (the verified fd is opened from the ALREADY
    verified package tree)."""
    doc = copy.deepcopy(binding_doc)
    doc["runtime_gates"]["NETWORK_READINESS"]["path"] = \
        "runtime/other-network-readiness.py"
    pkg2 = make_event_package(doc, tmp_path, name="pkg-other-nr-path")
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused,
                       match="NETWORK_READINESS_NOT_PACKAGE_MANIFEST_ROW"):
        Supervisor(binding, store, pkg2)


def test_s1_002_network_gate_artifact_digest_mismatch_refused(
        cust_dir, binding_doc, event_package):
    """A REGENERATED self-consistent package (pins updated) whose LIVE
    network-readiness artifact bytes differ from the binding descriptor's
    exact SHA-256 — while the manifest projection still declares the
    ORIGINAL descriptor — is refused at gate-artifact identity
    verification BEFORE any gate executes (record stays PREPARED)."""
    doc = copy.deepcopy(binding_doc)
    gate = event_package / "runtime" / "network-readiness.py"
    gate.write_text(gate.read_text() + "\n# one-byte-class change\n")
    os.chmod(gate, 0o755)
    rewrite_manifest(event_package, doc,
                     lambda m: m["files"].__setitem__(
                         next(i for i, row in enumerate(m["files"])
                              if row["path"] ==
                              "runtime/network-readiness.py"),
                         {"path": "runtime/network-readiness.py",
                          "bytes": gate.stat().st_size,
                          "sha256": sha_hex(gate.read_bytes())}))
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused,
                       match="NETWORK_READINESS_ARTIFACT_DIGEST_MISMATCH"):
        Supervisor(binding, store, event_package)
    assert inspect_accounting_record(
        cust_dir, binding.attempt_id, binding.digest)["last_state"] \
        == "PREPARED"


def test_s1_002_resource_gate_runs_after_network_and_blocks_alone(
        cust_dir, binding_doc, event_package, launcher, auditor_exe, stage, cust_out):
    """RESOURCE_GATE remains the LAST dynamic environmental gate: when
    NETWORK_READINESS passes but the live resource state is failing, the
    network gate HAS executed (count 1), the resource gate observes the
    failure fresh (count 1), and NO authority is granted."""
    write_rg_state(ATTEMPT, "fail-state")
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused, match="RESOURCE_GATE_RESULT_NOT_PASS"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert gate_count(nr_paths) == 1
    assert gate_count(rg_paths) == 1
    binding = parse_binding(json.dumps(binding_doc).encode())
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert "GATES_PASSED" not in view["states"]
    assert "CONSUMED_PRE_EXEC" not in view["states"]


# ---------------- S1-003: structural freshness coupling -----------------

def test_s1_003_old_public_preexec_sequence_is_gone():
    """The independent public authority-path operations no longer exist:
    no validate_gates and no verify_launcher on the Supervisor."""
    assert not hasattr(Supervisor, "validate_gates")
    assert not hasattr(Supervisor, "verify_launcher")


def test_s1_005_no_portable_grant_or_execute_surface_exists():
    """CR-EBS-S1-005/S1-004: the grant/consume/execute authority split is
    STRUCTURALLY GONE — there is no LaunchGrant class, no Supervisor
    consume/execute, and (with the AST shape test below) no public method
    returns in GATES_PASSED or CONSUMED_PRE_EXEC."""
    import ebs.launch as launch_mod
    assert not hasattr(launch_mod, "LaunchGrant")
    assert not hasattr(Supervisor, "consume")
    assert not hasattr(Supervisor, "execute")
    assert not hasattr(Supervisor, "validate_gates")
    assert not hasattr(Supervisor, "verify_launcher")


def test_s1_003_no_method_enters_gates_passed_without_consuming():
    """Source-shape regression: EVERY Supervisor method that transitions
    into GATES_PASSED also transitions to CONSUMED_PRE_EXEC within the
    same method body — no externally callable method can independently
    advance PREPARED -> GATES_PASSED and return."""
    source_path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "ebs", "launch.py")
    tree = ast.parse(open(source_path).read(), filename=source_path)
    supervisor = next(node for node in tree.body
                      if isinstance(node, ast.ClassDef)
                      and node.name == "Supervisor")

    def transition_targets(fn):
        targets = set()
        for node in ast.walk(fn):
            if isinstance(node, ast.Call) and \
                    isinstance(node.func, ast.Attribute) and \
                    node.func.attr == "transition" and node.args and \
                    isinstance(node.args[0], ast.Name):
                targets.add(node.args[0].id)
        return targets

    checked = 0
    for fn in [n for n in supervisor.body if isinstance(n, ast.FunctionDef)]:
        targets = transition_targets(fn)
        if "GATES_PASSED" in targets:
            assert "CONSUMED_PRE_EXEC" in targets, \
                f"{fn.name} enters GATES_PASSED without consuming"
            checked += 1
    assert checked >= 1    # the single authority operation must exist


def test_s1_003_single_operation_records_full_launch_sequence(
        cust_dir, binding_doc, event_package, launcher, auditor_exe, stage, cust_out):
    """THE S1-003/S1-005 positive: one public operation durably records
    PREPARED -> GATES_PASSED -> CONSUMED_PRE_EXEC -> EXEC_ATTEMPTED (in
    that order) and only then returns its ChildResult; both dynamic gates
    executed exactly once each (network first, resource last); the state
    machine is at EXEC_ATTEMPTED at return — never GATES_PASSED, never
    CONSUMED_PRE_EXEC."""
    sup, result = fresh_run(cust_dir, binding_doc, event_package,
                            launcher, auditor_exe, stage, cust_out)
    assert not result.exec_failed
    assert sup.state == "TERMINAL"
    assert gate_count(nr_paths) == 1
    assert gate_count(rg_paths) == 1
    binding = parse_binding(json.dumps(binding_doc).encode())
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["states"] == ["PREPARED", "GATES_PASSED",
                              "CONSUMED_PRE_EXEC", "EXEC_ATTEMPTED",
                              "REPORT_MISSING", "TERMINAL"]


def test_s1_003_launcher_mismatch_terminalizes_before_either_gate(
        cust_dir, tmp_path, launcher, auditor_exe, stage, cust_out):
    """Launcher identity verification happens BEFORE the dynamic gates: a
    launcher whose bytes differ from the bound SHA-256 terminalizes the
    attempt with BOTH gate execution counts at exactly 0 and no
    GATES_PASSED / CONSUMED record."""
    doc = binding_for("e" * 64, auditor_sha256=auditor_exe[1])
    pkg = make_event_package(doc, tmp_path, name="pkg-mutated-launcher")
    sup = build(cust_dir, doc, pkg)
    with pytest.raises(LaunchRefused, match="DIGEST"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    binding = parse_binding(json.dumps(doc).encode())
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["states"] == ["PREPARED", "TERMINAL_PREEXEC_STOP"]
    assert gate_count(nr_paths) == 0
    assert gate_count(rg_paths) == 0
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)   # no same-attempt retry


def test_s1_003_gates_passed_append_failure_returns_no_child_result(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch, stage, cust_out):
    """A GATES_PASSED record-persistence failure AFTER both fresh gate
    PASSes returns NO ChildResult, terminalizes fail-closed, and permits
    no same-attempt retry (both gates already executed exactly once)."""
    from ebs.accounting import AccountingError
    original = AccountingStore.append

    def refusing_append(self, state, extra=None):
        if state == "GATES_PASSED":
            raise AccountingError("injected durability failure")
        return original(self, state, extra=extra)

    monkeypatch.setattr(AccountingStore, "append", refusing_append)
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused,
                       match="PREEXEC_CONSUME_RECORD_FAILED"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    monkeypatch.undo()
    assert sup.state == "TERMINAL_PREEXEC_STOP"   # never GATES_PASSED
    binding = parse_binding(json.dumps(binding_doc).encode())
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert "GATES_PASSED" not in view["states"]
    assert "CONSUMED_PRE_EXEC" not in view["states"]
    assert gate_count(nr_paths) == 1
    assert gate_count(rg_paths) == 1
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)


def test_s1_003_consumed_append_failure_after_gates_passed(
        cust_dir, binding_doc, event_package, launcher, auditor_exe,
        monkeypatch, stage, cust_out):
    """THE caller-visible-GATES_PASSED negative: GATES_PASSED persists but
    the CONSUMED_PRE_EXEC append fails — NO ChildResult is returned, the
    supervisor terminalizes fail-closed (GATES_PASSED is never left as a
    returned-to-caller state), the durable record honestly shows the
    fail-closed terminal path, and no same-attempt retry exists."""
    from ebs.accounting import AccountingError
    original = AccountingStore.append

    def refusing_append(self, state, extra=None):
        if state == "CONSUMED_PRE_EXEC":
            raise AccountingError("injected durability failure")
        return original(self, state, extra=extra)

    monkeypatch.setattr(AccountingStore, "append", refusing_append)
    sup = build(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchRefused,
                       match="PREEXEC_CONSUME_RECORD_FAILED"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    monkeypatch.undo()
    assert sup.state == "TERMINAL_PREEXEC_STOP"   # NOT GATES_PASSED
    binding = parse_binding(json.dumps(binding_doc).encode())
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["states"] == ["PREPARED", "GATES_PASSED",
                              "TERMINAL_PREEXEC_STOP"]
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)      # no retry, no resumption
    assert gate_count(nr_paths) == 1              # no re-execution either
    assert gate_count(rg_paths) == 1


def test_s1_003_second_run_attempt_refused(cust_dir, binding_doc,
                                           event_package, launcher,
                                           auditor_exe, stage, cust_out):
    """run_attempt is single-issuance: after a successful run a second
    run_attempt is refused and neither gate re-executes."""
    sup, _ = fresh_run(cust_dir, binding_doc, event_package, launcher,
                       auditor_exe, stage, cust_out)
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    assert gate_count(nr_paths) == 1
    assert gate_count(rg_paths) == 1


def test_s1_003_freshness_observed_within_single_operation(
        cust_dir, binding_doc, event_package, launcher, auditor_exe, stage, cust_out):
    """The S1-003 RED scenario under the corrected authority path: a live
    resource state that has ALREADY deteriorated before the run is
    observed FRESH inside the single operation and blocks it — there is no
    earlier returned fresh PASS that can outlive the caller's delay."""
    write_rg_state(ATTEMPT, "pass")
    sup = build(cust_dir, binding_doc, event_package)
    write_rg_state(ATTEMPT, "fail-state")   # deteriorates BEFORE the run
    with pytest.raises(LaunchRefused, match="RESOURCE_GATE_RESULT_NOT_PASS"):
        sup.run_attempt(pipe_source(), str(launcher[0]),
                        str(auditor_exe[0]), stage, cust_out)
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert gate_count(rg_paths) == 1        # observed fresh, once
    assert gate_count(nr_paths) == 1
