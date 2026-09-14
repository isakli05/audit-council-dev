# AUCDEV-010 — R-B001 Exact Launch-Transition Binding Successor Correction — Canonical Record

Published: **2026-09-14** (Europe/Istanbul).

Session role: the IMPLEMENTER for ONE narrow successor correction to the
already-published B-001..B-004 bounded remediation. This session is NOT
Auditor A, NOT Auditor B, NOT the Control Room, NOT a qualification
authority and NOT an installation authority, and it performed ZERO
model/frontier/provider inference (no `/audit-council`, no Claude Opus, no
GPT-5.6 Sol, no codex inference, no other provider/model call). Only
deterministic local source, tests and tools were executed.

## 1. Live bootstrap (fail closed; verified before any edit)

Live GitHub `refs/heads/master` resolved EXACTLY to
`b04aa604771b237e3bc8abe96daa358fa8f9edd6` (= `origin/master` = local
HEAD; normalized full-SHA comparison). At that exact SHA this session
fetched and read CURRENT-STATE (history record 53), BACKLOG (AUCDEV-010
history record 55), the Control-Room Runbook, the Project Update Protocol
and `AUCDEV-010-B001-B004-BOUNDED-REMEDIATION.md`. Required identities
verified EXACT: historical audited target
`68e3b082958d2f6f35224702e51e35bbbd49d7db` (present, unmutated); published
bounded-remediation product candidate
`ecfece1830b44012cad3f46ab235bea9335fdeb7` (root tree
`682ae9f4568e51491004591c6701cd479d3511db`; `skill/` tree
`fb60425d17ee897e2d9dc9c6eaa08723541e7b45`); governance publication
`b04aa60…` sole parent `ecfece1…`. The pre-fix product bytes were EXACTLY
the published candidate bytes: live `b04aa60:skill` equals `fb60425d…`
(pre-fix `state_store.py` SHA-256
`c41a4ed8dddb365fa6fea28827a022fe46cc1246e586aa1743c142e9b8f2d8f3`; the
tracked working tree was clean — the ambient `smoke-fixture` /
`smoke-fixture-103` gitlink "modified (untracked content)" flags and the
untracked `aucdev019-evidence/` directory are pre-existing local state,
untouched by this session, with unchanged gitlink SHAs).

## 2. Input authority and scope

The Control Room readback of the B-001..B-004 bounded remediation is
PARTIALLY ACCEPTED. Accepted as implementation evidence pending fresh
audit: R-B002, R-B003, R-B004 and the R-B001 completeness/finalize
invariant. Still incomplete:
`R-B001_STAGE_LAUNCH_EXACT_TO_PHASE_BINDING_INCOMPLETE` —
`state_store.check_stage_launch()` accepted an unconsumed skip when
`from_phase == current` and `to_phase` merely CROSSED the skipped phase,
without requiring the record's `to_phase` to equal the exact transition
context of the stage being launched. A record such as
`CONTRACT_FROZEN -> FINALIZED` naming `OPUS_INDEPENDENT_COMPLETE`
therefore satisfied the independent-stage launch gate even though the
exact valid launch binding is `CONTRACT_FROZEN ->
CODEX_INDEPENDENT_COMPLETE`. The prior "misbound" regression tested a
different `from_phase`, not the same-from/wrong-to case.

Non-goals honored: no state-machine redesign; R-B002/R-B003/R-B004
production code untouched (no deterministic regression required touching
them); no other finding modified; no fresh A/B package prepared or
executed; no historical record rewritten.

## 3. Identities

| Identity | Value |
|---|---|
| Correction base (live master, exact) | `b04aa604771b237e3bc8abe96daa358fa8f9edd6` |
| Pre-fix product bytes | skill tree `fb60425d17ee897e2d9dc9c6eaa08723541e7b45` (= candidate `ecfece1…` skill tree); `state_store.py` SHA-256 `c41a4ed8dddb365fa6fea28827a022fe46cc1246e586aa1743c142e9b8f2d8f3` |
| Product successor commit | `d77333e86aa091d2ac003e9a2ad26c88dff56aeb` (sole parent `b04aa604771b237e3bc8abe96daa358fa8f9edd6`) |
| Successor root tree | `de7261e3c912fa74e3a06d3f114b7e489c66225c` |
| Successor `skill/` tree | `c792933a862d9a5434681a88d183470dd8b15d2f` |
| Changed paths | exactly 3: `skill/scripts/state_store.py`, `skill/tests/test_b001_b004_remediation.py`, `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md` |
| Diffstat | +135 / −14 |
| `git diff --check` | CLEAN |

## 4. Frozen pre-fix RED evidence (before any product edit)

Seven new deterministic regressions added to
`skill/tests/test_b001_b004_remediation.py` (`TestRB001SkipLaunchBinding`),
run against the exact pre-fix product bytes (RED-time module SHA-256 in
the handoff archive; `state_store.py` still `c41a4ed8…`):

- RED-1 `test_rb001_same_from_wrong_to_finalized_cannot_authorize_launch`
  — current `CONTRACT_FROZEN`, unconsumed record
  `skipped_phase=OPUS_INDEPENDENT_COMPLETE`, `from_phase=CONTRACT_FROZEN`,
  `to_phase=FINALIZED`: PRE-FIX observation **LAUNCH_ADMITTED**
  (`StateError not raised`) — must become refusal.
- RED-2 `test_rb001_same_from_wrong_to_normalized_cannot_authorize_launch`
  — the same shape with another well-formed later `to_phase`
  (`NORMALIZED`) that crosses the skipped phase but is not the
  independent-stage completion transition: PRE-FIX admitted, must be
  refused.
- RED-3 `test_rb001_cross_exam_same_from_wrong_to_refused` — the analogous
  early-launch form for the other skip-gated model stage
  (`cross_examination` from `CODEX_INDEPENDENT_COMPLETE`, both passed
  artifact phases covered by same-from records bound to `FINALIZED`):
  PRE-FIX admitted, must be refused.

Frozen result (verbatim output in the handoff archive): **Ran 36 tests —
FAILED (failures=3, errors=0)**. All three failures are exactly the
same-from/wrong-to mechanism; the 33 truthful-path guards passed on the
pre-fix bytes — including the CONTROL
(`CONTRACT_FROZEN -> CODEX_INDEPENDENT_COMPLETE` exact binding admitted),
wrong-from refusal, legacy-unbound refusal, consumed-exact-binding
refusal, at-entry launch admission, already-completed refusal, and the
cross-examination exact-binding early-launch admission — proving the
regressions block exactly the borrowed-authority mechanism, not the
truthful workflows. No timing is used anywhere.

## 5. Root cause and exact correction

Root cause (pre-fix `skill/scripts/state_store.py`, launch-coverage loop):
a skip record was counted as launch coverage when it was unconsumed, its
`from_phase` equaled the current phase, and its `to_phase` merely
satisfied `PHASE_INDEX[to_phase] > PHASE_INDEX[skipped_phase]` — a
crossing test that never compares against the stage's completion phase
`done = PHASE_CHAIN[PHASE_INDEX[entry] + 1]`, which the function already
computed. A future transition recorded for another purpose therefore lent
launch authority.

The correction (one comparison): an authorizing skip record for an early
model-stage launch must now satisfy ALL of —

1. `consumed is not True`;
2. `from_phase ==` the current phase;
3. `to_phase ==` the EXACT stage-completion phase, derived mechanically
   per stage: `PHASE_CHAIN[PHASE_INDEX[STAGE_ENTRY_PHASE[stage]] + 1]`
   (`CODEX_INDEPENDENT_COMPLETE` for `independent`;
   `CODEX_CROSS_EXAM_COMPLETE` for `cross_examination`;
   `ADJUDICATION_COMPLETE` for `adjudication`);
4. the record names the exact skipped artifact phase being covered (the
   record covers exactly its own `skipped_phase`, as before).

A record bound to ANY other `to_phase` — later, merely crossing, or
unbound legacy — authorizes nothing.
`PHASE_INDEX[to_phase] > PHASE_INDEX[skipped_phase]` is no longer used as
sufficient authorization anywhere in the launch gate. The gate's refusal
message now names the exact required transition
(`exactly {cur} -> {done}`), and the function docstring states the exact
binding. `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md` item 37 replaced the
too-broad "transition that actually crosses the skipped phase" claim with
the exact mechanically proven binding. No other production path changed.

## 6. GREEN evidence (first results preserved verbatim in the archive)

- Focused: remediation module **36/36 OK** (29 prior + 7 new); QX
  stabilization 41/41; state store 18/18; codex-runner mock 26/26;
  resume 11/11.
- Full deterministic suite, natural posture: **686 tests OK — 0 failures,
  0 errors, 0 skips** (121.3 s). The count is NOT assumed to remain 679:
  686 = 679 + the 7 new regressions, discovered, not hard-coded.
- Warning-visible posture (`PYTHONWARNINGS=always PYTHONTRACEMALLOC=15`):
  **686 OK — 0 warning lines of ANY category, 0 `Exception ignored`**
  (489.4 s).
- Warnings-as-error posture (`PYTHONWARNINGS=error`): **686 OK, exit 0**
  (121.6 s).
- Isolated clean-environment posture (`env -i`, fresh
  HOME/XDG/AUDIT_COUNCIL_CACHE_HOME/AUDIT_COUNCIL_ENV_ROOT,
  PATH=/usr/bin:/bin): **686 OK (skipped=7, rc 0)** — exactly the
  canonical external-condition classification (da27c0 archive not
  present ×1; production codex toolchain not on PATH ×5; smoke artifacts
  not present ×1); no new unexplained skip.
- `git diff --check`: CLEAN (base → successor).

No intermediate failure occurred in this session: every gate above is a
preserved FIRST result.

## 7. Historical evidence preservation

Nothing was modified or rewritten in: the historical `68e3b082…` audit
evidence; prior Auditor-A/B archives; the prior parity-invalid R0 record;
the prior remediation handoff archive. Carried forward EXACTLY, unchanged
(this session's nonblocking evidence limitation inherited from the prior
remediation session):

`INTERMEDIATE_FIRST_FULL_SUITE_LOG_OVERWRITTEN_IN_PRIOR_REMEDIATION_SESSION / FAILURE_CENSUS_PRESERVED / HISTORICAL_ARCHIVE_IMMUTABLE`

The missing historical intermediate log was NOT recovered and is NOT
claimed to exist.

## 8. Status and next route

`AUCDEV_010_RB001_EXACT_LAUNCH_BINDING_SUCCESSOR_CORRECTION_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK_AND_FRESH_AUDIT`

- The new product successor `d77333e86aa091d2ac003e9a2ad26c88dff56aeb` —
  NOT `ecfece1830b44012cad3f46ab235bea9335fdeb7` — is the ONLY candidate
  that may later be considered for a fresh A/B package, subject to
  Control Room readback. The prior candidate is recorded as
  `SUPERSEDED_AS_FRESH_AUDIT_TARGET_BY_RB001_EXACT_BINDING_SUCCESSOR`
  (supersession of a fresh-audit TARGET POINTER, not a qualification
  verdict and not failed qualification evidence; `ecfece1…` remains
  valid historical implementation evidence for its own bytes).
- Status remains `REMEDIATION_IMPLEMENTED / AWAITING_FRESH_AUDIT`
  vocabulary: no audited finding is closed, qualified or PASS; R-B002 /
  R-B003 / R-B004 remain exactly as published under the same status.
- `QUALIFICATION_READINESS = BLOCKED`; `QUALIFICATION = NONE`;
  `INSTALLATION = NONE`; the evidence-parity defect
  (`BOOTSTRAP_EVIDENCE_PARITY_INVALID`;
  `AUDITOR_B_EXTERNAL_TOOLING_METHODOLOGY_INPUT_PRESENT`) stands
  unchanged as a future fresh-audit harness requirement.
- No fresh A/B audit package was prepared or executed in this session.
- Model engagements this session: ZERO.
- Immediate next action: INDEPENDENT CONTROL ROOM READBACK of this
  successor-correction publication (verify the two-commit fast-forward
  chain `b04aa60…` → product successor `d77333e…` → this governance
  publication; RED/GREEN evidence and handoff archive); THEN — only if
  accepted — ONE fresh final A/B package preparation against
  `d77333e…` with a separate explicit operator execution authority, in an
  execution environment that prevents
  `AUDITOR_B_EXTERNAL_TOOLING_METHODOLOGY_INPUT_PRESENT`.
