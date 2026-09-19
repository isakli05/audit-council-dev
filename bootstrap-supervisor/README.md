# AUCDEV-023 External Bootstrap Supervisor (EBS) — remediation candidate

Bounded implementation of the operator-ADOPTED AUCDEV-023 auditor-bootstrap
governance architecture **R1 = CONTROLLERLESS / PROCESS-BOUND /
TARGET-INDEPENDENT / ONE-SHOT**, produced under the operator's 2026-09-19
bounded implementation authority and the 2026-09-19 bounded **EBS
remediation** authority (Control Room findings AUCDEV023-CR-EBS-001/-002/
-003; canonical remediation record:
`docs/chatgpt-project/AUCDEV-023-EBS-REMEDIATION-REPORT.md`).

## What this is

- An **AUCDEV-023-specific minimal bootstrap TCB**: complete transport
  binding validation, a one-shot state machine, operator-custodied durable
  accounting with full binding-identity records, sealed credential
  custody, a verified-open-fd boundary-child launch mechanism, runtime
  package self-identity verification, generic report custody with a
  credential leak screen, and an inspection-only CLI.
- **A remediation candidate awaiting a FRESH independent Control Room
  readback.** Not accepted, not trusted for any event.

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
{kind, name}, `gate_evidence` (7 mandatory PASS gates incl. GATE-W′).

Every dimension is mandatory, covered by `binding.digest`, mechanically
bound to the accounting store (attempt id AND digest equality), and
durably recorded at `CONSUMED_PRE_EXEC`. Swapping ANY dimension (an
unrelated launcher, sandbox profile, tool wrapper, or auditor executable)
changes the binding digest, so it cannot pass the declared frozen
event-package binding of the same attempt: the store refuses the digest
mismatch and record creation for an existing attempt fails closed.
Synthetic binding documents used by the zero-provider tests are built in
`tests/conftest.py` — no document builder exists in the production TCB.

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
  statemachine.py   one-shot attempt state machine (absorbing terminals)
  accounting.py     hash-chained JSONL record + read-only inspection
  custody.py        non-dumpable sealed-memfd credential custody
  launch.py         package self-verification + Supervisor + verified-fd exec
  reportcustody.py  report freeze + credential leak screen
  cli.py            inspection-only CLI (no authority operations)
tests/              deterministic zero-provider test battery
tests/fixtures/     inert synthetic local launch fixtures (NOT providers)
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
