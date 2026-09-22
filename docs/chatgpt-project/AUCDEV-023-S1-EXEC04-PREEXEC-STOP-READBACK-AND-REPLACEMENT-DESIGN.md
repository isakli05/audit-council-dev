# AUCDEV-023 S1 EXEC-04 Preexec-Stop Readback and Replacement Execution-Admission Binding Remediation Design

Date: 2026-09-22 (Europe/Istanbul). Canonical record of the AUCDEV-023 S1
EXEC-04 preexec-stop readback and the Control-Room-selected replacement
execution-admission binding remediation design.

## 0. Session role (verbatim scope declaration)

This is a RECORD / DESIGN PUBLISHER ONLY session (Claude Code + GLM-5.3,
ZERO-PROVIDER). This session is NOT the Control Room decision-maker, NOT an
execution controller, NOT Auditor-A or Auditor-B, NOT a replacement execution
authority, NOT a qualification authority, NOT an installation authority.

- EXEC-04 was NOT run by this session. The wrapper/driver were NOT executed.
- Neither auditor was run.
- NO credential was read.
- NOTHING was deployed.
- NO AccountingStore state was created.
- NO successor package was modified.
- EBS / qualification-harness / skill trees were NOT modified.
- NO replacement authority was created, granted or exercised (there is NO
  EXEC-05 authority; no replacement launcher was generated or executed; the
  EXEC-04 driver/wrapper were NOT altered).
- ZERO provider/model/frontier inference.

## 1. Live bootstrap (verified EXACT before any work)

Repository `isakli05/audit-council-dev`, branch `master`:

- live GitHub `refs/heads/master` (git ls-remote) =
  `28e76bc9fb3ad597b4436dff73c560cb5ba7968b` EXACT;
- local `origin/master` == `HEAD` == `master` =
  `28e76bc9fb3ad597b4436dff73c560cb5ba7968b` EXACT;
- root tree at that SHA = `323a8ecc7684c1602543fc2d1a39861ef19ebd38` EXACT;
- sole parent = `d471fed7e046a25afeb8214ce1070032735db28e` EXACT;
- protected trees at that SHA EXACT: `bootstrap-supervisor` =
  `732b8def9f22d7c466ce77f3d3049da53bfff3d0` (the remediated EBS),
  `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`,
  `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f` (the latter two EQUAL
  the frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322`);
- tracked working-tree drift at bootstrap = only the long-known pre-existing
  `smoke-fixture` / `smoke-fixture-103` gitlink drift (unstaged, preserved);
  ZERO tracked modifications under `bootstrap-supervisor/`,
  `qualification-harness/`, `skill/` or `docs/chatgpt-project/`.

Canonical governance documents were fetched and read at that exact SHA
(CURRENT-STATE, BACKLOG, SUCCESSOR-EVENT-PACKAGE-READBACK,
EXEC04-OPERATOR-LAUNCHER-PREPARATION-READBACK, CONTROL-ROOM-RUNBOOK,
PROJECT-UPDATE-PROTOCOL). Had live master differed, this session would have
STOPPED WITHOUT MUTATION.

## 2. Operator-supplied terminal observation (verbatim)

The HUMAN OPERATOR invoked, exactly once:

```
cd /home/isa/audit-council-dev
./run-aucdev023-firstpass-exec04.sh
```

The exact observed terminal result supplied by the operator, verbatim
(terminal line wrapping preserved as supplied):

```
[exec04 19:57:19] PHASE 0 — fail-closed operator / host / repository check
[exec04 19:57:19] STOP (10): LOCAL_HEAD_MISMATCH:
28e76bc9fb3ad597b4436dff73c560cb5ba7968b. STOP. DO NOT RE-RUN THIS
AUTHORITY. RETURN THE EXACT FAILURE AND MECHANICAL HANDOFF TO CONTROL ROOM.
ANY REPLACEMENT REQUIRES NEW EXPLICIT OPERATOR AUTHORITY.
```

Process exit status: `10`.

Classification: **OPERATOR_SUPPLIED_TERMINAL_OBSERVATION**. No additional
runtime evidence is invented, inferred or claimed by this session beyond
this transcript, its exit status, and the source-correlated mechanics in
§4/§5 below. This is NOT characterized as an Auditor-A or Auditor-B failure:
neither auditor process ever started.

## 3. Exact accepted EXEC-04 launcher identity (read-only re-verification)

All verified read-only by this session; NEITHER file was executed:

- driver `/home/isa/audit-council-dev/aucdev023-firstpass-exec04.py`
  SHA-256 `6f4d7d62ea3b26ad9643d6793392d069bc8125400553dab07597ab53c8329cc9`
  (103,484 B) mode `0700` — EXACT match to the Control-Room-accepted
  launcher preparation identity;
- wrapper `/home/isa/audit-council-dev/run-aucdev023-firstpass-exec04.sh`
  SHA-256 `ca3a872ba16b31a0e3d0e74817f5527f3e7f7f5e6174f2819af01c243930154a`
  (2,809 B) mode `0700` — EXACT;
- preparation handoff
  `/home/isa/audit-council-dev/AUCDEV-023-FIRSTPASS-EXEC04-LAUNCHER-PREPARATION-HANDOFF.tar.gz`
  SHA-256 `6a91482058413f5120c7b8c0ab2e579471d4abb847f04bc1961297d36a790c1e`
  (74,286 B) — EXACT (identity only; nothing extracted or executed).

## 4. RUN-001 — preexec cause established from the accepted driver source

Mechanically established from the accepted driver bytes (`6f4d7d62…`),
read-only:

- `:91` — `REQUIRED_HEAD = "d471fed7e046a25afeb8214ce1070032735db28e"` (the
  successor-package Control Room readback publication checkpoint at which
  the launcher was prepared);
- `:874-877` — phase-0 repository admission requires local
  `git rev-parse HEAD` == `REQUIRED_HEAD`, else
  `DriverStop(EXIT["PHASE0"], "LOCAL_HEAD_MISMATCH: <observed>. " + STOP_SUFFIX)`;
- `:879-882` — the SAME admission separately requires live
  `git ls-remote origin refs/heads/master` == `REQUIRED_HEAD`, else
  `REMOTE_MASTER_MISMATCH`;
- `:290` — `EXIT["PHASE0"] = 10` (the observed exit status 10 and the
  `STOP (10)` prefix are exactly this admission stop).

Observed correlation: the MANDATORY launcher-preparation Control Room
readback publication (commit `28e76bc9fb3ad597b4436dff73c560cb5ba7968b`,
docs/chatgpt-project only, protected runtime trees unchanged) — which the
launcher-preparation readback itself recorded as
`CANONICAL_PUBLICATION_REQUIRED_BEFORE_HUMAN_INVOCATION` — advanced
canonical master (local and remote) from `d471fed7…` to `28e76bc9…`
BEFORE the operator invocation. The operator-supplied transcript shows the
exact observed local HEAD `28e76bc9fb3ad597b4436dff73c560cb5ba7968b`
mismatching the pinned `REQUIRED_HEAD` `d471fed7…`, so the launcher
fail-closed stopped at the first repository-admission check (the remote
check at `:880` was never reached in this stop; nothing about the remote
state at run time is claimed beyond the source semantics).

Therefore the launcher's own mandatory readback publication deterministically
invalidated its exact-HEAD pin while leaving every runtime-critical identity
unchanged. Recorded:

**`AUCDEV023-CR-S1-EXEC04-RUN-001` =
MANDATORY_READBACK_PUBLICATION_INVALIDATED_EXACT_HEAD_PINNED_LAUNCHER**

Classification: HARNESS / PROTOCOL DEFECT / EXECUTION-ADMISSION BINDING
SEQUENCING DEFECT / OBSERVED_SOURCE_FACT + OPERATOR_SUPPLIED_TERMINAL_OBSERVATION
/ PREEXEC_STOP / ZERO_MODEL_ENGAGEMENT. This is NOT an Auditor-A/B failure
and NOT a successor-package defect: every package/binding/EBS/contract
identity remains exact (§7).

## 5. RUN-002 — pre-evidence handoff gap established from the same source

Mechanically established from the accepted driver bytes, read-only:

- `:784` — production context initializes `"evidence_dir": None`;
- `run_pipeline` (`:2123`) calls `phase0_operator_host_check(ctx)` FIRST;
- the runtime evidence directory is created only at `:1016-1022`
  (`os.makedirs(ctx["evidence_base"]…)` / `os.mkdir(ctx["evidence_dir"], 0o700)`),
  i.e. AFTER every phase-0 admission check including the `:875` local-HEAD
  check;
- `build_handoff(ctx)` (`:1884`) immediately returns `None` when
  `ctx["evidence_dir"] is None` (`:1890`), and the terminal
  `finally` handler (`:2157`) invokes handoff generation only
  `if ctx["evidence_dir"] is not None`;
- `:284-286` — `STOP_SUFFIX` demands: "STOP. DO NOT RE-RUN THIS AUTHORITY.
  RETURN THE EXACT FAILURE AND MECHANICAL HANDOFF TO CONTROL ROOM. ANY
  REPLACEMENT REQUIRES NEW EXPLICIT OPERATOR AUTHORITY."

Therefore this exact Phase-0 failure CANNOT produce the mechanical handoff
its own STOP suffix demands: the stop fires before any evidence context
exists. Corroborated live by this session: `exec04-run-evidence/` is ABSENT
under `/home/isa/audit-council-dev` (not even the evidence base was created)
and the future mechanical handoff path
`/home/isa/audit-council-dev/AUCDEV-023-S1-FIRSTPASS-EXEC-20260922-04-MECHANICAL-HANDOFF.tar.gz`
is ABSENT. Recorded:

**`AUCDEV023-CR-S1-EXEC04-RUN-002` =
PHASE0_STOP_REQUIRES_MECHANICAL_HANDOFF_BEFORE_EVIDENCE_CONTEXT_EXISTS**

Classification: HARNESS / PROTOCOL DEFECT / PREEXEC FAILURE-EVIDENCE
COMPLETENESS GAP / OBSERVED_SOURCE_FACT /
NO_RUNTIME_HANDOFF_EXPECTED_FOR_THIS_EXACT_STOP. NO runtime mechanical
handoff has been fabricated for EXEC-04; none exists; none is claimed.

## 6. EXEC-04 terminal authority state

Authority `AUCDEV-023-S1-FIRSTPASS-EXEC-20260922-04` is now recorded:

**CLOSED / PREEXEC_STOP / NO_RERUN / NON-TRANSFERABLE**

over event `evt-79182989824ce966`, attempt A `evt-79182989824ce966-A-01`,
attempt B `evt-79182989824ce966-B-01`. Supported runtime state (zero
engagement; no EBS attempt record exists for either attempt — the driver
stopped before any accounting surface could be created):

- deployment = NONE (deployed event remains the historical EXEC-03
  generation; `event.staging.exec04-successor` absent);
- AccountingStore creation = NONE;
- credential plaintext read = NONE;
- runtime RESOURCE_GATE execution = NONE;
- runtime NETWORK_READINESS execution = NONE;
- EBS runtime events: GATES_PASSED = NONE, CONSUMED_PRE_EXEC = NONE,
  EXEC_ATTEMPTED = NONE;
- Auditor-A process = NOT STARTED; Auditor-B process = NOT STARTED;
- report lifecycle = NOT STARTED;
- model engagements = 0 / 2.

## 7. Successor identities remain pristine (read-only verification NOW)

Verified by this session, read-only, all EXACT/ABSENT as required:

- successor A attempt root `…/attempts/evt-79182989824ce966-A-01` ABSENT;
  successor B attempt root `…/attempts/evt-79182989824ce966-B-01` ABSENT
  (launcher-root attempts namespace listing contains ZERO
  `evt-79182989824ce966*` entries; a bounded
  `find /home/isa/aucdev023-s1-prep002-rem002 -maxdepth 3 -name '*79182989824ce966*'`
  sweep returned ZERO paths);
- NO successor AccountingStore records, staging reports or custody outputs
  exist anywhere under the launcher root;
- future backup
  `/home/isa/aucdev023-s1-prep002-rem002/event.backup.pre-successor-event`
  ABSENT;
- deployed event root `/home/isa/aucdev023-s1-prep002-rem002/event/` remains
  the EXACT historical EXEC-03 generation: deployed
  `runtime/resource-gate.py` SHA-256
  `27948980653f4c0639041243d9f117087f0987c5cc53623abbfa39cbb143adaf`
  (both role copies), `runtime/network-readiness.py`
  `20f37e9191d3e1e025962723328c5f8a2849f664cf1bf215715ccf8da9fc7235`
  (both), `runtime/output-validator.py`
  `6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071`
  (both), deployed contract
  `e4204e673e56d62d4e4ba0aceb44cc5ca599cf2ddb4e774568977544ac3fdd73`
  at all four copies with `event_id: evt-31f2a399b3a7e11d`;
  `event.backup.pre-exec03-new-event` and `event.backup.pre-exec02`
  preserved untouched;
- accepted successor source workspace
  `/home/isa/aucdev023-s1-successor-event-package-prep/event/` byte/mode
  EXACT: binding files `5204d90e451df4098423a0b4a9b4bd97859496dee1ad384da2e1c49f48a3efe3`
  (A) and `489a3c911d00d109054e108fa0c89e878fa14f908e01f320022b6bbd1888ade4`
  (B); MANIFEST bytes
  `2f8efbd65c930da9f6ab68b3921bf74961d0cb8eaf0324b0d14ef439107d8e8d` (A) and
  `15729d8bac5ee61f0c317c15fe9318100f942751802bb87e9f7a754ded9d7440` (B);
  both bindings pin the accepted non-circular package identities
  `87fd285e13fc2a6c8bfd5e64f7a642d3a275b302a2d77183d92d02814195b8c4` (A) and
  `072d0087f950bd7495d29685065133ee405e60876bc35fa26fe1f2100b4a406d` (B);
  the successor contract
  `cc6ec29db510168f2f3831dfedc120b17b74a82b1b920c901abd7dde07226e76` is
  byte-identical at all four staged copies; both bindings pin the
  remediated EBS pair
  `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999` /
  `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8`.

Since no successor attempt/runtime state was created by EXEC-04:

**`SUCCESSOR_IDENTITY_REUSE_ELIGIBILITY` =
ELIGIBLE_UNDER_NEW_EXPLICIT_AUTHORITY_ONLY /
SAME_EVENT_EVT_79182989824CE966 / SAME_FRESH_A01_B01 /
NO_ATTEMPT_STATE_CREATED_BY_EXEC04 /
MUST_REVERIFY_AT_REPLACEMENT_PREPARATION_AND_RUNTIME**

This eligibility is NOT new execution authority (see §10).

## 8. Control-Room-selected replacement execution-admission design (for RUN-001)

The following design is recorded as the SELECTED remediation for RUN-001.
The replacement launcher MUST NOT require current development HEAD to equal
the HEAD that existed when the launcher was prepared. Reason: a mandatory
canonical readback/publication commit is itself expected to advance
development HEAD while leaving runtime-critical source and package
identities unchanged; the Project update protocol explicitly distinguishes
development HEAD from a release certificate and allows the
recording/publication commit to be a descendant of the last verified
checkpoint.

### 8.1 Immutable source-trust anchor

`SOURCE_TRUST_ANCHOR_COMMIT = d471fed7e046a25afeb8214ce1070032735db28e`
(the canonical successor-package Control Room readback publication
checkpoint). At future runtime require ALL of:

1. local HEAD == live origin/master;
2. `SOURCE_TRUST_ANCHOR_COMMIT` is an ancestor of current HEAD;
3. NO merge commit exists in `SOURCE_TRUST_ANCHOR_COMMIT..HEAD`;
4. every COMMITTED path changed in `SOURCE_TRUST_ANCHOR_COMMIT..HEAD` is
   under `docs/chatgpt-project/`;
5. no committed runtime/source path outside that documentation subtree
   changed.

This intentionally permits later canonical governance/readback
publications. It does NOT permit source/runtime drift.

### 8.2 Exact runtime-critical tree pins

Current HEAD must still carry EXACT:

- `bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0`
- `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`
- `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f`

and the working tree must contain NO tracked modifications under those
three paths.

### 8.3 Pin accepted canonical evidence records

A future replacement launcher must pin and verify at runtime the exact Git
blob identities of the immutable accepted records it depends on, including
at least:

- `docs/chatgpt-project/AUCDEV-023-S1-SUCCESSOR-EVENT-PACKAGE-READBACK.md`
  expected blob `57d09961303258902b7c9f3a6c0694bfaf9219a2`;
- `docs/chatgpt-project/AUCDEV-023-S1-EXEC04-OPERATOR-LAUNCHER-PREPARATION-READBACK.md`
  expected blob `ce54436df1d63c28f4ba4fa8405f88eca3d43203`.

The future replacement-design canonical record created by THIS session —
`docs/chatgpt-project/AUCDEV-023-S1-EXEC04-PREEXEC-STOP-READBACK-AND-REPLACEMENT-DESIGN.md`
— must ALSO be pinned by its exact Git blob in the future replacement
launcher (its blob identity is recorded in the CURRENT-STATE dated record of
this publication and in the generated-LAST publication handoff).
CURRENT-STATE and BACKLOG are intentionally NOT immutable byte pins because
append-only governance publication advances them.

### 8.4 Package / EBS / contract pins remain exact

Keep exact accepted successor identities unchanged:

- event = `evt-79182989824ce966`; A = `evt-79182989824ce966-A-01`;
  B = `evt-79182989824ce966-B-01`;
- contract = `cc6ec29db510168f2f3831dfedc120b17b74a82b1b920c901abd7dde07226e76`;
- validator = `6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071`;
- EBS manifest = `d683f64dd86c8e3c5da80c09b85522caa7930f5698fccab311f21ecc75257999`;
- EBS package = `d42aa9e3dd1f6d4ed8831c13aaf7352dcaaab20cbb5ac81559e57eae93c922f8`;
- A manifest = `2f8efbd65c930da9f6ab68b3921bf74961d0cb8eaf0324b0d14ef439107d8e8d`;
- A package = `87fd285e13fc2a6c8bfd5e64f7a642d3a275b302a2d77183d92d02814195b8c4`;
- A binding = `5204d90e451df4098423a0b4a9b4bd97859496dee1ad384da2e1c49f48a3efe3`;
- A binding digest = `4adb47a788275e2544a55113e4651d35e38ce946e0182339cba10e815bcf51ca`;
- B manifest = `15729d8bac5ee61f0c317c15fe9318100f942751802bb87e9f7a754ded9d7440`;
- B package = `072d0087f950bd7495d29685065133ee405e60876bc35fa26fe1f2100b4a406d`;
- B binding = `489a3c911d00d109054e108fa0c89e878fa14f908e01f320022b6bbd1888ade4`;
- B binding digest = `7846ad8eb3bf2ce44b5bfe58cd20c7c9d589d060a4ff97aa56357bbc539fc596`.

### 8.5 Working-tree fail-closed checks

The future launcher must fail closed if any tracked working-tree
modification exists under the runtime-critical tracked paths
`bootstrap-supervisor/`, `qualification-harness/`, `skill/`. The known
unrelated smoke-fixture gitlink drift does NOT grant permission to ignore
runtime-critical drift. Untracked launcher/evidence artifacts must continue
to be explicitly identity-bound where applicable.

### 8.6 Pre-attempt recheck

Immediately before EACH possible real attempt, re-run ALL of: local HEAD ==
live origin/master; anchor ancestry; zero merges since anchor;
committed-diff path allowlist; protected runtime trees; pinned
accepted-record blobs; exact package/binding/EBS/contract/runtime artifact
identities. No dynamic adaptation. Any failure: terminal PREEXEC STOP; no
retry.

## 9. Control-Room-selected remediation for RUN-002 (pre-phase evidence context)

A replacement launcher must create a NON-SECRET invocation/evidence context
BEFORE Git-admission checks that can fail. Requirements:

- the creation itself must NOT create an attempt root; must NOT create
  AccountingStore; must NOT read credentials; must NOT execute any runtime
  gate; must NOT deploy; must be authority/event scoped; must be
  non-overwriting; and its existence marks that the replacement authority
  invocation occurred.

On ANY subsequent Phase-0/preexec failure the context must receive: the
exact sanitized terminal failure facts; the authority/event identity;
local/remote HEAD where available; the zero-engagement state; and the
sanitized mechanical handoff generated LAST. This ensures the STOP
instruction can truthfully require a mechanical handoff. Report bytes and
credential material must NEVER enter this evidence plane.

## 10. No replacement authority yet

THIS session does NOT create or grant a replacement execution authority.
No EXEC-05 authority exists. No replacement launcher was generated or
executed. The EXEC-04 driver/wrapper were NOT altered (they remain at their
accepted identities in §3, now terminal historical artifacts). After this
record is independently verified by the Control Room, the HUMAN OPERATOR
must grant a NEW explicit replacement authority. The Control Room intends
that, if all pristine-state checks remain satisfied, the replacement
authority MAY bind the SAME successor event / A-01 / B-01 identities,
because EXEC-04 created no real attempt/accounting state. That future grant
remains a separate operator decision.

## 11. Canonical dispositions (recorded verbatim)

```
AUCDEV_023_S1_EXEC04_PREEXEC_STOP_READBACK =
ACCEPTED_SOURCE_CORRELATED_PREEXEC_MECHANICS
/ LOCAL_HEAD_MISMATCH_ESTABLISHED
/ RUN001_ESTABLISHED
/ RUN002_ESTABLISHED
/ ZERO_DEPLOYMENT
/ ZERO_ACCOUNTING
/ ZERO_CREDENTIAL_READ
/ ZERO_GATE_EXECUTION
/ ZERO_AUDITOR_EXECUTION
/ MODEL_ENGAGEMENTS_0_OF_2
/ AUTHORITY_EXEC04_CLOSED_NO_RERUN
/ SUCCESSOR_EVENT_ATTEMPTS_PRISTINE_IF_REVERIFIED
/ RUNTIME_MECHANICAL_HANDOFF_ABSENT_BY_PRE_EVIDENCE_DESIGN
/ REPLACEMENT_AUTHORITY_REQUIRED
```

```
AUCDEV_023_REPLACEMENT_EXECUTION_ADMISSION_REMEDIATION_DESIGN =
CONTROL_ROOM_SELECTED
/ PUBLICATION_SAFE_LINEAGE_BINDING
/ EXACT_RUNTIME_CRITICAL_TREE_BINDING
/ EXACT_ACCEPTED_RECORD_BLOB_BINDING
/ EXACT_PACKAGE_BINDING_HELD
/ PREPHASE_MECHANICAL_EVIDENCE_CONTEXT_REQUIRED
/ NO_DYNAMIC_ADAPTATION
/ IMPLEMENTATION_REQUIRES_NEW_REPLACEMENT_AUTHORITY
/ REAL_EXECUTION_NOT_AUTHORIZED
```

## 12. Publication discipline and zero-execution attestation

Changed paths EXACTLY: NEW
`docs/chatgpt-project/AUCDEV-023-S1-EXEC04-PREEXEC-STOP-READBACK-AND-REPLACEMENT-DESIGN.md`
+ MODIFIED `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` + MODIFIED
`docs/chatgpt-project/AUCDEV-BACKLOG.md`. ARCHITECTURE-SUMMARY UNCHANGED;
`bootstrap-supervisor/`, `qualification-harness/`, `skill/`,
`source/tests/MANIFEST` UNCHANGED; all append-only CURRENT history preserved
byte-for-byte; NO historical report rewritten. Exactly ONE bounded
fast-forward publication commit over sole parent
`28e76bc9fb3ad597b4436dff73c560cb5ba7968b`; no merge, rebase, amend, reset,
force or tag. AUCDEV-023 remains P1 / READY / NOT DONE with NO backlog
count/status change (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 /
P2 11). Qualification NONE; installation NONE.

Zero-execution attestation: ZERO provider/model/frontier executions; ZERO
real credential reads; ZERO Auditor-A/B / audit-council executions; ZERO
deployment; ZERO AccountingStore creation; ZERO runtime-gate execution; the
EXEC-04 wrapper/driver NOT executed by this session; network activity =
the git fetch/push of this publication only. The generated-LAST small
publication handoff is produced after the push; nothing mutates afterward.

## 13. Next action (exactly ONE)

CONTROL ROOM VERIFICATION OF THIS EXEC-04 PREEXEC-STOP / REPLACEMENT-DESIGN
PUBLICATION BEFORE THE HUMAN OPERATOR GRANTS ANY REPLACEMENT EXECUTION
AUTHORITY.
