# Audit Council v2.0 — Known Limitations

Date: 2026-09-04 (final release-qualification revision; reflects the tree
after SIX independent adversarial verification rounds and the wired
fake-model Tier-2 harness). Items marked INHERENT are accepted design
boundaries, not defects; RESOLVED items record what closed them; the rest
are concrete residuals with documented risk.

## Path confinement (A0.3) — Claude side (pre-tool, mechanically denied)

1. INHERENT — the PreToolUse hook is a no-inference lexical scanner.
   Encoded or dynamically-constructed payloads (`base64 -d | sh`,
   `chr()`-built or ANSI-C `$'\x2f'` paths, interpreter-generated strings)
   pass it. It is a deny-before-exec hardening layer on top of DETECTION
   (fingerprint freeze + write-guard + binding verification), not a
   sandbox.
2. Residual — shell-local indirection the scanner cannot see:
   `X=pw; cat $X` (session-local vars), and dash-named planted symlinks
   (`cat -- -pw`). Guard-visible env vars, bare `$VAR`, `~`, quoted
   absolute paths, interpreter `-c` payloads (incl. harness-path
   strings), wrappers, joined git flags, mutating tools naming harness
   paths, single/multi-component symlinks, and Glob patterns (including
   post-metacharacter and brace-alternative escapes) are all denied —
   regression-tested across rounds 4–6.
3. INHERENT — scan-to-exec TOCTOU (symlink swap after the check), also
   present at evidence-staging realpath→copy and wrapper-construction
   realpath→mount; the accepted class for every deny-before-exec layer.
4. Unkeyed integrity chain: run-dir files (binding, state, checksums) use
   plain sha256 with no secret. Cheap tampering is caught (checksum gate
   on finalize; state-pinned + registry-pinned binding digests; the
   registry lives outside the frozen root); an attacker with the run dir
   who rewrites files AND recomputes the whole ledger can forge
   consistency. Tamper-evident, not tamper-proof. Unpinned registry
   entries would be unanchored, but the v2 CLI always writes the pin.
5. RESOLVED (was: hook requires operator opt-in): the PreToolUse hook is
   declared in SKILL.md frontmatter and registers AUTOMATICALLY when
   /audit-council is invoked (session-scoped, inert with no active run).
6. Registry hygiene (round 6): registrations whose run dir disappears are
   pruned at every registration, and every test/harness spawner isolates
   its cache — the full suite leaves the real user cache empty
   (regression-tested). A dead entry CAN still appear if a host-level
   actor (outside all sandboxes) deletes a run dir mid-session; until the
   next registration prunes it the hook denies all tool calls
   (fail-closed, correct direction).

## Codex confinement (A0.3) — OS boundary

7. IMPLEMENTED (was: not wired): every codex launch (fresh, resume,
   repair) runs under bubblewrap (`scripts/codex_sandbox.py`;
   docs/A0-CODEX-CONFINEMENT.md). Reads outside the enumerated bind set
   are OS-BLOCKED; the repo is read-only; the run dir is the only
   writable repo subtree; `/tmp` is a fresh tmpfs with only authorized
   fixture roots bound; a caller-supplied `--codex-bin` contributes a
   single FILE bind (no directory, no sibling exposure); the run dir's
   realpath must lie under the frozen root at wrap time.
8. ACCEPTED RESIDUAL — **the bind set exposes `~/.codex` (read-write) to
   the Codex process because subscription auth and session state require
   it**: resuming the exact thread, `codex login status`, and session
   persistence all read/write `~/.codex`, and ChatGPT-subscription
   authentication is the only permitted auth mode (PAYG fails preflight).
   A model-generated command inside codex can therefore read codex's own
   auth/session material — the same access the codex process itself
   legitimately has on the host. This is an AUTH-BOUNDARY residual,
   accepted deliberately in exchange for subscription auth +
   explicit-session resume; it is not path confinement and is never
   claimed as such.
9. Residual — system directories (`/etc`, `/usr`, `/lib`) remain
   readable inside the wrapper by design (CA roots, resolver,
   toolchain). Without bubblewrap (`AC_CODEX_BWRAP=0` or absent),
   repo-root READ confinement is NOT ENFORCED / accepted residual
   (argv+output validation only), recorded per job as
   `sandbox.active=false`.
10. INHERENT — launch-time TOCTOU between the wrap-time realpath checks
    and the mount (the documented class); `run_dir == repo_root`
    equality would rw-bind the whole repo but is reachable only by the
    trusted caller (no model-reachable path).

## Evaluation (D)

11. Fake-model Tier-2 scoring IS wired (`eval/tier2_scoring.py`,
    `eval_cli.py tier2-score`; tests/test_tier2_scoring.py): scripted
    artifacts derived from sealed truth driven through the REAL state
    machine — 10/10 fixtures recall = precision = 1.0, protected
    controls 0 violations, seeded false positive rejected in-pipeline.
    It validates the SCORING machinery and pipeline honesty, NOT model
    capability. Real-model Tier-2 has never been run (budget-gated).
12. Tier-3 replay is approval-gated; it scored the sealed historical
    runs from recorded artifacts only (read-only; no re-audit, no new
    inference).
13. Benchmark 001's pre-1.0.3 telemetry gap (5 paid attempts, 0 recorded
    invocations) is scored honestly as a HARNESS failure in replay
    rather than annotated away.

## Telemetry (E)

14. Opus-side usage remains unexposed by Claude Code; never fabricated
    (null = unknown). UI quota percentage is never treated as linear
    with tokens.
15. `phase_attempts` is observational; the governor counts job records.

## Evidence store (B)

16. Payloads under `<run>/evidence/objects/` are readable by any in-root
    reader; the visibility barrier and access log govern the STORE API,
    not raw file reads. Per-run store; cross-run reuse is future work.
17. The finding-shape guard is marker-key based; tabular/string
    re-encodings evade it by construction (anti-accident guard; the kind
    enum is the real contract).

## Specialists (C)

18. Blindness and grounding are key-name/regex proxies: primary findings
    could be smuggled under unlisted key names in caller-supplied
    `repo_facts`, and backdated `recorded_at` values are accepted absent
    clock anchoring. Both require harness-side misuse; SKILL.md protocol
    is the other half of the enforcement. DEFAULT OFF stands.

## Harness (H)

19. SIX verification rounds total (rounds 1–5 qualification-era; round 6
    scoped to the round-5 fixes); every finding resolved with
    regressions (`tests/test_review_hardening.py`,
    `tests/test_codex_sandbox.py`). Round-6's issues (Glob
    post-metacharacter escapes; test-suite cache leakage bricking the
    auto-hook) were fixed and reverified.
20. Two v1 quirks retained deliberately: `advance`'s harmless dead
    `return` pair; instruction-file scanning limited to root +
    first-level dirs.
21. RESOLVED (was: ephemeral-worktree default-root divergence between
    environment_manager (XDG_DATA) and artifact_layout (XDG_CACHE)): all
    worktree creation flows through `environment_manager.env_root()`
    (`AUDIT_COUNCIL_ENV_ROOT`, production default XDG_DATA); the
    artifact_layout cache-root entry remains a documented layout OPTION,
    never used as a default — and every test injects its own root, so
    the two never disagree in practice.
22. No existing artifact directories were migrated or reorganized;
    MIGRATION-RETENTION-RECOMMENDATION.md remains a proposal awaiting
    explicit operator approval.

## v2.0.1 operational hardening (production run 20260904T222609Z-da27c0)

23. The first production run exposed three bwrap execution-environment
    defects (toolchain bound but absent from PATH → `execvp codex`
    failure; broken system node selected → libada.so.3; dangling
    resolv.conf symlink → DNS/model-refresh timeouts), a RELEASE
    staging contract violation, unreadable skill-owned protocols, and a
    record-vs-binding digest divergence. ALL FIXED in v2.0.1 with
    Tier-4 regressions (tests/test_tier4_da27c0.py, 16 tests); a
    zero-inference sandbox preflight now gates every codex launch
    BEFORE attempt accounting. The historical da27c0 run is preserved
    read-only and is NEVER rewritten.
