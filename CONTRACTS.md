# Audit Council — Shared Contracts (authoritative for all implementers)

Build root: `/home/isa/audit-council-dev/skill/` (installed later to `~/.claude/skills/audit-council/`).

Environment facts (verified 2026-09-03):
- Claude Code 2.1.259; personal skills at `~/.claude/skills/<name>/SKILL.md`; frontmatter supports `name`, `description`, `disable-model-invocation`, `model`, `allowed-tools`, `disallowed-tools`, `effort`; `${CLAUDE_SKILL_DIR}` substituted in skill body.
- Codex CLI 0.152.1 (`codex exec`, `codex exec resume <SESSION_ID>`), logged in via ChatGPT subscription, default model `gpt-5.6-sol`, `model_reasoning_effort = "xhigh"` already in `~/.codex/config.toml`.
- DIVERGENCE D1: `codex exec resume` has no `-s/--sandbox` flag. Resume invocations MUST set sandbox via `-c sandbox_mode="read-only"`. Fresh `codex exec` uses `-s read-only`.
- Python 3.14, stdlib only. No pip deps.

## Architecture

The Claude Code session running SKILL.md IS the Opus reasoning engine (no nested `claude -p`).
Python scripts provide all deterministic machinery: run lifecycle, state, fingerprinting,
Codex subprocess management, artifact validation, checksums, rendering, metrics.

## Artifact layout (inside target repo, the ONLY writable location)

    audit-output/audit-council/<run-id>/
      00-run-manifest.json        01-repository-state.json
      02-audit-contract.json      02-audit-contract.md
      10-opus-independent.json    10-opus-independent.md
      20-codex-independent.json   20-codex-independent.md
      30-normalized-findings.json
      31-opus-cross-examination.json
      32-codex-cross-examination.json
      40-disagreement-ledger.json 40-disagreement-ledger.md
      50-targeted-adjudication.json        (only when required)
      90-final-findings.json      90-final-audit.md
      99-run-metrics.json
      state.json
      checksums.sha256
      prompts/  (codex-independent.md, codex-cross-examination.md, codex-targeted-adjudication.md)
      logs/     (codex-*.jsonl, codex-*.stderr.log, jobs/<job-id>.json)

Run ID: `YYYYMMDDTHHMMSSZ-<6 hex>` (UTC). Collision → regenerate hex suffix.

## State machine (state.json)

`phase` ∈ CREATED → PREFLIGHT_COMPLETE → CONTRACT_FROZEN → OPUS_INDEPENDENT_COMPLETE →
CODEX_INDEPENDENT_COMPLETE → NORMALIZED → OPUS_CROSS_EXAM_COMPLETE → CODEX_CROSS_EXAM_COMPLETE →
LEDGER_COMPLETE → ADJUDICATION_COMPLETE → FINALIZED → COMPLETE.
`completeness_state` ∈ COMPLETE, COMPLETE_WITH_RESIDUAL_UNCERTAINTY, PARTIAL_CODEX_QUOTA,
PARTIAL_CODEX_FAILURE, PARTIAL_CLAUDE_INTERRUPTION, STALE_REPOSITORY, INVALID_AUDIT_INPUT,
RUNNING (initial). Transition rules: forward-only along the chain (ADJUDICATION_COMPLETE may be
skipped when ledger has no eligible disputes — skipping is recorded via `adjudication_skipped: true`);
every transition validates the phase's artifact exists, parses, validates against its schema, and
matches checksums.sha256. Completed phases are immutable (advance refuses to rewrite a satisfied
state backward; artifacts never rewritten).

state.json fields (see schemas/state.schema.json): run_id, phase, completeness_state, timestamps
(created_at, per-phase completed_at map), repo_fingerprint_ref, codex (session_id, jobs[],
stage_counts {independent, cross_examination, adjudication}), phase_attempts map, failure_reason,
adjudication_skipped, schema_version (1).

## Budget governor (hard)

Codex stage counts in state.json: independent ≤ 1, cross_examination ≤ 1, adjudication ≤ 1,
total ≤ 3. `codex_runner.py start` refuses (exit 3) when a count would be exceeded. Claude audit
stages likewise ≤ 1 each (enforced by SKILL.md protocol + state machine).

## Script CLIs (scripts/, all stdlib, python3, executable)

`audit_council.py` (run lifecycle):
- `preflight --repo R --brief B [--skip-codex]` → non-inference checks: git repo, brief exists
  readable non-empty, output dir creatable, ANTHROPIC_API_KEY detection (report presence as
  boolean only, never value; presence → fail with INVALID_AUDIT_INPUT-style diagnostic),
  `codex` on PATH, `codex login status` OK, `codex exec --help` contains required flags, model
  `gpt-5.6-sol` resolvable (config default or explicit flag). JSON result on stdout.
- `init-run --repo R --brief B` → creates run dir, writes 00-run-manifest.json,
  01-repository-state.json, state.json(CREATED), prompts/, logs/, checksums.sha256. Prints run dir.
- `freeze-contract --run DIR --contract FILE` → validate vs schema, copy to 02-audit-contract.json,
  checksum, advance to CONTRACT_FROZEN (also records PREFLIGHT_COMPLETE path).
- `advance --run DIR --to STATE --artifact FILE` → schema-validate artifact, checksum, transition.
- `verify-repo --run DIR` → recompute fingerprint vs 01-repository-state.json; exit 0 match /
  exit 4 STALE_REPOSITORY (with diff summary of what changed, no resets).
- `write-guard --run DIR` → compare working tree vs baseline inventory in 01-repository-state.json;
  report NEW modifications outside the run dir; exit 5 on violation (never deletes anything).
- `resume-check --run DIR` → validate state.json schema, verify all checksums, verify repo
  fingerprint, verify completed artifacts; print earliest incomplete phase + codex session ref.
- `render --run DIR --artifact NAME` → markdown rendering via render_report.py.

`codex_runner.py` (Codex process lifecycle):
- `start --run DIR --phase {independent|cross_examination|adjudication} [--session ID]`
  [--prompt FILE] → enforces budget governor; renders prompt (from prompts/ templates by phase,
  or --prompt); writes prompt to run prompts/; launches detached subprocess:
  fresh: `codex exec -C <repo> --model gpt-5.6-sol --sandbox read-only --json
         --output-schema <schemas/…> -c model_reasoning_effort="xhigh" -o <out-file> -`
  resume: `codex exec resume <SESSION_ID> --model gpt-5.6-sol --json --output-schema <schema>
         -c model_reasoning_effort="xhigh" -c sandbox_mode="read-only" -o <out-file> -`
  stdin = opened prompt file; stdout→logs/<phase>.jsonl; stderr→logs/<phase>.stderr.log;
  persist job json (job_id, pid, argv, start_ts, phase, session|null) in logs/jobs/. Prints job_id.
  NEVER uses `--last`, `--dangerously-bypass-approvals-and-sandbox`, `danger-full-access`.
- `wait <job_id or path> --timeout SEC` → poll process + completion markers; classify:
  RUNNING | COMPLETE | FAILED | QUOTA | AUTH_ERROR | INVALID_OUTPUT. On completion: parse JSONL
  (thread.started → session id persisted to state.json; turn.completed → token usage into
  99-run-metrics.json), validate -o output file exists and parses vs schema. Exit 0 COMPLETE,
  1 FAILED, 2 QUOTA, 3 AUTH_ERROR, 6 INVALID_OUTPUT, 7 still-RUNNING-after-timeout.
- `status <job>` / `result <job>` (print parsed final message) / `cancel <job>` (SIGTERM→SIGKILL).

`repo_fingerprint.py` — library + `capture --repo R` / `verify --repo R --state FILE`:
HEAD sha, branch, `git status --porcelain`, tracked inventory (`git ls-files -s` → path+mode+sha),
untracked inventory (names+size, not content), brief sha256, timestamps, tool versions.
`verify` returns structured diff. Material-change rule: any tracked-file sha/mode change, any
HEAD/branch change, or untracked file appearing/disappearing outside `audit-output/`.

`validate_artifact.py` — library: JSON Schema validation (use `jsonschema`? NO — stdlib only:
implement a minimal validator sufficient for our schemas: type/enum/required/properties/items/
additionalProperties/minItems/pattern). `validate --file F --schema S`, plus ledger/final
invariant checks: (i) every cluster origin id unique across clusters; (ii) REJECTED findings only
in rejected appendix of final; (iii) UNRESOLVED CRITICAL/HIGH present as unresolved risk;
(iv) late findings carry `validated_by` other-model reference or status UNRESOLVED.

`render_report.py` — library used by audit_council.py render: markdown for independent audits,
ledger, final audit (sections per spec §25), provenance lines per finding.

Atomic writes everywhere: write temp in same dir → fsync → os.replace. Checksums appended per
artifact (sha256) in checksums.sha256; resume verifies them (mismatch → exit 8).

## Finding model (schemas/finding.schema.json — shared $defs)

severity ∈ CRITICAL|HIGH|MEDIUM|LOW|INFO; confidence ∈ HIGH|MEDIUM|LOW;
status ∈ PROVISIONAL|CONFIRMED|PARTIALLY_CONFIRMED|REJECTED|UNRESOLVED;
evidence.kind ∈ OBSERVED_FACT|INFERENCE|HYPOTHESIS|REQUIREMENT_CLAIM;
evidence ref fields: path, symbol, lines, requirement_ref, test_ref, command_ref, artifact_hash
(never fabricate line numbers — enforced by protocol, validated structurally only).
provenance: discovered_by ∈ OPUS|CODEX, independently_confirmed_by[], challenged_by,
challenge_result ∈ CONFIRMED|PARTIALLY_CONFIRMED|REJECTED|INSUFFICIENT_EVIDENCE|null,
adjudication_result. Finding ids: `OPUS-<nnn>` / `CODEX-<nnn>`; clusters `CLUSTER-<nnn>`.
Cluster classification ∈ CONSENSUS_CANDIDATE|OPUS_ONLY|CODEX_ONLY|CLAIM_CONFLICT|
SEVERITY_CONFLICT|CAUSAL_CONFLICT. Ledger cluster status ∈ CONSENSUS|CONFIRMED_AFTER_CHALLENGE|
NARROWED|REJECTED|DISPUTED|UNRESOLVED.

## Cross-examination artifact (31/32)

Array of challenges: {target_finding_id, verdict ∈ CONFIRMED|PARTIALLY_CONFIRMED|REJECTED|
INSUFFICIENT_EVIDENCE, counter_evidence[], reasoning_summary, severity_recalibration?} plus
late_findings[] (each a full finding with provenance.discovered_by = challenger, status
PROVISIONAL, must include `validated_by` once validated).

## Codex output schemas (fed to --output-schema)

prompts pipeline uses schemas/independent-audit.schema.json (subset without $defs indirection —
Codex --output-schema requires a self-contained root schema) and schemas/cross-examination.schema.json
(Codex-compatible variant). Keep these SELF-CONTAINED (no $ref/$defs) for Codex.

## Preflight auth rules

Fail (with clear diagnostic, no secret values) if: ANTHROPIC_API_KEY present in env;
`codex login status` not logged in; env contains OPENAI_API_KEY or CODEX_API_KEY (warn + fail:
could silently select PAYG).
