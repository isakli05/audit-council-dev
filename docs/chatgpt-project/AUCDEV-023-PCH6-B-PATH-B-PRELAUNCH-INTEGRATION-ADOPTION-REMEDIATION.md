# AUCDEV-023 PCH6-B Path-B prelaunch integration INT-001 / INT-002 remediation report

Date: 2026-10-05 (Europe/Istanbul)
Authority: AUCDEV-023-PCH6B-PRELAUNCH-INT001-INT002-REMEDIATION-20261005-01
Canonical record (Git publication path):
`docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-PRELAUNCH-INTEGRATION-ADOPTION-REMEDIATION.md`

## 0. Role and bounds of this session

This session is the bounded IMPLEMENTER of the narrow zero-model
remediation of exactly two findings recorded by the accepted independent
Control Room readback of the prelaunch integration/adoption preparation
(preparation publication `1cf7badb1b6b4a60e5f438730692502e154311b0`;
readback publication `e9deeff5aac348827256fd94162becae160cbbcc`):

- AUCDEV023-CR-PCH6B-PRELAUNCH-INT-001
  PYTHON_EXECUTION_ENVIRONMENT_NOT_MECHANICALLY_CLOSED;
- AUCDEV023-CR-PCH6B-PRELAUNCH-INT-002
  HASH_CHECKED_PATH_BYTES_NOT_ATOMICALLY_BOUND_TO_EXECUTED_BYTES.

This session is NOT the Control Room, NOT an auditor, NOT an
/audit-council executor, NOT an Auditor-A or Auditor-B executor, NOT an
attempt executor, NOT an attempt authority, NOT starting or defining the
event-host VM, NOT running virsh/QGA, NOT running send_once_v2.py or
bridge-v2.py or any channel helper, NOT creating or consuming
OPERATOR_SEND_NOW, NOT connecting to or probing the credential channel,
NOT inspecting any real credential, NOT constructing or importing
BootstrapAuthority, NOT calling run_attempt, NOT executing Claude, Codex
or any provider/model, NOT granting Auditor-A or Auditor-B authority, NOT
a qualification or installation authority. Implementation completion does
NOT close INT-001 or INT-002 (candidate strength only; independent
Control Room readback required), does NOT close PREARM-001, is NOT an
audit verdict, establishes NO frozen-target product finding and grants
NOTHING.

## 1. Exact operator authorization (verbatim)

"AUTHORIZE AUCDEV-023 narrow zero-model remediation of
AUCDEV023-CR-PCH6B-PRELAUNCH-INT-001 and
AUCDEV023-CR-PCH6B-PRELAUNCH-INT-002 only; close the Python
execution-environment binding gap and the hash-check-to-exec byte-binding
gap without operational adoption, attempt-specific prelaunch packaging,
replacement attempt minting or execution, real credential use, channel
connection, VM/QGA execution, run_attempt, model execution, or
Auditor-B authority."

This is remediation implementation authority ONLY. It is NOT operational
adoption authority; NOT attempt-specific prelaunch-package authority;
NOT replacement Auditor-A reservation/minting/execution authority; NOT
VM/QGA authority; NOT real credential authority; NOT credential-channel
authority; NOT run_attempt authority; NOT provider/model authority; NOT
Auditor-B authority; NOT qualification authority; NOT installation
authority.

## 2. Exact live bootstrap (verified before writing)

Live GitHub master == origin/master == local HEAD ==
`e9deeff5aac348827256fd94162becae160cbbcc` EXACT at bootstrap,
re-resolved EXACT again before record authoring and re-resolved again
immediately before staging and immediately before commit (ls-remote
authoritative; fetch rc 0). Root tree
`86c989db5708b80ee26198cfda91333fadc28d33` EXACT. Sole parent
`1cf7badb1b6b4a60e5f438730692502e154311b0` EXACT (single-parent
fast-forward geometry). Trust anchor
`3058868416241d394cfaaa40cc585085db486f37` ancestor rc 0. Frozen audit
target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` (tree
`2585796efd5cb6902226cfff785bb901297a15e3`) present, ancestor, UNTOUCHED,
AUDIT SUBJECT / NOT AUTHORITY. Protected trees held EXACT at base AND in
the staged write-tree: bootstrap-authority
`154975872e15d53e1706016f5bb60c83727004f0`, bootstrap-supervisor
`3056e577259ab0b0b0472f82ebc306506f3e084c`, qualification-harness
`5b8d5e5465923740470ff63ed9b8683f257a3787`, skill
`efd8c2e48edbb25795b3aacb1ce3c23fde10082a`.

The nine mandated canonical records were read at the exact base with blob
identities verified: CURRENT `1c7346dcf2483a0b7da2587d53345832ce9c3fce`,
BACKLOG `a3d858ba76c13b9c4b0c8aa04322eca22578f670`, preparation record
`58c79be39a2ec8c06c876aabecd35d815af351f2`, preparation Control Room
readback `c7df7c9c0f5208053a6b1f9c8e5e32695eed5d06`, PREARM remediation
Control Room readback `16cc958a5f4d1b67a524d80342151ee641bd9fcf`, PREARM
remediation report
`877f1b6be7073972d7b1719630912358d0faf8b6`, attempt execution report
`d210e5adc13c2bafe9f5de23970be3ac51f2f1f5`, attempt Control Room
readback `3b9a5c8fd2658c24be7a65b5d14098856d9498b8`, update protocol
`42955b85710f09579cd0fd9174d042de231d060d`. This record's path is ABSENT
at base with zero full-history path rows. Repository drift (pre-existing
smoke-fixture / smoke-fixture-103 gitlink rows and pre-existing untracked
workspaces/handoffs) preserved UNSTAGED.

## 3. Original findings being remediated (from the accepted readback)

INT-001 (HARNESS / EXECUTION-PROTOCOL DEFECT; observed source facts of
the v1 adapter `566687a4…`): the verifier subprocess carried only
capture_output and timeout with NO env= closure; NO Python isolated-mode
flag; NO PYTHONPATH/PYTHONHOME/PYTHONSTARTUP/sitecustomize/usercustomize
closure; os.execv preserved the ambient environment downstream; the
operator template showed a PATH-resolved python3 with a RELATIVE adapter
path — exact file hashes did NOT bind executed interpreter/startup
semantics.

INT-002 (HARNESS / EXECUTION-PROTOCOL DEFECT; observed source facts of
the same v1 bytes): every executed object was hashed through a pathname
reader that opens and closes, then executed LATER by PATHNAME with no
fd/inode/immutable-object continuity — a pathname replacement between
identity check and use was not mechanically excluded; existing v1 tests
covered pre-check mismatch and post-contract tamper, NOT check-to-exec
replacement within a single run.

## 4. Accepted input identities (bytes govern; verified this session)

- v1 adapter bin/prelaunch_prearm_gate_v1.py
  `566687a4d25a10a703acf880caa8b714cddd174344bf0ca62d41d950937856c4`
  (12267 B) — preserved UNMODIFIED in the prior preparation workspace
  (read-only), superseded by the v2 candidate only at candidate strength;
  NEVER rewritten.
- accepted verifier deps/verify_prearm_ready_v1.py
  `3f4438e9e76c29d2c4e0b2889c6ec0614afc07e08f5df34a03276e95a5f8c61e`
  (10778 B) — byte-exact copy re-hashed EXACT in the new workspace;
  executed in tests ONLY from its sealed snapshot; NEVER modified.
- accepted waiter deps/prearm_sender_v1.py
  `b0ec4e7ee0ce6e047372a694c58f442a73dc8586d9d8742bba588406acd5c097`
  (10878 B) — byte-exact copy re-hashed EXACT; executed ONLY inside
  disposable /tmp sandboxes to stage live readiness proofs.
- accepted minter deps/gen_prearm_challenge_v1.py
  `af8671cf578c8f6c6bfc70adeee3cddddb9cb51013307a53c33a05375c2b4e49`
  (1960 B) — byte-exact copy re-hashed EXACT; sandbox-only.
- accepted sender sender/send_once_v2.py (mode 0555)
  `1cc6e22efb1cec386d6edebcbb3f42e4feac1896c101d7c465b8dac569d6a8dd`
  (3954 B, d7 EXACT) — re-derived this session FOUR independent ways
  (sha256sum on the two preserved prior-workspace copies, python hashlib,
  plus cmp byte-equality across copies; the new workspace copy re-hashed
  EXACT), read and hashed only, NEVER executed.
- canonical interpreter: /usr/bin/python3 is a SYMLINK on this host; the
  v2 contract pins the canonical non-symlink target /usr/bin/python3.14
  (Python 3.14.7, small dynamically linked main binary); interpreter
  symlinks are REFUSED by the v2 adapter.

If any required accepted bytes had mismatched, the mandated stop was
ACCEPTED_INPUT_IDENTITY_MISMATCH; none did.

## 5. Remediation workspace and artifacts (NEW, non-secret)

Workspace: /home/isa/aucdev023-pch6b-prelaunch-int001-int002-remediation-20261005-01/
(prior preparation workspace, prior remediation workspace, historical
handoffs and the frozen event root untouched). Full artifact manifest in
SHA256SUMS (20 entries). Principal identities:

- bin/prelaunch_prearm_gate_v2.py —
  `df2dea2911f8547a79326932b788ca916a7e5a502652bc2125fad5954e455d81`
  (19695 B, mode 0755, shebang `#!/usr/bin/python3 -IS`)
- integration/PRELAUNCH-INTEGRATION-CONTRACT-v2.json —
  `e8c884177a2794a8c0de992dcd098ed1affa320659811082c57c759031b41700`
- operator/FUTURE-PRELAUNCH-INTEGRATION-TEMPLATE-v2.txt —
  `2dbfbc5eb475ac43ef1c9438eae95171e297b59624690606c15dde53f6092f69`
- tests/run_tests.py —
  `797be7abbc7e5d96353b6c63760346a6e77ea172d938aa65f03fa73c1deb274a`
- tests/fixtures/downstream_fixture_v2.py —
  `fdcaf9bc2bbf0cb190b39bad9050270be32d8274daf1762abe85b7ecaa243198`
- tests/fixtures/fake_verifier_probe_v2.py —
  `a1134a0830109cd3aa2083aa66c002c8d20b52655913b7c333e1abcc8d1471b9`
- tests/fixtures/fake_verifier_slow_success_v2.py —
  `ca2f97dff8bc2d1153ff776aed61f13c0e4a4d1fd060911e395fab8a1d7bde57`
- tests/fixtures/fake_verifier_sleeper_v2.py —
  `cfb024614bb5f9cff082b3ef39b0873e9328718458919cd9b0e6d493663d6c82`
- tests/fixtures/replacement_downstream_fixture_v2.py —
  `5c48213890df4cf67864cdf1922bcc4fde9da3fabd92a16237ba6db83de46e1c`
- tests/fixtures/seal_selftest_v2.py —
  `c468a91f7e564553a8290757a21f6e68273a8767b1b546b648c38a29d22bc370`
- v1-inherited fixtures (bytes identical to the v1 preparation set):
  sender_fixture_v1.py `9b228bda…`, fake_verifier_success_v1.py
  `6f67a906…`, fake_verifier_no_token_v1.py `891acb6f…`,
  fake_verifier_mixed_v1.py `cb12eee4…`,
  fake_verifier_double_token_v1.py `ddf1865e…`, fake_verifier_fail_v1.py
  `db6407f9…`.

## 6. INT-001 remediation architecture (as implemented)

A. ADAPTER ENTRYPOINT: the production entrypoint is DIRECT EXECUTION of
the absolute adapter path; the shebang `#!/usr/bin/python3 -IS` (combined
single argument) starts Python isolated + no-site BEFORE any adapter code
executes. The first statements of the adapter mechanically verify
sys.flags isolated/no_site/ignore_environment/no_user_site all == 1 and
fail closed rc 6 (STARTUP refusal) otherwise — before ANY contract
processing. The adapter has ZERO environment access (no environ token
anywhere in code). Host capability gates at startup: fd-bound exec
support (`os.execve in os.supports_fd`, rc 8 refusal, NO pathname
fallback) and PR_SET_DUMPABLE=0 via ctypes prctl BEFORE any execution
descriptor is created (rc 7 refusal).

B. VERIFIER CHILD: the accepted verifier is invoked EXACTLY ONCE as a
child with argv-list semantics (no shell) from its SEALED interpreter and
SEALED script snapshots: executable=/proc/self/fd/<sealed_interpreter_fd>
with pass_fds containing ONLY the two sealed verifier descriptors, argv
[display_interpreter_name, "-IS", "/proc/self/fd/<sealed_script_fd>",
<the exact eight required verifier inputs>], and env=CLEAN_ENV where
CLEAN_ENV is the fixed literal {"PATH": "/usr/bin:/bin",
"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"} — built ONLY from the literal,
never a copy of the ambient environment; PYTHONPATH/PYTHONHOME/
PYTHONSTARTUP/PYTHONUSERBASE/PYTHONINSPECT and arbitrary parent variables
are structurally not conveyable. The child additionally runs under -IS.
Bounded timeout from the contract (verifier_timeout_seconds, 5..120).

C. DOWNSTREAM TRANSITION: after admission, a single fd-bound
`os.execve(sealed_downstream_interpreter_fd, downstream_argv, CLEAN_ENV)`
(replacing v1's environment-preserving os.execv). The transition
descriptor (os.dup of the sealed downstream script fd with close-on-exec
cleared via os.set_inheritable, so the downstream interpreter can open
the sealed script through /proc/self/fd after the exec) and BOTH argv
structures are prepared at BINDING time, before the verifier runs; the
verifier child never sees the transition descriptor (the subprocess
closes every descriptor except its two passed sealed fds). After
admission only in-memory stage reporting and the execve remain.

## 7. INT-002 remediation architecture (as implemented)

PREFERRED MECHANISM — SEALED MEMFD SNAPSHOTS, exactly as tasked, for each
of the four executed objects (verifier script, verifier interpreter,
downstream script, downstream interpreter):

1. open the source pathname ONCE with O_RDONLY|O_CLOEXEC|O_NOFOLLOW
   (plus O_NONBLOCK so special files cannot hang the open);
2. fstat the opened descriptor: regular file only (S_ISREG), else refuse
   rc 3; size/dev/ino recorded as NON-AUTHORITY diagnostic evidence;
   unsupported/special objects rejected;
3. read the bytes from THAT opened descriptor only;
4. SHA-256 those exact bytes and compare against the expected pin (any
   mismatch refuses rc 3 with the verifier NEVER invoked);
5. create a fresh memfd (os.memfd_create with MFD_CLOEXEC |
   MFD_ALLOW_SEALING);
6. write those exact verified bytes to the memfd;
7. set mode 0555 (fchmod);
8. seal with F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL
   (REQUIRED_SEALS 0xF) via F_ADD_SEALS;
9. confirm the required seals mechanically via F_GET_SEALS (refuse rc 3
   if incomplete);
10. re-hash the SEALED memfd bytes and require exact equality with the
    expected SHA-256 (refuse rc 3 otherwise);
11. from this point onward the original pathname is NEVER opened,
    re-hashed or resolved for execution — it is identity-source evidence
    only. Every execution goes through the sealed objects: the verifier
    child via executable=/proc/self/fd + argv script /proc/self/fd +
    pass_fds, and the downstream via the fd-bound execve with the
    script's /proc/self/fd path in argv.

The single no-follow open also implements the v2 PATH/CONTRACT hardening:
interpreter SYMLINKS are refused (the v1 "interpreter symlink acceptable"
behavior is gone; the contract must pin the canonical regular-file
target), as are symlink scripts and special/non-regular sources.
Memfds and their descriptors are EPHEMERAL process objects: never
serialized into any permit/grant/authority/admission artifact (the
adapter writes ZERO files in every outcome), and they die with the
process. NON-DUMPABLE hardening (PR_SET_DUMPABLE=0 before creating any
execution descriptor) is defense-in-depth for held descriptors and does
NOT replace sealed-byte binding.

## 8. Control-flow invariants (preserved + new ordering)

Preserved exactly from the accepted v1 logic: the accepted verifier is
mandatory and unbypassable; admission requires rc == 0 AND exactly ONE
MECHANICAL_PREARM_READY=VERIFIED in stdout AND zero
MECHANICAL_PREARM_READY=NOT_VERIFIED AND zero REASON failure lines AND
zero admission tokens in stderr (evaluate_admission is byte-for-byte the
v1 logic); textual ARMED has ZERO admission effect (no such input
exists); exactly ONE downstream transition; zero retry; zero fallback;
zero alternate downstream; no reusable permit (zero files written).

New v2 ordering (AST-proven by the test matrix): (1) startup isolation
verification precedes everything; (2) strict v2 contract parse (exact
20-key set, forbidden-key guard, TEST-ONLY context regex
^AUCDEV023-TEST-ONLY-[A-Z0-9-]{8,96}$ mechanically preventing
operational adoption of this candidate, hex64 pins, argv_tail 0..8,
timeout 5..120); (3) all four sealed snapshots created, pinned,
F_GET_SEALS-confirmed and sealed-re-hashed BEFORE the verifier is
invoked; (4) exact sealed identities established; (5) the accepted
verifier invoked from the sealed objects under CLEAN_ENV + -IS; (6)
admission evaluated; (7) if and only if admitted, the immediate fd-bound
execve transition into the sealed downstream objects under CLEAN_ENV.
After the last snapshot statement NO executed-object contract key is
referenced again (AST-verified: zero executed-object-key subscripts after
the binding stage; only locals, /proc/self/fd paths and the sealed
descriptors remain); after verifier PASS no pathname re-open, no
re-hash, no path resolution for an executable, no human acknowledgement,
no sleep, no network operation, no filesystem discovery, no new
snapshot, no credential operation, no VM inspection and no hook — only
in-memory stage prints and the fd-bound execve.

## 9. Test matrix (RED-first), race/adversarial and hostile-env evidence

The 42-case deterministic local-only harness was written BEFORE the
implementation and preserved RED evidence with the adapter absent
(evidence/tests/run-001-red.txt: 0/42). Final from-scratch run 42/42
(evidence/tests/run-004-final.txt, including the embedded repeatability
self-run 41/41 from a fresh sandbox) plus an independent repeatability
re-run 42/42 (evidence/tests/run-005-repeatability.txt). Standalone
source/AST invariant scan OVERALL=PASS
(evidence/source-invariant-scan.txt). Host capability probe (memfd
sealing, write-after-seal EPERM, sealed-interpreter execution with
stdlib discovery, fd-form execve, -IS shebang) OVERALL=PASS
(evidence/probe-out.txt; the probe script is preserved as
tests/fixtures/seal_selftest_v2.py and re-executed by test 13).

Coverage mapped to the mandated list 01..42: startup refusal without
isolation (01); direct entrypoint establishes isolated=1/no_site=1/
ignore_environment=1/no_user_site=1 (02); hostile PYTHONPATH module
injection (03); hostile sitecustomize canary (04); hostile usercustomize
canaries PYTHONPATH + PYTHONUSERBASE (05); hostile PYTHONHOME cannot
redirect the verifier interpreter environment (06); downstream sees
EXACTLY the {PATH,LANG,LC_ALL} allowlist with no attacker variable (07);
accepted verifier exact bytes required, tampered/wrong-pin refused
pre-invocation (08); verifier launched via sealed fd objects (09) with
in-child proof exe=/memfd:... argv0=/proc/self/fd/... (10); downstream
script from its sealed object (11); downstream interpreter from its
sealed object (12); seals present and verified, 4x seals=0xf
rehash=match + seal selftest (13); verifier pathname REPLACED after
snapshot before invocation — original sealed bytes still govern (14);
verifier pathname MODIFIED IN-PLACE post-snapshot (15); downstream
pathname replaced WHILE the verifier runs (16); downstream mutated
in-place mid-verify (17); verifier-interpreter pathname replaced after
snapshot (18); downstream-interpreter pathname replaced after snapshot
(19); ALL FOUR source paths DELETED post-snapshot with sealed execution
identity-correct (20); wrong source hash pre-snapshot (21); wrong
interpreter hash pre-snapshot (22); symlink sources refused including
interpreter symlinks (23); FIFO/special source refused fast (24);
malformed contract classes (25); verifier NOT_VERIFIED => downstream
absent, real and fake (26); verifier timeout => downstream absent with
duration evidence (27); textual ARMED zero admission effect (28); no
os.execv (29); fd-capable os.execve + explicit CLEAN_ENV (30); no
pathname resolution after binding (31); no reusable permit artifact
(32); exactly one verifier invocation path (33); exactly one downstream
transition path (34); no retry/fallback/alternate (35); no
socket/network (36); no credential logic (37); no VM/QGA (38); no
BootstrapAuthority/run_attempt (39); no attempt id/reservation/mint
(40); same-PID transition preserved (41); full-suite repeatability from
a fresh sandbox (42).

Race synchronization is deterministic and adds NO production hook: the
harness reads the adapter's stage diagnostics line-by-line, SIGSTOPs the
adapter upon observing the non-authority SNAPSHOTS_READY diagnostic
(tests 14/15/20) or the VERIFIER_INVOKING diagnostic immediately before
the child launch (tests 16-19, where a pinned 3-second test-only slow
verifier guarantees the mutation window overlaps the verifier's actual
execution), applies the path replacement / in-place mutation / deletion
to SANDBOX COPIES only (the host system interpreter is never touched),
then SIGCONTs. Direction-sensitive assertions discriminate: the
replacement objects would produce the OPPOSITE admission or a
REPLACED_DOWNSTREAM_RAN marker if the adapter executed pathnames; the
sealed originals govern instead.

Hostile-environment tests (03-07) launch the adapter under deliberately
hostile ambient values (PYTHONPATH with sitecustomize.py, usercustomize.py
and a rogue module; PYTHONUSERBASE with a site-packages usercustomize;
PYTHONHOME pointing at a nonexistent prefix; PYTHONSTARTUP canary;
PYTHONINSPECT=1; an attacker variable) with canary files proving ZERO
execution of any customization code, identical admission behavior to a
clean environment, and the downstream environment equal to the exact
three-key allowlist.

## 10. Acceptance criteria results

INT001-R-01 PASS — adapter startup isolated before any candidate Python
code executes (shebang -IS; tests 01/02/03-06).
INT001-R-02 PASS — adapter mechanically verifies the required Python
flags (test 01 refuses rc 6 without them; test 02 observes all four
flags == 1).
INT001-R-03 PASS — verifier executes with -IS under the explicit clean
environment (tests 06/09/10; AST scan enforces env=CLEAN_ENV + "-IS").
INT001-R-04 PASS — downstream executes under the explicit clean
environment (test 07: env == {PATH,LANG,LC_ALL} exactly; AST scan
enforces the execve third argument is CLEAN_ENV).
INT001-R-05 PASS — hostile PYTHON* and test-only customization injection
cannot affect semantics (tests 03/04/05: zero canaries, identical
admission).
INT001-R-06 PASS — operator template uses the absolute, mechanically
isolated direct entrypoint and contains no bare PATH-resolved
`python3 relative/path` (template v2; the only invocation form shown is
the absolute direct-exec path; INT001-R-06 also verified by the battery
gate over the template bytes).
INT002-R-01 PASS — each executable/script source opened once with
no-follow semantics and verified from that fd (AST: single os.open site
inside sealed_snapshot; test 23).
INT002-R-02 PASS — verified bytes copied into sealed immutable execution
objects (adapter mechanism; test 13 evidence lines).
INT002-R-03 PASS — required seals mechanically confirmed (F_GET_SEALS
mask 0xf asserted on all four objects; test 13 + seal selftest).
INT002-R-04 PASS — verifier executed bytes are the sealed verified bytes
(tests 10/14/15).
INT002-R-05 PASS — verifier-interpreter executed bytes are the sealed
verified bytes (tests 10/18).
INT002-R-06 PASS — downstream executed bytes are the sealed verified
bytes (tests 11/16/17).
INT002-R-07 PASS — downstream-interpreter executed bytes are the sealed
verified bytes (tests 12/19).
INT002-R-08 PASS — no executable original pathname re-resolved after
snapshot binding (AST zero executed-object-key references after the
binding stage; tests 09/31).
INT002-R-09 PASS — rename/path-swap/in-place-modification after snapshot
cannot change executed bytes (tests 14-19; deletion test 20).
INT002-R-10 PASS — unsupported fd/memfd execution fails closed with no
pathname fallback (startup rc 8 gate; os.execv banned; AST test 29).

HELD-R-01 PASS — PREARM verifier admission semantics unchanged (v1
evaluate_admission logic preserved verbatim; tests 08/26/28 and the full
session-staged matrix).
HELD-R-02 PASS — no reusable permit artifact (test 32: zero adapter
files on refusal, only fixture reached-evidence on success, empty cwd,
no marker-like names).
HELD-R-03 PASS — no retry/fallback (AST: no loops in the transition
function, single Try with refuse-only handler; test 35).
HELD-R-04 PASS — R1 credential-source operator premise unchanged (the
gate still does NOT establish fd 0 identity; no real credential used,
opened, stat'ed or hashed).
HELD-R-05 PASS — R2 post-verification liveness residual reduced, not
eliminated; NO pidfd-style waiter coupling claimed (the transition
descriptor and argv are prepared pre-verifier; only prints + execve
remain after PASS).
HELD-R-06 PASS — R3 preserved V2/runtime evidence strength unchanged (no
VM started, no fresh guest rehash; bridge-v2/channel-v2 stand at
preserved hash-bound strength).
HELD-R-07 PASS — no operational adoption occurs (additionally made
STRUCTURAL: the contract validation refuses every non-TEST-ONLY context
id, so this candidate cannot express a production binding).
HELD-R-08 PASS — no replacement attempt created/reserved/minted (zero
attempt-id constructs; test 40; TEST-ONLY contexts only).
HELD-R-09 PASS — no real credential/channel/VM/QGA/run_attempt/provider
activity (zero-execution census below; AST/token scans).

## 11. Honest session iteration (no erasure; every failed observation
disclosed; no failed observation rewritten as PASS without a corrected
re-derivation on IDENTICAL state)

- P-1 (pre-adapter probe, /tmp scratch): the first capability-probe run
  reported two FAILs — an exe-prefix assertion mis-encoding (/memfd:
  targets carry a leading slash and "(deleted)" suffix) and a REAL
  mechanism finding: Python's os.dup returns a close-on-exec descriptor
  (PEP 446), so the downstream script fd died at execve. Both corrected
  (assertion calibrated; os.set_inheritable added) and the probe re-run
  from scratch to PROBE_OVERALL=PASS (evidence/probe-out.txt holds the
  corrected PASS output; the first failing output was overwritten in the
  /tmp scratch by the tee re-run — disclosed here, no evidence file
  erased).
- I-1: deliberate RED-first 0/42 with the implementation absent
  (evidence/tests/run-001-red.txt).
- T-1: first implementation run 20/41 — ONE adapter defect: the
  downstream argv referenced the close-on-exec sealed script descriptor
  instead of its inheritable duplication, so the downstream interpreter
  could not open /proc/self/fd/<script> ("can't open file
  '/proc/self/fd/6'"). Corrected by preparing the transition descriptor
  (dup + set_inheritable) at BINDING time and referencing IT in the
  downstream argv — a strictly STRONGER ordering (less work after
  admission); full suite re-ran (terminal-observed; the harness had
  --skip-self-repeat for iteration, no evidence file written for this
  intermediate — disclosed).
- T-2: second run 39/41 — two HARNESS INSTRUMENT defects, not adapter
  defects: the test-13 snapshot-line filter matched the SNAPSHOTS_READY
  summary line as a fifth role line (prefix collision), and the
  launcher-shape structural scan did not accept the conditional
  [interpreter|adapter] argv form / the PY_CANON absolute-path constant.
  Both calibrated; corrected suite re-ran from scratch.
- T-3 (pre-first-GREEN calibration, terminal-only): the CLEAN_ENV key
  scan used double-quote patterns while ast.unparse emits single quotes
  (fixed before any GREEN observation); the dup-ordering scan was
  re-anchored from "between verifier and exec" to the stronger "after
  the last snapshot bind and before the exec" when the dup moved to
  binding time.
- Final evidence runs: run-004-final 42/42 and run-005-repeatability
  42/42 from scratch (both file-preserved); source-invariant scan
  OVERALL=PASS (file-preserved).

## 12. Zero-execution census

VM_RUNS 0; EVENT_HOST_DEFINES 0; QGA/virsh invocations 0;
CHANNEL_CONNECTIONS 0; CHANNEL_REPROBES 0; CONNECT_ATTEMPTS 0;
SOCKET_PROBES 0; OPERATOR_SEND_NOW created/consumed 0 (test sandboxes
use clearly-named sandbox paths only); send_once_v2 invocations 0 (read +
hashed only, four derivations); bridge-v2 invocations 0; V2/frozen
mutations 0; REAL_CREDENTIAL stats/opens/reads/hashes/transmissions 0;
BOOTSTRAP_AUTHORITY imports/constructions 0; RUN_ATTEMPT_CALLS 0; attempt
accounting records 0; report sinks 0; attempt ids created 0;
CLAUDE/CODEX/AUDIT-COUNCIL executions 0; provider/model/frontier requests
0; MODEL_ENGAGEMENTS_CONSUMED 0; FIRST_PASS artifacts 0; QUALIFICATION
NONE; INSTALLATION NONE. The only executions: the candidate v2 adapter,
the byte-exact accepted helper copies (waiter/verifier/minter — local,
non-secret, zero-network by their proven invariants; the verifier ONLY
via its sealed snapshot), synthetic inert fixtures, the seal selftest and
the harness inside disposable /tmp sandboxes, and the ordinary
Git/GitHub publication mechanics. The host system Python installation
was never modified (interpreter-swap tests use sandbox COPIES; the
canonical /usr/bin/python3.14 is only read and hashed).

## 13. Status, residuals and governance held

STATUS (candidate strength, at most as tasked):
INT_001_REMEDIATED_AS_CANDIDATE / INT_002_REMEDIATED_AS_CANDIDATE /
PYTHON_EXECUTION_ENVIRONMENT_MECHANICALLY_CLOSED_IN_CANDIDATE /
SEALED_IMMUTABLE_CHECK_TO_EXEC_BINDING_ESTABLISHED_IN_CANDIDATE /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK / NO_OPERATIONAL_ADOPTION /
NO_ATTEMPT_AUTHORITY / AUDITOR_B_AUTHORITY_NONE / AUDIT_VERDICT_NONE /
QUALIFICATION_NONE / INSTALLATION_NONE.

INT-001 = REMEDIATED_AS_CANDIDATE / AWAITING_INDEPENDENT_CONTROL_ROOM_
READBACK / NOT_CLOSED. INT-002 = REMEDIATED_AS_CANDIDATE /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK / NOT_CLOSED. PREARM-001 =
MECHANICALLY_REMEDIATED / CONTROL_ROOM_ACCEPTED_CANDIDATE /
OPERATIONAL_ADOPTION_PENDING / NOT_YET_CLOSED (unchanged).

RESIDUALS held: R1 credential-source attachment operator premise
(fd 0 identity remains an operator precondition; not established by the
gate); R2 post-verify liveness race (reduced — argv and transition
descriptor prepared pre-verifier, only prints + one execve after PASS —
but atomic pidfd-style coupling does NOT exist and is NOT claimed); R3
preserved V2/runtime evidence strength. Candidate scope note (disclosed,
applies to the whole sealed-execution class): the sealed interpreter
object binds the python executable BYTES — the small dynamically linked
main binary; its shared-library dependencies, the dynamic linker and the
kernel are ambient to any fd-exec mechanism of this class and are
outside the sealed-object binding. Snapshot dev/ino/size metadata is
non-authority diagnostics only. The verifier itself runs byte-exact
accepted bytes with UNCHANGED semantics; its permission-conditional
/proc fdinfo check remains SKIPPED_UNREADABLE for a non-dumpable waiter.

GOVERNANCE held: EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01
INSTANTIATED; PATH-B slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT;
AUCDEV-023 P1 / READY / NOT DONE; existing Auditor-A attempt
…-AUDITOR-A-01 remains SPENT / SINGLE-USE / NO-RETRY; NO replacement
Auditor-A attempt exists, reserved or minted; Auditor-B authority NONE;
MODEL_ENGAGEMENTS_USED remains 0 for the settled attempt; FIRST_PASS_A
ABSENT; frozen target AUDIT SUBJECT / NOT AUTHORITY; PCH6-B-SD-002 /
PCH6-CR-BSD-001 AWAITING FRESH INDEPENDENT AUDIT / NOT CLOSED;
PCH6-B-SD-001 RETAINED / OPEN; the five CRED/CREDCH closures at exactly
their LIMITED strengths; INDEPENDENT_AUDITOR_PROVENANCE_GATE
NOT_SATISFIED; installed Audit Council NOT AUTHORITY FOR THIS EVENT;
NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE DISCLOSED RESIDUAL; STAGING-RB-001
/ CREDCH-RB-EV-001 preserved; frozen external event root untouched
append-only; historical records/handoffs NOT rewritten; prior closures
RETAINED; no audit execution; no audit PASS.

## 14. NEXT — exactly one, grants nothing

INDEPENDENT CONTROL ROOM READBACK OF THE EXACT INT-001 / INT-002
PRELAUNCH-INTEGRATION REMEDIATION CANDIDATE, INCLUDING ADAPTER-STARTUP
ISOLATION, CLEAN PYTHON EXECUTION ENVIRONMENT, SEALED IMMUTABLE
EXECUTION-OBJECT BINDING, CHECK-TO-EXEC PATH-SWAP RESISTANCE, ACCEPTED
VERIFIER SEMANTICS, R1/R2/R3 RESIDUALS, ADVERSARIAL LOCAL-ONLY TEST
MATRIX, GENERATED-LAST HANDOFF AND ZERO-EXECUTION CENSUS, BEFORE ANY
OPERATIONAL ADOPTION, ATTEMPT-SPECIFIC PRELAUNCH PACKAGE, REPLACEMENT
AUDITOR-A ATTEMPT AUTHORITY OR AUDITOR-B AUTHORITY IS CONSIDERED.

Recording this NEXT grants NOTHING; no attempt authority follows
automatically; Auditor-B authority remains NONE; no replacement
Auditor-A attempt exists or is authorized; any new attempt,
attempt-specific prelaunch package, channel re-probe, protocol change,
teardown or real-credential use requires a NEW explicit operator
decision.

## 15. Disposition block

AUCDEV_023_PCH6B_PRELAUNCH_INTEGRATION_INT001_INT002_REMEDIATION =
INT_001_REMEDIATED_AS_CANDIDATE /
INT_002_REMEDIATED_AS_CANDIDATE /
PYTHON_EXECUTION_ENVIRONMENT_MECHANICALLY_CLOSED_IN_CANDIDATE /
SEALED_IMMUTABLE_CHECK_TO_EXEC_BINDING_ESTABLISHED_IN_CANDIDATE /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK /
NO_OPERATIONAL_ADOPTION /
NO_ATTEMPT_AUTHORITY /
AUDITOR_B_AUTHORITY_NONE /
AUDIT_VERDICT_NONE /
QUALIFICATION_NONE /
INSTALLATION_NONE

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
