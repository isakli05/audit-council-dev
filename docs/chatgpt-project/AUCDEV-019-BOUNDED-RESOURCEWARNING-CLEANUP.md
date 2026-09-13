# AUCDEV-019 — Bounded ResourceWarning Triage and Cleanup Before Final A/B Execution

Status: `AUCDEV_019_BOUNDED_RESOURCEWARNING_CLEANUP_COMPLETE_NEW_FINAL_REAUDIT_TARGET_PUBLISHED_FOR_CONTROL_ROOM_READBACK`
Candidate commit: `e652bdb45007e364aa282fa12685db1d726891f1` (sole parent `94f67038840673bbff8c987f3c01b920b0a5af50`)
Governance commit: THIS governance record (sole parent `e652bdb45007e364aa282fa12685db1d726891f1`; identity = the publish commit created by this session)
Session character: ZERO-MODEL bounded resource-lifecycle triage and cleanup
(NOT Auditor A/B, NOT the Control Room, NOT a qualification/installation
authority; ZERO model/frontier/provider/auditor calls — MODEL_ENGAGEMENTS_USED = 0).

## 1. Live bootstrap (fail-closed, exact)

- Fetched from GitHub: live `origin/master` = local HEAD =
  `94f67038840673bbff8c987f3c01b920b0a5af50` EXACT (required live HEAD).
- State verified at that HEAD: qualification readiness BLOCKED;
  QUALIFICATION_NONE; INSTALLATION_NONE; AUDITOR_A = NOT_STARTED;
  AUDITOR_B = NOT_STARTED; MODEL_ENGAGEMENTS_USED = 0;
  preparation campaign state `PREPARED_NOT_EXECUTION_AUTHORIZED`;
  AUCDEV-019 OPEN / not pre-adjudicated.
- Frozen audit target `5627b9eee63d0eab9beefd98c959194b778bbdb7`
  (tree `031431a16a073f8caf4dd6e77f2b5b94b9cd3b85`; skill tree
  `0264f171c4c73def8128492e077af809d9eb1215`) — skill tree verified
  byte-identical at live HEAD, so the census ran against the exact target
  product bytes.

## 2. Control Room readback disposition (recorded verbatim, pre-edit)

`AUCDEV_010_FINAL_FRESH_AB_REAUDIT_PREPARATION_READBACK_ACCEPTED_AS_PREPARATION_ONLY / LIVE_HEAD_94f67038840673bbff8c987f3c01b920b0a5af50 / FROZEN_TARGET_5627b9eee63d0eab9beefd98c959194b778bbdb7 / FULL_TARGET_IDENTITY_MECHANICS_SUPPORTED / COMMON_INPUT_PARITY_RECORD_SUPPORTED_NOT_INDEPENDENTLY_REVERIFIED_FROM_TRANSPORT_BYTES / SELFTEST_ACTUAL_24_OF_24_PASS_CANONICAL_21_OF_21_COUNT_NONCONFORMITY / AUCDEV_019_OPEN_WITH_CONFIRMED_PRODUCTION_RESOURCEWARNING_SITES / AUDITOR_EXECUTION_BLOCKED_PENDING_AUCDEV019_BOUNDED_TRIAGE / MODEL_ENGAGEMENTS_USED_0 / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

The preparation event `AUCDEV-010-BRQ-FINAL-5627B9EE-20260913-01` package is
preserved unmutated; its historical archive was NOT rewritten or repacked;
neither auditor was launched.

## 3. Fresh baseline census (before any edit)

Full deterministic suite `python3 -m unittest discover -s skill/tests` at the
exact current product bytes, warning-visible
(`PYTHONWARNINGS=always::ResourceWarning`) with tracemalloc allocation-site
attribution (`PYTHONTRACEMALLOC=15`); run itself `Ran 650 tests in 456.561s`
→ `OK`, 0 skips; exit 0. Raw: `baseline-census-stdout-stderr.txt`.

- **154 warning occurrences / 97 distinct sites / 17 project files**
  (2 production + 15 test) — re-established on current source; matches the
  prior historical census counts exactly.
- Production sites (16 occurrences):
  `skill/eval/tier2_scoring.py:246` — `binding = json.load(open(os.path.join(`
  (10×, cluster RC-1); `skill/scripts/codex_runner.py:700` —
  `return int(open(path, "r", encoding="utf-8").read().strip())`
  (6×, cluster RC-2).
- Zero `Exception ignored` finalizer markers; zero external/library sites
  (every occurrence's innermost allocation frame is repository code).

Artifacts: `AUCDEV019-RESOURCEWARNING-BASELINE.json`,
`AUCDEV019-RESOURCEWARNING-SITE-MATRIX.md`.

## 4. Root-cause clusters

Four mechanical clusters; every site assigned to exactly one:

| Cluster | Mechanism | Sites | Occ | Production |
|---|---|---|---|---|
| RC-1 | `json.load(open(...))` unclosed read handle | 67 | … | `tier2_scoring.py:246` |
| RC-2 | `open(...).read()` temporary read handle | 26 | … | `codex_runner.py:700` |
| RC-3 | `open(..., "w")` temporary write handle | 3 | 3 | — |
| RC-4 | comprehension iteration over `open(...)` | 1 | 1 | — |

No ownership-transfer, subprocess-pipe, socket/lock, external-library, or
false-attribution site exists. Full detail incl. per-site ownership,
lifetime, error-behavior and interaction-risk analysis:
`AUCDEV019-ROOT-CAUSE-CLUSTERS.md` (archived).

## 5. Production-site conclusions

- `tier2_scoring.py:246` (`run_fixture`): handle local to the expression,
  never referenced after `json.load`; fixed with
  `with open(os.path.join(run_dir, "01-environment-binding.json")) as fh:
  binding = json.load(fh)`. Same exceptions at same points
  (FileNotFoundError / JSONDecodeError propagate unchanged); closing a
  fully-read read-only handle changes no observable semantics.
- `codex_runner.py:700` (`read_exit_code_once`): handle local to the read
  expression inside `try/except (ValueError, OSError)`; fixed with
  `with open(path, "r", encoding="utf-8") as fh: return int(fh.read().strip())`.
  Contract (int-or-None) identical; the managed close executes one `close(2)`
  per poll immediately instead of at GC — same total work, NO timing-policy
  change, no retry/sleep added. This is the PRIMARY completion-signal path.

## 6. Cleanup (exactly 17 files, all census-listed)

`skill/eval/tier2_scoring.py`, `skill/scripts/codex_runner.py` + the 15
census-listed test modules. Mechanisms used: `with open(...) as fh` blocks
only (including one timer-callback lambda → nested def so the write handle
can be managed; same thread, same 0.5 s delay, same bytes — the managed
close merely flushes deterministically inside the timer callback before the
polled reader can observe the file, removing a latent GC-timing race).
NO behavior/timing/schema/contract/sandbox/audit-semantics changes; NO
warning suppression, NO `warnings.filterwarnings`, NO global filters, NO
retries/sleeps added. Diff: 233 insertions / 134 deletions.

## 7. Verification gates (all exact, all observed)

- Focused (warning-visible): all 15 modified modules PASS — 26, 20, 9, 8, 2,
  11, 29, 6, 18, 18, 14, 5, 24, 18, 9 tests respectively.
- Stress/repeats (warning-visible): `test_wait_lifecycle_v102`,
  `test_codex_runner_mock` (Codex exit-code reading/completion path),
  `test_tier2_scoring` (Tier-2 scoring path) ×5 each = 15/15 OK, 0 warnings.
- Warning-clean acceptance gate: full suite warning-visible ×2, complete
  captured output parsed — run 1: `Ran 650 tests in 456.080s` → `OK`,
  **0 ResourceWarning lines, 0 `Exception ignored`**; run 2: `Ran 650 tests
  in 458.166s` → `OK`, **0 / 0**. Baseline was 154 / 0 → reduction of
  154 → 0, including both production sites (16 → 0) and all 95 test sites
  (138 → 0).
- `PYTHONWARNINGS=error::ResourceWarning` full suite: parsed output (not
  exit status alone) — exit 0, `Ran 650 tests in 92.884s` → `OK`;
  0 ResourceWarning mentions; 0 `Exception ignored`; 0 FAILED/ERROR lines.
- Natural posture ×3: **650 OK ×3** (89.758 s / 92.758 s / 91.743 s;
  0 failures, 0 errors, 0 skips; test count unchanged at 650 before and
  after — no tests added or removed).
- Isolated clean-environment posture once (`env -i`, fresh
  HOME/XDG/AUDIT_COUNCIL_CACHE_HOME/AUDIT_COUNCIL_ENV_ROOT):
  `Ran 650 tests in 80.223s` → `OK (skipped=7)`, every skip an explicitly
  classified external condition — da27c0 archive not present ×1; production
  codex toolchain not on PATH ×5 (verbatim reason "external condition,
  explicitly classified"); smoke artifacts not present on this machine ×1 —
  the same seven as all prior campaigns.
- `git diff --check` (base → candidate): CLEAN.
- No test-count change: 650 before and after (no tests added/removed).

## 8. Final disposition summary

`AUCDEV019-FINAL-DISPOSITION-MATRIX.md` (archived): every one of the 97
baseline distinct sites represented exactly once; **97 ×
FIXED_AND_DETERMINISTICALLY_VERIFIED** (2 production + 95 test); 0 ×
REJECTED_WITH_COUNTER_EVIDENCE; 0 × EXTERNAL; **REMAINING_PROJECT_OWNED_
RESOURCEWARNINGS = 0**. No site silently disappeared; every production
warning received an explicit disposition; no ACCEPTED_RESIDUAL created.

## 9. Effect on the prepared final A/B package

Tracked product/test bytes CHANGED ⇒ the frozen preparation event package
for target `5627b9eee63d0eab9beefd98c959194b778bbdb7` is now
**`STALE_TARGET_SUPERSEDED_BY_AUCDEV019_CLEANUP`**. The package and its
historical archive are preserved untouched and remain valid historical
preparation evidence FOR THEIR EXACT TARGET ONLY; its target digest must not
be reused as current. The AUCDEV-019 cleanup candidate
`e652bdb45007e364aa282fa12685db1d726891f1` (tree `0161c57565b7acc68a498d06a6b8b741780e2afe`) is the ONLY candidate
eligible for a fresh final A/B package preparation, which must be prepared
anew against the new SHA (including fresh binding gates, identity proof,
parity and blindness mechanics per the standing preparation protocol).

## 10. Preparation-evidence residuals carried forward (append-only)

1. `FINAL_PREPARATION_SELFTEST_COUNT_RECORD_NONCONFORMITY` — canonical prose
   says 21/21; actual `20-package-self-tests.json` records 24 total, 0
   failed. Classification: COMPLETENESS LIMITATION / RECORD PRECISION.
2. `FINAL_PREPARATION_CONTROL_ROOM_TRANSPORT_BYTES_NOT_INCLUDED_IN_HANDOFF`
   — the Control Room handoff contains transport digests/parity records but
   not the actual Auditor-A/B transport tarball bytes or blind product-source
   archive bytes; Control Room therefore did not independently re-verify
   transport byte parity from delivered archives. Classification:
   COMPLETENESS LIMITATION / EXECUTION-EVIDENCE AVAILABILITY.

Requirement recorded for any NEW final package: the Control Room handoff
must include the actual frozen transport bytes, or a single actual canonical
transport when A=B byte-identical plus deterministic proof sufficient to
reconstruct/compare the second, so actual payload bytes can be independently
inspected.

## 11. Publication record

- Commit 1 (cleanup candidate `e652bdb45007e364aa282fa12685db1d726891f1`, sole parent
  `94f67038840673bbff8c987f3c01b920b0a5af50`): exactly the 17
  ResourceWarning-linked paths; tree `0161c57565b7acc68a498d06a6b8b741780e2afe`; skill tree
  `9139a6711212c22dfd1d7441e2ee5245002fc20e`. This candidate is named
  `FINAL_REAUDIT_RESOURCE_CLEAN_CANDIDATE_SHA`.
- Commit 2 (governance, sole parent the candidate): CURRENT-STATE, BACKLOG,
  and THIS NEW report only; QUALIFICATION-HISTORY untouched.
- Push policy (evidence captured contemporaneously in the handoff archive):
  live master re-verified EXACT == `94f67038…` immediately before ONE
  explicit fast-forward push of the two commits (no force, no retry, no
  tags, no wildcard); exact prepush ref, push argv/output and postpush ref
  recorded in the archive.
- FIRST postpush full deterministic suite with ResourceWarnings visible at
  published HEAD: REQUIRED to pass and meet warning-clean criteria on the
  FIRST attempt; complete captured output, parsed for
  warning/finalizer markers, is preserved in the handoff archive. Task
  success is NOT permitted if that first run fails or emits an unexplained
  project-owned ResourceWarning.
- Handoff archive: exactly ONE non-secret `.tar.gz` for Control Room
  (bootstrap, census, matrices, raw outputs, RED/GREEN evidence, all gate
  runs, source/test diff, staleness determination, residuals record,
  governance before/after, prepush/push/postpush evidence, FIRST postpush
  run, secret scan, inventory, SHA256SUMS generated LAST). Archive path,
  outer SHA-256, byte size and member census are reported with the session
  return and recorded in the archive inventory itself.

## 12. Standing state after this publication

- MODEL_ENGAGEMENTS_USED = 0; AUDITOR_A = NOT_STARTED; AUDITOR_B =
  NOT_STARTED; EXECUTION_AUTHORITY = NOT_YET_GRANTED.
- QUALIFICATION_READINESS = BLOCKED; QUALIFICATION = NONE; INSTALLATION =
  NONE. This cleanup is deterministic hygiene only: it is NOT a candidate
  PASS, NOT qualification readiness, NOT qualification, NOT installation.
- AUCDEV-019: CLOSED by this bounded campaign (REMAINING_PROJECT_OWNED_
  RESOURCEWARNINGS = 0), subject to Control Room readback.
- NEXT: independent Control Room readback of this publication; then fresh
  final A/B re-audit package preparation against `e652bdb45007e364aa282fa12685db1d726891f1`; then
  explicit operator execution authority. Auditors remain NOT started.
