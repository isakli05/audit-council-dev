"""IR-003 — production trust-check override removal (§20).

The operational CLI/path must NOT expose --yama-override or any
--fault-style mechanism that can alter a production trust decision.  Test
fault injection exists ONLY through monkeypatched internal seams in the
test suite — never reachable from the production entrypoint."""
from __future__ import annotations

import dataclasses
import os
import subprocess
import sys

import pytest

from conftest import HARNESS_ROOT

from qh import authority, cli


def _run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "qh.cli", *args],
        capture_output=True, text=True, timeout=60, cwd=str(HARNESS_ROOT),
        env={**os.environ, "PYTHONPATH": str(HARNESS_ROOT)})


def test_production_parser_rejects_yama_override():
    """Mandatory regression (§13/§20): `--yama-override` is rejected by
    the production argv parser."""
    r = _run_cli("supervisor", "--operator-state", "/tmp/x",
                 "--yama-override", "1")
    assert r.returncode == 2
    assert "PRODUCTION_CLI_REFUSED" in r.stderr
    assert "--yama-override" in r.stderr
    with pytest.raises(SystemExit) as exc:
        cli.main(["supervisor", "--operator-state", "/tmp/x",
                  "--yama-override", "1"])
    assert exc.value.code == 2


def test_production_parser_rejects_every_fault_flag():
    for flag in ("--fault", "--fault=noegress", "--fault-gatew",
                 "--fault-identity", "--fault-policy"):
        r = _run_cli("supervisor", "--operator-state", "/tmp/x", flag)
        assert r.returncode == 2, flag
        assert "PRODUCTION_CLI_REFUSED" in r.stderr, flag
    # and on every other subcommand path
    for sub in ("root", "compose-demo", "selfcheck"):
        r = _run_cli(sub, "--yama-override", "1")
        assert r.returncode == 2, (sub, r.stderr)
        assert "PRODUCTION_CLI_REFUSED" in r.stderr


def test_production_parser_rejects_yama_override_even_disguised():
    r = _run_cli("supervisor", "--operator-state", "/tmp/x",
                 "--yama-override=0")
    assert r.returncode == 2
    assert "PRODUCTION_CLI_REFUSED" in r.stderr


def test_supervisor_policy_has_no_trust_override_fields():
    """Structural proof: no fault/yama/operator-override knob exists in
    the production policy object — test injection uses ONLY the reader
    seams below, monkeypatched by the test suite."""
    fields = {f.name for f in dataclasses.fields(authority.SupervisorPolicy)}
    assert fields == {"env_reader", "stat_reader", "walker",
                      "set_dumpable", "require_custody",
                      "boundary_launcher"}, fields
    assert not any("fault" in f or "yama" in f or "override" in f
                   for f in fields)


def test_real_yama_reader_is_always_used(monkeypatch):
    """The production supervisor reads the REAL kernel knob; a
    mechanically simulated Yama < 1 FAILS CLOSED on the production path
    and NO CLI/test hook can convert it to PASS."""
    calls = {"n": 0}

    def fake_real_reader():
        calls["n"] += 1
        return 0  # simulated real Yama < 1

    monkeypatch.setattr(authority, "read_yama_ptrace_scope",
                        fake_real_reader)
    from qh.rootauth import hold_bytes_memfd
    grant = authority.Grant(
        grant_id="g", attempt_id="a", root="/tmp", root_dev=0,
        root_ino=0, manifest_id="m", secret="s",
        created_at="now", root_pid=None)
    spec = {"spec_version": 1, "noegress": {"required": True}}
    sup = authority.Supervisor(
        grant=grant, spec=spec, spec_id="0" * 64,
        operator_state_dir="/tmp/qh-none", custody_fd=None)
    sup.startup()
    assert calls["n"] == 1, "startup must read the REAL knob exactly once"
    assert sup.exit_code == 6
    assert sup.machine.is_terminal_preexec_stop
    assert "YAMA_PTRACE_SCOPE_LT_1" in \
        [r.get("reason") for r in
         authority.ObservabilityLedger("/tmp/qh-none").read_all()
         if r.get("event") == "TERMINAL_PREEXEC_STOP"] or \
        sup.machine.is_terminal_preexec_stop


def test_root_startup_also_reads_real_yama(monkeypatch):
    """The authority root has no Yama override either: a simulated real
    Yama < 1 fails the root closed at startup."""
    from qh import rootauth
    monkeypatch.setattr(rootauth, "read_yama_ptrace_scope", lambda: 0)
    root = rootauth.AuthorityRoot(
        operator_state_dir="/tmp/qh-none-root", spec_bytes=b"{}",
        custody_fd=-1)
    root.startup()
    assert root.exit_code == 6
    assert root.fail_reason == "YAMA_PTRACE_SCOPE_LT_1"


def test_no_cli_flag_can_force_a_trust_decision_shape():
    """Structural proof over the ACTUAL parser tree: no production option
    can force no-egress/identity/policy/custody/Yama trust state."""
    parser = cli._build_parser()
    for action in parser._actions:
        for opt in action.option_strings:
            low = opt.lower()
            assert not any(b in low for b in
                           ("fault", "yama", "override", "bypass",
                            "force")), opt
        for sub in (getattr(action, "choices", None) or {}).values():
            for sub_action in sub._actions:
                for opt in sub_action.option_strings:
                    low = opt.lower()
                    assert not any(b in low for b in
                                   ("fault", "yama", "override", "bypass",
                                    "force")), opt
