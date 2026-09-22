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
# AUCDEV-023-EBS-SECOND-REMEDIATION-REPORT.md; the battery then enforced
# an EXACT freeze at 1664, and the 1664 freeze REMAINS the last
# Control-Room-accepted baseline (reconfirmed at EXACT SHA 4448deea by
# the narrow-manifest-type-remediation readback, LOC 1664 -> 1664).
#
# CR-EBS-S1-001 gate-timing remediation: live runtime-gate execution
# (verified-fd open/hold, bounded fork/exec runner, strict result
# validation, durable fresh-evidence record) becomes part of the EBS
# authority boundary; honest growth beyond the 1664 freeze is disclosed
# as NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE with exact
# per-function attribution in
# AUCDEV-023-EBS-GATE-TIMING-REMEDIATION-REPORT.md, and the Control Room
# ACCEPTED 2035 as residual at implementation-readback strength on
# EXACT SHA 8e952d81 (2035 NOT standing authority for further growth).
#
# CR-EBS-S1-002/-003 preexec-gate remediation: the SECOND mandatory
# dynamic runtime gate (NETWORK_READINESS descriptor + strict result
# contract + transport-context argv) and the structural single
# preexec-consumption operation (launcher verify + both gates + durable
# GATES_PASSED/CONSUMED_PRE_EXEC in one caller-uninterruptible
# operation) grow the authority boundary beyond the accepted 2035;
# disclosed as NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE with
# exact per-module/per-function attribution in
# AUCDEV-023-EBS-PREEXEC-GATE-REMEDIATION-REPORT.md (LOC 2035 -> 2140; machinery REUSED:
# shared verified-fd open/hold, shared bounded runner, shared strict
# envelope core, shared result-evidence builder).  The candidate ceiling
# below is CANDIDATE_ONLY / NOT_CONTROL_ROOM_ACCEPTED; the prior
# accepted baselines above are PRESERVED and NOT rewritten.
# CR-EBS-S1-004/-005/-006 final launch-seam remediation: Supervisor
# custody ownership + live auditor-executable verify/hold/re-hash + the
# sealed exact-invocation transfer + the V4 binding schema grow the
# authority boundary beyond the accepted 2140 while REMOVING the
# LaunchGrant/consume/execute split; the Control Room ACCEPTED 2349 as
# residual at implementation-readback strength on EXACT SHA 4bb9b936
# (2349 NOT standing authority for further growth).
#
# CR-EBS-S1-007/-008 final execution-lifecycle remediation: the
# process-bound report lifecycle (immutable snapshot -> SAME-custody
# screen -> held frozen structural validator with sealed-snapshot
# delivery and its own timeout -> 0444 freeze -> TERMINAL -> custody/fd
# closure), the session-isolated monotonic-deadline bounded auditor
# wait with process-group timeout kill, and the V5 binding dimensions
# (output_validator + execution_limits) grow the authority boundary
# beyond the accepted 2349 while REMOVING the public adopt_report/
# finish split; disclosed as NEW_TCB_GROWTH /
# AWAITING_CONTROL_ROOM_ACCEPTANCE with exact per-module/per-function
# attribution in
# AUCDEV-023-EBS-FINAL-EXECUTION-LIFECYCLE-REMEDIATION-REPORT.md.
# The candidate ceiling below is CANDIDATE_ONLY / NOT_CONTROL_ROOM_
# ACCEPTED; the prior accepted baselines above are PRESERVED and NOT
# rewritten (2349 remains the last Control-Room-accepted residual).
FINAL_EXECUTION_LIFECYCLE_CANDIDATE_LOC_BOUND = 2800

# CR-EBS-S1-009 post-consumption fail-closed terminality remediation:
# the ONE centralized settlement primitive (_settle_post_consumption,
# separating the durable accounting attempt from the guaranteed
# in-process fail-closed death), the narrow StateMachine
# fail_closed_terminal primitive, and the exact
# PostConsumptionTerminalAccountingError incompleteness classification
# consolidate every earlier duplicated terminalization path
# (_settle/_terminalize_after_consumption REMOVED; the shared fd-closer
# and merged authority-hold closure also reused by the pre-exec path)
# while buying genuinely new authority guarantees: honest durable
# accounting-failure semantics, guaranteed in-process TERMINAL +
# custody/held-fd closure on EVERY post-consumption path (incl.
# injected post-EXEC_ATTEMPTED set_blocking/read/waitpid failures and
# timeout/report TERMINAL-append/transition failures), and original +
# settlement double-failure recoverability.  LOC 2800 -> 2904 disclosed
# as NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE with exact
# per-function attribution in
# AUCDEV-023-EBS-S1-009-POSTCONSUMPTION-TERMINALITY-REMEDIATION-REPORT.md.
# The candidate ceiling below is CANDIDATE_ONLY / NOT_CONTROL_ROOM_
# ACCEPTED; the prior accepted baselines above are PRESERVED and NOT
# rewritten (2800 remains the last Control-Room-accepted residual).
S1_009_POSTCONSUMPTION_TERMINALITY_CANDIDATE_LOC_BOUND = 2904

# EXEC-03 structural remediation (AUCDEV023-CR-S1-EXEC03-001/-004): the
# validator-child stderr channel becomes a WRITABLE bounded pipe with a
# STRUCTURAL-ONLY token sanitizer (the frozen validator's sole
# failure-diagnostic channel; every other gate child keeps the exact
# historical read-only /dev/null fd 2) and the REPORT_INVALID
# settlement durably pins the exact invalid snapshot SHA-256/size the
# validator saw (hash/size only — never report bytes).  LOC 2904 ->
# 3016 disclosed as NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE
# with exact per-function attribution in
# AUCDEV-023-S1-EXEC03-STRUCTURAL-REMEDIATION-REPORT.md.
# The candidate ceiling below is CANDIDATE_ONLY / NOT_CONTROL_ROOM_
# ACCEPTED; the prior baselines above are PRESERVED and NOT rewritten.
EXEC03_STRUCTURAL_REMEDIATION_CANDIDATE_LOC_BOUND = 3016


def test_production_loc_within_minimal_tcb_bound():
    total = sum(len(p.read_text().splitlines()) for p in PKG_FILES)
    assert total <= EXEC03_STRUCTURAL_REMEDIATION_CANDIDATE_LOC_BOUND, \
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


def test_launch_grant_entirely_removed():
    """CR-EBS-002 D + CR-EBS-S1-005 + CR-EBS-S1-007: the portable grant
    is not merely stateless — it is GONE, together with the
    consume()/execute() split AND the separate public report-custody/
    finish-later surface (adopt_report/finish); authority exists only as
    Supervisor process state inside the ONE public run_attempt call."""
    import ebs.launch as launch_mod
    assert not hasattr(launch_mod, "LaunchGrant")
    assert not hasattr(launch_mod.Supervisor, "consume")
    assert not hasattr(launch_mod.Supervisor, "execute")
    assert not hasattr(launch_mod.Supervisor, "adopt_report")
    assert not hasattr(launch_mod.Supervisor, "finish")
    src = (EBS_SRC / "launch.py").read_text()
    assert "def adopt_report" not in src
    assert "def finish(" not in src


def test_public_authority_api_has_no_caller_invocation_surface():
    """CR-EBS-S1-004/-006 source shape: no Supervisor method exposes a
    custody, grant, role, argv-tail, or environment parameter, and the
    single public authority operation accepts exactly the credential
    source fd plus the two byte-identity locator paths."""
    import ast as ast_mod
    import inspect as pyinspect
    from ebs.launch import Supervisor
    params = [name for name, param in
              pyinspect.signature(Supervisor.run_attempt).parameters.items()
              if param.kind != pyinspect.Parameter.POSITIONAL_OR_KEYWORD
              or name != "self"]
    assert params == ["credential_source_fd", "launcher_path",
                      "auditor_executable_path", "report_staging_path",
                      "output_root"]
    tree = ast_mod.parse((EBS_SRC / "launch.py").read_text())
    supervisor = next(node for node in tree.body
                      if isinstance(node, ast_mod.ClassDef)
                      and node.name == "Supervisor")
    for fn in [n for n in supervisor.body
               if isinstance(n, ast_mod.FunctionDef)]:
        for arg in fn.args.args + fn.args.kwonlyargs:
            assert arg.arg not in ("custody", "grant", "argv_tail", "env",
                                   "role", "auditor_role"), \
                f"run-authority caller surface: Supervisor.{fn.name}" \
                f"({arg.arg})"
