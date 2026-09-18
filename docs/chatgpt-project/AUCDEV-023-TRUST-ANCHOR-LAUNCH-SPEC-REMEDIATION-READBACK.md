# AUCDEV-023 — Trust-Anchor and Launch-Spec Binding Remediation: Control Room Readback (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION SESSION ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room decision-maker (this session publishes the Control Room's already-reached readback disposition verbatim), NOT a qualification authority, NOT an installation authority; NO remediation implementation, NO harness mutation, NO independent harness audit, NO auditor/model/provider execution, NO qualification, NO Campaign-2 recovery, NO Campaign-3; ZERO provider/model/frontier calls |
| Date | 2026-09-18 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-18) authorizes ONLY this publication of the Control Room readback disposition of the AUCDEV-023 trust-anchor and launch-spec binding remediation publication. It does NOT authorize source remediation, harness probes, independent audit, auditor/model/provider execution, qualification, installation, Campaign-2 recovery, or Campaign-3. |
| Exact governance base | `947f28244d7cae263f2e6fbb3025f94cfba7f4dc` (the AUCDEV-023 trust-anchor and launch-spec binding remediation publication commit; tree `42e07f54ca27db2589c92350da07b8a5543c6646`; sole parent `2e53ad583b00fbec6f62fcd0f80f39bd4acbfabd`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this readback's bootstrap |
| Subject | The AUCDEV-023 trust-anchor and launch-spec binding remediation (commit `947f2824…`), its source remediation handoff, its recorded self-test evidence, its accepted remediation portions, and the four NEW blocking findings AUCDEV023-CR-REMED-001/-002/-003/-004 recorded by this readback |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **DEFERRED_PENDING_REMEDIATION** (§13) — deferred by decision, not waived; the exact target `947f2824…` carries known blocking trust-bootstrap defects and must NOT consume independent audit authority |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `INFERENCE` (derived), `HYPOTHESIS` (unverified),
`REQUIREMENT` (task/record-mandated property).

## 1. Live bootstrap and mandatory state (OBSERVED_FACT)

Live `refs/heads/master` resolved EXACT
`947f28244d7cae263f2e6fbb3025f94cfba7f4dc` (tree
`42e07f54ca27db2589c92350da07b8a5543c6646`; sole parent
`2e53ad583b00fbec6f62fcd0f80f39bd4acbfabd`; local `HEAD`, `master` and
`origin/master` identical).  All mandated documents and harness sources
were read at that exact SHA (`git cat-file` at `947f2824`):
CURRENT-STATE, BACKLOG, CONTROL-ROOM-RUNBOOK,
PROJECT-UPDATE-PROTOCOL, the remediation record
`AUCDEV-023-TRUST-ANCHOR-LAUNCH-SPEC-REMEDIATION.md`, the prior
implementation-readback record
`AUCDEV-023-QUALIFICATION-HARNESS-IMPLEMENTATION-READBACK.md`, and the
harness sources `qh/util.py`, `qh/custody.py`, `qh/rootauth.py`,
`qh/authority.py`, `qh/cli.py`, `qh/trusted_spec.py`,
`tests/test_sealing.py`, `tests/test_rootauth.py`,
`tests/test_trusted_claims.py`.  Confirmed governing state at that SHA:

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
(this session observed it unchanged from the remediation session's
record): `smoke-fixture` / `smoke-fixture-103` gitlink drift (mode
160000; index entries unchanged) and untracked `aucdev019-evidence/`.

## 2. Source remediation handoff — integrity VERIFIED (read-only)

`AUCDEV-023-TRUST-ANCHOR-REMEDIATION-handoff-20260918.tar.gz`
(`/home/isa/`), independently re-verified read-only by THIS publication
session (in-memory tar inspection only; content NOT executed; nothing
extracted into the repository):

- outer SHA-256
  `4625f1769a7ded40ff4309b122ac9e3a6e5b21a1b2bb410ceaf899dd5eb83198`
  — EXACT match
- **222014 bytes** — EXACT match
- member census: **70 total = 63 regular files + 7 directories** — EXACT match
- unsafe/traversal paths: **0**; duplicate member names: **0**;
  symlink/hardlink/special members: **0**
- exactly ONE `SHA256SUMS`
  (`aucdev023-remediation-handoff/SHA256SUMS`)
- the `SHA256SUMS` contains **62 payload checksum entries**
  (`./`-prefixed, relative to the archive top-level directory)
- checksum verification: **62 / 62 PASS** (each payload member's bytes
  re-hashed in memory against its recorded entry; 0 bad, 0 missing)

HANDOFF_INTEGRITY_VERIFIED_62_OF_62.

## 3. Control Room disposition (recorded verbatim)

```
AUCDEV_023_TRUST_ANCHOR_REMEDIATION_READBACK_PARTIALLY_ACCEPTED
/ LIVE_HEAD_947F2824
/ HANDOFF_INTEGRITY_VERIFIED_62_OF_62
/ EXACT_29_PATH_REMEDIATION_VERIFIED
/ SKILL_TREE_UNCHANGED
/ HARNESS_TESTS_158_OF_158_ACCEPTED
/ PRODUCT_REGRESSION_34_OF_34_AND_686_OF_686_ACCEPTED
/ IR003_CLOSED_ACCEPTED
/ SYNTHETIC_PROVIDER_ADAPTERS_ACCEPTED
/ IR001_IR002_CLOSURE_NOT_ACCEPTED
/ MEMFD_AND_SEAL_CONSTANTS_INVALID
/ SEAL_CAPABILITY_CONCLUSION_INVALID
/ AUTHORITY_CRITICAL_SEAL_REQUIREMENT_NOT_ESTABLISHED
/ TRUSTED_SPEC_CHANNEL_NOT_PIPE_ONLY
/ SUPERVISOR_BOOTSTRAP_CODE_NOT_IMMUTABLY_ROOTED
/ AUTHORIZED_CONTROLLER_TRIGGER_NOT_ROOT_BOUND
/ REMEDIATION_COMPLETE_CLAIM_NOT_ACCEPTED
/ INDEPENDENT_HARNESS_AUDIT_DEFERRED
/ AUCDEV023_P1_READY
/ CAMPAIGN2_TERMINAL_UNCHANGED
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
```

## 4. Mechanically accepted publication facts (OBSERVED_FACT)

Re-derived mechanically by THIS session from git at the exact SHA:

- remediation commit `947f28244d7cae263f2e6fbb3025f94cfba7f4dc`;
  tree `42e07f54ca27db2589c92350da07b8a5543c6646`; sole parent
  `2e53ad583b00fbec6f62fcd0f80f39bd4acbfabd` (single parent confirmed
  via `git rev-list --parents -n 1`);
- changed paths EXACTLY **29** (`git diff --name-only 2e53ad5..947f282`):
  26 `qualification-harness/` paths (17 modified + 9 NEW, including
  `qh/rootauth.py`, `qh/trusted_spec.py`, `qh/adapters.py`,
  `tests/test_sealing.py`, `tests/test_trusted_spec.py`,
  `tests/test_rootauth.py`, `tests/test_production_surface.py`,
  `tests/test_trusted_claims.py`, `tests/test_provider_adapters.py`)
  + CURRENT-STATE + BACKLOG + the NEW canonical remediation record;
- `qualification-harness/` tree at `947f2824` =
  `e9f3df95f2dc1144223b12a53f58ca6ad9062df6`
  (parent `2e53ad5` harness tree
  `43ea608921b79142d12417c7856b4198ea7db4b3` — the remediation's
  confined, expected harness delta);
- `skill/` tree at BOTH `2e53ad5` and `947f2824` =
  `c792933a862d9a5434681a88d183470dd8b15d2f` — **UNCHANGED**;
- no other path changed between parent and child.

The prior HOST_NODE_PATH_DRIFT remains a known PATH-order-dependent
external condition even though it did not reproduce in the remediation
session (recorded honestly there; unchanged classification).

## 5. Accepted test evidence (implementation/self-test strength ONLY)

Accepted as RECORDED evidence at implementation/self-test strength
(publisher-recorded; NOT independently re-executed by this readback;
NOT an independent verdict):

- qualification-harness deterministic suite: **158 / 158 PASS**
  (first complete run of the final set; development iterations
  recorded separately in the remediation record);
- targeted product non-regression: **34 / 34 PASS**;
- full product deterministic suite: **686 / 686 PASS** plus
  **99 subtests PASS**.

Acceptance of these test RESULTS does not extend to the soundness of
the mechanisms the tests exercise where this readback records a
blocking finding (in particular `tests/test_sealing.py` exercises the
INVALID constants of CR-REMED-001 and therefore cannot establish the
claimed seal-capability conclusion; see §7).

## 6. Accepted remediation portions (implementation/self-test strength ONLY)

Accepted at implementation/self-test strength:

- **A.** public unrestricted `qh mint` REMOVED;
- **B.** root-held spec/custody architecture direction;
- **C.** controller request reduced to claim-only fields;
- **D.** security-critical bind/path/hash fields removed from
  controller authority;
- **E.** spec-bound evidence/target/auditor-output/Codex identities;
- **F.** protected-child trusted snapshot concept;
- **G.** production `--yama-override` REMOVAL;
- **H.** production `--fault` REMOVAL;
- **I.** real-Yama read on the production root/supervisor path;
- **J.** `codex_chatgpt_oauth_v1` synthetic concrete adapter;
- **K.** `claude_firstparty_oauth_v1` synthetic concrete adapter;
- **L.** `synthetic_inert_v1` rehearsal adapter;
- **M.** hard-no-egress, C-1/C4′, GATE-W and engagement-accounting
  non-regression.

Therefore:

```
AUCDEV023-CR-IMPL-003 = CLOSED / ACCEPTED
```

at implementation/self-test strength (production Yama/test-hook
override bypass eliminated: the production parser rejects
`--yama-override`/`--fault` on every subcommand; SupervisorPolicy
structurally override-free; real-knob Yama always).

These accepted portions are NOT acceptance of the complete
authority-root trust chain: IR-001/IR-002 closure remains NOT accepted
(§7, §8, §9, §10).

## 7. NEW blocking finding AUCDEV023-CR-REMED-001

```
Finding ID    : AUCDEV023-CR-REMED-001
Classification: HARNESS/PROTOCOL DEFECT
               / AUTHORITY_STATE_SEALING
               / LINUX_UAPI_CONSTANT_MISIDENTIFICATION
Support       : OBSERVED_FACT
Status        : BLOCKING — IR-001 closure NOT accepted
```

Live source at `947f2824` defines (OBSERVED_FACT,
`qualification-harness/qh/util.py:147-153` and the same values in
`qh/custody.py:49-53,102-103`):

```python
MFD_ALLOW_SEALING = 0x0004
F_SEAL_WRITE      = 0x0008
F_SEAL_GROW       = 0x0010
F_SEAL_SHRINK     = 0x0020
F_SEAL_SEAL       = 0x0040
```

Linux UAPI defines (verified against this host's authoritative headers
`/usr/include/linux/memfd.h:8-10` and
`/usr/include/linux/fcntl.h:47-52`; kernel `7.2.2-1-cachyos`):

```
MFD_CLOEXEC       = 0x0001    F_SEAL_SEAL     = 0x0001
MFD_ALLOW_SEALING = 0x0002    F_SEAL_SHRINK   = 0x0002
MFD_HUGETLB       = 0x0004    F_SEAL_GROW     = 0x0004
                              F_SEAL_WRITE    = 0x0008
                              F_SEAL_FUTURE_WRITE = 0x0010
                              F_SEAL_EXEC     = 0x0020
```

Therefore:

- the source's `MFD_ALLOW_SEALING = 0x0004` actually requests
  `MFD_HUGETLB` (a hugetlb memfd WITHOUT sealing permission) — which
  mechanically explains the remediation's observed
  `write(2)/ftruncate(2) → EINVAL` and `F_ADD_SEALS → EINVAL`
  behaviour on a host without a configured hugepage pool;
- the source's seal mask `_ALL_FOUR_SEALS = 0x0088` is actually
  `F_SEAL_WRITE | F_SEAL_FUTURE_WRITE` (and `F_SEAL_GROW`-as-0x0010 /
  `F_SEAL_SHRINK`-as-0x0020 / `F_SEAL_SEAL`-as-0x0040 are not the
  intended UAPI seal bits at all);
- the remediation's seal-capability probe (`qh/util.py` §sealing) and
  its corresponding test (`tests/test_sealing.py`, which imports the
  same constants) do NOT exercise the intended Linux sealing API.

The observed EINVAL / `unavailable_kernel` result therefore CANNOT
establish that the host lacks populated sealed-memfd support.  The
recorded residual

```
R-1 FOUR-SEAL MEMFD REPRESENTATION UNAVAILABLE ON THIS HOST CLASS
```

is **NOT accepted**.  The current OPTIONAL `--require-seals` does not
satisfy the remediation requirement that authority-critical sealed
state must FAIL CLOSED if the required representation cannot be
established (the default production path proceeds with
`seal_status=unavailable_kernel`).  Therefore:

```
AUTHORITY_CRITICAL_SEAL_REQUIREMENT = NOT ESTABLISHED
```

and IR-001 cannot yet be accepted as fully closed.

## 8. NEW blocking finding AUCDEV023-CR-REMED-002

```
Finding ID    : AUCDEV023-CR-REMED-002
Classification: HARNESS/PROTOCOL DEFECT
               / TRUST_ROOT_BOOTSTRAP
               / SUPERVISOR_CODE_NOT_IMMUTABLY_ROOTED
Support       : OBSERVED_FACT + direct trust-boundary inference
Status        : BLOCKING — IR-002 closure NOT accepted
```

The protected boundary child uses verified memfd snapshot bytes — that
portion is accepted (portion F).

However the privileged supervisor itself is spawned AFTER the authority
root has accepted the mint request (OBSERVED_FACT:
`qh/rootauth.py` `handle_mint_request` → `_spawn_supervisor(grant)` at
mint time) using:

```python
argv = [sys.executable, "-m", "qh.cli", "supervisor", ...]
env  = dict(os.environ, PYTHONPATH=harness_root + os.pathsep + ...)
```

with `harness_root = self.spec["harness"]["root"]` — an ordinary host
filesystem path (`Path(harness_root).resolve()` in
`qh/trusted_spec.py`).  The supervisor therefore imports its privileged
authority/custody code from the ordinary host harness tree.

Under the held threat model the same-UID controller may
write/delete/recreate ordinary user-owned filesystem state.  The
authority root does NOT snapshot and execute the supervisor/bootstrap
code from immutable authority-held bytes before controller execution
begins; a same-UID controller has a modification window between
legitimate root startup and supervisor spawn in which the host Python
harness tree may change.  The later supervisor-side
`TRUSTED_SPEC_VERIFY` (which itself checks against the LIVE filesystem)
cannot establish trust in the code performing that verification when
that code was loaded from the mutable surface.  The protected-child
snapshot begins too late to close the root-to-supervisor bootstrap
chain.  Therefore:

```
SUPERVISOR_BOOTSTRAP_TRUST = NOT ESTABLISHED
```

and IR-002 closure is NOT accepted.

## 9. NEW blocking finding AUCDEV023-CR-REMED-003

```
Finding ID    : AUCDEV023-CR-REMED-003
Classification: HARNESS/PROTOCOL DEFECT
               / TRUSTED_SPEC_INPUT_CHANNEL
               / ORDINARY_FILE_AUTHORITY_INPUT_PERMITTED
Support       : OBSERVED_FACT
Status        : BLOCKING — production trusted-spec input channel
```

The production root CLI reads `--spec-fd` with
`os.read(args.spec_fd, 1 << 20)` (`qh/cli.py:_cmd_root`) but performs
NO source-kind check.  Its own source comment explicitly permits
"pipe or regular file redirect".

The trusted launch spec is security-critical authority input.  Under
the held same-UID threat model an ordinary user-owned file is NOT a
trust boundary.  Because the spec id is computed only AFTER the root
reads the supplied bytes, a modified ordinary spec file simply becomes
a newly self-consistent authoritative spec.  The production root must
mechanically require an operator-held pipe/memfd/process capability for
trusted spec input, analogous to the custody source rule
(`CUSTODY_SOURCE_KIND_REFUSED:file`).  Regular-file spec input is NOT
acceptable as production authority input.

## 10. NEW blocking finding AUCDEV023-CR-REMED-004

```
Finding ID    : AUCDEV023-CR-REMED-004
Classification: HARNESS/PROTOCOL DEFECT
               / AUTHORIZED_CONTROLLER_TRIGGER_BINDING
               / ROOT_DOES_NOT_PREBIND_CONTROLLER_INSTANCE
Support       : OBSERVED_FACT + REQUIREMENT GAP
Status        : BLOCKING — authorized controller instance not root-bound
```

The root mint endpoint (`qh/rootauth.py:handle_mint_request`) currently
accepts the FIRST peer whose request contains the spec-bound attempt
id.  The trusted launch spec does NOT contain a pre-authorized
controller PID/starttime or equivalent root-issued controller
capability.

The supervisor then constructs the controller binding from whichever
peer connects (OBSERVED_FACT, `qh/authority.py`):
`SO_PEERCRED` peer PID + that peer's CURRENT starttime
(`_proc_starttime(peer_pid)`) + that peer's environment claims.  This
verifies the connected process's actual environment but does NOT
establish that the process is the controller instance previously
authorized by the operator root.  A same-UID unrelated process with
knowledge of the attempt/socket and the expected controller scope must
not be able to become the authorized controller merely by connecting
first and presenting a compatible environment.

The remediation task explicitly required the authorized controller
instance to be bound from trusted-root state.  That requirement is NOT
mechanically established.

## 11. Provider adapter status

Accepted at SYNTHETIC / implementation-self-test strength:

- `codex_chatgpt_oauth_v1`
- `claude_firstparty_oauth_v1`
- `synthetic_inert_v1`

The historical non-secret evidence supports the named runtime
materialization surfaces.  NO real credentials were used.  NO
campaign-ready live credential integration is claimed.  The adapters
remain subject to the corrected authority-root/bootstrap chain
(§7–§10) and the future independent harness audit (§13).

## 12. Governing remediation result

NOT accepted as the governing result:

```
AUCDEV023_TRUST_ANCHOR_REMEDIATION_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK
```

Published instead:

```
AUCDEV023_TRUST_ANCHOR_REMEDIATION_READBACK_PARTIALLY_ACCEPTED
/ SECOND_BOUNDED_REMEDIATION_REQUIRED_BEFORE_INDEPENDENT_HARNESS_AUDIT
```

AUCDEV-023 remains **P1 / READY** (NOT DONE).  G-1/G-2 design/probe
closures remain historical accepted evidence and are NOT reopened; the
next change is the bounded authority-bootstrap hardening remediation of
§7–§10, not a return to design research.

## 13. Independent harness audit — DEFERRED

```
DEFERRED_PENDING_REMEDIATION
```

The exact target `947f2824…` has known blocking trust-bootstrap defects
(§7–§10).  Independent audit authority must NOT be spent on this SHA.
A changed remediation SHA requires a fresh independent audit after:

```
second bounded remediation
→ Control Room readback
→ exact target freeze
```

## 14. Next bounded objective (RECORDED, NOT EXECUTED)

```
AUCDEV-023 AUTHORITY BOOTSTRAP HARDENING REMEDIATION
```

This publication records but does NOT execute and does NOT authorize
it.  The future remediation is limited to:

- **A.** correct Linux memfd/seal constants and mechanically
  re-establish the actual host sealing capability;
- **B.** make mandatory authority-critical sealing fail closed on the
  operational production path — no optional downgrade;
- **C.** mechanically root the privileged supervisor/bootstrap code in
  immutable authority-held bytes loaded before controller-controlled
  execution can mutate ordinary harness files;
- **D.** remove ordinary-file trusted-spec input from the production
  root;
- **E.** bind the authorized controller trigger to trusted-root state
  rather than letting the first compatible same-UID peer define itself
  as the controller;
- **F.** preserve the already accepted claim-only launch spec,
  adapters, no-egress, GATE-W and C-1 behavior.

No broad redesign.

## 15. Campaign / qualification held state (preserved EXACTLY)

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

## 16. Current-facing state after this publication

```
Active/current item       : AUCDEV-023 / P1 / READY
remediation state         : PARTIALLY_ACCEPTED
                            / SECOND_BOUNDED_REMEDIATION_REQUIRED
independent harness audit : DEFERRED_PENDING_REMEDIATION
```

G-1/G-2 design/probe readiness closures remain historical accepted
evidence.  Next action EXACTLY ONE:

```
INDEPENDENT CONTROL ROOM READBACK OF THIS REMEDIATION-READBACK
GOVERNANCE PUBLICATION.
```

This publication itself does NOT authorize source remediation.

Result: `AUCDEV_023_TRUST_ANCHOR_REMEDIATION_READBACK_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
