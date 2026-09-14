# AUCDEV-010 — Identity Manifest Digest Determinism Correction (Canonical Record)

Publication date: **2026-09-14** (Europe/Istanbul). Session class: ZERO-MODEL
QUALIFICATION-EVIDENCE DETERMINISM CORRECTION — NOT Auditor A, NOT Auditor
B, NOT the Control Room, NOT a qualification authority, NOT an installation
authority. ZERO model/frontier/provider inference calls. This session closed
the identity-manifest digest determinism defect exposed by the FIRST
postpush verification of the DeprecationWarning compatibility successor and
publishes this governance record. NO auditor execution is authorized by
this record. NO fresh final A/B package is prepared by this record.

Parallel records: CURRENT-STATE history record 50; BACKLOG AUCDEV-010
history record 52. Canonical base: `56acc23a0550cfdd046b23ef3d11d15b90721679`
(live GitHub `master` verified EXACT at bootstrap AND re-verified EXACT
immediately before the single fast-forward push of THIS publication).
Session evidence workspace + handoff archive identity: recorded in the
workspace FINAL-REPORT (an archive never contains its own digest).

## 1. Control Room disposition (input authority; recorded verbatim)

`AUCDEV_010_FINAL_PREAUDIT_DEPRECATIONWARNING_CORRECTION_READBACK_PARTIALLY_ACCEPTED / LIVE_HEAD_56acc23a0550cfdd046b23ef3d11d15b90721679 / WARNING_CLEAN_CANDIDATE_26d8730fe11834eb4be629db3a07e9ec83c4fd46 / DEPRECATIONWARNING_CORRECTION_MECHANICALLY_ACCEPTED / PROJECT_OWNED_WARNINGS_ZERO_SUPPORTED / FIRST_POSTPUSH_FULL_SUITE_FAILED_1_FAILURE / IDENTITY_MANIFEST_DIGEST_DETERMINISM_DEFECT_OBSERVED / GENERATED_AT_INCLUDED_IN_MANIFEST_SHA256 / FAILURE_PREEXISTED_DEPRECATIONWARNING_CORRECTION / RERUN_PASS_DOES_NOT_ERASE_FIRST_FAILURE / FRESH_AB_PACKAGE_PREPARATION_BLOCKED / AUDITOR_EXECUTION_BLOCKED / MODEL_ENGAGEMENTS_USED_0 / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

The prior DeprecationWarning fix REMAINS ACCEPTED and is PRESERVED (this
correction inherits it; `path_guard.py:701` is untouched here).

## 2. Observed defect (preserved exactly; authoritative RED)

The FIRST postpush warning-visible full suite at published HEAD `56acc23…`
produced:

- `Ran 650 tests in 452.524s` → `FAILED (failures=1)`, RC=1;
- failing test:
  `test_qx_stabilization.TestIdentityManifest.test_manifest_covers_every_tracked_file_and_is_deterministic`
  at the assertion `self.assertEqual(m1["manifest_sha256"], m2["manifest_sha256"])`;
- full preserved output: prior session handoff
  `aucdev010-dw-correction-evidence-20260914/first-postpush-warning-visible.txt`
  (copied into THIS session's handoff archive).

The immediate rerun passed. THE RERUN DOES NOT OVERWRITE THE FIRST FAILURE:
the original failure remains authoritative RED evidence. The prior
implementer label `FLAKY_IDENTITY_MANIFEST_DIGEST_GENERATED_AT_RACE` is
preserved as HISTORICAL REPORT LANGUAGE; the Control Room classification of
record is the one below.

## 3. Classification

`AUDIT_COUNCIL_PRODUCT_DEFECT / QUALIFICATION_EVIDENCE_DETERMINISM`
(support: `OBSERVED_FACT`). Mechanically established:

- `identity_manifest()` is production Audit Council code;
- its own docstring declared two invocations on an unchanged tree produce
  identical documents except `generated_at`;
- `generated_at = utc_now_iso()` (`state_store.py:143-144`), exactly
  one-second resolution;
- the previous `manifest_sha256` computation digested the WHOLE document
  including `generated_at` (`repo_fingerprint.py:380-382` pre-fix);
- therefore a second-boundary crossing changes BOTH `generated_at` AND
  `manifest_sha256` while every identity-bearing input stays equal;
- the determinism regression expects `manifest_sha256` to remain identical;
- the failure surface is byte-identical before and after the unrelated
  path_guard DeprecationWarning correction (that diff touched only
  `skill/scripts/path_guard.py`).

Not classified as a flaky-test assertion: the production invariant
(identity digest determinism) is the defect; no mechanical evidence
disproves it.

## 4. Consumer/contract review (before edit)

`IDENTITY-MANIFEST-DIGEST-SEMANTICS.md` (session workspace; included in the
handoff archive) inspected every repository consumer of
`identity_manifest()`, `manifest_sha256`, `manifest_version`, the
`identity-manifest` CLI and `verify-manifest-files`. Determinations:

- NO consumer requires `generated_at` to participate in `manifest_sha256`;
- NO verifier recomputes `manifest_sha256` (the only verifier,
  `verify_files_against_manifest`, checks per-file `worktree_sha256`
  values only);
- NO historical v1 manifest depends on timestamp-bound digest semantics
  (recorded digests are one-time append-only observations, never
  recomputed; the update protocol forbids rewriting them);
- `manifest_sha256` is intended as a TARGET-IDENTITY DIGEST over
  identity-bearing content; `generated_at` is non-identity metadata
  (docstring + committed regression + public-contract text all agree);
- `manifest_version` REMAINS 1: document shape unchanged, no consumer
  branches on it, no compatibility contract distinguishes digest
  algorithms.

No conflicting compatibility contract was found; no STOP condition applied.

## 5. Deterministic RED (no sleep, no timing luck)

Before any edit, on the exact current bytes, consecutive
`identity_manifest()` calls were forced to receive `2026-09-14T00:00:00Z`
and `2026-09-14T00:00:01Z` on an unchanged fixture tree:

- `generated_at` values differ: TRUE;
- every identity-bearing digest input EXCLUDING `generated_at` equal
  (head_sha, tree_sha, tracked, tracked_count, untracked_inventory,
  untracked_digest, total_tracked_bytes, repo_root, manifest_kind,
  manifest_version): TRUE;
- `manifest_sha256` differs: TRUE (`af05b8e5…` vs `c2ae025b…`) — RED
  CONFIRMED (`red-forced-straddle.txt` in the handoff archive).

## 6. Exact authorized correction

`skill/scripts/repo_fingerprint.py` (the ONLY product change):

```diff
     doc["manifest_sha256"] = sha256_bytes(
         canonical_json({k: v for k, v in doc.items()
-                        if k != "manifest_sha256"}).encode("utf-8"))
+                        if k not in ("manifest_sha256", "generated_at")})
+        .encode("utf-8"))
```

plus a docstring update stating the digest semantics explicitly.
`manifest_sha256` is now a pure function of the identity-bearing manifest
content. PRESERVED: `generated_at` in the emitted document; tracked
inventory; blob identities; worktree SHA-256 values; untracked
inventory/digest; head/tree identities; repo root semantics;
`manifest_version` = 1; fingerprint-v2 semantics; all unrelated
state/evidence behavior.

Post-fix invariant (proven by the regression): same identity-bearing target
content → same `manifest_sha256`, even when `generated_at` differs.

## 7. Strengthened regression (timing race removed)

`skill/tests/test_qx_stabilization.py`
(`TestIdentityManifest.test_manifest_covers_every_tracked_file_and_is_deterministic`)
now mechanically forces the second boundary via
`mock.patch.object(repo_fingerprint, "utc_now_iso", side_effect=[…T0, …T1])`
and proves: timestamps differ; `manifest_sha256` identical; ALL
identity-bearing fields identical (explicit key list); tracked coverage and
per-file sha256 shape unchanged; per-file identity verification succeeds on
BOTH documents. Verified RED on the pre-fix bytes (exact assertion:
`manifest_sha256 changed across a second boundary: the identity digest is
timestamp-bound`, failures=1, RC=1) and GREEN post-fix. The invariant was
strengthened, not weakened — the digest comparison is retained and made
load-bearing under forced time divergence.

## 8. Focused verification (§9)

- Complete `TestIdentityManifest` surface: 3/3 OK.
- Forced timestamp-straddle regression in FRESH processes: **50/50 PASS**.
- Complete `test_qx_stabilization.py` in fresh processes: **20/20 PASS**
  (41 tests each).
- One slow/tracemalloc posture focused run
  (`PYTHONWARNINGS=always` + `PYTHONTRACEMALLOC=15`): 3/3 OK, zero warning
  lines, zero `Exception ignored`.
- Zero hidden/intermediate failures (every executed run is recorded in the
  handoff archive).

## 9. Warning/compatibility preservation (§10)

The accepted DeprecationWarning and ResourceWarning closures remain intact:

- Warning-visible complete suite (`PYTHONWARNINGS=always` +
  `PYTHONTRACEMALLOC=15`) ×2: `Ran 650 tests` → `OK`, exit 0
  (453.693 s / 453.456 s); complete output parsed: **0 warning lines of ANY
  category, 0 `Exception ignored`** (both runs).
- `PYTHONWARNINGS=error` complete suite: `Ran 650 tests` → `OK`, exit 0
  (100.688 s); parsed output clean.
- Test count unchanged at 650.

## 10. Full regression gates (§11)

- Natural full suite ×3 (default posture): **650 OK ×3** (100.105 /
  99.915 / 99.485 s; 0 FAIL / 0 ERROR / 0 SKIP; rc=0 each).
- Isolated clean-environment suite (`env -i`, fresh
  HOME/XDG/AUDIT_COUNCIL_CACHE_HOME/AUDIT_COUNCIL_ENV_ROOT): `Ran 650
  tests` → `OK (skipped=7)`, rc=0 (80.599 s). Skip classification EXACTLY
  canonical, verbatim: `da27c0 archive not present` ×1; `production codex
  toolchain not on PATH (external condition, explicitly classified)` ×5;
  `smoke artifacts not present on this machine` ×1 (verbose enumeration
  run captured).
- `git diff --check`: CLEAN.
- No failed intermediate run occurred; nothing discarded.

## 11. Commit model and identity

- Commit 1 (this correction; sole parent
  `56acc23a0550cfdd046b23ef3d11d15b90721679`):
  `FINAL_REAUDIT_IDENTITY_DETERMINISTIC_CANDIDATE_SHA` =
  `68e3b082958d2f6f35224702e51e35bbbd49d7db`; tree
  `c36899d817c7e15fb8e31fc1e80fab198dc583a7`; `skill/` tree
  `ce06ef9f46d983548fba6ee960d4d202573feedd`; exactly TWO changed paths
  (`skill/scripts/repo_fingerprint.py` +6/−2,
  `skill/tests/test_qx_stabilization.py` +28/−3); inherits and preserves
  the accepted path_guard warning correction.
- Commit 2 (governance; sole parent `68e3b082…`): THIS file +
  CURRENT-STATE + BACKLOG. QUALIFICATION-HISTORY untouched.
- This new SHA `68e3b082…` is the ONLY target eligible for a fresh final
  A/B package preparation (subject to Control Room readback of THIS
  publication and a NEW package-preparation + execution authority chain).

## 12. Effect on the final package (staleness)

The historical package `AUCDEV-010-BRQ-FINAL-E652BDB4-20260914-01` REMAINS
`STALE_TARGET_SUPERSEDED_BY_DEPRECATIONWARNING_COMPATIBILITY_CORRECTION`
(now superseded as a target further by THIS identity-deterministic
successor; package/archive NOT mutated or repacked; preserved untouched as
valid historical preparation evidence for its exact target `e652bdb4…`
only). The warning-clean candidate `26d8730f…` is superseded as a
final-audit target by `68e3b082…`. NO fresh final A/B package is prepared
in this session; auditor execution remains BLOCKED.

## 13. Canonical result state

- `AUCDEV_010_IDENTITY_MANIFEST_DETERMINISM_CORRECTION_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
- MODEL_ENGAGEMENTS_USED = 0; AUDITOR_A = NOT_STARTED; AUDITOR_B =
  NOT_STARTED; EXECUTION_AUTHORITY = NOT_YET_GRANTED.
- Qualification readiness BLOCKED; qualification NONE; installation NONE;
  installed qualified predecessor NOT ESTABLISHED; bootstrap-root
  exception applicable and unconsumed.
- ZERO model/frontier/provider calls in this session; no auditor launched.

Immediate next action:
`INDEPENDENT CONTROL ROOM READBACK OF THIS IDENTITY MANIFEST DETERMINISM CORRECTION PUBLICATION; ONLY IF ACCEPTED, ONE FRESH FINAL A/B PACKAGE PREPARATION AGAINST 68e3b082… AND A SEPARATE EXPLICIT OPERATOR EXECUTION AUTHORITY`

This wording does NOT mean any auditor started, any authority granted, any
model engagement consumed, candidate PASS, qualification readiness,
qualification or installation.

## 14. Publication scope and hygiene

This publication changes exactly: `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`,
`docs/chatgpt-project/AUCDEV-BACKLOG.md`, and NEW
`docs/chatgpt-project/AUCDEV-010-IDENTITY-MANIFEST-DETERMINISM-CORRECTION.md`
(THIS file). QUALIFICATION-HISTORY untouched. Historical records are not
rewritten; supersession is recorded append-only. Local pre-existing cosmetic
smoke-fixture gitlink worktree entries remain untouched (identical in the
canonical tree; never staged). The FIRST postpush binding gate at the
published HEAD is executed after this publication and its evidence is
recorded in the workspace FINAL-REPORT/handoff archive, not in this file.
