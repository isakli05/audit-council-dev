# AUCDEV-023 — Second Bounded EBS Remediation Report (AUCDEV023-CR-EBS-REM-001)

| Field | Value |
|---|---|
| Status | **`AUCDEV_023_EBS_SECOND_REMEDIATION = IMPLEMENTED_CANDIDATE / AWAITING_FRESH_CONTROL_ROOM_READBACK`** — the one remaining blocking finding of the EBS remediation readback is remediated at implementation/self-test strength ONLY. NOT Control Room accepted, NOT closed, NOT an event package, NOT execution-authorized, NOT qualified, NOT installed, and supporting NO real provider/event. Implementation claims are NOT audit truth. |
| Session class | BOUNDED ZERO-PROVIDER SECOND-REMEDIATION-IMPLEMENTATION SESSION — the selected implementation agent (Claude Code + GLM-5.3) is an IMPLEMENTER ONLY: NOT the Control Room, NOT an independent auditor, NOT authorized to independently close Control Room findings, NOT authorized to prepare or instantiate an event package, NOT authorized to run a real auditor/model/provider, NOT authorized to use real provider credentials, NOT authorized to invoke `/audit-council`, NOT authorized to qualify or install anything |
| Operator authority | Operator tasking (2026-09-19) authorizing ONLY: second bounded AUCDEV-023 EBS remediation for AUCDEV023-CR-EBS-REM-001 (EVENT_PACKAGE_COMPONENT_CROSS_BINDING_NOT_ESTABLISHED); deterministic zero-provider / zero-real-credential validation; implementation evidence publication; bounded canonical state/backlog/report updates for this implementation transition. No other authority is implied or exercised. |
| Exact implementation base | `a9bbdea7aeebfc475b7042410943f32fccbe5e83` (tree `fe694a34bdf839a287b2ad0d168cbb2ec477c69c`; sole parent `7911f0576bec23cf4638665a667b160e61dd90a9`; bootstrap-supervisor subtree `753e9bc18e4cf297b43408d1877e77f6539de7cf`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this session's bootstrap (ls-remote + fetch) and re-resolved immediately before staging. THIS second-remediation publication is the sole commit ahead of that base. |
| Governing records read at the exact base | CURRENT-STATE, BACKLOG, PROJECT-UPDATE-PROTOCOL, CONTROL-ROOM-RUNBOOK, the EBS REMEDIATION-READBACK (canonical governing record for CR-EBS-REM-001), the EBS REMEDIATION-REPORT, the EBS IMPLEMENTATION-READBACK, the governance ADOPTION record, the design REVISION record, the design-revision READBACK record, `bootstrap-supervisor/MANIFEST.json`, `README.md`, the complete `bootstrap-supervisor/ebs/**` source, and the complete `bootstrap-supervisor/tests/**` suite |
| Frozen target (unchanged, EXACT) | `isakli05/audit-council-dev` @ `d4d584ffa47ad2848268ba947247f81a845b2322` (root tree `1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7`; qualification-harness tree `5b8d5e5465923740470ff63ed9b8683f257a3787`; skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`) — AUDIT SUBJECT / EVIDENCE ONLY, verified EXACT at bootstrap and pre-commit; `git diff a9bbdea… -- qualification-harness skill` EMPTY; both trees given NO bootstrap authority |
| Qualification / installation | qualification NONE / installation NONE |

Claim classes: `OBSERVED_FACT` (mechanically observed this session),
`FINDING_TEXT` (the Control Room readback's recorded requirements,
quoted), `IMPLEMENTED` (what this candidate's code does, evidenced by
the deterministic battery). CR-EBS-REM-001 and the CR-EBS-001 remainder
remain OPEN until a FRESH independent Control Room readback of THIS
publication says otherwise.

---

## 1. The finding and the required remediation strength (FINDING_TEXT)

Governing record `AUCDEV-023-EBS-REMEDIATION-READBACK.md` §7 (recorded
verbatim by the Control Room):

```
AUCDEV023-CR-EBS-REM-001
EVENT_PACKAGE_COMPONENT_CROSS_BINDING_NOT_ESTABLISHED
/ OPEN / BLOCKING
```

Required strength (readback §7, recorded verbatim):

> Implement a generic, fail-closed EBS mechanism that mechanically
> verifies a frozen event-package manifest against the binding BEFORE
> GATES_PASSED. […] It must NOT prepare the real AUCDEV-023 event
> package. At minimum, the mechanism must ensure that the frozen
> event-package identity cryptographically binds and the EBS
> mechanically cross-checks the declared: event id; role; attempt;
> target; prompt digest; common evidence digest; output identity;
> boundary launcher identity/hash; sandbox/profile identity; credential
> adapter/provider role; auditor executable identity/hash/version;
> tool-domain wrapper identity/hash; relevant gate/binding identities;
> EBS package identity where the adopted event-package contract includes
> it. An arbitrary valid component substitution while retaining the same
> declared event-package identity must fail closed. Do NOT merely add
> another opaque digest field. Do NOT treat Binding.digest itself as
> proof of event-package membership.

## 2. Exact event-package manifest schema (IMPLEMENTED)

Versioned strict contract in `ebs/binding.py`, enforced by
`ebs/launch.py::verify_event_package`:

```
EVENT_MANIFEST_SCHEMA = "AUCDEV-023-EVENT-PACKAGE-MANIFEST-V1"
EVENT_MANIFEST_KEYS  = frozenset({"schema", "transport_binding",
                                  "files", "package_sha256"})
```

A frozen event package's `MANIFEST.json` parsed document must have
EXACTLY that key set:

- `schema` — must equal `EVENT_MANIFEST_SCHEMA` exactly (version pin;
  unknown versions refused, no negotiation, no plugin surface);
- `transport_binding` — must equal the binding projection (§4);
- `files` — package rows `{path, bytes, sha256}`, verified by the SAME
  package verifier as the EBS manifest (§3);
- `package_sha256` — the non-circular package identity (§3).

Fail-closed parsing is the SHARED strict loader (`binding.strict_loads`):
duplicate JSON keys refused, non-finite constants (NaN/Infinity)
refused, non-UTF-8 / non-JSON refused, non-object refused. Missing
mandatory key, unknown security-relevant key, wrong schema tag: all
refused. Malformed digests and unsafe/absent component identities cannot
pass because projection comparison is exact equality against values that
`parse_binding` already fully validated (a malformed value on either
side cannot equal a validated value on the other). This is a small
explicit versioned schema, NOT a generic extensible metadata/plugin
schema.

## 3. Non-circular package-identity construction (IMPLEMENTED, reused)

The event package uses the SAME construction the Control Room accepted
for the EBS package (CR-EBS-003 closure, unchanged semantics):

- `manifest_sha256` = SHA-256 of the raw `MANIFEST.json` bytes;
- `package_sha256` = the value recorded INSIDE the manifest = SHA-256 of
  the canonical JSON (sort_keys, compact separators) of the manifest
  document EXCLUDING its own `package_sha256` key — it covers every
  identity-bearing manifest field, including `transport_binding`, file
  rows, and the schema tag, without hashing itself.

`verify_event_package` REUSES `verify_package_identity` (no second
package verifier) and therefore inherits, for the event package:
raw-manifest-byte pin verification, non-circular package-identity
self-consistency + pin verification, exact per-file byte size + SHA-256,
exact payload-set equality (missing payload / stale row / unrecorded
payload / symlink or special payload / symlinked directory refusal).
The only change to the shared verifier: manifest parsing now uses
`strict_loads` (duplicate-key / non-finite refusal — a strengthening
that cannot affect any previously accepted valid package) and the
parsed manifest document is returned as `"document"` for the
projection check.

## 4. Exact Binding projection definition (IMPLEMENTED)

`ebs/binding.py`:

```
PROJECTION_FIELDS = every TOP_LEVEL dimension except "event_package"
binding_projection(binding) = {name: getattr(binding, name)
                               for name in PROJECTION_FIELDS}
```

Concretely the projection carries: `policy_id`, `event_id`,
`auditor_role`, `attempt_id`, `target` (exact frozen five-field
identity: repository / commit / root tree / qh tree / skill tree),
`common_evidence_manifest_digest`, `prompt_contract_digest`,
`boundary_launcher` {identity, sha256}, `auditor_identity`
{provider_role, adapter_id, executable_identity, executable_sha256},
`sandbox_profile_id`, `tool_wrapper` {identity, sha256}, `ebs_package`
{manifest_sha256, package_sha256}, `output_identity` {kind, name}, and
the COMPLETE `gate_evidence` record set (every mandatory gate's status,
evidence digest, size, role, attempt).

**Intentional exclusion — exactly one field**: `event_package`
(the manifest/package identity pair of the event package itself). Why:
including it would make the package identity participate in proving
itself (circular). Instead the binding pins `event_package`
INDEPENDENTLY and §3 verifies the ACTUAL package bytes against those
pins, while the projection (covered by the package identity) proves
that the components the binding declares are the components the package
declares. `Binding.digest` is never used as event-package membership
proof anywhere.

Comparison is EXACT STRUCTURAL EQUALITY over canonical JSON bytes
(`canonical_bytes` on both sides, sort_keys + compact separators) —
type-strict (JSON `true` ≠ `1`, `1.0` ≠ `1`, `"1"` ≠ `1`), so a
Python-level equality quirk cannot admit a type-confused projection.

## 5. Startup / gate ordering (IMPLEMENTED)

`Supervisor.__init__(binding, store, event_package_root)` executes, in
order, failing closed at each step before any gate or authority
operation is reachable:

1. `verify_live_package_identity(binding)` — live EBS package bytes vs
   the binding's `ebs_package` pins (unchanged CR-EBS-003 mechanics);
2. store binding — exact `store.attempt_id == binding.attempt_id` AND
   `store.binding_digest == binding.digest` (unchanged CR-EBS-002
   mechanics);
3. `verify_event_package(event_package_root, binding)` — event-package
   identity against the binding's `event_package` pins (§3);
4. event-package transport-projection equality with the binding (§4);
5. only then does a Supervisor object exist that is capable of
   `validate_gates()` → `GATES_PASSED`.

The event-package root is a REQUIRED constructor argument: no default
value exists (statically asserted in the battery), non-path inputs are
refused (`SUPERVISOR_REQUIRES_EVENT_PACKAGE_ROOT`), and there is no
flag, environment variable, CLI command, or test-only production bypass
(the inspection-only CLI is unchanged and authority-token-free). The
ordering is mechanically pinned by tests: wrong EBS pins + nonexistent
package root → EBS refusal; store mismatch + nonexistent package root →
store refusal; valid EBS + valid store + identity-failing package →
identity refusal even when the projection ALSO mismatches.

## 6. Finding → source change → test/evidence mapping (IMPLEMENTED)

| Requirement (tasking §5) | Implementation | Evidence |
|---|---|---|
| A. versioned strict manifest contract, fail closed (missing/unknown key, wrong type, malformed digest, unsafe identity, malformed package identity, duplicate JSON keys) | `ebs/binding.py` contract constants + shared `strict_loads`; `ebs/launch.py::verify_event_package` exact-key/schema checks; projection equality against parser-validated values | `test_eventpackage.py` schema negatives (4) + duplicate-key negative; evidence 03/03b |
| B. independent event-package identity; reuse accepted package verification mechanics; raw manifest digest, non-circular package identity, per-file size+SHA-256, payload-set equality, missing/stale/unrecorded/symlink refusal | `verify_event_package` calls the UNCHANGED `verify_package_identity` against `binding.event_package` pins; `Binding.digest` never used as membership proof | package-identity negatives (8); evidence 03 |
| C. non-circular cross-binding projection covered by the package identity, no recursive self-hash | `PROJECTION_FIELDS` = TOP_LEVEL − event_package; projection lives INSIDE the manifest (covered by §3 identity); binding independently pins the package identity pair | `test_projection_covers_every_dimension_except_event_package`; §3/§4 above |
| D. required cross-checked dimensions (all of them, via one structural equality) | `binding_projection` + canonical-byte comparison covers policy/event/role/attempt/target(5)/prompt/common-evidence/output/launcher(id+sha)/sandbox/auditor(provider+adapter+executable id+sha)/tool wrapper(id+sha)/COMPLETE gate evidence/EBS package pair | the 12-case BINDING→PACKAGE matrix asserts per-dimension refusals with parse-validity proven first |
| E. component substitution under the same declared event-package identity fails closed BEFORE GATES_PASSED, from cross-binding (not binding-syntax refusal) | projection mismatch refusal; every matrix case first proves `parse_binding` SUCCEEDS and the pins are UNCHANGED, then asserts `EVENT_PACKAGE_PROJECTION_MISMATCH` and durable record still `PREPARED` | `test_same_package_identity_component_substitution_refused[12 cases]` |
| F. both directions: regenerated manifest + updated pins still refused; package identity ≠ component cross-binding | regenerated self-consistent package with one changed projection component (or missing/unknown projection field), `event_package` pins updated, binding component unchanged → refused | `test_regenerated_package_projection_mismatch_refused[8 cases]` incl. target-commit |
| §6 startup ordering + mandatory input + no bypass | §5 above; ordering pinned by dedicated tests; signature has no default (static assert); no env/flag surface (production-wide AST scan unchanged) | ordering/mandatory tests (4); evidence 09/10 |
| §7 generic interface only; synthetic/inert fixtures; no real event package | production interface = a required package root PATH for generic verification; synthetic builder lives ONLY in `tests/conftest.py::make_event_package` (unmistakable marker `EBS-SYNTHETIC-INERT-EVENT-PACKAGE-FIXTURE-NOT-A-REAL-EVENT-PACKAGE-…`); no real transport frozen, no historical real package copied, no provider config materialized, no networked boundary, no GATE-W′, no real credential | `test_event_package_fixture_is_unmistakably_synthetic`; credential scan (evidence 11); zero-provider attestation §11 |
| §8 preserve CR-EBS-002/-003 mechanics + all held invariants | CR-EBS-002 one-shot matrix and CR-EBS-003 self-identity matrix re-run unchanged in meaning (only constructor arity updated in tests); `custody.py`/`reportcustody.py`/`statemachine.py`/`accounting.py` BYTE-UNCHANGED | evidence 04 (21/21), 05 (15/15), 02 (223/223) |

## 7. Positive and complete negative matrix (OBSERVED_FACT)

`tests/test_eventpackage.py` — 41 tests, all PASS:

- POSITIVE (2): exact synthetic package + exact binding → Supervisor
  constructs and `GATES_PASSED` is reached; full path through
  `consume()` → `CONSUMED_PRE_EXEC`.
- PROJECTION CONTRACT (2): projection = exactly TOP_LEVEL −
  `event_package`; fixture unmistakably synthetic.
- PACKAGE IDENTITY (8): wrong manifest pin; wrong package pin; manifest
  byte mutation; payload mutation; missing payload; stale row
  (re-pinned, isolating the row-level check); unrecorded payload;
  symlinked payload — all refused.
- SCHEMA (4): unknown manifest key; missing manifest key; wrong schema
  tag (all with identity re-pinned, so refusal is the schema rule, not
  the digest); duplicate top-level JSON key refused even when the
  collapsed document is perfectly self-consistent and both pins match
  the poisoned bytes.
- BINDING→PACKAGE CROSS-BIND (13 = 12 + 1): with the SAME frozen
  event-package identity, internally-valid binding substitutions of —
  recombined event/attempt/output set; prompt digest; common-evidence
  digest (parity gate repaired); alternate allowed launcher identity;
  alternate valid launcher hash; alternate safe sandbox profile;
  alternate role-valid adapter; alternate auditor executable identity;
  alternate auditor executable hash; alternate tool-wrapper identity;
  alternate tool-wrapper hash; altered gate evidence — ALL refused with
  `EVENT_PACKAGE_PROJECTION_MISMATCH`, parse-validity asserted FIRST,
  durable record still `PREPARED` (BEFORE GATES_PASSED). EBS-package
  substitution is refused at the live self-verification layer (step 1)
  and is ALSO projection-covered (regenerated-package direction).
- PACKAGE→BINDING CROSS-BIND (8): regenerated self-consistent package
  with one changed projection component — launcher identity; sandbox
  profile; prompt digest; **different frozen target commit**; EBS
  package identity; gate evidence; missing projection field; unknown
  projection field — binding `event_package` pins UPDATED to the new
  package identity, binding component unchanged: ALL refused
  (`EVENT_PACKAGE_PROJECTION_MISMATCH`). Package identity verification
  and component cross-binding are thereby proven to be SEPARATE checks.
- ORDERING / MANDATORY (4): EBS self-identity first; store binding
  before event package; identity before projection within event
  verification; event-package root mandatory (no default, non-path
  refused).

No test contacts a provider; no network socket exists anywhere in the
battery (static scan).

## 8. Changed paths (complete inventory, this publication)

`bootstrap-supervisor/**` — 10 paths (9 modified + 1 new):
`MANIFEST.json` (regenerated: 21 rows, new identities, base commit,
status, task), `README.md` (second-remediation documentation),
`ebs/__init__.py` (version/status), `ebs/binding.py` (contract +
projection + public strict loader), `ebs/launch.py` (event-package
verification + Supervisor integration), `tests/conftest.py` (synthetic
event-package builder + fixtures), `tests/test_launch.py` (constructor
arity + regen of the one custom-doc case), `tests/test_selfcheck.py`
(constructor arity, two call sites), `tests/test_static.py` (LOC freeze
update with disclosure), NEW `tests/test_eventpackage.py`.
Byte-UNchanged: `ebs/accounting.py`, `ebs/cli.py`, `ebs/custody.py`,
`ebs/reportcustody.py`, `ebs/statemachine.py`, `tests/test_accounting.py`,
`tests/test_binding.py`, `tests/test_custody.py`, `tests/test_report.py`,
`tests/test_statemachine.py`, `tests/fixtures/*`.
Canonical records: NEW THIS report + bounded CURRENT-STATE + BACKLOG
updates + the bounded factual AUCDEV-023 implementation-status
paragraph in ARCHITECTURE-SUMMARY. NOT modified:
`qualification-harness/**`, `skill/**` (trees `5b8d5e54…` /
`c792933a…` unchanged and equal to the frozen target), the runbook, the
update protocol, the governance adoption/design/design-revision/readback
records, the EBS implementation report + implementation readback, the
EBS remediation report + remediation readback (append-only, untouched),
`AUCDEV-QUALIFICATION-HISTORY.md` (no qualification/installation event),
historical AUCDEV-010 records, Project Instructions, the frozen
`d4d584ff…` target. Pre-existing unrelated working-tree state
(`smoke-fixture` / `smoke-fixture-103` gitlink drift, untracked evidence
directories) preserved unstaged and untouched.

## 9. Production LOC (OBSERVED_FACT — NEW_TCB_GROWTH disclosed)

- Before (base `a9bbdea…`, the Control-Room-frozen 1571): **1571**
  physical lines (`wc -l bootstrap-supervisor/ebs/*.py`).
- After (this second remediation): **1664** physical lines, same
  counting method (binding 320, statemachine 74, accounting 235,
  custody 211, launch 611, reportcustody 118, cli 75, `__init__` 20).
- Delta: **+93**, classified:

```
NEW_TCB_GROWTH / AWAITING_CONTROL_ROOM_ACCEPTANCE
```

Function-level attribution (exact):
- `ebs/binding.py` 286 → 320 (+34): module docstring +4;
  `EVENT_MANIFEST_SCHEMA`/`EVENT_MANIFEST_KEYS`/`PROJECTION_FIELDS`
  contract block +13; `strict_loads` docstring +2 (rename
  `_strict_loads` → public `strict_loads`; parsing semantics
  UNCHANGED); NEW `binding_projection()` +15 (incl. docstring).
- `ebs/launch.py` 557 → 611 (+54): module docstring +5; `.binding`
  import +4; `verify_package_identity` strict-parse + document return
  (+3 net; duplicate-key/non-finite refusal is a strict STRENGTHENING
  of the accepted verifier — no accepted semantic altered); NEW
  `verify_event_package()` +38 (incl. docstring); `Supervisor`
  docstring +6; `Supervisor.__init__` mandatory event-package input +
  verification call +6 (net of the same-length store checks).
- `ebs/__init__.py` 15 → 20 (+5): version/status docstring.
- All other production modules BYTE-UNCHANGED.

Why mechanically necessary: the finding demands a NEW verification
boundary — a versioned manifest schema, a projection definition, a
verifier, and a mandatory startup integration — none of which existed
in any form (that absence IS the finding). Alternatives considered and
rejected: (a) a second standalone package verifier for event packages —
rejected as TCB duplication; the accepted verifier is REUSED; (b)
per-dimension one-off comparisons (~20 bespoke checks) — rejected: the
single structural projection equality is smaller AND stronger; (c)
hashing the projection into an opaque digest field — explicitly
forbidden by the finding; (d) removing docstrings/comments that
document the new security boundary to approach 1571 — rejected for the
same reviewability reasons the prior remediation recorded. Further
compression would require one-lining security-relevant code or gutting
the contract documentation. The battery now enforces an EXACT freeze at
1664 (`test_static.py::SECOND_REMEDIATION_LOC_BOUND = 1664`): ANY
further growth, even one line, fails the suite. The fresh Control Room
readback may accept, reject, or direct reduction; no acceptance is
presumed. The prior 1571 freeze was NOT standing authority for growth;
this +93 is submitted for acceptance, not assumed.

## 10. Manifest / package identity (OBSERVED_FACT)

Regenerated `MANIFEST.json`: 21 payload rows (20 prior + NEW
`tests/test_eventpackage.py`), per-file SHA-256 + byte size, policy id,
frozen target, `implementation_base_commit a9bbdea…`, status
`SECOND_REMEDIATION_CANDIDATE / AWAITING_FRESH_CONTROL_ROOM_READBACK`,
and the non-circular `package_sha256`. Shipped identities:

- manifest_sha256: `4946c9b6d1acb12dcc84f12e09949829064737c0ceceb3418c270f1753f9e1fe`
- package_sha256: `01ee6f5f9099b1ae0bf246f5f728452e7557982eb98c9d99a6f29232ada924ba`

Independent static drift recompute: 21/21 rows match shipped bytes,
sets equal, package identity self-consistent, `RESULT=NO_DRIFT`
(evidence 13). Generator preserved at
`aucdev023-ebs-second-remediation-evidence/gen-manifest.py` (evidence
tree only, untracked).

## 11. Deterministic validation (OBSERVED_FACT — all zero-provider)

| # | Check | Command / method | Result |
|---|---|---|---|
| 1 | compile | `python3 -m compileall bootstrap-supervisor/ebs` | exit 0 |
| 2 | full deterministic battery | `uv run --no-project --with pytest --python 3.11 python -m pytest -q bootstrap-supervisor/tests` | **223 passed, 0 failed** (binding 64, eventpackage 41, accounting 24, launch 21, statemachine 20, custody 17, selfcheck 15, static 12, report 9; baseline was 182) |
| 3 | focused CR-EBS-REM-001 suite | `pytest -q tests/test_eventpackage.py` | **41 passed** (node inventory in evidence 03b) |
| 4 | focused CR-EBS-002 one-shot regressions | `pytest -q tests/test_launch.py` | **21 passed** |
| 5 | focused CR-EBS-003 self-identity regressions | `pytest -q tests/test_selfcheck.py` | **15 passed** |
| 6 | qh regression (unchanged source) | `pytest -q qualification-harness/tests` | **221 passed, 0 failed** (24.8 s) |
| 7 | whitespace | `git diff --check` (+ staged) | clean |
| 8 | production LOC recount | `wc -l` + splitlines (same method as static test) | 1664 / 1664 |
| 9 | runtime import scan | AST top-level imports over `ebs/*.py` | stdlib + package-relative ONLY |
| 10 | forbidden qh/skill/runtime reach scan | greps over production | no qualification-harness/qh/skill reference, no sys.path manipulation |
| 11 | credential leak scan | SYNTH literal + marker + secret-token grep | synthetic literal ONLY in `tests/conftest.py`; event-package marker ONLY in tests; no secret material in production |
| 12 | CLI smoke | `validate-binding` ok exit 0; tampered sandbox id REFUSED exit 2; 0 authority tokens in cli.py | as expected |
| 13 | manifest static drift | independent recompute | NO_DRIFT; identity self-consistent |
| 14 | synthetic event-package positive/negative cross-binding matrix | test_eventpackage (§7) | 41/41 |
| 15 | changed-path inventory | git status/diff vs base | exactly §8 |
| 16 | protected trees | rev-parse + diff vs base / frozen target | qh `5b8d5e54…` / skill `c792933a…` unchanged, clean, equal frozen `d4d584ff…` target |

Evidence preserved under `aucdev023-ebs-second-remediation-evidence/`
(untracked, non-secret, mirrored into the handoff archive).

## 12. Zero-provider / zero-real-credential attestation (exact strength)

Mechanically enforced/observed THIS session: the static battery asserts
no `claude`/`codex` token, no `/audit-council` invocation token, no
socket/ssl/http/urllib/requests/subprocess/asyncio import anywhere
under `bootstrap-supervisor/**.py`; production imports
stdlib-allowlisted only; no qh/skill reach; the ONE synthetic
credential literal exists only in `tests/conftest.py`; every launched
child is `tests/fixtures/inert_boundary_launcher_{a,b}.py` (marker
`EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER`); every event
package is an unmistakably synthetic temporary tree (marker
`EBS-SYNTHETIC-INERT-EVENT-PACKAGE-FIXTURE-NOT-A-REAL-EVENT-PACKAGE-…`).
Provider/model/auditor/frontier executions = **ZERO**; real credentials
= **ZERO**; `/audit-council` = NOT invoked. Honest limit (unchanged):
unit tests cannot prove absence of all host networking history; the
attestation is the enforced scan + observed execution set above,
nothing stronger.

## 13. Preserved prior invariants — non-regression (IMPLEMENTED)

CR-EBS-002 one-shot mechanics: no `RESUMABLE_STATES`; no
`AccountingStore.attach`; no Supervisor attach/revival; `O_EXCL`
duplicate-attempt refusal; read-only `inspect_accounting_record`;
store attempt == binding attempt and store binding digest == binding
digest mechanical checks (both re-run in the new startup order BEFORE
event verification); exact-object `LaunchGrant`; single issuance;
irreversible launch-spent guard; post-consumption failures
terminalize and can never revive authority. CR-EBS-003 mechanics:
mandatory live EBS self-verification in the startup path; binding-pinned
raw manifest identity; binding-pinned non-circular package identity;
exact payload-set verification; changed-source + regenerated-manifest
refusal; no production bypass. All other held readback invariants:
controllerless authority path; target independence from qh/skill
runtime; exact frozen target constants; verified-open-fd launcher,
O_NOFOLLOW, regular-file verification, hash-the-already-open-fd, no
pathname re-open, `execveat(AT_EMPTY_PATH)` with ENOSYS-only fexecve
fallback, held-fd rehash before fork; `PR_SET_DUMPABLE=0` before
credential plaintext read; pipe/fully-sealed-memfd sources only; four
seals; credentials absent from argv/env/log/hash/accounting;
constrained inherited FDs; missing report stays MISSING; stdout/stderr
never substituted; contaminated report not frozen; clean report 0444;
terminal states absorbing; Python stdlib + Linux kernel primitives
only; no qh imports; no plugin/extension system; no daemon/network
service; inspection-only CLI. `ebs/accounting.py`, `ebs/cli.py`,
`ebs/custody.py`, `ebs/reportcustody.py`, `ebs/statemachine.py` are
byte-unchanged from `7911f057…`/`a9bbdea…`.

The prior Control Room CLOSURES of CR-EBS-002 and CR-EBS-003 on
`7911f057…` do NOT transfer to this new SHA; this publication holds
regression evidence at implementer strength and records:

```
AUCDEV023-CR-EBS-002 = PRIOR_CONTROL_ROOM_CLOSURE_ON_7911F057
                       / REGRESSION_EVIDENCE_HELD_BY_IMPLEMENTER
                       / AWAITING_FRESH_CONTROL_ROOM_READBACK_ON_NEW_SHA
AUCDEV023-CR-EBS-003 = PRIOR_CONTROL_ROOM_CLOSURE_ON_7911F057
                       / REGRESSION_EVIDENCE_HELD_BY_IMPLEMENTER
                       / AWAITING_FRESH_CONTROL_ROOM_READBACK_ON_NEW_SHA
```

## 14. Deviations, residuals, unresolved risks (honest record)

1. **NEW_TCB_GROWTH +93** (1571 → 1664) — full analysis and
   alternatives in §9; flagged for the fresh Control Room readback;
   exact freeze at 1664 enforced by the battery.
2. `verify_package_identity` manifest parsing switched to the shared
   strict loader (duplicate-key + non-finite refusal) and the parsed
   document is returned. This is a strengthening of the accepted
   verifier (no valid previously-accepted package is affected; the
   shipped manifest and all synthetic packages parse identically);
   recorded as a deliberate change, not a silent one.
3. `Supervisor.__init__` arity changed (mandatory third argument).
   Any external two-argument caller now fails loudly; no such caller
   exists in the repository (CLI is inspection-only and never
   constructs a Supervisor).
4. `test_static.py` LOC bound updated to the new exact freeze 1664
   with the growth disclosure (§9); this is a bound ENCLOSURE at the
   new number, not a relaxation of any semantic check.
5. Same-UID host residual (unchanged): any same-UID process can
   SIGKILL the EBS (denial only); operator/root can rewrite accounting
   or the live tree — the runtime checks' pins live in the frozen
   binding document, whose integrity is operator custody.
6. Child env may gain `LC_CTYPE` (PEP 538 C-locale coercion) —
   interpreter-injected, non-secret, disclosed (unchanged).
7. `fexecve` fallback exercised only under ENOSYS (not present on this
   host; execveat x86_64 322 exercised) — unchanged.
8. The binding's gate evidence remains an ENFORCEMENT INTERFACE over
   declared PASS evidence; this remediation binds the DECLARED evidence
   identities into the event-package projection — it does not and
   cannot prove any future gate evidence artifact sound; that remains
   the readback's/GATE-W′'s role.
9. Unresolved (out of scope, unchanged): GATE-W′ REQUIRED/UNPROVEN;
   real-client credential/tool isolation UNPROVEN /
   EVENT_PREPARATION_GATE; independent auditor provenance gate
   NOT_SATISFIED; host-netns exposure residual stands at design
   strength.

## 15. State after this publication

```
AUCDEV-023                                = P1 / READY (NOT DONE)
EBS_IMPLEMENTATION                        = SECOND_REMEDIATION_CANDIDATE
                                            / AWAITING_FRESH_CONTROL_ROOM_READBACK
AUCDEV023-CR-EBS-001                      = REMEDIATION_IMPLEMENTED
                                            / AWAITING_CONTROL_ROOM_READBACK
AUCDEV023-CR-EBS-REM-001                  = REMEDIATION_IMPLEMENTED
                                            / AWAITING_CONTROL_ROOM_READBACK
AUCDEV023-CR-EBS-002                      = PRIOR_CONTROL_ROOM_CLOSURE_ON_7911F057
                                            / REGRESSION_EVIDENCE_HELD
                                            / NEW_SHA_AWAITING_FRESH_CONTROL_ROOM_READBACK
AUCDEV023-CR-EBS-003                      = PRIOR_CONTROL_ROOM_CLOSURE_ON_7911F057
                                            / REGRESSION_EVIDENCE_HELD
                                            / NEW_SHA_AWAITING_FRESH_CONTROL_ROOM_READBACK
INDEPENDENT_HARNESS_AUDIT                 = BLOCKED_PENDING_FRESH_SECOND_EBS_REMEDIATION_READBACK
                                            _AND_EVENT_PREPARATION
                                            _AND_SEPARATE_EXECUTION_AUTHORITY
GATE_W_PRIME                              = REQUIRED / UNPROVEN
REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION     = UNPROVEN / EVENT_PREPARATION_GATE
EVENT_PACKAGE_PREPARATION                 = NOT_STARTED / NOT_AUTHORIZED
BOOTSTRAP_EVENT                           = NOT_INSTANTIATED
MODEL_ENGAGEMENTS_USED_UNDER_THIS_POLICY = 0
INDEPENDENT_AUDITOR_PROVENANCE_GATE       = NOT_SATISFIED
qualification                             = NONE
installation                              = NONE
```

`REMEDIATION_IMPLEMENTED / AWAITING_CONTROL_ROOM_READBACK` is the
implementer's disposition ONLY. CR-EBS-REM-001 (and the CR-EBS-001
remainder it blocks) is NOT closed, NOT Control-Room-accepted; no
acceptance from any earlier readback transfers to this or any future
SHA. The REAL event package is NOT prepared (only synthetic/inert
temporary fixtures exist, in tests only); no bootstrap event step is
taken; this remediation grants no execution authority of any kind.

Next action EXACTLY ONE: **INDEPENDENT CONTROL ROOM READBACK OF THE
AUCDEV-023 SECOND EBS REMEDIATION CANDIDATE.** Nothing follows
automatically.
