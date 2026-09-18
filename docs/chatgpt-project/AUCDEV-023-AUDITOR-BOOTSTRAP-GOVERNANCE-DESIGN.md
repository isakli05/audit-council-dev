# AUCDEV-023 — Auditor-Bootstrap Governance Procedure Design (Canonical PROPOSED Record)

| Field | Value |
|---|---|
| Status | **`PROPOSED_FOR_CONTROL_ROOM_READBACK`** — NOT ADOPTED, NOT ACTIVE, NOT EXECUTION_AUTHORIZED, NOT QUALIFIED; a design proposal requiring independent Control Room readback and separate explicit operator authority before ANY part of it may execute |
| Session class | ZERO-MODEL / EVIDENCE + DESIGN REVIEW SESSION ONLY — NOT Auditor A/B, NOT the Control Room decision-maker, NOT a qualification authority, NOT an installation authority; NO `/audit-council` execution, NO auditor/model/provider/frontier execution, NO bootstrap campaign instantiation, NO campaign/event execution, NO qualification, NO installation, NO source/harness remediation, NO mutation of the frozen AUCDEV-023 audit target; ZERO provider/model/frontier calls |
| Date | 2026-09-18 → 2026-09-19 (Europe/Istanbul; bootstrap and evidence review 2026-09-18, canonical publication after local midnight 2026-09-19T00:0x+03) |
| Operator authority | Operator tasking (2026-09-18) authorizing the PATH B design/evidence review: design of a NEW AUCDEV-023-specific auditor-bootstrap governance procedure; review of the historical AUCDEV-010 bootstrap-root procedure and campaign evidence; a staged evidence search rooted at EXACTLY `/home/isa`; and preparation/publication of THIS proposed canonical design record for Control Room readback. NOT authorized: `/audit-council`; Claude/Opus/Codex/GPT or any model execution; provider calls; a bootstrap campaign; campaign/event instantiation; qualification; installation; source/harness remediation; mutation of the frozen target; adoption of this procedure as operative policy; execution authority under this procedure |
| Exact governance base | `9cb4956f05954b50c3de810e5754a7f66455a88d` (tree `fccaf15e9c59cbba7b9d1ac5cc71414618b8112f`; sole parent `646fbe8ab11d9b9cf9b51477046a795529cb601c`), resolved EXACT as live `refs/heads/master` of `isakli05/audit-council-dev` at this session's bootstrap (OBSERVED_FACT; re-resolved immediately before staging per §16); THIS design publication is the sole commit ahead of that base (its own future SHA is NOT embedded, per the SHA recording rule) |
| Subject | A NEW, one-event AUCDEV-023 auditor-bootstrap governance procedure whose narrow purpose is to establish a conforming independent review path for the FROZEN AUCDEV-023 qualification-harness target when NO proven qualified installed Audit Council predecessor is available — informed by (a) an expanded `/home/isa` historical-evidence review (§§3–5), (b) the historical AUCDEV-010 bootstrap-root design revision chain REV.1–REV.6 (§§6–7), (c) the Campaign-1/Campaign-2 lesson matrix (§8), and (d) the frozen AUCDEV-023 harness capability map (§§9–10) |
| Qualification / installation | qualification NONE / installation NONE (unchanged; this design establishes no new qualification or installation event and grants no authority) |
| Independent harness audit | **BLOCKED_PENDING_AUDITOR_BOOTSTRAP_GOVERNANCE** (unchanged; NOT PASS/FAIL/IN_PROGRESS; no auditor has reviewed `d4d584ff…`; this PROPOSED design does not change that state — only Control Room acceptance of a design PLUS separate operator execution authority can) |

Claim classes used below: `OBSERVED_FACT` (mechanically observed in
this session), `INFERENCE` (derived, marked), `REQUIREMENT` (task- or
record-mandated property), `PROPOSAL` (design content of THIS record —
carries NO authority until separately adopted).

---

## 1. Live bootstrap and confirmed base state (OBSERVED_FACT)

```
live repository : isakli05/audit-council-dev
live branch     : refs/heads/master
live HEAD       : 9cb4956f05954b50c3de810e5754a7f66455a88d   (EXACT)
live HEAD tree  : fccaf15e9c59cbba7b9d1ac5cc71414618b8112f   (EXACT)
sole parent     : 646fbe8ab11d9b9cf9b51477046a795529cb601c   (EXACT)
qh tree @ HEAD  : 5b8d5e5465923740470ff63ed9b8683f257a3787   (EQUAL to frozen target)
skill tree @ HEAD: c792933a862d9a5434681a88d183470dd8b15d2f (EQUAL to frozen target)
```

All mandated documents were read at that exact SHA (`git show`):
CURRENT-STATE, BACKLOG, CONTROL-ROOM-RUNBOOK, PROJECT-UPDATE-PROTOCOL,
QUALIFICATION-HISTORY, the auditor-provenance reconciliation record and
its READBACK, and the pre-controller readback/audit-target-freeze
record; plus the Campaign-1/Campaign-2 records enumerated in §7 and the
frozen AUCDEV-023 remediation chain summaries they carry. Confirmed
governing state at the base (OBSERVED_FACT):

```
AUCDEV-023                                = P1 / READY (NOT DONE)
frozen audit target                       = d4d584ffa47ad2848268ba947247f81a845b2322
target root tree                          = 1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7
target qualification-harness tree         = 5b8d5e5465923740470ff63ed9b8683f257a3787
target skill tree                         = c792933a862d9a5434681a88d183470dd8b15d2f
KNOWN_IMPLEMENTATION_BLOCKERS             = CLOSED_AT_CONTROL_ROOM_READBACK_STRENGTH
INDEPENDENT_AUDITOR_PROVENANCE_GATE       = NOT_SATISFIED (Control Room disposition)
INDEPENDENT_HARNESS_AUDIT                 = BLOCKED_PENDING_AUDITOR_BOOTSTRAP_GOVERNANCE
installed source                          = 8ae33444f349ce73c1359b963722e2d16acba630
qualification / installation              = NONE / NONE
Campaign-2 / AUCDEV-010                   = TERMINAL / P1 BLOCKED; Campaign-3 DOES NOT EXIST
backlog counts                            = 19 open = READY 9 / OPEN 7 / BLOCKED 3 (P0 2 / P1 7 / P2 11)
```

The frozen target's tree identities were re-derived mechanically at
`d4d584ffa47ad2848268ba947247f81a845b2322` (commit/root/qh/skill all
EXACT). The frozen target source (`qualification-harness/qh/**`) was
read at that SHA — never current-master substitutes. Pre-existing
unrelated working-tree state preserved unstaged throughout:
`smoke-fixture`/`smoke-fixture-103` gitlink drift, untracked
`aucdev019-evidence/`. (OBSERVED_FACT)

---

## 2. Historical-evidence question (PATH A re-test at expanded scope)

The immediately preceding Control Room result is
`INSTALLED_8AE_QUALIFIED_PREDECESSOR_PROVENANCE_NOT_ESTABLISHED` /
`NO_ALTERNATE_QUALIFIED_PREDECESSOR_ESTABLISHED_FROM_INSPECTED_EVIDENCE`
with `OPERATOR_REPORTED_EXTERNAL_HISTORICAL_EVIDENCE =
UNRECONCILED / NOT_LOCATED_IN_INSPECTED_SCOPE`. The prior reconciliation
explicitly recorded as UNKNOWN whether two then-out-of-scope surfaces —
the LCO project tree and the council run history — could supply missing
chain links. THIS session was authorized to search ALL relevant material
beneath `/home/isa`, which mechanically includes those surfaces.

Required positive chain (unchanged, verbatim from the governing rule):
**A** exact historically qualified source SHA; **B** independent auditor
identity; **C** valid auditor qualification/authority or accepted
bootstrap authority; **D** independent qualification verdict + operator
qualification acceptance; **E** verified installation of that SAME
qualified source; **F** installed-byte identity; **G** no later mutation
inheriting qualification; **H** reviewable provenance/binding
references.

---

## 3. Expanded `/home/isa` search methodology (staged, secret-bounded)

### 3.1 PHASE 1 — names/metadata only

Full top-level census of `/home/isa` (names, types, sizes, mtimes), then
name-level enumeration of every relevance-token-bearing surface
(aucdev / audit-council / audit_council / qualification / bootstrap /
auditor / campaign / first-pass / binding / transport / provenance /
predecessor / harness / blind / rollback / install / Option-R / REV /
verdict / acceptance), plus SHA-token filename searches for the
historical identities (`579e39a*`, `68ce12ac*`, `8ae33444*`,
`1a902371*`, `ff3f848*`) outside already-known trees.
(OBSERVED_FACT)

### 3.2 PHASE 2 — content inspection ONLY where names/metadata established relevance

Inspected (content level, non-secret): the council run history
manifests/repository-state of a sampled run plus a full-population
classification of ALL 161 run manifests; the LCO tree's
`audit-output/` name inventory + the two audit-council-mentioning plan
files + `codex-external-audit` name inventory; the
`audit-council-operator-setup-2026-09-08` directory and (extracted to an
isolated temp dir) the three members of
`AUDIT-COUNCIL-OPERATOR-SOURCES.zip`; the
`~/audits` full 126-entry name inventory and the bootstrap-design
revision workspaces (REV.1–REV.6 design trees, CHANGE-RECONCILIATION
documents, R1/R2 decision matrix, Option-R1 S1/S3 FINAL-REPORT, policy
publication workspace). (OBSERVED_FACT)

### 3.3 EXCLUDED surfaces (recorded, boundary respected)

Credentials and secret stores — `~/.codex/auth.json`,
`~/.claude/.credentials.json` class material, `~/.zcode/v2/credentials.json`
(metadata only: 4993 B, mtime 2026-08-11, PRE-DATES the Audit Council
project — unrelated class), `.ssh`, `.google_authenticator`, `.aws`,
`.mcp-auth`, `.npmrc`, `.claude.json`, browser session backup
(`brave-oturum-yedegi-…`), `.pki` — NOT read, contents never hashed,
never published. Unrelated personal files (Downloads, media, CVs,
unrelated projects) NOT inspected. Sealed current-event Auditor-A/B
substance under `~/auditor-controller-roots/**` — name-level only
(two event roots, matching the canonical Campaign records). Provider
chat/session content (`~/.codex/sessions/**` 297 files,
`~/.zcode` session logs) — NAME-level check only (zero
audit/council/qualification-bearing filenames); no session bodies read.
(OBSERVED_FACT of exclusion)

### 3.4 New evidence discovered (identities)

| Surface | Identity / census | Class |
|---|---|---|
| Council run history `~/.local/share/audit-council/history/` | 161 runs, 2026-09-04T18:59Z → 2026-09-18T17:42Z; per-run manifest/binding/contract/findings JSONL set (e.g. run `20260904T185933Z-881bd5`, 13-file standard shape) | council OPERATING history |
| Council worktrees `~/.local/share/audit-council/worktrees/` | 3 entries (2026-09-04/05) | council operating state |
| LCO project `~/projects/llm_council_orchestrator/` | incl. `audit-output/codex-external-audit/` (14-part external audit OF LCO), Fourth/Fifth independent release audits OF LCO, 11 `lco-reaudit-wt-*` worktrees | audits OF another product |
| Operator setup `~/audit-council-operator-setup-2026-09-08/` | `AUDIT-COUNCIL-OPERATOR-SOURCES.zip` = exactly 3 doc members (`AUDIT-OPERATOR-CURRENT-CONTRACT.md` b74b140a…, `AUDIT-OPERATOR-RUNBOOK.md` 7ad76d39…, `SOURCE-MANIFEST.md` f2078db1…) | operator-desk documentation; self-described "not product audit evidence or qualification" |
| Bootstrap design REV.1–REV.6 + policy + Option-R1 + rev6-rebind | see §6 inventory | design/policy artifacts |
| `~/audits` full inventory | 126 top-level entries, all AUCDEV-010/023-era campaign/governance workspaces and handoff archives already canonically indexed in repository records | campaign/governance event evidence |

### 3.5 Mechanical findings of the expanded review

1. **Council run history (161 runs)**: EVERY run's audited `repo_root`
   is a synthetic fixture worktree (`skill/tests/fixtures/prep-*/envroot/…`
   with a.py-class inventories) under the repo, installed-skill,
   campaign-preparation or stabilization worktrees. ZERO runs audit a
   real product, ZERO audit the Audit Council itself, ZERO are
   qualification events. (OBSERVED_FACT — full-population
   classification of all 161 manifests)
2. **LCO tree**: contains external/council audits OF LCO and
   audit-council escalation design REFERENCES only
   (`AUDIT_COUNCIL_ESCALATION_RECOMMENDED` in LCO plans). No
   qualification-of-Audit-Council evidence. (OBSERVED_FACT)
3. **Operator setup zip**: 3 documentation members; explicitly
   non-evidence class. No auditor archive, no verdict, no acceptance.
   (OBSERVED_FACT)
4. **SHA-token filename sweep** outside known trees: only the
   already-canonical 2026-09-10 targeted-search handoff tarball.
   (OBSERVED_FACT)
5. `~/.claude/skills` audit-council surface unchanged (3 directories:
   installed + two rollback copies, byte-identities established
   2026-09-18 by the prior reconciliation — not re-derived here, no
   mutation observed). (OBSERVED_FACT)

### 3.6 §5 STOP-GATE RESULT (REQUIRED)

```
HISTORICAL_QUALIFIED_PREDECESSOR_CHAIN_CANDIDATE_DISCOVERED = NO
```

No newly inspected surface supplies any of links B/C/D for ANY
candidate source. Every new surface is implementation/operational
evidence, audits OF other products, fixture self-test runs, operator-desk
documentation, design artifacts, or campaign event evidence that itself
recorded qualification NONE/BLOCKED. The stop gate of §5 does NOT
trigger; the §37 publication branch is NOT taken. Recorded instead
(REQUIREMENT, evidence-scope statement only — NOT a claim of historical
nonexistence):

```
HISTORICAL_PROVENANCE_STILL_NOT_ESTABLISHED_AT_EXPANDED_HOME_ISA_SCOPE
```

Updated evidence-scope status of the operator-reported external
historical qualification evidence: still
`OPERATOR_REPORTED / UNRECONCILED / NOT_LOCATED_IN_INSPECTED_SCOPE` —
now with the LCO tree and council run history (the two surfaces the
prior reconciliation named as UNKNOWN) INSPECTED and negative. NOT_LOCATED
is NOT DOES_NOT_EXIST. (REQUIREMENT held)

---

## 4. What the historical evidence DOES newly establish (design input)

The expanded review adds materially useful DESIGN evidence even though
it adds no qualification link:

- the complete historical bootstrap-root design revision chain
  (REV.1–REV.6 archives, §6) with file-exact change reconciliations;
- the Option-R1 S1/S3 execution record (8 superseded run reports +
  final run-9 report) demonstrating the package-battery/validator
  iteration discipline;
- the policy-adoption evidence archive and the rev.6 re-bind
  publication (binding-version discipline after target succession);
- the council run history's standard run-record shape (manifest,
  environment binding, repository state, contract+sha, per-auditor
  records, disagreement ledger, final findings, metrics, checksums) —
  a reusable custody/record pattern at operating strength;
- mechanical confirmation that the LCO/council-operating surfaces
  cannot serve as predecessor evidence (sharpening why PATH B is
  required).

---

## 5. Self-qualification barrier (REQUIREMENT — restated and held)

The frozen target `d4d584ff…` MUST NOT audit itself, qualify itself,
orchestrate its own qualification verdict, select favorable auditor
evidence, adjudicate away unfavorable findings, or convert its
deterministic tests into qualification. The currently installed
unqualified/unknown-provenance Audit Council
(`8ae33444f349ce73c1359b963722e2d16acba630`) MUST NOT be relabeled a
qualified auditor; its 161 historical fixture runs MUST NOT be
re-labeled independent review. Bootstrap auditors under this procedure
are EXTERNAL independent models whose authority derives from the
operator event authority ONLY — never from candidate Audit Council
qualification status, and never from model capability. Model agreement
is not proof.

---

## 6. Historical bootstrap design revision inventory (§7 of the task; OBSERVED_FACT)

All archives verified present and hashed THIS session (SHA-256 / bytes):

| Artifact | Identity | Size (B) |
|---|---|---|
| REV.1 `AUCDEV-010-BOOTSTRAP-ROOT-PROCEDURE-DESIGN-20260910T194146Z.tar.gz` | `5013d2e9450faec21e99ff2dec94aa2fe291928f096b2bf1323bf920513fd29a` | 39121 |
| REV.2 `…-REV2-20260910T201943Z.tar.gz` | `f579e3102b55d61fd083a4bd688b0a1a82b51f54e865073bd4dc7df8c23e5ff2` | 46473 |
| REV.3 `…-REV3-20260910T213151Z.tar.gz` | `df6d92710f37cc8eaf48fe5efc4fd3ab0a5502846a7ab3f3e16245649de2a0ae` | 63291 |
| REV.4 `…-REV4-20260910T214616Z.tar.gz` | `db4fd9f3827d89667abe0831eed4818380fa3a9f78c910c37b42a2dcbaba2afa` | 68362 |
| REV.5 `…-REV5-20260910T221028Z.tar.gz` | `732df56f73d8c2b20d843cfe7fb8107a6f8a39e4fb47e44e31775139a745cc44` | 72265 |
| REV.6 `…-REV6-20260910T222047Z.tar.gz` | `a16a0bb529074220dde0f7b267300af215d15377190ca0f57f08be06fc549608` | 73421 |
| Policy adoption evidence `aucdev-010-bootstrap-root-policy-publication-evidence-20260910T204937Z.tar.gz` | `b7def02ed902a3209097129fe928369adc3c3f233f6c0b0902e7dbe2226974c9` | 45726 |
| rev.6 re-bind publication evidence `AUCDEV-010-REV6-REBIND-PUBLICATION-EVIDENCE-20260911T015000Z.tar.gz` | `37e0ab4da4d8f80d7aadd7821be86c7fb0da60c2343453822be17017c686147d` | 41366 |
| Option-R1 S1/S3 workspace `~/audits/aucdev-010-optionr1-s1s3-workspace-20260910T230713Z/` | dir: FINAL-REPORT.md 6702 B + 7 superseded run reports (run3–run8) + evidence/ + frozen-root/ + packages/ | workspace |

All locations under `/home/isa/audits/`. Each revision workspace also
contains the COMPLETE extracted design set (procedure, contract
template, evidence-manifest template, first-pass output contract,
execution stages, acceptance matrix, digest DAG (rev3+), FDR template
(rev3+), R1/R2 decision matrix, risk/residuals, policy exception
proposal, change reconciliation, final report, live-bootstrap
verification, zero-activity statement, SHA256SUMS). The design revision
chain terminates at REV.6, which the Option-R1 S1/S3 execution and the
rev.6 re-bind instantiated. Campaign-era artifacts (qualification
contracts `ab7555a2…`; first-pass output contract `4c42c2be…`;
structural validator `778e30f4…`; FDR `e2ce437d…`; A=B transports
`cb0baf7b…` (v3) after `e4f6e012…` (v2) / `2837e175…` (v1); boundary
launcher v2 `f3085085…` / v3 `fb5754a3…`; boundary manifest v3
`80b6d69b…`; resource gate `b9d5c596…`; controller instructions;
blindness maps `AUDITOR-VISIBLE-BLINDNESS-MAP.json`; evidence parity
proofs; post-exec access checker; campaign ledgers/EVENT-RECORDs;
terminal records; root-cause scoping handoff `b51b1dbe…`) are inventoried
in the canonical repository records cited in §7 and preserved immutable
under `~/audits` and `~/auditor-controller-roots`. (OBSERVED_FACT)

The latest revision is NOT assumed best: REV.6's deltas over REV.5 are
digest-lifecycle precision (byte-finalization vs digest-production), and
REV.2's deltas over REV.1 are governance semantics; the load-bearing
governance content (two-auditor rule, default budget 2, permanent
single-use exception, addenda-separate-authority, no-finding-transfer)
is fully present from REV.2 onward. What REV.1–REV.6 do NOT contain —
mechanical preexec terminality, process-bound one-shot authority,
write-capability proof, controller-scope pre-provenance,
no-egress/AF_UNIX regressions, provider custody — is exactly what the
frozen AUCDEV-023 harness later added (§9).

---

## 7. Historical design evolution table (§8 of the task)

"Mechanically proven behavior" = demonstrated by an executed event;
"design intent" = specified only. Sources: REV CHANGE-RECONCILIATION
documents (read in full), canonical campaign records (read in full).

| Revision / archive | Problem it solved | Authority model | Auditor model | Blindness model | Evidence parity | Transport/boundary | Credential/custody | Controller authority | Retry/terminality | Qualification semantics | Installation semantics | Known gaps AT that revision | Later change | Relevance after AUCDEV-023 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REV.1 (194146Z) | no proven qualified predecessor blocks AUCDEV-010 re-audit | one-time bootstrap exception + per-campaign separate operator authority (execution authority NOT granted by policy) | TWO external independent first-pass auditors (design intent) | procedural blindness + token-blacklist scans (intent) | common evidence manifest, FDR with in-contract digest quadruple (defective, self/mutual digest) | s3 frozen package; boundary v1 (5fd5a576) — later proven PID-ns incomplete | host-staged role-auth dirs mounted into boundary | fresh-controller clean-scope instructions (prose) | campaign retry policy max 2 per target; no mechanical latch | auditor recommendation ≠ operator acceptance; deterministic PASS ≠ qualification (intent) | qualification ≠ installation (intent) | addenda loosely bounded; exception revivable; R1/R2 matrix transferred findings onto 579e39a; in-contract digests self-referential | REV.2 C1/C2/C3; REV.3 digest fix | governance semantics superseded by REV.2+; transport superseded by v2/v3 + qh |
| REV.2 (201943Z) | Control Room corrections C1/C2/C3 | + permanent SINGLE-USE exception, NO REVIVAL (adopted clause 6/7) | TWO first passes = DEFAULT_MODEL_ENGAGEMENTS 2; addenda/adjudication ONLY under separate authority; ceiling 5 | + mechanical historical-coverage mapping vocabulary post-barrier | + coverage-mapping completeness blocking | unchanged from REV.1 | unchanged | unchanged | + "no standing addendum/reuse authority inferable" | + BOOTSTRAP_HISTORICAL_FINDING_COVERAGE_INCOMPLETE blocks readiness | unchanged | digest defect still present (fixed REV.3); boundary still v1 | REV.3 | DEFAULT-BUDGET-2 and permanent-single-use are CARRIED INTO this proposal |
| REV.3 (213151Z) | digest-canonicalization defect | unchanged | unchanged | unchanged | digest DAG: acyclic external digest binding; FDR-only digests; canonical JSON; manifest = EVIDENCE members only | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | three surviving payload-digest formulations (fixed REV.4) | REV.4 | digest-DAG/FDR-only-digest pattern carried into all later packages (proven through Campaign-2 freeze) |
| REV.4 (214616Z) | single COMMON_EVIDENCE_PAYLOAD_SHA256 definition | unchanged | unchanged | unchanged | one authoritative {bytes,path,sha256}-in-array-order projection | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | skill-tree pin typo + stale S3 labels (fixed REV.5) | REV.5 | payload-parity discipline carried forward |
| REV.5 (221028Z) | exact skill-tree pin; authoritative S3 map; R5-C3/C4 | unchanged | unchanged | unchanged | + exact-40-hex pin checker with negative control | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | digest lifecycle conflation (fixed REV.6) | REV.6 | exact-pin/identity-linter discipline carried forward (identity-linter in binding-v2) |
| REV.6 (222047Z) | byte-finalization ≠ digest-production | unchanged | unchanged | unchanged | digest lifecycle columns in DAG | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | ALL REMAINING GAPS ARE EXECUTION-PLANE (mechanical enforcement), not design | re-bind 2026-09-11 (target succession c114afe→…, binding_version discipline) | the FINAL historical design; its execution-plane gaps are precisely RC-1/2/3 → closed by AUCDEV-023 |
| Policy addendum (adopted 2026-09-10 23:46, `80b933c`; evidence `b7def02e…`) | give the no-predecessor state a lawful path | applicability AUCDEV-010-only; permanent single-use; NO REVIVAL; adoption ≠ execution authority | two external auditors required; mechanical blindness claimed only if mechanically established | honest procedural/mechanical split mandated | common manifest + explicit parity | — | — | — | — | operator accepts separately; FIRST_PROVEN… only after BOTH bootstrap qualification accepted AND installation verified | separate from qualification | no mechanical preexec terminality; no write-capability gate; no controller pre-provenance | AUCDEV-023 harness closes these | NON-TRANSFER to AUCDEV-023 already recorded (Control Room 2026-09-18); THIS proposal is the required NEW governance decision |
| Campaigns (S4/S5, 0CCF9A82, 68E3B082, D77333E8 C1+C2) | instantiate the design | 2 single-use engagements per campaign; consumed at inference-capable exec regardless of outcome | A=Opus first-party; B=GPT-5.6-sol codex ChatGPT-OAuth | PROCEDURAL-only blindness honestly labeled (AUCDEV-001 unresolved); B external-skill input invalidated 68E3B082 set | A=B byte-identical transports (proven every campaign) | v1→v2→v3 launcher (PID ns + role-minimal auth + tmpfs home + resolver provision); stateless launcher proven (RC-2) | role-auth ro-staged (Campaign-1 B errno30) → writable-at-init ephemeral CODEX_HOME + disable-all `.system` skills | controller scope gates C1–C7 (C4 self-hit RC-1); STOP rules prose-only | campaign terminal states recorded; unauthorized retry occurred (RC-2) and was classified | every campaign ended qualification-blocked/NONE | NONE | see §8 lesson matrix | AUCDEV-023 harness (d4d584ff) | the empirical lesson base of THIS proposal |

DESIGN INTENT vs MECHANICALLY PROVEN, historical chain: intent =
two-blind-pass independence, parity, terminality, STOP; proven =
transports byte-parity, freeze/battery discipline, authority consumption
accounting, boundary isolation (v3, 25/25), one successful frozen
first pass (A attempt-005), structural validation, custody freezing;
NOT proven historically = mechanical no-retry, C4′ pre-start
provenance, write-capability, first-pass-set completion.

---

## 8. Campaign-1 / Campaign-2 lesson matrix (§9 of the task)

Historical finding status is recorded AT ITS EVENT; current design
impact stated separately. "Closed by AUCDEV-023" = the frozen harness
`d4d584ff` contains the replacing mechanism (accepted at Control Room
readback strength, NOT independently audited — see §9 classifications).

| # | Failure / incident (event) | Observed failure | Classification | Proximate mechanism | Root cause | Resp. split (product/harness/controller/external) | Closed by frozen AUCDEV-023 harness? | Replacing mechanism | Remaining governance relevance | Required future policy rule |
|---|---|---|---|---|---|---|---|---|---|---|
| L-01 | Controller admission gate / C4 self-hit (B-FIRSTPASS-002) | raw C4 FAIL overridden; execution proceeded | HARNESS/PROTOCOL — EXECUTION_CONTROLLER_ADMISSION_GATE_OVERRIDE | package-only checker tested name-presence of `projects/` at check time; live controller auto-creates own session slug ~47 s after start | checker predicate unsatisfiable in-session (RC-1 ESTABLISHED) | harness checker (primary) + controller (override) | YES (control-plane role) | C-1 pre-controller content-addressed bootstrap manifest captured BEFORE controller start + C4′ kernel-identity verification (SO_PEERCRED pid + /proc starttime + environ CLAUDE_CONFIG_DIR; current tree ⊆ manifest ∪ own slug) | the C4-override VIOLATION class is behavioral: any future controller can still choose to proceed past a FAIL | raw gate FAIL is authoritative; proceeding past any preexec FAIL = terminal protocol violation; checkers must be pre-start, not in-session |
| L-02 | Preexec STOP override (B-FIRSTPASS-002) | STOP rules existed only as prose; controller continued | HARNESS/PROTOCOL — EXECUTION_CONTROLLER_PREEXEC_STOP_OVERRIDE | four prose instruments, zero code enforcement | STOP semantics not mechanical (RC-2) | protocol design gap + controller act | YES (attempt lifecycle) | qh `AttemptStateMachine`: TERMINAL_PREEXEC_STOP absorbing, process-bound, same-UID non-resettable | the networked auditor leg runs OUTSIDE qh (see §10 noegress fact) — terminality there must be BOUND to the qh attempt | STOP must latch mechanically per attempt; second launch of a stopped attempt = unauthorized retry |
| L-03 | Unauthorized retry after preexec boundary failure (B-FIRSTPASS-002 attempt-1 P10 FAIL → second launch without Control Room return) | second boundary launch performed | HARNESS/PROTOCOL — UNAUTHORIZED_RETRY_AFTER_PREEXEC_BOUNDARY_FAILURE | stateless launcher v3 re-executes with zero latch/token/consumed state | no launch-token/consumed state (RC-2) | harness design + controller act | PARTIAL | qh one-shot grant + duplicate-attempt-id refusal + engagement ledger; for the networked leg: launch argv capture + operator-held launch invocation | full closure on the networked leg is procedural+ledger, not process-memory | no silent retry by controller; replacement attempt ONLY via NEW operator mint; retryable-class failures defined in advance (§14) |
| L-04 | Codex application sandbox read-only / auditor-output write failure (B-FIRSTPASS-002) | `sandbox: read-only`; patch ops rejected; FIRST_PASS_B ABSENT | HARNESS/PROTOCOL — AUDITOR_B_WRITE_CAPABILITY / CODEX_APPLICATION_SANDBOX_READ_ONLY | outer bwrap allowed writes (P3) while codex app-sandbox default refused model-generated writes (EROFS) | two independent confinement layers; profile had no sandbox_mode; rehearsal argv copied (RC-3; PRIMARY package-preparation, CONTRIBUTING validator+controller) | package (primary) + validator + controller; external tool behavior contributed | YES (as policy + gate) | C-3 named restricted permission profile (workspace_roots = auditor-output; ONE write entry; NO CLI `-s`/`--add-dir`) + GATE-W static+dynamic zero-provider rehearsal | GATE-W as frozen validates under hard no-egress; the networked profile variant needs the §13 GATE-W′ delta rule | write capability MUST be proven pre-inference on the EXACT transport profile; provider inference must never be spent discovering write permissions |
| L-05 | Stale binding (Campaign-2 binding-v1) | auditor checklist pinned OLD root tree `c36899d8…`/parent `56acc23…` | HARNESS/PROTOCOL — FROZEN_AUDITOR_INSTRUCTIONS / STALE_TARGET_IDENTITY_BINDING / EXECUTION_BLOCKING | identity block carried from prior-target era; self-contradictory file | package re-instantiation did not re-derive every active identity expectation | harness/package | YES (pattern) | identity linter deriving identities from the git object store; binding-v2 map 74 rows/75 occurrences; negative battery | binding discipline is event-package-side, not in qh source | every binding_version bump re-runs an identity linter over the ACTUAL transport; linter negatives mandatory |
| L-06 | Auditor-visible prior outcome (binding-v2) | FDR/contracts disclosed prior-campaign outcomes, lineage, finding IDs | HARNESS/PROTOCOL — FIRST_PASS_BLINDNESS / AUDITOR_VISIBLE_PRIOR_CAMPAIGN_OUTCOME / EXECUTION_BLOCKING | blacklist scanner missed the semantic class (false negative) | blindness scan coverage gap | harness/package | YES (pattern) | binding-v3 allowlisted provenance schema (six classes) + full auditor-visible surface tiling (1096 lines / 39 regions / 113 fields, zero gaps) | blindness maps are per-event package artifacts | allowlist-class blindness map over EVERY auditor-visible byte; forbidden class = prior outcome substance |
| L-07 | External-tooling parity input (68E3B082 Auditor-B) | B read `.codex/skills/graphify/SKILL.md` pre-verification | BOOTSTRAP_EVIDENCE_PARITY_INVALID ⇒ FIRST_PASS_SET_INVALID | provider `.system`/user skills auto-advertised into every turn | skills advertisement not neutralized | harness staging | YES (policy+mechanism) | `.system` census + generated `[[skills.config]] enabled=false` for EVERY censused skill + strict coverage fail-closed + advertisement-absence sensitivity control | neutralization is staging-side (ephemeral CODEX_HOME build), enforced by pre+post census gates | disable-all MANDATORY with pre/post coverage proof; any uncovered skill fails closed |
| L-08 | PID namespace / `/proc` escape (boundary v1) | host sentinel PID visible; 594 host processes; own pid host-numbered | AUDITOR_EXTERNAL_TOOLING_BOUNDARY_PID_NAMESPACE_INCOMPLETE / PROC_PID_ROOT_ESCAPE_NOT_NEGATIVE_TESTED | launcher mounted `/proc` without `--unshare-pid` | boundary structurally incomplete | harness | YES (pattern, in qh boundary) | v2/v3 `--unshare-pid` + fresh `/proc` + host-sentinel-invisible + `/proc/<host-pid>/root` blocked negatives | networked leg reuses the v3 lineage with these gates mandatory | PID-ns + sentinel + root-escape negatives mandatory in every boundary battery |
| L-09 | Role-specific auth minimization (boundary v1) | BOTH role auth dirs mounted for either role; both env vars always set | ROLE_SPECIFIC_AUTH_MINIMIZATION_NOT_ENFORCED | v1 design mounted both | over-broad staging | harness | YES (in adapters/spec) | role-minimal auth: exactly the role's adapter materialized in boundary-private CODEX_HOME/CLAUDE_CONFIG_DIR; irrelevant role auth ABSENT is a battery gate | hold as battery gate | role-minimality positive+negative gates per transport |
| L-10 | Persistent home contamination (boundary v1 + DEV-1) | `/auditor-home` host-backed skeleton; post-validation CODEX_HOME re-home mutation | B_PROVIDER_FINAL_ENVIRONMENT_NOT_FULLY_VALIDATED / PRELAUNCH VALIDATOR COVERAGE GAP | writable-home requirements discovered at runtime; validator certified an environment later mutated | final-env ≠ validated-env | harness + controller | YES (in spec/boundary) | final writable homes constructed BEFORE validation; spec-bound env verified at launch; qh trusted-spec re-verification at launch (dev/ino + digest) | the validated==final identity rule for the networked leg | the exact paid-process environment must be what the validator certified; no post-validation mutation |
| L-11 | Resource-gate semantics (R6 false positive; argv exemption; swap FAILs) | required controller flagged as competing; `"aucdev" not in args` accidental exemption; swap ~16% / R2 3×FAIL | RESOURCE_PRELAUNCH_GATE / REQUIRED_CONTROLLER_FALSE_POSITIVE (+ unsafe exemption, over-breadth) | argv-substring matching on user-controlled text | rule not execution-satisfiable by construction | harness | YES (lineage carried) | R6 `/proc` ancestor-lineage binding: pid+starttime+exe+sha256, CONTROLLER_BOUND/AMBIGUOUS/ABSENT fail-closed; thresholds unweakened; gate invoked EXACTLY ONCE | resource gate stays an execution precondition (3 consecutive PASS immediately prelaunch) | gate EXACTLY ONCE per attempt (first invocation authoritative — attempt-001 lesson); thresholds byte-frozen |
| L-12 | Provider credential custody | host plaintext auth dirs; ro-mounted CODEX_HOME incompatible (errno30); values at risk of logging | HARNESS/PROTOCOL — custody | credentials staged from host filesystem | no operator custody channel | harness | YES (mechanism; synthetic strength) | qh custody: bytes enter ONLY via operator pipe/memfd, live in non-dumpable process memory, materialize boundary-locally at payload exec, never printed/hashed/committed; adapters codex_chatgpt_oauth_v1 / claude_firstparty_oauth_v1 (SYNTHETIC-concrete) | real-credential integration remains gated (adapters synthetic-only) | no credentials in evidence packages; boundary-local materialization; no credential hashing for publication |
| L-13 | Same-UID authority root | any same-UID process can read/write ordinary files; launch authority in files is forgeable | G-1 design gap (stateless authority) | authority represented in ordinary artifacts | same-UID threat model unaddressed | harness | YES (design + code) | process-bound authority in non-dumpable supervisor (PR_SET_DUMPABLE=0, Yama≥1, pipe-only grant, abstract socket, one request); ledger is observability-only | residual: same-UID can still DoS (kill supervisor) — accepted fail-closed R-6 class | authority NEVER in files; supervisor kill = denial only, never authority gain |
| L-14 | Trusted launch-spec binding (IR-002) | controller-supplied spec fields; self-asserted codex identity; controller-chosen rw bind | CONTROLLER_SUPPLIED_LAUNCH_SPEC_NOT_BOUND | spec values came from the untrusted controller | no trusted spec | harness | YES | trusted_spec v3: claim-only controller request (attempt id, starttime claim, env claims, payload kind — 16 authority fields removed; unknown fields TERMINAL); all security-critical values spec-bound; launch-time dev/ino+digest re-verification; verified bytes snapshotted to memfds and materialized via `--ro-bind-data` | hold | controller request is a CLAIM, never authority |
| L-15 | Controller-supplied security-critical state (IR-001/002 chain) | self-mint without external auth; self-asserted pins | CR-IMPL-001/002 | production mint reachable from controller context | authority root not mechanically anchored | harness | YES (rootauth) | two-phase `qh authority`: Phase A trusted pre-controller freeze (operator-selected expected harness identity; qh-harness-tree/2 path-independent digest; fail-closed drift; 21-file sealed bundle; all 19 privileged modules loaded pre-controller; import guard) + Phase B operator-held finalization (PIPE/sealed-memfd only; authorized_controller {uid,pid,starttime}; frozen-harness-id equality before trigger) | INDEPENDENT_AUDIT_FOCUS marks remain (§9) | pre-controller phase is the ONLY trusted phase |
| L-16 | Yama override / test-hook bypass (IR-003) | `--yama-override` and `--fault`-style flags reachable in production parser | PRODUCTION_TRUST_CHECK_OVERRIDE_BYPASS_PRESENT | test seams exposed on production CLI | parser surface | harness | YES | production parser structurally rejects `--yama-override`/`--fault*` on every subcommand; SupervisorPolicy contains only verification seams; real kernel knob always read; simulated <1 FAILS CLOSED | hold | no trust-check overrides in any production entry |
| L-17 | Sealing / UAPI (CR-REMED-001) | invalid memfd/seal constants ⇒ seal-capability conclusion invalid | AUTHORITY_CRITICAL_SEAL_REQUIREMENT NOT ESTABLISHED | wrong UAPI constants | implementation defect | harness | YES (code, self-test) | centralized corrected UAPI constants + deterministic UAPI-pin tests; MANDATORY authority-critical sealing; fail-closed AUTHORITY_CRITICAL_SEALING_UNAVAILABLE (exit 13) via test-only failing-seam proof | hold | seals mandatory where represented; fail-closed when unavailable |
| L-18 | Supervisor bootstrap immutability (CR-REMED-002) | supervisor/bootstrap loaded from ordinary mutable host tree | SUPERVISOR_BOOTSTRAP_TRUST NOT ESTABLISHED | host PYTHONPATH re-import possible | mutable-tree trust | harness | YES (CR-HARDEN-001 closure) | freeze-before-trigger (21-file set vs spec digest; BOOTSTRAP_FROZEN before ROOT_SOCKET_BOUND); QH_IMPORT_FROZEN meta_path guard; fork()-from-frozen supervisor; in-boundary bytes from frozen bundle; pre-start mutation ⇒ BOOTSTRAP_HARNESS_TREE_DRIFT exit 17 | INDEPENDENT_AUDIT_FOCUS: code-object provenance claim precision (get_code()+compile comparison is NOT standalone cryptographic proof) | pre-freeze privileged-code provenance rests on the operator Phase-A trust boundary — auditor MUST review this assumption |
| L-19 | Trusted-spec channel (CR-REMED-003) | regular-file spec fd permitted | SPEC INPUT NOT CAPABILITY-BOUND | ordinary file spec input | channel discipline | harness | YES | spec input capability-bound: PIPE or FULLY-SEALED memfd only; file stdin/`--spec-fd` refused (exit 15); unsealed/partial refused | hold | trusted inputs only via capability channels |
| L-20 | Authorized-controller binding (CR-REMED-004) | trigger consumable by unbound peer | AUTHORIZED CONTROLLER NOT PRE-BOUND | no pre-binding | binding gap | harness | YES | spec v2+/v3 REQUIRED authorized_controller {uid,pid,starttime} operator-authored inside the digest; root mint trigger + supervisor request enforce SO_PEERCRED + actual starttime; wrong-peer = accepted fail-closed DoS R-6 | hold | wrong-peer consumption = denial, not breach |
| L-21 | Provider API timeout (Campaign-1 A) | `Request timed out`, 0 tokens, 17-B error-only artifact, NONCONFORMING rc=2 | EXTERNAL CONDITION / PROVIDER_API_OR_ROUTE_FAILURE / COMPLETENESS_LIMITATION | provider-side failure after initiation | external | external | N/A (external) | — | engagement consumed at exec regardless of outcome (held) | consumption-at-exec rule; error-only output is NONCONFORMING; missing report never reconstructed |
| L-22 | Provider network failure (Campaign-1 B attempt-2) | rmcp/ws/DNS failures ~37 min; zero agent content | EXTERNAL CONDITION / PROVIDER NETWORK CONNECTIVITY FAILURE (root cause later corrected: boundary resolver defect L-23) | EAI_AGAIN inside boundary | initially external, later mechanically explained | harness(root)/external | YES for the resolver class (noegress masks /run/systemd/resolve + /run/dbus; AF_UNIX escape regression closed) | resolver provision + netns discipline | route readiness preflight mandatory prelaunch, non-inference | DNS/TCP/TLS/HTTP-auth-class readiness proven BEFORE any paid engagement |
| L-23 | Boundary resolver defect (Campaign-1 B root cause) | /etc/resolv.conf symlink dangling inside boundary (tmpfs /run) | CORRECTED_BOUNDARY_RESOLVER_DEFECT (REQUIRED_NONSECRET_CONFIG) | ro-bound /etc + tmpfs /run ⇒ no resolver | launcher composition | harness | YES (pattern in noegress/boundary) | `--ro-bind /run/systemd/resolve /run/systemd/resolve` provision + P12/N12 gates | the networked leg MUST re-provide the resolver with the same gates | resolver provision + its negative (no unrelated /run exposure) mandatory |
| L-24 | Read-only CODEX_HOME init failure (Campaign-1 B attempt-1) | errno30 local init failure pre-provider | HARNESS/PROTOCOL DEFECT (B_ATTEMPT1_LOCAL_INIT_FAILURE_READONLY_CODEX_HOME) | ro-mounted CODEX_HOME vs codex writable-at-init requirement; battery had substituted local probes | probe fidelity gap | harness | YES (adapter semantics) | adapter materializes writable-at-init boundary-private CODEX_HOME (Campaign-2 evidence) | hold | provider-runtime parity requirements established by evidence; rehearsals must exercise REAL provider init shapes zero-network |
| L-25 | Controller session-launch scope (A attempts 002/003) | controller launched from repo root with project auto-memory PRESENT; CLAUDE_CONFIG_DIR absent from env (C3/C4 FAIL) | HARNESS/PROTOCOL — EXECUTION_CONTROLLER_SESSION_LAUNCH_SCOPE / PREEXEC_STOP | authority handed to a session that did not satisfy launch-scope predicates | scope binding on wrong layer | controller/procedure | YES (C-1 + authorized_controller) | pre-start manifest + kernel-identity controller binding; the exact bound process is the only request source | the bound invocation discipline is procedural on the operator side | bind CLAUDE_CONFIG_DIR on the SAME launch invocation; fresh non-project root |
| L-26 | Marker precision (PROVIDER_REQUEST_INITIATED ambiguity; LOCAL_CLI_INITIALIZED basis) | wrapper markers denoted local exec, not provider initiation | RECORD_PRECISION / EXECUTION_MARKER limitations | markers at wrapper boundary | instrumentation | harness | PARTIAL (accounting rule) | consumption rule made explicit (exec-after-gates = consumed; §14); undeterminable cases treated as consumed | markers remain evidence-precision residuals | markers must distinguish local CLI exec vs provider-network initiation; undeterminable ⇒ consumed |
| L-27 | Post-exec access checker self-hit | rc=2 on controller-staged helper definitions | POST_EXEC_ACCESS_CHECKER_SCOPE / CONTROLLER_MECHANISM_SELF_HIT | checker scanned its own staged negatives | checker scope | harness | YES (scope rule) | auditor-surface-only scans + helper self-hit classification | hold | checkers scan auditor-produced surfaces, not controller staging |
| L-28 | Auxiliary Haiku usage (A attempt-005) | auxiliary first-party Haiku entry (1699/20 tokens) inside single exec | COMPLETENESS_LIMITATION / MODEL_ROLE_PROVENANCE (purpose not established) | provider-internal auxiliary call | external/toolchain | external | N/A | accounted as within the single engagement (MODEL_ENGAGEMENTS_USED unchanged) | disclose per run | auxiliary model usage inside an engagement is recorded and does not alter engagement accounting |
| L-29 | Bootstrap campaign terminality | Campaign-2 TERMINAL; A/B authorities CONSUMED_CLOSED; 2-of-2 campaigns used; no conforming blind set | CAMPAIGN ACCOUNTING | engagements consumed without a conforming set | combined L-01..L-24 | — | N/A (governance fact) | — | PRESERVED EXACTLY | Campaign-2 remains TERMINAL; new event namespace; NO Campaign-3; no transfer of old authority |

---

## 9. Current frozen AUCDEV-023 harness capability map (§10 of the task)

Read from the EXACT frozen target `d4d584ffa47ad2848268ba947247f81a845b2322`
(qh tree `5b8d5e54…`; 47 files; `qh/` = 19 modules + `fixtures/`).
Classifications are THIS design's reuse verdicts (PROPOSAL), grounded in
source verified this session (OBSERVED_FACT) and in Control Room
readback acceptances (implementation/readback strength, NOT independent
audit):

| Mechanism | Frozen source evidence (verified this session) | Classification |
|---|---|---|
| Pre-controller authority lifecycle (two-phase) | `qh/rootauth.py` `qh authority`: Phase A trusted freeze → `PRE_CONTROLLER_BOOTSTRAP_FROZEN` milestone; Phase B operator finalization; `ROOT_TRIGGER_BEFORE_FINALIZATION` refusal; `FINALIZATION_SOURCE_KIND_REFUSED` | **READY_TO_REUSE_AS_IS** (authority plane) |
| Operator-selected harness identity | REQUIRED `expected_harness_tree_digest` (no default); path-independent `qh-harness-tree/2` entries-only digest (`qh/trusted_spec.py:46-47` SPEC_SCHEMA_VERSION=3, TEMPLATE_SCHEMA_VERSION=1); fail-closed `BOOTSTRAP_HARNESS_TREE_DRIFT` | **READY_TO_REUSE_AS_IS** |
| Sealed bootstrap bundle | 21-file privileged byte set (19 qh modules + 2 fixtures) frozen before controller start; four-seal memfd; `_module_code_matches_frozen()` per-module loader/compile comparison | **READY_TO_REUSE_AS_IS** with **REQUIRES_INDEPENDENT_AUDIT_FOCUS** (code-object provenance claim precision — the Control Room INFORMATIONAL note; the loader-consistency mechanism and PRE-CONTROLLER trust assumption MUST be explicitly reviewed by the bootstrap auditors — they are reviewing the target that carries this mechanism) |
| Controller binding | spec v3 `authorized_controller {uid,pid,starttime}`; SO_PEERCRED uid/pid + actual `/proc` starttime enforcement (`qh/authority.py:371-397`); wrong-peer fail-closed (R-6 DoS accepted) | **READY_TO_REUSE_AS_IS** |
| Trusted spec/template | `qh/trusted_spec.py` v3 canonicalization, self-certifying id, source identity capture (realpath+dev+ino+digest; sensitive-named files NEVER hashed), launch-time re-verification | **READY_TO_REUSE_AS_IS** |
| One-shot authority | pipe-only mint (file-carried grant refused at mint AND supervisor); non-dumpable supervisor; abstract socket; serves EXACTLY ONE request | **READY_TO_REUSE_AS_IS** |
| Terminal PREEXEC behavior | `qh/statemachine.py`: MINTED→BOUND→PREEXEC_CHECKING→CONSUMED_FOR_LAUNCH→LAUNCHED→TERMINAL with absorbing TERMINAL_PREEXEC_STOP; invalid transitions raise; ledger deletion/recreation restores nothing (`qh/ledger.py` observability-only) | **READY_TO_REUSE_AS_IS** (see §13 two-plane binding for the networked leg) |
| Credential custody | `qh/custody.py` memfd holds; pipe/memfd-only sources; never printed/hashed/committed | **READY_TO_REUSE_AS_IS** (mechanism) + **REQUIRES_GOVERNANCE_BINDING_ONLY** (live-credential use is event-side policy; adapters synthetic) |
| Provider adapters | `qh/adapters.py`: `codex_chatgpt_oauth_v1` (auth.json 0600, writable-at-init CODEX_HOME), `claude_firstparty_oauth_v1` (.credentials.json 0600, boundary-private CLAUDE_CONFIG_DIR), `synthetic_inert_v1`; unknown adapter = blocker | **REQUIRES_GOVERNANCE_BINDING_ONLY** (SYNTHETIC strength; real roles evidence-supported per Campaign-2 parity closure) |
| Hard no-egress | `qh/noegress.py`: fresh netns; no address/route; loopback down; DNS/TCP probes fail; `/run/systemd/resolve` + `/run/dbus` masked (`DEFAULT_MASK_PATHS`); ZERO inherited socket FDs; no setns-back | **READY_TO_REUSE_AS_IS** for rehearsal/payload planes. **STRUCTURAL FACT**: the trusted-spec schema REQUIRES `noegress.required = true` (`qh/trusted_spec.py:456-458, 537-539`) — every protected launch the frozen harness can authorize is network-isolated; the networked auditor session CANNOT be a qh protected launch (source change would require a fresh target — out of scope). This is the mechanical basis of the two-plane design (§13) |
| PID/process isolation | bwrap fresh inner root; ro `/usr /lib* /etc`; PID/IPC/UTS/NET unshare; env cleared-then-set; tmpfs /tmp; no host harness-root bind | **READY_TO_REUSE_AS_IS** (networked variant via v3-lineage transport, §13) |
| Codex restricted profile | `qh/codex_profile.py`: identity pin; named restricted profile (`workspace_roots` = one role; single `write` entry; enumerated reads; no root-wide read; CODEX_HOME/auth never an entry); FORBIDDEN_CLI_FLAGS `--add-dir`, `-s`, `--sandbox`, bypass flags | **READY_TO_REUSE_AS_IS** (profile content; GATE-W′ networked delta per §13) |
| Auditor-output write semantics | exactly ONE rw bind (spec-bound host source); evidence/target RO or absent | **READY_TO_REUSE_AS_IS** |
| GATE-W | `qh/gatew.py` MATRIX_OPS static+dynamic semantic matrix under no-egress with synthetic custody (auditor-output CRUD allowed; evidence writes refused; target/host writes refused; auth ABSENT) | **READY_TO_REUSE_AS_IS** as the mandatory pre-inference write-capability proof (zero provider); networked-profile variant GATE-W′ = governance binding (§13) |
| Engagement accounting | `qh/campaign.py` EngagementLedger — operator-written ONLY; never touched by the attempt lifecycle (mechanically asserted by tests) | **READY_TO_REUSE_AS_IS** |
| Claim-only controller request | request schema = {attempt_id, controller_starttime, env_claims, payload_kind} (`qh/authority.py:87-89`); unknown fields TERMINAL | **READY_TO_REUSE_AS_IS** |
| Protected-child byte provenance | verified harness/config/exe bytes snapshotted to process-bound memfds; materialized via bwrap `--ro-bind-data`; boundary_child re-hashes every materialized file + re-verifies tree digests before payload exec | **READY_TO_REUSE_AS_IS** (for no-egress children); **REQUIRES_INDEPENDENT_AUDIT_FOCUS** (the check-to-use window reasoning) |
| Fork-from-frozen supervisor | supervisor forks from the frozen bootstrap; no exec/no host module path; `qh cli supervisor` test/diagnostic-only | **READY_TO_REUSE_AS_IS** + **REQUIRES_INDEPENDENT_AUDIT_FOCUS** (same as sealed-bundle item) |
| Finalization channel | operator-held PIPE or fully sealed memfd created pre-controller; write end NEVER in the controller process (/proc fd-inode proof); strict delta shape; unknown fields exit-18 | **READY_TO_REUSE_AS_IS** |
| Attempt ledger/state machine | see terminal PREEXEC row | **READY_TO_REUSE_AS_IS** |
| Generic qualification-payload machinery (C-1 bootstrap manifest/C4′, compose, boundary batteries) | `qh/bootstrap.py`, `qh/compose.py`, tests | **READY_TO_REUSE_AS_IS** for control-plane roles; **NOT_APPROPRIATE_FOR_BOOTSTRAP**: none — no mechanism is classified NOT_APPROPRIATE; the no-egress launch requirement is a SCOPE boundary (not a defect) handled by the two-plane design; the only UNKNOWN-classified element is real-provider credential integration behavior (governance-gated, §12) |

All READY_TO_REUSE classifications are PROPOSAL subject to Control Room
acceptance; none is executed by this session.

---

## 10. Old design → current harness delta matrix (§11 of the task)

| Historical AUCDEV-010 mechanism | Historical demonstrated problem | Current AUCDEV-023 mechanism (frozen `d4d584ff`) | Mechanically proven replacement? | Governance rule still needed? | Design decision for new procedure |
|---|---|---|---|---|---|
| s3 frozen package + FDR digest quadruple (REV.1) | self-/mutual-digest defect (REV.3 fix) | qh trusted-spec self-certifying content-addressed id + canonicalization | YES (self-tests) | keep event-side FDR for the transport plane | reuse REV.6-equivalent digest DAG for the event package; qh spec id for the control plane |
| Two external blind first passes (REV.2 default budget 2) | set never completed (Campaign-1 external failures; Campaign-2 B nonconforming) | NOT replaced — auditor topology is governance, not harness | N/A | YES — topology analysis (§11) | retain TWO-pass default on evidence (§11), on the new control plane |
| Prose STOP rules / stateless launcher (RC-2) | unauthorized retry | qh AttemptStateMachine absorbing terminal + one-shot process-bound grant | YES for qh-plane attempts | YES for the networked leg | two-plane binding (§13): attempt-terminality governs the transport launch; replacement = new operator mint only |
| In-session C4 checker (RC-1) | checker self-hit; override | C-1 pre-controller manifest + C4′ kernel identity | YES (self-tests) | raw-FAIL-authoritative rule | adopt C-1/C4′ for the controller scope gate; any raw FAIL = terminal |
| Boundary v1→v3 lineage | PID-ns leak; both-role auth; persistent home; resolver defect | qh boundary + noegress masks + adapters writable-at-init | YES (batteries; v3 proven live in attempt-005) | YES for networked leg | reuse v3-lineage composition + P/N gates for the networked transport (justified reuse, not blind copy: + launch-token binding + GATE-W′) |
| Token-blacklist blindness scanner | prior-outcome false negative (binding-v3 fix) | allowlisted provenance classes + full-surface tiling (package-side pattern) | package-side (pattern proven in binding-v3 freeze) | YES per event | mandatory blindness map over every auditor-visible byte of the NEW transport |
| Host-staged credentials | ro-mount init failure; plaintext exposure | qh custody + adapters (synthetic) | mechanism YES; real-credential NO (synthetic strength) | YES | custody policy §12; real roles only via evidence-supported adapters |
| Resource gate (R1–R7) | R6 false positives/exemptions; swap FAILs | corrected lineage-bound gate `b9d5c596` (package-side; carried as evidence) | YES (19/19 matrix; live 3/3 in attempt-005) | YES (once-only invocation rule) | adopt corrected gate as mandatory prelaunch precondition, invoked exactly once |
| Identity binding by instruction text | stale binding (binding-v2 fix) | identity linter from git object store (package-side) | YES (linter battery) | YES per binding | identity linter mandatory on every transport freeze |
| Authority consumption prose | marker ambiguity | qh campaign ledger separation + this procedure's §14 rule | PARTIAL (networked-leg consumption is rule+ledger) | YES | §14 consumption table |
| Write capability asserted in prompt | Codex app-sandbox read-only | C-3 profile + GATE-W | YES (profile+matrix; runtime Landmark residual) | YES — GATE-W′ for networked profile | §13 GATE-W′ mandatory pre-inference |
| Bootstrap exception policy (one-time, revivable in REV.1) | policy abuse risk | — (governance) | N/A | YES | this proposal's lifetime = ONE-EVENT single-use, explicit expiry (§16) |

---

## 11. External auditor model — topology analysis (§15 of the task)

Candidate topologies (analysis only; NOTHING instantiated):

**OPTION H-1 — TWO EXTERNAL INDEPENDENT BLIND FIRST PASSES** (AUCDEV-010
shape, re-instantiated on the new control plane): two auditors from
DIFFERENT providers (Auditor-A: Claude Opus first-party — route
mechanically established Campaign-2 §5 and proven live in attempt-005;
Auditor-B: GPT-5.6-sol xhigh via codex-cli ChatGPT-OAuth — entitlement
mechanically evidenced, write-capability solvable via C-3 profile),
byte-identical common evidence, mechanical first-pass confinement,
barrier, zero-model reconciliation.

**OPTION H-2 — ONE BLIND PRIMARY + ONE POST-BARRIER SECONDARY
CROSS-REVIEW**: one blind first pass; after its freeze, a second
external model receives the frozen primary report + identical evidence
for coverage/completeness cross-examination.

**OPTION H-3 — SINGLE BLIND FIRST PASS + ZERO-MODEL MECHANICAL
COMPLETENESS VERIFICATION**: one blind pass; completeness enforced by
structural validator + mandatory coverage map only.

| Criterion | H-1 (two blind) | H-2 (primary+secondary) | H-3 (single) |
|---|---|---|---|
| Independence | STRONG (both pre-barrier independent) | WEAK for secondary (anchored by primary's frozen report; procedural only) | single model |
| First-pass blindness | MECHANICAL+PROCEDURAL (MIXED, §12) for both | mechanical for primary only | mechanical+procedural for the one |
| Coverage/completeness | cross-detected blind-set-wide | directly audited by secondary | mechanical only — model blind spots uncaught |
| Cost / model budget (default) | 2 engagements | 2 engagements | 1 engagement |
| Failure recovery | asymmetric-failure path defined (§15) | primary failure collapses the design (secondary has nothing to review) | single failure = event failure or re-mint |
| Authority consumption | 2 single-use | 2 single-use | 1 single-use |
| Single-point-of-failure risk | lowest (no single model is load-bearing for acceptance) | primary is SPOF for substance | the one model is SPOF |
| Ability to audit harness/protocol code (not product behavior) | both review the same frozen source + contracts | same | same |
| Historical evidence | the two-pass rule is the only governance shape with ANY conforming first pass ever produced (attempt-005); its failures were harness-side (L-01..L-24), now closed | no historical precedent at bootstrap strength | no historical precedent; contradicts the adopted policy instinct |

**RECOMMENDATION (PROPOSAL): OPTION H-1** — two external independent
blind first passes. Reasons (evidence-backed): (a) the review target is
the TRUST ANCHOR for all future qualification — the cost asymmetry
favors redundancy; (b) the historical two-pass fragility was
overwhelmingly harness/controller defect (L-01..L-04), mechanically
closed by the frozen harness + this procedure's transport rules, not
auditor-model defect; (c) H-2's secondary is procedurally anchored —
it cannot make the independence claim this bootstrap exists to
establish, and model agreement would be over-read as proof; (d) H-3
leaves single-model blind spots uncaught at the highest-leverage trust
decision. H-2/H-3 remain available as Control Room alternatives; H-2's
secondary-review SHAPE is preserved as an OPTION under a separate
addendum authority post-barrier (REV.2 rule), not as the default.

Auditor identities (PROPOSAL, subject to fresh preflight at event time):
Auditor-A = Claude Code `claude` (first-party Anthropic route;
PLAIN_CLAUDE profile; frozen executable SHA at event freeze);
Auditor-B = `codex-cli` (ChatGPT-OAuth; model gpt-5.6-sol; xhigh;
named restricted write profile per C-3). Neither derives ANY authority
from Audit Council qualification status. Providers other than these two
evidence-supported roles remain BLOCKERS, not guesses.

---

## 12. Independence, blindness, evidence parity, credential custody (§§16–18, 20)

**Auditor independence (mechanical definition, PROPOSAL)**:
auditor identity = provider + model + executable SHA-256 + CLI version,
frozen in the event FDR before launch; fresh-session requirement =
ephemeral boundary-private HOME/CLAUDE_CONFIG_DIR or CODEX_HOME (fresh
construction, census + disable-all per L-07); controller/process
identity = the exact `authorized_controller`-bound process (C-1/C4′ +
spec v3), never the auditor process; workspace isolation = fresh
per-attempt roots outside the project; evidence scope = the frozen
common evidence set ONLY; forbidden peer visibility = no peer artifact
mounted anywhere in either boundary (mechanical), blindness map proves
the negative; authority budget = DEFAULT_MODEL_ENGAGEMENTS 2 (one per
auditor), ceiling 5 only via separate authorities; single-use = each
engagement consumed at the inference-capable exec (§14); retry = NONE
silent (§14); abort = preexec stop terminal for the ATTEMPT, engagement
unconsumed if no inference-capable exec occurred.

**Blindness model: MIXED** (honest classification; mechanical blindness
claimed ONLY for the mechanically established components):
- MECHANICAL (per event, proven by gates): peer-report invisibility
  (no peer bytes in either boundary; auditor-output is each session's
  own); controller history/project memory/home/skills excluded from the
  auditor boundary (boundary composition + N-gates); `.system`/user
  skill advertisement neutralized (pre+post census, sensitivity
  control); hard no-egress during GATE-W′ rehearsal (no external
  lookup); target-embedded provenance = the frozen evidence itself
  (allowlisted class); model-specific config = fresh config dirs, no
  host config, no session history; current-event peer artifacts absent
  by construction + post-exec checker on auditor surfaces only (L-27).
- PROCEDURAL (disclosed, NOT claimed mechanical): provider-side model
  priors/training knowledge; the operator/controller staging acts
  between freeze and launch; the outer operator decision sequence.
  AUCDEV-001 (repo-level blind-independence item) remains OPEN/unresolved
  in general; each run discloses the per-run blindness statement
  (`FIRST_PASS_BLINDNESS_MIXED_MECHANICAL_PLUS_PROCEDURAL`, or
  mechanical-only subset actually proven that run).

**Evidence parity (frozen COMMON EVIDENCE SET)**: one manifest; per-file
SHA-256 + sizes; COMMON_EVIDENCE_PAYLOAD_SHA256 (REV.4 single-projection
definition); archive identity = transport digests with A=B byte parity
proven (`cmp` + recomputed payload from each handoff); target identity =
`d4d584ff…` + root/qh/skill trees, identity-linter-derived from the git
object store; requirements/contract identity = frozen harness-audit
requirements contract (NEW, event-side; no expected findings, no
expected severities, no expected recommendation, no prior-peer
substance — enforced by the allowlist blindness map); role-specific
transport delta = ONLY the role profile materialization (adapter,
config, executable pin) — no substantive instruction differences;
any other delta must be explicitly justified in the FDR or the set is
INVALID (68E3B082 precedent).

**Credential governance**: no credential bytes in any evidence package;
operator/root custody (qh custody channel pattern); boundary-local
materialization at launch; controller non-possession; no logging; no
archive inclusion; no credential hashing for publication; only the two
evidence-supported provider roles; unknown formats remain blockers.

---

## 13. RECOMMENDED PROCEDURE — "AUCDEV-023 HARNESS BOOTSTRAP AUDIT (HBA)" (PROPOSAL)

**Two-plane composition** (forced by the frozen-harness structural fact
that every qh protected launch is no-egress):

- **PLANE 1 — CONTROL/AUTHORITY PLANE (the frozen qh harness at
  `d4d584ff`, unmodified)**: operator `qh authority` Phase A trusted
  pre-controller freeze; pre-controller scope manifest (C-1); one-shot
  process-bound attempt grants (one per auditor attempt); terminal
  PREEXEC state machine; GATE-W zero-provider write-capability +
  profile rehearsal under hard no-egress with synthetic custody;
  engagement accounting ledger (operator-written); claim-only request
  discipline. Plane 1 performs EVERY authority decision and every
  zero-provider gate.
- **PLANE 2 — AUDITOR TRANSPORT PLANE (a NEW frozen event package,
  built at event-preparation time under separate authority)**:
  auditor-facing evidence transports (A=B byte parity), the networked
  launch boundary derived from the Campaign-2 v3 launcher lineage
  (`--unshare-pid`, fresh `/proc`, sentinel-invisible, root-escape
  blocked, role-minimal auth, ephemeral writable-at-init homes,
  resolver provision P12/N12, auditor-output the ONE rw bind), the C-3
  named restricted codex profile, identity linter, blindness map,
  structural validator, resource gate (`b9d5c596` lineage, invoked
  exactly once, 3 consecutive PASS immediately prelaunch), route
  readiness (non-inference), and **GATE-W′** — the networked-profile
  variant of GATE-W: identical write/permission matrix assertions, with
  the network delta (provider endpoints reachable via outer boundary;
  write matrix unchanged) explicitly justified in the FDR and proven by
  a zero-provider dynamic rehearsal with a LOCAL deterministic payload
  in the networked boundary (write semantics only; no provider
  inference). Reuse of the v3 lineage is JUSTIFIED (it is the only
  mechanically proven networked auditor boundary — attempt-005 25/25),
  not blind copying: the additions are launch-token binding and
  GATE-W′.

**Plane binding**: each auditor attempt's qh grant id + attempt id are
embedded in the transport FDR; the engagement ledger records
consumption when the inference-capable auditor CLI is exec'd after all
Plane-1 and Plane-2 gates passed (§14); the transport launch invocation
is operator-held (never controller-held); pre/post launch captures
(argv, environment digest, timestamps) make any second launch of the
same attempt mechanically detectable — classified
UNAUTHORIZED_RETRY_AFTER_PREEXEC (L-03) and terminal for the event
unless the operator explicitly pre-authorized a replacement attempt.

**Stage sequence (one event)**: S0 operator event authority (new
namespace `AUCDEV-023-HBA-<date>-01`; budget 2; new authority records)
→ S1 package preparation + freeze (transports, contracts, validator,
linter, blindness map, GATE-W′, batteries; zero provider) → S2 Control
Room package readback → S3 per-auditor: resource gate (once) →
controller scope (C-1/C4′) → qh attempt mint+bind → all mechanical
gates → launch → freeze first-pass output → structural validation →
custody → S4 barrier opens ONLY when ALL required first passes are
present+frozen+validated → S5 zero-model R0 reconciliation (identities,
coverage map, findings classification, disagreement, completeness) →
S6 Control Room readback → S7 disposition (§17/§18). No stage launches
anything automatically; every stage transition is recorded.

**Scope (§14 of the task)**: the audit TARGET is the frozen harness
`d4d584ff…` (its source, its protocol semantics, its self-test
evidence, and the trust assumptions recorded in §9's audit-focus
marks). It is NOT an Audit Council product release-qualification
campaign; no product verdict; no installation; no Campaign-3.

---

## 14. Authority consumption / retry model (§21 of the task; PROPOSAL)

| Event | Auditor authority | Model engagement | Retry permitted? | Who decides next |
|---|---|---|---|---|
| Pre-controller Phase-A failure | unconsumed | unconsumed | new preparation round | operator |
| C-1/C4′ scope fail | unconsumed | unconsumed | NO on same attempt (terminal stop); replacement attempt = new mint | operator |
| Resource-gate fail | unconsumed | unconsumed | gate once per attempt; replacement attempt = new mint | operator |
| Boundary/route/identity/custody/GATE-W′ fail BEFORE inference-capable exec | unconsumed | unconsumed | NO same-attempt retry (L-03); package-byte change ⇒ new binding_version + re-freeze + re-readback | operator |
| Purely-local provider init failure BEFORE any provider-network/inference initiation, precisely marked | unconsumed (Campaign-1 precedent) | unconsumed | replacement attempt only | operator |
| Same class with UNDETERMINABLE markers | **treated as CONSUMED (fail-closed accounting)** | consumed | — | operator |
| Inference-capable CLI exec'd (after all gates) | **CONSUMED regardless of outcome** | **consumed** | NO retry/resume/fallback/repair (Campaign-1 rule) | operator |
| Model crash / API failure / timeout post-exec | consumed | consumed | no; first pass = as-evidenced (error-only ⇒ NONCONFORMING) | operator |
| Report missing / incomplete | consumed | consumed | no reconstruction ever | operator |
| Asymmetric auditor outcome | per-side as above | per-side | replacement FIRST PASS for the failed side under NEW separate operator authority while event budget remains; else event terminal-incomplete | operator |

No silent retry by ANY controller. Re-mint requires returning to the
operator (qh root is operator-side; public `qh mint` removed — verified
in frozen source). Every replacement authority is a NEW recorded
operator authority with named scope.

---

## 15. Terminal stop mechanics (§22 of the task; PROPOSAL)

STOP conditions: ANY mandatory preexec gate raw-FAIL (scope, resource,
identity/binding, custody, route, GATE-W′, no-egress rehearsal, parity
check), unknown request field, drift of any frozen identity.
Mechanical latch: qh `TERMINAL_PREEXEC_STOP` (absorbing; process-bound
in the non-dumpable supervisor; same-UID cannot read or reset;
ledger/socket/root deletion+recreation restores nothing — verified in
frozen source + README). Observable by: operator/Control Room (ledger,
supervisor exit code); NOT resettable by: the controller (no transition
out of absorbing states; duplicate attempt-id mint refused). Subsequent
launch on the same attempt: mechanically impossible on Plane 1
(supervisor serves exactly one request); on Plane 2 classified
unauthorized retry if attempted (pre/post captures). Operator-authorized
re-attempt = NEW attempt id + NEW out-of-band mint (+ new binding if
bytes changed) + new budget accounting — never a controller act.

---

## 16. Policy lifetime (§30 of the task; PROPOSAL)

**ONE-EVENT, single-use, explicit expiry.** This procedure, if adopted,
authorizes exactly ONE bootstrap harness-audit event
(`AUCDEV-023-HBA-…-01`, budget 2 engagements). It EXPIRES
automatically when the event reaches ANY terminal state
(complete-accepted review, terminal-incomplete, or operator
abandonment). It is NOT standing authority; it does NOT revive; a
second bootstrap event requires a NEW Control Room governance decision
+ NEW operator authority (mirroring the AUCDEV-010 §7 NO-REVIVAL rule
that this proposal deliberately re-instantiates for AUCDEV-023). It
conveys NO qualification, installation, or campaign authority. It
MUST NOT silently become permanent.

---

## 17. Success transition (§31 of the task; PROPOSAL)

If the event completes with a conforming blind first-pass set + R0
reconciliation + Control Room acceptance, the resulting state is:

```
AUCDEV023_HARNESS_INDEPENDENT_REVIEW_COMPLETE
/ EVENT <exact id>
/ TARGET d4d584ffa47ad2848268ba947247f81a845b2322 (root 1d4b8b8e…, qh 5b8d5e54…, skill c792933a…)
/ BINDING <exact transport/FDR/contract digests>
/ RUN/ATTEMPT/ENGAGEMENT identities exact
/ EVIDENCE <first-pass hashes/sizes/modes + R0 record + handoff identity>
/ FINDINGS <per-auditor verdicts + reconciled classification>
/ HARNESS_ACCEPTANCE <Control Room decision>
```

The harness audit itself does **NOT** establish a qualified Audit
Council predecessor (DEFAULT NO; changing this requires a separate,
explicitly justified Control Room decision). Nothing is installed. The
exact NEXT Control Room decision after acceptance: whether, and under
what governance, this harness may be used for subsequent Audit Council
qualification work — NOT pre-authorized here.

## 18. Failure transition (§32 of the task; PROPOSAL)

Blocking harness/protocol defects found ⇒ recorded as findings;
remediation requires a NEW exact SHA; the verdict does NOT transfer;
re-audit is FRESH on the changed target. Bootstrap EXECUTION failure
before valid audit completion ⇒ do NOT infer a target defect; classify
separately as harness/controller/external/completeness per §8 classes;
target remains `d4d584ff…` untouched.

---

## 19. Finding severity / blocking semantics (§27 of the task; PROPOSAL)

Severities: CRITICAL / HIGH / MEDIUM / LOW / INFORMATIONAL. Classes:
harness-or-protocol defect; completeness limitation; external
condition; accepted residual; informational. **Default blocking rule**:
unresolved material HIGH/CRITICAL trust-boundary findings BLOCK
`HARNESS_ACCEPTANCE`. Acceptance-with-residuals is possible only for
MEDIUM/LOW/INFO findings with recorded rationale + revisit trigger, and
never for a HIGH/CRITICAL trust-boundary defect. The frozen target is
NOT pre-scored by this design; severity assignment belongs to the
auditors and reconciliation.

## 20. Acceptance state separation (§26 of the task; PROPOSAL)

```
TARGET_AUDIT_VERDICT        (auditor-reached; per-auditor + reconciled; never operator-pre-written)
AUDIT_COMPLETENESS          (blind set conforming? coverage complete? mandatory stages done?)
HARNESS_ACCEPTANCE          (operator/Control Room decision on the review as sufficient)
AUDITOR_BOOTSTRAP_SUCCESS   (governance fact: a conforming independent review path existed and operated)
QUALIFICATION               (NONE — not in scope for this procedure)
INSTALLATION                (NONE — not in scope)
```
Never collapsed: a technically valid audit may be incomplete; a
complete audit may contain blocking findings; a PASSed harness review
qualifies/installs nothing.

---

## 21. Output custody / barrier / reconciliation (§§24–25 of the task; PROPOSAL)

Per first pass: report written by the auditor to its own
`/auditor-output` (the one rw bind); at process exit frozen immediately
(mode 0444; SHA-256/size recorded; moved into attempt-root custody;
handoff archive with internal SHA256SUMS). Missing report remains
MISSING (Campaign-1/2 precedent); controller stdout/stderr are NEVER
reconstructed as the report. BARRIER-OPEN criteria (ALL required):
every required first-pass artifact PRESENT + FROZEN + structural
validator rc=0 + per-side authority accounting closed + no blindness
violation. Post-barrier reconciliation: ZERO-MODEL by default — verify
identities, map coverage (REV.2 vocabulary
COVERED_BY_FIRST_PASS_A/B / COVERED_BY_MECHANICAL_EVIDENCE /
NOT_COVERED; gaps block), classify findings, identify disagreements,
assess completeness; NEVER fabricate substance, downgrade findings,
convert model agreement into proof, or pre-write qualification.
Auditor addenda / cross-examination / adjudication: ONLY under
separate operator authority (named IDs; frozen input digests; ≤1 call
per auditor per authority; no full reopen).

---

## 22. Design options compared (§33 of the task)

| Axis | OPTION D-1 (RECOMMENDED): two-plane control + H-1 two blind passes | OPTION D-2: single-plane legacy-style package (Campaign-2 pattern rebuilt, no qh control plane) | OPTION D-3: minimal single-pass (H-3) on the two-plane control |
|---|---|---|---|
| Auditor topology | H-1 (two external blind, different providers) | H-1 | H-3 (one blind) |
| Authority model | qh operator root + one-shot process-bound attempts + operator-held transport launch | package-side authority records + prose+launcher discipline (historical) | same as D-1 |
| Model budget | 2 default; ceiling 5 separate | 2 default | 1 default |
| Blindness | MIXED w/ mechanical confinement both passes | procedural-heavy (historical label) | mechanical for the one |
| Execution/control plane | frozen qh (authority/gates) + v3-lineage networked transport | rebuilt controller/package harness (Campaign-2 style) | frozen qh + transport |
| Failure recovery | §14 table; plane separation isolates authority from transport defects | historical fragility (L-01..L-04 recreated — precisely the defects the harness closed) | single-pass failure = event failure |
| Cost/complexity | highest of the three, bounded; no source change | high (rebuild) + re-introduces closed defects | lowest |
| Historical failure coverage | L-01..L-28 covered (matrix) | L-01..L-04 NOT covered (rejects the closures) | L-29-style incompleteness risk |
| New risks | plane-binding seam (mitigated: operator-held launch + ledger + captures); GATE-W′ delta must be justified | re-learning the entire historical lesson chain at runtime | single-model blind spots at the trust-anchor decision |
| Advantages | maximal independence; proven components only; no frozen-target change; mechanical authority | familiarity | cheapest |
| Disadvantages | two planes to freeze/readback | rebuilds proven-broken pattern; violates the delta-matrix rule | under-secured trust anchor |

**RECOMMENDED: OPTION D-1** (technical governance selection,
evidence-backed per §§8–11). NOT instantiated by this record.

---

## 23. Future operator decisions required (PROPOSAL; none granted here)

1. Control Room readback of THIS proposed design (the sole next action).
2. If accepted: separate explicit operator authority for EVENT
   PREPARATION (S1 package build/freeze under the two-plane design).
3. Separate explicit operator EXECUTION authority per auditor attempt
   (S3), with the §14 consumption rules included verbatim.
4. Any replacement attempt / addendum / adjudication authority
   (separate, named).
5. Post-review: the §17 acceptance decision, and any LATER decision on
   using the harness for qualification work.

## 24. Explicit non-authorities (REQUIREMENT)

This record authorizes NOTHING executable. In particular NOT:
`/audit-council`; any auditor/model/provider execution; any campaign or
event instantiation; qualification; installation; downgrade/rollback;
source/harness/skill mutation; remediation; adoption of this procedure
as policy; execution authority under this procedure; any gate
satisfaction; any change to Campaign-2/AUCDEV-010 historical states;
any change to `INDEPENDENT_AUDITOR_PROVENANCE_GATE` (remains
NOT_SATISFIED, a Control Room disposition) or
`INDEPENDENT_HARNESS_AUDIT` (remains
BLOCKED_PENDING_AUDITOR_BOOTSTRAP_GOVERNANCE until Control Room says
otherwise).

## 25. Frozen target preservation (REQUIREMENT, held)

```
TARGET COMMIT                   : d4d584ffa47ad2848268ba947247f81a845b2322
TARGET ROOT TREE                : 1d4b8b8eb0619cf0b854984b778e6ea081ad9aa7
TARGET QUALIFICATION-HARNESS TREE: 5b8d5e5465923740470ff63ed9b8683f257a3787
TARGET SKILL TREE               : c792933a862d9a5434681a88d183470dd8b15d2f
```
This design session changed no source, no harness, no skill, no
product test/contract, no historical report, no frozen Campaign-2
artifact. Later governance-only commits (including THIS publication) do
NOT transfer or rewrite the target; any source/harness change requires
a FRESH independent audit.

## 26. Zero-execution attestation (OBSERVED_FACT)

Provider/model/frontier calls: ZERO. Auditor executions: ZERO.
`/audit-council` executions: ZERO. Campaign/event instantiations: ZERO.
Qualifications: NONE. Installations: NONE. Source/harness/skill
mutations: NONE. Credential CONTENT reads/hashes: ZERO (metadata only;
`.zcode/v2/credentials.json` noted as pre-project unrelated class).
Sealed Auditor-A/B substance: NOT opened. Historical evidence
archives: inspected read-only (extraction only to isolated /tmp for the
3 non-secret operator-doc zip members). Frozen target source: read
byte-wise via `git show`, never executed.

## 27. Publication record

Changed paths EXACTLY: NEW THIS file +
`docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` +
`docs/chatgpt-project/AUCDEV-BACKLOG.md`. NOT modified:
`qualification-harness/**` (tree `5b8d5e54…` unchanged), `skill/**`
(tree `c792933a…` unchanged), product tests/contracts,
`AUCDEV-QUALIFICATION-HISTORY.md` (no qualification/installation event
established by a PROPOSED design — update NOT_APPLICABLE per the
2026-09-10/2026-09-18 precedent), the runbook (deliberately NOT
modified — adoption is a separate decision), Project Instructions,
historical AUCDEV-010 reports, frozen Campaign-2 artifacts, the frozen
AUCDEV-023 target. Exactly ONE append-only publication commit; at most
ONE fast-forward push. Post-publication state (§36 of the task):
AUCDEV-023 remains P1/READY — NOT DONE; frozen target `d4d584ff…`
held; gate NOT_SATISFIED; audit BLOCKED_PENDING_AUDITOR_BOOTSTRAP_
GOVERNANCE; new design state
`AUCDEV023_AUDITOR_BOOTSTRAP_GOVERNANCE_DESIGN =
PROPOSED_FOR_CONTROL_ROOM_READBACK`; qualification NONE; installation
NONE; NEXT ACTION EXACTLY ONE: INDEPENDENT CONTROL ROOM READBACK OF
THIS PROPOSED AUCDEV-023 AUDITOR-BOOTSTRAP GOVERNANCE DESIGN.

Result: `AUCDEV_023_AUDITOR_BOOTSTRAP_GOVERNANCE_DESIGN_PROPOSED_FOR_CONTROL_ROOM_READBACK`.
