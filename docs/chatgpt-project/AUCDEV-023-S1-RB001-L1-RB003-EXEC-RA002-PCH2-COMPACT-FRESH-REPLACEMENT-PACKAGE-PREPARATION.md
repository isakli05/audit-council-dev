# AUCDEV-023 S1 RB-001 L1 RB-003 EXEC-RA-002 PCH-002 Compact Fresh Replacement Package Preparation (Merged Closed-Shape Prompt Hardening / Fresh Event + Fresh A+B Packages)

- **Preparation authority**: `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-COMPACT-FRESH-REPLACEMENT-PACKAGE-PREP-20260927-02`
- **Date**: 2026-09-27 (Europe/Istanbul)
- **Session role**: BOUNDED PROMPT-CONFORMANCE HARDENING IMPLEMENTER AND FRESH REPLACEMENT PACKAGE PREPARER — NOT the Control Room decision-maker, NOT an execution-authority grantor, NOT a deployment authority, NOT an execution controller, NOT Auditor-A/B, NOT a qualification authority, NOT an installation authority. This task performed ZERO provider/model execution (the frozen client executed ONLY inside the isolated preparation-workspace composition against the deterministic loopback mock with scripted bytes) and created NO replacement execution authority.

## 1. Disposition

```
EXEC_RA002_PCH2_COMPACT_FRESH_REPLACEMENT_PACKAGE_PREPARATION =
PREPARED_AT_MECHANICAL_PACKAGE_STRENGTH /
CONTROL_ROOM_PROMPT_BUDGET_SCOPE_AMENDMENT_APPLIED /
MERGED_PCH1_PCH2_CLOSED_SHAPE_COMPACT_CLAUSE /
ALL_PCH1_SEMANTICS_PRESERVED /
PCH2_TOP_LEVEL_TEN_KEY_ROOT_SHAPE_ADDED /
VALIDATOR_UNCHANGED /
REPORT_SCHEMA_UNCHANGED /
EBS_1024_BYTE_ARGV_ITEM_BOUND_UNCHANGED_AND_HELD /
POST_HOC_NORMALIZATION_NONE /
FRESH_EVENT_DERIVED /
FRESH_A_B_PACKAGES_PREPARED /
FUTURE_B_BLINDNESS_PRESERVED /
ZERO_PROVIDER /
ZERO_RUNTIME /
AWAITING_CONTROL_ROOM_READBACK /
NO_REPLACEMENT_EXECUTION_AUTHORITY
```

Maximum allowed state reached and NOT exceeded: fresh event `PREPARED_ONLY` = `evt-aa640691cfe9d33c`; fresh A package `PREPARED / FROZEN`; fresh B package `PREPARED / FROZEN / SINGLE-WRITER-BOUND`; hardening scope EXACTLY `PCH-002 = TOP_LEVEL_CLOSED_SHAPE_FIRST_PASS_OUTPUT_PROMPT_HARDENING` (DEFENSE-IN-DEPTH PROMPT-CONFORMANCE HARDENING / EXTERNAL-AUDITOR-OUTPUT-RISK REDUCTION / NOT PRODUCT-DEFECT REMEDIATION); deployment NONE; launcher adaptation NONE; driver/wrapper creation NONE; chmod NONE; runtime attempts NONE; AccountingStore NONE; credential content read NONE; provider/model execution ZERO; replacement execution authority NONE; qualification NONE; installation NONE. The newly prepared event/packages are NOT admitted for execution until an independent Control Room readback.

**EXEC-RA-002 held state (NOT rewritten)**: `ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH`; Disposition A `AUDITOR_OUTPUT_STRUCTURAL_NONCONFORMANCE` — the deployed Auditor-B final response was a JSON object whose top-level key set did not equal the exact ten-key contract/validator set (WHICH keys were missing or added remains UNDETERMINED; both PCH1-generation report artifacts remain SEALED/UNREAD; identity-only operations throughout this preparation; no key-name inference). Never relabeled as an Audit Council product defect.

## 2. Previous PCH-002 preparation STOP + Control Room scope amendment

- **PCH2_PREPARATION_ATTEMPT_01 = FAIL_CLOSED_STOP / NO_WORKSPACE / NO_SELECTION / NO_EVENT / NO_PACKAGES / NO_CANONICAL_RECORD / NO_GIT_MUTATION / NO_RUNTIME** — verified this session BEFORE any work: no PCH2 workspace existed under /home/isa, the PCH-002 identifier `AUCDEV023-CR-S1-RB001-L1-RB003-PCH-002` and this task's authority identity had ZERO occurrences in the git tracked tree at the base, full history (`--all -S` + commit messages), and the working tree. The stopped task created NO preparation authority transition.
- The blocker was independently re-verified mechanically this session: frozen EBS `AUDITOR_INVOCATION_ITEM_MAX_BYTES = 1024` with the fail-closed per-item size check present in `bootstrap-supervisor/ebs/binding.py` (staged EBS source verified byte-equal to the accepted generation, package identity `d42aa9e3…`); accepted PCH1 Auditor-A prompt reconstructed at EXACTLY **1020 UTF-8 bytes** and Auditor-B at EXACTLY **1021 bytes** by pure text assembly from the accepted PCH1 builder bytes — 4/3 bytes of headroom, mechanically insufficient for any additive PCH-002 top-level clause. Classification: CONTROL_ROOM_TASKING_CONSTRAINT_CONFLICT / OBSERVED FACT / HARNESS_PROTOCOL_TASKING_DEFECT / NON_PRODUCT_DEFECT / RESOLVED_BY_THIS_SCOPE_AMENDMENT.
- **Scope amendment honored**: the prior TEXTUAL-PRESERVATION constraint on natural-language prompt wording was superseded; prompt text was compressed/reworded SOLELY to preserve exact semantics within the frozen 1024-byte item limit. The EBS byte limit, validator, schema, harness semantics, single-writer architecture, argc-8 B invocation, `--output-last-message` exactly once, prompt-final-positional, canonical-path-absent-from-B-prompt, no tool-write report instruction, no output repair/normalization/stripping, target-schemas-evidence-only, empty-`findings[]` validity, credential restrictions, and fail-closed binding/package verification were ALL left UNCHANGED.

## 3. Live base (mandatory bootstrap, EXACT — no drift)

- Repository `isakli05/audit-council-dev`, branch `master`.
- Base commit `b96a8eafc38dda3c92cec141d800cbcfb8fbc30b`, root tree `5c87325f2e0714fe336d35ea03a51c7cd2a9c7ea`, sole parent `9c39b219465c2dc025c45b3ef41d5bb310954d50` — resolved EXACT as live GitHub `refs/heads/master` at bootstrap (== local HEAD == FETCH_HEAD; no drift; no auto-rebase) and re-resolved EXACT immediately before staging.
- Canonical blobs at the base verified EXACT: EXEC-RA-002 diagnostic `d84943fdcf9d45617c34a43626f995c177dc6a3b`, CURRENT `52dab8de271c351846d0facbab7a2c28df9a7bfb`, BACKLOG `c7fe94c18684b3bdea2e8b27612ce37da8059427`, PCH1 preparation `5ab8ba0f1daa245e295a4644f1898d7dfa34c1d6`, PCH1 preparation Control Room readback `f01fb6a629551c51d59f65c025ddd5ca77b860c6`, historical EXEC-RA-001 diagnostic `6ace36554c175fd1f1176e4e196c25181495a4c9`.
- Protected trees verified EXACT at HEAD: `bootstrap-supervisor` `732b8def9f22d7c466ce77f3d3049da53bfff3d0`, `qualification-harness` `5b8d5e5465923740470ff63ed9b8683f257a3787`, `skill` `c792933a862d9a5434681a88d183470dd8b15d2f`; the five immutable governance pins each present exactly once. Lineage HELD: trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor, merges since anchor 0, changed paths since anchor all under `docs/chatgpt-project/` (0 offending). Tracked working-tree drift limited to the pre-existing smoke-fixture/smoke-fixture-103 gitlink rows outside governed paths (recorded honestly, NOT staged).

## 4. Held EXEC-RA-002 / terminal-history facts preserved (non-transfer rules honored)

- The deployed PCH1 event `evt-5cb2c58f855415c3` remains DEPLOYED and immutable (pinned byte-identical BEFORE the build and enforced byte-identical AFTER the freeze, together with its terminal `evt-5cb2c58f855415c3-A-01` REPORT_FROZEN attempt and `evt-5cb2c58f855415c3-B-01` REPORT_INVALID attempt, all SEVEN event backups, the COMPLETE 27-root attempts tree, the terminal accounting sequences of EXEC-05/RB-001-L1/RB002/RB003/PCH1, the COMPLETE accepted PCH1 preparation workspace, the prior corrected prep workspace, the EXEC-RB-004 implementation workspace, the EXEC-RB-003 diagnostic workspace, the rejected RB003 preparation workspace, the run-evidence directories and the input handoff archives).
- The PCH1 Auditor-A frozen report `dbc47587…`/28465/0444 and the Auditor-B 117-byte invalid snapshot `5a7d105b…`/0600 remain **SEALED / UNREAD / UNADJUDICATED** (identity-only hash/stat; never opened, parsed, quoted, normalized or stripped). The specific missing/added key names of the Auditor-B nonconformance remain UNDETERMINED and were NOT inferred, named or licensed by any artifact of this preparation.
- Consumed replacement execution authority `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` remains CONSUMED/TERMINAL/CLOSED/NO_RERUN; its driver `7a8389a3…`/166778/0700 and wrapper `5423ec76…`/3468/0700 were re-hashed identity-only and NEVER imported, executed or chmod'd; no retry, no authority reopening, no reconciliation; the historical consumed RB003 authority and all older consumed authorities remain untouched.

## 5. Compact builder (change boundary honored)

- Accepted mechanical base re-hashed EXACT from preserved evidence: the accepted PCH1 preparation builder `47dccba817a95a3de3963dd66898e4ef12811f66a49e3724631a9cef5ba0a8ec` / 61018 B / 1208 lines. Baseline copy pinned read-only in the fresh workspace.
- **NEW compact builder** = `485a4abbe4c0d0a8087f698314680c4af31b3b4bb8e2f862d0843b8b2d9b8969` / 62778 B / 1234 lines (py_compile PASS), constructed by anchored fail-closed patching with EXACTLY these authorized diff classes:
  - module docstring → PCH2 provenance (scope amendment, previous STOP, merged clause) — `LABEL_OR_PROVENANCE_ONLY`;
  - `WS` + `SELECTION_SCHEMA` → this fresh workspace and the PCH2 selection schema — `IDENTITY_OR_WORKSPACE_REBIND` (EVENT_ID stays DERIVED AT LOAD TIME from the persisted selection; `_derive_event_id_from_selection` UNTOUCHED);
  - `PCH1_A_CLAUSE` + `PCH1_B_CLAUSE` constants REPLACED by the single merged `COMPACT_CLOSED_SHAPE_CLAUSE` (364 B); `B_FINAL_RESPONSE_ONLY_CONTRACT` reworded to the exact Control-Room-approved 105-byte sentence; `B_NO_TOOL_WRITE_CONTRACT` reworded to the exact 64-byte sentence; `auditor_prompt` (A) and `auditor_b_prompt` (B) rewritten to the exact compact templates — `PROMPT_TEXT_SEMANTIC_COMPRESSION`;
  - ROLES invocation comments + `identity_derivation` provenance prose — `LABEL_OR_PROVENANCE_ONLY`.
- **AST acceptance PASS: 23 top-level functions, 20 AST-identical — including `_require_bound_b_output`, `_derive_event_id_from_selection`, `build_binding_and_manifest`, `freeze`, `stage1` and every package-build/validation/parity/blindness/EBS/manifest/filesystem function — 3 changed (`auditor_prompt`, `auditor_b_prompt`, `assemble_gate_evidence`, the latter provenance-prose-only with every differing leaf a string Constant inside the `identity_derivation` dict), 0 added, 0 removed; module constants changed = exactly {`WS`, `SELECTION_SCHEMA`, `B_FINAL_RESPONSE_ONLY_CONTRACT`, `B_NO_TOOL_WRITE_CONTRACT`}, added = exactly {`COMPACT_CLOSED_SHAPE_CLAUSE`}, removed = exactly {`PCH1_A_CLAUSE`, `PCH1_B_CLAUSE`} (merged); PCH-08 structural census of mutating/normalization constructs EQUALS the accepted builder (no del/pop/normalization code added).**

## 6. The exact compact prompt templates (§ byte-budget acceptance)

The merged common closed-shape clause carried IDENTICALLY in BOTH role prompts:

> Root keys EXACTLY schema,event_id,auditor_role,attempt_id,target_commit,summary,findings,coverage,residuals,methodology; finding keys EXACTLY id,title,severity,description,evidence; evidence-item keys EXACTLY source,detail. Target-repo schemas are evidence only, never output shape. Empty findings[] is valid. Self-check all three exact key sets; add/omit no keys.

- **Auditor-A compact template — EXACTLY 755 UTF-8 bytes** (live-verified from the frozen binding; 269 bytes of headroom under the frozen 1024-byte item bound): `You are Auditor-A of AUCDEV-023 event {EVENT_ID}. Read /evidence/common/prompt-contract.json and perform exactly its independent first-pass review. Write /auditor-output/{A_OUTPUT_NAME} as one AUCDEV-023-FIRST-PASS-REPORT-V1 JSON object. {merged clause} No prose outside the report. Never read, print or copy credential files under /auditor-home or /auditor-init.` (accepted PCH1 A prompt: 1020 bytes).
- **Auditor-B compact template — EXACTLY 939 UTF-8 bytes** (live-verified from the frozen binding; 85 bytes of headroom): `You are Auditor-B of AUCDEV-023 event {EVENT_ID}. Read /evidence/common/prompt-contract.json and perform exactly its independent first-pass review. Your FINAL response is the canonical report payload: ONLY one AUCDEV-023-FIRST-PASS-REPORT-V1 JSON object; no Markdown fence, preamble, epilogue or explanatory text. {merged clause} Do NOT create/write/modify report artifacts via tools/filesystem; the harness client's --output-last-message alone persists your final response to the bound output path. Never read, print or copy credential files under /auditor-home or /auditor-init.` (accepted PCH1 B prompt: 1021 bytes).
- No second/redundant clause was added; every auditor_invocation item computed 1..1024 inclusive; `parse_binding` PASS for both bindings through the exact live EBS.

## 7. Semantic preservation (nothing dropped to meet the byte budget)

Machine-readable matrix `evidence/semantic-preservation-matrix.json`: **19/19 requirements PASS** — 13 PCH1 requirements (event report schema authority; target schemas evidence-only; finding exact key set; evidence exact key set; NO sixth finding key; self-check; empty findings valid; no extra keys; no prose outside the report artifact (A) / canonical final response (B); no canonical report tool write for B; final-response-only single writer for B; credential prohibition) + 6 PCH2 requirements (exact ten root keys; no eleventh root key; no omitted root key; no alternate root envelope; target schemas cannot replace the event root schema; root key-set self-check), each mapped to the compact text carrying it, checked in BOTH new prompts under identical event substitution with the accepted PCH1 builder loaded side-by-side.

## 8. Fresh selection material + derived event

- Selection material `AUCDEV023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-COMPACT-FRESH-REPLACEMENT-EVENT-SELECTION-V1` (EIGHT schema fields exactly once: authority, live_base, hardening_builder_sha256, frozen_target, current_deployed_event, consumed_predecessor_authority, diagnostic_record_blob, purpose) persisted as exact UTF-8, LF-only, exactly one final newline. **Byte count = 689; SELECTION_SHA256 = `aa640691cfe9d33c867e1cc9c5b9e050eb8bbfddf8ae445935477ef157a325e5`; `hardening_builder_sha256` COMPUTED DIRECTLY FROM THE FINAL COMPACT BUILDER BYTES (`485a4abb…`) immediately before serialization — never manually transcribed.**
- Derived (never manually selected): **`EVENT_ID = evt-aa640691cfe9d33c`** (`"evt-" + first_16_lowercase_hex(selection_sha256)`; charset `evt-[0-9a-f]{16}`).
- Fail-closed selection-provenance gate SEL-01..18 run in the mandated phases, each independently parsing from bytes: **phase A in-memory BEFORE persistence (18/18), phase B persisted BEFORE package generation (18/18), phase C AFTER package freeze (18/18)**; phase D runs immediately before the generated-LAST handoff (evidence in the handoff archive).
- **FRESH_EVENT_ID_COLLISION_CHECK_PASS**: ZERO occurrences of `evt-aa640691cfe9d33c` across the live tracked tree at the exact base; `git log --all` pickaxe + commit messages + `%B` history universe; repository working tree; every `/home/isa/aucdev023*` + `audit-council-dev` filesystem surface (names + contents; `*.first-pass-report.json` report bodies and credentials excluded from content scans by rule; large binaries >64 MB skipped by content with pinned identities elsewhere); **133 `.tar.gz`/`.tgz` archives** (member names + streamed member contents); the deployed launcher-root namespace (attempts/event/backups); derived `evt-aa640691cfe9d33c-A-01`/`-B-01` ABSENT from the live launcher-root attempts namespace. None of `evt-60636835d5fd6f37` / `evt-f5bd9785d50a76f7` / `evt-4a51f4b9413a1476` / `evt-5cb2c58f855415c3` reused.

## 9. Fresh workspace + event rebinds

- Fresh isolated workspace `/home/isa/aucdev023-s1-rb001-l1-rb003-exec-ra002-pch2-compact-fresh-replacement-package-prep-20260927-02/` (verified absent, no symlink, before creation). The accepted PCH1 prep workspace (component source), the deployed launcher root, the deployed event, and every historical location: NEVER mutated (pinned + verified byte-identical before AND after).
- `ebs-ro/bootstrap-supervisor` git-archived from live HEAD `b96a8ea…` (tree `732b8def…`, MANIFEST package identity `d42aa9e3…` recomputed EXACT; byte-equal to the accepted generation's EBS; the 1024-byte argv item constant and its fail-closed check verified present). `target-ro/{qualification-harness,skill}` git-archived from the FROZEN audit target `d4d584ff…` with per-file git-blob identity verification (135 rows) and byte-equality to the accepted generation.
- Components staged byte-identical from the accepted PCH1 workspace EXCEPT the compact builder (installed by bounded patching) and the event-id-bearing boundary sandbox profiles (regenerated); the eight pinned frozen component identities (launcher `011a8713…`, tool-domain wrapper `0ed2ba48…`, sentinel, probes, network-readiness `20f37e91…`, validator `6aff0e7e…`, resource-gate `27948980…`) verified against BOTH the accepted PCH1 workspace AND its recorded linter-facts digests.
- **Prompt contract**: accepted PCH1 contract `7679ac2d830c26f87d99d0bc60133a31efe24a90390bf35ce1d5f7b2a7434ffd` with EXACTLY its top-level `event_id` value regenerated → fresh **`fe5243f4730827b21b1a5ec1b318813a7e681006350131397b99081334cf47a1`** (exact one-line textual diff; parsed equality after event_id normalization; `report_requirements` byte-identical — report-shape semantics UNCHANGED; no new substantive audit requirement). Sandbox profiles regenerated event-id-only: A `a8009d6f…` → **`39d0b6a75561671b481cbc128cc8ea04a793776818fcb4b938580bde22d9557c`**, B `c0e23e37…` → **`7f56a574e5b6426e8d9e42e99c918f9d3c30caf64b1986d57f1d0d300400e51a`** (same normalization proof). Companion constant-only repoints: `identity_linter.py` (WS+EVENT_ID), `isolation_evidence.py` (WS+EVENT_ID), `blindness_map.py` (WS) — classification `AUTHORIZED_WS_OR_EVENT_IDENTITY_REBIND`.
- Common-evidence manifest regenerated for the fresh event: 169 members (mount-set EQUAL to the accepted generation), projection `7b85ab8272264b341e40793f653565c944bbe06430d5153f6714accfe03af4b9`.

## 10. Fresh frozen package / binding / MANIFEST identities

| Identity | Auditor-A | Auditor-B |
|---|---|---|
| attempt | `evt-aa640691cfe9d33c-A-01` | `evt-aa640691cfe9d33c-B-01` |
| output | `evt-aa640691cfe9d33c-A-01.first-pass-report.json` | `evt-aa640691cfe9d33c-B-01.first-pass-report.json` |
| binding-file SHA-256 | `075b2de246065c4828fedc588256686750f15b04579444ac60f973e287411f16` | `19ba43f5869ee5a57e1191a9699fa012f48cb75724d76a9b476c40d7b0443fc1` |
| canonical binding digest | `439ee7fb5a76376f9572c8a38364c7cba288afb4ef23d18844ded68d1023fdb2` | `b38c1a5105bb2ac8789fb536ac5d3ff39a440956aeb3e01b3e9038fd697550a6` |
| MANIFEST SHA-256 | `45adb9800ff3ef93e71d09e08629a44df324c362e562cd93118575c329b853bd` | `9b18bcb046ba8bdbef49ac4083b6aaf401f2fb65d1952e6339ce9aa051f63b4c` |
| package SHA-256 | `0637a86e14916d750b8c0cd7ce553c7594deaa30a17ea45b8719dcffe7a4caaf` | `796457a2db3a8e33549ed4347daf7ff7d7de73c303917cbfe5d7bea7c9191aa3` |
| rows | 191 | 194 |
| payload bytes | 236323090 | 343454621 |

Runtime closure staged from the accepted held-identity generation (frozen client `CODEX-CLI-0.154.0-NATIVE` `3188814c…`, `claude 2.1.274` `15e2d051…`, vendored closure byte-identical; frozen boundary launcher `011a8713…`/41270/0555 A/B byte-identical; frozen validator `6aff0e7e…`); `RUNTIME_CLOSURE_HELD_IDENTITY_MISMATCH` gate PASS at freeze; **`parse_binding` PASS both roles; `binding_projection` carries `auditor_invocation`; `verify_event_package` PASS both fresh packages**.

## 11. Single-writer contract held EXACT + Auditor-A mechanics held

- B invocation (frozen binding surface): `["codex", "exec", "--skip-git-repo-check", "--profile", "aucdev023-c3", "--output-last-message", "/auditor-output/evt-aa640691cfe9d33c-B-01.first-pass-report.json", "<compact auditor_b_prompt: 939 bytes>"]` — argc 8; first 7 elements byte-equal to the accepted PCH1 derivation under event substitution; `--output-last-message` exactly once; exact canonical destination argv-only and ABSENT from the instruction; prompt final positional; no `--output-schema`; `_require_bound_b_output` AST-IDENTICAL and PASS on the frozen binding; nine fail-closed refusal classes re-proven live (L1–L8, with L8: stripping the merged compact clause itself is refused as NOT the exact generated single-writer contract).
- Auditor-A argv shape byte-equal under event substitution (single prompt positional = the exact generated compact template); no `--output-last-message`; no retry loop; no report post-processing; no JSON key deletion; no automatic repair; no canonicalizer. Any future nonconforming output remains terminal/fail-closed.

## 12. Parity / blindness / hygiene

- A/B common-evidence parity PASS: transport pair + payload/evidence files byte-equal. Changed-file census vs the accepted PCH1 generation EXACTLY the authorized 11-file event-identity/invocation/provenance set per package, UNEXPECTED=0.
- Blindness re-established: maps consistent with the fresh profiles; zero first-pass report artifacts in either package; zero peer references (single sanctioned linter check-metadata occurrence); zero imported historical A/B report bytes; no cross-role disclosure. **FUTURE_AUDITOR_B_SUBSTANTIVE_BLINDNESS = PRESERVED**; no PCH1-generation Auditor-A/B report substance, key-name inference, finding titles/claims/descriptions/evidence or substantive values in either package.
- Hygiene: 191/194 census == MANIFEST rows; 0 symlinks/hardlinks/specials; frozen modes exact; secret-shape scan clean.

## 13. Zero-provider rehearsal + synthetic controls

- **Zero-provider single-writer rehearsal: 26/26 mandatory assertions PASS** (the accepted 20 + the 6 new compact-prompt assertions: B prompt bytes EXACTLY 939; argc EXACTLY 8; `--output-last-message` exactly once; prompt final positional; canonical path argv-only not in the prompt; within the frozen 1024-byte bound) with the EXACT compact fresh argc-8 B invocation and the EXACT frozen client (fail-closed asserted before every session), inside the isolated workspace, `--unshare-net` loopback-only with the deterministic mock the ONLY reachable endpoint (mock logs record ONLY `/v1/*`), synthetic credential marker bytes only: SW1 positive canonical delivery + validator PASS + outside-write probe refused; SW2 terminal-writer dominance (real mid-session tool write NOT becoming the canonical report); SW3 invalid-final-response persisted VERBATIM and rejected with no repair/manufacture; NPC no-profile write refused; SW4 staging census exact; correct frozen target-commit literal `d4d584ffa47ad2848268ba947247f81a845b2322`.
- **Synthetic differential controls through the EXACT frozen validator (`6aff0e7e…`; synthetic data ONLY — both sealed PCH1-generation reports NEVER touched)**: SYN-A minimal valid fresh-event report PASS; SYN-B sixth finding property FAIL `FINDING_INVALID_AT_0`; SYN-C target-side 10-key finding shape FAIL `FINDING_INVALID_AT_0`; SYN-D empty findings PASS; **SYN-E EVERY one of the ten single-missing-root-key controls FAIL `REPORT_KEYS_INVALID`; SYN-F one extra eleventh root key FAIL `REPORT_KEYS_INVALID`; SYN-G target-repository-shaped four-key root FAIL `REPORT_KEYS_INVALID` (target schemas cannot replace the event root schema); SYN-H/I/J2/K wrong schema/event/role/attempt VALUES FAIL with the DISTINCT tokens `REPORT_SCHEMA_UNEXPECTED`/`REPORT_EVENT_MISMATCH`/`REPORT_ROLE_MISMATCH`/`REPORT_ATTEMPT_MISMATCH`; SYN-N conforming control through a different valid attempt id PASSES exit 0.**
- **Recorded residual (explicit)**: these controls verify fail-closed enforcement of the frozen closed shape ONLY; they DO NOT prove that a future model will obey the compact prompt — future-auditor output conformance remains probabilistic (defense-in-depth residual).

## 14. Acceptance matrix

**83/83 PASS** = the accepted PCH1 suite adapted (A–Z, L1–L8 with L8 re-bound to stripping the merged compact clause, SW1–SW6, HYGIENE-a/b) **PLUS** `PCH-01..PCH-12` re-bound to the merged compact clause **AND** `PCH2-01..PCH2-06` (exact ten-key root shape; no eleventh root key; no omitted root key; no alternate root envelope; target schemas cannot replace the event root schema; root key-set self-check) **AND** `PCH2-BYTE` (A=755 / B=939 exact; both ≤1024) **AND** `PCH2-MATRIX` (the 19/19 merged semantic-preservation matrix) **AND** `SYN-A..SYN-N` (§13) **AND** the SEL block re-bound to the eight-field PCH2 selection schema (SEL-PHASES, SEL-19 compact-builder byte-binding recomputed, SEL-20 builder↔selection mutual derivation, SEL-21/22 binding event identities, SEL-23 contract, SEL-24 profiles, SEL-25 MANIFEST projections). SEL-26 (handoff selection member byte-identity) is enforced fail-closed inside the generated-LAST handoff builder. Any failure anywhere = STOP; nothing was normalized or repaired after the fact.

## 15. Zero-runtime / no-authority attestation

deployment NONE; launcher adaptation NONE; driver/wrapper creation NONE; chmod NONE; runtime attempts NONE (fresh A/B attempts ABSENT under the launcher root; no new-event surface); AccountingStore NONE; credential content read NONE (synthetic rehearsal marker bytes only; sealed report identities verified hash/stat only); provider/model execution ZERO (the frozen client executed ONLY inside the isolated preparation-workspace composition against the deterministic loopback mock with scripted bytes); replacement execution authority NONE; qualification NONE; installation NONE. Audit completeness INCOMPLETE; AUCDEV-023 remains P1 / READY / NOT DONE with NO queue-count transition (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11).

## 16. Residuals / evidence limits

- Compact prompt hardening is defense-in-depth ONLY: no proof (and no claim) that a future model output will conform; the fail-closed validator remains the enforcement boundary and any nonconforming output stays terminal.
- Compositional rehearsal scope only (the full EBS `Supervisor.run_attempt` custody lifecycle NOT executed); fixture/rehearsal results create NO execution readiness and NO execution authority.
- **R-PCH2-CR-1 = FULL_FROZEN_PACKAGE_BYTES_NOT_PRESENT_IN_REVIEWER_HANDOFF / FRESH_EXACT_EBS_PACKAGE_BYTE_REVERIFICATION_REQUIRED_BEFORE_ANY_FUTURE_PRELAUNCH_OR_DEPLOYMENT_ADMISSION**: the large frozen A/B package payload streams (236323090 B / 343454621 B) are represented in the generated-LAST reviewer handoff by complete per-file SHA-256/size/mode inventories and the frozen packages remain byte-frozen on disk at the preparation workspace for independent verification; any future prelaunch or deployment admission MUST freshly re-verify the exact package bytes through the exact live EBS with BOTH roles PASS.
- **FUTURE LAUNCHER RESIDUAL**: the existing PCH1 replacement launcher (driver `7a8389a3…` + wrapper `5423ec76…`) is NOT admitted for identity-only reuse — the future predecessor geometry changed (Auditor-A REPORT_FROZEN/conforming + Auditor-B REPORT_INVALID/nonconforming, engagements 2/2 consumed); a separately authorized launcher rebind/adaptation DESIGN must determine the minimum verifier delta. NOT designed or implemented here.
- Carried: R-PIMP-CR-1 (implementation-analyzer evidence-method residual; honored — driver/wrapper never imported or executed); R-PGPL-CR-1 (EBS gate ROOT-labelled assertion evidence-method residual); R-RA002-1 (validator target-commit format-only predicate); PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP (historical, subject authority consumed/terminal).
- Closure of this preparation is NOT claimed: `AWAITING_CONTROL_ROOM_READBACK` only.

## 17. Publication and generated-LAST handoff

- Exactly THREE changed tracked paths over base `b96a8eafc38dda3c92cec141d800cbcfb8fbc30b`: NEW canonical preparation record (this file) + CURRENT-STATE (current-facing fields rotation lines 3/11/23-25 + one dated record appended with blank separator) + BACKLOG (one dated record appended with blank separator). Exactly ONE docs-only fast-forward publication commit whose sole parent is `b96a8ea…`; live master re-resolved EXACT immediately before staging; the pre-existing smoke-fixture/smoke-fixture-103 gitlink drift outside governed paths preserved unstaged; the EXEC-RA-002 diagnostic, prior canonical records, deployed runtime, old attempts, report files, old packages, protected trees, AUCDEV-ARCHITECTURE-SUMMARY.md and AUCDEV-QUALIFICATION-HISTORY.md NOT modified.
- The generated-LAST reviewer handoff `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-COMPACT-FRESH-REPLACEMENT-PACKAGE-PREPARATION-HANDOFF.tar.gz` is produced AFTER this push and the post-push readback, with nothing included mutated afterward.

**NEXT ACTION EXACTLY ONE**: CONTROL ROOM READBACK OF THE EXEC-RA-002 / PCH-002 COMPACT PROMPT-CONFORMANCE HARDENED FRESH REPLACEMENT EVENT AND A+B PACKAGE PREPARATION AND ITS GENERATED-LAST HANDOFF BEFORE ANY OPERATOR-LAUNCHER REBIND/ADAPTATION DESIGN, LAUNCHER IMPLEMENTATION, PRELAUNCH DESIGN, DEPLOYMENT, RUNTIME ATTEMPT CREATION, CREDENTIAL-CONTENT READ, REPLACEMENT EXECUTION-AUTHORITY GRANT, AUDITOR/PROVIDER EXECUTION, QUALIFICATION, OR INSTALLATION.
