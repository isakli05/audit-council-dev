# Audit Council v2.0 — Implementation Report

> Dated implementation history with later appendices, retained as evidence.
> Early “not installed”, “not replayed”, “local only” and 523-test claims are
> superseded for current-state purposes by later sections and
> [CURRENT-STATE](docs/chatgpt-project/AUCDEV-CURRENT-STATE.md).
> The last committed installation record cites 579e39a; current installed files
> match newer 8ae3344. Their independent v2.0.1 qualification reference remains
> unresolved; see [qualification history](docs/chatgpt-project/AUCDEV-QUALIFICATION-HISTORY.md).

Date: 2026-09-04. Program lead: ZCode/GLM-5.3 session (this worktree).
Baseline: v1.0.3 (tag `v1.0.3-baseline`, 160 tests). Final state:
**523 tests, OK (~64 s)**; `eval tier1` overall READY, ENVIRONMENT 1.0
(27/27), HARNESS 523/523. Zero real model calls were made for any of this
work; Benchmark 001 and the Fifth audit were never re-run and never
modified (read-only evidence; tier-3 replay of them is approval-gated code
that has NOT been executed).

## Commits (local only; no remote, no push)

    1a90237 baseline (v1.0.3 + Phase 0 artifacts)        372feaf h4 round-4 fixes
    cdbd4c8 PKG-A0    eafcf7b PKG-SCHEMA                 3f277a5 h4 round-3 fixes
    b23b030 A0.6 wiring                                  1810137 h4 round-2 fixes
    be98dd1 PKG-TELE  1b28442 PKG-ENV + PKG-EVID         04dbb9d h4 round-1 fixes
    a63f1de PKG-PUB + PKG-EVAL   296a003 PKG-SPEC
    3324632 PKG-INT (H.1–H.3)

## Execution model (MAO)

Lead reconstructed architecture and froze contracts (Phase 0 docs), then
delegated bounded packages to fresh sub-agents with exclusive write sets:
PKG-A0 (113 tests), PKG-SCHEMA (34), PKG-ENV (48), PKG-EVID (44), PKG-PUB
(14), PKG-EVAL (27), PKG-SPEC (36). PKG-TELE, A0.6 lifecycle wiring, and
PKG-INT were implemented by the lead (tightly coupled shared files). The
lead ran every integration checkpoint (full suite after each wave), fixed
all cross-package seams, and committed all work. Four independent
adversarial verification rounds were dispatched to fresh agents (H.4).

## What was built (pillar → deliverables)

- **A0**: `scripts/env_binding.py` (AuditEnvironmentBinding per
  ARCHITECTURE §3.4.1; digest excludes `binding_digest`+`frozen_at`),
  `scripts/path_guard.py` (canonicalize/containment/compound-command
  segmentation), `hooks/path_guard_hook.py` (PreToolUse deny-before-exec,
  registry-pinned), `schemas/env-binding.schema.json`; gate wired into
  `init-run` (capture+register), `advance` (refuses inference phases),
  `freeze-contract` (root/head authority), `verify-env` CLI,
  `resume-check` (reconstruct+re-register), `codex_runner start` (zero
  launches on env failure); `state.env_binding_digest` pins the binding;
  worktree-aware `repo_root_from` (git plumbing only; the legacy
  `.git`-directory sniffing is gone).
- **G**: typed `line_ranges` in all 5 finding-bearing schemas (8 inline
  locations), `scripts/evidence_migration.py` (no comma parsing, ever),
  reversed-range gate rejection, v1 in-memory reader scoped to v1-era
  runs, on-disk bytes never rewritten; the Fifth run's exact
  `"184-185, 240-273"` payload now validates end-to-end (wire→canonical).
- **E**: `_finalize_elapsed` on every terminal classification (QUOTA/
  AUTH/FAILED/INVALID_OUTPUT/CANCELLED/COMPLETE), `scripts/budgets.py`
  (v1-identical defaults + specialist caps + `record_omission`),
  `budget_omissions` re-derived into metrics idempotently; repair now
  consumes governor attempts and refuses COMPLETE jobs.
- **B**: `scripts/evidence_store.py` (EvidenceRecord, content addressing,
  visibility classes across the independence barrier, FRESH_REQUIRED
  never served, finding-shaped payload rejection, access log),
  `schemas/evidence-record.schema.json`.
- **A1/A2**: `scripts/environment_manager.py` (AUTO/CURRENT/RELEASE/
  HISTORICAL, detached worktrees, allow/deny-listed evidence staging,
  archive-before-remove with atomic swap, git-only worktree removal,
  dry-run-default cleanup), `scripts/artifact_layout.py`,
  `schemas/environment-record.schema.json`, `MIGRATION-RETENTION-
  RECOMMENDATION.md` (doc only — nothing reorganized).
- **C**: `scripts/specialists.py` (pre-frozen activation BEFORE first-pass
  completion, model-found-bug reasons rejected, blind context scrubbing,
  budget integration), `schemas/specialist-review.schema.json` (no verdict
  field anywhere), `prompts/specialist-domain-review.md`. DEFAULT OFF —
  zero lifecycle imports; `discovered_by` extended to
  `SPECIALIST-<domain>` (additive pattern; changelog recorded).
- **D**: `eval/scoring.py` (six dimensions; ENVIRONMENT hard-gated at
  100%; novel-finding truth rule — model agreement is never truth),
  `eval/tier1_harness.py`, `eval/tier2_fixtures.py` (10 seeded fixtures
  with sealed ground truth outside auditor context; telltales stripped),
  `eval/tier3_replay.py` (approval-gated, zero-access refusal),
  `eval/eval_cli.py`.
- **F**: `PUBLIC-CONTRACT.md`, `schemas/public-contract.schema.json`,
  `audit_council.py describe --json` (protocol_version 2.0) with drift
  tests (completeness enum, taxonomy, budgets mirror, no internals leak).
- **H**: explicit `phase_skips` (`advance --skip PHASE='reason'`; the
  state machine refuses silent passes over artifact phases),
  `INVALID_AUDIT_ENVIRONMENT` completeness state, SKILL.md/protocols/
  README v2 guidance, migration-compat tests, finalize checksum gate.

## Independent adversarial review (H.4) — rounds 1-4 of an eventual six

Round 1 (FAIL): 2 HIGH (path-guard interpreter/flag smuggling; tier-2
ground truth embedded in fixture source) + 6 MEDIUM (resume-check vs
skips; repair governor bypass; v1-fallback over-acceptance; env gate
fail-open on binding deletion; unkeyed integrity; phantom attempt bump).
All fixed in 04dbb9d + regression tests.

Round 2 (FAIL): all 8 confirmed RESOLVED; new: HIGH availability
regression (relative multi-component paths denied), HIGH hook self-DoS
(skill CLI blocked), MEDIUM encoded payloads (documented), bare `$VAR`/`~`
gap, binding substitution, tier-2 residual telltales. Fixed in 1810137.

Round 3 (FAIL): round-2 items resolved; new: HIGH write-access to the
guard machinery itself, HIGH repo-planted bare-symlink operands, MEDIUM
unanchored hook policy source. Fixed in 3f277a5.

Round 4 (FAIL): bare-symlink fix RESOLVED, registry pin RESOLVED;
write-variant family partially bypassed (quoted/dd of=/-t/editors/rm/mv/
ln/-c payloads) + HIGH bootstrap hole (forged state → finalize disarms
hook) + hook crash-open. Fixed in 372feaf: mutating tools may never name
harness paths; interpreter `-c` payloads may never contain harness
strings (the harness CLI's file-based invocation stays allowed); finalize
requires checksum integrity before unregistering; the hook fails closed
(with a stdlib-only fallback) whenever its guard modules are damaged and a
run is active.

**Verification status after the qualification sessions: SIX adversarial
rounds total (rounds 5 and 6 documented in the sections below), every
finding resolved with regressions (tests/test_review_hardening.py +
tests/test_codex_sandbox.py). Round-6 issues were fixed and reverified by
the same round-6 verifier.** The residual
escape classes that remain are inherent to a no-inference lexical layer
and are documented in AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md.

## Explicit answers

- Did any project/source file get modified outside the dev tree? **NO**
  (verified: `skill/`, `~/.claude/skills/audit-council/`, and both
  historical run trees untouched; only `/home/isa/audit-council-dev/**`
  and `/tmp/audit-council-review-*` written).
- Real Claude/Codex calls during implementation? **ZERO** (budget
  unchanged; no smoke A needed — the wire path is proven deterministically
  with the real Fifth payload).
- Installed skill updated? **NO** — installation is the operator-gated
  release-qualification step (H.5) and has NOT run.
- Historical runs rerun? **NO.**
- Final deterministic gates: full suite **523/523 OK**; `eval tier1`
  **READY** with ENVIRONMENT 1.0.


## Release-qualification round (2026-09-04, later session)

Operator-identified gaps closed (commits 4e53533, b7d081e, 29c89cb,
85d8634, 3d1a9c, 3e949ff):

1. **docs/A0-CODEX-CONFINEMENT.md delivered** — codex 0.153.0 probed
   deterministically (`codex sandbox`: outside reads SUCCEED under the
   stock sandbox; writes blocked): the stock sandbox is write-only
   enforcement. A bubblewrap OS boundary was implemented
   (scripts/codex_sandbox.py) and wired into EVERY codex launch (fresh +
   resume + repair): repo ro, run dir rw, ~/.codex rw, real toolchain
   roots ro, system dirs ro, /tmp fresh tmpfs, network preserved
   (subscription login verified INSIDE the wrapper). Reads outside the
   bind set are OS-BLOCKED (regressions: tests/test_codex_sandbox.py).
2. **Environment manager is user-facing**: `audit_council.py prepare
   --repo <src> --brief <b> [--mode M] [--ref <sha>] [--evidence-allow
   list]` = detached worktree at the exact HEAD + frozen binding for THAT
   worktree + authorized-evidence staging + run creation in one command;
   finalize archives before `git worktree remove`. Eight E2E proofs in
   tests/test_env_prepare_e2e.py (exact HEAD, live tree untouched,
   same-HEAD substitution blocked by a run-location identity check,
   record linkage, archive-before-remove, resume identity, allow/deny
   enforcement, AUTO-safety).
3. **Claude confinement is automatic and skill-scoped**: SKILL.md
   frontmatter now declares the PreToolUse hook (Bash/Read/Grep/Glob →
   hooks/path_guard_hook.py, `${CLAUDE_SKILL_DIR:-default}` resolution) —
   registered when /audit-council is invoked, inert without an active
   run. No operator settings setup required.
4. **Contract accuracy**: describe --json + PUBLIC-CONTRACT.md carry an
   exact enforcement map (OS-enforced / pre-tool mechanically denied /
   runner policy/detection / not enforced·accepted residual); the
   "session-opt-in" and "runner-enforced read confinement" overclaims
   are gone (drift-tested).
5. **Round-5 independent verification** (fresh agent): FAIL(narrow) →
   both blockers fixed (HISTORICAL evidence staging now realpath-resolves
   every entry — in-repo symlinks can no longer stage host files or
   deny-listed content; active-run registry gained dead-entry GC and the
   eval harness isolates its cache; 1,942 polluted real-cache entries
   purged, 0 alive) plus NEW-1/2/4/7 lows (codex-bin file-bind only,
   run-dir realpath containment at wrap time, Glob pattern prefix check,
   scorer path normalization) — all with regressions.
6. **Fake-model Tier-2 scoring harness** (eval/tier2_scoring.py,
   `eval_cli.py tier2-score`): scripted artifacts derived from sealed
   truth driven through the REAL state machine — 10/10 fixtures
   recall = precision = 1.0, protected controls 0 violations, seeded
   false positive rejected in-pipeline (tests/test_tier2_scoring.py).

## Round 6 (final gate, this session)

Fresh read-only verifier, scoped to the post-round-5 changes: two
Medium issues found (Glob post-metachar/brace escapes; test-suite
cache leakage bricking the auto-hook with dead registrations) + one
LOW (scorer symlink alias) + two nits. ALL FIXED: per-chunk Glob
confinement; cache isolation in every test/harness init-run spawner
(in-process ones included) with a suite-level real-cache-cleanliness
regression; scorer realpath normalization; clean exit-3 refusals for
wrap-time containment violations; tool-file bind ordered after the
/tmp tmpfs. Fixes reverified by the same round-6 verifier (PASS).

Final state: **555/555 tests OK**; `eval tier1` **READY,
ENVIRONMENT pass_fraction 1.0**; the real user cache stays EMPTY after
the full suite. Tier-3 replay of Benchmark 001 + the Fifth run was
executed under explicit operator authorization from RECORDED ARTIFACTS
ONLY (read-only; no re-audit; no new inference). Still NOT done
(operator gates): installation (the installed ~/.claude skill is stale
v1.0.3 WITHOUT hooks/ — shipping hooks/ is mandatory at install time),
real-model tier-2, any new real inference.

## Installation (2026-09-05, operator-approved)

INSTALLATION_VERIFIED. Source: dev HEAD 579e39a (git archive — wholesale,
no overlay). Installed: ~/.claude/skills/audit-council/ (hooks/ shipped).
Rollback: ~/.claude/skills/audit-council.v1.0.3-rollback-20260905/
(byte-identical to tag v1.0.3-baseline). Validations: tree identity
(only dev-side untracked test debris differs — installed == HEAD);
required v2 files all present; installed-copy suite 555/555 OK with
real cache left empty; describe --json 2.0 — all seven contract checks
(RELEASE/HISTORICAL, line_ranges, INVALID_AUDIT_ENVIRONMENT, automatic
skill-scoped hook, bwrap confinement, ~/.codex auth residual disclosed);
hook byte-identical + inert with no active run (rc 0) — 12 unrelated
interactive codex processes were running (freelance-project-assessment
cwds; zero audit-council associations) and were untouched; bwrap 0.12.0,
codex-cli 0.153.0, ChatGPT login OK; deterministic discovery (frontmatter
name/model/hooks + path) green; INVALID_AUDIT_INPUT fast-fail rc=1.
No real inference; LCO/historical artifacts untouched (0 files modified
under benchmarks; audits tree mtime-preserved). Not done (per orders):
LCO re-audit, real-model Tier-2, historical reruns, push/publish.
