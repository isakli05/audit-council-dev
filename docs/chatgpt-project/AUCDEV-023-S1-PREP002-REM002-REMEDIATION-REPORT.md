# AUCDEV-023 — S1 PREP-002 / REM-002 Execution-Boundary Remediation Report (Canonical Record)

| Field | Value |
|---|---|
| Status | **`AUCDEV_023_S1_PREP002_REM002_REMEDIATION = IMPLEMENTED / SUCCESSOR_PACKAGES_FROZEN / AWAITING_CONTROL_ROOM_READBACK`** — implementer-strength remediation evidence ONLY. NOT Control Room closure, NOT independent audit, NOT event execution, NOT qualification, NOT installation, and NO execution authority of any kind. |
| Session class | BOUNDED ZERO-PROVIDER REMEDIATION IMPLEMENTER SESSION under operator authority `AUCDEV-023-S1-PREP002-REM002-20260920-01` (Audit Council Dev Control Room, 2026-09-20); the selected IMPLEMENTER (Claude Code + GLM-5.3) only — NOT the Control Room, NOT an independent auditor, NOT Auditor-A/B, NOT a qualification or installation authority; ZERO provider/model/frontier executions (the deterministic mock transport returns FIXED scripted bytes — no model anywhere; the mock is reachable ONLY on loopback inside isolated `--unshare-net` namespaces), real credentials ZERO (SYNTHETIC bytes only, everywhere), `/audit-council` ZERO, neither reserved real attempt id was consumed or referenced by any rehearsal (`BOOTSTRAP_EVENT` remains `NOT_INSTANTIATED`; no accounting record for any real attempt) |
| Date | 2026-09-21 (Europe/Istanbul) |
| Authority | `AUCDEV-023-S1-PREP002-REM002-20260920-01` — permits ONLY bounded remediation of `AUCDEV023-CR-S1-PREP-002` and `AUCDEV023-CR-S1-REM-002`, the deterministic/local zero-inference testing needed to establish those fixes, construction of a NEW successor frozen S1 event-package generation for BOTH roles (shared launcher/wrapper bytes change), and publication of the implementation evidence. Does NOT permit real Auditor-A/B execution, provider/model/frontier inference, consumption of either reserved attempt, real credentials, `/audit-council`, qualification, installation, or autonomous retry. `MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY = 0`. |
| Exact implementation base | `75706e8b5ff17e5871a16c838e04e05b8260c50f` (tree `83c2d9179617bba4d06b5a4227e05049600ae209`; sole parent `5e8fefb030dd6dc02d4242c9c22e1ae40c405902`), resolved EXACT as live `origin/master` AND local HEAD at bootstrap and re-resolved immediately before staging and push; protected subtrees verified EXACT: bootstrap-supervisor `09f3d6c7ddc00305986cbedad431395c10c95af0`, qualification-harness `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill `c792933a862d9a5434681a88d183470dd8b15d2f`; frozen target `d4d584ffa47ad2848268ba947247f81a845b2322` (root tree `1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7`) verified EXACT and UNCHANGED throughout |
| Event / attempts | Event id `evt-7df609ec6c569043` PRESERVED; reserved attempt ids `evt-7df609ec6c569043-A-01` / `evt-7df609ec6c569043-B-01` PRESERVED — NOT started, NOT consumed, no CONSUMED_PRE_EXEC, no model engagement; reserved workspaces remain empty with no accounting record (V5 permits pre-execution package re-freeze around the same unstarted identities; NO replacement event or attempt was minted) |
| Workspaces | historical S1 workspace `/home/isa/aucdev023-s1-event-preparation/` and historical successor workspace `/home/isa/aucdev023-s1-prep-remediation/` treated as FROZEN HISTORICAL EVIDENCE — never mutated (immutability mechanically re-verified: ALL 371 historical manifest rows A 183/183 + B 188/188 byte-exact against the historical manifests; all expected historical identities matched — §4); ALL remediation work in the NEW dedicated workspace `/home/isa/aucdev023-s1-prep002-rem002/` (outside Git) |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in this
session), `IMPLEMENTER_CLAIM`, `SUBMITTED_EVIDENCE` (deterministic artifacts
submitted for Control Room readback, DATA ONLY), `REQUIREMENT`,
`DISCLOSED_RESIDUAL`.

---

## 1. Remediation summary (OBSERVED_FACT)

Both authorized findings were remediated at implementer strength in a NEW
successor event-package generation (BOTH roles; shared launcher and wrapper
bytes changed), with every prior generation left untouched as historical
evidence:

| Finding | Implementer disposition |
|---|---|
| AUCDEV023-CR-S1-REM-002 AUDITOR_B_REAL_TOOL_ENTRYPOINT_BYPASSES_CREDENTIAL_DOMAIN_WRAPPER | **REMEDIATION_IMPLEMENTED / AWAITING_CONTROL_ROOM_READBACK** — the NATIVE wrapper is interposed at `/usr/bin/bash` AND `/usr/bin/zsh` (the REAL observed Codex tool entry path `/usr/bin/zsh -lc` is now wrapper-interposed); the real client's model-directed report write executes THROUGH the wrapper into the credential-free tool domain with the `AUCDEV_TOOL_DOMAIN=1` marker observed in the recorded tool output; a differential no-wrapper control (same client, same scripted bytes, only the interposition removed) flips the oracle — marker absent, client-domain sentinel VISIBLE, and `/proc/1/root/auditor-init/credential.bin` READABLE on the unwrapped path vs UNREADABLE with the wrapper: CAUSAL traversal established, not inferred |
| AUCDEV023-CR-S1-PREP-002 AUDITOR_B_EFFECTIVE_CLIENT_RUNTIME_IDENTITY_NOT_FULLY_PINNED (complete pre-isolation execution closure) | **REMEDIATION_IMPLEMENTED / AWAITING_CONTROL_ROOM_READBACK** — the credential-domain wrapper is a NATIVE STATIC-PIE executable (NO host interpreter, NO dynamic loader/library before the namespace split; the historical `#!/usr/bin/python3` interpreter and its loader closure are GONE from the transition path); the wrapper execs the PACKAGE-PINNED engine `/auditor-tools/bin/bwrap` (never host `/usr/bin/bwrap`); the OUTER boundary composition itself is composed by the package-pinned vendored bwrap (a manifest row in BOTH packages); the pinned client's startup capability-probe payload (`/usr/bin/true`, mechanically observed executing in the credential-bearing window) is itself now a pinned package byte; every CLIENT_DOMAIN and SPLIT_TRANSITION row of the machine-readable authority-path inventory is a frozen, EBS-verified package byte |

Implementation completion is NOT Control Room closure.

## 2. REM-002 remediation mechanism (OBSERVED_FACT)

**A. Interposition at EVERY real initial shell entry point (§13).**
The successor launcher binds the NATIVE wrapper over `/usr/bin/bash` AND
`/usr/bin/zsh` — both REGULAR-FILE destinations on the event host; `/usr/bin/sh`
→ `bash` and `/bin` → `usr/bin` are symlinks, so `/bin/zsh`, `/bin/bash`,
`/bin/sh` and `/usr/bin/sh` all resolve onto the two interposed regular files
(NO bind targets a symlink destination — the historical bubblewrap
symlink-destination abort class cannot recur). Mechanically verified from
INSIDE the real boundary composition (client-domain probe evidence):
all six entry paths carry EXACTLY the frozen wrapper bytes
(`0ed2ba48…`), every one executable, and every one demonstrates the
`AUCDEV_TOOL_DOMAIN=1` marker when executed (assertion 7 probes).
`evidence/rem002/shell-entry-coverage.json`.

**B. The real client tool path crosses the wrapper (§11, SUBMITTED_EVIDENCE).**
Through the EXACT `codex exec --skip-git-repo-check --profile aucdev023-c3`
composition with the frozen profile bytes VERBATIM, driven by the deterministic
mock transport inside `--unshare-net` (loopback-only; every attempted external
egress fails closed, recorded):

1. the mechanically OBSERVED tool entry path is `/usr/bin/zsh -lc` (client
   stderr evidence, recorded in the proof document) — now the wrapper;
2. the REQUIRED report output path was WRITTEN by the real client THROUGH the
   wrapper-interposed path into the credential-free tool domain, exact scripted
   content, client returncode 0;
3. an UNAUTHORIZED evidence path write was REFUSED (`Read-only file system`);
4. the scripted ORACLE command executed INSIDE the real client tool path and
   its recorded tool output proves, in the tool domain:
   `TOOLMARKER=1` (wrapper marker), `SENTINEL=ABSENT` (the client-domain-only
   boundary sentinel), `HOMEDIR=ABSENT` (`/auditor-home` does not exist),
   `INITDIR=ABSENT` (`/auditor-init` does not exist),
   `CREDVIAPROC=UNREADABLE` (`/proc/1/root/auditor-init/credential.bin` not
   readable — fresh PID namespace; `/proc/1` is the tool-domain shell itself),
   and the fd census shows only the standard descriptors (the single fd-3
   entry is the `ls`/`readlink` self-listing artifact pointing at
   `/proc/<self>/fd` — no EBS-held fd exists in the tool domain);
5. the pinned-engine OBSERVATION composition (a disclosed logging shim
   shadowing `/auditor-tools/bin/bwrap`, exec'ing the real pinned engine from
   `/auditor-tools/bin/bwrap.real`) captured 30 engine invocations: the
   pinned client's own sandbox compositions (including its startup capability
   probes and its sandboxed SELF re-exec of the fd-verified
   `/auditor-init/auditor-executable` — the pinned byte) AND the NATIVE
   wrapper's exact frozen tool-domain composition argv — mechanically proving
   the wrapper execs exactly the PACKAGE-PINNED engine path;
6. the shell-selection logic retains zsh semantics: a basename containing
   `zsh` selects the real VENDORED zsh (bound post-split at
   `/auditor-tools/shells/zsh`, over `/usr/bin/zsh` INSIDE the tool domain);
   bash/sh forward to the real bash (`/auditor-tools/shells/bash`) — zsh is
   never silently replaced by bash. (A latent trap found BY this work and
   designed out: an `r`-prefixed preserved path would have put the vendored
   zsh in RESTRICTED mode, blocking command execution and redirections; the
   `shells/` basenames keep both real shells in NORMAL mode.)

**C. Differential no-wrapper negative control (§12, SUBMITTED_EVIDENCE).**
SAME real pinned client, SAME deterministic scripted provider bytes, SAME
synthetic inputs, in a composition where ONLY the wrapper interposition is
deliberately absent (`include_wrapper=False`): the oracle flips exactly —
`TOOLMARKER=` (absent), `SENTINEL=PRESENT`, `HOMEDIR=PRESENT`,
`INITDIR=PRESENT`, `CREDVIAPROC=READABLE` (on the unwrapped path the
credential staging copy IS reachable through `/proc/1/root` from the tool
command context of the client domain). The marker/sentinel/proc-visibility
flip together with the interposition is CAUSAL wrapper traversal, not an
unrelated denial. (This CONTROL is mechanical differential evidence about the
composition classes only; consistent with the Control Room's finding text, NO
claim is made that historical credential exposure occurred.)

**D. zsh semantics preserved; fail-closed wrapper.** The wrapper selects the
real shell from its invocation name, preserves argv/environment/cwd where
valid, adds the marker, and on ANY failure exits 126 WITHOUT executing any
real shell in the credential-bearing domain (no fallback path exists).

## 3. PREP-002 remediation mechanism — complete pre-isolation closure (OBSERVED_FACT)

**A. NATIVE STATIC-PIE wrapper (§5.A/§10).** Source
`boundary/tool-domain-wrapper.c` (9,973 B,
`4db7141d7dfb9c6ebc7c64ad410e949d32b683bc861f936e0383fb4e6ac43d60` —
complete reviewed source staged as a package row); built with
`/usr/bin/gcc -static-pie -Os -Wall -Wextra` + `strip`
(compiler `gcc (GCC) 16.2.1 20260810`, compiler SHA-256
`a5f680ca8b01b1e7a98d531cac90f258875a301d841fab28a8b56d513470f988`);
binary 871,144 B, mode 0555,
`0ed2ba485ccbb623bb1bb4a649635749ab845445dd78cef507787a108a66d572`;
ELF DYN (static-pie), **no PT_INTERP, no NEEDED entries, no script
interpreter**; REPRODUCIBLE (two independent rebuilds from the same source
produce the identical final SHA-256, which equals the frozen package byte).
`evidence/rem002/wrapper-build.json`.

**B. PACKAGE-PINNED engine at every level (§5.B/§6.4).** The wrapper execs
`/auditor-tools/bin/bwrap` (the frozen package's vendored bwrap row
`01fb705f…`, static-pie) — never host `/usr/bin/bwrap`. The pinned codex
client's OWN sandbox composition also resolves this same PATH-first shadow.
The OUTER boundary composition (launcher side) is now ALSO composed by the
package-pinned vendored bwrap — staged as a manifest row in BOTH role
packages (`payload/runtime/boundary-bwrap/bwrap` in the Auditor-A package;
the vendored closure row in Auditor-B; byte-identical A=B, negative control
N10) — so no unpinned host sandbox-engine byte stands anywhere between the
pinned clients and the credential-free tool domain.

**C. The capability-probe payload is pinned (§5.C, closed by observation).**
The pinned-engine observation log revealed the pinned codex client executing
a `true` payload (`/usr/bin/true`, `/bin/true`) inside its startup capability
probes WHILE the credential-bearing client namespace is in scope — an unpinned
host byte in the pre-isolation window. Closed by pinning: a reviewed trivial
static-pie replacement (`boundary/probe-true.c`, 305 B,
`b6517671380b1e07f00419749173d9663b413b6f4ba5ed842dda4a1d9c192ef6`; binary
862,952 B,
`d3321fd6f31d0082af0ed11ae33fe2f80db3d1e0c8fcbbd70e13f229cb6f5f9c`;
static-pie, no PT_INTERP/NEEDED) is a frozen package row bound over
`/usr/bin/true` in BOTH boundaries (and, through the read-only `/usr` plane,
inside every nested sandbox).

**D. Machine-readable authority-path inventory (§9).**
`evidence/rem002/authority-path-inventory.json` records every member with
logical role, execution path, frozen package path, SHA-256, size, file type,
ELF/interpreter classification, PT_INTERP, NEEDED deps, phase
(CLIENT_DOMAIN / CLIENT_DOMAIN_TO_TOOL_INTERCEPTION / SPLIT_TRANSITION /
TOOL_DOMAIN, plus two disclosed pre-client-entry BOUNDARY_SETUP rows),
credential-path visibility and identity-verification mechanism.
ACCEPTANCE (mechanically computed): every CLIENT_DOMAIN and SPLIT_TRANSITION
row is a frozen package byte (`unpinned_blocking_rows: []`); the
SPLIT_TRANSITION executable is static native; the engine is package-pinned;
and the observation-log scan confirms NO unpinned program executed through
the engine in the credential-bearing window
(`observation_no_unpinned_program_executed: true`).

Post-split TOOL_DOMAIN utilities are honestly classified environmental where
they cannot run until AFTER the boundary is dropped: the real zsh's
dynamic loader/libs resolve from the read-only `/usr` plane inside the tool
domain only; the real bash is host `/usr/bin/bash` bytes preserved at a
post-split-only path. The two BOUNDARY_SETUP rows (the frozen launcher
executed by host Python on the host — the same EBS/launcher custody
interpreter class as the accepted EBS itself — and its INNER bootstrap that
materializes the credential home once inside the boundary BEFORE the client
exec) are DISCLOSED pre-client-entry rows, outside the §5/§9 closure which
begins at the pinned client entry; neither runs in any tool path and both are
replaced at client exec.

## 4. New successor identities (SUBMITTED_EVIDENCE; every prior generation untouched)

Historical generation immutability RE-VERIFIED read-only at bootstrap and at
handoff assembly: all 371 historical manifest rows (A 183/183 + B 188/188)
byte-exact; A manifest `9e512e0e…` package `b4202c70…` binding digest
`23c32def…`; B manifest `6617aba9…` package `89f54f61…` binding digest
`c4bf3cd0…`; launcher `d7b15ad5…`; codex native `3188814c…` — ALL EXACTLY
the operator-expected values. NO historical byte was mutated.

| Dimension | Auditor-A successor (this generation) | Auditor-B successor (this generation) |
|---|---|---|
| binding file SHA-256 | `579d32f1e0e8d6d71045277c6b76e9b348b60de8dcbeac3cf55e59956c226cc2` | `66ccc5d897f477254d83e9c58a6b42a6fc5400861527a84605dd2083ca516a0d` |
| binding canonical digest | `316f6d3659c757a47d02581556f4829c0f18e672e6388d84eb42667bc6ead25f` | `6fe3ebc9978cbf2f764347d3134f6aa141698753a06c5f84f528bbd8b6d82c33` |
| manifest SHA-256 | `802ad1214b92940a6ada407d3663ad71c11265d16c50e962e317525ba3701101` | `4b2b77cb30866911a75665322cb55d37b30d245b2290ba8e47c1abfc564aea62` |
| package SHA-256 (non-circular) | `fd7ec3aed2639f8cd02568ae9464e747190e8cac0b9c4fbc4e839c51ac5983ac` | `8573e16285e4b5cceb96bb1cb92d0216bc540c084fad28ef25e213cb069537ab` |
| manifest rows / payload bytes | 189 / 236,260,424 | 192 / 343,391,385 |
| auditor executable (unchanged) | `CLAUDE-CODE-2.1.274-NATIVE` `15e2d051…` | `CODEX-CLI-0.154.0-NATIVE` `3188814c…` |
| boundary launcher SHA-256 | `2efb666042e44d272a53f9ad4ac93a19c14f1687a33fb38ed84f9823d9bc44a7` (IDENTICAL bytes both packages) | same |
| NATIVE wrapper (identity token `AUCDEV023-TOOL-DOMAIN-WRAPPER-V1`, bytes new) | binary `0ed2ba48…` (871,144 B) + source row `4db7141d…` — IDENTICAL bytes both packages | same |
| pinned probe payload `true` | `d3321fd6…` + source row `b6517671…` — IDENTICAL both packages | same |
| boundary sentinel | `102faf6aa1d4fc1c180565dcc6877ae10b52a80025cdc11fbea83c8f39782649` (28 B, `AUCDEV-BOUNDARY-SENTINEL-V1`) — IDENTICAL both packages | same |
| real shells (post-split) | host real bash at `/auditor-tools/shells/bash`; vendored zsh `67faaaa8…` at `/auditor-tools/shells/zsh` (A stages its own row `payload/runtime/shells/zsh`; B uses its vendored row — byte-identical, N10) | same |
| frozen invocation | `claude -p <prompt>` (unchanged) | `codex exec --skip-git-repo-check --profile aucdev023-c3 <prompt>` (unchanged from the prior successor) |
| event / attempts | `evt-7df609ec6c569043` + `…-A-01` PRESERVED | same, `…-B-01` PRESERVED |

Both bindings parsed and BOTH packages verified by the ACCEPTED EBS
`parse_binding` + `verify_event_package` read-only from the byte-identical
workspace copy of the accepted tree (per-file size/SHA-256, exact payload-set
equality, transport-projection equality). Freeze hygiene verified (regular
files only, modes 0555/0444, dirs 0555, no symlink/hardlink/special, census
clean). V5 UNCHANGED — no V6 invented; launcher identity token remains
`NETWORKED-BOUNDARY-LAUNCHER-V1`; wrapper identity token remains
`AUCDEV023-TOOL-DOMAIN-WRAPPER-V1` (bytes pinned per-package by SHA-256, the
established token-constant/bytes-per-generation pattern). The frozen
invocations, frozen profile/config surfaces, common-evidence manifest (167
members; digests byte-identical `ebddcd60…` / projection `ff116a9d…`) and the
complete execution-visible evidence payload are carried forward unchanged
(PREP-003 held, §5.B below).

## 5. Deterministic validation (OBSERVED_FACT — actually executed)

- **GATE-W′ full rerun, both roles** (composition changed — §14): ALL TWELVE
  assertions EXACT PASS for BOTH roles; `all_pass=True` under the PREP-001
  exact-equality rule; assertions 7/8/9 NON-VACUOUS (every initial shell
  entry — bash/zsh/sh via /usr/bin and /bin — crossed the wrapper with the
  marker observed; credential paths absent; `/proc` cross-access impossible;
  writable set exactly the specification incl. the new
  `/auditor-tools/bin` + `/auditor-tools/shells` ephemeral parents of
  read-only binds); assertion 10 through the REAL pinned clients both roles
  (Auditor-B now including the REM-002 oracle + differential control inside
  the assertion evidence); assertion 11 writable-set byte-equality net vs
  no-egress; assertion 12 report screen. `evidence/gate-w-prime/`.
- **NORMAL_EXIT_BOUNDARY_PROCESS_TREE_QUIESCENCE**: PASS both role layouts
  (lingering descendants incl. a credential-fd holder and a double-forked
  grandchild all dead after normal exit; zero synthetic marker bytes on
  host).
- **REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION**: PASS both roles at exact-PASS
  strength, now with the REAL codex tool path wrapper-interposed (the REM-002
  closure is embedded in the evidence); `CLIENT_IN_PROCESS_READ_PROTECTION`
  remains the APPLICATION_LEVEL residual class (unchanged classification,
  mechanically demonstrated write/deny evidence retained).
- **Identity linter**: ALL checks PASS both roles (component digests incl.
  the native wrapper/probe-true/sentinel rows; evidence-payload-vs-manifest
  git-blob consistency; EXTENDED A=B parity incl. the new shared boundary
  rows).
- **Negative controls N1–N10 ALL PASS** (`evidence/negative-controls.json`),
  including the NEW N9 (one flipped byte in the staged NATIVE wrapper →
  accepted-EBS `verify_event_package` REFUSES under the unchanged frozen
  identity; restore re-verifies clean) and N10 (A=B byte parity of every
  shared boundary component: launcher, native wrapper, wrapper source,
  sentinel, probe-true, real-zsh bytes, boundary-bwrap bytes).
- **Synthetic-identity EBS dress rehearsal** through the REAL successor
  launcher + REAL frozen output-validator + accepted EBS: `REPORT_FROZEN`,
  mode 0444, full hash-chained state chain, `real_attempt_ids_touched: []`.
- **Validation sweep all_pass**: live network-readiness NON-INFERENCE
  connect-only validation PASS both roles (recorded as validation evidence
  only; the frozen bindings carry NO runtime-gate result, by contract);
  offline resource-gate + output-validator PASS; hygiene census clean;
  secret-shape scan ZERO hits; protected trees re-verified EXACT at the base.
- **Deterministic batteries ACTUALLY RE-EXECUTED** in an isolated detached
  worktree at the EXACT base `75706e8b` (then removed): `compileall` exit 0;
  **EBS battery 489/489 PASS; qualification-harness battery 221/221 PASS**
  (host CPython 3.14.7 + pytest 9.1.1 isolated venv). These are REGRESSION
  verification runs — bootstrap-supervisor, qualification-harness and skill
  bytes are UNCHANGED in this remediation (NOT a changed EBS/qh candidate);
  `TEST_ENVIRONMENT_DIVERGENCE` limitation retained.

**Held accepted invariants (§15) — regression clean:**
- PREP-001: exact-PASS aggregation and fail-closed freeze unchanged and
  re-exercised (N1/N2; the frozen gate evidence carries twelve EXACT PASS
  both roles); assertion 10 re-demonstrated through the REAL pinned clients
  both roles with zero inference.
- PREP-003: execution-visible evidence remains package-internal and bound
  only from the frozen package (N7); EBS per-file verification before
  GATES_PASSED unchanged (N4/N6 mutation refusals re-exercised incl. the new
  wrapper row, N9); identities cross-consistent with complete A=B evidence
  parity (N8 + linter). The common-evidence manifest member set and digests
  are byte-identical to S1.

## 6. Disclosed residuals / completeness limitations (NONE converted to PASS)

1. `CLIENT_IN_PROCESS_READ_PROTECTION` remains the APPLICATION_LEVEL residual
   class (design S15.3.5/readback S10) — unchanged classification.
2. `NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE` — unchanged disclosed residual;
   endpoint-only egress NOT claimed.
3. Composition-layering semantics of the adopted wrapper design (the wrapper's
   designed ephemeral writable set is re-materialized in the fresh tool
   namespace; every host-backed/evidence path remains denied at both layers)
   — unchanged honest disclosure; the differential control now additionally
   demonstrates the unwrapped-path `/proc/1/root` credential reachability
   that the wrapper's fresh PID namespace removes.
4. The mock-transport proofs exercise the clients through transport-only
   configuration additions (disclosed verbatim in the evidence documents);
   the permission/sandbox semantics under proof were loaded from the exact
   frozen files. A REAL first pass remains event-time evidence requiring
   separate operator execution authority.
5. The engine OBSERVATION run shadows `/auditor-tools/bin/bwrap` with a
   logging shim (records argv, then execs the real pinned engine) — an
   OBSERVATION-ONLY composition disclosed in
   `evidence/rem002/engine-observation.json`; every isolation/permission
   proof runs in the REAL composition without the shim.
6. The two BOUNDARY_SETUP rows (launcher host-interpreter class; INNER
   bootstrap materializing the credential home before client exec) remain
   host-interpreter executions OUTSIDE the §5/§9 closure (disclosed in the
   inventory, not silently omitted). Eliminating them (a native inner-init)
   was NOT required by the authority and would ADD credential-handling TCB.
7. `TEST_ENVIRONMENT_DIVERGENCE` retained (historical `/mnt/archlinux` JSON
   C-recursion behavior not re-tested; actual event-runtime compatibility
   remains an S1 evidence obligation).
8. Code Mode unavailability observation (prior readback, INFORMATIONAL) —
   unchanged; not promoted, not deleted.

## 7. Zero-execution attestation (OBSERVED_FACT)

Provider/model/frontier inference: ZERO (the only "model responses" the
clients processed were fixed scripted bytes from the local deterministic mock
— no model, no real provider request; the mock was reachable only on loopback
inside isolated `--unshare-net` namespaces). Prompts to providers: ZERO.
`/audit-council`: ZERO. Auditor-A/B executions: ZERO. Real credential bytes
read/hashed/logged: ZERO (synthetic markers only). Real attempt ids
consumed/referenced: ZERO (`real_attempt_ids_touched: []`; reserved
workspaces empty; no accounting record). Bootstrap-supervisor /
qualification-harness / skill mutations: ZERO (protected trees verified EXACT
before and after; batteries re-executed in a detached worktree that was
removed). Frozen target mutation: ZERO. Historical workspace mutations: ZERO
(371 rows re-verified byte-exact). Qualifications/installations: NONE.

## 8. Repository changes (this publication)

Changed paths EXACTLY: NEW this record + `AUCDEV-CURRENT-STATE.md` (header +
current-facing fields + dated record) + `AUCDEV-BACKLOG.md` (dated record) +
the bounded factual AUCDEV-023 continuation in
`AUCDEV-ARCHITECTURE-SUMMARY.md` (trust-boundary FACTS changed: NATIVE
static-pie wrapper interposed at bash AND zsh; package-pinned engine at every
level incl. the outer composition; pinned probe-true; real shells at
`/auditor-tools/shells/{bash,zsh}`; boundary sentinel; AUCDEV_TOOL_DOMAIN
marker). NO bootstrap-supervisor, qualification-harness, skill, runbook,
protocol, qualification-history, prior-record or frozen-target byte is
modified. All event-package/workspace evidence stays OUTSIDE Git. Pre-existing
working-tree material (smoke-fixture gitlink drift, evidence directories)
preserved unstaged.

## 9. Disposition (REQUIREMENT — evidence-derived)

```
AUCDEV_023_S1_PREP002_REM002_REMEDIATION =
IMPLEMENTED / SUCCESSOR_PACKAGES_FROZEN / AWAITING_CONTROL_ROOM_READBACK

AUCDEV023-CR-S1-PREP-002 = REMEDIATION_IMPLEMENTED / AWAITING_CONTROL_ROOM_READBACK
AUCDEV023-CR-S1-REM-002  = REMEDIATION_IMPLEMENTED / AWAITING_CONTROL_ROOM_READBACK

GATE_W_PRIME (successor evidence) =
TWELVE_ASSERTIONS_EXACT_PASS_BOTH_ROLES / ZERO_PROVIDER_ZERO_INFERENCE /
REAL_TOOL_PATH_WRAPPER_INTERPOSED_WITH_CAUSAL_DIFFERENTIAL_CONTROL

PREP-001 / PREP-003 held invariants = REGRESSED CLEAN
HISTORICAL GENERATIONS = BYTE-IDENTICAL (371/371 rows verified)

EVENT evt-7df609ec6c569043 = PRESERVED (no replacement event/attempt minted)
REAL_ATTEMPTS = NOT STARTED / NOT CONSUMED
MODEL_ENGAGEMENTS_USED_UNDER_THIS_AUDIT_POLICY = 0
REAL_PROVIDER_CALL_AUTHORITY = NONE
AUDITOR_A_EXECUTION_AUTHORITY = NONE
AUDITOR_B_EXECUTION_AUTHORITY = NONE
MODEL_ENGAGEMENT_EXECUTION_AUTHORITY = NONE
QUALIFICATION_AUTHORITY = NONE
INSTALLATION_AUTHORITY = NONE
qualification = NONE
installation = NONE
```

Implementation completion is NOT Control Room closure. Even if every
remediation gate is accepted, a REAL first-pass execution requires a NEW
explicit operator execution authority after independent Control Room review.

## 10. Next action — EXACTLY ONE

```
INDEPENDENT CONTROL ROOM READBACK OF THE AUCDEV-023 S1 PREP-002 / REM-002
EXECUTION-BOUNDARY REMEDIATION EVIDENCE AND THE COMPLETE NEW
SUCCESSOR-PACKAGE BYTE HANDOFF
```

No auditor launch, no real credential use, no model execution and no
qualification/install activity follows automatically from this publication.

## 11. Generated-LAST handoff archive (OBSERVED_FACT)

After ALL remediation work, tests, the final commit, push and the
independent GitHub readback are complete, exactly ONE non-secret `.tar.gz`
handoff archive is generated LAST containing the COMPLETE actual regular-file
bytes of BOTH new successor packages (every manifest row), both new bindings,
the native wrapper + probe-true sources/binaries/build/ELF evidence, the
complete authority-path inventory, shell-entry coverage, the real-client
zero-inference proof, the differential control, GATE-W′ A/B evidence,
quiescence/isolation evidence, PREP-001/PREP-003 regression evidence,
package/linter verification evidence, deterministic test results, historical
immutability proof, the canonical publication files, the exact diff/commit
metadata/GitHub readback and the finding/disposition inventory, with exactly
one SHA256SUMS covering every payload regular file except itself. Its
path/SHA-256/size/census are recorded in this session's final return.
Nothing is mutated after archive generation.
