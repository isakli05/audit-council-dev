# Audit Council Dev — Current State

Last updated: **2026-09-05** (Europe/Istanbul).
Update this file at every significant implementation/audit/remediation/install transition.

| Field | Verified state |
|---|---|
| Canonical local repository | `/home/isa/audit-council-dev` |
| GitHub repository | `https://github.com/isakli05/audit-council-dev` (public, owner `isakli05`; remote `origin`) |
| Current branch | `master` |
| Last verified repository HEAD/checkpoint | `910339b661d2a18e4690a5bac95ee048e08cbae3` (live GitHub/default-branch checkpoint at start of Instructions optimization; this recording commit is a descendant) |
| Live current HEAD | Resolve `refs/heads/master` from GitHub or `git rev-parse HEAD`; see SHA recording rule below |
| Runtime source baseline | `8ae33444f349ce73c1359b963722e2d16acba630` |
| Installed skill path | `/home/isa/.claude/skills/audit-council/` |
| Installed operational version | **v2.0.1-equivalent**, inferred from byte-identical source and commit history; no explicit package patch-version marker |
| Installed source HEAD | `8ae33444f349ce73c1359b963722e2d16acba630`; all 84 tracked skill files match; no extra non-cache installed files |
| Installed protocol version | `2.0` from canonical describe/schema; not the package version |
| Currently installed qualified version/HEAD | **PENDING EVIDENCE RECONCILIATION**: operator confirms external historical qualification/install evidence; exact linkage not inspected here. Missing Git record does not establish absence |
| Latest documented verified installation | v2.0 source `579e39a409a1b6df58368a7b07dbdbbed5839dd9`, recorded in commit `d0c6008d1bdef5909db31852575a0b6a0685f187` as INSTALLATION_VERIFIED |
| Latest completed qualification status | Published history records six adversarial rounds/focused re-verification and 555-test install verification; reconcile additional operator-held evidence before deciding whether any new qualification is needed |
| Current development status | Runtime unchanged; compact UI policy and mandatory live bootstrap prepared; dynamic state/backlog no longer require per-cycle uploads |
| Active runtime backlog item | None; no feature program started |
| Next runtime objective | First reconcile existing AUCDEV-010 evidence; prioritize AUCDEV-001/009 (P0) for next candidate scope; no runtime program starts in this pass |
| Current validation | PASS: Instructions budget, document links/manifest paths, backlog counts/statuses, eight-scenario policy review and git diff --check; no qualification campaign. Prior 574-test result belongs to initial publication |
| Baseline ZIP in ChatGPT | `audit-council-dev-baseline-2026-09-05.zip` — HISTORICAL SNAPSHOT ONLY; embedded SHA not established |
| Project memory | PROJECT-ONLY MEMORY (operator configuration); not independently inspected in ChatGPT UI |
| GitHub Project access | Connected and verified according to operator; each conversation must still perform actual live retrieval |
| Instructions deployment budget | Observed UI maximum 8,000 characters; exact file must be <=7,500 Unicode characters (target 6,000–7,300) |

## Recent production observations

1. **Recorded**: run `20260904T222609Z-da27c0` exposed Codex wrapper PATH/node/resolver
   failures, missing RELEASE evidence/skill access, and record-vs-binding divergence.
   Source commits ff3f848 and 8ae3344 implement fixes with 19 Tier-4 regression methods.
   Do not reopen those exact fixes as missing; new inference/qualification is separate.
2. **OPERATOR_REPORTED, source-corroborated exposure**: a later v2.0.1 dual-model audit
   showed that Codex could technically read Opus's independent artifact, and external/
   denylisted evidence ingress remained awkward. Run ID, exact target/auditor SHA,
   archive digest, and final completeness are **unknown** here. AUCDEV-001/002/004/005.
3. Historical Benchmark 001 and Fifth runs exposed malformed citation/telemetry and
   partial-stage issues. Recorded replay preserves these failures; it is not a new audit.

## Blockers and residuals

AUCDEV-010 is P1/READY for existing evidence reconciliation, not a claim that
qualification is absent. First reconcile/import public-safe references to the
operator's historical records. Use of the installed tree as a qualified predecessor
still needs verified linkage; consider a new expensive audit only if existing
evidence is insufficient and the operator authorizes it. License choice (AUCDEV-014)
and real-model evaluation budget/provenance (AUCDEV-016) remain blocked.

Focused priority review: AUCDEV-001 and AUCDEV-009 are now P0/READY because the
documented peer-artifact exposure and executed protocol contradictions affect core
independence/completeness guarantees. This does not invalidate all prior audits.
Counts: 19 open — P0 2, P1 6, P2 11; statuses READY 9, OPEN 8, BLOCKED 2.

Prioritized remaining work includes mechanical independence, exact dirty-target byte
freshness (AUCDEV-018), completeness/visibility linkage, executable protocol drift,
authorized ingress, and disposable mutation experiments. None is implemented here.

Accepted residuals: Claude lexical/TOCTOU limits; unkeyed integrity; Codex auth/session
mount; readable system directories and inactive-bwrap posture; unknown usage/generic
failure parsing; heuristic evidence/specialist guards; host-deleted registry entries;
shallow instruction-file discovery. See the backlog's eight residual entries and
the canonical [known limitations](../../AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md).
Specialists stay default-off; fully autonomous development/audit lifecycle is DEFERRED.

## Next operator action

Copy the compact Project Instructions AS-IS into settings. Use the six durable
orientation Sources in [manifest](PROJECT-SOURCES-MANIFEST.md). Fetch CURRENT-STATE
and BACKLOG live at every new conversation and before state-dependent decisions;
no manual per-cycle upload refresh is required. Confirm the resulting LIVE CONTEXT.
Then reconcile existing qualification evidence before treating the installed tree
as a qualified predecessor. Keep the baseline ZIP historical.

Published refs: `master` and `v1.0.3-baseline`; only owner `isakli05` has admin/write
access. PRs are collaborator-only; Issues/Discussions/Wiki/Projects disabled;
master deletion/non-fast-forward rules active; Actions token read-only with PR
approval disabled. No GitHub setting is awaiting manual configuration.

## Recording discipline

This file records a verified checkpoint, not its own containing commit hash.
The commit that records a SHA necessarily has a different SHA. The current branch
tip must therefore be resolved live; the operator handoff supplies the exact final
publication tip. Do not confuse a later governance commit with an audited candidate.
See [update protocol](AUCDEV-PROJECT-UPDATE-PROTOCOL.md).

Evidence: [qualification history](AUCDEV-QUALIFICATION-HISTORY.md),
[backlog](AUCDEV-BACKLOG.md), [documentation map](../REPOSITORY-DOCUMENTATION-MAP.md),
[publication record](../REPOSITORY-PUBLICATION-RECORD.md).
