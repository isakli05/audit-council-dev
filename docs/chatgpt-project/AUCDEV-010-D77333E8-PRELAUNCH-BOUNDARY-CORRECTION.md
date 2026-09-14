# AUCDEV-010 — D77333E8 Prelaunch External-Tooling Isolation Boundary Correction (Canonical Record)

Publication date: **2026-09-14** (Europe/Istanbul). Session class: ZERO-MODEL
HARNESS / PRELAUNCH-BOUNDARY CORRECTION IMPLEMENTER — NOT Auditor A, NOT
Auditor B, NOT the Control Room, NOT a qualification authority, NOT an
installation authority. ZERO provider/model/frontier inference calls (the
corrected-boundary battery substituted LOCAL deterministic probes for the
provider executable; the RED probe ran against the frozen OLD launcher bytes
read-only). This session IMPLEMENTED the prelaunch external-tooling isolation
boundary correction ordered by the Control Room readback of the D77333E8
auditor package and publishes this governance-only record. NO auditor
execution is authorized by this record. The audit target and the
auditor-readable frozen transports were NOT modified.

Parallel records: CURRENT-STATE history record 56; BACKLOG AUCDEV-010 history
record 58. Canonical base: `96a53fc3fa49a95200787e1282268b8edffecc33` (live
GitHub `master` verified EXACT at bootstrap and re-verified immediately
before the single fast-forward push of THIS publication). Correction
workspace + Control Room handoff archive identity: §9.

## 1. Control Room readback disposition (input authority; recorded verbatim)

The D77333E8 auditor package target/payload portion is mechanically accepted.
Launch eligibility is NOT accepted because the frozen external-tooling
boundary has one material isolation gap and one auth-minimization gap:

`AUDITOR_EXTERNAL_TOOLING_BOUNDARY_PID_NAMESPACE_INCOMPLETE`
`PROC_PID_ROOT_ESCAPE_NOT_NEGATIVE_TESTED`
`ROLE_SPECIFIC_AUTH_MINIMIZATION_NOT_ENFORCED`

plus two nonblocking publication-record precision discrepancies:

`CANONICAL_TRANSPORT_CENSUS_RECORD_PRECISION_MISMATCH`
`CANONICAL_FINGERPRINT_RECORD_PRECISION_MISMATCH`

No historical evidence was mutated and no auditor transport was rebuilt.

## 2. Live bootstrap (mandatory; all EXACT)

Live GitHub `isakli05/audit-council-dev` branch `master` HEAD =
`96a53fc3fa49a95200787e1282268b8edffecc33` (== required; remote readback
identical). The five governance documents were read AT that SHA. Verified:
event `AUCDEV-010-BRQ-FINAL-D77333E8-20260914-01`; audit target
`d77333e86aa091d2ac003e9a2ad26c88dff56aeb` with root tree
`de7261e3c912fa74e3a06d3f114b7e489c66225c`, skill tree
`c792933a862d9a5434681a88d183470dd8b15d2f`, sole parent
`b04aa604771b237e3bc8abe96daa358fa8f9edd6` (137 tracked paths); Auditor A =
NOT_STARTED; Auditor B = NOT_STARTED; MODEL_ENGAGEMENTS_USED = 0;
EXECUTION_AUTHORITY = NOT_YET_GRANTED; qualification readiness BLOCKED;
qualification NONE; installation NONE.

## 3. Immutable auditor payload (re-verified unchanged; byte-for-byte)

Auditor-A transport = Auditor-B transport = SHA-256
`68ac889beba1df3f89837f5535f02425ebaea0efbae014e9506c26a64d4e1f47`, 453931
bytes each, byte-equal (`cmp`). COMMON_EVIDENCE_PAYLOAD
`3348a6e698456afa3b71a8e5ebe0120777b666ca80213fd9e4879db16da93e03`; FDR
`ee1f6fea17e5833db3e98c5ad680b3082a8e8af41a6e26f5bc6eeba9fec7b6af` + sidecar
`ee8f685b…`; evidence manifest `1bedece6…` with all 12 common-input entries
byte-verified; FDR artifact bindings (contract `9f5c732e…`, output contract
`84abffdf…`, structural validator `778e30f4…`) verified. The qualification
contract, output contract, common evidence, product archive, delta, target
identity proof and auditor transports are UNTOUCHED — the correction is
controller/harness-side ONLY.

## 4. Old boundary diagnosis (frozen bytes; preserved unmodified)

The frozen preparation-time launcher `launch-boundary.sh`
(`5fd5a5760d9c1b9404e843eda441f20985281f837839edd62e0d5a7fadd9261d`)
creates a mount-namespace allowlist but:

1. does NOT pass `--unshare-pid`: it mounts `--proc /proc` while retaining
   the caller's PID namespace, so the provider could enumerate host
   processes and potentially reach host paths via `/proc/<host-pid>/root/…`
   (direct `/home` absence is insufficient isolation evidence);
2. requires AND mounts BOTH `/auditor-auth/claude` AND `/auditor-auth/codex`
   for either role, and always sets BOTH `CLAUDE_CONFIG_DIR` and `CODEX_HOME`;
3. binds `/auditor-home` to a persistent host-backed skeleton directory.

All old boundary artifacts (launcher, contract `1edac717…`, clean-scope
instructions `8bbe5c57…`, validator `0fce0128…`, checker `2f7c0eaa…`,
manifest `d8786ab5…`, probe evidence) are preserved byte-identical as
historical package-preparation evidence and re-hashed this session.

## 5. Old-boundary RED observation (deterministic; honestly classified)

Zero-inference RED probe against the EXACT frozen OLD launcher bytes
(controller-side sentinel + canary outside the allowlist; workspace
`old-boundary-red/`, raw facts
`red-old-boundary-A.json` `fb20c5b3…`, classification
`705b246d…`): host sentinel PID 180620 (`sleep 600`) was VISIBLE inside the
old boundary (`/proc/180620` existed; `stat` and `cmdline` readable);
`/proc` exposed 594 host processes including host systemd PID 1
(`/usr/lib/systemd/systemd --switched-root --system`); own pid was
host-numbered (180624), not namespace-isolated. Attempted
`/proc/<sentinel>/root` dereference (root-link readlink, root listdir,
canary read through `/proc/<sentinel>/root/<canary>`) was DENIED errno=13 on
THIS host (kernel Yama `ptrace_scope=1`) — recorded precisely and NOT relied
upon as a control. Classification:
`OLD_BOUNDARY_PID_ISOLATION = RED_HOST_PID_NAMESPACE_LEAKED`
(host-process visibility alone establishes it; host ptrace policy drift
cannot be a security control). The old boundary was structurally incomplete
because it created no PID namespace, exactly as the readback found.

## 6. Corrected boundary mechanics (C1–C4; all NEW successor artifacts)

Correction workspace:
`/home/isa/audits/aucdev-010-d77333e8-prelaunch-boundary-correction-20260914/`.
Nothing old was overwritten; all corrected artifacts are new files under
`corrected-boundary/`, bound by the NEW successor manifest.

| Corrected artifact | SHA-256 |
|---|---|
| `launch-boundary.sh` (corrected) | `f30850850bf1fe57c3a83d80e358b4d8e55d2cef7ba2ac8b0f75fc05a61e3b22` |
| `verify-launch-environment.py` (corrected validator) | `efc410bdd53e8c8e911ef2e6d042152d0623dbc3951e8f6082cb6c8e53485534` |
| `post-execution-access-checker.py` (corrected) | `8ad0d0f371f4b99f32f6b85a965afdecdba9d9d33f3ad32ed105573e9fb02c83` |
| External-tooling boundary contract (corrected v2) | `2306625cf6de118990f279cb2e196acbebf9ecdf98c6831b9420334beec33b96` |
| Future-controller clean-scope instructions (corrected v2) | `42a5bc18e596d6bb190feeaf942e668d6f172b040fab13df15b1ca776dbad73d` |
| `run-zero-inference-probe.sh` (corrected battery) | `a473c1ddd0d5c58e103f2535a2ba9593104c5570d97ac9d5e2b6b28397db7e99` |
| `probe-inner.py` (corrected inner probe) | `6bd67a557b923c2aa2322150b9ac7d60c6754ef8eda9e471cd698da1e52bd37f` |
| Corrected launch-boundary manifest (successor, NEW) | `0a1710ed19e62523645760571db6eb3f8b609afb0b5725084dd6b10ea4ff1b63` |

- **C1 PID namespace** (closes
  `AUDITOR_EXTERNAL_TOOLING_BOUNDARY_PID_NAMESPACE_INCOMPLETE`): the
  corrected launcher ALWAYS passes `--unshare-pid` together with a freshly
  mounted `--proc /proc` instantiated FOR the sandbox PID namespace; the
  provider process tree sees only sandbox-namespace processes.
- **C2 role-specific auth minimization** (closes
  `ROLE_SPECIFIC_AUTH_MINIMIZATION_NOT_ENFORCED`): role A mounts ONLY
  `/auditor-auth/claude` (ro) and sets ONLY `CLAUDE_CONFIG_DIR`; role B
  mounts ONLY `/auditor-auth/codex` (ro) and sets ONLY `CODEX_HOME`. A
  fail-closed prelaunch validation over the CONSTRUCTED bwrap argv proves
  the irrelevant auth path and env var appear NOWHERE before exec. Runtime
  gates prove it at mount level: the battery staged BOTH provider subtrees
  in each probe auth root, and the irrelevant subtree was NONEXISTENT inside
  the boundary with its env var unset.
- **C3 writable-home precision**: `/auditor-home` is a fresh tmpfs
  (ephemeral, per-launch, role-specific, never peer-shared; NO host-backed
  home skeleton is mounted anywhere); the ONLY persistent writable surface
  is `/auditor-output`; `/tmp`, `/run`, `/var` remain tmpfs. No
  host-backing residual remains, so no residual record is needed.
- **C4 proc-escape negative testing** (closes
  `PROC_PID_ROOT_ESCAPE_NOT_NEGATIVE_TESTED`): `N_PROC_HOST_PID_INVISIBLE`
  and `N_PROC_HOST_ROOT_ESCAPE_BLOCKED` are ACTUAL battery gates in BOTH the
  corrected inner probe and the corrected execution-time validator, whose
  `--host-sentinel-pid/--host-canary-path/--host-canary-sha` arguments are
  MANDATORY (fail-closed if omitted).
- Network access is UNCHANGED (no `--unshare-net`; the provider route
  requires it and no proven route supports unsharing it); IPC namespace
  unchanged.

## 7. Corrected zero-inference battery (both roles; zero model calls)

The corrected `run-zero-inference-probe.sh` launched the EXACT corrected
boundary for role A and role B with local deterministic substitutes
(corrected validator + comprehensive inner probe) and inert synthetic
fixture auth files (explicit `SYNTHETIC-INERT-FIXTURE` markers; NO
credential bytes anywhere in any package, probe or handoff). Results
(`corrected-boundary-battery-results.json` `5c7a01ec…`):

- existing positive gates P1–P8 ALL PASS both roles (incl. node v24.14.0
  EXECUTED inside the PID-namespace boundary);
- existing forbidden-path gates N1–N9 ALL PASS both roles (prior
  contamination path, user trees, project memory, prior workspaces,
  governance workspace, `/home`, `/root` all nonexistent);
- new gates ALL PASS both roles: `P9_pid_namespace_established` (visible
  pids = [1, 2] only — the bwrap sandbox init and the payload — NSpid purity
  violations: none), `N_PROC_HOST_PID_INVISIBLE` (host sentinel
  `exists=False` inside), `N_PROC_HOST_ROOT_ESCAPE_BLOCKED`
  (`/proc/<sentinel>/root/<canary>` absent; root link not walkable),
  `P10_role_own_auth_readable`, `N11_irrelevant_auth_absent` (mount-level),
  `P11_home_ephemeral_tmpfs` (fstype=tmpfs);
- 94 inner gates total both roles (23 validator + 24 probe per role), zero
  failed;
- execution-time validator INSIDE the corrected boundary: exit 0 with the
  literal `ENVIRONMENT_VERIFIED` line both roles
  (`corrected-validator-inside-A.txt` `669a5876…`); the SAME validator
  OUTSIDE the boundary: exit 2 FAIL-CLOSED both roles (20 gates fail
  outside, incl. all forbidden-path, PID-namespace, sentinel and role-env
  gates);
- launcher fail-closed negative (role-own auth missing): exit 9;
- corrected checker fixtures: clean output exit 0; forbidden-path +
  `/proc/<pid>/root`-referencing output exit 2 (surfaced, never silent).

## 8. Record-precision corrections (append-only; values mechanically re-verified)

`evidence/RECORD-PRECISION-CORRECTIONS.md` (`3363a5f5…`) records, WITHOUT
touching any historical artifact:

1. **Transport census**: the actual transport tar has **21 total members =
   19 regular files + 2 directories**; its `SHA256SUMS` contains **18
   entries** and verifies **18/18 PASS** (exit 0). The prior canonical
   phrase "18 members / 17/17" was a record-precision error ONLY — transport
   bytes, checksums, parity and gate results unchanged.
2. **Candidate fingerprint**: the DELIVERED frozen capture
   (`common-inputs/repo-fingerprint.json`, `0e6f77c5…` inside BOTH
   transports), the workspace Event Record and the package self-test battery
   all record `fingerprint_sha256 =
   a60ae2d13073acef76082c85e434db8541d4674aeffbc82a72e1fc997a66b11d`; the
   prior canonical report/CURRENT-STATE token
   `8efb713ce6d5f25676e9d10bff4f5fea263bf4786790a9e55c9addec233bbf63` is
   NOT the value in the delivered frozen capture. Target identity unchanged
   in all cases (commit `d77333e8…`; root tree `de7261e3…`; skill tree
   `c792933a…`; identity manifest `9207e34b…`; full-target proof
   `56b3dfb3…`).

## 9. Successor launch-readiness battery, publication, handoff

Successor battery (`successor-launch-readiness-battery.py` `b0be83da…`;
results `evidence/successor-launch-readiness-battery.json` `f7960017…`):
gate classes SEPARATED as required — CLASS 1 immutable auditor-payload
gates: 15; CLASS 2 corrected external-boundary gates: 8; CLASS 3
record-precision disclosures: 3. **Total 26 gates, DERIVED MECHANICALLY from
the executed gate lists (no pre-written expected total): zero failed.**
Result: `CORRECTED_BOUNDARY_LAUNCH_ELIGIBLE_PENDING_CONTROL_ROOM_READBACK`,
binding the SAME event, SAME target `d77333e8…`, SAME A/B transport bytes
`68ac889b…` (453931 B each) and the NEW corrected boundary artifacts. The
original preparation archive remains immutable and unchanged (only its
record-precision description is corrected append-only).

Publication changes EXACTLY: `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`,
`docs/chatgpt-project/AUCDEV-BACKLOG.md`, NEW
`docs/chatgpt-project/AUCDEV-010-D77333E8-PRELAUNCH-BOUNDARY-CORRECTION.md`
(THIS file). No product/source/test path, no qualification-history path and
no frozen package artifact was modified. Single fast-forward push over exact
base `96a53fc3…` (prepush remote readback EXACT; postpush readback recorded
in the handoff). The Control Room handoff archive (FINAL-REPORT + bootstrap
+ diagnosis + RED evidence + corrected artifacts + battery results +
unchanged transport readback proof + record-precision corrections +
governance diff + push evidence + secret scan + inventory + SHA256SUMS
generated LAST) is delivered alongside this record; its outer SHA-256, byte
size and member census are recorded in the workspace FINAL-REPORT and
EVENT-RECORD.

## 10. Canonical result state

- `PRELAUNCH_BOUNDARY_CORRECTION_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK`.
- Auditor A = NOT_STARTED; Auditor B = NOT_STARTED; MODEL_ENGAGEMENTS_USED =
  0; EXECUTION_AUTHORITY = NOT_YET_GRANTED.
- Qualification readiness BLOCKED; qualification NONE; installation NONE;
  installed qualified predecessor NOT ESTABLISHED; bootstrap-root exception
  applicable, unconsumed.
- This record does NOT mean the package is accepted by the Control Room, any
  auditor started, execution authority granted, any model engagement
  consumed, candidate PASS, qualification ready, qualified or installed.

Immediate next action:
`INDEPENDENT CONTROL ROOM READBACK OF THIS D77333E8 PRELAUNCH BOUNDARY CORRECTION PUBLICATION (CORRECTED BOUNDARY ARTIFACTS + RED/GREEN EVIDENCE + SUCCESSOR BATTERY); ONLY IF ACCEPTED, EXPLICIT OPERATOR EXECUTION AUTHORITY FOR EVENT AUCDEV-010-BRQ-FINAL-D77333E8-20260914-01, WITH BOTH FUTURE CONTROLLER LAUNCHES UNDER THE CORRECTED BOUNDARY AND CORRECTED CLEAN-SCOPE INSTRUCTIONS (MANDATORY SENTINEL/CANARY STAGING)`

## 11. Success wording

`AUCDEV_010_D77333E8_PRELAUNCH_BOUNDARY_CORRECTION_IMPLEMENTED_AWAITING_CONTROL_ROOM_READBACK`
