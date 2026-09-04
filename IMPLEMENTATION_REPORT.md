# Audit Council — Final Implementation Report

Date: 2026-09-03. Spec: `/home/isa/audit_council_skill_prompt.md` (authoritative).

> **v1.0.1 hardening note (2026-09-03):** this report describes the v1.0.0 delivery.
> A subsequent hardening pass added the repository-fingerprint semantic invariant
> (INVALID_ARTIFACT), genuine inline-brief support (`--brief-inline` materialized to
> `inputs/original-audit-brief.md`), corrected smoke-record finding counts, and
> prevention-vs-detection write-guarantee wording. The test suite is now **114 tests,
> OK (~14 s)**. See `HARDENING_REPORT_v1.0.1.md` for details; where the two documents
> differ, the hardening report is current.
>
> **v1.0.2 note (2026-09-03):** a runner-robustness fix made the wrapper-persisted
> exit-code file the primary Codex completion signal (zombie processes no longer read
> as RUNNING). Suite: **123 tests, OK (~22 s)** — see `HARDENING_REPORT_v1.0.2.md`.
>
> **v1.0.3 note (2026-09-04):** harness-correctness fixes from the first real
> historical benchmark: a deterministic wire↔canonical adapter (canonically optional
> properties are wire-nullable; `lines: null` canonicalizes to omission; canonical
> validation remains the final authority) and attempt-based telemetry (every real
> Codex inference attempt is counted with usage even when its artifact is rejected;
> per-job logs can never overwrite; metrics rebuild idempotently from job records).
> Suite: **160 tests, OK (~25 s)** — see `HARDENING_REPORT_v1.0.3.md`.

## Installed path

`~/.claude/skills/audit-council/` (personal skill, all projects). Build tree:
`/home/isa/audit-council-dev/skill/` (identical). Records: `SMOKE_TEST_RECORD.md`,
`CONTRACTS.md` in `/home/isa/audit-council-dev/`.

## Architecture

The Claude Code session running SKILL.md IS the Opus reasoning engine (no nested
`claude -p`). Deterministic machinery lives in stdlib-only Python scripts:

- `scripts/audit_council.py` — run lifecycle CLI: `preflight`, `init-run`,
  `freeze-contract`, `advance [--artifact - --stdin]`, `verify-repo`, `write-guard`,
  `resume-check`, `render`, `finalize`.
- `scripts/codex_runner.py` — Codex process lifecycle: `start [--session ID]
  [--prompt -]`, `wait` (RUNNING/COMPLETE/FAILED/QUOTA/AUTH_ERROR/INVALID_OUTPUT),
  `status`, `result`, `cancel`, `repair` (once per phase). Detached subprocess (own
  session), prompt file as stdin, JSONL/stderr to run-owned logs, PID+argv+exit-code
  persistence for re-attach after restart.
- `scripts/state_store.py` — atomic writes, run IDs, forward-only state machine with
  adjudication-skip rules, checksums.sha256.
- `scripts/repo_fingerprint.py` — HEAD/branch/porcelain/tracked-inventory/untracked
  capture + verify (audit-output/ excluded from change detection).
- `scripts/validate_artifact.py` — minimal JSON Schema validator + ledger/final/late-
  finding invariants.
- `scripts/render_report.py` — deterministic markdown rendering (independent, ledger,
  final with all §25 sections + provenance lines).
- 8 JSON schemas, 8 protocol documents, 3 Codex prompt templates, README, SKILL.md
  orchestrator (<250 lines, per-phase protocol loading).

## Versions and model configuration

- Claude Code 2.1.259. Skill frontmatter: `model: claude-opus-5`,
  `disable-model-invocation: true`, `disallowed-tools: Edit, Write, NotebookEdit,
  AskUserQuestion`, `allowed-tools: Read, Grep, Glob, Bash`.
- Codex CLI 0.152.1. Fresh: `codex exec -C <repo> --model gpt-5.6-sol --sandbox
  read-only --json --output-schema <strict-variant> -c 'model_reasoning_effort="xhigh"'
  -o <out> -`. Resume: `codex exec resume <explicit-id> --model gpt-5.6-sol ... -c
  'sandbox_mode="read-only"'` (D1).

## Auth/billing safeguards

Preflight fails on: ANTHROPIC_API_KEY present (PAYG Claude risk), OPENAI_API_KEY /
CODEX_API_KEY present (PAYG Codex risk), `codex` missing, `codex login status` non-zero
or API-key mode, missing required `codex exec` flags, gpt-5.6-sol absent from the codex
models cache. Only key PRESENCE is ever read/printed; no credential values anywhere. No
API keys created; no global Claude/Codex config modified.

## Autonomous Codex mechanism

Direct `codex exec` / `codex exec resume <stored-session-id>` only. Never `--last`,
never bypass/danger flags (hard-refused in `compose_argv` + tests). No dependency on the
OpenAI Claude Code plugin (optional manual fallback only). The user only invokes
`/audit-council`; Claude runs bounded wait loops internally.

## State machine / checkpoint / resume

CREATED → PREFLIGHT_COMPLETE → CONTRACT_FROZEN → OPUS_INDEPENDENT_COMPLETE →
CODEX_INDEPENDENT_COMPLETE → NORMALIZED → OPUS_CROSS_EXAM_COMPLETE →
CODEX_CROSS_EXAM_COMPLETE → LEDGER_COMPLETE → [ADJUDICATION_COMPLETE | skip recorded] →
FINALIZED → COMPLETE (+ honest completeness_state via `finalize`). Every phase artifact
is schema-validated, checksummed, atomically written; completed phases immutable.
`--resume` revalidates state/checksums/fingerprint/artifacts and continues at the
earliest incomplete phase. Budget governor: ≤1 SUCCESSFUL stage per Codex phase, ≤3
total; failed/quota stages retryable on resume, hard cap 3 attempts per phase. Codex
session id persisted on every outcome (including quota/auth failure) for explicit resume.

## Repository integrity

Writes confined to `audit-output/audit-council/<run-id>/`. Fingerprint freeze +
`verify-repo` before every expensive phase (exit 4 STALE_REPOSITORY, no resets).
`write-guard` after every phase checkpoint (exit 5 on new mutations outside the run dir;
never deletes/resets). Dirty trees are audited as-is; no commits/branches/pushes ever.

## Cross-examination / adjudication / synthesis

Round 0 independent (contract frozen, no cross-leakage — the Codex independent prompt
template has no findings placeholder); Round 1 mutual falsification (verdict enums,
severity recalibration, late findings PROVISIONAL); disagreement ledger preserving
CONSENSUS/CONFIRMED_AFTER_CHALLENGE/NARROWED/REJECTED/DISPUTED/UNRESOLVED; Round 2
targeted adjudication ONLY for materially disputed/unresolved CRITICAL/HIGH clusters
(≤1 round, evidence packets, Codex resumes its session); final report built from the
adjudicated ledger only — REJECTED → appendix, UNRESOLVED HIGH → explicit unresolved
risk (machine-checked both directions), provenance on every finding, late findings
require other-model validation or stay UNRESOLVED (machine-checked at advance time).

## Tests

`python3 -m unittest discover -s tests` → **94 tests, OK** (build tree AND installed
copy). Coverage maps to spec §36 A–Z including quota/auth classification, session-id
resume, no `--last`, no danger modes, write guards, checksum-tamper resume block,
collision-safe run IDs, governor caps, disagreement preservation, rejected-exclusion,
unresolved-High visibility, credential non-logging.

## Real smoke test

PASS — see `SMOKE_TEST_RECORD.md`: skill discovery, ChatGPT-subscription Codex login,
real GPT-5.6 Sol fresh + explicit-session resume runs on the tiny fixture, read-only
verified, structured output validated, JSONL/thread-id captured, telemetry recorded.
Two genuine bugs were found and fixed by the smoke test (strict output-schema transform;
canonical validation of Codex output).

## Independent implementation audit

An adversarial review against the spec produced 13 findings. Fixed: F1 CRITICAL
(schema-validation no-op in runner — exit-0 malformed output could pass), F2 HIGH
(governor blocked quota-resume; now counts successes with 3-attempt retry cap), F3 HIGH
(adjudication prompt/schema shape drift), F4 (late-finding rule now enforced at
`advance --to FINALIZED`), F5 (partial runs without metrics can now finalize honestly),
F6 (session id persisted on quota/auth failure), F7 (write-guard every phase), F8
(verify-repo before adjudication), F9 (bounded wait loops, ≤20×540 s), F10
(severity_recalibration shape). Remaining (accepted, informational): F11 instruction-file
scan covers root + first-level dirs only; F12 finalize does not accept STALE_REPOSITORY
(stale runs stop before finalize by design).

## Known limitations

- Per-phase Claude effort override is guidance only (documented in SKILL.md).
- Independence before cross-pollination is enforced by protocol/prompt design and phase
  ordering, not by a runtime sandbox.
- Quota/auth/failed classification is stderr/stdout-pattern based; novel failure text
  classifies as FAILED (conservative).
- Codex JSONL telemetry parsing is generic; unusual shapes degrade telemetry (flagged),
  never the audit.
- Unbounded repo growth: untracked inventory records name+size only.

## Specification divergences

- D1: `codex exec resume` (codex-cli 0.152.1) has no `-s/--sandbox`; resume invocations
  use `-c sandbox_mode="read-only"`. Intent (read-only) preserved; test-asserted.
- D2: per-phase effort override not cleanly available; documented as guidance (spec §3
  permits this).
- D3: artifacts are checkpointed via `advance --artifact - --stdin` (piped heredoc)
  because Write/Edit are disallowed for the skill; functionally equivalent to §9.
- D4: Codex `--output-schema` requires OpenAI-strict schemas; the runner derives a
  strict run-local variant (all props required, patterns dropped, nullable enums →
  anyOf, `cluster_id` removed since clustering is Opus's Phase-3 job) and validates the
  OUTPUT against the canonical schema.
- D5: budget governor counts successful stages (not raw invocations) so §26 quota-resume
  works; bounded by a 3-attempts-per-phase cap. Spec §32 intent (no brute-force
  repetition) preserved.

## Exact user commands

- New audit: `/audit-council ./audit-brief.md` (or an inline brief)
- Resume: `/audit-council --resume audit-output/audit-council/<run-id>`

## Explicit answers

- Did any unrelated project/source file get modified? **NO** (only
  `~/audit-council-dev/`, `~/.claude/skills/audit-council/`, and
  `audit-output/` inside the dedicated smoke fixture).
- Is the OpenAI Claude Code Codex plugin required? **NO** (direct `codex exec` only).
- Is an OpenAI API key required? **NO** (ChatGPT/Codex subscription login).
- Is an Anthropic API key required? **NO** (Claude Pro subscription OAuth; preflight
  fails if ANTHROPIC_API_KEY is set).
- Can a normal audit run end-to-end without manual Codex relay? **YES** (runner +
  bounded wait loops; no /codex:status, /codex:result, or copy/paste anywhere).
- Was the real smoke test performed using subscription authentication? **YES**
  (Claude Pro OAuth session; Codex "Logged in using ChatGPT").
- Are all Definition-of-Done requirements verified? **YES** — all 33 items VERIFIED
  (see acceptance table below), several via real runtime evidence.

## Definition of Done (§39) acceptance

1 skill at personal path VERIFIED (installed tree) · 2 `/audit-council` recognized
VERIFIED (fresh-session invocation loaded it) · 3 Opus 5 VERIFIED (frontmatter) ·
4 no auto-trigger VERIFIED (disable-model-invocation, probe showed model-invisibility
while slash invocation works) · 5 no source modification VERIFIED (write-guard +
tests + smoke git status) · 6–8 Codex automatic/GPT-5.6 Sol/xhigh VERIFIED (argv +
tests + smoke) · 9 read-only VERIFIED · 10 independence VERIFIED (phase order +
findings-free prompt template) · 11 no copy/paste VERIFIED · 12–13 cross-exam both
directions VERIFIED · 14 session id persisted VERIFIED (smoke) · 15 explicit resume,
never --last VERIFIED · 16 disagreements preserved VERIFIED · 17 ≤1 adjudication round
VERIFIED · 18 no unlimited loop VERIFIED (governor + bounded waits) · 19–22 final
report invariants VERIFIED (machine-checked + tests) · 23 partial labelled VERIFIED ·
24 quota keeps work VERIFIED · 25 resumable VERIFIED (tests + smoke re-wait) ·
26 stale blocks resume VERIFIED · 27 metrics VERIFIED (smoke telemetry) · 28 no
credential logging VERIFIED · 29–30 PAYG detection VERIFIED · 31 94/94 tests OK ·
32 smoke PASS (subscription auth) · 33 no unrelated modifications VERIFIED.
