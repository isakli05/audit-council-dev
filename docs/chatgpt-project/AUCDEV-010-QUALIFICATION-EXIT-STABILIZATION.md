# AUCDEV-010 — Qualification Exit Stabilization — Canonical Implementation Record

Published: **2026-09-13** (Europe/Istanbul; implementation session).

## 0. Session role and authority

This session was an IMPLEMENTATION session ONLY — the consolidated
qualification-exit stabilization candidate. It was NOT Auditor A, NOT
Auditor B, NOT the Control Room, NOT a qualification authority, NOT an
installation authority, and it performed ZERO model/frontier/provider
inference (no `/audit-council`, no Claude Opus, no GPT-5.6 Sol, no
codex-cli inference, no other frontier/model/provider call). No original
finding is independently closed by this record; no candidate PASS,
qualification readiness, qualification or installation is claimed.

Authority recorded by the brief and carried verbatim into the session
record:

`AUCDEV_010_C8DDA1D0_R0_PUBLICATION_READBACK_ACCEPTED_WITH_EVIDENCE_RESIDUALS / LIVE_HEAD_f8a403a7f48d4cd1ce919338ef9dff7cdc7bfb30 / CANONICAL_R0_STATE_VERIFIED / AUDITOR_A_DO_NOT_QUALIFY / AUDITOR_B_INCOMPLETE / CURRENT_HIGH_FINDINGS_PRESENT / ALL_21_FINDINGS_REQUIRE_DISPOSITION / R0_PUBLICATION_PREPUSH_CAPTURE_LABEL_BINDING_NONCONFORMITY_NONBLOCKING / R0_PUBLICATION_PUSH_COMMAND_TEXT_REFSPEC_NONCONFORMITY_NONBLOCKING / QUALIFICATION_EXIT_STABILIZATION_AUTHORIZED / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

Live bootstrap (fail closed, verified before any edit): live GitHub
`refs/heads/master` = `f8a403a7f48d4cd1ce919338ef9dff7cdc7bfb30` (tree
`b9aeeaf8229db9a73b8d14e4374c74ca01fdce2d`; sole parent
`6be8cd6279b9bda8a146850b971354fbe5514fc5`); audited target
`c8dda1d0da81a4063b53cae339c7f6a201270bae` (tree `a1f37f25…`, skill tree
`2f69998e…`) verified; the base skill tree is byte-identical to the
audited target's skill tree; CURRENT/BACKLOG/R0/RUNBOOK/UPDATE
PROTOCOL/PUBLIC-CONTRACT fetched from the exact base; all 21 finding
identities mechanically extracted from the canonical R0 report;
qualification readiness BLOCKED / qualification NONE / installation NONE
verified. Work performed in a fresh DETACHED worktree at the exact base;
the operator's working tree was not touched.

## 1. Candidate identity (THE ONLY candidate for the next fresh audit)

| Identity | Value |
|---|---|
| QUALIFICATION_EXIT_CANDIDATE_SHA | `d2f7c89b63f63fd2a13005ffe4637494feb9d521` |
| Candidate tree | `11bf3f919950aa2c43c30be457ec76929d1a9400` |
| Candidate skill tree | `021aac6f03ad7b3655a9fcc444dd984f763b1137` |
| Sole parent | `f8a403a7f48d4cd1ce919338ef9dff7cdc7bfb30` |
| Subject | `fix: stabilize qualification trust boundaries` |
| Changed paths | 25, all finding-linked (see §3); no unrelated path |

This candidate SHA — NOT this governance commit — is the only candidate
for the next fresh audit. Nothing transfers from the c8dda1d0 audit.

## 2. Deterministic gates (exact, observed this session)

- Full deterministic suite (`python3 -m unittest discover -s skill/tests`):
  **625 tests OK — 0 failures, 0 errors, 0 skips** (natural posture; three
  full runs including the final gate after the last change).
- Isolated clean-environment run (fresh HOME/XDG/AUDIT_COUNCIL_CACHE_HOME/
  AUDIT_COUNCIL_ENV_ROOT, no host codex/login/network dependence):
  **625 tests OK — 0 failures, 0 errors, 7 skips** (every skip an
  explicitly classified external condition: bwrap, production codex
  toolchain, DNS, archived run evidence). Baseline before the
  stabilization, the same isolated posture produced **58 failures / 1
  error / 2 skips** of 584 — the F-A-06 non-reproducibility, captured.
- `git diff --check` — CLEAN (base→candidate).
- `audit_council.py describe --json` validates against
  `public-contract.schema.json` — PASS.
- RED evidence against the pristine audited base tree: the new
  stabilization regression module (`skill/tests/test_qx_stabilization.py`,
  41 tests) run against the base skill tree = **18 failures + 18 errors**
  (including the sandbox /proc exposing 593 host processes on the base);
  GREEN on the candidate. Handoff archive carries the full outputs.
- No intermediate failure hidden: the tier-4/test fixture rewrites and one
  transient ordering-sensitive failure (observed once in a combined module
  run, absent in the immediate rerun and all full-suite runs) are recorded
  in the archive evidence.

## 3. Work-package implementation summary (exact changed paths)

- QX-1 (F-A-01, F-A-02, F-A-03, B-001, B-002, B-003):
  `skill/scripts/codex_sandbox.py` (PID+IPC+UTS unshare, net shared by
  design; `--clearenv` + explicit HOME/PATH/TERM/LANG; preflight with no
  repo-root/home probe writes, argv-vector probes, run's-own codex binary,
  `/proc`-root-escape probe; `blind_paths` masking),
  `skill/scripts/codex_runner.py` (blind-path wiring + job-record
  blindness record; preflight codex_bin; stage gate consult),
  `skill/PUBLIC-CONTRACT.md` + `skill/scripts/audit_council.py`
  (PUBLIC_CONTRACT truthfulness), `skill/tests/test_tier4_da27c0.py`,
  `skill/tests/fixtures/fake_codex.py`.
- QX-2 (F-A-08, F-A-09, F-A-11, B-004, B-007):
  `skill/scripts/repo_fingerprint.py` (fingerprint v2: `-uall`
  content-addressed untracked inventory, dirty-worktree byte map,
  v1-normalizing diff; `identity-manifest` + `verify-manifest-files`),
  `skill/scripts/env_binding.py` (fingerprint_algorithm 2 + legacy-1
  byte-exact verification; `skill/schemas/env-binding.schema.json`),
  `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md` (truthful candidate review
  basis), `skill/tests/test_env_binding.py`.
- QX-3 (F-A-04, F-A-05, F-A-10, B-005): `skill/scripts/state_store.py`
  (SKIPPABLE_PHASES single source; sanity-check refusal of schema-invalid
  skip records; bound+consumed skip records; per-run flock
  `run_state_lock`; `STAGE_ENTRY_PHASE` + `check_stage_launch`),
  `skill/scripts/audit_council.py` (CLI skip vocabulary + bound
  recording), `skill/schemas/state.schema.json` (additive bound-skip
  fields), `skill/scripts/codex_runner.py`, `skill/tests/test_state_store.py`.
- QX-4 (F-A-12, B-006, B-008, F-A-13):
  `skill/protocols/evidence-policy.md`, `skill/prompts/codex-independent.md`,
  `skill/prompts/codex-cross-examine-opus.md` (v2 `line_ranges` alignment),
  `skill/scripts/first_pass_validator.py` (NEW generic validator),
  `skill/scripts/audit_council.py` (list-return contract), contract/
  limitations truthfulness for the evidence-visibility narrowing.
- QX-5 (F-A-06, F-A-07): `skill/SKILL.md` (fail-closed hook command),
  `skill/README.md` (hooks/ in documented install contents; fail-closed
  semantics), `skill/tests/test_codex_runner_mock.py`,
  `skill/tests/test_wait_lifecycle_v102.py`,
  `skill/tests/test_env_lifecycle.py` (hermetic fixture channel + base
  env), `skill/tests/test_qx_stabilization.py` (NEW),
  `skill/schemas/public-contract.schema.json`.

## 4. All 21 proposed dispositions (summary)

17 FIXED_AND_DETERMINISTICALLY_VERIFIED (F-A-01…F-A-11, F-A-13, B-003,
B-005, B-006, B-007, B-008); 4 SUBSUMED_BY_ROOT_CAUSE_WITH_PROOF (B-001,
B-002, B-004 — same rewrites as their A-family roots; F-A-12's
executable-policy half — root cause B-006 divergence eliminated);
0 REJECTED_WITH_COUNTER_EVIDENCE; 1 PROPOSED_ACCEPTED_RESIDUAL —
F-A-12's visibility-class half (EvidenceStore not wired into production
stages; all product claims narrowed truthfully) —
**REQUIRES_CONTROL_ROOM_OPERATOR_ACCEPTANCE**, NOT closed by the
implementer. Full per-finding detail (paths, proof identity, held
invariant, remaining uncertainty, fresh-review requirement): the POST
matrix in the handoff archive; every row flags fresh external audit
review as required.

## 5. Proposed residuals and carried publication-evidence residuals

1. F-A-12 visibility-class half — REQUIRES_CONTROL_ROOM_OPERATOR_
   ACCEPTANCE (see §4).
2. Out-of-scope observation, NOT a finding disposition:
   `skill/eval/tier1_harness.py` retains a `/usr/bin/python3` hard-code
   (QX-5 invariant 5 would prefer a mechanically resolved interpreter,
   but `skill/eval/**` is outside the task's permitted product surfaces;
   left unchanged; flagged for Control Room routing).
3. Publication-evidence residuals carried forward APPEND-ONLY, per the
   brief §15 — the old publication archive was NOT mutated or repacked
   and no standalone correction cycle was created:
   - `R0_PUBLICATION_PREPUSH_CAPTURE_LABEL_BINDING_NONCONFORMITY` — the
     immutable publication handoff's `20-prepush-live-ref.txt` is labeled
     prepush but shows the already-published `f8a403…` ref rather than
     required base `6be8cd…`, while claiming EXACT MATCH. Classification:
     COMPLETENESS LIMITATION / EVIDENCE CHRONOLOGY / LABEL-BINDING.
   - `R0_PUBLICATION_PUSH_COMMAND_TEXT_REFSPEC_NONCONFORMITY` — the
     archived textual command in `21-push-evidence.txt` is malformed
     relative to a valid explicit Git refspec, while the captured Git
     output and live GitHub state establish the final fast-forward
     result. Classification: COMPLETENESS LIMITATION / EVIDENCE
     COMMAND-RECORD PRECISION.
   No intent is speculated; the exact prepush chronology and exact command
   string are NOT claimed to be independently established by that archive.

## 6. Qualification state (unchanged by this record)

- AUCDEV-010: OPEN / P1 / BLOCKED.
- Event `AUCDEV-010-BRQ-001-0CCF9A82-20260912-01` (binding v2): closed;
  engagements 2/2; both single-use authorities CONSUMED.
- Qualification readiness: **BLOCKED**. Qualification: **NONE**.
  Installation: **NONE**. Installed source remains
  `8ae33444f349ce73c1359b963722e2d16acba630` (unchanged; nothing was
  installed).
- The next fresh A/B audit is justified only against
  `d2f7c89b63f63fd2a13005ffe4637494feb9d521` and must evaluate all five
  work packages and all 21 prior finding dispositions. Deterministic PASS
  is not qualification; model agreement is not proof; incomplete
  mandatory auditor coverage blocks readiness. The Control Room's
  root-qualification exit rule (§16 of the brief) is NOT claimed achieved.

## 7. Publication

Exactly TWO commits from the detached worktree: Commit 1 (the candidate,
sole parent `f8a403a7…`, product/tests/contract/documentation
finding-linked paths only) and Commit 2 (THIS governance record: CURRENT,
BACKLOG, and this NEW report; QUALIFICATION-HISTORY untouched — no audit
or qualification event occurred). Exactly ONE explicit fast-forward
refspec push after a final live-master EXACT re-check; stage-accurate
prepush/push/postpush evidence captured in the handoff archive.
