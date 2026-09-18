# AUCDEV-023 — Pre-Controller Immutable Authority-Bootstrap Provenance Remediation (Canonical Record)

| Field | Value |
|---|---|
| Session class | BOUNDED ZERO-PROVIDER REMEDIATION IMPLEMENTATION SESSION (operator-authorized AUCDEV-023 PRE-CONTROLLER IMMUTABLE AUTHORITY-BOOTSTRAP PROVENANCE REMEDIATION against the known blocker AUCDEV023-CR-HARDEN-001 ONLY) — NOT Auditor A/B, NOT the Control Room, NOT a qualification authority, NOT an installation authority, NOT an independent harness audit; NO auditor/model/provider execution; NO Campaign-2 recovery; NO Campaign-3; NO product (`skill/`) modification; NO reopening of accepted closures (CR-REMED-001/-003/-004, IR-003, C-1/C4′, GATE-W, no-egress, provider adapters, engagement accounting, protected-child frozen-byte execution, `skill/` non-interference); the harness was NOT self-audited |
| Date | 2026-09-18 (Europe/Istanbul) |
| Exact remediation base | `54fb4e0c07841cbc725ca317ae2d4987557f1220` (tree `86a7cb701b2281414f218920e12a824d97d3611f`; sole parent `c36558dc4f791971643d53e033de38cff2ceea67`; qualification-harness tree `d296a5a20a369d1df37d6f0816e4d95d8f5a9e9d`; skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this remediation's bootstrap and re-resolved EXACT immediately before staging; THIS publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Remediation scope | Close ONLY AUCDEV023-CR-HARDEN-001 / AUTHORITY_ROOT_BOOTSTRAP_PROVENANCE / PRE_FREEZE_MUTABLE_TREE_SELF_PINNING_TOCTOU (readback §10–§12 trust gaps A and B: PRE-SPEC SELF-PINNING and VERIFY-THEN-IMPORT / PRELOADED-CODE) |
| Disposition (recommended) | `AUCDEV023_PRE_CONTROLLER_BOOTSTRAP_PROVENANCE_REMEDIATION_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK` (§24) — implementer position ONLY, NOT an independent verdict |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **STILL REQUIRED — DEFERRED_PENDING_CONTROL_ROOM_READBACK of THIS remediation** (not executed in this session; a verdict on any earlier SHA does not transfer) |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `INFERENCE` (derived), `HYPOTHESIS` (unverified),
`REQUIREMENT` (task/record-mandated property).

## 1. Base identities and confirmed governing state (OBSERVED_FACT)

Live `refs/heads/master` resolved EXACT `54fb4e0c07841cbc725ca317ae2d4987557f1220`
(tree `86a7cb701b2281414f218920e12a824d97d3611f`; sole parent
`c36558dc4f791971643d53e033de38cff2ceea67`; qualification-harness tree
`d296a5a20a369d1df37d6f0816e4d95d8f5a9e9d`; skill tree
`c792933a862d9a5434681a88d183470dd8b15d2f`).  All mandated documents and
harness sources were read at that exact SHA.  Confirmed governing state:

```
AUCDEV-023                    = P1 / READY
AUCDEV023-CR-HARDEN-001       = BLOCKING
CR-REMED-001                  = CLOSED / ACCEPTED (held)
CR-REMED-003                  = CLOSED / ACCEPTED (held)
CR-REMED-004                  = CLOSED / ACCEPTED (held)
independent harness audit     = DEFERRED_PENDING_REMEDIATION
Campaign-2                    = TERMINAL
AUCDEV-010                    = P1 / BLOCKED
qualification                 = NONE
installation                  = NONE
```

Pre-existing unrelated working-tree state preserved unstaged throughout
(unchanged from the prior sessions' records; the nested fixture repo
gitlink HEADs MATCH the recorded gitlinks — only inner untracked
`audit-output/` fixtures) and untracked `aucdev019-evidence/`.

## 2. Exact changed paths (OBSERVED_FACT)

MODIFIED (15, all under `qualification-harness/`):

```
qualification-harness/qh/cli.py
qualification-harness/qh/compose.py
qualification-harness/qh/rootauth.py
qualification-harness/qh/trusted_spec.py
qualification-harness/qh/util.py
qualification-harness/tests/test_bootstrap_freeze.py
qualification-harness/tests/test_compose.py
qualification-harness/tests/test_controller_binding.py
qualification-harness/tests/test_integrated_hardening.py
qualification-harness/tests/test_production_surface.py
qualification-harness/tests/test_rootauth.py
qualification-harness/tests/test_seal_uapi.py
qualification-harness/tests/test_spec_channel.py
qualification-harness/tests/test_trusted_claims.py
qualification-harness/tests/test_trusted_spec.py
```

NEW (1 + 1 report + 2 governance appends):

```
qualification-harness/tests/test_precontroller_provenance.py
docs/chatgpt-project/AUCDEV-023-PRE-CONTROLLER-IMMUTABLE-AUTHORITY-BOOTSTRAP-PROVENANCE-REMEDIATION.md
docs/chatgpt-project/AUCDEV-CURRENT-STATE.md   (append-only)
docs/chatgpt-project/AUCDEV-BACKLOG.md         (append-only)
```

Total **19 staged paths**, confined EXACTLY to the authorized mutation
families (`qualification-harness/**`, CURRENT-STATE, BACKLOG, the NEW
remediation report).  `qh/authority.py` (supervisor), `qh/boundary*.py`,
`qh/bootstrap.py`, `qh/custody.py`, `qh/gatew.py`, `qh/noegress.py`,
`qh/codex_profile.py`, `qh/ledger.py`, `qh/statemachine.py`,
`qh/campaign.py`, `qh/adapters.py`, `fixtures/**` and `conftest.py` are
NOT modified (held closures preserved by construction).  `test-outputs/`
remains gitignored local evidence (archived in the handoff, not
committed).

## 3. CR-HARDEN-001 mapping — both trust gaps closed (OBSERVED_FACT)

Readback §11 gap **A (PRE-SPEC SELF-PINNING)**: `build_spec` previously
set `spec["harness"]["tree_digest"] = harness_tree_digest(<CURRENT LIVE
harness_root>)` — the mutable tree selected its own expected identity,
and schema v2 required the controller to exist before the final spec was
authored.  CLOSED: the authoring path is now the PRE-CONTROLLER LAUNCH
TEMPLATE (`build_pre_controller_template`) whose
`expected_harness_tree_digest` is a REQUIRED operator-supplied value used
VERBATIM; NO authoring/finalization helper computes a live-tree digest
(structural tests: `harness_tree_digest(` absent from the `rootauth`
source, from `build_pre_controller_template` and from `build_spec`;
`finalize_spec` copies the template's harness section verbatim).  The
authority verifies the LIVE tree against the operator value ONCE, in
Phase A, before any controller exists; the final spec's harness identity
is the frozen pre-controller identity, never recomputed.

Readback §11 gap **B (VERIFY-THEN-IMPORT / PRELOADED-CODE)**: privileged
modules were imported through the ordinary mutable host import path and
the freeze verified only file location/bytes.  CLOSED: the authority
process is started by the operator in the PRE-CONTROLLER TRUSTED PHASE
(the controller does not yet exist — the operator/bootstrap phase is the
trusted authority phase per the held threat model); at Phase A the
complete byte set is read, compared to the operator-selected identity
(fail-closed `BOOTSTRAP_HARNESS_TREE_DRIFT`), EVERY privileged module is
imported inside that same trusted phase, and — the new mechanical
linkage — each module's EXECUTING code object is proven STRUCTURALLY
EQUAL to a fresh `compile()` of the frozen verified bytes (recursive
co_code/co_names/co_varnames/co_flags/argcounts/freevars/cellvars/
co_filename + consts comparison; `BOOTSTRAP_MODULE_CODEOBJECT_MISMATCH`
fail-closed).  A same-UID modify-then-restore race can no longer make
other code execute as privileged authority code: trust derives from the
frozen representation, and the import guard (armed at the END of Phase A
— before the process signals readiness, not merely before the trigger)
refuses every NEW `qh.*` import from that moment.

Mechanism class: readback §15 direction 1+2 combined — a long-lived
pre-controller authority process loads ALL privileged modules while the
controller does not yet exist, and the loaded code is mechanically
reconciled to the verified sealed byte set by code-object equality (the
stronger "load == frozen bytes" linkage without a separate exec
machinery).

## 4. The two-phase authority lifecycle (§5/§9) — OBSERVED_FACT

Production entry: `qh authority --operator-state D --template-fd 0
--custody-fd N --finalization-fd M` (replaces the one-shot final-spec
`qh root` shape; the self-pinning entry surface is REMOVED).

```
PHASE A — PRE-CONTROLLER TRUST FREEZE (no controller process exists)
  1. operator starts the authority (template + custody + finalization
     channels ALL gated by require_trusted_spec_fd BEFORE any byte is
     read: PIPE or mechanically identified FULLY SEALED memfd; ordinary
     files refused — CR-REMED-003 held, now on two channels);
  2. ROOT_UP, PR_SET_DUMPABLE=0, real-Yama>=1 gate, seal-capability
     gate (CR-REMED-001 held);
  3. template parsed/validated (TEMPLATE_INVALID fail-closed; a template
     carrying authorized_controller is refused) and held in a MANDATORY
     SEALED memfd (TEMPLATE_BYTES_SEALED — §8 sealed authority state);
  4. custody bytes read from the pipe/memfd-only channel and sealed
     (ROOT_CUSTODY_ESTABLISHED; CUSTODY_SOURCE_KIND_REFUSED otherwise);
  5. LIVE ordinary tree verified against the OPERATOR-SELECTED identity
     (BOOTSTRAP_HARNESS_TREE_DRIFT fail-closed — §17 gate);
  6. complete privileged byte set (21 files) frozen into the MANDATORY
     SEALED authority bundle; all 19 privileged qh modules imported with
     per-module code-object verification; §18 provenance record written;
  7. import guard armed (every NEW qh.* import refused from here);
  8. PRE_CONTROLLER_BOOTSTRAP_FROZEN milestone recorded;
  9. PRECONTROLLER_READY printed — only NOW may the controller start.

PHASE B — CONTROLLER BINDING / FINAL SPEC / TRIGGER EXPOSURE
 10. operator starts the authorized controller and captures its actual
     uid/pid//proc-starttime;
 11. operator sends the finalization delta {template_id,
     authorized_controller{uid,pid,starttime}} over the operator-held
     finalization channel (created BEFORE controller startup; the write
     end never leaves the operator — §11);
 12. authority finalizes the final spec IN-PROCESS from the frozen
     template + controller identity ONLY (strict delta shape; unknown
     fields refused; TEMPLATE_ID_MISMATCH fail-closed exit 18);
 13. FINAL_SPEC_FROZEN_HARNESS_ID == PRE_CONTROLLER_FROZEN_HARNESS_ID
     proven (equal to the bundle digest-from-files AND the operator
     expected value; mismatch = FINAL_SPEC_FROZEN_HARNESS_ID_MISMATCH
     fail-closed exit 18 BEFORE any trigger);
 14. final spec bytes sealed (SPEC_BYTES_SEALED), observability copy,
     SPEC_FINALIZED recorded; ONLY THEN the trigger socket is bound
     (ROOT_TRIGGER_BEFORE_FINALIZATION structural refusal);
 15. the single mint enforces the pre-bound controller (CR-REMED-004
     held) and the supervisor is forked from the frozen state.
```

Mechanical ordering evidence (OBSERVED_FACT, ledger + tests): the
lifecycle-order test proves `events.index(PRE_CONTROLLER_BOOTSTRAP_FROZEN)
< events.index(SPEC_FINALIZED) < events.index(ROOT_SOCKET_BOUND)`, that
the test observes `PRECONTROLLER_READY` BEFORE spawning the controller,
that no abstract `qh-root-*` socket exists before finalization, and that
`bind_socket` refuses until finalization completes
(`test_phase_order_freeze_then_controller_then_finalize_then_trigger`,
`test_trigger_structurally_refused_before_finalization`;
`test-outputs/precontroller-LIFECYCLE-EVIDENCE.json` carries the
compose-demo instance of the same order).

## 5. Pre-controller trusted harness identity (§6) — OBSERVED_FACT

* A. the operator selects the exact qualification-harness source
  identity at template-authoring time (`expected_harness_tree_digest`,
  REQUIRED, no default — `test_template_expected_identity_is_operator_
  supplied` pins that the parameter cannot be omitted and that the
  builder performs NO live-tree digest computation);
* B. the authority verifies the ordinary source against that
  pre-authorized identity in Phase A (§17 negative: expected established
  INDEPENDENTLY from a pristine copy; the mutated deployed tree fails
  closed and is never self-pinned — `test_pre_freeze_mutated_tree_fails_
  closed_no_self_pinning`);
* C./D. the complete privileged byte set is snapshotted and packed into
  the MANDATORY fully sealed authority bundle (four-seal memfd);
* E. the frozen bundle identity/digest is recorded
  (PRE_CONTROLLER_BOOTSTRAP_FROZEN + the bootstrap provenance record);
* F. the frozen identity is retained in the long-lived authority process
  (bundle memfd + expected digest + module inventory);
* G. from the milestone onward the ordinary live harness tree is NOT
  authoritative (finalization, mint, supervisor, trusted-bytes snapshot
  and in-boundary code all derive from the frozen representation; the
  supervisor's TRUSTED_SPEC_VERIFY uses the frozen-bundle override as
  already accepted).

The harness-tree digest is now PATH-INDEPENDENT (`qh-harness-tree/2`,
entries only): the operator may compute the expected identity from ANY
trusted pristine copy of the same source — or from Git object bytes of
the operator-selected harness commit/tree — and it binds CONTENT only
(the root PATH is still pinned separately by `spec.harness.root` and the
module-provenance checks).  The historical `d296a5a2…` tree is NOT
hardcoded anywhere; the mechanism accepts any future operator-selected
harness commit/tree by supplying its digest
(`test-outputs/precontroller-LIFECYCLE-EVIDENCE.json` shows a live
instance: operator-expected digest `0a16afdb…`, frozen bundle digest
`c8a6fd2c…`, `expected_tree_digest_match=true`,
`frozen_harness_id_match=true`).

## 6. Pre-controller launch template (§8) — OBSERVED_FACT

`TEMPLATE_SCHEMA_VERSION = 1` (`qh/trusted_spec.py`).  Pre-bound fields:
attempt id; attempt-root identity (path/dev/ino); bootstrap manifest id +
config dir; expected controller-scope config path
(`controller_scope.env.CLAUDE_CONFIG_DIR`); harness root + OPERATOR
expected tree digest + optional Git provenance tuple; boundary-child
relpath; evidence/target/auditor-output identities; Codex executable
identity (path/dev/ino/sha256), version, profile, config digest;
credential-adapter identity; mount roles; noegress required; payload
kind.  The privileged-bootstrap bundle identity is DETERMINED by the
expected byte-set identity and is mechanically CROSS-CHECKED at the
freeze (bundle digest-from-files == operator expected digest) and at
finalization (SPEC_FINALIZED carries bundle_digest + frozen_harness_id).
The controller neither authors nor mutates the template (it does not
exist at authoring; the template travels only on the operator capability
channel); the template bytes are held in a MANDATORY sealed memfd
(TEMPLATE_BYTES_SEALED) — sealed authority state per §8.

## 7. Frozen privileged-bundle provenance + module-load inventory
(§12/§13/§18) — OBSERVED_FACT

`PrivilegedBootstrap.freeze(harness_root, expected_tree_digest,
provenance)` performs, in order: read the 21-file byte set (19 qh
modules + the two in-boundary payload fixtures); digest and compare to
the operator value; import each privileged module; verify
`mod.__file__` resolves under the pinned tree; verify the EXECUTING
code object equals a compile of the frozen bytes
(`codeobject_verified`); pack + seal the bundle.  The observability
record `operator-state/bootstrap/<template_id[:16]>.json` carries the
§18 provenance tuple: harness root; operator-expected digest; frozen
tree digest; frozen bundle digest; file count; PER-FILE digest manifest;
module inventory `{module: {load_phase: PRE_CONTROLLER_TRUSTED_PHASE,
file_relpath, file_sha256, codeobject_verified: true}}`; the
operator-side source-provenance tuple (repository full name, exact
source commit, qualification-harness Git tree — captured best-effort by
the operator helper, `source_role: qualification-harness`); seal state.
A version string alone is never provenance; the canonical authority
decision binds to the frozen bundle identity (SPEC_FINALIZED carries
bundle_digest; the grant binds the final spec id).

Module-load timing inventory (§13), mechanically recorded for all 19
privileged modules (`qh`, `qh.__main__`, `qh.util`, `qh.ledger`,
`qh.statemachine`, `qh.bootstrap`, `qh.campaign`, `qh.custody`,
`qh.noegress`, `qh.boundary`, `qh.boundary_child`, `qh.codex_profile`,
`qh.gatew`, `qh.authority`, `qh.compose`, `qh.cli`, `qh.trusted_spec`,
`qh.rootauth`, `qh.adapters`): **ALL loaded + frozen in the
PRE_CONTROLLER_TRUSTED_PHASE with code-object verification**
(`test_all_privileged_modules_loaded_and_verified_pre_controller`).
After Phase A a NEW privileged qh import FAILS CLOSED
(`QH_IMPORT_FROZEN` meta_path guard — armed at milestone time, i.e.
before the controller starts; the existing guard semantics PRESERVED and
STRENGTHENED, `test_post_controller_new_qh_import_fails_closed`).

## 8. Finalization channel (§11) — OBSERVED_FACT

The finalization channel must be a PIPE or a fully sealed memfd (the
same `require_trusted_spec_fd` gate, enforced at the CLI BEFORE any byte
is read and re-verified in `pre_controller_startup`:
`FINALIZATION_SOURCE_KIND_REFUSED`/`SPEC_SOURCE_KIND_REFUSED`).  In the
production composition the operator creates the pipe BEFORE controller
startup, keeps the write end, and writes the delta only after the
controller exists; trusted finalization material never appears in argv
or environment variables (it is an fd).  Controller-inheritance proof:
an inode-level `/proc/<controller-pid>/fd` scan shows the live
controller holds NO fd bound to the finalization pipe
(`test_controller_holds_no_finalization_channel_write_end`; repeated
inside the §20 integrated composition).  Ordinary-file and unsealed-memfd
finalization fds are refused (gate tests in
`tests/test_spec_channel.py`).

## 9. Final spec derivation + frozen-harness-id equality (§10) —
OBSERVED_FACT

`finalize_spec(template, controller_uid, controller_pid,
controller_starttime)` builds the final spec (SPEC_SCHEMA_VERSION 2 → 3:
v2 fields preserved + the REQUIRED `spec.pre_controller_template.
template_id`) by adding ONLY the controller identity to a private copy
of the frozen template.  The harness identity is copied VERBATIM from
the template.  At finalization the authority mechanically proves
`FINAL_SPEC_FROZEN_HARNESS_ID == PRE_CONTROLLER_FROZEN_HARNESS_ID` (==
the operator expected digest) and records
`SPEC_FINALIZED{final_spec_id, template_id, frozen_harness_id,
frozen_harness_id_match: true, bundle_digest}`.  Mismatch fails closed
(exit 18) BEFORE controller trigger exposure.  Changing the controller
pid/starttime still changes the final spec id (CR-REMED-004 semantics
preserved — retested); changing the live ordinary harness tree after
Phase A does NOT change the trusted frozen identity (§10/§14/§15 tests
assert the final spec digest equals the pre-controller value while the
live tree is attacker-modified).  The final spec additionally carries
the original harness path (provenance/diagnostics), the frozen
authority-bundle digest, the operator source/Git provenance tuple and
(via the frozen bundle) the executable file manifest.

## 10. Adversarial negatives (§14–§17) — OBSERVED_FACT

Unique attacker marker `QH-PRECONTROLLER-ATTACKER-4b7e91c2`
(`tests/test_precontroller_provenance.py`; marker-file + stderr scan):

* **§14 live-tree mutation BEFORE final spec** — parametrized
  independently for `qh/rootauth.py`, `qh/authority.py`, `qh/util.py`,
  `qh/trusted_spec.py`: after the freeze milestone and controller start,
  before the operator finalization write, the module is replaced with
  marker code; the operator finalizes and the authorized flow COMPLETES
  from the frozen representation (mint ok, C4′/custody/no-egress/profile/
  GATE-W/protected launch ok, root rc 0); the marker file NEVER appears
  anywhere; the final spec harness identity remains the pre-controller
  frozen identity;
* **§15 entire-tree replacement** — the whole ordinary harness tree is
  deleted/recreated with attacker bytes between the milestone and
  finalization: the replacement tree is NOT blessed (frozen identity
  preserved; the replacement's own identity differs or is not even
  digestible), the flow completes solely from the pre-controller frozen
  representation, no attacker code executes;
* **§16 modify-then-restore TOCTOU** — a privileged module is replaced
  with marker bytes and its ORIGINAL bytes restored before final-spec
  completion: restoration cannot change which privileged code is
  trusted/executed (the authority decision derives from the frozen
  representation, not from a later files-look-correct-again check); the
  attempt completes; the marker never executes;
* **§17 pre-freeze negative** — the deployed tree is mutated BEFORE the
  authority starts while the expected identity was established
  INDEPENDENTLY from a pristine copy: Phase A fails closed
  (ROOT_STARTUP_FAILED / BOOTSTRAP_HARNESS_TREE_DRIFT; no milestone, no
  finalization, no socket); ACTUAL and EXPECTED are never both derived
  from the same mutated tree in the test;
* finalization negatives — wrong `template_id` delta → exit 18
  `TEMPLATE_ID_MISMATCH`, no trigger; delta with extra fields → exit 18
  `SPEC_FINALIZATION_INVALID`, no trigger.

## 11. Integrated zero-provider composition (§20) — OBSERVED_FACT

`tests/test_integrated_hardening.py::test_integrated_pre_controller_
provenance_composition` proves the mandated 20-step order from ONE
integrated attempt: operator-selected source identity → bundle frozen
against it → mandatory seals verified (template + custody) →
PRE_CONTROLLER_BOOTSTRAP_FROZEN (all modules loaded, code objects
verified) → controller started ONLY afterward → operator captures
uid/pid/starttime → finalization over the trusted channel (controller
holds no write end — inode scan) → frozen-harness-id equality → trigger
exposed → wrong peer cannot mint (fail-closed DoS on a first root;
fresh root for the authorized flow) → authorized trigger accepted →
supervisor forked from frozen state (`channel=fork-frozen-bootstrap`) →
supervisor repeats the authorized-controller verification → C4′ passes →
custody established → hard no-egress passes → profile freezes → GATE-W
passes → synthetic protected launch succeeds (marker file) → reuse
refused → engagement accounting untouched.  Provider/model/auditor
execution = ZERO (no provider binary referenced or executed; asserted).
The sealed-memfd TEMPLATE channel variant completes the same flow
(`test_integrated_template_arrives_via_sealed_memfd_channel`).  The
`qh compose-demo` rehearsal is green over the new flow
(`ok=true, marker=true, reuse refused, engagements untouched`,
milestone `files=21 modules=19 sealed match=true`).

## 12. Held closure regressions (§4/§21) — OBSERVED_FACT

Preserved and retested, none weakened:

* **CR-REMED-001** — the ONE canonical UAPI constant set
  (`MFD_CLOEXEC=0x0001`, `MFD_ALLOW_SEALING=0x0002`, `F_ADD_SEALS=1033`,
  `F_GET_SEALS=1034`, `F_SEAL_SEAL|SHRINK|GROW|WRITE=0x0001/2/4/8`,
  `REQUIRED_SEALS=0x000F`), mandatory four-seal authority holds, no
  optional downgrade, no `--require-seals` flag, fail-closed production
  CLI under a failing seal backend (`tests/test_seal_uapi.py` —
  constants, capability, hold/refusals, type discrimination incl. the
  ordinary-file-fcntl regression — ALL unchanged and green);
* **CR-REMED-003** — production trusted input capability-bound:
  ordinary-file stdin / `--template-fd <file>` REFUSED before any byte
  is read; unsealed and partially sealed memfd REFUSED; pipe ACCEPTED
  (PRECONTROLLER_READY); fully sealed memfd ACCEPTED; the SAME gate now
  also protects the finalization channel (`tests/test_spec_channel.py`
  rewritten against the `authority` CLI with identical gate semantics);
* **CR-REMED-004** — operator-authored `authorized_controller
  {uid,pid,starttime}` inside the canonical digest (now via the operator
  finalization delta — still never a controller request; claim-only
  request schema unchanged and `authorized_controller`-as-claim is still
  UNKNOWN_CLAIM_FIELD terminal); root mint trigger AND supervisor
  request both enforce exact SO_PEERCRED uid/pid + ACTUAL /proc
  starttime; wrong pid / wrong starttime / reproduced-config-tree /
  full-knowledge peers refused pre-mint; authorized-controller-exit
  refused; wrong-peer first arrival terminally consumes the one-shot
  root (R-6 fail-closed DoS semantics unchanged);
  `tests/test_controller_binding.py` green;
* additionally held and green: freeze-before-trigger (milestone precedes
  ROOT_SOCKET_BOUND; bind_socket structural refusals extended with
  ROOT_TRIGGER_BEFORE_FINALIZATION), mandatory sealed 21-file bundle,
  post-ROOT-READY module-replacement and delete/recreate attacker
  regressions (marker never executes), post-freeze import guard, fork-
  from-frozen supervisor with no host PYTHONPATH re-import, protected
  child code snapshot from the frozen bundle, C-1/C4′, trusted-spec
  §19 mutation refusals, transit-swap refusal, controller-imitation
  powerlessness, hard no-egress, GATE-W matrix, engagement-accounting
  separation.

## 13. Tests and validation — FIRST results and reruns (OBSERVED_FACT)

Environment: Python 3.11.15 + pytest 9.1.1 via `uv run --no-project
--with pytest`; bwrap 0.12.0; Yama ptrace_scope = 1; kernel
7.2.2-1-cachyos; unprivileged user+net namespaces available.

* Pre-change baseline of the prior suite at the exact base: **200/200
  PASS** (`test-outputs/precontroller-BASELINE.txt`).
* RED-first evidence: the new CR-HARDEN-001 test file was written BEFORE
  implementation and recorded failing: **18 failed / 2 passed**
  (`test-outputs/precontroller-RED-FIRSTRUN.txt`; the 2 passing were the
  two §11 channel-gate probes over the already-accepted
  `require_trusted_spec_fd` mechanics).
* Development iterations, each recorded and resolved (nothing rerun away
  silently):
  - DEV1 (first implementation pass): **48 failed / 152 passed**
    (`precontroller-DEV1.txt`) — expected breakage of the legacy
    one-shot-spec call sites (old `build_spec` signature; `env.spec`
    pre-binding access; old `AuthorityRoot(spec_bytes=…)` constructors;
    `qh root` argv; tampered-FINAL-spec injection sites now tampering
    the TEMPLATE);
  - DEV2: **6 failed / 215 passed** (`precontroller-DEV2.txt`) —
    delivered-template/template-id state sync in `spawn_authority`;
    three test-shape fixes (dup2-free tampered-template subprocess,
    sealed-fail CLI wrapper pipes, wrong-starttime socket-name
    derivation) and two remaining template-override sites;
  - DEV3: **221 passed** (`precontroller-DEV3.txt`).
* **Complete remediated harness suite — FIRST complete run of the FINAL
  set: 221/221 PASSED**
  (`test-outputs/harness-suite-FIRSTRUN-PRECONTROLLER.txt`; 200 prior
  test intents preserved/updated + 21 new = 221; no test deleted, no
  assertion weakened — legacy call sites were mechanically migrated to
  the two-phase flow).
* Targeted product non-regression (read-only):
  `skill/tests/test_codex_sandbox.py` +
  `skill/tests/test_codex_runner_mock.py`: **34/34 passed (first run)**
  (`product-targeted-PRECONTROLLER.txt`).
* Product FULL deterministic suite `skill/tests`: **686/686 + 99
  subtests PASSED (first run)**
  (`product-fullsuite-PRECONTROLLER.txt`).  HOST_NODE_PATH_DRIFT did
  NOT reproduce in this session (PATH-order-dependent external
  condition; honestly recorded; no product test or host state altered).
* `git diff --check`: clean (worktree).
* Secret-pattern scan over every changed/new ordinary file (key/token/
  PEM/JWT/`sk-`/AKIA/xox/ghp patterns): **zero hits**.
* Zero-provider: EXTERNAL_PROVIDER_CONTACT = ZERO, MODEL_INFERENCE =
  ZERO, CAMPAIGN_AUDITOR_ENGAGEMENT = ZERO (by construction — the
  pinned "codex" executable is a synthetic fixture; asserted by test).

## 14. Product / historical non-interference (§23) — OBSERVED_FACT

`skill/` tree identity UNCHANGED before/after:
`git rev-parse 54fb4e0:skill` == `c792933a862d9a5434681a88d183470dd8b15d2f`
== post-change worktree (`git status skill/` clean; re-verified at
staging).  NOT modified: `skill/**`, `skill/tests/**`, `skill/schemas/**`,
`skill/PUBLIC-CONTRACT.md`, `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md`,
`AUCDEV-QUALIFICATION-HISTORY.md`, historical AUCDEV-010 reports,
frozen Campaign-2 artifacts (changed-path confinement proves it
mechanically; product suites ran read-only).  Campaign-2 remains
TERMINAL.  Qualification NONE.  Installation NONE.

## 15. Residuals and new blockers (explicit)

1. **CR-HARDEN-001 trust-boundary note (documented assumption, not a
   defect class):** the authority process's own interpreter-start module
   loads (qh.cli → qh.rootauth → privileged deps) necessarily execute
   from the ordinary tree BEFORE the Phase-A verification code runs.
   This is sound under the held threat model because the PRE-CONTROLLER
   operator/bootstrap phase is the TRUSTED authority phase (the
   controller does not exist), and the freeze mechanically reconciles
   those loads against the operator-selected identity (byte set + file
   location + EXECUTING-code-object equality).  An operator who
   launches the authority from an already-tampered tree of their own
   making is outside the threat model (same class as the operator
   handing over credentials).
2. **R-2 (carried, unchanged):** provider adapters remain
   SYNTHETIC-concrete only; real-credential campaign integration remains
   gated on separately authorized campaign preparation + the independent
   harness audit.
3. **R-3 (carried, bounded race):** DIRECTORY sources (evidence/target)
   in-place content writes racing between in-child digest verification
   and payload exec are detected no earlier than the child; CODE bytes
   are frozen+sealed from BEFORE controller start through the whole
   protected flow (strictly stronger than before this remediation).
4. **R-4 (carried, unchanged):** Codex-internal Landlock enforcement of
   the generated profile is not independently verified without running
   Codex.
5. **R-5 (carried, environmental):** HOST_NODE_PATH_DRIFT did not
   reproduce this session; recorded honestly, unmodified.
6. **R-6 (carried, accepted residual):** wrong-peer arrival terminally
   consumes the one-shot authority root (fail-closed DoS); semantics
   unchanged and retested.
7. **R-7 (carried):** the fork-based supervisor requires the authority
   process to run from the template-pinned harness tree (an operator
   misalignment is a fail-closed startup refusal).  The Python
   interpreter/stdlib, bwrap and unshare remain documented external TCB
   assumptions.
8. **R-8 (NEW, evidence/compatibility note, non-blocking):** the harness
   executable-identity digest formula changed to the path-independent
   `qh-harness-tree/2` (entries only) so an operator can establish the
   expected identity from any pristine copy or Git object bytes; all
   internal comparisons recompute with the same formula, SPEC_SCHEMA
   moved 2→3 (v2 specs are refused — every spec in the harness is
   freshly built), and the production CLI surface changed `qh root` →
   `qh authority` (the one-shot final-spec entry is REMOVED; the old
   SHAPE was the self-pinning surface itself).

No new blocking authority-bootstrap issue was identified by the
implementation evidence.  No STOP condition of the tasking was triggered.

## 16. Governing result (§25)

```
AUCDEV023-CR-HARDEN-001 = CLOSED  (pre-controller trusted freeze from the
                                   operator-selected identity + template
                                   sealed authority state + no live-tree
                                   self-pinning on any production path +
                                   all-privileged-modules pre-controller
                                   load with executing-code-object
                                   provenance + finalization channel +
                                   frozen-harness-id equality before the
                                   trigger + §14–§17 negatives green)
PRE_CONTROLLER_PRIVILEGED_CODE_PROVENANCE = ESTABLISHED (at
                                   implementation/self-test strength)
CR-REMED-001/-003/-004    = CLOSED / ACCEPTED (held, retested, unweakened)
```

Recommended (IMPLEMENTER position, NOT an independent verdict):

```
AUCDEV023_PRE_CONTROLLER_BOOTSTRAP_PROVENANCE_REMEDIATION_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK
```

AUCDEV-023 remains **P1 / READY** (NOT DONE).  Independent harness audit
remains **DEFERRED_PENDING_CONTROL_ROOM_READBACK** of THIS remediation,
then MANDATORY on the exact remediated SHA.  Do NOT transfer any verdict
from any earlier SHA to this one.

## 17. Campaign / qualification held state (preserved EXACTLY)

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

## 18. Required lifecycle

```
THIS remediation publication
→ NEXT (EXACTLY ONE): INDEPENDENT CONTROL ROOM READBACK OF THIS
  PRE-CONTROLLER PROVENANCE REMEDIATION
→ then EXACT TARGET FREEZE
→ then the fresh MANDATORY independent harness audit on this SHA
→ only then consider any future qualification package/campaign
```

This session did NOT self-audit, did NOT qualify, did NOT install, and
did NOT perform the independent audit.

Result: `AUCDEV_023_PRE_CONTROLLER_BOOTSTRAP_PROVENANCE_REMEDIATION_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
