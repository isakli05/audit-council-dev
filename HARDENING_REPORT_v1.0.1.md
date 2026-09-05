# Audit Council — v1.0.1 Hardening Report

> Historical version-specific evidence; retained unchanged below.
> For today's installed identity and residuals see [current state](docs/chatgpt-project/AUCDEV-CURRENT-STATE.md).

Date: 2026-09-03. Baseline: v1.0.0 delivery (see IMPLEMENTATION_REPORT.md).
Directive: focused hardening pass on four post-delivery review issues; no redesign,
no new features, no large real-model runs.

## Issue 1 — Artifact repository fingerprint now semantically validated — FIXED

JSON Schema only checked SHA syntax; a model could emit an arbitrary
`repository_fingerprint_sha256` (e.g. `aaa…`) and still be accepted. The real smoke
run had demonstrated exactly this (frozen `3f8ee2…` vs artifact `aaa…`).

Fix: `audit_council.py` gained `FINGERPRINT_FIELDS` + `_fingerprint_mismatches()` and a
dedicated exit code `9 = EXIT_INVALID_ARTIFACT`. The invariant
`artifact fingerprint == state.json:repo_fingerprint_sha256` is enforced on every
artifact-bearing path:

- `freeze-contract` (contract `target_repository.fingerprint_sha256`)
- `advance` for 10/20/90 (top-level field), after schema validation, before checksum +
  transition — mismatching artifacts never become canonical
- `resume-check` completed-artifact loop (exit 9) AND the auto-advance fast path (a
  staged wrong-fingerprint artifact is not silently advanced)
- `codex_runner wait` classification: a Codex output claiming a different fingerprint is
  `INVALID_OUTPUT` (exit 6, `INVALID_ARTIFACT:` in the job's `error` field), raw output
  preserved, stage NOT counted (retry stays possible), session id still persisted

Fail-closed: unloadable state ⇒ frozen=None ⇒ any claim mismatches. No silent
replacement or auto-correction ever occurs.

## Issue 2 — Smoke documentation corrected to match the canonical artifact — FIXED

Verified from artifacts: the canonical smoke run (`20260903T180532Z-bbc9b3`) contains
exactly ONE finding (`CODEX-001`, "average propagates unhandled exceptions for invalid
inputs", MEDIUM); the earlier REJECTED run (`…180054Z-24178a`) had two. The delivered
record had conflated them. SMOKE_TEST_RECORD.md now states the canonical count, explains
the miscount, and documents the fingerprint defect this pass fixes. No CODEX-002 was
fabricated; preserved artifacts untouched. A consistency test
(`test_v101_hardening.TestSmokeDocConsistency`, skip-guarded off-machine) compares the
record's finding ids and count against the canonical JSON artifact.

## Issue 3 — Inline audit brief genuinely implemented (Option A) — FIXED

Docs claimed inline briefs; scripts required a file path. Implemented the clean CLI
contract: `--brief-inline` (stdin) on both `preflight` and `init-run`, mutually exclusive
with `--brief`; a nonexistent `--brief` path is an explicit error, never reinterpreted
as inline text; neither-flag invocations get a clean JSON error (no traceback). Inline
content is read and validated BEFORE any run dir is created (no stray skeletons), then
materialized to the immutable run-owned `inputs/original-audit-brief.md`, checksummed
into `checksums.sha256`, and referenced by `00-run-manifest.json`
(`brief_source: "inline"`, `brief_path` = run-owned copy) so resume never depends on the
original shell argument. Quoted/multiline/`$`/backtick content is handled byte-exact.
SKILL.md startup parsing + Phase 0 instructions and README (incl. quoted usage example)
match the implementation exactly.

## Issue 4 — Write-guarantee documentation distinguishes prevention from detection — FIXED

Investigated Claude Code capabilities: no robust, portable, non-destructive way exists to
mechanically prevent Bash-driven writes while keeping the arbitrary read-only inspection
the audit needs; deny-lists cannot enumerate mutating commands, and chmod/chattr/mount
tricks were rejected as unsafe for user repositories. Outcome B taken: SKILL.md and
README now state verbatim-level semantics — Codex repository writes are mechanically
PREVENTED by its read-only sandbox; Claude mutation is prohibited by protocol + disabled
editing tools (Edit/Write/NotebookEdit), while per-phase write-guards and the frozen
fingerprint DETECT unexpected mutations and halt the audit ("detection, not an OS-level
sandbox"). Doc-consistency tests assert the wording and the absence of Claude-side
OS-sandbox claims. Behavior tests (artifact writes allowed; mutation detected; dirty
tree not misattributed; nothing reset/deleted; violation halts) were already green and
remain so.

## Full test suite

`python3 -m unittest discover -s tests` → **114 tests, OK, ~14.4 s** (was 94 tests in
v1.0.0; +18 hardening tests, +2 runner fingerprint tests). Per-module:
hardening 18 / 2.8 s · runner-mock 26 / 4.9 s · state-store 15 / 0.1 s · fingerprint 8 /
1.3 s · write-guard 6 / 1.7 s · schema 12 / 0.1 s · resume 9 / 2.2 s · normalization 20 /
1.3 s. The reported ">5 min" full-suite runtime did not reproduce (≈14 s here). The
runner's wait poll interval is now `CODEX_RUNNER_POLL_INTERVAL` (default 2.0 s, clamped
to [0.01, 2.0], unparseable falls back to 2.0); tests set 0.02 s. Production timing is
unchanged. Remaining runner-test time is real subprocess-spawn cost, kept for fidelity.

## Independent patch review

An independent reviewer attempted to falsify each fix and probed the CLI directly.
Verdict: **Issue 1 VERIFIED_FIXED, Issue 2 VERIFIED_FIXED, Issue 3 VERIFIED_FIXED,
Issue 4 VERIFIED_FIXED — no regressions** (governor success-count semantics,
quota-resume + 3-attempt cap, structured-output validation, session persistence on
failure, late-finding enforcement, write-guard, checksum-tamper exit 8, collision-safe
run ids all re-verified). Its actionable findings were resolved:

- missing hardening report / stale "94 tests" records → this document + report updates
- no-brief invocation traceback → clean JSON error (both subcommands)
- no automated runner fingerprint-rejection test → added (2 tests)
- INFO: `advance --to COMPLETE` could jump over FINALIZED → now guarded (COMPLETE only
  from FINALIZED; the honest `finalize` path is required)
- INFO: empty inline brief left a stray run-dir skeleton → stdin read/validation moved
  before any directory creation
- INFO: argument-hint omitted inline form → updated

Known accepted quirk (documented): the preserved v1.0.0 smoke run still contains its
original wrong-fingerprint artifacts; resume-check on it now correctly refuses (exit 9)
— history was not retroactively mutated.

## Quota consumption

Zero real Claude/Codex model calls in this hardening pass. All validation was
deterministic (unit/CLI probes with fake codex and synthetic git fixtures).

## Files changed (v1.0.1)

- skill/scripts/audit_council.py — fingerprint invariant + EXIT_INVALID_ARTIFACT +
  brief-inline + COMPLETE guard + clean no-brief errors
- skill/scripts/codex_runner.py — fingerprint check in classification + poll-interval
  env
- skill/SKILL.md, skill/README.md — inline brief usage; prevention-vs-detection wording;
  argument-hint
- skill/tests/test_v101_hardening.py (new, 18), test_codex_runner_mock.py (+2),
  fixtures/fake_codex.py (FAKE_CODEX_FINGERPRINT), test_resume.py +
  test_disagreement_normalization.py (use real run fingerprints)
- SMOKE_TEST_RECORD.md corrected; this report; IMPLEMENTATION_REPORT.md v1.0.1 note
- Installed copy refreshed: `~/.claude/skills/audit-council/` (verified byte-identical
  to the build tree; installed suite 114/114 OK)
