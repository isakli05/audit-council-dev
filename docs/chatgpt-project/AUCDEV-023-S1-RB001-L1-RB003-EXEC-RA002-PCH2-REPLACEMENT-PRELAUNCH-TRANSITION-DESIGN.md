# AUCDEV-023 — S1 RB-001 L1 RB-003 EXEC-RA-002 / PCH-002 — Replacement Prelaunch Transition Design

Design authority: `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN-20260927-01`

Disposition: `PCH2_REPLACEMENT_PRELAUNCH_TRANSITION_DESIGN = READY_FOR_CONTROL_ROOM_READBACK / ACCEPTED_IMPLEMENTATION_CANDIDATES_BOUND / DRIVER_WRAPPER_0600_NON_EXECUTABLE / PRELAUNCH_MODE_BARRIER_CLOSED / EXACT_FUTURE_HUMAN_GRANT_TARGET_DEFINED / FRESH_EXACT_EBS_BOTH_ROLE_FULL_PACKAGE_BYTE_GATE_DEFINED / CORRECT_GOVERNING_EBS_SHA_BOUND / LIVE_GATE_ROOT_COMPARISON_REQUIRED / CURRENT_PREDECESSOR_GATES_DEFINED / FRESH_NAMESPACE_GATES_DEFINED / REPOSITORY_AUTHORITY_GATES_DEFINED / CREDENTIAL_METADATA_ONLY_GATE_DEFINED / CHMOD_ONLY_POST_GRANT_ACTIVATION_DEFINED / DRIVER_THEN_WRAPPER_0600_TO_0700_ORDER_DEFINED / PARTIAL_CHMOD_FAIL_CLOSED_SEMANTICS_DEFINED / DEPLOYMENT_REMAINS_INSIDE_SINGLE_HUMAN_DIRECT_INVOCATION / SINGLE_USE_FAIL_CLOSED_AUTHORITY_CONSUMPTION_DEFINED / WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP_CARRIED / NO_RETRY / NO_RESUME / NO_FALLBACK / NO_GRANT / NO_CHMOD / NO_DEPLOYMENT / ZERO_RUNTIME / NO_EXECUTION_AUTHORITY / NO_QUALIFICATION / NO_INSTALLATION`

This session was a BOUNDED PRELAUNCH TRANSITION DESIGNER and READ-ONLY EVIDENCE COLLECTOR — NOT the human operator granting execution, NOT a grant publisher, NOT a prelaunch activator, NOT a launcher executor, NOT a deployment authority, NOT an execution controller, NOT Auditor-A/B, NOT a credential-content reader, NOT a provider/model execution authority, NOT a qualification authority, NOT an installation authority. THIS TASK WAS DESIGN ONLY: it designed — but did NOT perform — the transition from the Control-Room-accepted PCH2 replacement launcher implementation candidate to a possible future human-granted, chmod-only activated, single-use execution lifecycle.

Writing, quoting, recording or discussing the future grant phrase in this design DOES NOT GRANT IT.

---

## Section 0 — Role, boundary and zero-runtime attestation (PLD2-38..PLD2-43)

- ZERO runtime this session: NO grant issued or simulated; NEITHER candidate chmod'ed (both remain mode 0600 NON-EXECUTABLE, re-verified); driver NEVER executed/imported/sourced (non-executing `ast.parse` + static text reads only); wrapper NEVER executed/sourced (`bash -n` parse-only); NO deployment; NO staging or backup runtime state created; NO runtime attempts or AccountingStore created; NO credential content read (metadata only, and none needed beyond binding-declared structure); NEITHER sealed report opened (identity-only hash/stat/census); NO dynamic gate executed; NO auditor/provider/model run; NO execution authority created, granted or consumed; NO qualification; NO installation.
- Permitted local operations: read-only hashing/stat/census, `ast.parse` static analysis, text reads, `bash -n` parse-only, git bootstrap/publication tooling, read-only streaming verification of the input handoff archive, evidence-workspace writes under the untracked design evidence directory.
- Network: the mandated bootstrap `git ls-remote`, the pre-staging live re-resolve, the single `git push` of this publication, and the post-push readback ONLY.

## Section 1 — Exact live bootstrap (PLD2-01)

| Item | Value |
|---|---|
| Live GitHub master at bootstrap (`git ls-remote origin refs/heads/master`) | `00c9cb8b9d60a80e66f4e1556ebe118c553c116a` |
| Local HEAD == live master | EXACT (`00c9cb8b…`) |
| Root tree at base | `ffe450d2a6c648a5562caf0f71af45d0e8af2a72` EXACT |
| Sole parent | `217172bce17dd0c5aa11f30920b8f991165fe2b0` EXACT |
| Implementation Control Room readback blob | `ff8da9c0c17b31924925e237094489e6a5b4e23b` (path `…-PCH2-REPLACEMENT-OPERATOR-LAUNCHER-IMPLEMENTATION-CONTROL-ROOM-READBACK.md`) EXACT |
| CURRENT-STATE blob | `2ab4e1b625678d2cbdeb2592710405b3c0f871a4` EXACT |
| BACKLOG blob | `879b5c2dc02fdc88a6d9739d83ae46ede022c3bf` EXACT |
| Implementation record blob | `5083ac45e56dd5250c2482fd48db9b5a17b5c0ac` (path `…-PCH2-REPLACEMENT-OPERATOR-LAUNCHER-IMPLEMENTATION.md`) EXACT |
| Design-readback/correction blob | `609b0e45e16eb11b19f0412fb5a1e5b6a3392982` (path `…-PCH2-REPLACEMENT-OPERATOR-LAUNCHER-REBIND-ADAPTATION-DESIGN-CONTROL-ROOM-READBACK-CORRECTION.md`) EXACT |
| Lineage | trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor; 44 commits since anchor; merges since anchor 0; changed paths since anchor all under `docs/chatgpt-project/` (0 offending) |
| Tracked working-tree drift | pre-existing `smoke-fixture` / `smoke-fixture-103` gitlink rows only, outside governed paths, recorded honestly and NOT staged |

## Section 2 — Input implementation-readback handoff identity (PLD2-02)

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-REPLACEMENT-OPERATOR-LAUNCHER-IMPLEMENTATION-CONTROL-ROOM-READBACK-HANDOFF.tar.gz`

- Outer SHA-256 `c68a4cc456370ec229487cc1934226c87bf885a59be295feb975d5e5b00650ad` / 826738 B / regular `isa:isa` 0644 — EXACT.
- Census EXACTLY 23 members = 23 regular (22 payload + exactly 1 `SHA256SUMS`) + 0 directories + 0 symlinks/hardlinks/special + 0 unsafe/traversal/duplicate paths; `SHA256SUMS` 22 rows 22/22 PASS by read-only streaming re-hash; 0 missing; 0 unlisted; member set == SUMS row set.
- Canonical copies Git-blob EQUAL to the live Git blobs at `00c9cb8b`: readback `ff8da9c0…` / CURRENT `2ab4e1b6…` / BACKLOG `879b5c2d…`.
- ZERO archive members executed.

## Section 3 — Protected trees held (PLD2-03)

| Tree | ID at base | Working-tree drift |
|---|---|---|
| `bootstrap-supervisor` | `732b8def9f22d7c466ce77f3d3049da53bfff3d0` | NONE (byte-equal) |
| `qualification-harness` | `5b8d5e5465923740470ff63ed9b8683f257a3787` | NONE (byte-equal) |
| `skill` | `c792933a862d9a5434681a88d183470dd8b15d2f` | NONE (byte-equal) |

Five immutable governance pins re-resolved live at the base ALL EXACT: `9f7599fe…` / `578b58c8…` / `83951286…` / `7ba8910e…` / `776a039a…` (also statically present in the candidate driver's `PINNED_RECORD_BLOBS` and verified to resolve exactly at HEAD).

## Section 4 — Accepted PCH2 candidate driver — exact identity, read only (PLD2-04)

| Item | Value |
|---|---|
| Path | `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch2-aa640691-impl01.py` |
| SHA-256 | `63352e347c3ee03219c0fc16855a0114eab7f2bf238429d57b8dbfb7eb4e0a05` EXACT |
| Size | 169121 B EXACT |
| Lines | 3394 EXACT |
| Owner / type / mode | `isa:isa` / regular non-symlink / 0600 / executable-bit ABSENT |
| Static analysis | non-executing `ast.parse` PASS — 52 top-level functions, single class `DriverStop` |
| Runtime | NEVER executed/imported/sourced this session |

Driver identity constants statically verified (text read only): `AUTHORITY_ID` = the reserved future authority (Section 11); `EVENT_ID` = `evt-aa640691cfe9d33c`; `SOURCE_EVENT_ROOT` = the canonical PCH2 preparation workspace event root; `DRIVER_PATH`/`WRAPPER_PATH` exact; `STAGING_DIRNAME` = `event.staging.rb001-l1-rb003-aa640691-pch2`; `BACKUP_DIRNAME` = `event.backup.pre-pch2-replacement-event`; `EBS_PACKAGE_MANIFEST_SHA` = `d683f64d…` and `EBS_PACKAGE_SHA` = `d42aa9e3…e93c922f8` each pinned exactly once with the CORRECT governing value; `PROMPT_CONTRACT_SHA` = `fe5243f4…`; `LAUNCHER_SHA` = `011a8713…`; `EXPECT_NEW` binds the fresh A/B identity tables (A binding `075b2de2…` / canonical `439ee7fb…` / manifest `45adb980…` / package `0637a86e…` / 191 rows); frozen `EXEC_REL_PATHS` = EXACTLY the accepted 20-path mode-0555 executable table (9 A + 11 B); wrong historical EBS SHA occurrences in the driver: 0.

## Section 5 — Accepted PCH2 candidate wrapper — exact identity and pins (PLD2-05, PLD2-06)

| Item | Value |
|---|---|
| Path | `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch2-aa640691-impl01.sh` |
| SHA-256 | `e703af08d0b53120896aeb3e53bbada9a33de6a1e8a231adad8e518ab2ddec29` EXACT |
| Size | 3468 B EXACT |
| Lines | 82 EXACT |
| Owner / type / mode | `isa:isa` / regular non-symlink / 0600 / executable-bit ABSENT |
| Parse check | `bash -n` PASS (parse-only; never executed/sourced) |

Wrapper statically pins (text read only): `DRIVER` = the exact driver path above (line 44); `REQUIRED_DRIVER_SHA256` = `63352e347c3ee03219c0fc16855a0114eab7f2bf238429d57b8dbfb7eb4e0a05` (line 45) — the EXACT final driver SHA; `REQUIRED_DRIVER_MODE` = `700` (line 46). Control mechanics present and unchanged: `set -euo pipefail`, `set +x`, `umask 077`, core-dump refusal (`ulimit -c 0`), PATH pin, root refusal, regular/non-symlink/owner/mode/SHA pre-exec pins, `PYTHON*` unsets, direct `exec /usr/bin/python3 -I "$DRIVER"` (line 82). NO durable pre-exec consumption marker (carried gap, Section 20). Wrong historical EBS SHA occurrences in the wrapper: 0.

## Section 6 — PRELAUNCH_MODE_BARRIER = CLOSED (PLD2-07)

`PRELAUNCH_MODE_BARRIER = CLOSED` — reason: driver mode 0600 ≠ wrapper-required driver mode 0700 AND the wrapper itself remains non-executable 0600. No human-direct invocation is currently mechanically admitted. The barrier opens ONLY through the future bounded chmod-only activation defined in Section 16, which itself requires the prior explicit human grant.

## Section 7 — Governing EBS identity — correct value only (PLD2-08, PLD2-09)

From the LIVE protected `bootstrap-supervisor/MANIFEST.json` (working-tree copy git-blob-equal to HEAD):

| Item | Value |
|---|---|
| EBS MANIFEST SHA-256 | `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999` EXACT |
| EBS package SHA-256 (`package_sha256`) | `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8` — CORRECT, governs this design and every future gate |
| Historical mistranscription ending `…e93e922f8` | count 0 in the live MANIFEST, 0 in the candidate driver, 0 in the candidate wrapper — MUST NOT govern |

R-PCH2-DES-CR-1 remains CLOSED at record-precision strength; the correct pin governs. Both fresh PCH2 role bindings themselves declare `ebs_package.package_sha256` = the correct `d42aa9e3…e93c922f8` value. EBS semantics references for the future gate: `verify_event_package` at `bootstrap-supervisor/ebs/launch.py:469`; `AUDITOR_INVOCATION_ITEM_MAX_BYTES = 1024` at `bootstrap-supervisor/ebs/binding.py:149` with the fail-closed per-item check at `binding.py:302`; the MANIFEST describes a 33-file package.

## Section 8 — Current deployed predecessor — held until invocation (PLD2-10..PLD2-14)

Deploy root `/home/isa/aucdev023-s1-prep002-rem002`; current deployed event `evt-5cb2c58f855415c3`; staging dirs 0; attempt census 27.

Deployed generation identity (re-hashed read-only EXACT): A binding `7130cfc88ed6fdea1347c815e1b958c384eabda3534d33437243122e26f578e2` / B binding `68d622b291efcee25cea698165283561f94676481a3aec2e2532a8a48c7d70ab`; A MANIFEST `5d5eb70a9f938db19a12e2dec00af4c6fd97f10bb9eb4e40063eea8bc0609435` / B MANIFEST `b5874d90dc9b101cd93763b0cb5b0badbed5e8e90381f01de0673e3838ef24fb`.

Auditor-A predecessor attempt `evt-5cb2c58f855415c3-A-01`: accounting SHA `a95eb7b011dff4d5bf06ffcc36ad63ff683096990095952a8c17525621a70023` / 5616 B / 0600 with states EXACTLY `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_FROZEN → TERMINAL`; report-suffixed census EXACTLY `custody-out/evt-5cb2c58f855415c3-A-01.first-pass-report.json` (staging EMPTY); frozen report identity ONLY `dbc47587f866412cd09e129d6b3da42673e1965a0a511997154bb568f680b621` / 28465 B / 0444 / regular non-symlink.

Auditor-B predecessor attempt `evt-5cb2c58f855415c3-B-01`: accounting SHA `c1be982079b178aac68dfba05997d67370491f8446c7f861cf026ffde5b68c87` / 5662 B / 0600 with states EXACTLY `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_INVALID → TERMINAL`; custody-out EMPTY; report-suffixed census EXACTLY `staging/evt-5cb2c58f855415c3-B-01.first-pass-report.json`; invalid snapshot identity ONLY `5a7d105b3cb8c9c9da3e9858b31d760584fe8ded2c3351fc4d82da5374f256c0` / 117 B / 0600 / regular non-symlink.

Sealed-report blindness (PLD2-13): BOTH sealed artifacts verified by path / lstat / SHA-256 / size / mode / bounded census ONLY — never opened, decoded, printed, quoted or fed to any parser; no key-name inference; NO re-diagnosis of `REPORT_KEYS_INVALID`. The future grant/prelaunch session must re-verify this exact geometry identity-only before chmod, and the eventual driver independently re-verifies it again at invocation (phase0 predecessor verifier, already statically bound in the accepted candidate).

Historical backup census EXACTLY SEVEN, present and untouchable: `event.backup.pre-successor-event`, `event.backup.pre-exec03-new-event`, `event.backup.pre-exec02`, `event.backup.pre-rb001-l1-successor-event`, `event.backup.pre-rb002-successor-event`, `event.backup.pre-rb003-corrected-successor-event`, `event.backup.pre-pch1-replacement-event` (PLD2-14).

## Section 9 — Fresh runtime namespace — currently pristine (PLD2-15..PLD2-19)

Read-only recursive sweep of the deployed launcher root: `aa640691` content occurrences 0; `aa640691`-named paths 0; fresh attempt roots `evt-aa640691cfe9d33c-A-01` / `evt-aa640691cfe9d33c-B-01` ABSENT; fresh staging `event.staging.rb001-l1-rb003-aa640691-pch2` ABSENT; fresh backup `event.backup.pre-pch2-replacement-event` ABSENT; authority-tagged runtime artifacts 0; fresh invocation-evidence authority directory / fresh authority-bound mechanical handoff / fresh AccountingStore records ABSENT. Nothing deleted, normalized or reused. The same absence set is a MANDATORY pre-chmod gate for the future grant/prelaunch session: ANY presence ⇒ STOP (do NOT delete / normalize / reuse).

## Section 10 — Fresh PCH2 execution target and package identities (future gate targets)

Event `evt-aa640691cfe9d33c` (derivation `evt-` + first 16 lowercase hex of selection SHA `aa640691cfe9d33c867e1cc9c5b9e050eb8bbfddf8ae445935477ef157a325e5` / 689 B — reproduced); attempts `-A-01` / `-B-01`; maximum 2 inference-capable engagements TOTAL; Auditor-A FIRST, Auditor-B ONLY after a mechanically conforming Auditor-A `REPORT_FROZEN`. Fresh source event root (the ONLY permitted future deployment source): `/home/isa/aucdev023-s1-rb001-l1-rb003-exec-ra002-pch2-compact-fresh-replacement-package-prep-20260927-02/event`.

| Identity | Auditor-A | Auditor-B |
|---|---|---|
| Binding file SHA-256 | `075b2de246065c4828fedc588256686750f15b04579444ac60f973e287411f16` | `19ba43f5869ee5a57e1191a9699fa012f48cb75724d76a9b476c40d7b0443fc1` |
| Canonical binding digest | `439ee7fb5a76376f9572c8a38364c7cba288afb4ef23d18844ded68d1023fdb2` | `b38c1a5105bb2ac8789fb536ac5d3ff39a440956aeb3e01b3e9038fd697550a6` |
| MANIFEST SHA-256 | `45adb9800ff3ef93e71d09e08629a44df324c362e562cd93118575c329b853bd` | `9b18bcb046ba8bdbef49ac4083b6aaf401f2fb65d1952e6339ce9aa051f63b4c` |
| Package SHA-256 | `0637a86e14916d750b8c0cd7ce553c7594deaa30a17ea45b8719dcffe7a4caaf` | `796457a2db3a8e33549ed4347daf7ff7d7de73c303917cbfe5d7bea7c9191aa3` |
| Rows (unique) | 191 (191) | 194 (194) |
| Payload bytes | 236323090 | 343454621 |

Row counts and payload totals recomputed this session directly from the fresh MANIFESTs: EXACT. Shared plane (identical in both fresh bindings): prompt contract `fe5243f4730827b21b1a5ec1b318813a7e681006350131397b99081334cf47a1`; boundary launcher `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa`; resource gate `27948980653f4c0639041243d9f117087f0987c5cc53623abbfa39cbb143adaf`; network-readiness `20f37e9191d3e1e025962723328c5f8a2849f664cf1bf215715ccf8da9fc7235`; output validator `6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071`; tool-domain wrapper `0ed2ba485ccbb623bb1bb4a649635749ab845445dd78cef507787a108a66d572`; Auditor-A executable (claude 2.1.274) `15e2d05148f801b5774032faad87e624ecd172e9903288bda448b892eb58fa07`; Auditor-B executable (codex 0.154.0) `3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022`; frozen target commit `d4d584ffa47ad2848268ba947247f81a845b2322`. Frozen executable table: EXACTLY the accepted 20-path mode-0555 `EXEC_REL_PATHS` table statically present in the candidate driver (lines 371–392). Carried prompt bounds: A prompt 755 B / B prompt 939 B / B argc exactly 8 with the compact prompt as final positional — all within the frozen EBS 1024-byte argv item bound.

## Section 11 — Exact future grant target table (PLD2-20, PLD2-21, PLD2-22)

Authority (SUBJECT RESERVED FUTURE EXECUTION AUTHORITY):

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-REPLACEMENT-FIRSTPASS-EXEC-20260927-01`

Current state — and unchanged by this design: `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE`; **HUMAN OPERATOR GRANT = NONE**.

| Target | Value |
|---|---|
| Driver path | `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch2-aa640691-impl01.py` |
| Driver SHA-256 | `63352e347c3ee03219c0fc16855a0114eab7f2bf238429d57b8dbfb7eb4e0a05` |
| Driver size / required pre-grant mode | 169121 B / 0600 |
| Wrapper path | `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch2-aa640691-impl01.sh` |
| Wrapper SHA-256 | `e703af08d0b53120896aeb3e53bbada9a33de6a1e8a231adad8e518ab2ddec29` |
| Wrapper size / required pre-grant mode | 3468 B / 0600 |
| Wrapper pins | driver SHA exactly above; `REQUIRED_DRIVER_MODE=700` |
| Event / attempts | `evt-aa640691cfe9d33c` / `-A-01`, `-B-01` |
| Budget / ordering | max 2 inference-capable engagements TOTAL; A FIRST; B only after mechanically conforming A |
| Properties | ONE-SHOT; ONE HUMAN-DIRECT WRAPPER INVOCATION MAXIMUM; NON-TRANSFERABLE; EXACT-TARGET-SPECIFIC; NO RETRY; NO RESUME; NO FALLBACK; NO ALTERNATE DRIVER/WRAPPER/EVENT/ATTEMPT; NO QUALIFICATION AUTHORITY; NO INSTALLATION AUTHORITY |

The exact future human-operator grant phrase is:

`GRANT AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-REPLACEMENT-FIRSTPASS-EXEC-20260927-01`

A future grant is valid ONLY if the HUMAN OPERATOR later sends that exact grant as a separate explicit message AFTER this design AND its Control Room readback have been accepted. Malformed, partial, conditional, hedged, wrong-ID or wrong-target text = NO GRANT. Its appearance in this record grants nothing.

## Section 12 — Authority state machine (design only)

1. NOW and after this design: `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE`.
2. After a future separate explicit HUMAN OPERATOR GRANT, before chmod: `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_NOT_YET_ACTIVATED`.
3. After a SUCCESSFUL bounded chmod-only activation: `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED`.
4. At the BEGINNING of the eventual human-direct wrapper invocation: authority becomes permanently `CONSUMED / NON_REUSABLE` — FAIL-CLOSED regardless of whether wrapper prechecks complete, Python starts, driver invocation evidence is created, deployment happens, attempts are created, AccountingStore exists, credential contents are read, a dynamic gate runs, a provider starts, or inference occurs.
5. After that single invocation terminates/stops: `CONSUMED / TERMINAL / CLOSED / NO_RERUN`. No unused engagement capacity restores authority.

## Section 13 — Future exact-EBS both-role full package-byte gate — MANDATORY BEFORE ANY CHMOD (PLD2-23..PLD2-26)

R-PCH2-CR-1 remains BINDING. This design DEFINES but DOES NOT EXECUTE the following gate; it is a mandatory pre-chmod stage of the future bounded grant/prelaunch activation session. The gate executes NO auditor/provider/model and NO package executable.

1. Resolve the LIVE protected `bootstrap-supervisor` at its exact then-live canonical Git base.
2. Require protected tree `732b8def9f22d7c466ce77f3d3049da53bfff3d0`.
3. Require EBS MANIFEST SHA-256 `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999`.
4. Parse that MANIFEST and require its `package_sha256` EXACTLY `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8`.
5. Re-hash the complete protected EBS package source and reproduce that exact package SHA.
6. Load the exact LIVE EBS parsing/verification semantics (not a copy).
7. Parse BOTH fresh PCH2 bindings.
8. Recompute BOTH canonical binding digests: A `439ee7fb5a76376f9572c8a38364c7cba288afb4ef23d18844ded68d1023fdb2`; B `b38c1a5105bb2ac8789fb536ac5d3ff39a440956aeb3e01b3e9038fd697550a6`.
9. Run exact `verify_event_package` semantics for BOTH roles.
10. Independently walk BOTH package trees with `followlinks=false`.
11. Require: zero symlink dirs/files; zero hardlinks; zero specials; zero traversal; exact payload-set equality against each MANIFEST.
12. Re-hash EVERY payload byte for A: exactly 191 unique rows, exactly 236323090 payload bytes, every row SHA/size PASS.
13. Re-hash EVERY payload byte for B: exactly 194 unique rows, exactly 343454621 payload bytes, every row SHA/size PASS.
14. Require exact package identities: A `0637a86e14916d750b8c0cd7ce553c7594deaa30a17ea45b8719dcffe7a4caaf`; B `796457a2db3a8e33549ed4347daf7ff7d7de73c303917cbfe5d7bea7c9191aa3`.
15. Require exact MANIFEST identities: A `45adb9800ff3ef93e71d09e08629a44df324c362e562cd93118575c329b853bd`; B `9b18bcb046ba8bdbef49ac4083b6aaf401f2fb65d1952e6339ce9aa051f63b4c`.
16. Require event/attempt/role/frozen-target relations exact.
17. Require prompt contract `fe5243f4730827b21b1a5ec1b318813a7e681006350131397b99081334cf47a1`.
18. Require boundary-launcher / resource-gate / network-readiness / output-validator / auditor-executable identities exact (Section 10 table).
19. Require the exact frozen 20-path executable set with all modes exactly 0555.
20. **R-PGPL-CR-1 live ROOT comparison (PLD2-25)**: the gate MUST LIVE-COMPARE the ACTUAL bound gate/root binding values — not merely emit a literal-success assertion. Require BOTH roles' actual bound gate_root / strict-root value to equal `/home/isa/aucdev023-s1-prep002-rem002`, and RECORD the observed value from parsed binding/package material. The actual bound values verified statically by this design (for reference): both roles' `runtime/resource-gate.py` pin `ROOT = "/home/isa/aucdev023-s1-prep002-rem002"` (module constant, resource-gate line 59) and both roles' `boundary/networked-boundary-launcher.py` pin the same `ROOT` (line 147), with root-bound staging paths throughout `evidence/gate-w-prime.json`. A line equivalent to `check(..., True, "gate root contract pinned")` is NOT sufficient evidence; until this live comparison is performed, the R-PGPL-CR-1 evidence weakness is NOT superseded for PCH2.
21. BOTH roles must PASS.

ANY mismatch ⇒ STOP BEFORE chmod. Inventories/digests alone are insufficient — every payload byte is re-hashed.

## Section 14 — Repository / canonical-authority future gates

The future grant/prelaunch activation session MUST receive from Control Room the exact canonical prelaunch-design Control-Room-readback HEAD and blobs. Before chmod it MUST freshly verify: live GitHub default branch exact; live HEAD equals the exact authorized canonical base; expected sole-parent/lineage (trust-anchor ancestry, zero unauthorized merges, changed paths confined to `docs/chatgpt-project/`); protected trees exact (`732b8def…` / `5b8d5e54…` / `c792933a…`); candidate-related canonical records exact; `PINNED_RECORD_BLOBS` exact (`9f7599fe…` / `578b58c8…` / `83951286…` / `7ba8910e…` / `776a039a…`); no governed tracked drift; no unrelated staged content. Tip drift ⇒ STOP; no auto-rebase.

## Section 15 — Credential boundary — metadata only (PLD2-27)

This design inspected only binding-declared credential STRUCTURE (adapter ids and in-sandbox credential mount paths such as Auditor-A `/auditor-home/claude-config/.credentials.json` from the frozen isolation evidence); NO credential file was opened, hashed, printed, copied or read. The future prelaunch gate MUST: freshly resolve Auditor-A and Auditor-B credential source metadata; require regular non-symlink; expected owner; mode 0600; size within accepted custody bounds; record path/size/mode/owner ONLY; NEVER hash/print/copy/read contents. Environment locator overrides must be resolved fresh at future prelaunch. Credential CONTENT may only enter the future audited attempt through the already-frozen runtime custody mechanics at authorized-attempt start.

## Section 16 — Future grant/prelaunch activation order — design only (PLD2-28, PLD2-29, PLD2-31)

Runs ONLY after: this design is published; Control Room independently reads it back; the HUMAN OPERATOR sends the exact separate GRANT. Then the bounded grant/prelaunch session MUST perform, fail-closed, in order:

1. Fresh live Git/canonical bootstrap at the exact authorized post-readback SHA.
2. Verify the explicit human GRANT is exact and confined to the reserved ID.
3. Verify no prior grant/consumption/runtime artifact exists.
4. Re-hash/stat driver exact and require 0600.
5. Re-hash/stat wrapper exact and require 0600.
6. Verify wrapper exact driver SHA + `REQUIRED_DRIVER_MODE=700` pins.
7. Re-verify current predecessor A/B geometry identity-only (Section 8).
8. Re-verify all seven historical backups and no unexpected staging.
9. Re-verify fresh runtime namespace pristine (Section 9 set; ANY presence ⇒ STOP).
10. Verify repository lineage / protected trees / `PINNED_RECORD_BLOBS`.
11. Freshly resolve credential metadata ONLY (Section 15).
12. Perform the FULL exact-EBS both-role package-byte gate of Section 13, including the live ROOT comparison.
13. Re-check candidates still exact 0600 after all read-only gates.
14. ONLY THEN: `chmod DRIVER 0600 → 0700`.
15. Immediately stat + re-hash DRIVER: bytes/size/owner/path unchanged; mode exactly 0700.
16. ONLY THEN: `chmod WRAPPER 0600 → 0700`.
17. Immediately stat + re-hash WRAPPER: bytes/size/owner/path unchanged; mode exactly 0700.
18. Re-verify wrapper still pins exact driver SHA and mode 700.
19. EXECUTE NEITHER. 20. DEPLOY NOTHING. 21. CREATE NO ATTEMPTS. 22. Read NO credential contents. 23. Run NO auditor/provider/model.
24. Publish grant/prelaunch canonical record with state `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED`.
25. Generate reviewer handoff LAST. 26. Return to Control Room.

The activation is CHMOD-ONLY: driver first, then wrapper, each immediately re-verified; byte drift after chmod is a candidate-integrity incident and MUST NOT be normalized.

## Section 17 — Partial-chmod fail-closed semantics (PLD2-30)

If DRIVER chmod succeeds but its immediate verification fails; or WRAPPER chmod fails; or wrapper immediate verification fails; or ANY post-chmod invariant fails: STOP. Execute neither. Deploy nothing. Create no attempt. Run no provider. Do not retry automatically. Do not invent rollback authority. Do not silently chmod back to 0600. Do not proceed to human-direct invocation. Return the exact partial activation state to Control Room. A partial activation state is NOT invocation-eligible.

## Section 18 — Deployment boundary — inside the single human-direct invocation (PLD2-32, PLD2-33)

DEPLOYMENT MUST REMAIN INSIDE THE EVENTUAL SINGLE HUMAN-DIRECT WRAPPER INVOCATION. The future grant/prelaunch activation session MUST NOT deploy fresh `evt-aa640691cfe9d33c`, create staging runtime generation, create backup, or create attempts. Accepted eventual driver behavior remains: `EXPECTED_HISTORICAL` = only authorized deployment input; `ALREADY_NEW` = REFUSAL — never resume; UNKNOWN/unexpected = REFUSAL. The eventual human-direct invocation itself: verifies source; stages; verifies; reclassifies; atomically preserves predecessor backup; deploys; post-verifies; then proceeds A-first. Any external/prelaunch deployment would invalidate the one-shot lifecycle.

## Section 19 — Two-stage human lifecycle (PLD2-34)

STAGE A — FUTURE GRANT/PRELAUNCH ACTIVATION: the human first sends the separate exact GRANT; a bounded grant/prelaunch agent performs all gates, the full-byte package verification, the chmod-only activation; executes nothing; publishes the activated state; Control Room independently reads that publication back.

STAGE B — SINGLE HUMAN-DIRECT INVOCATION: ONLY after Control Room accepts the grant/prelaunch readback, the HUMAN OPERATOR directly invokes exactly once, with NO arguments:

```
cd /home/isa/audit-council-dev
./run-aucdev023-firstpass-rb001-l1-rb003-pch2-aa640691-impl01.sh
```

At the BEGINNING of that invocation the authority is irreversibly CONSUMED. No agent performs this human-direct invocation. No second invocation. No retry. No resume. No fallback. THIS DESIGN DOES NOT AUTHORIZE EITHER STAGE.

## Section 20 — PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP — carried OPEN (PLD2-37)

The wrapper still has no durable pre-exec consumption marker. Therefore, if a future human-direct wrapper invocation is KNOWN to begin but fails before the driver creates its durable invocation-evidence context: authority is STILL consumed; absence of the driver marker does NOT restore authority; marker absence is NOT proof no invocation occurred; NO second invocation; NO retry; return to Control Room. The wrapper is NOT redesigned in this task.

## Section 21 — Residual matrix (carried, no scope broadening)

| Residual | Status / requirement |
|---|---|
| R-PCH2-CR-1 | OPEN/BINDING — full package-byte reverification gate (Section 13) mandatory before ANY chmod; inventories alone insufficient |
| R-PCH2-CR-2 | OPEN — semantic-preservation matrix role-presence evidence precision (non-product, non-blocking) |
| R-PCH2-IMP-CR-1 | CLOSED at evidence-precision strength |
| R-PCH2-IMP-CR-2 | CLOSED at evidence-precision strength |
| R-PCH2-DES-CR-1 | CLOSED at record-precision strength; correct EBS SHA `d42aa9e3…e93c922f8` governs |
| R-PIMP-CR-1 | honored — static-analysis-only rule observed (ast.parse/text/bash -n; no execution) |
| PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP | OPEN / accepted / fail-closed / non-blocking (Section 20) |
| R-PGPL-CR-1 | OPEN for PCH2 — historical ROOT-assertion evidence-method residual; future full-byte gate MUST use actual live root comparison (Section 13 step 20) before this weakness can be considered superseded |
| R-RA002-1 | OPEN — target_commit format-only validator residual |

## Section 22 — Design acceptance matrix (PLD2-01..PLD2-43)

| Row | Check | Result |
|---|---|---|
| PLD2-01 | live Git exact (`00c9cb8b…` live == local; root tree/sole parent EXACT) | PASS |
| PLD2-02 | input implementation-readback handoff exact (outer SHA/size; 23 members; 22/22 PASS; 0 missing/unlisted; canonical copies blob-equal) | PASS |
| PLD2-03 | protected trees held (`732b8def…`/`5b8d5e54…`/`c792933a…`; zero drift) | PASS |
| PLD2-04 | candidate driver exact 0600/non-executable (SHA/size/lines/owner/type; ast.parse PASS) | PASS |
| PLD2-05 | candidate wrapper exact 0600/non-executable (SHA/size/lines/owner/type; bash -n PASS) | PASS |
| PLD2-06 | wrapper exact driver SHA + mode-700 pin (lines 44–46) | PASS |
| PLD2-07 | PRELAUNCH_MODE_BARRIER closed (0600 ≠ required 0700; wrapper non-executable) | PASS |
| PLD2-08 | governing EBS SHA correct (`d42aa9e3…e93c922f8` from live protected MANIFEST `d683f64d…`) | PASS |
| PLD2-09 | historical wrong EBS SHA rejected (count 0 in MANIFEST/driver/wrapper) | PASS |
| PLD2-10 | current predecessor event exact (`evt-5cb2c58f855415c3`; bindings/MANIFESTs EXACT; 27 attempts; 0 staging) | PASS |
| PLD2-11 | predecessor A geometry exact (accounting/states/census/report identity) | PASS |
| PLD2-12 | predecessor B geometry exact (accounting/states/custody-out EMPTY/snapshot identity) | PASS |
| PLD2-13 | sealed-report blindness held (identity-only hash/stat; never opened) | PASS |
| PLD2-14 | seven backups exact (exactly the named seven; total 7) | PASS |
| PLD2-15 | fresh staging absent (`event.staging.rb001-l1-rb003-aa640691-pch2`) | PASS |
| PLD2-16 | fresh backup absent (`event.backup.pre-pch2-replacement-event`) | PASS |
| PLD2-17 | fresh attempts absent (`-A-01`/`-B-01`) | PASS |
| PLD2-18 | fresh authority context absent (invocation-evidence dir / handoff / authority-tagged artifacts 0) | PASS |
| PLD2-19 | fresh AccountingStore absent | PASS |
| PLD2-20 | future grant target exact (Section 11 table) | PASS |
| PLD2-21 | HUMAN OPERATOR GRANT = NONE | PASS |
| PLD2-22 | authority currently RESERVED/NOT_GRANTED/NOT_CONSUMED/NOT_EXECUTABLE | PASS |
| PLD2-23 | future exact-EBS both-role full-byte gate defined (Section 13, 21 steps) | PASS |
| PLD2-24 | every payload byte rehash required (A 191 rows/236323090 B; B 194 rows/343454621 B) | PASS |
| PLD2-25 | actual gate-root live comparison required (both roles' bound ROOT == `/home/isa/aucdev023-s1-prep002-rem002`; observed value recorded; literal-True assertion insufficient) | PASS |
| PLD2-26 | package gate before ANY chmod (Section 16 step 12 precedes step 14) | PASS |
| PLD2-27 | credential metadata-only gate defined (Section 15) | PASS |
| PLD2-28 | driver-then-wrapper chmod order defined (Section 16 steps 14–17) | PASS |
| PLD2-29 | immediate post-chmod rehash defined (bytes/size/owner/path unchanged; mode 0700) | PASS |
| PLD2-30 | partial-chmod STOP semantics defined (Section 17) | PASS |
| PLD2-31 | execute-neither activation invariant defined (Section 16 steps 19–23) | PASS |
| PLD2-32 | deployment-inside-invocation preserved (Section 18) | PASS |
| PLD2-33 | ALREADY_NEW refusal preserved (Section 18) | PASS |
| PLD2-34 | single-human-direct-invocation contract defined (Section 19; no arguments; exactly once) | PASS |
| PLD2-35 | authority consumption at wrapper-invocation BEGIN defined (Section 12 state 4; fail-closed irrespective of subsequent failures) | PASS |
| PLD2-36 | no retry / no resume / no fallback | PASS |
| PLD2-37 | wrapper-preexec marker gap carried (Section 20) | PASS |
| PLD2-38 | ZERO runtime | PASS |
| PLD2-39 | NO grant | PASS |
| PLD2-40 | NO chmod (both candidates re-verified 0600 at publication time) | PASS |
| PLD2-41 | NO deployment | PASS |
| PLD2-42 | NO qualification | PASS |
| PLD2-43 | NO installation | PASS |

## Section 23 — Held truth (preserved verbatim)

Consumed authority `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA001-PCH1-REPLACEMENT-FIRSTPASS-EXEC-20260925-01` CONSUMED/TERMINAL/CLOSED/NO_RERUN (engagements 2/2); EXEC-RB-001 OPEN/ROOT_CAUSE_UNRESOLVED; EXEC-RB-002 CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH; EXEC-RB-003 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_MECHANICAL_STRENGTH; EXEC-RB-004 CLOSED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH; PREP-001 CLOSED; OLA-001 CLOSED; EXEC-RA-001 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH (old event only); EXEC-RA-002 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH (disposition A; superseded in consequence by the accepted PCH2 preparation path); PCH-001/PCH-002 DEFENSE-IN-DEPTH PROMPT-CONFORMANCE HARDENING / EXTERNAL-AUDITOR-OUTPUT-RISK REDUCTION / NOT PRODUCT-DEFECT REMEDIATION; prior nonconforming candidate `15198c02…`/`1366785b…` permanently NOT_ADMITTED untouched; old OLA001R1 artifacts `1863c343…`/`ac258cb3…` untouched; AUCDEV-023 remains P1 / READY / NOT DONE with NO queue-count transition (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11); audit completeness INCOMPLETE; qualification NONE; installation NONE; installed source `8ae33444f349ce73c1359b963722e2d16acba630` with installed-qualified provenance NOT ESTABLISHED.

## Section 24 — Publication boundary and next action

Exactly THREE tracked paths changed by this publication: NEW canonical prelaunch transition design record + CURRENT-STATE (current-facing fields rotation + one dated record appended) + BACKLOG (one dated record appended). The candidate driver/wrapper, packages, deployed event, historical backups, attempts/accounting, reports, credentials, protected trees, implementation/readback records, `AUCDEV-ARCHITECTURE-SUMMARY.md` and `AUCDEV-QUALIFICATION-HISTORY.md` NOT modified. Exactly ONE bounded docs-only fast-forward publication commit whose sole parent is `00c9cb8b9d60a80e66f4e1556ebe118c553c116a`. The design evidence workspace remains an UNTRACKED HOST ARTIFACT. The generated-LAST reviewer handoff is produced after the push and post-push verification with nothing included mutated afterward.

NEXT ACTION EXACTLY ONE: INDEPENDENT CONTROL ROOM READBACK OF THIS PCH2 REPLACEMENT PRELAUNCH TRANSITION DESIGN AND ITS GENERATED-LAST HANDOFF BEFORE ANY HUMAN EXECUTION-AUTHORITY GRANT, CHMOD, PRELAUNCH ACTIVATION, DEPLOYMENT, RUNTIME ATTEMPT CREATION, CREDENTIAL-CONTENT READ, AUDITOR/PROVIDER EXECUTION, QUALIFICATION, OR INSTALLATION.

DO NOT ISSUE THE GRANT. DO NOT CHMOD. DO NOT DEPLOY. DO NOT EXECUTE DRIVER/WRAPPER. DO NOT READ REPORT SUBSTANCE. DO NOT RUN AUDITORS/PROVIDERS.
