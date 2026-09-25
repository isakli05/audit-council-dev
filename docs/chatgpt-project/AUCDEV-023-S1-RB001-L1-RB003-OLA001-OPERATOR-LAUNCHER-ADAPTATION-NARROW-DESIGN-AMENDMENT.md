# AUCDEV-023 S1 RB-001 L1 RB-003 OLA-001 Operator-Launcher Adaptation — Narrow Design Amendment

**OLA001_NARROW_DESIGN_AMENDMENT = PREPARED_FOR_CONTROL_ROOM_READBACK / EXACT_PREDECESSOR_REPORT_INVALID_VERIFIER_DELTA_EXPLICITLY_DEFINED / ALL_OTHER_DRIVER_CONTROL_FLOW_HELD / EXISTING_NONCONFORMING_CANDIDATE_NOT_RETROACTIVELY_ADMITTED / FUTURE_REIMPLEMENTATION_REQUIRED / NO_PRELAUNCH_AUTHORITY / ZERO_RUNTIME**

Design authority: `AUCDEV-023-S1-RB001-L1-RB003-OLA001-NARROW-DESIGN-AMENDMENT-20260925-01`, over held finding `AUCDEV023-CR-S1-RB001-L1-RB003-OLA-001` (opened by the Control Room readback published at commit `41ba1012f2195879dfc30443e37ff0843a281ba6`).

Session role: **BOUNDED DESIGN-AMENDMENT AUTHOR / READ-ONLY EVIDENCE COLLECTOR** — NOT the Control Room decision-maker, NOT an implementation executor, NOT a prelaunch activator, NOT a deployment authority, NOT an execution controller, NOT an execution-authority grantor, NOT Auditor-A or Auditor-B, NOT a qualification authority, NOT an installation authority. This task DESIGNS the permitted semantic delta ONLY. It modified, chmod'd, executed, imported, replaced, deployed, activated and admitted NOTHING — the current candidate driver/wrapper are untouched (both still mode 0600), and this amendment does NOT retroactively convert their original nonconforming implementation authority into a conforming one. A future separately authorized implementation must establish conformance to this amendment.

Resulting finding state: **`OLA-001` remains OPEN / DESIGN_AMENDMENT_PREPARED_PENDING_CONTROL_ROOM_READBACK** (NOT closed by this task; maximum allowed state reached).

## 1. Live bootstrap (all EXACT; NO drift)

Live `origin/master` == local HEAD == `41ba1012f2195879dfc30443e37ff0843a281ba6` (branch `master`; root tree `f9f9bc7a32a60043e6c3c7b8c2f8ea07758d87cd`; sole parent `9888722a16e491a8d5c1cd7c3a1cefbf531d8c19`), resolved by the mandated `git ls-remote`. Blobs at the base verified EXACT: CURRENT `de775487c26243608f093639a1e6f3fb3a32c83e`, BACKLOG `f9b7d7715a015796043b009f53087b834557dc94`, OLA implementation CR readback `d01fd73ddf028b7e67e4d2a917ba2f4bb7d1cac6`, OLA implementation record `072dbbccb715b93d7b3e60b947b3af8222f94407`, corrected package-prep CR readback `7e483ba34f475a6bd0aecfd26c13e8887c803ecb`. Protected trees exact: `bootstrap-supervisor 732b8def9f22d7c466ce77f3d3049da53bfff3d0`, `qualification-harness 5b8d5e5465923740470ff63ed9b8683f257a3787`, `skill c792933a862d9a5434681a88d183470dd8b15d2f`. The two tracked working-tree entries `smoke-fixture` / `smoke-fixture-103` are the pre-existing unrelated gitlink drift outside governed/protected paths — recorded, NOT staged, NOT normalized. No auto-rebase anywhere.

## 2. Held finding (held verbatim; NOT closed)

**`AUCDEV023-CR-S1-RB001-L1-RB003-OLA-001` — PREDECESSOR_REPORT_STATE_TRANSITION_REQUIRES_UNAUTHORIZED_VERIFIER_DELTA** — HARNESS / PROTOCOL DEFECT / CONTROL-ROOM IMPLEMENTATION-INSTRUCTION CONTRADICTION / AUTHORITY-CONFORMANCE GAP / OBSERVED FACT / PRELAUNCH-BLOCKING; state before this task OPEN / NARROW_DESIGN_AMENDMENT_REQUIRED; state after this task **OPEN / DESIGN_AMENDMENT_PREPARED_PENDING_CONTROL_ROOM_READBACK**. This amendment is the narrow design remedy that finding required; it does not close the finding and does not decide admission.

## 3. Non-retroactivity

Existing candidate artifacts (both re-hashed EXACT read-only this session, never executed/imported):

- Driver `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-4a51f4b9.py` — SHA-256 `15198c024123f2471e85f8114ed783ee183a808c219b3f89b59465a1b9711b25` / 165489 B / 3335 lines / isa:isa / mode **0600**.
- Wrapper `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-4a51f4b9.sh` — SHA-256 `1366785b957c29c9e8b861ddaba0c6aab30d1c1f2297152bb9acfe2585af5c96` / 3408 B / 82 lines / isa:isa / mode **0600**; wrapper pins re-read: `REQUIRED_DRIVER_SHA256="15198c02…"` (the exact final driver bytes) and `REQUIRED_DRIVER_MODE="700"` (the intentional 0600/700 mismatch keeps the wrapper non-executable and refusing its driver until a separately authorized prelaunch stage).

Both remain **PREPARED / NON-EXECUTABLE / NOT_ADMITTED_FOR_PRELAUNCH**. The Control Room already classified their implementation authority as NONCONFORMING (OLA-001); this amendment does NOT rewrite that history and does NOT retroactively admit the existing bytes for chmod/prelaunch/deployment/execution. Their bytes are used here READ-ONLY as evidence of the exact proposed delta. A future separately authorized implementation must be built and must demonstrate conformance to §5–§9 of this amendment from its own evidence.

## 4. The exact contradiction being resolved

The historical RB002 launcher baseline (driver `aucdev023-firstpass-rb001-l1-rb002-60636835.py`, SHA-256 `fd977a9d6c6b819d1d3af055fb3073ae2a01a00e5f2c665697056914d530b784` / 163646 B / 3305 lines, re-hashed EXACT read-only, never executed) expected the predecessor Auditor-B report surface to be ABSENT: `phase0_operator_host_check` walks the predecessor B attempt root and refuses if ANY report-suffixed artifact exists (`HISTORICAL_PREDECESSOR_B_REPORT_MUST_REMAIN_ABSENT`, historical lines 1364–1375).

The current actual predecessor `evt-60636835d5fd6f37` is terminal Auditor-B `REPORT_INVALID / TERMINAL` — mechanically re-verified this session: B accounting `/home/isa/aucdev023-s1-prep002-rem002/attempts/evt-60636835d5fd6f37-B-01/accounting/evt-60636835d5fd6f37-B-01.jsonl` = SHA-256 `4e26b9afa7629a8233ac6cd4f71a429d617e594825ed36dd67b574ec82f8f6e9` / 5611 B / mode 0600, states exactly `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_INVALID → TERMINAL`; the attempt root contains EXACTLY the accounting file plus one sealed invalid snapshot at its exact staging pathname `…/evt-60636835d5fd6f37-B-01/staging/evt-60636835d5fd6f37-B-01.first-pass-report.json` = SHA-256 `6a1f079f68932f4249b17996f61b4624dc5d415c56fa0ed08cd5073b2f659387` / 202 B / mode 0600 (identity-only re-hash; substance NEVER opened); `custody-out` EMPTY.

Therefore a launcher adapted for the current predecessor cannot truthfully retain the historical invariant "B report artifacts MUST remain ABSENT". The prior implementation instruction simultaneously required exact predecessor state verification AND zero behavioral delta — not simultaneously satisfiable. That contradiction is the SOLE design issue amended here.

## 5. Exact semantic delta authorized for future implementation

**`AUTHORIZED_PREDECESSOR_REPORT_STATE_VERIFIER_CHANGE`** — exactly ONE behavior-class change, located ONLY inside `phase0_operator_host_check`. The predecessor Auditor-B report-state verifier may change from `HISTORICAL_PREDECESSOR_B_REPORT_MUST_REMAIN_ABSENT` to a fail-closed exact-identity verifier requiring all of:

- **A.** the sole report-like artifact under the predecessor B attempt root is exactly the expected sealed invalid snapshot pathname (i.e. the walked report-suffixed-path list equals EXACTLY the one pinned staging pathname — absence, extra report artifacts and pathname mismatch all fail);
- **B.** that pathname is a regular file (enforced semantically by the `os.path.isfile` guard: a non-regular file yields identity `None` ⇒ refusal);
- **C.** its exact mechanical identity matches SHA-256 `6a1f079f68932f4249b17996f61b4624dc5d415c56fa0ed08cd5073b2f659387`, size 202, mode 0600;
- **D.** any absence, additional report artifact, pathname mismatch, non-regular file, hash mismatch, size mismatch or mode mismatch fails closed with `DriverStop` (single fail-closed refusal conjunction; refusal token e.g. `HISTORICAL_PREDECESSOR_B_REPORT_IDENTITY_REFUSED`);
- **E.** verification is identity-only: no opening/parsing/reproducing report substance beyond the bytes required for SHA-256 hashing (hash/stat only);
- **F.** the exact identity is recorded into the mechanical historical-immutable evidence structure (e.g. `historical_immutable["historical_predecessor_B_report_identity"]`).

This is NOT a general authorization to alter Phase 0, and NOT an authorization to interpret, validate or reuse report substance.

## 6. Allowed implementation shape

A future implementation MAY introduce only the minimum data/statement surface needed for §5, including equivalents of: `b_snapshot`; `b_report_identity`; `os.path.isfile(...)`; `os.lstat(...)`; `sha256_file(...)`; and storage of `historical_predecessor_B_report_identity`. A single fail-closed exact-identity refusal conjunction is permitted. New module constants may include ONLY the exact predecessor B invalid-snapshot SHA (`6a1f079f…`), size (202) and mode (`0o600`) pins plus already-required identity-rebinding data. Exact variable names are not required; any semantic difference from this design must be shown equivalent.

## 7. Explicitly forbidden driver changes

No other semantic/control-flow change is authorized. In particular DO NOT alter: repository admission; source trust anchor; governed-path policy; package verification; `EXPECT_NEW` semantics; `EXPECT_OLD` event/package semantics other than the already accepted identity rebinding; deployment classification; deployment ordering; the ALREADY_NEW refusal; the deployment-in-single-wrapper-invocation invariant; Phase 3 deployed re-verification; attempt preparation; Auditor-A-first ordering; the Auditor-B-after-conforming-A gate; AccountingStore semantics; credential resolution/custody ordering; dynamic gate ownership; boundary invocation; report custody; the structural validator; conformance evaluation; engagement accounting; barrier logic; retry/resume/fallback refusal; handoff generation; `run_pipeline`; `main`. **No new success path. No new retry path. No bypass. No downgrade of any fail-closed gate.**

## 8. Required future implementation acceptance classification

The contradictory old requirement — every differing function only `RAW_AST_UNCHANGED` or `LABEL_OR_EVIDENCE_NAME_ONLY` — is SUPERSEDED for future OLA reimplementation by: every function must classify EXACTLY one of

1. `RAW_AST_UNCHANGED`;
2. `LABEL_OR_EVIDENCE_NAME_ONLY`;
3. `AUTHORIZED_OLA001_PREDECESSOR_REPORT_STATE_VERIFIER_DELTA`.

Category 3 is permitted for `phase0_operator_host_check` ONLY, with maximum cardinality **1 function**. All other functions: zero unauthorized structural differences. Future AST/fingerprint evidence MUST compare: called names; store targets; branch counts; loops; exception handlers; raises; returns; Pass/Continue/Break; non-string constants; control-flow-affecting operators. Any structural difference outside the exact §5 verifier ⇒ STOP = `UNAUTHORIZED_DRIVER_BEHAVIOR_CHANGE`.

## 9. Fail-closed character of the delta (explicitly established)

The authorized delta: narrows acceptance to ONE exact historical artifact identity (it replaces "anything present fails" with "only this exact artifact at this exact pathname with this exact hash/size/mode passes"); cannot transform a mismatch into success (the refusal is a disjunction of `!=` / `is None` failure conditions — every deviation raises; there is no else/success branch, success is only fall-through of an all-exact match); introduces NO retry; NO fallback; NO alternative predecessor; NO report-content interpretation (identity-only hash/stat); NO provider/model interaction; NO deployment behavior; NO authority transition. The change exists solely because the mechanically true predecessor state changed from `REPORT_MISSING` / no B report artifact to `REPORT_INVALID` / exact sealed invalid snapshot present. The amended verifier is the structural mirror of the already-existing Auditor-A exact-identity verifier (`HISTORICAL_PREDECESSOR_A_REPORT_IDENTITY_REFUSED`, same call family, same conjunction style) in the same function.

## 10. Held fresh-event/package state (preserved without redesign)

Admitted fresh event `evt-4a51f4b9413a1476`; attempts `evt-4a51f4b9413a1476-A-01` / `-B-01` (re-verified ABSENT from the real launcher root; 24 historical roots unchanged; future staging `event.staging.rb001-l1-rb003-4a51f4b9` and future backup `event.backup.pre-rb003-corrected-successor-event` ABSENT; five-backup set present untouched). Fresh identities re-verified EXACT read-only this session through the exact live EBS (plane manifest `d683f64d…` / package `d42aa9e3…` PASS; `parse_binding` + `binding.digest` + `verify_event_package` PASS both roles; per-file payload-set verification inside the EBS):

| Role | binding-file | canonical digest | MANIFEST | package | rows / payload B |
|---|---|---|---|---|---|
| A | `f2dada28ecab4ea850a8f4e820047d2493d9751e2bec357bc714bfad77ede755` | `168d6678d401439fd262f785114acf155681df447b90162c32efe4bc47b9b3be` | `f0898c99ef43b097c70ccaec458e107ef1091f0fa66fedd4f67bcce55fbc97da` | `206cd496fec835f11b8150fdcaaa9e7e20222a15ea9cfe7fc1a9765b151cbbfc` | 191 / 236321909 |
| B | `121f359dd7ab8dfaf0ffcf0f1bcd3365d27dd3a10c8c2adfc214ed69cc693325` | `35169ee5724d886ea3c6ef1e559cda87f0812f91e5d153de2d7b630fab3b0663` | `ddfcc31fbb67c8db51e2a5a4154d65ab17343da31bfe94b7771e51f4b78b436c` | `9a1809559b75d2d98ae22456d87c51e535c81adc649be2ecfd52d5224ee6f4fd` | 194 / 343453864 |

EXEC-RB-004 single-writer semantics remain unchanged. `AUCDEV023-CR-S1-RB001-L1-RB003-PREP-001` remains CLOSED.

## 11. Reserved authority / runtime state (zero-state preserved)

Reserved future authority `AUCDEV-023-S1-RB001-L1-RB003-FIRSTPASS-EXEC-20260925-01` remains RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE. This design task performed: chmod NONE; deployment NONE; runtime attempts NONE; credential read NONE; dynamic real gates NONE; boundary execution NONE; Auditor-A/B NONE; provider/model execution ZERO; qualification NONE; installation NONE. The candidate driver/wrapper remain mode 0600. Historical RB002 authority `AUCDEV-023-S1-RB001-L1-RB002-FIRSTPASS-EXEC-20260924-01` remains CONSUMED/TERMINAL/CLOSED/NO_RERUN (2/2 engagements USED).

## 12. Design disposition

**OLA001_NARROW_DESIGN_AMENDMENT = PREPARED_FOR_CONTROL_ROOM_READBACK / EXACT_PREDECESSOR_REPORT_INVALID_VERIFIER_DELTA_EXPLICITLY_DEFINED / ALL_OTHER_DRIVER_CONTROL_FLOW_HELD / EXISTING_NONCONFORMING_CANDIDATE_NOT_RETROACTIVELY_ADMITTED / FUTURE_REIMPLEMENTATION_REQUIRED / NO_PRELAUNCH_AUTHORITY / ZERO_RUNTIME.** `OLA-001` remains OPEN / DESIGN_AMENDMENT_PREPARED_PENDING_CONTROL_ROOM_READBACK. NOT closed by this task.

## 13. Design evidence (read-only, independently collected this session)

1. **Historical baseline verifier** — `fd977a9d…` lines 1364–1375: walk of predecessor B attempt root; `if b_reports:` ⇒ `DriverStop` `HISTORICAL_PREDECESSOR_B_REPORT_MUST_REMAIN_ABSENT`. Excerpt archived (`verifier-excerpts.txt`).
2. **Current terminal predecessor state** — B accounting `4e26b9af…`/5611/0600 states `PREPARED→GATES_PASSED→CONSUMED_PRE_EXEC→EXEC_ATTEMPTED→REPORT_INVALID→TERMINAL`; attempt-root census = accounting + ONE sealed snapshot; `custody-out` empty.
3. **Sealed snapshot identity** — `6a1f079f68932f4249b17996f61b4624dc5d415c56fa0ed08cd5073b2f659387` / 202 / 0600 at the exact staging pathname (identity-only hash/stat; substance NEVER opened).
4. **Exact existing candidate structural delta** — static `ast.parse` only (neither file executed/imported): 52 top-level functions, names+order identical; **50 `RAW_AST_UNCHANGED`; 1 `LABEL_OR_EVIDENCE_NAME_ONLY` (`build_handoff`, title string only); exactly 1 structurally different function = `phase0_operator_host_check`.** Qualified-call multiset delta: +1 each `os.path.join`, `os.path.isfile`, `os.lstat`, `oct`, `sha256_file` (all already called in the function — no new callee). Store-target delta: +`b_snapshot`, +`b_report_identity` (×2), +`info`, +1 store into `historical_immutable["historical_predecessor_B_report_identity"]`. Shape delta: If +1 (the isfile guard), BoolOp +1, Compare +5 (the exact-path/hash/size/mode conjunction) — NOTHING else. Non-string constants: +`4095` (the `0o7777` mask already used by the A-report block), +`None` ×2. Module-level assignment diff: 21 changed constants (14 event/adaptation rebinds + 7 `HISTORICAL_EXEC05_*` terminal-pin updates — exactly the authorized rebind set) + 3 new constants (`HISTORICAL_EXEC05_B_REPORT_SHA='6a1f079f…'`, `_SIZE=202`, `_MODE='0o600'`) + 0 removed.
5. **Fail-closed proof for the candidate delta** — Pass/Continue/Break deltas **0/0/0**; For 7=7, While 0=0 (**no new loop**); Try/ExceptHandler 2=2 (**no new handler**); Raise 16=16 (**no new raise path**); Return 0=0 (**no new success/early-exit return**); the refusal remains ONE fail-closed `DriverStop` + `STOP_SUFFIX` raise whose condition is a pure disjunction of failure terms (**no retry, no fallback, no bypass**).
6. **Old vs amended predicate** — OLD (historical 1372–1375): `if b_reports: raise DriverStop(... "HISTORICAL_PREDECESSOR_B_REPORT_MUST_REMAIN_ABSENT: " ...)` — absence invariant. NEW (candidate 1386–1405): `b_report_identity = None; if os.path.isfile(b_snapshot): info = os.lstat(b_snapshot); b_report_identity = {sha256: sha256_file(b_snapshot), size: info.st_size, mode: oct(info.st_mode & 0o7777)}; historical_immutable["historical_predecessor_B_report_identity"] = b_report_identity; if b_reports != [b_snapshot] or b_report_identity is None or sha != PIN or size != PIN or mode != PIN: raise DriverStop(... "HISTORICAL_PREDECESSOR_B_REPORT_IDENTITY_REFUSED: " ...)` — pinned exact-identity invariant. Excerpts archived side by side.
7. **Fresh package identities held** — §10 table re-verified EXACT through the exact live EBS (`verify_event_package` PASS both roles; binding-file/digest/MANIFEST/package/rows/payload all exact; package bytes untouched).

## 14. Allowed-vs-forbidden semantic delta matrix

| Surface | Allowed? | Notes |
|---|---|---|
| `phase0_operator_host_check` predecessor-B verifier: absence invariant → exact-identity invariant | **YES — the sole authorized delta** | §5 A–F; fail-closed conjunction only |
| New pins: B snapshot SHA/size/mode + identity-rebinding data | YES | §6; nothing else |
| Recording `historical_predecessor_B_report_identity` into historical-immutable evidence | YES | §5 F |
| Any change to the other 51 functions beyond `RAW_AST_UNCHANGED` / label-only | NO | `build_handoff` label-only accepted shape |
| Repository admission / trust anchor / governed-path policy / package verification / EXPECT_NEW / EXPECT_OLD (beyond accepted rebind) / deployment classification or ordering / ALREADY_NEW refusal / single-invocation deployment / Phase 3 re-verification / attempt preparation / Auditor-A-first ordering / B-after-conforming-A gate / AccountingStore / credential custody / dynamic gate ownership / boundary invocation / report custody / structural validator / conformance evaluation / engagement accounting / barrier logic / retry-resume-fallback refusal / handoff generation / `run_pipeline` / `main` | NO | §7 verbatim |
| New success path / retry path / bypass / gate downgrade / report-substance access / provider-model interaction / authority transition | NO | §7, §9 |

## 15. Publication

Exactly three changed tracked paths over base `41ba1012f2195879dfc30443e37ff0843a281ba6`: NEW canonical design-amendment record (this file) + `AUCDEV-CURRENT-STATE.md` (current-facing fields rotation lines 3/11/23–25 + one dated record appended) + `AUCDEV-BACKLOG.md` (one dated record appended with blank separator; prior content byte-identical prefix). Exactly ONE bounded docs-only fast-forward publication commit whose sole parent is `41ba1012…`, with live master re-resolved EXACT immediately before staging (no auto-rebase; STOP on drift). NOT modified: the candidate driver, the candidate wrapper, the OLA implementation record, the OLA implementation CR readback, packages, deployed event, attempts, protected trees, `AUCDEV-ARCHITECTURE-SUMMARY.md`, `AUCDEV-QUALIFICATION-HISTORY.md`. The generated-LAST reviewer handoff is produced after this push and the post-push readback with nothing included mutated afterward.

## 16. Next action — EXACTLY ONE

CONTROL ROOM READBACK OF THE OLA-001 NARROW DESIGN AMENDMENT BEFORE ANY REIMPLEMENTATION OR ADMISSION OF AN RB003 OPERATOR-LAUNCHER CANDIDATE, PRELAUNCH TRANSITION DESIGN, CHMOD-TO-0700 ACTIVATION, DEPLOYMENT, RUNTIME ATTEMPT CREATION, CREDENTIAL READ, EXECUTION-AUTHORITY GRANT, AUDITOR/PROVIDER EXECUTION, QUALIFICATION, OR INSTALLATION.
