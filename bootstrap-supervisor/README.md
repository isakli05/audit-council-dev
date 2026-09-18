# AUCDEV-023 External Bootstrap Supervisor (EBS) — implementation candidate

Bounded implementation of the operator-ADOPTED AUCDEV-023 auditor-bootstrap
governance architecture **R1 = CONTROLLERLESS / PROCESS-BOUND /
TARGET-INDEPENDENT / ONE-SHOT** (governance adoption record:
`docs/chatgpt-project/AUCDEV-023-AUDITOR-BOOTSTRAP-GOVERNANCE-ADOPTION.md`,
2026-09-19), produced under the operator's 2026-09-19 bounded EBS
implementation authority.

## What this is

- An **AUCDEV-023-specific minimal bootstrap TCB**: binding validation, a
  one-shot state machine, operator-custodied durable accounting, sealed
  credential custody, a verified-open-fd boundary-child launch mechanism,
  generic report custody with a credential leak screen, and an
  inspection-only CLI.
- **An implementation CANDIDATE awaiting independent Control Room
  readback.** Not accepted, not trusted for any event.

## What this is NOT

- NOT Audit Council and NOT part of the installed skill runtime.
- NOT qualified; NOT installed; NOT execution-authorized.
- NO real provider/event support is authorized or implemented by this
  task: no networked auditor boundary package exists here, no provider
  client is ever invoked, and no real credential is ever read.
- GATE-W′ remains REQUIRED / UNPROVEN. Real-client credential/tool
  isolation remains UNPROVEN / EVENT_PREPARATION_GATE. The bootstrap
  event is NOT instantiated.

## Boundary between EBS implementation and the future event package

This package implements ONLY the supervisor side of the adopted design.
Everything networked/auditor-facing remains a FUTURE, separately
authorized event-package stage: the frozen networked boundary launcher,
tool-domain wrapper, GATE-W′ rehearsal, real adapter materialization,
and per-attempt execution authority. The `gate_evidence` block of the
binding is an ENFORCEMENT INTERFACE: the EBS requires mechanically bound
PASS evidence for every mandatory gate before `GATES_PASSED`, but no
test in this package claims any real gate (including GATE-W′) has been
proven — tests use deterministic synthetic evidence only.

## Hard properties (see `tests/`)

- Strict frozen-target binding (fail-closed on every mismatch/unknown).
- One-shot: primary launch authority is non-exportable process state +
  state-machine control flow; no token anywhere; no retry/reset/mint.
- Durable hash-chained accounting record, fsync'd before the child exec
  path exists; restart/tamper/duplicate refusal.
- Credential sources: operator pipe or fully sealed memfd ONLY; the EBS
  is non-dumpable before ingestion; custody is a four-seal memfd;
  transfer to the child happens only by fd inheritance at a fixed fd
  number; plaintext never enters argv/env/files/logs/hashes.
- Launcher identity preserved across verify→exec by executing the
  already-open verified fd (`execveat` with `AT_EMPTY_PATH`); a
  pathname re-open is never used; substitution is tested against.
- Report custody: missing stays missing (stdout/stderr never
  substituted), symlink/oversize refused, credential-contaminated
  reports rejected before any hash/persistence, clean reports frozen
  0444 with recorded SHA-256/size under operator custody.

## Layout

```
ebs/                production source (Python 3 stdlib only, Linux-only)
  binding.py        frozen-binding parser/validator + policy constants
  statemachine.py   one-shot attempt state machine (absorbing terminals)
  accounting.py     operator-custodied hash-chained JSONL attempt record
  custody.py        non-dumpable sealed-memfd credential custody
  launch.py         Supervisor + verified-open-fd child execution
  reportcustody.py  report freeze + credential leak screen
  cli.py            inspection-only CLI (no authority operations)
tests/              deterministic zero-provider test battery
tests/fixtures/     inert synthetic local launch fixtures (NOT providers)
MANIFEST.json       per-file SHA-256 manifest (self-excluded)
```

## Running

```
python3 -m compileall bootstrap-supervisor/ebs
uv run --no-project --with pytest --python 3.11 \
    python -m pytest -q bootstrap-supervisor/tests
```

Zero provider/model/auditor executions occur anywhere in this package or
its tests. Qualification: NONE. Installation: NONE.
