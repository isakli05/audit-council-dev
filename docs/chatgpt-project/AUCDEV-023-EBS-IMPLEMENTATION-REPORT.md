# AUCDEV-023 — External Bootstrap Supervisor (EBS) Implementation Report

| Field | Value |
|---|---|
| Status | **`AUCDEV_023_EBS_IMPLEMENTATION = IMPLEMENTED_CANDIDATE / AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK`** — a bounded implementation of the operator-adopted R1 governance now exists under `bootstrap-supervisor/**`; it is NOT Control Room accepted, NOT an event package, NOT execution-authorized, NOT qualified, NOT installed, and supports NO real provider/event. Implementation claims are NOT audit truth. |
| Session class | BOUNDED ZERO-PROVIDER IMPLEMENTATION SESSION — deterministic tests + implementation evidence publication ONLY; NOT Auditor A/B, NOT the Control Room decision-maker; no event-package preparation, no real networked auditor boundary package, no GATE-W′ rehearsal, no real credentials, no provider/model/auditor execution, no `/audit-council`, no bootstrap event instantiation, no qualification, no installation, no frozen-target mutation |
| Operator authority | Operator tasking (2026-09-19) authorizing ONLY: bounded implementation of the adopted AUCDEV-023 External Bootstrap Supervisor; deterministic zero-provider tests; implementation evidence publication. All test credentials are clearly synthetic and inert; all launched test children are local deterministic fixtures under `bootstrap-supervisor/tests/fixtures/**`; model/provider engagements = ZERO |
| Exact implementation base | `f47c6d24f154d73881768c9039646763ea36f12a` (tree `9b966d47ef022c410c9133054851c8c2cddba231`; sole parent `d11665d789978ebb1c4fecf73fbbdb0e06eb3c55`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this session's bootstrap and re-resolved EXACT immediately before staging; THIS implementation publication is the sole commit ahead of that base |
| Governing records read at the exact base | CURRENT-STATE, BACKLOG, CONTROL-ROOM-RUNBOOK, PROJECT-UPDATE-PROTOCOL, ARCHITECTURE-SUMMARY, the governance ADOPTION record, the design REVISION record, and the design-revision READBACK record. Frozen qh source (`qh/custody.py`, `qh/statemachine.py`, `qh/tests/test_custody.py`, `qh/tests/test_statemachine.py`) was read at exact `d4d584ffa47ad2848268ba947247f81a845b2322` as DESIGN/BEHAVIORAL REFERENCE ONLY — never imported, never copied wholesale, never executed |
| Frozen target (unchanged, EXACT) | `isakli05/audit-council-dev` @ `d4d584ffa47ad2848268ba947247f81a845b2322` (root tree `1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7`; qualification-harness tree `5b8d5e5465923740470ff63ed9b8683f257a3787`; skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`) — verified EXACT at bootstrap and at pre-commit; `git diff d4d584ff… HEAD -- qualification-harness skill` is EMPTY |
| Qualification / installation | qualification NONE / installation NONE |

Claim classes: `OBSERVED_FACT` (mechanically observed this session),
`DESIGN_FACT` (content of the adopted governance records), `IMPLEMENTED`
(what this candidate's code does, evidenced by the deterministic battery).

---

## 1. Confirmed governing start state (OBSERVED_FACT)

All task-mandated start-state facts were confirmed before implementation:
AUCDEV-023 = P1/READY; governance = ADOPTED_BY_OPERATOR /
GOVERNANCE_POLICY_ONLY / NOT_IMPLEMENTED / NOT_EXECUTION_AUTHORIZED; R1 =
CONTROLLERLESS / PROCESS-BOUND / TARGET-INDEPENDENT / ONE-SHOT;
EBS_IMPLEMENTATION = NOT_STARTED / NOT_AUTHORIZED at base (no
`bootstrap-supervisor/**` existed); EVENT_PACKAGE_PREPARATION NOT_STARTED /
NOT_AUTHORIZED; BOOTSTRAP_EVENT NOT_INSTANTIATED; GATE_W_PRIME REQUIRED /
UNPROVEN; REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION UNPROVEN /
EVENT_PREPARATION_GATE; INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED;
qualification NONE; installation NONE; frozen target EXACT.

## 2. Authority scope actually exercised (OBSERVED_FACT)

Implementation under `bootstrap-supervisor/**` + the bounded repository
records (§4). NOT done, by design and by refusal: no event-package
preparation; no real networked boundary; no GATE-W′ rehearsal; no real
credentials (one synthetic inert literal only, confined to
`tests/conftest.py`); no provider/auditor invocation; no `/audit-council`;
no event instantiation; no qualification; no installation; no frozen-target
mutation. Pre-existing unrelated working-tree state (`smoke-fixture` /
`smoke-fixture-103` stat-cache drift with byte-identical content, untracked
`aucdev019-evidence/`) was preserved unstaged and untouched.

## 3. Architecture / module inventory (IMPLEMENTED)

Production package `bootstrap-supervisor/ebs/` — Python 3 standard
library ONLY + Linux kernel primitives; no plugin/extension surface;
unknown binding fields fail closed.

| Module | Physical lines | Responsibility |
|---|---|---|
| `binding.py` | 273 | policy id + frozen-target constants; strict JSON load (duplicate-key/non-finite refused); exact-key schema validation; role/adapter/launcher/gate enumerations; attempt/event and output-name derivation rules; canonical digest |
| `statemachine.py` | 74 | one-shot attempt states; absorbing terminals; no reset/retry/mint interfaces; `valid_path` for chain replay validation |
| `accounting.py` | 244 | operator-custodied hash-chained JSONL store; dirfd-safe opens with `O_NOFOLLOW`/`O_EXCL`; ownership/mode validation; fsync(file)+fsync(dir) per append; attach-time tamper/truncation/chain/sequence validation; reuse refusal |
| `custody.py` | 211 | prctl non-dumpable; source-kind discipline (pipe / fully sealed memfd only); bounded read; EBS-owned four-seal memfd; boolean-only `contains` screen; documented-once UAPI constants |
| `launch.py` | 345 | `open_verified_launcher` (open→regular-check→hash open fd); execveat(AT_EMPTY_PATH)/fexecve fd exec; child fd contract (fd 3 credential, fd 4 CLOEXEC exec-fail pipe, stdout metadata pipe); `LaunchGrant` single-use object; `Supervisor` orchestration with pre-fork re-hash |
| `reportcustody.py` | 118 | missing-stays-missing; symlink/oversize refusal; pre-publication credential screen (boolean only); O_EXCL freeze, fsync, chmod 0444, recorded SHA-256/size/mode |
| `cli.py` | 75 | inspection-only CLI (`validate-binding`, `inspect-accounting`); no authority operations |
| `__init__.py` | 17 | package identity/version |
| **Total production LOC** | **1357** | bound: ≤ ~1500 (SATISFIED) |

Tests: `bootstrap-supervisor/tests/` (7 files + conftest + 2 inert fixtures),
133 deterministic tests. `MANIFEST.json`: 19 files, per-file SHA-256+size,
policy id, frozen target, runtime-dependency statement, qualification_claim
NONE (self-excluded to avoid recursion).

## 4. Changed paths (this publication)

NEW `bootstrap-supervisor/**` (20 files) · NEW THIS report ·
`AUCDEV-CURRENT-STATE.md` (bounded) · `AUCDEV-BACKLOG.md` (bounded) ·
`AUCDEV-ARCHITECTURE-SUMMARY.md` (bounded §"AUCDEV-023 exceptional
auditor-bootstrap governance" factual update ONLY — the product/runtime
source baseline at the top of that document is UNCHANGED).
NOT modified: `qualification-harness/**` (tree `5b8d5e54…` UNCHANGED),
`skill/**` (tree `c792933a…` UNCHANGED), the runbook, the adoption record,
the design/revision/readback records, `AUCDEV-QUALIFICATION-HISTORY.md`
(no qualification/installation event — NOT_APPLICABLE per precedent),
Project Instructions, historical AUCDEV-010 records, the frozen target.

## 5. Binding schema (IMPLEMENTED)

Top-level keys exactly: `policy_id`, `event_id`, `auditor_role`,
`attempt_id`, `target`, `common_evidence_manifest_digest`,
`prompt_contract_digest`, `boundary_launcher` {identity, sha256},
`auditor_identity` {provider_role, adapter_id}, `output_identity`
{kind, name}, `gate_evidence` {7 gates}. Policy id:
`AUCDEV-023-R1-CONTROLLERLESS-PROCESS-BOUND-TARGET-INDEPENDENT-ONE-SHOT`.
Target must equal the frozen five-field identity EXACTLY. Roles:
AUDITOR_A/AUDITOR_B; provider roles and adapters per-role consistent
(design-named `claude_firstparty_oauth_v1` / `codex_chatgpt_oauth_v1`
plus the `synthetic_inert_local_v1` test-only adapter). Launcher ids:
`NETWORKED-BOUNDARY-LAUNCHER-V1` / `INERT-LOCAL-FIXTURE-LAUNCHER-V1`.
Event ids `evt-<16 hex>`; attempt ids `<event>-<A|B>-01`; output name
`<attempt>.first-pass-report.json`. Every gate must carry PASS status +
SHA-256 evidence + size + matching role/attempt; the COMMON_EVIDENCE_PARITY
gate evidence digest MUST equal the declared common-evidence manifest
digest. Unknown keys, wrong types, malformed SHAs, non-finite JSON
constants, duplicate keys: refused.

## 6. State machine + one-shot enforcement (IMPLEMENTED)

States PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED →
(REPORT_FROZEN | REPORT_MISSING | REPORT_SCREEN_FAIL) → TERMINAL, with
TERMINAL_PREEXEC_STOP reachable from PREPARED/GATES_PASSED and absorbing
(as is TERMINAL). No reset/retry/mint API exists (statically asserted).
Primary launch authority = in-process `LaunchGrant` (single-use,
non-exportable, no token bytes) + state-machine control flow + the
Supervisor's state precondition; the accounting file is evidence and
refusal, not authority. A second `execute` is refused twice over (dead
grant AND state != CONSUMED_PRE_EXEC); a forged grant is refused by state.

## 7. Atomic consumption order + accounting (IMPLEMENTED)

`consume()`: GATES_PASSED precondition → append CONSUMED_PRE_EXEC (write →
`fsync(file)` → `fsync(dir)`, inside append) → state transition → grant.
Only then does `execute()` become reachable (grant + state). Crash after
consumption leaves durable CONSUMED evidence; restart `attach` refuses
(CONSUMED/EXEC/REPORT_*/TERMINAL* all non-resumable; only
PREPARED/GATES_PASSED chains may resume). Hash-chained records
(seq/state/binding_digest/prev/ts/pid); tamper, truncation, seq gaps,
non-canonical lines, binding mismatch, symlinked/FIFO records, unsafe
custody dir (owner≠euid, group/world-writable), unsafe record mode — all
refused. Narrow claim held: no protection against operator/root rewrite is
claimed; the audited target/boundary child have no mutation path, and
restart semantics are mechanically checked.

## 8. Verify→exec identity (IMPLEMENTED)

`open_verified_launcher`: open with O_NOFOLLOW → fstat regular-file →
SHA-256 of the ALREADY-OPEN fd → compare → seek 0 → keep fd open.
`execute` re-hashes the held fd immediately before fork (same-inode drift
after consumption fails closed). The child execs THE OPEN FD via
`execveat(fd, "", AT_EMPTY_PATH)` (syscall 322 x86_64 / 281 aarch64;
fexecve fallback only on ENOSYS; otherwise fail closed — never a pathname
re-open). Proven by tests: directory-entry substitution to a different
inode still runs the VERIFIED bytes (variant A), and same-inode drift is
refused pre-fork.

## 9. Credential custody (IMPLEMENTED)

Source discipline: pipe (S_ISFIFO) or memfd with all four seals
(`/proc/self/fd` link discrimination, never an fcntl guess); ordinary
files, sockets, directories, unsealed and partially sealed memfds refused;
length window 1..65536 enforced. `PR_SET_DUMPABLE=0` established and
kernel-verified (PR_GET_DUMPABLE) BEFORE any read (order-observing test).
Custody memfd created `MFD_CLOEXEC|MFD_ALLOW_SEALING` (raw syscall —
`os.memfd_create` is absent on Python 3.11; constants defined once,
sourced from UAPI headers, kernel-verified via F_GET_SEALS), sealed with
F_SEAL_SEAL|SHRINK|GROW|WRITE. Metadata = role + length only; no plaintext
attribute exists; `contains()` screens in memory and returns a boolean
only. Transfer to the child ONLY by fd inheritance at fixed fd 3
(CLOEXEC cleared exactly there); the exec-fail pipe is CLOEXEC; all other
fds closed in-child via `/proc/self/fd` sweep. Never argv/env/file/log/
hash. UAPI constants: F_ADD_SEALS 1033, F_GET_SEALS 1034, seals
0x01/0x02/0x04/0x08 (defined once in `custody.py`, documented, kernel-tested).

## 10. Report custody (IMPLEMENTED)

Missing staging → REPORT_MISSING (stdout/stderr NEVER substituted —
tested with stdout present). Symlink staging refused; oversize refused;
credential-contaminated report → REPORT_SCREEN_FAIL with staging removed,
NO hash recorded, boolean classification only; clean report → O_EXCL
freeze under operator-custodied output dir (validated like the accounting
root), fsync, chmod 0444, recorded SHA-256/size/mode, then TERMINAL.
Existing output path never overwritten.

## 11. Test inventory and results (OBSERVED_FACT)

`pytest -q bootstrap-supervisor/tests` → **133 passed, 0 failed**
(Python 3.11.15 + pytest 9.1.1 via `uv run --no-project --with pytest`):
binding 42 (36-case refusal matrix + strictness), statemachine 20,
accounting 22, custody 17, launch 13, report 9, static 10.
`python3 -m compileall bootstrap-supervisor/ebs` → exit 0 (host 3.14.7).
CLI smoke: validate OK (exit 0) + wrong-policy refusal (exit 2).
TDD discipline: the battery was written FIRST against the designed
contract and observed failing (module-absent collection error), then the
implementation was driven to green; subsequent defects found by the
battery (memfd_create absence, sealed-source read offset, fd-listing race,
env coercion) were fixed in implementation/tests, not by weakening any
invariant.

## 12. Negative controls (all tested, fail-closed)

Wrong target (all five fields), unknown/missing keys, malformed SHAs,
wrong policy/role/event/attempt-relationship, wrong launcher identity,
role/adapter/provider mismatches, wrong output identity, missing/FAIL/
UNKNOWN/malformed gate evidence, parity-digest inconsistency, duplicate
JSON keys, non-finite constants; illegal transitions, absorbing states,
no-reset/no-retry/no-mint, consume-before-gates, launch-before-durable-
record, duplicate launch (dead + forged grant), restart-after-consumed/
terminal, tampered/truncated/seq-gapped chains, duplicate record creation,
symlink/FIFO/unsafe-mode/unsafe-dir records, binding mismatch, world/group-
writable custody dirs; ordinary-file/unsealed/partially-sealed/socket/
directory/empty/oversize credential sources, non-dumpable failure,
non-dumpable-before-read ordering, teardown closes fd, credential absent
from outputs/logs/accounting; wrong launcher digest pre-fork, directory-
entry substitution, same-inode post-consumption drift, credential not in
argv/env, intended fd inherited, unintended fds not inherited, exec
failure honestly recorded; missing report stays missing, no overwrite,
symlink staging, contaminated-report pre-publication rejection, size
limit, unsafe output dir.

## 13. Zero-provider attestation (OBSERVED_FACT — what was enforced/observed)

Mechanically enforced by static tests over ALL `bootstrap-supervisor/**.py`:
no `claude`/`codex` token (word-boundary, case-insensitive; design-named
adapter ids are underscore-joined and carry no standalone token), no
`/audit-council` invocation token, no import of socket/ssl/http/urllib/
requests/subprocess/asyncio anywhere in the package, no qh/skill/
qualification-harness reach, production imports stdlib-allowlisted.
Runtime-observed: every launched child is
`tests/fixtures/inert_boundary_launcher_{a,b}.py` (unmistakable marker
`EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER`); the single
credential literal exists only in `tests/conftest.py` and appears in no
other file under `bootstrap-supervisor/**` or `docs/chatgpt-project/**`
(grep evidence). Honest limit (recorded, not overclaimed): ordinary unit
tests cannot prove absence of all possible networking; the attestation is
the enforced scan + observed execution set above. Provider/model/auditor
executions = ZERO; engagements under this policy = 0.

## 14. qh regression (OBSERVED_FACT)

`pytest -q qualification-harness/tests` → **221 passed, 0 failed**
(24.9 s; same uv/pytest environment). The suite has grown from its
historical 84-test first-run record via later authorized remediation
publications; 221/221 pass with NO environment-specific external failure
to classify. qh and skill trees are byte-identical to the frozen target
(`git diff d4d584ff… HEAD -- qualification-harness skill` EMPTY;
pre-commit re-verified). No qh code was read for execution, imported, or
modified; frozen reference files were read via `git show` only.

## 15. Manifest identity (OBSERVED_FACT)

`bootstrap-supervisor/MANIFEST.json` — 19 payload files (excludes the
manifest itself and caches), per-file SHA-256 + byte size; records policy
id, frozen target identity, implementation status IMPLEMENTED_CANDIDATE,
runtime dependency statement, qualification_claim NONE. Manifest file
SHA-256: `ef06614d968ef85f37023cdbc350b1fa768a8c443a24f4451aaf68633192edd4`.
A static test re-derives every entry from shipped bytes (drift-detecting).

## 16. Known residuals and honest limits

1. EBS is trusted BEFORE any independent review — inherent to the adopted
   minimal-bootstrap-TCB basis; this publication claims nothing stronger.
2. Same-UID host residual: any same-UID process can SIGKILL the EBS
   (denial only, never authority gain); operator/root can rewrite
   accounting (not protected, not claimed).
3. Child env gains `LC_CTYPE` from the interpreter's C-locale coercion
   (PEP 538) — interpreter-injected, non-secret, disclosed.
4. `fexecve` fallback path is implemented for ENOSYS-only; on this host
   the execveat syscall is exercised directly (x86_64 322).
5. If fork itself fails after grant use, the grant is dead with no exec
   attempt — fail-closed dead end by design (no auto-replacement).
6. The enforcement interface requires PASS gate EVIDENCE; it cannot
   evaluate whether a future evidence artifact is itself sound — that is
   the readback's and GATE-W′'s job.
7. Exec-failure after consumption consumes the attempt honestly
   (EXEC_ATTEMPTED recorded; per adopted §28 both counters fail closed
   toward consumed when inference status is uncertain).

## 17. Event-preparation gates still UNPROVEN (explicit)

```
GATE_W_PRIME                            = REQUIRED / UNPROVEN
REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION   = UNPROVEN / EVENT_PREPARATION_GATE
EVENT_PACKAGE_PREPARATION               = NOT_STARTED / NOT_AUTHORIZED
BOOTSTRAP_EVENT                         = NOT_INSTANTIATED
NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE  = disclosed residual (design §19)
```

No test in this package claims any real GATE-W′ or client-isolation proof;
all gate evidence in tests is deterministic synthetic data.

## 18. Deviations from the adopted design (bounded, none weakening authority)

1. `REPORT_SCREEN_FAIL` is implemented as an explicit state (named by the
   implementation authority §20; not in the design §9 minimum list) — it
   transitions only to TERMINAL.
2. Adapter enumeration includes `synthetic_inert_local_v1` alongside the
   two design-named real adapter ids (no real adapter exists; the inert id
   is the only one exercisable by this task's zero-provider tests; any
   future real use requires the separately authorized event package).
3. Exact attempt-id/output-name derivation formats (`<event>-<A|B>-01`,
   `<attempt>.first-pass-report.json`) are new mechanical conventions
   implementing the design's "role/attempt-derived output identity".
4. `boundary_launcher` is {identity, sha256} (the implementation authority
   distinguishes identity refusal from digest refusal; the design named
   identity as the SHA-256 — both are bound and enforced).
5. The CLI is inspection-only: exposing authority operations as CLI
   invocations would contradict the adopted non-exportable-authority rule.
6. Design §6.2 "EBS refuses to run if its own live bytes do not match its
   recorded manifest (self-verification at start)" is implemented as the
   static manifest test + publication-time manifest freeze; a runtime
   self-check inside `ebs` is deferred to the event-package stage where
   the EBS package identity is frozen per event (recorded as a residual
   for the readback, not silently dropped).

## 19. State after this publication

```
AUCDEV-023                                = P1 / READY (NOT DONE)
EBS_IMPLEMENTATION                        = IMPLEMENTED_CANDIDATE
                                            / AWAITING_CONTROL_ROOM_READBACK
INDEPENDENT_HARNESS_AUDIT                 = BLOCKED_PENDING_EBS_IMPLEMENTATION_READBACK
                                            _AND_EVENT_PREPARATION
                                            _AND_SEPARATE_EXECUTION_AUTHORITY
INDEPENDENT_AUDITOR_PROVENANCE_GATE       = NOT_SATISFIED
EVENT_PACKAGE_PREPARATION                 = NOT_STARTED / NOT_AUTHORIZED
BOOTSTRAP_EVENT                           = NOT_INSTANTIATED
GATE_W_PRIME                              = REQUIRED / UNPROVEN
REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION     = UNPROVEN / EVENT_PREPARATION_GATE
MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY = 0
qualification                             = NONE
installation                              = NONE
```

Next action EXACTLY ONE: **INDEPENDENT CONTROL ROOM READBACK OF THE
AUCDEV-023 EBS IMPLEMENTATION.** No event-package preparation follows
automatically; no execution authority is requested or implied.
