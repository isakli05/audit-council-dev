# Audit Council Dev — Project Update Protocol

Canonical records live in Git. ChatGPT edits described in a conversation are
proposals until an authorized coding agent/operator commits them. Uploads are
snapshots; a GitHub connection does not guarantee a particular retrieved SHA.

| Event | Required repository updates | Evidence required |
|---|---|---|
| Objective accepted | CURRENT-STATE active item; BACKLOG scope/status | ID, baseline SHA, authority, dependencies |
| Implementation completed | CURRENT-STATE; BACKLOG; dated implementation report | Base/final SHA, diff, checks, deviations, risks |
| Independent audit received | CURRENT-STATE; BACKLOG findings; qualification history/reference | Auditor source/install identity, exact target, run/checksums, completeness, verdict |
| Remediation completed | CURRENT-STATE; BACKLOG dispositions; remediation report | Finding IDs, old/new SHA, changes, checks, fresh re-audit need |
| Qualification decision | CURRENT-STATE; BACKLOG; qualification history | Exact audited SHA, independent evidence, operator decision, residuals |
| Installation completed | CURRENT-STATE stable installation; qualification history installation row | Qualified SHA, installed byte identity, checks, rollback |
| Production harness observation | CURRENT-STATE; linked BACKLOG item; sanitized observation/reference | Origin/version/SHA if known, evidence class, impact, reproduction |
| Publication/governance changed | CURRENT-STATE pointer; publication record | Actual GitHub settings readback, visibility, refs, safety result |

Update architecture summary only when architecture, boundaries, or its factual
baseline changes. Update SKILL/protocol/schema/public-contract together when a
separately authorized product change alters their semantics. Do not edit static
architecture documents after every small fix. Historical reports are append-only
evidence with a dated status banner; never retroactively turn a failed audit green.

## SHA and status rules

Record full SHAs for implementation base/result, audited candidate, qualified
predecessor, and installed source. Development HEAD is not a release certificate.
No committed file can contain its own final commit hash without changing that hash.
CURRENT-STATE therefore records a full **last verified repository checkpoint** and
the canonical branch ref; its recording/publication commit may be a descendant.
Resolve the current tip with `git rev-parse HEAD` locally or the GitHub branch API.
The operator handoff reports that exact final tip. Never relabel a checkpoint as a
later audited target. A new candidate SHA always needs a fresh audit.

Each state update has a date, evidence/reference, and explicit unknowns. A report
claim, a deterministic test result, an independent verdict, and an operator
acceptance are four different facts. Do not overwrite earlier qualification rows;
append a row explaining supersession, remediation, or missing evidence.

BACKLOG status transitions require evidence: READY has bounded acceptance criteria;
IN_PROGRESS has an active authorized implementer; BLOCKED names the dependency;
DONE cites source plus validation/decision appropriate to the task. Accepted
residuals need rationale and a revisit trigger. Do not convert DEFERRED to READY
without an explicit prioritization decision. Counts exclude DONE and residuals from
open totals; DEFERRED is reported separately.

## Refresh ChatGPT Project Sources

Use [PROJECT-SOURCES-MANIFEST](PROJECT-SOURCES-MANIFEST.md) as the single upload list.
Replace changed CURRENT-STATE/BACKLOG after significant transitions; replace other
uploaded files only when their canonical contents change. Remove the superseded
upload from active Sources so two snapshots do not silently compete. Keep original
history in Git. Check the filename and source SHA/date in the new conversation.
The baseline ZIP remains HISTORICAL SNAPSHOT ONLY and need not be replaced.

If live GitHub cannot resolve the target, provide the exact SHA plus the narrow
changed source/diff/reports; do not use a new full ZIP as the default refresh path.
Updating repository instructions does not update ChatGPT settings automatically:
the operator copies the full Project Instructions text separately.
