# Migration & Retention Recommendation (Audit Council v2 — Pillar A2)

Status: RECOMMENDATION ONLY. No directory has been reorganized, moved, or
deleted. Every action listed under "Recommended operator actions" requires
EXPLICIT operator approval before anyone executes it (program constraint:
existing project-owned audit-output and eval-live-output directories are never
silently relocated; historical runs are read-only evidence).

## 1. What exists today (v1.0.3 layout — unchanged by v2)

| Content | Location | Notes |
|---|---|---|
| Run artifacts | `<repo>/audit-output/audit-council/<run-id>/` per audited repo | project-local, checksummed, finalized runs byte-frozen |
| Historical audit evidence | `/home/isa/audits/**` | READ-ONLY, never modified or re-run without approval |
| Benchmark corpus + results | `/home/isa/benchmarks/**` | READ-ONLY ground truth; must stay sealed away from EvidenceStore consumers |
| Runtime/cache state (active-run registry) | `${XDG_CACHE_HOME:-~/.cache}/audit-council/` (injectable via `AUDIT_COUNCIL_CACHE_HOME`) | ephemeral |
| Eval live output | `eval-live-output` (project-local) | project-owned |

## 2. v2 category model (implemented in `skill/scripts/artifact_layout.py`)

`resolve_roots()` resolves five categories; defaults PRESERVE v1:

| Category | Default | Override |
|---|---|---|
| PROJECT EVIDENCE | `<repo>/audit-output` | config `project_evidence` |
| RUN ARTIFACTS | `<repo>/audit-output/audit-council` (policy flag `project_local`) | config `run_artifacts` (policy becomes `config_override`) |
| EPHEMERAL WORKTREES | `${XDG_CACHE_HOME:-~/.cache}/audit-council/worktrees` (or `AUDIT_COUNCIL_ENV_ROOT` when set) | config `ephemeral_worktrees` |
| BENCHMARK CORPUS | `${XDG_DATA_HOME:-~/.local/share}/audit-council/benchmark` | config `benchmark_corpus` |
| LONG-TERM HISTORY | `${XDG_DATA_HOME:-~/.local/share}/audit-council/history` | config `long_term_history` |

The optional JSON config (path passed to `resolve_roots`) accepts any root
under a top-level key or an `"roots": {...}` subsection, plus `"repo"` to pin
the project-local base without depending on the CWD.

`environment_manager` lifecycle guarantees that make the split safe:

- Worktrees are ephemeral and git-managed: created with
  `git worktree add --detach` under the env root, removed only via
  `git worktree remove` (never raw deletion), and only AFTER
  `archive_run` copied the run dir into LONG-TERM HISTORY via an atomic
  directory swap (`<dest>.tmp-<pid>` then `os.rename`; a crash mid-archive
  leaves the original untouched and no partial archive visible).
- `cleanup()` is dry-run by default. Even with `dry_run=False` it removes
  only ephemeral worktrees of runs that have no active-run registry entry and
  no unarchived audit-output artifacts. LONG-TERM HISTORY and archives are
  never removed by `cleanup` — retention there is an operator decision.

## 3. Recommended operator actions (each gated on explicit approval)

1. **Do nothing initially.** The default layout keeps all v1 locations valid;
   v2 only adds new roots for worktrees/history/benchmarks going forward.
2. *(Optional)* Adopt a shared LONG-TERM HISTORY root for NEW finalized runs
   by writing a config file with `long_term_history` and wiring it into the
   run lifecycle (lead task PKG-INT H.1). Existing project-local run dirs are
   NOT moved; at most, an operator may `cp -a` (never `mv`) a finalized run
   into the history root after verifying `checksums.sha256` — originals stay.
3. *(Optional)* Retention: proposed default is KEEP FOREVER for archived runs
   (they are small JSON artifacts; the expensive raw logs already live inside
   them). If storage ever matters, prune history entries older than N months
   ONLY after exporting `99-run-metrics.json` summaries — and by an explicit
   command, never automatically.
4. *(Optional)* Point BENCHMARK CORPUS at a read-only mirror of
   `/home/isa/benchmarks` (copy, not move) so eval tiers can consume it
   without write access to the sealed originals.

## 4. Open wiring decisions for the lead (no action taken here)

- **Worktree default divergence.** `environment_manager` defaults its env
  root to `${XDG_DATA_HOME:-~/.local/share}/audit-council/worktrees` (per the
  frozen A1 contract paragraph, which explicitly retracted the cache-root
  placement), while `artifact_layout`'s documented default for EPHEMERAL
  WORKTREES is the `${XDG_CACHE_HOME}` one from the A2 paragraph. They agree
  whenever `AUDIT_COUNCIL_ENV_ROOT` or a config override is set (all tests
  inject it). The lead should pick ONE production default (recommendation:
  the XDG_DATA one, since worktrees hold audited state, not rebuildable
  cache) and align `artifact_layout._default_ephemeral_worktrees()` if
  desired — a one-line change.
- **Shared test wiring.** `skill/tests/test_schema_validation.py` hard-codes
  the schema-file count (9), an expected name list, and a `BUILDERS` entry
  per schema. The two new v2 schemas (`environment-record.schema.json` from
  PKG-ENV, `evidence-record.schema.json` from PKG-EVID) require lead edits
  there: count 9→11, both names in `test_expected_schema_set`, and
  representative-instance builders (a validated builder for
  environment-record is available in the PKG-ENV delivery report; a
  four-loader-error failure is otherwise observed at discovery time).
- **Record integration.** `environment_manager.prepare()` persists
  `<env-root>/<run-id>/environment-record.json`; PKG-INT H.1 should link the
  record (e.g. copy into the run dir and reference `env_binding_digest`) when
  wiring `--isolated`/`--target` preparation into `audit_council.py`.

## 5. Invariants preserved

- Historical runs (Benchmark 001, Fifth, smoke fixtures) untouched.
- Project-local `audit-output/audit-council` and `eval-live-output` are never
  relocated by default or by `cleanup()`.
- Deterministic tests never write the real user home: all roots are
  injectable (`AUDIT_COUNCIL_ENV_ROOT`, `AUDIT_COUNCIL_CACHE_HOME`,
  `XDG_DATA_HOME`, `XDG_CACHE_HOME`) and every PKG-ENV test injects
  disposable sandbox paths (verified by a dedicated regression test).
