"""Shared deterministic test fixtures for the AUCDEV-023 EBS test battery.

Every credential byte in this battery is SYNTHETIC and INERT.  Every
launched child is a repository test fixture.  No provider client, network
call, or real credential exists anywhere in this battery.

This module also owns the SYNTHETIC BINDING-DOCUMENT BUILDER and the
SYNTHETIC EVENT-PACKAGE BUILDER (both moved/kept out of the production
TCB: no doc/package builder lives in ebs/**).  The binding builder pins
the LIVE shipped EBS package identity by deriving it INDEPENDENTLY from
MANIFEST.json bytes — the same non-circular construction the production
verifier uses (README.md) — so every Supervisor-based test exercises the
true positive runtime self-identity path, and any live-tree tampering
fails the battery.  The event-package builder constructs ONLY
unmistakably synthetic/inert temporary event packages (the REAL
AUCDEV-023 event package is NOT authorized, NOT built, NOT committed).
"""
import copy
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

EBS_ROOT = Path(__file__).resolve().parents[1]
if str(EBS_ROOT) not in sys.path:
    sys.path.insert(0, str(EBS_ROOT))

from ebs.binding import (EVENT_MANIFEST_SCHEMA, FROZEN_TARGET,  # noqa: E402
                         NETWORK_READINESS_RESULT_SCHEMA, OUTPUT_KIND,
                         POLICY_ID, RESOURCE_GATE_RESULT_SCHEMA,
                         REQUIRED_GATES, ROLE_PROVIDER_ROLES,
                         VALIDATOR_RESULT_SCHEMA, attempt_id_for,
                         output_name_for)

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
                           executable_sha256=None,
                           evidence_seed="synthetic-evidence",
                           auditor_timeout_seconds=30,
                           validator_timeout_seconds=10) -> dict:
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
    # S1-001/S1-002: neither dynamic gate is a frozen evidence member —
    # the binding freezes the TWO RUNTIME gate descriptors instead (no
    # result, no PASS); make_event_package pins the sha256 of each
    # materialized artifact (deterministic order NETWORK_READINESS first,
    # RESOURCE_GATE last — the required dynamic execution order).
    runtime_gate = {
        "NETWORK_READINESS": {
            "identity": "SYNTHETIC-INERT-NETWORK-READINESS-GATE-V1",
            "path": "runtime/network-readiness.py",
            "sha256": seed_sha(evidence_seed, "network-readiness"),
            "result_schema": NETWORK_READINESS_RESULT_SCHEMA,
        },
        "RESOURCE_GATE": {
            "identity": "SYNTHETIC-INERT-RESOURCE-GATE-V1",
            "path": "runtime/resource-gate.py",
            "sha256": seed_sha(evidence_seed, "resource-gate"),
            "result_schema": RESOURCE_GATE_RESULT_SCHEMA,
        },
    }
    # S1-007/S1-008 V5: the frozen structural output-validator descriptor
    # and the frozen bounded execution limits (both pinned to real bytes
    # by make_event_package / make_validator below).
    output_validator = {
        "identity": "SYNTHETIC-INERT-OUTPUT-VALIDATOR-V1",
        "path": "runtime/output-validator.py",
        "sha256": seed_sha(evidence_seed, "output-validator"),
        "result_schema": VALIDATOR_RESULT_SCHEMA,
    }
    execution_limits = {
        "auditor_timeout_seconds": auditor_timeout_seconds,
        "validator_timeout_seconds": validator_timeout_seconds,
    }
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
            "executable_version": "SYNTHETIC-INERT-1.0.0",
            "executable_sha256": executable_sha256 or seed_sha(
                evidence_seed, "auditor-executable")},
        # S1-006 V4: the EXACT frozen auditor-client argv (distinct
        # per-event/role content so exact-delivery is observable).
        "auditor_invocation": [
            "synthetic-inert-auditor-client",
            "--event", event_id,
            "--role", role,
            "--mode", "inert-local-no-provider",
        ],
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
        "runtime_gates": runtime_gate,
        "output_validator": output_validator,
        "execution_limits": execution_limits,
    }


EVENT_PKG_NAME = "event-package"
EVENT_PKG_MARKER = (b"EBS-SYNTHETIC-INERT-EVENT-PACKAGE-FIXTURE-"
                    b"NOT-A-REAL-EVENT-PACKAGE-7c31d9f0-0002")


def make_event_package(doc, tmp_path, name=EVENT_PKG_NAME,
                       projection_mutator=None) -> Path:
    """Build ONE unmistakably synthetic/inert event package for a binding
    document and pin its live identity into doc["event_package"].

    Test aid ONLY (no package builder lives in the production TCB): the
    REAL AUCDEV-023 event package is NOT authorized, NOT built here, and
    NOT committed anywhere.  The manifest follows the production versioned
    event-package contract: exact key set (schema, transport_binding,
    files, package_sha256), the transport projection = every binding
    dimension EXCEPT event_package, and the non-circular package identity
    (digest of the manifest document EXCLUDING its own package_sha256
    key).  S1-001/S1-002: the package ALWAYS contains BOTH inert RUNTIME
    gate artifacts at their descriptors' bound paths and the binding's
    runtime_gates.*.sha256 values are pinned to the materialized bytes
    BEFORE the projection is derived.  Optional projection_mutator
    alters ONLY the manifest transport_binding projection
    (PACKAGE->BINDING negatives)."""
    root = tmp_path / name
    nr_path, nr_sha = make_network_readiness_gate(
        root / "runtime" / "network-readiness.py")
    gate_path, gate_sha = make_resource_gate(
        root / "runtime" / "resource-gate.py")
    val_path, val_sha = make_validator(root / "runtime" /
                                       "output-validator.py")
    doc["runtime_gates"]["NETWORK_READINESS"]["sha256"] = nr_sha
    doc["runtime_gates"]["RESOURCE_GATE"]["sha256"] = gate_sha
    doc["output_validator"]["sha256"] = val_sha
    payloads = {
        "SYNTHETIC-INERT-MARKER.txt": EVENT_PKG_MARKER,
        "transport/prompt-contract.json": json.dumps(
            {"synthetic_inert": True,
             "for_digest": doc["prompt_contract_digest"]},
            sort_keys=True).encode(),
        "transport/common-evidence-manifest.json": json.dumps(
            {"synthetic_inert": True,
             "for_digest": doc["common_evidence_manifest_digest"]},
            sort_keys=True).encode(),
        "runtime/network-readiness.py": nr_path.read_bytes(),
        "runtime/resource-gate.py": gate_path.read_bytes(),
        "runtime/output-validator.py": val_path.read_bytes(),
    }
    (root / "transport").mkdir(parents=True)
    for rel, data in payloads.items():
        (root / rel).write_bytes(data)
    projection = {key: copy.deepcopy(value) for key, value in doc.items()
                  if key != "event_package"}
    if projection_mutator is not None:
        projection_mutator(projection)
    manifest = {
        "schema": EVENT_MANIFEST_SCHEMA,
        "transport_binding": projection,
        "files": [{"path": rel, "bytes": len(data),
                   "sha256": sha_hex(data)}
                  for rel, data in sorted(payloads.items())],
    }
    manifest["package_sha256"] = sha_hex(json.dumps(
        manifest, sort_keys=True, separators=(",", ":")).encode())
    raw = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    (root / "MANIFEST.json").write_bytes(raw)
    doc["event_package"] = {"manifest_sha256": sha_hex(raw),
                            "package_sha256": manifest["package_sha256"]}
    return root


def make_auditor_executable(tmp_path: Path) -> "tuple[Path, str]":
    """Materialize the inert SYNTHETIC auditor executable (S1-006) with a
    runnable shebang and the executable bit the verified-open discipline
    requires; returns (path, sha256).  NEVER executed by the battery: it
    stands in for the live provider-client bytes the EBS must hash, hold,
    and hand to the boundary launcher as AUDITOR_EXEC_FD."""
    src = FIXTURES / "inert_auditor_executable.py"
    dst = tmp_path / "auditor_executable.py"
    text = src.read_text()
    text = text.replace("#!/usr/bin/python3\n", f"#!{sys.executable}\n", 1)
    dst.write_text(text)
    os.chmod(dst, 0o755)
    return dst, sha_hex(dst.read_bytes())


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


def make_resource_gate(dst: Path) -> "tuple[Path, str]":
    """Materialize the inert RUNTIME RESOURCE GATE fixture (S1-001) with a
    runnable shebang; returns (path, sha256).  Same shebang-rewrite
    discipline as make_launcher.  The gate's behavior is driven by an
    EXTERNAL /tmp state file keyed by attempt id (absent = honest PASS),
    so the SAME frozen artifact PASSes or FAILs on live state sampled at
    execution time — the freshness property under test."""
    src = FIXTURES / "inert_resource_gate.py"
    text = src.read_text()
    text = text.replace("#!/usr/bin/python3\n", f"#!{sys.executable}\n", 1)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)
    os.chmod(dst, 0o755)
    return dst, sha_hex(dst.read_bytes())


def make_network_readiness_gate(dst: Path) -> "tuple[Path, str]":
    """Materialize the inert LOCAL RUNTIME NETWORK READINESS GATE fixture
    (S1-002) — same shebang-rewrite discipline.  The fixture performs NO
    network access of any kind; its behavior is driven by an EXTERNAL
    /tmp state file keyed by attempt id (absent = honest PASS), and it
    writes its own attempt-keyed sentinel + counter so tests can prove
    execution occurrence, exactly-once, and gate ORDER against the
    resource gate's tracks."""
    src = FIXTURES / "inert_network_readiness_gate.py"
    text = src.read_text()
    text = text.replace("#!/usr/bin/python3\n", f"#!{sys.executable}\n", 1)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)
    os.chmod(dst, 0o755)
    return dst, sha_hex(dst.read_bytes())


def make_validator(dst: Path) -> "tuple[Path, str]":
    """Materialize the inert SYNTHETIC STRUCTURAL OUTPUT VALIDATOR fixture
    (S1-007) — same shebang-rewrite discipline; returns (path, sha256).
    Behavior is driven by an EXTERNAL /tmp state file keyed by attempt id
    (absent = honest PASS).  NOT qualification-harness code, NOT the
    Audit Council, never a provider client."""
    src = FIXTURES / "inert_validator.py"
    text = src.read_text()
    text = text.replace("#!/usr/bin/python3\n", f"#!{sys.executable}\n", 1)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)
    os.chmod(dst, 0o755)
    return dst, sha_hex(dst.read_bytes())


def make_hanging_launcher(tmp_path: Path) -> "tuple[Path, str]":
    """Materialize the inert HANGING BOUNDARY LAUNCHER fixture (S1-008):
    writes honest metadata, records its pids to a /tmp track keyed by
    attempt id, forks a descendant, and never exits — same shebang-rewrite
    discipline."""
    src = FIXTURES / "inert_hanging_boundary_launcher.py"
    dst = tmp_path / "hanging_launcher.py"
    text = src.read_text()
    text = text.replace("#!/usr/bin/python3\n", f"#!{sys.executable}\n", 1)
    dst.write_text(text)
    os.chmod(dst, 0o755)
    return dst, sha_hex(dst.read_bytes())


# Attempt-keyed /tmp "live resource state" tracks read/written by the
# inert gate fixtures (deterministic, host-local, cleaned per test).
RG_BASE = "/tmp/aucdev023-rg-"
NR_BASE = "/tmp/aucdev023-nr-"
VAL_BASE = "/tmp/aucdev023-val-state-"
HANG_BASE = "/tmp/aucdev023-hang-"


def rg_paths(attempt_id: str):
    return (RG_BASE + "state-" + attempt_id + ".json",
            RG_BASE + "sentinel-" + attempt_id,
            RG_BASE + "count-" + attempt_id)


def nr_paths(attempt_id: str):
    return (NR_BASE + "state-" + attempt_id + ".json",
            NR_BASE + "sentinel-" + attempt_id,
            NR_BASE + "count-" + attempt_id)


def write_rg_state(attempt_id: str, mode: str) -> None:
    """Flip the EXTERNAL live resource state the gate samples fresh at
    execution time (absent file = honest PASS)."""
    with open(rg_paths(attempt_id)[0], "w") as handle:
        json.dump({"mode": mode}, handle)


def write_nr_state(attempt_id: str, mode: str) -> None:
    """Flip the EXTERNAL live route/resolver state the network-readiness
    fixture samples fresh at execution time (absent = honest PASS)."""
    with open(nr_paths(attempt_id)[0], "w") as handle:
        json.dump({"mode": mode}, handle)


def write_val_state(attempt_id: str, mode: str) -> None:
    """Flip the EXTERNAL state the inert structural-validator fixture
    reads at execution time (absent = honest PASS)."""
    with open(VAL_BASE + attempt_id + ".json", "w") as handle:
        json.dump({"mode": mode}, handle)


def clear_val_tracks(attempt_id: str) -> None:
    for path in (VAL_BASE + attempt_id + ".json",
                 HANG_BASE + attempt_id):
        if os.path.exists(path):
            os.unlink(path)


def hang_track(attempt_id: str):
    """Read the hanging-launcher pid track (launcher_pid, descendant_pid)
    written by the S1-008 fixture, or None when not yet written."""
    path = HANG_BASE + attempt_id
    if not os.path.exists(path):
        return None
    with open(path) as handle:
        return json.load(handle)


def _clear_tracks(paths) -> None:
    for path in paths:
        if os.path.exists(path):
            os.unlink(path)


def clear_rg_tracks(attempt_id: str) -> None:
    _clear_tracks(rg_paths(attempt_id))


def clear_nr_tracks(attempt_id: str) -> None:
    _clear_tracks(nr_paths(attempt_id))


def binding_for(launcher_sha: str, auditor_sha256=None, **overrides) -> dict:
    doc = valid_binding_document(
        event_id="evt-0011223344556677",
        role="AUDITOR_A",
        launcher_sha256=launcher_sha,
        executable_sha256=auditor_sha256,
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
def stage(tmp_path):
    """Default NON-AUTHORITATIVE report staging FILE path for the single
    run_attempt call (no staging file exists unless a test plants one,
    so the default report outcome is REPORT_MISSING)."""
    root = tmp_path / "staging"
    root.mkdir()
    return root / "stage.json"


@pytest.fixture
def cust_out(tmp_path):
    """Default operator custody output directory for run_attempt."""
    root = tmp_path / "custody-out"
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
def auditor_exe(tmp_path):
    return make_auditor_executable(tmp_path)


@pytest.fixture
def binding_doc(launcher, auditor_exe, tmp_path):
    doc = binding_for(launcher[1], auditor_sha256=auditor_exe[1])
    make_event_package(doc, tmp_path)   # binds + pins a synthetic package
    return doc


@pytest.fixture
def event_package(tmp_path, binding_doc):
    """Root of the synthetic event package bound (and in-place pinned) by
    the binding_doc fixture — same tmp_path instance, so the pins in
    binding_doc match this tree exactly (depends on binding_doc so the
    package always exists when this fixture is requested)."""
    return tmp_path / EVENT_PKG_NAME


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
