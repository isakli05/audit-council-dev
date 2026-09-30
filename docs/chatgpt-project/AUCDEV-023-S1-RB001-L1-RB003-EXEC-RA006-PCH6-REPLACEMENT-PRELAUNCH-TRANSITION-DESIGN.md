# AUCDEV-023 S1 RB-001 L1 RB-003 EXEC-RA-006 PCH6 REPLACEMENT PRELAUNCH TRANSITION DESIGN

Publication authority: `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA006-PCH6-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN-20260930-01`
Disposition key: `PCH6_REPLACEMENT_PRELAUNCH_TRANSITION_DESIGN`
Date: 2026-09-30 (Europe/Istanbul). Canonical record: `docs/chatgpt-project/AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA006-PCH6-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN.md`.
Evidence workspace (untracked): `aucdev023-exec-ra006-pch6-prelaunch-transition-design-evidence`.

## Section 0 — Role, boundary and zero-runtime attestation

This session is the bounded **PCH6 REPLACEMENT PRELAUNCH TRANSITION DESIGNER and READ-ONLY MECHANICAL EVIDENCE COLLECTOR**. It designs — but does NOT perform — the future transition from the Control-Room-accepted PCH6 replacement launcher candidates at mode 0600 NON-EXECUTABLE to a possible later, separately human-granted, fail-closed chmod-only activated state.

This session is NOT the human operator issuing an execution grant, NOT a grant publisher, NOT a prelaunch activator, NOT a chmod authority, NOT a launcher executor, NOT a deployment authority, NOT an execution controller, NOT an execution-authority grantor/consumer, NOT Auditor-A/B, NOT a provider/model executor, NOT a qualification authority, NOT an installation authority.

ZERO execution grant. ZERO chmod. ZERO prelaunch activation. ZERO deployment. ZERO launcher execution. ZERO driver import. ZERO wrapper source/execute. ZERO attempt creation. ZERO AccountingStore mutation. ZERO authority consumption. ZERO credential-content access. ZERO auditor/provider/model execution. ZERO qualification. ZERO installation. This publication is DESIGN strength ONLY and is NOT an execution grant, NOT execution readiness, NOT prelaunch admission, NOT remediation proof, NOT fix verification, NOT qualification, NOT installation.

## Section 1 — Exact live bootstrap (PCHTD-01..PCHTD-05)

- Live GitHub `master` == local HEAD == `a982ee8ab725d11038ed10cb791e4a64ebbe604e` EXACT at bootstrap (single `ls-remote` resolve; re-resolved again before staging and immediately before commit — see Section 22 publication safety).
- Root tree `9491aed9acebf42bf1d8efde5a3b96d165a1b7dc`; sole parent `9ed1db1d03ff3c64a02b5713cc95bdec1cf89990` (single-parent, `rev-list --parents` exactly two fields).
- All TEN required canonical blobs verified EXACT at that SHA: package preparation `9ca40b49bf9e0c052bed444f03b7f430864a5c55` (path `…-PCH6-COVERAGE-INSTRUCTION-HARDENED-FRESH-REPLACEMENT-PACKAGE-PREPARATION.md`), package-preparation readback `6caed78cfcd650b584fe3c6391c5eed6c1e3852a`, accepted launcher design `283b2aa6da17de487324eb23b5623ebd8f1b5619`, launcher-design readback `ce9e1ce5eada00b1afb83d7279c2335f658a01b3`, execution-authority reservation `10aba581264efb2fc14be727aad625bb7fd73fd4`, reservation readback `e83e6c89463195b6c33be600f065f220a06e5a77`, implementation `d3528fd8f57632f91d408c626162c9040e62f013`, implementation readback `7b7eae1db386381746a8b8a48087d54012c455ab`, CURRENT `2002330d75a5d09d60982cb0ba0a0370d8253049`, BACKLOG `9ff40d2c8feeb48ebd8edecde6e5bffbb7eecb5c`.
- This design's canonical record path ABSENT at HEAD (`git cat-file -e` rc 128) with a never-existent control path also rc 128 (discrimination proven); full-history path rows exactly ZERO.
- Protected trees EXACT at HEAD with zero tracked drift and zero non-ignored untracked under all three: `bootstrap-supervisor` `732b8def9f22d7c466ce77f3d3049da53bfff3d0`, `qualification-harness` `5b8d5e5465923740470ff63ed9b8683f257a3787`, `skill` `c792933a862d9a5434681a88d183470dd8b15d2f`.
- Trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor rc 0; ZERO merge commits since the anchor; zero staged content before this publication; tracked working-tree drift confined to the pre-existing `smoke-fixture` / `smoke-fixture-103` gitlink rows preserved NOT staged.

## Section 2 — Governing accepted candidates — FRESH live restat (PCHTD-06..PCHTD-09)

FRESH `lstat`/`stat` + double independent SHA-256 + line/byte census on the live host paths, BEFORE any reliance (never executed/imported/sourced/chmodded):

- Driver `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch6-db0324e8-impl01.py`: regular file, non-symlink, owner `isa:isa` (1000:1000), nlink 1, **171086 B**, **3425 LF-terminated lines**, mode **0600** (executable bits ZERO), SHA-256 `b86fff14c4787f61a302fc0f801edb9b71b34da970c468e34d9890b9b7075dc2` — EXACT (two independent hash passes equal).
- Wrapper `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch6-db0324e8-impl01.sh`: regular file, non-symlink, owner `isa:isa`, nlink 1, **3468 B**, **82 lines**, mode **0600** (executable bits ZERO), SHA-256 `0ab7960cf5c5cea74c713c81c0a213729af3d8730deb0e56055b272b17326a8b` — EXACT.

Archive member/reference mode does NOT substitute for this live-host restat. No identity or mode drift was observed; nothing STOPped. **PRELAUNCH_MODE_BARRIER = CLOSED** throughout this design because both candidates remain 0600 with executable bits ZERO.

## Section 3 — Wrapper pin closure / prelaunch mode barrier (PCHTD-10..PCHTD-11)

Static inspection of the exact live wrapper bytes (read only; never sourced/executed):

- `DRIVER="/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch6-db0324e8-impl01.py"` — exact.
- `REQUIRED_DRIVER_SHA256="b86fff14c4787f61a302fc0f801edb9b71b34da970c468e34d9890b9b7075dc2"` — equals the live candidate driver SHA EXACT.
- `REQUIRED_DRIVER_MODE="700"` — preserved, so the pre-exec mode gate INTENTIONALLY FAILS while the live driver is 0600.
- Fail-closed mechanics preserved byte-identically: `set -euo pipefail`; `set +x`; `umask 077`; `ulimit -c 0`; unset of `BASH_XTRACEFD/ZSH_XTRACEFD/SHELLOPTS/BASHOPTS`; `export PATH=/usr/bin:/bin` pinned BEFORE any external call; root refusal (`id -u` == 0 → REFUSED); driver symlink refusal; regular-file check; ownership check (driver uid == operator uid); exact mode gate; exact hash gate; `unset PYTHONPATH PYTHONHOME PYTHONSTARTUP`; `exec /usr/bin/python3 -I "$DRIVER"`. Seven `REFUSED` guards counted.
- The reserved-authority token appears in the wrapper only as input data (the documented NOT-YET-GRANTED reservation), matching the accepted implementation.

## Section 4 — Reserved PCH6 execution authority — UNCHANGED (PCHTD-12)

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA006-PCH6-REPLACEMENT-FIRSTPASS-EXEC-20260930-01` remains **RESERVED / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE** with **EXECUTION_GRANT = NONE**. The accepted implementation only bound this token as launcher input data. This design does NOT grant it, does NOT consume it, does NOT activate it, does NOT create an invocation marker, does NOT create an invocation directory, and does NOT create the future mechanical execution handoff. The consumed PCH5 authority `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA005-PCH5-REPLACEMENT-FIRSTPASS-EXEC-20260929-01` remains permanently CONSUMED / TERMINAL / CLOSED / NO_RERUN (engagements 2/2) and transfers NOTHING to PCH6.

## Section 5 — Input Control Room readback handoff verified READ-ONLY (PCHTD-13..PCHTD-15)

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA006-PCH6-REPLACEMENT-OPERATOR-LAUNCHER-IMPLEMENTATION-CONTROL-ROOM-READBACK-HANDOFF-20260930-01.tar.gz`: outer SHA-256 `1e49db1827ec0b2d2e41dd63a8e46e493d7fc2c0231ba692fbde73adee91b32e` / **1083239 B** EXACT. In-memory read-only tar parsing with ZERO members executed and ZERO extracted to disk: census EXACTLY **54 regular** members, 0 directories, 0 links, 0 specials, 0 EXECUTABLE, 0 unsafe paths; `SHA256SUMS` exactly **53 rows, 53/53 PASS** with exact payload-set equality (0 missing / 0 unlisted / 0 mismatch; archive-root-relative row convention normalized reader-side); ZERO members of sealed hash `b63722154417e3bbbd8819853d4a4830bcbe20d5b49523dac274a1a7b8ead24e` / `5a4b49cfa2810eb45faa2e206a931b750dde17722c9209496de47acd97e8671f` or sealed size 27051/822; ZERO credential-named members and ZERO credential-content pattern hits. Required archive facts independently confirmed from the actual bytes: `13-genlast-report.json` present with `transient_count = 9`; README transient range T-1..T-9 == TRANSIENT-LEDGER.md distinct ids T-1..T-9 (count 9); canonical members real, NON-ZERO and Git-blob EQUAL to live Git — readback `7b7eae1db386381746a8b8a48087d54012c455ab` (30414 B), CURRENT `2002330d75a5d09d60982cb0ba0a0370d8253049` (1973653 B), BACKLOG `9ff40d2c8feeb48ebd8edecde6e5bffbb7eecb5c` (1469377 B), original implementation record `d3528fd8f57632f91d408c626162c9040e62f013` (30505 B). Canonical Git remains authoritative.

## Section 6 — New precision residuals recorded APPEND-ONLY (PCHTD-16..PCHTD-18)

### PCH6-CR-IMPL-RB-PUB-001

Classification: `EXTERNAL_FINAL_RETURN_TRANSIENT_COUNT_MISMATCH / COMPLETENESS_LIMITATION / OPERATOR_REPORTED_EXTRA_TRANSIENTS_UNPRESERVED / NON_PRODUCT_DEFECT / NON_BLOCKING`.

Bases (each independently confirmed in this session):

- (A) The externally supplied FINAL RETURN reports `T-1..T-13`.
- (B) The canonical publication commit `a982ee8` message enumerates session transients EXACTLY `T-1..T-9` (after stripping the two quoted range expressions `T-1..T-12` / `T-1..T-15`, which are PCH6-CR-IMPL-RB-001 Basis-D references to the ORIGINAL implementation archive's internal mismatch, not session transients).
- (C) The final generated-LAST: TRANSIENT-LEDGER.md = T-1..T-9 (9 distinct) and `13-genlast-report.json` `transient_count = 9` and README = T-1..T-9.
- (D) Precision extension observed by this session: the canonical readback record blob `7b7eae1d…` itself physically lists only `T-1..T-7` in its transient ledger section; T-8/T-9 (both docs-builder instrument-side, per the commit message and generated-LAST) are absent from the canonical record's own ledger — a record-level under-enumeration belonging to the same COMPLETENESS_LIMITATION family.

Consequences held: T-10..T-13 remain OPERATOR_REPORTED only; no preserved evidence for them is available to this Control Room; their substance is NOT invented and NOT reconstructed; canonical T-1..T-9 (and record-level T-1..T-7) evidence is NOT rewritten; this does NOT reopen target implementation/readback acceptance.

### PCH6-CR-IMPL-RB-PUB-002

Classification: `BACKLOG_SOLE_PARENT_TRANSCRIPTION_MISMATCH / RECORD_PRECISION_DEFECT / NON_PRODUCT_DEFECT / NON_BLOCKING / LIVE_GIT_IDENTITY_GOVERNS`.

Bases (each independently confirmed in this session): the latest BACKLOG append-only implementation-readback history row (line 2738 of the HEAD BACKLOG) records the implementation commit's sole parent as the 37-hex token `f416256d16a1c3f24495ea8f581d13045112a`, which does NOT resolve in Git (common prefix with the correct token = 33 hex chars; a 3-character deletion — NOT the one-hex-character class of the prior CURRENT-blob tasking typo). The exact actual parent proven by the live Git commit object is `f416256d16a1c3f24495ea8f581d13045315112a`, and the canonical implementation-readback record already records the CORRECT parent. The historical BACKLOG row is NOT edited or rewritten; an append-only correction is published in this design transition's BACKLOG record. The live Git commit object and canonical readback record govern.

The already-canonical `CONTROL_ROOM_TASKING_INPUT_DEFECT` family (including the prior CURRENT-blob tasking typo) is preserved; history is not rewritten.

## Section 7 — Publication-identity collision sweep BEFORE first use (PCHTD-19..PCHTD-22)

Fail-closed sweep over the NINE publication identities (publication authority; canonical record basename + `.md` path; disposition key `PCH6_REPLACEMENT_PRELAUNCH_TRANSITION_DESIGN`; evidence-workspace name; generated-LAST handoff stem; residual IDs `PCH6-CR-IMPL-RB-PUB-001` / `PCH6-CR-IMPL-RB-PUB-002`; acceptance-matrix prefix `PCH6PTD-`) with fresh never-existent guard `AUCDEV-023-NEVER-EXISTENT-GUARD-TOKEN-PCH6PTD-7742` and known-present sanity `evt-db0324e89c6ef4c7`, with sealed `*first-pass-report*` and credential-named files excluded BY NAME from every content scan:

- **S1** tracked content at exact HEAD (+ canonical-path absence rc 128 with never-existent control rc 128): all eight identities and the guard ZERO (10 tracked files × 34 occurrences for sanity).
- **S2** full-history `--all --full-history` pickaxe: all identities + guard ZERO; sanity x7 commits, all the governed PCH6 chain `976d7f8a` / `8c17fe9e` / `35b301fd` / `270f00b6` / `f416256d` / `9ed1db1d` / `a982ee8`.
- **S3** commit-message fixed strings: identical shape — identities + guard ZERO; sanity x7 governed commits.
- **S4** worktree readable contents excluding `.git` (single multi-pattern traversal, per-token attribution): identities + guard confined EXACTLY to this session's own untracked evidence workspace (GOVERNED_SELF; 2–8 files each, all instruments); sanity x187 files including the 10 tracked canonical docs and the candidate driver (known-present).
- **S5** repo-root names: only the evidence-workspace's own name (GOVERNED_SELF).
- **S6** `/home/isa` top-level names: ALL ZERO.
- **S7** FULL-DEPTH `/home/isa` path-name traversal — NO maxdepth, NO pruning, NO symlink following, `find` rc 0 with stderr EMPTY: census **2,236,448 names**, enumeration identity 268507770 B / SHA-256 `edee41a5bca00035011532b24dcba48ff2f834ee4f95e29958a0e18edc758d6d`; every identity ZERO except the evidence workspace's own 66 paths (GOVERNED_SELF); guard ZERO; the 268 MB enumeration is retained in the untracked evidence workspace and intentionally excluded from the generated-LAST for size.
- **S8** deployed-root path names (6,428 names, rc 0, stderr empty): ALL identities + sanity ZERO.
- **S9** readable deployed-root non-sealed contents: rc 1, ZERO matching files, stderr empty.
- **S10** PCH6 runtime namespace: ZERO `db0324e8` / `evt-db0324e8` paths under the deployed root; ZERO `PCH6-REPLACEMENT-FIRSTPASS-EXEC` names anywhere in the full-depth enumeration (invocation/marker namespace absent); ZERO `evt-db0324e8` paths anywhere under `/home/isa`.
- Name-surface liveness proven by supplemental probes (the surfaces discriminate): `db0324e8` appears in exactly the 2 candidate basenames at repo root, and the deployed PCH5 predecessor identity `a54899df` appears in 57 full-depth paths.

**CORRECTED_REAL_COLLISION_COUNT = 0 AND SCAN_ERROR_COUNT = 0.** No alternate publication identities were invented.

## Section 8 — PCH6 prepared generation re-verified at DESIGN strength (PCHTD-23..PCHTD-26)

Fresh event `evt-db0324e89c6ef4c7`; attempts `evt-db0324e89c6ef4c7-A-01` / `evt-db0324e89c6ef4c7-B-01`; selection file (800 B) SHA-256 `db0324e89c6ef4c76cb2137df222fb3410d2f4847fd41f02cf61f684370edffc` EXACT; `evidence/selection.json` re-parsed with `fresh_event` and both attempt ids EXACT. Through ONE read-only import of the LIVE protected EBS parser (method precedent: the accepted implementation session; `sys.dont_write_bytecode`; zero mutation):

- Binding files re-hashed EXACT: A `4e538fd37a40c2ce23ac65a4c8e6a529f1d28c2361ecc41807cf52fbbea2f088`, B `a9c6a5d30d1a36958c23a1f528636dd94beda7e5be61995689e8fbb174653953`.
- `parse_binding` OK for both roles (event/role/attempt/output-name geometry exact).
- Canonical binding digests RECOMPUTED EXACT through the live parser: A `506d3b3f14af3436ac23bd0f7fc67550a60fb6c82876d8962bc0d4a1b239e84f`, B `3cd8aa925eca0e162c75aa3b49dad4278f5d4aed6a0f2ec997d50460ecca4580`.
- MANIFESTs re-hashed EXACT: A `ddd515113ce3651b800dc8f3164e56ffc2bbde96ab5c5ca711b44fce4bc878ca`, B `c42a5b7bef1991ddc2ec3ebdf38d22f32498462400aafe9ab867f08201b1ea98`; binding pins (`manifest_sha256` / `package_sha256`) exact; package digests A `be364cf25220f8af5765eff02ebb266c4df14fc9344bb00fbfb8051c941c99fe`, B `178ab21c33c41903e5e5d7d4d0afd70033a9c7671fe2365c573d85ab21334a72`.
- `verify_event_package` PASS both roles: A files=191 / bytes=236327843; B files=194 / bytes=343459010 — EXACT geometry (MANIFEST row census re-derived directly: 191 / 194 rows; payload byte totals exact).
- Prompt contract `59c0450f1f4e465f64a099fed05c0bd3f9e9edba7ce1b44141bfaf79b1450c09` EXACT at ALL FIVE live copies (A/B × transport + payload-evidence, plus common-evidence).
- Profiles EXACT: A `865e912a0ed6da93c56d3c190cc17c3c229294b19eec2691ab910898b62d75e5`, B `586c1f7fc63e2474335371f6d6358d19a1bf119a470c3d8fd1dd8296db0f5f88`.
- Current-live EBS corroboration recorded as DESIGN-TIME ONLY: `bootstrap-supervisor/MANIFEST.json` freshly re-hashed EXACT at the canonical pin `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999`; live `ebs/binding.py` SHA-256 `39bd966a94825f2e01d4613bf6a7e8be4070e8712266a4d58d99051632574184` and live `ebs/launch.py` SHA-256 `dfc63f0033aad802e5355e9dad652499d27a602122c7cfa1e2fa4d252947e9b7` (the protected `bootstrap-supervisor` tree is pinned EXACT at HEAD, so no drift since HEAD is possible); the governing EBS package SHA `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8` remains as canonically recorded and is NOT recomputed in this zero-runtime session — THEN-live resolution is REQUIRED at future activation.

ZERO mutation of package/binding/MANIFEST/contract/profile bytes. **These design-time identity observations do NOT satisfy and do NOT waive the future R-PCH2-CR-1 gate** (Section 12).

## Section 9 — Deployed PCH5 predecessor and fresh namespace — identity-only (PCHTD-27..PCHTD-29)

Read-only observation of `/home/isa/aucdev023-s1-prep002-rem002` with ZERO mutation: event root EXACTLY 4 entries (binding-auditor-a.json, binding-auditor-b.json, package-auditor-a, package-auditor-b); attempt census EXACTLY 35 top-level entries / 76 files; historical backups EXACTLY ELEVEN (including `event.backup.pre-pch5-replacement-event`); staging ZERO; deployed predecessor binding identities re-hashed EXACT unchanged (A `4532767335de4385c49c8b31df1bc776600773ca837b7d7e0d423394b71260c9`, B `3a1ff88ef2defc3e0936f8a78d8a03d9f5b9d37befeea15fcf4b03453904c7b8`); the fresh PCH6 runtime identity, both candidate basenames and the authority invocation-marker namespace ABSENT from the deployed tree at any depth. No material mismatch; nothing STOPped; this design does not repair any state.

## Section 10 — Exact future human grant target — DESIGN ARTIFACT ONLY (PCHTD-30..PCHTD-31)

Target authority: `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA006-PCH6-REPLACEMENT-FIRSTPASS-EXEC-20260930-01`. Target driver `aucdev023-firstpass-rb001-l1-rb003-pch6-db0324e8-impl01.py` SHA-256 `b86fff14c4787f61a302fc0f801edb9b71b34da970c468e34d9890b9b7075dc2`; target wrapper `run-aucdev023-firstpass-rb001-l1-rb003-pch6-db0324e8-impl01.sh` SHA-256 `0ab7960cf5c5cea74c713c81c0a213729af3d8730deb0e56055b272b17326a8b`; target event `evt-db0324e89c6ef4c7`; target attempts `evt-db0324e89c6ef4c7-A-01` / `evt-db0324e89c6ef4c7-B-01`. Invocation budget: exactly ONE human-direct no-argument wrapper invocation maximum, only after every future admission step.

Future grant properties (MUST include all): ONE-SHOT; NON-TRANSFERABLE; EXACT-TARGET-SPECIFIC; NO RETRY; NO RESUME; NO FALLBACK; NO ALTERNATE DRIVER; NO ALTERNATE WRAPPER; NO ALTERNATE EVENT; NO ALTERNATE ATTEMPT; NO QUALIFICATION AUTHORITY; NO INSTALLATION AUTHORITY.

The exact future human grant phrase, recorded as **DESIGN DATA ONLY**:

```
GRANT AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA006-PCH6-REPLACEMENT-FIRSTPASS-EXEC-20260930-01
```

**Recording this string grants NOTHING.** It becomes operative ONLY if, AFTER (1) this design is canonically published and (2) an independent Control Room readback accepts it, the HUMAN OPERATOR later sends that exact grant as a NEW, separate, explicit, unconditional message. Partial, malformed, conditional, hedged, wrong-ID, copied-from-record or inferred text is NO GRANT. At design time: **HUMAN_OPERATOR_GRANT = NONE**.

## Section 11 — Future authority state machine — DESIGN ONLY (PCHTD-32)

Current state: RESERVED / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE; candidates 0600; PRELAUNCH_MODE_BARRIER CLOSED. After this design's acceptance only: the SAME state — still RESERVED, still 0600, still CLOSED. Only after ALL of: the exact later human grant; every future activation gate PASS; full R-PCH2-CR-1 PASS; candidate restat PASS; the authorized chmod sequence PASS — may the future state become GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED. **This design MUST NOT and does NOT enter that state.** The authority becomes permanently non-reusable from the BEGINNING of the later single human-direct wrapper invocation regardless of later success or failure.

## Section 12 — R-PCH2-CR-1 — future mandatory pre-chmod full-byte gate (PCHTD-33..PCHTD-35)

Current state: `BINDING_FOR_PCH6 / UNREACHED_AT_PRELAUNCH`. **THIS DESIGN DOES NOT SATISFY IT** (Section 8's design-time observations are corroboration only). The future activation session MUST, immediately before any chmod against the THEN-live protected EBS, freshly: (1) resolve the THEN-live EBS identities; (2) verify protected EBS package identity; (3) parse both exact PCH6 bindings; (4) recompute both canonical binding digests; (5) verify exact event/role/attempt/frozen-target relationships; (6) verify package/MANIFEST identities; (7) perform a no-follow independent package walk; (8) reject symlinks/hardlinks/special files; (9) prove exact payload-set equality; (10) re-hash EVERY payload byte for BOTH roles; (11) require every row SHA and size exact; (12) require exact row counts A 191 / B 194; (13) require exact byte totals A 236327843 / B 343459010; (14) verify prompt-contract identity; (15) verify held runtime-component identities; (16) re-derive the required executable set from authoritative bytes/records (the exact executable path table is deliberately NOT hand-transcribed into this design — the one-character-SHA-transcription defect class governs); (17) verify all required executable payload modes; (18) reject any unexpected executable-bit payload; (19) parse and compare ACTUAL ROOT from verified package components (Section 13); (20) run the authoritative then-live package verifier; (21) fail closed on ANY mismatch or error. **PACKAGE_GATE_BEFORE_ANY_CHMOD is mandatory.** No check may be weakened to accommodate observed drift.

## Section 13 — ACTUAL ROOT gate (PCHTD-36..PCHTD-37)

The future activation MUST parse ACTUAL ROOT from all four VERIFIED PCH6 package components required by the accepted mechanism — A `runtime/resource-gate.py`, A `boundary/networked-boundary-launcher.py`, B `runtime/resource-gate.py`, B `boundary/networked-boundary-launcher.py` — mechanically deriving the expected root from governing candidate/package evidence, with all four verified parsed values required to agree with the accepted expected root; a constant-success assertion is FORBIDDEN. Design-time static verification ONLY (this session): the candidate's comparison mechanism remains intact in the exact live bytes — `DEPLOY_ROOT = "/home/isa/aucdev023-s1-prep002-rem002"` (driver L211), `LAUNCHER_REL = "boundary/networked-boundary-launcher.py"` (L247) and `GATE_REL = "runtime/resource-gate.py"` (L248), `strict_roots: True` wired in both role expectation tables (L307/L348) and consumed by `verify_role_generation` (`resource_gate_root` / `launcher_root` records vs `gate_root_expected`, L759–763, invoked at L816); and all four frozen package components currently carry `ROOT = "/home/isa/aucdev023-s1-prep002-rem002"` (read-only design corroboration). **The future live ROOT gate remains UNREACHED and is NOT claimed satisfied.**

## Section 14 — Future canonical Git gate (PCHTD-38)

The future grant/activation task must be bound to the exact Git identity that will exist AFTER this prelaunch design publication AND its independent Control Room readback publication. **This design MUST NOT and does NOT pre-authorize activation against current `a982ee8a…`.** Before any chmod the future session MUST freshly verify: live default branch; exact full authorized HEAD; sole-parent/authorized lineage; trust-anchor ancestry; merge conditions; protected trees; the candidate implementation/readback records; authority reservation/readback; package preparation/readback; THIS design and ITS readback; all applicable pinned-record blobs; exact tracked-change geometry; zero unrelated staged content. Tip drift ⇒ STOP, NO AUTO-REBASE.

## Section 15 — Credential boundary — METADATA ONLY (PCHTD-39..PCHTD-40)

Credential-path logic derived from the exact accepted candidate bytes: environment overrides `AUCDEV_A_CREDENTIAL_FILE` / `AUCDEV_B_CREDENTIAL_FILE` (preferred) with conventional fallbacks A `/home/isa/.claude/.credentials.json` and B `/home/isa/.codex/auth.json`; candidate custody bounds `CREDENTIAL_MIN_BYTES = 1`, `CREDENTIAL_MAX_BYTES = 65536` (EBS custody bound); resolver is METADATA ONLY in the candidate itself (regular non-symlink via lstat; operator-owned; size within bounds; returns path/size/mtime ONLY). Design-time observation: both environment overrides ABSENT in this session; both conventional candidates observed metadata-only — regular, non-symlink, `isa:isa`, mode 0600, nlink 1, A 519 B and B 4231 B, both within the custody bound. **NO open, read, hash, parse, print or copy of credential contents occurred.** These point-in-time observations are NOT future validity proof; the future activation MUST repeat the metadata-only gate. Credential contents may enter an audited attempt only through already-frozen runtime custody mechanics after a later authorized attempt begins.

## Section 16 — Future activation order — DESIGN ONLY (PCHTD-41)

Using the accepted PCH5 prelaunch-transition design/readback as METHOD PRECEDENT ONLY (344-line record at `afd1e693…` cross-checked; no PCH5 identity copied), the exact PCH6 future activation order — 27 fail-closed steps:

1. Fresh live bootstrap at the exact future Control-Room-authorized Git frontier (post this-design-readback SHA).
2. Require a NEW separate exact HUMAN grant message (Section 10 semantics).
3. Verify no prior grant/consumption/invocation for PCH6.
4. Fresh driver restat/hash; require mode 0600 and exact identity.
5. Fresh wrapper restat/hash; require mode 0600 and exact identity.
6. Wrapper pin closure re-verification.
7. Deployed-state invariants re-verification.
8. Fresh PCH6 namespace absence re-verification.
9. Authoritative record/blob pins re-verification.
10. Protected EBS identity resolution (THEN-live).
11. Credentials METADATA ONLY.
12. COMPLETE R-PCH2-CR-1 BOTH-role every-payload-byte gate (Section 12, items 1–21).
13. Candidate driver+wrapper re-stat after all read-only gates (still 0600).
14. ONLY THEN chmod DRIVER 0600 → 0700.
15. Immediate complete driver re-stat/re-hash (exact identity at 0700).
16. ONLY THEN chmod WRAPPER 0600 → 0700.
17. Immediate complete wrapper re-stat/re-hash (exact identity at 0700).
18. Wrapper/driver pin closure after chmod.
19. Exact authority/grant-state assertion.
20. Zero deployment during activation; zero attempt creation; zero AccountingStore mutation.
21. Zero credential-content read during activation.
22. Zero auditor/provider/model execution during activation.
23. Publish activated-state canonical record.
24. Create reviewer handoff only after canonical publication/readback evidence.
25. Return to Control Room.
26. Require independent activation readback.
27. ONLY AFTER that later readback may Control Room consider admission of the single human-direct wrapper invocation.

PCH5-precedent cross-check: every mechanically necessary ordered gate of the accepted predecessor method is present or subsumed (negative invariants appear as steps 20–22 with the AccountingStore/credential/auditor prohibitions explicit; the admission sequencing of predecessor steps 25–27 is refined as steps 25–27 here). **No ordering protection is removed.** Mandatory ordering invariants: `PACKAGE_GATE_BEFORE_ANY_CHMOD`; `DRIVER_THEN_WRAPPER_CHMOD_ORDER`; `IMMEDIATE_POST_CHMOD_REHASH`.

## Section 17 — Partial-chmod fail-closed semantics (PCHTD-42)

If driver chmod succeeds but driver post-chmod verification fails, or wrapper chmod fails, or wrapper post-chmod verification fails, or ANY post-chmod invariant fails, then: STOP. Execute neither candidate. Deploy nothing. Create no attempt. Mutate no AccountingStore. Read no credential contents. Run no auditor/provider/model. No automatic retry. No invented rollback authority. No silent chmod of the driver back to 0600. No continuation to invocation. The exact partial activation state returns to Control Room. **PARTIAL ACTIVATION IS NOT INVOCATION-ELIGIBLE.**

## Section 18 — Deployment / future human invocation (PCHTD-43)

Prelaunch activation MUST NOT deploy PCH6. Deployment remains INSIDE the later single HUMAN-OPERATOR-DIRECT wrapper invocation, which must be: human-direct; no-argument; exactly once maximum; no helper; no scheduler; no automation; no agent invocation; no direct driver invocation; no alternate shell substitute. The execution authority becomes permanently non-reusable at invocation BEGIN, regardless of wrapper precheck failure, Python startup, durable marker creation, deployment success/failure, attempt creation, provider engagement, or report outcome. Carried forward UNCHANGED: `PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP` — marker absence MUST NEVER restore authority when invocation is known to have been attempted. This design does NOT remediate that residual absent new evidence.

## Section 19 — Sealed historical artifacts — identity-only forever (PCHTD-44)

Auditor-A frozen report `b63722154417e3bbbd8819853d4a4830bcbe20d5b49523dac274a1a7b8ead24e` / 27051 B / 0444 and Auditor-B invalid snapshot `5a4b49cfa2810eb45faa2e206a931b750dde17722c9209496de47acd97e8671f` / 822 B / 0600 remain IDENTITY-ONLY forever within this governance: never opened, parsed, grepped, decoded, sampled, quoted, copied, substance-inferred or fed to any model; excluded BY NAME from every content scan. The PCH5 persisted coverage value(s), the historical PCH4 wrong target_commit literal and the historical PCH3 wrong attempt_id value remain UNKNOWN and uninferred.

## Section 20 — Held governance / residuals carried (PCHTD-45)

Preserved EXACTLY: AUCDEV-023 P1 / READY / NOT DONE; queue counts READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11; no backlog item marked DONE; two-conforming-first-pass set INCOMPLETE; audit completeness INCOMPLETE; qualification NONE; installation NONE; installed source `8ae33444f349ce73c1359b963722e2d16acba630` with installed-qualified provenance NOT ESTABLISHED; PCH6 authority RESERVED / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE with EXECUTION_GRANT NONE; R-PCH2-CR-1 BINDING_FOR_PCH6 / UNREACHED_AT_PRELAUNCH; PCH6 event PREPARED_ONLY; packages PREPARED / FROZEN / NON-DEPLOYED; EXEC-RA-006 ROOT_CAUSE_NOT_ESTABLISHED with the PCH5 persisted coverage value(s) UNKNOWN and uninferred; Option-B DEFENSE_IN_DEPTH_ONLY with CAUSALITY_NOT_ESTABLISHED. Carried APPEND-ONLY: `PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP`; `AUCDEV023-CR-PCH5-PLTD-001`; `AUCDEV023-CR-PCH5-REM-001`; `AUCDEV023-CR-PCH5-GPL-001`; `AUCDEV023-CR-PCH5-EMRB-001`; EXEC-RA-006 DRB-001/002/003; `PCH6-CR-PREP-001/-002/-003`; `PCH6-CR-LDES-RB-001`; `PCH6-CR-RES-001` (CLOSED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH WITH HOST_REWALK_LIMITATION); `PCH6-CR-IMPL-RB-001`; `CONTROL_ROOM_TASKING_INPUT_DEFECT`; plus the NEW `PCH6-CR-IMPL-RB-PUB-001` and `PCH6-CR-IMPL-RB-PUB-002` recorded by this design (Section 6). No historical record is rewritten.

## Section 21 — Session transients (recorded honestly, WITHOUT erasure) (PCHTD-46)

All instrument-side; NONE a driver/wrapper/EBS/product defect; NO failed observation was rewritten as PASS without a corrected re-derivation; every first output is preserved verbatim in the untracked evidence workspace:

- T-1 candidate-restat v1 `stat %F` under the host's Turkish locale returned `normal dosya`, failing the two REGULAR assertions while every substantive observation (mode/size/SHA/owner/lines) was correct; corrected v2 under `LC_ALL=C` (02b).
- T-2 residual-bases v1 used a naive `T-1[0-3]` regex that misclassified quoted PCH6-CR-IMPL-RB-001 basis-D text (`T-1..T-12` / `T-1..T-15`) as session transients and missed line-format differences; corrected by scoped re-derivations.
- T-3 residual-bases v2's sentence-leading anchor was too narrow (T-1/T-2 follow `:`/`.` separators); corrected v3 strips the two quoted range expressions before enumeration, yielding exactly T-1..T-9.
- T-4 S4 v1 attribution labels were shifted by the session zsh's 1-indexed arrays (labels off by one; the union traversal itself was valid); corrected v2 under `bash` with 0-indexed arrays and stable instrument-file placement.
- T-5 package-reverify v1 subtracted 1 from `verify_event_package`'s `files` count (which already equals the payload row count); corrected by a direct MANIFEST row census; the geometry observations were never wrong.

## Section 22 — Design disposition and publication safety (PCHTD-47..PCHTD-48)

Disposition (Section 21 of the tasking, held equivalent in substance):

```
PCH6_REPLACEMENT_PRELAUNCH_TRANSITION_DESIGN =
PREPARED_AT_CONTROL_ROOM_PRELAUNCH_TRANSITION_DESIGN_STRENGTH /
CONTROL_ROOM_ACCEPTED_IMPLEMENTATION_CANDIDATES_BOUND /
LIVE_HOST_DRIVER_WRAPPER_0600_REVERIFIED /
PRELAUNCH_MODE_BARRIER_CLOSED /
RESERVED_AUTHORITY_NOT_GRANTED_NOT_CONSUMED_NOT_EXECUTABLE /
EXACT_FUTURE_HUMAN_GRANT_TARGET_DEFINED /
HUMAN_OPERATOR_GRANT_NONE /
FUTURE_ONE_SHOT_AUTHORITY_STATE_MACHINE_DEFINED /
R_PCH2_CR_1_BINDING_UNREACHED /
FUTURE_FULL_BOTH_ROLE_EVERY_PAYLOAD_BYTE_GATE_DEFINED /
PACKAGE_GATE_BEFORE_ANY_CHMOD /
ACTUAL_ROOT_GATE_DEFINED /
FUTURE_EXACT_GIT_FRONTIER_GATE_DEFINED /
CREDENTIAL_METADATA_ONLY_GATE_DEFINED /
DRIVER_THEN_WRAPPER_CHMOD_ORDER_DEFINED /
IMMEDIATE_POST_CHMOD_REHASH_REQUIRED /
PARTIAL_CHMOD_FAIL_CLOSED_SEMANTICS_DEFINED /
DEPLOYMENT_REMAINS_INSIDE_SINGLE_HUMAN_DIRECT_INVOCATION /
PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP_CARRIED /
PCH6_CR_IMPL_RB_PUB_001_002_RECORDED /
ZERO_GRANT /
ZERO_CHMOD /
ZERO_DEPLOYMENT /
ZERO_RUNTIME /
NO_EXECUTION_READINESS /
NO_PRELAUNCH_ADMISSION /
NO_QUALIFICATION /
NO_INSTALLATION /
READY_FOR_INDEPENDENT_CONTROL_ROOM_PRELAUNCH_DESIGN_READBACK
```

This is DESIGN strength ONLY. Publication safety: live master re-resolved EXACT at `a982ee8ab725d11038ed10cb791e4a64ebbe604e` immediately before staging and again immediately before commit; `git diff --check` PASS and staged diff `--check` PASS; staged EXACTLY the three allowed documentation paths (this NEW canonical design record + M `AUCDEV-CURRENT-STATE.md` + M `AUCDEV-BACKLOG.md`); the evidence workspace, sweep instruments, input handoff archive, candidates and every design artifact remain UNTRACKED host artifacts NOT staged; no candidate file, no source/runtime/package path, no credential path committed; protected trees held EXACT in the staged write-tree; the pre-existing smoke-fixture gitlink rows preserved NOT staged; CURRENT built from the EXACT LIVE base blob `2002330d75a5d09d60982cb0ba0a0370d8253049` with the rotation confined exactly to lines 3/11/23-25 + one dated record appended with blank separator (non-rotated lines byte-identical, 1103 → 1105 lines, script-asserted at build AND re-asserted from the staged blob with the changed-line set exactly [3, 11, 23, 24, 25]); BACKLOG purely additive one dated record with blank separator (2738 → 2740 lines, prefix byte-identical, script-asserted at build AND from the staged blob); hex-literal gate PASS over the new canonical record in full and all changed/appended CURRENT/BACKLOG lines (every 40/64-hex literal machine-verified against the session-derived identity set; zero unknown; zero bad-length; the PUB-002 malformed 37-hex token is recorded AS malformed and is not an operative identity); exactly ONE bounded docs-only fast-forward commit whose sole parent is `a982ee8ab725d11038ed10cb791e4a64ebbe604e`; exactly ONE push; post-push live master == local new HEAD EXACT with the design record, CURRENT and BACKLOG fetched back from GitHub at the new SHA and Git blob equality verified; the generated-LAST reviewer handoff is produced AFTER this push and the post-push readback with nothing included mutated afterward.

## Section 23 — Design acceptance matrix

| # | Check | Result |
|---|---|---|
| PCHTD-01 | Live master == local HEAD == `a982ee8ab725d11038ed10cb791e4a64ebbe604e` at bootstrap | PASS |
| PCHTD-02 | Root tree `9491aed9acebf42bf1d8efde5a3b96d165a1b7dc` + sole parent `9ed1db1d03ff3c64a02b5713cc95bdec1cf89990` | PASS |
| PCHTD-03 | TEN required canonical blobs EXACT at HEAD | PASS |
| PCHTD-04 | Canonical design path ABSENT (rc 128 + never-existent control rc 128; zero history rows) | PASS |
| PCHTD-05 | Protected trees EXACT, zero drift; anchor rc 0; zero merges; zero staged; smoke-fixture rows preserved | PASS |
| PCHTD-06 | Driver fresh restat: regular non-symlink isa:isa 171086 B / 3425 lines / 0600 / SHA exact (double hash) | PASS |
| PCHTD-07 | Wrapper fresh restat: regular non-symlink isa:isa 3468 B / 82 lines / 0600 / SHA exact (double hash) | PASS |
| PCHTD-08 | Executable bits ZERO both candidates → PRELAUNCH_MODE_BARRIER CLOSED | PASS |
| PCHTD-09 | Archive-member mode NOT substituted for live-host restat (restat performed fresh in THIS session) | PASS |
| PCHTD-10 | Wrapper pins: DRIVER path / REQUIRED_DRIVER_SHA256 / REQUIRED_DRIVER_MODE="700" exact | PASS |
| PCHTD-11 | Wrapper fail-closed mechanics preserved (umask/PATH/root-refusal/symlink/ownership/mode/hash gates; exec /usr/bin/python3 -I) | PASS |
| PCHTD-12 | Reserved authority state unchanged: RESERVED / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE; EXECUTION_GRANT NONE | PASS |
| PCHTD-13 | Input readback handoff identity 1e49db18… / 1083239 B EXACT | PASS |
| PCHTD-14 | Census 54 regular / 0 links / 0 specials / 0 executable; SHA256SUMS 53/53 exact payload-set equality; zero sealed/credential members | PASS |
| PCHTD-15 | 13-genlast-report.json present (transient_count 9); README == ledger == T-1..T-9; four canonical members non-zero Git-blob equal | PASS |
| PCHTD-16 | PCH6-CR-IMPL-RB-PUB-001 bases A–D independently confirmed; classification recorded append-only | PASS |
| PCHTD-17 | PCH6-CR-IMPL-RB-PUB-002 bases confirmed (actual parent exact; 37-hex malformed token unresolvable; BACKLOG row present; record correct) | PASS |
| PCHTD-18 | CONTROL_ROOM_TASKING_INPUT_DEFECT family preserved append-only; no history rewritten | PASS |
| PCHTD-19 | Collision sweep S1/S2/S3: eight identities + guard ZERO | PASS |
| PCHTD-20 | S4 single multi-pattern traversal: identities + guard GOVERNED_SELF-confined; sanity x187 known-present | PASS |
| PCHTD-21 | S5/S6/S7 (full-depth, no pruning, rc 0, stderr empty; census 2,236,448 / edee41a5…) identities ZERO except evidence-workspace self | PASS |
| PCHTD-22 | S8/S9/S10 deployed root clean; PCH6 runtime + invocation-marker namespace ABSENT; name liveness probes discriminate | PASS |
| PCHTD-23 | Selection file + selection.json: event/attempt identities exact | PASS |
| PCHTD-24 | Binding files re-hashed exact; parse_binding geometry exact both roles | PASS |
| PCHTD-25 | Canonical binding digests recomputed EXACT through live EBS parser; binding pins exact | PASS |
| PCHTD-26 | verify_event_package PASS both roles at exact geometry (191/236327843; 194/343459010); prompt contract x5 copies exact; profiles exact | PASS |
| PCHTD-27 | Deployed event root EXACTLY 4 entries | PASS |
| PCHTD-28 | Attempts EXACTLY 35 / 76 files; backups ELEVEN; staging ZERO; bindings re-hashed unchanged | PASS |
| PCHTD-29 | Fresh PCH6 runtime identity / candidate basenames / invocation markers ABSENT at any depth | PASS |
| PCHTD-30 | Exact future grant target defined with all required one-shot properties; invocation budget ONE | PASS |
| PCHTD-31 | Grant phrase recorded as DESIGN DATA ONLY; HUMAN_OPERATOR_GRANT = NONE | PASS |
| PCHTD-32 | Future authority state machine defined; activation state NOT entered | PASS |
| PCHTD-33 | R-PCH2-CR-1 BINDING_FOR_PCH6 / UNREACHED; this design does NOT satisfy it | PASS |
| PCHTD-34 | Future 21-item full both-role every-payload-byte pre-chmod gate defined; executable table NOT hand-transcribed | PASS |
| PCHTD-35 | PACKAGE_GATE_BEFORE_ANY_CHMOD mandatory invariant defined | PASS |
| PCHTD-36 | ACTUAL ROOT four-component gate defined; constant-success assertion forbidden | PASS |
| PCHTD-37 | Candidate ROOT-comparison mechanism statically intact; four components agree at design time; future live gate UNREACHED | PASS |
| PCHTD-38 | Future canonical Git frontier gate defined; no pre-authorization against a982ee8a | PASS |
| PCHTD-39 | Credential logic derived from candidate bytes; metadata-only observation recorded (env absent; 519/4231 B within 1..65536; contents untouched) | PASS |
| PCHTD-40 | Future metadata-only gate repetition required; custody-mechanics-only content path preserved | PASS |
| PCHTD-41 | Exact 27-step future activation order defined with the three mandatory ordering invariants; PCH5 method-precedent cross-check complete | PASS |
| PCHTD-42 | Partial-chmod fail-closed semantics defined; partial activation NOT invocation-eligible | PASS |
| PCHTD-43 | Deployment confined to the single future human-direct invocation; consumption-at-BEGIN semantics; marker-gap residual carried | PASS |
| PCHTD-44 | Sealed artifacts identity-only; unknown values remain uninferred | PASS |
| PCHTD-45 | Held governance + full residual set carried append-only (including the two new PUB residuals) | PASS |
| PCHTD-46 | Session transients T-1..T-5 recorded honestly with first outputs preserved | PASS |
| PCHTD-47 | Design disposition recorded at DESIGN strength only | PASS |
| PCHTD-48 | Publication safety: three-path staging, rotation/additive proofs, hex-literal gate, one commit/one push/post-push equality | PASS |

## Section 24 — Exactly one next action

**INDEPENDENT CONTROL ROOM READBACK OF THE PCH6 REPLACEMENT PRELAUNCH TRANSITION DESIGN AND ITS GENERATED-LAST HANDOFF, STRICTLY BEFORE ANY HUMAN EXECUTION-AUTHORITY GRANT, CHMOD, PRELAUNCH ACTIVATION, DEPLOYMENT OR RUNTIME.** Until that readback is accepted: NO human execution-authority grant; NO chmod; NO prelaunch activation; NO deployment; NO runtime; NO authority consumption.

## Section 25 — Never list (binding on this record)

Never grant or consume the reserved PCH6 authority on the strength of this design. Never treat the recorded grant phrase as a grant. Never chmod either candidate to 0700 inside a design session. Never execute/import the driver or execute/source the wrapper. Never deploy the PCH6 event, create attempts, or mutate AccountingStore. Never read credential contents. Never execute a real auditor or provider/model. Never open either historical real report artifact (`b6372215`/27051/0444 and `5a4b49cf`/822/0600 remain identity-only forever within this governance). Never infer the actual invalid Auditor-B coverage value(s), the PCH4 wrong target_commit literal or the PCH3 wrong attempt_id value. Never hand-transcribe executable path tables or operative SHAs (machine-derived values govern). Never claim the Option-B hardening fixes the historical failure. Never claim remediation, qualification or installation. Never claim this design satisfies R-PCH2-CR-1 or opens the mode barrier. Never invent substance for OPERATOR_REPORTED T-10..T-13. Never rewrite historical records, matrices, prompts or evidence workspaces (append-only). Never rerun the launcher. Never retry/resume/fallback/reconcile.
