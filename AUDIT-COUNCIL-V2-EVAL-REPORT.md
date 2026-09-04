# Audit Council v2.0 — Eval Report

Date: 2026-09-04. Command: `cd skill && /usr/bin/python3 eval/eval_cli.py tier1`.

## Tier 1 — deterministic harness eval: RUN, PASSING

- **Overall: READY** (environment_integrity_pass: true).
- **ENVIRONMENT: 1.0** — 27/27 mapped mandatory environment-regression
  cases green (the program spec's A0.6 matrix mapped by name across
  test_env_binding.py, test_path_guard.py, test_env_lifecycle.py; 0
  unmapped). Environment integrity remains a hard 100% requirement in
  `scoring.py` — any failing case forces overall NOT_READY.
- **HARNESS: 1.0** — full unittest discovery: **523 tests, OK (~64 s)**
  (v1.0.3 baseline was 160; +363 deterministic v2 tests across 19 files,
  including 22 adversarial-review regressions).
- FINAL_QUALITY / PROCESS / ECONOMICS / DIVERSITY: not-run at tier 1 by
  design (they require model-facing tiers).

## Tier 2 — synthetic seeded fixtures: BUILT (deterministic), model runs NOT executed

All 10 fixture repos build deterministically in ~0.13 s
(`eval/tier2_fixtures.py build_all`), ground truth sealed under
`<root>/sealed/` OUTSIDE every fixture repo (loader fail-closed against
traversal/symlinks): auth-bypass, stale-transaction-recovery,
path-escape-toctou, cross-tenant-access, unsafe-migration, api-drift,
release-supply-chain, evidence-provenance-mismatch,
structural-identity-mismatch, clean-idioms (protected negatives renamed
from "negative-controls" to stop the name itself leaking the answer).
Four adversarial review rounds specifically audited and cleaned the
fixtures of auditor-visible telltales ("DEFECT (seeded)", "protected
control", "suspicious-looking", README announcements) — ground truth now
lives only in the sealed JSONs.

**Not run:** recall/precision scoring with real or fake models — the
fake-model scoring harness and any real-model tier-2 runs are the
model-facing half of D.2 and are budget-gated (see below).

## Tier 3 — historical replay: EXISTS, approval-gated, NOT executed

`eval/tier3_replay.py` implements read-only replay + PROCESS/HARNESS/
ECONOMICS/DIVERSITY scoring over the sealed runs (Benchmark 001
`20260904T014146Z-f3384a`, Fifth `20260904T081903Z-60651d`). It refuses
without `--i-have-operator-approval --approver <name> --approved-at <ISO>`
and performs ZERO filesystem access on refusal. Unit-level tests exercise
the gate and the re-derivation chain on copied fixtures (including the
Fifth's `"184-185, 240-273"` INVALID_OUTPUT reproductions via the current
v2 chain). **No historical run has been re-run or re-audited.**

## Tier 4 — real release-audit observations: deferred by design

## Scoring rules implemented (eval/scoring.py)

- ENVIRONMENT hard gate: overall NOT_READY unless environment fraction is
  exactly 1.0 AND the harness suite passes; the gate survives score
  merging (a historical replay alone can never assert READY).
- Novel-finding truth rule: a claimed new CRITICAL/HIGH is truth only
  with deterministic reproduction, an independent evaluator, human
  confirmation, or predefined runtime/source evidence — model agreement
  alone is never truth (enforced helper + tests).

## Model-call accounting for this report

Zero real Claude/Codex calls. Development budget order was followed:
deterministic unit/integration → fake/mock fixtures (fake_codex.py) →
(no smoke A: the v2 wire path is proven deterministically with the real
Fifth payload through wire_adapter + canonical validation, so no
wire-shape doubt remains to justify a paid smoke) → seeded evals with
models: NOT run (budget-gated) → historical: NOT run (approval-gated).

## Gates now standing (operator decisions required)

1. Fake-model tier-2 scoring harness wiring (deterministic, no budget) —
   recommended next deterministic step.
2. Real-model tier-2 seeded evals — requires budget approval per fixture
   cost ceilings.
3. Tier-3 historical replay execution — requires explicit operator
   approval (`--i-have-operator-approval`).
4. Round-5 independent verification of the round-4 security fixes —
   recommended before installation.
5. Installation to `~/.claude/skills/audit-council/` — release
   qualification only.
