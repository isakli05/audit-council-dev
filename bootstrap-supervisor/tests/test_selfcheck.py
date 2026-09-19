"""Runtime EBS self-identity verification tests (CR-EBS-003).

All destructive tests operate on COPIED temporary synthetic package
trees; canonical repository bytes are never mutated.  Every identity is
real (derived from actual bytes) or unmistakably synthetic — no real
event package exists or is constructed here.
"""
import copy
import json
import os
import shutil

import pytest

from ebs.binding import parse_binding
from ebs.launch import (LaunchError, LaunchRefused, Supervisor,
                        verify_live_package_identity,
                        verify_package_identity)
from ebs.accounting import AccountingStore

from conftest import EBS_ROOT, binding_for, live_package_identity

MANIFEST = "MANIFEST.json"


def copy_package(tmp_path, name="pkg"):
    dst = tmp_path / name
    shutil.copytree(EBS_ROOT, dst,
                    ignore=shutil.ignore_patterns("__pycache__"))
    return dst


def pins_of(root):
    return live_package_identity(root)


def write_manifest(root, doc):
    (root / MANIFEST).write_text(json.dumps(doc, indent=2, sort_keys=True)
                                 + "\n")


def read_manifest(root):
    return json.loads((root / MANIFEST).read_text())


def regenerate_manifest_for(root):
    """Rebuild every file row + package identity from the LIVE tree at
    root (the attack a manifest-regenerator would perform)."""
    doc = read_manifest(root)
    doc.pop("package_sha256", None)
    rows = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fname in filenames:
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, root)
            if rel == MANIFEST:
                continue
            with open(full, "rb") as handle:
                data = handle.read()
            import hashlib
            rows.append({"path": rel, "bytes": len(data),
                         "sha256": hashlib.sha256(data).hexdigest()})
    doc["files"] = sorted(rows, key=lambda r: r["path"])
    import hashlib
    doc["package_sha256"] = hashlib.sha256(json.dumps(
        doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    write_manifest(root, doc)


def test_exact_shipped_package_passes():
    manifest_sha, package_sha = pins_of(EBS_ROOT)
    result = verify_package_identity(EBS_ROOT, manifest_sha, package_sha)
    assert result["files"] == len(json.loads(
        (EBS_ROOT / MANIFEST).read_text())["files"])
    assert result["manifest_sha256"] == manifest_sha


def test_non_circular_package_identity_construction():
    """package_sha256 == digest of the manifest document EXCLUDING its own
    field (independently re-derived); no recursive self-hash exists."""
    import hashlib
    raw = (EBS_ROOT / MANIFEST).read_bytes()
    doc = json.loads(raw)
    recorded = doc.pop("package_sha256")
    derived = hashlib.sha256(json.dumps(
        doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert recorded == derived
    assert hashlib.sha256(raw).hexdigest() != recorded  # distinct roles


def test_one_production_source_byte_changed_refused(tmp_path):
    pkg = copy_package(tmp_path)
    target = pkg / "ebs" / "statemachine.py"
    target.write_text(target.read_text() + "\n")     # one trailing byte
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD_MISMATCH"):
        verify_package_identity(pkg, *pins_of(pkg))


def test_changed_source_plus_regenerated_manifest_refused(tmp_path):
    """THE core CR-EBS-003 B negative: attacker modifies live source AND
    regenerates a perfectly self-consistent manifest — but the FROZEN
    binding pins the original identities, so both pins mismatch."""
    pkg = copy_package(tmp_path)
    frozen_pins = pins_of(pkg)
    (pkg / "ebs" / "binding.py").write_text(
        "# attacker modification\n" + (pkg / "ebs" / "binding.py").read_text())
    regenerate_manifest_for(pkg)          # full self-consistent rebuild
    with pytest.raises(LaunchRefused, match="MANIFEST_IDENTITY_MISMATCH"):
        verify_package_identity(pkg, *frozen_pins)


def test_manifest_byte_changed_refused(tmp_path):
    pkg = copy_package(tmp_path)
    frozen_pins = pins_of(pkg)                    # captured BEFORE mutation
    raw = (pkg / MANIFEST).read_bytes()
    (pkg / MANIFEST).write_bytes(raw + b"\n")   # whitespace-only byte change
    with pytest.raises(LaunchRefused, match="MANIFEST_IDENTITY_MISMATCH"):
        verify_package_identity(pkg, *frozen_pins)


def test_missing_manifest_payload_refused(tmp_path):
    pkg = copy_package(tmp_path)
    (pkg / "ebs" / "custody.py").unlink()
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD_MISSING"):
        verify_package_identity(pkg, *pins_of(pkg))


def test_extra_unrecorded_authority_bearing_payload_refused(tmp_path):
    pkg = copy_package(tmp_path)
    (pkg / "ebs" / "attacker_module.py").write_text("import os\n")
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD_UNRECORDED"):
        verify_package_identity(pkg, *pins_of(pkg))


def test_stale_manifest_row_refused(tmp_path):
    pkg = copy_package(tmp_path)
    doc = read_manifest(pkg)
    doc["files"].append({"path": "ebs/never_shipped.py", "bytes": 1,
                         "sha256": "0" * 64})
    doc.pop("package_sha256")
    import hashlib
    doc["package_sha256"] = hashlib.sha256(json.dumps(
        doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    write_manifest(pkg, doc)
    with pytest.raises(LaunchRefused, match="PACKAGE_PAYLOAD_MISSING"):
        verify_package_identity(pkg, *pins_of(pkg))


def test_malformed_manifest_refused(tmp_path):
    pkg = copy_package(tmp_path)
    (pkg / MANIFEST).write_text("this is not json")
    with pytest.raises(LaunchRefused, match="PACKAGE_MANIFEST"):
        verify_package_identity(pkg, "0" * 64, "0" * 64)


def test_inconsistent_declared_package_identity_refused(tmp_path):
    pkg = copy_package(tmp_path)
    frozen_pins = pins_of(pkg)                    # captured BEFORE mutation
    doc = read_manifest(pkg)
    doc["package_sha256"] = "1" * 64     # field no longer covers the doc
    write_manifest(pkg, doc)
    with pytest.raises(LaunchRefused,
                       match="PACKAGE_IDENTITY_NOT_SELF_CONSISTENT"):
        verify_package_identity(pkg, *frozen_pins)


def test_wrong_bound_manifest_identity_refused(tmp_path):
    pkg = copy_package(tmp_path)
    _, package_sha = pins_of(pkg)
    with pytest.raises(LaunchRefused, match="LIVE_MANIFEST_IDENTITY"):
        verify_package_identity(pkg, "2" * 64, package_sha)


def test_wrong_bound_ebs_package_identity_refused(tmp_path):
    pkg = copy_package(tmp_path)
    manifest_sha, _ = pins_of(pkg)
    with pytest.raises(LaunchRefused, match="EBS_PACKAGE_IDENTITY"):
        verify_package_identity(pkg, manifest_sha, "3" * 64)


def test_symlinked_payload_refused(tmp_path):
    pkg = copy_package(tmp_path)
    victim = pkg / "ebs" / "custody.py"
    data = victim.read_bytes()
    victim.unlink()
    victim.symlink_to(tmp_path / "outside.py")
    (tmp_path / "outside.py").write_bytes(data)
    with pytest.raises(LaunchRefused):
        verify_package_identity(pkg, *pins_of(pkg))


def test_self_check_runs_before_gates_can_pass(cust_dir, tmp_path, launcher, stage, cust_out):
    """CR-EBS-003 D: a binding pinning a WRONG package identity cannot
    even construct a supervisor, so gates can never pass; the production
    entry takes no parameters (no bypass surface)."""
    import inspect as pyinspect
    assert list(pyinspect.signature(
        verify_live_package_identity).parameters) == ["binding"]
    doc = copy.deepcopy(binding_for(launcher[1]))
    doc["ebs_package"] = {"manifest_sha256": "4" * 64,
                          "package_sha256": "5" * 64}
    binding = parse_binding(json.dumps(doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    with pytest.raises(LaunchRefused, match="MANIFEST_IDENTITY"):
        Supervisor(binding, store, tmp_path / "never-reached-package")
    # with the correct live pins the same construction path works and
    # gates can pass (positive control; DISTINCT attempt id, live tree
    # untouched):
    from conftest import make_auditor_executable, make_event_package, \
        pipe_source, valid_binding_document
    auditor_exe2 = make_auditor_executable(tmp_path)
    doc2 = valid_binding_document(event_id="evt-0011223344556688",
                                  role="AUDITOR_B",
                                  launcher_sha256=launcher[1],
                                  executable_sha256=auditor_exe2[1])
    pkg2 = make_event_package(doc2, tmp_path, name="pkg-selfcheck-pos")
    binding2 = parse_binding(json.dumps(doc2).encode())
    store2 = AccountingStore.create(cust_dir, binding2.attempt_id,
                                    binding2.digest)
    sup = Supervisor(binding2, store2, pkg2)
    sup.run_attempt(pipe_source(), str(launcher[0]), str(auditor_exe2[0]), stage, cust_out)
    assert sup.state == "TERMINAL"


def test_no_environment_or_flag_bypass_surface():
    """The production verifier reads no environment variable; no CLI flag
    or config knob exists that could disable it (static guarantee: no
    os.environ/getenv call anywhere in production, and the production
    self-verification entry is parameter-free apart from the binding)."""
    import ast
    modules = ["binding.py", "statemachine.py", "accounting.py",
               "custody.py", "launch.py", "reportcustody.py", "cli.py"]
    for name in modules:
        tree = ast.parse((EBS_ROOT / "ebs" / name).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and \
                    node.attr in ("environ", "getenv", "getbabuiltin"):
                raise AssertionError(
                    f"{name}: environment access {node.attr}")
            if isinstance(node, ast.Name) and node.id == "environ":
                raise AssertionError(f"{name}: environment access")


# -------- REM2-001: row byte-count type contract on the live layer --------

def rewrite_row_bytes(root, path, value):
    """Set one manifest row's recorded byte count to value and regenerate
    the self-consistent package identity; pins_of(root) then match the
    mutated manifest exactly, so ONLY the row-type rule can refuse."""
    import hashlib
    doc = read_manifest(root)
    for row in doc["files"]:
        if row["path"] == path:
            row["bytes"] = value
    doc.pop("package_sha256", None)
    doc["package_sha256"] = hashlib.sha256(json.dumps(
        doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    write_manifest(root, doc)


def test_rem2_001_live_layer_row_float_bytes_refused(tmp_path):
    """REM2-001 refresh of the shared verifier's CR-EBS-003 layer: a
    FLOAT row byte count that numerically EQUALS the live file size, in
    a perfectly self-consistent copied package with matching pins, is
    refused (the exact numeric-equality type-confusion defect class)."""
    pkg = copy_package(tmp_path)
    target = "ebs/statemachine.py"
    rewrite_row_bytes(pkg, target, float((pkg / target).stat().st_size))
    with pytest.raises(LaunchRefused,
                       match="PACKAGE_MANIFEST_ROW_BYTES_TYPE_INVALID"):
        verify_package_identity(pkg, *pins_of(pkg))


def test_rem2_001_live_layer_row_bool_bytes_refused(tmp_path):
    """A BOOL row byte count is refused at row validation in the copied
    live-layer package, whatever the true file size (bool is never an
    integer byte-count type for this contract)."""
    pkg = copy_package(tmp_path)
    rewrite_row_bytes(pkg, "ebs/statemachine.py", True)
    with pytest.raises(LaunchRefused,
                       match="PACKAGE_MANIFEST_ROW_BYTES_TYPE_INVALID"):
        verify_package_identity(pkg, *pins_of(pkg))
