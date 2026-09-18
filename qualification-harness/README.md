# Qualification Harness (AUCDEV-023) — Fail-Closed Execution & Auditor Write Capability

Durable, reusable, NON-PRODUCT harness implementing the accepted C-1 / C-2 /
C-3 mechanisms for future Audit Council qualification campaigns.  It is
**generic**: no historical target, attempt, auditor or finding identity is
baked into behavior — demonstrated profile values live only as DATA in
`fixtures/demonstrated-profile.json`.

This harness does NOT qualify anything, is NOT installed, and has NOT been
independently audited yet.  An independent harness audit is required before
any future qualification package/campaign may rely on it.

## Layout

```
qh/rootauth.py       IR-001: operator authority root (spec + custody pipes;
                     the ONLY production mint; spawns the supervisor)
qh/trusted_spec.py   IR-002: canonical versioned TRUSTED LAUNCH SPEC
                     (identity capture + launch-time verification)
qh/adapters.py       synthetic provider custody adapters (evidence-based)
qh/bootstrap.py      C-1: pre-controller scope provenance + C4' verification
qh/authority.py      C-2: one-shot supervising gatekeeper (spec-authoritative)
qh/custody.py        credential custody (memfd holds; adapter binding)
qh/statemachine.py   terminal PREEXEC attempt lifecycle
qh/noegress.py       hard no-egress gate (facts + checks)
qh/boundary.py       outer boundary (bwrap + immutable trusted-bytes binds)
qh/boundary_child.py in-namespace child entry (gate -> verify -> exec)
qh/codex_profile.py  C-3: identity pin + named restricted profile + CLI
qh/gatew.py          GATE-W matrix + evaluation
qh/campaign.py       campaign engagement accounting (SEPARATE lifecycle)
qh/ledger.py         append-only OBSERVABILITY ledger (never authority)
qh/compose.py        integrated authority-root composition
qh/cli.py            operator entry points (root / supervisor / demo)
fixtures/            payloads + synthetic controller + demonstrated data
tests/               deterministic zero-provider adversarial tests
```

## Threat model and trust boundary

- The **controller** (the agent session that would run a campaign, e.g. a
  Claude Code process with skip permissions) is UNTRUSTED for launch
  authority.  It is **same-UID**: it can read and write every ordinary
  file the user owns, and can SIGKILL any user process.
- **Same-UID controller assumption (inherent limit, disclosed):** no
  ordinary file can be authority — the controller could delete, forge or
  recreate it.  Therefore attempt authority is **process-bound**: it
  exists only in the supervising gatekeeper's memory, which the controller
  cannot read because the supervisor sets `PR_SET_DUMPABLE = 0` and Yama
  `ptrace_scope >= 1` is required (same-UID non-parent ptrace denied).
  What same-UID CANNOT be prevented from: running its own processes,
  killing the supervisor (fail-closed DoS), or reading anything the
  operator deliberately pipes through it.  Operator-vs-controller process
  distinction is procedural (operator session) plus mechanical best
  effort (pipe-only grant channel; optional `--operator-pid`).
- **Linux-only.** Requires: user+network+mount namespaces (bubblewrap,
  unprivileged user namespaces), `memfd_create` + seals, `SO_PEERCRED`,
  Yama ptrace_scope, `/proc`.  No cross-platform claim.  Fail closed when
  an environmental property is absent.
- The **audited product is never modified** by this harness; the frozen
  historical target stays historical.

## C-1 — pre-controller scope provenance

Before the controller starts, the operator captures an immutable,
content-addressed **bootstrap manifest** over the dedicated
`CLAUDE_CONFIG_DIR` scope (sensitive-named files are hashed NEVER —
metadata only).  Capture fails closed on pre-existing `skills/` entries
(disable-all posture) or ANY pre-existing `projects/` state.  The manifest
id is bound into the attempt grant.  After controller start, **C4'**
verifies the ACTUAL controller process through the kernel-provided socket
peer pid, `/proc/<pid>/stat` starttime (pid-reuse defense) and
`/proc/<pid>/environ` (`CLAUDE_CONFIG_DIR` exact match), and that the
current scope equals the manifest plus at most the controller's OWN
current-session project slug subtree (`current tree ⊆ manifest ∪ {own
current-session slug}`).  No universal assumption is made that any
particular runtime version always creates a session tree — observed state
is compared against the bound manifest, so a still-clean scope also
passes.  Modified/deleted manifest entries, new `skills/`, extra
project/session state, PID/env mismatches and manifest tamper all fail
closed.

## C-2 / G-1 — single-use process-bound launch authority

The operator mints a grant (attempt id + root dev/inode + manifest id +
secret) **only to a pipe** (a file-carried grant is refused by mint AND by
the supervisor — copied grants have no authority).  The supervisor
(process started by the operator, never by the controller) immediately
becomes non-dumpable, requires Yama >= 1, binds an abstract unix socket
(no filesystem object to tamper), and serves EXACTLY ONE request:

```
MINTED -> BOUND -> PREEXEC_CHECKING -> CONSUMED_FOR_LAUNCH -> LAUNCHED -> TERMINAL
                        \-> TERMINAL_PREEXEC_STOP (absorbing)
```

Wrong attempt / wrong root / root identity change / manifest mismatch /
binding mismatch / C4' failure / custody failure / no-egress failure /
identity or policy drift / GATE-W failure ⇒ **TERMINAL_PREEXEC_STOP**,
supervisor exits nonzero, and the attempt can never launch again.  Ledger
deletion/recreation, socket deletion and root recreation restore nothing
(authority was never in a file).  Supervisor SIGKILL = denial (DoS) only.
A genuinely new attempt requires a NEW out-of-band mint (duplicate attempt
ids refused).  A pre-inference stop does NOT consume campaign
auditor/model authority (`qh/campaign.py` is never touched by this
lifecycle — asserted by tests).

## Credential custody (MANDATORY for G-1 enforcement)

`CREDENTIAL_CUSTODY_IS_REQUIRED_FOR_G1_ENFORCEMENT`: credential material
enters the AUTHORITY ROOT only through an operator pipe/memfd
(ordinary-file source refused), lives only in a process-bound memfd in
non-dumpable process memory, is unsealed only inside the supervised
boundary's ephemeral storage for the authorized child immediately before
payload exec, and is never printed, hashed into reports, committed or
copied into handoffs (labels + byte lengths only; a redaction registry
scrubs all outputs).  Custody failure fails closed.

**Provider adapters are SYNTHETIC-CONCRETE** (see `qh/adapters.py`):
`codex_chatgpt_oauth_v1` materializes `auth.json` inside a
boundary-private CODEX_HOME (writable at init per the Campaign-2
evidence) and `claude_firstparty_oauth_v1` materializes
`.credentials.json` mode 0600 inside a boundary-private
CLAUDE_CONFIG_DIR — both from frozen non-secret evidence, both driven
ONLY by synthetic inert bytes in every test and rehearsal.  No real
credential is ever read, parsed, inferred or contacted; provider roles
without established evidence remain explicit blockers.  Authority-state
sealing: the four-seal memfd representation is required in strict mode
(`qh root --require-seals`, fails closed when the host cannot produce
it); on the demonstrated host class the sealed representation is
mechanically unavailable, reconciling with the G-1 demonstrated
non-dumpable memory-only posture (outcome recorded, never silently
downgraded).

## Hard no-egress contract

The gate runs INSIDE the would-be-launch environment before any payload
exec and requires: fresh network namespace; private mount namespace; no
usable IPv4/IPv6 address; no usable route (unconditional IPv6
multicast/link-local stubs ignored); loopback DOWN (frozen profile); all
DNS probes fail; all external TCP probes fail; `/run/systemd/resolve`
and `/run/dbus` inaccessible (AF_UNIX host paths are NOT mediated by a
network namespace — the `SYSTEMD_RESOLVED_AF_UNIX_ESCAPE_SURFACE`
regression); **inherited socket FD count = ZERO**
(`HARD_NO_EGRESS_GATE_MUST_REQUIRE_ZERO_INHERITED_SOCKET_FDS`); no
inherited netns FD; descendants cannot setns back to the host netns.  A
bare `unshare --net` is NOT sufficient evidence.

## C-3 / G-2 — Auditor-B application write policy

Exactly ONE persistent model-write root: the auditor-output role
(`-C <auditor-output>`); NO `--add-dir`; NO CLI `-s/--sandbox
workspace-write`; the write capability comes from the **named restricted
permission profile** in the generated disposable `CODEX_HOME/config.toml`
(workspace_roots = one role; filesystem map with one `write` entry +
enumerated reads; network disabled; project trust key).  No root-wide
read entry.  Evidence read-only; target/source read-only or absent per
the outer boundary; CODEX_HOME/auth never a profile entry.  The cosmetic
CLI banner is not authoritative.

## GATE-W — zero-provider pre-inference rehearsal

Before any launch: static validation of the exact generated profile +
dynamic rehearsal of the semantic operation matrix by a LOCAL
deterministic payload inside the composed boundary under hard no-egress
with synthetic custody material (auditor-output CRUD ALLOWED; evidence
write/modify/delete/rename REFUSED; target/host writes REFUSED;
unrelated host paths ABSENT; config readable, auth ABSENT).  A failed
GATE-W ⇒ PREEXEC_STOP; no provider-capable auditor launches afterward.

## Outer boundary

Bubblewrap composes a fresh inner root: `/usr` `/lib*` `/etc` read-only
(merged-usr toolchain), spec binds for evidence (RO), CODEX_HOME (RO),
target (RO/absent) and auditor-output (the ONE rw bind), `--tmpfs /tmp`
(accepted EPHEMERAL namespace-local residual — never a persistent
host-backed model-write surface), `--dev`/`--proc`, PID/IPC/UTS/NET
unshared, environment cleared then set.  Host AF_UNIX resolver/DBus paths
are absent (masked by private-mount absence, verified by the gate).

## Fail-closed lifecycle

Invalid state transitions raise and force terminal stops; every mandatory
gate failure is terminal for the attempt; missing environmental
properties (Yama, bwrap, memfd seals) refuse launch rather than degrade.

## Zero-provider rehearsal

All tests and the demo (`python -m qh.cli compose-demo --out DIR`) run
with local payloads, synthetic credentials and hard no-egress only:
EXTERNAL_PROVIDER_CONTACT = ZERO, MODEL_INFERENCE = ZERO, and campaign
engagement accounting is never touched.

## Explicit residuals

1. Provider adapters are implemented against SYNTHETIC bytes only; real
   credential integration (operator-side custody of live credentials)
   remains gated on separately authorized campaign preparation.
2. Same-UID cannot mechanically distinguish operator from controller
   processes; the pipe-only grant channel + operator-session procedure +
   optional operator-pid binding are the boundary.  A controller that
   somehow captured live grant pipe bytes could start its own supervisor
   — prevented only by process isolation (non-dumpable), not by files.
3. GATE-W proves the generated profile CONTENT and the OUTER boundary
   semantics; Codex-internal Landlock enforcement of the profile is a
   residual verifiable only by a future authorized (no-egress) campaign.
4. The gate's DNS/TCP probe names are data; on hosts without
   systemd-resolved the AF_UNIX regression is exercised via fixtures and
   the live bare-netns test where available.
5. Yama < 1 hosts cannot run the root or supervisor (fail closed) — by
   design.  The production CLI has NO trust-check override of any kind
   (`--yama-override` and every `--fault`-style flag are rejected by the
   production parser); deterministic test fault injection lives ONLY in
   the test suite via monkeypatched reader/launcher seams.
6. Four-seal memfd sealing is unavailable on the demonstrated host class
   (an MFD_ALLOW_SEALING memfd cannot be populated; F_ADD_SEALS fails
   without it).  Strict mode fails closed on such hosts; the default
   records `seal_status=unavailable_kernel` and keeps the non-dumpable
   memory-only hold (the accepted G-1 demonstrated posture).

## Trusted launch spec and trusted bytes (IR-002)

The controller request is a CLAIM, never authority: its schema carries
only attempt id, starttime claim, env claims and payload kind — every
security-critical value (harness code identity, boundary child,
evidence/target/auditor-output sources, codex home/config/exe/sha,
profile, mount roles, adapter identity, payload role) comes from the
canonical versioned trusted launch spec bound in the authority root.
Unknown request fields are TERMINAL.  At launch the complete spec is
re-verified against the live filesystem (object identity by dev/ino
rejects delete/recreate; content digests reject swaps) and the verified
harness/config/executable bytes are SNAPSHOTTED into process-bound
memfds and materialized inside the boundary via bwrap `--ro-bind-data`
— the protected launch never executes host-path code.  Evidence/target
tree digests are re-verified INSIDE the boundary before payload exec
(closing the check-to-use substitution window).

## What this harness does NOT prove

- No qualification, installation, or fitness of any Audit Council
  candidate (the frozen historical target is untouched and NOT repaired
  retroactively).
- No Campaign-2 recovery, no Campaign-3, no auditor/model/provider
  execution.
- No independent audit of the harness itself — that is a required,
  separate next step before any campaign reliance.
- No proof that Codex's runtime enforces the generated profile
  internally (only that the profile is generated, frozen, validated and
  that the outer OS boundary enforces the matrix).
