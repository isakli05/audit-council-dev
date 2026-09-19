"""Binding contract tests (task §24 negative matrix + positives)."""
import copy
import json

import pytest

from ebs.binding import (FROZEN_TARGET, POLICY_ID, REQUIRED_GATES,
                         BindingError, parse_binding)

from conftest import sha_hex


def parse(doc):
    return parse_binding(json.dumps(doc).encode())


def test_valid_synthetic_binding_accepted(binding_doc, parsed_binding):
    assert parsed_binding.policy_id == POLICY_ID
    assert parsed_binding.target == FROZEN_TARGET
    assert parsed_binding.digest == sha_hex(
        json.dumps(binding_doc, sort_keys=True, separators=(",", ":")).encode())
    assert set(parsed_binding.gate_evidence) == set(REQUIRED_GATES)


def test_binding_binds_every_required_field_class(parsed_binding):
    b = parsed_binding
    for name in ("policy_id", "event_id", "auditor_role", "attempt_id",
                 "common_evidence_manifest_digest", "prompt_contract_digest",
                 "sandbox_profile_id"):
        assert isinstance(getattr(b, name), str) and getattr(b, name)
    assert b.boundary_launcher["sha256"]
    assert b.auditor_identity["adapter_id"]
    assert b.auditor_identity["executable_identity"]
    assert b.auditor_identity["executable_sha256"]
    assert b.tool_wrapper["identity"] and b.tool_wrapper["sha256"]
    for pkg in (b.ebs_package, b.event_package):
        assert set(pkg) == {"manifest_sha256", "package_sha256"}
    assert b.output_identity["name"].endswith(".first-pass-report.json")


# ---------------- mutation matrix (each must be refused) ----------------

def mutated(binding_doc, mutate):
    doc = copy.deepcopy(binding_doc)
    mutate(doc)
    return doc


def wrong_target_field(field, value):
    def _m(doc):
        doc["target"][field] = value
    return _m


CASES = [
    ("wrong repository", wrong_target_field("repository", "evil/repo")),
    ("wrong commit", wrong_target_field("commit", "0" * 40)),
    ("wrong root tree", wrong_target_field("root_tree", "1" * 40)),
    ("wrong qh tree", wrong_target_field("qh_tree", "2" * 40)),
    ("wrong skill tree", wrong_target_field("skill_tree", "3" * 40)),
    ("missing target key", lambda d: d["target"].pop("qh_tree")),
    ("extra target key", lambda d: d["target"].update(extra="x")),
    ("unknown top-level key", lambda d: d.update(unexpected=1)),
    ("missing top-level key", lambda d: d.pop("prompt_contract_digest")),
    ("wrong type bool for digest", lambda d: d.update(prompt_contract_digest=True)),
    ("wrong type list for role", lambda d: d.update(auditor_role=["AUDITOR_A"])),
    ("invalid sha syntax short",
     lambda d: d.update(prompt_contract_digest="abc123")),
    ("invalid sha syntax nonhex",
     lambda d: d.update(common_evidence_manifest_digest="z" * 64)),
    ("invalid sha uppercase",
     lambda d: d.update(common_evidence_manifest_digest="A" * 64)),
    ("wrong policy id", lambda d: d.update(policy_id="AUCDEV-999-R0")),
    ("wrong role", lambda d: d.update(auditor_role="AUDITOR_C")),
    ("wrong event id format", lambda d: d.update(event_id="EVT-nothex!")),
    ("wrong attempt/event relationship",
     lambda d: d.update(attempt_id="evt-0011223344556677-B-01")),
    ("wrong attempt sequence",
     lambda d: d.update(attempt_id="evt-0011223344556677-A-02")),
    ("wrong launcher identity",
     lambda d: d["boundary_launcher"].update(identity="UNKNOWN-LAUNCHER")),
    # NOTE: a syntactically valid but semantically wrong launcher sha256 is
    # not parse-detectable; it is refused mechanically at verify_launcher
    # (see test_launch.py::test_wrong_digest_refused_before_fork).
    ("wrong common-evidence digest",
     lambda d: d.update(common_evidence_manifest_digest="9" * 64)),
    ("unknown provider role",
     lambda d: d["auditor_identity"].update(provider_role="MYSTERY-PROVIDER")),
    ("unknown adapter id",
     lambda d: d["auditor_identity"].update(adapter_id="real_adapter_v9")),
    ("role/adapter mismatch",
     lambda d: d["auditor_identity"].update(
         adapter_id="codex_chatgpt_oauth_v1")),
    ("wrong output identity kind",
     lambda d: d["output_identity"].update(kind="SECOND_PASS_REPORT")),
    ("wrong output identity name",
     lambda d: d["output_identity"].update(name="other-name.json")),
    ("unsafe output identity name",
     lambda d: d["output_identity"].update(name="../../etc/passwd")),
    ("missing required gate",
     lambda d: d["gate_evidence"].pop("GATE_W_PRIME")),
    ("unknown extra gate",
     lambda d: d["gate_evidence"].update(EXTRA_GATE={
         "status": "PASS", "evidence_sha256": "0" * 64,
         "evidence_size": 1, "role": "AUDITOR_A",
         "attempt_id": "evt-0011223344556677-A-01"})),
    ("fail gate status",
     lambda d: d["gate_evidence"]["GATE_W_PRIME"].update(status="FAIL")),
    ("unknown gate status",
     lambda d: d["gate_evidence"]["GATE_W_PRIME"].update(status="UNKNOWN")),
    ("malformed gate evidence no digest",
     lambda d: d["gate_evidence"]["GATE_W_PRIME"].pop("evidence_sha256")),
    ("malformed gate evidence bad size type",
     lambda d: d["gate_evidence"]["GATE_W_PRIME"].update(evidence_size="64")),
    ("gate evidence role mismatch",
     lambda d: d["gate_evidence"]["IDENTITY_LINTER"].update(role="AUDITOR_B")),
    ("gate evidence attempt mismatch",
     lambda d: d["gate_evidence"]["BLINDNESS_MAP"].update(
         attempt_id="evt-ffffffffffffffff-A-01")),
    ("gate evidence unknown field",
     lambda d: d["gate_evidence"]["GATE_W_PRIME"].update(note="hi")),
    # ---- new mandatory transport-binding dimensions (CR-EBS-001) ----
    ("missing sandbox profile id", lambda d: d.pop("sandbox_profile_id")),
    ("sandbox profile id unsafe",
     lambda d: d.update(sandbox_profile_id="bad profile/id!")),
    ("sandbox profile id wrong type",
     lambda d: d.update(sandbox_profile_id=["SANDBOX"])),
    ("tool wrapper missing",
     lambda d: d.pop("tool_wrapper")),
    ("tool wrapper unknown field",
     lambda d: d["tool_wrapper"].update(extra=1)),
    ("tool wrapper missing identity",
     lambda d: d["tool_wrapper"].pop("identity")),
    ("tool wrapper identity unsafe",
     lambda d: d["tool_wrapper"].update(identity="TOOL WRAPPER!")),
    ("tool wrapper sha malformed",
     lambda d: d["tool_wrapper"].update(sha256="xyz")),
    ("auditor executable identity missing",
     lambda d: d["auditor_identity"].pop("executable_identity")),
    ("auditor executable identity unsafe",
     lambda d: d["auditor_identity"].update(
         executable_identity="an executable identity string")),
    ("auditor executable identity wrong type",
     lambda d: d["auditor_identity"].update(executable_identity=7)),
    ("auditor executable sha missing",
     lambda d: d["auditor_identity"].pop("executable_sha256")),
    ("auditor executable sha malformed",
     lambda d: d["auditor_identity"].update(executable_sha256="A" * 64)),
    ("ebs package missing",
     lambda d: d.pop("ebs_package")),
    ("ebs package unknown key",
     lambda d: d["ebs_package"].update(extra="x")),
    ("ebs package missing key",
     lambda d: d["ebs_package"].pop("package_sha256")),
    ("ebs package wrong type",
     lambda d: d.update(ebs_package="pin")),
    ("ebs package malformed sha",
     lambda d: d["ebs_package"].update(manifest_sha256="0" * 63)),
    ("event package missing",
     lambda d: d.pop("event_package")),
    ("event package wrong type",
     lambda d: d.update(event_package=["pin"])),
    ("event package malformed sha",
     lambda d: d["event_package"].update(package_sha256="zzz")),
    ("event package unknown key",
     lambda d: d["event_package"].update(note="hi")),
    # ---- S1-001 gate-timing split: frozen vs runtime gate contract ----
    ("frozen RESOURCE_GATE PASS in gate evidence",
     lambda d: d["gate_evidence"].update(RESOURCE_GATE={
         "status": "PASS", "evidence_sha256": "0" * 64,
         "evidence_size": 64, "role": d["auditor_role"],
         "attempt_id": d["attempt_id"]})),
    # ---- S1-002: the SECOND mandatory dynamic runtime gate -------------
    ("frozen NETWORK_READINESS PASS in gate evidence",
     lambda d: d["gate_evidence"].update(NETWORK_READINESS={
         "status": "PASS", "evidence_sha256": "0" * 64,
         "evidence_size": 64, "role": d["auditor_role"],
         "attempt_id": d["attempt_id"]})),
    ("runtime gates missing",
     lambda d: d.pop("runtime_gates")),
    ("runtime gates wrong type",
     lambda d: d.update(runtime_gates=["RESOURCE_GATE"])),
    ("missing NETWORK_READINESS runtime gate",
     lambda d: d["runtime_gates"].pop("NETWORK_READINESS")),
    ("unknown runtime gate",
     lambda d: d["runtime_gates"].update(DNS_READINESS=dict(
         d["runtime_gates"]["RESOURCE_GATE"]))),
    ("runtime gate descriptor missing field",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].pop("sha256")),
    ("runtime gate descriptor extra field",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(result={})),
    ("runtime gate identity unsafe",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         identity="a gate identity!")),
    ("runtime gate identity wrong type",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(identity=5)),
    ("runtime gate path absolute",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         path="/etc/passwd")),
    ("runtime gate path traversal",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         path="../../outside/gate.py")),
    ("runtime gate path empty",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(path="")),
    ("runtime gate path dot segment",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         path="runtime/./resource-gate.py")),
    ("runtime gate path double slash",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         path="runtime//resource-gate.py")),
    ("runtime gate path wrong type",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(path=None)),
    ("runtime gate sha malformed",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(sha256="zzz")),
    ("runtime gate result schema wrong",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(
         result_schema="AUCDEV-023-RESOURCE-GATE-RESULT-V0")),
    ("runtime gate result schema missing value",
     lambda d: d["runtime_gates"]["RESOURCE_GATE"].update(result_schema="")),
    ("network gate descriptor missing field",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].pop("sha256")),
    ("network gate descriptor extra field",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].update(result={})),
    ("network gate identity unsafe",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].update(
         identity="a gate identity!")),
    ("network gate path absolute",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].update(
         path="/etc/passwd")),
    ("network gate path traversal",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].update(
         path="../../outside/gate.py")),
    ("network gate path backslash form",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].update(
         path="runtime\\network-readiness.py")),
    ("network gate sha malformed",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].update(
         sha256="0" * 63)),
    ("network gate result schema wrong",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].update(
         result_schema="AUCDEV-023-NETWORK-READINESS-RESULT-V0")),
    ("network gate result schema is resource schema",
     lambda d: d["runtime_gates"]["NETWORK_READINESS"].update(
         result_schema="AUCDEV-023-RESOURCE-GATE-RESULT-V1")),
    # ---- S1-006 V4: executable_version + exact auditor_invocation ----
    ("executable version missing",
     lambda d: d["auditor_identity"].pop("executable_version")),
    ("executable version wrong type",
     lambda d: d["auditor_identity"].update(executable_version=7)),
    ("executable version empty",
     lambda d: d["auditor_identity"].update(executable_version="")),
    ("executable version has whitespace",
     lambda d: d["auditor_identity"].update(
         executable_version="1.0 0")),
    ("executable version has control char",
     lambda d: d["auditor_identity"].update(
         executable_version="1.0\x00")),
    ("executable version non-ascii",
     lambda d: d["auditor_identity"].update(
         executable_version="sürüm-1")),
    ("executable version oversized",
     lambda d: d["auditor_identity"].update(executable_version="v" * 65)),
    ("auditor invocation missing",
     lambda d: d.pop("auditor_invocation")),
    ("auditor invocation wrong type dict",
     lambda d: d.update(auditor_invocation={"argv": []})),
    ("auditor invocation wrong type string",
     lambda d: d.update(auditor_invocation="client --flag")),
    ("auditor invocation empty list",
     lambda d: d.update(auditor_invocation=[])),
    ("auditor invocation non-string item",
     lambda d: d.update(auditor_invocation=["client", 7])),
    ("auditor invocation bool item",
     lambda d: d.update(auditor_invocation=["client", True])),
    ("auditor invocation null item",
     lambda d: d.update(auditor_invocation=["client", None])),
    ("auditor invocation empty item",
     lambda d: d.update(auditor_invocation=["client", ""])),
    ("auditor invocation NUL item",
     lambda d: d.update(auditor_invocation=["client", "a\x00b"])),
    ("auditor invocation newline item",
     lambda d: d.update(auditor_invocation=["client", "a\nb"])),
    ("auditor invocation item oversized",
     lambda d: d.update(auditor_invocation=["client", "x" * 1025])),
    ("auditor invocation total oversized",
     lambda d: d.update(auditor_invocation=["x" * 1000] * 9)),
    ("auditor invocation too many items",
     lambda d: d.update(auditor_invocation=[f"arg{i}" for i in range(33)])),
    # ---- S1-007/S1-008 V5: output_validator + execution_limits ----
    ("output validator missing",
     lambda d: d.pop("output_validator")),
    ("output validator wrong type",
     lambda d: d.update(output_validator="validator")),
    ("output validator unknown field",
     lambda d: d["output_validator"].update(extra=1)),
    ("output validator missing field",
     lambda d: d["output_validator"].pop("sha256")),
    ("output validator identity unsafe",
     lambda d: d["output_validator"].update(identity="a validator id!")),
    ("output validator path absolute",
     lambda d: d["output_validator"].update(path="/etc/validator.py")),
    ("output validator path traversal",
     lambda d: d["output_validator"].update(
         path="../../outside/validator.py")),
    ("output validator sha malformed",
     lambda d: d["output_validator"].update(sha256="zzz")),
    ("output validator result schema wrong",
     lambda d: d["output_validator"].update(
         result_schema="AUCDEV-023-REPORT-VALIDATOR-RESULT-V0")),
    ("execution limits missing",
     lambda d: d.pop("execution_limits")),
    ("execution limits wrong type",
     lambda d: d.update(execution_limits=[30])),
    ("execution limits unknown key",
     lambda d: d["execution_limits"].update(extra=5)),
    ("execution limits missing key",
     lambda d: d["execution_limits"].pop("validator_timeout_seconds")),
    ("auditor timeout bool",
     lambda d: d["execution_limits"].update(auditor_timeout_seconds=True)),
    ("auditor timeout float",
     lambda d: d["execution_limits"].update(auditor_timeout_seconds=30.0)),
    ("auditor timeout string",
     lambda d: d["execution_limits"].update(auditor_timeout_seconds="30")),
    ("auditor timeout zero",
     lambda d: d["execution_limits"].update(auditor_timeout_seconds=0)),
    ("auditor timeout negative",
     lambda d: d["execution_limits"].update(auditor_timeout_seconds=-1)),
    ("auditor timeout oversize",
     lambda d: d["execution_limits"].update(auditor_timeout_seconds=3601)),
    ("validator timeout bool",
     lambda d: d["execution_limits"].update(
         validator_timeout_seconds=False)),
    ("validator timeout float",
     lambda d: d["execution_limits"].update(
         validator_timeout_seconds=10.0)),
    ("validator timeout zero",
     lambda d: d["execution_limits"].update(validator_timeout_seconds=0)),
    ("validator timeout oversize",
     lambda d: d["execution_limits"].update(
         validator_timeout_seconds=10 ** 9)),
]


def test_s1_007_008_v5_dimensions_digest_covered(binding_doc,
                                                 parsed_binding):
    """S1-007/S1-008: output_validator and execution_limits are mandatory
    V5 dimensions, exactly parsed, and covered by Binding.digest (any
    change to either changes the digest)."""
    assert parsed_binding.output_validator == \
        binding_doc["output_validator"]
    assert parsed_binding.execution_limits == \
        binding_doc["execution_limits"]
    base = parse_binding(json.dumps(binding_doc).encode())
    bumped = copy.deepcopy(binding_doc)
    bumped["execution_limits"]["auditor_timeout_seconds"] = 31
    assert parse_binding(json.dumps(bumped).encode()).digest != base.digest
    swapped = copy.deepcopy(binding_doc)
    swapped["output_validator"]["identity"] = \
        "SYNTHETIC-INERT-OUTPUT-VALIDATOR-V2"
    assert parse_binding(json.dumps(swapped).encode()).digest != base.digest


def test_runtime_gate_set_is_exactly_two_dynamic_gates(parsed_binding):
    """S1-002: the binding requires EXACTLY the two dynamic runtime gates
    in the required execution order (network readiness FIRST, resource
    gate LAST); neither is a frozen evidence member."""
    from ebs.binding import REQUIRED_GATES, RUNTIME_GATES
    assert RUNTIME_GATES == ("NETWORK_READINESS", "RESOURCE_GATE")
    assert set(parsed_binding.runtime_gates) == set(RUNTIME_GATES)
    assert not set(RUNTIME_GATES) & set(REQUIRED_GATES)


@pytest.mark.parametrize("name,mutate", CASES, ids=[c[0] for c in CASES])
def test_binding_refusal_matrix(binding_doc, name, mutate):
    with pytest.raises(BindingError):
        parse(mutated(binding_doc, mutate))


def test_not_json_refused():
    with pytest.raises(BindingError):
        parse_binding(b"this is not json")


def test_duplicate_key_refused(binding_doc):
    text = json.dumps(binding_doc)
    poisoned = text[:-1] + ',"policy_id":"x"}'
    with pytest.raises(BindingError):
        parse_binding(poisoned.encode())


def test_nan_refused(binding_doc):
    text = json.dumps(binding_doc).replace('"prompt_contract_digest"',
                                           '"nan_field", NaN, "prompt_contract_digest"')
    with pytest.raises(BindingError):
        parse_binding(text.encode())


def test_s1_006_v4_dimensions_digest_and_order_covered(binding_doc,
                                                       parsed_binding):
    """S1-006: executable_version and auditor_invocation are mandatory
    V4 dimensions, exactly parsed with ordering preserved, and covered
    by Binding.digest (any change to either changes the digest)."""
    import copy as copy_mod
    assert parsed_binding.auditor_identity["executable_version"] == \
        binding_doc["auditor_identity"]["executable_version"]
    assert parsed_binding.auditor_invocation == \
        binding_doc["auditor_invocation"]          # exact ordered argv
    base = parse_binding(json.dumps(binding_doc).encode())
    reordered = copy_mod.deepcopy(binding_doc)
    reordered["auditor_invocation"] = list(reversed(
        reordered["auditor_invocation"]))
    assert parse_binding(json.dumps(reordered).encode()).digest != base.digest
    bumped = copy_mod.deepcopy(binding_doc)
    bumped["auditor_identity"]["executable_version"] = "SYNTHETIC-INERT-1.0.1"
    assert parse_binding(json.dumps(bumped).encode()).digest != base.digest


def test_binding_is_target_specific(parsed_binding):
    """Target-independence means code independence, not reusable policy:
    the frozen AUCDEV-023 target identity is the only accepted target."""
    assert parsed_binding.target["commit"] == \
        "d4d584ffa47ad2848268ba947247f81a845b2322"
