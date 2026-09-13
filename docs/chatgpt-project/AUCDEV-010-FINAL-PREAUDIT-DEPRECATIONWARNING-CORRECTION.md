# AUCDEV-010 — Final Pre-Audit DeprecationWarning Compatibility Correction (Canonical Record)

Publication date: **2026-09-14** (Europe/Istanbul). Session class: ZERO-MODEL
NARROW COMPATIBILITY CORRECTION — NOT Auditor A, NOT Auditor B, NOT the
Control Room, NOT a qualification authority, NOT an installation authority.
ZERO model/frontier/provider inference calls. This session reproduced, closed
and published the single Control-Room-observed project-owned production
`DeprecationWarning` at the exact final re-audit target and publishes this
governance record. NO auditor execution is authorized by this record.

Parallel records: CURRENT-STATE history record 49; BACKLOG AUCDEV-010
history record 51. Canonical base: `d0af87991993fc77c8b3f1e7c91baa7a76402981`
(live GitHub `master` verified EXACT at bootstrap AND re-verified EXACT
immediately before the single fast-forward push of THIS publication).
Session evidence workspace + handoff archive identity: recorded in the
workspace FINAL-REPORT (an archive never contains its own digest).

## 1. Control Room readback disposition (input authority; recorded verbatim)

`AUCDEV_010_FINAL_FRESH_AB_REAUDIT_PACKAGE_E652BDB4_READBACK_PARTIALLY_ACCEPTED / LIVE_HEAD_d0af87991993fc77c8b3f1e7c91baa7a76402981 / TARGET_e652bdb45007e364aa282fa12685db1d726891f1 / PACKAGE_IDENTITY_AND_FULL_TARGET_PROOF_VERIFIED / ACTUAL_A_B_TRANSPORT_BYTES_VERIFIED_EQUAL / TRANSPORT_INTERNAL_CHECKSUMS_17_OF_17_EACH / PRODUCT_BYTES_88_OF_88_VERIFIED / PACKAGE_SELFTEST_29_OF_29_PASS / AUCDEV019_RESOURCEWARNING_CLOSURE_ACCEPTED / NEW_PROJECT_OWNED_PRODUCTION_DEPRECATIONWARNING_OBSERVED / PATH_GUARD_LINE_701_MAXSPLIT_POSITIONAL / AUDITOR_EXECUTION_BLOCKED_PENDING_NARROW_COMPATIBILITY_CORRECTION / MODEL_ENGAGEMENTS_USED_0 / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

Authority scope: close the demonstrated warning with the smallest
semantics-preserving correction ONLY. The E652BDB4 package remains valid
historical preparation evidence for its exact target `e652bdb4…`, but any
product-byte correction makes it STALE for execution.

## 2. RED reproduction (before edit; exact observed production warning)

- Exact site: `skill/scripts/path_guard.py:701`, in the `Glob`
  pattern-INITIAL-root branch (`re.split` on the literal chunk before the
  first wildcard metacharacter for patterns beginning `/` or `~`).
- Exact warning text (verbatim, 8× identical occurrences):
  `/home/isa/audit-council-dev/skill/scripts/path_guard.py:701: DeprecationWarning: 'maxsplit' is passed as positional argument`
  followed by the source line `head = re.split(r"[*?\[\]{},]", pattern, 1)[0] \`.
- Interpreter: CPython 3.14.7 (`/usr/bin/python3`).
- Focused relevant tests with all warnings visible
  (`PYTHONWARNINGS=always`; `test_path_guard` 72 OK, `test_review_hardening`
  29 OK, `test_source_write_guard` 6 OK, `test_env_binding` 41 OK): **8
  occurrences**, all reached through the `test_review_hardening.py` Glob
  pattern-root cases (e.g. `{"pattern": "/etc/*"}`); the other three files
  reach the guard through non-pattern inputs and emit none.
- One natural full deterministic suite, default posture
  (`python3 -m unittest discover -s skill/tests`): `Ran 650 tests in
  98.832s` → `OK`, exit 0, with the SAME **8 occurrences** at
  `path_guard.py:701` (unittest's default warning visibility surfaces it —
  no filter was added, removed or configured).
- No other project-owned warning of any category appeared anywhere in the
  complete captured output of either RED run. No additional defect inferred.

## 3. Exact authorized correction (one line; semantics-preserving)

`skill/scripts/path_guard.py:701`, before → after (the ONLY product change):

```diff
-                    head = re.split(r"[*?\[\]{},]", pattern, 1)[0] \
+                    head = re.split(r"[*?\[\]{},]", pattern, maxsplit=1)[0] \
                         or pattern[:1]
```

- `maxsplit` becomes a keyword argument; the regex, the `maxsplit` VALUE
  (`1`), the `[0]` head extraction, the `or pattern[:1]` fallback, the
  surrounding `_classify_path` call and every path-classification decision
  are byte-identical in behavior. `re.split(pattern, string, maxsplit=1)`
  is the documented spelling of the identical call.
- NOT done (held boundaries): no regex change; no path-classification
  behavior change; no refactor of `path_guard.py`; no schema/contract/
  prompt/sandbox change; no warning suppression; no warning filters added.
- No new test: existing `test_review_hardening.py` Glob pattern-root
  coverage exercises the changed line (it produced the 8 RED occurrences),
  so semantic equivalence is established by existing coverage alone.
- Commit identity (Commit 1, sole parent
  `d0af87991993fc77c8b3f1e7c91baa7a76402981`):
  `FINAL_REAUDIT_WARNING_CLEAN_CANDIDATE_SHA` =
  `26d8730fe11834eb4be629db3a07e9ec83c4fd46`; tree
  `f6b961f7061a2e955fa99ea4da960040def5804e`; `skill/` tree
  `5a3fd4be796c5f10077eff5c9ebbc3a0277180f3`; exactly ONE changed product
  path, +1/−1.

## 4. Focused regression (warnings visible)

`PYTHONWARNINGS=always` over the directly relevant path-guard/hook tests,
all PASS with rc=0: `test_path_guard` 72 (3.599 s), `test_review_hardening`
29 (5.487 s), `test_source_write_guard` 6 (1.969 s), `test_env_binding` 41
(1.819 s) — 148/148 OK. Markers in complete captured output:
**0 DeprecationWarning, 0 ResourceWarning, 0 `Exception ignored`, 0
`path_guard.py:701` occurrences.**

## 5. Full warning census (complete output parsed, not exit code alone)

- Warning-visible complete deterministic suite
  (`PYTHONWARNINGS=always` + `PYTHONTRACEMALLOC=15`):
  `Ran 650 tests in 452.821s` → `OK`, exit 0. Complete output parsed:
  **0 project-owned DeprecationWarning, 0 project-owned ResourceWarning,
  0 `Exception ignored` — and zero warning lines of ANY category**
  (project-owned or otherwise).
- Warning-as-error posture sufficient to cover BOTH categories
  (`PYTHONWARNINGS=error::ResourceWarning,error::DeprecationWarning`):
  `Ran 650 tests in 99.248s` → `OK`, exit 0; parsed output contains no
  warning occurrence (the only two category-name mentions in the log are
  the echoed command header itself).
- No new project-owned warning class appeared; no unbounded cleanup was
  opened.

## 6. Regression gates

- Natural full suite ×3 (default posture, post-fix): **650 OK ×3**
  (98.777 s / 99.427 s / 98.245 s; 0 FAIL / 0 ERROR / 0 SKIP; rc=0 each;
  0 DeprecationWarning / 0 ResourceWarning / 0 `Exception ignored` each).
- Isolated clean-environment suite (`env -i`, fresh
  HOME/XDG/AUDIT_COUNCIL_CACHE_HOME/AUDIT_COUNCIL_ENV_ROOT):
  `Ran 650 tests in 80.665s` → `OK (skipped=7)` (a second identical-posture
  verbose repetition for skip enumeration: 80.017 s, same result). Skip
  classification EXACTLY canonical, verbatim: `da27c0 archive not present`
  ×1; `production codex toolchain not on PATH (external condition,
  explicitly classified)` ×5; `smoke artifacts not present on this machine`
  ×1 — the same seven as all prior campaigns. Zero warning markers.
- `git diff --check`: CLEAN (base → candidate; re-verified before each
  commit and before push).
- Test count unchanged at 650 before and after (no tests added/removed);
  no failed intermediate run discarded (every executed run is recorded in
  the handoff archive).

## 7. Effect on the final package (staleness)

Because the production target bytes change, the frozen event/package
`AUCDEV-010-BRQ-FINAL-E652BDB4-20260914-01` (binding_version 1, target
`e652bdb45007e364aa282fa12685db1d726891f1`) becomes:

`STALE_TARGET_SUPERSEDED_BY_DEPRECATIONWARNING_COMPATIBILITY_CORRECTION`

The package, its FROZEN-DIGEST-RECORD and its handoff archive are NOT
mutated, resealed or repacked; they remain valid historical preparation
evidence for the exact target `e652bdb4…` only (the readback-verified
identity/parity/transport properties of the package itself are unaffected).
The correction successor
`26d8730fe11834eb4be629db3a07e9ec83c4fd46` is the ONLY candidate eligible
for ONE fresh final A/B package preparation (subject to Control Room
readback of THIS publication and a NEW package-preparation + execution
authority chain). The older `AUCDEV-010-BRQ-FINAL-5627B9EE-20260913-01`
package remains `STALE_TARGET_SUPERSEDED_BY_AUCDEV019_CLEANUP` (preserved
untouched).

## 8. Canonical result state

- `AUCDEV_010_FINAL_PREAUDIT_DEPRECATIONWARNING_CORRECTION_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
- MODEL_ENGAGEMENTS_USED = 0; AUDITOR_A = NOT_STARTED; AUDITOR_B =
  NOT_STARTED; EXECUTION_AUTHORITY = NOT_YET_GRANTED.
- Qualification readiness BLOCKED; qualification NONE; installation NONE;
  installed qualified predecessor NOT ESTABLISHED; bootstrap-root
  exception applicable and unconsumed.
- ZERO model/frontier/provider calls in this session; no auditor launched.

Immediate next action:
`INDEPENDENT CONTROL ROOM READBACK OF THIS DEPRECATIONWARNING COMPATIBILITY CORRECTION PUBLICATION; ONLY IF ACCEPTED, ONE FRESH FINAL A/B PACKAGE PREPARATION AGAINST 26d8730f… AND A SEPARATE EXPLICIT OPERATOR EXECUTION AUTHORITY`

This wording does NOT mean any auditor started, any authority granted, any
model engagement consumed, candidate PASS, qualification readiness,
qualification or installation.

## 9. Publication scope and hygiene

This publication changes exactly: `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`,
`docs/chatgpt-project/AUCDEV-BACKLOG.md`, and NEW
`docs/chatgpt-project/AUCDEV-010-FINAL-PREAUDIT-DEPRECATIONWARNING-CORRECTION.md`
(THIS file). QUALIFICATION-HISTORY untouched. Historical records are not
rewritten; supersession is recorded append-only. Local pre-existing cosmetic
smoke-fixture gitlink worktree entries remain untouched (identical in the
canonical tree; never staged). The FIRST postpush warning-visible gate at
the published HEAD is executed after this publication and its evidence is
recorded in the workspace FINAL-REPORT/handoff archive, not in this file.
