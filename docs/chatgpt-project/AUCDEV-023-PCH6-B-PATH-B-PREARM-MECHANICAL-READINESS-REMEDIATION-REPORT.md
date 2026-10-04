# AUCDEV-023 PCH6-B Path-B prearm mechanical-readiness remediation — IMPLEMENTATION CANDIDATE

Publication identity: implementation/remediation authority
AUCDEV-023-PCH6B-PREARM-MECHANICAL-READINESS-REMEDIATION-20261005-01.
Date: 2026-10-05 (Europe/Istanbul).
Canonical base of THIS record: 5ea2edb5e1a6c819120fc64bb2caad4fe45cfd04
(root tree 8d785b314bd0cbfc6cb1104d6b5cef87625b85ee, sole parent
f24f5c106796914dd3ef625879763f43869ef136, the Path-B Auditor-A attempt
20261004-02 Control Room readback provenance correction whose recorded NEXT
— the operator decision on this remediation — THIS publication implements).
Operator authorization scope (exact): "AUCDEV-023 narrow zero-model
prearm-mechanical-readiness protocol remediation only; no attempt execution,
no real credential use, no channel connect, no model execution, and no
Auditor-B authority."

## 0. Disposition

AUCDEV_023_PCH6B_PREARM_MECHANICAL_READINESS_REMEDIATION =
IMPLEMENTED_AS_CANDIDATE
/ AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK
/ PREARM_001_NOT_CLOSED
/ ZERO_MODEL_ENGAGEMENTS
/ ZERO_VM_RUNS
/ ZERO_CHANNEL_CONNECTIONS
/ ZERO_REAL_CREDENTIAL_ACCESS
/ ADDITIVE_OPERATOR_SIDE_ONLY
/ ACCEPTED_V2_BYTES_UNCHANGED
/ FROZEN_RUNTIME_AND_TARGET_UNCHANGED
/ NO_NEW_ATTEMPT_AUTHORITY
/ AUDITOR_B_AUTHORITY_NONE
/ AUDIT_VERDICT_NONE
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
/ AUCDEV_023_P1_READY_NOT_DONE

THIS PUBLICATION GRANTS NOTHING. Implementation completion does NOT close
PREARM-001 (candidate strength only), is NOT an audit verdict, establishes
NO frozen-target product finding, grants NO attempt authority, NO channel
action, NO Auditor-B authority, NO qualification and NO installation.

## 1. Role and scope of this session

This session is the bounded IMPLEMENTER of the narrow pre-arm
mechanical-readiness remediation for AUCDEV023-CR-PCH6B-PREARM-001. It is
NOT the Control Room, NOT an auditor, NOT an /audit-council executor, NOT an
Auditor-A or Auditor-B attempt executor, NOT an attempt authority, NOT a
provider/model executor, and NOT a qualification or installation authority.
All activity was LOCAL and DATA-ONLY with respect to the live chain: no VM
was started or defined, no channel socket was connected to or probed, no
real credential was requested, located, stat'ed, opened, read, hashed,
transmitted or recorded, no BootstrapAuthority was imported or constructed,
run_attempt was never called, and no provider/model was executed. The ONLY
executions were (a) ordinary Git/GitHub publication mechanics and (b) the
deterministic local-only tests of the new candidate helpers against
synthetic inert fixtures inside the non-secret workspace.

## 2. Live bootstrap (verified before writing)

Live GitHub master == origin/master == local HEAD ==
5ea2edb5e1a6c819120fc64bb2caad4fe45cfd04 EXACT at bootstrap (ls-remote
authoritative; fetch rc 0); root tree 8d785b314bd0cbfc6cb1104d6b5cef87625b85ee
EXACT; sole parent f24f5c106796914dd3ef625879763f43869ef136 EXACT
(single-parent fast-forward geometry); trust anchor
3058868416241d394cfaaa40cc585085db486f37 ancestor rc 0; frozen audit target
730d2b29f7c0e7d33af3451b6d9205ec27c143ed (tree
2585796efd5cb6902226cfff785bb901297a15e3) present, ancestor, UNTOUCHED,
AUDIT SUBJECT / NOT AUTHORITY; protected trees bootstrap-authority
154975872e15d53e1706016f5bb60c83727004f0 / bootstrap-supervisor
3056e577259ab0b0b0472f82ebc306506f3e084c / qualification-harness
5b8d5e5465923740470ff63ed9b8683f257a3787 / skill
efd8c2e48edbb25795b3aacb1ce3c23fde10082a held EXACT at base; the eleven
mandated canonical records read at the exact base with blob identities
recorded (CURRENT 0676b006 / BACKLOG 6125262a / provenance-correction
record ca35ed60 / attempt Control Room readback 3b9a5c8f / attempt
execution report d210e5ad / V2 remediation report 68987706 / V2 remediation
Control Room readback 424b9aff / clean verification report 43591c64 / clean
verification Control Room readback 3a99528b / governance design revision
08667b14 / update protocol 42955b85) with the CURRENT and BACKLOG working
copies verified byte-identical to the base blobs before editing; THIS
record's path ABSENT at base with zero full-history path rows; repository
drift (pre-existing smoke-fixture / smoke-fixture-103 gitlink rows and
pre-existing untracked workspaces/handoffs) preserved UNSTAGED. Live master
is re-resolved EXACT immediately before staging and again immediately before
commit (tasking mandate).

## 3. Original finding being remediated

AUCDEV023-CR-PCH6B-PREARM-001
OPERATOR_PREARM_ACK_NOT_MECHANICALLY_BOUND_TO_ACTUAL_SENDER_READINESS
(recorded OPEN / BLOCKING by the attempt 20261004-02 Control Room readback
at f24f5c1, preserved by the provenance correction at 5ea2edb): the settled
single-use Auditor-A attempt proved that the previous pre-arm mechanism
accepted a textual "ARMED" acknowledgement without mechanically
establishing that a real operator-side sender process was alive and waiting;
the irreversible attempt-global claim was then crossed while no sender
process actually existed (operator post-settlement correction: no separate
sender terminal, no waiting sender process, no credential ever sent, total
credential-channel census 0/0). Classification: HARNESS / EXECUTION-PROTOCOL
DEFECT; NOT a frozen-target product defect. Required correction: replace
the textual-only pre-arm admission with NON-SECRET MECHANICAL READINESS
EVIDENCE GENERATED BY THE ACTUAL WAITING OPERATOR-SIDE SENDER PROCESS, such
that a future orchestration can never treat a mere chat/text acknowledgement
as sufficient readiness evidence.

## 4. Architecture of the additive candidate (minimum change, operator side)

All candidate bytes live in the NEW non-secret workspace
/home/isa/aucdev023-pch6b-prearm-mechanical-readiness-remediation-20261005-01/
and are hash-bound in this record and the generated-LAST handoff. NO
accepted V2 component, canonical runtime file, event package, VM/XML/image,
custody path or frozen-root path was modified (verified §12). The candidate
contains the minimum equivalent of an operator-side pre-arm
waiter/supervisor, an independent pre-arm readiness verifier, an operator
launch template, deterministic local-only tests and non-secret evidence.

- bin/prearm_sender_v1.py — the pre-arm waiter/supervisor. Lifecycle:
  (1) strict non-secret config validation (exact key allowlist; absolute
  paths; no credential field can appear in the config schema at all);
  (2) rejects invocation unless the config's waiter_source_path IS the
  running file; (3) sets PR_SET_DUMPABLE=0 BEFORE readiness (refuses if
  prctl fails); (4) verifies the fresh NON-SECRET challenge (strict schema,
  hex64 nonce, context binding); (5) verifies its own source bytes by
  SHA-256; (6) verifies the accepted sender file bytes against the expected
  identity (d7 EXACT in production); (7) verifies the future send-now
  marker is ABSENT; (8) only then atomically creates the NON-SECRET
  readiness proof with O_CREAT|O_EXCL mode 0600 (duplicate proof is refused
  by O_EXCL); (9) remains alive polling ONLY for marker existence — ZERO
  socket logic (AST-verified import allowlist), ZERO reads of file
  descriptor 0 (the future credential source is held unread), ZERO
  credential knowledge; (10) when the marker appears, re-validates every
  invariant (challenge nonce/context, boot id, own source hash, sender
  bytes) and then performs EXACTLY ONE os.execv transition into the
  verified sender — the SAME PID becomes the sender. No fork, no retry, no
  fallback, no second sender path exists anywhere in the source (tested).
  Fail-closed exit codes: 2 pre-arm refusal; 3 re-validation/exec failure;
  4 bounded wait expiry (no exec). There is NO production dry-run mode.
- bin/verify_prearm_ready_v1.py — the INDEPENDENT fail-closed readiness
  verifier (read-only; ZERO network code; creates nothing). It is the ONLY
  authoritative admission decision for pre-arm readiness and refuses with
  MECHANICAL_PREARM_READY=NOT_VERIFIED plus explicit REASON lines on ANY
  failure condition (§7). On success it prints exactly
  MECHANICAL_PREARM_READY=VERIFIED (exit 0) plus the bound identities and
  the statement THIS_VERIFICATION_CARRIES_NO_ATTEMPT_AUTHORITY.
- bin/gen_prearm_challenge_v1.py — mints ONE fresh NON-SECRET challenge
  (256-bit os.urandom nonce) with O_EXCL 0600; refuses overwrite.
- operator/OPERATOR-PREARM-TEMPLATE.txt — the operator launch template:
  six steps (mint challenge; compute waiter identity; write config; launch
  waiter under sender privileges with fd 0 ALREADY attached to the
  credential source and left unread; run the independent verifier; and —
  only a separately-authorized future attempt — create the send-now marker
  carrying the credential-channel socket path so the SAME PID execs the
  accepted sender). The template documents textual "ARMED" as OPTIONAL
  human UX ONLY, never an admission gate.
- tests/run_tests.py + tests/fixtures/ — deterministic local-only tests
  (§9) using ONLY the synthetic inert sender fixture
  tests/fixtures/sender_fixture_v1.py and the detection control
  tests/fixtures/stdin_consumer_control_v1.py. The REAL accepted sender was
  NEVER executed.

CORE DESIGN REQUIREMENT satisfied: the waiting process that emits the
readiness proof IS the SAME process that later transitions into the
accepted sender by exec — same PID, proven at runtime by test 02 (fixture
reports its PID == waiter PID) and structurally by the single exec site
(test 16 source invariant: exactly one os.execv, zero child-process/retry
constructs).

## 5. Candidate artifact identities (session-derived, sha256)

- bin/gen_prearm_challenge_v1.py
  af8671cf578c8f6c6bfc70adeee3cddddb9cb51013307a53c33a05375c2b4e49 (1960 B)
- bin/prearm_sender_v1.py
  b0ec4e7ee0ce6e047372a694c58f442a73dc8586d9d8742bba588406acd5c097 (10878 B)
- bin/verify_prearm_ready_v1.py
  3f4438e9e76c29d2c4e0b2889c6ec0614afc07e08f5df34a03276e95a5f8c61e (10778 B)
- operator/OPERATOR-PREARM-TEMPLATE.txt
  23f1020635a9f8cdc211affcebf42e89050b8727ff44617d5581aace76ee355d (6242 B)
- tests/run_tests.py
  816ccf1873d496044589d697cd35bdb49484a240dfd8b2a97c3c4779a76144c3 (19486 B)
- tests/fixtures/sender_fixture_v1.py
  2054ec12b74cfd56d9efe2d3971a7ab199e59e9594db41150b954a3ee2207980 (2212 B)
- tests/fixtures/stdin_consumer_control_v1.py
  ad2f870ff2cc20c6b85fe6d0daf314d69f590d041c0332cd6aaae97e72b6fcae (598 B)
- sender/send_once_v2.py (byte-exact preserved copy, mode 0555, NEVER
  executed this session) — identity in §6.

Helper/test source is NOT committed to Git: the tasking authorizes exactly
three tracked documentation paths, and no live canonical contract requires
tracking this source; the bytes live hash-bound in the non-secret workspace
and the generated-LAST handoff (full manifest evidence/identity-manifest.txt).

## 6. Accepted sender identity (bytes govern; re-verified this session)

send_once_v2.py = 3954 B, SHA-256
1cc6e22efb1cec386d6edebcbb3f42e4feac1896c101d7c465b8dac569d6a8dd
(d7 EXACT). Re-derived this session SIX ways, data-only (read + hash only,
never executed): the V2 remediation workspace original
/home/isa/aucdev023-pch6b-credential-channel-remediation-20261004-01/bin/send_once_v2.py
(sha256sum + hashlib), the attempt workspace copy
/home/isa/aucdev023-pch6b-auditora-attempt-20261004-02/send_once_v2.py
(sha256sum + hashlib), and the new byte-exact workspace copy
sender/send_once_v2.py (sha256sum + hashlib + cmp byte-identical to the
original; mode 0555). All six = d7 EXACT, matching the operator tasking,
the provenance-correction record and the origin V2 remediation report.

## 7. Readiness proof schema and freshness semantics

Proof = single JSON document, atomic O_CREAT|O_EXCL create, mode 0600,
NON-SECRET, carries NO authority. STRICT key set (any extra or missing key
is refused — this structurally excludes authority-bearing or
credential-bearing fields; a sample proof's keys contain ZERO
credential-term keys, mechanically scanned):

  schema=AUCDEV023-PREARM-PROOF, version=1,
  state=READY_WAITING_FOR_SEND_NOW, context_id, challenge_nonce (hex64),
  boot_id, waiter_pid, waiter_starttime (/proc stat field 22),
  waiter_source_path, waiter_sha256, sender_path, sender_sha256 (= d7 in
  production), marker_path, prctl_dumpable_rc, created_at_utc
  (INFORMATIONAL ONLY — wall-clock is never authoritative).

Freshness/replay: the verifier fails closed on challenge mismatch; wrong
schema; wrong boot id; PID absent (process exited/killed); PID start-time
mismatch (start-time is unique per boot, so same-boot PID reuse cannot
collide); waiter process cmdline not bound to the expected waiter source;
waiter source hash mismatch; sender path/d7 hash mismatch; send-now marker
already present at pre-arm establishment (waiter refuses readiness) or at
verification; proof predating the fresh challenge (secondary ctime
ordering; primary binding is the nonce); malformed/truncated proof;
duplicate proof (O_EXCL refusal, tested); unexpected extra fields; proof
mode not 0600; PR_SET_DUMPABLE not set; and waiter fd-0 offset non-zero
(when /proc fdinfo is readable — enforced whenever the verifier runs with
sufficient privilege; unprivileged cross-user readers are denied BY DESIGN
because the waiter is non-dumpable). Replaying BOTH an old challenge and
its old proof reduces to requiring the ORIGINAL waiter process still alive
with matching pid/start-time/source bytes on the CURRENT boot — i.e. the
actual waiting sender — which is not a replay; any substitution is caught
by the liveness and identity bindings. Wall-clock timestamps alone are
never relied upon.

## 8. Before-run_attempt integration requirement (binding on future attempts)

A future attempt orchestration MUST require

  MECHANICAL_PREARM_READY = VERIFIED

(exact verifier stdout token, exit code 0) BEFORE it may even reach the
irreversible run_attempt / attempt-global-claim boundary. THE VERIFIER,
NOT HUMAN TEXT, IS AUTHORITATIVE FOR PRE-ARM READINESS. Textual "ARMED"
may remain at most as human UX acknowledgement and has NO admission
effect (test 17: a file containing ARMED is refused like any malformed
proof). This requirement is documented in the operator template, in the
verifier header, and here; adoption for a specific future attempt is a
Control Room/operator decision at that attempt's tasking (this record
grants no attempt).

## 9. Deterministic local-only test matrix — 18/18 PASS from scratch

Zero network; zero credential material (stdin is a synthetic non-secret
sentinel file or /dev/null); sender is ALWAYS the synthetic inert fixture;
the real send_once_v2.py is NEVER executed. Sandboxes recreated from
scratch under tests/run/ at every run start. Final run 18/18 PASS
(evidence/tests/run-004.txt); independent repeatability re-run 18/18 PASS
(evidence/tests/run-005-repeatability.txt).

 01 happy pre-arm: waiter with synthetic fixture config emits ONE proof;
    verifier PASSes while the exact waiter process is alive; proof mode
    0600; PREARM_READY emitted. PASS.
 02 same-process transition: after the synthetic send-now marker the
    waiter performs ONE exec transition into the fixture and RETAINS THE
    SAME PID (fixture-reported pid == waiter pid); fd-0 offset at exec
    entry == 0; synthetic stdin sha256 and length EXACT across the
    boundary; argv shape exact. PASS.
 03 proof from a killed/exited waiter => verifier FAIL. PASS.
 04 PID/start-time mismatch (tampered proof) => FAIL. PASS.
 05 boot-id mismatch (tampered proof) => FAIL. PASS.
 06 challenge mismatch (different fresh challenge) => FAIL. PASS.
 07 stale/replayed proof from an earlier pre-arm session verified against
    a new session's challenge => FAIL. PASS.
 08 altered waiter bytes after readiness => FAIL. PASS.
 09 altered sender bytes after readiness => FAIL. PASS.
 10 send-now marker already present before readiness => waiter refuses
    (nonzero exit, PREARM_REFUSED, NO proof created). PASS.
 11 malformed/truncated proof (and empty proof) => FAIL. PASS.
 12 duplicate/O_EXCL: second waiter on the same proof path refuses; the
    original proof bytes unchanged. PASS.
 13 waiter performs ZERO stdin reads before send-now: source-level scan
    (no stdin constructs) + runtime exec-time offset witness (0) +
    detection control (a launcher that consumes 16 bytes reports 16 —
    proving the witness detects consumption). PASS.
 14 waiter performs ZERO socket/connect operations: forbidden-pattern
    scan + AST import allowlist (argparse, ctypes, datetime, hashlib,
    json, os, re, sys, time only — no networking facility loadable) +
    runtime artifact-set invariant + live observation that unprivileged
    /proc fd introspection of the waiter is DENIED (PR_SET_DUMPABLE=0
    took effect). PASS.
 15 verifier performs ZERO socket/connect operations and exposes no
    textual-acknowledgement input; admission token present. PASS.
 16 no automatic retry or fallback sender execution: sender removed after
    readiness => marker handling refuses (nonzero exit, NO exec line, NO
    fixture execution); source invariant: exactly ONE exec site, zero
    child-process/fork/retry constructs. PASS.
 17 textual "ARMED" alone cannot make the verifier PASS. PASS.
 18 killing the waiter after proof but before the irreversible boundary
    makes the same verification fail closed (was VERIFIED, becomes
    NOT_VERIFIED). PASS.

## 10. Honest iteration ledger (first outputs preserved; every re-run from scratch)

- I-1 (deliberate RED, tests written first): evidence/tests/run-001-red.txt
  — 0/18 FAIL, every failure the absence of the implementation (correct
  failing state; no production code existed before the tests).
- T-1: harness v1 attempted live stdin/fd evidence by reading
  /proc/<waiter>/fdinfo/0 and /proc/<waiter>/fd (run-002, 15/18) —
  PermissionError on BOTH because the waiter correctly sets
  PR_SET_DUMPABLE=0, which denies unprivileged fd introspection even to
  the parent. This CONFIRMS the hardening and exposes an instrument
  limitation, not a product defect. Corrected harness re-derives the same
  invariants without weakening anything: exec-time fd-0 offset witness, a
  16-byte consumption detection control (test-of-the-test), AST import
  allowlist, runtime artifact-set assertion, and a live observation of the
  denial itself. The verifier's fdinfo check was already
  permission-conditional by design. Re-run from scratch run-003 (17/18).
- T-2: harness argv expectation bug — test 02 expected the fixture's
  argv to retain the interpreter path as argv[0], but Python sets
  sys.argv[0] to the exec'd script path (run-003 test 02 FAIL after the
  PID/offset/payload assertions had already PASSED). Corrected expectation
  only; re-run from scratch run-004 = 18/18; independent repeatability
  run-005 = 18/18.
- T-3: standalone source-invariant scan v1 (evidence/scans/
  source-invariants.txt) reported FAIL by banning the bare token
  run_attempt, which the verifier docstring legitimately uses to DOCUMENT
  the mandated integration point; over-broad instrument, not a product
  defect. Calibrated to invocation-shaped bans (run_attempt( etc.);
  corrected scan v2 re-ran from scratch: SOURCE_INVARIANT_SCAN_OVERALL=PASS
  (evidence/scans/source-invariants-v2.txt).
No failed observation was rewritten as PASS without a corrected re-derivation
on identical state; every first output is preserved verbatim under evidence/.

## 11. Source-invariant evidence (zero-connect / zero-credential-read)

Waiter: zero occurrences of sys.stdin / os.read(0 / os.fdopen(0 /
.readline( / any networking import or construct (import socket, from
socket, socket., connect(, connect_ex(, AF_UNIX, create_connection);
exactly one os.execv call site; zero subprocess/fork/system/popen/Popen;
zero bootstrap_authority / BootstrapAuthority / run_attempt references;
imports AST-verified within the non-networking allowlist. Verifier: same
zero-socket set plus zero exec and zero textual-ack flags; admission token
MECHANICAL_PREARM_READY=VERIFIED present. Fixture, control and challenge
minter: zero socket constructs. Sample readiness proof keys contain ZERO
credential-term keys. Full outputs: evidence/scans/source-invariants.txt
(v1, preserved), evidence/scans/source-invariants-v2.txt (PASS),
evidence/identity-manifest.txt (+ modes), evidence/scans/
sender-d7-verification.txt, evidence/scans/v2-frozen-identities.txt.

## 12. Unchanged V2 / frozen-runtime identities (data-only re-verification)

- send_once_v2.py 3954 B d7 EXACT (three preserved copies, six derivations,
  §6). bridge-v2.py 7958 B
  93bb97b7af8a06bf56738c15cdb06a51bc063c81e748d8ef1df4ec3017af9fd3 EXACT and
  channel-v2.json 1489 B
  10e4db64ba8094e599bd934a829b0925ee65bdbe310d1fdf06da3613e927e102 EXACT
  (preserved V2 remediation workspace guest-staging copies, re-hashed this
  session, unchanged). Historical bridge.py/channel.json are guest-resident
  only; NO host copy exists and NOTHING guest-side was touched (zero VM
  runs, zero channel operations — §14).
- Frozen audit target 730d2b29f7c0e7d33af3451b6d9205ec27c143ed (tree
  2585796efd5cb6902226cfff785bb901297a15e3) present and ancestor at base
  and held EXACT in the staged write-tree; protected trees held EXACT
  (§2); canonical runtime/event package, event-host VM/image/XML, custody
  roots and the frozen external event root untouched (no mutation
  operation of any kind was performed on any of them).
- PREARM-MR-10/PREARM-MR-11 evidence = this section + the zero-execution
  census + the precommit battery protected-tree/frozen-target gates.

## 13. PREARM-MR acceptance (candidate strength, §9-§12 evidence)

PREARM-MR-01 readiness evidence generated by the actual waiting process:
PASS (waiter creates the proof itself after its own invariant checks).
PREARM-MR-02 that same PID structurally execs the accepted sender: PASS
(single exec site; runtime same-PID proof, tests 02/16).
PREARM-MR-03 proof bound to fresh challenge + boot id + PID + start-time:
PASS (schema §7; tests 04/05/06/07/18).
PREARM-MR-04 bound to exact waiter source identity and sender d7 identity:
PASS (tests 08/09; §6).
PREARM-MR-05 stale/dead/replayed/mismatched evidence fails closed: PASS
(tests 03/04/05/06/07/08/09/11/12/18).
PREARM-MR-06 textual ARMED not sufficient: PASS (test 17; verifier has no
acknowledgement input at all).
PREARM-MR-07 no credential byte or metadata needed: PASS (config/proof
schemas structurally exclude credential fields; tests use synthetic stdin
only; §11 proof-key scan).
PREARM-MR-08 zero live credential-channel connection needed: PASS
(zero-socket waiter/verifier; readiness is established entirely offline).
PREARM-MR-09 no retry/fallback/re-mint/second sender path: PASS (test 16;
source invariants).
PREARM-MR-10 accepted V2 sender/bridge/channel bytes unchanged: PASS (§12).
PREARM-MR-11 frozen runtime, frozen target, event host and custody
unchanged: PASS (§12, §14).
PREARM-MR-12 no new Auditor-A attempt, no Auditor-B authority: PASS (no
attempt id minted; tests use a non-authority test context identifier;
governance §17).
PREARM-MR-13 future orchestration can mechanically gate BEFORE run_attempt
on verifier PASS: PASS at candidate strength (exact token + exit code;
documented §8 and in the template; adoption is a future Control Room
decision).
PREARM-MR-14 all local-only deterministic tests PASS from scratch: PASS
(18/18, plus an independent repeatability re-run 18/18).

## 14. Zero-execution authority census

VM_RUNS 0; EVENT_HOST_DEFINES 0; CHANNEL_CONNECTIONS 0; CONNECT_ATTEMPTS 0;
SOCKET_PROBES 0; OPERATOR_SEND_NOW created/consumed 0; send_once_v2
invocations 0 (three preserved copies read + hashed only, d7 EXACT, NEVER
executed); bridge-v2 invocations 0; BRIDGE/channel json mutations 0;
REAL_CREDENTIAL stats/opens/reads/hashes/transmissions 0 (none located,
none requested); BOOTSTRAP_AUTHORITY_IMPORTS 0 / CONSTRUCTIONS 0;
RUN_ATTEMPT_CALLS 0; ATTEMPT_ACCOUNTING_RECORDS_CREATED 0;
REPORT_SINKS_CREATED 0; CLAUDE/CODEX/AUDIT-COUNCIL EXECUTIONS 0;
PROVIDER_MODEL_FRONTIER_REQUESTS 0; MODEL_ENGAGEMENTS_CONSUMED 0;
FIRST_PASS_ARTIFACTS 0; V2/FROZEN-RUNTIME/EVENT-ROOT MUTATIONS 0;
QUALIFICATION NONE; INSTALLATION NONE. Executed this session, within
authority: the new candidate helpers and synthetic fixtures in local test
sandboxes ONLY (deterministic, offline, non-secret), and ordinary
Git/GitHub publication mechanics. The generated-LAST handoff archive of
THIS publication is created after commit/push under the self-commit
identity rule, with its identity reported in the FINAL-RETURN.

## 15. Residual risks and completeness limitations

1. The verifier mechanically binds proof <-> live process <-> bytes <->
   operator/Control-Room-supplied expected identities; the integrity of
   the SUPPLIED expectations (waiter sha, d7, paths, context id) is a
   governance trust question outside this mechanism.
2. fd-0 offset enforcement is permission-conditional (the non-dumpable
   waiter denies unprivileged cross-user /proc fd reads BY DESIGN); when
   the verifier runs with privilege (recommended in the template) it is
   enforced; primary zero-stdin evidence remains source-level + exec-time
   witness + detection control.
3. The proof-predates-challenge ctime ordering is a secondary heuristic;
   primary freshness is nonce binding + process liveness + boot-id.
4. Boot-id binding detects reboots; within one boot, PID reuse is caught
   by the unique start-time binding; same-pid+same-starttime substitution
   is not possible for a live process.
5. Challenge freshness depends on the operator minting a new challenge
   per pre-arm session (O_EXCL prevents overwrite; the template mandates
   a fresh session directory).
6. The mechanism is NOT yet integrated into any attempt orchestration;
   PREARM-MR-13 is candidate strength until a future attempt tasking
   adopts the mandatory gate.
7. The bounded-wait expiry path (rc 4) exits WITHOUT exec by design; no
   dry-run mode exists; a max_wait_s value is an operator convenience
   that can only fail closed.
8. Same-user /proc visibility (stat, cmdline) is world-readable and
   trusted for liveness binding; a compromised host can forge /proc
   evidence (host compromise out of scope, as for the whole chain).
9. Helper/test source is untracked by design (no canonical contract
   requires tracking); independent verification relies on the hash-bound
   workspace and the generated-LAST handoff copies.

## 16. Canonical record changes made by this publication

Exactly three tracked paths: NEW this record; M
docs/chatgpt-project/AUCDEV-CURRENT-STATE.md (rotation confined to the
Last-updated line, the canonical-base line, the active P1/READY state
line and the active NEXT line, plus one NEW dated tail record); M
docs/chatgpt-project/AUCDEV-BACKLOG.md (one NEW dated status bullet
immediately after the provenance-correction status bullet, plus one NEW
dated tail record; zero replace/delete in the base region). NOT edited:
any historical record, handoff, matrix, prompt, evidence workspace,
source, runtime, helper, protocol, VM, event-root or package path.
Protected trees and the frozen audit target held EXACT in the staged
write-tree; repository drift preserved UNSTAGED.

## 17. Governance held

EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 INSTANTIATED; PATH-B
slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT; AUCDEV-023 P1 / READY / NOT
DONE; frozen target 730d2b29f7c0e7d33af3451b6d9205ec27c143ed AUDIT
SUBJECT / NOT AUTHORITY; PREARM-001 = IMPLEMENTED_AS_CANDIDATE /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK / NOT CLOSED (opens only via
the independent Control Room readback of this candidate); reserved
Auditor-A attempt ...-AUDITOR-A-01 remains SPENT / SINGLE-USE / NO-RETRY;
Auditor-A replacement attempt DOES NOT EXIST; Auditor-B authority NONE;
MODEL_ENGAGEMENTS_USED 0 for the settled attempt; FIRST_PASS_A ABSENT;
PCH6-B-SD-002 / PCH6-CR-BSD-001 AWAITING FRESH INDEPENDENT AUDIT / NOT
CLOSED; PCH6-B-SD-001 RETAINED / OPEN; the five CRED/CREDCH closures
remain at exactly their LIMITED strengths;
INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED (installed source
8ae33444f349ce73c1359b963722e2d16acba630); installed Audit Council NOT
AUTHORITY FOR THIS EVENT; NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE DISCLOSED
RESIDUAL; STAGING-RB-001 / CREDCH-RB-EV-001 preserved; frozen external
event root untouched append-only; historical records/handoffs NOT
rewritten; prior closures RETAINED; no audit execution; no audit PASS.

## 18. NEXT — exactly one

INDEPENDENT CONTROL ROOM READBACK OF THE EXACT ZERO-MODEL
PREARM-MECHANICAL-READINESS REMEDIATION CANDIDATE, INCLUDING SOURCE
IDENTITIES, PROOF/FRESHNESS SEMANTICS, SAME-PID EXEC TRANSITION,
ZERO-CONNECT / ZERO-CREDENTIAL-READ EVIDENCE, TEST MATRIX, GENERATED-LAST
HANDOFF AND UNCHANGED V2/FROZEN-RUNTIME IDENTITIES, BEFORE ANY REPLACEMENT
AUDITOR-A OR AUDITOR-B ATTEMPT AUTHORITY IS CONSIDERED.

Recording this NEXT grants NOTHING. No attempt authority follows
automatically. Auditor-B authority remains NONE. No replacement Auditor-A
attempt exists or is authorized.

## 19. Standing prohibitions (unchanged)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from
an agent session absent an explicit single-use operator attempt authority
(and even then at most the ONE authorized call, never a second); never
rerun the launcher; never treat any recorded grant phrase (including any
phrase recorded here) as a new grant; never execute a real auditor or
provider/model; never open, read, hash, log, persist or stat any real
credential byte; never open the four historical sealed artifacts
(identity-only forever); never relabel or rewrite historical model
identities, runs, records, matrices, prompts or evidence workspaces
(append-only); never claim audit PASS, qualification, installation or any
authority from this publication — it grants none; never rewrite or repack
the frozen external event root; never repack the historical generated-LAST
handoff archives; never mutate the canonical runtime root or restage the
event host after event instantiation absent a separate explicit operator
remediation authority; never delete or repurpose the rehearsal-derived
artifacts under /srv/frevp/; never start or reopen the event-host VM or
connect to the candidate credential channel from a record-only session;
and never run privileged mount/pivot_root/umount experiments on the
operator's live host and never automatically re-run an interrupted
privileged command — privileged GATE-W-prime boundary work belongs in the
disposable-KVM environment.
