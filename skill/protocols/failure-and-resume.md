# Protocol: Failure and Resume — spec §26/§28

## Principles

- Fail explicitly. Never silently replace a failed Codex pass with Opus-generated
  content; never present a partial audit as council-complete.
- Completed phases are immutable and survive failures — quota exhaustion never erases
  prior work; nothing completed is repeated after resume.
- Never destroy or reset user state to "recover" (no git operations, no deletions).

## Environment failure (v2: INVALID_AUDIT_ENVIRONMENT)

`AC verify-env` (or the automatic gate before any inference phase) fails when the
frozen environment binding no longer matches reality: brief root/HEAD mismatch,
worktree identity change, repo root replaced, CWD outside the frozen root, path
escape, alternate worktree access, unauthorized /tmp, symlink escape. Rules:

- ZERO model calls happen through a failed environment gate; `codex_runner start`
  refuses (exit 3) and `advance` to any inference phase refuses.
- An environment failure NEVER yields a product GO/NO-GO verdict — the
  completeness state is `INVALID_AUDIT_ENVIRONMENT` and the run must be re-prepared.
- Historical/narrative absolute paths in brief prose are inert text; only the
  explicit fenced `target:` metadata block has authority.

## Codex wait classification (codex_runner.py wait)

- exit 7 RUNNING → issue another bounded `wait --timeout 540`. Repeat while the job shows
  progress; this is internal orchestration, the user never polls.
- exit 0 COMPLETE → proceed with the validated artifact.
- exit 2 QUOTA → quota handling, below.
- exit 3 AUTH_ERROR → stop the run with completeness `PARTIAL_CODEX_FAILURE` and a
  diagnostic telling the user to run `codex login status` (do not attempt to fix auth).
- exit 1 FAILED / exit 6 INVALID_OUTPUT → see Malformed output, below.

## Quota handling (spec §26)

- Quota exhausted BEFORE the Codex independent audit completes:
  completeness_state `PARTIAL_CODEX_QUOTA`. Stop; the run is resumable — the user can
  re-invoke `--resume` later when quota resets.
- Quota exhausted AFTER the independent pass (cross-examination or adjudication):
  keep completed artifacts; do not repeat any completed pass; mark the remaining Codex
  stage deferred; proceed with final synthesis as a PARTIAL report
  (`PARTIAL_CODEX_QUOTA` or `COMPLETE_WITH_RESIDUAL_UNCERTAINTY` per judgment) whose
  `claims_lacking_second_model[]` names exactly which claims lacked second-model
  adjudication. Unvalidated late findings become UNRESOLVED.
- Resume of a quota-deferred Codex stage is permitted only within the budget governor.
  The governor counts SUCCESSFUL stages (independent ≤ 1, cross_examination ≤ 1,
  adjudication ≤ 1, total ≤ 3); a failed/quota-exhausted attempt may be retried on
  resume, hard-capped at 3 ATTEMPTS per phase (launch attempts, successful or not).

## Malformed Codex output

- Preserve the raw output (logs/ JSONL + stderr remain in the run dir).
- At most ONE schema-repair retry if inexpensive and possible.
- Otherwise mark INVALID_OUTPUT → completeness `PARTIAL_CODEX_FAILURE`.
- NEVER have Opus fabricate or "fix" Codex's structured response.

## Repository staleness (STALE_REPOSITORY)

`verify-repo` / `resume-check` exit 4: the repository changed materially since the frozen
state. Stop. Do not compare reviewers that audited different code; do not mix evidence
from old and new repo states; do not restore anything. Report what changed (the script's
diff summary). A new audit run is required.

## Claude-side interruption

Interruptions (session restart, crash) leave the run directory consistent at the last
completed phase. On resume, completeness is corrected to
`COMPLETE_WITH_RESIDUAL_UNCERTAINTY` or `PARTIAL_CLAUDE_INTERRUPTION` if the run cannot
be continued.

## Completeness states

| State | Meaning |
|---|---|
| COMPLETE | full two-model council: independent + cross + (optional) adjudication + synthesis |
| COMPLETE_WITH_RESIDUAL_UNCERTAINTY | full protocol ran; UNRESOLVED findings remain |
| PARTIAL_CODEX_QUOTA | a Codex stage could not run/finish due to quota |
| PARTIAL_CODEX_FAILURE | Codex failed (auth, malformed output, process) |
| PARTIAL_CLAUDE_INTERRUPTION | Opus side was interrupted and could not continue |
| STALE_REPOSITORY | repository changed mid-audit; results not comparable |
| INVALID_AUDIT_INPUT | bad brief/invocation; failed before expensive calls |

## Resume procedure (spec §28)

`/audit-council --resume audit-output/audit-council/<run-id>`:

1. `AC resume-check --run <run-dir>` — validates state.json schema, verifies ALL
   checksums (mismatch → exit 8: stop, report which artifact), verifies the repository
   fingerprint (exit 4 → STALE_REPOSITORY handling above), verifies completed artifacts,
   and prints the earliest incomplete phase plus the Codex session reference.
2. Verify the Codex session reference if the next phase needs it (4B/6 resume the exact
   stored session id; if it is missing or invalid, a fresh Codex session is acceptable
   for that stage ONLY within budget, and the session id is re-persisted).
3. Continue from the earliest incomplete phase per SKILL.md. Never repeat a completed
   phase unless its artifact failed integrity validation (checksum/schema), in which case
   resume-check reports it and the phase is redone from its own inputs.

## Write-guard violations

`AC write-guard --run "$RUN"` exit 5: new modifications appeared outside the run dir.
Stop immediately, record the invariant violation, do not delete or reset anything,
report precisely what changed. This ends the run (PARTIAL_*).
