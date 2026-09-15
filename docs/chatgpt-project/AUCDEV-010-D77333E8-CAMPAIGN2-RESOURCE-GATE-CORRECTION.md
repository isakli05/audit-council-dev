# AUCDEV-010 D77333E8 — Campaign-2 Prelaunch Resource-Gate Controller-Lineage Correction (APPEND-ONLY CORRECTION)

| Field | Value |
|---|---|
| Session class | ZERO-MODEL HARNESS CORRECTION IMPLEMENTER ONLY — NOT Auditor A/B, NOT the Control Room, NOT a qualification/installation authority |
| Date | 2026-09-15 (Europe/Istanbul) |
| Governance base | live master `c4b58ac1901b788ec979ef6581449f40b944d1c1` (verified EXACT at bootstrap; sole parent of this publication commit) |
| Input authority | Control Room correction mandate of 2026-09-15: `HARNESS/PROTOCOL DEFECT / RESOURCE_PRELAUNCH_GATE / REQUIRED_CONTROLLER_FALSE_POSITIVE` in the Campaign-2 prelaunch resource gate; replace the argv-substring exemption with a mechanically bound controller-lineage policy; thresholds NOT weakened |
| Frozen target | `d77333e86aa091d2ac003e9a2ad26c88dff56aeb` UNCHANGED (tree `de7261e3c912fa74e3a06d3f114b7e489c66225c`; skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`; sole parent `b04aa60477b0237e3bc8abe96daa353fa8f9edd6`; re-verified live at bootstrap and battery time) |
| Provider/model inference | ZERO — no Claude Opus, no GPT-5.6/Codex model turn, no `/audit-council`, no completion/messages/responses request; only read-only `/proc`/filesystem observation, deterministic PID-namespace process fixtures, and artifact hashing |
| Campaign accounting | `D77333E8_CAMPAIGNS_USED = 1` of max 2; remaining 1; NO Campaign 2 created; NO new event ID; NO new transports; NO execution authority; Campaign-1 and preflight historical evidence untouched |
| Outcome | **`AUCDEV_010_D77333E8_CAMPAIGN2_STATIC_PREFLIGHT_PARITY_CLOSED_RESOURCE_GATE_CORRECTED_AWAITING_CONTROL_ROOM_READBACK`** |
| Successor battery v2 | 25 gates (A 5 / B 11 / S 9), **25 PASS / 0 FAIL**, 1 deferred item (dynamic resource state, `DEFERRED_TO_EXECUTION_GATE`); historical 24-gate battery byte-preserved (sha256 `bfc97040…`) |
| Qualification/installation | readiness BLOCKED / qualification NONE / installation NONE |

## 1. Scope and bootstrap

Mandatory live bootstrap verified: `refs/remotes/origin/master` = `c4b58ac1901b788ec979ef6581449f40b944d1c1` EXACT; local HEAD identical; the six required documents (CURRENT-STATE, BACKLOG, CONTROL-ROOM-RUNBOOK, PROJECT-UPDATE-PROTOCOL, the parity-closure report, the harness-preflight correction report) were fetched at that SHA and hashed; the frozen target commit/tree/skill-tree/parent identities re-verified. Working-tree noise (`smoke-fixture*`, `aucdev019-evidence/`) left untouched and excluded. Session workspace: `/home/isa/audits/aucdev-010-d77333e8-c2-resource-gate-correction-20260915/`.

## 2. The corrected defect — old R6 (frozen bytes, sha256 `28f711087b51552fd3d834fc7f95dca565c886d1aa5a0a2e80d2c3ccf2788109`)

```python
if re.search(r"(^|/)(codex|claude)( |$|-)", args) and "aucdev" not in args: ... FAIL
```

Mechanically evidenced failure modes (historical + this session):

1. **REQUIRED_CONTROLLER_FALSE_POSITIVE**: the ecba509 preflight session (pid 156628) and the parity-closure session (pid 2268570) each had R6 FAIL with the REQUIRED controller itself (`claude --settings …/profiles/zai.json`) as the only "competing" process — the rule was not execution-satisfiable by construction because the controller must exist while the immediately-prelaunch gate runs.
2. **Unsafe accidental exemption** (`"aucdev" not in args`, user-controlled argv text): an unrelated provider with "aucdev" in argv was silently exempted — RED-proven on the exact frozen bytes (test T5old old-gate PASS vs T5new corrected-gate FAIL). During this session the exemption even fired ACCIDENTALLY on workspace PATH text (a provider-shaped test controller exempted because the session path contains "aucdev"), recorded as direct evidence of the "accidental" in the Control Room classification.
3. **argv-text over-breadth**: the full-args scan flagged non-provider processes merely mentioning claude-like paths (live host: a `ugrep` worker; reproduced as T0b) — also not execution-satisfiable in a real controller environment whose own tool shells carry `/tmp/claude-…` argv text.

## 3. Corrected R6 — mechanically bound controller-lineage policy (corrected gate sha256 `b9d5c596a62de85f91954568303086e85d9789b70c3b9b3d5e25d08fe82c493b`)

At gate invocation the gate walks its OWN `/proc` ancestor chain and binds THE authorized controller ancestor by kernel-truth identity: **pid + starttime (`/proc/<pid>/stat` field 22) + executable path (`/proc/<pid>/exe`) + sha256 of the running binary + argv (recorded as METADATA ONLY)**. Exactly one usable candidate ⇒ `CONTROLLER_BOUND`; zero ⇒ `CONTROLLER_ANCESTOR_ABSENT` (fail under the frozen require-controller default); two or more ⇒ `AMBIGUOUS_CONTROLLER_LINEAGE`; provider-shaped ancestor with incomplete `/proc` identity evidence or a chain gap ⇒ `CONTROLLER_IDENTITY_EVIDENCE_MISSING` — all fail closed. No process name, cwd text, `"aucdev"` substring, environment label or other user-controlled argv text is an authorization basis.

**Future-controller binding contract**: the fresh controller records its own 4-field identity JSON (`pid`, `starttime`, `exe`, `exe_sha256`) and the gate is invoked with `--controller-binding FILE`; the binding NEVER substitutes for derivation — the mechanically derived ancestor must exist AND match all four fields exactly; stale PID (gone), reused PID (same pid, different starttime) and wrong-identity bindings all FAIL (`CONTROLLER_BINDING_MISMATCH`).

**Census classification**: provider-shaped = provider EXECUTABLE identity (exe-path pattern) OR invocation shape (argv[0]/argv[1] — the executable-as-invoked/script-shim signal that catches `node …/bin/codex`, since codex on this host is a node script). Everything provider-shaped is `COMPETING_PROVIDER_PROCESS` EXCEPT exactly the one authorized controller identity (pid+starttime) and non-provider-executable processes mechanically INSIDE the controller's subtree (its own tool/shell/gate processes). The future auditor process is NOT exempt (must not exist at gate time); the controller's own concurrent provider-exe workers also fail closed. **Measurements include the controller**: R1–R5 read system-wide/cgroup-wide state and the bound controller's RSS is recorded in every sample.

## 4. Fail-closed deterministic test matrix — 19/19 PASS (bwrap PID namespaces + synthetic procfs fixtures)

T0a old gate flags the required controller (RED on frozen bytes, neutral paths) · T1a one bound controller ancestor allowed · T1b binding file MATCH · T2a unrelated claude FAIL · T2b second controller-like session (argv clone) FAIL · T3a unrelated codex (native) FAIL · T3b unrelated codex (script-shim, exe=runtime) FAIL · T4 two controller-like ancestors in lineage ⇒ AMBIGUOUS FAIL · T5new "aucdev" in argv does NOT bypass · T5old old gate EXEMPTED the same process (defect) · T6 controller name/argv spoof without lineage FAIL · T0b ugrep-with-claude-path argv false-positive class fixed · T7a wrong-starttime (PID reuse) binding FAIL · T7b stale/dead-PID binding FAIL · T7c wrong-identity (ns-init) binding FAIL · T8 missing `/proc` identity evidence FAIL (+ full-identity control binds) · T9 no controller ancestor FAIL (require-controller) · T9b no controller + unrelated codex FAIL. Full per-test JSON: `03-tests/runs/TEST-MATRIX-RESULT.json` + `03-tests/nsbind/`.

## 5. Threshold preservation proof

`04-threshold-diff/THRESHOLD-DIFF-PROOF.txt`: `read_meminfo`/`read_psi`/`read_cgroup`/`oom_evidence` are BYTE-IDENTICAL between old and corrected gates (`inspect.getsource` sha compared); R1–R5/R7 policy strings byte-identical; all five threshold expressions textually present in both. Runtime equivalence: T10 runs OLD and NEW gates in one namespace — R1–R5 thresholds and pass-flags identical on identical inputs (measured-value drift between sequential runs recorded as informational), only R6 differs. **No memory/swap/PSI/cgroup/load threshold was weakened; nothing else in the accepted static-preflight mechanism set was weakened.**

## 6. Current dynamic resource state — honest

Live 3-sample run of the corrected gate under the REAL controller: `CONTROLLER_BOUND` all samples (controller RSS recorded each sample); R1/R3/R4/R5 PASS; **R2 FAIL (swap ≈13% free vs frozen ≥50%)**; **R6 FAIL on exactly ONE TRUE-positive competing process** — a stale orphaned `claude.exe` instance running with argv rewritten to look like `ugrep` (outside the authorized lineage; invisible to the old argv rule; NOT killed by this session); OOM evidence honestly `OOM_EVIDENCE_UNREADABLE_WITHOUT_ELEVATED_AUTHORITY`. No swap manipulation; no unrelated process killed. The dynamic condition therefore remains **`DEFERRED_TO_EXECUTION_GATE`**: immediately before future Auditor A, and separately immediately before future Auditor B, three consecutive all-PASS samples under the corrected gate (frozen thresholds, controller-lineage R6, recommended recorded `--controller-binding`) are REQUIRED before any launch.

## 7. Successor battery v2 (append-only)

`06-battery/successor_battery_v2.py` → `battery-result-v2.json`: **25 gates, 25 PASS / 0 FAIL**, 1 deferred (dynamic resource state). Gates A1–A5/B1–B11/S1–S2/S5–S8 re-derive from the SAME frozen parity evidence (not weakened); S3/S4 re-derive from the corrected-gate evidence; S9 is NEW (correction proven + historical battery preserved). The historical parity 24-gate battery result is byte-preserved (sha256 `bfc97040adfac669d6c697642760eaebbaeea6245303d2bcde8feda666d951ca`, still 24/24/1) and NOT overwritten; the ecba509 25-gate battery likewise untouched.

## 8. Dispositions

`AUCDEV_010_D77333E8_CAMPAIGN2_STATIC_PREFLIGHT_PARITY_CLOSED_RESOURCE_GATE_CORRECTED_AWAITING_CONTROL_ROOM_READBACK / BASE_c4b58ac1901b788ec979ef6581449f40b944d1c1 / TARGET_d77333e86aa091d2ac003e9a2ad26c88dff56aeb_UNCHANGED / ZERO_PROVIDER_MODEL_INFERENCE / OLD_R6_DEFECT_REQUIRED_CONTROLLER_FALSE_POSITIVE_RED_PROVEN_ON_FROZEN_BYTES / UNSAFE_AUCDEV_ARGV_EXCEPTION_DEMONSTRATED_AND_REMOVED / ARGV_TEXT_OVERBREADTH_FIXED / CORRECTED_R6_MECHANICALLY_BOUND_CONTROLLER_LINEAGE_PID_STARTTIME_EXE_SHA256 / CONTROLLER_BINDING_CROSSCHECK_MANDATORY_MATCH_STALE_REUSED_PID_FAIL / MATRIX_19_GATES_19_PASS_0_FAIL / THRESHOLDS_R1_R5_R7_BYTE_IDENTICAL_ONLY_R6_CHANGED / MEASUREMENTS_INCLUDE_CONTROLLER / LIVE_RUN_CONTROLLER_BOUND_HONEST_FAIL_SWAP_AND_TRUE_POSITIVE_STALE_DISGUISED_PROVIDER / DYNAMIC_RESOURCE_STATE_DEFERRED_TO_EXECUTION_GATE / SUCCESSOR_BATTERY_V2_25_GATES_25_PASS_0_FAIL_1_DEFERRED / HISTORICAL_BATTERIES_BYTE_PRESERVED / CAMPAIGNS_USED_1_OF_2 / CAMPAIGNS_REMAINING_1 / CAMPAIGN2_NOT_CREATED / CAMPAIGN2_NOT_AUTHORIZED / NO_NEW_EVENT_ID / NO_NEW_TRANSPORTS / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

This correction does NOT create Campaign 2, does NOT allocate an event ID, does NOT prepare auditor transports, does NOT qualify or install anything, and does NOT grant any execution or model authority.

## 9. Publication mechanics

Exactly ONE governance commit over exact base `c4b58ac1901b788ec979ef6581449f40b944d1c1`; changed paths EXACTLY `AUCDEV-CURRENT-STATE.md`, `AUCDEV-BACKLOG.md`, NEW THIS file. One fast-forward push after immediate prepush live-master re-resolution requiring exactly `c4b58ac…`; no retry; no force; no tags. No product source/test, qualification history, historical report, Campaign-1 evidence or prior preflight artifact modified.

## 10. Immediate next action

Independent Control Room readback of THIS publication and its handoff archive (old-gate RED proof, corrected gate + design, 19/19 matrix, threshold-diff proof, live dynamic result, battery v2). On acceptance, the operator decides Campaign-2 PACKAGE PREPARATION with the corrected gate as the mandatory immediately-prelaunch execution precondition (three consecutive all-PASS samples separately before future Auditor A and Auditor B). Campaign-2 creation remains a distinct later operator decision — NOT made by this record.
