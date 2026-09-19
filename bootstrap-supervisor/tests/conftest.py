"""Shared deterministic test fixtures for the AUCDEV-023 EBS test battery.

Every credential byte in this battery is SYNTHETIC and INERT.  Every
launched child is a repository test fixture.  No provider client, network
call, or real credential exists anywhere in this battery.

This module also owns the SYNTHETIC BINDING-DOCUMENT BUILDER (moved out
of the production TCB at remediation time: no doc-builder lives in
ebs/**).  The builder pins the LIVE shipped EBS package identity by
deriving it INDEPENDENTLY from MANIFEST.json bytes — the same
non-circular construction the production verifier uses (README.md) —
so every Supervisor-based test exercises the true positive runtime
self-identity path, and any live-tree tampering fails the battery.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

EBS_ROOT = Path(__file__).resolve().parents[1]
if str(EBS_ROOT) not in sys.path:
    sys.path.insert(0, str(EBS_ROOT))

from ebs.binding import (FROZEN_TARGET, OUTPUT_KIND, POLICY_ID,  # noqa: E402
                         REQUIRED_GATES, ROLE_PROVIDER_ROLES,
                         attempt_id_for, output_name_for)

# The one synthetic inert credential literal used by the whole battery.
SYNTH_CRED = b"EBS-SYNTHETIC-INERT-CREDENTIAL-7c31d9f0-NOT-REAL-0001"

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def sha_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def live_package_identity(root: Path = EBS_ROOT) -> "tuple[str, str]":
    """INDEPENDENTLY derive (manifest_sha256, package_sha256) of the
    shipped package: sha256 of the raw MANIFEST.json bytes, and sha256 of
    the canonical JSON of the manifest document with its own
    package_sha256 key removed (which must equal the recorded field)."""
    raw = (root / "MANIFEST.json").read_bytes()
    doc = json.loads(raw)
    recorded = doc["package_sha256"]
    doc.pop("package_sha256")
    derived = hashlib.sha256(json.dumps(
        doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert derived == recorded, \
        "shipped MANIFEST.json package identity is not self-consistent"
    return sha_hex(raw), derived


EBS_MANIFEST_SHA, EBS_PACKAGE_SHA = live_package_identity()


def seed_sha(seed: str, tag: str) -> str:
    return hashlib.sha256(f"{seed}:{tag}".encode()).hexdigest()


def valid_binding_document(event_id, role, launcher_sha256,
                           launcher_identity="INERT-LOCAL-FIXTURE-LAUNCHER-V1",
                           adapter_id="synthetic_inert_local_v1",
                           provider_role=None, ebs_manifest_sha256=None,
                           ebs_package_sha256=None,
                           evidence_seed="synthetic-evidence") -> dict:
    """Build one well-formed SYNTHETIC binding document (test aid only).

    The EBS package identity pair defaults to the LIVE shipped package so
    ordinary tests exercise the true runtime self-verification positive
    path; destructive tests override it with copied-tree identities."""
    if ebs_manifest_sha256 is None:
        ebs_manifest_sha256 = EBS_MANIFEST_SHA
    if ebs_package_sha256 is None:
        ebs_package_sha256 = EBS_PACKAGE_SHA
    attempt = attempt_id_for(event_id, role)
    prov = provider_role or next(iter(ROLE_PROVIDER_ROLES[role]))
    gates = {gate: {
        "status": "PASS",
        "evidence_sha256": seed_sha(evidence_seed, "common") if gate ==
        "COMMON_EVIDENCE_PARITY" else seed_sha(evidence_seed, gate),
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
        "common_evidence_manifest_digest": seed_sha(evidence_seed, "common"),
        "prompt_contract_digest": seed_sha(evidence_seed, "contract"),
        "boundary_launcher": {"identity": launcher_identity,
                              "sha256": launcher_sha256},
        "auditor_identity": {
            "provider_role": prov,
            "adapter_id": adapter_id,
            "executable_identity": f"SYNTHETIC-INERT-{role}-EXECUTABLE-V1",
            "executable_sha256": seed_sha(evidence_seed,
                                          "auditor-executable")},
        "sandbox_profile_id": "SYNTHETIC-INERT-LOCAL-SANDBOX-V1",
        "tool_wrapper": {"identity": "SYNTHETIC-INERT-TOOL-WRAPPER-V1",
                         "sha256": seed_sha(evidence_seed, "tool-wrapper")},
        "ebs_package": {"manifest_sha256": ebs_manifest_sha256,
                        "package_sha256": ebs_package_sha256},
        "event_package": {"manifest_sha256":
                          seed_sha(evidence_seed, "event-package-manifest"),
                          "package_sha256": seed_sha(evidence_seed,
                                                     "event-package")},
        "output_identity": {"kind": OUTPUT_KIND,
                            "name": output_name_for(attempt)},
        "gate_evidence": gates,
    }


def pipe_source(data: bytes = SYNTH_CRED) -> int:
    """Operator-style pipe credential source (writer closes after write)."""
    r, w = os.pipe()
    os.write(w, data)
    os.close(w)
    return r


def sealed_memfd_source(data: bytes = SYNTH_CRED, seals: int = 0x0F) -> int:
    """Fully (or partially) sealed memfd credential source."""
    from ebs.custody import (MFD_ALLOW_SEALING, MFD_CLOEXEC, F_ADD_SEALS,
                             memfd_create)
    fd = memfd_create("ebs-test-source", MFD_CLOEXEC | MFD_ALLOW_SEALING)
    os.write(fd, data)
    if seals:
        import fcntl
        fcntl.fcntl(fd, F_ADD_SEALS, seals)
    return fd


def make_launcher(tmp_path: Path, variant: str = "a") -> "tuple[Path, str]":
    """Materialize an inert fixture launcher with a runnable shebang.

    Returns (path, sha256).  The shebang is rewritten to the current
    interpreter so the fixture is executable on this host deterministically.
    """
    src = FIXTURES / f"inert_boundary_launcher_{variant}.py"
    dst = tmp_path / f"launcher_{variant}.py"
    text = src.read_text()
    text = text.replace("#!/usr/bin/python3\n", f"#!{sys.executable}\n", 1)
    dst.write_text(text)
    os.chmod(dst, 0o755)
    return dst, sha_hex(dst.read_bytes())


def binding_for(launcher_sha: str, **overrides) -> dict:
    doc = valid_binding_document(
        event_id="evt-0011223344556677",
        role="AUDITOR_A",
        launcher_sha256=launcher_sha,
    )
    for key, value in overrides.items():
        doc[key] = value
    return doc


def write_binding(tmp_path: Path, doc: dict) -> Path:
    path = tmp_path / "binding.json"
    path.write_text(json.dumps(doc, indent=2, sort_keys=True))
    return path


@pytest.fixture
def cust_dir(tmp_path):
    root = tmp_path / "accounting"
    root.mkdir(mode=0o700)
    os.chmod(root, 0o700)
    return root


@pytest.fixture
def out_dir(tmp_path):
    root = tmp_path / "custody-out"
    root.mkdir(mode=0o700)
    os.chmod(root, 0o700)
    return root


@pytest.fixture
def launcher(tmp_path):
    return make_launcher(tmp_path, "a")


@pytest.fixture
def launcher_b(tmp_path):
    return make_launcher(tmp_path, "b")


@pytest.fixture
def binding_doc(launcher):
    return binding_for(launcher[1])


@pytest.fixture
def parsed_binding(binding_doc):
    from ebs.binding import parse_binding
    return parse_binding(json.dumps(binding_doc).encode())


def scan_tree_for(root: Path, needle: bytes) -> "list[Path]":
    """Return files under root whose content contains needle."""
    hits = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            if needle in path.read_bytes():
                hits.append(path)
    return hits
