# AUCDEV-024 — Model-Selection / Model-Generation Migration Implementation

Implementation authority: `AUCDEV-024-MODEL-SELECTION-MODEL-GENERATION-MIGRATION-IMPLEMENTATION-20261001-01` (operator-authorized in-session against exact base `ca276949a6435d58edbd3d142c7700f9e08c8b25`).
Date: 2026-10-01 (Europe/Istanbul).
Status: **implementation CANDIDATE awaiting independent Control Room readback — NOT DONE; no audit PASS, no qualification, no installation is claimed.**

This session was the IMPLEMENTER of the accepted AUCDEV-024 objective only
(model-selection / model-generation migration in the skill source, schemas,
docs and deterministic zero-provider tests). It did NOT run any auditor, did
NOT invoke the AUCDEV-023 governance-chain wrapper/driver/launcher, did NOT
touch deployment state, attempts or AccountingStore, did NOT read credential
contents or sealed substance, and did NOT qualify or install anything.

## 1. Exact identities

- Required base verified EXACT at bootstrap, before staging and before
  commit: live GitHub `refs/heads/master` == `origin/master` == local HEAD ==
  `ca276949a6435d58edbd3d142c7700f9e08c8b25` (ls-remote authoritative; fetch
  clean rc 0).
- Candidate HEAD: see §9 (recorded after the single push; sole parent
  `ca276949a6435d58edbd3d142c7700f9e08c8b25`).

## 2. Implemented policy (objective §3 / acceptance A–M)

New canonical module `skill/scripts/model_selection.py` (stdlib only):

- **audit-default** — Auditor A (opus/Claude) `claude-opus-5-5` / `high`;
  Auditor B (codex/Codex) `gpt-6.1-sol` / `high` (acceptance A).
- **inherit** — only when explicitly requested. Codex source: top-level
  `model` + `model_reasoning_effort` keys of `~/.codex/config.toml`
  (tomllib; profiles deliberately NOT resolved pre-inference). Claude source:
  `ANTHROPIC_MODEL` + `CLAUDE_CODE_EFFORT_LEVEL`. Both halves must resolve to
  concrete supported identities BEFORE any inference; unresolved, missing,
  symbolic (`current`/`default`/`auto`/…) or alias values (e.g. the live host
  redirect `glm-5.3[1m]`) FAIL CLOSED with zero inference (acceptance B;
  readiness ZP-B1 routing).
- **explicit** — caller supplies BOTH a concrete supported model AND effort;
  partial explicit fails closed (the missing half must not silently become
  the default); values validated then frozen (acceptance C).
- **Precedence** exactly `explicit > explicitly requested inherit >
  audit-default`; **no silent fallback** anywhere — unsupported values raise
  `ModelSelectionError`, never substitute (acceptances D, H).
- Supported sets: models opus `claude-opus-5-5`, `claude-opus-5`; codex
  `gpt-6.1-sol`, `gpt-5.6-sol`. Efforts opus `high`/`medium`/`low`; codex
  `high`/`medium`/`low`/`minimal`/`xhigh` (`xhigh` = legacy, selectable so
  frozen legacy runs resume exactly). Legacy identities remain valid
  historical values; historical artifacts are never relabelled (acceptance I).

## 3. Pre-inference provenance freeze (acceptance E, F)

- `model_selection.freeze_record()` produces the immutable record
  `{auditor, mode, source, requested_model, requested_effort, model, effort,
  client_version, frozen_at, selection_digest}`; `selection_digest` is a
  SHA-256 over the canonical selection core (mutation-detecting); the record
  lives inside the checksum-ledger-protected `state.json` (same residual
  posture as the environment-binding digest: state.json itself is ledger-
  anchored; full-ledger forgery remains the documented R4 residual).
- **Auditor A**: `init-run` / `prepare` resolve (flags `--claude-model`,
  `--claude-effort`, `--inherit-claude-model`; audit-default when absent) and
  freeze `state.model_selection.opus` at run creation, before any inference.
- **Auditor B**: `codex_runner.py start` resolves (flags `--model`,
  `--effort`, `--inherit-model`) under the R-B002 run-state lock; the run's
  FIRST codex stage stages the freeze into the existing launch transaction
  (spawn + authoritative persistence are one serialized mutation; a
  persistence failure terminates the child, so no inference can complete
  without the frozen selection becoming durable). `client_version` records
  the local codex `--version` (stdin `DEVNULL`, 30 s bound, `None` when
  unobtainable).
- **Resume lock (acceptance F, J)**: every later stage, resume and repair
  reuses the run-frozen selection exactly; explicit CLI values that CONFLICT
  with it are refused (`RUN_FROZEN_MODEL_CONFLICT` /
  `RUN_FROZEN_EFFORT_CONFLICT`); a tampered record (digest mismatch) is
  refused (`FROZEN_RECORD_TAMPERED`); an old resumable run WITHOUT a frozen
  selection FAILS CLOSED (`RESUME_WITHOUT_FROZEN_SELECTION`) — never guessed,
  never silently migrated `claude-opus-5 -> claude-opus-5-5`,
  `gpt-5.6-sol -> gpt-6.1-sol`, `xhigh -> high`.

## 4. Claude environment safety (readiness ZP-B2 routing)

- `model_selection.claude_ambient_conflicts()` compares (never prints) the
  ambient Claude selection env vars `ANTHROPIC_MODEL`,
  `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL`,
  `CLAUDE_CODE_MAIN_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL`,
  `CLAUDE_CODE_EFFORT_LEVEL` against the resolved selection: unset-or-exact-
  equal passes; ANY other value (alias, other generation, redirect — the live
  host pins all of them to `glm-5.3[1m]` and effort `max`) is a conflict.
- Fail-closed boundaries: `preflight` (failure row
  `claude-model-environment`), `init-run`/`prepare` (refuse BEFORE creating
  the run), `resume-check` (stage `model-selection`, exit 10). Variable NAMES
  only are ever reported; values are never printed.
- The documented launch contract (SKILL.md hard rules + PUBLIC-CONTRACT.md)
  requires the session be launched with explicit `claude-opus-5-5` +
  `--effort high` (the local catalog default effort is `medium`, so effort
  must never be omitted) in a sanitized model environment.
- Artifact identity gate: `advance`/`resume-check` reject an independent
  audit artifact whose `model` differs from the run-frozen selection of that
  auditor (`INVALID_ARTIFACT`); inert on legacy runs without a frozen
  selection (their identities are immutable historical values).

## 5. Codex fresh + resume + mismatch (readiness ZP-B3 routing)

- Both the fresh argv and the resume argv pass the run-frozen explicit
  `--model` and `-c model_reasoning_effort="…"`; user-config defaults are
  never relied upon.
- `parse_effective_identity()` extracts best-effort effective model/effort
  from codex `--json` events (`model_slug` anywhere; `model`/`effort` inside
  turn_context-style events). Any OBSERVABLE mismatch with the frozen
  selection finalizes the attempt as `MODEL_MISMATCH` (runner exit **8**,
  stage not counted, raw output preserved) — the explicit fail-closed
  boundary (acceptance G). Absent identity evidence enforces nothing
  ("where mechanically obtainable"); undocumented Codex internal resume
  precedence is NOT claimed established.
- `99-run-metrics.json` invocations now carry `effective_model` /
  `effective_effort` (null = unknown).

## 6. Contract / schema / docs agreement (acceptance K)

- `audit_council.py PUBLIC_CONTRACT`: model_roles opus `claude-opus-5-5` /
  effort `high`, codex `gpt-6.1-sol` / `high`; NEW additive
  `model_selection` contract section (modes, precedence,
  `no_silent_fallback: true`, audit_default, supported sets, inherit sources,
  claude launch contract, resume lock, mismatch boundary, legacy note).
  Protocol stays 2.0 (additive change; no documented field's meaning
  changed).
- `public-contract.schema.json`: additive optional `effort` on the opus role
  + the `model_selection` section shape.
- `state.schema.json`: additive optional `model_selection` (per-auditor
  record with mode/model/effort enums incl. legacy values and
  `^[0-9a-f]{64}$` digest); legacy states without it keep validating.
- `audit-contract.schema.json`: additive OPTIONAL `model_selection` block;
  historical contracts keep validating.
- `independent-audit.schema.json`: `model` enum ADDS `claude-opus-5-5` and
  `gpt-6.1-sol` (legacy values retained — historical artifacts still
  validate).
- Preflight codex model-resolvability advisory now checks the new
  audit-default `gpt-6.1-sol`.
- Docs: `SKILL.md` (frontmatter `model: claude-opus-5-5`, prose, hard-rules
  model-selection block, preflight/init/phase guidance, artifact guidance),
  `PUBLIC-CONTRACT.md` (roles + new "Model selection" section),
  `README.md`, `prompts/codex-independent.md` (output example identity),
  `protocols/independent-audit.md`. Dated historical design records
  (e.g. `docs/A0-CODEX-CONFINEMENT.md`) were NOT rewritten.

## 7. Tests (acceptance L, M — deterministic, zero-provider)

- NEW `skill/tests/test_model_selection.py` (48 tests): audit-default exact
  pair; inherit/explicit/precedence (incl. explicit-beats-inherit,
  inherit-beats-default, no-request-means-no-inherit); unsupported/symbolic/
  partial selection fail-closed with no fallback; codex config inherit
  (concrete, missing-key, symbolic, absent-config) and Claude env inherit
  (concrete, missing effort, alias-redirect `glm-5.3[1m]`); provenance freeze
  shape/digest/roundtrip; tamper rejection (model, mode); ambient conflict
  gate (matching passes; model/default/subagent/effort conflicts detected;
  names-only never values); CLI gates (preflight pass/fail, init freeze,
  init ambient refusal with zero side effects, resume-check conflict exit
  10); artifact identity gate (wrong generation rejected, frozen identity
  accepted, legacy run inert); public-contract agreement (module ↔ machine
  contract ↔ md mirror ↔ SKILL frontmatter).
- `test_codex_runner_mock.py` (+12 tests, updated assertions): fresh argv
  `--model gpt-6.1-sol` + `model_reasoning_effort="high"`; audit-default
  freeze into state (mode/source/digest); explicit legacy pair
  (`gpt-5.6-sol`/`xhigh`) selected+frozen; unsupported/symbolic/partial
  fail-closed with zero jobs and zero inference; resume without frozen
  selection fails closed; resume reuses frozen LEGACY generation exactly
  (no migration); conflicting CLI model on a frozen run refused; tampered
  frozen selection refused; effective model/effort MISMATCH → exit 8
  `MODEL_MISMATCH` with stage not counted; matching effective identity
  completes; absent identity evidence enforces nothing.
- `test_schema_validation.py`: shared fixture default → `claude-opus-5-5`;
  enum additive (new+legacy valid, alias rejected); state
  `model_selection` provenance validity/invalidity; contract optional
  `model_selection`.
- `test_public_contract.py` (+3 drift tests), `test_migration_compat.py`
  (v1 artifact legacy identity asserted + v1-era simulation also drops
  `model_selection`), `test_telemetry_v103.py` (new default identities),
  hermeticity scrubs (ambient Claude model env vars popped at module import)
  in the 14 audit_council-driving test files so the new gate cannot be
  tripped by the host's live redirect, `fixtures/fake_codex.py` (echoes the
  selected identity; emits `turn_context` effective-identity evidence with
  `EFFECTIVE_MODEL`/`EFFECTIVE_EFFORT` overrides), `eval/tier2_scoring.py`
  scripted artifacts re-based to the new audit-default pair.

## 8. Validation performed (all zero-provider)

- Targeted modules first, then the complete deterministic suite
  (`python3 -m unittest discover -s skill/tests`):
  **753 tests, ALL PASS, 0 failures, 0 errors, 0 skips** (final recorded
  run `aucdev024-implementation-evidence/full-suite-final.txt`; intermediate
  honest iteration notes in §10).
- Schema/contract mechanical validation evidence recorded in
  `aucdev024-implementation-evidence/schema-contract-validation.txt`
  (describe-contract vs schema; state with/without selection; contract
  with/without model_selection; independent-audit enum additive; resolved
  audit-default pair; precedence).
- ZERO provider/model/frontier inference calls, ZERO real auditor
  execution, ZERO wrapper/driver invocation, ZERO credential-content access,
  ZERO sealed-substance access, ZERO deployment mutation, ZERO installation
  occurred during implementation or testing. No Claude/Codex install or
  upgrade was performed.

## 9. Changed paths (exactly)

NEW: `skill/scripts/model_selection.py`; `skill/tests/test_model_selection.py`;
`docs/chatgpt-project/AUCDEV-024-MODEL-SELECTION-MODEL-GENERATION-MIGRATION-IMPLEMENTATION.md`.
MODIFIED: `skill/SKILL.md`, `skill/PUBLIC-CONTRACT.md`, `skill/README.md`,
`skill/prompts/codex-independent.md`, `skill/protocols/independent-audit.md`,
`skill/eval/tier2_scoring.py`, `skill/schemas/{independent-audit,
audit-contract,public-contract,state}.schema.json`,
`skill/scripts/audit_council.py`, `skill/scripts/codex_runner.py`,
`skill/tests/fixtures/fake_codex.py`, `skill/tests/test_codex_runner_mock.py`,
`test_schema_validation.py`, `test_public_contract.py`, `test_resume.py`,
`test_migration_compat.py`, `test_telemetry_v103.py`, `test_tier2_scoring.py`,
`test_v101_hardening.py`, and the hermetic-scrub-only edits to
`test_b001_b004_remediation.py`, `test_disagreement_normalization.py`,
`test_env_lifecycle.py`, `test_env_prepare_e2e.py`,
`test_evidence_pipeline.py`, `test_qx_stabilization.py`,
`test_review_hardening.py`, `test_source_write_guard.py`,
`test_tier4_da27c0.py`; plus this record's two companions
(`AUCDEV-CURRENT-STATE.md` rotation lines 3/11/23-25 + dated record;
`AUCDEV-BACKLOG.md` item status note + dated tail record).
Pre-existing `smoke-fixture`/`smoke-fixture-103` gitlink drift preserved
UNSTAGED. Evidence workspace, handoff archive and instruments are UNTRACKED
host artifacts, NOT committed.

Candidate HEAD: the single bounded fast-forward commit created by this
implementation (sole parent `ca276949a6435d58edbd3d142c7700f9e08c8b25`;
exactly one push; post-push live master == local HEAD verified in-session).
A commit cannot embed its own identity: the exact candidate SHA is recorded
in the session's final return and in the generated-LAST reviewer handoff
produced after the push.

## 10. Honest session notes (append-only, no erasure)

- Test-iteration failures during development were fixed in-session and every
  first output is preserved in the evidence workspace (`full-suite-run1.txt`,
  `full-suite-run2.txt`): run 1 had 3 failures + 4 errors — (i) a v1-era
  simulation that predated selection freezing (fixed: the v1 simulation now
  also drops `model_selection`), (ii) tier-2 scripted artifacts claiming the
  legacy pair against the frozen new default (fixed: re-based to the new
  audit-default pair), (iii) tier2 tests lacking the ambient-var scrub
  (fixed), (iv) an import error in `test_v101_hardening.py` from the scrub
  block (fixed), (v) RB002 launch-transaction ordering (fixed: the codex
  freeze joins the existing post-spawn persistence transaction instead of a
  separate pre-spawn save, preserving the R-B002 kill-on-persistence-failure
  semantics).
- One product-code defect found and fixed during validation:
  `_codex_client_version` initially inherited stdin, letting a `--version`
  probe block on a non-EOF stdin (30 s timeout per freeze under piped
  stdin); fixed with `stdin=subprocess.DEVNULL`.
- The ambient-conflict gate intentionally FAILS CLOSED on this host's live
  environment (all Claude model env vars pinned to `glm-5.3[1m]`, effort
  `max`): real audit runs require the documented sanitized launch contract.
  Tests are hermetic against that host state by explicit scrubbing.

## 11. Next action (EXACTLY ONE)

INDEPENDENT CONTROL ROOM READBACK OF THIS AUCDEV-024 IMPLEMENTATION
CANDIDATE AT THE NEW EXACT SHA. Do NOT start an independent audit; do NOT
qualify; do NOT install. This implementation claims NO audit PASS, NO
qualification, NO installation, and grants nothing.

## 12. Standing prohibitions

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from
an agent session; never rerun the launcher; never treat any recorded grant
phrase as a new grant; never execute a real auditor or provider/model;
never open the four sealed artifacts; never relabel or rewrite historical
model identities, runs, records, matrices, prompts or evidence workspaces
(append-only); never claim remediation of PCH6 findings, qualification or
installation from this implementation.
