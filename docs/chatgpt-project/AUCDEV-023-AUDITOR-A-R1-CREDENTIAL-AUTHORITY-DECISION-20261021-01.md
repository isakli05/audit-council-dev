# AUCDEV-023 Auditor-A R1 credential delivery — ACTUAL operator decision record (2026-10-21, nonsecret)

One short canonical record of the ACTUAL operator decision on the exact
separate credential-delivery authority request. Recorder: GLM-5.3 bounded
record-only implementer; Codex Control Room owns independent review, ordinary
non-force Git publication and the single final sanitized archive. This record
grants nothing on its own and triggers nothing.

## Exact approved request identity (verified this session at local HEAD)

- Path: `docs/chatgpt-project/AUCDEV-023-AUDITOR-A-R1-CREDENTIAL-AUTHORITY-REQUEST-20261021-01.json`
- Canonical bytes: SHA-256 `014eda5dad2a89bc3a11ad420cbfeee6ff53ec4fc01931a8962bbce54c4a0b68`, 8882 bytes
- Git blob `9e8831680e0789d576ef94842b6fdfc2f5eb63dc` — working tree == index == HEAD `957379ccb4da8742e93fc793270dd2709990abb9` (the request publication commit; parent `b2872137d5597ec95136ce1a6ffca3fdc9cd342d`).
- The request file itself is UNCHANGED by this decision: its `status` `PENDING_OPERATOR_NO_AUTHORITY_ISSUED` and `operator_decision: null` remain the historical proposal state; no approval was written into it. This separate record is the sole decision artifact. (A Git file cannot contain its own future publication SHA; `957379c…` is the last verified checkpoint at recording.)

## Actual operator decision

- Decision: `APPROVE_CONDITIONAL_ONE_SHOT_CREDENTIAL_DELIVERY`
- Credential authority ID (confirmed exactly as proposed): `AUCDEV-023-CRED-DELIVERY-AUDITOR-A-R1-20261021-01`
- Operator-confirmed exact request SHA-256: `014eda5dad2a89bc3a11ad420cbfeee6ff53ec4fc01931a8962bbce54c4a0b68` (matches the verified file above)
- Existing binding: governance event `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01`, auditor role `AUDITOR_A`, attempt slot `AUDITOR_A_REPLACEMENT_1`, attempt `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-R1`
- Sole provenance: the operator's actual reply received in the 2026-10-21 Codex Control Room operator conversation and forwarded verbatim in the GLM-5.3 implementation task; transcribed (including its BEGIN/END EXACT OPERATOR MESSAGE conversation guard lines) at `/home/isa/aucdev023-credential-decision-20261021-01/OPERATOR-DECISION-SOURCE.txt` — SHA-256 `9d33962c613eeb24bd57ed111ca21a0d260d1cc6fa72db58b89561043b54a7e0`, 2704 bytes. That file is a CONVERSATION TRANSCRIPTION, NOT a separately signed artifact; none was created or inferred, and no permission is claimed from any JSON field, token, marker or Codex assessment.

## Disposition: CONDITIONAL_OPERATOR_APPROVAL_RECORDED_NOT_ACTIVATED

Approval is RECORDED ONLY. It is NOT live admission and NOT permission to
execute, and it satisfies no then-live prerequisite by itself. Actual
credential delivery NOT_OCCURRED. The operator reply and this record do NOT
authorize VM/QGA operations, auditor execution, Auditor-B, qualification or
installation, and waive no G12 condition and no mandatory then-live
preflight/PREARM check.

## Approved one-shot scope (exactly the request's, unchanged)

ONE fresh live R1-bound PREARM session (bound before any credential access) →
ONE `OPERATOR_SEND_NOW` go-marker → ONE sender invocation → ONE host AF_UNIX
connect attempt (a FAILED first connect also consumes the one-connect budget)
→ ONE FRAMED_V2 credential transfer through the accepted waiter/sender/bridge
channel only. The ≤600 s limit is an authority-scope initiation/wait window
only, not a channel-protocol change. While UNUSED, the permission expires at
the session deadline/death/boot, on identity change, refusal or revocation;
the first valid invocation consumes it for the ONE in-flight frame, which
neither expiry nor consumption interrupts midway; no retry, second connect,
replacement attempt, authority refresh or automatic delivery is permitted.
The operator alone controls the credential source; no credential source path
or material appears in this record or the transcription (the request by
design contains none).

## Current activation state (no clock started)

- Initiation window: NOT_STARTED — it begins only with the future freshly
  bound live R1 PREARM session, NOT with the operator reply or this record.
- One-shot budget: NOT_CONSUMED.
- No real nonce, PID, PREARM session, go-marker, sender invocation, connect
  or transfer was created by this task; zero VM/QGA/channel/marker operations
  were performed.
- Current code preparation remains READY_FOR_THEN_LIVE_CHECK; all class-C
  then-live checks remain NOT_PERFORMED (no synthetic or preparation result
  became a live fact).

## Unchanged context (existing identities, not re-derived here)

G12 conditional decision record `b2872137d5597ec95136ce1a6ffca3fdc9cd342d`
(`AUCDEV-023-G12-EXEC-AUDITOR-A-R1-20261020-01`,
APPROVE_CONDITIONAL_SINGLE_ATTEMPT) and the G11 static-only verdict
`d3546f1c664604f3a284ab56aa80bca00650c990` unchanged; grant identity
`b4c8fb7c41af4fedf51108ac75056c6dd12cdcd5649e3d36e9dd7e758191cbde`, package
`f5dbde97148cf585aa4d13da4235471c61166e2f36bc877c52b99aeaca6138e2`, receipt
`8a72b50bae5f59e9e8ef1e5128e167f7aa92afe564e925cdd16069e9fa4d4482`
unchanged; the LOST original pre-freeze observation stays LOST (no backdated
or recreated proof); installed qualification NOT_ESTABLISHED; no release,
qualification, installation or Auditor-B engagement; prior archives, reports,
final checklist and protected history untouched. This record supersedes only
the pending-operator state of the 2026-10-21 preparation report's blocker 4;
that preparation report remains historical and unchanged.

## Remaining blocker (single)

Separately valid authority for the then-live VM/QGA/preflight/PREARM
operations and the actual fresh live checks. The operator credential approval
recorded here and the G12 conditional decision need not be repeated.
