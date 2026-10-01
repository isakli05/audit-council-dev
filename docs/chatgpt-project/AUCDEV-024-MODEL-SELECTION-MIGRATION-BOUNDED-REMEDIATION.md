# AUCDEV-024 — Model-Selection Migration BOUNDED REMEDIATION (AUCDEV024-CR-IMPL-001 / -002 / -003)

- **Authority**: explicit operator authorization `AUTHORIZE AUCDEV-024 BOUNDED
  REMEDIATION FOR AUCDEV024-CR-IMPL-001 / -002 / -003 AGAINST
  111eb9487b442b6de990b5ff4be9f53e252c1f03` (2026-10-01). Remediation
  implementation authority ONLY.
- **Session role**: bounded REMEDIATION IMPLEMENTER of exactly the three named
  Control Room findings on the already-published AUCDEV-024 implementation
  candidate. NOT a redesign of AUCDEV-024, NOT an independent audit, NOT a
  qualification authority, NOT an installation authority, NOT Auditor-A/B,
  NOT a wrapper/driver invoker.
- **Exact base**: `111eb9487b442b6de990b5ff4be9f53e252c1f03` — verified EXACT
  at bootstrap as live master == origin/master == local HEAD (ls-remote
  authoritative; fetch clean rc 0). Pre-existing tracked drift (the
  `smoke-fixture` / `smoke-fixture-103` gitlink rows) was preserved UNSTAGED.
- **Zero-provider**: ZERO provider/model/frontier inference calls, ZERO client
  inference calls, ZERO auditor execution, ZERO wrapper/driver invocation,
  ZERO qualification, ZERO installation, ZERO credential-content access,
  ZERO sealed-substance access, ZERO deployment mutation in THIS session.
  The only non-inference local observation re-confirming the readiness-probe
  surface was reading this session's own `CLAUDE_EFFORT` value (present,
  value `max`; never used as selection input — the audit-default gate treats
  it as a conflicting effective effort that fails closed).
- **Disposition**: `AUCDEV_024_BOUNDED_REMEDIATION_IMPLEMENTED =
  CR_IMPL_001_PRE_SPAWN_DURABLE_CODEX_FREEZE /
  CR_IMPL_002_CLAUDE_EFFECTIVE_EFFORT_MECHANICALLY_BOUND /
  CR_IMPL_003_RESUME_WITHOUT_FROZEN_OPUS_SELECTION_FAILS_CLOSED /
  HELD_SEMANTICS_PRESERVED / DETERMINISTIC_ZERO_PROVIDER_TESTS_772_PASS /
  REMEDIATION_IMPLEMENTED_AWAITING_FRESH_CONTROL_ROOM_READBACK /
  NO_AUDIT_PASS / NO_QUALIFICATION / NO_INSTALLATION`.
- **Status**: AUCDEV-024 remains **P1 / READY / NOT DONE** —
  REMEDIATION IMPLEMENTED / AWAITING FRESH CONTROL ROOM READBACK. The three
  findings are addressed by this remediation; their CLOSURE as independent
  fact belongs to Control Room readback and is NOT claimed here.

---

## 1. Finding 1 — AUCDEV024-CR-IMPL-001 (BLOCKING)
`CODEX_PREINFERENCE_FREEZE_NOT_DURABLE_BEFORE_SPAWN`

**Observed defect**: in `skill/scripts/codex_runner.py` the run's first Codex
selection was frozen into the in-memory `state` before launch, but the
inference-capable child spawned (`launch()` → `Popen`) BEFORE the
authoritative `save_state` — killing the child after a post-spawn persistence
failure does NOT prove zero inference before the failure.

**Fix** (source: `skill/scripts/codex_runner.py`, `cmd_start`, inside the
existing R-B002 run-state-lock launch transaction): for a run's first Codex
selection, after `resolve_codex_selection()` creates the frozen provenance
record, the record is AUTHORITATIVELY persisted (`save_state`) BEFORE
`launch()`/`Popen` can occur. If that pre-spawn persistence fails, `cmd_start`
returns fail-closed (exit 3) with the stable token
`MODEL_SELECTION:CODEX_FREEZE_PERSIST_FAILED` and ZERO children were started.

**Held semantics** (unchanged, re-proven by tests): active-attempt uniqueness;
attempt numbering/accounting; R-B002 post-spawn attempt/job persistence with
kill-on-persistence-failure (`_terminate_launched_job`); a launch failure
after a successful pre-spawn freeze may legitimately leave the run selection
frozen (durable provenance before spawn is preferable to spawning without
it); later attempts reuse the frozen selection exactly (no re-freeze, no
generation switch).

**Tests** (`skill/tests/test_codex_runner_mock.py`, new class
`TestPreSpawnFreeze`, in-process `codex_runner.main` with instrumented
persistence/spawn):
- `test_freeze_persist_failure_zero_launch` — injected selection-freeze
  persistence failure ⇒ exit 3, `CODEX_FREEZE_PERSIST_FAILED`, exactly one
  save attempt (the pre-spawn freeze), **launch count 0**, no durable freeze,
  no job record. (RED first: the pre-fix code spawned and reported
  "authoritative launch persistence failed … terminated".)
- `test_normal_first_launch_freeze_durable_before_spawn` — a Popen probe
  snapshots the on-disk `state.json` at the moment the `/bin/sh` wrap-script
  child is entered: `model_selection.codex` is already durable
  (`gpt-6.1-sol`/`high`, digest verifies); the post-spawn job persistence
  keeps the identical record. (RED first: snapshot was `None`.)
- `test_later_launch_reuses_frozen_record_exactly` — second stage launch
  reuses the frozen record byte-identically (guard on pre-existing semantics).

**Adapted existing test** (`skill/tests/test_b001_b004_remediation.py`,
`test_rb002_persistence_failure_terminates_spawned_child`): its
always-failing save injection now (correctly) hits the pre-spawn freeze save
first, so the injection was moved to fail only the POST-spawn job-persistence
save — the R-B002 kill-on-persistence-failure coverage the tasking requires
is fully preserved (36/36 in that file).

## 2. Finding 2 — AUCDEV024-CR-IMPL-002 (BLOCKING)
`CLAUDE_EFFECTIVE_EFFORT_NOT_MECHANICALLY_BOUND`

**Observed defect**: the candidate froze `claude-opus-5-5 / high` but the
ambient gate only rejected conflicting selection VARIABLES when present; with
`CLAUDE_CODE_EFFORT_LEVEL` absent, `high` could be recorded without
mechanically establishing that the active Claude session runs at effective
effort `high`. Documentation alone was not enforcement.

**Fix** (sources: `skill/scripts/model_selection.py` +
`skill/scripts/audit_council.py`): a new effective-effort gate over the
readiness-probe-established per-turn surface (gate CLAUDE-07, Claude Code
2.1.281: `CLAUDE_EFFORT` — "the active effort level for the current turn …
after any silent downgrade for the selected model", exposed to hook commands
and Bash; re-confirmed locally, non-inference).

- `model_selection.CLAUDE_EFFECTIVE_EFFORT_ENV = "CLAUDE_EFFORT"`;
  `claude_effective_effort(environ)` returns the normalized observable token
  (None when absent/blank); `claude_effective_effort_violation(effort,
  environ)` returns None (equal — pass) or a stable token:
  `EFFECTIVE_EFFORT_UNOBSERVABLE` (absent surface) /
  `EFFECTIVE_EFFORT_MISMATCH` (silent downgrade/clamp). The observed value is
  compared but NEVER returned or printed (names/tokens only, same policy as
  the ambient gate).
- `audit_council._claude_effective_effort_failure(frozen_effort)` formats the
  fail-closed message; the gate is enforced at exactly the tasking-required
  surfaces:
  - **preflight** (`_resolve_claude_selection`): failure check
    `claude-effective-effort`;
  - **init-run / prepare** (`_init_run_core`, which both commands share):
    refuses BEFORE creating the run (zero side effects);
  - **resume-check** (`cmd_resume_check`): before resumed inference.
- The gate requires observable effective effort == the resolved/frozen
  Auditor-A effort (for audit-default therefore `high`); absent/unobservable
  FAILS CLOSED; mismatch FAILS CLOSED; never silently downgrades. It is exact
  equality against the RESOLVED effort — never faked from requested CLI
  values, SKILL frontmatter, the frozen state itself or provider defaults.
- The existing ambient-redirect conflict gate is kept unchanged (additive
  gate, additive fail-closed tokens
  `MODEL_SELECTION:EFFECTIVE_EFFORT_UNOBSERVABLE` /
  `MODEL_SELECTION:EFFECTIVE_EFFORT_MISMATCH` at preflight/init-run and the
  `INVALID_MODEL_SELECTION:`-prefixed forms at resume-check).

**Tests** (`skill/tests/test_model_selection.py`, new classes
`TestEffectiveEffortGateUnit` + `TestEffectiveEffortGate`):
- effective `high` ⇒ preflight PASS;
- effective `medium` ⇒ preflight fail closed (`claude-effective-effort`,
  `EFFECTIVE_EFFORT_MISMATCH`, observed value never printed);
- effective missing ⇒ preflight fail closed (`EFFECTIVE_EFFORT_UNOBSERVABLE`);
- init-run effective mismatch ⇒ refuses BEFORE creation (zero side effects);
- explicit `low` + effective `low` ⇒ accepted (equality, not a high-only
  rule);
- resume-check effective mismatch ⇒ exit 10 / stage `model-selection` /
  `INVALID_MODEL_SELECTION`;
- frozen legacy `claude-opus-5`/`high` + effective mismatch on resume ⇒ fail
  closed, frozen identity never migrated;
- unit: equal passes, mismatch/missing/blank fail closed, case-normalized
  comparison, token-never-value.
All CLI-level tests were written RED first (no gate existed: rc 0/`ok:true`
where fail-closed was required).

**Test-hermeticity consequence** (16 test files): run-lifecycle tests that
create audit-default runs now pin the simulated session surface
`CLAUDE_EFFORT = DEFAULT_EFFORT["opus"]` in their existing ambient-scrub
preambles (`test_model_selection.py` additionally scrubs the surface from
its clean env and pins it per-call). This is simulation-of-session state in
tests only; production reads the live session surface.

## 3. Finding 3 — AUCDEV024-CR-IMPL-003 (BLOCKING)
`LEGACY_OPUS_RESUME_WITHOUT_FROZEN_SELECTION_NOT_FAIL_CLOSED`

**Observed defect**: `resume-check` validated the Auditor-A selection only
when `state.model_selection.opus` existed; when absent, the model-selection
resume gate was silently skipped — conflicting with the accepted AUCDEV-024
rule that an old resumable run without sufficient frozen provenance FAILS
CLOSED rather than guess or silently migrate.

**Fix** (source: `skill/scripts/audit_council.py`, `cmd_resume_check`): when
a run CAN resume inference (phase not in `_NO_INFERENCE_PHASES =
("FINALIZED", "COMPLETE")` — no inference remains past adjudication) and the
required frozen Auditor-A selection is absent, resume-check fails closed
with the explicit stable reason
`MODEL_SELECTION:RESUME_WITHOUT_FROZEN_SELECTION` (exit `EXIT_ENV`/10, stage
`model-selection`, `completeness_state` `INVALID_MODEL_SELECTION`). Nothing
is invented from version/date/default; no legacy run is silently migrated;
no historical state is rewritten (the run's own `state.json` stays exactly
as history left it — verified by test).

**Schema compatibility preserved** (separate concern from operational resume
permission): `model_selection` remains OPTIONAL in `state.schema.json`
(unchanged); a historical state WITHOUT `model_selection` still validates as
a historical artifact — re-proven by
`test_historical_state_without_model_selection_remains_schema_valid`.

**Tests** (`skill/tests/test_model_selection.py` new class
`TestResumeWithoutFrozenSelection` + `skill/tests/test_migration_compat.py`):
- historical state without `model_selection` still schema-valid;
- resume-check on a resumable state lacking Auditor-A frozen provenance
  FAILS (exit 10 / `MODEL_SELECTION:RESUME_WITHOUT_FROZEN_SELECTION`) and
  leaves the state untouched;
- a terminal `COMPLETE` legacy run without frozen selection is NOT gated
  (cannot resume inference; other completeness problems are separate);
- a properly frozen legacy `claude-opus-5`/`high` run resumes exactly as
  frozen (exit 0, identity unchanged — no generation migration), subject to
  the effective-effort/model gates;
- `test_migration_compat.test_v1_lines_artifact_accepted_bytes_unchanged`
  updated to the accepted rule: the genuine v1-era run (no binding, no
  `model_selection`) at a resumable phase now FAILS CLOSED at resume-check
  (the v1 artifact itself was already accepted by `advance` and its bytes
  stay unchanged — that coverage is unchanged).

## 4. Change inventory (finding mapping)

| Path | Change | Finding |
|---|---|---|
| `skill/scripts/codex_runner.py` | pre-spawn authoritative freeze save + `CODEX_FREEZE_PERSIST_FAILED` fail-closed path; comment updated | CR-IMPL-001 |
| `skill/scripts/model_selection.py` | `CLAUDE_EFFECTIVE_EFFORT_ENV`, `claude_effective_effort`, `claude_effective_effort_violation`; docstring | CR-IMPL-002 |
| `skill/scripts/audit_council.py` | `_claude_effective_effort_failure` helper; gate at preflight / `_init_run_core` / `cmd_resume_check`; `_NO_INFERENCE_PHASES`; `RESUME_WITHOUT_FROZEN_SELECTION` else-branch | CR-IMPL-002, CR-IMPL-003 |
| `skill/tests/test_codex_runner_mock.py` | `TestPreSpawnFreeze` (3 tests) + imports | CR-IMPL-001 |
| `skill/tests/test_b001_b004_remediation.py` | R-B002 injection moved to the post-spawn save (kill-on-failure coverage preserved) | CR-IMPL-001 |
| `skill/tests/test_model_selection.py` | `TestEffectiveEffortGateUnit` (5) + `TestEffectiveEffortGate` (7) + `TestResumeWithoutFrozenSelection` (4); hermetic `CLAUDE_EFFORT` scrub/pin; 5 existing gate tests pinned to the simulated surface | CR-IMPL-002, CR-IMPL-003 |
| `skill/tests/test_migration_compat.py` | v1-era resumable resume now asserted fail-closed; preamble pin | CR-IMPL-003 (+002 hermeticity) |
| 13 further `skill/tests/test_*.py` | preamble pin of the simulated effective-effort surface only | CR-IMPL-002 hermeticity |

## 5. Held AUCDEV-024 semantics (NOT regressed)

Audit-default pair `claude-opus-5-5`/high + `gpt-6.1-sol`/high; modes
audit-default / explicit-request-only inherit / explicit; precedence
EXACTLY explicit > explicitly requested inherit > audit-default; NO silent
fallback; additive legacy schema identities (schemas untouched this session);
historical artifacts never relabelled; Codex fresh + resume explicit
run-frozen model/effort; Codex `MODEL_MISMATCH` exit-8 boundary; Claude
ambient-model redirect fail-closed gate; selection-digest tamper detection;
unsupported/symbolic inherit fail-closed. No unrelated AUCDEV-023/PCH6
finding was remediated.

## 6. Validation (all zero-provider)

- Focused, per tasking minimum: CR-IMPL-001 `TestPreSpawnFreeze` 3/3;
  CR-IMPL-002 `TestEffectiveEffortGateUnit` + `TestEffectiveEffortGate`
  12/12; CR-IMPL-003 `TestResumeWithoutFrozenSelection` +
  `test_migration_compat` + `test_schema_validation` 21/21 — ALL PASS.
- Directly affected suites: `test_model_selection`, `test_resume`,
  `test_migration_compat`, `test_public_contract` 94/94;
  `test_codex_runner_mock` 42/42; `test_b001_b004_remediation` 36/36.
- Full deterministic suite `python3 -m unittest discover -s skill/tests`:
  **772 tests, ALL PASS, 0 failures, 0 errors, 0 skips** (753 pre-existing +
  19 new). First outputs of every RED run are preserved verbatim in the
  untracked evidence workspace `aucdev024-bounded-remediation-evidence/`.

## 7. Honest session iteration (no erasure)

- **T-1 (fixed in-session)**: full-suite run 1 had exactly ONE failure —
  `test_b001_b004_remediation…test_rb002_persistence_failure_terminates_
  spawned_child`: its unconditional persistence-failure injection
  (correctly) hit the new pre-spawn freeze save first, so zero children
  spawned and no diagnostic job record existed for it to inspect. The
  injection was bounded to fail only the post-spawn job-persistence save
  (first output preserved; run-1 output preserved in
  `20-suite/full-suite-v1.txt` capture); the R-B002 kill-on-failure coverage
  is preserved and green. No failed observation was rewritten as PASS.
- Cosmetic: one GREEN tee captured the CR-IMPL-003 run twice (harmless
  duplicate in the evidence file, not a test rerun falsification).

## 8. Next action (exactly one; grants nothing)

INDEPENDENT CONTROL ROOM READBACK OF THE AUCDEV-024 BOUNDED REMEDIATION
CANDIDATE AT THE NEW EXACT SHA. Do NOT start an independent audit; do NOT
qualify; do NOT install. This remediation claims NO audit PASS, NO
qualification, NO installation, and closes nothing as independent fact.
