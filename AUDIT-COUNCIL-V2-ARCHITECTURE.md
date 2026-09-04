# Audit Council v2.0 — Architecture (Phase 0 Reconstruction + Target Design)

Status: **Phase 0 complete** — this document records the reconstructed v1.0.3
architecture, the verified evidence behind every v2 change, and the frozen shared
contracts that all v2 workstreams must implement against. Implementation has not
begun. Companion document: `plans/audit-council-v2.md` (workstream packages,
task decomposition, integration order, budget, rollback).

Authoritative inputs (all inspected 2026-09-04):

| Input | Location | Status |
|---|---|---|
| Original v1 spec | `/home/isa/audit_council_skill_prompt.md` (41 sections) | read |
| v1.0.3 dev source | `/home/isa/audit-council-dev/skill/` | read, verified |
| Installed skill | `~/.claude/skills/audit-council/` | byte-identical to dev source (only `__pycache__` differs) |
| Shared contracts | `/home/isa/audit-council-dev/CONTRACTS.md` | read |
| Hardening reports | `HARDENING_REPORT_v1.0.1/2/3.md`, `IMPLEMENTATION_REPORT.md`, `SMOKE_TEST_RECORD.md` | read |
| Benchmark 001 run | `/home/isa/benchmarks/lco-audit-council-001/.../20260904T014146Z-f3384a` | read-only |
| Fifth audit run | `/home/isa/audits/lco-fifth-independent-release-audit/.../20260904T081903Z-60651d` | read-only |
| v2 program spec | pasted 2026-09-04 (pillars A0/A1/A2/B/C/D/E/F/G/H) | governing |

Environment facts verified this session: Claude Code **2.1.260**, codex-cli
**0.153.0** (login: ChatGPT subscription), git **2.55.0**, Python 3.14 stdlib-only.
Divergence D1 still stands (`codex exec resume` has no `-s`; resume sets
`-c sandbox_mode="read-only"`). `codex exec --help` still exposes
`--sandbox/--output-schema/--json/-C/-c/-m`; note the new-to-us config example
`-c sandbox_permissions=[...]` (A0 research item, see §5.3).

---

## 1. v1.0.3 current-state map (reconstructed)

### 1.1 Components

```
~/.claude/skills/audit-council/            (== /home/isa/audit-council-dev/skill/)
├── SKILL.md                    Opus-session orchestrator (263 lines). Frontmatter:
│                               model claude-opus-5, disable-model-invocation,
│                               allowed Read/Grep/Glob/Bash, disallowed
│                               Edit/Write/NotebookEdit/AskUserQuestion
├── protocols/ (8 files)        audit-contract, evidence-policy, independent-audit,
│                               cross-examination, adjudication, final-synthesis,
│                               severity-policy, failure-and-resume
├── schemas/ (8 JSON Schemas)  audit-contract, finding, independent-audit,
│                               cross-examination, disagreement-ledger,
│                               adjudication, final-findings, state
├── prompts/ (3 templates)     codex-independent, codex-cross-examine-opus,
│                               codex-targeted-adjudication ({{placeholder}} vars)
├── scripts/ (stdlib-only py)  audit_council.py (933), codex_runner.py (986),
│                               state_store.py (391), repo_fingerprint.py (258),
│                               validate_artifact.py (373), wire_adapter.py (253),
│                               render_report.py (488)
└── tests/ (11 files)          160 tests, ~25 s, fake_codex.py fixture
```

The Claude Code session running SKILL.md IS the Opus engine (no nested
`claude -p`). Codex is driven by `codex_runner.py` as a detached subprocess.

### 1.2 Run lifecycle (state machine, state_store.py)

`CREATED → PREFLIGHT_COMPLETE → CONTRACT_FROZEN → OPUS_INDEPENDENT_COMPLETE →
CODEX_INDEPENDENT_COMPLETE → NORMALIZED → OPUS_CROSS_EXAM_COMPLETE →
CODEX_CROSS_EXAM_COMPLETE → LEDGER_COMPLETE → [ADJUDICATION_COMPLETE | recorded
skip] → FINALIZED → COMPLETE`, with honest `completeness_state` (RUNNING,
COMPLETE, COMPLETE_WITH_RESIDUAL_UNCERTAINTY, PARTIAL_CODEX_QUOTA,
PARTIAL_CODEX_FAILURE, PARTIAL_CLAUDE_INTERRUPTION, STALE_REPOSITORY,
INVALID_AUDIT_INPUT). Forward-only; every `advance` schema-validates the phase
artifact, checksums it (checksums.sha256), and refuses backward motion.
Completed phases are immutable. Atomic writes everywhere (tmp → fsync →
os.replace). Artifacts land in the target repo under
`audit-output/audit-council/<run-id>/` (00-manifest … 99-metrics, state.json,
prompts/, logs/, schemas/ run-local wire variants).

### 1.3 Codex pipeline (codex_runner.py)

- `start` enforces the budget governor (≤1 SUCCESSFUL stage per phase, ≤3 total,
  ≤3 attempts/phase, 1 repair/phase), renders the prompt into the run dir,
  builds the strict wire schema via `wire_adapter.canonical_to_wire` (v1.0.3),
  launches detached via a `/bin/sh` wrapper persisting the real exit code
  (zombie-safe), per-job log paths `logs/<phase>.<job_id>.{jsonl,stderr.log,
  final.json}` (no attempt can overwrite another).
- Fresh: `codex exec -C <repo> --model gpt-5.6-sol --sandbox read-only --json
  --output-schema <wire> -c model_reasoning_effort="xhigh" -o <out> -`.
  Resume: `codex exec resume <explicit-id> ... -c sandbox_mode="read-only"`
  (D1). Never `--last`, never bypass/danger flags (hard-refused in argv builder
  + tests).
- `wait` classifies via the wrapper-persisted exit code (primary), then
  stderr/stdout patterns: COMPLETE / FAILED / QUOTA / AUTH_ERROR /
  INVALID_OUTPUT (exit 0 but output missing/unparseable/wire-invalid/
  canonically-invalid/fingerprint-mismatch). On exit 0 the raw output is
  preserved, `wire_adapter.wire_to_canonical` normalizes (schema-aware;
  optional-null→omitted; required-non-nullable-null fails closed), the
  candidate is validated against the ORIGINAL canonical schema (final
  authority), fingerprint-checked against run state, and a `.canonical.json`
  sidecar is written.
- Telemetry (v1.0.3): every terminal attempt persists usage/tokens on its job
  record (null = unknown, never fabricated zero); `rebuild_metrics()` derives
  `99-run-metrics.json` idempotently from `logs/jobs/*.json`.
- `repair` = one-shot schema-repair resume of the SAME thread, same budget stage.

### 1.4 Integrity machinery

- `repo_fingerprint.py`: HEAD sha, branch, porcelain, tracked inventory
  (`ls-files -s`), untracked inventory (name+size), tool versions; structured
  diff; material-change rule excludes only `audit-output/`. `verify-repo`
  before every expensive phase (exit 4 STALE_REPOSITORY). `write-guard` after
  every advance (exit 5 on new mutations outside the run dir; never resets).
- Semantic fingerprint invariant (v1.0.1): canonical artifacts claiming a
  repository fingerprint must equal the frozen run fingerprint
  (INVALID_ARTIFACT on mismatch) — enforced at advance, resume-check, and in
  the runner's output classification.
- Ledger/final invariants (validate_artifact.py): unique cluster/member ids;
  REJECTED only in the rejected appendix; UNRESOLVED CRITICAL/HIGH explicitly
  listed as unresolved risks; late findings require other-model
  `validated_by` or stay UNRESOLVED.

### 1.5 v1 invariants v2 must preserve (from program spec, all verified present)

Opus 5 interactive orchestrator + independent auditor; GPT-5.6 Sol xhigh
independent second auditor via direct `codex exec`; subscription auth only, no
PAYG fallback (preflight fails on ANTHROPIC_API_KEY / OPENAI_API_KEY /
CODEX_API_KEY presence); Codex read-only sandbox; exact thread id persisted and
resumed, never `--last`; first-pass independence; no forced consensus;
REJECTED excluded + unresolved material disagreements explicit; bounded
targeted adjudication (≤1 round, CRITICAL/HIGH DISPUTED/UNRESOLVED only);
successful-stage governor bounded; canonical validation authoritative after
wire normalization; INVALID_OUTPUT ≠ successful stage; raw model output
preserved; fingerprint + write-guard fail-closed; honest quota/auth/crash/
cancel/partial states; unknown usage never fabricated as zero; per-job logs
never overwrite; zombie/exit-code lifecycle hardening; no automatic
push/merge/publish.

---

## 2. Phase 0 evidence — known limitations reproduced deterministically

Reproduction script: `repro/phase0_limitations_repro.py` (run with
`/usr/bin/python3`; writes only under `repro/tmp/`; historical runs opened
read-only). Results (all REPRODUCED, `repro/tmp/phase0-repro-results.json`):

### 2.1 G — multi-range evidence rejected (Fifth run, exact values)

The real Fifth cross-examination wire output
(`logs/cross_examination.cross_examination-repair-86eeb1ee.final.json`) contains
`"lines": "184-185, 240-273"` among 32 otherwise-valid single ranges. Through
the production path (`wire_to_canonical` → canonical validation):

```
<root>.challenges[4].counter_evidence[3].lines: '184-185, 240-273'
does not match pattern '^[0-9]+(-[0-9]+)?$'
```

and through the full `classify_and_finalize` classifier (exit 0, real payload):
status INVALID_OUTPUT, artifact_status SCHEMA_INVALID. Control: the same
document with multi-range values replaced by their first range validates with
zero errors — the rejection is caused by the multi-range value alone. Run
outcome (historical fact): Codex cross-exam failed twice (original + the single
permitted repair reproduced the identical field), `32-codex-cross-examination
.json` was never checkpointed, run finalized `PARTIAL_CODEX_FAILURE`.
Benchmark 001 showed the sibling faces of the same defect: `"lines": ""`
(empty sentinel, 5/5 attempts INVALID_OUTPUT, 0 successful stages, metrics
`invocation_count: 0` under the pre-1.0.3 telemetry).

### 2.2 E — telemetry elapsed gap (Fifth run, exact values)

`99-run-metrics.json` of the Fifth run: both INVALID_OUTPUT cross-exam
attempts carry `completed_at` + full token usage but `elapsed_sec: null`.
Reproduced: a QUOTA-classified attempt and an INVALID_OUTPUT attempt both get
`completed_at` persisted and no `elapsed_sec`, while a COMPLETE attempt gets
`elapsed_sec: 30.006`. Cause (source-verified): `classify_and_finalize`
computes elapsed only on the COMPLETE path. v2 requirement: every terminal
attempt with started_at + completed_at has stable elapsed unless a documented
clock-data failure makes it genuinely unavailable.

### 2.3 A0 — no brief/environment consistency gate (Fifth run failure mode)

The Fifth brief
(`.../control/FIFTH-INDEPENDENT-RELEASE-AUDIT-AUDIT-COUNCIL.md`) contains
legacy absolute paths to `/home/isa/projects/llm_council_orchestrator` while
the frozen target was a detached-HEAD copy at
`/home/isa/audits/lco-fifth-independent-release-audit/target`
(head `f8c2b2c6955d19df7902cf2efc140ba558af044e`, branch `HEAD`). v1 stayed on
the right target only by harness reasoning. Reproduced mechanically: with a
brief declaring a DIFFERENT live repository as root, `preflight` returns
`ok: true` and `init-run` succeeds; the frozen fingerprint contains no
git_dir / git_common_dir / worktree-identity / detached-head / brief-root /
expected-head fields at all. There is no gate comparing the brief's declared
target to the frozen root, and nothing that would fail on a same-HEAD
alternate worktree, a symlinked root, or a root replaced mid-run.

### 2.4 Additional v1 observations (reconstruction findings)

1. **Implicit phase skipping**: `advance` to a later phase fills timestamps for
   passed-over intermediate phases without requiring their artifacts. The Fifth
   run reached LEDGER_COMPLETE with a CODEX_CROSS_EXAM_COMPLETE timestamp but
   no 32- artifact and no `phase_attempts` entry for it. Honest-but-implicit;
   v2 (pillar H) must make every skip an explicit, reason-carrying record
   (e.g. `phase_skips[]` in state.json) instead of silent timestamp filling.
2. **`detect_repo_root` is worktree-blind**: it requires `.git` to be a
   *directory*; in a linked/detached worktree `.git` is a file, so the walk
   overshoots the worktree root. Masked today because `state.repo_root` is
   always set; becomes a real defect the moment A1 creates worktrees.
   **Pre-freeze correction (operator, 2026-09-04): eliminated by plan Task
   A0.5 — all `.git`-directory sniffing is banned; git plumbing
   (`git rev-parse --show-toplevel`) is the only discovery authority, with
   regressions for main worktree, linked worktree, detached linked worktree,
   nested cwd, and non-repository paths.**
3. **Instruction-file scan** covers root + first-level dirs only (known F11).
4. **Wire adapter drops `pattern`/`minLength`/bounds** (canonical validation
   re-imposes them). Typed `line_ranges` objects ARE expressible in the strict
   wire subset (`type/properties/required/items/additionalProperties`), so the
   G fix is wire-clean end-to-end.
5. **Benchmark 001 artifacts use pre-1.0.3 shared log paths**
   (`logs/independent.jsonl` etc.) and a zero-invocation metrics file —
   finalized history; v2 must READ them (migration, pillar D replay) but never
   rewrite them (pillar A2).
6. **Both historical targets are detached-HEAD** (`branch: "HEAD"`): detached
   HEAD is a first-class valid v2 environment, not an anomaly.
7. **Codex read-only sandbox is not root confinement**: `--sandbox read-only`
   (Linux Landlock/seccomp in codex-cli) prevents writes but reads are not
   scoped to `-C <repo>`; `-C` only sets cwd. A0 must not assume otherwise.

---

## 3. v2 target architecture

### 3.1 Layered view

```
┌─ PUBLIC CONTRACT (F) ── describe --json + PUBLIC-CONTRACT.md (versioned)
├─ ORCHESTRATION (SKILL.md v2 + protocols) — Opus session; H lifecycle below
├─ ENVIRONMENT LAYER (A0/A1) ─ env_binding.py (freeze/verify), path_guard.py
│   (canonicalize + containment), environment_manager.py (AUTO/CURRENT/
│   RELEASE/HISTORICAL, worktree lifecycle, archive/cleanup = A2)
├─ EVIDENCE LAYER (B/G) ─ evidence_store.py (EvidenceRecord cache, visibility
│   classes, freshness) + evidence model v2 (typed line_ranges) + migration
├─ MODEL LAYER (unchanged core + E) — codex_runner.py (+elapsed everywhere,
│   budget config 2.0); Opus session roles unchanged
├─ SPECIALIST LAYER (C) — registry, blind post-barrier domain reviews,
│   default OFF, eval-gated
├─ EVAL LAYER (D) — tiers 1-4, sealed ground truth, scoring dimensions
└─ ARTIFACT LAYER (A2) — configurable roots; run artifacts never lost on
    worktree removal; sealed corpus isolated from auditor context
```

### 3.2 End-to-end lifecycle (pillar H — every arrow checkpointable + failure-classified)

```
brief invocation
 → brief/public-contract validation          [INVALID_AUDIT_INPUT]
 → environment mode resolution (AUTO/CURRENT/RELEASE/HISTORICAL)
 → isolated environment if needed (A1)      [WORKTREE_PREP_FAILED]
 → environment binding freeze (A0.1)
 → evidence staging (authorized only)
 → root/HEAD consistency gate (A0.2)         [INVALID_AUDIT_ENVIRONMENT:* → ZERO inference]
 → Opus independent  ∥  Codex independent    [PARTIAL_* / INVALID_OUTPUT / QUOTA / AUTH]
 → independence barrier (recorded timestamp)
 → optional blind specialists (C, default off)
 → normalization + clustering
 → mutual falsification (cross-exam both ways)
 → disagreement ledger
 → targeted adjudication (bounded, conditional)
 → final findings/report (from adjudicated ledger only)
 → telemetry/eval record (E/D)
 → archival/cleanup per retention policy (A2)
```

### 3.3 Trust boundaries — who enforces what (A0.3 design stance)

| Guarantee | Enforcement | Notes |
|---|---|---|
| Codex cannot WRITE target | OS (codex Landlock/seacomp read-only sandbox) | keep `-s read-only` / D1 resume config |
| Codex reads scoped to frozen root | **not guaranteed by codex** | read scope is not repo-bound; v2 adds runner-enforced argv/output validation + optional OS wrapper (research spike: bubblewrap `--ro-bind` launcher, or Landlock); document residual risk honestly |
| Opus path confinement (Read/Grep/Glob/Bash) | runner-enforced: PreToolUse hooks calling `path_guard` (deny before execution) + post-hoc write-guard/fingerprint | hook config is project/session-level settings; documented as runner-enforced, not OS |
| Repo identity immutability | `env_binding` digest re-verified before every inference phase + worktree-identity (not just HEAD) | same-HEAD alternate worktree denied |
| Brief consistency | explicit `target:` metadata (root + expected_head) validated against frozen binding; narrative absolute paths are inert text | zero model calls on mismatch |
| Disposable fixtures | capability-bound roots `/tmp/audit-council/<run-id>/<fixture-id>/` only; symlink + sibling-run escapes denied | never arbitrary `/tmp/**` |
| No secrets | unchanged v1 preflight rules | presence booleans only |

### 3.4 Frozen shared contracts (v2 schema version 2)

All v2 canonical artifacts carry `schema_version: 2`; readers accept 1 (via
deterministic migration) and 2; finalized v1 runs are NEVER rewritten.

#### 3.4.1 AuditEnvironmentBinding (A0.1 — schemas/env-binding.schema.json)

```json
{
  "binding_version": 2,
  "binding_digest": "<sha256 over canonical JSON of every field in this object EXCEPT binding_digest and frozen_at>",
  "frozen_at": "2026-09-04T00:00:00Z",
  "repo_root_realpath": "<realpath of audited worktree root>",
  "git_toplevel_realpath": "<git rev-parse --show-toplevel, realpath>",
  "git_dir_realpath": "<git rev-parse --absolute-git-dir, realpath>",
  "git_common_dir_realpath": "<git rev-parse --git-common-dir, realpath>",
  "head_sha": "<40-hex>",
  "detached_head": true,
  "worktree_identity": "<sha256(git_dir_realpath + '\\n' + repo_root_realpath)>",
  "source_repository_identity": {
    "common_dir_realpath": "<main worktree git dir when auditing a linked worktree>",
    "remote_url": "<git config remote.origin.url or null>"
  },
  "brief_sha256": "<sha256 of run-owned materialized brief>",
  "brief_target": {
    "declared_repository_root": "<from explicit brief metadata target block, or null>",
    "declared_expected_head": "<from explicit brief metadata, or null>"
  },
  "expected_head": "<40-hex; equals head_sha at freeze time>",
  "allowed_disposable_roots": ["/tmp/audit-council/<run-id>/<fixture-id>"],
  "repo_fingerprint_sha256": "<v1 fingerprint digest, unchanged algorithm>"
}
```

Rules: `binding_digest` is computed over every field of this object except
`binding_digest` itself and `frozen_at` — freeze time is metadata and never
participates in identity; two captures with otherwise identical inputs produce
identical digests. HEAD alone is NOT identity (two worktrees at one commit
differ by
`worktree_identity`). Detached HEAD valid (`detached_head: true`, branch
reporting untouched). A0.2 gate (before ANY frontier inference): recomputed
binding must equal frozen digest; declared brief root must realpath-resolve to
`repo_root_realpath`; declared expected head must equal `head_sha`. Mismatch →
`INVALID_AUDIT_ENVIRONMENT` with a reason from §3.4.2 and **zero model calls**.
Binding re-verified at wait/status/resume boundaries (identity stable across
restarts; A0.6 case "binding reconstructs identically after restart").

#### 3.4.2 INVALID_AUDIT_ENVIRONMENT failure taxonomy (A0.5)

Reasons: `BRIEF_ROOT_MISMATCH`, `BRIEF_HEAD_MISMATCH`,
`WORKTREE_IDENTITY_CHANGED`, `CWD_OUTSIDE_FROZEN_ROOT`, `PATH_ESCAPE_ATTEMPT`,
`ALTERNATE_WORKTREE_ACCESS`, `UNAUTHORIZED_TMP_ACCESS`, `REPO_ROOT_REPLACED`,
`SYMLINK_ESCAPE`. An environment failure never yields a product GO/NO-GO
verdict (it precedes/aborts inference; completeness state
`INVALID_AUDIT_ENVIRONMENT` is added alongside v1 states).

#### 3.4.3 Structured evidence model v2 — typed multi-range (G)

Evidence/counter-evidence items (all 6 inline locations across the 5 finding-
bearing schemas) gain, in schema version 2:

```json
"line_ranges": [
  {"start": 184, "end": 185},
  {"start": 240, "end": 273}
]
```

- `start`,`end`: integers, `minimum: 1`, `end >= start` (reversed → invalid);
  array `maxItems: 32`; deterministic canonical ordering = sort by `start`
  then `end` (canonicalizer sorts before fingerprinting; unsorted input is
  normalized, not rejected).
- Zero ranges = requirement-level/document evidence (legitimate; the smoke
  fixture proved `lines: null` → omitted). One range. Many disjoint ranges.
  `path`/`symbol` identity unchanged alongside.
- The legacy `lines` string is REMOVED from v2 canonical output; v1 artifacts
  are read via deterministic migration `lines "N"|"N-M" → line_ranges
  [{start:N,end:N}]|[{start:N,end:M}]`. **No comma-separated parsing, ever** —
  a v1-style multi-range string stays INVALID (it exists only inside raw logs
  of failed attempts, which are preserved untouched).
- Wire compatibility: `{start,end}` objects are expressible in the strict
  OpenAI wire subset (no pattern needed); the adapter marks `line_ranges`
  optional-nullable exactly like other optional evidence fields; canonical
  validation remains the final authority (bounds/ordering re-imposed).
- Fingerprint/canonicalization operates on the normalized semantic object
  (sorted ranges), and cross-exam/adjudication schemas share the identical
  evidence item definition (single `$defs`-style source, inlined per schema to
  keep Codex wire schemas self-contained).

#### 3.4.4 EvidenceRecord / provenance-bound store (B — schemas/evidence-record.schema.json)

```json
{
  "evidence_id": "ev-<16hex of content digest>",
  "kind": "REPO_FACT|FILE_EXCERPT|SEARCH_RESULT|DEPENDENCY_QUERY|GRAPH_RESULT|
           BUILD_RESULT|LINT_RESULT|TEST_RESULT|COVERAGE_RESULT|GIT_DIFF|
           DETERMINISTIC_PROBE|PACKAGE_SMOKE|TOOL_VERSION",
  "repository_fingerprint_sha256": "…",
  "environment_binding_digest": "…",
  "input_digest": "<sha256 of canonicalized command/query+args+scope>",
  "tool": {"name": "pytest", "version": "…"},
  "command_or_query": "pytest -q",
  "produced_at": "…",
  "freshness_policy": {"class": "FRESH_REQUIRED|CACHEABLE",
                       "ttl_sec": null, "invalidated_by": ["tracked_change",
                       "head_change", "binding_change"]},
  "result_digest": "…", "result_location": "evidence/<digest>.json",
  "producer": "HARNESS|OPUS|CODEX|SPECIALIST",
  "visibility": "SHARED_MECHANICAL|AUDITOR_PRIVATE|POST_BARRIER_SHARED",
  "validity_scope": "RUN|REPOSITORY|GLOBAL",
  "deterministic": true, "reproducible": true
}
```

Invariants: the store caches EVIDENCE ONLY — the kind enum excludes
finding/verdict/conclusion shapes and a content scanner rejects
finding-shaped documents (id/severity/claim fields) fail-closed; reuse
requires repository_fingerprint + binding_digest + input_digest + tool version
+ freshness match; `FRESH_REQUIRED` entries (release gates) are never served
from cache; `AUDITOR_PRIVATE` records (e.g. an Opus hypothesis-driven probe)
are not servable to the other auditor before the recorded independence
barrier (store API filters by consumer + barrier timestamp); consumers cite
`evidence_id` refs just-in-time (no cache dumps into context) and an access
log records exactly which evidence each model saw.

#### 3.4.5 Telemetry & governor 2.0 (E)

Job record v2 adds: `elapsed_sec` on EVERY terminal classification (computed
once at classification; null only with `elapsed_unknown_reason`), `budget_
decision_trace[]`; run metrics add per-phase retry cost, specialist cost,
cache-savings (evidence reuse count/tokens avoided), and keep
successful_stage_counted semantics (INVALID_OUTPUT contributes invocation +
tokens + elapsed + retry cost, never a successful stage). Budgets become a
configurable block (defaults preserving v1: successful stages ≤1/phase, ≤3
total, ≤3 attempts/phase; new: max specialists 0/2/3 default/normal/hard, max
specialist turns, max dynamic probes, cached-evidence policy,
force-fresh release gates). Every budget-driven omission is an explicit
`budget_omissions[]` record {stage, decision, reason}; the governor may never
skip mandatory independent passes, required fresh gates, hide material
disputes, downgrade model/reasoning, or promote PARTIAL→COMPLETE. UI quota
percentage is never treated as linear with tokens (Fifth/Bench usage below).

#### 3.4.6 Public audit contract (F)

`audit-council describe --json` (+ human-readable `PUBLIC-CONTRACT.md`),
semver-ish `protocol_version: 2` with documented compatibility policy:
additive changes keep 2.x; anything a prompt-authoring agent relied on that
changes bumps the major. Exposes: protocol version; environment modes;
model roles + independence rules; canonical artifact/evidence semantics
(incl. line_ranges); completeness states; governor constraints; brief target
metadata format (`target: {repository_root, expected_head}` block); known
limitations; runtime capabilities (sandbox guarantees per §3.3). Prompt
authors must never need `codex_runner.py`/`wire_adapter.py` internals.

#### 3.4.7 Specialist layer (C — default OFF)

Registry of domains (security-trust, concurrency-state,
authorization-multitenancy, data-integrity-migrations, api-contracts,
release-supply-chain, test-eval-quality, performance-resources,
frontend-accessibility). Activation requires a pre-frozen, documented reason
recorded in the run manifest BEFORE first-pass completion (based on
contract/repo/risk — never "a primary model already revealed the bug"). After
the independence barrier a specialist receives neutral context (repo, contract,
domain charter, SHARED_MECHANICAL evidence refs) and NO primary findings;
output schema `specialist-review.schema.json` (domain coverage, candidate
findings as full finding objects with `provenance.discovered_by:
SPECIALIST-<domain>`, negative evidence, unresolved questions, evidence refs).
Candidates enter normal normalization + falsification; specialists never own
GO/NO-GO. Counts: default 0, normal cap 2, hard cap 3. Remain default-off
until pillar D shows measurable recall/precision/root-cause/uncertainty
benefit per cost.

#### 3.4.8 Eval suite (D)

Tiers: (1) harness-deterministic (unit/integration, no models); (2) synthetic
seeded fixtures — small repos with known ground truth and protected negatives:
auth bypass, stale transaction/post-commit recovery, path escape/TOCTOU,
cross-tenant access, unsafe migration, API drift, release/supply-chain issue,
evidence provenance mismatch, structural identity mismatch, negative controls;
(3) historical replay — seeds Benchmark 001 (`0a5cee799f1c6ee0027183a8b36121e
6f02d3156`) and Fifth (`f8c2b2c6955d19df7902cf2efc140ba558af044e`), sealed
ground truth, run only for major protocol/model/security changes, release
candidates, or explicit operator approval; (4) real release-audit observations.
Scoring dimensions (separately reported): FINAL QUALITY (recall, precision,
root-cause fidelity, severity, novel verified findings), PROCESS
(independence, cross-exam corrections, rejection/narrowing, disagreement
resolution, evidence provenance, specialist incremental contribution),
HARNESS (COMPLETE/PARTIAL rate, schema/environment failures, retry/resume,
stale detection), ECONOMICS (Opus usage if exposed, Codex
input/cached/output/reasoning tokens, inference wall, total wall, tool/gate
count, retry cost, specialist cost, cache savings), DIVERSITY (Opus-only,
Codex-only, specialist-only valid; consensus; rescued; false positives
rejected), ENVIRONMENT (root escape, brief mismatch, alternate worktree,
unauthorized temp, false blocks — **100% required**). Novel CRITICAL/HIGH
truth requires deterministic reproduction, independent evaluator, human
confirmation, or predefined equivalent source/runtime evidence — model
agreement alone is never ground truth. Sealed ground truth never enters
active auditor context.

#### 3.4.9 Environment manager + artifact lifecycle (A1/A2)

Modes: AUTO (safest derivation; never silently downgrades required
isolation), CURRENT (live repo, only if contract permits), RELEASE (isolated
frozen target), HISTORICAL (isolated detached target + explicitly staged
evidence under allow/deny lists). The manager: detects source repo/target;
creates isolated detached worktrees (`git worktree add --detach`); freezes the
binding; creates an environment record; validates brief/root/HEAD; launches
only after preflight; leaves the live worktree untouched (never
clean/reset/stash); archives run artifacts BEFORE any worktree removal
(`git worktree remove`, never raw deletion); records provenance of
worktree/commit/archive. CLI surface stays small: `/audit-council <brief>`
(unchanged), optional `--isolated`, `--target`, `--prepare-only` only if they
earn their complexity. Artifact roots become configurable (default preserves
project-local `audit-output/audit-council`; an optional user data root such as
`~/.local/share/audit-council/` may be configured) with categories PROJECT
EVIDENCE / RUN ARTIFACTS / EPHEMERAL WORKTREES / BENCHMARK CORPUS / LONG-TERM
HISTORY; status/list/cleanup workflow with dry-run default for history;
existing project-owned audit-output/eval-live-output dirs are never silently
relocated — v2 ships a migration/retention recommendation requiring explicit
operator approval to act. Runtime/cache state (e.g. the path-guard active-run
registry) lives under an injectable root — `AUDIT_COUNCIL_CACHE_HOME` env
override, production default `${XDG_CACHE_HOME:-$HOME/.cache}/audit-council/`
— and deterministic development tests MUST inject an isolated disposable root
under the dev tree, never the real user cache.

### 3.5 Observed economics (calibration data for E/D, from READ-ONLY runs)

Fifth run (4 invocations, 2 successful stages): input 11,692,279 (cached
10,603,008), output 59,170, reasoning 22,544; independent elapsed 1010.9 s,
adjudication 64.7 s; ~61 min wall 08:19→09:20. Benchmark 001 (pre-1.0.3
telemetry): 5 attempts, 0 successful stages, metrics recorded 0 invocations.
Implication already frozen into E: attempt-based accounting, elapsed on every
terminal attempt, and no linear token/quota assumptions.

### 3.6 Honest limitations of the v2 design (to carry into KNOWN-LIMITATIONS)

- Codex read-confinement, if the OS-wrapper spike fails, degrades to
  runner-enforced validation + detection (documented residual risk; §3.3).
- Claude-side path enforcement via PreToolUse hooks is runner/session-level,
  not OS-level; a hooks-disabled session weakens to detection-only (fingerprint
  + write-guard), which the run manifest must record.
- Specialist value is unproven until Tier-2 evals say otherwise; default-off
  is the honest posture.
- Historical replay is expensive; its ground truth stays sealed and its use is
  approval-gated.
- The v1 implicit-phase-skip behavior will be made explicit, which is a state-
  machine semantics change (schema_version 2) — old runs remain readable and
  unwritten.

---

## 4. Traceability — spec pillar → design section

| Pillar | Design here | Plan package |
|---|---|---|
| A0 confinement + binding | §2.3, §3.3, §3.4.1, §3.4.2 | PKG-A0 |
| A1 environment manager | §3.4.9 | PKG-ENV |
| A2 artifact lifecycle | §3.4.9 | PKG-ENV |
| B evidence store/cache | §3.4.4 | PKG-EVID |
| C specialists | §3.4.7 | PKG-SPEC |
| D eval suite | §3.4.8, §3.5 | PKG-EVAL |
| E telemetry/governor | §2.2, §3.4.5 | PKG-TELE |
| F public contract | §3.4.6 | PKG-PUB |
| G structured evidence v2 | §2.1, §3.4.3 | PKG-SCHEMA |
| H integration | §3.2, §2.4(1) | lead + PKG-INT |
