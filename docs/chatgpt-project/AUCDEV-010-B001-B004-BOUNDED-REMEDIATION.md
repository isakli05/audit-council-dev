# AUCDEV-010 — B-001..B-004 Source-Supported Qualification-Blocker Bounded Remediation — Canonical Record

Published: **2026-09-14** (Europe/Istanbul).

Session role: the bounded-remediation IMPLEMENTER ONLY. This session is NOT
Auditor A, NOT Auditor B, NOT the Control Room, NOT a qualification
authority and NOT an installation authority, and it performed ZERO
model/frontier/provider inference (no `/audit-council`, no Claude Opus, no
GPT-5.6 Sol, no codex inference, no other provider/model call). Only
deterministic local source, tests and tools were executed. Every codex
launch in the new regressions uses `skill/tests/fixtures/fake_codex.py`.

## 1. Live bootstrap (fail closed; verified before any edit)

Live GitHub `refs/heads/master` resolved EXACT to
`b61059589249a52ff451bd4c0a5a77112dd40704` (= `origin/master` = local HEAD).
At that exact SHA this session fetched and read CURRENT-STATE (history
record 52), BACKLOG (AUCDEV-010 history record 54), the Control-Room
Runbook, the Project Update Protocol and
`AUCDEV-010-FINAL-68E3B082-FIRSTPASS-R0-RECONCILIATION.md`. Historical
audited target verified unmutated: `68e3b082958d2f6f35224702e51e35bbbd49d7db`
(tree `c36899d817c7e15fb8e31fc1e80fab198dc583a7`; `skill/` tree
`ce06ef9f46d983548fba6ee960d4d202573feedd`). Live `b610595:skill` equals
`ce06ef9f…` — the product bytes were EXACTLY the audited bytes before
remediation; `b610595` differs from `68e3b082` only in
`docs/chatgpt-project/*` (governance only).

## 2. Authority basis

The qualification first-pass set for event
`AUCDEV-010-BRQ-FINAL-68E3B082-20260914-01` remains
`BOOTSTRAP_EVIDENCE_PARITY_INVALID`; neither frozen first-pass
recommendation is treated as a qualification verdict. The remediation
authority is the Control Room's INDEPENDENT source readback of the four
HIGH mechanisms (canonical record §10), retained here as provenance labels
only: `B-001`, `B-002`, `B-003`, `B-004`. Current state entering this
session: `QUALIFICATION_BLOCKING_CONDITIONS_PRESENT`;
`QUALIFICATION_READINESS = BLOCKED`; `QUALIFICATION = NONE`;
`INSTALLATION = NONE`.

Non-goals honored: B-005..B-010 and A-F01..A-F09 were NOT remediated merely
because they exist; the Graphify parity defect was NOT touched in product
source (it is a future fresh-audit harness requirement:
`AUDITOR_B_EXTERNAL_TOOLING_METHODOLOGY_INPUT_PRESENT`); no fresh A/B audit
package was prepared or executed; no historical record was rewritten.

## 3. Identities

| Identity | Value |
|---|---|
| Remediation base (live master, exact) | `b61059589249a52ff451bd4c0a5a77112dd40704` |
| Pre-fix product bytes | skill tree `ce06ef9f46d983548fba6ee960d4d202573feedd` (= audited target's skill tree); scripts tree `e2095426be713f0c345eed529707b566bbcc94eb`; schemas tree `653d3c7ac4d78fd426da88877a5e87fe6d4d2d77` |
| Product candidate commit | `ecfece1830b44012cad3f46ab235bea9335fdeb7` (sole parent `b61059589249a52ff451bd4c0a5a77112dd40704`) |
| Candidate root tree | `682ae9f4568e51491004591c6701cd479d3511db` |
| Candidate `skill/` tree | `fb60425d17ee897e2d9dc9c6eaa08723541e7b45` |
| Changed paths | 10 (see §5) |
| Diffstat | +1345 / −179 |
| `git diff --check` | CLEAN |

## 4. Frozen pre-fix RED evidence (before any product edit)

One new narrowly-named regression module,
`skill/tests/test_b001_b004_remediation.py` (29 tests; RED-time SHA-256
`7926be4ad02cb675c781c8fa84ea38800d97a5717c1c128e71159c8b62a94675`), run
against the exact pre-fix product bytes:

- RED-B001 (A): truthful quota-style partial runs at FINALIZED (built only
  through the public state-store API, every skip bound to the transition
  that consumes it) currently accept `COMPLETE` and
  `COMPLETE_WITH_RESIDUAL_UNCERTAINTY` labels (library `set_completeness`
  and CLI `finalize`); (B): `check_stage_launch` currently admits a stage
  launch on an unconsumed skip record that names the necessary phase but is
  bound to a DIFFERENT transition (mis-bound, and separately the legacy
  unbound record). No model calls.
- RED-B002: (A) two concurrent in-process `cmd_start` calls for the same
  run+stage rendezvous AT the spawn point (synchronization primitives, no
  sleep-luck) both spawn paid children and the last stale-state save drops
  the other launched job from authoritative `state.json` (spawn count 2,
  job records 2, authoritative jobs 1); (B) a second thread enters
  `run_state_lock` while another thread of the same process holds it (the
  process-wide registry fast path bypasses the flock) — proven by a
  happens-before flag chain, not timing.
- RED-B003: same-size untracked byte mutation and further dirty-worktree
  tracked byte mutation after the baseline fingerprint are reported by
  `diff_fingerprints` (`changed_untracked` / `changed_dirty_worktree`) but
  invisible to `AC write-guard` (exit 0); special Git filenames (embedded
  double-quote, backslash, tab, non-ASCII) disappear behind C-quoting
  (`line[3:].strip('"')`) from the untracked and dirty inventories, the
  fingerprint diff AND the write guard.
- RED-B004: the canonical validator currently accepts `"evidence": []` and
  `"evidence": [{}]` on every affected schema surface (finding,
  final-findings, independent-audit via `$ref`, cross-examination via
  `$ref`).

Frozen result (verbatim output preserved in the handoff archive):
**Ran 29 tests — FAILED (failures=19, errors=0)**. All 19 failures are
mechanism tests (B-001 ×7, B-002 ×6 incl. stress, B-003 ×4, B-004 ×2); the
10 truthful-path guards (honest full run → COMPLETE; documented
post-independent quota omission → CW_RU; skipped-independent partial →
PARTIAL_CODEX_QUOTA; exactly-bound skip → admitted launch; terminal quota
retry; clean tree; ordinary add/remove violations; valid typed evidence)
passed on the pre-fix bytes — proving the regressions block exactly the
mechanisms, not the truthful workflows. RED-RUN.txt SHA-256
`caa448b5e89ea4d8a0bef55f20aad59652b8c784f02311995b328bcf8c8da9f2`.

## 5. Implementation (per mechanism, exact changed paths)

Changed paths (product candidate commit only):

- `skill/scripts/state_store.py` — R-B001: `INDEPENDENT_COMPLETION_PHASES`
  + `COMPLETENESS_MANDATORY_PHASES` + pure `completeness_skip_violations()`;
  `set_completeness` enforces the invariant under the run-state lock;
  `check_stage_launch` builds launch coverage from NAME + EXACT binding
  (unconsumed, `from_phase ==` current phase, `to_phase` crossing the
  skipped phase — the same binding `transition()` requires when consuming
  the record). R-B002: `run_state_lock` reentrancy scoped to the owning
  thread (registry stores owner thread id; every other caller opens its own
  file description and blocks on the flock, which conflicts between
  separate `open()`s even within one process).
- `skill/scripts/codex_runner.py` — R-B002: `cmd_start` performs the
  authoritative state read, budget/phase admission, active-attempt
  uniqueness (`_active_job_for_stage`, STARTING/RUNNING only — terminal
  attempts still retry within the governor's caps), attempt numbering,
  spawn and authoritative persistence as ONE serialized launch transaction
  under `run_state_lock`; persistence failure after spawn fails closed
  (`_terminate_launched_job`: SIGKILL the process group, preserve the
  diagnostic job record `ABORTED_PERSISTENCE_FAILURE`, collect the child);
  `_update_state_after_wait` re-reads state under the lock; supervised
  children registry (`_SUPERVISED_PROCS`) keeps detached Popen objects
  referenced until terminal so no supervised-child ResourceWarning fires;
  `atomic_write_json` temp names are per execution context (pid+thread id —
  two same-process threads used to collide on the shared run-local codex
  schema tmp file, exposed deterministically by the new concurrent-launch
  regression; same B-002 mechanism family).
- `skill/scripts/repo_fingerprint.py` — R-B003: inventories parse the
  NUL-separated machine-readable forms (`git status --porcelain -z -uall`
  via `_porcelain_records`, rename/copy source-path records included;
  `git ls-files -s -z` via `_parse_ls_files`) so special filenames are
  keyed byte-exactly; the STORED `porcelain` document field keeps its exact
  legacy bytes, so legacy fingerprint/binding documents compare unchanged
  under the algorithm they were frozen with (a hypothetical historical
  document frozen with a C-misquoted special path diverges fail-closed —
  reported as changed — never silently verified).
- `skill/scripts/audit_council.py` — R-B003: `_write_guard_violations`
  consumes `changed_dirty_worktree` (kind `modified`) and
  `changed_untracked` (kind `untracked-change`); the guard is never weaker
  than the fingerprint it inherits. R-B001: `cmd_finalize` validates the
  mandatory-stage invariant on freshly loaded state BEFORE the irreversible
  `apply_transition(run_dir, "COMPLETE")`, with the
  checksum-record→transition→label sequence one serialized mutation under
  `run_state_lock`.
- `skill/schemas/finding.schema.json`, `skill/schemas/final-findings.schema.json`
  — R-B004: `evidence` gains `minItems: 1` and evidence items gain
  `required: ["kind"]` (the `kind` enum already existed). This is
  enforcement alignment with the already-authoritative
  `protocols/evidence-policy.md` ("Every evidence or counter-evidence item
  carries a `kind`"), NOT a protocol change; no major version bump.
  `validate_artifact.py` was NOT changed (its generic validator already
  enforces `required` and `minItems` when schemas declare them).
  `counter_evidence` deliberately keeps no `minItems` (no counter-evidence
  found is a legitimate state).
- `skill/tests/test_b001_b004_remediation.py` — the new regression module.
- `skill/tests/test_line_ranges_v2.py`, `skill/tests/test_disagreement_normalization.py`
  — test-fixture alignment only: minimal valid documents now carry one
  typed evidence item instead of `evidence: []`.
- `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md` — items 34/36/37 (+38 note) now
  state the mechanically proven invariants with status
  `SOURCE_SUPPORTED_MECHANISM / REMEDIATION_IMPLEMENTED /
  AWAITING_FRESH_AUDIT`; no prior audit record was deleted or rewritten.

Production paths NOT changed: `skill/scripts/budgets.py` (caps semantics
unchanged — successful-stage caps and attempt caps verified unchanged),
`skill/scripts/validate_artifact.py` (schema-declared enforcement already
sufficient), `skill/PUBLIC-CONTRACT.md` (the fixes make the implementation
match the already-documented contract: COMPLETE = "all phases finished",
the "cannot skip a mandatory independent pass … or promote PARTIAL to
COMPLETE" guarantee, the write-guard freshness inheritance).

## 6. GREEN evidence (first results preserved verbatim in the archive)

- Focused: remediation module 29/29 OK (also 29/29 OK with
  `-W error::ResourceWarning`); QX stabilization module 41/41 OK with
  ResourceWarning-as-error; codex-runner mock 26/26 OK; repo fingerprint
  8/8; source write guard 6/6; state store 18/18; schema family
  12+34+12+20+18+2 all OK.
- Concurrency stress (zero inference, exact counts): 25 iterations × 2
  paired concurrent same-stage starts on a fresh run each — every iteration
  exactly ONE paid spawn, ONE admitted launch (rc 0), ONE refusal (rc 3),
  ONE authoritative job, ONE job record; 0 violations over the run. Thread
  mutual exclusion: 8 threads × 25 in-lock read-modify-write bumps = 200/200
  counted. Terminal-quota retry: quota attempt → wait (QUOTA, rc 2) →
  retry admitted (attempt_number 2) → COMPLETE.
- Full deterministic suite, natural posture ×3: **679 tests OK — 0
  failures, 0 errors, 0 skips** (120.5 s / 120.9 s / 121.1 s).
- Warning-visible posture (`PYTHONWARNINGS=always PYTHONTRACEMALLOC=15`):
  **679 OK — 0 project-owned warning lines of ANY category, 0 `Exception
  ignored`** (486.8 s).
- Warnings-as-error posture (`PYTHONWARNINGS=error`): **679 OK, exit 0**
  (120.0 s).
- Isolated clean-environment posture (`env -i`, fresh
  HOME/XDG/AUDIT_COUNCIL_CACHE_HOME/AUDIT_COUNCIL_ENV_ROOT, PATH=/usr/bin:/bin):
  **679 OK (skipped=7, rc 0)** — the exact canonical external-condition
  classification as before this remediation (da27c0 archive not present;
  production codex toolchain not on PATH ×5; smoke artifacts not present),
  no new unexplained skip.
- `git diff --check` CLEAN (base → candidate).

Intermediate failures during development (recorded, not hidden; each
remediated and re-run): the first post-implementation full-suite run
FAILED with 11 failures — 8 in `test_disagreement_normalization` (fixture
`evidence: []` now correctly rejected), 1 in `test_env_lifecycle`
(`f.fsync` transcription slip in the rewritten stdin-staging block) and 1
in `test_eval_framework` (matrix L3, downstream of the env-lifecycle
failure), plus 2 focused `test_line_ranges_v2` failures (same fixture
class). The two focused module failures and the 11 full-suite failures
were all fixture/transcription corrections on the test/rewrite side; no
product invariant was weakened to make them pass.

## 7. Final completeness matrix (R-B001)

Mechanical signal: a `phase_skips` entry naming a phase means that phase
was never honestly completed (`transition()` admits a skip record only
when the machine passes OVER that phase).

| completeness_state | OPUS_INDEP | CODEX_INDEP | OPUS_CROSS | CODEX_CROSS | LEDGER | ADJUDICATION | FINALIZED |
|---|---|---|---|---|---|---|---|
| COMPLETE | skip ⇒ refuse | skip ⇒ refuse | skip ⇒ refuse | skip ⇒ refuse | skip ⇒ refuse (unreachable skip) | optional (existing explicit rule) | skip ⇒ refuse |
| COMPLETE_WITH_RESIDUAL_UNCERTAINTY | skip ⇒ refuse | skip ⇒ refuse | documented post-independent quota omission allowed | documented post-independent quota omission allowed | skip ⇒ refuse (unreachable skip) | optional | skip ⇒ refuse |
| PARTIAL_* / STALE_REPOSITORY / INVALID_* | no mandatory-stage requirement (truthful for their own semantics) |

Enforced in `state_store.set_completeness` (public library API, under the
lock) and in `audit_council.cmd_finalize` BEFORE the irreversible
transition to COMPLETE. Skip functionality itself is untouched.

## 8. Status and next route

`AUCDEV_010_B001_B004_BOUNDED_REMEDIATION_IMPLEMENTED_AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK_AND_FRESH_AUDIT`

- The four HIGH mechanisms are recorded ONLY as
  `SOURCE_SUPPORTED_MECHANISM / REMEDIATION_IMPLEMENTED /
  AWAITING_FRESH_AUDIT`. They are NOT `CLOSED_BY_AUDIT`, NOT `QUALIFIED`,
  NOT `PASS` — only a fresh audit of the NEW target SHA can close them.
- `QUALIFICATION_READINESS = BLOCKED`; `QUALIFICATION = NONE`;
  `INSTALLATION = NONE`. B-005..B-010 and A-F01..A-F09 remain as recorded,
  unmerged and unadjudicated; the evidence-parity defect
  (`BOOTSTRAP_EVIDENCE_PARITY_INVALID`) stands unchanged.
- The product candidate commit `ecfece1…` is the ONLY remediation
  candidate eligible for a future fresh A/B audit package, subject to
  Control Room readback. No fresh audit package was prepared or executed
  in this session; the next fresh-audit harness must prevent
  `AUDITOR_B_EXTERNAL_TOOLING_METHODOLOGY_INPUT_PRESENT`.
- Model engagements this session: ZERO (no Auditor A/B, no provider/model
  call of any kind; all launches were the deterministic fake-codex
  fixture).
