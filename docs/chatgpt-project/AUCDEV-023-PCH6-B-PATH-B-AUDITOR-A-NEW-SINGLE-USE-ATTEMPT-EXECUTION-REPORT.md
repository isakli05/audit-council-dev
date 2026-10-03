# AUCDEV-023 PCH6-B — Path-B Auditor-A NEW single-use attempt — FAIL-CLOSED PRE-RUN STOP (operator credential source not established) publication record

Publication authority: AUCDEV-023-PCH6B-730D2B29-PATHB-AUDITOR-A-ATTEMPT-20261004-01
(single-use operator execution authority for EXACTLY ONE reserved Auditor-A attempt inside the already-instantiated Path-B event; this session STOPPED FAIL-CLOSED BEFORE any authority import, any BootstrapAuthority construction and any run_attempt call, and its single-use authority is CLOSED UNEXERCISED).

## 1. Disposition — recorded EXACTLY at the reached (fail-closed) strength

AUCDEV_023_PCH6B_PATH_B_AUDITOR_A_NEW_SINGLE_USE_ATTEMPT_EXECUTION =
FAIL_CLOSED_PRE_RUN_OPERATOR_CREDENTIAL_SOURCE_NOT_ESTABLISHED /
LIVE_BASE_3817CEF_VERIFIED_EXACT /
EVENT_HOST_CONTINUITY_PRE_START_EXACT /
CANONICAL_RUNTIME_LAYOUT_VERIFIED_37_OF_37_DATA_ONLY /
PRECALL_CUSTODY_NEGATIVES_PASS_PRE_AND_POST /
NO_CONFORMING_OPERATOR_CREDENTIAL_CHANNEL_ESTABLISHED /
OPERATOR_DECIDED_STOP_FAIL_CLOSED /
CREDENTIAL_SOURCE_CLASS_NONE /
NO_REAL_CREDENTIAL_BYTE_READ_HASHED_LOGGED_OR_PERSISTED /
BOOTSTRAP_AUTHORITY_CONSTRUCTIONS_0 /
RUN_ATTEMPT_CALLS_0 /
NO_ATTEMPT_ACCOUNTING_CLAIM_CREATED /
SESSION_AUTHORITY_CLOSED_UNEXERCISED /
RESERVED_ATTEMPT_RUNTIME_UNCLAIMED /
AUDITOR_B_AUTHORITY_NONE /
MODEL_ENGAGEMENTS_USED_0 /
FIRST_PASS_A_ABSENT /
EVENT_REMAINS_INSTANTIATED /
PATH_B_SINGLE_EVENT_SLOT_REMAINS_BOUND /
NO_AUDIT_EXECUTION /
NO_AUDIT_PASS /
QUALIFICATION_NONE /
INSTALLATION_NONE /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK

This disposition is NOT an audit verdict, establishes NO frozen-target product
finding, and grants NO execution authority of any kind.

## 2. Role and boundary of THIS session

This session was the EXECUTION IMPLEMENTER for the operator's new single-use
authority AUCDEV-023-PCH6B-730D2B29-PATHB-AUDITOR-A-ATTEMPT-20261004-01 for
reserved attempt AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01 of
event AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 (frozen audit target
`730d2b29f7c0e7d33af3451b6d9205ec27c143ed` AUDIT SUBJECT / NOT AUTHORITY): at
most ONE `BootstrapAuthority.run_attempt(...)` call. NOT Auditor-B (authority
NONE throughout), NOT a retry/revival/re-mint of the earlier CLOSED UNEXERCISED
Auditor-A execution-session authority (which was NOT revived and is NOT the
source of the new authority), NOT an event-package preparer/rebuilder/restager
(ZERO restaging — the accepted canonical runtime layout was only VERIFIED, never
mutated), NOT a package/binding/event/target mutator, NOT the Control Room, NOT
an independent auditor, NOT an `/audit-council` executor, NOT a
provider/model/frontier executor, NOT a qualification authority, NOT an
installation authority. The §16 fail-closed stop recorded here is NOT an audit
verdict and establishes NO frozen-target product finding.

## 3. Exact live bootstrap verification (performed BEFORE any VM start)

- `git fetch origin` clean rc 0; live GitHub master (ls-remote authoritative) ==
  origin/master == local HEAD == `3817cef05f8f0ac36f5c21f36d711d412b23ea29`
  EXACT — the authorized governance base of this authority.
- Root tree `6c2dfdb15b4d72fedfdaa786265493efbdf92e78` EXACT; sole parent
  `e5878a4fa751eed366790985ba30a77da0649181` EXACT (the event-host
  execution-layout staging Control Room readback whose recorded NEXT operator
  decision — the new single-use Auditor-A attempt authority — THIS record
  implements); single-parent fast-forward geometry; trust anchor
  `3058868416241d394cfaaa40cc585085db486f37` ancestor rc 0.
- Frozen audit target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` present
  (tree `2585796efd5cb6902226cfff785bb901297a15e3`, remediation parent
  `068f5e29904f446bf832138fd64c8833b9037cb7`), ancestor, UNTOUCHED,
  AUDIT SUBJECT / NOT AUTHORITY.
- Protected trees held EXACT at base: bootstrap-authority
  `154975872e15d53e1706016f5bb60c83727004f0`, bootstrap-supervisor
  `3056e577259ab0b0b0472f82ebc306506f3e084c`, qualification-harness
  `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill
  `efd8c2e48edbb25795b3aacb1ce3c23fde10082a`.
- The prior readback publication geometry re-verified: exactly three changed
  tracked paths over `e5878a4f` (NEW staging CR readback record, M CURRENT, M
  BACKLOG), no protected source/package path touched.
- The eight mandated canonical records read at the exact base with blob
  identities recorded: CURRENT `25f1d6c6`, BACKLOG `2c465ed6`, staging CR
  readback `35bb182e`, staging remediation report `d0df52fe`, Auditor-A pre-run
  stop CR readback `0177a779`, Auditor-A attempt execution report `bb35e6f0`,
  runbook `a1d27ed1`, protocol `42955b85`; CURRENT/BACKLOG working copies
  verified byte-identical to the base blobs before any editing.
- Required governance state (tasking §2) verified from CURRENT at the exact
  base: AUCDEV-023 P1 / READY / NOT DONE; EVENT INSTANTIATED; PATH-B one-event
  slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT; reserved Auditor-A attempt
  RUNTIME-UNCLAIMED; MODEL_ENGAGEMENTS_USED = 0 (PROPOSED 2 unchanged);
  FIRST_PASS_A ABSENT; AUDITOR_B_ATTEMPT_AUTHORITY NONE; QUALIFICATION NONE;
  INSTALLATION NONE; PRERUN-001/PRERUN-002 closed only at Control Room
  remediation-readback strength; STAGING-RB-001 nonblocking. None of these was
  reinterpreted as an audit PASS.
- Repository drift (232 status entries incl. the smoke-fixture /
  smoke-fixture-103 gitlink rows) preserved UNSTAGED throughout; this record's
  path ABSENT at base.

## 4. §10 event-host pre-start continuity — PASS EXACT

- Preserved domain XML
  `/home/isa/aucdev023-pch6b-codex-followup-20261003-01/vm/cxfollowup-domain.xml`
  SHA-256 `b66adf20df6d229fca99c23e37de78fe1eb9d23dffcd5dd36de5e7c0992834fe`
  EXACT; domain name `aucdev-frevp-730d2b29-20261002-02`, UUID
  `d8d26fc1-15dc-4602-989c-ea40ec50010e`, work disk
  `/var/lib/libvirt/images/aucdev-gatew/aucdev-frevp-cxfollowup-20261003-01-work.qcow2`
  all EXACT.
- Quiescent pre-start work-disk SHA-256
  `473a96a00374fdf62b6e21bfce5cead121e16279b5c59eb7d317018551a2f712` —
  EXACT match to the accepted latest event-host continuity checkpoint.
- Rehearsal domain `aucdev-gatew-730d2b29-20261002-01` shut off, untouched
  throughout; event-host domain pre-session state UNDEFINED (quiescent).
- Host boot-id `a2aec063-adc9-4342-9789-bc042d77bfc7` and host mount count 84
  recorded (unchanged from the accepted prior-session values).

## 5. Event-host administration cycle (ONE bounded cycle, ordinary administration only, ZERO canonical-guest writes)

- Domain defined from the exact preserved XML; started
  2026-10-03T21:56:55.674Z (libvirt 12.8.0 / qemu 11.1.1); qemu-guest-agent
  responsive after 3 pings; guest kernel `7.2.7-arch1-1` lineage EXACT; fresh
  guest boot-id `9fcae785-93f6-4257-987c-10da5fd9d0b6` recorded as event
  metadata only.
- ALL guest interactions were read-only data-only QGA queries EXCEPT one
  non-secret instrument transfer: the session-written data-only verifier
  `/tmp/verify_precall.py` (7839 bytes; byte-fidelity re-hashed in-guest before
  execution; strictly standard-library hashing/JSON/stat/listing; never imports
  bootstrap_authority, never executes any package member) transferred via the
  QGA file interface and REMOVED from the guest after use.
- The canonical runtime root `/srv/aucdev-frevp-event-runtime/…`, the custody
  tree `/srv/aucdev-frevp-custody/…`, the frozen packages, the pinned client
  and everything else under `/srv` were NEVER written: ZERO repair, ZERO
  restaging, ZERO repopulation.
- Clean shutdown 2026-10-03T22:08:05.866Z (ACPI; shut off within ~5 s);
  undefine restoring the pre-session UNDEFINED domain state; rehearsal domain
  untouched.
- Post-stop quiescent work-disk SHA-256
  `d99c74a8dff39cb641133cfb1577a81154f21d904f6f7e83dc469e3b2ca4747d`
  recorded as the NEW event-host continuity checkpoint (the normal consequence
  of the authorized boot/agent cycle; equality with the pre-start checkpoint is
  NOT claimed; no reset/rollback/copy-over was performed — attempt history is
  append-only). Host boot-id and mount count 84 UNCHANGED post-cycle — host
  non-mutation EXACT (no mount/pivot_root/unshare/bwrap experiment, no
  live-host boundary execution, no credential operation).

## 6. §11/§12 read-only precall gates — 37/37 PASS data-only (before ANY authority import/construction)

Verified in-guest by the session-written data-only verifier, re-run from
scratch after instrument corrections and re-run AGAIN immediately before
shutdown (identical 37/37):

- RUNTIME_ROOT
  `/srv/aucdev-frevp-event-runtime/AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01`
  exists; authority-package MANIFEST raw SHA-256
  `7713b89e2618d27963be0df4dd5ebb33961a5b48c063c62ecacff2238da1425f` EXACT with
  non-circular package_sha256 `4399cb062e3fe9a5c4e6e71ad90e8515b3f0b462b6a648c458068cd6f01263db`
  declared AND recomputed (canonical JSON of MANIFEST minus its own
  package_sha256) EXACT; Auditor-A binding raw SHA-256
  `36596c24f2a4a8bc56482cf19c989a7728ab5767720f5e946a1a2c25be91da80` EXACT;
  Auditor-A event-package MANIFEST raw
  `d48ae36b228b730bfad8138cb08af38cf34bb4fec954f948a17ba8e5f8dc5a46` EXACT with
  package_sha256 `abc6d34ae65069157e7bf9a09a939fb66877a77a6fdc57dcaa1c356337519744`
  declared AND recomputed EXACT.
- EVERY manifest-covered payload re-hashed size+SHA: 12/12 authority-package
  rows and 18/18 Auditor-A event-package rows PASS — NO unexpected mutation;
  full runtime-root file-set equality (manifest rows + the two non-circular
  MANIFEST.json members + auditor-a/binding.json, nothing extra, nothing
  missing); zero `__pycache__`.
- Canonical caller launcher
  `${RUNTIME_ROOT}/auditor-a/event-package/boundary/frevp_launcher` SHA-256
  `8c40138f5ba1354cc095e988125ed14b3507e313eaa3a21f6cd86d6e691a4c04` EXACT;
  pinned client `/opt/node-dist/node-v24.14.0-linux-x64/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`
  present, SHA-256 `56fe3da88458465fb27d7e9299dddb3fead55750fb9c2de795f233b5eea6dce1`
  EXACT; dynamic-gate rows CLIENT_SELECTION_PREFLIGHT `1029e9c2…`,
  NETWORK_READINESS `b2407af1…`, RESOURCE_GATE `034abc60…`, validator
  `b38d12b5…`, wrapper (`705ca96a…` prefix) and profile `b552e40b…` each found
  EXACTLY ONCE in the verified manifest rows; modes dirs 0555 / files 0444 /
  the six runtime executables 0555 / owner root:root throughout.
- §12 custody negatives (PASS and re-verified unchanged immediately before
  shutdown): auditor-a-01 st_dev 33 st_ino 60133 mode 0700 owner
  aucdev:aucdev EMPTY; auditor-b-01 st_dev 33 st_ino 60134 mode 0700 owner
  aucdev:aucdev EMPTY; whole custody tree ONLY the two roots; all six reserved
  artifacts (`…-AUDITOR-A-01.{jsonl,report.json,first-pass-report.json}` and
  `…-AUDITOR-B-01.{jsonl,report.json,first-pass-report.json}`) PROVEN ABSENT.

## 7. §16 credential-source gate — the decisive FAIL-CLOSED finding

Discovery was strictly metadata-only (names, stat, socket/fifo census); NO
credential byte was ever opened, read, hashed, logged, copied or persisted by
this session, in either host or guest:

- Guest-wide FIFO/socket census: only distribution gnupg sockets; NO
  credential fifo, NO credential unix/vsock listener, NO credential daemon or
  systemd service.
- Guest name search (cred/feed/vault/seal/channel over /srv /opt /home /root
  /etc/systemd /usr/local) and a recent-file sweep: the ONLY credential-named
  artifact is `/srv/frevp/src/cred-init/cred.bin` — a regular file of exactly
  87 bytes = the SYNTHETIC rehearsal credential
  (`AUCDEV023-FREVP-SYNTHETIC-CREDENTIAL-…-DISJOINT-NOT-REAL`, disjoint from
  every real identity; metadata inspected ONLY, content NEVER opened); it is
  rehearsal infrastructure, NOT a real credential and NOT a conforming source.
- No operator-staged real credential exists anywhere in the guest; no
  established PIPE or sealed-memfd channel exists. The guest's only
  host→guest control path is the qemu-guest-agent channel (the tasking forbids
  carrying the credential through QGA JSON/orchestration logs; the domain XML
  has no second virtio channel).
- The frozen `CredentialCustody.ingest` source contract was read DATA-ONLY
  from Git (never imported): permitted sources are a PIPE fd (S_ISFIFO) or a
  fully-sealed memfd; ordinary persisted plaintext files are REFUSED
  (`CUSTODY_SOURCE_IS_ORDINARY_FILE`); reads are bounded 1..65536 bytes inside
  run_attempt only.
- Host-side, the operator's real credential exists at
  `~/.claude/.credentials.json` (291 bytes, mode 0600 — EXISTENCE/stat ONLY,
  content NEVER read). The guest is host-reachable at 192.168.122.19 on the
  default NAT network.
- CONFORMING ESTABLISHED OPERATOR-CONTROLLED SOURCE: NOT AVAILABLE. The
  operator was presented the decision (establish a conforming operator-fed
  sealed-memfd/PIPE channel now, with the feed performed by the operator so
  credential bytes never transit this session, versus the tasking's §16
  fail-closed stop) and EXPLICITLY CHOSE: STOP FAIL-CLOSED PER §16.
- Therefore: `AUDITOR_A_OPERATOR_CREDENTIAL_SOURCE_NOT_ESTABLISHED`;
  CREDENTIAL_SOURCE_CLASS = NONE; credential_source_fd NEVER opened; the §17
  final irreversible pre-run check and the §18 run_attempt call were NEVER
  REACHED.

Sequencing note (recorded transparently): the tasking orders construction
(§13–§15) before the §16 credential gate. Because the §16 precondition was
determinately absent BEFORE construction and the operator chose the §16 stop,
this session performed NO authority import, NO strict-parse execution and NO
BootstrapAuthority construction (BOOTSTRAP_AUTHORITY_CONSTRUCTIONS = 0) — a
strictly more conservative path than constructing an authority that could only
have reached the same §16 stop; nothing was left PREPARED, no fds were held,
and the §32 required state for a credential-source gate stop before
run_attempt is satisfied EXACTLY.

## 8. Governance state after this session (held EXACTLY)

- NEW Auditor-A SESSION AUTHORITY (AUCDEV-023-PCH6B-730D2B29-PATHB-AUDITOR-A-ATTEMPT-20261004-01)
  = CONSUMED_BY_THIS_PUBLICATION / CLOSED / FAIL_CLOSED_PRE_RUN /
  UNEXERCISED (zero run_attempt calls; recording the stop consumes the
  single-use authority; do NOT reuse or revive it).
- RESERVED ATTEMPT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01
  = RUNTIME-UNCLAIMED / SINGLE-USE (no O_EXCL claim, no accounting record, no
  report sink; any future Auditor-A execution requires a NEW explicit operator
  decision).
- AUDITOR_B_ATTEMPT_AUTHORITY = NONE (no Auditor-B construction, binding
  inspection for execution, credential, run_attempt, engagement, peer-output
  access or reconciliation — all never started).
- MODEL_ENGAGEMENTS_USED = 0 (PROPOSED 2 unchanged; CONSUMED_PRE_EXEC absent —
  engagement count derived from the absence of any attempt accounting, not
  guesswork). FIRST_PASS_A = ABSENT.
- EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 remains INSTANTIATED;
  PATH-B one-event slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT; the stop created
  NO second event and revokes NOTHING.
- The earlier Auditor-A execution-session authority remains CLOSED UNEXERCISED;
  no recorded grant phrase was treated as a new grant.
- Held governance preserved: frozen target `730d2b29…` AUDIT SUBJECT / NOT
  AUTHORITY; PCH6-B-SD-002 and PCH6-CR-BSD-001 AWAITING FRESH INDEPENDENT AUDIT
  / NOT CLOSED; PCH6-B-SD-001 RETAINED / OPEN; ROOT_CAUSE_NOT_ESTABLISHED
  unchanged; INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED with installed
  source `8ae33444…`; installed Audit Council NOT authority for this event;
  NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE disclosed residual; STAGING-RB-001
  nonblocking residual unchanged; historical records/handoffs NOT rewritten;
  prior closures RETAINED; NO audit execution, NO audit PASS, QUALIFICATION
  NONE, INSTALLATION NONE; AUCDEV-023 remains P1 / READY / NOT DONE.
- The frozen external event root was NOT touched by this session (no read of
  its bytes was required; all verification used the canonical in-guest runtime
  layout); it remains VALID append-only and MUST NOT be rewritten.

## 9. Zero-execution census (this session)

VM_RUNS = 1 (the ONE authorized bounded administration cycle, read-only guest
operations + the single non-secret /tmp instrument, reported separately);
EVENT_HOST_CANONICAL_WRITES = 0 (ZERO restaging/repair/repopulation);
BOOTSTRAP_AUTHORITY_CONSTRUCTIONS = 0; BOOTSTRAP_AUTHORITY_IMPORTS = 0;
RUN_ATTEMPT_CALLS = 0; ATTEMPT_AUTHORITIES_GRANTED = 0 (the single-use
operator authority was received, held and closed UNEXERCISED);
ATTEMPT_ACCOUNTING_RECORDS_CREATED = 0; REPORT_SINKS_CREATED = 0;
CREDENTIAL_SOURCES_OPENED = 0; REAL_CREDENTIAL_CONTENT_READS = 0;
DYNAMIC_GATE_EXECUTIONS = 0; BOUNDARY_LAUNCHER_EXECUTIONS = 0;
TOOL_WRAPPER_EXECUTIONS = 0; VALIDATOR_EXECUTIONS = 0; CLAUDE_EXECUTIONS = 0;
CODEX_EXECUTIONS = 0; AUDIT_COUNCIL_EXECUTIONS = 0;
PROVIDER_MODEL_FRONTIER_REQUESTS = 0; MODEL_ENGAGEMENTS_CONSUMED = 0;
FIRST_PASS_ARTIFACTS = 0; PRIVILEGED_NAMESPACE_MOUNT_OPERATIONS = 0;
QUALIFICATION = NONE; INSTALLATION = NONE. (Every verification data-only —
Git identity resolution, byte/blob equality, stream-read hashing, JSON/text
scanning, filesystem stat/listing; the only network operations are the
ordinary Git/GitHub publication mechanics; the synthetic rehearsal cred.bin
was never opened.)

## 10. Publication safety (this session)

Live master re-resolved AFTER the fail-closed stop and immediately before
staging: still `3817cef05f8f0ac36f5c21f36d711d412b23ea29` EXACT — canonical
publication permitted. Staged EXACTLY the three authorized documentation paths
(NEW this record; M CURRENT; M BACKLOG) with the rotation confined EXACTLY to
CURRENT lines 3/11/23-24 plus one NEW dated tail record, and BACKLOG EXACTLY
two pure insert zones (one NEW dated status bullet immediately after the
staging CR readback status bullet; one NEW dated tail record) — zone sets
computed-before-write by an assertion-guarded builder AND re-asserted from the
staged blobs. Protected trees and frozen target held EXACT in the staged
write-tree (ZERO source modification staged and ZERO performed); staged ==
working on all three paths; `git diff --check` and staged
`git diff --cached --check` PASS; no source/test/package path staged, no
.jsonl, no event-package tracked path, no VM/binary artifact, no event-root
file, no credential material, no accounting record, no report sink and no
first-pass bytes committed; repository drift preserved unstaged; queue
mechanically recounted base == staged on every structural dimension; CURRENT
top-level active state contains EXACTLY ONE NEXT (line-start NEXT census
unchanged 10 → 10: one active + nine historical); no queue-row status
transition; no backlog item marked DONE; credential/secret mechanical scan
clean over the NEW record and all diff-added lines; the full record-only
precommit gate battery re-ran FROM SCRATCH on the FINAL staged bytes and ALL
PASSED (battery results recorded in the session evidence workspace and the
generated-LAST handoff). The commit message records the exact authorized base,
the staged write-tree, branch master and this disposition; the exact resulting
publication SHA and result root tree are reported in the FINAL-RETURN, the
post-push GitHub readback and the generated-LAST handoff (SELF-COMMIT
IDENTITY RULE).

## 11. Honest iteration ledger (this session — instrument-side ONLY, no state consequence)

- T-1: the §11/§12 verifier v1 assumed MANIFEST file rows keyed
  `name`/`size`; the frozen MANIFEST rows are keyed `path`/`bytes` — a
  read-only KeyError on the first payload pass (all identity checks already
  PASS); corrected key mapping re-ran the full battery on IDENTICAL bytes.
- T-2: the verifier v2 file-set-equality expectation omitted the two
  MANIFEST.json members themselves (the frozen manifest is non-circular and
  does not self-list) producing one false FAIL with the two "extra" files
  being exactly the legitimate MANIFESTs; corrected expectation re-ran FROM
  SCRATCH on IDENTICAL bytes 37/37 PASS.
- Every first output is preserved in the untracked session evidence workspace
  `aucdev023-pch6b-auditora-newattempt-evidence-20261004-01`; NO failed
  observation was rewritten as PASS without a corrected re-derivation on
  IDENTICAL bytes.

## 12. Next action — EXACTLY ONE (grants nothing)

INDEPENDENT CONTROL ROOM READBACK OF THIS EXACT FAIL-CLOSED PRE-RUN STOP
(OPERATOR CREDENTIAL SOURCE NOT ESTABLISHED), THE PRECALL 37/37 GATE
EVIDENCE, THE PRE/POST CUSTODY NEGATIVES, THE NEW EVENT-HOST DISK CONTINUITY
CHECKPOINT AND THE GENERATED-LAST HANDOFF — INCLUDING THE CREDENTIAL-CHANNEL
AVAILABILITY FINDING — BEFORE ANY NEW AUDITOR-A ATTEMPT AUTHORITY IS
CONSIDERED (with the establishment of a conforming operator-controlled
credential delivery channel a separate explicit operator decision that any
future attempt authority depends on). Recording this NEXT grants NOTHING.
STOP after Auditor-A. NO second run_attempt. NO retry. NO Auditor-B. NO peer
substance access. NO `/audit-council`. NO qualification. NO installation.

## 13. Standing prohibitions (unchanged)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from an
agent session absent an explicit single-use operator attempt authority (and
even then at most the ONE authorized call, never a second); never rerun the
launcher; never treat any recorded grant phrase (including any phrase recorded
here) as a new grant; never execute a real auditor or provider/model; never
open the four historical sealed artifacts (identity-only forever); never open,
read, hash, log or persist any real credential byte; never relabel or rewrite
historical model identities, runs, records, matrices, prompts or evidence
workspaces (append-only); never claim audit PASS, qualification, installation
or any authority from this publication — it grants none; never rewrite or
repack the frozen external event root; never mutate the canonical runtime root
or restage the event host after event instantiation absent a separate explicit
operator remediation authority; never delete or repurpose the rehearsal-derived
artifacts under `/srv/frevp/`; never start or reopen the event-host VM from a
record-only session; and never run privileged mount/pivot_root/umount
experiments on the operator's live host and never automatically re-run an
interrupted privileged command — privileged GATE-W-prime boundary work belongs
in the disposable-KVM environment.
