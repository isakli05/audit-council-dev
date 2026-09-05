# Audit Council Dev — Qualification and Installation Evidence Index

Updated 2026-09-05. This index distinguishes recorded claims, current filesystem
facts, and independent qualification evidence. It does not issue a new release verdict.

| Record | Source identity | Evidence / status |
|---|---|---|
| v1.0.3 baseline | Tag `v1.0.3-baseline`, commit `1a9023714da3a223c009668569d4bfd0ece5dd22` | Historical hardening report records 160 installed tests and discovery; rollback directory exists |
| v2.0 qualification-era revisions | Multiple commits through `68ce12acc6c614d1876b902e6511d21f95b33c43` | Implementation report describes six adversarial verification rounds, scoped follow-ups and passing re-verification; original independent auditor archives not imported here |
| Latest committed installation verification | Source `579e39a409a1b6df58368a7b07dbdbbed5839dd9`; record commit `d0c6008d1bdef5909db31852575a0b6a0685f187` | INSTALLATION_VERIFIED, 555 installed-copy tests and hooks shipped, according to the dated implementation report |
| v2.0.1 operational hardening | `ff3f848f6ce0169eb985f03712d603538868948b`, then `8ae33444f349ce73c1359b963722e2d16acba630` | Source and 19 Tier-4 regression methods confirm implementation; latter commit reports 574 tests. This is not a standalone release qualification certificate |
| Installed filesystem inspection, 2026-09-05 | 84 tracked skill files exactly match `8ae33444f349ce73c1359b963722e2d16acba630:skill` | Observed byte identity, no extra non-cache files. No distinct v2.0.1 install/independent qualification record found in the repository or installed skill directory |

Current installed path: `/home/isa/.claude/skills/audit-council/`.
Skill tree Git object: `0908c6b70e9a8eb9efeb01e5395dcb486053d4d4`.
Content manifest SHA-256:
`bc2a0995e2bb15d959ea75d4e41f8ba5d5b3e66cb03d26b396844ef0e73812d8`.
Manifest method: sorted `git ls-files skill` entries mapped to relative path and
SHA-256 of each file; hash compact JSON array of `[relative_path, sha256]` pairs.
Generated `__pycache__`/`.pyc` are excluded; they are not release source.

The installed operational label is **v2.0.1-equivalent**, inferred from source
identity and commit descriptions. There is no package patch-version marker or
v2.0.1 tag; `describe --json` identifies **protocol 2.0**, which is a different fact.
The currently installed **qualified** version/source cannot be certified from the
available records. The latest documented installation source is the older v2.0
`579e39a409a1b6df58368a7b07dbdbbed5839dd9`. Do not quietly attach its verification
to the later source. AUCDEV-010 is blocked pending actual evidence or predecessor selection.

Rollback directory observed:
`/home/isa/.claude/skills/audit-council.v1.0.3-rollback-20260905/`.
The old installation report claims byte identity to the baseline; a new rollback
operation must verify the exact selected predecessor and preserve the installed copy.
No installation, downgrade, model audit, or historical replay was performed by
this governance task.

For each future audit/install append: date; backlog IDs; auditor qualified version
and full source SHA; candidate full SHA; run/contract/binding/fingerprint/digests;
completeness; independent verdict; residuals; operator acceptance; installed tree
identity/checks; rollback reference. Keep originals immutable and private when needed.

References: [implementation report](../../AUDIT-COUNCIL-V2-IMPLEMENTATION-REPORT.md),
[eval report](../../AUDIT-COUNCIL-V2-EVAL-REPORT.md),
[v1.0.3 hardening](../../HARDENING_REPORT_v1.0.3.md),
[current state](AUCDEV-CURRENT-STATE.md), [bootstrap runbook](AUCDEV-CONTROL-ROOM-RUNBOOK.md).
