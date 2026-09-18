# AUCDEV-023 — Authority Bootstrap Hardening: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION SESSION ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room decision-maker (this session publishes the Control Room's already-reached readback disposition verbatim), NOT a qualification authority, NOT an installation authority; NO source remediation, NO harness mutation, NO independent harness audit, NO auditor/model/provider execution, NO qualification, NO Campaign-2 recovery, NO Campaign-3; ZERO provider/model/frontier calls |
| Date | 2026-09-18 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-18) authorizes ONLY this publication of the Control Room readback disposition of the AUCDEV-023 authority bootstrap hardening (second bounded remediation) publication. It does NOT authorize source remediation, harness probes, independent audit, auditor/model/provider execution, qualification, installation, Campaign-2 recovery, or Campaign-3. |
| Exact governance base | `c36558dc4f791971643d53e033de38cff2ceea67` (the AUCDEV-023 authority bootstrap hardening remediation publication commit; tree `3ec8422e3d4152d83837b2374a6177a70ae4c62c`; sole parent `27c68fdc8175b0ae6cc6ed0b7ec594e956074864`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this readback's bootstrap |
| Subject | The AUCDEV-023 authority bootstrap hardening remediation (commit `c36558dc…`), its source hardening handoff, its recorded self-test evidence, the accepted closures CR-REMED-001/-003/-004, the partially accepted CR-REMED-002, and the NEW blocking finding AUCDEV023-CR-HARDEN-001 recorded by this readback |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **DEFERRED_PENDING_REMEDIATION** (§13) — deferred by decision, not waived; the exact target `c36558dc…` carries a known blocking authority-bootstrap provenance defect and must NOT consume independent audit authority |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `INFERENCE` (derived), `HYPOTHESIS` (unverified),
`REQUIREMENT` (task/record-mandated property).

## 1. Live bootstrap and mandatory state (OBSERVED_FACT)

Live `refs/heads/master` resolved EXACT
`c36558dc4f791971643d53e033de38cff2ceea67` (tree
`3ec8422e3d4152d83837b2374a6177a70ae4c62c`; sole parent
`27c68fdc8175b0ae6cc6ed0b7ec594e956074864`; single parent confirmed
via `git log --format=%P -1`).  All mandated documents and harness
sources were read at that exact SHA (`git cat-file`/`git show` at
`c36558dc`): CURRENT-STATE, BACKLOG, CONTROL-ROOM-RUNBOOK,
PROJECT-UPDATE-PROTOCOL, the hardening record
`AUCDEV-023-AUTHORITY-BOOTSTRAP-HARDENING-REMEDIATION.md`, the prior
readback record
`AUCDEV-023-TRUST-ANCHOR-LAUNCH-SPEC-REMEDIATION-READBACK.md`, and the
harness sources `qh/rootauth.py`, `qh/trusted_spec.py`, `qh/util.py`,
`qh/authority.py`, `qh/cli.py`, `tests/test_bootstrap_freeze.py`,
`tests/test_controller_binding.py`, `tests/test_spec_channel.py`,
`tests/test_seal_uapi.py`.  Confirmed governing state at that SHA:

```
AUCDEV-023                    = P1 / READY
remediation state             = IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK
                                (implementer RECOMMENDED position only)
independent harness audit     = DEFERRED_PENDING_CONTROL_ROOM_READBACK
AUCDEV-010                    = P1 / BLOCKED
Campaign-2                    = TERMINAL
qualification                 = NONE
installation                  = NONE
```

Pre-existing unrelated working-tree state preserved unstaged throughout
(unchanged from the prior sessions' records): `smoke-fixture` /
`smoke-fixture-103` gitlink drift and untracked `aucdev019-evidence/`.

## 2. Source hardening handoff — integrity VERIFIED (read-only)

`AUCDEV-023-AUTHORITY-BOOTSTRAP-HARDENING-handoff-20260918.tar.gz`
(`/home/isa/`), independently re-verified read-only by THIS publication
session (tar inspection + one isolated extraction to a temporary
directory for checksum recomputation only; content NOT executed;
nothing extracted into the repository):

- outer SHA-256
  `9e2a1860e29936a81ee2bce61195499a1746c7584f0f17ab9bc6fd745b224783`
  — EXACT match
- **220716 bytes** — EXACT match
- member census: **85 total = 75 regular files + 10 directories** — EXACT match
- unsafe/traversal paths: **0**; duplicate member names: **0**;
  symlink/hardlink/special members: **0**
- exactly ONE `SHA256SUMS`
  (`aucdev023-hardening-handoff/SHA256SUMS`)
- the `SHA256SUMS` contains **74 payload checksum entries**
- checksum verification: **74 / 74 PASS** (canonical `LC_ALL=C`
  re-hash of every payload member; 0 bad, 0 missing)

HANDOFF_INTEGRITY_VERIFIED_74_OF_74.

## 3. Control Room disposition (recorded verbatim)

```
AUCDEV_023_AUTHORITY_BOOTSTRAP_HARDENING_READBACK_PARTIALLY_ACCEPTED
/ LIVE_HEAD_C36558DC
/ HANDOFF_INTEGRITY_VERIFIED_74_OF_74
/ EXACT_23_PATH_REMEDIATION_VERIFIED
/ SKILL_TREE_UNCHANGED
/ CR_REMED_001_CLOSED_ACCEPTED
/ CR_REMED_003_CLOSED_ACCEPTED
/ CR_REMED_004_CLOSED_ACCEPTED
/ CR_REMED_002_PARTIAL_NOT_ACCEPTED
/ PRE_FREEZE_PRIVILEGED_CODE_PROVENANCE_NOT_ROOTED
/ LIVE_MUTABLE_TREE_SELF_PINNING
/ AUTHORITY_ROOT_PRELOAD_TOCTOU
/ HARNESS_TESTS_200_OF_200_ACCEPTED_AT_SELFTEST_STRENGTH
/ PRODUCT_NONREGRESSION_ACCEPTED
/ INDEPENDENT_HARNESS_AUDIT_DEFERRED
/ AUCDEV023_P1_READY
/ CAMPAIGN2_TERMINAL_UNCHANGED
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
```

## 4. Mechanically accepted publication facts (OBSERVED_FACT)

Re-derived mechanically by THIS session from git at the exact SHA:

- hardening commit `c36558dc4f791971643d53e033de38cff2ceea67`;
  tree `3ec8422e3d4152d83837b2374a6177a70ae4c62c`; sole parent
  `27c68fdc8175b0ae6cc6ed0b7ec594e956074864`;
- changed paths EXACTLY **23**
  (`git diff-tree --name-status -r 27c68fd c36558dc`): the NEW
  canonical hardening record
  `docs/chatgpt-project/AUCDEV-023-AUTHORITY-BOOTSTRAP-HARDENING-REMEDIATION.md`
  + CURRENT-STATE + BACKLOG + **20 `qualification-harness/` paths**
  (1 NEW fixture `fixtures/bound_controller.py`; 9 modified `qh/`
  modules incl. `rootauth.py`, `trusted_spec.py`, `util.py`,
  `authority.py`, `cli.py`; 10 test paths of which 5 NEW
  (`test_bootstrap_freeze.py`, `test_controller_binding.py`,
  `test_integrated_hardening.py`, `test_seal_uapi.py`,
  `test_spec_channel.py`) and 5 modified);
- `qualification-harness/` tree at `c36558dc` =
  `d296a5a20a369d1df37d6f0816e4d95d8f5a9e9d`
  (parent `27c68fd` harness tree
  `e9f3df95f2dc1144223b12a53f58ca6ad9062df6` — the hardening's
  confined, expected harness delta);
- `skill/` tree at `c36558dc` =
  `c792933a862d9a5434681a88d183470dd8b15d2f`
  — IDENTICAL at commit and parent (**SKILL_TREE_UNCHANGED**); no
  historical Campaign-2 artifact changed (changed-path confinement
  proves it mechanically).

EXACT_23_PATH_REMEDIATION_VERIFIED.

## 5. Accepted test evidence (implementation/self-test strength ONLY)

Accepted as recorded by the hardening publication (first-run outputs
preserved by that session; NOT re-executed by this zero-model
governance session; NOT an independent audit):

- qualification-harness suite: **200 / 200 PASS** (FIRST complete run
  of the final set; RED-first authoring and all development
  iterations recorded separately by the remediation session);
- targeted product non-regression: **34 / 34 PASS**;
- full product suite: **686 / 686 PASS + 99 subtests PASS**
  (HOST_NODE_PATH_DRIFT did not reproduce in that session — known
  PATH-order-dependent external condition, honestly recorded).

Acceptance of these numbers is acceptance of RECORDED
implementation/self-test evidence ONLY.  It is NOT an independent
verdict and does NOT extend to the pre-freeze provenance property at
issue in §10–§12.

## 6. CR-REMED-001 — CLOSED / ACCEPTED

`AUCDEV023-CR-REMED-001 = CLOSED / ACCEPTED`.  Accepted evidence
(observed in the exact `c36558dc` bytes):

- corrected, centralized Linux UAPI constants in `qh/util.py`
  (`MFD_CLOEXEC=0x0001`, `MFD_ALLOW_SEALING=0x0002`,
  `F_SEAL_SEAL=0x0001`, `F_SEAL_SHRINK=0x0002`, `F_SEAL_GROW=0x0004`,
  `F_SEAL_WRITE=0x0008`; platform `os.MFD_*` preferred; duplicates
  removed; the historical 0x0004/0x0010/0x0020/0x0040 defect
  documented as corrected);
- required seal mask `REQUIRED_SEALS = 0x000F`;
- populated memfd successfully sealed with the complete four-seal set;
  `F_GET_SEALS = 0x000F`; post-seal write/grow/shrink refused
  (recorded capability evidence; seal-UAPI test set green);
- authority-critical sealing MANDATORY on every authority path
  (root startup fails closed `AUTHORITY_CRITICAL_SEALING_UNAVAILABLE`
  when the representation cannot be established);
- the optional production downgrade REMOVED (the `--require-seals`
  flag no longer exists; there is no unsealed production mode);
- production fail-closed path demonstrated (test-only failing seal
  backend);
- trusted-spec channel refuses regular/unsealed sources (§7).

The historical `FOUR-SEAL MEMFD REPRESENTATION UNAVAILABLE` conclusion
(and residual R-1 as previously recorded) remains SUPERSEDED.

## 7. CR-REMED-003 — CLOSED / ACCEPTED

`AUCDEV023-CR-REMED-003 = CLOSED / ACCEPTED`.  Production
trusted-spec input (`qh/util.py::require_trusted_spec_fd`, wired into
the `qh root` CLI before any byte is read) now accepts ONLY:

- an operator-held **PIPE**; or
- a mechanically identified **fully sealed memfd** (discriminated by
  its `/proc/self/fd` `"/memfd:"` link target — not by `F_GET_SEALS`,
  which returns values even for ordinary files on this kernel class —
  and required to carry the COMPLETE `0x000F` seal set).

Ordinary file input (including stdin redirected from a file) is
REFUSED (`SPEC_SOURCE_KIND_REFUSED:file`); unsealed or partially
sealed memfd is REFUSED (`SPEC_MEMFD_SEALS_INCOMPLETE`).  Test set
green (`tests/test_spec_channel.py`).

## 8. CR-REMED-004 — CLOSED / ACCEPTED

`AUCDEV023-CR-REMED-004 = CLOSED / ACCEPTED`.  Trusted-spec schema v2
contains the OPERATOR-authored

```
authorized_controller.uid
authorized_controller.pid
authorized_controller.starttime
```

inside the canonical spec digest (changing the bound pid/starttime
changes the spec id).  Root mint acceptance verifies the exact
`SO_PEERCRED` uid/pid plus the ACTUAL `/proc/<pid>/stat` starttime of
the peer; supervisor request acceptance verifies the SAME pre-bound
identity again (fail-closed `AUTHORIZED_CONTROLLER_MISMATCH` /
`CONTROLLER_STARTTIME_MISMATCH` at both enforcement points).  A wrong
same-UID peer does NOT obtain authority.  A wrong-peer FIRST arrival
may terminally consume the one-shot root as fail-closed denial of
service — carried as:

```
R-6 = ACCEPTED RESIDUAL / FAIL-CLOSED DOS
```

Test set green (`tests/test_controller_binding.py`).

## 9. CR-REMED-002 — accepted portion (material improvement)

The following improvement IS accepted (observed in the exact
`c36558dc` bytes):

- the root freezes the **21-file privileged harness byte set** (19 qh
  modules + the two in-boundary payload fixtures) BEFORE exposing the
  controller trigger (`bind_socket` structurally refuses
  `ROOT_TRIGGER_BEFORE_BOOTSTRAP_FREEZE`; ledger order
  `BOOTSTRAP_FROZEN` precedes `ROOT_SOCKET_BOUND`);
- the frozen bundle is MANDATORILY sealed (`bundle_seal_status`
  required `sealed`; no optional downgrade);
- post-freeze NEW `qh.*` imports are denied by the planted meta_path
  guard (`QH_IMPORT_FROZEN`);
- the supervisor is created by `fork()` from the ALREADY-LOADED frozen
  root process state — no exec, no host-tree module search path; the
  old fresh-interpreter `python -m qh.cli supervisor` + host
  `PYTHONPATH` production path is REMOVED (the CLI `supervisor`
  subcommand is documented non-production);
- protected-child bytes are produced FROM the frozen bundle;
- host-tree mutation AFTER ROOT READY cannot substitute the supervisor
  (attacker unique-marker regressions, including delete/recreate,
  pass).

These are MATERIAL improvements.  They do NOT establish complete
root-bootstrap provenance; the blocking residual is §10–§11.

## 10. NEW blocking finding AUCDEV023-CR-HARDEN-001

```
Finding ID    : AUCDEV023-CR-HARDEN-001
Classification: HARNESS/PROTOCOL DEFECT
               / AUTHORITY_ROOT_BOOTSTRAP_PROVENANCE
               / PRE_FREEZE_MUTABLE_TREE_SELF_PINNING_TOCTOU
Support       : OBSERVED_FACT + direct trust-boundary inference
Status        : BLOCKING — CR-REMED-002 closure NOT accepted
```

Observed source facts at exact `c36558dc` (each verified read-only by
THIS session in the exact bytes):

**A.** `qh/rootauth.py` imports privileged harness modules at ordinary
Python module-load time BEFORE `PrivilegedBootstrap.freeze()` can
execute (module-level `from . import trusted_spec`, `from .authority
import …`, `from .ledger import ObservabilityLedger`,
`from .trusted_spec import HARNESS_EXEC_RELPATHS`, `from .util import
…`, plus transitive privileged qh dependencies; `freeze()` is a
classmethod invoked later from the `AuthorityRoot` startup flow).

**B.** The trusted-spec authoring helper (`build_spec`) computes
`spec["harness"]["tree_digest"]` by hashing the CURRENT LIVE
`harness_root` filesystem tree (`harness_tree_digest(harness_root)`).
There is no separately pre-authorized immutable harness digest / Git
source identity supplied as the expected value.

**C.** Schema v2 REQUIRES the authorized controller pid/starttime
inside the spec (`authorized_controller` is a mandatory canonical-digest
field; `build_spec` takes `controller_pid`/`controller_starttime`
arguments).  Therefore the authorized controller process necessarily
exists before the final trusted spec can be authored.

**D.** The held threat model permits that same-UID controller to
modify ordinary user-owned filesystem state (the design's own premise:
the root exists to be a mechanical root of trust OUTSIDE the untrusted
same-UID controller).

**E.** `PrivilegedBootstrap.freeze()` reads the live host files,
compares those bytes with the spec digest, then loads privileged
modules through ordinary Python import state (`importlib.import_module`).
For ALREADY-LOADED modules (including the §10.A module-level
preloads), the freeze verifies only their filesystem location
(`mod.__file__` under the pinned tree) — not that their EXECUTING
Python code objects were mechanically instantiated from the verified
sealed byte representation (`module_ids` records digests of the file
bytes; the sealed bundle is packed after the load).

## 11. Trust gap

The current mechanism protects against host harness mutation AFTER
the successful freeze / root-ready boundary.  It does NOT
mechanically establish provenance for privileged code loaded BEFORE
that boundary.  Two classes remain unclosed:

**A. PRE-SPEC SELF-PINNING.**  If the untrusted same-UID controller
changes the mutable harness tree before the operator's final spec
authoring, `build_spec()` hashes the CHANGED tree and places that
current value into the trusted spec.  The mutable tree has therefore
selected the value used as its own expected identity
(LIVE_MUTABLE_TREE_SELF_PINNING).

**B. VERIFY-THEN-IMPORT / PRELOADED-CODE GAP.**  Even when the spec
digest represents good bytes, the code performing root authority
decisions is initially loaded through the ordinary mutable host Python
import path.  Filesystem-byte verification AFTER that load does not
mechanically prove that the already-executing privileged Python code
was instantiated from the verified sealed byte representation
(AUTHORITY_ROOT_PRELOAD_TOCTOU).  A same-UID pre-freeze
modification/restoration race is therefore outside the current
post-ready attacker tests.

## 12. Existing test limit

The current attacker regressions successfully test mutation AFTER the
root has frozen and become ready (`test_bootstrap_freeze.py`:
host-harness module replacement and delete/recreate after ROOT READY —
attacker marker never executes).  The pre-root drift tests demonstrate
that benign/currently-loaded code detects a changed host file
(`verify_loaded_modules`).  They do NOT establish security against a
malicious modification of the privileged root/bootstrap code that
performs that detection itself.  Therefore:

```
POST_FREEZE_IMMUTABILITY               = ACCEPTED
PRE_FREEZE_PRIVILEGED_CODE_PROVENANCE  = NOT_ESTABLISHED
```

## 13. Governing remediation result

NOT accepted as the final governing remediation result:

```
AUCDEV023_AUTHORITY_BOOTSTRAP_HARDENING_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK
```

Published instead:

```
AUCDEV023_AUTHORITY_BOOTSTRAP_HARDENING_READBACK_PARTIALLY_ACCEPTED
/ FINAL_PRE_CONTROLLER_BOOTSTRAP_PROVENANCE_REMEDIATION_REQUIRED
```

AUCDEV-023 remains **P1 / READY** (NOT DONE).  Independent harness
audit remains **DEFERRED_PENDING_REMEDIATION** — do NOT spend
independent audit authority on `c36558dc…`.  G-1/G-2 design/probe
closures remain historical accepted evidence and are NOT reopened;
the next change is the bounded pre-controller provenance remediation
of §14, not a return to design research or another qualification-
harness redesign.

## 14. Next bounded objective (RECORDED, NOT EXECUTED)

```
AUCDEV-023 PRE-CONTROLLER IMMUTABLE AUTHORITY-BOOTSTRAP PROVENANCE
REMEDIATION
```

This publication records but does NOT execute and does NOT authorize
it (separate operator authorization required).  The next remediation
must be limited to this ONE trust-root gap.  Required property:

The privileged authority/root code identity MUST be frozen from a
trusted, operator-controlled source BEFORE the untrusted controller
can modify the ordinary harness tree.  A later live mutable tree must
NOT be allowed to define its own expected identity.  The authority
root must not initially execute security-critical qh code from a
controller-writable ordinary tree and then attempt to prove that code
trustworthy after execution has begun.

## 15. Required design direction for the next remediation

The implementation may choose the smallest mechanism satisfying the
property.  A strongly preferred bounded pattern:

1. PRE-CONTROLLER PHASE: while the untrusted controller does not yet
   exist, establish the exact privileged harness byte set and place it
   into a fully sealed operator-held authority bundle;
2. start/load the trusted authority bootstrap from that already
   frozen representation, or keep a long-lived pre-controller
   authority-bootstrap process containing those trusted loaded bytes;
3. only AFTER the privileged bootstrap is immutable, start the
   controller;
4. obtain the operator-authorized controller uid/pid/starttime;
5. complete/finalize the launch spec through an operator-held
   capability channel;
6. require the final spec's harness identity to match the
   already-frozen PRE-CONTROLLER authority bundle identity;
7. expose the controller trigger only after that match;
8. fork the supervisor from that frozen authority state as already
   accepted.

The exact mechanism remains implementer-owned.  Do NOT broaden this
into another qualification-harness redesign.

## 16. Required future negative evidence

The future remediation must demonstrate:

- controller starts only AFTER privileged bootstrap identity is
  frozen;
- controller modifies ordinary host `qh/rootauth.py` before final spec
  completion → trusted privileged code remains the pre-controller
  frozen version OR the root refuses;
- controller modifies `qh/authority.py`, `qh/util.py`,
  `qh/trusted_spec.py` before final spec completion → attacker marker
  never executes;
- controller modifies the entire ordinary harness tree before final
  spec completion → final spec cannot bless that changed tree as the
  authority identity;
- restoring original files after malicious privileged code load cannot
  make the run appear trusted;
- operator final spec harness identity must equal the PRE-CONTROLLER
  frozen authority identity;
- mismatch → fail closed before controller trigger;
- sealed bootstrap bundle remains immutable;
- already-accepted CR-REMED-001/003/004 behavior remains green.

## 17. Held accepted state (preserved EXACTLY)

```
CR-REMED-001 = CLOSED / ACCEPTED
CR-REMED-003 = CLOSED / ACCEPTED
CR-REMED-004 = CLOSED / ACCEPTED
IR-003       = CLOSED / ACCEPTED
R-6          = ACCEPTED RESIDUAL / FAIL-CLOSED DOS
provider adapters = accepted at SYNTHETIC strength
hard no-egress = held
GATE-W = held
C-1/C4′ = held
claim-only controller request = held
mandatory sealing = held
pipe/sealed-memfd spec channel = held
authorized controller double-check = held
skill tree unchanged
Campaign-2 terminal
```

## 18. Campaign / qualification held state (preserved EXACTLY)

```
AUDITOR_A_AUTHORITY              = CONSUMED_CLOSED
AUDITOR_B_AUTHORITY              = CONSUMED_CLOSED
MODEL_ENGAGEMENTS_AUTHORIZED     = 2
MODEL_ENGAGEMENTS_USED           = 2
FIRST_PASS_A                     = PRESENT / FROZEN
FIRST_PASS_B                     = ABSENT
FIRST_PASS_BARRIER               = CLOSED
NO_CONFORMING_BLIND_FIRST_PASS_SET
CAMPAIGNS                        = 2 OF MAX 2
CAMPAIGN_3                       = NOT AUTHORIZED / DOES NOT EXIST
AUCDEV-010                       = P1 / BLOCKED
QUALIFICATION                    = NONE
INSTALLATION                     = NONE
```

No historical verdict changed; no frozen artifact touched.

## 19. Current-facing state after this publication

```
Active/current item       : AUCDEV-023 / P1 / READY
remediation state         : PARTIALLY_ACCEPTED
                            / FINAL_PRE_CONTROLLER_BOOTSTRAP_
                              PROVENANCE_REMEDIATION_REQUIRED
independent harness audit : DEFERRED_PENDING_REMEDIATION
```

Next action EXACTLY ONE:

```
INDEPENDENT CONTROL ROOM READBACK OF THIS HARDENING-READBACK
GOVERNANCE PUBLICATION.
```

This publication does NOT authorize source remediation.  BACKLOG
counts UNCHANGED (mechanically recounted by this session: 19 open =
READY 9 / OPEN 7 / BLOCKED 3; P0 2 / P1 7 / P2 11 = 20 queue rows;
3 DEFERRED; 8 ACCEPTED_RESIDUAL; 5 DONE).
