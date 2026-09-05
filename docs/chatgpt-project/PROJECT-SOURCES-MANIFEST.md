# Audit Council Dev — Project Sources Manifest

Add the following files to **Audit Council Dev → Sources** in this priority order.
Paths are relative to the repository root. Do not create convenience copies of the
contract, skill, or limitations at a second canonical path. The seven control-room
documents live here; the actual public contract remains `skill/PUBLIC-CONTRACT.md`.

| Order / class | Repository path | Purpose / authority | Update / manual refresh | Prefer live GitHub? |
|---|---|---|---|---|
| 1 REQUIRED | `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` | Canonical control-room state; facts derived from Git/install evidence | Every significant transition; replace upload when changed | Yes; resolve branch SHA |
| 2 REQUIRED | `docs/chatgpt-project/AUCDEV-BACKLOG.md` | Canonical development queue, evidence, acceptance criteria | Every status/scope decision; replace when changed | Yes |
| 3 REQUIRED | `docs/chatgpt-project/AUCDEV-ARCHITECTURE-SUMMARY.md` | Derived compact orientation; source/schema outranks summary | Architecture/boundary changes; replace when changed | Yes |
| 4 REQUIRED | `skill/PUBLIC-CONTRACT.md` | Canonical human contract, mirrors `describe --json`; tested enum/list facts | Contract changes; replace when changed | Yes; inspect code for conflicts |
| 5 REQUIRED | `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md` | Canonical current limitations with dated historical dispositions | Residual changes; replace when changed | Yes |
| 6 RECOMMENDED | `skill/SKILL.md` | Canonical repository orchestration source; not proof of installed qualification | Skill policy/release changes; replace when changed | Yes; distinguish installed source SHA |
| 7 RECOMMENDED | `docs/chatgpt-project/AUCDEV-CONTROL-ROOM-RUNBOOK.md` | Canonical manual workflow and handoff requirements | Workflow changes; replace when changed | Yes |
| 8 RECOMMENDED | `docs/chatgpt-project/AUCDEV-PROJECT-UPDATE-PROTOCOL.md` | Canonical transition/update and SHA discipline | Record policy changes; replace when changed | Yes |
| 9 OPTIONAL/HISTORICAL | `docs/chatgpt-project/AUCDEV-QUALIFICATION-HISTORY.md` | Canonical index of qualification/install evidence, including unknowns | Audit/install transitions; replace if uploaded | Yes |
| 10 OPTIONAL/HISTORICAL | `AUDIT-COUNCIL-V2-ARCHITECTURE.md` | Historical Phase 0 reconstruction and target design, not current implementation | Retain historical body; refresh only if index/banner changes and needed | Yes for current code, not to reinterpret history |
| 11 OPTIONAL/HISTORICAL | `AUDIT-COUNCIL-V2-IMPLEMENTATION-REPORT.md` | Historical implementation/installation evidence | Dated appendices; replace only if actively needed | Yes |
| 12 OPTIONAL/HISTORICAL | `AUDIT-COUNCIL-V2-EVAL-REPORT.md` | Historical deterministic/fake/replay results, not model qualification | New recorded evidence; replace if actively needed | Yes |
| 13 OPTIONAL/HISTORICAL | Baseline ZIP already uploaded (exact filename/SHA unknown) | **HISTORICAL SNAPSHOT ONLY** | Keep labeled historical; no replacement per commit | Live GitHub always outranks it for current truth |

The compact initial set is entries **1–8**. Entry 9 is useful for qualification
discussions but can be retrieved when needed. Do not upload raw production ZIPs,
private logs, credentials, auth/session state, or smoke-fixture outputs.

Separately, copy the **entire text** of
`docs/chatgpt-project/AUDIT-COUNCIL-DEV-PROJECT-INSTRUCTIONS.md` into
**Project settings → Instructions**. It is settings policy, not another required
Source upload. This manifest itself is the operator's checklist.

## Connect and verify

Connect the published repository to ChatGPT using the GitHub access available to
the operator's account. In a new conversation inside this project, request the
repository's current branch SHA and one source path, and check the response against
GitHub. A public URL or Project Source upload alone does not establish live access.
When retrieval cannot prove freshness, supply the exact SHA and a narrow diff/source
bundle. Do not require a repository ZIP after each cycle.

PROJECT-ONLY MEMORY is the operator-selected configuration. Keep decisions needed
across conversations in these committed records and curated Sources. Uploaded files
are manually refreshed snapshots, not a continuous mirror of the repository.
Project instructions and Sources organize shared context; ChatGPT Projects do not
inherently grant access to this local filesystem. See the official
[Projects and chats documentation](https://learn.chatgpt.com/docs/projects)
(checked 2026-09-05). Account-specific GitHub availability must be verified in ChatGPT.
