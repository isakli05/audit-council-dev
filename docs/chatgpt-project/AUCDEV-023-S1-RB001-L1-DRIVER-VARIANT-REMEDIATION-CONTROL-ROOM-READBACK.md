# AUCDEV-023 S1 RB-001 L1 DRIVER-VARIANT REMEDIATION — CONTROL ROOM READBACK (CANONICAL PUBLICATION)

## 1. AUTHORITY

- Authority ID: `AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-CR-READBACK-PUBLICATION-20260923-01`
- Task class: BOUNDED GOVERNANCE-PUBLICATION (record-only / append-only / zero-runtime / zero-implementation).
- The Control Room independently verified the remediated L1 source-candidate publication (commit
  `8e2f09bfd2ecf1a004e54ce31aabf782f194a3b3`, canonical record
  `docs/chatgpt-project/AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-REMEDIATION.md`, operator authority
  `AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-REMEDIATION-20260923-01`) and its generated-LAST handoff.
- This session publishes the ALREADY-DECIDED Control Room readback faithfully. It is a RECORD PUBLISHER
  ONLY; it does NOT independently re-audit or alter the Control Room disposition.
- This session is NOT authorized to (and did NOT): modify the candidate driver; modify the candidate
  boundary; modify EBS; modify packages/MANIFESTs/bindings; create an event; execute
  auditors/providers; qualify or install anything; remediate source in this task.
- ZERO runtime implementation; ZERO auditor execution; ZERO provider/model/frontier inference; ZERO
  network/provider probe; ZERO credential read; ZERO report-substance read — the Auditor-A frozen report
  `ba8a29a12867273616143e48a86f101f14f6e0e207136d83b31e7fd2426ec1a0` / 23727 B / mode 0444 is referenced
  mechanically ONLY and was NEVER opened. The vendored frozen bwrap
  (`01fb705f067bd5365b63d8ad2323a61c8d007733ca5e649437e086f3fb9935d8` / 529776 B) was NOT executed.

## 2. EXACT LIVE BOOTSTRAP (VERIFIED BEFORE ANY MUTATION)

- Repository: `isakli05/audit-council-dev` (remote `origin` = `https://github.com/isakli05/audit-council-dev.git`); branch `master`.
- Authorized baseline `8e2f09bfd2ecf1a004e54ce31aabf782f194a3b3` — verified EXACT as live GitHub master at
  bootstrap (`git ls-remote origin master`) and as local HEAD.
- Root tree `91515b16c2bc7259cc369d1ea0832acce3ef8357` — EXACT.
- Sole parent `7af938fa63af0abd3b08f7e4b176afaf0ecd6278` — EXACT (exactly one parent).
- Canonical blobs verified EXACT at the baseline:
  - `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` = `09a415cbb3988f19874d47de97eedc6abb0954c8`
  - `docs/chatgpt-project/AUCDEV-BACKLOG.md` = `3376a383b9f1661416b8390122edd97203f2f394`
  - `docs/chatgpt-project/AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-REMEDIATION.md` = `86f30d061adde17b1b2602561ca368bcc290b134`
- Protected trees verified EXACT and byte-unchanged at the baseline:
  - `bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0`
  - `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`
  - `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f`
  - the latter two EQUAL the frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322`.
- Working tree: zero tracked modifications (untracked evidence directories and launcher artifacts left
  untracked and unaltered, per protocol).

## 3. PREDECESSOR PUBLICATION IDENTITY

- Publication: commit `8e2f09bfd2ecf1a004e54ce31aabf782f194a3b3` (root tree
  `91515b16c2bc7259cc369d1ea0832acce3ef8357`; sole parent `7af938fa63af0abd3b08f7e4b176afaf0ecd6278`),
  exactly three changed paths (NEW driver-variant remediation record + CURRENT-STATE rotation + BACKLOG
  append), protected trees byte-unchanged.
- Authority: `AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-REMEDIATION-20260923-01` (NARROW DRIVER-ONLY
  REMEDIATOR + VALIDATION EXPANDER + RECORD PUBLISHER ONLY).
- Target findings: `AUCDEV023-CR-S1-RB001-L1-IMPL-RB-001` (early rc=3 progressive prefixes rejected by
  the driver validator) and `AUCDEV023-CR-S1-RB001-L1-IMPL-RB-002` (EBS exec-failure variant collapsed
  to generic metadata rejection).
- Key published artifacts: successor driver `858b825da55eb04abf127463db92721b7ee44c6323a3316b7382683b0dfddf25`
  / 149121 B (predecessor `cd4608a972bb3d1023f6a6bf8283189a8e7658bb58ca4bc9b46704f8d7fb617f` / 139721 B;
  diff `022e79cbedcce28b9ea687e52a2c144a2378c28ca17f371859c4fbc6d8016afb` / 15928 B, reported +185/−20 —
  see §10); the exact rc=3 pre-composition prefix state machine; the V-EBS-EXEC-FAILURE variant; the
  expanded suites (differential 17021/0, design suite 61/61, implementation matrix 119/119, source
  invariants 41/41); boundary `011a8713…` / wrapper `17e0abcd…` / reference classifier `d3066e81…` / EBS
  all byte-unchanged; vendored-bwrap fixture evidence REUSED with exact identity reverification.

## 4. GENERATED-LAST PREDECESSOR VERIFICATION

### 4.1 Control Room verification (recorded)

The Control Room independently verified the archive
`/home/isa/audit-council-dev/AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-REMEDIATION-HANDOFF.tar.gz`:

- Outer SHA-256 `d2e3c851be4f66fec3501ae953ea74bd2c20fefbce8db747fb8fe2953c3fb1c6`; size 788566 bytes.
- Census: 47 total members = 31 regular + 16 directories; 0 unsafe/traversal; 0 duplicates; 0 symlinks;
  0 hardlinks; 0 special files.
- SHA256SUMS: exactly one; 30 rows; 30/30 PASS; zero missing; zero unlisted.
- Archive-byte / live-Git blob equality for: remediation record `86f30d06…`; CURRENT `09a415cb…`;
  BACKLOG `3376a383…`.
- Exact packaged source identities independently re-hashed: successor driver
  `858b825da55eb04abf127463db92721b7ee44c6323a3316b7382683b0dfddf25` / 149121 B; predecessor driver
  `cd4608a972bb3d1023f6a6bf8283189a8e7658bb58ca4bc9b46704f8d7fb617f` / 139721 B; boundary
  `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa` / 41270 B; wrapper
  `17e0abcd34303d0defda2326587cb80550872e8ebdb55b1055fb880e6d06534c` / 2836 B; reference classifier
  `d3066e8199afb26190e123a5d5f44e46194e541fd730f0795c413250426297e6` / 19869 B.

### 4.2 This session's independent read-only re-verification (nothing executed)

Reproduced EXACT: outer SHA-256 `d2e3c851be4f66fec3501ae953ea74bd2c20fefbce8db747fb8fe2953c3fb1c6`;
size 788566 B; census 47 = 31 regular / 16 directories / 0 unsafe / 0 duplicates / 0 symlinks / 0
hardlinks / 0 special; exactly one SHA256SUMS with 30 rows, 30/30 PASS, zero missing, zero unlisted;
git-blob byte equality CONFIRMED for all three canonical records (remediation record / CURRENT /
BACKLOG); SHA-256 re-hash CONFIRMED EXACT for the successor driver, predecessor driver, boundary
candidate, wrapper, and reference classifier (sizes 149121 / 139721 / 41270 / 2836 / 19869 B); the
packaged exact driver diff re-hashed EXACT (`022e79cb…` / 15928 B); the packaged validation result
totals re-read (implementation matrix 119 pass / 0 fail; source invariants 41 / 0; differential 0
failures). The vendored frozen bwrap was NOT executed during this readback.

## 5. CONTROL ROOM DISPOSITION (PUBLISHED VERBATIM)

```
AUCDEV_023_S1_RB001_L1_DRIVER_VARIANT_REMEDIATION_CONTROL_ROOM_READBACK =
PUBLICATION_VERIFIED
/ GENERATED_LAST_INTEGRITY_VERIFIED
/ SUCCESSOR_DRIVER_IDENTITY_VERIFIED
/ BOUNDARY_BYTE_IDENTITY_VERIFIED
/ VENDORED_BWRAP_EVIDENCE_REUSE_ACCEPTED
/ PREDECESSOR_IMPLEMENTATION_RB_001_CLOSED_AT_IMPLEMENTATION_STRENGTH_ACCEPTED
/ PREDECESSOR_IMPLEMENTATION_RB_002_CLOSED_AT_IMPLEMENTATION_STRENGTH_ACCEPTED
/ THREE_NEW_DRIVER_DIAGNOSTIC_PERSISTENCE_FINDINGS
/ L1_SOURCE_CANDIDATE_NOT_PACKAGE_PREPARATION_READY
/ PACKAGE_MANIFEST_BINDING_EVENT_PREPARATION_BLOCKED
/ RB001_OPEN
/ REPLACEMENT_EXECUTION_NONE
/ QUALIFICATION_NONE
/ INSTALLATION_NONE
```

This does NOT reject the accepted boundary implementation. This does NOT reopen the two predecessor
findings. It establishes three NEW implementation findings in the successor driver. This is a Control
Room governance disposition. It is NOT: product qualification; package-preparation authority;
replacement-execution authorization; operator residual-risk acceptance.

## 6. ACCEPTED PREDECESSOR REMEDIATION FACTS

The Control Room independently accepts:

- `AUCDEV023-CR-S1-RB001-L1-IMPL-RB-001` = **CLOSED_AT_IMPLEMENTATION_STRENGTH** for its original
  defect: legal early rc=3 progressive prefix forms are no longer generically rejected.
- `AUCDEV023-CR-S1-RB001-L1-IMPL-RB-002` = **CLOSED_AT_IMPLEMENTATION_STRENGTH** for its original
  defect: EBS exec-failure `{}` + `exec_failed=true` is now recognized before generic identity
  validation.

Accepted mechanical facts (implementer/mechanical evidence facts ONLY — NOT independent audit PASS,
NOT qualification):

- exactly three reachable rc=3 progressive prefix classes: INITIAL, IDENTITY_ESTABLISHED, STAGING_READY;
- exhaustive 32-subset matrix: exactly 3 accepted, 29 rejected;
- explicit EBS exec-failure variant exists;
- predecessor 83 tests remain green; implementation matrix = 119/119; differential = 17021/17021;
  source invariants = 41/41; predecessor design suite = 61/61;
- boundary candidate byte identity unchanged
  (`011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa`); wrapper unchanged; EBS
  unchanged; W1/W2 absent; packages/events not regenerated.

## 7. NEW FINDING REM-RB-001

- Finding ID: `AUCDEV023-CR-S1-RB001-L1-REM-RB-001`
- Title: **PRECOMPOSITION_PROVEN_FALSE_COLLAPSED_TO_PROTOCOL_VIOLATION**
- Classification: HARNESS/PROTOCOL IMPLEMENTATION DEFECT / DIAGNOSTIC SEMANTICS LOSS / OBSERVED SOURCE
  FACT / IMPLEMENTATION-BLOCKING.
- Status: **OPEN** (implementation-blocking; to be closed by a future NARROW DRIVER-ONLY remediation).

Exact evidence (Control Room finding, independently confirmed by this session's read-only inspection
of the frozen successor driver `858b825d…`):

- The accepted design contract's outcome-discriminated union specifies
  `V-OUTER-PRE-COMPOSITION` = rc=3, no `client_returncode`, legal base/progressive prefix, exec reach =
  PROVEN_FALSE. This is mechanically sound because these variants occur before the composition and
  therefore before any auditor-client exec.
- The successor validator correctly recognizes the three legal variants
  (`ACCEPTED_PRECOMPOSITION_INITIAL` / `ACCEPTED_PRECOMPOSITION_IDENTITY_ESTABLISHED` /
  `ACCEPTED_PRECOMPOSITION_STAGING_READY`).
- BUT when any of those variants is accepted, the persisted `exec_evidence` is
  `exec_stage_class = EXEC_STATUS_PROTOCOL_VIOLATION`, `client_exec_reached = null`,
  `proof_strength = UNDETERMINED`, `transport = NOT_PRODUCED`
  (successor driver `validate_boundary_metadata_l1`, accepted-prefix return at lines 2132–2137:
  `_exec_evidence_record("EXEC_STATUS_PROTOCOL_VIOLATION", None, "UNDETERMINED", (), "",
  "NOT_PRODUCED")`).
- The implementation test explicitly asserts this behavior (per-prefix acceptance tests assert
  `client_exec_reached is None`).
- Therefore the driver recognizes the outer variant correctly but discards the stronger mechanically
  proven exec-reach fact.

Required future correction (for the future remediation authority; NOT implemented in this task):

- For every ACCEPTED `V-OUTER-PRE-COMPOSITION` variant: `client_exec_reached = false`,
  `proof_strength = PROVEN_FALSE`, with an honest finite stage representation.
- Prefer the existing finite stage `PRE_INNER_COMPOSITION_FAILURE` (already present in
  `PERSISTED_EXEC_CLASSES`, successor driver line 1719) if and only if Control Room/source review
  confirms it is semantically admissible for failures occurring before trusted INNER/composition reach.
- Do NOT add a new persisted stage enum unless necessary.
- Completed L1 classifier semantics MUST remain unchanged.

## 8. NEW FINDING REM-RB-002

- Finding ID: `AUCDEV023-CR-S1-RB001-L1-REM-RB-002`
- Title: **REJECTED_METADATA_KEYS_COMPUTED_BUT_NOT_PERSISTED**
- Classification: HARNESS/PROTOCOL IMPLEMENTATION DEFECT / FAILURE-DIAGNOSTIC EVIDENCE LOSS / OBSERVED
  SOURCE FACT / IMPLEMENTATION-BLOCKING.
- Status: **OPEN** (implementation-blocking; to be closed by a future NARROW DRIVER-ONLY remediation).

Exact evidence (Control Room finding, independently confirmed by this session's read-only inspection):

- `validate_boundary_metadata_l1()` correctly computes, for rejection: `metadata_keys` = sorted finite
  string key inventory bounded to 64 keys (successor driver lines 1993 and 2254–2255), and returns it in
  `exec_view`.
- However `evaluate_conformance()` (line 2263) persists only `attempt_result.exec_evidence`,
  `attempt_result.metadata_validation`, `attempt_result.metadata_violations` (persistence sites at
  lines ~2400–2403). It does NOT persist `exec_view["metadata_keys"]` anywhere in the attempt summary.
- Therefore the validator computes the safe keys-only diagnostic and the caller immediately discards
  it. This contradicts the accepted fail-closed persistence contract: on schema validation failure,
  VALUES rejected but safe bounded metadata key inventory + finite violation classes retained. This is
  directly relevant to the original RB-001 evidence-loss invariant.

Required future correction (for the future remediation authority; NOT implemented in this task):

- Persist a bounded safe field such as `metadata_keys` from `exec_view` when present.
- Requirements: keys only; strings only; sorted deterministically; ≤64 entries; each key bounded; NO
  values; NO raw JSON; NO exception text; NO report bytes; NO credential data.
- Accepted valid variants may use an empty/omitted safe key inventory if the variant token itself
  completely captures their exact shape, but rejected forms MUST preserve the validator-produced safe
  key inventory.

## 9. NEW FINDING REM-RB-003

- Finding ID: `AUCDEV023-CR-S1-RB001-L1-REM-RB-003`
- Title: **TRANSPORT_FAILURE_VARIANT_NOT_MATERIALIZED**
- Classification: HARNESS/PROTOCOL IMPLEMENTATION DEFECT / COMPLETENESS LIMITATION / DIAGNOSTIC VARIANT
  LOSS / IMPLEMENTATION-BLOCKING.
- Status: **OPEN** (implementation-blocking; to be closed by a future NARROW DRIVER-ONLY remediation).

Exact evidence (Control Room finding, independently confirmed by this session's read-only inspection):

- The accepted outcome-discriminated design contains `V-TRANSPORT-FAILURE` for the case where boundary
  metadata cannot be parsed/obtained after the boundary exec seam, while `timed_out = false`,
  `exec_failed = false`, and no valid boundary metadata object survives.
- The protected EBS parses the metadata pipe and reduces absent/unparseable metadata to
  `metadata or {}`. Thus under the exact frozen boundary contract, `metadata == {}` AND
  `exec_failed = false` AND `timed_out = false` cannot be a valid normal boundary metadata variant.
- The successor validator currently falls through generic identity/pre-composition checks and returns
  `REJECTED_FAIL_CLOSED` (dispatch order: V-TIMEOUT at line ~1946 → not-a-dict → V-EBS-EXEC-FAILURE →
  rc=2 forms → rc=3 prefixes → completed/legacy → else fail-closed; no transport-failure token exists in
  `ACCEPTED_METADATA_VALIDATION_TOKENS` lines 1792–1796 or `TRANSPORT_ENUM` lines 1710–1711) instead of
  preserving a finite transport-failure variant.
- Fail-closed behavior is retained, but the outcome discriminator is lost.

Required future correction (for the future remediation authority; NOT implemented in this task):

- Recognize the mechanically supported empty-metadata transport-failure envelope BEFORE generic
  identity validation, AFTER the higher-precedence timeout and EBS-exec-failure variants.
- Suggested finite result: `metadata_validation = ACCEPTED_TRANSPORT_FAILURE`; exec evidence
  `client_exec_reached = null`, `proof_strength = UNDETERMINED`, finite stage
  `EXEC_STATUS_PROTOCOL_VIOLATION` or another EXISTING finite fail-closed class supported by the frozen
  contract; `transport = UNPARSEABLE_FAIL_CLOSED` or an equivalent EXISTING finite transport token
  (i.e., extend `TRANSPORT_ENUM` minimally with the new finite token; do NOT invent raw transport
  bytes).
- Do NOT change EBS. Nonempty malformed boundary metadata remains `REJECTED_FAIL_CLOSED`.

## 10. NON-BLOCKING EVIDENCE DISCREPANCY (INFORMATIONAL, PROSPECTIVE CORRECTION)

`AUCDEV023-CR-S1-RB001-L1-REM-INFO-001` = **DRIVER_DIFFSTAT_ADDITION_COUNT_MISMATCH** — recorded
separately as INFORMATIONAL / EVIDENCE-METADATA CORRECTION.

- The packaged exact diff (SHA-256 `022e79cbedcce28b9ea687e52a2c144a2378c28ca17f371859c4fbc6d8016afb`,
  15928 bytes) mechanically contains **+187 / −20** ordinary content-line changes (excluding diff
  headers).
- The remediation record / final return reports **+185 / −20**.
- The exact diff SHA, successor driver SHA and byte size are correct; the discrepancy does NOT
  invalidate candidate identity.
- This readback corrects the fact prospectively (+187/−20). No predecessor history is rewritten. (This
  session independently recomputed the diffstat both from the packaged diff and from a fresh `diff -u`
  of the two packaged drivers: both yield +187/−20.)

## 11. RESULTING CANDIDATE STATE

- Boundary candidate: **ACCEPTED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH** — SHA-256
  `011a87139254b7199ec55566074ea4da2324c7986337313d30c50670be403cfa` / 41270 B. Do NOT modify the
  boundary candidate.
- Vendored-bwrap fixture evidence: **ACCEPTED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH**. Do NOT
  rerun vendored bwrap unless a new dependency is introduced.
- Successor driver `858b825da55eb04abf127463db92721b7ee44c6323a3316b7382683b0dfddf25` / 149121 B:
  **NOT YET PACKAGE-PREPARATION READY** — REM-RB-001, REM-RB-002 and REM-RB-003 must be closed by
  another NARROW DRIVER-ONLY remediation before any package/MANIFEST/binding/event preparation
  authority.
- RB-001 remains OPEN with the operator-accepted L1 ambiguity residual recorded separately.
- AUCDEV-023 remains P1 / READY / NOT DONE (counts UNCHANGED: READY 9 / OPEN 7 / BLOCKED 3 = 19 open;
  P0 2 / P1 7 / P2 11).

## 12. RB-001 / AUCDEV-023 RESULTING STATE

- Historical finding `AUCDEV023-CR-S1-EXEC05-RB-001` (RB-001) remains **OPEN**, with its historical
  classification UNCHANGED: COMPLETENESS LIMITATION / FAILURE-DIAGNOSTIC EVIDENCE GAP / OBSERVED FACT /
  ROOT_CAUSE_UNRESOLVED / NO_PRODUCT_DEFECT_CONCLUSION_YET; the operator-accepted residual
  (`SE` + positive-nonzero-rc + report-absent = `EXEC_CALL_ATTEMPTED_TRANSITION_AMBIGUOUS` / null /
  UNDETERMINED) remains recorded separately and implemented honestly; W1/W2 remain DEFERRED/ABSENT.
- EXEC-05 authority `AUCDEV-023-S1-FIRSTPASS-EXEC-20260922-05` remains CLOSED / NO_RERUN /
  NON-TRANSFERABLE with budget 2/2 charged fail-closed and barrier
  CLOSED_PENDING_CONTROL_ROOM_MECHANICAL_READBACK.
- Attempts `evt-79182989824ce966-A-01` / `evt-79182989824ce966-B-01` remain TERMINAL.
- Auditor-A report substance remains sealed/unread.
- Installed runtime source remains historically recorded as `8ae33444f349ce73c1359b963722e2d16acba630`
  with installed qualified source/provenance NOT ESTABLISHED.
- Qualification: NONE. Installation: NONE.

## 13. AUTHORITY BARRIERS (EXPLICIT)

- package preparation authority = NONE;
- MANIFEST regeneration authority = NONE;
- binding regeneration authority = NONE;
- event generation authority = NONE;
- replacement execution = NONE (no replacement event prepared; attempts of `evt-79182989824ce966`
  remain TERMINAL; same-event new attempts NOT EXPRESSIBLE under the frozen EBS attempt derivation);
- auditor/provider/model execution = NONE;
- qualification = NONE;
- installation = NONE;
- source remediation in THIS task = NONE (this session publishes the readback only).

## 14. NEXT ACTION (EXACTLY ONE)

CONTROL ROOM PREPARATION OF A NARROW DRIVER-ONLY REMEDIATION PROMPT FOR
`AUCDEV023-CR-S1-RB001-L1-REM-RB-001` / `AUCDEV023-CR-S1-RB001-L1-REM-RB-002` /
`AUCDEV023-CR-S1-RB001-L1-REM-RB-003` BEFORE ANY PACKAGE / MANIFEST / BINDING / EVENT PREPARATION
AUTHORITY.

The remediation must target the successor driver ONLY (base `858b825d…`); the boundary candidate
`011a8713…`, wrapper `17e0abcd…`, reference classifier `d3066e81…`, EBS, packages, MANIFESTs, bindings
and event state remain unchanged; vendored bwrap is NOT rerun unless a new dependency is introduced;
completed L1 classifier semantics MUST remain unchanged.

## 15. PUBLICATION MECHANICS

- Exactly 3 changed paths: this NEW record + `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`
  (current-facing fields + next-operator-action rotation with the previous action preserved append-only
  under the "previously recorded next actions" section + one new dated record; every other line
  byte-identical) + `docs/chatgpt-project/AUCDEV-BACKLOG.md` (one dated record appended; every earlier
  line byte-identical).
- No predecessor record rewritten (including
  `docs/chatgpt-project/AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-REMEDIATION.md`); ARCHITECTURE-SUMMARY,
  bootstrap-supervisor / qualification-harness / skill trees, candidate boundary, candidate driver,
  wrapper, reference classifier, EBS, packages, MANIFESTs, bindings, events and attempt state all
  UNCHANGED.
- Exactly ONE fast-forward publication commit whose sole parent is
  `8e2f09bfd2ecf1a004e54ce31aabf782f194a3b3`.
- The generated-LAST reviewer handoff
  (`AUCDEV-023-S1-RB001-L1-DRIVER-VARIANT-CR-READBACK-PUBLICATION-HANDOFF.tar.gz`) is produced AFTER
  the push; nothing mutates after archive generation.
