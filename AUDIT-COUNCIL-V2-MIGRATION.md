# Audit Council v2.0 — Migration & Compatibility

## Current guidance — 2026-09-05

The historical plan below is retained for traceability, not as current install or
rollback instructions. The PreToolUse hook is now automatic and skill-scoped via
`skill/SKILL.md`; global settings registration is not required. User-facing
`prepare --mode AUTO|CURRENT|RELEASE|HISTORICAL --repo ... --ref ...` and
`--evidence-allow` are implemented. RELEASE/HISTORICAL stage source-contained,
non-denylisted authorized files into run-owned staging and link the final binding.

Installation from `579e39a409a1b6df58368a7b07dbdbbed5839dd9` was recorded as verified
on 2026-09-05. Currently installed files match newer
`8ae33444f349ce73c1359b963722e2d16acba630`; independent qualification of that newer
installation is unresolved. See [qualification history](docs/chatgpt-project/AUCDEV-QUALIFICATION-HISTORY.md).

For any future upgrade/rollback, select an exact qualified source first, preserve
the existing installed tree, export the selected `skill/` into a separate temporary
directory, compare its whole manifest including hooks, then perform only the
authorized installation and installed-copy checks. Do not use the old plan's
`git checkout ... -- skill/` against the active development tree. The observed
v1.0.3 rollback directory is identified in qualification history; no rollback occurs here.
Historical run bytes remain immutable; legacy conversion is in-memory only.

Production worktree creation uses environment_manager's XDG_DATA default. The
artifact_layout API retains a different XDG_CACHE default; AUCDEV-013 tracks that
contract debt. This task migrates no runtime or historical directory.

## Historical migration plan (2026-09-04; superseded where noted above)

Date: 2026-09-04. Principle: finalized history is never rewritten; v2
reads v1 everywhere through deterministic in-memory migration; new runs
are strictly v2.

## v1.0.3 artifact compatibility (verified by tests)

- **Evidence model**: v1 `lines: "N" | "N-M"` artifacts validate through
  `evidence_migration.migrate_artifact` IN MEMORY
  (`audit_council._validate_artifact_file`); on-disk bytes are byte-for-
  byte unchanged (test_migration_compat.py). Multi-range strings
  (`"184-185, 240-273"`, the Fifth failure) remain INVALID everywhere —
  they are never comma-parsed; v2 emits typed `line_ranges` instead.
- **Scope guard (H.4 F5)**: the legacy reader applies ONLY to v1-era runs
  (state without `env_binding_digest`). A v2 run cannot introduce legacy
  `lines` artifacts.
- **Old metrics**: v1 `99-run-metrics.json` shapes (including
  Benchmark 001's zero-invocation pre-1.0.3 form) are read as-is; v2
  rebuilds derive from job records + budget omissions; nothing
  back-computed or rewritten.
- **Old state files** (schema_version 1): load and validate unchanged;
  v2's new fields (`env_binding_digest`, `phase_skips`) are optional
  properties; readers accept both.

## State-machine semantics change (the one real behavior change)

v1 silently filled timestamps when a forward transition passed over
artifact phases (the Fifth run crossed CODEX_CROSS_EXAM_COMPLETE with no
32- artifact and no record). v2 REFUSES such transitions unless each
passed-over phase has an explicit reason-carrying record:
`advance --skip PHASE='reason'` (persisted in `state.phase_skips`;
adjudication keeps its dedicated `adjudication_skipped` rule;
resume-check honors recorded skips). Runs that legitimately finalize past
quota-deferred Codex stages must now say so — that is the point.

## CLI surface

Unchanged for users: `/audit-council <brief>`, inline briefs,
`--resume <run-dir>`. New deterministic subcommands: `verify-env`,
`describe --json`. `advance` gains `--skip` (required only for jumps).
Briefs may OPTIONALLY declare authority via a fenced ```json
`{"target": {"repository_root": ..., "expected_head": ...}}` block; all
prose paths are inert text.

## Runtime/cache roots

Active-run registry + disposable worktrees/evidence/archive roots are
injectable: `AUDIT_COUNCIL_CACHE_HOME` (default
`${XDG_CACHE_HOME:-~/.cache}/audit-council/`), `AUDIT_COUNCIL_ENV_ROOT`
(default `${XDG_DATA_HOME:-~/.local/share}/audit-council/worktrees`).
Project-local `audit-output/audit-council/` remains the default run
artifact location; NOTHING existing is relocated (see
MIGRATION-RETENTION-RECOMMENDATION.md — recommendation only, operator
approval required to act).

## Installed-skill upgrade / rollback (NOT yet performed)

Upgrade (release qualification only): copy the build tree to
`~/.claude/skills/audit-council/`, `diff -rq` byte-identity excluding
`__pycache__`, run the full suite IN the installed copy, verify fresh
discovery + `describe --json`. Rollback: `git checkout v1.0.3-baseline --
skill/` in the dev tree and reinstall that tree (verified byte-identical
to the currently installed v1.0.3). Existing audit/benchmark dirs are
never deleted by upgrade or rollback.

## Optional operator opt-in: the path-guard PreToolUse hook

One-time registration in `~/.claude/settings.json` (README §v2.0): with
no active run the hook exits 0 (zero session impact); during a run it
denies out-of-root tool calls before execution. Runner-enforced (not OS);
see KNOWN-LIMITATIONS for its honest boundary.
