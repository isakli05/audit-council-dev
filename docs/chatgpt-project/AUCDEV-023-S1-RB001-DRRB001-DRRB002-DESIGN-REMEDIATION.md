# AUCDEV-023 S1 — RB-001 DR-RB-001 / DR-RB-002 BOUNDED EXEC-REACH DESIGN REMEDIATION + VALIDATION-CLOSURE DESIGN

- **Authority (operator-granted, design-remediation only):** `AUCDEV-023-S1-RB001-DRRB001-DRRB002-DESIGN-REMEDIATION-20260923-01` — DESIGN-ONLY / ZERO-RUNTIME-IMPLEMENTATION, over target findings `AUCDEV023-CR-S1-RB001-DR-RB-001` (SE_POSITIVE_RC_DOES_NOT_PROVE_CLIENT_EXEC_REACH) and `AUCDEV023-CR-S1-RB001-DR-RB-002` (SYNTHETIC_SIGNAL_VALIDATION_DOES_NOT_EXERCISE_ACTUAL_BWRAP_CLASSIFIER_PATH).
- **Session role:** BOUNDED DESIGN REMEDIATOR + VALIDATION-CLOSURE DESIGNER + RECORD PUBLISHER ONLY. NOT Auditor-A/B, NOT the Control Room decision-maker, NOT an execution controller, NOT an implementation / boundary-launcher / driver / EBS / package / binding / event-generation / replacement-first-pass / qualification / installation authority. An honest proof of impossibility or required mechanism choice was an acceptable result and was NOT forced toward a proof.
- **Activity class:** ZERO-RUNTIME / ZERO-IMPLEMENTATION / ZERO-AUDITOR / ZERO-PROVIDER design remediation + read-only exact-evidence verification + local deterministic host mechanical probes (no model/provider/client call, no network, no real-attempt-namespace access) + reference-model design validation + canonical governance publication.
- **Date:** 2026-09-23 (Europe/Istanbul).
- **RB-001 status after this record:** **OPEN at DR-RB-001/DR-RB-002 DESIGN-REMEDIATION strength.** ZERO implementation occurred; no replacement execution, implementation, event, attempt, qualification or installation is authorized by this record.

---

## 1. Mandatory live bootstrap (performed BEFORE any design work)

- Live GitHub default branch `master`; `git ls-remote origin master` = `7578d47785172e6c86de883ccabc8b138a89b0e3` = local HEAD — the EXACT authorized baseline; STOP-WITHOUT-MUTATION clause NOT triggered.
- Root tree `fa8e29c95a8da5631c075c8425fec2a8183f3508`; sole parent `b963245e5f3be8150a5eaf3c5c96c7a9c1239eeb` — both EXACT.
- Canonical blobs at the baseline, all EXACT: CURRENT-STATE `c389c17320948fe24a7a44ad37dc9df0853bc06b`; BACKLOG `470654f8ea2ff84907919608f1161c962155f28d`; CR readback record `29cc15e7838a9ce0a43d9570a0b914dd61209ad4`; predecessor design-remediation record `5eddc9505c7d7eb35aa2e01f5968ad3041a7957b`.
- Protected trees at the baseline, all EXACT and byte-unchanged by this session: `bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0` (the remediated EBS); `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`; `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f` (the latter two equal the frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322`).
- Tracked working-tree drift at bootstrap: NONE (zero tracked modifications; the long-known smoke-fixture gitlink drift does not appear in `git status --porcelain --untracked-files=no` at this bootstrap and no protected/docs path is touched).

## 2. Exact evidence re-verification (read-only; nothing executed, nothing altered)

| Artifact | Identity (re-hashed/verified by this session) | Status |
|---|---|---|
| EXEC-05 driver `aucdev023-firstpass-exec05.py` | `d4d1eca2baa3b8f50aa7f666986cf4d1e6ca4cf2bc09ea2dfe6feca503032357`, 117120 B, mode 0700; `:1798` keys-only `metadata_keys` reduction re-confirmed the SOLE `result.metadata` consumption; `:1869` driver failure-path `repr(exc)[:2000]` re-confirmed informational | EXACT |
| EXEC-05 wrapper `run-aucdev023-firstpass-exec05.sh` | `17e0abcd34303d0defda2326587cb80550872e8ebdb55b1055fb880e6d06534c`, 2836 B, mode 0700 | EXACT |
| Predecessor generated-LAST review handoff | `AUCDEV-023-S1-RB001-DESIGN-REMEDIATION-REVIEW-HANDOFF.tar.gz` outer `f71894fb6343a303367f76e9a89e01b6493bfbc1beac84af89ab981d60ab0827`, 812156 B | EXACT (relied on as packaged evidence source) |
| Frozen boundary launcher (BOTH role packages) | `2efb666042e44d272a53f9ad4ac93a19c14f1687a33fb38ed84f9823d9bc44a7`, 27719 B, `cmp` A↔B byte-identical (re-verified) | EXACT |
| MANIFEST A/B | `2f8efbd65c930da9f6ab68b3921bf74961d0cb8eaf0324b0d14ef439107d8e8d` / `15729d8bac5ee61f0c317c15fe9318100f942751802bb87b9f7a754ded9d7440` | EXACT |
| Bindings A/B | `5204d90e451df4098423a0b4a9b4bd97859496dee1ad384da2e1c49f48a3efe3` / `489a3c911d00d109054e108fa0c89e878fa14f908e01f320022b6bbd1888ade4` (both pin boundary `2efb6660…`) | EXACT |
| EBS source (protected tree) | `ebs/launch.py` Git blob `063b6ce1f4c726bd6ba809f605a115511667fb09`; `reportcustody.py` blob `18f1cc600c684e520b72026e0b4cdf8ba6287cb9`; `binding.py` blob `47eeb5171e9b50b09668aa672b6458c2ea33dd05` | EXACT, read-only |
| Vendored frozen bwrap (the ACTUAL composition engine — frozen source `boundary_engine_source()` binds the package payload bytes for BOTH roles) | `payload/runtime/codex-0.154.0-linux-x64/codex-resources/bwrap` = `01fb705f067bd5365b63d8ad2323a61c8d007733ca5e649437e086f3fb9935d8`, 529776 B, ELF static-pie stripped (manifest row in package-auditor-b; Auditor-A stages the identical vendored bytes as a shared boundary-component row) | EXACT, NOT executed |
| Host bwrap analog | `/usr/bin/bwrap` bubblewrap 0.12.0, `8dea6d013ac3a476f1964ffc6d407a3b6223f43cd4a0c43207146a5cefe59882`, 88560 B | executed ONLY for the mechanical probes of §4 |
| Auditor-A frozen report | identity only `ba8a29a12867273616143e48a86f101f14f6e0e207136d83b31e7fd2426ec1a0` / 23727 B / 0444 | referenced mechanically ONLY; NEVER opened |

## 3. Governing findings (canonical, preserved verbatim in intent, NOT weakened)

DR-RB-001: `tokens=="SE" AND client_returncode>=0 → CLIENT_EXECUTED / true / PROVEN_TRUE` is INVALID — `tokens="SE", rc=137` is compatible with BOTH post-exec death AND death in the `[E, execve)` pre-transition window; future classifiers MUST classify the mechanically ambiguous "SE" signal-death family honestly as UNDETERMINED unless an additional trusted mechanism proves completion of the exec transition; NO rc sign/value inference alone may close that gap.

DR-RB-002: the previous 83/83 suite truthfully passed but never fed the actual/probed composition exit-code semantics through the classifier; future validation MUST exercise `"SE"`+137, shell-style 128+n, direct negative rc, ambiguity-preserving expectations and vendored-bwrap implementation-time probes.

**Event vocabulary fixed by this record (never conflated again):** `EXEC_CALL_IMMINENT` — INNER wrote `E`, the instruction immediately before the exec call; `EXEC_TRANSITION_COMPLETED` — the process image BECAME the intended auditor. The E token proves ONLY the first. These are different events and are not renamed into each other anywhere in this design.

## 4. Host mechanical probes (21 records; `host-bwrap-probes.py` → `probe-results.json`)

All local, deterministic, fresh `mkdtemp`, zero network/provider/client/credential, vendored bwrap NOT executed. Selected OBSERVED FACTS:

- **P1 exit conventions:** child SIGKILL → composition rc **137** (positive 128+n); SIGTERM → **143**; `exit 7` → **7**; `exit 137` (NORMAL, no signal) → **137**; `exit 0` → **0**. The 137-collision is mechanically demonstrated.
- **P2 raw wait status:** for a signal-killed child the composition's RAW waitpid status decodes **EXITED(137)** — byte-identical (`35072`) to the normal-`exit 137` case: the child's termination CAUSE is destroyed by the bwrap synthesis at the boundary's wait interface. Direct (no bwrap) SIGKILL control: Python rc **−9**.
- **P3 fd passthrough + CLOEXEC:** the normalized fixed fd 8 passes through the host bwrap into the payload (token `S` written from inside), and EOF arrives exactly at the payload's execve of a replacement image.
- **P4 supervisor fd non-retention:** with the payload closing fd 8 and sleeping, EOF is observed at the outer **0.02 s later while the composition is still alive** — neither bwrap level retains the write end (host analog; vendored fixture mandated).
- **P5 process topology + outer observation:** host bwrap 0.12 unprivileged topology is THREE levels — spawned outer bwrap → **resident inner bwrap (payload's parent, exe=bwrap)** → payload; outer discovery must walk two levels. With that, the OUTER observer reads the payload's `/proc/<pid>/exe` across the pid-namespace boundary and observes the image transition (`python3.14` before → `/usr/bin/sleep` after).
- **P6 in-sandbox witness:** a trusted INNER-analog forks an auditor-analog child, matches `/proc/<child>/exe` `(st_dev, st_ino)` against the intended executable INSIDE the namespace-local `/proc`, and writes the post-proof token `A` only on positive match — tokens `SA`, rc 0.
- **P7 supervisor external kill:** raw status SIGNALED(9) (Python rc −9) at the composition level; `--die-with-parent` (present in the frozen composition args, source-verified) kills the payload; client fate NOT determined.
- **P8 grace expiry:** no EOF within a bounded grace while a live holder exists (fail-closed class, host-analog).
- **P9 THE AMBIGUOUS TRIPLE (the DR-RB-001 core, mechanically reproduced):** H1 kill in `[E, execve)` / H2 post-exec client SIGKILL / H3 post-exec client NORMAL exit 137 — ALL THREE produce the byte-identical observation `tokens="SE", rc=137, EOF-within-grace`.
- **P10 rc==0 cell:** post-exec client exit 0 → `("SE", 0)`.

## 5. Primary design question — determination

**WHAT IS THE MINIMUM TRUSTED MECHANISM, IF ANY, THAT CAN PROVE THE INTENDED AUDITOR EXEC TRANSITION ACTUALLY OCCURRED?**

**Answer (three-part, precise):**

1. **Within the existing channels — PARTIALLY.** Two proof channels exist INSIDE the current boundary+driver trust surface without any protocol addition: the **rc==0 structural lemma** (assumptions L-A..L-D below) and the **report-present transitive lemma** (R-A..R-C). Both were already recognized transitively in the predecessor chain and are here formalized with explicit assumption stacks and mandatory vendored-bwrap fixtures.
2. **For the residual `"SE" + rc>0 + report-absent` cell — NO, by an admissible-channel impossibility argument.** Histories H1/H2/H3 of probe P9 produce byte-identical observations on EVERY admissible channel (tokens, collapsed rc, report absence; timing is inadmissible by governing rule). The two histories differ only in whether the transition completed; no admissible channel carries that bit; therefore NO classifier over the admissible channels can separate them. This is information-theoretic, not incidental — and it is NOT closable by wait-status analysis (§8).
3. **By ADDING a designed in-surface identity channel — YES.** A positive `/proc/<pid>/exe` `(dev, ino)` match against the fd-verified auditor image PROVES the transition completed: `/proc/exe` resolves to the file backing the CURRENT image and changes ONLY via execve, so the only way a process's `/proc/exe` can read as the auditor is to have completed the execve onto it — **unforgeable by construction, one-sided** (no match ⇒ UNDETERMINED, never FALSE). Two variants are designed (§6B/W): both stay inside the existing trust surface (trusted INNER / trusted launcher; no EBS change; no new trusted binary; no new privileged supervisor), and both are host-analog demonstrated (P6/W01, P5). Neither is implemented; adoption is a governance decision (§14/§18).

**CAN ACTUAL AUDITOR EXEC REACH BE PROVEN WITHIN THE CURRENT BOUNDARY+DRIVER TRUST SURFACE?** — **PARTIALLY: YES for the rc==0 and report-present cells (structural/transitive proofs, existing surface); NO for the `"SE"+rc>0+report-absent` cell through any manipulation of the existing channels (impossibility proven, §5.2); YES for that cell too IF one of the designed exe-identity witnesses is adopted — a mechanism addition INSIDE the existing trust surface (no EBS change, no trust-boundary expansion), requiring its own implementation authority.**

## 6. Required alternatives analysis

### 6.A Conservative semantic downgrade — SELECTED as the corrected default protocol (level L1)

The three-token S/E/I/X structure is KEPT; the classification is corrected: `"SE"` + rc>0 → **`EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS`** with `client_exec_reached = UNDETERMINED` (null); `"SE"` + rc<0 → `OUTER_SIGNAL_DEATH_STAGE_UNDETERMINED`; `"SE"` + rc==0 → `CLIENT_EXECUTED_EXIT_0` **PROVEN_TRUE** (structural lemma); report-present → `CLIENT_EXECUTED_REPORT_PRESENT` **PROVEN_TRUE** (transitive lemma); grammar/transport violations and impossible combinations fail closed (`EXEC_STATUS_PROTOCOL_VIOLATION` / `EXEC_STATUS_CONTRADICTION`).

- RB-001 diagnostic questions closed by L1: every pre-INNER/INNER-failure class (D-class discrimination for `""`/`S`/`SI`/`SEX` — exec PROVEN_FALSE for ANY rc sign); post-exec completion with exit 0; post-exec completion with report; timeout/exec-fail/argv-refusal classes (unchanged from the predecessor variant schema).
- Questions left honestly unresolved: the `"SE"+rc>0+report-absent` cell (the historical Auditor-B rc=1 REPORT_MISSING cell becomes `EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS` — materially better classified than today's indistinguishable D/E collapse: the E token proves the trusted INNER reached the exec call site, eliminating every pre-E failure class; but D-vs-E in the narrow sense (transition completed vs killed in-window) remains UNDETERMINED); pre-INNER 4-vs-5 indistinguishability (unchanged residual, immaterial to D-vs-E).
- Sufficiency for DR-RB-001: the finding's defect is the INVALID PROVEN_TRUE claim. L1 eliminates every invalid proof claim and satisfies the mandated honesty rule exactly. It closes DR-RB-001 at design strength WITHOUT proving actual client execution for the ambiguous cell — permitted, because the finding demands honesty, not clairvoyance (§14).

### 6.B Post-exec trusted witness (identity channel) — DESIGNED (level L2), NOT implemented; governance decision required

**W1 (primary): in-sandbox resident-parent fork-witness.** The revised trusted INNER keeps the S/I/E discipline, then instead of exec'ing the auditor itself: `fork()`; the CHILD execve's the fd-verified auditor (on failure writes `X`, `_exit`); the PARENT (witness, survives the transition) bounded-polls `/proc/<child>/exe` `(st_dev, st_ino)` against the auditor bind (the SAME dev+ino discipline the frozen launcher already uses in `resolve_auditor_path`), and on positive match writes token `A` (post-proof), then `waitpid`s the child and forwards its status (`WIFEXITED` → same code; `WIFSIGNALED` → `128+n` — numerically the SAME shell convention bwrap itself uses, P1). Grammar: `""`,`S`,`SI`,`SE`,`SEF`(fork failed),`SEX`(child execve failed),`SEA`(transition proven).
- Trusted process: INNER (already trusted; NO new binary, NO supply-chain addition). Namespace: everything inside the existing sandbox; namespace-local `/proc` (already mounted `--proc /proc`). Observation: `(dev, ino)` of `/proc/<child>/exe`. Pre-exec forgery: IMPOSSIBLE (W-A..W-C) — the only way to make `/proc/exe` read as the auditor is to complete the execve onto it; the witness writes `A` only after ITS OWN positive match; the client holds no write end (CLOEXEC). Kill windows: `[E,fork)` / `[fork, child-execve)` / witness-killed-before-match → no `A` → honestly UNDETERMINED (one-sided; false negatives admitted); witness killed AFTER `A` → `A` is already durable in the pipe buffer → PROVEN. TOCTOU: `/proc/exe` stat is an atomic kernel snapshot. Signals: child signal-death forwarded as 128+n (convention collision with normal exits REMAINS for cause-analysis but is IRRELEVANT to exec-reach once `A` exists — rc carries no exec information post-proof). Trust boundary: UNCHANGED surface (INNER is already trusted; no EBS contract change; no package identity formula change beyond the boundary row). Controllerless/process-bound architecture: PRESERVED (no controller, no supervisor outside the existing tree). Cost: the auditor is no longer the namespace init (it is the witness's child); composition rc becomes witness-forwarded (numeric convention identical); INNER complexity grows (orphan reaping as PID 1, signal forwarding, fork failure class `SEF`).
**W2 (alternative): outer concurrent observer.** The trusted launcher runs an observer thread during `subprocess.run`: two-level payload discovery (P5 topology), polls `/proc/<payload>/exe` `(dev, ino)` vs the fd-verified auditor; a positive is persisted as `exec_witness_observed=true` and proves the transition identically. NO INNER/topology/rc change; but depends on the bwrap process model (vendored fixture), reads sandbox processes from the host `/proc` view, and misses fast-exiting clients more often (one-sided false negatives only). DESIGNED, host-analog demonstrated (P5), NOT implemented.
**B2 (EOF-while-alive) — REJECTED as a strict proof, recorded why:** P4 shows EOF-while-alive IS observable (supervisor non-retention), and P3 shows EOF at execve; BUT a SIGKILLed process closes its fds during `do_exit()` BEFORE it becomes a waitable zombie, so "EOF observed, `waitpid(WNOHANG)` says alive" is realizable by a DYING process in a microscopic race — EOF-while-alive is not a strict proof, only a corroborating signal. Additionally it would depend on vendored-bwrap non-retention. REJECTED for PROVEN_TRUE use; the token grammar does not use it.

### 6.C Double-exec / trampoline — REJECTED

Five-step chain: (1) EBS→boundary exec; (2) boundary→bwrap; (3) bwrap→INNER; (4) INNER→trampoline; (5) trampoline→auditor. A marker emitted after (4) proves ONLY trampoline exec — NOT auditor exec (the exact conflation §C forbids). If the trampoline performs the final exec, the new `[E2, execve-auditor)` kill window re-appears with IDENTICAL structure (marker written, transition not completed, signal death surfaces 128+n) — the ambiguity is MOVED, not resolved. A trampoline additionally introduces a new trusted binary (supply-chain + qualification expansion). REJECTED. (W1's witness is NOT a trampoline: the witness does not exec the auditor IN ITS OWN IMAGE — the child does — and the proof is an identity observation of the child, not a marker before a further exec.)

### 6.D Parent/proc observation — analyzed; the identity primitive is adopted as W1/W2's core

`/proc/<pid>/exe` is THE canonical one-sided unforgeable prover: exe changes only via execve; a positive `(dev, ino)` match equals a completed transition at or before the observation instant. PID addressing: inside (W1) the parent knows the child pid exactly (no scanning); outside (W2) two-level topology discovery is required (P5; vendored fixture). bwrap DOES introduce a PID namespace; parent-namespace `/proc` still shows descendant tasks (P5 demonstrated). Observation-vs-exit races: a dead/gone pid ⇒ read failure ⇒ UNDETERMINED (fail-closed), never FALSE. Failed observation = UNDETERMINED; successful observation = unforgeable PROVEN_TRUE (W-A..W-C). pidfd: useful for wait-race hygiene, provides NO exe identity — not required by the design. ptrace `PTRACE_EVENT_EXEC`: would give an exact kernel EXEC event but requires tracer topology through bwrap, changes signal-delivery semantics, and collides with the `PR_SET_DUMPABLE=0` discipline — REJECTED as a trust-boundary expansion. No timing heuristic substitutes for the identity proof anywhere.

### 6.E Honest impossibility / trust-boundary result — returned in its precise scoped form

For the existing channels: `ACTUAL_AUDITOR_EXEC_REACH_NOT_PROVABLE_FROM_EXISTING_CHANNELS_FOR_THE_SE_POSITIVE_RC_NO_REPORT_CELL` (mechanically demonstrated, P9 + §5.2). NOT `REQUIRES_TRUST_BOUNDARY_EXPANSION`: the witness designs prove the cell WITHOUT expanding the trust boundary (trusted INNER/launcher reused; EBS unchanged; no new binary for W2, and W1 needs no new binary either). The remaining requirement is a governance CHOICE between accepting the permanent UNDETERMINED residual (L1) and adopting a witness (L2) — not a forced boundary expansion.

## 7. Corrected signal model

Full matrix: `signal-history-equivalence-matrix.md` (26 history rows × tokens × rc family × exec-reach × why × trusted producer × report-adds-proof). Governing honesty rules, each mechanically grounded: integer 137 (any 128+n) may be a normal exit OR a signal encoding — never infer cause from the integer (P1/P9, X10); negative rc is an API-layer convention (direct −9 vs bwrap-positive 137 for the SAME physical signal, P2) — never equate a numeric convention with a process-history fact; and the design never does.

## 8. Wait-status determination

The boundary's `subprocess` interface exposes a collapsed integer, but the RAW wait status of the composition IS observable (`os.waitpid`) — this session recorded it (P2): for a signal-killed sandbox child it decodes **EXITED(137)**, byte-identical to a normal exit 137; the CHILD's true wait status is not exposed by bwrap at all (its synthesis is the lossy step; preserving it would require changing the bwrap invocation/binary — outside boundary+driver scope). Decisively: **even with the exact child wait status, "died of SIGKILL" does not ORDER the death before/after execve** — the `[E, execve)` ambiguity is untouched by termination-cause information. Wait status CANNOT solve the exec-transition question; only identity-channel evidence (report presence, exe witness) can. (Explicitly stated as demanded: knowing signal termination does not prove whether the signal occurred before or after exec.)

## 9. Report-lifecycle evidence — transitive proof analysis (from the frozen output contract)

`REPORT_FROZEN` / `REPORT_SCREEN_FAIL` / `REPORT_INVALID` (EBS snapshot terminals that operated on an EXISTED staging snapshot) and boundary `report_present=true` each imply **`client_exec_reached` PROVEN_TRUE transitively** (R-A: staging is the ONE host-backed rw bind `/auditor-output`; R-B: no trusted component writes the report — INNER writes only the credential + frozen config under the role home, the launcher only the stdout metadata line, bwrap/EBS nothing; R-C: the EBS snapshot semantics of `reportcustody.snapshot_staging` and the launch settlement chain). `REPORT_MISSING` implies NOTHING about exec-reach (pre-exec failure OR exec'd client that wrote nothing) — generalizing MISSING to exec-not-reached is FORBIDDEN and the classifier does not do it. Timeout/exec-failed classes have their own terminals (metadata discarded / fail-byte) and carry no exec information.

## 10. Corrected finite-state classifier (normative reference model)

`reference_classifier.py` — states, with token pattern / rc constraints / report constraints / `client_exec_reached` (true/false/null) / proof strength / impossible combinations / persisted representation:

| State | Tokens | rc | report | reached | strength |
|---|---|---|---|---|---|
| EBS_BOUNDARY_EXEC_FAILURE | — (exec_failed) | 98 | n/a | false | PROVEN_FALSE |
| EXEC_STATUS_UNDETERMINED_TIMEOUT | — (timed_out) | — | n/a | null | UNDETERMINED |
| PRE_INNER_COMPOSITION_FAILURE | `""` | ≠0 | absent | false | PROVEN_FALSE |
| INNER_STARTED_ABNORMAL_DEATH | `S` | any | absent | false | PROVEN_FALSE |
| INNER_SETUP_FAILED | `SI` | any | absent | false | PROVEN_FALSE |
| AUDITOR_EXEC_CALL_FAILED | `SEX` | ≠0 | absent | false | PROVEN_FALSE |
| AUDITOR_DISPATCH_FORK_FAILED (L2) | `SEF` | ≠0 | absent | false | PROVEN_FALSE |
| CLIENT_EXECUTED_EXIT_0 | `SE` | ==0 | any | **true** | PROVEN_TRUE (P1 lemma) |
| CLIENT_EXECUTED_REPORT_PRESENT | `SE` | any | present | **true** | PROVEN_TRUE (P2 lemma) |
| AUDITOR_EXEC_PROVEN_BY_WITNESS (L2) | `SEA` | ANY | any | **true** | PROVEN_TRUE (P3 witness) |
| EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS | `SE` | >0 | absent | **null** | UNDETERMINED |
| OUTER_SIGNAL_DEATH_STAGE_UNDETERMINED | `SE` | <0 | absent | null | UNDETERMINED |
| EXEC_STATUS_GRACE_EXPIRED | unread | any | may prove | null | UNDETERMINED |
| EXEC_STATUS_PROTOCOL_VIOLATION | malformed/oversize/unreachable | any | absent | null | UNDETERMINED |
| EXEC_STATUS_CONTRADICTION | e.g. `""`/`S`/`SI`/`SEX` with rc==0 or report present | — | — | null | UNDETERMINED |

NO branch sets `client_exec_reached=true` without an explicit proof basis: `ZERO_EXIT_STRUCTURAL` (L-A: bwrap passes child exit codes exactly; L-B: bwrap exits 0 only if the child exited 0 — its own failures exit 1; L-C: INNER has no normal-exit path after E without successful execve — source-structural; L-D: no signal path yields 0), `REPORT_PRESENT_TRANSITIVE` (R-A..R-C), or `EXE_IDENTITY_WITNESS` (W-A..W-C). L-A/L-B are host-analog probed and remain MANDATORY vendored-bwrap implementation-time fixtures; the lemma stack is embedded in the reference model and cross-checked by the suite. Impossible combinations rejected fail-closed: rc=0 with any KNOWN non-CLIENT_EXECUTED stage; report presence with any PROVEN_FALSE stream; `exec_failed=true` with nonempty tokens; unreachable streams (`SX`,`ES`,`E`,`I`,`X`,`SA`,`SEI`,`SEAX`,`SES`,`SEXY`,…); oversize; `credential_printed=true` escalation (predecessor rule retained in the persisted model).

## 11. DR-RB-002 validation closure — corrected DESIGN-strength suite

`design-validation-suite.py` + `validation-results.json`: **61/61 PASS, 0 FAIL.** The classifier under test is the ACTUAL reference model (imported, not reimplemented), and the composition semantics fed through it are ACTUAL/PROBED: X01 `"SE"+137` → NOT proven (the exact previously-missing case); X02 143; X03 −9; X04 exit-137-after-independent-proof (report + witness channels); X05/X06 two/three distinct live histories with identical observations collapsing to UNDETERMINED; **X07 the host-bwrap child-SIGKILL probe result (rc=137) fed DIRECTLY into the classifier → ambiguous, NOT CLIENT_EXECUTED** — the exact DR-RB-002 missing link, now exercised; X08 vendored-frozen-bwrap fixture SPEC (fd-passthrough, signal/normal exit conventions, exit-0-only-from-child-0, version+SHA recorded, two-level topology, supervisor non-retention) — specified as implementation-time obligations, NOT executed now; X09 no-bwrap negative-rc control; X10 normal-exit-137 control; X11 report-state transitive tests (FROZEN/SCREEN_FAIL/INVALID → PROVEN_TRUE; MISSING → null); X12 malformed/unreachable streams; X13 fixed-fd normalization; X14 fd collision; X15 CLOEXEC ownership; X16 canaries. Plus the retained predecessor regression set (R01–R16: pre-INNER failures, SI/SEX/S classes, rc=0 lemma live-fed, the Auditor-B rc=1 cell honestly ambiguous, grace-vs-oversize, EBS variants, rc=0/report contradiction rules, report dominance) and the witness series (W01 positive live demonstration through bwrap — `SEA` proven; W02 negative control — child never exec'd stays UNDETERMINED; W03–W08 grammar/dominance), schema/persistence (S01–S07: allowlisted persisted records, legacy-generation compatibility, deterministic serialization) and canary battery (C01–C02: no raw stdout/stderr/credential/report-substance/exception-repr in ANY persisted form). All fixtures local deterministic python3//bin/sh under fresh tempdirs; ZERO provider/client/model calls; ZERO network; ZERO real-attempt-namespace access; vendored bwrap NOT executed. **Fixture success is DESIGN-STRENGTH evidence, NOT an implementation PASS.**

## 12. Fixed-fd design (normative; semantics only — no runtime change)

The write end is normalized to the FIXED fd 8 by EXPLICIT `dup2` (never first-free allocation); any occupant of fd 8 is defensively displaced (`dup` aside) and restored — collision handling is deterministic and verified (X14); the natural-allocation alias is closed; ownership is verified (`fstat`/`F_GETFD`); the fd is kept INHERITABLE by the outer (so it passes into the composition) and receives FD_CLOEXEC EXPLICITLY at the trusted INNER stage (X15: EOF arrives exactly at the payload's execve); the read side is drained post-composition within a bounded grace (P8). The predecessor's "fds 3–6 occupied ⇒ 7/8 first free" rationale is RETIRED as non-normative (the EBS child fd contract `{0,1,2,3,4,5,6}` + the surviving `launcher_fd` makes natural allocation unsafe to assume, per the CR fixed-fd note).

## 13. EBS change determination

**`EBS_CHANGE_NOT_REQUIRED` — PRESERVED (third consecutive reconfirmation).** Every mechanism in this design (L1 classification, fixed-fd channel, L2 witness W1 inside INNER, W2 observer in the launcher) lives in the boundary launcher / driver plane; the EBS transports parsed metadata values and the report lifecycle unchanged. No evidence in this remediation demonstrates a need for an EBS contract change. `EBS_CHANGE_REQUIRED_FOR_PROOF` is NOT returned.

## 14. Result dispositions

- **`AUCDEV023-CR-S1-RB001-DR-RB-001` = CLOSED_AT_DESIGN_STRENGTH.** The defect was the invalid `PROVEN_TRUE` derivation from `"SE"`+rc≥0. The corrected design contains NO rc-sign/value-derived exec-reach proof anywhere; the mechanically ambiguous family is honestly UNDETERMINED; the two legitimate proof channels are formalized with explicit assumption stacks and mandatory implementation-time fixtures; and the escape hatch the finding contemplates ("unless an additional trusted mechanism proves completion") is DESIGNED (W1/W2, in-surface, host-analog demonstrated) for the Control Room's adoption decision. Closure is at DESIGN strength: it becomes effective governance state only after the Control Room verifies this publication; it is NOT an implementation PASS, and the residual non-separability of the `"SE"+rc>0+report-absent` cell under L1 is recorded honestly as inherent (not hidden, not "accepted residual" — a stated UNDETERMINED with a designed remedy pending governance choice).
- **`AUCDEV023-CR-S1-RB001-DR-RB-002` = CLOSED_AT_DESIGN_VALIDATION_STRENGTH.** The corrected suite feeds actual/probed composition semantics through the actual classifier, including every mandated item (`"SE"`+137; 128+n; negative rc; ambiguity preservation; host probe into classifier; vendored-bwrap implementation-time fixture specification — exactly as the finding's own correction clause contemplates). Closure is at DESIGN-VALIDATION strength — the vendored-binary fixtures and the full regression set remain mandatory at implementation time; test success here is NOT an implementation PASS.

## 15. Identity blast radius (WOULD change if later implemented; nothing regenerated now)

| Identity | L1-only (downgrade + schema + fixed-fd) | + L2 W1 (fork-witness) | + L2 W2 (outer observer) |
|---|---|---|---|
| Boundary launcher bytes | CHANGE (classification table + fixed-fd + DEVNULL isolation; `launcher_version` bump) | CHANGE (INNER fork/observe/forward logic) | CHANGE (observer thread; INNER unchanged from L1) |
| Driver bytes | CHANGE (`:1798` → strict-allowlist persistence + exec-evidence record) | same | same |
| Wrapper bytes | unchanged | unchanged | unchanged |
| Role MANIFESTs / package hashes / bindings / binding digests | ALL REGENERATE (exactly one boundary row per manifest — OBSERVED FACT) | same | same |
| Prompt contract `cc6ec29d…` | NOT forced (re-verify at preparation) | same | same |
| EBS package `d683f64d…`/`d42aa9e3…` | UNCHANGED | UNCHANGED | UNCHANGED |
| Event / attempt identity | unchanged formula; same-event attempts NOT EXPRESSIBLE (EBS `attempt_id_for`) ⇒ any future first-pass = NEW EVENT + fresh A/B + full preparation + CR readback + NEW authority | same | same |
| Frozen audit target `d4d584ff…` | UNCHANGED | UNCHANGED | UNCHANGED |
| New trusted binary / supply chain | NONE | NONE (INNER is existing trusted python3 code) | NONE |
| Composition rc semantics | bwrap-native (unchanged) | witness-forwarded (numeric convention identical: 128+n) | bwrap-native (unchanged) |
| Client PID position | namespace init (unchanged) | child of witness (NOT init) | namespace init (unchanged) |

W1's behavioral deltas (client not PID 1; witness reaping/forwarding) and W2's bwrap-topology dependency are the substantive implementation-risk differences the governance decision must weigh.

## 16. Residual uncertainty (stated honestly)

1. The `"SE"+rc>0+report-absent` cell is NOT separable under L1 — inherent, recorded, with a designed remedy (L2) pending governance choice. 2. Vendored-bwrap conventions (fd passthrough, exit synthesis, exit-0-only-from-child-0, two-level topology, non-retention) are host-analog established ONLY; mandatory implementation-time fixtures specified. 3. The rc==0 and report-present lemmas rest on L-A/L-B/R-A..R-C assumption stacks (source-structural parts verified; binary-behavior parts fixture-pending). 4. Pre-INNER 4-vs-5 indistinguishability (bwrap-construction vs interpreter-startup failure) remains — immaterial to D-vs-E. 5. WHY a reached client exited nonzero remains out of RB-001 scope. 6. The witness is one-sided: fast-exiting clients can die before a positive observation (UNDETERMINED, never FALSE). 7. B2 (EOF-while-alive) carries a microscopic do_exit race and is rejected for proof use.

## 17. Attestations + resulting state

ZERO runtime implementation; ZERO auditor/provider/frontier execution; ZERO network or provider probe; ZERO credential read; ZERO report-substance read (Auditor-A frozen report identity referenced mechanically only — NEVER opened); ZERO mutation of EXEC-05 attempt/accounting state, the deployed successor event, historical backups, EXEC-05 driver/wrapper, the EBS, the frozen boundary launcher bytes, or successor packages/bindings/manifests; ZERO new event/attempt identities; ZERO package/binding regeneration; ZERO qualification; ZERO installation; ZERO replacement-execution authority. Writes: the three canonical governance paths, the untracked evidence directory `aucdev023-rb001-drrb-design-remediation-evidence/`, and the generated-LAST reviewer handoff (after the push). Historical records NOT rewritten; protected trees byte-unchanged. **RB-001 remains OPEN at DR-RB-001/DR-RB-002 DESIGN-REMEDIATION strength. Implementation = NONE; replacement execution authority = NONE; qualification = NONE; installation = NONE.** EXEC-05 authority remains CLOSED / NO_RERUN / NON-TRANSFERABLE (budget 2/2, barrier CLOSED_PENDING_CONTROL_ROOM_MECHANICAL_READBACK); attempts `evt-79182989824ce966-A-01`/`-B-01` remain TERMINAL; AUCDEV-023 remains P1 / READY / NOT DONE (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11).

## 18. Next action (EXACTLY ONE)

**CONTROL ROOM VERIFICATION OF THE DR-RB-001 / DR-RB-002 DESIGN-REMEDIATION PUBLICATION AND GOVERNANCE DECISION ON THE EXEC-REACH PROOF STRATEGY — ACCEPT THE PERMANENT `EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS` RESIDUAL CELL UNDER THE L1 DOWNGRADE PROTOCOL, OR ADOPT THE DESIGNED IN-SANDBOX RESIDENT-PARENT EXE-IDENTITY WITNESS (W1) / OUTER-OBSERVER ALTERNATIVE (W2), BOTH WITHIN THE EXISTING TRUST SURFACE AND NEITHER REQUIRING AN EBS CHANGE — BEFORE ANY IMPLEMENTATION AUTHORITY.**

This task does NOT request implementation authority, does NOT prepare a replacement event, and does NOT pre-authorize execution.
