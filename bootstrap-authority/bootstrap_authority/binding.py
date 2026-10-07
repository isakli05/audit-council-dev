"""Strict frozen-binding parser for the AUCDEV-023 PCH6-B PATH-B
candidate-specific target-independent bootstrap authority.

NEW authority-specific source for the wholly NEW PATH-B lineage
(Control Room design readback 2026-10-02); shares NO code with, and
imports NOTHING from, the audit target
`730d2b29:bootstrap-supervisor/**` (AUDIT SUBJECT, never authority)
or the legacy EBS at `068f5e2` (REFERENCE_ONLY).  Fail-closed
validation of the operator-declared attempt binding document against
the PATH-B policy identity, the frozen fresh-audit target, the
design-reserved event/attempt identities and the governance-frozen
auditor selections: unknown fields, wrong types, malformed digests,
wrong target identity, wrong event/role/attempt pairing, substituted
model/effort/client selections, and incomplete or non-PASS static
gate evidence are all refused.  The output identity additionally
freezes the output-custody root and report-source path as canonical
absolute paths, the custody directory's host-local OBJECT identity
(st_dev/st_ino) and the invocation-to-report-sink equality edge
(BA-PREP-001/002 + BA-PREP-RB2-001/002).  The policy is
candidate-specific — NOT standing authority for any other candidate;
every dimension is mandatory and digest-covered by `Binding.digest`;
synthetic test documents are built in tests/conftest.py.

Gate split (PATH-B): the EIGHT STATIC preparation gates are frozen
PASS evidence members; the THREE DYNAMIC runtime gates are NOT frozen
evidence: each is an exact executable-artifact DESCRIPTOR executed
fresh exactly once inside the ONE public preexec-consumption
operation (a package-time PASS cannot exist in a valid binding);
CLIENT_SELECTION_PREFLIGHT is the NO-FALLBACK enforcement point.  The
VERSIONED STRICT EVENT-PACKAGE / AUTHORITY-PACKAGE MANIFEST contracts
(exact key sets, schema tags, file rows, non-circular identities) and
the canonical transport projection `binding_projection` (verified by
runtime before GATES_PASSED) are defined here too.

The SEPARATE explicitly versioned V2 REPLACEMENT contract (G2 of the
accepted G0-G12 governance order) adds exactly ONE source-level
replacement slot (label AUDITOR_A_REPLACEMENT_1; the actual auditor
role stays AUDITOR_A) with a CLOSED mapping — plus an additive V2
authority-manifest schema, the immutable 20-field
AUCDEV-023-PACKAGE-BINDING-GRANT-V2 canonicalization/identity
mechanics and the NON-RUNTIME package-binding receipt V1 source
primitive, whose ONE canonical namespace is pinned by the strict
VERIFIED future G7 mint-publication context (never a caller-selected
root).  All UNISSUED/UNCREATED: nothing in this module creates an
attempt, grant, receipt, accounting state or execution authority.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass

POLICY_ID = ("AUCDEV-023-PCH6B-CAND730D2B29-TARGET-INDEPENDENT-"
             "BOOTSTRAP-AUTHORITY-V1")

# The one frozen fresh-audit target accepted by this policy (readback
# 6.5); any other target is refused before inference can be reachable.
FROZEN_TARGET = {
    "repository": "isakli05/audit-council-dev",
    "commit": "730d2b29f7c0e7d33af3451b6d9205ec27c143ed",
    "root_tree": "2585796efd5cb6902226cfff785bb901297a15e3",
    "bootstrap_supervisor_tree":
        "3056e577259ab0b0b0472f82ebc306506f3e084c",
    "qualification_harness_tree":
        "5b8d5e5465923740470ff63ed9b8683f257a3787",
    "skill_tree": "efd8c2e48edbb25795b3aacb1ce3c23fde10082a",
    "remediation_parent":
        "068f5e29904f446bf832138fd64c8833b9037cb7",
}
TARGET_KEYS = ("repository", "commit", "root_tree",
               "bootstrap_supervisor_tree", "qualification_harness_tree",
               "skill_tree", "remediation_parent")
# Design-reserved identities for the wholly NEW lineage (readback 6.7):
# binding constants ONLY — parsing them instantiates nothing; synthetic
# fixtures using them are NON-AUTHORITATIVE / ZERO-PROVIDER.
EVENT_ID = "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01"
RESERVED_ATTEMPT_IDS = {
    "AUDITOR_A":
        "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01",
    "AUDITOR_B":
        "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-B-01",
}
ROLES = ("AUDITOR_A", "AUDITOR_B")

# Governance-frozen auditor selections (readback 6.8) — explicit, never
# ambient/default/auto, never inherited, NO fallback; the client
# executable identity/version/SHA-256 come from the LATER event
# package.
AUDITOR_SELECTIONS = {
    "AUDITOR_A": {"provider_role": "CLAUDE_FIRSTPARTY",
                  "client_family": "CLAUDE_FIRSTPARTY",
                  "model": "claude-opus-5-5", "effort": "high"},
    "AUDITOR_B": {"provider_role": "CODEX_CHATGPT_OAUTH",
                  "client_family": "CODEX_CHATGPT_OAUTH",
                  "model": "gpt-6.1-sol", "effort": "high"},
}
SELECTION_KEYS = ("provider_role", "client_family", "model", "effort",
                  "client_executable")
CLIENT_EXECUTABLE_KEYS = ("identity", "version", "sha256")

# STATIC preparation gates: frozen PASS evidence members only.
REQUIRED_STATIC_GATES = (
    "PACKAGE_BINDING_IDENTITY",
    "COMMON_EVIDENCE_PARITY",
    "IDENTITY_LINTER",
    "BLINDNESS_MAP",
    "NEUTRAL_CONTRACT_FREEZE",
    "GATE_W_PRIME",
    "REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION",
    "TARGET_AUTHORITY_SEPARATION",
)

# The THREE DYNAMIC gates in the REQUIRED execution order —
# CLIENT_SELECTION_PREFLIGHT first (the no-fallback enforcement point),
# NETWORK_READINESS second, RESOURCE_GATE LAST; none may EVER appear
# as a frozen PASS evidence member (a package-time PASS would go
# stale).
DYNAMIC_GATE_ORDER = ("CLIENT_SELECTION_PREFLIGHT", "NETWORK_READINESS",
                      "RESOURCE_GATE")
CLIENT_SELECTION_RESULT_SCHEMA = \
    "AUCDEV-023-CAND730D2B29-CLIENT-SELECTION-PREFLIGHT-RESULT-V1"
NETWORK_READINESS_RESULT_SCHEMA = \
    "AUCDEV-023-CAND730D2B29-NETWORK-READINESS-RESULT-V1"
RESOURCE_GATE_RESULT_SCHEMA = \
    "AUCDEV-023-CAND730D2B29-RESOURCE-GATE-RESULT-V1"
DYNAMIC_GATE_RESULT_SCHEMAS = {
    "CLIENT_SELECTION_PREFLIGHT": CLIENT_SELECTION_RESULT_SCHEMA,
    "NETWORK_READINESS": NETWORK_READINESS_RESULT_SCHEMA,
    "RESOURCE_GATE": RESOURCE_GATE_RESULT_SCHEMA,
}
# Descriptor field sets: an EXECUTABLE descriptor (launcher/wrapper)
# pins identity/path/sha256/bytes; a RUNNABLE descriptor (a dynamic
# gate or the structural validator) adds the result schema tag and
# bounded timeout/result size.  The structural validator is SHAPE-ONLY
# for target_commit (check_report_binding is the binding authority).
EXECUTABLE_DESCRIPTOR_FIELDS = ("identity", "path", "sha256", "bytes")
RUNNABLE_DESCRIPTOR_FIELDS = ("identity", "path", "sha256", "bytes",
                              "result_schema", "timeout_seconds",
                              "max_result_bytes")
OUTPUT_VALIDATOR_FIELDS = RUNNABLE_DESCRIPTOR_FIELDS
VALIDATOR_RESULT_SCHEMA = \
    "AUCDEV-023-CAND730D2B29-REPORT-VALIDATOR-RESULT-V1"
EXECUTION_LIMITS_FIELDS = ("auditor_timeout_seconds",
                           "validator_timeout_seconds",
                           "max_report_bytes")
EXECUTION_LIMITS_MAX_SECONDS = 3600
MAX_REPORT_BYTES_LIMIT = 64 * 1024 * 1024

BINDING_SCHEMA = "AUCDEV-023-CAND730D2B29-BOOTSTRAP-AUTHORITY-BINDING-V1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
IDENTITY_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
EXECUTABLE_VERSION_RE = re.compile(r"^[!-~]{1,64}$")
PATH_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
OUTPUT_KIND = "FIRST_PASS_REPORT"
OUTPUT_IDENTITY_FIELDS = ("kind", "name", "custody_root", "report_source",
                          "custody_dev", "custody_ino")
GATE_EVIDENCE_FIELDS = ("status", "evidence_sha256", "evidence_size",
                        "auditor_role", "attempt_id")
PACKAGE_FIELDS = ("manifest_sha256", "package_sha256")
EVENT_PACKAGE_FIELDS = ("manifest_schema", "package_sha256")
AUDITOR_INVOCATION_MAX_ITEMS = 32
AUDITOR_INVOCATION_ITEM_MAX_BYTES = 1024
AUDITOR_INVOCATION_TOTAL_MAX_BYTES = 8192
# The ONE canonical report-destination option of the frozen auditor
# invocation (RB2-002): its value must equal the frozen report source.
INVOCATION_REPORT_OPTION = "--report"

TOP_LEVEL = ("schema", "policy_id", "event_id", "auditor_role",
             "attempt_id", "target", "common_evidence_manifest_digest",
             "prompt_contract_digest", "auditor_selection",
             "boundary_launcher", "sandbox_profile_id", "tool_wrapper",
             "authority_package", "event_package", "output_identity",
             "static_gate_evidence", "dynamic_gates",
             "auditor_invocation", "output_validator",
             "execution_limits")

# --- the SEPARATE explicitly versioned V2 REPLACEMENT binding contract
# (G2 of the accepted G0-G12 governance order): exactly ONE source-level
# replacement slot for the ACTUAL auditor role AUDITOR_A within the SAME
# single governance event — a CLOSED mapping with NO R2, NO allocator,
# NO sequence counter, NO UUID, NO timestamp-derived id, NO discovery
# and NO fallback; the slot label is NEVER an auditor_role value and
# the spent historical V1 attempt identities are mechanically refused.
# SOURCE-LEVEL CONTRACT MATERIALIZATION ONLY: parsing a V2 document
# creates NO runtime attempt, AccountingStore state, execution
# authority, grant or package binding. ---
BINDING_SCHEMA_V2 = ("AUCDEV-023-CAND730D2B29-BOOTSTRAP-AUTHORITY-"
                     "BINDING-V2")
REPLACEMENT_ATTEMPT_SLOTS = {
    "AUDITOR_A_REPLACEMENT_1": EVENT_ID + "-AUDITOR-A-R1",
}
REPLACEMENT_SLOT_ROLES = {"AUDITOR_A_REPLACEMENT_1": "AUDITOR_A"}
V2_PERMITTED_AUDITOR_ROLES = ("AUDITOR_A",)
TOP_LEVEL_V2 = ("schema", "policy_id", "event_id", "auditor_role",
                "attempt_slot", "attempt_id") + TOP_LEVEL[4:]

# --- versioned strict event-package manifest contract: a frozen event
# package's manifest has an EXACT key set, an EXACT schema tag, exact
# per-file rows, a non-circular package identity, and the COMPLETE
# transport projection below (every binding security dimension EXCEPT
# event_package itself) ---
EVENT_MANIFEST_SCHEMA = "AUCDEV-023-CAND730D2B29-EVENT-PACKAGE-MANIFEST-V1"
EVENT_MANIFEST_KEYS = frozenset(
    ("schema", "transport_binding", "files", "package_sha256"))

# --- versioned strict AUTHORITY-PACKAGE manifest contract (verified
# against the live package bytes at EVERY construction): exact key set
# + the exact semantic values; design ids stay RESERVED-ONLY constants.
AUTHORITY_MANIFEST_SCHEMA = "AUCDEV-023-BOOTSTRAP-AUTHORITY-PACKAGE-MANIFEST-V1"
AUTHORITY_MANIFEST_KEYS = frozenset(
    ("schema", "package", "policy_id", "target", "design_event_id",
     "design_attempt_ids", "status", "qualification_claim",
     "runtime_dependencies", "source_provenance", "files",
     "package_sha256"))
# The SEPARATE V2 authority-manifest schema: every V1 key and every V1
# historical provenance check (design_event_id == EVENT_ID and
# design_attempt_ids == RESERVED_ATTEMPT_IDS verbatim — the pins are
# NOT extended with the replacement identity) PLUS exactly the two
# accepted replacement dimensions: design_replacement_attempt_slots ==
# REPLACEMENT_ATTEMPT_SLOTS and package_grant_identity as the exact
# immutable package-grant reference (the SINGLE 64-hex grant identity
# namespace; the Git-tracked repository MANIFEST stays V1 — NO
# operative grant identity is fabricated; synthetic fixtures only).
AUTHORITY_MANIFEST_SCHEMA_V2 = ("AUCDEV-023-BOOTSTRAP-AUTHORITY-"
                                "PACKAGE-MANIFEST-V2")
AUTHORITY_MANIFEST_KEYS_V2 = frozenset(AUTHORITY_MANIFEST_KEYS | {
    "design_replacement_attempt_slots", "package_grant_identity"})
AUTHORITY_STATUS = "IMPLEMENTATION_CANDIDATE_ONLY / NO_EXECUTION_AUTHORITY"
AUTHORITY_QUALIFICATION_CLAIM = "NONE"
PROJECTION_FIELDS = tuple(name for name in TOP_LEVEL
                          if name != "event_package")
PROJECTION_FIELDS_V2 = tuple(name for name in TOP_LEVEL_V2
                             if name != "event_package")

# Fixed safe semantic report-binding failure tokens (readback 6.6): the
# submitted wrong value, report prose, parser prose and credentials NEVER
# enter a durable reason or accounting record.
REPORT_BINDING_UNPARSEABLE = "REPORT_BINDING_UNPARSEABLE"
REPORT_TARGET_COMMIT_MISMATCH = "REPORT_TARGET_COMMIT_MISMATCH"
REPORT_EVENT_ID_MISMATCH = "REPORT_EVENT_ID_MISMATCH"
REPORT_AUDITOR_ROLE_MISMATCH = "REPORT_AUDITOR_ROLE_MISMATCH"
REPORT_ATTEMPT_ID_MISMATCH = "REPORT_ATTEMPT_ID_MISMATCH"
class BindingError(ValueError):
    """Refused binding document (fail closed)."""
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
    """Strict JSON parse (binding, reports, gate envelopes, manifests):
    UTF-8 only, duplicate keys and non-finite constants refused."""
    if isinstance(data, str):
        data = data.encode()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BindingError("NOT_UTF8") from exc
    try:
        return json.loads(text,
                          object_pairs_hook=_no_duplicate_keys,
                          parse_constant=_reject_constant)
    except BindingError:
        raise
    except json.JSONDecodeError as exc:
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
def _positive_int(value, where, maximum):
    if isinstance(value, bool) or not isinstance(value, int) \
            or not 0 < value <= maximum:
        raise BindingError(f"{where}_INVALID: {value!r}")
    return value
def _safe_relpath(value, where):
    """Safe package-relative POSIX path (charset-bounded segments;
    absolute/empty/"."/".." and non-str refused)."""
    if not isinstance(value, str) or not 0 < len(value) <= 512:
        raise BindingError(f"{where}_NOT_A_SAFE_RELATIVE_PATH")
    for segment in value.split("/"):
        if segment in ("", ".", "..") or not PATH_SEGMENT_RE.match(segment):
            raise BindingError(f"{where}_NOT_A_SAFE_RELATIVE_PATH")
    return value
def _frozen_abs_path(value, where):
    """One frozen authoritative HOST path dimension (BA-PREP-001/002):
    a canonical absolute POSIX path — printable, no control chars, no
    empty/'.'/'..' segment, no trailing '/', bounded length."""
    if not isinstance(value, str) or not 2 <= len(value) <= 4096:
        raise BindingError(f"{where}_NOT_A_FROZEN_ABSOLUTE_PATH")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7f for ch in value):
        raise BindingError(f"{where}_NOT_A_FROZEN_ABSOLUTE_PATH")
    segments = value[1:].split("/")
    if value[0] != "/" or not segments or "" in segments \
            or "." in segments or ".." in segments:
        raise BindingError(f"{where}_NOT_A_FROZEN_ABSOLUTE_PATH")
    return value
def _frozen_object_id(value, where, minimum):
    """One frozen host-local filesystem OBJECT identity component
    (BA-PREP-RB2-001): a plain int (bool refused) at or above `minimum`."""
    if isinstance(value, bool) or not isinstance(value, int) \
            or value < minimum:
        raise BindingError(f"{where}_INVALID: {value!r}")
    return value
def _executable_descriptor(value, where):
    """Frozen executable descriptor: exact keys identity/path/sha256/
    bytes, safe relative path, positive size."""
    _exact_keys(value, EXECUTABLE_DESCRIPTOR_FIELDS, where)
    _identity_field(value["identity"], f"{where}_IDENTITY")
    _safe_relpath(value["path"], f"{where}_PATH")
    _sha_field(value["sha256"], f"{where}_SHA256")
    _positive_int(value["bytes"], f"{where}_BYTES", 2 ** 31 - 1)
    return dict(value)
def _runnable_descriptor(value, where, result_schema):
    """Frozen RUNNABLE descriptor (dynamic gate / validator): the
    executable discipline PLUS the result schema tag and bounded
    timeout/result size — no result, no PASS, ever."""
    _exact_keys(value, RUNNABLE_DESCRIPTOR_FIELDS, where)
    _identity_field(value["identity"], f"{where}_IDENTITY")
    _safe_relpath(value["path"], f"{where}_PATH")
    _sha_field(value["sha256"], f"{where}_SHA256")
    _positive_int(value["bytes"], f"{where}_BYTES", 2 ** 31 - 1)
    if value["result_schema"] != result_schema:
        raise BindingError(f"{where}_RESULT_SCHEMA_UNEXPECTED: "
                           f"{value['result_schema']!r}")
    _positive_int(value["timeout_seconds"], f"{where}_TIMEOUT_SECONDS",
                  EXECUTION_LIMITS_MAX_SECONDS)
    _positive_int(value["max_result_bytes"], f"{where}_MAX_RESULT_BYTES",
                  2 ** 31 - 1)
    return dict(value)
def _invocation_field(value, where):
    """The EXACT frozen auditor-client argv: non-empty ordered bounded
    strings, no control characters; JSON list order."""
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
def _execution_limits_field(value):
    """Frozen bounded execution limits: auditor/validator timeouts and
    the report byte bound, each a strictly-positive int (bool refused)
    under conservative maxima — the ONLY such authority."""
    _exact_keys(value, EXECUTION_LIMITS_FIELDS, "EXECUTION_LIMITS")
    limits = {}
    for key in ("auditor_timeout_seconds", "validator_timeout_seconds"):
        limits[key] = _positive_int(value[key],
                                    f"EXECUTION_LIMITS_{key.upper()}",
                                    EXECUTION_LIMITS_MAX_SECONDS)
    limits["max_report_bytes"] = _positive_int(
        value["max_report_bytes"], "EXECUTION_LIMITS_MAX_REPORT_BYTES",
        MAX_REPORT_BYTES_LIMIT)
    return limits
def _package_fields(value, where):
    """Validate one pinned package-identity pair."""
    _exact_keys(value, PACKAGE_FIELDS, where)
    _sha_field(value["manifest_sha256"], f"{where}_MANIFEST")
    _sha_field(value["package_sha256"], f"{where}_PACKAGE")
    return dict(value)
@dataclass(frozen=True)
class Binding:
    schema: str
    policy_id: str
    event_id: str
    auditor_role: str
    attempt_id: str
    target: dict
    common_evidence_manifest_digest: str
    prompt_contract_digest: str
    auditor_selection: dict
    boundary_launcher: dict
    sandbox_profile_id: str
    tool_wrapper: dict
    authority_package: dict
    event_package: dict
    output_identity: dict
    static_gate_evidence: dict
    dynamic_gates: dict
    auditor_invocation: list
    output_validator: dict
    execution_limits: dict
    digest: str
    attempt_slot: str = None      # V2 replacement slot (None on V1)
def parse_binding(data) -> Binding:
    """Parse and fully validate a frozen PATH-B binding document — the
    HISTORICAL V1 parse route (fail closed; no coercion, no fallback);
    a V2-schema document is refused as any other wrong schema."""
    doc = strict_loads(data)
    _exact_keys(doc, TOP_LEVEL, "BINDING")

    if doc["schema"] != BINDING_SCHEMA:
        raise BindingError(f"BINDING_SCHEMA_UNEXPECTED: {doc['schema']!r}")
    if doc["policy_id"] != POLICY_ID:
        raise BindingError(f"POLICY_ID_UNEXPECTED: {doc['policy_id']!r}")
    if doc["event_id"] != EVENT_ID:
        raise BindingError(f"EVENT_ID_UNEXPECTED: {doc['event_id']!r}")

    role = doc["auditor_role"]
    if role not in ROLES:
        raise BindingError(f"AUDITOR_ROLE_UNKNOWN: {role!r}")
    attempt = doc["attempt_id"]
    if attempt != RESERVED_ATTEMPT_IDS[role]:
        raise BindingError(
            f"ATTEMPT_ID_NOT_THE_RESERVED_IDENTITY_FOR_ROLE: {attempt!r} "
            f"!= {RESERVED_ATTEMPT_IDS[role]!r}")

    common = _common_binding_dimensions(doc, role, attempt)
    return Binding(schema=doc["schema"], policy_id=doc["policy_id"],
                   event_id=doc["event_id"], auditor_role=role,
                   attempt_id=attempt,
                   digest=hashlib.sha256(
                       canonical_bytes(doc)).hexdigest(), **common)
def parse_binding_v2(data) -> Binding:
    """Parse and fully validate a frozen PATH-B REPLACEMENT binding
    document — the SEPARATE explicitly versioned V2 parse route (fail
    closed; no coercion, no fallback, no field-presence auto-detection;
    neither route ever falls back to the other).  Ordered identity
    gates: BINDING_SCHEMA_UNEXPECTED, POLICY_ID_UNEXPECTED,
    EVENT_ID_UNEXPECTED, ATTEMPT_SLOT_MISSING, closed-world keys,
    REPLACEMENT_SLOT_LABEL_NOT_AN_AUDITOR_ROLE,
    AUDITOR_ROLE_NOT_PERMITTED_IN_V2 (excluding every historical V1
    role, hence the spent A-01 identity), ATTEMPT_SLOT_UNKNOWN,
    REPLACEMENT_ATTEMPT_ID_MAY_NOT_REUSE_SPENT_IDENTITY,
    ATTEMPT_ID_NOT_THE_RESERVED_IDENTITY_FOR_SLOT,
    ATTEMPT_SLOT_ATTEMPT_MISMATCH, then the shared V1 tail."""
    doc = strict_loads(data)
    if not isinstance(doc, dict):
        raise BindingError("BINDING_NOT_AN_OBJECT")
    if "attempt_slot" not in doc:
        raise BindingError(
            "ATTEMPT_SLOT_MISSING: the V2 binding contract carries the "
            "replacement attempt-slot dimension explicitly")
    _exact_keys(doc, TOP_LEVEL_V2, "BINDING")

    if doc["schema"] != BINDING_SCHEMA_V2:
        raise BindingError(f"BINDING_SCHEMA_UNEXPECTED: {doc['schema']!r}")
    if doc["policy_id"] != POLICY_ID:
        raise BindingError(f"POLICY_ID_UNEXPECTED: {doc['policy_id']!r}")
    if doc["event_id"] != EVENT_ID:
        raise BindingError(f"EVENT_ID_UNEXPECTED: {doc['event_id']!r}")

    role = doc["auditor_role"]
    if not isinstance(role, str) or role in REPLACEMENT_ATTEMPT_SLOTS:
        raise BindingError(
            f"REPLACEMENT_SLOT_LABEL_NOT_AN_AUDITOR_ROLE: {role!r} is a "
            "replacement slot label, never an auditor_role value")
    if role not in V2_PERMITTED_AUDITOR_ROLES:
        raise BindingError(f"AUDITOR_ROLE_NOT_PERMITTED_IN_V2: {role!r}")
    slot = doc["attempt_slot"]
    if slot not in REPLACEMENT_ATTEMPT_SLOTS:
        raise BindingError(f"ATTEMPT_SLOT_UNKNOWN: {slot!r}")
    attempt = doc["attempt_id"]
    if attempt in set(RESERVED_ATTEMPT_IDS.values()):
        raise BindingError(
            "REPLACEMENT_ATTEMPT_ID_MAY_NOT_REUSE_SPENT_IDENTITY: "
            f"{attempt!r} is a spent historical V1 attempt identity")
    if attempt != REPLACEMENT_ATTEMPT_SLOTS[slot]:
        raise BindingError(
            f"ATTEMPT_ID_NOT_THE_RESERVED_IDENTITY_FOR_SLOT: {attempt!r} "
            f"!= {REPLACEMENT_ATTEMPT_SLOTS[slot]!r}")
    if REPLACEMENT_SLOT_ROLES[slot] != role:
        raise BindingError(
            f"ATTEMPT_SLOT_ATTEMPT_MISMATCH: slot {slot!r} is not a "
            f"{role!r} replacement slot")

    common = _common_binding_dimensions(doc, role, attempt)
    return Binding(schema=doc["schema"], policy_id=doc["policy_id"],
                   event_id=doc["event_id"], auditor_role=role,
                   attempt_id=attempt, attempt_slot=slot,
                   digest=hashlib.sha256(
                       canonical_bytes(doc)).hexdigest(), **common)
def _common_binding_dimensions(doc, role, attempt) -> dict:
    """The shared binding-dimension tail (from `target` onward),
    validated in the EXACT accepted V1 order for BOTH parse routes."""
    _exact_keys(doc["target"], TARGET_KEYS, "TARGET")
    for key in TARGET_KEYS:
        if doc["target"][key] != FROZEN_TARGET[key]:
            raise BindingError(
                f"FROZEN_TARGET_MISMATCH: {key}={doc['target'][key]!r}")

    _sha_field(doc["common_evidence_manifest_digest"],
               "COMMON_EVIDENCE_MANIFEST_DIGEST")
    _sha_field(doc["prompt_contract_digest"], "PROMPT_CONTRACT_DIGEST")
    # Governance-frozen selection: NO fallback/inherit/"auto"/generation
    # substitution/silent downgrade — any substituted selection is
    # refused at parse.
    selection = doc["auditor_selection"]
    _exact_keys(selection, SELECTION_KEYS, "AUDITOR_SELECTION")
    frozen = AUDITOR_SELECTIONS[role]
    for key in ("provider_role", "client_family", "model", "effort"):
        if selection[key] != frozen[key]:
            raise BindingError(
                f"AUDITOR_SELECTION_{key.upper()}_SUBSTITUTED: "
                f"{selection[key]!r} != the governance-frozen "
                f"{frozen[key]!r} for {role}")
    client = selection["client_executable"]
    _exact_keys(client, CLIENT_EXECUTABLE_KEYS, "CLIENT_EXECUTABLE")
    _identity_field(client["identity"], "CLIENT_EXECUTABLE_IDENTITY")
    if not isinstance(client["version"], str) \
            or not EXECUTABLE_VERSION_RE.match(client["version"]):
        raise BindingError("CLIENT_EXECUTABLE_VERSION_INVALID")
    _sha_field(client["sha256"], "CLIENT_EXECUTABLE_SHA256")

    boundary_launcher = _executable_descriptor(
        doc["boundary_launcher"], "BOUNDARY_LAUNCHER")
    _identity_field(doc["sandbox_profile_id"], "SANDBOX_PROFILE_ID")
    tool_wrapper = _executable_descriptor(doc["tool_wrapper"],
                                          "TOOL_WRAPPER")
    authority_package = _package_fields(doc["authority_package"],
                                        "AUTHORITY_PACKAGE")
    _exact_keys(doc["event_package"], EVENT_PACKAGE_FIELDS,
                "EVENT_PACKAGE")
    _sha_field(doc["event_package"]["package_sha256"],
               "EVENT_PACKAGE_PACKAGE")
    if doc["event_package"]["manifest_schema"] != EVENT_MANIFEST_SCHEMA:
        raise BindingError(
            "EVENT_PACKAGE_MANIFEST_SCHEMA_UNEXPECTED: "
            f"{doc['event_package']['manifest_schema']!r}")

    _exact_keys(doc["output_identity"], OUTPUT_IDENTITY_FIELDS,
                "OUTPUT_IDENTITY")
    if doc["output_identity"]["kind"] != OUTPUT_KIND:
        raise BindingError("OUTPUT_KIND_UNEXPECTED")
    if doc["output_identity"]["name"] != output_name_for(attempt):
        raise BindingError("OUTPUT_NAME_NOT_ATTEMPT_DERIVED")
    _frozen_abs_path(doc["output_identity"]["custody_root"],
                     "OUTPUT_CUSTODY_ROOT")
    _frozen_abs_path(doc["output_identity"]["report_source"],
                     "REPORT_SOURCE")
    _frozen_object_id(doc["output_identity"]["custody_dev"],
                      "OUTPUT_CUSTODY_DEV", 0)
    _frozen_object_id(doc["output_identity"]["custody_ino"],
                      "OUTPUT_CUSTODY_INO", 1)
    # RB2-001/002: ONE custody domain — the report source is the
    # authority-created attempt-owned sink, a DIRECT child of the frozen
    # custody root (never the frozen output name), so the sink, the
    # accounting claim and the frozen first pass share ONE held object.
    prefix = doc["output_identity"]["custody_root"] + "/"
    report_source = doc["output_identity"]["report_source"]
    sink_name = report_source[len(prefix):] \
        if report_source.startswith(prefix) else None
    if sink_name is None or "/" in sink_name:
        raise BindingError(
            "REPORT_SOURCE_NOT_A_DIRECT_CHILD_OF_CUSTODY_ROOT: the "
            "report source must be the attempt-owned sink the authority "
            "creates directly inside the frozen custody root")
    if sink_name == doc["output_identity"]["name"]:
        raise BindingError(
            "REPORT_SINK_NAME_COLLIDES_WITH_FROZEN_OUTPUT: the report "
            "sink and the frozen first-pass artifact are distinct names")
    # A package-time PASS for any DYNAMIC gate is exactly the
    # stale-evidence defect — refused FIRST.
    for dynamic_gate in DYNAMIC_GATE_ORDER:
        if dynamic_gate in doc["static_gate_evidence"]:
            raise BindingError(
                f"GATE_EVIDENCE_{dynamic_gate}_FORBIDDEN: "
                f"{dynamic_gate} is a DYNAMIC runtime gate (frozen "
                "executable-artifact descriptor in dynamic_gates), never "
                "a frozen PASS evidence member; a package-time PASS "
                "cannot exist in a valid binding")
    _exact_keys(doc["static_gate_evidence"], REQUIRED_STATIC_GATES,
                "STATIC_GATE_EVIDENCE")
    for gate, evidence in doc["static_gate_evidence"].items():
        _exact_keys(evidence, GATE_EVIDENCE_FIELDS, f"GATE_{gate}")
        if evidence["status"] != "PASS":
            raise BindingError(
                f"GATE_{gate}_NOT_PASS: {evidence['status']!r}")
        _sha_field(evidence["evidence_sha256"], f"GATE_{gate}_EVIDENCE")
        size = evidence["evidence_size"]
        if isinstance(size, bool) or not isinstance(size, int) \
                or not 0 <= size <= 2 ** 31 - 1:
            raise BindingError(f"GATE_{gate}_EVIDENCE_SIZE_INVALID")
        if evidence["auditor_role"] != role:
            raise BindingError(f"GATE_{gate}_ROLE_MISMATCH")
        if evidence["attempt_id"] != attempt:
            raise BindingError(f"GATE_{gate}_ATTEMPT_MISMATCH")
    # Cross-plane consistency: COMMON_EVIDENCE_PARITY must carry the
    # SAME frozen manifest digest the binding declares.
    if doc["static_gate_evidence"]["COMMON_EVIDENCE_PARITY"][
            "evidence_sha256"] != doc["common_evidence_manifest_digest"]:
        raise BindingError(
            "COMMON_EVIDENCE_PARITY_DIGEST_INCONSISTENT: gate evidence "
            "is not the declared common-evidence manifest digest")

    # EXACTLY the three dynamic gates, in frozen descriptor form.
    dynamic = doc["dynamic_gates"]
    _exact_keys(dynamic, DYNAMIC_GATE_ORDER, "DYNAMIC_GATES")
    descriptors = {}
    for dynamic_gate in DYNAMIC_GATE_ORDER:
        descriptors[dynamic_gate] = _runnable_descriptor(
            dynamic[dynamic_gate], f"RUNTIME_GATE_{dynamic_gate}",
            DYNAMIC_GATE_RESULT_SCHEMAS[dynamic_gate])
    validator = _runnable_descriptor(
        doc["output_validator"], "OUTPUT_VALIDATOR",
        VALIDATOR_RESULT_SCHEMA)
    execution_limits = _execution_limits_field(doc["execution_limits"])
    invocation = _invocation_field(doc["auditor_invocation"],
                                   "AUDITOR_INVOCATION")
    # RB2-002: the frozen invocation's designated report destination IS
    # the binding-frozen report sink: exactly ONE canonical report
    # option, exactly one value, EXACT equality — two independently
    # frozen values are not sufficient.
    option_indexes = [index for index, item in enumerate(invocation)
                      if item == INVOCATION_REPORT_OPTION]
    if not option_indexes:
        raise BindingError(
            f"AUDITOR_INVOCATION_REPORT_OPTION_ABSENT: the frozen "
            "auditor invocation must designate its report destination "
            f"with the canonical {INVOCATION_REPORT_OPTION} option")
    if len(option_indexes) > 1:
        raise BindingError(
            "AUDITOR_INVOCATION_REPORT_OPTION_DUPLICATE: an ambiguous "
            "report destination is refused fail-closed")
    value_index = option_indexes[0] + 1
    if value_index >= len(invocation):
        raise BindingError(
            f"AUDITOR_INVOCATION_REPORT_VALUE_ABSENT: the canonical "
            f"{INVOCATION_REPORT_OPTION} option has no destination value")
    if invocation[value_index] != report_source:
        raise BindingError(
            "AUDITOR_INVOCATION_REPORT_SINK_MISMATCH: the invocation's "
            "designated report destination is not the binding-frozen "
            "attempt report source")

    return {"target": dict(doc["target"]),
            "common_evidence_manifest_digest": doc[
                "common_evidence_manifest_digest"],
            "prompt_contract_digest": doc["prompt_contract_digest"],
            "auditor_selection": dict(selection),
            "boundary_launcher": boundary_launcher,
            "sandbox_profile_id": doc["sandbox_profile_id"],
            "tool_wrapper": tool_wrapper,
            "authority_package": authority_package,
            "event_package": dict(doc["event_package"]),
            "output_identity": dict(doc["output_identity"]),
            "static_gate_evidence": {k: dict(v) for k, v in
                                     doc["static_gate_evidence"].items()},
            "dynamic_gates": descriptors,
            "auditor_invocation": invocation,
            "output_validator": validator,
            "execution_limits": execution_limits}
def binding_projection(binding: Binding) -> dict:
    """Canonical transport projection of a parsed binding: the EXACT
    value a frozen event-package manifest's transport_binding must
    equal (compared as canonical JSON bytes, so type confusions such as
    true==1 cannot pass); covers every projection dimension of the
    binding's OWN schema version (V2 adds exactly attempt_slot),
    event_package EXCLUDED (non-circular).  Internal use only."""
    fields = PROJECTION_FIELDS_V2 if binding.schema == BINDING_SCHEMA_V2 \
        else PROJECTION_FIELDS
    return {name: getattr(binding, name) for name in fields}


# --- the immutable NON-EXECUTION package-binding grant V2 (accepted
# schema AUCDEV-023-PACKAGE-BINDING-GRANT-V2; UNISSUED — SOURCE
# mechanics only: NO grant is minted, NO grant bytes exist, NO runtime
# surface consumes one): a strictly-schema'd flat closed-world
# 20-field document in the EXACT fixed canonical field order below,
# whose grant_identity is SHA-256 of the EXACT canonical bytes — the
# SINGLE 64-hex grant identity namespace. ---
GRANT_SCHEMA = "AUCDEV-023-PACKAGE-BINDING-GRANT-V2"
GRANT_FIELDS = ("schema", "purpose", "operator_authority_id",
                "authorization_record_path", "authorization_commit_sha",
                "authorization_record_blob_sha1",
                "authorization_record_sha256", "governance_event_id",
                "auditor_role", "attempt_slot", "future_machine_attempt_id",
                "frozen_target_commit", "frozen_target_tree",
                "accepted_active_v3_procedure_sha256",
                "accepted_active_v3_binding_sha256", "one_package_only",
                "execution_authority", "secret_material", "expiry_policy",
                "issuance_semantics")
GRANT_PURPOSE = "NON_EXECUTION_PACKAGE_BINDING"
GRANT_FROZEN_TARGET_COMMIT = FROZEN_TARGET["commit"]
GRANT_FROZEN_TARGET_TREE = FROZEN_TARGET["root_tree"]
GRANT_ACTIVE_V3_PROCEDURE_SHA256 = ("32460cd5011c29efd042e2a4c79f09efa"
                                    "bb2662a211f2822410e6ee309f7852e")
GRANT_ACTIVE_V3_BINDING_SHA256 = ("801279b546ec0c0b590a9d7a3cf9993cb0"
                                  "cbd51c99a84830ee870cac945cae12")
GRANT_EXECUTION_AUTHORITY = "NONE"
GRANT_SECRET_MATERIAL = "NONE"
GRANT_EXPIRY_POLICY = "NO_EXPIRY"
GRANT_ISSUANCE_SEMANTICS = "IMMUTABLE_NON_EXECUTION_PACKAGE_BINDING_GRANT"
GRANT_MUTABLE_LIFECYCLE_FIELD_NAMES = frozenset(("lifecycle_state",))
def grant_canonical_bytes(document: dict) -> bytes:
    """EXACT canonical serialization of the immutable grant: strict JSON,
    exactly the 20 fields in the EXACT fixed order, compact separators,
    UTF-8, no BOM/comments/duplicate keys/trailing newline."""
    if not isinstance(document, dict):
        raise BindingError("GRANT_NOT_AN_OBJECT")
    got, want = set(document), set(GRANT_FIELDS)
    if got != want:
        if (got - want) & GRANT_MUTABLE_LIFECYCLE_FIELD_NAMES:
            raise BindingError(
                f"GRANT_MUTABLE_FIELD_PRESENT: {sorted(got - want)}")
        raise BindingError(
            f"GRANT_FIELD_UNKNOWN_OR_MISSING: unknown={sorted(got - want)} "
            f"missing={sorted(want - got)}")
    return json.dumps({name: document[name] for name in GRANT_FIELDS},
                      separators=(",", ":")).encode()
def grant_identity(canonical: bytes) -> str:
    """grant_identity = SHA-256(EXACT canonical grant bytes) — the single
    64-hex grant identity namespace (deterministic, non-secret,
    recomputable by any verifier; NEVER minted at runtime)."""
    return hashlib.sha256(canonical).hexdigest()
def _validated_grant_document(data) -> tuple:
    """Parse, canonically re-derive and fully validate ONE immutable
    AUCDEV-023-PACKAGE-BINDING-GRANT-V2 document (fail closed) and
    return (document, canonical_bytes); all refusal families apply."""
    raw = data.encode() if isinstance(data, str) else data
    doc = strict_loads(raw)
    canonical = grant_canonical_bytes(doc)
    if canonical != raw:
        raise BindingError(
            "GRANT_CANONICALIZATION_INVALID: the bytes are not the exact "
            "canonical serialization (fixed field order, compact "
            "separators, no whitespace/BOM/trailing newline)")
    if doc["schema"] != GRANT_SCHEMA:
        raise BindingError(f"GRANT_SCHEMA_UNEXPECTED: {doc['schema']!r}")
    if doc["purpose"] != GRANT_PURPOSE:
        raise BindingError(f"GRANT_PURPOSE_INVALID: {doc['purpose']!r}")
    if doc["governance_event_id"] != EVENT_ID:
        raise BindingError(
            f"GRANT_EVENT_MISMATCH: {doc['governance_event_id']!r}")
    if not isinstance(doc["auditor_role"], str) \
            or doc["auditor_role"] in REPLACEMENT_ATTEMPT_SLOTS \
            or doc["auditor_role"] != REPLACEMENT_SLOT_ROLES[
                "AUDITOR_A_REPLACEMENT_1"]:
        raise BindingError(f"GRANT_ROLE_SLOT_MISMATCH: "
                           f"{doc['auditor_role']!r}")
    if doc["attempt_slot"] != "AUDITOR_A_REPLACEMENT_1":
        raise BindingError(f"GRANT_ATTEMPT_SLOT_MISMATCH: "
                           f"{doc['attempt_slot']!r}")
    if doc["future_machine_attempt_id"] != \
            REPLACEMENT_ATTEMPT_SLOTS["AUDITOR_A_REPLACEMENT_1"]:
        raise BindingError("GRANT_ATTEMPT_SLOT_MISMATCH: "
                           f"{doc['future_machine_attempt_id']!r}")
    if doc["frozen_target_commit"] != GRANT_FROZEN_TARGET_COMMIT or \
            doc["frozen_target_tree"] != GRANT_FROZEN_TARGET_TREE:
        raise BindingError("GRANT_TARGET_MISMATCH")
    if doc["accepted_active_v3_procedure_sha256"] != \
            GRANT_ACTIVE_V3_PROCEDURE_SHA256 or \
            doc["accepted_active_v3_binding_sha256"] != \
            GRANT_ACTIVE_V3_BINDING_SHA256:
        raise BindingError("GRANT_ACTIVE_V3_STALE")
    if doc["execution_authority"] != GRANT_EXECUTION_AUTHORITY:
        raise BindingError("GRANT_EXECUTION_AUTHORITY_CLAIM_INVALID: "
                           f"{doc['execution_authority']!r}")
    if doc["secret_material"] != GRANT_SECRET_MATERIAL:
        raise BindingError(f"GRANT_SECRET_MATERIAL_INVALID: "
                           f"{doc['secret_material']!r}")
    if doc["one_package_only"] is not True:
        raise BindingError("GRANT_LIFECYCLE_FIELD_INVALID: one_package_only"
                           f"={doc['one_package_only']!r}")
    if doc["expiry_policy"] != GRANT_EXPIRY_POLICY:
        raise BindingError(f"GRANT_LIFECYCLE_FIELD_INVALID: "
                           f"{doc['expiry_policy']!r}")
    if doc["issuance_semantics"] != GRANT_ISSUANCE_SEMANTICS:
        raise BindingError(f"GRANT_LIFECYCLE_FIELD_INVALID: "
                           f"{doc['issuance_semantics']!r}")
    _identity_field(doc["operator_authority_id"],
                    "GRANT_OPERATOR_AUTHORITY_ID")
    _safe_relpath(doc["authorization_record_path"],
                  "GRANT_AUTHORIZATION_RECORD_PATH")
    for field in ("authorization_commit_sha",
                  "authorization_record_blob_sha1"):
        if not isinstance(doc[field], str) or not SHA1_RE.match(doc[field]):
            raise BindingError(f"GRANT_{field.upper()}_INVALID")
    _sha_field(doc["authorization_record_sha256"],
               "GRANT_AUTHORIZATION_RECORD_SHA256")
    return doc, canonical
def parse_package_grant(data, expected_grant_identity=None) -> str:
    """Fully validate ONE immutable grant document (above) and return
    its grant_identity; with expected_grant_identity the DERIVED
    identity is cross-checked (one namespace, no second identity)."""
    _doc, canonical = _validated_grant_document(data)
    identity = grant_identity(canonical)
    if expected_grant_identity is not None \
            and identity != expected_grant_identity:
        raise BindingError(
            f"GRANT_IDENTITY_MISMATCH: claimed "
            f"{expected_grant_identity!r} != derived {identity!r}")
    return identity
def check_package_grant_reference(claimed_grant_identity,
                                  grant_bytes=None) -> str:
    """The minimum accepted V2 grant-reference consistency cross-check:
    the ONE 64-hex grant identity namespace must agree wherever the V2
    contract represents it (manifest package_grant_identity, receipt
    grant_identity, grant_identity of the exact grant bytes); with
    grant bytes supplied they are fully parsed and the DERIVED identity
    must EQUAL the claim — no second namespace, runtime NEVER mints."""
    if not isinstance(claimed_grant_identity, str) \
            or not SHA256_RE.match(claimed_grant_identity):
        raise BindingError("GRANT_IDENTITY_MALFORMED")
    if grant_bytes is None:
        return claimed_grant_identity
    return parse_package_grant(
        grant_bytes, expected_grant_identity=claimed_grant_identity)


# --- the NON-RUNTIME package-binding receipt V1 SOURCE PRIMITIVE
# (accepted schema AUCDEV-023-PACKAGE-BINDING-RECEIPT-V1; UNCREATED —
# source mechanics only, NO operative receipt exists): ONE canonical
# namespace pinned by the VERIFIED future G7 context below (NEVER a
# caller-selected root), the receipt context derived from the EXACT
# canonical grant bytes and the EXACT frozen package artifact, ONE
# record per grant_identity created O_EXCL mode 0600 (fsync file then
# directory), duplicate FAILS CLOSED, NO update/append/rebind/reuse
# API; the namespace is NEVER AccountingStore, NEVER the frozen event
# runtime root, NEVER a Git-tracked operative path; ZERO execution
# authority. ---
RECEIPT_SCHEMA = "AUCDEV-023-PACKAGE-BINDING-RECEIPT-V1"
RECEIPT_FIELDS = ("schema", "grant_identity", "package_sha256",
                  "governance_event_id", "auditor_role", "attempt_slot",
                  "attempt_id", "operator_authority_id",
                  "created_under_package_binding_authority",
                  "binding_semantics")
RECEIPT_BINDING_SEMANTICS = \
    "ONE_SHOT_IMMUTABLE_NON_RUNTIME_PACKAGE_BINDING"
RECEIPT_MODE = 0o600
RECEIPT_NAME_SUFFIX = ".package-binding-receipt.json"
def receipt_name(grant_identity: str) -> str:
    """The deterministic receipt record name (ONE per grant_identity)."""
    if not isinstance(grant_identity, str) \
            or not SHA256_RE.match(grant_identity):
        raise BindingError("GRANT_IDENTITY_MALFORMED")
    return grant_identity + RECEIPT_NAME_SUFFIX
def receipt_canonical_bytes(document: dict) -> bytes:
    """EXACT canonical receipt serialization (exact fields, fixed
    order, compact separators, no trailing newline)."""
    if not isinstance(document, dict):
        raise BindingError("RECEIPT_NOT_AN_OBJECT")
    _exact_keys(document, RECEIPT_FIELDS, "RECEIPT")
    return json.dumps({name: document[name] for name in RECEIPT_FIELDS},
                      separators=(",", ":")).encode()
def parse_package_binding_receipt(data) -> dict:
    """Parse and fully validate ONE package-binding receipt record (fail
    closed): exact closed key world, exact schema tag, well-formed
    identities and the exact replacement-contract values — ANY
    inconsistency is RECEIPT_MISMATCH_REFUSED."""
    doc = strict_loads(data)
    if not isinstance(doc, dict):
        raise BindingError("RECEIPT_NOT_AN_OBJECT")
    _exact_keys(doc, RECEIPT_FIELDS, "RECEIPT")
    if doc["schema"] != RECEIPT_SCHEMA:
        raise BindingError(f"RECEIPT_SCHEMA_UNEXPECTED: {doc['schema']!r}")
    _sha_field(doc["grant_identity"], "RECEIPT_GRANT_IDENTITY")
    _sha_field(doc["package_sha256"], "RECEIPT_PACKAGE_SHA256")
    _identity_field(doc["operator_authority_id"],
                    "RECEIPT_OPERATOR_AUTHORITY_ID")
    if doc["created_under_package_binding_authority"] is not True:
        raise BindingError("RECEIPT_MISMATCH_REFUSED: "
                           "created_under_package_binding_authority")
    if doc["governance_event_id"] != EVENT_ID \
            or not isinstance(doc["auditor_role"], str) \
            or doc["auditor_role"] in REPLACEMENT_ATTEMPT_SLOTS \
            or doc["auditor_role"] != REPLACEMENT_SLOT_ROLES[
                "AUDITOR_A_REPLACEMENT_1"] \
            or doc["attempt_slot"] != "AUDITOR_A_REPLACEMENT_1" \
            or doc["attempt_id"] != REPLACEMENT_ATTEMPT_SLOTS[
                "AUDITOR_A_REPLACEMENT_1"] \
            or doc["binding_semantics"] != RECEIPT_BINDING_SEMANTICS:
        raise BindingError(
            "RECEIPT_MISMATCH_REFUSED: the receipt does not carry the "
            "exact replacement-contract event/role/slot/attempt/binding "
            "values")
    return {name: doc[name] for name in RECEIPT_FIELDS}


# --- the strict closed-world VERIFIED future G7 mint-publication
# context — the RECEIPT NAMESPACE AUTHORITY (future NON-RUNTIME
# package tooling / Control Room independently derives and verifies
# the canonical G7 publication under the accepted PUBID/DIFFSEM
# selector; this primitive validates strict shape and identity syntax
# ONLY, NOT Git governance).  The minimal non-secret namespace
# identity the future G7 semantic payload carries for G10 is EXACTLY
# G7_NAMESPACE_PAYLOAD_KEYS — absolute normalized path (never
# repository-relative, never caller-composed at receipt time) plus the
# exact established namespace directory OBJECT identity. ---
G7_MINT_PUBLICATION_RECORD_PATH = ("docs/chatgpt-project/AUCDEV-023-PCH6-B-"
                                   "PATH-B-REPLACEMENT-AUDITOR-A-GRANT-MINT-"
                                   "PUBLICATION.md")
G7_NAMESPACE_PAYLOAD_KEYS = ("receipt_namespace_path",
                             "receipt_namespace_st_dev",
                             "receipt_namespace_st_ino")
VERIFIED_G7_CONTEXT_KEYS = ("grant_mint_publication_commit_sha",
                            "grant_mint_publication_root_tree",
                            "grant_mint_publication_record_path",
                            "grant_mint_publication_record_blob_sha1",
                            "grant_mint_publication_record_sha256",
                            "grant_identity") + G7_NAMESPACE_PAYLOAD_KEYS
def parse_verified_g7_context(data) -> dict:
    """Parse and fully validate ONE strict VERIFIED G7 context (fail
    closed): exact closed key world, exact reserved record path,
    well-formed identities, canonical namespace path and plain-int
    object ids — no arbitrary local object can pose as canonical."""
    doc = data if isinstance(data, dict) else strict_loads(data)
    _exact_keys(doc, VERIFIED_G7_CONTEXT_KEYS, "G7_CONTEXT")
    for field, pattern in (
            ("grant_mint_publication_commit_sha", SHA1_RE),
            ("grant_mint_publication_root_tree", SHA1_RE),
            ("grant_mint_publication_record_blob_sha1", SHA1_RE),
            ("grant_mint_publication_record_sha256", SHA256_RE),
            ("grant_identity", SHA256_RE)):
        if not isinstance(doc[field], str) or not pattern.match(doc[field]):
            raise BindingError(f"G7_CONTEXT_{field.upper()}_INVALID")
    if doc["grant_mint_publication_record_path"] != \
            G7_MINT_PUBLICATION_RECORD_PATH:
        raise BindingError(
            "G7_CONTEXT_RECORD_PATH_UNEXPECTED: the context must name the "
            "exact reserved canonical G7 mint-publication record path")
    _frozen_abs_path(doc["receipt_namespace_path"], "RECEIPT_NAMESPACE_PATH")
    context = {name: doc[name] for name in VERIFIED_G7_CONTEXT_KEYS}
    context["receipt_namespace_st_dev"] = _frozen_object_id(
        doc["receipt_namespace_st_dev"], "RECEIPT_NAMESPACE_ST_DEV", 0)
    context["receipt_namespace_st_ino"] = _frozen_object_id(
        doc["receipt_namespace_st_ino"], "RECEIPT_NAMESPACE_ST_INO", 1)
    return context
def _open_verified_receipt_namespace(context: dict) -> int:
    """Open and verify THE canonical NON-RUNTIME receipt namespace
    carried by the VERIFIED G7 context (never a caller-selected root):
    opened O_NOFOLLOW at the context's exact absolute path; a real
    owner-uid directory, not group/world writable, that IS the exact
    pinned OBJECT (live st_dev/st_ino == the pair — anything else is
    RECEIPT_NAMESPACE_IDENTITY_MISMATCH); held as an fd."""
    try:
        fd = os.open(context["receipt_namespace_path"],
                     os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as exc:
        raise BindingError(f"RECEIPT_NAMESPACE_UNOPENABLE: {exc!r}") from exc
    try:
        info = os.fstat(fd)
        if not stat.S_ISDIR(info.st_mode):
            raise BindingError("RECEIPT_NAMESPACE_NOT_A_DIRECTORY")
        if info.st_uid != os.geteuid():
            raise BindingError("RECEIPT_NAMESPACE_NOT_OWNER_UID")
        if info.st_mode & 0o022:
            raise BindingError("RECEIPT_NAMESPACE_GROUP_OR_WORLD_WRITABLE")
        if info.st_dev != context["receipt_namespace_st_dev"] \
                or info.st_ino != context["receipt_namespace_st_ino"]:
            raise BindingError(
                "RECEIPT_NAMESPACE_IDENTITY_MISMATCH: the live namespace "
                "object is not the exact pinned G7-context object")
    except Exception:
        os.close(fd)
        raise
    return fd
def derive_frozen_package_sha256(package_artifact) -> str:
    """Derive package_sha256 from the EXACT frozen package artifact
    bytes (never a naked caller digest): opened without following
    symlinks, regular file required, hashed from the held object."""
    try:
        fd = os.open(os.fspath(package_artifact),
                     os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise BindingError(f"PACKAGE_ARTIFACT_UNOPENABLE: {exc!r}") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise BindingError("PACKAGE_ARTIFACT_NOT_A_REGULAR_FILE")
        digest = hashlib.sha256()
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            digest.update(chunk)
    finally:
        os.close(fd)
    return digest.hexdigest()
def _derived_receipt_context(verified_g7_context, grant_bytes) -> tuple:
    """Parse the VERIFIED G7 context and the EXACT canonical grant
    bytes, cross-checking the single grant identity namespace (the
    context's grant_identity MUST equal the DERIVED identity — a naked
    caller digest is never trusted); returns (context, document, id)."""
    context = parse_verified_g7_context(verified_g7_context)
    document, canonical = _validated_grant_document(grant_bytes)
    identity = grant_identity(canonical)
    if identity != context["grant_identity"]:
        raise BindingError(
            "RECEIPT_GRANT_CONTEXT_MISMATCH: the verified G7 context does "
            "not name the exact supplied grant identity")
    return context, document, identity
def _crosscheck_receipt(validated, grant_document, identity,
                        package_sha256) -> None:
    """The grant-derived receipt-context relation: the receipt must
    agree with the EXACT parsed grant bytes on every dimension and with
    the independently derived package digest (fail closed)."""
    for field, derived in (
            ("grant_identity", identity),
            ("operator_authority_id",
             grant_document["operator_authority_id"]),
            ("governance_event_id", grant_document["governance_event_id"]),
            ("auditor_role", grant_document["auditor_role"]),
            ("attempt_slot", grant_document["attempt_slot"]),
            ("attempt_id", grant_document["future_machine_attempt_id"])):
        if validated[field] != derived:
            raise BindingError(
                f"RECEIPT_MISMATCH_REFUSED: {field} != the grant-derived "
                "value of the exact canonical grant bytes")
    if validated["package_sha256"] != package_sha256:
        raise BindingError(
            "PACKAGE_SUBSTITUTION_REFUSED: the receipt does not bind the "
            "digest derived from the exact frozen package artifact")
def write_package_binding_receipt(verified_g7_context, grant_bytes,
                                  package_artifact, record: dict) -> dict:
    """NON-RUNTIME package-binding receipt SOURCE PRIMITIVE (NOT a
    BootstrapAuthority operation; ZERO execution authority; NO
    AccountingStore state): requires the VERIFIED canonical G7
    context, the EXACT canonical grant bytes and the EXACT frozen
    package artifact — derives grant_identity, the grant-dimension
    receipt context and package_sha256 ITSELF, derives the namespace
    SOLELY from the verified context (NO raw-root authority input),
    verifies the exact namespace OBJECT, then creates the ONE receipt
    per grant_identity O_EXCL mode 0600 relative to the held fd (fsync
    file then directory); a duplicate FAILS CLOSED; no
    update/rebind/reuse surface exists."""
    context, document, identity = _derived_receipt_context(
        verified_g7_context, grant_bytes)
    package_sha256 = derive_frozen_package_sha256(package_artifact)
    canonical = receipt_canonical_bytes(record)
    _crosscheck_receipt(parse_package_binding_receipt(canonical), document,
                        identity, package_sha256)
    name = receipt_name(identity)
    dir_fd = _open_verified_receipt_namespace(context)
    try:
        try:
            fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | os.O_NOFOLLOW, RECEIPT_MODE, dir_fd=dir_fd)
        except FileExistsError as exc:
            raise BindingError(
                "DUPLICATE_PACKAGE_BINDING_REFUSED: a receipt already "
                "exists for this grant identity in the canonical "
                "namespace (one record per grant_identity; no rebind, "
                "no reuse)") from exc
        except OSError as exc:
            raise BindingError(
                f"RECEIPT_CREATE_REFUSED: {exc!r}") from exc
        try:
            os.write(fd, canonical)
            os.fsync(fd)
        finally:
            os.close(fd)
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
    return {"path": name, "sha256": hashlib.sha256(canonical).hexdigest(),
            "size": len(canonical), "grant_identity": identity,
            "package_sha256": package_sha256}
def verify_package_binding_receipt(verified_g7_context, grant_bytes,
                                   package_artifact) -> dict:
    """Verify the ONE receipt bound to grant_identity against the
    independently re-derived context (fail closed): namespace from the
    VERIFIED G7 context, grant identity/dimensions from the EXACT
    grant bytes, package_sha256 from the EXACT frozen artifact; the
    receipt file (no symlink) must BE the exact canonical record.
    Confers ZERO execution authority."""
    context, document, identity = _derived_receipt_context(
        verified_g7_context, grant_bytes)
    package_sha256 = derive_frozen_package_sha256(package_artifact)
    name = receipt_name(identity)
    dir_fd = _open_verified_receipt_namespace(context)
    try:
        try:
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
        except OSError as exc:
            raise BindingError(
                f"RECEIPT_ABSENT_OR_UNOPENABLE: {exc!r}") from exc
        try:
            data = b""
            while True:
                chunk = os.read(fd, 65536)
                if not chunk:
                    break
                data += chunk
        finally:
            os.close(fd)
    finally:
        os.close(dir_fd)
    validated = parse_package_binding_receipt(data)
    if receipt_canonical_bytes(validated) != data:
        raise BindingError("RECEIPT_CANONICALIZATION_INVALID")
    _crosscheck_receipt(validated, document, identity, package_sha256)
    return validated
