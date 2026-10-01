# AUCDEV-024 — Auditor Model Selection Policy & Model Generation Migration (Backlog Objective)

Publication authority: `AUCDEV-024-BACKLOG-OBJECTIVE-PUBLICATION-20261001-01`
Published: 2026-10-01 (Europe/Istanbul) — RECORD-ONLY backlog-objective publication
Exact live base: `47aedfeeffac168f79f2d2fd6fe6dc346aaacd37` (root tree `5f2d5b40adc53ab5942bfb44e30c3760915ed147`; sole parent `89e3ab7610f4e4137ab3d3c8bcdc4f70ac1d61e5`)
Backlog priority/status: **P1 / OPEN**

This session is the RECORD-ONLY publication agent of a NEW backlog objective.
This record CREATES `AUCDEV-024` and grants NOTHING: no implementation
authority, no provider/model/frontier execution authority, no readiness-probe
authority, no audit or qualification authority, no installation authority.
ZERO provider/model/frontier calls, ZERO auditor execution, ZERO qualification,
ZERO installation, ZERO product/runtime source modification, ZERO
credential-content access occurred in this publication session. This record
does not implement model selection or model-generation migration and does not
change any historical model identity.

## 1. Verified predecessor transition

The immediately preceding Control Room publication at the exact base above
canonically completed and ACCEPTED the independent publication verification of
the EXEC-RA-006 PCH6-B diagnostic-readback chain. The following held state is
carried into this objective UNCHANGED and is NOT reopened here:

- AUCDEV-023 = P1 / READY / NOT DONE
- PCH6 execution authority = CONSUMED / TERMINAL / CLOSED / NO_RERUN
- MODEL_ENGAGEMENTS = 2/2 USED; retry FALSE; reconciliation FALSE
- CONFORMING_TWO_FIRSTPASS_SET = INCOMPLETE; audit completeness = INCOMPLETE
- qualification NONE; installation NONE
- installed source `8ae33444f349ce73c1359b963722e2d16acba630` with
  installed-qualified predecessor provenance NOT ESTABLISHED
- PCH6-CR-BSD-001 / PCH6-B-SD-001 / PCH6-B-SD-002: NO remediation authorized
- sealed report substance remains UNREAD (identity-only forever)

## 2. Problem / evidence (verified at the exact base)

| Surface | Verified fact at `47aedfeeffac168f79f2d2fd6fe6dc346aaacd37` |
|---|---|
| `skill/SKILL.md` | frontmatter `model: claude-opus-5` (L5); prose identifies Claude Opus 5 and Codex GPT-5.6 Sol with Codex reasoning described as xhigh (L3, L24-L25); auditor-artifact guidance pins `model: "claude-opus-5"` (L162) |
| `skill/PUBLIC-CONTRACT.md` | Opus model = `claude-opus-5` (L56); Codex model = `gpt-5.6-sol` with reasoning effort `xhigh` (L57) |
| `skill/scripts/audit_council.py` | preflight model-resolvability advisory hardcoded to `gpt-5.6-sol` (L282-L290); PUBLIC_CONTRACT model roles hardcoded to `claude-opus-5` and `gpt-5.6-sol`/`xhigh` (L1462, L1467-L1468) |
| `skill/scripts/codex_runner.py` | module constants `MODEL = "gpt-5.6-sol"` (L42) and `REASONING_EFFORT = "xhigh"` (L43); the SAME constants govern BOTH the fresh argv (L207, L211) and the resume argv (L194-L198) |
| `skill/schemas/independent-audit.schema.json` | `model` enum contains ONLY `claude-opus-5` and `gpt-5.6-sol` |
| `skill/schemas/audit-contract.schema.json` | NO model-selection / model-effort provenance is currently frozen in the audit contract |
| `skill/tests/` | 32 test files; 12 carry hardcoded legacy model identities — `test_codex_runner_mock.py` (5 hits), `test_schema_validation.py`, `fixtures/fake_codex.py`, `fixtures/fifth-opus-independent-v1.json`, `test_disagreement_normalization.py`, `test_evidence_pipeline.py`, `test_line_ranges_v2.py`, `test_review_hardening.py`, `test_telemetry_v103.py`, `test_telemetry_v2.py`, `test_v101_hardening.py`, `test_wire_adapter_v103.py`; the lifecycle/resume/public-contract/migration surfaces (`test_env_lifecycle.py`, `test_resume.py`, `test_migration_compat.py`, `test_public_contract.py`, `test_codex_sandbox.py`, `test_wait_lifecycle_v102.py`) must be reviewed for model-selection semantics |

Therefore this objective is NOT a global string-replacement task.

## 3. Operator product direction (PROSPECTIVE)

For FUTURE Audit Council runs/candidates, establish a model-selection policy
with these modes and precedence:

1. **audit-default** — Auditor A: exact model `claude-opus-5-5`, exact effort
   `high`. Auditor B: exact model `gpt-6.1-sol`, exact reasoning effort
   `high`.
2. **inherit** — inheritance occurs ONLY when explicitly requested; before ANY
   inference, inheritance MUST resolve to concrete exact model identities and
   concrete effort values; unresolved/ambiguous inheritance FAILS CLOSED; no
   symbolic `current`, `default`, `auto` or equivalent unresolved value may
   reach inference; the authoritative inheritance source must be explicitly
   defined, mechanically observable where supported, and recorded.
3. **explicit** — caller supplies concrete supported model/effort selections;
   selections are validated and frozen before inference.

Precedence: `explicit > explicitly requested inherit > audit-default`.
There is NO silent fallback.

This direction applies PROSPECTIVELY. It MUST NOT relabel historical runs or
historical auditor identities.

## 4. Scope

AUCDEV-024 covers the design and later implementation of:

- one canonical model-selection policy/resolution layer;
- audit-default / inherit / explicit modes;
- deterministic precedence;
- exact requested and resolved auditor model identities;
- exact requested and resolved effort identities;
- selection source/provenance;
- client/runtime version provenance where mechanically available;
- pre-inference freezing of the resolved selection into immutable run/audit
  provenance;
- Claude-side exact-model and exact-effort enforcement;
- Codex-side exact-model and exact-reasoning-effort enforcement;
- fresh-launch enforcement;
- resume enforcement;
- actual/effective model observation where the client exposes trustworthy
  evidence;
- mismatch detection;
- unavailable/unresolvable model handling;
- no-fallback enforcement;
- schema/public-contract/docs updates;
- deterministic tests and compatibility fixtures.

The exact minimal representation may be chosen during design/implementation,
but the resolved selection MUST become immutable, checksum-bound provenance
before the first inference phase and MUST be referenced by run state/contract
such that later inference cannot silently change it.

## 5. Non-goals

AUCDEV-024 does NOT:

- retry or repair PCH6;
- remediate PCH6-CR-BSD-001, PCH6-B-SD-001 or PCH6-B-SD-002;
- read any sealed report substance;
- rewrite historical Audit Council runs;
- relabel historical `claude-opus-5` or `gpt-5.6-sol` outputs;
- transfer any historical audit or qualification verdict;
- qualify a new candidate;
- install a candidate;
- grant provider/model execution authority;
- implement an autonomous development/audit lifecycle;
- weaken first-pass blindness, confinement, target binding, engagement
  accounting, immutable checkpoints, or fail-closed behavior.

## 6. Held invariants

The future implementation must preserve: exact target identity; first-pass
blindness; Codex read-only/confinement semantics; Claude
procedural/mechanical boundaries exactly as actually supported; evidence
provenance; model-engagement accounting; bounded retry/repair behavior;
explicit completeness states; immutable checkpoint/resume integrity; no
silent fallback; no historical verdict transfer; candidate
self-qualification prohibition. Historical model identity is immutable
evidence.

## 7. Historical / resume compatibility

Legacy identities remain valid historical values: `claude-opus-5`,
`gpt-5.6-sol`, and historical `gpt-5.6-sol` reasoning `xhigh`. The
independent-audit result schema must not simply replace the legacy enum with
new values; historical artifacts must continue to validate at their historical
identity. A resumed existing run MUST retain the exact model generation and
effort bound to that run. Resume MUST NOT silently migrate
`claude-opus-5` -> `claude-opus-5-5`, `gpt-5.6-sol` -> `gpt-6.1-sol`,
`xhigh` -> `high`, or perform any other generation/effort substitution. If an
old resumable run lacks sufficient frozen provenance to establish its
original concrete model/effort safely, the implementation must FAIL CLOSED
rather than guess. Do not rewrite historical artifacts to add new provenance.

## 8. Acceptance criteria

A future implementation candidate is mechanically acceptable only if ALL of
the following are demonstrated:

- **A. DEFAULT** — a fresh run with no model-selection override resolves
  exactly to Auditor A = `claude-opus-5-5` / `high` and Auditor B =
  `gpt-6.1-sol` / `high`.
- **B. INHERIT** — explicit inherit resolves concrete exact identities and
  effort BEFORE inference; ambiguous/unobservable/unresolvable inheritance
  fails closed with ZERO inference.
- **C. EXPLICIT** — explicit supported concrete model/effort selections are
  validated and frozen.
- **D. PRECEDENCE** — exactly `explicit > explicitly requested inherit >
  audit-default`.
- **E. FREEZE** — for each auditor, immutable pre-inference provenance records
  at minimum: selection mode; selection source; requested model, if
  applicable; resolved exact model; requested effort, if applicable; resolved
  exact effort; client/runtime version where mechanically obtainable;
  actual/effective observed model where mechanically obtainable;
  binding/digest sufficient to detect later mutation.
- **F. ENFORCEMENT** — fresh inference uses the frozen exact model/effort;
  resume inference uses the SAME run-frozen exact model/effort.
- **G. MISMATCH** — any mechanically observable actual/effective model
  mismatch invalidates or fails the run at an explicitly defined fail-closed
  boundary; it may never silently continue under a different model.
- **H. NO FALLBACK** — unavailable, unsupported or rejected selected models do
  not fall back to another model generation, alias or effort level.
- **I. HISTORY** — historical artifacts with the old model identities remain
  valid and are never relabelled.
- **J. RESUME** — a run started under a legacy or new generation cannot
  generation-switch on resume.
- **K. CONTRACT / SCHEMA** — public contract, machine-readable contract,
  schemas, SKILL documentation, runtime enforcement and tests agree on
  selection semantics.
- **L. TESTS** — deterministic tests cover at minimum: audit-default exact
  pair; inherit; explicit; precedence; resolved-selection freeze;
  unsupported/unresolvable model; effort unsupported/unresolvable; observed
  mismatch; no fallback; fresh launch; resume identity lock; historical
  schema compatibility; legacy artifact compatibility; public-contract drift;
  model-selection provenance mutation/tamper rejection where applicable.
- **M. ZERO-PROVIDER MECHANICAL VALIDATION** — mechanical correctness of the
  implementation must be testable without a real provider/model call.

## 9. Readiness gap — BLOCKS OPEN -> READY

Before any implementation prompt is released, ONE bounded ZERO-PROVIDER
runtime/model-resolution readiness probe must be separately authorized and
performed. The probe must establish the CURRENT LOCAL CLIENT surfaces,
versions and mechanisms for:

Claude side: installed Claude Code/client version; exact supported
syntax/mechanism for selecting `claude-opus-5-5`; exact supported mechanism
for forcing effort = high for the interactive orchestrator; whether that
effort is mechanically observable/verifiable before or after inference;
whether any alias/default/fallback behavior could substitute another model;
whether the skill frontmatter can enforce effort or a separate session/client
mechanism is required.

Codex side: installed Codex CLI version; `--model` support; exact
`gpt-6.1-sol` resolvability from local supported metadata/cache/help where
available; exact high reasoning-effort configuration syntax; fresh and resume
argv behavior; any alias/default/fallback behavior; actual/effective model
evidence exposed by the client/job record.

The probe MUST make ZERO provider/model/frontier inference calls; may inspect
local client `--help`/`--version`/config schema/model metadata; must not read
credentials or auth contents; must distinguish official capability
documentation from what the installed local clients mechanically expose; and
must FAIL CLOSED on inability to establish the required control surface.
OPEN -> READY requires a fresh Control Room readback accepting that readiness
evidence and a bounded implementation surface.

## 10. Sequencing

1. Publish this AUCDEV-024 objective at P1 / OPEN (THIS publication).
2. Independent Control Room readback of the objective publication.
3. Separately authorize and perform the bounded ZERO-PROVIDER
   runtime/model-resolution readiness probe.
4. Control Room readback of that probe.
5. Only if readiness is established: AUCDEV-024 OPEN -> READY.
6. Separately authorize implementation against a fresh exact base SHA.
7. Implementation creates a NEW candidate SHA.
8. Control Room verifies diff/tests/invariants.
9. Fresh independent audit/qualification governance applies to that exact new
   candidate; prior verdicts do not transfer.
10. Installation, if ever authorized, remains a separate later transition.

## 11. Validation budget for this publication

This publication is docs/governance only: ZERO provider/model calls; ZERO
client inference calls; ZERO runtime modification; ZERO product source
modification; ZERO qualification/install work.

## 12. Next action (EXACTLY ONE)

INDEPENDENT CONTROL ROOM READBACK OF THE AUCDEV-024 OBJECTIVE PUBLICATION
BEFORE ANY RUNTIME/MODEL-RESOLUTION PROBE OR IMPLEMENTATION PROMPT.
Until that readback is returned and accepted: NO readiness probe, NO
implementation prompt release, NO product/runtime source modification, NO
provider/model/frontier call, NO qualification, NO installation. Recording
this next action grants nothing.

## 13. Acceptance matrix (publication gates)

| ID | Gate | Status |
|---|---|---|
| AUC024OP-01 | live GitHub master == local HEAD == origin/master == expected base at bootstrap (ls-remote authoritative; fetch clean rc 0) | PASS |
| AUC024OP-02 | base re-resolved EXACT immediately before build and again before staging | PASS |
| AUC024OP-03 | base root tree / sole parent / trust-anchor ancestry / zero merges derived from git only | PASS |
| AUC024OP-04 | four canonical docs read AT the exact SHA | PASS |
| AUC024OP-05 | AUCDEV-024 free: no backlog heading and no queue row at base | PASS |
| AUC024OP-06 | AUCDEV-024 free: canonical objective path absent (rc 128) and full-history path rows ZERO | PASS |
| AUC024OP-07 | AUCDEV-024 references at base are historical "only if free" prose only (excluded class per tasking) | PASS |
| AUC024OP-08 | source fact verified: skill/SKILL.md | PASS |
| AUC024OP-09 | source fact verified: skill/PUBLIC-CONTRACT.md | PASS |
| AUC024OP-10 | source fact verified: skill/scripts/audit_council.py | PASS |
| AUC024OP-11 | source fact verified: skill/scripts/codex_runner.py fresh + resume constants | PASS |
| AUC024OP-12 | source fact verified: independent-audit schema enum | PASS |
| AUC024OP-13 | source fact verified: audit-contract schema freezes no selection provenance | PASS |
| AUC024OP-14 | test-surface inventory derived (32 files; 12 with hardcoded identities; lifecycle/resume/public-contract/migration surfaces listed) | PASS |
| AUC024OP-15 | collision sweep S1 CLEAN (tracked content at exact base) with sanity liveness | PASS |
| AUC024OP-16 | collision sweep S2 CLEAN (full-history pickaxe) with sanity liveness | PASS |
| AUC024OP-17 | collision sweep S3 CLEAN (commit-message fixed strings) with sanity liveness | PASS |
| AUC024OP-18 | collision sweep S4 CLEAN (full readable worktree; TRACKED = 0, OTHER = 0, GOVERNED_SELF confined to this session's evidence workspace) | PASS |
| AUC024OP-19 | collision sweep S5 CLEAN (repo-root names: evidence-workspace self-name only) | PASS |
| AUC024OP-20 | collision sweep S6 CLEAN (/home/isa top-level names: ALL ZERO) | PASS |
| AUC024OP-21 | collision sweep S7 CLEAN (full-depth path-name traversal; no maxdepth/pruning/symlink-following; stderr EMPTY; guard ZERO) | PASS |
| AUC024OP-22 | collision sweep S8 CLEAN (deployed-root path names) with deployed-namespace sanity | PASS |
| AUC024OP-23 | collision sweep S9 CLEAN (readable deployed-root non-sealed contents, sealed/credential files excluded BY NAME) with sanity liveness | PASS |
| AUC024OP-24 | CORRECTED_REAL_COLLISION_COUNT = 0 AND SCAN_ERROR_COUNT = 0; zero session transients in the sweep instrument | PASS |
| AUC024OP-25 | CURRENT-STATE built from the exact live base blob with rotation confined to lines 3/11/23-25 + one dated record appended; non-rotated lines byte-identical | PASS |
| AUC024OP-26 | BACKLOG built from the exact live base blob with only authorized hunks (counts paragraph, 2026-10-01 recount line, AUC024 queue row, AUCDEV-024 work item, one dated record) | PASS |
| AUC024OP-27 | mechanical queue recount of the built backlog: READY 9 / OPEN 8 / BLOCKED 3 = 20 open; P0 2 / P1 8 / P2 11 = 21 queue rows; 3 DEFERRED; exactly one AUCDEV-024 heading and row | PASS |
| AUC024OP-28 | hex-literal gate PASS over the new record in full and all changed/appended CURRENT/BACKLOG lines | PASS |
| AUC024OP-29 | precommit: live master re-resolved == expected base immediately before staging | PASS |
| AUC024OP-30 | precommit: changed tracked paths EXACTLY the three authorized documentation paths | PASS |
| AUC024OP-31 | precommit: `git diff --check` and staged diff --check PASS | PASS |
| AUC024OP-32 | precommit: skill / qualification-harness / bootstrap-supervisor protected trees EXACT at HEAD and held EXACT in the staged write-tree | PASS |
| AUC024OP-33 | preexisting smoke-fixture gitlink drift preserved UNSTAGED | PASS |
| AUC024OP-34 | exactly ONE bounded docs-only commit whose sole parent is the exact base | PASS |
| AUC024OP-35 | exactly ONE push | PASS |
| AUC024OP-36 | post-push: live master == local new HEAD; the three paths fetched from GitHub at the new SHA and Git-blob equality verified | REQUIRED_POST_PUSH (evidence: generated-LAST handoff) |
| AUC024OP-37 | generated-LAST reviewer handoff produced AFTER the push and post-push readback, with SHA256SUMS covering EVERY regular payload member including README and exact payload-set equality | REQUIRED_POST_PUSH (evidence: generated-LAST handoff) |
| AUC024OP-38 | next action EXACTLY ONE: independent Control Room readback of this objective publication | PASS |

## 14. Standing prohibitions

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from an
agent session; never rerun the launcher; never treat any recorded grant phrase
as a new grant; never execute a real auditor or provider/model; never open the
four sealed artifacts; never remediate PCH6 findings from this objective;
never relabel or rewrite historical model identities, runs, records or
artifacts; never run the readiness probe or release an implementation prompt
from this publication; never claim qualification or installation; never claim
any authority — this publication grants none. Historical records, matrices,
prompts and evidence workspaces are append-only.
