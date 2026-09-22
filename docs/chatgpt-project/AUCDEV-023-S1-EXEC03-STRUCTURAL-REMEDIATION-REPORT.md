# AUCDEV-023 — S1 EXEC-03 STRUCTURAL CONTRACT / VALIDATOR REMEDIATION — IMPLEMENTATION REPORT

- **Date**: 2026-09-22 (Europe/Istanbul)
- **Authority**: `AUCDEV-023-S1-EXEC03-STRUCTURAL-REM-20260922-01`
  (bounded zero-provider remediation; granted by the HUMAN OPERATOR;
  this authority grants NO real Auditor-A/B execution, NO provider/model
  engagement, NO credential use, NO replacement event/attempt minting,
  NO deployment, NO qualification and NO installation).
- **Session role**: BOUNDED REMEDIATION IMPLEMENTER ONLY (Claude Code +
  GLM-5.3). NOT the Control Room, NOT Auditor-A/B, NOT an execution
  controller / execution / qualification / installation authority.
  Auditor-A substantive report content and the four findings' subject
  matter were NOT read or evaluated; only the mechanical defect
  descriptions in the Control- Room-accepted EXEC-03 mechanical
  readback were remediated.
- **Disposition (implementer, §16)**:
  `AUCDEV_023_S1_EXEC03_STRUCTURAL_REMEDIATION = IMPLEMENTED /
  EXEC03_003_CONTRACT_BOOLEAN_TYPE_EXPLICIT / VALIDATOR_STRICTNESS_HELD /
  EXEC03_001_SAFE_VALIDATOR_FAILURE_DIAGNOSTIC_IMPLEMENTED /
  EXEC03_002_REAL_VALIDATOR_NEGATIVE_PATH_REGRESSION_ADDED /
  EXEC03_004_INVALID_SNAPSHOT_IDENTITY_DURABLE /
  HISTORICAL_EXEC03_STATE_IMMUTABLE / NO_REPLACEMENT_EVENT_MINTED /
  ZERO_PROVIDER_MODEL_EXECUTION / AWAITING_CONTROL_ROOM_READBACK`
  — NOT a claim that any finding is CLOSED (findings close only at
  Control Room readback), NOT an audit PASS, NOT qualification, NOT
  replacement-execution readiness.

## 1. Bootstrap and base verification (EXACT)

- Live GitHub `master` resolved at session bootstrap and re-resolved
  immediately before staging: `58161595fb217c947a05eed8fd7f1cd5f018ab22`
  (GitHub branch API readback identical).
- Required tree verified EXACT: `1a1af40e19424515181157122f3fd7f47bda76f9`;
  sole parent `e7bff48c91686c74f72e81d42497cf72caf35bcd` (single-parent
  verified).
- Starting protected subtrees verified EXACT at the base:
  bootstrap-supervisor `09f3d6c7ddc00305986cbedad431395c10c95af0`,
  qualification-harness `5b8d5e5465923740470ff63ed9b8683f257a3787`,
  skill `c792933a862d9a5434681a88d183470dd8b15d2f` (the latter two
  equal the frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322`;
  both remain byte-unchanged by this remediation — verified again after
  implementation).
- The six authoritative docs were fetched AT that exact SHA and read
  before any mutation.

## 2. Remediation workspace and future-generation source establishment

Workspace: `/home/isa/aucdev023-s1-exec03-structural-remediation/` (all
NEW files; nothing else written outside it and the Git working tree).

Canonical preparation-component provenance established (§4): the
accepted new-event preparation workspace
`/home/isa/aucdev023-s1-new-event-identity-regen/` holds the
future-generation authority — its `common-evidence/prompt-contract.json`
(accepted contract SHA-256
`e4204e673e56d62d4e4ba0aceb44cc5ca599cf2ddb4e774568977544ac3fdd73`) is
the exact file `components/build/build_packages.py` copies verbatim into
both role packages (`transport/prompt-contract.json` 0644 and
`payload/evidence/common/prompt-contract.json` 0444), and
`components/runtime/output-validator.py` is the canonical frozen
validator source. The frozen validator identity
`6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071`
(7228 B) was re-verified byte-identical at all five copies (both
deployed role packages, both accepted-preparation event-package copies,
and the accepted component source). STOP did not arise: an authoritative
future-generation source WAS established.

## 3. EXEC03-003 — corrected future-generation prompt-contract source

The frozen validator remains STRICT and UNCHANGED
(`isinstance(covered, bool)` at `output-validator.py:123-124`; NOT
broadened; `"COVERED"`/`"NOT covered"` remain REFUSED wire values).

Future-generation source (external remediation workspace, where the
established preparation authority lives, per §12):

- `contract/prompt-contract.future-template.json` — SHA-256
  `5b2c39bd1f1782ce30d8c23d1a71a55f626b30547bc2e733360c780693628e3a`,
  6164 B, derived mechanically from the accepted contract bytes with
  EXACTLY TWO edits:
  1. the ONE authorized substantive clarification: the
     `report_requirements.schema.coverage` clause keeps its full
     original text and appends
     `; covered MUST be a JSON boolean: true means COVERED, false means
     NOT covered`;
  2. mechanical event-id parameterization: the single top-level
     `event_id` value (exactly one occurrence) replaced by the sentinel
     `{{EVENT_ID}}`.
- `contract/render_prompt_contract.py` — the deterministic renderer:
  refuses any event id not matching the frozen EBS grammar
  `^evt-[0-9a-f]{16}$`, requires the sentinel to occur exactly once,
  requires the rendered strict-JSON output to carry the corrected
  clause and the rendered event id, and writes nothing else.
- Generator: `scripts/02_build_contract_template.py` (asserts the
  accepted-bytes SHA before editing; asserts uniqueness of both edit
  targets; asserts the template parses as strict JSON).

NO new real event id was minted; the template carries only the sentinel.
Historical contracts are untouched (re-verified byte-exact in all five
accepted-copy locations — see §9).

**Semantic-hold evidence** (`evidence/contract-semantic-hold.json`,
script `scripts/03_contract_semantic_hold.py`): rendering the template
with the current accepted event id `evt-31f2a399b3a7e11d` (comparison
value ONLY — no package built) vs the accepted contract bytes:

- parsed deep-diff count = **1**, exactly
  `$.report_requirements.schema.coverage`, old value = the original
  clause, new value = original clause + the appended boolean
  specification; EVERY other field (schema, event_id, task, target,
  frozen_evidence_set, review_requirements.* minus the one clause,
  execution_permissions, report_requirements.format/independence,
  neutrality) parsed-EQUAL;
- textual unified diff = **exactly one changed line** (the coverage
  clause line);
- the corrected clause states all three required facts (covered MUST be
  a JSON boolean / true means COVERED / false means NOT covered);
- renderer fail-closed negatives: 5 malformed event-id inputs all
  refused with no output file; a sentinel-corrupted (double-sentinel)
  template refused.

**Contract ↔ validator coherence (§9)**
(`evidence/contract-validator-coherence.json`, deterministic zero-model
test in the external preparation-component test plane
`tests/contract_validator_coherence.py`): C1 the future contract
declares `covered` a JSON boolean; C2 true→COVERED / false→NOT covered;
C3 the EXACT frozen validator (identity re-verified) ACCEPTS booleans
true and false through the exact EBS child fd contract; C4 the EXACT
validator REJECTS the strings `"COVERED"` and `"NOT covered"` with the
exact structural diagnostic `COVERAGE_0_COVERED_NOT_BOOL`; C5 contract
and validator specify the SAME wire type — **all verdicts TRUE**.

## 4. EXEC03-001 — safe validator failure diagnostic

Root cause (from the accepted mechanical readback, mechanically
re-confirmed here at the exact base): `_run_runtime_gate` opened
`/dev/null` `O_RDONLY` and `_gate_child` dup2'd that read-only fd onto
child fd 0 AND fd 2; the real frozen validator writes
`VALIDATION_ERROR: …` to stderr on structural FAIL (its stdout envelope
carries NO error field), so the write failed and CPython terminated as
exit 120, masking the intended rc-1 result and its diagnostic.

Remediation (bootstrap-supervisor/ebs/launch.py only):

1. `_gate_child` gains an optional `stderr_w`; when provided it is
   dup2'd onto child fd 2 INSTEAD of the read-only devnull. Every
   non-validator gate call passes nothing and keeps the exact historical
   fd shape (unit-pinned by
   `test_exec03_u5_non_validator_gates_retain_readonly_stderr`: a
   stderr-writing NON-validator child still yields exactly
   `…_NONZERO_EXIT: exited 120` with no captured diagnostic).
2. `_run_runtime_gate` gains `capture_stderr` (used ONLY by
   `_run_validator`): a bounded stderr pipe read under the SAME
   deadline and size discipline — more than `VALIDATOR_STDERR_MAX`
   (4096) stderr bytes kills the child and refuses fail-closed
   (`…_STDERR_TOO_LARGE`), and a final bounded drain runs after the
   child is reaped.
3. `_sanitize_structural_diagnostic` — the bounded STRUCTURAL-ONLY
   diagnostic grammar established by inspecting the exact validator
   source: every emission is `VALIDATION_ERROR: <detail>` where
   `<detail>` is either a fixed uppercase structural token, or a token
   plus report-derived data (duplicate-key names, repr'd values,
   parser/codec prose). The sanitizer accepts the captured channel ONLY
   if it decodes as UTF-8, is within the size bound, starts with the
   frozen `VALIDATION_ERROR: ` prefix, and reduces the pre-colon token
   to a short uppercase `[A-Z0-9_]{1,128}` identifier. Everything else
   (prose, reprs, key names, lowercase, non-UTF-8, oversize, empty)
   yields `""` → the caller falls back to the EXACT prior generic
   refusal message. On a non-zero validator exit the refusal detail
   becomes `…NONZERO_EXIT: exited 1; structural_error=<token>` — the
   `[:256]` terminal-reason cap and all existing message forms are
   otherwise unchanged.
4. No credential fd enters the validator path (unchanged `_gate_child`
   fd discipline; the report snapshot remains the ONLY inherited data
   channel at the fixed `VALIDATOR_REPORT_FD`).

## 5. EXEC03-004 — durable invalid snapshot identity

In `_report_and_terminalize`, the REPORT_INVALID settlement now pins
the EXACT immutable snapshot that was supplied to the validator:

- the durable `REPORT_INVALID` accounting record gains
  `report_sha256` (SHA-256 of the exact in-memory snapshot bytes that
  were sealed onto the validator memfd) and `report_size`;
- the mechanical `AttemptResult` carries the same two values;
- hash/size ONLY — the invalid report BYTES are never persisted to any
  EBS/mechanical surface (the operator's own staging file remains in
  the operator plane exactly as before; nothing is frozen; REPORT_FROZEN
  semantics unchanged);
- REPORT_INVALID remains terminal and nonconforming; no freeze, no
  acceptance, no retry.

REPORT_MISSING and REPORT_SCREEN_FAIL records remain identity-free (a
missing report has no snapshot; a contaminated report is screened
BEFORE the validator — existing semantics preserved and re-pinned by
the updated `test_s1_007_recorded_digest_only_after_screen_passes`).

## 6. EXEC03-002 — real validator negative-path regression

- `tests/real_validator_materialization.py` (NEW): the mechanically
  byte-equivalent materialization of the exact frozen validator source
  (base64 payload; SHA-256 asserted == `6aff0e7e…` at EVERY
  materialization — drift fails closed). NOT a `tests/fixtures/*.py`
  inert fixture; the inert fixture discipline and marker are untouched.
- `tests/conftest.py`: `make_event_package` gains an additive optional
  `validator_bytes` parameter (None → byte-identical prior behavior for
  every pre-existing call).
- `tests/test_exec03_real_validator_lifecycle.py` (NEW, 31 tests):
  through the EXACT EBS `run_attempt` → `_run_validator` →
  `_run_runtime_gate` → `_gate_child` → fd_exec path with the REAL
  frozen validator bound into a synthetic event package
  (synthetic event `evt-0000e03c0de0aa55` — disjoint from every
  reserved real/rehearsal id):
  - **V1** conforming boolean report (true AND false) → validator PASS
    → REPORT_FROZEN with the exact frozen bytes;
  - **V2** `coverage[*].covered` = the STRING `"COVERED"` →
    REPORT_INVALID, NO rc-120, durable reason contains
    `structural_error=COVERAGE_0_COVERED_NOT_BOOL`;
  - **V3** the durable record + AttemptResult pin the exact planted
    snapshot SHA-size (bytes never retained in mechanical evidence);
  - **V4** distinctive prose markers planted in summary/note/methodology
    appear NOWHERE in the terminal reason, AttemptResult repr, or raw
    accounting bytes;
  - **V5** stderr oversize → `STDERR_TOO_LARGE` fail-closed kill;
    malformed (non-VALIDATION_ERROR) stderr → generic bounded refusal
    with zero child text; a genuine token line → the token carried;
  - **V6** exactly one EXEC_ATTEMPTED / one REPORT_INVALID record and a
    refused second `run_attempt` (no second validator attempt, no
    retry);
  - **V7** 15 parametrized pre-existing structural negatives
    (keys/schema/event/role/attempt/target/summary/findings/severity/
    coverage-shape/coverage-area/residuals) each REPORT_INVALID with
    the exact expected token + exact snapshot identity + no prose; plus
    malformed-JSON (generic, no parser prose), duplicate-keys (token
    `DUPLICATE_KEY`, duplicated KEY NAME absent), non-UTF-8 (generic);
  - **U1–U5** sanitizer grammar unit pins (accept pure tokens; token
    only, detail dropped; refuse prose/lowercase/non-prefix/non-UTF-8/
    oversize; exact two-level bounds) and the non-validator-gate
    read-only-stderr retention pin.
- Existing inert-validator tests retained and still passing for what
  they test; the two assertions that pinned the pre-remediation
  REPORT_INVALID shape were updated to the remediated contract (see §8
  classification).

## 7. §11 historical reproduction — BEFORE (preserved historical copy)

Run in an isolated detached git worktree at the EXACT base
`5816159` (removed after; `evidence/hist-rc120-reproduction.json`):

- **R1** frozen validator, writable stderr, string-covered synthetic
  report: rc **1** (not 120), stdout FAIL envelope, envelope
  `report_sha256`/`report_size` exactly the snapshot identity;
- **R2** the SAME validator through the EXACT BASE
  `_run_runtime_gate(..., report_bytes=…)` (fd 0+2 from an `O_RDONLY`
  /dev/null): `LaunchRefused("OUTPUT_VALIDATOR_NONZERO_EXIT: exited
  120")` — NO envelope, NO diagnostic — the exact masking;
- **R3** the FULL BASE `Supervisor.run_attempt` lifecycle with the real
  validator bound into a synthetic event package: states
  PREPARED→GATES_PASSED→CONSUMED_PRE_EXEC→EXEC_ATTEMPTED→
  REPORT_INVALID→TERMINAL; durable terminal reason
  `REPORT_INVALID: OUTPUT_VALIDATOR_NONZERO_EXIT: exited 120`; the
  REPORT_INVALID record's key set = {state, terminal_reason} ONLY —
  `report_sha256=""` / `report_size=0` — the exact EXEC03-004 gap shape
  observed in the historical `evt-31f2a399b3a7e11d-A-01` record.

## 8. Source diff discipline (§12) — exact change set and classification

Tracked Git changes over the exact base (5 modified + 2 new; NOTHING
else; smoke-fixture gitlink drift pre-existing and preserved unstaged):

| Path | base blob → new blob | Classification |
|---|---|---|
| `bootstrap-supervisor/ebs/launch.py` | `7c45fcddd3a8` → `063b6ce1f4c7` | EXEC03_001_REMEDIATION (stderr channel + sanitizer) + EXEC03_004_PROVENANCE (REPORT_INVALID identity) — SHARED_NECESSARY between the two; +112 production lines (1573→1685 in launch.py; ebs total 2904→3016) |
| `bootstrap-supervisor/tests/conftest.py` | `3ffb71034cf7` → `477481a95007` | EXEC03_002_REGRESSION (additive `validator_bytes` parameter; default path byte-identical) |
| `bootstrap-supervisor/tests/real_validator_materialization.py` | NEW `65c2ca7319e6` | EXEC03_002_REGRESSION |
| `bootstrap-supervisor/tests/test_exec03_real_validator_lifecycle.py` | NEW `f4c3ee8c7608` | EXEC03_002_REGRESSION (covers V1–V7 for -001/-002/-003/-004) |
| `bootstrap-supervisor/tests/test_final_execution_lifecycle.py` | `4a789434e6ce` → `4a27c1103cf6` | EXEC03_004_PROVENANCE (two assertions moved from the pre-remediation empty-identity shape to the exact snapshot-identity contract; all other semantics unchanged) |
| `bootstrap-supervisor/tests/test_static.py` | `bedb1a45f9e8` → `78326bc5fd93` | SHARED_NECESSARY (minimal-TCB LOC bound raised to the new exact total 3016 with the established NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE disclosure chain; prior baselines preserved, not rewritten) |
| `bootstrap-supervisor/MANIFEST.json` | `8d27e478154f` → `20f1dedf2760` | SHARED_NECESSARY (deterministic regeneration over the changed tree — mandatory because the EBS fail-closed-verifies its own live package bytes against this manifest at every Supervisor construction; metadata updated: implementation_base_commit `5816159…`, status `EXEC03_STRUCTURAL_REMEDIATION_CANDIDATE / AWAITING_FRESH_CONTROL_ROOM_READBACK`, task updated; `target.*` frozen-audit-target block byte-unchanged; 31→33 file rows = the two new test files) |

UNEXPECTED source changes: **NONE**. qualification-harness and skill:
byte-unchanged (trees re-verified EXACT after implementation). The
EXEC03-003 future-generation contract source remains in the bounded
external remediation workspace (where the established event-package
preparation authority lives); no architecture was moved into Git.

## 9. Held invariants and historical immutability

- Frozen audit target `d4d584ff…` untouched; qh + skill trees EXACT.
- Auditor-A/B provider identities, credential adapters,
  NETWORK_READINESS semantics, RESOURCE_GATE remediation semantics,
  one-shot authority semantics, custody no-follow behavior, barrier
  blindness, A-before-B, no-retry: unchanged (no code path touched
  beyond the validator stderr channel and the REPORT_INVALID
  settlement extras).
- Historical EXEC-03 state re-verified read-only byte-EXACT after the
  implementation: `evt-31f2a399b3a7e11d-A-01` accounting
  `85f7a80b0f427794fdb4532f19e55dd7ff17b962bee5756308e95aa86f2f2c27`
  (six records, PREPARED→…→REPORT_INVALID→TERMINAL) and its staging
  artifact `d62cb6680e00a16224fc77b73233e3c6075be85ef2b84190cbe7a527777efa19`
  / 30713 B (post-run diagnostic artifact — status NEVER upgraded by
  this remediation); `evt-31f2a399b3a7e11d-B-01` empty (NOT STARTED);
  the launcher-root attempts listing is exactly the historical set (no
  new entries); deployed event generation, both backups, the accepted
  preparation workspace and all historical contracts/records only ever
  READ.
- The frozen validator itself was NOT modified (both deployed copies
  still `6aff0e7e…`); strictness held (§3).

## 10. Tests and batteries (all on the remediated live tree)

- Focused: `tests/test_static.py` +
  `tests/test_final_execution_lifecycle.py` +
  `tests/test_exec03_real_validator_lifecycle.py` → 75 passed.
- Complete EBS deterministic battery: **520 passed / 0 failed / 0
  skipped** in 39.93 s (rc 0). Accepted pre-remediation baseline 489;
  the collected-count change is EXACTLY the 31 newly added EXEC03
  regression tests (2 V1 + V2 + V3 + V6 + 3 V5 + 15 parametrized V7 + 3
  V7 extras + 5 U) — no existing test removed or weakened; the two
  updated assertions are the remediated EXEC03-004 contract described
  in §8.
- Complete qualification-harness battery: **221 passed / 0 failed / 0
  skipped** in 27.49 s (rc 0) — exactly the accepted baseline; qh tree
  byte-unchanged.
- `compileall -q bootstrap-supervisor qualification-harness` rc 0.
- Test environment: host CPython 3.14.7 + pytest 9.1.1 (the same
  isolated venv reused as the accepted battery environment);
  TEST_ENVIRONMENT_DIVERGENCE retained.

## 11. Zero-execution attestation

Provider/model/frontier inference ZERO; real credential bytes ZERO
(only the synthetic `SYNTH_CRED` test fixture); Auditor-A/B /
`/audit-council` executions ZERO; `Supervisor.run_attempt` executions =
the SYNTHETIC lifecycle tests/reproductions above ONLY (synthetic event
ids `evt-0000e03c0de0aa55` / `evt-c0ffee00000e03c0` in throwaway /tmp
trees — disjoint from every reserved real/rehearsal attempt id); real
AccountingStore creation ZERO outside those synthetic /tmp trees;
GATES_PASSED / CONSUMED_PRE_EXEC / EXEC_ATTEMPTED on any REAL attempt
ZERO; wrapper execution ZERO; deployment ZERO; replacement event or
attempt minting ZERO; qualification NONE; installation NONE; network
activity ZERO beyond this publication's git fetch/push. Auditor-A
substantive report content was never read, summarized or evaluated.

## 12. Resulting state and next action

EXEC-03 historical state unchanged and closed (authority
`AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-03` remains CLOSED / NO RETRY /
NON-TRANSFERABLE; Auditor-A CONSUMED / REPORT_INVALID / TERMINAL;
Auditor-B NOT STARTED; budget 1/2 fail-closed; NO conforming first
pass). The four findings remain OPEN as Control Room facts with
implementer disposition REMEDIATION_IMPLEMENTED for -001/-002/-004 and
contract-template PREPARED for -003; AUCDEV-023 remains P1 / READY /
NOT DONE with NO backlog count/status change (READY 9 / OPEN 7 /
BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11 — no backlog-row transition;
no finding CLOSED by this session).

NEXT ACTION EXACTLY ONE: CONTROL ROOM READBACK OF THIS EXEC-03
STRUCTURAL REMEDIATION BEFORE ANY REPLACEMENT EVENT OR FIRST-PASS
EXECUTION AUTHORITY (verify the exact base/result SHAs, the §8 change
classification, the 520/221 battery results, the contract template +
renderer + semantic-hold + coherence evidence under
`/home/isa/aucdev023-s1-exec03-structural-remediation/`, and the
generated-LAST complete handoff archive).
