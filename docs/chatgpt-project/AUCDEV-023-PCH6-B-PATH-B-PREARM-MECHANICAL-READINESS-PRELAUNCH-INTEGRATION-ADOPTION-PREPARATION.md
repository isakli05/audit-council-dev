# AUCDEV-023 PCH6-B Path-B prearm mechanical-readiness — PRELAUNCH INTEGRATION / ADOPTION PREPARATION

Implementation authority:
AUCDEV-023-PCH6B-PRELAUNCH-INTEGRATION-ADOPTION-PREPARATION-20261005-01
(canonical base of THIS record:
`536000c0229e49be40798d45468705f92bb72e20`)

Operator authorization scope (exact): "AUCDEV-023 bounded zero-model
prelaunch integration/adoption preparation only, binding the accepted
prearm mechanical-readiness verifier as a mandatory gate immediately
before the run_attempt / attempt-global-claim boundary; no replacement
attempt minting or execution, no real credential use, no channel
connection, no VM execution, no run_attempt, no model execution, and no
Auditor-B authority."

AUCDEV_023_PCH6B_PREARM_PRELAUNCH_INTEGRATION_ADOPTION_PREPARATION =
PRELAUNCH_INTEGRATION_PREPARED_AS_CANDIDATE /
ACCEPTED_PREARM_VERIFIER_STRUCTURALLY_BOUND_IN_PREPARATION /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK /
NO_OPERATIONAL_ATTEMPT_ADOPTION /
NO_ATTEMPT_AUTHORITY /
PREARM_001_NOT_YET_CLOSED /
ZERO_MODEL_ENGAGEMENTS /
ZERO_VM_RUNS /
ZERO_CHANNEL_CONNECTIONS /
ZERO_REAL_CREDENTIAL_ACCESS /
SYNTHETIC_DOWNSTREAM_ONLY /
ACCEPTED_PREARM_BYTES_UNCHANGED /
FROZEN_RUNTIME_AND_TARGET_UNCHANGED /
NO_REUSABLE_PERMIT_ARTIFACT /
AUDITOR_B_AUTHORITY_NONE /
AUDIT_VERDICT_NONE /
QUALIFICATION_NONE /
INSTALLATION_NONE /
AUCDEV_023_P1_READY_NOT_DONE

THIS PUBLICATION GRANTS NOTHING. Implementation completion is candidate
strength only, is NOT an audit verdict, establishes NO frozen-target
product finding, closes NO finding (PREARM-001 remains NOT_YET_CLOSED),
adopts the gate into NO operational attempt orchestration, and grants NO
attempt authority, NO channel action, NO Auditor-B authority, NO
qualification and NO installation.

## 0. Role and bounds of this session

This session is the bounded IMPLEMENTER of the prelaunch
integration/adoption PREPARATION for the accepted PREARM
mechanical-readiness remediation (Control Room readback publication
`536000c0229e49be40798d45468705f92bb72e20`, readback record blob
`16cc958a5f4d1b67a524d80342151ee641bd9fcf`, disposition
ACCEPTED_MECHANICAL_REMEDIATION_CANDIDATE), implementing the NEXT that
readback recorded. This session is NOT the Control Room, NOT an auditor,
NOT an attempt executor, NOT an /audit-council executor, NOT a
provider/model executor, and NOT qualification or installation authority.
The downstream launch seam in this preparation is a LOCAL SYNTHETIC
INERT FIXTURE ONLY; no real guest runner was launched, transferred,
defined or invoked.

## 1. Exact live bootstrap (verified before writing)

Live GitHub master == origin/master == local HEAD ==
`536000c0229e49be40798d45468705f92bb72e20` EXACT at bootstrap (ls-remote
authoritative; fetch rc 0); root tree
`0fa543585571c8793637306329956f8837d7c3d8` EXACT; sole parent
`2b948e8d19e71706b7ecc9c3e81715aca3a62739` EXACT (single-parent
fast-forward geometry, parent count verified = 1); trust anchor
`3058868416241d394cfaaa40cc585085db486f37` ancestor rc 0; frozen audit
target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` (tree
`2585796efd5cb6902226cfff785bb901297a15e3`) present, ancestor, UNTOUCHED,
AUDIT SUBJECT / NOT AUTHORITY; protected trees bootstrap-authority
`154975872e15d53e1706016f5bb60c83727004f0` / bootstrap-supervisor
`3056e577259ab0b0b0472f82ebc306506f3e084c` / qualification-harness
`5b8d5e5465923740470ff63ed9b8683f257a3787` / skill
`efd8c2e48edbb25795b3aacb1ce3c23fde10082a` held EXACT at base. The eight
mandated canonical records were read at the exact base with blob
identities recorded (CURRENT `a3ae966525fe1b30e7a71d4e09786487a6dd9f1e` /
BACKLOG `2a3e646e4cbe33d4acb77e48604ef75a2840d766` / accepted PREARM CR
readback `16cc958a5f4d1b67a524d80342151ee641bd9fcf` / remediation report
`877f1b6be7073972d7b1719630912358d0faf8b6` / attempt execution report
`d210e5adc13c2bafe9f5de23970be3ac51f2f1f5` / attempt CR readback
`3b9a5c8fd2658c24be7a65b5d14098856d9498b8` / governance design revision
`08667b14bc1a53d3e38037ac2f899c972d07bf18` / update protocol
`42955b85710f09579cd0fd9174d042de231d060d`) plus the three method-
precedent PCH6 prelaunch/launcher records read as METHOD PRECEDENT ONLY
(prelaunch transition design `7a1add8b8e5e10f9c10ec993d654a937fa31c748` /
human-direct invocation admission
`3f49ca110e974e47cbfe31c52a14ce5210d560b5` / grant-prelaunch
`5dbfc67f0fe262c7d2a5635abf3f564c6386c183` — none of them current
authority). CURRENT/BACKLOG working copies were verified byte-identical
to the base blobs before editing. THIS record's path was ABSENT at base
with zero full-history path rows. Repository drift (pre-existing
smoke-fixture / smoke-fixture-103 gitlink rows and pre-existing untracked
workspaces/handoffs) preserved UNSTAGED. Live master re-resolved EXACT
immediately before staging and will be re-resolved immediately before
commit.

## 2. Accepted PREARM dependency verification (bytes govern)

Resolved from the accepted remediation workspace
`/home/isa/aucdev023-pch6b-prearm-mechanical-readiness-remediation-20261005-01/`
(hash-bound by the accepted readback; NEVER recreated from prose; NEVER
modified):

- `bin/prearm_sender_v1.py` (the waiter): SHA-256
  `b0ec4e7ee0ce6e047372a694c58f442a73dc8586d9d8742bba588406acd5c097`,
  10878 B — EXACT.
- `bin/verify_prearm_ready_v1.py` (the verifier): SHA-256
  `3f4438e9e76c29d2c4e0b2889c6ec0614afc07e08f5df34a03276e95a5f8c61e`,
  10778 B — EXACT.
- `bin/gen_prearm_challenge_v1.py` (the minter): SHA-256
  `af8671cf578c8f6c6bfc70adeee3cddddb9cb51013307a53c33a05375c2b4e49`,
  1960 B — EXACT.
- accepted sender `sender/send_once_v2.py` (mode 0555): SHA-256
  `1cc6e22efb1cec386d6edebcbb3f42e4feac1896c101d7c465b8dac569d6a8dd`
  (d7 EXACT, 3954 B) — re-derived TWO independent ways this session
  (sha256sum AND python hashlib), read and hashed only, NEVER executed.
- generated-LAST handoff of the accepted remediation present and
  hash-verified as context: `AUCDEV-023-PCH6B-PATHB-PREARM-REMEDIATION-
  HANDOFF-20261005-01.tar.gz`, 1140354 B, outer SHA-256
  `9a353730977cd6cfb0907406475ac377537822eea0349e66011669addace58d2`
  (not repacked, not rewritten).

ACCEPTED_PREARM_BYTES_UNAVAILABLE_OR_MISMATCHED did NOT occur. The new
preparation workspace holds byte-exact copies of the waiter/verifier/
minter in `deps/` (re-hashed EXACT after copy; the verifier copy is the
external exact-byte dependency the adapter pins).

## 3. The protected host-to-guest seam (recorded at preserved historical strength)

From the settled single-use attempt 20261004-02 execution evidence
(blob `d210e5ad`, preserved historical strength, NOT modified): host
RUNNER_LAUNCHED (the single QGA `/bin/sh -c` launch of the guest attempt
runner, 15:32:06Z) -> guest DRIVER_STARTED (driver starts as aucdev,
pid 481) -> guest CALLING_RUN_ATTEMPT (15:32:07Z) -> attempt-global
O_EXCL accounting claim created (seq 1 PREPARED; the reserved attempt
became RUNTIME-CLAIMED / SINGLE-USE / NO-RETRY from that moment — the
irreversible boundary). The integration contract identifies THE HOST-SIDE
LAUNCH ACTION THAT CAN CAUSE RUNNER_LAUNCHED as the mandatory protected
seam: for any future replacement attempt, NO host action that can start
the guest runner may occur unless the accepted PREARM verifier has just
returned rc 0 with exactly one MECHANICAL_PREARM_READY=VERIFIED token.
The historical settled attempt is untouched by this preparation.

## 4. Integration adapter architecture (the candidate)

Workspace: `/home/isa/aucdev023-pch6b-prelaunch-integration-adoption-prep-20261005-01/`
(NEW, non-secret, untracked by Git, hash-bound by this report and the
generated-LAST handoff). Core artifact `bin/prelaunch_prearm_gate_v1.py`
(SHA-256 `566687a4d25a10a703acf880caa8b714cddd174344bf0ca62d41d950937856c4`,
12267 B, mode 0644). Composition is exactly the strongest allowed:

    STATIC FUTURE-LAUNCH BINDING CHECKS
            |
    ACCEPTED verify_prearm_ready_v1.py (external exact-byte dependency,
    invoked ONCE, argv-list, no shell, bounded 120 s timeout)
            |
    require rc == 0 AND exactly one MECHANICAL_PREARM_READY=VERIFIED
    (stdout) AND no MECHANICAL_PREARM_READY=NOT_VERIFIED AND no REASON
    line AND no admission token in stderr
            |
    IMMEDIATE SAME-PROCESS os.execv TRANSITION into the bound downstream
    launcher ([downstream_interpreter, downstream_path] + argv_tail)

Control flow (fail-closed at every step; rc 2 contract / rc 3 binding /
rc 4 admission / rc 5 transition):

1. `--contract` is the ONLY input; it must be an absolute path. The
   adapter reads exactly ONE file itself (the contract, bounded 16384 B,
   via its single shared read helper also used for hashing) and has NO
   other input channel: no environment access at all (no PATH lookup),
   no chat/operator text input, no textual ARMED acknowledgement input
   of any kind.
2. STRICT contract validation: exact 19-key flat key set; forbidden-key
   token guard refusing any key name carrying credential/permit/token/
   authority/grant/attempt/secret/password/approval/session semantics;
   exact schema/version; strict context-id rules; every executed path
   absolute AND normalized (normpath equality — relative, `..`,
   doubled-slash and traversal forms refused); hex64 for all six pinned
   hashes; argv_tail a list of 0..8 nonempty strings <=4096 without NUL.
3. IDENTITY BINDING BEFORE ANY VERIFIER EXECUTION: the verifier file is
   refused unless absolute, normalized, a regular non-symlink file whose
   live SHA-256 equals the contract pin (the accepted verifier identity);
   the downstream launcher likewise (absolute, normalized, regular,
   non-symlink, exact SHA-256); both interpreters absolute, normalized,
   existing regular files with content hash-bound to the contract. Any
   discrepancy refuses with the verifier NEVER invoked (proven at runtime
   by canary and by the VERIFIER_INVOKED stage line's absence).
4. THE VERIFIER CALL: exactly ONE `subprocess.run([verifier_interpreter,
   verifier_path, --proof, --challenge, --waiter-source,
   --expected-waiter-sha, --sender-path, --expected-sender-sha,
   --marker-path, --context-id], capture_output, timeout)` — argv-list
   semantics, no shell, every element from the contract. A timeout
   refuses fail-closed.
5. ADMISSION (pure function, the only decision point): rc == 0; exactly
   ONE occurrence of MECHANICAL_PREARM_READY=VERIFIED in stdout; zero
   occurrences of MECHANICAL_PREARM_READY=NOT_VERIFIED in stdout+stderr;
   zero REASON-prefixed lines; zero admission tokens in stderr. Nothing
   else may decide admission: PREARM_READY-style waiter tokens, process
   existence, proof-file existence, rc 0 alone, friendly prose, ARMED
   text and operator chat have ZERO admission effect (the adapter never
   even observes them).
6. TRANSITION: after admission the ONLY remaining actions are in-memory
   argv assembly, two stage-report prints, and the SINGLE `os.execv`
   into `[downstream_interpreter, downstream_path] + argv_tail` — the
   SAME process (runtime-proven: the downstream fixture records the
   adapter child's exact PID). No network operation, no credential
   operation, no VM inspection, no mutable state discovery, no human
   acknowledgement wait, no arbitrary hook, no retry, no sleep, no
   fallback, no alternate downstream path. An OSError from exec refuses
   rc 5 without any second attempt.
7. The adapter writes ZERO files of ANY kind in every outcome and emits
   NO reusable admission artifact (no permit, token, approval, grant or
   attempt-id file; stdout lines are ephemeral diagnostics carrying no
   authority).

Source-level invariants (AST + code-only token scans over the
docstring-blanked parse; all mechanically enforced by the test harness):
imports EXACTLY argparse/hashlib/json/os/re/subprocess/sys; exactly ONE
os.execv site and exactly ONE subprocess.run site; zero
fork/Popen/call/check_*/system/popen/spawn; zero shell= keywords; zero
eval/exec-string/compile/__import__ calls; zero os.environ access; zero
socket/connect/urllib/http/AF_UNIX/SOCK_ tokens in code; zero
virsh/qemu/qga tokens; zero run_attempt / BootstrapAuthority /
bootstrap-import shapes; the string "credential" occurs ONLY inside the
forbidden-key guard tuple; exactly one open() site (the shared bounded
reader). Static ORDERING proof: within the transition function the
verifier invocation strictly precedes the exec site, the only statements
between them are stage prints, the admission assignment and ONE
fail-closed admission guard (`if not admitted: refuse(...)`), the exec
site is wrapped by exactly one Try whose handler only refuses, and the
function contains NO loop of any kind — the downstream transition is
therefore unreachable unless the accepted verifier call completed and the
exact admission checks passed.

## 5. Strict integration contract schema

`integration/PRELAUNCH-INTEGRATION-CONTRACT-v1.json` (7586 B, SHA-256
`63a7bbeba2b4d4948bdc0e31451508bbed06f489385876a08bbb5473f59f7f35`) is
the normative schema document: the 19-key strict set, the forbidden-key
tokens, all validation/admission/transition semantics, the accepted
dependency identities, the future production binding requirements, and a
TEST-ONLY SYNTHETIC EXAMPLE binding the synthetic fixtures with a
NON-AUTHORITY test context id. NO production attempt-specific contract
exists or is authorized by this preparation. A future real downstream
binding MUST pin: the exact downstream launcher absolute path + SHA-256,
the exact argv tail, the exact event/context binding, the accepted
verifier identity, the accepted waiter identity and the sender d7
identity — and requires separate operator authority plus independent
Control Room readback BEFORE the attempt-specific prelaunch package is
authored.

## 6. Downstream binding semantics (deferred real binding)

This preparation binds ONLY the SYNTHETIC INERT downstream fixture
`tests/fixtures/downstream_fixture_v1.py` (2207 B, SHA-256
`eddc6b46e5ce0ee8511fa5e943755478f28d8190b27df4246671302cd2e604cb`) —
zero network, zero credential knowledge, zero VM capability, zero
authority; it exists so the same-process transition is observable (it
writes ONE non-secret reached-evidence file recording its PID and exact
argv; that file is TEST evidence, not an admission artifact). NO real
replacement-attempt launcher is bound because NO replacement attempt
exists and NO execution authority exists. The future real seam is the
host-side launch action that can cause RUNNER_LAUNCHED (§3) and is
deferred to separate operator authority and Control Room review
(INT-PRE-13).

## 7. Preparation acceptance criteria — INT-PRE-01..15 results

- INT-PRE-01 PASS — accepted verifier identity
  (`3f4438e9…`) pinned in the contract schema document, pinned in every
  test contract, and ENFORCED by the adapter's live SHA-256 binding
  before invocation (tests 01, 04, 27).
- INT-PRE-02 PASS — the verifier is MANDATORY and cannot be bypassed:
  single verifier call site, static ordering proof, runtime refusals
  with the downstream never reached (tests 03, 07-11, 22, 24).
- INT-PRE-03 PASS — exact VERIFIED token + rc 0 required; token count
  must be exactly one; failure token / REASON lines / stderr tokens
  refuse (tests 05, 06).
- INT-PRE-04 PASS — textual ARMED has zero admission authority (no such
  input exists; dead-waiter+ARMED refused, live-waiter+ARMED unaffected)
  (test 15).
- INT-PRE-05 PASS — downstream path/hash/argv (and both interpreters)
  mechanically bound BEFORE verifier execution (tests 12, 13, 14, 27;
  VERIFIER_INVOKED-absent proof).
- INT-PRE-06 PASS — after verifier PASS no human/manual/stateful
  intermediate step exists (only in-memory argv assembly + one exec;
  AST-proven; runtime same-PID proof) (tests 02, 24).
- INT-PRE-07 PASS — no reusable permit token/file exists (zero files
  written in every outcome; cwd stays empty; permit-like names absent)
  (tests 21, 28).
- INT-PRE-08 PASS — exactly one downstream transition path (single
  os.execv site; no alternate path variable) (tests 22, 23).
- INT-PRE-09 PASS — failure anywhere before the transition fails closed
  (rc 2/3/4 classes all runtime-exercised) (tests 01, 03-14, 26, 27).
- INT-PRE-10 PASS — no real VM/QGA/channel/credential/run_attempt/
  provider activity occurs (census §11; scans tests 16-20).
- INT-PRE-11 PASS — no attempt id and no authority created (test
  contexts are NON-AUTHORITY test ids; zero attempt artifacts; census).
- INT-PRE-12 PASS — R1/R2/R3 preserved explicitly (§10; schema document;
  operator template).
- INT-PRE-13 PASS — future attempt-specific downstream binding clearly
  deferred to separate operator authority and Control Room review (§5,
  §6; template STEP 0).
- INT-PRE-14 PASS — the historical settled attempt remains untouched
  (read-only reads of its canonical record; nothing rewritten; frozen
  external event root untouched).
- INT-PRE-15 PASS — all deterministic local-only tests pass from scratch
  AND repeatably (§8).

## 8. Deterministic local-only test matrix (28 cases)

Harness `tests/run_tests.py` (47329 B, SHA-256
`88481f7268ddaaa216349cfd2b1e17855ddffc3a63b19c112f340fd7d4a748f4`);
fixtures: synthetic inert downstream `eddc6b46…`, synthetic inert sender
`9b228bda…` (799 B), five TEST-ONLY fake verifiers for output-forgery
classes (`6f67a906…` success-forger 1143 B, `891acb6f…` no-token 764 B,
`cb12eee4…` mixed 925 B, `ddf1865e…` doubled 790 B, `db6407f9…`
failure-shape 843 B). Live proofs are produced by the byte-exact
ACCEPTED waiter copy (`b0ec4e7e…`, re-hashed EXACT in-sandbox at every
staging) configured with the SYNTHETIC INERT sender fixture — the real
sender d7 is NEVER executed. Matrix (tasking 01-25 + 3 extras):

01 exact accepted verifier identity enforced (tampered bytes / wrong
pin, refused at binding pre-invocation); 02 happy integration — accepted
verifier VERIFIED -> SAME-PID transition into the synthetic downstream
with exact argv fidelity and reached-evidence, no unexpected files; 03
verifier NOT_VERIFIED + rc!=0 -> downstream never executes; 04 forged
success text from a hash-mismatched fake verifier refused BEFORE
execution (canary absent); 05 rc 0 without the exact token refused; 06
token+NOT_VERIFIED/REASON refused and doubled token refused; 07 dead
waiter -> accepted verifier refuses -> downstream absent; 08
stale/replayed proof vs reminted challenge (waiter alive) -> refused; 09
marker already present (waiter SIGSTOPped to isolate the cause) ->
refused; 10 altered waiter source after proof -> refused; 11 altered
sender bytes after proof -> refused; 12 downstream hash mismatch (wrong
pin AND post-contract tamper) refused pre-verifier; 13 downstream path
substitution (relative/traversal/missing/symlink) refused; 14 argv
mismatch (non-list/empty/NUL/oversized/int/null) refused; 15 textual
ARMED file+env: dead waiter refused, live waiter unaffected; 16 no
shell=/system/eval/exec-string/environ in adapter code; 17 no
network/socket logic (exact import allowlist + token scan); 18 no
credential fields (forbidden-key contract refused; credential term only
inside the guard tuple; single open() site); 19 no run_attempt /
BootstrapAuthority shapes; 20 no VM/QGA/virsh capability anywhere
(fixture token scan + structural harness launcher check: every child is
absolute sys.executable); 21 no reusable PASS/permit file (zero new
files on refusal; only fixture reached-evidence on success; empty cwd
stays empty); 22 exactly one exec site / one verifier subprocess site;
23 zero retry/fallback/alternate paths; 24 static ordering proof (AST
dominance of the admission guard over the transition); 25 repeatability
(full matrix minus the self-repeat re-run from scratch in a fresh
process: 27/27); 26 EXTRA strict contract schema negatives (extra key /
schema / version / malformed JSON / relative proof path / bad hex /
bad context); 27 EXTRA verifier path+interpreter binding negatives
(relative/symlink verifier, relative interpreter); 28 EXTRA no
OPERATOR_SEND_NOW-style marker or permit artifact across a full happy
cycle.

RESULTS (full outputs preserved under `evidence/tests/`): run-001 RED
0/28 with the adapter ABSENT (`5d63f7c3…`); run-002 18/28 (instrument
defects, §9); run-003 26/28 (one instrument self-hit, §9);
run-004-final 28/28 FROM SCRATCH (`010b9fb3…`); run-005-repeatability
28/28 (`55f29afd…`). The internal self-repeat of test 25 itself re-ran
27/27 inside both final runs.

## 9. Honest session iteration (instrument-side only; no erasure)

Every first output is preserved; NO failed observation was rewritten as
PASS without a corrected re-derivation on IDENTICAL state:

- I-1 (pre-adapter, after RED): the harness AST scan expected the
  admission-guard body and the exec-handler body to be bare Call nodes;
  Python wraps statement calls in Expr nodes — corrected the scan to
  unwrap Expr BEFORE any adapter existed (RED output unaffected).
- T-1: harness v1 `build_contract` hashed deliberately-nonexistent paths
  (downstream substitution cases) raising FileNotFoundError in the
  HARNESS, not the adapter — corrected to compute a placeholder hash for
  nonexistent paths; re-ran from scratch.
- T-2: the bytes argv_tail case was not JSON-representable at all (json
  dump TypeError in the harness) — replaced with a JSON null-entry case
  via a raw contract; the dead partial edit was removed before any run
  (compile would have failed); re-ran from scratch.
- T-3: test 21 snapshotted the sandbox BEFORE writing the contract file,
  false-FAILing the adapter for the harness's own file — reordered
  snapshot after contract authoring; re-ran from scratch.
- T-4: the harness token self-scan of run_tests.py hit the scan's own
  banned-token tuples (the known self-hit class) — corrected to a
  STRUCTURAL harness self-review (every child launch must be absolute
  sys.executable; launcher inventory >= 5) with token scans retained for
  adapter+fixtures; re-ran from scratch (26/28 -> 28/28).
- R-T1: the rotation builder's first execution exceeded the interactive
  120 s command budget while difflib computed CHARACTER-level zones over
  the ~380 KB BACKLOG text (no write had occurred; both files verified
  byte-identical to base) — the builder was killed and corrected to
  LINE-level zone computation (the intended semantics all along).
- R-T2: the corrected builder's pre-write zone guard fired on a
  mis-encoded expected tail-insert old-side index for the BACKLOG
  (encoded as len(rows)+1; the correct old-side insertion point is
  len(rows)) — fired BEFORE any write with both files verified
  byte-identical to base; corrected expectation re-ran from scratch.
- R-T3: the builder's pre-write invariant guard fired on a mis-encoded
  "exactly one active NEXT" predicate (CURRENT legitimately carries TEN
  line-start NEXT rows, one per historical dated record; the ACTIVE next
  is specifically row 24) — fired BEFORE any write with both files
  verified untouched; corrected to assert row 24 carries the exact tasked
  NEXT text; the completed builder then ran with zones asserted BEFORE
  and AFTER the write.

The ADAPTER itself needed two pre-test corrections made BEFORE the first
matrix run (both preserved here for honesty): the bounded reader
originally had two open() sites (unified into one shared site) and
admission refusals originally omitted the verifier's captured output
(which tests 07-11 use to assert the failure cause — the refusal line
now carries a whitespace-sanitized 400-char tail of the captured
verifier stdout; admission semantics unchanged).

Publication-instrument iterations (all on instruments; staged content
compliant throughout; every battery re-run FROM SCRATCH on the IDENTICAL
staged bytes):

- B-T1: precommit battery v1 crashed at runtime on a malformed hex-gate
  expression (TypeError) before printing any gate result — corrected to
  the clean boundary-delimited allow-list logic and re-run from scratch.
- B-T2: battery v2's frozen-target gate used tree-path syntax
  (`write-tree:<commit-sha>^{tree}`) instead of commit syntax — produced
  a path-echo artifact; corrected to resolve the frozen-target commit's
  tree plus an ancestor-of-HEAD check.
- B-T3: the disposition parser could not parse the house ` /` token
  separator — corrected to line-wise token extraction.
- B-T4: the PREARM-001 status gate expected the full status quad on the
  CURRENT L23 headline line where this rotation carries the short
  NOT_YET_CLOSED form (the full quad is on L3 and in the tail record) —
  calibrated the gate to the compliant layout.
- B-T5: the credential scan false-positived twice — first on pure-hex
  git identities, then on slash-joined lowercase prose lists (the two
  known hex/base64 heuristic classes) — and the hex allow-set was
  initially missing verified identities the record legitimately quotes
  (the four protected trees, the three method-precedent record blobs,
  the prior-commit root trees and the compound event-id dash-segment);
  each correction verified the literal against Git before allowing it,
  and the battery re-ran from scratch on the IDENTICAL staged bytes
  after every correction.
- B-T6: an initial v2 identity-manifest scope that also covered the
  publication instruments created a self-referential hash loop
  (battery scans the record; record quotes the manifest; manifest lists
  the battery) — resolved by reverting the manifest to CANDIDATE-bytes
  scope (19 entries) with the instruments hash-reported in the
  FINAL-RETURN and the generated-LAST handoff instead.

## 10. Residuals — R1/R2/R3 preserved explicitly

R1 CREDENTIAL-SOURCE ATTACHMENT OPERATOR PREMISE: the gate (verifier +
adapter) does NOT mechanically establish that fd 0 references the
intended real credential source; the operator template keeps fd 0
attached before waiter launch as an OPERATOR PRECONDITION. This
preparation does not read, stat, hash or inspect any real credential and
does NOT establish real credential-delivery readiness.

R2 POST-VERIFY LIVENESS RACE: verifier PASS proves liveness at
verification time. This integration REDUCES the verifier-to-launch
interval to the in-memory argv assembly plus one exec call and removes
all human/manual work between them, but atomic pidfd-style coupling does
NOT exist and is NOT claimed. (Reduced, NOT eliminated.)

R3 PRESERVED V2/RUNTIME EVIDENCE STRENGTH: this preparation starts NO
VM and performs NO fresh guest rehash; bridge-v2 `93bb97b7…` /
channel-v2 `10e4db64…` identities stand at their preserved/hash-bound
strength.

## 11. Zero-execution census

VM_RUNS 0; EVENT_HOST_DEFINES 0; QGA/virsh invocations 0 (the seam is
recorded from historical evidence only); CHANNEL_CONNECTIONS 0;
CHANNEL_REPROBES 0; CONNECT_ATTEMPTS 0; SOCKET_PROBES 0; OPERATOR_SEND_NOW
created/consumed 0 (test sandboxes use clearly-named test paths and the
accepted waiter copy in isolated /tmp sandboxes only); send_once_v2
invocations 0 (read + hashed only); bridge-v2 invocations 0; V2/frozen
mutations 0; REAL_CREDENTIAL stats/opens/reads/hashes/transmissions 0;
BOOTSTRAP_AUTHORITY imports/constructions 0; RUN_ATTEMPT_CALLS 0; attempt
accounting records 0; report sinks 0; attempt ids created 0; CLAUDE/
CODEX/AUDIT-COUNCIL executions 0; provider/model/frontier requests 0;
MODEL_ENGAGEMENTS_CONSUMED 0; FIRST_PASS artifacts 0; qualification
NONE; installation NONE. The only executions: the candidate adapter, the
byte-exact accepted helper copies (waiter/verifier/minter — all local,
non-secret, zero-network by their own proven invariants), synthetic
fixtures and the harness inside disposable /tmp sandboxes, and ordinary
Git/GitHub publication mechanics.

## 12. Governance held

EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 INSTANTIATED;
PATH-B slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT. AUCDEV-023 = P1 /
READY / NOT DONE. AUCDEV023-CR-PCH6B-PREARM-001 =
MECHANICALLY_REMEDIATED / CONTROL_ROOM_ACCEPTED_CANDIDATE /
OPERATIONAL_ADOPTION_PENDING / NOT_YET_CLOSED (this preparation does NOT
close it and does NOT adopt the gate into any operational attempt). The
existing Auditor-A attempt ...-AUDITOR-A-01 remains SPENT / SINGLE-USE /
NO-RETRY; NO replacement Auditor-A attempt exists and none is created,
reserved or implied; Auditor-B authority NONE; MODEL_ENGAGEMENTS_USED
remains 0 for the settled Path-B attempt; FIRST_PASS_A ABSENT;
qualification NONE; installation NONE; frozen target
`730d2b29f7c0e7d33af3451b6d9205ec27c143ed` AUDIT SUBJECT / NOT
AUTHORITY; PCH6-B-SD-002 / PCH6-CR-BSD-001 AWAITING FRESH INDEPENDENT
AUDIT / NOT CLOSED; PCH6-B-SD-001 RETAINED / OPEN; the five CRED/CREDCH
closures at exactly their LIMITED strengths;
INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED; installed Audit
Council NOT AUTHORITY FOR THIS EVENT;
NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE DISCLOSED RESIDUAL; STAGING-RB-001
/ CREDCH-RB-EV-001 preserved; frozen external event root untouched
append-only; historical records/handoffs NOT rewritten; prior closures
RETAINED; no audit execution; no audit PASS.

## 13. Artifact manifest (hash-bound; machine-derived manifest at
IDENTITY-MANIFEST.json, `02cb432c42cd7cb8245a5f7206ffbd6c3e5cbecb4d15beb6046ba7588fb10735`,
4724 B, 19 entries covering the CANDIDATE bytes — adapter, schema
document, operator template, accepted deps copies, tests, fixtures and
evidence; the session publication instruments and FINAL-RETURN are
hash-reported in the FINAL-RETURN and the generated-LAST handoff)

bin/prelaunch_prearm_gate_v1.py 12267 B 0644
`566687a4d25a10a703acf880caa8b714cddd174344bf0ca62d41d950937856c4`;
integration/PRELAUNCH-INTEGRATION-CONTRACT-v1.json 7586 B
`63a7bbeba2b4d4948bdc0e31451508bbed06f489385876a08bbb5473f59f7f35`;
operator/FUTURE-PRELAUNCH-INTEGRATION-TEMPLATE.txt 6404 B
`060f1c976ca1866ab6ea04361a09bdb17cf6891f791118c1bbbc5df11e9fd632`;
deps/verify_prearm_ready_v1.py 10778 B (accepted EXACT);
deps/prearm_sender_v1.py 10878 B (accepted EXACT);
deps/gen_prearm_challenge_v1.py 1960 B (accepted EXACT);
tests/run_tests.py 47329 B
`88481f7268ddaaa216349cfd2b1e17855ddffc3a63b19c112f340fd7d4a748f4`;
tests/fixtures/{downstream_fixture_v1.py 2207 B `eddc6b46…`,
sender_fixture_v1.py 799 B `9b228bda…`, fake_verifier_success_v1.py
1143 B `6f67a906…`, fake_verifier_no_token_v1.py 764 B `891acb6f…`,
fake_verifier_mixed_v1.py 925 B `cb12eee4…`,
fake_verifier_double_token_v1.py 790 B `ddf1865e…`,
fake_verifier_fail_v1.py 843 B `db6407f9…`};
evidence/tests/{run-001-red.txt 3804 B `5d63f7c3…`, run-002.txt 4121 B
`c99b1a81…`, run-003.txt 4180 B `d3506ba6…`, run-004-final.txt 3705 B
`010b9fb3…`, run-005-repeatability.txt 3705 B `55f29afd…`}.

## 14. Publication safety (rotation computed-before-write and re-asserted)

Staged EXACTLY the three authorized documentation paths: THIS NEW
canonical record; M CURRENT `a3ae966525fe1b30e7a71d4e09786487a6dd9f1e`
-> new blob with the rotation confined EXACTLY to lines 3/11/23-24 plus
one NEW dated tail record (difflib LINE zones replace@3 + replace@11 +
replace@23-24 + insert@tail x4; split-rows 1675 -> 1679; line-start NEXT
occurrences unchanged 10 -> 10 with the ACTIVE next — row 24 — carrying
the exact tasked NEXT text; exactly one new ## section); M BACKLOG
`2a3e646e4cbe33d4acb77e48604ef75a2840d766` -> new blob with EXACTLY two
pure insert LINE zones (0-based zone insert@3560 x1 = one NEW dated
status bullet immediately after the prearm-remediation Control Room
readback status bullet at 1-based row 3560 and before the section blank;
insert@tail x4 = one NEW dated tail record), zero replace/delete,
split-rows 4872 -> 4877, base region rows 1..3560 (1-based)
byte-identical including the queue summary/queue table/Priority-status
bullets, no queue-row status transition, no NEW DONE, exactly one new ##
section.
Both zone sets were computed-before-write by the assertion-guarded
builder AND re-asserted from the written files. The staged write-tree
holds the protected trees and the frozen target EXACT; therefore ZERO
source modification was staged and ZERO performed; staged == working on
all three paths; git diff --check and staged git diff --cached --check
PASS; the mandated historical records verified unchanged; no helper or
test source, no channel helper, no send_once_v2 bytes, no domain XML, no
VM image, no credential/auth/session material, no .jsonl, no
event-package tracked path and no event-root file committed; repository
drift preserved unstaged; the disposition block is token-for-token exact;
PREARM-001 is recorded as NOT_YET_CLOSED everywhere and is NOT fully
CLOSED anywhere in staged content; credential/secret mechanical scan
clean over the NEW record and all diff-added lines; the FULL precommit
gate battery ran from scratch on the FINAL staged bytes and ALL PASSED
(gate count in the commit message and FINAL-RETURN).

## 15. Self-commit identity rule

This publication records the exact authorized base
`536000c0229e49be40798d45468705f92bb72e20`, the staged write-tree,
branch master and the disposition in the commit message. The commit
cannot contain its own final SHA, so the exact resulting publication SHA
and result root tree are reported in the FINAL-RETURN, the post-push
GitHub readback and the generated-LAST handoff (created after
commit/push).

## 16. NEXT — exactly one, grants nothing

INDEPENDENT CONTROL ROOM READBACK OF THE EXACT PRELAUNCH INTEGRATION /
ADOPTION PREPARATION CANDIDATE, INCLUDING THE ACCEPTED VERIFIER
IDENTITY, MANDATORY-GATE CONTROL FLOW, DOWNSTREAM PATH/HASH/ARGV
BINDING, VERIFIER-TO-LAUNCH ORDERING, ZERO-REUSABLE-PERMIT PROPERTY,
R1/R2/R3 RESIDUALS, LOCAL-ONLY TEST MATRIX, GENERATED-LAST HANDOFF AND
ZERO-EXECUTION CENSUS, BEFORE ANY ATTEMPT-SPECIFIC PRELAUNCH PACKAGE,
REPLACEMENT AUDITOR-A ATTEMPT AUTHORITY OR AUDITOR-B AUTHORITY IS
CONSIDERED.

Recording this NEXT grants NOTHING.

## 17. Standing negative constraints

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain
from an agent session absent an explicit single-use operator attempt
authority (and even then at most the ONE authorized call, never a
second); never rerun the launcher; never treat any recorded grant phrase
(including any phrase recorded here) as a new grant; never execute a
real auditor or provider/model; never open, read, hash, log, persist or
stat any real credential byte; never open the four historical sealed
artifacts (identity-only forever); never relabel or rewrite historical
model identities, runs, records, matrices, prompts or evidence
workspaces (append-only); never claim audit PASS, qualification,
installation or any authority from this publication — it grants none;
never rewrite or repack the frozen external event root; never repack the
historical generated-LAST handoff archives; never mutate the canonical
runtime root or restage the event host after event instantiation absent
a separate explicit operator remediation authority; never delete or
repurpose the rehearsal-derived artifacts under /srv/frevp/; never start
or reopen the event-host VM or connect to the candidate credential
channel from a record-only session; and never run privileged
mount/pivot_root/umount experiments on the operator's live host and
never automatically re-run an interrupted privileged command —
privileged GATE-W-prime boundary work belongs in the disposable-KVM
environment.
