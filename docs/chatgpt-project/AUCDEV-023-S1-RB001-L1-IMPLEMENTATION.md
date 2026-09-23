# AUCDEV-023 S1 — RB-001 L1 BOUNDED IMPLEMENTATION (SOURCE-CANDIDATE IMPLEMENTATION + EXACT VENDORED-BWRAP FIXTURES; NO PACKAGE / EVENT / REPLACEMENT EXECUTION)

**Canonical record — published 2026-09-23 (Europe/Istanbul).**

**Classification of the resulting candidate: `L1_IMPLEMENTED_AT_SOURCE_CANDIDATE_STRENGTH`.**
This is IMPLEMENTATION EVIDENCE ONLY. It is NOT `AUDITED`, NOT `PASS BY
INDEPENDENT AUDITOR`, NOT `QUALIFIED`, NOT `INSTALLED`, NOT
`EXECUTION_READY`. The candidate does NOT self-qualify.

---

## 1. Implementation authority

`AUCDEV-023-S1-RB001-L1-IMPLEMENTATION-20260923-01` — the FIRST exercise
of `FUTURE_BOUNDED_L1_IMPLEMENTATION_AUTHORITY` granted by the canonical
operator governance decision record
`docs/chatgpt-project/AUCDEV-023-S1-RB001-L1-RESIDUAL-GOVERNANCE-DECISION.md`
(blob `01f9c41fbdf66466901fced8f4bf43eb60737355`) under the human
operator's explicit **DECISION=A** (L1_RESIDUAL = OPERATOR_ACCEPTED).

Role of this session: **BOUNDED L1 IMPLEMENTER**. It is NOT Auditor-A,
NOT Auditor-B, NOT an independent auditor, NOT a qualification authority,
NOT an installation authority, NOT a replacement-execution controller,
NOT an event-preparation authority, NOT the Control Room decision-maker.

## 2. Live exact bootstrap identity (verified before any write)

- live GitHub `master` (git ls-remote) = local HEAD =
  `efa8173ea2eec4f8f905738cd3b110d902d7bfa8` (authorized baseline EXACT
  MATCH; no `LIVE_BASE_CHANGED`);
- root tree `108907e7e30b174f8b75883447f84e8e5414a4d6`; sole parent
  `fab62b1c7c9c9a7521ddbcfcb1a43c4cb19feead`;
- canonical blobs verified EXACT: CURRENT-STATE `d538f7a8cac53d8ff38a5
  8dfbc4e8a0b22ba56d1`, BACKLOG `618587eabc04c1b00fb8619c1fcfcb5a2328c70c`,
  governance-decision record `01f9c41fbdf66466901fced8f4bf43eb60737355`,
  predecessor CR readback `284af0e798e484ab985719868d9f04a505210a2b`,
  predecessor DR-RB design record `76ce2ccff9dde7518be827974b0c6a10a283eb
  a7`;
- protected trees verified EXACT at HEAD: bootstrap-supervisor
  `732b8def9f22d7c466ce77f3d3049da53bfff3d0`, qualification-harness
  `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill
  `c792933a862d9a5434681a88d183470dd8b15d2f`;
- tracked working-tree drift: ONLY the pre-existing smoke-fixture /
  smoke-fixture-103 gitlink drift (preserved unstaged, as in every
  predecessor publication); 39 pre-existing untracked evidence/launcher
  artifacts preserved untracked and unaltered.

## 3. Operator decision verification

DECISION=A verified in the canonical record: operator response DECISION=A
(2026-09-23T08:41:49Z / 11:41:49+03:00), `L1_RESIDUAL = OPERATOR_ACCEP
TED`, `FUTURE_BOUNDED_L1_IMPLEMENTATION_AUTHORITY` granted, exercisable
ONLY under a fresh Control Room exact-SHA implementation prompt including
mandatory vendored-bwrap fixtures. **Accepted residual identity:** the
cell `tokens == "SE" AND client_returncode > 0 AND report absent`
REMAINS `EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS` /
`client_exec_reached = null` / `UNDETERMINED` — ACCEPTED RESIDUAL /
DIAGNOSTIC COMPLETENESS LIMITATION, never PROVEN_TRUE, never
PROVEN_FALSE, never a product PASS or qualification PASS. W1 and W2
remain DEFERRED and are NOT implemented.

## 4. Exact predecessor evidence verification

- DR-RB design handoff
  `/home/isa/audit-council-dev/AUCDEV-023-S1-RB001-DRRB001-DRRB002-DESIGN
  -REMEDIATION-HANDOFF.tar.gz`: outer SHA-256 `e534998f503e0128b9cb7fae66
  5f82cc746b5b9cb10224753ffecefcc13acec1`, 836709 B, census 30 = 30
  regular / 0 dir / 0 unsafe / 0 duplicate / 0 symlink / 0 hardlink / 0
  special, exactly one SHA256SUMS 29 rows 29/29 PASS, 0 missing, 0
  unlisted. ALL 14 critical payload identities verified EXACT
  (reference_classifier.py `d3066e81…` 19869 B; design-validation-suite.py
  `2b5cb596…` 38598 B; implementation-time-fixture-spec.json `c197d2f5…`
  1541 B; probe-results.json `5a77cb7c…` 6437 B;
  signal-history-equivalence-matrix.md `3ab47d06…` 10071 B; boundary
  `2efb6660…` 27719 B; driver `d4d1eca2…` 117120 B; wrapper `17e0abcd…`
  2836 B; MANIFESTs `2f8efbd6…`/`15729d8b…`; bindings `5204d90e…`/
  `489a3c91…`; ebs-launch.py `dfc63f00…`; ebs-reportcustody.py
  `e83b5d53…`).
- governance handoff `AUCDEV-023-S1-RB001-L1-RESIDUAL-GOVERNANCE-DECISION
  -HANDOFF.tar.gz`: outer SHA-256 `115243f2958bcab74918edc0f7357f5853b528
  afc15150d8b2fb41fad2f2b031`, 683039 B, census 18 = 13 regular + 5 dir /
  0 unsafe / 0 duplicate / 0 symlink / 0 hardlink / 0 special, exactly one
  SHA256SUMS 12 rows 12/12 PASS, 0 missing, 0 unlisted; canonical copies
  map EXACTLY to live Git blobs (`01f9c41f…`, `d538f7a8…`, `618587ea…`,
  predecessor readback `284af0e7…`).

## 5. Exact vendored-bwrap identity

`01fb705f067bd5365b63d8ad2323a61c8d007733ca5e649437e086f3fb9935d8`,
529776 B, ELF 64-bit static-pie stripped, version string
"bubblewrap built for Codex". Verified as REGULAR files (no symlink
substitution; `readlink -f` = self) at BOTH frozen role packages:
A-side `payload/runtime/boundary-bwrap/bwrap` (MANIFEST-A row, line 920)
and B-side `payload/runtime/codex-0.154.0-linux-x64/codex-resources/
bwrap` (MANIFEST-B row, line 940); both deployed MANIFESTs re-hashed to
the frozen identities. Fixtures executed a SHA-256-verified workspace
COPY (deployed bytes only ever READ, never executed in place).

## 6. Vendored-bwrap fixture gate — COMPLETE RESULTS (all PASS)

Runner: `fixtures/vendored_bwrap_fixture_gate.py`; results:
`fixtures/vendored-bwrap-fixture-results.json`. Synthetic local fixtures
only (fresh tempdirs; ZERO credentials; ZERO provider/model/client; ZERO
network use; ZERO real-event-namespace access; hard timeouts + explicit
child cleanup).

- `child_normal_exit_passthrough`: payload exit 0 → composition rc **0**
  EXACT; exit 7 → **7** EXACT; normal exit 137 → **137** EXACT.
- `child_signal_exit_convention`: SIGKILL → **137**; SIGTERM → **143**
  (positive 128+n CONFIRMED on the vendored engine, mechanically
  observed — not assumed from the host analog).
- `exit0_only_from_child_0` (falsification): setup-bind failure → rc 1;
  invalid invocation (no args) → rc 1; payload exec failure → rc 1;
  payload exit 7 → 7; exit 137 → 137; SIGKILL → 137; SIGTERM → 143. NO
  tested failure/death path maps to 0; the ONLY tested rc-0 path is
  payload exit 0.
- `fd_passthrough_of_fixed_fd`: normalized fd 8 reached the synthetic
  payload; marker `Z8` arrived intact with EOF (fstat FIFO verified
  in-payload).
- `supervisor_fd_non_retention`: CLOEXEC-close-at-exec EOF observed at
  **0.0187 s** WHILE the composition was still alive; negative control
  (live holder, no CLOEXEC) produced NO EOF in the window; L1 protocol
  composite produced tokens `"SE"` with composition rc **0** through the
  vendored engine.
- `topology_two_level_discovery` (INFORMATIONAL only; MUST NOT cause
  W1/W2 implementation): one spawn walked two levels to the payload —
  outer pid exe = the vendored bwrap; the payload (`/bin/sh` =
  /usr/bin/bash on this host) appeared as the DIRECT child of the outer
  pid with `sleep` as its child. The host-analog P5 "resident inner
  bwrap" mid-level was NOT observed as a separate long-lived process
  with this build in this window; recorded exactly as observed. A doubly
  NESTED vendored bwrap cannot mount its root tmpfs in this environment
  (recorded; L1 requires no nested composition).
- `version_and_sha256_recorded`: path (workspace copy + both deployed
  provenance paths), SHA-256, byte size, format and version recorded
  with the results.

**GOVERNANCE-GATING CONDITIONS: (1) child exit status passthrough
ESTABLISHED (0/7/137 exact); (2) composition rc==0 ONLY from payload
exit 0 (no falsification path produced 0); (3) no signal/death/failure
path maps to 0; (4) fd-8/CLOEXEC transport required by L1 ESTABLISHED
(passthrough + EOF-while-alive + live-holder negative control + SE/rc-0
composite). ALL FOUR PASS — the rc==0 structural lemma
(ZERO_EXIT_STRUCTURAL) is supported at IMPLEMENTATION-EVIDENCE strength
for THIS exact vendored identity.**

Transparency (`fixtures/fixture-runner-defect-note.md`): the FIRST gate
run failed uniformly (every composition rc=1, `execvp ENOENT`) due to a
FIXTURE-COMPOSITION DEFECT (the runner's minimal bind set omitted the
usr/lib64 symlink, so the dynamic loader was absent inside the sandbox;
HOST bwrap reproduced the identical failure with the same defective
shape, and the vendored binary worked with the frozen-boundary shape).
The composition was corrected to mirror the frozen boundary shape; NO
assertion was weakened (the corrected composition is a superset of the
defective one). The first-run observed values are preserved in the defect
note. A second defect (the topology family initially misread as nested
bwrap invocations) was corrected to the actual P5 single-spawn analog.

## 7. Candidate boundary launcher

- baseline `2efb666042e44d272a53f9ad4ac93a19c14f1687a33fb38ed84f9823d9bc4
  4a7` / 27719 B → candidate **`011a87139254b7199ec55566074ea4da2324c7986
  33731d30c50670be403cfa` / 41270 B**;
  diff `diffs/boundary.diff` (`bf1fcac21502de91c858bc24ecd8623a9a505bac5f
  e4c8306a5ce2f58f0285e0`, 19157 B, +295/−28);
- `launcher_version` = **`S1-PREP002-REM2-2`** (the designed successor
  identity; IDENTITY TOKEN unchanged: NETWORKED-BOUNDARY-LAUNCHER-V1);
- **A. fixed exec-status fd 8**: explicit collision-safe normalization
  (`_normalize_exec_status_fd`): deterministic F_DUPFD displacement of any
  pre-existing fd-8 occupant (inheritable state preserved; the cred/
  invocation memfds routinely occupy 8 and are re-referenced by relocated
  fd number), natural-alias closure (fd 8 is the outer's ONLY write
  alias), fstat FIFO ownership verification, inheritable into the
  composition; the trusted INNER sets FD_CLOEXEC at its stage; never
  first-free-fd reliance;
- **B. L1 token grammar**: valid runtime streams EXACTLY `""`, `"S"`,
  `"SI"`, `"SE"`, `"SEX"`. Trusted INNER: verify fd 8 + FD_CLOEXEC AT
  ENTRY, write one-byte `S`, ALL setup under a BaseException-safe `I`
  path (re-raise, nonzero), one-byte `E` IMMEDIATELY before the unique
  final `os.execv` with NO semantically relevant work between, one-byte
  `X` ONLY if that exec call returns failure (re-raise, nonzero);
  successful exec closes fd 8 through CLOEXEC (the EOF the outer
  observes). NO token written before exec is interpreted as proof that
  exec completed;
- **C. transport**: outer closes its own write-side alias BEFORE reading;
  bounded nonblocking post-composition drain, grace 0.5 s, cap 3 bytes;
  oversize = protocol violation (NOT grace expiry); no-EOF-within-grace =
  fail-closed UNDETERMINED (`READ_NO_EOF_GRACE_EXPIRED`); no token byte
  invented; malformed/non-ASCII collapses fail-closed;
- **D. stdout isolation**: `subprocess.run(..., stdout=DEVNULL)` on the
  composition ONLY (the accepted minimum isolation); client stdout
  neither captured nor persisted; stderr behavior unchanged;
- **E/F. finite metadata**: the emitted metadata carries the L1
  exec-evidence fields (exec_stage_class / client_exec_reached /
  proof_strength / proof_basis / exec_status_tokens /
  exec_status_transport / exec_status_protocol_level="L1" /
  witness_observed=null + oversize/malformed flags) alongside the frozen
  identity fields; rc=3 failure metadata carries ONLY the finite
  `error_class` ("LAUNCHER_FAILURE") — raw exception repr/text NEVER
  persists; the exact frozen rc=2 ARGV_CONTRACT_INVALID and
  METADATA_OVERSIZE forms are preserved byte-identically.

## 8. Candidate driver

- baseline `d4d1eca2baa3b8f50aa7f666986cf4d1e6ca4cf2bc09ea2dfe6feca50303
  2357` / 117120 B → candidate **`cd4608a972bb3d1023f6a6bf8283189a8e765
  8bb58ca4bc9b46704f8d7fb617f` / 139721 B**;
  diff `diffs/driver.diff` (`c4e15b351478e3ef7b4dfffe6606845f32b43e39482
  611dc715cd7f7acf9cf3c`, 30170 B, +457/−17);
- the historical `:1798` metadata_keys-only reduction is REPLACED by
  `validate_boundary_metadata_l1` strict finite VALUE persistence:
  identity cross-checks type/length/grammar BEFORE equality (launcher
  token, launcher_version grammar `S1-PREP002-REM2-<digits>` then
  equality with `S1-PREP002-REM2-2`, role/attempt/event/staging_dir/
  output_name, 64-hex invocation_sha256 recomputed via
  `ebs.binding.canonical_bytes(list(binding.auditor_invocation))`,
  credential_printed escalation guard), finite key-inventory allowlist
  (unknown keys are forbidden fields), the exact frozen rc=2
  ARGV-refusal and METADATA_OVERSIZE forms, rc=3 pre-composition prefix
  shapes, completed post-composition full form, legacy
  S1-PREP002-REM2-1 acceptance (LEGACY_NO_EXEC_STAGE), timeout-discarded
  variant, impossible-combination rules, report-state relationship, and
  RE-DERIVATION of the classification from the mechanical scalars with an
  exact-match requirement against the boundary's emitted fields;
- the persisted exec-evidence sub-record is EXACTLY the normative
  allowlisted 8 keys with finite enums; on ANY validation failure it
  FAILS CLOSED (values rejected; finite keys + violation tokens
  persisted; a conformance check row makes the attempt nonconforming);
  `_exec_evidence_record` is record-equal to the reference
  `build_exec_evidence_record` (including the unpersistable-token
  collapse to EXEC_STATUS_PROTOCOL_VIOLATION);
- the raw `repr(exc)` persistence sites (the `:1869` failure path,
  accounting/inspect errors, the unexpected-exception record, and every
  exception-text embedding reaching evidence/chronicle) are remediated
  to the finite `_exc_class` bounded class name — raw exception
  repr/message NEVER persists.

## 9. Wrapper — unchanged

`exec05-wrapper.sh` = `17e0abcd34303d0defda2326587cb80550872e8ebdb55b1055
fb880e6d06534c` / 2836 B, byte-identical to the frozen baseline. No
wrapper change was required.

## 10. EBS — unchanged

`EBS_CHANGE_NOT_REQUIRED` governing: bootstrap-supervisor tree
`732b8def9f22d7c466ce77f3d3049da53bfff3d0` EXACT at HEAD; EBS blobs
`bootstrap-supervisor/ebs/launch.py` = `063b6ce1f4c726bd6ba809f605a11551
1667fb09` and `bootstrap-supervisor/ebs/reportcustody.py` = `18f1cc600c6
84e520b72026e0b4cdf8ba6287cb9` EXACT. The candidate adapts to the
existing EBS transport (one bounded JSON metadata line on stdout).

## 11. Differential validation (normative reference)

Runner `results/differential_validation.py`, results
`results/differential-validation-results.json`: BOTH embedded runtime
classifiers (boundary + driver) compared against the EXACT normative
`reference_classifier.py` (`d3066e81…`): the full mandated explicit case
list (40 checks) + an exhaustive semantic grid (15 360 checks) + the
persisted-record renderer equivalence (1 620 checks) + allowlist identity
= **17 021 checks, 0 failures — DIFFERENTIAL PASS**. The predecessor
design-validation suite was re-run unchanged against the same reference
bytes: **61/61 PASS**. L2/W1/W2 tokens appear only as negative cases
proving L1 rejects them (SEA/SEF/SX/SA → EXEC_STATUS_PROTOCOL_VIOLATION;
witness claims → REJECTED_FAIL_CLOSED).

Explicit handling: SE+1, SE+7, SE+137, SE+143, SE+normal-exit-137 →
`EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS` / null / UNDETERMINED;
SE+rc0 → `CLIENT_EXECUTED_EXIT_0` PROVEN_TRUE via ZERO_EXIT_STRUCTURAL
(implementation-acceptable ONLY because the vendored fixture gate PASSED
in this same task); SE+REPORT_FROZEN / REPORT_SCREEN_FAIL /
REPORT_INVALID (and report_present=true) → `CLIENT_EXECUTED_REPORT_
PRESENT` PROVEN_TRUE via REPORT_PRESENT_TRANSITIVE; REPORT_MISSING alone
proves nothing; `""`/`S`/`SI`/`SEX` → PRE_INNER_COMPOSITION_FAILURE /
INNER_STARTED_ABNORMAL_DEATH / INNER_SETUP_FAILED /
AUDITOR_EXEC_CALL_FAILED all PROVEN_FALSE; grace expiry → UNDETERMINED;
oversize → protocol violation; malformed token → protocol violation; SX
→ rejected; SEA/SEF → rejected under L1.

## 12. Implementation test matrix

Runner `results/implementation_tests.py`, results
`results/implementation-tests-results.json`: **83/83 PASS**. Includes
unit fd-8 tests (explicit normalization; pre-existing fd-8 collision
with displacement + occupant usability; alias closure; FIFO/inheritable
state; drain oversize/malformed/grace-expiry semantics) and INTEGRATION
tests of the REAL INNER string + REAL outer helpers through the EXACT
vendored bwrap with INERT synthetic payloads: exec+exit0 → SE/0
PROVEN_TRUE; exec+7 / exec+137 / signal-death-137 → SE ambiguous; execv
failure → SEX PROVEN_FALSE; INNER setup failure → SI; pre-INNER
composition failure → `""`; interpreter-never-started → `""`; post-S
abnormal death → S; report-present proves exec WITHOUT reading content
(content canary never observed); stdout canary cannot corrupt the
metadata channel (with the no-isolation negative control demonstrating
the historical loss mode); stderr canary not persisted; driver
validation matrix (identity/grammar/discriminated variants/impossible
combinations/forbidden fields/credential escalation/witness rejection/
deterministic serialization); `_exc_class` canary absence; no-retry
structural check (single `supervisor.run_attempt(` call site).

## 13. Source-level invariants (mechanical facts)

Runner `results/source_invariants.py`, results
`results/source-invariants-results.json`: **31/31 PASS**. (1) exactly
one final auditor exec call site in the INNER (AST-proven); (2) S
precedes all setup protected by I; (3) E immediately precedes the unique
final exec with nothing between; (4) X only in that exec's failure
handler; (5) no exit(0)/_exit path after E; (6) fd-8 writes are exactly
{S,I,E,X} — no A/F token exists; (7) composition stdout is DEVNULL and
every outer stdout write is a json.dumps line (or the `line` variable
whose every assignment is json.dumps); (8) no metadata_keys-only
evidence reduction remains (metadata_keys appears only in the fail-closed
rejection path); (9) the driver contains ZERO `repr(exc)`; (10) EBS
protected trees + blobs byte-unchanged; (11) W1/W2 absent from both
candidates (witness strings appear only as rejected tokens/enum entries;
no L2 emission); (12) deployed MANIFESTs, bindings, vendored bwrap and
the deployed boundary launcher all re-hashed to the frozen identities —
NOTHING regenerated.

## 14. Zero-runtime attestations

ZERO provider/model/frontier calls; ZERO auditor execution; ZERO
network use in every fixture/test (the only spawns are the vendored
bwrap with inert local payloads, python3 and /bin/sh fixtures); ZERO
credential reads (synthetic byte strings only); ZERO real-event/attempt
namespace access; ZERO report-substance read (the Auditor-A frozen
report `ba8a29a12867273616143e48a86f101f14f6e0e207136d83b31e7fd2426ec1a0`
/ 23727 B / 0444 referenced mechanically ONLY, never opened); deployed
event tree only ever READ (hash verification); implementation performed
in the isolated workspace
`/home/isa/aucdev023-s1-rb001-l1-implementation-20260923-01/` outside
the deployed event; no candidate source added to any protected tracked
tree.

## 15. Identity blast radius (ANALYSIS ONLY — nothing regenerated)

A future preparation authority adopting this candidate boundary would
need to regenerate: BOTH role MANIFESTs, BOTH package hashes, BOTH
binding files, BOTH binding canonical digests, and the future
execution-controller/preparation chain (driver identity change).
UNCHANGED: wrapper, EBS package, frozen audit target. The prompt
contract is NOT automatically forced to change (re-verify at future
package preparation). Any future first-pass requires a NEW EVENT
generation with fresh A/B attempt identities + full successor
preparation + Control Room readback + NEW explicit operator execution
authority — none of which is granted by this implementation.

## 16. Resulting state

- historical finding `AUCDEV023-CR-S1-EXEC05-RB-001` (RB-001) remains
  OPEN with its historical classification COMPLETENESS LIMITATION /
  FAILURE-DIAGNOSTIC EVIDENCE GAP / OBSERVED FACT / ROOT_CAUSE_
  UNRESOLVED / NO_PRODUCT_DEFECT_CONCLUSION_YET unchanged; the
  operator-accepted residual (SE + positive-nonzero rc + report absent =
  EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS / null / UNDETERMINED) is
  implemented honestly and recorded separately;
- EXEC-05 authority `AUCDEV-023-S1-FIRSTPASS-EXEC-20260922-05` remains
  CLOSED / NO_RERUN / NON-TRANSFERABLE (budget 2/2 charged fail-closed;
  barrier CLOSED_PENDING_CONTROL_ROOM_MECHANICAL_READBACK); attempts
  `evt-79182989824ce966-A-01`/`-B-01` remain TERMINAL;
- packages regenerated = NO; MANIFESTs regenerated = NO; bindings
  regenerated = NO; new event created = NO; replacement execution
  authority = NONE; auditor/provider execution = NONE; qualification =
  NONE; installation = NONE; independent verification still required;
- AUCDEV-023 remains **P1 / READY / NOT DONE** (no backlog count/status
  change: READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11);
  no qualification-history row added; ARCHITECTURE-SUMMARY unchanged.

## 17. Next action (exactly one)

**CONTROL ROOM VERIFICATION OF THE EXACT L1 SOURCE-CANDIDATE
IMPLEMENTATION, VENDORED-BWRAP FIXTURES, DIFFERENTIAL VALIDATION, AND
GENERATED-LAST HANDOFF BEFORE ANY PACKAGE / MANIFEST / BINDING / EVENT
PREPARATION OR REPLACEMENT EXECUTION AUTHORITY.**
