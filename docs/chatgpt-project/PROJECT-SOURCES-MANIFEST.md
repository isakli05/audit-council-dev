# Audit Council Dev — Project Sources Manifest

Operating decision: 2026-09-05. The operator reports GitHub access connected and
verified. Each conversation must still retrieve live context; a connection alone
does not prove freshness. Paths below are repository-relative.

## LIVE GITHUB CURRENT TRUTH

These dynamic files are REQUIRED LIVE READS, not required Project Source uploads:

| Repository path | Purpose / authority | Update frequency | Manual upload/refresh |
|---|---|---|---|
| `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` | Canonical current control-room record, derived from cited Git/install evidence | Significant transitions | Not required |
| `docs/chatgpt-project/AUCDEV-BACKLOG.md` | Canonical priorities, statuses, scope and acceptance | Status/scope/priority decisions | Not required |

At every new conversation and before a state-dependent decision, resolve the live
default branch and full HEAD of **isakli05/audit-council-dev**, fetch both files at
that SHA, then report LIVE CONTEXT before planning. Follow the
[runbook bootstrap](AUCDEV-CONTROL-ROOM-RUNBOOK.md#mandatory-live-session-bootstrap).

Do not upload/replace these files after every development cycle or commit. If the
operator keeps optional uploaded copies, label them **POTENTIALLY STALE SNAPSHOT**
with their source SHA/date. They cannot establish current HEAD, installed stable
state, backlog status or active program without live resolution. Existing uploads
may be removed from Sources or kept as labeled snapshots; canonical history stays in Git.

## UPLOADED DURABLE ORIENTATION SOURCE

Recommended compact upload set, in priority order. These are relatively stable
orientation references, not a competing authority for current repository state.
Live GitHub/source at the applicable SHA wins for current facts; historical
evidence still governs the event it records.

| Order / class | Repository path | Purpose / canonical vs derived | Update / manual refresh |
|---|---|---|---|
| 1 RECOMMENDED | `docs/chatgpt-project/AUCDEV-ARCHITECTURE-SUMMARY.md` | Derived architecture/trust orientation | Architecture/boundary changes; replace upload when materially changed |
| 2 RECOMMENDED | `skill/PUBLIC-CONTRACT.md` | Canonical human contract, mirrors describe/schema | Contract changes; replace when changed |
| 3 RECOMMENDED | `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md` | Canonical limitations and dated dispositions | Residual changes; replace when changed |
| 4 RECOMMENDED | `skill/SKILL.md` | Canonical repository orchestration; not installed qualification proof | Skill policy/release changes; replace when changed |
| 5 RECOMMENDED | `docs/chatgpt-project/AUCDEV-CONTROL-ROOM-RUNBOOK.md` | Canonical detailed workflow/handoffs | Workflow changes; replace when changed |
| 6 RECOMMENDED | `docs/chatgpt-project/AUCDEV-PROJECT-UPDATE-PROTOCOL.md` | Canonical record/refresh discipline | Policy changes; replace when changed |

Refresh these uploads when their relevant contents change, not after unrelated
commits. Do not create convenience copies of canonical skill/contract/limitations.

## HISTORICAL SNAPSHOT

| Class / source | Purpose / authority | Refresh / current-truth rule |
|---|---|---|
| OPTIONAL/HISTORICAL: `audit-council-dev-baseline-2026-09-05.zip` (already uploaded; not a repository path) | **HISTORICAL SNAPSHOT ONLY**; embedded SHA not established here | Keep its historical label; never replace per commit or use as current source |
| OPTIONAL/HISTORICAL: `AUDIT-COUNCIL-V2-ARCHITECTURE.md` | Original Phase 0 reconstruction/target design | Retrieve when needed; historical body remains evidence, not current implementation |
| OPTIONAL/HISTORICAL: `AUDIT-COUNCIL-V2-IMPLEMENTATION-REPORT.md`, `AUDIT-COUNCIL-V2-EVAL-REPORT.md` | Dated implementation/eval events | Retrieve relevant version/event; not current HEAD or a new qualification verdict |

`docs/chatgpt-project/AUCDEV-QUALIFICATION-HISTORY.md` is an OPTIONAL live reference
index, updated on evidence reconciliation/audit/install transitions. Fetch it when
needed. A missing index entry does not prove qualification absent; reconcile
operator-held historical evidence first. Historical evidence is authoritative for
its recorded event, not every later version. Import only public-safe summaries/
references/digests; keep sensitive original archives private.

## Project settings and unavailable retrieval

Copy the entire text of
`docs/chatgpt-project/AUDIT-COUNCIL-DEV-PROJECT-INSTRUCTIONS.md` into
**Audit Council Dev → Project settings → Instructions**. This is the compact UI
policy (at most 7,500 Unicode characters), not another required Source upload.
Detailed procedures stay in the existing runbook, update protocol and architecture
summary; there is no second “full instructions” file.

If live access fails, state that limitation and require/use an exact SHA plus
relevant source/diff/evidence before an execution-critical prompt. Uploaded dynamic
snapshots alone are insufficient; never claim a live lookup happened when it did not.
Do not default to a new full ZIP or publish raw production/auth/session archives.

PROJECT-ONLY MEMORY remains the operator configuration. Context organization does
not itself grant local filesystem access. See the previously consulted official
[Projects and chats documentation](https://learn.chatgpt.com/docs/projects).
