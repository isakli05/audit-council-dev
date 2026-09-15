# AUCDEV-010 D77333E8 — Campaign-2 binding-v2 Non-Overwriting Stale-Identity Correction (Canonical Record)

| Field | Value |
|---|---|
| Session class | ZERO-MODEL PACKAGE-CORRECTION IMPLEMENTER ONLY — NOT Auditor A, NOT Auditor B, NOT the Control Room, NOT a qualification authority, NOT an installation authority |
| Date | 2026-09-15 (Europe/Istanbul) |
| Governance base | live master `a5e5272f2699737524938420e11b8cd8528e75d9` (verified EXACT at bootstrap via live GitHub `refs/heads/master`; sole parent of this publication commit; re-resolved EXACT immediately before the single fast-forward push) |
| Input authority | operator's explicit 2026-09-15 ZERO-MODEL, NON-OVERWRITING correction mandate within the EXISTING Campaign-2 event ONLY |
| Provider/model inference | ZERO — no Claude Opus, no GPT-5.6 Sol, no Codex model turn, no `/audit-council`, no completion/messages/responses request |
| Frozen event (UNCHANGED) | `AUCDEV-010-BRQ-FINAL-D77333E8-20260915-02` (campaign class `BOOTSTRAP_ROOT_QUALIFICATION_FINAL_FRESH_REAUDIT_CAMPAIGN_2`; binding_version 1 → 2; NO Campaign 3; NO new event ID) |
| Frozen target (UNCHANGED) | `d77333e86aa091d2ac003e9a2ad26c88dff56aeb` (tree `de7261e3c912fa74e3a06d3f114b7e489c66225c`; skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`; sole parent `b04aa604771b237e3bc8abe96daa358fa8f9edd6`; all four re-verified mechanically against the git object store in THIS session) |
| Outcome | **`AUCDEV_010_D77333E8_CAMPAIGN2_BINDING_V2_CORRECTED_FROZEN_AWAITING_CONTROL_ROOM_READBACK_EXECUTION_AUTHORITIES_SUSPENDED_UNCONSUMED`** |
| Package battery | NEW machine-derived binding-v2 battery, **80 gates / 80 PASS / 0 FAIL** (`PACKAGE_SELF_TEST_FAILED = 0`); the historical binding-v1 66-gate battery is NOT overwritten |
| Qualification/installation | readiness BLOCKED / qualification NONE / installation NONE |

## 1. Control Room defect finding (recorded verbatim)

Control Room independently inspected the ACTUAL frozen Campaign-2 binding-v1
transport before Auditor-A execution and found, inside
`common-inputs/neutral-auditor-instructions.md`, that the mandatory
pre-inference verification checklist requires an OLD root tree beginning
`c36899d8…` and an OLD sole parent beginning `56acc23…` instead of the actual
D77333E8 identities. Classification:

`HARNESS/PROTOCOL DEFECT / FROZEN_AUDITOR_INSTRUCTIONS / STALE_TARGET_IDENTITY_BINDING / EXECUTION_BLOCKING`
`HARNESS/PROTOCOL DEFECT / PACKAGE_SELF_TEST_COVERAGE_GAP`

Mechanically established in THIS session against the git object store:
`c36899d817c7e15fb8e31fc1e80fab198dc583a7` = `tree(68e3b082)` (the
semantic-delta baseline tree) and `56acc23a0550cfdd046b23ef3d11d15b90721679`
= `parent(68e3b082)` — both carried from a prior-target era of the checklist
(the full-SHA identity block in the same file §2 step 2 was already correct,
making the document self-contradictory). The frozen instructions themselves
require STOP on identity mismatch; therefore execution against binding-v1 is
prohibited. No auditor was launched. Binding-v1 model engagements used: 0.

The identical stale tree value appears LEGITIMATELY in
`common-inputs/delta-inventory.json` as `baseline_tree` (machine-derived
semantic-delta baseline product evidence); that occurrence is NOT a defect
and was deliberately NOT "fixed".

## 2. Binding-v1 immutability (verified this session; NEVER mutated)

Binding-v1 remains byte-immutable historical package evidence in
`/home/isa/audits/aucdev-010-d77333e8-campaign2-package-20260915/`.
Re-hashed UNCHANGED in THIS session: transports A=B
`2837e175aa3c549869e018604b453c967e1081b5b57512b6fec0782e83f62b6a`
(454317 B each), FDR `43fe0791da9beff9a98f6a80103db1af52c9412785e380941f7908ba0d350dbf`,
common payload `9c94e6ef6f9f6afb2131ffe187d2ffc96451c11f5e5a34dc6a9b7120167ad302`,
contract `ab7555a2…`, output contract `4c42c2be…`, structural validator
`778e30f4…`, launcher v3 `fb5754a3…`, boundary manifest v3 instance
`81765bdc…`, resource gate `b9d5c596…`. Append-only disposition recorded:

`CAMPAIGN2_BINDING_V1_EXECUTION_BLOCKED_STALE_AUDITOR_TARGET_IDENTITY`

## 3. Binding-v2 successor freeze (SAME event, binding_version 2)

New non-overwriting workspace
`/home/isa/audits/aucdev-010-d77333e8-campaign2-package-binding-v2-20260915/`.

- **Primary correction** — `common-inputs/neutral-auditor-instructions.md`,
  exactly 3 asserted line replacements vs binding-v1 (recorded diff
  `evidence/instructions-correction-v2.diff`): binding line
  `binding_version 1 (frozen at preparation…)` → `binding_version 2
  (non-overwriting successor freeze under the same event…)`; ROOT TREE
  checklist expectation `c36899d8…` → `de7261e3…`; sole-parent checklist
  expectation `56acc23…` → `b04aa604…`. Corrected instructions SHA-256
  `3a05cb205ba9c6b3551b4c530f941b7d2da3711169f619aba494f1b0c84ff1ba`
  (binding-v1: `d07e5d62831d2ac56379aeb916a339041dc0fe2ce9a54e762829bda59d5e510d`).
  Mechanically inspected ALL active auditor-facing authored instruction/control
  files (instructions, qualification contract, output contract, structural
  validator, target-identity-verifier, FDR, evidence manifest): no other
  stale ACTIVE identity expectation exists; legitimate historical-provenance
  and semantic-delta baseline identities preserved untouched.
- **Auditor-facing identity binding map** — `AUDITOR-FACING-IDENTITY-BINDING-MAP.json`:
  74 rows / 75 occurrences classified (ACTIVE_EXPECTATION 14;
  ACTIVE_CURRENT_TARGET_REFERENCE 34; HISTORICAL_PROVENANCE 7;
  SEMANTIC_DELTA_BASELINE 17; OTHER 2); 0 unclassified authored Git
  identities; every ACTIVE value equals the git-derived identity; every
  HISTORICAL/DELTA row mechanically supported by a declared git derivation.
- **NEW fail-closed identity linter** — `run/identity-linter.py`: derives
  target/tree/skill/parent from the git object store (commit-object fields +
  subtree resolution + gitlink pins) plus the package verifier self-test,
  never trusting instruction text; scans the ACTUAL final transport
  contents. PASS on both extracted successor transports. Test battery
  14/14 required verdicts: wrong target/tree/skill/parent ⇒ FAIL; known
  prior-target tree `c36899d8…` in mandatory verification ⇒ FAIL; known
  prior-target parent `56acc23…` ⇒ FAIL; unclassified Git identity ⇒ FAIL;
  historical identity relabelled as current/required ⇒ FAIL; gitlink pin
  mutated ⇒ FAIL; delta baseline relabelled as target tree ⇒ FAIL;
  legitimate explicit historical baseline ⇒ PASS; legitimate semantic-delta
  baseline ⇒ PASS. (Closes `PACKAGE_SELF_TEST_COVERAGE_GAP`.)
- **Substantive contract preservation** — qualification contract
  `ab7555a2…`, first-pass output contract `4c42c2be…`, structural validator
  `778e30f4…` all BYTE-IDENTICAL to binding-v1 (proven at copy, at freeze
  precondition, at transport-member diff, and by battery gates). No
  qualification criterion, severity element, mandatory review area,
  completeness requirement, recommendation token or verdict rule changed.
- **Target-evidence byte preservation** — all 11 non-instruction common-input
  evidence members (incl. `blind-product-source.tar.gz` `49b79452…` and the
  product delta) byte-identical to binding-v1 (transport-level member diff).
- **`BINDING-V1-TO-V2-DEPENDENCY-DIFF.json`** — member census v1=19, v2=19;
  14 IDENTICAL_PRESERVED; 1 PRIMARY_CORRECTION (instructions); 4
  MECHANICALLY_DEPENDENT_REHASH (FDR, evidence manifest, sidecar, internal
  SHA256SUMS); binding metadata re-instantiated (parity proof, readiness
  records, boundary manifest); **UNEXPECTED = 0**.
- **Fresh A/B successor transports** —
  `AUCDEV-010-BRQ-FINAL-D77333E8-20260915-02-BINDING-V2-PREP-handoff-A.tar.gz`
  = `-handoff-B.tar.gz` = SHA-256
  `e4f6e01207aa897114b16cc2137d6f39587f9bf9fb9bd5c01f8aabac016b4f1c`,
  454795 B each, byte-identical (cmp), 21 total tar entries = 19 regular +
  2 directories, internal SHA256SUMS 18/18 PASS each, common payload
  recomputed from EACH handoff equals the FDR. Successor FDR
  `16812d77886bf947c29d0af8889b7b9cf147f0a6955c2eb3f8fadd8e28680f92`;
  successor common evidence payload
  `25e31c6caf6bb213a76f56b572b511d33922f27b9493267fe57f612472fefe71`.
  The successor transport SHA differs from binding-v1 (2837e175…) exactly
  because the common auditor instructions changed; the OLD transport
  remains untouched.
- **Blindness re-run on the ACTUAL successor transports** — PASS both roles:
  no Campaign-1 first-pass substance, no Campaign-1 execution-failure
  narrative substance, no peer/reconciliation/qualification-recommendation
  content, no credentials, no controller project memory, no user
  skills/methodology, no Graphify, no `/audit-council`; and NEW: none of the
  binding-v1 package identities (2837e175/43fe0791/9c94e6ef/9894791b/921fa73e),
  none of the correction-history narrative, and the stale prior-target tokens
  appear NOWHERE except the single legitimate semantic-delta
  `baseline_tree` occurrence in machine-derived `delta-inventory.json`. The
  auditor is NOT told that an earlier package contained stale target
  identities: the corrected instructions/FDR use neutral non-overwriting
  successor-freeze wording only.
- **Execution safeguards carried forward, NO weakening** — launcher v3
  `fb5754a3…` byte-identical; corrected resource gate `b9d5c596…`
  byte-identical (matrix 19/19 preserved; live dynamic state honestly
  `DEFERRED_TO_EXECUTION_GATE` — this correction claims NO resource-gate
  satisfaction); boundary manifest v3 re-instantiated BINDING-ONLY (sha
  `5561288a310d3cb271cad647da5bdeee289b3267db405f0287084bd18866e2d5`;
  mechanical v1→v2 field diff: ONLY transport/FDR/payload digest bindings +
  `binding_version 2` + supersedes lineage changed; all mechanism fields —
  mounts, PID namespace, resolver provision C5, role auth, ephemeral home,
  denials, credential rule, probe summary (102 inner gates, byte-carried
  battery results `2aad8f95…`) — identical); Auditor-A plain-Claude
  first-party profile (exe `26d02035…`) and Auditor-B
  ChatGPT-OAuth/GPT-5.6-Sol-xhigh profile (codex 0.154.0 native `3188814c…`,
  `.system` disable-all, advertisement absent, writable-CODEX_HOME-before-
  validation, zero-network rehearsal) carried byte-identically;
  controller-scope, route-readiness, final-env manifest and evidence/marker
  contract (retired `PROVIDER_REQUEST_INITIATED`) mechanisms carried and
  battery-verified.
- **Binding-v2 battery** — 80 machine-derived gates, 80 PASS / 0 FAIL
  (`PACKAGE_SELF_TEST_FAILED = 0`): target identity/reconstruction ×8;
  contract preservation + validator fixtures ×10; identity-binding coverage
  ×10; parity/blindness ×7; boundary ×12; A runtime ×5; B runtime ×12;
  shared safeguards ×10; record precision ×3 (incl. binding-v1 immutability
  re-hash); execution-authority accounting ×3.

## 4. Execution-authority accounting (§16 of the mandate; NOT exercised)

`MODEL_ENGAGEMENTS_AUTHORIZED = 2` · `MODEL_ENGAGEMENTS_USED = 0` ·
`AUDITOR_A_AUTHORITY = GRANTED_SUSPENDED_UNCONSUMED` (Claude Opus /
first-party Anthropic / plain Claude) ·
`AUDITOR_B_AUTHORITY = GRANTED_SUSPENDED_UNCONSUMED` (GPT-5.6 Sol / xhigh /
ChatGPT-OAuth Codex) · `AUDITOR_A = NOT_STARTED` · `AUDITOR_B = NOT_STARTED`.
They were never exercised and may NOT be exercised until this corrected
successor package receives independent Control Room readback acceptance.
This session activated neither. Future execution still requires three
consecutive all-PASS resource samples immediately before Auditor A and three
NEW consecutive all-PASS samples immediately before Auditor B; nothing in
this correction consumes or bypasses that requirement.

## 5. State after this correction

`CAMPAIGN2_BINDING_VERSION = 2` ·
`CAMPAIGN2_BINDING_V1 = HISTORICAL_EXECUTION_BLOCKED_STALE_IDENTITY` ·
`CAMPAIGN2_BINDING_V2 = PREPARED_FROZEN_AWAITING_CONTROL_ROOM_READBACK` ·
`EXECUTION_AUTHORITY = GRANTED_BUT_SUSPENDED_PENDING_BINDING_V2_READBACK` ·
`MODEL_ENGAGEMENTS_AUTHORIZED = 2` / `MODEL_ENGAGEMENTS_USED = 0` ·
`AUDITOR_A = NOT_STARTED` / `AUDITOR_B = NOT_STARTED` ·
`FIRST_PASS_BARRIER = CLOSED` ·
`D77333E8_CAMPAIGNS_USED = 2 OF MAX 2` / `REMAINING = 0` (NO Campaign 3) ·
`QUALIFICATION_READINESS = BLOCKED` · `QUALIFICATION = NONE` ·
`INSTALLATION = NONE`.

## 6. Governance publication scope

Exactly ONE governance commit over exact base
`a5e5272f2699737524938420e11b8cd8528e75d9`. Changed paths EXACTLY:
`docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (narrow current-facing
re-alignment + append-only history record 63), `docs/chatgpt-project/
AUCDEV-BACKLOG.md` (append-only history record 65 + milestone bullet), and
the NEW `docs/chatgpt-project/AUCDEV-010-D77333E8-CAMPAIGN2-BINDING-V2-
STALE-IDENTITY-CORRECTION.md` (this report). NOT modified: the Campaign-2
binding-v1 preparation report; the package-readback correction report;
Campaign-1 reports; qualification history; product source/tests; any frozen
package byte. Push discipline: live remote master re-resolved immediately
before push and required EXACT `a5e5272…`; ONE fast-forward push maximum;
no retry; no force; no tags. Postpush exact readback recorded in the
workspace `evidence/pub/`.

## 7. Mandatory handoff archive

Exactly ONE non-secret `.tar.gz` containing all independent-readback
material, including BOTH actual binding-v2 A/B transport archives, the
identity linter with all positive/negative tests, the binding map, the
dependency diff, the corrected instructions, the boundary-manifest
binding-only diff, governance before/after + push evidence, secret scan,
inventory, and exactly one `SHA256SUMS` generated LAST. Its path/SHA-256/
bytes/member census are reported in the session's final return and recorded
in project auto-memory, not embedded in this committed report.
