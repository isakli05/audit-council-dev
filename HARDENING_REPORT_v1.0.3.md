# Audit Council — v1.0.3 Hardening Report

> Historical version-specific evidence; retained unchanged below. Remaining v1
> limitations are dispositioned in the [current backlog](docs/chatgpt-project/AUCDEV-BACKLOG.md).

## Structured-Output Canonicalization & Telemetry Hardening

Date: 2026-09-04. Scope: two production harness defects found by the first real historical
benchmark (LCO-AUDIT-COUNCIL-B001, run `20260904T014146Z-f3384a`, treated READ-ONLY).
No protocol redesign, no model-role changes, no benchmark rerun, no full audit.

## Defect reproductions (before the fix)

Defect 1 — schema contradiction, reproduced deterministically: the strict wire projection
made canonically-optional `evidence.lines` a REQUIRED plain string; canonical validation
rejects `null` (type) and `""` (pattern) — no valid representation existed. The benchmark
showed all three faces: `lines: ""` (empty sentinel), `lines: "325-343, 488-547"`
(multi-range), plus a garbage fingerprint (caught by the v1.0.1 invariant). All five real
Codex attempts classified INVALID_OUTPUT → run finished PARTIAL_CODEX_FAILURE.

Defect 2 — telemetry/log coupling, reproduced from the benchmark run: five paid attempts
with usage-bearing `turn.completed` events in JSONL, yet `99-run-metrics.json` reported
zero invocations (metrics were appended only on COMPLETE); shared per-phase log paths
(`logs/<phase>.jsonl`) let the second independent attempt overwrite the first's evidence.

## A. Adapter design

New deterministic boundary `scripts/wire_adapter.py`:

- `canonical_to_wire(schema, dir)` — the only place the wire projection lives: inlines
  local `$ref`s, drops keywords OpenAI strict outputs reject (pattern, minLength, ...),
  enforces `additionalProperties: false` + all-properties-required, converts type arrays
  and null-bearing enums to `anyOf`, and makes canonically OPTIONAL properties nullable
  (null = the wire representation of "absent").
- `wire_to_canonical(doc, canonical_schema, dir)` — schema-aware normalization (see B);
  never a blind strip-nulls pass.
- `drop_wire_property_under(wire, name, containers)` — scoped removal used for
  `finding.cluster_id` (under `findings`/`late_findings` only; the adjudication
  `rounds[].cluster_id` is canonically REQUIRED and stays representable).

`codex_runner.build_codex_schema` now delegates to the adapter; the legacy in-runner
transformation was deleted.

## B. Optional/null semantics

Optional + wire null → omitted before canonical validation. Required + genuinely nullable
(e.g. `state.codex.session_id`) → null preserved. Required + non-nullable + null → ERROR
(flag-closed; the null is kept in the candidate so canonical validation rejects it too).
Unknown keys pass through so `additionalProperties: false` still rejects them. No defaults
are ever invented; null never becomes "", [], {}, 0, or false. Dropped wire constraints
are safe only because the canonical validator re-imposes them on the normalized candidate.

## C. Canonical validation ordering

exit 0 → raw preserved at the per-job `final.json` → `wire_to_canonical` → candidate
validated against the ORIGINAL canonical schema (final authority; catches `""`,
multi-ranges, minLength, enums) → repository-fingerprint semantic check on the normalized
candidate (fail-closed INVALID_ARTIFACT / FINGERPRINT_MISMATCH) → canonical sidecar written
to `<final>.canonical.json` (raw and canonical never leak into each other). A missing
canonical schema at wait time now fails CLOSED (no wire-schema fallback — review F2 fix).

## D. Telemetry data model

Every job record carries: job_id, phase, attempt_number, fresh_or_resumed, session/thread
id, started_at/completed_at/elapsed, model (gpt-5.6-sol), reasoning_effort (xhigh),
process classification (COMPLETE/INVALID_OUTPUT/QUOTA/AUTH_ERROR/FAILED/CANCELLED/RUNNING),
artifact status (NOT_PRODUCED/WIRE_VALID/CANONICAL_INVALID/SCHEMA_INVALID/
FINGERPRINT_MISMATCH/CANONICAL_VALID), successful_stage_counted, and usage tokens
(null = explicitly unknown — never fabricated zeros).

## E. Attempt vs successful-stage distinction

`_record_usage()` persists turns/tokens on EVERY terminal outcome (including INVALID_
OUTPUT, QUOTA, AUTH_ERROR, FAILED, CANCELLED); a usage-bearing `turn.completed` before a
quota failure is retained. Only COMPLETE (canonical-valid + fingerprint-ok) counts as a
successful governor stage. Governor semantics unchanged: success-count per phase ≤ 1,
total ≤ 3, failed/quota attempts retryable, hard cap 3 attempts per phase.

## F. Log naming/preservation

Per-attempt paths: `logs/<phase>.<job_id>.jsonl`, `.<job_id>.stderr.log`,
`.<job_id>.final.json` (+ `.canonical.json` sidecar); job metadata and exit codes under
`logs/jobs/<job_id>.{json,exitcode}`. Fresh, repair, resumed, and failed attempts each
keep their own files; cancel deletes nothing; resume never reuses a stale output/log path.

## G. Idempotence / resume

`99-run-metrics.json` is DERIVED state: `rebuild_metrics()` reconstructs it from
`logs/jobs/*.json` (dedup by stable job_id), invoked from terminal wait paths, cancel
(after the job record is persisted), and status. Repeated wait/status are idempotent
(no double counting, no elapsed inflation — elapsed is computed once); deleting the file
and re-running status reconstructs it byte-identically. Metrics survive process exit and
are rebuildable with state.json absent.

## H. Tests added (37 new)

- `test_wire_adapter_v103.py` (19): nullable-wire projection shapes; optional-null →
  omitted → canonical PASS; valid non-null preserved; empty-string and multi-range
  (the benchmark's exact values) FAIL canonical; required-non-null null fails closed;
  required-nullable null preserved; nested/array-item/multi-level nulls;
  additionalProperties enforcement; no-defaults; unknown-key rejection; canonical round-
  trip; scoped cluster_id drop (adjudication keeps REQUIRED cluster_id, findings drop it).
- `test_telemetry_v103.py` (18): COMPLETE counts stage+invocation; INVALID_OUTPUT counts
  invocation+usage but not the stage; fingerprint mismatch retains usage; quota-after-
  usage retains usage; AUTH/FAILED retained; repair counts both attempts with unique
  logs and one successful stage; resumed counted separately; repeated wait/status never
  double-count; restart reconstructs identical metrics; unknown usage stays null;
  totals equal the sum of usage-bearing attempts; per-job logs cannot overwrite; cancel
  preserves logs; attempt numbers increment; re-wait does not inflate elapsed; wait-after
  -cancel stays CANCELLED; cancel-after-COMPLETE does not relabel.

## I. Full test count / pass / runtime

**160 tests, OK, ~25.3 s** (build tree and installed copy). Classification/lifecycle
modules re-run independently green.

## J. Independent patch review

First review verdict: **FAIL** with one HIGH finding — my global `cluster_id` drop had
deleted the canonically REQUIRED `rounds[].cluster_id` from the adjudication wire schema
(the mocks were blind because fake_codex ignores `--output-schema`). All fixes applied
and regression-tested:
- F1 (HIGH): drop scoped to `findings`/`late_findings` via `drop_wire_property_under`;
  adjudication `rounds[].cluster_id` retained and test-asserted.
- F2 (LOW-MED): missing-canonical-schema fallback now fails closed.
- F3 (LOW): elapsed computed once; repeated waits cannot inflate it.
- F4 (LOW): re-wait on a terminal job is idempotent — CANCELLED can't relabel to FAILED.
- F5 (LOW): cancel refuses to modify an already-terminal job record.
All other review areas passed: optionality preservation (all 8 schemas), required-null
fail-closed, canonical strength (empty/malformed/unknown-key probes), recursive
normalization, fingerprint ordering, telemetry idempotence and on-failure accounting,
retry log preservation, resume reconstruction, and no regressions (write guards,
read-only sandbox argv, explicit-session resume, never `--last`, zombie exit-code
authority, checksums, stale-repo, secret-leakage guards — all re-verified by the
unchanged legacy suites, 156 pre-existing tests green).

## K. Real Codex smoke calls

Exactly ONE fresh real invocation (authorized tiny structured-output smoke):
`smoke-fixture-103`, job `independent-c370c118`, run `20260904T054559Z-5b54c7` —
GPT-5.6 Sol @ xhigh via `codex exec --sandbox read-only`, prompt required one
requirement-level finding with no line range. Result: raw wire contains `"lines": null`
(plus 9 other optional nulls), the canonical sidecar omits the field entirely,
classification COMPLETE with `artifact_status: CANONICAL_VALID`, usage recorded
(input 259,706 / cached 224,384 / output 5,034 / reasoning 3,078 tokens). This proves
the real strict-schema path end-to-end. No resumed follow-up was needed (resume shares
compose_argv + the same adapter + deterministic mock coverage). Zero real Claude calls.

Observed environment drift: Codex CLI is now 0.153.0 (was 0.152.1 at v1.0.0); the
required flag surface is unchanged and `codex exec resume` still lacks `-s` (D1 stands).
Login remains ChatGPT subscription; no API-key env vars.

## L/M. Installed path / files changed

Installed: `~/.claude/skills/audit-council/` — byte-identical to the build tree;
installed suite 160/160 OK; skill discovery verified (fresh invocation parsed arguments
and failed fast on a missing brief as designed).
Changed: `scripts/wire_adapter.py` (new), `scripts/codex_runner.py`,
`scripts/audit_council.py` (finalize note only), `tests/test_wire_adapter_v103.py` (new),
`tests/test_telemetry_v103.py` (new), `tests/test_codex_runner_mock.py` (per-job paths,
metrics shape), `tests/fixtures/fake_codex.py` (usage-first quota mode), this report,
implementation-report note.

## N. Remaining limitations

- Comma multi-range `lines` values ("325-343, 488-547") remain canonically INVALID by
  design (canonical authority); the protocol handles them via the one-shot repair or
  cross-examination, not by loosening the schema.
- fake_codex does not enforce `--output-schema` itself; wire-shape regressions are
  guarded by schema-level assertions instead (documented test blind spot, mitigated).
- `rebuild_metrics` orders equal-timestamp records by directory order (deterministic in
  practice).
- Fingerprint garbage from a model remains INVALID_OUTPUT/FINGERPRINT_MISMATCH; making
  prompts always echo the exact frozen fingerprint is protocol guidance (SKILL.md), not
  mechanically enforced.
