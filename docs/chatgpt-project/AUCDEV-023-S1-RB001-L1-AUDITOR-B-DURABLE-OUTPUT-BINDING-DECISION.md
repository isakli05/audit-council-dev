# AUCDEV-023 S1 RB-001 L1 — AUDITOR-B DURABLE OUTPUT BINDING: CONTROL ROOM REMEDIATION-DECISION PUBLICATION

Authority (of THIS publication): `AUCDEV-023-S1-RB001-L1-B-DURABLE-OUTPUT-BINDING-DECISION-20260924-01`
Date: 2026-09-24 (Europe/Istanbul)

THIS SESSION IS A ZERO-PROVIDER CONTROL ROOM GOVERNANCE / REMEDIATION-DECISION PUBLISHER ONLY. It records the Control Room decision reached from the already-published execution mechanical readback (`AUCDEV-023-S1-RB001-L1-FIRSTPASS-EXECUTION-MECHANICAL-READBACK-20260924-01`) and additional exact frozen-client static evidence. It did NOT implement the remediation and did NOT: execute any model/provider/client (codex, claude, boundary launcher, operator driver/wrapper — not even `--help`); read Auditor-A report substance; create a replacement event or attempts; prepare replacement packages; grant replacement execution authority; qualify; install. ZERO provider/model execution; network activity = the mandated git ls-remote/push of this publication ONLY.

---

## 1. Live bootstrap (verified before any mutation)

- Repository `isakli05/audit-council-dev`, branch `master`.
- Authorized baseline `b5185497676babae855a5cd46a01031198424813` — EXACT (local HEAD and live `git ls-remote --symref origin HEAD`).
- Root tree `0fe5a84e73b0d6f3c030399e869460c799adb1bc` — EXACT; sole parent `0b4334be60e5bd869f8a6de8f1e1faa23a91e56a` — EXACT.
- Canonical blobs at the base: CURRENT `b68c5a1e7729eda4863807bc1571930411d2c9d9`; BACKLOG `e8757335175a8740f3794931597fd96ba959ba11`; execution mechanical readback `5694d2c526e83f0ca1c2a7271d1f6cf6312973d9` — ALL EXACT.
- Protected trees: `bootstrap-supervisor` `732b8def9f22d7c466ce77f3d3049da53bfff3d0`; `qualification-harness` `5b8d5e5465923740470ff63ed9b8683f257a3787`; `skill` `c792933a862d9a5434681a88d183470dd8b15d2f` — ALL EXACT.
- Tracked working tree: only the pre-existing smoke-fixture gitlink drift, preserved unstaged.
- Live master re-resolved EXACT immediately before staging (§17).

## 2. Execution-readback handoff — verified read-only

`/home/isa/audit-council-dev/AUCDEV-023-S1-RB001-L1-FIRSTPASS-EXECUTION-MECHANICAL-READBACK-HANDOFF.tar.gz`

- Outer SHA-256 `e58b9c17815d4f5593eb83acbeba7035c14d8cfe937b02b1136a471b33afb2fd` / 714369 B — EXACT.
- Census: 23 members = 23 regular files, 0 unsafe/traversal, 0 duplicates, 0 symlinks, 0 hardlinks, 0 special — EXACT.
- Exactly one SHA256SUMS: 22 rows, 22/22 PASS, zero missing, zero unlisted — EXACT.
- Packaged Git blob identities EXACT: canonical execution readback `5694d2c5…`; resulting CURRENT `b68c5a1e…`; resulting BACKLOG `e8757335…` (verified with the repository's SHA-1 blob formula; one initial mismatch in this session's own first check was a session-side SHA-256-vs-SHA-1 computation error, corrected here — no artifact discrepancy).
- No member executed; no Auditor-A report substance present or read (identity-only references throughout).

## 3. Additional exact frozen-client static evidence (§4 of the authority)

Preparation handoff verified read-only: `/home/isa/aucdev023-s1-rb001-l1-successor-package-prep-20260923-01/handoff/AUCDEV-023-S1-RB001-L1-SUCCESSOR-PACKAGE-PREPARATION-HANDOFF.tar.gz` — outer SHA-256 `8d179b5a3a7253162e1d0ecc9dfed2855d0a73e1a9a1479acfd3a2ca7364f0a1` / 233404608 B — EXACT (the accepted artifact lives in the preparation workspace handoff directory; the authority's suggested repo-root path does not exist).

Frozen Auditor-B executable member `package-auditor-b/payload/runtime/codex-0.154.0-linux-x64/bin/codex`:

- SHA-256 `3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022` — EXACT; size 262858016 B — EXACT.
- **NOT EXECUTED.** Verification was read-only static byte/string inspection, streamed in memory from the archive (zero extraction to disk, zero execution of any byte).

Mechanically observed embedded CLI string table (single occurrence each):

1. **`output-last-message`** (exactly 1 occurrence, file offset 215518414) — adjacent clap CLI metadata: value name `LAST_MESSAGE_FILE` / env-style `last_message_file`, with the embedded description **`Specifies file where the last message from the agent should be written`** — exactly the expected description. The same region embeds the `codex exec [OPTIONS] [PROMPT]` usage string.
2. **`output-schema`** (exactly 1 occurrence, file offset 215518198) — adjacent metadata: value name `OUTPUT_SCHEMA` / `output_schema`, with the embedded description **`Path to a JSON Schema file describing the model's final response shape`** — identifying a JSON Schema file for the model's final response shape.

**This is STATIC CLIENT-CAPABILITY EVIDENCE ONLY. It is NOT proof that either option caused or would have prevented the historical B event.**

## 4. Held EXEC-RB-001 disposition (unchanged)

`AUCDEV023-CR-S1-RB001-L1-EXEC-RB-001` — AUDITOR_B_EXIT0_REPORT_MISSING_AFTER_PROVEN_CLIENT_EXECUTION — remains EXACTLY: COMPLETENESS LIMITATION / FAILURE-DIAGNOSTIC EVIDENCE GAP / OBSERVED FACT / MANDATORY_SECOND_FIRST_PASS_MISSING / **ROOT_CAUSE_UNRESOLVED** / NO_AUDIT_COUNCIL_PRODUCT_DEFECT_CONCLUSION_YET. It is NOT rewritten as proven harness causality, proven model behavior, proven external condition, or proven provider defect. The observed event-level root cause remains unresolved.

## 5. Historical B invocation fact (from the executed frozen binding and published readback)

Executed Auditor-B frozen invocation: `codex exec --skip-git-repo-check --profile aucdev023-c3 <first-pass instruction>` (argc 6). The report pathname `/auditor-output/evt-f3136c29213a1d4d-B-01.first-pass-report.json` existed ONLY in the natural-language first-pass instruction. There was NO deterministic Codex CLI output-file binding. The frozen boundary simultaneously: mounted `/auditor-output` as the ONE host-backed writable output bind; used `/auditor-output` as client cwd; discarded composition stdout to `subprocess.DEVNULL`. The historical event mechanically observed: `client_exec_reached = true`; `returncode = 0`; `report_state = REPORT_MISSING`; custody-out EMPTY; staging EMPTY. Existing GATE-W-prime evidence proves the exact transport composition CAN write a report through `/auditor-output` with deterministic mock transport — channel capability, NOT proof that the historical real B turn performed the model-directed file-write action.

## 6. NEW CONTROL ROOM FINDING — `AUCDEV023-CR-S1-RB001-L1-EXEC-RB-002`

Title: **AUDITOR_B_DURABLE_REPORT_PATH_NOT_MECHANICALLY_BOUND**

Classification: **HARNESS / PROTOCOL DEFECT / STATICALLY OBSERVED / EXECUTION-COMPLETENESS RISK / EVENT-CAUSALITY NOT PROVEN / REMEDIATION_REQUIRED_BEFORE_ANY_REPLACEMENT_EXECUTION**

Observed support:

1. The adopted output-custody requirement requires exactly one canonical first-pass report under `/auditor-output`. (OBSERVED — frozen binding `output_identity` + boundary one-rw-bind discipline.)
2. The historical B invocation did not mechanically bind the Codex client's final message to the canonical report pathname. (OBSERVED — frozen argv, argc 6.)
3. The report pathname appeared only in natural-language instructions. (OBSERVED.)
4. Boundary stdout was intentionally discarded. (OBSERVED — `stdout=subprocess.DEVNULL` in the frozen launcher.)
5. Therefore durable report production depended on the auditor/model performing an instructed filesystem write rather than on a deterministic client output binding. (FOLLOWS from 1–4.)
6. The exact frozen Codex 0.154.0 client exposes a native `output-last-message` file-destination capability. (STATICALLY OBSERVED — §3 above.)
7. The historical invocation did not use that capability. (OBSERVED — frozen argv.)

**Causality non-claim:** THIS FINDING DOES NOT ESTABLISH THAT THE ABSENCE OF `output-last-message` CAUSED THE HISTORICAL REPORT_MISSING EVENT. EXEC-RB-001 remains ROOT_CAUSE_UNRESOLVED. The finding instead establishes that the harness/protocol left mandatory durable report delivery unnecessarily dependent on model-directed tool behavior despite an available pinned-client mechanism for deterministic final-message persistence.

## 7. Control Room decision

`AUCDEV_023_S1_RB001_L1_EXEC_RB001_CONTROL_ROOM_DECISION =`

**EXEC_RB_001_ROOT_CAUSE_UNRESOLVED_PRESERVED / EXEC_RB_002_HARNESS_PROTOCOL_DEFECT_ESTABLISHED / EXTERNAL_AUDITOR_CONDITION_NOT_PROVEN / BOUNDED_HARNESS_PROTOCOL_REMEDIATION_REQUIRED / NO_REPLACEMENT_EXECUTION_AUTHORITY / NO_MODEL_EXECUTION / QUALIFICATION_NONE / INSTALLATION_NONE**

The next path is NOT `EXTERNAL_AUDITOR_CONDITION_DISPOSITION` (available evidence does not prove an external auditor/client condition). The next path IS **BOUNDED HARNESS / PROTOCOL REMEDIATION** (a distinct mechanically demonstrated delivery-binding defect exists).

## 8. Minimum remediation direction — DECISION ONLY (no implementation in this task)

The future remediation MUST be the smallest change closing EXEC-RB-002. For the Auditor-B Codex invocation, bind the final client message directly to the canonical output identity using the exact frozen client's native option:

```
--output-last-message /auditor-output/<EXACT-B-ATTEMPT>.first-pass-report.json
```

Future exact argv shape is expected to be semantically:

```
codex exec --skip-git-repo-check --profile aucdev023-c3 \
  --output-last-message /auditor-output/<EXACT-B-ATTEMPT>.first-pass-report.json \
  <neutral first-pass instruction>
```

The final implementation task MUST determine and freeze the exact ordered argv. The path MUST equal `"/auditor-output/" + binding.output_identity.name` exactly and appear exactly once. The invocation remains digest-covered and event-package-bound.

## 9. Explicit non-goals of the first remediation

DO NOT: add `--output-schema`; capture or persist stdout; change stdout DEVNULL behavior; alter the first-pass report schema; alter the structural validator; change credential handling; change sandbox roots; change network policy; change tool-domain wrapper behavior; change target source; change `qualification-harness/**`; change `skill/**`; read prior Auditor-A substance; reuse the historical event; reuse historical attempts; grant execution authority. Rationale: the existing structural validator already provides fail-closed schema validation (so `--output-schema` would be an additional behavior change not required to close the demonstrated durable-delivery binding invariant), and persisting stdout would create a new substantive output surface and is unnecessary.

## 10. Future zero-provider acceptance requirements

A future remediation implementation must mechanically prove, with ZERO real provider/model inference:

- **A.** exact frozen Codex executable identity remains `3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022`;
- **B.** the exact future B `auditor_invocation` contains `--output-last-message` exactly once;
- **C.** its following path equals the exact bound output identity under `/auditor-output/`;
- **D.** no stale historical B attempt/output pathname remains in an active invocation;
- **E.** the exact invocation remains binding-digest and package-manifest covered;
- **F.** the existing GATE-W-prime deterministic mock transport is rerun/adapted against the EXACT remediated invocation and proves: the real pinned Codex client starts; the final mock agent response is persisted at the exact canonical output path; the report reaches the existing validator/custody lifecycle; no real provider/model inference occurs; the outside-write negative control remains refused; the no-profile negative control remains refused as applicable;
- **G.** stdout remains non-authoritative and discarded;
- **H.** the existing report validator remains the sole structural acceptance authority after the client writes the durable final message.

## 11. Replacement-event governance (ONE EVENT / SINGLE USE / NO REVIVAL)

- Historical execution authority `AUCDEV-023-S1-RB001-L1-FIRSTPASS-EXEC-20260923-01` remains CONSUMED / TERMINAL / CLOSED / NO_RERUN.
- Historical event `evt-f3136c29213a1d4d` remains historical and MUST NOT be revived.
- Historical Auditor-A report remains SEALED / UNREAD and MUST NOT be transferred as the Auditor-A half of a future successful event; it remains valuable historical evidence only.
- Successful-event semantics require BOTH required first-pass reports under ONE exact event identity.
- Any eventual post-remediation real execution requires: a NEW event identity; fresh A-01 attempt; fresh B-01 attempt; common-evidence parity re-established for that event; first-pass blindness re-established; a fresh total model-engagement budget of 2; a NEW explicit human operator execution authority. **No such event or authority is created by THIS decision.**

## 12. Remediation mutation boundary (decision; does NOT predetermine implementation files)

The subsequent implementation task must first identify the smallest actual generation/configuration surface responsible for the Auditor-B frozen invocation. Preferred scope: the event-package / binding / generation logic necessary to introduce the exact `output-last-message` binding and its zero-provider validation. Avoid `bootstrap-supervisor` source changes unless mechanically necessary; do NOT broaden `bootstrap-supervisor/**` merely to encode a one-event configuration invariant if the invariant can be enforced in the frozen event binding / identity-linter / package-preparation surface. Any trust-boundary source change that proves necessary must be called out and separately reviewed.

## 13. Resulting state

- `AUCDEV023-CR-S1-RB001-L1-EXEC-RB-001`: OPEN / ROOT_CAUSE_UNRESOLVED (held).
- `AUCDEV023-CR-S1-RB001-L1-EXEC-RB-002`: OPEN / HARNESS_PROTOCOL_DEFECT / REMEDIATION_REQUIRED.
- Executed authority `AUCDEV-023-S1-RB001-L1-FIRSTPASS-EXEC-20260923-01`: CONSUMED / TERMINAL / CLOSED / NO_RERUN.
- Audit completeness: INCOMPLETE. Qualification readiness: BLOCKED_BY_MISSING_MANDATORY_AUDITOR_B_FIRST_PASS. Qualification: NONE. Installation: NONE.
- AUCDEV-023: P1 / READY / NOT DONE (queue counts unchanged: READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11; EXEC-RB-002 is tracked within AUCDEV-023's existing open item).
- Next frontier: BOUNDED ZERO-PROVIDER IMPLEMENTATION OF EXEC-RB-002 DURABLE OUTPUT BINDING, FOLLOWED BY CONTROL ROOM READBACK BEFORE ANY NEW EVENT PREPARATION OR EXECUTION AUTHORITY.

## 14. Expected tracked mutation

Exactly three tracked paths: this NEW decision record; `AUCDEV-CURRENT-STATE.md`; `AUCDEV-BACKLOG.md`. Nothing else. No runtime, package, or event mutation; no model execution.

## 15. NEXT ACTION — EXACTLY ONE

**CONTROL ROOM PREPARATION OF A BOUNDED ZERO-PROVIDER EXEC-RB-002 IMPLEMENTATION PROMPT THAT MECHANICALLY BINDS AUDITOR-B CODEX FINAL OUTPUT TO THE EXACT `/auditor-output/<attempt>.first-pass-report.json` PATH USING THE PINNED `output-last-message` CLIENT OPTION, WITHOUT YET PREPARING A NEW REAL EVENT OR GRANTING ANY REPLACEMENT EXECUTION AUTHORITY.**
