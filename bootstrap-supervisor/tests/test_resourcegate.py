"""Runtime RESOURCE_GATE gate-timing tests (CR-EBS-S1-001).

Every gate executed here is the repository test fixture
tests/fixtures/inert_resource_gate.py — an unmistakably synthetic local
double whose behavior is driven by an EXTERNAL /tmp live-state file
keyed by attempt id (absent = honest PASS with three fresh PASS
samples).  No provider, no network, no real credential, no real event
package: the REAL AUCDEV-023 event package is NOT authorized, NOT
built, NOT committed.

Freshness matrix (gate-timing tasking §13):
  * a package-time RESOURCE_GATE PASS cannot exist in a valid binding;
  * the bound runtime-gate artifact is EXECUTED by the EBS exactly once
    during the live attempt, AFTER startup identity checks and BEFORE
    GATES_PASSED — there is no path from PREPARED to GATES_PASSED
    without the fresh execution;
  * live state that turns FAILING AFTER the freeze is observed FRESH
    and blocks GATES_PASSED;
  * every malformed/failed/oversized/wrong-context result blocks, with
    authority unconsumed and a durable TERMINAL_PREEXEC_STOP;
  * the GATES_PASSED record durably carries the fresh result evidence.
"""
import copy
import json
import os

import pytest

from ebs.accounting import AccountingStore, inspect_accounting_record
from ebs.binding import parse_binding
from ebs.launch import LaunchError, LaunchRefused, Supervisor, \
    verify_package_identity

from conftest import binding_for, make_event_package, rg_paths, seed_sha, \
    sha_hex, write_rg_state, clear_rg_tracks

ATTEMPT = "evt-0011223344556677-A-01"


@pytest.fixture(autouse=True)
def clean_rg_tracks():
    clear_rg_tracks(ATTEMPT)
    yield
    clear_rg_tracks(ATTEMPT)


def binding_and_store(cust_dir, doc):
    binding = parse_binding(json.dumps(doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    return binding, store


def rewrite_manifest(pkg_root, doc, mutate):
    """Apply mutate(manifest_dict), recompute the non-circular package
    identity, rewrite MANIFEST.json, and re-pin doc (isolates the
    manifest-level checks from raw-byte identity)."""
    manifest = json.loads((pkg_root / "MANIFEST.json").read_bytes())
    mutate(manifest)
    manifest.pop("package_sha256", None)
    manifest["package_sha256"] = sha_hex(json.dumps(
        manifest, sort_keys=True, separators=(",", ":")).encode())
    raw = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    (pkg_root / "MANIFEST.json").write_bytes(raw)
    doc["event_package"] = {"manifest_sha256": sha_hex(raw),
                            "package_sha256": manifest["package_sha256"]}


def fresh_pass(cust_dir, binding_doc, event_package):
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    sup.validate_gates()
    return sup, binding


# ---------------- frozen-vs-runtime gate separation (positive base) ----

def test_s1_001_fresh_pass_gate_reaches_gates_passed(cust_dir, binding_doc,
                                                     event_package):
    """GREEN base: a freshly EXECUTED gate with exactly three PASS
    samples — sampled live at execution time — reaches GATES_PASSED, and
    the execution actually happened (sentinel + count)."""
    sup, binding = fresh_pass(cust_dir, binding_doc, event_package)
    assert sup.state == "GATES_PASSED"
    _, sentinel, count = rg_paths(ATTEMPT)
    assert os.path.exists(sentinel)      # the gate REALLY executed
    with open(count) as handle:
        assert handle.read().strip() == "1"
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["last_state"] == "GATES_PASSED"


def test_s1_001_gate_executes_exactly_once(cust_dir, binding_doc,
                                           event_package):
    """Exactly-once: the bound artifact executes ONE time per attempt;
    a second validate_gates() call is refused outright and the execution
    count stays 1 (no same-attempt re-execution path exists)."""
    sup, binding = fresh_pass(cust_dir, binding_doc, event_package)
    with pytest.raises(LaunchError, match="GATES_ALREADY_EVALUATED"):
        sup.validate_gates()
    with open(rg_paths(ATTEMPT)[2]) as handle:
        assert handle.read().strip() == "1"


def test_s1_001_launcher_verification_requires_gates_passed(
        cust_dir, binding_doc, event_package, launcher):
    """Runtime ordering: launcher verification exists ONLY after the
    fresh resource-gate execution and the GATES_PASSED transition."""
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    assert sup.state == "PREPARED"
    with pytest.raises(LaunchError,
                       match="LAUNCHER_VERIFICATION_REQUIRES_GATES_PASSED"):
        sup.verify_launcher(str(launcher[0]))
    sup.validate_gates()
    assert sup.verify_launcher(str(launcher[0])) > 0


# ---------------- freshness: the core S1-001 criterion ----------------

def test_s1_001_live_state_fail_after_freeze_blocks_gates_passed(
        cust_dir, binding_doc, event_package):
    """THE S1-001 criterion: the package/binding freeze happens with a
    PASSING live resource state; the state then turns FAILING; the
    freshly executed gate OBSERVES the failure and blocks GATES_PASSED —
    no frozen PASS can satisfy the current resource state.  Authority
    stays unconsumed; the attempt terminalizes."""
    write_rg_state(ATTEMPT, "pass")           # healthy at freeze time
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)   # verified + held
    write_rg_state(ATTEMPT, "fail-state")     # live state degrades AFTER
    with pytest.raises(LaunchRefused,
                       match="RESOURCE_GATE_RESULT_NOT_PASS"):
        sup.validate_gates()
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["last_state"] == "TERMINAL_PREEXEC_STOP"
    assert "GATES_PASSED" not in view["states"]
    assert "CONSUMED_PRE_EXEC" not in view["states"]
    with open(rg_paths(ATTEMPT)[2]) as handle:
        assert handle.read().strip() == "1"   # executed exactly once


def test_s1_001_stale_pass_shape_cannot_exist_in_binding(binding_doc):
    """The OLD defect shape — a RESOURCE_GATE member inside the frozen
    gate_evidence — is structurally unrepresentable now: parse refuses
    it before anything else, and the surviving frozen gate set is
    exactly the six STATIC preparation gates."""
    doc = copy.deepcopy(binding_doc)
    doc["gate_evidence"]["RESOURCE_GATE"] = {
        "status": "PASS", "evidence_sha256": "0" * 64,
        "evidence_size": 64, "role": doc["auditor_role"],
        "attempt_id": doc["attempt_id"]}
    with pytest.raises(Exception,
                       match="GATE_EVIDENCE_RESOURCE_GATE_FORBIDDEN"):
        parse_binding(json.dumps(doc).encode())
    from ebs.binding import REQUIRED_GATES
    assert "RESOURCE_GATE" not in REQUIRED_GATES
    assert set(parse_binding(
        json.dumps(binding_doc).encode()).gate_evidence) == \
        set(REQUIRED_GATES)


# ---------------- malformed / failed result matrix (fail closed) ------

S1_001_MODES = [
    ("exit-nonzero", "RESOURCE_GATE_NONZERO_EXIT"),
    ("malformed", "RESOURCE_GATE_RESULT_MALFORMED"),
    ("dup-key", "RESOURCE_GATE_RESULT_MALFORMED"),
    ("wrong-schema", "RESOURCE_GATE_RESULT_SCHEMA_UNEXPECTED"),
    ("wrong-event", "RESOURCE_GATE_RESULT_CONTEXT_MISMATCH"),
    ("wrong-role", "RESOURCE_GATE_RESULT_CONTEXT_MISMATCH"),
    ("wrong-attempt", "RESOURCE_GATE_RESULT_CONTEXT_MISMATCH"),
    ("fail-status", "RESOURCE_GATE_RESULT_NOT_PASS"),
    ("sample-fail", "RESOURCE_GATE_SAMPLE_NOT_PASS"),
    ("sample-count-2", "RESOURCE_GATE_SAMPLE_COUNT_INVALID"),
    ("sample-count-4", "RESOURCE_GATE_SAMPLE_COUNT_INVALID"),
    ("empty-output", "RESOURCE_GATE_OUTPUT_MISSING"),
    ("oversized", "RESOURCE_GATE_OUTPUT_TOO_LARGE"),
]


@pytest.mark.parametrize("mode,refusal", S1_001_MODES,
                         ids=[case[0] for case in S1_001_MODES])
def test_s1_001_mode_matrix_blocks_before_gates_passed(
        cust_dir, binding_doc, event_package, mode, refusal):
    """Every malformed / failed / wrong-context fresh result blocks
    GATES_PASSED (fail closed): authority unconsumed, durable
    TERMINAL_PREEXEC_STOP, exactly one execution, no CONSUMED/EXEC
    record.  A top-level PASS never overrides a failed sample; PASS is
    never inferred from the exit code alone (exit-nonzero prints a
    perfectly VALID envelope and is still refused)."""
    write_rg_state(ATTEMPT, mode)
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    with pytest.raises(LaunchRefused, match=refusal):
        sup.validate_gates()
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["last_state"] == "TERMINAL_PREEXEC_STOP"
    assert "GATES_PASSED" not in view["states"]
    assert "CONSUMED_PRE_EXEC" not in view["states"]
    assert "EXEC_ATTEMPTED" not in view["states"]


def test_s1_001_hang_is_bounded_and_blocks(cust_dir, binding_doc,
                                           event_package):
    """A hung gate process is NOT an unbounded authority process: the
    deterministic bounded timeout kills it and fails closed."""
    import time
    write_rg_state(ATTEMPT, "hang")
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    started = time.monotonic()
    with pytest.raises(LaunchRefused, match="RESOURCE_GATE_TIMEOUT"):
        sup.validate_gates()
    assert time.monotonic() - started < 60     # bounded, not hung forever
    assert sup.state == "TERMINAL_PREEXEC_STOP"


# ---------------- artifact identity / held-fd discipline --------------

def test_s1_001_gate_artifact_digest_mismatch_refused(
        cust_dir, binding_doc, event_package, tmp_path):
    """A REGENERATED self-consistent package (pins updated) whose LIVE
    gate artifact bytes differ from the binding's runtime-gate
    descriptor SHA-256 — while the manifest projection still declares
    the ORIGINAL descriptor — is refused at gate-artifact identity
    verification, BEFORE GATES_PASSED, record PREPARED."""
    doc = copy.deepcopy(binding_doc)
    gate = event_package / "runtime" / "resource-gate.py"
    gate.write_text(gate.read_text() + "\n# one-byte-class change\n")
    os.chmod(gate, 0o755)
    rewrite_manifest(event_package, doc,
                     lambda m: m["files"].__setitem__(
                         next(i for i, row in enumerate(m["files"])
                              if row["path"] == "runtime/resource-gate.py"),
                         {"path": "runtime/resource-gate.py",
                          "bytes": gate.stat().st_size,
                          "sha256": sha_hex(gate.read_bytes())}))
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused,
                       match="RESOURCE_GATE_ARTIFACT_DIGEST_MISMATCH"):
        Supervisor(binding, store, event_package)
    assert inspect_accounting_record(
        cust_dir, binding.attempt_id, binding.digest)["last_state"] \
        == "PREPARED"


def test_s1_001_gate_path_not_a_manifest_row_refused(
        cust_dir, binding_doc, event_package, tmp_path):
    """A descriptor path that is no manifest row of the verified package
    (here: a SECOND valid package carrying a differently-named gate) is
    refused — the executed artifact must be package-manifest-covered."""
    doc = copy.deepcopy(binding_doc)
    doc["runtime_gates"]["RESOURCE_GATE"]["path"] = \
        "runtime/other-resource-gate.py"
    pkg2 = make_event_package(doc, tmp_path, name="pkg-other-path")
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused,
                       match="RESOURCE_GATE_NOT_PACKAGE_MANIFEST_ROW"):
        Supervisor(binding, store, pkg2)


def test_s1_001_held_fd_drift_refused(cust_dir, binding_doc,
                                      event_package):
    """The held verified fd is RE-HASHED immediately before execution:
    in-place artifact mutation after startup (same inode, so the held
    fd now reads DIFFERENT bytes) fails closed as fd drift — the bytes
    that execute are exactly the bytes the binding freezes."""
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)   # verified + held
    gate = event_package / "runtime" / "resource-gate.py"
    gate.write_text(gate.read_text() + "\n# post-verification drift\n")
    with pytest.raises(LaunchRefused, match="RESOURCE_GATE_FD_DRIFT"):
        sup.validate_gates()
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    assert not os.path.exists(rg_paths(ATTEMPT)[1])   # never executed


def test_s1_001_gate_symlink_refused(cust_dir, binding_doc, event_package,
                                     tmp_path):
    """A symlinked gate artifact is refused BEFORE gates: the shared
    package verifier's exact payload-set/regular-file walk refuses it
    first (the O_NOFOLLOW verified open in open_runtime_gate remains as
    defense-in-depth behind that layer)."""
    doc = copy.deepcopy(binding_doc)
    gate = event_package / "runtime" / "resource-gate.py"
    data = gate.read_bytes()
    gate.unlink()
    (tmp_path / "outside-gate.py").write_bytes(data)
    gate.symlink_to(tmp_path / "outside-gate.py")
    rewrite_manifest(event_package, doc, lambda m: None)  # identity only
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD"):
        Supervisor(binding, store, event_package)
    assert inspect_accounting_record(
        cust_dir, binding.attempt_id, binding.digest)["last_state"] \
        == "PREPARED"


def test_s1_001_gate_not_executable_refused(cust_dir, binding_doc,
                                            event_package):
    """A non-executable gate artifact (mode without any x bit) is
    refused at startup: the bound artifact must be executable for the
    verified-fd exec to be possible at all."""
    doc = copy.deepcopy(binding_doc)
    gate = event_package / "runtime" / "resource-gate.py"
    os.chmod(gate, 0o644)
    rewrite_manifest(event_package, doc, lambda m: None)
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused, match="RESOURCE_GATE_NOT_EXECUTABLE"):
        Supervisor(binding, store, event_package)


# ---------------- no-retry / accounting failure ------------------------

def test_s1_001_failed_gate_cannot_retry_same_attempt(
        cust_dir, binding_doc, event_package):
    """After a gate failure there is NO same-attempt retry: the second
    validate_gates() is refused by state (TERMINAL_PREEXEC_STOP is
    absorbing) and the execution count stays 1."""
    write_rg_state(ATTEMPT, "fail-status")
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    with pytest.raises(LaunchRefused):
        sup.validate_gates()
    with pytest.raises(LaunchError, match="GATES_ALREADY_EVALUATED"):
        sup.validate_gates()
    with open(rg_paths(ATTEMPT)[2]) as handle:
        assert handle.read().strip() == "1"


def test_s1_001_result_persistence_failure_blocks(cust_dir, binding_doc,
                                                  event_package,
                                                  monkeypatch):
    """A GATES_PASSED record-persistence failure AFTER a fresh gate PASS
    still blocks GATES_PASSED (no in-memory transition), terminalizes,
    and permits no same-attempt retry (the exactly-once guard)."""
    from ebs.accounting import AccountingError
    original = AccountingStore.append

    def refusing_append(self, state, extra=None):
        if state == "GATES_PASSED":
            raise AccountingError("injected durability failure")
        return original(self, state, extra=extra)

    monkeypatch.setattr(AccountingStore, "append", refusing_append)
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    with pytest.raises(LaunchRefused, match="RESOURCE_GATE_RECORD_FAILED"):
        sup.validate_gates()
    monkeypatch.undo()
    assert sup.state == "TERMINAL_PREEXEC_STOP"
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert "GATES_PASSED" not in view["states"]
    with pytest.raises(LaunchError, match="GATES_ALREADY_EVALUATED"):
        sup.validate_gates()
    with open(rg_paths(ATTEMPT)[2]) as handle:
        assert handle.read().strip() == "1"


# ---------------- durable fresh-evidence record ------------------------

def test_s1_001_gates_passed_record_carries_fresh_result_evidence(
        cust_dir, binding_doc, event_package):
    """The durable GATES_PASSED record carries the bound gate identity,
    gate SHA-256, result schema, and the canonical validated result
    JSON + its exact SHA-256 and byte size — mechanically bound to the
    recorded digest."""
    sup, binding = fresh_pass(cust_dir, binding_doc, event_package)
    descriptor = binding.runtime_gates["RESOURCE_GATE"]
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    record = view["records"][-1]
    assert record["state"] == "GATES_PASSED"
    assert record["resource_gate_identity"] == descriptor["identity"]
    assert record["resource_gate_sha256"] == descriptor["sha256"]
    assert record["resource_gate_result_schema"] == \
        descriptor["result_schema"]
    result = json.loads(record["resource_gate_result"])
    assert result["schema"] == descriptor["result_schema"]
    assert result["status"] == "PASS"
    assert result["event_id"] == binding.event_id
    assert result["auditor_role"] == binding.auditor_role
    assert result["attempt_id"] == binding.attempt_id
    assert len(result["samples"]) == 3
    canonical = json.dumps(result, sort_keys=True,
                           separators=(",", ":")).encode()
    assert record["resource_gate_result_size"] == len(canonical)
    assert record["resource_gate_result_sha256"] == sha_hex(canonical)


def test_s1_001_no_consumption_during_gate_tests(cust_dir, binding_doc,
                                                 event_package):
    """Gate-only operation: no CONSUMED_PRE_EXEC / EXEC_ATTEMPTED record
    and no launch authority exists anywhere in the gate lifecycle (the
    gate itself is NOT a provider/model engagement)."""
    fresh_pass(cust_dir, binding_doc, event_package)
    binding = parse_binding(json.dumps(binding_doc).encode())
    view = inspect_accounting_record(cust_dir, binding.attempt_id,
                                     binding.digest)
    assert view["states"] == ["PREPARED", "GATES_PASSED"]
    assert "CONSUMED_PRE_EXEC" not in view["states"]
    assert "EXEC_ATTEMPTED" not in view["states"]


def test_s1_001_verified_gate_layer_uses_shared_verifier(binding_doc,
                                                         event_package):
    """The runtime-gate artifact is covered by the SAME package identity
    verification (no second verifier): verify_package_identity alone
    authenticates the gate bytes recorded in the manifest."""
    result = verify_package_identity(
        event_package,
        binding_doc["event_package"]["manifest_sha256"],
        binding_doc["event_package"]["package_sha256"])
    rows = {row["path"] for row in result["document"]["files"]}
    assert binding_doc["runtime_gates"]["RESOURCE_GATE"]["path"] in rows
