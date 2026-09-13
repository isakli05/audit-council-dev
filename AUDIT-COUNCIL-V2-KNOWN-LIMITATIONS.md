# Audit Council v2.0 — Known Limitations

Current review basis: **this stabilization candidate itself** (the
qualification-exit stabilization changes shipping in the same commit as
this document — sandbox namespace/env isolation, host-write-free preflight,
content-aware fingerprint v2, bound skip records, run-state locking,
stage-launch gating, v2 evidence-field alignment, generic first-pass
validator, hermetic suite; see the AUCDEV-010 qualification-exit
stabilization record). A commit cannot contain its own final hash, so the
exact candidate SHA is established by the containing commit's parent chain
(recorded in the stabilization report), not by this file. This candidate
has had NO independent audit yet: a fresh external audit of its exact SHA
is required before any qualification claim. The last INDEPENDENTLY
reviewed basis remains the 2026-09-05 review of v2.0.1-equivalent source
`8ae33444f349ce73c1359b963722e2d16acba630` (audited targets since then,
including `c8dda1d0…`, carry their own audit records). Items below
describe THIS candidate's tree truthfully; items 31+ state the
stabilization deltas. See the
[backlog](docs/chatgpt-project/AUCDEV-BACKLOG.md) for ownership and
acceptance criteria.

Date: 2026-09-13 (qualification-exit stabilization revision). Items marked
INHERENT are accepted design boundaries, not defects; RESOLVED items
record what closed them; the rest are concrete residuals with documented
risk.

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
21. PRODUCTION CREATION ROUTE RESOLVED; API DEFAULT DEBT REMAINS:
    environment_manager (XDG_DATA) and artifact_layout (XDG_CACHE) still
    have different uninjected defaults in current source. All
    worktree creation flows through `environment_manager.env_root()`
    (`AUDIT_COUNCIL_ENV_ROOT`, production default XDG_DATA); the
    artifact_layout cache-root entry is still that resolver's default,
    although it is not the production creation route. Injected tests align
    them and do not prove default API parity. AUCDEV-013 tracks reconciliation;
    no historical directories are relocated in this task.
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

## Current control-room review — 2026-09-05

24. Mechanical blind-stage isolation is absent: the wrapper binds the whole
    repository and run, including Opus's already-created independent artifact.
    The protocol forbids cross-pollination, but raw file access is possible.
    EvidenceStore API visibility is not filesystem enforcement, and the library
    is not wired through production stages. AUCDEV-001/017. The operator reports
    exposure in a later dual-model run; exact run ID is not available here.
25. Operator-authorized external or denylisted audit-output ingress is not
    supported by the current source-contained allowlist. The v2.0.1 RELEASE
    staging fix does not implement Evidence Ingress v2. AUCDEV-002.
26. No disposable writable mutation/falsification copy exists. The detached
    RELEASE worktree remains an immutable authoritative target. AUCDEV-003.
27. Completeness/state metadata does not establish mechanical independence or
    effective raw evidence visibility. Failure protocol quota wording can conflict
    with full-completeness semantics; v2 evidence-policy still requests legacy
    `lines`. These executable instructions remain unchanged pending a separately
    qualified correction. AUCDEV-004/008/009/012.
28. Fingerprint comparison does not cover every working-tree byte: tracked
    inventory uses index IDs and dirty-path presence; untracked inventory uses
    names/sizes. Repeated dirty edits and same-size untracked changes can evade
    compared fields. AUCDEV-018; clean exact-target confinement is not a proof
    that CURRENT dirty-tree freshness is complete.
29. Whole-program dynamic-probe/omission governance is not fully integrated;
    equal-timestamp metrics ordering follows directory order and unreadable job
    records are skipped. Existing successful-stage/attempt/repair caps remain.
    AUCDEV-007. Current suite also emits unclosed-file ResourceWarnings (AUCDEV-019).
30. Installed current bytes match 8ae3344 but the committed verified installation
    cites 579e39a. A distinct independent v2.0.1 qualification/install reference
    is unresolved (AUCDEV-010); passing deterministic tests is not qualification.

## Qualification-exit stabilization deltas — 2026-09-13 (candidate review basis)

31. F-A-01/B-001: the bwrap wrapper now unshares PID+IPC+UTS namespaces
    (network shared by design) and clears the environment to an explicit
    minimal set (HOME/PATH/TERM/LANG). The preflight proves the
    /proc/<pid>/root escape is closed and that a host environment marker
    does not leak. The module docstring and the public contract state the
    exact namespace/env boundary; system dirs (/etc, /usr) remain readable
    by design; the ~/.codex auth-boundary residual (item 8) is unchanged.
32. F-A-02/B-002/F-A-03: the sandbox preflight no longer creates ANY probe
    file in the frozen repository root or the operator home — the repo read
    probe reads an existing file, the outside sentinel lives in a
    preflight-owned tempdir, and the only created fixtures are the outside
    sentinel and the run-dir probe (inside the sanctioned writable
    subtree). All probes are argv vectors (no shell string concatenation).
    The repo-write probe attempts creation of `.ac-sbx-write-probe` and
    requires the OS to refuse it; that file can only ever appear when the
    read-only bind is already broken (which is the reported failure).
33. B-003: first-pass independence is now MECHANICAL on the codex side —
    the sandboxed codex independent stage cannot read the peer first-pass
    artifact (shadowed by an empty ro-bind; recorded in the job record).
    The interactive opus side remains protocol-enforced (disclosed; item 24
    partially superseded).
34. F-A-08/B-004: fingerprint v2 is content-aware (`-uall` untracked
    inventory with per-file sha256; dirty-worktree byte map; no untracked
    directory collapse). The write guard and verify inherit it. Bindings
    frozen before algorithm 2 record no `fingerprint_algorithm` and verify
    under the legacy algorithm 1 (reproduced byte-exactly); their blind
    spot is historical and closed only for new runs.
35. F-A-04/F-A-10: the CLI skip vocabulary now equals the state.schema.json
    enum exactly (SKIPPABLE_PHASES single source, drift-tested), save_state
    refuses schema-invalid skip records, and every skip record is bound to
    the exact from→to transition that consumes it and consumed on use;
    legacy unbound records no longer authorize any new transition.
36. F-A-05: run-state mutations (state.json + checksums ledger) serialize
    on a per-run flock; concurrent writers can no longer interleave
    read-modify-write cycles.
37. B-005: model-stage launch is mechanically gated by the authoritative
    state-machine phase (`state_store.check_stage_launch`); the runner
    consults the gate and holds no phase-order policy of its own.
38. B-006/F-A-12 (executable-instruction half): all active executable
    instructions (evidence policy + both codex prompts) now cite the v2
    typed `line_ranges` shape, matching finding.schema.json
    (additionalProperties:false). The evidence-store visibility classes
    remain a library API not wired into production stages — now stated as
    such everywhere a claim could be read (no production control claimed).
39. B-008: the product ships a GENERIC first-pass structural validator
    (`scripts/first_pass_validator.py`) — parameter-driven identity,
    generic self-description, no baked event constants. Frozen binding-v2
    validator bytes remain immutable historical evidence for their event.
40. F-A-11/B-007: `repo_fingerprint.py identity-manifest` emits a
    files-only-verifiable full-target identity document (head/tree sha,
    per-file blob sha + worktree sha256, untracked content digest) with a
    `verify-manifest-files` check an isolated auditor can run against
    handed-off bytes alone.
41. F-A-06: the deterministic suite is hermetic in a clean environment —
    preflight probes use the run's own codex binary (fixture-served), the
    resolver probe defaults to localhost under test injection, the fixture
    codex receives its control knobs via a run-dir file (the sandbox clears
    the environment), and genuinely external conditions (bwrap, production
    codex toolchain, DNS, archived run evidence) are explicitly classified
    skip conditions with reasons rather than silent host state.
42. F-A-07: the PreToolUse hook command resolves interpreter and skill
    directory mechanically and fails CLOSED (deny) when either cannot be
    established; the documented install contents now include `hooks/`.
    F-A-13: the fingerprint-mismatch helper honors its list return
    contract.
