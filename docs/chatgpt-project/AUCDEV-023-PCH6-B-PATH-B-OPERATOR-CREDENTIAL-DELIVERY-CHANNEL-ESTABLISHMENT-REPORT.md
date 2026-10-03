# AUCDEV-023 PCH6-B — Path-B operator credential-delivery channel establishment — FAIL-CLOSED (synthetic end-to-end probe verifier mismatch) publication record

Establishment authority: AUCDEV-023-PCH6B-730D2B29-CREDENTIAL-CHANNEL-ESTABLISHMENT-20261004-01
(narrow ZERO-ATTEMPT operator-controlled credential-delivery channel establishment for the EXISTING instantiated Path-B event AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01; this session was the bounded IMPLEMENTER of the channel-establishment remediation limited to resolving AUCDEV023-CR-PCH6B-AUDITORA-CRED-001; throughout the session AUDITOR_A_ATTEMPT_AUTHORITY = NONE, AUDITOR_B_ATTEMPT_AUTHORITY = NONE, MODEL_ENGAGEMENTS_USED = 0, RESERVED_ATTEMPT = RUNTIME-UNCLAIMED, RUN_ATTEMPT_CALLS = 0, and NO real credential byte was read by this session).

## 1. Disposition — recorded EXACTLY at the reached (fail-closed) strength

AUCDEV_023_PCH6B_OPERATOR_CREDENTIAL_DELIVERY_CHANNEL_ESTABLISHMENT =
FAIL_CLOSED_SYNTHETIC_END_TO_END_PROBE_VERIFIER_MISMATCH /
LIVE_BASE_53390FA0_VERIFIED /
EXISTING_EVENT_HELD_NO_SECOND_EVENT /
PRE_CHANNEL_EVENT_HOST_CONTINUITY_VERIFIED /
HOST_LOCAL_LIBVIRT_UNIX_VIRTIO_SERIAL_CHANNEL_DESIGN_ESTABLISHED /
NO_TCP_UDP_VSOCK_CHANNEL /
SUCCESSOR_XML_APPEND_ONLY_ONE_CHANNEL /
GUEST_BRIDGE_NON_SECRET_STAGED /
CHANNEL_JSON_NON_SECRET_STAGED /
PREWRITE_GATES_38_OF_38 /
POSTWRITE_GATES_33_OF_33 /
SYNTHETIC_PROBE_SINGLE_CONNECTION_CONSUMED /
SYNTHETIC_PROBE_FAILED_VERIFIER_MISMATCH /
BRIDGE_RC_0_CLEAN_EOF_CONSISTENT_WITH_EMPTY_RELAY /
ROOT_CAUSE_NOT_ESTABLISHED /
NO_RETRY_PER_TASKING_FAIL_CLOSED /
CRED_001_REMAINS_OPEN_BLOCKING /
REAL_CREDENTIAL_BYTES_USED_0 /
FROZEN_RUNTIME_UNCHANGED /
CUSTODY_IDENTITIES_HELD /
CUSTODY_ROOTS_EMPTY /
RESERVED_ATTEMPT_RUNTIME_UNCLAIMED /
AUDITOR_A_AUTHORITY_NONE /
AUDITOR_B_AUTHORITY_NONE /
BOOTSTRAP_AUTHORITY_CONSTRUCTIONS_0 /
RUN_ATTEMPT_CALLS_0 /
MODEL_ENGAGEMENTS_USED_0 /
FIRST_PASS_A_ABSENT /
NO_AUDIT_EXECUTION /
NO_AUDIT_PASS /
QUALIFICATION_NONE /
INSTALLATION_NONE /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK

This disposition is NOT an audit verdict, establishes NO frozen-target product
finding, and grants NO execution authority of any kind.  The channel
candidate was NOT accepted: the single authorized synthetic end-to-end probe
connection FAILED verification and, per the tasking's explicit no-retry rule,
NO retry was performed; the session STOPPED FAIL-CLOSED.

## 2. Role and boundary of THIS session

This session was the bounded IMPLEMENTER of the operator-authorized narrow
zero-attempt channel establishment.  It was NOT an Auditor-A or Auditor-B
attempt executor, NOT an auditor, NOT an /audit-council executor, NOT a
provider/model/frontier executor, NOT a qualification authority, NOT an
installation authority, NOT the Control Room.  It performed NO
BootstrapAuthority.run_attempt, NO BootstrapAuthority construction for
attempt execution, NO attempt accounting creation, NO report-sink creation,
NO dynamic audit gate, NO boundary launcher execution, NO Claude/Codex
inference, NO provider/model request, NO model-engagement consumption, NO
second event, NO frozen package rebuild, NO binding mutation, NO
frozen-target mutation, NO external event-root mutation, NO qualification
and NO installation.  No real credential byte was opened, stated, hashed,
copied, read, sent, tested, or placed into any channel.json, QGA payload,
argv, environment variable, Git object, or evidence archive.

## 3. Live bootstrap and held governance (verified before any mutation)

- Live GitHub master == origin/master == local HEAD ==
  53390fa036a4a5f21ef39102a490a4c35c5607e2 EXACT at bootstrap (fetch clean
  rc 0; ls-remote authoritative), root tree
  fc120559aad1ed501ba80d577a942d0486a3d59b EXACT, sole parent
  47d943c7b8816189fd2bfb374e10dd5b065e18ff EXACT; re-resolved EXACT
  immediately before staging (§27 rule).
- Trust anchor 3058868416241d394cfaaa40cc585085db486f37 ancestor rc 0.
- Frozen audit target 730d2b29f7c0e7d33af3451b6d9205ec27c143ed present,
  ancestor, UNTOUCHED, AUDIT SUBJECT / NOT AUTHORITY.
- Protected trees bootstrap-authority 154975872e15d53e1706016f5bb60c83727004f0 /
  bootstrap-supervisor 3056e577259ab0b0b0472f82ebc306506f3e084c /
  qualification-harness 5b8d5e5465923740470ff63ed9b8683f257a3787 /
  skill efd8c2e48edbb25795b3aacb1ce3c23fde10082a held EXACT at base.
- The seven mandated canonical records were read at the exact base with blob
  identities recorded (CURRENT 62688b01 / BACKLOG 3d8d28e9 / credential-source
  prerun stop CR readback 6cbcc441 / Auditor-A NEW attempt execution report
  4ed6efba / event-host staging CR readback 35bb182e / runbook a1d27ed1 /
  protocol 42955b85); CURRENT/BACKLOG working copies verified byte-identical
  to the base blobs before editing.
- Held governance verified: AUCDEV-023 P1 / READY / NOT DONE; EVENT
  AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 INSTANTIATED; PATH-B
  one-event slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT; reserved Auditor-A
  attempt RUNTIME-UNCLAIMED; Auditor-A attempt authority NONE; Auditor-B
  attempt authority NONE; MODEL_ENGAGEMENTS_USED 0; FIRST_PASS_A ABSENT;
  CRED-001 OPEN / BLOCKING; QUALIFICATION NONE; INSTALLATION NONE.  No
  previous Auditor-A authority was revived.
- Frozen CredentialCustody source contract read DATA-ONLY from the protected
  tree at the exact base (bootstrap_authority/custody.py blob
  37e6b5bb4365c7b29ba3632fe95362d5a7e16c09): permitted plaintext sources are
  a PIPE fd (stat.S_ISFIFO) or a fully-sealed memfd carrying ALL FOUR seals
  (F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE); ordinary files,
  directories, sockets and unsealed/partially-sealed memfds are refused;
  MAX_CREDENTIAL_BYTES = 65536.  The selected design therefore targets a
  final PIPE fd on the future attempt driver's stdin.

## 4. Design selection and successor domain XML (append-only)

- Selected transport class LIBVIRT_VIRTIO_SERIAL_HOST_LOCAL_UNIX with virtio
  target name org.aucdev.pch6b.cred.a and expected guest device
  /dev/virtio-ports/org.aucdev.pch6b.cred.a.  NO TCP, UDP, IP listener, use
  of the previously observed 192.168.122.19 address, vsock, SSH, QGA-JSON
  credential carriage, environment-variable or argv credential carriage, or
  guest plaintext credential file was used.  There is NO fallback transport.
- Historical preserved XML
  /home/isa/aucdev023-pch6b-codex-followup-20261003-01/vm/cxfollowup-domain.xml
  verified UNCHANGED (SHA-256
  b66adf20df6d229fca99c23e37de78fe1eb9d23dffcd5dd36de5e7c0992834fe) and was
  NOT rewritten.  Data-only inspection confirmed a sufficient existing
  baseline (virtio-serial controller index 0 plus the QGA unix channel), so
  the dedicated second channel needed NO new controller or device class.
- NEW successor XML created at
  /home/isa/aucdev023-pch6b-credential-channel-20261004-01/vm/credchannel-domain.xml
  (SHA-256 065096925d43240b1c69b2f0c0ae976f7bd6202a30c11228c936e89ce40d30b3,
  4417 bytes) derived byte-semantically from the exact historical XML by an
  assertion-guarded builder: textual decomposition is EXACTLY one insert zone
  of 4 lines immediately after the QGA </channel>; the normalized (C14N +
  deterministic indent, both sides through the SAME transform) semantic diff
  contains EXACTLY the one added channel element
  (<channel type='unix'><target type='virtio' name='org.aucdev.pch6b.cred.a'/>
  <address type='virtio-serial' controller='0' bus='0' port='2'/></channel>)
  with ZERO removals; explicit preserved-field assertions hold for domain
  name aucdev-frevp-730d2b29-20261002-02, UUID
  d8d26fc1-15dc-4602-989c-ea40ec50010e, work disk
  /var/lib/libvirt/images/aucdev-gatew/aucdev-frevp-cxfollowup-20261003-01-work.qcow2,
  NIC MAC 52:54:00:6d:17:e4, 4 vCPUs, 8 GiB, machine pc-q35-11.1, ALL
  existing controllers, the QGA channel byte-for-byte, emulator, features,
  clock and pm.  The new channel carries NO explicit source path
  (libvirt-managed UNIX source-path allocation, mirroring the established
  QGA channel style); libvirt schema validation (virt-xml-validate) PASS.
  No Internet/IP listener was created.

## 5. Event-host continuity and the ONE bounded VM cycle

- Pre-session state: event-host domain aucdev-frevp-730d2b29-20261002-02
  ABSENT (undefined, quiescent); rehearsal domain aucdev-gatew-730d2b29-20261002-01
  shut off and untouched; host boot-id a2aec063-adc9-4342-9789-bc042d77bfc7
  and mount count 84 recorded.
- PRE-START work-disk SHA-256 verified EXACT =
  d99c74a8dff39cb641133cfb1577a81154f21d904f6f7e83dc469e3b2ca4747d
  (the accepted latest continuity checkpoint; 1747124224 bytes).
- ONE bounded ordinary-VM-administration cycle only: defined from the exact
  successor XML (both unix channels present in the defined XML), started
  2026-10-03T23:27:57Z, QGA responsive after 4 pings, guest kernel
  7.2.7-arch1-1 lineage EXACT, fresh guest boot-id
  64682b09-afd9-4e34-a97c-db41fab09358 recorded, clean agent shutdown
  2026-10-03T23:33:41Z, undefine restoring the pre-session undefined state.
  All guest interactions were read-only data-only QGA queries EXCEPT the
  authorized channel staging writes (§6) and the ephemeral non-secret /tmp
  instruments (gates/verifiers/probe runner), each removed after use.  The
  canonical runtime root, custody tree, frozen packages and pinned client
  were NEVER written (no repair, no restaging, no repopulation).
- POST-CHANNEL quiescent work-disk SHA-256 =
  b0c5f958dbf069f0c0f0cc33eb0e49eaf8c4fd0de8f303c36607c17425d008b4
  recorded as the NEW event-host continuity candidate checkpoint (the disk
  change is the authorized consequence of the boot cycle plus the staged
  bridge/channel.json; equality with the pre-channel checkpoint NOT claimed).
- Host non-mutation EXACT: boot-id and mount count 84 unchanged post-cycle;
  no mount/pivot_root/unshare/bwrap experiment; no live-host boundary
  execution.  No persistent socket exists while the domain is shut down (the
  libvirt channel directory is removed at shutdown; ss -lx verified absent
  after shutdown).

## 6. Channel artifacts (non-secret, staged OUTSIDE runtime root and custody)

- CHANNEL_ROOT =
  /srv/aucdev-frevp-credential-channel/AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01/auditor-a
  was ABSENT before staging (pre-write gate); the frozen runtime root
  /srv/aucdev-frevp-event-runtime/... and the custody tree were NOT touched.
- Exactly TWO persistent guest artifacts staged via the QGA file interface
  with byte-fidelity re-hash (guest sha == host sha EXACT for both):
  bridge.py — SHA-256
  46ce06dd9ac0a1c57712a6b8db750bd6f82f31dcdf989d5e323234b66ffeca0d (2787
  bytes), mode 0555 owner root:root; a tiny one-shot standard-library bridge
  (ctypes/os/stat/sys only) that: makes itself non-dumpable
  (PR_SET_DUMPABLE=0, PR_GET_DUMPABLE==0 verified) BEFORE reading any
  channel byte; verifies its stdout is a FIFO/pipe BEFORE reading; opens ONLY
  /dev/virtio-ports/org.aucdev.pch6b.cred.a read-only and verifies the fd is
  a character device; reads the channel stream once until EOF; writes the
  exact received bytes only to stdout; enforces the hard 65536-byte maximum;
  exits after one stream; emits only fixed non-secret failure tokens
  (ERR_PRCTL_SET / ERR_DUMPABLE_NOT_CLEARED / ERR_STDOUT_FSTAT /
  ERR_STDOUT_NOT_PIPE / ERR_CHANNEL_OPEN / ERR_CHANNEL_FSTAT /
  ERR_CHANNEL_NOT_CHARDEV / ERR_MAXBYTES / ERR_STREAM) on stderr; never
  prints, hashes, logs or persists payload content and never reports payload
  length.  No daemon, listener, background service or systemd credential
  daemon exists; the bridge runs only when explicitly invoked by a future
  authorized attempt session.  It never imports bootstrap_authority or any
  package member.  Its control logic was validated host-locally BEFORE
  staging (9/9: dumpable-cleared, stdout-FIFO gate, char-device class gate
  refusing a FIFO path, hard-max cap on /dev/zero, empty-stream clean EOF on
  /dev/null, single-constant dev-variant delta proof, send_once single
  connect + exact copy + token).
  channel.json — SHA-256
  025e0d743f89bbc9d8a4c31b2314b180b88c728889088415932040f7e0c34481 (664
  bytes), mode 0444 owner root:root; NON-SECRET immutable metadata exactly:
  schema AUCDEV-023-PCH6B-CREDENTIAL-CHANNEL-V1, event_id
  AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01, auditor_role AUDITOR_A,
  transport LIBVIRT_VIRTIO_SERIAL_HOST_LOCAL_UNIX, virtio_target_name
  org.aucdev.pch6b.cred.a, guest_device
  /dev/virtio-ports/org.aucdev.pch6b.cred.a, final_source_contract
  PIPE_FD_ON_FUTURE_DRIVER_STDIN, max_bytes 65536, bridge_sha256 (exact),
  real_credential_used_during_establishment false, run_attempt_authorized
  false, auditor_a_attempt_authority NONE, auditor_b_attempt_authority NONE.
  No credential path or credential metadata is included (mechanically
  verified).  All CHANNEL_ROOT directories finalized 0555 root:root; no
  pycache, bytecode, log, PID file or payload file exists anywhere under
  CHANNEL_ROOT.
- Host-side NON-SECRET sender tool
  /home/isa/aucdev023-pch6b-credential-channel-20261004-01/bin/send_once.py
  (SHA-256 5d20d11fbdffc233ed6ef7f319ed9a6fcef9c0b2a0b90865963e26f30cf3d324,
  mode 0555): Python standard library only, socket path as sole argv operand,
  payload ONLY from stdin, connects exactly once to AF_UNIX/SOCK_STREAM,
  copies stdin to the socket, shutdown(SHUT_WR), closes, prints one fixed
  token (SEND_ONCE_OK), no retry loop, no content logging, no payload
  hashing/echo/persistence, never opens ~/.claude/.credentials.json or any
  credential store itself.  This preserves the future operator pattern: the
  operator's OWN shell redirects the credential file in as stdin so no
  credential byte ever appears in an agent command argument.

## 7. Live channel evidence (runtime only; AF_UNIX only)

- While the domain ran, the live dumpxml resolved the libvirt-managed source
  socket for the EXACT target channel to
  /run/libvirt/qemu/channel/1-aucdev-frevp-730d2b2/org.aucdev.pch6b.cred.a
  (belonging to target org.aucdev.pch6b.cred.a; address virtio-serial
  controller 0 bus 0 port 2; qemu device line: virtserialport nr=2
  name=org.aucdev.pch6b.cred.a on socket chardev server=on,wait=off).
- Guest side: /dev/virtio-ports/org.aucdev.pch6b.cred.a present (udev symlink
  to /dev/vport1p2, character special file major 0xf4 minor 2); open+fstat
  fd-class S_ISCHR verified True (device mode 0600).
- Host side: the socket is AF_UNIX SOCK_STREAM LISTEN (ss -lx), mode 0775
  owner libvirt-qemu:libvirt-qemu — EXACT PARITY with the established QGA
  channel socket on the same domain (no permission widening by this work);
  world holds NO connect/write permission on the socket, so it is neither
  world-writable nor world-connectable.
- NO TCP/UDP listening socket was introduced by this work: listening
  endpoint sets before define and after start are IDENTICAL for TCP and UDP
  (the diff is empty; the libvirt default-network dnsmasq endpoints on
  virbr0 pre-date this session and are the standard consequence of the
  UNMODIFIED historical NIC); the qemu process owns ZERO tcp/udp listeners.
  No vsock device exists in the domain.  No TCP fallback, vsock fallback,
  QGA credential carriage or real-credential test occurred at any time.

## 8. The synthetic end-to-end probe — FAILED; session STOPPED FAIL-CLOSED

- Probe definition: deterministic NON-SECRET synthetic probe (header line
  "AUCDEV023-SYNTHETIC-CHANNEL-PROBE-20261004-01\n" + sha256-chained blocks,
  exactly 8192 bytes, SHA-256
  81130ddeb4b97fe07750733d1cc9fc5729cf902eafe0f8fa88d47272a6dcb280).  It is
  NOT the rehearsal cred.bin and is NOT derived from any real credential.
  The identical generation algorithm is embedded in the ephemeral guest
  verifier, so NO probe bytes were ever written inside the guest.  Host-side
  consistency proven locally: gen_probe() output == probe.bin EXACT and the
  verifier through a pipe emits STDIN_IS_FIFO + VERIFY_PASS on the exact
  bytes.
- Probe topology (matching future source-fd semantics): host send_once.py
  (stdin = probe.bin via shell redirection) -> libvirt AF_UNIX socket ->
  virtio-serial guest device -> staged bridge.py -> OS PIPE -> ephemeral
  synthetic verifier stdin.
- The in-guest runner created the pipe, spawned the staged bridge with
  stdout = pipe write end and the ephemeral verifier with stdin = pipe read
  end.  The host sender was launched per the operator feed shape (shell
  redirection supplies stdin; the socket requires privilege, so the send ran
  under sudo — recorded as operator-feed metadata).
- OBSERVED OUTCOME (the single authorized probe connection, completed):
  send_once rc 0 with token SEND_ONCE_OK; bridge RC=0 with EMPTY stderr
  (clean stream + clean EOF, no failure token); verifier STDIN_IS_FIFO
  (the final consumer fd WAS a FIFO/pipe) but VERIFY_MISMATCH_FAIL with
  VERIFY_RC=1; runner PROBE_RESULT=FAIL (exit 1).
- DIAGNOSIS AT THE PERMITTED STRENGTH: the relayed stream did NOT equal the
  synthetic probe.  The token signature (bridge rc 0, empty stderr, FIFO
  pass, mismatch) is consistent with an EMPTY relayed stream.  Local
  re-derivation on IDENTICAL bytes proves the probe bytes, the generator,
  the verifier and the pipe wiring are mutually consistent, so the
  discrepancy arose in the live channel path.  The session's own earlier
  instrument actions on the live channel socket are the PRIME SUSPECT: a
  zero-byte root connect/close class probe performed BEFORE any guest
  consumer existed, and an unprivileged connect attempt that failed EACCES,
  either of which may have left the virtio port in a stale
  host-connected/disconnected state so the bridge's open/read completed with
  EOF before the real data connection.  ROOT_CAUSE_NOT_ESTABLISHED —
  verifying any hypothesis would require another channel connection, which
  the tasking forbids.
- FAIL-CLOSED DECISION: the tasking mandates "Use one connection.  No
  retries after a completed probe connection.  If the probe fails: STOP
  FAIL-CLOSED.  Do not switch transports."  One connection was consumed and
  FAILED; NO retry, NO second probe, NO transport switch, NO credential
  test, NO attempt execution occurred.  The channel artifacts were NOT
  erased (they remain staged, hash-bound, awaiting independent Control Room
  readback), and the event host was cleanly shut down and restored to its
  quiescent undefined state.
- ALLOWED-CLAIM BOUND: even the successful sub-steps are recorded at their
  exact strength — channel MECHANICS established as a CANDIDATE (design,
  successor XML, AF_UNIX transport, bridge staging, FIFO-shape proof token)
  with the end-to-end synthetic verification NOT PASSED.  NO claim of real
  credential delivery, CredentialCustody ingest, BootstrapAuthority
  constructor, run_attempt readiness, or Auditor-A attempt capability is
  made; CRED-001 is NOT closed.

## 9. CRED-001 state after the fail-closed outcome

AUCDEV023-CR-PCH6B-AUDITORA-CRED-001
CONFORMING_OPERATOR_CREDENTIAL_DELIVERY_CHANNEL_NOT_ESTABLISHED remains
OPEN / BLOCKING FUTURE AUDITOR-A EXECUTION.  Exact blocker recorded:

  AUCDEV023-CR-PCH6B-AUDITORA-CREDCH-001
  SYNTHETIC_END_TO_END_PROBE_VERIFIER_MISMATCH /
  RELAYED_STREAM_NOT_EQUAL_TO_SYNTHETIC_PROBE /
  SINGLE_CONNECTION_CONSUMED_NO_RETRY_PER_TASKING /
  CANDIDATE_CHANNEL_NOT_ACCEPTED
  (EXECUTION PREPARATION / CHANNEL VERIFICATION GAP / OBSERVED FACT; the
  host->AF_UNIX->virtio->bridge candidate channel did NOT deliver the exact
  synthetic bytes to the FIFO-shape consumer on the single authorized probe
  connection; bridge rc 0 with empty stderr is consistent with an empty
  relayed stream; ROOT_CAUSE_NOT_ESTABLISHED; prime suspect = this session's
  own pre-consumer zero-byte class connect on the live socket, an
  instrument-side action disclosed in §13; NOT a frozen-target product
  defect; NOT proof that the virtio-serial design, the bridge, the AF_UNIX
  transport or CredentialCustody is defective; future Auditor-A execution
  remains BLOCKED until a conforming channel is established AND
  synthetically verified AND independently read back under new explicit
  operator authority).

## 10. Negative gates (data-only, in-guest)

- PRE-WRITE gates 38/38 PASS before any CHANNEL_ROOT byte: canonical frozen
  runtime layout reverified DATA-ONLY with every frozen identity held
  (authority MANIFEST raw 7713b89e2618d27963be0df4dd5ebb33961a5b48c063c62ecacff2238da1425f,
  package_sha256 4399cb062e3fe9a5c4e6e71ad90e8515b3f0b462b6a648c458068cd6f01263db
  declared AND recomputed; Auditor-A binding raw
  36596c24f2a4a8bc56482cf19c989a7728ab5767720f5e946a1a2c25be91da80;
  Auditor-A package MANIFEST raw
  d48ae36b228b730bfad8138cb08af38cf34bb4fec954f948a17ba8e5f8dc5a46 with
  package abc6d34ae65069157e7bf9a09a939fb66877a77a6fdc57dcaa1c356337519744;
  every manifest-covered payload re-hashed 12/12 + 18/18; full runtime-root
  file-set equality, no __pycache__; canonical launcher
  8c40138f5ba1354cc095e988125ed14b3507e313eaa3a21f6cd86d6e691a4c04; pinned
  claude.exe 56fe3da88458465fb27d7e9299dddb3fead55750fb9c2de795f233b5eea6dce1;
  gates 1029e9c2 / b2407af1 / 034abc60, validator b38d12b5, wrapper
  705ca96a prefix, profile b552e40b each exactly once; modes/owners exact),
  CHANNEL_ROOT absent (collision gate), custody auditor-a-01 st_dev 33
  st_ino 60133 and auditor-b-01 st_dev 33 st_ino 60134 mode 0700 owner
  aucdev:aucdev BOTH EMPTY, whole custody tree only the two roots, all six
  reserved attempt artifacts ABSENT.
- POST-WRITE gates 33/33 PASS after the probe and before shutdown: the SAME
  frozen runtime layout unchanged (all identities re-verified DATA-ONLY);
  both custody roots still exact and EMPTY; six reserved artifacts still
  ABSENT; CHANNEL_ROOT present with EXACTLY bridge.py + channel.json (exact
  bytes/modes/owner; dirs 0555 root:root; no pycache/log/PID/payload); no
  bridge or daemon process running; NO real credential file anywhere in the
  guest; NO persistent synthetic payload under /tmp (ephemeral instruments
  removed after use).

## 11. Zero-attempt census

VM_RUNS = 1 (the ONE authorized bounded administration cycle);
CREDENTIAL_CHANNEL_ESTABLISHMENTS = 1 (candidate infrastructure: successor
XML + AF_UNIX virtio channel + guest bridge/channel.json staged);
SYNTHETIC_CHANNEL_PROBES = 1 (single completed connection — FAILED
verification; NOT retried);
REAL_CREDENTIAL_BYTES_USED = 0;
REAL_CREDENTIAL_CONTENT_READS = 0;
REAL_CREDENTIAL_BYTES_SENT = 0 (only the synthetic probe bytes traversed the
channel);
EVENT_INSTANTIATIONS = 0;
ATTEMPT_AUTHORITIES_GRANTED = 0;
BOOTSTRAP_AUTHORITY_IMPORTS = 0;
BOOTSTRAP_AUTHORITY_CONSTRUCTIONS = 0;
RUN_ATTEMPT_CALLS = 0;
ATTEMPT_ACCOUNTING_RECORDS_CREATED = 0;
REPORT_SINKS_CREATED = 0;
DYNAMIC_GATE_EXECUTIONS = 0;
BOUNDARY_LAUNCHER_EXECUTIONS = 0;
TOOL_WRAPPER_EXECUTIONS = 0;
VALIDATOR_EXECUTIONS = 0;
CLAUDE_EXECUTIONS = 0;
CODEX_EXECUTIONS = 0;
AUDIT_COUNCIL_EXECUTIONS = 0;
PROVIDER_MODEL_FRONTIER_REQUESTS = 0;
MODEL_ENGAGEMENTS_CONSUMED = 0;
FIRST_PASS_ARTIFACTS = 0;
QUALIFICATION = NONE;
INSTALLATION = NONE.
VM/administration operations, the data-only gate batteries and the synthetic
probe are reported separately and were never misclassified as an auditor
attempt.  Every verification was data-only (hashing, byte equality, JSON
parse, filesystem stat/listing, XML parse of SHA-verified bytes); the only
network operations are the ordinary Git/GitHub publication mechanics.

## 12. Event and authority governance (preserved)

EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 remains INSTANTIATED
(this fail-closed outcome created NO second event and revokes NOTHING);
PATH-B one-event slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT; reserved
Auditor-A attempt AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01
RUNTIME-UNCLAIMED; AUDITOR_A_ATTEMPT_AUTHORITY NONE; AUDITOR_B_ATTEMPT
AUTHORITY NONE; MODEL_ENGAGEMENTS_USED 0 (PROPOSED 2 unchanged);
FIRST_PASS_A ABSENT; AUCDEV-023 remains P1 / READY / NOT DONE; frozen target
730d2b29 AUDIT SUBJECT / NOT AUTHORITY; PCH6-B-SD-002 and PCH6-CR-BSD-001
AWAITING FRESH INDEPENDENT AUDIT / NOT CLOSED; PCH6-B-SD-001 RETAINED /
OPEN; ROOT_CAUSE_NOT_ESTABLISHED unchanged; INDEPENDENT_AUDITOR_PROVENANCE_GATE
NOT_SATISFIED with installed source 8ae33444f349ce73c1359b963722e2d16acba630;
installed Audit Council NOT AUTHORITY FOR THIS EVENT;
NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE DISCLOSED RESIDUAL; STAGING-RB-001
NONBLOCKING; the frozen external event root remains VALID append-only
MUST-NOT-be-rewritten and untouched; historical records/handoffs NOT
rewritten; prior closures RETAINED; NO audit execution; NO audit PASS;
QUALIFICATION NONE; INSTALLATION NONE.  No new attempt authority arises from
channel establishment or from this fail-closed outcome.

## 13. Honest iteration ledger (instrument-side; no failed observation
rewritten as PASS; every first output preserved in the untracked evidence
workspace aucdev023-pch6b-credchannel-evidence-20261004-01)

T-1 successor-XML builder v1 asserted the difflib insert zone with an
off-by-one point convention AFTER the byte-exact write (historical XML
untouched; successor bytes identical) — corrected expectation computes zones
BEFORE the write and re-asserts AFTER, and re-ran cleanly.
T-2 the semantic-diff normalizer v1 used bare C14N (single-line output) so
the unified diff showed whole-document replace — fixed by a deterministic
indent pass through the SAME transform on BOTH sides, re-derived from the
identical bytes.
T-3 the additions-shape assertion expected 1 line where the indented
canonical form uses 4 — corrected; zero-removal assertion already held.
T-4 the preserved-controller comparison sorted tuples with a missing model
attribute (None vs str) — corrected with an empty-string key; read-only.
T-5 the host-local pty stand-in proved UNSUITABLE for full-stream relay
(canonical-mode mangling; then racy close/drain EOF with input-queue drops;
one diagnostic recorded a byte-EXACT 16380-byte relayed prefix) — replaced
by a deterministic char-device battery (/dev/null empty-stream clean EOF,
/dev/zero hard-max cap, FIFO class refusal) 9/9 PASS; the synthetic probe
was resized 32768 -> 8192 bytes accordingly BEFORE staging; full exact-byte
relay on a real stream device was left to the single authorized probe.
T-6 the hard-max local test expected exit code 3 where the bridge design
returns 2 with the ERR_MAXBYTES token (tokens are the contract) — test
expectation corrected; instrument bytes unchanged.
T-7 guest-exec argv convention: two read-only probes passed the executable
path again as arg[0] (uname rc 1; gates exec ENOENT) — corrected arg lists;
no state impact.
T-8 locale artifact: host stat %F printed Turkish ("soket") — re-run under
LC_ALL=C; class facts unchanged.
T-9 the live-socket regex v1 greedily matched the QGA channel's source for
the credential channel — the paired assertion caught it; corrected to
extract within the target block.
T-10 the listener-diff v1 compared mismatched ss flag/column shapes —
recomputed with IDENTICAL command shapes and endpoint-set comparison; the
true diff is EMPTY for TCP and UDP.
T-11 (SUBSTANTIVE-DISCLOSURE) before any guest consumer existed, the session
performed a zero-byte root connect/close class probe on the live credential
channel socket to prove it connectable AF_UNIX, and one unprivileged connect
attempt that failed EACCES (the privileged send pattern was then adopted).
The zero-byte probe is the PRIME SUSPECT for the stale virtio-port state
that best explains the empty relay on the real probe; it was an
instrument-side action by THIS session and is disclosed here rather than
hidden; ROOT_CAUSE_NOT_ESTABLISHED (verification would require a forbidden
second connection).
T-12 the post-probe process-scan assertion matched its own scanner shell —
corrected to exclude self; scan clean.
T-13 the pre-write gate summary was asserted as 39/39 where the battery
genuinely contains 38 checks — count expectation corrected; the gate run
itself was rc 0 all-PASS on the first complete execution.
T-14 the synthetic probe itself FAILED (§8) — recorded as the substantive
fail-closed outcome, NOT rewritten, NOT retried.

## 14. Publication safety

Staged EXACTLY the three authorized documentation paths (NEW canonical
channel-establishment report; M CURRENT; M BACKLOG).  No channel helper or
source, no domain XML, no credential/auth/session material, no VM disk, no
accounting/report artifact, no .jsonl, no event-package tracked path and no
event-root file is committed to Git.  Repository drift (smoke-fixture /
smoke-fixture-103 gitlink rows plus pre-existing untracked entries)
preserved unstaged.  The queue was mechanically recounted base == staged on
every structural dimension; CURRENT top-level active state contains EXACTLY
ONE NEXT; disposition block token-for-token exact in the record; the
credential/secret mechanical scan is clean over the NEW record and all
diff-added lines; the full precommit gate battery ran from scratch on the
FINAL staged bytes and ALL PASSED; git diff --check and
git diff --cached --check PASS.

## 15. NEXT action — EXACTLY ONE (recording grants NOTHING)

INDEPENDENT CONTROL ROOM READBACK OF THE EXACT FAIL-CLOSED ZERO-ATTEMPT
CREDENTIAL-DELIVERY CHANNEL ESTABLISHMENT OUTCOME — INCLUDING THE FAILED
SYNTHETIC END-TO-END PROBE (SINGLE CONNECTION CONSUMED, NO RETRY), THE
RECORDED BLOCKER AUCDEV023-CR-PCH6B-AUDITORA-CREDCH-001, THE SUCCESSOR
DOMAIN XML, THE HOST-LOCAL AF_UNIX/VIRTIO CHANNEL EVIDENCE, THE GUEST
BRIDGE AND channel.json, THE NEW EVENT-HOST DISK CONTINUITY CHECKPOINT, THE
CUSTODY NEGATIVES AND THE GENERATED-LAST HANDOFF — BEFORE CRED-001 MAY BE
CLOSED, BEFORE THE CANDIDATE CHANNEL IS REUSED OR RE-PROBED, AND BEFORE ANY
NEW AUDITOR-A ATTEMPT AUTHORITY IS CONSIDERED.  Any channel re-probe,
channel redesign or channel teardown requires a NEW explicit operator
decision.  This publication does NOT authorize any probe retry, does NOT
close CRED-001, does NOT accept the candidate channel, does NOT authorize
Auditor-A or Auditor-B, does NOT call run_attempt, does NOT construct
BootstrapAuthority and does NOT consume a model engagement.

## 16. Standing prohibitions (unchanged)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from
an agent session absent an explicit single-use operator attempt authority
(and even then at most the ONE authorized call, never a second); never rerun
the launcher; never treat any recorded grant phrase (including any phrase
recorded here) as a new grant; never execute a real auditor or
provider/model; never open, read, hash, log or persist any real credential
byte; never open the four historical sealed artifacts (identity-only
forever); never relabel or rewrite historical model identities, runs,
records, matrices, prompts or evidence workspaces (append-only); never claim
audit PASS, qualification, installation or any authority from this
publication — it grants none; never rewrite or repack the frozen external
event root; never mutate the canonical runtime root or restage the event
host after event instantiation absent a separate explicit operator
remediation authority; never delete or repurpose the rehearsal-derived
artifacts under /srv/frevp/; never start or reopen the event-host VM from a
record-only session; and never run privileged mount/pivot_root/umount
experiments on the operator's live host and never automatically re-run an
interrupted privileged command — privileged GATE-W-prime boundary work
belongs in the disposable-KVM environment.
