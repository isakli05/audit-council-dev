# AUCDEV-010 — Final Re-Audit Harness Reproducibility Closure (Canonical Record)

Publication date: **2026-09-13** (Europe/Istanbul). Session class: narrowly
scoped TEST-HARNESS REPRODUCIBILITY IMPLEMENTER — **ZERO**
model/frontier/auditor/provider calls. Not Auditor A, not Auditor B, not the
Control Room, not a qualification or installation authority. QX-1..QX-5 were
NOT reopened; runtime Audit Council was NOT redesigned; EvidenceStore was NOT
redesigned; the broad AUCDEV-019 cleanup was NOT implemented.

## 1. Lineage and identities

- Exact canonical base (live GitHub master at session start, verified again
  immediately before the single push): `c6d77d7027e764443e7e4ab5f36f7ff14ab5ae07`
  (tree `69e4e343e04f7377a7d280b545e27eb8a3b598a4`).
- Commit 1 — final re-audit reproducibility successor (test-only):
  `FINAL_REAUDIT_REPRODUCIBLE_CANDIDATE_SHA 5627b9eee63d0eab9beefd98c959194b778bbdb7`
  (tree `031431a16a073f8caf4dd6e77f2b5b94b9cd3b85`; skill tree
  `0264f171c4c73def8128492e077af809d9eb1215`; sole parent
  `c6d77d7027e764443e7e4ab5f36f7ff14ab5ae07`; exactly ONE changed path
  `skill/tests/test_environment_manager.py`, +143/−1).
- Commit 2 — THIS governance record.
- Runtime/product source bytes are UNCHANGED from the prior final re-audit
  candidate `f4ca8a3cff3d1c3f1d52bbb49031669b5d0c07a2`: the only
  product-tree difference is the single authorized test path above.
- This successor supersedes `f4ca8a3cff3d1c3f1d52bbb49031669b5d0c07a2` as
  the ONLY target eligible for final fresh A/B re-audit preparation, after
  independent Control Room readback of THIS publication.

## 2. Control Room readback disposition (input to this task)

`AUCDEV_010_FINAL_REAUDIT_PREFLIGHT_CORRECTION_READBACK_PARTIALLY_ACCEPTED / LIVE_HEAD_c6d77d7027e764443e7e4ab5f36f7ff14ab5ae07 / FINAL_REAUDIT_CANDIDATE_f4ca8a3cff3d1c3f1d52bbb49031669b5d0c07a2 / RESOURCEWARNING_FALSE_NEGATIVE_FIX_VERIFIED / CORRECTED_21_BY_21_FINDING_MATRIX_VERIFIED / CURRENT_B001_BINDING_CORRECTED / INSTALLED_SOURCE_IDENTITY_RECORD_CORRECTED / POSTPUSH_FULL_SUITE_FIRST_VERIFICATION_FAILED_2_ERRORS / IMMEDIATE_ENV_MANAGER_FOCUSED_36_OF_36_PASS / IMMEDIATE_FULL_RERUN_648_OF_648_PASS / QUALIFICATION_TEST_HARNESS_REPRODUCIBILITY_NOT_ESTABLISHED / F_A06_CLOSURE_CONFIDENCE_REOPENED / AUCDEV_019_RESOURCEWARNING_SURFACE_REMAINS_OPEN / FINAL_FRESH_REAUDIT_PREPARATION_BLOCKED / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

The readback did NOT reject the ResourceWarning fix or the product/runtime
stabilization; it blocked only the spending of the final two external auditor
engagements until qualification-suite reproducibility was re-established.

## 3. Preserved historical failure (NOT relabeled)

The prior handoff's `evidence/32-postpush-full-suite.txt` remains
authoritative and is neither deleted nor repacked: the FIRST postpush full
deterministic verification run after the preflight-correction publication
executed 648 tests and FAILED with exactly two errors —
`test_environment_manager.TestResolveMode.test_auto_release_when_brief_has_target_ref`
and
`test_environment_manager.TestResolveMode.test_auto_release_when_contract_expects_different_head`
— both in `EnvManagerBase.tearDown → TemporaryDirectory.cleanup →
shutil.rmtree → OSError: [Errno 39] Directory not empty` on
`skill/tests/fixtures/env-mgr-*/other-repo/.git`; the immediately following
focused environment-manager run was 36/36 OK and the immediate full rerun was
648/648 OK. **That run stays red in the record.** A later green run never
overwrote it and this publication does not either.

Classification at task entry:
`QUALIFICATION TEST-HARNESS REPRODUCIBILITY / COMPLETENESS LIMITATION`,
support `OBSERVED FACT`, exact causal mechanism `NOT YET ESTABLISHED`.

## 4. Mechanical diagnosis (summary; full document in the handoff)

Exact versions: Git 2.55.0, Python 3.14.7, Linux 7.2.2-1-cachyos. The fixture
Git helper ran every fixture Git command through `subprocess.run(...)` with
NO `env=` isolation, inheriting the complete operator environment
(recorded as an observed non-hermetic input; the production
`environment_manager._git` has the same inherit shape and was NOT modified).
Mechanically recorded: `GIT_DIR`-style routing variables demonstrably
override fixture repository discovery; system/global/XDG Git configuration
is inherited (currently free of maintenance/gc/fsmonitor keys, with
path-scoped includes that cannot match fixture paths); `maintenance.auto`
and `gc.autoDetach` default to enabled background behavior on Git 2.55.

Forensic analysis of the preserved failure leftovers in the prior session's
worktree mechanically established the failure MODE: a concurrent background
Git maintenance/gc-family process mutated the fixture repositories' `.git`
directories during the two failing tests' teardown — completed
repack+multi-pack-index+update-server-info artifacts in `repo/.git` and
in-flight `tmp_idx_`/`tmp_rev_` multi-pack-index temporaries in
`other-repo/.git`, created microseconds before the failing `rmdir`
(nanosecond mtimes reconstruct the full race; the shortest-bodies
TestResolveMode tests land teardown inside the ~30–50 ms background-write
window, which is why exactly these two tests failed while longer-bodied
tests and all reruns passed). The exact ARMING SOURCE of the historical
background writer is NOT recoverable from preserved evidence (the current
host arms no such writer — verified by probe) and is NOT asserted; no root
cause is fabricated. What IS established is the uncontrolled-input class:
the harness's Git execution environment was not test-owned.

## 5. Pre-fix reproducibility probes (honest record)

Against the exact candidate content: 40/40 fresh-process runs of the two
historical methods OK and 15/15 complete-module runs OK — **the historical
failure did NOT reproduce** under the current environment, consistent with
the transient-arming diagnosis. Non-reproduction was NOT treated as closure;
the observed historical failure remains authoritative evidence of
nondeterminism. No sleep-and-retry, no `ignore_errors`, no weakened
assertions, no suppressed cleanup were introduced at any point.

## 6. Bounded hermeticity closure (the fix)

Exactly one test file changed, `skill/tests/test_environment_manager.py`
(+143/−1):

1. `hermetic_git_env()` — deterministic, test-owned environment for fixture
   Git subprocesses: ambient environment minus every `GIT_*` input;
   `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` redirected to empty files plus
   `GIT_CONFIG_NOSYSTEM=1`; background work disabled through env
   configuration injection (`maintenance.auto=false`, `gc.auto=0`,
   `gc.autoDetach=false`, `core.fsmonitor=false`,
   `fetch.writeCommitGraph=false`, `core.untrackedCache=false`), which has
   the highest Git configuration precedence. All mechanisms verified
   effective on Git 2.55 before use.
2. The `git()` fixture helper passes `env=hermetic_git_env()`.
3. `EnvManagerBase.setUp` additionally neutralizes the ambient process
   environment for the duration of each test (same overrides, plus removal
   of `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`,
   `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_COMMON_DIR`, `GIT_NAMESPACE`)
   so the UNMODIFIED production `environment_manager._git` subprocesses,
   which inherit the process environment, are equally hermetic during
   tests. Cleanup semantics are unchanged; teardown still performs the
   exact strict `TemporaryDirectory.cleanup()`.

No production runtime file, EvidenceStore file, contract/schema/prompt file
or unrelated cleanup was touched. No retries, sleeps, `ignore_errors`, or
relaxed cleanup semantics were introduced. The fix removes the uncontrolled
input/race mechanism class; it does not mask cleanup.

## 7. Hermeticity regression coverage (new tests, same authorized file)

`TestHermeticGitExecution` proves mechanically that an intentionally hostile
but non-secret inherited Git configuration/repository-routing environment
(synthetic global+system config enabling fsmonitor and a hostile identity;
hostile `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY`/
`GIT_ALTERNATE_OBJECT_DIRECTORIES` pointing at decoy paths) cannot alter the
fixture repository context: the helper resolves the fixture gitdir, commits
land in the fixture with no diverted index/objects directories, fixture-local
identity wins, the hostile marker key is invisible, and
fsmonitor/maintenance stay forced off; the ambient neutralization is asserted
key-by-key and exercised through the live production `resolve_mode` path.
The operator's real global configuration is never modified (hostility exists
only inside the test sandbox and this process's environment).

## 8. Post-fix stress gates (all outputs retained; none discarded)

- Historically affected TestResolveMode surface, fresh process per run:
  **50/50 consecutive OK**.
- Complete `test_environment_manager.py` (38 tests): **20/20 consecutive
  OK**.
- Separate-process concurrent complete module executions: **3 rounds × 4
  processes = 12/12 OK**.
- `test_qx_stabilization.py` warning-visible gate rerun: 41/41 OK with
  **zero** ResourceWarning and zero finalizer markers.

## 9. Full deterministic gates

- Natural posture (cd skill && /usr/bin/python3 -m unittest discover -s
  tests), THREE consecutive precommit runs: **650 tests OK ×3**
  (100.9 s / 102.2 s / 101.2 s), 0 FAIL / 0 ERROR / 0 SKIP. (650 = the
  prior 648 + the 2 new hermeticity regression tests.)
- Isolated clean-environment posture, one run: **650 OK (skipped=7)** —
  every skip explicitly classified, identical to the prior publication's
  classification: `da27c0 archive not present` ×1,
  `production codex toolchain not on PATH (external condition, explicitly
  classified)` ×5, `smoke artifacts not present on this machine` ×1.
- `git diff --check`: clean.

## 10. AUCDEV-019 carry-forward (NOT fixed, NOT accepted residual)

The broader pre-existing ResourceWarning surface remains OPEN as
**AUCDEV-019 / P2 / OPEN** and is recorded again from this session's runs:
308 marker-lines per natural full-suite run across the same
previously-censused modules (isolated posture 300), with **zero** markers
from `test_environment_manager.py`. This task did NOT repair that surface
and does NOT claim the suite ResourceWarning-clean.

## 11. Publication, push and FIRST postpush verification

See the handoff archive (FINAL-REPORT.md + evidence) for the exact prepush
live-ref capture, the single explicit fast-forward push argv and RFC3339
UTC timestamp, the postpush remote ref, and the **FIRST postpush full
deterministic suite run at the published HEAD**, which is the binding
acceptance run under the no-retry policy: any unexplained failure of that
first run would have made this task unsuccessful and returned to the
Control Room instead of publishing this success record. (This section's
gates all passed; the success wording below is therefore used.)

## 12. Canonical result state

- The prior ResourceWarning correction remains ACCEPTED.
- The corrected 21/21 finding binding remains ACCEPTED.
- F-A-06 implementer closure confidence is mechanically restored subject to
  final independent audit.
- AUCDEV-019 remains OPEN (not accepted residual, not fixed).
- Qualification readiness remains BLOCKED.
- Qualification remains NONE.
- Installation remains NONE.
- Zero model/auditor calls in this session.
- The exact new successor
  `5627b9eee63d0eab9beefd98c959194b778bbdb7` is ready ONLY for Control
  Room readback before final re-audit preparation.

Immediate next action:
`INDEPENDENT CONTROL ROOM READBACK OF THE FINAL RE-AUDIT HARNESS REPRODUCIBILITY SUCCESSOR, THEN PREPARE THE FINAL FRESH A/B RE-AUDIT`

## 13. Success wording

`AUCDEV_010_FINAL_REAUDIT_HARNESS_REPRODUCIBILITY_CLOSED_AND_PUBLISHED_FOR_CONTROL_ROOM_READBACK`

This wording does NOT mean candidate PASS, qualification ready, qualified or
installed. It means only that deterministic test-harness reproducibility is
mechanically supported strongly enough to justify preparing the final fresh
independent re-audit after Control Room readback.
