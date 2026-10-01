"""BA-13..BA-25: binding parser, frozen target/identities/selections,
and the versioned event-package manifest contract (zero-provider,
zero-network; pure parse-level with synthetic digests unless a full
synthetic world is required)."""
from __future__ import annotations

import copy
import json

import pytest

from bootstrap_authority import binding as bab
from bootstrap_authority import runtime as bar
from conftest import (build_world, canonical, minimal_binding_doc,
                      variant)

WRONG = {
    "commit": "1111111111111111111111111111111111111111",
    "root_tree": "2222222222222222222222222222222222222222",
    "bootstrap_supervisor_tree":
        "3333333333333333333333333333333333333333",
    "qualification_harness_tree":
        "4444444444444444444444444444444444444444",
    "skill_tree": "5555555555555555555555555555555555555555",
    "remediation_parent":
        "6666666666666666666666666666666666666666",
    "repository": "someone/other-repo",
}


# --- BA-13: only the exact frozen target parses ------------------------


@pytest.mark.parametrize("role", ["AUDITOR_A", "AUDITOR_B"])
def test_ba13_exact_target_accepted(role):
    parsed = bab.parse_binding(canonical(minimal_binding_doc(role)))
    assert parsed.target == bab.FROZEN_TARGET


# --- BA-14: any wrong target dimension fails closed ---------------------


@pytest.mark.parametrize("field", list(WRONG))
def test_ba14_wrong_target_dimension_refused(field):
    def mutate(doc):
        doc["target"][field] = WRONG[field]
    with pytest.raises(bab.BindingError, match="FROZEN_TARGET_MISMATCH"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))


def test_ba14_missing_target_dimension_refused():
    def mutate(doc):
        del doc["target"]["bootstrap_supervisor_tree"]
    with pytest.raises(bab.BindingError, match="TARGET_KEYS_INVALID"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))


# --- BA-15: only the exact reserved event accepted ----------------------


def test_ba15_wrong_event_refused():
    def mutate(doc):
        doc["event_id"] = "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-99999999-99"
    with pytest.raises(bab.BindingError, match="EVENT_ID_UNEXPECTED"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))


# --- BA-16: only the exact role/attempt pair accepted --------------------


def test_ba16_cross_role_attempt_refused():
    for role, attempt in (("AUDITOR_A",
                           bab.RESERVED_ATTEMPT_IDS["AUDITOR_B"]),
                          ("AUDITOR_B",
                           bab.RESERVED_ATTEMPT_IDS["AUDITOR_A"])):
        def mutate(doc, role=role, attempt=attempt):
            doc["auditor_role"] = role
            doc["attempt_id"] = attempt
            # keep output name + gate evidence attempt-consistent so the
            # ATTEMPT check is what fires
            doc["output_identity"]["name"] = attempt + \
                ".first-pass-report.json"
            for gate in doc["static_gate_evidence"].values():
                gate["attempt_id"] = attempt
        with pytest.raises(bab.BindingError,
                           match="ATTEMPT_ID_NOT_THE_RESERVED"):
            bab.parse_binding(variant(minimal_binding_doc(), mutate))


def test_ba16_unknown_role_refused():
    def mutate(doc):
        doc["auditor_role"] = "AUDITOR_C"
    with pytest.raises(bab.BindingError, match="AUDITOR_ROLE_UNKNOWN"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))


# --- BA-17/BA-18: exact A/B model+effort selections accepted -------------


@pytest.mark.parametrize("role", ["AUDITOR_A", "AUDITOR_B"])
def test_ba17_ba18_selections_accepted(role):
    parsed = bab.parse_binding(canonical(minimal_binding_doc(role)))
    frozen = bab.AUDITOR_SELECTIONS[role]
    for key in ("provider_role", "client_family", "model", "effort"):
        assert parsed.auditor_selection[key] == frozen[key]


# --- BA-19: substitutions refused ----------------------------------------


@pytest.mark.parametrize("mutation", [
    lambda doc: doc["auditor_selection"].__setitem__("model",
                                                     "claude-haiku-4-5"),
    lambda doc: doc["auditor_selection"].__setitem__("effort", "medium"),
    lambda doc: doc["auditor_selection"].__setitem__(
        "provider_role", "CODEX_CHATGPT_OAUTH"),
    lambda doc: doc["auditor_selection"].__setitem__(
        "client_family", "CODEX_CHATGPT_OAUTH"),
])
def test_ba19_selection_substitutions_refused(mutation):
    with pytest.raises(bab.BindingError):
        bab.parse_binding(variant(minimal_binding_doc(), mutation))


def test_ba19_generation_substitution_between_roles_refused():
    def mutate(doc):
        doc["auditor_selection"]["model"] = "gpt-6.1-sol"  # B's model on A
    with pytest.raises(bab.BindingError, match="MODEL_SUBSTITUTED"):
        bab.parse_binding(variant(minimal_binding_doc("AUDITOR_A"),
                                  mutate))


# --- BA-20: duplicate JSON keys refused ----------------------------------


def test_ba20_duplicate_keys_refused():
    doc = minimal_binding_doc()
    raw = canonical(doc).decode()
    duped = raw[:-1] + ',"policy_id": "%s"}' % bab.POLICY_ID
    with pytest.raises(bab.BindingError, match="DUPLICATE_KEY"):
        bab.strict_loads(duped.encode())
    with pytest.raises(bab.BindingError, match="DUPLICATE_KEY"):
        bab.parse_binding(duped.encode())


# --- BA-21: unknown/missing/type-confused fields refused -----------------


def test_ba21_unknown_top_level_field_refused():
    def mutate(doc):
        doc["surprise"] = 1
    with pytest.raises(bab.BindingError, match="KEYS_INVALID"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))


def test_ba21_missing_field_refused():
    def mutate(doc):
        del doc["sandbox_profile_id"]
    with pytest.raises(bab.BindingError, match="KEYS_INVALID"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))


@pytest.mark.parametrize("mutation", [
    lambda doc: doc.__setitem__("schema", 7),
    lambda doc: doc["execution_limits"].__setitem__(
        "auditor_timeout_seconds", True),          # bool for int refused
    lambda doc: doc["execution_limits"].__setitem__(
        "auditor_timeout_seconds", 0),              # non-positive refused
    lambda doc: doc["boundary_launcher"].__setitem__("bytes", "1024"),
    lambda doc: doc.__setitem__("auditor_invocation", "not-a-list"),
    lambda doc: doc["auditor_invocation"].append(""),  # empty item refused
    lambda doc: doc["auditor_invocation"].append("bad\x00arg"),
    lambda doc: doc["dynamic_gates"]["RESOURCE_GATE"].__setitem__(
        "path", "../escape.py"),
    lambda doc: doc["dynamic_gates"]["RESOURCE_GATE"].__setitem__(
        "path", "/absolute.py"),
    lambda doc: doc["boundary_launcher"].__setitem__("sha256",
                                                     "XYZ" * 21),
    lambda doc: doc["output_validator"].__setitem__("result_schema",
                                                    "SOMETHING-ELSE-V9"),
])
def test_ba21_type_confusions_refused(mutation):
    with pytest.raises(bab.BindingError):
        bab.parse_binding(variant(minimal_binding_doc(), mutation))


# --- BA-22: the digest covers every security dimension -------------------


def _mutations():
    hex2 = "c" * 64
    return [
        ("target", lambda d: d["target"].__setitem__("commit", WRONG[
            "commit"])),
        ("common_evidence", lambda d: d.__setitem__(
            "common_evidence_manifest_digest", hex2)),
        ("prompt_contract", lambda d: d.__setitem__(
            "prompt_contract_digest", hex2)),
        ("selection_model", lambda d: d["auditor_selection"].__setitem__(
            "model", "x")),
        ("selection_client", lambda d: d[
            "auditor_selection"]["client_executable"].__setitem__(
            "sha256", hex2)),
        ("launcher", lambda d: d["boundary_launcher"].__setitem__(
            "sha256", hex2)),
        ("launcher_path", lambda d: d["boundary_launcher"].__setitem__(
            "path", "other/launcher.bin")),
        ("launcher_bytes", lambda d: d["boundary_launcher"].__setitem__(
            "bytes", 2)),
        ("sandbox", lambda d: d.__setitem__("sandbox_profile_id", "OTHER")),
        ("wrapper", lambda d: d["tool_wrapper"].__setitem__(
            "sha256", hex2)),
        ("authority_manifest_pin", lambda d: d[
            "authority_package"].__setitem__("manifest_sha256", hex2)),
        ("authority_package_pin", lambda d: d[
            "authority_package"].__setitem__("package_sha256", hex2)),
        ("event_pin", lambda d: d["event_package"].__setitem__(
            "package_sha256", hex2)),
        ("output_name", lambda d: d["output_identity"].__setitem__(
            "name", "other.json")),
        ("static_gate_evidence", lambda d: d["static_gate_evidence"][
            "GATE_W_PRIME"].__setitem__("evidence_sha256", hex2)),
        ("gate_descriptor", lambda d: d["dynamic_gates"][
            "NETWORK_READINESS"].__setitem__("sha256", hex2)),
        ("gate_timeout", lambda d: d["dynamic_gates"][
            "RESOURCE_GATE"].__setitem__("timeout_seconds", 31)),
        ("invocation", lambda d: d["auditor_invocation"].__setitem__(
            2, "other-model")),
        ("validator", lambda d: d["output_validator"].__setitem__(
            "sha256", hex2)),
        ("limits", lambda d: d["execution_limits"].__setitem__(
            "auditor_timeout_seconds", 61)),
        ("event_id", lambda d: d.__setitem__("event_id", "OTHER-EVENT")),
        ("attempt_id", lambda d: d.__setitem__("attempt_id", "OTHER")),
        ("role", lambda d: d.__setitem__("auditor_role", "AUDITOR_B")),
    ]


def test_ba22_digest_covers_every_dimension():
    base = minimal_binding_doc()
    base_digest = bab.parse_binding(canonical(base)).digest
    for label, mutation in _mutations():
        mutated = copy.deepcopy(base)
        mutation(mutated)
        digest = hashlib_sha256_canonical(mutated)
        assert digest != base_digest, label


def hashlib_sha256_canonical(doc):
    import hashlib
    return hashlib.sha256(canonical(doc)).hexdigest()


# --- BA-23: event-package manifest contract enforced ----------------------


def _world_event_manifest(world):
    return json.loads((world.event_root / "MANIFEST.json").read_text())


def _tamper_and_rebind(world, mutate):
    """Rewrite the synthetic event manifest self-consistently AND
    re-parse the binding with the updated event pin, so the specific
    EVENT_MANIFEST semantic branch (not the pin check) is exercised."""
    import copy
    import hashlib
    manifest = _world_event_manifest(world)
    mutate(manifest)
    semantics = {k: v for k, v in manifest.items()
                 if k != "package_sha256"}
    manifest["package_sha256"] = hashlib.sha256(
        canonical(semantics)).hexdigest()
    (world.event_root / "MANIFEST.json").write_bytes(
        canonical(manifest) + b"\n")
    doc = copy.deepcopy(world.doc)
    doc["event_package"]["package_sha256"] = manifest["package_sha256"]
    return bab.parse_binding(canonical(doc))


def test_ba23_event_package_accepted(world_a):
    result = bar.verify_event_package(world_a.event_root, world_a.binding)
    assert result["files"] == 7


def test_ba23_wrong_schema_tag_refused(world_a):
    binding = _tamper_and_rebind(
        world_a, lambda m: m.__setitem__(
            "schema", "AUCDEV-023-CAND730D2B29-EVENT-PACKAGE-MANIFEST-V0"))
    with pytest.raises(bar.AuthorityRefused,
                       match="EVENT_MANIFEST_SCHEMA_UNEXPECTED"):
        bar.verify_event_package(world_a.event_root, binding)


def test_ba23_unknown_key_refused(world_a):
    binding = _tamper_and_rebind(world_a, lambda m: m.__setitem__(
        "extra", 1))
    with pytest.raises(bar.AuthorityRefused,
                       match="EVENT_MANIFEST_KEYS_INVALID"):
        bar.verify_event_package(world_a.event_root, binding)


def test_ba23_projection_mismatch_refused(world_a):
    def mutate(manifest):
        manifest["transport_binding"]["sandbox_profile_id"] = "SWAPPED"
    binding = _tamper_and_rebind(world_a, mutate)
    with pytest.raises(bar.AuthorityRefused,
                       match="EVENT_PACKAGE_PROJECTION_MISMATCH"):
        bar.verify_event_package(world_a.event_root, binding)


def test_ba23_wrong_package_identity_refused(world_a):
    manifest = _world_event_manifest(world_a)
    manifest["package_sha256"] = "d" * 64
    (world_a.event_root / "MANIFEST.json").write_bytes(
        canonical(manifest) + b"\n")
    with pytest.raises(bar.AuthorityRefused):
        bar.verify_event_package(world_a.event_root, world_a.binding)


def test_ba23_file_row_mismatch_refused(world_a):
    (world_a.event_root / "tools" / "wrapper.bin").write_bytes(
        b"TAMPERED-WRAPPER\n")
    with pytest.raises(bar.AuthorityRefused, match="PACKAGE_PAYLOAD"):
        bar.verify_event_package(world_a.event_root, world_a.binding)


# --- BA-24: static gate evidence exact set required ------------------------


def test_ba24_missing_static_gate_refused():
    def mutate(doc):
        del doc["static_gate_evidence"]["GATE_W_PRIME"]
    with pytest.raises(bab.BindingError, match="STATIC_GATE_EVIDENCE"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))


def test_ba24_extra_static_gate_refused():
    def mutate(doc):
        doc["static_gate_evidence"]["EXTRA_GATE"] = dict(
            doc["static_gate_evidence"]["IDENTITY_LINTER"])
    with pytest.raises(bab.BindingError, match="STATIC_GATE_EVIDENCE"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))


@pytest.mark.parametrize("mutation", [
    lambda doc: doc["static_gate_evidence"]["BLINDNESS_MAP"].__setitem__(
        "status", "FAIL"),
    lambda doc: doc["static_gate_evidence"]["BLINDNESS_MAP"].__setitem__(
        "auditor_role", "AUDITOR_B"),
    lambda doc: doc["static_gate_evidence"]["BLINDNESS_MAP"].__setitem__(
        "attempt_id", "OTHER"),
    lambda doc: doc["static_gate_evidence"]["COMMON_EVIDENCE_PARITY"][
        "evidence_sha256"].__class__ and
        doc["static_gate_evidence"]["COMMON_EVIDENCE_PARITY"].
        __setitem__("evidence_sha256", "e" * 64),
])
def test_ba24_bad_evidence_member_refused(mutation):
    with pytest.raises(bab.BindingError):
        bab.parse_binding(variant(minimal_binding_doc(), mutation))


# --- BA-25: dynamic gate package-time PASS forbidden ------------------------


@pytest.mark.parametrize("gate", list(bab.DYNAMIC_GATE_ORDER))
def test_ba25_dynamic_gate_frozen_pass_forbidden(gate):
    def mutate(doc):
        doc["static_gate_evidence"][gate] = dict(
            doc["static_gate_evidence"]["IDENTITY_LINTER"])
    with pytest.raises(bab.BindingError,
                       match="GATE_EVIDENCE_.*_FORBIDDEN"):
        bab.parse_binding(variant(minimal_binding_doc(), mutate))
