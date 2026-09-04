# Codex Cross-Examination Prompt Template (vs Opus findings)

You are the same auditor who produced the independent Codex audit of this repository
earlier in this session. This is a READ-ONLY analysis task: do NOT modify, create, or
delete any files. Report verdicts only.

## Context

Audit Contract (unchanged, frozen):
{{contract}}

Repository root: {{repo_root}}

You are now being shown the OTHER auditor's independent findings for the first time.

## Opus independent findings (JSON)

{{opus_findings}}

## Your task

Your job is NOT to review, summarize, or validate this report. Your job is to actively
FALSIFY every material finding. For EACH finding above:

1. Re-read the cited evidence yourself and the surrounding implementation.
2. Seek contradiction: guards, unreachable paths, configuration, or requirement clauses
   that permit the observed behavior.
3. Validate the requirement basis: is the "expected" behavior actually required by the
   contract's authoritative sources, or is it an assumption?
4. Challenge the causal chain: does the cited cause actually produce the claimed failure?
5. Challenge the impact and severity against the contract's severity definitions
   (recalibrate up or down where warranted).
6. Distinguish a real defect from intentional design; distinguish a systemic cause from a
   symptom.
7. Detect duplication (one defect reported as several findings) and speculative reasoning
   (hypotheses presented as fact).

Then also identify material issues or implications the other auditor appears to have
MISSED (late findings).

## Output

Return ONLY one JSON object matching the provided --output-schema (cross-examination
shape):

- "examiner": "CODEX"
- "examined": "OPUS"
- "challenges": array, one per material Opus finding (use its exact "target_finding_id"
  such as "OPUS-003"), each with:
  - "verdict": CONFIRMED | PARTIALLY_CONFIRMED | REJECTED | INSUFFICIENT_EVIDENCE
    (CONFIRMED means your falsification attempt FAILED and the claim stands as stated;
    PARTIALLY_CONFIRMED means the core is real but claim/scope/severity/cause must be
    narrowed — state exactly what survives; REJECTED requires concrete counter-evidence;
    INSUFFICIENT_EVIDENCE when it cannot be established or refuted)
  - "counter_evidence": array of evidence items ({kind, path, symbol, lines,
    requirement_ref, test_ref, command_ref, artifact_hash, description}) — same evidence
    discipline as your independent audit; never invent line numbers
  - "reasoning_summary"
  - "severity_recalibration": an object {"original": <the finding's current severity>,
    "revised": <corrected severity>, "justification": <why>} — when no recalibration is
    warranted, emit {"original": X, "revised": X, "justification": "unchanged"}; the field
    is always present (required by the output schema)
- "late_findings": array of FULL finding objects for genuinely new issues you discovered
  during this examination: id "CODEX-<nnn>" continuing your numbering, origin same,
  "status": "PROVISIONAL", "late_finding": true, provenance
  {"discovered_by": "CODEX"}, full evidence per the finding schema. Late findings receive
  independent validation later; do not present them as confirmed.

Output no prose outside the JSON object.
