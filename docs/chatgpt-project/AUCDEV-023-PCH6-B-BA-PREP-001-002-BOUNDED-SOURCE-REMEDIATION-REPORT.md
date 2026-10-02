# AUCDEV-023 PCH6-B — BA-PREP-001 / BA-PREP-002 Bounded Source Remediation — Implementation Record (2026-10-02)

Status banner: **REMEDICATION IMPLEMENTED AS CANDIDATE / AWAITING_FRESH_CONTROL_ROOM_READBACK /
FINDINGS NOT CLOSED BY THE IMPLEMENTER / NO EXECUTION AUTHORITY / EVENT-PACKAGE PREPARATION STILL
HELD / EVENT NOT INSTANTIATED / ATTEMPT AUTHORITIES NOT GRANTED / MODEL ENGAGEMENTS USED 0 /
NO AUDIT EXECUTION / NO AUDIT PASS / QUALIFICATION NONE / INSTALLATION NONE**

## 0. Authority and role

This session is the explicitly authorized REMEDIATION IMPLEMENTER for exactly the two
Control-Room-verified blocking findings:

- `AUCDEV023-CR-PCH6B-BA-PREP-001` `ATTEMPT_GLOBAL_ONE_SHOT_BYPASS_VIA_CALLER_SELECTED_OUTPUT_ROOT`
- `AUCDEV023-CR-PCH6B-BA-PREP-002` `REPORT_ACCEPTANCE_SOURCE_NOT_BOUND_TO_FROZEN_OUTPUT_CUSTODY`

under remediation-implementation authority
`AUCDEV-023-PCH6B-730D2B29-BA-PREP-001-002-REMEDIATION-IMPLEMENTATION-20261002-01`
(operator grant received after the event-package preparation preflight Control Room HOLD
publication Control Room verification at `cfff321bd206b246f61cdc6ad6294bbe30489134` recorded the
two findings CONFIRMED OPEN BLOCKING and named exactly this operator decision as the next action).

THIS AUTHORITY IS REMEDIATION IMPLEMENTATION ONLY. This session is NOT an event-package preparer,
NOT an event-instantiation authority, NOT an attempt-execution authority, NOT Auditor-A/B, NOT an
independent auditor, NOT an Audit Council /audit-council executor, NOT a provider/model/frontier
executor, NOT a qualification authority, NOT an installation authority. This remediation does NOT
close either finding (findings close only through the Control Room), does NOT release the
FAIL-CLOSED HELD event-package preparation authority, and grants no authority of any kind.

Zero-provider / zero-network discipline held for the whole session: ZERO provider/model/frontier
calls, ZERO client inference calls, ZERO auditor execution, ZERO /audit-council execution, ZERO
wrapper/driver invocation in the AUCDEV-023 governance chain, ZERO package-manager/PyPI/npm fetch
(PIP_NO_INDEX=1 UV_OFFLINE=1 for every test command; pre-existing local pytest bytes via uv's
offline cache + /usr/bin/python3 Python 3.14.7, the interpreter of record), ZERO credential-content
access, ZERO sealed-substance access. All fixtures SYNTHETIC / NON-AUTHORITATIVE / ZERO-PROVIDER /
NON-PERSISTENT. The only network operations are the ordinary Git/GitHub publication mechanics:
fetch, ls-remote, the one authorized push and the post-push GitHub readback.

## 1. Exact live bootstrap and identity

Live GitHub master == local HEAD == origin/master ==
`cfff321bd206b246f61cdc6ad6294bbe30489134` EXACT at bootstrap (ls-remote authoritative; fetch
clean rc 0; re-resolved EXACT again immediately before staging and immediately before commit).
Authorized base root tree `bae48da3fbdb1c1a37fe953c20fb3fc8c960cb5e`; sole parent
`77563029873bf08d19dea3eee7d5b8ab13cead3d` (the BA-PREP HOLD publication Control Room
verification; single-parent fast-forward geometry; second parent absent rc 1); trust anchor
`3058868416241d394cfaaa40cc585085db486f37` ancestor rc 0; zero merges since the anchor; zero
staged content before this remediation; the pre-existing untracked drift and the pre-existing
smoke-fixture / smoke-fixture-103 gitlink drift preserved UNSTAGED (tracked-dirty count 2,
unchanged from before this session). The frozen audit target
`730d2b29f7c0e7d33af3451b6d9205ec27c143ed` remains AUDIT SUBJECT / NOT AUTHORITY / UNTOUCHED.
This report's path was ABSENT at the base (rc 1) with zero full-history path rows.

## 2. Demonstrated defects (re-derived at the exact base before any edit)

Both defects were FIRST demonstrated live by synthetic probes against the UNMODIFIED base
(preserved in the untracked evidence workspace `aucdev023-pch6b-ba-prep-remediation-evidence`,
outputs 01-red1-defect-probes.out, 2 passed):

- BA-PREP-001: `run_attempt` received `output_root` from the caller (runtime.py:1210-1212);
  `accounting_name` correctly keyed the attempt-global O_EXCL claim by the reserved attempt id
  alone (runtime.py:202-208, BA-RB-001 remediation INTACT) while `AccountingStore.create`
  (accounting.py:98-123) obtained the O_EXCL claim INSIDE the caller-selected root; the binding
  froze NO custody-root identity (binding.py OUTPUT_IDENTITY exact keys kind+name only); the
  probe minted a SECOND authority claim `<attempt_id>.jsonl` for the SAME reserved attempt inside
  a caller-selected alternate otherwise-valid 0700 root.
- BA-PREP-002: `run_attempt` accepted `report_staging_path` from the caller (runtime.py:1211,
  type-validated only); the binding froze no report-source locator; runtime snapshotted the
  CALLER-selected path with zero staging-to-binding comparison; the probe substituted a DIFFERENT
  pre-existing regular file containing an otherwise structurally and semantically VALID first-pass
  report for the SAME target/event/role/attempt and the authority snapshotted, validated and FROZE
  the substituted bytes (and then discarded the substituted file as if it were the attempt-owned
  staging artifact).

## 3. Remediation design (narrowest mechanically sound fix)

The authoritative custody and report-source identities are now BINDING-FROZEN authority
dimensions, and every authority action uses the FROZEN binding values exclusively:

- binding.py: `output_identity` now carries exactly `kind`, `name`, `custody_root`,
  `report_source` (constant `OUTPUT_IDENTITY_FIELDS`). Both new dimensions must be canonical
  absolute host paths (validator `_frozen_abs_path`: str, 2..4096 chars, printable — no control
  characters — leading '/', no empty / '.' / '..' segments, no trailing '/', filesystem root
  refused), so the FROZEN form IS the canonical comparison form. Both dimensions are automatically
  digest-covered (`Binding.digest` = SHA-256 over the canonical whole binding document) and
  automatically transported (the event-package manifest `transport_binding` equals
  `binding_projection`, which covers every TOP_LEVEL dimension; the projection and digest coverage
  are machine-checked by the extended BA-22 digest matrix and the existing projection tests).
- runtime.py: `run_attempt` performs the identity gate BEFORE any custody open, attempt-global
  O_EXCL claim, dynamic gate or credential read: `os.path.normpath` of the caller-supplied
  `output_root` / `report_staging_path` must equal the frozen `custody_root` / `report_source`
  EXACTLY, else `AuthorityRefused` with the fixed tokens `OUTPUT_CUSTODY_ROOT_MISMATCH` /
  `REPORT_SOURCE_MISMATCH` (pre-advance refusal: the authority object stays PREPARED, nothing
  acquired, nothing executed, credential source never read). Inside the lifecycle the authority
  then uses ONLY the frozen values: `open_custody_dir(frozen_output)`,
  `AccountingStore.create(frozen_output, attempt_id, digest)`, and
  `self._staging_path = frozen_source` — the caller values are never used for any authority
  action. The frozen identities are additionally recorded as durable non-secret binding facts at
  CONSUMED_PRE_EXEC (`output_custody_root`, `report_source`).
- Exact identity semantics documented and regression-pinned: identity = exact equality of the
  normpath-normalized absolute path against the binding-frozen canonical form; syntactic aliases
  that normalize to the frozen form are harmless (the frozen value is what is used); every OTHER
  name for the same object — including a symlink alias — is a different name and is REFUSED
  fail-closed. The authority never opens the caller string, so no alias comparison weakness
  exists; final-component symlink and regular-file protections remain those of the UNCHANGED
  `open_custody_dir` / `snapshot_staging` primitives.
- accounting.py and reportcustody.py are UNCHANGED (byte-identical to their pinned pre-target
  blobs; see §5): the freeze belongs at the authority boundary (binding + runtime), not inside
  the reused primitives, and no primitive change was needed.

Why the invariants now hold mechanically:

- BA-PREP-001: ONE reserved attempt identity -> ONE mechanically authorized process-bound
  one-shot authority. A caller cannot mint a second claim for the SAME reserved attempt by
  selecting a different root: the mismatch is refused before the O_EXCL namespace is even
  reachable, and the one namespace that IS reachable is the binding-frozen custody root. A second
  process for the same attempt under the SAME frozen root still fails at the existing
  attempt-global O_EXCL claim (BA-RB-001 semantics unchanged).
- BA-PREP-002: frozen invocation -> exact mechanically authorized attempt-owned report source ->
  immutable snapshot -> credential screen -> structural validation -> semantic binding -> frozen
  first pass. Acceptance snapshots ONLY the binding-frozen report source; a substituted
  pre-existing regular file is refused at the identity gate before anything executes, before any
  stdout/stderr fallback consideration, and the honest REPORT_MISSING semantics for an absent
  frozen source are retained unchanged.

## 4. Exact change surface (ten paths, no eleventh tracked path)

MODIFY (7 package paths):

- `bootstrap-authority/bootstrap_authority/binding.py`
  `b6d14302719316dc2508451cea12d9fb2d75094a` -> `d209bc70f2799bad489ef12ce9ff9c341d3753b5`
  (OUTPUT_IDENTITY_FIELDS + `_frozen_abs_path` validator + parse-time freeze; comment-budget
  compression elsewhere; 573 -> 585 LOC)
- `bootstrap-authority/bootstrap_authority/runtime.py`
  `26e7e3814069f1280484ef759d6cee79980535b8` -> `2e2fbf8cde75a09a92606857b4f75db2f51d36e3`
  (the pre-advance identity gate; frozen-value-exclusive custody open / O_EXCL claim / staging
  snapshot; durable output_custody_root / report_source facts; comment-budget compression;
  1725 -> 1713 LOC)
- `bootstrap-authority/tests/conftest.py`
  `c7f99014245ffef6ece853507f37c940daea8f12` -> `400231839cb105cc5b32ca0222e1bb26b1a7e0e5`
  (fixtures freeze the real world custody root / report source into every synthetic binding;
  `build_world(output_root=...)` override for shared-root worlds)
- `bootstrap-authority/tests/test_binding.py`
  `b4c54a2adbf19bedd7b3b88c64017fd1b44c1791` -> `55be2093b9659c73567e9fdb472c04a1d74dde00`
  (BA-22 digest matrix extended with the two new dimensions; missing-dimension, non-canonical
  path and exact-parse tests)
- `bootstrap-authority/tests/test_runtime.py`
  `9bdeaaf0ac54324f5bbad1d9a62ed98ae195b87c` -> `a7826b711babe05ab609bf6b76fe2cca88e145f6`
  (the four adversarial BA-PREP regressions; the two BA-RB-001 shared-root regressions now
  construct the second world with the shared root FROZEN into its binding)
- `bootstrap-authority/README.md`
  `3cd8506dc541fe5443f7e376525fe04b9f14da9c` -> `5b06359c203c44dce6497ad46cc4ef7da9ffd71e`
  (documents the frozen dimensions, the identity gate and the fail-closed refusal semantics)
- `bootstrap-authority/MANIFEST.json`
  `db2f2a096297ec83c3dd8e4e9f0d3c57908883dd` -> `7d55d823ec77dc03571cb99f899c3e4e7f75566e`
  (regenerated LAST from the final package bytes; raw MANIFEST SHA-256
  `121a70cf2acb9f641959e850859e43faacfe07ece70efe6ce150f4ed90d5d1fb`; non-circular
  package_sha256
  `9e76c0df7b66177ab25e8a78e0497f72fabc56981cbd06afc0b521dbeb5e9bd1`; exactly six changed rows,
  each equal in size/SHA-256 to the final live bytes; 12 rows; schema/package/policy_id/target/
  design ids/status/qualification_claim/runtime_dependencies/source_provenance preserved EXACT)

ADD (1): `docs/chatgpt-project/AUCDEV-023-PCH6-B-BA-PREP-001-002-BOUNDED-SOURCE-REMEDIATION-REPORT.md`
(THIS record).

MODIFY (2 governance, per AUCDEV-PROJECT-UPDATE-PROTOCOL.md "Remediation completed"):
`docs/chatgpt-project/AUCDEV-CURRENT-STATE.md`
(`56059edfdf2e2247c05d8a57a94432bd4fb83e2a` -> rotation confined EXACTLY to lines 3/11/23-25
plus one dated tail record; 1336 -> 1379 wc-l) and
`docs/chatgpt-project/AUCDEV-BACKLOG.md`
(`352ea17dbbe49aaa9b37cd13efbf13a97841881b` -> one NEW dated status bullet inserted immediately
after the BA-PREP HOLD publication Control Room verification status bullet plus one NEW dated
tail record; 4179 -> 4243 wc-l). Both diffs zone-verified by script at build time AND re-asserted
from the staged blobs.

test_static.py is NOT modified: EXPECTED_PACKAGE_PATHS, the pinned pre-target reuse blobs, the
provenance contract and the unchanged LOC bound 3000 all still hold as-is.

## 5. Held invariants — verified unchanged

- The four EXACT pre-target reuse blobs byte-identical: statemachine.py
  `cf563d2178907e7666ce661b81ab1bf16fb71201`, accounting.py
  `03de6f663db283cf99f6a98e26e752a24457c52a`, custody.py
  `37e6b5bb4365c7b29ba3632fe95362d5a7e16c09`, reportcustody.py
  `18f1cc600c684e520b72026e0b4cdf8ba6287cb9`; plus `__init__.py`
  `5db170f1143950de69320548962c29d68d6e697a`. BA-RB-001 closure retained in its demonstrated
  scope (attempt-global O_EXCL name still the reserved attempt id ALONE, digest-independent,
  digest still durable and inspection-bound in every record). BA-RB-002 closure retained (gates
  still strictly before credential materialization; execution order CLIENT_SELECTION_PREFLIGHT
  -> NETWORK_READINESS -> RESOURCE_GATE LAST -> durable GATES_PASSED -> custody ->
  CONSUMED_PRE_EXEC -> irreversible spend -> immediate launch unchanged). BA-RB-003 retained.
- Report protections all retained: no-follow behavior, regular-file requirement, size bound,
  exactly one immutable snapshot, credential leak screen, structural validator, semantic
  target/event/role/attempt binding, 0444 O_EXCL freeze — reportcustody.py untouched.
- Protected trees byte-identical at the staged write-tree: bootstrap-supervisor
  `3056e577259ab0b0b0472f82ebc306506f3e084c`, qualification-harness
  `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill `efd8c2e48edbb25795b3aacb1ce3c23fde10082a`.
- Production LOC exactly 3000 <= the unchanged 3000 ceiling (per-file: __init__ 35, binding 585,
  statemachine 102, accounting 235, custody 211, reportcustody 119, runtime 1713); achieved by
  comment-budget compression only — NO safety logic deleted, NO ceiling change, no test weakened.
- No public grant/consume/resume/retry/adopt_report/finish/mint_attempt/create_event capability
  introduced; the run_attempt signature is unchanged (machine-checked by BA-31).
- The new refusals are pre-consumption, pre-advance and pre-gate: no credential byte read, no
  dynamic gate executed, no O_EXCL claim attempted on a mismatch (machine-checked by the new
  regressions).

## 6. Adversarial regression coverage (deterministic, zero-provider)

- `test_ba_prep001_alternate_output_root_refused_fail_closed`: for the SAME binding/package and
  reserved attempt, a caller-selected alternate otherwise-valid 0700 root is refused with
  OUTPUT_CUSTODY_ROOT_MISMATCH BEFORE any credential read (every synthetic credential byte still
  readable from the source pipe), the alternate root contains NOTHING (no `<attempt_id>.jsonl`
  namespace acquired), no dynamic gate executed (order file absent), no claim/staging anywhere;
  the SAME authority object remains PREPARED and the FROZEN root then succeeds under normal
  synthetic execution; a SECOND process for the SAME attempt under the SAME frozen root still
  refuses at RECORD_CREATE_REFUSED (attempt-global O_EXCL retained).
- `test_ba_prep001_symlink_alias_output_root_refused`: a symlink alias of the frozen custody root
  is a different name and is refused pre-consumption.
- `test_ba_prep002_report_source_substitution_refused`: a DIFFERENT pre-existing regular file
  containing an otherwise structurally and semantically VALID report for the SAME
  target/event/role/attempt is refused with REPORT_SOURCE_MISMATCH pre-consumption; the
  substituted file is NOT accepted, NOT frozen, NOT discarded; no stdout/stderr fallback; no
  output artifacts; the SAME authority object remains PREPARED and the honest REPORT_MISSING
  semantics of an absent frozen source are retained through a normal run.
- `test_ba_prep002_symlink_alias_report_source_refused`: a symlink alias of the frozen report
  source is refused; the normal path through the EXACT frozen source still freezes
  (REPORT_FROZEN).
- Existing symlink / non-regular / size / credential-screen / structural / semantic-binding
  regressions all still pass unchanged; the SAME-root duplicate-attempt regression and the
  cross-binding SAME-root BA-RB-001 regression still pass (the latter now with the shared root
  frozen into BOTH bindings, so the O_EXCL refusal — not the new identity gate — is what it
  exercises); distinct reserved attempts remain independent namespaces under one frozen root.
- Binding-plane: missing `custody_root`/`report_source` refused; relative / dot-segment /
  redundant-separator / trailing-slash / root / control-character / non-str values refused; the
  exact frozen pair parses back EXACTLY; the BA-22 digest matrix now also proves swapping either
  dimension changes `Binding.digest`.

## 7. Validation evidence (every command, honest outcomes)

- RED-1 defect probes on the UNMODIFIED base (01-red1-defect-probes.py):
  2 passed, exit 0 — both defects DEMONSTRATED (alternate root minted the same-attempt claim;
  substituted report frozen and discarded as staging). Probes are untracked instruments, never
  staged.
- RED-2 committed regressions BEFORE production code: test_binding -k ba_prep 10 failed /
  2 passed, exit 1; test_runtime -k "ba_prep or rb001" 6 failed, exit 1 — all failing at the
  missing schema dimension (`OUTPUT_IDENTITY_KEYS_INVALID: unknown=['custody_root',
  'report_source']`), the expected missing-feature failure (outputs 02/03).
- After implementation: focused ba_prep + rb001 runs green; full package suite
  `PIP_NO_INDEX=1 UV_OFFLINE=1 uv run --offline --no-project --python /usr/bin/python3 --with
  pytest python -m pytest -q bootstrap-authority/tests` -> **123 passed, 0 failed, 0 errors,
  0 skips, exit 0** (binding 61 / runtime 29 / static 33; +15 tests vs the prior 108), re-run
  green again from scratch after the FINAL MANIFEST regeneration (outputs 07/08/09).
- `git diff --check` and staged `git diff --cached --check` PASS (battery G7).
- Final staged full-suite staged-tree binding: PRE_TEST_STAGED_TREE == POST_TEST_STAGED_TREE
  around the final complete suite run on the final staged bytes (recorded in the evidence
  workspace and the generated-LAST handoff; the Control Room does not rerun pytest by policy).
- Full precommit gate battery on the FINAL staged bytes: ALL PASS (path-set/protected trees/
  lineage blobs/no-jsonl/staged==working/queue recount/sealed-identity/credential scan/
  hex allow-set/wording gates — see the battery output member).

## 8. Honest session iteration accounting (instrument-side; no defect rewritten as PASS)

- T-1: RED-1 probe v1 crashed EBADF closing the already-consumed credential source fd in its
  finally block after the (successful, defect-demonstrating) runs; corrected with a tolerant
  close. No repository state change.
- T-2: RED-1 probe v2 read the substituted file AFTER run_attempt and hit FileNotFoundError —
  the authority had discarded (unlinked) the substituted file as staging, which IS the defect
  being demonstrated; corrected by capturing the bytes before the run.
- T-3: RED-2 binding parametrize originally included a bytes value that cannot pass canonical
  JSON serialization (TypeError before parse); removed — the non-str case is already covered by
  the int case. Test-instrument defect, no production change.
- T-4: the first full-suite run used uv's default Python 3.11.15, whose build lacks
  os.memfd_create, producing one false failure; corrected by pinning --python /usr/bin/python3
  (Python 3.14.7, the interpreter of record) — the suite is green there.
- T-5: after each package byte change the package self-identity correctly refused constructions
  until MANIFEST.json was regenerated from the final bytes (the fail-closed mechanism working as
  designed, not a defect); a deterministic regenerator instrument was built and the FINAL
  regeneration followed the final byte change.
- T-6: LOC compression 3051 -> 3000 EXACTLY over several measured passes (comment-budget
  compression and five interior blank-line removals in binding.py; several Edit attempts were
  rejected as no-ops or stale matches and were re-applied; NO safety logic deleted, NO ceiling
  change). After the final count the full suite re-ran green from scratch.

## 9. Governance disposition

- `AUCDEV023-CR-PCH6B-BA-PREP-001`: REMEDIATION_IMPLEMENTED / AWAITING_FRESH_CONTROL_ROOM_READBACK
- `AUCDEV023-CR-PCH6B-BA-PREP-002`: REMEDIATION_IMPLEMENTED / AWAITING_FRESH_CONTROL_ROOM_READBACK
- Neither finding is CLOSED by this implementation. BA-RB-001 = CLOSED_AT_CONTROL_ROOM_REMEDIATION_
  READBACK_STRENGTH, BA-RB-002 = CLOSED_AT_CONTROL_ROOM_REMEDIATION_READBACK_STRENGTH,
  BA-RB-003 = CLOSED_BY_FRESH_BOUND_EVIDENCE — all RETAINED, not reopened. Historical
  informational residuals retained without rewrite; historical handoffs NOT repacked.
- The operator's event-package preparation authority remains RECEIVED / NOT EXECUTED / NOT
  CONSUMED / FAIL-CLOSED HELD; this remediation publication does NOT release it and is NOT
  converted into any preparation or execution authority. Event NOT instantiated; attempt
  authorities NOT granted; new-lineage model engagements USED 0 with PROPOSED 2 unchanged;
  historical PCH6 authority CONSUMED / TERMINAL / CLOSED / NO_RERUN, identities NON-TRANSFERABLE;
  PCH6-B-SD-002 and PCH6-CR-BSD-001 remain NOT CLOSED awaiting fresh independent audit of the
  frozen target; PCH6-B-SD-001 RETAINED / OPEN; ROOT_CAUSE_NOT_ESTABLISHED unchanged with no
  causal conversion; the independent-auditor provenance gate remains NOT_SATISFIED (installed
  Audit Council source `8ae33444f349ce73c1359b963722e2d16acba630` predecessor provenance NOT
  ESTABLISHED, not relabeled); AUCDEV-023 P1 / READY / NOT DONE; AUCDEV-024 P1 / READY / NOT
  DONE; qualification NONE; installation NONE; NO audit execution; NO audit PASS; no
  /audit-council execution authorized. Disposition token form:
  `AUCDEV_023_PCH6B_BA_PREP_001_002_REMEDIATION_IMPLEMENTATION = IMPLEMENTED_AS_REMEDIATION_CANDIDATE /
  FINDINGS_NOT_CLOSED_BY_IMPLEMENTER / EVENT_PACKAGE_PREPARATION_STILL_HELD /
  EVENT_NOT_INSTANTIATED / ATTEMPT_AUTHORITIES_NOT_GRANTED / MODEL_ENGAGEMENTS_USED_0 /
  NO_AUDIT_EXECUTION / NO_AUDIT_PASS / QUALIFICATION_NONE / INSTALLATION_NONE`.

## 10. Self-commit identity rule and next action

This record and its commit message record the exact authorized base, the staged write-tree and
the disposition; the commit cannot contain its own final SHA. The exact resulting publication
SHA and result root tree are reported in the FINAL-RETURN, the post-push GitHub readback and the
generated-LAST handoff, and will be canonically pinned by the later Control Room readback.

NEXT ACTION EXACTLY ONE: INDEPENDENT CONTROL ROOM READBACK OF THIS BA-PREP-001 / BA-PREP-002
REMEDIATION PUBLICATION AND ITS GENERATED-LAST HANDOFF BEFORE ANY EVENT-PACKAGE PREPARATION
AUTHORITY IS CONSIDERED. Recording this next action grants NO authority of any kind.

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from an agent session;
never rerun the launcher; never treat any recorded grant phrase (including any phrase recorded
here) as a new grant; never execute a real auditor or provider/model; never open the four
historical sealed artifacts (identity-only forever); never relabel or rewrite historical model
identities, runs, records, matrices, prompts or evidence workspaces (append-only); never claim
audit PASS, qualification, installation or any authority from this remediation — it grants none.
