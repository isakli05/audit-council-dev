# bootstrap-authority — AUCDEV-023 PCH6-B PATH-B candidate-specific target-independent bootstrap authority

**Status: `IMPLEMENTATION_CANDIDATE_ONLY / NO_EXECUTION_AUTHORITY`.**
**qualification_claim: NONE.** This package is the Control Room
design-readback-accepted (2026-10-02, over the PATH-B transition
preparation at `78b5bc3`) NEW authority plane for a *future* fresh
independent audit of the frozen candidate target
`730d2b29f7c0e7d33af3451b6d9205ec27c143ed`. It is an implementation
candidate only: not readback-accepted, not execution-ready, and it has
NOT prepared an event package, instantiated the design event, granted
attempt authorities, or consumed any model engagement. The BA-RB-001 /
BA-RB-002 bounded source remediation (attempt-global O_EXCL claim;
gates before credential materialization), the BA-PREP-001 /
BA-PREP-002 bounded source remediation (binding-frozen output-custody
root and report source; caller path substitution refused fail-closed
before any authority action) and the BA-PREP-RB2-001 / RB2-002
follow-up bounded source remediation (binding-frozen custody
directory OBJECT identity st_dev/st_ino with the held-fd O_EXCL claim;
the authority-CREATED attempt-owned report sink with the
invocation-to-sink equality edge and held-fd snapshot acceptance) are
each implemented AS A REMEDIATION CANDIDATE — no Control Room finding
is closed by the implementer, and a fresh Control Room readback of
each remediation candidate is required before any event-package
preparation.

## What this package is

A deliberately minimal replacement authority TCB for the wholly NEW
PATH-B lineage: controllerless on the authority path, process-bound,
one-shot, stdlib-only, and strictly **target-independent** — it imports
NOTHING from, and derives no authority from, the audit target's
`bootstrap-supervisor/**` (AUDIT SUBJECT / READ-ONLY EVIDENCE ONLY),
`qualification-harness/**`, or `skill/**`. The candidate may only be
executed later in a credential-free non-authoritative audit/test domain
as subject matter. It contains **no substantive audit verdict logic**:
no PASS/FAIL verdicts, no finding scoring/closure, no qualification or
installation decisions, no auditor-output reconciliation.

## Layout (exactly thirteen package paths)

| Path | Kind |
|---|---|
| `MANIFEST.json` | strict non-circular self-identity manifest (generated last from final bytes) |
| `README.md` | this file |
| `bootstrap_authority/__init__.py` | NEW authority-specific |
| `bootstrap_authority/statemachine.py` | EXACT pre-target blob reuse |
| `bootstrap_authority/accounting.py` | bounded RB2 derivative of the pre-target blob |
| `bootstrap_authority/custody.py` | EXACT pre-target blob reuse |
| `bootstrap_authority/reportcustody.py` | bounded RB2 derivative of the pre-target blob |
| `bootstrap_authority/binding.py` | NEW authority-specific |
| `bootstrap_authority/runtime.py` | NEW authority-specific |
| `tests/conftest.py` | synthetic zero-provider fixtures |
| `tests/test_binding.py` | BA-13..BA-25 binding/gate-contract tests |
| `tests/test_runtime.py` | BA-26..BA-50 + BA-RB-001/BA-RB-002 + BA-PREP-001/BA-PREP-002 + BA-PREP-RB2-001/RB2-002 remediation regressions |
| `tests/test_static.py` | BA-01..BA-12, BA-51..BA-59 provenance/identity/governance tests |

No CLI, no provider adapters, no real event package, no credential
files, no model/client binaries.

## Source provenance (summary)

`statemachine.py` and `custody.py` are byte-for-byte the pre-candidate
EBS blobs at `068f5e29904f446bf832138fd64c8833b9037cb7` (pinned
per-file in `MANIFEST.json` `source_provenance` and re-verified at
every `BootstrapAuthority` construction):

- `statemachine.py` — blob `cf563d2178907e7666ce661b81ab1bf16fb71201`
- `custody.py` — blob `37e6b5bb4365c7b29ba3632fe95362d5a7e16c09`

`accounting.py` and `reportcustody.py` are bounded RB2 derivatives of
their exact pre-target blobs (BA-PREP-RB2-001/RB2-002: the narrow
held-fd object-custody primitives ONLY — `create_at`,
`create_report_sink`, `snapshot_held_sink`, `discard_held_sink` — with
the superseded pathname snapshot/discard staging primitives removed);
the derivation origin stays pinned per-file in `source_provenance`:

- `accounting.py` — derived from blob
  `03de6f663db283cf99f6a98e26e752a24457c52a`
- `reportcustody.py` — derived from blob
  `18f1cc600c684e520b72026e0b4cdf8ba6287cb9`

`__init__.py`, `binding.py`, and `runtime.py` are NEW
authority-specific source (`origin = THIS_BOUNDED_IMPLEMENTATION`).
Neither historical nor candidate `binding.py`/`launch.py` was copied
wholesale; the legacy EBS at `068f5e2` is REFERENCE_ONLY (its binding
pins the historical target `d4d584ff` and its launch boundary predates
the exact semantic report-target acceptance this authority implements
natively).

## Binding and identity model

`binding.py` parses ONE strict versioned binding document
(`AUCDEV-023-CAND730D2B29-BOOTSTRAP-AUTHORITY-BINDING-V1`) binding:
the PATH-B policy id, the design-reserved event identity
`AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01`, the exact
role/attempt pair (AUDITOR_A/-A-01 or AUDITOR_B/-B-01), the FULL
frozen target (repository, commit `730d2b29…`, root tree, REQUIRED
bootstrap-supervisor subtree, qualification-harness and skill trees,
remediation parent `068f5e2`), common-evidence/prompt-contract
digests, the governance-frozen auditor selection (Auditor A:
`claude-opus-5-5`/high CLAUDE_FIRSTPARTY; Auditor B:
`gpt-6.1-sol`/high CODEX_CHATGPT_OAUTH — no fallback/inherit/"auto"),
the boundary launcher / tool wrapper / dynamic gate / validator
descriptors, authority- and event-package identity pins, the exact
auditor invocation argv, and the bounded execution limits. Every
dimension is covered by `Binding.digest`. Eight STATIC gates are
frozen PASS evidence; the THREE DYNAMIC gates
(`CLIENT_SELECTION_PREFLIGHT` → `NETWORK_READINESS` → `RESOURCE_GATE`
last) exist only as executable descriptors executed fresh exactly
once — a package-time PASS for them cannot exist in a valid binding.

`runtime.py` enforces, inside the ONE public operation
`BootstrapAuthority.run_attempt(credential_source_fd, launcher_path,
auditor_executable_path, report_staging_path, output_root)`:
self-identity of the executing package (both pinned identities, live
per-file equality, payload-set equality, semantic values — no
caller-provided root), event-package identity + transport projection,
a **binding-frozen output-custody/report-source identity gate**
(BA-PREP-001/BA-PREP-002: the binding's `output_identity` freezes the
attempt's authoritative `custody_root` and `report_source` as
canonical absolute host paths; caller-supplied `output_root` /
`report_staging_path` arguments that do not equal the frozen values
after `os.path.normpath` normalization are refused fail-closed BEFORE
any custody open, O_EXCL claim, dynamic gate or credential read, and
every authority action then uses the FROZEN binding values
exclusively — a caller-selected alternate custody root cannot mint a
second same-attempt claim, and report acceptance cannot be redirected
to a different pre-existing file), a **binding-frozen custody
directory OBJECT identity gate** (BA-PREP-RB2-001: `output_identity`
additionally freezes the custody directory's host-local `st_dev`/
`st_ino` pair; the frozen pathname is opened EXACTLY ONCE and the held
fd must BE that object — a renamed-away custody directory with a fresh
replacement at the exact frozen pathname is refused before any claim,
and the attempt-global O_EXCL claim is created RELATIVE TO the held
verified directory object, never a pathname re-open, so a mid-run
pathname rebind cannot split accounting custody from output custody),
the **authority-CREATED attempt-owned report sink**
(BA-PREP-RB2-002: `report_source` must be a direct child of the frozen
custody root, the frozen invocation's single canonical `--report`
destination must equal it (parser-enforced), and the authority creates
the sink `O_CREAT|O_EXCL|O_NOFOLLOW` under the same held object after
the gates and before any credential read — a pre-existing object at
the frozen sink name refuses, acceptance snapshots ONLY the held sink
object (empty = honest `REPORT_MISSING`; a replacement object at the
pathname is never accepted and never unlinked by cleanup)), an
**attempt-global O_EXCL
authority claim keyed by the exact reserved
attempt id alone** (BA-RB-001: ONE reserved attempt id = ONE global
claim, independent of the binding digest, while the exact binding
digest remains durable, inspection-bound evidence inside every
accounting record), verified-held executables with identity-preserving
exec (`execveat(AT_EMPTY_PATH)`, fexecve fallback; unavailability
fails closed), and the BA-RB-002 security order — fresh dynamic gates
(`CLIENT_SELECTION_PREFLIGHT` → `NETWORK_READINESS` → `RESOURCE_GATE`
last) → durable `GATES_PASSED` → **only then** credential
materialization via non-dumpable pipe/sealed-memfd custody (ordinary
files refused) → durable `CONSUMED_PRE_EXEC` → immediate launch, with
no caller control anywhere in between and **no credential byte read
until every required pre-inference gate has durably passed**: a
failing pre-inference gate leaves the real credential unread and
unmaterialized — plus own-session
bounded child execution with process-group kill on timeout, and the
report lifecycle: one immutable snapshot of the HELD sink object →
credential screen → frozen
SHAPE-ONLY structural validator → **the authority's own independent
semantic report binding** (exact `target_commit` ==
`730d2b29f7c0e7d33af3451b6d9205ec27c143ed` plus event/role/attempt
equality; fixed safe tokens only) → 0444 O_EXCL freeze under operator
custody. Missing stays `REPORT_MISSING`; stdout/stderr never
reconstruct a report; every post-consumption failure is terminal
(distinct `PostConsumptionTerminalAccountingError`; never a
successful result; no retry/resume/revival).

The design-reserved event/attempt identities are binding CONSTANTS
ONLY. Deterministic temporary test fixtures exercise them as
SYNTHETIC / NON-AUTHORITATIVE / ZERO-PROVIDER / NON-PERSISTENT
strings inside test-controlled temporary directories — never as
canonical event instantiation.

## Production LOC bound

`bootstrap_authority/*.py` (the reused and derived modules included)
is bounded at **3000 LOC** (`wc -l`); the candidate reports its actual
final count in the canonical implementation record and
`tests/test_static.py` enforces the ceiling. The package must remain
smaller than the 3057-LOC candidate `bootstrap-supervisor` production
tree under audit.

## Tests

Zero-provider / zero-network. Run from the repository root with the
already-local interpreter and pytest (no fetch; `PIP_NO_INDEX=1
UV_OFFLINE=1`):

```
PYTHONPATH=bootstrap-authority python3 -m pytest -q bootstrap-authority/tests
```

`tests/conftest.py` builds synthetic worlds (temporary authority-
package copies, synthetic event packages, inert gate/launcher/
auditor/validator scripts, synthetic non-secret credential bytes,
temporary accounting/output directories). No fixture invokes any
provider, network route, or real client. The historical frozen
structural validator (`6aff0e7e…`, 7228 B) MAY be pinned by a future
event package as a SHAPE-ONLY structural component; tests use inert
validators with the same result-envelope contract.

## Governance

AUCDEV-023 remains P1 / READY / NOT DONE. The independent-auditor
provenance gate remains NOT_SATISFIED. PCH6-B-SD-002 and
PCH6-CR-BSD-001 remain IMPLEMENTED_AS_CANDIDATE /
AWAITING_FRESH_INDEPENDENT_AUDIT / NOT CLOSED; PCH6-B-SD-001 remains
RETAINED / OPEN; ROOT_CAUSE_NOT_ESTABLISHED is unchanged. Historical
PCH6 authority is CONSUMED / TERMINAL / CLOSED / NO_RERUN (model
engagements 2/2 USED historical truth; non-transferable). This
lineage's design budget: PROPOSED 2 / USED 0 — this implementation
consumes ZERO engagements. No audit execution, no audit PASS, no
qualification, no installation. The next action is a FRESH Control
Room readback of THIS BA-PREP-RB2-001 / RB2-002 follow-up remediation
candidate and its generated-LAST handoff before any event-package
preparation is authorized.
