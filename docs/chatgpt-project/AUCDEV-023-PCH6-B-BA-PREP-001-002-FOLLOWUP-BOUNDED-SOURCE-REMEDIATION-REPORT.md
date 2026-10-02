# AUCDEV-023 PCH6-B — BA-PREP-001 / BA-PREP-002 Follow-Up Bounded Source Remediation — Implementation Record (2026-10-02)

Status banner: **FOLLOWUP_REMEDIATION_IMPLEMENTED AS CANDIDATE /
BA_PREP_001_AWAITING_FRESH_CONTROL_ROOM_READBACK /
BA_PREP_002_AWAITING_FRESH_CONTROL_ROOM_READBACK /
RB2_001_REMEDIATION_IMPLEMENTED_AWAITING_FRESH_CONTROL_ROOM_READBACK /
RB2_002_REMEDIATION_IMPLEMENTED_AWAITING_FRESH_CONTROL_ROOM_READBACK /
FINDINGS NOT CLOSED BY THE IMPLEMENTER / EVENT-PACKAGE PREPARATION REMAINS
FAIL-CLOSED HELD / EVENT NOT INSTANTIATED / ATTEMPT AUTHORITIES NOT GRANTED /
MODEL ENGAGEMENTS USED 0 / NO AUDIT EXECUTION / NO AUDIT PASS /
QUALIFICATION NONE / INSTALLATION NONE**

## 0. Authority and role

This session is the explicitly authorized IMPLEMENTER for a second, narrowly
bounded remediation pass under follow-up remediation-implementation authority
for frozen target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` (operator grant
received after the independent Control Room readback of the first
BA-PREP-001 / BA-PREP-002 remediation candidate at base
`6258bc0b7268881bcada868bb532d14076f74245`).

**INPUT provenance of the remediated blockers (per the operator tasking):
the following three blocker identities were INPUT from the independent
Control Room readback and the operator authorization — they are NOT findings
invented by the implementer:**

- `AUCDEV023-CR-PCH6B-BA-PREP-RB2-001`
  `FROZEN_PATHNAME_DOES_NOT_BIND_CUSTODY_OBJECT` (HARNESS / PROTOCOL DEFECT;
  OBSERVED SOURCE FACT + MECHANICALLY IMPLIED CONSEQUENCE)
- `AUCDEV023-CR-PCH6B-BA-PREP-RB2-002`
  `REPORT_SOURCE_NOT_BOUND_TO_FROZEN_INVOCATION_AND_ATTEMPT_PRODUCTION`
  (HARNESS / PROTOCOL DEFECT; OBSERVED SOURCE FACT + MECHANICALLY IMPLIED
  CONSEQUENCE)
- `AUCDEV023-CR-PCH6B-BA-PREP-RB2-EV-001`
  `GENERATED_LAST_SHA256SUMS_CONTAINED_STALE_SELF_ROW` (HARNESS /
  EVIDENCE-INSTRUMENTATION PRECISION LIMITATION; OBSERVED ARCHIVE FACT;
  NONBLOCKING for the source findings, NOT a product defect)

The original findings remain OPEN and are NOT closed by this implementation:

- `AUCDEV023-CR-PCH6B-BA-PREP-001`
  `ATTEMPT_GLOBAL_ONE_SHOT_BYPASS_VIA_CALLER_SELECTED_OUTPUT_ROOT`
- `AUCDEV023-CR-PCH6B-BA-PREP-002`
  `REPORT_ACCEPTANCE_SOURCE_NOT_BOUND_TO_FROZEN_OUTPUT_CUSTODY`

THIS AUTHORITY IS FOLLOW-UP REMEDIATION IMPLEMENTATION ONLY. This session is
NOT an event-package preparer, NOT an event-instantiation authority, NOT an
attempt-execution authority, NOT Auditor-A/B, NOT an independent auditor, NOT
an Audit Council /audit-council executor, NOT a provider/model/frontier
executor, NOT a qualification authority, NOT an installation authority. This
remediation does NOT close any finding (findings close only through the
Control Room), does NOT release the FAIL-CLOSED HELD event-package
preparation authority, and grants no authority of any kind.

Zero-provider / zero-network discipline held for the whole session: ZERO
provider/model/frontier calls, ZERO client inference calls, ZERO auditor
execution, ZERO /audit-council execution, ZERO wrapper/driver invocation in
the AUCDEV-023 governance chain, ZERO package-manager/PyPI/npm fetch
(PIP_NO_INDEX=1 UV_OFFLINE=1 for every test command; pre-existing local
pytest bytes via uv's offline cache + /usr/bin/python3 Python 3.14.7, the
interpreter of record), ZERO credential-content access, ZERO sealed-substance
access. All fixtures SYNTHETIC / NON-AUTHORITATIVE / ZERO-PROVIDER /
NON-PERSISTENT with synthetic non-secret credential bytes only. The only
network operations are the ordinary Git/GitHub publication mechanics: fetch,
ls-remote, the one authorized push and the post-push GitHub readback.

## 1. Exact live bootstrap and identity

Live GitHub master == local HEAD == origin/master ==
`6258bc0b7268881bcada868bb532d14076f74245` EXACT at bootstrap (ls-remote
authoritative; fetch clean rc 0; re-resolved EXACT again immediately before
staging and immediately before commit). Authorized base root tree
`31f56b6cd739107123f9d64c24a6ae45555eca17`; sole parent
`cfff321bd206b246f61cdc6ad6294bbe30489134` (the BA-PREP-001/002 remediation
candidate publication; single-parent fast-forward geometry; second parent
absent); trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor
rc 0; bootstrap-authority tree `60126f327e1096a07c1ad071dbe4b4f974763354`;
protected trees bootstrap-supervisor
`3056e577259ab0b0b0472f82ebc306506f3e084c`, qualification-harness
`5b8d5e5465923740470ff63ed9b8683f257a3787`, skill
`efd8c2e48edbb25795b3aacb1ce3c23fde10082a` all EXACT; the frozen audit
target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` remains AUDIT SUBJECT /
NOT AUTHORITY / UNTOUCHED. All seven tasking-listed in-scope blob identities
verified EXACT at the base before any edit (accounting.py
`03de6f663db283cf99f6a98e26e752a24457c52a`, binding.py
`d209bc70f2799bad489ef12ce9ff9c341d3753b5`, reportcustody.py
`18f1cc600c684e520b72026e0b4cdf8ba6287cb9`, runtime.py
`2e2fbf8cde75a09a92606857b4f75db2f51d36e3`, conftest.py
`400231839cb105cc5b32ca0222e1bb26b1a7e0e5`, test_binding.py
`55be2093b9659c73567e9fdb472c04a1d74dde00`, test_runtime.py
`a7826b711babe05ab609bf6b76fe2cca88e145f6`). Zero staged content before
this remediation; the pre-existing untracked drift and the pre-existing
smoke-fixture / smoke-fixture-103 gitlink drift preserved UNSTAGED. This
report's path was ABSENT at the base with zero full-history path rows.

## 2. Demonstrated residual defects (re-derived at the exact base before any edit)

All four residual defects were FIRST demonstrated live by synthetic probes
against the UNMODIFIED base (untracked evidence workspace
`aucdev023-pch6b-ba-prep-rb2-remediation-evidence`,
`01-red-rb2-defect-probes.out`, 12/12 checks passed, exit 0):

- RB2-001 Case A (probe 1): with the frozen pathname preserved, the bound
  custody directory renamed away and a NEW otherwise-valid 0700 same-UID
  directory created at the EXACT frozen pathname, a SECOND authority process
  for the SAME reserved attempt ran a COMPLETE second lifecycle — the
  pathname identity gate passed, the replacement directory's fresh O_EXCL
  namespace accepted the attempt-global claim, and TWO attempt-global
  records plus TWO frozen first-pass artifacts existed for ONE reserved
  attempt identity.
- RB2-001 Case B (probe 2): rebinding the pathname between the custody open
  and the accounting create (deterministic monkeypatch of the store create)
  SPLIT custody — the accounting record landed in the REPLACEMENT directory
  object while the frozen report went through the held fd into the ORIGINAL
  (renamed-away) object.
- RB2-002 A (probe 3): a binding whose `auditor_invocation` designated
  `--report /elsewhere/report.json` while `output_identity.report_source`
  named a different path PARSED SUCCESSFULLY — no invocation-to-report-source
  edge existed anywhere (the `_invocation_field` validator checked argv
  structure only).
- RB2-002 B (probe 4): a structurally AND semantically VALID report
  pre-written at the EXACT frozen report pathname was ACCEPTED and FROZEN
  (REPORT_FROZEN with the pre-existing bytes' digest) under a "none"
  launcher that produced no report, and the pre-existing file was then
  DISCARDED as staging.

## 3. Follow-up remediation design (narrowest mechanically sound fix)

The first-pass pathname identity gates are RETAINED unchanged as
defense-in-depth (OUTPUT_CUSTODY_ROOT_MISMATCH / REPORT_SOURCE_MISMATCH
pre-consumption refusals unchanged). The follow-up adds OBJECT-level custody:

- **binding.py**: `output_identity` now carries exactly `kind`, `name`,
  `custody_root`, `report_source`, `custody_dev`, `custody_ino`
  (`OUTPUT_IDENTITY_FIELDS`). The custody directory's host-local filesystem
  OBJECT identity (`st_dev`/`st_ino`; `_frozen_object_id` — plain int, bool
  refused, dev >= 0, ino >= 1) is binding-frozen, digest-covered
  (automatically, via `Binding.digest` over the canonical whole document —
  machine-checked by the extended BA-22 matrix) and transport-projected
  (automatically, via `binding_projection` over every TOP_LEVEL dimension).
  The report source must now be a DIRECT child of the frozen custody root
  (ONE custody domain; `REPORT_SOURCE_NOT_A_DIRECT_CHILD_OF_CUSTODY_ROOT`)
  and must not collide with the frozen output name
  (`REPORT_SINK_NAME_COLLIDES_WITH_FROZEN_OUTPUT`). The frozen invocation's
  designated report destination is mechanically bound to the frozen report
  source: exactly ONE canonical `--report` option
  (`INVOCATION_REPORT_OPTION`), exactly one value, EXACT equality, else
  `AUDITOR_INVOCATION_REPORT_OPTION_ABSENT` / `_DUPLICATE` /
  `AUDITOR_INVOCATION_REPORT_VALUE_ABSENT` /
  `AUDITOR_INVOCATION_REPORT_SINK_MISMATCH` (fail-closed at parse — two
  independently frozen values are no longer sufficient).
- **runtime.py**: `run_attempt` opens the frozen custody pathname EXACTLY
  ONCE and verifies with `fstat()` that the HELD fd IS the binding-frozen
  directory OBJECT before any claim, gate or credential read
  (`OUTPUT_CUSTODY_OBJECT_MISMATCH` — a pre-advance refusal: the authority
  object stays PREPARED, nothing acquired, so a replacement directory at the
  exact frozen pathname can never provide a fresh O_EXCL namespace for the
  same reserved attempt). The attempt-global O_EXCL claim (BA-RB-001
  semantics unchanged: reserved attempt id ALONE, digest-independent,
  observable `RECORD_CREATE_REFUSED` retained for a second same-attempt
  process) is created RELATIVE TO THE SAME HELD verified directory OBJECT
  via `AccountingStore.create_at` — never a pathname re-open, so a mid-run
  pathname rebind cannot split accounting custody from output custody. After
  the three dynamic gates and durable GATES_PASSED but BEFORE any credential
  read, the authority CREATES the attempt-owned report sink with
  `O_CREAT|O_EXCL|O_NOFOLLOW` (0600, O_RDWR) under the SAME held custody
  object (`create_report_sink`; a pre-existing object at the frozen sink
  name refuses — `REPORT_SINK_PREEXISTING` — so a pre-existing exact-path
  report can NEVER become the accepted first pass), and holds its fd for the
  whole attempt. The frozen invocation already names this exact sink
  (parser-enforced edge). Acceptance snapshots ONLY the held sink object
  (`snapshot_held_sink`; empty = honest `REPORT_MISSING`; a replacement
  object at the pathname is never accepted), the screen/validator/semantic
  chain is unchanged on exactly those bytes, the 0444 O_EXCL freeze goes
  through the SAME held custody dir fd as before, and cleanup
  (`discard_held_sink`) unlinks ONLY the exact held sink object — it
  resolves the name relative to the held custody fd and compares the
  `st_dev`/`st_ino` pair against the held sink fd before unlinking, so a
  replacement object at the sink pathname is never deleted. On every
  terminal report outcome (MISSING / SCREEN_FAIL / INVALID / FROZEN) the
  authority-owned sink is safe-discarded; a pre-consumption failure after
  sink creation safe-discards it on the way out. The frozen
  `custody_dev`/`custody_ino` are additionally durable non-secret binding
  facts at CONSUMED_PRE_EXEC (`output_custody_dev` / `output_custody_ino`).
- **accounting.py** (bounded RB2 derivative): UNCHANGED semantics plus ONE
  narrow primitive, `AccountingStore.create_at(dir_fd, attempt_id,
  binding_digest, first_state)` — the O_EXCL claim relative to an
  ALREADY-HELD verified custody directory fd, with EXPLICIT ownership: the
  store dups and owns its own fd (closed by `close()`); the caller keeps its
  fd untouched. `create(root, ...)` is now a thin wrapper
  (open_custody_dir + create_at + close). Nothing else changed.
- **reportcustody.py** (bounded RB2 derivative): UNCHANGED freeze semantics
  plus the three narrow held-fd sink primitives `create_report_sink`,
  `snapshot_held_sink`, `discard_held_sink` (full semantics above); the
  superseded pathname-based `snapshot_staging` / `discard_staging` staging
  primitives are REMOVED as dead surface (no production or test caller
  remained; the held-fd sink discipline replaces them — the no-follow /
  regular-file / size-bound / one-snapshot / credential-screen / structural
  / semantic / 0444-O_EXCL invariants are all retained in the new path).
- **Source provenance consequence (explicit)**: `statemachine.py` and
  `custody.py` remain EXACT pre-target blob reuses
  (`cf563d2178907e7666ce661b81ab1bf16fb71201` /
  `37e6b5bb4365c7b29ba3632fe95362d5a7e16c09`); `accounting.py` and
  `reportcustody.py` are now recorded as bounded RB2 DERIVATIVES of their
  exact pre-target blobs (`kind = EXACT_PRETARGET_BLOB_DERIVATIVE_RB2`,
  `derivation = AUCDEV-023-PCH6B-BA-PREP-RB2-001-002-BOUNDED-
  HELD-FD-OBJECT-CUSTODY`, original blobs pinned in
  `source_git_blob`) in `runtime.EXPECTED_PROVENANCE`, `MANIFEST.json`
  `source_provenance`, and the updated test_static pins (test_ba03 now also
  proves the derivative files DIFFER from their pinned pre-target blobs —
  an honest derivation, never a silent reuse claim).

Why the invariants now hold mechanically (RB2-001): ONE reserved attempt
identity -> ONE binding-frozen custody OBJECT (st_dev/st_ino) -> ONE held
custody directory authority (opened once, fstat-verified) -> ONE
attempt-global O_EXCL accounting namespace (created relative to the held
object) -> the SAME held directory object for the frozen report. A pathname
that no longer resolves to the frozen object is refused before anything is
acquired, and pathname rebinding during the run cannot redirect any
authority action. (RB2-002): frozen invocation -> exact authority-created /
attempt-owned report sink (O_EXCL; pre-existing refused) -> immutable
snapshot of THAT SAME held sink object -> credential screen -> structural
validation -> semantic binding -> frozen first pass; no stdout/stderr
substitution; empty sink stays honest REPORT_MISSING; replacement objects
are neither accepted nor unlinked.

## 4. Exact change surface (thirteen paths, no fourteenth tracked path)

MODIFY (10 package paths):

- `bootstrap_authority/binding.py` — OUTPUT_IDENTITY_FIELDS + object-id
  validator + direct-child sink + invocation->sink edge (BA-22 matrix rows)
- `bootstrap_authority/runtime.py` — object gate, held-fd claim, sink
  create/snapshot/discard integration, durable dev/ino facts, provenance
  constants for the two derivatives
- `bootstrap_authority/accounting.py` — `create_at` held-fd primitive
  (bounded derivative)
- `bootstrap_authority/reportcustody.py` — held-fd sink primitives,
  superseded staging primitives removed (bounded derivative)
- `tests/conftest.py` — report source is now the attempt-derived sink under
  the frozen custody root; custody dev/ino frozen from the built world;
  invocation `--report` bound to the frozen sink; new `replace` launcher
  mode (unlink sink + write replacement object at the same pathname)
- `tests/test_binding.py` — RB2 parse-plane refusals + BA-22 extensions +
  adapted exact-parse test
- `tests/test_runtime.py` — four RB2 runtime regressions + the adapted
  symlink-alias regression (the pre-fix fixture pre-write of the frozen
  staging file removed — a pre-existing object at the frozen sink name is
  now refused by its own regression)
- `tests/test_static.py` — provenance pins: 2 exact reuses + 2 bounded
  derivatives (`DERIVED_REUSE_BLOBS`, `test_ba03`/`test_ba05`)
- `README.md` — object gate, sink lifecycle, provenance change documented
- `MANIFEST.json` — regenerated LAST from the final package bytes (raw
  SHA-256 `7713b89e2618d27963be0df4dd5ebb33961a5b48c063c62ecacff2238da1425f`;
  non-circular package_sha256
  `4399cb062e3fe9a5c4e6e71ad90e8515b3f0b462b6a648c458068cd6f01263db`;
  12 rows; schema/package/policy_id/target/design ids/status/
  qualification_claim/runtime_dependencies preserved EXACT;
  source_provenance = 2 EXACT_PRETARGET_BLOB_REUSE + 2
  EXACT_PRETARGET_BLOB_DERIVATIVE_RB2 + 3 NEW_AUTHORITY_SPECIFIC)

ADD (1): THIS record.

MODIFY (2 governance, per AUCDEV-PROJECT-UPDATE-PROTOCOL.md "Remediation
completed"): `docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (rotation
confined EXACTLY to lines 3/11/23-25 plus one dated tail record) and
`docs/chatgpt-project/AUCDEV-BACKLOG.md` (exactly two pure insert zones),
both zone-verified by script at build time AND re-asserted from the staged
blobs.

test_static.py LOC_BOUND stays UNCHANGED at 3000: production LOC is EXACTLY
3000 after the compression pass (see §7 T-4); NO ceiling change, NO test
weakened, NO safety logic deleted.

## 5. Held invariants — verified unchanged

- BA-RB-001 closure retained in its established scope: the attempt-global
  O_EXCL claim is still keyed by the reserved attempt id ALONE
  (`accounting_name` unchanged), still digest-independent, with the binding
  digest still durable and inspection-bound in every record
  (`RECORD_BINDING_MISMATCH` retained); the same-root duplicate-attempt
  regression still refuses `RECORD_CREATE_REFUSED` (the claim precedes sink
  creation precisely to keep this observable token unchanged).
- BA-RB-002 closure retained: gates still strictly before credential
  materialization (the sink creation was inserted AFTER durable
  GATES_PASSED and BEFORE `CredentialCustody.ingest`, so no new pre-gate
  action exists beyond the custody open/claim the first pass already had);
  CLIENT_SELECTION_PREFLIGHT -> NETWORK_READINESS -> RESOURCE_GATE LAST ->
  durable GATES_PASSED -> custody -> durable CONSUMED_PRE_EXEC ->
  irreversible spend -> immediate launch unchanged; the failing-preflight
  regression still observes the credential unread, no sink, no record
  contamination.
- BA-RB-003 retained; all report protections retained in the new held-fd
  path: O_NOFOLLOW, regular-file requirement, size bound, exactly one
  immutable snapshot, credential screen, frozen structural validator
  identity, structural validation, semantic exact target/event/role/attempt
  binding, final 0444/O_EXCL freeze, honest REPORT_MISSING, no stdout/stderr
  substitution ever.
- One public `run_attempt` lifecycle; run_attempt signature UNCHANGED
  (machine-checked by BA-31); no grant/consume/resume/retry/adopt_report/
  finish/mint_attempt/create_event surface introduced.
- statemachine.py and custody.py byte-identical to their pinned pre-target
  blobs; protected trees byte-identical at the staged write-tree
  (bootstrap-supervisor `3056e577259ab0b0b0472f82ebc306506f3e084c`,
  qualification-harness `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill
  `efd8c2e48edbb25795b3aacb1ce3c23fde10082a`); the frozen audit target
  `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` remains AUDIT SUBJECT / NOT
  AUTHORITY / UNTOUCHED.
- The first-pass pathname identity gates are RETAINED (not weakened):
  alternate-root, symlink-alias-root, substituted-source and
  symlink-alias-source refusals all still pass unchanged.

## 6. Adversarial regression coverage (deterministic, zero-provider)

- `test_rb2_001_replacement_directory_same_pathname_refused` (Case A GREEN):
  rename + replacement 0700 directory at the EXACT frozen pathname ->
  `OUTPUT_CUSTODY_OBJECT_MISMATCH` BEFORE any credential read (every
  synthetic byte still readable from the source pipe), ZERO dynamic gates,
  ZERO accounting records in EITHER object, replacement acquired NO
  namespace, the SAME authority object stays PREPARED and then SUCCEEDS
  once the pathname names the frozen object again, and a second same-attempt
  process still refuses `RECORD_CREATE_REFUSED` (BA-RB-001 retained).
- `test_rb2_001_single_run_rebind_accounting_uses_held_object` (Case B
  GREEN): a deterministic mid-run pathname rebind (monkeypatched
  `AccountingStore.create_at` wrapper — no production test hook) proves the
  O_EXCL claim is created relative to the HELD object (record inside the
  renamed-away directory, NOTHING in the replacement), the frozen output
  would freeze through the same held object, the launcher's path-written
  report in the replacement is NEVER accepted (honest REPORT_MISSING), and
  the authority-owned sink in the held object is safely discarded.
- `test_rb2_002_preexisting_exact_frozen_report_refused`: a VALID report
  pre-existing at the EXACT frozen sink pathname -> refused pre-consumption
  (`REPORT_SINK_PREEXISTING`) with the credential unread, no freeze, the
  pre-existing object intact (not ours — never unlinked), durable record
  TERMINAL_PREEXEC_STOP without CONSUMED_PRE_EXEC / EXEC_ATTEMPTED.
- `test_rb2_002_sink_replacement_during_execution_not_accepted`: the
  synthetic auditor UNLINKS the authority-created sink and writes a fresh
  VALID replacement at the exact same pathname -> acceptance reads only the
  held original sink (empty) -> honest REPORT_MISSING, no frozen artifact,
  and the replacement object SURVIVES untouched (cleanup never unlinked it).
- Binding-plane refusals: missing `custody_dev`/`custody_ino`; invalid
  dev/ino (bool / negative / zero-ino / float / string); report source
  outside the root, at the root itself, nested, prefix-trap; sink name
  colliding with the frozen output name; invocation sink mismatch, report
  option absent / duplicate / value absent; BA-22 matrix extended to
  `custody_dev` and `custody_ino` (swapping either changes the digest).
- Honest normal cases retained: valid sink -> REPORT_FROZEN (full success,
  role B via memfd included); no produced report -> REPORT_MISSING;
  credential-contaminated report -> REPORT_SCREEN_FAIL; structural /
  semantic failures -> REPORT_INVALID with fixed tokens; symlink alias of
  the report source refused pre-consumption while the exact frozen sink
  still freezes through a normal run; oversize / non-regular sink paths
  fail closed.

## 7. Validation evidence (every command, honest outcomes)

- RED-1 probes on the UNMODIFIED base (`01-red-rb2-defect-probes.py`):
  12/12 checks passed, exit 0 — all four residual defects DEMONSTRATED
  (outputs `01-red-rb2-defect-probes.out`). Probes are untracked
  instruments, never staged.
- RED-2 committed regressions BEFORE production code: `test_binding.py -k
  "rb2 or ba_prep"` 27 failed / 4 passed, exit 1; `test_runtime.py` 8
  failed, exit 1 — failing at the missing schema dimensions
  (`OUTPUT_IDENTITY_KEYS_INVALID: unknown=['custody_dev','custody_ino']`)
  and missing mechanics (outputs 02/03).
- After implementation: full package suite
  `PIP_NO_INDEX=1 UV_OFFLINE=1 uv run --offline --no-project --python
  /usr/bin/python3 --with pytest python -m pytest -q bootstrap-authority/tests`
  -> **147 passed, 0 failed, 0 errors, 0 skips, exit 0** on the FINAL bytes
  after the FINAL MANIFEST regeneration (binding 81 / runtime 33 / static
  33; +24 tests vs the prior 123), re-run green from scratch after every
  final byte change (output 13).
- `git diff --check` PASS (and staged `git diff --cached --check` PASS —
  battery).
- Final staged full-suite staged-tree binding: PRE_TEST_STAGED_TREE ==
  POST_TEST_STAGED_TREE around the final complete suite run on the final
  staged bytes (recorded in the evidence workspace and the generated-LAST
  handoff; the Control Room does not rerun pytest by policy).
- Protected trees / frozen target verified EXACT from the staged write-tree
  (battery); production LOC exactly 3000 (per-file: __init__ 35, binding
  605, statemachine 102, accounting 239, custody 211, reportcustody 146,
  runtime 1662 — total EXACTLY 3000 within the unchanged ceiling).
- Full precommit gate battery on the FINAL staged bytes: ALL PASS (path
  set/protected trees/lineage blobs/no-jsonl/staged==working/queue
  recount/sealed-identity/credential scan/hex allow-set/wording gates —
  see the battery output member).

## 8. Honest session iteration accounting (instrument-side; no defect rewritten as PASS)

- T-1: the bootstrap identity instrument hit zsh `:q`/`:s` parameter
  modifier substitution on `$R:path` twice (unquoted, then inside double
  quotes); fixed with braced `${R}:path`. No repository state change.
- T-2: the first `test_rb2_002_invocation_report_value_absent` mutation
  deleted the `--report` OPTION together with its value, so the ABSENT
  token could not fire; corrected to delete only the value. Test-instrument
  defect, no production change.
- T-3: after each package byte change the package self-identity correctly
  refused constructions until MANIFEST.json was regenerated (the fail-closed
  mechanism working as designed — first observed as 32 runtime-test
  failures with the un-regenerated interim manifest); the deterministic
  regenerator was built, an interim regeneration enabled the GREEN phase,
  and the FINAL regeneration followed the final byte change.
- T-4: LOC compression 3254 -> 3000 EXACTLY over many measured passes —
  comment/docstring budget compression (module and method docstrings
  reduced to their essential invariants), top-level 2-blank separators
  collapsed to 1 (73 lines) and decorative interior blanks removed (20
  lines, string-safe via tokenize), 16 whole-line/trailing comments
  removed, the superseded dead pathname snapshot/discard staging primitives
  removed, and several strictly-counted line-surgery rewrites; instrument
  defects on the way: two early docstring edits introduced 7 stray blank
  lines (collapsed, plus 2 pre-existing), one blank-collapse script crashed
  on a boolean-precedence defect BEFORE any write (verified nothing was
  written), one line-surgery script aborted twice on its own
  shorter-than-span assertion BEFORE any write (verified nothing was
  written), and several prose edits turned out line-count-neutral
  (rewrap-only) and were redone with strict counting. NO safety logic
  deleted, NO ceiling change, NO test weakened; the full suite re-ran green
  from scratch after the final byte change and final MANIFEST regeneration.
- T-5: one `echo ====` line was parsed by zsh as a command (cosmetic
  instrument defect in a display pipe); rerun with quoting.

RB2-EV-001 (GENERATED_LAST_SHA256SUMS_CONTAINED_STALE_SELF_ROW): the
generated-LAST archive of THIS remediation mechanically demonstrates the
corrected behavior — SHA256SUMS contains EXACTLY the N payload members,
never itself, verification is N/N PASS with payload-set equality TRUE, and
the outer archive SHA-256 is computed separately after the archive is final
(see §10).

## 9. Governance disposition

- `AUCDEV023-CR-PCH6B-BA-PREP-001`: FOLLOWUP_REMEDIATION_IMPLEMENTED /
  AWAITING_FRESH_CONTROL_ROOM_READBACK (NOT closed)
- `AUCDEV023-CR-PCH6B-BA-PREP-002`: FOLLOWUP_REMEDIATION_IMPLEMENTED /
  AWAITING_FRESH_CONTROL_ROOM_READBACK (NOT closed)
- `AUCDEV023-CR-PCH6B-BA-PREP-RB2-001`: REMEDIATION_IMPLEMENTED /
  AWAITING_FRESH_CONTROL_ROOM_READBACK (NOT closed)
- `AUCDEV023-CR-PCH6B-BA-PREP-RB2-002`: REMEDIATION_IMPLEMENTED /
  AWAITING_FRESH_CONTROL_ROOM_READBACK (NOT closed)
- `AUCDEV023-CR-PCH6B-BA-PREP-RB2-EV-001`: packaging instrumentation
  corrected — the generated-LAST archive of THIS remediation mechanically
  demonstrates the corrected SHA256SUMS behavior (exactly N payload rows,
  no self-row, N/N PASS, payload-set equality TRUE); retained as a
  NONBLOCKING evidence-instrumentation residual, NOT converted into a
  product defect.
- Prior closures RETAINED and NOT reopened: BA-RB-001, BA-RB-002, BA-RB-003
  (their exact scopes unchanged); historical informational findings
  (BA-RB-004, BA-RB-PUB-001, BA-RB-PUB-002, BA-REM-RB-001, BA-REM-RB-002,
  BA-PREP-HOLD-RB-001, BA-PREP-HOLD-RB-002) retained WITHOUT rewriting or
  repacking; historical handoffs NOT repacked; the previous implementation
  report NOT rewritten (THIS record is a NEW dated follow-up record).
- HELD governance preserved: the operator's event-package preparation
  authority remains RECEIVED / NOT EXECUTED / NOT CONSUMED / FAIL-CLOSED
  HELD and is NOT released by this remediation; event NOT instantiated;
  attempt authorities NOT granted; new-lineage model engagements USED 0
  with PROPOSED 2 unchanged; historical PCH6 authority CONSUMED /
  TERMINAL / CLOSED / NO_RERUN with all historical identities
  NON-TRANSFERABLE and the AUCDEV-010 bootstrap-root exception
  NON-TRANSFERABLE; PCH6-B-SD-002 and PCH6-CR-BSD-001 remain NOT CLOSED
  awaiting fresh independent audit of the frozen target; PCH6-B-SD-001
  RETAINED / OPEN; ROOT_CAUSE_NOT_ESTABLISHED unchanged with NO causal
  conversion; independent-auditor provenance gate NOT_SATISFIED with
  installed Audit Council source `8ae33444f349ce73c1359b963722e2d16acba630`
  predecessor provenance NOT ESTABLISHED, NOT relabeled; AUCDEV-023 P1 /
  READY / NOT DONE; AUCDEV-024 P1 / READY / NOT DONE; qualification NONE;
  installation NONE; no /audit-council execution authorized. Disposition
  token form:
  `AUCDEV_023_PCH6B_BA_PREP_001_002_FOLLOWUP_REMEDIATION = FOLLOWUP_REMEDIATION_IMPLEMENTED /
  BA_PREP_001_AWAITING_FRESH_CONTROL_ROOM_READBACK /
  BA_PREP_002_AWAITING_FRESH_CONTROL_ROOM_READBACK /
  RB2_001_REMEDIATION_IMPLEMENTED_AWAITING_FRESH_CONTROL_ROOM_READBACK /
  RB2_002_REMEDIATION_IMPLEMENTED_AWAITING_FRESH_CONTROL_ROOM_READBACK /
  CUSTODY_OBJECT_IDENTITY_BINDING_FROZEN_ST_DEV_ST_INO /
  HELD_DIR_FD_O_EXCL_CLAIM_NO_PATHNAME_REOPEN /
  AUTHORITY_CREATED_ATTEMPT_OWNED_O_EXCL_REPORT_SINK /
  INVOCATION_REPORT_SINK_EDGE_PARSER_ENFORCED /
  ACCEPTANCE_SNAPSHOTS_ONLY_THE_HELD_SINK_OBJECT /
  CLEANUP_NEVER_UNLINKS_A_REPLACEMENT /
  EVENT_PACKAGE_PREPARATION_REMAINS_FAIL_CLOSED_HELD /
  EVENT_NOT_INSTANTIATED / ATTEMPT_AUTHORITIES_NOT_GRANTED /
  MODEL_ENGAGEMENTS_USED_0 / BA_RB_001_002_003_PRIOR_CLOSURES_RETAINED /
  TWO_PRETARGET_PRIMITIVES_BYTE_IDENTICAL_TWO_BOUNDED_DERIVATIVES_PINNED /
  PCH6_B_SD_002_NOT_CLOSED / PCH6_CR_BSD_001_NOT_CLOSED /
  PCH6_B_SD_001_RETAINED_OPEN / ROOT_CAUSE_NOT_ESTABLISHED_UNCHANGED /
  INDEPENDENT_AUDITOR_PROVENANCE_GATE_NOT_SATISFIED /
  NO_AUDIT_EXECUTION / NO_AUDIT_PASS / QUALIFICATION_NONE /
  INSTALLATION_NONE`.

## 10. Self-commit identity rule and next action

This record and its commit message record the exact authorized base, the
staged write-tree and the disposition; the commit cannot contain its own
final SHA. The exact resulting publication SHA and result root tree are
reported in the FINAL-RETURN, the post-push GitHub readback and the
generated-LAST handoff, and will be canonically pinned by the later Control
Room readback.

NEXT ACTION EXACTLY ONE: INDEPENDENT CONTROL ROOM READBACK OF THE EXACT
FOLLOW-UP REMEDIATION PUBLICATION AND ITS GENERATED-LAST HANDOFF.
Recording this next action grants NO authority of any kind.

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from
an agent session; never rerun the launcher; never treat any recorded grant
phrase (including any phrase recorded here) as a new grant; never execute a
real auditor or provider/model; never open the four historical sealed
artifacts (identity-only forever); never relabel or rewrite historical model
identities, runs, records, matrices, prompts or evidence workspaces
(append-only); never claim audit PASS, qualification, installation or any
authority from this remediation — it grants none.
