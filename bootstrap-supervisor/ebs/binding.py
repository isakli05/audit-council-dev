"""Strict frozen-binding parser/validator for the AUCDEV-023 EBS.

Fail-closed validation of the operator-declared attempt binding document
against the adopted R1 policy identity and the frozen audit-target
identity.  Unknown fields, wrong types, malformed digests, wrong target
identity, wrong roles/identities, and incomplete or non-PASS mandatory
gate evidence are all refused.  The binding is AUCDEV-023-specific:
target-independence means independence from the audited code, NOT
reusability of this policy for unrelated targets.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

POLICY_ID = ("AUCDEV-023-R1-CONTROLLERLESS-PROCESS-BOUND-"
             "TARGET-INDEPENDENT-ONE-SHOT")

# The one frozen audit-target identity accepted by this policy (adopted
# governance records, 2026-09-19); any other target is refused.
FROZEN_TARGET = {
    "repository": "isakli05/audit-council-dev",
    "commit": "d4d584ffa47ad2848268ba947247f81a845b2322",
    "root_tree": "1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7",
    "qh_tree": "5b8d5e5465923740470ff63ed9b8683f257a3787",
    "skill_tree": "c792933a862d9a5434681a88d183470dd8b15d2f",
}
TARGET_KEYS = ("repository", "commit", "root_tree", "qh_tree", "skill_tree")

ROLES = ("AUDITOR_A", "AUDITOR_B")
ROLE_PROVIDER_ROLES = {
    "AUDITOR_A": {"CLAUDE_FIRSTPARTY"},
    "AUDITOR_B": {"CODEX_CHATGPT_OAUTH"},
}
# The two adapter identities named by the adopted design revision plus the
# inert local-fixture adapter used by this task's zero-provider tests.
ROLE_ADAPTERS = {
    "AUDITOR_A": {"claude_firstparty_oauth_v1", "synthetic_inert_local_v1"},
    "AUDITOR_B": {"codex_chatgpt_oauth_v1", "synthetic_inert_local_v1"},
}

LAUNCHER_IDS = ("NETWORKED-BOUNDARY-LAUNCHER-V1",
                "INERT-LOCAL-FIXTURE-LAUNCHER-V1")

REQUIRED_GATES = (
    "PACKAGE_BINDING_IDENTITY",
    "COMMON_EVIDENCE_PARITY",
    "IDENTITY_LINTER",
    "BLINDNESS_MAP",
    "RESOURCE_GATE",
    "GATE_W_PRIME",
    "REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION",
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EVENT_ID_RE = re.compile(r"^evt-[0-9a-f]{16}$")
OUTPUT_KIND = "FIRST_PASS_REPORT"
GATE_FIELDS = ("status", "evidence_sha256", "evidence_size", "role",
               "attempt_id")
TOP_LEVEL = ("policy_id", "event_id", "auditor_role", "attempt_id", "target",
             "common_evidence_manifest_digest", "prompt_contract_digest",
             "boundary_launcher", "auditor_identity", "output_identity",
             "gate_evidence")


class BindingError(ValueError):
    """Refused binding document (fail closed)."""


def attempt_id_for(event_id: str, role: str) -> str:
    """Deterministic first-pass attempt identity for an event/role pair."""
    return f"{event_id}-{role.rsplit('_', 1)[-1]}-01"


def output_name_for(attempt_id: str) -> str:
    return f"{attempt_id}.first-pass-report.json"


def canonical_bytes(document: dict) -> bytes:
    return json.dumps(document, sort_keys=True,
                      separators=(",", ":")).encode()


def _no_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise BindingError(f"DUPLICATE_KEY: {key}")
        obj[key] = value
    return obj


def _reject_constant(name):
    raise BindingError(f"NON_FINITE_JSON_CONSTANT: {name}")


def _strict_loads(data):
    if isinstance(data, str):
        data = data.encode()
    try:
        return json.loads(data.decode("utf-8"),
                          object_pairs_hook=_no_duplicate_keys,
                          parse_constant=_reject_constant)
    except BindingError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BindingError(f"NOT_VALID_JSON: {exc}") from exc


def _exact_keys(mapping, expected, where):
    if not isinstance(mapping, dict):
        raise BindingError(f"{where}_NOT_AN_OBJECT")
    got, want = set(mapping), set(expected)
    if got != want:
        raise BindingError(
            f"{where}_KEYS_INVALID: unknown={sorted(got - want)} "
            f"missing={sorted(want - got)}")


def _sha_field(value, where):
    if not isinstance(value, str) or not SHA256_RE.match(value):
        raise BindingError(f"{where}_NOT_SHA256")
    return value


@dataclass(frozen=True)
class Binding:
    policy_id: str
    event_id: str
    auditor_role: str
    attempt_id: str
    target: dict
    common_evidence_manifest_digest: str
    prompt_contract_digest: str
    boundary_launcher: dict
    auditor_identity: dict
    output_identity: dict
    gate_evidence: dict
    digest: str


def valid_binding_document(event_id: str, role: str, launcher_sha256: str,
                           launcher_identity: str = "INERT-LOCAL-FIXTURE-LAUNCHER-V1",
                           adapter_id: str = "synthetic_inert_local_v1",
                           provider_role: str = None,
                           evidence_seed: str = "synthetic-evidence") -> dict:
    """Build one well-formed synthetic binding document (operator/test aid)."""
    attempt = attempt_id_for(event_id, role)
    prov = provider_role or next(iter(ROLE_PROVIDER_ROLES[role]))
    manifest_digest = hashlib.sha256(
        f"{evidence_seed}:common".encode()).hexdigest()
    gates = {gate: {
        "status": "PASS",
        "evidence_sha256": manifest_digest
        if gate == "COMMON_EVIDENCE_PARITY" else hashlib.sha256(
            f"{evidence_seed}:{gate}".encode()).hexdigest(),
        "evidence_size": 64,
        "role": role,
        "attempt_id": attempt,
    } for gate in REQUIRED_GATES}
    return {
        "policy_id": POLICY_ID,
        "event_id": event_id,
        "auditor_role": role,
        "attempt_id": attempt,
        "target": dict(FROZEN_TARGET),
        "common_evidence_manifest_digest": manifest_digest,
        "prompt_contract_digest": hashlib.sha256(
            f"{evidence_seed}:contract".encode()).hexdigest(),
        "boundary_launcher": {"identity": launcher_identity,
                              "sha256": launcher_sha256},
        "auditor_identity": {"provider_role": prov, "adapter_id": adapter_id},
        "output_identity": {"kind": OUTPUT_KIND,
                            "name": output_name_for(attempt)},
        "gate_evidence": gates,
    }


def parse_binding(data) -> Binding:
    """Parse and fully validate a frozen binding document (fail closed)."""
    doc = _strict_loads(data)
    _exact_keys(doc, TOP_LEVEL, "BINDING")

    if doc["policy_id"] != POLICY_ID:
        raise BindingError(f"POLICY_ID_UNEXPECTED: {doc['policy_id']!r}")

    event_id = doc["event_id"]
    if not isinstance(event_id, str) or not EVENT_ID_RE.match(event_id):
        raise BindingError(f"EVENT_ID_MALFORMED: {event_id!r}")

    role = doc["auditor_role"]
    if role not in ROLES:
        raise BindingError(f"AUDITOR_ROLE_UNKNOWN: {role!r}")

    attempt = doc["attempt_id"]
    if not isinstance(attempt, str) or attempt != attempt_id_for(event_id,
                                                                 role):
        raise BindingError(
            f"ATTEMPT_EVENT_RELATIONSHIP_INVALID: {attempt!r} != "
            f"{attempt_id_for(event_id, role)!r}")

    _exact_keys(doc["target"], TARGET_KEYS, "TARGET")
    for key in TARGET_KEYS:
        if doc["target"][key] != FROZEN_TARGET[key]:
            raise BindingError(
                f"FROZEN_TARGET_MISMATCH: {key}={doc['target'][key]!r}")

    _sha_field(doc["common_evidence_manifest_digest"],
               "COMMON_EVIDENCE_MANIFEST_DIGEST")
    _sha_field(doc["prompt_contract_digest"], "PROMPT_CONTRACT_DIGEST")

    _exact_keys(doc["boundary_launcher"], ("identity", "sha256"),
                "BOUNDARY_LAUNCHER")
    if doc["boundary_launcher"]["identity"] not in LAUNCHER_IDS:
        raise BindingError(
            "BOUNDARY_LAUNCHER_IDENTITY_UNKNOWN: "
            f"{doc['boundary_launcher']['identity']!r}")
    _sha_field(doc["boundary_launcher"]["sha256"],
               "BOUNDARY_LAUNCHER_SHA256")

    _exact_keys(doc["auditor_identity"], ("provider_role", "adapter_id"),
                "AUDITOR_IDENTITY")
    if doc["auditor_identity"]["provider_role"] not in \
            ROLE_PROVIDER_ROLES[role]:
        raise BindingError(
            "PROVIDER_ROLE_UNKNOWN_FOR_ROLE: "
            f"{doc['auditor_identity']['provider_role']!r}")
    if doc["auditor_identity"]["adapter_id"] not in ROLE_ADAPTERS[role]:
        raise BindingError(
            f"ADAPTER_ID_UNKNOWN: {doc['auditor_identity']['adapter_id']!r}")

    _exact_keys(doc["output_identity"], ("kind", "name"), "OUTPUT_IDENTITY")
    if doc["output_identity"]["kind"] != OUTPUT_KIND:
        raise BindingError("OUTPUT_KIND_UNEXPECTED")
    if doc["output_identity"]["name"] != output_name_for(attempt):
        raise BindingError("OUTPUT_NAME_NOT_ATTEMPT_DERIVED")

    _exact_keys(doc["gate_evidence"], REQUIRED_GATES, "GATE_EVIDENCE")
    for gate, evidence in doc["gate_evidence"].items():
        _exact_keys(evidence, GATE_FIELDS, f"GATE_{gate}")
        if evidence["status"] != "PASS":
            raise BindingError(
                f"GATE_{gate}_NOT_PASS: {evidence['status']!r}")
        _sha_field(evidence["evidence_sha256"], f"GATE_{gate}_EVIDENCE")
        size = evidence["evidence_size"]
        if isinstance(size, bool) or not isinstance(size, int) \
                or not 0 <= size <= 2 ** 31 - 1:
            raise BindingError(f"GATE_{gate}_EVIDENCE_SIZE_INVALID")
        if evidence["role"] != role:
            raise BindingError(f"GATE_{gate}_ROLE_MISMATCH")
        if evidence["attempt_id"] != attempt:
            raise BindingError(f"GATE_{gate}_ATTEMPT_MISMATCH")

    # Cross-plane consistency: the COMMON_EVIDENCE_PARITY gate must carry
    # evidence bound to the SAME frozen manifest the binding declares.
    if doc["gate_evidence"]["COMMON_EVIDENCE_PARITY"]["evidence_sha256"] != \
            doc["common_evidence_manifest_digest"]:
        raise BindingError(
            "COMMON_EVIDENCE_PARITY_DIGEST_INCONSISTENT: gate evidence is "
            "not the declared common-evidence manifest digest")

    return Binding(
        policy_id=doc["policy_id"], event_id=event_id, auditor_role=role,
        attempt_id=attempt, target=dict(doc["target"]),
        common_evidence_manifest_digest=doc["common_evidence_manifest_digest"],
        prompt_contract_digest=doc["prompt_contract_digest"],
        boundary_launcher=dict(doc["boundary_launcher"]),
        auditor_identity=dict(doc["auditor_identity"]),
        output_identity=dict(doc["output_identity"]),
        gate_evidence={k: dict(v) for k, v in doc["gate_evidence"].items()},
        digest=hashlib.sha256(canonical_bytes(doc)).hexdigest())
