# AUCDEV-023 — Trust-Anchor and Launch-Spec Binding Remediation (Canonical Record)

| Field | Value |
|---|---|
| Session class | BOUNDED ZERO-PROVIDER REMEDIATION IMPLEMENTATION SESSION (operator-authorized AUCDEV-023 trust-anchor and launch-spec binding remediation against findings AUCDEV023-CR-IMPL-001/-002/-003 and the held provider credential-custody integration blocker) — NOT Auditor A/B, NOT the Control Room, NOT a qualification authority, NOT an installation authority, NOT an independent harness audit; NO auditor/model/provider execution; NO Campaign-2 recovery; NO Campaign-3; NO product (`skill/`) modification; the harness was NOT self-audited; NO G-1/G-2 design research reopened |
| Date | 2026-09-18 (Europe/Istanbul) |
| Exact remediation base | `2e53ad583b00fbec6f62fcd0f80f39bd4acbfabd` (tree `df42664adf43d04f1b5b9249e66646a76f3fe02a`; sole parent `3c59264007bab172e72a5c03c0299a5dec71f8d3`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this remediation's bootstrap and re-resolved EXACT immediately before staging and immediately before the single fast-forward push; THIS remediation publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Remediation scope | Close ONLY IR-001 (`CONTROL_ROOM_MINT_ROOT_NOT_MECHANICALLY_ANCHORED`), IR-002 (`CONTROLLER_SUPPLIED_LAUNCH_SPEC_NOT_BOUND` incl. `SELF_ASSERTED_CODEX_IDENTITY_PIN` and `CONTROLLER_CHOSEN_RW_BIND_AND_HARNESS_ROOT`), IR-003 (`PRODUCTION_YAMA_OVERRIDE_BYPASS_PRESENT`), and as much of `PROVIDER_CREDENTIAL_CUSTODY_INTEGRATION_NOT_IMPLEMENTED` as existing non-secret evidence mechanically supports |
| Disposition (recommended) | `AUCDEV023_TRUST_ANCHOR_REMEDIATION_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK` (see §24 for the governing assessment and the recorded host-condition residual) |
| Qualification / installation | qualification NONE / installation NONE (unchanged) |
| Independent harness audit | **STILL REQUIRED — DEFERRED_PENDING_CONTROL_ROOM_READBACK of THIS remediation** (not executed in this session; a verdict on the base SHA does not transfer to the remediated SHA) |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `INFERENCE` (derived), `HYPOTHESIS` (unverified),
`REQUIREMENT` (task/record-mandated property).

## 1. Base identities and confirmed governing state (OBSERVED_FACT)

Live `refs/heads/master` resolved EXACT `2e53ad583b00fbec6f62fcd0f80f39bd4acbfabd`
(tree `df42664adf43d04f1b5b9249e66646a76f3fe02a`; sole parent
`3c59264007bab172e72a5c03c0299a5dec71f8d3`).  All mandated documents and
harness sources were read at that exact SHA.  Confirmed governing state:

```
AUCDEV-023                    = P1 / READY
implementation                = PARTIALLY_ACCEPTED / REMEDIATION_REQUIRED
independent harness audit     = DEFERRED_PENDING_REMEDIATION
AUCDEV-010                    = P1 / BLOCKED
Campaign-2                    = TERMINAL
qualification                 = NONE
installation                  = NONE
```

Pre-existing unrelated working-tree state preserved unstaged throughout:
`smoke-fixture` / `smoke-fixture-103` gitlink drift (inner untracked
`audit-output/` leftovers; nested HEADs MATCH the recorded gitlinks —
verified) and untracked `aucdev019-evidence/`.

## 2. Exact changed paths (OBSERVED_FACT)

NEW (9 harness + 1 report):

```
qualification-harness/qh/rootauth.py
qualification-harness/qh/trusted_spec.py
qualification-harness/qh/adapters.py
qualification-harness/tests/test_sealing.py
qualification-harness/tests/test_trusted_spec.py
qualification-harness/tests/test_rootauth.py
qualification-harness/tests/test_production_surface.py
qualification-harness/tests/test_trusted_claims.py
qualification-harness/tests/test_provider_adapters.py
docs/chatgpt-project/AUCDEV-023-TRUST-ANCHOR-LAUNCH-SPEC-REMEDIATION.md
```

MODIFIED (17 harness + 2 governance):

```
qualification-harness/qh/authority.py
qualification-harness/qh/boundary.py
qualification-harness/qh/boundary_child.py
qualification-harness/qh/cli.py
qualification-harness/qh/compose.py
qualification-harness/qh/custody.py
qualification-harness/qh/util.py
qualification-harness/qh/__init__.py
qualification-harness/fixtures/gatew_payload.py
qualification-harness/fixtures/launch_sim_payload.py
qualification-harness/tests/test_authority_c2.py
qualification-harness/tests/test_compose.py
qualification-harness/tests/test_custody.py
qualification-harness/tests/test_gatew.py
qualification-harness/tests/test_noegress.py
qualification-harness/README.md
qualification-harness/.gitignore
docs/chatgpt-project/AUCDEV-CURRENT-STATE.md   (record 82, append-only)
docs/chatgpt-project/AUCDEV-BACKLOG.md         (AUCDEV-023 record 7, append-only)
```

Total **29 changed paths**, confined EXACTLY to the authorized mutation
families (`qualification-harness/**`, CURRENT-STATE, BACKLOG, the NEW
remediation report).  `fixtures/fake_controller.py` and
`fixtures/demonstrated-profile.json` are UNCHANGED.  The
qualification-harness tree grows from 31 to **40 tracked blobs**.

## 3. Architecture delta (OBSERVED_FACT)

```
BEFORE (implementation 3c59264):
  qh mint (public CLI, caller-supplied attempt/root/manifest/state)
    | pipe
  qh supervisor (CLI; --yama-override/--fault flags; request supplies
    harness_root/binds/codex identity/config/profile)
    -> boundary (host harness_root RO-bound at /opt/qh)

AFTER (THIS remediation):
  OPERATOR (out-of-band, before controller request execution)
    pipes: trusted-launch-spec.json  +  provider credential bytes
      -> qh root  (PR_SET_DUMPABLE=0; REAL Yama>=1 gate; spec id +
         custody bound in process memory; abstract socket; performs the
         ONLY production mint for EXACTLY the spec-bound attempt, at most
         once; spawns the supervisor as its own child)
           | grant+spec on a pipe; custody memfd inherited
         qh supervisor  (ppid==root enforced from the grant; REAL Yama
           gate, no override anywhere; CLAIM-ONLY request schema;
           TRUSTED_SPEC_VERIFY; spec-bound adapter + custody; verified
           harness/config/exe bytes snapshotted to memfds; noegress;
           spec-bound identity/profile freeze; GATE-W; one-shot consume)
             -> boundary (NO host code bind: /opt/qh, config, trusted exe
                and credential materialize from memfd --bind-data /
                --ro-bind-data; evidence/target RO from spec-bound
                verified sources; auditor-output the ONE rw bind;
                in-child re-verification of trusted bytes + source
                digests before payload exec)
```

The public `qh mint` subcommand is REMOVED from the production CLI
(parser rejects it); `mint_attempt_grant()` remains an internal
operator-side API whose production caller is the authority root only.

## 4. Trusted authority-root design (IR-001) — OBSERVED_FACT

`qh/rootauth.py` implements the accepted design direction:

* the root is established BEFORE controller-controlled request execution
  by the OPERATOR: `qh root --operator-state D --custody-fd N <
  trusted-launch-spec.json` — the spec and the credential bytes arrive
  through operator-held inherited FDs (an ordinary-file custody source
  is refused: `CUSTODY_SOURCE_KIND_REFUSED:file`);
* the root immediately sets `PR_SET_DUMPABLE=0` (same-UID non-parents
  cannot read its memory, environ or fd list — kernel-proven by test)
  and requires Yama ptrace_scope >= 1 via the REAL kernel read;
* the canonical spec id and the credential bytes are bound ONLY in root
  process memory (memfd); the persisted
  `operator-state/specs/<spec_id>.json` copy is OBSERVABILITY ONLY and
  tamper-evident through the self-certifying content address;
* the root serves EXACTLY ONE mint on its abstract socket
  (`\0qh-root-<spec_id16>`): only the spec-bound attempt id is accepted
  (`MINT_WRONG_ATTEMPT` otherwise, root fails closed); the mint itself
  is performed by the root process (no caller-supplied authority
  values anywhere); duplicate attempts are refused from root memory +
  the observability ledger;
* the root itself constructs and spawns the one-shot supervisor and
  passes grant, spec and custody ONLY through inherited pipes/fds;
  the supervisor enforces `ppid == root_pid` (recorded by the minting
  process inside the grant — never a caller-supplied CLI flag;
  `--operator-pid` is REMOVED) and sets `PR_SET_PDEATHSIG=SIGKILL` so a
  killed root cannot leave a listening supervisor behind;
* root SIGKILL is fail-closed denial (DoS) only (§18.F test);
* a controller-created parallel root can at most mint a powerless
  imitation (§18.B tests): it holds no operator credential bytes and no
  operator-authorized spec, and its flows never touch the legitimate
  custody value.

### 4.1 Root capability / sealed state (§6 reconciliation) — OBSERVED_FACT

The four-seal representation over POPULATED memfd content is
mechanically UNAVAILABLE on the demonstrated host class (re-confirmed
twice in this session, sandboxed and unsandboxed): a memfd created with
`MFD_ALLOW_SEALING` cannot be populated (`write(2)`/`ftruncate(2)` →
EINVAL), and `F_ADD_SEALS` on a memfd created without it returns EINVAL;
additionally `F_GET_SEALS` returns a value even for ordinary files on
this kernel class (memfds are therefore discriminated by their
`/proc/self/fd` link target).  Reconciliation implemented:

* STRICT policy: `qh root --require-seals` REQUIRES
  `F_SEAL_WRITE|F_SEAL_GROW|F_SEAL_SHRINK|F_SEAL_SEAL` to succeed and
  FAILS CLOSED up front when the host cannot produce it
  (`SEALED_REPRESENTATION_UNAVAILABLE_ON_THIS_HOST`, exit 13) —
  deterministically proven by `tests/test_sealing.py` on this host;
* DEFAULT posture: authority bytes live in anonymous process-bound
  memfds with `PR_SET_DUMPABLE=0` + Yama >= 1 as the PRIMARY protections
  and the seal outcome RECORDED (`seal_status=unavailable_kernel`) —
  the previously demonstrated G-1 mechanism, per remediation §6's
  reconciliation clause, never silently downgraded;
* root secret hygiene: no authority secret travels in argv, environment
  variables, ordinary files, logs or reports (the per-attempt grant
  secret is redaction-registered and never authenticates anything by
  itself); authority state dies with its process.

## 5. Trusted launch-spec format and binding (IR-002) — OBSERVED_FACT

`qh/trusted_spec.py` introduces the ONE canonical versioned TRUSTED
LAUNCH SPEC (`qh-trusted-launch-spec/1`), authored by the operator and
delivered to the root through the operator pipe.  Minimum
security-critical content (validated fail-closed, `validate_spec`):
spec version; attempt id; attempt/root identity (realpath+dev+ino);
bootstrap manifest identity (manifest id + config dir); expected
controller-scope binding inputs (`CLAUDE_CONFIG_DIR`); trusted harness
implementation identity (recursive digest over the exact executable
byte set); trusted boundary-child identity (pinned member of that set);
evidence source identity; target source identity; auditor-output
role/identity; exact Codex executable identity (realpath+dev+ino+SHA-256);
expected Codex version/profile identity; exact generated config digest;
allowed mount/read/write roles; credential-custody adapter
identity/version; provider role; required no-egress policy (MUST be
true); exact payload/launch role.  The document is canonically
serialized (sorted-key compact JSON) and its content address is the
spec id — bound in root memory, embedded in the minted grant
(`grant.spec_id`), and re-checked by the spawned supervisor (a spec
whose canonical id differs from the grant-bound id is refused at
supervisor startup, exit 13 — closing the transit channel).

Source identities are captured at authoring time (realpath, dev, ino,
recursive content digest with sensitive-named files recorded by
metadata only — no credential value is ever hashed into a spec) and
re-verified at launch by `verify_spec`: delete/recreate substitution
(dev/ino change), in-place content swap (digest change) and path
mismatch are each refused.

## 6. Controller request schema delta (IR-002) — OBSERVED_FACT

The controller request is now a CLAIM with EXACTLY four allowed fields:

```
{ attempt_id, controller_starttime, env_claims, payload_kind }
```

`harness_root`, `boundary_child`, `evidence_src`, `target_src`,
`auditor_output_src`, `codex_home`, `config_path`, `identity_version`,
`identity_sha256`, `identity_exe_path`, `profile_name`, `model_name`,
`credential_adapter`, `root`, `manifest_id` and `controller_pid` are
REMOVED from the protocol entirely.  Supplying any of them is
`UNKNOWN_CLAIM_FIELD:<names>` → `TERMINAL_PREEXEC_STOP` (each of the 16
former fields is covered by a parametrized adversarial test).  No
authority value is ever constructed from a request field: binds,
executable identity, config, child paths and adapter all come from the
spec.  `payload_kind` and `attempt_id` claims must match the spec/grant
exactly.

## 7. Harness-code identity mechanism (IR-002 / §9) — OBSERVED_FACT

The trusted executable byte set (`HARNESS_EXEC_RELPATHS`: the 19 `qh/`
modules + the two in-boundary payload fixtures; tests/docs/data are
deliberately excluded) is pinned by a recursive digest in the spec.  At
launch, AFTER `TRUSTED_SPEC_VERIFY` passes, the supervisor snapshots the
VERIFIED bytes into process-bound memfds; the boundary materializes them
via bwrap `--perms 0644 --ro-bind-data <fd> /opt/qh/<relpath>` (and the
rendered config at the boundary-private CODEX_HOME, the verified
provider executable at `/run-qh/trusted-provider-exe` mode 0755).  The
boundary performs **NO host harness-root bind at all** — the
controller-selected `harness_root` defect is closed mechanically: no
host-path code executes inside the protected launch, and bwrap copies
the fd bytes at sandbox setup so later host-side writes cannot reach the
materialized files.  `boundary_child` additionally re-hashes every
materialized code/config file against the spec-provided SHA-256 before
payload exec (`trusted_bytes` records), so a swap racing the pre-launch
window fails closed INSIDE the boundary.  Code identity is content
identity: byte-identical recreation substitutes nothing (tested).

## 8. Evidence / target / output binding (§10) — OBSERVED_FACT

Evidence and target are spec-bound RO sources; auditor-output is the
ONE rw bind and its host source is spec-bound (role `rw`).  For every
security-critical directory source: identity canonicalized (realpath +
dev + ino + recursive digest) at authoring; verified at launch
(`verify_spec` — delete/recreate and content drift refused); and the
tree digest is re-verified INSIDE the boundary over the mounted tree
before payload exec (the digest is deliberately path-independent for
this).  Check-to-use residual: a same-UID in-place write racing between
the in-child verification and payload exec is not atomically prevented
for DIRECTORY sources — bounded to the supervisor's verified snapshot
for all CODE bytes (memfd-immutable), detected at both verification
points for content, and object substitution is impossible (dev/ino);
recorded as residual R-3 (§23).  No writable host exposure was
broadened (auditor-output remains the single rw bind).

## 9. Executable identity binding / Codex identity pin (§11) — OBSERVED_FACT

The controller can no longer supply BOTH the executable and its hash:
neither field exists in the request.  The spec provides the expected
executable identity; the supervisor (a) verifies the ACTUAL bytes'
SHA-256 + object identity at `TRUSTED_SPEC_VERIFY`, (b) re-verifies at
profile freeze (`verify_codex_identity`), and (c) launches only the
VERIFIED byte snapshot (memfd-materialized trusted exe).  Mandatory
controls tested: arbitrary executable E + SHA256(E) as claims ⇒ REFUSED
(`UNKNOWN_CLAIM_FIELD`); trusted executable changed after spec creation
⇒ `TRUSTED_SPEC_VERIFY_FAIL:…CODEX_EXE…` (terminal).  The generated
config digest is likewise spec-bound: the supervisor re-renders the
profile from spec parameters and refuses any mismatch
(`PROFILE_CONFIG_DIGEST_MISMATCH`), so neither the config path nor its
content is request-controlled.

## 10. Trigger authentication / binding (§12) — OBSERVED_FACT

The one allowed trigger is bound to the authorized controller instance
and attempt through the C-1-consistent mechanism: the supervisor serves
exactly one connection; `SO_PEERCRED` supplies the peer pid (never
request-supplied); the ACTUAL `/proc/<pid>/environ` must carry the
spec-bound `CLAUDE_CONFIG_DIR` (C4′); pid-reuse is defended by
starttime binding; and the expected authorization state (attempt, spec,
custody) originates from the trusted root, never from the request.  A
competing same-UID process can burn the single mint/request (DoS) but
cannot obtain a provider-capable launch: the boundary, custody bytes
and spec values are all root-authoritative (tests §18.A/C, §15).

## 11. Yama / test-hook remediation (IR-003) — OBSERVED_FACT

* the operational CLI exposes NO `--yama-override` and NO `--fault` of
  any kind: `_reject_forbidden_flags` refuses them (exit 2,
  `PRODUCTION_CLI_REFUSED`) on every subcommand BEFORE parsing, even
  disguised as `--yama-override=0`;
* `SupervisorPolicy` structurally contains ONLY verification seams
  (`env_reader`, `stat_reader`, `walker`, `set_dumpable`,
  `require_custody`, `boundary_launcher`) — no fault/yama/override
  knob exists (dataclass-fields test);
* `Supervisor.startup()` and `AuthorityRoot.startup()` always read the
  REAL kernel knob (`read_yama_ptrace_scope`); a mechanically simulated
  Yama < 1 FAILS CLOSED on the production entrypoint (monkeypatched
  REAL-reader seam in tests — no CLI/test hook can convert it to PASS);
* the parser option-tree is structurally asserted to contain no
  fault/yama/override/bypass/force option on any subcommand;
* deterministic test fault injection now lives ONLY in the test suite
  (monkeypatched readers; an in-process launcher DI seam that can only
  ever return FAILING real-shape gate records, never convert a failure
  to a pass); every production trust decision is computed from real
  values.

## 12. Credential adapters (§14) — OBSERVED_FACT

Provider-capable CHILD launches gated by AUCDEV-023 (established from
the frozen evidence): Auditor-B / Codex ChatGPT-OAuth (`codex exec` with
`auth_mode=chatgpt`) and Auditor-A / Claude Code first-party OAuth
(dedicated `CLAUDE_CONFIG_DIR`).  Concrete adapters implemented in
`qh/adapters.py` against SYNTHETIC inert bytes only:

* `codex_chatgpt_oauth_v1` — evidence: Campaign-2 preflight correction
  (role-B staging census EXACTLY `auth.json` + minimal `config.toml`;
  CODEX_HOME must be WRITABLE at init —
  `B_ATTEMPT1_LOCAL_INIT_FAILURE_READONLY_CODEX_HOME`) and the accepted
  G-2 closure (auth.json is the required runtime interface; NEVER a
  model-command permission-profile entry).  Materializes custody bytes
  as `auth.json` mode 0600 inside the boundary-private
  `CODEX_HOME=/run-qh/codex-home` (composed with the rendered
  config.toml from the verified snapshot), removed with the namespace;
* `claude_firstparty_oauth_v1` — evidence: Campaign-2 static preflight
  parity closure (in a fresh dedicated `CLAUDE_CONFIG_DIR` the
  credential surface is `.credentials.json` ALONE, `claudeAiOauth` key
  shape, mode 0600, no settings/projects/plugins/skills).  Materializes
  custody bytes as `.credentials.json` mode 0600 inside the
  boundary-private `CLAUDE_CONFIG_DIR=/run-qh/claude-config`;
* `synthetic_inert_v1` — the inert rehearsal adapter (GATE-W/gate
  launches keep the ACCEPTED matrix exactly: custody verified at the
  inert path; `auth.json` ABSENT from the rehearsal CODEX_HOME).

Adapter contract: bytes arrive only from the authority-root custody
channel; never persisted as host plaintext; materialized only inside
the supervised child boundary at the exact provider/runtime path;
restrictive mode as defense-in-depth; unavailable to model-generated
commands per the accepted policy (the generated profile contains NO
credential-surface read entry — asserted inside the protected payload);
removed with the child namespace; never logged/hashed/reported
(labels + lengths only); identified and bound in the trusted launch
spec (unknown adapter id ⇒ `CREDENTIAL_ADAPTER_INVALID` terminal).
No undocumented credential format was inferred; no real credential was
read or contacted.  Provider roles beyond the two above are not
established by existing evidence and remain explicit blockers
(`UNESTABLISHED_PROVIDER_ROLES`).

## 13. Ambient credential absence (§15) — OBSERVED_FACT (structural custody proof, zero provider contact)

Proven with synthetic fixtures (`tests/test_provider_adapters.py`):
controller process environment carries no provider credential;
controller-visible config tree contains none; the authority root's
custody memfd is unreachable through same-UID `/proc` (fd list AND
direct fd opens denied — non-dumpable); the legitimate root refuses to
materialize credential bytes outside the trusted bound launch (single
mint; every tampered request is terminal); a controller-created fake
root never causes the legitimate bytes to appear anywhere (full-tree
value scan); the protected child receives the synthetic material only
through the trusted adapter (target/length/mode asserted in-payload);
after teardown the material is absent from every persistent ordinary
file (full-tree scans for the unique synthetic values = zero hits;
`auth.json`/`.credentials.json` nonexistent on the host side).

## 14. IR-001 mapping (AUCDEV023-CR-IMPL-001) — CLOSED at implementation/self-test strength

Every observed defect fact from the readback is remediated:

| Readback observed fact | Remediation |
|---|---|
| `qh.cli mint` needs no external capability | public mint subcommand REMOVED; only the root mints |
| caller supplies attempt/root/manifest/operator-state | mint request carries only the attempt-id claim; root/manifest/state are root-bound; wrong attempt refused |
| caller-selected ledger is the duplicate registry | duplicate registry is root memory + observability ledger (files grant nothing) |
| same-UID process can create its own scope/manifest/state/grant | it can — and obtains only a powerless imitation (no operator custody/spec); production-valid mint for the legitimate attempt is refused |
| `--operator-pid` optional + caller-supplied | flag REMOVED; ppid==minting-root enforced from inside the grant; PDEATHSIG binds supervisor lifetime to the root |
| grant secret never authenticates anything | unchanged by design (it never claimed to); authority is the root's process-bound spec+custody capability |

Adversarial evidence: §18 A–F all covered by `tests/test_rootauth.py`
(A: public-mint removal + wrong-attempt refusal + powerless imitation;
B: fake root lacks legitimate custody/campaign capability — value-scan
proofs; C: no second mint after terminal stop; D: state deletion
restores nothing; E: new attempt only after new operator/root
authorization; F: root SIGKILL = denial only).

## 15. IR-002 mapping (AUCDEV023-CR-IMPL-002) — CLOSED at implementation/self-test strength

Readback consequences A/B/C (controller-chosen RW bind;
controller-chosen harness_root executed as the trusted boundary child;
self-asserted executable identity) are each mechanically closed
(§§6–9).  Adversarial evidence: 16-field parametrized claim-refusal
matrix + the three mandatory controls (arbitrary exe+sha ⇒ REFUSED;
arbitrary RW dir ⇒ NOT BOUND — attacker dir verified empty; arbitrary
harness_root ⇒ NOT EXECUTED) + post-authorization real-drift refusals
(codex exe bytes/recreate, evidence content/recreate, target recreate,
auditor-output recreate, harness code, config digest, attempt root,
boundary-child set membership, spec-id transit mismatch, wrong adapter,
wrong attempt, payload-kind mismatch) — `tests/test_trusted_claims.py`
+ `tests/test_trusted_spec.py` (27 + 17 tests).

## 16. IR-003 mapping (AUCDEV023-CR-IMPL-003) — CLOSED at implementation/self-test strength

`--yama-override` and the whole `--fault` surface are gone from the
operational CLI; both root and supervisor always read the real kernel
knob; simulated real-Yama<1 fails closed on the production entrypoint;
no CLI flag can alter any production trust decision (parser-tree
structural proof).  Regression proving the production argv parser
rejects `--yama-override`: `tests/test_production_surface.py`
(7 tests).  The prior suite's flag-based fault injections were replaced
by real conditions or test-only seams (§11).

## 17. Provider integration status (§14)

```
PROVIDER_CREDENTIAL_CUSTODY_INTEGRATION
  = SYNTHETIC_CONCRETE_ADAPTERS_IMPLEMENTED
    (codex_chatgpt_oauth_v1, claude_firstparty_oauth_v1)
  + synthetic_inert_v1 rehearsal adapter
  - synthetic-only: no real credential read/parsed/contacted
  - unestablished provider roles: explicit blockers, none invented
```

This closes as much of the held blocker as existing non-secret evidence
mechanically supports.  NOT claimed: campaign-ready REAL credential
integration (operator-side custody of live credentials, real provider
runtimes) — that remains gated on separately authorized campaign
preparation and the independent harness audit.

## 18. Integrated composition (§22) — OBSERVED_FACT

The mandated order is proven from ONE integrated attempt's observability
ledger (`tests/test_compose.py`): `ROOT_UP` → `SPEC_BOUND` →
`ROOT_CUSTODY_ESTABLISHED` (all BEFORE `REQUEST_RECEIVED`) →
`CONTROLLER_BINDING_ESTABLISHED` → `C4P_RESULT` → `TRUSTED_SPEC_VERIFY`
→ `AUTHORITY_BOUND` → `CREDENTIAL_ADAPTER_BOUND` →
`CUSTODY_ESTABLISHED` → `TRUSTED_BYTES_SNAPSHOTTED` → `NOEGRESS_GATE` →
`PROFILE_FROZEN` → `GATEW_RESULT` → `CONSUMED_FOR_LAUNCH` → `LAUNCHED`
→ `TERMINAL`; marker produced; engagement accounting untouched
(before == after); reuse refused; step 13 (fresh controller-created
imitation cannot launch with legitimate custody/spec) proven in the
demo and §18.B tests.  `compose-demo` exercises the same flow
(happy ok / reuse refused / engagements untouched / imitation
powerless).  Provider/model/auditor execution = ZERO (the pinned
"codex" executable is a synthetic fixture; no `codex`/provider process
is ever launched — asserted by test).

## 19. Tests and validation — FIRST results (reruns recorded separately)

Environment: Python 3.11.15 + pytest 9.1.1 via `uv run --no-project
--with pytest`; bwrap 0.12.0; Yama ptrace_scope = 1; unprivileged
user+net namespaces available.

- Complete remediated harness suite: **158/158 PASSED — FIRST complete
  run of the final set**
  (`test-outputs/harness-suite-FIRSTRUN-REMEDIATED.txt`).
  Development iterations BEFORE the final set, each recorded and
  resolved (nothing rerun away silently):
  - `test-outputs/rootauth-FIRSTRUN.txt` — 9 failed / 3 passed
    (rootauth↔authority circular import; missing CLI `root` command);
  - `rootauth-RERUN2.txt` — 6 failed (populated-memfd misclassified as
    an ordinary file by `_fd_kind`; Python `oct()` format rejected by
    bwrap `--perms`; ROOT_PID reason not surfaced);
  - `rootauth-RERUN3.txt` — 5 failed (`--perms` octal string;
    F_GET_SEALS succeeds on ordinary files on this kernel — memfd
    discrimination moved to the `/proc/self/fd` link target);
  - `rootauth-RERUN4.txt` — 1 failed (inter-attempt GATE-W mkdir
    state — made idempotent);
  - `rootauth-RERUN5.txt` — 1 failed (leaked supervisor socket
    collision → `PR_SET_PDEATHSIG` lifetime binding added);
  - `trusted-claims-FIRSTRUN.txt` — 4 failed (test-flow re-authoring
    bug; `PolicyDrift` uncaught in the snapshot path);
  - `trusted-claims-RERUN2/3.txt` — 2 then 0 failed;
  - `provider-adapters-FIRSTRUN.txt` — 2 failed (claude-role rehearsal
    missing the generic CODEX_HOME config — config target made
    role-independent); `RERUN2.txt` — 0 failed;
  - pre-existing suite against remediated code: first run 32 failed /
    52 passed (old interfaces); all rewritten/updated files GREEN
    thereafter.
- Targeted product non-regression (read-only):
  `skill/tests/test_codex_sandbox.py` + `skill/tests/test_codex_runner_mock.py`:
  **34/34 passed (first run)**.
- Product FULL deterministic suite `skill/tests`: **686/686 + 99
  subtests PASSED** (first run this session; the previously recorded
  host Node PATH drift condition did not reproduce — PATH-ordering
  dependent external condition, see §21; nothing was modified to make
  it pass).
- `git diff --check`: clean (worktree).
- Secret-pattern scan over every changed/new ordinary file: zero hits
  (no key/token/PEP/JWT/`sk-`/AKIA/xox/ghp patterns; adapter
  `auth.json`/`.credentials.json` references are documentation of the
  synthetic interfaces only).
- Zero-provider: EXTERNAL_PROVIDER_CONTACT = ZERO, MODEL_INFERENCE =
  ZERO, CAMPAIGN_AUDITOR_ENGAGEMENT = ZERO (by construction: no
  provider binary is referenced or executed anywhere in the harness).

## 20. Product / historical non-interference (§24) — OBSERVED_FACT

`skill/` tree identity UNCHANGED before/after:
`git rev-parse 2e53ad5:skill` == `git rev-parse <result>:skill` ==
`c792933a862d9a5434681a88d183470dd8b15d2f` (verified post-commit).
NOT modified: `skill/**`, `skill/tests/**`, `skill/schemas/**`,
`skill/PUBLIC-CONTRACT.md`, `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md`,
`AUCDEV-QUALIFICATION-HISTORY.md`, historical AUCDEV-010 reports,
frozen Campaign-2 artifacts (changed-path confinement proves it
mechanically).  Campaign-2 remains TERMINAL (§25).  No old verdict
transfers (§26).

## 21. Product full-suite result (recorded verbatim)

Targeted: 34/34 (first run).  Full suite: recorded in
`test-outputs/product-fullsuite-REMEDIATED.txt` — **686/686 + 99
subtests PASSED** in this session.  The previously recorded
HOST_NODE_PATH_DRIFT condition did NOT reproduce in this session:
`~/.local/bin/node` still symlinks to the Hermes node, but this
session's PATH orders the NVM node directory before `.local/bin`, so
host `shutil.which("node")` resolves the NVM v24.14.0 node and the
tier4 f2 expectation matches.  The condition therefore remains
PATH-ORDERING-DEPENDENT and can recur in sessions where `.local/bin`
precedes NVM — recorded honestly as the known external condition
(HOST_NODE_PATH_DRIFT, EXTERNAL_CONDITION, PRE-EXISTING, unrelated to
this remediation which modifies no tracked `skill/` file; the product
test was NOT modified).

## 22. Held accepted mechanics — non-regression (§17) — OBSERVED_FACT

Preserved (surgical interface changes only where a finding required
it): C-1 bootstrap/provenance and C4′ actual-process verification
(untouched); attempt state-machine absorbing PREEXEC stop (untouched);
`PR_SET_DUMPABLE=0` (root + supervisor); Yama >= 1 REAL production gate
(now override-free); systemd-resolved/DBus masking and the hard
no-egress contract incl. ZERO inherited socket FDs (untouched; live
regressions still pass); named restricted Codex profile semantics and
generation (unchanged renderer; digest now spec-bound); NO `--add-dir`;
NO CLI `-s workspace-write`; one model-write role only; GATE-W semantic
matrix unchanged (17 ops; CODEX_HOME path parameterized to the
boundary-private home, matrix semantics identical; inert custody target
preserved); campaign engagement accounting separation (asserted);
skill/product separation (proven).  G-1/G-2 design research was NOT
reopened.

## 23. Residuals and blockers (explicit)

1. **R-1 (HOST CONDITION, recorded — NOT silently downgraded):** the
   four-seal memfd representation is mechanically unavailable on the
   demonstrated host class (§4.1).  Strict mode fails closed on such
   hosts; the default reconciles to the accepted G-1 non-dumpable
   memory-only posture with `seal_status=unavailable_kernel` recorded.
   A seal-capable host gets the sealed representation through the same
   code path.
2. **R-2 (completeness):** provider adapters are SYNTHETIC-concrete
   only; real-credential campaign integration (live operator custody,
   real provider runtimes) remains gated on separately authorized
   campaign preparation + the independent harness audit.  No
   campaign-readiness claim is made beyond the synthetic boundary.
3. **R-3 (bounded race):** for DIRECTORY sources (evidence/target), a
   same-UID in-place content write racing between the in-child digest
   verification and payload exec is detected at no earlier-than-child
   point but not atomically prevented; object substitution is
   impossible (dev/ino); CODE bytes are fully memfd-immutable.  Same-UID
   in-place tampering of RO-bound evidence DURING payload execution
   remains an inherent same-UID residual (documented threat model).
4. **R-4 (residual, carried):** Codex-internal Landlock enforcement of
   the generated profile is NOT independently verified without running
   Codex (unchanged residual; outer-boundary + profile-content proofs
   only).
5. **R-5 (environmental):** the pre-existing host Node PATH drift
   condition (§21) did not reproduce in this session (PATH ordering
   resolved the NVM node first; the Hermes symlink remains in place, so
   the condition is order-dependent and can recur); honestly recorded,
   not modified away.

No STOP condition of remediation §6/§9/§14/§25 was triggered: the
sealed-state host condition is handled exactly as §6 prescribes (strict
fail-closed + recorded reconciliation, not a silent downgrade);
immutable trusted-bytes execution IS established (memfd snapshot);
every evidence-established provider role has a concrete adapter and no
further role was invented.

## 24. Governing result

```
IR-001  mechanically closed   (authority root outside the controller;
                               adversarial §18 A–F evidence)
IR-002  mechanically closed   (trusted launch spec + claim-only schema +
                               immutable trusted bytes + identity binding;
                               §19 matrix evidence)
IR-003  mechanically closed   (no production override anywhere; §20
                               evidence)
provider adapters: synthetic-concrete for every evidence-established
                               role; no remaining campaign-reliance
                               blocker within the synthetic boundary
residuals: R-1..R-5 recorded (R-1 is the demonstrated host sealing
           condition reconciled per §6, fail-closed in strict mode)
```

Recommended (IMPLEMENTER position, NOT an independent verdict):

```
AUCDEV023_TRUST_ANCHOR_REMEDIATION_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK
```

AUCDEV-023 remains **P1 / READY** (NOT DONE).  Independent harness
audit remains **DEFERRED_PENDING_CONTROL_ROOM_READBACK** of THIS
remediation, then mandatory on the exact remediated SHA.  Do NOT
transfer any verdict from the base implementation to this SHA.

## 25. Campaign / qualification held state (preserved EXACTLY)

```
AUDITOR_A_AUTHORITY            = CONSUMED_CLOSED
AUDITOR_B_AUTHORITY            = CONSUMED_CLOSED
MODEL_ENGAGEMENTS_AUTHORIZED   = 2
MODEL_ENGAGEMENTS_USED         = 2
FIRST_PASS_A                   = PRESENT / FROZEN
FIRST_PASS_B                   = ABSENT
FIRST_PASS_BARRIER             = CLOSED
NO_CONFORMING_BLIND_FIRST_PASS_SET
CAMPAIGNS                      = 2 OF MAX 2
CAMPAIGN_3                     = NOT AUTHORIZED / DOES NOT EXIST
AUCDEV-010                     = P1 / BLOCKED
QUALIFICATION                  = NONE
INSTALLATION                   = NONE
```

No historical verdict changes.

## 26. Required lifecycle

```
THIS remediation publication
→ NEXT (EXACTLY ONE): INDEPENDENT CONTROL ROOM READBACK OF THIS
  TRUST-ANCHOR AND LAUNCH-SPEC BINDING REMEDIATION
→ then INDEPENDENT HARNESS AUDIT on the exact remediated SHA
→ only then consider any future qualification package/campaign
```

This session did NOT self-audit, did NOT qualify, did NOT install, and
did NOT perform the independent audit.

Result: `AUCDEV_023_TRUST_ANCHOR_LAUNCH_SPEC_REMEDIATION_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
