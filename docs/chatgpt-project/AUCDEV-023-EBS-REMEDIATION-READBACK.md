# AUCDEV-023 — EBS Remediation: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION SESSION ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room decision-maker (this session publishes the Control Room's already-decided readback disposition verbatim), NOT an auditor, NOT authorized to modify bootstrap-supervisor implementation source, NOT authorized to perform the second remediation, NOT authorized to prepare an event package, NOT authorized to invoke any provider/model/auditor, `/audit-council`, real credential, bootstrap event, qualification process, or installation; ZERO provider/model/frontier calls |
| Date | 2026-09-19 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-19) authorizes ONLY this record-only/append-only publication of the Control Room readback disposition of the AUCDEV-023 bounded EBS remediation candidate. It does NOT authorize implementation-source modification, a second remediation, event-package preparation, auditor/model/provider execution, qualification, installation, or any bootstrap event step. The disposition below was already decided by the Control Room; it is recorded faithfully — not reinterpreted, weakened, strengthened, merged, closed, or invented. |
| Candidate under readback | `7911f0576bec23cf4638665a667b160e61dd90a9` (tree `b0abc77337707dec1a1ec5266348367d17e86147`; sole parent / remediation base `bfe4b0fc5a2bc0c6371ed4f6df80820d4b6feed0`; bootstrap-supervisor subtree `753e9bc18e4cf297b43408d1877e77f6539de7cf`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this publication session's bootstrap |
| Subject | The AUCDEV-023 bounded EBS remediation publication (commit `7911f057…`, canonical record `AUCDEV-023-EBS-REMEDIATION-REPORT.md`, the remediated `bootstrap-supervisor/**` candidate for AUCDEV023-CR-EBS-001/-002/-003), its handoff archive identity/integrity, its submitted deterministic test evidence, the disposition of the three prior blocking findings, and the ONE NEW blocking finding AUCDEV023-CR-EBS-REM-001 recorded by this readback |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **BLOCKED_PENDING_SECOND_EBS_REMEDIATION_AND_FRESH_CONTROL_ROOM_READBACK_AND_EVENT_PREPARATION_AND_SEPARATE_EXECUTION_AUTHORITY** — the readback's PARTIAL disposition keeps the independent harness audit blocked; no auditor has reviewed `d4d584ff…` |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `OBSERVED_SOURCE_FACT` / `REQUIREMENT_CLAIM`
(Control Room finding support classes, recorded verbatim from the
disposition), `REQUIREMENT` (record-mandated property). §§2–9 are the
CONTROL ROOM's disposition recorded EXACTLY; this publication session
neither adjudicates nor amends it.

---

## 1. Live bootstrap and candidate identity (OBSERVED_FACT)

Live `refs/heads/master` of `isakli05/audit-council-dev` was resolved at
this session's bootstrap and required to equal EXACTLY the mandated
remediation candidate `7911f0576bec23cf4638665a667b160e61dd90a9`; it did,
so no STOP-WITHOUT-MUTATION was required:

- candidate commit `7911f0576bec23cf4638665a667b160e61dd90a9`;
- tree `b0abc77337707dec1a1ec5266348367d17e86147`;
- sole parent `bfe4b0fc5a2bc0c6371ed4f6df80820d4b6feed0`
  (single-parent confirmed via `git cat-file -p`);
- `bootstrap-supervisor` subtree
  `753e9bc18e4cf297b43408d1877e77f6539de7cf`;
- qualification-harness tree
  `5b8d5e5465923740470ff63ed9b8683f257a3787` — EQUAL to the frozen
  audit target `d4d584ffa47ad2848268ba947247f81a845b2322` (unchanged);
- skill tree `c792933a862d9a5434681a88d183470dd8b15d2f` — EQUAL to the
  frozen audit target (unchanged);
- exact compare base..candidate: **one commit ahead / zero behind**;
  changed paths EXACTLY **17** (13 `bootstrap-supervisor/**` files + the
  canonical remediation report + CURRENT-STATE + BACKLOG +
  ARCHITECTURE-SUMMARY).

All mandated documents were fetched and read at that exact SHA
(`git show` at `7911f057…`): CURRENT-STATE, BACKLOG,
PROJECT-UPDATE-PROTOCOL, CONTROL-ROOM-RUNBOOK, the EBS
IMPLEMENTATION-READBACK, the EBS REMEDIATION-REPORT, the governance
ADOPTION record, the design REVISION record, the design-revision
READBACK record, and the relevant `bootstrap-supervisor` source.

Confirmed governing state at the candidate (as recorded by the
remediation publication): AUCDEV-023 = P1 / READY;
`EBS_IMPLEMENTATION = REMEDIATED_CANDIDATE /
AWAITING_FRESH_CONTROL_ROOM_READBACK`;
`INDEPENDENT_HARNESS_AUDIT = BLOCKED_PENDING_FRESH_EBS_REMEDIATION_READBACK
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
disposition states — `RESUMABLE_STATES` ABSENT from `ebs/**`;
`AccountingStore.attach` ABSENT from `ebs/**`; read-only
`inspect_accounting_record` present in `ebs/accounting.py`;
`verify_package_identity` / `verify_live_package_identity` present in
`ebs/launch.py`; and `event_package` used in production `ebs/**` ONLY in
`ebs/binding.py` (validated digest fields), `ebs/cli.py` (displayed
metadata), and `ebs/launch.py` (durable accounting facts) — with NO
production path that opens or verifies a frozen event-package manifest.
The remediation handoff archive was independently re-verified read-only
by THIS session with results identical to the Control Room's §3 values
(outer SHA-256, byte size, census, zero unsafe/duplicate/symlink/
hardlink/special members, exactly one SHA256SUMS); its contents were NOT
executed and nothing was extracted into the repository.

Pre-existing unrelated working-tree state preserved unstaged throughout
(unchanged from prior session records): `smoke-fixture` /
`smoke-fixture-103` gitlink drift and untracked `aucdev019-evidence/`,
`aucdev023-ebs-evidence/`, `aucdev023-ebs-remediation-evidence/`.

## 2. Control Room disposition (recorded verbatim)

```
AUCDEV_023_EBS_REMEDIATION_READBACK =
PARTIALLY_ACCEPTED / SECOND_BOUNDED_REMEDIATION_REQUIRED

Remediation candidate:
7911f0576bec23cf4638665a667b160e61dd90a9

Candidate tree:
b0abc77337707dec1a1ec5266348367d17e86147

Remediation base:
bfe4b0fc5a2bc0c6371ed4f6df80820d4b6feed0

Publication/archive identity:
ACCEPTED

Source/evidence identity:
ACCEPTED

AUCDEV023-CR-EBS-001 =
PARTIALLY_REMEDIATED / OPEN_BLOCKING

AUCDEV023-CR-EBS-002 =
CLOSED / ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH

AUCDEV023-CR-EBS-003 =
CLOSED / ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH

NEW BLOCKING FINDING:

AUCDEV023-CR-EBS-REM-001 =
EVENT_PACKAGE_COMPONENT_CROSS_BINDING_NOT_ESTABLISHED
/ OPEN / BLOCKING

This is NOT:
- an independent audit;
- qualification;
- installation;
- event readiness;
- execution authority;
- GATE-W′ PASS;
- real-client credential/tool-isolation PASS.
```

Publication/archive identity ACCEPTED; source/evidence identity
ACCEPTED; remediation semantics PARTIAL — CR-EBS-002 and CR-EBS-003
CLOSED at Control Room implementation-readback strength (§§4–5),
CR-EBS-001 PARTIALLY remediated and still OPEN/BLOCKING (§6), and ONE
NEW blocking finding AUCDEV023-CR-EBS-REM-001 (§7).

## 3. Verified remediation handoff evidence (recorded exactly)

Exact result identity:

```
7911f0576bec23cf4638665a667b160e61dd90a9
tree b0abc77337707dec1a1ec5266348367d17e86147
sole parent bfe4b0fc5a2bc0c6371ed4f6df80820d4b6feed0
```

bootstrap-supervisor subtree:

```
753e9bc18e4cf297b43408d1877e77f6539de7cf
```

GitHub compare: one commit ahead / zero behind, exactly 17 changed
paths.

Protected trees unchanged:

```
qualification-harness =
5b8d5e5465923740470ff63ed9b8683f257a3787

skill =
c792933a862d9a5434681a88d183470dd8b15d2f
```

Handoff archive independently checked read-only:

```
outer SHA-256:
9a78d5a0502a828340f197a8e947e35279c6493dc5f1340f638687a3d4f7f134

size:
579079 bytes

census:
53 entries =
45 regular files +
8 directories

unsafe/traversal = 0
duplicates = 0
symlinks = 0
hardlinks = 0
special = 0

exactly one SHA256SUMS
44 checksum entries
44/44 PASS
```

All 17 changed publication files contained in the handoff were
independently matched by Git blob identity to the live GitHub bytes at
`7911f057…`.

Submitted deterministic evidence records:

```
EBS full battery:
182/182 PASS

focused remediation:
60/60 PASS

qualification-harness regression:
221/221 PASS
```

These are VERIFIED SUBMITTED EVIDENCE ONLY. Control Room did NOT
execute archive contents.

Manifest evidence independently re-derived:

```
raw MANIFEST SHA-256 =
787dc78071b7278e36b7cbd3825538a614e098d4ef81bd8e47f369c086d3db78

non-circular package SHA-256 =
22ebcbd14b00b0185cb9a0c79e971bdcd9f95201fe6acf89c885ba6371496219
```

recorded and independently derived package identity MATCH.

No obvious credential/private-key pattern was found in the handoff.

## 4. CR-EBS-002 — ACCEPT CLOSURE AT CONTROL ROOM READBACK STRENGTH

Record that source inspection mechanically establishes:

- RESUMABLE_STATES removed;
- AccountingStore.attach removed;
- no authority revival path from historical accounting;
- existing attempt creation fails via O_EXCL;
- historical inspection is separated into read-only
  inspect_accounting_record returning data, not authority;
- Supervisor requires exact store.attempt_id == binding.attempt_id;
- Supervisor requires exact store.binding_digest == binding.digest;
- LaunchGrant carries no bearer state;
- execute accepts only the exact grant object issued by that Supervisor;
- consume is single-issuance;
- irreversible _spent guard is set before held-fd rehash/fork;
- post-consumption/pre-exec failures terminalize best-effort;
- even terminal-accounting failure cannot restore in-process launch
  authority.

Disposition:

```
AUCDEV023-CR-EBS-002 =
CLOSED / ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
```

This closure does not transfer to a different future SHA.

## 5. CR-EBS-003 — ACCEPT CLOSURE AT CONTROL ROOM READBACK STRENGTH

Record that source inspection mechanically establishes:

- mandatory runtime package self-verification in Supervisor startup;
- runs before gate passage and authority consumption;
- no production flag/env bypass;
- executing package root derived from launch.py __file__;
- raw live MANIFEST bytes checked against the binding-pinned manifest
  digest;
- package_sha256 recomputed using the documented non-circular
  construction;
- independently binding-pinned package identity compared;
- every manifest payload verified for exact size + SHA-256;
- missing/stale/unrecorded/symlink payload conditions fail closed;
- changed source + regenerated manifest cannot pass an unchanged frozen
  binding.

Disposition:

```
AUCDEV023-CR-EBS-003 =
CLOSED / ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH
```

This closure does not transfer to a different future SHA.

## 6. CR-EBS-001 — PARTIAL ONLY

Accept these remediation portions:

- missing transport dimensions are now mandatory fields;
- strict parsing remains fail closed;
- binding digest covers those fields;
- Supervisor/store attempt+digest consistency is enforced;
- CONSUMED_PRE_EXEC accounting records explicit non-secret
  security-critical identity facts rather than only an opaque digest.

DO NOT accept closure of CR-EBS-001.

Reason (Control Room, recorded verbatim):

The adopted architecture requires the EBS itself to verify the FROZEN
EVENT PACKAGE MANIFEST and every transport-binding field against it
before GATES_PASSED.

The remediation currently represents:

```
event_package = {
  manifest_sha256,
  package_sha256
}
```

but production EBS source provides no path that:

- opens the frozen event-package manifest;
- verifies its bytes against event_package.manifest_sha256;
- verifies its package identity against event_package.package_sha256;
- parses its component identity declarations;
- compares actual event-package declarations for:
  boundary launcher,
  sandbox/profile,
  tool-domain wrapper,
  auditor executable,
  adapter/provider role,
  prompt/evidence/target/output identities
  against the EBS Binding before GATES_PASSED.

Source-wide inspection establishes that event_package is used only as:

- validated digest fields in binding.py;
- displayed metadata in cli.py;
- durable accounting facts in launch.py.

No production event-package manifest validation/cross-binding mechanism
exists.

The synthetic binding builder further demonstrates the structural gap:
event-package hashes are generated independently of the synthetic
launcher, sandbox profile, tool wrapper, and auditor executable fields.

Therefore a NEW attempt can carry the same declared event-package
identity with different otherwise-valid component identities and still
pass Binding parsing. Changing Binding.digest does not close this
relationship for a new attempt/store.

Digest coverage proves:
"these fields belong to this binding document."

It does NOT prove:
"these fields are the components of the frozen event package identified
by event_package."

Disposition:

```
AUCDEV023-CR-EBS-001 =
PARTIALLY_REMEDIATED / OPEN_BLOCKING
```

## 7. NEW BLOCKING FINDING (recorded exactly)

```
Finding:
AUCDEV023-CR-EBS-REM-001

Title:
EVENT_PACKAGE_COMPONENT_CROSS_BINDING_NOT_ESTABLISHED

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

Required future remediation strength (Control Room, recorded
verbatim):

Implement a generic, fail-closed EBS mechanism that mechanically
verifies a frozen event-package manifest against the binding BEFORE
GATES_PASSED.

This future remediation may use ONLY synthetic/inert event-package
fixtures until separately authorized event-package preparation exists.

It must NOT prepare the real AUCDEV-023 event package.

At minimum, the mechanism must ensure that the frozen event-package
identity cryptographically binds and the EBS mechanically cross-checks
the declared:

- event id;
- role;
- attempt;
- target;
- prompt digest;
- common evidence digest;
- output identity;
- boundary launcher identity/hash;
- sandbox/profile identity;
- credential adapter/provider role;
- auditor executable identity/hash/version;
- tool-domain wrapper identity/hash;
- relevant gate/binding identities;
- EBS package identity where the adopted event-package contract includes
  it.

An arbitrary valid component substitution while retaining the same
declared event-package identity must fail closed.

Do NOT merely add another opaque digest field.
Do NOT treat Binding.digest itself as proof of event-package membership.

## 8. LOC residual

Production LOC independently supported by submitted evidence:

```
1357 -> 1571
```

Adopted design wording: target size bound <= approximately 1500 source
lines.

Control Room classification:

```
ACCEPTED_RESIDUAL_AT_CURRENT_IMPLEMENTATION_READBACK_STRENGTH
/ NONBLOCKING
```

Rationale (Control Room, recorded verbatim): 1571 is +71 lines /
approximately +4.7% over literal 1500; the adopted bound is explicitly
approximate, source remains line-by-line reviewable, and the added
security logic is directly attributable to the three remediation
findings.

This is NOT standing authority for further TCB growth. The current 1571
freeze may be recorded. Any future production LOC growth requires
explicit justification and review.

## 9. Resulting state (recorded verbatim)

```
AUCDEV-023 =
P1 / READY / NOT DONE

EBS_IMPLEMENTATION =
CONTROL_ROOM_REMEDIATION_READBACK_PARTIAL
/ SECOND_BOUNDED_REMEDIATION_REQUIRED

AUCDEV023-CR-EBS-001 =
PARTIALLY_REMEDIATED / OPEN_BLOCKING

AUCDEV023-CR-EBS-002 =
CLOSED / ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH

AUCDEV023-CR-EBS-003 =
CLOSED / ACCEPTED_AT_CONTROL_ROOM_IMPLEMENTATION_READBACK_STRENGTH

AUCDEV023-CR-EBS-REM-001 =
OPEN / BLOCKING

INDEPENDENT_HARNESS_AUDIT =
BLOCKED_PENDING_SECOND_EBS_REMEDIATION
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
(because it stated the remediation was awaiting its fresh Control Room
readback; the adopted R1 architecture/policy semantics are NOT altered).
Exactly four changed paths. NOT modified:
`bootstrap-supervisor/**` (byte-unchanged from
`7911f0576bec23cf4638665a667b160e61dd90a9`), `qualification-harness/**`,
`skill/**`, `AUCDEV-QUALIFICATION-HISTORY.md`,
`AUCDEV-CONTROL-ROOM-RUNBOOK.md`,
`AUCDEV-PROJECT-UPDATE-PROTOCOL.md`, the EBS implementation report, the
EBS implementation readback, the EBS remediation report, the governance
adoption/design/revision/readback records, Project Instructions,
historical AUCDEV-010 records, and the frozen `d4d584ff…` target.

This publication is governance/record-only. No implementation source
was modified, no second remediation was written, no event package was
prepared, and no provider, model, auditor, or `/audit-council` execution
occurred.

## 11. Next action (EXACTLY ONE)

```
OPERATOR DECISION ON AUTHORIZING SECOND BOUNDED AUCDEV-023 EBS
REMEDIATION FOR AUCDEV023-CR-EBS-REM-001
```

That remediation is NOT implemented in this task. It is NOT authorized
implicitly. The event package is NOT prepared. This record grants no
execution authority of any kind.

---

Disposition (permitted publication wording only; NOT a Control Room
acceptance of its own publication):

```
AUCDEV_023_EBS_REMEDIATION_READBACK_PUBLICATION =
PARTIALLY_ACCEPTED
/ SECOND_BOUNDED_REMEDIATION_REQUIRED
/ RECORDED
```
