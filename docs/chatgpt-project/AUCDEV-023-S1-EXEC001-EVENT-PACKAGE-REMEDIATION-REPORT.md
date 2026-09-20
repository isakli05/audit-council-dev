# AUCDEV-023 — S1 EXEC-001 Event-Package Remediation Report (Canonical Record)

| Field | Value |
|---|---|
| Status | **`AUCDEV_023_S1_EXEC001_REMEDIATION = IMPLEMENTED / NEW_SUCCESSOR_PACKAGES_FROZEN / AWAITING_CONTROL_ROOM_READBACK`** — implementer-strength remediation evidence ONLY. NOT Control Room closure, NOT `EXEC-001 CLOSED`, NOT execution readiness, NOT auditor authorization, NOT audit PASS, NOT qualification, NOT installation, and NO execution authority of any kind. |
| Session class | BOUNDED ZERO-PROVIDER REMEDIATION IMPLEMENTER SESSION under operator authority `AUCDEV-023-S1-EXEC001-REM-20260921-01`; the selected IMPLEMENTER (Claude Code + GLM-5.3) only — NOT the Control Room, NOT an independent auditor, NOT Auditor-A/B, NOT a launch controller, NOT a qualification or installation authority; ZERO provider/model/frontier executions, ZERO real credential reads, ZERO real attempt consumption, ZERO AccountingStore real-attempt creation, ZERO GATES_PASSED, ZERO CONSUMED_PRE_EXEC, ZERO `/audit-council`, ZERO network activity (the live network-readiness validation was NOT rerun — its frozen bytes are unchanged and this authority permits zero network activity), no real-client rehearsal of any kind (GATE-W′ / isolation / dress evidence carried forward as mechanically unaffected — the boundary composition is byte-identical) |
| Date | 2026-09-21 (Europe/Istanbul) |
| Authorized finding ONLY | `AUCDEV023-CR-S1-EXEC-001` RESOURCE_GATE_VALIDATES_STALE_ATTEMPT_WORKSPACE_ROOT |
| Exact implementation base | `5797884ba7fa83d1e1c8bdc9ae25e2e73c606edb` (tree `ab8407e6b45c5cb4e499ab4507fb6a2bb98388ee`; sole parent `0fccfc27d924b840a03dacb8041324d71d65e089`), resolved EXACT as live GitHub `master` AND local HEAD at bootstrap and re-resolved immediately before staging and push; protected trees verified EXACT at every checkpoint: bootstrap-supervisor `09f3d6c7ddc00305986cbedad431395c10c95af0`, qualification-harness `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill `c792933a862d9a5434681a88d183470dd8b15d2f` (qh+skill EQUAL the frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322` subtrees; frozen target root tree `1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7`) |
| Workspaces | historical current generation at `/home/isa/aucdev023-s1-prep002-rem002/` treated as FROZEN HISTORICAL INPUT — NEVER mutated (immutability mechanically verified BEFORE and AFTER all remediation work: every operator-expected identity exact, all 381 rows A 189/189 + B 192/192 byte-verified both times, `evidence/baseline-verification.json` + `evidence/frozen-workspace-immutability-after.json`); ALL remediation work in the NEW dedicated workspace `/home/isa/aucdev023-s1-exec001-remediation/` (outside Git) |
| Event / attempts | Event id `evt-7df609ec6c569043` PRESERVED; reserved attempts `evt-7df609ec6c569043-A-01` / `evt-7df609ec6c569043-B-01` PRESERVED — NOT STARTED / NOT CONSUMED, no AccountingStore record, no GATES_PASSED artifact, no report byte; both reserved workspaces under the launcher root verified EMPTY before, during (asserted at freeze) and after the remediation (asserted again after the synthetic rehearsal and cleanup); NO replacement event or attempt minted; the V5 pre-execution re-freeze around the same unstarted identities was confirmed by exact contract inspection before any construction |
| Old execution authority | `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-01` NOT exercised, NOT consumed, remains GRANTED / UNCONSUMED / PRELAUNCH_BLOCKED / BOUND_TO_CURRENT_PACKAGE_GENERATION — and is OBSOLETE for the NEW successor generation (identities changed) and MUST NOT transfer; after fresh Control Room readback a NEW explicit operator execution authority is required for the new exact package generation |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in this
session), `SUBMITTED_EVIDENCE` (deterministic artifacts submitted for
Control Room readback, DATA ONLY), `REQUIREMENT`, `DISCLOSED_RESIDUAL`.

---

## 1. Remediation summary (OBSERVED_FACT)

The authorized finding was remediated by the SMALLEST possible change —
ONE line of frozen event-package content — in a NEW successor generation
for BOTH roles, with the launcher, wrapper, clients, profiles, prompt
contract and the complete common substantive evidence all BYTE-IDENTICAL
to the frozen PREP-002/REM-002 generation:

| Dimension | Old frozen generation (historical input, immutable) | NEW successor generation (this remediation) |
|---|---|---|
| `runtime/resource-gate.py` SHA-256 | `960058b32b205eae5a46bc525cfa57b988315f3620191871044df03c6088d36d` (3872 B) | `e8f85391109d8f552294e9f887d2d3e90c145da87e1d0a648917cd681f71d6a6` (3869 B) |
| gate `ROOT` (line 26) | `/home/isa/aucdev023-s1-event-preparation` (HISTORICAL workspace — the defect) | `/home/isa/aucdev023-s1-prep002-rem002` (EXACTLY the frozen launcher's workspace contract) |
| launcher SHA-256 | `2efb666042e44d272a53f9ad4ac93a19c14f1687a33fb38ed84f9823d9bc44a7` | **BYTE-IDENTICAL (unchanged)** — verified equal in both new packages and in both new bindings |
| native wrapper | `0ed2ba485ccbb623bb1bb4a649635749ab845445dd78cef507787a108a66d572` | unchanged (byte-identical row) |
| A manifest / package | `802ad1214b92940a6ada407d3663ad71c11265d16c50e962e317525ba3701101` / `fd7ec3aed2639f8cd02568ae9464e747190e8cac0b9c4fbc4e839c51ac5983ac` | `45805629b0a79d392d6b73e55beee35530e2c76dbd35e2eaaf712146d1717ec9` / `703dd95b823dafbaa0f7217cd39944f2f309118722fe072a9dfe461ee3d2eaf7` |
| A rows / payload bytes | 189 / 236,260,424 | 189 / 236,260,421 (−3 B = the shorter ROOT string; NO row added/removed) |
| A binding file / canonical digest | `579d32f1e0e8d6d71045277c6b76e9b348b60de8dcbeac3cf55e59956c226cc2` / `316f6d3659c757a47d02581556f4829c0f18e672e6388d84eb42667bc6ead25f` | `9cb8002fa2039309b6c9eeb3fde21dd97c8b239f8a988dc26e86d9af1a493df5` / `5c48fa3f432dff7648a78e454e4f77ee00c4811ba0b7e60439a0fb5827e18202` |
| B manifest / package | `4b2b77cb30866911a75665322cb55d37b30d245b2290ba8e47c1abfc564aea62` / `8573e16285e4b5cceb96bb1cb92d0216bc540c084fad28ef25e213cb069537ab` | `5c1421aeece04f7fabb96f3fcbdd91c64bc50e83a50e9f7d0f24babbdcd9fae3` / `23131e88d71ff18fc3b2d9d549f5fe5427c2bd3849a0fa969767a1917432e0e9` |
| B rows / payload bytes | 192 / 343,391,385 | 192 / 343,391,382 (−3 B; NO row added/removed) |
| B binding file / canonical digest | `66ccc5d897f477254d83e9c58a6b42a6fc5400861527a84605dd2083ca516a0d` / `6fe3ebc9978cbf2f764347d3134f6aa141698753a06c5f84f528bbd8b6d82c33` | `12f8930878e6c076c1e282269062f00d769f1f6a541cc810d825e4bd66d40cd2` / `f088b1327f171cd3fdac2163c13a46515de166dfad630bdbe8073512eab2fd85` |
| common substantive evidence | `ebddcd60…` manifest / `ff116a9d…` projection (167 members) | **BYTE-IDENTICAL** (regenerated from the same frozen inputs and verified byte-equal) |
| V5 schema / tokens | V5; launcher `NETWORKED-BOUNDARY-LAUNCHER-V1`; wrapper `AUCDEV023-TOOL-DOMAIN-WRAPPER-V1` | UNCHANGED (no V6; no token change) |
| frozen invocations | `claude -p …` / `codex exec --skip-git-repo-check --profile aucdev023-c3 …` | UNCHANGED (byte-identical bindings fields) |

## 2. Exact change discipline (OBSERVED_FACT)

A full row-by-row comparison of the NEW generation against the FROZEN
generation (`evidence/generation-diff-vs-frozen.json`) proves the change
set is EXACTLY four files per package and NOTHING else:

```
runtime/resource-gate.py                 (the authorized one-line change)
evidence/identity-linter.json            (identity-derived regeneration)
evidence/package-binding-identity.json   (identity-derived regeneration)
MANIFEST.json                             (identity-derived regeneration)
```

- stage-1 safety check (before any evidence assembly): staged trees
  differed from the frozen generation in `runtime/resource-gate.py` ONLY;
- post-freeze full-tree check: no row added, no row removed, no other row
  changed; row counts remain 189 / 192 EXACTLY as the authority expected;
- the new gate differs from the old gate by EXACTLY ONE line (line 26,
  the `ROOT` assignment), verified by `diff`;
- identity-derived regeneration is NOT treated as substantive evidence
  drift: the GATE-W′, blindness-map and real-client credential/tool
  isolation evidence documents inside the packages are the SAME BYTES as
  the frozen generation (their binding `gate_evidence` SHA entries are
  unchanged for those gates), because the boundary composition they
  rehearsed is byte-identical;
- the linter was RERUN against the new packages with regenerated facts
  (ALL PASS both roles — its output embeds the new component digests);
  `package-binding-identity.json` was regenerated by the same accepted
  builder code path (its `component_sha256` map now carries the new gate
  identity).

## 3. Workspace-contract proof (§9 — SUBMITTED_EVIDENCE)

`evidence/workspace-contract-verification.json` records, for BOTH roles:
launcher SHA + ROOT, RESOURCE_GATE SHA + ROOT, exact event/attempt ids,
binding-derived output artifact name, intended
`report_staging_path` / `output_root` / `accounting_root`, and the
equality checks. Required final relationships ALL hold:

```
RESOURCE_GATE_ROOT == LAUNCHER_ROOT == /home/isa/aucdev023-s1-prep002-rem002
classification: EXACT_MATCH (both roles; problems: [])
```

with per-role intended operator paths derived EXACTLY as:

```
report staging directory = ROOT/attempts/<attempt>/staging
report_staging_path      = ROOT/attempts/<attempt>/staging/<attempt>.first-pass-report.json
custody/output root      = ROOT/attempts/<attempt>/custody-out
accounting root          = ROOT/attempts/<attempt>/accounting
```

and the reserved attempt workspaces verified present and EMPTY (0 files)
under that root. This is PREPARATION EVIDENCE ONLY — no AccountingStore
was created for either real attempt and `Supervisor.run_attempt` was
never called.

## 4. Non-vacuous negative controls (§10 — SUBMITTED_EVIDENCE)

`evidence/exec001-negative-controls.json` — ALL PASS:

- **N1** the HISTORICAL pair (gate ROOT
  `/home/isa/aucdev023-s1-event-preparation` vs launcher ROOT
  `/home/isa/aucdev023-s1-prep002-rem002`) is classified
  `ROOT_MISMATCH / FAIL` by the same deterministic checker used for the
  production verification (not a narrative string comparison);
- **N2** the NEW pair is classified `EXACT_MATCH / PASS`;
- **N3** a planted one-byte mutation of the NEW
  `runtime/resource-gate.py` without manifest/binding regeneration is
  REFUSED by the accepted EBS `verify_event_package` under the unchanged
  new binding identity; byte-exact restore re-verifies clean;
- **N4** descriptor substitution fails closed BOTH directions: (a) a
  binding carrying the HISTORICAL gate SHA
  (`960058b3…`) against the package carrying the NEW gate bytes is
  REFUSED (transport-projection mismatch), and (b) the NEW binding
  against the FROZEN historical package is REFUSED (package identity
  mismatch);
- **N5** synthetic workspace contracts changing exactly ONE of
  staging / custody-out / accounting to a different root are each
  classified `FAIL` by the checker.

## 5. Zero-inference RESOURCE_GATE rehearsal (§11 — SUBMITTED_EVIDENCE)

`evidence/resource-gate-synthetic-rehearsal.json`: the EXACT new frozen
gate bytes were executed (both roles' package artifacts) with
UNMISTAKABLY SYNTHETIC probe attempt ids `evt-exec001probe-A-01` /
`evt-exec001probe-B-01` — a namespace disjoint from every reserved real
attempt id. Observed: rc 0; strict envelope
`AUCDEV-023-RESOURCE-GATE-RESULT-V1` with `status: PASS`; exactly three
samples ALL PASS; event/role/attempt echoed exactly; the gate CREATED
exactly `{staging,custody-out,accounting}` for each probe UNDER THE
ACTUAL LAUNCHER ROOT `/home/isa/aucdev023-s1-prep002-rem002/attempts/`
(mechanical proof the sampled root is the launcher root — the EXEC-001
defect class cannot recur in this composition); `sampled:
attempt-workspace`; staging/custody-out/accounting all writable=true.
Invariants: both reserved real attempt workspaces EMPTY and UNCHANGED
before/after; the HISTORICAL workspace listing unchanged (read-only);
probe artifacts were the ONLY things created and were COMPLETELY REMOVED
after evidence capture (cleanup verified). No provider, no credential, no
model, no auditor, no `Supervisor.run_attempt`, no AccountingStore; ZERO
engagement authority consumed.

## 6. Prelaunch operator-path dry proof (§12 — SUBMITTED_EVIDENCE)

`evidence/launch-plan-auditor-a.json` + `evidence/launch-plan-auditor-b.json`
(DATA-ONLY; NOT authority; launches nothing): for each role the future
exact operator values — `event_package_root`, `binding path`,
`launcher_path`, `auditor_executable_path`, `report_staging_path`,
`output_root`, `accounting_root` — with mechanically verified package
and binding identities, launcher identity, auditor executable identity
(equal to the binding pin), binding-derived output artifact name
relation, and all three writable attempt roots agreeing with the
RESOURCE_GATE's frozen ROOT. DISCLOSED DEPLOYMENT FACT (recorded in the
artifacts): the byte-identical launcher resolves its package tree from
its own frozen ROOT, so the NEW successor generation bytes must be
deployed AT that ROOT's `event/` location (replacing the historical
generation's files there) before any real launch — a future operator
action under a NEW explicit execution authority, NOT performed by this
remediation session; the plan states both the current staging source
(this workspace) and the deployed destination, and requires the deployed
bytes to verify to EXACTLY the NEW identities.

## 7. Affected regressions and held invariants (§13/§14 — OBSERVED_FACT)

- Strict V5 binding parse (accepted EBS `parse_binding`) BOTH roles PASS
  (canonical digests above); binding transport projections equal the
  package transport bindings (verified inside
  `verify_event_package`).
- Strict manifest parse + complete row ↔ regular-file equality + every
  row size/SHA + non-circular package identity: A 189/189, B 192/192
  (`evidence/new-generation-identity-inventory.json`).
- `ebs.launch.verify_event_package` BOTH roles PASS (the pre-GATES_PASSED
  authority verification every Supervisor construction performs).
- Package identity linter: ALL PASS both roles (11 checks each).
- A=B common substantive evidence parity: shared components byte-equal
  (launcher, wrapper, wrapper source, sentinel, probe-true, real-zsh,
  boundary-bwrap, resource-gate, output-validator, network-readiness);
  complete staged evidence payload 169 files compared, ZERO differences.
- Shared launcher parity + launcher byte-equality to the prior
  generation: `2efb6660…` IDENTICAL both packages and IDENTICAL to the
  frozen historical launcher.
- RESOURCE_GATE descriptor equality: binding descriptor SHA == actual
  package gate bytes == `e8f85391…` both roles.
- Workspace-contract checks N1–N5 ALL PASS (§4).
- Deterministic synthetic RESOURCE_GATE rehearsal PASS (§5).
- Historical current-package immutability: frozen generation verified
  EXACT before AND after all work (§ Workspaces above).
- Regression rerun of the accepted PREP002/REM-002 negative-control
  suite (N1–N10 classes) against the NEW generation: ALL PASS
  (`evidence/negative-controls.json`) — exact-PASS-only aggregation and
  fail-closed freeze (PREP-001), runtime-closure and evidence-payload
  mutation refusals by the EBS (PREP-003 byte binding), no external
  evidence mounts, identity cross-consistency, native-wrapper mutation
  refusal, A=B shared-boundary parity (REM-002). The one adapted check
  (the closure anchor) now verifies the launcher-resolved package
  location relative structure PLUS byte-equality of the staged
  executable against the launcher-resolved location — the honest form
  of the same invariant in a new-workspace build (the adapted scripts
  with their bounded adaptations are in the handoff).
- Validation sweep all_pass (`evidence/validation-sweep.json`): offline
  resource-gate validation with a SYNTHETIC probe attempt PASS through
  the exact new frozen bytes; output-validator offline validation PASS;
  hygiene census clean both packages; secret-shape scan ZERO hits;
  protected trees re-verified EXACT at the exact base. The live
  network-readiness probes were deliberately NOT rerun (unchanged
  frozen bytes; zero network activity under this authority) and are
  recorded as SKIPPED, never as PASS.
- Deterministic batteries ACTUALLY RE-EXECUTED in an isolated detached
  worktree at the EXACT base `5797884b` (then removed):
  `compileall` exit 0; **EBS battery 489/489 PASS; qualification-harness
  battery 221/221 PASS** (host CPython 3.14.7 + pytest 9.1.1 isolated
  venv). REGRESSION verification only — protected source bytes are
  UNCHANGED in this remediation (NOT a changed EBS/qh candidate);
  `TEST_ENVIRONMENT_DIVERGENCE` limitation retained.
- GATE-W′ accepted evidence, blindness maps and real-client
  credential/tool-isolation evidence CARRIED FORWARD byte-identical
  (mechanically unaffected: the boundary composition they rehearse is
  byte-identical in this generation); no real-client rehearsal was run
  under this authority. PREP-001/-002/-003 and REM-001/-002 are NOT
  reopened (no contradictory evidence; their held invariants regressed
  clean above).

## 8. Disclosed bounded builder adaptations (OBSERVED_FACT)

The new generation was built in the new workspace by the SAME accepted
builder code with exactly three disclosed adaptations (adapted scripts
included verbatim in the handoff): (1) workspace root constants point at
the new workspace, with all inputs byte-identical copies of the frozen
generation except the one-line gate change; (2) the real attempt-workspace
reservation was REPLACED by a read-only assertion that the reserved
workspaces already exist EMPTY under the LAUNCHER root (the builder never
creates or mutates anything there); (3) the validation sweep skips the
live network-readiness probes (unchanged bytes; zero network under this
authority) and uses a synthetic probe attempt id for the offline gate
validation instead of the historical real-attempt-id usage. Runtime and
boundary closures still stage from the live installed sources exactly as
the accepted builder did — the live sources were verified to hash
IDENTICALLY to the frozen identities before staging (`claude.exe`
`15e2d051…`, codex `3188814c…`, bwrap `01fb705f…`, zsh `67faaaa8…`, rg
`e62198eb…`, code-mode-host `0c57be43…`).

## 9. Repository changes (this publication)

Changed paths EXACTLY: NEW this record
(`AUCDEV-023-S1-EXEC001-EVENT-PACKAGE-REMEDIATION-REPORT.md`) +
`AUCDEV-CURRENT-STATE.md` (header + current-facing fields + dated record
+ next-operator-action rotation) + `AUCDEV-BACKLOG.md` (dated record) +
ONE small bounded factual continuation in
`AUCDEV-ARCHITECTURE-SUMMARY.md` (the runtime-gate workspace-contract
fact of the new generation; no architecture redesign; adopted R1
architecture/policy semantics unaltered; append-only prior records
untouched). NO bootstrap-supervisor, qualification-harness, skill,
runbook, protocol, qualification-history, prior-record or frozen-target
byte is modified. All event-package/workspace evidence stays OUTSIDE
Git. Pre-existing working-tree material (smoke-fixture gitlink drift,
evidence directories) preserved unstaged.

## 10. Zero-execution attestation (OBSERVED_FACT)

Provider/model/frontier inference: ZERO. Real credential bytes
read/hashed/logged: ZERO. Auditor-A/B / `/audit-council` executions:
ZERO. `Supervisor.run_attempt`: ZERO calls (for reserved OR synthetic
attempts). AccountingStore creation for `evt-…-A-01` / `evt-…-B-01`:
ZERO. GATES_PASSED / CONSUMED_PRE_EXEC / EXEC_ATTEMPTED: ZERO. Real
attempt ids sampled by any gate execution: ZERO (synthetic
`evt-exec001probe-*` only). Historical frozen workspace mutations: ZERO
(verified before/after). Protected tree mutations: ZERO (verified at
bootstrap, after construction, and immediately before staging).
Qualification/installation: NONE. Network activity: ZERO (no live
network-readiness validation; no external requests). The old execution
authority was NOT exercised and does NOT transfer to this generation.

## 11. Disposition (REQUIREMENT — evidence-derived)

```
AUCDEV_023_S1_EXEC001_REMEDIATION =
IMPLEMENTED / NEW_SUCCESSOR_PACKAGES_FROZEN / AWAITING_CONTROL_ROOM_READBACK

AUCDEV023-CR-S1-EXEC-001 = REMEDIATION_IMPLEMENTED / AWAITING_CONTROL_ROOM_READBACK
  (implementer disposition ONLY — implementation completion is NOT Control
   Room closure and this report does NOT claim EXEC-001 CLOSED)

WORKSPACE_CONTRACT = RESOURCE_GATE_ROOT == LAUNCHER_ROOT ==
  /home/isa/aucdev023-s1-prep002-rem002 (EXACT_MATCH both roles)

EVENT evt-7df609ec6c569043 = PRESERVED (no replacement event/attempt minted)
REAL_ATTEMPTS = NOT STARTED / NOT CONSUMED
MODEL_ENGAGEMENTS_USED_UNDER_THIS_AUDIT_POLICY = 0
OLD_AUTHORITY AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-01 = UNCONSUMED /
  NOT TRANSFERABLE TO THE NEW GENERATION
REAL_PROVIDER_CALL/AUDITOR_A/AUDITOR_B/MODEL_ENGAGEMENT/QUALIFICATION/
INSTALLATION AUTHORITY = NONE
qualification = NONE
installation = NONE
AUCDEV-023 = P1 / READY / NOT DONE (counts unchanged: READY 9 / OPEN 7 /
BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11 — no backlog-row transition)
```

## 12. Next action — EXACTLY ONE

```
INDEPENDENT CONTROL ROOM READBACK OF THE EXEC-001 REMEDIATION,
WORKSPACE-CONTRACT EVIDENCE, AND COMPLETE NEW SUCCESSOR-PACKAGE
BYTE HANDOFF
```

No auditor launch, no real credential use, no model execution and no
qualification/install activity follows automatically from this
publication. Even if the readback accepts every gate, a REAL first-pass
execution requires a NEW explicit operator execution authority for the
NEW exact package generation (the old authority is bound to the
historical generation and MUST NOT transfer).

## 13. Generated-LAST handoff archive (OBSERVED_FACT)

After ALL remediation work, tests, the final commit, push and the
independent GitHub readback are complete, exactly ONE non-secret
`.tar.gz` handoff archive is generated LAST containing the COMPLETE
actual regular-file bytes of BOTH new successor packages (every manifest
row: A 189 + B 192 + MANIFEST.json), both new bindings, the new
RESOURCE_GATE actual bytes, the unchanged launcher bytes, the
workspace-contract verification, the synthetic rehearsal evidence, the
N1–N5 controls, the regression controls, the future operator launch-plan
DATA artifacts, package/binding/linter/identity verification, the
generation diff, held-invariant regression evidence, EBS and qh battery
outputs, historical immutability evidence, the canonical publication
files, the exact diff/commit metadata/GitHub readback and the
finding/disposition inventory, with exactly one SHA256SUMS covering
every payload regular file except itself. Its path/SHA-256/size/census
are recorded in this session's final return. Nothing is mutated after
archive generation.
