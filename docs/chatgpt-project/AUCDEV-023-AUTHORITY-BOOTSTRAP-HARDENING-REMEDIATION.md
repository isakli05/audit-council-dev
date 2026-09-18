# AUCDEV-023 — Authority Bootstrap Hardening Remediation (Canonical Record)

| Field | Value |
|---|---|
| Session class | BOUNDED ZERO-PROVIDER REMEDIATION IMPLEMENTATION SESSION (operator-authorized AUCDEV-023 AUTHORITY BOOTSTRAP HARDENING against findings AUCDEV023-CR-REMED-001/-002/-003/-004 ONLY) — NOT Auditor A/B, NOT the Control Room, NOT a qualification authority, NOT an installation authority, NOT an independent harness audit; NO auditor/model/provider execution; NO Campaign-2 recovery; NO Campaign-3; NO product (`skill/`) modification; NO G-1/G-2 design research reopened; the harness was NOT self-audited |
| Date | 2026-09-18 (Europe/Istanbul) |
| Exact remediation base | `27c68fdc8175b0ae6cc6ed0b7ec594e956074864` (tree `b42a58aa571c3a2e198d5a1911f464457c77232e`; sole parent `947f28244d7cae263f2e6fbb3025f94cfba7f4dc`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this remediation's bootstrap and re-resolved EXACT immediately before staging; THIS publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Remediation scope | Close ONLY AUCDEV023-CR-REMED-001 (invalid Linux UAPI memfd/seal constants + invalid seal-capability conclusion + optional `--require-seals`), AUCDEV023-CR-REMED-002 (privileged supervisor bootstrap from the ordinary mutable host harness tree), AUCDEV023-CR-REMED-003 (ordinary-file trusted-spec input), AUCDEV023-CR-REMED-004 (authorized controller not pre-bound in trusted-root state) |
| Disposition (recommended) | `AUCDEV023_AUTHORITY_BOOTSTRAP_HARDENING_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK` (§22) |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **STILL REQUIRED — DEFERRED_PENDING_CONTROL_ROOM_READBACK of THIS remediation** (not executed in this session; a verdict on any earlier SHA does not transfer) |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `INFERENCE` (derived), `HYPOTHESIS` (unverified),
`REQUIREMENT` (task/record-mandated property).

## 1. Base identities and confirmed governing state (OBSERVED_FACT)

Live `refs/heads/master` resolved EXACT `27c68fdc8175b0ae6cc6ed0b7ec594e956074864`
(tree `b42a58aa571c3a2e198d5a1911f464457c77232e`; sole parent
`947f28244d7cae263f2e6fbb3025f94cfba7f4dc`).  All mandated documents and
harness sources were read at that exact SHA.  Confirmed governing state:

```
AUCDEV-023                    = P1 / READY
CR-REMED-001..004             = OPEN / BLOCKING (each)
IR-003 (AUCDEV023-CR-IMPL-003)= CLOSED / ACCEPTED
independent harness audit     = DEFERRED_PENDING_REMEDIATION
AUCDEV-010                    = P1 / BLOCKED
Campaign-2                    = TERMINAL
qualification                 = NONE
installation                  = NONE
```

Pre-existing unrelated working-tree state preserved unstaged throughout:
`smoke-fixture` / `smoke-fixture-103` gitlink dirt (nested HEADs MATCH the
recorded gitlinks — verified; only inner untracked `audit-output/`
fixtures) and untracked `aucdev019-evidence/`.

## 2. Exact changed paths (OBSERVED_FACT)

MODIFIED (14, all under `qualification-harness/`):

```
qualification-harness/qh/__main__.py
qualification-harness/qh/authority.py
qualification-harness/qh/boundary.py
qualification-harness/qh/cli.py
qualification-harness/qh/compose.py
qualification-harness/qh/custody.py
qualification-harness/qh/rootauth.py
qualification-harness/qh/trusted_spec.py
qualification-harness/qh/util.py
qualification-harness/tests/test_compose.py
qualification-harness/tests/test_rootauth.py
qualification-harness/tests/test_sealing.py
qualification-harness/tests/test_trusted_claims.py
qualification-harness/tests/test_trusted_spec.py
```

NEW (6 + 1 report + 2 governance appends):

```
qualification-harness/fixtures/bound_controller.py
qualification-harness/tests/test_seal_uapi.py
qualification-harness/tests/test_spec_channel.py
qualification-harness/tests/test_bootstrap_freeze.py
qualification-harness/tests/test_controller_binding.py
qualification-harness/tests/test_integrated_hardening.py
docs/chatgpt-project/AUCDEV-023-AUTHORITY-BOOTSTRAP-HARDENING-REMEDIATION.md
docs/chatgpt-project/AUCDEV-CURRENT-STATE.md   (append-only)
docs/chatgpt-project/AUCDEV-BACKLOG.md         (append-only)
```

Total **23 staged paths**, confined EXACTLY to the authorized mutation
families (`qualification-harness/**`, CURRENT-STATE, BACKLOG, the NEW
remediation report).  Unchanged: `fixtures/fake_controller.py`,
`fixtures/gatew_payload.py`, `fixtures/launch_sim_payload.py`,
`fixtures/demonstrated-profile.json`, `tests/conftest.py` and every
non-listed harness test; `test-outputs/` remains gitignored local
evidence (archived in the handoff, not committed).

## 3. CR-REMED-001 disposition — CORRECTED LINUX MEMFD / SEAL UAPI (CLOSED)

Corrected, centralized constants (`qh/util.py`, the ONE canonical set —
`qh/custody.py` now imports them and holds no numeric definitions):

```
MFD_CLOEXEC       = 0x0001   (os.MFD_CLOEXEC preferred when present)
MFD_ALLOW_SEALING = 0x0002   (os.MFD_ALLOW_SEALING preferred when present)
F_ADD_SEALS       = 1033
F_GET_SEALS       = 1034
F_SEAL_SEAL       = 0x0001
F_SEAL_SHRINK     = 0x0002
F_SEAL_GROW       = 0x0004
F_SEAL_WRITE      = 0x0008
REQUIRED_SEALS    = 0x000F  (the intended four-seal mask)
```

The misidentified `MFD_ALLOW_SEALING=0x0004` (= `MFD_HUGETLB`) and the
seal values 0x0010/0x0020/0x0040 (actually `F_SEAL_FUTURE_WRITE` /
`F_SEAL_EXEC` / unused) are gone from the codebase.  Platform `os`
constants are preferred where Python exposes them; the fallback numerics
are pinned to the authoritative UAPI values by deterministic tests
(`tests/test_seal_uapi.py`: `test_util_constants_equal_authoritative_uapi`,
`test_platform_os_constants_agree_when_available`,
`test_constants_are_centralized_no_contradictory_duplicates`).

## 4. Actual host seal capability — RECOMPUTED, ESTABLISHED (OBSERVED_FACT)

With the corrected API the demonstrated host (kernel `7.2.2-1-cachyos`)
MECHANICALLY ESTABLISHES the four-seal populated memfd representation
(probe recorded this session):

```
memfd_create("probe", MFD_CLOEXEC|MFD_ALLOW_SEALING) -> fd
write(2) populated bytes                     -> OK (21 bytes)
fcntl(F_ADD_SEALS, 0x000F)                   -> OK
fcntl(F_GET_SEALS)                           -> 0x000f
subsequent write(2)                          -> EPERM (refused)
ftruncate grow (4096)                        -> EPERM (refused)
ftruncate shrink (4)                         -> EPERM (refused)
```

The historical `unavailable_kernel` conclusion was an artifact of the
`MFD_HUGETLB` misidentification and is NOT carried forward: the corrected
`memfd_seal_capability()` probe recomputes the capability per process
(create with sealing flags, populate, apply the four seals, require all
four bits in `F_GET_SEALS`, and require a post-seal write REFUSAL) and
returns `sealed` on this host class.  No `AUTHORITY_CRITICAL_SEALING_
BLOCKED_BY_HOST` STOP condition arose.

## 5. Mandatory authority-critical sealing (CLOSED)

* `hold_bytes_memfd` (util) now ALWAYS creates with
  `MFD_CLOEXEC|MFD_ALLOW_SEALING`, populates, applies the four required
  seals and verifies `F_GET_SEALS`; failure raises
  `SealUnavailableError` — there is no unsealed hold and no optional
  downgrade path anywhere;
* `CredentialCustody.establish` (supervisor-side custody) uses the SAME
  corrected seal semantics and FAILS CLOSED
  (`CUSTODY_SEAL_FAILED`) when the sealed representation cannot be
  produced — the best-effort/unsealed posture is removed;
* the production authority root seals EVERY authority-critical
  representation in its non-dumpable process before any trigger is
  exposed: the canonical trusted-spec bytes (`SPEC_BYTES_SEALED`,
  sealed memfd `qh-root-trusted-spec`), the root-held provider custody
  bytes (`ROOT_CUSTODY_ESTABLISHED` with `seal_status=sealed`), and the
  frozen privileged bootstrap bundle (`BOOTSTRAP_FROZEN` with
  `bundle_seal_status=sealed`);
* the optional `--require-seals` CLI shape is REMOVED (parser carries no
  such option; passing it is an argparse error) — production always
  enforces the required sealing property; root startup additionally
  fails closed up front (`AUTHORITY_CRITICAL_SEALING_UNAVAILABLE`, exit
  13) when the corrected probe cannot establish the representation on
  the host;
* deterministic fail-closed proof uses a mechanically separate FAILING
  seal backend injected ONLY by test code at the single
  `qh.util._apply_seals` seam (monkeypatch in-process;
  `tests/test_seal_uapi.py::test_root_cli_fails_closed_when_seal_backend_fails`
  drives the PRODUCTION CLI through a test wrapper process): no READY,
  no socket, `AUTHORITY_CRITICAL_SEALING_*` refusal — production
  CLI/controller input cannot disable sealing.

## 6. Sealed-memfd type discrimination (CLOSED)

`qh.util.fd_source_kind` classifies `PIPE | MEMFD | FILE | OTHER` by the
robust Linux-specific method: `fstat` mode (FIFO→pipe) plus, for regular
files, the `/proc/self/fd/<n>` link target (`/memfd:` prefix → memfd;
anything else — INCLUDING tmpfs regular files — → ordinary file).  fcntl
values are deliberately never used for classification (this kernel class
returns an `F_GET_SEALS` value even for ordinary files — regression
test included).  Trusted-memfd channels additionally require the
COMPLETE required seal set via `F_GET_SEALS`
(`has_required_seals`).  Negative tests cover ordinary regular file,
tmpfs regular file, unsealed memfd, partially sealed memfd (only
`F_SEAL_WRITE`), fully sealed memfd, and pipe
(`tests/test_seal_uapi.py`).

## 7. CR-REMED-003 disposition — capability-bound trusted-spec input (CLOSED)

The production root CLI gates the spec channel BEFORE any byte is read
(`qh.util.require_trusted_spec_fd`):

* **PIPE** (including the default stdin pipe): ACCEPTED — the complete
  bounded spec bytes are read into the root, which is already
  non-dumpable-by-startup-order (PR_SET_DUMPABLE=0 at startup top, well
  before `bind_socket`), validated, canonicalized and immediately moved
  into the mandatory sealed authority-state representation
  (`SPEC_BYTES_SEALED`) BEFORE the controller trigger surface exists;
* **fully SEALED memfd**: ACCEPTED — mechanically verified memfd identity
  (link-target method) AND the complete four-seal set required
  (`SPEC_MEMFD_SEALS_INCOMPLETE` refusal otherwise);
* **ordinary regular file** — including stdin redirected from an
  ordinary file and `--spec-fd <regular-file-fd>`: REFUSED
  (`SPEC_SOURCE_KIND_REFUSED:file`, exit 15);
* **unsealed / partially sealed memfd**: REFUSED.

Tests (`tests/test_spec_channel.py`): stdin-from-ordinary-file REFUSED;
`--spec-fd` regular file REFUSED; unsealed memfd REFUSED; partially
sealed memfd REFUSED; proper pipe ACCEPTED (root reaches READY); fully
sealed memfd ACCEPTED (integrated attempt completes —
`tests/test_integrated_hardening.py::test_integrated_spec_arrives_via_
sealed_memfd_channel`).

## 8. CR-REMED-002 disposition — immutable privileged supervisor bootstrap (CLOSED)

Mechanism (implementer-owned, preferred direction A — preload + fork):

1. **Privileged bootstrap byteset** (`PRIVILEGED_BOOTSTRAP_RELPATHS`):
   the exact spec-pinned executable byte set — all 19 `qh/` modules
   (root authority `rootauth`, grant/supervisor `authority`, supervisor
   entry `cli`, spec verification `trusted_spec`, C4′ `bootstrap`,
   custody `custody`, no-egress `noegress`, policy freezing
   `codex_profile`, GATE-W `gatew`, boundary construction
   `boundary`/`boundary_child`, plus `util`, `ledger`, `statemachine`,
   `campaign`, `compose`, `adapters`, `__init__`, `__main__`) + the two
   in-boundary payload fixtures = 21 files (`HARNESS_EXEC_RELPATHS`).
   System/stdlib/runtime dependencies (Python interpreter + stdlib,
   bwrap, unshare, host `/usr,/lib,/etc,/proc` boundary RO binds) are
   explicitly documented as external trusted-computing-base assumptions
   (`EXTERNAL_TCB_ASSUMPTIONS` in `qh/rootauth.py`).
2. **Freeze before the trigger** (`PrivilegedBootstrap.freeze`, invoked
   at the end of `AuthorityRoot.startup`, BEFORE `bind_socket` —
   enforced structurally: `bind_socket` refuses
   `ROOT_TRIGGER_BEFORE_BOOTSTRAP_FREEZE`): read the complete byte set
   from the harness root, compare it to the TRUSTED SPEC identity
   (`harness_digest_from_files` == `spec["harness"]["tree_digest"]`,
   else `BOOTSTRAP_HARNESS_TREE_DRIFT` fail-closed exit 17), IMPORT
   every privileged module into the root process (verifying each
   module's `__file__` resolves under the pinned tree), pack the bytes
   into the sealed immutable authority bundle (mandatory four-seal
   memfd), and record `BOOTSTRAP_FROZEN` (bundle digest, 21 files, 19
   modules, spec-tree match, sealed status).
3. **Post-freeze import guard**: a `sys.meta_path` finder refuses every
   NEW `qh`/`qh.*` import (`QH_IMPORT_FROZEN`) from the moment of the
   freeze — planted modules and lazy host re-imports fail closed instead
   of loading possibly-attacker code.  Stdlib imports remain available.
4. **Supervisor creation by fork()** (`_fork_supervisor`, the production
   default): at mint acceptance the root FORKS; the child closes the
   root-owned sockets, verifies the inherited frozen bundle is still
   sealed and its loaded modules are still the frozen ones, then runs
   the one-shot supervisor ENTIRELY from the already-loaded trusted
   process state — NO exec, NO fresh interpreter, NO host-tree module
   search path (the previous `python -m qh.cli supervisor` +
   host-PYTHONPATH spawn shape is REMOVED from the authority root;
   `qh/cli.py supervisor` remains ONLY as an explicitly-labeled
   TEST/diagnostic entry).  Grant/spec/custody/bundle cross by process
   inheritance only; `PR_SET_PDEATHSIG` still binds the supervisor
   lifetime to the root.
5. **In-boundary code bytes from the frozen representation**: the forked
   supervisor's trusted-bytes snapshot is built from the frozen sealed
   bundle (`snapshot_data_files_from_files` — no host harness read at
   all), and its `TRUSTED_SPEC_VERIFY` harness check uses the
  FROZEN-bundle digest (`harness_digest_override`), so later ordinary
   host-tree mutation can neither alter the protected flow nor derail
   it into loading different code; evidence/target/executable sources
   are still verified against the LIVE host as before.

Adversarial regression reproducing the previous vulnerability
(`tests/test_bootstrap_freeze.py`, real subprocesses, unique attacker
marker `QH-ATTACKER-CODE-EXECUTED-9c1f7ad2` dropped by hostile module
replacements):

* attacker REPLACES privileged modules (`qh/authority.py`,
  `qh/gatew.py`, `qh/custody.py`, `qh/boundary_child.py`,
  `qh/util.py`) on the ordinary host tree AFTER root-ready, BEFORE
  supervisor creation: the authorized controller proceeds, the protected
  launch completes from the FROZEN bytes, and the attacker marker is
  NEVER executed anywhere (outcome A);
* attacker DELETES and recreates the entire harness path with hostile
  bytes after root-ready: same — no attacker execution (frozen flow);
* host tree mutated BETWEEN spec authorization and root start: the root
  itself fails closed at the freeze (`BOOTSTRAP_HARNESS_TREE_DRIFT`,
  no trigger exposed — outcome B; this supersedes the older
  supervisor-time-only `HARNESS_TREE_DRIFT` refusal with an EARLIER
  refusal, recorded as a test-semantics update);
* freeze identity mechanically evidenced in the ledger BEFORE
  `ROOT_SOCKET_BOUND`; post-freeze planted-module import refused
  (`QH_IMPORT_FROZEN`); the authority-root source structurally contains
  no CLI-supervisor/PYTHONPATH spawn.

## 9. CR-REMED-004 disposition — pre-bound authorized controller (CLOSED)

Smallest mechanical mechanism (the task's preferred bounded design):

* the trusted launch spec (schema v2) gains a REQUIRED
  `authorized_controller` field — `{uid: int, pid: int, starttime: str}`
  (`/proc/<pid>/stat` field 22) — OPERATOR-authored in `build_spec`
  (`controller_pid`, `controller_starttime`, `controller_uid`), never
  obtained from a controller request.  The expected controller
  config/scope binding remains the existing pre-controller C-1 manifest
  + `controller_scope.env.CLAUDE_CONFIG_DIR` (C-1 NOT reinterpreted:
  the manifest is still captured BEFORE controller startup; the spec
  subsequently binds the operator-authorized controller instance);
* the binding is inside the canonical digest: changing the bound
  pid or starttime CHANGES the spec id (tested);
* **root trigger acceptance** (`AuthorityRoot.handle_mint_request`,
  BEFORE any mint): `SO_PEERCRED` uid and pid must match exactly AND the
  peer's ACTUAL `/proc/<pid>/stat` starttime must match exactly;
  ANY mismatch → `AUTHORIZED_CONTROLLER_MISMATCH:*` refusal BEFORE mint
  (PID alone is never sufficient; knowledge of attempt id + socket name
  + manifest id is not the capability);
* **supervisor request acceptance** (`Supervisor.handle_request`, at the
  controller-binding step): the SAME pre-bound identity is verified
  again against the connected peer (SO_PEERCRED uid/pid + actual
  starttime) before C4′; C4′ remains responsible for the actual
  controller environment/scope verification;
* wrong-peer arrivals terminally consume the one-shot root —
  classified ACCEPTABLE FAIL-CLOSED DoS and recorded
  (`ROOT_FAIL_CLOSED`/`AUTHORIZED_CONTROLLER_MISMATCH` ledger rows); no
  auto-recovery (the root dies with its single trigger consumed).

Wrong-peer/DoS evidence (`tests/test_controller_binding.py`, real
processes): wrong PID same UID + full knowledge → REFUSED before mint
(no `MINTED`, no supervisor); correct PID wrong starttime → REFUSED;
same-UID peer reproducing the expected `CLAUDE_CONFIG_DIR` tree → STILL
REFUSED; wrong peer first consumes the root (fail-closed DoS recorded;
the synthetic custody value never delivered anywhere); authorized
controller exits → subsequent trigger REFUSED; exact authorized
controller → ACCEPTED (full launch); supervisor refuses a non-bound
peer with `AUTHORIZED_CONTROLLER_MISMATCH` terminal stop and no launch;
controller-supplied `authorized_controller` claim → `UNKNOWN_CLAIM_FIELD`
terminal (claim-only schema preserved, §14).

## 10. Trusted-spec schema delta (OBSERVED_FACT)

```
SPEC_SCHEMA_VERSION: 1 -> 2
+ spec.authorized_controller = {uid:int, pid:int, starttime:str}   (REQUIRED)
```

`validate_spec` enforces presence/types (starttime must be the decimal
`/proc` field 22).  All other §7 security-critical content is unchanged;
`build_spec` captures the controller identity from OPERATOR inputs at
authoring time.  Existing spec verification semantics (self-certifying
content-addressed id, delete/recreate and content-drift refusals) are
unchanged and retested.

## 11. Controller-side mechanics (test infrastructure, non-authoritative)

`fixtures/bound_controller.py` (NEW, host-side test fixture —
deliberately NOT part of `HARNESS_EXEC_RELPATHS`): a persistent
synthetic controller process the operator side starts BEFORE authoring
the spec (its uid/pid/starttime become the binding), driven by one JSON
command per stdin line (`mint`/`request`/`exit`); it carries only
CLAIM payloads and any peer failure is a fail-closed response.
`CompositionEnv` now routes its mint/request helpers through the
operator-authorized bound controller instance
(`root_mint`/`controller_request`), with explicit ATTACK channels
(`raw_root_mint`/`raw_controller_request`) that connect from unrelated
same-UID peers.  The controller request schema itself is UNCHANGED
(claim-only: `attempt_id`, `controller_starttime`, `env_claims`,
`payload_kind`).

## 12. Integrated zero-provider composition (§18) — OBSERVED_FACT

`tests/test_integrated_hardening.py::test_integrated_hardened_composition`
proves the mandated order from ONE integrated attempt: operator-authorized
controller identity established (live process + pre-controller C-1
manifest) → spec constructed and delivered via the permitted pipe
channel (and, separately, via a fully SEALED memfd channel) → authority
root starts → corrected UAPI seals established
(`seal_status=sealed` for spec bytes AND custody) → complete privileged
bootstrap bytes (21 files) frozen BEFORE the controller trigger → root
exposes the trigger → a WRONG peer cannot mint (fail-closed DoS on a
first root; fresh root for the authorized flow) → the CORRECT
controller trigger accepted at the root (uid/pid/starttime verified) →
supervisor created from the frozen bootstrap (`channel=
fork-frozen-bootstrap`) → C4′ passes → custody established → no-egress
passes → profile freezes → GATE-W passes → local synthetic protected
launch succeeds (marker produced) → reuse refused → engagement
accounting untouched (before == after).  Provider/model/auditor
execution = ZERO (no provider binary referenced or executed; asserted).
`qh compose-demo` over the same flow: happy ok / marker present /
engagements untouched / reuse refused / controller-imitation powerless
(controller-owned fake custody only; the legitimate synthetic custody
value appears nowhere in its flow), `BOOTSTRAP_FROZEN` recorded with
`bundle_digest f5d7d561…`, files 21 / modules 19 / sealed / spec-tree
match.

## 13. Held accepted mechanics — non-regression (OBSERVED_FACT)

Preserved and retested (surgical interface changes only where a finding
required them): public unrestricted `qh mint` remains absent; root-held
trusted-spec/custody architecture (now mandatorily sealed); claim-only
controller request; security-critical bind/path/hash values outside
controller authority; spec-bound evidence/target/output/Codex
identities; protected-child immutable snapshot mechanism (memfd
`--bind-data`); production Yama/test-fault overrides remain absent
(real Yama >= 1 gates on root AND supervisor; parser-tree structural
proofs unchanged); synthetic concrete provider adapters
(`codex_chatgpt_oauth_v1`, `claude_firstparty_oauth_v1`,
`synthetic_inert_v1` — adapter registry untouched; only the custody
seal semantics under them changed); C-1 bootstrap manifest and C4′
actual-process binding (untouched semantics; the wrong-env C4′ negative
now drives a spec-bound wrong-env controller); hard no-egress
(systemd-resolved/D-Bus masking, ZERO inherited socket FDs — live
regressions pass); GATE-W semantic matrix; zero inherited socket-FD
gate; attempt terminality (absorbing PREEXEC stop) and one-shot
consumption; engagement-accounting separation (asserted); `skill/`
non-interference (§15).  G-1/G-2 design research was NOT reopened.

## 14. Tests and validation — FIRST results (reruns recorded separately)

Environment: Python 3.11.15 + pytest 9.1.1 via `uv run --no-project
--with pytest`; bwrap 0.12.0; Yama ptrace_scope = 1; kernel
7.2.2-1-cachyos; unprivileged user+net namespaces available.

* Pre-change baseline of the 158 prior tests (with the new RED tests
  excluded): **158/158 PASS** (development baseline, recorded to
  `test-outputs/baseline-PRE-HARDENING.txt` — run interleaved with the
  RED authoring, see below).
* RED-first evidence: the new finding-closure tests were written BEFORE
  implementation and recorded failing
  (`test-outputs/hardening-RED-FIRSTRUN.txt`: **37 failed / 6 passed**
  — the 6 passing were pure host-capability probes and structural
  facts that already held; the 13 initially-failing
  `test_seal_uapi.py` cases were also captured inside the combined
  baseline run).
* Complete remediated harness suite: **200/200 PASSED — FIRST complete
  run of the FINAL set**
  (`test-outputs/harness-suite-FIRSTRUN-HARDENED.txt`).
* Development iterations BEFORE the final set, each recorded and
  resolved (nothing rerun away silently):
  - combined baseline+RED run: 13 failed (all `test_seal_uapi.py` RED)
    / 162 passed — the expected pre-implementation state;
  - DEV iteration 1 (implementation pass): 77 failed / 123 passed —
    root subprocess double-execution traced to `qh/__main__.py` calling
    `sys.exit(main())` at import (re-entered by the freeze importing
    `qh.__main__`); fixed by an import guard in `__main__.py`;
  - DEV iteration 2: 12 failed (freeze `PYTHONPATH`-mismatch semantics
    → `spawn_root` now runs the root from the spec-pinned tree; the
    `preexec dup2` fd-closing race in two spec-channel tests → direct
    fd-number passing; docstring literal colliding with a structural
    test);
  - DEV iteration 3: 6 failed (controller fixture died on an uncaught
    `ConnectionResetError` racing a SIGKILLed peer → fixture hardened;
    ledger-event assertion naming; connect-failure reason updated;
    harness-drift test semantics moved to the earlier root-refusal);
  - DEV iterations 4–5: 2 then 1 failed (guard-probe wrapper
    `importlib.util` import; structural name alignment); 199 then 200
    passed;
  - post-final micro-edit (a test-local `--operator-state` path moved
    into `tmp_path` after a stray `X/ledger.jsonl` was observed; the
    pre-edit full-suite output is preserved separately as
    `hardening-DEV-RUN2-pre-final-edit.txt` and the FINAL-set FIRST run
    was recorded afresh after the edit — both runs 200/200).
* Targeted product non-regression (read-only):
  `skill/tests/test_codex_sandbox.py` + `skill/tests/test_codex_runner_mock.py`:
  **34/34 passed (first run)** (`test-outputs/product-targeted-HARDENED.txt`).
* Product FULL deterministic suite `skill/tests`: **686/686 + 99
  subtests PASSED (first run)** (`test-outputs/product-fullsuite-HARDENED.txt`).
  The previously recorded HOST_NODE_PATH_DRIFT condition did NOT
  reproduce in this session (same PATH-ordering-dependent external
  condition as recorded by the prior session — honestly recorded, not
  modified away; no product test or host state was altered).
* `git diff --check`: clean (worktree).
* Secret-pattern scan over every changed/new ordinary file: zero hits
  (no key/token/PEM/JWT/`sk-`/AKIA/xox/ghp patterns).
* Zero-provider: EXTERNAL_PROVIDER_CONTACT = ZERO, MODEL_INFERENCE =
  ZERO, CAMPAIGN_AUDITOR_ENGAGEMENT = ZERO (by construction — the
  pinned "codex" executable is a synthetic fixture; asserted by test).

## 15. Product / historical non-interference (OBSERVED_FACT)

`skill/` tree identity UNCHANGED before/after:
`git rev-parse 27c68fd:skill` == post-change worktree ==
`c792933a862d9a5434681a88d183470dd8b15d2f` (re-verified at staging).
NOT modified: `skill/**`, `skill/tests/**`, `skill/schemas/**`,
`skill/PUBLIC-CONTRACT.md`, `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md`,
`AUCDEV-QUALIFICATION-HISTORY.md`, historical AUCDEV-010 reports,
frozen Campaign-2 artifacts (changed-path confinement proves it
mechanically; product suites ran read-only).  Campaign-2 remains
TERMINAL (§18).  No old verdict transfers.

## 16. Residuals and new blockers (explicit)

1. **R-1 (RESOLVED by this remediation):** the historical "four-seal
   memfd representation unavailable on this host class" residual is
   SUPERSEDED — with the corrected UAPI constants the host establishes
   the representation and authority-critical sealing is MANDATORY and
   enforced (no optional downgrade exists to reconcile).
2. **R-2 (carried, unchanged):** provider adapters remain
   SYNTHETIC-concrete only; real-credential campaign integration
   remains gated on separately authorized campaign preparation + the
   independent harness audit.  No campaign-readiness claim.
3. **R-3 (carried, bounded race):** for DIRECTORY sources
   (evidence/target), a same-UID in-place content write racing between
   the in-child digest verification and payload exec is detected at no
   earlier-than-child point but not atomically prevented; CODE bytes
   are now frozen-and-sealed from BEFORE trigger exposure through the
   whole protected flow (strictly stronger than before).
4. **R-4 (carried, unchanged):** Codex-internal Landlock enforcement of
   the generated profile is not independently verified without running
   Codex (outer-boundary + profile-content proofs only).
5. **R-5 (environmental, carried):** HOST_NODE_PATH_DRIFT did not
   reproduce this session (PATH-order-dependent external condition);
   recorded honestly, unmodified.
6. **R-6 (NEW, accepted residual):** wrong-peer arrival terminally
   consumes the one-shot authority root — classified acceptable
   fail-closed DoS per the remediation tasking (recorded; authority is
   never recovered automatically).
7. **R-7 (NEW, environmental dependency):** the fork-based supervisor
   requires the authority root process itself to run from the
   spec-pinned harness tree (the freeze refuses otherwise — an operator
   misalignment is a fail-closed startup refusal, not a bypass).  The
   Python interpreter/stdlib, bwrap and unshare remain documented
   external TCB assumptions.

No new blocking authority-bootstrap issue was identified by the
implementation evidence.  No STOP condition of remediation §4/§21 was
triggered (the corrected seal capability IS established on this host).

## 17. Governing result (§22)

```
AUCDEV023-CR-REMED-001 = CLOSED  (corrected UAPI constants centralized;
                                  host seal capability RE-ESTABLISHED;
                                  mandatory sealing; no optional
                                  downgrade; §17 test set green)
AUCDEV023-CR-REMED-002 = CLOSED  (freeze-before-trigger + import guard +
                                  fork-from-frozen supervisor; attacker
                                  marker never executed incl.
                                  delete/recreate; §10 test set green)
AUCDEV023-CR-REMED-003 = CLOSED  (pipe / fully-sealed-memfd spec channel
                                  only; ordinary-file stdin and
                                  --spec-fd refused; §7 test set green)
AUCDEV023-CR-REMED-004 = CLOSED  (operator-authored controller identity
                                  in the spec digest; root AND supervisor
                                  enforce uid/pid/starttime; wrong-peer
                                  fail-closed DoS recorded; §12 test set
                                  green)
```

Recommended (IMPLEMENTER position, NOT an independent verdict):

```
AUCDEV023_AUTHORITY_BOOTSTRAP_HARDENING_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK
```

AUCDEV-023 remains **P1 / READY** (NOT DONE).  Independent harness
audit remains **DEFERRED_PENDING_CONTROL_ROOM_READBACK** of THIS
remediation, then MANDATORY on the exact remediated SHA.  Do NOT
transfer any verdict from any earlier SHA to this one.

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

No historical verdict changes; no frozen artifact touched.

## 19. Required lifecycle

```
THIS remediation publication
→ NEXT (EXACTLY ONE): INDEPENDENT CONTROL ROOM READBACK OF THIS
  AUTHORITY BOOTSTRAP HARDENING REMEDIATION
→ then EXACT TARGET FREEZE
→ then the fresh MANDATORY independent harness audit on this SHA
→ only then consider any future qualification package/campaign
```

This session did NOT self-audit, did NOT qualify, did NOT install, and
did NOT perform the independent audit.

Result: `AUCDEV_023_AUTHORITY_BOOTSTRAP_HARDENING_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
