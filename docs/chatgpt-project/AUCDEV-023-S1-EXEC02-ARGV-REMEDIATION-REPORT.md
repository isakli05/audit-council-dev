# AUCDEV-023 — S1 EXEC02-001/002 RESOURCE_GATE FD-EXEC Argv Remediation Report (Canonical Record)

| Field | Value |
|---|---|
| Status | **`AUCDEV_023_S1_EXEC02_ARGV_REMEDIATION = IMPLEMENTED / NEW_SUCCESSOR_PACKAGES_FROZEN / EXACT_EBS_FD_EXEC_REGRESSION_PASS / EXEC02_001_REMEDIATED_IN_SUCCESSOR / EXEC02_002_TEST_GAP_REMEDIATED_IN_SUCCESSOR / AWAITING_CONTROL_ROOM_READBACK / REAL_EXECUTION_NOT_AUTHORIZED`** — implementer-level disposition ONLY. NOT `EXEC02-001 CLOSED`, NOT `EXEC02-002 CLOSED` (only the Control Room may accept at readback strength), NOT execution readiness, NOT auditor authorization, NOT audit PASS, NOT qualification, NOT installation, and NO execution authority of any kind. |
| Session class | BOUNDED ZERO-PROVIDER REMEDIATION IMPLEMENTER SESSION under operator authority `AUCDEV-023-S1-EXEC02-ARGV-REM-20260921-01`; the selected IMPLEMENTER (Claude Code + GLM-5.3) only — NOT the Control Room, NOT an independent auditor, NOT Auditor-A/B, NOT an execution controller, NOT a qualification or installation authority; ZERO provider/model/frontier executions, ZERO real credential reads, ZERO real attempt consumption, ZERO AccountingStore creation, ZERO GATES_PASSED, ZERO CONSUMED_PRE_EXEC, ZERO `/audit-council`, ZERO network activity, no real-client rehearsal (GATE-W′ / blindness / isolation evidence carried forward byte-identical — the boundary composition is byte-identical) |
| Date | 2026-09-21 (Europe/Istanbul) |
| Authorized findings ONLY | `AUCDEV023-CR-S1-EXEC02-001` RESOURCE_GATE_EBS_ARGV_CONTRACT_MISMATCH (remediated in successor) + `AUCDEV023-CR-S1-EXEC02-002` SYNTHETIC_RESOURCE_GATE_REHEARSAL_DID_NOT_REPRODUCE_EBS_FD_EXEC_ARGV (test gap remediated in successor) |
| Exact implementation base | `5d8c233ce9a497296c998909da666993a55c5ec3` (tree `43b905deab16fcbbe7034326f2afeb3e98e93017`; sole parent `52c4bb2544affcf61b5851b593914d2988006141`), resolved EXACT as live GitHub `master` AND local HEAD at bootstrap and re-resolved immediately before staging and push; protected trees verified EXACT at every checkpoint: bootstrap-supervisor `09f3d6c7ddc00305986cbedad431395c10c95af0`, qualification-harness `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill `c792933a862d9a5434681a88d183470dd8b15d2f` (qh+skill EQUAL the frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322` subtrees) |
| Workspaces | accepted (EXEC-001 successor / EXEC-02-deployed) generation at `/home/isa/aucdev023-s1-prep002-rem002/event/` (deployed historical EXEC-02 execution evidence) AND `/home/isa/aucdev023-s1-exec001-remediation/event/` BOTH treated as FROZEN HISTORICAL INPUT — NEVER mutated (verified byte-exact BEFORE and AFTER all work: all 381 rows A 189/189 + B 192/192, both locations, `evidence/baseline-verification.json` + `evidence/accepted-workspace-immutability-after.json`; the two locations verified byte-identical to each other); historical backup `/home/isa/aucdev023-s1-prep002-rem002/event.backup.pre-exec02` verified 381/381 rows against its OLD_ACCEPTED identities; ALL remediation work in the NEW dedicated workspace `/home/isa/aucdev023-s1-exec02-argv-remediation/` (outside Git) |
| Event / attempts | Event id `evt-7df609ec6c569043` PRESERVED; historical A attempt `evt-7df609ec6c569043-A-01` = TERMINAL_PREEXEC_STOP / UNCONSUMED / MODEL-ENGAGEMENT-ZERO / MUST NOT BE REUSED — its accounting record (`PREPARED` → `TERMINAL_PREEXEC_STOP`, SHA-256 `d753df02…`) byte-UNCHANGED before/during/after (pinned `evidence/attempt-state-pin.json`; asserted at freeze; re-verified by every ARGV-5 control); B attempt `evt-7df609ec6c569043-B-01` = NOT STARTED (attempt tree pristine EMPTY throughout); NO replacement event or attempt minted |
| Historical execution authority | `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02` = NO FURTHER EXECUTION / NO SAME-ATTEMPT RETRY / NON-TRANSFERABLE to this remediated generation (event-package identity changed); no part of it was exercised by this session |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `SUBMITTED_EVIDENCE` (deterministic artifacts submitted
for Control Room readback, DATA ONLY), `REQUIREMENT`, `DISCLOSED`.

---

## 1. Remediation summary (OBSERVED_FACT)

The authorized finding was remediated in a NEW successor event-package
generation for BOTH roles by changing ONLY the frozen RESOURCE_GATE's
argv consumption (plus its docstring invocation-contract documentation)
— the SMALLEST substantive change the finding permits — with the
launcher, NETWORK_READINESS, wrapper, clients, profiles, prompt
contract, common substantive evidence, thresholds, sampling logic,
result schema and gate identity ALL BYTE-IDENTICAL to the accepted
generation:

| Dimension | Accepted generation (immutable historical input) | NEW successor generation (this remediation) |
|---|---|---|
| `runtime/resource-gate.py` SHA-256 / size | `e8f85391109d8f552294e9f887d2d3e90c145da87e1d0a648917cd681f71d6a6` (3869 B) | `27948980653f4c0639041243d9f117087f0987c5cc53623abbfa39cbb143adaf` (5528 B) |
| gate `main()` argv contract | `if len(sys.argv) < 5: return 3` / `_identity, event, role, attempt = sys.argv[1:5]` (the EXEC02-001 defect) | `if len(sys.argv) != 4: return 3` / `_script, event, role, attempt = sys.argv[0:4]` (event from `sys.argv[1]`, role `sys.argv[2]`, attempt `sys.argv[3]`; NEVER depends on the logical identity string surviving as a separate Python argv element) |
| gate ROOT / thresholds / sampling / schema / IDENTITY | `/home/isa/aucdev023-s1-prep002-rem002`; 2 GiB disk / 1 GiB mem / 6000 processes; three local samples; `AUCDEV-023-RESOURCE-GATE-RESULT-V1`; `AUCDEV023-RESOURCE-GATE-V1` | UNCHANGED (byte-identical code outside the two argv lines + docstring) |
| launcher SHA-256 | `2efb666042e44d272a53f9ad4ac93a19c14f1687a33fb38ed84f9823d9bc44a7` | **BYTE-IDENTICAL (unchanged)** — verified equal in both new packages and both new bindings |
| NETWORK_READINESS SHA-256 | `20f37e9191d3e1e025962723328c5f8a2849f664cf1bf215715ccf8da9fc7235` | **BYTE-IDENTICAL (unchanged)** both roles |
| auditor executables | A `15e2d05148f801b5774032faad87e624ecd172e9903288bda448b892eb58fa07`; B `3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022` | **BYTE-IDENTICAL (unchanged)** both roles (see §9 transcription note) |
| A manifest / package | `45805629b0a79d392d6b73e55beee35530e2c76dbd35e2eaaf712146d1717ec9` / `703dd95b823dafbaa0f7217cd39944f2f309118722fe072a9dfe461ee3d2eaf7` | `5b6bb4dc14ed94929af068ada567110c8fed7bfd113dad253babb811868b26e2` / `0670817a02b9b8f51b78066837c6abc6018fced6b52169e13391e29343d8a7bf` |
| A rows / payload bytes | 189 / 236,260,421 | 189 / 236,262,080 (+1659 B = the gate size delta; NO row added/removed) |
| A binding file / canonical digest | `9cb8002fa2039309b6c9eeb3fde21dd97c8b239f8a988dc26e86d9af1a493df5` / `5c48fa3f432dff7648a78e454e4f77ee00c4811ba0b7e60439a0fb5827e18202` | `140c43e4615e8de3af5d355b945a6fd8505e6b70ccd5a755aab92e5b33b9e9be` / `5de31410c3a44997ef52dfb10c849e110915b63ce829d061a6c09e07538e8d2b` |
| B manifest / package | `5c1421aeece04f7fabb96f3fcbdd91c64bc50e83a50e9f7d0f24babbdcd9fae3` / `23131e88d71ff18fc3b2d9d549f5fe5427c2bd3849a0fa969767a1917432e0e9` | `9c692e86c504d0447f3e9efb8fce4faf95f516783c2df6a0fbcb6bb627619ba6` / `e56708f9048297b3b214003c4b3480d6b123e4ca431aa9b688ebfa36e93533bf` |
| B rows / payload bytes | 192 / 343,391,382 | 192 / 343,393,041 (+1659 B; NO row added/removed) |
| B binding file / canonical digest | `12f8930878e6c076c1e282269062f00d769f1f6a541cc810d825e4bd66d40cd2` / `f088b1327f171cd3fdac2163c13a46515de166dfad630bdbe8073512eab2fd85` | `2e192073e74477bec5eef0f22e082f725fa7c562694b7a722c097636610187d0` / `4f5624be720ce75aa85b68953ffed00280bd83dc517fddb097de00a70068b6e0` |
| EBS package pins (both bindings) | manifest `68490d79…` / package `8685c36e…` | UNCHANGED (EBS source byte-identical; protected tree verified) |
| common-evidence manifest / projection | `ebddcd60…` / `ff116a9d…` (167 members) | **BYTE-IDENTICAL** (regenerated from the same frozen inputs, verified byte-equal) |
| V5 schema / tokens / invocations / profiles | V5; launcher `NETWORKED-BOUNDARY-LAUNCHER-V1`; wrapper `AUCDEV023-TOOL-DOMAIN-WRAPPER-V1`; frozen invocations | UNCHANGED (no V6; no token change) |
| gate ROOT workspace contract | `RESOURCE_GATE_ROOT == LAUNCHER_ROOT == /home/isa/aucdev023-s1-prep002-rem002` (EXACT_MATCH both roles) | UNCHANGED (EXEC-001's corrected ROOT preserved — the new defect was distinct) |

## 2. Exact change discipline (OBSERVED_FACT)

A full row-by-row comparison of the NEW generation against the ACCEPTED
generation (`evidence/generation-diff-vs-accepted.json`; every row of
BOTH generations byte-verified) proves the change set is EXACTLY three
payload files per package plus the root manifest and NOTHING else:

```
runtime/resource-gate.py                 (the authorized argv-contract change)
evidence/identity-linter.json            (identity-derived regeneration)
evidence/package-binding-identity.json   (identity-derived regeneration)
MANIFEST.json                             (identity-derived regeneration)
```

- stage-1 safety check (before any evidence assembly): the staged trees
  differed from the accepted generation in `runtime/resource-gate.py`
  ONLY;
- post-freeze full-tree check: no row added, no row removed, no other
  row changed; row counts remain 189 / 192 EXACTLY as the authority
  required; payload byte delta exactly +1659 per role (= 5528 − 3869,
  the gate size delta);
- the new gate differs from the accepted gate ONLY in (a) the docstring
  argv-contract section — which now documents the TWO DISTINCT notions
  (EBS LOGICAL gate binding/invocation identity vs PYTHON-VISIBLE
  sys.argv under the verified-fd/shebang execution path) exactly as the
  authority directed — and (b) the two `main()` argv lines; the ROOT,
  thresholds, sampling logic, result schema and IDENTITY are
  byte-identical (`evidence/resource-gate-old-to-new.diff`);
- the corrected gate adopts the SAME working convention the sibling
  frozen NETWORK_READINESS gate already demonstrates under this SAME
  EBS fd-exec/shebang path (script slot at `sys.argv[0]`, bound facts
  from `sys.argv[1:]`; NETWORK_READINESS requires exactly 7 for its
  seven-element EBS argv — consistent with NETWORK_READINESS passing in
  the real EXEC-02 attempt);
- the linter was RERUN against the new packages with regenerated facts
  (ALL PASS both roles, 11 checks each; its output embeds the new gate
  digest — `evidence/linter/`); `package-binding-identity.json` was
  regenerated by the same accepted builder code path; GATE-W′,
  blindness-map and real-client credential/tool-isolation evidence are
  the SAME BYTES as the accepted generation (their rehearsed boundary
  composition is byte-identical; binding `gate_evidence` SHA entries for
  those gates unchanged — `evidence/held-invariants.json`).

## 3. MANDATORY exact EBS fd-exec regression ARGV-1…ARGV-6 (SUBMITTED_EVIDENCE — closes the EXEC02-002 coverage gap)

`evidence/fdexec-argv-regression.json` (package mode, frozen package
gate bytes, BOTH roles). A direct `python resource-gate.py identity
event role attempt` invocation was NOT accepted as sufficient: the
harness imports the EXACT LIVE EBS SOURCE at the remediation base
(`/home/isa/audit-council-dev/bootstrap-supervisor`, with `HEAD ==
5d8c233…` and the protected bootstrap-supervisor tree `09f3d6c7…`
asserted at run time) and exercises the REAL internal path

```
verified open fd (O_NOFOLLOW, hash-the-open-fd, exact SHA equality, rewind)
→ launch._run_runtime_gate   (bounded fail-closed timeout, size-bounded pipe)
→ launch._gate_child         (fd discipline, no credential fd, non-dumpable)
→ launch.fd_exec             (execveat AT_EMPTY_PATH / fexecve, shebang)
→ the gate process's Python-visible sys.argv
```

with the SAME four-element EBS argv construction the production launch
used (`argv = [descriptor["identity"], binding.event_id,
binding.auditor_role, binding.attempt_id]`, env exactly
`{PATH: /usr/bin:/bin, LANG: C}`). ALL SIX CONTROLS PASS:

- **ARGV-1 HISTORICAL NEGATIVE** — the OLD gate bytes (verified
  `e8f85391…`, opened from the deployed accepted package) through the
  exact fd-exec path with a synthetic probe: REFUSED
  `RESOURCE_GATE_NONZERO_EXIT: exited 3`, no result bytes, and the
  probe workspace directory NOT created — mechanically reproducing the
  observed EXEC-02 production failure and proving the refusal happens
  BEFORE resource sampling (the failure is NOT evidence of low disk,
  memory or process count);
- **ARGV-2 CORRECTED POSITIVE** — the NEW gate bytes (frozen package
  bytes of BOTH roles; both verified `27948980…`) through the SAME path
  with synthetic probes `evt-exec02argvprobe-A-01` /
  `evt-exec02argvprobe-B-01`: rc 0; strict envelope
  `AUCDEV-023-RESOURCE-GATE-RESULT-V1`; status PASS; event/role/attempt
  echoed EXACTLY; EXACTLY three samples ALL PASS; workspace sample
  `sampled: attempt-workspace` executed (the gate CREATED exactly
  `{staging, custody-out, accounting}` for each probe UNDER THE ACTUAL
  LAUNCHER ROOT `/home/isa/aucdev023-s1-prep002-rem002/attempts/`);
  memory sample (`proc-meminfo`) executed; process-count sample
  (`proc-process-count`) executed; top-level PASS iff all three PASS;
- **ARGV-3 STRICT ARITY NEGATIVES** — malformed fd-exec argv counts
  (3 elements missing attempt; 5 elements extra trailing; 1 element;
  7 elements NETWORK_READINESS-shape) each REFUSED `exited 3` by the
  same corrected gate through the same path;
- **ARGV-4 VALIDATOR COMPATIBILITY** — the positive raw result bytes
  validated by `launch._validate_resource_gate_result` (the EXACT EBS
  RESOURCE_GATE result validator, envelope + sample semantics);
  a context-tampered result and a not-PASS result are each REFUSED
  (non-vacuous);
- **ARGV-5 NO RESERVED-ATTEMPT EFFECT** — before/after: A-01
  accounting bytes unchanged and equal to the pinned baseline
  (`PREPARED` → `TERMINAL_PREEXEC_STOP`), A-01 staging/custody
  unchanged (empty), B-01 remains EMPTY (not started), no real
  AccountingStore created, only the two synthetic probe dirs appeared,
  no other attempt directory touched; no credential fd exists on the
  gate path (`_gate_child` closes everything except 0/1/2/gate-fd; env
  is PATH/LANG only); the only child ever forked is the gate itself
  (local sampling only — no provider/model process by construction);
- **ARGV-6 CLEANUP** — both synthetic probe directories COMPLETELY
  removed; the launcher-root attempts listing byte-restored to the
  pre-probe baseline; A-01/B-01 final state re-pinned clean.

This exact-fd-exec regression is retained as MANDATORY evidence for
this and every later RESOURCE_GATE successor generation (the EXEC02-002
limitation — the historical rehearsal's five-sys.argv-element direct
invocation shape — is thereby remediated in successor testing practice;
the historical rehearsal itself is RETAINED valid for what it actually
tested and NOT rewritten).

## 4. Workspace contract, negative controls, parity (SUBMITTED_EVIDENCE)

- `evidence/workspace-contract-verification.json` — the EXEC-001
  corrected-ROOT invariant PRESERVED in the successor:
  `RESOURCE_GATE_ROOT == LAUNCHER_ROOT ==
  /home/isa/aucdev023-s1-prep002-rem002`, classification EXACT_MATCH
  both roles, binding descriptors match actual gate/launcher bytes,
  launcher byte-identical to the frozen identity, intended future
  operator paths recorded per role.
- `evidence/exec02-negative-controls.json` — ALL PASS: **N1** one
  planted gate-byte mutation REFUSED by the accepted EBS
  `verify_event_package` under the unchanged new binding (byte-exact
  restore re-verifies clean; file re-frozen read-only); **N2**
  descriptor substitution refused BOTH directions (accepted-generation
  binding vs NEW package → refusal; NEW binding vs accepted-generation
  package → refusal); **N3** the deterministic workspace-contract
  classifier fails each one-root-changed synthetic contract
  (non-vacuous); **N4** NETWORK_READINESS byte identity held
  (new == accepted == `20f37e91…` both roles); **N5** launcher byte
  identity held (`2efb6660…` both roles, == accepted); **N6** binding
  attempt derivation equals `ebs.binding.attempt_id_for` (see §6);
  **N7** the regenerated in-package identity evidence carries the NEW
  gate digest in both roles.
- `evidence/generation-diff-vs-accepted.json` — A=B shared-component
  parity byte-equal (launcher, wrapper + source, sentinel, probe-true +
  source, zsh, boundary-bwrap, resource-gate, network-readiness,
  output-validator); execution-visible `payload/evidence/**` 169 files
  per role, same path set, 169/169 byte-identical.
- `evidence/new-generation-verification.json` — one comprehensive
  verification: strict V5 `parse_binding` both roles (canonical digests
  above), `verify_event_package` both roles, every manifest row
  byte-verified (A 189/189, B 192/192), non-circular package identity
  recomputed EXACT, binding `event_package` pins equal the actual
  package bytes, EBS package pins unchanged (`68490d79…`/`8685c36e…`
  both roles), common-evidence manifest + prompt contract
  byte-identical to the accepted generation.

## 5. Deterministic regressions and held invariants (OBSERVED_FACT)

- Identity linter ALL PASS both roles (11 checks each) against the new
  packages with regenerated facts (`evidence/linter/`).
- Validation sweep ALL PASS (`evidence/validation-sweep.json`): hygiene
  census clean both packages (regular-file set == manifest set; no
  symlink/hardlink/special); secret-shape scan ZERO hits over workspace
  evidence/components/bindings/package payload; protected trees
  re-verified EXACT at the exact base; the unchanged frozen
  output-validator executed offline against an unmistakably synthetic
  probe (fail-closed rc 3 on the deliberately minimal probe — the
  artifact executes; no real report involved).
- Held invariants (`evidence/held-invariants.json`): PREP-001
  exact-PASS freeze discipline re-exercised at freeze; PREP-002/REM-002
  boundary/wrapper/executable rows byte-identical; PREP-003
  evidence-payload binding re-exercised (EBS per-row verification at
  freeze + N1 mutation refusal); REM-001 complete-package byte
  discipline re-exercised; EXEC-001 corrected ROOT invariant EXACT_MATCH
  (§4); GATE-W′/blindness/isolation evidence byte-identical carried
  forward; historical backup `event.backup.pre-exec02` all 381 rows
  verified unchanged.
- Deterministic batteries ACTUALLY RE-EXECUTED in an isolated detached
  worktree at the EXACT base `5d8c233…` (then removed):
  `compileall` exit 0 (one pre-existing historical SyntaxWarning in
  qh/statemachine.py, non-fatal); **EBS battery 489/489 PASS (37.2 s);
  qh battery 221/221 PASS (27.5 s)** — EXACT match to the prior
  accepted counts, no count change to investigate; host CPython 3.14.7
  + pytest 9.1.1 (the same isolated venv reused as the accepted battery
  environment — zero network activity under this authority).
  REGRESSION verification only — protected source bytes are UNCHANGED
  in this remediation (NOT a changed EBS/qh candidate);
  TEST_ENVIRONMENT_DIVERGENCE retained.
- Historical immutability BEFORE and AFTER all work:
  `evidence/baseline-verification.json` /
  `evidence/accepted-workspace-immutability-after.json` — every
  operator-expected accepted-generation identity EXACT at BOTH
  locations, all 381 rows byte-verified both times, historical attempt
  state pinned and unchanged.

## 6. Successor attempt/binding plan — returned to Control Room (OBSERVED_FACT + SUBMITTED_EVIDENCE)

`evidence/launch-plan-auditor-a.json` / `-b.json` (DATA ONLY; launches
nothing; confers NO authority) record the future exact operator values
per role with identities mechanically verified, the deployment
precondition (the byte-identical launcher resolves its package tree
from its own frozen ROOT, so the NEW generation must be deployed AT
`/home/isa/aucdev023-s1-prep002-rem002/event/` under a FUTURE new
operator execution authority, with the historical EXEC-02 deployed
generation preserved by dated backup and the deployed bytes reverified
to EXACTLY the new identities BEFORE any AccountingStore creation,
credential read, dynamic gate, GATES_PASSED, CONSUMED_PRE_EXEC or
provider/model execution), and:

- **B-01 PRESERVED — SAFE AND UNAMBIGUOUS**: the successor B binding
  parses with exactly `evt-7df609ec6c569043-B-01` (the frozen
  derivation), the historical B-01 attempt is NOT STARTED (pristine
  tree), and nothing about the argv remediation conflicts with it. The
  §7 STOP clause for B-01 is NOT triggered.
- **A-02 MECHANICAL FACT (returned, not decided)**: the operator
  directs the future replacement Auditor-A attempt id
  `evt-7df609ec6c569043-A-02`. The ACCEPTED FROZEN EBS derives attempt
  ids ONLY as `{event}-{role}-01` (`ebs.binding.attempt_id_for`;
  `parse_binding` REFUSES any other attempt for this event with
  `ATTEMPT_EVENT_RELATIONSHIP_INVALID`) — mechanically PROVEN during
  this session by parsing a constructed A-02 binding under the frozen
  EBS (refusal recorded verbatim in both launch plans). No binding
  document carrying A-02 can be accepted by the protected frozen EBS,
  and this remediation is FORBIDDEN from changing bootstrap-supervisor
  source. Expressing an A-02 attempt therefore requires either a NEW
  event id (which mechanically derives a fresh `-A-01`; minting is NOT
  authorized here) or a separate explicit EBS-source remediation
  authority. The successor A binding mechanically carries
  `evt-7df609ec6c569043-A-01` — the TERMINAL_PREEXEC_STOP /
  MUST-NOT-BE-REUSED historical identity — so a future Auditor-A
  launch decision MUST resolve the attempt identity explicitly under
  its own authority. This session neither mints an event/attempt nor
  decides the resolution.

## 7. Repository changes (this publication)

Changed paths EXACTLY: NEW this record
(`AUCDEV-023-S1-EXEC02-ARGV-REMEDIATION-REPORT.md`) +
`AUCDEV-CURRENT-STATE.md` (header + current-facing fields + dated
record + next-operator-action rotation) + `AUCDEV-BACKLOG.md` (dated
record) + ONE small bounded factual continuation in
`AUCDEV-ARCHITECTURE-SUMMARY.md` (the successor generation's
runtime-gate invocation-contract fact; no architecture redesign;
adopted R1 architecture/policy semantics unaltered; append-only prior
records untouched). NO bootstrap-supervisor, qualification-harness,
skill, runbook, protocol, qualification-history, prior-record or
frozen-target byte is modified (preferred repository source changes:
NONE outside canonical documentation — satisfied). All
event-package/workspace evidence stays OUTSIDE Git. Pre-existing
working-tree material (smoke-fixture gitlink drift, untracked evidence
directories) preserved unstaged.

## 8. Disclosed bounded builder adaptations + transcription note (DISCLOSED)

The new generation was built in the new workspace by the SAME accepted
builder code with exactly these disclosed adaptations (adapted scripts
in the handoff): (1) workspace root constants point at the new
workspace, and `components/runtime/resource-gate.py` is the corrected
argv-contract gate (all other inputs byte-identical copies of the
accepted generation); (2) the EXEC-001 reserved-workspace-empty
assertion was REPLACED by a read-only assertion against the pinned
historical attempt state (A-01 = EXACTLY its terminal accounting record
with empty staging/custody; B-01 entirely empty) — the builder never
creates or mutates anything under the launcher root; (3) the identity
linter's workspace constant points at the new workspace (its only
workspace-bound references are the package tree, the components
directory and a composition-string staging path); (4) the batteries
reused the accepted isolated pytest venv (CPython 3.14.7 + pytest 9.1.1)
to keep this session zero-network.

TRANSCRIPTION NOTE (INFORMATIONAL; no canonical defect): the remediation
authority's §5 Auditor-B executable constant as received renders as
…bddc60226**23**d7ddf… (one hex digit); the mechanically authoritative
accepted-generation identity — equal to the binding pin AND the manifest
row AND the Control-Room-verified bytes (EXEC-001 readback, A 189/189 +
B 192/192 byte-verified) — is …bddc60226**e3**d7ddf…
(`3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022`).
Byte-identity of BOTH auditor executables to the accepted generation
was enforced against the authoritative anchors; every other §10
identity constant verified EXACT.

RUN-ORDER NOTE: each deterministic battery was executed exactly ONCE in
a FRESH worktree at the exact base with output captured on first
execution (a battery re-executed in an already-run tree fails its own
shipped-bytes manifest tests from first-run artifacts — a test-tree
hygiene property, not a source defect; the recorded result is the clean
first-execution run).

## 9. Zero-execution attestation (OBSERVED_FACT)

Provider/model/frontier inference: ZERO. Real credential bytes
read/hashed/logged: ZERO (the gate env is PATH/LANG only; no credential
fd exists on the gate path). Auditor-A/B / `/audit-council` executions:
ZERO. `Supervisor.run_attempt`: ZERO calls. AccountingStore creation:
ZERO. GATES_PASSED / CONSUMED_PRE_EXEC / EXEC_ATTEMPTED: ZERO. Real
attempt ids sampled by any gate execution: ZERO (synthetic
`evt-exec02argvprobe-*` and `evt-0000offlineprobe` namespaces only).
Historical workspace/deployed-tree/backup mutations: ZERO (verified
before/after; the only writes under the launcher root were the two
synthetic probe attempt directories, created BY the corrected gate
during ARGV-2 and completely removed by ARGV-6). Protected tree
mutations: ZERO (verified at bootstrap, at every battery run, in the
validation sweep and immediately before staging). Network activity:
ZERO. Qualification/installation: NONE. The historical execution
authority was NOT exercised and does NOT transfer to this generation.

## 10. Disposition (REQUIREMENT — evidence-derived, implementer strength ONLY)

```
AUCDEV_023_S1_EXEC02_ARGV_REMEDIATION =
IMPLEMENTED / NEW_SUCCESSOR_PACKAGES_FROZEN / EXACT_EBS_FD_EXEC_REGRESSION_PASS /
EXEC02_001_REMEDIATED_IN_SUCCESSOR / EXEC02_002_TEST_GAP_REMEDIATED_IN_SUCCESSOR /
AWAITING_CONTROL_ROOM_READBACK / REAL_EXECUTION_NOT_AUTHORIZED

AUCDEV023-CR-S1-EXEC02-001 = REMEDIATION_IMPLEMENTED_IN_SUCCESSOR / AWAITING_CONTROL_ROOM_READBACK
AUCDEV023-CR-S1-EXEC02-002 = TEST_GAP_REMEDIATED_IN_SUCCESSOR / AWAITING_CONTROL_ROOM_READBACK
  (implementer dispositions ONLY — NOT CLOSED; only the Control Room may accept)

EVENT evt-7df609ec6c569043 = PRESERVED (no replacement event/attempt minted)
A-01 = TERMINAL_PREEXEC_STOP / UNCONSUMED / MUST NOT BE REUSED (byte-unchanged)
B-01 = NOT STARTED (preserved; safe and unambiguous)
A-02 = OPERATOR-DIRECTED FUTURE IDENTITY; NOT EXPRESSIBLE in a binding accepted
  by the frozen EBS (ATTEMPT_EVENT_RELATIONSHIP_INVALID, mechanically proven);
  requires NEW event id or separate EBS remediation — RETURNED to Control Room
MODEL_ENGAGEMENTS_USED_UNDER_THIS_AUDIT_POLICY = 0
AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02 = NO FURTHER EXECUTION / NON-TRANSFERABLE
REAL_PROVIDER_CALL/AUDITOR_A/AUDITOR_B/MODEL_ENGAGEMENT/QUALIFICATION/
INSTALLATION AUTHORITY = NONE
qualification = NONE
installation = NONE
AUCDEV-023 = P1 / READY / NOT DONE (counts unchanged: READY 9 / OPEN 7 /
BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11 — no backlog-row transition)
```

## 11. Next action — EXACTLY ONE

```
INDEPENDENT CONTROL ROOM READBACK OF THE EXEC02-001/002 ARGV REMEDIATION,
EXACT EBS FD-EXEC REGRESSION EVIDENCE, AND COMPLETE NEW SUCCESSOR-PACKAGE
BYTE HANDOFF
```

No auditor launch, no real credential use, no model execution and no
qualification/install activity follows automatically from this
publication. A future real attempt requires a NEW explicit operator
execution authority for the NEW exact package generation (deployed at
the launcher-resolved event location and reverified first), with the
Auditor-A attempt identity question of §6 resolved by that authority.

## 12. Generated-LAST handoff archive (OBSERVED_FACT)

After ALL remediation work, tests, the final commit, push and the
independent GitHub readback are complete, exactly ONE non-secret
`.tar.gz` COMPLETE handoff archive is generated LAST containing the
COMPLETE actual bytes of BOTH new successor packages, both new
bindings, the corrected and historical RESOURCE_GATE actual bytes, the
unchanged launcher bytes, NETWORK_READINESS hash proof, the exact
old→new gate diff, the package-generation diff, all identity/linter
evidence, the ARGV-1…ARGV-6 exact fd-exec regression evidence, probe
cleanup and immutability evidence, the battery outputs, the canonical
publication files, the exact Git diff + commit metadata + GitHub
readback, protected-tree verification, the finding/disposition
inventory, the future launch-plan DATA (incl. the A-02 disclosure), and
exactly one SHA256SUMS covering every payload regular file except
itself. NO credentials, NO private logs, NO auditor substantive report
content. Its path/SHA-256/size/census are recorded in this session's
final return. Nothing is mutated after archive generation.
