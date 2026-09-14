#!/usr/bin/env python3
"""AUCDEV-010 R-B001..R-B004 bounded-remediation regressions (2026-09-14).

Every test names the source-supported qualification-blocking mechanism it
closes (B-001 completeness/skip-gating integrity, B-002 launch admission /
spawn / persistence serialization, B-003 content-aware write guard + Git
special-path correctness, B-004 canonical evidence enforcement). The
mechanism tests were demonstrated RED on the exact pre-fix product bytes
(skill tree ce06ef9f46d983548fba6ee960d4d202573feedd, unchanged at live
governance base b610595) BEFORE any product edit; the frozen RED output is
in the remediation handoff archive.

Zero model inference: every codex launch uses tests/fixtures/fake_codex.py.
All concurrency uses synchronization primitives (events / rendezvous
happens-before chains), never sleep-luck.

Successor correction (2026-09-14, R-B001 exact launch-transition binding):
the same-from/wrong-to tests in TestRB001SkipLaunchBinding were
demonstrated RED on the exact pre-fix product bytes of candidate
ecfece1830… (skill tree fb60425d…, unchanged at live governance base
b04aa60) BEFORE the state_store.py correction; the frozen RED output is
in the successor-correction handoff archive. The prior "misbound" test
covered a wrong from_phase only; the exact-to-phase binding
(R-B001_STAGE_LAUNCH_EXACT_TO_PHASE_BINDING_INCOMPLETE) needed its own
regressions.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL_DIR, "scripts")
SCHEMAS = os.path.join(SKILL_DIR, "schemas")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

import audit_council  # noqa: E402
import codex_runner  # noqa: E402
import repo_fingerprint  # noqa: E402
import state_store  # noqa: E402
import validate_artifact  # noqa: E402

from test_qx_stabilization import FAKE_CODEX, git, make_repo, make_run  # noqa: E402
import test_schema_validation as tsv  # noqa: E402

PYTHON = "python3"
AC = os.path.join(SCRIPTS, "audit_council.py")
RUNNER = os.path.join(SCRIPTS, "codex_runner.py")

RUNNER_ENV = dict(os.environ, AC_CODEX_BWRAP="0",
                  CODEX_RUNNER_POLL_INTERVAL="0.02",
                  AC_SANDBOX_DNS_PROBE_HOST="localhost")


def reap_launched_children():
    """In-process launches are supervised by codex_runner until their job
    reaches a terminal state; scenarios that never call `wait` must collect
    their (exited) children here so no supervised Popen is dropped without
    a recorded returncode (ResourceWarning hygiene)."""
    with codex_runner._PROC_MUTEX:
        entries = list(codex_runner._SUPERVISED_PROCS.items())
    for job_id, proc in entries:
        try:
            proc.wait(timeout=30)
        except Exception:  # noqa: BLE001 — best-effort test hygiene
            pass
        codex_runner._unsupervise(job_id)


# ---------------------------------------------------------------------------
# R-B001 helpers: truthful partial/full runs built through the PUBLIC
# state-store API only (no forged documents). Every skip record is bound to
# the exact transition that consumes it (the existing F-A-10 rules).
# ---------------------------------------------------------------------------
def _transitions(run_dir, targets, **kw):
    for target in targets:
        state_store.apply_transition(run_dir, target, **kw)


def run_at_finalized_skipping(tmp, repo, skipped_phase):
    """A truthful quota/failure-style partial run at FINALIZED where exactly
    one independent completion phase was explicitly skipped."""
    run_dir = make_run(tmp, repo, phase="CONTRACT_FROZEN")
    if skipped_phase == "OPUS_INDEPENDENT_COMPLETE":
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": skipped_phase,
             "reason": "opus independent pass unavailable (interruption)"}],
            from_phase="CONTRACT_FROZEN",
            to_phase="CODEX_INDEPENDENT_COMPLETE")
        _transitions(run_dir, ["CODEX_INDEPENDENT_COMPLETE", "NORMALIZED"])
    elif skipped_phase == "CODEX_INDEPENDENT_COMPLETE":
        _transitions(run_dir, ["OPUS_INDEPENDENT_COMPLETE"])
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": skipped_phase,
             "reason": "codex quota exhausted before the independent pass"}],
            from_phase="OPUS_INDEPENDENT_COMPLETE", to_phase="NORMALIZED")
        _transitions(run_dir, ["NORMALIZED"])
    else:
        raise ValueError(skipped_phase)
    _transitions(run_dir, ["OPUS_CROSS_EXAM_COMPLETE",
                           "CODEX_CROSS_EXAM_COMPLETE", "LEDGER_COMPLETE"])
    state_store.apply_transition(run_dir, "FINALIZED", adjudication_skipped=True)
    return run_dir


def run_at_finalized_full(tmp, repo, later_omission=None):
    """An honest full-protocol run at FINALIZED (both independent passes,
    both cross-exam passes, ledger; adjudication explicitly optional).
    `later_omission` may name ONE post-independent phase skipped under the
    documented quota path."""
    run_dir = make_run(tmp, repo, phase="CONTRACT_FROZEN")
    _transitions(run_dir, ["OPUS_INDEPENDENT_COMPLETE"])
    if later_omission == "CODEX_INDEPENDENT_COMPLETE":
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": later_omission,
             "reason": "codex quota exhausted before the independent pass"}],
            from_phase="OPUS_INDEPENDENT_COMPLETE", to_phase="NORMALIZED")
        _transitions(run_dir, ["NORMALIZED"])
    else:
        _transitions(run_dir, ["CODEX_INDEPENDENT_COMPLETE", "NORMALIZED"])
    if later_omission == "CODEX_CROSS_EXAM_COMPLETE":
        _transitions(run_dir, ["OPUS_CROSS_EXAM_COMPLETE"])
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": later_omission,
             "reason": "codex quota exhausted after the independent pass"}],
            from_phase="OPUS_CROSS_EXAM_COMPLETE",
            to_phase="LEDGER_COMPLETE")
        _transitions(run_dir, ["LEDGER_COMPLETE"])
    else:
        _transitions(run_dir, ["OPUS_CROSS_EXAM_COMPLETE",
                               "CODEX_CROSS_EXAM_COMPLETE",
                               "LEDGER_COMPLETE"])
    state_store.apply_transition(run_dir, "FINALIZED", adjudication_skipped=True)
    return run_dir


def ac_finalize(run_dir, completeness):
    return subprocess.run(
        [PYTHON, AC, "finalize", "--run", run_dir,
         "--completeness", completeness],
        capture_output=True, text=True, env=dict(os.environ), timeout=120)


# ===========================================================================
# R-B001 — completeness / mandatory-stage / skip-gating integrity
# ===========================================================================
class TestRB001CompletenessIntegrity(unittest.TestCase):
    """B-001: a run must never mechanically claim a completeness state
    stronger than the stages actually performed."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="rb001-",
                                    dir=os.path.join(HERE, "fixtures"))
        self._repo_n = 0

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _repo(self):
        self._repo_n += 1
        return make_repo(os.path.join(self.tmp, "repo-%d" % self._repo_n))

    def test_rb001_skipped_codex_independent_cannot_be_labeled_complete(self):
        run_dir = run_at_finalized_skipping(self.tmp, self._repo(),
                                            "CODEX_INDEPENDENT_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.set_completeness(run_dir, "COMPLETE")

    def test_rb001_skipped_codex_independent_cannot_be_labeled_cwru(self):
        run_dir = run_at_finalized_skipping(self.tmp, self._repo(),
                                            "CODEX_INDEPENDENT_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.set_completeness(
                run_dir, "COMPLETE_WITH_RESIDUAL_UNCERTAINTY")

    def test_rb001_skipped_opus_independent_cannot_be_labeled_cwru(self):
        run_dir = run_at_finalized_skipping(self.tmp, self._repo(),
                                            "OPUS_INDEPENDENT_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.set_completeness(
                run_dir, "COMPLETE_WITH_RESIDUAL_UNCERTAINTY")

    def test_rb001_finalize_refuses_complete_before_irreversible_close(self):
        run_dir = run_at_finalized_skipping(self.tmp, self._repo(),
                                            "CODEX_INDEPENDENT_COMPLETE")
        proc = ac_finalize(run_dir, "COMPLETE")
        self.assertNotEqual(proc.returncode, 0,
                            "finalize accepted COMPLETE with a skipped "
                            "mandatory independent pass")
        state = state_store.load_state(run_dir)
        self.assertEqual(state["phase"], "FINALIZED",
                         "the refusal must happen BEFORE the irreversible "
                         "transition to COMPLETE")
        self.assertNotEqual(state["completeness_state"], "COMPLETE")

    def test_rb001_finalize_cwru_refused_with_skipped_independent(self):
        run_dir = run_at_finalized_skipping(self.tmp, self._repo(),
                                            "CODEX_INDEPENDENT_COMPLETE")
        proc = ac_finalize(run_dir, "COMPLETE_WITH_RESIDUAL_UNCERTAINTY")
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(state_store.load_state(run_dir)["phase"],
                         "FINALIZED")

    def test_rb001_partial_quota_close_remains_truthful(self):
        run_dir = run_at_finalized_skipping(self.tmp, self._repo(),
                                            "CODEX_INDEPENDENT_COMPLETE")
        proc = ac_finalize(run_dir, "PARTIAL_CODEX_QUOTA")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        state = state_store.load_state(run_dir)
        self.assertEqual(state["phase"], "COMPLETE")
        self.assertEqual(state["completeness_state"], "PARTIAL_CODEX_QUOTA")

    def test_rb001_honest_full_run_still_finalizes_complete(self):
        run_dir = run_at_finalized_full(self.tmp, self._repo())
        proc = ac_finalize(run_dir, "COMPLETE")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        state = state_store.load_state(run_dir)
        self.assertEqual(state["completeness_state"], "COMPLETE")

    def test_rb001_cwru_with_documented_later_omission_still_allowed(self):
        # quota AFTER the independent pass is the documented residual path
        run_dir = run_at_finalized_full(self.tmp, self._repo(),
                                        later_omission="CODEX_CROSS_EXAM_COMPLETE")
        proc = ac_finalize(run_dir, "COMPLETE_WITH_RESIDUAL_UNCERTAINTY")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        state = state_store.load_state(run_dir)
        self.assertEqual(state["completeness_state"],
                         "COMPLETE_WITH_RESIDUAL_UNCERTAINTY")


class TestRB001SkipLaunchBinding(unittest.TestCase):
    """B-001: a skip record authorizes check_stage_launch only when bound
    to the exact transition context for the stage being launched — recorded
    from the CURRENT phase (from_phase == current) AND pointing at the
    EXACT phase that stage completes into (to_phase == stage completion;
    PHASE_CHAIN[PHASE_INDEX[STAGE_ENTRY_PHASE[stage]] + 1]). A record bound
    to ANY other to_phase — later, merely crossing the skipped phase, or
    unbound legacy — authorizes nothing: the launch gate must not borrow
    authority from a future transition recorded for another purpose."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="rb001b-",
                                    dir=os.path.join(HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.tmp, "repo"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_rb001_misbound_skip_cannot_authorize_stage_launch(self):
        # names the necessary phase, but is bound to a DIFFERENT transition
        # context (recorded from a phase that is not the current one)
        run_dir = make_run(self.tmp, self.repo, phase="CONTRACT_FROZEN")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "OPUS_INDEPENDENT_COMPLETE",
             "reason": "stale record from an aborted plan"}],
            from_phase="PREFLIGHT_COMPLETE",
            to_phase="CODEX_INDEPENDENT_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "independent")

    def test_rb001_unbound_skip_cannot_authorize_stage_launch(self):
        run_dir = make_run(self.tmp, self.repo, phase="CONTRACT_FROZEN")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "OPUS_INDEPENDENT_COMPLETE",
             "reason": "legacy record with no transition binding"}])
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "independent")

    def test_rb001_exactly_bound_skip_still_authorizes_stage_launch(self):
        run_dir = make_run(self.tmp, self.repo, phase="CONTRACT_FROZEN")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "OPUS_INDEPENDENT_COMPLETE",
             "reason": "opus pass unavailable; codex independent authorized"}],
            from_phase="CONTRACT_FROZEN",
            to_phase="CODEX_INDEPENDENT_COMPLETE")
        state = state_store.check_stage_launch(run_dir, "independent")
        self.assertEqual(state["phase"], "CONTRACT_FROZEN")

    # -- R-B001 successor: EXACT to-phase launch binding -------------------
    def test_rb001_same_from_wrong_to_finalized_cannot_authorize_launch(self):
        # same from_phase (the CURRENT phase), but the record is bound to
        # CONTRACT_FROZEN -> FINALIZED — a well-formed future transition
        # recorded for another purpose that merely CROSSES the skipped
        # phase. The exact independent-stage completion transition is
        # CONTRACT_FROZEN -> CODEX_INDEPENDENT_COMPLETE; a record bound to
        # any other to_phase must authorize nothing.
        run_dir = make_run(self.tmp, self.repo, phase="CONTRACT_FROZEN")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "OPUS_INDEPENDENT_COMPLETE",
             "reason": "future-jump record bound to a different purpose"}],
            from_phase="CONTRACT_FROZEN",
            to_phase="FINALIZED")
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "independent")

    def test_rb001_same_from_wrong_to_normalized_cannot_authorize_launch(self):
        # second same-from/wrong-to shape: another well-formed later
        # to_phase that crosses the skipped phase but is NOT the
        # independent-stage completion transition
        run_dir = make_run(self.tmp, self.repo, phase="CONTRACT_FROZEN")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "OPUS_INDEPENDENT_COMPLETE",
             "reason": "record bound to the normalization transition"}],
            from_phase="CONTRACT_FROZEN",
            to_phase="NORMALIZED")
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "independent")

    def test_rb001_consumed_exact_binding_cannot_authorize_launch(self):
        # the exact stage-completion binding, but already consumed by its
        # own transition — consumed records never re-authorize
        run_dir = make_run(self.tmp, self.repo, phase="CONTRACT_FROZEN")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "OPUS_INDEPENDENT_COMPLETE",
             "reason": "opus pass unavailable; codex independent authorized"}],
            from_phase="CONTRACT_FROZEN",
            to_phase="CODEX_INDEPENDENT_COMPLETE")
        state = state_store.load_state(run_dir)
        state["phase_skips"][0]["consumed"] = True
        state_store.save_state(run_dir, state)
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "independent")

    def test_rb001_at_entry_launch_needs_no_skip(self):
        # the ordinary at-entry launch stays admitted with no skip records
        run_dir = make_run(self.tmp, self.repo,
                           phase="OPUS_INDEPENDENT_COMPLETE")
        state = state_store.check_stage_launch(run_dir, "independent")
        self.assertEqual(state["phase"], "OPUS_INDEPENDENT_COMPLETE")

    def test_rb001_completed_stage_launch_still_refused(self):
        # once the state machine has reached the stage's completion phase,
        # the stage may not launch again
        run_dir = make_run(self.tmp, self.repo,
                           phase="CODEX_INDEPENDENT_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "independent")

    def test_rb001_cross_exam_exact_binding_early_launch_admitted(self):
        # analogous early-launch form for the other skip-gated model stage:
        # every passed artifact phase covered by an unconsumed skip bound
        # to the EXACT stage completion transition
        # CODEX_INDEPENDENT_COMPLETE -> CODEX_CROSS_EXAM_COMPLETE
        run_dir = make_run(self.tmp, self.repo,
                           phase="CODEX_INDEPENDENT_COMPLETE")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "NORMALIZED",
             "reason": "normalization covered elsewhere"},
            {"skipped_phase": "OPUS_CROSS_EXAM_COMPLETE",
             "reason": "opus cross-exam unavailable; codex cross authorized"}],
            from_phase="CODEX_INDEPENDENT_COMPLETE",
            to_phase="CODEX_CROSS_EXAM_COMPLETE")
        state = state_store.check_stage_launch(run_dir, "cross_examination")
        self.assertEqual(state["phase"], "CODEX_INDEPENDENT_COMPLETE")

    def test_rb001_cross_exam_same_from_wrong_to_refused(self):
        # both records same-from and crossing, but bound to FINALIZED —
        # borrowed future-transition authority, not the cross-examination
        # stage completion transition
        run_dir = make_run(self.tmp, self.repo,
                           phase="CODEX_INDEPENDENT_COMPLETE")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "NORMALIZED",
             "reason": "future-jump record bound to a different purpose"},
            {"skipped_phase": "OPUS_CROSS_EXAM_COMPLETE",
             "reason": "future-jump record bound to a different purpose"}],
            from_phase="CODEX_INDEPENDENT_COMPLETE",
            to_phase="FINALIZED")
        with self.assertRaises(state_store.StateError):
            state_store.check_stage_launch(run_dir, "cross_examination")


# ===========================================================================
# R-B002 — launch admission / spawn / persistence serialization
# ===========================================================================
class TestRB002LaunchTransaction(unittest.TestCase):
    """B-002: admission -> paid-process spawn -> authoritative job
    persistence is ONE serialized launch transaction per run+stage."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="rb002-",
                                    dir=os.path.join(HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.tmp, "repo"))
        self.run_dir = make_run(self.tmp, self.repo)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _start_args(self, run_dir=None, phase="independent"):
        return argparse.Namespace(run=run_dir or self.run_dir, phase=phase,
                                  prompt=None, session=None,
                                  codex_bin=FAKE_CODEX)

    # -- RED-B002 B: process-wide reentrancy registry ----------------------
    def test_rb002_run_state_lock_excludes_other_threads(self):
        a_inside = threading.Event()
        a_may_leave = threading.Event()
        b_entered = threading.Event()
        overlap = {}

        def holder_a():
            with state_store.run_state_lock(self.run_dir):
                a_inside.set()
                a_may_leave.wait(timeout=60)
                overlap["a_exited"] = True

        def contender_b():
            with state_store.run_state_lock(self.run_dir):
                # happens-before: this read runs only AFTER acquisition; the
                # broken registry fast path enters instantly while A still
                # holds (a_may_leave unset); a correct lock can only get
                # here after A released (a_may_leave set).
                overlap["b_entered_while_a_inside"] = not a_may_leave.is_set()
                b_entered.set()

        ta = threading.Thread(target=holder_a)
        ta.start()
        self.assertTrue(a_inside.wait(timeout=60), "holder A never entered")
        tb = threading.Thread(target=contender_b)
        tb.start()
        # Deterministic pre-fix (happens-before chain): B's registry fast
        # path enters, records the flag and fires b_entered while A still
        # holds. Post-fix B blocks on the flock, so this bounded wait is the
        # safety valve that releases A; B then records the flag after A.
        slipped_in = b_entered.wait(timeout=5)
        a_may_leave.set()
        ta.join(timeout=60)
        tb.join(timeout=60)
        self.assertFalse(ta.is_alive() or tb.is_alive())
        self.assertFalse(overlap.get("b_entered_while_a_inside", False),
                         "a second thread of the same process entered "
                         "run_state_lock while another thread held it "
                         "(slipped_in=%r)" % slipped_in)

    # -- RED-B002 A: duplicate concurrent launch / lost authoritative job --
    def test_rb002_concurrent_same_stage_starts_admit_exactly_one(self):
        spawn_count = {"n": 0}
        second_at_spawn = threading.Event()
        count_mutex = threading.Lock()
        real_launch = codex_runner.launch

        def counting_launch(*a, **k):
            with count_mutex:
                spawn_count["n"] += 1
                nth = spawn_count["n"]
            if nth == 1:
                # pre-fix rendezvous at the spawn point: hold the first
                # spawner until the second thread also reaches spawn — the
                # exact duplicate-launch window. Post-fix the second start
                # is refused under the serialization boundary BEFORE spawn,
                # so its refusal (below) fires this event instead; no
                # timing luck either way.
                second_at_spawn.wait(timeout=10)
            elif nth == 2:
                second_at_spawn.set()
            return real_launch(*a, **k)

        results = {}

        def run_start(name):
            rc = codex_runner.cmd_start(self._start_args())
            results[name] = rc
            if rc != 0:
                second_at_spawn.set()

        with mock.patch.dict(os.environ, RUNNER_ENV), \
                mock.patch.object(codex_runner, "launch", counting_launch), \
                contextlib.redirect_stdout(io.StringIO()):
            t1 = threading.Thread(target=run_start, args=("t1",))
            t2 = threading.Thread(target=run_start, args=("t2",))
            t1.start()
            t2.start()
            t1.join(timeout=120)
            t2.join(timeout=120)
        self.assertFalse(t1.is_alive() or t2.is_alive())

        state = state_store.load_state(self.run_dir)
        jobs = [j for j in state["codex"]["jobs"]
                if j.get("phase") == "independent"]
        job_files = [f for f in os.listdir(
            os.path.join(self.run_dir, "logs", "jobs"))
            if f.endswith(".json")]
        self.assertEqual(spawn_count["n"], 1,
                         "two concurrent starts for the same run+stage both "
                         "spawned a paid child")
        self.assertEqual(len(jobs), 1,
                         "authoritative state lost a launched job")
        self.assertEqual(len(job_files), 1)
        self.assertEqual(sorted(results.values()), [0, 3],
                         "exactly one admitted launch and one refusal; got "
                         "%r" % (results,))
        reap_launched_children()

    def test_rb002_active_attempt_blocks_second_start(self):
        with mock.patch.dict(os.environ, RUNNER_ENV), \
                contextlib.redirect_stdout(io.StringIO()):
            rc1 = codex_runner.cmd_start(self._start_args())
            self.assertEqual(rc1, 0)
            rc2 = codex_runner.cmd_start(self._start_args())
        self.assertNotEqual(rc2, 0,
                            "a second start while the first attempt is "
                            "active must be refused")
        state = state_store.load_state(self.run_dir)
        running = [j for j in state["codex"]["jobs"]
                   if j.get("phase") == "independent"
                   and j.get("status") in ("STARTING", "RUNNING")]
        self.assertEqual(len(running), 1)
        reap_launched_children()

    def test_rb002_successful_stage_remains_non_repeatable(self):
        # governor semantics unchanged: after a SUCCESSFUL stage, a repeat
        # start for the same phase is refused by the budget cap
        with mock.patch.dict(os.environ, RUNNER_ENV), \
                contextlib.redirect_stdout(io.StringIO()):
            rc1 = codex_runner.cmd_start(self._start_args())
            self.assertEqual(rc1, 0)
        self._wait_only_job()
        state = state_store.load_state(self.run_dir)
        state.setdefault("codex", {}).setdefault("stage_counts", {})
        state["codex"]["stage_counts"]["independent"] = 1
        state_store.save_state(self.run_dir, state)
        with mock.patch.dict(os.environ, RUNNER_ENV), \
                contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):
                # governor: a successfully completed stage never repeats
                codex_runner.cmd_start(self._start_args())
        reap_launched_children()

    def _wait_only_job(self):
        jobs_dir = os.path.join(self.run_dir, "logs", "jobs")
        records = sorted(f for f in os.listdir(jobs_dir)
                         if f.endswith(".json"))
        self.assertEqual(len(records), 1)
        return os.path.join(jobs_dir, records[0])

    def test_rb002_persistence_failure_terminates_spawned_child(self):
        def failing_save(run_dir, state):
            raise OSError("simulated authoritative persistence failure")

        with open(os.path.join(self.run_dir, "fake-codex-control"), "w") as fh:
            fh.write("MODE=slow\nSLEEP=30\n")
        outcome = {}

        def run_start():
            outcome["rc"] = codex_runner.cmd_start(self._start_args())

        with mock.patch.dict(os.environ, RUNNER_ENV), \
                mock.patch.object(codex_runner, "save_state", failing_save), \
                contextlib.redirect_stdout(io.StringIO()):
            t = threading.Thread(target=run_start)
            t.start()
            t.join(timeout=120)
        self.assertFalse(t.is_alive())

        self.assertNotEqual(outcome.get("rc", 1), 0,
                            "cmd_start must fail closed when authoritative "
                            "persistence fails after spawn")
        job_path = self._wait_only_job()
        with open(job_path) as fh:
            job = json.load(fh)
        self.assertEqual(job.get("status"), "ABORTED_PERSISTENCE_FAILURE",
                         "diagnostic job record not preserved fail-closed: "
                         "%r" % job.get("status"))
        self.assertIn("persistence_failure", job)
        # the paid child must not keep running untracked: bounded poll for
        # process exit (deterministic post-fix — the child is killed)
        pid = job["pid"]
        reaped = (0, 0)
        for _ in range(60):  # <= 15s deadline
            try:
                reaped = os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                reaped = (pid, 0)  # already collected elsewhere
                break
            if reaped[0]:
                break
            time.sleep(0.25)
        self.assertNotEqual(reaped[0], 0,
                            "spawned child still running after persistence "
                            "failure (untracked paid work)")
        # authoritative state must not claim a job it could not persist
        state = state_store.load_state(self.run_dir)
        self.assertEqual(
            [j for j in state["codex"]["jobs"]
             if j.get("phase") == "independent"], [])
        reap_launched_children()


# ===========================================================================
# R-B002 — concurrency stress (zero inference; exact counts in evidence)
# ===========================================================================
class TestRB002Stress(unittest.TestCase):
    """Concurrency stress: repeated paired concurrent same-stage starts,
    thread-lock mutual exclusion, and terminal-quota retry."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="rb002s-",
                                    dir=os.path.join(HERE, "fixtures"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_rb002_stress_concurrent_same_stage_starts(self):
        """25 iterations x 2 paired concurrent starts on a fresh run each.
        The post-fix outcome is deterministic regardless of interleaving:
        exactly ONE active launch per run+stage, no lost authoritative job."""
        iterations = 25
        real_launch = codex_runner.launch
        totals = {"spawned": 0, "admitted": 0, "refused": 0}
        violations = []

        for i in range(iterations):
            repo = make_repo(os.path.join(self.tmp, "repo-%02d" % i))
            run_dir = make_run(self.tmp, repo)
            spawn = {"n": 0}
            mutex = threading.Lock()

            def counting_launch(*a, **k):
                with mutex:
                    spawn["n"] += 1
                return real_launch(*a, **k)

            results = {}

            def run_start(name):
                rc = codex_runner.cmd_start(argparse.Namespace(
                    run=run_dir, phase="independent", prompt=None,
                    session=None, codex_bin=FAKE_CODEX))
                results[name] = rc

            with mock.patch.dict(os.environ, RUNNER_ENV), \
                    mock.patch.object(codex_runner, "launch",
                                      counting_launch), \
                    contextlib.redirect_stdout(io.StringIO()):
                ts = [threading.Thread(target=run_start, args=(n,))
                      for n in ("a", "b")]
                for t in ts:
                    t.start()
                for t in ts:
                    t.join(timeout=120)
            state = state_store.load_state(run_dir)
            jobs = [j for j in state["codex"]["jobs"]
                    if j.get("phase") == "independent"]
            job_files = [f for f in os.listdir(
                os.path.join(run_dir, "logs", "jobs"))
                if f.endswith(".json")]
            if spawn["n"] != 1:
                violations.append((i, "spawns", spawn["n"]))
            if len(jobs) != 1:
                violations.append((i, "authoritative jobs", len(jobs)))
            if len(job_files) != 1:
                violations.append((i, "job records", len(job_files)))
            if sorted(results.values()) != [0, 3]:
                violations.append((i, "return codes", dict(results)))
            totals["spawned"] += spawn["n"]
            totals["admitted"] += sum(1 for v in results.values() if v == 0)
            totals["refused"] += sum(1 for v in results.values() if v == 3)
        self.assertEqual(violations, [],
                         "race regressions over %d paired starts: %r"
                         % (iterations, violations))
        self.assertEqual(totals, {"spawned": iterations,
                                  "admitted": iterations,
                                  "refused": iterations})
        reap_launched_children()

    def test_rb002_stress_run_state_lock_mutual_exclusion(self):
        """8 threads x 25 in-lock read-modify-write bumps = 200 counted
        (pre-fix: the registry fast path loses updates)."""
        repo = make_repo(os.path.join(self.tmp, "repo"))
        run_dir = make_run(self.tmp, repo)
        threads = 8
        per_thread = 25

        def bump():
            for _ in range(per_thread):
                state_store.bump_phase_attempt(run_dir, "P")

        ts = [threading.Thread(target=bump) for _ in range(threads)]
        for t in ts:
            t.start()
        for t in ts:
            t.join(timeout=120)
        state = state_store.load_state(run_dir)
        self.assertEqual(state["phase_attempts"]["P"],
                         threads * per_thread,
                         "lost updates under same-process concurrent "
                         "run-state writers")

    def test_rb002_terminal_quota_attempt_permits_bounded_retry(self):
        repo = make_repo(os.path.join(self.tmp, "repo"))
        run_dir = make_run(self.tmp, repo)
        # match the fake codex's claimed fingerprint so COMPLETE output
        # passes the frozen-fingerprint identity invariant
        state = state_store.load_state(run_dir)
        state["repo_fingerprint_sha256"] = "deadbeefdeadbeef"
        state_store.save_state(run_dir, state)

        def cli(*args, mode):
            env = dict(RUNNER_ENV)
            env["FAKE_CODEX_MODE"] = mode
            if args and args[0] == "start":
                # write the control ONLY for launch commands — rewriting it
                # before a wait could race the already-started fake process
                with open(os.path.join(run_dir, "fake-codex-control"),
                          "w") as fh:
                    fh.write("MODE=%s\n" % mode)
            return subprocess.run(
                [PYTHON, RUNNER] + list(args),
                capture_output=True, text=True, env=env, timeout=120)

        p1 = cli("start", "--run", run_dir, "--phase", "independent",
                 "--codex-bin", FAKE_CODEX, mode="quota")
        self.assertEqual(p1.returncode, 0, p1.stderr)
        job1 = p1.stdout.strip()
        w1 = cli("wait", job1, "--timeout", "30", mode="quota")
        self.assertEqual(w1.returncode, 2, w1.stdout + w1.stderr)  # QUOTA
        # a TERMINAL quota attempt is not active: retry within budget
        p2 = cli("start", "--run", run_dir, "--phase", "independent",
                 "--codex-bin", FAKE_CODEX, mode="ok")
        self.assertEqual(p2.returncode, 0, p2.stderr)
        job2 = p2.stdout.strip()
        w2 = cli("wait", job2, "--timeout", "30", mode="ok")
        self.assertEqual(w2.returncode, 0, w2.stdout + w2.stderr)
        state = state_store.load_state(run_dir)
        jobs = [j for j in state["codex"]["jobs"]
                if j.get("phase") == "independent"]
        self.assertEqual(len(jobs), 2)
        statuses = sorted(j["status"] for j in jobs)
        self.assertEqual(statuses, ["COMPLETE", "QUOTA"])
        with open(os.path.join(run_dir, "logs", "jobs",
                               os.path.basename(job2))) as fh:
            second = json.load(fh)
        self.assertEqual(second["attempt_number"], 2)


# ===========================================================================
# R-B003 — content-aware write guard + Git special-path correctness
# ===========================================================================
SPECIAL_NAMES = [
    'quo"te.txt',        # embedded double-quote (C-quoted by git)
    'back\\slash.txt',   # embedded backslash
    'tab\tfile.txt',     # embedded tab
    'ünïcode-ß.txt',     # non-ASCII (core.quotePath default)
]


class TestRB003WriteGuard(unittest.TestCase):
    """B-003: every byte change represented by fingerprint v2 must be
    visible to the write guard, and Git C-quoted special filenames must be
    parsed path-correctly everywhere."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="rb003-",
                                    dir=os.path.join(HERE, "fixtures"))
        self.repo = make_repo(os.path.join(self.tmp, "repo"))
        self.run_dir = os.path.join(self.repo, "audit-output",
                                    "audit-council",
                                    "20260914T000000Z-rb0003")
        os.makedirs(self.run_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _baseline(self):
        return repo_fingerprint.capture(self.repo)

    def _guard(self, baseline):
        state_store.atomic_write_json(
            os.path.join(self.run_dir, state_store.REPO_STATE_NAME),
            {"repo_root": self.repo, "fingerprint": baseline})
        proc = subprocess.run([PYTHON, AC, "write-guard", "--run",
                               self.run_dir],
                              capture_output=True, text=True,
                              env=dict(os.environ), timeout=120)
        # parse the JSON verdict: special filenames are JSON-escaped in the
        # serialized output, so assertions compare PARSED violation paths
        proc.violation_paths = None
        if proc.stdout.strip().startswith("{"):
            try:
                doc = json.loads(proc.stdout)
                proc.violation_paths = sorted(
                    v.get("path", "") for v in doc.get("violations", []))
            except ValueError:
                pass
        return proc

    def test_rb003_changed_untracked_bytes_visible_to_write_guard(self):
        path = os.path.join(self.repo, "notes.txt")
        with open(path, "wb") as fh:
            fh.write(b"AAAAAAAAAA")
        baseline = self._baseline()
        with open(path, "wb") as fh:
            fh.write(b"BBBBBBBBBB")  # same size, different bytes
        proc = self._guard(baseline)
        self.assertEqual(proc.returncode, 5,
                         "same-size untracked byte change invisible to the "
                         "write guard: %s" % proc.stdout)
        self.assertIn("notes.txt", proc.stdout)

    def test_rb003_changed_dirty_worktree_bytes_visible_to_write_guard(self):
        path = os.path.join(self.repo, "a.py")
        with open(path, "a") as fh:
            fh.write("y = 2\n")  # now dirty, recorded in baseline
        baseline = self._baseline()
        self.assertIn("a.py", baseline["dirty_worktree"])
        with open(path, "a") as fh:
            fh.write("z = 3\n")  # further byte change, still just as dirty
        proc = self._guard(baseline)
        self.assertEqual(proc.returncode, 5,
                         "dirty-worktree byte change invisible to the write "
                         "guard: %s" % proc.stdout)
        self.assertIn("a.py", proc.stdout)

    def test_rb003_special_git_filenames_fingerprinted_and_guarded(self):
        for name in SPECIAL_NAMES:
            with open(os.path.join(self.repo, name), "wb") as fh:
                fh.write(b"one")
        baseline = self._baseline()
        for name in SPECIAL_NAMES:
            self.assertIn(name, baseline["untracked_inventory"],
                          "special Git filename %r disappeared from the "
                          "untracked inventory" % name)
            entry = baseline["untracked_inventory"][name]
            self.assertEqual(entry.get("kind"), "file")
            self.assertIsNotNone(entry.get("sha256"))
        for name in SPECIAL_NAMES:
            with open(os.path.join(self.repo, name), "wb") as fh:
                fh.write(b"two")  # same-size byte change
        fresh = repo_fingerprint.capture(self.repo)
        diff = repo_fingerprint.diff_fingerprints(baseline, fresh)
        self.assertTrue(diff["changed"],
                        "special-filename byte change evaded the fingerprint")
        for name in SPECIAL_NAMES:
            self.assertIn(name, diff["changed_untracked"])
        proc = self._guard(baseline)
        self.assertEqual(proc.returncode, 5,
                         "special-filename byte change invisible to the "
                         "write guard: %s" % proc.stdout)
        for name in SPECIAL_NAMES:
            self.assertIn(name, proc.violation_paths or [])

    def test_rb003_dirty_tracked_special_name_visible_to_write_guard(self):
        special = 'spec"ial.py'
        with open(os.path.join(self.repo, special), "w") as fh:
            fh.write("x = 1\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "special")
        with open(os.path.join(self.repo, special), "a") as fh:
            fh.write("y = 2\n")  # dirty at baseline
        baseline = self._baseline()
        self.assertIn(special, baseline["dirty_worktree"],
                      "dirty tracked special filename missing from the "
                      "dirty-worktree inventory")
        with open(os.path.join(self.repo, special), "a") as fh:
            fh.write("z = 3\n")  # further dirty byte change
        proc = self._guard(baseline)
        self.assertEqual(proc.returncode, 5,
                         "dirty tracked special-filename byte change "
                         "invisible to the write guard: %s" % proc.stdout)
        self.assertIn(special, proc.violation_paths or [])

    def test_rb003_clean_tree_still_verifies_clean(self):
        proc = self._guard(self._baseline())
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_rb003_tracked_add_still_a_violation(self):
        baseline = self._baseline()
        with open(os.path.join(self.repo, "new.py"), "w") as fh:
            fh.write("n = 1\n")
        git(self.repo, "add", "new.py")
        proc = self._guard(baseline)
        self.assertEqual(proc.returncode, 5)
        self.assertIn("new.py", proc.stdout)

    def test_rb003_untracked_add_remove_still_violations(self):
        path = os.path.join(self.repo, "gone.txt")
        with open(path, "wb") as fh:
            fh.write(b"x")
        baseline = self._baseline()
        os.remove(path)
        proc = self._guard(baseline)
        self.assertEqual(proc.returncode, 5)
        self.assertIn("gone.txt", proc.stdout)


# ===========================================================================
# R-B004 — canonical evidence enforcement
# ===========================================================================
class TestRB004CanonicalEvidence(unittest.TestCase):
    """B-004: a canonical finding cannot be accepted with zero evidence
    items or wholly untyped evidence items, on every affected schema
    surface (finding, final-findings, and the $ref-inheriting
    independent-audit and cross-examination schemas)."""

    @staticmethod
    def _errors(schema_name, doc):
        return validate_artifact.validate(
            doc, tsv.load_schema(schema_name), base_dir=Path(SCHEMAS))

    def _surfaces(self, evidence):
        """(schema, doc) pairs for every canonical schema surface that
        carries finding-shaped evidence."""
        finding_doc = tsv.finding(evidence=evidence)
        final = tsv.final_findings()
        final["findings"][0]["evidence"] = evidence
        cross = tsv.cross_examination()
        cross["late_findings"][0]["evidence"] = evidence
        return (
            ("finding.schema.json", finding_doc),
            ("final-findings.schema.json", final),
            ("independent-audit.schema.json",
             tsv.independent_audit(findings=[finding_doc])),
            ("cross-examination.schema.json", cross),
        )

    def test_rb004_empty_evidence_rejected(self):
        for schema_name, doc in self._surfaces([]):
            errors = self._errors(schema_name, doc)
            self.assertTrue(errors,
                            "%s accepted evidence=[]" % schema_name)

    def test_rb004_untyped_evidence_item_rejected(self):
        for schema_name, doc in self._surfaces([{}]):
            errors = self._errors(schema_name, doc)
            self.assertTrue(errors,
                            "%s accepted evidence=[{}]" % schema_name)

    def test_rb004_valid_typed_evidence_still_accepted(self):
        for schema_name, doc in self._surfaces(
                [{"kind": "OBSERVED_FACT", "path": "src/app.py"}]):
            errors = self._errors(schema_name, doc)
            self.assertEqual(errors, [],
                             "%s rejected valid typed evidence: %r"
                             % (schema_name, errors))


if __name__ == "__main__":
    unittest.main()
