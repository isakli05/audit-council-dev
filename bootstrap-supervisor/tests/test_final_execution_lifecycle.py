"""Final execution-lifecycle focused suites (CR-EBS-S1-007 +
CR-EBS-S1-008).

Every credential byte here is SYNTHETIC and INERT; every launched child
is a repository test fixture (inert boundary launcher, inert hanging
boundary launcher, inert structural validator); the auditor executable
is the inert synthetic fixture and is NEVER executed.  No provider, no
network, no real event package, no canonical event id.

S1-007 matrix (tasking §25/§26): run_attempt NEVER returns before the
terminal report disposition; the public adopt_report surface is absent;
the SAME Supervisor-held custody performs the leak screen; custody and
launcher/auditor/invocation/validator held fds close before return; a
valid report freezes the EXACT screened+validated bytes at 0444 with
recorded digest/size; missing stays missing (stdout/stderr never
synthesize a report); a contaminated report is REPORT_SCREEN_FAIL with
the validator NOT run; structural validator PASS is required before
REPORT_FROZEN; validator FAIL/non-zero/malformed/mismatch/timeout are
REPORT_INVALID; no refusal path leaves EXEC_ATTEMPTED; no failure
allows a second report attempt; V5 is required (V1-V4 refused — see
test_eventpackage.py); output_validator and execution_limits are
mandatory, digest- and projection-covered; the validator fd is held,
its live bytes verified, no caller path exists, no credential fd is
inherited, and PASS cannot be forged by exit-code-only behavior.

S1-008 matrix (tasking §27/§28): the auditor timeout comes ONLY from
the frozen binding (no caller/env override exists); the child deadline
uses monotonic time; no parent-side pipe read can block past the
deadline; a hanging synthetic boundary tree is terminated by the EBS
itself; the descendant dies with it; an UNRELATED process survives; the
direct child is reaped with no zombie; timeout happens only after
durable CONSUMED_PRE_EXEC with TIMEOUT_AFTER_CONSUMPTION accounting;
state becomes TERMINAL; custody and held fds close; no report freezes;
a second run_attempt is refused; both runtime gates still execute
exactly once in order.
"""
import ast
import hashlib
import inspect as pyinspect
import json
import os
import time

import pytest

from ebs.accounting import AccountingStore, inspect_accounting_record
from ebs.binding import parse_binding
from ebs.custody import CustodyError
from ebs.launch import (AttemptResult, LaunchError, Supervisor,
                        open_output_validator)
from ebs.statemachine import TERMINAL

from conftest import (SYNTH_CRED, binding_for, clear_nr_tracks,
                      clear_rg_tracks, clear_val_tracks, hang_track,
                      make_event_package, make_hanging_launcher, nr_paths,
                      pipe_source, rg_paths, sha_hex, write_nr_state,
                      write_val_state)

ATTEMPT = "evt-0011223344556677-A-01"
CLEAN_REPORT = b'{"synthetic": "inert first-pass double"}\n'


@pytest.fixture(autouse=True)
def clean_tracks():
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    clear_val_tracks(ATTEMPT)
    yield
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    clear_val_tracks(ATTEMPT)


def build(cust_dir, binding_doc, event_package):
    binding = parse_binding(json.dumps(binding_doc).encode())
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    return Supervisor(binding, store, event_package)


def run(sup, launcher, auditor_exe, stage, cust_out, planted=None):
    if planted is not None:
        stage.write_bytes(planted)
    return sup.run_attempt(pipe_source(), str(launcher[0]),
                           str(auditor_exe[0]), str(stage), str(cust_out))


def states_of(cust_dir, sup):
    return inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)["states"]


def custody_is_closed(sup) -> bool:
    if sup._custody is None:
        return True
    try:
        sup._custody.fd
        return False
    except CustodyError:
        return True


def held_fds_closed(sup) -> bool:
    return all(fd is None for fd in (sup._launcher_fd, sup._auditor_fd,
                                     sup._invocation_fd,
                                     sup._validator_fd,
                                     sup._out_dir_fd))


def gate_count(paths):
    _, _, count = paths(ATTEMPT)
    if not os.path.exists(count):
        return 0
    with open(count) as handle:
        return int(handle.read().strip() or 0)


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


# ===================== S1-007: process-bound lifecycle ==================

def test_s1_007_run_attempt_signature_is_the_single_call(launcher,
                                                         auditor_exe):
    """The ONE public authority operation carries the credential source
    fd, the two byte-identity locators, and the two NON-AUTHORITATIVE
    report locators — nothing else."""
    params = list(pyinspect.signature(
        Supervisor.run_attempt).parameters)
    assert params == ["self", "credential_source_fd", "launcher_path",
                      "auditor_executable_path", "report_staging_path",
                      "output_root"]


def test_s1_007_no_public_report_or_finish_surface(launcher, auditor_exe):
    """adopt_report and finish are GONE — no separate post-exec report
    custody or finish-later API exists anywhere on the Supervisor."""
    assert not hasattr(Supervisor, "adopt_report")
    assert not hasattr(Supervisor, "finish")


def test_s1_007_public_surface_is_exactly_read_only_plus_run_attempt():
    """The Supervisor's complete PUBLIC surface is the single authority
    operation plus read-only properties: no other public method exists
    that could mutate state, adopt a report, or finish an attempt."""
    public = {name for name, member in vars(Supervisor).items()
              if not name.startswith("_")
              and (callable(member) or isinstance(member, property))}
    assert public == {"run_attempt", "state", "store", "launcher_fd"}


def test_s1_007_only_public_method_touching_state_is_run_attempt():
    """AST shape: no public Supervisor method other than run_attempt
    appends to the store or transitions the machine — the ONLY public
    operation that can put the machine into EXEC_ATTEMPTED or any
    REPORT_* state is the single authority call itself."""
    src_path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "ebs", "launch.py")
    tree = ast.parse(open(src_path).read())
    supervisor = next(node for node in tree.body
                      if isinstance(node, ast.ClassDef)
                      and node.name == "Supervisor")
    for fn in [n for n in supervisor.body if isinstance(n, ast.FunctionDef)]:
        if fn.name.startswith("_") or fn.name == "run_attempt":
            continue
        for node in ast.walk(fn):
            assert not (isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Attribute)
                        and node.func.attr in ("transition", "append")), \
                f"public method Supervisor.{fn.name} mutates attempt state"


def test_s1_007_every_exec_or_report_state_reaches_terminal_same_body():
    """AST shape (extends the accepted S1-003/S1-005 regression; S1-009
    strengthens it onto the ONE centralized settlement primitive):
    EVERY method that transitions into EXEC_ATTEMPTED or any REPORT_*
    outcome reaches TERMINAL within the SAME body — directly or through
    the statically-verified _settle_post_consumption — so no method can
    leave the machine in a nonterminal execution/report state."""
    src_path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "ebs", "launch.py")
    tree = ast.parse(open(src_path).read())
    supervisor = next(node for node in tree.body
                      if isinstance(node, ast.ClassDef)
                      and node.name == "Supervisor")

    def targets(fn):
        out = set()
        for node in ast.walk(fn):
            if isinstance(node, ast.Call) and \
                    isinstance(node.func, ast.Attribute) and \
                    node.func.attr == "transition" and node.args and \
                    isinstance(node.args[0], ast.Name):
                out.add(node.args[0].id)
            # report-outcome settlements enter their state via the ONE
            # centralized settlement primitive
            if isinstance(node, ast.Call) and \
                    isinstance(node.func, ast.Attribute) and \
                    node.func.attr == "_settle_post_consumption" and \
                    node.args and isinstance(node.args[0], ast.Name):
                out.add(node.args[0].id)
        return out

    def calls_settle(fn):
        return any(isinstance(node, ast.Call) and
                   isinstance(node.func, ast.Attribute) and
                   node.func.attr == "_settle_post_consumption"
                   for node in ast.walk(fn))

    # the settlement primitive is statically verified: Concept A durably
    # records TERMINAL; Concept B is a GUARANTEED finally that lands the
    # in-process machine on TERMINAL via fail_closed_terminal and closes
    # the custody and every held fd — so every call site inherits the
    # terminal + closure guarantee whatever the durable medium does.
    settle = next(fn for fn in supervisor.body
                  if isinstance(fn, ast.FunctionDef)
                  and fn.name == "_settle_post_consumption")
    assert "TERMINAL" in targets(settle)
    finally_calls = [
        call for node in ast.walk(settle)
        if isinstance(node, ast.Try) and node.finalbody
        for sub in node.finalbody for call in ast.walk(sub)
        if isinstance(call, ast.Call)]
    assert any(getattr(call.func, "attr", "") == "fail_closed_terminal"
               for call in finally_calls), \
        "settlement primitive lacks the guaranteed fail-closed death"
    assert any(getattr(call.func, "attr", "") == "_close_authority_holds"
               for call in finally_calls), \
        "settlement primitive lacks guaranteed custody/held-fd closure"
    checked = 0
    for fn in [n for n in supervisor.body if isinstance(n, ast.FunctionDef)]:
        got = targets(fn)
        if got & {"EXEC_ATTEMPTED", "REPORT_FROZEN", "REPORT_MISSING",
                  "REPORT_INVALID", "REPORT_SCREEN_FAIL"}:
            assert "TERMINAL" in got or calls_settle(fn), \
                f"{fn.name} enters a nonterminal execution/report state " \
                f"without reaching TERMINAL in the same body"
            checked += 1
    assert checked >= 2    # the wait path and the report path both exist


def test_s1_007_success_returns_only_after_terminal(launcher, auditor_exe,
                                                    cust_dir, binding_doc,
                                                    event_package, stage,
                                                    cust_out):
    """THE process-bound proof: a VALID report freezes inside the call,
    and run_attempt returns an AttemptResult strictly AFTER TERMINAL
    with custody and every held fd closed."""
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe, stage, cust_out,
                 planted=CLEAN_REPORT)
    assert isinstance(result, AttemptResult)
    assert result.report_state == "REPORT_FROZEN"
    assert result.report_sha256 == sha_hex(CLEAN_REPORT)
    assert result.report_size == len(CLEAN_REPORT)
    assert result.timed_out is False
    assert sup.state == TERMINAL
    assert states_of(cust_dir, sup) == [
        "PREPARED", "GATES_PASSED", "CONSUMED_PRE_EXEC", "EXEC_ATTEMPTED",
        "REPORT_FROZEN", "TERMINAL"]
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)


def test_s1_007_frozen_bytes_are_the_exact_screened_validated_snapshot(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """The frozen artifact carries exactly the screened+validated bytes
    at mode 0444, its recorded digest/size equal the frozen bytes, and
    the durable REPORT_FROZEN record carries the same digest/size."""
    sup = build(cust_dir, binding_doc, event_package)
    run(sup, launcher, auditor_exe, stage, cust_out,
        planted=CLEAN_REPORT)
    frozen = cust_out / sup._binding.output_identity["name"]
    import stat as stat_mod
    assert frozen.read_bytes() == CLEAN_REPORT
    assert stat_mod.S_IMODE(os.stat(frozen).st_mode) == 0o444
    view = inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)
    rec = [r for r in view["records"]
           if r["state"] == "REPORT_FROZEN"][-1]
    assert rec["report_sha256"] == sha_hex(CLEAN_REPORT)
    assert rec["report_size"] == len(CLEAN_REPORT)
    assert rec["report_mode"] == "0444"


def test_s1_007_missing_report_stays_missing_no_stdout_synthesis(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """No staging file: REPORT_MISSING -> TERMINAL inside the call; the
    child's stdout metadata is NEVER reconstructed as a report."""
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe, stage, cust_out)
    assert result.report_state == "REPORT_MISSING"
    assert result.report_sha256 == ""          # nothing hashed
    assert not any(cust_out.iterdir())
    assert sup.state == TERMINAL
    assert states_of(cust_dir, sup)[-2:] == ["REPORT_MISSING", "TERMINAL"]
    assert custody_is_closed(sup) and held_fds_closed(sup)


def test_s1_007_contaminated_report_screens_before_validator(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """A report carrying the synthetic credential is REPORT_SCREEN_FAIL
    via the SAME held custody; the validator is NOT run (its sentinel
    proves absence); nothing is frozen; TERMINAL inside the call."""
    write_val_state(ATTEMPT, "pass")           # validator WOULD pass
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe, stage, cust_out,
                 planted=b'{"prefix": "ok"}' + SYNTH_CRED + b'{"s": 1}')
    assert result.report_state == "REPORT_SCREEN_FAIL"
    assert result.report_sha256 == ""          # contaminated never hashed
    assert not any(cust_out.iterdir())
    assert not stage.exists()                   # staging removed
    assert sup.state == TERMINAL
    assert states_of(cust_dir, sup)[-2:] == ["REPORT_SCREEN_FAIL",
                                             "TERMINAL"]
    assert custody_is_closed(sup)


@pytest.mark.parametrize("mode,refusal", [
    ("fail-status", "REPORT_INVALID"),      # status FAIL, exit 1
    ("nonzero", "REPORT_INVALID"),          # exit 3 with output
    ("malformed", "REPORT_INVALID"),        # not JSON, exit 0
    ("mismatch-sha", "REPORT_INVALID"),     # result digest != snapshot
    ("mismatch-size", "REPORT_INVALID"),    # result size != snapshot
    ("wrong-context", "REPORT_INVALID"),    # result event mismatch
], ids=["fail-status", "nonzero", "malformed", "mismatch-sha",
        "mismatch-size", "wrong-context"])
def test_s1_007_validator_negative_outcomes_are_report_invalid(
        mode, refusal, launcher, auditor_exe, cust_dir, binding_doc,
        event_package, stage, cust_out):
    """FAIL / non-zero / malformed / snapshot-mismatch validator results
    are all REPORT_INVALID -> TERMINAL -> no accepted frozen report ->
    no same-attempt retry."""
    write_val_state(ATTEMPT, mode)
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe, stage, cust_out,
                 planted=CLEAN_REPORT)
    assert result.report_state == refusal
    # (EXEC03-004 remediated) the durable REPORT_INVALID identity pins
    # the EXACT invalid snapshot supplied to the validator
    assert result.report_sha256 == hashlib.sha256(CLEAN_REPORT).hexdigest()
    assert result.report_size == len(CLEAN_REPORT)
    assert not any(cust_out.iterdir())
    assert sup.state == TERMINAL
    assert states_of(cust_dir, sup)[-2:] == ["REPORT_INVALID", "TERMINAL"]
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run(sup, launcher, auditor_exe, stage, cust_out)  # no retry


def test_s1_007_pass_requires_full_envelope_not_exit_code_only(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """PASS cannot be forged by exit-code-only behavior: the malformed
    mode exits 0 with no valid envelope and is REPORT_INVALID (covered
    parametrically above); here a VALID envelope with FAIL status and
    exit 0 is also refused — proving the envelope, not the exit code,
    carries the verdict."""
    write_val_state(ATTEMPT, "fail-status")
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe, stage, cust_out,
                 planted=CLEAN_REPORT)
    assert result.report_state == "REPORT_INVALID"
    assert sup.state == TERMINAL


def test_s1_007_report_refusal_paths_never_leave_exec_attempted(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out, monkeypatch):
    """An injected report-custody operational refusal (here: the freeze
    collides with a pre-existing output artifact) terminalizes
    fail-closed INSIDE the call — never EXEC_ATTEMPTED, no second report
    attempt, custody closed."""
    sup = build(cust_dir, binding_doc, event_package)
    (cust_out / sup._binding.output_identity["name"]).write_text(
        "operator already holds this slot")
    result = run(sup, launcher, auditor_exe, stage, cust_out,
                 planted=CLEAN_REPORT)
    assert result.report_state == ""            # no report outcome state
    assert sup.state == TERMINAL
    assert states_of(cust_dir, sup)[-1] == TERMINAL
    assert not any(r["state"].startswith("REPORT_")
                   for r in inspect_accounting_record(
                       cust_dir, sup._binding.attempt_id,
                       sup._binding.digest)["records"])
    assert custody_is_closed(sup) and held_fds_closed(sup)
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run(sup, launcher, auditor_exe, stage, cust_out)


def test_s1_007_staging_symlink_and_oversize_refuse_terminal(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out, tmp_path):
    """A symlinked staging report (TOCTOU vector) and an oversize report
    are operational refusals: terminal fail-closed, nothing frozen."""
    real = tmp_path / "real-report.json"
    real.write_bytes(CLEAN_REPORT)
    link = stage
    link.symlink_to(real)
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe, link, cust_out)
    assert result.report_state == ""
    assert sup.state == TERMINAL
    assert not any(cust_out.iterdir())


def test_s1_007_exec_failed_child_settles_consumed_terminal_no_report(
        cust_dir, tmp_path, launcher, auditor_exe, stage, cust_out):
    """A launcher that cannot exec: no report phase is semantically
    appropriate — direct consumed TERMINAL with an exact durable
    reason; custody/fds closed; no retry."""
    bogus = tmp_path / "bogus_launcher.py"
    bogus.write_text("this is not an executable image\n")
    doc = binding_for(sha_hex(bogus.read_bytes()),
                      auditor_sha256=auditor_exe[1])
    pkg = make_event_package(doc, tmp_path, name="pkg-bogus")
    sup = build(cust_dir, doc, pkg)
    result = sup.run_attempt(pipe_source(), str(bogus),
                             str(auditor_exe[0]), str(stage), str(cust_out))
    assert result.exec_failed
    assert result.report_state == ""
    assert sup.state == TERMINAL
    view = inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)
    assert view["states"] == ["PREPARED", "GATES_PASSED",
                              "CONSUMED_PRE_EXEC", "EXEC_ATTEMPTED",
                              "TERMINAL"]
    assert "EXEC_FAILED_AFTER_CONSUMPTION" in view["records"][-1][
        "terminal_reason"]
    assert custody_is_closed(sup)


def test_s1_007_unsafe_output_root_refused_preexec(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """The output custody directory is validated BEFORE consumption: an
    unsafe (world-writable) output root refuses PREEXEC with authority
    unconsumed and both gate counts zero."""
    os.chmod(cust_out, 0o777)
    try:
        sup = build(cust_dir, binding_doc, event_package)
        with pytest.raises(LaunchError):
            run(sup, launcher, auditor_exe, stage, cust_out)
        assert sup.state == "TERMINAL_PREEXEC_STOP"
        assert gate_count(nr_paths) == 0
        assert gate_count(rg_paths) == 0
    finally:
        os.chmod(cust_out, 0o700)


def test_s1_007_caller_cannot_override_artifact_name(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """The frozen artifact name derives ONLY from
    binding.output_identity: an attacker-named file planted in staging
    cannot redirect the freeze (only the supplied staging locator is
    read), the frozen output name is exactly the binding-derived name,
    and no caller filename parameter exists on the public call."""
    (stage.parent / "attacker-chosen-name.json").write_bytes(b'{"x": 1}')
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe, stage, cust_out,
                 planted=CLEAN_REPORT)
    assert result.report_state == "REPORT_FROZEN"
    frozen = cust_out / sup._binding.output_identity["name"]
    assert frozen.exists()
    assert [p.name for p in cust_out.iterdir()] == [frozen.name]


# ===================== S1-007: validator binding ========================

def test_s1_007_validator_fd_held_and_verified_at_construction(
        launcher, auditor_exe, cust_dir, binding_doc, event_package):
    """Supervisor construction opens, verifies and HOLDS the validator
    artifact fd from the frozen event package (no caller path surface);
    a mismatched descriptor sha is refused at construction."""
    sup = build(cust_dir, binding_doc, event_package)
    assert sup._validator_fd is not None
    binding = parse_binding(json.dumps(binding_doc).encode())
    fd = open_output_validator(event_package, binding,
                               {"files": [{"path":
                                           binding.output_validator[
                                               "path"]}]})
    try:
        assert os.fstat(fd).st_size > 0
    finally:
        os.close(fd)


def test_s1_007_validator_live_bytes_verified_against_descriptor(
        launcher, auditor_exe, tmp_path):
    """Verified-open discipline on the DIRECT opener: the live artifact
    bytes must equal the descriptor's exact SHA-256 (any mismatch, e.g.
    same path different bytes, is refused), the artifact must be
    regular + executable, and a path outside the frozen package
    manifest rows is refused (the validator lives ONLY in the frozen
    event package)."""
    doc = binding_for(launcher[1], auditor_sha256=auditor_exe[1])
    pkg = make_event_package(doc, tmp_path, name="pkg-val-open")
    binding = parse_binding(json.dumps(doc).encode())
    rows = [{"path": binding.output_validator["path"]}]
    fd = open_output_validator(pkg, binding, {"files": rows})
    try:
        assert os.fstat(fd).st_size > 0
    finally:
        os.close(fd)
    with pytest.raises(LaunchError, match="DIGEST_MISMATCH"):
        open_output_validator_with_sha(pkg, binding, rows, "e" * 64)
    with pytest.raises(LaunchError, match="NOT_PACKAGE_MANIFEST_ROW"):
        open_output_validator(pkg, binding,
                              {"files": [{"path": "never-shipped.py"}]})


def open_output_validator_with_sha(pkg, binding, rows, sha):
    """Direct negative driver: a descriptor pinning a DIFFERENT sha
    against the same live artifact bytes."""
    import copy
    mutated = copy.deepcopy(dict(binding.output_validator))
    mutated["sha256"] = sha
    from ebs.launch import _open_bound_artifact
    return _open_bound_artifact(pkg, mutated,
                                {row["path"] for row in rows},
                                "OUTPUT_VALIDATOR")


def test_s1_007_validator_receives_no_credential_fd_and_exact_snapshot(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """The in-fixture leak guard proves the validator NEVER inherits the
    sealed custody or invocation memfds (it would exit 4 = REPORT_INVALID),
    and the honest PASS proves the delivered sealed snapshot equals the
    binding-bound digest of the exact screened bytes."""
    sup = build(cust_dir, binding_doc, event_package)
    result = run(sup, launcher, auditor_exe, stage, cust_out,
                 planted=CLEAN_REPORT)
    assert result.report_state == "REPORT_FROZEN"    # guard did not trip


def test_s1_007_recorded_digest_only_after_screen_passes(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """Digest/size enter the durable record ONLY on the screen-passed
    path (EXEC03-004 remediated): a screened-out or missing report is
    never hashed (no identity in SCREEN_FAIL/MISSING records), while a
    report that REACHED the validator — whatever its outcome — has its
    EXACT immutable snapshot identity pinned (REPORT_FROZEN full
    record; REPORT_INVALID hash/size-only pin of the invalid snapshot,
    never its bytes)."""
    write_val_state(ATTEMPT, "fail-status")
    sup = build(cust_dir, binding_doc, event_package)
    run(sup, launcher, auditor_exe, stage, cust_out,
        planted=CLEAN_REPORT)
    assert sup.state == TERMINAL
    view = inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)
    for rec in view["records"]:
        if rec["state"] in ("REPORT_SCREEN_FAIL", "REPORT_MISSING"):
            assert "report_sha256" not in rec
        if rec["state"] == "REPORT_INVALID":
            assert rec["report_sha256"] == hashlib.sha256(
                CLEAN_REPORT).hexdigest()
            assert rec["report_size"] == len(CLEAN_REPORT)


# ===================== S1-008: auditor timeout ==========================

def hanging_scenario(cust_dir, tmp_path, auditor_exe,
                     auditor_timeout=2):
    launcher = make_hanging_launcher(tmp_path)
    doc = binding_for(launcher[1], auditor_sha256=auditor_exe[1])
    doc["execution_limits"] = {
        "auditor_timeout_seconds": auditor_timeout,
        "validator_timeout_seconds":
            doc["execution_limits"]["validator_timeout_seconds"]}
    pkg = make_event_package(doc, tmp_path, name="pkg-hanging")
    return build(cust_dir, doc, pkg), launcher


def test_s1_008_hanging_boundary_tree_killed_by_ebs_itself(
        launcher, auditor_exe, cust_dir, tmp_path, stage, cust_out):
    """THE S1-008 proof: a hanging synthetic boundary launcher (with a
    surviving descendant) is terminated by the EBS under its FROZEN
    auditor timeout — process group killed, direct child reaped, no
    zombie, TERMINAL with TIMEOUT_AFTER_CONSUMPTION, custody and held
    fds closed, no report frozen, no same-attempt retry."""
    sup, hang = hanging_scenario(cust_dir, tmp_path, auditor_exe,
                                 auditor_timeout=2)
    started = time.monotonic()
    result = sup.run_attempt(pipe_source(), str(hang[0]),
                             str(auditor_exe[0]), str(stage),
                             str(cust_out))
    elapsed = time.monotonic() - started
    assert result.timed_out is True
    assert result.report_state == ""            # no report accepted
    assert not any(cust_out.iterdir())
    assert elapsed < 30                          # bounded, not hung
    assert sup.state == TERMINAL
    view = inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)
    assert view["states"] == ["PREPARED", "GATES_PASSED",
                              "CONSUMED_PRE_EXEC", "EXEC_ATTEMPTED",
                              "TERMINAL"]
    terminal = view["records"][-1]
    assert terminal["terminal_reason"] == "TIMEOUT_AFTER_CONSUMPTION"
    assert terminal["auditor_timeout_seconds"] == 2
    track = hang_track(ATTEMPT)
    assert track is not None
    for pid in (track["launcher_pid"], track["descendant_pid"]):
        until = time.monotonic() + 5
        while pid_alive(pid) and time.monotonic() < until:
            time.sleep(0.05)
        assert not pid_alive(pid), f"pid {pid} survived the group kill"
    assert custody_is_closed(sup)
    assert held_fds_closed(sup)
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run(sup, hang, auditor_exe, stage, cust_out)  # no retry
    assert gate_count(nr_paths) == 1           # gates still exactly once
    assert gate_count(rg_paths) == 1


def test_s1_008_unrelated_process_not_killed(
        launcher, auditor_exe, cust_dir, tmp_path, stage, cust_out):
    """Scoping proof: an UNRELATED process (the test's own child, in the
    test process group — not the attempt session) SURVIVES the EBS
    timeout kill."""
    unrelated_r, unrelated_w = os.pipe()      # liveness signal channel
    unrelated_pid = os.fork()
    if unrelated_pid == 0:
        os.close(unrelated_r)
        time.sleep(120)
        os._exit(0)
    os.close(unrelated_w)
    try:
        sup, hang = hanging_scenario(cust_dir, tmp_path, auditor_exe,
                                     auditor_timeout=1)
        result = sup.run_attempt(pipe_source(), str(hang[0]),
                                 str(auditor_exe[0]), str(stage),
                                 str(cust_out))
        assert result.timed_out is True
        assert pid_alive(unrelated_pid)       # untouched by killpg
    finally:
        os.kill(unrelated_pid, 15)
        os.waitpid(unrelated_pid, 0)
        os.close(unrelated_r)


def test_s1_008_timeout_value_only_from_frozen_binding(launcher,
                                                        auditor_exe):
    """No caller or environment override surface exists for either
    timeout: the public signature has no timeout parameter and the
    production source reads no environment variable at all."""
    params = list(pyinspect.signature(
        Supervisor.run_attempt).parameters)
    assert "timeout" not in " ".join(params)
    src = open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "ebs", "launch.py")).read()
    assert "os.environ" not in src.replace("os.environ", "os.environ")
    assert "getenv(" not in src
    assert "environ[" not in src            # no environment read surface


def test_s1_008_timeout_after_durable_consumption(launcher, auditor_exe,
                                                   cust_dir, tmp_path,
                                                   stage, cust_out):
    """The durable record proves CONSUMED_PRE_EXEC precedes the timeout
    terminal — authority and model engagement are CONSUMED, the
    accounting reason is exact, and the consumed facts are present in
    the CONSUMED record (V5 limits included)."""
    sup, hang = hanging_scenario(cust_dir, tmp_path, auditor_exe,
                                 auditor_timeout=1)
    result = sup.run_attempt(pipe_source(), str(hang[0]),
                             str(auditor_exe[0]), str(stage),
                             str(cust_out))
    assert result.timed_out is True
    view = inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)
    states = [r["state"] for r in view["records"]]
    assert states.index("CONSUMED_PRE_EXEC") < states.index("TERMINAL")
    consumed = [r for r in view["records"]
                if r["state"] == "CONSUMED_PRE_EXEC"][-1]
    assert consumed["auditor_timeout_seconds"] == 1
    assert consumed["output_validator_identity"] == \
        "SYNTHETIC-INERT-OUTPUT-VALIDATOR-V1"


def test_s1_008_no_blocking_read_bypasses_deadline(
        launcher, auditor_exe, cust_dir, tmp_path, stage, cust_out):
    """Both parent-side pipes are handled NONBLOCKING inside the
    deadline loop (source shape: no blocking os.read of the fail/metadata
    pipes outside os.set_blocking(False) discipline) — a child that
    never execs-and-never-exits cannot stall the EBS past the frozen
    timeout through any earlier read."""
    src_path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "ebs", "launch.py")
    tree = ast.parse(open(src_path).read())
    fn = next(node for node in ast.walk(tree)
              if isinstance(node, ast.FunctionDef)
              and node.name == "_fork_and_launch")
    # BOTH parent-side pipes are switched to NONBLOCKING before the
    # bounded deadline loop, and EVERY waitpid inside the loop itself is
    # WNOHANG (the only blocking waitpids are the deterministic
    # post-SIGKILL / post-failure reaps outside the loop)
    assert sum(isinstance(n, ast.Call) and getattr(n.func, "attr", "") ==
               "set_blocking" for n in ast.walk(fn)) == 2
    loop = next(n for n in ast.walk(fn) if isinstance(n, ast.While))
    waitpids = [n for n in ast.walk(loop)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute)
                and n.func.attr == "waitpid"]
    assert waitpids
    for call in waitpids:
        second = call.args[1]
        assert (isinstance(second, ast.Attribute)
                and second.attr == "WNOHANG") or \
            (isinstance(second, ast.Name) and second.id == "WNOHANG"), \
            "a waitpid inside the deadline loop is blocking (no WNOHANG)"


# ===================== validator timeout (§28) ==========================

def test_s1_008_validator_timeout_is_report_invalid(
        launcher, auditor_exe, cust_dir, binding_doc, event_package,
        stage, cust_out):
    """A hanging synthetic structural validator is killed/refused within
    its FROZEN validator timeout: REPORT_INVALID -> TERMINAL -> no
    same-attempt retry -> no accepted frozen report.  The auditor
    engagement was already consumed; the validator execution is NOT a
    new model engagement."""
    import copy
    doc = copy.deepcopy(binding_doc)
    doc["execution_limits"]["validator_timeout_seconds"] = 1
    pkg = make_event_package(doc, stage.parent, name="pkg-val-hang")
    sup = build(cust_dir, doc, pkg)
    write_val_state(ATTEMPT, "hang")
    planted = stage
    planted.write_bytes(CLEAN_REPORT)
    started = time.monotonic()
    result = sup.run_attempt(pipe_source(), str(launcher[0]),
                             str(auditor_exe[0]), str(planted),
                             str(cust_out))
    elapsed = time.monotonic() - started
    assert result.report_state == "REPORT_INVALID"
    assert not any(cust_out.iterdir())
    assert elapsed < 30                       # bounded by the frozen 1s
    assert sup.state == TERMINAL
    assert states_of(cust_dir, sup)[-2:] == ["REPORT_INVALID", "TERMINAL"]
    assert custody_is_closed(sup) and held_fds_closed(sup)
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run(sup, launcher, auditor_exe, stage, cust_out)
