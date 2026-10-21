# AUCDEV-023 R1 live VM/QGA preflight — actual authority + live results record (2026-10-21)

One short combined record of the ACTUAL bounded live preflight authority and its
live results. Recorder: GLM-5.3 technical implementer; Codex Control Room owns
independent review and Git publication. Grants nothing beyond the recorded
facts; no execution authority is created here.

## Actual authority (transcribed, not re-derived)

- Authority ID (adopted after uniqueness check): `AUCDEV-023-R1-VMQGA-LIVE-PREFLIGHT-20261021-01`
- Provenance: the operator's actual reply in the 2026-10-21 Codex Control Room
  operator conversation, forwarded verbatim in the GLM-5.3 task. Transcription
  (delimiters `-----BEGIN/END EXACT OPERATOR MESSAGE-----` declared and
  preserved inclusive): `/home/isa/aucdev023-r1-live-preflight-20261021-01/OPERATOR-AUTHORIZATION-SOURCE.txt`
  — SHA-256 `77edb374297f5a77f9c11a5dd21494e43127da6c7b96c7cbb13ab11ee76df594`;
  embedded operator-message extract SHA-256 `8ed4939130690ff00bce2e5eb5bdfbd46b0ec07ec1e89d89c4027f4b8565d740`.
  Conversation transcription, NOT a signed artifact. The BEGIN/END lines are
  TASK-FORWARDING DELIMITERS present in the forwarded Codex task text, declared
  by the recorder — not original operator text and not a signature boundary;
  transcription bytes are unchanged by this clarification, which is recorded
  here only.
- Uniqueness bounded to the actually searched records: 0 hits in the tracked
  tree at HEAD `ddc8e25693b8d97d33d569b183b3d6cbbf318443` and 0 in full Git
  history (`git log --all -S` exact ID and prefix class); the only occurrences
  found in that searched scope are this task's own records (excluded). No
  claim is made about records outside the searched scope.
- Exact target: repo `isakli05/audit-council-dev`, expected/verified HEAD
  `ddc8e25693b8d97d33d569b183b3d6cbbf318443` (local == `git ls-remote origin
  master`), attempt `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-R1`;
  G12 `AUCDEV-023-G12-EXEC-AUDITOR-A-R1-20261020-01` and credential
  `AUCDEV-023-CRED-DELIVERY-AUDITOR-A-R1-20261021-01` NOT repeated.

## Live results (evidence JSON: `/home/isa/aucdev023-r1-live-preflight-20261021-01/LIVE-PREFLIGHT-EVIDENCE.json`)

Disposition: **LIVE_PREFLIGHT_PARTIAL**. Source/host identity checks passed
with exact identities; one REAL-XML compatibility finding is OPEN; live
guest-side checks are BLOCKED (no running guest, no start issued); nothing
attempt-relevant was consumed; no synthetic value substitutes any live fact;
protected-boundary admission remains FAIL_CLOSED until all real prerequisites
are met.

- Static identities re-verified EXACT (read-only; gate never
  executed/imported/chmod'd): procedure `32460cd5…`, binding `801279b5…`, gate
  `410b1410…` 20535 B 0500/uid1000/nlink1 with THIS session's fresh ctime
  observation `2026-10-05T15:26:43.323396086+03:00`, verifier `3f4438e9…`,
  waiter `b0ec4e7e…`, sender source `1cc6e22e…`, package `f5dbde97…`/593920,
  receipt `8a72b50b…`/622, G12 request `086b4ea0…`/4759, credential request
  `014eda5d…`/8882 (decision stays RECORDED_NOT_ACTIVATED), reviewed launcher
  `076cab42…` 3716 B 0500/uid1000/nlink1 (fresh ctime 2026-10-21T10:56:19+03),
  interpreter `/usr/bin/python3.14` `dd65a07e…`, host seam `/usr/bin/virsh`
  `525c340f…`/976608 0755/uid0 — identity re-observed read-only. Read-only
  libvirt QUERY invocations of that binary occurred (list/dominfo/domuuid
  below); the PROTECTED seam surface (`virsh qemu-agent-command` guest-exec)
  was never invoked; no blanket zero-execution claim is made for that binary.
- Live domain identity/state (read-only `virsh -r -c qemu:///system`, single
  bounded invocations 2026-10-21T12:23:01Z): exact bound event host
  `aucdev-frevp-730d2b29-20261002-02` UNDEFINED — exactly the accepted
  quiescent baseline (every accepted session ended define→use→shutdown→undefine);
  only the rehearsal domain `aucdev-gatew-730d2b29-20261002-01` exists (UUID
  `22d95782-8525-4c80-aa77-3200d34721f4` EXACT, shut off, autostart disabled).
- Accepted successor XML identity EXACT: `credchannel-domain.xml`
  `06509692…`/4417 B; name/UUID == authorized identity
  (`d8d26fc1-15dc-4602-989c-ea40ec50010e`); QGA channel `org.qemu.guest_agent.0`
  present; credential channel `org.aucdev.pch6b.cred.a` present (host-initiated
  only); on_poweroff/on_reboot/on_crash = destroy; no qemu:commandline hooks.
  Raw XML never exposed; sanitized identity fields + hash only.
- Work disk identity EXACT: `aucdev-frevp-cxfollowup-20261003-01-work.qcow2`
  1747124224 B, SHA-256 `d1de371a0d07ef97fd1d55c794c9a05a4972b9119f3f55fda86e119dbbda321e`
  == latest accepted post-attempt checkpoint; mtime 2026-10-04 18:50:36+03;
  unchanged, not substituted.
- BLOCKED (live): QGA availability and guest-runner identity — no running
  guest; live runtime-root staging NOT_PERFORMED_LIVE (then-live collector
  duty). PASS (static): QGA topology; correlation namespace regex
  `^AUCDEV023-PREARM-OPADOPT-V1-[A-F0-9]{32}$` matches active-v3 exactly (no
  session started); seam/argv derivation contract (guest-exec `/bin/sh -c`
  validated runner; `--connect <uri> qemu-agent-command <domain> <payload>`).
- FINDING (C12, OPEN — REAL-XML compatibility, current reviewed adapter): the
  current reviewed adapter `4702daac…` `_observe_domain` requires the staged
  live snapshot bytes to carry `id='…'`, `<event_id>`, `<attempt_id>` matching
  R1 exactly; genuine libvirt XML for this domain (accepted `06509692…`, 4417 B)
  contains none of these elements, so a FAITHFUL RAW dumpxml snapshot is
  INCOMPATIBLE with the current adapter (it is refused with
  `domain_cross_attempt_identity`). This tag-embedding shape is a property of
  the current reviewed adapter, NOT a requirement of active-v3 itself —
  active-v3 separately requires domain identity + live XML digest and exact
  attempt binding but does not prescribe embedding these tags in libvirt XML.
  Resolution requires an explicitly reviewed R1-domain binding integration
  compatible with genuine libvirt XML and the exact existing attempt, OR a
  separately accepted changed XML with new identity; any code/target change
  needs exact new byte pins and appropriate fresh review, with no silent
  inheritance of old favorable evidence or approved-request pins. A collector
  must NOT append fabricated R1 tags to, or substitute altered/synthetic XML
  for, genuine live dumpxml. No fix implemented; no verdict manufactured here.

## Conditional ONE VM start — decision (explicit)

Genuinely necessary: YES. Startup-safety prerequisite: **NOT_ESTABLISHED** for
the CURRENT disk generation `d1de371a…` (post-attempt bytes). XML topology (no
qemu:commandline hooks; destroy on poweroff/reboot/crash), the
host-initiated-only seam/credential-channel design, and accepted historical
read-only boot cycles are SUPPORTING METHOD EVIDENCE ONLY, on EARLIER disk
generations
(`2312cfe9…`/`6a77fb5a…`/`f654a51e…`/`800531cf…`); none of the inspected
accepted records proves the absence of guest boot services, autorun scripts
or other startup triggers on the exact current `d1de371a…` bytes, and no new
live/guest/mount/appliance/device operation was performed to look for proof. A
VM-cycle scope approval alone would NOT cure this unmet condition. Definition/
cleanup scope: the exact bound domain is currently UNDEFINED, and the accepted
historical method for every event-host use is define-from-exact-XML → ONE
start → read-only checks → clean shutdown → undefine restoration; whether the
ordinary persistent definition/cleanup mechanics of that method are covered by
the current single-conditional-start authorization is an UNRESOLVED CONTROL
ROOM BOUNDARY INTERPRETATION that must be reconciled with the exact authorized
scope BEFORE any such mutation — recorded here as facts and interpretation,
not as a binding contract quote and not as the only blocker; no fresh-human
-approval requirement for those mechanics is invented and none presumed
satisfied. **No start condition satisfied; NO start issued** (and no
define/undefine/reboot/reset/destroy/replacement). G12 and credential
approvals remain valid and need no repetition. The boundary and unresolved
prerequisites are named below rather than spending the attempt.

## Protected-boundary status (no permission manufactured)

This preflight is preliminary live-readiness only; it is NOT a final fresh
session and NOT the immediately-used same-process fd-bound PREARM. Still
unresolved before the protected boundary (no single approval assumed to remove
all gaps; admission stays FAIL_CLOSED until every real prerequisite is met):
(1) BOTH of — (a) reconciliation of the event-host definition/cleanup
mechanics (define from accepted XML `06509692…` → ONE start → read-only QGA
identity queries → clean shutdown → undefine restoration) with the exact
authorized scope (Control Room boundary interpretation, not the only blocker),
AND (b) the mandatory startup-safety (no-autotrigger) prerequisite for the
CURRENT disk `d1de371a…`, NOT_ESTABLISHED — a VM-cycle approval alone does not
cure it without accepted proof covering the exact current disk or fresh
then-live verification per the applicable contract; (2) the C12 REAL-XML
compatibility gap — explicitly reviewed R1-domain binding integration
compatible with genuine libvirt XML and the exact existing attempt, or a
separately accepted changed XML with new identity, with exact new byte pins
and appropriate fresh review (no collector tag-fabrication, no
altered/synthetic XML as live dumpxml, no silent inheritance of old evidence);
(3) the boundary operations themselves — fresh correlation + R1-bound PREARM
session, real verifier admission exactly once, immediate fd-bound execve,
fresh gate ctime/XML-digest/guest-runner/runtime-root/QGA observations — none
of which any preflight result replaces; (4) credential activation stays
UNACTIVATED (window NOT_STARTED, budget NOT_CONSUMED). Forbidden here and not
performed: operational PREARM gate, waiter/sender/connection,
OPERATOR_SEND_NOW, guest shell/guest-exec, auditor/model execution,
run_attempt, any package/grant/receipt/attempt mutation.

## Unchanged

G12 `b2872137…` / G11 `d3546f1c…` verdicts, grant `b4c8fb7c…`, GRANT_ISSUED
`83cc20a3…`, package/receipt identities, the LOST pre-freeze observation
(stays LOST), installed qualification NOT_ESTABLISHED, five protected trees,
all prior workspaces/archives/reports. AUCDEV-023 remains **P1 / READY /
NOT DONE**. The checklist's historical PENDING_OPERATOR credential section is
superseded by the recorded `ddc8e25…` decision; no other checklist/history
rewrite.
