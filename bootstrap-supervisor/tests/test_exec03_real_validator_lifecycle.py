"""EXEC-03 structural remediation focused suites (AUCDEV023-CR-S1-
EXEC03-001/-002/-003/-004 regression).

Every credential byte here is SYNTHETIC and INERT; the event id, attempt
id and every report field are unmistakably synthetic; the ONLY
non-fixture executable is the REAL frozen structural first-pass
validator (byte-exact materialization, identity asserted per use) — the
exact frozen deployed component the EBS holds and executes — run
through the EXACT EBS validator execution path against SYNTHETIC
reports only.  No provider, no network, no real event package, no real
event id, no Auditor substance.

Coverage required by the remediation authority §8/§9/§11:

  V1  a structurally valid synthetic report (coverage booleans) PASSES
      the REAL validator and freezes (REPORT_FROZEN);
  V2  coverage[*].covered as the STRING "COVERED" is REPORT_INVALID
      with NO rc-120 masking and the exact safe structural diagnostic
      COVERAGE_0_COVERED_NOT_BOOL in the durable reason (EXEC03-001 +
      the wire type the corrected contract now states — EXEC03-003);
  V3  the durable REPORT_INVALID record pins the EXACT invalid snapshot
      SHA-256/size (EXEC03-004);
  V4  NO substantive report text appears in any durable or mechanical
      surface (reason, result, accounting bytes);
  V5  stderr over-size and malformed diagnostics fail closed (bounded
      generic refusal, never arbitrary child text);
  V6  no second validator attempt, no auditor retry;
  V7  the REAL validator still rejects every pre-existing structural
      negative of its contract with the exact safe token (or a generic
      refusal for non-token diagnostics) and no prose leak.

  U*  the bounded structural-only diagnostic grammar and the
      capture_stderr channel are unit-pinned, including that NON-
      validator gates retain the exact historical read-only-stderr fd
      shape (no rc-120 change where the authority requires none).
"""
import hashlib
import json
import os
import sys

import pytest

from ebs.accounting import AccountingStore, inspect_accounting_record
from ebs.binding import parse_binding
from ebs.launch import (LaunchError, LaunchRefused, Supervisor,
                        _run_runtime_gate, _sanitize_structural_diagnostic,
                        VALIDATOR_STDERR_MAX)
from ebs.statemachine import TERMINAL

from conftest import (SYNTH_CRED, clear_nr_tracks, clear_rg_tracks,
                      clear_val_tracks, make_auditor_executable,
                      make_event_package, make_launcher, pipe_source,
                      valid_binding_document)
from real_validator_materialization import (REAL_VALIDATOR_IDENTITY,
                                            REAL_VALIDATOR_SHA256,
                                            real_validator_bytes)

EVENT = "evt-0000e03c0de0aa55"
ROLE = "AUDITOR_A"
ATTEMPT = EVENT + "-A-01"
TARGET_COMMIT = "0123456789abcdef0123456789abcdef01234567"
PROSE_MARKERS = ["SUMMARY-MARKER-9d1f6a2b", "NOTE-MARKER-4c7e81dd",
                 "METHODOLOGY-MARKER-2b9a40c1"]


@pytest.fixture(autouse=True)
def clean_tracks():
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    clear_val_tracks(ATTEMPT)
    yield
    clear_rg_tracks(ATTEMPT)
    clear_nr_tracks(ATTEMPT)
    clear_val_tracks(ATTEMPT)


def synth_report(covered=True, coverage_count=2):
    """A schema-conforming SYNTHETIC first-pass report; covered is the
    value placed in coverage[*].covered (bool = conforming, the STRING
    'COVERED' = the exact EXEC-03 structural-defect shape)."""
    return {
        "schema": "AUCDEV-023-FIRST-PASS-REPORT-V1",
        "event_id": EVENT,
        "auditor_role": ROLE,
        "attempt_id": ATTEMPT,
        "target_commit": TARGET_COMMIT,
        "summary": "synthetic summary " + PROSE_MARKERS[0],
        "findings": [],
        "coverage": [
            {"area": "synthetic-area-%d" % index,
             "covered": covered,
             "note": ("note " + PROSE_MARKERS[1]) if index == 0 else ""}
            for index in range(coverage_count)
        ],
        "residuals": [],
        "methodology": "synthetic methodology " + PROSE_MARKERS[2],
    }


def render(report) -> bytes:
    return (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()


def build_real(tmp_path):
    """One synthetic event package whose bound validator is the EXACT
    frozen REAL validator bytes, plus its Supervisor."""
    launcher = make_launcher(tmp_path)
    auditor = make_auditor_executable(tmp_path)
    doc = valid_binding_document(
        event_id=EVENT, role=ROLE, launcher_sha256=launcher[1],
        executable_sha256=auditor[1])
    doc["output_validator"] = {
        "identity": REAL_VALIDATOR_IDENTITY,
        "path": "runtime/output-validator.py",
        "sha256": "0" * 64,        # pinned to live bytes by the builder
        "result_schema": "AUCDEV-023-REPORT-VALIDATOR-RESULT-V1",
    }
    pkg = make_event_package(doc, tmp_path, name="pkg-exec03-real",
                             validator_bytes=real_validator_bytes())
    assert doc["output_validator"]["sha256"] == REAL_VALIDATOR_SHA256
    binding = parse_binding(json.dumps(doc).encode())
    cust_dir = tmp_path / "accounting"
    cust_dir.mkdir(mode=0o700)
    os.chmod(cust_dir, 0o700)
    out_root = tmp_path / "custody-out"
    out_root.mkdir(mode=0o700)
    os.chmod(out_root, 0o700)
    store = AccountingStore.create(cust_dir, binding.attempt_id,
                                   binding.digest)
    sup = Supervisor(binding, store, pkg)
    stage = tmp_path / "staging" / "stage.json"
    stage.parent.mkdir()
    return sup, launcher, auditor, stage, out_root, cust_dir


def run_planted(sup, launcher, auditor, stage, out_root, payload):
    stage.write_bytes(payload)
    return sup.run_attempt(pipe_source(), str(launcher[0]),
                           str(auditor[0]), str(stage), str(out_root))


def view_of(cust_dir, sup):
    return inspect_accounting_record(cust_dir, sup._binding.attempt_id,
                                     sup._binding.digest)


def invalid_record(view):
    return next(rec for rec in view["records"]
                if rec["state"] == "REPORT_INVALID")


def accounting_raw_bytes(cust_dir, sup) -> bytes:
    return (cust_dir / (sup._binding.attempt_id + ".jsonl")).read_bytes()


def assert_no_prose(*surfaces):
    for surface in surfaces:
        text = surface if isinstance(surface, str) else repr(surface)
        for marker in PROSE_MARKERS:
            assert marker not in text, \
                f"substantive report text leaked into a durable surface: {marker}"


# ================= V1: conforming report -> PASS -> frozen =============

def test_exec03_v1_conforming_boolean_report_passes_and_freezes(tmp_path):
    """Through the EXACT EBS path the REAL frozen validator ACCEPTS a
    structurally conforming synthetic report (coverage booleans true AND
    false — true means COVERED, false means NOT covered) and the report
    proceeds to REPORT_FROZEN in the synthetic lifecycle."""
    sup, launcher, auditor, stage, out_root, cust_dir = \
        build_real(tmp_path)
    payload = render(synth_report(covered=True))
    result = run_planted(sup, launcher, auditor, stage, out_root, payload)
    assert result.report_state == "REPORT_FROZEN"
    assert result.report_sha256 == hashlib.sha256(payload).hexdigest()
    assert result.report_size == len(payload)
    frozen = out_root / sup._binding.output_identity["name"]
    assert frozen.read_bytes() == payload
    assert sup.state == TERMINAL
    assert view_of(cust_dir, sup)["states"][-2:] == ["REPORT_FROZEN",
                                                     TERMINAL]


def test_exec03_v1_false_covered_also_conforming(tmp_path):
    """covered=false (NOT covered) is exactly as conforming as true —
    the wire type is boolean, not truthiness."""
    sup, launcher, auditor, stage, out_root, _ = build_real(tmp_path)
    payload = render(synth_report(covered=False))
    result = run_planted(sup, launcher, auditor, stage, out_root, payload)
    assert result.report_state == "REPORT_FROZEN"


# ================= V2/V3/V4/V6: the EXEC-03 defect shape ===============

def test_exec03_v2_string_covered_report_invalid_safe_diagnostic(tmp_path):
    """The exact EXEC-03 structural defect — coverage[*].covered as the
    JSON STRING 'COVERED' — is REPORT_INVALID with NO rc-120 masking:
    the real validator's intended structural failure is visible as the
    bounded safe diagnostic structural_error=COVERAGE_0_COVERED_NOT_BOOL
    in the durable terminal reason."""
    sup, launcher, auditor, stage, out_root, cust_dir = \
        build_real(tmp_path)
    payload = render(synth_report(covered="COVERED"))
    result = run_planted(sup, launcher, auditor, stage, out_root, payload)
    assert result.report_state == "REPORT_INVALID"
    assert sup.state == TERMINAL
    record = invalid_record(view_of(cust_dir, sup))
    reason = record["terminal_reason"]
    assert "exited 120" not in reason            # no rc-120 masking
    assert "structural_error=COVERAGE_0_COVERED_NOT_BOOL" in reason
    assert not any(out_root.iterdir())           # nothing frozen
    # V4: no substantive text in any durable/mechanical surface
    assert_no_prose(reason, repr(result),
                    accounting_raw_bytes(cust_dir, sup).decode(
                        errors="replace"))


def test_exec03_v3_invalid_snapshot_identity_durably_recorded(tmp_path):
    """The REPORT_INVALID accounting record and AttemptResult pin the
    EXACT immutable snapshot supplied to the validator: report_sha256 /
    report_size equal the exact planted bytes (hash/size ONLY — the
    report bytes themselves are never retained as mechanical
    evidence)."""
    sup, launcher, auditor, stage, out_root, cust_dir = \
        build_real(tmp_path)
    payload = render(synth_report(covered="COVERED"))
    result = run_planted(sup, launcher, auditor, stage, out_root, payload)
    expect_sha = hashlib.sha256(payload).hexdigest()
    assert result.report_state == "REPORT_INVALID"
    assert result.report_sha256 == expect_sha
    assert result.report_size == len(payload)
    record = invalid_record(view_of(cust_dir, sup))
    assert record["report_sha256"] == expect_sha
    assert record["report_size"] == len(payload)
    assert "report_sha256" in record and "report_size" in record
    # nothing frozen; the operator's own staging file remains in the
    # OPERATOR plane exactly as in the historical lifecycle (only the
    # custody-output plane is EBS-controlled), and the invalid bytes
    # never enter the durable MECHANICAL record
    assert not any(out_root.iterdir())
    assert payload not in accounting_raw_bytes(cust_dir, sup)


def test_exec03_v6_no_second_validator_attempt_no_retry(tmp_path):
    """After the terminal REPORT_INVALID there is no second validator
    attempt and no auditor retry: exactly one EXEC_ATTEMPTED and one
    REPORT_INVALID durable record, and the second run_attempt call is
    refused."""
    sup, launcher, auditor, stage, out_root, cust_dir = \
        build_real(tmp_path)
    payload = render(synth_report(covered="COVERED"))
    run_planted(sup, launcher, auditor, stage, out_root, payload)
    view = view_of(cust_dir, sup)
    assert view["states"].count("EXEC_ATTEMPTED") == 1
    assert view["states"].count("REPORT_INVALID") == 1
    assert view["states"][-1] == TERMINAL
    with pytest.raises(LaunchError, match="RUN_ATTEMPT_REFUSED"):
        run_planted(sup, launcher, auditor, stage, out_root, payload)


# ================= V5: fail-closed stderr channel bounds ===============

def _misbehaving_gate(tmp_path, body):
    src = f"#!{sys.executable}\nimport os, sys\n{body}\n"
    path = tmp_path / ("misbehave_" + hashlib.sha256(
        body.encode()).hexdigest()[:8] + ".py")
    path.write_text(src)
    os.chmod(path, 0o755)
    return path


def _run_gate_with(gate_path, argv):
    fd = os.open(gate_path, os.O_RDONLY)
    try:
        return _run_runtime_gate(
            "OUTPUT_VALIDATOR", fd, argv,
            {"PATH": "/usr/bin:/bin", "LANG": "C"}, timeout=30,
            capture_stderr=True)
    finally:
        os.close(fd)


def test_exec03_v5a_oversize_stderr_fails_closed(tmp_path):
    """A validator child emitting more than VALIDATOR_STDERR_MAX stderr
    bytes is refused fail-closed — bounded channel, no diagnostic, no
    hang."""
    gate = _misbehaving_gate(
        tmp_path,
        "os.write(2, b'VALIDATION_ERROR: ' + b'A' * "
        f"{VALIDATOR_STDERR_MAX + 1})\nsys.exit(1)")
    with pytest.raises(LaunchRefused, match="STDERR_TOO_LARGE"):
        _run_gate_with(gate, ["x", "e", "r", "a", "o", "0", "0"])


def test_exec03_v5b_malformed_stderr_diagnostic_fails_closed(tmp_path):
    """Arbitrary (non-VALIDATION_ERROR) child stderr NEVER enters the
    durable reason: the refusal stays the bounded generic NONZERO_EXIT
    form with no structural_error and no child text."""
    gate = _misbehaving_gate(
        tmp_path,
        "os.write(2, b'arbitrary child prose MARKER 12345\\n')\n"
        "sys.exit(1)")
    with pytest.raises(LaunchRefused) as excinfo:
        _run_gate_with(gate, ["x", "e", "r", "a", "o", "0", "0"])
    message = str(excinfo.value)
    assert message == "OUTPUT_VALIDATOR_NONZERO_EXIT: exited 1"
    assert "arbitrary" not in message and "MARKER" not in message


def test_exec03_v5c_valid_token_stderr_visible_in_refusal(tmp_path):
    """A genuine structural VALIDATION_ERROR token on stderr is carried
    into the bounded refusal detail (the EXEC03-001 remediated
    channel)."""
    gate = _misbehaving_gate(
        tmp_path,
        "os.write(2, b'VALIDATION_ERROR: COVERAGE_0_COVERED_NOT_BOOL"
        "\\n')\nsys.exit(1)")
    with pytest.raises(LaunchRefused) as excinfo:
        _run_gate_with(gate, ["x", "e", "r", "a", "o", "0", "0"])
    assert str(excinfo.value) == ("OUTPUT_VALIDATOR_NONZERO_EXIT: "
                                  "exited 1; "
                                  "structural_error="
                                  "COVERAGE_0_COVERED_NOT_BOOL")


# ================= V7: real validator structural negatives =============

NEGATIVES = [
    ("unknown_top_key",
     lambda r: r.update({"extra_key": 1}), "REPORT_KEYS_INVALID", True),
    ("missing_methodology",
     lambda r: r.pop("methodology"), "REPORT_KEYS_INVALID", True),
    ("wrong_schema_value",
     lambda r: r.update({"schema": "SOMETHING-ELSE"}),
     "REPORT_SCHEMA_UNEXPECTED", True),
    ("event_mismatch",
     lambda r: r.update({"event_id": "evt-ffffffffffffffff"}),
     "REPORT_EVENT_MISMATCH", True),
    ("role_mismatch",
     lambda r: r.update({"auditor_role": "AUDITOR_B"}),
     "REPORT_ROLE_MISMATCH", True),
    ("attempt_mismatch",
     lambda r: r.update({"attempt_id": EVENT + "-B-01"}),
     "REPORT_ATTEMPT_MISMATCH", True),
    ("target_commit_malformed",
     lambda r: r.update({"target_commit": "zzz"}),
     "REPORT_TARGET_COMMIT_MALFORMED", True),
    ("summary_empty",
     lambda r: r.update({"summary": "   "}), "SUMMARY_EMPTY", True),
    ("summary_not_a_string",
     lambda r: r.update({"summary": 42}), "SUMMARY_NOT_A_STRING", True),
    ("findings_not_a_list",
     lambda r: r.update({"findings": {"id": "x"}}), "FINDINGS_NOT_A_LIST",
     True),
    ("finding_severity_invalid",
     lambda r: r.update({"findings": [{"id": "f1", "title": "t",
                                       "severity": "BLOCKER",
                                       "description": "d",
                                       "evidence": []}]}),
     "FINDING_0_SEVERITY_INVALID", True),
    ("coverage_not_a_list",
     lambda r: r.update({"coverage": {"area": "x"}}),
     "COVERAGE_NOT_A_LIST", True),
    ("coverage_item_keys_invalid",
     lambda r: r.update({"coverage": [{"area": "a", "covered": True}]}),
     "COVERAGE_INVALID_AT_0", True),
    ("coverage_area_empty",
     lambda r: r["coverage"][0].update({"area": "  "}),
     "COVERAGE_0_AREA_EMPTY", True),
    ("residuals_not_a_list",
     lambda r: r.update({"residuals": "no"}), "RESIDUALS_NOT_A_LIST",
     True),
]


@pytest.mark.parametrize("name,mutate,token,token_expected", NEGATIVES,
                         ids=[row[0] for row in NEGATIVES])
def test_exec03_v7_real_validator_structural_negatives(
        name, mutate, token, token_expected, tmp_path):
    """Every pre-existing structural negative of the REAL validator's
    contract stays REFUSED (REPORT_INVALID, terminal, no retry): the
    safe diagnostic carries the exact structural token when the token
    grammar covers it, never report prose, never rc-120."""
    sup, launcher, auditor, stage, out_root, cust_dir = \
        build_real(tmp_path)
    report = synth_report(covered=True)
    mutate(report)
    payload = render(report)
    result = run_planted(sup, launcher, auditor, stage, out_root, payload)
    assert result.report_state == "REPORT_INVALID"
    assert sup.state == TERMINAL
    record = invalid_record(view_of(cust_dir, sup))
    reason = record["terminal_reason"]
    assert "exited 120" not in reason
    if token_expected:
        assert f"structural_error={token}" in reason
    assert result.report_sha256 == hashlib.sha256(payload).hexdigest()
    assert result.report_size == len(payload)
    assert_no_prose(reason, repr(result))
    assert not any(out_root.iterdir())


def test_exec03_v7_malformed_json_generic_refusal_no_prose(tmp_path):
    """A non-JSON snapshot yields the validator's parser-diagnostic
    class, which the structural-token grammar correctly REFUSES: the
    durable reason stays generic (bounded NONZERO_EXIT, no parser
    prose, no rc-120)."""
    sup, launcher, auditor, stage, out_root, cust_dir = \
        build_real(tmp_path)
    payload = b'{"this is not valid json ' + PROSE_MARKERS[0].encode() \
        + b'\n'
    result = run_planted(sup, launcher, auditor, stage, out_root, payload)
    assert result.report_state == "REPORT_INVALID"
    record = invalid_record(view_of(cust_dir, sup))
    reason = record["terminal_reason"]
    assert "exited 120" not in reason
    assert "structural_error=" not in reason
    assert result.report_sha256 == hashlib.sha256(payload).hexdigest()
    assert result.report_size == len(payload)
    assert_no_prose(reason, repr(result),
                    accounting_raw_bytes(cust_dir, sup).decode(
                        errors="replace"))


def test_exec03_v7_duplicate_keys_token_without_key_name(tmp_path):
    """A duplicate-key report yields the DUPLICATE_KEY structural token
    with the duplicated KEY NAME itself never persisted (bounded
    token-only diagnostic)."""
    sup, launcher, auditor, stage, out_root, cust_dir = \
        build_real(tmp_path)
    payload = (b'{"schema": "A", "schema": "B", '
               b'"MARKER-DUPKEY-51ab77": 1, '
               b'"MARKER-DUPKEY-51ab77": 2}')
    result = run_planted(sup, launcher, auditor, stage, out_root, payload)
    assert result.report_state == "REPORT_INVALID"
    record = invalid_record(view_of(cust_dir, sup))
    reason = record["terminal_reason"]
    assert "structural_error=DUPLICATE_KEY" in reason
    assert "MARKER-DUPKEY-51ab77" not in reason
    assert result.report_sha256 == hashlib.sha256(payload).hexdigest()
    assert_no_prose(reason,
                    accounting_raw_bytes(cust_dir, sup).decode(
                        errors="replace"))


def test_exec03_v7_non_utf8_generic_refusal(tmp_path):
    """Non-UTF-8 snapshot bytes: codec diagnostics are refused by the
    token grammar (generic bounded reason), still REPORT_INVALID, still
    no rc-120."""
    sup, launcher, auditor, stage, out_root, cust_dir = \
        build_real(tmp_path)
    payload = b"\xff\xfe\x00\x81 not utf8 " + PROSE_MARKERS[1].encode()
    result = run_planted(sup, launcher, auditor, stage, out_root, payload)
    assert result.report_state == "REPORT_INVALID"
    reason = invalid_record(view_of(cust_dir, sup))["terminal_reason"]
    assert "exited 120" not in reason
    assert "structural_error=" not in reason
    assert result.report_sha256 == hashlib.sha256(payload).hexdigest()
    assert_no_prose(reason)


# ================= U*: diagnostic grammar unit pins ====================

def test_exec03_u1_sanitizer_accepts_pure_structural_tokens():
    assert _sanitize_structural_diagnostic(
        b"VALIDATION_ERROR: COVERAGE_0_COVERED_NOT_BOOL\n") == \
        "COVERAGE_0_COVERED_NOT_BOOL"
    assert _sanitize_structural_diagnostic(
        b"VALIDATION_ERROR: REPORT_EVENT_MISMATCH") == \
        "REPORT_EVENT_MISMATCH"


def test_exec03_u2_sanitizer_keeps_token_drops_detail():
    """Pre-colon structural token only: validator detail suffixes
    (duplicate key names, repr'd values) never survive."""
    assert _sanitize_structural_diagnostic(
        b"VALIDATION_ERROR: DUPLICATE_KEY: MARKER-DUPKEY-51ab77\n") == \
        "DUPLICATE_KEY"
    assert _sanitize_structural_diagnostic(
        b"VALIDATION_ERROR: REPORT_SCHEMA_UNEXPECTED: "
        b"'arbitrary prose value'\n") == "REPORT_SCHEMA_UNEXPECTED"


def test_exec03_u3_sanitizer_refuses_non_token_diagnostics():
    assert _sanitize_structural_diagnostic(
        b"VALIDATION_ERROR: Expecting value: line 1 column 2 (char 1)\n") \
        == ""
    assert _sanitize_structural_diagnostic(
        b"VALIDATION_ERROR: coverage_0_lower\n") == ""
    assert _sanitize_structural_diagnostic(b"arbitrary prose\n") == ""
    assert _sanitize_structural_diagnostic(b"") == ""
    assert _sanitize_structural_diagnostic(b"\xff\xfe\x00") == ""
    assert _sanitize_structural_diagnostic(
        b"VALIDATION_ERROR: " + b"A" * 200) == ""


def test_exec03_u4_sanitizer_bounds():
    """Two independent fail-closed bounds: a valid token line at the
    exact channel bound is accepted; one byte over the channel bound
    (or over the 128-char token bound) is refused."""
    exact = b"VALIDATION_ERROR: " + b"A" * (VALIDATOR_STDERR_MAX
                                            - len("VALIDATION_ERROR: "))
    assert len(exact) == VALIDATOR_STDERR_MAX
    assert _sanitize_structural_diagnostic(exact[:len(
        "VALIDATION_ERROR: ") + 128]) == "A" * 128
    assert _sanitize_structural_diagnostic(exact) == ""      # token > 128
    assert _sanitize_structural_diagnostic(exact + b"A") == ""


def test_exec03_u5_non_validator_gates_retain_readonly_stderr(tmp_path):
    """Runtime gates OTHER than the output validator retain the exact
    historical child fd shape (fd 2 dup2'd from an O_RDONLY /dev/null):
    a stderr-writing non-validator child still exits 120 with NO
    captured diagnostic and NO structural_error in the refusal."""
    gate = _misbehaving_gate(
        tmp_path,
        "os.write(2, b'VALIDATION_ERROR: COVERAGE_0_COVERED_NOT_BOOL"
        "\\n')\nsys.exit(1)")
    fd = os.open(gate, os.O_RDONLY)
    try:
        with pytest.raises(LaunchRefused) as excinfo:
            _run_runtime_gate(
                "RESOURCE_GATE", fd, ["x"],
                {"PATH": "/usr/bin:/bin", "LANG": "C"}, timeout=30)
        message = str(excinfo.value)
        assert message == "RESOURCE_GATE_NONZERO_EXIT: exited 120"
        assert "structural_error" not in message
    finally:
        os.close(fd)
