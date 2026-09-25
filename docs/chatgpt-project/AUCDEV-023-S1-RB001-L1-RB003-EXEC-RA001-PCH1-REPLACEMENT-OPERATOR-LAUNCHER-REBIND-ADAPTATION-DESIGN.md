# AUCDEV-023 S1 RB-001 L1 RB-003 EXEC-RA-001 PCH1 — Replacement Operator-Launcher Rebind/Adaptation Design (DESIGN ONLY)

```
PCH1_REPLACEMENT_OPERATOR_LAUNCHER_REBIND_ADAPTATION_DESIGN =
READY_FOR_CONTROL_ROOM_READBACK /
CURRENT_PREDECESSOR_GEOMETRY_MECHANICALLY_ESTABLISHED /
OLD_OLA001R1_USED_AS_HISTORICAL_STRUCTURAL_INPUT_ONLY /
FRESH_PCH1_EVENT_AND_PACKAGE_IDENTITIES_BOUND_AT_DESIGN_STRENGTH /
MINIMUM_PREDECESSOR_STATE_VERIFIER_DELTA_DEFINED /
DELTA_CONFINED_TO_BOUNDED_PHASE0_SURFACE /
SINGLE_HUMAN_DIRECT_INVOCATION_PRESERVED /
FAIL_CLOSED_NO_RETRY_NO_RESUME_PRESERVED /
FRESH_FUTURE_AUTHORITY_IDENTITY_RESERVED_ONLY /
FUTURE_IMPLEMENTATION_BOUNDED /
SEALED_REPORT_SUBSTANCE_UNREAD /
ZERO_RUNTIME /
NO_IMPLEMENTATION /
NO_EXECUTION_AUTHORITY /
NO_QUALIFICATION /
NO_INSTALLATION
```

- **Design authority**: `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-OPERATOR-LAUNCHER-REBIND-ADAPTATION-DESIGN-20260925-01`
- **Date**: 2026-09-25 (Europe/Istanbul)
- **Session role**: BOUNDED OPERATOR-LAUNCHER ADAPTATION DESIGNER / READ-ONLY EVIDENCE COLLECTOR — NOT the Control Room decision-maker, NOT a launcher implementation executor, NOT a deployment authority, NOT a prelaunch activator, NOT an execution controller, NOT an execution-authority grantor, NOT Auditor-A/B, NOT a credential-content reader, NOT a qualification authority, NOT an installation authority. This task is DESIGN ONLY: it created no driver/wrapper, chmod'd nothing, deployed nothing, created no runtime attempts, mutated no AccountingStore, read no credential contents, ran no dynamic real gate, invoked no auditor/provider, consumed/granted no execution authority, retried/resumed nothing, and inspected no sealed report substance.
- **Input status**: the accepted PCH1 package-preparation readback (blob `f01fb6a629551c51d59f65c025ddd5ca77b860c6` at commit `d8afb0ae469d922158de36159a68030e3654db46`) grants NO launcher admission, NO launcher implementation, NO prelaunch approval, NO deployment authority, NO replacement execution authority, NO audit verdict, NO qualification, NO installation. This design creates none of those either.

## 1. Exact live base identity (mandatory bootstrap, EXACT — no drift)

- Live GitHub `refs/heads/master` resolved EXACT `d8afb0ae469d922158de36159a68030e3654db46` == local HEAD at bootstrap; fetched at that exact SHA (FETCH_HEAD EXACT).
- Root tree `72a3c6907ed81751eb011ea80b9ab86d151c4210`; sole parent `7d6c928e513c6812d8eb4a46309bc74116980249` — both EXACT.
- Canonical blobs at the base verified EXACT: CURRENT `158ee6b8f0749844f54fd08534f8975386cfae41`, BACKLOG `2b7196667500d67c6e6f0d046020a2795fbbc074`, PCH1 package-preparation Control Room readback `f01fb6a629551c51d59f65c025ddd5ca77b860c6`, PCH1 preparation `5ab8ba0f1daa245e295a4644f1898d7dfa34c1d6`, execution mechanical readback `bfe9664bdfa2b037e75b8083039d43aa223b991c`, EXEC-RA-001 zero-provider structural diagnostic `6ace36554c175fd1f1176e4e196c25181495a4c9`.
- Protected trees verified EXACT: `bootstrap-supervisor` `732b8def9f22d7c466ce77f3d3049da53bfff3d0`, `qualification-harness` `5b8d5e5465923740470ff63ed9b8683f257a3787`, `skill` `c792933a862d9a5434681a88d183470dd8b15d2f`.
- Lineage HELD: trust anchor `3058868416241d394cfaaa40cc585085db486f37` IS ancestor; ZERO merges since anchor; 30 changed paths since anchor ALL under `docs/chatgpt-project/` with 0 offending. Tracked working-tree drift limited to the pre-existing `smoke-fixture`/`smoke-fixture-103` gitlink drift outside governed paths — recorded honestly, NOT staged.

## 2. Source / evidence inventory (read at the exact live SHA; saved read-only)

Canonical records read: CURRENT-STATE; BACKLOG; PCH1 fresh-replacement package preparation (blob `5ab8ba0f…`) and its Control Room readback (`f01fb6a6…`); RB-003 first-pass execution mechanical readback (`bfe9664b…`); EXEC-RA-001 zero-provider structural diagnostic (`6ace3655…`); OLA-001 narrow design amendment (`08f87f03…`) and its Control Room readback (`25de8229…`); OLA-001 reimplementation (`b8a75e37…`) and its Control Room readback (`7237b38f…`); RB-003 prelaunch transition design (`18edf81f…`) and its Control Room readback (`c5a9280b…`); AUCDEV-CONTROL-ROOM-RUNBOOK (`a1d27ed1…`); AUCDEV-PROJECT-UPDATE-PROTOCOL (`42955b85…`).

## 3. Reviewed PCH1 CR handoff — verified read-only, ZERO members executed (DES-03)

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-FRESH-REPLACEMENT-PACKAGE-PREPARATION-CONTROL-ROOM-READBACK-HANDOFF.tar.gz`: outer SHA-256 `83278f22754038819f3205f5971a3ca948c39abd620084eeee919d525ea257c8` / `864374` B EXACT (regular, isa, 0644). Census EXACTLY 43 regular members = 42 payload + 1 SHA256SUMS; 0 directories/absolute/traversal/duplicate paths; 0 symlinks/hardlinks/special files; SHA256SUMS 42 rows, **42/42 checksums PASS by read-only streaming re-hash**, 0 missing, 0 unlisted; the sealed report blob `4af00532…` is ABSENT from the archive (identity-only comparison). Integrity PASS.

## 4. Current deployed predecessor mechanical geometry (DES-06..09)

Deploy root `/home/isa/aucdev023-s1-prep002-rem002`; deployed event root `…/event` carries the **`evt-4a51f4b9413a1476`** generation, verified at metadata strength this session: binding `binding-auditor-a.json` = `f2dada28ecab4ea850a8f4e820047d2493d9751e2bec357bc714bfad77ede755`, `binding-auditor-b.json` = `121f359dd7ab8dfaf0ffcf0f1bcd3365d27dd3a10c8c2adfc214ed69cc693325`, MANIFESTs `f0898c99ef43b097c70ccaec458e107ef1091f0fa66fedd4f67bcce55fbc97da` / `ddfcc31fbb67c8db51e2a5a4154d65ab17343da31bfe94b7771e51f4b78b436c` — all EXACT. Six historical backups present and untouchable (`pre-successor-event`, `pre-exec03-new-event`, `pre-exec02`, `pre-rb001-l1-successor-event`, `pre-rb002-successor-event`, `pre-rb003-corrected-successor-event`); historical staging `event.staging.rb001-l1-rb003-4a51f4b9` consumed/ABSENT.

**Predecessor Auditor-A (terminal)** — attempt `evt-4a51f4b9413a1476-A-01`:
- accounting `…/attempts/evt-4a51f4b9413a1476-A-01/accounting/evt-4a51f4b9413a1476-A-01.jsonl` = SHA-256 `816658e8008c58712a66345e345d765ad1c9dc57f892a490cf021d4c812505bf` / 5677 B / mode 0600; state sequence EXACTLY `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_INVALID → TERMINAL` (6 records; mechanical state fields only).
- sealed report at the exact staging pathname `…/attempts/evt-4a51f4b9413a1476-A-01/staging/evt-4a51f4b9413a1476-A-01.first-pass-report.json` = SHA-256 `4af005323ab5803ec876f63a73426d9445abde0815a8e9c0e16d8e340da047bb` / 28361 B / mode 0600 / regular isa:isa — **identity-only (hash/stat); substance NEVER opened, parsed or quoted**; report-suffixed census under the A attempt root = EXACTLY that one path; `custody-out` EMPTY.

**Predecessor Auditor-B (NOT_RUN)** — the B attempt root `…/attempts/evt-4a51f4b9413a1476-B-01` is **ENTIRELY ABSENT**; no B accounting record exists anywhere under the attempts root (bounded probe); no B report artifact exists; the unused 1/2 engagement budget of the consumed authority is NOT authority and licenses no B execution.

Attempt-root census: 25 roots = 24 historical + exactly `evt-4a51f4b9413a1476-A-01`; fresh `evt-5cb2c58f855415c3-A-01`/`-B-01` ABSENT. Historical invocation-evidence context `rb003-l1-ola001r1-run-evidence/AUCDEV-023-S1-RB001-L1-RB003-FIRSTPASS-EXEC-20260925-01` present (terminal historical runtime evidence, untouched).

## 5. Old OLA001R1 — historical/structural input ONLY (DES-05, DES-11)

Re-hashed read-only this session, NEVER executed/imported/sourced/chmod'd:
- driver `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-4a51f4b9-ola001r1.py` = `1863c3439253ec66470c558fa64720250bda166c4bf25f72241be5a603d14420` / 165613 B / 3336 lines / isa:isa / current mode 0700 (the historical post-activation consumed-authority state; recorded honestly — this design assumes nothing about it);
- wrapper `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-4a51f4b9-ola001r1.sh` = `ac258cb362cded97d0a952b5969db3b2cb62b4ef0d3d4f8a42b1a6905fc98c1e` (canonical lowercase) / 3426 B / 82 lines / mode 0700; pins `REQUIRED_DRIVER_SHA256=1863c343…`, `REQUIRED_DRIVER_MODE="700"`.

These artifacts executed the now-terminal historical authority over predecessor `evt-60636835d5fd6f37`. Their authority, target event, predecessor geometry and prelaunch approval do NOT transfer to PCH1. Structural facts established by static source read + `ast.parse` (no import/execution):

- 52 top-level functions; ALL 12 predecessor-pin constants (`HISTORICAL_EXEC05_{A,B}_ACCOUNTING_{SHA,SIZE}`, `…_{A,B}_STATES`, `…_{A,B}_REPORT_{SHA,SIZE,MODE}`) are referenced by EXACTLY ONE function — `phase0_operator_host_check` (AST-verified). No other function references predecessor state.
- Old predecessor verifier semantics (phase0 §14 block): a per-role loop requiring BOTH A and B accounting records PRESENT with pinned sha/size/state-sequences; an Auditor-A exact-identity report verifier at the **custody-out** pathname (pins `812ffb26…`/34217/`"0o444"`); an Auditor-B exact-identity verifier at the **staging** pathname with a report-suffixed census walk (pins `6a1f079f…`/202/`"0o600"`), refusal tokens `HISTORICAL_PREDECESSOR_{role}_ACCOUNTING_ABSENT_REFUSED` / `…_{role}_STATE_MUTATED_REFUSED` / `HISTORICAL_PREDECESSOR_{A,B}_REPORT_IDENTITY_REFUSED` — built for predecessor `evt-60636835d5fd6f37` (A REPORT_FROZEN, B REPORT_INVALID).
- Old EXPECT_NEW = `evt-4a51f4b9413a1476` package pins (A `f2dada28…`/`168d6678…`/`f0898c99…`/`206cd496…`/191/236321909; B `121f359d…`/`35169ee5…`/`ddfcc31b…`/`9a180955…`/194/343453864); old EXPECT_OLD = `evt-60636835d5fd6f37` generation pins. `classify_destination` and the pre-rename re-classification are fully table-driven by these dicts (data rebind surface). Deployment: verify-staging → re-classify EXPECTED_HISTORICAL → non-overwriting backup → atomic same-filesystem rename pair, INSIDE the single invocation. Phase-0 also refuses root execution, non-owner, existing new backup target, absent historical backups, present successor attempt roots (RETRY_REFUSED), existing handoff (non-overwriting), and creates the invocation-evidence context BEFORE any fail-able Git admission.

## 6. Fresh PCH1 event/package contract (DES-10; identities consumed from the accepted canonical readback at PREPARATION evidence strength)

- Fresh event `evt-5cb2c58f855415c3`; attempts `evt-5cb2c58f855415c3-A-01` / `evt-5cb2c58f855415c3-B-01`; selection SHA-256 `5cb2c58f855415c3752f40329a54e98be018356ac913c0d479a122f9dbade2a0` (635 B, eight fields); hardening builder `47dccba817a95a3de3963dd66898e4ef12811f66a49e3724631a9cef5ba0a8ec`.
- Deployment source root (the ONLY permitted future deployment source): `/home/isa/aucdev023-s1-rb001-l1-rb003-exec-ra001-pch1-fresh-replacement-package-prep-20260925-01/event` — present with both role trees; binding files re-hashed EXACT this session at metadata strength: A `7130cfc88ed6fdea1347c815e1b958c384eabda3534d33437243122e26f578e2`, B `68d622b291efcee25cea698165283561f94676481a3aec2e2532a8a48c7d70ab`; MANIFESTs `5d5eb70a9f938db19a12e2dec00af4c6fd97f10bb9eb4e40063eea8bc0609435` / `b5874d90dc9b101cd93763b0cb5b0badbed5e8e90381f01de0673e3838ef24fb` — all matching the accepted readback EXACT.
- Full A/B identity table (accepted readback §8): A canonical binding digest `48361f2d0488ffe980a1a734f93274e219cd1410cd794dbe2cf142e8ce6dcbbb`, package `e6b6631378342e0506c42d5e85d26b8de299610fcd9c754b1f0ac8099578defa`, 191 rows / 236323239 B; B digest `35cbc561b71f7b45e58b6470e746d4b7083b2640abbfec4ddafe91de17508956`, package `bb6b06a4319cf98f77a7d7d4983bf85d979515a16d31b1275feb3352c5ae48dd`, 194 rows / 343454376 B. Prompts A 1020 B / B 1021 B (≤1024 bound); B single-writer invocation EXACT argc 8 with `--output-last-message /auditor-output/evt-5cb2c58f855415c3-B-01.first-pass-report.json` exactly once, argv-only.
- Held frozen identities: validator `6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071`; prompt contract FRESH `7679ac2d830c26f87d99d0bc60133a31efe24a90390bf35ce1d5f7b2a7434ffd` (event-id-only regeneration of `4d3c168b…`, schema semantics UNCHANGED); frozen target `d4d584ffa47ad2848268ba947247f81a845b2322`; EBS plane manifest `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999` / package `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8` at bootstrap-supervisor `732b8def…`; boundary launcher `011a8713…`; resource gate `27948980…`; auditor executables A `15e2d051…` (claude 2.1.274) / B `3188814c…` (codex 0.154.0); frozen 20-path 0555 executable mode table (mode census A 183×0444+9×0555 / B 184×0444+11×0555 = the accepted 20-path set).
- **R-PCH1-CR-2 carried (DES-20)**: the 236 MB / 343 MB host package byte streams were NOT re-hashed by this design and are supported by complete inventories + binding material + recorded EBS verification at the accepted readback strength. Fresh exact-EBS verification of the frozen package bytes is MANDATORY before ANY future prelaunch/deployment admission.

## 7. Exact difference classification (minimum-diff analysis; DES-12, DES-13)

Every required difference between the accepted OLA001R1 driver/wrapper (`1863c343…`/`ac258cb3…`, historical structural input) and the proposed future PCH1 contract classifies into EXACTLY the three authorized classes. No fourth class is required.

### 7.1 IDENTITY_OR_DATA_REBIND (module constants; zero control-flow effect)

1. `AUTHORITY_ID` → `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` (§9; also the `HANDOFF_PATH` literal; `INVOCATION_DIRNAME` derives automatically).
2. `EVENT_ID` → `evt-5cb2c58f855415c3`; `ATTEMPT` → `evt-5cb2c58f855415c3-A-01`/`-B-01`.
3. `SOURCE_EVENT_ROOT` → the PCH1 preparation workspace event root (§6).
4. `DRIVER_PATH` / `WRAPPER_PATH` / `EVIDENCE_BASE` → the NEW future artifact names (contract §10; values unknown until implementation).
5. `STAGING_DIRNAME` → a fresh unique staging tag (e.g. `event.staging.rb001-l1-rb003-5cb2c58f-pch1`; probed ABSENT); `BACKUP_DIRNAME` → a fresh fixed backup name for preserving the `evt-4a51f4b9413a1476` generation (e.g. `event.backup.pre-pch1-replacement-event`; probed ABSENT).
6. `HISTORICAL_BACKUP_DIRNAMES` → SIX entries: the five historical PLUS `event.backup.pre-rb003-corrected-successor-event` (now historical, present on host).
7. `EXPECT_NEW` → the PCH1 role pins of §6 (per-role binding_file/canonical/manifest/package/rows/payload_bytes + `event` → `evt-5cb2c58f855415c3`; `exe_sha` values HELD).
8. `EXPECT_OLD` → the currently deployed `evt-4a51f4b9413a1476` generation pins (A `f2dada28…`/`168d6678…`/`f0898c99…`/`206cd496…`/191/236321909; B `121f359d…`/`35169ee5…`/`ddfcc31b…`/`9a180955…`/194/343453864; `event` → `evt-4a51f4b9413a1476`; `launcher_sha`/`gate_sha` held-equal).
9. Predecessor pin VALUES: A-accounting sha/size/states → `816658e8…`/5677/`(PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, REPORT_INVALID, TERMINAL)`; A-report sha/size/mode → `4af00532…`/28361/`"0o600"`; B-accounting/B-report pins RETIRED (replaced by the §8 absence invariant).
10. `PROMPT_CONTRACT_SHA` → `7679ac2d…` (fresh contract; referenced only in `build_handoff` evidence — data).
11. HELD constants (no change permitted or required): `SOURCE_TRUST_ANCHOR_COMMIT`, `GOVERNANCE_DOCS_PREFIX`, `PINNED_RECORD_BLOBS` (five immutable records remain exact), `PROTECTED_TREES`, `FROZEN_TARGET_COMMIT`, `REPO`, `EBS_ROOT`, `DEPLOY_ROOT`/`DEPLOY_EVENT`/`ATTEMPTS_ROOT`, EBS plane pins, `LAUNCHER_SHA`/`HISTORICAL_LAUNCHER_SHA`/`GATE_SHA_NEW`/`NETWORK_READINESS_SHA`/`OUTPUT_VALIDATOR_SHA`/`TOOL_WRAPPER_SHA`/`PROBE_TRUE_SHA`, `EXEC_TABLE`/`EXEC_REL_PATHS`/`ROOT_BINDING_FILES`, credential contracts (paths only), `CREDENTIAL_*`, barrier constants.

### 7.2 LABEL_OR_PROVENANCE_ONLY

Module docstring (authority/event/backup-list/provenance prose), comments surrounding the rebind constants, `build_handoff` title/evidence label strings (e.g. the historical-predecessor-generation title line), wrapper docstring/pins presentation. Zero AST-behavior effect.

### 7.3 AUTHORIZED_PROPOSED_PCH1_PREDECESSOR_STATE_VERIFIER_DELTA — `phase0_operator_host_check` ONLY, cardinality 1 function (§8)

## 8. Proposed predecessor-state verifier contract (DESIGN strength only; no code)

The single authorized semantic delta replaces the predecessor-state verification block inside `phase0_operator_host_check` so it verifies the MECHANICALLY TRUE current predecessor geometry (A terminal REPORT_INVALID with sealed staging snapshot; B NOT_RUN with no attempt at all). Required checks, each fail-closed with its own `DriverStop` refusal token:

**Auditor-A (predecessor `evt-4a51f4b9413a1476-A-01`) — present-and-exact:**
- **A-1** accounting file PRESENT at the canonical path `attempts/evt-4a51f4b9413a1476-A-01/accounting/evt-4a51f4b9413a1476-A-01.jsonl` — absence ⇒ `HISTORICAL_PREDECESSOR_A_ACCOUNTING_ABSENT_REFUSED`;
- **A-2** accounting identity EXACT: SHA-256 `816658e8008c58712a66345e345d765ad1c9dc57f892a490cf021d4c812505bf`, size 5677 — mismatch ⇒ `HISTORICAL_PREDECESSOR_A_STATE_MUTATED_REFUSED`;
- **A-3** state sequence EXACTLY `(PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, REPORT_INVALID, TERMINAL)` — mismatch ⇒ same refusal family;
- **A-4** report-suffixed census under the A attempt root == EXACTLY `[staging/evt-4a51f4b9413a1476-A-01.first-pass-report.json]` (os.walk census — the mirror of the existing OLA001R1 B-side census; proves custody-out stays EMPTY and no extra report artifact exists) — mismatch ⇒ `HISTORICAL_PREDECESSOR_A_REPORT_CENSUS_REFUSED`;
- **A-5** sealed report mechanical identity EXACT at that staging pathname: SHA-256 `4af005323ab5803ec876f63a73426d9445abde0815a8e9c0e16d8e340da047bb` / size 28361 / mode `"0o600"` (isfile + lstat + sha256_file; IDENTITY-ONLY — hash/stat; substance never opened, parsed or persisted) — mismatch ⇒ `HISTORICAL_PREDECESSOR_A_REPORT_IDENTITY_REFUSED`.

**Auditor-B (predecessor `evt-4a51f4b9413a1476-B-01`) — NOT_RUN absence invariant:**
- **B-1** the B attempt root is ENTIRELY ABSENT (`os.path.lexists == False`) — presence in ANY form ⇒ `HISTORICAL_PREDECESSOR_B_ATTEMPT_PRESENT_REFUSED`;
- **B-2** no B accounting record exists at the canonical accounting pathname (explicit defensive probe; vacuously implied by B-1 but kept distinct for observability) — presence ⇒ same refusal;
- **B-3** no report-suffixed artifact for the B attempt id under the attempts root — presence ⇒ same refusal;
- **B-4** the NOT_RUN geometry (`attempt_root_absent: true`) is recorded into the `historical_immutable` evidence structure (replacing the old B report identity/path entries).

**One conjunction or multiple independent checks?** — MULTIPLE INDEPENDENT fail-closed checks, each with a DISTINCT refusal token, sequentially enforced (each raises before the next runs). Mechanically clearer because: (a) precise per-predicate failure diagnostics in the generated handoff — directly answering the EXEC-RA-001 R-D4 observability residual (aggregate tokens obscure the failing sub-predicate); (b) no short-circuit masking — a single conjunction surfaces only the first mismatch while independent tokens identify the exact predicate; (c) the existing OLA001R1 verifier family already uses per-concern tokens, so independent checks keep the future AST delta minimal and reviewable; (d) fail-closed equivalence is exact — sequential independent raises are semantically the conjunction (NO success branch exists; success is only the fall-through of an all-exact match).

**Forbidden, absolutely:** any success bypass or else-branch; treating B-absence as license to create/infer a B attempt, B report or B verdict for the OLD event; retry/resume/fallback semantics; ALREADY_NEW as resume authority; pre-deployment mutation; report-substance access beyond hash/stat; downgrade of any other fail-closed gate; revival of the consumed authority. Evidence recorded into historical-immutable: A accounting sha/size/state-sequence, A report identity at its exact staging path, the census result, and the B NOT_RUN absence record — identity-only values.

**Structural containment proof (DES-14/15):** AST analysis of `1863c343…` proves all 12 predecessor pins are referenced ONLY inside `phase0_operator_host_check`; `classify_destination`, `deploy_generation`, `build_handoff`, `verify_*`, `prepare_attempt`, `execute_one_shot_attempt`, `evaluate_conformance`, `engagement_accounting`, `run_pipeline`, `main` are table/data-driven or logic-identical and require NO semantic change. The delta is confined to the bounded phase0 predecessor-state block; nothing outside `phase0_operator_host_check` changes behavior. The future implementation must reproduce this proof by AST diff at its own readback (acceptance classification: every function EXACTLY ONE of RAW_AST_UNCHANGED / LABEL_OR_EVIDENCE_NAME_ONLY / AUTHORIZED_PCH1_PREDECESSOR_STATE_VERIFIER_DELTA, category 3 permitted for `phase0_operator_host_check` ONLY with cardinality 1; any other structural difference ⇒ STOP `UNAUTHORIZED_DRIVER_BEHAVIOR_CHANGE`).

## 9. Fresh proposed execution-authority identity — RESERVED ONLY, NOT GRANTED (DES-18)

```
AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01
```

State in THIS design: **`RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE`**. Writing this identity grants NOTHING. It does NOT equal or alias the consumed `AUCDEV-023-S1-RB001-L1-RB003-FIRSTPASS-EXEC-20260925-01` (terminal CONSUMED/TERMINAL/CLOSED/NO_RERUN; unused 1/2 engagement budget NOT authority). Bounded collision sweep performed this session: ZERO occurrences across the git tracked tree at the base, full git history (`--all -S`), the working tree (excluding this task's evidence directory), `/home/isa` top-level workspace names, the attempts/backup namespace at the deploy root, and repo-root archive names; distinct from every existing authority-family id enumerated from CURRENT-STATE. No GRANT statement is written as though effective; a future grant requires the exact accepted human-operator pattern (`GRANT <id>` as an explicit separate operator message, only after the future implementation readback AND a future bounded prelaunch-transition design/readback are canonically accepted).

## 10. Future implementation artifact contract (DES-19; NO files created by this design)

A future, separately authorized implementation task must produce a NEW driver/wrapper pair: regular files, operator-owned (isa:isa), mode **0600**, NON-EXECUTABLE, NOT DEPLOYED, NOT ADMITTED FOR EXECUTION; their SHA-256 values are UNKNOWN until implementation and MUST NOT be invented. The future wrapper must pin the exact FINAL future driver SHA-256 and `REQUIRED_DRIVER_MODE="700"` (the intentional 0600/700 mismatch remains the closed prelaunch barrier), preserving all wrapper safety mechanics byte-for-byte in style (no CLI argument forwarding, no authority-override surface, root/symlink refusal, regular-file+owner checks, xtrace off, core dumps off, fixed PATH, env clearing, `/usr/bin/python3 -I`, no retry). The old OLA001R1 files are NOT the future candidate and must NOT be patched, chmod'd or renamed into apparent freshness. The future driver's phase0 must re-verify, at runtime, every §8 predicate against live state (design-time geometry can drift before execution — which is exactly why phase0 re-checks).

## 11. Preserved lifecycle — single human direct invocation, fail-closed, no retry/no resume (DES-16/17)

The future lifecycle remains structurally capable of the accepted two-stage human pattern: (1) future implementation + independent Control Room implementation readback; (2) future bounded prelaunch-transition design/readback; (3) separate explicit human operator grant of §9; (4) separately authorized chmod-only 0600→0700 activation (bytes re-hashed unchanged; neither artifact executed); (5) Control Room readback of the granted-prelaunch state; (6) EXACTLY ONE later HUMAN-OPERATOR-DIRECT wrapper invocation; (7) authority consumed fail-closed AT INVOCATION START regardless of outcome (including pre-Python-startup failure — marker absence never restores authority); (8) no retry/no resume/no fallback/no automatic rollback/no alternate artifact/event/attempt; any failure returns to Control Room. Deployment remains INSIDE the single invocation (activate→deploy→readback→execute remains REJECTED; pre-deployment would strand the granted authority on `DEPLOYED_EVENT_NOT_EXPECTED_HISTORICAL_PREDECESSOR`/`ALREADY_NEW` refusals). All other driver invariants held unchanged per §5/§7: source-trust anchor and publication-safe lineage admission; governed-path policy; protected-tree verification; package verification; EXPECT_NEW semantics (rebound); EXPECT_OLD deployment classification (rebound); deployment ordering; ALREADY_NEW refusal; attempt preparation ordering; Auditor-A FIRST; Auditor-B only after mechanically conforming Auditor-A; AccountingStore fail-closed semantics (CONSUMED_PRE_EXEC conservative charge; EXEC_ATTEMPTED = inference-capable fact); credential resolution/custody ordering (metadata-only prelaunch; contents read exactly once per authorized attempt by the custody pipe); resource/network/dynamic gate ownership; execution boundary mechanics; report custody (identity-only inventory); frozen structural validator `6aff0e7e…`; conformance evaluation; conservative engagement charging (max 2); barrier logic; no report repair/normalization (any nonconforming output stays terminal/fail-closed); no stdout/stderr report manufacture; generated-LAST handoff; `run_pipeline`/`main` control structure.

## 12. Blindness rules (DES-21)

The sealed predecessor Auditor-A report `4af00532…`/28361/0600 was verified by hash/stat/pathname/census ONLY this session; its substance was NEVER opened, parsed, string-inspected or quoted, and its unknown additional-property name remains undetermined with NO inference licensed. The design uses identity-only pins; the future verifier is identity-only (hash/stat). No sealed report substance appears in this record, the evidence, or the reviewer handoff; future-Auditor-B blindness is preserved (the fresh packages bind hardened prompts + frozen evidence payloads only).

## 13. Design acceptance matrix

| Gate | Check | Result |
|---|---|---|
| DES-01 | live Git identity exact (`d8afb0a…`, root `72a3c690…`, parent `7d6c928e…`) | PASS |
| DES-02 | canonical input blobs exact (CURRENT `158ee6b8…`, BACKLOG `2b719666…`, PCH1 CR readback `f01fb6a6…` + 9 further records) | PASS |
| DES-03 | reviewed PCH1 CR handoff integrity exact (`83278f22…`/864374 B/43 members/42+1/42-of-42 PASS; sealed blob absent) | PASS |
| DES-04 | protected trees exact (3/3) | PASS |
| DES-05 | old OLA001R1 source identities exact (`1863c343…`/165613/3336; `ac258cb3…`/3426/82; modes honestly recorded 0700; never executed) | PASS |
| DES-06 | current deployed predecessor identity exact (`evt-4a51f4b9413a1476` bindings+manifests at metadata strength) | PASS |
| DES-07 | predecessor A terminal accounting geometry established (`816658e8…`/5677/0600; 6-state REPORT_INVALID→TERMINAL) | PASS |
| DES-08 | predecessor sealed A report identity established WITHOUT substance read (`4af00532…`/28361/0600; census exactly 1; custody-out empty) | PASS |
| DES-09 | predecessor B NOT_RUN geometry established (attempt root absent; no accounting; no report) | PASS |
| DES-10 | fresh PCH1 event/package identities exact at accepted evidence strength (workspace bindings+manifests re-hashed; package bytes NOT re-hashed per R-PCH1-CR-2) | PASS |
| DES-11 | old verifier semantics statically established (full phase0 source + AST; 52 functions; pin-reference map) | PASS |
| DES-12 | required identity/data rebind set enumerated (§7.1, 11 entries + held set) | PASS |
| DES-13 | predecessor-state semantic delta minimized (§8; nothing beyond A-path/census + B-absence + pin values) | PASS |
| DES-14 | delta confined to `phase0_operator_host_check` (AST: all 12 predecessor pins phase0-only) | PASS |
| DES-15 | no other semantic/control-flow change required (all other functions table/data-driven or logic-held) | PASS |
| DES-16 | single-human-direct-invocation preserved (§11 lifecycle) | PASS |
| DES-17 | no-retry/no-resume/fail-closed accounting preserved (§11) | PASS |
| DES-18 | fresh authority identity collision-clean and NOT GRANTED (§9 sweep) | PASS |
| DES-19 | future candidate remains 0600/non-executable by design (§10) | PASS |
| DES-20 | package-byte residual carried to future prelaunch (§6 R-PCH1-CR-2 mandate) | PASS |
| DES-21 | sealed-report blindness preserved (§12) | PASS |
| DES-22 | ZERO runtime mutation (attestation §15) | PASS |
| DES-23 | ZERO auditor/provider execution (attestation §15) | PASS |
| DES-24 | publication geometry valid (§16: exactly 3 tracked paths, one docs-only fast-forward, sole parent `d8afb0a…`, `git diff --check` PASS, protected trees unchanged) | PASS |

## 14. Residuals and evidence-strength limitations

- **R-PDES-1**: PCH1 package identities are consumed at accepted-readback evidence strength; host package bytes were NOT re-hashed (binding files + MANIFESTs re-hashed EXACT at metadata strength). Fresh exact-EBS package-byte verification is MANDATORY before any future prelaunch/deployment admission (R-PCH1-CR-2 carried, binding).
- **R-PDES-2**: this design is STATIC: old-driver analysis used source read + `ast.parse` only (never imported/executed). The future implementation must independently reproduce the classification by AST diff; nothing here proves future runtime behavior.
- **R-PDES-3**: predecessor geometry was established at design time; live state may drift before any future execution — which is precisely why the future phase0 verifier re-establishes every §8 predicate at runtime, fail-closed.
- **R-PDES-4**: the proposed staging/backup/evidence/handoff names in §7.1 are ILLUSTRATIVE reserved-direction values verified pristine at design time; the future implementation fixes exact values and must re-verify pristineness then.
- **R-PDES-5**: the fresh authority identity collision sweep is bounded to the enumerated namespaces (git tree/history, working tree, `/home/isa` top level, attempts/backup namespace, archive names); the future prelaunch must re-run a fresh sweep.
- **R-PDES-6**: the old OLA001R1 driver/wrapper remain mode 0700 on the host (historical post-activation state). They are terminal historical artifacts; this design does not rely on, change, or "fix" their modes, and the future candidate must be NEW files at 0600.
- **R-PDES-7** (informational): `HISTORICAL_EXEC05_*` constant names are retained legacy internal identifiers (values rebind); the future implementation MAY rename them truthfully (label-only) but MUST NOT alter their phase0-only reference geometry.
- **R-PDES-8**: pre-existing `smoke-fixture`/`smoke-fixture-103` gitlink drift outside governed paths preserved unstaged.

## 15. Zero-runtime / no-authority attestation

THIS DESIGN performed and authorized NOTHING runtime: driver/wrapper creation/modification/chmod NONE; deployment NONE; staging NONE; runtime attempts NONE; AccountingStore mutation NONE; credential-content read NONE (no credential file opened at all); dynamic real gates NONE; boundary/auditor/provider/model execution ZERO; execution authority granted/consumed NONE; retry/resume NONE; qualification NONE; installation NONE; sealed-report substance access NONE (identity-only hash/stat). Local executions were this task's own deterministic read-only probes (git, sha256sum/stat, python tarfile streaming verification, python `ast.parse` of the never-imported driver). Network = the mandated bootstrap `git ls-remote`, the fetch at the exact base, the pre-staging live re-resolve, the single `git push` of this publication, and the post-push readback ONLY.

## 16. Publication of THIS record

Exactly THREE changed tracked paths over base `d8afb0ae469d922158de36159a68030e3654db46`: THIS NEW canonical design record + `AUCDEV-CURRENT-STATE.md` (current-facing fields rotation lines 3/11/23–25 + one dated record appended) + `AUCDEV-BACKLOG.md` (one dated record appended with blank separator). `git diff --check` PASS; exactly ONE bounded docs-only fast-forward publication commit whose sole parent is `d8afb0ae…`; live master re-resolved EXACT immediately before staging (STOP on drift; no auto-rebase). NOT modified: the old OLA001R1 driver/wrapper, packages, deployed event, attempts, AccountingStore, sealed reports, credentials, execution handoffs, historical backups, protected trees, `AUCDEV-ARCHITECTURE-SUMMARY.md`, `AUCDEV-QUALIFICATION-HISTORY.md`, historical canonical records. The generated-LAST reviewer handoff is produced after this push and the post-push readback, with nothing included mutated afterward.

## 17. Held historical truth (preserved verbatim)

EXEC-RB-001 = OPEN / ROOT_CAUSE_UNRESOLVED; EXEC-RB-002 = CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH; EXEC-RB-003 = ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_MECHANICAL_STRENGTH; EXEC-RB-004 = CLOSED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH; PREP-001 = CLOSED_AT_CONTROL_ROOM_PACKAGE_PREPARATION_READBACK_STRENGTH; OLA-001 = CLOSED_AT_CONTROL_ROOM_DESIGN_AMENDMENT_READBACK_STRENGTH; EXEC-RA-001 = ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH. PCH-001 remains DEFENSE-IN-DEPTH PROMPT-CONFORMANCE HARDENING / EXTERNAL-AUDITOR-OUTPUT-RISK REDUCTION / NOT PRODUCT-DEFECT REMEDIATION (the external auditor-output structural nonconformance is NOT converted into an Audit Council product defect). Old authority `AUCDEV-023-S1-RB001-L1-RB003-FIRSTPASS-EXEC-20260925-01` remains CONSUMED/TERMINAL/CLOSED/NO_RERUN; prior nonconforming candidate `15198c02…`/`1366785b…` remains permanently NOT_ADMITTED. AUCDEV-023 remains **P1 / READY / NOT DONE** with NO queue-count transition (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11); audit completeness INCOMPLETE; qualification NONE; installation NONE; installed source `8ae33444f349ce73c1359b963722e2d16acba630` with installed-qualified provenance NOT ESTABLISHED.

## 18. Next action — EXACTLY ONE

CONTROL ROOM READBACK OF THE PCH1 REPLACEMENT OPERATOR-LAUNCHER REBIND/ADAPTATION DESIGN AND ITS GENERATED-LAST HANDOFF BEFORE ANY LAUNCHER IMPLEMENTATION, DRIVER/WRAPPER CREATION, CHMOD, PRELAUNCH ACTIVATION, DEPLOYMENT, RUNTIME ATTEMPT CREATION, CREDENTIAL-CONTENT READ, REPLACEMENT EXECUTION-AUTHORITY GRANT, AUDITOR/PROVIDER EXECUTION, QUALIFICATION, OR INSTALLATION.

THIS DESIGN DOES NOT IMPLEMENT THE LAUNCHER, DOES NOT GRANT EXECUTION AUTHORITY, AND DOES NOT PROCEED TO PRELAUNCH.
