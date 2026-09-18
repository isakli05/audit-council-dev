# AUCDEV-023 — Auditor-Bootstrap Governance Design REVISION (Canonical Record)

| Field | Value |
|---|---|
| Status | **`PROPOSED_REVISION_FOR_CONTROL_ROOM_READBACK`** — NOT ADOPTED, NOT ACTIVE, NOT EXECUTION_AUTHORIZED, NOT QUALIFIED; the RECOMMENDED corrected architecture R1 of THIS revision is a design proposal requiring independent Control Room readback AND separate explicit operator authority before ANY part of it may be implemented or executed |
| Session class | ZERO-AUDITOR / ZERO-PROVIDER-INFERENCE DESIGN SESSION ONLY — NOT Auditor A/B, NOT the Control Room decision-maker, NOT a qualification authority, NOT an installation authority; NO independent auditor execution, NO provider inference, NO `/audit-council`, NO bootstrap event execution, NO qualification, NO installation, NO frozen-target mutation, NO runbook/policy adoption, NO bootstrap package implementation (design only); ZERO provider/model/frontier calls |
| Date | 2026-09-19 (Europe/Istanbul) |
| Operator authority | Operator tasking (2026-09-19) authorizing the AUCDEV-023 auditor-bootstrap governance DESIGN REVISION recorded as the next design objective by the design-readback publication (`5fba5c04…` §17): design/evidence review and canonical design-publication preparation ONLY, bounded to closing `AUCDEV023-CR-BOOTSTRAP-DESIGN-001/-002/-003` by design. NOT authorized: implementation of the external bootstrap supervisor; bootstrap package implementation; event-package preparation; `/audit-council`; auditor/model/provider execution; provider inference; event instantiation; qualification; installation; frozen-target mutation; adoption of this revision as operative policy; execution authority under this design |
| Exact governance base | `5fba5c04e91d30cf83e32ccebf920b84d78a3f38` (tree `f2c6541ef9475da58df84c6742dd2a3e19a5705d`; sole parent `45b9c818d4a324b1c7beb7b0d61460dbbe0762d4`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this session's bootstrap (OBSERVED_FACT; re-resolved EXACT immediately before staging per §37); THIS revision publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Subject | The REQUIRED REVISION of the AUCDEV-023 auditor-bootstrap governance procedure design after its `PARTIALLY_ACCEPTED / REVISION_REQUIRED_BEFORE_ADOPTION` disposition: a corrected architecture whose EXTERNAL BOOTSTRAP SUPERVISOR removes the frozen qh target from authority-root status (CR-BOOTSTRAP-DESIGN-001), mechanically enforces single-use networked launch (CR-BOOTSTRAP-DESIGN-002), and establishes target-independent networked provider credential custody with credential-to-tool isolation (CR-BOOTSTRAP-DESIGN-003) — while preserving every accepted topology/blindness/evidence-parity/output/lifetime design direction |
| Qualification / installation | qualification NONE / installation NONE (unchanged; this revision establishes no new qualification or installation event and grants no authority) |
| Independent harness audit | **BLOCKED_PENDING_AUDITOR_BOOTSTRAP_GOVERNANCE** (unchanged; NOT PASS/FAIL/IN_PROGRESS; no auditor has reviewed the frozen target `d4d584ff…`; this revision does NOT change that state — only Control Room acceptance/adoption of a corrected design PLUS separate operator execution authority can) |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in this session), `OBSERVED_SOURCE_FACT` (mechanically observed in the frozen target source read at its exact SHA), `OBSERVED_DESIGN_FACT` (mechanically observed in the proposed design/readback records), `INFERENCE` (derived, marked), `REQUIREMENT` (task/record-mandated property), `PROPOSAL` (design content of THIS record — carries NO authority until separately adopted).

---

## 1. Live bootstrap and confirmed governing start state (OBSERVED_FACT)

```
live repository : isakli05/audit-council-dev
live branch     : refs/heads/master
live HEAD       : 5fba5c04e91d30cf83e32ccebf920b84d78a3f38   (EXACT, = required base)
live HEAD tree  : f2c6541ef9475da58df84c6742dd2a3e19a5705d   (EXACT)
sole parent     : 45b9c818d4a324b1c7beb7b0d61460dbbe0762d4   (EXACT)
```

All mandated documents were read at that exact SHA (`git show`): CURRENT-STATE,
BACKLOG, CONTROL-ROOM-RUNBOOK, PROJECT-UPDATE-PROTOCOL, the PROPOSED design
record `AUCDEV-023-AUDITOR-BOOTSTRAP-GOVERNANCE-DESIGN.md`, its READBACK
record `AUCDEV-023-AUDITOR-BOOTSTRAP-GOVERNANCE-DESIGN-READBACK.md`, the
independent-auditor-provenance reconciliation READBACK, and the relevant
historical AUCDEV-010 campaign/design records referenced by them. Confirmed
governing start state (OBSERVED_FACT, equal to the task-mandated start state):

```
AUCDEV-023                                = P1 / READY (NOT DONE)
frozen audit target                       = d4d584ffa47ad2848268ba947247f81a845b2322
  target root tree                        = 1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7
  target qualification-harness tree       = 5b8d5e5465923740470ff63ed9b8683f257a3787
  target skill tree                       = c792933a862d9a5434681a88d183470dd8b15d2f
KNOWN_IMPLEMENTATION_BLOCKERS             = CLOSED_AT_CONTROL_ROOM_READBACK_STRENGTH
AUCDEV023_AUDITOR_BOOTSTRAP_GOVERNANCE_DESIGN
                                          = PARTIALLY_ACCEPTED / REVISION_REQUIRED_BEFORE_ADOPTION
INDEPENDENT_AUDITOR_PROVENANCE_GATE       = NOT_SATISFIED (Control Room disposition)
INDEPENDENT_HARNESS_AUDIT                 = BLOCKED_PENDING_AUDITOR_BOOTSTRAP_GOVERNANCE
qualification / installation              = NONE / NONE
```

The three frozen-target tree identities were mechanically re-derived at
`d4d584ff…` this session (root/qh/skill all EXACT). Frozen source facts this
revision depends on were re-verified byte-wise at `d4d584ff…` (read-only;
never executed): `qh/trusted_spec.py` REQUIRES `noegress.required = true` for
every protected launch (template+spec validation, lines 456–458 / 537–539);
`qh/custody.py` accepts operator pipe/memfd sources ONLY (ordinary file
REFUSED), holds bytes in a sealed memfd in a non-dumpable supervisor, never
prints/hashes/logs; `qh/adapters.py` materializes
`codex_chatgpt_oauth_v1` → `auth.json` + minimal config surface inside a
WRITABLE-AT-INIT boundary-private `CODEX_HOME`, and
`claude_firstparty_oauth_v1` → `.credentials.json` mode 0600 inside a
boundary-private `CLAUDE_CONFIG_DIR`; `qh/statemachine.py` states
MINTED→BOUND→PREEXEC_CHECKING→CONSUMED_FOR_LAUNCH→LAUNCHED→TERMINAL with
absorbing TERMINAL_PREEXEC_STOP. Pre-existing unrelated working-tree state
preserved unstaged throughout: `smoke-fixture`/`smoke-fixture-103` gitlink
drift, untracked `aucdev019-evidence/`. (OBSERVED_FACT)

**No auditor/model/provider execution is authorized by anything in this
record.** (REQUIREMENT held)

---

## 2. Scope — exactly three blocking findings; nothing reopened (REQUIREMENT)

THIS revision closes, by design ONLY:

- `AUCDEV023-CR-BOOTSTRAP-DESIGN-001` — TARGET_UNDER_AUDIT_USED_AS_AUTHORITY_ROOT;
- `AUCDEV023-CR-BOOTSTRAP-DESIGN-002` — NETWORKED_LAUNCH_SINGLE_USE_NOT_MECHANICALLY_ENFORCED;
- `AUCDEV023-CR-BOOTSTRAP-DESIGN-003` — NETWORKED_PROVIDER_CREDENTIAL_CUSTODY_NOT_ESTABLISHED.

No broad historical re-search was performed (the expanded `/home/isa` review
result stands as accepted). No accepted topology/blindness/evidence-parity/
output/lifetime decision was reopened absent new evidence (§§24–28, §33–§35
restate them HELD). The original design record and its readback are NOT
modified; the historical chain is preserved append-only.

---

## 3. Fundamental trust rule (REQUIREMENT — governing principle of this revision)

The frozen qh target `d4d584ffa47ad2848268ba947247f81a845b2322` is the
**AUDIT SUBJECT**. Correctness of the qh target is NEVER a precondition for
independently launching, authorizing, credentialing, stopping, or accounting
the external auditors. A malicious or materially defective qh target must not
gain authority over the process that reviews it. Therefore the qh target MAY
be: audit subject; evidence source; rehearsal/test subject; deterministic
signal producer. The qh target MUST NOT be: the authority root; the one-shot
capability minter; the credential custodian; the launch path; the accounting
authority. qh authority/root/supervisor/state-machine behavior may be
examined and exercised as AUDIT EVIDENCE — it is NOT the bootstrap authority
root. (This section closes the trust-role inversion identified by
CR-BOOTSTRAP-DESIGN-001; the replacing mechanism is §4–§6.)

---

## 4. The new minimal bootstrap trust root — AUCDEV-023 EXTERNAL BOOTSTRAP SUPERVISOR (PROPOSAL)

### 4.1 Definition and identity

The **EXTERNAL BOOTSTRAP SUPERVISOR (EBS)** is a deliberately minimal,
operator-controlled, target-independent bootstrap trust root. It is a single
small frozen package (design-only location proposal in §31) whose exact
source/package bytes are frozen, hashed, and Control-Room-readback BEFORE any
event execution authority exists.

The EBS is **NOT**: Audit Council; the qh target or any part of
`qualification-harness/**`; a qualified predecessor; an auditor; a verdict
engine; a model; a general-purpose audit framework; standing infrastructure.

### 4.2 Permitted responsibilities (closed list; nothing else)

1. **Event/package identity validation** — verify the frozen event package
   manifest and every binding field (§26) against the operator-declared
   binding before any gate passes.
2. **Frozen common-evidence binding** — verify the common evidence set
   identity (A=B substantive byte parity) against the frozen manifest.
3. **Auditor-role binding** — bind exactly one auditor role (A or B) per
   supervisor invocation/attempt.
4. **Single-use launch authority** — hold the one-shot launch capability as
   non-exportable process state (§9) and consume it atomically (§10).
5. **Provider credential custody** — hold credential bytes in sealed
   in-memory custody and transfer them ONLY into the final networked boundary
   (§§13–15).
6. **Pre-inference gate result enforcement** — require recorded PASS results
   for every mandatory pre-inference gate (resource, route readiness,
   GATE-W′, identity linter, blindness map, parity) before GATES_PASSED.
7. **Atomic authority consumption** — the GATES_PASSED → CONSUMED_PRE_EXEC
   transition with durable accounting BEFORE any inference-capable exec (§10).
8. **Networked auditor exec** — fork/exec the frozen networked boundary
   launcher (event package) exactly once, from the EBS process itself
   (controllerless, §7).
9. **Report/output custody transition** — freeze the first-pass report at
   process completion (mode 0444, SHA-256, size, move under operator custody),
   enforce missing-report-stays-MISSING, run the credential-leak screen
   (§15.4), and hand off to operator/Control-Room custody.
10. **Mechanical event accounting** — maintain the append-only attempt
    accounting record and the two counters (§29).

The EBS **MUST make no substantive audit finding** — it never evaluates
evidence quality, never classifies findings, never produces or influences a
verdict. Every judgment-bearing stage (first-pass substance, R0, acceptance)
belongs to the auditors, zero-model reconciliation, and the Control Room.

### 4.3 Minimality constraints (REQUIREMENT)

- Single package; target size bound ≤ ~1500 source lines total (excluding
  tests/docs) — small enough to be meaningfully line-by-line reviewable by
  the Control Room and by future auditors as a reviewed TCB artifact.
- Dependencies: Linux kernel primitives (namespaces, mount, memfd/seals,
   fsync, `/proc`), Python 3 standard library ONLY; no third-party packages,
  no network services, no daemons, no persistent state beyond the append-only
  accounting record.
- No plugin/extension points; no configuration parsing beyond the frozen
  binding document; unknown binding fields ⇒ fail-closed refusal.
- The EBS is exercised per event attempt as a ONE-SHOT PROCESS: it starts,
  validates, consumes, launches, freezes, records, and EXITS. It is never
  long-running.

### 4.4 Explicit TCB declaration (REQUIREMENT)

The EBS is trusted code. THIS design does not pretend otherwise and does not
recurse (§6): before any event execution authority, the EBS package must
satisfy the bootstrap root-of-trust conditions of §6, and its full TCB
inventory entry appears in §32. The frozen qh target is NOT in the EBS TCB:
the EBS neither imports, executes, nor trusts qh code at any point (the qh
mechanism patterns it re-instantiates — sealed-memfd custody, process-bound
one-shot authority — are re-implemented as small independent code, because
reusing qh code would re-introduce the circular trust of finding 001).

---

## 5. Closure analysis — CR-BOOTSTRAP-DESIGN-001 (circular trust) → CLOSED_BY_DESIGN

```
Finding ID     : AUCDEV023-CR-BOOTSTRAP-DESIGN-001
Required       : minimal target-independent bootstrap authority plane,
                 outside qualification-harness/**, operator-controlled,
                 frozen before any untrusted controller, no substantive
                 findings, no dependence on installed Audit Council
                 qualification or on qh correctness
Design closure : §§3–6, §7 (R1), §31, §32
```

**How the correction is satisfied**: the authority root for the independent
review of the frozen qh target becomes the EBS — code that is OUTSIDE
`qualification-harness/**` and `skill/**`, operator-controlled, frozen before
any event (and therefore before any controller/auditor process exists),
restricted to the closed responsibility list of §4.2, making no substantive
finding, depending on NO installed Audit Council qualification and on NO qh
behavior. The frozen qh target is demoted to audit subject/evidence/rehearsal
subject (§3). Every property the readback required is structural in the
design: the EBS cannot delegate authority (no mint interface exists — the
operator starts a NEW EBS process per attempt from the frozen package, which
IS the new authority), and the qh target is never on the launch, custody, or
accounting path.

**Residual honestly recorded**: the EBS itself is trusted BEFORE the
independent qh audit (it must be — this is a bootstrap). The design's answer
is explicit minimal-TCB declaration + §6 acceptance discipline, NOT a false
claim that the EBS is independently qualified. The EBS package is itself
included in the future event's common evidence or Control-Room review surface
so that its trustworthiness is examined, at readback strength, before and
again after the event.

**Verdict: CR-BOOTSTRAP-DESIGN-001 = CLOSED_BY_DESIGN** (structural; no qh
dependence anywhere on the authority path).

---

## 6. Bootstrap root of trust — no recursion (REQUIREMENT + PROPOSAL)

The EBS's authority basis is exactly:

**OPERATOR-ACCEPTED MINIMAL BOOTSTRAP TCB.**

Required conditions before ANY event execution authority (all mandatory;
any failure ⇒ the EBS does not run an event):

1. **Exact source/package bytes frozen before event execution** — the EBS
   package (source + tests + manifest) is frozen at an exact commit/bytes;
   no post-freeze mutation is permitted without a new freeze + readback.
2. **Exact package SHA-256 / file manifest** — a per-file SHA-256 manifest
   with total size and file count, recorded in the event package and in the
   Control Room record; the EBS refuses to run if its own live bytes do not
   match its recorded manifest (self-verification at start).
3. **Deterministic mechanical tests** — a self-test battery (positive +
   negative controls; fail-closed negatives mandatory) runnable zero-network
   zero-model; battery identity frozen with the package.
4. **Complete Control Room source/design readback BEFORE execution
   authority** — the full EBS source and THIS design revision are read back
   by the Control Room; adoption is a separate explicit decision; operator
   execution authority is a further separate explicit act.
5. **No model-generated runtime authority** — no LLM output ever feeds the
   EBS's validation, gating, consumption, or accounting decisions; all EBS
   inputs are the frozen binding document, the frozen event package, the
   operator-held credential channel, and OS interfaces.
6. **No dependence on qh correctness** — §4.4.
7. **No dependence on installed Audit Council qualification** — the EBS
   never consults, invokes, or trusts the installed skill or any Audit
   Council runtime.

The bootstrap is thereby EXPLICIT and non-recursive: trust bottoms out at
(operator + kernel + the frozen, reviewable, minimal EBS package), accepted
by recorded operator/Control Room decision — not at a claimed independent
qualification of the EBS. The design does NOT create another general-purpose
audit framework (§4.3 constraints), and the EBS is subject to review again
after the event (its accounting record and behavior are event evidence).

---

## 7. Controller necessity review — OPTION A adopted (controllerless) (PROPOSAL)

### 7.1 The two options

**OPTION A — CONTROLLERLESS OPERATOR-OWNED LAUNCH (adopted into R1).**
After all gates pass, the EBS itself launches the frozen networked auditor
boundary. NO controller process holds launch authority at any point. The
historical "controller" role decomposes into: (a) the OPERATOR, who starts
the one-shot EBS per attempt and holds all authority decisions; (b) the
EVENT-PACKAGE preparation session (S1, separately authorized, before any
attempt), which freezes transports/contracts/gates; (c) the CONTROL ROOM
readback stages, which read frozen artifacts and decide — all OFF the launch
authority path. There is NO inference-capable or instruction-following agent
between the operator and the auditor exec.

**OPTION B — AUTHENTICATED CONTROLLER REQUEST (rejected; documented).**
A controller session may request launch; the EBS independently binds and
authorizes it via kernel-identity authentication (SO_PEERCRED uid/pid +
`/proc` starttime, pre-bound in the frozen binding — the qh
`authorized_controller` pattern re-instantiated independently).

### 7.2 Comparison and decision

| Axis | OPTION A (controllerless) | OPTION B (authenticated controller) |
|---|---|---|
| Authority-path process count | minimum: EBS → boundary → client | +1: controller request channel on the path |
| Trust surface | no controller identity machinery at all | must bind/authenticate a controller process; request schema; claim discipline |
| Historical failure classes covered | removes the RC-1 admission-gate override ACTOR and the RC-2 retry ACTOR entirely (no controller exists to override or retry) | controller acts remain possible; must be defended against |
| One-shot semantics | simplest: capability lives and dies in the EBS process | capability must additionally survive a controller↔EBS handoff or refusal thereof |
| Credential custody | credential never visible to any controller (none exists) | controller must be proven non-possession (extra negative obligations) |
| Blindness | strictly better: no controller context/session can leak into the launch path (L-01/L-25 classes structurally absent) | controller-scope gates (C-1/C4′-style) must be re-established for the new controller |
| Operator burden | operator (or operator-authored frozen invocation) starts each attempt — already the recorded direction ("operator-held launch invocation") | same operator burden PLUS controller lifecycle management |
| Adaptive behavior need | none required: per-attempt launch is fully deterministic; all judgment stages (preparation, barrier, R0, acceptance) are elsewhere and zero-model or operator-side | a controller adds judgment on the authority path — exactly what must be minimized |

**No concrete required workflow property makes a controller necessary.**
Every step a controller historically performed between freeze and launch is
either (i) frozen at S1 package-preparation time, (ii) a deterministic gate
the EBS checks mechanically, or (iii) an operator/Control-Room decision that
is deliberately human/governance. Post-barrier readback sessions that may use
model assistance sit strictly OFF the authority path (they read frozen
artifacts; they cannot launch anything).

**DECISION: OPTION A.** Reducing the authority-path process count is treated
as a positive design objective, and OPTION B's only advantages (deferred
operator presence; a controller composing steps adaptively) are precisely the
properties the failure history (L-01, L-03, L-14, L-25) shows to be hazards.
R1 (§30) is OPTION A concretized.

---

## 8. No portable bearer token (REQUIREMENT) — pattern evaluation

**PATTERN P1 — PROCESS-BOUND ONE-SHOT SUPERVISOR (ADOPTED).** The one-shot
launch capability is internal, non-exportable state of the EBS process: the
frozen binding document (validated at start) + the sealed credential memfd +
the in-memory state machine. There is NO capability object that can be
serialized, copied, or presented twice: nothing is written to the filesystem
except the append-only accounting record (which records STATES, never
capability material); nothing enters argv or environment; no IPC text carries
it; no other process ever holds it.

**PATTERN P2 — SEALED CAPABILITY OBJECT (documented; NOT adopted).** A
sealed/inherited capability object bound to (event, role, attempt, transport
package identity, auditor executable identity), atomically consumable by the
authority. P2 is viable and is the correct pattern if launch authority must
ever cross a process boundary (it would be the basis of an OPTION-B-style
design). It is NOT adopted because R1 keeps the capability inside one process
for its entire lifetime — a strictly smaller trusted surface with identical
binding semantics.

**Hard prohibitions (REQUIREMENT, held from the readback):** NO copyable
token in: filesystem; argv; environment; ordinary IPC text; controller-owned
memory (no controller exists in R1; and the prohibition stands for any future
variant).

**DECISION: P1** — satisfies all required single-use semantics with less
trusted surface (§10).

---

## 9. EBS attempt state machine (PROPOSAL — independent of qh)

```
                    operator starts frozen EBS
                    (package self-verify + binding load)
                              │
                          PREPARED ──────────── any validation/gate FAIL
                              │                  → TERMINAL_PREEXEC_STOP
                              │                  (absorbing)
                    all pre-inference gates recorded PASS
                              │
                        GATES_PASSED ────────── any late FAIL/stop
                              │                  → TERMINAL_PREEXEC_STOP
                    ┌─────────┴──────────────────
                    │ ATOMIC (§10): in-memory transition
                    │ + append-only accounting record
                    │   CONSUMED_PRE_EXEC, fsync BEFORE exec
                    ▼
                 CONSUMED_PRE_EXEC
                              │ fork; child execs frozen boundary launcher;
                    │ parent records EXEC_ATTEMPTED
                    ▼
                 EXEC_ATTEMPTED ──── child/boundary/client any outcome
                              │        (authority+engagement already consumed)
                    child exit; report freeze + screen + custody
                    ▼
                 REPORT_FROZEN (report present)   or   REPORT_MISSING
                              │
                           TERMINAL
```

- States: `PREPARED`, `GATES_PASSED`, `CONSUMED_PRE_EXEC`, `EXEC_ATTEMPTED`,
  `REPORT_FROZEN`, `REPORT_MISSING`, `TERMINAL`, `TERMINAL_PREEXEC_STOP`.
- `TERMINAL_PREEXEC_STOP` and `TERMINAL` are absorbing; no transition out;
  the EBS process exits on reaching them. There is no reset interface.
- The machine is INDEPENDENT of qh: it is implemented in the EBS, and its
  durable trace is the EBS append-only accounting record (operator-held
  path, one file per attempt, fsync'd; never writable by any other process;
  replay of a recorded attempt id is refused at EBS start by binding check).
- **After CONSUMED_PRE_EXEC the authority is consumed REGARDLESS of**: exec
  failure; provider initialization failure whose inference status is
  uncertain; provider/API failure; timeout; model crash; missing report.
  **No second provider-capable exec from the same authority is possible**:
  the capability exists only as the EBS process's pre-consumption state,
  which no longer exists once the transition is made, and the code path that
  performs a launch is unreachable in any post-CONSUMED state (state check
  + single-shot code structure; the process exits after TERMINAL).
- A crash of the EBS parent AFTER CONSUMED_PRE_EXEC but before report freeze
  leaves the durable record at CONSUMED_PRE_EXEC/EXEC_ATTEMPTED: authority
  and engagement accounted CONSUMED (fail-closed); report custody falls back
  to the operator-side frozen-output location; classified in the failure
  matrix (§31, rows E/F/Q/R).

---

## 10. Atomic consumption semantics (PROPOSAL)

The transition `GATES_PASSED → CONSUMED_PRE_EXEC` is a single program-order
sequence inside the non-dumpable EBS process with NO intervening operation
that could launch anything:

1. verify every mandatory gate result is recorded PASS and every binding
   field matches (state = GATES_PASSED);
2. write the accounting record `CONSUMED_PRE_EXEC` with the full binding
   (event id, auditor role, attempt id, transport package SHA-256, prompt/
   evidence manifest digest, auditor executable SHA-256, adapter id, output
   identity, EBS package SHA-256, timestamp) and **fsync** it durably;
3. only then fork, and in the child exec the frozen networked boundary
   launcher (never the provider client directly).

Properties:

- There is **no observable state** in which an inference-capable exec has
  occurred or could occur while the authority is unconsumed: step 3 is
  unreachable unless step 2 completed; if the process dies between 2 and 3,
  the authority is durably recorded CONSUMED with no engagement — fail-closed
  (replacement requires NEW operator authority, §12).
- The record is append-only; attempting any second consumption in the same
  process is unreachable (state machine), and re-running the EBS for the
  same attempt id is refused at start (binding/attempt check against the
  existing accounting record set).
- The ledger/pre-post captures from the original design remain OBSERVABILITY
  EVIDENCE ONLY; they are not on the authority path (readback §10 requirement
  satisfied — enforcement now lives IN the launch path itself).

---

## 11. Replay / duplication refusal matrix (PROPOSAL — all mechanically refused)

| Attack / mistake | Mechanism that refuses it | Where enforced |
|---|---|---|
| Second launch using same authority | capability is pre-consumption process state; post-CONSUMED the launch path is unreachable; EBS is one-shot and exits | EBS state machine (§9) |
| Copied authority material | nothing copyable exists: no token bytes are ever serialized to fs/argv/env/IPC; accounting record records states only | P1 pattern (§8) |
| Wrong auditor role | binding document pins role; EBS refuses GATES_PASSED on mismatch; transport profile/credential role derived from binding | EBS binding validation |
| Wrong attempt | attempt id in binding + accounting-record-set check at EBS start (duplicate/unknown attempt refused) | EBS start + binding |
| Wrong event | event id in binding and in the frozen event package manifest; mismatch ⇒ TERMINAL_PREEXEC_STOP | EBS binding validation |
| Wrong frozen transport package | package SHA-256 + per-file manifest verified by EBS before gates | EBS package validation |
| Wrong prompt/evidence manifest | common-evidence manifest digest + A=B parity proof verified before gates | EBS evidence binding |
| Wrong model executable | auditor executable SHA-256 verified by EBS immediately before fork/exec | EBS exec binding |
| Wrong provider adapter | adapter id in binding; materialization layout keyed to adapter id; unknown adapter refused | EBS + boundary launcher |
| Wrong output role | output location derived from binding (role+attempt), created by EBS, the ONLY writable target of the boundary | EBS output binding |
| Same-UID host process attempting to forge/mint | no mint interface exists at all; authority = starting a NEW EBS from the frozen package under NEW operator authority; same-UID can at most kill the EBS (denial, never authority gain — L-13/R-6 class) | architecture (§4, §7) |

Observability logs remain supplementary only; every row above is enforced by
a mechanism, not by a log check. (REQUIREMENT satisfied.)

---

## 12. Replacement attempt (PROPOSAL — REQUIREMENT restated mechanically)

A replacement auditor attempt REQUIRES ALL of: NEW explicit operator
authority (a recorded authority id); NEW attempt id; NEW EBS process started
from the frozen package (NEW supervisor authority state — the old process is
gone); NEW output location (role+attempt-derived, never reused); NEW
accounting record (append-only; references the superseded attempt). If
event-package bytes changed: NEW package binding/version AND a new Control
Room package readback are required before any gate may pass. NO controller
may autonomously retry or re-mint — in R1 there is no controller at all, and
the EBS has no retry/mint interface (single-shot process; replacement is an
operator act by construction).

---

## 13. Credential custody — target-independent (PROPOSAL; closes the custody half of CR-BOOTSTRAP-DESIGN-003)

### 13.1 Source and ingestion

- Credential plaintext MUST NOT enter: the qh target (never passed to or
  readable by any qh code); any controller (none exists in R1); the evidence
  package; the handoff archive; argv; environment; an ordinary persistent
  host file; published hashes/logs. (REQUIREMENT)
- **Source: operator-controlled pipe or fully sealed memfd ONLY.** An
  ordinary-file plaintext source is **REFUSED** (fail-closed at EBS start —
  the same source-discipline as the evidence-supported qh custody mechanism,
  re-implemented independently in the EBS per §4.4).
- The EBS makes itself **non-dumpable BEFORE receiving credential material**
  (`prctl(PR_SET_DUMPABLE, 0)` at process start, before opening the source
  channel).

### 13.2 Custody state

- The EBS reads ONLY the expected role credential (role label from the
  binding; the irrelevant role's credential is never requested and MUST be
  ABSENT from the boundary).
- Bytes are copied into a **sealed memfd** (MFD_CLOEXEC | MFD_ALLOW_SEALING;
  seals applied) — sealed in-memory custody using the platform's established
  memfd/seal semantics; the source fd is closed after ingestion.
- The EBS **never prints, hashes, or logs plaintext**. Retained metadata is
  the MINIMUM: role label and byte length. (No credential digest enters any
  published artifact — "no credential hashing for publication" held.)
- **If mandatory safe custody cannot be established** (memfd/seals
  unavailable; source kind invalid; ingestion mismatch) ⇒ **PREEXEC STOP**
  (TERMINAL_PREEXEC_STOP, authority unconsumed). **No downgrade path exists.**

### 13.3 Transfer to the final boundary

- The sealed memfd is passed to the boundary launcher child **by fd
  inheritance across exec** (close-on-exec cleared for exactly that fd) — a
  capability channel, never argv/env/file. The boundary launcher (frozen
  event-package code, SHA-verified by the EBS before fork) is a declared TCB
  component (§32) and is the ONLY code that materializes plaintext.
- The EBS parent closes its sealed memfd at TERMINAL; the child's fd dies
  with the boundary at teardown.

### 13.4 Why this closes the readback's required correction

The readback required a TARGET-INDEPENDENT mechanical custody path from the
operator secret source to the NETWORKED external auditor child, with the
twelve enumerated properties (not argv/env/persistent-file/controller-
readable/hashed/logged; qh never receives plaintext; non-dumpable/sealed
process custody; exactly the authorized role; materialization only inside
the final networked boundary; irrelevant role credential absent; ephemeral
writable-at-init child home; teardown removal; controller cannot reproduce a
provider-capable launch; fake/replayed capability cannot obtain the
credential). Every property is assigned a mechanism: §§13–15 for custody and
materialization; §8/§10 for the unforgeable capability (a fake/replayed
launch has no EBS pre-consumption state and no sealed memfd — there is
nothing to present); R1 removes the controller entirely. The IMPLEMENTATION
is independent of qh (§4.4); the FORMATS reuse the two evidence-supported
layouts (§14). Custody is thereby DEFINED MECHANICALLY in the design; its
zero-provider proof obligation is GATE-W′ (§21) at event preparation, and
real-credential behavior remains event-time evidence-gated. NO real
credential execution is authorized or performed by this design revision.

---

## 14. Final networked boundary materialization (PROPOSAL)

Credential plaintext is materialized ONLY in the FINAL external-auditor
network boundary, immediately before auditor-client initialization, using
the evidence-supported role layouts:

- **Claude first-party (Auditor-A role candidate)**: `CLAUDE_CONFIG_DIR/
  .credentials.json` — fresh dedicated ephemeral `CLAUDE_CONFIG_DIR`,
  credential file mode 0600, minimal config surface only; no settings/
  projects/plugins/skills/history.
- **Codex ChatGPT OAuth (Auditor-B role candidate)**: `CODEX_HOME/auth.json`
  (mode 0600) plus the required minimal `config.toml` surface, inside a
  fresh ephemeral `CODEX_HOME` that is WRITABLE at client initialization
  (L-24 errno30 lesson held).

Materialization location properties (all REQUIRED):

- **boundary-private**: on namespace-local ephemeral storage (tmpfs) inside
  the networked boundary's mount namespace, at a path derived from the
  frozen binding — never a host-visible persistent path;
- **ephemeral**: destroyed with the boundary mount namespace at teardown
  (the launcher unlinks the file and the tmpfs dies with the ns); EBS
  verifies teardown completion (namespace/process reaping) before TERMINAL;
- **writable at client initialization where required** (CODEX_HOME class);
- **not visible from the host controller**: in R1 no controller exists; the
  host-side path is reachable only through the EBS/boundary processes, and
  the mount exists only inside the boundary mount namespace;
- **not shared with the peer auditor**: each auditor boundary is a separate
  namespace tree with its own tmpfs; peer mounts are absent by construction
  (blindness map proves the negative);
- **removed at teardown** (above);
- **irrelevant provider credential ABSENT** — only the bound role's adapter
  material is ever ingested or materialized (role-minimal auth, L-09 held).

---

## 15. CRITICAL ADDITION — credential-to-tool isolation (PROPOSAL; closes the isolation half of CR-BOOTSTRAP-DESIGN-003)

### 15.1 The threat

The networked auditor has tooling capable of reading or executing the
target. A malicious qh target (or target-launched subprocess, or injected
instruction inside target/evidence bytes) must NOT be able to steal the
auditor's provider credential: `auth.json`, `.credentials.json`, raw
OAuth/token material, supervisor custody fds, or supervisor process memory.
Prompt instructions are NOT a defense. The design therefore separates:

- **PROVIDER CLIENT CREDENTIAL DOMAIN** — the provider client process and
  its mount namespace, which contains the credential tmpfs; it may
  authenticate to its provider; and
- **AUDITOR TOOL / TARGET EXECUTION DOMAIN** — every process initiated as a
  tool/command during the audit (bash/shell tools, file operations executed
  as subprocesses, target/test subprocesses); this domain MUST NOT be able
  to read the credential material, the custody fds, or supervisor memory.

### 15.2 C1 — load-then-remove (evaluated; NOT adopted)

C1 = provider client loads the credential, then the credential file is
removed/unmounted before target-tool execution begins, with evidence that
the client remains functional. **NOT adopted: do not assume C1 works for
Claude/Codex without evidence.** Both evidence-supported clients treat the
credential file as a live runtime interface, not a read-once input: the
writable-at-init CODEX_HOME requirement (L-24) and the OAuth token-refresh
class imply mid-session re-read/write-back (refresh persistence) — removing
the file after initial load risks breaking authentication mid-session and
is UNPROVEN safe for either client. C1 is recorded as an UNRESOLVED
REQUIREMENT (client refresh-persistence behavior) and is not relied upon.

### 15.3 C2 — namespace-split credential domain (ADOPTED)

Mechanism (mechanical isolation, no reliance on auditor instructions):

1. The boundary launcher mounts the credential tmpfs ONLY in the provider
   client's mount namespace (the boundary's root mount ns).
2. Every tool/command execution the model client performs goes through a
   shell/tool entry point inside the boundary. The boundary installs a
   **frozen, hashed tool-execution wrapper** at the shell path(s) the client
   uses: the wrapper (a ~30-line reviewed script/binary from the frozen
   event package) does `unshare(CLONE_NEWNS)` → `umount2(<credential
   mount>, MNT_DETACH)` (also detaching the supervisor/launcher-internal
   mounts if any are visible) → exec the real shell. Each tool subprocess
   tree therefore runs in a mount namespace where **the credential path
   does not exist**. Mount-ns copies make the detach private to the tool
   subtree; the provider client's own view is untouched.
3. Target/test subprocess execution (§18) occurs only through this tool
   domain — the audited qh target and anything it launches can never see
   the credential, the sealed memfd is host-side in the EBS (different
   process tree, no fd passing), and EBS memory is unreachable (separate
   PID namespace; non-dumpable).
4. `/proc`-mediated cross-domain access (`/proc/<client>/root`, `/proc/<fd>`
   duplication, `/proc/<client>/mem`) is denied by composition: fresh
   boundary PID namespace (only boundary processes visible), non-dumpable
   client process (PR_SET_DUMPABLE=0 inherited through the launcher),
   ptrace-protected (Yama where available). These negatives are MANDATORY
   GATE-W′ assertions with SYNTHETIC bytes (§21); if any negative cannot be
   demonstrated on the event host, it is recorded as a BLOCKER/residual —
   not assumed.
5. **In-process tool reads** (a client tool that reads files inside the
   client process itself, e.g. a built-in Read tool): mitigated by frozen
   client configuration deny-rules over the credential path
   (application-level), plus the §15.4 report screen as the outer tripwire.
   HONESTLY CLASSIFIED: subprocess-domain isolation is MECHANICAL;
   in-process read protection is APPLICATION-LEVEL (client-config
   semantics), mechanically rehearsed only to the extent GATE-W′ allows
   without inference, and is disclosed as a residual unless the event
   proves more.

### 15.4 Post-exec report screen

At report freeze, the EBS (which holds the sealed credential bytes) scans
the frozen report for the credential plaintext and refuses/unmarks any
report containing it (result recorded as a boolean; plaintext never logged,
never hashed into evidence). In GATE-W′ rehearsal the same screen must fire
on a deliberately-planted SYNTHETIC marker. This is a detection tripwire
layered over the §15.3 prevention — supplementary, not a substitute.

### 15.5 Conditional BLOCKER rule (REQUIREMENT)

If, at event preparation or GATE-W′, a provider client is found to REQUIRE
credential visibility in a context that the tool/target domain must share
(bypassing the shell wrapper via a non-shell execution path, or requiring
the credential mounted in the shared domain), THAT IS A RECORDED BLOCKER
for that role: no hand-waving, no downgrade; the role is not launched until
redesigned or re-evidenced.

**Verdict on CR-BOOTSTRAP-DESIGN-003 = CLOSED_BY_DESIGN**: the custody path
is defined mechanically and target-independently (§13–§14); credential-to-
tool separation is defined mechanically with an explicit domain split,
named residuals, mandatory synthetic proof obligations, and a conditional
BLOCKER rule (§15). Remaining uncertainties (GATE-W′ unproven; real-client
refresh behavior; in-process-read application-level classification) are
recorded as event-time evidence gates and residuals — not as satisfied
claims. No real credential is executed in this design session.

---

## 16. Target execution policy (PROPOSAL)

The auditor reviews the qh target independently without the qh target
becoming privileged. Execution classes, defined separately:

1. **Source reads** — frozen target source RO-mounted in the auditor
   boundary (read-only bind from the git object store checkout at
   `d4d584ff…`); identical for A and B (common evidence parity).
2. **Static analysis** — unrestricted within the RO evidence/target mounts
   and bounded scratch.
3. **Deterministic test execution** — the auditor MAY execute the target's
   own deterministic/self-test batteries.
4. **Arbitrary target subprocess execution** — permitted ONLY inside the
   auditor sandbox.

ANY target execution occurs in a sandbox (the tool domain of §15) with ALL
of: NO provider credential (C2 domain split — path absent); NO launch
authority (nothing forgeable exists; authority is host-side EBS process
state); NO bootstrap-supervisor IPC authority (the EBS has no IPC surface;
it is not reachable from inside any boundary); NO write access to the
first-pass report except explicitly mediated output (the report location is
EBS-custodied; the auditor's own `/auditor-output` is the ONE writable bind
— the tool domain cannot write the frozen/custody copies); NO peer
artifacts (not mounted; blindness map proves absence); bounded scratch only
(size-capped tmpfs); network policy explicitly recorded per §20 (default:
the networked boundary's provider-connectivity policy applies to the
client; target-initiated network egress inside the tool domain is NOT
granted beyond the boundary's recorded policy, and any target egress is
disclosed as residual exposure of the networked class — see §20.6).

---

## 17. Networked transport (PROPOSAL — frozen event package; held semantics refined)

The networked auditor transport remains a **FROZEN EVENT PACKAGE** built at
event-preparation time (S1) under separate operator authority. It may use
the historically evidenced v3 launcher lineage (`fb5754a3…` composition:
`--unshare-pid`, fresh `/proc`, host-sentinel-invisible, `/proc/<pid>/root`
escape blocked, role-minimal auth, ephemeral writable-at-init homes,
resolver provision P12/N12, auditor-output as the ONE rw bind) as DESIGN
INPUT ONLY — it inherits NO historical authority; every binding is
re-derived at freeze and re-verified by the identity linter.

**Required transport binding** (frozen in the event package AND in the EBS
binding document; every field verified by the EBS before GATES_PASSED):

event id; auditor role; attempt id; auditor executable SHA-256/version;
provider role; frozen prompt (digest); common evidence manifest (digest);
target identity (`d4d584ff…` + root/qh/skill trees); output identity
(role+attempt-derived path); boundary launcher identity (SHA-256); sandbox/
profile identity (including the Codex named restricted profile per C-3 with
`workspace_roots` = auditor-output and NO credential path entry);
credential adapter identity (`codex_chatgpt_oauth_v1` /
`claude_firstparty_oauth_v1`); GATE-W′ evidence record (from the S1
rehearsal); EBS package identity (SHA-256 + manifest); tool-domain wrapper
identity (SHA-256).

---

## 18. GATE-W′ — future pre-inference proof design (PROPOSAL; REQUIRED but UNPROVEN)

GATE-W′ remains REQUIRED and is NOT treated as proven. It must be
IMPLEMENTED and TESTED during separately authorized event-package
preparation, BEFORE any inference execution, using a LOCAL deterministic
payload (a synthetic stand-in "client" script) in the FINAL networked
boundary. Provider inference during GATE-W′ validation = ZERO (it never
counts as an engagement, §29). Required assertions:

1. evidence mounts read-only (write refused);
2. target mounts read-only (write refused);
3. auditor output writable (the one rw bind; CRUD proven);
4. unauthorized host paths unwritable;
5. peer output absent/inaccessible (mount-negative + probe);
6. persistent home unavailable (no host-backed home; ephemeral only);
7. **credential target location behaves as designed using SYNTHETIC bytes
   only**: client-domain read succeeds; client-domain refresh-style
   write-back succeeds (writable-at-init class); TOOL-domain read DENIED
   (path absent after the §15.3 wrapper detach); tool-domain `/proc`
   cross-access negatives (§15.3.4) all DENY;
8. tool/target domain cannot read the synthetic provider credential
   (assert 7's negative, restated as a first-class gate);
9. no extra writable role (writable-set enumeration equals the spec);
10. application-level sandbox/profile allows the required report write
    (Codex profile `sandbox_mode` write-permission class — the L-04 lesson,
    at application level, zero-provider);
11. the network delta does NOT add filesystem authority: the permitted
    write set of the networked boundary is BYTE-EQUAL to the no-egress
    GATE-W baseline write set (mount/writable matrix comparison);
12. the §15.4 report screen fires on a planted synthetic credential marker
    (negative control).

If any assertion cannot be demonstrated without inference (e.g. a client
behavior only observable mid-session), the EXACT unresolved requirement is
recorded (assertion number + missing evidence class) and the corresponding
role is not launched until resolved.

---

## 19. Network policy (PROPOSAL — honest classification)

"Networked auditor transport" permits exactly and only what is recorded
here; "network enabled" alone is NEVER a sufficient specification:

1. **Provider connectivity requirement**: outbound HTTPS to the bound
   provider's endpoints (Auditor-A role candidate: Anthropic first-party
   API endpoints; Auditor-B role candidate: ChatGPT/OpenAI backend
   endpoints) is REQUIRED for the auditor client. This is the only
   connectivity the design REQUIRES.
2. **DNS/resolver behavior**: public name resolution must function inside
   the boundary (v3-lineage resolver provision P12/N12: read-only
   `/run/systemd/resolve` provision with its negatives). Resolver
   visibility of query names is a DISCLOSED information exposure (the
   resolver learns the provider hostnames — unavoidable with system
   resolution).
3. **Unrelated local/private service access**: the networked boundary uses
   the HOST network namespace (that is what distinguishes it from qh
   no-egress launches). Host-local and RFC1918 services are therefore
   REACHABLE unless separately filtered. The design RECORDS this exposure
   and does not claim it is filtered.
4. **Loopback**: shared with the host namespace ⇒ host loopback services
   reachable from inside the boundary. Disclosed; not filtered.
5. **Host namespace reachability**: network namespace SHARED (required for
   provider connectivity); PID/IPC/UTS/MOUNT namespaces NOT shared; `/proc`
   fresh and boundary-local.
6. **Endpoint-level egress restriction feasibility**: mechanically
   restricting egress to provider endpoints ONLY is **NOT ESTABLISHED**:
   provider frontends sit behind CDNs and rotating edge ranges; DNS
   indirection defeats naive IP pinning; the clients' full runtime endpoint
   set (auth, telemetry, websockets, CDN assets) is not enumerable a priori.
   The design therefore does NOT claim provider-endpoint-only isolation.
   Per-event OBSERVABILITY may record the contacted-endpoint set, but it is
   evidence, not enforcement.
7. **Peer process visibility**: separate PID namespace per auditor
   boundary ⇒ the peer auditor and host processes are invisible; peer
   artifacts are not mounted.
8. **Residual classification (honest)**: the networked auditor boundary
   carries HOST-EQUIVALENT OUTBOUND NETWORK EXPOSURE (class
   `NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE`), mitigated only by: the
   credential being absent from the tool domain (§15), the report screen
   (§15.4), the boundary's non-network isolation (PID/mount/IPC/UTS), and
   the frozen prompt/evidence set. Target-initiated egress from inside the
   tool domain falls under this same residual class and is disclosed per
   event. Any future tightening (per-endpoint filtering) requires new
   evidence and a new design decision.

---

## 20. First-pass auditor topology — HELD (design candidates; not executed)

TWO independent external first passes, different providers. Preferred role
candidates (unchanged, design strength): **Auditor-A = Claude Opus
first-party / fresh dedicated session** (ephemeral boundary-private
`CLAUDE_CONFIG_DIR`; frozen `claude` executable SHA; PLAIN_CLAUDE-class
profile; one-shot invocation); **Auditor-B = GPT-5.6-sol xhigh via Codex
ChatGPT-OAuth / fresh dedicated session** (ephemeral writable-at-init
`CODEX_HOME`; frozen `codex` executable SHA; C-3 named restricted profile;
`--sandbox`/`--add-dir`/`-s` class flags forbidden). THIS revision refines
only the invocation REQUIREMENTS (exact argv frozen at S1 with the identity
linter; GATE-W′ rehearsal on the EXACT transport profile; fresh-session
composition identical for A and B up to role-specific deltas). NOTHING is
executed by this record; other providers remain BLOCKERS, not guesses.

---

## 21. Blindness — HELD (MIXED; mechanically isolated where possible)

Mechanically isolated (per event, proven by gates): peer reports/output
(not mounted; blindness-map negative); prior/current-event auditor
substance (absent from every auditor-visible byte — allowlist-class
blindness map over the full auditor-visible surface, binding-v3 lineage);
unrelated home state (no host home; ephemeral homes only); installed Audit
Council runtime and project/chat histories (not mounted; PID/mount
isolation); `.system`/user skills advertisement neutralized (census +
disable-all with pre/post coverage proof, L-07); controller implementation
notes (NO controller exists in R1; frozen-requirements-only disclosure).
R1 strictly IMPROVES the mechanical set: with no controller process at all,
the controller-context leakage class (L-01/L-25) is structurally absent.
Procedural limitations remain DISCLOSED, never overstated: provider-side
model priors; operator staging between freeze and launch; the operator
decision sequence. Complete mechanical blindness is NOT claimed. AUCDEV-001
remains OPEN generally; per-run blindness statements record the actually
proven subset.

---

## 22. Common evidence — HELD

Frozen COMMON EVIDENCE SET: one manifest; per-file SHA-256 + sizes;
single-projection `COMMON_EVIDENCE_PAYLOAD_SHA256`; A=B substantive bytes
EQUAL. Role-specific differences ONLY: provider executable/config,
provider credential layout, mechanically necessary invocation wrapper (+
the frozen tool-domain wrapper, identical logic per role). No expected
findings; no expected severities; no expected recommendation; no peer
substance. Any other delta explicitly justified in the FDR or the set is
INVALID (68E3B082 precedent).

---

## 23. Audit requirements contract — frozen neutral (PROPOSAL; content only)

A NEW frozen harness-audit requirements contract (event-side, S1) requires
independent review of: source correctness; trust-boundary design; authority
semantics; controller/process isolation (in R1: the ABSENCE of a controller
and the EBS process isolation); pre-controller provenance (the qh
two-phase authority design as SUBJECT); credential custody design (both qh's
own custody AND the EBS custody of §13–§15); provider adapters; no-egress
behavior; GATE-W (and the event's GATE-W′ evidence); attempt terminality;
engagement accounting; code-object provenance precision note (the qh
loader/compile comparison claim — INDEPENDENT_AUDIT_FOCUS held); tests/
evidence completeness; known residuals. The contract contains NO expected
findings, NO pre-written PASS expectation, no severity pre-assignment; it
names the target identities and the frozen evidence set only.

---

## 24. Output custody — HELD

Each first pass writes EXACTLY ONE canonical first-pass report to its own
`/auditor-output` (the ONE rw bind). At process completion the EBS freezes
immediately: mode 0444; SHA-256 recorded; size recorded; mode recorded;
moved/held under operator bootstrap custody; the §15.4 screen runs before
custody acceptance. Missing report remains MISSING. stdout/stderr are NEVER
reconstructed as the first-pass report. Handoff archive with internal
SHA256SUMS per the established pattern.

---

## 25. Barrier — HELD

The barrier opens ONLY when BOTH required first passes are: present;
frozen; identity-bound; structurally valid (validator rc=0); authority-
accounted (EBS accounting records terminal and consistent); blindness-
valid (map + post-exec checks). If one first pass is missing or
nonconforming: NO peer disclosure; NO synthetic completion; event state
reflects incompleteness (asymmetric-failure path per §31 row T and §33).

---

## 26. R0 — HELD (zero-model)

Post-barrier R0 is ZERO-MODEL by default. It MAY: verify identity; verify
completeness; map coverage (COVERED_BY_FIRST_PASS_A/B /
COVERED_BY_MECHANICAL_EVIDENCE / NOT_COVERED; gaps block); classify
findings; identify disagreements; record counter-evidence. It MAY NOT:
invent substance; downgrade findings without basis; pre-write
qualification; convert agreement into proof.

---

## 27. Transport binding recap (see §17) — all fields EBS-verified pre-gate (PROPOSAL)

(Consolidated in §17; nothing added here.)

---

## 28. Authority / engagement accounting (PROPOSAL)

Two SEPARATE counters, both operator-side, both append-only:

- **AUDITOR_ATTEMPT_AUTHORITY** — one per attempt; consumed by the atomic
  GATES_PASSED → CONSUMED_PRE_EXEC transition (§10);
- **MODEL_ENGAGEMENT** — consumed only by the inference-capable executable
  attempt immediately following consumption.

**Precise consumption marker**: the successful atomic transition to
CONSUMED_PRE_EXEC (durably recorded) IMMEDIATELY followed by the
inference-capable exec attempt. If exact inference-start state cannot be
mechanically distinguished (provider init failure with uncertain inference
status; marker ambiguity — L-26 lesson): FAIL CLOSED toward CONSUMED for
BOTH counters. Deterministic GATE-W′ rehearsal NEVER counts as a model
engagement (it runs before GATES_PASSED, in the same attempt, with
synthetic bytes; the accounting record distinguishes rehearsal records from
engagement records by kind).

---

## 29. Recommended corrected architecture — R1 (PROPOSAL)

**R1 — CONTROLLERLESS PROCESS-BOUND BOOTSTRAP SUPERVISOR** (OPTION A + P1 +
EBS): the operator starts the frozen EBS for an attempt; the EBS validates
the frozen binding/package/evidence, ingests custody, enforces gate results,
atomically consumes, fork/execs the frozen networked boundary launcher,
waits (timeout-enforced), freezes and screens the report, records TERMINAL,
exits. No controller; no bearer token; no qh dependence; one-shot by
construction.

**(R2 — authenticated controller + supervisor-held sealed capability**
(documented alternative): the §7 OPTION B + §8 P2 combination — a
pre-bound controller requests launch; the EBS authenticates it (kernel
identity) and consumes a sealed capability object on its behalf. Viable,
strictly more machinery; rejected for the §7/§8 reasons.)

| Axis | R1 (controllerless, process-bound) | R2 (authenticated controller + sealed capability) |
|---|---|---|
| TCB size | smallest: EBS + boundary launcher + client + adapter + hasher + freezer (§32) | R1's set + controller binding/authentication + request schema + capability-object mint/consume logic |
| Mechanical one-shot guarantee | structural (capability = pre-consumption process state; process one-shot; no copyable form) | enforced at consume-time by the authority; capability object exists (sealed) and must be proven unforgeable/uncopyable across its lifetime |
| Credential isolation | credential never leaves EBS+boundary; no third process on path | equal isolation possible, but the controller process is an additional same-UID observer to defend against |
| Tool/target credential separation | identical (§15, boundary-side) | identical |
| Blindness | best achievable: no controller context exists | controller-scope gates must be rebuilt and proven |
| Implementation complexity | lowest (no request channel, no peer auth, no capability serialization) | moderate-high |
| Historical failure coverage | covers RC-1/RC-2/L-01/L-03/L-14/L-25 by REMOVING the actor class; L-13 same-UID DoS-only residual shared | covers them only if the new binding machinery is itself correct |
| New risks | operator presence per attempt (accepted: already the recorded direction); EBS parent death post-consumption (§9 fail-closed row) | all of R1's + request-channel attacks + capability-object lifecycle defects |
| Failure recovery | operator re-mint (§12) | same, plus controller restart handling |

**RECOMMENDATION: R1.** It matches the preferred direction (§30) and every
held semantic with the smallest trusted surface. R2 is retained as the
documented fallback should a future concrete workflow property require an
authenticated requester (none is identified).

---

## 30. Preferred direction (REQUIREMENT acknowledged — followed)

**CONTROLLERLESS + PROCESS-BOUND + TARGET-INDEPENDENT + ONE-SHOT** —
adopted as R1 because it removes the controller from the authority path and
avoids a portable bearer token, exactly as directed; no evidence found that
demonstrates a requirement for a controller or a transferable capability.

---

## 31. Failure matrix (PROPOSAL — complete, per attempt)

Legend: Auth = AUDITOR_ATTEMPT_AUTHORITY; Eng = MODEL_ENGAGEMENT;
"consumed" = durably recorded. Replacement = new operator authority (§12).

| # | Failure | Auth | Eng | Same-attempt retry | Replacement required? | Event terminal? | Classification |
|---|---|---|---|---|---|---|---|
| A | Package identity mismatch (EBS/package/linter) | unconsumed | unconsumed | NO (stop) | package fix ⇒ NEW binding_version + CR package readback, then replacement | no (attempt terminal) | PREEXEC_PACKAGE_IDENTITY_FAIL / TERMINAL_PREEXEC_STOP |
| B | Common-evidence mismatch / parity fail | unconsumed | unconsumed | NO | yes (after S1 fix + re-freeze + readback) | no (attempt terminal) | PREEXEC_EVIDENCE_PARITY_FAIL |
| C | Wrong role / attempt / event binding | unconsumed | unconsumed | NO | yes (correct binding) | no | PREEXEC_BINDING_REFUSED |
| D | Wrong auditor executable SHA | unconsumed | unconsumed | NO | yes (correct freeze) | no | PREEXEC_EXECUTABLE_IDENTITY_FAIL |
| E | Credential source invalid (ordinary file / wrong channel) | unconsumed | unconsumed | NO | yes (operator re-run with pipe/memfd) | no | PREEXEC_CREDENTIAL_SOURCE_REFUSED |
| F | Sealing unavailable / non-dumpable unavailable | unconsumed | unconsumed | NO (no downgrade) | yes (on a host supporting mandatory custody) | no | PREEXEC_CUSTODY_UNAVAILABLE_FAIL_CLOSED |
| G | Credential materialization fail (boundary) | unconsumed (fail occurs pre-GATES_PASSED at GATE-W′; if at launch: consumed—see row N note) | unconsumed | NO | yes | no | PREEXEC_MATERIALIZATION_FAIL |
| H | GATE-W′ fail (any assertion) | unconsumed | unconsumed | NO | yes (after fix + re-freeze + readback) | no | PREEXEC_GATE_W_PRIME_FAIL |
| I | Resource gate fail (R1–R7 class, invoked exactly once) | unconsumed | unconsumed | NO on same attempt | yes | no | PREEXEC_RESOURCE_GATE_FAIL |
| J | Boundary creation fail (launcher error pre-client) | consumed iff post-CONSUMED (fork/exec stage): CONSUMED, Eng unconsumed (no inference-capable exec) — fail-closed to Auth consumed when uncertain | unconsumed | NO | yes | no | EXEC_BOUNDARY_CREATION_FAIL_AFTER_CONSUMPTION |
| K | Network readiness fail (route/resolver preflight, non-inference) | unconsumed | unconsumed | NO | yes | no | PREEXEC_NETWORK_READINESS_FAIL |
| L | Provider client local init fail BEFORE any provider-network/inference initiation, precisely marked | consumed (post-CONSUMED exec attempted); Eng unconsumed if precisely pre-inference (Campaign-1 precedent), else consumed | unconsumed (precise) / consumed (uncertain) | NO | yes | no | LOCAL_INIT_FAIL_PRECISE / UNDETERMINABLE_FAIL_CLOSED |
| M | Authority already consumed (replay attempt) | already consumed | — | NO (refused mechanically, §11) | replacement only via NEW authority | no | REPLAY_REFUSED |
| N | Exec failure after consumption (exec error, child death pre-client) | consumed | consumed (fail-closed: inference status uncertain ⇒ Eng consumed) | NO | yes | no | EXEC_FAIL_AFTER_CONSUMPTION |
| O | Provider/API failure post-initiation | consumed | consumed | NO | per-side replacement under NEW authority | no (side terminal) | EXTERNAL_PROVIDER_FAIL / NONCONFORMING |
| P | Timeout (EBS-enforced, per-attempt bound) | consumed | consumed | NO | yes | no | TIMEOUT_AFTER_CONSUMPTION |
| Q | Auditor crash / EBS parent killed post-consumption | consumed | consumed | NO | yes; report custody falls back to operator-side frozen location | no (attempt terminal) | CRASH_AFTER_CONSUMPTION / DoS-only same-UID class |
| R | Report absent at child exit | consumed | consumed | NO (never reconstructed) | yes (or event-incomplete) | side terminal; event may be terminal-incomplete if budget exhausted | REPORT_MISSING |
| S | Report structurally invalid (validator rc≠0) or fails credential screen | consumed | consumed | NO | yes (redesign if screen-fired ⇒ treat as attempted leak: BLOCKER-class review) | no (attempt terminal) | REPORT_INVALID / REPORT_SCREEN_FAIL |
| T | Blindness breach detected (map/post-exec check) | per-side consumed state stands | per-side | NO | yes + design review | potentially (if pre-barrier peer exposure established ⇒ event terminal-incomplete) | BLINDNESS_VIOLATION |
| U | Both first passes conforming + frozen + validated | consumed ×2 | consumed ×2 | — | — | barrier OPENS (not terminal-failure) | SUCCESS_PATH (accounting closed) |

Every row is enforced by state machine + accounting-record durability;
observability logs are supplementary. No silent retry exists in any row.

---

## 32. Minimal TCB inventory (PROPOSAL — components trusted BEFORE the independent qh audit)

| Component | Why trusted | How identified | How frozen | Target-independent? | Mechanically testable? | Future review status |
|---|---|---|---|---|---|---|
| Operator | authority source; starts EBS; holds secrets | human; recorded authority ids | n/a (governance records) | yes | n/a | Control Room governance |
| OS/kernel primitives (namespaces, mount ns, memfd+seals, fsync, PID ns, Yama/ptrace, SO_PEERCRED-not-needed-in-R1) | provide isolation/sealing/durability semantics the design relies on | kernel version recorded per event | host platform recorded | yes (qh uses the same classes) | yes (GATE-W′ negatives + EBS self-tests) | event record + GATE-W′ evidence |
| EBS package (bootstrap supervisor) | the authority root: gates, consumption, custody, accounting | package SHA-256 + file manifest + self-verification | frozen commit + manifest before any authority (§6) | YES (outside qh/skill; no qh imports) | yes (deterministic battery + self-test, zero-network) | Control Room source readback BEFORE execution authority; included in event evidence; reviewable again post-event |
| Networked boundary launcher (event package; v3-lineage-derived) | composes the auditor boundary; materializes credential ( sole plaintext materializer) | SHA-256 in binding | S1 freeze + CR package readback | YES (event-side code) | yes (GATE-W′ battery) | CR package readback pre-event; GATE-W′ proof |
| Tool-domain wrapper (§15.3) | detaches credential mount for every tool exec | SHA-256 in binding | S1 freeze | yes | yes (GATE-W′ synthetic negatives) | same as launcher |
| Provider client executables (claude / codex CLI) | must faithfully implement auth + tool execution + sandbox/profile semantics | executable SHA-256 + version pinned in binding | pinned at S1 | external but pinned | partially (GATE-W′ app-level assertions; client internals evidence-gated) | event-time evidence; refresh/deny-rule behavior = recorded residual |
| Credential adapter/materialization logic | writes plaintext to the boundary-private layout for the bound role only | part of launcher package (hashed) | S1 freeze | yes (re-implemented; qh layouts reused as FORMATS only) | yes with SYNTHETIC bytes (GATE-W′) | CR readback + GATE-W′ |
| Identity/hash utilities (SHA-256, manifest comparison, linter) | identity decisions | stdlib + frozen linter SHA | S1 freeze / EBS package | yes | yes (negative controls; linter battery) | CR readback |
| Output freezer/validator + report screen | custody truth of first passes | part of EBS + frozen validator SHA | EBS package + S1 freeze | yes | yes (deterministic; synthetic screen negative) | CR readback; R0 verifies records |

NOT in the TCB: the qh target (subject/evidence); the installed Audit
Council skill; any model output; any controller (none exists); any
historical artifact (inputs only). The TCB is exactly the operator, kernel,
EBS package, and the four frozen event-package components above — kept
minimal by construction (§4.3).

---

## 33. Held semantics recap (NOT reopened)

Success semantics (§34 below), ONE-EVENT single-use no-revival lifetime
(§35), two-pass topology (§20), MIXED blindness (§21), common-evidence
parity (§22), neutral contract (§23), output custody (§24), barrier (§25),
zero-model R0 (§26), accounting separation (§28), no-silent-retry,
addenda/adjudication under separate authority, qualification/installation
separation — ALL HELD from the accepted design inputs; THIS revision
changed ONLY the authority/custody architecture that the three findings
targeted.

---

## 34. Success semantics — HELD

A successful future event can establish ONLY:

```
AUCDEV023_HARNESS_INDEPENDENT_REVIEW_COMPLETE
/ EVENT <exact id>
/ TARGET d4d584ffa47ad2848268ba947247f81a845b2322 (root 1d4b8b8e…, qh 5b8d5e54…, skill c792933a…)
/ AUDITORS <exact A/B identities + bindings>
/ BINDING <exact transport/FDR/contract/EBS digests>
/ REPORTS <exact first-pass hashes/sizes/modes>
/ COMPLETENESS <barrier + coverage map state>
/ FINDINGS <per-auditor verdicts + reconciled classification>
/ CONTROL_ROOM_ACCEPTANCE <explicit decision>
```

It does NOT establish: a qualified Audit Council predecessor; Audit Council
qualification; installation; standing bootstrap authority (§35).

---

## 35. Policy lifetime — HELD

**ONE EVENT. Single-use. No revival.** Adoption (if the Control Room ever
adopts) authorizes exactly ONE bootstrap harness-audit event with a new
event namespace and default budget 2 engagements. Any later bootstrap event
requires a NEW Control Room governance decision AND new explicit operator
execution authority. This revision itself authorizes NOTHING.

---

## 36. Design acceptance criteria — findings closure verdicts (PROPOSAL)

```
CR-BOOTSTRAP-DESIGN-001 : CLOSED_BY_DESIGN   (§§3–6: EBS = minimal
                         target-independent operator-controlled authority
                         root; qh demoted to subject/evidence; no qh/AC
                         dependence on the authority path; non-recursive
                         §6 authority basis)
CR-BOOTSTRAP-DESIGN-002 : CLOSED_BY_DESIGN   (§§8–12: P1 process-bound
                         one-shot; atomic GATES_PASSED→CONSUMED_PRE_EXEC
                         fsync-before-exec; replay/duplication mechanically
                         refused in the launch path itself; ledger demoted
                         to observability)
CR-BOOTSTRAP-DESIGN-003 : CLOSED_BY_DESIGN   (§§13–15: target-independent
                         mechanical custody pipe/memfd→sealed memfd→fd-
                         inheritance→boundary-only materialization with
                         teardown; credential-to-tool isolation by C2
                         domain split + screen + conditional BLOCKER rule;
                         GATE-W′ synthetic proof obligations mandatory)
NEW blocking trust-boundary issues identified by THIS revision : NONE
                         (new RESIDUALS honestly recorded: GATE-W′
                         unproven until event prep; real-client refresh/
                         deny-rule behavior evidence-gated; in-process
                         read protection application-level; host-netns
                         network exposure class §19.8; EBS trusted-before-
                         audit by declared minimal TCB §6 — inherent to
                         bootstrap, disclosed not hidden)
```

All three findings are closed by design and no NEW BLOCKING trust-boundary
issue is identified; the residuals above are DISCLOSED UNCERTAINTIES AND
EVENT-TIME GATES, not satisfied claims. Therefore THIS revision recommends
itself as ADOPTION-READY FOR CONTROL ROOM READBACK (recommendation only;
adoption is the Control Room's decision; NO execution follows
automatically from this record).

---

## 37. Current-facing state (after this publication)

```
AUCDEV-023                                = P1 / READY (NOT DONE)
frozen audit target                       = d4d584ffa47ad2848268ba947247f81a845b2322 (held EXACTLY)
KNOWN_IMPLEMENTATION_BLOCKERS             = CLOSED_AT_CONTROL_ROOM_READBACK_STRENGTH
auditor-bootstrap governance design       = PROPOSED design PARTIALLY_ACCEPTED / REVISION_REQUIRED (unchanged historical fact)
THIS design revision                      = PROPOSED_REVISION_FOR_CONTROL_ROOM_READBACK
                                            (findings 001/002/003 CLOSED_BY_DESIGN; R1 recommended)
INDEPENDENT_AUDITOR_PROVENANCE_GATE       = NOT_SATISFIED
INDEPENDENT_HARNESS_AUDIT                 = BLOCKED_PENDING_AUDITOR_BOOTSTRAP_GOVERNANCE
                                            (until Control Room accepts/adopts a corrected design
                                            AND the operator separately authorizes preparation/execution)
qualification                             = NONE
installation                              = NONE
```

Next action EXACTLY ONE: **INDEPENDENT CONTROL ROOM READBACK OF THIS
DESIGN-REVISION PUBLICATION.**

---

## 38. Future implementation source location — DESIGN ONLY (PROPOSAL)

A future EBS implementation SHOULD live in a NEW separate repository
subtree/package, proposed: top-level `bootstrap-supervisor/` (e.g.
`bootstrap-supervisor/ebs/` + `bootstrap-supervisor/tests/` +
`bootstrap-supervisor/MANIFEST.md`). It MUST NOT live inside
`qualification-harness/**` or `skill/**` (it would re-create the circular
trust of finding 001). Expected future mutation boundary: files under
`bootstrap-supervisor/**` change ONLY via separately authorized tasks;
every change ⇒ new freeze (SHA-256 manifest + battery) + new Control Room
readback BEFORE any event execution authority; the subtree carries no
standing authority; nothing in it is created by THIS task. The networked
boundary launcher, tool wrapper, linter, validator, gates, and blindness
map remain EVENT-PACKAGE-side artifacts (per-event frozen packages outside
qh/skill), per the S1 stage of the original design.

---

## 39. Publication record (this session)

Changed paths EXACTLY: NEW THIS record +
`docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` +
`docs/chatgpt-project/AUCDEV-BACKLOG.md`. NOT modified:
`qualification-harness/**` (tree `5b8d5e54…` unchanged), `skill/**` (tree
`c792933a…` unchanged), the runbook, Project Instructions,
`AUCDEV-QUALIFICATION-HISTORY.md` (no qualification/installation event —
update NOT_APPLICABLE per the 2026-09-10/2026-09-18 precedent), the
original design record, the design-readback record, historical AUCDEV-010
reports, frozen Campaign-2 artifacts, and the frozen AUCDEV-023 target.
Exactly ONE append-only design-revision publication commit; at most ONE
fast-forward push; live master re-resolved EXACT against the required base
immediately before staging.

---

## 40. Zero-execution attestation (OBSERVED_FACT)

Provider/model/frontier calls: ZERO. Auditor executions: ZERO.
`/audit-council` executions: ZERO. Bootstrap-event executions: ZERO.
Qualifications: NONE. Installations: NONE. EBS implementation: NONE
(design only — no `bootstrap-supervisor/` was created). Event-package
preparation: NONE. Frozen-target mutations: NONE (target `d4d584ff…` and
its trees re-verified EXACT; source read byte-wise via `git show`, never
executed). Runbook/policy adoption: NONE. Credential CONTENT reads/hashes:
ZERO. The original design record, its readback, and all historical records
were read READ-ONLY and left unmodified.

---

Result: `AUCDEV_023_AUDITOR_BOOTSTRAP_GOVERNANCE_DESIGN_REVISION_PROPOSED_FOR_CONTROL_ROOM_READBACK` (findings CR-BOOTSTRAP-DESIGN-001/-002/-003 CLOSED_BY_DESIGN; recommended corrected architecture R1 = controllerless process-bound target-independent one-shot external bootstrap supervisor).
