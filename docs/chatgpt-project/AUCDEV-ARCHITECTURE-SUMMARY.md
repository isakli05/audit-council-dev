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
