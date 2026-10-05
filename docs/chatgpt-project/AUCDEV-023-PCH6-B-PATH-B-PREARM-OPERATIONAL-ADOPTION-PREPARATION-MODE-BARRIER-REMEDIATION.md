# AUCDEV-023 PCH6-B Path-B — Prearm operational-adoption preparation MODE-BARRIER REMEDIATION (OPADOPT-PREP-001)

**Disposition:** `AUCDEV_023_PCH6B_PREARM_OPADOPT_PREP001_MODE_BARRIER_REMEDIATED_AS_CANDIDATE` — `SUCCESSOR_SOURCE_BYTES_UNCHANGED` / `AUTHORITATIVE_PREPARED_OBJECT_MODE_0000` / `DIRECT_PATH_EXECUTION_DENIED` / `EXPLICIT_INTERPRETER_PATH_EXECUTION_DENIED` / `ORDINARY_FILE_LOADER_ACCESS_DENIED` / `HISTORICAL_0600_CANDIDATE_SUPERSEDED_NOT_AUTHORITY` / `V2_DERIVED_SECURITY_MECHANICS_PRESERVED` / `REUSABLE_HOST_LAUNCH_PROCEDURE_SCOPE_PRESERVED` / `AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK` / `PREARM_001_NOT_YET_CLOSED` / `NO_SUCCESSOR_ACTIVATION` / `NO_CHMOD_AUTHORITY_USED` / `NO_OPERATIONAL_ADOPTION` / `NO_ATTEMPT_AUTHORITY` / `AUDITOR_B_AUTHORITY_NONE` / `AUDIT_VERDICT_NONE` / `QUALIFICATION_NONE` / `INSTALLATION_NONE`

This remediation closes NOTHING. OPADOPT-PREP-001 moves to
REMEDIATED_AS_CANDIDATE / AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK /
NOT_CLOSED. PREARM-001 remains NOT_YET_CLOSED.

## 1. Authority and role

Implementation authority `AUCDEV-023-PCH6B-OPADOPT-PREP001-MODE-BARRIER-REMEDIATION-20261005-01`.
The operator explicitly authorized ONLY:

> "AUTHORIZE AUCDEV-023 narrow zero-model remediation of
> AUCDEV023-CR-PCH6B-OPADOPT-PREP-001 only, so that the authoritative
> operational-adoption successor cannot execute through either direct execution
> or explicit interpreter invocation while in its PREPARED_ONLY state; preserve
> the accepted v2-derived security mechanics and operational-adoption procedure
> scope, with no successor activation or chmod authority, no operational
> adoption, no attempt-specific prelaunch package, no replacement attempt
> minting or execution, no real credential use, no channel connection, no
> VM/QGA execution, no run_attempt, no model execution, and no Auditor-B
> authority."

This session is the bounded IMPLEMENTER of exactly
AUCDEV023-CR-PCH6B-OPADOPT-PREP-001
(`PREPARED_ONLY_MODE_BARRIER_BLOCKS_DIRECT_EXEC_ONLY`, published by the
accepted OPADOPT-PREP Control Room readback at commit `c351ddf7…`). It is
NOT the Control Room, NOT an auditor, NOT an attempt executor, NOT an
operational-adoption activator, NOT a qualification or installation
authority. This is MODE-BARRIER REMEDIATION authority only: no successor
activation authority, no chmod-to-activation authority, no operational
adoption, no attempt-specific packaging authority, no replacement attempt
authority, no VM/QGA authority, no credential/channel authority, no
run_attempt authority, no model/provider authority, no Auditor-B
authority.

## 2. Exact live bootstrap

Live GitHub master == origin/master == local HEAD ==
`c351ddf7bb26a9803c6d794064b387e1123577db` EXACT at bootstrap
(ls-remote authoritative; fetch rc 0), re-resolved EXACT immediately
before staging and again immediately before commit. Root tree
`dfc7401c7a60cb0dc62a9361c7899936a5bf1569` EXACT; sole parent
`336c8cdd1917cd77da68575e72013d84e389e6a1` EXACT (single-parent
fast-forward geometry); trust anchor `3058868416241d394cfaaa40cc585085db486f37`
ancestor rc 0; frozen audit target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed`
(tree `2585796efd5cb6902226cfff785bb901297a15e3`) present, ancestor,
UNTOUCHED, AUDIT SUBJECT / NOT AUTHORITY; protected trees
bootstrap-authority `154975872e15d53e1706016f5bb60c83727004f0` /
bootstrap-supervisor `3056e577259ab0b0b0472f82ebc306506f3e084c` /
qualification-harness `5b8d5e5465923740470ff63ed9b8683f257a3787` /
skill `efd8c2e48edbb25795b3aacb1ce3c23fde10082a` held EXACT at base. The
six mandated canonical records fetched at the exact base with blob
identities verified (CURRENT `9bf69dc4d1df61d7f53685c5381e42c458c1e283` /
BACKLOG `a822e5fabbe6547e30907ac0ffd3f10cda68e1f0` / OPADOPT preparation
Control Room readback `d6f9cf5ae665ff3c5c5ab6ec6a549c436b04b722` / OPADOPT
preparation record `5007b4a960057e70f29a8f6a8750a4720e505f47` / accepted
handoff-fidelity-correction Control Room readback
`00fd9efcfa113252c27b757ee826a47c7db3dffd` / update protocol
`42955b85710f09579cd0fd9174d042de231d060d`) with CURRENT/BACKLOG working
copies verified byte-identical to the base blobs before editing. This
record's path ABSENT at base with zero full-history path rows. Repository
drift (pre-existing smoke-fixture / smoke-fixture-103 gitlink rows and
pre-existing untracked workspaces/handoffs) preserved UNSTAGED. Session
euid 1000 (ordinary non-root `isa`) — the POSIX DAC test boundary.

## 3. Subject source — byte immutability (SOURCE_DIFF = ZERO)

- Successor source bytes: `prelaunch_prearm_gate_opadopt_v1.py`, SHA-256
  `410b141054c347f42422e402dde22a966f608adf1f83605eab539656d29cebf4`,
  20535 bytes — ALREADY source-reviewed; NOT modified by this
  remediation.
- Accepted v2 ancestor `df2dea2911f8547a79326932b788ca916a7e5a502652bc2125fad5954e455d81`
  (19695 B, preserved-workspace copy re-hashed EXACT this session, mode
  0755) — NOT modified.
- NO in-source activation guard was introduced: an in-source guard runs
  only AFTER the interpreter has already opened, parsed and started
  executing successor source bytes, so it could not establish the required
  prepared-state property at the OS boundary. The barrier is therefore a
  FILESYSTEM-LEVEL property of the authoritative object, with the source
  bytes untouched: pre-creation hash of the source bytes ==
  same-fd post-write rehash == `410b1410…` == the historical candidate ==
  the data-only review copy, and the authoritative object's
  identity (dev/ino/size/mode) plus ctime are unchanged since creation.

## 4. Historical 0600 candidate — superseded, preserved

`/home/isa/aucdev023-pch6b-prearm-operational-adoption-prep-20261005-01/bin/prelaunch_prearm_gate_opadopt_v1.py`
— mode 0600, 20535 B, dev 52 ino 33214498, mtime 1791169164, SHA-256
`410b1410…` re-hashed EXACT before AND after all remediation work. It was
NOT chmod'ed, overwritten, renamed, deleted or executed; it remains
immutable historical evidence now classified HISTORICAL /
SUPERSEDED_AS_PREPARED_STATE_AUTHORITY / NOT_OPERATIONAL_AUTHORITY. No
future procedure/binding document points to it (verified by scan, §9).

## 5. Authoritative PREPARED_ONLY object — mode 0000 from inception

New non-secret workspace
`/home/isa/aucdev023-pch6b-opadopt-prep001-mode-barrier-remediation-20261005-01/`.
Authoritative object:
`prepared-authority/bin/prelaunch_prearm_gate_opadopt_v1.py`, created by
`instruments/create_authoritative_0000.py` in ONE bounded sequence with
ZERO chmod anywhere:

1. exact bytes obtained from the preserved historical 0600 candidate
   (read as its owner; historical object only READ), pre-hash required ==
   `410b1410…`;
2. fresh never-existing path required ABSENT (lexists False; O_EXCL
   protects against pre-existing-path substitution);
3. single `os.open(O_CREAT | O_EXCL | O_RDWR | O_CLOEXEC, 0o000)` —
   mode 0000 FROM INCEPTION (umask cannot add permission bits);
4. the exact 20535 verified bytes written THROUGH that already-open fd;
   fsync;
5. same-fd fstat: regular file; size 20535; mode exactly 0000;
   uid 1000 == creator euid; nlink 1; dev 52 ino 33239873;
6. rewind (lseek 0) and independent SHA-256 THROUGH THE SAME still-open
   fd before close: 20535 bytes, digest `410b141054c347f42422e402dde22a966f608adf1f83605eab539656d29cebf4` EXACT;
7. fd closed; post-close lstat persistence: mode 0000, size 20535,
   dev 52 ino 33239873.

Creation-window immutability evidence (instrument gap disclosed in the
ledger: the creation JSON did not record `st_ctime_ns`): the object's
ctime `1791191502.570723561` PRECEDES the creation-evidence write at
`1791191502.578251819` by 7.5 ms with ctime == mtime, so the last inode
change IS the creation sequence; any later chmod/permission transition
would have bumped ctime above that bound. The final regression run
additionally asserted ctime stability across the whole suite window, and
the chmod-site scan shows zero chmod sites targeting the authoritative
object anywhere in the session instruments/suite. After creation, the
authoritative path was NEVER opened for reading again in this session
(no later source read required or permitted); every later observation is
lstat-only.

**Claim boundary (exact).** The permitted candidate-strength claim: the
authoritative PREPARED_ONLY object is mechanically unreadable and
non-executable by the ordinary non-root operator process under POSIX DAC,
therefore ordinary direct path execution and ordinary explicit
interpreter/file-loader invocation of that authoritative path fail before
successor source execution. NOT claimed: protection against root;
protection against a file owner who performs an unauthorized permission
change; cryptographic immutability of the filesystem inode; successor
activation; operational adoption. The permission transition remains
governance-controlled and separately authorized.

## 6. Data-only review copy (NON-AUTHORITY)

`data-only/bin/prelaunch_prearm_gate_opadopt_v1.py` — SHA-256
`410b1410…` EXACT, 20535 B, mode 0644 readable. It is NOT an activation
source, NOT a future launch path, NOT an operational authority, NOT a
permit. The reusable procedure/binding contain ZERO references to any
readable evidence copy (scan-verified, §9); the generated-LAST handoff
carries this copy as readable evidence.

## 7. Prepared-state negative probes (non-root; euid 1000)

`instruments/probe_prepared_state.py` (run-001, FINAL), against the
authoritative object after the creation fd was closed — every probe
DENIED with ZERO successor diagnostics:

- **A** fresh `open(O_RDONLY | O_NOFOLLOW)` → EACCES;
- **B** direct exec `[authoritative, --contract, synthetic]` → EACCES at
  the OS boundary (zero successor bytes executed);
- **C** explicit `/usr/bin/python3 -IS <authoritative> --contract
  <synthetic>` → nonzero, `can't open file … [Errno 13] Permission
  denied`, ZERO `PRELAUNCH_GATE_*` tokens, ZERO admission token, ZERO
  verifier invocation (no source-start marker), ZERO synthetic seam
  reach — the exact missing OPADOPT-PREP-001 class;
- **D** separate-process `runpy.run_path(authoritative)` → PermissionError
  before successor source execution; `importlib` `SourceFileLoader
  .get_source` variant → EACCES likewise;
- **E** plain non-root `open(..., "rb")` → EACCES.

These validate the OS-level read/execute barrier, NOT a source-internal
guard. The identical probe instrument run against the RED disposable 0600
copy reports the READ-class probes GRANTED/STARTED (§8), so the GREEN
denials are attributable to the mode-0000 barrier alone.

## 8. RED-first evidence — the 0600 interpreter-invocation bypass

`instruments/red_0600_bypass_evidence.py` (run-003, FINAL) against a
BYTE-EXACT DISPOSABLE copy of the exact `410b1410…` source at mode 0600
in a fresh private temp dir (never the historical authoritative path),
destroyed afterwards (verified): ordinary read GRANTED (owner-readable);
direct execution denied (EACCES/PermissionError — the old barrier's only
covered direction); EXPLICIT INTERPRETER INVOCATION
`/usr/bin/python3 -IS <0600-copy> --help` rc 0 WITH the successor's own
argparse description ("operational-adoption preparation successor opadopt
v1") in the output — the interpreter opened, parsed and started executing
the successor source WITHOUT its execute bit; harmless form (cannot reach
verifier/launch substance). The shared probe instrument on the same copy:
A/E GRANTED, C/D/D2 STARTED. This reproduces the finding
PREPARED_ONLY_MODE_BARRIER_BLOCKS_DIRECT_EXEC_ONLY exactly, as evidence
of the finding, not operational execution.

## 9. Procedure / binding remediation (narrow, ordering preserved)

`operator/FUTURE-AUDITOR-A-HOST-LAUNCH-PROCEDURE-modebarrier-v2.txt`
(SHA-256 `d369d81057172eb4619daaa569cbea36693e03bc0c526e7bd4955f1e6b21e5ab`)
and
`integration/FUTURE-AUDITOR-A-HOST-LAUNCH-BINDING-modebarrier-v2.json`
(SHA-256 `c8d2da8ad52100f065ff77b9d060c8298d20b4486a98573e4af78d6bd728d62d`):
narrow v2 revisions preserving ALL previously accepted ordering (PRE-GATE
PREFLIGHT → PREARM GATE → immediate same-process execve → the future
downstream launcher's first substantive irreversible operation = the
exact pre-authorized host guest-runner launch seam) and adding ONLY the
PREPARED_ONLY artifact rule: the authoritative successor source object is
mode 0000 while PREPARED_ONLY (created from inception); the historical
0600 candidate is superseded/non-authority (identified by identity only —
ZERO references to the historical path); DATA-ONLY review copies are
never operative launch paths (ZERO "data-only" references in
procedure/binding); any future permission transition/materialization/
activation requires a NEW explicit operator decision and fresh Control
Room review; this task grants no such transition and prescribes no
activation action. The binding adds a `prepared_only_artifact_rule`
section (authoritative object role + SHA-256 + prepared-state mode 0000 +
denial boundary + historical supersession + evidence-copy policy +
future-transition rule) and three new prohibited_now entries. Scans
(suite test 57 + MBR-22/23): zero historical-path references, zero
evidence-copy references, authority identified by role + exact identity
only.

## 10. Source security mechanics — preserved by byte identity

Because the source bytes remain EXACTLY `410b1410…`, every previously
supported mechanic is byte-identical and INT-001 / INT-002 remain CLOSED
at their retained strengths: isolated `-IS` shebang startup with
sys.flags verification; literal CLEAN_ENV with zero ambient environment
access; PR_SET_DUMPABLE=0; fd-exec capability gate; O_NOFOLLOW sealed
memfd snapshots with regular-file enforcement, SHA-256 pinning,
F_SEAL_SEAL|SHRINK|GROW|WRITE and sealed-byte rehash; the accepted
verifier exact-byte dependency (3f4438e9…) invoked EXACTLY ONCE under
-IS + CLEAN_ENV; exact PREARM admission semantics with ZERO textual-ARMED
effect; exactly one same-process fd-bound `os.execve` transition; ZERO
`os.execv`, retry, fallback, reusable permit, network, credential, VM,
QGA, BootstrapAuthority or run_attempt capability. No source change was
made to satisfy this remediation.

## 11. Test evidence

Ported regression matrix `tests/run_tests.py` (SHA-256
`0b9b92fa1a2e2785852d6a2ca37ef8f2c42c9a34fbf12cd0425f05003381914c`,
94021 B): the prior 53-test OPADOPT suite with the barrier tests
retargeted/strengthened to the mode-0000 dual-target model (AUTHORITATIVE
object lstat-only; regression reads the byte-exact DATA-ONLY copy; every
execution through disposable 0755 sandbox copies destroyed afterwards)
plus five NEW tests 54-58 (authoritative unreadable; explicit-interpreter
denial with zero diagnostics; runpy/file-loader denial;
procedure/binding non-authority path separation; authoritative-object
metadata immobility incl. ctime across the suite) — 58 tests +
POST-SUITE-BARRIER:

- matrix run-001 57/59 (one scanner self-hit, ledgered T-1) — preserved;
- **run-002 FINAL 59/59 PASS** (incl. embedded fresh-sandbox self-repeat);
- **run-003 repeatability FROM SCRATCH 59/59 PASS**;
- run-002 and run-003 outputs byte-identical (cmp rc 0; both SHA-256
  `7263e04d9649f784bb4233de025e07faff19ae22ac9437565d6e9139dc47cf65`) —
  deterministic suite, disclosed as NOT independently distinguishable
  output evidence (same known non-blocking class as the accepted
  preparation session);
- POST-SUITE-BARRIER PASS in both: authoritative object still mode 0000
  with dev/ino/size/ctime identical to suite start; data-only copy hash
  stable; authoritative object still 0000 after ALL tests (MBR-30/31).

**MBR acceptance matrix** (`instruments/mbr_matrix.py`, run-003 FINAL):
**MBR-01..35 ALL 35/35 PASS** — exact live base; historical SHA; historical
preservation; SOURCE_DIFF ZERO; fresh path; mode 0000 from inception; no
chmod (site scan + ctime bound); same-fd rehash/size/mode/regular-nlink-uid;
post-close read/direct-exec/interpreter/runpy+loader denials; zero
diagnostics/verifier/seam during denials; RED bypass + RED copy destroyed;
data-only hash; procedure/binding path separation; ordering preserved;
future-activation authority language; no activation performed; no
attempt-specific package (integration/ holds only the NON-AUTHORITY
binding template and the UNMODIFIED carried contract documentation
`92c09f42…`); no replacement attempt; inherited regressions 59/59;
authoritative mode/identity after all tests; zero real-runtime capability
(AST census over session-authored artifacts); no successor-source byte
change; no premature closure claim; full repeatability.

## 12. Honest session iteration

Full ledger in the workspace `evidence/HONEST-ITERATION-LEDGER.md`:
R-T1/R-T2 RED-instrument encoding iterations (runs preserved; R-T3 FINAL);
I-1 disclosed creation-JSON ctime gap covered by the recorded
creation-window bound; T-1 suite scanner self-hit (run-001 preserved;
run-002/run-003 FINAL); B-T1..B-T3 MBR-matrix scan iterations including
the scanner correctly REFUSED by the authoritative mode-0000 object when
it tried to read it (runs preserved; B-T4 run-003 35/35 FINAL). NO failed
observation was rewritten as PASS without a corrected re-derivation on
IDENTICAL bytes/state.

## 13. Zero-real-runtime census

VM_RUNS 0; EVENT_HOST_DEFINES 0; QGA/virsh 0; channel connections/probes/
connect attempts/socket probes 0; OPERATOR_SEND_NOW created/consumed 0;
send_once_v2 invocations 0 (carried d7 copy read+hashed only, NEVER
executed); bridge-v2 0; V2/frozen/canonical-runtime/event-host/event-root
mutations 0; REAL_CREDENTIAL stats/opens/reads/hashes/logs/transmissions
0; BootstrapAuthority imports/constructions 0; run_attempt calls 0;
attempt accounting records 0; attempt ids created 0; replacement attempts
created/reserved/minted 0; provider/model/frontier requests 0;
CLAUDE/CODEX/AUDIT-COUNCIL executions 0; MODEL_ENGAGEMENTS_CONSUMED 0;
chmod operations against the authoritative object 0; chmod operations
against the historical candidate 0; authoritative-object executions 0
(every probe failed EACCES before any successor byte; zero bytes ever
executed from the authoritative path); historical-candidate executions 0
(read+hash only); host Python installation never modified. The only
executions: the local synthetic matrix and denial/RED probes on synthetic
local fixtures, ordinary Git/GitHub publication mechanics, and local
data-only python text/hash/AST/tar tooling on non-secret bytes.

## 14. Residuals — preserved unchanged

R1 (credential-source attachment operator premise), R2 (post-verify
liveness race REDUCED NOT ELIMINATED), R3 (preserved V2/runtime evidence
strength) unchanged, with the sealed-interpreter platform-boundary
disclosure retained, and the NEW disclosed boundary of this remediation:
the mode-0000 DAC barrier is valid only in the ordinary non-root operator
context together with the governance invariant that no permission
transition is authorized until a separately authorized future activation
decision; POSIX DAC does not constrain root and cannot prevent the file
owner from a later unauthorized permission change; no root-proof or
cryptographic inode immutability is claimed.

## 15. Status held

- OPADOPT-PREP-001: **REMEDIATED_AS_CANDIDATE /
  AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK / NOT_CLOSED** (moved only
  because every remediation gate passed).
- PREARM-001: **MECHANICALLY_REMEDIATED /
  CONTROL_ROOM_ACCEPTED_CANDIDATE / OPERATIONAL_ADOPTION_PENDING /
  NOT_YET_CLOSED** — unchanged.
- HANDOFF-001 CLOSED, HANDOFF-002 CLOSED, INT-001 CLOSED, INT-002 CLOSED
  — retained at exactly their accepted strengths.
- AUCDEV-023 P1 / READY / NOT DONE. EVENT
  AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 INSTANTIATED; PATH-B
  slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT; existing Auditor-A attempt
  …-AUDITOR-A-01 remains SPENT / SINGLE-USE / NO-RETRY; NO replacement
  Auditor-A attempt exists, reserved or minted; Auditor-B authority NONE;
  FIRST_PASS_A ABSENT; MODEL_ENGAGEMENTS_USED remains 0; qualification
  NONE; installation NONE; audit verdict NONE; operational adoption NONE;
  successor NOT_ACTIVATED (still mode 0000); installed source
  `8ae33444f349ce73c1359b963722e2d16acba630` with installed-qualified
  provenance NOT ESTABLISHED; frozen external event root untouched
  append-only; historical records/handoffs NOT rewritten; prior closures
  RETAINED; the five CRED/CREDCH closures at exactly their LIMITED
  strengths.

## 16. Workspace artifacts

`/home/isa/aucdev023-pch6b-opadopt-prep001-mode-barrier-remediation-20261005-01/`
— `prepared-authority/bin/` (authoritative mode-0000 object);
`data-only/bin/` (readable NON-AUTHORITY copy, same SHA-256);
`accepted-v2/`, `deps/`, `sender/` (carried byte-exact accepted
identities, hash-pinned, sender read+hash only); `operator/` +
`integration/` (modebarrier-v2 procedure/binding + unmodified carried
contract documentation); `tests/` (ported suite + carried fixtures);
`instruments/` (creation / RED / probes / MBR matrix / port — all
NON-AUTHORITY); `evidence/` (numbered runs, honest-iteration ledger);
generated-LAST handoff archive at the workspace root (created AFTER
commit/push; see FINAL-RETURN and §17). No workspace artifact is
Git-tracked under this authority.

## 17. Publication (three authorized documentation paths, commit once, push once)

NEW `docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-PREARM-OPERATIONAL-ADOPTION-PREPARATION-MODE-BARRIER-REMEDIATION.md`
(this record; absent at base); M
`docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`; M
`docs/chatgpt-project/AUCDEV-BACKLOG.md`. No fourth tracked path; no
source, helper, test, workspace or archive Git-tracked; repository drift
preserved unstaged; the full record-only precommit gate battery ran from
scratch on the FINAL staged bytes and ALL PASSED. Self-commit identity
rule honored: this record carries the exact authorized base
`c351ddf7bb26a9803c6d794064b387e1123577db`, the staged write-tree, branch
master and this disposition; the exact resulting publication SHA and
result root tree are reported in the FINAL-RETURN, the post-push GitHub
readback and the generated-LAST handoff (created after commit/push).

## 18. NEXT — exactly one, grants nothing

INDEPENDENT CONTROL ROOM READBACK OF THE EXACT
AUCDEV023-CR-PCH6B-OPADOPT-PREP-001 MODE-BARRIER REMEDIATION CANDIDATE,
INCLUDING ZERO SOURCE-BYTE CHANGE, HISTORICAL 0600 CANDIDATE
SUPERSESSION, AUTHORITATIVE MODE-0000 CREATION-FROM-INCEPTION AND
SAME-FD HASH PROOF, NON-ROOT DIRECT-EXEC / EXPLICIT-INTERPRETER /
FILE-LOADER DENIAL, PROCEDURE/BINDING NON-AUTHORITY PATH SEPARATION,
INHERITED V2/OPADOPT REGRESSIONS, GENERATED-LAST INTEGRITY, R1/R2/R3
AND ZERO-REAL-RUNTIME CENSUS, BEFORE OPADOPT-PREP-001 OR PREARM-001
CLOSURE, SUCCESSOR ACTIVATION, OPERATIONAL ADOPTION, ANY ATTEMPT-SPECIFIC
PRELAUNCH PACKAGE, REPLACEMENT AUDITOR-A ATTEMPT AUTHORITY OR AUDITOR-B
AUTHORITY IS CONSIDERED.

Recording this NEXT grants NOTHING; no attempt authority follows
automatically; any new attempt, attempt-specific prelaunch package,
successor activation/permission transition, channel re-probe, protocol
change, teardown or real-credential use requires a NEW explicit operator
decision.

## 19. Standing prohibitions (house)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain
from an agent session absent an explicit single-use operator attempt
authority (and even then at most the ONE authorized call, never a
second); never rerun the launcher; never treat any recorded grant phrase
(including any phrase recorded here) as a new grant; never execute a real
auditor or provider/model; never open, read, hash, log, persist or stat
any real credential byte; never open the four historical sealed artifacts
(identity-only forever); never relabel or rewrite historical model
identities, runs, records, matrices, prompts or evidence workspaces
(append-only); never claim audit PASS, qualification, installation or any
authority from this publication — it grants none; never rewrite, repack,
replace or delete a historical subject archive and never publish a
corrected archive under a historical archive's filename; never repack any
historical generated-LAST handoff archive; never edit the accepted v2
remediation source or the accepted PREARM/sender bytes; never chmod the
authoritative mode-0000 prepared object (or the historical 0600 candidate)
absent separate operator authority after independent Control Room
readback; never use root to defeat the prepared-state DAC barrier; never
use a TEST-ONLY context for any future real launch; never mutate the
canonical runtime root or restage the event host after event
instantiation absent a separate explicit operator remediation authority;
never rewrite or repack the frozen external event root; never delete or
repurpose the rehearsal-derived artifacts under /srv/frevp/; never start
or reopen the event-host VM or connect to the candidate credential
channel from a remediation session; and never run privileged
mount/pivot_root/umount experiments on the operator's live host and never
automatically re-run an interrupted privileged command — privileged
GATE-W-prime boundary work belongs in the disposable-KVM environment.
