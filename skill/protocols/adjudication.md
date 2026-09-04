# Protocol: Disagreement Ledger and Targeted Adjudication (Phases 5–6) — spec §21/§22

## Phase 5 — Disagreement ledger (Opus)

Build `40-disagreement-ledger.json` from the normalized findings plus BOTH
cross-examinations. One ledger entry per cluster (disagreement-ledger.schema.json):

- `cluster_id`, `member_finding_ids`
- `initial_classification` (carried from Phase 3)
- `positions`: `opus` and `codex` objects, each with `position` (their claim, summarized
  faithfully — including "no finding" for OPUS_ONLY/CODEX_ONLY clusters where the other
  model did not report it), their `severity` (null if none), and their
  `challenge_result` (the verdict the OTHER model's cross-examination gave their finding;
  null if not challenged).
- `evidence_overlap` (string), `counter_evidence[]`, `severity_divergence`,
  `causal_divergence` (booleans)
- `status` ∈ `CONSENSUS` | `CONFIRMED_AFTER_CHALLENGE` | `NARROWED` | `REJECTED` |
  `DISPUTED` | `UNRESOLVED`
- `adjudication_eligible` (boolean — see Phase 6 gate)
- `notes`

Status assignment guidance:

- CONSENSUS: both models found it and the challenge verdicts did not narrow it.
- CONFIRMED_AFTER_CHALLENGE: one model's finding survived the other's falsification
  attempt (verdict CONFIRMED, or PARTIALLY_CONFIRMED without material narrowing).
- NARROWED: the surviving claim is materially narrower (scope, cause, or severity) than
  the original — capture the narrowed claim in `notes`.
- REJECTED: a challenge produced concrete counter-evidence (verdict REJECTED) or the
  expectation was shown not to be required, and the originating model's position did not
  survive.
- DISPUTED: the models' positions materially conflict and evidence has not resolved it.
- UNRESOLVED: evidence is insufficient to decide (including INSUFFICIENT_EVIDENCE
  verdicts and unvalidated late findings).

Preserve disagreement — do not round DISPUTED toward your own opinion. Advance
`--to LEDGER_COMPLETE`, then render.

## Phase 6 — Targeted adjudication (conditional, ≤ 1 round)

Gate: adjudicate ONLY clusters that are (severity CRITICAL or HIGH) AND (status DISPUTED
or UNRESOLVED) — or clusters whose resolution would change the validity of several other
findings. Set `adjudication_eligible` accordingly in the ledger. If no cluster is
eligible: skip Phase 6 (record `adjudication_skipped: true` script-mediated) and proceed
to final synthesis. NEVER run a second adjudication round; never rerun a full repository
audit here.

Per eligible cluster, build a compact Evidence Packet (field names per
`schemas/adjudication.schema.json` `evidence_packet` object):

- the precise disputed claim,
- the relevant requirement (authoritative source reference),
- the exact supporting evidence and exact counter-evidence (file/symbol/line refs),
- each model's position and challenge result,
- what specifically remains unresolved.

Both model families may inspect the underlying repository again, but the task is strictly
BOUNDED to the dispute in the packet:

1. Opus verdict: reason at maximum depth on the packet alone. Verdict ∈ CONFIRMED |
   PARTIALLY_CONFIRMED | REJECTED | UNRESOLVED.
2. Codex verdict: `codex_runner.py start --run "$RUN" --phase adjudication --session
   <stored-session-id>` with `prompts/codex-targeted-adjudication.md`; bounded wait loop;
   failure classification per failure-and-resume.md.
3. Record each round: `cluster_id`, `evidence_packet`, `opus_verdict`, `codex_verdict`,
   `final_status` (CONFIRMED | PARTIALLY_CONFIRMED | REJECTED | UNRESOLVED), `rationale`.

Final status is decided on evidence, not on model count: two agreeing models raise
confidence but are not proof. If uncertainty remains after this single round, it stays
UNRESOLVED — do not burn more quota attempting to manufacture agreement. Advance `--to
ADJUDICATION_COMPLETE --artifact 50-targeted-adjudication.json`.
