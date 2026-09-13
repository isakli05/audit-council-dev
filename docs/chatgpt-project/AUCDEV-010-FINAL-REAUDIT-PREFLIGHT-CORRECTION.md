# AUCDEV-010 — Final Re-audit Preflight Correction — Canonical Record

Published: **2026-09-13** (Europe/Istanbul; final re-audit preflight
correction session).

## 0. Session role and authority

This session was a NARROW TEST/EVIDENCE CORRECTION IMPLEMENTER ONLY. The
qualification-exit completion implementation is SUBSTANTIALLY ACCEPTED
and was NOT reopened: QX-1..QX-5 were not reopened, EvidenceStore was
not redesigned, runtime/product behavior was not altered (the single
code change is two context-manager conversions inside one TEST file).
This session was NOT Auditor A, NOT Auditor B, NOT the Control Room, NOT
a qualification authority, NOT an installation authority, and it
performed ZERO model/frontier/provider/auditor inference (no
`/audit-council`, no Claude Opus, no GPT-5.6 Sol, no codex-cli
inference, no external model/provider call of any kind).

Control Room readback disposition recorded verbatim by the brief and
carried into this record:

`AUCDEV_010_QUALIFICATION_EXIT_COMPLETION_READBACK_PARTIALLY_ACCEPTED / LIVE_HEAD_c03d7a27f5f16f04b274ab3efbe394610c660a / CANDIDATE_4fb4025a66d24432aa4b4ea570cc00b66a730f68_MAJOR_COMPLETION_MECHANICS_SUPPORTED / EVIDENCESTORE_PRODUCTION_WIRING_SUPPORTED / FINAL_21_BY_21_DISPOSITION_CARDINALITY_SUPPORTED / F_A12_SINGLE_FIXED_DISPOSITION_SUPPORTED_PENDING_FRESH_AUDIT / RESOURCEWARNING_CLOSURE_GATE_FALSE_NEGATIVE / TEST_QX_STABILIZATION_TWO_UNCLOSED_FILE_SITES_CONFIRMED / CURRENT_B001_FINDING_LABEL_BINDING_NONCONFORMITY / CURRENT_INSTALLED_SOURCE_STATUS_SHA_TYPO / COMPLETION_PUSH_TIMESTAMP_FORMAT_RESIDUAL_NONBLOCKING / FINAL_FRESH_REAUDIT_NOT_AUTHORIZED / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

This disposition is a PARTIAL acceptance of the completion publication —
it is NOT a rejection of the completion implementation, whose mechanics
REMAIN SUPPORTED historical implementation evidence.

## 1. Live bootstrap (fail closed; verified before any edit)

Live GitHub `isakli05/audit-council-dev` `refs/heads/master` =
`c03d7a27f5f16f04b27404ab3efbe394610c660a` — EXACT. Governance HEAD
sole parent = `4fb4025a66d24432aa4b4ea570cc00b66a730f68` (completion
candidate; tree `7ef4ce40ef21ca60e02da37e9ffd0e48d5b89b22`; skill tree
`541a5cfc0f25ba4c2244abf1d6196feb04d310ad`; its own parent
`12187b60e0f2bc0d9541c241696203c4597654f4`) — all EXACT. CURRENT,
BACKLOG, `AUCDEV-010-QUALIFICATION-EXIT-COMPLETION.md`, RUNBOOK and
UPDATE PROTOCOL fetched at the exact live HEAD;
`skill/tests/test_qx_stabilization.py` fetched at the exact candidate.
Readiness BLOCKED / qualification NONE / installation NONE verified in
the fetched state. The candidate governance commit differs from the
candidate in docs only (skill bytes byte-identical). Work was performed
in a fresh DETACHED worktree at the exact base `c03d7a27…`; the
operator's working tree (a divergent local lineage with uncommitted
edits) was NOT touched.

## 2. Defect R1 — ResourceWarning closure-gate false negative

Reproduced at the base state BEFORE any edit: the focused module
(`skill/tests/test_qx_stabilization.py`, 41 tests) run with
`PYTHONWARNINGS=always::ResourceWarning` exits **0 with "Ran 41 tests …
OK" WHILE the same captured output contains 4 ResourceWarning marker
lines** for the two unclosed-file sites (`open(brief, "w").write("# b\n")`
at lines 547 and 562, in `test_new_binding_records_algorithm_and_
drifts_on_untracked_bytes` and `test_legacy_binding_without_algorithm_
field_verifies`). Therefore a `PYTHONWARNINGS=error::ResourceWarning`
EXIT STATUS alone could not establish warning cleanliness: the warning
fires at file-object finalization (unraisable there), so the run stays
green while the markers persist. This confirms the Control Room finding
that the completion session's C4 gate was a FALSE NEGATIVE for these two
sites (the completion's nine other fixes stand).

Fix (test-only, exactly two hunks, +4/−2 lines in exactly one file):
both writes converted to `with open(brief, "w") as fh: fh.write("# b\n")`.
No tested behavior changed; no runtime/source/contract/schema/prompt/
EvidenceStore change.

## 3. Robust warning-clean gates (all PASS; nothing hidden)

PASS requires BOTH unittest PASS and ZERO occurrences of
`ResourceWarning` and `Exception ignored while finalizing file` in the
captured output. All 34 outputs verified by machine check
(`checked=34 fail=0`; every file: `OK` + `Ran 41 tests` + zero markers):

- warning-visible gate (`always::ResourceWarning`): exit 0, 41/41 OK, 0 markers;
- warning-as-error gate (`error::ResourceWarning`): exit 0, 41/41 OK, 0 markers;
- 20 consecutive serial focused runs (warning-visible): 20/20 exit 0, 41/41, 0 markers;
- 12 bounded concurrent focused runs (3 rounds × 4 parallel): 12/12 exit 0, 41/41, 0 markers.

## 4. Full deterministic suite

- Natural posture ×2: **648 tests OK — 0 failures, 0 errors, 0 skips**
  (99.5 s / 99.5 s) — count matches the completion baseline exactly.
- Isolated clean-environment posture (fresh HOME/XDG/
  AUDIT_COUNCIL_CACHE_HOME/AUDIT_COUNCIL_ENV_ROOT via `env -i`):
  **648 OK — 7 skips**, the same seven explicitly classified external
  conditions as the completion (da27c0 archived evidence absent;
  production codex toolchain not on PATH ×5; smoke artifacts absent).
- `git diff --check`: CLEAN (working and staged).
- Zero markers from `test_qx_stabilization.py` in any full-suite run.
- One preserved invocation artifact, honestly recorded: a FIRST
  reproduction attempt with unredirected stdin produced an unrelated
  `TimeoutExpired` in `test_version_and_login_probes_served` (the
  fake-codex fixture blocks reading a never-EOF stdin). With stdin at
  EOF — the posture of every archived prior run — the module is green;
  the artifact output is retained unmodified in the handoff. Not a
  product/test defect; not hidden by retry-and-discard.

## 5. Broader full-suite ResourceWarning census — routed to AUCDEV-019

The full suite STILL emits pre-existing `ResourceWarning` output OUTSIDE
`test_qx_stabilization.py` (154 warnings / 97 distinct file:line sites
per natural run; the two natural runs identical per-site; isolated
posture 150/95; two production-module sites among them:
`skill/eval/tier2_scoring.py:246`, `skill/scripts/codex_runner.py:700`;
zero `Exception ignored while finalizing file` anywhere). The WHOLE SUITE
IS NOT ResourceWarning-CLEAN and this record does NOT claim it is. Full
census: `FULL-SUITE-RESOURCEWARNING-CENSUS.md` (handoff). Classified as
the already-tracked broader file-resource-hygiene surface of
**AUCDEV-019 (P2 / OPEN — Bounded file-resource cleanup)** — NOT
silently fixed by this task; no AUCDEV-019 implementation was performed
(separate authority required). This task closes ONLY the demonstrated C4
false-negative claim inside `test_qx_stabilization.py`.

## 6. Defect R2 — current B-001 finding-ID label binding corrected

The completion handoff matrix row 14 labeled current `B-001` as
`checkpoint immutability` — that label belongs to the HISTORICAL
`c114afe6865d160259af3c4d8e647437b6bef332` campaign's B-001 family. The
authoritative CURRENT fresh-audit finding is:

**`B-001` — HIGH / OBSERVED_FACT / product defect: Sandbox preserves
host environment and exposes procfs without PID isolation.**

R0 relation `F-A-01 ↔ B-001`, family
`SANDBOX_NAMESPACE_PROCFS_READ_CONFINEMENT` (R0-MAP-01). Disposition
UNCHANGED: `SUBSUMED_BY_ROOT_CAUSE_WITH_PROOF`, root `F-A-01`.
Corrected deliverable `FINDING-DISPOSITION-MATRIX-FINAL-CORRECTED.md`
(handoff) — machine-verified: exactly 21 rows, 21 unique current finding
IDs each exactly once, 17 FIXED_AND_DETERMINISTICALLY_VERIFIED,
4 SUBSUMED_BY_ROOT_CAUSE_WITH_PROOF, 0 REJECTED, 0 accepted residual;
explicit note distinguishing historical c114 B-001 (checkpoint
immutability, authoritative for `c114afe…` ONLY) from the current
sandbox/procfs B-001. The original auditor findings, the historical c114
evidence, all severities/classifications and every other row are
UNCHANGED; no new disposition was invented.

## 7. CURRENT installed-source status SHA typo corrected

`CURRENT_INSTALLED_SOURCE_STATUS_SHA_TYPO_CORRECTED`: the CURRENT-STATE
"Current development status" line contained
`8ae33444f349ce73c1359c963722e2d16acba630` (…`9c96`…); the AUTHORITATIVE
installed source identity is
`8ae33444f349ce73c1359b963722e2d16acba630` (…`9b96`…), which the
canonical `Installed source HEAD` field already carried and which this
correction now also uses. Record-precision correction ONLY: it does NOT
establish installed qualification provenance; installed qualified
predecessor remains **NOT ESTABLISHED**. Historical records (including
the completion report's own §6 occurrence of the typo'd string) are NOT
rewritten.

## 8. Old completion archive timestamp residual (preserved)

`COMPLETION_PUSH_TIMESTAMP_FORMAT_NONCONFORMITY` — the preserved,
unmutated completion archive's push evidence uses malformed timestamp
strings `2026-09-13T13:28:0XZ` (push) and `2026-09-13T13:28:2XZ`
(postpush capture). Classification: COMPLETENESS LIMITATION / EVIDENCE
TIMESTAMP PRECISION. The missing seconds digit is NOT invented; the old
archive is NOT repacked; the Git fast-forward result (12187b6..c03d7a2)
remains independently supported by GitHub state and Git output. For THIS
session every new stage timestamp is valid RFC3339 UTC with concrete
numeric seconds.

## 9. Final re-audit candidate identity (THE ONLY target for the final fresh audit)

| Identity | Value |
|---|---|
| FINAL_REAUDIT_CANDIDATE_SHA | `f4ca8a3cff3d1c3f1d52bbb49031669b5d0c07a2` |
| Candidate tree | `7b6abaa0b106e3630594c3775e0e099fa49f79ad` |
| Candidate skill tree | `d758e772693e1a524f4fab62f5e01fbc325542ae` |
| Sole parent | `c03d7a27f5f16f04b27404ab3efbe394610c660a` (completion governance publication) |
| Subject | `test: close qualification-exit warning gate` |
| Changed paths | exactly ONE: `skill/tests/test_qx_stabilization.py` (+4/−2) |

This SHA SUPERSEDES `4fb4025a…` as the ONLY candidate for the final
fresh A/B re-audit. `4fb4025a…` is NOT independently closed, NOT
re-audited and NOT rejected — its completion mechanics REMAIN SUPPORTED
historical implementation evidence inside this successor's chain
(EvidenceStore production wiring, F-A-12 single FIXED disposition,
21-by-21 cardinality all stand, pending fresh audit). All runtime/skill
product bytes other than the single test-file change are IDENTICAL to
`4fb4025a…`.

## 10. Publication

Exactly TWO commits from the detached worktree: Commit 1 = the test-only
successor above (sole parent `c03d7a27…`); Commit 2 = THIS governance
record (exactly `AUCDEV-CURRENT-STATE.md`,
`AUCDEV-BACKLOG.md`, and NEW
`AUCDEV-010-FINAL-REAUDIT-PREFLIGHT-CORRECTION.md`;
QUALIFICATION-HISTORY untouched — no audit or qualification event
occurred). Exactly ONE explicit fast-forward refspec push
(`git push origin <GOVERNANCE_SHA>:refs/heads/master`) after a final
live-master EXACT re-check at `c03d7a27…`; contemporaneous
precommit/prepush/push/postpush evidence with valid RFC3339 UTC
timestamps in the handoff archive.

## 11. Qualification state (unchanged by this record)

- AUCDEV-010: OPEN / P1 / BLOCKED.
- Qualification readiness: **BLOCKED**. Qualification: **NONE**.
  Installation: **NONE**. Installed source identity:
  `8ae33444f349ce73c1359b963722e2d16acba630` (authoritative; typo
  corrected in CURRENT status text). Installed qualified predecessor:
  NOT ESTABLISHED.
- Permitted success of THIS publication is ONLY:
  `AUCDEV_010_FINAL_REAUDIT_PREFLIGHT_CORRECTION_PUBLISHED_FOR_CONTROL_ROOM_READBACK`
  — it does NOT mean candidate PASS, qualification readiness,
  qualification, or installation.
- Immediate next action: INDEPENDENT CONTROL ROOM READBACK of THIS
  publication, THEN preparation of the FINAL FRESH A/B RE-AUDIT of
  `f4ca8a3cff3d1c3f1d52bbb49031669b5d0c07a2`. Neither auditor is
  launched by this record; no auditor/model execution, addendum,
  adjudication, qualification or installation is authorized.
