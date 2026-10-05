# AUCDEV-023 PCH6-B Path-B replacement Auditor-A minimum identity/authority binding — STOPPED AT PROTECTED AUTHORITY SEMANTICS BOUNDARY

**Status banner (dated 2026-10-05):** `AUCDEV_023_PCH6B_REPLACEMENT_AUDITOR_A_MINIMUM_IDENTITY_AUTHORITY_BINDING = MINIMUM_IDENTITY_AUTHORITY_BINDING_STOPPED_AT_PROTECTED_AUTHORITY_SEMANTICS_BOUNDARY / EXISTING_GOVERNANCE_EVENT_PRESERVED / SPENT_AUDITOR_A_01_NOT_REUSED / NO_REPLACEMENT_ATTEMPT_ID_CREATED / NO_REPLACEMENT_ATTEMPT_RESERVED / NO_REPLACEMENT_ATTEMPT_ALLOCATED / NO_AUTHORITY_TOKEN_FABRICATED / NO_ACCOUNTING_STATE_CREATED / NO_VALID_ATTEMPT_PACKAGE_COMPLETED / PROTECTED_BOOTSTRAP_AUTHORITY_UNCHANGED / SEPARATE_AUTHORITY_PROTOCOL_DESIGN_DECISION_REQUIRED / NO_EXECUTION_AUTHORITY / NO_REAL_RUNTIME / AUDITOR_B_AUTHORITY_NONE / AUDIT_VERDICT_NONE / QUALIFICATION_NONE / INSTALLATION_NONE`

**THIS PUBLICATION GRANTS NOTHING.** The minimum identity/authority-binding step correctly STOPPED at the protected-authority semantics boundary, and that STOP is the CORRECT successful fail-closed outcome for the granted authority — it is NOT a failed remediation, NOT an implementation defect and NOT a frozen-target product defect. Nothing in this record is an audit verdict, an attempt authorization, an identity/token creation or an execution authority of any kind.

## 1. Authority and role

Implementation authority `AUCDEV-023-PCH6B-REPLACEMENT-AUDITOR-A-MINIMUM-IDENTITY-AUTHORITY-BINDING-20261005-01` (this session). The operator authorized ONLY the minimum NON-EXECUTION identity / authority-binding step required to complete and freeze exactly ONE valid future replacement Auditor-A attempt-specific prelaunch package under the Control-Room-accepted active-v3 contract: permit creation/derivation and package binding of only the exact future machine-level event/attempt identity and package authority/grant token values proven mandatory by the accepted REQUIRED-BINDINGS matrix, while preserving the existing AUCDEV-023 governance event and creating no second governance event. The authority is package-binding authority ONLY and grants NO attempt execution authority, NO wrapper/driver invocation, NO credential access, NO credential-channel connection or probe, NO VM/QGA execution, NO run_attempt, NO model/provider execution and NO Auditor-B authority. The tasking's STOP clause — "if the canonical identity/token mechanism cannot create and bind those minimum values without creating runtime attempt/accounting state, consuming execution capacity, mutating the frozen event/runtime root, or otherwise crossing into execution authority, STOP before doing so and return to the Control Room" — was honored: the STOP fired on protected-authority semantics, before ANY machine attempt identity or authority token was created.

This session is the bounded IMPLEMENTER of that step. It is NOT the Control Room, NOT an attempt executor, NOT an execution-authority grantor, NOT an attempt-id allocator, NOT an authority-token minter, NOT an auditor, NOT an /audit-council executor, NOT an Auditor-A or Auditor-B attempt executor, NOT an attempt authority, NOT a provider/model/frontier executor, NOT starting or defining the event-host VM, NOT running virsh/QGA, NOT running send_once_v2.py or bridge-v2.py or any channel helper, NOT creating or consuming OPERATOR_SEND_NOW, NOT connecting to or probing the credential channel, NOT inspecting any real credential, NOT constructing or importing BootstrapAuthority, NOT calling run_attempt, NOT executing Claude, Codex or any provider/model, NOT granting Auditor-A or Auditor-B authority, NOT a qualification or installation authority, and NOT permitted to modify protected authority semantics or to instantiate runtime attempt/accounting state.

## 2. Mandatory live bootstrap — EXACT

Live GitHub master == origin/master == local HEAD == `5c88c8751576839cafd6c0f1e99f1ed63f839e1e` EXACT at bootstrap (ls-remote authoritative; fetch rc 0), re-resolved EXACT immediately before staging and again immediately before commit. Root tree `31e2c95a84c25ebe8ab8c3d9a3550a1116cb2739` EXACT. Sole parent `62b614f8179184fd3039a448f100e5138e7adb8f` EXACT (single-parent fast-forward geometry; the parent's own parent verified `e15067dedac37a15c3ff3680d937ebac0ca7246f`). Trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor rc 0. Frozen audit target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` (tree `2585796efd5cb6902226cfff785bb901297a15e3`) present, ancestor, UNTOUCHED, AUDIT SUBJECT / NOT AUTHORITY. Protected trees bootstrap-authority `154975872e15d53e1706016f5bb60c83727004f0` / bootstrap-supervisor `3056e577259ab0b0b0472f82ebc306506f3e084c` / qualification-harness `5b8d5e5465923740470ff63ed9b8683f257a3787` / skill `efd8c2e48edbb25795b3aacb1ce3c23fde10082a` held EXACT at base AND in the staged write-tree. The mandated canonical records were fetched at the exact base with blob identities verified (CURRENT `3d97704a281aa4b5c3ad2f7c4f0f8fadb7ee6d8c` / BACKLOG `e70f091a185230b6a9cb142bc7248201ff7761b2` / accepted pkgprep Control Room readback `38d95663459c2bd1dc41b784834be40516e814d6` / accepted pkgprep preparation record `cb3b6a93894e633e9cd4a15c5eecb87109b706d7` / update protocol `42955b85710f09579cd0fd9174d042de231d060d`), with the CURRENT/BACKLOG working copies verified byte-identical to the base blobs before editing. This record's path was ABSENT at base with zero full-history path rows. Repository drift (242 pre-existing untracked rows) preserved UNSTAGED. Publisher session euid 1000 (ordinary non-root isa).

## 3. Accepted inputs — verified EXACT

Accepted active-v3 procedure `FUTURE-AUDITOR-A-HOST-LAUNCH-PROCEDURE-active-v3.txt` SHA-256 `32460cd5011c29efd042e2a4c79f09efabb2662a211f2822410e6ee309f7852e` (12748 B) and accepted active-v3 binding `FUTURE-AUDITOR-A-HOST-LAUNCH-BINDING-active-v3.json` SHA-256 `801279b546ec0c0b590a9d7a3cf9993cb0cbd51c99a84830ee870cac945cae12` (6420 B), re-hashed EXACT this session on BOTH preserved live workspace copies AND the accepted data-only copies inside the preserved package-preparation workspace (byte-identical both directions; the artifacts NOT modified). Accepted REQUIRED-BINDINGS matrix `128d4cf6e3e90feaafeddf7d770700a122dc2d542415a905059ef0d2529619a1` (9465 B) re-hashed EXACT and copied byte-identical into the data-only bundle. Accepted matrix conclusion held: `ATTEMPT_ID_REQUIRED_FOR_COMPLETE_PACKAGE = TRUE`, `AUTHORITY_TOKEN_REQUIRED_FOR_COMPLETE_PACKAGE = TRUE`, `CAN_VALID_PACKAGE_BE_COMPLETED_WITHOUT_CREATING_ATTEMPT_IDENTITY = FALSE`. The existing governance event `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01` is PRESERVED; NO second governance event was created.

## 4. Canonical attempt-identity source — static proof over the exact protected bytes

The exact protected `bootstrap-authority/bootstrap_authority/binding.py` blob `1448c9cbfbb795c534f9f517052e998c636d28d6` (content SHA-256 `fa94691d23a84a917e98d38f57eeda4bb15fadbd8012f4d83515b9f18c4715c0`, 605 lines) was inspected DATA-ONLY (blob read plus `ast.parse` of the exact bytes — static analysis only; the module was NEVER imported, NEVER executed, and no doc-builder or runtime path was touched). Verified EXACT from the source bytes:

- line 72: `EVENT_ID = "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01"`
- lines 73-78: `RESERVED_ATTEMPT_IDS = {"AUDITOR_A": "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01", "AUDITOR_B": "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-B-01"}` — the Auditor-A reserved value sits at line 75
- line 79: `ROLES = ("AUDITOR_A", "AUDITOR_B")`
- lines 415-416: the strict parser requires `doc["event_id"] == EVENT_ID` (refusal `EVENT_ID_UNEXPECTED`)
- lines 421-425: the strict parser requires `doc["attempt_id"] == RESERVED_ATTEMPT_IDS[role]`, refusing any other value with exactly `ATTEMPT_ID_NOT_THE_RESERVED_IDENTITY_FOR_ROLE` (the failure token is emitted at line 424)
- AST census: `EVENT_ID` is assigned exactly ONCE and `RESERVED_ATTEMPT_IDS` is assigned exactly ONCE (single module-level constants; no writer, mutator or alternate identity table anywhere in the module); `parse_binding` is the single parse entry constructing `Binding`; the design-reserved constants' own comment (lines 68-71) states that parsing them does NOT instantiate the event, mint attempt capability, grant execution, or consume an engagement.

## 5. Replacement-identity representability decision

Determined by static reasoning over the exact source ONLY; NO candidate runtime identity was created, derived, synthesized or tested (rule C honored — no synthetic identity was generated merely to prove rejection). Rules honored: (A) reuse of `...-AUDITOR-A-01` is prohibited because it is spent/single-use/no-retry (verified from the canonical records: the accepted pkgprep Control Room readback `38d95663459c2bd1dc41b784834be40516e814d6` and the CURRENT status line hold the existing Auditor-A machine attempt as SPENT / SINGLE-USE / NO-RETRY); (B) a hypothetical `...-AUDITOR-A-02`, a random/UUID identity, a hash-derived identity, a timestamp-derived identity and a TEST-ONLY identity are ALL non-canonical because the protected parser rejects every one of them (none equals `RESERVED_ATTEMPT_IDS["AUDITOR_A"]`, so each fails closed at line 422 with `ATTEMPT_ID_NOT_THE_RESERVED_IDENTITY_FOR_ROLE`); (D) `RESERVED_ATTEMPT_IDS` was NOT modified; (E) `EVENT_ID` was NOT modified; (F) NO protected bootstrap-authority source was modified. Because the only parser-admissible Auditor-A identity is the spent A-01:

`CURRENT_PROTECTED_AUTHORITY_HAS_NO_REPRESENTABLE_REPLACEMENT_AUDITOR_A_IDENTITY = TRUE`

## 6. Authority / grant token semantics — static proof over the exact protected bytes

The exact protected `bootstrap-authority/bootstrap_authority/runtime.py` blob `069c221fc1f84f9e8e8342ffed72ec761b9286b5` (content SHA-256 `f90338087f214ce0b4af5659afff9b4001398c5896a4dc97ffeae6885225427a`, 1662 lines) was inspected DATA-ONLY (blob read plus `ast.parse`; the module was NEVER imported, `BootstrapAuthority` NEVER constructed, `run_attempt` NEVER called). Verified EXACT from the source bytes:

- line 13: "Primary launch authority is NON-EXPORTABLE AUTHORITY PROCESS STATE" — the architecture statement, first line of the module docstring's authority paragraph.
- lines 13-24: the whole irreversible attempt lifecycle — package/event identity verification, static byte identities, the custody-OBJECT identity gate, the three fresh dynamic gates in frozen order, durable GATES_PASSED, the authority-created report sink, credential custody strictly after the gates, durable CONSUMED_PRE_EXEC, the irreversible spend and the IMMEDIATE fork/exec — happens inside ONE public authority operation `BootstrapAuthority.run_attempt(...)`.
- lines 22-23: "no grant/consume/resume/retry/adopt_report/finish/mint_attempt/create_event surface exists, and no caller ever regains control between GATES_PASSED, CONSUMED_PRE_EXEC and the exec."
- AST census of the exact bytes: the complete public surface of `class BootstrapAuthority` (line 975) is exactly `{state, store, run_attempt}` (two read-only properties plus the single authority operation; every other member is underscore-private); NONE of the eight forbidden names exists as a method, attribute or module-level definition anywhere in the module (`forbidden_at_module_level` = empty). This matches the protected test suite's own static assertion (tests/test_runtime.py BA-31: `test_ba31_no_public_split_surface` asserts `not hasattr(bar.BootstrapAuthority, name)` for exactly `grant, consume, resume, retry, adopt_report, finish, mint_attempt, create_event`).
- lines 184-188: `accounting_name(binding)` returns exactly `binding.attempt_id` (AST-verified return of the `attempt_id` attribute of the parameter `binding`), with the docstring "Attempt-GLOBAL O_EXCL authority-claim name (BA-RB-001): ONE reserved attempt id = ONE global claim".

Therefore the primary launch authority is non-exportable process state with no token-shaped surface at all: `RUNTIME_AUTHORITY_SURFACE_VERDICT = NO_EXPORTABLE_GRANT_OR_TOKEN_SURFACE`.

## 7. Token-source decision

The active-v3 procedure requires future "authority tokens — all FUTURE values minted by the operator, never reused from history" (Section A), while historical authority state MUST NOT be reused (procedure line 208: "no historical authority token, event id, attempt id, executable path, grant state ... may be reused for any future launch"). An exhaustive static search (pattern `(?i)\btoken|grant|mint\b`, every hit classified verbatim, full listing preserved at the external workspace `evidence/static-search-results.txt`) was run across the authorized source set: bootstrap-authority/** (13 files at HEAD, 24 hits), bootstrap-supervisor/** (34 files at HEAD, 64 hits), the accepted active-v3 procedure (4 hits), the accepted active-v3 binding (4 hits), the accepted pkgprep canonical preparation record (13 hits) and the accepted pkgprep Control Room readback record (12 hits). Classification of every relevant candidate:

- `binding.authority_package` (manifest_sha256/package_sha256 digest pair) — PACKAGE_IDENTITY_DIGEST, not a token: carrying it proves byte identity only.
- `AUTHORITY_STATUS` / `AUTHORITY_QUALIFICATION_CLAIM` manifest strings — fixed STATUS_LABELs ("IMPLEMENTATION_CANDIDATE_ONLY / NO_EXECUTION_AUTHORITY", "NONE"), not minted authority values.
- `EVENT_ID` / `RESERVED_ATTEMPT_IDS` — DESIGN_RESERVED_IDENTITY constants; identities, not tokens; A-01 is spent.
- structural diagnostic "safe token" machinery (`STRUCTURAL_TOKEN_PREFIX` sanitization) — bounded ERROR_LABEL sanitization, nothing authority-shaped.
- PREARM operational correlation context — CORRELATION_VALUE; the accepted active-v3 binding namespaces it as "NOT an attempt id, NOT an event id, NOT an authority token, NOT a grant, NOT a credential identifier, NOT a reusable permit".
- OPERATOR_SEND_NOW — CHANNEL_OPERATOR_CUE, explicitly barred by the tasking.
- historical execution-authority identifiers / the spent A-01 execution grant — HISTORICAL_SPENT; reuse prohibited.
- AccountingStore record / accounting filename — RUNTIME_ACCOUNTING_STATE; creating one is out of scope (Section 8).
- the current task authority ID itself — TASKING_IDENTIFIER; no authoritative contract defines it as the required package authority token.
- Git commit/tree identities — SOURCE_IDENTITY provenance, not minted values.
- random UUID / free-form invented string — FABRICATION; prohibited.
- the active-v3 "authority tokens" FUTURE-requirement text and the pkgprep readback's "minimum missing authority" paragraph — REQUIREMENT_ONLY: the contract REQUIRES future operator-minted authority tokens but defines NO schema, NO minting mechanism and NO verification semantics; the accepted readback itself records that token semantics "must be bounded in that separately authorized task".

Zero hits define a field-shaped token (`"authority_token"` / `"grant_token"` / `"package_token"`: 0 occurrences). Therefore:

`CANONICAL_NON_EXECUTION_PACKAGE_AUTHORITY_TOKEN_SOURCE = NOT_ESTABLISHED`

No token was fabricated to fill the gap.

## 8. Accounting / runtime barrier

The exact protected `bootstrap-authority/bootstrap_authority/accounting.py` blob `26368783dd88782dd3c63a76fbf11582ee16caa1` (content SHA-256 `4ea6d871b175a5354448b650fbbbd03ff77f6e98940a343ccc95eca50382b2b4`, 239 lines) was inspected DATA-ONLY (blob read plus `ast.parse`; the module was NEVER imported; `AccountingStore.create` was NEVER called). Verified EXACT from the source bytes: `AccountingStore.create_at` (lines 88-122) creates the per-attempt record file with `os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW` (O_CREAT at line 104, O_EXCL at line 105; AST-confirmed the same os.open call carries O_CREAT, O_EXCL and O_APPEND), appends the initial state at line 121 with `first_state` defaulting to `PREPARED`, and `append` enforces `FIRST_RECORD_MUST_BE_PREPARED` (lines 139-140); `AccountingStore.create` (lines 123-131) opens the custody directory and wraps `create_at`. The module docstring (lines 6-14) holds: the accounting record is NOT launch authority and can NEVER reconstruct it; a writable store exists ONLY via `create`/`create_at` in the ONE authority process for an attempt. Therefore invoking `AccountingStore.create`/`create_at` IS runtime attempt/accounting-state creation (durable PREPARED state, attempt-global O_EXCL claim) and is OUT OF SCOPE for this authority. This session created NO accounting record, NO custody attempt file, NO attempt directory, NO report sink, NO attempt runtime namespace and NO durable PREPARED state.

## 9. Required feasibility verdicts (from the exact source evidence)

- `CURRENT_EVENT_ID_CAN_BE_REUSED_WITHOUT_SECOND_GOVERNANCE_EVENT = TRUE` — binding.py accepts exactly the held EVENT_ID (gate at line 415); the governance event is instantiated once in the frozen external event root and held as ONE event / NO_SECOND_EVENT by the canonical records; a future binding under the SAME EVENT_ID requires no second governance event.
- `SPENT_AUDITOR_A_01_CAN_BE_REUSED = FALSE` — canonical records hold ...-AUDITOR-A-01 as SPENT / SINGLE-USE / NO-RETRY.
- `NEW_REPLACEMENT_AUDITOR_A_IDENTITY_ACCEPTED_BY_CURRENT_PROTECTED_BINDING = FALSE` — the line-422 gate admits only the spent A-01 for AUDITOR_A.
- `NEW_REPLACEMENT_IDENTITY_REQUIRES_PROTECTED_AUTHORITY_SEMANTIC_CHANGE = TRUE` — representing a new identity requires changing `RESERVED_ATTEMPT_IDS` (line 73) or the parser gate (line 422), both protected bootstrap-authority source.
- `CANONICAL_NON_EXECUTION_PACKAGE_AUTHORITY_TOKEN_SOURCE_ESTABLISHED = FALSE` — Section 7.
- `RUNTIME_ACCOUNTING_REQUIRED_TO_CLAIM_EXECUTION_AUTHORITY = TRUE` — the whole lifecycle including the O_EXCL accounting claim keyed by `accounting_name(binding) == binding.attempt_id` happens inside `run_attempt`, and the authority is non-exportable process state; claiming execution authority necessarily creates runtime accounting state.
- `CAN_CURRENT_AUTHORITY_COMPLETE_VALID_REPLACEMENT_PACKAGE_WITHOUT_CROSSING_SCOPE = FALSE` — a valid replacement package requires BOTH a parser-representable NEW attempt identity (impossible without protected-source change) AND a canonical package authority/grant-token source (NOT_ESTABLISHED); completing one would cross into protected-source modification or token fabrication, so the STOP clause fires. This expected fail-closed result was NOT forced: it is what the exact source evidence independently shows.

## 10. Terminal stop

Because the protected parser cannot represent a new replacement attempt AND no canonical package-token source is established, this session STOPPED before creating ANY machine attempt identity or authority token, exactly as the tasking's Section 10 requires. Terminal disposition (token-for-token):

`MINIMUM_IDENTITY_AUTHORITY_BINDING_STOPPED_AT_PROTECTED_AUTHORITY_SEMANTICS_BOUNDARY / EXISTING_GOVERNANCE_EVENT_PRESERVED / SPENT_AUDITOR_A_01_NOT_REUSED / NO_REPLACEMENT_ATTEMPT_ID_CREATED / NO_REPLACEMENT_ATTEMPT_RESERVED / NO_REPLACEMENT_ATTEMPT_ALLOCATED / NO_AUTHORITY_TOKEN_FABRICATED / NO_ACCOUNTING_STATE_CREATED / NO_VALID_ATTEMPT_PACKAGE_COMPLETED / PROTECTED_BOOTSTRAP_AUTHORITY_UNCHANGED / SEPARATE_AUTHORITY_PROTOCOL_DESIGN_DECISION_REQUIRED / NO_EXECUTION_AUTHORITY / NO_REAL_RUNTIME / AUDITOR_B_AUTHORITY_NONE / AUDIT_VERDICT_NONE / QUALIFICATION_NONE / INSTALLATION_NONE`

This is a successful fail-closed outcome for THIS task. No replacement identity or token was invented merely because creation was authorized conditionally.

## 11. Control Room observations recorded

`AUCDEV023-CR-PCH6B-PKGIDENT-001` — `REPLACEMENT_AUDITOR_A_IDENTITY_NOT_REPRESENTABLE_BY_CURRENT_PROTECTED_BOOTSTRAP_AUTHORITY`. Classification: HARNESS / AUTHORITY-PROTOCOL LIMITATION. Support: OBSERVED SOURCE FACT (binding.py accepts only the design-reserved Auditor-A A-01 identity, which is already spent/single-use/no-retry — Section 4/5 evidence). Status: OPEN / BLOCKING_VALID_REPLACEMENT_PACKAGE_IDENTITY_BINDING / NOT_A_FROZEN_TARGET_PRODUCT_DEFECT.

`AUCDEV023-CR-PCH6B-PKGIDENT-002` — `ACTIVE_V3_AUTHORITY_TOKEN_REQUIREMENT_HAS_NO_ESTABLISHED_CANONICAL_NON_EXECUTION_TOKEN_SOURCE`. Classification: HARNESS / PROTOCOL-CONTRACT GAP. Support: OBSERVED ACTIVE-V3 REQUIREMENT + OBSERVED PROTECTED-RUNTIME AUTHORITY MODEL + NO CANONICAL TOKEN SOURCE FOUND IN AUTHORIZED SOURCE SET (Section 6/7 evidence). Status: OPEN / BLOCKING_VALID_REPLACEMENT_PACKAGE_AUTHORITY_BINDING / NOT_AN_EXECUTION_VERDICT / NOT_A_FROZEN_TARGET_PRODUCT_DEFECT.

Both findings are harness/protocol observations about the NEW authority plane; neither asserts anything about the frozen audit target.

## 12. Non-authority feasibility bundle

External NON-AUTHORITY workspace `/home/isa/aucdev023-pch6b-minimum-identity-authority-binding-20261005-01/` (NOT Git-tracked), every readiness artifact machine-asserted to carry all six banners `NON_AUTHORITY / NO_ATTEMPT_ID_CREATED / NO_AUTHORITY_TOKEN_CREATED / NO_EXECUTION_AUTHORITY / NOT_AN_ATTEMPT_PACKAGE / NOT_VALID_FOR_INVOCATION`:

- `readiness/PROTECTED-IDENTITY-SEMANTICS.json` — SHA-256 `3f74af533dd171ea02201f61c3480ec36a23d5f74c21b5ba87a17897a2e9f4a4`
- `readiness/TOKEN-SOURCE-ANALYSIS.json` — SHA-256 `bd9af3ccbecea2b3c1e9edfb11e3394e4a825143cf85660f027770cb0aa5274f`
- `readiness/ACCOUNTING-BOUNDARY.json` — SHA-256 `8dc1ff1989061203a9d980e9bcdb766f3bca5cd34f570f263558f473fa52da7e`
- `readiness/IDENTITY-AUTHORITY-FEASIBILITY-DECISION.json` — SHA-256 `fdfa539c22e64ec1a05e06fe907c136955c49dfcade2a741ee1b5042d5a56b65`
- `readiness/PACKAGE-COMPLETION-STOP.md` — SHA-256 `07430bbbd48fbdb62376435ccdf4ea12cb70d9f55f1029405806170423c84410`
- `data-only/` — byte-exact NON-AUTHORITY copies of the accepted REQUIRED-BINDINGS matrix (`128d4cf6...`), the accepted active-v3 procedure (`32460cd5...`) and the accepted active-v3 binding (`801279b5...`), each verified byte-identical to its preserved source.
- `evidence/` — bootstrap-verification.json (29/29 PASS), static-source-proof.json plus preserved defective first outputs, source-line-evidence.txt, static-search-results.txt, exact-source-identities.json, readiness-bundle-verification.json, zero-runtime-census.md, honest-iteration-ledger.md, drift-snapshot-base.txt.
- `instruments/` — the data-only python instruments (01 bootstrap, 02 static source proof, 03 readiness bundle; later: rotation builder, precommit battery, generated-LAST builder).

The bundle is evidence and readiness ONLY. It is NOT an attempt package, NOT a token source and NOT valid for any gate invocation.

## 13. Acceptance matrix IDB-01..35

| ID | Requirement | Result |
|---|---|---|
| IDB-01 | live base exact (master == origin/master == HEAD == `5c88c875...`, root `31e2c95a...`, sole parent `62b614f...`) | PASS |
| IDB-02 | pkgprep CRRB blob exact (`38d95663...`) and preparation record (`cb3b6a93...`) at HEAD | PASS |
| IDB-03 | protected bootstrap-authority tree exact (`15497587...`) at base and in staged write-tree | PASS |
| IDB-04 | binding.py blob exact (`1448c9cb...`) | PASS |
| IDB-05 | runtime.py blob exact (`069c221f...`) | PASS |
| IDB-06 | accounting.py blob exact (`26368783...`) | PASS |
| IDB-07 | EVENT_ID exact (`AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01`, binding.py line 72) | PASS |
| IDB-08 | reserved Auditor-A identity exact A-01 (binding.py line 75; single assignment) | PASS |
| IDB-09 | A-01 spent/no-retry status verified from canonical records (CRRB `38d95663...` + CURRENT status line) | PASS |
| IDB-10 | parser exact attempt equality requirement verified (binding.py lines 421-425) | PASS |
| IDB-11 | non-reserved identity rejection semantics verified (`ATTEMPT_ID_NOT_THE_RESERVED_IDENTITY_FOR_ROLE`, line 424) | PASS |
| IDB-12 | no replacement identity generated (UUID/random/hash/timestamp/TEST-ONLY/A-02 all zero) | PASS |
| IDB-13 | protected source unchanged (protected trees + blobs held EXACT in staged write-tree) | PASS |
| IDB-14 | runtime NON-EXPORTABLE authority model verified (runtime.py line 13) | PASS |
| IDB-15 | no mint_attempt surface verified (AST; BA-31 corroboration) | PASS |
| IDB-16 | no create_event surface verified (AST; BA-31 corroboration) | PASS |
| IDB-17 | no grant surface verified (AST: public surface exactly {state, store, run_attempt}) | PASS |
| IDB-18 | accounting global claim uses binding.attempt_id (runtime.py lines 184-188, AST return) | PASS |
| IDB-19 | AccountingStore.create durable-state semantics verified (O_CREAT|O_EXCL, PREPARED append) | PASS |
| IDB-20 | AccountingStore.create NOT called | PASS |
| IDB-21 | no accounting state created (record/custody file/attempt dir/report sink/PREPARED: 0) | PASS |
| IDB-22 | active-v3 authority-token requirement verified (Section A quote, matrix rows) | PASS |
| IDB-23 | token-source static search complete (6 sources, 121 raw hits, all classified) | PASS |
| IDB-24 | no free-form token fabricated | PASS |
| IDB-25 | existing governance event preserved | PASS |
| IDB-26 | no second governance event | PASS |
| IDB-27 | no valid package falsely claimed | PASS |
| IDB-28 | no execution authority | PASS |
| IDB-29 | no credential/channel/VM/QGA/run_attempt/model activity (census all-zero) | PASS |
| IDB-30 | PREARM-001 remains CLOSED (retained at exactly its accepted scope) | PASS |
| IDB-31 | ACTIVATION-001 remains CLOSED (retained) | PASS |
| IDB-32 | successor remains mode 0500 without permission transition (not touched this session) | PASS |
| IDB-33 | Auditor-B NONE | PASS |
| IDB-34 | qualification NONE | PASS |
| IDB-35 | installation NONE | PASS |

35/35 PASS.

## 14. Zero-runtime census

Full census at the external workspace `evidence/zero-runtime-census.md`. Headline: protected modules imported 0 (static `ast.parse` analysis only); BootstrapAuthority constructed 0; run_attempt 0; AccountingStore created/called 0; successor gate executions 0; permission transitions 0; chmod 0; credential access 0; channel connect/probe 0; send_once_v2 0; bridge-v2 0; OPERATOR_SEND_NOW 0; VM/virsh/QGA/guest-runner 0; Claude/Codex//audit-council/provider-model 0; Auditor-B 0; test executions 0; archive-member executions 0 (data-only tar-stream reads only, payload copies under /tmp OUTSIDE the repository, cleaned after); attempt-id creation/reservation/allocation 0; authority-token creation 0; valid package completion 0. The only executions this session: ordinary Git/GitHub publication mechanics and local data-only python text/hash/AST/tar tooling on non-secret bytes.

## 15. Honest session iteration without erasure

Instrument-side ONLY; every first output preserved under the external evidence workspace; NO failed observation rewritten as PASS without a corrected re-derivation on IDENTICAL bytes/state; NO subject byte was ever changed across any iteration:

- bootstrap instrument run-001-defective: an f-string interpolation bug (`NameError: name 'tree'`) crashed before any evidence was written; run-002-defective: the four protected-tree checks used a `HEAD:path^{tree}` resolution form that git echoes unresolved (an instrument resolution-form defect — the trees were independently verified EXACT by direct `git rev-parse HEAD:<path>`); run-003 FINAL 29/29 PASS.
- static-source-proof instrument run-001-defective: the `accounting_name` body check did not skip the docstring statement, and the O_CREAT/O_EXCL check assumed a single-line flag list (the exact source splits the flags across lines 104-105); run-002-defective: the run_attempt lifecycle docstring needle was broken by a source line wrap (fixed by whitespace-normalized docstring matching — lexical content and case exact); run-003 FINAL PASS on the IDENTICAL blob bytes. Both defective outputs preserved (`static-source-proof.run-001-defective.json`, `static-source-proof.run-002-defective.json`).
- exact-source-identities heredoc run-001-defective: bytes stdin passed to a text-mode subprocess (`AttributeError`) aborted before any file was written; re-run wrote the evidence with the /tmp extractions re-verified against the exact blobs.
- readiness bundle, token-source search, and data-only copies: FIRST-RUN PASS.
- rotation-builder: FIRST-RUN PASS — every zone assertion (CURRENT replace@3/11/23-24 + insert@tail x4; BACKLOG insert@3576 x1 + insert@tail x4; row/section counts; NEXT line-start count; base-region byte-identity; done-mark count) computed-before-write AND re-asserted from the written files; no aborted or defective builder run occurred and no pre-write abort was needed.
- precommit battery run-001-defective (61/64): three instrument-side strictness defects on IDENTICAL staged bytes — an over-strict closure needle (`INT-001/INT-002` where the record writes `INT-001 / INT-002`), an A-02 gate that flagged the tasking-mandated hypothetical-rejection mention instead of requiring its hypothetical/rejected attribution, and the hex allow-set missing the two verified short prefixes `5c88c875`/`62b614f` used in the IDB table; run-002 64/64 PASS FROM SCRATCH on the IDENTICAL staged bytes (both runs resolved the SAME staged write-tree, recorded in the battery evidence file; NO staged byte changed across any battery run); after this record-text ledger correction, the FINAL battery run was executed FROM SCRATCH on the FINAL staged bytes and ALL PASSED.

## 16. Held governance state (unchanged by this task)

AUCDEV-023 P1 / READY / NOT DONE. EVENT `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01` instantiated; PATH-B slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT. PREARM-001 MECHANICALLY_REMEDIATED / CONTROL_ROOM_ACCEPTED / OPERATIONALLY_ADOPTED / CLOSED (retained at exactly its accepted scope). ACTIVATION-001 MECHANICALLY_REMEDIATED / CONTROL_ROOM_ACCEPTED / CLOSED (retained). OPADOPT-PREP-001 / HANDOFF-001 / HANDOFF-002 / INT-001 / INT-002 CLOSED (retained). R1/R2/R3 unchanged. The successor remains the CONTROL_ROOM_ACCEPTED_ACTIVE_SUCCESSOR_GATE at MODE_0500 / OPERATIONALLY_ADOPTED_FOR_REUSABLE_FUTURE_AUDITOR_A_HOST_LAUNCH / NOT_ATTEMPT_AUTHORITY with NO permission transition (its identity remains hash-bound by the accepted transition-02 records; the gate object was NOT touched this session). The existing Auditor-A machine attempt ...-AUDITOR-A-01 remains SPENT / SINGLE-USE / NO-RETRY and was NOT reused. NO replacement Auditor-A attempt exists, is reserved, is allocated or is minted. Auditor-B authority NONE. FIRST_PASS_A ABSENT. Audit verdict NONE. Qualification NONE. Installation NONE. MODEL_ENGAGEMENTS_USED remains 0. Installed source `8ae33444f349ce73c1359b963722e2d16acba630` with installed-qualified provenance NOT ESTABLISHED (governance-recorded identity, retained). The five CRED/CREDCH closures remain at exactly their LIMITED strengths. Frozen external event root untouched append-only. Historical records/handoffs NOT rewritten. Prior closures RETAINED.

## 17. Publication safety and geometry

Staged EXACTLY the three authorized documentation paths (NEW canonical record; M CURRENT rotated with the rotation confined EXACTLY to lines 3/11/23-24 plus one NEW dated tail record; M BACKLOG rotated with EXACTLY two pure insert LINE zones — one NEW dated status bullet immediately after the pkgprep-readback status bullet and one NEW dated tail record). Both zone sets were computed-before-write by the assertion-guarded builder AND re-asserted from the STAGED blobs by the precommit battery. Protected trees, protected source blobs and the frozen target held EXACT in the staged write-tree; therefore ZERO source modification staged and ZERO performed. Staged == working on all three paths; `git diff --check` and staged `git diff --cached --check` PASS. The mandated historical records verified unchanged in the staged write-tree. No source/helper/test/archive file, no channel helper, no send_once_v2 bytes, no domain XML, no VM image, no credential/auth/session material, no .jsonl, no event-package tracked path and no event-root file committed. The feasibility workspace, instruments, data-only copies and all evidence remain EXTERNAL, hash-bound by this record. Repository drift preserved unstaged. The disposition block is token-for-token exact; PREARM-001 / ACTIVATION-001 / OPADOPT-PREP-001 / HANDOFF-001/002 / INT-001/002 closures appear on added lines only as RETAINED prior statuses (attribution-checked); no attempt id, no authority token, no valid attempt-specific package and no Auditor-B authority anywhere in staged content; credential/secret mechanical scan clean; invisible-character scan clean; hex-literal gate PASS with every >=7-char boundary-delimited non-decimal hex literal in the NEW record and added lines machine-verified case-insensitively against the session-derived independently-verified identity allow-set. The FULL record-only precommit gate battery ran from scratch on the FINAL staged bytes and ALL PASSED.

## 18. NEXT — exactly one, grants nothing

OPERATOR DECISION ON WHETHER TO AUTHORIZE A BOUNDED ZERO-MODEL AUTHORITY-PROTOCOL DESIGN FOR ONE REPLACEMENT AUDITOR-A ATTEMPT WITHIN THE EXISTING AUCDEV-023 GOVERNANCE EVENT, DEFINING — WITHOUT IMPLEMENTATION OR EXECUTION — (A) HOW A NEW SINGLE-USE REPLACEMENT AUDITOR-A MACHINE ATTEMPT IDENTITY IS REPRESENTED BY THE PROTECTED BOOTSTRAP-AUTHORITY CONTRACT WITHOUT REUSING THE SPENT A-01 IDENTITY, AND (B) THE CANONICAL NON-EXECUTION PACKAGE AUTHORITY/GRANT-TOKEN SEMANTICS REQUIRED BY ACTIVE-V3; THE DESIGN MUST PRESERVE THE ONE-EVENT GOVERNANCE BOUNDARY, ONE-SHOT/NO-RETRY SEMANTICS, FROZEN TARGET, PROTECTED AUTHORITY SEPARATION AND THE DISTINCTION BETWEEN PACKAGE BINDING AUTHORITY AND EXECUTION AUTHORITY. NO PROTECTED-SOURCE CHANGE, ATTEMPT CREATION, ACCOUNTING STATE, PACKAGE COMPLETION, CREDENTIAL ACCESS, CHANNEL/VM/QGA/run_attempt/MODEL EXECUTION OR AUDITOR-B AUTHORITY IS AUTHORIZED BY THAT DECISION UNLESS SEPARATELY AND EXPLICITLY GRANTED AFTER DESIGN READBACK.

Recording this NEXT grants NOTHING. No attempt authority follows automatically; Auditor-B authority remains NONE; no replacement Auditor-A attempt exists or is authorized; any attempt-identity creation, attempt-specific package completion, channel re-probe, protocol change, teardown or real-credential use requires a NEW explicit operator decision.

## 19. Standing prohibitions (house, retained)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from an agent session absent an explicit single-use operator attempt authority (and even then at most the ONE authorized call, never a second); never rerun the launcher; never treat any recorded grant phrase (including any phrase recorded here) as a new grant; never execute a real auditor or provider/model; never open, read, hash, log, persist or stat any real credential byte; never open the four historical sealed artifacts (identity-only forever); never relabel or rewrite historical model identities, runs, records, matrices, prompts or evidence workspaces (append-only); never claim audit PASS, qualification, installation or any authority from this publication — it grants none; never rewrite, repack, replace or delete a historical subject archive and never publish a corrected archive under a historical archive's filename; never repack any historical generated-LAST handoff archive; never edit the accepted v2 remediation source or the accepted PREARM/sender bytes; never chmod the now-mode-0500 activated authoritative object (or the historical 0600 candidate) absent separate operator authority after independent Control Room readback — both single-use activation transitions have been SPENT and performed, and NO further permission transition (including any de-activation or re-transition) is authorized by this publication; never use root to defeat the activated-state DAC boundary; never use a TEST-ONLY context for any future real launch; never mutate the canonical runtime root or restage the event host after event instantiation absent a separate explicit operator remediation authority; never rewrite or repack the frozen external event root; never delete or repurpose the rehearsal-derived artifacts under /srv/frevp/; never start or reopen the event-host VM or connect to the candidate credential channel from a preparation or record-only session; and never run privileged mount/pivot_root/umount experiments on the operator's live host and never automatically re-run an interrupted privileged command — privileged GATE-W-prime boundary work belongs in the disposable-KVM environment.
