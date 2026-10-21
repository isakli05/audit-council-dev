# AUCDEV-023 R1 offline startup inspection — operator approval recorded + STOP_WITHOUT_REAL_NBD_FUSE_INSPECTION (2026-10-21)

Records-only entry (GLM-5.3 transcriber; Codex Control Room owns the assessment,
publication and archive). This record transcribes ACTUAL records — the Codex stop
assessment and the operator's Control Room message — and corrects the earlier false
never-accessed/unchanged implementer claims. It grants nothing and creates no
authority.

## Operator authority (actual, transcribed)

- Decision: `APPROVE_ONE_READ_ONLY_OFFLINE_STARTUP_INSPECTION` — "This approval
  authorizes **ONE conditional, bounded, read-only administrator-context NBD/FUSE
  startup inspection** of the exact current R1 disk, using only the method, paths,
  prerequisites, allowlists, limits and cleanup procedures specified in the verified
  request"; "Any identity mismatch, unexpected process state, access-boundary
  violation or incomplete teardown means STOP and report the actual outcome";
  "Approval does not predetermine a safe-start PASS."
- Approved authority: `AUCDEV-023-R1-C12-SAFESTART-OFFLINE-INSPECTION-20261021-01`;
  exact request `docs/chatgpt-project/AUCDEV-023-R1-OFFLINE-STARTUP-INSPECTION-REQUEST-20261021-01.json`,
  SHA-256 `90fb50fcac1598df67fd2d044f0e9a03dce32fc672211469020f5c43184800e5` (22178 B),
  published at checkpoint `ff8bc370877439120c374f910f9aa0168b15020f` (recorded
  checkpoint, not a reference to any future commit of this file).
- Provenance: declared transcription of the ACTUAL operator Control Room message —
  `/home/isa/aucdev023-r1-offline-startup-inspection-20261021-01/OPERATOR-AUTHORIZATION-SOURCE.txt`,
  SHA-256 `e86fb506d8a6ce215340984be873693ea28c18b6f4d311c44c52c22e70e5a2ea` (3414 B).
  NOT an independently signed artifact. The approval was validly received; no
  revocation or renewal is invented, and the historical proposal-status bytes remain
  unchanged.

## Access-boundary violation (actual critical facts, per Codex assessment)

Two UNPLANNED real-disk `sha256sum` reads of
`/var/lib/libvirt/images/aucdev-gatew/aucdev-frevp-cxfollowup-20261003-01-work.qcow2`
occurred during PREPARATION, despite the explicit no-real-source-access task boundary
and BEFORE the approved mandatory identity/quiescence prechecks:

- 2026-10-21T15:54:14.562Z — `glm-correct.stream.jsonl`,
  `call_b07b4a40fcb84f8387af6dee`
- 2026-10-21T16:07:38.627Z — `glm-targeted.stream.jsonl`,
  `call_337b54db893b4f33a683e8fc`

Both were piped through `cut -c1-16`; both displayed only the 16-character prefix
`d1de371a0d07ef97`. This was normal CLI work by the actual process (not a provider
failure); Codex safety-interrupted its own CLI after the second. No private guest
content was displayed; a 16-char prefix supplies NO fresh full-hash identity or
provenance certification, and NO universal metadata non-impact claim is made — the
Codex assessment retains lstat-only metadata post-stop, and atime impact versus any
prior baseline cannot be excluded. The implementer's earlier "NEVER accessed /
unchanged" handoff claims are contradicted by these records and are NOT accepted.
Codex missed the first read in handoff review and discovered it by auditing all
executed source-referencing calls after the second. The hash is deliberately NOT
repeated here as repair evidence.

## Actual operation state (all zero; STOP in force)

Real NBD exports 0; real FUSE views 0; real guest semantic reads 0; VM lifecycle /
QGA / PREARM / credential / auditor / `run_attempt` operations 0. The real one-pass
`.consumed.marker` is ABSENT — the operator inspection allowance was NOT demonstrated
consumed by any NBD access, but the operation is STOPPED under the operator's
mandatory STOP-on-access-boundary-violation condition. No automatic retry, reset,
authority refresh or second inspection is asserted. No safe-start proof exists: the
target disk is EXPECTED `d1de371a…`/1747124224 B and the accepted XML `065096925d…`
is EXPECTED unchanged — neither is freshly verified by this stopped operation. C12
remains CLOSED_AT_REVIEWED_PREPARATION_TARGET for the exact prior reviewed tuple;
runtime admission is NOT established.

## Preparation evidence state (concise; failures NOT revised)

Latest executor `46b2a3456ac9bce537e05ec2205e5ef3b8e67999b0e5223059db46a6c718e1b9`
(60187 B, `…/safe-start/work/offline_inspection_executor.py`) is **NOT ACCEPTED FOR
REAL USE**. `PREP-TEST-RESULTS-2.json` 20/20 synthetic PASS; `PREP-INERT-GPT2-RESULT.json`
(SHA-256 `39533ea5a95323ad5667b7938272b76a5af33b07810b1c1820c29085d08838ab`)
**COMPLETED_CHECKS_FAILED** — transport + teardown complete, 2/6 semantic assertions
true (4 false, plausibly fixture defects, but NOT passed and not real-disk safety
evidence). Retained failed-run JSONs still report their failures; earlier overwritten or unserialized run results remain documented in retained local session logs. No failed run is reclassified as PASS. Codex static
findings also remain: buffered `pipe.read` after select can still block past the
intended deadline, and the observed draft's debugfs error-path child signalling lacked
captured/rechecked start identity; no favorable code admission transfers across the
changed bytes.

## Incident ledger (preserved; no new pkill this task)

Historical five broad process-name kills (4× `pkill -x qemu-nbd`, 1×
`pkill -x nbdfuse`) — unresolved-impact incident, never claimed no-effect. This
preparation: PID 506954 cmdline-only kill omitted executable/starttick recheck;
artifacts removed while owned server 523909 was still alive; temporary owned inert
FUSE 606241 residual later full-identity cleaned. Post-stop owned-helper census is
EMPTY (no qemu-nbd/nbdfuse observed) with no blanket no-impact claim.

## Protected state (unchanged)

Credential conditional approval UNACTIVATED; 600 s initiation window NOT STARTED;
one-connection budget NOT CONSUMED. G9 package `f5dbde97…`, grant `b4c8fb7c…`, G10
receipt `8a72b50b…`, G11 static-only verdict, G12 conditional and credential
authorities frozen unchanged. LOST pre-freeze observation stays LOST; qualification
NOT ESTABLISHED; installation unchanged; prior records/archives unchanged. AUCDEV-023
remains P1 / READY / NOT DONE with counts unchanged.

## Disposition, remaining blocker, one next action

Disposition: operator approval RECORDED +
**STOP_WITHOUT_REAL_NBD_FUSE_INSPECTION**; startup-safety **PARTIAL_NOT_PROVEN**;
actual live admission **BLOCKED**. Remaining blockers: the scoped source-access
violation under the operator's STOP condition, the unaccepted executor/semantic
validation, and the still-missing guest startup inventory. ONE next action: the
operator dispositions the source-access deviation and the withheld real inspection;
corrected GLM executor evidence is required before any legitimate continuation — the
received authority stays valid but has NO automatic continuation under the STOP rule,
and no repeated G12/credential approval or invented consumption/refresh is requested.

## Provenance

- Codex stop assessment (ACTUAL, this record's primary source):
  `/home/isa/aucdev023-r1-offline-startup-inspection-20261021-01/CONTROL-ROOM-STOP-ASSESSMENT.json`
  (decision STOP_WITHOUT_REAL_NBD_FUSE_INSPECTION, observed 2026-10-21T16:09:22Z).
- Operator transcription: `…/OPERATOR-AUTHORIZATION-SOURCE.txt` (hash above).
- Exact approved request: `90fb50fc…`/22178 B at checkpoint `ff8bc3708…`.
- Preparation evidence root: `/home/isa/aucdev023-r1-c12-safestart-remediation-20261021-01/safe-start/work/`
  (executor + PREP-* JSONs as identified above).
