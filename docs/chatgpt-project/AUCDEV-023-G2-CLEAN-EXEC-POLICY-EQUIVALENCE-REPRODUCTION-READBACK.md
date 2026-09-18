# AUCDEV-023 — G-2 Clean Exec-Policy Equivalence Reproduction: Control Room Readback and OPEN→READY Readiness Transition (Canonical Record)

| Field | Value |
|---|---|
| Session class | RECORD-ONLY, APPEND-ONLY, ZERO-MODEL GOVERNANCE-PUBLICATION IMPLEMENTER ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room, NOT a qualification authority, NOT an installation authority, NOT remediation implementation; NO probe execution; NO product/harness implementation; NO auditor/model/provider execution; NO qualification; NO installation; NO Campaign-2 recovery; NO Campaign-3; ZERO provider/model/frontier calls by this publication session |
| Date | 2026-09-18 (Europe/Istanbul) |
| Operator publication authority | Control Room tasking (2026-09-18) authorizes ONLY this publication recording (1) Control Room acceptance of the clean G-2 equivalence reproduction, (2) G-2 closure at DESIGN/PROBE strength, (3) satisfaction of readiness gaps G-1 and G-2, and (4) the AUCDEV-023 transition P1 / OPEN → P1 / READY. It does NOT authorize remediation implementation or any further execution. |
| Exact governance base | `2b70592486d510d02dca552a1aebd7b382fd7556` (the AUCDEV-023 G-2 exact exec-policy probe readback publication commit; tree `98525d8be8835bab85faf8f61f29519e8a2173b2`; sole parent `571bb2459ff583d71df38ac172679246972de9a9`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this publication's bootstrap and re-resolved EXACT immediately before its single fast-forward push; THIS publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Subject investigation | AUCDEV-023 G-2 clean exec-policy-equivalence reproduction (2026-09-18, zero-model, hard-no-egress, exactly ONE authorized `codex exec` policy-introspection invocation; zero canonical repository mutation) — source handoff `AUCDEV-023-G2-CLEAN-EXEC-REPRO-handoff-20260918.tar.gz` |
| Qualification/installation | readiness BLOCKED / qualification NONE / installation NONE (unchanged) |

## 1. Source clean-reproduction handoff — integrity VERIFIED (read-only)

Control Room verification independently re-executed read-only by THIS
publication session before any mutation (identical results):

- outer SHA-256 `cd436d42457155a21b75eeebeab3c2b2a37de8395c2aecb415612cc4e77dc653`
- **414863 bytes**
- member census: **50 total = 38 regular files + 12 directories**
- unsafe/traversal 0; duplicates 0; symlink/hardlink/special 0
- exactly ONE `SHA256SUMS`
- the `SHA256SUMS` contains **37 payload checksum entries**
- checksum verification result: **37/37 PASS**

The archive was inspected in an isolated temporary location, its content NOT
executed, and NO credential, auth-token contents, Auditor-A substantive
material or Auditor-B substantive runtime material is republished here (the
handoff `CODEX_HOME` fixture carries only the investigation's synthetic INERT
auth marker; its contents are not disclosed in this record).

Probe-session self-declarations were accepted only where mechanically
supported by the handoff evidence, and the decisive equivalence and no-egress
evidence was INDEPENDENTLY RECOMPUTED by this readback session from the
handoff artifacts (§6) rather than trusted from the probe's own tooling.

## 2. Control Room readback disposition (recorded verbatim)

```
AUCDEV_023_G2_CLEAN_EXEC_POLICY_EQUIVALENCE_READBACK_ACCEPTED
/ HANDOFF_INTEGRITY_VERIFIED_37_OF_37
/ EXACT_CODEX_IDENTITY_VERIFIED
/ HARD_NO_EGRESS_ACCEPTED
/ EXACTLY_ONE_AUTHORIZED_EXEC_INTROSPECTION_VERIFIED
/ EXEC_DERIVED_POLICY_CAPTURE_VERIFIED
/ ACCEPTED_BASELINE_PROVENANCE_CROSSCHECKED
/ NORMALIZED_POLICY_BYTE_EQUAL
/ SEMANTIC_ENTRY_SET_EQUAL
/ EXTERNAL_PROVIDER_CONTACT_ZERO
/ MODEL_INFERENCE_ZERO
/ CAMPAIGN_ENGAGEMENT_ZERO
/ G2_CLOSED_AT_DESIGN_PROBE_STRENGTH
/ AUCDEV023_READINESS_CRITERIA_SATISFIED
/ OPEN_TO_READY_TRANSITION_SUPPORTED
/ CAMPAIGN2_TERMINAL_UNCHANGED
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
```

## 3. Independently accepted G-2 evidence

Accepted:

```
G2_CLEAN_EQUIVALENCE_REPRODUCTION = PASS
```

Exact Codex identity (verified at task start AND at the pre-launch identity
gate immediately before the single invocation):

```
codex-cli 0.154.0
native SHA-256: 3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022
```

The clean reproduction used the already-accepted candidate:

- primary workspace = `/auditor-output` role (disposable auditor-output
  equivalent workspace fixture);
- NO `--add-dir`;
- NO CLI `-s workspace-write`;
- named restricted permission profile from disposable `CODEX_HOME`.

The candidate policy showed NO evidence drift beyond the authorized
disposable fixture-path substitution: this readback session re-diffed the
reproduction `config.toml` against the prior accepted demonstrated fixture
config byte-for-byte — differences are EXACTLY the four fixture-path lines
(workspace_roots key; `out=write`; `evidence=read`; projects trust key); every
policy-semantic byte is identical
(`NO_EVIDENCE_DRIFT — FIXTURE_PATH_SUBSTITUTION_ONLY`).

Record precision (non-blocking): the probe report §3 parenthetically cites
prior-report SHA `05d67741…` for the prior named-profile fixture config; the
prior report §11 value `05d67741…` is actually the prior AUTH-fixture config
SHA. The mechanically authoritative drift-diff artifact records the correct
prior named-profile fixture config SHA `a34b4224…`, which this readback
independently re-verified against the prior probe workspace bytes
(byte-identical). Classification: `COMPLETENESS_LIMITATION / RECORD_PRECISION /
PRIOR_CONFIG_SHA_CITATION_SLIP / NON_BLOCKING`; the historical handoff is NOT
rewritten; the drift conclusion is unaffected.

## 4. Hard no-egress readback — ACCEPTED (the ACTUAL authorized v2 invocation environment)

Before the single Codex invocation, the wrapper mechanically established:

- fresh user/network/mount namespaces
  (net `net:[4026535213]` vs host `net:[4026531833]`;
  user `user:[4026534880]`; mount `mnt:[4026534883]`);
- no IPv4/IPv6 usable address (`addr4_count=0`; only the unconditional
  multicast/local IPv6 stub routes present in every netns);
- no usable route (main/all route tables empty);
- loopback DOWN (`lo` state DOWN; `127.0.0.53:53` → ENETUNREACH);
- DNS tests **3/3 failed** (`api.openai.com`, `chatgpt.com`,
  `one.one.one.one` → `[Errno -3]` name-resolution failure);
- external TCP tests **4/4 failed** (`1.1.1.1:443`, `1.1.1.1:53`,
  `8.8.8.8:443` → ENETUNREACH; `api.openai.com:443` → DNS failure);
- inherited socket descriptors = **0** (fd inventory: `/dev/null`, console,
  transient `/proc` read only);
- systemd-resolved AF_UNIX path masked (`/run/systemd/resolve` bind-masked
  empty in the private mount namespace);
- D-Bus path masked (`/run/dbus` bind-masked empty);
- no foreign network-namespace descriptor inherited (socket fd count 0);
  `setns()` back to the host netns would require `CAP_SYS_ADMIN` in the
  initial user namespace, which the process does not hold.

The process descendants remained inside the same isolated network namespace
(every poll-second sample of the invocation tree — node shim and native codex
— carried `ns/net = net:[4026535213]`; postflight `/proc/net/tcp` inside the
namespace contains only the header line: no socket was ever established).

Postflight network tests remained denied (postflight DNS and TCP still
failed as required).

Exactly ONE attempted provider DNS resolution occurred AFTER local policy
derivation (stderr: `failed to lookup address information: Try again, url:
wss://api.openai.com/v1/responses`), and it FAILED LOCALLY inside the hard
no-egress namespace. No external provider connection ever succeeded.

Therefore, preserved EXACTLY:

```
EXTERNAL_PROVIDER_CONTACT = ZERO
MODEL_INFERENCE = ZERO
CAMPAIGN_AUDITOR_ENGAGEMENT = ZERO
```

This readback does NOT misclassify the isolated invocation as a consumed
Auditor-B engagement or as model inference (the rollout contains NO
agent_message/agent_reasoning/token_count records; `tokens_used=0`; no
model-generated content exists in any captured artifact).

## 5. Preflight v1 finding — recorded accurately

The FIRST wrapper execution (06:59:48Z, under `unshare -rn` with the mount
namespace still shared with the host):

- **STOPPED BEFORE CODEX** — the gate evaluated FAIL and exited before any
  codex launch; **authorized Codex invocation count at that point = ZERO**;
- discovered that a bare network namespace was insufficient on this host:
  host `systemd-resolved` remained reachable over its AF_UNIX socket
  (`/run/systemd/resolve/io.systemd.resolve`), and all three DNS test names
  RESOLVED inside the netns (12 addresses each) despite 0 interfaces /
  0 addresses / 0 routes and TCP ENETUNREACH everywhere;
- the first wrapper also exposed an **inherited socket descriptor on fd 0**
  (`/proc/self/fd/0 -> socket:[…]`; `inherited_socket_fd_count = 1`);
- **no Codex invocation occurred under that state.**

The subsequent hardening BEFORE the authorized invocation included:

- private mount namespace;
- masking `/run/systemd/resolve`;
- masking `/run/dbus`;
- stdin `/dev/null`;
- inherited socket descriptor count = **ZERO**.

Classification:

```
HARNESS/PROTOCOL
/ NO_EGRESS_PREFLIGHT
/ SYSTEMD_RESOLVED_AF_UNIX_ESCAPE_SURFACE
```

and implementation requirement:

```
HARD_NO_EGRESS_GATE_MUST_REQUIRE_ZERO_INHERITED_SOCKET_FDS
```

This is NOT a G-2 closure blocker because the actual single authorized Codex
invocation occurred only AFTER the hardened v2 preflight passed. Both the
masking requirement and the zero-inherited-socket-FD requirement MUST be
carried into future implementation acceptance criteria (§9, §11).

## 6. Exec-policy equivalence — mechanically established and independently recomputed

Accepted as mechanically established (and independently RECOMPUTED by THIS
readback session from the handoff's own session-DB copy, rollout copy and
baseline artifacts, using this session's own verifier — the probe's tooling
was NOT executed):

- session DB `threads.sandbox_policy` and rollout
  `turn_context.permission_profile` were mutually byte-identical for the
  derived effective restricted profile;
- the clean-reproduction derived profile was independently compared with the
  previously accepted v6 named-profile baseline;
- the accepted baseline used for comparison was independently
  provenance-crosschecked against the prior AUCDEV-023 G-2 probe handoff
  (outer SHA-256 `3c51f7c4…`, 795319 B, the exact archive accepted by the
  prior readback): the baseline policy JSON is byte-equal (canonical) to the
  prior handoff's `v6-named-profile-policy.json` member, and the carried
  accepted fixture config is byte-identical to the prior probe workspace's
  demonstrated fixture.

Normalized canonical policy SHA-256 on BOTH sides (recomputed independently
by this readback, matching the probe's recorded values):

```
4f00aec1bdf285ce91ead6f56ef9f4b919037770447e92ce028a2b017a745ba1
```

Results:

```
NORMALIZED_CANONICAL_BYTE_EQUAL = TRUE
SEMANTIC_ENTRY_SET_EQUAL = TRUE
only_in_clean_reproduction = EMPTY
only_in_accepted_baseline = EMPTY
```

Compared dimensions (all EQUAL):

- write roots: exactly ONE role — `workspace` (auditor-output);
- root-wide read entry (`/`): ABSENT;
- network: `restricted`;
- profile type: `managed` / `restricted`;
- `CODEX_HOME`/auth: NOT exposed through the model-command permission
  profile; only the documented runtime-generated arg0-helper READ entry
  exists (`auth.json` is never an entry — no credential exposure path);
- `turn_context.workspace_roots` count = exactly ONE, with `cwd` equal to
  that primary workspace root.

Therefore:

```
G2_EXEC_POLICY_EQUIVALENCE = ESTABLISHED
```

The decisive equivalence evidence was obtained through a
Control-Room-authorized method inside the hard no-egress environment with
exactly ONE authorized exec introspection invocation — closing the
execution-scope nonconformance that blocked the prior probe's closure
(`ISOLATED_CODEX_EXEC_WITH_PROMPT_NONCONFORMANCE` is NOT repeated here: the
v1 fail-closed preflight stop had ZERO codex invocations and the hardened v2
gate PASSED before the single authorized invocation).

## 7. Prior accepted G-2 evidence — remains held without rerunning

Carried forward unchanged (no rerun; no full matrix repeat was required
because exact binary identity and candidate policy had no material drift):

- exact Codex identity;
- primary-workspace design;
- named restricted-profile semantics;
- repaired g2p05;
- dynamic shipped-zsh matrix: 20 semantic operations = 10 ALLOWED /
  10 REFUSED;
- repaired static payload matrix: 30 semantic operations = 15 ALLOWED /
  15 REFUSED;
- outer + inner composition;
- evidence integrity;
- target/host denial;
- no unbounded persistent model-write surface.

## 8. G-2 governing status

```
G2 = CLOSED_AT_DESIGN_PROBE_STRENGTH
```

This is a readiness/design closure. It is NOT:

- remediation implementation completion;
- package qualification;
- candidate qualification;
- installation;
- authorization to recover Campaign-2.

Implementation residuals/invariants carried forward:

- **A.** hard no-egress environment must mask host resolver/DBus AF_UNIX
  paths as required by the demonstrated host class;
- **B.** launch gate must mechanically require inherited socket FD count =
  ZERO;
- **C.** arg0 helper READ entry is accepted as a bounded non-credential
  residual;
- **D.** cosmetic `sandbox: workspace-write` banner text is NOT the
  authoritative permission representation; the managed permission profile is;
- **E.** inner-root tmpfs scaffold is an accepted namespace-local ephemeral
  residual, not a persistent host-backed model-write root;
- **F.** Linux-only assumptions remain explicit.

## 9. G-1 governing status — carried forward unchanged

```
G1 = DESIGN_PROBE_CLOSURE_ACCEPTED
```

Mandatory future implementation invariant:

```
CREDENTIAL_CUSTODY_IS_REQUIRED_FOR_G1_ENFORCEMENT
```

Real provider credential integration has NOT yet been implemented.

Also preserved — the demonstrated Linux prelaunch requirement:

```
Yama ptrace_scope >= 1
```

(observed host value 1, before and after the reproduction).

## 10. AUCDEV-023 readiness decision — OPEN → READY

Both readiness gaps are now accepted at design/probe strength:

```
G-1 = CLOSED / ACCEPTED FOR READINESS
G-2 = CLOSED / ACCEPTED FOR READINESS
```

Therefore this publication records the governance transition:

```
AUCDEV-023:  P1 / OPEN  →  P1 / READY
Classification: READINESS_CRITERIA_SATISFIED
```

This transition means: the remediation objective is now bounded enough for a
separately authorized implementation task. It DOES NOT itself authorize
implementation. **No implementation may begin from this publication alone.**

## 11. Readiness acceptance criteria for future implementation

Carried into the future implementation brief as held invariants:

- **C-1:** pre-controller controller-scope provenance and C4′ actual
  process-binding evidence; do not regress blindness/confinement.
- **C-2 / G-1:** process-bound one-shot supervising launch authority;
  terminal PREEXEC stop; replay/reuse/binding rejection; new attempt only
  from a new Control Room/operator mint; credential custody mandatory;
  Yama >= 1 environmental gate.
- **C-3 / G-2:** primary workspace = auditor-output role; NO `--add-dir`;
  NO CLI `-s workspace-write`; named restricted permission profile; one
  persistent model-write root only; evidence read-only; target/host denied
  as designed; `CODEX_HOME`/auth hidden from model-command sandbox; hard
  no-egress gate including systemd-resolved/DBus masking where applicable;
  zero inherited socket FD gate; pre-inference GATE-W / zero-provider
  rehearsal.

Implementation must be independently reviewable and must NOT inherit a
qualification verdict from these design/probe results.

## 12. Campaign-2 held state — preserved EXACTLY

```
AUDITOR_A_AUTHORITY = CONSUMED_CLOSED
AUDITOR_B_AUTHORITY = CONSUMED_CLOSED
MODEL_ENGAGEMENTS_AUTHORIZED = 2
MODEL_ENGAGEMENTS_USED = 2
FIRST_PASS_A = PRESENT / FROZEN
FIRST_PASS_B = ABSENT
FIRST_PASS_BARRIER = CLOSED
NO_CONFORMING_BLIND_FIRST_PASS_SET
CAMPAIGNS = 2 OF MAX 2
CAMPAIGN_3 = NOT AUTHORIZED / DOES NOT EXIST
QUALIFICATION_EVIDENCE_COMPLETENESS = BLOCKING for that historical campaign
QUALIFICATION = NONE
INSTALLATION = NONE
```

AUCDEV-010 remains **P1 / BLOCKED**. The AUCDEV-023 READY transition does
NOT reopen, repair or extend Campaign-2. Nothing in this readback altered,
reinterpreted, revived or reset any of these states; no historical verdict
was rewritten.

## 13. Backlog counts — mechanically derived after the transition

Recounted mechanically from the complete prioritized queue at the exact base
BEFORE mutation (20 queue rows; statuses READY 8 + OPEN 8 + BLOCKED 3 +
DONE 1; DONE excluded from open totals per the update protocol) and
re-derived after the AUCDEV-023 OPEN→READY transition:

```
total open items (unchanged; OPEN→READY stays inside the open-total definition) = 19
READY = 9
OPEN = 7
BLOCKED = 3
IN_PROGRESS = 0
P0 = 2 / P1 = 7 / P2 = 11  (unchanged)
DEFERRED = 3 (AUCDEV-020/021/022 unchanged)
ACCEPTED_RESIDUAL = 8 (R01–R08 unchanged)
DONE = 5 (unchanged)
```

## 14. Publication change set (EXACTLY these paths)

1. `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (current-facing fields
   updated; `Last updated` and checkpoint advanced; CURRENT-STATE history
   record 79 appended)
2. `docs/chatgpt-project/AUCDEV-BACKLOG.md` (counts block updated with the
   OPEN→READY recount; AUCDEV-023 prioritized-queue row OPEN → READY; work
   item updated with the clean-reproduction readback + readiness-transition
   status; AUCDEV-023 BACKLOG history record 4 appended)
3. `docs/chatgpt-project/AUCDEV-023-G2-CLEAN-EXEC-POLICY-EQUIVALENCE-REPRODUCTION-READBACK.md`
   (THIS canonical record; NEW path)

NOT changed: `AUCDEV-QUALIFICATION-HISTORY.md`,
`AUCDEV-ARCHITECTURE-SUMMARY.md`, `skill/`, `tests/`, schemas/contracts,
frozen Campaign-2 artifacts, prior AUCDEV-023 reports (including
`AUCDEV-023-G2-EXACT-EXEC-POLICY-PROBE-READBACK.md`), historical AUCDEV-010
reports.

## 15. Current-facing state after this publication

- Active/current item: **AUCDEV-023 / P1 / READY**
- G-1: `DESIGN_PROBE_CLOSURE_ACCEPTED`
- G-2: `CLOSED_AT_DESIGN_PROBE_STRENGTH`
- Current validation: AUCDEV-023 G-2 clean exec-policy-equivalence
  reproduction Control Room readback ACCEPTED; readiness criteria satisfied.
- **Implementation authority = NONE.** This publication itself authorizes NO
  implementation.

## 16. Next action and result

Immediate next action (EXACTLY ONE): **INDEPENDENT CONTROL ROOM READBACK OF
THIS AUCDEV-023 OPEN-TO-READY READINESS PUBLICATION.**

Result: `AUCDEV_023_G2_CLEAN_EXEC_POLICY_EQUIVALENCE_READBACK_AND_OPEN_TO_READY_TRANSITION_PUBLISHED_FOR_CONTROL_ROOM_READBACK`.
