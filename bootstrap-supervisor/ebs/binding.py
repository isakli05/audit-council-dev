"""Strict frozen-binding parser/validator for the AUCDEV-023 EBS.

Fail-closed validation of the operator-declared attempt binding document
against the adopted R1 policy identity and the frozen audit-target
identity.  Unknown fields, wrong types, malformed digests, wrong target
identity, wrong roles/identities, and incomplete or non-PASS mandatory
gate evidence are all refused.  The binding is AUCDEV-023-specific:
target-independence means independence from the audited code, NOT
reusability of this policy for unrelated targets.

The schema carries the COMPLETE adopted transport-binding dimension
set (design §17; list and semantics in README.md): every dimension is
mandatory, digest-covered by `Binding.digest`, mechanically bound to the
accounting store, and durably recorded at CONSUMED_PRE_EXEC — swapping
ANY dimension changes the digest, which store and supervisor refuse for
the same attempt.  Synthetic test documents are built in
tests/conftest.py (no doc-builder lives in the TCB).

Second remediation (CR-EBS-REM-001): this module also defines the
VERSIONED STRICT EVENT-PACKAGE MANIFEST CONTRACT and the canonical
transport projection `binding_projection`, established mechanically by
`launch.verify_event_package` BEFORE GATES_PASSED (non-circular
construction documented in README.md + the second-remediation report).

Gate-timing remediation (CR-EBS-S1-001) and preexec-gate remediation
(CR-EBS-S1-002/-003): the gate dimension is SPLIT.  The six STATIC
preparation gates above remain frozen PASS evidence members; the TWO
DYNAMIC runtime gates — NETWORK_READINESS and RESOURCE_GATE, in that
required execution order — are NOT frozen evidence: each is frozen as
an exact executable-artifact DESCRIPTOR (identity, safe
event-package-relative path, exact SHA-256, exact per-gate result
schema), covered by `Binding.digest` and by the transport projection,
and EXECUTED by the EBS exactly once each inside the ONE public
preexec-consumption operation (`launch.Supervisor.run_attempt`).  A
package-time PASS for either runtime gate cannot exist in a valid
binding.

Final launch-seam remediation (CR-EBS-S1-004/-005/-006): the transport
binding advances to V4 — `auditor_identity` gains the mandatory
`executable_version` (a bounded frozen version TOKEN: declared binding
fact, never a live-extracted claim) and the NEW top-level dimension
`auditor_invocation` freezes the EXACT ordered auditor-client argv
(bounded control-free non-empty strings, bounded in count/per-item/
total bytes; NUL and every control character refused; order preserved).
Both are digest- and projection-covered; the event-package manifest
schema advances V3 -> V4 with every older tag refused.
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

# STATIC preparation gates: frozen PASS evidence members only (S1-001).
REQUIRED_GATES = (
    "PACKAGE_BINDING_IDENTITY",
    "COMMON_EVIDENCE_PARITY",
    "IDENTITY_LINTER",
    "BLINDNESS_MAP",
    "GATE_W_PRIME",
    "REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION",
)

# The TWO DYNAMIC gates (S1-001; S1-002 adds NETWORK_READINESS), in the
# REQUIRED dynamic execution order — NETWORK_READINESS first, so
# RESOURCE_GATE is the LAST live environmental gate immediately before
# durable consumption.  Neither may EVER appear as a frozen PASS
# evidence member (a package-time PASS would go stale before the
# separately authorized execution): the binding instead freezes an
# exact EXECUTABLE-ARTIFACT DESCRIPTOR (RUNTIME_GATE_FIELDS) per gate,
# executed fresh by the EBS (launch.py).  No descriptor carries a
# result or a PASS.
RUNTIME_GATES = ("NETWORK_READINESS", "RESOURCE_GATE")
RUNTIME_GATE_FIELDS = ("identity", "path", "sha256", "result_schema")
RESOURCE_GATE_RESULT_SCHEMA = "AUCDEV-023-RESOURCE-GATE-RESULT-V1"
NETWORK_READINESS_RESULT_SCHEMA = "AUCDEV-023-NETWORK-READINESS-RESULT-V1"
RUNTIME_GATE_RESULT_SCHEMAS = {
    "NETWORK_READINESS": NETWORK_READINESS_RESULT_SCHEMA,
    "RESOURCE_GATE": RESOURCE_GATE_RESULT_SCHEMA,
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EVENT_ID_RE = re.compile(r"^evt-[0-9a-f]{16}$")
# Pinned identity strings (executable/sandbox/wrapper): safe tokens only.
IDENTITY_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
# Frozen auditor-executable version TOKEN (S1-006): bounded printable
# ASCII without whitespace (so NUL and every control char are refused);
# a declared binding fact, NOT a live-extracted claim.
EXECUTABLE_VERSION_RE = re.compile(r"^[!-~]{1,64}$")
# Exact frozen auditor-client argv bounds (S1-006).
AUDITOR_INVOCATION_MAX_ITEMS = 32
AUDITOR_INVOCATION_ITEM_MAX_BYTES = 1024
AUDITOR_INVOCATION_TOTAL_MAX_BYTES = 8192
# Safe event-package-relative path segments (runtime-gate artifact path):
# charset-bounded, no empty segment (rejects absolute "/"-prefixed and
# "//"), no "." / ".." traversal, no drive/backslash forms.
PATH_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
OUTPUT_KIND = "FIRST_PASS_REPORT"
GATE_FIELDS = ("status", "evidence_sha256", "evidence_size", "role",
               "attempt_id")
# A pinned package identity pair (see launch.py / README.md for the
# non-circular construction of both digests).
PACKAGE_FIELDS = ("manifest_sha256", "package_sha256")
AUDITOR_IDENTITY_FIELDS = ("provider_role", "adapter_id",
                           "executable_identity", "executable_version",
                           "executable_sha256")
TOP_LEVEL = ("policy_id", "event_id", "auditor_role", "attempt_id", "target",
             "common_evidence_manifest_digest", "prompt_contract_digest",
             "boundary_launcher", "auditor_identity", "sandbox_profile_id",
             "tool_wrapper", "ebs_package", "event_package",
             "output_identity", "gate_evidence", "runtime_gates",
             "auditor_invocation")

# --- versioned strict event-package manifest contract (CR-EBS-REM-001;
# full semantics in README.md + second-remediation report): a frozen
# event package's manifest has an EXACT key set, an EXACT schema tag,
# and the COMPLETE transport projection below.  V2 (CR-EBS-S1-001): the
# projection semantics MATERIALLY CHANGE — RESOURCE_GATE is no longer a
# frozen evidence member and the runtime-gate descriptor becomes a bound
# security dimension.  V3 (CR-EBS-S1-002/-003): they change AGAIN — the
# mandatory dynamic runtime-gate set becomes EXACTLY TWO descriptors
# (NETWORK_READINESS + RESOURCE_GATE) and the runtime-gate execution
# ordering/consumption semantics change (single preexec-consumption
# operation).  V4 (CR-EBS-S1-004/-005/-006 final launch-seam): they
# change AGAIN — auditor_identity gains executable_version and the NEW
# auditor_invocation dimension freezes the exact auditor-client argv,
# with the whole authority path collapsed into the single
# run_attempt(credential_source_fd, ...) operation.  Each advance
# REFUSES the older tag, never silently accepting it as equivalent; no
# real V1/V2/V3 event package exists to migrate. ---
EVENT_MANIFEST_SCHEMA = "AUCDEV-023-EVENT-PACKAGE-MANIFEST-V4"
EVENT_MANIFEST_KEYS = frozenset(
    ("schema", "transport_binding", "files", "package_sha256"))
# Every binding security dimension EXCEPT event_package itself (the
# package's own identity pair is pinned independently by the binding and
# verified against the actual package bytes — no circular self-hashing).
PROJECTION_FIELDS = tuple(name for name in TOP_LEVEL
                          if name != "event_package")


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


def strict_loads(data):
    """Strict JSON parse (shared by the binding document and both package
    manifest verifiers): duplicate keys and non-finite constants refused."""
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


def _identity_field(value, where):
    if not isinstance(value, str) or not IDENTITY_RE.match(value):
        raise BindingError(f"{where}_NOT_A_SAFE_IDENTITY")
    return value


def _executable_version_field(value):
    """Mandatory frozen auditor-executable version token (S1-006):
    bounded, whitespace-free, control-free (NUL included) printable
    ASCII.  Declared cross-bound metadata — the EBS never claims it was
    extracted from live executable bytes."""
    if not isinstance(value, str) or not EXECUTABLE_VERSION_RE.match(value):
        raise BindingError("AUDITOR_EXECUTABLE_VERSION_INVALID")
    return value


def _invocation_field(value, where):
    """The EXACT frozen auditor-client argv (S1-006): a non-empty ordered
    list of bounded strings, bounded in item count, per-item UTF-8 bytes
    and total bytes; every item is a non-empty string with NO control
    character (NUL included); ordering is exactly the JSON list order."""
    if not isinstance(value, list) or not value:
        raise BindingError(f"{where}_NOT_A_NONEMPTY_LIST")
    if len(value) > AUDITOR_INVOCATION_MAX_ITEMS:
        raise BindingError(f"{where}_ITEM_COUNT_INVALID")
    total = 0
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise BindingError(f"{where}_ITEM_NOT_A_STRING_AT_{index}")
        if any(ord(char) < 0x20 or ord(char) == 0x7f for char in item):
            raise BindingError(f"{where}_ITEM_CONTROL_CHAR_AT_{index}")
        try:
            size = len(item.encode("utf-8"))
        except UnicodeEncodeError:
            raise BindingError(
                f"{where}_ITEM_NOT_UTF8_AT_{index}") from None
        if not 0 < size <= AUDITOR_INVOCATION_ITEM_MAX_BYTES:
            raise BindingError(f"{where}_ITEM_SIZE_INVALID_AT_{index}")
        total += size
    if total > AUDITOR_INVOCATION_TOTAL_MAX_BYTES:
        raise BindingError(f"{where}_TOTAL_SIZE_INVALID")
    return list(value)


def _safe_relpath(value, where):
    """A safe event-package-relative POSIX path: non-empty bounded str of
    charset-bounded segments; absolute paths, empty segments, "."/".."
    traversal, and any non-str type are refused (fail closed)."""
    if not isinstance(value, str) or not 0 < len(value) <= 512:
        raise BindingError(f"{where}_NOT_A_SAFE_RELATIVE_PATH")
    for segment in value.split("/"):
        if segment in ("", ".", "..") or not PATH_SEGMENT_RE.match(segment):
            raise BindingError(f"{where}_NOT_A_SAFE_RELATIVE_PATH")
    return value


def _package_fields(value, where):
    """Validate one pinned package-identity pair (exact keys, digests)."""
    _exact_keys(value, PACKAGE_FIELDS, where)
    _sha_field(value["manifest_sha256"], f"{where}_MANIFEST")
    _sha_field(value["package_sha256"], f"{where}_PACKAGE")
    return dict(value)


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
    sandbox_profile_id: str
    tool_wrapper: dict
    ebs_package: dict
    event_package: dict
    output_identity: dict
    gate_evidence: dict
    runtime_gates: dict
    auditor_invocation: list
    digest: str


def parse_binding(data) -> Binding:
    """Parse and fully validate a frozen binding document (fail closed)."""
    doc = strict_loads(data)
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

    _exact_keys(doc["auditor_identity"], AUDITOR_IDENTITY_FIELDS,
                "AUDITOR_IDENTITY")
    if doc["auditor_identity"]["provider_role"] not in \
            ROLE_PROVIDER_ROLES[role]:
        raise BindingError(
            "PROVIDER_ROLE_UNKNOWN_FOR_ROLE: "
            f"{doc['auditor_identity']['provider_role']!r}")
    if doc["auditor_identity"]["adapter_id"] not in ROLE_ADAPTERS[role]:
        raise BindingError(
            f"ADAPTER_ID_UNKNOWN: {doc['auditor_identity']['adapter_id']!r}")
    _identity_field(doc["auditor_identity"]["executable_identity"],
                    "AUDITOR_EXECUTABLE_IDENTITY")
    _executable_version_field(doc["auditor_identity"]["executable_version"])
    _sha_field(doc["auditor_identity"]["executable_sha256"],
               "AUDITOR_EXECUTABLE_SHA256")

    _identity_field(doc["sandbox_profile_id"], "SANDBOX_PROFILE_ID")

    _exact_keys(doc["tool_wrapper"], ("identity", "sha256"), "TOOL_WRAPPER")
    _identity_field(doc["tool_wrapper"]["identity"], "TOOL_WRAPPER_IDENTITY")
    _sha_field(doc["tool_wrapper"]["sha256"], "TOOL_WRAPPER_SHA256")

    ebs_package = _package_fields(doc["ebs_package"], "EBS_PACKAGE")
    event_package = _package_fields(doc["event_package"], "EVENT_PACKAGE")

    _exact_keys(doc["output_identity"], ("kind", "name"), "OUTPUT_IDENTITY")
    if doc["output_identity"]["kind"] != OUTPUT_KIND:
        raise BindingError("OUTPUT_KIND_UNEXPECTED")
    if doc["output_identity"]["name"] != output_name_for(attempt):
        raise BindingError("OUTPUT_NAME_NOT_ATTEMPT_DERIVED")

    for runtime_gate in RUNTIME_GATES:
        if runtime_gate in doc["gate_evidence"]:
            # S1-001/S1-002: a frozen package-time PASS for a RUNTIME
            # gate is exactly the stale-evidence defect — refused BEFORE
            # any other gate check.
            raise BindingError(
                f"GATE_EVIDENCE_{runtime_gate}_FORBIDDEN: "
                f"{runtime_gate} is a RUNTIME gate (frozen "
                "executable-artifact descriptor in runtime_gates), never "
                "a frozen PASS evidence member; a package-time PASS "
                "cannot exist in a valid binding")
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

    # S1-001/S1-002 runtime-gate descriptors: EXACTLY the two dynamic
    # runtime gates, each with the EXACT descriptor field set — a frozen
    # identity/path/digest/result-schema contract per gate, no result,
    # no PASS.
    runtime = doc["runtime_gates"]
    _exact_keys(runtime, RUNTIME_GATES, "RUNTIME_GATES")
    descriptors = {}
    for runtime_gate in RUNTIME_GATES:
        descriptor = runtime[runtime_gate]
        _exact_keys(descriptor, RUNTIME_GATE_FIELDS,
                    f"RUNTIME_GATE_{runtime_gate}")
        _identity_field(descriptor["identity"], "RUNTIME_GATE_IDENTITY")
        _safe_relpath(descriptor["path"], "RUNTIME_GATE_PATH")
        _sha_field(descriptor["sha256"], "RUNTIME_GATE_SHA256")
        if descriptor["result_schema"] != \
                RUNTIME_GATE_RESULT_SCHEMAS[runtime_gate]:
            raise BindingError(
                "RUNTIME_GATE_RESULT_SCHEMA_UNEXPECTED: "
                f"{descriptor['result_schema']!r}")
        descriptors[runtime_gate] = dict(descriptor)

    return Binding(
        policy_id=doc["policy_id"], event_id=event_id, auditor_role=role,
        attempt_id=attempt, target=dict(doc["target"]),
        common_evidence_manifest_digest=doc["common_evidence_manifest_digest"],
        prompt_contract_digest=doc["prompt_contract_digest"],
        boundary_launcher=dict(doc["boundary_launcher"]),
        auditor_identity=dict(doc["auditor_identity"]),
        sandbox_profile_id=doc["sandbox_profile_id"],
        tool_wrapper=dict(doc["tool_wrapper"]),
        ebs_package=ebs_package,
        event_package=event_package,
        output_identity=dict(doc["output_identity"]),
        gate_evidence={k: dict(v) for k, v in doc["gate_evidence"].items()},
        runtime_gates=descriptors,
        auditor_invocation=_invocation_field(doc["auditor_invocation"],
                                             "AUDITOR_INVOCATION"),
        digest=hashlib.sha256(canonical_bytes(doc)).hexdigest())


def binding_projection(binding: Binding) -> dict:
    """Canonical transport projection of a parsed binding: the EXACT value
    a frozen event-package manifest's transport_binding field must equal
    (launch.verify_event_package compares the two as canonical JSON
    bytes, so JSON type confusions such as true==1 cannot pass).  Covers
    every security dimension in PROJECTION_FIELDS; event_package is
    intentionally EXCLUDED — it is the package's own identity pair,
    verified independently against the actual package bytes (the
    non-circular construction).  Internal use only: the result is
    serialized, never mutated."""
    return {name: getattr(binding, name) for name in PROJECTION_FIELDS}
