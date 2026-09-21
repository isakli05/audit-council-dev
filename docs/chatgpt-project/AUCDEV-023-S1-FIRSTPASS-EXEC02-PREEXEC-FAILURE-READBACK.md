# AUCDEV-023 — S1 EXEC-02 First-Pass Preexec Failure: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION SESSION — a RECORD PUBLISHER ONLY for the Audit Council Dev Control Room's ALREADY-COMPLETED mechanical handoff readback and ALREADY-DECIDED disposition; NOT the Control Room decision-maker, NOT a remediation implementer, NOT an independent auditor, NOT Auditor-A/B, NOT an execution controller, NOT an execution/qualification/installation authority; NOT authorized to remediate anything, to retry or replace any attempt, or to reinterpret/strengthen/weaken any finding; ZERO provider/model/frontier executions, ZERO Auditor-A/B/`/audit-council` executions, ZERO real credential reads, ZERO new real attempt consumption, ZERO AccountingStore real-attempt creation, ZERO GATES_PASSED, ZERO CONSUMED_PRE_EXEC, ZERO package/binding/manifest/launcher/runtime-gate/EBS/qh/skill/frozen-target/event/attempt mutation; NO rollback of the accepted deployment; no submitted handoff script or package artifact executed |
| Date | 2026-09-21 (Europe/Istanbul) |
| Subject event | The FIRST real first-pass execution attempt under operator execution authority `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02` for event `evt-7df609ec6c569043`, reserved attempts `evt-7df609ec6c569043-A-01` / `evt-7df609ec6c569043-B-01` — the human operator executed the frozen deterministic wrapper/driver directly with NO Claude Code / GLM / inference-capable controller on the runtime authority path; the attempt reached and failed the frozen RESOURCE_GATE pre-exec (exit 3) and terminated TERMINAL_PREEXEC_STOP before any GATES_PASSED / CONSUMED_PRE_EXEC / exec / report; mechanical handoff `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02-MECHANICAL-HANDOFF.tar.gz` outer SHA-256 `281f31e120608351cbb794ccb0d4296e26848e93f2e7138559e8d104ffafe31b` (31837 bytes; outer identity re-verified read-only EXACT by THIS publication session at `/home/isa/audit-council-dev/AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02-MECHANICAL-HANDOFF.tar.gz` — size and SHA-256 both EXACT; nothing executed from any archive) |
| Subject | The Control Room mechanical readback of the EXEC-02 deployment + failed Auditor-A attempt, the new finding `AUCDEV023-CR-S1-EXEC02-001` RESOURCE_GATE_EBS_ARGV_CONTRACT_MISMATCH (OPEN / BLOCKING FIRST-PASS EXECUTION), the recorded completeness limitation `AUCDEV023-CR-S1-EXEC02-002`, the credential-custody and NETWORK_READINESS facts, the authority/attempt/budget state, the held prior states, and the resulting no-retry / non-transferable-authority posture |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |

Claim classes: `OBSERVED_FACT` (mechanically observed in this session),
`FINDING_TEXT` (Control Room disposition/finding text, recorded verbatim),
`REQUIREMENT`. §§2–11 are the CONTROL ROOM's decision recorded EXACTLY; this
publication session neither adjudicates nor amends it.

---

## 1. Live bootstrap (OBSERVED_FACT)

Live `refs/heads/master` of `isakli05/audit-council-dev` was resolved at this
session's bootstrap (fetch + `git rev-parse origin/master`) and required to
equal EXACTLY the mandated base: commit
`52c4bb2544affcf61b5851b593914d2988006141`; tree
`a5f648f6e6b3e2320848cb252e77ef087ae47356`; sole parent
`ef5e9998ed9dc92bb906f9036aec87cae62814a0`. Protected trees verified EXACT
(bootstrap-supervisor `09f3d6c7ddc00305986cbedad431395c10c95af0`;
qualification-harness `5b8d5e5465923740470ff63ed9b8683f257a3787`; skill
`c792933a862d9a5434681a88d183470dd8b15d2f`, the latter two EQUAL the frozen
audit target `d4d584ffa47ad2848268ba947247f81a845b2322`). CURRENT-STATE,
BACKLOG and the existing AUCDEV-023 EXEC-001/readback/governance records
were fetched and read at that exact SHA. No STOP-WITHOUT-MUTATION was
required: no drift existed. Pre-existing smoke-fixture gitlink drift and
untracked evidence directories (including `exec02-run-evidence/`, the frozen
driver `aucdev023-firstpass-exec02.py` and its wrapper) were observed and
preserved unstaged.

Read-only evidence re-verification performed by THIS publication session
(nothing executed, nothing mutated): the mechanical handoff outer identity
(size 31837 B; SHA-256 `281f31e1…`) EXACT; handoff census 15 regular files /
14 SHA256SUMS rows / 14-of-14 checksum PASS / unsafe-traversal 0 / duplicates
0 / symlink-hardlink-special 0; the handoff's A accounting record carries
EXACTLY `PREPARED` then `TERMINAL_PREEXEC_STOP` and no
GATES_PASSED/CONSUMED_PRE_EXEC/EXEC_ATTEMPTED/REPORT_FROZEN; the LIVE
accounting record at
`/home/isa/aucdev023-s1-prep002-rem002/attempts/evt-7df609ec6c569043-A-01/accounting/`
equals that two-state record EXACTLY (B accounting directory EMPTY); the
Auditor-A staging/custody-out directories EMPTY; the historical generation
backup `/home/isa/aucdev023-s1-prep002-rem002/event.backup.pre-exec02`
PRESENT; the deployed frozen RESOURCE_GATE at
`/home/isa/aucdev023-s1-prep002-rem002/event/package-auditor-{a,b}/runtime/resource-gate.py`
SHA-256 `e8f85391109d8f552294e9f887d2d3e90c145da87e1d0a648917cd681f71d6a6`
(3869 B) IDENTICAL both roles; and the live EBS source at exact repository
HEAD `52c4bb2…` (`bootstrap-supervisor/ebs/launch.py`) constructs the
RESOURCE_GATE argv exactly as recorded in §6 below.

## 2. Authorized execution event (FINDING_TEXT — recorded exactly)

```
Authority: AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02
Event:     evt-7df609ec6c569043
Attempts:  evt-7df609ec6c569043-A-01
           evt-7df609ec6c569043-B-01

The human operator executed the frozen deterministic wrapper directly.
No Claude Code / GLM / inference-capable controller was on the runtime
authority path.
```

## 3. Control Room mechanical handoff readback (FINDING_TEXT — recorded exactly)

```
Mechanical handoff:
AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02-MECHANICAL-HANDOFF.tar.gz

Control Room independently verified:
outer SHA-256 =
281f31e120608351cbb794ccb0d4296e26848e93f2e7138559e8d104ffafe31b
size = 31837 bytes
member census = 15 regular files
unsafe/traversal = 0
duplicates = 0
symlinks = 0
hardlinks = 0
special = 0
exactly one SHA256SUMS = 14 rows / 14 PASS
unlisted payload = 0
listed-but-absent = 0
```

The handoff contains NO credential material of any kind (credential sources
referenced by PATH METADATA only) and NO first-pass report bytes (there are
no first-pass reports to include); the driver recorded stat/SHA-256/size/mode
inventory data only and never parsed report substance.

## 4. Deployment result (FINDING_TEXT — recorded exactly)

```
The operator driver successfully completed:

PHASE 0: live/local HEAD exact (52c4bb2544affcf61b5851b593914d2988006141);
protected trees exact; live EBS identity exact (package 8685c36e…,
manifest 68490d79…, 31 rows); attempts pristine.

PHASE 1: accepted successor generation exact for both roles
(A manifest 45805629… / package 703dd95b… / binding digest 5c48fa3f…;
B manifest 5c1421ae… / package 23131e88… / binding digest f088b132…;
launcher 2efb6660…; RESOURCE_GATE e8f85391… — the Control-Room-accepted
EXEC-001 successor identities, source /home/isa/aucdev023-s1-exec001-remediation/event).

PHASE 2: prior accepted deployed event generation classified OLD_ACCEPTED;
accepted new generation staged, completely verified and atomically deployed;
historical generation preserved at:
/home/isa/aucdev023-s1-prep002-rem002/event.backup.pre-exec02

PHASE 3: deployed A+B generation completely reverified exact — full deployed
reverify completed BEFORE any AccountingStore creation and BEFORE any
credential read.

Deployment itself is accepted as mechanically completed.
Do not roll it back in this publication.
```

## 5. Auditor-A attempt result (FINDING_TEXT — recorded exactly)

```
Attempt: evt-7df609ec6c569043-A-01

Accounting record contains EXACTLY:
PREPARED
TERMINAL_PREEXEC_STOP

and does NOT contain:
GATES_PASSED
CONSUMED_PRE_EXEC
EXEC_ATTEMPTED
REPORT_FROZEN

Mechanical attempt failure:
RESOURCE_GATE_NONZERO_EXIT: exited 3

Auditor-A:
NO conforming first pass
NO frozen first-pass report
NO inference-capable exec attempt
AUTHORITY NOT CONSUMED

Auditor-B:
NOT STARTED
accounting record ABSENT

Fail-closed model-engagement budget charge:
0 / 2

Barrier:
CLOSED

No retry is authorized.
```

## 6. NEW FINDING EXEC02-001 (FINDING_TEXT — recorded exactly)

```
Record:
AUCDEV023-CR-S1-EXEC02-001

Title:
RESOURCE_GATE_EBS_ARGV_CONTRACT_MISMATCH

Classification:
HARNESS / PROTOCOL DEFECT
/ RUNTIME-GATE INVOCATION CONTRACT MISMATCH

Support:
OBSERVED runtime failure
* exact frozen-source fact
* exact live-EBS source fact

Frozen RESOURCE_GATE:
SHA-256 =
e8f85391109d8f552294e9f887d2d3e90c145da87e1d0a648917cd681f71d6a6

Resource gate declares:

argv contract:
identity, event_id, auditor_role, attempt_id

but implementation contains:

if len(sys.argv) < 5:
return 3

_identity, event, role, attempt = sys.argv[1:5]

Control Room independently verified the gate byte length:
3869 bytes
and SHA-256 exact equality to the accepted frozen gate.

Live EBS at exact repository HEAD invokes RESOURCE_GATE with:

argv = [
descriptor["identity"],
binding.event_id,
binding.auditor_role,
binding.attempt_id,
]

and passes that list directly through the verified-fd exec path.

Therefore the real EBS invocation exposes:

argv[0] = identity
argv[1] = event
argv[2] = role
argv[3] = attempt

The RESOURCE_GATE expects an extra leading argv element and exits 3 before
sampling workspace, memory or process headroom.

Therefore this failure is NOT evidence of low disk, low memory or excessive
process count.

Disposition:
OPEN / BLOCKING FIRST-PASS EXECUTION
```

Publication-session read-only confirmation of the two source facts: the
deployed frozen gate at both role package `runtime/` locations is byte-length
3869 with SHA-256 `e8f85391…` and contains exactly the declared argv contract
line, the `if len(sys.argv) < 5: return 3` guard and the
`_identity, event, role, attempt = sys.argv[1:5]` unpack; the live EBS at
exact HEAD `52c4bb2…` (`bootstrap-supervisor/ebs/launch.py`) builds
`argv = [descriptor["identity"], binding.event_id, binding.auditor_role,
binding.attempt_id]` and passes that exact list through
`_run_runtime_gate` → `_gate_child` → `fd_exec` (verified-fd exec; no
program-name element is prepended), so the gate process observes
`len(sys.argv) == 4 < 5` and exits 3 before any sampling. (The same EBS
construction appends three further elements for NETWORK_READINESS, which is
consistent with NETWORK_READINESS passing — §8.)

## 7. NEW FINDING EXEC02-002 (FINDING_TEXT — recorded exactly)

```
Record:
AUCDEV023-CR-S1-EXEC02-002

Title:
SYNTHETIC_RESOURCE_GATE_REHEARSAL_DID_NOT_REPRODUCE_EBS_FD_EXEC_ARGV

Classification:
COMPLETENESS LIMITATION
/ HARNESS TEST-COVERAGE GAP

The earlier EXEC-001 synthetic RESOURCE_GATE rehearsal invoked the gate
directly with an argv shape equivalent to:

  <gate>
  identity
  event
  role
  attempt

This produced five sys.argv elements and PASSed.

That rehearsal therefore validated:
* corrected workspace ROOT;
* actual launcher-root workspace sampling;
* resource samples;

but did NOT reproduce the EBS verified-fd exec argv semantics.

It consequently did not detect EXEC02-001.

Retain the historical synthetic rehearsal as valid for what it actually
tested; do NOT rewrite it as fraudulent or absent.
```

## 8. Network / credential facts (FINDING_TEXT — recorded exactly)

```
The live EBS order is:

credential custody ingest
→ NETWORK_READINESS
→ RESOURCE_GATE
→ GATES_PASSED
→ CONSUMED_PRE_EXEC
→ provider-capable exec

Because RESOURCE_GATE was reached:
* credential material for Auditor-A had already been ingested into sealed EBS
  custody;
* NETWORK_READINESS had already completed successfully;
* RESOURCE_GATE then failed before GATES_PASSED.

The operator driver reported the credential source metadata size as 519 bytes.

Do NOT publish credential content.

No credential material exists in the mechanical handoff.

NETWORK_READINESS is a resolver + TCP-connect readiness gate with zero
application payload bytes.

Therefore record separately:

REAL A CREDENTIAL CUSTODY INGEST =
OCCURRED

NETWORK_READINESS =
PASSED BEFORE RESOURCE_GATE

PROVIDER CLIENT EXECUTION =
NONE

MODEL INFERENCE =
NONE

MODEL ENGAGEMENT BUDGET CHARGED =
0 / 2

Do not call NETWORK_READINESS a model/provider inference call.
```

## 9. Authority / attempt state (FINDING_TEXT — recorded exactly)

```
Authority:
AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02

Resulting operational state:

NO FURTHER EXECUTION UNDER THIS AUTHORITY
/ NO SAME-ATTEMPT RETRY

A attempt:
evt-7df609ec6c569043-A-01 =
TERMINAL_PREEXEC_STOP
/ UNCONSUMED
/ NO MODEL ENGAGEMENT
/ MUST NOT BE REUSED

B attempt:
evt-7df609ec6c569043-B-01 =
NOT STARTED

However, because remediation of the shared frozen RESOURCE_GATE will change
event-package identity, this exact-generation authority MUST NOT transfer to
the remediated generation.

A future replacement requires:
* NEW explicit operator authority;
* NEW attempt id for replacement Auditor-A;
* new bindings/package identities as mechanically required by the remediation;
* fresh Control Room readback before execution.

Do NOT authorize any replacement here.
```

## 10. Held states (FINDING_TEXT — recorded exactly)

```
Do NOT reopen merely because of this finding:
PREP-001/-002/-003
REM-001/-002
EXEC-001

EXEC-001's corrected workspace ROOT remains correct.

The new defect is distinct:
EXEC02-001 = argv invocation contract mismatch.

AUCDEV-023 remains:
P1 / READY / NOT DONE

Qualification:
NONE

Installation:
NONE
```

## 11. Control Room disposition (FINDING_TEXT — recorded exactly)

```
AUCDEV_023_S1_FIRSTPASS_EXEC02_MECHANICAL_READBACK =
ACCEPTED_MECHANICS
/ DEPLOYMENT_VERIFIED
/ AUDITOR_A_TERMINAL_PREEXEC_STOP
/ AUDITOR_A_AUTHORITY_UNCONSUMED
/ AUDITOR_A_MODEL_ENGAGEMENT_ZERO
/ AUDITOR_B_NOT_STARTED
/ MODEL_ENGAGEMENT_BUDGET_0_OF_2
/ BARRIER_CLOSED
/ EXEC02_001_OPEN_BLOCKING
/ EXEC02_002_RECORDED_COMPLETENESS_LIMITATION
/ NO_RETRY_AUTHORIZED
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
```

This disposition is neither reinterpreted, strengthened nor weakened by this
publication session.

## 12. What this disposition is NOT (FINDING_TEXT — recorded exactly)

This is NOT:

* audit PASS;
* first-pass completion;
* qualification;
* installation.

## 13. Publication scope (OBSERVED_FACT — what THIS session changes)

Create exactly one NEW append-only canonical record:
`docs/chatgpt-project/AUCDEV-023-S1-FIRSTPASS-EXEC02-PREEXEC-FAILURE-READBACK.md`
(THIS file). Update `AUCDEV-CURRENT-STATE.md` (header + current-facing
fields + dated record + next-operator-action rotation) and
`AUCDEV-BACKLOG.md` (dated record). `AUCDEV-ARCHITECTURE-SUMMARY.md` is
UNCHANGED: this preexec failure does not change the adopted R1 architecture
and no bounded factual note is required. NOT rewritten: the EXEC-001
remediation report and readback records, the first-pass execution-prelaunch
readback record, and every earlier preparation/remediation/readback record
(append-only history preserved). No backlog count/status change (no
backlog-row status transition; no backlog item DONE; AUCDEV-023 remains
P1 / READY / NOT DONE). No product/EBS/package source modification. No
remediation. No historical record rewrite. No rollback of the accepted
deployment. Pre-existing smoke-fixture gitlink drift + evidence directories
preserved unstaged.

## 14. Zero-execution / non-mutation attestation (OBSERVED_FACT)

Provider/model/frontier inference: ZERO. Auditor-A/B/`/audit-council`
executions: ZERO (the recorded preexec failure belongs to the operator's
ALREADY-PERFORMED authorized execution event, NOT to this session). Real
credential reads: ZERO (the credential-custody fact of §8 is recorded from
the Control Room's mechanical evidence; this session never opened any
credential source). New real attempt consumption: ZERO. AccountingStore
creation: ZERO. `Supervisor.run_attempt`: ZERO. Runtime-gate execution:
ZERO. Package/binding/manifest/launcher/wrapper/EBS/qh/skill/frozen-target/
event/attempt mutation: ZERO (protected trees verified EXACT before staging;
the deployed event tree, frozen workspaces, attempt directories and the
mechanical handoff were only read; the handoff archive outer identity was
re-verified read-only EXACT). Qualification/installation: NONE. No
deployment and no rollback performed. This publication confers NO execution
authority, authorizes NO retry or replacement, and authorizes NO remediation.

## 15. Commit / push protocol (OBSERVED_FACT)

Immediately before staging, live master will be re-resolved and required to
equal exactly `52c4bb2544affcf61b5851b593914d2988006141` with all protected
trees unchanged. Exactly ONE bounded append-only record-publication commit
whose sole parent is `52c4bb2544affcf61b5851b593914d2988006141`, followed by
at most ONE normal fast-forward push. No amend, merge, rebase, reset, force
push or tag. After push the result is independently read back from GitHub
(exact result SHA, root tree, sole parent, base..result relation, exact
changed paths, canonical blobs, protected trees, live master equality).

## 16. Next action — EXACTLY ONE (FINDING_TEXT)

```
CONTROL ROOM VERIFICATION OF THIS EXEC-02 PREEXEC FAILURE PUBLICATION,
FOLLOWED — ONLY IF CLEAN — BY BOUNDED RESOURCE_GATE/EBS-ARGV CONTRACT
REMEDIATION PLANNING UNDER A NEW EXPLICIT OPERATOR AUTHORITY.
```

## 17. Generated-LAST handoff archive (OBSERVED_FACT)

After ALL record work, commit, push and the independent GitHub readback are
complete, exactly ONE small non-secret `.tar.gz` publication handoff archive
is generated LAST, containing the new readback record, the resulting
CURRENT-STATE and BACKLOG, the exact diff, commit metadata, the GitHub
readback, protected-tree verification, the finding inventory, the
authority/accounting inventory, and the reference binding this publication to
the mechanical handoff outer SHA-256
`281f31e120608351cbb794ccb0d4296e26848e93f2e7138559e8d104ffafe31b`, with
exactly one SHA256SUMS covering every payload regular file except itself. NO
credentials, NO private logs, NO auditor report content (there are no
first-pass reports to include). Its path/SHA-256/size/census are recorded in
this session's final return. Nothing is mutated after archive generation.
