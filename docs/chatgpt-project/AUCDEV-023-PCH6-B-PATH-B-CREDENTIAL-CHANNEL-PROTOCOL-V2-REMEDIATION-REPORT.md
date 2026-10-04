# AUCDEV-023 PCH6-B — Path-B credential-channel protocol remediation V2 and ONE fresh synthetic end-to-end verification — PASS — publication record

Remediation authority: AUCDEV-023-PCH6B-730D2B29-CREDCHANNEL-PROTOCOL-REMEDIATION-20261004-01 (narrow ZERO-ATTEMPT remediation of the EXISTING candidate credential-channel protocol for the EXISTING instantiated Path-B event AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 plus EXACTLY ONE fresh synthetic end-to-end verification, resolving the authorized scope AUCDEV023-CR-PCH6B-AUDITORA-CREDCH-RB-001 / CREDCH-RB-002 and, through the successful fresh verification, CREDCH-001; throughout the session AUDITOR_A_ATTEMPT_AUTHORITY = NONE, AUDITOR_B_ATTEMPT_AUTHORITY = NONE, MODEL_ENGAGEMENTS_USED = 0, RESERVED_ATTEMPT = RUNTIME-UNCLAIMED, RUN_ATTEMPT_CALLS = 0, BOOTSTRAP_AUTHORITY_CONSTRUCTIONS = 0, REAL_CREDENTIAL_BYTES_USED = 0, and the real operator credential was never even stat'ed — REAL_CREDENTIAL_STATS = 0).

## 1. Disposition — recorded at exactly the reached strength

AUCDEV_023_PCH6B_CREDENTIAL_CHANNEL_PROTOCOL_V2_REMEDIATION =
FRESH_SYNTHETIC_END_TO_END_VERIFICATION_PASS /
LIVE_BASE_C695648_VERIFIED /
PRE_REMEDIATION_EVENT_HOST_CONTINUITY_VERIFIED /
TRANSPORT_HELD_NO_REDESIGN /
HISTORICAL_CANDIDATE_ARTIFACTS_UNTOUCHED /
FRAMED_V2_PROTOCOL_IMPLEMENTED /
GUEST_READY_MARKER_BEFORE_SINGLE_HOST_CONNECT /
EARLY_EMPTY_READ_NOT_SUCCESS /
TRUNCATION_FAIL_CLOSED /
LOCAL_NON_LIVE_TESTS_42_OF_42 /
SOURCE_LEVEL_ONE_CONNECT_PROOF /
PREWRITE_GATES_48_OF_48 /
APPEND_ONLY_V2_STAGING_FOUR_FILE_SET /
NON_CONNECTING_SOCKET_DISCOVERY /
EXACTLY_ONE_HOST_CONNECT_ATTEMPT_ONE_COMPLETED /
BRIDGE_READY_FOR_HOST_BEFORE_CONNECT /
SEND_V2_OK /
BRIDGE_RC_0 /
VERIFY_STDIN_IS_FIFO /
VERIFY_PASS_EXACT_SYNTHETIC_PAYLOAD_EQUALITY /
PROBE_RESULT_PASS /
NO_SECOND_CONNECTION_NO_RETRY /
POSTWRITE_GATES_40_OF_40 /
REAL_CREDENTIAL_STATS_0 /
REAL_CREDENTIAL_CONTENT_READS_0 /
REAL_CREDENTIAL_BYTES_SENT_0 /
FROZEN_RUNTIME_UNCHANGED /
CUSTODY_IDENTITIES_HELD /
CUSTODY_ROOTS_EMPTY /
RESERVED_ATTEMPT_RUNTIME_UNCLAIMED /
AUDITOR_A_AUTHORITY_NONE /
AUDITOR_B_AUTHORITY_NONE /
BOOTSTRAP_AUTHORITY_IMPORTS_0 /
BOOTSTRAP_AUTHORITY_CONSTRUCTIONS_0 /
RUN_ATTEMPT_CALLS_0 /
MODEL_ENGAGEMENTS_USED_0 /
FIRST_PASS_A_ABSENT /
NO_AUDIT_EXECUTION /
NO_AUDIT_PASS /
QUALIFICATION_NONE /
INSTALLATION_NONE /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK

This disposition is NOT an audit verdict, establishes NO frozen-target product finding, and grants NO execution authority of any kind.  The remediation is IMPLEMENTED AS CANDIDATE; every remediated finding is recorded AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK / NOT_CLOSED — only the Control Room may close them at the supported readback strength.  No claim of real credential delivery, CredentialCustody ingest, BootstrapAuthority constructor, run_attempt readiness or Auditor-A attempt capability is made.

## 2. Role and boundary of THIS session

This session was the bounded IMPLEMENTER of the operator-authorized narrow zero-attempt protocol remediation and the ONE fresh synthetic verification.  It was NOT an Auditor-A or Auditor-B attempt executor, NOT an auditor, NOT an /audit-council executor, NOT a provider/model/frontier executor, NOT a qualification authority, NOT an installation authority, NOT the Control Room.  It performed NO BootstrapAuthority import or construction, NO run_attempt, NO attempt accounting creation, NO report-sink creation, NO dynamic audit gate, NO boundary launcher execution, NO Claude/Codex inference, NO provider/model request, NO model-engagement consumption, NO second event, NO frozen package rebuild, NO binding mutation, NO frozen-target mutation, NO external event-root mutation, NO redesign or teardown of the channel transport, NO mutation of the historical candidate artifacts, NO invocation of the historical bridge.py or send_once.py, NO CredentialCustody invocation, and NO qualification or installation.  No real credential byte was opened, stated, hashed, copied, read, sent, tested or otherwise touched: the real credential was never stat'ed by this session (REAL_CREDENTIAL_STATS = 0), and only deterministic SYNTHETIC non-secret bytes ever traversed the channel.

## 3. Live bootstrap and held governance (verified before any mutation)

- Live GitHub master == origin/master == local HEAD ==
  c69564897f3acd1e3e2e2ed6ff0e4d1363bcdf64 EXACT at bootstrap (fetch clean rc 0; ls-remote authoritative), root tree 541189215fc54e1af64d6fa7081d7eeb33eda8ec EXACT, sole parent 31d70a58cb45f1b01ef68fe9e029150a1195feb4 EXACT (single-parent fast-forward geometry); re-resolved EXACT after the VM/probe mutation immediately before staging (§34 rule).
- Trust anchor 3058868416241d394cfaaa40cc585085db486f37 ancestor rc 0.  Frozen audit target 730d2b29f7c0e7d33af3451b6d9205ec27c143ed (tree 2585796efd5cb6902226cfff785bb901297a15e3) present, ancestor, UNTOUCHED, AUDIT SUBJECT / NOT AUTHORITY.  Protected trees bootstrap-authority 154975872e15d53e1706016f5bb60c83727004f0 / bootstrap-supervisor 3056e577259ab0b0b0472f82ebc306506f3e084c / qualification-harness 5b8d5e5465923740470ff63ed9b8683f257a3787 / skill efd8c2e48edbb25795b3aacb1ce3c23fde10082a held EXACT at base and in the staged write-tree.
- The six mandated canonical records were read at the exact base with blob identities recorded (CURRENT dccf27a3044b0c0b8e986bd62ea6abe2343a1bf4 / BACKLOG e317d7e6ec3df668cce869cfe0500e6cd2e891f7 / channel-establishment CR readback d847129178a42351666793bc5f41e108fea4c2f3 / channel-establishment report 5c8ce6465eb970c8d16ead873f6ca49e5cdbae34 / runbook a1d27ed1431b024a9fb5f7e54bba8c71f1bc295a / protocol 42955b85710f09579cd0fd9174d042de231d060d) with the CURRENT/BACKLOG working copies verified byte-identical to the base blobs before editing.
- Held governance verified before any mutation: AUCDEV-023 P1 / READY / NOT DONE; EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 INSTANTIATED; PATH-B one-event slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT; reserved Auditor-A attempt AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01 RUNTIME-UNCLAIMED; Auditor-A attempt authority NONE; Auditor-B attempt authority NONE; MODEL_ENGAGEMENTS_USED 0 (PROPOSED 2 unchanged); FIRST_PASS_A ABSENT; CRED-001 OPEN / BLOCKING; CREDCH-001 OPEN / BLOCKING; CREDCH-RB-001 OPEN / BLOCKING; CREDCH-RB-002 OPEN / BLOCKING; ROOT_CAUSE_NOT_ESTABLISHED preserved; QUALIFICATION NONE; INSTALLATION NONE.
- Frozen CredentialCustody source contract read DATA-ONLY from the protected tree at the exact base (bootstrap-authority/bootstrap_authority/custody.py blob 37e6b5bb4365c7b29ba3632fe95362d5a7e16c09, NOT imported, NOT invoked): permitted plaintext sources a PIPE fd (stat.S_ISFIFO) or a fully-sealed memfd (all four seals); ordinary files/sockets/directories refused; MIN_CREDENTIAL_BYTES 1; MAX_CREDENTIAL_BYTES 65536.  The candidate architecture therefore preserves FINAL SOURCE CONTRACT = PIPE/FIFO FD (PIPE_FD_ON_FUTURE_DRIVER_STDIN).

## 4. Transport held — no redesign; historical artifacts untouched

- Transport RETAINED exactly: LIBVIRT_VIRTIO_SERIAL_HOST_LOCAL_UNIX with virtio target org.aucdev.pch6b.cred.a and guest device /dev/virtio-ports/org.aucdev.pch6b.cred.a.  The accepted successor domain XML /home/isa/aucdev023-pch6b-credential-channel-20261004-01/vm/credchannel-domain.xml was verified UNMODIFIED (SHA-256 065096925d43240b1c69b2f0c0ae976f7bd6202a30c11228c936e89ce40d30b3, 4417 bytes); no channel added, no TCP/UDP/IP listener, no vsock, no SSH, no QGA payload carriage, no env/argv payload carriage, no fallback transport.  QGA was used ONLY for non-secret guest administration and synthetic test orchestration.
- The EXISTING candidate artifacts are HISTORICAL and were NOT overwritten, deleted, renamed or invoked: guest bridge.py 46ce06dd9ac0a1c57712a6b8db750bd6f82f31dcdf989d5e323234b66ffeca0d (2787 B, mode 0555 root:root) and channel.json 025e0d743f89bbc9d8a4c31b2314b180b88c728889088415932040f7e0c34481 (664 B, mode 0444 root:root) under CHANNEL_ROOT /srv/aucdev-frevp-credential-channel/AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01/auditor-a, and host sender send_once.py 5d20d11fbdffc233ed6ef7f319ed9a6fcef9c0b2a0b90865963e26f30cf3d324.  Their identities were re-verified EXACT by the pre-write battery before staging and by the post-write battery after the probe.  The remediation is APPEND-ONLY.

## 5. Event-host continuity and the ONE bounded VM cycle

- Pre-session state: event-host domain aucdev-frevp-730d2b29-20261002-02 ABSENT (undefined, quiescent); rehearsal domain aucdev-gatew-730d2b29-20261002-01 shut off and untouched; host boot-id a2aec063-adc9-4342-9789-bc042d77bfc7 and mount count 84 recorded.  PRE-START work-disk SHA-256 verified EXACT = b0c5f958dbf069f0c0f0cc33eb0e49eaf8c4fd0de8f303c36607c17425d008b4 (the accepted post-channel continuity checkpoint).
- ONE bounded ordinary-VM-administration cycle only: defined from the exact accepted successor XML (both unix channels confirmed in the defined XML; exactly one virtio-serial controller), started 2026-10-04T12:17:14Z, QGA responsive after 4 pings, guest kernel 7.2.7-arch1-1 lineage EXACT, fresh guest boot-id c25d4161-b91d-49eb-893f-600a2f14cd5b recorded as event metadata, channel device present as udev symlink to /dev/vport1p2 character special file f4:2 mode 0600 with open+fstat fd-class S_ISCHR verified True in-guest (the exact check bridge-v2 performs at runtime), clean agent shutdown 2026-10-04T12:25:47Z, undefine restoring the pre-session undefined state.
- POST-REMEDIATION quiescent work-disk SHA-256 = f654a51ed49dd23cc42e5235953d648da74d49feda3b7991b8dab4507823da21 recorded as the NEW event-host continuity checkpoint (the disk change is the authorized consequence of the bounded cycle plus the staged V2 artifacts; equality NOT claimed; no reset/rollback/copy-over).
- Host non-mutation EXACT: boot-id and mount count 84 unchanged post-cycle; no socket persists while shut down (ss -lx verified absent); no mount/pivot_root/unshare/bwrap experiment; no live-host boundary execution.

## 6. FRAMED_V2 protocol (remediation of CREDCH-RB-002) — implemented as candidate

Exact framing used by BOTH bridge-v2 and send_once_v2 (identical constants, mechanically cross-checked):

  START_MAGIC = b"AUCDEV023-CRED-FRAME-V2\n"  (24 bytes: ASCII text + trailing 0x0A newline — the tasking's source-level \\n escape read as a newline byte, Ruling D)
  UINT32_BE payload length, accepted 1..65536
  payload bytes
  END_MAGIC   = b"AUCDEV023-CRED-END-V2\n"    (22 bytes)

- bridge-v2.py (SHA-256 93bb97b7af8a06bf56738c15cdb06a51bc063c81e748d8ef1df4ec3017af9fd3, 7958 B): Python standard library only; never imports bootstrap_authority; PR_SET_DUMPABLE=0 with PR_GET_DUMPABLE==0 verified BEFORE any channel byte is consumed; stdout stat.S_ISFIFO verified BEFORE payload handling; opens ONLY /dev/virtio-ports/org.aucdev.pch6b.cred.a read-only and verifies the fd is a character device; emits exactly one fixed NON-SECRET control token READY_FOR_HOST on stderr only AFTER all four preconditions PASS; then bounded readiness semantics — BEFORE the first frame byte an empty os.read means NOT_READY/DISCONNECTED, NEVER success, retried under a bounded monotonic deadline (default 30 s) ending in ERR_READY_TIMEOUT; once ANY frame byte has been received an empty read before the complete frame is ERR_TRUNCATED_FRAME (no revert to readiness waiting, no later connection accepted); malformed START_MAGIC / invalid length / malformed END_MAGIC each fail with their own fixed non-secret tokens; the payload is written to stdout ONLY after the COMPLETE frame validates; no payload hash, no content log, no payload-length log, best-effort overwrite of the mutable payload buffer before exit; exits after one frame; no daemon/listener/background service.  Optional argv overrides (device path, readiness window) exist ONLY for local instrument testing; the production invocation passes NO arguments (Ruling C).
- send_once_v2.py (SHA-256 1cc6e22efb1cec386d6edebcbb3f42e4feac1896c101d7c465b8dac569d6a8dd, 3954 B, host mode 0555): standard library only; non-dumpable verified BEFORE reading stdin; exactly ONE argv operand that MUST be an absolute AF_UNIX path; exactly ONE connect() call site with NO retry loop, NO fallback, NO connect_ex (AST-verified: the connect call is not enclosed by any loop); payload ONLY from stdin, read boundedly (at most 65537 bytes) ONLY AFTER a successful connect; sends exactly START_MAGIC + uint32_be(length) + payload + END_MAGIC; shutdown(SHUT_WR); close; prints exactly SEND_V2_OK; never hashes/logs/echoes/persists payload; never opens any credential store itself.  The orchestration invokes it ONLY after the guest readiness marker is independently observed.
- Readiness is established OUTSIDE the credential socket (no host-before-guest connection, remediating CREDCH-RB-001): the ephemeral guest probe_runner_v2.py requires the FIRST bridge stderr control line to be exactly READY_FOR_HOST and only then creates the fixed non-secret marker /tmp/aucdev-pch6b-cred-v2.ready (contents READY_FOR_HOST_V2, mode 0600; removed on exit); the orchestration polls that marker via QGA file reads — no socket connect may occur before it exists and NONE did.
- channel-v2.json (SHA-256 10e4db64ba8094e599bd934a829b0925ee65bdbe310d1fdf06da3613e927e102, 1489 B, mode 0444 root:root): schema AUCDEV-023-PCH6B-CREDENTIAL-CHANNEL-V2 with exactly the mandated NON-SECRET fields — event id, AUDITOR_A role, transport, virtio target, guest device, final source PIPE_FD_ON_FUTURE_DRIVER_STDIN, protocol version FRAMED_V2, START/END magic textual + hex + byte-length identities, max payload 65536, readiness model GUEST_READY_MARKER_BEFORE_SINGLE_HOST_CONNECT (window 30 s), early-empty behavior NOT_SUCCESS_BOUNDED_WAIT, post-frame-start EOF behavior FAIL_TRUNCATED, bridge-v2 and send_once_v2 SHA-256, historical bridge/channel.json SHA-256, real_credential_used false, run_attempt_authorized false, both attempt authorities NONE — and NO credential path or credential metadata (mechanically verified).

## 7. Local NON-LIVE protocol tests BEFORE staging (tasking §18)

The full battery ran from scratch on the FINAL source bytes: 42/42 PASS, rc 0 (evidence 05-local-v2-tests-FINAL.txt), using ONLY synthetic local in-memory/socket/pipe/raw-pty fixtures — the ONLY AF_UNIX listener used was a /tmp test fixture; the live credential-channel socket was never touched (Ruling B).  Covered: shared constants agreement (both magics identical across bridge and sender; 24/22 bytes; max 65536); unit framing cases (valid frame -> exact payload; first-empty-reads-then-frame NOT success; readiness deadline; malformed magic; truncated magic; truncated length; length 0; length 65537; truncated payload; malformed END_MAGIC; EOF after frame start before completion; complete 8192-byte synthetic payload exact; byte-at-a-time chunking; transient OSError pre-first-byte retried; OSError after frame start fails closed); subprocess cases against the REAL bridge binary (stdout not FIFO refused; non-char device refused; empty stream with small and with the PRODUCTION DEFAULT 30 s window -> READY_FOR_HOST then ERR_READY_TIMEOUT rc 3 at 0.52 s / 30.07 s); FULL-PATH raw-pty character-device relay (READY token emitted; complete 8192-byte synthetic payload relayed EXACT through a real char device with FIFO stdout, rc 0; malformed magic rc 5; truncated frame fails closed rc 4/9-class); sender cases (usage; relative path refused; stdin NOT read before connect — fast ERR_CONNECT on a never-written FIFO stdin; exact 8242-byte frame on the wire + SEND_V2_OK; empty payload refused; 65537-byte payload refused); source invariants (exactly one connect call site, no connect_ex call, connect not inside any loop, connect strictly before the stdin read in source order); runner fail-closed without a bridge (no marker created); generator/verifier identical derivation; V2 probe DISTINCT from the V1 probe; probe size 8192.

Synthetic probe: deterministic NON-SECRET 8192-byte payload, identity string AUCDEV023-SYNTHETIC-CHANNEL-PROBE-V2-20261004-01, construction = 64-byte zero-padded identity header + indexed sha256 block chain (generator gen_probe_v2.py SHA-256 5fbc639e46176e60dc29eceb1c62a638a7b1bfe3f214e5761f6ae25101acc14b); payload SHA-256 b71722a517cfa0f9b8d8b7b5bda2fba4bc4094330099f634454ce064e925d1f8, size 8192 — a construction and byte content DISTINCT from the previous failed V1 probe (81130ddeb4b97fe07750733d1cc9fc5729cf902eafe0f8fa88d47272a6dcb280); NOT the rehearsal cred.bin; NOT derived from any real credential; the identical algorithm embedded in the ephemeral guest verifier so no probe bytes were ever written inside the guest.

Source-level single-connect proof (tasking §17), run on the COMPLETE final helper set (bridge-v2, sender, runner, verifier, generator, both gate batteries, channel-v2 builder, qga library and every phase script): send_once_v2.py contains EXACTLY ONE .connect( call site; EVERY other helper contains ZERO; zero connect_ex calls anywhere; zero nc/netcat/socat invocations (the only textual matches are the scripts' own prohibition docstrings).  The proof was re-run after every later instrument patch (final scan 07-one-connect-proof-final.txt).

## 8. Pre-write gates (tasking §19) — 48/48 PASS

Before any V2 byte was staged, the data-only battery verified IN-GUEST: the accepted frozen runtime layout EXACT (authority MANIFEST raw 7713b89e2618d27963be0df4dd5ebb33961a5b48c063c62ecacff2238da1425f with package_sha256 4399cb062e3fe9a5c4e6e71ad90e8515b3f0b462b6a648c458068cd6f01263db declared AND recomputed; Auditor-A binding raw 36596c24f2a4a8bc56482cf19c989a7728ab5767720f5e946a1a2c25be91da80; Auditor-A package MANIFEST raw d48ae36b228b730bfad8138cb08af38cf34bb4fec954f948a17ba8e5f8dc5a46 with package abc6d34ae65069157e7bf9a09a939fb66877a77a6fdc57dcaa1c356337519744 declared AND recomputed; every manifest-covered payload re-hashed 12/12 + 18/18; full file-set equality; no __pycache__; canonical launcher 8c40138f5ba1354cc095e988125ed14b3507e313eaa3a21f6cd86d6e691a4c04; pinned claude.exe 56fe3da88458465fb27d7e9299dddb3fead55750fb9c2de795f233b5eea6dce1; gates 1029e9c2 / b2407af1 / 034abc60, validator b38d12b5, wrapper 705ca96a prefix, profile b552e40b each exactly once; modes/owners exact); Auditor-A custody auditor-a-01 st_dev 33 st_ino 60133 mode 0700 owner aucdev:aucdev EMPTY and Auditor-B custody auditor-b-01 st_dev 33 st_ino 60134 mode 0700 owner aucdev:aucdev EMPTY; whole custody tree only the two roots; all six reserved attempt artifacts ABSENT; CHANNEL_ROOT present with EXACTLY the historical bridge.py + channel.json (exact hashes/modes/owners above; dirs 0555 root:root; no pycache/log/PID/payload); bridge-v2.py ABSENT; channel-v2.json ABSENT; no stale readiness marker.

## 9. Append-only V2 staging (tasking §20) — exactly the four authorized files

Exactly TWO new files staged via the QGA file interface with byte-fidelity re-hash (guest sha == host sha EXACT for both): bridge-v2.py mode 0555 root:root and channel-v2.json mode 0444 root:root.  After staging the CHANNEL_ROOT persistent file set is EXACTLY bridge.py, channel.json, bridge-v2.py, channel-v2.json (verified by name, hash, mode and owner; find shows no other file under the channel tree; no pycache, payload, log or credential material).  The historical files were not overwritten.

## 10. Non-connecting socket discovery (tasking §15)

Live dumpxml resolved the libvirt-managed source socket for the EXACT target org.aucdev.pch6b.cred.a to /run/libvirt/qemu/channel/1-aucdev-frevp-730d2b2/org.aucdev.pch6b.cred.a; socket stat: socket 775 libvirt-qemu:libvirt-qemu (exact parity with the QGA channel socket; world holds NO connect permission); ss -lx shows it as an AF_UNIX SOCK_STREAM listener; read-only qemu query-chardev shows the credential chardev disconnected with frontend-open=false pre-probe while the QGA chardev is connected; the qemu command line shows the virtserialport for the exact target and NO vsock device.  NO connect(), connect_ex, netcat, socat, zero-byte connect/close or unprivileged connect test was performed.  NO TCP/UDP listener was introduced: the endpoint-set diff against the (re-captured, hardened) baselines shows added = EMPTY for TCP (75 -> 75) and for UDP (32 -> 21; eleven transient host-daemon UDP endpoints DISAPPEARED, none added — recorded as benign host drift), and the qemu process owns ZERO tcp/udp listeners.

## 11. The ONE fresh synthetic end-to-end verification — PASS

Sequence (tasking §24 D-J), with the connect census recorded at every step:

- Ephemeral instruments transferred through QGA with byte-fidelity re-hash: probe_runner_v2.py 27d6875b9f00beeafcab8ab0f94680c3796ba7c6bf6c1514c66a9139b3edb69c (4467 B) and probe_verify_v2.py f0c4c478521fca1f01884b824a8baf920f4b366e187a5a884e282edf471144b3 (1867 B); no probe bytes were written in the guest (the verifier re-derives the payload from the embedded algorithm).
- probe_runner_v2 started in the guest WITHOUT waiting (wrapper pid recorded, 2026-10-04T12:24:23Z).  (One earlier instrument-side launch failure is disclosed in §13-T14: the runner did not start at all due to a QGA argv-convention defect in the orchestration call site; the readiness gate then STOPPED FAIL-CLOSED with ZERO connect attempts, the §24 sequence had not begun, and no bridge/marker/channel byte existed.  The single-connection budget was and remains INTACT — the failed attempt consumed NOTHING.)
- GUEST READINESS established OUTSIDE the credential socket: the bridge emitted READY_FOR_HOST as its first and only stderr line; the runner created the marker; the orchestration polled the marker via QGA file reads and observed it at 2026-10-04T12:24:24Z with EXACT contents READY_FOR_HOST_V2.
- Runner and bridge processes verified alive DATA-ONLY (ps listing: wrapper 536, runner 538 python3 /tmp/probe_runner_v2.py, bridge 539 python3 .../bridge-v2.py).
- THE single host sender invocation — the ONE connect of the entire session — under sudo with shell-redirection-equivalent stdin (no payload byte in argv): send_once_v2 rc 0, stdout exactly SEND_V2_OK, empty stderr, 0.04 s.  HOST_CREDENTIAL_CHANNEL_CONNECT_ATTEMPTS = 1; HOST_CREDENTIAL_CHANNEL_COMPLETED_CONNECTIONS = 1.  No other socket connect occurred before or after it (source-level proof §7; no bridge/runner/phase helper contains any connect logic).
- Guest result: BRIDGE_FIRST_STDERR=READY_FOR_HOST; MARKER_CREATED=1; BRIDGE_RC=0; verifier VERIFY_STDOUT=STDIN_IS_FIFO|VERIFY_PASS; VERIFY_STDERR empty; VERIFY_RC=0; runner PROBE_RESULT=PASS.  The bridge stderr capture contains exactly READY_FOR_HOST — no error token, no secret or content output.
- ALL §25 PASS requirements hold: sender rc 0 + SEND_V2_OK; READY_FOR_HOST before host connection; exactly one connect invocation with no earlier successful or failed connect; bridge rc 0 with no secret/content output; verifier stdin stat.S_ISFIFO; VERIFY_PASS with EXACT synthetic payload equality through the live channel (host sender -> AF_UNIX socket -> virtio-serial -> bridge-v2 -> OS pipe -> verifier stdin); runner PROBE_RESULT=PASS; no framing/truncation error; no readiness timeout; no residual synthetic payload; readiness marker removed; ephemeral probe scripts removed after evidence capture (§12).  NO second connection and NO retry occurred or was attempted.

## 12. Post-probe negative gates (tasking §27) — 40/40 PASS

After the probe and before shutdown, with the ephemeral /tmp instruments already removed after evidence capture (final residual count 0): the frozen runtime layout UNCHANGED with every identity held; historical bridge.py/channel.json UNCHANGED; V2 files match their recorded hashes with modes 0555/0444 root:root; CHANNEL_ROOT exactly the four authorized files; custody auditor-a-01 st_dev 33 st_ino 60133 and auditor-b-01 st_dev 33 st_ino 60134 mode 0700 owner aucdev:aucdev BOTH EMPTY; whole custody tree no files; all six reserved artifacts ABSENT; readiness marker ABSENT; no bridge/runner/daemon process; NO real credential file anywhere in the guest; no synthetic payload or instrument under /tmp; channel-v2.json schema/authority fields exact with no credential metadata.

## 13. Honest iteration ledger (instrument-side only; no failed observation rewritten as PASS; every first output preserved in the untracked evidence workspace aucdev023-pch6b-credential-channel-remediation-20261004-01/evidence)

T-1 in-memory fake reader discarded bytes beyond each read cap — push-back buffer fix; T-2 not-char fixture used a FIFO whose read-only open correctly blocks — regular-file fixture; T-3 readiness-timeout expectation compared full stderr instead of the terminal line; T-4 raw-pty termios rebuild dropped the cc array; T-5 no-connect_ex scan matched the sender's own docstring — call-syntax regex; T-6 guest uname used the v1 arg list (argv append convention) — rc 1 "extra operand", fixed; T-7 qga_lib guest_sh/transfer passed the executable name as a first arg — rc 126 "cannot execute binary file"; convention pinned EMPIRICALLY (A-E battery preserved); T-8 baseline command built the INVALID flag string "-ltcpnp" via f-string (ss: invalid option -- 'c') with the udp sibling "-ludnp" — root cause established and ALL phase copies fixed; T-9 baseline capture recorded neither rc nor stderr (hid T-8) — hardened capture with retries; T-10 channel device path is a udev symlink — authoritative char-class check moved to the resolved target + in-guest open+fstat proof; T-11 stat %F wording variant ("character special file"); T-12 endpoint parser expected protocol-prefixed ss rows — vacuous empty-set diff; fixed to the actual LISTEN/UNCONN column shape and re-run with a real non-empty diff; T-13 abort-path status poll on a reaped QGA pid asserts — tolerant form; T-14 (SUBSTANTIVE-SEQUENCE DISCLOSURE) the first probe-runner launch used the old broken argv form at a call site bypassing the patched library — the runner NEVER STARTED, no output file, no bridge run, no marker, and the readiness gate correctly STOPPED FAIL-CLOSED with CONNECT_ATTEMPTS = 0 / COMPLETED = 0: the §24 sequence had not begun, no channel byte or connect existed, and the single-connection budget stayed INTACT; call site fixed, sequence restarted at §24.D and PASSED; T-15 four-file expectation literal in manual order vs sorted() comparison ('-' sorts before '.') — actual guest set was already exactly correct; T-16 the §27 battery ran before the /tmp cleanup — phase reordered cleanup-first; T-17 the battery's leftover scan matched its own file — self-exclusion + final zero-residual recount.  Rulings: A (§19 gates run in-guest after start but before staging); B (§18 local socket fixtures are authorized local-only sender tests; §14's forbidden list governs the LIVE socket); C (bridge argv overrides exist only for local instrument testing; production passes no arguments); D (the tasking's \\n read as the source-level newline byte; magics 24/22 bytes with hex identities recorded); E (bytes after a complete END_MAGIC are out of contract for the one-shot bridge); F (pty master-close mid-frame surfaces as EIO rc 9 — both fail closed; the deterministic truncation token proven at unit level).

## 14. Zero-attempt census (tasking §31)

VM_RUNS = 1 (the ONE authorized bounded administration cycle, 12:17:14Z - 12:25:47Z);
CREDENTIAL_PROTOCOL_REMEDIATIONS = 1;
FRESH_SYNTHETIC_CHANNEL_PROBES = 1 (PASS);
HOST_CREDENTIAL_CHANNEL_CONNECT_ATTEMPTS = 1;
HOST_CREDENTIAL_CHANNEL_COMPLETED_CONNECTIONS = 1;
REAL_CREDENTIAL_STATS = 0;
REAL_CREDENTIAL_CONTENT_READS = 0;
REAL_CREDENTIAL_BYTES_SENT = 0 (only synthetic bytes traversed the channel);
EVENT_INSTANTIATIONS = 0;
ATTEMPT_AUTHORITIES_GRANTED = 0;
BOOTSTRAP_AUTHORITY_IMPORTS = 0;
BOOTSTRAP_AUTHORITY_CONSTRUCTIONS = 0;
RUN_ATTEMPT_CALLS = 0;
ATTEMPT_ACCOUNTING_RECORDS_CREATED = 0;
REPORT_SINKS_CREATED = 0;
DYNAMIC_GATE_EXECUTIONS = 0;
BOUNDARY_LAUNCHER_EXECUTIONS = 0;
CLAUDE_EXECUTIONS = 0;
CODEX_EXECUTIONS = 0;
AUDIT_COUNCIL_EXECUTIONS = 0;
PROVIDER_MODEL_FRONTIER_REQUESTS = 0;
MODEL_ENGAGEMENTS_CONSUMED = 0 (PROPOSED 2 unchanged);
FIRST_PASS_ARTIFACTS = 0;
QUALIFICATION = NONE;
INSTALLATION = NONE.

VM/administration operations, the data-only gate batteries and the single synthetic probe are reported separately and were never misclassified as an auditor attempt.  Every verification was data-only (hashing, byte equality, JSON parse, filesystem stat/listing, XML/JSON parse of SHA-verified bytes, QGA file reads); the only network operations are the ordinary Git/GitHub publication mechanics plus the ONE authorized AF_UNIX channel connection carrying synthetic bytes.

## 15. Finding states after the successful fresh probe (tasking §29 — recorded, NOT closed here)

  AUCDEV023-CR-PCH6B-AUDITORA-CREDCH-RB-001
  PRECONSUMER_CONNECTION_VIOLATED_SINGLE_CONNECTION_PROBE_CONTRACT =
    IMPLEMENTED_AS_CANDIDATE /
    NO_PRECONSUMER_CHANNEL_CONNECTION /
    EXACTLY_ONE_FRESH_HOST_CONNECTION /
    AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK /
    NOT_CLOSED

  AUCDEV023-CR-PCH6B-AUDITORA-CREDCH-RB-002
  BRIDGE_DISCONNECTED_EOF_AMBIGUITY_NO_READINESS_FRAMING =
    IMPLEMENTED_AS_CANDIDATE /
    V2_BOUNDED_READINESS_AND_EXPLICIT_FRAMING_ESTABLISHED /
    EARLY_EMPTY_READ_NOT_SUCCESS /
    TRUNCATION_FAIL_CLOSED /
    AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK /
    NOT_CLOSED

  AUCDEV023-CR-PCH6B-AUDITORA-CREDCH-001
  SYNTHETIC_END_TO_END_PROBE_VERIFIER_MISMATCH =
    FRESH_SYNTHETIC_END_TO_END_VERIFICATION_PASS /
    IMPLEMENTED_AS_CANDIDATE /
    AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK /
    NOT_CLOSED

  AUCDEV023-CR-PCH6B-AUDITORA-CRED-001
  CONFORMING_OPERATOR_CREDENTIAL_DELIVERY_CHANNEL_NOT_ESTABLISHED =
    IMPLEMENTED_AS_CANDIDATE /
    CONFORMING_PIPE_SHAPE_AND_SYNTHETIC_PAYLOAD_DELIVERY_MECHANICALLY_DEMONSTRATED /
    REAL_CREDENTIAL_NOT_USED /
    AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK /
    NOT_CLOSED

Only the Control Room may close these at the supported readback strength.  This session does NOT independently declare closure, does NOT accept the candidate channel for real credential use, and does NOT authorize any future Auditor-A attempt.  ROOT_CAUSE_NOT_ESTABLISHED for the historical V1 failed run remains preserved as recorded by the prior readback (the fresh V2 run does not retroactively establish the V1 root cause; it establishes the V2 candidate's own observed PASS).

## 16. Governance after remediation (tasking §32)

EVENT AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 remains INSTANTIATED; PATH-B one-event slot BOUND_TO_THIS_EVENT / NO_SECOND_EVENT; reserved Auditor-A attempt AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-01 RUNTIME-UNCLAIMED; AUDITOR_A_ATTEMPT_AUTHORITY NONE; AUDITOR_B_ATTEMPT_AUTHORITY NONE; MODEL_ENGAGEMENTS_USED 0; FIRST_PASS_A ABSENT; AUCDEV-023 remains P1 / READY / NOT DONE; frozen target 730d2b29 AUDIT SUBJECT / NOT AUTHORITY; PCH6-B-SD-002 and PCH6-CR-BSD-001 AWAITING FRESH INDEPENDENT AUDIT / NOT CLOSED; PCH6-B-SD-001 RETAINED / OPEN; INDEPENDENT_AUDITOR_PROVENANCE_GATE NOT_SATISFIED with installed source 8ae33444f349ce73c1359b963722e2d16acba630; installed Audit Council NOT AUTHORITY FOR THIS EVENT; NETWORKED_BOUNDARY_HOST_NETNS_EXPOSURE DISCLOSED RESIDUAL; STAGING-RB-001 NONBLOCKING; the frozen external event root remains VALID append-only MUST-NOT-be-rewritten and untouched; historical records/handoffs NOT rewritten; prior closures RETAINED; NO audit execution; NO audit PASS; QUALIFICATION NONE; INSTALLATION NONE.  No execution authority arises from this remediation.

## 17. Publication safety

Staged EXACTLY the three authorized documentation paths (NEW canonical V2 remediation report; M CURRENT; M BACKLOG).  No fourth tracked path.  No channel helper or source, no channel-v2.json, no send_once_v2, no domain XML, no synthetic payload, no VM image, no credential/auth/session material, no accounting/report artifact, no .jsonl, no event-package tracked path and no event-root file is committed to Git.  Repository drift preserved UNSTAGED.  The queue was mechanically recounted base == staged on every structural dimension; CURRENT top-level active state contains EXACTLY ONE NEXT; the disposition block is token-for-token exact in the record; the credential/secret mechanical scan is clean over the NEW record and all diff-added lines; the hex-literal gate PASSed with every >=7-char boundary-delimited non-decimal hex literal in the NEW record and diff-added lines machine-verified case-insensitively against the session-derived independently-verified identity allow-set (decimal-only and verified short prefixes/dash-segments exempt), which mechanically subsumes the sealed-identity no-NEW-occurrences gate; the full precommit gate battery ran from scratch on the FINAL staged bytes and ALL PASSED; git diff --check and git diff --cached --check PASS.

## 18. NEXT action — EXACTLY ONE (recording this NEXT grants NOTHING)

INDEPENDENT CONTROL ROOM READBACK OF THE EXACT CREDENTIAL-CHANNEL V2 PROTOCOL REMEDIATION AND THE ONE FRESH SYNTHETIC END-TO-END VERIFICATION, INCLUDING THE CONNECTION-COUNT EVIDENCE, V2 READINESS/FRAMING SOURCE, SYNTHETIC PROBE RESULT, EVENT-HOST CONTINUITY CHECKPOINT, CUSTODY NEGATIVES AND GENERATED-LAST HANDOFF, BEFORE CRED-001 OR CREDCH FINDINGS MAY BE CLOSED AND BEFORE ANY NEW AUDITOR-A ATTEMPT AUTHORITY IS CONSIDERED.

This publication does NOT close CRED-001, CREDCH-001, CREDCH-RB-001 or CREDCH-RB-002; does NOT accept the candidate channel for credential use; does NOT authorize Auditor-A or Auditor-B; does NOT call run_attempt; does NOT construct or import BootstrapAuthority; does NOT consume a model engagement; and any channel re-probe, further protocol change, teardown or real-credential use requires a NEW explicit operator decision.

## 19. Standing prohibitions (unchanged)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from an agent session absent an explicit single-use operator attempt authority (and even then at most the ONE authorized call, never a second); never rerun the launcher; never treat any recorded grant phrase (including any phrase recorded here) as a new grant; never execute a real auditor or provider/model; never open, read, hash, log or persist any real credential byte (and never stat it in a remediation session); never open the four historical sealed artifacts (identity-only forever); never relabel or rewrite historical model identities, runs, records, matrices, prompts or evidence workspaces (append-only); never claim audit PASS, qualification, installation or any authority from this publication — it grants none; never rewrite or repack the frozen external event root; never repack the historical generated-LAST handoff archives; never mutate the canonical runtime root or restage the event host after event instantiation absent a separate explicit operator remediation authority; never delete or repurpose the rehearsal-derived artifacts under /srv/frevp/; never start or reopen the event-host VM or connect to the candidate credential channel from a record-only session; and never run privileged mount/pivot_root/umount experiments on the operator's live host and never automatically re-run an interrupted privileged command — privileged GATE-W-prime boundary work belongs in the disposable-KVM environment.
