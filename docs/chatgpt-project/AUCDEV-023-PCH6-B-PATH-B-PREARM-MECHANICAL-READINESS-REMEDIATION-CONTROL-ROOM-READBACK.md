# AUCDEV-023 PCH6-B Path-B prearm mechanical-readiness remediation — INDEPENDENT CONTROL ROOM READBACK

Record-only publication authority:
AUCDEV-023-PCH6B-730D2B29-PATHB-PREARM-REMEDIATION-CRRB-PUB-20261005-01
(readback subject: implementation publication
`2b948e8d19e71706b7ecc9c3e81715aca3a62739` over base
`5ea2edb5e1a6c819120fc64bb2caad4fe45cfd04`)

AUCDEV_023_PCH6B_PREARM_MECHANICAL_READINESS_REMEDIATION_CONTROL_ROOM_READBACK =
ACCEPTED_MECHANICAL_REMEDIATION_CANDIDATE /
GENERATED_LAST_INTEGRITY_PASS /
SOURCE_INVARIANTS_PASS /
PROCESS_LIVENESS_BINDING_PASS /
SAME_PID_EXEC_PATH_PASS /
TEXTUAL_ARMED_ADMISSION_REMOVED /
ZERO_CONNECT_ZERO_CREDENTIAL_READ_SUPPORTED /
PREARM_001_MECHANICALLY_REMEDIATED_AT_CANDIDATE_STRENGTH /
OPERATIONAL_ADOPTION_REQUIRED /
AUDITOR_B_AUTHORITY_NONE /
AUDIT_VERDICT_NONE /
QUALIFICATION_NONE /
INSTALLATION_NONE

This disposition is NOT: audit PASS; a frozen-target product verdict;
replacement-attempt authority; Auditor-B authority; qualification;
installation. THIS PUBLICATION GRANTS NOTHING.

## 0. Role and bounds of this session

This session is the bounded RECORD-ONLY publisher of the ALREADY-completed
independent Control Room readback of the AUCDEV-023 PCH6-B prearm
mechanical-readiness remediation candidate (implementation publication
`2b948e8d19e71706b7ecc9c3e81715aca3a62739`, canonical implementation report
blob `877f1b6be7073972d7b1719630912358d0faf8b6`). This session is NOT the
substantive Control Room decision-maker (the readback was already completed),
NOT an implementer, NOT an auditor, NOT an attempt executor, NOT an
/audit-council executor, NOT a provider/model executor, and NOT qualification
or installation authority. Every verification below is DATA-ONLY.

## 1. Exact live bootstrap (verified before writing)

Live GitHub master == origin/master == local HEAD ==
`2b948e8d19e71706b7ecc9c3e81715aca3a62739` EXACT at bootstrap (ls-remote
authoritative; fetch rc 0); root tree
`23e6379148bb2eb28d7b9d15e2568e6a6308970d` EXACT; sole parent
`5ea2edb5e1a6c819120fc64bb2caad4fe45cfd04` EXACT (single-parent fast-forward
geometry); trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor
rc 0; frozen audit target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` (tree
`2585796efd5cb6902226cfff785bb901297a15e3`) present, ancestor, UNTOUCHED,
AUDIT SUBJECT / NOT AUTHORITY; protected trees bootstrap-authority
`154975872e15d53e1706016f5bb60c83727004f0` / bootstrap-supervisor
`3056e577259ab0b0b0472f82ebc306506f3e084c` / qualification-harness
`5b8d5e5465923740470ff63ed9b8683f257a3787` / skill
`efd8c2e48edbb25795b3aacb1ce3c23fde10082a` held EXACT at base. The eight
mandated canonical records were read at the exact base with blob identities
recorded (CURRENT `1577978d930dc2a5c0a6ceeb560c5d6033a77769` / BACKLOG
`ce798a2c76ff624c2413937ef20fc7cca5c124c0` / remediation report
`877f1b6be7073972d7b1719630912358d0faf8b6` / attempt CR readback
`3b9a5c8fd2658c24be7a65b5d14098856d9498b8` / provenance correction
`ca35ed60c3fc385faba6ca9d5d4e8ca204ca3c40` / V2 remediation report
`689877060fdd0afa542cf6a2485ccb93381f975c` / V2 clean verification report
`43591c644691b2463c351f67a9d2514e838eae68` / update protocol
`42955b85710f09579cd0fd9174d042de231d060d`); this record's path was ABSENT at
base with zero full-history path rows. Repository drift (pre-existing
smoke-fixture / smoke-fixture-103 gitlink rows and pre-existing untracked
workspaces/handoffs) preserved UNSTAGED. Live master was re-resolved EXACT
before staging and again immediately before commit.

## 2. Readback subject publication geometry (data-only)

Implementation publication `2b948e8d19e71706b7ecc9c3e81715aca3a62739` over
base `5ea2edb5e1a6c819120fc64bb2caad4fe45cfd04` is exactly ONE fast-forward
commit changing exactly three tracked paths (NEW remediation report
`877f1b6be7073972d7b1719630912358d0faf8b6`; M CURRENT ->
`1577978d930dc2a5c0a6ceeb560c5d6033a77769`; M BACKLOG ->
`ce798a2c76ff624c2413937ef20fc7cca5c124c0`); no protected source/package
tree touched; frozen target tree unchanged.

## 3. Generated-LAST handoff integrity (independent census + rehash)

Archive AUCDEV-023-PCH6B-PATHB-PREARM-REMEDIATION-HANDOFF-20261005-01.tar.gz
verified DATA-ONLY: outer size 1140354 bytes EXACT; outer SHA-256
`9a353730977cd6cfb0907406475ac377537822eea0349e66011669addace58d2` EXACT;
census 53 total members = 38 regular files + 15 directories + 0 symlinks +
0 hardlinks + 0 special files; 0 duplicate paths; 0 unsafe/traversal paths;
one common top-level prefix; exactly one SHA256SUMS; 37 manifest rows; no
self-row; 37/37 independent payload rehash PASS; exact manifest/payload-set
equality in both directions with every regular payload including README.md
listed exactly once; extraction fidelity 38/38 (extracted bytes identical to
tar stream bytes). Archived Git-copy identities independently reproduced by
BOTH recomputed git blob identity AND direct byte equality to the live base
blobs: report `877f1b6be7073972d7b1719630912358d0faf8b6`; CURRENT
`1577978d930dc2a5c0a6ceeb560c5d6033a77769`; BACKLOG
`ce798a2c76ff624c2413937ef20fc7cca5c124c0`. Inspected under /tmp OUTSIDE the
repository with ZERO members executed.

## 4. Independent Control Room source findings (from the generated-LAST bytes)

Each finding was re-derived data-only this session from the SHA-verified
archive bytes (hashing, AST parsing and text scanning only; no execution):

1. prearm_sender_v1.py (the waiter) SHA-256 =
`b0ec4e7ee0ce6e047372a694c58f442a73dc8586d9d8742bba588406acd5c097`
(10878 B) — EXACT.
2. verify_prearm_ready_v1.py (the verifier) SHA-256 =
`3f4438e9e76c29d2c4e0b2889c6ec0614afc07e08f5df34a03276e95a5f8c61e`
(10778 B) — EXACT.
3. accepted sender copy sender/send_once_v2.py SHA-256 =
`1cc6e22efb1cec386d6edebcbb3f42e4feac1896c101d7c465b8dac569d6a8dd`
(d7 EXACT, 3954 B) — re-derived two independent ways this session
(sha256sum and python hashlib on the archived copy), matching the Control
Room tasking, the V2 remediation origin report and the archived attempt-time
sender-identity evidence.
4. Waiter imports ONLY: argparse, ctypes, datetime, hashlib, json, os, re,
sys, time (AST-verified import set equals the allowlist exactly).
5. Waiter source contains: exactly ONE os.execv call site; ZERO os.fork;
ZERO subprocess/Popen/system/popen child-process path; ZERO
socket/networking import (the single textual "socket" occurrence is the
docstring's "no socket object" design prose); ZERO connect/connect_ex path;
ZERO stdin-consumption path before exec (text scan AND AST stdin-read sites
both zero — the only file reads are bounded JSON reads of named config/
challenge/marker paths, file hashing of named waiter/sender paths, and
/proc reads; file descriptor 0 is never read).
6. The waiter creates the readiness proof ITSELF only AFTER (source order
main() lines 238-252): strict config validation including refusal unless
the configured waiter_source_path IS the running file; PR_SET_DUMPABLE=0
call SUCCEEDS (refusal on nonzero rc, before readiness); fresh challenge
validation (strict schema, hex64 nonce, context binding); live boot-id
acquisition; PID + /proc/self/stat start-time acquisition; exact
own-source hash; exact sender hash (verify_sender); marker-absence check —
and only then the proof write.
7. The proof is O_CREAT|O_EXCL, mode 0600 (fsync'd; duplicate refused by
O_EXCL) and binds: fresh challenge nonce, context, boot-id, PID, process
start-time, waiter source/path/hash, sender path/hash and marker path
(strict 15-key schema, structurally excluding any credential field).
8. The verifier INDEPENDENTLY checks: strict proof schema and strict key
set (any extra authority-bearing field refused); strict challenge schema;
nonce/context binding (stale or replayed proof from a different pre-arm
session refused); proof-predates-challenge ctime ordering; live boot-id
matched against the proof; live waiter PID liveness via /proc; process
start-time matched (defeats same-boot PID reuse); waiter cmdline containing
the expected waiter source; waiter source/path/hash identity against BOTH
the proof and the expected identity; sender path/hash against BOTH the
proof and the expected accepted identity; send-now marker absence at
verification time; proof file mode 0600; recorded PR_SET_DUMPABLE result
== 0; and waiter fd-0 offset zero via /proc fdinfo whenever readable
(permission-conditional, recorded SKIPPED_UNREADABLE otherwise). The
verifier is read-only with ZERO network code and ZERO exec sites (imports
argparse/hashlib/json/os/re/sys only).
9. The verifier has NO textual ARMED/ACK admission input (zero textual
ARMED occurrences in the verifier; its only inputs are the proof,
challenge, waiter/sender source and identity, marker and context
parameters). A plain textual ARMED cannot produce
MECHANICAL_PREARM_READY=VERIFIED; the ONLY authoritative pre-arm admission
decision is the verifier's exact output token, fail-closed with explicit
REASON lines otherwise.
10. Same-process exec transition is structurally supported: after marker
appearance the waiter re-validates every invariant (challenge nonce and
context unchanged, boot-id unchanged, own source bytes unchanged, sender
bytes exact, marker schema/argv_tail strict) and then performs the SINGLE
exec transition into the verified accepted sender AS THE SAME PID; there
is no child sender process, no fork, no fallback and no retry path (exec
failure and bounded-wait expiry both fail closed without retry).

Corroborating artifact identities re-derived EXACT from the archive:
challenge minter `af8671cf578c8f6c6bfc70adeee3cddddb9cb51013307a53c33a05375c2b4e49`
(1960 B); operator template
`23f1020635a9f8cdc211affcebf42e89050b8727ff44617d5581aace76ee355d` (6242 B);
synthetic inert fixture
`2054ec12b74cfd56d9efe2d3971a7ab199e59e9594db41150b954a3ee2207980` (2212 B);
stdin detection control
`ad2f870ff2cc20c6b85fe6d0daf314d69f590d041c0332cd6aaae97e72b6fcae` (598 B);
deterministic local-only harness
`816ccf1873d496044589d697cd35bdb49484a240dfd8b2a97c3c4779a76144c3`
(19486 B). The archived identity manifest records the sender copy mode 555
(the tar materializes 0755; the archived manifest and the bytes govern).

## 5. Test-evidence classification

The archived implementation test history is PRESERVED verbatim and was
corroborated this session by reading the SHA-verified archived run files:
RED 0/18 (evidence/tests/run-001-red.txt); intermediate 15/18 (run-002);
intermediate 17/18 (run-003); final 18/18 from scratch (run-004);
independent repeatability 18/18 (run-005-repeatability.txt). Classified:

HASH-BOUND PRESERVED IMPLEMENTATION RUNTIME EVIDENCE /
SOURCE-CORROBORATED /
NOT INDEPENDENTLY RE-EXECUTED BY CONTROL ROOM

The Control Room did NOT re-execute these tests. The generated-LAST was
reviewed DATA-ONLY and NO archive member was executed.

## 6. PREARM-001 status

AUCDEV023-CR-PCH6B-PREARM-001 =
MECHANICALLY_REMEDIATED /
CONTROL_ROOM_ACCEPTED_CANDIDATE /
OPERATIONAL_ADOPTION_PENDING /
NOT_YET_CLOSED

Reason: the demonstrated textual-only admission defect (operator pre-arm
acknowledgement not mechanically bound to actual sender readiness) is
mechanically remediated by a NON-SECRET readiness proof generated by a live
waiter process and independently verified before the future run_attempt
boundary. However, the mechanism is not yet adopted into any
replacement-attempt orchestration/tasking, no replacement attempt exists,
and NO attempt authority is granted by this readback.

## 7. Residuals / completeness (preserved explicitly)

R1 — CREDENTIAL-SOURCE ATTACHMENT OPERATOR PREMISE. The verifier establishes
the live waiter/process/source identities and zero-consumption properties
but does NOT mechanically establish that fd 0 references the intended real
credential source. The operator template requires fd 0 to be attached before
waiter launch. No real credential was used in remediation. Classification:
ACCEPTED RESIDUAL / OPERATOR PRECONDITION / NOT A FAILURE OF THE
DEMONSTRATED PREARM-001 PROCESS-LIVENESS REMEDIATION. Real
credential-delivery readiness is NOT claimed from this candidate.

R2 — POST-VERIFY LIVENESS RACE. The verifier establishes waiter liveness at
verification time. A process could terminate after verifier PASS but before
a later run_attempt boundary. Classification: EXTERNAL LIVENESS / TOCTOU
RESIDUAL. Future orchestration must place the mechanical verification
immediately at the pre-run_attempt admission boundary and must fail closed
if verification is not current. Atomic pidfd-style coupling does NOT exist
and is NOT claimed.

R3 — PRESERVED V2 / RUNTIME EVIDENCE STRENGTH. send_once_v2.py was
independently available in the handoff and hashes d7 EXACT (re-derived this
session from the archived copy). bridge-v2/channel-v2 identities were
implementation-session preserved-copy rehashes plus zero-mutation evidence;
the Control Room did NOT start the event-host VM and did NOT perform a fresh
guest rehash (the preserved guest-staging copies are no longer present on
this host; the identities stand at archived-evidence strength). Recorded at
preserved/hash-bound evidence strength, NOT fresh live-guest strength.

## 8. Governance held

EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 INSTANTIATED; PATH-B
slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT. AUCDEV-023 = P1 / READY /
NOT DONE. Existing Auditor-A attempt AUCDEV-023-CAND730D2B29-FRESH-AUDIT-
20261002-01-AUDITOR-A-01 remains SPENT / SINGLE-USE / NO-RETRY. NO
replacement Auditor-A attempt exists. Auditor-B authority = NONE.
MODEL_ENGAGEMENTS_USED remains 0 for the settled Path-B attempt.
FIRST_PASS_A remains ABSENT. Qualification NONE. Installation NONE. Frozen
target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` remains AUDIT SUBJECT /
NOT AUTHORITY. PCH6-B-SD-002 / PCH6-CR-BSD-001 AWAITING FRESH INDEPENDENT
AUDIT / NOT CLOSED; PCH6-B-SD-001 RETAINED / OPEN; the five CRED/CREDCH
closures remain at exactly their LIMITED strengths;
INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED; installed Audit Council
NOT AUTHORITY FOR THIS EVENT; NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE
DISCLOSED RESIDUAL; STAGING-RB-001 / CREDCH-RB-EV-001 preserved; frozen
external event root untouched append-only; historical records/handoffs NOT
rewritten; prior closures RETAINED; no audit execution; no audit PASS.

## 9. Zero-execution publication census

VM_RUNS 0; EVENT_HOST_DEFINES 0; CHANNEL_CONNECTIONS 0; CHANNEL_REPROBES 0;
CONNECT_ATTEMPTS 0; SOCKET_PROBES 0; OPERATOR_SEND_NOW created/consumed 0;
send_once_v2 invocations 0 (read and hashed only); bridge-v2 invocations 0;
V2/frozen mutations 0; REAL_CREDENTIAL stats/opens/reads/hashes/transmissions
0; BOOTSTRAP_AUTHORITY imports/constructions 0; RUN_ATTEMPT_CALLS 0; attempt
accounting records 0; report sinks 0; CLAUDE/CODEX/AUDIT-COUNCIL executions
0; provider/model/frontier requests 0; MODEL_ENGAGEMENTS_CONSUMED 0;
ARCHIVE_MEMBER_EXECUTIONS 0 (the generated-LAST was reviewed data-only);
test re-executions 0 (archived evidence classified, not re-run). The only
executions this session: ordinary Git/GitHub publication mechanics and
local data-only python text/hash/AST tooling on non-secret bytes.

## 10. Honest session iteration (instrument-side only; no erasure)

Every first output is preserved in the untracked evidence workspace
aucdev023-pch6b-prearm-rem-crrb-pub-20261005-01/evidence; NO failed
observation was rewritten as PASS without a corrected re-derivation on
IDENTICAL bytes:

T-1 archive census v1 compared SHA256SUMS rows (recorded top-relative with
'./' prefixes) against unnormalized tar member names, producing a
mirror-image 37-row false MISSING set per entry (known prior-session
normalization class) — corrected top-relative normalization re-ran FROM
SCRATCH on identical bytes: 37/37 PASS + EXACT_PAYLOAD_SET_EQUALITY
SATISFIED.

T-2 the independent source-review script v1 failed at compile time on a
backslash literal inside an f-string expression BEFORE any execution —
corrected and re-run from scratch over the identical archive bytes.

T-3 the rotation builder's pre-write guard fired on a mis-encoded line-start
NEXT count expectation for the base CURRENT blob (the count of '\nNEXT'
occurrences is 10, not 9 — every NEXT-leading row is preceded by a newline);
fired BEFORE any write with both target files verified byte-identical to the
base blobs; corrected expectation re-ran cleanly.

T-4 the rotation builder v2 failed at start-up by invoking git WITHOUT -C
from the evidence workspace cwd (rc 128, no repository context, no state
impact, no file touched) — corrected invocation re-ran from scratch.

T-5 the rotation builder's pre-write guard fired on a mis-encoded no-DONE
predicate: the base BACKLOG has ZERO '- [x]' rows and THREE PRE-EXISTING
historical 'DONE' continuation lines (rows 2543/2783/3373 — wrapped prose of
historical records, not queue markers), so an absolute '- [x] == 3'
expectation was wrong twice over; corrected to bracket-count equality at 0
plus a no-NEW-DONE equality check on the DONE-prefix rows; fired BEFORE any
write with both files verified untouched.

T-6 two further pre-write zone-guard firings on expectation-encoding errors
in the builder's expected difflib tuples (the CURRENT tail-insert end index
encoded as 1679 instead of 1675; the BACKLOG bullet slice placed the new
bullet after the blank row 3560 instead of immediately after the
prearm-remediation bullet at row 3559, and the expected tail-insert tuple was
double-shifted) — every firing BEFORE any write with both files verified
byte-identical to base; the corrected builder re-ran from scratch with zones
asserted BEFORE and AFTER the write. (Cosmetic instrument wart, recorded for
completeness: one rev-parse invocation with a '^ {blob}' path argument echoed
the argument instead of resolving; blob identities were re-derived correctly
via git ls-files -s.)

T-7 the precommit battery v1 itself carried a path-constant typo (the new
record's constant dropped the 'PATH-B-' name segment), producing a false
staged-set FAIL and an empty ls-files crash before the summary — staged
content verified correct by direct inspection; corrected constant re-ran the
battery from scratch.

T-8 battery v2 reported three false FAILs of instrument classes on compliant
staged bytes: the PREARM-001 not-fully-closed gate scanned ALL staged lines
including UNCHANGED historical wrapped records that legitimately pair
'PREARM-001 remains OPEN / BLOCKING' prose with unrelated closure tokens
(corrected scope: NEW/CHANGED lines only, plus a separate classifier gate
confirming every PREARM-001 historical line still carries an open/pending
classification); the P1/READY/NOT-DONE gate expected the canonical phrase on
CURRENT lines where the house layout does not place it (corrected to CURRENT
L23 headline + the record's canonical phrase); the no-new-attempt needle was
case-sensitive against the record's 'NO replacement …' phrasing (corrected
case-insensitive). The battery v3 classifier was completed with the current
legitimate PREARM-001 status tokens. The corrected battery re-ran FROM
SCRATCH on the IDENTICAL staged bytes: 75/75 PASS.

## 11. Publication safety

Staged EXACTLY the three authorized documentation paths (this NEW canonical
readback record; M CURRENT `1577978d930dc2a5c0a6ceeb560c5d6033a77769` ->
new blob with the rotation confined EXACTLY to lines 3/11/23-24 plus one NEW
dated tail record — difflib zones replace@3 + replace@11 + replace@23-24 +
insert@tail x4, split-rows 1671 -> 1675, line-start NEXT occurrences
unchanged 10 -> 10 with EXACTLY ONE active NEXT carrying the exact tasked
NEXT text, exactly one new ## section; M BACKLOG
`ce798a2c76ff624c2413937ef20fc7cca5c124c0` -> new blob with EXACTLY two
pure insert zones [insert@3560 x1 = one NEW dated status bullet immediately
after the prearm-remediation status bullet, insert@tail x4 = one NEW dated
tail record], zero replace/delete, split-rows 4867 -> 4872, base region
1..3559 byte-identical including the queue summary/queue table/Priority
-status bullets, no queue-row status transition, no NEW DONE, exactly one
new ## section). Both zone sets were computed-before-write by an
assertion-guarded builder AND re-asserted from the staged blobs. The staged
write-tree holds the protected trees and the frozen target EXACT; therefore
ZERO source modification was staged and ZERO performed. staged == working on
all three paths; git diff --check and staged git diff --cached --check PASS;
the six mandated historical records verified unchanged; no channel helper or
source, no send_once_v2 execution, no domain XML, no VM image, no
credential/auth/session material, no .jsonl, no event-package tracked path
and no event-root file committed; repository drift preserved unstaged;
disposition block token-for-token exact (13 tokens plus the key) with the
disposition key and the ACCEPTED_MECHANICAL_REMEDIATION_CANDIDATE token
present in the record and CURRENT L3/L23; credential/secret mechanical scan
clean over the NEW record and all diff-added lines; hex-literal gate PASS
with every >=7-char boundary-delimited non-decimal hex literal in the NEW
record and diff-added lines machine-verified case-insensitively against the
session-derived independently-verified identity allow-set (all verified
git/tree/blob identities, the archive outer SHA-256, the seven re-derived
candidate artifact hashes and the sender d7 identity; decimal-only,
verified short prefixes and inner segments of verified compound identifiers
exempt); the FULL record-only precommit gate battery ran from scratch on
the FINAL staged bytes and ALL PASSED (gate count recorded in the FINAL
-RETURN and the commit message).

## 12. Self-commit identity rule

This publication records the exact authorized base
`2b948e8d19e71706b7ecc9c3e81715aca3a62739`, the staged write-tree, branch
master and the disposition in the commit message. The commit cannot contain
its own final SHA, so the exact resulting publication SHA and result root
tree are reported in the FINAL-RETURN, the post-push GitHub readback and
the generated-LAST handoff (created after commit/push).

## 13. NEXT — exactly one, grants nothing

OPERATOR DECISION ON WHETHER TO AUTHORIZE A BOUNDED ZERO-MODEL PRELAUNCH
INTEGRATION / ADOPTION PREPARATION THAT BINDS THE ACCEPTED PREARM
MECHANICAL-READINESS VERIFIER AS A MANDATORY GATE IMMEDIATELY BEFORE THE
run_attempt / ATTEMPT-GLOBAL-CLAIM BOUNDARY FOR A POSSIBLE FUTURE
REPLACEMENT AUDITOR-A ATTEMPT.

This NEXT does NOT authorize: replacement Auditor-A execution;
creation/minting of an attempt; real credential use; channel connection;
VM execution; run_attempt; provider/model execution; Auditor-B. Any
replacement attempt authority remains a later, separate explicit operator
decision after the integration/adoption preparation is independently
reviewed. Recording this NEXT grants NOTHING.

## 14. Standing negative constraints

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
