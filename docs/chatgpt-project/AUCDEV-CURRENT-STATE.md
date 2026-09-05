# Audit Council Dev — Current State

Last updated: **2026-09-05** (Europe/Istanbul).
Update this file at every significant implementation/audit/remediation/install transition.

| Field | Verified state |
|---|---|
| Canonical local repository | `/home/isa/audit-council-dev` |
| GitHub repository | `https://github.com/isakli05/audit-council-dev` (public, owner `isakli05`; remote `origin`) |
| Current branch | `master` |
| Last verified repository HEAD/checkpoint | `8ae33444f349ce73c1359b963722e2d16acba630` (runtime baseline; governance commits will be descendants) |
| Live current HEAD | Resolve `refs/heads/master` from GitHub or `git rev-parse HEAD`; see SHA recording rule below |
| Runtime source baseline | `8ae33444f349ce73c1359b963722e2d16acba630` |
| Installed skill path | `/home/isa/.claude/skills/audit-council/` |
| Installed operational version | **v2.0.1-equivalent**, inferred from byte-identical source and commit history; no explicit package patch-version marker |
| Installed source HEAD | `8ae33444f349ce73c1359b963722e2d16acba630`; all 84 tracked skill files match; no extra non-cache installed files |
| Installed protocol version | `2.0` from canonical describe/schema; not the package version |
| Currently installed qualified version/HEAD | **UNRESOLVED**: current byte identity does not establish independent qualification |
| Latest documented verified installation | v2.0 source `579e39a409a1b6df58368a7b07dbdbbed5839dd9`, recorded in commit `d0c6008d1bdef5909db31852575a0b6a0685f187` as INSTALLATION_VERIFIED |
| Latest completed qualification status | Historical report records six adversarial rounds/focused re-verification and 555-test installation verification; exact independent v2.0.1 qualification reference not found |
| Current development status | Runtime unchanged; repository governance/ChatGPT documents completed; source push pending final commit checks |
| Active runtime backlog item | None; no feature program started |
| Next runtime objective | Resolve AUCDEV-010 provenance, then choose a bounded candidate scope; do not start it in this governance task |
| Current validation | 574 deterministic tests OK in 94.050 s; installed 84-file identity unchanged; no real model calls; final document checks in publication record |
| Baseline ZIP in ChatGPT | HISTORICAL SNAPSHOT ONLY; filename and embedded SHA unknown |
| Project memory | PROJECT-ONLY MEMORY (operator configuration); not independently inspected in ChatGPT UI |

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

Next candidate qualification is blocked by AUCDEV-010 until auditor provenance is
resolved. A license choice (AUCDEV-014) and real-model evaluation budget/provenance
(AUCDEV-016) also remain unresolved. They do not authorize self-qualification or
automatic model spending. Publication status is recorded separately below.

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

After publication, copy Project Instructions into ChatGPT settings and add the compact
Sources set from [manifest](PROJECT-SOURCES-MANIFEST.md). Verify live GitHub access and
SHA in a new project conversation. Then resolve the qualification evidence gap before
using the installed tree as a predecessor auditor. No new full ZIP upload cycle is needed.

## Recording discipline

This file records a verified checkpoint, not its own containing commit hash.
The commit that records a SHA necessarily has a different SHA. The current branch
tip must therefore be resolved live; the operator handoff supplies the exact final
publication tip. Do not confuse a later governance commit with an audited candidate.
See [update protocol](AUCDEV-PROJECT-UPDATE-PROTOCOL.md).

Evidence: [qualification history](AUCDEV-QUALIFICATION-HISTORY.md),
[backlog](AUCDEV-BACKLOG.md), [documentation map](../REPOSITORY-DOCUMENTATION-MAP.md),
[publication record](../REPOSITORY-PUBLICATION-RECORD.md).
