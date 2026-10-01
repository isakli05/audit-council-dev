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

PRODUCTION = sorted(
    p.name for p in (AUTHORITY_ROOT / "bootstrap_authority").glob("*.py"))
EXPECTED_PRODUCTION = ["__init__.py", "accounting.py", "binding.py",
                       "custody.py", "reportcustody.py", "runtime.py",
                       "statemachine.py"]
PINNED_REUSE_BLOBS = {
    "statemachine.py": "cf563d2178907e7666ce661b81ab1bf16fb71201",
    "accounting.py": "03de6f663db283cf99f6a98e26e752a24457c52a",
    "custody.py": "37e6b5bb4365c7b29ba3632fe95362d5a7e16c09",
    "reportcustody.py": "18f1cc600c684e520b72026e0b4cdf8ba6287cb9",
}
PRETARGET_COMMIT = "068f5e29904f446bf832138fd64c8833b9037cb7"
HISTORICAL_BINDING_BLOB = "47eeb5171e9b50b09668aa672b6458c2ea33dd05"
HISTORICAL_LAUNCH_BLOB = "063b6ce1f4c726bd6ba809f605a115511667fb09"
CANDIDATE_LAUNCH_BLOB = "1d6b8d6d5751dbf9a73a84e6b2f1ee594f6ca49e"
LOC_BOUND = 3000
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
