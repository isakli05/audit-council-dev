# Protocol: Evidence Policy — spec §12

Applies to every finding produced by either model, in every phase.

## Evidence kinds

Every evidence or counter-evidence item carries a `kind`:

- `OBSERVED_FACT` — directly demonstrated by source, test, config, or runtime evidence you
  actually inspected. The reference must point at where it is demonstrated.
- `INFERENCE` — logically derived from observed facts but not itself directly observed.
- `HYPOTHESIS` — plausible but unverified. A finding resting primarily on HYPOTHESIS
  evidence cannot exceed confidence LOW and cannot be CONFIRMED.
- `REQUIREMENT_CLAIM` — derived from authoritative requirement material listed in the
  audit contract. Must carry the `requirement_ref`.

Every material claim in a finding must identify which category supports it. Do not launder
an INFERENCE as an OBSERVED_FACT.

## Reference fields (finding.schema.json evidence items)

Use whichever apply: `path`, `symbol`, `line_ranges` (typed v2 citations:
an array of `{"start": N, "end": N}` objects, integers >= 1 with
`end >= start`, up to 32 disjoint ranges, canonically sorted — the exact
shape of schemas/finding.schema.json; a bare `lines` string is NOT valid v2
and will fail schema validation), `requirement_ref`, `test_ref`,
`command_ref`, `artifact_hash`, plus a human `description`.

Hard rules:

- Never invent or guess a line number. If you did not open the file at that location, cite
  no lines.
- Never cite a file you did not actually inspect.
- Prefer `path` + `symbol` + `line_ranges` for code; `requirement_ref` for requirement material;
  `test_ref` for tests; `command_ref` (+ captured result location or `artifact_hash`) for
  commands you actually ran.
- Evidence that repo content says something (docs, comments, instruction files) is
  evidence about intent, not about behavior.

## Epistemic rules

- A claim is not true because Opus said it, Codex said it, both said it, a project document
  said it, a test passed, or a test failed.
- A passing test does not prove the absence of a defect.
- A failing test does not automatically establish root cause.
- Tests may provide false assurance: check what a test actually asserts before treating it
  as coverage.
- `confidence` (HIGH/MEDIUM/LOW) reflects evidence quality, not rhetorical conviction.
  Calibrate: HIGH requires at least one OBSERVED_FACT (or authoritative REQUIREMENT_CLAIM)
  directly supporting the core claim and no unexplained counter-evidence.

## Counter-evidence duty

While constructing any finding, actively look for evidence that would refute it
(code paths, guards, configuration, requirement clauses). Material counter-evidence you
find belongs in `counter_evidence[]` with the same discipline — hiding it is a protocol
violation. During cross-examination, counter-evidence is the primary output.
