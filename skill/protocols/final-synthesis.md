# Protocol: Final Synthesis (Phase 7) — spec §24/§25

The final report is compiled FROM THE ADJUDICATED LEDGER (and, where run, adjudication
rounds). The compiler — the running Opus session — MUST NOT invent new findings, upgrade
severities without ledger support, or resolve disputes the evidence did not resolve.

## Inclusion rules (per ledger cluster status)

- CONSENSUS → primary findings.
- CONFIRMED_AFTER_CHALLENGE → primary findings.
- NARROWED → primary findings, stating ONLY the narrowed evidence-supported claim (scope,
  cause, severity as narrowed), not the original broader claim.
- REJECTED → excluded from primary findings; retained in `rejected_appendix` (high-value
  false positives are worth keeping visible, with the counter-evidence that rejected
  them).
- UNRESOLVED CRITICAL/HIGH → included explicitly as unresolved risk
  (`unresolved_risks`), never silently dropped or softened.
- UNRESOLVED MEDIUM/LOW → `residual_risks` appendix, unless contract scope requires
  prominence.
- Late findings: include only if independently validated by the other model
  (`provenance.validated_by` set); otherwise they are UNRESOLVED and follow the
  unresolved/residual rules.
- DISPUTED clusters that did not receive adjudication (ineligible) are represented as
  unresolved at their severity (CRITICAL/HIGH → unresolved_risks; MEDIUM/LOW →
  residual_risks) with both positions stated.

## Provenance preservation (mandatory)

Every final finding entry (final-findings.schema.json item) carries `provenance` and the
full chain, e.g.:

    Origin: CODEX-012 → Opus challenge: CONFIRMED → (Codex re-evaluation where applicable)
    → Final status: CONSENSUS

Concretely: preserve `discovered_by`, `independently_confirmed_by[]`, `challenged_by`,
`challenge_result`, `adjudication_result`, and the `member_finding_ids` behind the
cluster. Do not hide disagreement — where models diverged, the divergence appears in the
report.

## Artifact construction

`90-final-findings.json` (final-findings.schema.json) — required: `completeness_state`
(honest: COMPLETE only for a fully council-verified run; see failure-and-resume.md for
partial states), `repository_fingerprint_sha256`, `executive_summary`, `findings[]`.
Optional but expected for a full run: `methodology`, `rejected_appendix[]`,
`unresolved_risks[]`, `residual_risks[]`, `coverage_gaps[]` (from requirement_coverage),
`limitations[]`, `claims_lacking_second_model[]` (mandatory content when completeness is
partial: exactly which claims never received second-model adjudication).

Each primary finding item: `cluster_id`, `title`, `category`, `severity`,
`final_status`, `claim` (the adjudicated claim), `provenance`, `evidence[]`.

Then: `advance --to FINALIZED --artifact 90-final-findings.json --stdin`, and
`AC render --run "$RUN" --artifact 90-final-findings.json` → `90-final-audit.md`.

## Rendered report sections (render_report.py, spec §25)

Executive summary; audit scope and repository identity (root, HEAD SHA, fingerprint,
dirty-state note); audit completeness status; methodology (independent → falsification →
ledger → bounded adjudication); evidence hierarchy (OBSERVED_FACT / INFERENCE / HYPOTHESIS
/ REQUIREMENT_CLAIM); confirmed findings ordered by severity; systemic/root-cause
findings; requirement coverage gaps; rejected high-value false positives; unresolved
disputes; residual risks; audit limitations; model provenance summary; run metrics
reference (`99-run-metrics.json`).

No marketing prose. No inflated claims. Do not hide disagreement.

## Completion

After FINALIZED: run `AC write-guard --run "$RUN"` (exit 5 → stop and report the
invariant violation precisely; never reset files). State reaches COMPLETE via the script.
Report to the user: run directory, completeness state, and the path to
`90-final-audit.md`.
