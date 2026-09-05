# Audit Council Dev — Control-Room Runbook

This is a manual, human-in-the-loop development workflow for Audit Council itself.
The fully autonomous lifecycle remains deferred. Instructions and implementation
prompts default to English; operator discussion may be Turkish.

## Start a cycle

Read [CURRENT-STATE](AUCDEV-CURRENT-STATE.md) and [BACKLOG](AUCDEV-BACKLOG.md).
Retrieve current GitHub source and resolve its exact SHA; if unavailable, declare
the limitation and obtain the narrow source/diff needed for this objective.
The baseline ZIP is historical. Memory and implementation reports cannot certify HEAD.
Choose one READY objective; reconcile its evidence and dependencies before work starts.
Record the operator's scope/authority and validation budget; existing approval persists.

## Stage sequence and handoffs

| Transition | Required handoff | Exit condition |
|---|---|---|
| Backlog → implementation prompt | ID; baseline full SHA; scope; non-goals; files/contracts; held invariants; acceptance checks; budget; stop conditions | Bounded, reviewable implementation scope |
| Implementer → control room | Base/final SHAs; branch; clean/dirty state; diff/stat; files; commands/results; failures; deviations; unresolved risks; report path | Claims checked against exact source and tests |
| Control room → independent audit | Qualified auditor version/source SHA and installation identity; candidate full SHA; environment mode; neutral brief; requirements; exclusions; evidence authorization; budget | Auditor provenance available; target frozen; no expected verdict |
| Fresh Opus session → /audit-council | Invoke installed predecessor skill; prepare/freeze the exact candidate; keep model-independent stages blind | Valid run, binding, contract, and explicit scope |
| Auditor → control room | Run ID; target SHA/root/fingerprint/binding; auditor identity; checksums; canonical/human reports; findings/ledger; failed/skipped stages; metrics; residuals | Integrity/completeness and evidence assessed |
| Control room → remediation | Finding IDs; bounded fixes; held invariants; counter-evidence; acceptance checks; new candidate SHA required | Every finding has a disposition |
| Remediation → re-audit | Old/new SHAs; diff; prior findings; held invariants; changed trust boundaries; fresh run brief | New SHA audited; old verdict not inherited |
| Qualification → installation | Exact independently audited source; verdict/completeness; deterministic evidence; accepted residuals; operator decision; rollback identity | Qualification recorded separately from implementation |
| Installer → control room | Qualified SHA; installed path/tree identity; hooks shipped; installed-copy validation; discovery; rollback; no historical mutation | Stable installation provenance agrees |
| Any significant transition → records | State/backlog/report or qualification/installation update | Committed canonical records; uploaded copies refreshed as needed |

## Bootstrap gate

The previously installed RELEASE-QUALIFIED Audit Council audits a candidate.
A candidate cannot audit itself to become qualified. For example, qualified
installed v2.0.1 audits candidate v2.0.2, then installed qualified v2.0.2 can audit
the next candidate. Version strings are illustrative; use discovered facts.
Byte identity establishes installed contents, not who qualified them.
If current installed bytes lack a qualification reference, first recover that
reference or choose a proven predecessor. Keep candidate qualification blocked.
Do not reinstall, downgrade, or overwrite the installed skill just to hide the gap.

The repository currently records an older verified v2.0 installation and a newer
v2.0.1-equivalent installed tree; see [qualification history](AUCDEV-QUALIFICATION-HISTORY.md).
This documentation/publication task does not certify or install a runtime release.

## Implementation prompt template

```text
Objective: <backlog ID and bounded result>
Repository and baseline: <URL/local path>, <full SHA>, <branch>
Scope / non-goals: <precise boundaries>
Requirements and source: <canonical paths, relevant tests>
Held invariants: <properties that must remain true>
Implementation constraints: <compatibility, safety, budget, existing authority>
Acceptance criteria and validation: <observable outcomes and commands>
Stop conditions: <new trust boundary, missing requirement, unexpected mutation>
Handoff: base/final SHA, diff, files, tests/results, risks, report,
CURRENT-STATE/BACKLOG changes. Do not claim independent qualification.
```

## Fresh audit brief template

```text
Task: independently audit Audit Council candidate <full SHA>.
Auditor: installed qualified <version>, source <full SHA>, qualification <ref>.
Target: <candidate repository>; environment <RELEASE or justified alternative>.
Requirements: <objective and canonical requirements, no expected findings>.
Scope/exclusions: <bounded surface and unchanged invariants>.
Evidence: <explicit authorized sources and visibility; private material withheld>.
Validation budget: <bounded deterministic work / authorized inference>.
Report: exact target/binding, completeness, findings, counter-evidence,
provenance, residuals, failures/skips, and independently reached recommendation.
```

In RELEASE/HISTORICAL the frozen root is the detached prepared worktree. Do not
put the live repository root into authoritative target metadata if it will differ.
Have preparation establish the exact target root, then verify the binding and SHA.
Do not insert implementation conclusions or expected findings into independent
prompts. Cross-examination can receive peer artifacts only after the barrier.
Current raw filesystem blindness is incomplete; disclose AUCDEV-001 per run.

## Audit ZIP/report review

Inspect archives in an isolated temporary location without executing their content.
Reject traversal/symlink escapes and keep private archives out of Git. Obtain
canonical files rather than trusting a rendered GO sentence. Verify the checksum
manifest, state, contract, target/binding linkage, ledger and final findings.
Record what is missing; never reconstruct missing auditor outputs from implementer text.

Classify each observation: Audit Council product defect, harness/protocol defect,
completeness limitation, external condition, accepted residual, or informational.
Attach its source and confidence. External DNS/auth/quota failure can coexist with
an actionable harness failure; it is not automatically a target product defect.
COMPLETE_WITH_RESIDUAL_UNCERTAINTY requires completion of mandatory protocol stages.
PARTIAL/INVALID/STALE results cannot silently satisfy release qualification.

## Remediation and qualification

Prefer fixes that directly resolve evidenced findings. Re-audit scope is compiled
manually from prior findings, held invariants, the diff, and changed trust boundaries.
Narrow scope when justified, but always use a fresh run for a changed target SHA.
Do not transfer a verdict across a post-audit documentation commit either: identify
the qualified runtime source separately from the later governance repository tip.
Qualification records cite the audited SHA, not merely a version or latest branch.
The auditor reaches its own verdict; the operator records the acceptance decision.

## Production feedback from other products

Record only the harness lesson, sanitized reproduction, and public-safe references.
Keep originating product findings in their own project. A narrative-only report is
marked OPERATOR_REPORTED until direct artifacts establish the details. Missing run
ID/SHA stays unknown. Preserve originals privately; do not upload full run logs here.

## Finish the transition

Follow [update protocol](AUCDEV-PROJECT-UPDATE-PROTOCOL.md), commit the records, and
refresh only changed curated Project Sources. Copy Project Instructions into the
settings only when their policy changes. GitHub retrieval is preferred for live
code; connected access must be checked in the actual ChatGPT conversation.
