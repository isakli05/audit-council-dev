# AUCDEV-023 S1 RB-001 L1 RB-002 EXEC-RB-004 Single-Writer Implementation (Candidate Remediation)

- **Implementation authority**: `AUCDEV-023-S1-RB001-L1-RB002-EXEC-RB004-SINGLE-WRITER-IMPLEMENTATION-20260924-01`
- **Finding addressed**: `AUCDEV023-CR-S1-RB001-L1-RB002-EXEC-RB-004` — `AUDITOR_B_CANONICAL_REPORT_PATH_DUAL_WRITER_COLLISION` (published with the EXEC-RB-003 dual-writer diagnostic at commit `a6966012…`)
- **Date**: 2026-09-24 (Europe/Istanbul)
- **Session role**: BOUNDED ZERO-PROVIDER IMPLEMENTER — NOT the Control Room decision-maker, NOT Auditor-A/B, NOT an execution controller, NOT a replacement-event preparer, NOT an execution-authority grantor, NOT a qualification authority, NOT an installation authority.

## 1. Disposition

```
EXEC_RB_004_IMPLEMENTATION =
CANDIDATE_REMEDIATION_IMPLEMENTED /
EXEC_RB_002_DETERMINISTIC_CANONICAL_BINDING_PRESERVED /
DUAL_AUTHORITATIVE_WRITER_ROLE_REMOVED /
CODEX_FINAL_MESSAGE_IS_CANONICAL_REPORT /
ROLE_A_UNCHANGED /
FROZEN_VALIDATOR_UNCHANGED /
ZERO_PROVIDER /
NO_REAL_EVENT /
NO_EXECUTION_AUTHORITY
```

**EXEC-RB-004 is NOT CLOSED.** The finding remains `OPEN / CANDIDATE_REMEDIATION_IMPLEMENTATED_PENDING_CONTROL_ROOM_READBACK` (previously `OPEN / REMEDIATION_REQUIRED`); closure requires independent Control Room readback of this publication and its generated-LAST handoff.

## 2. Live base (mandatory bootstrap, EXACT)

- Repository `isakli05/audit-council-dev`, branch `master`.
- Base commit `a6966012192c238c77c22eb101e490e36154361d`, root tree `2d7396930713e45c53f1cb1f87d8441eafaf6fa5`, sole parent `fea4ccb93bbd2d9b2f4c0f9d9bb52f7bf6799564` — resolved EXACT locally AND as live GitHub `refs/heads/master` at bootstrap (fail-closed; no drift; no auto-rebase).
- Canonical blobs at the base verified EXACT: CURRENT `1181e3fc2e6a879ec014728770d58a76533e5ab4`, BACKLOG `7aeaa3b9240de62f01dd0fbd6963b1e37515668e`, EXEC-RB-003 diagnostic `65514b5d63010945a7ad982b4056598c78e075f7`, execution mechanical readback `507c14c49315a4cede787fa7565a7d7226d80ad9`, historical EXEC-RB-002 implementation `a39e577ae5781646566a88bb4e189a719630c5d2`.
- Protected trees byte-unchanged: `bootstrap-supervisor` `732b8def9f22d7c466ce77f3d3049da53bfff3d0`, `qualification-harness` `5b8d5e5465923740470ff63ed9b8683f257a3787`, `skill` `c792933a862d9a5434681a88d183470dd8b15d2f`; tracked working-tree drift limited to the two pre-existing smoke-fixture gitlink entries (preserved unstaged, per protocol).

## 3. Cross-finding constraint honored

```
EXEC_RB_004_CROSS_FINDING_CONSTRAINT = DO_NOT_REOPEN_EXEC_RB_002
```

EXEC-RB-002 was closed specifically because the canonical Auditor-B durable report output became mechanically bound to the frozen Codex client (`--output-last-message`). The current EBS `Supervisor.run_attempt` lifecycle snapshots ONLY the supplied canonical `report_staging_path` (`snapshot_staging` → credential screen → frozen validator → freeze canonical bytes); there is NO promotion/copy operation from a separate last-message file to the canonical report path. Therefore a distinct-last-message-path-only patch would make the canonical report dependent again on model-directed tool/filesystem writing and would REGRESS the closed EXEC-RB-002 invariant.

**This implementation therefore REFINES the EXEC-RB-003 diagnostic's initial "distinct last-message path" example remedy** (the diagnostic record is NOT rewritten; its remediation direction was a DECISION-ONLY example, not an accepted design). The implemented terminal contract instead satisfies BOTH invariants simultaneously:

- **I1 — EXEC-RB-002 deterministic delivery (preserved)**: the terminal canonical Auditor-B report bytes are mechanically written to the exact canonical report path `/auditor-output/<output_identity.name>` by the pinned frozen Codex client through `--output-last-message` (exactly once, destination unchanged, `--output-schema` still forbidden).
- **I2 — EXEC-RB-004 semantic single-writer custody (new)**: the natural-language Auditor-B instruction NO LONGER designates that pathname as a model/tool-written report artifact.

```
AUTHORITATIVE_CANONICAL_REPORT_SOURCE      = CODEX_FINAL_AGENT_MESSAGE
AUTHORITATIVE_CANONICAL_REPORT_PERSISTENCE = --output-last-message
```

The canonical pathname remains `/auditor-output/<attempt>.first-pass-report.json`; no second authoritative writer role targets it. No separate `.last-message.txt` production artifact exists in this candidate.

## 4. Prompt-contract preflight (§5)

Frozen accepted Auditor-B `transport/prompt-contract.json` located and verified EXACT at SHA-256 `29081b670f2c07ede6262ed47231a353348ff3b80c2cbd78dc10cbbe61a749d8` (deployed event copy `package-auditor-b/transport/` == its `payload/evidence/common/` copy == the EXEC-RB-003 diagnostic fixture copy; the older `74cbd8d4…` copies in the historical EXEC-RB-002 workspace are pre-remediation synthetic fixtures, NOT the accepted frozen contract). Read completely (60 lines).

**Classification: `PROMPT_CONTRACT_FINAL_RESPONSE_COMPATIBLE`.** The single output-related clause is `execution_permissions.output`: *"the ONLY host-backed writable location is /auditor-output; write your report to the exact output path given in your invocation"*. Grounds, tested against the four STOP criteria:

1. The contract never names the canonical pathname; it references the output path **by invocation reference**, and under the remediated binding the invocation contains exactly one output-path designation — the `--output-last-message` destination. The contract thereby points at the very mechanism this remediation makes authoritative.
2. The clause sits in a permissions/custody block (with evidence-read, deterministic-test-execution, scratch, and network/credential rules) defining the sanctioned output channel; no clause specifies a file-creation mechanism, and none of "create", "use a tool", shell/Python/filesystem-write appears as a report mechanism.
3. `report_requirements` specify report CONTENT ("a single JSON document conforming to AUCDEV-023-FIRST-PASS-REPORT-V1") and independence — fully compatible with final-response-as-payload.
4. No clause treats a tool-written file as authoritative; tool permissions cover review activity (deterministic self-test batteries) only.

The clause is an outcome/location obligation — the report lands at the exact invocation path under the only host-backed writable root — satisfied under the remediated contract by the pinned client persisting the final agent response via `--output-last-message`. No contract modification and no reinterpretation beyond this recorded reading. The diagnostic record's earlier static observation that the B instruction designated the path is a fact about the BUILDER-GENERATED instruction, not the frozen contract, and is what this candidate removes.

## 5. Baseline and candidate identities

- **Baseline (authoritative accepted EXEC-RB-002 preparation source)**: `/home/isa/aucdev023-s1-rb001-l1-exec-rb002-output-binding-implementation-20260924-01/candidate/components/build/build_packages.py`, SHA-256 `7cb0ba0a8ef1cbc3ce5ad8bd5e502b4d3b3ead9d2ea07e8bc513726be3c17141` — verified EXACT against the expected hash AND independently byte-identical to the accepted implementation handoff copy (`…-HANDOFF/candidate/components/build/build_packages.py`; the handoff `baseline/` copy `5ae3a111…` is the documented pre-EXEC-RB-002 before-state, correctly different). No `ACCEPTED_EXEC_RB_002_SOURCE_IDENTITY_MISMATCH`.
- **Candidate**: `/home/isa/aucdev023-s1-rb002-exec-rb004-single-writer-implementation-20260924-01/candidate/components/build/build_packages.py`, SHA-256 `68fc60d4816fc4b68edb18fd85a6c03701a9e6a0e378b62dfc794660ba9e8852`, 1127 lines, produced by anchored fail-closed patching (each anchor must occur exactly once or the patch refuses), minimal unified diff `+132/−23` recorded at `diff/build_packages.py.diff`.
- New isolated workspace `/home/isa/aucdev023-s1-rb002-exec-rb004-single-writer-implementation-20260924-01/` — outside the deployed real event, outside the accepted EXEC-RB-002 workspace (which is byte-unchanged, re-verified), outside the diagnostic workspace.

### 5.1 Minimum source change surface (exactly seven bounded edit groups)

1. Layered module-docstring `(RB-004)` block (authority, cross-finding constraint, terminal contract, refinement rationale).
2. `WS` repointed at the new isolated workspace (synthetic fixture only).
3. `EVENT_ID` set to fresh synthetic fixture identity `evt-b0045fa1e0000045` (charset `evt-[0-9a-f]{16}`, collision-checked against every historical/rehearsal/foreign fixture id).
4. `auditor_prompt` docstring relabel only (now documented as the AUDITOR_A instruction; function body AST-identical).
5. New deterministic contract constants `B_FINAL_RESPONSE_ONLY_CONTRACT` and `B_NO_TOOL_WRITE_CONTRACT` (no path/event literals) + new role-specific `auditor_b_prompt(event_id)`.
6. The `AUDITOR_B` invocation's final positional element changed from `auditor_prompt("B", EVENT_ID, _B_OUTPUT_NAME)` to `auditor_b_prompt(EVENT_ID)` (+ comment).
7. `_require_bound_b_output` strengthened (see §7).

AST verification (static suite): every top-level function AST-identical to baseline EXCEPT `_require_bound_b_output` (strengthened) and the NEW `auditor_b_prompt`; no changed line touches stdout/DEVNULL/subprocess-auditor surface; `--output-schema` still appears in source ONLY inside the fail-closed refusal function.

## 6. Old vs new Auditor-B instruction contract

**OLD (shared A/B instruction; the dual-writer designation)**:

> You are Auditor-B of AUCDEV-023 event `<event>`. Read /evidence/common/prompt-contract.json and perform exactly the independent first-pass review it defines. **Write your report to /auditor-output/<attempt>.first-pass-report.json in the exact AUCDEV-023-FIRST-PASS-REPORT-V1 schema the contract specifies.** Never read, print or copy any credential file under /auditor-home or /auditor-init.

**NEW (role-specific single-writer contract)**:

> You are Auditor-B of AUCDEV-023 event `<event>`. Read /evidence/common/prompt-contract.json and perform exactly the independent first-pass review it defines. **Your FINAL AGENT RESPONSE itself is the canonical report payload: it must consist ONLY of one exact AUCDEV-023-FIRST-PASS-REPORT-V1 JSON object in the exact schema the contract specifies, with no Markdown fence, no preamble, no epilogue and no explanatory text outside the JSON. Do NOT create, write or modify the canonical report path or any report artifact via shell, patch, Python, tool calls or any filesystem write; the harness client, not your tool activity, mechanically persists your final response to the exact output path given in your invocation.** Never read, print or copy any credential file under /auditor-home or /auditor-init.

The canonical pathname does not occur in the new instruction; the only path reference is by invocation reference, mirroring the frozen contract's own phrasing.

**Resulting B argv shape (unchanged structure, argc 8, prompt final positional):**

```
["codex", "exec", "--skip-git-repo-check",
 "--profile", "aucdev023-c3",
 "--output-last-message", "/auditor-output/<output_identity.name>",
 "<auditor_b_prompt(event_id)>"]
```

Auditor-A semantics byte-identical (see T1); Auditor-A's instruction keeps its accepted form including its own path designation (A's report custody is tool-written by design and was never part of EXEC-RB-002/004).

## 7. Strengthened fail-closed build-time gate

`_require_bound_b_output(doc)` (invoked exactly as before, only for `AUDITOR_B` bindings, before any binding/manifest byte is frozen) now refuses unless ALL hold, using deterministic generated expectations (no stale event/path literals):

1. `doc["auditor_role"] == "AUDITOR_B"` (gate refuses misapplication to any non-B role).
2. `--output-schema` absent (`EXEC_RB_002_OUTPUT_SCHEMA_FORBIDDEN_IN_AUDITOR_B_INVOCATION`).
3. `--output-last-message` occurs exactly once (`EXEC_RB_002_OUTPUT_LAST_MESSAGE_NOT_EXACTLY_ONCE`).
4. The immediately following item equals `"/auditor-output/" + doc["output_identity"]["name"]` (`EXEC_RB_002_DURABLE_OUTPUT_PATH_NOT_MECHANICALLY_BOUND`).
5. The prompt is the FINAL positional element — exactly one element after the destination (`EXEC_RB_004_PROMPT_NOT_FINAL_POSITIONAL_ELEMENT`).
6. The canonical pathname (and any `/auditor-output/` mention) is ABSENT from the natural-language instruction (`EXEC_RB_004_CANONICAL_PATH_DESIGNATED_IN_AUDITOR_B_INSTRUCTION`).
7. No tool-written-report instruction is present (`"Write your report to"` absent — `EXEC_RB_004_TOOL_WRITTEN_CANONICAL_REPORT_INSTRUCTION_PRESENT`).
8. The exact final-response-only contract sentences are present (`EXEC_RB_004_FINAL_RESPONSE_ONLY_CONTRACT_ABSENT`).
9. The prompt equals exactly `auditor_b_prompt(doc["event_id"])` (`EXEC_RB_004_PROMPT_NOT_THE_EXACT_GENERATED_SINGLE_WRITER_CONTRACT`).

All nine refusal classes demonstrated live (G1–G9 in the static suite).

## 8. Zero-provider test matrix (T1–T11) — ALL PASS

Static suite `tests/run_static.py` (56/56 PASS; deterministic, zero-network) + zero-provider suite `tests/run_zero_provider.py` (4 frozen-client compositions; all PASS). Synthetic identities only: `evt-b0045fa1e0000045` (binding fixtures), `evt-rb004swcafe0045` (client rehearsals).

- **T1 Role-A byte identity — PASS**: candidate A invocation == baseline A invocation byte-identically (synthetic-normalized AND normalization-free at the baseline's own identity); `auditor_prompt` function body AST-identical.
- **T2 B argv shape — PASS**: argc 8; option exactly once; destination == canonical `output_identity` and UNCHANGED from the accepted EXEC-RB-002 binding (I1 preserved); prompt final positional.
- **T3 B prompt non-tool-write contract — PASS**: canonical pathname absent; old imperative absent; exact final-response-only contract present; prompt == generated contract; old vs new instructions differ exactly by the write-designation removal + final-response contract.
- **T4 Binding/package coverage — PASS**: B invocation mutation changes `Binding.digest` (baseline `140310884ef1…` vs candidate `efbf16ec5c3f…` at the synthetic fixture; four mutation classes digest-sensitive); `binding_projection` carries the invocation; MANIFEST `transport_binding` carries it; the EXACT existing `ebs.launch.verify_event_package` PASSES on the candidate synthetic fixture package; candidate binding parses through the EXACT `ebs.binding.parse_binding`; baseline-shape binding still parses (EBS semantics unbroken); role-A binding builds and verifies UNCHANGED through the candidate builder.
- **T5 No protected runtime-source change — PASS**: all three protected trees byte-unchanged at HEAD; frozen launcher `011a8713…`, frozen validator `6aff0e7e…`, and the EBS source copy (34 files, pyc-free) identical to the live protected tree.
- **T6 Positive canonical-final-message delivery — PASS**: deterministic mock final-agent response = synthetic validator-PASS `AUCDEV-023-FIRST-PASS-REPORT-V1` JSON; mock performs NO canonical-report tool write (zero tool calls); exact frozen client exits 0; `--output-last-message` creates the canonical path; canonical file bytes == exact scripted final response (`f005e3b6…`/878 B); frozen validator exit 0.
- **T7 Terminal-writer dominance control — PASS**: canonical path pre-seeded with a non-authoritative sentinel (present in-namespace before client start) AND re-written mid-session by a model-directed tool call (executed successfully through the wrapper-interposed tool path, exit 0, no refusal); final agent response = valid synthetic report JSON; after client rc0 the canonical bytes == final-response JSON (`7b00e500…`/878 B — NOT the pre-seeded and NOT the mid-session bytes); frozen validator exit 0. Even incidental tool activity cannot determine the terminal canonical bytes.
- **T8 Invalid-final-response fail-closed control — PASS**: scripted final response is deliberately non-report text; client exits 0; canonical path exists with exactly that text (`2ed2b58e…`/191 B); frozen validator exit 1; bytes unchanged after validation — no report manufactured or repaired.
- **T9 Empty-final-message behavior — PASS**: scripted final response is the empty string; client exits 0; canonical path exists with 0 bytes (`e3b0c442…`, the empty-file digest); frozen validator exit 1; no stdout/tool-write fallback. (The separately-"missing" final-message form is not expressible with the deterministic mock's terminal behavior — script exhaustion itself yields a text message — so the empty form, which the diagnostic's public-source evidence identifies as the missing-final-message write content, is the proven form; recorded as residual R-3.)
- **T10 Historical-path census — PASS**: the real historical B output pathname absent from candidate source; real event/attempt ids (and foreign synthetic fixture ids) absent from active identity-generating logic; module-level historical ids confined to the three frozen historical-state pin constants; candidate default EVENT_ID fresh synthetic, no collision; generated invocations carry no real historical ids.
- **T11 No separate last-message artifact — PASS**: the successful T6 staging contains EXACTLY the canonical report artifact (`[<attempt>.first-pass-report.json]`, namespace listing captured at client exit before the proof file, host listing identical excluding the proof); no `.last-message.txt`, no new durable substantive side channel — the staging surface expected by the existing EBS lifecycle is unchanged.

## 9. Frozen identities (zero-provider executions)

- Frozen client `CODEX-CLI-0.154.0-NATIVE` SHA-256 `3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022` — fixture copy exhaustively verified byte-identical to the DEPLOYED frozen B package (195/195 files), fail-closed asserted by the runner before every session.
- Frozen boundary launcher `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa`; frozen output validator `6aff0e7eda0b16f9885bc7a7200bba7b6bcea42a9c5e9af2ef6ceb19848dd071` (invoked under the EBS fd-3 argv contract: sealed snapshot at fd 3, argv = identity/event/role/attempt/output-name/digest/size).
- Accepted mock transport `mock_provider.py` `8c3aa5d771c1691defa08bbd2b45c27d5ed36b02ab7e50946efadaa17e3cdc01` and `mock_scripts.py` `10e6093654d949b104bff39061ca4a6b56b9c7ddf6e711265b2f1d8039af5241` — byte-identical to BOTH accepted prior copies (EXEC-RB-002 rehearsal and EXEC-RB-003 diagnostic).
- Every client session ran inside the REAL accepted boundary composition (vendored bwrap, frozen C-3 profile bytes, tool-domain wrapper, `--unshare-net` loopback-only) with the mock at `127.0.0.1` the only reachable endpoint; mock logs recorded ONLY `/v1/responses` in every run.

## 10. Zero-provider / zero-runtime / held-state attestation

ZERO real provider. ZERO real inference (scripted deterministic bytes only). ZERO real credentials (synthetic marker bytes only). ZERO real event state (synthetic fixture identities only). The deployed real event, all five backups, the deployed packages/bindings (B binding `d9de33cb…`, B MANIFEST `f6801960…`), the real attempts tree (24 roots; the only `evt-60636835*` roots are the two terminal real attempts; ZERO synthetic rb004 roots), the accepted EXEC-RB-002 workspace, and the EXEC-RB-003 diagnostic workspace are untouched (re-verified read-only this session). No EBS source, boundary launcher, output validator, report schema, `--output-schema` flag, stdout custody/DEVNULL behavior, sandbox/network/tool wrapper, credential handling, Auditor-A path, or target commit was modified. No real event created, no packages generated for any real event, no launcher adaptation, nothing deployed, no auditor executed.

Held findings preserved verbatim: **EXEC-RB-001 = OPEN / ROOT_CAUSE_UNRESOLVED**; **EXEC-RB-002 = CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH** (not reopened; its deterministic canonical binding is mechanically preserved by this candidate and re-proven at T2d/T4/T6); **EXEC-RB-003 = ROOT_CAUSE_ESTABLISHED_AT_ZERO_PROVIDER_MECHANICAL_STRENGTH** (diagnostic record NOT rewritten); **EXEC-RB-004 = OPEN** (candidate implemented; closure pending Control Room readback).

Real execution authority `AUCDEV-023-S1-RB001-L1-RB002-FIRSTPASS-EXEC-20260924-01` = **CONSUMED / TERMINAL / CLOSED / NO_RERUN**; real model engagements 2/2 USED; no retry exists; audit completeness INCOMPLETE; qualification readiness `BLOCKED_BY_MISSING_MANDATORY_AUDITOR_B_CONFORMING_FIRST_PASS`; qualification NONE; installation NONE; AUCDEV-023 remains **P1 / READY / NOT DONE** with NO queue-count transition (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11).

## 11. Residuals (all non-blocking)

- **R-1** — The frozen prompt contract's imperative phrasing ("write your report to the exact output path given in your invocation") is satisfied under the remediated contract through client-mediated persistence of the final agent response; a future contract revision could state final-response delivery explicitly. NOT done here (the contract is frozen; §5 forbids modification). Recorded reading, not a reinterpretation.
- **R-2** — The candidate builder ships SYNTHETIC TEST FIXTURE defaults (`WS`, `EVENT_ID = evt-b0045fa1e0000045`). A future separately authorized preparation task MUST set its own fresh workspace root, fresh real event id, and its own identity_derivation/provenance prose before any real generation (accepted-builder convention, unchanged).
- **R-3** — T9 proves the EMPTY final-message form (0-byte canonical write, validator fail-closed). The separately-MISSING final-message form is not expressible with the deterministic mock (script exhaustion yields a text terminal message); the diagnostic's public-source evidence (`std::fs::write` of EMPTY content on missing final message) covers that form at corroboration strength.
- **R-4** — This candidate is preparation-source ONLY. No real event has been prepared or selected, no fresh packages generated for any real identity, no launcher adapted, no execution authority granted. EXEC-RB-004 closure, any fresh real event preparation, and any successor-execution authorization remain future Control Room decisions.
- **R-5** — The new B instruction references the output location by invocation reference (mirroring the contract's phrasing) rather than by name; the gate enforces the absence of the literal canonical path and of any write-designation, and the exact-generated-prompt equality check makes any deviation fail-closed.
- **R-6** — Observed fact carried forward from the diagnostic and re-observed at T7: model-directed tool writes to `/auditor-output` are POSSIBLE inside the tool domain. The enforced custody is the instruction-level prohibition plus the client's terminal write ordering; T7 proves mechanically that incidental tool writes cannot determine the terminal canonical bytes.

## 12. Publication

Exactly three changed tracked paths: NEW canonical record (this file) + `AUCDEV-CURRENT-STATE.md` (current-facing fields rotation lines 3/11/23–25 + one dated record appended) + `AUCDEV-BACKLOG.md` (one dated record appended; prior content byte-identical prefix). Exactly ONE bounded docs-only fast-forward publication commit whose sole parent is `a6966012192c238c77c22eb101e490e36154361d`, live master re-resolved immediately before staging (no auto-rebase). The generated-LAST reviewer handoff archive is produced AFTER the push and the post-push readback, with nothing included mutated afterward.

## 13. Next action — EXACTLY ONE

```
CONTROL ROOM READBACK OF THE EXEC-RB-004 SINGLE-WRITER IMPLEMENTATION
CANDIDATE BEFORE ANY FRESH REAL EVENT SELECTION, PACKAGE GENERATION,
LAUNCHER ADAPTATION, REPLACEMENT EXECUTION AUTHORITY, AUDITOR/PROVIDER
EXECUTION, QUALIFICATION, OR INSTALLATION.
```
