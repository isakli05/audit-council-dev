# AUCDEV-023 S1 RB-001 L1 RB-003 EXEC-RA-001 PCH1 — Replacement Prelaunch Transition Design (PCH1 Candidate Executable-Mode Activation, Deployment, and Single-Use Execution-Authority Transition)

- **Publication date:** 2026-09-26 (Europe/Istanbul)
- **Design authority:** `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN-20260926-01` (collision-swept BEFORE use: ZERO occurrences across the git tracked tree at the base, full git history `--all -S` and commit messages, the working tree, `/home/isa` top-level workspace names, and repo-root archive names).
- **Subject reserved future execution authority:** `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` — current state exactly `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE`.
- **Session class:** BOUNDED PRELAUNCH TRANSITION DESIGNER / READ-ONLY EVIDENCE COLLECTOR ONLY. This session DESIGNS — but does NOT perform — the future human-operator GRANT, the exact 0600→0700 chmod-only activation, the mandatory fresh exact-EBS package-byte reverification, the prelaunch gates, and the single-use fail-closed authority transition for the Control-Room-accepted PCH1 replacement operator-launcher candidate. This session is NOT the Control Room decision-maker, NOT the human operator granting execution, NOT a grant publisher, NOT a prelaunch activator, NOT a deployment authority, NOT an execution controller, NOT Auditor-A/B, NOT a credential-content reader, NOT a qualification authority, NOT an installation authority. **Writing, quoting, recording or discussing the future GRANT phrase inside THIS design record DOES NOT GRANT IT. THIS SESSION RECORDS: HUMAN OPERATOR GRANT = NONE.**
- **Zero-runtime attestation:** NOTHING in this task was chmod'd, deployed, staged, attempted, accounted, credential-read (contents), gated, launched or executed. The accepted candidate driver `7a8389a3…` was NEVER imported or executed (full static analysis of all 3352 source lines by pure non-executing `ast.parse` + read-only hashing only; per R-PIMP-CR-1 NO exec-based candidate evaluation was used). The accepted wrapper `5423ec76…` was NEVER executed (full read + `bash -n` parse only). NO execution authority was granted, consumed or broadened. NO dynamic real gate ran. NO package payload byte was re-hashed (the fresh exact-EBS package-byte reverification is DESIGNED here as a MANDATORY FUTURE GATE, not performed).

## 0. Design disposition

**`PCH1_REPLACEMENT_PRELAUNCH_TRANSITION_DESIGN = READY_FOR_CONTROL_ROOM_READBACK / ACCEPTED_CANDIDATE_EXACT_ARTIFACTS_BOUND / PRELAUNCH_MODE_BARRIER_CONFIRMED / EXACT_FUTURE_HUMAN_GRANT_TARGET_DEFINED / FRESH_EXACT_EBS_PACKAGE_BYTE_REVERIFICATION_REQUIRED_BEFORE_CHMOD / CURRENT_PREDECESSOR_GATES_DEFINED / REPOSITORY_AUTHORITY_NAMESPACE_GATES_DEFINED / CREDENTIAL_METADATA_ONLY_GATE_DEFINED / CHMOD_ONLY_POST_GRANT_ACTIVATION_DEFINED / DEPLOYMENT_REMAINS_INSIDE_SINGLE_HUMAN_DIRECT_INVOCATION / SINGLE_USE_FAIL_CLOSED_AUTHORITY_CONSUMPTION_DEFINED / WRAPPER_PREEXEC_CONSUMPTION_RESIDUAL_CARRIED / NO_RETRY / NO_RESUME / NO_FALLBACK / R_PIMP_CR_1_CARRIED / NO_GRANT / NO_CHMOD / NO_DEPLOYMENT / ZERO_RUNTIME / NO_EXECUTION_AUTHORITY / NO_QUALIFICATION / NO_INSTALLATION`**

No STOP condition was reached. Every held state (Section 3) was re-verified read-only EXACT this session at identity/metadata strength. The subject execution authority remains `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE` — UNCHANGED by this publication.

## 1. Mandatory live bootstrap (verified EXACT — no drift)

| Identity | Value | Result |
|---|---|---|
| Live branch | `master` | EXACT |
| Live HEAD (`git ls-remote origin master`) | `29a264472180524918a5781afc82c8cf25dd81f7` | EXACT |
| Root tree | `b9af0d995067a3e69fb1c89bfe54b3faab24523c` | EXACT |
| Sole parent | `ce88d0c3ebc43b4a2e8d3f6d7a530954f06f32dd` | EXACT (exactly one parent) |
| Local HEAD == FETCH_HEAD after fetch at the exact base | `29a26447…` | EXACT |

Canonical blobs at the base (all EXACT):

| Record | Blob |
|---|---|
| `AUCDEV-CURRENT-STATE.md` | `5fd97d9368b70aa0b8f6394b8058964d17917832` |
| `AUCDEV-BACKLOG.md` | `1bf85b2adf0dc92c2dd7fe671e5c3ee91c0821dd` |
| PCH1 implementation Control Room readback | `9dd9cf9c674cf301af5ee3aa070d138bf9a73702` |

Protected trees at the base (all EXACT): `bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0`; `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`; `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f`. Lineage HELD: trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor; ZERO merges since anchor; 34 changed paths since anchor ALL under `docs/chatgpt-project/` with 0 offending; tracked working-tree drift limited to the pre-existing `smoke-fixture`/`smoke-fixture-103` gitlink drift outside every governed/protected path — recorded honestly, NOT staged, NOT treated as a collision.

## 2. Input implementation-readback handoff — verified READ-ONLY, ZERO members executed

`/home/isa/audit-council-dev/AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-OPERATOR-LAUNCHER-IMPLEMENTATION-CONTROL-ROOM-READBACK-HANDOFF.tar.gz`:

- outer SHA-256 `f72e16ec9de75e8e064d746d8e4469c290adb02f8007abbc8b94b871b099c168` / size 790021 B EXACT; regular isa:isa 0644;
- census EXACTLY 25 members = 22 regular files (21 payload + exactly 1 `SHA256SUMS`) + 3 directories; 0 symlinks, 0 hardlinks, 0 special files; 0 unsafe/absolute/traversal paths; 0 duplicates;
- `SHA256SUMS` exactly 21 rows; 21/21 checksums PASS by read-only streaming re-hash; 0 missing, 0 unlisted;
- canonical equality: the archive copies of the implementation-readback record, CURRENT and BACKLOG are `git hash-object`-EQUAL to the live Git blobs at `29a2644` (9dd9cf9c… / 5fd97d93… / 1bf85b2a…);
- payload inventory: `INDEX.md`, canonical record copies, and 17 evidence files (`01-bootstrap-identity.txt` … `16-post-push-verification.txt`, `cr-independent-classifier.py`). ZERO members executed; read-only byte access for checksum/equality inspection only.

## 3. Held accepted state — re-verified read-only EXACT this session

| Item | Identity | Verified |
|---|---|---|
| PCH1 implementation Control Room readback | `ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH` (record `9dd9cf9c…` at `29a2644`); candidate `ADMITTED_FOR_PRELAUNCH_TRANSITION_DESIGN_ONLY` | held |
| Driver `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.py` | SHA-256 `7a8389a30c9849d0efffd6f6e32b2e9760921eb3a296bfceb4707d660771829b` / 166778 B / 3352 lines / isa:isa (1000:1000) / regular non-symlink / mode 0600 | EXACT (re-hashed this session) |
| Wrapper `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.sh` | SHA-256 `5423ec76ac562844d7fde243aba982dbf96a02e61a6dfbe427c3d311d8120d77` / 3468 B / 82 lines / isa:isa / regular non-symlink / mode 0600 | EXACT (re-hashed this session) |
| Wrapper pins | L44 `DRIVER=` exact candidate path; L45 `REQUIRED_DRIVER_SHA256="7a8389a3…0829b"`; L46 `REQUIRED_DRIVER_MODE="700"` | pins EXACT; **PRELAUNCH MODE BARRIER = CLOSED** (both artifacts 0600 ≠ 700 → wrapper refuses before any interpreter start) |
| Fresh event / attempts | `evt-5cb2c58f855415c3` / `evt-5cb2c58f855415c3-A-01` / `evt-5cb2c58f855415c3-B-01` | PREPARED_ONLY / ABSENT (Section 13) |
| Reserved future authority | `…PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` = `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE` | held; THIS design grants nothing (Section 8) |
| Historical consumed authority | `AUCDEV-023-S1-RB001-L1-RB003-FIRSTPASS-EXEC-20260925-01` | CONSUMED / TERMINAL / CLOSED / NO_RERUN (unused 1/2 engagement budget NOT authority) |
| Deployed predecessor | `evt-4a51f4b9413a1476` (Auditor-A `REPORT_INVALID`/TERMINAL; Auditor-B NOT_RUN) | classifies `EXPECTED_HISTORICAL` inputs satisfied (Section 10) |
| Prior nonconforming candidate | driver `15198c02…` / wrapper `1366785b…` | permanently NOT_ADMITTED (untouched) |
| Old OLA001R1 artifacts | driver `1863c343…` / wrapper `ac258cb3…` (host mode 0700 historical post-activation) | terminal historical inputs, untouched by this session |
| EXEC-RB-001 / EXEC-RB-002 / EXEC-RB-003 / EXEC-RB-004 / PREP-001 / OLA-001 / EXEC-RA-001 | OPEN-ROOT-CAUSE-UNRESOLVED / CLOSED / ROOT_CAUSE_ESTABLISHED / CLOSED / CLOSED / CLOSED / ROOT_CAUSE_ESTABLISHED (at their recorded strengths) | held verbatim |
| Qualification / Installation | NONE / NONE | held |

## 4. Historical precedent — READ-ONLY, NON-TRANSFERABLE

The RB-002 and RB-003 L1 prelaunch chains (RB003 design blob `18edf81f…` at `8687e3f…`, its readback at `0e823ce…`, the RB003 grant-prelaunch at `639148b…`, its readback, and the terminal RB003/RB002 single invocations) establish the TWO-STAGE human-operator pattern as executed precedent: (1) explicit human GRANT canonicalized by a bounded grant/prelaunch session that, only after every read-only gate passes — INCLUDING for PCH1 the fresh exact-EBS full package-byte reverification of Section 11 — applies chmod 0700 EXACTLY to driver+wrapper, re-hashes both (bytes unchanged), executes NEITHER, and publishes `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED`; (2) Control Room readback of that publication; (3) exactly one HUMAN-OPERATOR-DIRECT wrapper invocation which itself performs deployment and the one-shot A/B attempt lifecycle. Their old authority, old candidate, old event, old package identities, old predecessor geometry and old grant target DO NOT transfer to PCH1. The historical RB003 authority is CONSUMED / TERMINAL / CLOSED / NO_RERUN and MUST NOT be revived; precedent, NOT authority, and NOT a prediction of outcome.

## 5. Final wrapper static contract (82 lines read in full; `bash -n` PASS; NEVER executed)

- **No CLI argument/authority override surface:** ZERO positional/argument-forwarding occurrences (`$1`/`$@`/`$*` absent by census); the only operator inputs are the two documented PATH-only credential-source env locators (Section 14), which the wrapper itself never reads, prints or hashes; `DRIVER` (L44), `REQUIRED_DRIVER_SHA256` (L45), `REQUIRED_DRIVER_MODE` (L46) are hardcoded and unreachable from any argument.
- **Exact driver SHA pin:** L45 = `7a8389a30c9849d0efffd6f6e32b2e9760921eb3a296bfceb4707d660771829b`, enforced fail-closed L69–75.
- **Exact driver-mode requirement:** L46 = `"700"`, exact-match enforced L63–68 — the CURRENT 0600 state makes the wrapper refuse before any interpreter start: **the prelaunch mode barrier is the wrapper's own first executable gate**.
- **Root refusal** (L39–42); **owner check** uid==operator (L57–62); **symlink refusal** (L49–52); **regular-file check** (L53–56).
- **xtrace disabled** (`set +x` L32, never enabled; `BASH_XTRACEFD/ZSH_XTRACEFD/SHELLOPTS/BASHOPTS` unset L35); **core dumps disabled** (`ulimit -c 0` fail-closed L34); `set -euo pipefail` (L30); `umask 077` (L33).
- **Fixed PATH pinned before any external call** (`/usr/bin:/bin`, L37); all utilities absolute-pathed.
- **Isolated Python exec:** `PYTHONPATH/PYTHONHOME/PYTHONSTARTUP` unset (L80); `exec /usr/bin/python3 -I "$DRIVER"` (L82) — NO arguments forwarded to the driver; no retry; no fallback.
- **NO durable pre-exec consumption marker exists in the wrapper** (write/redirection census: the only redirections are `2>/dev/null` stderr suppressions on `ulimit`/`unset`; zero file-creation constructs) — basis of Residual R-PLD-5 (Section 16).

## 6. Final driver static contract (3352 lines analysed statically; NEVER imported/executed; ast.parse ONLY per R-PIMP-CR-1)

- `main()` (L3340) accepts NO arguments: `len(sys.argv) != 1` → REFUSED (L3342) — no authority/event/attempt/package override surface exists.
- `run_pipeline()` (L3291) order is EXACTLY: Phase 0 operator/host/repository checks (`phase0_operator_host_check`, L1200, incl. invocation-evidence-context creation at L1231 BEFORE Git admission at L1239) → Phase 1 source verification (`phase1_verify_source`) → Phase 2 deployment (`phase2_deploy`, L1653 → `deploy_generation`, L1561) → Phase 3 deployed re-verification (`phase3_reverify_deployed`, L1670, full reverify BEFORE any AccountingStore and BEFORE credential content, L1666/L1681) → Auditor-A one-shot attempt (`run_attempt_for_role(ctx,"A")`, L2744, called L3298) → Auditor-B ONLY if A mechanically conforms (L3299–3304 conditional AND the independent guard `AUDITOR_B_REFUSED_WITHOUT_CONFORMING_AUDITOR_A`, L2752) → Phase 6 mechanical barrier evidence (`phase6_mechanical_check`, L3307) → generated-LAST mechanical handoff (`build_handoff`, L3033, invoked in the `finally` at L3331 on EVERY terminal path once the evidence context exists).
- `create_invocation_evidence_context()` (L961) is NON-OVERWRITING: pre-existing `pch1-5cb2c58f-impl01-run-evidence/<AUTHORITY_ID>/` → `EVIDENCE_CONTEXT_ALREADY_EXISTS_NON_OVERWRITING` refusal (L985/L993; "A SECOND invocation under authority … is refused"; `FileExistsError` race handled identically); created BEFORE any fail-able Git-admission check — **the invocation marker is the durable mechanical authority-consumption marker**.
- The module-level surface contains ONLY imports (L102–116), the `DriverStop` class (L431), module constants, and the `__main__` guard (L3351 → `main()`): **no other executable entry point exists in the file**.
- Credential CONTENT is read only after the custody precondition: `resolve_credential_source` (L809) is METADATA-ONLY (lstat: symlink/regular/owner/size 1..65536; record carries path/size/mtime ONLY); the producer thread reads the source bytes ONCE at authorized-attempt start and writes exclusively into the EBS custody pipe; nothing is printed, hashed into evidence, copied or persisted.
- `AccountingStore` is created only inside `execute_one_shot_attempt()` (L1759; `ebs.accounting.AccountingStore.create` L1800, O_EXCL).
- Dynamic real gates run only through the EBS Supervisor inside `execute_one_shot_attempt`; Phases 0/1 verify gate bytes/ROOT without executing gates.
- No retry/resume authority exists: `DriverStop` is fail-closed with `STOP_SUFFIX` (L408, "DO NOT RE-RUN THIS AUTHORITY…"); phase-0 refuses any existing fresh-attempt root (`RETRY_REFUSED_ATTEMPT_*_ROOT_PRESENT`, L1436), any existing handoff (`HANDOFF_ALREADY_EXISTS`, L1446), any existing invocation context; `retry_authorized: false` / `reconciliation_authorized: false` at every barrier/evidence surface (L2634, L2772, L2951–2952, L3149–3150, L3312); no retry loop exists.
- The phase-0 §14 predecessor-state verifier (candidate L1312–1420) implements the accepted PCH1 contract with seven distinct fail-closed refusal points: A-1 `HISTORICAL_PREDECESSOR_A_ACCOUNTING_ABSENT_REFUSED` (L1333); A-2/A-3 `…_A_STATE_MUTATED_REFUSED` (L1349); A-4 `…_A_REPORT_CENSUS_REFUSED` (L1365); A-5 `…_A_REPORT_IDENTITY_REFUSED` (L1382, identity-only hash/stat — the sealed report is NEVER opened or parsed); B-1..B-3 `HISTORICAL_PREDECESSOR_B_ATTEMPT_PRESENT_REFUSED` (L1392/L1400/L1411); B-4 NOT_RUN geometry recorded into historical-immutable evidence. Its designed inputs are the CURRENT live predecessor geometry and are SATISFIED at design time (Section 10).

## 7. Deployment MUST remain inside the one human-direct wrapper invocation (mechanical proof, reproduced statically this session)

Non-executing AST call-graph analysis of the exact accepted candidate establishes the complete reachability chain:

```
exec /usr/bin/python3 -I "$DRIVER"            (wrapper L82 — the ONLY wrapper effect)
  → __main__ guard (driver L3351)
    → main() (L3340; refuses any argv)
      → run_pipeline() (L3291; sole caller of main-guard)
        → phase2_deploy() (L1653; sole caller = run_pipeline)
          → deploy_generation() (L1561; sole caller = phase2_deploy)
            → classify_destination() (L1541; called ONLY by deploy_generation + phase0 read-only classification)
```

Every deployment mutation is reachable ONLY inside `main()` ← `__main__` ← the single wrapper `exec`; the module level contains no other entry point (Section 6). Attempt creation occurs only later inside `prepare_attempt()` (L1695, called from `run_attempt_for_role` L2744 after Phases 0–3); AccountingStore only inside `execute_one_shot_attempt()` (L1759/L1800). No separate deployment/prelaunch entry point exists.

`classify_destination()` returns `EXPECTED_HISTORICAL` / `ALREADY_NEW` / `UNKNOWN`(`UNKNOWN_ABSENT`) (L1541–1552). The ONLY authorized mutation case is `EXPECTED_HISTORICAL` — the exact terminal `evt-4a51f4b9413a1476` generation, whose identity-only geometry is re-verified this session (Section 10). If ANY separate prelaunch task deployed the fresh generation first, the later authorized driver invocation would fail closed at TWO independent layers:

1. **Phase 0** (L1292–1296): the deployed root is classified read-only and must be `EXPECTED_HISTORICAL`, else `DEPLOYED_EVENT_NOT_EXPECTED_HISTORICAL_PREDECESSOR` STOP — an `ALREADY_NEW` destination fails here already.
2. **Phase 2** (L1581–1596): `classification == "ALREADY_NEW"` → `DESTINATION_ALREADY_NEW_GENERATION` STOP — plus the destination is RE-CLASSIFIED immediately before the rename layer (L1627) and must still be `EXPECTED_HISTORICAL`.

A pre-deployment would therefore (a) violate the mutation boundary — the deployment + non-overwriting backup creation would have happened under no grant surface; (b) force destination-classification refusals (`ALREADY_NEW` / not-expected-historical) that make the one authorized invocation mechanically unable to proceed; and (c) strand the one-shot granted authority, because `ALREADY_NEW` is a REFUSAL, never resume authority, and the fresh attempt roots would still be absent so no partial-attempt state exists to continue from. **Therefore the accepted lifecycle is NOT `grant → chmod → external/prelaunch deployment → readback → execute`; it is (Section 9): future explicit GRANT → bounded chmod-only 0600→0700 activation (with the Section-11 package gate BEFORE chmod) → Control Room granted-prelaunch readback → exactly ONE human-operator-direct wrapper invocation which ITSELF performs deployment and the attempt lifecycle. No design alternative in this record pre-deploys.**

## 8. Future GRANT semantics — DESIGN ONLY (nothing granted here)

The exact human statement to be required later (ONLY as a future explicit human-operator message, AFTER Control Room acceptance of THIS design AND its independent Control Room readback are canonical):

```
GRANT AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01
```

**WRITING, QUOTING, RECORDING OR DISCUSSING THAT STRING IN THIS DESIGN DOES NOT GRANT THE AUTHORITY. THIS SESSION RECORDS: HUMAN OPERATOR GRANT = NONE.** The future grant becomes meaningful only if issued later as a separate, explicit HUMAN-OPERATOR message. Any malformed, partial, conditional, hedged, wrong-ID or wrong-target grant must be treated as NO GRANT (precedent: the RB-001 L1 GRANT-ID-001 identity-correction chain).

Exact-target table binding the future grant (the grant/prelaunch session must present this table and refuse on ANY mismatch):

| Component | Exact identity |
|---|---|
| Authority | `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` (currently RESERVED / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE; must verify it was RESERVED before the grant with no prior consumption/runtime artifact) |
| Driver | `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.py` — SHA-256 `7a8389a30c9849d0efffd6f6e32b2e9760921eb3a296bfceb4707d660771829b` / 166778 B / isa:isa / regular non-symlink / mode 0600 at grant time |
| Wrapper | `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.sh` — SHA-256 `5423ec76ac562844d7fde243aba982dbf96a02e61a6dfbe427c3d311d8120d77` / 3468 B / isa:isa / regular non-symlink / mode 0600 at grant time; pins driver SHA `7a8389a3…` + `REQUIRED_DRIVER_MODE=700` |
| Event | `evt-5cb2c58f855415c3` |
| Attempt A | `evt-5cb2c58f855415c3-A-01` |
| Attempt B | `evt-5cb2c58f855415c3-B-01` |
| Maximum model engagements | 2 TOTAL; Auditor-A FIRST; Auditor-B ONLY after a mechanically conforming Auditor-A |
| Grant properties | ONE-SHOT / ONE HUMAN-DIRECT WRAPPER INVOCATION MAXIMUM / NON-TRANSFERABLE / EXACT-TARGET-SPECIFIC / NO RETRY / NO RESUME / NO FALLBACK / NO ALTERNATE DRIVER / NO ALTERNATE WRAPPER / NO ALTERNATE EVENT / NO ALTERNATE ATTEMPT / NO QUALIFICATION AUTHORITY / NO INSTALLATION AUTHORITY |

## 9. Authority state machine + two-stage lifecycle (DESIGN ONLY)

**TWO_STAGE_HUMAN_OPERATOR_PATTERN = PRESERVED.** The lifecycle MUST remain:

1. THIS design publication.
2. Independent Control Room readback of THIS design (and its generated-LAST handoff).
3. FUTURE explicit HUMAN OPERATOR GRANT (the exact phrase of Section 8).
4. Bounded GRANT/PRELAUNCH session performing ONLY: the read-only gates in the exact order of Section 15 (including the MANDATORY fresh exact-EBS full package-byte reverification of Section 11 BEFORE any chmod); exact chmod 0600→0700 of driver + wrapper ONLY; immediate re-hash proving bytes unchanged; execute NEITHER; publish `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED`.
5. Independent Control Room readback of the granted-prelaunch publication.
6. Exactly ONE HUMAN-OPERATOR-DIRECT wrapper invocation (Section 15.2).
7. That invocation itself performs deployment + the one-shot A/B attempt lifecycle.

Exact authority-state transitions:

| Stage | Authority state |
|---|---|
| Current (and after THIS design) | `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE` |
| After future explicit human GRANT, before chmod | `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_NOT_YET_ACTIVATED` |
| After successful bounded chmod-only activation | `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED` |
| BEGINNING of the eventual human-direct wrapper invocation | authority becomes **permanently NON-REUSABLE / CONSUMED FAIL-CLOSED** |
| After the single invocation terminates | `CONSUMED / TERMINAL / CLOSED / NO_RERUN` (regardless of outcome) |

**Terminal rule (fail-closed at invocation start):** from the BEGINNING of the human-direct wrapper invocation the authority must be treated as consumed irrespective of whether Python starts, the driver's durable invocation marker is created, deployment happens, attempt roots are created, an AccountingStore exists, credential contents are read, a dynamic gate executes, a provider starts, or an inference-capable engagement occurs. Durable mechanical marker WHEN REACHED: creation of `pch1-5cb2c58f-impl01-run-evidence/<AUTHORITY_ID>/` by `create_invocation_evidence_context` (L961/L1231) — non-overwriting; a second invocation under the same authority is refused outright (L985–993). Any later re-invocation would additionally fail closed at the phase-0 destination classification (`ALREADY_NEW`), the handoff-existence check (L1446) and the fresh-attempt-root checks (L1436).

### 9.1 Preserved consumption-marker residual

**`PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP`** — ACCEPTED RESIDUAL / FAIL-CLOSED / NON-BLOCKING (Section 16): if a known human-direct wrapper invocation begins but fails before the driver creates its durable invocation evidence context, the authority is STILL consumed; absence of the driver marker does NOT restore authority and is NOT evidence of reusability; no retry is permitted; return to Control Room.

## 10. Current deployed predecessor gates (read-only, ALL verified this session at identity/metadata strength)

Deploy root `/home/isa/aucdev023-s1-prep002-rem002` (candidate constants `DEPLOY_ROOT`/`ATTEMPTS_ROOT`):

- Deployed event `evt-4a51f4b9413a1476` EXACT (binding-auditor-a `f2dada28ecab4ea850a8f4e820047d2493d9751e2bec357bc714bfad77ede755`, binding-auditor-b `121f359dd7ab8dfaf0ffcf0f1bcd3365d27dd3a10c8c2adfc214ed69cc693325`, MANIFESTs `f0898c99ef43b097c70ccaec458e107ef1091f0fa66fedd4f67bcce55fbc97da` / `ddfcc31fbb67c8db51e2a5a4154d65ab17343da31bfe94b7771e51f4b78b436c`); SIX historical backups present (incl. `event.backup.pre-rb003-corrected-successor-event`); historical staging `event.staging.rb001-l1-rb003-4a51f4b9` consumed/ABSENT.
- Attempt census 25 roots = 24 historical + exactly `evt-4a51f4b9413a1476-A-01`; fresh `evt-5cb2c58f855415c3-A-01`/`-B-01` ABSENT.
- **Predecessor Auditor-A** TERMINAL: accounting `…/attempts/evt-4a51f4b9413a1476-A-01/accounting/evt-4a51f4b9413a1476-A-01.jsonl` = SHA-256 `816658e8008c58712a66345e345d765ad1c9dc57f892a490cf021d4c812505bf` / 5677 B / 0600 / regular with EXACT six-record state sequence `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_INVALID → TERMINAL` (mechanical state fields only); report-suffixed census under the A attempt root EXACTLY one path — `staging/evt-4a51f4b9413a1476-A-01.first-pass-report.json`; sealed report = SHA-256 `4af005323ab5803ec876f63a73426d9445abde0815a8e9c0e16d8e340da047bb` / 28361 B / 0600 / regular isa:isa — **IDENTITY-ONLY (hash/stat); substance NEVER opened, parsed, string-inspected or quoted; custody-out EMPTY; the unknown additional-property name remains undetermined with NO inference licensed. The report remains SEALED / UNREAD / UNADJUDICATED.**
- **Predecessor Auditor-B** NOT_RUN: attempt root `evt-4a51f4b9413a1476-B-01` ENTIRELY ABSENT (`os.path.lexists` semantics); canonical B accounting path absent; bounded walk of the attempts root found ZERO B-attempt-id report-suffixed artifacts; the unused 1/2 engagement budget of the consumed historical authority is NOT authority.
- **The accepted candidate's phase-0 §14 verifier inputs are therefore SATISFIED at design time** — the deployed destination will classify `EXPECTED_HISTORICAL` provided this geometry holds at invocation time. Design-time geometry MAY drift before any future execution (Residual R-PLD-3); the candidate's phase0 verifier is the fail-closed guard, and the future grant/prelaunch session MUST re-verify this exact geometry (Section 15 step 8) BEFORE chmod.

## 11. FUTURE EXACT-EBS PACKAGE-BYTE REVERIFICATION GATE — MANDATORY BEFORE ANY CHMOD (defined, NOT performed this session)

The accepted implementation readback carries the binding package-byte residual **R-PCH1-CR-2 / R-PDES-1 / R-IMP-1**: the full PCH1 A/B package payload bytes have NOT been independently freshly re-hashed at any Control Room session since preparation. **THIS DESIGN DEFINES the mandatory future gate and explicitly DOES NOT treat prior inventory/digest evidence as sufficient for future chmod/prelaunch admission.**

### 11.1 Canonical package identity table (from the accepted PCH1 records; re-verified at metadata strength this session)

| Item | Auditor-A | Auditor-B |
|---|---|---|
| Source generation root | `/home/isa/aucdev023-s1-rb001-l1-rb003-exec-ra001-pch1-fresh-replacement-package-prep-20260925-01/event` | (same root) |
| Binding file | `binding-auditor-a.json` = `7130cfc88ed6fdea1347c815e1b958c384eabda3534d33437243122e26f578e2` | `binding-auditor-b.json` = `68d622b291efcee25cea698165283561f94676481a3aec2e2532a8a48c7d70ab` |
| Canonical binding digest | `48361f2d0488ffe980a1a734f93274e219cd1410cd794dbe2cf142e8ce6dcbbb` | `35cbc561b71f7b45e58b6470e746d4b7083b2640abbfec4ddafe91de17508956` |
| MANIFEST identity | `package-auditor-a/MANIFEST.json` = `5d5eb70a9f938db19a12e2dec00af4c6fd97f10bb9eb4e40063eea8bc0609435` (42226 B) | `package-auditor-b/MANIFEST.json` = `b5874d90dc9b101cd93763b0cb5b0badbed5e8e90381f01de0673e3838ef24fb` (43042 B) |
| Package identity | `e6b6631378342e0506c42d5e85d26b8de299610fcd9c754b1f0ac8099578defa` | `bb6b06a4319cf98f77a7d7d4983bf85d979515a16d31b1275feb3352c5ae48dd` |
| Row count | 191 | 194 |
| Payload byte count | 236323239 B | 343454376 B |
| Event / attempts | `evt-5cb2c58f855415c3` / `-A-01` / `-B-01` | (same) |
| Auditor executable | `15e2d051…` (claude 2.1.274) | `3188814c…` (codex 0.154.0) |

Additional pinned plane identities: fresh prompt contract `7679ac2d830c26f87d99d0bc60133a31efe24a90390bf35ce1d5f7b2a7434ffd`; frozen target `d4d584ffa47ad2848268ba947247f81a845b2322`; EBS plane at `bootstrap-supervisor` (protected tree `732b8def…`): plane MANIFEST `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999` and EBS package `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93e922f8` (BOTH re-hashed/re-read EXACT this session at plane-manifest strength); boundary launcher `011a8713…` + resource gate `27948980…` + frozen 20-path 0555 executable mode table HELD. Metadata-strength facts verified this session: workspace binding files re-hashed EXACT; workspace MANIFESTs re-hashed EXACT with row counts 191/194 EXACT and `package_sha256` identity fields EXACT. **The package payload byte streams were NOT re-hashed by this design session.**

### 11.2 The future gate (exact ordered contract — the future grant/prelaunch session MUST perform ALL of this BEFORE chmod; ANY mismatch ⇒ STOP before chmod, NO chmod may occur)

1. Re-resolve the exact live EBS from `EBS_ROOT = /home/isa/audit-council-dev/bootstrap-supervisor` (live read, not memory).
2. Verify the exact EBS implementation/plane identity: plane MANIFEST SHA-256 `d683f64d…` AND its `package_sha256` = `d42aa9e3…` (byte-plane identity), within the protected tree `732b8def…`.
3. Parse each A/B binding file (`binding-auditor-a.json` / `binding-auditor-b.json`) with the exact EBS (`parse_binding`).
4. Recompute each canonical binding digest and require `48361f2d…` (A) / `35cbc561…` (B).
5. Run the exact event-package verifier for BOTH roles (`verify_event_package` semantics: per-row size + SHA-256, exact payload-set equality, transport projection).
6. Re-hash EVERY frozen package payload byte required by the package inventories — all 191 (A) / 194 (B) MANIFEST rows against the workspace package trees.
7. Establish exact payload-set equality (no missing row-file, no extra file).
8. Verify per-row size and SHA-256 for every row.
9. Verify MANIFEST identity `5d5eb70a…` (A) / `b5874d90…` (B).
10. Verify package identity `e6b66313…` (A) / `bb6b06a4…` (B) from the recomputed inventory.
11. Verify event/attempt/role/frozen-target relations (`evt-5cb2c58f855415c3`, `-A-01`/`-B-01`, `FROZEN_TARGET_COMMIT d4d584ff…`, prompt contract `7679ac2d…`).
12. Verify launcher/gate/auditor executable identities (`011a8713…`, `27948980…`, `15e2d051…`/`3188814c…`) and the frozen mode table (executable set EXACTLY the 20 pinned paths, all 0555, no extras).
13. Require BOTH roles PASS.
14. STOP before chmod on ANY mismatch — **a package mismatch is an absolute pre-chmod STOP; no partial admission, no role-specific waiver, no reliance on prior inventory/digest evidence.**

If the exact live EBS or package bytes cannot be fully verified, future prelaunch MUST STOP and NO chmod may occur. Package bytes MUST NOT be modified by anyone (any modification is a new preparation task under new authority). This gate is a READ-ONLY verification gate, not an execution/admission transition, and performing it belongs exclusively to the future grant/prelaunch session (and is re-derived again at driver runtime by phases 0–3).

## 12. Repository / provenance gates (future prelaunch contract; reproduced read-only at the base this session — ALL PASS)

The future grant/prelaunch session MUST verify, immediately before chmod:

- **Mandatory live GitHub bootstrap** (resolve live `master`; verify the then-current canonical chain: design → design readback → (future) grant canonicalization; STOP on drift; no auto-rebase; local HEAD == live == FETCH_HEAD).
- **Exact accepted implementation/readback lineage present**: implementation record `4cd7befe…` at `ce88d0c3`, implementation CR readback `9dd9cf9c…` at `29a2644`, and THIS design record + its readback, all reachable as docs-only fast-forward descendants.
- **Candidate source identities exact** (Section 3 table).
- **Protected trees exact** (`732b8def…` / `5b8d5e54…` / `c792933a…`).
- **Trust anchor ancestor** (`30588684…`); ZERO merges since anchor; changed paths since anchor ALL under `docs/chatgpt-project/` (governed prefix).
- **No unexpected tracked drift under governed/protected paths**; the pre-existing `smoke-fixture`/`smoke-fixture-103` gitlink drift is OUTSIDE every governed/protected path, classified separately and NOT staged.
- **Reserved authority references confined** to the canonical accepted lineage + candidate source (tracked-tree occurrences at the base: exactly the design record, design-readback record, implementation record, implementation-readback record, CURRENT and BACKLOG; full-history pickaxe = exactly the accepted lineage commits `aaab3fa`/`7204eb6`/`ce88d0c3`/`29a2644`); canonical reserved-ID occurrences are EXPECTED and are NOT collisions and are NOT grants.
- **No effective GRANT/consumption/runtime artifact except the future explicit operator grant once it exists** (grant-statement probe clean at design time; evidence root ABSENT; fresh attempts ABSENT; future handoff path ABSENT).
- **Immutable governance pins** exact at HEAD (the five `PINNED_RECORD_BLOBS`: `9f7599fe…`, `578b58c8…`, `83951286…`, `7ba8910e…`, `776a039a…`).

Every future governance publication before invocation must remain a docs-only fast-forward descendant compatible with the frozen driver admission policy (later governance records existing is NOT a source-mutation reason — the lineage contract exists precisely to admit them).

## 13. Fresh-runtime namespace pristine contract (verified ABSENT this session)

Current and future prelaunch verification must require the ABSENCE of AT LEAST (exact names from the accepted candidate constants):

| Namespace | Path | This session |
|---|---|---|
| Fresh A attempt root | `/home/isa/aucdev023-s1-prep002-rem002/attempts/evt-5cb2c58f855415c3-A-01` | ABSENT |
| Fresh B attempt root | `/home/isa/aucdev023-s1-prep002-rem002/attempts/evt-5cb2c58f855415c3-B-01` | ABSENT |
| Future invocation-evidence root | `/home/isa/audit-council-dev/pch1-5cb2c58f-impl01-run-evidence` | ABSENT |
| Future mechanical handoff | `/home/isa/audit-council-dev/AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01-MECHANICAL-HANDOFF.tar.gz` | ABSENT |
| Future staging | `/home/isa/aucdev023-s1-prep002-rem002/event.staging.rb001-l1-rb003-5cb2c58f-pch1` | ABSENT |
| Future backup | `/home/isa/aucdev023-s1-prep002-rem002/event.backup.pre-pch1-replacement-event` | ABSENT |
| AccountingStore for the new attempts | any accounting state under the two fresh attempt roots | ABSENT (roots absent) |
| Unexpected runtime artifact under the future authority | any file/directory whose name contains the reserved authority ID outside the canonical accepted lineage + candidate source | NONE FOUND (sweep clean) |

**Design rule:** if ANY is unexpectedly present at prelaunch time, the prelaunch session does NOT delete, normalize, overwrite, rename or reuse it — it returns `STOP = UNEXPECTED_RUNTIME_STATE_PRESENT` to Control Room. Existing historical backups/attempt roots remain immutable.

## 14. Credential metadata-only gate (TIME-OF-DESN design facts; future re-resolution REQUIRED)

Static resolution semantics from the accepted candidate source (`resolve_credential_source`, L809–853; non-executing AST extraction of the exact constants): the driver-supported PATH locators are the environment variables `AUCDEV_A_CREDENTIAL_FILE` (role A) / `AUCDEV_B_CREDENTIAL_FILE` (role B); when unset, the single conventional candidates `A: /home/isa/.claude/.credentials.json`, `B: /home/isa/.codex/auth.json`. EXACTLY ONE admissible source per role is required (0 or >1 existing candidates ⇒ `CREDENTIAL_SOURCE_{role}_AMBIGUOUS_OR_ABSENT` fail-closed); lstat checks: NOT a symlink, regular file, operator-owned, size within `CREDENTIAL_MIN_BYTES=1`..`CREDENTIAL_MAX_BYTES=65536`; the resolution record carries path/size/mtime ONLY — contents, and any content hash, NEVER enter any record.

Host metadata (lstat ONLY, this session — never opened/read/hashed): `/home/isa/.claude/.credentials.json` exists, regular, non-symlink, isa:isa, mode 0600, 519 B (in bounds); `/home/isa/.codex/auth.json` exists, regular, non-symlink, isa:isa, mode 0600, 4231 B (in bounds); NO `AUCDEV_*_CREDENTIAL_FILE` override currently set (resolution will take the conventional candidates). **This evidence is TIME-OF-DESIGN ONLY (Residual R-PLD-4): the future grant/prelaunch activation session MUST re-resolve credential metadata immediately before any chmod; no credential content may be read during prelaunch.** If an override is ever required it must be EXPLICIT and PATH-only (set by the human operator and recorded as metadata) — never a silently added locator, never a content-reading surface.

## 15. Future GRANT/PRELAUNCH activation — exact order (DESIGN ONLY)

### 15.1 The bounded post-GRANT session (performs chmod ONLY after ALL gates pass)

After BOTH Control Room acceptance of THIS design AND its readback AND the explicit human GRANT exist, a later bounded GRANT/PRELAUNCH session may perform EXACTLY, in this fail-closed order:

1. Live GitHub bootstrap (resolve live `master`; verify the then-current canonical chain; STOP on drift; no auto-rebase).
2. Verify the exact canonical design + Control Room design-readback chain (THIS record and its readback, blobs exact).
3. Verify the exact explicit human GRANT string and the exact-target table (Section 8) — refuse any mismatch (malformed/partial/conditional/hedged/wrong-ID/wrong-target = NO GRANT).
4. Verify the authority was RESERVED before the grant and has NO prior consumption/runtime artifact (Section 13 sweep clean at that time).
5. Verify candidate driver EXACT: path `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.py` / SHA-256 `7a8389a3…` / 166778 B / owner isa:isa / regular / non-symlink / CURRENT mode 0600.
6. Verify candidate wrapper EXACT: path `run-aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.sh` / SHA-256 `5423ec76…` / 3468 B / owner isa:isa / regular / non-symlink / CURRENT mode 0600.
7. Verify wrapper exact driver-SHA pin `7a8389a3…` and `REQUIRED_DRIVER_MODE="700"` (the 0600/700 mismatch is what keeps the wrapper refusing until this moment).
8. Verify the historical/current deployed predecessor classification and the A `REPORT_INVALID` / B `NOT_RUN` identity-only geometry EXACT (Section 10 facts, re-resolved live).
9. Perform the FULL fresh exact-EBS PCH1 A+B package-byte reverification of Section 11.2 (steps 1–14), BOTH roles PASS. **This gate is MANDATORY and PRECEDES chmod; ANY mismatch ⇒ STOP before chmod.**
10. Verify the fresh runtime namespace pristine (Section 13, all eight namespaces ABSENT).
11. Verify repository lineage / protected trees / immutable governance pins (Section 12, re-resolved live).
12. Re-resolve credential-source admissibility METADATA ONLY (Section 14, fresh lstat).
13. Re-run the future authority confinement/collision/admission checks (reserved-ID occurrences confined to accepted lineage + candidate; NO effective grant/consumption/runtime artifact beyond the operator grant being canonicalized).
14. Only after ALL gates 1–13 PASS: `chmod 0700` EXACTLY the driver. NO other filesystem mutation.
15. `chmod 0700` EXACTLY the wrapper.
16. Immediately re-hash BOTH.
17. Require exact SHA/size/owner/path — bytes EXACTLY unchanged (`7a8389a3…`/166778 and `5423ec76…`/3468).
18. Require modes EXACTLY 0700 on BOTH.
19. Execute NEITHER artifact.
20. Publish the exact granted-prelaunch state: `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED` (docs-only fast-forward publication; no stronger claim).
21. Generate reviewer handoff LAST.

If any gate fails before chmod: NO chmod. No deployment. No attempt creation. No AccountingStore. No credential-content read. No dynamic gates. No boundary/auditor/provider execution.

### 15.2 Partial-chmod failure semantics (fail-closed, explicit)

- **Driver chmod succeeds, then wrapper chmod FAILS (or any immediate post-chmod verification fails):** the session MUST STOP; DO NOT execute either artifact; DO NOT deploy; DO NOT retry automatically; DO NOT chmod anything further; DO NOT "roll back" the driver to 0600 unless canonical policy already authorizes that specific rollback (no rollback authority is invented by this design — the canonical record supports none). The session returns to Control Room with the EXACT partial activation state recorded (which artifact(s) are at 0700, their re-hashed identities, and the exact failing gate). The partial state is NOT execution readiness: the wrapper still refuses a wrong-mode/wrong-SHA driver, and NO invocation may occur. The authority remains `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED` with activation INCOMPLETE — resumption or abandonment is a Control Room decision on a future separately authorized task, not an automatic action.
- **Both chmods succeed but a re-hash/mode verification fails (bytes changed, owner changed, wrong mode):** identical treatment — STOP, execute neither, no auto-retry, no rollback invention, exact partial state to Control Room. A byte change at this point is a candidate-integrity incident (the chmod is mode-only; any byte drift means the artifact is not the accepted candidate) and MUST NOT be normalized.
- **Any chmod attempt that fails outright (permission etc.):** STOP before any execution; nothing activated; report exact state.
- In EVERY partial/failed case: NO human-direct invocation is authorized, the single-invocation budget remains unspent but the grant is NOT consumable in the partial state, and Control Room adjudication is required before ANY further filesystem or authority action.

### 15.3 The eventual single human-direct invocation (recorded; NOT authorized by this record)

If and ONLY if ALL of: THIS design receives Control Room acceptance AND its readback; a future explicit HUMAN GRANT exists; the bounded chmod-only granted-prelaunch activation (with the Section-11 package gate) completes; its canonical publication completes; and Control Room independently accepts that granted-prelaunch publication — then the sole proposed runtime invocation (quoted here; THIS task did NOT execute it and no agent/controller may):

```
cd /home/isa/audit-council-dev
./run-aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.sh
```

No arguments (the wrapper forwards none; the driver refuses any). No inference-capable controller. No automation. No agent standing authority. No second invocation. No retry. The wrapper verifies driver identity/mode and directly execs isolated Python (`/usr/bin/python3 -I`); the driver itself performs deployment and the one-shot A/B lifecycle. **QUOTING THIS COMMAND GRANTS NO AUTHORITY TO EXECUTE IT.**

## 16. Wrapper preexec consumption-marker residual — re-evaluated for the NEW wrapper

Historical residual `PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP` (from EXEC-04/EXEC-05/RB002/RB003): the wrapper writes no durable marker before its exec. **Re-evaluation on the accepted PCH1 wrapper this session (mechanically supported):** the write/redirection census of the 82-line wrapper finds ZERO file-creation constructs — the only redirections are `2>/dev/null` stderr suppressions on `ulimit`/`unset`; no `touch`/`tee`/`cp`/`mv`/output redirection to any path exists; the wrapper's only effects before `exec` are read-only checks and `echo` refusals to stdout. **THE RESIDUAL REMAINS OPEN — it is NOT closed by the new wrapper, and this design does NOT claim it is closed.** The wrapper source is NOT modified by this design (no source change is authorized or proposed).

The fail-closed governance rule is therefore PRESERVED verbatim: if the human-direct wrapper invocation is KNOWN to have begun, the authority is consumed even if the driver's later invocation marker is absent (e.g., failure at the wrapper's own mode/SHA/owner refusals, or interpreter startup failure before the driver creates its evidence context). Marker absence NEVER restores authority and is NEVER evidence that the authority remains reusable. No retry. No second invocation. Return to Control Room.

## 17. Engagement / attempt accounting (designed exactly, from the accepted candidate source)

- **Maximum 2 inference-capable engagements TOTAL** (`model_engagement_budget_maximum: 2`); Auditor-A FIRST; Auditor-B ONLY after a mechanically conforming A (guarded in `run_pipeline` L3298–3304 AND independently at `run_attempt_for_role` L2752 `AUDITOR_B_REFUSED_WITHOUT_CONFORMING_AUDITOR_A`).
- `CONSUMED_PRE_EXEC` = the conservative fail-closed authority-budget charge (durable accounting fact; every attempt whose accounting reached `CONSUMED_PRE_EXEC` charges the budget, L2845–2893).
- `EXEC_ATTEMPTED` = the inference-capable execution fact (durable accounting record).
- Consumed-pre-exec WITHOUT `EXEC_ATTEMPTED` ⇒ the charge is PRESERVED and the case recorded `CONTROL_ROOM_ADJUDICATION_REQUIRED` ("FAIL-CLOSED BUDGET CHARGE RETAINED") — the driver never infers provider/model substance and never undercounts.
- Historical old-event attempts do NOT count against the new-event budget; the unused 1/2 engagement budget of the CONSUMED historical authority is NOT authority.
- No stdout/stderr report manufacture (`evaluate_conformance` never inspects report substance; frozen artifacts are only stat()ed and SHA-256 hashed). No report repair/normalization. No unauthorized peer first-pass access (nothing Auditor-A-derived enters the Auditor-B attempt). No retry authority; no reconciliation execution authority (`reconciliation_authorized: false`, `retry_authorized: false` in every barrier record).

## 18. R-PIMP-CR-1 — carried forward accurately

```
R-PIMP-CR-1 = IMPLEMENTATION_ANALYZER_PARTIAL_ASSIGNMENT_EXECUTION
Support: OBSERVED FACT (established by the implementation Control Room readback, record 9dd9cf9c… §12)
Classification: HARNESS/PROTOCOL EVIDENCE-METHOD RESIDUAL
              / NON-BLOCKING
              / NOT CANDIDATE SOURCE REMEDIATION
```

The historical implementation analyzer (`classify-and-accept.py`) compiled+executed a bounded candidate-derived top-level assignment-only AST subset (76 Assigns; exactly 9 RHS calls, all `frozenset`; zero user-defined/attribute/file/network/provider calls). The residual does NOT establish a candidate behavioral defect, does NOT establish launcher runtime execution, does NOT create execution authority, and does NOT require candidate source remediation before the next stage. **THIS design session honours the mandate: every source analysis in THIS record was performed by NON-EXECUTING parsing/extraction only (pure `ast.parse` + a safe literal evaluator over Constant/List/Tuple/Dict/Name/Add nodes with NO `exec`, NO `compile`-to-execution, and NO import of the candidate; `bash -n` parse-only for the wrapper).** Future static-only analyzers MUST NOT reuse the exec-based method.

## 19. Residuals (recorded prospectively; none blocks the future grant)

- **R-PLD-1 (carried) FRESH_EBS_PACKAGE_BYTE_REVERIFICATION_REQUIRED** — R-PCH1-CR-2 / R-PDES-1 / R-IMP-1: the 236323239 B / 343454376 B package payload byte streams were NOT re-hashed by this design session; the Section-11.2 gate is MANDATORY before ANY future chmod/prelaunch/deployment admission; prior inventory/digest evidence is NOT sufficient.
- **R-PLD-2 STATIC_ONLY_ANALYSIS** — this design is static/read-only strength; the AST deployment-reachability proof, verifier-input satisfaction and wrapper census prove source structure, NOT future runtime behavior; the future phase0–3 pipeline re-establishes every predicate fail-closed at runtime.
- **R-PLD-3 DESIGN_TIME_GEOMETRY_MAY_DRIFT** — the predecessor/namespace/repository/credential facts verified this session are time-of-design; the future grant/prelaunch session MUST re-verify each immediately before chmod (Section 15 order).
- **R-PLD-4 CREDENTIAL_METADATA_TIME_OF_DESIGN** — the lstat-only credential-locator snapshot is time-of-design; re-resolve immediately before any chmod; contents remain UNREAD.
- **R-PLD-5 PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP** — Section 16: the new wrapper writes NO durable pre-exec marker (write census zero file-creation constructs); the residual REMAINS OPEN; protocol rule preserved (marker absence never restores authority).
- **R-PLD-6 R_PIMP_CR_1 CARRIED** — Section 18, verbatim.
- **R-PLD-7 RESERVED_AUTHORITY_OCCURRENCES_EXPECTED** — after this publication the reserved-ID string is EXPECTED in the canonical design/readback lineage + implementation lineage + candidate source; future sweeps verify CONFINEMENT + absence of grant/consumption/runtime artifacts, NOT zero occurrence.
- **R-PLD-8 SMOKE_FIXTURE_GITLINK_DRIFT** — the pre-existing `smoke-fixture`/`smoke-fixture-103` gitlink drift is unrelated, outside governed paths, preserved unstaged.

## 20. Design acceptance matrix (deterministic gates)

| Gate | Check | Result |
|---|---|---|
| PLD-01 | live Git exact: master `29a264472180524918a5781afc82c8cf25dd81f7` == local HEAD == FETCH_HEAD; root `b9af0d99…`; sole parent `ce88d0c3…` | PASS |
| PLD-02 | CURRENT/BACKLOG/implementation-readback blobs exact (`5fd97d93…`/`1bf85b2a…`/`9dd9cf9c…`) | PASS |
| PLD-03 | implementation-readback handoff integrity exact (`f72e16ec…`/790021 B/25 members = 21 payload + 1 SHA256SUMS + 3 dirs; 21/21 PASS; 0 missing 0 unlisted; canonical copies git-EQUAL; ZERO members executed) | PASS |
| PLD-04 | protected trees exact (`732b8def…`+`5b8d5e54…`+`c792933a…`) | PASS |
| PLD-05 | candidate driver exact 0600 (`7a8389a3…`/166778/3352/isa:isa/regular/non-symlink; L129 AUTHORITY_ID = reserved future authority) | PASS |
| PLD-06 | candidate wrapper exact 0600 (`5423ec76…`/3468/82/isa:isa/regular/non-symlink) | PASS |
| PLD-07 | wrapper SHA/mode pins exact (L45 `7a8389a3…`, L46 `"700"`; 0600/700 mismatch = CLOSED barrier) | PASS |
| PLD-08 | reserved authority still NOT_GRANTED (tracked-tree occurrences confined to accepted lineage; full-history pickaxe = accepted lineage commits only; NO effective GRANT statement anywhere) | PASS |
| PLD-09 | no consumption/runtime artifact (fresh attempts ABSENT; evidence root ABSENT; future handoff ABSENT; no invocation evidence under the authority) | PASS |
| PLD-10 | current deployed predecessor identity exact (`evt-4a51f4b9413a1476`; bindings `f2dada28…`/`121f359d…`; MANIFESTs `f0898c99…`/`ddfcc31b…`; six backups; old staging consumed) | PASS |
| PLD-11 | predecessor A REPORT_INVALID/TERMINAL identity-only geometry exact (accounting `816658e8…`/5677/0600; six-state sequence; census exactly one; sealed report `4af00532…`/28361/0600; custody-out EMPTY) | PASS |
| PLD-12 | predecessor B NOT_RUN geometry exact (attempt root entirely ABSENT; no B accounting; no B report artifact by bounded walk) | PASS |
| PLD-13 | sealed-report blindness preserved (hash/stat/pathname/census ONLY; never opened/parsed/quoted; unknown additional-property name undetermined, NO inference licensed) | PASS |
| PLD-14 | fresh runtime namespace pristine (all eight Section-13 namespaces ABSENT; attempt census 25 unchanged) | PASS |
| PLD-15 | deployment-inside-single-invocation statically proven (AST call-graph: `deploy_generation` ← `phase2_deploy` ← `run_pipeline` ← `main` ← `__main__` guard ← wrapper `exec`; no other module-level entry point) | PASS |
| PLD-16 | external/prelaunch deployment explicitly REJECTED (phase-0 `DEPLOYED_EVENT_NOT_EXPECTED_HISTORICAL_PREDECESSOR` L1296; phase-2 `DESTINATION_ALREADY_NEW_GENERATION` L1596 + pre-rename re-classification L1627; `ALREADY_NEW` = refusal never resume; mutation-boundary violation + stranded one-shot authority) | PASS |
| PLD-17 | exact future human grant target defined (Section-8 statement + exact-target table + one-shot properties + malformed-grant refusal rule) | PASS |
| PLD-18 | authority state machine fail-closed (Section-9 transitions; consumption at invocation BEGIN irrespective of earliness of failure; terminal NO_RERUN) | PASS |
| PLD-19 | wrapper-preexec consumption residual correctly carried (Section-16 re-evaluation: residual REMAINS OPEN, mechanically supported by write census; no source modification claimed or made) | PASS |
| PLD-20 | future exact-EBS full package-byte verification gate defined (Section-11.2 fourteen-step contract, BOTH roles, from the canonical identity table) | PASS |
| PLD-21 | package mismatch ⇒ STOP before chmod (Section-11.2 step 14 absolute; prior inventory evidence NOT sufficient) | PASS |
| PLD-22 | credential metadata-only gate defined (Section-14; lstat-only facts; bounds; time-of-design classification; future re-resolution requirement) | PASS |
| PLD-23 | exact chmod-only order defined (Section-15.1 twenty-one-step fail-closed order; gates 1–13 precede chmod) | PASS |
| PLD-24 | partial-chmod failure semantics defined fail-closed (Section-15.2: STOP; execute neither; no auto-retry; no invented rollback; exact partial state to Control Room) | PASS |
| PLD-25 | post-chmod exact re-hash requirement defined (Section-15.1 steps 16–18: bytes/owner/modes exact) | PASS |
| PLD-26 | execute-neither rule defined (Section-15.1 step 19; wrapper/driver NOT executed by the activation session) | PASS |
| PLD-27 | single human-direct invocation maximum preserved (Section-15.3; no arguments; no controller/automation/agent; no second invocation) | PASS |
| PLD-28 | no-retry/no-resume/no-fallback preserved (STOP_SUFFIX; RETRY_REFUSED/HANDOFF_ALREADY_EXISTS/EVIDENCE_CONTEXT_ALREADY_EXISTS refusals; `retry_authorized:false` everywhere; no retry constructs) | PASS |
| PLD-29 | A-first / B-after-conforming-A preserved (run_pipeline conditional + independent `AUDITOR_B_REFUSED_WITHOUT_CONFORMING_AUDITOR_A` guard) | PASS |
| PLD-30 | conservative engagement accounting preserved (max 2 TOTAL; CONSUMED_PRE_EXEC charge; EXEC_ATTEMPTED fact; CONTROL_ROOM_ADJUDICATION_REQUIRED on charge-without-exec; no manufacture/normalization) | PASS |
| PLD-31 | R-PIMP-CR-1 carried (Section-18 verbatim; this session's analysis non-executing by construction) | PASS |
| PLD-32 | ZERO runtime mutation this session (attestation Section-21) | PASS |
| PLD-33 | ZERO auditor/provider execution this session (attestation Section-21) | PASS |
| PLD-34 | NO GRANT this session (HUMAN OPERATOR GRANT = NONE; quoting grants nothing) | PASS |
| PLD-35 | publication geometry valid (Section-22: exactly three tracked paths; one docs-only fast-forward; sole parent `29a2644…`; live re-resolve before staging) | PASS |

## 21. Zero-runtime / no-grant attestation

THIS DESIGN performed and authorized NOTHING runtime: HUMAN OPERATOR GRANT = NONE; chmod NONE (driver and wrapper remain mode 0600 NON-EXECUTABLE); driver execution/import NONE (non-executing `ast.parse` + safe literal extraction ONLY); wrapper execution NONE (read + `bash -n` parse only); deployment NONE; staging NONE; new backup NONE; runtime attempts NONE (census unchanged 25; fresh attempts ABSENT); AccountingStore NONE; credential CONTENT read NONE (metadata-only lstat; no credential file opened); dynamic real gates NONE; boundary execution NONE; Auditor-A/B execution NONE; provider/model execution ZERO; sealed-report substance access NONE (identity-only hash/stat/census); package payload bytes NOT modified and NOT re-hashed (the EBS gate is DESIGNED, not performed); execution authority granted/consumed NONE; qualification NONE; installation NONE; retry/resume of any historical execution NONE. Local executions were this task's own deterministic read-only tools (git, sha256sum/stat, python `ast.parse`/`tarfile` streaming). Network = the mandated bootstrap `git ls-remote`, the fetch at the exact base, the pre-staging live re-resolve, the single `git push` of this publication, and the post-push readback ONLY.

## 22. Publication of THIS record

Exactly THREE changed tracked paths over base `29a264472180524918a5781afc82c8cf25dd81f7`: THIS NEW canonical design record + `AUCDEV-CURRENT-STATE.md` (current-facing fields rotation lines 3/11/23–25 + one dated record appended with blank separator) + `AUCDEV-BACKLOG.md` (one dated record appended with blank separator). The candidate driver/wrapper remain UNTRACKED HOST ARTIFACTS, NOT modified, mode 0600. NOT modified: protected trees, packages, deployed event, attempts, AccountingStore, sealed reports, credentials, execution handoffs, historical backups, old OLA001R1 artifacts, prior canonical records, `AUCDEV-ARCHITECTURE-SUMMARY.md`, `AUCDEV-QUALIFICATION-HISTORY.md`. `git diff --check` PASS; live master re-resolved EXACT immediately before staging (STOP on drift; no auto-rebase); exactly ONE bounded docs-only fast-forward publication commit whose sole parent is `29a2644…`. The generated-LAST reviewer handoff is produced after this push and the post-push readback, with nothing included mutated afterward.

## 23. Held project state (preserved verbatim)

EXEC-RB-001 = OPEN / ROOT_CAUSE_UNRESOLVED; EXEC-RB-002 = CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH; EXEC-RB-003 = ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_MECHANICAL_STRENGTH; EXEC-RB-004 = CLOSED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH; PREP-001 = CLOSED_AT_CONTROL_ROOM_PACKAGE_PREPARATION_READBACK_STRENGTH; OLA-001 = CLOSED_AT_CONTROL_ROOM_DESIGN_AMENDMENT_READBACK_STRENGTH; EXEC-RA-001 = ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH; PCH-001 remains DEFENSE-IN-DEPTH PROMPT-CONFORMANCE HARDENING / EXTERNAL-AUDITOR-OUTPUT-RISK REDUCTION / NOT PRODUCT-DEFECT REMEDIATION. The consumed authority `AUCDEV-023-S1-RB001-L1-RB003-FIRSTPASS-EXEC-20260925-01` remains CONSUMED/TERMINAL/CLOSED/NO_RERUN; prior nonconforming candidate `15198c02…`/`1366785b…` remains permanently NOT_ADMITTED. AUCDEV-023 remains **P1 / READY / NOT DONE** with NO queue-count transition (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11); audit completeness INCOMPLETE; qualification NONE; installation NONE; installed source `8ae33444f349ce73c1359b963722e2d16acba630` with installed-qualified provenance NOT ESTABLISHED.

## 24. Next action — EXACTLY ONE

CONTROL ROOM READBACK OF THE PCH1 REPLACEMENT PRELAUNCH TRANSITION DESIGN AND ITS GENERATED-LAST HANDOFF BEFORE ANY HUMAN-OPERATOR GRANT, CHMOD-TO-0700 ACTIVATION, DEPLOYMENT, RUNTIME ATTEMPT CREATION, CREDENTIAL-CONTENT READ, DYNAMIC REAL GATE, EXECUTION-AUTHORITY TRANSITION, AUDITOR/PROVIDER EXECUTION, QUALIFICATION, OR INSTALLATION.

THIS DESIGN DOES NOT ISSUE THE GRANT, DOES NOT CHMOD THE CANDIDATE, DOES NOT EXECUTE IT, DOES NOT DEPLOY, DOES NOT CREATE ATTEMPTS, DOES NOT READ CREDENTIAL CONTENTS, AND DOES NOT PROCEED TO GRANT/PRELAUNCH ACTIVATION.
