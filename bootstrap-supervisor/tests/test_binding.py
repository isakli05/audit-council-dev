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
    ("runtime gates missing",
     lambda d: d.pop("runtime_gates")),
    ("runtime gates wrong type",
     lambda d: d.update(runtime_gates=["RESOURCE_GATE"])),
    ("unknown runtime gate",
     lambda d: d["runtime_gates"].update(NETWORK_READINESS=dict(
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
]


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


def test_binding_is_target_specific(parsed_binding):
    """Target-independence means code independence, not reusable policy:
    the frozen AUCDEV-023 target identity is the only accepted target."""
    assert parsed_binding.target["commit"] == \
        "d4d584ffa47ad2848268ba947247f81a845b2322"
