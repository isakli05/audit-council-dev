# audit-council

A personal Claude Code skill that runs a bounded, read-only, two-model adversarial audit:
Claude Opus 5 and Codex (GPT-5.6 Sol, xhigh reasoning) independently audit a repository,
falsify each other's findings, resolve what evidence permits, and emit one
provenance-preserving final report.

## Installation

Personal skill, available in all projects:

    ~/.claude/skills/audit-council/

(Contents: SKILL.md, README.md, protocols/, schemas/, prompts/, scripts/, tests/.)

## Requirements

- Claude Code, logged in via Claude subscription OAuth (NOT an ANTHROPIC_API_KEY
  environment variable — preflight fails if one is detected, to avoid PAYG billing).
- Codex CLI on PATH, logged in via your ChatGPT/Codex subscription. Verify:

      codex login status

  It must report logged in. Do not configure an OpenAI API key; preflight fails if
  OPENAI_API_KEY / CODEX_API_KEY is set (it could silently select PAYG billing).
- A Git repository containing the code to audit, and an audit brief file.
- Python 3 (stdlib only).

## Invocation

    /audit-council ./audit-brief.md

The brief is a short markdown document stating what to audit, against which requirements,
and any scope/exclusions. Inline brief text is also accepted instead of a file path:

    /audit-council "Audit the authentication subsystem of src/auth for correctness and security defects."

The inline text is materialized into the run's own immutable
`inputs/original-audit-brief.md` (checksummed, referenced on resume) before any model
inference — identical provenance to a file-based brief. A path argument that does not
exist is reported as an error, never silently treated as inline text.

The run is autonomous: Codex is invoked, waited on, and cross-examined automatically. You
do not run /codex:status, /codex:result, or copy any output manually.

## Resume

If a run was interrupted (quota exhaustion, restart, Codex failure):

    /audit-council --resume audit-output/audit-council/<run-id>

Completed phases are never repeated; the audit continues from the earliest incomplete
phase. If the repository changed since the run started, the skill reports
STALE_REPOSITORY and stops rather than mixing evidence from different code states.

## Output

Everything is written under (inside the audited repository):

    audit-output/audit-council/<run-id>/

Key files: `90-final-audit.md` (final human-readable report), `90-final-findings.json`
(canonical), `40-disagreement-ledger.md` (per-cluster disagreement record),
`02-audit-contract.md`, per-phase artifacts, `99-run-metrics.json`, `state.json`.

## Completeness states

| State | Meaning |
|---|---|
| COMPLETE | full two-model council ran end to end |
| COMPLETE_WITH_RESIDUAL_UNCERTAINTY | full protocol ran; some findings remain UNRESOLVED |
| PARTIAL_CODEX_QUOTA | a Codex stage could not run/finish due to quota; resumable |
| PARTIAL_CODEX_FAILURE | Codex failed (auth, malformed output, process) |
| PARTIAL_CLAUDE_INTERRUPTION | the Claude side was interrupted |
| STALE_REPOSITORY | repository changed mid-audit; results not comparable |
| INVALID_AUDIT_INPUT | bad brief/invocation; failed before expensive calls |

Partial reports explicitly list which claims lacked second-model adjudication
(`claims_lacking_second_model` in `90-final-findings.json`).

## What the skill NEVER modifies

- Source files, tests, package files, project configuration, documentation
- Git index, branches, commits, working-tree state
- Anything outside `audit-output/audit-council/<run-id>/`
- It never applies fixes or patches, and never pushes.

How this is enforced — the two sides differ, and the difference matters:

- Codex repository writes are mechanically PREVENTED by its read-only sandbox
  (`--sandbox read-only` / `sandbox_mode="read-only"`).
- Claude source mutation is prohibited by protocol and by disabling the direct editing
  tools (Edit/Write/NotebookEdit); because Bash remains available for audit inspection,
  repository integrity guards DETECT unexpected mutations after every phase
  (write-guard + frozen fingerprint) and halt the audit. This is detection, not an
  OS-level sandbox.

If an unexpected source mutation is detected mid-run, the run stops and reports exactly
what changed; nothing is reset or deleted.

## Quota failure representation

Codex quota exhaustion is detected and classified (not retried in a loop). Work completed
before exhaustion is kept. The final report is honestly labelled PARTIAL_CODEX_QUOTA and
names the claims that lacked second-model adjudication; a later `--resume` continues the
missing stage within the budget limits (max 3 Codex inference stages per run).

## Run metrics

    cat audit-output/audit-council/<run-id>/99-run-metrics.json

Codex token usage (input/cached/reasoning/output), turns, elapsed time, number of
invocations, and fresh vs resumed sessions — so you can compare council-architecture
quota cost against full Codex-only audits. Claude subscription token usage is not
fabricated.

## Uninstall

    rm -rf ~/.claude/skills/audit-council

Audit outputs under `audit-output/audit-council/` in audited repositories are ordinary
files; remove them yourself if desired.

## v2.0 additions

- **Environment binding (A0)**: every run freezes `01-environment-binding.json`
  (repo root realpath, git dirs, worktree identity, HEAD, brief sha). Before
  any model inference the binding is re-verified (`AC verify-env`); a mismatch
  fails closed with `INVALID_AUDIT_ENVIRONMENT` and zero model calls. A brief
  may declare its target explicitly with a fenced ```json block
  `{"target": {"repository_root": ..., "expected_head": ...}}`; all other
  prose paths are inert text.
- **Automatic path confinement (skill-scoped, no setup needed)**: the
  skill's frontmatter registers a PreToolUse hook (Bash/Read/Grep/Glob →
  hooks/path_guard_hook.py) the moment /audit-council is invoked; it
  denies out-of-root tool calls before execution while a run is active
  and is inert otherwise (zero impact on sessions that never invoke the
  skill). An optional belt-and-suspenders GLOBAL registration
  (~/.claude/settings.json PreToolUse, same command) can still be added
  by the operator, but is NOT required for release/historical audits.
- **Codex OS confinement**: every codex launch (fresh and resume) runs
  inside a bubblewrap boundary — repo read-only, run dir writable,
  `~/.codex` and toolchain readable, everything else outside the bind
  set unreadable, `/tmp` a fresh tmpfs. See
  docs/A0-CODEX-CONFINEMENT.md for the probe evidence and the honest
  boundary (system dirs remain readable).
- **What the hook is NOT**: a mechanical, no-inference scanner. Encoded or
  dynamically-constructed payloads (`base64 -d | sh`, `chr()`-built paths,
  interpreter-generated strings) are beyond any lexical deny layer — the
  hook is a deny-before-exec hardening layer on top of detection
  (fingerprint freeze + write-guard), not a sandbox. Harness operands
  (the skill's own `scripts/`+`hooks/` trees and the system interpreter
  binaries) are inherently allowed so the audit can run itself.
- **Typed evidence (G)**: evidence citations use `line_ranges:
  [{"start": 184, "end": 185}, {"start": 240, "end": 273}]`; v1 artifacts
  are read via an in-memory migration reader and never rewritten.
- **Explicit phase skips (H)**: passing over an artifact phase (e.g.
  finalizing past a quota-deferred Codex stage) requires
  `advance --skip PHASE='reason'`; silent skips are refused.
- **Telemetry 2.0 (E)**: every terminal Codex attempt records stable elapsed
  (including INVALID_OUTPUT/QUOTA/cancel); budget omissions are explicit in
  `99-run-metrics.json`.
- **Specialists (C) are DEFAULT OFF** and remain off until eval evidence
  shows net value; activation requires a pre-frozen documented reason.
- **Public contract (F)**: `PUBLIC-CONTRACT.md` and
  `audit_council.py describe --json` (protocol version 2.0) are the stable
  surface for prompt-authoring agents.
- **Eval suite (D)**: `eval/eval_cli.py tier1` runs the deterministic harness
  + environment-integrity gate (100% required); tier-2 fixtures and the
  approval-gated tier-3 historical replay live under `eval/`.
