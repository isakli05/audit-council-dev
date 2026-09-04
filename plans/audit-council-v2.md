# Audit Council v2.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Multi-agent-orchestration (MAO) is the sole orchestration authority when packages are delegated; the lead owns shared contracts, integration, verification, installation, and reports.

**Goal:** Evolve Audit Council v1.0.3 into a reproducible, environment-bound,
evidence-efficient, eval-driven audit platform (pillars A0/A1/A2/B/C/D/E/F/G/H)
while preserving every validated v1 invariant.

**Architecture:** Add an environment/binding trust layer (A0/A1) beneath the
unchanged two-model council core; a provenance-bound evidence cache (B) and
typed multi-range evidence model (G) around it; attempt-complete telemetry and
configurable budgets (E); eval-gated specialists kept default-off (C); a
four-tier eval suite (D); a versioned public contract (F); and an explicit,
checkpointable end-to-end lifecycle (H). Full design + frozen contract schemas:
`AUDIT-COUNCIL-V2-ARCHITECTURE.md` (§ references below are to that document).

**Tech Stack:** Python 3.14 stdlib only (no pip deps), JSON Schema subset
supported by `validate_artifact.py`, git plumbing, `codex exec` CLI 0.153.0,
Claude Code 2.1.260 session skills + PreToolUse hooks. No network requirements.

## Global Constraints (apply to every task)

- Build tree: `/home/isa/audit-council-dev/skill/`. Installed copy
  `~/.claude/skills/audit-council/` is NOT touched until release qualification
  (PKG-INT Task 9) — never write there during implementation.
- Historical runs (Benchmark 001, Fifth, smoke fixtures) are READ-ONLY
  evidence: never modified, never re-run without explicit operator approval.
- v1 invariants list (ARCHITECTURE §1.5) is binding; any task that would
  weaken one redesigns instead. In particular: subscription auth only; direct
  `codex exec`; read-only Codex sandbox; exact thread-id resume, never
  `--last`; first-pass independence; canonical validation authoritative;
  INVALID_OUTPUT ≠ successful stage; unknown usage never fabricated as zero;
  per-job logs never overwrite; no automatic push/merge/publish — **commits
  stay local; never `git push` or add remotes**.
- All writes during implementation stay under `/home/isa/audit-council-dev/`.
- New schemas/JSON carry `schema_version: 2` (readers accept 1 and 2); finalized
  v1 run artifacts are never rewritten.
- Test command: `cd /home/isa/audit-council-dev/skill && /usr/bin/python3 -m
  unittest discover -s tests` — must remain green at every task boundary
  (160/160 today) plus each task's new tests.
- Deterministic only: no real model calls anywhere in this plan except the two
  explicitly gated smokes (Task 8.4, PKG-EVAL) — see Model-Call Budget.
- Environment quirk: spawn children with `/usr/bin/python3`, never
  `sys.executable` (this host's `python3` shim makes `sys.executable` the
  ZCode AppImage).
- Deterministic tests MUST NOT write persistent state under the real user
  cache/home: every runtime/cache root is injectable via
  `AUDIT_COUNCIL_CACHE_HOME`, and tests inject an isolated path under
  `/home/isa/audit-council-dev/` or a `tempfile` root (pre-freeze
  clarification 3).

---

## 0. Dependency graph and integration order

```
Task 0 (lead): git baseline + frozen shared contracts
   │
   ├─→ PKG-SCHEMA (G)  ──┐            [no deps; pure schemas+migration]
   ├─→ PKG-A0 (A0) ──────┤            [no deps; env_binding + path_guard]
   │                      ├─→ PKG-TELE (E)      [touches codex_runner only]
   │                      ├─→ PKG-ENV (A1/A2)   [needs env_binding]
   │                      └─→ PKG-EVID (B)      [needs binding digest + G refs]
   │                                │
   │                                ├─→ PKG-SPEC (C) [needs evidence refs; stays OFF]
   │                                └─→ PKG-EVAL (D) [tier1 now; tiers 2-4 later]
   └─→ PKG-PUB (F)      [after SCHEMA+TELE contracts freeze]
                        │
                        └─→ PKG-INT (H) [integrates all; e2e; migration; install]
                                │
                                └─→ Independent adversarial review → RC
                                        └─→ (operator approval) historical eval → installation
```

Integration order: **0 → PKG-A0 ∥ PKG-SCHEMA → PKG-TELE → PKG-ENV → PKG-EVID →
PKG-PUB → PKG-EVAL(tier 1) → PKG-SPEC → PKG-INT → review → RC**. Packages own
disjoint file sets (below); anything outside a package's file list is
lead-only. Contracts in ARCHITECTURE §3.4 are frozen at Task 0; changes to them
are lead decisions recorded in this file's changelog.

---

## Task 0 (lead): baseline + frozen contracts

**Files:** Create: `.gitignore` (`__pycache__/`, `repro/tmp/`),
`plans/audit-council-v2.md` (this file), `AUDIT-COUNCIL-V2-ARCHITECTURE.md`;
Modify: none in `skill/`.

- [ ] **0.1** `git init` in `/home/isa/audit-council-dev` (local only, no
  remote ever), commit baseline: current v1.0.3 tree + reports + this plan +
  architecture doc + `repro/phase0_limitations_repro.py`. Tag `v1.0.3-baseline`.
- [ ] **0.2** Run `/usr/bin/python3 -m unittest discover -s tests` in
  `skill/` → record 160/160 OK (~25 s). Run
  `/usr/bin/python3 ../repro/phase0_limitations_repro.py` → 4/4 REPRODUCED.
- [ ] **0.3** Freeze contracts: ARCHITECTURE §3.4.1–§3.4.9 are normative.
  Commit. (Any later contract change = lead edit + changelog line here.)

---

## PKG-SCHEMA — Structured Evidence Model v2 (pillar G)

**Ownership (sub-agent package):** files below only. Cannot touch
`codex_runner.py`, `audit_council.py`, `state_store.py`.

**Files:**
- Modify: `skill/schemas/finding.schema.json`,
  `cross-examination.schema.json`, `disagreement-ledger.schema.json`,
  `adjudication.schema.json`, `final-findings.schema.json`
- Create: `skill/scripts/evidence_migration.py`,
  `skill/tests/test_line_ranges_v2.py`
- Modify: `skill/scripts/render_report.py` (render `line_ranges`),
  `skill/scripts/wire_adapter.py` (only if a test proves a gap)

**Interfaces produced (frozen):**
```python
# evidence_migration.py
def lines_to_ranges(lines: str) -> list[dict[str, int]]:
    """'^\\d+$' -> [{start:N,end:N}]; '^\\d+-\\d+$' -> [{start:N,end:M}];
    ANY other shape (comma, empty, reversed) raises ValueErrorMigration."""
class MigrationError(ValueError): ...
def normalize_ranges(ranges: list[dict]) -> list[dict]:
    """validate start>=1, end>=start; sort by (start,end); returns new list."""
def migrate_artifact(doc: dict) -> dict:
    """v1 artifact -> v2: for every evidence/counter_evidence item, drop
    'lines' string, set 'line_ranges' via lines_to_ranges. Idempotent.
    Raises MigrationError on multi-range strings (never comma-parse)."""
def is_v1_artifact(doc) -> bool:
    """True iff any evidence item carries a legacy 'lines' key."""
```

### Task G.1 — typed line_ranges in all five schemas
- [ ] **Step 1 (failing tests).** In `test_line_ranges_v2.py` write, using
  `validate_artifact.validate(instance, schema, base_dir=schemas_dir)`:
  - `test_zero_ranges_valid` — a minimal finding whose single evidence item has
    only `{kind, requirement_ref}` (no line_ranges) validates.
  - `test_one_range_valid`, `test_many_disjoint_valid` — `[{184,185},{240,273}]`
    validates in `finding.schema.json` findings AND in
    `cross-examination.schema.json` `challenges[].counter_evidence` AND
    `adjudication.schema.json` `evidence_packet.evidence` AND
    `final-findings.schema.json` findings AND `disagreement-ledger.schema.json`
    clusters[].counter_evidence (all five inline locations).
  - `test_reversed_rejected`, `test_zero_start_rejected`,
    `test_float_rejected`, `test_extra_key_rejected`
    (`additionalProperties:false` on the range object),
    `test_over_maxitems_rejected` (33 ranges).
  - `test_legacy_lines_string_rejected_in_v2` — an item with `lines:
    "184-185"` FAILS v2 schemas (v2 accepts only line_ranges).
- [ ] **Step 2.** Run → FAIL (line_ranges unknown today).
- [ ] **Step 3.** In each of the five schemas add to every
  evidence/counter-evidence item:
  ```json
  "line_ranges": {"type": "array", "maxItems": 32, "items": {
    "type": "object", "additionalProperties": false,
    "required": ["start", "end"],
    "properties": {"start": {"type": "integer", "minimum": 1},
                   "end":   {"type": "integer", "minimum": 1}}}}
  ```
  and REMOVE the `lines` property. (No comma-form anywhere.)
- [ ] **Step 4.** Run → PASS. Full suite → green except v1-era tests that
  assert `lines` (update those tests to v2 in this same task; they are in
  package scope via `tests/` additions only — coordinate legacy-test edits
  with the lead; the lead pre-approves editing ONLY the `lines`-asserting
  assertions in existing test files, listed in the package brief).
- [ ] **Step 5.** Commit `feat(schema): typed multi-range line_ranges (G)`.

### Task G.2 — migration reader + canonicalization
- [ ] **Step 1 (failing tests):** `lines_to_ranges("184") == [{"start":184,
  "end":184}]`; `"184-185" -> [{184,185}]`; `MigrationError` on
  `"184-185, 240-273"`, `""`, `"185-184"`, `"0-3"`. `normalize_ranges` sorts
  `[{240,273},{184,185}] -> [{184,185},{240,273}]`. `migrate_artifact`
  converts a full v1 finding doc (use the Fifth run's `10-opus-independent
  .json` READ-ONLY as fixture input copied into `tests/fixtures/`) and is
  idempotent (`migrate_artifact(migrate_artifact(x)) == migrate_artifact(x)`).
- [ ] **Step 2/3/4.** Implement; run; green. Commit
  `feat(migration): v1 lines -> v2 line_ranges reader (G)`.

### Task G.3 — wire path end-to-end (exact Fifth regression)
- [ ] **Step 1 (failing test):** `build_codex_schema`-produced wire schema for
  cross-examination contains `line_ranges` items as strict objects; feeding
  the REAL Fifth wire payload with `"lines"` replaced by typed
  `"line_ranges": [{"start":184,"end":185},{"start":240,"end":273}]` through
  `wire_to_canonical` + canonical validation → PASS (this is the regression
  that would have saved Phase 4B).
- [ ] **Step 2/3/4.** Adapter already passes objects through; add tests only
  if red. Commit `test(schema): Fifth multi-range payload now canonical-valid (G)`.

### Task G.4 — render + backward artifact read
- [ ] render_report emits `L184-185, 240-273` style citations from
  line_ranges; `resume-check` path validates v1 artifacts via
  `migrate_artifact` in-memory WITHOUT rewriting them on disk (test: resume
  check on a copied v1 run dir passes and leaves bytes identical).
  Commit.

**Acceptance (DoD G):** zero/one/many disjoint ranges canonically supported;
comma ambiguity structurally eliminated; old artifacts readable; finalized
runs byte-untouched; canonical validation remains authority; all five schema
locations consistent; Fifth exact values regression-green.

---

## PKG-A0 — Repo-Root Confinement & Environment/Binding (pillar A0)

**Ownership:** `skill/scripts/env_binding.py` (new),
`skill/scripts/path_guard.py` (new), `skill/hooks/path_guard_hook.py` (new),
`skill/schemas/env-binding.schema.json` (new),
`skill/tests/test_env_binding.py`, `skill/tests/test_path_guard.py` (new).
`audit_council.py`/`state.schema.json` integration is done by the LEAD in
Task A0.6 (shared-file conflict with PKG-TELE/PKG-INT). Test files may also
edit legacy `lines`-constructing lines ONLY where required to keep the suite
green (same pre-approval as PKG-SCHEMA).

**Interfaces produced (frozen):**
```python
# env_binding.py  (schema: ARCHITECTURE §3.4.1)
class EnvironmentBindingError(Exception):
    def __init__(self, reason: str, detail: dict): ...  # reason ∈ §3.4.2
def capture(repo_root: str, run_id: str, brief_path: str,
            brief_target: dict | None, allowed_disposable_roots: list[str]) -> dict
def digest(binding: dict) -> str            # sha256 over canonical JSON minus digest
def verify_frozen(binding: dict) -> dict    # recompute live; {ok, reason, live, frozen}
def assert_consistent(binding: dict) -> None  # A0.2 gate; raises EnvironmentBindingError
def reconstruct(run_dir: str) -> dict       # rebuild binding from disk, must equal frozen
def repo_root_from(path: str) -> str        # git rev-parse --show-toplevel (worktree-aware);
                                           # raises on non-repo; NEVER sniffs for a .git directory
def cache_root() -> str                     # AUDIT_COUNCIL_CACHE_HOME override, else
                                           # ${XDG_CACHE_HOME:-~/.cache}/audit-council/

# path_guard.py
def canonicalize(path: str) -> str          # realpath-resolved, absolute
def is_within(path: str, root: str) -> bool # component-wise containment after canonicalize
def check_tool_call(tool: str, tool_input: dict, frozen_root: str,
                    allowed_roots: list[str]) -> tuple[bool, str]
def scan_bash_command(cmd: str, cwd: str, frozen_root: str,
                      allowed_roots: list[str]) -> list[str]  # list of escape reasons
```

### Task A0.1 — binding capture/verify
- [ ] **Step 1 (failing tests)** in `test_env_binding.py`, using disposable
  fixture repos created by the test itself under `tests/fixtures/` +
  `tempfile` inside the dev tree (git init/commit; a linked worktree via
  `git worktree add --detach` for the identity tests):
  - capture on a plain repo → all §3.4.1 fields present, `detached_head`
    correct; **digest excludes `binding_digest` + `frozen_at` (pre-freeze
    clarification 1)**, so two captures seconds apart produce the SAME digest
    despite differing `frozen_at` values.
  - capture on a detached worktree → succeeds; `worktree_identity` differs
    from the main worktree at the SAME head_sha (the A0.1 "HEAD alone is
    insufficient" test).
  - `verify_frozen` detects: root replaced (delete+recreate dir), HEAD moved
    (new commit), worktree identity changed (recreate worktree at same HEAD).
  - `reconstruct` after "restart" (new process, same files) == frozen digest.
- [ ] **Step 2/3/4.** Implement with `git rev-parse --show-toplevel`,
  `--absolute-git-dir`, `--git-common-dir`, `--is-inside-work-tree`; commit.

### Task A0.2 — brief consistency gate (zero-inference)
- [ ] **Step 1 (failing tests):** `assert_consistent` raises
  `BRIEF_ROOT_MISMATCH` when `brief_target.declared_repository_root` (realpath)
  ≠ `repo_root_realpath`; `BRIEF_HEAD_MISMATCH` on head mismatch; passes when
  both match; passes when `brief_target` is null (no declared metadata —
  then the contract's own `target_repository` is checked identically); a
  brief whose PROSE contains `/any/absolute/path` never affects the outcome
  (inert-text test — the exact Fifth failure mode, expect NO raise).
- [ ] **Step 2/3/4.** Implement; commit. This function is THE gate the lead
  wires before Phase 1/2 inference in Task A0.5.

### Task A0.3 — mechanical root confinement (path_guard)
- [ ] **Step 1 (failing tests)** in `test_path_guard.py` (fixture: root R with
  symlink `R/link -> /elsewhere/live-repo`, sibling worktree W at same HEAD,
  authorized fixture dir F under allowed_roots):
  - `is_within` rejects: absolute outside path, `../` escape, symlink escape
    (single + nested), `R/link/inside`, alternate worktree W, `git -C
    <outside>`, subshell `(cd /outside && ...)`, env-var expanded
    `$OUTSIDE/x` (expand then check), multi-root `rg pat /outside /R`,
    path-alias forms; accepts paths under R and F.
  - `check_tool_call` maps Read/Grep/Glob/Bash inputs (file_path, path,
    command, cwd) to `scan_bash_command`/`is_within` and returns
    `(False, reason)` with reasons from §3.4.2 (`PATH_ESCAPE_ATTEMPT`,
    `ALTERNATE_WORKTREE_ACCESS`, `SYMLINK_ESCAPE`, `UNAUTHORIZED_TMP_ACCESS`
    for any `/tmp` path not under an allowed fixture root,
    `CWD_OUTSIDE_FROZEN_ROOT`). Ambiguous/unparseable shell → deny
    (fail-closed) with reason `PATH_ESCAPE_ATTEMPT`.
  - Compound-command policy (pre-freeze clarification 4): `scan_bash_command`
    must segment compound constructs (`&&`, `||`, `;`, `|`, subshells,
    command substitution) and validate EACH segment; ordinary in-root usage
    MUST remain allowed. Required false-positive regressions:
    `test_compound_and_in_root_allowed`, `test_pipe_in_root_allowed`,
    `test_subshell_in_root_allowed`,
    `test_command_substitution_in_root_allowed`,
    `test_semicolon_sequence_in_root_allowed`. Required malicious denials:
    `cd /outside && …`, `… | cat > /outside`, `(cd /outside; …)`,
    `$(cat /outside/secret)` — all DENIED. Blanket denial of compound syntax
    is a task failure, not a policy.
- [ ] **Step 2/3/4.** Implement (stdlib `shlex` + explicit deny of `;`, `&&`,
  `|`, `$()`, backticks segments resolving outside; conservative by design);
  commit.

### Task A0.4 — Claude PreToolUse hook (runner-enforced deny-before-exec)
- [ ] **Step 1 (failing tests):** `hooks/path_guard_hook.py` reads a JSON
  `{"tool_name","tool_input"}` on stdin; with an active run registered in
  `<cache_root()>/active-runs/<run-id>` (file = run dir path; cache root
  honors `AUDIT_COUNCIL_CACHE_HOME` → `${XDG_CACHE_HOME:-~/.cache}/
  audit-council/`), it
  calls `check_tool_call` against the run's frozen binding; exit 2 + stderr
  reason blocks the call; with NO active run it exits 0 (zero impact on
  normal sessions); malformed input exits 2 (fail-closed). Tests inject
  `AUDIT_COUNCIL_CACHE_HOME` pointing at an isolated dev-tree root — the hook
  must never write the real user cache under test (pre-freeze clarification
  3).
- [ ] **Step 2/3/4.** Implement; commit. Operator installation of the hook
  into `~/.claude/settings.json` (PreToolUse matcher Bash/Read/Grep/Glob,
  command `"/usr/bin/python3 ~/.claude/skills/audit-council/hooks/path_guard_hook.py"`)
  is a documented ONE-TIME opt-in in README (lead writes docs in PKG-INT);
  the hook is runner-enforced and the manifest records whether it was active.
- [ ] **Research spike (doc-only, no code):** codex read confinement. Verify
  from codex docs/local probes what `--sandbox read-only` and
  `-c sandbox_permissions` guarantee on Linux 6.x (Landlock). Evaluate a
  bubblewrap wrapper (`bwrap --ro-bind <frozen_root> /workspace --ro-bind
  /usr /usr … --dev /dev --proc /proc --tmpfs /tmp --unshare-user`) around
  `codex exec -C /workspace` (probe: is `bwrap` installed? `landlock`?
  kernel 7.2.2 CachyOS). Deliverable: `docs/A0-CODEX-CONFINEMENT.md` stating
  OS-enforced vs runner-enforced guarantees and the chosen default (wrapper
  if bwrap present and smoke-proven; else runner-enforced + documented
  residual risk). No wrapper is wired into the runner without lead approval
  after the PKG-EVAL tier-1 gate.

### Task A0.5 — worktree-aware repository discovery (pre-freeze clarification 2)
- [ ] **Step 1 (failing tests):** `env_binding.repo_root_from(path)` returns
  the correct worktree root for: a main worktree; a linked worktree
  (`git worktree add`); a DETACHED linked worktree; a cwd nested deeply
  inside the worktree; and raises for a non-repository path. All new
  discovery code uses git plumbing only — no `.git`-directory sniffing
  (`os.path.isdir(…"/.git")` is banned in new code; eliminating the legacy
  `codex_runner.detect_repo_root` sniffing is the LEAD's Task A0.6).
- [ ] **Step 2/3/4.** Implement via `git -C <path> rev-parse --show-toplevel`
  (+ `--absolute-git-dir` where needed); commit.

### Task A0.6 (LEAD) — wire the gate into the lifecycle
- [ ] `audit_council.py`: `init-run` captures + persists binding to
  `01-environment-binding.json`, registers active-run entry; `verify-env
  --run DIR` subcommand = `assert_consistent` + fingerprint verify; `advance`
  for inference phases (OPUS_INDEPENDENT→…) refuses unless `verify-env` ok;
  `finalize`/`cancel` unregister the active run. `state.schema.json` v2 adds
  `env_binding_digest`, `completeness_state: INVALID_AUDIT_ENVIRONMENT`.
  `resume-check` reconstructs binding identically. `codex_runner.detect_repo_root`
  delegates to `env_binding.repo_root_from` (a cross-scripts grep test bans
  `.git`-directory sniffing in ALL repository-discovery code). Tests in
  `tests/test_env_lifecycle.py` (lead-owned): root mismatch → zero codex
  `start` calls accepted (governor-level refusal), HEAD mismatch → zero,
  correct detached worktree passes end-to-end with fake_codex.
- [ ] The program spec's mandatory regression matrix (its "A0.6" list, all
  ~20 cases) exists as named tests across `test_env_binding.py` /
  `test_path_guard.py` / `test_env_lifecycle.py`; a checklist comment maps
  each spec case → test name; CI-equivalent = the unittest run.

**Acceptance (DoD A0):** spec's explicit YES/NO list — stale absolute cd
cannot redirect (NO); same-HEAD alternate worktree (NO); Read/Grep/Glob/Bash
escape (NO); symlink escape (NO); /tmp restricted to capability roots (YES);
root/HEAD mismatch fails before inference (YES); detached HEAD supported
(YES); environment integrity tests 100%.

---

## PKG-TELE — Telemetry Governor 2.0 (pillar E)

**Ownership:** `skill/scripts/codex_runner.py` (telemetry/governor sections
only), new `skill/scripts/budgets.py`, `skill/tests/test_telemetry_v2.py`.

**Interfaces produced:**
```python
# budgets.py
DEFAULT_BUDGETS = {"max_successful_stages_per_phase": 1, "max_total_stages": 3,
  "max_attempts_per_phase": 3, "max_repairs_per_phase": 1,
  "specialists_default": 0, "specialists_normal_cap": 2, "specialists_hard_cap": 3,
  "max_specialist_turns": 2, "max_dynamic_probes": 4,
  "cached_evidence_policy": "REUSE_WHEN_VALID", "force_fresh_release_gates": True}
def load(run_dir) -> dict; def check(stage, budgets, state) -> None (raises BudgetExceeded)
def record_omission(run_dir, entry: dict) -> None   # explicit budget_omissions[]
# codex_runner.py (modified semantics, same signatures)
def _finalize_elapsed(job: dict) -> float   # called on EVERY terminal path, computed once
```

### Task E.1 — elapsed on every terminal attempt (fixes reproduced R2)
- [ ] **Step 1 (failing tests):** for QUOTA, AUTH_ERROR, FAILED,
  INVALID_OUTPUT, CANCELLED terminal classifications, the persisted job record
  has `elapsed_sec` (float ≥0) computed once — re-wait does not inflate it;
  genuinely unavailable clock data (no `started_at_monotonic`) →
  `elapsed_sec: null` + `elapsed_unknown_reason: "monotonic_start_missing"`.
  INVALID_OUTPUT contributes invocation count + token totals + elapsed but
  NOT `successful_stage_counted`. These tests are the Phase-0 repro promoted
  to permanent tests.
- [ ] **Step 2/3/4.** Add `_finalize_elapsed`, call from every terminal branch
  in `classify_and_finalize` + `cmd_cancel`; commit.

### Task E.2 — budgets 2.0 + explicit omissions
- [ ] Failing tests: budgets block read from run manifest (defaults above);
  `record_omission` appends `{stage, decision, reason}` to
  `99-run-metrics.json` via a derived-state rebuild (idempotent); governor
  still refuses: 4th successful stage, 2nd successful same-phase stage,
  4th attempt in a phase, 2nd repair. Metrics remain idempotent /
  restart-reconstructible / job-deduplicated (delete metrics file → `status`
  rebuilds byte-identical). Specials: `check("specialist", …)` obeys
  0-default (any specialist without explicit activation → BudgetExceeded).
- [ ] Implement; commit. Wall-clock (`started_at`/`completed_at`) cross-check:
  `elapsed_sec` within ±2 s of wall delta for every attempt (new invariant
  test using the fake fixtures).

**Acceptance (DoD E):** all terminal inference attempts in telemetry with
stable elapsed; INVALID_OUTPUT contributes tokens+elapsed; metrics
idempotent/reconstructible; budget omissions explicit; failed attempts
excluded from successful-stage counts.

---

## PKG-ENV — Environment Manager + Artifact Lifecycle (A1/A2)

**Ownership:** `skill/scripts/environment_manager.py` (new),
`skill/scripts/artifact_layout.py` (new), `skill/schemas/environment-record.
schema.json` (new), `skill/tests/test_environment_manager.py`,
`skill/tests/test_artifact_layout.py`. Depends on PKG-A0 `env_binding`.

**Interfaces produced:**
```python
def resolve_mode(contract: dict, brief_meta: dict) -> str   # AUTO|CURRENT|RELEASE|HISTORICAL
def prepare(mode, source_repo, run_id, target_ref=None) -> dict  # EnvironmentRecord
def archive_run(run_dir, worktree_root) -> str               # archive path
def remove_worktree(worktree_root) -> None                   # git worktree remove ONLY
def list_runs() -> list[dict]; def cleanup(dry_run=True) -> dict
# artifact_layout.py
def resolve_roots(config_path=None) -> dict  # {project_evidence, run_artifacts,
  #  ephemeral_worktrees, benchmark_corpus, long_term_history} with defaults
  #  preserving project-local audit-output/audit-council
```

### Task ENV.1 — mode resolution + isolated preparation
- [ ] Failing tests: AUTO never silently downgrades (contract requires
  isolation → RELEASE even if CURRENT would be cheaper); CURRENT only when
  contract permits (else RELEASE); HISTORICAL stages ONLY explicitly
  authorized evidence (allow-list; deny-list wins); `prepare` creates a
  DETACHED worktree (`git worktree add --detach <root> <ref>`), freezes a
  binding whose `source_repository_identity` points at the source repo,
  leaves the source working tree byte-identical (porcelain snapshot before/
  after), and writes an environment record.
- [ ] Implement; commit.

### Task ENV.2 — archive-before-remove + hygiene
- [ ] Failing tests: run artifacts under a to-be-removed worktree are copied
  to the long-term-history root BEFORE `git worktree remove` (kill -9
  mid-archive leaves either complete archive or untouched original — atomic
  dir swap); `remove_worktree` uses git only (test asserts no `rm -rf`
  syscall pattern by asserting via a wrapper that any raw deletion raises);
  cleanup dry-run by default; project-local `audit-output/audit-council` and
  `eval-live-output` are never relocated by default; sealed benchmark ground
  truth files live under benchmark_corpus root and are NEVER served to
  EvidenceStore consumers (visibility test in PKG-EVID).
- [ ] Implement + write `MIGRATION-RETENTION-RECOMMENDATION.md` (doc only;
  no reorganization without operator approval); commit.

**Acceptance (DoD A1/A2):** release/historical audits self-prepare isolation;
live worktree untouched; artifacts archived before cleanup; linked-worktree
cleanup uses git correctly; project-owned dirs left alone.

---

## PKG-EVID — Provenance-Bound Evidence Store & Cache (pillar B)

**Ownership:** `skill/scripts/evidence_store.py` (new),
`skill/schemas/evidence-record.schema.json` (new),
`skill/tests/test_evidence_store.py`. Depends on PKG-A0 (binding digest),
PKG-SCHEMA (evidence refs).

**Interfaces produced:**
```python
class EvidenceStore:
    def __init__(self, run_dir: str, barrier_state: Callable[[], bool]): ...
    def put(self, record: dict) -> str            # evidence_id; asserts not-finding-shaped
    def get(self, evidence_id: str, consumer: str) -> dict | None  # visibility+barrier filter
    def revalidate(self, record: dict) -> bool    # fingerprint+binding+input+tool+freshness
    def access_log(self, consumer: str | None = None) -> list[dict]
```

### Task B.1 — record shape + anti-conclusion guard
- [ ] Failing tests: put/get roundtrip; kind enum enforced; a document
  shaped like a finding (has `severity`+`claim`+`id`) is rejected fail-closed
  (assertion error path, nothing stored); content-addressed id stability.

### Task B.2 — visibility classes + independence barrier
- [ ] Failing tests (the spec's leakage cases): `AUDITOR_PRIVATE` record
  produced-by OPUS is NOT returned to consumer CODEX while barrier closed;
  IS returned after barrier opens (barrier_state flips); `SHARED_MECHANICAL`
  always served; `POST_BARRIER_SHARED` served only post-barrier; every get()
  appends to access_log; a later artifact citing `evidence_id`s can be
  cross-checked against the log (which-evidence-each-model-saw test).

### Task B.3 — freshness + fresh-required gates
- [ ] Failing tests: reuse allowed only when repository_fingerprint +
  binding_digest + input_digest + tool.version all match and policy is
  CACHEABLE and TTL unexpired; `FRESH_REQUIRED` records NEVER satisfy from
  cache (release-gate case: stored green TEST_RESULT + fresh-required policy
  → `get` returns None with reason `fresh_required`); invalidation on
  tracked_change / head_change / binding_change; run-scoped vs repo-scoped
  validity. Just-in-time refs: serving returns a REF (id + digest + location)
  with content loaded on demand — no cache dumps (test: get() never returns
  the full payload unless `include_content=True`).

**Acceptance (DoD B):** cache contains evidence not findings; bound to
repo/env/tool/input; private evidence hidden across the barrier; stale cache
cannot satisfy a fresh gate.

---

## PKG-PUB — Public Audit Contract (pillar F)

**Ownership:** `skill/PUBLIC-CONTRACT.md` (new),
`skill/schemas/public-contract.schema.json` (new),
`skill/tests/test_public_contract.py`. Depends on PKG-SCHEMA + PKG-TELE
contracts.

### Task F.1 — describe --json + versioned contract doc
- [ ] `audit_council.py describe --json` (lead-approved shared-file edit or
  lead-implemented): emits the versioned contract (protocol_version 2, env
  modes, model roles/independence rules, artifact+evidence semantics incl.
  line_ranges, completeness states incl. INVALID_AUDIT_ENVIRONMENT, governor
  constraints + defaults, brief `target:` metadata format, known limitations,
  runtime capabilities incl. §3.3 enforcement table).
- [ ] Failing tests: output validates against public-contract.schema.json;
  `protocol_version` matches SKILL.md + schemas' `schema_version` (drift
  test); every completeness state in state.schema.json appears in the doc
  (drift test); doc contains no reference to codex_runner/wire_adapter
  internals (grep test); compatibility policy section present.

**Acceptance (DoD F):** a prompt-authoring agent can understand capability
without private runner internals; contract versioned and runtime-consistent.

---

## PKG-EVAL — Eval Suite (pillar D)

**Ownership:** `skill/eval/` tree (new): `tier1_harness.py`,
`tier2_fixtures/` (generator + 10 fixture specs), `tier3_replay.py`,
`scoring.py`, `eval_cli.py`, `skill/tests/test_eval_framework.py`.

### Task D.1 — tier 1 (deterministic harness eval) + scoring skeleton
- [ ] `eval tier1` runs the full unittest suite + the A0.6 matrix and emits a
  scorecard with dimensions FINAL QUALITY/PROCESS/HARNESS/ECONOMICS/DIVERSITY/
  ENVIRONMENT (tiers 2-4 dimensions report "not-run"); ENVIRONMENT dimension
  = pass rate of A0.6 matrix with 100% hard requirement (non-100% → overall
  NOT_READY). Self-tests: scorecard schema, dimension math, sealed-truth
  non-exposure helper.

### Task D.2 — tier 2 seeded fixtures (deterministic, fake models)
- [ ] Fixture generator creates tiny repos with KNOWN ground truth for:
  auth bypass, stale transaction/post-commit recovery, path escape/TOCTOU,
  cross-tenant access, unsafe migration, API drift, release/supply-chain
  issue, evidence provenance mismatch, structural identity mismatch, negative
  controls (protected negatives MUST stay unfound). Each fixture: target,
  sealed ground truth (outside auditor context), severity range, protected
  controls, environment expectations, cost ceiling. Scoring implements
  recall/precision/root-cause fidelity vs the sealed truth; novel
  CRITICAL/HIGH truth rule enforced (agreement alone ≠ truth). Deterministic
  first: driven by `fixtures/fake_codex.py` + scripted Opus-side artifacts;
  real-model tier-2 runs are budgeted separately (see Model-Call Budget).
- [ ] Tier 3: `tier3_replay.py` reads Benchmark 001/Fifth artifacts
  READ-ONLY, replays harness decisions against recorded raw outputs, scores
  PROCESS/HARNESS/ECONOMICS/DIVERSITY — **execution requires the approval
  gate flag** `--i-have-operator-approval` plus a recorded approval line;
  without it the command refuses and prints the gate text.

**Acceptance (DoD D):** deterministic + seeded + historical tiers exist;
environment integrity is a hard requirement; novel-finding truth independently
validated.

---

## PKG-SPEC — Eval-Gated Specialists (pillar C) — kept DEFAULT OFF

**Ownership:** `skill/scripts/specialists.py` (new),
`skill/schemas/specialist-review.schema.json` (new),
`skill/prompts/specialist-domain-review.md` (new),
`skill/tests/test_specialists.py`. Depends on PKG-EVID; activation is
additive machinery only (zero behavior change while counts are 0).

### Task C.1 — registry, pre-frozen activation, blind context
- [ ] Failing tests: default specialist count 0 and `start`-equivalent
  refuses any specialist without a pre-frozen activation reason recorded
  BEFORE first-pass completion (reason recorded after OPUS_INDEPENDENT
  completes → refusal; reason referencing "model already found X" phrasing is
  allowed only if recorded pre-barrier — mechanically: timestamp ordering);
  normal cap 2 / hard cap 3 enforced; blind context builder excludes any
  primary-model finding content (fixture: context contains contract+repo+
  domain+SHARED_MECHANICAL refs only; grep-test for finding JSON absence);
  specialist output candidates flow into normalization as findings with
  `discovered_by: SPECIALIST-<domain>`; specialist NEVER produces final
  verdict (schema has no verdict field; final synthesis treats candidates
  exactly like provisional findings). Budget integration: each specialist
  turn consumes `max_specialist_turns` accounting; `record_omission` used
  when the governor declines a specialist.
- [ ] Implement; commit. **No SKILL.md change that enables specialists by
  default; no real specialist invocation in this program phase.**

**Acceptance (DoD C):** default-off until eval proves value; bounded counts;
blind during domain pass; cannot issue GO/NO-GO.

---

## PKG-INT — End-to-End Integration, Migration, Installation (pillar H) — LEAD

**Files:** `skill/SKILL.md`, `skill/README.md`, `skill/protocols/*.md`
(lifecycle + failure-and-resume updates), `skill/scripts/audit_council.py`,
`skill/scripts/state_store.py`, `skill/tests/test_lifecycle_e2e.py`,
`skill/tests/test_migration_compat.py`, plus integration wiring from all
packages.

### Task H.1 — explicit lifecycle + state v2
- [ ] `state.schema.json` v2: `env_binding_digest`, `phase_skips[]`
  `{skipped_phase, reason, recorded_at}` (replaces implicit timestamp
  filling — `apply_transition` REQUIRES a skip record for any passed-over
  phase that has an artifact expectation, or the transition refuses; the
  Fifth-style "ledger without 32-" path becomes an explicit, reason-carrying
  skip), `budget_omissions[]` (derived), completeness
  `INVALID_AUDIT_ENVIRONMENT`. Old state files (schema_version 1) validate as
  v1 via reader tolerance (never rewritten).
- [ ] `test_lifecycle_e2e.py`: fake-model full run through the §3.2 chain —
  brief → binding freeze → gate → Opus∥Codex independent (fake) → barrier →
  normalization → cross-exam both ways → ledger → adjudication → final →
  metrics → archival; every transition checkpointed and failure-classified;
  injection points assert the right INVALID_* code and ZERO codex launches on
  environment failures.

### Task H.2 — migration & compatibility verification
- [ ] `test_migration_compat.py`: v1.0.3 artifacts from BOTH historical runs
  (copied fixtures) are readable end-to-end (state → artifacts → metrics via
  migration readers) with bytes unchanged; old `evidence.lines`, old metrics
  shapes, `/audit-council <brief>` CLI surface, project-local output layout
  all verified; installed-skill upgrade path = replace directory + rerun full
  suite; rollback = reinstall from `v1.0.3-baseline` tag + byte-verify.

### Task H.3 — SKILL.md v2 orchestration + protocols
- [ ] SKILL.md gains: environment mode resolution + `verify-env` before
  inference phases, `phase_skips` recording on failure-partial advance,
  evidence-ref discipline (cite `evidence_id`s, JIT content), budget
  omission reporting, public-contract pointer; protocols/failure-and-resume
  gains INVALID_AUDIT_ENVIRONMENT handling (never a product verdict);
  README gains hook opt-in instructions + A2 layout description.

### Task H.4 — independent adversarial review (fresh verifier sub-agent)
Checklist (each must be falsified-attempted and resolved): root/same-HEAD
worktree/symlink/tmp escapes; brief root/HEAD mismatch; binding staleness;
cache independence leakage; stale cache satisfying fresh gate; conclusions
cached as evidence; malformed multi-range + canonical weakening; invalid-
output telemetry/elapsed omission; metrics double counting; failed attempt
counted successful; specialist premature visibility or verdict ownership;
ground-truth leakage; cleanup losing artifacts or misusing git worktree;
public contract/runtime drift. Verdict + fixes recorded in
`AUDIT-COUNCIL-V2-IMPLEMENTATION-REPORT.md`.

### Task H.5 — release qualification + installation (ONLY after review green)
- [ ] Full suite (build tree) green; eval tier-1 ENVIRONMENT=100%;
  `AUDIT-COUNCIL-V2-EVAL-REPORT.md` (tiers actually run),
  `AUDIT-COUNCIL-V2-MIGRATION.md`, `AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md`,
  `AUDIT-COUNCIL-V2-IMPLEMENTATION-REPORT.md` written.
- [ ] Gate: historical benchmark rerun + any real-model spend beyond the
  budget table below requires EXPLICIT operator approval (ask, never assume).
- [ ] Install: refresh `~/.claude/skills/audit-council/` from the build tree;
  verify byte identity (`diff -rq` excluding `__pycache__`); run the full
  suite IN the installed copy; verify fresh discovery (invoke `/audit-council`
  in a scratch session, expect argument parse + fast INVALID_AUDIT_INPUT on a
  missing brief); verify `describe --json`; do NOT delete existing
  audit/benchmark dirs; no push/publish.

---

## Test matrix (required by program spec → owning package)

| Requirement | Tests | Package |
|---|---|---|
| all v1/v1.0.3 tests keep passing | existing 11 files (updated only where `lines` asserted) | all |
| A0 confinement (20-case matrix) | test_env_binding / test_path_guard / test_env_lifecycle | PKG-A0 |
| environment manager | test_environment_manager | PKG-ENV |
| evidence cache visibility/freshness | test_evidence_store | PKG-EVID |
| multi-range + migration | test_line_ranges_v2 (+ G.3 Fifth regression) | PKG-SCHEMA |
| telemetry/governor | test_telemetry_v2 | PKG-TELE |
| specialist routing/independence | test_specialists | PKG-SPEC |
| eval framework self-tests | test_eval_framework | PKG-EVAL |
| artifact cleanup/retention | test_artifact_layout | PKG-ENV |
| public-contract compatibility | test_public_contract | PKG-PUB |
| installed-copy tests | full suite in installed dir | PKG-INT H.5 |

## Model-call budget (development)

Order of evidence, cheapest first; every real call recorded in the program
cost log (implementation report):

1. Deterministic unit/integration (this plan) — 0 model calls.
2. Fake/mock model fixtures (existing `fake_codex.py`) — 0 model calls.
3. **Gated smoke A (only if Task G.3 leaves wire-shape doubt):** one tiny
   `codex exec` structured-output call on `smoke-fixture-103`-class fixture
   asking for a two-range evidence item; ≤ ~300k input tokens expected (cached
   ~250k), recorded. Requires lead sign-off before spending.
4. **Gated smoke B (only if hook/wire integration doubt remains):** one tiny
   environment/hook smoke — 0 Codex calls (hook deny path is local).
5. Tier-2 seeded evals with real models: NOT in this program phase; proposed
   separately with per-fixture cost ceilings after RC.
6. Historical benchmark (tier 3 real): ONLY after v2 RC AND explicit operator
   approval. Benchmark 001 is never re-run implicitly.

Fifth/Bench observed economics (ARCHITECTURE §3.5) calibrate all ceilings;
UI quota % is never treated as linear with tokens.

## Rollback strategy

- Task 0 git baseline + `v1.0.3-baseline` tag; per-task commits; package
  branches merged only by the lead. Any package rollback = `git revert` of
  its commits (local only).
- Installed skill: untouched until H.5; rollback = reinstall from the tag +
  byte-verify + installed suite green.
- Schemas: v2 additive with v1 readers; artifacts carry schema_version;
  finalized runs never rewritten, so no data rollback exists or is needed.
- `repro/` and `eval/tier2_fixtures/` are disposable; `repro/tmp/` gitignored.
- Worst case: `git checkout v1.0.3-baseline -- skill/` restores the exact
  v1.0.3 build tree (verified byte-identical to the currently installed copy).

## Changelog (contract changes — lead edits only)

- 2026-09-04: contracts frozen per AUDIT-COUNCIL-V2-ARCHITECTURE §3.4.
- 2026-09-04 (pre-freeze contract clarifications — operator, applied before
  the Task 0 baseline):
  1. `binding_digest` excludes `binding_digest` and `frozen_at` (freeze time
     is metadata); otherwise-identical inputs produce identical digests.
  2. Worktree-blind `.git`-directory discovery eliminated: git plumbing
     (`git rev-parse --show-toplevel`) is the only discovery authority;
     regressions required for main worktree, linked worktree, detached
     linked worktree, nested cwd, non-repo (new Task A0.5; legacy
     `detect_repo_root` rewired in Task A0.6).
  3. Runtime/cache root is injectable (`AUDIT_COUNCIL_CACHE_HOME`, production
     default `${XDG_CACHE_HOME:-~/.cache}/audit-council/`); deterministic
     tests never write the real user cache.
  4. Compound-command confinement validates each segment; ordinary in-root
     `&&`, pipes, and subshells MUST remain usable (false-positive
     regressions required in addition to escape denials).

## Execution handoff

**Plan complete and saved to `plans/audit-council-v2.md`.** Program protocol:
the lead executes Task 0 and shared-file tasks (A0.5, H.*); packages PKG-SCHEMA
and PKG-A0 are delegated first (disjoint files, both dependency-free);
subsequent packages per the integration order in §0 under
multi-agent-orchestration. Two execution options per package: **1.
Subagent-Driven (recommended)** — fresh sub-agent per package with two-stage
review; **2. Inline Execution** — lead executes with checkpoint reviews. The
operator may also adjust package order or budgets before kickoff.
