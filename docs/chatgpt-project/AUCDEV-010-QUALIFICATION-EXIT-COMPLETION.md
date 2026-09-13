# AUCDEV-010 — Qualification Exit Completion — Canonical Implementation Record

Published: **2026-09-13** (Europe/Istanbul; completion implementation session).

## 0. Session role and authority

This session was a narrowly scoped COMPLETION IMPLEMENTER ONLY — it closed
the Control-Room-readback blockers left by the qualification-exit
stabilization, BEFORE the final external A/B re-audit. It was NOT Auditor
A, NOT Auditor B, NOT the Control Room, NOT a qualification authority,
NOT an installation authority, and it performed ZERO model/frontier/
provider inference (no `/audit-council`, no Claude Opus, no GPT-5.6 Sol,
no codex-cli inference, no other frontier/model/provider call). No original
finding is independently closed by this record; no candidate PASS,
qualification readiness, qualification or installation is claimed.

Authority recorded by the brief and carried verbatim into the session
record:

`AUCDEV_010_QUALIFICATION_EXIT_STABILIZATION_READBACK_PARTIALLY_ACCEPTED / LIVE_HEAD_12187b60e0f2bc0d9541c241696203c4597654f4 / CANDIDATE_d2f7c89b63f63fd2a13005ffe4637494feb9d521_MECHANICALLY_SUPPORTED / FULL_DETERMINISTIC_SUITE_625_GREEN / MAJOR_QX1_QX2_QX3_QX4_QX5_IMPLEMENTATION_SUPPORTED / F_A12_VISIBILITY_RESIDUAL_NOT_ACCEPTED / POST_MATRIX_DISPOSITION_CARDINALITY_NONCONFORMITY / TRANSIENT_TEST_ERROR_COMPLETENESS_RESIDUAL / TEST_RESOURCEWARNING_HYGIENE_RESIDUAL / CURRENT_NEXT_OBJECTIVE_STALE_POINTER / STABILIZATION_PRECOMMIT_RECORD_POSTHOC_LABEL_RESIDUAL / FINAL_EXTERNAL_REAUDIT_NOT_YET_AUTHORIZED / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

Live bootstrap (fail closed, verified before any edit and re-verified
before staging): live GitHub `refs/heads/master` =
`12187b60e0f2bc0d9541c241696203c4597654f4` (tree
`dff7df8b679427c4c86cf57cebd13c6c0edf41f9`; sole parent
`d2f7c89b63f63fd2a13005ffe4637494feb9d521`); candidate tree
`11bf3f919950aa2c43c30be457ec76929d1a9400`, skill tree
`021aac6f03ad7b3655a9fcc444dd984f763b1137`, candidate parent
`f8a403a7f48d4cd1ce919338ef9dff7cdc7bfb30` — all EXACT. The mandated
documents were fetched from the exact live HEAD and the candidate skill
files from the exact candidate. Work performed in a fresh DETACHED
worktree at the exact base; the operator's working tree was not touched;
the supported d2f7 QX-1..QX-5 implementations were not reopened or
redesigned.

## 1. Completion successor identity (THE ONLY target for the final fresh audit)

| Identity | Value |
|---|---|
| QUALIFICATION_EXIT_COMPLETION_CANDIDATE_SHA | `4fb4025a66d24432aa4b4ea570cc00b66a730f68` |
| Candidate tree | `7ef4ce40ef21ca60e02da37e9ffd0e48d5b89b22` |
| Candidate skill tree | `541a5cfc0f25ba4c2244abf1d6196feb04d310ad` |
| Sole parent | `12187b60e0f2bc0d9541c241696203c4597654f4` |
| Subject | `fix: close qualification-exit residuals` |
| Changed paths | 10, all mechanically required for C1–C6 (below) |

This SHA supersedes `d2f7c89b…` as the ONLY candidate for the next fresh
audit. d2f7 is NOT independently closed and is NOT called re-audited; it
remains historical implementation evidence (QX-1..QX-5) inside this
successor's chain. Its history was not rewritten; the old stabilization
evidence archive was not mutated.

Changed paths (exactly): `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md` (append-only
claim-reconciliation item 43), `skill/PUBLIC-CONTRACT.md`,
`skill/eval/tier1_harness.py`, `skill/scripts/audit_council.py`,
`skill/scripts/codex_runner.py`, `skill/scripts/evidence_store.py`,
`skill/scripts/render_report.py`, `skill/tests/test_eval_framework.py`,
`skill/tests/test_qx_stabilization.py`, and NEW
`skill/tests/test_evidence_pipeline.py`.

## 2. Blocker closure summary (C1–C7)

- **C1 — F-A-12 one final disposition**: the former split (executable-policy
  half SUBSUMED + visibility-class half PROPOSED_ACCEPTED_RESIDUAL) is
  replaced by exactly ONE disposition for the whole finding:
  `FIXED_AND_DETERMINISTICALLY_VERIFIED` (both halves closed with proof;
  see §4 and the final matrix). No accepted residual; no split.
- **C2 — EvidenceStore/cache contract closure**: the ACTUAL production call
  graph was mechanically established FIRST (deliverable
  `EVIDENCESTORE-PRODUCTION-CALLGRAPH.md`, retained in the handoff): ZERO
  production importers of EvidenceStore; the public claim `cached evidence
  reused when valid` (budgets.DEFAULT_BUDGETS + describe + PUBLIC-CONTRACT
  governor text) had NO runtime implementation; EvidenceStore IS the
  intended mechanism (AUCDEV-017 P2/OPEN scopes exactly this integration;
  no competing cache exists). Closure = bounded integration (NOT a
  redesign; the §5 STOP condition was assessed and NOT triggered):
  - `evidence_store.py`: lifecycle-owned wiring layer — `run_barrier_state`
    (barrier open ⇔ authoritative phase ≥ CODEX_INDEPENDENT_COMPLETE,
    fail-closed), `open_run_store`, `frozen_run_identity` (state.json
    fingerprint + binding digest, fail-closed), `serve_run_evidence`
    (production consumption point: full visibility + freshness law PLUS
    CACHEABLE revalidation against the frozen identity —
    `stale_not_reusable` denials are access-logged), record builders for
    the three production record shapes, `find_records` lookup, additive
    `get(reuse_gate=)` and content-key dedup (produced_at-independent).
  - `audit_council.py`: prepare records every staged evidence file
    (SHARED_MECHANICAL, FRESH_REQUIRED — retained for provenance/access
    accounting, never served from cache); advance records the AUDITOR_PRIVATE
    identity manifest for each checkpointed first-pass artifact
    (`10-opus-independent.json` → OPUS, `20-codex-independent.json` →
    CODEX; payload is {path, sha256, bytes} only — the anti-conclusion
    guard keeps finding-shaped substance OUT of the store by design);
    unbound v1-era runs (env-gate migration precedent) record
    `unbound_run_no_record` / `unbound_run_no_evidence_store` honestly.
  - `codex_runner.py`: stage-launch wiring — for the independent phase the
    OPUS private manifest is served to consumer CODEX through the store and
    MUST be denied pre-barrier; any serve ABORTS the launch (defense in
    depth behind B-003 sandbox masking — the cache can never become a
    first-pass-barrier bypass); every launch PUTs its stage-input manifest
    (prompt/schema/codex-binary identities) and REUSES a prior one only
    while still valid (REUSE_WHEN_VALID mechanically true); all store
    failures abort the launch with ZERO model attempts consumed.
  - `render_report.py`: "Evidence store provenance" section (records by
    visibility/freshness class, access decisions by reason; honest absence
    statement) — provenance survives report generation.
  - Claims reconciled EVERYWHERE they could be read: describe
    known-limitations + evidence_staging capability text, PUBLIC-CONTRACT
    limitation/governor/staging text, root KNOWN-LIMITATIONS item 43
    (append-only supersession of the not-wired halves of items 24/38 for
    this successor; remaining boundaries stated: payloads under
    `<run>/evidence/objects/` remain readable by in-root readers; store
    law governs the STORE API; canonical phase artifacts remain
    authoritative; interactive-side recording remains protocol-enforced).
  - Production-path tests (NEW `test_evidence_pipeline.py`, 18 tests):
    real prepare → staged-evidence records; real advance → first-pass
    manifest + pre-barrier denial + post-barrier serve; real
    `codex_runner start` (fake codex) → pre-barrier peer denial + stage
    input record; retry-with-identical-inputs → REUSED (same id);
    changed prompt → NOT reused (new id); changed fingerprint/binding →
    `stale_not_reusable` denial; FRESH_REQUIRED denial through the
    production serve path; unbound-run honesty; report provenance;
    describe/MD claim reconciliation.
- **C3 — tier1 interpreter hard-code**: `/usr/bin/python3` replaced by
  `resolve_python()` — deterministic, mechanically probed CPython-3 ladder
  (current interpreter → `/usr/bin/python3` → `which python3`), skipping
  AppImage transient self-mounts (the documented host/AppImage concern,
  preserved by `_is_appimage_mount`), verified by a no-side-effect
  identity probe; unresolvable ⇒ explicit `Tier1InterpreterError`, never a
  silent unrelated runtime. `test_eval_framework.py` routed through it;
  five new contract tests (order, AppImage skip, first-verified-wins,
  non-CPython/non-py3 rejection, explicit failure).
- **C4 — transient/Resource hygiene**: the historical transient ERROR
  (~2026-09-13T12:18:24Z, traceback not retained; nine immediate reruns
  and three full-suite runs green) is PRESERVED as historical fact — no
  traceback invented, no root cause claimed. All NINE unclosed-file
  ResourceWarnings in `test_qx_stabilization.py` fixed with context
  managers. Gates: `PYTHONWARNINGS=error::ResourceWarning` focused run =
  PASS (41/41); 20/20 consecutive serial focused runs; 12/12 bounded
  concurrent repetitions (3 rounds × 4 parallel), every run executing the
  full 41-test module; NO unexplained transient error recurred in any of
  the 33 focused runs, 2 natural full-suite runs, or 2 isolated-posture
  runs this session; no failed intermediate run occurred (nothing hidden).
- **C5 — regression provenance**: `FINAL-REGRESSION-PROVENANCE.md`
  (handoff): final modules vs `c8dda1d0` / `d2f7c89b` / completion —
  stabilization module RED at base (19F+18E of 41, observed this session
  with the final module overlaid), green at d2f7 and completion; the two
  NEW capability test surfaces classified STATIC ABSENCE at base/d2f7
  (AttributeError on the absent wiring/resolver — no fabricated RED);
  the unchanged library module green on all three trees. Both historical
  RED records (40-test summary; 41-test full execution) remain preserved
  as historical evidence, not re-issued.
- **C6 — 21/21 final dispositions**:
  `FINDING-DISPOSITION-MATRIX-FINAL.md` (§4 below): 21 IDs, 21 rows, each
  EXACTLY ONE disposition — 17 FIXED_AND_DETERMINISTICALLY_VERIFIED,
  4 SUBSUMED_BY_ROOT_CAUSE_WITH_PROOF, 0 REJECTED, 0 accepted residual;
  F-A-12 single disposition FIXED. Every row still requires fresh
  independent external audit review.
- **C7 — canonical pointer corrected**: the CURRENT `Next runtime
  objective` no longer points at the c8dda1d0 fresh-first-pass/R0
  readback; it now requires (in order) INDEPENDENT CONTROL ROOM READBACK
  OF THIS COMPLETION SUCCESSOR, and only after that readback, PREPARATION
  OF THE FINAL FRESH A/B RE-AUDIT of `4fb4025a…`. History record 42 was
  NOT rewritten; THIS record appends history record 43 (CURRENT) /
  46 (BACKLOG AUCDEV-010).

## 3. Deterministic gates (exact, observed this session)

- Full deterministic suite natural posture ×2: **648 tests OK — 0
  failures, 0 errors, 0 skips** (98.6 s / 97.5 s).
- Isolated clean-environment posture (fresh HOME/XDG/
  AUDIT_COUNCIL_CACHE_HOME/AUDIT_COUNCIL_ENV_ROOT via `env -i`):
  **648 OK — 7 skips, every skip an explicitly classified external
  condition** (da27c0 archived evidence absent; production codex toolchain
  not on PATH ×5; smoke artifacts not present), verbatim reasons retained.
- Focused: evidence pipeline 18/18; evidence-store standalone 44/44; eval
  framework 32/32; state/runner/sandbox/fingerprint modules all OK;
  stabilization module 41/41 with ResourceWarning-as-error.
- `git diff --check` CLEAN (base → candidate).
- `audit_council.py describe --json` validates against
  `public-contract.schema.json` — no errors (contract change validated).
- Zero model/frontier/auditor calls.

## 4. Final 21-finding disposition matrix (exact counts)

F-A-01 FIXED · F-A-02 FIXED · F-A-03 FIXED · F-A-04 FIXED · F-A-05 FIXED ·
F-A-06 FIXED · F-A-07 FIXED · F-A-08 FIXED · F-A-09 FIXED · F-A-10 FIXED ·
F-A-11 FIXED · **F-A-12 FIXED (single disposition; the former proposed
accepted residual is CLOSED by the production wiring + claim
reconciliation above)** · F-A-13 FIXED · B-001 SUBSUMED (root F-A-01) ·
B-002 SUBSUMED (root F-A-02) · B-003 FIXED · B-004 SUBSUMED (root F-A-08)
· B-005 FIXED · B-006 FIXED · B-007 SUBSUMED (root F-A-11) · B-008 FIXED.

Counts: 17 + 4 + 0 = **21**; 0 accepted residual; no split dispositions.
Full per-row evidence anchors: `FINDING-DISPOSITION-MATRIX-FINAL.md`
(handoff archive).

## 5. Carried residuals (preserved, append-only; NOT finding dispositions)

1. `QX_STABILIZATION_PRECOMMIT_GATE_RECORD_POSTHOC_LABEL_NONCONFORMITY`
   (recorded by THIS completion per the brief): the OLD stabilization
   archive's `15-precommit-gates.txt` (file timestamp 2026-09-13T12:22:36Z)
   postdates both the candidate commit (12:11:35Z) and the archived push
   (12:16:19Z) — a post-hoc gate summary, not contemporaneous precommit
   capture. Classification: COMPLETENESS LIMITATION / EVIDENCE CHRONOLOGY
   / LABEL-BINDING. The old archive is NOT repacked or mutated; the
   independently verifiable final Git/test identities are NOT invalidated.
   THIS completion captured its stage evidence contemporaneously:
   precommit gates BEFORE commit (`15-precommit-gates.txt` written
   2026-09-13T13:19:35Z, before the candidate commit at
   2026-09-13T13:20:39Z = 16:20:39+03:00), prepush remote ref BEFORE
   push, executed push argv + output DURING push, postpush remote ref
   AFTER push — exact mtimes and the stage-accurate files are in the
   handoff.
2. R0 publication-evidence residuals (prepush label-binding;
   push-command text refspec) — carried forward unchanged, append-only.
3. Out-of-scope observations, unchanged: the historical transient ERROR
   (traceback not retained) preserved honestly in §2-C4.

## 6. Qualification state (unchanged by this record)

- AUCDEV-010: OPEN / P1 / BLOCKED. Event `AUCDEV-010-BRQ-001-0CCF9A82-
  20260912-01` closed; engagements 2/2 consumed; first-pass barrier OPEN.
- Qualification readiness: **BLOCKED**. Qualification: **NONE**.
  Installation: **NONE**. Installed source remains
  `8ae33444f349ce73c1359c963722e2d16acba630` (unchanged; nothing was
  installed).
- The final fresh A/B audit is justified only against
  `4fb4025a66d24432aa4b4ea570cc00b66a730f68` and must evaluate all five
  stabilization work packages, all 21 prior finding dispositions, and the
  completion closures. Deterministic PASS is not qualification; model
  agreement is not proof. NO auditor/model execution, addendum,
  adjudication, qualification or installation is authorized by this
  record.

## 7. Publication

Exactly TWO commits from the detached worktree: Commit 1 (the completion
successor `4fb4025a…`, sole parent `12187b60…`, the 10 product paths
above) and Commit 2 (THIS governance record: CURRENT, BACKLOG, and this
NEW report; QUALIFICATION-HISTORY untouched — no audit or qualification
event occurred). Exactly ONE explicit fast-forward refspec push after a
final live-master EXACT re-check; stage-accurate precommit/prepush/push/
postpush evidence captured contemporaneously in the handoff archive.
