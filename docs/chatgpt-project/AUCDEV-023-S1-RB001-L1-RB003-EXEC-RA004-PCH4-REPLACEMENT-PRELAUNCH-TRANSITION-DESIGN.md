# AUCDEV-023 — S1 RB-001 L1 RB-003 EXEC-RA-004 / PCH-004 — Replacement Prelaunch Transition Design

Design authority: `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA004-PCH4-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN-20260928-01`
Date: 2026-09-28 (Europe/Istanbul)
Exact live base: `e22bbd4312ee3afb7a912aa2581edccc44790876` (live master == local HEAD EXACT at bootstrap; re-resolved EXACT immediately before staging and again immediately before commit)
Root tree: `2b829173b62f9fd80414c91ea65434069a6577be`; sole parent: `021175a9fd70343aba4d83ad787d0ba9f2681763`

## Section 0 — Role, boundary and zero-runtime attestation (PLTD4-47)

This session is the BOUNDED PCH4 REPLACEMENT PRELAUNCH TRANSITION DESIGNER and READ-ONLY MECHANICAL EVIDENCE COLLECTOR. It designs — and does NOT perform — the transition from the accepted PCH4 0600 NON-EXECUTABLE launcher candidates to a possible FUTURE, separately human-granted, chmod-only activated, single-use execution lifecycle.

NOT: the human operator issuing an execution grant; a grant publisher; a prelaunch activator; a launcher executor; a deployment authority; an execution controller; an execution-authority grantor; Auditor-A or Auditor-B; an /audit-council runner; a credential-content reader; a provider/model execution authority; a qualification authority; an installation authority.

ZERO RUNTIME in this session: execution grant NONE; candidate chmod NONE; candidate execution/import/sourcing NONE (both candidates read as STATIC TEXT only; wrapper never sourced; driver never imported); deployment NONE; staging/backup runtime transition NONE; attempt creation NONE; AccountingStore mutation NONE; credential-content reads NONE (metadata-only lstat/stat; neither credential file opened, read, hashed, parsed, printed or copied); sealed-report substance reads NONE (both sealed predecessor artifacts verified path/lstat/stat/SHA-256/size/mode identity-ONLY, never opened/parsed/sampled/quoted/decoded/copied); the actual persisted wrong PCH3 attempt_id value NOT inspected and NOT inferred and remains UNKNOWN by design; auditor/provider/model executions ZERO; /audit-council execution ZERO; execution authority NONE granted and NONE consumed (the exact reserved authority remains RESERVED / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE); qualification NONE; installation NONE.

Permitted local computation: live Git/bootstrap reads; read-only hashing/stat/census; candidate lstat/stat/hash and static text inspection; JSON parsing of non-report governance/binding/MANIFEST/accounting-state files; parsing via the exact live protected EBS modules (`bootstrap-supervisor/ebs/binding.py`, `bootstrap-supervisor/ebs/launch.py` at the exact base); input-handoff read-only tar verification with ZERO members executed; evidence-workspace writes; docs-only publication. Network: the mandated bootstrap `git ls-remote`, the pre-staging AND pre-commit live re-resolves, the single push of this publication, and the post-push readback ONLY.

## Section 1 — Exact live bootstrap (PLTD4-01..PLTD4-05)

- `git ls-remote origin` at bootstrap: default branch `master`; live master `e22bbd4312ee3afb7a912aa2581edccc44790876` == local HEAD EXACT == expected baseline EXACT.
- Root tree `2b829173b62f9fd80414c91ea65434069a6577be`; `git rev-list --parents -n 1 HEAD` gives sole parent `021175a9fd70343aba4d83ad787d0ba9f2681763` EXACT (exactly one parent).
- Canonical blobs at this exact base verified EXACT (all read at that exact SHA):
  - `AUCDEV-CURRENT-STATE.md` `cc2fb3163431ba0e284c45311875e45dd145af8e`;
  - `AUCDEV-BACKLOG.md` `7cecdf9f5c7153057489132433480b56e274bc53`;
  - PCH4 implementation record `91511f36bcd4c44e4997aff4943c5b167f7807cb`;
  - PCH4 implementation Control Room readback `550a0b469a9b0fa8bded2e1a4a2ee81b2deb8720`;
  - PCH4 reservation Control Room readback `398cdbb880846f2d12f7b9b9cecb3d0053891ee3`;
  - PCH4 rebind/adaptation design `d763f3d0fb83a8a986e61ce559b4d62ab2f929b0`;
  - PCH4 rebind/adaptation design Control Room readback `ac8375075d649afc46bd7827344f4129ea929209`.
- Protected trees at the exact base ALL EXACT: `bootstrap-supervisor` `732b8def9f22d7c466ce77f3d3049da53bfff3d0`; `qualification-harness` `5b8d5e5465923740470ff63ed9b8683f257a3787`; `skill` `c792933a862d9a5434681a88d183470dd8b15d2f`.
- Tracked working-tree drift: limited to the pre-existing `smoke-fixture` / `smoke-fixture-103` gitlink rows (outside governed paths), preserved and NOT staged.
- Live master re-resolved EXACT immediately before staging and again immediately before commit; tip drift would STOP with NO edit and NO auto-rebase.

## Section 2 — Input implementation-readback handoff verified READ-ONLY (PLTD4-06..PLTD4-11)

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA004-PCH4-REPLACEMENT-OPERATOR-LAUNCHER-IMPLEMENTATION-CONTROL-ROOM-READBACK-HANDOFF-20260928-01.tar.gz`

- outer SHA-256 `398fbc3967e00ab198dd33a9462801a07d2bf52916803114d0f3c88b576ffeae`; size 999156 B EXACT; regular, non-symlink, isa:isa.
- census EXACT: 44 members = 37 regular files (36 payload + exactly 1 SHA256SUMS) + 7 directories; 0 symlinks; 0 hardlinks; 0 specials; 0 unsafe/traversal; 0 duplicate names.
- checksums: exactly 36 rows, 36/36 PASS by `LC_ALL=C sha256sum -c`; exact payload-set equality: 0 missing, 0 unlisted.
- canonical members byte-equal to the exact live Git blobs (trailing final LF `0x0a` verified at byte level on all three): implementation CR readback `550a0b46…`; CURRENT `cc2fb316…`; BACKLOG `7cecdf9f…`.
- handoff candidate copies hash-identical to the live host candidates: driver copy `5b946a1b…`; wrapper copy `03ad514b…`.
- ZERO members byte-equal to either sealed PCH3 report identity; ZERO credential material.
- ZERO archive members executed, sourced, imported or otherwise run.

## Section 3 — Design publication identity collision sweep BEFORE first use (PLTD4-12)

Four exact identities swept BEFORE first use, fail-closed (rc taxonomy 0 = matches / 1 = none / >=2 = SCAN ERROR; every command's exit status checked; stderr captured separately per surface, zero suppression, required empty; `find` without `-L`):

- T1 authority `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA004-PCH4-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN-20260928-01`;
- T2 canonical record path `docs/chatgpt-project/AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA004-PCH4-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN.md`;
- T3 evidence workspace `aucdev023-exec-ra004-pch4-prelaunch-transition-design-evidence`;
- T4 generated-LAST handoff `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA004-PCH4-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN-HANDOFF-20260928-01.tar.gz`.

Surfaces: A tracked tree at exact HEAD (`git grep -F` at `HEAD`); B full git history `--all` exact-string pickaxe; C commit messages fixed-string; D working-tree contents excluding `.git` and the own evidence workspace (recorded self-reference exclusion) with sealed `*first-pass-report*` files excluded by basename; E repository-root names (own evidence workspace excluded, recorded); F `/home/isa` top-level names; G deployed launcher-root `/home/isa/aucdev023-s1-prep002-rem002` path names AND contents excluding sealed `*first-pass-report*` files.

**RESULT: COLLISION_COUNT = 0 AND SCAN_ERROR_COUNT = 0** (32 surface-token rows; zero stderr bytes; sweep script + verbatim output preserved in the evidence workspace). No alternate identities invented.

## Section 4 — Accepted PCH4 candidates — fresh LIVE-HOST restat (PLTD4-13..PLTD4-17)

Driver `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch4-e7f217c5-impl01.py`:
SHA-256 `5b946a1bf8d5275dbf46a0a18765b77dd504f76330c89184d6f7acbb42a22ea8`; size 170138 B EXACT; 3410 lines EXACT; regular; non-symlink; owner isa:isa; mode EXACTLY 0600; executable bits ABSENT.

Wrapper `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch4-e7f217c5-impl01.sh`:
SHA-256 `03ad514b9f73422e05bdf011f2b3fd717fa702e04b698a741732a9ca86ac7872`; size 3468 B EXACT; 82 lines EXACT; regular; non-symlink; owner isa:isa; mode EXACTLY 0600; executable bits ABSENT.

**PRELAUNCH_MODE_BARRIER = CLOSED** — both candidates remain 0600 while the wrapper requires `REQUIRED_DRIVER_MODE="700"`; no human-direct invocation is mechanically admitted in this state (a hypothetical invocation would be refused by the wrapper's exact-mode precheck before anything executes).

Wrapper static pin verification (text read only; NEVER sourced):
- `DRIVER="/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch4-e7f217c5-impl01.py"` exact absolute path;
- `REQUIRED_DRIVER_SHA256="5b946a1b…"` — THREE-WAY SHA closure EXACT: wrapper pin == live candidate re-hash == input-handoff candidate copy;
- `REQUIRED_DRIVER_MODE="700"` — intentional fail-closed refusal at the present 0600;
- control mechanics held: `set -euo pipefail`; `set +x` never enabled; `umask 077`; `ulimit -c 0` fail-closed; xtrace-env clearing; `PATH=/usr/bin:/bin` pinned BEFORE any external call; root refusal; symlink refusal; regular-file check; owner check; exact mode+SHA pre-exec checks; `PYTHONPATH/PYTHONHOME/PYTHONSTARTUP` unset; `exec /usr/bin/python3 -I "$DRIVER"` with NO positional forwarding; ZERO report logic; ZERO deployment logic; parse-only check (`bash -n`) consistent with prior accepted sessions; the wrapper was NEVER executed or sourced by this session.

## Section 5 — Current deployed predecessor geometry (PLTD4-18..PLTD4-25)

Deploy root `/home/isa/aucdev023-s1-prep002-rem002`; current deployed predecessor event `evt-2b618b6e2fccb80a`. Freshly re-derived identity-only:

- attempt census EXACTLY 31 attempt roots;
- historical backup census EXACTLY NINE names: `event.backup.pre-exec02`, `event.backup.pre-exec03-new-event`, `event.backup.pre-pch1-replacement-event`, `event.backup.pre-pch2-replacement-event`, `event.backup.pre-pch3-replacement-event`, `event.backup.pre-rb001-l1-successor-event`, `event.backup.pre-rb002-successor-event`, `event.backup.pre-rb003-corrected-successor-event`, `event.backup.pre-successor-event`;
- staging: ZERO `event.staging.*`.

Auditor-A predecessor attempt `evt-2b618b6e2fccb80a-A-01`: accounting SHA-256 `6349f9afc1813fb8d61ed0cfd8d7cfe88a44ef54cb86cd67ab17acc30be0cf74` / 5616 B / mode 0600 EXACT; state sequence EXACT `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_FROZEN → TERMINAL`; custody-out census EXACTLY the sealed report `evt-2b618b6e2fccb80a-A-01.first-pass-report.json` — SHA-256 `5b73bc81ea48a614982f82511c0e46655901fde820114d6c5cf7725ec93c1d3c` / 30169 B / mode 0444, verified IDENTITY-ONLY (path/lstat/stat/SHA-256/size/mode; never opened/parsed/sampled/quoted/decoded/copied).

Auditor-B predecessor attempt `evt-2b618b6e2fccb80a-B-01`: accounting SHA-256 `8881e281b2d8e0a13ea38f59b3ff9e433d0b4a35170814bdf32ba01fdecf15e5` / 5666 B / mode 0600 EXACT; state sequence EXACT `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_INVALID → TERMINAL`; custody-out EMPTY EXACT; staging census EXACTLY the sealed invalid snapshot `evt-2b618b6e2fccb80a-B-01.first-pass-report.json` — SHA-256 `f3babc7d29717e06ba8d9b6bce2bbda6257a4bd0462c7317a688a2c066bac1c8` / 907 B / mode 0600, verified IDENTITY-ONLY, never opened.

**SEALED BLINDNESS HELD**: the actual persisted wrong PCH3 attempt_id value was NOT inspected and NOT inferred and remains UNKNOWN.

## Section 6 — Fresh PCH4 runtime namespace PRISTINE (PLTD4-26, PLTD4-27)

Read-only absence, with nothing deleted/normalized/renamed/reused to create absence:

- ZERO `evt-e7f217c5*` paths anywhere under the deploy root (fresh event `evt-e7f217c5675fd9d1` remains PREPARED_ONLY);
- ZERO `event.staging.rb001-l1-rb003-e7f217c5-pch4`; ZERO `event.backup.pre-pch4-replacement-event`;
- ZERO `pch4-e7f217c5-impl01-run-evidence` runtime namespace (repo + deploy root);
- ZERO authority-bound mechanical runtime handoff: the NINE `*MECHANICAL-HANDOFF.tar.gz` names present at the repository root are ALL historical convention-named handoffs of prior published stages (EXEC chains through PCH3, each enumerated and classified in the evidence workspace); ZERO paths anywhere matching the PCH4 reserved-authority-bound derivation `*PCH4-REPLACEMENT-FIRSTPASS-EXEC*MECHANICAL-HANDOFF*`;
- repository-root `e7f217c5` artifacts: EXACTLY the two accepted candidates, nothing else;
- ZERO grant/consumption/runtime-authority artifact anywhere swept.

## Section 7 — Exact reserved PCH4 execution authority (PLTD4-28)

Verified byte-exact from the canonical reservation Control Room readback record `398cdbb8…` at the exact base (and consistent with CURRENT-STATE):

- `PCH4_FUTURE_EXECUTION_AUTHORITY_ID = AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA004-PCH4-REPLACEMENT-FIRSTPASS-EXEC-20260928-01`;
- `PCH4_EXECUTION_AUTHORITY = RESERVED / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE`;
- `EXECUTION_GRANT = NONE`.

THIS DESIGN DOES NOT MUTATE THIS STATE. The reservation is an IDENTITY RESERVATION ONLY; it is NOT an execution grant; it is NOT consumed by this design; consumption can occur ONLY inside the single human-direct invocation of a FUTURE, separately activated launcher after its own readback, the exact human grant, grant/prelaunch activation and the R-PCH2-CR-1 gate. No old authority transfers (PCH3 authority `…-EXEC-RA003-PCH3-REPLACEMENT-FIRSTPASS-EXEC-20260927-01` remains CONSUMED / TERMINAL / CLOSED / NO_RERUN, engagements 2/2).

## Section 8 — Exact future human grant target — DESIGN ONLY (PLTD4-29, PLTD4-30)

| Target element | Exact value |
|---|---|
| Driver | `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch4-e7f217c5-impl01.py` (SHA `5b946a1b…`, 170138 B) — required pre-grant/pre-activation mode 0600 |
| Wrapper | `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch4-e7f217c5-impl01.sh` (SHA `03ad514b…`, 3468 B) — required pre-grant/pre-activation mode 0600 |
| Event | `evt-e7f217c5675fd9d1` |
| Attempts | `evt-e7f217c5675fd9d1-A-01`, `evt-e7f217c5675fd9d1-B-01` |
| Maximum inference-capable engagements | 2 TOTAL |
| Ordering | Auditor-A FIRST; Auditor-B ONLY after mechanically conforming Auditor-A completion |
| Invocation budget | exactly ONE human-direct wrapper invocation maximum |

Properties: ONE-SHOT; NON-TRANSFERABLE; EXACT-TARGET-SPECIFIC; NO RETRY; NO RESUME; NO FALLBACK; NO ALTERNATE DRIVER; NO ALTERNATE WRAPPER; NO ALTERNATE EVENT; NO ALTERNATE ATTEMPT; NO QUALIFICATION AUTHORITY; NO INSTALLATION AUTHORITY.

Exact future grant phrase (defined; **recording it here grants NOTHING**):

```
GRANT AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA004-PCH4-REPLACEMENT-FIRSTPASS-EXEC-20260928-01
```

It may become operative ONLY if the HUMAN OPERATOR later sends that exact line as a NEW, separate, explicit message AFTER (1) this design is published and (2) an independent Control Room readback accepts the design. Malformed, partial, conditional, hedged, wrong-ID or wrong-target text produces NO GRANT.

## Section 9 — Authority state machine — DESIGN ONLY (PLTD4-31)

| State | Condition | Value |
|---|---|---|
| STATE 1 — NOW | (this design; no grant) | RESERVED / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE |
| STATE 2 | after a FUTURE separate exact human grant, before chmod | GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_NOT_YET_ACTIVATED |
| STATE 3 | after successful FUTURE chmod-only activation | GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED |
| STATE 4 | at BEGINNING of the eventual human-direct wrapper invocation | CONSUMED / NON_REUSABLE |
| STATE 5 | after invocation terminates/stops | CONSUMED / TERMINAL / CLOSED / NO_RERUN |

STATE-4 consumption occurs regardless of whether: wrapper prechecks complete; Python starts; driver invocation evidence exists; deployment happens; attempts are created; AccountingStore exists; credentials are read; dynamic gates run; a provider starts; inference occurs. Unused engagement capacity NEVER restores authority.

## Section 10 — R-PCH2-CR-1 future full package-byte gate — DEFINED, NOT CLOSED, NOT CONSUMED (PLTD4-32..PLTD4-37)

R-PCH2-CR-1 remains **BINDING_FOR_PCH4**. THIS DESIGN DEFINES THE GATE; THIS DESIGN DOES NOT CLOSE OR CONSUME IT. The gate MUST be freshly executed by a later, separately authorized HUMAN-GRANT / PRELAUNCH ACTIVATION session BEFORE ANY chmod. Inventories and top-level package digests alone are INSUFFICIENT.

Governing EBS identity (verified THIS session through the live protected module itself, `ebs.launch.verify_package_identity` on the protected `bootstrap-supervisor` tree at the exact base — full per-file byte verification PASS):

- MANIFEST SHA-256 `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999`;
- package SHA-256 `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8`.

(The historical malformed transcription `…e93e922f8` governs NOTHING.)

For BOTH PCH4 roles the future gate MUST: 1. resolve the exact then-live protected EBS identity; 2. verify its protected-tree identity; 3. reproduce/verify the exact governing EBS package identity; 4. load the exact then-live EBS verifier semantics — no copied approximation; 5. parse the exact binding; 6. recompute the canonical digest; 7. run exact `verify_event_package` semantics; 8. independently walk the package tree with `followlinks=false`; 9. refuse symlinks; 10. refuse hardlinks where prohibited by the package contract; 11. refuse special files/traversal; 12. require exact payload-set equality with the MANIFEST; 13. re-hash EVERY payload byte; 14. require EVERY row SHA and size; 15. require exact row count; 16. require exact payload byte total; 17. require exact package and MANIFEST identities; 18. require event/role/attempt/frozen-target relations; 19. require prompt-contract and held-component identities; 20. require the exact accepted executable-set contract and mode 0555; 21. perform and record ACTUAL live ROOT comparisons from verified package bytes. BOTH roles PASS or STOP BEFORE chmod.

Expected PCH4 package identities (design-strength verification THIS session: bindings parsed via the exact live EBS parser; canonical digests recomputed; event/attempt derivations reproduced via `ebs.binding.attempt_id_for`; MANIFEST row counts and payload byte totals recomputed; package/manifest pins pin-equal; contract copies re-hashed inside both packages):

| Identity | Auditor-A | Auditor-B |
|---|---|---|
| binding SHA-256 | `20cca3226a7b052f887658f2e24cea174f5804246527c38f0460c6c50caf628d` | `c9bdc12cec8705cca27e180423a245881659e30c5c6c387039830224284cb790` |
| canonical digest | `7de9eccd83fdbf811cb309af46570b55e9bb2726f4f693eea0c275867683f0c9` | `9831aa95fcc7a920d68674b8a07b6a77f804762ce278405bacbc1863720d411b` |
| MANIFEST SHA-256 | `fb3b8083ed69bc9f6d1ee132f265d18122fc822bb7e83a57df74af56d4cb804c` | `d844e5cfc62b08d6c483645e20f03d3a8e8dc96d53f967fdfc71a911a085b108` |
| package SHA-256 | `0b25ccda257df240972c5beb16844699b302ef0c9692941401aa6fe95052f6ff` | `a5369a16aec7ef63eef64410606d298fe75f72e355330f12632e2e068f61377c` |
| rows | 191 | 194 |
| payload bytes | 236324841 | 343456370 |

Prompt contract `bc9d14824780606df8c3efbdeb397dbfb5a223ee83241e7f48fc33412697db02` — re-hashed THIS session EXACT at all four fresh-package copies (`payload/evidence/common/prompt-contract.json`, `transport/prompt-contract.json` in BOTH packages). Frozen target commit `d4d584ffa47ad2848268ba947247f81a845b2322` (type `commit`, present in the repository; pinned in both fresh bindings with the exact protected subtrees).

Held components re-hashed THIS session EXACT inside BOTH fresh packages (identical across roles): `boundary/networked-boundary-launcher.py` `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa`; `runtime/resource-gate.py` `27948980653f4c0639041243d9f117087f0987c5cc53623abbfa39cbb143adaf`; `runtime/output-validator.py` `6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071`; `runtime/network-readiness.py` `20f37e9191d3e1e025962723328c5f8a2849f664cf1bf215715ccf8da9fc7235`.

Accepted executable-set contract (re-read from the accepted candidate driver's frozen `EXEC_REL_PATHS`/`EXEC_TABLE`, consistent with the canonical implementation/readback records) — EXACTLY 20 paths at mode 0555, all other package files 0444, both root binding files 0644:

- `package-auditor-a/boundary/networked-boundary-launcher.py`, `…/boundary/probe-true`, `…/boundary/tool-domain-wrapper`, `…/payload/runtime/boundary-bwrap/bwrap`, `…/payload/runtime/claude-code-2.1.274/bin/claude.exe`, `…/payload/runtime/shells/zsh`, `…/runtime/network-readiness.py`, `…/runtime/output-validator.py`, `…/runtime/resource-gate.py`;
- `package-auditor-b/boundary/networked-boundary-launcher.py`, `…/boundary/probe-true`, `…/boundary/tool-domain-wrapper`, `…/payload/runtime/codex-0.154.0-linux-x64/bin/codex`, `…/bin/codex-code-mode-host`, `…/codex-path/rg`, `…/codex-resources/bwrap`, `…/codex-resources/zsh/bin/zsh`, `…/runtime/network-readiness.py`, `…/runtime/output-validator.py`, `…/runtime/resource-gate.py`.

Transcription observation (recorded honestly; `06a-binding-b-hash-correction-note.txt` in the evidence workspace): the design task's Section-10 Auditor-B binding value `…5c6b3870…` (b-variant, position 43) matches NOTHING — full-history pickaxe 0, worktree 1 hit = this session's own first evidence script (recorded self-reference). The live binding file hashes to `…5c6c3870…`, which is the exact value carried by ALL THREE canonical records (implementation `91511f36…`, CR readback `550a0b46…`, design `d763f3d0…`). The canonical + live value governs and is recorded in the table above. `TRANSCRIPTION_VARIANT / CANONICAL_VALUE_GOVERNS / NON_PRODUCT_DEFECT / NON_BLOCKING`.

## Section 11 — R-PGPL-CR-1 actual live ROOT comparison — CARRIED (PLTD4-38)

For BOTH verified PCH4 packages, the future activation gate MUST parse the ACTUAL ROOT values from `runtime/resource-gate.py` and `boundary/networked-boundary-launcher.py` and require the observed ROOT to equal `/home/isa/aucdev023-s1-prep002-rem002`.

Observed THIS session from verified fresh-package material (first `ROOT = "…"` assignment, the exact `extract_root_assignment` semantics preserved in the accepted candidate driver):

- Auditor-A `runtime/resource-gate.py` ROOT = `/home/isa/aucdev023-s1-prep002-rem002`;
- Auditor-A `boundary/networked-boundary-launcher.py` ROOT = `/home/isa/aucdev023-s1-prep002-rem002`;
- Auditor-B `runtime/resource-gate.py` ROOT = `/home/isa/aucdev023-s1-prep002-rem002`;
- Auditor-B `boundary/networked-boundary-launcher.py` ROOT = `/home/isa/aucdev023-s1-prep002-rem002`.

The accepted candidate structurally preserves the actual-comparison mechanism (`extract_root_assignment` + `verify_generation` on BOTH verified copies vs the table `gate_root` under `strict_roots`, both roles — statically confirmed present). A constant-success assertion or prose saying "root pinned" is NOT evidence; this design verifies the PRESERVATION statically and does NOT pretend the future live comparison has already satisfied the activation gate.

## Section 12 — Future repository / canonical authority gate (PLTD4-39)

The future grant/prelaunch activation session must receive from Control Room the exact canonical Git identity produced AFTER this design publication AND the independent Control Room readback acceptance. Before chmod it must freshly verify: live GitHub default branch; exact live HEAD equals the exact Control-Room-authorized post-readback SHA; sole-parent/lineage; trust-anchor ancestry; zero unauthorized merge; authorized changed-path geometry; protected trees exact; PCH4 preparation/design/implementation/readback records exact; authority reservation/readback exact; no governed tracked drift; no unrelated staged content; five PINNED_RECORD_BLOBS exact and applicable. Tip drift: STOP, NO AUTO-REBASE.

## Section 13 — Five PINNED_RECORD_BLOBS (PLTD4-40)

Re-resolved at the design baseline `e22bbd4…` — ALL FIVE applicable and EXACT:

- `AUCDEV-023-S1-RB001-L1-AUDITOR-B-DURABLE-OUTPUT-BINDING-CONTROL-ROOM-READBACK.md` → `9f7599fe079efd248dcf08319914eb53fadb0ce1`;
- `AUCDEV-023-S1-RB001-L1-RB002-SUCCESSOR-PACKAGE-PREPARATION.md` → `578b58c8deffa716278c394a640076a3f5eb900d`;
- `AUCDEV-023-S1-RB001-L1-RB002-SUCCESSOR-PACKAGE-CONTROL-ROOM-READBACK.md` → `83951286cf74b33e9836147f4d7656be6e76d257`;
- `AUCDEV-023-S1-RB001-L1-RB002-OPERATOR-LAUNCHER-ADAPTATION-DESIGN-REVISION.md` → `7ba8910ec9dfbf52fe4f877fb28247efd3c8cee1`;
- `AUCDEV-023-S1-RB001-L1-RB002-OPERATOR-LAUNCHER-ADAPTATION-DESIGN-REVISION-CONTROL-ROOM-READBACK.md` → `776a039a221a6d74bf98b17a4ccd8f59cd88f07a`.

FIVE APPLICABLE / FIVE EXACT / SAME ADMISSION SEMANTICS / NO CURRENT PIN / NO BACKLOG PIN / NO SIXTH RECORD.

## Section 14 — Credential boundary — METADATA ONLY (PLTD4-41)

Resolved THIS session using the accepted env-override-first, conventional-fallback rule (exactly the candidate driver's `CREDENTIAL_ENV` / `CREDENTIAL_CONVENTIONAL` contract):

| Role | Resolution class | Resolved path | stat |
|---|---|---|---|
| A | CONVENTIONAL_FALLBACK (`AUCDEV_A_CREDENTIAL_FILE` unset) | `/home/isa/.claude/.credentials.json` | regular; non-symlink; isa:isa; mode 0600; 519 B |
| B | CONVENTIONAL_FALLBACK (`AUCDEV_B_CREDENTIAL_FILE` unset) | `/home/isa/.codex/auth.json` | regular; non-symlink; isa:isa; mode 0600; 4231 B |

Both sizes within the accepted custody bounds `CREDENTIAL_MIN_BYTES=1 .. CREDENTIAL_MAX_BYTES=65536`. NO open; NO read; NO hash of contents; NO print; NO copy; NO parse; NO packaging. Credential metadata observed during DESIGN is NOT future-validity proof; the future activation session MUST repeat this metadata-only gate. Credential contents may enter the audited attempt only through already-frozen runtime custody mechanics after an authorized attempt begins.

## Section 15 — Future human-grant / prelaunch activation order — DESIGN ONLY (PLTD4-42)

All read-only gates happen FIRST, in this exact fail-closed order:

1. Fresh live Git/canonical bootstrap at the exact future authorized SHA.
2. Verify exact explicit human GRANT and exact reserved authority ID.
3. Verify no prior grant/consumption/runtime-authority artifact.
4. Fresh lstat/stat/re-hash DRIVER; require exact 0600.
5. Fresh lstat/stat/re-hash WRAPPER; require exact 0600.
6. Re-verify wrapper driver-path, driver-SHA and `REQUIRED_DRIVER_MODE="700"`.
7. Re-verify current deployed predecessor geometry identity-only.
8. Re-verify NINE historical backups and ZERO staging.
9. Re-verify fresh PCH4 runtime namespace pristine.
10. Re-verify repository lineage/protected trees/PINNED_RECORD_BLOBS.
11. Resolve credential METADATA ONLY.
12. Perform COMPLETE R-PCH2-CR-1 exact-EBS BOTH-role full package-byte gate, including ACTUAL live ROOT comparisons.
13. Re-stat/re-hash BOTH candidate files again and require they remain exact 0600 after every read-only gate.

ONLY THEN:

14. chmod DRIVER 0600 → 0700.
15. Immediately stat + full re-hash DRIVER; require exact path, exact bytes, exact SHA, exact size, exact owner, regular non-symlink, mode exactly 0700.
16. ONLY after driver verification PASS: chmod WRAPPER 0600 → 0700.
17. Immediately stat + full re-hash WRAPPER; require exact identity and mode 0700.
18. Re-verify wrapper pins exact.
19. EXECUTE NEITHER. 20. DEPLOY NOTHING. 21. CREATE NO ATTEMPT. 22. MUTATE NO AccountingStore. 23. READ NO credential contents. 24. RUN NO auditor/provider/model.
25. Publish future human-grant/prelaunch activated-state canonical record.
26. Generate reviewer handoff LAST.
27. Return to Control Room.

Future activated authority state: GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED. Activation is CHMOD-ONLY.

## Section 16 — Partial-chmod fail-closed semantics (PLTD4-43)

If DRIVER chmod succeeds but immediate driver verification fails; OR WRAPPER chmod fails; OR WRAPPER immediate verification fails; OR any post-chmod invariant fails: STOP. Execute neither. Deploy nothing. Create no attempt. Read no credential contents. Run no auditor/provider/model. Do not retry automatically. Do not invent rollback authority. Do not silently chmod back to 0600. Do not proceed to human-direct invocation. Return the exact partial activation state to Control Room. A partial activation state is NOT invocation-eligible.

## Section 17 — Deployment remains inside the single human-direct invocation (PLTD4-44)

The future grant/prelaunch activation session MUST NOT deploy `evt-e7f217c5675fd9d1`; MUST NOT create a staging generation; MUST NOT create `event.backup.pre-pch4-replacement-event`; MUST NOT create attempts; MUST NOT mutate AccountingStore. Deployment remains inside the eventual single human-direct wrapper invocation.

Preserved accepted driver destination semantics: `EXPECTED_HISTORICAL` — only state permitting replacement; `ALREADY_NEW` — STOP, return to Control Room, NEVER resume; `UNKNOWN` / `ABSENT` / unexpected — STOP. The eventual single invocation performs its own verify → stage → verify → reclassify → atomic predecessor backup → deployment → post-deployment full verification → only then attempt/accounting/credential/runtime progression. External or prelaunch deployment invalidates the intended one-shot lifecycle.

## Section 18 — Two-stage human lifecycle — DESIGN ONLY (PLTD4-45)

STAGE A — FUTURE human-grant / prelaunch activation. Only after this design is published, an independent Control Room readback accepts it, and the human operator separately sends the exact GRANT line. A bounded activation agent performs all read-only gates, the full package-byte gate, chmod-only activation; executes neither candidate; deploys nothing; publishes activated state; returns to Control Room for independent readback.

STAGE B — FUTURE single human-direct invocation. Only after Control Room independently accepts the Stage-A publication. The HUMAN OPERATOR — NOT an agent — may directly invoke exactly once, with NO arguments:

```
cd /home/isa/audit-council-dev && ./run-aucdev023-firstpass-rb001-l1-rb003-pch4-e7f217c5-impl01.sh
```

At invocation BEGIN the authority becomes irreversibly CONSUMED / NON_REUSABLE. No second invocation. No retry. No resume. No fallback. THIS DESIGN AUTHORIZES NEITHER STAGE.

## Section 19 — Prelaunch wrapper preexec consumption-marker gap — CARRIED (PLTD4-46)

`PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP = OPEN / ACCEPTED / FAIL-CLOSED / NON-BLOCKING`

The wrapper has no durable pre-exec authority-consumption marker. If a future human-direct invocation is KNOWN to begin but fails before the driver's durable invocation-evidence context exists: authority is STILL consumed; marker absence does NOT restore authority; marker absence is NOT proof no invocation occurred; NO second invocation; NO retry; NO resume; return to Control Room. The wrapper is NOT redesigned in this task.

## Section 20 — Held project truth / residuals (PLTD4-48)

Preserved verbatim: AUCDEV-023 remains P1 / READY / NOT DONE with NO queue-count transition (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11; no backlog item marked DONE; this design NOT reinterpreted as execution readiness). EXEC-RB-001 OPEN/ROOT_CAUSE_UNRESOLVED; EXEC-RB-002 CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH; EXEC-RB-003 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_MECHANICAL_STRENGTH; EXEC-RB-004 CLOSED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH; PREP-001 CLOSED; OLA-001 CLOSED; EXEC-RA-001/002 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH; EXEC-RA-003/004 CLOSED_AT_CONTROL_ROOM_DISPOSITION_STRENGTH with EXEC-RA-004-INST-1 preserved informational; PCH-001..004 DEFENSE-IN-DEPTH PROMPT-CONFORMANCE HARDENING / NOT PRODUCT-DEFECT REMEDIATION; PCH3 execution authority CONSUMED/TERMINAL/CLOSED/NO_RERUN 2/2; prior nonconforming candidate 15198c02/1366785b permanently NOT_ADMITTED untouched; fresh PCH4 event PREPARED_ONLY and A/B packages PREPARED/FROZEN NOT deployed NOT execution-ready; installed source `8ae33444f349ce73c1359b963722e2d16acba630` with installed-qualified provenance NOT ESTABLISHED; audit completeness INCOMPLETE; qualification NONE; installation NONE.

## Section 21 — Evidence-script session transients (recorded honestly, WITHOUT erasure) (PLTD4-49)

1. First canonical-blob verification loop ran under the interactive zsh where the loop variable name `path` is zsh's special PATH-tied array, emptying command resolution (all seven lookups empty-FAIL); superseded by the bash evidence script `01-bootstrap-canonical-blobs.sh` (all PASS); first output preserved in the session transcript.
2. Input-handoff payload-set comparison assumed unprefixed sums rows (rows are `./`-prefixed) and guessed wrong canonical-member payload paths; MISSING=36/UNLISTED=36 false alarm; superseded by `02b-input-handoff-fix.sh` (0/0; canonical members byte-equal); first output preserved at `02-input-handoff-verify.out`.
3. Candidate restat compared locale-localized `stat %F` output ("normal dosya") to the C-locale literal "regular file"; all data was exact; superseded by `04b-candidate-restat-fix.sh` under `LC_ALL=C` (PASS); first output preserved at `04-candidate-restat.out`.
4. Binding-B expected-value transcription variant from the design task text (Section 10 note above); canonical + live value governs; first output preserved at `06-package-ebs-design-evidence.out`; correction note `06a-binding-b-hash-correction-note.txt`.
5. The CURRENT/BACKLOG installation command hung on the operator shell's interactive `cp` alias (cp −i semantics) at its FIRST overwrite prompt, timing out before ANY file was modified (both canonical files verified still original at 1035/2670 lines; the stale `/tmp/backlog-record.txt` found on disk dated from an unrelated prior session and was deleted before rewrite); the task was stopped and re-run with alias-immune redirection writes, which installed both files byte-identically to the intended content; no repository file was altered by the hung attempt.
6. The first staged-diff assertion script used SIGPIPE-fragile `grep -q` pipelines (early match → git SIGPIPE → pipefail → false SEM FAIL on six checks whose strings were demonstrably present) and one over-broad negative regex that flagged the record's own NEGATED statements ("NOT execution readiness", "NEVER claim execution readiness"); superseded by `08b-assertions-fix.sh` (diff saved to file; affirmative-form-only negatives): 9/9 semantic PASS, 6/6 negative PASS, the single added `PCH4_EXECUTION_AUTHORITY` line is the exact RESERVED value, all `EXECUTION_GRANT` mentions NONE-valued; first output preserved at `08-semantic-negative-assertions.out`.

ALL: `EVIDENCE_SCRIPT_TRANSIENT_DIAGNOSTIC / CORRECTED_IN_SESSION / FIRST_OUTPUT_PRESERVED / NON_PRODUCT_DEFECT / NON_BLOCKING / NO_NEW_OPEN_RESIDUAL`.

## Section 22 — Design disposition (PLTD4-50)

```
PCH4_REPLACEMENT_PRELAUNCH_TRANSITION_DESIGN =
  READY_FOR_CONTROL_ROOM_READBACK /
  ACCEPTED_IMPLEMENTATION_CANDIDATES_BOUND /
  LIVE_HOST_DRIVER_WRAPPER_0600_REVERIFIED /
  PRELAUNCH_MODE_BARRIER_CLOSED /
  EXACT_FUTURE_HUMAN_GRANT_TARGET_DEFINED /
  HUMAN_OPERATOR_GRANT_NONE /
  FUTURE_AUTHORITY_RESERVED_NOT_GRANTED /
  FRESH_EXACT_EBS_BOTH_ROLE_FULL_PACKAGE_BYTE_GATE_DEFINED /
  EVERY_PAYLOAD_BYTE_REHASH_REQUIRED /
  CORRECT_GOVERNING_EBS_SHA_BOUND /
  LIVE_GATE_ROOT_COMPARISON_REQUIRED /
  PACKAGE_GATE_BEFORE_ANY_CHMOD /
  REPOSITORY_CANONICAL_FUTURE_GATES_DEFINED /
  FIVE_PINNED_RECORD_BLOBS_VERIFIED /
  CREDENTIAL_METADATA_ONLY_GATE_DEFINED /
  DRIVER_THEN_WRAPPER_CHMOD_ORDER_DEFINED /
  IMMEDIATE_POST_CHMOD_REHASH_REQUIRED /
  PARTIAL_CHMOD_FAIL_CLOSED_SEMANTICS_DEFINED /
  DEPLOYMENT_REMAINS_INSIDE_SINGLE_HUMAN_DIRECT_INVOCATION /
  SINGLE_USE_FAIL_CLOSED_AUTHORITY_CONSUMPTION_DEFINED /
  PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP_CARRIED /
  NO_RETRY / NO_RESUME / NO_FALLBACK /
  NO_GRANT / NO_CHMOD / NO_DEPLOYMENT / ZERO_RUNTIME /
  NO_EXECUTION_AUTHORITY / NO_QUALIFICATION / NO_INSTALLATION
```

This session does NOT claim Control Room design acceptance; that belongs to the independent readback.

## Section 23 — Design acceptance matrix

| ID | Check | Result |
|---|---|---|
| PLTD4-01 | Live GitHub master == local HEAD == `e22bbd4…` at bootstrap | PASS |
| PLTD4-02 | Root tree `2b829173…` + sole parent `021175a9…` EXACT | PASS |
| PLTD4-03 | Seven canonical blobs EXACT at the base | PASS |
| PLTD4-04 | Protected trees EXACT (bootstrap-supervisor/qualification-harness/skill) | PASS |
| PLTD4-05 | Pre-existing smoke-fixture gitlink drift recorded, NOT staged | PASS |
| PLTD4-06 | Input handoff outer SHA `398fbc39…` / 999156 B / regular isa:isa | PASS |
| PLTD4-07 | Census 44 = 37 regular (36 payload + 1 SHA256SUMS) + 7 dirs; 0 symlinks/hardlinks/specials/unsafe/duplicates | PASS |
| PLTD4-08 | SHA256SUMS 36/36 PASS; 0 missing; 0 unlisted | PASS |
| PLTD4-09 | Canonical members byte-equal to live blobs with trailing LF | PASS |
| PLTD4-10 | Handoff candidate copies hash-identical to live candidates | PASS |
| PLTD4-11 | ZERO sealed-report bytes; ZERO credential material in handoff | PASS |
| PLTD4-12 | Four-identity collision sweep: COLLISION_COUNT=0, SCAN_ERROR_COUNT=0 | PASS |
| PLTD4-13 | Driver live restat: `5b946a1b…`/170138/3410 lines/0600/isa:isa/regular/non-symlink/exec-bits-absent | PASS |
| PLTD4-14 | Wrapper live restat: `03ad514b…`/3468/82 lines/0600/isa:isa/regular/non-symlink/exec-bits-absent | PASS |
| PLTD4-15 | PRELAUNCH_MODE_BARRIER = CLOSED recorded | PASS |
| PLTD4-16 | Wrapper three-way SHA closure + DRIVER path + `REQUIRED_DRIVER_MODE="700"` static | PASS |
| PLTD4-17 | Wrapper control mechanics held (parse-only; never sourced) | PASS |
| PLTD4-18 | Predecessor attempt census EXACTLY 31 | PASS |
| PLTD4-19 | Backup census EXACTLY NINE exact names | PASS |
| PLTD4-20 | ZERO `event.staging.*` | PASS |
| PLTD4-21 | Auditor-A accounting `6349f9af…`/5616 + exact six-state sequence | PASS |
| PLTD4-22 | Auditor-A sealed report `5b73bc81…`/30169/0444 identity-only UNREAD | PASS |
| PLTD4-23 | Auditor-B accounting `8881e281…`/5666 + exact six-state sequence | PASS |
| PLTD4-24 | Auditor-B custody-out EMPTY; sealed snapshot `f3babc7d…`/907/0600 identity-only UNREAD | PASS |
| PLTD4-25 | Actual wrong PCH3 attempt value remains UNKNOWN | PASS |
| PLTD4-26 | Fresh PCH4 namespace PRISTINE (zero attempt/staging/backup/run-evidence/grant artifacts) | PASS |
| PLTD4-27 | Nine historical mechanical handoffs classified; ZERO authority-bound | PASS |
| PLTD4-28 | Reserved authority exact and UNMUTATED; EXECUTION_GRANT = NONE | PASS |
| PLTD4-29 | Exact future grant target table defined | PASS |
| PLTD4-30 | Exact grant phrase recorded with grants-NOTHING semantics | PASS |
| PLTD4-31 | Five-state authority machine defined | PASS |
| PLTD4-32 | R-PCH2-CR-1 gate defined (21 requirements; DEFINED NOT CLOSED) | PASS |
| PLTD4-33 | Auditor-A package identities exact at design strength | PASS |
| PLTD4-34 | Auditor-B package identities exact at design strength (canonical value; b-variant transcription noted) | PASS |
| PLTD4-35 | Governing EBS identity exact via live protected verifier | PASS |
| PLTD4-36 | Prompt contract `bc9d1482…` at all four fresh copies; frozen target commit present and pinned | PASS |
| PLTD4-37 | Held components re-hashed; exact 20-path 0555 executable table re-read from accepted records | PASS |
| PLTD4-38 | R-PGPL-CR-1: ACTUAL ROOT observed = deploy root from all four verified package files; mechanism preservation statically confirmed | PASS |
| PLTD4-39 | Future repository/canonical authority gate defined | PASS |
| PLTD4-40 | Five PINNED_RECORD_BLOBS 5/5 APPLICABLE+EXACT; no current/backlog pin; no sixth record | PASS |
| PLTD4-41 | Credential metadata-only both roles (CONVENTIONAL_FALLBACK; 0600; within custody bounds; contents untouched) | PASS |
| PLTD4-42 | 27-step activation order defined (read-only gates first; driver-then-wrapper chmod; post-chmod rehash) | PASS |
| PLTD4-43 | Partial-chmod fail-closed semantics defined | PASS |
| PLTD4-44 | Deployment-inside-single-invocation invariant defined | PASS |
| PLTD4-45 | Two-stage lifecycle defined; THIS DESIGN AUTHORIZES NEITHER STAGE | PASS |
| PLTD4-46 | Consumption-marker gap carried OPEN/ACCEPTED/FAIL-CLOSED/NON-BLOCKING | PASS |
| PLTD4-47 | Zero-runtime attestation complete | PASS |
| PLTD4-48 | Held project truth preserved (counts, residuals, qualification NONE, installation NONE) | PASS |
| PLTD4-49 | Four session transients recorded honestly with first outputs preserved | PASS |
| PLTD4-50 | Design disposition emitted at design strength ONLY | PASS |
| PLTD4-51 | Exactly one next action recorded | PASS |

(PLTD4-01..PLTD4-50 finalized at staging; PLTD4-51 finalized at the generated-LAST handoff. Machine-checkable evidence in the untracked evidence workspace `aucdev023-exec-ra004-pch4-prelaunch-transition-design-evidence`.)

## Section 24 — Exactly one next action

INDEPENDENT CONTROL ROOM READBACK OF THE PCH4 REPLACEMENT PRELAUNCH TRANSITION DESIGN AND ITS GENERATED-LAST HANDOFF, STRICTLY BEFORE ANY HUMAN EXECUTION-AUTHORITY GRANT, CHMOD, PRELAUNCH ACTIVATION, DEPLOYMENT, RUNTIME ATTEMPT, CREDENTIAL-CONTENT ACCESS, AUDITOR/PROVIDER EXECUTION, QUALIFICATION OR INSTALLATION.

The design publication itself issues and simulates NO grant.

## Section 25 — Never list (binding on this record)

NEVER treat this design as an execution grant; NEVER issue or simulate the GRANT; NEVER consume the reserved authority; NEVER chmod, deploy or run the candidate launcher; NEVER execute/import/source either candidate; NEVER open either real report artifact; NEVER infer the actual PCH3 invalid attempt value; NEVER run an auditor/provider/model or /audit-council; NEVER claim execution readiness, prelaunch admission, remediation proof, fix verification, future auditor conformance, qualification or installation.
