# AUCDEV-023 PCH6-B Path-B prelaunch integration INT-001/INT-002 remediation — independent Control Room readback

Publication authority (record-only): `AUCDEV-023-PCH6B-730D2B29-PATHB-INT001-INT002-REMEDIATION-CRRB-PUB-20261005-01`
Date: 2026-10-05 (Europe/Istanbul)
Canonical record: `docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-PRELAUNCH-INTEGRATION-ADOPTION-REMEDIATION-CONTROL-ROOM-READBACK.md`

## Role

This session is the bounded RECORD-ONLY publisher of the ALREADY-completed
independent Control Room readback of the AUCDEV-023 PCH6-B INT-001 / INT-002
remediation candidate (remediation publication
`67ad6d3e0650ee78b7d1acf1451f479f5833329d`). It is NOT the substantive Control
Room decision-maker of the readback (already completed), NOT an implementer,
NOT an auditor, NOT an attempt executor, NOT an `/audit-council` executor, NOT
an Auditor-A or Auditor-B attempt executor, NOT an attempt authority, NOT a
provider/model/frontier executor, NOT starting or defining the event-host VM,
NOT running virsh/QGA, NOT running `send_once_v2.py` or `bridge-v2.py` or any
channel helper, NOT creating or consuming `OPERATOR_SEND_NOW`, NOT connecting
to or probing the credential channel, NOT inspecting any real credential, NOT
constructing or importing BootstrapAuthority, NOT calling `run_attempt`, NOT
executing Claude, Codex or any provider/model, NOT granting Auditor-A or
Auditor-B authority, NOT a qualification or installation authority.

THIS PUBLICATION GRANTS NOTHING. The disposition is NOT an audit verdict,
establishes NO frozen-target product finding, closes NO finding beyond the
statuses recorded below and grants NO attempt authority.

## Exact live bootstrap (verified this session)

- Live GitHub `master` == `origin/master` == local HEAD ==
  `67ad6d3e0650ee78b7d1acf1451f479f5833329d` EXACT at bootstrap
  (`git ls-remote` authoritative; `git fetch` rc 0), re-resolved EXACT
  immediately before staging and again immediately before commit.
- Root tree `633e6245bd4359d9c4cb906d328c66a00bb4d4ce` EXACT; sole parent
  `e9deeff5aac348827256fd94162becae160cbbcc` EXACT (single-parent
  fast-forward geometry).
- Trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor rc 0.
- Frozen audit target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed`
  (tree `2585796efd5cb6902226cfff785bb901297a15e3`) present, ancestor,
  UNTOUCHED, AUDIT SUBJECT / NOT AUTHORITY.
- Protected trees held EXACT at base: `bootstrap-authority`
  `154975872e15d53e1706016f5bb60c83727004f0`, `bootstrap-supervisor`
  `3056e577259ab0b0b0472f82ebc306506f3e084c`, `qualification-harness`
  `5b8d5e5465923740470ff63ed9b8683f257a3787`, `skill`
  `efd8c2e48edbb25795b3aacb1ce3c23fde10082a`.
- The six mandated canonical records read at the exact base with blob
  identities verified: CURRENT `64de57c3099daf2f48fef660fd3d66c885fd2f78`,
  BACKLOG `744f811723997b9a4166c98eb0eba5ba0bef9969`, remediation record
  `6a6850fb9547bfc8061ec186548facd1935ef8a2`, prior preparation Control Room
  readback `c7df7c9c0f5208053a6b1f9c8e5e32695eed5d06`, prior prearm
  remediation Control Room readback `16cc958a5f4d1b67a524d80342151ee641bd9fcf`,
  update protocol `42955b85710f09579cd0fd9174d042de231d060d`. CURRENT/BACKLOG
  working copies verified byte-identical to the base blobs before editing.
- This record's path ABSENT at base with zero full-history path rows.
- Repository drift (pre-existing `smoke-fixture` / `smoke-fixture-103` gitlink
  rows and pre-existing untracked workspaces/handoffs) preserved UNSTAGED.

## Readback subject geometry — PASS

Remediation publication `67ad6d3` over `e9deeff` is exactly ONE fast-forward
commit changing exactly three tracked paths (NEW remediation record
`6a6850fb`; M CURRENT -> `64de57c3`; M BACKLOG -> `744f8117`), no protected
tree touched, frozen target unchanged — `git diff-tree --no-commit-id
--name-status -r` re-derived EXACT this session.
PUBLICATION_GEOMETRY_PASS.

Readback subject identities (bytes govern; re-derived EXACT this session from
the SHA-verified subject archive): candidate v2 adapter
`bin/prelaunch_prearm_gate_v2.py` — SHA-256
`df2dea2911f8547a79326932b788ca916a7e5a502652bc2125fad5954e455d81`, 19695
bytes; accepted verifier `deps/verify_prearm_ready_v1.py` — SHA-256
`3f4438e9e76c29d2c4e0b2889c6ec0614afc07e08f5df34a03276e95a5f8c61e`, 10778
bytes (byte-exact to the ACCEPTED prearm verifier identity).

## Independent source remediation findings — SUPPORTED

All findings re-derived this session DATA-ONLY from the SHA-verified archived
adapter bytes (hashing, AST parsing, text scanning; NO execution). The 39-gate
static source review ran to OVERALL=PASS.

1. Adapter bytes SHA-256 EXACT:
   `df2dea2911f8547a79326932b788ca916a7e5a502652bc2125fad5954e455d81`,
   19695 bytes (verified twice: archive member + preserved implementation
   workspace copy).
2. Shebang bytes EXACT: `#!/usr/bin/python3 -IS`.
3. Startup code mechanically requires `isolated == 1`, `no_site == 1`,
   `ignore_environment == 1`, `no_user_site == 1` (tuple comparison against
   `(1, 1, 1, 1)`, refusing with rc 6), BEFORE any contract processing; the
   fd-exec capability gate (`os.execve not in os.supports_fd` -> rc 8, no
   pathname fallback) and `PR_SET_DUMPABLE=0` via ctypes prctl (rc 7) also
   run before any execution descriptor is created.
4. `CLEAN_ENV` is the EXACT literal
   `{"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}`;
   ZERO `os.environ` / `getenv` access anywhere in the adapter.
5. Exactly ONE `subprocess.run` verifier site exists, with
   `executable="/proc/self/fd/<sealed interpreter fd>"`, `env=CLEAN_ENV`,
   `capture_output=True`, `timeout=<contract>`, `pass_fds=(v_ifd, v_sfd)`
   (only the two sealed verifier descriptors).
6. Verifier argv includes `-IS` (argv[1]) and the sealed script path
   `/proc/self/fd/<sealed script fd>`.
7. Exactly ONE `os.execve` downstream site exists;
   `os.execv` sites = 0.
8. Each of the FOUR executed objects is created through the
   `sealed_snapshot` mechanism with exact roles: `verifier_interpreter`,
   `verifier_script`, `downstream_interpreter`, `downstream_script`.
9. `sealed_snapshot`: opens the source with
   `O_RDONLY | O_CLOEXEC | O_NOFOLLOW | O_NONBLOCK`; `os.fstat` requires a
   regular file (`stat.S_ISREG`); reads the whole content from THAT opened
   descriptor; compares the SHA-256 against the expected pin (refuse rc 3,
   verifier NEVER invoked); creates a fresh
   `os.memfd_create(..., MFD_CLOEXEC | MFD_ALLOW_SEALING)`; writes the
   verified bytes; `fchmod 0555`; applies
   `F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE` via F_ADD_SEALS
   (REQUIRED_SEALS == 0xf); verifies the seals through F_GET_SEALS; re-hashes
   the SEALED bytes and requires exact equality.
10. After binding, verifier execution uses `/proc/self/fd` sealed objects
    (both the executable and the script argv entry); NO executed-object
    contract key is referenced after the last snapshot statement (AST proof;
    only non-executed contract inputs remain).
11. Downstream uses fd-form `os.execve(d_ifd, downstream_argv, CLEAN_ENV)` —
    the interpreter is the sealed descriptor and CLEAN_ENV is the explicit
    literal third argument.
12. No source-level retry/fallback/alternate downstream path was found:
    zero loop constructs in the transition function, exactly two Try
    statements (verifier invocation + the execve itself), zero other
    exec/spawn/fork/system/popen sites, zero banned constructs (no
    eval/exec/`compile`/`__import__` calls; the two `re.compile` sites are
    regex constants), import allowlist exactly
    argparse/ctypes/fcntl/hashlib/json/os/re/stat/subprocess/sys.
13. The accepted PREARM admission semantics remain EXACT: rc == 0 AND
    exactly one `MECHANICAL_PREARM_READY=VERIFIED` in stdout AND zero
    `MECHANICAL_PREARM_READY=NOT_VERIFIED` AND zero `REASON` failure lines
    AND zero admission tokens in stderr (`evaluate_admission` is the only
    admission decider).
14. No source-level contradiction was found that reopens INT-001 or INT-002
    remediation mechanics (compositional verdict over findings 1-13 plus the
    structural scans; the credential term appears only inside the
    FORBIDDEN_KEY_TOKENS guard tuple and the module docstring;
    zero `run_attempt` / `BootstrapAuthority` tokens).

INT001_REMEDIATION_MECHANICS_SUBSTANTIALLY_SUPPORTED.
INT002_REMEDIATION_MECHANICS_SUBSTANTIALLY_SUPPORTED.

## Test evidence classification

The archived runtime evidence states: RED `0/42` (run-001-red), final
`42/42` (run-004-final), repeatability `42/42` (run-005-repeatability). The
final and repeatability outputs are hash-bound archive payloads and their
contents were independently READ this session (SUMMARY lines verified:
`pass=0 total=42` / `pass=42 total=42`).

Classification (exactly as mandated):

HASH-BOUND PRESERVED IMPLEMENTATION RUNTIME EVIDENCE /
SOURCE-CORROBORATED /
NOT INDEPENDENTLY RE-EXECUTED BY CONTROL ROOM.

The Control Room did NOT re-execute the test suite and this publication
claims NO re-execution.

Non-blocking evidence observation (disclosed, append-only): the archived
`evidence/tests/run-005-repeatability.txt` is BYTE-IDENTICAL to
`evidence/tests/run-004-final.txt` (cmp rc 0; both 5441 bytes; manifest rows
`d28bf805…` for both). The repeatability claim therefore rests on a
byte-identical copy rather than a distinct output artifact; this does not
weaken the classification above (which already disclaims Control Room
re-execution) and does NOT constitute a new finding.
PRESERVED_RUNTIME_EVIDENCE_SOURCE_CORROBORATED.

## Generated-LAST subject archive integrity — NOT full pass

Subject: `AUCDEV-023-PCH6B-PRELAUNCH-INT001-INT002-REMEDIATION-HANDOFF-20261005-01.tar.gz`
Outer size 1176728 EXACT; outer SHA-256
`016091a98cf66403c879b7d6b84fe65fcb77fc3e5de84a9e87acfc4e994a7400` EXACT
(two independent derivations: sha256sum AND python hashlib).

Independent census: 49 total members = 37 regular + 12 directories +
0 symlinks + 0 hardlinks + 0 special; 0 duplicate paths; 0 unsafe/traversal
paths; one common top-level prefix; exactly one SHA256SUMS.

- 36 regular payloads exist OTHER THAN SHA256SUMS.
- The checksum manifest contains 35 VALID SHA-256 rows (plus one `#` comment
  header line).
- All 35 listed payloads independently rehash PASS: 35/35 PASS.
  GENERATED_LAST_LISTED_PAYLOAD_REHASH_PASS.
- EXACT payload-set equality FAILS: the unlisted regular payload is
  `README.md` (3097 bytes, SHA-256
  `c2bd97a6d8dcd47ef37c53eb1a971344440bd92a5299708020bfdebae197921a`;
  payload-set minus manifest-set = {README.md}; manifest-set minus
  payload-set = {}).
- Therefore GENERATED_LAST_FULL_PAYLOAD_COVERAGE = FAIL, and the
  implementation report's / user return's claim of payload-set equality in
  both directions is NOT supported by the actual archive.

## FINDING HANDOFF-001

- ID: `AUCDEV023-CR-PCH6B-PRELAUNCH-REM-HANDOFF-001`
- Name: GENERATED_LAST_MANIFEST_PAYLOAD_SET_INCOMPLETE
- Classification: HARNESS / PROTOCOL DEFECT + COMPLETENESS LIMITATION
- Support: OBSERVED FACT
- Disposition: OPEN /
  BLOCKING_FULL_CONTROL_ROOM_READBACK_COMPLETENESS /
  NOT_AN_ADAPTER_SOURCE_DEFECT
- Reason: the mandatory generated-LAST invariant requires every regular
  payload other than the checksum manifest itself to be listed exactly once.
  36 such payloads exist; only 35 are listed; README.md is omitted.
- Direction: do NOT rewrite or replace the historical archive.

## Mode fidelity

Independent tar-header inspection shows ALL 37 regular subject-archive
members carry tar mode 0644, including:

- `bin/prelaunch_prearm_gate_v2.py`: tar mode = 0644
- `sender/send_once_v2.py`: tar mode = 0644

The canonical remediation record / preserved runtime evidence reports the
implementation-workspace adapter as mode 0755 and the sender as mode 0555
(the archived FINAL-RETURN states both; the PRESERVED implementation
workspace independently observes 0755 / 0555 — non-authority corroboration,
NOT derived from the generated-LAST). This publication does NOT infer that
the implementation workspace itself was mode 0644. What IS established is
that the generated-LAST does NOT preserve the reported executable/read-only
mode metadata. This matters because the operator template's entrypoint rule
(INT001-R-01 / absolute isolated direct entrypoint via the adapter shebang)
relies on the adapter being directly executable. The archived 42/42 runtime
evidence includes a test whose code directly executes the adapter path and
reports successful isolated startup; that remains HASH-BOUND IMPLEMENTATION
RUNTIME EVIDENCE, NOT an independently re-executed Control Room observation.

## FINDING HANDOFF-002

- ID: `AUCDEV023-CR-PCH6B-PRELAUNCH-REM-HANDOFF-002`
- Name: GENERATED_LAST_EXECUTABLE_MODE_FIDELITY_NOT_PRESERVED
- Classification: HARNESS / HANDOFF-PACKAGING DEFECT + COMPLETENESS LIMITATION
- Support: OBSERVED TAR-METADATA FACT + EVIDENCE-STRENGTH INFERENCE
- Disposition: OPEN /
  BLOCKING_FULL_CONTROL_ROOM_READBACK_COMPLETENESS /
  NOT_AN_ADAPTER_SOURCE_DEFECT
- Constraint: do NOT claim the workspace executable mode as independently
  verified FROM the generated-LAST.

The new HANDOFF-001 / HANDOFF-002 findings concern evidence
packaging/completeness. They do NOT constitute a new adapter-source defect
and do NOT discard the valid v2 remediation evidence.

## Archived Git copies — PASS

Independently reproduced Git blob identities from the subject archive (git
blob sha1 recomputed from archived bytes AND direct byte equality against
live Git at `67ad6d3`):

- canonical remediation record: `6a6850fb9547bfc8061ec186548facd1935ef8a2`
- CURRENT: `64de57c3099daf2f48fef660fd3d66c885fd2f78`
- BACKLOG: `744f811723997b9a4166c98eb0eba5ba0bef9969`

All match live Git at the publication SHA EXACTLY.

## INT-001 / INT-002 status

Neither finding is closed by this readback:

- INT-001 = `AUCDEV023-CR-PCH6B-PRELAUNCH-INT-001`:
  REMEDIATED_AS_CANDIDATE /
  SOURCE_MECHANICS_SUPPORTED_BY_CONTROL_ROOM_READBACK /
  HANDOFF_COMPLETENESS_CORRECTION_PENDING /
  NOT_CLOSED
- INT-002 = `AUCDEV023-CR-PCH6B-PRELAUNCH-INT-002`:
  REMEDIATED_AS_CANDIDATE /
  SOURCE_MECHANICS_SUPPORTED_BY_CONTROL_ROOM_READBACK /
  HANDOFF_COMPLETENESS_CORRECTION_PENDING /
  NOT_CLOSED

## PREARM-001 — preserved exactly

`AUCDEV023-CR-PCH6B-PREARM-001` =
MECHANICALLY_REMEDIATED /
CONTROL_ROOM_ACCEPTED_CANDIDATE /
OPERATIONAL_ADOPTION_PENDING /
NOT_YET_CLOSED.

## R1 / R2 / R3 — preserved unchanged

- R1 credential-source attachment operator premise (unchanged).
- R2 post-verify liveness race reduced, not eliminated (unchanged).
- R3 preserved V2/runtime evidence strength (unchanged).

The remediation report's disclosed scope boundary is preserved at its
recorded strength: the sealed interpreter binds the Python MAIN-BINARY bytes;
its shared-library dependencies, the dynamic linker and the kernel remain
ambient execution-platform dependencies outside the sealed-object binding.
This disclosure is NOT silently promoted to an independently accepted
residual beyond its currently recorded evidence strength.

## Governance held

- EVENT `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01` INSTANTIATED;
  PATH-B slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT.
- AUCDEV-023 = P1 / READY / NOT DONE.
- Existing Auditor-A attempt `…-AUDITOR-A-01` remains SPENT / SINGLE-USE /
  NO-RETRY. No replacement Auditor-A attempt exists; none is reserved or
  minted. Auditor-B authority = NONE. FIRST_PASS_A = ABSENT.
- MODEL_ENGAGEMENTS_USED = 0 for the settled attempt.
- Qualification NONE; installation NONE; audit verdict NONE; NO operational
  adoption.
- Frozen external event root untouched append-only; historical
  records/handoffs NOT rewritten; prior closures RETAINED.

## Zero-execution publication census

VM/QGA/virsh = 0; channel connections/probes = 0; connect attempts = 0;
socket probes = 0; real credential access (stats/opens/reads/hashes/
transmissions) = 0; send_once_v2 invocation = 0 (read + hashed only);
bridge-v2 invocation = 0; OPERATOR_SEND_NOW created/consumed = 0;
BootstrapAuthority imports/constructions = 0; run_attempt = 0; attempt
accounting records = 0; attempt ids created = 0; provider/model/frontier
requests = 0; CLAUDE/CODEX/AUDIT-COUNCIL executions = 0;
archive-member execution = 0; test execution = 0. The only executions this
session: ordinary Git/GitHub publication mechanics and local data-only
python text/hash/AST/tar tooling on non-secret bytes.

## Honest session iteration (instrument-side, without erasure)

Every first output is preserved under the untracked evidence workspace
`aucdev023-pch6b-int001int002-rem-crrb-pub-20261005-01/evidence`. NO failed
observation was rewritten as PASS without a corrected re-derivation on
IDENTICAL bytes:

- T-1 the subject-archive manifest parser v1 counted the manifest's single
  `#` comment header line as a checksum row (36 raw lines -> false
  "manifest_row_count_36" and a phantom empty-path row). Corrected to
  comment-aware parsing; the verifier re-ran FROM SCRATCH on identical bytes
  with 35 valid rows + 1 comment line and ALL 30 gates PASS
  (subject-archive-verify-run-002; run-001 preserved).
- T-2 the source-review instrument v1 reported four false FAILs of known
  encoding classes on compliant SHA-verified bytes: (a) the verifier-argv
  script-element check looked for the `/proc/self/fd` string inside the list
  element instead of the Name bound to it (the binding is separately proven
  by S10); (b) the REQUIRED_SEALS comparison included statement parentheses
  that `ast.get_source_segment` excludes from the value expression (the seal
  constants are exactly 0x1|0x2|0x4|0x8 = 0xf); (c) the banned-construct
  text scan hit the two legitimate `re.compile` regex sites (corrected to an
  AST call-name check); (d) the credential-term location check used
  `tree.body[1]` for the module docstring end (the docstring is `body[0]`,
  ending line 78, which covers the line-71 docstring mention). All four
  corrected; the review re-ran FROM SCRATCH on identical bytes with ALL 39
  gates PASS (source-review-run-002; run-001 preserved).

## Publication scope

Exactly one NEW canonical record (this file) plus rotation of
`docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (lines 3 / 11 / 23-24 and one
NEW dated tail record) and `docs/chatgpt-project/AUCDEV-BACKLOG.md` (one NEW
dated status bullet immediately after the INT-001/INT-002 remediation status
bullet and one NEW dated tail record; pure inserts). No fourth tracked path.
NOT altered: the remediation record; the preparation/readback records;
v1/v2 candidate source; accepted PREARM bytes; accepted V2 bytes; frozen
runtime; frozen target; event-host state; historical generated-LAST archives
(including the subject archive, whose SHA-256
`016091a98cf66403c879b7d6b84fe65fcb77fc3e5de84a9e87acfc4e994a7400` is
recorded here for identity; a future correction, if separately authorized,
must create a NEW append-only correction handoff identity and must NOT
overwrite, mutate or silently replace the historical archive).

## Disposition

AUCDEV_023_PCH6B_PRELAUNCH_INTEGRATION_INT001_INT002_REMEDIATION_CONTROL_ROOM_READBACK =
PARTIALLY_ACCEPTED /
PUBLICATION_GEOMETRY_PASS /
INT001_REMEDIATION_MECHANICS_SUBSTANTIALLY_SUPPORTED /
INT002_REMEDIATION_MECHANICS_SUBSTANTIALLY_SUPPORTED /
PRESERVED_RUNTIME_EVIDENCE_SOURCE_CORROBORATED /
GENERATED_LAST_LISTED_PAYLOAD_REHASH_PASS /
GENERATED_LAST_MANIFEST_PAYLOAD_SET_INCOMPLETE /
GENERATED_LAST_EXECUTABLE_MODE_FIDELITY_NOT_PRESERVED /
HANDOFF_CORRECTION_REQUIRED_BEFORE_FINDING_CLOSURE /
NO_OPERATIONAL_ADOPTION /
NO_ATTEMPT_AUTHORITY /
AUDITOR_B_AUTHORITY_NONE /
AUDIT_VERDICT_NONE /
QUALIFICATION_NONE /
INSTALLATION_NONE

THIS READBACK GRANTS NOTHING.

## NEXT — exactly one, grants nothing

OPERATOR DECISION ON WHETHER TO AUTHORIZE A NARROW ZERO-MODEL APPEND-ONLY
GENERATED-LAST HANDOFF-FIDELITY CORRECTION FOR
AUCDEV023-CR-PCH6B-PRELAUNCH-REM-HANDOFF-001 AND
AUCDEV023-CR-PCH6B-PRELAUNCH-REM-HANDOFF-002, WITHOUT MODIFYING OR
REPLACING THE HISTORICAL SUBJECT ARCHIVE OR THE V2 REMEDIATION SOURCE,
BEFORE INT-001 / INT-002 FINDING CLOSURE, OPERATIONAL ADOPTION,
ATTEMPT-SPECIFIC PRELAUNCH PACKAGING, REPLACEMENT AUDITOR-A ATTEMPT
AUTHORITY OR AUDITOR-B AUTHORITY IS CONSIDERED.

Recording this NEXT grants NOTHING. No attempt authority follows
automatically; Auditor-B authority remains NONE; no replacement Auditor-A
attempt exists or is authorized; any new attempt, attempt-specific prelaunch
package, channel re-probe, protocol change, teardown or real-credential use
requires a NEW explicit operator decision.

## Standing negative constraints (unchanged)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from an
agent session absent an explicit single-use operator attempt authority (and
even then at most the ONE authorized call, never a second); never rerun the
launcher; never treat any recorded grant phrase (including any phrase
recorded here) as a new grant; never execute a real auditor or
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
artifacts under `/srv/frevp/`; never start or reopen the event-host VM or
connect to the candidate credential channel from a record-only session; and
never run privileged mount/pivot_root/umount experiments on the operator's
live host and never automatically re-run an interrupted privileged command —
privileged GATE-W-prime boundary work belongs in the disposable-KVM
environment.
