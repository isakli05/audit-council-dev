# AUCDEV-023 — S1 RB-001 L1 RB-003 EXEC-RA-002 / PCH-002 — Replacement Operator-Launcher Rebind / Adaptation Design

Design authority: `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-REPLACEMENT-OPERATOR-LAUNCHER-REBIND-ADAPTATION-DESIGN-20260927-01`

Disposition: `PCH2_REPLACEMENT_OPERATOR_LAUNCHER_REBIND_ADAPTATION_DESIGN = READY_FOR_CONTROL_ROOM_READBACK / CURRENT_PREDECESSOR_GEOMETRY_MECHANICALLY_ESTABLISHED / CONSUMED_PCH1_LAUNCHER_USED_AS_HISTORICAL_STRUCTURAL_INPUT_ONLY / FRESH_PCH2_EVENT_AND_PACKAGE_IDENTITIES_BOUND_AT_DESIGN_STRENGTH / MINIMUM_PREDECESSOR_STATE_VERIFIER_DELTA_DEFINED / DELTA_CONFINED_TO_PHASE0_OPERATOR_HOST_CHECK / SEMANTIC_DELTA_CARDINALITY_ONE_FUNCTION / IDENTITY_DATA_REBIND_SURFACE_DEFINED / SINGLE_HUMAN_DIRECT_INVOCATION_PRESERVED / DEPLOYMENT_INSIDE_INVOCATION_PRESERVED / FAIL_CLOSED_NO_RETRY_NO_RESUME_PRESERVED / FUTURE_EXACT_EBS_FULL_PACKAGE_BYTE_GATE_CARRIED / FRESH_FUTURE_AUTHORITY_IDENTITY_RESERVED_ONLY / FUTURE_IMPLEMENTATION_BOUNDED / SEALED_REPORT_SUBSTANCE_UNREAD / ZERO_RUNTIME / NO_IMPLEMENTATION / NO_GRANT / NO_EXECUTION_AUTHORITY / NO_QUALIFICATION / NO_INSTALLATION`

This session was a BOUNDED OPERATOR-LAUNCHER REBIND/ADAPTATION DESIGNER and READ-ONLY EVIDENCE COLLECTOR — NOT the Control Room decision-maker, NOT a launcher implementation executor, NOT a deployment authority, NOT a prelaunch activator, NOT an execution controller, NOT an execution-authority grantor, NOT Auditor-A/B, NOT a credential-content reader, NOT a provider/model execution authority, NOT a qualification authority, NOT an installation authority. DESIGN ONLY.

---

## Section 0 — Role, boundary and zero-runtime attestation

- ZERO runtime this session: NO driver or wrapper created, patched, chmod'ed, imported, sourced or executed; NO deployment; NO staging/backup directories created; NO runtime attempts created; NO AccountingStore mutation; NO credential file opened (zero credential access, not even metadata — none was needed); BOTH sealed first-pass artifacts (Auditor-A frozen report `dbc47587…`, Auditor-B invalid snapshot `5a7d105b…`) verified by PATH / lstat / SHA-256 / SIZE / MODE / bounded census ONLY — never opened, decoded, printed, quoted or fed to any parser; NO auditor/provider/model execution; NO execution authority created or granted; NO qualification; NO installation.
- Permitted local operations: read-only hashing/stat/census, `ast.parse` static analysis of the consumed PCH1 driver (never executed/imported — R-PIMP-CR-1 honored), text reads, git bootstrap/publication tooling, archive read-only verification of the input handoff.
- Network: the mandated bootstrap `git ls-remote`, the fetch at the exact base, the pre-staging live re-resolve, the single `git push` of this publication, and the post-push readback ONLY.

## Section 1 — Exact live bootstrap (DES2-01, DES2-03)

| Item | Value |
|---|---|
| Live GitHub master at bootstrap (`git ls-remote origin refs/heads/master`) | `8fdc86c988ff592e0750e3538b0b7b981eaed1ed` |
| Local HEAD == FETCH_HEAD == live master | EXACT (`8fdc86c…`) |
| Root tree at base | `1c0bb069ab67bd505508948f532eeefb6bc944ef` EXACT |
| Sole parent | `82b74ec0840deb5f96fbadaf602993eb93313e1c` EXACT |
| PCH2 package-preparation CR readback blob | `46b74061944e9bec63f834a2e3cff9544f6e977c` EXACT |
| CURRENT-STATE blob | `0e17729a19c2491253ea014c1c07368c6f8678ea` EXACT |
| BACKLOG blob | `8eeb374bbca2cdafb5f3b341e782ed9d38aa919c` EXACT |
| PCH2 package preparation blob | `eb0d119989d92063154ef31db078d355fb8e7d02` EXACT |
| EXEC-RA-002 diagnostic blob | `d84943fdcf9d45617c34a43626f995c177dc6a3b` EXACT |
| PCH1 launcher design blob | `8218a320c81a804f2fae6df72c3b4b4e32bd5838` (path `…-EXEC-RA001-PCH1-REPLACEMENT-OPERATOR-LAUNCHER-REBIND-ADAPTATION-DESIGN.md`) EXACT |
| PCH1 launcher implementation CR readback blob | `9dd9cf9c674cf301af5ee3aa070d138bf9a73702` (path `…-PCH1-REPLACEMENT-OPERATOR-LAUNCHER-IMPLEMENTATION-CONTROL-ROOM-READBACK.md`) EXACT |
| Protected trees at base | `bootstrap-supervisor 732b8def9f22d7c466ce77f3d3049da53bfff3d0` + `qualification-harness 5b8d5e5465923740470ff63ed9b8683f257a3787` + `skill c792933a862d9a5434681a88d183470dd8b15d2f` ALL EXACT |
| Five immutable governance pins at base | `9f7599fe…` / `578b58c8…` / `83951286…` / `7ba8910e…` / `776a039a…` ALL EXACT |
| Lineage | trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor; merges since anchor 0; changed paths since anchor all under `docs/chatgpt-project/` (0 offending) |

## Section 2 — Input PCH2 Control-Room readback handoff identity (DES2-02)

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-COMPACT-FRESH-REPLACEMENT-PACKAGE-PREPARATION-CONTROL-ROOM-READBACK-HANDOFF.tar.gz`

- Outer SHA-256 `25f78da026f9217834af609b257a86483ebeb5dcdc35d1e80869894fb3efae5e` / 816195 B / regular `isa:isa` 0644 — EXACT.
- Census EXACTLY 28 members = 28 regular (27 payload + exactly 1 `SHA256SUMS`) + 0 directories + 0 symlinks/hardlinks/special + 0 unsafe/traversal/duplicate paths; `SHA256SUMS` 27 rows 27/27 PASS (re-hashed read-only under `LC_ALL=C`); 0 missing; 0 unlisted; member set == SUMS row set.
- Canonical copies Git-blob EQUAL to the live Git blobs at `8fdc86c`: readback `46b74061…` / CURRENT `0e17729a…` / BACKLOG `8eeb374b…`.
- ZERO archive members executed.

## Section 3 — Consumed PCH1 launcher — historical/structural input only (DES2-04)

| Artifact | Path | SHA-256 | Size | Lines | Owner | Mode |
|---|---|---|---|---|---|---|
| Driver | `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.py` | `7a8389a30c9849d0efffd6f6e32b2e9760921eb3a296bfceb4707d660771829b` | 166778 | 3352 | isa:isa | 0700 |
| Wrapper | `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch1-5cb2c58f-impl01.sh` | `5423ec76ac562844d7fde243aba982dbf96a02e61a6dfbe427c3d311d8120d77` | 3468 | 82 | isa:isa | 0700 |

Belonging to CONSUMED authority `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` (CONSUMED / TERMINAL / CLOSED / NO_RERUN; engagements 2/2). Used ONLY by read-only byte inspection and non-executing `ast.parse`/static text extraction. NEVER executed/imported/sourced/chmod'ed/patched. Authority does NOT transfer.

## Section 4 — Current deployed predecessor geometry (DES2-05..DES2-10)

Deploy root `/home/isa/aucdev023-s1-prep002-rem002`; current event `evt-5cb2c58f855415c3`; no staging directory present; attempt census 27 = 24 historical + `evt-4a51f4b9413a1476-A-01` + `evt-5cb2c58f855415c3-A-01` + `evt-5cb2c58f855415c3-B-01`; SEVEN historical backup generations present and untouchable.

Deployed generation identity (re-hashed read-only EXACT):

| Item | Value |
|---|---|
| A binding | `7130cfc88ed6fdea1347c815e1b958c384eabda3534d33437243122e26f578e2` |
| B binding | `68d622b291efcee25cea698165283561f94676481a3aec2e2532a8a48c7d70ab` |
| A MANIFEST | `5d5eb70a9f938db19a12e2dec00af4c6fd97f10bb9eb4e40063eea8bc0609435` |
| B MANIFEST | `b5874d90dc9b101cd93763b0cb5b0badbed5e8e90381f01de0673e3838ef24fb` |
| Relations | A: `evt-5cb2c58f855415c3-A-01`/AUDITOR_A; B: `evt-5cb2c58f855415c3-B-01`/AUDITOR_B EXACT |

Auditor-A — PRESENT / REPORT_FROZEN / TERMINAL (DES2-06, DES2-07):

- Accounting `attempts/evt-5cb2c58f855415c3-A-01/accounting/evt-5cb2c58f855415c3-A-01.jsonl` — SHA-256 `a95eb7b011dff4d5bf06ffcc36ad63ff683096990095952a8c17525621a70023` / 5616 B / 0600 / regular EXACT.
- State sequence EXACT: `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_FROZEN → TERMINAL`.
- Report-suffixed census under the A attempt root EXACTLY `custody-out/evt-5cb2c58f855415c3-A-01.first-pass-report.json` (no second report artifact).
- Frozen report identity ONLY: SHA-256 `dbc47587f866412cd09e129d6b3da42673e1965a0a511997154bb568f680b621` / 28465 B / mode 0444 / regular non-symlink — SEALED / UNREAD / UNADJUDICATED.

Auditor-B — PRESENT / REPORT_INVALID / TERMINAL (DES2-08, DES2-09):

- Accounting `attempts/evt-5cb2c58f855415c3-B-01/accounting/evt-5cb2c58f855415c3-B-01.jsonl` — SHA-256 `c1be982079b178aac68dfba05997d67370491f8446c7f861cf026ffde5b68c87` / 5662 B / 0600 / regular EXACT.
- State sequence EXACT: `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_INVALID → TERMINAL`.
- Custody-out: EMPTY (present as an empty directory — no frozen report).
- Report-suffixed census under the B attempt root EXACTLY `staging/evt-5cb2c58f855415c3-B-01.first-pass-report.json`.
- Invalid staging snapshot identity ONLY: SHA-256 `5a7d105b3cb8c9c9da3e9858b31d760584fe8ded2c3351fc4d82da5374f256c0` / 117 B / mode 0600 / regular — SEALED / UNREAD / UNADJUDICATED; recorded safe structural token `REPORT_KEYS_INVALID` is carried as GOVERNANCE EVIDENCE ONLY — the future predecessor verifier does NOT parse the snapshot or re-diagnose the token.

Blindness (DES2-10): both artifacts were only stat'ed/hashed/censused; no report byte entered this session's model context, terminal output, Git, evidence files or the generated archive.

## Section 5 — Fresh PCH2 event / package contract bound at design strength (DES2-11, DES2-12)

Fresh event `evt-aa640691cfe9d33c` (selection SHA-256 `aa640691cfe9d33c867e1cc9c5b9e050eb8bbfddf8ae445935477ef157a325e5` / 689 B re-hashed EXACT; derivation `evt-` + first 16 lowercase hex reproduced). Fresh attempts `evt-aa640691cfe9d33c-A-01` / `evt-aa640691cfe9d33c-B-01`.

Canonical source root (the ONLY permitted future deployment source): `/home/isa/aucdev023-s1-rb001-l1-rb003-exec-ra002-pch2-compact-fresh-replacement-package-prep-20260927-02/event` — resolved from the accepted preparation record `eb0d1199…` and re-verified on the host.

| Identity | Auditor-A | Auditor-B |
|---|---|---|
| binding file | `075b2de246065c4828fedc588256686750f15b04579444ac60f973e287411f16` | `19ba43f5869ee5a57e1191a9699fa012f48cb75724d76a9b476c40d7b0443fc1` |
| canonical binding digest | `439ee7fb5a76376f9572c8a38364c7cba288afb4ef23d18844ded68d1023fdb2` | `b38c1a5105bb2ac8789fb536ac5d3ff39a440956aeb3e01b3e9038fd697550a6` |
| MANIFEST | `45adb9800ff3ef93e71d09e08629a44df324c362e562cd93118575c329b853bd` | `9b18bcb046ba8bdbef49ac4083b6aaf401f2fb65d1952e6339ce9aa051f63b4c` |
| package | `0637a86e14916d750b8c0cd7ce553c7594deaa30a17ea45b8719dcffe7a4caaf` | `796457a2db3a8e33549ed4347daf7ff7d7de73c303917cbfe5d7bea7c9191aa3` |
| rows | 191 (unique 191) | 194 (unique 194) |
| payload bytes | 236323090 | 343454621 |

Shared plane (identical in BOTH fresh bindings and BOTH fresh packages; UNCHANGED from the accepted PCH1 generation): prompt contract `fe5243f4730827b21b1a5ec1b318813a7e681006350131397b99081334cf47a1` (event-id-only regeneration of `7679ac2d…`, report-requirements byte-equal); frozen validator `6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071`; frozen target `d4d584ffa47ad2848268ba947247f81a845b2322`; EBS MANIFEST `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999` / package `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93e922f8`; boundary launcher `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa`; network-readiness `20f37e9191d3e1e025962723328c5f8a2849f664cf1bf215715ccf8da9fc7235`; resource gate `27948980653f4c0639041243d9f117087f0987c5cc53623abbfa39cbb143adaf`; tool-domain-wrapper `0ed2ba48…`; probe-true `d3321fd6…`; auditor executables `15e2d051…` (claude 2.1.274, A) and `3188814c…` (codex 0.154.0, B).

Fresh B invocation (from the fresh binding, verified read-only): argc EXACTLY 8 — `codex exec --skip-git-repo-check --profile aucdev023-c3 --output-last-message /auditor-output/evt-aa640691cfe9d33c-B-01.first-pass-report.json <compact 939-byte prompt, final positional>`; every `auditor_invocation` item within the frozen 1024-byte EBS argv bound (max item 939).

Collision-clean (DES2-12): ZERO occurrences of `evt-aa640691cfe9d33c` anywhere under the deployed launcher root; fresh A/B attempt roots ABSENT under the deploy root. The preparation workspace `attempts/` contains ONLY the four accepted zero-provider rehearsal directories (`…-B-01`, `…-B-PCH2CTRL`, `…-B-SW2`, `…-B-SW3` — mock-session artifacts of the accepted single-writer rehearsal); these are FROZEN PREPARATION EVIDENCE outside the deployed launcher namespace: the future launcher's fresh-namespace gates bind the DEPLOYED root namespace and must NOT delete, normalize or reuse those preparation artifacts.

## Section 6 — Static containment proof on the consumed PCH1 driver (DES2-13, DES2-14, DES2-15)

Method: `ast.parse` over the exact driver bytes (`7a8389a3…`, 166778 B, 3352 lines) — no exec/compile-to-codeobject/import/eval of candidate code (R-PIMP-CR-1 honored); per-function census of global-constant Name-loads and identity-bearing string literals.

6.1 Top-level census: 52 functions, 1 class (`DriverStop`), 76 top-level assigns.

6.2 Predecessor-pin confinement: the module constants `HISTORICAL_EXEC05_A_ACCOUNTING_SHA` / `_ACCOUNTING_SIZE` / `_STATES` / `_REPORT_SHA` / `_REPORT_SIZE` / `_REPORT_MODE` (whose VALUES are the evt-4a51f4b9413a1476 predecessor pins) are referenced by EXACTLY ONE top-level function: `phase0_operator_host_check` (lines 1200–1501; §14 block lines ~1311–1446). AST Name-load census across all 52 functions: zero other referents.

6.3 Old-event-id confinement: the literal `evt-4a51f4b9413a1476` occurs at exactly 10 source locations: module docstring/comments (labels), the `EXPECT_OLD["event"]` DATA value (line 319), §14 comments (labels) and the `build_handoff` title label (line 3106). No control-flow branch anywhere depends on an event identity literal.

6.4 Classification is table-driven (DES2-15): `classify_destination(ctx, root)` iterates `((ctx["expect_old"], "EXPECTED_HISTORICAL"), (ctx["expect_new"], "ALREADY_NEW"))` and calls `verify_generation` — returning `EXPECTED_HISTORICAL` / `ALREADY_NEW` / `UNKNOWN(_ABSENT)` with ZERO event-specific branching. `deploy_generation` re-classifies immediately before the rename layer with the same tables; `ALREADY_NEW` is a STOP-and-return-to-Control-Room refusal (never resume authority); `UNKNOWN` refuses. `phase1_verify_source` and `phase3_reverify_deployed` verify through `verify_generation(…, ctx["expect_new"], …)`.

6.5 Package verification is table-driven: `verify_role_generation(event_root, role, expect, ebs, …)` takes every identity from the `expect` table — binding-file SHA, strict `parse_binding`, canonical digest, role/event/attempt relations, frozen target commit, `verify_event_package` (manifest SHA, non-circular package SHA, EVERY row size/SHA, exact row↔file equality, transport projection), row count, payload byte total, binding-pinned pair equality, launcher bytes + pin, resource-gate bytes + pin + LIVE ROOT comparison (`extract_root_assignment` — note: the driver's ROOT check IS a live comparison; the R-PGPL-CR-1 constant-True finding applies to the historical grant/prelaunch verifier script, not to this driver), auditor executable bytes + pin.

6.6 Runtime functions (`prepare_attempt`, `execute_one_shot_attempt`, `run_attempt_for_role`, `evaluate_conformance`, `report_custody_inventory`, `phase6_mechanical_check`, `build_handoff`) reference ONLY data constants (`ATTEMPT`, `EVENT_ID`, `AUTHORITY_ID`, pinned SHAs) — identity rebind suffices.

6.7 Conclusion: EVERY predecessor-specific behavior is confined to `phase0_operator_host_check`; deployment/classification/package verification/runtime are data-driven by `EXPECT_OLD`/`EXPECT_NEW` and pinned identity tables. CONTAINMENT PROVEN.

## Section 7 — Structural precedent (secondary, no transfer)

The old pre-PCH1 OLA001R1 launcher (`aucdev023-firstpass-rb001-l1-rb003-4a51f4b9-ola001r1.py` SHA-256 `1863c3439253ec66470c558fa64720250bda166c4bf25f72241be5a603d14420`, wrapper `ac258cb362cded97d0a952b5969db3b2cb62b4ef0d3d4f8a42b1a6905fc98c1e`) historically verified exactly an A=REPORT_FROZEN (custody-out, mode 0o444) / B=REPORT_INVALID (staging snapshot) predecessor geometry. Its §14 block establishes, as accepted structural precedent, the both-present per-role verifier shape (per-role accounting sha/size/states pins with `HISTORICAL_PREDECESSOR_{role}_STATE_MUTATED_REFUSED`; A custody-out identity with `…_A_REPORT_IDENTITY_REFUSED`; B census == exactly the staging snapshot with identity pins and `…_B_REPORT_IDENTITY_REFUSED`). The PCH2 §14 delta below is structurally isomorphic to that accepted verifier. NO OLA001R1 identity, authority, pin or byte transfers; any code reuse claim rests on this static comparison only; the old artifacts remain untouched (NOT_ADMITTED lineage).

## Section 8 — Minimum phase0 predecessor-state verifier delta (DES2-16, DES2-17)

AUTHORIZED_PCH2_PREDECESSOR_STATE_VERIFIER_DELTA — confined to `phase0_operator_host_check`; cardinality EXACTLY ONE FUNCTION. The §14 block's pin constants and predicates change as follows (all other logic of the function — root refusal, umask/core/xtrace discipline, invocation-evidence context BEFORE failable Git admission, repository admission, live EBS identity, source-root presence, backup gates, destination classification, same-filesystem rename-layer check, fresh-attempt absence gates, non-overwriting handoff gate, preflight evidence — is UNCHANGED apart from the data rebinds of Section 9):

Pin constants (data, consumed only inside this function):

| Pin | Old PCH1 value (evt-4a51f4b9413a1476) | New PCH2 value (evt-5cb2c58f855415c3) |
|---|---|---|
| A accounting SHA / size | `816658e8…` / 5677 | `a95eb7b011dff4d5bf06ffcc36ad63ff683096990095952a8c17525621a70023` / 5616 |
| A states | …EXEC_ATTEMPTED, REPORT_INVALID, TERMINAL | PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, REPORT_FROZEN, TERMINAL |
| A report SHA / size / mode / location | `4af00532…` / 28361 / `0o600` / `staging/` | `dbc47587f866412cd09e129d6b3da42673e1965a0a511997154bb568f680b621` / 28465 / `0o444` / **`custody-out/`** |
| B accounting SHA / size | (none — B pinned NOT_RUN-absent) | `c1be982079b178aac68dfba05997d67370491f8446c7f861cf026ffde5b68c87` / 5662 |
| B states | (none) | PREPARED, GATES_PASSED, CONSUMED_PRE_EXEC, EXEC_ATTEMPTED, REPORT_INVALID, TERMINAL |
| B snapshot SHA / size / mode / location | (none) | `5a7d105b3cb8c9c9da3e9858b31d760584fe8ded2c3351fc4d82da5374f256c0` / 117 / `0o600` / `staging/` |

Independent fail-closed predicates (distinct refusal tokens), identity-only — substance NEVER parsed:

AUDITOR-A — PRESENT / REPORT_FROZEN / TERMINAL
- A-1 attempt root + accounting path PRESENT → else `HISTORICAL_PREDECESSOR_A_ACCOUNTING_ABSENT_REFUSED`.
- A-2 accounting SHA-256 + size EXACT → else `HISTORICAL_PREDECESSOR_A_STATE_MUTATED_REFUSED`.
- A-3 state sequence EXACT (…REPORT_FROZEN…TERMINAL) → else `HISTORICAL_PREDECESSOR_A_STATE_MUTATED_REFUSED`.
- A-4 report-suffixed census under the A attempt root EXACTLY `[custody-out/evt-5cb2c58f855415c3-A-01.first-pass-report.json]` → else `HISTORICAL_PREDECESSOR_A_REPORT_CENSUS_REFUSED`.
- A-5 frozen report identity EXACT: SHA `dbc47587…` / 28465 / mode `0o444` / regular non-symlink → else `HISTORICAL_PREDECESSOR_A_REPORT_IDENTITY_REFUSED`.

AUDITOR-B — PRESENT / REPORT_INVALID / TERMINAL
- B-1 attempt root + accounting path PRESENT → else `HISTORICAL_PREDECESSOR_B_ACCOUNTING_ABSENT_REFUSED`.
- B-2 accounting SHA-256 + size EXACT → else `HISTORICAL_PREDECESSOR_B_STATE_MUTATED_REFUSED`.
- B-3 state sequence EXACT (…REPORT_INVALID…TERMINAL) → else `HISTORICAL_PREDECESSOR_B_STATE_MUTATED_REFUSED`.
- B-4 custody-out contains NO frozen report (empty) → else `HISTORICAL_PREDECESSOR_B_CUSTODY_NOT_EMPTY_REFUSED`.
- B-5 report-suffixed census under the B attempt root EXACTLY `[staging/evt-5cb2c58f855415c3-B-01.first-pass-report.json]` → else `HISTORICAL_PREDECESSOR_B_REPORT_CENSUS_REFUSED`.
- B-6 invalid staging snapshot identity EXACT: SHA `5a7d105b…` / 117 / mode `0o600` / regular non-symlink → else `HISTORICAL_PREDECESSOR_B_REPORT_IDENTITY_REFUSED`.

The old B-absence (NOT_RUN) predicates are RETIRED (their refusal classes disappear with the geometry they guarded). The verifier does NOT parse report substance and does NOT re-diagnose `REPORT_KEYS_INVALID`.

## Section 9 — Identity / data rebind table (complete old→new)

Every changed future driver/wrapper value. Classes: `IDENTITY_OR_DATA_REBIND` (R), `LABEL_OR_PROVENANCE_ONLY` (L), `AUTHORIZED_PCH2_PREDECESSOR_STATE_VERIFIER_DELTA` (V). Control-flow effect: NO for every R and L row; the V rows change which predicates execute inside the ONE function (authorized).

| # | Location (PCH1 driver `7a8389a3…`) | Old value | New value | Class | Justification |
|---|---|---|---|---|---|
| 1 | `AUTHORITY_ID` (line 129) | `…-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` | `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-REPLACEMENT-FIRSTPASS-EXEC-20260927-01` (RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE) | R | new one-shot authority identity; consumed PCH1 authority terminal |
| 2 | `EVENT_ID` (130) | `evt-5cb2c58f855415c3` | `evt-aa640691cfe9d33c` | R | fresh accepted event |
| 3 | `ATTEMPT` (131–134) | `…-5cb2c58f855415c3-A/B-01` | `…-aa640691cfe9d33c-A/B-01` | R | fresh attempts |
| 4 | `SOURCE_EVENT_ROOT` (191–194) | `…-exec-ra001-pch1-fresh-replacement-package-prep-20260925-01/event` | `…-exec-ra002-pch2-compact-fresh-replacement-package-prep-20260927-02/event` | R | only permitted source = accepted PCH2 preparation workspace (0555 runtime modes there; reviewer archives are never deployment sources) |
| 5 | `DRIVER_PATH`/`WRAPPER_PATH` (200–201) | `…-pch1-5cb2c58f-impl01.py/.sh` | `…-pch2-aa640691-impl01.py/.sh` (NEW artifacts) | R | future candidate names, collision-clean |
| 6 | `EVIDENCE_BASE` (202) | `pch1-5cb2c58f-impl01-run-evidence` | `pch2-aa640691-impl01-run-evidence` | R | fresh run-evidence namespace, collision-clean |
| 7 | `HANDOFF_PATH` (204–206) | `…-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01-MECHANICAL-HANDOFF.tar.gz` | `…-PCH2-REPLACEMENT-FIRSTPASS-EXEC-20260927-01-MECHANICAL-HANDOFF.tar.gz` | R | fresh authority-bound handoff, collision-clean |
| 8 | `STAGING_DIRNAME` (207) | `event.staging.rb001-l1-rb003-5cb2c58f-pch1` | `event.staging.rb001-l1-rb003-aa640691-pch2` | R | deterministic fresh staging, proven ABSENT |
| 9 | `BACKUP_DIRNAME` (208) | `event.backup.pre-pch1-replacement-event` | `event.backup.pre-pch2-replacement-event` | R | deterministic fresh backup, proven ABSENT, non-overwriting |
| 10 | `HISTORICAL_BACKUP_DIRNAMES` (209–216) | 6 entries | ALL SEVEN live generations: `pre-successor-event`, `pre-exec03-new-event`, `pre-exec02`, `pre-rb001-l1-successor-event`, `pre-rb002-successor-event`, `pre-rb003-corrected-successor-event`, **`pre-pch1-replacement-event`** (resolved from live host census 2026-09-27) | R | PCH1's own deployment created the seventh; none omitted |
| 11 | `PROMPT_CONTRACT_SHA` (225) | `7679ac2d…` | `fe5243f4730827b21b1a5ec1b318813a7e681006350131397b99081334cf47a1` | R | fresh contract (event-id-only regeneration; report-requirements byte-equal) |
| 12 | `EXPECT_NEW` (258–296) | PCH1 evt-5cb2c58f855415c3 identities | A: binding `075b2de2…`/canonical `439ee7fb…`/manifest `45adb980…`/package `0637a86e…`/191 rows/236323090 B; B: binding `19ba43f5…`/canonical `b38c1a51…`/manifest `9b18bcb0…`/package `796457a2…`/194 rows/343454621 B; `event` `evt-aa640691cfe9d33c`; exe_rel/exe_sha UNCHANGED | R | fresh accepted packages |
| 13 | `EXPECT_OLD` (297–322) | evt-4a51f4b9413a1476 identities | currently-deployed evt-5cb2c58f855415c3 identities: A binding `7130cfc8…`/canonical `48361f2d…`/manifest `5d5eb70a…`/package `e6b66313…`/191/236323239; B binding `68d622b2…`/canonical `35cbc561…`/manifest `b5874d90…`/package `bb6b06a4…`/194/343454376; `event` `evt-5cb2c58f855415c3`; `launcher_sha` `011a8713…` (frozen boundary held across the generation pair) | R | destination classification of the exact deployed predecessor |
| 14 | `HISTORICAL_EXEC05_*` §14 pins (340–360) | evt-4a51f4b9413a1476 A-REPORT_INVALID-staging / B-NOT_RUN | evt-5cb2c58f855415c3 A-REPORT_FROZEN-custody-out + B-REPORT_INVALID-staging pin set (Section 8 table) | V | the ONE authorized verifier delta |
| 15 | §14 predicate block (~1311–1446) | A staging-census + identity; B root/accounting/report ABSENT (NOT_RUN) | Section 8 predicates A-1..A-5, B-1..B-6 with distinct refusal tokens (incl. new `…_B_CUSTODY_NOT_EMPTY_REFUSED`); B-absence classes RETIRED | V | predecessor geometry change |
| 16 | `PINNED_RECORD_BLOBS` (152–179) | five governance pins at the PCH1 base | the exact pin set resolved at FUTURE IMPLEMENTATION time from the then-exact live base (identity table refresh) | R | repository admission pins move with the publication tip; anchor/protected trees unchanged |
| 17 | Module docstring + header comments (1–128, 185–250, 338–339) | PCH1 lineage prose | PCH2 lineage prose (new authority/event/design-record provenance) | L | no executable effect |
| 18 | `log()` prefix (444) | `[rb003-pch1 …]` | `[rb003-pch2 …]` | L | cosmetic log provenance |
| 19 | `build_handoff` title (3105–3106) | `PCH1-REPLACEMENT … (historical predecessor generation evt-4a51f4b9413a1476)` | `PCH2-REPLACEMENT … (historical predecessor generation evt-5cb2c58f855415c3)` | L | handoff title label only |
| 20 | §14 comment prose | old-geometry description | new-geometry description (custody-out A + present B) | L | comment only |

UNCHANGED (explicitly): `REPO`, `EBS_ROOT`, `DEPLOY_ROOT`, `DEPLOY_EVENT`, `ATTEMPTS_ROOT`, `DRIVER_DIR`; `SOURCE_TRUST_ANCHOR_COMMIT 3058868…`; `FROZEN_TARGET_COMMIT d4d584ff…`; `EBS_PACKAGE_MANIFEST_SHA d683f64d…` / `EBS_PACKAGE_SHA d42aa9e3…`; `LAUNCHER_SHA 011a8713…`; `HISTORICAL_LAUNCHER_SHA` (011a8713, equal across the pair); `GATE_SHA_NEW 27948980…`; `NETWORK_READINESS_SHA 20f37e91…`; `OUTPUT_VALIDATOR_SHA 6aff0e7e…`; `TOOL_WRAPPER_SHA 0ed2ba48…`; `PROBE_TRUE_SHA d3321fd6…`; `PROTECTED_TREES`; `ROOT_BINDING_FILES`; `EXEC_MODE 0o555` + `EXEC_REL_PATHS` (20 frozen executable rel paths) + `EXEC_TABLE`; every runtime/accounting/validator/conformance/custody/handoff function body except the §14 block; all wrapper control mechanics.

Wrapper deltas (`5423ec76…`, 82 lines):

| # | Location | Old | New | Class |
|---|---|---|---|---|
| W1 | `DRIVER=` | `…-pch1-5cb2c58f-impl01.py` | `…-pch2-aa640691-impl01.py` | R |
| W2 | `REQUIRED_DRIVER_SHA256=` | `7a8389a3…` | the EXACT final SHA-256 of the future implemented driver, filled at future implementation time (contract: the wrapper MUST pin it exactly) | R |
| W3 | header/authority/one-human-command comments | PCH1 authority text | PCH2 reserved-authority text (`RESERVED_IDENTITY_PROPOSED_ONLY — NOT YET GRANTED`) | L |

`REQUIRED_DRIVER_MODE="700"`, `set -euo pipefail` / `set +x`, umask 077, core-dump refusal, xtrace env unset, PATH pin, root refusal, symlink/regular-file/owner/mode/SHA pre-exec identity pin, `PYTHON*` unset, `exec /usr/bin/python3 -I` — ALL UNCHANGED (DES2-18). The pre-exec block contains no durable consumption marker; `PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP` is carried OPEN (DES2-30) — the future authority is consumed from the BEGINNING of the human-direct wrapper invocation irrespective of outcome.

Classification result: NO fourth semantic class is required; predecessor semantic delta cardinality == 1 function; wrapper control mechanics unchanged except identity pins/labels. DESIGN BOUNDARY HOLDS.

## Section 10 — Future deployment / staging / backup / invocation mechanics (DES2-18..DES2-21, DES2-32)

Preserved from the accepted PCH1 launcher design, unchanged (statically re-verified in the consumed source):

- Invocation-evidence context created BEFORE any failable Git admission; per-authority non-overwriting dir (`INVOCATION_DIRNAME = AUTHORITY_ID`); second invocation under the same authority REFUSED; authority permanently consumed fail-closed from the BEGINNING of the single human-direct wrapper invocation; marker absence never restores authority; NO retry / resume / fallback / reconciliation.
- Source-event verification (phase1, full both-role byte+mode verification against `EXPECT_NEW` through the exact live EBS) BEFORE deployment; deployment INSIDE the same invocation (phase2); external pre-deployment NOT authorized; staged tree fully verified then destination RE-CLASSIFIED immediately before the atomic same-filesystem rename pair (`os.rename(event→backup)` + `os.rename(staging→event)` + fsync); non-overwriting NEW fixed backup; seven historical backups untouchable; post-deployment full identity re-verification (phase3).
- Destination classification: `EXPECTED_HISTORICAL` (exact `EXPECT_OLD` generation) / `ALREADY_NEW` → REFUSAL, never resume authority / unexpected → STOP. Data-driven — proven Section 6.4.
- Auditor-A FIRST; Auditor-B ONLY after a mechanically conforming Auditor-A; fail-closed `CONSUMED_PRE_EXEC` accounting; maximum 2 inference-capable engagements; generated mechanical handoff LAST (`run_pipeline` finally-block).
- Fresh namespace gates (all must be ABSENT before future execution; presence => fail closed; nothing deleted/normalized/reused): attempts `evt-aa640691cfe9d33c-A-01`/`-B-01` under the deployed attempts root; fresh invocation-evidence authority context; fresh authority-bound mechanical handoff; `event.staging.rb001-l1-rb003-aa640691-pch2`; `event.backup.pre-pch2-replacement-event`; any fresh AccountingStore record; any unexpected fresh authority-tagged runtime artifact (all verified ABSENT at design time — DES2-32).

## Section 11 — Future candidate naming / mode contract (DES2-24, DES2-25, DES2-26)

- Driver: `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch2-aa640691-impl01.py`; Wrapper: `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch2-aa640691-impl01.sh` — collision-clean (ZERO occurrences across the tracked tree at the base, full history `--all -S`, commit messages, working tree, /home/isa top-level names, repo-root archive names).
- Future implementation (if separately authorized) MUST create NEW artifacts: regular / `isa:isa` / mode 0600 / NON-EXECUTABLE at creation. The future wrapper MUST pin the exact final driver SHA-256 and `REQUIRED_DRIVER_MODE=700`; any chmod-to-0700 activation happens only under a separately granted authority after fresh exact-EBS BOTH-role full package-byte reverification.
- This design creates NOTHING.

## Section 12 — Future execution authority — RESERVED IDENTITY ONLY (DES2-22, DES2-23)

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-REPLACEMENT-FIRSTPASS-EXEC-20260927-01` — state during and after this task: `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE`. Collision-checked (ZERO occurrences across tracked tree at base, full git history `-S`, commit messages, working tree, host workspace/archive names). Its appearance in THIS DESIGN grants nothing. HUMAN OPERATOR GRANT = NONE. Future contract if ever granted: event `evt-aa640691cfe9d33c`; attempts A-01/B-01; maximum 2 TOTAL inference-capable engagements; Auditor-A FIRST, Auditor-B ONLY after mechanically conforming A; ONE-SHOT / EXACTLY ONE HUMAN-DIRECT WRAPPER INVOCATION MAXIMUM / NON-TRANSFERABLE / EXACT-TARGET-SPECIFIC / NO RETRY / NO RESUME / NO FALLBACK / NO ALTERNATE driver-wrapper-event-attempt / NO QUALIFICATION AUTHORITY / NO INSTALLATION AUTHORITY.

## Section 13 — Binding future gates and carried residuals (DES2-27..DES2-30)

- **R-PCH2-CR-1** `FULL_FROZEN_PACKAGE_BYTES_NOT_PRESENT_IN_REVIEWER_HANDOFF` — BINDING FUTURE GATE (DES2-27): before ANY future prelaunch/deployment admission, the exact candidate must undergo fresh exact-EBS BOTH-ROLE full package-byte reverification — resolve exact live EBS; `parse_binding` both roles; recompute canonical binding digests (`439ee7fb…`/`b38c1a51…`); run exact `verify_event_package` semantics both roles; re-hash EVERY A and B package payload byte; exact payload-set equality; every per-row SHA/size; exact package/MANIFEST identities; event/attempt/role/target relations; launcher/gate/auditor identities; frozen executable mode table (20 paths 0555); both roles PASS. ANY mismatch => STOP BEFORE chmod/deployment. Inventories/digests alone are insufficient.
- **R-PCH2-CR-2** `SEMANTIC_PRESERVATION_MATRIX_ROLE_PRESENCE_FLAGS_OVERSTATED` (DES2-28) — carried as EVIDENCE-REPORTING PRECISION RESIDUAL / NON-PRODUCT-DEFECT / NON-BLOCKING; future semantic matrices MUST be role-aware (applicability/role field; presence evaluated only against applicable role prompts). Not remediated here.
- **R-PIMP-CR-1** `IMPLEMENTATION_ANALYZER_PARTIAL_ASSIGNMENT_EXECUTION` (DES2-29) — honored: no exec-based candidate analysis; `ast.parse`/text reads only; driver/wrapper never imported or executed.
- **PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP** (DES2-30) — carried OPEN as accepted fail-closed residual; no scope broadening to close it.
- **R-PGPL-CR-1** — carried as the historical EBS gate ROOT-labelled assertion evidence-method residual of the grant/prelaunch verifier script; NOT confused with current PCH2 package identity; the DRIVER's own ROOT check is a live comparison.
- **R-RA002-1** (validator target-commit format-only) — carried unchanged.

## Section 14 — Design acceptance matrix

| ID | Check | Result |
|---|---|---|
| DES2-01 | live Git exact (base/parent/root-tree/canonical-blobs/pins) | PASS (Section 1) |
| DES2-02 | input handoff integrity | PASS (Section 2) |
| DES2-03 | protected trees held | PASS (Section 1; working tree untouched) |
| DES2-04 | consumed PCH1 launcher exact / read-only | PASS (Section 3) |
| DES2-05 | current predecessor event exact | PASS (Section 4) |
| DES2-06 | A accounting exact | PASS (Section 4) |
| DES2-07 | A REPORT_FROZEN report identity/census exact | PASS (Section 4) |
| DES2-08 | B accounting exact | PASS (Section 4) |
| DES2-09 | B REPORT_INVALID snapshot identity/census exact | PASS (Section 4) |
| DES2-10 | sealed-report blindness held | PASS (identity-only; attested Section 0) |
| DES2-11 | fresh PCH2 package identities bound | PASS (Section 5) |
| DES2-12 | fresh event/attempt identities collision-clean | PASS (Section 5) |
| DES2-13 | current PCH1 source static containment proved | PASS (Section 6) |
| DES2-14 | predecessor refs confined to phase0 | PASS (Sections 6.2, 6.3) |
| DES2-15 | EXPECT_OLD/EXPECT_NEW classification data-driven | PASS (Section 6.4) |
| DES2-16 | predecessor verifier delta explicitly specified | PASS (Section 8) |
| DES2-17 | delta confined to one function | PASS (cardinality 1: `phase0_operator_host_check`) |
| DES2-18 | wrapper control mechanics held | PASS (Section 9, W-table) |
| DES2-19 | deployment stays inside invocation | PASS (Section 10; `run_pipeline` order static) |
| DES2-20 | external pre-deployment rejected | PASS (Section 10) |
| DES2-21 | no-retry/no-resume preserved | PASS (Section 10) |
| DES2-22 | future authority exact identity reserved only | PASS (Section 12) |
| DES2-23 | no grant exists | PASS (NONE; publication is docs-only) |
| DES2-24 | future candidate names collision-clean | PASS (Section 11) |
| DES2-25 | future candidate mode contract 0600/non-executable | PASS (Section 11) |
| DES2-26 | future wrapper final-driver SHA/mode pin contract | PASS (Section 11, W2) |
| DES2-27 | R-PCH2-CR-1 full-byte future gate carried | PASS (Section 13) |
| DES2-28 | R-PCH2-CR-2 carried | PASS (Section 13) |
| DES2-29 | R-PIMP-CR-1 honored | PASS (Section 6 method) |
| DES2-30 | wrapper-preexec marker gap carried | PASS (Section 13) |
| DES2-31 | credential contents unread | PASS (zero credential access this session) |
| DES2-32 | fresh runtime namespace still absent | PASS (Section 10) |
| DES2-33 | ZERO runtime | PASS (Section 0) |
| DES2-34 | NO execution authority | PASS (Section 12) |
| DES2-35 | NO qualification/install | PASS |

## Section 15 — Publication boundary and held truth

Exactly THREE tracked paths changed by this publication: (1) NEW canonical design record (this file); (2) `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (current-facing field rotation + one dated appended record); (3) `docs/chatgpt-project/AUCDEV-BACKLOG.md` (one dated appended record). NOT modified: the consumed PCH1 driver/wrapper (re-hashed read-only), fresh PCH2 packages, deployed event, backups, attempts, AccountingStore, reports, credentials, protected trees, prior canonical records, `AUCDEV-ARCHITECTURE-SUMMARY.md`, `AUCDEV-QUALIFICATION-HISTORY.md`. Sole parent of the single docs-only fast-forward commit: `8fdc86c988ff592e0750e3538b0b7b981eaed1ed`. The design evidence workspace is an UNTRACKED HOST ARTIFACT.

Held truth preserved verbatim: consumed authority `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` remains CONSUMED/TERMINAL/CLOSED/NO_RERUN; EXEC-RB-001 OPEN/ROOT_CAUSE_UNRESOLVED; EXEC-RB-002 CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH; EXEC-RB-003 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_MECHANICAL_STRENGTH; EXEC-RB-004 CLOSED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH; PREP-001 CLOSED; OLA-001 CLOSED; EXEC-RA-001 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH (old event only); EXEC-RA-002 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH (disposition A; superseded in consequence by the accepted PCH2 preparation path); PCH-001/PCH-002 DEFENSE-IN-DEPTH PROMPT-CONFORMANCE HARDENING / EXTERNAL-AUDITOR-OUTPUT-RISK REDUCTION / NOT PRODUCT-DEFECT REMEDIATION; prior nonconforming candidate `15198c02…`/`1366785b…` permanently NOT_ADMITTED untouched; old OLA001R1 artifacts `1863c343…`/`ac258cb3…` untouched; AUCDEV-023 remains **P1 / READY / NOT DONE** with NO queue-count transition (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11); audit completeness INCOMPLETE; qualification NONE; installation NONE; installed source `8ae33444f349ce73c1359b963722e2d16acba630` with installed-qualified provenance NOT ESTABLISHED.

## Section 16 — Next action — EXACTLY ONE

CONTROL ROOM READBACK OF THE PCH2 REPLACEMENT OPERATOR-LAUNCHER REBIND/ADAPTATION DESIGN AND ITS GENERATED-LAST HANDOFF BEFORE ANY LAUNCHER IMPLEMENTATION, NEW DRIVER/WRAPPER CREATION, CHMOD, PRELAUNCH ACTIVATION, DEPLOYMENT, RUNTIME ATTEMPT CREATION, CREDENTIAL-CONTENT READ, REPLACEMENT EXECUTION-AUTHORITY GRANT, AUDITOR/PROVIDER EXECUTION, QUALIFICATION, OR INSTALLATION.

DO NOT IMPLEMENT THE LAUNCHER. DO NOT CREATE DRIVER/WRAPPER ARTIFACTS. DO NOT CHMOD. DO NOT DEPLOY. DO NOT READ REPORT SUBSTANCE. DO NOT RUN AUDITORS/PROVIDERS. DO NOT GRANT EXECUTION AUTHORITY.
