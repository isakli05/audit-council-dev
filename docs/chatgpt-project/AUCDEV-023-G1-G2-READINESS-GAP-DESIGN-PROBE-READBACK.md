# AUCDEV-023 — G-1/G-2 Readiness-Gap Design/Probe Investigation: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION IMPLEMENTER ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room, NOT a qualification authority, NOT an installation authority, NOT remediation implementation; NO new design/probe execution; NO auditor/model execution; NO package rebuild; NO qualification; NO installation; NO Campaign-2 recovery; NO Campaign-3; ZERO provider/model/frontier calls by this publication session |
| Date | 2026-09-17 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-17) authorizes ONLY this publication of the Control Room's readback disposition of the AUCDEV-023 G-1/G-2 readiness-gap design/probe investigation handoff; it does NOT authorize the follow-up G-2 probe, any remediation implementation, auditor/model execution, package rebuild/reseal, qualification, installation, Campaign-2 recovery or Campaign 3. |
| Exact governance base | `61547f85770334a18fe03742b93437406066d579` (the Campaign-2 terminal-harness root-cause scoping publication-readback correction commit; sole parent `ef9a78ec0f36ed5fc3fac1cd7e334b27b1003a74`; tree `a7675ef9b039f85fcf8dc14ce11bb59d2fd59403`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this publication's bootstrap and re-resolved EXACT immediately before its single fast-forward push; THIS publication is the sole commit ahead of that base |
| Subject investigation | AUCDEV-023 G-1/G-2 readiness-gap closure design + deterministic probe investigation (2026-09-17, zero-model, zero canonical repository mutation) — source handoff `AUCDEV-023-G1G2-READINESS-GAP-DESIGN-PROBE-handoff-20260917.tar.gz` |
| Qualification/installation | readiness BLOCKED / qualification NONE / installation NONE (unchanged) |

## 1. Source investigation handoff — integrity VERIFIED (read-only)

Control Room verification independently re-executed read-only by THIS
publication session before any mutation (identical results):

- outer SHA-256 `6833ba187687e70fd46e2e27197deb7397a321b565c096abcd873fb116063b05`
- **794886 bytes**
- member census: **52 total = 38 regular files + 14 directories**
- unsafe/traversal 0; duplicates 0; symlink/hardlink/special 0
- exactly ONE `SHA256SUMS`
- the `SHA256SUMS` contains **37 payload checksum entries**
- checksum verification result: **37/37 PASS**

The archive was inspected in an isolated temporary location, its content NOT
executed, and NO credential, auth value, Auditor-A substantive material or
Auditor-B substantive runtime material is republished here (the handoff's
`codex-home` fixture is the investigation's synthetic INERT auth fixture;
its contents are not disclosed in this record).

Investigation session self-declarations accepted as verified where
mechanically supported by the handoff evidence: ZERO provider/model
engagements; ZERO canonical repository mutation; Campaign-2 terminal state
unchanged by the investigation.

## 2. Control Room readback disposition (recorded verbatim)

```
AUCDEV_023_G1G2_READINESS_GAP_INVESTIGATION_READBACK_PARTIALLY_ACCEPTED
/ HANDOFF_INTEGRITY_VERIFIED
/ ZERO_CANONICAL_REPO_MUTATION_ACCEPTED
/ G1_DESIGN_PROBE_CLOSURE_ACCEPTED_WITH_MANDATORY_CREDENTIAL_CUSTODY_INVARIANT
/ G2_CUSTOM_PERMISSION_PROFILE_MATRIX_ACCEPTED
/ G2_EXEC_POLICY_EQUIVALENCE_NOT_ESTABLISHED
/ G2_PRIMARY_WORKSPACE_WRITABILITY_NOT_RESOLVED
/ G2_HOST_LAYOUT_FIX_PROBE_PARTIAL_STATIC_FIXTURE_INVALID
/ G2_REMAINS_OPEN
/ READY_RECOMMENDATION_NOT_ACCEPTED
/ AUCDEV023_REMAINS_P1_OPEN
/ CAMPAIGN2_TERMINAL_UNCHANGED
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
```

This is a governance readback record only. The investigation's evidence is
accepted only at the strengths recorded below; its `G-2 = CLOSED` and
`READY_RECOMMENDED_FOR_CONTROL_ROOM_REVIEW` conclusions are NOT accepted.

## 3. G-1 readback — DESIGN/PROBE CLOSURE ACCEPTED

```
G1_DESIGN_PROBE_CLOSURE = ACCEPTED
```

Selected design direction accepted: a Control-Room/operator-minted, one-shot
supervising gatekeeper that holds attempt authority only in kernel-protected
process state, with:

- `PR_SET_DUMPABLE=0`;
- process-bound authority rather than controller-writable files;
- one-shot binding to exact attempt/root;
- terminal `PREEXEC_STOP` state;
- replay/reforge rejection;
- new attempt only through a new out-of-band operator mint.

Accepted deterministic evidence (handoff `g1-matrix`, zero-provider):

- same-UID `/proc` memory/fd/environ/maps/cwd access denied;
- ptrace denied;
- authorized use succeeds once;
- second/replayed use fails;
- wrong attempt/root fails;
- `PREEXEC_STOP` prevents later launch;
- on-disk observability-ledger tampering does not restore authority;
- SIGKILL results in fail-closed DoS, not authority gain;
- fresh operator mint creates a distinct new attempt without changing
  campaign authority accounting.

### 3.1 MANDATORY IMPLEMENTATION INVARIANT

```
CREDENTIAL_CUSTODY_IS_REQUIRED_FOR_G1_ENFORCEMENT
```

Reason: if the same-UID controller retains ambient readable provider
credentials, it can bypass the launch gate by independently constructing a
provider-capable launch. Any future C-2 implementation MUST:

- remove/seal real provider credentials from controller-readable surfaces for
  the campaign duration;
- keep unsealed credential material outside the controller's readable
  process/filesystem authority surface;
- release it only into the supervised authorized launch path;
- fail closed if custody cannot be established;
- preserve a bounded restore/recovery procedure.

The investigation demonstrated the process-bound custody primitive with
SYNTHETIC credentials. Actual provider credential integration remains
IMPLEMENTATION WORK and must be independently reviewed before reliance.

### 3.2 Preserved host assumption

Yama `ptrace_scope >= 1` is a required prelaunch environmental gate for the
demonstrated Linux design (observed host value 1). NOT claimed: cross-platform
portability; SIGKILL resistance (SIGKILL is accepted as fail-closed DoS).

## 4. G-2 — ACCEPTED EVIDENCE

```
G2_CUSTOM_PERMISSION_PROFILE_DYNAMIC_MATRIX = ACCEPTED
```

The zero-provider `codex sandbox --sandbox-state-json` vehicle mechanically
demonstrated, under the exact local codex-cli 0.154.0 runtime:

- restricted managed permission-profile enforcement;
- `/auditor-output` create/read/modify/mkdir/delete ALLOWED;
- `/auditor-evidence` write/delete REFUSED while read remains ALLOWED;
- runtime/system writes REFUSED;
- unrelated host target absent/refused under outer composition;
- no demonstrated widening of outer bwrap filesystem confinement;
- default read-only policy refuses writes;
- the exact local Codex sandbox runtime uses the observed bwrap + re-exec
  enforcement path.

Also accepted — host-layout root-cause evidence: restricted profiles on the
merged-usr/NVM host require additional treatment for dynamic payload
interpreter paths. The shipped-zsh probe established that a candidate
real-directory bind layout can make the dynamic shell executable while
preserving at least the directly tested evidence-write denial.

## 5. G-2 — CLOSURE REJECTED (G-2 remains OPEN)

### 5.1 EXEC POLICY EQUIVALENCE NOT ESTABLISHED

The investigation report itself classifies as INFERENCE the statement that
`codex exec -s workspace-write --add-dir /auditor-output` derives a managed
restricted permission profile equivalent to the custom `sandbox-state-json`
profile used by the successful zero-provider probes. The readiness task
required the probe vehicle to be SHOWN to exercise semantics equivalent to
the intended future Auditor-B application policy. Same underlying sandbox
runtime is necessary but NOT sufficient evidence that the exec-side derived
permission entries are identical.

```
G2_EXEC_POLICY_EQUIVALENCE = NOT_ESTABLISHED
```

No provider/model call may be spent merely to resolve this.

### 5.2 PRIMARY WORKSPACE WRITABILITY NOT RESOLVED

The exact local codex-cli 0.154.0 help says `--add-dir` adds writable
directories ALONGSIDE THE PRIMARY WORKSPACE. The historical actual Auditor-B
launch shape used `-C /auditor-home`; the successful custom-profile probe
instead used `sandboxCwd = file:///auditor-output` and explicitly demonstrated
`/auditor-home` as absent/non-writable. Therefore the proposed future
shorthand `codex exec ... -s workspace-write --add-dir /auditor-output` is NOT
sufficiently frozen unless its exact primary workspace / `-C` behavior is also
resolved. A future policy must prove mechanically that the effective
application sandbox exposes NO writable surface beyond those explicitly
authorized by the AUCDEV-023 requirement. If `workspace-write` necessarily
makes the primary workspace writable, the design must either:

- choose/bind the primary workspace so it is itself the authorized output
  surface; OR
- select another exact application-policy mechanism whose dynamic behavior
  can be proven zero-provider.

NEITHER option is selected by this publication.

```
COMPLETENESS_LIMITATION
/ G2_PRIMARY_WORKSPACE_POLICY_NOT_RESOLVED
```

### 5.3 Host-layout fix probe — partial static-fixture invalid

The candidate real-directory bind experiment contains useful evidence:
shipped zsh executed; zsh write to `/auditor-output` succeeded; zsh write to
`/auditor-evidence` was refused. However its three subsequent static-payload
checks are NOT valid permission-matrix evidence: the probe script invoked
`/auditor-evidence/g2payload` without staging that file into the candidate
probe's evidence fixture, and those invocations produced Rust/linux-sandbox
panic output rather than meaningful permission-operation results.

```
COMPLETENESS_LIMITATION
/ PROBE_FIXTURE
/ G2P05_STATIC_PAYLOAD_NOT_STAGED
```

The valid zsh evidence is NOT discarded; the panicked static checks are NOT
counted as PASS or as permission REFUSAL. A future G-2 closure probe must
repair this fixture and rerun the candidate outer-layout denial matrix
cleanly.

### 5.4 G-2 governing status

```
G2 = OPEN
```

Accepted: custom-profile dynamic permission matrix; sandbox runtime identity;
outer+inner composition evidence; host-layout root-cause; partial
real-dir-bind candidate evidence. Not established: exact future `codex exec`
policy derivation; exact primary-workspace writability; complete clean
dynamic-shell candidate matrix. Therefore the investigation's `G-2 = CLOSED`
and `READY_RECOMMENDED_FOR_CONTROL_ROOM_REVIEW` are NOT accepted by the
Control Room.

## 6. AUCDEV-023 governing status

`AUCDEV-023` remains **P1 / OPEN**.

- G-1: DESIGN/PROBE CLOSED / ACCEPTED, with the mandatory credential-custody
  and Yama environmental invariants carried into implementation scope.
- G-2: OPEN.

AUCDEV-023 MUST NOT transition OPEN -> READY on the basis of this readback.
No implementation is authorized.

## 7. Next G-2 evidence required (RECORDED, NOT EXECUTED)

The remaining bounded evidence objective for the next design/probe task
(NOT authorized by this publication) is ZERO-PROVIDER evidence for the exact
future application policy, including:

A. exact future `-C` / primary-workspace choice;
B. exact relationship between the future `codex exec` configuration and the
   effective permission profile;
C. proof that only the authorized output surface is writable;
D. clean dynamic-shell execution under the corrected merged-usr outer layout;
E. repaired g2p05 fixture with all denial tests producing semantic permission
   results rather than panic/missing-payload failures;
F. deterministic evidence sufficient to freeze the future application policy
   without making a provider/model inference call.

If exact exec-side derivation cannot be mechanically observed zero-provider,
the investigator must NOT mark G-2 closed merely from shared-runtime evidence.

## 8. Held Campaign-2 terminal state (preserved EXACTLY)

```
AUDITOR_A_AUTHORITY = CONSUMED_CLOSED
AUDITOR_B_AUTHORITY = CONSUMED_CLOSED
MODEL_ENGAGEMENTS_AUTHORIZED = 2
MODEL_ENGAGEMENTS_USED = 2
FIRST_PASS_A = PRESENT / FROZEN / mechanical custody
FIRST_PASS_B = ABSENT
FIRST_PASS_BARRIER = CLOSED
NO_CONFORMING_BLIND_FIRST_PASS_SET
CAMPAIGNS = 2 OF MAX 2
CAMPAIGN_3 = NOT AUTHORIZED / DOES NOT EXIST
QUALIFICATION_EVIDENCE_COMPLETENESS = BLOCKING
QUALIFICATION = NONE
INSTALLATION = NONE
```

Nothing in this readback altered, reinterpreted, revived, or reset any of
these states; no historical verdict was rewritten. AUCDEV-010 remains
**P1 / BLOCKED** (linkage recorded in the backlog history structure only; its
status is unchanged by this publication).

## 9. Publication change set (EXACTLY these paths)

1. `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (current-facing fields
   updated; `Last updated` and checkpoint advanced; history record 76
   appended)
2. `docs/chatgpt-project/AUCDEV-BACKLOG.md` (AUCDEV-023 queue row and work
   item appended with the G-1/G-2 readback governing status; AUCDEV-023
   history record appended; counts UNCHANGED)
3. `docs/chatgpt-project/AUCDEV-023-G1-G2-READINESS-GAP-DESIGN-PROBE-READBACK.md`
   (THIS canonical readback record; NEW path)

NOT changed: `AUCDEV-QUALIFICATION-HISTORY.md`,
`AUCDEV-ARCHITECTURE-SUMMARY.md`, `skill/`, `tests/`, schemas/contracts,
frozen Campaign-2 artifacts, historical AUCDEV-010 reports, AUCDEV-020/021/022.

## 10. Next action and result

Immediate next action (EXACTLY ONE): **INDEPENDENT CONTROL ROOM READBACK OF
THIS AUCDEV-023 G-1/G-2 INVESTIGATION READBACK PUBLICATION.** This
publication itself does NOT authorize the follow-up G-2 probe.

Result: `AUCDEV_023_G1G2_READINESS_GAP_INVESTIGATION_READBACK_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
