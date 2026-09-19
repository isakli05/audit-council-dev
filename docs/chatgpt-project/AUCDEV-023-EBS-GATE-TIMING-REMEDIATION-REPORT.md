# AUCDEV-023 — Narrow Bounded EBS Gate-Timing Remediation Report (AUCDEV023-CR-EBS-S1-001)

| Field | Value |
|---|---|
| Status | **`AUCDEV_023_EBS_GATE_TIMING_REMEDIATION = IMPLEMENTED_CANDIDATE / AWAITING_FRESH_CONTROL_ROOM_READBACK`** — the finding is remediated at implementation/self-test strength ONLY. NOT Control Room accepted, NOT closed, NOT an event package, NOT execution-authorized, NOT qualified, NOT installed, and supporting NO real provider/event. Implementation claims are NOT audit truth. |
| Session class | BOUNDED ZERO-PROVIDER REMEDIATION-IMPLEMENTATION SESSION — the selected implementation agent (Claude Code + GLM-5.3) is an IMPLEMENTER ONLY: NOT the Control Room, NOT an independent auditor, NOT authorized to independently close Control Room findings, NOT authorized to prepare or instantiate an event package, NOT authorized to run a real auditor/model/provider, NOT authorized to use real provider credentials, NOT authorized to invoke `/audit-council`, NOT authorized to qualify or install anything |
| Operator authority | Operator tasking (2026-09-19) authorizing ONLY: narrow bounded AUCDEV-023 EBS gate-timing remediation for AUCDEV023-CR-EBS-S1-001 (`EXECUTION_TIME_RESOURCE_GATE_FROZEN_AT_S1_AND_NOT_REVALIDATED`); deterministic zero-provider / zero-real-credential validation; implementation evidence publication; bounded canonical state/report updates for this transition. The previously granted operator authorization for bounded AUCDEV-023 EVENT-PACKAGE PREPARATION (S1), incl. zero-inference GATE-W′ validation, EXISTS in the Control Room conversation and REMAINS PAUSED, NOT CONSUMED — S1-001 blocked trustworthy package freeze, and this remediation MUST NOT and DID NOT perform S1 itself. No event execution authority is granted or exercised. |
| Exact implementation base | `63db66a3433f2d02a2fdc0745450ee017323ffc2` (tree `4c71509386f544556f1aa044de893b665c52d81f`; sole parent `4448deea18ae90f14904f38c997aaffbf2507a6a`; bootstrap-supervisor subtree `f2e526c3a4fc44cfc4273c05faea57a71a8ef989`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this session's bootstrap (fetch + ls-remote of origin) and re-resolved immediately before staging. THIS gate-timing publication is the sole commit ahead of that base. |
| Governing records read at the exact base | CURRENT-STATE, BACKLOG, PROJECT-UPDATE-PROTOCOL, CONTROL-ROOM-RUNBOOK, the governance ADOPTION + DESIGN-REVISION + DESIGN-REVISION-READBACK records, the EBS NARROW-MANIFEST-TYPE-REMEDIATION REPORT + its ACCEPTED READBACK (all five prior EBS findings CLOSED on EXACT SHA `4448deea…`), the AUCDEV-010 Campaign-2 RESOURCE-GATE CORRECTION (historical `DEFERRED_TO_EXECUTION_GATE` evidence), `bootstrap-supervisor/MANIFEST.json`, `README.md`, the complete `bootstrap-supervisor/ebs/**` source, and the complete `bootstrap-supervisor/tests/**` suite |
| Frozen target (unchanged, EXACT) | `isakli05/audit-council-dev` @ `d4d584ffa47ad2848268ba947247f81a845b2322` (root tree `1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7`; qualification-harness tree `5b8d5e5465923740470ff63ed9b8683f257a3787`; skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`) — AUDIT SUBJECT / EVIDENCE ONLY, verified EXACT at bootstrap and pre-commit; both trees given NO bootstrap authority |
| Prior accepted EBS identity (inherited, EXACT) | manifest_sha256 `049c200771c7b85d39a9445b645d2ad8c27c521ddd18be7f6ce35a7a2016a88f` / package_sha256 `d478a5013ede94ebd63870948594c0675914792ad1b8268708473366123ef9fd` (21 rows, shipped by exact accepted candidate `4448deea…`) |
| Qualification / installation | qualification NONE / installation NONE |

Claim classes: `OBSERVED_FACT` (mechanically observed this session),
`FINDING_TEXT` (the Control Room tasking's recorded requirements),
`IMPLEMENTED` (what this candidate's code does, evidenced by the
deterministic battery). CR-EBS-S1-001 remains OPEN until a FRESH
independent Control Room readback of THIS publication says otherwise.

---

## 1. The finding and the required remediation strength (FINDING_TEXT)

```
AUCDEV023-CR-EBS-S1-001
EXECUTION_TIME_RESOURCE_GATE_FROZEN_AT_S1_AND_NOT_REVALIDATED
/ OPEN / BLOCKING
BOOTSTRAP_SUPERVISOR_IMPLEMENTATION_DEFECT
/ GOVERNANCE_CONTRACT_TIMING_MISMATCH
```

Core required invariant (tasking §4): STATIC/S1 preparation gates must
remain frozen and transport-bound; the DYNAMIC RESOURCE_GATE must NOT be
frozen as a historical PASS result — it must be defined/frozen as an
exact executable gate artifact contract during S1, identity-bound into
the binding/event-package projection, EXECUTED by the EBS itself during
the live attempt after Supervisor startup identity/package checks and
BEFORE GATES_PASSED, exactly once, fail-closed on any non-PASS or
malformed/failed execution, durably evidenced in the GATES_PASSED
accounting record, and impossible to satisfy with a stale S1 PASS
document. No controller or external instruction-following process may
supply a trusted RESOURCE_GATE PASS; no caller-supplied boolean, JSON
PASS, timestamp, mtime, or ordinary file claim is sufficient.

## 2. Exact defect (OBSERVED_FACT at the base)

`bootstrap-supervisor/ebs/binding.py` defined `REQUIRED_GATES`
INCLUDING `RESOURCE_GATE`, and `parse_binding()` required every
`gate_evidence` member to carry `status == "PASS"` — the complete
object binding-digest-covered and event-package transport-projection-
covered. `bootstrap-supervisor/ebs/launch.py:
Supervisor.validate_gates()` did NOT execute RESOURCE_GATE or
re-evaluate any live resource condition; it relied on the already-parsed
frozen PASS evidence and appended `GATES_PASSED`. A RESOURCE_GATE PASS
generated/frozen during S1 package preparation therefore remained
usable at a later, separately authorized execution while stale.

### 2.1 RED reproduction (recorded BEFORE the fix, preserved separately)

`RED-01-s1-001-defect-reproduction.txt` (evidence directory), run in an
isolated worktree at EXACT base `63db66a…` with the canonical tree
untouched: a synthetic binding/event package was frozen carrying a
RESOURCE_GATE PASS in `gate_evidence`; the inert runtime-gate fixture
(see §7) — which, if executed, writes an attempt-keyed /tmp sentinel +
execution counter and emits the strict result envelope — was bound
INSIDE the frozen package as a manifest row with regenerated
self-consistent pins; AFTER the freeze the external live resource state
was flipped to a demonstrably FAILING condition
(`/tmp/aucdev023-rg-state-<attempt>.json` = `fail-state`). Result at
the base: `parse_binding` ACCEPTED the stale package-time PASS;
`Supervisor.validate_gates()` reached `GATES_PASSED`; the durable record
ended `GATES_PASSED`; and the sentinel + counter were ABSENT — the
bound gate was NEVER EXECUTED despite the failing live state. This is
the exact S1-001 defect, at both the parse layer and the launch layer,
in its strongest form.

## 3. Frozen-vs-runtime gate separation (IMPLEMENTED)

`ebs/binding.py` now splits the gate dimension:

- `REQUIRED_GATES` is EXACTLY the six STATIC preparation gates:
  `PACKAGE_BINDING_IDENTITY`, `COMMON_EVIDENCE_PARITY`,
  `IDENTITY_LINTER`, `BLINDNESS_MAP`, `GATE_W_PRIME`,
  `REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION`. A `RESOURCE_GATE` member
  inside `gate_evidence` is refused outright
  (`GATE_EVIDENCE_RESOURCE_GATE_FORBIDDEN`) BEFORE the generic
  exact-key-set check — the stale-PASS shape is structurally
  unrepresentable.
- `runtime_gates` is a NEW mandatory top-level binding dimension with
  the EXACT key set `{"RESOURCE_GATE"}` and the EXACT descriptor field
  set `{identity, path, sha256, result_schema}`:
  - `identity`: safe identity token (charset-bounded);
  - `path`: safe event-package-relative path (non-empty bounded str of
    charset-bounded segments; absolute, `""`/`.`/`..`/empty segments,
    and non-str types refused);
  - `sha256`: exact 64-hex digest of the frozen artifact bytes;
  - `result_schema`: exactly `AUCDEV-023-RESOURCE-GATE-RESULT-V1`.
- The descriptor carries NO result and NO PASS; unknown runtime gates,
  unknown descriptor fields, malformed digests, unsafe paths, and wrong
  result-schema identities are all refused at parse (fail closed,
  type-strict).
- The descriptor is covered by `Binding.digest` (canonical JSON of the
  whole document) and by `binding_projection` (every security dimension
  except `event_package`), so ANY descriptor substitution under the
  same declared event-package identity fails cross-binding.

## 4. Event-package manifest schema V1 → V2 (IMPLEMENTED)

Because the projection semantics materially change (RESOURCE_GATE left
the frozen evidence set; the runtime-gate descriptor became a bound
security dimension), `EVENT_MANIFEST_SCHEMA` advances to
`AUCDEV-023-EVENT-PACKAGE-MANIFEST-V2`. A V1 manifest — including a
perfectly self-consistent one with updated pins — is REFUSED
(`EVENT_MANIFEST_SCHEMA_UNEXPECTED`), never silently accepted as
equivalent. No real AUCDEV-023 event package exists to migrate; NO
compatibility machinery was added for an unused real V1 package;
synthetic test packages were regenerated under V2. The strict manifest
key set `{schema, transport_binding, files, package_sha256}`, the
REM2-001 exact-int `files[].bytes` row contract, and the non-circular
package identity construction are all preserved unchanged.

## 5. Runtime RESOURCE_GATE execution authority (IMPLEMENTED)

The runtime resource gate is an EVENT-PACKAGE-SIDE trusted component;
the EBS implements NO resource thresholds or policy. New
`ebs/launch.py` machinery — reusing the EXISTING low-level primitives
(`_hash_fd`/`open_verified_launcher` discipline, `fd_exec` /
`_execveat(AT_EMPTY_PATH)` verified-fd exec, `strict_loads`,
`canonical_bytes`):

- `open_runtime_gate(root, binding, event_manifest)`: resolves the
  descriptor path from the ALREADY-VERIFIED event-package tree;
  requires the path to be a manifest row of that verified package;
  opens with `O_RDONLY|O_NOFOLLOW`; requires a regular file with an
  execute bit; requires the fd's SHA-256 to EQUAL the descriptor's
  exact `sha256`; returns the HELD verified fd.
- `_gate_child(...)`: child-side hygiene — stdout is the bounded result
  pipe, stdin/stderr are devnull, every fd except {0,1,2,gate_fd} is
  closed, the gate fd is made exec-surviving, `PR_SET_DUMPABLE=0` is
  set, and the ALREADY-VERIFIED open fd is exec'd. NO credential fd is
  inherited (custody never enters this path) and NO launch
  authority/custody plaintext is exposed to the gate. No pathname
  re-open exists after final verification — the executed image IS the
  held fd (the same fexecve-class identity-preserving exec as the
  launcher path).
- `_run_runtime_gate(...)`: forks ONCE and executes the held fd with
  argv bound to this attempt `[identity, event_id, auditor_role,
  attempt_id]` and a clean minimal environment `{"PATH":
  "/usr/bin:/bin", "LANG": "C"}` (identical shape to the launcher
  child); the result is size-bounded (`RESOURCE_GATE_RESULT_MAX` =
  65536 bytes) BEFORE acceptance; the child is polled with a
  deterministic deadline (`RESOURCE_GATE_TIMEOUT` = 10.0 s) — a hung
  gate is SIGKILLed, reaped, and refused (`RESOURCE_GATE_TIMEOUT`), so
  no unbounded authority process can exist; non-zero child exit is
  refused (exit 98 = exec failure refused as `RESOURCE_GATE_EXEC_FAILED`);
  missing/empty output is refused. NO `subprocess` import, NO
  networking, NO daemon/scheduler was added (stdlib-only scan + battery
  static tests enforce this).
- `_validate_resource_gate_result(output, binding)`: strict JSON
  (`strict_loads`: duplicate keys and non-finite constants refused);
  exact top-level key set; schema exactly
  `AUCDEV-023-RESOURCE-GATE-RESULT-V1`; `event_id`/`auditor_role`/
  `attempt_id` EXACTLY equal the binding's; top-level `status` must be
  `PASS`; EXACTLY three `samples`, each an object with the exact key
  set `{status, detail}`, `status` exactly `PASS`, `detail` an object.
  A top-level PASS never overrides a failed sample, and PASS is never
  inferred from the exit code alone.

## 6. Exact runtime ordering (IMPLEMENTED; battery-proven)

`Supervisor.__init__` startup order: (1) live EBS package
self-identity verification; (2) store attempt + binding-digest
equality; (3) event-package identity verification; (4) event-package
transport-projection equality (V2); (5) `open_runtime_gate` — the
runtime-gate artifact identity verified and the verified open fd HELD.
`validate_gates()` (the only PREPARED → GATES_PASSED path): (6)
exactly-once guard; (7) held-fd RE-HASH immediately before execution
(`RESOURCE_GATE_FD_DRIFT` on mismatch); (8) EXECUTION of the verified
fd exactly once; (9) strict fresh-result validation; (10) durable
`GATES_PASSED` append carrying the fresh evidence; (11) in-memory
transition. Launcher verification exists ONLY at/after GATES_PASSED
(`LAUNCHER_VERIFICATION_REQUIRES_GATES_PASSED`); CONSUMED_PRE_EXEC and
the future execution path are NOT exercised by this remediation's
tests beyond the existing inert launcher regressions. ANY failure at
steps 6–10 durably terminalizes the attempt
(`TERMINAL_PREEXEC_STOP`, authority unconsumed, zero model
engagement) and NO same-attempt retry of the gate exists (state is
absorbing AND the `_resource_gate_executed` guard refuses re-entry).

## 7. Synthetic/inert fixtures ONLY

The ONE new fixture `tests/fixtures/inert_resource_gate.py`
(marker `EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER`) is an
unmistakably synthetic local gate whose behavior is driven by an
EXTERNAL attempt-keyed /tmp live-state file (absent = honest PASS with
three fresh PASS samples: external state + `statvfs("/tmp")` +
`/proc/meminfo`), plus a sentinel + execution counter proving whether
and how often the EBS executed it. The SAME frozen artifact PASSes or
FAILs on state sampled at execution time — exactly the freshness
property under test. `tests/conftest.py` materializes it (shebang
rewritten to the current interpreter, mode 0755) into every synthetic
event package at the bound path `runtime/resource-gate.py` and pins
its digest into `runtime_gates.RESOURCE_GATE.sha256` BEFORE the
projection is derived. The REAL AUCDEV-023 event package is NOT
prepared, NOT built, NOT committed.

## 8. RED → GREEN test matrix (deterministic, zero-provider)

- RED (before the fix; §2.1 above): stale frozen PASS accepted;
  GATES_PASSED reached with the gate never executed; sentinel/count
  absent; durable record GATES_PASSED. Preserved separately in
  `RED-01-s1-001-defect-reproduction.txt`.
- GREEN (after the fix; `tests/test_resourcegate.py`, 29/29; plus
  `test_binding.py` 81/81 and `test_eventpackage.py` 63/63):
  1. frozen RESOURCE_GATE PASS in gate_evidence refused;
  2. runtime_gates mandatory (missing/wrong-type/unknown-gate refused);
  3. descriptor wrong/missing/extra fields refused;
  4. unsafe paths refused (absolute/traversal/empty/dot/double-slash/
     wrong type);
  5. live artifact digest ≠ descriptor refused at startup
     (regenerated self-consistent package, pins updated, projection
     equal — ONLY the artifact hash can refuse); path not a manifest
     row refused; non-executable refused; symlink refused;
  6. event-package manifest V1 refused;
  7. V2 projection binds the runtime-gate descriptor;
  8. same package + substituted runtime-gate identity/sha/path
     refused by cross-binding in BOTH directions (binding-side and
     regenerated-package-side, incl. descriptor result-schema);
  9. freshly executed PASS gate with three PASS samples reaches
     GATES_PASSED (sentinel + counter prove real execution);
  10. gate executes EXACTLY ONCE (second validate refused; count 1);
  11. live state flipped to FAIL AFTER the freeze is observed fresh
      and blocks GATES_PASSED (TERMINAL_PREEXEC_STOP, authority
      unconsumed, count 1);
  12–21. mode matrix fail-closed: non-zero child exit (with a
      perfectly VALID envelope printed — PASS never inferred from
      output alone), malformed JSON, duplicate-key JSON, wrong schema,
      wrong event, wrong role, wrong attempt, top-level FAIL, one
      failed sample under a top-level PASS, sample count 2, sample
      count 4, empty output, oversized output — every case blocks,
      record terminal, no CONSUMED/EXEC;
  hang: bounded timeout kills the child and refuses (< 60 s wall);
  held-fd drift: in-place artifact mutation after startup refused
  before execution;
  22. no same-attempt retry after any failure (state + guard); result
      persistence/accounting failure after a fresh PASS still blocks
      GATES_PASSED and terminalizes (monkeypatched append failure);
  23. GATES_PASSED durable record carries `resource_gate_identity`,
      `resource_gate_sha256`, `resource_gate_result_schema`,
      `resource_gate_result` (canonical validated JSON string),
      `resource_gate_result_sha256`, `resource_gate_result_size` —
      digest/size mechanically re-verified against the stored string;
  24. gate-only lifecycle records contain NO CONSUMED_PRE_EXEC and NO
      EXEC_ATTEMPTED (the gate is NOT a model engagement).

## 9. Prior-finding fresh regressions on the new candidate (IMPLEMENTED)

All five prior EBS Control Room closures are bound to EXACT SHA
`4448deea…` and do NOT transfer automatically; fresh regression
evidence is held on THIS candidate:
- CR-EBS-001 (complete mandatory transport binding, now STRENGTHENED
  by the runtime-gate descriptor dimension): cross-binding suites;
- CR-EBS-002 (one-shot: process-bound grant, O_EXCL, exact-object
  grant, irreversible spend, fsync-before-exec, no retry/reset/mint):
  `test_launch.py` 21/21;
- CR-EBS-003 (runtime self-identity, raw manifest pin, non-circular
  package pin, exact payload set/size/hash, changed-source +
  regenerated-manifest refusal): `test_selfcheck.py` 17/17;
- CR-EBS-REM-001 (strict event-package contract, package identity
  separate from cross-binding, full projection coverage,
  both-direction substitution refusals): `test_eventpackage.py` 63/63;
- CR-EBS-REM2-001 (exact non-negative int `files[].bytes`, bool/
  float/string/null/container/negative refused): `-k rem2_001` 16/16
  plus live-layer cases in `test_selfcheck.py`.

## 10. Deterministic validation (all commands run this session; the
final-set runs below are the FIRST complete final-set runs and their
results are reported exactly)

| Validation | Command (essence) | Result |
|---|---|---|
| RED defect reproduction | worktree at EXACT `63db66a…` | 1 passed (defect reproduced) |
| compileall | `python3 -m compileall bootstrap-supervisor/ebs` | exit 0 |
| Full battery | `uv run --no-project --with pytest --python 3.11 python -m pytest -q -p no:cacheprovider bootstrap-supervisor/tests` | **293 passed** (base 239) |
| Focused S1-001 gate-timing | `… pytest -q tests/test_resourcegate.py` | 29/29 |
| Event-package V2/cross-binding | `… tests/test_eventpackage.py` | 63/63 |
| CR-EBS-002 one-shot | `… tests/test_launch.py` | 21/21 |
| CR-EBS-003 self-identity | `… tests/test_selfcheck.py` | 17/17 |
| CR-EBS-REM2-001 row-type | `… -k rem2_001` | 16/16 |
| Binding schema incl. S1-001 matrix | `… tests/test_binding.py` | 81/81 |
| qh regression (source byte-unchanged) | `… pytest -q qualification-harness/tests` | 221/221 |
| git diff --check | — | clean |
| stdlib-only import scan | AST scan over `ebs/*.py` | NONE non-stdlib |
| provider/network/subprocess scan | grep over `bootstrap-supervisor/**` | no imports, no provider names, no skill invocation path |
| forbidden qh/skill reach scan | grep over production+tests | production clean (test-side boundary-enforcement tokens only) |
| credential/private-key scan | over all changed non-docs files | zero hits |
| protected trees | `git rev-parse HEAD:qualification-harness HEAD:skill` | `5b8d5e54…` / `c792933a…` EXACT, equal frozen target |
| zero provider/model/auditor execution | session statement + scans | ZERO (all children are repository fixtures) |

Development RED/GREEN iteration runs were preserved separately from
the final-set runs above; the final-set runs are the first complete
pass and include every prior-finding regression.

## 11. EBS package identities (old → new, recorded EXACTLY)

| Identity | Old (accepted `4448deea…`) | New (THIS candidate) |
|---|---|---|
| manifest_sha256 | `049c200771c7b85d39a9445b645d2ad8c27c521ddd18be7f6ce35a7a2016a88f` | `c09cb5a275edbab16531fe231cf6af1f12fc8a5a1a8516c7b430a6bf22e6056b` |
| package_sha256 | `d478a5013ede94ebd63870948594c0675914792ad1b8268708473366123ef9fd` | `4f330647eb677547a882ec61fee8abe283a6d99a044b00b9297444364656cf47` |
| rows | 21 | 23 (NEW `tests/fixtures/inert_resource_gate.py`, NEW `tests/test_resourcegate.py`) |
| implementation_base_commit | `dbe0dc5d…` | `63db66a3433f2d02a2fdc0745450ee017323ffc2` |

The new manifest is non-circular (package_sha256 independently
re-derived == recorded) with all byte counts exact non-negative ints.
NO old acceptance transfers to the regenerated package.

## 12. Production LOC / TCB growth (§18 disclosure)

1664 (Control-Room-accepted freeze, reconfirmed at `4448deea…`) →
**2035** = **+371**, classified:

```
NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE
```

Per-module delta: `binding.py` +68, `launch.py` +298, `__init__.py`
+5; `accounting.py`, `cli.py`, `custody.py`, `reportcustody.py`,
`statemachine.py` byte-unchanged. Per-function attribution
(function-level, mechanically derived):

- `binding.py`: `_safe_relpath` NEW +10; `parse_binding` +25 (frozen-
  PASS refusal + runtime-gate descriptor validation); remainder =
  module docstring + split constants (RUNTIME_GATES/
  RUNTIME_GATE_FIELDS/RESOURCE_GATE_RESULT_SCHEMA/PATH_SEGMENT_RE/
  TOP_LEVEL/V2 schema note) +33.
- `launch.py`: `open_runtime_gate` NEW +33, `_kill_and_reap` NEW +11,
  `_gate_child` NEW +26, `_run_runtime_gate` NEW +73,
  `_validate_resource_gate_result` NEW +58,
  `_execute_resource_gate` NEW +25, `validate_gates` +15,
  `verify_launcher` +5 (GATES_PASSED-only ordering),
  `Supervisor.__init__` +3 (held fd + exactly-once guard); remainder =
  module docstring + gate constants +49.

Why the growth is mechanically necessary: live runtime-gate execution
is REQUIRED to become part of the EBS authority boundary (verified-fd
open/hold/drift re-hash, a bounded fork/exec/poll/reap runner with a
timeout, strict result-envelope validation, and the durable
fresh-evidence record have no pre-existing implementation to reuse —
only the fd-exec/hash/strict-parse PRIMITIVES were reusable, and they
WERE reused; no second verifier, no second package walker, no schema
framework, no new dependency, no new production module, no daemon, no
plugin architecture). No meaningful security check was deleted.
`test_static.py`'s frozen bound was updated to the exact candidate
ceiling 2035 labeled `CANDIDATE_ONLY / NOT_CONTROL_ROOM_ACCEPTED` with
the prior accepted 1664 baseline PRESERVED verbatim in the test
history — history was NOT rewritten. NO claim of Control Room
acceptance of the new LOC is made.

## 13. Exact changed paths (this remediation)

Production (2): `ebs/binding.py`, `ebs/launch.py`. Package/status (3):
`MANIFEST.json`, `README.md`, `ebs/__init__.py`. Tests (4+2 new):
`tests/conftest.py`, `tests/test_binding.py`,
`tests/test_eventpackage.py`, `tests/test_static.py` (modified);
`tests/fixtures/inert_resource_gate.py`, `tests/test_resourcegate.py`
(NEW). Canonical (4): THIS report (NEW), `AUCDEV-CURRENT-STATE.md`,
`AUCDEV-BACKLOG.md`, `AUCDEV-ARCHITECTURE-SUMMARY.md` (bounded factual
status paragraph only). `ebs/accounting.py`, `ebs/cli.py`,
`ebs/custody.py`, `ebs/reportcustody.py`, `ebs/statemachine.py` and
`tests/test_accounting.py`, `tests/test_custody.py`,
`tests/test_launch.py`, `tests/test_report.py`,
`tests/test_selfcheck.py`, `tests/test_statemachine.py` are
byte-unchanged. Pre-existing smoke-fixture/smoke-fixture-103 gitlink
drift preserved unstaged, as at the base.

## 14. Route-readiness evidence gap — OUT OF SCOPE, recorded verbatim

During Control Room preparation of this remediation, a separate
evidence gap was observed: the adopted R1 design lists ROUTE READINESS
among mandatory pre-inference gates, while the current EBS
`REQUIRED_GATES` contains no separate route-readiness gate and
`launch.py` contains no route-readiness enforcement. This
authorization does NOT permit silently fixing that issue. Recorded
exactly as required:

```
CONTROL_ROOM_OBSERVED_OUT_OF_SCOPE_EVIDENCE_GAP =
ADOPTED_DESIGN_NAMES_ROUTE_READINESS_AS_MANDATORY_PRE_INFERENCE_GATE
/ CURRENT_EBS_HAS_NO_SEPARATE_ROUTE_READINESS_GATE
/ NOT_REMEDIATED_UNDER_S1_001_AUTHORITY
/ CONTROL_ROOM_DISPOSITION_REQUIRED
```

No `NETWORK_READINESS` gate was added, RESOURCE_GATE was NOT
reinterpreted as route readiness, the gap is NOT claimed closed, and
event readiness is NOT claimed. No final finding disposition is
assigned on behalf of the Control Room.

## 15. Boundaries held (zero-provider / zero-real-credential)

THIS TASK did NOT: build the real AUCDEV-023 event package; allocate
or instantiate a canonical event id; run GATE-W′ against a real
transport; run a networked provider client; call any Claude/Opus or
GPT/Codex inference; invoke `/audit-council`; read/hash/copy/export
real provider credentials; test real provider authentication; consume
any model engagement; or consume any future auditor attempt authority.
Synthetic local runtime-gate fixtures only. Real credentials = ZERO.
Zero provider/model/auditor executions. The previously granted S1
authorization remains operator-granted but PAUSED pending the fresh
Control Room readback of THIS candidate; S1 preparation has NOT
started.

## 16. Resulting state / implementer finding position

```
AUCDEV-023 = P1 / READY / NOT DONE
EBS_IMPLEMENTATION = GATE_TIMING_REMEDIATION_CANDIDATE
                     / AWAITING_FRESH_CONTROL_ROOM_READBACK
AUCDEV023-CR-EBS-S1-001 =
    REMEDIATION_IMPLEMENTED / AWAITING_CONTROL_ROOM_READBACK
AUCDEV023-CR-EBS-001 =
    PRIOR_CONTROL_ROOM_CLOSURE_ON_4448DEEA
    / REGRESSION_EVIDENCE_HELD
    / NEW_SHA_AWAITING_FRESH_CONTROL_ROOM_READBACK
AUCDEV023-CR-EBS-002 = (same as CR-EBS-001)
AUCDEV023-CR-EBS-003 = (same as CR-EBS-001)
AUCDEV023-CR-EBS-REM-001 = (same as CR-EBS-001)
AUCDEV023-CR-EBS-REM2-001 = (same as CR-EBS-001)
EVENT_PACKAGE_PREPARATION = AUTHORIZED_BY_OPERATOR / NOT_STARTED
                            / PAUSED_PENDING_GATE_TIMING_REMEDIATION_READBACK
BOOTSTRAP_EVENT = NOT_INSTANTIATED
GATE_W_PRIME = REQUIRED / UNPROVEN
REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION = UNPROVEN / EVENT_PREPARATION_GATE
MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY = 0
INDEPENDENT_AUDITOR_PROVENANCE_GATE = NOT_SATISFIED
INDEPENDENT_HARNESS_AUDIT =
    BLOCKED_PENDING_FRESH_GATE_TIMING_REMEDIATION_READBACK
    _AND_EVENT_PREPARATION
    _AND_SEPARATE_EXECUTION_AUTHORITY
qualification = NONE
installation = NONE
```

NO finding is claimed CLOSED on the future SHA. No event id is
allocated by this remediation. No backlog item becomes DONE.

NEXT ACTION EXACTLY ONE: INDEPENDENT CONTROL ROOM READBACK OF THE
AUCDEV-023 EBS GATE-TIMING REMEDIATION CANDIDATE — no event-package
preparation follows automatically from this publication.
