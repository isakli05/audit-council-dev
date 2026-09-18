# AUCDEV-023 — Qualification-Harness Implementation: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION SESSION ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room decision-maker (this session publishes the Control Room's already-reached readback disposition verbatim), NOT a qualification authority, NOT an installation authority; NO remediation implementation; NO new harness probe; NO auditor/model/provider execution; NO independent harness audit; NO qualification; NO installation; NO Campaign-2 recovery; NO Campaign-3; ZERO provider/model/frontier calls by this publication session |
| Date | 2026-09-18 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-18) authorizes ONLY this publication of the Control Room readback disposition of the AUCDEV-023 qualification-harness implementation publication. It does NOT authorize remediation implementation, harness probes, independent audit, auditor/model/provider execution, qualification, installation, Campaign-2 recovery or Campaign-3. |
| Exact governance base | `3c59264007bab172e72a5c03c0299a5dec71f8d3` (the AUCDEV-023 qualification-harness implementation publication commit; tree `afcc1aa87caaf57000adcbb6b48cbbb431831482`; sole parent `695fd11a67f3fb3d80fc519e66755dab33ae562f`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this publication's bootstrap and re-resolved EXACT immediately before mutation, immediately before its single fast-forward push, and from GitHub after the push; THIS readback publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Subject | AUCDEV-023 qualification-harness implementation (commit `3c592640…`), its source implementation handoff, its self-test evidence, and its integrated C-2/C-3 launch-authority trust boundary |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **DEFERRED_PENDING_REMEDIATION** (§13) — deferred by decision, not waived; remains mandatory after bounded remediation + readback + exact-SHA freeze |

## 1. Live bootstrap and mandatory state (OBSERVED_FACT)

Live `refs/heads/master` resolved EXACT `3c59264007bab172e72a5c03c0299a5dec71f8d3`
(tree `afcc1aa87caaf57000adcbb6b48cbbb431831482`; sole parent
`695fd11a67f3fb3d80fc519e66755dab33ae562f`).  All mandated files were read
at that exact SHA.  Confirmed governing state at that SHA:

```
AUCDEV-023   = P1 / READY
AUCDEV-010   = P1 / BLOCKED
Campaign-2   = TERMINAL
qualification = NONE
installation  = NONE
```

## 2. Source implementation handoff — integrity VERIFIED (read-only)

`AUCDEV-023-QUALIFICATION-HARNESS-IMPLEMENTATION-handoff-20260918.tar.gz`,
independently re-verified read-only by THIS publication session (in-memory
tar inspection only; content NOT executed; nothing extracted into the
repository):

- outer SHA-256 `949a79a459fdd0060b99f2e081aa1133c121597ed38ff4099ba2ffe9103099c9`
- **156936 bytes**
- member census: **56 total = 46 regular files + 10 directories**
- unsafe/traversal 0; duplicates 0; symlink/hardlink/special 0
- exactly ONE `SHA256SUMS`
- the `SHA256SUMS` contains **45 payload checksum entries**
- checksum verification result: **45/45 PASS**

## 3. Control Room disposition (recorded verbatim)

```
AUCDEV_023_QUALIFICATION_HARNESS_IMPLEMENTATION_READBACK_PARTIALLY_ACCEPTED
/ LIVE_HEAD_3C592640
/ HANDOFF_INTEGRITY_VERIFIED_45_OF_45
/ EXACT_34_PATH_PUBLICATION_VERIFIED
/ SKILL_TREE_UNCHANGED
/ HARNESS_SELFTEST_EVIDENCE_84_OF_84_ACCEPTED
/ PRODUCT_TARGETED_NONREGRESSION_34_OF_34_ACCEPTED
/ PRODUCT_FULL_SUITE_685_OF_686_WITH_PREEXISTING_NODE_PATH_EXTERNAL_CONDITION
/ C1_MECHANICS_ACCEPTED_AT_IMPLEMENTATION_SELFTEST_STRENGTH
/ NOEGRESS_AND_GATEW_MECHANICS_ACCEPTED_AT_IMPLEMENTATION_SELFTEST_STRENGTH
/ C2_G1_ENFORCEMENT_NOT_ACCEPTED
/ CONTROL_ROOM_MINT_ROOT_NOT_MECHANICALLY_ANCHORED
/ CONTROLLER_SUPPLIED_LAUNCH_SPEC_NOT_BOUND
/ SELF_ASSERTED_CODEX_IDENTITY_PIN
/ CONTROLLER_CHOSEN_RW_BIND_AND_HARNESS_ROOT
/ PRODUCTION_YAMA_OVERRIDE_BYPASS_PRESENT
/ PROVIDER_CREDENTIAL_INTEGRATION_BLOCKER_HELD
/ IMPLEMENTATION_COMPLETE_CLAIM_NOT_ACCEPTED
/ INDEPENDENT_HARNESS_AUDIT_DEFERRED_PENDING_REMEDIATION
/ AUCDEV023_REMAINS_P1_READY
/ CAMPAIGN2_TERMINAL_UNCHANGED
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
```

## 4. Mechanically accepted publication facts (OBSERVED_FACT)

Independently re-derived by THIS publication session from the live
repository at the exact SHA:

- implementation commit `3c59264007bab172e72a5c03c0299a5dec71f8d3`;
- tree `afcc1aa87caaf57000adcbb6b48cbbb431831482`;
- sole parent `695fd11a67f3fb3d80fc519e66755dab33ae562f`;
- exact changed-path count **34**;
- changed paths confined EXACTLY to `qualification-harness/**` (31 paths)
  plus `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`,
  `docs/chatgpt-project/AUCDEV-BACKLOG.md` and the NEW
  `docs/chatgpt-project/AUCDEV-023-QUALIFICATION-HARNESS-IMPLEMENTATION.md`;
- the `skill/` tree is UNCHANGED:
  `git rev-parse 3c59264:skill` == `git rev-parse 695fd11:skill` ==
  `c792933a862d9a5434681a88d183470dd8b15d2f`;
- NO historical Campaign-2 artifact was changed (the changed-path
  confinement proves it mechanically).

## 5. Accepted test evidence (implementation/self-test strength ONLY)

Accepted as implementation/self-test evidence, **NOT** independent audit
proof:

```
qualification-harness deterministic final suite : 84 / 84 PASS
targeted existing product non-regression        : 34 / 34 PASS
product full suite                              : 685 / 686 PASS
                                                 (99 subtests PASS)
```

The sole product-suite failure
(`skill/tests/test_tier4_da27c0.py::TestWrapperExecutionEnvironment::test_f2_intended_node_runtime_selected`)
reproduced on the recorded rerun with the same host Node PATH mismatch:
the sandbox resolved the NVM node while host `shutil.which("node")`
resolved the Hermes node.  Because the `skill/` tree is byte-identical
before/after, the failing product test was not modified, and the same
environmental mismatch reproduced, this observation is classified:

```
EXTERNAL_CONDITION
/ PRODUCT_NONREGRESSION_COMPLETENESS_LIMITATION
/ HOST_NODE_PATH_DRIFT
```

It does NOT establish an AUCDEV-023 implementation defect.  The
historical test failure was NOT rewritten or suppressed.

## 6. Accepted implementation surfaces (implementation/self-test strength ONLY)

Accepted at implementation/self-test strength only:

A. **C-1 bootstrap/provenance mechanics** — pre-controller manifest
   capture; actual controller process C4′ checks; SO_PEERCRED /
   process-starttime / environment binding; own-current-session
   bounded-tree handling; foreign/pre-existing state and tamper
   rejection.

B. **Attempt state-machine terminality mechanics.**

C. **Hard no-egress detection mechanics**, including
   `SYSTEMD_RESOLVED_AF_UNIX_ESCAPE_SURFACE` and
   `HARD_NO_EGRESS_GATE_MUST_REQUIRE_ZERO_INHERITED_SOCKET_FDS`.

D. **Generated named restricted Codex profile semantics** at
   static/self-test strength.

E. **GATE-W** local deterministic matrix and widened-evidence negative
   test.

F. **Skill/product separation.**

These accepted portions MUST NOT be interpreted as acceptance of the
integrated launch-authority trust boundary.

## 7. Blocking finding IR-001 — AUCDEV023-CR-IMPL-001

```
Classification:
HARNESS/PROTOCOL DEFECT
/ LAUNCH_AUTHORITY_ROOT_OF_TRUST
/ CONTROL_ROOM_MINT_NOT_MECHANICALLY_ANCHORED
Support: OBSERVED_FACT
```

The accepted G-1 property requires launch authority to be minted only by
an operator/Control-Room-side authority surface OUTSIDE the untrusted
same-UID controller's authority.  The implementation does NOT
mechanically establish that property.  Observed source facts (each
independently confirmed by THIS publication session in the exact
implementation bytes, read-only):

- `qh.cli mint` requires no external Control-Room/operator capability;
- the caller supplies attempt id, root, manifest id and operator-state
  path;
- `mint_attempt_grant()` treats the caller-selected ordinary
  `operator_state_dir` ledger as the duplicate-attempt registry;
- a same-UID process can create a fresh operator-state directory and a
  fresh bootstrap manifest itself;
- the `--operator-pid` supervisor check is OPTIONAL and the expected pid
  is caller supplied;
- a controller process that directly spawns its own supervisor can
  supply its own pid as that value;
- the minted grant's `secret` is carried and registered for redaction
  but is never used to authenticate the controller request or to
  establish a Control-Room-rooted capability.

Independent Control Room source-level adversarial probe against the
exact implementation bytes established:

```
SELF_MINT_WITHOUT_EXTERNAL_AUTH = TRUE
```

A same-UID caller created its own clean config scope, its own manifest,
its own operator-state directory, and a fresh grant — without any
mechanically distinct Control-Room authorization input.  Therefore:

```
C2_G1_ENFORCEMENT = NOT ACCEPTED
```

The fact that the live supervisor is non-dumpable does protect the
authority of an already-legitimate supervisor from inspection.  It does
NOT prove that only the Control Room/operator can instantiate a
legitimate-looking supervisor.

## 8. Blocking finding IR-002 — AUCDEV023-CR-IMPL-002

```
Classification:
HARNESS/PROTOCOL DEFECT
/ TRUSTED_LAUNCH_SPEC_BINDING
/ CONTROLLER_SUPPLIED_SECURITY_CRITICAL_STATE
Support: OBSERVED_FACT
```

The untrusted controller request supplies security-critical values
including `harness_root`, `evidence_src`, `auditor_output_src`,
`target_src`, `codex_home`, `config_path`, profile/model fields, the
Codex executable path, and the expected Codex SHA-256/version.  The
supervising gatekeeper binds only the attempt/root/bootstrap-manifest
identity before using these request fields.  It does NOT compare the
complete security-critical launch specification with an immutable
operator/Control-Room-minted launch manifest/capability.  Observed
consequences (each confirmed in the exact implementation bytes,
read-only):

A. `request["auditor_output_src"]` becomes the HOST source of the RW
   bind — a controller-selected host path → `/auditor-output`.

B. `request["harness_root"]` becomes the host source bound at `/opt/qh`,
   and the boundary then executes `/opt/qh/qh/boundary_child.py`.  An
   untrusted controller can therefore select the code bytes used as the
   trusted boundary child unless this value is operator-bound.

C. `request["identity_sha256"]` is treated as the expected Codex
   identity while `request["identity_exe_path"]` supplies the executable
   being checked.  A controller can supply arbitrary executable bytes
   plus their matching SHA-256 and satisfy the current "identity pin"
   check.

Independent Control Room source-level probes against the exact
implementation bytes established:

```
CONTROLLER_CHOSEN_RW_BIND        = ACCEPTED
CONTROLLER_CHOSEN_HARNESS_ROOT   = ACCEPTED
SELF_ASSERTED_EXECUTABLE_IDENTITY = ACCEPTED
```

This is incompatible with the accepted requirement that the exact launch
identity/profile/evidence/output boundary be frozen by trusted authority
rather than self-asserted by the controller.  Impact:

- C-3 exact identity pin is not a trusted pin at the integrated boundary;
- evidence/target/output mount identity is not Control-Room bound;
- future real credential custody would be unsafe to rely on, because a
  controller-selected boundary child could potentially move
  child-visible custody material into a controller-readable writable
  surface.

Therefore the integrated C-2/C-3 composition is NOT accepted.

## 9. Blocking finding IR-003 — AUCDEV023-CR-IMPL-003

```
Classification:
HARNESS/PROTOCOL DEFECT
/ TEST_HOOK_PRODUCTION_TRUST_PATH
/ YAMA_GATE_OVERRIDE
Support: OBSERVED_FACT
```

The operational `qh supervisor` CLI exposes `--yama-override`, and
`Supervisor.startup()` uses the supplied value INSTEAD OF reading the
real kernel `ptrace_scope`.  The mandatory environmental gate is
therefore not mechanically mandatory on that execution path.  An
independent source-level Control Room probe established that when the
real-Yama reader was deterministically forced to report `0`, supplying
policy `yama_value=1` allowed the startup gate to continue with exit
state 0.  This is a deterministic code-path proof, NOT a claim that the
current host's actual Yama value is 0.

Test fault-injection controls must not be able to weaken production
trust checks.  The existing test-only fault-injection functionality may
be retained only through a mechanically separate test surface that
cannot be selected by the untrusted controller or by the production
launch path.

## 10. Provider credential integration — blocker HELD

```
Classification:
COMPLETENESS_LIMITATION
/ IMPLEMENTATION_BLOCKER
/ PROVIDER_CREDENTIAL_CUSTODY_INTEGRATION_NOT_IMPLEMENTED
```

The implementation correctly discloses
`PROVIDER_SPECIFIC_INTEGRATION_STATUS = NOT_IMPLEMENTED_INTERFACE_ONLY`.
Synthetic credential custody evidence is useful and retained.  However,
real provider credential integration is NOT implemented.  The
implementation MUST NOT be described as campaign-ready or as having
completed the mandatory credential-custody enforcement path.  This is
NOT treated as concealment or a false evidence claim, because the
implementer explicitly reported the blocker.  It IS a blocker to
accepting `AUCDEV023_IMPLEMENTATION_COMPLETE_AWAITING_CONTROL_ROOM_READBACK`
as the governing implementation result.

## 11. Record precision — harness file-count correction (current-facing only)

```
Classification:
COMPLETENESS_LIMITATION
/ RECORD_PRECISION
/ QUALIFICATION_HARNESS_FILE_COUNT
```

The live tree for `qualification-harness/` at the implementation commit
contains **31 regular blobs, not 30** (mechanically:
`git ls-tree -r 3c59264 -- qualification-harness` → 31 blobs, all mode
100644).  The implementation commit total of 34 changed paths is correct:
31 qualification-harness paths + 3 governance/report paths = 34.  The
current-facing count is corrected to 31 by THIS publication.  The
historical implementation commit and the source implementation handoff
archive are NOT rewritten.

## 12. Governing implementation result

NOT accepted as the governing result:

```
AUCDEV023_IMPLEMENTATION_COMPLETE_AWAITING_CONTROL_ROOM_READBACK
```

Published instead:

```
AUCDEV023_IMPLEMENTATION_READBACK_PARTIALLY_ACCEPTED
/ REMEDIATION_REQUIRED_BEFORE_INDEPENDENT_HARNESS_AUDIT
```

Accepted implementation evidence remains valid only at the strengths
explicitly recorded in §5 and §6.  AUCDEV-023 remains **P1 / READY**
(NOT DONE).  Reason for keeping READY: the remediation objective remains
bounded and execution-ready; this readback does NOT reopen G-1/G-2
design research.  The next change is implementation remediation of
demonstrated trust-boundary defects, not a return to readiness-gap
investigation.

## 13. Independent harness audit — DEFERRED

The independent harness audit is DEFERRED.  Reason: the current
implementation SHA has known blocking trust-boundary defects and will
necessarily change during remediation.  A verdict on this SHA MUST NOT
transfer to the remediated SHA.  Spending independent audit authority on
a target already known to require replacement is avoided.  The
independent harness audit remains mandatory AFTER:

1. bounded remediation;
2. Control Room readback of the remediation;
3. exact remediated SHA freeze.

## 14. Next bounded objective (RECORDED, NOT EXECUTED)

Recorded, but NOT executed and NOT authorized by this publication:

**AUCDEV-023 TRUST-ANCHOR AND LAUNCH-SPEC BINDING REMEDIATION.**

The future remediation must be limited to demonstrated blockers.  At
minimum it must address:

A. a mechanically distinct Control-Room/operator launch-authority root
   that a same-UID untrusted controller cannot mint/recreate/self-assert;

B. immutable trusted binding of the COMPLETE security-critical launch
   spec, including:

   - harness code identity;
   - evidence identity/source;
   - target identity/source;
   - auditor-output identity/source;
   - Codex executable expected identity;
   - Codex config/profile identity;
   - allowed read/write/mount roles;
   - credential-custody adapter identity;
   - attempt/root/bootstrap-manifest identity;

C. controller request values must be treated as requests/claims and
   compared against the trusted bound spec, never used as authority by
   themselves;

D. production trust checks must not expose a test override capable of
   changing mandatory Yama/no-egress/custody decisions;

E. provider-specific credential adapter integration must either be
   implemented with synthetic fixtures and no real credentials, or
   remain an explicit blocker with no campaign-reliance claim.

Do NOT redesign the already-accepted C-1, no-egress or GATE-W mechanics
unless the remediation dependency requires a surgical interface change.

## 15. Campaign / qualification held state (preserved EXACTLY)

```
AUDITOR_A_AUTHORITY            = CONSUMED_CLOSED
AUDITOR_B_AUTHORITY            = CONSUMED_CLOSED
MODEL_ENGAGEMENTS_AUTHORIZED   = 2
MODEL_ENGAGEMENTS_USED         = 2
FIRST_PASS_A                   = PRESENT / FROZEN
FIRST_PASS_B                   = ABSENT
FIRST_PASS_BARRIER             = CLOSED
NO_CONFORMING_BLIND_FIRST_PASS_SET
CAMPAIGNS                      = 2 OF MAX 2
CAMPAIGN_3                     = NOT AUTHORIZED / DOES NOT EXIST
AUCDEV-010                     = P1 / BLOCKED
QUALIFICATION                  = NONE
INSTALLATION                   = NONE
```

No historical verdict changes.

## 16. Current-facing state after this publication

```
Active/current item      : AUCDEV-023 / P1 / READY
Implementation state     : PARTIALLY_ACCEPTED / REMEDIATION_REQUIRED
Independent harness audit: DEFERRED_PENDING_REMEDIATION
```

G-1/G-2 design/probe readiness closures remain historical accepted
evidence.  The implementation defects recorded here do NOT reopen those
design/probe results.  Next action EXACTLY ONE:

```
INDEPENDENT CONTROL ROOM READBACK OF THIS IMPLEMENTATION-READBACK
GOVERNANCE PUBLICATION.
```

The publication itself does NOT authorize remediation.

Result: `AUCDEV_023_QUALIFICATION_HARNESS_IMPLEMENTATION_READBACK_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
