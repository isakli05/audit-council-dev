# Audit Council — Public Contract

Protocol version **2.0**. Machine-readable source of truth:
`python3 scripts/audit_council.py describe --json` (validated by
`schemas/public-contract.schema.json`); this file mirrors it for prompt
authors, with drift tests keeping enum/list facts identical.

## What Audit Council does

A two-model adversarial audit council that reviews a git repository against your audit brief and produces a
provenance-preserving final report with an explicit GO/NO-GO recommendation. It is read-only, resumable, and
checkpointed (every phase transition validates and checksums its canonical artifact); every finding must cite
typed, checkable evidence, and failures are classified honestly.

## Invocation

```
/audit-council <audit-brief.md | "inline brief text">
/audit-council --resume audit-output/audit-council/<run-id>
```

The brief declares scope, requirements, exclusions, and severity rules. Run
artifacts land under `audit-output/audit-council/<run-id>/` — the only
location Audit Council ever writes.

## Brief target metadata

The ONLY brief text with execution authority is an explicit fenced block:

```json
{"target": {"repository_root": "/absolute/path/to/repo", "expected_head": "<40-hex sha>"}}
```

The declared root (by realpath) and head must match the frozen audit environment, or the run refuses inference
(`INVALID_AUDIT_ENVIRONMENT`, zero model calls). All other brief prose — including any absolute paths — is
inert text, never execution authority.

## Environment modes

| Mode | Meaning |
|---|---|
| AUTO | safest derivation; never silently downgrades required isolation |
| CURRENT | audit the live repo; only when the contract permits |
| RELEASE | isolated frozen target (detached worktree) |
| HISTORICAL | isolated detached target + explicitly staged evidence only |

An environment binding (root realpath, git identity, worktree identity, HEAD, brief digest) is frozen at run
init and re-verified before every inference phase; the digest excludes freeze time. Environment failures carry
one of nine reasons — `BRIEF_ROOT_MISMATCH`, `BRIEF_HEAD_MISMATCH`, `WORKTREE_IDENTITY_CHANGED`,
`CWD_OUTSIDE_FROZEN_ROOT`, `PATH_ESCAPE_ATTEMPT`, `ALTERNATE_WORKTREE_ACCESS`, `UNAUTHORIZED_TMP_ACCESS`,
`REPO_ROOT_REPLACED`, `SYMLINK_ESCAPE` — aborting before inference with zero model calls, never a product
verdict.

## Model roles and independence

- **Opus** (`claude-opus-5`): primary interactive orchestrator + independent auditor; one independent pass.
- **Codex** (`gpt-5.6-sol`, reasoning `xhigh`): independent second auditor via direct `codex exec` (fresh) or
  `codex exec resume <explicit-id>`, read-only sandbox; subscription auth only — PAYG keys fail preflight.

Independence rules: a first-pass barrier means neither auditor sees the other's findings before both
independent audits complete; cross-examination is falsification, not validation; no forced consensus —
disagreements are preserved in the ledger and resolved (or left explicitly unresolved) by bounded adjudication.

## Evidence model (line_ranges)

Evidence items carry typed multi-range citations:

```json
"line_ranges": [{"start": 184, "end": 185}, {"start": 240, "end": 273}]
```

`start`/`end` are integers >= 1 with `end >= start`; up to 32 disjoint ranges per item, canonically sorted.
Zero ranges = document/requirement-level evidence. Raw model outputs are always preserved alongside
canonical artifacts.

## Completeness states

| State | Meaning |
|---|---|
| RUNNING | audit in progress |
| COMPLETE | all phases finished |
| COMPLETE_WITH_RESIDUAL_UNCERTAINTY | finished with unresolved questions |
| PARTIAL_CODEX_QUOTA | Codex budget/quota exhausted mid-run |
| PARTIAL_CODEX_FAILURE | Codex failed terminally mid-run |
| PARTIAL_CLAUDE_INTERRUPTION | orchestrator interrupted |
| STALE_REPOSITORY | repository changed during the audit |
| INVALID_AUDIT_INPUT | brief/contract input invalid |
| INVALID_AUDIT_ENVIRONMENT | environment/binding gate failed (never a product verdict) |

## Governor defaults

Successful Codex stages <= 1 per phase, <= 3 total; <= 3 attempts per
phase; 1 repair per phase; specialists 0 (normal cap 2, hard cap 3, 2
turns each); <= 4 dynamic probes; cached evidence reused when valid;
release gates always fresh. The governor may never skip a mandatory
independent pass, hide a material dispute, or promote PARTIAL to
COMPLETE; every budget-driven omission is recorded in run metrics.

## What is NEVER modified

Source, tests, config, docs, and git state of the audited repository. Codex writes are OS-prevented
(read-only sandbox). The only writable location is `audit-output/audit-council/<run-id>/`; finalized
historical runs are never rewritten.

## Known limitations

- Codex read confinement is runner-enforced, not OS-enforced (documented
  residual risk); the sandbox prevents writes but does not scope reads.
- The Claude path-confinement hook is runner-enforced and session-opt-in;
  without it enforcement weakens to detection (fingerprint + write-guard).
- Specialists are default-off until eval-proven.
- Historical replay is approval-gated; benchmarks are never re-run implicitly.

## Compatibility policy

Additive changes keep protocol 2.x; any change to a documented field's
meaning or any removal bumps the major version.
