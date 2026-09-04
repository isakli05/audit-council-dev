# Audit Council v2.0 — Known Limitations

Date: 2026-09-04. Honest inventory after implementation + four
independent adversarial verification rounds. Items marked INHERENT are
accepted design boundaries, not defects; the remainder are concrete
residuals with documented risk.

## Path confinement (A0.3) — runner-enforced, not OS-enforced

1. INHERENT — the PreToolUse hook is a no-inference lexical scanner.
   Encoded or dynamically-constructed payloads
   (`base64 -d | sh`, `chr()`-built or ANSI-C `$'\x2f'` paths,
   interpreter-generated strings) pass it. It is a deny-before-exec
   hardening layer on top of DETECTION (fingerprint freeze + write-guard
   + binding verification), not a sandbox. The systemic fix is an OS
   boundary (Landlock/bubblewrap wrapper for codex, see A0 spike) and
   remains future work.
2. Residual — shell-local indirection the scanner cannot see:
   `X=pw; cat $X` (session-local vars), and dash-named planted symlinks
   (`cat -- -pw`). Guard-visible env vars, bare `$VAR`, `~`, quoted
   absolute paths, interpreter `-c` payloads, joined git flags, mutating
   tools naming harness paths, and single/multi-component symlinks are
   all denied (regression-tested).
3. INHERENT — scan-to-exec TOCTOU (symlink swap after the check).
4. Unkeyed integrity chain: run-dir files (binding, state, checksums)
   use plain sha256 with no secret. Cheap tampering is caught (checksum
   gate on finalize; state-pinned + registry-pinned binding digests; the
   registry lives outside the frozen root), but an attacker with the
   run dir who rewrites files AND recomputes the whole checksum ledger
   can forge consistency. Tamper-evident against non-recomputing edits;
   not tamper-proof.
5. RESOLVED (was: hook requires one-time operator opt-in): the
   PreToolUse hook is now declared in SKILL.md frontmatter and registers
   AUTOMATICALLY when /audit-council is invoked (active for the session,
   inert when no run is active). The no-inference lexical boundary
   itself (item 1-3) is unchanged.
6. RESOLVED (was: codex read confinement not wired): every codex launch
   (fresh + resume) now runs under the bubblewrap OS boundary
   (scripts/codex_sandbox.py; docs/A0-CODEX-CONFINEMENT.md): reads
   outside the enumerated bind set are OS-BLOCKED. Residuals: system
   directories (/etc, /usr) remain readable by design; without bwrap
   (`AC_CODEX_BWRAP=0` or absent) confinement falls back to the accepted
   residual posture (argv/output validation only), recorded per job.

## Evaluation (D)

7. Tier-2 recall/precision SCORING with models (fake or real) is not yet
   wired; fixtures + sealed truths + truth rules are. Specialists stay
   DEFAULT OFF until such evals show net value (they are also mechanically
   refused without a pre-frozen activation reason).
8. Tier-3 replay is approval-gated and has never been executed against
   the sealed historical runs.
9. Benchmark 001's pre-1.0.3 telemetry gap (5 paid attempts, 0 recorded
   invocations) is scored honestly as a HARNESS failure in any replay
   rather than annotated away.

## Telemetry (E)

10. Opus-side usage remains unexposed by Claude Code; never fabricated
    (null = unknown). UI quota percentage is never treated as linear
    with tokens.
11. `phase_attempts` is observational; the governor itself counts from
    job records.

## Evidence store (B)

12. Payloads under `<run>/evidence/objects/` are readable by any in-root
    reader; the visibility barrier and access log govern the STORE API,
    not raw file reads. The store is per-run; REPOSITORY/GLOBAL
    validity_scope reuse across runs is future composition.
13. The finding-shape guard is marker-key based; tabular/string
    re-encodings of conclusions can evade it by construction (it is an
    anti-accident guard, with the kind enum as the real contract).

## Specialists (C)

14. Blindness and grounding are key-name/regex proxies: a caller could
    smuggle primary findings under unlisted key names in `repo_facts`,
    and backdated `recorded_at` values are accepted absent clock
    anchoring. Both require harness-side misuse (the SKILL.md protocol
    is the other half of the enforcement).

## Harness (H)

15. The round-4 security fixes (mutating-tool/harness denial,
    interpreter-payload harness strings, checksum-gated finalize,
    crash-closed hook) have regression tests but no fifth independent
    verification pass — recommended before installation.
16. Two pre-existing v1 quirks retained deliberately: `advance`'s
    harmless dead `return` pair, and instruction-file scanning limited
    to root + first-level dirs.

## Environment (A1/A2)

17. Ephemeral-worktree default root: env-manager uses XDG_DATA while
    artifact_layout documents XDG_CACHE for the same concept — they agree
    under `AUDIT_COUNCIL_ENV_ROOT`/config (all tests inject); production
    default unification (recommend XDG_DATA) is a pending lead decision.
18. No existing artifact directories were migrated or reorganized;
    MIGRATION-RETENTION-RECOMMENDATION.md is a proposal awaiting explicit
    operator approval.
