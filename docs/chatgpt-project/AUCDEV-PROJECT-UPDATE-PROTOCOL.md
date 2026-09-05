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

## Live state and durable Project Sources

Use [PROJECT-SOURCES-MANIFEST](PROJECT-SOURCES-MANIFEST.md) as the single upload list.
Commit CURRENT-STATE/BACKLOG updates after significant transitions, then fetch both
live at session bootstrap and before state-dependent decisions. They do not require
manual upload or replacement per cycle/commit. Optional uploads must be labeled
POTENTIALLY STALE SNAPSHOT with SHA/date; they never replace live resolution.
Refresh the six durable orientation Sources in the manifest when their relevant
contents change, not after unrelated commits. Remove superseded orientation uploads
to avoid ambiguity; retain history in Git. The existing
`audit-council-dev-baseline-2026-09-05.zip` remains HISTORICAL SNAPSHOT ONLY.

If live GitHub cannot resolve the target, provide the exact SHA plus the narrow
changed source/diff/reports; do not use a new full ZIP as the default refresh path.
Updating repository instructions does not update ChatGPT settings automatically:
the operator copies the compact Project Instructions text separately. Procedures
stay in the runbook/architecture/update documents; do not create a duplicate full policy.

## Instructions deployment check

The operator observed an **8,000-character UI maximum** and a rejected paste.
The repository's engineering cap is **7,500 Unicode characters**, preferably
6,000–7,300, counting exact file text including Markdown/newlines. Do not infer
UI acceptance from UTF-8 bytes or rendered Markdown. Run this read-only check after
every Instructions edit, from the repository root:

```sh
python3 - <<'PY'
from pathlib import Path
p = Path('docs/chatgpt-project/AUDIT-COUNCIL-DEV-PROJECT-INSTRUCTIONS.md')
raw = p.read_bytes()
text = raw.decode('utf-8')
print({'unicode_characters': len(text), 'utf8_bytes': len(raw),
       'lines': len(text.splitlines())})
assert len(text) <= 7500, 'Project Instructions exceed engineering cap'
PY
git diff --check
```

Also review these scenarios against the exact compact policy (a manual semantic
review, not proof of model compliance or a paid qualification campaign):

| Scenario | Required policy outcome |
|---|---|
| New conversation with no explicit state | Live default-branch/HEAD resolution and state/backlog fetch before planning |
| GLM implementation report | Verify exact SHA/diff, then neutral independent audit; claims are not audit truth |
| PARTIAL because Codex failed | Separate external/harness/completeness effects; no product PASS |
| Candidate implementation completed | Previously qualified installed auditor; no candidate self-qualification |
| Target SHA changed after remediation | Fresh audit; no inherited verdict |
| LCO production blindness finding | AUCDEV evidence/backlog routing; no LCO remediation takeover |
| Uploaded state conflicts with newer GitHub | Live GitHub wins for current facts; historical events retain their own evidence |
| Autonomous harness requested without policy change | Keep DEFERRED; require explicit operator policy change grounded in workflow evidence |
