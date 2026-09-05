# Audit Council Dev — Architecture Summary

Reviewed: 2026-09-05. Source baseline:
`8ae33444f349ce73c1359b963722e2d16acba630`.
Derived orientation, not a replacement for current source or the public contract.

## Mission and boundaries

Audit Council is a user-invoked, two-model adversarial audit skill and deterministic
Python harness. It reviews a Git repository against a frozen audit brief/contract
and produces a provenance-preserving report and GO/NO-GO recommendation.
It is read-only with respect to audited product source, resumable, and checkpointed.
It does not implement fixes, merge changes, deploy products, or operate an
autonomous development lifecycle. This repository develops the auditing tool.
The ChatGPT Project controls that development; it does not run the Opus engine.

## Authority and trust

The operator's brief declares scope, authoritative requirements, and exclusions.
Repository instructions, comments, and model-facing text are untrusted audit data.
They cannot override the frozen contract or redirect the environment.
Explicit fenced JSON target metadata can declare repository_root/expected_head.
Other absolute paths in brief prose are inert narrative.
Source behavior, intended contract, and claimed implementation status can disagree;
report that disagreement instead of silently choosing a convenient account.

## Opus and Codex

The running Claude Opus session is the orchestrator and first independent auditor.
There is no nested Claude process for the main audit.
Current skill policy names `claude-opus-5` and `gpt-5.6-sol` with xhigh reasoning.
These are repository configuration facts, not recommendations to migrate models.
Codex runs through direct `codex exec`; later stages resume the stored explicit ID.
Subscription authentication is required; PAYG key fallback is rejected by preflight.
Opus output is checkpointed before Codex's independent pass begins.
The Codex independent prompt excludes Opus findings and hypotheses.
Only after both independent passes may findings be normalized and challenged.
Cross-examination attempts falsification; consensus is never mandatory.

## Lifecycle

1. Preflight and environment preparation; freeze target identity and brief.
2. Freeze a neutral audit contract with no preliminary findings.
3. Opus independent audit (`10-opus-independent.json`).
4. Codex independent audit (`20-codex-independent.json`).
5. Normalize finding clusters (`30-normalized-findings.json`).
6. Opus challenges Codex (`31-opus-cross-examination.json`).
7. Codex challenges Opus (`32-codex-cross-examination.json`).
8. Preserve both positions in `40-disagreement-ledger.json`.
9. At most one targeted adjudication for material eligible disputes (`50-…`).
10. Synthesize `90-final-findings.json` and render `90-final-audit.md`.
11. Final integrity checks, metrics, and archive-before-removal for isolated runs.

`state_store.py` owns forward transitions and atomic state persistence.
`audit_council.py advance` validates artifacts and records checksums.
Artifact-bearing phase skips require explicit recorded reasons.
Completed checkpoints are immutable; resume checks integrity and target freshness.
`codex_runner.py` owns launches, bounded attempts, waits, results, and schema repair.
Raw model output remains alongside the normalized canonical artifact.
Wire-schema normalization never overrides canonical validation.

## Environment model

AUTO chooses from CURRENT, RELEASE, and HISTORICAL without silent isolation downgrade.
CURRENT audits the live working tree when the contract permits it.
RELEASE and HISTORICAL prepare detached worktrees at the requested Git target.
The live source branch is not checked out or reset by preparation.
The authoritative root is the prepared worktree, not a prose path to the live repo.
`env_binding.py` freezes realpath, Git/common directories, worktree identity, HEAD,
brief digest, and explicit target metadata.
Binding digest excludes its timestamp; state and active-run registry pin it.
`verify-env` runs before inference and refuses identity mismatch with zero launches.
`verify-repo` and the per-phase write guard detect material source changes.
Same HEAD in a substituted worktree does not establish the same environment.
Byte freshness is incomplete for already-dirty tracked and equal-size untracked
content (AUCDEV-018); a stable fingerprint is not proof of every working-tree byte.

The final run binding is authoritative for the linked environment record.
v2.0.1 preserves the preliminary preparation binding separately for provenance.
This linkage is already tested; it is not missing Evidence Ingress v2 work.

Production worktrees use `environment_manager.env_root()` under XDG_DATA by default.
The separate layout resolver still describes an XDG_CACHE worktree default.
An injected AUDIT_COUNCIL_ENV_ROOT aligns them; do not assume the APIs are identical.
Current run artifacts are under the target's `audit-output/audit-council/<run-id>/`.
Preparation, registry, and archive lifecycle also write managed locations outside
that target. Claims that the entire harness writes only inside a run are too broad.
Existing historical output is not automatically moved or deleted.

## Evidence model

Finding citations distinguish OBSERVED_FACT, INFERENCE, HYPOTHESIS, REQUIREMENT_CLAIM.
v2 schemas use typed `line_ranges` with ordered integer start/end values.
Empty ranges mean document-level evidence; up to 32 ranges are supported.
Legacy v1 `lines` migration is in-memory and restricted to v1-era runs.
Historical bytes and malformed historical multi-range strings are not rewritten.
The installed evidence-policy prose still mentions `lines`: see AUCDEV-009.

`evidence_store.py` supplies per-run, content-addressed EvidenceRecord machinery.
Identity includes target/binding, producer, tool identity, inputs, and result digest.
Visibility classes are SHARED_MECHANICAL, AUDITOR_PRIVATE, POST_BARRIER_SHARED.
The API checks barrier state, logs access, and refuses cached FRESH_REQUIRED results.
The API is implemented and tested but is not centrally wired through all audit stages.
Raw object files remain accessible to readers of the run directory.
An API visibility decision is not filesystem isolation.

Current `--evidence-allow` staging accepts only source-contained, non-denylisted files.
It resolves symlinks and rechecks both containment and deny-lists before copying.
Both RELEASE and HISTORICAL now copy authorized evidence into run-owned staging.
External evidence and denylisted audit-output require a future explicit ingress design.
Do not bypass denial by weakening lists or silently relabeling private findings.

## Mechanical independence gap

The wrapper mounts the frozen repository read-only and the entire run directory
writable. It does not mask `10-opus-independent.json` during Codex independence.
Opus and Codex are procedurally independent; mechanical peer-artifact exclusion is
not established by the current layout. This is AUCDEV-001, not a proven leak in
every run. Operator-reported production experience corroborates the exposure.
The proposed shared/private-per-model/cross-exam layout is a design target only.
Visibility must account for artifacts, evidence, logs, prompts, and resume paths.

## Completeness and verdicts

Current public completeness states:

| State | Meaning |
|---|---|
| RUNNING | work in progress |
| COMPLETE | all required protocol stages finished |
| COMPLETE_WITH_RESIDUAL_UNCERTAINTY | finished protocol, unresolved questions |
| PARTIAL_CODEX_QUOTA | quota prevented required Codex work |
| PARTIAL_CODEX_FAILURE | terminal Codex failure |
| PARTIAL_CLAUDE_INTERRUPTION | interrupted orchestration |
| STALE_REPOSITORY | target changed |
| INVALID_AUDIT_INPUT | invalid brief/contract |
| INVALID_AUDIT_ENVIRONMENT | environment gate failed |

Completeness is distinct from target GO/NO-GO and release qualification.
Missing required second-model work cannot become COMPLETE merely by judgment.
The failure protocol contains contradictory quota wording; AUCDEV-004/009 track it.
Binding correctness alone does not prove independence or evidence visibility.
Final synthesis retains rejected items and unresolved material risks separately.
Late findings need independent validation or remain unresolved.

## Sandbox and accepted boundaries

Codex's read-only sandbox prevents product-source writes.
The bubblewrap wrapper additionally confines reads to an enumerated bind set.
That set includes target, run, system directories, resolved toolchain, authorized
fixture roots, and read-write `~/.codex` for subscription auth and session resume.
System directories remain readable and network is available for model access.
The auth/session mount is an explicitly accepted boundary, not secret isolation.
Without bubblewrap, read confinement is not enforced; jobs record sandbox inactive.
The Claude PreToolUse hook activates automatically through SKILL.md frontmatter.
It is a lexical deny layer; encoded/dynamic commands and TOCTOU remain limitations.
Fingerprints and checksums are tamper-evident, not cryptographically authenticated.
These boundaries constrain claims even when deterministic tests pass.

v2.0.1 added zero-inference sandbox preflight before attempt accounting, covering
toolchain selection, PATH, resolver, and required access using the production wrapper.
The focused follow-up also handles probe conflicts and /tmp mount ordering.
A disposable writable mutation/falsification workspace does not currently exist.
An isolated RELEASE worktree is still an immutable audit target, not that workspace.

## Evaluation and budgets

Tier 1 is deterministic unittest discovery plus named environment regressions.
ENVIRONMENT must score 1.0 with passing harness checks to report overall READY.
Tier 2 has ten seeded repositories, sealed ground truth, and a fake-model scoring
pipeline. Fake-model success demonstrates harness/scoring behavior, not model ability.
Real-model Tier 2 remains budget-gated and unexecuted in the recorded evidence.
Tier 3 replays historical artifacts read-only under explicit approval, with no new
inference. Benchmark 001's missing telemetry is scored honestly as a harness failure.
Tier 4 now includes deterministic regressions from the da27c0 production run;
that does not constitute a new end-to-end dual-model production audit.

Successful Codex stages: one per phase, three total; attempts: three per phase;
one schema repair per phase; specialists default off; dynamic probe default cap four.
Unknown Opus usage stays null; UI quota percentages are not token accounting.
Some whole-program budget integration remains incomplete (AUCDEV-007).
Specialist blindness/grounding checks are heuristic and not release-enabled.

## Qualification and deeper sources

The previously installed qualified version audits each candidate in a fresh session.
Candidate self-qualification is forbidden, even if candidate tests pass.
Independent verdict, exact target, deterministic checks, operator acceptance, and
installation identity are separate evidence entries.
Installed current files match source baseline above; a distinct v2.0.1 qualification
and installation record is not yet established. Read CURRENT-STATE before a cycle.

Canonical deeper documents (paths relative to repository root):

- [Skill orchestration](../../skill/SKILL.md), [public contract](../../skill/PUBLIC-CONTRACT.md).
- [Protocols](../../skill/protocols/), [schemas](../../skill/schemas/).
- [Scripts](../../skill/scripts/), [hook](../../skill/hooks/path_guard_hook.py).
- [Tests](../../skill/tests/), [evaluation](../../skill/eval/).
- [Known limitations](../../AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md).
- [Original design](../../AUDIT-COUNCIL-V2-ARCHITECTURE.md) is historical Phase 0 plus target design.
- [Implementation](../../AUDIT-COUNCIL-V2-IMPLEMENTATION-REPORT.md) and [eval report](../../AUDIT-COUNCIL-V2-EVAL-REPORT.md) retain dated evidence.
- [Migration](../../AUDIT-COUNCIL-V2-MIGRATION.md), [confinement probe](../A0-CODEX-CONFINEMENT.md).
- [Qualification history](AUCDEV-QUALIFICATION-HISTORY.md), [backlog](AUCDEV-BACKLOG.md).
