# Protocol: Cross-Examination (Phases 3, 4A, 4B) — spec §18/§19/§20/§23

## Normalization (Phase 3, Opus)

Do not compare the two audits by prose similarity. Build `30-normalized-findings.json`:

- Normalize each OPUS-*/CODEX-* finding into canonical clusters `CLUSTER-<nnn>`.
- Merge into one cluster ONLY when findings represent substantially the same underlying
  failure or root cause. Do NOT merge merely related findings when merging would hide
  distinct failure modes — two symptoms of one root cause may cluster; two causes of one
  symptom may not.
- Preserve full provenance: every member finding id, its origin model, severity, and
  evidence remain addressable.
- Give each cluster an `initial_classification`:
  `CONSENSUS_CANDIDATE` | `OPUS_ONLY` | `CODEX_ONLY` | `CLAIM_CONFLICT` |
  `SEVERITY_CONFLICT` | `CAUSAL_CONFLICT`.
- This classification is preliminary bookkeeping, NOT adjudication.

Only after this artifact is checkpointed does Opus begin adversarial review of Codex
findings.

## Phase 4A — Opus falsifies Codex (the running Opus session)

Your task is NOT to validate Codex findings. Attempt to FALSIFY every material CODEX
finding:

- Independently inspect the cited evidence AND the surrounding implementation.
- Seek counter-evidence: guards, unreachable paths, config, requirement clauses that
  permit the observed behavior.
- Challenge causal claims (does the cited cause actually produce the claimed failure?) and
  impact claims (is the failure scenario realistic?).
- Challenge severity (protocols/severity-policy.md) — record `severity_recalibration`
  where warranted.
- Check whether the "expected" behavior is actually required by an authoritative source,
  or is an assumption.
- Detect duplication (same defect re-reported as several findings) and speculative
  reasoning (claims resting on HYPOTHESIS presented as fact).

For each material finding emit a challenge object: `target_finding_id`, `verdict` ∈
`CONFIRMED` | `PARTIALLY_CONFIRMED` | `REJECTED` | `INSUFFICIENT_EVIDENCE`,
`counter_evidence[]` (evidence-policy discipline), `reasoning_summary`, optional
`severity_recalibration`.

- CONFIRMED means your falsification attempt failed and the claim stands as stated.
- PARTIALLY_CONFIRMED means the core is real but claim/scope/severity/cause needed
  narrowing — say precisely what survives.
- REJECTED requires concrete counter-evidence or demonstration that the expectation is
  not required. Disagreement alone is not rejection.
- INSUFFICIENT_EVIDENCE when the claim cannot be established or refuted from the
  repository — preserve uncertainty; do not default to CONFIRMED.

## Phase 4B — Codex falsifies Opus

`codex_runner.py start --run "$RUN" --phase cross_examination --session <stored-session-id>`
resumes the EXACT original Codex thread (never `--last`) with
`prompts/codex-cross-examine-opus.md` receiving `10-opus-independent.json` findings as
JSON. The same falsification standard applies (re-read evidence, inspect surrounding code,
seek contradiction, validate requirement basis, challenge causal chain and severity,
distinguish real defect from intentional design and systemic cause from symptom). Same
bounded wait loop and failure classification as Phase 2. Artifact:
`32-codex-cross-examination.json` (examiner CODEX, examined OPUS).

Artifact shape (cross-examination.schema.json, both 31 and 32): `examiner`, `examined`,
`challenges[]` as above, plus `late_findings[]`.

## Late findings (spec §23)

A model may discover genuinely new issues during cross-examination. A late finding:

- is a FULL finding object with `provenance.discovered_by` = the challenger (OPUS for 31,
  CODEX for 32), `status: PROVISIONAL`, and `late_finding: true`;
- does NOT enter the final report directly — it must receive at least one independent
  validation by the OTHER model (recorded via `provenance.validated_by`);
- if quota/time does not permit validation: final status `UNRESOLVED` (residual-risk /
  unresolved handling per final-synthesis). Never promote an unvalidated late finding to
  confirmed.
