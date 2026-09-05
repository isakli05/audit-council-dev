# Audit Council — v1.0.2 Runner Robustness Hardening

> Historical version-specific evidence; retained unchanged below.
> For today's installed identity and residuals see [current state](docs/chatgpt-project/AUCDEV-CURRENT-STATE.md).

Date: 2026-09-03. Scope: ONE narrowly-scoped detached-process lifecycle fix in
`codex_runner.py::cmd_wait`. No architecture change, no new features, no real model calls.
After this fix, Audit Council v1 is FROZEN for real-world benchmark evaluation.

## Defect (independently reproduced)

`cmd_wait()` gated completion on `proc_alive(pid) == False`. `proc_alive` uses
`os.kill(pid, 0)`, which SUCCEEDS for zombie (terminated, unreaped) processes. A finished
Codex subprocess whose wrapper had already persisted the real exit code was therefore
reported RUNNING until timeout. This is environment-dependent (PID 1 reaping policy) and
could hang the deterministic suite in some containers.

## Fix

The wrapper-generated `job["exit_code_path"]` is now the PRIMARY, portable, authoritative
completion signal (`read_exit_code_once()` — single non-blocking read; empty/partial file
→ treated as absent, no crash). Liveness is SECONDARY: when the process is truly gone,
the existing bounded grace loop (`read_exit_code`, 20 × 0.2 s) recovers a late-written
code; a code that never appears finalizes through the normal failure classification
(`exit_code: null` → FAILED). Timeout still yields RUNNING (exit 7). No `/proc` zombie
detection, no busy polling; the poll interval stays clamped to [0.01, 2.0] s with the
2.0 s production default unchanged. `cmd_cancel`'s bounded wait now also breaks
immediately when the exit-code file exists, so it no longer spends 5 s signaling an
already-dead zombie (still ≤ 5 s, always records CANCELLED).

A zombie process with an already-persisted exit code is FINISHED, not RUNNING.

All classification semantics preserved: COMPLETE / INVALID_OUTPUT / FAILED / QUOTA /
AUTH_ERROR / RUNNING with their CLI codes (0/6/1/2/3/7); structured-output and
repository-fingerprint validation untouched; raw-output preservation, session-id
persistence on failure, quota-retry and budget-governor (success-count) semantics,
telemetry, explicit-session resume, and read-only sandbox flags all unchanged.

## Tests

New `tests/test_wait_lifecycle_v102.py` — 9 deterministic tests, zombie conditions
simulated by mocking `proc_alive` (no OS zombies required):

1. exit-code file present + PID "alive" (zombie) → COMPLETE, not RUNNING
2. quota mode under zombie liveness → QUOTA (exit 2), stage not counted
3. auth mode under zombie liveness → AUTH_ERROR (exit 3), stage not counted
4. crash mode under zombie liveness → FAILED (exit 1)
5. genuinely running process (5 s fake sleep vs 1 s timeout) → RUNNING (exit 7)
6. reaped process + persisted exit file → finalizes via secondary path
7. reaped process + exit file lost → grace exhausts → FAILED (exit 1, null code)
8. zombie liveness + no exit file (no authoritative signal) → RUNNING (exit 7)
9. grace-loop race: exit file written ~0.5 s after process gone → recovered and
   finalized correctly

Reverting the fix (gating on `proc_alive == False`) makes the zombie-pinned tests fail
— the defect is regression-pinned.

## Verification

- Full deterministic suite: **123 tests, OK, ~21.8 s** (121 before review fixes; the two
  added grace-path tests bring real ~4 s / ~0.6 s waits by design).
- Classification modules independently: `tests.test_codex_runner_mock` (26) OK,
  `tests.test_wait_lifecycle_v102` (9) OK.
- Independent lightweight patch review: **PASS** — false completion OK (wrapper writes
  the code as its last action; per-job filenames; pre-cleared at launch), races OK
  (empty-read → absent; late-file recovered; exit 0 still fully validated), cancel OK
  (bounded, never loses CANCELLED), classification unchanged, RUNNING semantics OK, no
  busy polling. Its actionable findings were resolved: the misnamed/duplicated grace
  test was replaced with real gone+no-file → FAILED coverage; the grace loop's
  late-written-code race got a dedicated test; file handles closed and temp dirs
  cleaned up. Accepted-and-documented: the gone-process grace path is bounded to 4 s
  even when `--timeout` is smaller (finalizing beats a spurious RUNNING); a pre-existing
  (out-of-scope) PID-reuse hazard in cancel's unconditional group SIGTERM.
- Real Claude/Codex model calls during this patch: **0**.
- Installed copy refreshed: `~/.claude/skills/audit-council/` — verified byte-identical
  to the build tree; installed suite 123/123 OK.

## Files changed

- `skill/scripts/codex_runner.py` — `read_exit_code_once` (primary signal),
  `read_exit_code` grace loop refactor, `cmd_wait` reordering (exit-code → liveness →
  deadline), `_poll_interval` helper, `cmd_cancel` exit-code-aware break
- `skill/tests/test_wait_lifecycle_v102.py` — new (9 tests)
- Installed copy refreshed; this report; v1.0.2 note in IMPLEMENTATION_REPORT.md

**Audit Council v1 is now feature-frozen.** No further feature development or
speculative hardening; next step is real-world benchmark evaluation.
