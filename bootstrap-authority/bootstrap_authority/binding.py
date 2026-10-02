"""Strict frozen-binding parser for the AUCDEV-023 PCH6-B PATH-B
candidate-specific target-independent bootstrap authority.

NEW authority-specific source for the wholly NEW PATH-B lineage
(Control Room design readback 2026-10-02); shares NO code with, and
imports NOTHING from, the audit target
`730d2b29:bootstrap-supervisor/**` (AUDIT SUBJECT, never authority)
or the legacy EBS at `068f5e2` (REFERENCE_ONLY).

Fail-closed validation of the operator-declared attempt binding
document against the PATH-B policy identity, the frozen fresh-audit
target, the design-reserved event/attempt identities and the
governance-frozen auditor selections: unknown fields, wrong types,
malformed digests, wrong target identity, wrong event/role/attempt
pairing, substituted model/effort/client selections, and incomplete or
non-PASS static gate evidence are all refused.  The output identity
additionally freezes the attempt's authoritative output-custody root
and report-source path as canonical absolute paths (BA-PREP-001/002),
so caller path substitution is refused at the authority boundary.
The policy is candidate-specific — NOT standing authority for any
other candidate.  Every dimension is mandatory and digest-covered by
`Binding.digest` (swapping ANY dimension changes the digest, which
the store and authority refuse for the same attempt); synthetic test
documents are built in tests/conftest.py (no doc-builder in the TCB).

Gate split (PATH-B): the EIGHT STATIC preparation gates are frozen
PASS evidence members; the THREE DYNAMIC runtime gates
(CLIENT_SELECTION_PREFLIGHT, NETWORK_READINESS, RESOURCE_GATE, in
that required order) are NOT frozen evidence: each is frozen as an
exact executable-artifact DESCRIPTOR (identity, safe package-relative
path, exact SHA-256/byte size/result schema, bounded timeout/result
size) and EXECUTED fresh exactly once inside the ONE public
preexec-consumption operation — a package-time PASS for any dynamic
gate cannot exist in a valid binding; CLIENT_SELECTION_PREFLIGHT is
the NO-FALLBACK enforcement point (no fallback, inherit, "auto",
generation substitution or silent downgrade).

This module also defines the VERSIONED STRICT EVENT-PACKAGE MANIFEST
and AUTHORITY-PACKAGE MANIFEST contracts (exact key sets, schema
tags, file rows, non-circular package identities: package_sha256
covers the document EXCLUDING its own field) and the canonical
transport projection `binding_projection`, established mechanically
by runtime.verify_event_package BEFORE GATES_PASSED.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

POLICY_ID = ("AUCDEV-023-PCH6B-CAND730D2B29-TARGET-INDEPENDENT-"
             "BOOTSTRAP-AUTHORITY-V1")

# The one frozen fresh-audit target accepted by this policy (readback
# 6.5); any other target is refused before inference can become
# reachable.
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
# binding constants ONLY — parsing them does NOT instantiate the event,
# mint attempt capability, grant execution, or consume an engagement;
# synthetic fixtures using them are NON-AUTHORITATIVE / ZERO-PROVIDER /
# NON-PERSISTENT.
EVENT_ID = "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01"
RESERVED_ATTEMPT_IDS = {
    "AUDITOR_A":
        "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01",
    "AUDITOR_B":
        "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-B-01",
}
ROLES = ("AUDITOR_A", "AUDITOR_B")

# Governance-frozen auditor selections (readback 6.8) — explicit, never
# ambient/default/current/auto, never inherited, NO fallback of any
# kind; the client executable identity/version/SHA-256 are frozen from
# values supplied by the LATER event package, never invented here.
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
# CLIENT_SELECTION_PREFLIGHT first (the no-fallback model/effort/client
# enforcement point), NETWORK_READINESS second, RESOURCE_GATE LAST as
# the final live environmental gate before durable consumption.  None
# may EVER appear as a frozen PASS evidence member (a package-time
# PASS would go stale before the separately authorized execution).
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
# gate or the structural validator) adds the result schema tag, a
# bounded timeout, and a bounded result size.  The structural
# validator is SHAPE-ONLY for target_commit (runtime.check_report_binding
# is the binding authority); the execution limits are the ONLY
# timeout/report-size authority.
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
IDENTITY_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
EXECUTABLE_VERSION_RE = re.compile(r"^[!-~]{1,64}$")
PATH_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
OUTPUT_KIND = "FIRST_PASS_REPORT"
OUTPUT_IDENTITY_FIELDS = ("kind", "name", "custody_root", "report_source")
GATE_EVIDENCE_FIELDS = ("status", "evidence_sha256", "evidence_size",
                        "auditor_role", "attempt_id")
PACKAGE_FIELDS = ("manifest_sha256", "package_sha256")
EVENT_PACKAGE_FIELDS = ("manifest_schema", "package_sha256")
AUDITOR_INVOCATION_MAX_ITEMS = 32
AUDITOR_INVOCATION_ITEM_MAX_BYTES = 1024
AUDITOR_INVOCATION_TOTAL_MAX_BYTES = 8192

TOP_LEVEL = ("schema", "policy_id", "event_id", "auditor_role",
             "attempt_id", "target", "common_evidence_manifest_digest",
             "prompt_contract_digest", "auditor_selection",
             "boundary_launcher", "sandbox_profile_id", "tool_wrapper",
             "authority_package", "event_package", "output_identity",
             "static_gate_evidence", "dynamic_gates",
             "auditor_invocation", "output_validator",
             "execution_limits")

# --- versioned strict event-package manifest contract: a frozen event
# package's manifest has an EXACT key set, an EXACT schema tag, exact
# per-file rows, a non-circular package identity, and the COMPLETE
# transport projection below (every binding security dimension EXCEPT
# event_package itself, whose identity is pinned independently by the
# binding — no circular self-hashing). ---
EVENT_MANIFEST_SCHEMA = "AUCDEV-023-CAND730D2B29-EVENT-PACKAGE-MANIFEST-V1"
EVENT_MANIFEST_KEYS = frozenset(
    ("schema", "transport_binding", "files", "package_sha256"))

# --- versioned strict AUTHORITY-PACKAGE manifest contract (verified
# against the live package bytes by runtime.verify_own_package at
# EVERY construction): exact key set + the exact semantic values below;
# the design ids stay RESERVED-ONLY binding constants.
AUTHORITY_MANIFEST_SCHEMA = "AUCDEV-023-BOOTSTRAP-AUTHORITY-PACKAGE-MANIFEST-V1"
AUTHORITY_MANIFEST_KEYS = frozenset(
    ("schema", "package", "policy_id", "target", "design_event_id",
     "design_attempt_ids", "status", "qualification_claim",
     "runtime_dependencies", "source_provenance", "files",
     "package_sha256"))
AUTHORITY_STATUS = "IMPLEMENTATION_CANDIDATE_ONLY / NO_EXECUTION_AUTHORITY"
AUTHORITY_QUALIFICATION_CLAIM = "NONE"
PROJECTION_FIELDS = tuple(name for name in TOP_LEVEL
                          if name != "event_package")

# Fixed safe semantic report-binding failure tokens (readback 6.6): the
# submitted wrong value, report prose, parser exception prose and
# credentials NEVER enter a durable reason or accounting record.
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
    UTF-8 only, duplicate keys refused, non-finite constants refused,
    no fallback."""
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
    """Safe event-package-relative POSIX path (charset-bounded
    segments; absolute paths, empty segments, "."/".." traversal and
    non-str types are refused)."""
    if not isinstance(value, str) or not 0 < len(value) <= 512:
        raise BindingError(f"{where}_NOT_A_SAFE_RELATIVE_PATH")
    for segment in value.split("/"):
        if segment in ("", ".", "..") or not PATH_SEGMENT_RE.match(segment):
            raise BindingError(f"{where}_NOT_A_SAFE_RELATIVE_PATH")
    return value


def _frozen_abs_path(value, where):
    """One frozen authoritative HOST path dimension (BA-PREP-001/002):
    an absolute POSIX path in exact canonical form — printable non-empty
    UTF-8 (no control characters), leading '/', no empty/'.'/'..'
    segment, no trailing '/', bounded length; every non-canonical form
    is refused at parse so the frozen form IS the canonical comparison
    form (the runtime identity gate compares against it)."""
    if not isinstance(value, str) or not 2 <= len(value) <= 4096:
        raise BindingError(f"{where}_NOT_A_FROZEN_ABSOLUTE_PATH")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7f for ch in value):
        raise BindingError(f"{where}_NOT_A_FROZEN_ABSOLUTE_PATH")
    segments = value[1:].split("/")
    if value[0] != "/" or not segments or "" in segments \
            or "." in segments or ".." in segments:
        raise BindingError(f"{where}_NOT_A_FROZEN_ABSOLUTE_PATH")
    return value


def _executable_descriptor(value, where):
    """One frozen executable-artifact descriptor (launcher/wrapper):
    exact keys identity/path/sha256/bytes, safe relative path,
    strictly positive byte size."""
    _exact_keys(value, EXECUTABLE_DESCRIPTOR_FIELDS, where)
    _identity_field(value["identity"], f"{where}_IDENTITY")
    _safe_relpath(value["path"], f"{where}_PATH")
    _sha_field(value["sha256"], f"{where}_SHA256")
    _positive_int(value["bytes"], f"{where}_BYTES", 2 ** 31 - 1)
    return dict(value)


def _runnable_descriptor(value, where, result_schema):
    """One frozen RUNNABLE executable-artifact descriptor (a dynamic
    gate or the structural validator): the executable discipline PLUS
    the exact result schema tag, a bounded timeout and a bounded
    accepted-result size — no result and no PASS can appear here."""
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
    strings with no control character; ordering is exactly the JSON list
    order; no caller argv tail can extend it."""
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
    """The frozen bounded execution limits: auditor wait timeout,
    validator timeout and report byte bound, each a strictly-positive
    int (bool refused) under conservative maxima — the ONLY timeout/
    size authority on the post-consumption path."""
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
    """Validate one pinned package-identity pair (exact keys, digests)."""
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


def parse_binding(data) -> Binding:
    """Parse and fully validate a frozen PATH-B binding document (fail
    closed; no coercion, no fallback, no repair)."""
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

    _exact_keys(doc["target"], TARGET_KEYS, "TARGET")
    for key in TARGET_KEYS:
        if doc["target"][key] != FROZEN_TARGET[key]:
            raise BindingError(
                f"FROZEN_TARGET_MISMATCH: {key}={doc['target'][key]!r}")

    _sha_field(doc["common_evidence_manifest_digest"],
               "COMMON_EVIDENCE_MANIFEST_DIGEST")
    _sha_field(doc["prompt_contract_digest"], "PROMPT_CONTRACT_DIGEST")
    # Governance-frozen selection: NO fallback/inherit/"auto"/generation
    # substitution/silent downgrade — any substituted provider/client/
    # model/effort or client executable identity is refused at parse.
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
    # A package-time PASS for any DYNAMIC gate is exactly the
    # stale-evidence defect — refused BEFORE any other gate check.
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

    return Binding(
        schema=doc["schema"], policy_id=doc["policy_id"],
        event_id=doc["event_id"], auditor_role=role, attempt_id=attempt,
        target=dict(doc["target"]),
        common_evidence_manifest_digest=doc[
            "common_evidence_manifest_digest"],
        prompt_contract_digest=doc["prompt_contract_digest"],
        auditor_selection=dict(selection),
        boundary_launcher=boundary_launcher,
        sandbox_profile_id=doc["sandbox_profile_id"],
        tool_wrapper=tool_wrapper,
        authority_package=authority_package,
        event_package=dict(doc["event_package"]),
        output_identity=dict(doc["output_identity"]),
        static_gate_evidence={k: dict(v) for k, v in
                              doc["static_gate_evidence"].items()},
        dynamic_gates=descriptors,
        auditor_invocation=invocation,
        output_validator=validator,
        execution_limits=execution_limits,
        digest=hashlib.sha256(canonical_bytes(doc)).hexdigest())


def binding_projection(binding: Binding) -> dict:
    """Canonical transport projection of a parsed binding: the EXACT
    value a frozen event-package manifest's transport_binding must
    equal (compared as canonical JSON bytes, so type confusions such
    as true==1 cannot pass).  Covers every dimension in
    PROJECTION_FIELDS; event_package is EXCLUDED (the package's own
    identity — the non-circular construction).  Internal use only."""
    return {name: getattr(binding, name) for name in PROJECTION_FIELDS}
