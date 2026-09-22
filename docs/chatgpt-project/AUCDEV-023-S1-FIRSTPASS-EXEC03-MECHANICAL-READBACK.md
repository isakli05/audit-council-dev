# AUCDEV-023 — S1 FIRST-PASS EXEC-03 MECHANICAL READBACK (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL publication of the ALREADY-PERFORMED operator EXEC-03 execution event and the ALREADY-DECIDED Control Room mechanical disposition, plus this session's bounded mechanical diagnostic reproductions; a RECORD PUBLISHER / BOUNDED MECHANICAL DIAGNOSTIC REPRODUCER ONLY — NOT the Control Room decision-maker, NOT a remediation implementer, NOT an independent auditor, NOT Auditor-A/B, NOT an execution controller, NOT an execution/qualification/installation authority; NOT authorized to remediate anything, mint any event or attempt, replace or reconcile anything, launch Auditor-B, retry Auditor-A, or qualify/install anything; ZERO provider/model/frontier executions, ZERO Auditor-A/B/`/audit-council` executions, ZERO real credential reads (no credential path opened), ZERO new real attempt consumption, ZERO AccountingStore creation, ZERO GATES_PASSED/CONSUMED_PRE_EXEC, ZERO package/binding/manifest/launcher/runtime-gate/EBS/qh/skill/frozen-target/event/attempt mutation, NO wrapper executed, NO deployment, NO retry; Auditor-A substantive report content NEVER read, summarized, evaluated or published (deterministic scripts emitted ONLY SHA-256/size/key sets/identity fields/type census/severity values/coverage status literals/validator exit+envelope+error) |
| Date | 2026-09-22 (Europe/Istanbul) |
| Execution authority (historical event under readback) | `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-03` — now TERMINAL: NO FURTHER EXECUTION / NO SAME-ATTEMPT RETRY / NON-TRANSFERABLE; historical authority `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-02` remains CLOSED / NON-TRANSFERABLE |
| Event / attempts | `evt-31f2a399b3a7e11d` / Auditor-A `evt-31f2a399b3a7e11d-A-01` / Auditor-B `evt-31f2a399b3a7e11d-B-01` |
| Canonical mechanical handoff | `/home/isa/audit-council-dev/AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-03-MECHANICAL-HANDOFF.tar.gz` outer SHA-256 `c4cd35d62e6fe9cdd9adb0174563509512a10fbeb43d56bcf0b3a82a09e8723f`, 34255 B (integrity re-verified read-only EXACT by THIS session — §3) |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |

Claim classes: `OBSERVED_FACT` (mechanically observed/reproduced by this
session), `FINDING_TEXT` (Control Room disposition/finding text, recorded
verbatim), `REQUIREMENT`. §§13–14 are the CONTROL ROOM's disposition
recorded EXACTLY; this publication session neither adjudicates nor amends it.

---

## 1. Live bootstrap (OBSERVED_FACT)

Live `refs/heads/master` of `isakli05/audit-council-dev` resolved at bootstrap
(fetch + `git rev-parse origin/master`) EXACTLY the mandated base: commit
`e7bff48c91686c74f72e81d42497cf72caf35bcd`; tree
`48e5c116df0cdd5bddc9c7664cdcc94db9af13d7`; sole parent
`e2a89aa56257b00e30053536dea8d78828a24af7`. Protected trees verified EXACT
and byte-unchanged through this publication: bootstrap-supervisor
`09f3d6c7ddc00305986cbedad431395c10c95af0`; qualification-harness
`5b8d5e5465923740470ff63ed9b8683f257a3787`; skill
`c792933a862d9a5434681a88d183470dd8b15d2f` (the latter two EQUAL the frozen
audit target `d4d584ffa47ad2848268ba947247f81a845b2322` subtrees). CURRENT-
STATE, BACKLOG, the new-event identity-regen readback, the EXEC02 argv
readback, the Control-Room runbook and the project update protocol were read
at that exact SHA (tracked working tree byte-identical to the base). The live
EBS source needed for report-validation mechanics was read at the exact base
(`bootstrap-supervisor/ebs/launch.py`, `tests/conftest.py`,
`tests/fixtures/inert_validator.py`). No STOP-WITHOUT-MUTATION was required.
Pre-existing smoke-fixture gitlink drift and untracked evidence directories
were observed and preserved unstaged.

## 2. Mechanical handoff integrity (OBSERVED_FACT)

Streaming read-only verification of
`AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-03-MECHANICAL-HANDOFF.tar.gz`:
outer SHA-256 `c4cd35d62e6fe9cdd9adb0174563509512a10fbeb43d56bcf0b3a82a09e8723f`
EXACT; size 34255 B EXACT; census 15 members = 15 regular files; unsafe/
traversal 0; duplicates 0; symlinks 0; hardlinks 0; special 0; exactly one
SHA256SUMS with 14 rows, 14/14 checksum PASS, no unlisted payload, no
listed-but-absent payload. Nothing was extracted to the repository and nothing
executed from the archive; NO substantive report content exists in the
handoff (member set: preflight/source-verification/deployment/deployed-
reverify/attempt-a-summary/barrier-check/authority-summary/chronology JSONs,
README, accounting JSONL, both bindings, both package MANIFESTs). The handoff
members `bindings/binding-auditor-{a,b}.json`,
`manifests/package-auditor-{a,b}-MANIFEST.json` and
`accounting/evt-31f2a399b3a7e11d-A-01.jsonl` are byte-identical (SHA-256
recomputed) to the LIVE deployed bindings/manifests and the LIVE durable
accounting record — the handoff binds to the live execution state.

## 3. Deployment + accepted mechanical execution facts (OBSERVED_FACT + FINDING_TEXT)

DEPLOYMENT VERIFIED COMPLETED: the deployed generation at
`/home/isa/aucdev023-s1-prep002-rem002/event/` IS the exact accepted
new-event generation (every identity independently recomputed EXACT by this
session): Auditor-A MANIFEST `f0e40902…` / package `d142d62c…` / binding file
`387e9597…b`; Auditor-B MANIFEST `49c275d1…` / package `9fd5a36c…` / binding
file `a83f962b…`; prompt contract `e4204e67…` byte-identical at all four
package copies; RESOURCE_GATE `27948980…` (both roles); NETWORK_READINESS
`20f37e91…` (both roles); launcher `2efb6660…` (both roles, byte-identical);
auditor executables identified by hash — A `claude.exe` `15e2d051…`, B
`codex` `3188814c…`; frozen output validator `6aff0e7e…` (both roles);
common-evidence manifest `e5bae461…`; sandbox profiles A `2e8fd257…` /
B `12266b0f…`; native tool wrapper `0ed2ba48…`; probe-true `d3321fd6…`. The
historical EXEC-02 generation is PRESERVED at the fixed EXEC-03 backup
`event.backup.pre-exec03-new-event` (verified: gate `e8f85391…`, historical
contract `7973d643…`, A MANIFEST `45805629…`, B `5c1421ae…` — the EXEC-001-
remediation generation that was deployed at EXEC-02); the older
`event.backup.pre-exec02` remains untouched.

AUDITOR-A DURABLE ACCOUNTING (live record
`attempts/evt-31f2a399b3a7e11d-A-01/accounting/evt-31f2a399b3a7e11d-A-01.jsonl`,
5531 B, SHA-256 `85f7a80b0f427794fdb4532f19e55dd7ff17b962bee5756308e95aa86f2f2c27`,
six records): state sequence EXACTLY `PREPARED` → `GATES_PASSED` →
`CONSUMED_PRE_EXEC` → `EXEC_ATTEMPTED` → `REPORT_INVALID` → `TERMINAL`;
the `GATES_PASSED` record carries the resource-gate result digest under gate
`27948980…` and network-readiness result under `20f37e91…`; the
`CONSUMED_PRE_EXEC` record pins `output_validator_sha256
6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071` with
identity `AUCDEV023-FIRST-PASS-REPORT-VALIDATOR-V1` and prompt-contract
digest `e4204e67…`; the terminal reason is EXACTLY
`REPORT_INVALID: OUTPUT_VALIDATOR_NONZERO_EXIT: exited 120`. AttemptResult
(mechanical summary in the handoff): `returncode = 0`, `exec_failed = false`,
`timed_out = false`, `report_state = REPORT_INVALID`, `report_sha256 = ""`,
`report_size = 0`. Therefore `AUDITOR_A_AUTHORITY = CONSUMED / CLOSED`;
`AUDITOR_A_INFERENCE_CAPABLE_EXEC = OCCURRED`; fail-closed budget charged
`1 / 2`; inference-capable EXEC_ATTEMPTED records = 1.

AUDITOR-B: NOT STARTED — no `evt-31f2a399b3a7e11d-B-01` attempt directory
exists at the launcher root and no accounting record exists (absence
mechanically observed).

BARRIER: `CLOSED_PENDING_CONTROL_ROOM_MECHANICAL_READBACK`. No REPORT_FROZEN
exists. No accepted conforming first pass exists. The remaining numerical 1/2
budget slot confers NO authority to launch B, retry A, or replace either
attempt.

## 4. Report diagnostic artifact — identity and evidentiary limitation (OBSERVED_FACT + REQUIREMENT)

The current staging diagnostic artifact
`attempts/evt-31f2a399b3a7e11d-A-01/staging/evt-31f2a399b3a7e11d-A-01.first-pass-report.json`
has SHA-256 `d62cb6680e00a16224fc77b73233e3c6075be85ef2b84190cbe7a527777efa19`
and size 30713 B — EXACTLY the current Control Room diagnostic copy identity.
Bounded structural census (deterministic scripts; NO substantive prose
emitted): top-level key set exactly {schema, event_id, auditor_role,
attempt_id, target_commit, summary, findings, coverage, residuals,
methodology}; identity fields exact (`schema
AUCDEV-023-FIRST-PASS-REPORT-V1`, `event_id evt-31f2a399b3a7e11d`,
`auditor_role AUDITOR_A`, `attempt_id evt-31f2a399b3a7e11d-A-01`);
`coverage` length 14 with every entry shaped {area, covered, note} and every
`covered` value a JSON STRING `"COVERED"` (string count 14/14, boolean count
0/14); `findings` length 3 with severity VALUES {CRITICAL×1, LOW×2}
(structural validation only — no finding text, evidence, title or
description was read or emitted).

IMPORTANT (REQUIREMENT): the mechanical runtime handoff did NOT record the
invalid snapshot's digest/size, so the current staging artifact is a
POST-RUN DIAGNOSTIC ARTIFACT — NOT CRYPTOGRAPHICALLY BOUND TO THE EXACT
RUNTIME VALIDATOR SNAPSHOT and NOT AN ACCEPTED FIRST-PASS REPORT. Its
evidentiary status must NEVER be upgraded (see finding EXEC03-004). This
publication records its identity only.

## 5. Exact frozen validator + structural diagnostic result (OBSERVED_FACT)

The deployed validator bytes at both
`event/package-auditor-{a,b}/runtime/output-validator.py` hash EXACTLY to
`6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071`, identity
`AUCDEV023-FIRST-PASS-REPORT-VALIDATOR-V1` (also pinned by the live
CONSUMED_PRE_EXEC accounting record). Its structural rule at source line
123–124 is exactly `if not isinstance(item["covered"], bool): raise
ValueError(f"COVERAGE_{index}_COVERED_NOT_BOOL")`. The validator was NOT
changed by this session.

Diagnostic run (exact frozen validator against the current diagnostic
staging artifact, report delivered on fd 3 per the frozen argv contract, with
a WRITABLE diagnostic stderr, outside the real attempt lifecycle, zero
credential / zero provider call / zero AccountingStore / zero network / zero
attempt mutation):

- validator rc = `1` (expected);
- stderr error EXACTLY `VALIDATION_ERROR: COVERAGE_0_COVERED_NOT_BOOL`;
- result envelope: schema `AUCDEV-023-REPORT-VALIDATOR-RESULT-V1`,
  status `FAIL`, event_id `evt-31f2a399b3a7e11d`, auditor_role `AUDITOR_A`,
  attempt_id `evt-31f2a399b3a7e11d-A-01`,
  report_sha256 `d62cb6680e00a16224fc77b73233e3c6075be85ef2b84190cbe7a527777efa19`,
  report_size `30713`.

All 14 coverage entries currently carry the STRING status `"COVERED"` rather
than JSON boolean `true` (their `area`/`note` prose was never printed).

## 6. Prompt contract ↔ validator coverage-type mismatch — EXEC03-003 (OBSERVED_FACT + FINDING_TEXT)

The exact accepted prompt contract (SHA-256
`e4204e673e56d62d4e4ba0aceb44cc5ca599cf2ddb4e774568977544ac3fdd73`, verified
byte-identical at all four deployed package copies; ONLY its report schema
definition was read) specifies:

> `coverage` = "array of {area, covered, note} mapping each review
> requirement above to COVERED or NOT covered"

The prompt contract does NOT specify that `covered` must be a JSON boolean.
The frozen validator DOES require `isinstance(item["covered"], bool)`
(`output-validator.py:123-124`). Control Room classification recorded
verbatim:

```
AUCDEV023-CR-S1-EXEC03-003 =
PROMPT_CONTRACT_OUTPUT_VALIDATOR_COVERAGE_TYPE_MISMATCH
HARNESS / PROTOCOL DEFECT
/ FIRST-PASS STRUCTURAL CONTRACT MISMATCH
/ OPEN
/ BLOCKING REPLACEMENT FIRST-PASS EXECUTION
```

Support: observed fact + contract comparison. It is NOT claimed that
Auditor-A violated an explicitly documented boolean type requirement — the
contract did not state one.

## 7. Single-blocker normalization probe (OBSERVED_FACT)

A TEMPORARY diagnostic copy (in `/tmp`) of the staging artifact was created
with exactly one class of change: for every one of the 14 coverage entries
`"COVERED"` → JSON `true`. Deterministic proof: exactly 14 parsed JSON values
changed; every change is `coverage[*].covered` (diff paths
`$.coverage[0..13].covered`, old JSON type string `"COVERED"` → new JSON type
boolean `true`); parsed equality after normalizing only those fields TRUE; 0
unexpected diffs. The exact frozen validator run on the temporary copy:
rc = `0`, envelope status `PASS`. The temporary copy was then DELETED
(deletion verified); the staging artifact was byte-unchanged before and after
the probe (verified). This establishes: COVERAGE TYPE MISMATCH IS THE ONLY
STRUCTURAL VALIDATOR BLOCKER OBSERVED IN THE CURRENT DIAGNOSTIC ARTIFACT. It
does NOT repair the historical report, does NOT create REPORT_FROZEN, does
NOT revive the consumed attempt, and does NOT authorize substantive use of
the report.

## 8. Validator failure-diagnostic channel defect — EXEC03-001 (OBSERVED_FACT + FINDING_TEXT)

Exact EBS `_gate_child` / `_run_runtime_gate` mechanics verified at the exact
base source: `bootstrap-supervisor/ebs/launch.py:658` opens `/dev/null` with
`os.O_RDONLY`; `_gate_child` (lines 602–604) dup2's that SAME read-only fd
onto child fd 0 AND fd 2; the REAL frozen output-validator writes
`VALIDATION_ERROR: …` to stderr on FAIL (`output-validator.py:165`); writing
stderr to the read-only descriptor causes the Python process to terminate as
exit 120 rather than its intended exit 1; EBS `_run_runtime_gate` (lines
712–715) then records `OUTPUT_VALIDATOR_NONZERO_EXIT: exited 120` instead of
the structural error.

Mechanically REPRODUCED by this session (same frozen validator, same
diagnostic artifact, fd 2 dup2'd from an `os.O_RDONLY` /dev/null — the exact
EBS child shape): validator rc = `120`, NO result envelope emitted, and the
`VALIDATION_ERROR: COVERAGE_0_COVERED_NOT_BOOL` detail completely masked —
versus rc = `1` with the error detail visible under a writable stderr (§5).
Control Room classification recorded verbatim:

```
AUCDEV023-CR-S1-EXEC03-001 =
OUTPUT_VALIDATOR_STDERR_CHANNEL_MASKS_VALIDATION_FAILURE_DETAIL
HARNESS / PROTOCOL DEFECT
/ VALIDATOR FAILURE-DIAGNOSTIC CHANNEL DEFECT
/ OPEN
```

Important nuance (FINDING_TEXT): merely changing `/dev/null` from read-only
to writable would change the observable rc-120 behavior, but EBS currently
discards validator stderr anyway. NO remediation is pre-decided by this
publication.

## 9. Real validator negative-path test gap — EXEC03-002 (OBSERVED_FACT + FINDING_TEXT)

Verified at the exact base: the deterministic EBS negative
output-validator lifecycle tests build every synthetic event package's
`runtime/output-validator.py` from `tests/fixtures/inert_validator.py`
(`tests/conftest.py:327-333`), NOT the real frozen validator. The inert
fixture's negative modes (`nonzero` → rc 3, FAIL → rc 1, `malformed`,
`mismatch-sha`, `mismatch-size`, `wrong-context`, `hang`) never write
`VALIDATION_ERROR: …` to stderr on schema failure, so they cannot reproduce
the real validator's stderr write and could not detect the EXEC03-001
rc-120 masking. Control Room classification recorded verbatim:

```
AUCDEV023-CR-S1-EXEC03-002 =
REAL_OUTPUT_VALIDATOR_NEGATIVE_PATH_NOT_COVERED_BY_INERT_FIXTURE
COMPLETENESS LIMITATION
/ HARNESS TEST-COVERAGE GAP
/ OPEN
```

The existing tests are NOT invalidated for what they actually test.

## 10. Invalid snapshot provenance gap — EXEC03-004 (OBSERVED_FACT + FINDING_TEXT)

Verified in runtime accounting and source: the durable REPORT_INVALID record
carries `report_sha256 = ""` and `report_size = 0` (observed in the live
accounting record REC[4]: keys = state/terminal_reason only). The EBS
computes a snapshot digest for validator invocation
(`launch.py:1463`, passed as the frozen argv context) but does NOT persist
that invalid snapshot identity in the durable REPORT_INVALID accounting
record (the outcome digest/size fields are initialized empty at lines
1485–1486 and are populated ONLY in the REPORT_FROZEN branch at lines
1526–1534). Therefore the current staging artifact cannot be
cryptographically proven to be the exact immutable snapshot the runtime
validator saw. Control Room classification recorded verbatim:

```
AUCDEV023-CR-S1-EXEC03-004 =
REPORT_INVALID_SNAPSHOT_IDENTITY_NOT_DURABLY_RECORDED
COMPLETENESS LIMITATION
/ FORENSIC-BINDING GAP
/ OPEN
```

This gap does NOT change the valid fail-closed terminality of the attempt.

## 11. CONTROL ROOM DISPOSITION (FINDING_TEXT — recorded verbatim)

```
AUCDEV_023_S1_EXEC03_MECHANICAL_READBACK =
ACCEPTED_MECHANICS
/ DEPLOYMENT_VERIFIED_COMPLETED
/ AUDITOR_A_AUTHORITY_CONSUMED
/ AUDITOR_A_EXEC_ATTEMPTED
/ AUDITOR_A_PROCESS_RC0
/ AUDITOR_A_REPORT_INVALID
/ AUDITOR_B_NOT_STARTED
/ BARRIER_CLOSED
/ MODEL_ENGAGEMENT_BUDGET_CHARGED_1_OF_2
/ AUTHORITY_EXEC03_CLOSED_NO_RETRY
/ STRUCTURAL_REJECTION_TRIGGER_ESTABLISHED
/ CONTRACT_VALIDATOR_COVERAGE_TYPE_MISMATCH_ESTABLISHED
/ VALIDATOR_FAILURE_DIAGNOSTIC_CHANNEL_DEFECT_ESTABLISHED
/ REAL_VALIDATOR_NEGATIVE_PATH_TEST_GAP_ESTABLISHED
/ INVALID_REPORT_SNAPSHOT_BINDING_GAP_RECORDED
/ SUBSTANTIVE_REPORT_FINDINGS_NOT_ADOPTED_OR_EVALUATED
```

This disposition is NOT: a conforming Auditor-A first pass; an audit PASS; a
qualification decision; an installation decision; permission to read/adopt
report substance; permission to run Auditor-B; permission to retry
Auditor-A.

## 12. Resulting state (FINDING_TEXT)

- AUCDEV-023: P1 / READY / NOT DONE.
- EXEC-03 authority `AUCDEV-023-S1-FIRSTPASS-EXEC-20260921-03`: CLOSED /
  NO FURTHER EXECUTION / NO RETRY / NON-TRANSFERABLE.
- Event `evt-31f2a399b3a7e11d`; Auditor-A CONSUMED / EXEC_ATTEMPTED /
  REPORT_INVALID / TERMINAL / NO CONFORMING FIRST PASS; Auditor-B NOT
  STARTED; barrier CLOSED.
- New-event model-engagement accounting: fail-closed charged = 1 / 2;
  inference-capable EXEC_ATTEMPTED records = 1.
- Qualification NONE; installation NONE; replacement first-pass execution
  NOT AUTHORIZED.

## 13. Zero-execution attestation for THIS publication session (OBSERVED_FACT)

Provider/model/frontier inference ZERO; real credential bytes ZERO (no
credential path opened; no custody ingest); Auditor-A/B/`/audit-council`
executions ZERO; `Supervisor.run_attempt` ZERO; AccountingStore creation
ZERO; GATES_PASSED/CONSUMED_PRE_EXEC/EXEC_ATTEMPTED ZERO; real attempt ids
sampled by any gate ZERO; wrapper execution ZERO (the operator's
`run-aucdev023-firstpass-exec03.sh` was NOT executed by this session); the
only executed components were the EXACT frozen output-validator OFFLINE
against (a) the current diagnostic staging artifact twice (writable-stderr
FAIL rc 1; read-only-stderr masked rc 120) and (b) a temporary normalized
diagnostic copy (PASS rc 0, then deleted) — all deterministic, offline,
zero-network, zero-attempt-mutation (the staging artifact verified
byte-unchanged before and after every diagnostic); network activity ZERO
except the git fetch/push of this canonical publication. NO new finding was
minted by this session beyond recording the ALREADY-DECIDED Control Room
dispositions EXEC03-001/-002/-003/-004 verbatim.

## 14. Publication discipline (OBSERVED_FACT)

Exactly 3 changed paths in THIS publication: NEW canonical readback record
(this file) + CURRENT-STATE (header + current-facing fields + dated record +
next-operator-action rotation) + BACKLOG (dated record). ARCHITECTURE-SUMMARY
UNCHANGED (this publication records execution evidence and findings only; no
architecture change occurred). Protected source NOT modified; historical
records NOT rewritten; no qualification-history row added; pre-existing
smoke-fixture gitlink drift + evidence directories (including
`exec03-run-evidence/`, `aucdev023-exec03-prep-evidence/`, the frozen driver
`aucdev023-firstpass-exec03.py` and its wrapper) preserved unstaged. Exactly
ONE append-only fast-forward publication commit whose sole parent is
`e7bff48c91686c74f72e81d42497cf72caf35bcd`. No merge, no rebase, no amend,
no reset, no force push, no tag.

## 15. Generated-LAST publication handoff (OBSERVED_FACT)

A SMALL publication handoff (this record + resulting CURRENT-STATE + BACKLOG
+ exact publication diff + commit metadata + GitHub readback +
protected-tree verification + sanitized mechanical execution inventory +
accounting chronology + the EXEC03-001/-002/-003/-004 finding/disposition
inventory + the deterministic structural-diagnostic result + the
contract-vs-validator structural comparison + the temporary-normalization
diagnostic result + the invalid-snapshot provenance limitation + the binding
reference to the mechanical handoff outer SHA `c4cd35d62e6fe9cdd9adb0174563509512a10fbeb43d56bcf0b3a82a09e8723f`)
is generated AFTER this publication with exactly one SHA256SUMS covering
every payload regular file except itself. It contains NO Auditor-A report
bytes, NO normalized report copy, NO credential bytes or hashes, NO
provider/session private logs, NO peer substantive material, NO secrets, NO
unsafe paths, symlinks, hardlinks, specials or unrelated files. Nothing
mutates afterward.

## 16. Next action (EXACTLY ONE)

CONTROL ROOM VERIFICATION OF THIS EXEC-03 MECHANICAL-READBACK PUBLICATION
BEFORE ANY REMEDIATION AUTHORITY IS GRANTED.

Nothing else follows automatically — this publication confers NO retry, NO
replacement, NO Auditor-B launch, NO substantive-report-use and NO
qualification authority.
