# AUCDEV-023 — EBS Second Remediation: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION SESSION ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room decision-maker (this session publishes the Control Room's already-decided readback disposition verbatim), NOT an independent auditor, NOT authorized to modify bootstrap-supervisor implementation source, NOT authorized to remediate the new finding, NOT authorized to prepare an event package, NOT authorized to instantiate a bootstrap event, NOT authorized to invoke any provider/model/auditor, `/audit-council`, real credential, qualification process, or installation; ZERO provider/model/frontier calls |
| Date | 2026-09-19 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-19) authorizes ONLY this record-only/append-only publication of the Control Room readback disposition of the AUCDEV-023 second bounded EBS remediation candidate. It does NOT authorize implementation-source modification, the narrow REM2-001 remediation, event-package preparation, auditor/model/provider execution, qualification, installation, or any bootstrap event step. The disposition below was ALREADY DECIDED by the Control Room; it is recorded faithfully — not reinterpreted, weakened, strengthened, merged, closed, or invented. |
| Candidate under readback | `8f998209ed401f7a22586f2cfdee4d89d440faf9` (tree `8b089aab5cca1c2c8ef18f458051546b287ee0ad`; sole parent / implementation base `a9bbdea7aeebfc475b7042410943f32fccbe5e83`; bootstrap-supervisor subtree `f0cbe9473aaf397a1c9a4d299a70bbbdf27f0f9f`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this publication session's bootstrap |
| Subject | The AUCDEV-023 second bounded EBS remediation publication (commit `8f998209…`, canonical record `AUCDEV-023-EBS-SECOND-REMEDIATION-REPORT.md`, the remediated `bootstrap-supervisor/**` candidate for AUCDEV023-CR-EBS-REM-001), its handoff archive identity/integrity, its submitted deterministic test evidence, the disposition of AUCDEV023-CR-EBS-REM-001 and the CR-EBS-001 remainder, the reconfirmation of CR-EBS-002/-003 on the new SHA, the TCB LOC disposition, and the ONE NEW blocking finding AUCDEV023-CR-EBS-REM2-001 recorded by this readback |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **BLOCKED_PENDING_NARROW_EBS_MANIFEST_TYPE_REMEDIATION_AND_FRESH_CONTROL_ROOM_READBACK_AND_EVENT_PREPARATION_AND_SEPARATE_EXECUTION_AUTHORITY** — the readback's PARTIAL disposition keeps the independent harness audit blocked; no auditor has reviewed `d4d584ff…` |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `OBSERVED_SOURCE_FACT` / `REQUIREMENT_CLAIM`
(Control Room finding support classes, recorded verbatim from the
disposition), `REQUIREMENT` (record-mandated property). §§2–9 are the
CONTROL ROOM's disposition recorded EXACTLY; this publication session
neither adjudicates nor amends it.

---

## 1. Live bootstrap and candidate identity (OBSERVED_FACT)

Live `refs/heads/master` of `isakli05/audit-council-dev` was resolved at
this session's bootstrap (fetch + `git rev-parse origin/master`) and
required to equal EXACTLY the mandated second-remediation candidate
`8f998209ed401f7a22586f2cfdee4d89d440faf9`; it did, so no
STOP-WITHOUT-MUTATION was required:

- candidate commit `8f998209ed401f7a22586f2cfdee4d89d440faf9`;
- tree `8b089aab5cca1c2c8ef18f458051546b287ee0ad`;
- sole parent `a9bbdea7aeebfc475b7042410943f32fccbe5e83`
  (single-parent confirmed via `git show -s`);
- `bootstrap-supervisor` subtree
  `f0cbe9473aaf397a1c9a4d299a70bbbdf27f0f9f`;
- qualification-harness tree
  `5b8d5e5465923740470ff63ed9b8683f257a3787` — EQUAL to the frozen
  audit target `d4d584ffa47ad2848268ba947247f81a845b2322` (unchanged);
- skill tree `c792933a862d9a5434681a88d183470dd8b15d2f` — EQUAL to the
  frozen audit target (unchanged);
- exact compare base..candidate: **one commit ahead / zero behind**;
  changed paths EXACTLY **14** (10 `bootstrap-supervisor/**` files —
  `ebs/binding.py`, `ebs/__init__.py`, `ebs/launch.py`, `MANIFEST.json`,
  `README.md`, `tests/conftest.py`, NEW `tests/test_eventpackage.py`,
  `tests/test_launch.py`, `tests/test_selfcheck.py`, `tests/test_static.py`
  — plus the canonical second-remediation report + CURRENT-STATE +
  BACKLOG + the bounded ARCHITECTURE-SUMMARY paragraph).

All mandated documents were fetched and read at that exact SHA
(worktree pinned to the exact commit; tracked files byte-identical to
the `8f998209…` blobs): CURRENT-STATE, BACKLOG,
PROJECT-UPDATE-PROTOCOL, CONTROL-ROOM-RUNBOOK, the EBS
IMPLEMENTATION-READBACK, the EBS REMEDIATION-READBACK, the EBS
SECOND-REMEDIATION-REPORT, the governance design REVISION record, and
the relevant `bootstrap-supervisor` source.

Confirmed governing state at the candidate (as recorded by the
second-remediation publication): AUCDEV-023 = P1 / READY;
`EBS_IMPLEMENTATION = SECOND_REMEDIATION_CANDIDATE /
AWAITING_FRESH_CONTROL_ROOM_READBACK`;
`INDEPENDENT_HARNESS_AUDIT =
BLOCKED_PENDING_SECOND_EBS_REMEDIATION_AND_FRESH_CONTROL_ROOM_READBACK
_AND_EVENT_PREPARATION_AND_SEPARATE_EXECUTION_AUTHORITY`;
GATE_W_PRIME REQUIRED / UNPROVEN; REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION
UNPROVEN / EVENT_PREPARATION_GATE; EVENT_PACKAGE_PREPARATION
NOT_STARTED / NOT_AUTHORIZED; BOOTSTRAP_EVENT NOT_INSTANTIATED;
MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY 0;
INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED; qualification NONE;
installation NONE.

Read-only corroboration performed by THIS publication session (for
recording consistency; NOT an audit): the source anchors cited by the
disposition were each located in the candidate source exactly as the
disposition states — `verify_event_package` in `ebs/launch.py` reuses
`verify_package_identity` and then enforces the strict versioned
event-manifest contract (`EVENT_MANIFEST_KEYS`,
`EVENT_MANIFEST_SCHEMA = "AUCDEV-023-EVENT-PACKAGE-MANIFEST-V1"`,
`binding.py`) with `canonical_bytes(manifest["transport_binding"]) ==
canonical_bytes(binding_projection(binding))`;
`binding_projection` (`binding.py`) covers every PROJECTION_FIELDS
security dimension EXCEPT `event_package`; the Supervisor constructor
requires `event_package_root` (no default) and runs
`verify_live_package_identity` → store attempt+digest binding →
`verify_event_package` before any Supervisor capable of
`validate_gates()` exists; `verify_package_identity`'s files[] row
validation checks dict/exact keys/path-string/path-unique but
establishes NO exact type invariant for `row["bytes"]`, while the
later size comparison is `os.fstat(fd).st_size != row["bytes"]`
(Python numeric equality — `True == 1`, `1.0 == 1`), and
`ebs/binding.py` DOES enforce `isinstance(size, bool) or not
isinstance(size, int)` for gate-evidence sizes, establishing that the
strictness exists elsewhere but not on manifest file rows; the
focused test battery (`tests/test_eventpackage.py` and the full suite)
contains NO negative covering this type-confusion case; the
second-remediation diff does NOT touch `ebs/accounting.py`,
`ebs/statemachine.py`, `ebs/custody.py`, or `ebs/reportcustody.py`.
The second-remediation handoff archive was independently re-verified
read-only by THIS session with results identical to the Control
Room's §3 values (outer SHA-256, byte size, census, zero
unsafe/duplicate/symlink/hardlink/special members, exactly one
SHA256SUMS, 40/40 payload checksums PASS, all 40 payload regular
files covered, all 14 changed files matched by Git blob identity to
the live `8f998209…` bytes, zero obvious credential/private-key
pattern hits); its contents were NOT executed and nothing was
extracted into the repository.

Pre-existing unrelated working-tree state preserved unstaged throughout
(unchanged from prior session records): `smoke-fixture` /
`smoke-fixture-103` gitlink drift and untracked `aucdev019-evidence/`,
`aucdev023-ebs-evidence/`, `aucdev023-ebs-remediation-evidence/`,
`aucdev023-ebs-remediation-readback-evidence/`,
`aucdev023-ebs-second-remediation-evidence/`.

## 2. Control Room disposition (recorded verbatim)

```
AUCDEV_023_EBS_SECOND_REMEDIATION_READBACK =
PARTIALLY_ACCEPTED
/ NARROW_MANIFEST_ROW_TYPE_REMEDIATION_REQUIRED

Candidate:
8f998209ed401f7a22586f2cfdee4d89d440faf9

Candidate tree:
8b089aab5cca1c2c8ef18f458051546b287ee0ad

Implementation base:
a9bbdea7aeebfc475b7042410943f32fccbe5e83

Publication/archive identity:
ACCEPTED

Source/evidence identity:
ACCEPTED

AUCDEV023-CR-EBS-REM-001 =
CLOSED
/ ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209

AUCDEV023-CR-EBS-001 =
CLOSED
/ ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209

AUCDEV023-CR-EBS-002 =
CLOSED
/ RECONFIRMED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209

AUCDEV023-CR-EBS-003 =
CLOSED
/ RECONFIRMED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209

NEW BLOCKING FINDING:

AUCDEV023-CR-EBS-REM2-001 =
EVENT_PACKAGE_MANIFEST_FILE_ROW_TYPE_VALIDATION_INCOMPLETE
/ OPEN / BLOCKING

This is NOT:
- independent audit;
- qualification;
- installation;
- event readiness;
- execution authority;
- GATE-W′ PASS;
- real-client credential/tool-isolation PASS.

No closure transfers to a future changed SHA.
```

Publication/archive identity ACCEPTED; source/evidence identity
ACCEPTED; second-remediation semantics PARTIAL — CR-EBS-REM-001 and
the CR-EBS-001 remainder CLOSED and CR-EBS-002/-003 RECONFIRMED at
Control Room implementation-readback strength, all bound to the exact
SHA `8f998209…` (§§4–6), and ONE NEW blocking finding
AUCDEV023-CR-EBS-REM2-001 (§7).

## 3. Verified identity / handoff evidence (recorded exactly)

Exact result identity:

```
commit:
8f998209ed401f7a22586f2cfdee4d89d440faf9

tree:
8b089aab5cca1c2c8ef18f458051546b287ee0ad

sole parent:
a9bbdea7aeebfc475b7042410943f32fccbe5e83

compare:
one ahead / zero behind
exactly 14 changed paths
```

bootstrap-supervisor subtree:

```
f0cbe9473aaf397a1c9a4d299a70bbbdf27f0f9f
```

Protected trees unchanged:

```
qualification-harness =
5b8d5e5465923740470ff63ed9b8683f257a3787

skill =
c792933a862d9a5434681a88d183470dd8b15d2f
```

Handoff archive independently checked READ-ONLY:

```
outer SHA-256:
83a4e40c647721ed6141903875dcd1f79a45afb69157aecd4886024dc0e0293b

size:
579101 bytes

census:
47 members =
41 regular files +
6 directories

unsafe/traversal = 0
duplicates = 0
symlinks = 0
hardlinks = 0
special = 0

exactly one SHA256SUMS
40 payload entries
40/40 PASS
```

All 14 changed canonical/source files represented in the handoff
matched the exact live GitHub blobs at `8f998209…`.

No obvious credential/private-key pattern found.

Submitted deterministic evidence is accepted as VERIFIED SUBMITTED
EVIDENCE ONLY; the Control Room did NOT execute archive contents:

```
- full EBS battery: 223/223 PASS
- CR-EBS-REM-001 focused suite: 41/41 PASS
- CR-EBS-002 focused regressions: 21/21 PASS
- CR-EBS-003 focused regressions: 15/15 PASS
- qualification-harness regression: 221/221 PASS
- compileall exit 0
- git diff --check clean
- stdlib-only / forbidden-tree / credential scans recorded clean.
```

## 4. CR-EBS-REM-001 — ACCEPT CLOSURE AT CONTROL ROOM READBACK STRENGTH

Record that exact source inspection establishes:

1. Strict versioned event-package top-level contract:
   `AUCDEV-023-EVENT-PACKAGE-MANIFEST-V1`.

2. Binding independently pins:
   `event_package.manifest_sha256`
   `event_package.package_sha256`.

3. `verify_event_package` reuses `verify_package_identity` for:
   - raw manifest identity;
   - non-circular package identity;
   - per-file size/hash comparison;
   - payload-set equality;
   - missing/stale/unrecorded/symlink refusal.

4. `binding_projection` covers EVERY Binding TOP_LEVEL security
   dimension except `event_package` itself.

5. The `event_package` self-identity pair is intentionally excluded
   from the projection because it is independently pinned and verified
   against the actual package bytes, avoiding recursive self-hashing.

6. Event-package manifest `transport_binding` and Binding projection
   are compared as canonical JSON bytes.

7. Supervisor requires `event_package_root` and verifies, before a
   Supervisor capable of `validate_gates()` exists:
   - live EBS package identity;
   - store attempt+binding digest;
   - event-package identity;
   - event-package projection equality.

8. Internally valid Binding component substitution while retaining the
   same event-package identity is refused with
   `EVENT_PACKAGE_PROJECTION_MISMATCH`.

9. The reverse direction is also established: a regenerated
   self-consistent synthetic package with changed projection plus
   updated `event_package` pins remains refused when its projection
   differs from the Binding.

10. The real AUCDEV-023 event package was NOT prepared.

Therefore:

```
AUCDEV023-CR-EBS-REM-001 =
CLOSED / ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
```

And the remaining portion of:

```
AUCDEV023-CR-EBS-001 =
CLOSED / ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
```

on EXACT SHA `8f998209ed401f7a22586f2cfdee4d89d440faf9`.

These closures do NOT transfer to a future changed SHA.

## 5. CR-EBS-002 — RECONFIRM CLOSURE ON THE NEW SHA

Fresh source readback establishes the previously accepted one-shot
mechanics remain held:

- accounting authority attach/resume remains absent;
- O_EXCL duplicate-attempt refusal remains;
- historical accounting remains read-only;
- Supervisor/store attempt+digest binding remains;
- exact-object single-issuance LaunchGrant remains;
- irreversible spent guard remains;
- post-consumption failures cannot revive launch authority;
- best-effort durable terminalization remains.

The second-remediation diff does not modify `accounting.py`,
state-machine authority semantics, custody, or the execute/consume
one-shot mechanics except for required Supervisor
construction/event-package verification integration.

Disposition:

```
AUCDEV023-CR-EBS-002 =
CLOSED
/ RECONFIRMED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209
```

This reconfirmation does NOT transfer to a future changed SHA.

## 6. CR-EBS-003 — RECONFIRM CLOSURE ON THE NEW SHA

Fresh source readback establishes:

- mandatory live EBS self-verification remains;
- raw manifest identity remains binding-pinned;
- non-circular EBS package identity remains binding-pinned;
- exact live payload hash/size/set verification remains;
- changed source + regenerated manifest cannot pass unchanged frozen
  pins;
- no production bypass was introduced.

The shared strict JSON loader change is a strengthening of manifest
parsing.

Disposition:

```
AUCDEV023-CR-EBS-003 =
CLOSED
/ RECONFIRMED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209
```

This reconfirmation does NOT transfer to a future changed SHA.

## 7. NEW BLOCKING FINDING (recorded exactly)

```
Finding:
AUCDEV023-CR-EBS-REM2-001

Title:
EVENT_PACKAGE_MANIFEST_FILE_ROW_TYPE_VALIDATION_INCOMPLETE

Classification:
BOOTSTRAP_SUPERVISOR_IMPLEMENTATION_DEFECT
+
GOVERNANCE_CONTRACT_DEVIATION

Support:
OBSERVED_SOURCE_FACT
+
REQUIREMENT_CLAIM

Disposition:
OPEN / BLOCKING
```

Evidence (Control Room, recorded verbatim):

The authorized second-remediation contract required the versioned
event-package manifest to be STRICT and fail closed on wrong types.

Current `verify_package_identity` validates each files[] row with:

- row is dict;
- exact keys are path / bytes / sha256;
- path is string;
- path is unique.

It does NOT establish an exact type invariant for `row["bytes"]`.

The actual size check later is equivalent to:

```
os.fstat(fd).st_size != row["bytes"]
```

Python numeric equality is not type-strict:

```
True == 1
1.0 == 1
```

Therefore an otherwise self-consistent, correctly re-pinned frozen
package containing a one-byte regular payload can encode for that
row:

```
"bytes": true
```

or:

```
"bytes": 1.0
```

and the size comparison can accept the malformed type.

The current focused test battery has no negative covering this
type-confusion case.

This does NOT invalidate the newly established transport component
cross-binding itself; therefore CR-EBS-REM-001 may close.

It IS a fail-closed defect in the authority-critical frozen package
manifest contract and must be repaired before event-package
preparation proceeds.

Required future remediation strength (Control Room, recorded
verbatim):

- require files[].bytes to be an INTEGER;
- explicitly refuse bool;
- require bytes >= 0;
- preserve exact hash/size comparison;
- add deterministic negatives at minimum for:
  * bytes=true on a one-byte payload;
  * bytes=false on a zero-byte payload if a zero-byte synthetic case
    is used;
  * bytes=1.0 on a one-byte payload;
  * bytes as string;
  * negative bytes;
- prove all malformed rows are refused BEFORE GATES_PASSED;
- preserve all current cross-binding, one-shot and self-identity
  invariants;
- no real event package;
- no provider/model/credential work.

Prefer the smallest possible source change.

Do NOT broaden this finding into a redesign.

## 8. TCB LOC disposition

Observed production physical LOC:

```
1571 -> 1664 (+93)
```

Control Room disposition:

```
ACCEPTED_RESIDUAL_AT_CURRENT_IMPLEMENTATION_READBACK_STRENGTH
/ NONBLOCKING
```

Rationale (Control Room, recorded verbatim):

- the growth directly implements the required event-package
  cross-binding;
- the existing package verifier was reused rather than duplicated;
- one structural projection equality avoids a larger per-field
  verifier;
- no third-party runtime dependency was introduced;
- no plugin/daemon/network-service surface was added;
- source remains line-by-line reviewable.

This acceptance is bound to the exact current candidate.

1664 is NOT standing authority for further TCB growth.

The future narrow REM2-001 fix SHOULD stay at or below 1664 physical
production LOC where reasonably possible by using the smallest type
check/refactor.

Any growth beyond 1664 must again be disclosed and separately
accepted.

## 9. Resulting state (recorded verbatim)

```
AUCDEV-023 =
P1 / READY / NOT DONE

EBS_IMPLEMENTATION =
CONTROL_ROOM_SECOND_REMEDIATION_READBACK_PARTIAL
/ NARROW_MANIFEST_ROW_TYPE_REMEDIATION_REQUIRED

AUCDEV023-CR-EBS-001 =
CLOSED
/ ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209

AUCDEV023-CR-EBS-002 =
CLOSED
/ RECONFIRMED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209

AUCDEV023-CR-EBS-003 =
CLOSED
/ RECONFIRMED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209

AUCDEV023-CR-EBS-REM-001 =
CLOSED
/ ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
/ EXACT_SHA_8F998209

AUCDEV023-CR-EBS-REM2-001 =
OPEN / BLOCKING

INDEPENDENT_HARNESS_AUDIT =
BLOCKED_PENDING_NARROW_EBS_MANIFEST_TYPE_REMEDIATION
_AND_FRESH_CONTROL_ROOM_READBACK
_AND_EVENT_PREPARATION
_AND_SEPARATE_EXECUTION_AUTHORITY
```

Preserve exactly:

```
GATE_W_PRIME =
REQUIRED / UNPROVEN

REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION =
UNPROVEN / EVENT_PREPARATION_GATE

EVENT_PACKAGE_PREPARATION =
NOT_STARTED / NOT_AUTHORIZED

BOOTSTRAP_EVENT =
NOT_INSTANTIATED

MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY =
0

INDEPENDENT_AUDITOR_PROVENANCE_GATE =
NOT_SATISFIED

qualification =
NONE

installation =
NONE
```

No acceptance transfers automatically to any future changed SHA.

## 10. Record-only publication scope (OBSERVED_FACT)

This publication creates EXACTLY ONE new canonical readback record
(THIS file) and updates only CURRENT-STATE and BACKLOG (bounded
current-facing fields + dated records), plus ONLY the bounded factual
AUCDEV-023 implementation-status paragraph in ARCHITECTURE-SUMMARY
(because it stated the second-remediation candidate was awaiting its
fresh Control Room readback; the adopted R1 architecture/policy
semantics are NOT altered). NOT modified:
`bootstrap-supervisor/**` (byte-unchanged from
`8f998209ed401f7a22586f2cfdee4d89d440faf9`), `qualification-harness/**`,
`skill/**`, `AUCDEV-QUALIFICATION-HISTORY.md`,
`AUCDEV-CONTROL-ROOM-RUNBOOK.md`,
`AUCDEV-PROJECT-UPDATE-PROTOCOL.md`, any prior EBS
implementation/remediation report or readback, the governance
adoption/design/revision/readback records, Project Instructions,
historical AUCDEV-010 records, and the frozen `d4d584ff…` target.

This publication is governance/record-only. No implementation source
was modified, no REM2-001 remediation was written, no event package
was prepared, and no provider, model, auditor, or `/audit-council`
execution occurred.

## 11. Next action (EXACTLY ONE)

```
OPERATOR DECISION ON AUTHORIZING NARROW BOUNDED AUCDEV-023 EBS
REMEDIATION FOR AUCDEV023-CR-EBS-REM2-001
```

That remediation is NOT implemented in this task. Authorization is
NOT inferred. The event package is NOT prepared. This record grants
no execution authority of any kind.

---

Disposition (permitted publication wording only; NOT a Control Room
acceptance of its own publication):

```
AUCDEV_023_EBS_SECOND_REMEDIATION_READBACK_PUBLICATION =
PARTIALLY_ACCEPTED
/ NARROW_MANIFEST_ROW_TYPE_REMEDIATION_REQUIRED
/ RECORDED
```
