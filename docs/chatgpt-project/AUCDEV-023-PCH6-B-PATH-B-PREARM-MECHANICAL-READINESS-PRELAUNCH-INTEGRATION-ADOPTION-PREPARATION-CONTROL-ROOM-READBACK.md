# AUCDEV-023 PCH6-B Path-B prearm prelaunch integration/adoption preparation — INDEPENDENT CONTROL ROOM READBACK

Record-only publication authority:
AUCDEV-023-PCH6B-730D2B29-PATHB-PRELAUNCH-INTEGRATION-PREP-CRRB-PUB-20261005-01
(readback subject: preparation publication
`1cf7badb1b6b4a60e5f438730692502e154311b0` over base
`536000c0229e49be40798d45468705f92bb72e20`)

AUCDEV_023_PCH6B_PREARM_PRELAUNCH_INTEGRATION_ADOPTION_PREPARATION_CONTROL_ROOM_READBACK =
PARTIALLY_ACCEPTED /
GENERATED_LAST_INTEGRITY_PASS /
STATIC_CONTROL_FLOW_SUBSTANTIALLY_SUPPORTED /
PREARM_VERIFIER_GATE_INTENT_ACCEPTED /
PYTHON_EXECUTION_ENVIRONMENT_BINDING_BLOCKING_DEFECT /
PATH_CHECK_TO_EXEC_BYTE_BINDING_BLOCKING_DEFECT /
REMEDIATION_REQUIRED_BEFORE_OPERATIONAL_ADOPTION /
NO_ATTEMPT_AUTHORITY /
AUDITOR_B_AUTHORITY_NONE /
AUDIT_VERDICT_NONE /
QUALIFICATION_NONE /
INSTALLATION_NONE

This disposition is NOT: audit PASS; a frozen-target product verdict;
acceptance for operational adoption; replacement-attempt authority;
Auditor-B authority; qualification; installation. THIS READBACK GRANTS
NOTHING.

## 0. Role and bounds of this session

This session is the bounded RECORD-ONLY publisher of the ALREADY-completed
independent Control Room readback of the AUCDEV-023 PCH6-B prelaunch
integration/adoption preparation candidate (preparation publication
`1cf7badb1b6b4a60e5f438730692502e154311b0`, canonical preparation record
blob `58c79be39a2ec8c06c876aabecd35d815af351f2`). This session is NOT the
substantive Control Room decision-maker (the readback was already
completed), NOT an implementer, NOT an auditor, NOT an attempt executor,
NOT an /audit-council executor, NOT a provider/model executor, and NOT
qualification or installation authority. Every verification below is
DATA-ONLY: hashing, byte/blob equality, tar census, AST parsing and text
scanning of SHA-verified non-secret bytes; NO archive member was executed
and NO test was re-executed.

## 1. Exact live bootstrap (verified before writing)

Live GitHub master == origin/master == local HEAD ==
`1cf7badb1b6b4a60e5f438730692502e154311b0` EXACT at bootstrap (ls-remote
authoritative; fetch rc 0); root tree
`eb71237fbf267799e19d7cac56d9d6bf99918a81` EXACT; sole parent
`536000c0229e49be40798d45468705f92bb72e20` EXACT (single-parent
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
identities recorded (CURRENT `9ba6233b778fad8c73f23bcd42a4171b47e56e58` /
BACKLOG `db7db8537f292f96866767e8321f896d911acd13` / preparation record
`58c79be39a2ec8c06c876aabecd35d815af351f2` / accepted PREARM CR readback
`16cc958a5f4d1b67a524d80342151ee641bd9fcf` / accepted PREARM remediation
report `877f1b6be7073972d7b1719630912358d0faf8b6` / settled attempt
execution report `d210e5adc13c2bafe9f5de23970be3ac51f2f1f5` / settled
attempt CR readback `3b9a5c8fd2658c24be7a65b5d14098856d9498b8` / update
protocol `42955b85710f09579cd0fd9174d042de231d060d`). CURRENT/BACKLOG
working copies were verified byte-identical to the base blobs before
editing. THIS record's path was ABSENT at base with zero full-history
path rows. Repository drift (pre-existing smoke-fixture / smoke-fixture-103
gitlink rows and pre-existing untracked workspaces/handoffs) preserved
UNSTAGED. Live master re-resolved EXACT immediately before staging and
again immediately before commit.

## 2. Readback subject geometry (verified data-only)

`536000c0229e49be40798d45468705f92bb72e20` ->
`1cf7badb1b6b4a60e5f438730692502e154311b0` is exactly ONE fast-forward
commit changing exactly three tracked paths (NEW preparation record
`58c79be39a2ec8c06c876aabecd35d815af351f2`; M CURRENT ->
`9ba6233b778fad8c73f23bcd42a4171b47e56e58`; M BACKLOG ->
`db7db8537f292f96866767e8321f896d911acd13`). No protected tree touched;
frozen target tree unchanged; no helper, test, channel, VM, credential or
event-package path tracked.

## 3. Generated-LAST handoff integrity (data-only, zero member execution)

`AUCDEV-023-PCH6B-PATHB-PRELAUNCH-INTEGRATION-PREP-HANDOFF-20261005-01.tar.gz`
inspected in place (tar stream reads only; ZERO members extracted to any
executable context and ZERO executed): outer size 1149181 B EXACT; outer
SHA-256 `f7c3e8a4b9c081bf9a6e314f8f28000260cfd3c3eef178632c2810f83f85c9d0`
EXACT, re-derived TWO independent ways this session (sha256sum AND python
hashlib); census 44 members = 30 regular + 14 directories + 0 symlinks /
0 hardlinks / 0 special, 0 duplicate paths, 0 unsafe/traversal paths, one
common top-level prefix; exactly one SHA256SUMS with 29 manifest rows, NO
self-row, README.md exactly once; independent payload rehash 29/29 PASS;
exact manifest/payload-set equality both directions SATISFIED. The
archived Git copies verified by BOTH recomputed git blob identity AND
direct byte equality to the live base blobs: preparation record
`58c79be39a2ec8c06c876aabecd35d815af351f2`, CURRENT
`9ba6233b778fad8c73f23bcd42a4171b47e56e58`, BACKLOG
`db7db8537f292f96866767e8321f896d911acd13`. The archived candidate test
history (run-001-red, run-002, run-003, run-004-final,
run-005-repeatability) was READ as SHA-verified bytes and classified per
§7; the Control Room did NOT re-execute any test.

## 4. Candidate identity re-derivation (bytes govern; read/hash only)

Re-derived EXACT from the preparation workspace
`/home/isa/aucdev023-pch6b-prelaunch-integration-adoption-prep-20261005-01/`
(hash-bound by the preparation publication; NEVER executed this session):

- adapter `bin/prelaunch_prearm_gate_v1.py`: 12267 B, SHA-256
  `566687a4d25a10a703acf880caa8b714cddd174344bf0ca62d41d950937856c4`
  EXACT (two independent derivations: sha256sum AND python hashlib) —
  matches the tasked candidate identity EXACT.
- accepted verifier `deps/verify_prearm_ready_v1.py`: 10778 B, SHA-256
  `3f4438e9e76c29d2c4e0b2889c6ec0614afc07e08f5df34a03276e95a5f8c61e`
  EXACT (two independent derivations) — byte-identical to the ACCEPTED
  prearm remediation verifier identity.
- accepted waiter `deps/prearm_sender_v1.py`: 10878 B
  `b0ec4e7ee0ce6e047372a694c58f442a73dc8586d9d8742bba588406acd5c097`
  EXACT; accepted minter `deps/gen_prearm_challenge_v1.py`: 1960 B
  `af8671cf578c8f6c6bfc70adeee3cddddb9cb51013307a53c33a05375c2b4e49`
  EXACT.
- accepted sender `send_once_v2.py` (d7): 3954 B, SHA-256
  `1cc6e22efb1cec386d6edebcbb3f42e4feac1896c101d7c465b8dac569d6a8dd`
  EXACT — re-derived THREE independent ways this session across two
  preserved non-secret copies (remediation workspace original + attempt
  workspace copy, each sha256sum, plus python hashlib, plus cmp byte
  equality); read and hashed only, NEVER executed.

ACCEPTED_PREARM_BYTES_MISMATCHED did NOT occur. The archived copies of
these files inside the SHA-verified handoff rehash to the same identities
(manifest §3).

## 5. FINDING 1 — AUCDEV023-CR-PCH6B-PRELAUNCH-INT-001

Name: PYTHON_EXECUTION_ENVIRONMENT_NOT_MECHANICALLY_CLOSED.
Classification: HARNESS / EXECUTION-PROTOCOL DEFECT. Support: OBSERVED
SOURCE FACT + MECHANICAL EXECUTION-SEMANTICS INFERENCE.

Observed source facts (all re-derived data-only this session by AST
parsing and text scanning of the SHA-verified adapter
`566687a4d25a10a703acf880caa8b714cddd174344bf0ca62d41d950937856c4`):

- the single `subprocess.run` verifier invocation carries ONLY the
  keywords `capture_output` and `timeout`; NO `env=` parameter is
  supplied (adapter lines 239-240);
- the verifier argv is `[verifier_interpreter, verifier_path, ...]` with
  NO Python isolated-mode flag (zero `-I` / `-E` / `-S` occurrences
  anywhere in the adapter);
- NO PYTHONPATH / PYTHONHOME / PYTHONSTARTUP / PYTHONNOUSERSITE /
  sitecustomize / usercustomize closure of any kind is present (zero
  code occurrences of every token; zero `os.environ` access by the
  adapter's own invariant);
- the downstream transition uses `os.execv` (adapter line 258), which
  PRESERVES the current process environment into the downstream
  launcher;
- the operator template line 89 shows
  `python3 bin/prelaunch_prearm_gate_v1.py --contract <contract.json>`
  — a PATH-resolved interpreter and a RELATIVE adapter path.

Impact: exact verifier/interpreter file hashes do NOT by themselves
mechanically bind the semantics actually executed when the ambient
interpreter/startup environment can alter Python startup, module search
and import behavior (e.g. environment-controlled `sitecustomize`
importation in the invoked interpreter, or `PYTHONHOME`-driven stdlib
redirection). The current 28/28 matrix does not exercise malicious or
hostile Python startup-environment classes. The adapter's hash binding
closes the FILE-identity channel, not the INTERPRETER-STARTUP channel.

Disposition: OPEN / BLOCKING_BEFORE_OPERATIONAL_ADOPTION.

## 6. FINDING 2 — AUCDEV023-CR-PCH6B-PRELAUNCH-INT-002

Name: HASH_CHECKED_PATH_BYTES_NOT_ATOMICALLY_BOUND_TO_EXECUTED_BYTES.
Classification: HARNESS / EXECUTION-PROTOCOL DEFECT. Support: OBSERVED
SOURCE FACT + TRUST-BOUNDARY INFERENCE.

Observed source facts (same SHA-verified adapter bytes):

- the verifier path is hashed during `check_bound_file` (adapter lines
  114-125, invoked at line 211) via the shared pathname reader;
- execution occurs LATER through the same PATHNAME string
  (`c["verifier_path"]`, adapter lines 227-239) in `subprocess.run`;
- the downstream path is hashed BEFORE verifier execution (lines
  214-217) and executed LATER through that pathname via the interpreter
  argv (lines 255-258);
- both interpreter paths are similarly hash-checked (lines 212-213,
  216-217) and later executed BY PATHNAME (line 239 verifier
  interpreter; line 258 `os.execv(c["downstream_interpreter"], ...)`);
- NO opened-file-descriptor / inode / immutable-object continuity
  mechanically binds the checked bytes to the subsequently executed
  bytes: the hash reader opens by pathname and closes, and each later
  execution re-resolves the pathname (no `fexecve`-style or
  `/proc/self/fd` execution, no fd held across check-to-use).

Impact: a pathname replacement between identity check and use is not
mechanically excluded. The existing tests cover pre-check mismatch and
post-contract tamper (tests 01, 04, 12, 27), NOT a check-to-exec
replacement performed between the binding stage and the invocation stage
of a single adapter run.

Disposition: OPEN / BLOCKING_BEFORE_OPERATIONAL_ADOPTION.

## 7. Held accepted evidence and test classification

The following VALID candidate evidence is HELD and NOT discarded: the
generated-LAST integrity PASS (§3); exactly ONE verifier subprocess site
and ONE downstream exec site with NO retry/fallback path; the exact
admission-token evaluation logic (rc 0 AND exactly one
MECHANICAL_PREARM_READY=VERIFIED AND zero NOT_VERIFIED/REASON/stderr
tokens); textual ARMED having NO admission input; NO reusable permit
artifact intentionally created; the VM/QGA/channel/credential/
run_attempt/provider census remaining zero; and the archived test
history remaining RED 0/28 -> 18/28 -> 26/28 -> 28/28 -> 28/28.

Test classification: HASH-BOUND PRESERVED IMPLEMENTATION RUNTIME
EVIDENCE / SOURCE-CORROBORATED / NOT INDEPENDENTLY RE-EXECUTED BY
CONTROL ROOM / DOES_NOT_COVER_INT_001_OR_INT_002.

## 8. PREARM-001 status preserved exactly

AUCDEV023-CR-PCH6B-PREARM-001 =
MECHANICALLY_REMEDIATED / CONTROL_ROOM_ACCEPTED_CANDIDATE /
OPERATIONAL_ADOPTION_PENDING / NOT_YET_CLOSED — unchanged. The two new
findings concern INTEGRATION/ADOPTION of the gate, NOT the demonstrated
original textual-ARMED process-liveness remediation, which remains
accepted at its recorded candidate strength. Nothing in this readback
reopens, downgrades or closes PREARM-001.

## 9. R1 / R2 / R3 preserved unchanged

R1 CREDENTIAL-SOURCE ATTACHMENT OPERATOR PREMISE, R2 POST-VERIFY
LIVENESS RACE (TOCTOU, reduced-not-eliminated), and R3 PRESERVED
V2/RUNTIME EVIDENCE STRENGTH are preserved EXACTLY as recorded by the
accepted PREARM remediation readback `16cc958a5f4d1b67a524d80342151ee641bd9fcf`
and restated by the preparation record. INT-001 and INT-002 are NEW
blocking INTEGRATION defects and are deliberately NOT folded into R2.

## 10. Governance held

EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 INSTANTIATED;
PATH-B slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT. AUCDEV-023 = P1 /
READY / NOT DONE. The existing Auditor-A attempt ...-AUDITOR-A-01
remains SPENT / SINGLE-USE / NO-RETRY; NO replacement Auditor-A attempt
exists; NO replacement attempt is reserved or minted; Auditor-B
authority = NONE; FIRST_PASS_A = ABSENT; MODEL_ENGAGEMENTS_USED = 0 for
the settled attempt; qualification NONE; installation NONE; frozen
target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` AUDIT SUBJECT / NOT
AUTHORITY; PCH6-B-SD-002 / PCH6-CR-BSD-001 AWAITING FRESH INDEPENDENT
AUDIT / NOT CLOSED; PCH6-B-SD-001 RETAINED / OPEN; the five CRED/CREDCH
closures at exactly their LIMITED strengths;
INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED; installed Audit
Council NOT AUTHORITY FOR THIS EVENT; NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE
DISCLOSED RESIDUAL; STAGING-RB-001 / CREDCH-RB-EV-001 preserved; frozen
external event root untouched append-only; historical records/handoffs
NOT rewritten; prior closures RETAINED; no audit execution; no audit
PASS.

## 11. Honest session iteration (instrument-side only; no erasure)

Every first output is preserved under the untracked evidence workspace
`aucdev023-pch6b-prelaunch-integration-crrb-pub-20261005-01/evidence`;
NO failed observation was rewritten as PASS without a corrected
re-derivation on IDENTICAL bytes:

- T-1: handoff census v1 compared top-relative SHA256SUMS rows against
  unnormalized tar member names, producing a mirror-image 29-row false
  MISSING set (the known prior-session normalization class) — corrected
  normalization re-ran FROM SCRATCH on identical bytes 29/29 PASS with
  set equality SATISFIED both directions.
- T-2: the archived-Git-copy verification script v2 tripped its own
  prefix assertion on the archive's top-level DIRECTORY member (the
  members list includes the prefix directory itself) — an instrument
  defect with zero state impact; corrected to regular-members-only and
  re-run from scratch with all three blob identities and byte equality
  EXACT.

(The rotation-builder and battery instrument iterations of THIS
publication session are recorded in §12's battery evidence; every
correction re-ran from scratch on IDENTICAL staged bytes.)

## 12. Zero-execution publication census

VM_RUNS 0; QGA/virsh invocations 0; EVENT_HOST_DEFINES 0; channel
connections 0; channel re-probes 0; connect attempts 0; socket probes 0;
OPERATOR_SEND_NOW created/consumed 0; send_once_v2 invocations 0 (read
and hashed only); bridge-v2 invocations 0; V2/frozen mutations 0; real
credential stats/opens/reads/hashes/transmissions 0;
BOOTSTRAP_AUTHORITY imports/constructions 0; RUN_ATTEMPT_CALLS 0;
attempt accounting records 0; report sinks 0; attempt ids created 0;
CLAUDE/CODEX/AUDIT-COUNCIL executions 0; provider/model/frontier
requests 0; MODEL_ENGAGEMENTS_CONSUMED 0; ARCHIVE_MEMBER_EXECUTIONS 0;
TEST_EXECUTIONS 0 (the archived 28-matrix was READ, never re-run); the
candidate adapter, verifier, waiter, minter, sender copy, fixtures and
harness were read and hashed ONLY. The only executions: ordinary
Git/GitHub publication mechanics and local data-only python
text/hash/AST/tar tooling on non-secret bytes.

## 13. Publication safety

Staged EXACTLY the three authorized documentation paths (THIS NEW
canonical readback record; M CURRENT; M BACKLOG). The original candidate
preparation record, the accepted PREARM records, the settled attempt
records, the protected trees, the frozen target, the canonical runtime,
the event host and the frozen external event root are all UNCHANGED. No
helper or test source, no channel helper, no send_once_v2 bytes, no
domain XML, no VM image, no credential/auth/session material, no .jsonl,
no event-package tracked path and no event-root file committed.
Repository drift preserved unstaged. The disposition block above is
token-for-token exact (12 tokens plus the key) with the disposition key
and the PARTIALLY_ACCEPTED token present in THIS record, CURRENT L3/L23
and the BACKLOG bullet. PREARM-001 is recorded as NOT_YET_CLOSED (full
preserved quad in §8) and is NOT fully CLOSED anywhere in staged content;
INT-001 and INT-002 are recorded OPEN / BLOCKING_BEFORE_OPERATIONAL_
ADOPTION; no replacement attempt, attempt reservation or Auditor-B
authority appears anywhere in staged content; credential/secret
mechanical scan clean over the NEW record and all diff-added lines; the
hex-literal gate machine-verifies every >=7-char boundary-delimited
non-decimal hex literal in the NEW record and diff-added lines
case-insensitively against the session-derived independently-verified
identity allow-set (verified git/tree/blob identities, the re-derived
candidate/dependency identities, the sender d7 identity, the archive
outer SHA-256 and the archived-payload SHA-256 values rehashed this
session; decimal-only and verified short prefixes exempt). The FULL
record-only precommit gate battery ran from scratch on the FINAL staged
bytes and ALL PASSED (gate count in the commit message and
FINAL-RETURN). The rotation zones were computed-before-write by an
assertion-guarded builder and re-asserted from the staged blobs
(CURRENT: replace@3 + replace@11 + replace@23-24 + insert@tail; BACKLOG:
insert-after-prelaunch-prep-bullet x1 + insert@tail; details in the
battery evidence).

## 14. Self-commit identity rule

This publication records the exact authorized base
`1cf7badb1b6b4a60e5f438730692502e154311b0`, the staged write-tree,
branch master and the disposition in the commit message. The commit
cannot contain its own final SHA, so the exact resulting publication SHA
and result root tree are reported in the FINAL-RETURN, the post-push
GitHub readback and the generated-LAST handoff (created after
commit/push).

## 15. NEXT — exactly one, grants nothing

OPERATOR DECISION ON WHETHER TO AUTHORIZE A NARROW ZERO-MODEL REMEDIATION
OF AUCDEV023-CR-PCH6B-PRELAUNCH-INT-001 AND
AUCDEV023-CR-PCH6B-PRELAUNCH-INT-002 BEFORE ANY OPERATIONAL ADOPTION,
ATTEMPT-SPECIFIC PRELAUNCH PACKAGE, REPLACEMENT AUDITOR-A ATTEMPT
AUTHORITY, OR AUDITOR-B AUTHORITY IS CONSIDERED.

Recording this NEXT grants NOTHING. The remediation decision is separate
and must not be inferred.

## 16. Standing negative constraints

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
