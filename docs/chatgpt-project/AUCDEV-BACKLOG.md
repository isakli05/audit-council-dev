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
