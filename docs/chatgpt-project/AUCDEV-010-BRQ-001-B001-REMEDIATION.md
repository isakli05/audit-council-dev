# AUCDEV-010 BRQ-001 — B-001 Checkpoint-Immutability Bounded Remediation — Canonical Record

Publication date: 2026-09-12 (Europe/Istanbul). Canonical base: `5f40c641c5a110086a49811503c580bf7cd6dabc` (the S4/S5 + R0 reconciliation publication commit; sole parent `f1873d74d1142e718f7a791da3bd20ebb1a2d991`; tree `7a8820ae022524ab6cc3abcefcfa3eee11f83b2c`; skill tree `c01b8e690eb19f474e4284be2290c44459571dfe`; live GitHub `master` verified EXACT at remediation start). Base canonical blobs verified EXACT: CURRENT `376e118f69a796fdce51a5f61f6027d9084302c2`, BACKLOG `7c627db125ecb881d1ef461476a65df6d4c65be1`, QUALIFICATION-HISTORY `d072f808eba61213759fe5a62c7535d1d64057a0`, R0 report `0a5c7cf4d7b86bedb2652448af529eac764013fd`, RUNBOOK `cf65cf17990d1710315dc984227e8c0d47869ab0`, UPDATE PROTOCOL `42955b85710f09579cd0fd9174d042de231d060d`. Parallel records: CURRENT history record 37; BACKLOG AUCDEV-010 history record 40.

Role boundary: THIS remediation was prepared by a narrowly scoped IMPLEMENTER that is NOT Auditor A, NOT Auditor B, NOT an independent auditor, NOT the Control Room, NOT a qualification authority and NOT an installation authority. THIS session implemented a fix only; it does NOT independently establish that B-001 is resolved. Because the candidate SHA changed, a FRESH INDEPENDENT RE-AUDIT IS REQUIRED. No external model/provider/auditor call was authorized or performed (zero model engagements consumed; budget remains 2 authorized / 2 used, both consumed by the historical S4/S5 first passes).

## 1. Remediation scope (exactly one finding)

- Finding: B-001 — severity HIGH; classification product defect; title (frozen artifact, exact) `Completed checkpoint and frozen-contract bytes can be replaced before a rejected transition`.
- Old audited target: candidate `c114afe6865d160259af3c4d8e647437b6bef332` (candidate tree `f6251a669b2a45876e8e0c925a5619f7cb31ed32`; candidate skill tree `c01b8e690eb19f474e4284be2290c44459571dfe`; binding version 9). B-001 on the old target remains UNRESOLVED HIGH / QUALIFICATION BLOCKING and remains authoritative for that old target.
- No other finding (A-01/A-02/B-003; A-04/B-002; A-05/B-005; A-14/B-006; A-13/B-007; any other A-*/B-*; historical F-A2–F-A13) is claimed remediated, disposed of, or altered by this record.

## 2. Root cause (independently confirmed against exact base source)

`state_store.transition` correctly rejects same-phase/backward transitions (`ti <= ci`: completed phases are immutable). The defect was ordering in the CLI layer:

- `cmd_freeze_contract` (base `skill/scripts/audit_council.py`): `_read_stdin_artifact` staged stdin bytes DIRECTLY to the canonical `02-audit-contract.json`, then destination bytes were written, the `checksums.sha256` entry replaced, the `02-audit-contract.sha256` sidecar rewritten, and `01-repository-state.json` contract identity updated — ALL BEFORE `state_store.apply_transition(run_dir, "CONTRACT_FROZEN")` decided eligibility.
- `cmd_advance`: stdin staged directly to the canonical phase artifact, `record_phase_skips` persisted, and the artifact checksum recorded — ALL BEFORE `apply_transition` decided eligibility.

Consequence (mechanically reproduced on the exact base, zero model calls): a deterministically rejected same/backward transition still replaced the completed checkpoint's canonical bytes, checksum binding and sidecar, and `resume-check` / `verify-checksums` then PASSED with the replacement bytes because the replaced checksum entries legalized them.

## 3. RED reproduction (deterministic, non-secret, zero model calls)

Exact commands, hashes, exit codes and before/after identity matrices are preserved in the implementer handoff archive (delivered out-of-band to Control Room with this publication; its identity is recorded in the operator handoff, not in this commit). Summary, all against live worktree checkout of exact base `5f40c641`:

- RED-1 (repeated freeze-contract): valid freeze, then a repeat freeze with a DIFFERENT schema-valid stdin contract. Command failed (exit 1, `phase CONTRACT_FROZEN is already at or beyond CONTRACT_FROZEN; completed phases are immutable`) — yet base code REPLACED `02-audit-contract.json`, `02-audit-contract.sha256`, and the `checksums.sha256` entry for the contract; `resume-check` exit 0 with the replacement bytes.
- RED-2 (same-phase advance): after `OPUS_INDEPENDENT_COMPLETE`, a repeat advance to the same phase with DIFFERENT valid stdin bytes. Command failed (exit 1, same class) — yet base code REPLACED `10-opus-independent.json` and its checksum entry; `resume-check` exit 0 with the replacement bytes.
- RED-3 (backward advance): backward advance to the completed `CONTRACT_FROZEN` with DIFFERENT valid stdin contract bytes. Command failed (exit 1) — yet base code REPLACED `02-audit-contract.json` and its checksum entry (the sidecar is freeze-path-only and was untouched, as expected for the advance path).

## 4. Implementation (Commit 1 — remediated candidate)

Implemented invariant: ALL transition eligibility conditions determinable from existing run state + requested target + requested skip/adjudication semantics are validated successfully BEFORE any canonical checkpoint destination byte is staged/replaced or any completed-checkpoint identity record is updated.

- `skill/scripts/state_store.py`: NEW `check_transition(run_dir, target, *, adjudication_skipped=None, prospective_skips=None)` — a PURE eligibility preview that applies the SAME authoritative `transition()` rules (forward-only order, adjudication-skip rules, LEDGER_COMPLETE, explicit artifact-phase skip records) with zero mutation (no state save, no attempt accounting, no skip persistence); `prospective_skips` are validated by the SAME `_merged_skip_entries` helper now shared with `record_phase_skips` (behavior-identical refactor) and admitted into the in-memory state copy only.
- `skill/scripts/audit_council.py`: `cmd_freeze_contract` calls `state_store.check_transition(run_dir, "CONTRACT_FROZEN")` before stdin is consumed or any canonical byte is staged; `cmd_advance` calls `check_transition` (with the prospective artifact-name-derived adjudication flag and prospective skips) before stdin staging, skip persistence or checksum recording. On rejection both commands perform ONLY the pre-existing normal failed-attempt accounting (`bump_phase_attempt`) and fail; the terminal `apply_transition` remains the committing authority. No second phase-order/skip rule set exists in `audit_council.py` (the authoritative `ti <= ci` rule remains solely in `state_store.transition`). Unweakened: forward-only semantics, explicit phase-skip requirements, adjudication-skip rules, schema validation, fingerprint checks, environment gates, checksum verification, attempt accounting.
- Tests (authorized files only): `skill/tests/test_resume.py` — strengthened `test_advance_rejects_backward_transition` and NEW `test_repeated_freeze_rejected_preserves_frozen_contract`, `test_same_phase_advance_rejected_preserves_checkpoint` (canonical bytes, checksum binding, sidecar, repository-state identity byte-identical after rejection; `resume-check` ok; only failed-attempt accounting changes state.json). `skill/tests/test_state_store.py` — NEW `TestCheckTransition` (preview agrees with apply on rejections; preview writes nothing; prospective skips evaluated without persisting; invalid/duplicate prospective skips rejected identically).
- Changed paths (exactly four): `skill/scripts/audit_council.py`, `skill/scripts/state_store.py`, `skill/tests/test_resume.py`, `skill/tests/test_state_store.py`. 293 insertions / 26 deletions.

## 5. Test evidence (preserved verbatim in the handoff archive)

- Focused: `python3 -m unittest discover -s skill/tests -p 'test_resume.py'` — 11 tests OK; `-p 'test_state_store.py'` — 18 tests OK. Both observed RED (correct assertion/AttributeError failures) on base code BEFORE the fix, GREEN after.
- Full deterministic suite `python3 -m unittest discover -s skill/tests`: base 579 tests OK (pre-existing ResourceWarnings only); remediated candidate 584 tests, 1 failure, classified below.
- CLASSIFIED IMPLEMENTATION RESIDUAL (factually reported; NOT silently remediated because its file is outside this remediation's authorized test paths): `test_v101_hardening.py::TestFingerprintInvariant::test_finalize_cannot_consume_mismatched_final_artifact` asserts the `INVALID_ARTIFACT` message for an advance that is an inherently INELIGIBLE multi-phase jump (`OPUS_INDEPENDENT_COMPLETE -> FINALIZED` passing over LEDGER_COMPLETE and ADJUDICATION_COMPLETE without skip records). Base code surfaced the artifact-validation error first only because validation preceded the state machine; under the mandated eligibility-first ordering the same command is now (correctly) rejected EARLIER with the state-machine error, before any staging. The protected property still holds (command fails, exit != 0, mismatched final artifact never consumed, nothing staged); the fingerprint machinery itself is unchanged and independently covered by passing tests (`test_contract_fingerprint_mismatch_rejected`, `test_resume_refuses_mismatched_completed_artifact`, `test_invalid_output_diagnosable_not_canonical`). Whether to adjust that single assertion (a one-line test-only change) is a Control Room scope decision flagged for the readback; this residual is a FRESH-AUDIT REVIEW INPUT.

## 6. Identity model (two commits from a fresh detached worktree at exact base)

- Commit 1 (REMEDIATED CANDIDATE; sole parent `5f40c641c5a110086a49811503c580bf7cd6dabc`): **NEW_CANDIDATE_SHA `d88d469229f65ca764312cad447b89d399dcb7dd`**; tree `c4d7db30ca2b4605369c4089272933e2a0e06ab0`; **NEW skill tree `7e849656cc7193b3793b143b1937ed0fbafe687e`**; changed paths exactly the four authorized product/test paths; subject `fix: preserve completed checkpoints on rejected transitions`. THIS is the ONLY runtime candidate a future fresh re-audit may target.
- Commit 2 (GOVERNANCE RECORD; sole parent `d88d469229f65ca764312cad447b89d399dcb7dd`; subject `docs: record AUCDEV-010 B-001 remediation`): changes exactly `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`, `docs/chatgpt-project/AUCDEV-BACKLOG.md` and this NEW report. The governance commit is NOT the runtime audit target.

## 7. Governance disposition (published exactly)

`AUCDEV_010_B001_REMEDIATION_IMPLEMENTED_AND_PUBLISHED_FOR_CONTROL_ROOM_READBACK / B001_REMEDIATION_IMPLEMENTED / B001_AWAITING_FRESH_REAUDIT / OLD_HIGH_B001_REMAINS_AUTHORITATIVE_FOR_OLD_TARGET_c114afe / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE / MODEL_ENGAGEMENTS_2_AUTHORIZED_2_USED_UNCHANGED / NO_NEW_AUDIT_OR_MODEL_AUTHORITY`

This means ONLY: code remediation implemented; deterministic tests completed as reported (including the one classified residual above); exact new candidate identity established; governance transition published. It does NOT mean: B-001 independently resolved; candidate PASS; qualification ready; qualified; installed.

- AUCDEV-010 remains OPEN / P1 / BLOCKED. Blockers: (1) FIRST_PROVEN_QUALIFIED_INSTALLED_PREDECESSOR NOT YET ESTABLISHED; (2) B-001 remediation implemented but AWAITING FRESH REAUDIT — the old HIGH finding remains authoritative for old target `c114afe…` and qualification readiness stays BLOCKED until a fresh independent audit of `d88d469229f65ca764312cad447b89d399dcb7dd` is separately authorized and completed.
- The old S4/S5/R0 evidence remains immutable historical evidence for old candidate `c114afe…`; the old model budget remains 2 authorized / 2 used; the old S4/S5 authority is NOT reused or reopened; NO new audit/model authority is created by this record.
- Runtime/install unchanged: installed source remains `8ae33444f349ce73c1359b963722e2d16acba630` with installed qualification provenance NOT ESTABLISHED; the remediated candidate is NOT installed.

## 8. Immediate next action

INDEPENDENT CONTROL ROOM READBACK OF THIS B-001 REMEDIATION (verify the two-commit parent chain `5f40c641 -> d88d4692 -> <governance commit>`, the four authorized Commit-1 paths, the three authorized Commit-2 paths, the NEW skill tree `7e849656…`, the RED/GREEN evidence in the handoff archive, and this recorded state). Only after that readback may Control Room define/authorize the FRESH independent audit of NEW_CANDIDATE_SHA `d88d469229f65ca764312cad447b89d399dcb7dd`. THIS session does NOT start, simulate or substitute for that re-audit.

## 9. Publication mechanics

- One remediation commit (authorized product/test paths only) + one governance record commit (the three authorized doc paths only), both from a fresh DETACHED worktree at exact base `5f40c641`; the operator's dirty/diverged working tree was neither used nor cleaned.
- Live `refs/heads/master` re-resolved EXACT (`5f40c641`) immediately before exactly ONE fast-forward push of the governance commit (no force, no retry, no tags, no wildcard); readback from GitHub performed after push.
- QUALIFICATION-HISTORY, RUNBOOK, UPDATE PROTOCOL, architecture summary, PUBLIC-CONTRACT, SKILL.md, protocols, schemas, known-limitations, unrelated tests, S4/S5/R0 reports, old evidence archives and the installed Audit Council were NOT modified.
- Zero model/frontier/provider executions; zero auditor executions; zero qualification/installation decisions; zero frozen-artifact changes; zero credential reads/hashes by this session.
