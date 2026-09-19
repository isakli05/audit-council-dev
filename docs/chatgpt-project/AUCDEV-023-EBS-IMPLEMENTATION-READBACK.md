# AUCDEV-023 — EBS Implementation: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION SESSION ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room decision-maker (this session publishes the Control Room's already-reached readback disposition verbatim), NOT a qualification authority, NOT an installation authority, NOT authorized to remediate implementation source, NOT authorized to prepare an event package; NO provider/model/auditor execution, NO `/audit-council`, NO real credential, NO bootstrap event, NO qualification process, NO installation; ZERO provider/model/frontier calls |
| Date | 2026-09-19 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-19) authorizes ONLY this record-only/append-only publication of the Control Room readback disposition of the AUCDEV-023 bounded EBS implementation candidate. It does NOT authorize implementation source remediation, event-package preparation, auditor/model/provider execution, qualification, installation, or any bootstrap event step. The disposition below was already decided by the Control Room; it is recorded faithfully — not reinterpreted, weakened, strengthened, merged, closed, or invented. |
| Candidate under readback | `e2f8986057368f5b13e73fa349db7b288f670c62` (tree `b3ae0526aa2efb389e22a8ef6f7b4810613dd5f8`; sole parent / implementation base `f47c6d24f154d73881768c9039646763ea36f12a`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this publication session's bootstrap |
| Subject | The AUCDEV-023 bounded EBS implementation publication (commit `e2f8986…`, canonical record `AUCDEV-023-EBS-IMPLEMENTATION-REPORT.md`, the `bootstrap-supervisor/**` minimal-TCB candidate), its handoff archive identity/integrity, its submitted deterministic test evidence, and the THREE NEW blocking findings AUCDEV023-CR-EBS-001/-002/-003 recorded by this readback |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **BLOCKED_PENDING_EBS_REMEDIATION_AND_FRESH_CONTROL_ROOM_READBACK_AND_EVENT_PREPARATION_AND_SEPARATE_EXECUTION_AUTHORITY** — the readback's PARTIAL disposition keeps the independent harness audit blocked; no auditor has reviewed `d4d584ff…` |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `OBSERVED_SOURCE_FACT` / `INFERENCE` /
`REQUIREMENT_CLAIM` (Control Room finding support classes, recorded
verbatim from the disposition), `REQUIREMENT` (record-mandated
property). Findings §§4–6 are the CONTROL ROOM's findings recorded
EXACTLY; this publication session neither adjudicates nor amends them.

---

## 1. Live bootstrap and candidate identity (OBSERVED_FACT)

Live `refs/heads/master` of `isakli05/audit-council-dev` was resolved at
this session's bootstrap and required to equal EXACTLY the mandated
candidate; it did, so no stop was required:

- candidate commit `e2f8986057368f5b13e73fa349db7b288f670c62`;
- tree `b3ae0526aa2efb389e22a8ef6f7b4810613dd5f8`;
- sole parent `f47c6d24f154d73881768c9039646763ea36f12a`
  (single-parent confirmed via `git cat-file -p`);
- `bootstrap-supervisor` subtree
  `77a617a8ed7a8fbe25db5c84be959fbf48070c7a`;
- qualification-harness tree
  `5b8d5e5465923740470ff63ed9b8683f257a3787` — EQUAL to the frozen
  audit target `d4d584ffa47ad2848268ba947247f81a845b2322` (unchanged);
- skill tree `c792933a862d9a5434681a88d183470dd8b15d2f` — EQUAL to the
  frozen audit target (unchanged);
- exact compare base..candidate: **one commit ahead / zero behind**;
  changed paths EXACTLY **24** (20 `bootstrap-supervisor/**` files + the
  canonical implementation report + CURRENT-STATE + BACKLOG +
  ARCHITECTURE-SUMMARY).

All mandated documents were fetched and read at that exact SHA
(`git show` at `e2f8986`): CURRENT-STATE, BACKLOG,
PROJECT-UPDATE-PROTOCOL, CONTROL-ROOM-RUNBOOK, the governance ADOPTION
record, the design REVISION record, the design-revision READBACK
record, and the EBS IMPLEMENTATION-REPORT.

Confirmed governing state at the candidate (as recorded by the
implementation publication): AUCDEV-023 = P1 / READY;
`EBS_IMPLEMENTATION = IMPLEMENTED_CANDIDATE /
AWAITING_CONTROL_ROOM_READBACK`;
`INDEPENDENT_HARNESS_AUDIT = BLOCKED_PENDING_EBS_IMPLEMENTATION_READBACK
_AND_EVENT_PREPARATION_AND_SEPARATE_EXECUTION_AUTHORITY`;
GATE_W_PRIME REQUIRED / UNPROVEN; REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION
UNPROVEN / EVENT_PREPARATION_GATE; EVENT_PACKAGE_PREPARATION
NOT_STARTED / NOT_AUTHORIZED; BOOTSTRAP_EVENT NOT_INSTANTIATED;
MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY 0;
INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED; qualification NONE;
installation NONE.

Read-only corroboration performed by THIS publication session (for
recording consistency; NOT an audit): production physical LOC
recomputed `wc -l bootstrap-supervisor/ebs/*.py` = **1357** (identical
to the Control Room's independent recomputation); production
import/source inspection found Python stdlib + package-relative
modules only, with no runtime import/reach into qualification-harness,
`qh`, `skill`, or any installed Audit Council; the source anchors cited
by finding AUCDEV023-CR-EBS-002 (`RESUMABLE_STATES` in
`ebs/accounting.py`, `Supervisor.attach` in `ebs/launch.py`,
`test_attach_restart_ok_before_consumption` in
`tests/test_accounting.py`, directly constructible `LaunchGrant`) were
each located in the candidate source exactly as the finding states.

Pre-existing unrelated working-tree state preserved unstaged throughout
(unchanged from prior session records): `smoke-fixture` /
`smoke-fixture-103` gitlink drift and untracked `aucdev019-evidence/`,
`aucdev023-ebs-evidence/`.

## 2. Control Room disposition (recorded verbatim)

```
AUCDEV_023_EBS_IMPLEMENTATION_READBACK =
PARTIALLY_ACCEPTED / REMEDIATION_REQUIRED

Target candidate:
e2f8986057368f5b13e73fa349db7b288f670c62

Candidate tree:
b3ae0526aa2efb389e22a8ef6f7b4810613dd5f8

Implementation base:
f47c6d24f154d73881768c9039646763ea36f12a

Publication/archive identity and integrity:
ACCEPTED.

Source/evidence identity:
ACCEPTED.

Implementation semantics:
PARTIAL — THREE BLOCKING FINDINGS REQUIRE REMEDIATION.

This is NOT:
- independent audit;
- qualification;
- installation;
- event readiness;
- execution authority;
- GATE-W′ PASS;
- real-client credential/tool-isolation PASS.
```

Publication/archive identity and integrity ACCEPTED; source/evidence
identity ACCEPTED; implementation semantics PARTIAL. The three blocking
findings follow in §§4–6.

## 3. Verified positive evidence (Control Room readback strength)

Recorded as Control Room-verified readback evidence. Archive-content
facts were verified read-only by the Control Room and are NOT
re-executed or re-derived by this publication session; the identity
facts in the first four bullets were also independently observed by
this session at bootstrap (§1).

- Live GitHub candidate identity matched:
  commit `e2f8986057368f5b13e73fa349db7b288f670c62`
  tree `b3ae0526aa2efb389e22a8ef6f7b4810613dd5f8`
  sole parent `f47c6d24f154d73881768c9039646763ea36f12a`
  bootstrap-supervisor subtree
  `77a617a8ed7a8fbe25db5c84be959fbf48070c7a`.

- Exact compare base..candidate: one commit ahead / zero behind;
  exactly 24 changed paths.

- qualification-harness tree unchanged:
  `5b8d5e5465923740470ff63ed9b8683f257a3787`.

- skill tree unchanged:
  `c792933a862d9a5434681a88d183470dd8b15d2f`.

- Handoff archive independently checked read-only:
  outer SHA-256:
  `354e77be966107af87ba4d013aa28f3b55c0e2f43d29a6bdb7834bcc9da34e9a`

  size: 573017 bytes

  census: 52 entries = 46 regular files + 6 directories

  unsafe/traversal names = 0; duplicate member names = 0; symlinks = 0;
  hardlinks = 0; special files = 0

  exactly one SHA256SUMS; 45 payload checksum entries; 45/45 PASS.

- All 20 `bootstrap-supervisor/**` publication files and the four
  canonical changed docs included in the archive matched the exact
  GitHub blobs at `e2f8986057368f5b13e73fa349db7b288f670c62`.

- MANIFEST.json: 19 payload entries; 19/19 archived payload SHA-256 and
  byte-size values independently matched.

- Production physical LOC independently recomputed: 1357.

- Production import/source inspection: Python stdlib +
  package-relative modules only; no runtime import/reach into
  qualification-harness, `qh`, `skill`, or installed Audit Council was
  found.

- Submitted deterministic logs record: EBS tests 133/133 PASS; qh
  regression 221/221 PASS.
  IMPORTANT: the Control Room did NOT execute archive contents, so
  these stand as verified submitted evidence/log artifacts, NOT as a
  fresh Control Room test run.

- No contradictory evidence of provider/model/auditor execution was
  found. The zero-provider statement is accepted only at its recorded
  evidence strength: static source boundary + inert fixture execution
  evidence, not an absolute proof of all host networking history.

## 4. Blocking finding AUCDEV023-CR-EBS-001 (recorded exactly)

```
Finding:
AUCDEV023-CR-EBS-001

Title:
MANDATORY_TRANSPORT_BINDING_INCOMPLETE

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

Evidence and rationale (Control Room, recorded verbatim):

The adopted design revision requires the frozen event package AND the
EBS binding document to bind and the EBS to verify before GATES_PASSED,
including:

- event id;
- auditor role;
- attempt id;
- auditor executable SHA-256/version;
- provider role;
- frozen prompt digest;
- common evidence manifest digest;
- frozen target identity;
- output identity;
- boundary launcher identity/SHA-256;
- sandbox/profile identity;
- credential adapter identity;
- GATE-W′ evidence;
- EBS package identity (SHA-256 + manifest);
- tool-domain wrapper identity (SHA-256).

Current `bootstrap-supervisor/ebs/binding.py` does not carry or verify
several mandatory fields, including at minimum:

- auditor executable SHA-256/version;
- sandbox/profile identity;
- EBS package identity;
- tool-domain wrapper identity;
- complete frozen event-package identity/manifest binding.

Therefore the current EBS cannot mechanically verify those adopted
mandatory binding dimensions before GATES_PASSED.

The current accounting record also persists primarily `binding_digest`
rather than the adopted §10 full binding identity set, so the durable
accounting evidence does not itself carry the complete required binding
facts.

Required remediation strength (Control Room, recorded verbatim):

mechanically add and enforce the missing mandatory binding dimensions,
using synthetic-only fixtures/tests until event-package preparation is
separately authorized. Do NOT prepare a real event package in the
remediation task.

## 5. Blocking finding AUCDEV023-CR-EBS-002 (recorded exactly)

```
Finding:
AUCDEV023-CR-EBS-002

Title:
PROCESS_BOUND_ONE_SHOT_NOT_STRUCTURALLY_CLOSED

Classification:
BOOTSTRAP_SUPERVISOR_IMPLEMENTATION_DEFECT
+
GOVERNANCE_CONTRACT_DEVIATION

Support:
OBSERVED_SOURCE_FACT
+
INFERENCE
+
REQUIREMENT_CLAIM

Disposition:
OPEN / BLOCKING
```

Evidence and rationale (Control Room, recorded verbatim):

The adopted P1 design says:
- authority exists as non-exportable state of ONE EBS process;
- re-running the EBS for the same attempt id is refused at start;
- accounting is durable evidence / duplicate refusal, NOT the
  authority;
- after CONSUMED_PRE_EXEC there is no retry/revival;
- a replacement requires NEW explicit operator authority + NEW attempt
  id + NEW EBS process/state + NEW accounting/output identity.

Current implementation violates that structural requirement in
multiple ways:

A. `accounting.py` defines:
   `RESUMABLE_STATES = (PREPARED, GATES_PASSED)`

   `AccountingStore.attach()` accepts an existing same-attempt record
   in those states.

   `test_accounting.py` explicitly treats:
   `test_attach_restart_ok_before_consumption`
   as valid behavior.

   `launch.py` `Supervisor.attach()` reconstructs a Supervisor from
   that durable record.

   This revives same-attempt authority in a new process before
   consumption and makes durable accounting state an
   authority-continuation input, contrary to the adopted
   process-bound/no-revival design.

B. `Supervisor.__init__(binding, store)` checks only that store is an
   AccountingStore. It does NOT mechanically require:
   `store attempt id == binding.attempt_id` AND
   `store binding digest == binding.digest`.

   `AccountingStore.create()` independently accepts an arbitrary safe
   attempt name. Therefore the same Binding can be paired with a
   differently named fresh store, defeating the intended
   binding-to-record-set duplicate-attempt refusal.

C. `execute()` marks a LaunchGrant dead before the post-consumption
   re-hash/fork path. If that path fails before EXEC_ATTEMPTED,
   Supervisor state can remain CONSUMED_PRE_EXEC. LaunchGrant is
   directly constructible, so a fresh `LaunchGrant(supervisor)` can be
   created and `execute()` retried while state remains
   CONSUMED_PRE_EXEC.

   The current tests cover forged grants after a successful
   EXEC_ATTEMPTED transition, but do not close the
   post-consumption/pre-exec-failure retry path.

Required remediation strength (Control Room, recorded verbatim):

make the same-attempt authority irreversibly
single-process/single-use; remove authority continuation from
accounting attach; mechanically bind Supervisor/store attempt+digest to
the Binding; and terminalize/refuse every post-consumption failure path
so no replacement grant/execute call can revive the consumed authority.

## 6. Blocking finding AUCDEV023-CR-EBS-003 (recorded exactly)

```
Finding:
AUCDEV023-CR-EBS-003

Title:
RUNTIME_SELF_IDENTITY_VERIFICATION_ABSENT

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

Evidence and rationale (Control Room, recorded verbatim):

The adopted governance design §6.2 requires:

- exact EBS source/package bytes frozen;
- exact per-file manifest;
- EBS refuses to run when its own live bytes do not match the recorded
  manifest;
- runtime self-verification occurs at EBS start.

The candidate implements:
- publication-time MANIFEST.json;
- static manifest drift test.

It does NOT implement the required runtime EBS self-verification.
The implementation report explicitly records this deviation and defers
it to event-package preparation.

Control Room disposition: this deferral is NOT accepted as an
implementation residual.

Reason (Control Room, recorded verbatim):

the requirement is an EBS behavior. An external event-package verifier
is not equivalent to "the EBS refuses to run if its own live bytes do
not match its recorded manifest." Adding this behavior later would
change EBS source bytes, creating a new implementation candidate that
requires fresh Control Room readback anyway.

Required remediation strength (Control Room, recorded verbatim):

add fail-closed runtime self-identity verification before
authority/gates are reachable. The recorded EBS package/manifest
identity must itself be bound by the mandatory binding so a modified
live MANIFEST cannot simply bless modified live EBS bytes.

## 7. Accepted / held implementation areas (no additional blocking finding)

No additional blocking Control Room finding was established in this
readback for these inspected areas:

- target independence from frozen qh/skill runtime;
- exact frozen target constants;
- controllerless/inspection-only CLI boundary;
- fd-based verify-to-exec launcher identity;
- O_NOFOLLOW / regular-file checks and held-fd rehash;
- non-dumpable credential ingestion ordering;
- pipe / fully sealed memfd source discipline;
- four-seal EBS custody;
- fixed credential-fd inheritance and fd cleanup design;
- missing-report-stays-missing;
- contaminated report not frozen/published as conforming;
- 0444 clean-report freeze;
- absorbing terminal states;
- minimal-TCB physical LOC at 1357;
- stdlib-only production dependency surface;
- frozen qualification-harness and skill tree preservation;
- no event-package/source creep found in this publication.

These are CONTROL ROOM implementation-readback observations only. They
are NOT an independent audit verdict and MUST NOT be labeled qualified,
audited, production-ready, or execution-ready.

## 8. Held state preserved EXACTLY (recorded verbatim)

```
GATE_W_PRIME                             = REQUIRED / UNPROVEN
REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION    = UNPROVEN / EVENT_PREPARATION_GATE
EVENT_PACKAGE_PREPARATION                = NOT_STARTED / NOT_AUTHORIZED
BOOTSTRAP_EVENT                          = NOT_INSTANTIATED
MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY = 0
INDEPENDENT_AUDITOR_PROVENANCE_GATE      = NOT_SATISFIED
qualification                            = NONE
installation                             = NONE
```

No acceptance transfers to any future changed SHA. A remediated
candidate is a NEW implementation candidate requiring a FRESH Control
Room readback.

## 9. State after this publication (recorded verbatim)

```
AUCDEV-023                   = P1 / READY / NOT DONE

EBS_IMPLEMENTATION           = CONTROL_ROOM_READBACK_PARTIAL
                              / REMEDIATION_REQUIRED

Candidate under this readback =
e2f8986057368f5b13e73fa349db7b288f670c62

Blocking findings            = AUCDEV023-CR-EBS-001 OPEN
                               AUCDEV023-CR-EBS-002 OPEN
                               AUCDEV023-CR-EBS-003 OPEN

INDEPENDENT_HARNESS_AUDIT    =
BLOCKED_PENDING_EBS_REMEDIATION
_AND_FRESH_CONTROL_ROOM_READBACK
_AND_EVENT_PREPARATION
_AND_SEPARATE_EXECUTION_AUTHORITY
```

## 10. Record-only publication scope (OBSERVED_FACT)

This publication creates EXACTLY ONE new canonical readback record
(THIS file) and updates only CURRENT-STATE and BACKLOG (bounded
current-facing fields + dated records). NOT modified:
`bootstrap-supervisor/**` (byte-unchanged from
`e2f8986057368f5b13e73fa349db7b288f670c62`), `qualification-harness/**`,
`skill/**`, `AUCDEV-ARCHITECTURE-SUMMARY.md` (architecture NOT changed
by this record-only publication),
`AUCDEV-CONTROL-ROOM-RUNBOOK.md`,
`AUCDEV-PROJECT-UPDATE-PROTOCOL.md`,
`AUCDEV-QUALIFICATION-HISTORY.md`, the governance
adoption/design/design-revision/readback records, Project Instructions,
historical AUCDEV-010 records, and the frozen `d4d584ff…` target.

No implementation source remediation was authorized or performed in
this task. No event package was prepared. No provider, model, auditor,
or `/audit-council` execution occurred.

## 11. Next action (EXACTLY ONE)

```
OPERATOR DECISION ON AUTHORIZING BOUNDED AUCDEV-023 EBS REMEDIATION
FOR AUCDEV023-CR-EBS-001 / -002 / -003
```

The remediation implementation is NOT written in this task. It is NOT
authorized implicitly. The event package is NOT prepared. This record
grants no execution authority of any kind.

---

Disposition (permitted publication wording only; NOT a Control Room
acceptance of its own publication):

```
AUCDEV_023_EBS_IMPLEMENTATION_READBACK_PUBLICATION =
PARTIALLY_ACCEPTED / REMEDIATION_REQUIRED / RECORDED
```
