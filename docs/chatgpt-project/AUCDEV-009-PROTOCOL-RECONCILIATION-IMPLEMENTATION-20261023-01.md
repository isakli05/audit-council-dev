# AUCDEV-009 protocol reconciliation — implementation evidence, 2026-10-23

Status: **IMPLEMENTATION_COMPLETE / AWAITING_INDEPENDENT_REVIEW**; BACKLOG P0 / IN_PROGRESS, not DONE. This is implementation evidence, not an independent audit, release qualification or installation decision.

## Authority and identity

The current operator request explicitly authorizes this bounded correction and adopts the existing label-specific `COMPLETENESS_MANDATORY_PHASES` in `skill/scripts/state_store.py` as the shared AUCDEV-004/009 policy. The [canonical preparation record](AUCDEV-CGR005-NOGO-AND-AUCDEV009-SCOPE-20261023-01.md) remains historical; its preparation-only routing is superseded by that current approval.

Live default branch `master`, remote HEAD/master and local HEAD were verified at exact baseline `39e837c1b9c7f07b5445cfdc9a10533f4b801622` before modification. CURRENT-STATE/BACKLOG were fetched live at that SHA and matched local Git/working-tree bytes. Tracked baseline was clean; unrelated pre-existing untracked artifacts/submodule content were left untouched. No Graphify graph exists. Candidate branch: `aucdev009-protocol-reconciliation-20261023`. Exact final commit SHA, diffstat, file hashes, validation output and the single archive identity are recorded in the external consolidated handoff; a committed record cannot contain its own final SHA. Canonical master is not advanced by this work.

## Policy-to-change mapping

| Approved policy | Implementation / evidence |
|---|---|
| COMPLETE: both independent passes, both cross-examinations, ledger and synthesis; adjudication only through documented skip | Failure/resume states and matrix, SKILL synthesis rule, PUBLIC-CONTRACT rows; per-surface/per-label derivation and finite truth table against the normative matrix |
| Residual completeness: both independents and synthesis, only already-permitted quota omissions with explicit provenance | Quota wording distinguishes transition-bound cross-exam skips from script-mediated adjudication skips; existing quota residual path retained, disputes remain UNRESOLVED; omissions never claimed as performed/full council success |
| Missing independent work remains PARTIAL | All three surfaces; real state-store rejection checks plus existing B-001 finalize/skip regressions |
| Exact stored Codex session; missing/invalid identity stops | All three surfaces; runner's fresh-launch construction remains disclosed as AUCDEV-008 runtime gap, not claimed fixed |
| Checksum/schema failure stops without rewriting/repeating checkpoints | All three surfaces; synthetic state-schema failure byte preservation and existing checksum-tamper/immutable-resume checks; schema failure not falsely described as uniformly exit 8 |
| Failed environment admission, zero inference through failed gate, no product verdict | All three surfaces; finalize's unsupported environment label explicitly distinguished from admission status |
| Citation consistency and compatibility | All five scoped instruction sources inventoried: one concrete two-range public example and two actual N-placeholder fragments, validated in eight evidence locations across five canonical schemas plus normalization/admission range checks; malformed examples pass through the same extractor; v1 fixture migration preserves source/input bytes |

Product write set: `skill/protocols/failure-and-resume.md`, narrowly corresponding `skill/SKILL.md` / `skill/PUBLIC-CONTRACT.md`, and new `skill/tests/test_protocol_consistency.py`. Governance write set: this record, CURRENT-STATE, BACKLOG. Runtime Python scripts, schemas, other protocols/prompts, frozen models/efforts, budgets, first-pass blindness and historical artifacts remain unchanged. The two cited citation instruction sources were already correct and stayed read-only; the legacy-lines correction was not reimplemented. No protocol version change: wording is reconciled to existing label enforcement, with no field/schema/runtime change.

## Validation

Exactly one bounded offline targeted pass, exit 0: **136 passed / 0 failed / 0 errors / 0 skipped**, 8.260 seconds, no warnings and no reruns (33 new consistency tests). Command from repository root:

```sh
PYTHONPATH=skill/tests:skill/scripts python3 -m unittest -v test_protocol_consistency test_schema_validation test_line_ranges_v2 test_migration_compat test_public_contract test_resume test_b001_b004_remediation.TestRB001CompletenessIntegrity test_b001_b004_remediation.TestRB001SkipLaunchBinding test_qx_stabilization.TestV2EvidenceFieldAlignment
```

`git diff --check` and the seven-path final inventory are recorded in the consolidated handoff. GLM also performed compile and ad hoc static checks during preparation; those are not independent acceptance evidence. Broader/full suite, real `/audit-council`, historical replay, independent release/auditor campaign, qualification and installation checks were not run under this budget.

## Review corrections, deviations and remaining limits

GLM-5.3 owned routine implementation/test authoring. Codex reviewed source and the actual diff, corrected false exit-code/finalize claims, skip-mechanism assumptions, weak citation extraction and unbound label checks. The final GLM invocation hit its turn cap after writing changes; its process exit was 1 and was not treated as successful completion. Codex inspected the written result, made three small integration corrections (supported run-state failure reason, synthesis sequencing, closed recursive file reads) and verified the final candidate through the targeted pass. Intermediate static-check failures and the capped invocation do not disappear behind the green suite; task artifacts retain their disposition.

Tooling deviation: `zcode --help` unexpectedly launched the desktop app; its task-owned command exited after Ctrl-C. The operator supplied `cc-zai --dangerously-skip-permissions`, which was used for the GLM-5.3 work. Desktop startup logs/application-state effects are not represented as product evidence; no claim of zero app-state effects is made. Raw logs/transcripts are excluded from the handoff.

Text/schema/source consistency is finite evidence, not proof of model compliance or runtime hardening. AUCDEV-001, the wider AUCDEV-004 objective, AUCDEV-008 missing-session enforcement and AUCDEV-010 qualification provenance are not fully resolved. **CGR-005 remains NO-GO / OPEN / BLOCKING.** No runtime/schema scope expansion was necessary. No installed Audit Council inspection/mutation, protected host/Root/disk/VM/NBD operations, credential-content access, historical private evidence access or historical replay occurred.

Publication: local development-branch commit only; no push or fast-forward of master. No independent release qualification or installation was performed. Qualification history is unchanged because neither event occurred.

Recommended next action: arrange independent review of the exact candidate, first satisfying the separate AUCDEV-010 predecessor-provenance and execution-authority gates; this record initiates no audit.
