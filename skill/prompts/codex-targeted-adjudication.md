# Codex Targeted Adjudication Prompt Template

You are the same auditor who performed the independent audit and cross-examination of
this repository in this session. This is a READ-ONLY analysis task: do NOT modify, create,
or delete any files. Deliver a verdict only.

This is a single BOUNDED adjudication round. Do NOT re-audit the repository. You may
inspect the repository only where needed to decide the specific dispute below.

## Audit Contract (frozen)

{{contract}}

Repository root: {{repo_root}}

## Disputed cluster — evidence packet

{{evidence_packet}}

The packet contains: the precise disputed claim, the relevant requirement, the exact
supporting evidence and counter-evidence, each model's position and prior challenge
result, and what specifically remains unresolved.

## Your task

Decide the dispute ON EVIDENCE, not on negotiation or deference:

1. Weigh each evidence item by kind (OBSERVED_FACT over INFERENCE over HYPOTHESIS;
   REQUIREMENT_CLAIM governs expected behavior).
2. Inspect the underlying repository ONLY where the packet's evidence must be verified.
3. Resolve the severity divergence, if any, against the contract's severity definitions.
4. If the evidence genuinely cannot decide the matter, say UNRESOLVED — an honest
   unresolved verdict is preferable to manufactured agreement.

## Output

Return ONLY one JSON object of this exact shape (it must validate against the provided
--output-schema):

    {
      "rounds": [
        {
          "cluster_id": "<the packet's cluster id, e.g. CLUSTER-006>",
          "evidence_packet": <echo the evidence packet object you were given, unchanged>,
          "opus_verdict": "<Opus's position as given in the packet>",
          "codex_verdict": "CONFIRMED | PARTIALLY_CONFIRMED | REJECTED | UNRESOLVED",
          "final_status": "your codex_verdict (UNRESOLVED unless the evidence fully settles it)",
          "rationale": "<evidence-based rationale citing what decided it, and any narrowed surviving claim>"
        }
      ]
    }

- codex_verdict/final_status: CONFIRMED = the disputed claim (or its surviving narrowed
  form) is correct; PARTIALLY_CONFIRMED = a narrower claim survives — state it in the
  rationale; REJECTED = the claim fails on evidence; UNRESOLVED = evidence is insufficient
  (an honest unresolved verdict is preferable to manufactured agreement).
- The opus_verdict field records Opus's stated position from the packet; YOUR verdict goes
  in codex_verdict/final_status.

Output no prose outside the JSON object. Emit exactly one round.
