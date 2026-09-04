# Audit Council — Real-Model Smoke Test Record (spec §37)

Date: 2026-09-03 · Fixture: `/home/isa/audit-council-dev/smoke-fixture` (2-file git repo,
planted defect: `average([])` → ZeroDivisionError) · All tests (94) green beforehand.

## Checks and results

| §37 requirement | Result | Evidence |
|---|---|---|
| Claude skill discovery | PASS | `claude -p "/audit-council ./does-not-exist-brief.md"` loaded the skill and stopped with usage/INVALID_AUDIT_INPUT (no model spend); separate probe proved `disable-model-invocation`+`model`+`allowed-tools` frontmatter registers as user-invocable slash command |
| Codex login (subscription) | PASS | `codex login status` → "Logged in using ChatGPT"; preflight `ok: true`; no ANTHROPIC_/OPENAI_/CODEX_API_KEY in env |
| GPT-5.6 Sol via codex exec | PASS | run `20260903T180532Z-bbc9b3`, job `independent-71f15f02`, exit 0, `--model gpt-5.6-sol` in persisted argv |
| Read-only execution | PASS | fixture `git status --porcelain` clean except `?? audit-output/`; `--sandbox read-only` on fresh exec |
| Structured output | PASS | `logs/independent.final.json` validates against canonical `independent-audit.schema.json`; 1 finding (CODEX-001, "average propagates unhandled exceptions for invalid inputs", MEDIUM — includes the planted empty-list divide-by-zero), evidence with real file+line refs (`calc.py`, `test_calc.py`, `audit-brief.md`) |
| JSONL capture | PASS | `logs/independent.jsonl` (70 KB), `thread.started` + `turn.completed` parsed |
| Thread ID capture | PASS | `state.json` codex.session_id `01a06872-8f81-7042-88b5-a44a1d7db387` |
| Resume pathway | PASS | job `cross_examination-b6c95063` via `codex exec resume <explicit-id>` + `-c sandbox_mode="read-only"` (D1), COMPLETE; metrics show `resumed: true`, `resumed_count: 1` |
| Final artifact handoff | PASS | `advance --to CODEX_INDEPENDENT_COMPLETE` on the validated output succeeded |
| Usage telemetry | PASS | 99-run-metrics.json: input 225,591 (cached 189,696), output 8,257, reasoning 4,819 tok; 2 invocations, 1 fresh + 1 resumed |

Two earlier smoke attempts failed and drove real fixes: (1) OpenAI strict-schema rejection
(`additionalProperties` required false everywhere) → `build_codex_schema` strict transform;
(2) cluster_id/pattern + canonical-vs-wire validation issues → cluster_id dropped from wire
schema, canonical validation in `wait`. An earlier rejected attempt (run
`20260903T180054Z-24178a`, superseded) had produced two findings (CODEX-001/002); the
canonical accepted artifact above contains ONE finding — an earlier version of this record
miscounted it as two.

CORRECTION (v1.0.1 hardening, 2026-09-03): the canonical run-3 Codex artifact also carried
`repository_fingerprint_sha256 = "aa…"` (a placeholder echoed from the hand-built smoke
contract) instead of the frozen run fingerprint `3f8ee2…`, and was accepted because only
SHA syntax was validated. v1.0.1 adds the semantic fingerprint invariant (INVALID_ARTIFACT
on mismatch in `advance`, `resume-check`, and `codex_runner wait`), with regression tests.

Quota cost: 2 small Codex calls + 3 tiny claude -p discovery checks. No full-repo audit run.
