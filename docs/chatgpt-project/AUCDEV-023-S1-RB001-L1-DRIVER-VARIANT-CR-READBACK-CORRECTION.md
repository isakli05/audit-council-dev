# AUCDEV-023 S1 RB-001 L1 DRIVER-VARIANT CONTROL ROOM READBACK CORRECTION — STAGING_READY EXEC-REACH AMBIGUITY

Authority ID: `AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-CR-READBACK-CORRECTION-20260923-01`
Date: 2026-09-23
Task class: **BOUNDED GOVERNANCE CORRECTION-PUBLICATION** — record-only / append-only / zero-runtime / zero-implementation

## 1. Authority and purpose

The preceding Control Room readback publication (canonical record
`docs/chatgpt-project/AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-REMEDIATION-CONTROL-ROOM-READBACK.md`,
commit `c6cf349eb0aa760bebc272c7141480a6d84e2c85`) was **faithfully published**. A subsequent
exact-source re-read by the Control Room found material counter-evidence showing that the
future-remediation requirement recorded in `AUCDEV023-CR-S1-RB001-L1-REM-RB-001` was scoped
**too broadly**. This session is a BOUNDED GOVERNANCE CORRECTION-PUBLICATION RECORD PUBLISHER
ONLY: it verifies the exact boundary source read-only, records the correction finding
`AUCDEV023-CR-S1-RB001-L1-CRRB-CORR-001`, narrows the prospective REM-RB-001 remediation
scope, and publishes the result. It is NOT the operator, NOT Auditor-A/B, NOT the Control Room
decision-maker, NOT an execution controller, NOT an implementation/boundary-launcher/driver/
EBS/package/binding/event-generation/replacement-first-pass/qualification/installation
authority.

**ZERO source remediation is performed in this task.** No predecessor record is rewritten.

## 2. Live bootstrap verification (EXACT)

- Repository `isakli05/audit-council-dev`, branch `master`, remote `origin`.
- Live master resolved by `git ls-remote origin master` AND local `git rev-parse HEAD`:
  `c6cf349eb0aa760bebc272c7141480a6d84e2c85` — EQUALS the authorized baseline EXACT.
- Root tree: `61d73c3940ff2207e3efbdd97c0eac1baf2248dc` — EXACT.
- Sole parent: `8e2f09bfd2ecf1a004e54ce31aabf782f194a3b3` — EXACT.
- Canonical blobs at that SHA, all EXACT:
  - `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` = `27c8ce0ddbc5f792f13635dc385be93ced7f5302`
  - `docs/chatgpt-project/AUCDEV-BACKLOG.md` = `9f47f733b4e733d4df41eb68ec1f1eacb8c9df32`
  - `docs/chatgpt-project/AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-REMEDIATION-CONTROL-ROOM-READBACK.md` = `819f2732a42e13e7e60f2eb67d177e987389ac36`
- Protected trees at that SHA, all EXACT and byte-unchanged:
  - `bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0`
  - `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`
  - `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f`

## 3. Predecessor CR readback identity and generated-LAST predecessor verification (read-only)

Predecessor publication: commit `c6cf349eb0aa760bebc272c7141480a6d84e2c85` (this session's
authorized baseline and sole parent), canonical record blob `819f2732a42e13e7e60f2eb67d177e987389ac36`.

Predecessor generated-LAST reviewer handoff verified read-only EXACT (extraction to a scratch
tempdir for hash/census verification ONLY; ZERO execution of any packaged byte; ZERO mutation):

- Archive: `AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-CR-READBACK-PUBLICATION-HANDOFF.tar.gz`
- Outer SHA-256: `56c3a4608842669f834fd17e32181fe85e8428163758477e5fe46a26ce3ed574` — EXACT
- Size: 756492 bytes — EXACT
- Census: 26 total = 17 regular + 9 directories; 0 unsafe/traversal, 0 duplicates,
  0 symlinks, 0 hardlinks, 0 special — EXACT
- Exactly one `SHA256SUMS` (`handoff/SHA256SUMS`): 16 rows, 16/16 PASS, zero missing,
  zero unlisted — EXACT
- Critical source identities, all EXACT:
  - Successor driver `handoff/candidate/exec05-driver.py` =
    `858b825da55eb04abf127463db92721b7ee44c6323a3316b7382683b0dfddf25` / 149121 bytes
  - Boundary candidate `handoff/candidate/boundary-networked-boundary-launcher.py` =
    `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa` / 41270 bytes
    **(the decisive source for this correction)**
  - (Also verified: predecessor driver `cd4608a972bb3d1023f6a6bf8283189a8e7658bb58ca4bc9b46704f8d7fb617f` / 139721 bytes.)

## 4. Exact boundary source sequence (OBSERVED SOURCE FACT, read-only)

All line numbers are from the verified boundary candidate
`011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa` / 41270 bytes
(`main()`), inspected read-only; nothing was executed or modified:

- **Lines 739–741** — the six base identity fields are assigned
  (`launcher`, `launcher_version`, `role`, `attempt`, `event`, `credential_printed`).
- **Line 742** — `try:` opens the single guarded region.
- **Lines 743–748** — credential / invocation / auditor-path work: `os.lseek(CRED_FD, …)` +
  `read_bounded`, `os.lseek(AUDITOR_INVOCATION_FD, …)` + `read_bounded`, `json.loads`
  (frozen argv parse), `resolve_auditor_path(AUDITOR_EXEC_FD)`. These are the only raising
  sites reachable while `metadata` still holds exactly the base six fields (**INITIAL**
  prefix); all occur before any composition construction or launch.
- **Line 749** — `metadata["auditor_executable_inode_checked"] = True`.
- **Line 755** — `metadata["auditor_executable_is_frozen_package_payload"] = …`.
- **Line 757** — `metadata["invocation_sha256"] = …` (**IDENTITY_ESTABLISHED** prefix from
  here).
- **Lines 759–760** — `staging_dir = os.path.join(…)`; `os.makedirs(staging_dir,
  exist_ok=True)` (a raising site reachable with the IDENTITY_ESTABLISHED prefix, before the
  STAGING_READY assignments and composition launch).
- **Line 761** — `metadata["staging_dir"] = staging_dir`.
- **Line 762** — `metadata["output_name"] = output_name_for(attempt)` (**STAGING_READY**
  prefix from here).
- **Lines 768–769** — `cred_r = _memfd_with(cred)`; `inv_r = _memfd_with(invocation_raw)`.
- **Line 770** — `args = build_composition(…)`.
- **Line 776** — `exec_r, exec_w = os.pipe()`.
- **Line 777** — `displaced = _normalize_exec_status_fd(exec_w)` (+ re-referencing 778–780).
- **Lines 781–787** — data-fd argument construction.
- **Lines 793–795** — `completed = subprocess.run(args, pass_fds=(cred_r, inv_r,
  EXEC_STATUS_FD), stdout=subprocess.DEVNULL, timeout=None)`. **The composition — and the
  synthetic/auditor payload — executes HERE.**
- **Lines 796–803** — AFTER `subprocess.run` returns, still INSIDE the same try:
  `os.close(cred_r)` (796), `os.close(inv_r)` (797), `os.close(EXEC_STATUS_FD)` (801),
  `tokens, eof, oversize = _drain_exec_status(exec_r)` (802), `os.close(exec_r)` (803).
- **Line 804** — `metadata["client_returncode"] = completed.returncode` — assigned ONLY
  AFTER all of the cleanup/drain operations above.
- **Lines 834–841** — the entire try is covered by `except Exception:` which sets
  `metadata["error_class"] = "LAUNCHER_FAILURE"`, emits the finite metadata, and
  `return 3`.

Therefore the **STAGING_READY** metadata prefix (base + three identity fields +
`staging_dir` + `output_name`, with `error_class=LAUNCHER_FAILURE`, rc=3, and NO
`client_returncode`) is emitted from BOTH:

- **A.** genuinely pre-composition / pre-INNER failures (raising sites 768–795 before or
  during `subprocess.run` invocation); AND
- **B.** failures AFTER `subprocess.run` returned (raising sites 796–803: the fd closes and
  the bounded drain), at which point the composition has already run and the payload may
  have executed or even completed, but `client_returncode` has not yet been copied into
  `metadata`.

## 5. New correction finding

- **ID:** `AUCDEV023-CR-S1-RB001-L1-CRRB-CORR-001`
- **Title:** `STAGING_READY_PREFIX_DOES_NOT_PROVE_PRECOMPOSITION`
- **Classification:** HARNESS/PROTOCOL DESIGN / CONTROL-ROOM-READBACK DEFECT / OBSERVED
  SOURCE FACT / IMPLEMENTATION-BLOCKING CORRECTION
- **Support:** OBSERVED SOURCE FACT (Section 4: boundary candidate lines 762–804 and
  834–841, byte-verified identity `011a8713…`).
- **Finding:** the accepted historical outcome-union and the immediately preceding Control
  Room readback treated `rc=3` + no `client_returncode` + legal progressive prefix as
  uniformly V-OUTER-PRE-COMPOSITION / `PROVEN_FALSE`. That is NOT true for the
  STAGING_READY prefix: the same exact prefix is reachable from operations before
  `subprocess.run` AND from cleanup/drain operations after `subprocess.run` completed but
  before the `client_returncode` metadata assignment. A driver-only observer cannot
  distinguish those histories from this prefix alone. **No rc value may repair that
  ambiguity.**
- **Disposition:** recorded in this correction publication; the prospective future-remediation
  requirement of `AUCDEV023-CR-S1-RB001-L1-REM-RB-001` is NARROWED per Section 6. The
  predecessor records are NOT rewritten.

## 6. Corrected REM-RB-001 scope (prospective replacement; earlier record NOT rewritten)

`AUCDEV023-CR-S1-RB001-L1-REM-RB-001` remains a real implementation finding, but its valid
scope is narrowed prospectively as follows.

### 6.1 INITIAL

- Exact prefix: the six base identity fields only.
- All reachable failure sites represented by this exact prefix (boundary lines 743–748)
  occur before composition launch.
- Correct future evidence:
  - `exec_stage_class = PRE_INNER_COMPOSITION_FAILURE`
  - `client_exec_reached = false`
  - `proof_strength = PROVEN_FALSE`
- Transport may remain the appropriate existing no-status transport token.

### 6.2 IDENTITY_ESTABLISHED

- Exact prefix: base fields + `auditor_executable_inode_checked` +
  `auditor_executable_is_frozen_package_payload` + `invocation_sha256`.
- The relevant failure (boundary line 760, `os.makedirs`) is before the STAGING_READY
  assignments and composition launch.
- Correct future evidence:
  - `exec_stage_class = PRE_INNER_COMPOSITION_FAILURE`
  - `client_exec_reached = false`
  - `proof_strength = PROVEN_FALSE`

### 6.3 STAGING_READY

- Exact prefix: IDENTITY_ESTABLISHED + `staging_dir` + `output_name`.
- This prefix is **NOT a proof of pre-composition.** It covers failures across the
  subsequent composition + cleanup/drain region (boundary lines 768–803) before the
  `client_returncode` metadata assignment (line 804).
- Correct future evidence MUST remain fail-closed:
  - `client_exec_reached = null`
  - `proof_strength = UNDETERMINED`
- Do NOT relabel this prefix `PRE_INNER_COMPOSITION_FAILURE`. Do NOT claim `PROVEN_FALSE`.
- The existing finite `EXEC_STATUS_PROTOCOL_VIOLATION` representation is acceptable unless
  the future remediation demonstrates a more precise EXISTING enum that does not overclaim.
- Do NOT add a new enum merely for naming convenience.

Mechanical note for the future implementer (observed read-only in the successor driver
`858b825d…`, lines 2132–2137): the current driver persists
`EXEC_STATUS_PROTOCOL_VIOLATION / client_exec_reached=None / UNDETERMINED / NOT_PRODUCED`
uniformly for all three accepted prefixes. Under the corrected scope that behavior is
**correct as-is for STAGING_READY** and must be preserved there; the PROVEN_FALSE
correction applies only to INITIAL and IDENTITY_ESTABLISHED. `PRE_INNER_COMPOSITION_FAILURE`
is already a persisted finite class in the successor driver (`PERSISTED_EXEC_CLASSES`), and
the reference classifier already emits `(PRE_INNER_COMPOSITION_FAILURE, false, PROVEN_FALSE)`
for the `""` token stream, so no new persisted enum is required.

## 7. Effect on the predecessor design contract

- The historical design-remediation record is preserved as historical evidence and MUST NOT
  be rewritten.
- Its broad statement that `V-OUTER-PRE-COMPOSITION` + `rc=3` + no `client_returncode` ⇒
  `PROVEN_FALSE` is **superseded PROSPECTIVELY for the STAGING_READY envelope** by this
  exact source-derived correction.
- This does NOT affect:
  - EBS_BOUNDARY_EXEC_FAILURE `PROVEN_FALSE`;
  - INITIAL pre-composition proof;
  - IDENTITY_ESTABLISHED pre-composition proof;
  - completed L1 SE semantics;
  - the operator-accepted SE+positive-nonzero-rc+report-absent residual
    (`EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS` / null / UNDETERMINED);
  - report-present proof;
  - rc==0 structural proof.

## 8. REM-RB-002 status — UNCHANGED

`AUCDEV023-CR-S1-RB001-L1-REM-RB-002` (`REJECTED_METADATA_KEYS_COMPUTED_BUT_NOT_PERSISTED`)
remains **OPEN / IMPLEMENTATION-BLOCKING / UNCHANGED**. The future remediation still must
preserve a safe bounded keys-only diagnostic for rejected metadata forms (keys only,
strings only, sorted deterministically, ≤64 entries, each key bounded; NO values, NO raw
JSON, NO exception text, NO report bytes, NO credential data). NOT implemented in this task.

## 9. REM-RB-003 status — UNCHANGED

`AUCDEV023-CR-S1-RB001-L1-REM-RB-003` (`TRANSPORT_FAILURE_VARIANT_NOT_MATERIALIZED`)
remains **OPEN / IMPLEMENTATION-BLOCKING / UNCHANGED**. Future remediation still must
recognize `metadata == {}` + `exec_failed == false` + `timed_out == false` as the finite
transport-failure envelope BEFORE generic identity validation (and after the
higher-precedence timeout and EBS-exec-failure variants), while remaining
`client_exec_reached = null` / `proof_strength = UNDETERMINED`. NOT implemented in this
task.

## 10. INFO-001 status — UNCHANGED

`AUCDEV023-CR-S1-RB001-L1-REM-INFO-001` remains informational and unchanged. Actual driver
diff: **+187 / −20**. Exact diff SHA/size (`022e79cb…`/15928) and source identities remain
valid.

## 11. Resulting source-candidate state

- **Boundary candidate** `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa`
  / 41270 bytes: `ACCEPTED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH` — **DO NOT MODIFY.**
- **Vendored-bwrap fixture evidence**: `ACCEPTED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH`
  — DO NOT rerun unless a genuinely new dependency is introduced.
- **Successor driver** `858b825da55eb04abf127463db92721b7ee44c6323a3316b7382683b0dfddf25`
  / 149121 bytes: **NOT PACKAGE-PREPARATION READY.**
- Correct future driver remediation scope (driver-only; boundary NOT modified):
  1. INITIAL → `PRE_INNER_COMPOSITION_FAILURE` / `false` / `PROVEN_FALSE`
  2. IDENTITY_ESTABLISHED → `PRE_INNER_COMPOSITION_FAILURE` / `false` / `PROVEN_FALSE`
  3. STAGING_READY → preserve `UNDETERMINED` (fail-closed; no PROVEN_FALSE claim)
  4. persist safe bounded rejected-metadata key evidence (REM-RB-002)
  5. materialize the finite transport-failure variant (REM-RB-003)
- No completed-L1 semantic change.
- **RB-001 remains OPEN** (historical classification COMPLETENESS LIMITATION /
  FAILURE-DIAGNOSTIC EVIDENCE GAP / OBSERVED FACT / ROOT_CAUSE_UNRESOLVED /
  NO_PRODUCT_DEFECT_CONCLUSION_YET unchanged; operator-accepted L1 ambiguity residual
  recorded separately and still implemented honestly).
- **AUCDEV-023 remains P1 / READY / NOT DONE.**

## 12. Authority barriers

Package preparation authority = NONE. MANIFEST regeneration authority = NONE. Binding
regeneration authority = NONE. Event generation authority = NONE. Replacement execution =
NONE. Auditor/provider execution = NONE. Qualification = NONE. Installation = NONE.
Implementation in this task = NONE (source NOT remediated here). The Auditor-A frozen
report `ba8a29a12867273616143e48a86f101f14f6e0e207136d83b31e7fd2426ec1a0` / 23727 B / 0444
is referenced mechanically ONLY and was NEVER opened; the vendored frozen bwrap
`01fb705f067bd5365b63d8ad2323a61c8d007733ca5e649437e086f3fb9935d8` / 529776 B was NOT
executed. ZERO credentials read. ZERO provider/model/frontier probe. ZERO network probe
beyond `git ls-remote` publication mechanics. ZERO report-substance read.

## 13. Next action — EXACTLY ONE

**CONTROL ROOM PREPARATION OF THE CORRECTED NARROW DRIVER-ONLY REMEDIATION PROMPT FOR THE
TWO PROVEN-FALSE EARLY PREFIXES (INITIAL and IDENTITY_ESTABLISHED), REJECTED-METADATA-KEY
PERSISTENCE (REM-RB-002), AND TRANSPORT-FAILURE MATERIALIZATION (REM-RB-003), WHILE
PRESERVING STAGING_READY AS UNDETERMINED, BEFORE ANY PACKAGE / MANIFEST / BINDING / EVENT
PREPARATION AUTHORITY.**
