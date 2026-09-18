"""GATE-W — zero-provider pre-inference write rehearsal tests."""
from __future__ import annotations

import os

import pytest

from qh.boundary import RESULT_FILE_INNER, BoundarySpec, launch
from qh.custody import CredentialCustody, SyntheticInertAdapter
from qh.gatew import evaluate_payload_result, run_static
from qh.noegress import NoEgressSpec
from qh.util import Redactor

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns

SYNTH = "SYNTHETIC-INERT-GATEW-CREDENTIAL"


def _payload_argv():
    # payload paths are INNER boundary paths (harness ro-bound at /opt/qh)
    return ["/usr/bin/python3",
            "/opt/qh/fixtures/gatew_payload.py",
            "--result-file", RESULT_FILE_INNER]


def _custody():
    r, w = os.pipe()
    os.write(w, SYNTH.encode())
    os.close(w)
    return CredentialCustody.establish(r, label="gatew-synthetic",
                                       redactor=Redactor())


def test_static_validation_pass(env):
    failures = run_static(env.codex_artifact["config_path"],
                          env.profile_spec)
    assert failures == []


def test_static_validation_flags_drift(env):
    cfg = env.codex_artifact["config_path"]
    text = open(cfg).read().replace(
        '"/auditor-output" = "write"',
        '"/auditor-output" = "write"\n"/" = "read"')
    with open(cfg, "w") as fh:
        fh.write(text)
    failures = run_static(cfg, env.profile_spec)
    assert "ROOT_WIDE_READ_ENTRY_PRESENT" in failures, failures


def test_evaluate_payload_result_matrix():
    ok = {"ops": [{"name": "n", "path": "p", "expect": "refused",
                   "actual": "refused:13", "ok": True}],
          "custody_file_present": True}
    assert evaluate_payload_result(ok) == []
    bad = {"ops": [{"name": "n", "path": "p", "expect": "refused",
                    "actual": "allowed", "ok": False}],
           "custody_file_present": False}
    failures = evaluate_payload_result(bad)
    assert any(f.startswith("GATEW_OP") for f in failures)
    assert "GATEW_CUSTODY_FILE_ABSENT" in failures


@requires_bwrap
@requires_userns
def test_dynamic_gatew_pass(env):
    """Full GATE-W over the composed boundary: the semantic operation
    matrix holds exactly, custody materialized for the authorized child
    only, hard no-egress inside."""
    custody = _custody()
    adapter = SyntheticInertAdapter()
    plan = custody.child_plan(adapter.child_target_path())
    spec = BoundarySpec(
        harness_root=str(HARNESS_ROOT),
        payload_argv=_payload_argv(),
        ro_binds=[(str(env.evidence), "/evidence"),
                  (str(env.codex_home_dir), "/codex-home"),
                  (str(env.target), "/target")],
        rw_binds=[(str(env.auditor_output), "/auditor-output")],
        env={"CODEX_HOME": "/codex-home"},
        secret_plans=[plan],
        noegress=NoEgressSpec(),
        pass_fds=[plan.fd])
    result = launch(spec, timeout=120)
    try:
        assert result.gate and result.gate["passed"], \
            (result.gate, result.stderr[:400])
        payload = result.payload_result
        assert payload is not None, (result.returncode,
                                     result.stderr[:400])
        assert payload["all_expected"], payload["ops"]
        assert payload["custody_file_present"] is True
        assert payload["custody_length"] == len(SYNTH)
        # auditor-output ops REALLY happened on the host-rw surface
        assert (env.auditor_output / "probe-dir").is_dir()
        assert not (env.evidence / "new-file.txt").exists()
        assert not (env.evidence / "evidence.md.renamed").exists()
    finally:
        custody.teardown()


@requires_bwrap
@requires_userns
def test_dynamic_gatew_widened_evidence_fails(env):
    """REAL GATE-W failure: evidence bound writable (policy drift at the
    outer layer) — the evidence-refused ops come back allowed and GATE-W
    evaluation fails (=> PREEXEC_STOP upstream)."""
    spec = BoundarySpec(
        harness_root=str(HARNESS_ROOT),
        payload_argv=_payload_argv(),
        ro_binds=[(str(env.codex_home_dir), "/codex-home")],
        rw_binds=[(str(env.auditor_output), "/auditor-output"),
                  (str(env.evidence), "/evidence")],  # DRIFT: rw evidence
        noegress=NoEgressSpec())
    result = launch(spec, timeout=120)
    payload = result.payload_result
    assert payload is not None
    assert not payload["all_expected"]
    failures = evaluate_payload_result(payload, custody_required=False)
    assert any("evidence create" in f for f in failures)
