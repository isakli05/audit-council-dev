# AUCDEV-023 — S1 RB-001 L1 RB-003 EXEC-RA-003 / PCH-003 — Replacement Prelaunch Transition Design

Design authority: `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA003-PCH3-REPLACEMENT-PRELAUNCH-TRANSITION-DESIGN-20260928-01`
Date: 2026-09-28 (Europe/Istanbul)
Exact live base: `e99e30622468d507c6166c63399a5146f4a30793` (live master == local HEAD EXACT at bootstrap; re-resolved EXACT immediately before staging and again immediately before commit)
Root tree: `80c735077894f2178fdd597c0057471d5d681919`; sole parent: `b464a437263e16295ab1bb282bdcb2e5113e1358`

## Section 0 — Role, boundary and zero-runtime attestation (PLD3-50..PLD3-56)

This session is the BOUNDED PCH3 REPLACEMENT PRELAUNCH TRANSITION DESIGNER and READ-ONLY MECHANICAL EVIDENCE COLLECTOR. It designs — and does NOT perform — the transition from the accepted PCH3 0600 NON-EXECUTABLE launcher candidates to a possible FUTURE, separately human-granted, chmod-only activated, single-use execution lifecycle.

NOT: the human operator granting execution; a grant publisher; a prelaunch activator; a launcher executor; a deployment authority; an execution controller; an execution-authority grantor; Auditor-A or Auditor-B; a credential-content reader; a provider/model execution authority; a qualification authority; an installation authority.

ZERO RUNTIME in this session (PLD3-50): execution-authority grant NONE (PLD3-51); candidate chmod NONE (PLD3-52); candidate execution/import/sourcing NONE; deployment NONE (PLD3-53); runtime attempts NONE; AccountingStore mutation NONE; credential-content reads NONE (metadata-only lstat permitted by the Section 16 boundary; no credential file opened, read or hashed); sealed-report substance reads NONE (both sealed predecessor artifacts stat/SHA/census identity-only, never opened/parsed/decoded/quoted); auditor/provider/model executions ZERO; execution authority NONE created/granted/consumed (PLD3-54); qualification NONE (PLD3-55); installation NONE (PLD3-56).

Permitted local computation: live Git/bootstrap reads; read-only hashing/stat/census; candidate lstat/stat/hash and static text inspection; JSON parsing of non-report governance/binding/MANIFEST/accounting-state files; corrected-handoff read-only verification (ZERO members executed); evidence-workspace writes; docs-only publication. Network: the mandated bootstrap `git ls-remote`, the pre-staging AND pre-commit live re-resolves, the single push of this publication, and the post-push readback ONLY.

## Section 1 — Exact live bootstrap (PLD3-01)

- `git ls-remote origin refs/heads/master` at bootstrap: `e99e30622468d507c6166c63399a5146f4a30793` == local HEAD EXACT.
- Root tree `80c735077894f2178fdd597c0057471d5d681919`; `git rev-list --parents -n 1 HEAD` gives sole parent `b464a437263e16295ab1bb282bdcb2e5113e1358` EXACT.
- Canonical blobs at this exact base verified EXACT:
  - PCH3 implementation record `0652e1400020a66de65508e11825859dcdfd4e2f`;
  - PCH3 implementation Control Room readback `e667fe935b470edc47446a5939f6a22d67073c70`;
  - `AUCDEV-CURRENT-STATE.md` `ef19f28589bffd88a85a703cf4b06a866f882be2`;
  - `AUCDEV-BACKLOG.md` `4900428e21b16dfa90e8e3514b997da2d3cef7f1`;
  - accepted earlier PCH3 launcher rebind/adaptation design `a6890c22fa5ad858fbd4a39a08ba216a5f414f22` and its Control Room readback `3e79c3d13568c21fb0a12af84b783a54e18e7cf5` preserved byte-for-byte.
- Live master re-resolved EXACT immediately before staging and again immediately before commit; tip drift would STOP with no auto-rebase.

## Section 2 — Operative corrected handoff; historical packaging defect closed (PLD3-02..PLD3-07)

The ONLY operative implementation-readback reviewer handoff is:

`AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA003-PCH3-REPLACEMENT-OPERATOR-LAUNCHER-IMPLEMENTATION-CONTROL-ROOM-READBACK-HANDOFF-CORRECTED-20260928-01.tar.gz`

Verified READ-ONLY with ZERO members executed (PLD3-02..PLD3-05):

- outer SHA-256 `e6a62375a1beb328688301c08c8fc4c937a127731247b9689a7869978e42100f`; size 977741 B EXACT;
- geometry EXACT: 44 members = 38 regular files (37 payload + exactly 1 SHA256SUMS) + 6 directories; 0 symlinks; 0 hardlinks; 0 special files; 0 duplicates; 0 unsafe paths;
- checksums: exactly 37 rows, 37/37 PASS by independent re-hash of every extracted member copy; 0 missing; 0 unlisted;
- post-package archive-member Git blob identities EXACT (canonical copies routed as RAW Git blob bytes, verified `git hash-object` == live blob, trailing final LF present at byte level `0x0a` on all three):
  - implementation Control Room readback `e667fe935b470edc47446a5939f6a22d67073c70`;
  - CURRENT `ef19f28589bffd88a85a703cf4b06a866f882be2`;
  - BACKLOG `4900428e21b16dfa90e8e3514b997da2d3cef7f1`.

Historical nonconforming handoff (EVIDENCE HISTORY ONLY, immutable, NON-OPERATIVE for canonical-byte provenance): `…-CONTROL-ROOM-READBACK-HANDOFF.tar.gz`, outer SHA-256 `3f5d8995cfc0b70dfb9260df4c7dc45ccab880306660df876a566630d85bfc38`, 975624 B. Established defect, re-proven mechanically THIS session from the actual historical bytes (PLD3-06):

`HANDOFF_PACKAGING / EVIDENCE_PROVENANCE_DEFECT / TRAILING_NEWLINE_LOSS_IN_CANONICAL_ARCHIVE_COPIES / OBSERVED_FACT / NON_PRODUCT_DEFECT / NON_IMPLEMENTATION_BYTE_DEFECT / CANONICAL_GIT_PUBLICATION_UNAFFECTED`

- historical non-LF-terminated Git blobs re-observed EXACT: readback `bb8a1fd41cbb8ea6e59ede42ea81f4b61010058a`, CURRENT `772061f0ada2b788dffed0f41515678ea2a215c6`, BACKLOG `54ae9c1ee25c7ae988fc1aa396bc8544b1dbbc67`;
- for EACH of the three: appending exactly one LF to the historical member reproduces the exact live Git blob — proving the defect was EXACTLY one missing final LF and nothing else;
- the corrected handoff independently closes that exact packaging defect (canonical members byte-equal to live Git).

Record-count precision correction (PLD3-07): the historical archive contained 36 payload files total = 3 canonical + 33 non-canonical; the corrected repackaging necessarily rebuilt INDEX and SHA256SUMS and added `handoff-correction.txt`; exactly 32 historical non-canonical payload files (excluding the rebuilt INDEX) were mechanically observed byte-identical across old and corrected archives, with 0 absent (re-swept mechanically this session). The earlier "35 non-canonical payloads byte-identical" wording is inaccurate and MUST NOT be repeated. Classification: `RECORD_COUNT_PRECISION_CORRECTION / NON_BLOCKING / NON_PRODUCT_DEFECT`; no new open residual.

## Section 3 — Protected trees held (PLD3-08)

At the exact base: `bootstrap-supervisor` `732b8def9f22d7c466ce77f3d3049da53bfff3d0`; `qualification-harness` `5b8d5e5465923740470ff63ed9b8683f257a3787`; `skill` `c792933a862d9a5434681a88d183470dd8b15d2f` — ALL EXACT, none modified by this publication.

## Section 4 — Accepted PCH3 driver — fresh live-host readback (PLD3-09)

Path: `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch3-2b618b6e-impl01.py`

Freshly lstat/stat/re-hashed on the ACTUAL LIVE HOST in THIS design session:

- SHA-256 `73376afabd2927a9cfbe7d6de45a787c1cf3340d4e1822fa4c7ec74d239d1d66` EXACT; size 169665 B EXACT; 3403 lines EXACT;
- regular file; non-symlink; owner `isa:isa`; mode EXACTLY `0600`; executable bits ABSENT.

This fresh LIVE-HOST restat closes the carried prelaunch evidence-metadata requirement (the implementation-readback's INFORMATIONAL note that archive-copy 0o644 metadata is not authoritative for live-host mode) at DESIGN observation strength. The driver was NEVER executed/imported/sourced; static text only.

## Section 5 — Accepted PCH3 wrapper — fresh live-host readback and pins (PLD3-10, PLD3-11)

Path: `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch3-2b618b6e-impl01.sh`

Freshly lstat/stat/re-hashed on the ACTUAL LIVE HOST in THIS design session:

- SHA-256 `05d6fcc9b9310a569e7af22a5bc97907f402a261700150abbe245cb0d0cd45c1` EXACT; size 3468 B EXACT; 82 lines EXACT;
- regular; non-symlink; owner `isa:isa`; mode EXACTLY `0600`; executable bits ABSENT.

Static pins verified by direct read (PLD3-11): `DRIVER=` the exact PCH3 driver path above; `REQUIRED_DRIVER_SHA256="73376afabd2927a9cfbe7d6de45a787c1cf3340d4e1822fa4c7ec74d239d1d66"`; `REQUIRED_DRIVER_MODE="700"`. Control mechanics present byte-identically: `set -euo pipefail`; `set +x`; `umask 077`; `ulimit -c 0` refusal; pinned PATH; root refusal; regular/non-symlink/owner/mode/SHA pre-exec checks; PYTHON* unsets; `exec /usr/bin/python3 -I "$DRIVER"`; no positional-argument forwarding. The wrapper was NEVER executed/sourced.

## Section 6 — PRELAUNCH_MODE_BARRIER = CLOSED (PLD3-12)

Driver actual mode `0600`; wrapper actual mode `0600`; wrapper-required driver mode `700`. Therefore NO human-direct invocation is mechanically admitted. The barrier opens ONLY through a FUTURE, separately human-granted, bounded chmod-only activation session AFTER this design is published, receives independent Control Room readback acceptance, the human operator sends the exact explicit grant, and every mandatory read-only prelaunch gate passes. THIS DESIGN DOES NOT OPEN THE BARRIER.

## Section 7 — Governing EBS identity — correct value only (PLD3-13, PLD3-14)

Live `bootstrap-supervisor/MANIFEST.json` re-hashed from the exact repo blob at the exact base: SHA-256 `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999` carrying `package_sha256` `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8` (PLD3-13). This correct pair is pinned in the candidate driver (L230/L232), pinned in BOTH deployed PCH2 predecessor bindings' `ebs_package`, and pinned in BOTH fresh PCH3 bindings. The rejected historical wrong transcription (documented in prior records) occurs ZERO times in the candidate driver, the candidate wrapper and THIS record, and never governs any pin or assertion (PLD3-14).

## Section 8 — Current deployed predecessor — identity only (PLD3-15..PLD3-20)

Deploy root `/home/isa/aucdev023-s1-prep002-rem002`; current predecessor event `evt-aa640691cfe9d33c` (PLD3-15). All facts re-verified identity-only THIS session:

- Auditor-A deployed generation (PLD3-16): binding file SHA-256 `075b2de246065c4828fedc588256686750f15b04579444ac60f973e287411f16`; canonical digest `439ee7fb5a76376f9572c8a38364c7cba288afb4ef23d18844ded68d1023fdb2` (corroborated by the live accounting `binding_digest` pin); MANIFEST `45adb9800ff3ef93e71d09e08629a44df324c362e562cd93118575c329b853bd`; package `0637a86e14916d750b8c0cd7ce553c7594deaa30a17ea45b8719dcffe7a4caaf`; rows/payload-bytes 191/236323090 independently recomputed from the live MANIFEST.
- Auditor-B deployed generation (PLD3-17): binding `19ba43f5869ee5a57e1191a9699fa012f48cb75724d76a9b476c40d7b0443fc1`; canonical `b38c1a5105bb2ac8789fb536ac5d3ff39a440956aeb3e01b3e9038fd697550a6` (live accounting `binding_digest` pin); MANIFEST `9b18bcb046ba8bdbef49ac4083b6aaf401f2fb65d1952e6339ce9aa051f63b4c`; package `796457a2db3a8e33549ed4347daf7ff7d7de73c303917cbfe5d7bea7c9191aa3`; rows/payload-bytes 194/343454621 recomputed EXACT.
- Auditor-A attempt `evt-aa640691cfe9d33c-A-01`: accounting `4f2e84b27f7f6d6fc300b76af81bd3f7bbe64eb8ca4cd166611b9930957e9aac` / 5616 B / mode 0600, exact six-state sequence PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_FROZEN → TERMINAL; staging EMPTY; custody-out census EXACTLY `evt-aa640691cfe9d33c-A-01.first-pass-report.json`; sealed frozen report identity ONLY: `a0f69d22fefe8333eb9a3b349a934b20438371f63f80ad1bfdf215554b4379d8` / 26208 B / 0444.
- Auditor-B attempt `evt-aa640691cfe9d33c-B-01`: accounting `a91c8914cac38d8d454575f1d56d002db6b9c9025c4abc158b3eff3a376a5849` / 5663 B / 0600, exact six-state sequence ending REPORT_INVALID → TERMINAL; custody-out EMPTY; staging census EXACTLY `evt-aa640691cfe9d33c-B-01.first-pass-report.json`; sealed invalid snapshot identity ONLY: `877eb06c74996d316501aaab23ef4ea15262e787f3e9b70bcdf555a7343d81f0` / 699 B / 0600.
- BLINDNESS (PLD3-18): both sealed artifacts stat/SHA/census identity-only — NEVER opened, parsed, decoded, printed or quoted; the actual invalid `auditor_role` value REMAINS UNKNOWN; NO inference recorded.
- Attempt-root census EXACTLY 29 (PLD3-15 context); exact historical backup set of EIGHT observed (PLD3-19): `event.backup.pre-successor-event`, `pre-exec03-new-event`, `pre-exec02`, `pre-rb001-l1-successor-event`, `pre-rb002-successor-event`, `pre-rb003-corrected-successor-event`, `pre-pch1-replacement-event`, `pre-pch2-replacement-event`; ZERO `event.staging.*` directories (PLD3-20).

## Section 9 — Fresh PCH3 runtime namespace — pristine (PLD3-21..PLD3-24)

Freshly verified read-only THIS session: zero `evt-2b618b6e*` attempt roots under the deploy root (PLD3-21); `event.staging.rb001-l1-rb003-2b618b6e-pch3` ABSENT; `event.backup.pre-pch3-replacement-event` ABSENT (PLD3-22); zero `*2b618b6e*` paths anywhere under the deploy root; `pch3-2b618b6e-impl01-run-evidence` ABSENT at the repo root (PLD3-23); the authority-bound `…PCH3-REPLACEMENT-FIRSTPASS-EXEC-20260927-01-MECHANICAL-HANDOFF.tar.gz` ABSENT; zero grant/consumption/runtime-authority artifacts anywhere (PLD3-24). ANY unexpected presence would have STOPed; nothing was deleted, normalized, renamed or reused.

## Section 10 — Fresh PCH3 package identities — design binding strength (PLD3-32, PLD3-33, PLD3-34)

Preparation root: `/home/isa/aucdev023-s1-rb001-l1-rb003-exec-ra003-pch3-exact-role-literal-fresh-replacement-package-prep-20260927-01/event`. Verified live read-only THIS session at DESIGN strength (the future full package-byte gate of Section 13 is deliberately NOT claimed here):

- Auditor-A: binding file `33944324890d5c36680f0282364878203304115b146f5e8e6ce877638fe3d645`; canonical digest `ee50c8af50e8d83c83729aa2a232af4386a5a296b2c1e8d55e8a9c1945d14aa0` (accepted preparation evidence); MANIFEST `fa48693db06fd981f1832b880a12df54c539fafd0342ba727869272803ea7102`; package `5a53ce0286417a4ca06c2a795e8eb93af2712ccde9b8e765199372c6255ef99a`; rows/payload-bytes 191/236323302 independently recomputed from the live fresh MANIFEST (PLD3-32); event/attempt/role relations exact (`evt-2b618b6e2fccb80a` / `evt-2b618b6e2fccb80a-A-01` / `AUDITOR_A`); auditor executable `payload/runtime/claude-code-2.1.274/bin/claude.exe` SHA `15e2d05148f801b5774032faad87e624ecd172e9903288bda448b892eb58fa07` re-hashed EXACT in-package, mode 0555.
- Auditor-B: binding `f668dcbd787a426d5fdf53f3d2b2e08cc0ca332e3d02df168f13cca0527ed329`; canonical `f7c18ae9f0fc692bb3b8c5b63da0027582217b6293575116b24e76ebdaab5740`; MANIFEST `bbacc7c26be2b5c1c552810546e46a7114055c2f022a18c0e6015943a699d5ca`; package `0026999cef4399ac5b1c562b9783d6ce26510e9265a9b0ccff30757619234e59`; rows/payload-bytes 194/343454833 recomputed EXACT (PLD3-33); relations exact (`…-B-01` / `AUDITOR_B`); auditor executable `payload/runtime/codex-0.154.0-linux-x64/bin/codex` SHA `3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022` re-hashed EXACT in-package, mode 0555; binding invocation geometry intact (argc 8; `--output-last-message` exactly once; canonical destination argv-only; prompt the FINAL positional element carrying the exact role literal).
- Shared held identities re-hashed live inside BOTH fresh packages EXACT: boundary launcher `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa` (`boundary/networked-boundary-launcher.py`); resource gate `27948980653f4c0639041243d9f117087f0987c5cc53623abbfa39cbb143adaf` (`runtime/resource-gate.py`); network readiness `20f37e9191d3e1e025962723328c5f8a2849f664cf1bf215715ccf8da9fc7235` (`runtime/network-readiness.py`); output validator `6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071` (`runtime/output-validator.py`) — all UNCHANGED.
- Prompt contract `13658e6499d6591db860cd85458ee2c6ada90eb0ffe194002f6d4c633c10ac91` located by exact hash at ALL FOUR expected package copies (per-role `payload/evidence/common/prompt-contract.json` + `transport/prompt-contract.json`), byte-identical; frozen target `d4d584ffa47ad2848268ba947247f81a845b2322` pinned in both bindings and MANIFEST transport bindings.
- Executable contract BOUND for the future gate (PLD3-34): the accepted 20-path event-relative executable set with EVERY executable mode EXACTLY 0555 (both auditor executables observed 0555 live this session; the complete set re-walk is mandatory inside the future Section 13 gate, not here).

## Section 11 — Future execution authority — RESERVED ONLY; exact grant target (PLD3-25..PLD3-28)

Reserved future execution authority (PLD3-27): `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA003-PCH3-REPLACEMENT-FIRSTPASS-EXEC-20260927-01` — state `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE`. Its appearance anywhere (including this record and the candidate source constants) grants NOTHING.

HUMAN OPERATOR GRANT: NONE (PLD3-26).

Exact future grant phrase (PLD3-28), valid ONLY if the HUMAN OPERATOR later sends this exact line as a separate explicit message AFTER this design is published AND independent Control Room readback has accepted it:

`GRANT AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA003-PCH3-REPLACEMENT-FIRSTPASS-EXEC-20260927-01`

Malformed, partial, conditional, hedged, wrong-ID or wrong-target text: NO GRANT.

Exact grant target (PLD3-25):

| Element | Value |
|---|---|
| driver | `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb003-pch3-2b618b6e-impl01.py` — SHA-256 `73376afa…d1d66`, required pre-grant mode 0600 |
| wrapper | `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb003-pch3-2b618b6e-impl01.sh` — SHA-256 `05d6fcc9…cd45c1`, required pre-grant mode 0600 |
| event | `evt-2b618b6e2fccb80a` |
| attempts | `evt-2b618b6e2fccb80a-A-01`, `evt-2b618b6e2fccb80a-B-01` |
| engagement budget | maximum 2 inference-capable engagements TOTAL |
| ordering | Auditor-A FIRST; Auditor-B ONLY after mechanically conforming Auditor-A completion |

Properties: ONE-SHOT; ONE HUMAN-DIRECT WRAPPER INVOCATION MAXIMUM; NON-TRANSFERABLE; EXACT-TARGET-SPECIFIC; NO RETRY; NO RESUME; NO FALLBACK; NO ALTERNATE DRIVER/WRAPPER/EVENT/ATTEMPT; NO QUALIFICATION AUTHORITY; NO INSTALLATION AUTHORITY.

## Section 12 — Authority state machine — design only (PLD3-29)

1. NOW: `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE`.
2. After a FUTURE separate explicit HUMAN OPERATOR GRANT, before chmod: `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_NOT_YET_ACTIVATED`.
3. After SUCCESSFUL future bounded chmod-only activation: `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED`.
4. At the BEGINNING of the eventual human-direct wrapper invocation: authority becomes permanently `CONSUMED / NON_REUSABLE` — regardless of whether wrapper prechecks complete, Python starts, driver invocation evidence exists, deployment happens, attempts are created, AccountingStore exists, credentials are read, dynamic gates run, a provider starts, or inference occurs.
5. When the one invocation terminates/stops: `CONSUMED / TERMINAL / CLOSED / NO_RERUN`. Unused engagement capacity NEVER restores authority.

## Section 13 — R-PCH2-CR-1 future full package-byte gate — DEFINED, NOT EXECUTED (PLD3-30, PLD3-31, PLD3-36)

R-PCH2-CR-1 remains BINDING_FOR_PCH3. This design DEFINES but DOES NOT EXECUTE the gate; it MUST run in a later separately authorized HUMAN-GRANT / PRELAUNCH ACTIVATION session BEFORE ANY chmod (PLD3-36). The gate executes NO auditor/provider/model and NO package executable. Mandatory steps:

1. Resolve the then-LIVE protected bootstrap-supervisor at its exact canonical Git base.
2. Require protected tree `732b8def9f22d7c466ce77f3d3049da53bfff3d0`.
3. Require EBS MANIFEST SHA-256 `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999`.
4. Parse it and require `package_sha256` `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8`.
5. Re-hash the complete protected EBS package source and reproduce the exact package SHA.
6. Load the exact then-LIVE EBS parsing/verification semantics — never a copied approximation.
7. Parse BOTH exact fresh PCH3 bindings.
8. Recompute canonical digests: A `ee50c8af50e8d83c83729aa2a232af4386a5a296b2c1e8d55e8a9c1945d14aa0`; B `f7c18ae9f0fc692bb3b8c5b63da0027582217b6293575116b24e76ebdaab5740`.
9. Run exact `verify_event_package` semantics for BOTH roles.
10. Independently walk BOTH package trees with followlinks=false.
11. Require zero symlink dirs/files; zero hardlinks; zero specials; zero traversal; exact payload-set equality against each MANIFEST.
12. Re-hash EVERY A payload byte (PLD3-31): exactly 191 unique rows; exactly 236323302 payload bytes; every SHA/size PASS.
13. Re-hash EVERY B payload byte: exactly 194 unique rows; exactly 343454833 payload bytes; every SHA/size PASS.
14. Require package identities A `5a53ce0286417a4ca06c2a795e8eb93af2712ccde9b8e765199372c6255ef99a`, B `0026999cef4399ac5b1c562b9783d6ce26510e9265a9b0ccff30757619234e59`.
15. Require MANIFEST identities A `fa48693db06fd981f1832b880a12df54c539fafd0342ba727869272803ea7102`, B `bbacc7c26be2b5c1c552810546e46a7114055c2f022a18c0e6015943a699d5ca`.
16. Require exact event/attempt/role/frozen-target relations: event `evt-2b618b6e2fccb80a`; `AUDITOR_A`/`A-01`; `AUDITOR_B`/`B-01`; target `d4d584ffa47ad2848268ba947247f81a845b2322`.
17. Require prompt contract `13658e6499d6591db860cd85458ee2c6ada90eb0ffe194002f6d4c633c10ac91`.
18. Require boundary-launcher / resource-gate / network-readiness / output-validator / auditor-executable identities EXACT.
19. Require the exact accepted 20-path event-relative executable set, every executable mode EXACTLY 0555.
20. Perform the ACTUAL live ROOT comparison required by R-PGPL-CR-1 (Section 14).
21. BOTH roles PASS. ANY mismatch: STOP BEFORE chmod. Inventories or top-level digests alone are insufficient.

## Section 14 — R-PGPL-CR-1 — actual live ROOT comparison (PLD3-35)

The future gate MUST inspect the actual verified fresh PCH3 bytes: for BOTH A and B, actual parsed ROOT values in `runtime/resource-gate.py` and `boundary/networked-boundary-launcher.py` must equal `/home/isa/aucdev023-s1-prep002-rem002`, recording the observed value from verified package material. A literal assertion equivalent to `check(..., True, "root pinned")` is NOT evidence. The accepted candidate driver PRESERVES this comparison structurally: `verify_role_generation` performs `extract_root_assignment` on BOTH verified package components against `gate_root_expected` (= `DEPLOY_ROOT`) under `strict_roots` — verified by static read this session at driver L736-743. R-PGPL-CR-1 remains CARRIED until the later live full-byte prelaunch gate actually performs and records the comparison.

## Section 15 — Repository / canonical authority future gate (PLD3-37, PLD3-38)

The future grant/prelaunch activation session MUST receive from Control Room the exact canonical HEAD/blobs produced AFTER this design publication and its independent Control Room readback. Before chmod it must freshly verify: live GitHub default branch exact; live HEAD equals the exact Control-Room-authorized post-readback SHA; exact sole-parent/lineage; trust-anchor ancestry; zero unauthorized merge; changed paths confined to authorized governance docs; protected trees exact; PCH3 preparation/design/implementation/readback records exact; corrected handoff identity recorded exactly; no governed tracked drift; no unrelated staged content. Tip drift: STOP; no auto-rebase.

Five immutable PINNED_RECORD_BLOBS retained and freshly re-resolved EXACT at the live base THIS session (PLD3-38): `9f7599fe079efd248dcf08319914eb53fadb0ce1` (B durable-output-binding readback), `578b58c8deffa716278c394a640076a3f5eb900d` (RB002 successor package prep), `83951286cf74b33e9836147f4d7656be6e76d257` (RB002 successor package readback), `7ba8910ec9dfbf52fe4f877fb28247efd3c8cee1` (RB002 OLA design revision), `776a039a221a6d74bf98b17a4ccd8f59cd88f07a` (RB002 OLA design revision readback).

## Section 16 — Credential boundary — metadata only (PLD3-39)

This design inspected ONLY credential STRUCTURE and metadata (lstat; no open/read/hash/print/copy/package/parse of contents):

- Role A conventional source `/home/isa/.claude/.credentials.json`: regular, non-symlink, owner `isa:isa`, mode 0600, size 519 B.
- Role B conventional source `/home/isa/.codex/auth.json`: regular, non-symlink, owner `isa:isa`, mode 0600, size 4231 B.
- Both sizes within the accepted custody bounds (1..65536 B per the driver constants `CREDENTIAL_MIN_BYTES`/`CREDENTIAL_MAX_BYTES`).
- Supported environment locator overrides: `AUCDEV_A_CREDENTIAL_FILE` / `AUCDEV_B_CREDENTIAL_FILE` (resolution class: env-override-first, conventional-fallback).

The FUTURE prelaunch activation MUST freshly resolve both credential source paths including any override, and for each require regular file / non-symlink / expected owner / mode 0600 / size within custody bounds — recording ONLY path, size, mode, owner and source/override resolution class; NEVER content or hash. Credential content may enter the audited attempt only through the already-frozen runtime custody mechanics after authorized attempt start.

## Section 17 — Future grant/prelaunch activation order — design only (PLD3-40, PLD3-41, PLD3-43)

Runs ONLY after this design publication + independent Control Room acceptance + separate exact HUMAN OPERATOR GRANT. Exact fail-closed order:

1. Fresh live Git/canonical bootstrap at the exact authorized post-readback SHA.
2. Verify exact human grant and exact reserved authority ID.
3. Verify no prior grant/consumption/runtime artifact exists.
4. Freshly lstat/stat/re-hash DRIVER; require exact 0600.
5. Freshly lstat/stat/re-hash WRAPPER; require exact 0600.
6. Verify wrapper pins exact driver SHA and `REQUIRED_DRIVER_MODE=700`.
7. Re-verify current deployed PCH2 predecessor geometry identity-only.
8. Re-verify exact eight historical backups and zero unexpected staging.
9. Re-verify complete fresh PCH3 runtime namespace pristine.
10. Verify repository lineage, protected trees and PINNED_RECORD_BLOBS.
11. Resolve credential METADATA ONLY.
12. Perform the COMPLETE exact-EBS BOTH-role package-byte gate from Section 13, INCLUDING the actual live ROOT comparisons.
13. Re-check both candidate files are still exact 0600 after every read-only gate.
14. ONLY THEN: chmod DRIVER 0600 → 0700 (PLD3-40).
15. Immediately stat + re-hash DRIVER: exact bytes, size, owner, path; mode exactly 0700 (PLD3-41).
16. ONLY AFTER DRIVER verification PASS: chmod WRAPPER 0600 → 0700.
17. Immediately stat + re-hash WRAPPER: exact bytes, size, owner, path; mode exactly 0700.
18. Re-verify wrapper still pins exact driver SHA and `REQUIRED_DRIVER_MODE=700`.
19. EXECUTE NEITHER (PLD3-43). 20. DEPLOY NOTHING. 21. CREATE NO ATTEMPT. 22. Read NO credential contents. 23. Run NO auditor/provider/model.
24. Publish a future human-grant/prelaunch canonical record with state `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED`.
25. Generate reviewer handoff LAST. 26. Return to Control Room.

Activation is CHMOD-ONLY. NONE of these mutation steps is performed in THIS design session.

## Section 18 — Partial-chmod fail-closed semantics (PLD3-42)

If DRIVER chmod succeeds but immediate verification fails; OR wrapper chmod fails; OR wrapper immediate verification fails; OR any post-chmod invariant fails: STOP. Execute neither; deploy nothing; create no attempt; run no provider; do not retry automatically; do not invent rollback authority; do not silently chmod back to 0600; do not proceed to human-direct invocation. Return the exact partial activation state to Control Room. A partial activation state is NOT invocation-eligible.

## Section 19 — Deployment boundary (PLD3-44, PLD3-45)

Deployment MUST remain INSIDE the eventual single human-direct wrapper invocation. The future grant/prelaunch activation session MUST NOT deploy `evt-2b618b6e2fccb80a`, create staging runtime generation, create the pre-PCH3 backup, create attempts, or mutate AccountingStore. Accepted eventual driver behavior remains: `EXPECTED_HISTORICAL` the only state permitting replacement; `ALREADY_NEW` → STOP / return to Control Room / NEVER resume (PLD3-45, refusal arm verified statically at driver L1635/L1313); `UNKNOWN`/`ABSENT`/unexpected → STOP (L1601/L1609). The eventual single invocation performs its own verify → stage → verify → reclassify → atomic predecessor backup → deployment → post-verification lifecycle before A-first execution. External/prelaunch deployment invalidates the one-shot lifecycle (PLD3-44).

## Section 20 — Two-stage human lifecycle (PLD3-46, PLD3-47, PLD3-48)

STAGE A — future human-grant/prelaunch activation: the human operator first sends the exact separate GRANT; a bounded prelaunch agent performs all gates, the full-byte package verification, chmod-only activation, executes neither candidate, deploys nothing, publishes activated state; Control Room independently reads back that publication.

STAGE B — single human-direct invocation: ONLY after Control Room accepts the grant/prelaunch readback, the HUMAN OPERATOR may directly invoke EXACTLY ONCE with NO arguments:

```
cd /home/isa/audit-council-dev
./run-aucdev023-firstpass-rb001-l1-rb003-pch3-2b618b6e-impl01.sh
```

NO AGENT performs that human-direct invocation. At invocation BEGIN the authority is irreversibly CONSUMED / NON_REUSABLE (PLD3-47). No second invocation. No retry. No resume. No fallback (PLD3-48). THIS DESIGN AUTHORIZES NEITHER STAGE (PLD3-46 defined only).

## Section 21 — Wrapper preexec consumption-marker gap — carried (PLD3-49)

`PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP = OPEN / ACCEPTED / FAIL-CLOSED / NON-BLOCKING`. The wrapper has no durable pre-exec consumption marker. If a future human-direct invocation is KNOWN to begin but fails before the driver's durable invocation-evidence context exists: authority is STILL consumed; marker absence does NOT restore authority and is NOT proof no invocation occurred; NO second invocation, NO retry, NO resume; return to Control Room. The wrapper is NOT redesigned in this task.

## Section 22 — Residual / correction matrix (no scope broadening)

- R-PCH2-CR-1: OPEN / BINDING_FOR_PCH3 — full both-role package-byte gate mandatory before ANY future chmod (Section 13).
- R-PCH2-CR-2: CARRIED_AND_HONORED.
- R-PCH2-IMP-CR-1: CLOSED_AT_EVIDENCE_PRECISION_STRENGTH.
- R-PCH2-IMP-CR-2: CLOSED_AT_EVIDENCE_PRECISION_STRENGTH.
- R-PCH2-DES-CR-1: CLOSED_AT_RECORD_PRECISION_STRENGTH (correct EBS SHA only).
- R-PIMP-CR-1: HONORED.
- R-PGPL-CR-1: CARRIED — actual live ROOT comparison mandatory in the future full-byte prelaunch gate (Section 14).
- R-RA002-1: CARRIED.
- PRELAUNCH_WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP: OPEN / ACCEPTED / FAIL-CLOSED / NON-BLOCKING (Section 21).
- PCH3 implementation-readback historical handoff trailing-LF packaging defect: CLOSED_AT_CORRECTED_HANDOFF_CONTROL_ROOM_READBACK_STRENGTH — historical outer SHA `3f5d8995…`; operative corrected outer SHA `e6a62375…`; canonical Git publication unaffected; NON_PRODUCT_DEFECT (Section 2).
- Historical report payload-count wording correction: 33 non-canonical historical payloads; rebuilt INDEX excluded; 32 historical non-canonical payloads mechanically carried byte-identical; `RECORD_COUNT_PRECISION_CORRECTION / NON_BLOCKING` (Section 2).

NO new OPEN residual was directly observed this session.

## Section 23 — Design acceptance matrix (PLD3-01..PLD3-58)

| Row | Requirement | Result |
|---|---|---|
| PLD3-01 | live Git exact (`e99e3062` == local HEAD; root/parent exact) | PASS |
| PLD3-02 | corrected handoff outer SHA `e6a62375…` / 977741 B exact | PASS |
| PLD3-03 | corrected archive geometry 44 = 38 regular (37 payload + 1 SHA256SUMS) + 6 dirs; 0 sym/hard/special/dup/unsafe | PASS |
| PLD3-04 | corrected archive 37 rows 37/37 PASS; 0 missing; 0 unlisted | PASS |
| PLD3-05 | corrected canonical members exact Git blobs `e667fe93`/`ef19f285`/`4900428e` incl. final LF | PASS |
| PLD3-06 | historical LF packaging defect recorded accurately (three +1LF reproductions) | PASS |
| PLD3-07 | historical payload-count precision corrected (33/32 wording) | PASS |
| PLD3-08 | protected trees held (`732b8def`/`5b8d5e54`/`c792933a`) | PASS |
| PLD3-09 | live-host driver exact SHA/size/lines/owner/type; mode exactly 0600; exec bits absent | PASS |
| PLD3-10 | live-host wrapper exact SHA/size/lines/owner/type; mode exactly 0600; exec bits absent | PASS |
| PLD3-11 | wrapper exact driver SHA pin + REQUIRED_DRIVER_MODE=700 + control mechanics | PASS |
| PLD3-12 | PRELAUNCH_MODE_BARRIER = CLOSED | PASS |
| PLD3-13 | governing EBS identities correct (`d683f64d`/`d42aa9e3` live + pinned everywhere) | PASS |
| PLD3-14 | wrong EBS transcription governs nothing (0 occurrences driver/wrapper/this record) | PASS |
| PLD3-15 | current predecessor event exact (`evt-aa640691cfe9d33c`; census 29) | PASS |
| PLD3-16 | predecessor A geometry exact identity-only (bindings/MANIFEST/package/rows/bytes/accounting/states/sealed) | PASS |
| PLD3-17 | predecessor B geometry exact identity-only (incl. EMPTY custody-out; REPORT_INVALID) | PASS |
| PLD3-18 | sealed-report blindness held (both artifacts identity-only; invalid role value still UNKNOWN) | PASS |
| PLD3-19 | exact eight historical backups | PASS |
| PLD3-20 | zero unexpected staging | PASS |
| PLD3-21 | fresh PCH3 attempts absent | PASS |
| PLD3-22 | fresh backup absent | PASS |
| PLD3-23 | fresh invocation/evidence namespace absent | PASS |
| PLD3-24 | fresh AccountingStore/runtime authority state absent | PASS |
| PLD3-25 | future grant target exact (table, Section 11) | PASS |
| PLD3-26 | human grant NONE | PASS |
| PLD3-27 | authority reserved/not-granted/not-consumed/not-executable | PASS |
| PLD3-28 | exact future grant phrase defined | PASS |
| PLD3-29 | authority state machine defined (5 states, Section 12) | PASS |
| PLD3-30 | full exact-EBS both-role gate defined (21 steps, Section 13) | PASS |
| PLD3-31 | every payload byte rehash mandatory (steps 12-13) | PASS |
| PLD3-32 | PCH3 A package/count identities exact at design strength | PASS |
| PLD3-33 | PCH3 B package/count identities exact at design strength | PASS |
| PLD3-34 | executable 20-path/0555 contract bound | PASS |
| PLD3-35 | actual live ROOT comparison mandatory (Section 14) | PASS |
| PLD3-36 | package/root gate before ANY chmod (ordering; inventories insufficient) | PASS |
| PLD3-37 | repository/canonical gate defined (Section 15) | PASS |
| PLD3-38 | five PINNED_RECORD_BLOBS retained + re-resolved EXACT | PASS |
| PLD3-39 | credential metadata-only gate defined (+ metadata recorded) | PASS |
| PLD3-40 | driver-then-wrapper chmod order defined | PASS |
| PLD3-41 | immediate post-chmod rehash defined | PASS |
| PLD3-42 | partial-chmod STOP semantics defined | PASS |
| PLD3-43 | execute-neither activation invariant defined | PASS |
| PLD3-44 | deployment-inside-invocation preserved | PASS |
| PLD3-45 | ALREADY_NEW refusal preserved | PASS |
| PLD3-46 | single-human-direct invocation defined | PASS |
| PLD3-47 | authority consumed at wrapper invocation BEGIN | PASS |
| PLD3-48 | no retry/no resume/no fallback | PASS |
| PLD3-49 | wrapper-preexec marker gap carried | PASS |
| PLD3-50 | ZERO runtime | PASS |
| PLD3-51 | NO grant | PASS |
| PLD3-52 | NO chmod | PASS |
| PLD3-53 | NO deployment | PASS |
| PLD3-54 | NO execution authority | PASS |
| PLD3-55 | NO qualification | PASS |
| PLD3-56 | NO installation | PASS |
| PLD3-57 | tracked publication path set exact (3 paths) | PASS |
| PLD3-58 | generated-LAST handoff post-package canonical-byte gate exact | PASS |

## Section 24 — Held truth (preserved verbatim)

Consumed authority `AUCDEV-023-S1-RB001-L1-RB003-EXEC-RA002-PCH2-REPLACEMENT-FIRSTPASS-EXEC-20260927-01` CONSUMED/TERMINAL/CLOSED/NO_RERUN (engagements 2/2; its driver `63352e34…`/wrapper `e703af08…` NOT executed/imported/sourced/chmod'ed here). EXEC-RB-001 OPEN/ROOT_CAUSE_UNRESOLVED; EXEC-RB-002 CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH; EXEC-RB-003 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_MECHANICAL_STRENGTH; EXEC-RB-004 CLOSED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH; PREP-001 CLOSED; OLA-001 CLOSED; EXEC-RA-001 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH (old event only); EXEC-RA-002 ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_STRUCTURAL_STRENGTH (disposition A; superseded in consequence by the accepted PCH2 preparation path); EXEC-RA-003 CLOSED_AT_CONTROL_ROOM_DISPOSITION_STRENGTH (NO wording causality; NOT FIX_VERIFIED/REMEDIATION_PROVEN/MODEL_BEHAVIOR_PROVEN/PRODUCT_DEFECT_CLOSED); PCH-001/PCH-002/PCH-003 DEFENSE-IN-DEPTH PROMPT-CONFORMANCE HARDENING / EXTERNAL-AUDITOR-OUTPUT-RISK REDUCTION / NOT PRODUCT-DEFECT REMEDIATION; prior nonconforming candidate `15198c02`/`1366785b` permanently NOT_ADMITTED untouched; old OLA001R1 artifacts `1863c343`/`ac258cb3` untouched; AUCDEV-023 remains P1 / READY / NOT DONE with NO queue-count transition (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11); audit completeness INCOMPLETE; qualification NONE; installation NONE; installed source `8ae33444` with installed-qualified provenance NOT ESTABLISHED.

## Section 25 — Disposition, publication boundary and next action

Disposition:

`PCH3_REPLACEMENT_PRELAUNCH_TRANSITION_DESIGN = READY_FOR_CONTROL_ROOM_READBACK / ACCEPTED_IMPLEMENTATION_CANDIDATES_BOUND / CORRECTED_IMPLEMENTATION_READBACK_HANDOFF_ACCEPTED / HISTORICAL_HANDOFF_PACKAGING_DEFECT_CLOSED / LIVE_HOST_DRIVER_WRAPPER_0600_REVERIFIED / PRELAUNCH_MODE_BARRIER_CLOSED / EXACT_FUTURE_HUMAN_GRANT_TARGET_DEFINED / FUTURE_AUTHORITY_RESERVED_NOT_GRANTED / FRESH_EXACT_EBS_BOTH_ROLE_FULL_PACKAGE_BYTE_GATE_DEFINED / CORRECT_GOVERNING_EBS_SHA_BOUND / LIVE_GATE_ROOT_COMPARISON_REQUIRED / CURRENT_PREDECESSOR_GATES_DEFINED / FRESH_NAMESPACE_GATES_DEFINED / REPOSITORY_AUTHORITY_GATES_DEFINED / CREDENTIAL_METADATA_ONLY_GATE_DEFINED / CHMOD_ONLY_POST_GRANT_ACTIVATION_DEFINED / DRIVER_THEN_WRAPPER_0600_TO_0700_ORDER_DEFINED / PARTIAL_CHMOD_FAIL_CLOSED_SEMANTICS_DEFINED / DEPLOYMENT_REMAINS_INSIDE_SINGLE_HUMAN_DIRECT_INVOCATION / SINGLE_USE_FAIL_CLOSED_AUTHORITY_CONSUMPTION_DEFINED / WRAPPER_PREEXEC_CONSUMPTION_MARKER_GAP_CARRIED / NO_RETRY / NO_RESUME / NO_FALLBACK / NO_GRANT / NO_CHMOD / NO_DEPLOYMENT / ZERO_RUNTIME / NO_EXECUTION_AUTHORITY / NO_QUALIFICATION / NO_INSTALLATION`

This disposition is DESIGN strength only — NOT prelaunch approval, NOT execution readiness, NOT an audit verdict, NOT qualification, NOT installation.

Publication boundary: exactly three changed tracked paths — NEW this design record + `AUCDEV-CURRENT-STATE.md` (rotation + dated append) + `AUCDEV-BACKLOG.md` (dated append); the candidate driver/wrapper, both handoff archives, the evidence workspace and all runtime trees remain UNTRACKED/UNTOUCHED; exactly ONE docs-only fast-forward commit whose sole parent is `e99e30622468d507c6166c63399a5146f4a30793`; reviewer handoff generated LAST from raw Git bytes.

NEXT ACTION EXACTLY ONE: INDEPENDENT CONTROL ROOM READBACK OF THE PCH3 REPLACEMENT PRELAUNCH TRANSITION DESIGN AND ITS GENERATED-LAST HANDOFF — BEFORE ANY human execution-authority grant, chmod, prelaunch activation, deployment, runtime attempt, credential-content access, auditor/provider execution, qualification, or installation. DO NOT ISSUE THE GRANT. DO NOT CHMOD. DO NOT DEPLOY. DO NOT EXECUTE THE DRIVER OR WRAPPER. DO NOT RUN AUDITORS/PROVIDERS.
