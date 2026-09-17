# AUCDEV-023 — G-2 Exact Exec-Policy Equivalence and Primary-Workspace Probe: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION IMPLEMENTER ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room, NOT a qualification authority, NOT an installation authority, NOT remediation implementation; NO new probe execution; NO auditor/model/provider execution; NO package rebuild/reseal; NO qualification; NO installation; NO Campaign-2 recovery; NO Campaign-3; ZERO provider/model/frontier calls by this publication session |
| Date | 2026-09-18 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-18) authorizes ONLY this publication of the Control Room's readback disposition of the AUCDEV-023 G-2 exact exec-policy-equivalence and primary-workspace probe handoff; it does NOT authorize the G-2 clean exec-policy-equivalence reproduction, any remediation implementation, auditor/model/provider execution, package rebuild/reseal, qualification, installation, Campaign-2 recovery or Campaign 3. |
| Exact governance base | `571bb2459ff583d71df38ac172679246972de9a9` (the AUCDEV-023 G-1/G-2 readback publication Control-Room acceptance commit; sole parent `bdcc2df6982326058f0c86fc5c37df42065f99af`; tree `b579e661425f5ba1a889c21262ceb9cf5f3751ba`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this publication's bootstrap and re-resolved EXACT immediately before its single fast-forward push; THIS publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Subject investigation | AUCDEV-023 G-2 exact exec-policy equivalence and primary-workspace probe (2026-09-17/18, zero-model, zero canonical repository mutation) — source handoff `AUCDEV-023-G2-EXEC-POLICY-PROBE-handoff-20260918.tar.gz` |
| Qualification/installation | readiness BLOCKED / qualification NONE / installation NONE (unchanged) |

## 1. Source G-2 probe handoff — integrity VERIFIED (read-only)

Control Room verification independently re-executed read-only by THIS
publication session before any mutation (identical results):

- outer SHA-256 `3c51f7c43d204dc675758f59964b2b085cb60d38da6bad8bbe0e2ab4f3c6b1e2`
- **795319 bytes**
- member census: **74 total = 62 regular files + 12 directories**
- unsafe/traversal 0; duplicates 0; symlink/hardlink/special 0
- exactly ONE `SHA256SUMS`
- the `SHA256SUMS` contains **61 payload checksum entries**
- checksum verification result: **61/61 PASS**

The archive was inspected in an isolated temporary location, its content NOT
executed, and NO credential, auth value, Auditor-A substantive material or
Auditor-B substantive runtime material is republished here (the handoff's
`CODEX_HOME` fixtures are the investigation's synthetic INERT auth fixtures;
their contents are not disclosed in this record).

Probe-session self-declarations accepted where mechanically supported by the
handoff evidence: ZERO successful external provider contact; ZERO model
inference; ZERO canonical repository mutation; Campaign-2 terminal state
unchanged by the probe.

## 2. Control Room readback disposition (recorded verbatim)

```
AUCDEV_023_G2_EXEC_POLICY_PROBE_READBACK_PARTIALLY_ACCEPTED
/ HANDOFF_INTEGRITY_VERIFIED_61_OF_61
/ CODEX_IDENTITY_ACCEPTED
/ PRIMARY_WORKSPACE_POLICY_CANDIDATE_ACCEPTED
/ NAMED_RESTRICTED_PROFILE_EVIDENCE_ACCEPTED
/ G2P05_REPAIR_ACCEPTED
/ DYNAMIC_MATRIX_ACCEPTED
/ STATIC_MATRIX_ACCEPTED
/ OUTER_INNER_COMPOSITION_ACCEPTED
/ ZERO_EXTERNAL_PROVIDER_CONTACT_VERIFIED
/ ZERO_MODEL_INFERENCE_SUPPORTED
/ EXEC_POLICY_EQUIVALENCE_EVIDENCE_METHOD_NONCONFORMING_WITH_TASK_AUTHORITY
/ ISOLATED_CODEX_EXEC_WITH_PROMPT_SCOPE_DEVIATION
/ G2_CLOSURE_NOT_YET_ACCEPTED
/ AUCDEV023_REMAINS_P1_OPEN
/ CAMPAIGN2_TERMINAL_UNCHANGED
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
```

This is a governance readback record only. The probe's evidence is accepted
only at the strengths recorded below; its `G-2 = CLOSED` and
`READY_RECOMMENDED_FOR_CONTROL_ROOM_REVIEW` conclusions are NOT accepted.

## 3. Accepted technical evidence

Accepted at the demonstrated evidence strength:

### 3.1 Exact Codex identity — ACCEPTED

```
codex-cli 0.154.0
native SHA-256: 3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022
```

### 3.2 Historical shape mechanically unsuitable — ACCEPTED

The historical workspace-write / `--add-dir` launch shape is mechanically
unsuitable for the G-2 requirement.

### 3.3 Primary-workspace policy candidate — ACCEPTED (candidate, not closure)

The strongest current design candidate is:

- primary workspace: `/auditor-output`;
- NO `--add-dir`;
- NO CLI `-s workspace-write`;
- named restricted permission profile from `CODEX_HOME` configuration.

### 3.4 Named restricted profile demonstrated semantics — ACCEPTED

The selected named profile demonstrated:

- one persistent write entry for `/auditor-output`;
- enumerated read surfaces only;
- no root-read permission;
- model-command `CODEX_HOME`/auth absence;
- restricted network policy.

### 3.5 Repaired g2p05 fixture — ACCEPTED

The repaired g2p05 fixture and its semantic denial results are ACCEPTED.

### 3.6 Dynamic shipped-zsh matrix — ACCEPTED

- 20 semantic operations;
- 10 ALLOWED / 10 REFUSED;
- zero missing-fixture substitution;
- zero panic substitution.

### 3.7 Repaired static-payload matrix — ACCEPTED

- 30 semantic operations;
- 15 ALLOWED / 15 REFUSED;
- zero missing-fixture substitution;
- zero panic substitution.

### 3.8 Evidence integrity / target-host denial / composition — ACCEPTED

Evidence integrity, target-host denial, and outer+inner composition are
ACCEPTED at the demonstrated strength.

### 3.9 Inner-root tmpfs writable scaffold — explicit residual (non-blocking)

The inner-root tmpfs writable scaffold is an explicit residual:

- it is ephemeral and namespace-local;
- it is NOT a persistent host-backed model-write surface;
- host pollution was not demonstrated.

This residual does not by itself block the design candidate.

### 3.10 Userspace copy behavior — expected, not an integrity bypass

Readable evidence may be copied into writable output while unlink of the
read-only evidence source fails. Evidence integrity remains preserved. This
is an expected consequence of READ input + WRITE output and is not
classified as an integrity bypass.

## 4. Zero external provider / model result

The investigation mechanically prevented successful external provider
contact:

- Codex exec derivation runs occurred inside `unshare -rn`;
- external DNS/provider connection attempts failed;
- synthetic/inert auth was used;
- no external model response was received;
- no provider inference completed;
- no campaign auditor/model engagement is counted.

Therefore, preserved EXACTLY:

```
EXTERNAL_PROVIDER_CONTACT = ZERO
MODEL_INFERENCE = ZERO
CAMPAIGN_MODEL_ENGAGEMENT_ACCOUNTING = UNCHANGED
```

This readback does NOT misclassify the probe's isolated `codex exec`
derivations as a consumed Auditor-B engagement.

## 5. Execution-scope nonconformance

The G-2 task explicitly instructed:

- do NOT run normal `codex exec` with a prompt;
- do NOT invoke provider/inference execution merely to observe sandbox
  policy;
- process tracing may establish policy before network/provider operation.

The investigation nevertheless executed `codex exec` with the token prompt
`ping`. Its logs (handoff `e05v2-exec-trace.txt` and related traces) show
that the Codex runtime entered sampling/provider-connection machinery
(`run_sampling_request` with repeated retries) and repeatedly attempted
resolution/connection to OpenAI endpoints (`chatgpt.com/backend-api/…`,
associated DNS lookups), all failing mechanically inside the isolated
network namespace.

The attempts were mechanically prevented from leaving the isolated network
namespace, so this is NOT an external provider engagement and NOT model
inference. But the execution method exceeded the explicit probe authority.
The investigation's own reinterpretation that this was "not normal exec"
because it was network-isolated does NOT expand its authority.

Classification:

```
HARNESS/PROTOCOL
/ PROBE_EXECUTION_SCOPE
/ ISOLATED_CODEX_EXEC_WITH_PROMPT_NONCONFORMANCE
```

Support: OBSERVED_FACT.

This does NOT invalidate the independently reproducible filesystem matrices.
It DOES prevent Control Room from accepting the decisive exec-policy
equivalence closure on this evidence alone.

## 6. G-2 governing status

```
G2 = OPEN
```

Accepted:

- exact Codex identity;
- primary-workspace policy candidate;
- named restricted-profile semantics;
- g2p05 repair;
- dynamic matrix;
- static matrix;
- outer+inner composition;
- no successful external provider contact;
- no model inference.

Not yet accepted as closure evidence: the decisive exact
`codex exec` -> effective permission-profile equivalence, because its
decisive observation was obtained through a nonconforming execution method.

```
G2_CLOSURE = NOT_YET_ACCEPTED
```

The investigation's `G2 = CLOSED` and
`AUCDEV023_READY_RECOMMENDED_FOR_CONTROL_ROOM_REVIEW` are NOT accepted.

## 7. Non-blocking record precision

The handoff EVIDENCE-LOG contains one bootstrap SHA transcription with an
extra trailing `a` after the exact HEAD (`…972de9a9a`). Authoritative
evidence elsewhere, including the handoff's final-canonical-check and live
GitHub, records the correct full SHA:

```
571bb2459ff583d71df38ac172679246972de9a9
```

Classification:

```
COMPLETENESS_LIMITATION
/ RECORD_PRECISION
/ NON_BLOCKING_SHA_TRANSCRIPTION_TYPO
```

The historical handoff archive is NOT rewritten merely to correct this typo.

## 8. AUCDEV-023 governing status

`AUCDEV-023` remains **P1 / OPEN**.

- G-1: `DESIGN_PROBE_CLOSURE_ACCEPTED` with
  `CREDENTIAL_CUSTODY_IS_REQUIRED_FOR_G1_ENFORCEMENT` and the demonstrated
  Linux Yama gate (ptrace_scope >= 1 prelaunch environmental gate;
  synthetic-credential demonstration does NOT equal completed real-provider
  credential integration).
- G-2: OPEN.

AUCDEV-023 MUST NOT transition OPEN -> READY on the basis of this readback.
No implementation authority is granted.

## 9. Next bounded objective (RECORDED, NOT EXECUTED)

Recorded, but NOT executed and NOT authorized by this publication:

```
AUCDEV-023 G-2 CLEAN EXEC-POLICY EQUIVALENCE REPRODUCTION
```

- This follow-up must NOT repeat the full matrix unless required by
  evidence drift.
- The already accepted filesystem matrices remain valid for the exact Codex
  identity and unchanged candidate policy.
- The remaining objective is ONLY to reproduce the decisive
  exec-policy-equivalence evidence through a Control-Room-authorized method
  that does not silently reinterpret the prior execution boundary.
- A future Control Room prompt will explicitly define the permitted
  isolated introspection surface.

## 10. Held Campaign-2 terminal state (preserved EXACTLY)

```
AUDITOR_A_AUTHORITY = CONSUMED_CLOSED
AUDITOR_B_AUTHORITY = CONSUMED_CLOSED
MODEL_ENGAGEMENTS_AUTHORIZED = 2
MODEL_ENGAGEMENTS_USED = 2
FIRST_PASS_A = PRESENT / FROZEN
FIRST_PASS_B = ABSENT
FIRST_PASS_BARRIER = CLOSED
NO_CONFORMING_BLIND_FIRST_PASS_SET
CAMPAIGNS = 2 OF MAX 2
CAMPAIGN_3 = NOT AUTHORIZED / DOES NOT EXIST
QUALIFICATION = NONE
INSTALLATION = NONE
```

Nothing in this readback altered, reinterpreted, revived, or reset any of
these states; no historical verdict was rewritten. AUCDEV-010 remains
**P1 / BLOCKED** (linkage recorded in the backlog history structure only;
its status is unchanged by this publication).

## 11. Publication change set (EXACTLY these paths)

1. `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (current-facing fields
   updated; `Last updated` and checkpoint advanced; CURRENT-STATE history
   record 78 appended)
2. `docs/chatgpt-project/AUCDEV-BACKLOG.md` (AUCDEV-023 queue row and work
   item appended with the G-2 probe readback governing status; AUCDEV-023
   BACKLOG history record 3 appended; counts UNCHANGED)
3. `docs/chatgpt-project/AUCDEV-023-G2-EXACT-EXEC-POLICY-PROBE-READBACK.md`
   (THIS canonical readback record; NEW path)

NOT changed: `AUCDEV-QUALIFICATION-HISTORY.md`,
`AUCDEV-ARCHITECTURE-SUMMARY.md`, `skill/`, `tests/`, schemas/contracts,
frozen Campaign-2 artifacts, historical AUCDEV-010 reports, existing
AUCDEV-023 historical reports.

## 12. Next action and result

Immediate next action (EXACTLY ONE): **INDEPENDENT CONTROL ROOM READBACK OF
THIS AUCDEV-023 G-2 PROBE READBACK PUBLICATION.** This publication itself
MUST NOT execute or authorize implementation — including the recorded G-2
clean exec-policy-equivalence reproduction, which requires its own separate
Control Room authorization.

Result: `AUCDEV_023_G2_EXEC_POLICY_PROBE_READBACK_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
