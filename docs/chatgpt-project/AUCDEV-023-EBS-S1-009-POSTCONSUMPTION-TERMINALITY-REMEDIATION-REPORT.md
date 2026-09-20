# AUCDEV-023 EBS S1-009 Post-Consumption Fail-Closed Terminality Remediation Report (2026-09-20)

Implementer-strength record ONLY. NOT the Control Room, NOT an
independent auditor, NOT a closure of any finding, NOT event readiness,
NOT execution authority, NOT qualification, NOT installation.

## 1. Authority and non-authorities

Authority: the operator's explicit narrow bounded remediation mandate
for exactly ONE finding — AUCDEV023-CR-EBS-S1-009
(POST_CONSUMPTION_EXCEPTION_TERMINALIZATION_CAN_ESCAPE_PROCESS_BOUND_
CLEANUP) — plus deterministic zero-provider tests, package regeneration
necessitated by changed EBS bytes, and the required implementation/
canonical records. The selected implementer (Claude Code + GLM-5.3) is
IMPLEMENTER ONLY and is NOT: the Audit Council Dev Control Room; an
independent auditor; authorized to close the Control Room finding;
authorized to prepare the real AUCDEV-023 event package; authorized to
instantiate an event; authorized to run GATE-W′; authorized to invoke
Claude/Opus, GPT/Codex, `/audit-council`, or any provider/model;
authorized to inspect or use real provider credentials; authorized to
qualify or install anything. THIS TASK DID NOT PERFORM S1. The existing
S1 event-package-preparation authorization remains AUTHORIZED_BY_
OPERATOR / NOT_STARTED / PAUSED / NOT_CONSUMED.

## 2. Exact base identity (verified before any mutation)

- live GitHub default-branch master resolved EXACTLY to
  `76e6012d2753af94215670ce87abd35d43d9f57b` (tree
  `d38da71979e8cba278e035730d135520b3f1d10a`; sole parent
  `0f79d3bd817eba9aceb2d89142f1bee509139ec2`) — local HEAD identical,
  0 ahead / 0 behind;
- bootstrap-supervisor subtree `65f6f296b4a670a6e566e092974b1ccedf4b0562`;
- qualification-harness tree `5b8d5e5465923740470ff63ed9b8683f257a3787`;
- skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`;
- current EBS package going in: manifest_sha256
  `8ccb450c3e0b64fdebb7ff8ba8f77408d0dfb3bc010079d6e02431ac49fe8fb7`,
  package_sha256
  `6c39d889733ce02c5a4089933276a6b7dc13252485e783a020646b43da6d32fc`,
  30 rows; accepted production LOC 2800
  (ACCEPTED_RESIDUAL_AT_CURRENT_IMPLEMENTATION_READBACK_STRENGTH /
  NONBLOCKING_IN_ITSELF / EXACT_SHA_0F79D3BD / NOT_STANDING_AUTHORITY).

## 3. Exact source defect (as recorded by the Control Room readback)

`_fork_and_launch()` durably appends and transitions to EXEC_ATTEMPTED
before its bounded parent wait lifecycle; its BaseException handler
closes child pipe fds and kills/reaps the direct child but calls
`_terminalize_after_consumption` ONLY when
`self._machine.state == CONSUMED_PRE_EXEC`, so parent-side exceptions
AFTER the EXEC_ATTEMPTED transition (os.set_blocking / non-BlockingIOError
os.read / waitpid(WNOHANG) / unexpected wait-loop failures) skip
terminalization while in-process state may remain EXEC_ATTEMPTED, the
Supervisor-held CredentialCustody may remain open, held
launcher/auditor/invocation/validator/output-directory fds may remain
open, and no process-bound TERMINAL settlement is guaranteed before
control escapes. Second gap: the explicit timeout path performs
store.append(TERMINAL) → machine.transition(TERMINAL) → close custody →
close held fds WITHOUT a fail-closed finally/fallback wrapper, so a
TERMINAL append/transition failure can skip cleanup and the public
attempt call can escape with the consumed attempt still holding
custody/fds. Anchors at the exact base: launch.py:1192-1194, 1275-1276
(handler at 1259), 1198/1199 + 1209/1230 + 1220/1238, 1297-1306,
1354.

## 4. RED evidence on the exact base (before ANY production edit)

Isolated detached worktree `/tmp/aucdev-s1009-red` at EXACT base
`76e6012d…`; production bytes byte-identical to the base (the worktree
MANIFEST.json was regenerated metadata-only — rows 30 → 31 for the new
untracked test file — because the EBS fail-closed self-identity walk
refuses unmanifested files; implementation_base_commit/status/task
fields byte-unchanged; worktree manifest_sha256
`edeeab9e24353d7902659bcfd0c3243e4ab50b9c974a04ff59e16c3f37a71ce4`,
package_sha256
`a65d2d022950387d2a83fc0c3c7f00b6ddc5b134c190beb65c9dbda0d8705249`).
Evidence preserved in `aucdev023-s1-009-evidence/red/`.

RESULT: 9 failed / 3 passed (exit 1). Deterministic one-shot fault
injections (raising an exact OSError the FIRST time the guarded call
occurs with the machine in EXEC_ATTEMPTED / a post-consumption state;
every other call delegates to the real function):

- RED-009-A (os.set_blocking failure after EXEC_ATTEMPTED), RED-009-B
  (waitpid(WNOHANG) and non-BlockingIOError os.read failures after
  EXEC_ATTEMPTED, parametrized): observed base defect — the original
  OSError re-raised while in-process state remains EXEC_ATTEMPTED
  (assert `'EXEC_ATTEMPTED' == 'TERMINAL'` fails), Supervisor custody
  still open, held launcher/auditor/invocation/validator/output-dir fds
  still open, NO durable TERMINAL record;
- RED-009-C (timeout-path store.append(TERMINAL) failure): observed
  base defect — the raw OSError escapes the public call with NO
  settlement, state EXEC_ATTEMPTED, custody/fds held, no timed-out
  AttemptResult and no incompleteness classification;
- RED-009-D (timeout-path machine.transition(TERMINAL) failure after a
  successful TERMINAL append): observed base defect — the
  InvalidTransition escapes with cleanup skipped (custody/fds held);
- report-path TERMINAL append failure (after a successful REPORT_FROZEN
  append) and report-outcome-state (REPORT_MISSING) append failure:
  observed base defect — the accounting failure is silently swallowed
  by the generic report-lifecycle handler, the durable record is
  settled best-effort, and a NON-CONFORMING AttemptResult is returned
  quietly (DID NOT RAISE);
- original+accounting double failure: the raw original OSError escapes
  with no settlement and no recoverable accounting failure;
- StateMachine.fail_closed_terminal: absent on the base.

The 3 tests that pass on the base are regression guards over
already-correct base behavior (a CONSUMED_PRE_EXEC pre-fork failure,
the normal exec-failed consumed path, and preexec refusals staying
TERMINAL_PREEXEC_STOP) — correctly not RED.

## 5. After design — the ONE centralized settlement primitive

`Supervisor._settle_post_consumption(report_state, report_extra,
terminal_extra=None, original_error=None, related_error=None)` replaces
the duplicated semantics previously spread across
`_terminalize_after_consumption`, `_settle`, the timeout-path
terminalization, and the exceptional cleanup (all removed), with TWO
separated concepts:

- A. DURABLE ACCOUNTING ATTEMPT: the report-outcome record (when one
  applies) and then the TERMINAL record, each with its normal
  transition while the chain still advances; the FIRST durable failure
  stops further appends — the existing record is preserved exactly as
  it exists (nothing fabricated, rewritten, or truncated) and is NEVER
  treated as durable success;
- B. IN-PROCESS FAIL-CLOSED DEATH (a finally that can never raise):
  whether or not the durable accounting completed, the already-consumed
  attempt lands on TERMINAL via the narrow
  `StateMachine.fail_closed_terminal()` primitive (idempotent no-op
  when already TERMINAL) and `_close_authority_holds()` closes the
  Supervisor-held custody and EVERY held fd
  (launcher/auditor-executable/invocation/validator/output-directory).

Outcome semantics: a durable failure raises the exact
`PostConsumptionTerminalAccountingError`
(POSTCONSUMPTION_TERMINAL_ACCOUNTING_FAILED) chaining the original or
related failure; durable success re-raises `original_error` when one
exists (the parent-failure path); otherwise the caller returns through
only on a durably complete settlement.

## 6. State-machine fail-closed primitive (§7)

`StateMachine.fail_closed_terminal()`: callable ONLY from
CONSUMED_PRE_EXEC / EXEC_ATTEMPTED / REPORT_FROZEN / REPORT_MISSING /
REPORT_INVALID / REPORT_SCREEN_FAIL (idempotent no-op from TERMINAL);
moves ONLY to TERMINAL; REFUSES PREPARED, GATES_PASSED and
TERMINAL_PREEXEC_STOP with
`FAIL_CLOSED_TERMINAL_REFUSED_<STATE>`; creates NO general
force/reset/retry API; never makes TERMINAL leaveable; no resumable
state exists. launch.py never mutates `_state` directly — the invariant
is expressed ONLY through the explicit primitive. The settlement also
keeps the normal `transition(TERMINAL)` on the durable-success path
with the primitive as the guaranteed fallback when that transition
itself is unavailable (RED-009-D's GREEN counterpart proves the
fallback recovers: durable TERMINAL present, in-process TERMINAL,
custody/fds closed, normal timed-out AttemptResult returned).

## 7. Durable accounting-failure semantics (§8) and double failure (§9)

On any required post-consumption append failure: no missing durable
record is fabricated; the accounting file is never rewritten or
truncated; durable TERMINAL is never claimed; no normal success, no
`AttemptResult(timed_out=True)`, and no conforming REPORT_FROZEN result
is returned for a failed terminal chain — instead the existing record
is preserved exactly, in-process TERMINAL is established fail-closed,
custody and held fds close, retry remains impossible, and the exact
`POSTCONSUMPTION_TERMINAL_ACCOUNTING_FAILED` classification is raised.
When an original post-consumption failure and a terminal-accounting
failure BOTH occur, the raised error carries BOTH mechanically
recoverable — in the message (both reprs), as explicit attributes
(`original_error` / `related_error` / `accounting_error`), and on the
exception chain (`raise … from original`). No credential bytes or
sensitive content are ever logged; no silent exception replacement
occurs.

## 8. EXEC_ATTEMPTED parent-side exceptions (§10)

The `_fork_and_launch` BaseException handler now applies to EVERY
post-consumption state (the `state == CONSUMED_PRE_EXEC` condition is
REMOVED): remaining parent pipe fds close first (a metadata-blocked
child unblocks and dies), the EXACT attempt process group is killed
under the accepted S1-008 scoping discipline (pgid guard, fallback to
the direct child, never an unrelated process) and the direct child is
deterministically reaped, and ONLY THEN the centralized settlement runs
(durable `PARENT_FAILURE_AFTER_EXEC_ATTEMPTED` /
`PRE_EXEC_FAILURE_AFTER_CONSUMPTION` terminal reason; in-process
TERMINAL; custody + every held fd closed; second run_attempt refused);
the original failure re-raises when the durable settlement completed,
the combined incompleteness error when it did not. S1-008 process-group
design was NOT reopened.

## 9. Timeout path (§11)

Refactored onto the same primitive. The exact process group is killed
and the direct child reaped BEFORE the settlement; on durable success
the TIMEOUT_AFTER_CONSUMPTION semantics are byte-identical (same
terminal_reason/auditor_timeout_seconds/child_pid record, same
timed-out AttemptResult). On TERMINAL append failure: no report
accepted, authority/model engagement fail-closed consumed, in-process
TERMINAL, custody/fds closed, no retry, NO timed-out AttemptResult —
the exact incompleteness error is raised (RED-009-C/GREEN).

## 10. Report lifecycle settlement (§12)

REPORT_MISSING / REPORT_SCREEN_FAIL / REPORT_INVALID / REPORT_FROZEN
all settle through the same primitive: a report-state or TERMINAL
append failure leaves NO caller-visible nonterminal operational state
(in-process TERMINAL, custody/fds closed, no retry) with the durable
incompleteness surfaced honestly by exception. If report bytes were
already frozen before the accounting fails, the artifact REMAINS
operator-custodied evidence (never deleted to fake atomicity) and is
NEVER represented as a conforming/complete first pass by the returned
API (no AttemptResult is returned at all — the incompleteness error
raises). The ReportRefused and unexpected report-lifecycle handlers
pass the concurrent failure as `related_error` so an accounting failure
of their own settlement chains it; preexec semantics are untouched
(§13): TERMINAL_PREEXEC_STOP stays distinct, the fail-closed primitive
refuses every non-post-consumption source state, and PREPARED/
GATES_PASSED failures remain authority-unconsumed (proven by the
preexec regression test).

## 11. Custody/fd closure, kill/reap, and retry-refusal proofs

The focused suite asserts, per injected fault: exact resulting
in-process state; exact durable last state actually present; custody
closure (the sealed custody fd is closed); closure of ALL five held fds
(launcher, auditor executable, invocation spec, validator,
output-custody directory); the attempt child pid (from the durable
EXEC_ATTEMPTED record) gone with no zombie; the hanging-launcher tree
(launcher pid + descendant pid) dead after the timeout-path failures;
second `run_attempt` refused (`RUN_ATTEMPT_REFUSED…`); and the exact
returned-vs-raised outcome. TERMINAL remains absorbing (transition out
of TERMINAL refused) and no reset/retry/resume surface exists on the
StateMachine.

## 12. Unchanged V5 contract (§5)

No schema change: `AUCDEV-023-EVENT-PACKAGE-MANIFEST-V5` retained;
V1-V4 still refused (138/138 binding + 94/94 event-package tests
green). binding.py, reportcustody.py, accounting.py, custody.py and
cli.py are BYTE-UNCHANGED; output_validator semantics,
execution_limits semantics, auditor invocation binding, executable
identity binding, the public run_attempt input surface (exact
parameter set statically tested), the report snapshot contract and the
GATE-W′ contract are untouched.

## 13. Production change surface (§20) and file-level justification

Changed production files (exactly two, as strongly expected, plus
package metadata):

- `ebs/launch.py` (1500 → 1573): the centralized primitive
  `_settle_post_consumption` +48 NEW; exact classification
  `PostConsumptionTerminalAccountingError` +18 NEW (class + __init__);
  `_close_authority_holds` +23 NEW merged custody+held-fd closure
  (absorbing `_close_custody` -5 and `_close_held_fds` -15, each close
  failure-absorbing so the guaranteed path can never raise);
  `_close_fds` +10 NEW shared fd-closer reused by the gate/validator
  runner and the attempt-pipe cleanup (-10 across `_run_runtime_gate`
  and `_fork_and_launch`); `_report_and_terminalize` +10 (settlement
  routing, the incompleteness re-raise clause, the §12 frozen-artifact
  comment); `_fork_and_launch` -3 and `_preexec_stop` -1 (consolidated
  closure + the removed CONSUMED_PRE_EXEC-only condition replaced by
  the unconditional centralized settlement); module docstring +10
  (S1-009 paragraph). REMOVED: `_settle` -15 and
  `_terminalize_after_consumption` -12.
- `ebs/statemachine.py` (77 → 102): `fail_closed_terminal` +18 NEW and
  `POST_CONSUMPTION_STATES` +6 (the §7 primitive).
- `ebs/__init__.py` (38 → 44): VERSION
  `0.8.0-s1-009-postconsumption-terminality-candidate` + a bounded
  docstring sentence — package metadata/documentation mechanically
  required by the standard every prior candidate followed.
- `MANIFEST.json` (regenerated: 30 → 31 rows for the NEW focused test
  file; implementation_base_commit `76e6012d…`; status
  S1_009_POSTCONSUMPTION_TERMINALITY_REMEDIATION_CANDIDATE /
  AWAITING_FRESH_CONTROL_ROOM_READBACK; task names the S1-009
  authority) and `README.md` (title/authority/status + the centralized
  settlement section + the stale `adopt_report` parenthetical
  corrected): mechanically expected package metadata/documentation.
- Tests: NEW `tests/test_s1_009_postconsumption_terminality.py` (the
  RED→GREEN fault-injection suite);
  `tests/test_final_execution_lifecycle.py` (the AST terminality-shape
  test re-pointed from `_settle` to `_settle_post_consumption` and
  STRENGTHENED to statically verify the guaranteed fail-closed finally:
  `fail_closed_terminal` + `_close_authority_holds` inside a finalbody);
  `tests/test_static.py` (the S1-009 LOC disclosure comment + the
  candidate-only ceiling; all prior accepted baselines preserved
  verbatim).

## 14. TCB / LOC discipline (§19)

Production LOC 2800 → 2904 (+104), recounted by two consistent methods
(`wc -l` sum and `splitlines()` sum over `ebs/*.py`), classified
NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE / CANDIDATE_ONLY with
the exact per-function attribution in §13. The strong ≤2800 target was
NOT met: the growth buys three genuinely new authority guarantees that
did not exist at the accepted base — (1) honest durable
accounting-failure semantics (exact incompleteness classification,
original-failure chaining, never a success/timed-out/conforming result
over a failed terminal chain); (2) the guaranteed in-process fail-closed
death (TERMINAL + custody + all five held fds closed on EVERY
post-consumption path, incl. injected post-EXEC_ATTEMPTED
set_blocking/read/waitpid failures and timeout/report
TERMINAL-append/transition failures); (3) the narrow state-machine
primitive making the invariant explicit — while the consolidation
genuinely REMOVED the duplicated `_settle`/`_terminalize_after_
consumption` paths (-27) and merged the closure helpers; deeper cuts
would strip either the new guarantees themselves or the documentation
standard every prior candidate was held to, both forbidden. 2800
remains the last Control-Room-accepted residual; this ceiling
(2904) is CANDIDATE_ONLY / NOT_CONTROL_ROOM_ACCEPTED and is NOT
standing authority for any future growth.

## 15. Exact test environment (§21)

Host CPython 3.14.7 + pytest 9.1.1 in the isolated venv
`/tmp/aucdev-venv` (single final validation campaign; the historical
`/mnt/archlinux` JSON C-recursion fault was not re-tested and is
treated as a historical diagnostic only — no production change was
made to accommodate it; actual event-runtime compatibility remains an
S1 evidence obligation).

## 16. Validation results (§23, all first-attempt)

- exact-base RED suite: 9 failed / 3 passed (defect demonstrated);
- `compileall` exit 0;
- focused S1-009 GREEN suite: 12/12;
- S1-007 lifecycle suite: 31/31 (incl. the strengthened AST shape
  test); S1-008 timeout/process-group: included (hanging tree killed
  by the EBS, descendant dead, unrelated process survives,
  TIMEOUT_AFTER_CONSUMPTION accounting);
- validator tests (binding-side validator descriptors within 138/138;
  validator-timeout within the lifecycle suite); snapshot/TOCTOU 11/11;
- V5 binding 138/138; V5 event-package cross-binding 94/94;
- S1-004/-005/-006 (final launch seam) 31/31; S1-001 27/27;
  S1-002+S1-003 36/36; CR-EBS-001/-002 (test_launch) 18/18;
  CR-EBS-003 selfcheck 17/17; REM-001/REM2-001 (within
  binding/eventpackage suites) green;
- FULL bootstrap-supervisor deterministic battery: 489/489 (base 477 +
  12 NEW);
- qualification-harness regression: 221/221, qh source BYTE-UNCHANGED
  (tree `5b8d5e5465923740470ff63ed9b8683f257a3787`);
- `git diff --check` CLEAN;
- production LOC recount by two consistent methods: 2904 = 2904;
- stdlib-only import scan: no non-stdlib/non-internal import anywhere
  in `ebs/*.py`;
- provider/network surface scan: only the frozen binding.py policy
  tokens and pre-existing negation comments ("No subprocess, no
  networking", "No bearer token exists", the frozen repository slug);
  zero socket/ssl/urllib/requests/subprocess/http imports anywhere
  under bootstrap-supervisor;
- forbidden qh/skill reach scan: zero production references (the only
  `qualification-harness` strings are pre-existing negation comments
  and the FORBIDDEN_TOKENS policy constant in tests);
- credential/private-key scan of production + fixtures: zero (single
  pre-existing negation-comment hit);
- MANIFEST verification: NO_DRIFT over all 31 rows, non-circular
  package identity MATCH, live-tree payload-set equality;
- final package identities: manifest_sha256
  `68490d796b66d8e7598a38a8f28cc4546e27be1bd75b637463b69677ffcdaf72`,
  package_sha256
  `8685c36e8286acb4e7fdc59bd68c92aa7ec96d27d3623a19d0f975e67d73c0d8`,
  31 rows, implementation_base_commit
  `76e6012d2753af94215670ce87abd35d43d9f57b` (the OLD accepted
  identities `8ccb450c…`/`6c39d889…` are recorded here; NO acceptance
  transfers to the regenerated package);
- protected-tree identity: qualification-harness and skill trees
  unchanged from the base (verified again at the pre-commit gate);
- zero-provider/zero-network proof: every executed fixture imports
  only `hashlib/json/os/sys/time`; every inert fixture carries
  EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER; the inert
  auditor executable is NEVER executed;
- no real event package, no canonical event id (BOOTSTRAP_EVENT
  NOT_INSTANTIATED; only long-standing synthetic fixture ids).

## 17. Zero-real-execution boundary (§22)

actual network = ZERO; provider calls = ZERO; model calls = ZERO;
auditor executions = ZERO; real credentials = ZERO (the only credential
bytes anywhere are the SYNTHETIC INERT `SYNTH_CRED` fixture); real
event package NOT PREPARED; canonical event id NOT INSTANTIATED;
GATE-W′ NOT RUN; qualification NONE; installation NONE.
NORMAL_EXIT_BOUNDARY_PROCESS_TREE_QUIESCENCE remains
NOT_YET_PROVEN / S1_EVENT_PREPARATION_EVIDENCE_REQUIREMENT and was
deliberately NOT attempted here (§18: no real boundary launcher exists;
S1-009 was not broadened into that evidence obligation).

## 18. Implementer position (§24)

- AUCDEV023-CR-EBS-S1-009 = REMEDIATION_IMPLEMENTED /
  AWAITING_CONTROL_ROOM_READBACK (implementer position ONLY — NOT a
  closure).
- S1-007, S1-008 and ALL prior closed findings (CR-EBS-001/-002/-003,
  REM-001, REM2-001, S1-001..S1-006) = PRIOR_CONTROL_ROOM_CLOSURE /
  REGRESSION_EVIDENCE_HELD / NEW_SHA_AWAITING_FRESH_CONTROL_ROOM_
  READBACK (fresh regression evidence held at implementer strength;
  NOT closed, NOT Control-Room-accepted, no self-audit).
- NO backlog item becomes DONE; AUCDEV-023 remains P1 / READY /
  NOT DONE.
- Resulting implementer-strength state: EBS_IMPLEMENTATION =
  S1_009_POSTCONSUMPTION_TERMINALITY_REMEDIATION_CANDIDATE /
  AWAITING_FRESH_CONTROL_ROOM_READBACK; EVENT_PACKAGE_PREPARATION =
  AUTHORIZED_BY_OPERATOR / NOT_STARTED / PAUSED_PENDING_S1_009_
  REMEDIATION_READBACK (preserved, paused, unconsumed); BOOTSTRAP_EVENT
  = NOT_INSTANTIATED; GATE_W_PRIME = REQUIRED / UNPROVEN;
  REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION = UNPROVEN /
  EVENT_PREPARATION_GATE; MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY =
  0; qualification NONE; installation NONE.

## 19. Residuals and evidence gaps

- The +104 LOC growth awaits Control Room acceptance (§14).
- No prior closure transfers to the changed SHA; the fresh Control Room
  readback must re-derive everything at the candidate SHA.
- Test-environment completeness limitation retained (host CPython
  3.14.7 + pytest 9.1.1 isolated venv; the historical /mnt/archlinux
  JSON C-recursion fault not re-tested; NOT production/event runtime
  compatibility — an S1 evidence obligation).
- NORMAL_EXIT_BOUNDARY_PROCESS_TREE_QUIESCENCE remains an S1
  event-preparation evidence requirement (§18).
- The RED worktree required a metadata-only MANIFEST regeneration
  (documented in §4) because the EBS self-identity walk refuses
  unmanifested files; production bytes at RED were byte-identical to
  the exact base.

NEXT ACTION EXACTLY ONE: INDEPENDENT CONTROL ROOM READBACK OF THE
AUCDEV-023 EBS S1-009 POST-CONSUMPTION FAIL-CLOSED TERMINALITY
REMEDIATION CANDIDATE. No event-package preparation follows
automatically.
