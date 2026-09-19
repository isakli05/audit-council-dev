"""Static boundary tests (tasks §4, §22, §23, §31, §32).

These mechanically establish:
  * production EBS imports ONLY the Python 3 standard library;
  * production EBS never imports/reaches qualification-harness, qh, skill,
    or any Audit Council runtime;
  * the EBS contains no audit-substance logic;
  * zero provider surfaces anywhere under bootstrap-supervisor/**;
  * the minimal-TCB source-size bound holds;
  * MANIFEST.json matches the shipped bytes.
"""
import ast
import hashlib
import json
import re
from pathlib import Path

EBS_ROOT = Path(__file__).resolve().parents[1]
EBS_SRC = EBS_ROOT / "ebs"
PKG_FILES = sorted(EBS_SRC.glob("*.py"))

ALLOWED_STDLIB = {
    "__future__", "argparse", "ctypes", "dataclasses", "enum", "errno",
    "fcntl", "hashlib", "json", "os", "pathlib", "platform", "re", "stat",
    "sys", "time", "typing",
}

# The frozen repository identifier string is required policy data and
# legitimately appears in binding.py; what is forbidden is any import or
# reach into the harness/skill source trees.
FORBIDDEN_TOKENS = [
    "qualification-harness", "qualification_harness",
]

AUDIT_LOGIC_TOKENS = [
    "verdict", "severity", "finding_level", "go_no_go", "disposition",
    "recommend",
]


def test_package_exists_with_expected_module_split():
    names = {p.name for p in PKG_FILES}
    expected = {"__init__.py", "binding.py", "statemachine.py",
                "accounting.py", "custody.py", "launch.py",
                "reportcustody.py", "cli.py"}
    assert expected <= names
    assert names == expected  # no file proliferation beyond the design


INTERNAL_MODULES = {"ebs", "binding", "statemachine", "accounting",
                    "custody", "launch", "reportcustody", "cli"}


def _imported_top_modules(path):
    """Top-level module names imported by a source file; relative imports
    are internal package imports."""
    for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative: internal package module
                yield (node.module or "").split(".")[0]
            elif node.module:
                yield node.module.split(".")[0]


def test_production_imports_stdlib_only():
    for path in PKG_FILES:
        for mod in _imported_top_modules(path):
            assert mod in ALLOWED_STDLIB or mod in INTERNAL_MODULES, \
                f"{path.name}: third-party/unknown import {mod!r}"


def test_production_never_imports_or_reaches_forbidden_trees():
    for path in PKG_FILES:
        src = path.read_text()
        for token in FORBIDDEN_TOKENS:
            assert token not in src, f"{path.name}: forbidden token {token}"
        assert re.search(r"\bqh\b", src) is None, f"{path.name}: qh reference"
        assert "skill/" not in src, f"{path.name}: skill tree reference"
        assert "sys.path" not in src, f"{path.name}: path manipulation"
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in {"import_module", "__import__"}


def test_no_audit_substance_logic():
    for path in PKG_FILES:
        src = path.read_text().lower()
        for token in AUDIT_LOGIC_TOKENS:
            assert token not in src, f"{path.name}: audit-substance token {token}"


def test_no_plugin_or_extension_architecture():
    for path in PKG_FILES:
        src = path.read_text()
        for token in ("entry_points", "plugin", "register_adapter",
                      "load_extension", "setuptools"):
            assert token not in src, f"{path.name}: extension surface {token}"


# Adopted design §4.3 bound: <= ~1500 production source lines (baseline
# 1357 at the first implementation candidate; 1571 at the CR-EBS-001/
# -002/-003 remediation, accepted as residual by the Control Room and
# frozen).  The CR-EBS-REM-001 second remediation adds the event-package
# cross-binding boundary and closes at EXACTLY 1664 lines — +93 over the
# 1571 freeze, classified NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE
# with exact function-level attribution in
# AUCDEV-023-EBS-SECOND-REMEDIATION-REPORT.md; the battery now enforces
# an EXACT freeze at 1664: ANY further growth, even one line, fails.
SECOND_REMEDIATION_LOC_BOUND = 1664


def test_production_loc_within_minimal_tcb_bound():
    total = sum(len(p.read_text().splitlines()) for p in PKG_FILES)
    assert total <= SECOND_REMEDIATION_LOC_BOUND, \
        f"production source grew to {total} lines"


def test_zero_provider_surfaces_under_bootstrap_supervisor():
    # patterns assembled from fragments so this test file cannot match itself
    pattern = re.compile(r"\b(cla" + r"ude|cod" + r"ex)\b", re.IGNORECASE)
    # the skill invocation command token, NOT the repository slug
    # (isakli05/…-dev is frozen policy data inside binding.py)
    command = re.compile(r'(?<![\w-])/audit' + r'-council\b')
    net_imports = ("socket", "ssl", "http", "urllib", "requests",
                   "subprocess", "asyncio")
    for path in EBS_ROOT.rglob("*.py"):
        src = path.read_text()
        assert pattern.search(src) is None, \
            f"{path.relative_to(EBS_ROOT)}: provider name present"
        assert command.search(src) is None, \
            f"{path.relative_to(EBS_ROOT)}: skill invocation path present"
        mods = set(_imported_top_modules(path))
        assert not (mods & set(net_imports)), \
            f"{path.relative_to(EBS_ROOT)}: network/subprocess import {mods}"


def test_fixtures_are_unmistakably_synthetic():
    fixtures = sorted((EBS_ROOT / "tests" / "fixtures").glob("*.py"))
    assert fixtures
    for path in fixtures:
        assert "EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER" \
            in path.read_text()
        assert "#!/usr/bin/python3" in path.read_text()


def test_manifest_matches_shipped_bytes():
    manifest = json.loads((EBS_ROOT / "MANIFEST.json").read_text())
    # non-circular package identity: the recorded field equals the digest
    # of the manifest document EXCLUDING its own package_sha256 key
    identity_source = dict(manifest)
    recorded_identity = identity_source.pop("package_sha256")
    assert hashlib.sha256(json.dumps(
        identity_source, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest() == recorded_identity, \
        "package_sha256 is not the non-circular identity of the manifest"
    recorded = {entry["path"]: entry for entry in manifest["files"]}
    shipped = set()
    for path in sorted(EBS_ROOT.rglob("*")):
        if (not path.is_file()) or path.is_symlink():
            continue
        rel = path.relative_to(EBS_ROOT).as_posix()
        if rel == "MANIFEST.json" or "__pycache__" in rel:
            continue
        shipped.add(rel)
        data = path.read_bytes()
        entry = recorded.get(rel)
        assert entry is not None, f"MANIFEST missing {rel}"
        assert entry["sha256"] == hashlib.sha256(data).hexdigest()
        assert entry["bytes"] == len(data)
    assert set(recorded) == shipped  # no stale manifest rows
    assert manifest["policy_id"]
    assert manifest["target"]["commit"] == \
        "d4d584ffa47ad2848268ba947247f81a845b2322"
    assert "standard library only" in manifest["runtime_dependencies"].lower()
    assert manifest.get("qualification_claim", "NONE") == "NONE"


def test_cli_is_inspection_only():
    src = (EBS_SRC / "cli.py").read_text()
    for token in ("consume", "execute", "launch", "ingest"):
        assert token not in src, "CLI must not expose authority operations"


def test_authority_continuation_surface_removed():
    """CR-EBS-002 A: the attach/revival authority path is structurally
    gone from production source (not merely refused at runtime)."""
    for path in PKG_FILES:
        src = path.read_text()
        assert "def attach" not in src, f"{path.name}: attach surface"
        assert ".attach(" not in src, f"{path.name}: attach call surface"
        assert "RESUMABLE" not in src, \
            f"{path.name}: resumable-state surface present"
        assert "def reset" not in src and "def retry" not in src and \
            "def mint" not in src, f"{path.name}: revival API present"


def test_launch_grant_carries_no_authority_state():
    """CR-EBS-002 D: the grant object has no liveness flag, token, or
    issuer reference to copy or mutate; authority is supervisor-side."""
    from ebs.launch import LaunchGrant
    assert LaunchGrant.__slots__ == ()
