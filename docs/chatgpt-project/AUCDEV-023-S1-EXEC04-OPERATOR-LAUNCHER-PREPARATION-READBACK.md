# AUCDEV-023 — S1 EXEC-04 DETERMINISTIC OPERATOR-LAUNCHER PREPARATION: Control Room Readback (Canonical Record)

- **Date**: 2026-09-22 (Europe/Istanbul)
- **Session role**: RECORD PUBLISHER ONLY (Claude Code + GLM-5.3). NOT the
  Control Room decision-maker, NOT the launcher implementer, NOT an
  independent auditor, NOT Auditor-A/B, NOT an execution controller, NOT
  an execution authority, NOT a qualification/installation authority.
  This session publishes the ALREADY-DECIDED Control Room readback
  disposition verbatim.
- **Zero-execution attestation**: ZERO deployment; ZERO AccountingStore
  creation; ZERO credential read; ZERO runtime-gate execution; ZERO
  auditor execution; ZERO provider/model/frontier inference; the EXEC-04
  wrapper and driver were NOT executed by this session. The only work was
  read-only: the streamed census+checksum verification of the preparation
  handoff (nothing extracted to disk, nothing executed), hash/mode checks
  of the driver/wrapper/test-suite files, independent read-only
  regeneration and byte-comparison of the archived predecessor diffs,
  read-only source inspection of the driver/wrapper for the structural
  acceptance facts, read-only live-state checks of the launcher root and
  attempts namespace, and the canonical document updates. Network
  activity ZERO except the git fetch/push of this publication.
- **Exact base**: `d471fed7e046a25afeb8214ce1070032735db28e` (tree
  `8c8695e3efa5021fcbde7ec9f73b102bd389d3d9`; sole parent
  `7b24972f02997eba80f3cd309422acd31ce06f99`) verified EXACT as live
  master at bootstrap and re-resolved immediately before staging and
  push.

## 1. Live bootstrap (OBSERVED_FACT)

Live `origin/master` resolved to exactly
`d471fed7e046a25afeb8214ce1070032735db28e` (tree
`8c8695e3efa5021fcbde7ec9f73b102bd389d3d9`; sole parent
`7b24972f02997eba80f3cd309422acd31ce06f99`); local HEAD and FETCH_HEAD
identical; tracked working tree CLEAN apart from the pre-existing
smoke-fixture gitlink drift and untracked evidence directories/launcher
artifacts, all preserved unstaged. The five canonical documents
(CURRENT-STATE, BACKLOG, the successor-event-package readback, the
Control Room runbook, the project update protocol) were fetched at that
exact SHA. Protected trees at the base, all EXACT:
`bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0`
(the REMEDIATED EBS); `qualification-harness` =
`5b8d5e5465923740470ff63ed9b8683f257a3787`; `skill` =
`c792933a862d9a5434681a88d183470dd8b15d2f` (the latter two EQUAL the
frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322`
subtrees).

## 2. CONTROL ROOM READBACK DISPOSITION (FINDING_TEXT — recorded verbatim)

```
AUCDEV_023_S1_EXEC04_OPERATOR_LAUNCHER_PREPARATION_READBACK =
TECHNICALLY_ACCEPTED
/ DRIVER_IDENTITY_VERIFIED
/ WRAPPER_IDENTITY_VERIFIED
/ EXEC03_PREDECESSOR_DIFF_VERIFIED
/ ONE_SHOT_A_THEN_CONDITIONAL_B_VERIFIED
/ NO_RETRY_STRUCTURE_VERIFIED
/ REMEDIATED_REPORT_INVALID_MECHANICS_VERIFIED
/ GENERATED_LAST_MECHANICAL_HANDOFF_PATH_VERIFIED
/ AUTHORITY_EXEC04_NOT_EXERCISED
/ SUCCESSOR_EXECUTION_NOT_YET_INVOKED
/ PREPARATION_NAMESPACE_INCIDENT_RECORDED
/ CANONICAL_PUBLICATION_REQUIRED_BEFORE_HUMAN_INVOCATION
```

This is NOT execution success, NOT audit PASS, NOT first-pass
completion, NOT qualification and NOT installation.

## 3. Preparation handoff (FINDING_TEXT + OBSERVED_FACT)

Preparation handoff independently re-verified read-only EXACT by this
publication session (streamed census and checksum verification only;
nothing extracted or executed):

- Archive: `/home/isa/audit-council-dev/AUCDEV-023-FIRSTPASS-EXEC04-LAUNCHER-PREPARATION-HANDOFF.tar.gz`
- Outer SHA-256: `6a91482058413f5120c7b8c0ab2e579471d4abb847f04bc1961297d36a790c1e`
- Size: 74286 bytes
- Census: 14 members = 14 regular files; unsafe/traversal 0; duplicates
  0; symlinks 0; hardlinks 0; special 0
- Exactly one `SHA256SUMS`: 13 rows, 13/13 PASS; no missing; no
  unlisted payload.

## 4. Accepted launcher identities (FINDING_TEXT + OBSERVED_FACT)

- Driver: `/home/isa/audit-council-dev/aucdev023-firstpass-exec04.py`,
  SHA-256 `6f4d7d62ea3b26ad9643d6793392d069bc8125400553dab07597ab53c8329cc9`
  (103484 B, 2184 lines), runtime mode **0700** — re-hashed and
  re-stated EXACT by this session.
- Wrapper: `/home/isa/audit-council-dev/run-aucdev023-firstpass-exec04.sh`,
  SHA-256 `ca3a872ba16b31a0e3d0e74817f5527f3e7f7f5e6174f2819af01c243930154a`,
  runtime mode **0700** — re-hashed and re-stated EXACT by this session.
- The wrapper pins the driver SHA above
  (`REQUIRED_DRIVER_SHA256="6f4d7d62ea3b26ad9643d6793392d069bc8125400553dab07597ab53c8329cc9"`)
  and its final action is the single `exec /usr/bin/python3 -I` of the
  pinned driver; the wrapper refuses root execution, symlinked,
  non-regular, wrong-owner, wrong-mode and mutated drivers, disables
  core dumps and removes the `PYTHON*` startup environment.
- Preparation test suite:
  `/home/isa/audit-council-dev/aucdev023-exec04-prep-tests.py`, SHA-256
  `fd7c85a8e5d61d145561a8c4c73160569e093fc47fc8e5fd45337a41d9575c9e`,
  mode 0700 — re-hashed EXACT by this session.
- The future human command remains **DATA ONLY** in this publication
  session and was NOT run by this publisher:

  ```
  cd /home/isa/audit-council-dev
  ./run-aucdev023-firstpass-exec04.sh
  ```

## 5. Predecessor verification (FINDING_TEXT + OBSERVED_FACT)

- EXEC-03 driver `aucdev023-firstpass-exec03.py` SHA-256
  `722d4549c7466dd95a8d43907be053177633c75604f07537d424821331592133`;
  EXEC-03 wrapper `run-aucdev023-firstpass-exec03.sh` SHA-256
  `32876911716eb58e7aabd618c3d27d26354a8cda3e471668b07014b93077b190` —
  both re-hashed EXACT by this session (read as design precedent only;
  never executed).
- The Control Room independently verified the actual byte diff:
  driver = **27 hunks**, wrapper = **2 hunks**, with no unrelated
  behavioral drift.
- This publication session independently regenerated both unified diffs
  read-only from the live files and compared them byte-for-byte against
  the archived diff members of the preparation handoff:
  `driver-exec03-to-exec04.diff` (35886 B, SHA-256
  `378fb3c6a4da442d606ab68669537aa88efb1ac96fd8dedd09ac70180f296a6c`,
  27 hunks) and `wrapper-exec03-to-exec04.diff` (1357 B, SHA-256
  `152de87bf3730925a8bde6a8b65744b6d3a4e3aae30137dc5fa8287ae1872607`,
  2 hunks) — **byte-identical** in both cases, so the archived diff hunk
  bodies EQUAL the independently generated diffs.

## 6. Structural acceptance facts (FINDING_TEXT; source-verified read-only by this session)

- exactly one `AccountingStore.create` semantic site
  (`aucdev023-firstpass-exec04.py:1368`, inside the one-shot attempt
  executor);
- exactly one `Supervisor` construction site (`:1375`);
- exactly one `Supervisor.run_attempt` semantic site (`:1401`);
- no retry loop: the pipeline is one-shot (phase 0 precheck → phase 1
  source verify → phase 2 atomic deploy → phase 3 post-deploy reverify →
  exactly one Auditor-A attempt → conditional exactly one Auditor-B
  attempt → mechanical barrier → generated-LAST handoff); every failure
  path records `retry_authorized: false` and there is no loop-back;
- the Auditor-B path mechanically refuses unless Auditor-A is conforming
  (`run_role` refuses `AUDITOR_B_REFUSED_WITHOUT_CONFORMING_AUDITOR_A`
  when `ctx["a_conforming"] is not True`, and the pipeline only reaches
  B after a conforming A);
- REPORT_INVALID does NOT count as conformance even with client rc=0
  (`evaluate_conformance` requires `report_state == "REPORT_FROZEN"`;
  `returncode == 0` alone never establishes conformance);
- remediated REPORT_INVALID retains the exact invalid snapshot SHA/size
  (the remediated invalid block surfaces
  `invalid_snapshot_sha256`/`invalid_snapshot_size` from BOTH the
  AttemptResult and the durable REPORT_INVALID accounting record);
  invalid report BYTES are never copied into any evidence surface;
- the safe structural diagnostic token is bounded
  (`STRUCTURAL_TOKEN_MAX = 128` characters);
- both conforming reports yield only
  `BARRIER_CONDITIONS_SATISFIED_PENDING_CONTROL_ROOM_READBACK`;
- every other combination yields
  `CLOSED_PENDING_CONTROL_ROOM_MECHANICAL_READBACK`;
- report substance is not placed into the mechanical handoff (strict
  allowlist; any member whose basename ends with the report-name suffix
  is structurally refused);
- the future mechanical handoff path is exactly
  `/home/isa/audit-council-dev/AUCDEV-023-S1-FIRSTPASS-EXEC-20260922-04-MECHANICAL-HANDOFF.tar.gz`.

## 7. Preparation test evidence (FINDING_TEXT — recorded from the final clean run)

- source/live-state checks = **120/120 PASS**
- launcher-preparation tests = **36/36 PASS** (P1–P34 + P28 + SYNTAX)
- py_compile = PASS; bash -n = PASS (rc 0); zsh -n = PASS (rc 0)

The final clean tests establish: successor source identities and modes
exact; current deployed generation classified as expected historical
EXEC-03; future backup absent; successor A/B roots absent; synthetic
atomic deployment works; existing backup refuses; destination drift
refuses; A failure blocks B; A REPORT_INVALID blocks B; conforming A
permits exactly one B path; both conforming yields only mechanical
barrier-satisfied state; wrapper mutation/symlink/root execution
refused; credential plaintext ordering occurs only after verified
non-dumpable state; no substantive report bytes enter the handoff; no
retry surface exists.

## 8. Preparation incident (FINDING_TEXT — recorded verbatim, NOT concealed)

```
AUCDEV023-CR-S1-EXEC04-PREP-RB-001 =
REAL_SUCCESSOR_ATTEMPT_NAMESPACE_TRANSIENTLY_MUTATED_DURING_PREPARATION_TEST

Classification:

HARNESS / PROTOCOL DEFECT
/ PREPARATION TEST CONFINEMENT VIOLATION
/ OBSERVED FACT
/ EMPTY_SCAFFOLD_ONLY
/ RESTORED
/ NO_ACCOUNTING
/ NO_CREDENTIAL_READ
/ NO_GATE_OR_AUDITOR_EXECUTION
/ NO_AUTHORITY_CONSUMPTION
/ FINAL_PRISTINE_PRECONDITION_REESTABLISHED
/ NON_BLOCKING_FOR_ACCEPTED_LAUNCHER_BYTES
```

Exact incident: a mis-wired P31 preparation-test context used the real
attempts root and `prepare_attempt` created
`/home/isa/aucdev023-s1-prep002-rem002/attempts/evt-79182989824ce966-B-01/`
containing exactly three empty directories (`accounting/`,
`custody-out/`, `staging/`). No regular files existed. No AccountingStore
was created. No credential bytes were accessed. No runtime gate was
executed. No auditor process was executed. No authority was consumed.
The empty scaffold was removed. The final clean suite subsequently
verified: A root ABSENT, B root ABSENT, successor stray entries = [].
The test harness was hardened to assert its attempts_root is under the
synthetic temporary root and NOT under the real DEPLOY_ROOT before
`prepare_attempt` can be reached.

This incident is NOT erased or hidden. The preparation session is
therefore NOT described as having performed zero real-namespace
mutation — it DID perform this transient namespace mutation. This
publication session independently re-verified read-only that the real
attempts root currently contains ZERO `evt-79182989824ce966*` entries
(the pristine precondition holds). The preparer-side incident record
(handoff member `02-preparation-incident-record.json`, internally
labelled `AUCDEV023-EXEC04-PREP-INCIDENT-001`) carries the same facts.

## 9. EXEC-04 authority state (FINDING_TEXT)

- Authority: `AUCDEV-023-S1-FIRSTPASS-EXEC-20260922-04`
- Event: `evt-79182989824ce966`
- A: `evt-79182989824ce966-A-01`
- B: `evt-79182989824ce966-B-01`
- Execution authority remains **GRANTED BY OPERATOR but NOT YET
  EXERCISED**.
- Model engagement accounting remains **0 / 2**.
- No GATES_PASSED. No CONSUMED_PRE_EXEC. No EXEC_ATTEMPTED. No
  REPORT_FROZEN. No REPORT_INVALID runtime event.
- `exec04-run-evidence/` does not exist (the driver's evidence base was
  never created) — verified read-only by this session.
- Historical EXEC-03 authority
  `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-03` remains CLOSED /
  NO FURTHER EXECUTION / NO RETRY / NON-TRANSFERABLE.

## 10. Resulting state (FINDING_TEXT)

- `evt-79182989824ce966` = PREPARED IDENTITY ONLY
- A: `evt-79182989824ce966-A-01` = PREPARED IDENTITY ONLY / NOT STARTED
- B: `evt-79182989824ce966-B-01` = PREPARED IDENTITY ONLY / NOT STARTED
- Model engagements: 0 / 2. Barrier: NOT STARTED. Real execution:
  NOT YET INVOKED. Qualification: NONE. Installation: NONE.
- The currently deployed event generation at
  `/home/isa/aucdev023-s1-prep002-rem002/event/` remains the historical
  EXEC-03 generation (gate `27948980…` re-hashed by this session); the
  future backup `event.backup.pre-successor-event` remains ABSENT; the
  successor generation will be deployed by the driver itself under the
  EXEC-04 invocation.
- AUCDEV-023: P1 / READY / NOT DONE.

## 11. Publication discipline (OBSERVED_FACT)

Exactly ONE bounded fast-forward publication commit over exact base
`d471fed7e046a25afeb8214ce1070032735db28e`; sole parent that commit; no
merge/rebase/amend/reset/force/tag. Exactly three changed paths: NEW
`docs/chatgpt-project/AUCDEV-023-S1-EXEC04-OPERATOR-LAUNCHER-PREPARATION-READBACK.md`;
MODIFIED `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`; MODIFIED
`docs/chatgpt-project/AUCDEV-BACKLOG.md`. NO bootstrap-supervisor
source/test/MANIFEST change; NO qh or skill change; NO
ARCHITECTURE-SUMMARY change; NO historical canonical report rewritten;
NO qualification-history row added; the restored CURRENT append-only
historical block preserved byte-for-byte (no
compaction/deduplication/rewriting — current-facing fields + next-action
rotation + one new dated record only); pre-existing smoke-fixture
gitlink drift and evidence directories preserved unstaged; the untracked
launcher artifacts (driver/wrapper/test-suite/prep-evidence/handoff)
remain untracked.

## 12. Generated-LAST small publication handoff (OBSERVED_FACT)

Exactly ONE SMALL `.tar.gz` (or `.zip`) handoff is generated LAST, after
the push, containing: the new readback record; the resulting CURRENT;
the resulting BACKLOG; the exact publication diff; commit metadata;
GitHub readback; protected-tree verification; the launcher identity
inventory; the predecessor diff verification (27 + 2 hunks, archived ==
independently generated); the 120/120 + 36/36 result summary; the
incident record; the authority-state inventory; and the reference to the
preparation handoff SHA
`6a91482058413f5120c7b8c0ab2e579471d4abb847f04bc1961297d36a790c1e` —
with exactly one SHA256SUMS covering every regular payload file except
itself; credentials, report substance, provider logs and unrelated
evidence excluded; the 74,286 B preparation handoff NOT duplicated.
Nothing mutates afterward.

## 13. Next action (EXACTLY ONE)

**HUMAN OPERATOR DIRECT EXEC-04 INVOCATION USING THE PINNED ONE-COMMAND
WRAPPER, WITH NO INFERENCE-CAPABLE CONTROLLER ON THE RUNTIME PATH.**

Exact command:

```
cd /home/isa/audit-council-dev
./run-aucdev023-firstpass-exec04.sh
```

This command is recorded as the next action only. This publisher did
NOT run it. This record confers no execution authority beyond the
operator's existing `AUCDEV-023-S1-FIRSTPASS-EXEC-20260922-04` and no
qualification/installation.
