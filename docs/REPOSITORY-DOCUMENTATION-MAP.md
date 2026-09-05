# Repository documentation authority and reconciliation

Reviewed 2026-09-05 against runtime source
`8ae33444f349ce73c1359b963722e2d16acba630` and installed byte identity.
No persistent Graphify graph exists in this repository; orientation used the tracked
tree, exact source, tests and history. Future exploration uses Graphify first if a
usable graph is added, including coverage/freshness checks before relying on it.

## One current source per concept

| Concept | Canonical current location | Historical/supporting material |
|---|---|---|
| Code and machine contract | `skill/scripts/`, `skill/schemas/`; `audit_council.py describe --json` | Git history |
| Human public contract | `skill/PUBLIC-CONTRACT.md` | `CONTRACTS.md` is a v1 historical contract |
| Skill orchestration | `skill/SKILL.md`, `skill/protocols/`, `skill/prompts/` | Prior versions in Git; executable protocol debt below |
| Current limitations | `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md` | Numbered historical dispositions retained |
| Current state and work | `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`, `docs/chatgpt-project/AUCDEV-BACKLOG.md` | Dated reports and commits |
| Architecture orientation | `docs/chatgpt-project/AUCDEV-ARCHITECTURE-SUMMARY.md` (derived) | `AUDIT-COUNCIL-V2-ARCHITECTURE.md` Phase 0 reconstruction/target design |
| Qualification/install references | `docs/chatgpt-project/AUCDEV-QUALIFICATION-HISTORY.md` | Implementation report installation appendix, original private evidence |
| ChatGPT workflow and refresh | `docs/chatgpt-project/AUCDEV-CONTROL-ROOM-RUNBOOK.md`, `docs/chatgpt-project/AUCDEV-PROJECT-UPDATE-PROTOCOL.md` | No full ZIP refresh cycle |
| Upload selection | `docs/chatgpt-project/PROJECT-SOURCES-MANIFEST.md` | Baseline ZIP historical only |
| Public governance | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/REPOSITORY-PUBLICATION-RECORD.md` | GitHub actual settings readback |

## Inconsistencies and dispositions

| Finding | Treatment in this task |
|---|---|
| Root README absent; public contract only under skill/ | Added repository README linking canonical contract; no duplicate contract |
| Architecture and plan say implementation has not begun | Added historical-snapshot banners; retained original design/evidence |
| CONTRACTS.md claims authority for all implementers but describes v1 | Added superseded/historical banner with current contract link |
| Implementation report says install not done / v1 installed, then appends successful install | Dated sections retained; banner points to current state and later evidence |
| Eval starts at 523 tests, later installation records 555, newest commit claims 574 | Preserved dated results; current checks recorded separately, no retroactive count rewrite |
| Eval says replay executed but later calls it unrun; round-5/install remain listed as pending | Historical banner and current-status addendum replace their use as current gate authority |
| Eval says Tier 4 deferred, but test_tier4_da27c0 exists | Addendum distinguishes implemented 19 deterministic regressions from new live audit evidence |
| Migration says hook opt-in and installation pending | Reconciled current guidance; historical original preserved in Git; no installed skill changed |
| Migration rollback suggests checking old skill into live development tree | Replaced with isolated exact-revision export/backup procedure; no rollback executed |
| Retention proposal old schema count/record-link TODOs | Dated note marks implemented schema/record wiring; proposal and original details retained |
| Worktree roots claimed resolved, but two APIs still have different defaults | Corrected limitations: production creation uses XDG_DATA; resolver XDG_CACHE discrepancy is AUCDEV-013 |
| v2.0.1 label vs protocol 2.0; installed current bytes vs 579e39a install record | Separate identities in CURRENT-STATE/history; missing qualification evidence is AUCDEV-010 |
| evidence-policy still uses lines; quota/resume prose conflicts with SKILL/schema | AUCDEV-009/004/008; executable Markdown left byte-identical in this non-product task |
| Public contract/skill README overbroad write and read-isolation claims, incomplete tables | AUCDEV-012; current orientation documents boundaries without changing installed behavior |
| Dirty fingerprint compares index/status and untracked name/size, not all audited bytes | AUCDEV-018; identified from source and existing tests, no runtime fix in governance work |
| Source TODO/FIXME and historical residuals | Explicit disposition matrix at end of backlog; no hidden future-work list |

The numbered verification history comprises six reported adversarial rounds plus
focused follow-ups; it is not a count of six full production Audit Council runs.
No old implementation claim is promoted into an independent qualification verdict.

## Historical evidence inventory

`IMPLEMENTATION_REPORT.md`, `HARDENING_REPORT_v1.0.1.md`,
`HARDENING_REPORT_v1.0.2.md`, `HARDENING_REPORT_v1.0.3.md`, and
`SMOKE_TEST_RECORD.md` describe v1-era work. The v2 implementation/eval reports
contain dated follow-up evidence. Original retained evidence is not cleanup debris.

The parent Git tree has two gitlinks without .gitmodules:

- `smoke-fixture` → `c2118e01668dab1d12288f4b2a2ca627a2084b00`.
- `smoke-fixture-103` → `12a5e48cb2d66cebbf194ec1d94d685d4f261799`.

These pointer commits do not transfer nested repository objects or untracked logs.
Do not stage their local runtime output, invent remote URLs, or claim a recursive
clone can restore them. AUCDEV-015 tracks portable historical reproductions.

Private original production archives remain outside the publication set. The two
tracked Fifth JSON fixtures contain technical audits of an already-public owner
repository and were reviewed for publication; future fixtures should be reduced
to sanitized deterministic minimums. See the public-safety record for exact scope.
