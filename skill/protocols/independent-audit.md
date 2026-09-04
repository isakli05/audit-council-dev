# Protocol: Independent Audit (Phases 1 and 2) — spec §16/§17

Two independent audits of the same repository state against the same frozen Audit
Contract. Neither model sees the other's output before both passes are complete.

## Independence rules (hard)

- Opus completes and checkpoints Phase 1 (`10-opus-independent.json` advanced via script)
  BEFORE any Codex output is read by Opus.
- The Codex Phase 2 prompt contains ONLY: audit contract, repository root, original audit
  brief, authoritative source paths. It must NOT contain Opus findings, markdown,
  hypotheses, or confidence estimates.
- Both models audit the same frozen repository state; `verify-repo` runs before each
  expensive phase. On STALE_REPOSITORY, stop (protocols/failure-and-resume.md).
- Do not communicate expected conclusions, expected finding counts, or "areas of concern"
  to Codex in the prompt.

## Investigative mandate (both models)

- Independently reconstruct the relevant architecture rather than trusting documentation.
- Test each authoritative requirement against the actual implementation.
- Seek hidden assumptions (concurrency, environment, input domain, ordering, failure
  handling, auth, data lifetime).
- Search for missing behavior, not just wrong behavior.
- Identify false assurances from tests and docs.
- Identify systemic / root-cause defects, not only symptoms.
- Distinguish OBSERVED_FACT / INFERENCE / HYPOTHESIS / REQUIREMENT_CLAIM throughout
  (protocols/evidence-policy.md).
- Avoid style nitpicks unless the audit contract explicitly puts style in scope.
- Stay within contract scope and exclusions.

## Output artifact

`independent-audit.schema.json` shape — required: `model` (`claude-opus-5` for the Opus
artifact, `gpt-5.6-sol` for Codex), `repository_fingerprint_sha256` (from
`01-repository-state.json`), `findings[]`, `audit_summary`; optional `requirement_coverage[]`
(requirement, covered, note), `limitations[]`.

Each finding (finding.schema.json): id `OPUS-<nnn>` / `CODEX-<nnn>` (zero-padded, unique),
`origin` = own id at this phase, `status: PROVISIONAL`, `provenance.discovered_by` =
`OPUS` / `CODEX`. Severity per protocols/severity-policy.md; confidence per
protocols/evidence-policy.md calibration. Use the descriptive fields (`claim`,
`failure_scenario`, `impact`, `root_cause`, `verification_method`, `residual_uncertainty`)
for material findings; don't pad with empty strings.

An empty findings array is a legitimate result — do not invent findings to seem
productive. Record coverage honestly in `requirement_coverage` and `limitations`.

## Phase 1 (Opus) mechanics

The running Opus session performs the audit with Read/Grep/Glob/read-only Bash, composes
the JSON, and pipes it to `advance --to OPUS_INDEPENDENT_COMPLETE --artifact
10-opus-independent.json --stdin`, then `render`. The phase is complete only when
`advance` succeeds.

## Phase 2 (Codex) mechanics

`codex_runner.py start --run "$RUN" --phase independent` renders
`${CLAUDE_SKILL_DIR}/prompts/codex-independent.md` with the contract/brief, writes the
prompt to `prompts/codex-independent.md`, and launches a FRESH read-only
`codex exec` (gpt-5.6-sol, xhigh, `--output-schema`). Opus then runs a bounded wait loop
(`wait --timeout 540`, repeat while exit 7 RUNNING). On COMPLETE, the runner has validated
the `-o` file against `independent-audit.schema.json` and persisted the Codex thread ID
into `state.json`. Opus advances `--to CODEX_INDEPENDENT_COMPLETE` (piping the validated
content via `--stdin` or the artifact path per script support) and renders
`20-codex-independent.md`. Failure classification: protocols/failure-and-resume.md.
