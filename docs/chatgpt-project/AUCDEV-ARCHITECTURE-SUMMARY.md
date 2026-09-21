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

## AUCDEV-023 exceptional auditor-bootstrap governance

Governance adopted 2026-09-19 by explicit operator decision — governance/
policy acceptance ONLY. This is NOT runtime/current Audit Council product
functionality, and adoption granted no execution authority. A bounded EBS
implementation candidate was published 2026-09-19 under separate bounded
implementation authority (canonical report:
[AUCDEV-023-EBS-IMPLEMENTATION-REPORT](AUCDEV-023-EBS-IMPLEMENTATION-REPORT.md));
the Control Room readback of that candidate returned
PARTIALLY_ACCEPTED / REMEDIATION_REQUIRED with three OPEN/BLOCKING findings
(AUCDEV023-CR-EBS-001/-002/-003; canonical record:
[AUCDEV-023-EBS-IMPLEMENTATION-READBACK](AUCDEV-023-EBS-IMPLEMENTATION-READBACK.md)),
and a bounded REMEDIATION candidate now exists under `bootstrap-supervisor/**`
(published 2026-09-19 under the operator's bounded remediation authority:
complete mandatory transport binding; structurally closed one-shot authority
with no revival and read-only record inspection; runtime package
self-identity verification pinned non-circularly in the binding; canonical
report:
[AUCDEV-023-EBS-REMEDIATION-REPORT](AUCDEV-023-EBS-REMEDIATION-REPORT.md)).
The fresh Control Room readback of that remediation candidate returned
PARTIALLY_ACCEPTED / SECOND_BOUNDED_REMEDIATION_REQUIRED (canonical record:
[AUCDEV-023-EBS-REMEDIATION-READBACK](AUCDEV-023-EBS-REMEDIATION-READBACK.md)):
AUCDEV023-CR-EBS-002 and AUCDEV023-CR-EBS-003 CLOSED at Control Room
implementation-readback strength, AUCDEV023-CR-EBS-001 PARTIALLY_REMEDIATED /
OPEN_BLOCKING, and NEW blocking finding AUCDEV023-CR-EBS-REM-001
(event-package component cross-binding not established). A bounded SECOND
remediation candidate now exists under `bootstrap-supervisor/**` (published
2026-09-19 under the operator's second bounded remediation authority:
generic fail-closed frozen event-package verification with exact transport
cross-binding BEFORE GATES_PASSED, mandatory event-package root on every
authority-bearing supervisor, synthetic/inert fixtures only; canonical
report:
[AUCDEV-023-EBS-SECOND-REMEDIATION-REPORT](AUCDEV-023-EBS-SECOND-REMEDIATION-REPORT.md)).
The fresh Control Room readback of that second remediation candidate
returned PARTIALLY_ACCEPTED / NARROW_MANIFEST_ROW_TYPE_REMEDIATION_REQUIRED
(canonical record:
[AUCDEV-023-EBS-SECOND-REMEDIATION-READBACK](AUCDEV-023-EBS-SECOND-REMEDIATION-READBACK.md)):
AUCDEV023-CR-EBS-REM-001 and the AUCDEV023-CR-EBS-001 remainder CLOSED /
ACCEPTED and AUCDEV023-CR-EBS-002/-003 CLOSED / RECONFIRMED at Control Room
implementation-readback strength — all bound to EXACT SHA `8f998209…` with
no transfer to a future changed SHA — and NEW blocking finding
AUCDEV023-CR-EBS-REM2-001 (event-package manifest files[] row `bytes` type
validation incomplete). A bounded NARROW manifest row-type remediation was
then implemented and published under the operator's narrow remediation
authority (every manifest files[].bytes row must be an exact non-negative
int, bool explicitly refused, at row validation BEFORE GATES_PASSED;
synthetic/inert fixtures only; canonical report:
[AUCDEV-023-EBS-NARROW-MANIFEST-TYPE-REMEDIATION-REPORT](AUCDEV-023-EBS-NARROW-MANIFEST-TYPE-REMEDIATION-REPORT.md)),
and its fresh Control Room readback ACCEPTED it at
implementation-readback strength (canonical record:
[AUCDEV-023-EBS-NARROW-MANIFEST-TYPE-REMEDIATION-READBACK](AUCDEV-023-EBS-NARROW-MANIFEST-TYPE-REMEDIATION-READBACK.md)):
AUCDEV023-CR-EBS-REM2-001 CLOSED / ACCEPTED and
AUCDEV023-CR-EBS-001/-002/-003/REM-001 CLOSED / RECONFIRMED, all bound to
EXACT SHA `4448deea…` with no transfer to a future changed SHA. A bounded
GATE-TIMING remediation candidate for AUCDEV023-CR-EBS-S1-001
(EXECUTION_TIME_RESOURCE_GATE_FROZEN_AT_S1_AND_NOT_REVALIDATED) was then
implemented and published under the operator's narrow gate-timing
remediation authority (the six STATIC preparation gates remain frozen
PASS evidence; the DYNAMIC RESOURCE_GATE is bound as an exact frozen
executable-artifact descriptor and EXECUTED by the EBS exactly once per
attempt, after startup identity checks and BEFORE GATES_PASSED, with a
strict result envelope and durable fresh evidence; event-package
manifest schema V2 with V1 refused; synthetic/inert fixtures only;
canonical report:
[AUCDEV-023-EBS-GATE-TIMING-REMEDIATION-REPORT](AUCDEV-023-EBS-GATE-TIMING-REMEDIATION-REPORT.md)),
and its fresh Control Room readback returned PARTIALLY_ACCEPTED
(canonical record:
[AUCDEV-023-EBS-GATE-TIMING-REMEDIATION-READBACK](AUCDEV-023-EBS-GATE-TIMING-REMEDIATION-READBACK.md)):
AUCDEV023-CR-EBS-S1-001 CLOSED / ACCEPTED and
AUCDEV023-CR-EBS-001/-002/-003/REM-001/REM2-001 CLOSED / RECONFIRMED,
all bound to EXACT SHA `8e952d81…` with no transfer to a future changed
SHA, and the +371 TCB growth (1664 → 2035) accepted as a nonblocking
residual at implementation-readback strength — while NEW blocking
findings AUCDEV023-CR-EBS-S1-002 (mandatory route-readiness gate
absent) and AUCDEV023-CR-EBS-S1-003 (RESOURCE_GATE PASS freshness not
coupled to consumption) remain OPEN — and the EBS is NOT installed
Audit Council runtime; the product/runtime source baseline of this
document is unchanged. Under the operator's 2026-09-19 narrow
preexec-gate remediation authority, a bounded candidate for BOTH
findings was then implemented and published at implementer strength
ONLY (canonical report:
[AUCDEV-023-EBS-PREEXEC-GATE-REMEDIATION-REPORT](AUCDEV-023-EBS-PREEXEC-GATE-REMEDIATION-REPORT.md)):
the binding freezes EXACTLY TWO dynamic runtime-gate descriptors in the
required order (NETWORK_READINESS first, RESOURCE_GATE last;
event-package manifest schema V3 with V1/V2 refused), and the formerly
separate public preexec operations validate_gates()/verify_launcher()
are REMOVED in favor of the ONE public consume(launcher_path) operation
that verifies the launcher, executes both gates exactly once, durably
records GATES_PASSED with both evidence sets and immediately
CONSUMED_PRE_EXEC — GATES_PASSED is an internal transient never returned
to the caller; AUCDEV023-CR-EBS-S1-002/-003 = REMEDIATION_IMPLEMENTATED
/ AWAITING_CONTROL_ROOM_READBACK, prior closures =
PRIOR_CONTROL_ROOM_CLOSURE_ON_8E952D81 / REGRESSION_EVIDENCE_HELD /
NEW_SHA_AWAITING_FRESH_CONTROL_ROOM_READBACK; production LOC 2035 →
2140 disclosed NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE;
zero provider/model/auditor executions; real event package NOT
PREPARED; existing S1 authorization PRESERVED / PAUSED / NOT CONSUMED.
The fresh Control Room readback of that candidate returned
PARTIALLY_ACCEPTED (canonical record:
[AUCDEV-023-EBS-PREEXEC-GATE-REMEDIATION-READBACK](AUCDEV-023-EBS-PREEXEC-GATE-REMEDIATION-READBACK.md))
and the 2026-09-20 implementer-strength follow-up
([AUCDEV-023-EBS-FINAL-LAUNCH-SEAM-REMEDIATION-REPORT](AUCDEV-023-EBS-FINAL-LAUNCH-SEAM-REMEDIATION-REPORT.md)):
S1-002/S1-003 were CLOSED / ACCEPTED and
S1-001/-002/-003/REM-001/REM2-001 CLOSED / RECONFIRMED at EXACT SHA
`6cf30f90…` (no transfer to a changed SHA), and the three FINAL
LAUNCH-SEAM findings AUCDEV023-CR-EBS-S1-004 (credential custody and
role not bound before consumption), AUCDEV023-CR-EBS-S1-005
(consumption-to-execution immediacy not enforced) and
AUCDEV023-CR-EBS-S1-006 (frozen exec invocation binding incomplete)
are REMEDIATED AT IMPLEMENTER STRENGTH ONLY on the new candidate
(`FINAL_LAUNCH_SEAM_REMEDIATION_CANDIDATE / AWAITING_FRESH_CONTROL_
ROOM_READBACK`): Supervisor-owned binding-derived-role custody admitted
before gates and consumption, the LaunchGrant/consume()/execute() split
removed into one caller-uninterruptible run_attempt call through
IMMEDIATE fork/exec, the live auditor executable verified/held against
the binding SHA and delivered as AUDITOR_EXEC_FD=5, the exact frozen
auditor argv and executable_version bound under manifest schema V4
(V1/V2/V3 refused) and delivered byte-for-byte on a sealed
AUDITOR_INVOCATION_FD=6, with no caller argv/env/custody/role/grant
surface; CR-EBS-001 fresh reconfirmation remains WITHHELD (prior
closure on 8e952d81 stands; the S1-006 conflict is remediated at
implementer strength, awaiting fresh readback); the +209 TCB growth
(2140 → 2349) is CANDIDATE_ONLY / NOT_CONTROL_ROOM_ACCEPTED
(NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE); event-package
preparation remains AUTHORIZED / PAUSED pending the fresh final
launch-seam readback; the EBS is NOT installed Audit Council runtime
and the product/runtime source baseline of this document is unchanged.
The fresh Control Room readback of that candidate returned
PARTIALLY_ACCEPTED (canonical record:
[AUCDEV-023-EBS-FINAL-LAUNCH-SEAM-REMEDIATION-READBACK](AUCDEV-023-EBS-FINAL-LAUNCH-SEAM-REMEDIATION-READBACK.md)):
AUCDEV023-CR-EBS-S1-004 CLOSED / ACCEPTED,
AUCDEV023-CR-EBS-S1-005 CLOSED / ACCEPTED and
AUCDEV023-CR-EBS-S1-006 CLOSED / ACCEPTED, and
AUCDEV023-CR-EBS-001 CLOSED / FRESHLY_RECONFIRMED, with
CR-EBS-002/-003/REM-001/REM2-001/S1-001/S1-002/S1-003 source-level
reconfirmed, all bound to EXACT SHA `4bb9b936…` with no transfer to a
future changed SHA; the +209 TCB growth (2140 → 2349) accepted as a
NONBLOCKING residual at implementation-readback strength
(NOT_STANDING_AUTHORITY) — while NEW blocking FINAL EXECUTION-LIFECYCLE
findings AUCDEV023-CR-EBS-S1-007 (report-custody validation and
terminalization not process-bound) and AUCDEV023-CR-EBS-S1-008 (auditor
execution timeout not EBS-enforced) remained OPEN. Under the operator's
2026-09-20 narrow final execution-lifecycle remediation authority, a
bounded candidate for BOTH findings was then implemented and published
at implementer strength ONLY (canonical report:
[AUCDEV-023-EBS-FINAL-EXECUTION-LIFECYCLE-REMEDIATION-REPORT](AUCDEV-023-EBS-FINAL-EXECUTION-LIFECYCLE-REMEDIATION-REPORT.md)):
the ONE public operation extends to run_attempt(credential_source_fd,
launcher_path, auditor_executable_path, report_staging_path,
output_root) -> AttemptResult — the separate public
adopt_report()/finish() surface is REMOVED; after the bounded child
wait the SAME call takes ONE immutable report snapshot, screens it with
the SAME held custody, runs the FROZEN STRUCTURAL VALIDATOR (V5
output_validator descriptor, held fd, sealed-snapshot delivery, strict
AUCDEV-023-REPORT-VALIDATOR-RESULT-V1 envelope, its own frozen
validator timeout) and freezes the exact screened+validated bytes 0444
through a pre-opened custody fd before TERMINAL; the boundary child
runs in its own session under the frozen
execution_limits.auditor_timeout_seconds monotonic deadline with
process-group SIGKILL and TIMEOUT_AFTER_CONSUMPTION consumed
accounting; manifest schema V5 with V1-V4 refused;
AUCDEV023-CR-EBS-S1-007/-008 = REMEDIATION_IMPLEMENTED /
AWAITING_CONTROL_ROOM_READBACK, prior closures =
PRIOR_CONTROL_ROOM_CLOSURE / REGRESSION_EVIDENCE_HELD /
NEW_SHA_AWAITING_FRESH_CONTROL_ROOM_READBACK; production LOC 2349 →
2800 disclosed NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE;
zero provider/model/auditor executions; real event package NOT
PREPARED; existing S1 authorization PRESERVED / PAUSED / NOT CONSUMED;
the EBS is NOT installed Audit Council runtime and the
product/runtime source baseline of this document is unchanged.
The fresh Control Room readback of that candidate returned
PARTIALLY_ACCEPTED (canonical record:
[AUCDEV-023-EBS-FINAL-EXECUTION-LIFECYCLE-REMEDIATION-READBACK](AUCDEV-023-EBS-FINAL-EXECUTION-LIFECYCLE-REMEDIATION-READBACK.md)):
AUCDEV023-CR-EBS-S1-007 CLOSED / ACCEPTED and
AUCDEV023-CR-EBS-S1-008 CLOSED / ACCEPTED, with
CR-EBS-001/-002/-003/REM-001/REM2-001/S1-001/S1-002/S1-003/S1-004/
S1-005/S1-006 source-level reconfirmed, all bound to EXACT SHA
`0f79d3bd…` with no transfer to a future changed SHA; the +451 TCB
growth (2349 → 2800) accepted as a NONBLOCKING residual at
implementation-readback strength (NOT_STANDING_AUTHORITY) — while the
NEW blocking finding AUCDEV023-CR-EBS-S1-009
(POST_CONSUMPTION_EXCEPTION_TERMINALIZATION_CAN_ESCAPE_PROCESS_BOUND_CLEANUP:
post-EXEC_ATTEMPTED parent-side exceptions and an unwrapped
timeout-path TERMINAL accounting sequence can escape process-bound
fail-closed terminal settlement with custody/held fds open) remains
OPEN/BLOCKING, a normal-exit boundary process-tree quiescence
obligation is recorded as an S1 event-preparation evidence
requirement (NOT_YET_PROVEN; additional lifecycle evidence, NOT an
alteration of the twelve mandatory GATE-W′ assertions), and
event-package preparation remains AUTHORIZED / PAUSED pending S1-009
remediation and fresh readback; the EBS is NOT installed Audit
Council runtime and the product/runtime source baseline of this
document is unchanged.
Under the operator's 2026-09-20 narrow S1-009 post-consumption
fail-closed terminality remediation authority, a bounded candidate for
that ONE finding was then implemented and published at implementer
strength ONLY (canonical report:
[AUCDEV-023-EBS-S1-009-POSTCONSUMPTION-TERMINALITY-REMEDIATION-REPORT](AUCDEV-023-EBS-S1-009-POSTCONSUMPTION-TERMINALITY-REMEDIATION-REPORT.md)):
ALL post-consumption terminal settlement is centralized in ONE
primitive separating the durable accounting attempt (first failure
preserves the record exactly) from a guaranteed never-raising
in-process fail-closed death (the narrow absorbing-terminal-focused
state-machine primitive restricted to post-consumption source states,
plus custody and all held-fd closure); post-EXEC_ATTEMPTED parent-side
exceptions, the timeout path and every report outcome settle through
it; a durable accounting failure raises the exact incompleteness
classification chaining any concurrent original failure and never a
success/timed-out/conforming result; V5 is UNCHANGED; RED was proven
first on the exact base and the deterministic battery (489/489, qh
221/221) now contains the required injected S1-009 regressions;
AUCDEV023-CR-EBS-S1-009 = REMEDIATION_IMPLEMENTED /
AWAITING_CONTROL_ROOM_READBACK (implementer position ONLY); production
LOC 2800 → 2904 disclosed NEW_TCB_GROWTH /
AWAITING_CONTROL_ROOM_ACCEPTANCE; zero provider/model/auditor
executions; the EBS is NOT installed Audit Council runtime and the
product/runtime source baseline of this document is unchanged.
The fresh Control Room readback of that candidate returned ACCEPTED
(canonical record:
[AUCDEV-023-EBS-S1-009-POSTCONSUMPTION-TERMINALITY-REMEDIATION-READBACK](AUCDEV-023-EBS-S1-009-POSTCONSUMPTION-TERMINALITY-REMEDIATION-READBACK.md)):
AUCDEV023-CR-EBS-S1-009 CLOSED / ACCEPTED at Control Room
implementation-readback strength, with all thirteen prior EBS invariants
(CR-EBS-001/-002/-003, REM-001, REM2-001 and S1-001 through S1-008)
source-level freshly reconfirmed on EXACT SHA `8c27b8a8…` with no
closure transferring to a future changed SHA; the +104 TCB growth
(2800 → 2904) accepted as a residual at implementation-readback
strength (NOT_STANDING_AUTHORITY); there is NO known EBS implementation
blocker at current readback strength — while
NORMAL_EXIT_BOUNDARY_PROCESS_TREE_QUIESCENCE remains NOT_YET_PROVEN
(S1 event-preparation evidence requirement), GATE-W′ remains
REQUIRED/UNPROVEN, real-client credential/tool isolation remains
UNPROVEN, the bootstrap event remains NOT_INSTANTIATED, and
event-package preparation remains AUTHORIZED / NOT_STARTED / PAUSED
pending this readback publication's independent verification; the EBS
is NOT installed Audit Council runtime and the product/runtime source
baseline of this document is unchanged.

The S1-009 readback publication itself (commit `0610e900…`) has now been
independently verified by the Control Room:
`AUCDEV_023_EBS_S1_009_POSTCONSUMPTION_TERMINALITY_REMEDIATION_READBACK_PUBLICATION_VERIFICATION =
ACCEPTED / PUBLICATION_IDENTITY_VERIFIED / HANDOFF_INTEGRITY_VERIFIED /
CANONICAL_BYTES_VERIFIED / PROTECTED_TREES_UNCHANGED /
NO_PUBLICATION_DEFECT_FOUND` (canonical record:
[AUCDEV-023-S1-EVENT-PACKAGE-PREPARATION-RESUMPTION](AUCDEV-023-S1-EVENT-PACKAGE-PREPARATION-RESUMPTION.md));
consequently event-package preparation is now AUTHORIZED_BY_OPERATOR /
NOT_STARTED / RESUMABLE and S1_AUTHORIZATION =
EXISTING_OPERATOR_AUTHORITY_PERSISTS / NOT_CONSUMED / RESUMABLE — the
underlying operator authority is pre-existing and unconsumed (NO new
authorization granted; S1 NOT started; no event package, no event id;
GATE-W′ REQUIRED/UNPROVEN, real-client credential/tool isolation
UNPROVEN, NORMAL_EXIT_BOUNDARY_PROCESS_TREE_QUIESCENCE NOT_YET_PROVEN,
bootstrap event NOT_INSTANTIATED, model engagements 0; zero
provider/model/auditor executions; qualification NONE; installation
NONE); the EBS is NOT installed Audit Council runtime and the
product/runtime source baseline of this document is unchanged.

The S1 event-package preparation has since been PERFORMED (2026-09-20,
canonical record:
[AUCDEV-023-S1-EVENT-PACKAGE-PREPARATION-REPORT](AUCDEV-023-S1-EVENT-PACKAGE-PREPARATION-REPORT.md)):
`AUCDEV_023_S1_EVENT_PACKAGE_PREPARATION = PREPARED / AWAITING_CONTROL_ROOM_READBACK`
— the real V5 event packages and bindings for event `evt-7df609ec6c569043`
exist frozen OUTSIDE the repository with the frozen networked boundary
launcher, tool-domain wrapper, runtime-gate artifacts, structural
validator, sandbox profiles, neutral prompt contract and A=B common
evidence; GATE-W′ = PASS with both assertion-10 completeness limitations
disclosed, NORMAL_EXIT_BOUNDARY_PROCESS_TREE_QUIESCENCE = PASS at
synthetic rehearsal strength, and REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION =
PASS at the adopted design's strength (subprocess isolation mechanical;
in-process read protection application-level residual). The bootstrap
event itself remains NOT_INSTANTIATED, model engagements remain 0, and
every real execution authority remains NONE — a real first pass requires
a NEW explicit operator execution authority after the independent Control
Room readback of the S1 evidence; the product/runtime source baseline of
this document is unchanged.

The Control Room readback of that S1 preparation has since returned
PARTIALLY_ACCEPTED (2026-09-20, canonical record:
[AUCDEV-023-S1-EVENT-PACKAGE-PREPARATION-READBACK](AUCDEV-023-S1-EVENT-PACKAGE-PREPARATION-READBACK.md)):
publication identity, handoff integrity, canonical bytes, protected
trees and the mechanical event-package identities are VERIFIED and MOST
S1 mechanical evidence is ACCEPTED — but GATE_W′ is NOT_ACCEPTED
(assertion 10 is incomplete for both roles and the rehearsal harness's
`all_pass`/frozen-PASS conversion makes the frozen classification
invalid), and THREE findings are OPEN/BLOCKING:
AUCDEV023-CR-S1-PREP-001 GATE_W_PRIME_ASSERTION_10_INCOMPLETE_BUT_FROZEN_PASS,
AUCDEV023-CR-S1-PREP-002 AUDITOR_B_EFFECTIVE_CLIENT_RUNTIME_IDENTITY_NOT_FULLY_PINNED
(the frozen entrypoint SHA does not cover the launcher-mounted Node
runtime), and AUCDEV023-CR-S1-PREP-003
LIVE_COMMON_EVIDENCE_SET_NOT_PRECONSUMPTION_REVERIFIED (no live
walk/hash rebound of the externally mounted common-evidence payload to
the frozen manifest on the pre-consumption authority path).
AUDITOR_A/B_EVENT_READINESS = BLOCKED, real execution is NOT authorized,
and bounded remediation plus a fresh Control Room readback are REQUIRED;
the implementation report's original claims remain historical implementer
claims, superseded only for CURRENT Control Room state; model
engagements remain 0, qualification NONE / installation NONE, and the
product/runtime source baseline of this document is unchanged.

The bounded S1 remediation (2026-09-20, operator authority
`AUCDEV-023-S1-PREP-REM-20260920-01`; canonical record:
[AUCDEV-023-S1-EVENT-PACKAGE-REMEDIATION-REPORT](AUCDEV-023-S1-EVENT-PACKAGE-REMEDIATION-REPORT.md))
has since implemented all three remediations at implementer strength in a
NEW successor event-package set (historical S1 packages untouched;
implementer dispositions AWAITING_CONTROL_ROOM_READBACK — NOT Control Room
closure). Trust-boundary FACTS of the successor composition, all
mechanically evidenced: (1) the boundary mounts NO `/opt/node` runtime —
the Auditor-B executable is the NATIVE codex 0.154.0 binary and its
COMPLETE six-file vendored runtime closure is staged INSIDE the frozen
event package as manifest rows, with the package's vendored bwrap and rg
bound PATH-first ahead of the host system surface (the prior
peer-provider-client-code visibility at /opt/node no longer exists);
(2) EVERY execution-visible evidence byte (frozen target subtrees,
common evidence, EBS source, per-role gate evidence) is staged INSIDE the
frozen event package and mounted ONLY from there, so the accepted EBS
per-file package verification before GATES_PASSED is now also the
pre-consumption identity binding of the mounted evidence (no external
workspace evidence mount remains); (3) GATE-W′ aggregation and package
freeze accept ONLY the exact status PASS, and assertion 10 is
mechanically demonstrated for both roles through the REAL pinned clients
via a deterministic mock transport (fixed scripted bytes, loopback-only
inside isolated network namespaces — zero model inference, zero real
provider request, zero real credential), which also surfaced and fixed
three latent frozen-surface defects: the pinned claude client does not
match `Write(...)` rules for file permission checks (corrected
`Edit(//…)` surface), the pinned codex client refuses exec in a non-git
cwd (frozen invocation gains `--skip-git-repo-check`), and the S1 tool
wrapper's bind over the `/usr/bin/sh` symlink destination aborted every
nested tool composition on this host (fail-closed but functionally
inert; fixed, so the tool domain now genuinely executes). A disclosed
composition-layering fact: beneath the interposed wrapper the designed
ephemeral writable set is re-materialized in the fresh tool namespace,
so the codex profile's writable_roots restriction is subsumed for
namespace-local scratch only — every host-backed or evidence path
remains denied at both layers. No EBS/qh/skill source change was made
anywhere in the remediation; the product/runtime source baseline of this
document is unchanged.

The Control Room's complete-handoff readback of that remediation (2026-09-20,
canonical record:
[AUCDEV-023-S1-REMEDIATION-COMPLETE-HANDOFF-READBACK](AUCDEV-023-S1-REMEDIATION-COMPLETE-HANDOFF-READBACK.md))
independently byte-verified the complete successor packages (A 183/183, B
188/188) and CLOSED PREP-001, PREP-003 and REM-001 at Control Room readback
strength — but found the NEW execution-boundary defect
AUCDEV023-CR-S1-REM-002 AUDITOR_B_REAL_TOOL_ENTRYPOINT_BYPASSES_CREDENTIAL_DOMAIN_WRAPPER
(OPEN/BLOCKING, with PREP-002 remaining OPEN/BLOCKING): the real Codex
client's recorded tool path executes commands through `/usr/bin/zsh -lc`,
while the frozen launcher interposes the credential-domain wrapper ONLY at
`/usr/bin/bash` — and the read-only host `/usr` bind leaves `/usr/bin/zsh`
a real executable path independent of the vendored frozen zsh. The adopted
C2 mechanical isolation invariant (every tool subprocess tree runs where
the credential path does not exist) is therefore NOT ESTABLISHED for the
observed REAL Auditor-B tool path: real Auditor-B subprocess
credential/tool-domain isolation must NOT be represented as established or
execution-ready while REM-002 remains open (the earlier remediation-era
statement that the tool domain "genuinely executes" remains true only of
the wrapper composition itself and of shell entries that resolve through
`/usr/bin/bash`). No credential exposure is claimed to have occurred; the
defect is the unproven invariant. A fail-closed Code Mode unavailability
observation is preserved as INFORMATIONAL. A separately authorized bounded
PREP-002/REM-002 remediation is required before Auditor-B event readiness
can be reconsidered; no source or package was changed by this record.

That separately authorized bounded remediation has since been implemented
(2026-09-21, operator authority `AUCDEV-023-S1-PREP002-REM002-20260920-01`;
canonical record:
[AUCDEV-023-S1-PREP002-REM002-REMEDIATION-REPORT](AUCDEV-023-S1-PREP002-REM002-REMEDIATION-REPORT.md))
at implementer strength in a NEW successor event-package generation for BOTH
roles (every prior generation untouched; implementer dispositions
AWAITING_CONTROL_ROOM_READBACK — NOT Control Room closure). Trust-boundary
FACTS of the new successor composition, all mechanically evidenced and
frozen as package rows: (1) the credential-domain wrapper is a NATIVE
STATIC-PIE executable — no host interpreter, no dynamic loader and no
dynamic library executes in the credential-bearing transition path —
interposed at BOTH real initial shell entry points `/usr/bin/bash` AND
`/usr/bin/zsh` (regular-file destinations; every `sh`/`/bin` entry resolves
onto them), so the REAL observed Codex tool entry path `/usr/bin/zsh -lc`
now crosses the wrapper, with the `AUCDEV_TOOL_DOMAIN=1` marker observed
inside the real client tool path and a differential no-wrapper control
establishing CAUSAL traversal (on the deliberately unwrapped control path
the credential staging copy is `/proc/1/root`-readable; with the wrapper it
is UNREADABLE and the client-domain sentinel is absent); (2) the wrapper
execs the PACKAGE-PINNED sandbox engine `/auditor-tools/bin/bwrap` (the
frozen vendored bwrap row), and the OUTER boundary composition itself is
likewise composed by the package-pinned vendored bwrap staged as a manifest
row in BOTH role packages — no unpinned host sandbox-engine byte remains
between the pinned clients and the credential-free tool domain; (3) the
pinned client's startup capability-probe payload (`/usr/bin/true`,
mechanically observed executing in the credential-bearing window) is itself
a pinned static-pie package row; (4) the real shells are preserved at
post-split-only paths `/auditor-tools/shells/{bash,zsh}` (basenames chosen
so zsh runs in NORMAL mode, retaining zsh semantics; never silently replaced
by bash) and are bound over the wrapper's own interposition paths INSIDE the
tool domain; (5) a fixed synthetic boundary sentinel is staged read-only at
`/auditor-init/boundary-sentinel` (client-domain-only; absent from the tool
domain by construction) as the no-wrapper differential oracle. The
machine-readable authority-path inventory mechanically establishes that
every CLIENT_DOMAIN and SPLIT_TRANSITION executable byte is a frozen,
EBS-verified package byte (the two pre-client-entry launcher/INNER custody
rows are disclosed as outside the closure). No EBS/qh/skill source change
was made anywhere in this remediation; the product/runtime source baseline
of this document is unchanged.

The Control Room's readback of that remediation (2026-09-21, canonical
record:
[AUCDEV-023-S1-PREP002-REM002-REMEDIATION-READBACK](AUCDEV-023-S1-PREP002-REM002-REMEDIATION-READBACK.md))
returned **ACCEPTED**: the generated-last complete remediation handoff
(`d16b81d4…`; 512 members, 431/431 checksums PASS) was independently
verified, the complete NEW successor package bytes were independently
byte-verified (Auditor-A 189/189; Auditor-B 192/192; new package/binding
identities verified incl. binding transport projections and the identical
shared launcher), the native wrapper closure was verified (ELF static-PIE,
no PT_INTERP, no dynamic NEEDED, no script interpreter; package-pinned
bwrap and probe-true; wrapper-mutation negative control fails closed;
A/B boundary parity passes), and the real Codex zsh-entry wrapper
interposition was verified WITH the causal differential no-wrapper control
(wrapper-positive: TOOLMARKER=1, sentinel/home/init ABSENT, credential
unreadable via /proc; no-wrapper control: marker absent, all PRESENT,
readable). AUCDEV023-CR-S1-PREP-002 and AUCDEV023-CR-S1-REM-002 are
therefore CLOSED at Control Room readback strength (with PREP-001/PREP-003
held invariants verified regression-clean and REM-001 remaining CLOSED);
the known S1 preparation/remediation blockers are
CLOSED_AT_CONTROL_ROOM_READBACK_STRENGTH — this is NOT independent-audit
PASS and NOT qualification. The disclosed residuals are retained
(application-level CLIENT_IN_PROCESS_READ_PROTECTION; host-netns exposure;
composition-layering; zero-inference mock-transport limitation with a real
first pass still event-time evidence; OBSERVATION-ONLY engine shim; the two
disclosed pre-client-entry BOUNDARY_SETUP host-interpreter rows outside the
bounded closure; TEST_ENVIRONMENT_DIVERGENCE; Code Mode INFORMATIONAL), and
a 20-byte implementer FINAL-RETURN transcription discrepancy on the
Auditor-A payload-byte count (236,260,404 vs the established 236,260,424)
is recorded as INFORMATIONAL with no package identity defect. Resulting
posture: Auditor-A AND Auditor-B event readiness =
READY_FOR_SEPARATE_OPERATOR_EXECUTION_AUTHORITY (real execution still NOT
AUTHORIZED; event `evt-7df609ec6c569043` and both reserved attempts
preserved NOT-STARTED/NOT-CONSUMED; MODEL_ENGAGEMENTS 0; qualification
NONE / installation NONE). No source or package was changed by this
record; the product/runtime source baseline of this document is unchanged.

Subsequently (2026-09-21, canonical record:
[AUCDEV-023-S1-FIRSTPASS-EXECUTION-PRELAUNCH-READBACK](AUCDEV-023-S1-FIRSTPASS-EXECUTION-PRELAUNCH-READBACK.md))
the operator granted the first-pass execution authority
`AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-01` (event `evt-7df609ec6c569043`;
reserved attempts `-A-01`/`-B-01`; budget exactly 2), and the Control
Room's exact operator-launch preflight **STOPPED_PREEXEC** on NEW blocking
finding AUCDEV023-CR-S1-EXEC-001
(RESOURCE_GATE_VALIDATES_STALE_ATTEMPT_WORKSPACE_ROOT; HARNESS/PROTOCOL
DEFECT / PREEXEC RUNTIME-GATE COVERAGE GAP): the frozen
`runtime/resource-gate.py` (`960058b3…`, identical in both role packages)
samples the HISTORICAL S1 preparation workspace root
`/home/isa/aucdev023-s1-event-preparation`, while the frozen shared
launcher (`2efb6660…`, identical in both role packages) constructs the
ACTUAL first-pass attempt staging under
`/home/isa/aucdev023-s1-prep002-rem002/attempts/<attempt>/staging` and
bind-mounts it as `/auditor-output` — both artifacts correctly frozen and
byte-verified, so this is a SEMANTIC runtime-gate COVERAGE mismatch
between two correctly frozen components, not an identity mismatch; the
mandatory live pre-consumption workspace-readiness invariant is therefore
NOT mechanically established for the actual successor composition (the
gate's freshness is temporal but its attempt-workspace TARGET is stale).
The PREP/REM closures above remain HISTORICAL and are not reopened, but
CURRENT execution readiness is superseded: Auditor-A and Auditor-B event
readiness = BLOCKED_PENDING_EXEC_001_REMEDIATION; INDEPENDENT_HARNESS_AUDIT
= BLOCKED_PRELAUNCH; REAL EXECUTION = DO NOT START. The authority is
GRANTED / UNCONSUMED / PRELAUNCH_BLOCKED and
BOUND_TO_CURRENT_PACKAGE_GENERATION — it does NOT transfer automatically
to any successor generation that changes any frozen
event-package/binding/launcher/runtime-gate identity; remediation + fresh
Control Room readback + a NEW explicit operator execution authority are
required. No source or package was changed by this record; no architecture
redesign; the adopted R1 architecture/policy semantics are unaltered; the
product/runtime source baseline of this document is unchanged.

Subsequently (2026-09-21, canonical record:
[AUCDEV-023-S1-EXEC001-EVENT-PACKAGE-REMEDIATION-REPORT](AUCDEV-023-S1-EXEC001-EVENT-PACKAGE-REMEDIATION-REPORT.md))
a bounded implementer session under operator authority
`AUCDEV-023-S1-EXEC001-REM-20260921-01` remediated EXEC-001 at implementer
strength by the smallest authorized change: a NEW successor event-package
generation for BOTH roles (workspace
`/home/isa/aucdev023-s1-exec001-remediation/`; historical generation
byte-immutable, verified before and after) in which the frozen
`runtime/resource-gate.py` line-26 `ROOT` is now
`/home/isa/aucdev023-s1-prep002-rem002` — EXACTLY equal to the
byte-identical frozen launcher's workspace contract (`2efb6660…`
unchanged), so the dynamic RESOURCE_GATE now samples the SAME
`ROOT/attempts/<attempt>/{staging,custody-out,accounting}` tree the
launcher actually constructs and the EBS `run_attempt` report locators
point into (workspace-contract verification EXACT_MATCH both roles;
new gate `e8f85391…`; new A manifest `45805629…` / package `703dd95b…` /
binding digest `5c48fa3f…` 189 rows and B manifest `5c1421ae…` / package
`23131e88…` / binding digest `f088b132…` 192 rows; per-package change set
EXACTLY the gate line + identity-derived linter/package-binding-identity/
MANIFEST regenerations; EBS-verified both roles; N1–N5 contract/mutation/
substitution controls + a synthetic zero-inference gate rehearsal proving
the gate samples the actual launcher root, all PASS; EBS 489/489 + qh
221/221 regression batteries at the exact base). This is a
runtime-gate workspace-contract FACT continuation only: no architecture
redesign, the adopted R1 architecture/policy semantics and the V5
package/binding schema are unaltered, the launcher/wrapper/client bytes
are unchanged, and the disposition is REMEDIATION_IMPLEMENTED /
AWAITING_CONTROL_ROOM_READBACK — EXEC-001 is NOT closed by the
implementer, the old execution authority remains UNCONSUMED and
non-transferable, and the new generation requires deployment at the
launcher-resolved root location plus a NEW explicit operator execution
authority after readback acceptance. The product/runtime source baseline
of this document is unchanged.

Subsequently (2026-09-21, canonical record:
[AUCDEV-023-S1-EXEC001-EVENT-PACKAGE-REMEDIATION-READBACK](AUCDEV-023-S1-EXEC001-EVENT-PACKAGE-REMEDIATION-READBACK.md))
the Control Room readback of that remediation was **ACCEPTED** and
**EXEC-001 was CLOSED at Control Room readback strength** (NOT
independent-audit PASS, NOT qualification): the complete 233,161,895-byte
handoff (`80e7d204…`; 512 members = 434 regular + 78 directories; exactly
one SHA256SUMS, 433/433 PASS, no unlisted or absent payload) verified with
the four canonical publication files Git-blob-identical to live GitHub; the
new successor packages verified A 189/189 and B 192/192 with the new
identities (A manifest `45805629…` / package `703dd95b…` / binding file
`9cb8002f…` / canonical digest `5c48fa3f…`; B manifest `5c1421ae…` /
package `23131e88…` / binding file `12f89308…` / canonical digest
`f088b132…`); the historical→new gate source difference confirmed EXACTLY
ONE substantive line (the ROOT correction) with the launcher `2efb6660…`
BYTE-IDENTICAL, so `RESOURCE_GATE_ROOT == LAUNCHER_ROOT ==
/home/isa/aucdev023-s1-prep002-rem002` for BOTH roles with
workspace-contract classification EXACT_MATCH; the change scope confirmed
EXACTLY the gate row + identity-derived regenerations + MANIFEST root per
package with A/B execution-visible `payload/evidence/**` 169/169
byte-identical; the N1–N5 negative controls, the synthetic zero-inference
gate rehearsal and the held PREP-001/-002/-003 + REM-001/-002 invariants
(EBS 489/489 + qh 221/221) all verified. Resulting posture: Auditor-A AND
Auditor-B event readiness =
READY_FOR_NEW_EXACT_GENERATION_EXECUTION_AUTHORITY and
INDEPENDENT_HARNESS_AUDIT =
READY_FOR_NEW_EXACT_GENERATION_EXECUTION_AUTHORITY / NOT YET AUTHORIZED
— REAL EXECUTION AUTHORITY FOR THE NEW GENERATION = NONE; the OLD
authority `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-01` remains GRANTED
HISTORICALLY / UNCONSUMED / PRELAUNCH_BLOCKED FOR ITS GENERATION /
NON-TRANSFERABLE to the new generation. EXECUTION PRECONDITION (not a new
defect): the byte-identical launcher resolves its execution package tree
under `/home/isa/aucdev023-s1-prep002-rem002/event/`, so before any future
real attempt — under a NEW explicit operator execution authority — the
Control-Room-accepted NEW successor generation must be DEPLOYED to that
launcher-resolved event location, and the deployed bytes must be
mechanically reverified to EXACTLY the accepted
package/binding/launcher/gate identities BEFORE any AccountingStore
creation, credential ingestion, dynamic runtime gate, GATES_PASSED,
CONSUMED_PRE_EXEC or provider/model execution. No source or package was
changed by this record; no architecture redesign; the adopted R1
architecture/policy semantics are unaltered; the product/runtime source
baseline of this document is unchanged.

The adopted design (Control Room readback-accepted revision, architecture R1)
introduces, for at most one future AUCDEV-023 harness-audit event only:

- a minimal EXTERNAL BOOTSTRAP SUPERVISOR (EBS) outside `qualification-harness/**`
  and `skill/**` — a target-independent, operator-controlled, controllerless,
  process-bound, one-shot bootstrap authority with no substantive audit
  verdict logic and no qh imports;
- the frozen qh target (`d4d584ff…`) as audit subject only — never launch,
  credential, or accounting authority for its own review;
- a networked auditor transport as a future per-event frozen package, bound to
  exact event/role/attempt/model/evidence/target/output identities;
- two external blind first passes (default engagement budget 2).

Credential custody is target-independent (operator pipe/sealed memfd →
non-dumpable EBS → sealed in-memory custody → fd inheritance → ephemeral
boundary-private provider home → teardown). Credential/tool isolation (C2
namespace-split is the required architecture) and GATE-W′ (REQUIRED/UNPROVEN)
are mandatory future preparation gates, not satisfied claims; the real
client's in-process credential-read protection is NOT YET PROVEN
(application-level residual; role blocked if no effective deny exists).
Host-netns network exposure is an accepted disclosed residual at design
strength. Policy lifetime is one-event / single-use / no-revival. No
execution, qualification, or installation authority follows from adoption;
the independent auditor provenance gate remains NOT_SATISFIED and the
ordinary predecessor chain is not claimed. Canonical record:
[AUCDEV-023-AUDITOR-BOOTSTRAP-GOVERNANCE-ADOPTION](AUCDEV-023-AUDITOR-BOOTSTRAP-GOVERNANCE-ADOPTION.md).

The product/runtime source baseline of this document is unchanged by the
adoption, the implementation candidate, its readback, the remediation
candidate, the second remediation candidate, its readback, the narrow
manifest row-type remediation candidate, its readback, the gate-timing
remediation candidate, or its readback: the EBS is separate bootstrap tooling under
`bootstrap-supervisor/**` (stdlib-only minimal TCB; one-shot process-bound
authority; sealed-memfd custody; verified-open-fd launch; durable
accounting; fail-closed frozen event-package verification with transport
cross-binding and exact int-typed manifest row byte counts; runtime
RESOURCE_GATE bound as a frozen executable-artifact descriptor and
executed exactly once live before GATES_PASSED; report custody
with leak screen; inert synthetic test fixtures
only; zero provider/model executions; qualification NONE / installation
NONE), whose gate-timing remediation readback is PARTIALLY_ACCEPTED —
CR-EBS-S1-001 CLOSED / ACCEPTED and
CR-EBS-001/-002/-003/REM-001/REM2-001 CLOSED / RECONFIRMED, all on
EXACT SHA `8e952d81…` with no closure of any finding transferring to a
future SHA, and the 2035-LOC TCB residual accepted nonblocking at
implementation-readback strength — but with TWO PREEXEC GATE BLOCKERS
OPEN (CR-EBS-S1-002 mandatory route-readiness gate absent;
CR-EBS-S1-003 RESOURCE_GATE PASS freshness not coupled to consumption);
the operator-granted authorization for bounded event-package preparation
(S1), incl. zero-inference GATE-W′ validation, exists but remains
PAUSED pending the preexec-gate remediation and its fresh readback —
the event package is NOT prepared. It is NOT an
event package and is NOT
execution-authorized: GATE-W′ (REQUIRED/UNPROVEN) and real-client
credential/tool isolation (UNPROVEN / EVENT_PREPARATION_GATE) remain future
preparation gates, and the future networked boundary launcher / tool
wrapper / event-package artifacts remain separately authorized event-side
stages.

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
