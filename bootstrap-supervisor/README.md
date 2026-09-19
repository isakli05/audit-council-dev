# AUCDEV-023 External Bootstrap Supervisor (EBS) — gate-timing remediation candidate

Bounded implementation of the operator-ADOPTED AUCDEV-023 auditor-bootstrap
governance architecture **R1 = CONTROLLERLESS / PROCESS-BOUND /
TARGET-INDEPENDENT / ONE-SHOT**, produced under the operator's 2026-09-19
bounded implementation authority, the 2026-09-19 bounded **EBS
remediation** authority (Control Room findings AUCDEV023-CR-EBS-001/-002/
-003; canonical remediation record:
`docs/chatgpt-project/AUCDEV-023-EBS-REMEDIATION-REPORT.md`), and the
2026-09-19 bounded **second EBS remediation** authority (finding
AUCDEV023-CR-EBS-REM-001; canonical record:
`docs/chatgpt-project/AUCDEV-023-EBS-SECOND-REMEDIATION-REPORT.md`), and
the 2026-09-19 bounded **narrow EBS manifest row-type remediation**
authority (finding AUCDEV023-CR-EBS-REM2-001; canonical record:
`docs/chatgpt-project/AUCDEV-023-EBS-NARROW-MANIFEST-TYPE-REMEDIATION-REPORT.md`),
and the 2026-09-19 bounded **EBS gate-timing remediation** authority
(finding AUCDEV023-CR-EBS-S1-001; canonical record:
`docs/chatgpt-project/AUCDEV-023-EBS-GATE-TIMING-REMEDIATION-REPORT.md`).

## What this is

- An **AUCDEV-023-specific minimal bootstrap TCB**: complete transport
  binding validation, a one-shot state machine, operator-custodied durable
  accounting with full binding-identity records, sealed credential
  custody, a verified-open-fd boundary-child launch mechanism, runtime
  package self-identity verification, **generic fail-closed frozen
  event-package verification with transport cross-binding (second
  remediation)**, generic report custody with a
  credential leak screen, and an inspection-only CLI.
- **A gate-timing remediation candidate awaiting a FRESH independent
  Control Room readback.** Not accepted, not trusted for any event.

## What this is NOT

- NOT Audit Council and NOT part of the installed skill runtime.
- NOT qualified; NOT installed; NOT execution-authorized.
- NO real provider/event support is authorized or implemented: no
  networked auditor boundary package exists here, no provider client is
  ever invoked, and no real credential is ever read.
- GATE-W′ remains REQUIRED / UNPROVEN. Real-client credential/tool
  isolation remains UNPROVEN / EVENT_PREPARATION_GATE. The bootstrap
  event is NOT instantiated; NO event package is prepared.

## Mandatory transport binding (complete adopted dimension set)

The frozen binding document (`ebs/binding.py`, strict fail-closed parse:
unknown/missing fields, wrong types, malformed digests, role-inconsistent
provider/adapter, mismatched target and attempt/output derivation all
refused) MUST carry EVERY adopted dimension (design §17):

`policy_id`, `event_id`, `auditor_role`, `attempt_id`,
`target` (exact frozen five-field identity), `prompt_contract_digest`,
`common_evidence_manifest_digest`, `boundary_launcher` {identity, sha256},
`auditor_identity` {provider_role, adapter_id, **executable_identity,
executable_sha256**}, **`sandbox_profile_id`**, **`tool_wrapper`**
{identity, sha256}**, **`ebs_package`** {manifest_sha256, package_sha256},
**`event_package`** {manifest_sha256, package_sha256}, `output_identity`
{kind, name}, `gate_evidence` (the 6 mandatory STATIC preparation PASS
gates incl. GATE-W′), and **`runtime_gates`** — the frozen RUNTIME
RESOURCE_GATE executable-artifact descriptor (see the gate-timing
section below).

Every dimension is mandatory, covered by `binding.digest`, mechanically
bound to the accounting store (attempt id AND digest equality), and
durably recorded at `CONSUMED_PRE_EXEC`. Swapping ANY dimension (an
unrelated launcher, sandbox profile, tool wrapper, or auditor executable)
changes the binding digest, so it cannot pass the declared frozen
event-package binding of the same attempt: the store refuses the digest
mismatch and record creation for an existing attempt fails closed.
Synthetic binding documents used by the zero-provider tests are built in
`tests/conftest.py` — no document builder exists in the production TCB.

## Frozen event-package cross-binding (CR-EBS-REM-001, second remediation)

`ebs/launch.py: verify_event_package` is executed by EVERY Supervisor
construction, BEFORE any gate can pass, immediately after the live EBS
self-identity verification and the Supervisor⇄store binding. The frozen
event package root is a **MANDATORY** `Supervisor` constructor input —
no default, no flag, no environment variable, no CLI bypass (the CLI
remains inspection-only).

**Versioned strict event-package manifest contract**
(`ebs/binding.py: EVENT_MANIFEST_SCHEMA` =
`AUCDEV-023-EVENT-PACKAGE-MANIFEST-V2`, advanced from V1 by the
S1-001 gate-timing remediation because the projection semantics
materially changed — `RESOURCE_GATE` left the frozen evidence set and
the runtime-gate descriptor became a bound security dimension; a V1
manifest is REFUSED, never silently accepted as equivalent): the
package's `MANIFEST.json`
parsed document has EXACTLY the key set `{schema, transport_binding,
files, package_sha256}` — unknown or missing keys, a wrong schema tag,
or duplicate/non-finite JSON are refused (the shared strict parser).
`files` rows and `package_sha256` follow the SAME non-circular package
identity construction as the EBS manifest above, and verification REUSES
`verify_package_identity` (no second package verifier): raw manifest
bytes against the binding-pinned `event_package.manifest_sha256`,
non-circular package identity against the binding-pinned
`event_package.package_sha256`, exact per-file byte size + SHA-256,
exact payload-set equality, missing/stale/unrecorded payload and
symlink refusal.  Strict row typing (AUCDEV023-CR-EBS-REM2-001, narrow
remediation): every `files[]` row's recorded `bytes` must be an EXACT
non-negative integer — `true`/`false`, floats (`1.0`), strings (`"1"`),
`null`, containers, and negative values are all refused at
manifest-row validation BEFORE tree traversal and before any gate; the
exact live size/SHA-256 comparison itself is unchanged.

**Non-circular cross-binding projection**: the manifest's
`transport_binding` field must equal `binding_projection(binding)` —
EVERY binding security dimension (policy id; event id; auditor role;
attempt id; the exact frozen five-field target; prompt-contract digest;
common-evidence manifest digest; boundary launcher identity+SHA-256;
auditor identity incl. provider role, adapter id, executable
identity+SHA-256; sandbox profile id; tool wrapper identity+SHA-256;
EBS package identity pair; output identity; the COMPLETE six-gate
preparation evidence set; the runtime-gate descriptor) — EXCEPT
`event_package` itself. The two sides are compared
as canonical JSON bytes (type-strict: JSON `true` ≠ `1`, `1.0` ≠ `1`).
The exclusion is what makes the construction non-circular: the
projection is covered by the event-package manifest/package identity,
while the event-package identity pair is pinned INDEPENDENTLY by the
binding and verified against the actual package bytes. No field is
verified by hashing itself.

**Consequences** (both directions are tested in
`tests/test_eventpackage.py`):

- A binding that remains internally valid but substitutes ANY component
  identity (launcher, sandbox, adapter, auditor executable, tool
  wrapper, prompt/evidence digests, gate evidence, a recombined
  event/attempt/output set) while RETAINING the same declared
  event-package identity is REFUSED (`EVENT_PACKAGE_PROJECTION_MISMATCH`)
  before `GATES_PASSED` — digest coverage of the binding document is
  never used as event-package membership proof.
- A regenerated, perfectly self-consistent event package whose manifest
  projection declares a different component — including a different
  frozen target — is REFUSED even when the binding's `event_package`
  pins are updated to the new package identity: package identity
  verification and component cross-binding are separate checks.

Synthetic event packages for the zero-provider tests are built in
`tests/conftest.py: make_event_package` (unmistakably inert temporary
trees). The REAL AUCDEV-023 event package is NOT authorized, NOT built,
NOT committed anywhere in this repository.

## Frozen-vs-runtime gate split (CR-EBS-S1-001, gate-timing remediation)

The six **STATIC preparation gates** (`PACKAGE_BINDING_IDENTITY`,
`COMMON_EVIDENCE_PARITY`, `IDENTITY_LINTER`, `BLINDNESS_MAP`,
`GATE_W_PRIME`, `REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION`) remain frozen
PASS evidence members, transport-bound exactly as before.

The **DYNAMIC `RESOURCE_GATE` is NOT frozen evidence** — a package-time
PASS would go stale before the separately authorized execution. The
binding instead freezes an exact **runtime-gate descriptor**:

```
runtime_gates = {"RESOURCE_GATE": {
    "identity": <safe frozen identity token>,
    "path": <safe event-package-relative path>,
    "sha256": <exact SHA-256 of the frozen artifact bytes>,
    "result_schema": "AUCDEV-023-RESOURCE-GATE-RESULT-V1"}}
```

The descriptor carries NO result and NO PASS. Its exact key set, safe
relative path (absolute/traversal/empty/dot segments refused), exact
SHA-256, and result-schema identity are type-strict fail-closed
validated at parse; a `RESOURCE_GATE` member inside `gate_evidence` is
refused outright (`GATE_EVIDENCE_RESOURCE_GATE_FORBIDDEN`). The
descriptor is covered by `binding.digest` and by the event-package
transport projection, so ANY substitution fails cross-binding.

**Runtime ordering** (every step fail-closed; there is no path from
PREPARED to GATES_PASSED without the live execution, and no second
execution in the same attempt):

1. live EBS package self-identity verification;
2. Supervisor⇄store attempt + binding-digest equality;
3. frozen event-package identity verification;
4. event-package transport-projection equality (schema V2);
5. runtime RESOURCE_GATE artifact identity verified from the ALREADY
   verified package tree (manifest-row membership, regular executable
   file, `O_NOFOLLOW` open, exact SHA-256) and the verified open fd
   HELD;
6. `validate_gates()` re-hashes the held fd immediately before
   execution (held-fd drift refused), then EXECUTES exactly that open
   fd — the SAME verified-fd `execveat(AT_EMPTY_PATH)` primitive the
   launcher path uses — exactly ONCE, bound to this attempt's
   event/role/attempt, with a clean minimal environment, NO credential
   fd inherited, no launch authority/custody plaintext exposed, and a
   bounded deterministic timeout (a hung gate is SIGKILLed and fails
   closed);
7. the fresh result is strictly validated (schema
   `AUCDEV-023-RESOURCE-GATE-RESULT-V1`: strict JSON, exact key set,
   exact event/role/attempt match with the binding, top-level PASS,
   EXACTLY three samples each explicitly PASS — a top-level PASS never
   overrides a failed sample, and PASS is never inferred from the exit
   code; size-bounded before acceptance; non-zero exit refused);
8. only then is `GATES_PASSED` durably appended — carrying the fresh
   evidence (`resource_gate_identity`, `resource_gate_sha256`,
   `resource_gate_result_schema`, the canonical validated result JSON
   plus its exact SHA-256 and byte size) — and the state machine
   transitions. Any failure at any point leaves authority unconsumed
   and terminalizes the attempt (`TERMINAL_PREEXEC_STOP`), with no
   same-attempt retry.

The gate itself is an EVENT-PACKAGE-SIDE trusted component: the EBS
implements NO resource thresholds or policy — it binds, verifies,
executes, validates, records, and fails closed. `RESOURCE_GATE`
execution is NOT a provider/model engagement. Launcher verification
exists only AFTER the GATES_PASSED transition.

## Runtime self-identity verification (CR-EBS-003)

`ebs/launch.py: verify_package_identity` is executed by EVERY Supervisor
construction — before `GATES_PASSED`, before consumption, before any
launch authority exists. It is not optional: it takes no CLI flag and
reads no environment variable; the production entry
(`verify_live_package_identity`) is parameter-free and verifies THE
EXECUTING package tree.

**Non-circular package identity construction** (no recursive self-hash):

- `manifest_sha256` = SHA-256 of the raw `MANIFEST.json` file bytes;
- `package_sha256` = the value recorded INSIDE `MANIFEST.json`, defined as
  SHA-256 of the canonical JSON (sort_keys, compact separators) of the
  manifest document **excluding its own `package_sha256` key** — it covers
  every identity-bearing manifest field (file rows, policy id, frozen
  target, status, ...) without hashing itself.

Both digests are pinned **independently** in the frozen binding
(`ebs_package`). Verification refuses (fail closed) on: manifest bytes
mismatching the pinned manifest identity; the declared package identity
not being self-consistent or mismatching the pinned package identity; any
files[] row whose recorded `bytes` is not an exact non-negative integer
(bool/float/string/null/container/negative — refused at row validation,
REM2-001); any
manifest-listed payload file whose live size or SHA-256 differs; any
missing payload; any unrecorded payload file; any symlink in the package
tree; malformed/non-object manifests. Therefore an attacker who modifies
live source AND regenerates a perfectly self-consistent manifest still
fails BOTH frozen pins. Package payload rule: every regular file under
the package root except `MANIFEST.json` itself and `__pycache__`
directories must be exactly the manifest row set — no missing payload, no
stale row, no unrecorded authority-bearing production payload.

## One-shot authority: structurally closed (CR-EBS-002)

- **No revival from durable records.** A writable accounting store exists
  only via `AccountingStore.create` in the ONE authority process for an
  attempt; creation uses `O_EXCL`, so an existing same-attempt record
  (any state, including PREPARED/GATES_PASSED) makes a new authority
  process fail closed. The old `attach` API and `RESUMABLE_STATES` are
  REMOVED (statically asserted absent). History is inspectable READ-ONLY
  via `inspect_accounting_record` (read-only opens; returns a plain
  summary dict with no fd, no append path, no resumable state).
- **Supervisor ⇄ store mechanical binding.** Before any gate/authority
  operation the supervisor requires `store.attempt_id ==
  binding.attempt_id` AND `store.binding_digest == binding.digest`.
- **Single-issuance, exact-object grant.** `LaunchGrant` carries NO state
  (empty `__slots__`); `execute()` accepts only the exact object returned
  by THIS supervisor's `consume()` (identity comparison), and `consume()`
  mints exactly one grant ever.
- **Irreversible spend.** The moment `execute()` begins (after
  precondition checks), `_spent` is set: a held-fd re-hash failure, fork
  failure, pre-child setup failure, or unreachable EXEC record leaves the
  authority permanently dead; the durable record gets a best-effort
  `TERMINAL` append with a reason (`CONSUMED_PRE_EXEC → TERMINAL`), and
  the event is never relabeled unconsumed. A replacement attempt requires
  NEW operator authority + NEW attempt id + NEW EBS process + NEW
  accounting/output identity. No reset/retry/mint API exists.

## Durable accounting (hash-chained JSONL)

Operator-custodied, mode 0600, fsync(file)+fsync(dir) per append,
hash-chained with seq/prev; tamper, truncation, seq gaps, non-canonical
lines, binding mismatch, symlink/FIFO records, unsafe custody dirs all
refused at read. The `CONSUMED_PRE_EXEC` record persists the COMPLETE
non-secret binding identity set (event, role, target trees, event-package
identity, boundary launcher id/hash, auditor executable id/hash,
provider/adapter, prompt digest, common-evidence digest, sandbox profile,
tool wrapper id/hash, output identity, EBS package identity, binding
digest) — no credential or sensitive plaintext ever enters accounting.

## Credential custody, launch identity, report custody (unchanged areas)

Preserved from the accepted implementation readback: pipe/fully-sealed
memfd sources only; `PR_SET_DUMPABLE=0` before any plaintext read; four
seal custody memfd; credential plaintext absent from argv/env/log/hash/
accounting; fixed fd-3 inheritance with unintended fds closed; verified
open-fd launcher (`O_NOFOLLOW`, regular-file check, hash-the-open-fd,
`execveat(AT_EMPTY_PATH)` with ENOSYS-only fexecve fallback, pre-fork
held-fd re-hash); missing report stays MISSING; contaminated report not
frozen; clean report frozen 0444; absorbing terminal states.

## Layout

```
ebs/                production source (Python 3 stdlib only, Linux-only)
  binding.py        frozen-binding parser/validator + policy constants
                    + event-package manifest contract + binding projection
  statemachine.py   one-shot attempt state machine (absorbing terminals)
  accounting.py     hash-chained JSONL record + read-only inspection
  custody.py        non-dumpable sealed-memfd credential custody
  launch.py         package verification (EBS self + event package with
                    transport cross-binding) + Supervisor + verified-fd exec
                    + runtime RESOURCE_GATE open/hold/execute/validate
  reportcustody.py  report freeze + credential leak screen
  cli.py            inspection-only CLI (no authority operations)
tests/              deterministic zero-provider test battery
tests/fixtures/     inert synthetic local launch + runtime-gate fixtures
                    (NOT providers)
MANIFEST.json       per-file SHA-256 manifest + non-circular package identity
```

## Running

```
python3 -m compileall bootstrap-supervisor/ebs
uv run --no-project --with pytest --python 3.11 \
    python -m pytest -q bootstrap-supervisor/tests
```

Zero provider/model/auditor executions occur anywhere in this package or
its tests. Qualification: NONE. Installation: NONE.
