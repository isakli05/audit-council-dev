# Audit Council Dev — Engineering Backlog

Last reviewed: 2026-09-08 against source
`8ae33444f349ce73c1359b963722e2d16acba630`, tracked history, installed bytes,
and the operator's production observations. This is the canonical development
queue. No feature implementation is authorized by creation of this backlog.

OPEN = needs refinement; READY = bounded and ready for assignment;
IN_PROGRESS = authorized work underway; BLOCKED = named dependency unavailable;
DEFERRED = future only; DONE = evidenced closure; ACCEPTED_RESIDUAL = documented
boundary, not a claim that a defect was fixed. Priority is impact/urgency, not
implementation order. Recommended versions are planning suggestions, not releases.

Counts: **19 open** (OPEN/READY/BLOCKED; none IN_PROGRESS), **P0 2 / P1 6 / P2 11**;
**3 DEFERRED**, **8 ACCEPTED_RESIDUAL**, **4 DONE**. Open statuses: READY 9,
OPEN 8, BLOCKED 2. No speculative issue is promoted to P0.

Focused priority review, 2026-09-05, repository checkpoint
`910339b661d2a18e4690a5bac95ee048e08cbae3`: only AUCDEV-001/009/010 reconsidered.
P0 here prioritizes evidenced defects in the core independent-review/completeness
guarantees before relying on those guarantees for a candidate release. It does not
declare every past verdict contaminated or assign CRITICAL severity to every finding.
No runtime work starts with this prioritization. AUCDEV-010 is READY evidence
reconciliation: the operator confirms historical evidence outside the initial
publication snapshot; a missing repository entry is not proof of absent qualification.

## Prioritized queue

| ID | Priority | Status | Title | Suggested milestone |
|---|---|---|---|---|
| AUCDEV-001 | P0 | READY | Mechanical blind-independence isolation | v2.0.2 design, implementation after approval |
| AUCDEV-009 | P0 | READY | Reconcile executable protocol/schema instructions | v2.0.2 candidate |
| AUCDEV-010 | P1 | READY | Reconcile existing installed qualification provenance | Before next candidate audit |
| AUCDEV-018 | P1 | READY | Dirty-target byte-level freshness coverage | v2.0.2 candidate |
| AUCDEV-004 | P1 | READY | Completeness and visibility provenance hardening | v2.0.2 candidate |
| AUCDEV-002 | P1 | OPEN | Operator-authorized Evidence Ingress v2 | v2.0.2 or v2.1 after design |
| AUCDEV-005 | P1 | READY | Sanitized real-run regression corpus | v2.0.2 candidate |
| AUCDEV-003 | P1 | OPEN | Disposable mutation/falsification workspace | v2.1 design |
| AUCDEV-008 | P2 | READY | Human escalation and bounded retry semantics | v2.0.2 candidate |
| AUCDEV-007 | P2 | OPEN | Whole-program governor integration | v2.1 after measurements |
| AUCDEV-006 | P2 | OPEN | STANDARD / RELEASE / FORENSIC effort semantics | v2.1 design only initially |
| AUCDEV-011 | P2 | OPEN | Targeted re-audit compiler | After manual cycle evidence |
| AUCDEV-012 | P2 | READY | Public-contract and operator usability simplification | v2.0.2 docs/product review |
| AUCDEV-013 | P2 | READY | Resolve layout-default API divergence | v2.0.2 candidate |
| AUCDEV-014 | P2 | BLOCKED | Owner license decision | Repository governance |
| AUCDEV-015 | P2 | OPEN | Portable historical smoke-fixture provenance | Repository hygiene |
| AUCDEV-016 | P2 | BLOCKED | Budgeted real-model seeded evaluation | After qualification provenance |
| AUCDEV-017 | P2 | OPEN | EvidenceStore lifecycle integration | After isolation/ingress contracts |
| AUCDEV-019 | P2 | OPEN | Bounded file-resource cleanup | Next maintenance cycle |

## Work items

### AUCDEV-001 — Mechanical blind-independence isolation

- Priority/status: P0 / READY.
- Problem/evidence: `skill/scripts/codex_sandbox.py:build_sandbox_argv` binds the entire
  run directory; Opus's checkpoint already exists before Codex independence.
  `EvidenceStore._visible` is an API barrier, not raw filesystem isolation.
  The operator reports this exposure in a real v2.0.1 dual-model run; its run ID is unknown.
- Why it matters: procedural blindness cannot substantiate a mechanical independence claim.
  Priority raised from P1: the source-corroborated production exposure defeats a core
  trust boundary without requiring a new speculative attack. Actual cross-pollination
  or verdict impact still needs per-run evidence; this is not blanket historical invalidation.
- Scope: design and then implement model-specific views: `shared/`, `private/opus/`,
  `private/codex/`, `cross-exam/`; include artifacts, logs, prompts, evidence, and resume.
  Peer artifacts become accessible only after a recorded barrier transition.
- Non-goals: different audit models, a distributed service, auth-system redesign, automatic development.
- Dependencies: AUCDEV-010 for release audit; agree visibility contract with AUCDEV-004/002.
- Acceptance: direct peer reads and enumerations fail before barrier for both auditor
  contexts, including symlink/alternate-path access; own/shared evidence works;
  peer reads work after barrier; frozen target identity survives view construction.
  Document the exact remaining Claude-side enforcement limit.
- Validation: deterministic sentinel reads through actual production stage views,
  fresh/resume/repair tests, barrier failure tests, then independent candidate audit.
- References: `skill/protocols/independent-audit.md`, `skill/scripts/codex_sandbox.py`,
  `skill/scripts/evidence_store.py`, `skill/tests/test_codex_sandbox.py`,
  `skill/tests/test_evidence_store.py`, KNOWN-LIMITATIONS items 16 and 24.
- Milestone: v2.0.2 design; implement only the approved bounded design.

### AUCDEV-002 — Operator-authorized Evidence Ingress v2

- Priority/status: P1 / OPEN.
- Problem/evidence: `environment_manager._stage_evidence` requires source-contained
  files and rejects `audit-output` via EVIDENCE_DENYLIST even when allowlisted.
  External evidence and historical-output evidence remain awkward; operator confirms
  this in the later production run. Existing RELEASE staging is already fixed.
- Why it matters: operators need authorized evidence without granting arbitrary host reads.
- Scope: explicit authorization → realpath/symlink validation → sealed run-owned copy
  → source/result digests and provenance → audience/phase visibility policy.
- Non-goals: weaken deny-lists; ingest auth material; expose private findings during independence.
- Dependencies: visibility contract with AUCDEV-001/004; source-disclosure policy in SECURITY.md.
- Acceptance: only exact authorized files enter; original and resolved paths are checked;
  symlink escapes, path collisions, changed bytes, and unauthorized inputs fail closed;
  sealed copies retain hashes/authorization and model-specific visibility.
- Validation: deterministic external-file and historical-output fixtures, denied sensitive
  paths, symlink/race cases, copy integrity and identical authorized model views.
- References: `skill/scripts/environment_manager.py`, `skill/scripts/audit_council.py:cmd_prepare`,
  `skill/schemas/evidence-record.schema.json`, `skill/tests/test_environment_manager.py`,
  `skill/tests/test_tier4_da27c0.py`.
- Milestone: v2.0.2 or v2.1 after explicit design.

### AUCDEV-003 — Disposable mutation/falsification workspace

- Priority/status: P1 / OPEN.
- Problem/evidence: the source-write prohibition and ro-bind prevent mutation-sensitive
  experiments; current detached RELEASE targets remain authoritative immutable targets.
- Why it matters: a green guard test may be insensitive to a meaningful code mutation.
- Scope: bounded writable throwaway copy derived from the exact target; record parent
  SHA, original digest, mutations, commands, results, and cleanup/retention policy.
- Non-goals: edit frozen target/live repository; treat mutated output as authoritative;
  build a general code-execution platform or enable uncontrolled network/secrets.
- Dependencies: AUCDEV-001/002 for workspace/evidence isolation; explicit experiment budgets.
- Acceptance: frozen/live bytes and Git state stay unchanged; experiment workspace is
  unmistakably non-authoritative; outputs identify mutations and exact parent;
  outside writes/access remain confined and failure leaves target recoverable.
- Validation: deterministic kill/survive mutant examples, path-escape checks, digest
  comparisons before/after, failure cleanup and provenance tests.
- References: `skill/SKILL.md` hard rules, `skill/scripts/codex_sandbox.py`,
  `skill/scripts/environment_manager.py`, `skill/tests/test_source_write_guard.py`.
- Milestone: v2.1 design.

### AUCDEV-004 — Completeness and visibility provenance hardening

- Priority/status: P1 / READY.
- Problem/evidence: current final/state schemas express stages and skips but do not
  certify mechanical independence or effective evidence visibility. The failure
  protocol permits residual-complete wording after quota-deferred required work.
- Why it matters: a verdict can appear stronger than the audit actually performed.
- Scope: design explicit independence/visibility claims and stage evidence linkage;
  review finalize/skip/completeness compatibility and blocked environment reasons.
- Non-goals: redo v2.0.1 run-binding linkage; treat completeness as a product verdict;
  declare every accepted boundary a failed run without an agreed contract.
- Dependencies: AUCDEV-009 protocol reconciliation; AUCDEV-001 visibility semantics.
- Acceptance: missing mandatory work cannot report full completeness; every claim
  about isolation/visibility points to evidence or is marked unestablished;
  state/final/report/metrics agree; historical records remain readable without rewriting.
- Validation: table-driven omitted-stage, quota, inactive-sandbox, failed-barrier,
  resume and historical compatibility tests through real finalize/render paths.
- References: `skill/scripts/audit_council.py:cmd_finalize`, `skill/scripts/state_store.py`,
  `skill/schemas/state.schema.json`, `skill/schemas/final-findings.schema.json`,
  `skill/protocols/failure-and-resume.md`, `skill/tests/test_env_lifecycle.py`.
- Milestone: v2.0.2 candidate; version policy review if field meaning changes.

### AUCDEV-005 — Sanitized real-run regression corpus

- Priority/status: P1 / READY.
- Problem/evidence: da27c0 has 19 current deterministic regression methods (16 initial,
  three focused follow-ups). Fifth fixtures retain sizeable real public-product audit
  narratives. The later isolation/ingress observations lack a sanitized fixture/run reference.
- Why it matters: preserve causal lessons without turning private archives into public data.
- Scope: compact reproductions for sandbox/toolchain/DNS failure, no-inference attempt
  accounting, isolation exposure, ingress denial, and historical malformed output.
  Record source observation → sanitized fixture → regression mapping.
- Non-goals: rerun historical audits, copy private logs, rewrite historical Git evidence,
  count fake-model scoring as model quality.
- Dependencies: AUCDEV-001/002 supply behavior expectations; operator provides missing
  later-run identifiers only if available. Narrative evidence stays labeled meanwhile.
- Acceptance: fixture corpus is public-safe and deterministic; every claimed closure
  has a failing-before/passing-after check; old telemetry gaps remain visible.
- Validation: run targeted regressions/fake-model scoring; inspect all fixture fields
  and history before publication; no real inference without its own budget authority.
- References: `skill/tests/test_tier4_da27c0.py`, `skill/tests/test_wire_adapter_v103.py`,
  `skill/tests/test_line_ranges_v2.py`, `skill/tests/fixtures/`,
  `AUDIT-COUNCIL-V2-EVAL-REPORT.md`.
- Milestone: v2.0.2 candidate.

### AUCDEV-006 — STANDARD / RELEASE / FORENSIC effort semantics

- Priority/status: P2 / OPEN.
- Problem/evidence: current CLI modes AUTO/CURRENT/RELEASE/HISTORICAL describe
  environments; no independent review-effort policy exists.
- Why it matters: ordinary reviews should retain valuable dual independent review
  without always paying for every release/forensic mechanism.
- Scope: design effort invariants, mandatory/optional stages, containment, evidence,
  budgets, outputs, and a compatibility table with existing environment modes.
- Non-goals: implement flags before design; remove independent review from STANDARD;
  make RELEASE ambiguous between two dimensions; build autonomous orchestration.
- Dependencies: measured manual cycles; AUCDEV-001/004 baseline trust semantics.
- Acceptance: STANDARD retains dual independent review; RELEASE names exact-target gates;
  FORENSIC names extra machinery and why; no silent mode downgrade or unsupported promise.
- Validation: design review using ordinary review, release qualification, and incident
  scenarios; estimate measured overhead; subsequent implementation gets its own tests.
- References: `skill/PUBLIC-CONTRACT.md`, `skill/scripts/environment_manager.py:resolve_mode`,
  `skill/scripts/budgets.py`, `AUCDEV-CONTROL-ROOM-RUNBOOK.md`.
- Milestone: v2.1 design only initially.

### AUCDEV-007 — Whole-program governor integration

- Priority/status: P2 / OPEN.
- Problem/evidence: runner stages call budgets.check, but dynamic-probe counters and
  record_omission have no general production orchestration callers; Opus usage is unknown.
- Why it matters: published defaults are not proof of a whole-program resource ceiling.
- Scope: inventory actual enforcement vs guidance; measure stages/probes and optional
  work; connect enforceable counters and explicit omissions where justified. Include
  deterministic ordering for equal started_at job timestamps and explicit treatment
  of unreadable/corrupt job records currently skipped by rebuild_metrics.
- Non-goals: fabricated Opus token usage, linear UI-quota estimates, skipping mandatory
  passes/fresh gates, accounting service or billing integration.
- Dependencies: real manual-cycle measurements; AUCDEV-006 design where applicable.
- Acceptance: every advertised cap identifies an enforcement point or guidance label;
  attempts, repairs, preflight failures and optional omissions are counted honestly;
  unknown usage remains null and governor cannot upgrade completeness; equal-timestamp
  rebuilds have a stable tie-breaker and corrupt inputs do not silently erase accounting.
- Validation: boundary tests against persisted jobs, failure/repair accounting, optional
  probe limits and metrics reconstruction; measured representative cycle costs.
- References: `skill/scripts/budgets.py`, `skill/scripts/codex_runner.py:enforce_budget`,
  `skill/scripts/specialists.py`, `skill/tests/test_telemetry_v2.py`,
  `skill/tests/test_telemetry_v103.py`, `skill/PUBLIC-CONTRACT.md`.
- Milestone: v2.1 after measurements.

### AUCDEV-008 — Human escalation and bounded retry semantics

- Priority/status: P2 / READY.
- Problem/evidence: attempts/repairs are bounded and SKILL caps 20 waits, but failure
  prose differs on exact-thread fallback, corrupt checkpoints, and quota completeness.
- Why it matters: recovery must not repeat paid work or silently weaken provenance.
- Scope: define terminal-vs-retryable matrix for quota/auth/environment/schema/process
  failure, progress/stall detection, operator handoffs and same-target resume rules.
- Non-goals: automatic credential repair, unbounded retries, ignoring failed integrity,
  required routine operator questions inside an otherwise valid audit.
- Dependencies: AUCDEV-004/009; retain current three-attempt/one-repair caps.
- Acceptance: each terminal status has one bounded disposition; integrity mismatch stops;
  thread replacement and omitted stages are explicit; escalation preserves artifacts.
- Validation: fake Codex exit/quota/auth/malformed/stall scenarios, exhausted budgets,
  missing session and resume checks; no new real model calls required for mechanics.
- References: `skill/protocols/failure-and-resume.md`, `skill/SKILL.md`,
  `skill/scripts/codex_runner.py`, `skill/tests/test_wait_lifecycle_v102.py`,
  `skill/tests/test_resume.py`.
- Milestone: v2.0.2 candidate.

### AUCDEV-009 — Reconcile executable protocol/schema instructions

- Priority/status: P0 / READY.
- Problem/evidence: evidence-policy still asks for legacy `lines`; current schemas use
  `line_ranges`. failure-and-resume includes quota-completeness and integrity-resume
  exceptions that conflict with stricter SKILL/public requirements.
- Why it matters: these Markdown files directly instruct the installed audit agents;
  changing them is product behavior, not harmless publication cleanup.
  Priority raised from P1: current executed instructions contradict v2 citation and
  mandatory-stage completeness rules, risking invalid output or overstated audit
  completion. Schema rejection limits some damage but does not resolve conflicting policy.
- Scope: a separately authorized focused protocol correction with source/schema/tests
  reviewed together; include consistent INVALID_AUDIT_ENVIRONMENT guidance.
- Non-goals: silently patch installed skill in this governance task; alter historical
  artifacts; loosen validators to fit stale instructions.
- Dependencies: agreed completeness policy (AUCDEV-004); AUCDEV-010 before qualification.
- Acceptance: citation examples use valid v2 shapes; no incomplete-required-stage
  upgrade; resume instructions preserve immutable checkpoints and explicit session rules;
  all published protocol examples validate against applicable schemas.
- Validation: documentation/example checks plus schema/migration/public-contract and
  resume tests; independent audit of the resulting candidate SHA.
- References: `skill/protocols/evidence-policy.md`, `skill/protocols/failure-and-resume.md`,
  `skill/SKILL.md`, `skill/schemas/finding.schema.json`, `skill/tests/test_schema_validation.py`.
- Milestone: v2.0.2 candidate.

### AUCDEV-010 — Reconcile existing installed qualification provenance

- Priority/status: P1 / READY (reconcile existing evidence before proposing new qualification).
- Problem/evidence: installed 84 source files match `8ae33444f349ce73c1359b963722e2d16acba630`;
  last committed INSTALLATION_VERIFIED cites `579e39a409a1b6df58368a7b07dbdbbed5839dd9`.
  Protocol version is 2.0; no explicit package patch-version marker or v2.0.1 tag exists.
  Operator clarification (2026-09-05): historical qualification/installation evidence
  exists outside the initial publication snapshot. Its contents/exact applicability
  have not been inspected in this optimization pass; absence from Git is not absence
  of qualification. READY describes evidence collection, not a qualified-auditor verdict.
- Why it matters: the installed candidate must not certify itself as the predecessor.
- Scope: first locate/reconcile existing operator-held audit/install evidence; import
  public-safe references/summaries/digests linking auditor/candidate SHAs, completeness,
  verdict, acceptance, installed identity and rollback. Private originals stay private.
- Non-goals: invent qualification from a commit title or byte match; overwrite installation;
  rerun an expensive qualification campaign as part of repository governance.
- Dependencies: access to existing operator-held evidence; a new audit is a fallback
  only after evidence insufficiency is established and the operator authorizes it.
- Acceptance: reconcile installed identity to historical independent qualification,
  or document the exact remaining evidence gap. Do not infer failure/absence from a
  missing standalone file. If evidence is insufficient, choose a verifiable predecessor
  and obtain authority before any new expensive qualification run.
- Validation: full SHA resolution, source/installed manifest comparison, audit checksum
  and verdict inspection; append qualification history without replacing earlier entries.
- References: `AUDIT-COUNCIL-V2-IMPLEMENTATION-REPORT.md` Installation section,
  `AUCDEV-QUALIFICATION-HISTORY.md`, `AUCDEV-CURRENT-STATE.md`.
- Opus-V5 extension progress (2026-09-06 → 2026-09-07; cumulative record, item
  remains OPEN): mechanical bootstrap lineage of sealed non-overwriting packages,
  each with its own fresh zero-frontier matrix (frontier_calls=0): prospective →
  remediation (R1–R4) → r2r5 → binding → custody → peerbind → peerbind-recordfix →
  **net-trust** (resolver + explicit CA; seal `c8905290…`, 121 records; Control
  Room mechanically accepted). One separately authorized Auditor-A execution ran
  against net-trust: it reached the real upstream and failed HTTP 401 PRE-INFERENCE
  (classification `NONCONFORMING_AUTHENTICATION_FAILURE_UPSTREAM_401_PRE_INFERENCE`;
  zero completed inference; authority consumed; barrier CLOSED; Sol untouched;
  Attempt-004 substantive result still unread; verified evidence archive
  SHA-256 `b506e3d3…`; credential source `opus-oauth-token`). The bounded
  OAuth-binding remediation then sealed `execution-addenda/opus-v5-oauthbind/`
  (MODE A Bearer-placeholder substitution; new mandatory OA matrix phase;
  frontier_calls=0; provider request count 0; authoritative matrix
  `validation-20260907T190621Z`), and its mechanics are now **CONTROL ROOM
  MECHANICALLY ACCEPTED** (accepted seal
  `9959bbf1385f0314c54b4b053f18c13fa111b9b1f6177b3de477a1d12fb15730`, 127
  manifest records). Terminology note: OA-1 mechanically executed the pinned
  Claude Code 2.1.261 CLI against strictly local synthetic infrastructure
  (3 AUTH_TOKEN + 3 control observations; client/wire-capability probes only;
  no real credential; no provider request; no frontier/model inference) —
  local synthetic CLI executions, NOT Auditor-A executions, creating no
  qualification or execution authority. Current chain state: no conforming
  Auditor-A first pass; prior real Auditor-A authority consumed; future Opus
  authority NONE pending fresh explicit operator authorization; first-pass
  barrier CLOSED; Sol/Auditor-B authority NONE; qualification verdict NONE;
  no runtime/install change. A dated append-only post-seal record-integrity
  correction was issued (sealed bytes unchanged; no matrix rerun; no reseal).
- Opus-V5 extension continuation (2026-09-08; item remains OPEN): fresh
  Auditor-A authority was granted after canonical publication `b05aa33e`,
  and exactly ONE real Opus execution ran against the accepted oauthbind
  package (session `cf71e782-9c4e-4e06-8733-0990b8329d4b`; one Claude CLI
  invocation; exit 0; real frontier inference completed; exclusive
  `claude-opus-5` modelUsage with strict modelUsage PASS; frozen structural
  validator FAIL `INVALID_FIRST_PASS: 'Target SHA' occurs 0 times; exactly
  one is required`; classification `NONCONFORMING_AUDITOR_A_FIRST_PASS`;
  nonconforming substantive artifact preserved unread — HASH-ONLY identity
  SHA-256 `68dae378…`, 38183 bytes; execution authority consumed; retry 0;
  no conforming Auditor-A first pass; first-pass barrier CLOSED;
  Auditor-B/GPT-5.6 Sol NOT STARTED; qualification NONE; the accepted
  oauthbind package remained 127/127 intact with its seal unchanged;
  verified evidence archive SHA-256 `838a2aa4…`). A mechanical census
  established strict frozen form 0/12 versus relaxed label recognition
  12/12 — a syntax/conformance failure, not missing content; the frozen
  validator remains authoritative. The bounded ZERO-FRONTIER
  structural-output-conformance remediation then sealed the non-overwriting
  successor `execution-addenda/opus-v5-structfmt/` (format-only trailer
  generated from the frozen validator's exact 12-field contract and
  composed AFTER the unchanged frozen prompt bytes; envelope-vs-structural
  validation terminology split; the frozen structural validator mechanically
  gates any CONFORMING classification; AUTOMATIC_REPAIR=false; new
  mandatory SF matrix phase with deterministic synthetic fixtures only;
  seal `e7b0a897e9b2a495174e62e584d6f0afe1cc328ec5a69eafb672136fe96f840f`,
  408 manifest records; authoritative matrix `validation-20260908T102043Z`
  OVERALL=PASS, frontier_calls=0, provider request count 0; three
  intermediate matrix runs preserved and accounted inside the sealed
  package). Successor Control Room disposition: CONTROL ROOM MECHANICALLY ACCEPTED
  (2026-09-08 post-acceptance record correction; sealed remediation archive
  `5ff306f7…` immutable). Future real Opus authority: NONE. Sol authority:
  NONE. Installed qualification provenance
  remains unresolved; runtime/install unchanged. This continuation does not
  close the original provenance-reconciliation scope, which remains
  unresolved.
- Opus-V5 identity-coverage continuation (2026-09-08; item remains OPEN):
  fresh operator authority was granted after the canonical `c284ce78`
  publication, and exactly ONE real Opus execution ran against the accepted
  structfmt package (session `a06eb35a-212a-43d6-a918-570c5ee94070`; one
  Claude CLI invocation; exit 0; real frontier inference completed;
  exclusive `claude-opus-5` modelUsage with strict modelUsage PASS; frozen
  structural validator FAIL `INVALID_FIRST_PASS: Claude CLI/model identity
  field is incomplete` — the CLI/model identity field did not contain both
  frozen-required tokens `claude-opus-5` and `2.1.261` while every earlier
  frozen check passed; classification `NONCONFORMING_AUDITOR_A_FIRST_PASS`;
  nonconforming substantive artifact preserved unread — HASH-ONLY identity
  SHA-256 `f599a6583690ba4060343c60e48dc141467205661932c3d003cdb91d69cabe69`, 41999 bytes; execution authority consumed; retry 0;
  no conforming Auditor-A first pass; first-pass barrier CLOSED;
  Auditor-B/GPT-5.6 Sol NOT STARTED; qualification NONE; the accepted
  structfmt package remained 408/408 intact with its seal unchanged;
  verified evidence archive SHA-256 `5e68380e…`). Bounded root cause: the
  structfmt guidance's overbroad value-free policy had not exposed the
  validator-enforced deterministic identity requirement — a prospective
  harness-guidance coverage defect, not a candidate or validator defect.
  The bounded ZERO-FRONTIER structural-identity-constraint remediation then
  sealed the non-overwriting successor `execution-addenda/opus-v5-structid/`
  (identity-exposing trailer composed AFTER the unchanged frozen prompt
  bytes, mechanically exposing the frozen CLI/model identity tokens
  `claude-opus-5` and `2.1.261` and the Auditor-A identity token set;
  machine-readable deterministic constraint inventory DC-1..DC-9 derived
  from the frozen validator with
  `ALL_MECHANICALLY_PREDETERMINED_VALIDATOR_CONSTRAINTS_GUIDED` coverage;
  sealed coverage checker failing closed; SF TR-4 refined to
  value-free-except-whitelisted-execution-identity; new mandatory SI matrix
  phase with deterministic synthetic fixtures only; frozen prompt, frozen
  validator, qualification contract, and strict modelUsage semantics all
  byte-unchanged; AUTOMATIC_REPAIR=false; seal
  `fde6cd776a4aa65d52a762be7122825f51782004d5c6e802ff9ccd9e740553fc`, 235
  manifest records; authoritative matrix `validation-20260908T140305Z`
  OVERALL=PASS, frontier_calls=0, provider request count 0; one intermediate
  failed matrix run preserved and accounted inside the sealed package; the
  five local-synthetic pinned-CLI E-phase sessions are deterministic
  client/wire route tests against local synthetic sinks only — NOT
  Auditor-A executions, creating no qualification or execution authority,
  and performing no frontier/model inference; SF 27/27 PASS and SI 14/14
  PASS).
  Successor Control Room disposition: **CONTROL ROOM MECHANICALLY
  ACCEPTED** (2026-09-08 post-acceptance record correction; record-only:
  sealed bytes, seal, matrix, and candidate/runtime unchanged; no matrix
  rerun; no reseal; no inference; no new authority). Future real Opus
  authority: NONE. Sol authority: NONE. Installed qualification provenance
  remains unresolved; runtime/install unchanged. This continuation does not close the original
  provenance-reconciliation scope, which remains unresolved.
- Opus-V5 prospective-precheck continuation (2026-09-08; item remains
  OPEN): fresh Auditor-A execution authority was granted after the canonical
  `d2a68bec` state, and exactly ONE sealed prospective launcher attempt ran
  against the CONTROL-ROOM-MECHANICALLY-ACCEPTED structid package: the
  isolation wrapper failed its prospective precheck BEFORE `PRECHECK_PASS`,
  BEFORE BubbleWrap namespace entry, and BEFORE any Claude CLI process was
  started — classification `FAILED_AUDITOR_A_EXECUTION_PRE_CLI_LAUNCH`;
  sealed-launcher invocations = 1; Claude Auditor-A CLI processes started =
  0; frontier/model inference 0; provider requests 0; session NONE;
  modelUsage ABSENT; tokens/cost NONE; substantive artifact NONE (none may
  ever appear for this event); execution authority consumed; retry 0;
  first-pass barrier CLOSED; Auditor-B/GPT-5.6 Sol NOT STARTED;
  qualification NONE; verified evidence archive SHA-256
  `82995b5a2e81c7e7db83b9684ed8063a8d65d56d7c5a0f498461ae3a994c0010`.
  Nonblocking historical terminology residual
  `LAUNCHER_ATTEMPT_COUNTER_MISLABELED_AS_CLI_INVOCATION`: the archive's
  orchestrator line `cli_invocations_performed=1` actually counts the single
  sealed-LAUNCHER attempt (authoritative process/phase evidence:
  sealed-launcher invocations = 1; Claude Auditor-A CLI processes started =
  0); the historical archive is NOT modified; all new records use distinct
  counters (sealed-launcher invocations / Auditor-A CLI sessions /
  pinned-CLI `--version` identity probes). Bounded root cause: the structid
  isolation wrapper's prospective-mode precheck pinned the obsolete
  STRUCTFMT trailer digest `7f098595…` while the accepted STRUCTID trailer
  is `52bfd1a5…` (launcher and seal gate were already correctly bound); the
  accepted predecessor matrix exercised the wrapper only in
  `V5R_MODE=validation`, which bypasses the prospective input/trailer
  branch. The bounded ZERO-FRONTIER prospective-precheck remediation then
  sealed the non-overwriting successor
  `execution-addenda/opus-v5-structid-preflight/` (authorized mechanical
  fix: the wrapper's single prospective expected-trailer digest constant
  updated to the exact accepted STRUCTID trailer `52bfd1a5…`, trailer
  preserved byte-for-byte, launcher binding and prelaunch seal-gate binding
  preserved, plus unavoidable package-root path updates; new mandatory PX
  matrix phase PX-1..PX-10 executing the ACTUAL successor wrapper in
  `V5R_MODE=prospective` with the exact frozen view/meta/evidence-MCP and
  trailer, actual pinned BubbleWrap and pinned CLI identity/version
  precheck, strictly local synthetic guard/socket infrastructure, and a
  deterministic benign `/usr/bin/true` namespace command — eight pinned-CLI
  `--version` mechanical identity probes counted separately, zero
  Auditor-A CLI sessions, zero frontier calls, zero provider requests;
  frozen prompt `755ced88…`, frozen structural validator `23d9b03f…`, and
  all trust boundaries byte-identical; `AUTOMATIC_REPAIR=false`; the
  accepted structid predecessor remains immutable — its bytes, seal
  `fde6cd77…`, own record, and results never modified or reused), seal
  `b48c74736e15985ebf3609a08dbe4ef5611ab7b8a65e937aa21a0f1dfc295820`, 147
  manifest records (NUL-safe; verified 147/147 with 0 missing / 0
  mismatched / 0 unmanifested trusted regular files); authoritative matrix
  `validation-20260908T174134Z` OVERALL=PASS, `frontier_calls=0`, provider
  request count 0, all inherited mandatory phases PASS (G-before, A-BC-S-P,
  R5, D, E, F, G-after, J, K, NT, OA, SF, SI) plus PX 10/10 PASS; one
  matrix execution, PASS on the first attempt, zero failed/intermediate
  matrix attempts. Successor disposition: **CONTROL ROOM MECHANICALLY ACCEPTED**
  (2026-09-08 post-acceptance record correction; record-only: sealed
  bytes, seal, matrix, and candidate/runtime unchanged; no matrix rerun;
  no reseal; no inference; no new authority). Future real Opus authority: NONE. Sol
  authority: NONE. Installed qualification provenance remains unresolved;
  runtime/install unchanged. This continuation does not close the original
  provenance-reconciliation scope, which remains unresolved.
Status record 2026-09-08 (FOURTH 8 Sep execution event; verified
nonconforming at the binding/integrity gate): fresh Auditor-A execution
authority was granted against the CONTROL-ROOM-MECHANICALLY-ACCEPTED
`opus-v5-structid-preflight` package (canonical base for the cycle
`c4be751e013d83db28c0ee19ee796c31a3313c2e`, live GitHub `master` resolved
EXACT before the pass; the package was verified 147/147 intact). Exactly
ONE sealed prospective launcher attempt ran; one substantive Auditor-A
session `d8c85a23-8565-4f59-81e2-4a9743e0eacd`; real Claude Opus inference
completed; exact modelUsage key set `["claude-opus-5"]` with the strict
modelUsage gate PASS; CLI exit 0; isolation exit 0; frozen structural
validator PASS; binding/integrity gate FAILED before
`OPUS_V5R_LAUNCH_PHASE=BINDING_INTEGRITY_PASS` — classification
`NONCONFORMING_AUDITOR_A_FIRST_PASS`. Verified root cause: the sealed
supervisor archived the runtime binding record only at
`guard-binding/run-<id>/GUARD-BINDING.json` while the sealed launcher
requires the direct per-attempt contract path `guard-binding/
GUARD-BINDING.json` (observed drift preserved under
`operator-diagnostics/opus-v5-structid-preflight/attempts/attempt-20260908T184502Z-lxLUcY/`:
run-scoped record present, direct record absent). Historical artifact
UNREAD/HASH-ONLY: `682413e549f81b3bcfeef2009729efb7d42b5a6ea588c649b073424de507338b`,
39983 bytes, 0444; response envelope
`5ee59d86c4f6f62c2c6be78b1fd61ff1894e202ac933478c785bb85a957d6c85`,
42010 bytes, 0444; the event's `FIRST-PASS.sha256` freeze record exists
but is NOT a conforming barrier digest; no retroactive repair or
reclassification. Authority consumed; retry 0; 39 directly observed
in-session `UPSTREAM_FAILURE` events; exact total provider request count
unobservable from the sealed guard logs (`num_turns=62` is never converted
into a provider-request count); first-pass barrier CLOSED; Auditor-B/
GPT-5.6 Sol NOT STARTED (authority NONE); qualification NONE. Verified
execution evidence archive SHA-256
`5c91ac6d74ad5b2e32f1eac3b3cc80e692565245f898ef5e47e13aa3617e5ada`.

Status record 2026-09-08 (binding-record path-contract mechanical
remediation; subsequently CONTROL ROOM MECHANICALLY ACCEPTED via the
2026-09-08 post-acceptance record correction below): exactly ONE bounded
ZERO-FRONTIER mechanical pass (not an Auditor-A retry; no real
Claude/Opus inference; no Auditor-B/Sol execution; no qualification
decision) sealed the non-overwriting successor
`execution-addenda/opus-v5-structid-preflight-bindpath/`, derived only
from the intact structid-preflight predecessor (seal `b48c7473…` verified
147/147 with 0 missing / 0 mismatched / 0 unmanifested trusted regular
files before any successor byte was written; predecessor immutable, seal
never reused). Authorized fix (producer-side only; launcher consumer
check byte-identical): the supervisor cleanup publishes a byte-identical
copy of the exact runtime `GUARD-BINDING.json` at the direct per-attempt
contract path via an exclusive no-clobber create, only after the binding
is established, inside the launcher's unique attempt record directory;
stale/pre-existing/symlink direct records and symlinked record dirs
(out-of-attempt escape) fail the run closed; byte identity is verified
against the runtime record and the retained run-scoped archival copy; no
peer/process/socket binding semantics or any other trust boundary changed.
New mandatory deterministic zero-frontier matrix phase `BP`
(BP-1..BP-12, `tests/test_binding_path.py`): actual-successor supervisor
lifecycle over strictly local synthetic infrastructure with a benign
command; exact direct-record contract path; byte identity across
authoritative copies; absent/stale/second-producer/symlink/escape
fail-closed; the exact historical failure shape reproduced with synthetic
metadata only; the EXACT sealed launcher binding/integrity gate logic
dynamically executed against deterministic synthetic frozen-output files;
frozen mode/digest regressions; inotify non-access proof for the
historical artifact; barrier/Sol fail-closed; exact future gate sequence
preserved. RED->GREEN discipline preserved (pre-fix BP-1/2/4/5/6/8 fail
exactly on the producer defect; post-fix 30/30 PASS). Frozen identities
preserved byte-for-byte: prompt `755ced88…`, structural validator
`23d9b03f…`, STRUCTID trailer `52bfd1a5…`, pinned Claude `4ae40dd1…`
(`2.1.261 (Claude Code)`), model `claude-opus-5`, `AUTOMATIC_REPAIR=false`.
The authoritative matrix, seal and BP identities for this successor are
recorded in the evidence archive accompanying this status record.
Disposition: `STRUCTID_PREFLIGHT_BINDING_PATH_MECHANICAL_REMEDIATION_PASS_FRONTIER_NOT_AUTHORIZED`.
Post-acceptance correction 2026-09-08 (record-only; no sealed package byte
modified, no matrix rerun, no reseal, no inference, no Auditor-B/Sol
launch, no barrier change, no qualification decision, no new execution
authority): Control Room has MECHANICALLY ACCEPTED
`execution-addenda/opus-v5-structid-preflight-bindpath/` — seal
`2851002fc54f146b8a252934775aa0b5459de0eb61c81ca036c2e43f146bf560`, 250
manifest records, authoritative zero-frontier matrix
`validation-20260908T195913Z` with all 17 mandatory phases PASS (SF 27/27,
SI 14/14, PX 10/10, BP 30/30; H phase authoritative sealed values:
live_components=51, inventory_table_components=50, mismatches=[]);
`frontier_calls=0`, provider request count 0, substantive Auditor-A
sessions during remediation 0. Counting terminology: the five E-phase
local-synthetic pinned-CLI sessions, the eight PX `--version` mechanical
identity probes, the five BP supervisor lifecycles with five BP seal-gate
`--version` probes, and any J/K mechanical version-probe executions are
NOT Auditor-A executions, performed zero frontier/model inference and
zero provider requests, and create no authority. One failed matrix
attempt `validation-20260908T194519Z` was preserved (K FAIL on the RI-2
supersession-record self-identity check); the final complete rerun
`validation-20260908T195913Z` PASSed. The accepted package is the sole
eligible package for any FUTURE Auditor-A execution, which still requires
a fresh explicit operator authorization (none exists). No conforming Auditor-A first pass
exists; future real Opus authority NONE; AUCDEV-010 remains OPEN;
installed qualification provenance remains unresolved; runtime/install
unchanged; the original provenance-reconciliation scope remains open.

Status record 2026-09-08 (FIFTH 8 Sep execution event; execution failure
during the substantive Claude session; recorded by a record-only
governance pass closed 2026-09-09 Europe/Istanbul, pass start
2026-09-08T21:14:39Z UTC): fresh Auditor-A execution authority was granted
(canonical base `ca8ad5507505b98963f0960973347fe8ea52bf8a`, live GitHub
`master` resolved and verified EXACT at pass start and re-verified EXACT at
close), and exactly ONE sealed prospective launcher attempt ran against
the CONTROL-ROOM-MECHANICALLY-ACCEPTED `opus-v5-structid-preflight-bindpath`
package (seal `2851002fc54f146b8a252934775aa0b5459de0eb61c81ca036c2e43f146bf560`,
250 manifest records, verified 250/250 intact before the attempt and
after). Exactly ONE substantive Auditor-A Claude CLI session started
(session `b13b36ab-fc17-4c42-aa8b-64d2bd017dc7`) and FAILED DURING
EXECUTION: machinery marker `CLAUDE_CLI_FAILURE`; accepted Control Room
classification `SEALED_EXECUTION_FAILURE_DURING_SUBSTANTIVE_CLAUDE_SESSION`;
explicitly NOT `CONFORMING_AUDITOR_A_FIRST_PASS` and NOT
`NONCONFORMING_AUDITOR_A_FIRST_PASS` — no first pass was produced.
Progression: prelaunch seal gate PASS; supervisor seal/nettrust prechecks
PASS; fresh guard runtime; guard bound; guard-only credential delivery
(peer-verified; `credential_received credential_len=108`); isolation
`PRECHECK_BEGIN`; `PRECHECK_PASS`; BubbleWrap execution entry
(`BUBBLEWRAP_ENTERED`); `CLAUDE_ARGV_READY`; then CLI failure. Claude CLI
exit 1; isolation exit 1; launcher exit 1 at `SUPERVISOR_ISOLATION_EXIT_1`.
Execution authority CONSUMED; top-level retry 0; NO second launcher
attempt; NO second substantive Claude session. Terminal response-envelope
metadata (mechanical scalars only; the envelope `result`-field value was
never read and no `result` substance is published): `is_error=True`;
`api_error_status=401`; `modelUsage={}`; `duration_api_ms=0`;
`total_cost_usd=0`; `num_turns=1` — NO successful model inference
established. NO `first-pass.md`; NO `FIRST-PASS.sha256`; NO
`SESSION-IDENTITY.json`; NO structural-validation artifact exists for this
event. Post-output gates NOT REACHED: the strict modelUsage launcher gate,
the frozen structural validator, the binding/integrity consumer gate, and
any conforming classification — the observed empty `modelUsage={}` would
not establish exclusive `claude-opus-5` use, and the sealed
strict-modelUsage gate itself did NOT execute. Provider telemetry
precision: exactly 11 guard `accept` relay events are DIRECTLY OBSERVED
(all `POST /v1/messages?beta=true`; all `credential_substituted=true`),
comprising the first relay plus 10 additional in-session client retry
relays (top-level retry remains 0); the guard does NOT record per-relay
HTTP status, so per-relay 401 is NOT claimed; the terminal response
envelope reports `api_error_status=401`. Mechanically established failure:
`PROVIDER_AUTHORIZATION_FAILURE / TERMINAL_401`. Credential-source
attribution boundary: the execution return attributes the failure to
delivery of an expired bootstrap credential copy instead of the live
operator credential — recorded ONLY as `OPERATOR_REPORTED_CREDENTIAL_SOURCE_ERROR`
(operator-reported; NOT upgraded into a mechanically established fact;
separate non-secret evidence would be required to independently prove the
source-selection chain), together with
`CREDENTIAL_SOURCE_ATTRIBUTION_NOT_INDEPENDENTLY_REPLAYABLE_FROM_EXECUTION_ARCHIVE`
(the accepted execution archive contains the operator attribution
narrative but does NOT contain a raw source-selection command/script or
independent source/expiry transcript sufficient for Control Room to
reproduce which credential source supplied the delivered bytes); NO
credential/token bytes were hashed, printed, copied, exposed, or archived.
BINDPATH result: the accepted producer-side correction was exercised
successfully BEFORE cleanup — the direct binding record and the retained
run-scoped binding record were byte-identical (exact SHA-256
`04633cd25fbe88ad7cb135e5c3ded97cc98019fb1211a86a764608c9c298ba7c`, size
`2337`); the direct record existed inside the exact attempt directory and
the record directory was not a symlink; the launcher's post-output
`BINDING_INTEGRITY_PASS` consumer gate was NOT REACHED because the Claude
CLI failed first — this run did NOT exercise that consumer gate. Cleanup
evidence residual: `CLEANUP_PROCESS_COUNT_EVIDENCE_CONFLICT` — the
execution archive's `post-run-integrity.txt` reports
`stale_guard_processes=3` while the operator classification prose states
cleanup left no residual guard/bwrap processes (operator-reported,
out-of-archive: a later self-excluding process check in the same operator
session observed none — NOT mechanically established from the archive);
an evidence-quality residual, NOT by itself a sealed-package defect
finding; the three counted processes are NOT inferred to have caused the
provider 401; historical zero-residual cleanup is NOT claimed as
independently established from this archive. Frozen response-envelope
metadata: SHA-256
`b32f4662c00e22b1ef1bdd2dee7bc13813f8efac07bd621d9b744d81b15b4194`, size
`1196`, mode `0444`; no first-pass substantive artifact exists for this
event. Immutable identities unchanged: candidate
`8ae33444f349ce73c1359b963722e2d16acba630`; accepted package
`execution-addenda/opus-v5-structid-preflight-bindpath/`; accepted seal
`2851002fc54f146b8a252934775aa0b5459de0eb61c81ca036c2e43f146bf560`; 250
manifest records; frozen prompt
`755ced882b0e4238a512e1ce7a4120956eb68f99dd77c4097a4cf07ab7285a72`; frozen
structural validator
`23d9b03fcbf15e2893a911999a0f39b5d625f2f9541392f3c63624b94af69d57`;
STRUCTID trailer
`52bfd1a5db2bc82762cef5ac3dcd30ad3f66cd312ba117f0ba3a5b5167f9bfa5`; pinned
Claude executable
`4ae40dd1784e85753e742e09f267d29ecbb82890361ad3817d27560866d364a6`;
Claude Code `2.1.261`; no package modification, reseal, or matrix rerun
occurred or was authorized; the accepted BINDPATH package remains the
mechanically accepted package — this execution failure does not by itself
supersede or revoke that mechanical package acceptance. Terminal
governance state: ALL FIVE 8 Sep Auditor-A execution authorities are
consumed; no conforming Auditor-A first pass exists; first-pass barrier
CLOSED; Auditor-B/GPT-5.6 Sol NOT STARTED; Sol authority NONE; future real
Opus authority NONE; qualification NONE; AUCDEV-010 OPEN; installed
qualification provenance unresolved; runtime/install unchanged. Verified
execution evidence archive SHA-256
`e17f682953d4ed7941305a542be40a5abdc5320e67a538e97edd42ccee9bbed3`.
This record-only pass created no future execution authority and implies
none.

Credential-source readiness preflight governance record (2026-09-08
UTC; record-only; zero-frontier), prepared against exact canonical base
`895c4e063019eb7a1e00c9987b41e7af5559909e` (live GitHub `master` resolved
EXACT at record start 2026-09-08T21:57:16Z, re-verified EXACT at close):
records exactly ONE bounded ZERO-FRONTIER operational readiness pass — no
Auditor-A execution, no Claude/Opus inference, no provider request, no
Auditor-B/GPT-5.6 Sol execution, no remediation, no package modification, no
qualification decision, no commit/push. Accepted classification
`CREDENTIAL_SOURCE_READINESS_MECHANICALLY_ESTABLISHED_FRONTIER_NOT_AUTHORIZED`
— recorded as a zero-frontier operational readiness observation only, NOT an
Auditor-A execution, NOT qualification, NOT package remediation, and NOT a
credential validity guarantee for all future time. Verified readiness
evidence archive SHA-256
`ec814c8b66ed3c3aa1cb047fcf7eaea7020b7eb52d6fc15855286711dca0abe8`.
Credential-source contract: the accepted future execution credential-source
identity is `/home/isa/.claude/.credentials.json`; selection is fail-closed
and requires the RESOLVED REALPATH to equal that exact path; ineligible
REGARDLESS of contents: any path under `/home/isa/audits`, any
`runtime-auth/` path, any `opus-home/` path, any execution-attempt/historical
attempt directory, any sealed `execution-addenda` package area, and
specifically
`/home/isa/audit-council-dev/runtime-auth/opus-home/.claude/.credentials.json`
(that reported bootstrap path was ABSENT during the pass and was mechanically
REJECTED by path policy regardless of content). Credential source identity is
NOT credential bytes; no credential/token bytes, hashes, fingerprints,
prefixes, suffixes, or encodings are published. Point-in-time non-secret
metadata observed: source realpath `/home/isa/.claude/.credentials.json`;
regular file; not a symlink; owner uid/gid `1000/1000`; mode `0600`;
access-token field PRESENT; access-token byte length `108` only; expiry
observed `2026-09-09T00:57:44Z`; verification time `2026-09-08T21:46:28Z`;
remaining lifetime at that verification `11475 seconds / 191.3 minutes`;
required execution-readiness floor `45 minutes`. Explicit:
`FUTURE_EXECUTION_MUST_REVERIFY_SOURCE_AND_EXPIRY_AT_DELIVERY_TIME` — the
record does NOT imply the credential remains valid indefinitely. Deterministic
selector testing: 8 synthetic negative cases REJECTED 8/8 as expected
(runtime-auth; opus-home; symlink/realpath escape; expired; under 45-minute
remaining lifetime; missing access-token field; empty token; unreadable
source), 1 synthetic valid live-source-shaped case ACCEPTED as expected, and
3 real-contract cases as expected — 12/12 expected behavior, zero real
provider access. Process baseline: initial relevant residual
guard/supervisor/BubbleWrap count = 0; final relevant residual count = 0;
self-excluding scan; no process killed. `CLEANUP_PROCESS_COUNT_EVIDENCE_CONFLICT`
is PRESERVED UNRESOLVED as historical evidence for the FIFTH execution; this
readiness baseline does NOT retroactively resolve that historical conflict.
Accepted package invariance re-verified read-only:
`execution-addenda/opus-v5-structid-preflight-bindpath/`, seal
`2851002fc54f146b8a252934775aa0b5459de0eb61c81ca036c2e43f146bf560`, manifest
`250/250`, candidate `8ae33444f349ce73c1359b963722e2d16acba630`, authoritative
matrix `validation-20260908T195913Z` `OVERALL=PASS` `frontier_calls=0`; no
package byte modified, no reseal, no matrix rerun. AF_UNIX runtime-remnant
precision: the readiness verifier observed 20 unmanifested AF_UNIX socket
runtime remnants (`guard.sock`, `sink.sock`) under historical E-phase result
directories — recorded ONLY as
`KNOWN_UNMANIFESTED_AF_UNIX_RUNTIME_REMNANTS_OUTSIDE_SEALED_TRUSTED_REGULAR_SET`;
no `zero filesystem extra entries` claim is made and the remnants are NOT
reinterpreted as a seal failure; the trusted manifest state remains `250/250`.
Evidence-quality residual: the readiness archive's malformed local-only
diagnostic values are non-authoritative and are NOT copied into canonical
governance; canonical authority for the pass is live GitHub `master`, verified
EXACT at start and close; the operator's pre-existing local divergent branch
remains non-canonical and unchanged. Historical blindness preserved: all
historical substantive Auditor-A artifacts remain UNREAD/HASH-ONLY; no
substantive result entered the governance archive. Terminal governance state:
credential-source readiness mechanically established at the observed preflight
time; any future execution must reverify the live source and a >=45-minute
remaining lifetime before credential delivery; all FIVE prior Auditor-A
authorities remain consumed; no conforming Auditor-A first pass exists;
first-pass barrier CLOSED; Auditor-B/GPT-5.6 Sol NOT STARTED; Sol authority
NONE; future real Opus authority NONE; qualification NONE; AUCDEV-010 OPEN;
installed qualification provenance unresolved; runtime/install unchanged; the
accepted BINDPATH mechanical acceptance stands. Disposition:
`CREDENTIAL_SOURCE_READINESS_GOVERNANCE_RECORD_PREPARED / FUTURE_EXECUTION_REVERIFY_REQUIRED / FRONTIER_NOT_AUTHORIZED`.
This readiness record creates NO future Auditor-A execution authority.

Status record 2026-09-09 (SIXTH Auditor-A authority; closed pre-execution at
the sealed launcher fixed-output freshness precondition; record-only governance
pass, closeout executed 2026-09-08 UTC): the SIXTH Auditor-A execution authority
was issued by Control Room against exact canonical HEAD
`69655a4fdc6290a994258d55ae6a5b0cb1161d2d` and CLOSED BEFORE the sealed
prospective launcher attempt started. Accepted classification
`PRE_EXECUTION_READINESS_FAILURE`; specific blocker
`SEALED_LAUNCHER_FIXED_OUTPUT_FRESHNESS_PRECONDITION_UNAVAILABLE`; explicitly NOT
classified as `CONFORMING_AUDITOR_A_FIRST_PASS`, NOT as
`NONCONFORMING_AUDITOR_A_FIRST_PASS`, and NOT as a substantive Claude execution
failure — no first pass existed. Verified closeout evidence archive SHA-256
`acb0c5863afa59c3e640828393341f790ef30a8d121f1b01899965d5a9e29963`.
Mechanically verified launcher blocker against the accepted bindpath package
(`execution-addenda/opus-v5-structid-preflight-bindpath/`, seal
`2851002fc54f146b8a252934775aa0b5459de0eb61c81ca036c2e43f146bf560`, trusted
manifest 250/250 PASS, sealed launcher SHA-256
`478ad909cad6b8240fddd8a5a7788015fbd465b45607736765da9a994a10e592`): launcher
line 60 fixes the output directory to
`$qroot/private/opus-v5-structid-preflight-bindpath`; no runtime output-directory
override exists; launcher line 141 requires that output directory to be completely
empty; the check is fail-closed; failure occurs before supervisor/BubbleWrap/
Claude/provider execution. The directory is non-empty because it contains the
FIFTH execution's frozen failure evidence, byte-identical to the previously
accepted FIFTH frozen metadata: `response.json` SHA-256
`b32f4662c00e22b1ef1bdd2dee7bc13813f8efac07bd621d9b744d81b15b4194`,
`CLI-EXIT-CODE.txt` SHA-256
`4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`,
`EXECUTION-PHASE.txt` SHA-256
`417750270a0aac71081cd9646ea605928ed57b08cf7d3e7603b18a2a7f5f952a`,
`PRELAUNCH-IDENTITY.txt` SHA-256
`b7e3ed39aee4cc12c7d943e0cab6d3645b7049f14b5553968c76efa4e80c5a14`, `stderr.log`
SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, plus the
empty `supervisor-runs/` directory; the FIFTH `response.json` result substance
remains UNREAD/HASH-ONLY. Sixth-authority counters: sixth authority CLOSED
pre-execution; sealed prospective launcher attempts = 0; substantive Auditor-A
Claude CLI sessions = 0; session ID NONE; credential-readiness gate invocations =
0; credential source access NONE; credential delivery NONE; provider calls 0;
guard relays 0; in-session provider retries 0; mechanical pinned-CLI `--version`
probes = 1; top-level retries 0; no response envelope generated by the sixth
authority (the historical FIFTH `response.json` at the same path is the FIFTH
event's frozen envelope and is NOT a SIXTH-event response envelope); no sixth
first-pass artifact; no sixth first-pass digest/freeze record. Credential
readiness: `DELIVERY_TIME_CREDENTIAL_GATE_NOT_INVOKED`; no expiry/lifetime value
is recorded for the sixth execution because no credential was accessed; the
canonical credential-source readiness contract remains valid, and a future
execution must still perform
`FUTURE_EXECUTION_MUST_REVERIFY_SOURCE_AND_EXPIRY_AT_DELIVERY_TIME` after the
launcher-freshness blocker has been remediated and before credential delivery.
Process state (point-in-time): initial relevant residual-process count = 0; final
relevant residual-process count = 0; self-excluding scan; no process killed;
`CLEANUP_PROCESS_COUNT_EVIDENCE_CONFLICT` preserved UNRESOLVED as historical.
Immutable identities unchanged: candidate
`8ae33444f349ce73c1359b963722e2d16acba630`; frozen prompt
`755ced882b0e4238a512e1ce7a4120956eb68f99dd77c4097a4cf07ab7285a72`; frozen
structural validator
`23d9b03fcbf15e2893a911999a0f39b5d625f2f9541392f3c63624b94af69d57`; STRUCTID
trailer
`52bfd1a5db2bc82762cef5ac3dcd30ad3f66cd312ba117f0ba3a5b5167f9bfa5`; pinned Claude
executable
`4ae40dd1784e85753e742e09f267d29ecbb82890361ad3817d27560866d364a6`; Claude Code
`2.1.261`; package bytes, seal, matrix, candidate, runtime and install unchanged.
Historical blindness: all historical substantive Auditor-A artifacts remain
UNREAD/HASH-ONLY (`68dae378c7056b6123f58ddc66f3a0600c56d341522d288d0a37261406038105`,
`f599a6583690ba4060343c60e48dc141467205661932c3d003cdb91d69cabe69`,
`682413e549f81b3bcfeef2009729efb7d42b5a6ea588c649b073424de507338b`,
`5ee59d86c4f6f62c2c6be78b1fd61ff1894e202ac933478c785bb85a957d6c85`, fifth failed
envelope `b32f4662c00e22b1ef1bdd2dee7bc13813f8efac07bd621d9b744d81b15b4194`);
none were relocated. Control Room remediation decision:
`FRESH_OUTPUT_SUCCESSOR_REMEDIATION_REQUIRED` and
`HISTORICAL_FROZEN_EVIDENCE_MUST_NOT_BE_RELOCATED`; the preferred resolution is a
NEW non-overwriting sealed successor package whose prospective launcher allocates
a fresh per-attempt output namespace; that remediation is NOT authorized in this
record-only pass; the FIFTH frozen output directory was NOT moved, archived,
deleted, renamed, chmod'ed, replaced, or otherwise mutated, and the blocker was
NOT solved by clearing the current path. Rationale: the current fixed-output +
empty-directory contract is effectively one-shot; moving historical evidence
would mutate historical path custody; relocation would need to recur after future
failed/completed executions; a fresh-output successor is the durable
non-destructive fix. Authority accounting after this record: FIVE prior execution
authorities remain consumed; the SIXTH authority is CLOSED pre-execution; no
seventh/future authority exists; no conforming Auditor-A first pass exists;
barrier CLOSED; Auditor-B/GPT-5.6 Sol NOT STARTED; Sol authority NONE; future
real Opus authority NONE; qualification NONE; AUCDEV-010 OPEN; installed
qualification provenance unresolved. The canonical event recorded here is the
SIXTH authority issued by Control Room against canonical HEAD
`69655a4fdc6290a994258d55ae6a5b0cb1161d2d` and closed by the accepted archive
`acb0c5863afa59c3e640828393341f790ef30a8d121f1b01899965d5a9e29963`; an earlier
operator closeout artifact of a claimed prior "sixth issuance" at the same
blocker exists but is NOT canonicalized by this record. Disposition:
`SIXTH_PREEXECUTION_CLOSEOUT_GOVERNANCE_RECORD_PREPARED / FRESH_OUTPUT_SUCCESSOR_REMEDIATION_REQUIRED / FRONTIER_NOT_AUTHORIZED`.
This record creates no future execution authority.

2026-09-09 FRESHOUT successor post-acceptance governance record (record-only;
the remediation executed 2026-09-09 UTC under exactly ONE bounded ZERO-FRONTIER
mechanical authorization — no Auditor-A retry, no Claude/Opus inference, no
provider request, no credential access/delivery, no Auditor-B/Sol execution, no
qualification, no installation, no package modification, no reseal, no matrix
rerun, no commit, no push): Control Room disposition
**`FRESH_OUTPUT_SUCCESSOR_MECHANICALLY_ACCEPTED`** (mechanical acceptance is
NOT qualification). Accepted successor
`execution-addenda/opus-v5-structid-preflight-bindpath-freshout/`, seal
`80ddad6d5aeae148887d76bb6c75f5acf06b3ba2c7eca7033322bb15f96b16cf`, trusted
manifest 457 records: 457/457 PASS, zero missing, zero mismatched, zero
unmanifested trusted regular files, anchor manifest byte-identical, anchor
digest equals the successor seal, sealed prelaunch gate PASS records=457.
Accepted remediation evidence archive SHA-256
`b1af2c2d3c329d597341621de0b304bcb6d05a04a7c55c8d30002486fb91d7c7`. The
previously canonical defect is mechanically resolved: the immediate predecessor
`execution-addenda/opus-v5-structid-preflight-bindpath/` (seal
`2851002fc54f146b8a252934775aa0b5459de0eb61c81ca036c2e43f146bf560`, launcher
SHA-256 `478ad909cad6b8240fddd8a5a7788015fbd465b45607736765da9a994a10e592`)
used one fixed reusable Auditor-A output directory with empty-directory
freshness applied to that historical reusable path; the FIFTH frozen evidence
permanently occupied it; the launcher was effectively one-shot; the SIXTH
authority closed pre-execution with launcher attempts = 0. The Control Room
decisions `FRESH_OUTPUT_SUCCESSOR_REMEDIATION_REQUIRED` and
`HISTORICAL_FROZEN_EVIDENCE_MUST_NOT_BE_RELOCATED` are now mechanically
satisfied; the historical SIXTH closeout is NOT rewritten. Accepted fresh-output
design (successor launcher SHA-256
`d18af82a72deb65ac664dfcf7528277df1dda4b369d6686c18ed1c8c2e1d85d4`): output
root `$qroot/private/opus-v5-structid-preflight-bindpath-freshout/attempts`;
output directory generated internally per launcher attempt; identity derived
from the same validated fresh `attempt_dir` identity; no arbitrary
operator/environment output override; output must not pre-exist; exclusive
fail-closed creation; mode `0700`; realpath containment inside the exact
expected output root; symlink/collision/escape fail-closed; historical output
never cleared/moved/reused; the preserved empty-directory freshness assertion
applies only to the new per-attempt directory; `INVOCATION.txt` records attempt
identity/output path/root/allocation; auditor isolation uses that exact output;
frozen structural validation targets that exact per-attempt `first-pass.md`;
post-output integrity checks target the same exact output; binding-record
mechanics remain tied to the corresponding `attempt_dir`. Matrix acceptance:
authoritative run `validation-20260909T010308Z` OVERALL=PASS; mandatory phases
18/18 PASS (`G-before, A-BC-S-P, R5, D, E, F, G-after, J, K, NT, OA, SF, SI,
PX, BP, FO, H, I`); counts R5 32, K 39, SF 27/27, SI 14/14, PX 10/10, BP
30/30, FO 31/31; G-before == G-after byte-identical; frontier_calls = 0;
provider/frontier real calls = 0; substantive Auditor-A sessions = 0;
mechanical pinned-Claude `--version` probes = 13 total (PX 8; BP 5; FO 0);
synthetic/local mechanical CLI activity is NOT Auditor-A inference.
RED->GREEN / intermediate history preserved (all runs remain sealed as
evidence; none hidden or deleted): `validation-20260909T002920Z` OVERALL FAIL,
BP only, all other mandatory phases including FO PASS;
`validation-20260909T004043Z` OVERALL PASS, later superseded because package
bytes subsequently changed during seal-gate implementation correction;
`validation-20260909T005226Z` OVERALL FAIL, SI only, all other phases including
FO PASS; `validation-20260909T010308Z` final authoritative OVERALL PASS after
final bytes; plus the retained first seal attempt failure where the inherited
pipeline-style membership check encountered a `set -o pipefail` / early-`grep
-q` SIGPIPE race at the enlarged manifest. DIFF-INVENTORY PRECISION CORRECTION
(evidence/reporting count correction only; does NOT change package bytes,
seal, matrix, or acceptance): the implementer's summary
`differing_or_added=10` failed to increment its counter for ADDED entries
before `continue`; the correct component-level inventory excluding validation
results, `__pycache__`, and the package manifest is 51 predecessor files /
53 successor files / 34 byte-identical / 7 identical after
package-identity/path normalization / 10 modified existing / 2 newly added
(`tests/test_freshout.py`, `FRESHOUT-REMEDIATION-RECORD.md`) / 0 removed;
therefore 12 entries are modified-or-added after normalization (10 modified
existing + 2 added). SEAL-GATE IMPLEMENTATION PRECISION: the successor
`prelaunch-seal-gate.sh` is NOT byte-identical to the predecessor; its
trust-boundary membership semantics are preserved, but its implementation
contains TWO inherited SIGPIPE-safe membership rewrites — `tests/test_oauthbind.py`
and `tests/test_binding_path.py`, from the predecessor shape `tr '\0' '\n' |
sed ... | grep -qxF` to `grep -qxF <target> "$tmp_records"` — plus TWO NEW FO
membership assertions using `$tmp_records` (`tests/test_freshout.py`,
`FRESHOUT-REMEDIATION-RECORD.md`); do NOT describe all four as inherited
rewrites. Control Room independent mechanical finding:
`SEALGATE_MEMBERSHIP_SEMANTICS_PRESERVED_WITH_SIGPIPE_SAFE_IMPLEMENTATION_REWRITE`
— `$tmp_records` is generated from the same already-validated NUL manifest
records and contains the exact sorted relative-path membership set; the
replacement performs the same exact fixed-string whole-line membership
predicate; no accepted membership is broadened; no fail-closed trust check is
removed; it removes only the spurious upstream SIGPIPE failure caused by early
`grep -q` under `pipefail`; accepted as implementation-equivalent hardening
preserving trust-boundary semantics, not a separate product/authentication
behavior change. Predecessor and frozen-history invariance: predecessor seal
`2851002fc54f146b8a252934775aa0b5459de0eb61c81ca036c2e43f146bf560` 250/250,
immutable historical package, never resealed or relabelled; FIFTH frozen
evidence preserved at its historical path with hash-only invariance PASS
(`response.json` `b32f4662c00e22b1ef1bdd2dee7bc13813f8efac07bd621d9b744d81b15b4194`,
`CLI-EXIT-CODE.txt` `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`,
`EXECUTION-PHASE.txt` `417750270a0aac71081cd9646ea605928ed57b08cf7d3e7603b18a2a7f5f952a`,
`PRELAUNCH-IDENTITY.txt` `b7e3ed39aee4cc12c7d943e0cab6d3645b7049f14b5553968c76efa4e80c5a14`,
`stderr.log` `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
`supervisor-runs/` remained empty); no historical substantive artifact was
read. Frozen identities unchanged: candidate
`8ae33444f349ce73c1359b963722e2d16acba630`; frozen prompt
`755ced882b0e4238a512e1ce7a4120956eb68f99dd77c4097a4cf07ab7285a72`; frozen
structural validator
`23d9b03fcbf15e2893a911999a0f39b5d625f2f9541392f3c63624b94af69d57`; STRUCTID
trailer `52bfd1a5db2bc82762cef5ac3dcd30ad3f66cd312ba117f0ba3a5b5167f9bfa5`;
pinned Claude executable
`4ae40dd1784e85753e742e09f267d29ecbb82890361ad3817d27560866d364a6`; Claude
Code `2.1.261`; guard implementation and credential-delivery client remain
byte-identical to the predecessor; supervisor/authentication/binding semantics
unchanged except unavoidable successor package path identities; credential
source NOT accessed. Credential readiness remains future-time gated:
`FUTURE_EXECUTION_MUST_REVERIFY_SOURCE_AND_EXPIRY_AT_DELIVERY_TIME` — any
future separately authorized execution must still require exact source
`/home/isa/.claude/.credentials.json` and at least 45 minutes remaining
lifetime immediately before delivery; this post-acceptance record creates no
execution authority. Terminal authority state after this record: FIVE earlier
real execution authorities remain consumed; SIXTH authority remains CLOSED
pre-execution; no seventh/future Auditor-A authority exists; no conforming
Auditor-A first pass exists; barrier CLOSED; Auditor-B/GPT-5.6 Sol NOT
STARTED; Sol authority NONE; future real Opus authority NONE; qualification
NONE; AUCDEV-010 OPEN; installed qualification provenance unresolved;
runtime/install unchanged. Mechanical successor acceptance is NOT
qualification. Disposition:
`FRESH_OUTPUT_SUCCESSOR_POSTACCEPTANCE_GOVERNANCE_RECORD_PREPARED / DIFF_COUNT_CORRECTED / SEALGATE_MEMBERSHIP_EQUIVALENCE_RECORDED / FRONTIER_NOT_AUTHORIZED`.

2026-09-09 SEVENTH Auditor-A authority status record (execution executed
2026-09-09 UTC; record-only governance pass 2026-09-09): the SEVENTH bounded
execution authority ran against the accepted
`execution-addenda/opus-v5-structid-preflight-bindpath-freshout/` package and
produced the FIRST Control-Room-accepted conforming Auditor-A first pass in the
Opus-V5 chain — accepted classification `CONFORMING_AUDITOR_A_FIRST_PASS`,
record `SEVENTH_AUDITOR_A_FIRST_PASS_ACCEPTED`. Canonical/package/candidate:
live GitHub `master` `67267d5bc0787e6d1515769fed1a629c7b3fb833` EXACT pre and
post; candidate `8ae33444f349ce73c1359b963722e2d16acba630`; seal
`80ddad6d5aeae148887d76bb6c75f5acf06b3ba2c7eca7033322bb15f96b16cf` pre == post;
manifest 457/457 PASS with 0 missing / 0 mismatched / 0 unmanifested trusted
regular files, anchor manifest byte-identical, digest anchor equals seal, sealed
prelaunch gate PASS records=457; package/candidate/runtime/install unchanged;
frozen identities unchanged (prompt `755ced88…`, validator `23d9b03f…`, trailer
`52bfd1a5…`, FRESHOUT launcher `d18af82a…`, pinned Claude `4ae40dd1…` / Claude
Code `2.1.261`, required model `claude-opus-5`; `AUTOMATIC_REPAIR=false`). FRESHOUT
attempt identity: `attempt-20260909T094248Z-FUUZDc`; output root
`/home/isa/audits/aucdev-bootstrap-8ae33444-attempt2/private/opus-v5-structid-preflight-bindpath-freshout/attempts`;
exact per-attempt output `…/attempts/attempt-20260909T094248Z-FUUZDc`;
`FRESH_OUTPUT_ALLOCATED` with internal identity derivation, no override, no
pre-existence, exclusive creation, mode `0700`, canonical realpath containment,
no symlink/collision/escape, `INVOCATION.txt` bound, isolation/structural/binding
all on that exact identity. Credential delivery-time readiness (metadata only):
source `/home/isa/.claude/.credentials.json` exact realpath, uid/gid `1000/1000`,
mode `0600`, regular non-symlink, token PRESENT byte length `108` only, verified
`2026-09-09T09:42:53Z`, expiry `2026-09-09T15:51:20Z`, remaining `368.5` minutes
(floor 45) PASS, one sealed peer-bound delivery, client RC 0;
`FUTURE_EXECUTION_MUST_REVERIFY_SOURCE_AND_EXPIRY_AT_DELIVERY_TIME` (the
historical credential is NOT implied valid for any future execution); no
credential/token bytes, hashes, fingerprints, prefixes, suffixes, or encodings
recorded. Execution counters: launcher attempts 1; mechanical `--version` probes
5; substantive Auditor-A sessions 1; top-level retry 0; session
`fd7102dc-9eb2-43a5-8b9c-a861bf961c48`; CLI exit 0, isolation exit 0, launcher
exit 0; residual relevant processes 0 initial / 0 final, none killed;
historical `CLEANUP_PROCESS_COUNT_EVIDENCE_CONFLICT` remains unresolved and
unrelated. Progression (observed order): `SEAL_GATE_PASS`, `PREFLIGHT_PASS`,
`NETTRUST_PASS`, `GUARD_BOUND`, `CREDENTIAL_RECEIVED_GUARD_ONLY`, `AUDITOR_BEGIN`,
`PRECHECK_BEGIN`, `PRECHECK_PASS`, `BWRAP_EXEC`, `AUDITOR_EXIT_0`,
`STRUCTURAL_VALIDATION_PASS`, `BINDING_INTEGRITY_PASS`,
`CONFORMING_AUDITOR_A_FIRST_PASS`; no conformance stage claimed before its
predecessor gate. Model identity: exact modelUsage key set `["claude-opus-5"]`
(`STRICT_EXCLUSIVE_MODELUSAGE_PASS`); cost USD `2.67339325`; duration
`770665` ms; `num_turns=42` (never converted to a provider request count).
Structural: `STRUCTURAL_OUTPUT_CONTRACT_PASS`, frozen validator exit `0` on the
exact SEVENTH per-attempt `first-pass.md`;
`MATERIAL_COMPLETENESS_REQUIRES_HUMAN_REVIEW=true` (NOT a completed human
substantive review); `AUTOMATIC_REPAIR=false`. Binding/integrity:
`BINDING_INTEGRITY_PASS`; direct and run-scoped records byte-identical;
binding-record SHA-256
`0346b10f5dc4cddf05b3e61acbc43d118550198a5c85a22bb51f4ef8ae109eed`; guard
peer/starttime verification preserved; no credential material exposed. Frozen
Auditor-A artifacts: first pass `0171b7ff60c721297ae204f7020074d8772a1dc28e354cd81dc571921218c136`
(45368 bytes, mode 0444) and response envelope
`6b1424f87922619a0af36e927e7decc71a094f8ce6ad90249b45605f76754717`
(47330 bytes, mode 0444), frozen, digest record present, no automatic repair,
substantive content UNREAD, response substance private, historical substantive
artifacts UNREAD/HASH-ONLY; no substantive findings in governance files.
Telemetry count correction
(`TELEMETRY_COUNT_CORRECTION_24_DIRECTLY_LOGGED_UPSTREAM_FAILURE_EVENTS`):
independent Control Room inspection of the raw archived `guard-log.jsonl`
established 28 total records — 4 lifecycle (`start`,
`credential_socket_listening`, `listening`, `credential_received`) and exactly
24 records with event `error` / code `UPSTREAM_FAILURE` / method `POST` / path
`/v1/messages?beta=true`, 0 `accept`, 0 `reject`, no per-relay HTTP status
field; the prior operator count of 25 was a nonblocking off-by-one
evidence/reporting error and is NOT canonicalized; do NOT infer that all 24
provider operations failed, one-to-one request correspondence, or any provider
request count from `num_turns=42`
(`EXACT_PROVIDER_REQUEST_COUNT_NOT_ESTABLISHABLE_FROM_GUARD_LOG`; the guard
relays response bytes as they arrive and a later upstream reset can reach the
`UPSTREAM_FAILURE` path after relay — the label alone is not a conformance
failure); the correction does not change the accepted classification.
Authority accounting after this record: FIVE earlier real Auditor-A execution
authorities consumed; SIXTH authority CLOSED pre-execution; SEVENTH authority
CONSUMED and CLOSED (exactly one sealed prospective attempt; exactly one
substantive Auditor-A Claude session; top-level retry 0); no EIGHTH/future
Auditor-A authority exists. Barrier/blindness: first-pass barrier REMAINS
CLOSED; Auditor-A artifact NOT exposed to Auditor-B; GPT-5.6 Sol NOT STARTED;
Sol authority NONE; no cross-examination, adjudication, or qualification; a
separate Control Room decision after canonical publication is required before
Auditor-B may execute. Qualification remains NONE (a conforming first pass is a
prerequisite milestone, not a final qualification verdict); installed
qualification provenance remains PENDING EVIDENCE RECONCILIATION; AUCDEV-010
remains OPEN. Verified execution evidence archive SHA-256
`6fbd364b432788258efc4c3cb3ef4a86c30c00d423b3441e209f6d4572d0f903`.
Disposition:
`SEVENTH_CONFORMING_AUDITOR_A_GOVERNANCE_RECORD_PREPARED / TELEMETRY_COUNT_CORRECTED / BARRIER_CLOSED / SOL_NOT_AUTHORIZED / QUALIFICATION_NONE`.

2026-09-09 FIRST Auditor-B (GPT-5.6 Sol) authority status record (execution
executed 2026-09-09 UTC; record-only governance pass 2026-09-09): after
canonical publication of the SEVENTH record (this record's exact canonical
base `413712b489fe30adb87915718044a127527f99db`, live GitHub `master`
re-resolved EXACT at the record's start and close), Control Room granted the
FIRST Auditor-B/GPT-5.6 Sol blind first-pass authority; it executed exactly
ONE substantive session and closed NONCONFORMING. Accepted classification
`NONCONFORMING_AUDITOR_B_FIRST_PASS` with evidence acceptance
`AUDITOR_B_FIRST_PASS_EVIDENCE_ACCEPTED` (Control Room independently verified
the execution evidence archive SHA-256
`b852747a63a58e1b151d85452792a3bb3be58ee2e9d91b719eca6ea4febb1356`, exact
size 13183 bytes: 21 total tar members; 18 regular files; 3 directories; 17
outer SHA256SUMS records excluding SHA256SUMS itself with 17/17 checksum
PASS; complete regular-file coverage; no unsafe archive members; no
substantive Auditor-A content; no substantive Auditor-B content; no raw
frozen Sol prompt; independent secret-shaped scan PASS). A first-pass
artifact EXISTS and the single substantive model execution COMPLETED — this
is not an execution-failure classification; the frozen output-contract
validator REJECTED the artifact: exact structural failure
`CONTRACT_DIGEST_FIELD_NOT_EXACT` (frozen validator output
`INVALID_FIRST_PASS: Contract digest field is not exact`, exit 1); the
artifact was NOT repaired, the incorrect field value was NOT inspected, and
no root cause beyond the mechanically established validator failure is
claimed or inferred. `NO_SOL_SEAL_CREATED` (sealing is validator-gated; the
seal step aborts at its validation gate). Frozen Auditor-B artifacts
(UNREAD/HASH-ONLY): `private/sol/first-pass.md` SHA-256
`29266fadac540bbf7156dc5aafa0d53ba33f69e60aeaa2ac34b9c5871d918f6e`, 1088
bytes, mode 0444 — frozen, unrepaired, launcher-hashed; `private/sol/
events.jsonl` SHA-256
`12cb40d36c4227e351f42c7d20999ca87f8e6fb8e94d6dd3d55bb7a5c8cd1a7b`, 2497
bytes, mode 0444; no substantive model result text is included in
governance. Execution identity: model `gpt-5.6-sol`; reasoning `xhigh`;
`codex-cli 0.153.4`; fresh thread `01a085e0-da05-70e2-aefe-59b2393a4749`;
session mode `--ephemeral`, no resume, no `--last`; substantive model-call
count 1; launcher exit 0; CLI exit 0; mechanical event inventory
`thread.started=1`, `turn.started=1`, `turn.completed=1`, `item.completed=4`,
non-Sol model strings 0, fallback fields 0, reroute text 0 — these
mechanical launcher checks PASS but do NOT override the frozen
structural-validator failure. Frozen bootstrap identities unchanged pre and
post: candidate `8ae33444f349ce73c1359b963722e2d16acba630`; baseline
`68ce12acc6c614d1876b902e6511d21f95b33c43:skill`; qualification contract
SHA-256
`3d7168ba3768485a16df0d2fcb266b6962b4657d2d30eaf1bc97f237a9d17bbf`; common
input manifest SHA-256
`14cd8b3b06dfd8edf679486d955c40f8e0096345e33c669bb9f279aed8b09ad8`;
first-pass output contract SHA-256
`3b787c0689a718e5194042972ad97e26bf5b51481560706b5bc887122d1f2c3a`; Sol
bundle SHA-256
`162c5bcc3e4f8b98534df6210306090d4ad7bc2ee1aa2a70f5dae74d4ed0099c` (opus
symmetric bundle identical); frozen Sol prompt
`views/sol/input/common/SOL-FIRST-PASS-PROMPT.md` SHA-256
`8b8f8e3954631759fa0fd41747ce0b52669c920869fde16f799e681b91c617b6`;
`BOOTSTRAP_DELTA_COMPLETE` with frozen input surface 224/224 PASS pre and
post. Blindness `AUDITOR_B_BLIND_VIEW_PASS`: `/audit` exposes only `input`,
`meta`, `output`; common input read allowed, write denied; own output write
allowed; peer output denied; host repository denied; Claude skill path
denied; Codex history denied; host `.bashrc` denied; host `.ssh` denied;
entire bootstrap root denied; alternate symlink escape denied; MCP
credential/traversal reads denied; Auditor-A substantive artifacts were never
read, opened, hashed, summarized or exposed to the model; executor
inspection was names/stat metadata only; pre/post metadata for all
Auditor-A/Opus historical entries remained identical (the `private/sol`
directory entry changed only because this Auditor-B execution created its
own frozen output); barrier remains CLOSED. Authentication (non-secret
mechanics only): PAYG environment gate PASS-absent (no `OPENAI_API_KEY`, no
`CODEX_API_KEY`); ChatGPT subscription auth; in-sandbox `codex login status`
PASS; no credential contents were included, hashed, fingerprinted or
otherwise exposed. Execution deviations, recorded precisely: DEV-1 — the
frozen isolation logic contained an unconditional Claude executable hash pin
even though the Sol branch does not mount or execute Claude; the current
host NVM Claude binary had drifted; the execution wrapper verified the
required historical SHA against the archived hash-exact pinned Claude
2.1.261 binary
`4ae40dd1784e85753e742e09f267d29ecbb82890361ad3817d27560866d364a6`; Claude
was NOT mounted into the Sol view and NOT executed. DEV-2 — the historical
bootstrap Codex auth copy was stale relative to the current logged-in host
state; the execution used the existing live ChatGPT subscription credential
at `/home/isa/.codex/auth.json` as a read-only sandbox bind; its contents
were NOT read by the executor, printed, hashed, copied or archived;
in-sandbox `codex login status` established logged-in readiness. Deviation
governance boundary
`EXECUTION_DEVIATIONS_RECORDED_NOT_AUTOMATICALLY_CANONICALIZED_FOR_FUTURE_SUCCESS`:
Control Room accepts these facts as part of the evidence for this
NONCONFORMING event only; this acceptance does NOT establish that the
modified execution wrapper is itself a canonical successor execution package
suitable for a future successful Auditor-B run; no future authority may be
granted based solely on these deviations; a future Control Room decision may
require a bounded zero-frontier Sol execution-environment reconciliation
before any new substantive B authority. Post-run invariance PASS: candidate
identity unchanged; baseline identity unchanged; qualification contract
unchanged; common manifest unchanged; first-pass output contract unchanged;
Sol input bundle unchanged; 224/224 frozen input surface unchanged;
Auditor-A private metadata unchanged; barrier CLOSED; canonical GitHub HEAD
unchanged during execution; qualification NONE; no cross-examination,
adjudication or qualification occurred. Frozen Auditor-A state preserved:
`SEVENTH_AUDITOR_A_FIRST_PASS_ACCEPTED` and its
`CONFORMING_AUDITOR_A_FIRST_PASS` classification remain canonical; the
Auditor-A first-pass artifact remains private, frozen and UNREAD; no
Auditor-A substance was exposed to Auditor-B and no Auditor-B substance was
exposed to Auditor-A. Terminal authority state after this record: FIVE
earlier Auditor-A execution authorities consumed; SIXTH Auditor-A authority
CLOSED pre-execution; SEVENTH Auditor-A authority consumed/closed with the
accepted conforming A pass; no EIGHTH Auditor-A authority; FIRST
Auditor-B/Sol authority consumed/closed; Auditor-B first pass classified
`NONCONFORMING_AUDITOR_B_FIRST_PASS`; no second Auditor-B authority; no
automatic retry; barrier CLOSED;
cross-examination authority NONE; adjudication authority NONE;
qualification NONE; AUCDEV-010 remains OPEN; installed qualification
provenance remains `PENDING EVIDENCE RECONCILIATION`. No remediation
decision is made by this record: the frozen Sol prompt, frozen output
contract, validator, launcher, isolation wrapper, Sol bundle and common
manifest are all unchanged; no further Sol model call is authorized; after
this governance event is independently accepted and published, Control Room
will separately determine whether the next bounded action is zero-frontier
structural-output remediation, zero-frontier Sol execution-environment
reconciliation, both in a staged order, or another governance disposition.
Disposition:
`NONCONFORMING_AUDITOR_B_GOVERNANCE_RECORD_PREPARED / CONTRACT_DIGEST_MISMATCH_RECORDED / EXECUTION_DEVIATIONS_RECORDED / BARRIER_CLOSED / QUALIFICATION_NONE`.

2026-09-09 Stage-1 Sol execution-boundary successor post-acceptance status
record (remediation executed 2026-09-09 UTC; record-only governance pass
2026-09-09): against the exact canonical base
`35c02c60fb624ab9985d10ff9bed3fe5cb00d4c3` (live GitHub `master`
re-resolved EXACT at the record's start and close), Control Room
mechanically accepted the Stage-1 zero-frontier Sol execution-boundary
successor. Accepted disposition
`SOL_EXECUTION_BOUNDARY_SUCCESSOR_MECHANICALLY_ACCEPTED` — mechanical
acceptance is NOT an Auditor-B first pass and NOT qualification. Control
Room independently verified the accepted evidence archive SHA-256
`4ff28849573e603b37b586ba2705207bcf68bfea6813b3a6c7bf3049da18a697`, exact
size 242225 bytes (190 total tar members; 173 regular files; 17
directories; no symlink/hardlink/special members; 172 outer SHA256SUMS
records excluding itself, 172/172 PASS; complete regular-file coverage;
independent secret-shaped scan PASS). Successor identity: package
`execution-addenda/sol-v1-execbound/`; seal SHA-256
`76ee6a5158792215bcda8f9cd3e845f02570012b0205844032d48ae88ff66ecc`;
trusted manifest 139 records (139/139 PASS; zero missing; zero mismatched;
zero unmanifested trusted regular files; NUL-safe; external anchor manifest
byte-identical; digest anchor equals the exact seal; post-seal prelaunch
gate PASS); launcher
`87a7eb179262b812db6deba47ff8e5b5b417e6cf794a0b5223ea8d6719308d21`; Sol
isolation wrapper
`37a166feb4d618623d9889ae5efacd958d95cc8db2baa23ab7c899adcd8164b2`;
prelaunch seal gate
`b431191af5788052f61220a745fedbc80a4720830f9f8e10ca2f6b2d3ae4d7cb`;
attempt sealer
`021ad99066075a87ca08327aeb42fa761d37f2c94f29e6fbccc8781d9481d84f`.
Fixed-output RED: `SOL_FIXED_OUTPUT_FRESHNESS_BLOCKER_REPRODUCED` —
historical frozen predecessor `output=$qroot/private/sol` with an
empty-directory requirement; historical `private/sol` held seven frozen
entries; the exact frozen predicate failed rc=1; the actual frozen launcher
exited rc=1 before its model execution surface; strict launch-signature
processes 0 before and 0 after; no model/provider call. Accepted
resolution: `SOL_FIXED_OUTPUT_FUTURE_EXECUTION_BLOCKER_RESOLVED` —
dedicated root `$qroot/private/sol-attempts`; internally generated fresh
attempt identity; no arbitrary environment/operator output override;
attempt output must not pre-exist; exclusive fail-closed creation; mode
0700; exact realpath containment; root/attempt symlink rejection; collision
rejection; escape rejection; prior attempts do not block future attempts;
failed attempts may remain frozen without blocking later attempts;
historical `private/sol` never cleared/moved/reused; validator and future
attempt-sealer target exactly the fresh attempt output; launcher
hard-blocked unless a separate future Control Room execution authority
sets the explicit execution-authorized condition. DEV-1 acceptance:
`SOL_CLAUDE_DEPENDENCY_RECONCILIATED` — the frozen Sol branch carried an
unconditional mutable-host Claude executable pin although Claude was not
part of the Sol execution surface; the accepted successor has no Claude
executable digest dependency on the Sol path, mounts no Claude binary,
executes no Claude binary, provides no Claude command path, and preserves
all Sol-consumed executable and frozen-input pins; the exact removed pin
set is only
`4ae40dd1784e85753e742e09f267d29ecbb82890361ad3817d27560866d364a6`; the
observed current host NVM Claude digest during remediation
`26d020351e8112f4006790f3cfce43b4c9df0c1bb1d0e542364d64151b81d5ba` is
historical metadata only and NOT a new Sol dependency. DEV-2 acceptance:
`SOL_LIVE_SUBSCRIPTION_AUTH_SOURCE_CONTRACT_ACCEPTED` — sole eligible
future auth source `/home/isa/.codex/auth.json`; bind-time contract:
requested path exact, resolved realpath exact, regular file, not symlink,
owner/mode metadata recorded, group/other-writable rejected,
audit/bootstrap/runtime-auth/historical-output/package locations rejected,
stale bootstrap copy explicitly ineligible, no alternate source, no
fallback, no automatic login, no automatic refresh, auth contents never
inspected/printed/hashed/fingerprinted/copied/archived, exact live file
read-only bound into the isolated Sol environment only; preserved
`FUTURE_SOL_EXECUTION_MUST_REVERIFY_LIVE_SUBSCRIPTION_AUTH_SOURCE_AT_BIND_TIME`;
Stage-1 did NOT execute `codex login status`; any future separately
authorized execution must perform the readiness decision required by its
future execution authority — this record does not authorize that access.
Frozen Codex/model identity preserved: payload SHA-256
`56ef98ab4032d317ab26e9b5e5a175650717351edb16ed9cde0cb6d1734d62da`;
observed CLI `codex-cli 0.153.4`; future required model `gpt-5.6-sol`;
future required reasoning `xhigh`; no fallback/reroute accepted; no model
invoked during Stage-1. Blindness acceptance:
`AUDITOR_B_BLIND_VIEW_SUCCESSOR_ACCEPTED` — the authoritative BV phase
mechanically established the successor sandbox denial/visibility contract
(common input readable/unwritable; own fresh output writable; peer output
denied; host repository denied; Claude skill denied; Claude credential
path denied; Codex history denied; `.bashrc` denied; `.ssh` denied; entire
bootstrap root denied; historical `private/opus` denied; historical
`private/sol` denied; execution-addenda host path denied; alternate
symlink escape denied; evidence-MCP credential/traversal denial; exact
`/audit/input`, `/audit/meta`, `/audit/output` surface; ephemeral auditor
home; read-only Codex auth bind; no Claude mount); barrier remains CLOSED.
Authoritative matrix: final run `validation-20260909T123406Z`,
OVERALL=PASS — EB 42/42 PASS; OF 33/33 PASS; C1 30/30 PASS; AU 26/26
PASS; BV 31/31 PASS; NP 19/19 PASS; frontier/accounting
`sol_model_calls=0`, `claude_calls=0`, `provider_requests=0`,
`credential_material_archived=0`, `historical_substantive_read=0`,
`frontier_calls=0`; all intermediate runs preserved unrewritten
(`validation-20260909T123015Z` FAIL OF crash; `validation-20260909T123052Z`
FAIL OF 31 PASS / 2 FAIL; `validation-20260909T123132Z` FAIL C1;
`validation-20260909T123216Z` FAIL AU; `validation-20260909T123249Z` FAIL
NP; `validation-20260909T123327Z` PASS but intermediate with package bytes
later changed; `validation-20260909T123406Z` authoritative final PASS).
Historical first-B invariance preserved at the original path:
`private/sol/first-pass.md` SHA-256
`29266fadac540bbf7156dc5aafa0d53ba33f69e60aeaa2ac34b9c5871d918f6e`, 1088
bytes, mode 0444 — byte/mode invariant, HASH-ONLY, UNREAD, never moved,
never replaced; `private/sol/events.jsonl` SHA-256
`12cb40d36c4227e351f42c7d20999ca87f8e6fb8e94d6dd3d55bb7a5c8cd1a7b`, 2497
bytes, mode 0444; Auditor-A substantive artifacts remain UNREAD and
unchanged. Frozen bootstrap identities preserved: candidate
`8ae33444f349ce73c1359b963722e2d16acba630`; baseline
`68ce12acc6c614d1876b902e6511d21f95b33c43:skill`; qualification contract
`3d7168ba3768485a16df0d2fcb266b6962b4657d2d30eaf1bc97f237a9d17bbf`; common
manifest
`14cd8b3b06dfd8edf679486d955c40f8e0096345e33c669bb9f279aed8b09ad8`;
first-pass output contract
`3b787c0689a718e5194042972ad97e26bf5b51481560706b5bc887122d1f2c3a`; Sol
bundle
`162c5bcc3e4f8b98534df6210306090d4ad7bc2ee1aa2a70f5dae74d4ed0099c`; frozen
Sol prompt
`8b8f8e3954631759fa0fd41747ce0b52669c920869fde16f799e681b91c617b6`; frozen
structural validator
`23d9b03fcbf15e2893a911999a0f39b5d625f2f9541392f3c63624b94af69d57`;
evidence MCP
`ee80e465818117587b14974de8541394fd5d5f9c49c683ec2fa28b31b804a520`; Codex
bootstrap config
`d1e5c4654a5502667aa7438456e82ea830d016d3e919bb3859408398f8caf55a`.
OUTPUT-CONTRACT EVIDENCE PRECISION recorded exactly:
`OUTPUT_CONTRACT_DIRECT_EB_ASSERTION_ABSENT_STAGE1_ARCHIVE` — Stage-1 EB
did NOT contain a separately named direct assertion for the exact
`FIRST-PASS-OUTPUT-CONTRACT.md` digest; Stage-1 did NOT independently
renew or re-attest that identity; the exact frozen output-contract identity
remains inherited from previously accepted bootstrap evidence
`3b787c0689a718e5194042972ad97e26bf5b51481560706b5bc887122d1f2c3a`; Stage-1
was not authorized to modify that contract and no structural-output
remediation occurred; Control Room treats this as an evidence-precision
gap, NOT an execution-boundary behavioral failure; before any Stage-2
structural-output remediation may be mechanically accepted, Stage-2 MUST
directly and explicitly hash the exact frozen
`FIRST-PASS-OUTPUT-CONTRACT.md`, require the exact digest above, include
that assertion in its deterministic identity phase, include that identity
in its prelaunch/seal integrity gate as appropriate, and return direct
evidence of the check — recorded as
`STAGE2_MUST_DIRECTLY_REASSERT_OUTPUT_CONTRACT_IDENTITY`. Known nonblocking
gate warning recorded:
`KNOWN_NONBLOCKING_GNU_GREP_ESCAPED_SLASH_WARNING` — the sealed prelaunch
gate's ADDENDUM directory-membership check may emit a GNU grep warning
caused by escaped `/` characters in an ERE; Control Room independently
inspected the code; the warning does NOT change the membership predicate
outcome and does not weaken the separate exact manifest/file-set checks; no
reseal or mutation of Stage-1 is performed to remove this cosmetic warning;
a later authorized successor may remove it only if that change is
explicitly accounted for. Structural failure remains intentionally
unresolved: `CONTRACT_DIGEST_FIELD_NOT_EXACT` — Stage-1 did NOT remediate
it; no conforming Auditor-B first pass exists; Stage-2 remains a separate
future Control Room decision. Authority state after this record: Auditor-A
SEVENTH accepted conforming first pass unchanged; FIRST Auditor-B authority
CONSUMED/CLOSED with its first pass NONCONFORMING; second Auditor-B
authority NONE; no automatic retry; barrier CLOSED; cross-examination
authority NONE; adjudication authority NONE; qualification NONE;
AUCDEV-010 OPEN; installed qualification provenance remains `PENDING
EVIDENCE RECONCILIATION`; mechanical acceptance of `sol-v1-execbound`
creates NO model execution authority. Disposition:
`SOL_EXECBOUND_SUCCESSOR_POSTACCEPTANCE_GOVERNANCE_RECORD_PREPARED / OUTPUT_CONTRACT_PRECISION_GAP_RECORDED / STAGE2_DIRECT_REASSERTION_REQUIRED / BARRIER_CLOSED / QUALIFICATION_NONE`.

2026-09-09 — AUCDEV-010 Stage-2 Sol contract-digest structural-output
successor post-acceptance governance record (record-only; canonical base
`b2ccf8d52bd956f03c87c8683868fbddb44fdf50` exact at start and close; no
commit/push by the preparation pass). Control Room mechanically accepted
the sealed Stage-2 successor package
`execution-addenda/sol-v1-execbound-contractdigest/` — seal SHA-256
`31f8bf68cc9d5da1bf8be6b3a86a552ab2c1f38e4d347157e547b09e4e8395df`,
trusted manifest 206 records verified 206/206 PASS (0 missing, 0
mismatched, 0 extra trusted regular files); remediation evidence archive
`aucdev-010-sol-contractdigest-remediation-evidence-20260909.tar.gz`
SHA-256 `74cb245a8c396d8f9d41d4c3c1c88ffe8a675cfb6be49a492141d4cd84da68ae`,
448451 bytes — Control-Room independent verification: 251 members, 234
regular files, 17 directories, no traversal, no symlink/hardlink/special
members, outer SHA256SUMS 233/233 with complete coverage excluding itself,
nested trusted manifest 206/206 with manifest digest equal to the successor
seal, outer/nested anchors agreeing, independent secret-shaped scan clean.
Disposition:
`SOL_CONTRACT_DIGEST_STRUCTURAL_SUCCESSOR_MECHANICALLY_ACCEPTED_WITH_EVIDENCE_PRECISION_RESIDUALS`
/ `FRONTIER_NOT_AUTHORIZED` — bounded structural mechanics accepted,
structural remediation evidence sufficient for governance recording,
Stage-1 output-contract direct-identity gap mechanically closed by Stage-2
evidence; NOT a conforming Auditor-B first pass, NOT a second Auditor-B
authority, NOT Sol execution permission, NOT a future-compliance guarantee,
NOT barrier-opening, cross-examination, or adjudication authority, NOT
qualification, NOT installation authority. The Stage-1 predecessor
`execution-addenda/sol-v1-execbound/` (seal
`76ee6a5158792215bcda8f9cd3e845f02570012b0205844032d48ae88ff66ecc`,
139/139 PASS) is preserved unmodified with its accepted records
(`SOL_FIXED_OUTPUT_FUTURE_EXECUTION_BLOCKER_RESOLVED`,
`SOL_CLAUDE_DEPENDENCY_RECONCILED`,
`SOL_LIVE_SUBSCRIPTION_AUTH_SOURCE_CONTRACT_ACCEPTED`,
`AUDITOR_B_BLIND_VIEW_SUCCESSOR_ACCEPTED`,
`FUTURE_SOL_EXECUTION_MUST_REVERIFY_LIVE_SUBSCRIPTION_AUTH_SOURCE_AT_BIND_TIME`,
`KNOWN_NONBLOCKING_GNU_GREP_ESCAPED_SLASH_WARNING`). Direct output-contract
reassertion: exactly one frozen common-input FIRST-PASS-OUTPUT-CONTRACT.md
candidate resolved; direct SHA-256 of
`views/sol/input/common/FIRST-PASS-OUTPUT-CONTRACT.md` =
`3b787c0689a718e5194042972ad97e26bf5b51481560706b5bc887122d1f2c3a`;
`STAGE2_MUST_DIRECTLY_REASSERT_OUTPUT_CONTRACT_IDENTITY = SATISFIED`;
`OUTPUT_CONTRACT_DIRECT_EB_ASSERTION_ABSENT_STAGE1_ARCHIVE = CLOSED BY
DIRECT STAGE-2 MECHANICAL EVIDENCE`; that digest is the frozen FILE
identity and is NOT the validator-required model-output Contract digest
value. Mechanically derived model-output field (from frozen
validator/instruction mechanics; historical Auditor-B substantive artifact
never read): label `Contract digest`; expected value
`3d7168ba3768485a16df0d2fcb266b6962b4657d2d30eaf1bc97f237a9d17bbf`;
identity: qualification-contract digest / `qualification_digests`
`contract_sha256`. Synthetic RED: wrong value → frozen validator rc=1
`INVALID_FIRST_PASS: Contract digest field is not exact`
(`SOL_CONTRACT_DIGEST_STRUCTURAL_BLOCKER_REPRODUCED`); synthetic
exact-value GREEN: rc=0 `STRUCTURAL_OUTPUT_CONTRACT_PASS` — GREEN proves
validator semantics only, NOT future GPT-5.6 Sol compliance. Accepted
design: frozen Sol first-pass prompt, frozen output contract, frozen
structural validator preserved byte-for-byte; structure-only trailer
`SOL-FIRST-PASS-STRUCTURE-TRAILER.md` (SHA-256
`f9efcc71a34db939046515b82fc10f8b744816a8b7fca783d3953d37ef1884c5`)
composed deterministically after the unchanged frozen prompt with the
exact label/value guidance explicit; no Auditor-A substance; no historical
Auditor-B substance; no findings/hypotheses/verdicts inserted; no
model-output post-processing; no automatic repair; the frozen validator
remains the final structural conformance/sealing gate; Stage-1
execution-boundary behavior preserved. Authoritative final matrix
`validation-20260909T164016Z` OVERALL=PASS (ID 56/56, CD 37/37, PC 20/20,
OF 33/33, C1 30/30, AU 26/26, BV 32/32, NP 19/19; frontier_calls=0); the
six failed/intermediate runs (validation-20260909T163441Z, 163552Z,
163655Z, 163734Z, 163804Z, 163847Z) are preserved unrewritten historical
evidence. Zero-activity accounting for the accepted task:
sol_model_calls=0, claude_calls=0, provider_requests=0, frontier_calls=0,
codex_login_status=0, historical_substantive_read=0,
credential_material_archived=0. THREE Control-Room evidence-precision
residuals recorded as governance truth (sealed Stage-2 record preserved
unchanged; no mutation, no reseal): R1
`SEALED_REMEDIATION_RECORD_DIFF_ACCOUNTING_TEXT_INCONSISTENCY`
(evidence/reporting precision defect; non-behavioral; non-blocking for
mechanical acceptance) — the sealed CONTRACTDIGEST-REMEDIATION-RECORD.md
§5 incorrectly places tests/test_fresh_output.py,
tests/test_claude_dependency.py, tests/test_auth_source.py, and
tests/test_no_frontier.py under byte-identical carries; the byte-identical
carries are exactly auth/AUTH-SOURCE-CONTRACT.md and
launcher/seal-attempt-first-pass-v1e.sh; test_fresh_output.py,
test_auth_source.py, and test_no_frontier.py changed by successor package
path identity only; test_claude_dependency.py changed by package path
identity PLUS deterministic Stage-2 test changes permitting/asserting the
authorized structural-trailer read-only mount and exact trailer digest
pin; test_blind_view.py changed by package path identity PLUS
deterministic Stage-2 trailer visibility verification; the external
06-DIFF-ACCOUNTING-AND-MATRIX-INDEX.txt, machine diff artifacts, and final
matrix provide the correct reconcilable changed-byte evidence; R2
`REAL_AUTH_METADATA_PROBE_REPORTING_PRECISION` (implementation/reporting
precision deviation; no credential-content exposure observed; non-blocking)
— synthetic auth fixtures covered the adversarial AU cases while the real
eligible path `/home/isa/.codex/auth.json` also received metadata-only
path/readiness checks (file/path/stat properties), was read-only bound for
blind-view readability and write-denial verification, and evidence-MCP
credential-content access attempts were expected to be denied; precise
accounting: credential_content_read=0, credential_material_archived=0,
real_auth_metadata_probe=OCCURRED, real_auth_read_only_bind_probe=OCCURRED
(correcting the implementer's overbroad "synthetic fixtures only"); R3
`FINAL_IMPLEMENTATION_REPORT_ARCHIVE_COMPLETENESS_GAP` (evidence-package
completeness limitation; non-behavioral; non-blocking) — the remediation
archive does not contain a standalone copy of the 57-item REQUIRED FINAL
RETURN provided to Control Room; the original archive remains immutable
historical evidence; this governance record includes its own complete
record/report. Historical Auditor-B identity preserved hash/stat-only
(`29266fadac540bbf7156dc5aafa0d53ba33f69e60aeaa2ac34b9c5871d918f6e`, 1088
bytes, 0444; events
`12cb40d36c4227e351f42c7d20999ca87f8e6fb8e94d6dd3d55bb7a5c8cd1a7b`, 2497
bytes, 0444; substantive content never read, grep'd, parsed, diffed,
quoted, copied, relocated, or repaired; Auditor-A substantive artifacts
remain unread, metadata/hash/stat only). Authority state after this record:
Auditor-A SEVENTH accepted conforming first pass unchanged; FIRST
Auditor-B authority CONSUMED/CLOSED with its first pass
NONCONFORMING_AUDITOR_B_FIRST_PASS (`CONTRACT_DIGEST_FIELD_NOT_EXACT`
unchanged); second Auditor-B authority NONE; automatic retry NONE; barrier
CLOSED; cross-examination NONE; adjudication NONE; qualification NONE;
AUCDEV-010 OPEN; installed qualification provenance remains `PENDING
EVIDENCE RECONCILIATION`; the Stage-2 mechanical acceptance creates NO
model execution authority; a future second Auditor-B first-pass authority
can only be considered by a separate Control Room decision AFTER this
governance record is independently verified and canonically published.
Disposition: `SOL_CONTRACTDIGEST_SUCCESSOR_POSTACCEPTANCE_GOVERNANCE_RECORD_PREPARED_WITH_EVIDENCE_PRECISION_RESIDUALS / BARRIER_CLOSED / QUALIFICATION_NONE`.

- Milestone: before the next candidate audit; verified historical evidence may close
  the item without rerunning qualification. A new summary alone is not proof.

### AUCDEV-011 — Targeted re-audit compiler

- Priority/status: P2 / OPEN.
- Problem/evidence: bounded in-run adjudication exists; a new-candidate re-audit scope
  compiler from remediation changes does not. Manual procedure now exists in the runbook.
- Why it matters: narrow fixes should not automatically trigger broad expensive audits.
- Scope: derive scope from prior findings, held invariants, remediation diff and changed
  trust boundaries; start with a reviewable brief/template before coding automation.
- Non-goals: transfer old verdict to new SHA; skip fresh release gates; autonomous lifecycle.
- Dependencies: several manual cycles and stable AUCDEV-004 semantics.
- Acceptance: scope includes changed boundaries and previously failed invariants; excluded
  areas have rationale; every new target gets a new run and independently reached verdict.
- Validation: replay manual planning against narrow-fix and trust-boundary-expansion examples.
- References: `skill/protocols/adjudication.md`, `AUCDEV-CONTROL-ROOM-RUNBOOK.md`,
  `AUCDEV-PROJECT-UPDATE-PROTOCOL.md`.
- Milestone: after measured manual cycles.

### AUCDEV-012 — Public-contract and operator usability simplification

- Priority/status: P2 / READY.
- Problem/evidence: public prose promises writes only in run dir while prepare/registry/
  archive write managed roots; read-confinement language can imply other in-target runs
  are masked although the whole target is bound. Nine binding reasons coexist with a
  SANDBOX_PREFLIGHT diagnostic. Skill README omits states in its first table.
- Why it matters: prompt authors need one accurate surface with clear enforcement limits.
- Scope: reconcile human contract, describe/schema, README examples, paths, and capability
  claims; distinguish environment binding reasons from sandbox-preflight diagnostics.
- Non-goals: duplicate root contract, hide residuals, change runtime to satisfy marketing,
  treat protocol 2.0 as package v2.0.1.
- Dependencies: AUCDEV-004/009 semantics; coordinate AUCDEV-007 cap descriptions.
- Acceptance: complete state table; accurate lifecycle write locations and bind set;
  runnable copy/paste examples; version and enforcement classifications consistent.
- Validation: public-contract drift tests plus explicit semantic/doc example review
  (existing enum/list tests alone do not cover these prose contradictions).
- References: `skill/README.md`, `skill/PUBLIC-CONTRACT.md`,
  `skill/scripts/audit_council.py:PUBLIC_CONTRACT`, `skill/schemas/public-contract.schema.json`,
  `skill/tests/test_public_contract.py`, `docs/A0-CODEX-CONFINEMENT.md`.
- Milestone: v2.0.2 docs/product review.

### AUCDEV-013 — Resolve layout-default API divergence

- Priority/status: P2 / READY.
- Problem/evidence: `artifact_layout._default_ephemeral_worktrees` uses XDG_CACHE,
  `environment_manager.env_root` uses XDG_DATA. Production creation uses the latter;
  injected tests align them but do not erase the separate API defaults.
- Why it matters: future consumers could discover/manage a different root from creation.
- Scope: choose/document one default contract or explicitly distinct resolver semantics;
  verify no un-injected consumer selects the wrong location.
- Non-goals: migrate/delete historical directories or change retention automatically.
- Dependencies: inventory current callers; operator approval only if relocation is proposed.
- Acceptance: APIs and docs have an unambiguous contract; uninjected default tests prove it;
  existing roots/history remain untouched.
- Validation: environment/layout unit tests with overrides absent and present, plus prepare lifecycle.
- References: `skill/scripts/artifact_layout.py`, `skill/scripts/environment_manager.py`,
  `skill/tests/test_artifact_layout.py`, `MIGRATION-RETENTION-RECOMMENDATION.md`.
- Milestone: v2.0.2 candidate.

### AUCDEV-014 — Owner license decision

- Priority/status: P2 / BLOCKED (owner license choice absent).
- Problem/evidence: no LICENSE file or governing grant exists in the tracked tree/history.
- Why it matters: public visibility alone does not specify a reuse/distribution license.
- Scope: owner chooses license or deliberately retains no grant; document that decision.
- Non-goals: choose a license on the owner's behalf or introduce community governance.
- Dependencies: explicit owner decision.
- Acceptance: README and any LICENSE accurately match the decision; attribution reviewed.
- Validation: inspect final text and repository metadata; no tests necessary.
- References: `README.md`, `CONTRIBUTING.md`.
- Milestone: repository governance.

### AUCDEV-015 — Portable historical smoke-fixture provenance

- Priority/status: P2 / OPEN.
- Problem/evidence: `smoke-fixture` and `smoke-fixture-103` are gitlinks with no
  .gitmodules. Clones preserve pointer SHAs but cannot initialize these local fixture repos.
  Their untracked audit outputs are private/local-only and not part of a parent push.
- Why it matters: public readers cannot reconstruct these historical smoke runs directly.
- Scope: document pointer provenance and decide a sanitized deterministic replacement or
  explicitly authorized fixture publication; keep historical objects intact.
- Non-goals: recursively stage local outputs, add guessed submodule URLs, rewrite history.
- Dependencies: public-safety review of any future fixture material.
- Acceptance: historical evidence pointers remain documented; ordinary clone/testing works;
  any future reproducibility fixture is self-contained and public-safe.
- Validation: ordinary clean clone, deterministic fixture setup, archive-content review.
- References: `SMOKE_TEST_RECORD.md`, `skill/tests/fixtures/tiny_repo_setup.sh`,
  `docs/REPOSITORY-DOCUMENTATION-MAP.md`.
- Milestone: repository hygiene.

### AUCDEV-016 — Budgeted real-model seeded evaluation

- Priority/status: P2 / BLOCKED (separate inference budget and qualified auditor required).
- Problem/evidence: fake-model Tier 2 passes do not measure model recall/precision;
  real-model Tier 2 has not run in the recorded evidence.
- Why it matters: release capability and effort-mode choices need measured model behavior.
- Scope: pre-register a small budgeted fixture subset, protected negatives, truth access,
  actual model versions, stopping conditions and comparison metrics.
- Non-goals: rerun benchmarks implicitly, infer quality from model agreement or fake scores.
- Dependencies: AUCDEV-010; secrecy/visibility checks; explicit inference budget.
- Acceptance: sealed truth never enters auditor context; costs and unknown usage are honest;
  novel findings require independent evidence; results include false positives/omissions.
- Validation: deterministic harness first, then only authorized bounded real calls.
  The fake Codex fixture does not implement provider-side strict-schema enforcement;
  retain schema/adapter assertions and distinguish them from provider acceptance.
- References: `skill/eval/tier2_fixtures.py`, `skill/eval/tier2_scoring.py`,
  `skill/eval/scoring.py`, `AUDIT-COUNCIL-V2-EVAL-REPORT.md`.
- Milestone: after qualification provenance, before capability/efficiency claims.

### AUCDEV-017 — EvidenceStore lifecycle integration

- Priority/status: P2 / OPEN.
- Problem/evidence: EvidenceStore and its visibility/freshness checks are implemented
  and tested, but scripts/hooks/eval have no production stage consumer of the class.
- Why it matters: an available library is not proof that all audit evidence follows it.
- Scope: map real stage evidence creation/lookup and integrate the minimal useful path
  with lifecycle-owned barrier identity, references and access records.
- Non-goals: cross-run global cache, cache findings/opinions, bypass FRESH_REQUIRED,
  expose ground truth or install a database service.
- Dependencies: AUCDEV-001/002/004 contracts; assess AUCDEV-007 measurements.
- Acceptance: real stage flow exercises producer/consumer/freshness policy; provenance
  survives report generation; optional unmigrated evidence is identified honestly.
- Validation: deterministic real-pipeline consumer tests including denied lookup,
  changed binding/tool/input digest, barrier failure, and fresh-release requirements.
- References: `skill/scripts/evidence_store.py`, `skill/tests/test_evidence_store.py`,
  `skill/schemas/evidence-record.schema.json`, `skill/SKILL.md` evidence-efficiency guidance.
- Milestone: after isolation/ingress contracts.

### AUCDEV-018 — Dirty-target byte-level freshness coverage

- Priority/status: P1 / READY.
- Problem/evidence: repo_fingerprint captures index blob IDs and dirty-path presence,
  not changed worktree bytes; untracked entries use name/size. A second edit to an
  already-dirty tracked file or equal-size untracked content can leave the compared
  fields unchanged. Existing dirty-tree test only proves non-mutation on capture.
- Why it matters: CURRENT permits dirty targets, so a frozen fingerprint can miss
  changes even when HEAD stays the same. Clean RELEASE confinement reduces exposure
  but does not establish correctness for all supported targets.
- Scope: define and bind exact audited bytes for dirty/untracked target content;
  review ignored-file and nested-directory exclusions and write-guard reuse.
- Non-goals: reset user changes, hash unrestricted host files, weaken exclusions, or
  claim a reproduced whole-audit exploit from this source-level gap alone.
- Dependencies: AUCDEV-004 completeness claims; environment binding remains intact.
- Acceptance: changes to already-dirty tracked bytes and equal-size untracked bytes
  are detected; dirty capture itself remains read-only; exclusions are explicit;
  target changes produce STALE_REPOSITORY consistently in verify and write guard.
- Validation: temporary repository regressions for same-status tracked edits,
  same-size untracked edits, nested untracked files, ignored policy, and clean controls.
- References: `skill/scripts/repo_fingerprint.py:capture`,
  `skill/scripts/repo_fingerprint.py:diff_fingerprints`,
  `skill/tests/test_repo_fingerprint.py:test_dirty_tree_preserved_no_git_mutations`,
  `skill/tests/test_source_write_guard.py`, `IMPLEMENTATION_REPORT.md` Known limitations.
- Milestone: v2.0.2 candidate; validate before changing fingerprint semantics.

### AUCDEV-019 — Bounded file-resource cleanup

- Priority/status: P2 / OPEN.
- Problem/evidence: the 574-test run passed but emitted ResourceWarnings for unclosed
  files in tests and `codex_runner.py` exit-code reading. No failed test or production
  descriptor-exhaustion incident is established.
- Why it matters: resource warnings obscure useful diagnostics and weaken ownership clarity.
- Scope: context managers for demonstrated unclosed files; verify subprocess/file ownership.
- Non-goals: broad refactoring, changing lifecycle semantics, treating warnings as release failure.
- Dependencies: none; schedule after correctness work.
- Acceptance: named warnings are removed without suppressing them globally or changing results.
- Validation: relevant warning-emitting tests with ResourceWarning visible; full suite once integrated.
- References: `skill/scripts/codex_runner.py`, `skill/tests/test_codex_runner_mock.py`,
  `skill/tests/test_wait_lifecycle_v102.py`, `AUDIT-COUNCIL-V2-EVAL-REPORT.md` current addendum.
- Milestone: next maintenance cycle.

## Deferred / future

### AUCDEV-020 — Fully Autonomous Development Audit Lifecycle

- Priority/status: P2 / DEFERRED.
- Problem/evidence: no active full development/remediation harness exists; the operator
  explicitly chooses a ChatGPT human-in-the-loop control room first.
- Why it matters: automation should address measured repetitive costs, not hypothetical ones.
- Scope: future assessment after several real cycles; identify a small automatable bottleneck.
- Non-goals: large autonomous coding harness now; candidate self-qualification.
- Dependencies: manual-cycle measurements, stable bootstrap and human escalation policy.
- Acceptance: a future proposal quantifies benefit, authority limits, failure recovery,
  independent audit boundaries and operator stop controls before implementation approval.
- Validation: compare proposal against recorded manual cycles; no implementation now.
- References: `AUCDEV-CONTROL-ROOM-RUNBOOK.md`, `AUCDEV-PROJECT-UPDATE-PROTOCOL.md`.
- Milestone: FUTURE, unscheduled.

### AUCDEV-021 — Cross-run evidence reuse and optional retention migration

- Priority/status: P2 / DEFERRED.
- Problem/evidence: EvidenceStore is per-run; retention/layout proposal deliberately did
  not reorganize old archives. No measured storage/reuse need justifies migration yet.
- Why it matters: future reuse must preserve freshness, authorization and sealed truth.
- Scope: future cache/retention design only if measurements warrant it.
- Non-goals: move/delete history, reuse findings, skip fresh release checks.
- Dependencies: AUCDEV-017; explicit authority for any actual archive relocation.
- Acceptance: proposal specifies provenance, invalidation, access policy and recoverable
  migration, with originals retained until explicitly authorized otherwise.
- Validation: copied synthetic archives and stale-cache rejection; no historical mutation.
- References: `MIGRATION-RETENTION-RECOMMENDATION.md`, `skill/scripts/evidence_store.py`.
- Milestone: FUTURE, unscheduled.

### AUCDEV-022 — Eval-proven specialist enablement

- Priority/status: P2 / DEFERRED.
- Problem/evidence: specialist machinery exists but has zero core lifecycle imports and
  is default-off; context scrubbing and activation timestamps are heuristic.
- Why it matters: extra reviewers must improve outcomes enough to justify overhead/risk.
- Scope: future grounding/blindness checks, bounded activation, measured comparative eval.
- Non-goals: enable specialists now; smuggle first-pass findings or let specialists decide GO.
- Dependencies: AUCDEV-001/007/016; explicit benefit evidence.
- Acceptance: pre-frozen activation, caps, credible blindness and grounding; measured net
  value before default policy changes.
- Validation: adversarial renamed-key/backdated-context tests and budgeted comparative eval.
- References: `skill/scripts/specialists.py`, `skill/tests/test_specialists.py`,
  `skill/schemas/specialist-review.schema.json`, KNOWN-LIMITATIONS item 18.
- Milestone: FUTURE, unscheduled.

## Accepted residual register

These entries carry forward documented boundaries; this governance task does not
newly authorize broader risk. Each has owner review on its trigger.

| ID / priority / status | Problem/evidence and why it matters | Scope / non-goals | Dependencies / acceptance and revisit trigger | Validation / reference / milestone |
|---|---|---|---|---|
| AUCDEV-R01 — Lexical/TOCTOU boundary / P2 / ACCEPTED_RESIDUAL | Claude lexical scanning misses encoded/dynamic/shell-local paths and scan-to-exec TOCTOU; it is not an OS sandbox | Disclose current boundary; no ever-expanding parser arms race | Trusted harness plus write guards; revisit on reachable exploit or FORENSIC threat model | Existing adversarial path tests and new exploit repro if observed; `skill/scripts/path_guard.py`, KNOWN-LIMITATIONS 1–3,10; ongoing |
| AUCDEV-R02 — Unkeyed integrity / P2 / ACCEPTED_RESIDUAL | Plain SHA-256 integrity can be forged by an actor rewriting the entire ledger | Tamper-evident chain; no signing/key service now | Trusted host/registry; revisit if hostile run writers enter supported model | Checksum/binding tamper tests; `skill/scripts/state_store.py`, KNOWN-LIMITATIONS 4; ongoing |
| AUCDEV-R03 — Authentication mount / P2 / ACCEPTED_RESIDUAL | Read-write ~/.codex exposes own auth/session state inside bind set | Disclose auth boundary; never publish or inspect auth contents | Subscription login and explicit resume; revisit if narrower supported auth transport exists | Wrapper bind review; `skill/scripts/codex_sandbox.py`, KNOWN-LIMITATIONS 8; ongoing |
| AUCDEV-R04 — System and inactive-wrapper exposure / P2 / ACCEPTED_RESIDUAL | System directories remain readable; missing/disabled bwrap removes extra read confinement | Report actual sandbox.active; no claim of full host/peer isolation | Required toolchain/network; revisit for a supported platform or stronger effort policy | Wrapper/inactive-mode tests; `docs/A0-CODEX-CONFINEMENT.md`, KNOWN-LIMITATIONS 9; ongoing |
| AUCDEV-R05 — Usage and classification limits / P2 / ACCEPTED_RESIDUAL | Claude usage/per-phase effort control unavailable; quota percentage non-linear; unfamiliar Codex JSONL degrades telemetry and novel failure text conservatively becomes FAILED | Null usage and guidance only; no fabricated accounting | Host/API format capability; revisit when metrics become exposed or a real misclassification appears | Metrics unknown-value and failure-classification tests; `skill/scripts/codex_runner.py`, `skill/SKILL.md`, KNOWN-LIMITATIONS 14; ongoing |
| AUCDEV-R06 — Heuristic evidence guards / P2 / ACCEPTED_RESIDUAL | Finding-shape detection and specialist context scrubbing use markers/regex | Anti-accident defenses; no universal semantic leak detector; specialists stay off | Trusted caller; revisit with AUCDEV-001/017/022 | Renamed-key/string tests when activated; `skill/scripts/evidence_store.py`, `skill/scripts/specialists.py`, KNOWN-LIMITATIONS 17–18; ongoing |
| AUCDEV-R07 — Host-deleted registry entries / P2 / ACCEPTED_RESIDUAL | Host deletion can leave a dead registry entry until next registration, failing closed | Preserve deny behavior; no automatic destructive cache sweep | Existing registration GC; revisit on real operator disruption | Dead-entry and cache-isolation tests; `skill/scripts/path_guard.py`, `skill/tests/test_review_hardening.py`, KNOWN-LIMITATIONS 6; ongoing |
| AUCDEV-R08 — Shallow instruction inventory / P2 / ACCEPTED_RESIDUAL | Instruction-file discovery is root/first-level only; harmless dead return pair retained | Document shallow inventory; no unrelated cleanup | Revisit if deep instruction census is required by audit scope; do not infer deep coverage | Fingerprint/source inspection; `skill/scripts/repo_fingerprint.py`, `skill/scripts/audit_council.py`, KNOWN-LIMITATIONS 20; ongoing |

## Evidenced closures — do not reopen as missing features

### AUCDEV-D01 — v2 binding and explicit phase integrity

- Priority/status: P1 / DONE (implementation, not independent release certification).
- Problem/evidence: v1 brief/root mismatch and implicit skip gaps were implemented in
  env_binding, state, advance/resume; source and named regression tests exist.
- Why it matters: target identity and explicit omissions underpin all later claims.
- Scope/non-goals: recognize implemented binding/skip gates; do not close AUCDEV-004.
- Dependencies: none for historical disposition.
- Acceptance: source capture/verify/pinning and skip rejection implemented.
- Validation/references: `skill/tests/test_env_binding.py`, `skill/tests/test_env_lifecycle.py`,
  `skill/tests/test_review_hardening.py`, implementation report rounds 1–6.
- Milestone: v2.0 implementation history.

### AUCDEV-D02 — Typed ranges, terminal telemetry and fake scoring

- Priority/status: P1 / DONE (bounded implemented contracts).
- Problem/evidence: v1 multi-range output/elapsed/attempt gaps have typed schemas,
  in-memory migration, terminal accounting, and fake-model pipeline regressions.
- Why it matters: these known fixes must not be confused with new corpus/governor work.
- Scope/non-goals: closure of named implementation gaps; no real-model quality claim.
- Dependencies: none for historical disposition.
- Acceptance: schemas/adapter/migration and accounting paths exist; fake scoring is wired.
- Validation/references: `skill/tests/test_line_ranges_v2.py`, `skill/tests/test_telemetry_v2.py`,
  `skill/tests/test_tier2_scoring.py`, `AUDIT-COUNCIL-V2-EVAL-REPORT.md`.
- Milestone: v2.0 implementation history; stale evidence-policy prose remains AUCDEV-009.

### AUCDEV-D03 — v2.0.1 da27c0 operational fixes

- Priority/status: P1 / DONE (implementation only).
- Problem/evidence: PATH/node/resolver failures, missing RELEASE staging/skill reads,
  and binding record divergence are fixed in ff3f848 and focused 8ae3344 follow-up.
- Why it matters: later ingress/isolation work must preserve these regressions.
- Scope/non-goals: recognize exact fixes; no claim of independently qualified installation.
- Dependencies: none for historical disposition; qualification remains AUCDEV-010.
- Acceptance: preflight precedes attempt accounting; run-owned RELEASE evidence;
  run-binding linked with preparation provenance; correct mount and toolchain order.
- Validation/references: `skill/tests/test_tier4_da27c0.py` (19 methods),
  `skill/scripts/codex_sandbox.py`, `skill/scripts/audit_council.py`, KNOWN-LIMITATIONS 23.
- Milestone: v2.0.1 source `8ae33444f349ce73c1359b963722e2d16acba630`.

### AUCDEV-D04 — Manual ChatGPT control-room knowledge base

- Priority/status: P2 / DONE (local documentation deliverable; publication separately recorded).
- Problem/evidence: no repository-level README or durable project state/backlog existed.
- Why it matters: the owner can now run bounded development/audit cycles from canonical records.
- Scope/non-goals: curated docs, evidence queue, update/runbook/instructions; no runtime change.
- Dependencies: operator copies settings text; dynamic state/backlog are fetched live;
  only changed durable orientation Sources need refresh per the current manifest.
- Acceptance: seven requested documents exist, paths resolve, current unknowns disclosed,
  candidate self-qualification forbidden, baseline ZIP historical, autonomous lifecycle deferred.
- Validation/references: `PROJECT-SOURCES-MANIFEST.md`, `AUCDEV-PROJECT-UPDATE-PROTOCOL.md`,
  `../REPOSITORY-PUBLICATION-RECORD.md` for actual validation/publication result.
- Milestone: repository governance, 2026-09-05.

## Explicit backlog quality audit

Inspected all tracked source TODO/FIXME markers (none actionable found), the eight
protocols, schemas, scripts/hooks, tests/eval, original contracts/design/plan,
implementation/hardening/smoke/eval/migration reports and all 23 original limitations.
No untracked production archive was imported as a backlog source. Dispositions:

| Evidence family | Disposition |
|---|---|
| Known limitations 1–4, 8–10, 14, 17–18, 20 | Accepted R01–R06/R08; specialist enablement 022 deferred |
| Limitations 5,7,19: automatic hook, wrapper, six review rounds | Historical implemented closure D01; no new feature item |
| Limitation 6: registry GC/cache pollution | Historical fix D01; host-deletion residual R07 |
| Limitations 11–13: fake scoring, replay, historical telemetry | D02 implemented; real-model evidence 016; sanitized corpus 005 |
| Limitation 15: observational attempts | D02 terminal accounting; whole-program scope 007 |
| Limitation 16: API-only visibility/per-run store | 001/017 open; cross-run cache 021 deferred |
| Limitations 21–22: roots/retention | API defaults 013 open; creation route documented; retention 021 deferred |
| Limitation 23: da27c0 fixes | D03 done in source; additional corpus 005; install provenance 010 |
| Production mechanical independence and ingress seeds | 001/002 open, corroborated by current source; run ID unknown |
| Mutation workspace, effort modes, re-audit scope seeds | 003/006/011 open; not implemented by detached targets/adjudication |
| Governor and human escalation seeds | Existing caps recognized; 007/008 cover remaining work |
| Migration proposal old schema-count and record-wiring TODOs | Historical/closed: 13 schemas with builders; cmd_prepare links run record; D01/D03 |
| Historical v1 reports: subprocess resume, exit/zombie, schema-wire, telemetry gaps | Closed in current source/tests; retained history, no duplicate items |
| v1 remaining dirty/untracked fingerprint weakness | AUCDEV-018 open; source confirms missing byte comparison, not silently accepted |
| v1 equal-timestamp metrics ordering and generic telemetry/classification | AUCDEV-007 ordering/accounting; R05 conservative degradation retained |
| v1 fake Codex does not enforce provider wire schema | AUCDEV-016 validation limitation; existing adapter assertions recognized |
| Current deterministic run ResourceWarnings | AUCDEV-019 open, low-impact maintenance; tests passed |
| Original architecture “implementation not begun” and old round/test counts | Historical snapshot labels + documentation map; not runtime TODOs |
| Evidence-policy/failure protocol contradictions, README/contract omissions | 009/012 actionable; left unmodified in executable skill in this task |
| Landlock alternative to bubblewrap | Not actionable now: existing wrapper, no evidenced unmet need; reconsider under 006 |
| Source `from __future__`, test fixture “deferred”, generic domain mentions | Not actionable markers, not backlog work |
| No license and unreconstructable gitlinks | 014/015 open with explicit owner/data boundaries |
| Fully autonomous lifecycle | 020 DEFERRED; no active implementation found |

Reference convention: source paths above are repository-relative; KNOWN-LIMITATIONS
means `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md`. Links to deeper authority are in
[architecture summary](AUCDEV-ARCHITECTURE-SUMMARY.md) and
[documentation map](../REPOSITORY-DOCUMENTATION-MAP.md).
