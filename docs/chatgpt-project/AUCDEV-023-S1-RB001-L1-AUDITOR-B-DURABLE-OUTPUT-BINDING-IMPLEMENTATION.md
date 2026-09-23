# AUCDEV-023 S1 RB-001 L1 — Auditor-B Durable Output Binding (EXEC-RB-002) — Bounded Zero-Provider Implementation Record

- **Authority**: `AUCDEV-023-S1-RB001-L1-EXEC-RB002-IMPLEMENTATION-20260924-01`
- **Implementer role**: bounded zero-provider IMPLEMENTER ONLY — NOT the
  Control Room decision-maker, NOT Auditor-A/B, NOT the operator, NOT an
  execution controller, NOT a qualification/installation authority.
- **Decision authority implemented**:
  `AUCDEV-023-S1-RB001-L1-B-DURABLE-OUTPUT-BINDING-DECISION-20260924-01`
  (canonical record blob `17569d6e…` at base), closing ONLY the
  demonstrated invariant of finding
  `AUCDEV023-CR-S1-RB001-L1-EXEC-RB-002`
  AUDITOR_B_DURABLE_REPORT_PATH_NOT_MECHANICALLY_BOUND.
- **Date**: 2026-09-24 (Europe/Istanbul)
- **Workspace** (fresh, verified absent before creation):
  `/home/isa/aucdev023-s1-rb001-l1-exec-rb002-output-binding-implementation-20260924-01/`

## 1. Live bootstrap (all EXACT)

- Live GitHub default branch `master` resolved by `git ls-remote`:
  `3c596857ad92581cf5d2d676f25c9dfbcce56e14` == expected authorized
  baseline (no `LIVE_BASE_CHANGED`).
- Local HEAD / root tree / sole parent:
  `3c596857ad92581cf5d2d676f25c9dfbcce56e14` /
  `708384ffe4e2e6442606a609f248d08a13876f18` /
  `b5185497676babae855a5cd46a01031198424813` — all EXACT.
- Canonical blobs at base: CURRENT `2e7761566baae04aa159cbe9fd795a84d37b7ac0`,
  BACKLOG `bdb25c74635295a2bc645726187dcbbf687b18ec`, decision record
  `17569d6ece9e09489b5259938a71501dabc519cd` — all EXACT.
- Protected trees: `bootstrap-supervisor 732b8def…`,
  `qualification-harness 5b8d5e54…`, `skill c792933a…` — EXACT;
  protected source blobs `bootstrap-supervisor/ebs/binding.py 47eeb517…`
  and `bootstrap-supervisor/ebs/launch.py 063b6ce1…` — EXACT.
- Pre-existing working-tree drift recorded separately
  (`evidence/preexisting-drift.txt`: 47 untracked-only entries — evidence
  dirs, drivers, wrappers; tracked diff vs HEAD EMPTY).

## 2. Control Room decision handoff (verified read-only)

`/home/isa/audit-council-dev/AUCDEV-023-S1-RB001-L1-B-DURABLE-OUTPUT-BINDING-DECISION-HANDOFF.tar.gz`
— outer SHA-256 `fc7194d27501a1b7c654e8db3b87426e3ff05d5726c8777df5d47328f2dee896`,
710695 B; census 19 regular / 0 unsafe / 0 duplicates / 0 symlinks /
0 hardlinks / 0 special; one SHA256SUMS, 18 rows 18/18 PASS, zero
missing, zero unlisted; verified fully in-memory, ZERO extraction, ZERO
execution. (One initial 0-PASS report from this session's own first
parser was a session-side path-normalization bug — SHA256SUMS rows are
relative to the archive's top-level directory — corrected; no artifact
discrepancy.) No handoff member executed.

## 3. Accepted preparation-source discovery (§8)

See `evidence/source-surface-discovery.md` (workspace). Summary:

- The role-B `auditor_invocation` generation surface is EXACTLY ONE
  isolated preparation-source file (NOT tracked repository source):
  `…successor-package-prep-20260923-01/components/build/build_packages.py`
  (baseline SHA-256 `5ae3a11129002a8715bac853a72bf1a322d50dba715b5530d799386735735e2c`,
  46193 B): `EVENT_ID` literal, `ROLES[...]["invocation"]` static argv
  literals, `identity_facts()`, `build_binding_and_manifest()`
  (binding doc + V5 transport projection + MANIFEST).
- Read-only canonical dependencies (UNCHANGED):
  `ebs/binding.py` `39bd966a94825f2e01d4613bf6a7e8be4070e8712266a4d58d99051632574184`
  (`attempt_id_for`/`output_name_for`; invocation bounds 32 items /
  1024 B per item / 8192 B total / no control chars; `Binding.digest`
  over the full doc incl. `auditor_invocation`; projection fields),
  `ebs/launch.py` `dfc63f0033aad802e5355e9dad652499d27a602122c7cfa1e2fa4d252947e9b7`
  (`verify_event_package`), and the frozen argv CONSUMER
  `components/boundary/networked-boundary-launcher.py`
  `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa` /
  41270 B — reads the invocation bounded at 8192 B and `execv`s it
  VERBATIM with NO argv-content validation (so the remediated argv needs
  NO boundary/EBS change).
- Historical dataflow: `EVENT_ID` → attempt → `output_identity.name`;
  the invocation literal was INDEPENDENT of that derivation and carried
  the report pathname only in natural-language prompt text (argc 6) —
  the EXEC-RB-002 defect.
- §8 STOP conditions NOT triggered
  (`PREPARATION_SOURCE_SURFACE_NOT_ESTABLISHED` — surface established;
  `TRACKED_IMPLEMENTATION_SURFACE_DISCOVERED_SCOPE_CHANGE` — surface is
  NOT tracked source). Baseline copies + hashes:
  `evidence/baseline-hashes.json` (8 files).

## 4. The candidate remediation (§9, §10)

- Candidate: `candidate/components/build/build_packages.py`
  SHA-256 `7cb0ba0a8ef1cbc3ce5ad8bd5e502b4d3b3ead9d2ea07e8bc513726be3c17141`.
- Minimal unified diff `diff/build_packages.py.diff`: +109/−25 lines in
  ONE file, containing ONLY:
  1. provenance docstring note (RB-002);
  2. `WS`/`EVENT_ID` SYNTHETIC TEST FIXTURE defaults
     (`evt-c0dec0dec0decafe`; future authorized preparation task MUST set
     its own fresh workspace + fresh real event id + its own
     identity_derivation prose first);
  3. canonical derivation helpers `attempt_id_for` / `output_name_for`
     (== `ebs.binding` functions; equality-tested T0) + `auditor_prompt`;
  4. AUDITOR_A invocation DERIVED (semantics UNCHANGED — byte-identical
     argv for any given event id, proven H1 without normalization);
  5. AUDITOR_B invocation gains EXACTLY the two ordered elements
     `--output-last-message`, `/auditor-output/<output_name>` immediately
     before the final positional prompt;
  6. the three derivation call sites unified on the helpers;
  7. NEW fail-closed freeze gate `_require_bound_b_output(doc)` —
     refuses ANY AUDITOR_B binding whose argv does not carry
     `--output-last-message` exactly once followed by EXACTLY
     `"/auditor-output/" + doc["output_identity"]["name"]`, or that
     carries `--output-schema`.
- Exact role-B invocation, BEFORE (historical, argc 6):
  `codex exec --skip-git-repo-check --profile aucdev023-c3 <prompt>`
  (pathname only inside `<prompt>`).
- Exact role-B invocation, AFTER (candidate, argc 8 — synthetic fixture
  identity shown; real future event derives identically):
  `codex exec --skip-git-repo-check --profile aucdev023-c3 --output-last-message /auditor-output/evt-c0dec0dec0decafe-B-01.first-pass-report.json <neutral first-pass instruction>`
  — prompt REMAINS the final positional element (proven valid by the
  frozen client itself executing this ordering successfully in the §15
  rehearsal; NOT inferred from general Codex knowledge).
- Ordering note (client grammar): the frozen client's embedded usage
  string `codex exec [OPTIONS] [PROMPT]` (static evidence held in the
  decision record) plus the successful rc=0 execution of the exact
  ordered argv in the rehearsal establish the exact valid ordering
  mechanically.
- Auditor-A: invocation, executable, sandbox profile, provider role,
  output mechanism, boundary behavior ALL UNCHANGED (H1/H2; the launcher
  and EBS sources byte-pinned; role-A bindings untouched by the
  fail-closed gate).

## 5. Deterministic acceptance tests (§13 A–N, §14) — 38/38 PASS

Runner `tests/run_acceptance.py`
(SHA-256 `0523b8f94b4bf9439105f42cad291586ed733f427a628cb8ba9dbdb6e6ae01f9`);
full per-check record `evidence/acceptance-tests.json`. All identities
synthetic (`evt-c0dec0dec0decafe`, `evt-feedfacefeedface`).

- A `--output-last-message` exactly once (count=1); B following item ==
  `/auditor-output/` + output_identity.name; B2 prompt final positional.
- C distinct synthetic identities → distinct derived paths, no stale
  literals; D historical B pathname absent from candidate source;
  E/E2/E3/E4 historical ids absent from identity-generating logic and
  from module constants except the three frozen historical-state PIN
  constants (§6-sanctioned explicit historical comparisons) and the
  docstring; default EVENT_ID synthetic.
- F1/F2 `--output-schema` absent from every generated invocation and
  present in source ONLY inside the fail-closed refusal function.
- G1–G4 stdout behavior unchanged (no changed line touches any
  stdout/DEVNULL/subprocess-auditor surface; every non-target function
  AST-identical — changed set exactly {identity_facts,
  build_binding_and_manifest} + the four new helpers; boundary launcher
  bytes 011a8713…; EBS launch.py unchanged).
- H1/H2 role-A argv byte-identical (incl. normalization-free historical
  reproduction); I1/I2 role-B differs by EXACTLY the two ordered
  elements.
- J1/J2/J2b within EBS `auditor_invocation` bounds (8 items, 550 B
  total ≤ 32/8192) and the remediated binding parses through the EXACT
  `parse_binding` (baseline-shape binding still parses too).
- §14 (K14a–K14g): baseline vs remediated B bindings built through the
  SAME builder logic at the same synthetic fixture inputs differ ONLY in
  `auditor_invocation` (+ the `event_package` identity pair that covers
  it in the frozen manifest); digests differ
  (`b496d686885d…` vs `3dc08e5ce06e…`); invocation included in
  `Binding.digest` (mutation-sensitive), `binding_projection`, and the
  event-package MANIFEST `transport_binding`; the EXACT existing
  `verify_event_package` PASSES on the remediated synthetic fixture
  package (TEST_FIXTURE_ONLY / NOT_A_REAL_EVENT, isolated workspace).
- K option-name / output-path / ordering mutations each change the
  binding digest; L removing the option →
  `EXEC_RB_002_OUTPUT_LAST_MESSAGE_NOT_EXACTLY_ONCE`; M non-canonical
  destination → `EXEC_RB_002_DURABLE_OUTPUT_PATH_NOT_MECHANICALLY_BOUND`;
  M2 `--output-schema` → `EXEC_RB_002_OUTPUT_SCHEMA_FORBIDDEN…`
  (all three fail-closed refusals observed).
- N1/N2 accepted workspace byte-unchanged; no real-tree changes (see
  §8 below).

## 6. Zero-provider GATE-W-prime rehearsal (§15) — ALL ITEMS PROVEN

Runner `tests/rehearsal_rb002.py`
(SHA-256 `55a69c9cc6c5d8ca33522363355c593c7c29d727b425a27527da3e43251966bf`);
evidence `evidence/gate-w-prime-rb002/{rehearsal-evidence.json,SUMMARY.md}`.

Mode: the REAL frozen pinned codex 0.154.0 client
(`3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022` /
262858016 B, re-verified) inside the REAL accepted boundary composition
(vendored bwrap engine, frozen C-3 profile layer bytes, tool-domain
wrapper, `/auditor-output` the one host-backed rw bind), executed from
the ISOLATED byte-verified copy of the accepted package
(`fixture-generation/`, 195/195 files byte+size+mode identical);
`net=False` (--unshare-net, loopback only); deterministic scripted mock
provider (accepted components reused read-only) the ONLY reachable
endpoint; synthetic credential bytes only; synthetic fixture identity
`evt-feedfacefeedface`.

1. Frozen client STARTED and exited rc=0 with the EXACT remediated
   argc-8 argv (ordering proven by execution).
2. argv carried `--output-last-message` exactly once + exact canonical
   path (proof record echoes the memfd invocation).
3. The mock final-agent message was DURABLY WRITTEN BY THE CLIENT to the
   exact synthetic canonical path
   `/auditor-output/evt-feedfacefeedface-B-01.first-pass-report.json` —
   content BYTE-IDENTICAL to the scripted final message (sha256
   `d4f7ff6c6db78ec7b5c67349ae71f8fbbba267744257563f13d5da1f84fa85bc`,
   822 B).
4. NO secondary output file: staging at client exit contained EXACTLY
   ONE file (the bound report).
5. The EXISTING frozen structural validator
   (AUCDEV023-FIRST-PASS-REPORT-VALIDATOR-V1, package bytes executed
   as-is under its exact EBS fd-3 sealed-snapshot argv contract)
   ACCEPTED the delivered file: status PASS, exit 0.
6. stdout NON-AUTHORITATIONAL and discarded: delivery is by the client's
   own file write; the boundary launcher (stdout-discarding) bytes are
   unchanged; nothing in the composition persists stdout.
7. Outside-write negative control REFUSED ("Read-only file system").
8. No-profile control (EXACT accepted control shape) REFUSED
   ("Read-only file system"), NO report file created.
9. ZERO real provider/model inference: mock log = exactly 2 requests,
   both `http://127.0.0.1:<port>/v1/*`; no external route exists inside
   the namespace; zero real credential.
The fallback token
`ZERO_PROVIDER_NATIVE_OUTPUT_LAST_MESSAGE_REHEARSAL_NOT_MECHANICALLY_AVAILABLE`
was NOT needed.

## 7. Held findings and explicit non-goals

- EXEC-RB-001: OPEN / COMPLETENESS LIMITATION / FAILURE-DIAGNOSTIC
  EVIDENCE GAP / ROOT_CAUSE_UNRESOLVED — held EXACTLY; nothing here
  claims historical causality.
- EXEC-RB-002: implemented at CANDIDATE strength ONLY (see §9); NOT
  CLOSED — Control Room acceptance is separate.
- Non-goals held (§11): no `--output-schema` (actively forbidden), no
  stdout capture/persistence or DEVNULL change, no report-schema /
  validator / freezer / screen change, no credential / network / sandbox
  / tool-wrapper / boundary-launcher / EBS-binding-schema / EBS-launch /
  target-source change, no `qualification-harness/**` or `skill/**`
  change, no real replacement event/attempts, no deployment, no reading
  of historical Auditor-A substance, no replacement execution authority
  (`evidence/attestations.md`).

## 8. Historical immutability + no-real-event verification

`evidence/historical-immutability.json`:
- Accepted prep workspace: `build_packages.py` byte-unchanged; the
  accepted package-auditor-b source tree re-verified 195/195 files
  byte+size+mode identical post-implementation (against the staged
  byte-verified copy).
- Deployed root pins re-verified EXACT: bindings `ef0428c4…` /
  `4a97ced6…`, MANIFESTs `b9572520…` /
  `7fe23950081b52cf9e4b109f667f3bbbc2cd1b71a0d7be507d3684012ec4e081`,
  boundary launcher `011a8713…` byte-identical in BOTH packages, frozen
  codex `3188814c…`; attempts namespace 22 entries with ZERO synthetic
  fixture entries; all four event backups present; the four historical
  backups and the pre-replacement generation untouched.
- Historical Auditor-A frozen report verified by mechanical identity
  ONLY (`058a611f…` / 26314 / 0444, intact) — substance NEVER opened.
- Historical authority `AUCDEV-023-S1-RB001-L1-FIRSTPASS-EXEC-20260923-01`
  remains CONSUMED / TERMINAL / CLOSED / NO_RERUN; historical event /
  attempts NOT reused as active identities (only in negative
  stale-literal tests / historical comparisons).
- **Publication typo observation (disclosure, no historical mutation)**:
  2 of 11 published occurrences of the deployed B MANIFEST digest at
  base `3c596857` carry a 2-character transposition
  (`…0d3644012…` instead of `…0d3684012…`) — in
  `AUCDEV-023-S1-RB001-L1-FIRSTPASS-EXECUTION-AUTHORITY-GRANT-PRELAUNCH.md`
  and
  `AUCDEV-023-S1-RB001-L1-FIRSTPASS-GRANT-PRELAUNCH-CONTROL-ROOM-READBACK.md`;
  the LIVE artifact bytes are UNCHANGED (deployed root, accepted
  workspace, the frozen execution-handoff member `3710d813…` and this
  session's byte-verified copy ALL hash to the SAME correct value).
  Historical records preserved unrewritten; this session's own first
  expected literal inherited the typo and was corrected session-side
  with NO artifact discrepancy.
- Synthetic fixture identity inventory + collision/absence proofs:
  `evidence/synthetic-fixture-identities.json` (SYNTHETIC TEST FIXTURE
  IDENTITY ONLY values absent from deployed and accepted trees).

## 9. Resulting disposition (IMPLEMENTATION strength ONLY)

EXEC_RB_002_IMPLEMENTATION =
CANDIDATE_REMEDIATION_IMPLEMENTED
/ AUDITOR_B_DURABLE_OUTPUT_PATH_MECHANICALLY_BOUND
/ OUTPUT_LAST_MESSAGE_EXACTLY_ONCE
/ OUTPUT_PATH_DERIVED_FROM_BOUND_OUTPUT_IDENTITY
/ ROLE_A_UNCHANGED
/ STDOUT_BEHAVIOR_UNCHANGED
/ BINDING_DIGEST_COVERAGE_PROVEN
/ NO_OUTPUT_SCHEMA
/ NO_BOUNDARY_CHANGE
/ NO_EBS_SOURCE_CHANGE
/ NO_REAL_EVENT_PREPARED
/ NO_REPLACEMENT_AUTHORITY
/ ZERO_REAL_PROVIDER_MODEL_INFERENCE
/ REQUIRES_CONTROL_ROOM_READBACK

NOT CLOSED — Control Room acceptance is separate. EXEC-RB-001 remains
ROOT_CAUSE_UNRESOLVED.

Resulting state: real event created NO; real attempts NO; production
package prepared NO; deployment NONE; real credential read NONE; real
provider/model inference NONE; replacement execution authority NONE;
qualification NONE; installation NONE; model engagements 0 (zero-provider
task); historical authority CONSUMED/TERMINAL/CLOSED/NO_RERUN; audit
completeness INCOMPLETE; qualification readiness
BLOCKED_BY_MISSING_MANDATORY_AUDITOR_B_FIRST_PASS; AUCDEV-023 remains
P1 / READY / NOT DONE with NO queue-count transition (READY 9 / OPEN 7 /
BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11).

## 10. Limitations (stated plainly)

- Candidate strength only: the candidate builder ships SYNTHETIC TEST
  FIXTURE defaults; the future separately authorized preparation task
  MUST set its own fresh workspace root, fresh real event id, and its
  own identity_derivation/provenance prose (the historical provenance
  prose inside the builder remains as inherited evidence text).
- The rehearsal proves mechanical delivery binding of the exact frozen
  client/composition at a synthetic identity with a scripted provider —
  NOT real-auditor behavior and NOT the EXEC-RB-001 root cause.
- The EBS `run_attempt` custody lifecycle (real pipeline) was NOT
  executed; observability was demonstrated at rehearsal strength
  (validator acceptance at the exact canonical staging location,
  single-file staging).
- Live npm/codex drift remains an external environment condition
  (`AUCDEV023-S1-RB001-L1-PREP-ENV-001`); the frozen runtime closure
  bytes were used exclusively (re-verified).

## 11. NEXT ACTION EXACTLY ONE

CONTROL ROOM VERIFICATION OF THE EXEC-RB-002 CANDIDATE REMEDIATION AND
ZERO-PROVIDER EVIDENCE BEFORE ANY FRESH REAL EVENT SELECTION, PACKAGE
GENERATION, LAUNCHER ADAPTATION, OR REPLACEMENT EXECUTION AUTHORITY.
