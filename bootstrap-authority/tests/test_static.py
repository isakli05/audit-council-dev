"""BA-01..BA-12 + BA-51..BA-59: authority source/provenance, package
self-identity, and held-governance mechanical tests (all zero-provider,
zero-network; tamper scenarios run against temporary package COPIES in
subprocesses so the real executing package is never mutated)."""
from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import (AUTHORITY_ROOT, REPO_ROOT, authority_package_pins,
                      canonical, git_blob_sha1, minimal_binding_doc,
                      sha256_bytes)
from bootstrap_authority import runtime as barmod

PRODUCTION = sorted(
    p.name for p in (AUTHORITY_ROOT / "bootstrap_authority").glob("*.py"))
EXPECTED_PRODUCTION = ["__init__.py", "accounting.py", "binding.py",
                       "custody.py", "reportcustody.py", "runtime.py",
                       "statemachine.py"]
PINNED_REUSE_BLOBS = {
    "statemachine.py": "cf563d2178907e7666ce661b81ab1bf16fb71201",
    "custody.py": "37e6b5bb4365c7b29ba3632fe95362d5a7e16c09",
}
# RB2 bounded derivatives: accounting.py / reportcustody.py derive from
# the EXACT pre-target blobs below with ONLY the narrow held-fd
# object-custody primitives added (BA-PREP-RB2-001 / RB2-002); the
# pinned source_git_blob records the derivation ORIGIN.
DERIVED_REUSE_BLOBS = {
    "accounting.py": "03de6f663db283cf99f6a98e26e752a24457c52a",
    "reportcustody.py": "18f1cc600c684e520b72026e0b4cdf8ba6287cb9",
}
PRETARGET_COMMIT = "068f5e29904f446bf832138fd64c8833b9037cb7"
HISTORICAL_BINDING_BLOB = "47eeb5171e9b50b09668aa672b6458c2ea33dd05"
HISTORICAL_LAUNCH_BLOB = "063b6ce1f4c726bd6ba809f605a115511667fb09"
CANDIDATE_LAUNCH_BLOB = "1d6b8d6d5751dbf9a73a84e6b2f1ee594f6ca49e"
# LOC ceiling: the V1 implementation was bounded at 3000 (< the
# 3057-LOC audit-subject EBS tree); the G2 V2 replacement contract
# grew the protected production source to 3577.  The operator's G2
# remediation authorization EXPLICITLY ACCEPTED the 3577 baseline as a
# CEILING for this V2 lineage (G3 finding G1SCOPE-LOC-001 disposition:
# the 3000 ceiling is retired; 3577 is a ceiling, NOT a required
# equality — the former exact-equality test was removed with that
# governance change rather than kept as filler-forcing).  The G2
# remediation fits inside via narrow docstring/comment consolidation.
LOC_BOUND = 3577
EXPECTED_PACKAGE_PATHS = {
    "MANIFEST.json", "README.md",
    "bootstrap_authority/__init__.py",
    "bootstrap_authority/statemachine.py",
    "bootstrap_authority/accounting.py",
    "bootstrap_authority/custody.py",
    "bootstrap_authority/reportcustody.py",
    "bootstrap_authority/binding.py",
    "bootstrap_authority/runtime.py",
    "tests/conftest.py", "tests/test_binding.py",
    "tests/test_runtime.py", "tests/test_static.py",
}
RECORD_REL = ("docs/chatgpt-project/AUCDEV-023-PCH6-B-CANDIDATE-SPECIFIC"
              "-BOOTSTRAP-AUTHORITY-IMPLEMENTATION.md")


def git(*args, cwd=REPO_ROOT):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          text=True)


# --- BA-01: bootstrap-authority exists in the result, not in the
# frozen audit target (nor at the authorized base) ----------------------


def test_ba01_package_exists_only_in_result():
    assert (AUTHORITY_ROOT / "bootstrap_authority" / "runtime.py").is_file()
    for rev in ("730d2b29f7c0e7d33af3451b6d9205ec27c143ed",
                "63e842e392320b74a7fac923ae140984b28079dd"):
        probe = git("cat-file", "-e", f"{rev}:bootstrap-authority")
        assert probe.returncode != 0, rev


# --- BA-02: no production import/runtime dependency on target code -----


def test_ba02_no_target_imports_in_production():
    forbidden = {"bootstrap_supervisor", "ebs", "qualification_harness",
                 "skill"}
    for name in PRODUCTION:
        tree = ast.parse(
            (AUTHORITY_ROOT / "bootstrap_authority" / name).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods = {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom):
                mods = {node.module.split(".")[0]} if node.module else set()
            else:
                continue
            assert not (mods & forbidden), (name, mods)


# --- BA-03: the four reused modules have the exact Git blob identities -


def test_ba03_reused_blob_identities():
    for name, blob in PINNED_REUSE_BLOBS.items():
        data = (AUTHORITY_ROOT / "bootstrap_authority" / name).read_bytes()
        assert git_blob_sha1(data) == blob, name
    for name, blob in DERIVED_REUSE_BLOBS.items():
        data = (AUTHORITY_ROOT / "bootstrap_authority" / name).read_bytes()
        # RB2 bounded derivatives: the live bytes DIFFER from the
        # pre-target blob (an honest derivation, never a silent reuse
        # claim); the origin blob stays pinned in the manifest
        # provenance (test_ba05)
        assert git_blob_sha1(data) != blob, name


# --- BA-04: binding/runtime are NEW blobs, not historical/candidate ----


def test_ba04_new_authority_blobs():
    known = {HISTORICAL_BINDING_BLOB, HISTORICAL_LAUNCH_BLOB,
             CANDIDATE_LAUNCH_BLOB}
    for name in ("binding.py", "runtime.py"):
        data = (AUTHORITY_ROOT / "bootstrap_authority" / name).read_bytes()
        assert git_blob_sha1(data) not in known, name
        for other in ("bootstrap-supervisor/ebs/binding.py",
                      "bootstrap-supervisor/ebs/launch.py"):
            target_path = REPO_ROOT / other
            if target_path.exists():
                assert sha256_bytes(data) != sha256_bytes(
                    target_path.read_bytes()), (name, other)


# --- BA-05: every production source path has manifest provenance ------


def test_ba05_manifest_provenance():
    doc = json.loads((AUTHORITY_ROOT / "MANIFEST.json").read_text())
    provenance = doc["source_provenance"]
    assert set(provenance) == {"bootstrap_authority/%s" % n
                               for n in EXPECTED_PRODUCTION}
    for name, blob in PINNED_REUSE_BLOBS.items():
        entry = provenance["bootstrap_authority/%s" % name]
        assert entry == {"kind": "EXACT_PRETARGET_BLOB_REUSE",
                         "source_commit": PRETARGET_COMMIT,
                         "source_path": "bootstrap-supervisor/ebs/" + name,
                         "source_git_blob": blob}
    for name, blob in DERIVED_REUSE_BLOBS.items():
        entry = provenance["bootstrap_authority/%s" % name]
        assert entry == {"kind": barmod.DERIVATION_KIND,
                         "source_commit": PRETARGET_COMMIT,
                         "source_path": "bootstrap-supervisor/ebs/" + name,
                         "source_git_blob": blob,
                         "derivation": barmod.DERIVATION_REASON}
    for name in ("__init__.py", "binding.py", "runtime.py"):
        assert provenance["bootstrap_authority/%s" % name] == {
            "kind": "NEW_AUTHORITY_SPECIFIC",
            "origin": "THIS_BOUNDED_IMPLEMENTATION"}


# --- BA-06: production LOC <= 3000 -------------------------------------


def test_ba06_loc_bound():
    total = 0
    per_file = {}
    for name in PRODUCTION:
        count = len((AUTHORITY_ROOT / "bootstrap_authority" / name)
                    .read_text().splitlines())
        per_file[name] = count
        total += count
    assert total <= LOC_BOUND, per_file


# --- BA-07..BA-11: package self-identity of the live manifest ----------


def _live_manifest():
    raw = (AUTHORITY_ROOT / "MANIFEST.json").read_bytes()
    return raw, json.loads(raw.decode("utf-8"))


def test_ba07_manifest_raw_digest_is_the_binding_pin():
    raw, _doc = _live_manifest()
    pins = authority_package_pins()
    assert pins["manifest_sha256"] == sha256_bytes(raw)


def test_ba08_package_sha256_self_consistency():
    _raw, doc = _live_manifest()
    semantics = {k: v for k, v in doc.items() if k != "package_sha256"}
    assert sha256_bytes(canonical(semantics)) == doc["package_sha256"]


def test_ba09_rows_match_live_bytes():
    _raw, doc = _live_manifest()
    for row in doc["files"]:
        full = AUTHORITY_ROOT / row["path"]
        data = full.read_bytes()
        assert len(data) == row["bytes"], row["path"]
        assert sha256_bytes(data) == row["sha256"], row["path"]


def test_ba11_payload_set_equality():
    _raw, doc = _live_manifest()
    recorded = {row["path"] for row in doc["files"]}
    walked = set()
    for dirpath, dirnames, filenames in os.walk(
            AUTHORITY_ROOT, followlinks=False):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name),
                                  AUTHORITY_ROOT)
            if rel != "MANIFEST.json":
                walked.add(rel)
    assert recorded == walked


# --- BA-10/BA-12: tampered package copies fail closed (subprocess) -----


TAMPER_DRIVER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from bootstrap_authority import binding as bab, runtime as bar
doc = json.loads(open(sys.argv[2], "rb").read().decode())
binding = bab.parse_binding(json.dumps(doc).encode())
try:
    bar.BootstrapAuthority(binding, sys.argv[3])
except Exception as exc:
    print("REFUSED", type(exc).__name__, str(exc)[:200])
    sys.exit(0)
print("CONSTRUCTED")
sys.exit(0)
'''


def _run_tamper(tmp_path, mutate_package, doc_mutate=None,
                pins=None):
    """Copy the REAL package to a tmp root, mutate the copy, build a
    binding document pinned to the copy's (or the given) package
    identities, and run the construction in a subprocess so the real
    executing package is never mutated."""
    pkg = tmp_path / "pkg"
    shutil.copytree(AUTHORITY_ROOT, pkg,
                    ignore=shutil.ignore_patterns("__pycache__"))
    mutate_package(pkg)
    raw = (pkg / "MANIFEST.json").read_bytes()
    copy_doc = json.loads(raw.decode("utf-8"))
    if pins is None:
        pins = {"manifest_sha256": sha256_bytes(raw),
                "package_sha256": copy_doc["package_sha256"]}
    doc = minimal_binding_doc("AUDITOR_A", authority_pins=pins)
    if doc_mutate:
        doc_mutate(doc)
    event_root = tmp_path / "event"
    event_root.mkdir()
    (event_root / "MANIFEST.json").write_text("{}")
    script = tmp_path / "driver.py"
    script.write_text(TAMPER_DRIVER)
    binding_doc = tmp_path / "binding.json"
    binding_doc.write_text(json.dumps(doc))
    out = subprocess.run(
        [sys.executable, str(script), str(pkg), str(binding_doc),
         str(event_root)], capture_output=True, text=True, timeout=120,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).parent)})
    return out.stdout


def _regenerate_manifest_for(pkg):
    """Recompute a SELF-CONSISTENT manifest for the (tampered) copy so
    only the operator-supplied binding pins stand between the tampered
    bytes and acceptance (the BA-12 'bless itself' scenarios)."""
    rows = []
    for dirpath, dirnames, filenames in os.walk(pkg, followlinks=False):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, pkg)
            if rel == "MANIFEST.json" or os.path.islink(full):
                continue
            data = open(full, "rb").read()
            rows.append({"path": rel, "bytes": len(data),
                         "sha256": sha256_bytes(data)})
    doc = json.loads((pkg / "MANIFEST.json").read_text())
    doc["files"] = sorted(rows, key=lambda r: r["path"])
    semantics = {k: v for k, v in doc.items() if k != "package_sha256"}
    doc["package_sha256"] = sha256_bytes(canonical(semantics))
    (pkg / "MANIFEST.json").write_text(
        json.dumps(doc, indent=2, sort_keys=True) + "\n")


def test_ba10_unrecorded_file_refused(tmp_path):
    def add_extra(pkg):
        (pkg / "bootstrap_authority" / "smuggled.py").write_text("x = 1\n")
    assert "PACKAGE_PAYLOAD_UNRECORDED" in _run_tamper(tmp_path, add_extra)


def test_ba10_missing_file_refused(tmp_path):
    def remove_readme(pkg):
        (pkg / "README.md").unlink()
    assert "PACKAGE_PAYLOAD_MISSING" in _run_tamper(tmp_path, remove_readme)


def test_ba10_symlink_refused(tmp_path):
    def symlink_source(pkg):
        target = pkg / "bootstrap_authority" / "binding.py"
        original = target.read_bytes()
        (pkg / "original.py").write_bytes(original)
        target.unlink()
        target.symlink_to(pkg / "original.py")
    assert "REFUSED" in _run_tamper(tmp_path, symlink_source)


def test_ba12_tampered_source_cannot_bless_itself(tmp_path):
    # (a) tamper source + REGENERATE the self-consistent manifest, but
    # keep the binding's manifest_sha256 pin at the OLD live value: the
    # raw-manifest identity must refuse.
    live_pins = authority_package_pins()

    def tamper_and_regenerate(pkg):
        target = pkg / "bootstrap_authority" / "binding.py"
        target.write_bytes(target.read_bytes() + b"\n# TAMPERED\n")
        _regenerate_manifest_for(pkg)
    out = _run_tamper(tmp_path, tamper_and_regenerate, pins=live_pins)
    assert "LIVE_MANIFEST_IDENTITY_MISMATCH" in out, out

    # (b) change ONLY the binding's manifest_sha256 pin (single identity
    # field) on an otherwise untampered package: the package_sha256 pin
    # must refuse.
    def only_manifest_pin(doc):
        doc["authority_package"]["manifest_sha256"] = "b" * 64
    # changing ONLY the raw-manifest pin: the raw identity check fires
    assert "LIVE_MANIFEST_IDENTITY_MISMATCH" in _run_tamper(
                  tmp_path / "b", lambda pkg: None,
                  only_manifest_pin)

    # (c) change ONLY the package_sha256 pin: the raw pin still matches
    # (bytes unchanged), so the PACKAGE identity pin refuses.
    def only_package_pin(doc):
        doc["authority_package"]["package_sha256"] = "b" * 64
    assert "PACKAGE_IDENTITY_MISMATCH" in _run_tamper(
        tmp_path / "c", lambda pkg: None, only_package_pin)


# --- BA-51..BA-59: held governance (mechanical) ------------------------


def test_ba51_no_real_event_package_or_credentials_in_repo():
    present = set()
    for dirpath, dirnames, filenames in os.walk(
            AUTHORITY_ROOT, followlinks=False):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in filenames:
            present.add(os.path.relpath(os.path.join(dirpath, name),
                                        AUTHORITY_ROOT))
    assert present == EXPECTED_PACKAGE_PATHS
    for rel in present:
        low = rel.lower()
        assert "event-package" not in low and not low.endswith(".jsonl"), rel
        assert "CAND730D2B29-FRESH-AUDIT" not in rel, rel
    tracked = git("ls-files", "--", "bootstrap-authority")
    tracked_paths = {line[len("bootstrap-authority/"):]
                     for line in tracked.stdout.splitlines()
                     if line.startswith("bootstrap-authority/")}
    assert tracked_paths <= EXPECTED_PACKAGE_PATHS
    assert "bootstrap-authority/event-package" not in tracked.stdout


def test_ba52_no_provider_or_network_surface_in_production():
    banned_imports = {"socket", "urllib", "http", "requests", "ssl",
                      "ftplib", "telnetlib", "smtplib", "asyncio"}
    for name in PRODUCTION:
        text = (AUTHORITY_ROOT / "bootstrap_authority" / name).read_text()
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods = {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom):
                mods = {node.module.split(".")[0]} if node.module else set()
            else:
                continue
            assert not (mods & banned_imports), (name, mods)
        assert "https://" not in text and "api.anthropic.com" not in text, name


def _record_text():
    return (REPO_ROOT / RECORD_REL).read_text()


@pytest.mark.parametrize("token", [
    "AUCDEV_023_PCH6B_BOOTSTRAP_AUTHORITY_IMPLEMENTATION",
    "IMPLEMENTED_AS_CANDIDATE",
    "MODEL_ENGAGEMENTS_USED_0",
    "EVENT_PACKAGE_NOT_PREPARED",
    "EVENT_NOT_INSTANTIATED",
    "ATTEMPT_AUTHORITIES_NOT_GRANTED",
    "PCH6_AUTHORITY_CONSUMED_TERMINAL_CLOSED_NO_RERUN",
    "PCH6_B_SD_002_NOT_CLOSED",
    "PCH6_CR_BSD_001_NOT_CLOSED",
    "PCH6_B_SD_001_RETAINED_OPEN",
    "ROOT_CAUSE_NOT_ESTABLISHED_UNCHANGED",
    "INDEPENDENT_AUDITOR_PROVENANCE_GATE_NOT_SATISFIED",
    "QUALIFICATION_NONE",
    "INSTALLATION_NONE",
    "NO_AUDIT_EXECUTION",
    "NO_AUDIT_PASS",
])
def test_ba53_to_ba59_record_governance_tokens(token):
    assert token in _record_text()


def test_ba53_no_engagement_accounting_anywhere_in_package():
    for dirpath, dirnames, filenames in os.walk(
            AUTHORITY_ROOT, followlinks=False):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in filenames:
            assert not name.endswith(".jsonl"), name


# =====================================================================
# G2 V2 REPLACEMENT contract — structural / held-governance tests
# (ARD-AC-01/02, ARD-AC-14/15, ARD-AC-25..40)
# =====================================================================

from bootstrap_authority import binding as bab                  # noqa: E402

# The exact authorized-base (G2 base c8ffd8b) git blob identities of
# every byte-held production module: NOTHING protected outside the
# authorized binding.py/runtime.py pair may change.
BASE_HELD_BLOBS = {
    "accounting.py": "26368783dd88782dd3c63a76fbf11582ee16caa1",
    "statemachine.py": "cf563d2178907e7666ce661b81ab1bf16fb71201",
    "custody.py": "37e6b5bb4365c7b29ba3632fe95362d5a7e16c09",
    "reportcustody.py": "dd09e1e54c9246aa6de5f38391984c35e8baac87",
}
EXPECTED_RESERVED_ATTEMPT_IDS = {
    "AUDITOR_A":
        "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01",
    "AUDITOR_B":
        "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-B-01",
}
EXPECTED_FROZEN_TARGET = {
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
RESERVED_CANONICAL_PATHS = (
    "docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-AUDITOR-"
    "A-PACKAGE-BINDING-AUTHORITY.md",
    "docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-AUDITOR-"
    "A-GRANT-MINT-PUBLICATION.md",
)
FORBIDDEN_CAPABILITY_NAMES = (
    "grant", "consume", "resume", "retry", "adopt_report", "finish",
    "mint_attempt", "create_event", "mint_grant", "bind_package",
    "create_receipt",
)


def test_ard_01_v1_constants_byte_exact():
    """ARD-AC-01/02/40: every held V1 constant retains its exact
    historical value (historical records keep their original meaning;
    the spent A-01 identity is NOT reinterpreted as a replacement
    registry entry)."""
    assert bab.POLICY_ID == ("AUCDEV-023-PCH6B-CAND730D2B29-TARGET-"
                             "INDEPENDENT-BOOTSTRAP-AUTHORITY-V1")
    assert bab.EVENT_ID == \
        "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01"
    assert bab.RESERVED_ATTEMPT_IDS == EXPECTED_RESERVED_ATTEMPT_IDS
    assert bab.ROLES == ("AUDITOR_A", "AUDITOR_B")
    assert bab.BINDING_SCHEMA == \
        "AUCDEV-023-CAND730D2B29-BOOTSTRAP-AUTHORITY-BINDING-V1"
    assert bab.FROZEN_TARGET == EXPECTED_FROZEN_TARGET           # AC-37
    assert bab.AUTHORITY_MANIFEST_SCHEMA == \
        "AUCDEV-023-BOOTSTRAP-AUTHORITY-PACKAGE-MANIFEST-V1"
    assert bab.AUTHORITY_MANIFEST_KEYS == frozenset(
        ("schema", "package", "policy_id", "target", "design_event_id",
         "design_attempt_ids", "status", "qualification_claim",
         "runtime_dependencies", "source_provenance", "files",
         "package_sha256"))
    assert bab.V2_PERMITTED_AUDITOR_ROLES == ("AUDITOR_A",)


def test_ard_held_production_blobs_exact():
    """ARD-AC-35/36 + the byte-held file requirement: accounting.py,
    statemachine.py, custody.py and reportcustody.py keep their exact
    authorized-base git blob identities."""
    for name, blob in BASE_HELD_BLOBS.items():
        data = (AUTHORITY_ROOT / "bootstrap_authority" / name).read_bytes()
        assert git_blob_sha1(data) == blob, name


def test_ard_replacement_mapping_exactly_one_slot():
    assert list(bab.REPLACEMENT_ATTEMPT_SLOTS) == \
        ["AUDITOR_A_REPLACEMENT_1"]                    # one slot only
    assert bab.REPLACEMENT_ATTEMPT_SLOTS["AUDITOR_A_REPLACEMENT_1"] == \
        bab.EVENT_ID + "-AUDITOR-A-R1"
    assert "AUDITOR_A_REPLACEMENT_1" not in bab.ROLES
    assert "AUDITOR_A_REPLACEMENT_1" not in bab.RESERVED_ATTEMPT_IDS
    assert "AUDITOR_A_REPLACEMENT_1" not in \
        bab.V2_PERMITTED_AUDITOR_ROLES
    for slot in bab.REPLACEMENT_ATTEMPT_SLOTS:         # no Auditor-B slot
        assert "AUDITOR_B" not in slot                  # ARD-AC-34
    assert set(bab.REPLACEMENT_ATTEMPT_SLOTS.values()).isdisjoint(
        set(bab.RESERVED_ATTEMPT_IDS.values()))


def test_ard_14_15_public_surface_and_forbidden_capabilities():
    """ARD-AC-14/15: the public BootstrapAuthority surface remains
    EXACTLY {state, store, run_attempt} and NONE of the forbidden
    capability names (grant mint / package bind / receipt create /
    attempt mint / event create included) exists anywhere on the
    class."""
    public = {name for name, member in
              vars(barmod.BootstrapAuthority).items()
              if not name.startswith("_")
              and not isinstance(member, (classmethod, staticmethod))}
    assert public == {"state", "store", "run_attempt"}
    for name in FORBIDDEN_CAPABILITY_NAMES:
        assert not hasattr(barmod.BootstrapAuthority, name), name
    import inspect
    params = list(inspect.signature(
        barmod.BootstrapAuthority.run_attempt).parameters)
    assert params == ["self", "credential_source_fd", "launcher_path",
                      "auditor_executable_path", "report_staging_path",
                      "output_root"]
    # the runtime never consumes grant bytes
    assert "parse_package_grant" not in \
        (AUTHORITY_ROOT / "bootstrap_authority" / "runtime.py").read_text()


def test_ard_25_32_reserved_canonical_paths_absent():
    """The design-reserved G5/G7 canonical paths remain ABSENT (on disk,
    tracked, and across ALL history) and the repository MANIFEST
    fabricates NO operative grant identity."""
    for rel in RESERVED_CANONICAL_PATHS:
        assert not (REPO_ROOT / rel).exists(), rel
        history = git("log", "--oneline", "--", rel)
        assert history.stdout == "", (rel, history.stdout)
    doc = json.loads((AUTHORITY_ROOT / "MANIFEST.json").read_text())
    assert doc["schema"] == bab.AUTHORITY_MANIFEST_SCHEMA    # stays V1
    assert "package_grant_identity" not in doc
    assert "design_replacement_attempt_slots" not in doc


def test_ard_33_single_governance_event_constant():
    """ARD-AC-33: exactly ONE governance event constant; the V2 route
    admits only that event (no second event is representable)."""
    text = (AUTHORITY_ROOT / "bootstrap_authority" / "binding.py"
            ).read_text()
    assert text.count('EVENT_ID = "') == 1
    assert "FRESH-AUDIT-20261002-01" in text
    assert "FRESH-AUDIT-20261002-02" not in text


def test_ard_no_credential_or_channel_surface_in_production():
    """No real credential literal and no channel/VM surface appears in
    the production source (zero-runtime census, mechanical side)."""
    for name in PRODUCTION:
        text = (AUTHORITY_ROOT / "bootstrap_authority" / name).read_text()
        for banned in ("OPERATOR_SEND_NOW", "send_once_v2", "bridge-v2",
                       "virsh", "QGA", "sk-ant", "BEGIN PRIVATE KEY"):
            assert banned not in text, (name, banned)


def test_ard_06_loc_ceiling():
    """RCTX-29: production LOC stays AT OR UNDER the operator-accepted
    3577 CEILING (the exact-equality form encoded the superseded G1
    wording and was removed per the G2 remediation LOC governance
    reconciliation — no filler code is forced by an equality pin)."""
    total = 0
    for name in PRODUCTION:
        total += len((AUTHORITY_ROOT / "bootstrap_authority" / name)
                     .read_text().splitlines())
    assert total <= LOC_BOUND, total


# =====================================================================
# G2 REMEDIATION structural tests (RCTX-21..RCTX-30; RECEIPTCTX-001 /
# G1CONTRACT-001 / G1SCOPE-LOC-001 reconciliation)
# =====================================================================


def test_rctx_21_bootstrap_authority_never_consumes_grant_bytes():
    """RCTX-21: BootstrapAuthority does not parse, hash or consume
    grant bytes — no grant-parser/grant-canonicalization reference of
    any kind exists in runtime.py (the G1 runtime cross-check wording
    is superseded by the operator's reconciliation: grant-byte
    verification belongs EXCLUSIVELY to NON-RUNTIME binding/package
    tooling and the independent readback)."""
    runtime_text = (AUTHORITY_ROOT / "bootstrap_authority" /
                    "runtime.py").read_text()
    for banned in ("parse_package_grant", "_validated_grant_document",
                   "grant_canonical_bytes", "check_package_grant_reference",
                   "bab.grant_identity", "grant_identity(canonical)"):
        assert banned not in runtime_text, banned
    # the manifest surface checks only the STRUCTURAL 64-hex form
    assert "SHA256_RE.match(grant_reference)" in runtime_text


def test_rctx_22_bootstrap_authority_never_touches_receipts():
    """RCTX-22: BootstrapAuthority neither writes nor verifies receipts
    — no receipt primitive of any kind is reachable from runtime.py."""
    runtime_text = (AUTHORITY_ROOT / "bootstrap_authority" /
                    "runtime.py").read_text()
    for banned in ("write_package_binding_receipt",
                   "verify_package_binding_receipt", "receipt_name",
                   "RECEIPT_SCHEMA", "parse_package_binding_receipt"):
        assert banned not in runtime_text, banned
    for name in ("write_package_binding_receipt",
                 "verify_package_binding_receipt", "create_receipt"):
        assert not hasattr(barmod.BootstrapAuthority, name), name


def test_rctx_23_public_surface_exact():
    """RCTX-23: the public BootstrapAuthority surface remains EXACTLY
    {state, store, run_attempt} (re-asserted for the remediation)."""
    public = {name for name, member in
              vars(barmod.BootstrapAuthority).items()
              if not name.startswith("_")
              and not isinstance(member, (classmethod, staticmethod))}
    assert public == {"state", "store", "run_attempt"}


def test_rctx_24_grant_schema_bytes_unchanged():
    """RCTX-24: the accepted 20-field grant schema and its canonical
    byte semantics are unchanged by the remediation."""
    assert bab.GRANT_FIELDS == (
        "schema", "purpose", "operator_authority_id",
        "authorization_record_path", "authorization_commit_sha",
        "authorization_record_blob_sha1", "authorization_record_sha256",
        "governance_event_id", "auditor_role", "attempt_slot",
        "future_machine_attempt_id", "frozen_target_commit",
        "frozen_target_tree", "accepted_active_v3_procedure_sha256",
        "accepted_active_v3_binding_sha256", "one_package_only",
        "execution_authority", "secret_material", "expiry_policy",
        "issuance_semantics")
    assert len(bab.GRANT_FIELDS) == 20
    assert "lifecycle_state" not in bab.GRANT_FIELDS
    assert bab.GRANT_EXECUTION_AUTHORITY == "NONE"
    assert bab.GRANT_SECRET_MATERIAL == "NONE"


def test_rctx_25_v1_semantics_unchanged():
    """RCTX-25: the V1 parse route and manifest semantics are unchanged
    (spot re-derivation; the full contract lives in the BA-13..25 and
    ARD-AC test batteries above)."""
    assert bab.BINDING_SCHEMA == \
        "AUCDEV-023-CAND730D2B29-BOOTSTRAP-AUTHORITY-BINDING-V1"
    assert bab.AUTHORITY_MANIFEST_KEYS == frozenset(
        ("schema", "package", "policy_id", "target", "design_event_id",
         "design_attempt_ids", "status", "qualification_claim",
         "runtime_dependencies", "source_provenance", "files",
         "package_sha256"))


def test_rctx_26_replacement_semantics_unchanged():
    """RCTX-26: the one-slot replacement role/slot/attempt semantics
    are unchanged (spot re-derivation)."""
    assert bab.REPLACEMENT_ATTEMPT_SLOTS == {
        "AUDITOR_A_REPLACEMENT_1":
            bab.EVENT_ID + "-AUDITOR-A-R1"}
    assert bab.REPLACEMENT_SLOT_ROLES == {
        "AUDITOR_A_REPLACEMENT_1": "AUDITOR_A"}
    assert bab.V2_PERMITTED_AUDITOR_ROLES == ("AUDITOR_A",)


def test_rctx_27_28_held_modules_byte_exact():
    """RCTX-27/28: accounting.py and statemachine.py keep their exact
    authorized-base git blob identities (byte-held through the
    remediation)."""
    held = {"accounting.py": "26368783dd88782dd3c63a76fbf11582ee16caa1",
            "statemachine.py":
                "cf563d2178907e7666ce661b81ab1bf16fb71201"}
    for name, blob in held.items():
        data = (AUTHORITY_ROOT / "bootstrap_authority" / name).read_bytes()
        assert git_blob_sha1(data) == blob, name


def test_rctx_30_reserved_paths_remain_absent():
    """RCTX-30: the design-reserved G7 mint-publication and
    package-binding-authority canonical paths remain ABSENT (on disk
    and across all history) — the remediation may NOT create them."""
    for rel in RESERVED_CANONICAL_PATHS:
        assert not (REPO_ROOT / rel).exists(), rel
        assert git("log", "--oneline", "--", rel).stdout == "", rel
    # the G7 record path constant matches the reserved canonical path
    assert bab.G7_MINT_PUBLICATION_RECORD_PATH == (
        "docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-"
        "AUDITOR-A-GRANT-MINT-PUBLICATION.md")
    assert not (REPO_ROOT / bab.G7_MINT_PUBLICATION_RECORD_PATH).exists()
