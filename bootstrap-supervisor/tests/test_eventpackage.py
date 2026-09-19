"""Frozen event-package cross-binding tests (CR-EBS-REM-001).

Every event package in this file is an unmistakably SYNTHETIC/INERT
temporary tree built by conftest.make_event_package under a pytest
tmp_path — the REAL AUCDEV-023 event package is NOT authorized, NOT
built, NOT committed.  No provider, no network, no real credential.

Matrix (second-remediation tasking §11):
  PROJECTION CONTRACT  binding_projection covers every binding security
                       dimension EXCEPT event_package (non-circular).
  POSITIVE             exact synthetic package + exact binding ->
                       Supervisor constructs; GATES_PASSED reachable.
  PACKAGE IDENTITY     wrong pins / byte / payload / missing / stale /
                       unrecorded / symlink mutations -> refused.
  BINDING->PACKAGE     internally-valid binding component substitution
                       under the SAME frozen event-package identity ->
                       EVENT_PACKAGE_PROJECTION_MISMATCH (never a mere
                       syntax refusal; parse succeeds first).
  PACKAGE->BINDING     regenerated self-consistent package with one
                       changed projection component AND updated pins ->
                       still EVENT_PACKAGE_PROJECTION_MISMATCH.
  TARGET               self-consistent package declaring a different
                       frozen target, pins updated -> refused.
  SCHEMA               unknown/missing manifest key, wrong schema tag,
                       duplicate JSON key, missing/unknown projection
                       field -> refused.
  ORDERING / MANDATORY startup order EBS -> store -> package identity ->
                       projection -> gates; event-package root has no
                       default and no bypass.
  ROW TYPE (REM2-001)   files[].bytes must be an EXACT non-negative int
                        (bool explicitly refused) at manifest-row
                        validation, BEFORE GATES_PASSED.
  GATE TIMING (S1-001)  manifest schema is V2 (V1 refused); the
                        projection covers the runtime_gates descriptor;
                        runtime-gate descriptor substitutions in EITHER
                        direction are refused as projection mismatches.
"""
import copy
import json

import pytest

from ebs.accounting import AccountingStore, inspect_accounting_record
from ebs.binding import (PROJECTION_FIELDS, TOP_LEVEL, attempt_id_for,
                         binding_projection, output_name_for, parse_binding)
from ebs.launch import LaunchError, LaunchRefused, Supervisor, \
    verify_event_package, verify_package_identity

from conftest import EVENT_PKG_MARKER, binding_for, make_event_package, \
    seed_sha, sha_hex

ALT = seed_sha("crossbind-alternate", "dimension")   # a valid 64-hex digest


def binding_and_store(cust_dir, doc):
    binding = parse_binding(json.dumps(doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    return binding, store


def rewrite_manifest(pkg_root, doc, mutate):
    """Apply mutate(manifest_dict), recompute the non-circular package
    identity, rewrite MANIFEST.json, and re-pin doc — isolating the
    manifest-level checks from raw-byte identity (the mutation would
    otherwise be refused at the manifest digest first)."""
    manifest = json.loads((pkg_root / "MANIFEST.json").read_bytes())
    mutate(manifest)
    manifest.pop("package_sha256", None)
    manifest["package_sha256"] = sha_hex(json.dumps(
        manifest, sort_keys=True, separators=(",", ":")).encode())
    raw = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    (pkg_root / "MANIFEST.json").write_bytes(raw)
    doc["event_package"] = {"manifest_sha256": sha_hex(raw),
                            "package_sha256": manifest["package_sha256"]}


def recombined(doc, event_id):
    """Repair ALL internal attempt/output/gate consistency for a new
    event id (the substitution stays an INTERNALLY VALID binding)."""
    attempt = attempt_id_for(event_id, doc["auditor_role"])
    doc["event_id"] = event_id
    doc["attempt_id"] = attempt
    doc["output_identity"]["name"] = output_name_for(attempt)
    for gate in doc["gate_evidence"].values():
        gate["attempt_id"] = attempt


# ---------------- projection contract ----------------

def test_projection_covers_every_dimension_except_event_package(
        parsed_binding):
    """The projection is EXACTLY the complete binding dimension set minus
    the event-package self-identity pair (non-circular construction)."""
    assert set(PROJECTION_FIELDS) == set(TOP_LEVEL) - {"event_package"}
    projection = binding_projection(parsed_binding)
    assert set(projection) == set(PROJECTION_FIELDS)
    assert projection["boundary_launcher"] == \
        parsed_binding.boundary_launcher
    assert projection["gate_evidence"] == parsed_binding.gate_evidence
    assert projection["target"] == parsed_binding.target
    assert "event_package" not in projection


def test_event_package_fixture_is_unmistakably_synthetic(event_package):
    assert EVENT_PKG_MARKER.startswith(b"EBS-SYNTHETIC-INERT")
    assert b"NOT-A-REAL-EVENT-PACKAGE" in EVENT_PKG_MARKER
    assert (event_package / "SYNTHETIC-INERT-MARKER.txt").read_bytes() \
        == EVENT_PKG_MARKER


# ---------------- positive ----------------

def test_exact_synthetic_package_reaches_gates_passed(cust_dir, binding_doc,
                                                      event_package):
    result = verify_event_package(event_package,
                                  parse_binding(json.dumps(
                                      binding_doc).encode()))
    assert result["files"] == 4   # marker + 2 transport + runtime gate
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    sup.validate_gates()
    assert sup.state == "GATES_PASSED"


def test_positive_path_through_consumption(launcher, cust_dir, binding_doc,
                                           event_package):
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    sup.validate_gates()
    sup.verify_launcher(str(launcher[0]))
    sup.consume()
    assert sup.state == "CONSUMED_PRE_EXEC"


# ---------------- package identity (against the pins) ----------------

def test_wrong_event_manifest_pin_refused(cust_dir, binding_doc,
                                          event_package):
    doc = copy.deepcopy(binding_doc)
    doc["event_package"]["manifest_sha256"] = "6" * 64
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused, match="LIVE_MANIFEST_IDENTITY"):
        Supervisor(binding, store, event_package)


def test_wrong_event_package_pin_refused(cust_dir, binding_doc,
                                         event_package):
    doc = copy.deepcopy(binding_doc)
    doc["event_package"]["package_sha256"] = "7" * 64
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused, match="EBS_PACKAGE_IDENTITY"):
        Supervisor(binding, store, event_package)


def test_event_manifest_byte_mutation_refused(cust_dir, binding_doc,
                                              event_package):
    path = event_package / "MANIFEST.json"
    path.write_bytes(path.read_bytes() + b"\n")   # whitespace-only byte
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="LIVE_MANIFEST_IDENTITY"):
        Supervisor(binding, store, event_package)


def test_event_payload_mutation_refused(cust_dir, binding_doc,
                                        event_package):
    (event_package / "SYNTHETIC-INERT-MARKER.txt").write_bytes(
        EVENT_PKG_MARKER + b"-mutated")
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD_MISMATCH"):
        Supervisor(binding, store, event_package)


def test_event_payload_missing_refused(cust_dir, binding_doc,
                                       event_package):
    (event_package / "transport" / "prompt-contract.json").unlink()
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD_MISSING"):
        Supervisor(binding, store, event_package)


def test_event_stale_row_refused(cust_dir, binding_doc, event_package):
    def add_stale_row(manifest):
        manifest["files"].append({"path": "never-shipped.txt", "bytes": 1,
                                  "sha256": "0" * 64})
    rewrite_manifest(event_package, binding_doc, add_stale_row)
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD_MISSING"):
        Supervisor(binding, store, event_package)


def test_event_unrecorded_payload_refused(cust_dir, binding_doc,
                                          event_package):
    (event_package / "attacker-payload.json").write_text("{}")
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD_UNRECORDED"):
        Supervisor(binding, store, event_package)


def test_event_symlink_payload_refused(cust_dir, binding_doc, tmp_path,
                                       event_package):
    victim = event_package / "SYNTHETIC-INERT-MARKER.txt"
    data = victim.read_bytes()
    victim.unlink()
    (tmp_path / "outside-marker.txt").write_bytes(data)
    victim.symlink_to(tmp_path / "outside-marker.txt")
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD"):
        Supervisor(binding, store, event_package)


# ---------------- strict versioned manifest schema ----------------

def test_event_manifest_unknown_key_refused(cust_dir, binding_doc,
                                            event_package):
    rewrite_manifest(event_package, binding_doc,
                     lambda m: m.update(extra_dimension="x"))
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="EVENT_MANIFEST_KEYS_INVALID"):
        Supervisor(binding, store, event_package)


def test_event_manifest_missing_key_refused(cust_dir, binding_doc,
                                            event_package):
    rewrite_manifest(event_package, binding_doc,
                     lambda m: m.pop("schema"))
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="EVENT_MANIFEST_KEYS_INVALID"):
        Supervisor(binding, store, event_package)


def test_event_manifest_wrong_schema_refused(cust_dir, binding_doc,
                                             event_package):
    rewrite_manifest(event_package, binding_doc,
                     lambda m: m.update(
                         schema="AUCDEV-023-EVENT-PACKAGE-MANIFEST-V0"))
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="EVENT_MANIFEST_SCHEMA"):
        Supervisor(binding, store, event_package)


def test_event_manifest_v1_schema_refused(cust_dir, binding_doc,
                                          event_package):
    """S1-001: the manifest schema advanced to V2 (the projection
    semantics materially changed — RESOURCE_GATE left the frozen
    evidence set and the runtime-gate descriptor became a bound
    dimension); a self-consistent V1 package with matching pins is
    refused, never silently accepted as equivalent."""
    rewrite_manifest(event_package, binding_doc,
                     lambda m: m.update(
                         schema="AUCDEV-023-EVENT-PACKAGE-MANIFEST-V1"))
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused, match="EVENT_MANIFEST_SCHEMA"):
        Supervisor(binding, store, event_package)
    assert inspect_accounting_record(
        cust_dir, binding.attempt_id, binding.digest)["last_state"] \
        == "PREPARED"


def test_event_manifest_duplicate_key_refused(cust_dir, binding_doc,
                                              event_package):
    """A duplicate top-level manifest key is refused by the STRICT parse
    even when the collapsed document is perfectly self-consistent and
    both pins match the poisoned raw bytes."""
    manifest = json.loads((event_package / "MANIFEST.json").read_bytes())
    collapsed = dict(manifest)
    collapsed["schema"] = "DUP-LAST-WINS"          # last-wins duplicate
    collapsed.pop("package_sha256")
    collapsed["package_sha256"] = sha_hex(json.dumps(
        collapsed, sort_keys=True, separators=(",", ":")).encode())
    body = json.dumps(collapsed, sort_keys=True, separators=(",", ":"))
    raw = ('{"schema":"AUCDEV-023-EVENT-PACKAGE-MANIFEST-V2",'
           + body[1:]).encode()                    # "schema" appears twice
    (event_package / "MANIFEST.json").write_bytes(raw)
    doc = copy.deepcopy(binding_doc)
    doc["event_package"] = {"manifest_sha256": sha_hex(raw),
                            "package_sha256": collapsed["package_sha256"]}
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused, match="PACKAGE_MANIFEST_MALFORMED"):
        Supervisor(binding, store, event_package)


# ---------------- BINDING -> PACKAGE cross-bind (core criterion) ----------------

BINDING_MUTATIONS = [
    ("recombined-event-attempt-output",
     lambda d: recombined(d, "evt-0011223344556801")),
    ("prompt-contract-digest",
     lambda d: d.update(prompt_contract_digest=ALT)),
    ("common-evidence-digest-with-parity-repair",
     lambda d: (d.update(common_evidence_manifest_digest=ALT),
                d["gate_evidence"]["COMMON_EVIDENCE_PARITY"].update(
                    evidence_sha256=ALT))),
    ("alternate-allowed-launcher-identity",
     lambda d: d["boundary_launcher"].update(
         identity="NETWORKED-BOUNDARY-LAUNCHER-V1")),
    ("alternate-valid-launcher-hash",
     lambda d: d["boundary_launcher"].update(sha256=ALT)),
    ("alternate-safe-sandbox-profile",
     lambda d: d.update(sandbox_profile_id=
                        "SYNTHETIC-INERT-LOCAL-SANDBOX-V2")),
    ("alternate-role-valid-adapter",
     lambda d: d["auditor_identity"].update(
         adapter_id="claude_firstparty_oauth_v1")),
    ("alternate-auditor-executable-identity",
     lambda d: d["auditor_identity"].update(
         executable_identity="SYNTHETIC-INERT-AUDITOR_A-EXECUTABLE-V2")),
    ("alternate-auditor-executable-hash",
     lambda d: d["auditor_identity"].update(executable_sha256=ALT)),
    ("alternate-tool-wrapper-identity",
     lambda d: d["tool_wrapper"].update(
         identity="SYNTHETIC-INERT-TOOL-WRAPPER-V2")),
    ("alternate-tool-wrapper-hash",
     lambda d: d["tool_wrapper"].update(sha256=ALT)),
    ("altered-gate-evidence",
     lambda d: d["gate_evidence"]["GATE_W_PRIME"].update(
         evidence_sha256=seed_sha("crossbind-alternate", "gate"))),
    ("altered-runtime-gate-identity",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         identity="SYNTHETIC-INERT-RESOURCE-GATE-V2")),
    ("altered-runtime-gate-sha",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         sha256=seed_sha("crossbind-alternate", "runtime-gate"))),
    ("altered-runtime-gate-path",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         path="runtime/resource-gate-alt.py")),
]


@pytest.mark.parametrize("name,mutate", BINDING_MUTATIONS,
                         ids=[c[0] for c in BINDING_MUTATIONS])
def test_same_package_identity_component_substitution_refused(
        cust_dir, binding_doc, event_package, name, mutate):
    """CORE CR-EBS-REM-001 acceptance criterion: an INTERNALLY VALID
    binding (parse succeeds) carrying substituted component identities
    while RETAINING the SAME frozen event-package identity is refused by
    the event-package cross-binding — not by binding syntax — BEFORE
    GATES_PASSED (durable record stays PREPARED)."""
    doc = copy.deepcopy(binding_doc)
    mutate(doc)
    binding = parse_binding(json.dumps(doc).encode())   # must STILL parse
    assert binding.event_package == parse_binding(
        json.dumps(binding_doc).encode()).event_package
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    with pytest.raises(LaunchRefused,
                       match="EVENT_PACKAGE_PROJECTION_MISMATCH"):
        Supervisor(binding, store, event_package)
    assert inspect_accounting_record(
        cust_dir, binding.attempt_id, binding.digest)["last_state"] \
        == "PREPARED"


def test_ebs_package_substitution_refused_at_live_layer(
        cust_dir, binding_doc, event_package):
    """An EBS-package substitution in the binding is refused FIRST by the
    live self-verification layer (any valid binding must pin the LIVE
    bytes); the projection covers ebs_package as well, proven by the
    regenerated-package direction below."""
    doc = copy.deepcopy(binding_doc)
    doc["ebs_package"] = {"manifest_sha256": seed_sha("alt", "m"),
                          "package_sha256": seed_sha("alt", "p")}
    binding = parse_binding(json.dumps(doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    with pytest.raises(LaunchRefused, match="LIVE_MANIFEST_IDENTITY"):
        Supervisor(binding, store, event_package)


# ---------------- PACKAGE -> BINDING cross-bind (regenerated manifest) ----------------

PACKAGE_MUTATIONS = [
    ("launcher-identity",
     lambda p: p["boundary_launcher"].update(
         identity="NETWORKED-BOUNDARY-LAUNCHER-V1")),
    ("sandbox-profile-id",
     lambda p: p.update(sandbox_profile_id=
                        "SYNTHETIC-INERT-LOCAL-SANDBOX-V2")),
    ("prompt-contract-digest",
     lambda p: p.update(prompt_contract_digest=ALT)),
    ("target-commit",
     lambda p: p["target"].update(commit="0" * 40)),
    ("ebs-package-identity",
     lambda p: p["ebs_package"].update(package_sha256=ALT)),
    ("gate-evidence",
     lambda p: p["gate_evidence"]["GATE_W_PRIME"].update(
         evidence_sha256=seed_sha("crossbind-alternate", "gate"))),
    ("runtime-gate-descriptor-identity",
     lambda p: p["runtime_gates"]["RESOURCE_GATE"].update(
         identity="SYNTHETIC-INERT-RESOURCE-GATE-V2")),
    ("runtime-gate-descriptor-sha",
     lambda p: p["runtime_gates"]["RESOURCE_GATE"].update(
         sha256=seed_sha("crossbind-alternate", "runtime-gate"))),
    ("runtime-gate-descriptor-path",
     lambda p: p["runtime_gates"]["RESOURCE_GATE"].update(
         path="runtime/resource-gate-alt.py")),
    ("runtime-gate-descriptor-result-schema",
     lambda p: p["runtime_gates"]["RESOURCE_GATE"].update(
         result_schema="AUCDEV-023-RESOURCE-GATE-RESULT-V0")),
    ("missing-projection-field",
     lambda p: p.pop("sandbox_profile_id")),
    ("unknown-projection-field",
     lambda p: p.update(rogue_dimension="x")),
]


@pytest.mark.parametrize("name,mutate", PACKAGE_MUTATIONS,
                         ids=[c[0] for c in PACKAGE_MUTATIONS])
def test_regenerated_package_projection_mismatch_refused(
        tmp_path, binding_doc, name, mutate):
    """The OTHER direction: a regenerated, perfectly self-consistent
    synthetic event package whose manifest projection declares a
    different component (or a missing/unknown projection field), with the
    Binding's event_package pins UPDATED to the new package identity and
    the corresponding Binding component LEFT UNCHANGED — the package
    identity now matches, but the projection does not, so the Supervisor
    still refuses.  This separates package-identity verification from
    component cross-binding.  The target-commit case proves a
    self-consistent package declaring a DIFFERENT frozen target is
    refused against the fixed Binding."""
    doc = copy.deepcopy(binding_doc)
    pkg = make_event_package(doc, tmp_path, name="pkg-regenerated",
                             projection_mutator=mutate)
    binding = parse_binding(json.dumps(doc).encode())
    cust = tmp_path / "cust"
    cust.mkdir(mode=0o700)
    store = AccountingStore.create(cust, binding.attempt_id, binding.digest)
    with pytest.raises(LaunchRefused,
                       match="EVENT_PACKAGE_PROJECTION_MISMATCH"):
        Supervisor(binding, store, pkg)


# ---------------- startup ordering / mandatory input ----------------

def test_startup_order_ebs_self_identity_first(cust_dir, tmp_path, launcher):
    doc = binding_for(launcher[1])
    doc["ebs_package"] = {"manifest_sha256": "4" * 64,
                          "package_sha256": "5" * 64}
    binding = parse_binding(json.dumps(doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    with pytest.raises(LaunchRefused, match="LIVE_MANIFEST_IDENTITY"):
        Supervisor(binding, store,
                   tmp_path / "nonexistent-event-package")


def test_startup_order_store_binding_before_event_package(
        cust_dir, binding_doc, tmp_path):
    binding = parse_binding(json.dumps(binding_doc).encode())
    store = AccountingStore.create(cust_dir, "evt-0011223344556677-B-01",
                                   binding.digest)
    with pytest.raises(LaunchError, match="STORE_ATTEMPT_MISMATCH"):
        Supervisor(binding, store, tmp_path / "nonexistent-event-package")


def test_identity_precedes_projection_in_event_verification(
        cust_dir, binding_doc, event_package):
    """Within event verification the pinned identity is established
    BEFORE the projection comparison (a package failing BOTH reports the
    identity refusal)."""
    doc = copy.deepcopy(binding_doc)
    doc["sandbox_profile_id"] = "SYNTHETIC-INERT-LOCAL-SANDBOX-V2"
    doc["event_package"]["manifest_sha256"] = "8" * 64
    binding, store = binding_and_store(cust_dir, doc)
    with pytest.raises(LaunchRefused, match="LIVE_MANIFEST_IDENTITY"):
        Supervisor(binding, store, event_package)


def test_event_package_input_is_mandatory(cust_dir, binding_doc):
    """The event-package root is a REQUIRED supervisor input: no default
    value exists (statically asserted) and non-path inputs are refused."""
    import inspect as pyinspect
    params = pyinspect.signature(Supervisor.__init__).parameters
    assert "event_package_root" in params
    assert params["event_package_root"].default is pyinspect.Parameter.empty
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchError, match="SUPERVISOR_REQUIRES_EVENT"):
        Supervisor(binding, store, None)
    with pytest.raises(LaunchError, match="SUPERVISOR_REQUIRES_EVENT"):
        Supervisor(binding, store, 123)


# ---------------- REM2-001: files[].bytes exact row-type contract ----------------

REM2_ONE_BYTE = b"R"      # a REAL one-byte payload
REM2_ROW_BYTES_CASES = [
    ("bool-true-one-byte", True, REM2_ONE_BYTE),
    ("float-one-dot-zero-one-byte", 1.0, REM2_ONE_BYTE),
    ("string-one-one-byte", "1", REM2_ONE_BYTE),
    ("negative-int", -1, REM2_ONE_BYTE),
    ("bool-false-zero-byte", False, b""),
    ("none-one-byte", None, REM2_ONE_BYTE),
    ("list-one-byte", [1], REM2_ONE_BYTE),
    ("dict-one-byte", {"bytes": 1}, REM2_ONE_BYTE),
    ("float-wrong-value-one-byte", 2.0, REM2_ONE_BYTE),
    ("empty-string-one-byte", "", REM2_ONE_BYTE),
]


def add_payload_row(pkg_root, rel, data, row_bytes):
    """Materialize a REAL payload of exactly len(data) live bytes whose
    manifest row carries a CORRECT sha256 but the (possibly type-invalid)
    recorded byte count row_bytes; the regenerated package identity is
    re-pinned by rewrite_manifest, so only the recorded TYPE differs."""
    (pkg_root / rel).write_bytes(data)

    def mutate(manifest):
        manifest["files"].append({"path": rel, "bytes": row_bytes,
                                  "sha256": sha_hex(data)})
    return mutate


@pytest.mark.parametrize("name,row_bytes,payload", REM2_ROW_BYTES_CASES,
                         ids=[case[0] for case in REM2_ROW_BYTES_CASES])
def test_rem2_001_manifest_row_bytes_type_refused_before_gates_passed(
        cust_dir, binding_doc, event_package, name, row_bytes, payload):
    """REM2-001: a self-consistent, correctly re-pinned synthetic package
    whose manifest row byte count is NOT an exact non-negative int (bool
    explicitly included) is refused at manifest-ROW validation BEFORE
    GATES_PASSED; the durable record stays PREPARED.  The live payload
    size and hash are EXACT for the row, so nothing but the recorded TYPE
    can fail: for bytes=true/false/1.0 the size comparison is numerically
    equal (True == 1, False == 0, 1.0 == 1), for the other values the
    refusal must still come from row validation, not the later payload
    comparison."""
    mutate = add_payload_row(event_package, "rem2-payload.bin", payload,
                             row_bytes)
    rewrite_manifest(event_package, binding_doc, mutate)
    binding, store = binding_and_store(cust_dir, binding_doc)
    with pytest.raises(LaunchRefused,
                       match="PACKAGE_MANIFEST_ROW_BYTES_TYPE_INVALID"):
        Supervisor(binding, store, event_package)
    assert inspect_accounting_record(
        cust_dir, binding.attempt_id, binding.digest)["last_state"] \
        == "PREPARED"


@pytest.mark.parametrize("row_bytes", [True, 1.0, "1"],
                         ids=["bool", "float", "string"])
def test_rem2_001_row_type_refusal_is_at_row_validation(
        binding_doc, event_package, row_bytes):
    """The refusal comes from manifest-ROW validation, not the tree walk
    or any gate: verify_package_identity ITSELF (no store, no gates
    surface) refuses the malformed row against freshly re-pinned
    identities."""
    mutate = add_payload_row(event_package, "rem2-payload.bin",
                             REM2_ONE_BYTE, row_bytes)
    rewrite_manifest(event_package, binding_doc, mutate)
    with pytest.raises(LaunchRefused,
                       match="PACKAGE_MANIFEST_ROW_BYTES_TYPE_INVALID"):
        verify_package_identity(
            event_package,
            binding_doc["event_package"]["manifest_sha256"],
            binding_doc["event_package"]["package_sha256"])


def test_rem2_001_manifest_row_bytes_valid_int_control_accepted(
        cust_dir, binding_doc, event_package):
    """Positive control: exact INTEGER byte counts remain ACCEPTED —
    including bytes=0 for a REAL zero-byte regular payload and bytes=1
    for a one-byte payload; the strict rule refuses only non-int, bool,
    and negative values."""
    (event_package / "rem2-zero-byte.bin").write_bytes(b"")
    (event_package / "rem2-one-byte.bin").write_bytes(REM2_ONE_BYTE)

    def mutate(manifest):
        manifest["files"] += [
            {"path": "rem2-zero-byte.bin", "bytes": 0,
             "sha256": sha_hex(b"")},
            {"path": "rem2-one-byte.bin", "bytes": 1,
             "sha256": sha_hex(REM2_ONE_BYTE)}]
    rewrite_manifest(event_package, binding_doc, mutate)
    binding, store = binding_and_store(cust_dir, binding_doc)
    sup = Supervisor(binding, store, event_package)
    sup.validate_gates()
    assert sup.state == "GATES_PASSED"
