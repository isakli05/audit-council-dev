# AUCDEV-023 — Qualification Harness Implementation (C-1 / C-2 / C-3): Implementation Publication (Canonical Record)

| Field | Value |
|---|---|
| Session class | BOUNDED ZERO-PROVIDER IMPLEMENTATION SESSION (operator-authorized AUCDEV-023 implementation task against the recorded readiness acceptance criteria) — NOT Auditor A/B, NOT the Control Room, NOT a qualification authority, NOT an installation authority; NO auditor/model/provider execution; NO Campaign-2 recovery; NO Campaign-3; NO product change; NO modification of any historical frozen artifact; the harness was NOT self-audited |
| Date | 2026-09-18 (Europe/Istanbul) |
| Exact implementation base | `695fd11a67f3fb3d80fc519e66755dab33ae562f` (tree `9977862cf44a3eafca6f3c792c14c97d3bce5a61`; sole parent `2b70592486d510d02dca552a1aebd7b382fd7556`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at bootstrap (origin/master identical) and re-resolved EXACT immediately before the single fast-forward push; THIS implementation publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Disposition | `AUCDEV023_IMPLEMENTATION_COMPLETE_AWAITING_CONTROL_ROOM_READBACK` (recommended; NOT DONE; AUCDEV-023 remains **P1 / READY** — implementation completion and readiness status are different facts) |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **STILL REQUIRED** — this publication does NOT self-audit, does NOT qualify, does NOT install the harness |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in this
session), `INFERENCE` (derived), `HYPOTHESIS` (unverified), `REQUIREMENT`
(task/record-mandated property).

## 1. Scope and authority

REQUIREMENT (tasking): implement the accepted C-1 / C-2 / C-3
qualification-harness mechanisms as a durable, reusable, NON-PRODUCT
harness component under a new top-level `qualification-harness/` subtree;
generic (no historical target/attempt/auditor/verdict identity baked into
behavior; demonstrated profile values carried only as DATA in
`fixtures/demonstrated-profile.json`); mechanically testable with
synthetic/zero-provider fixtures.  NOT authorized: product semantic
change, Campaign-2 recovery, Campaign-3, Auditor-A/B execution, any
qualification campaign, real provider/model inference, installation,
qualification, modification of historical frozen artifacts.  All held.

`skill/` tree (reference / non-regression input ONLY): NOT modified —
tree identity `c792933a862d9a5434681a88d183470dd8b15d2f` at the exact
base and identical in the implementation commit (OBSERVED_FACT;
`git rev-parse <base>:skill` == `git rev-parse <result>:skill`).  The
historical frozen target `d77333e86aa091d2ac003e9a2ad26c88dff56aeb`
remains historical and unchanged; nothing here repairs it
retroactively.

## 2. Architecture (30 source files under `qualification-harness/`)

- `qh/bootstrap.py` — C-1: pre-controller content-addressed bootstrap
  manifest over the dedicated `CLAUDE_CONFIG_DIR` scope (sensitive-named
  files hashed NEVER — metadata only) + C4′ verification (SO_PEERCRED
  peer pid, `/proc/<pid>/stat` starttime pid-reuse defense,
  `/proc/<pid>/environ` `CLAUDE_CONFIG_DIR` exact match, manifest
  integrity re-hash, scope consistency
  `current tree ⊆ manifest ∪ {own current-session slug}`).
- `qh/authority.py` — C-2: pipe-only operator `mint` (ordinary-file
  output refused; duplicate attempt refused) + the one-shot supervising
  gatekeeper (abstract-socket single request, `PR_SET_DUMPABLE=0`,
  Yama ptrace_scope >= 1 mandatory gate, terminal PREEXEC_STOP, replay /
  wrong-attempt / wrong-root / root-identity-change / manifest-mismatch
  refusal, engagement accounting never touched).
- `qh/custody.py` — credential custody: pipe/memfd-only source
  (ordinary-file source refused), memory-only hold in a memfd, seals
  best-effort (see §8 residuals), redaction registry, child-only
  materialization plan, provider adapter INTERFACE ONLY.
- `qh/statemachine.py` — MINTED→BOUND→PREEXEC_CHECKING→
  CONSUMED_FOR_LAUNCH→LAUNCHED→TERMINAL with absorbing
  TERMINAL_PREEXEC_STOP; invalid transitions raise and force closed.
- `qh/noegress.py` — hard no-egress gate: facts collection (fd/ns scan,
  per-iface ioctl flags/addresses, /proc route tables, masked AF_UNIX
  path connectability, DNS/TCP probes, forked setns-regain probe) +
  fail-closed checks incl. ZERO inherited socket FDs and the
  systemd-resolved AF_UNIX escape regression.
- `qh/boundary.py` + `qh/boundary_child.py` — outer boundary:
  `unshare --user --map-root-user --net` (fresh netns, loopback
  untouched/DOWN — the frozen demonstrated profile) wrapping bwrap
  (fresh inner root: `/usr` `/lib*` `/etc` RO, harness RO at `/opt/qh`,
  evidence/target/codex-home RO, auditor-output the ONE rw bind,
  `--tmpfs /tmp` `/run-qh`, `--dev/--proc`, `--clearenv` + explicit env);
  child entry = no-egress gate → custody verification → payload exec;
  results return via a write-bound JSONL file; custody memfds enter via
  `--bind-data` (bwrap >= 0.10 removed `--pass-fd`).
- `qh/codex_profile.py` — C-3: identity pin (SHA-256 of the supplied
  executable), named restricted permission profile generation
  (`default_permissions` + `[permissions.<name>]` with one
  `workspace_roots` role, one `write` entry, enumerated reads, network
  disabled, `[projects.<role>]` trust), static semantic validation (no
  root-wide read, no CODEX_HOME/auth entry, evidence read-only), CLI
  construction (`-C <auditor-output>`; `--add-dir` / `-s` / `--sandbox`
  forbidden), freeze/drift verification.
- `qh/gatew.py` — GATE-W: the 17-operation semantic matrix +
  evaluation; static validation wrapper.
- `qh/campaign.py` — separate campaign engagement accounting
  (NEVER called by the attempt lifecycle; separation asserted by tests).
- `qh/ledger.py` — append-only OBSERVABILITY ledger (explicitly NOT
  authority).
- `qh/compose.py` + `qh/cli.py` — composition environment, subprocess
  supervisor orchestration, operator CLI (`mint | supervisor`,
  `compose-demo`, `selfcheck`), documented TEST fault-injection hooks
  (`--yama-override`, `--fault ...`; every use ledger-recorded).
- `fixtures/` — local deterministic payloads (`gatew_payload.py`,
  `launch_sim_payload.py`), synthetic controller, demonstrated-profile
  DATA.
- `tests/` — 84 deterministic tests (§5).  `README.md` — threat model,
  trust boundary, contracts, residuals, what the harness does NOT prove.

## 3. C-1 — OBSERVED_FACT (tests `test_bootstrap_c1.py`, 12 PASS)

Clean pre-controller capture PASS; content-addressed determinism (same
content ⇒ same id; changed content ⇒ different id); pre-existing
`skills/` and ANY pre-existing `projects/` state rejected at capture;
own current-session slug tree allowed at C4′ (accepted
`current tree ⊆ manifest ∪ {own current-session slug}` rule) while TWO
new slugs / new top-level state / new `skills/` after capture are
rejected; peer-pid mismatch, starttime (pid-reuse) mismatch,
`CLAUDE_CONFIG_DIR` actual-vs-claim mismatch, manifest tamper (digest
mismatch), scope modification (content change of a recorded file) all
fail closed; a still-clean scope ALSO passes (no universal
runtime-tree assumption — evidence boundary preserved); sensitive files
never hashed into the manifest; fixture-reader injection path also
covered.  Live-controller cases verify through the ACTUAL
`/proc/<pid>/environ` of spawned processes.

## 4. C-2 / G-1 — OBSERVED_FACT (tests `test_authority_c2.py` +
`test_statemachine.py` + `test_compose.py`, all PASS)

Single-use PASS with real supervisor subprocesses (abstract-socket
single request; marker file produced through the rw auditor-output
bind; supervisor exit 0; state TERMINAL); second use / replay refused
(connection refused — the supervisor and its authority are gone);
wrong-attempt, wrong-root, root-identity-change (deleted+recreated
root), manifest-id mismatch each ⇒ TERMINAL_PREEXEC_STOP with exit 9;
C4′ failure (controller starttime binding mismatch; real
env-mismatch flow) ⇒ terminal stop, grant never relaunchable; ledger
deletion + forged recreation restore nothing (authority was never in a
file); supervisor SIGKILL = denial only, same attempt re-mint refused,
a genuinely NEW attempt with a fresh mint runs independently; campaign
engagement accounting UNTOUCHED by both the terminal-stop flow and the
consumed happy path; copied grant in an ordinary FILE refused by the
supervisor (exit 3, "not a pipe"); Yama failure simulation (override 0)
⇒ startup fail-closed exit 6 with ledger-recorded
TERMINAL_PREEXEC_STOP; custody via ordinary file or missing fd ⇒
terminal stop; operator-pid mismatch refused; the live supervisor
verifiably runs non-dumpable (same-UID non-parent cannot read
`/proc/<pid>/environ` — kernel-process-bound authority).

## 5. Credential custody — OBSERVED_FACT (tests `test_custody.py`, 5 PASS + integration)

Establish from pipe OK (sealed memfd hold, label/length only); ordinary
file source refused; empty source refused; child plan + idempotent
teardown deterministic; same-UID process cannot read a dumpable=0
process's environ/mem/fd-list (live kernel proof); after a full flow no
synthetic credential value appears in ANY operator-state file or the
supervisor stderr.  PROVIDER-SPECIFIC INTEGRATION: INTERFACE ONLY
(`custody.PROVIDER_SPECIFIC_INTEGRATION_STATUS`) — real provider
credential injection is NOT implemented and NOT claimed (implementation
blocker recorded, §8).

## 6. Hard no-egress + C-3 + GATE-W — OBSERVED_FACT

No-egress (`test_noegress.py`, 12 PASS): fixture matrix (zero socket
FDs PASS; inherited socket FD FAIL; ns-fd FAIL; shared mount ns FAIL;
address/route/lo-up FAIL; systemd-resolved connectable FAIL; DNS/TCP
success FAIL; setns regained FAIL / denied-pass) + LIVE regression
inside `unshare --user --map-root-user --net` WITHOUT a private mount
namespace: the host `io.systemd.Resolve` AF_UNIX socket is connectable
and the gate FAILS with `MASKED:/run/systemd/resolve` (the historical
`SYSTEMD_RESOLVED_AF_UNIX_ESCAPE_SURFACE` finding, reproduced
deterministically WITHOUT any external DNS query — probe set empty);
with the composed boundary (private mount namespace, masked by
absence) the gate PASSES; a REAL socket descriptor present in the
gated process fails the gate (`ZERO_INHERITED_SOCKET_FDS`); the
boundary gate holds with the full GATE-W payload (DNS/TCP probes
execute inside and fail).

C-3 (`test_codex_profile_c3.py`, 11 PASS): exact generated config
(byte-stable render; `default_permissions`; exactly one
`workspace_roots` role; one `write` entry; evidence `read`; system
read set; `network.enabled=false`; project trust key); only-one-write-
root; root-wide read entry rejected; second write root rejected;
network-enabled rejected; CLI `-C <auditor-output>` with NO `--add-dir`
and NO `-s/--sandbox` (forbidden flags raise); generated CODEX_HOME
contains config.toml ONLY (no auth material); CODEX_HOME/auth entries
in the profile rejected; identity pin + REAL binary drift rejection;
frozen-profile REAL config drift rejection; demonstrated fixture DATA
loads and drives a spec end-to-end.

GATE-W (`test_gatew.py`, 4 PASS + integration): static validation pass
+ drift flagged; payload-matrix evaluation; DYNAMIC full rehearsal
inside the composed boundary with custody — 17 operations
(auditor-output create/write/modify/mkdir/delete ALLOWED; evidence
read ALLOWED, create/write/modify/delete/rename REFUSED; target write
REFUSED; `/etc` `/root` `/home` access REFUSED/ABSENT; codex config
readable, `auth.json` ABSENT) with all expected, custody materialized
for the authorized child (length only), auditor-output ops REAL on the
host rw surface, evidence untouched; a REAL widened-evidence boundary
(evidence rw-bound) makes GATE-W FAIL (⇒ PREEXEC_STOP upstream).

## 7. Composition — OBSERVED_FACT (`test_compose.py`, 10 PASS)

The mandated ORDER proven from ONE integrated attempt's observability
ledger: manifest captured → CONTROLLER_BINDING_ESTABLISHED → C4P_RESULT
(passed) → AUTHORITY_BOUND → CUSTODY_ESTABLISHED → NOEGRESS_GATE
(passed) → PROFILE_FROZEN → GATEW_RESULT (passed) →
CONSUMED_FOR_LAUNCH → LAUNCHED → TERMINAL; marker produced; engagement
accounting untouched; reuse fails closed.  Negative branches all
terminal: REAL C4′ failure (actual controller env elsewhere);
no-egress failure (injected) + real inherited-socket-FD gate failure
(module level); GATE-W failure (injected) + REAL widened-evidence
failure (module level); Codex binary identity drift (REAL byte-swap
+ injected) and profile policy drift (REAL config mutation +
injected); custody failure (REAL ordinary-file source); Yama failure
simulation (startup terminal); replay; ledger deletion.  Zero-provider
assertion: the protected launch runs a local deterministic script; no
`codex exec` process is ever launched by the harness.

## 8. Residuals, limitations, blockers (explicit)

1. PROVIDER-SPECIFIC CREDENTIAL INTEGRATION — IMPLEMENTATION BLOCKER
   (interface only).  All custody tests use synthetic inert fixtures.
2. Same-UID operator-vs-controller process distinction is procedural +
   mechanical best effort (pipe-only grant; optional operator-pid
   binding); no file can be authority (documented threat model).
3. GATE-W proves the generated profile CONTENT and the OUTER OS
   boundary semantics; Codex-internal Landlock enforcement of the
   profile is NOT independently verified without running Codex
   (residual for a future authorized no-egress campaign).
4. Kernel observations on the demonstrated host (7.2.2-cachyos,
   OBSERVED_FACT): bwrap 0.12.0 removed `--pass-fd` (protocol uses
   `--bind-data` + bound files); bwrap `--unshare-net` brings loopback
   UP (violates the frozen loopback-DOWN profile) ⇒ the boundary wraps
   bwrap in `unshare --user --map-root-user --net` (the demonstrated
   chain); bwrap drops capabilities in the child (in-child
   `unshare(CLONE_NEWNET)` is EPERM); `F_ADD_SEALS` returns EINVAL on
   this kernel ⇒ memfd seals are best-effort and RECORDED
   (`seal_status=unavailable_kernel`) — the custody hold remains
   memory-only and process-bound.  `--yama-override`/`--fault` hooks
   are deterministic TEST fault injections (ledger-recorded).
5. Host AF_UNIX escape regression is exercised live where
   systemd-resolved exists; the DNS/TCP probe names are DATA.
6. `test dirs` write-scaffold: `/tmp` and `/run-qh` tmpfs are the
   accepted ephemeral namespace-local residual (residual E carried).

## 9. Tests and validation — FIRST results (reruns listed separately)

Environment: Python 3.11.15 + pytest 9.1.1 via `uv run --no-project
--with pytest` (host `/usr/bin/python` 3.14.7 carries no pytest);
bwrap 0.12.0; Yama ptrace_scope = 1; unprivileged user+net namespaces
available.

- Harness suite `qualification-harness/tests` (84 tests):
  **84 passed** — FIRST run of the complete final set
  (`test-outputs/harness-suite-FINAL-FIRSTRUN.txt`).  Development
  iterations BEFORE the final set (all resolved; nothing rerun away
  silently): initial subset runs failed on (a) a test-authoring
  truncate-then-read bug, (b) missing stdlib memfd binding → ctypes
  wrapper + kernel MFD-flag semantics, (c) the C-1 single-slug rule
  counting the `projects/` container node, (d) an ioctl ifreq buffer
  size, (e) bwrap `--pass-fd` absence → boundary channel redesign,
  (f) bwrap lo-UP → outer-unshare chain, (g) memfd offset rewind for
  repeated `--bind-data`, (h) a leaked supervisor from a failing run
  (test-hygiene: env cleanup fixture), (i) import/name fixes.  The
  first FULL-suite run including live tests after (h)/(i) fixes:
  84 passed, 0 failed.
- Product non-regression (read-only):
  `skill/tests/test_codex_sandbox.py` + `skill/tests/test_codex_runner_mock.py`:
  **34 passed** (first run).
- Product FULL deterministic suite `skill/tests` (686 tests + 99
  subtests): **685 passed, 1 failed** (first run,
  `test-outputs/product-fullsuite-FIRSTRUN.txt`) —
  `test_tier4_da27c0.py::TestWrapperExecutionEnvironment::test_f2_intended_node_runtime_selected`.
  ROOT CAUSE (OBSERVED_FACT, PRE-EXISTING, unrelated to this
  implementation which modifies no tracked file): host `node` PATH
  drift — `~/.local/bin/node` → `/home/isa/.hermes/node/bin/node`
  (created 2026-09-10) while the wrapper correctly resolves the nvm
  v24.14.0 toolchain INSIDE the sandbox; the test's OUTER expectation
  (`shutil.which("node")`) now resolves to the hermes node.  RERUN
  (recorded separately, `product-fullsuite-F2-RERUN-with-nvm-PATH.txt`):
  still failed, same environmental cause (`/home/isa/.nvm/.../node !=
  /home/isa/.hermes/node/bin/node`).  Per tasking §16 the unrelated
  condition is PRESERVED and reported, not reset; the failing test
  was NOT modified.
- `git diff --check`: clean (worktree; staged diff re-checked before
  commit).
- Zero-provider: every harness mechanism executes local payloads,
  synthetic credentials and hard no-egress namespaces only —
  EXTERNAL_PROVIDER_CONTACT = ZERO, MODEL_INFERENCE = ZERO,
  CAMPAIGN_AUDITOR_ENGAGEMENT = ZERO (OBSERVED_FACT by construction:
  no provider binary is referenced or executed anywhere in the
  harness; the pinned "codex" executable in compositions is a
  synthetic fixture whose bytes the tests generate).

## 10. Campaign-2 non-interference (OBSERVED_FACT)

`AUDITOR_A_AUTHORITY = CONSUMED_CLOSED`; `AUDITOR_B_AUTHORITY =
CONSUMED_CLOSED`; `MODEL_ENGAGEMENTS_AUTHORIZED = 2 / USED = 2`;
`FIRST_PASS_A = PRESENT/FROZEN`; `FIRST_PASS_B = ABSENT`;
`FIRST_PASS_BARRIER = CLOSED`; `CAMPAIGNS = 2 OF MAX 2`;
`CAMPAIGN_3 = NOT AUTHORIZED / DOES NOT EXIST`; AUCDEV-010 remains
**P1 / BLOCKED**; qualification **NONE**; installation **NONE**.  This
implementation touched no frozen artifact and no historical report.

## 11. Changed paths (EXACTLY this set)

NEW: `qualification-harness/**` (30 files: 17 `qh/` modules, 4
fixtures, 9 tests, README, .gitignore — no compiled artifacts);
`docs/chatgpt-project/AUCDEV-023-QUALIFICATION-HARNESS-IMPLEMENTATION.md`
(THIS record).
MODIFIED: `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (record 80 +
current-facing fields), `docs/chatgpt-project/AUCDEV-BACKLOG.md`
(AUCDEV-023 row + work item + history record 5; counts UNCHANGED).
NOT changed: `skill/**` (tree identity proven unchanged),
`AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md`, qualification history,
architecture summary, schemas/contracts, frozen Campaign-2 artifacts,
all historical reports.  Unrelated working-tree state preserved
unstaged: `smoke-fixture` / `smoke-fixture-103` submodule gitlink
drift; untracked `aucdev019-evidence/`.

## 12. Status and required lifecycle

```
AUCDEV-023 = P1 / READY  (unchanged — implementation completion and
                          readiness are different facts)
IMPLEMENTATION COMPLETE (mechanical/test strength, zero provider)
→ NEXT (EXACTLY ONE): INDEPENDENT CONTROL ROOM READBACK OF THIS
  IMPLEMENTATION PUBLICATION
→ then INDEPENDENT HARNESS AUDIT
→ remediation/re-audit if needed
→ only then consider a fresh future qualification package/campaign
```

This harness has NOT been independently audited; no qualification and
no installation is claimed or implied; the harness does NOT inherit a
qualification verdict from the G-1/G-2 design/probe results.

Result: `AUCDEV023_QUALIFICATION_HARNESS_IMPLEMENTATION_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
