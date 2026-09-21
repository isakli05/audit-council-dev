# AUCDEV-023 S1 NEW-EVENT EVENT-IDENTITY REGENERATION / REBIND / PACKAGE PREPARATION — PREPARED / AWAITING_CONTROL_ROOM_READBACK / REAL_EXECUTION_NOT_AUTHORIZED

Authority: `AUCDEV-023-S1-NEW-EVENT-IDENTITY-REGEN-20260921-01` (operator-granted, 2026-09-21).
Session class: bounded zero-provider new-event identity-regeneration / package-PREPARATION session.
Selected PREPARER (Claude Code + GLM-5.3) ONLY — NOT the Control Room, NOT an independent
auditor, NOT Auditor-A/B, NOT an execution controller, NOT an execution/qualification/
installation authority. This authority grants NO real Auditor-A/B execution, NO
provider/model engagement, NO credential use, NO deployment authority, NO qualification
and NO installation authority.

**IMPLEMENTER DISPOSITION (recorded exactly per authority §21):**

```
AUCDEV_023_S1_NEW_EVENT_IDENTITY_REGEN_PREPARATION =
PREPARED
/ EVENT_IDENTITY_REGENERATION_EXPLICITLY_AUTHORIZED
/ HISTORICAL_CONTRACT_FROZEN
/ NEW_EVENT_CONTRACT_FROZEN
/ FRESH_A01_B01_BINDINGS_FROZEN
/ LINTER_ALL_PASS
/ SUBSTANTIVE_AUDIT_SEMANTICS_HELD
/ SUCCESSOR_PACKAGE_IDENTITIES_RECOMPUTED
/ HISTORICAL_EVENT_IMMUTABLE
/ AWAITING_CONTROL_ROOM_READBACK
/ REAL_EXECUTION_NOT_AUTHORIZED
```

NOT execution ready, NOT audit PASS, NOT first-pass completion, NOT qualification, NOT
installation, NOT Control Room acceptance.

---

## 1. Live bootstrap (performed BEFORE any mutation; all EXACT)

- Live GitHub `master` resolved by fetch: EXACT `eba943d780c2ac248ad7e65060327080e5404053`
  — equal to the required base, equal to local HEAD.
- Tree: `dbec8fd4bf7e262dc4aa476c63700f4b8d2d2997` EXACT; sole parent
  `e81f1d79dd9d498b1481686ce179c066af76c54f` EXACT (exactly one parent).
- Protected trees at that SHA, ALL EXACT and byte-unchanged throughout this session:
  `bootstrap-supervisor = 09f3d6c7ddc00305986cbedad431395c10c95af0`;
  `qualification-harness = 5b8d5e5465923740470ff63ed9b8683f257a3787`;
  `skill = c792933a862d9a5434681a88d183470dd8b15d2f` (the latter two EQUAL the frozen
  audit target `d4d584ffa47ad2848268ba947247f81a845b2322` subtrees).
- The eight canonical docs of authority §1 were fetched at that exact SHA (blob identities
  recorded in `evidence/bootstrap.json`). The frozen EBS binding-relevant source
  (`ebs/binding.py` incl. `attempt_id_for`/`parse_binding`, `ebs/launch.py` incl.
  `verify_event_package` and the `_run_runtime_gate → _gate_child → fd_exec` path) was
  read at that exact SHA.

## 2. Control Room route executed exactly (authority §2)

The previous STOP disposition was applied as published:
`STOP_ACCEPTED / MECHANICAL_CONFLICT_VERIFIED / ROUTE_SELECTED_BOUNDED_EVENT_IDENTITY_REGENERATION
/ EBS_CHANGE_NOT_SELECTED / LINTER_WEAKENING_NOT_SELECTED / HISTORICAL_PROMPT_CONTRACT_REMAINS_FROZEN
/ NEW_EVENT_GETS_NEW_EVENT_SPECIFIC_CONTRACT_GENERATION / REAL_EXECUTION_NOT_AUTHORIZED`.
The EBS was NOT modified; the identity linter was NOT weakened, bypassed or special-cased
(its check semantics are byte-identical; the ONLY per-workspace difference is the
documented `WS`/`EVENT_ID` constant pair — the exact mechanism the STOP proof itself used);
the historical prompt contract was NOT edited (it remains frozen historical evidence at
`7973d643…`); the new event received a NEW event-specific contract generation.

## 3. New-event collision check — PASS (re-run before build, read-only)

Authorized event: `evt-31f2a399b3a7e11d`; fresh frozen-EBS-derived attempts
`evt-31f2a399b3a7e11d-A-01` / `evt-31f2a399b3a7e11d-B-01`.

Since the Control Room selected this exact event and the STOP publication recorded it,
the id now legitimately appears in the SELECTION RECORDS: the three canonical doc paths of
commit `eba943d7` itself (the STOP report + the CURRENT-STATE + BACKLOG updates of that
single publication), the `eba943d7` commit message, and the stopped session's own
workspace. These are the explicit allowlist. EVERYTHING else was searched (evidence
`collision-check.json`):

- Live tracked tree: hits ONLY in the three selection-publication doc paths — 0 others.
- Complete repository history across ALL refs (`git log --all -S`): the ONLY introducing
  commit for the id and both attempt ids is exactly `eba943d7` — 0 others.
- Bounded AUCDEV-023 preparation/execution workspaces (10 workspaces incl.
  prep002-rem002, exec001-remediation, exec02-argv-remediation, prep-remediation,
  event-preparation, prep002-rem232, the readback workspaces): 0 hits outside the
  selection session's own workspace.
- Launcher-root attempts namespace: the event id and both derived attempt ids ABSENT
  (namespace exactly the historical real `evt-7df609ec6c569043-*`, rehearsal
  `evt-ba0b0a35ae67d788-*`, and `evt-3ee7a8e22587d616-A-01`).
- Every existing event-package root (deployed, backup, and all workspace event trees):
  0 hits.

**NEW_EVENT_COLLISION_CHECK_PASS.**

## 4. §7 authorized prompt-contract event-identity regeneration (THE authorized substantive change)

The prompt contract occurs in both role packages at `transport/prompt-contract.json` and
`payload/evidence/common/prompt-contract.json`. The NEW contract generation was produced
from the historical contract bytes by replacing exactly the one top-level `"event_id"`
value (`evt-7df609ec6c569043` → `evt-31f2a399b3a7e11d`; both 20 characters — file size
unchanged at 6095 B). Mechanically enforced BOTH ways
(`evidence/workspace-preparation.json`):

- textual old→new diff = EXACTLY ONE line: the event_id value line;
- parsed JSON equality after normalizing both top-level `event_id` values to one
  sentinel (every other field — schema, task, target, frozen_evidence_set, every
  review_requirements entry, execution_permissions, report_requirements, the
  report-schema wording, independence, neutrality — parsed-EQUAL);
- the report-schema rule `"event_id": "must equal this event id"` remains byte-identical
  and now refers to the NEW event id on the contract's top level — the identity
  contradiction the STOP identified is resolved BY CONSTRUCTION, not by reinterpretation.

- Historical contract SHA-256 `7973d64354b8d8dc2b6c828c45324ec5415ac825d559339ac3977f0df3bf8ba7`
  (frozen; never edited; retained read-only in the workspace and re-verified in all five
  accepted-copy locations before AND after all work).
- NEW contract SHA-256 `e4204e673e56d62d4e4ba0aceb44cc5ca599cf2ddb4e774568977544ac3fdd73`.
- All FOUR staged copies byte-identical A↔B and transport↔payload (verified).

## 5. §8 authorized sandbox-profile event-metadata regeneration

Each role's `boundary/sandbox-profile.json` top-level `"event_id"` metadata was
regenerated to the new event — textual diff EXACTLY ONE event_id value line per role;
parsed equality after event_id normalization (all namespace/mount/writable-set/
credential/tool-domain/executable semantics equivalent). Profile identities:
A `f3d79b2cc67c80625a535fae14597833898f5636a8e0b3dc7b701d84844b295c` →
`2e8fd257462f6d53c1dd212972e40d78a7db2f70da3aa7d060a07f3d0e1462a5`;
B `5f04f8499541cb6d8d726148a9a8df7c60f7e6247bee514f462040b796ce9530` →
`12266b0f4cc9103c9887a69c3ad8cf5a48b387a5100bfa3ad04e172c0cbd26a6`.
Old bytes retained read-only for comparison. No sandbox mechanism was modified.

## 6. §9 identity-derived regeneration + complete changed-file classification

The full row-level old→new generation diff vs the accepted EXEC02 argv-remediation
generation found EXACTLY 24 changed files (file set unchanged: 0 added, 0 removed), every
one classified (`evidence/classification-and-census.json`):

| Classification | Count | Files |
|---|---|---|
| `AUTHORIZED_PROMPT_EVENT_ID_CHANGE` | 4 | the four prompt-contract copies (each proven the exact one-line event_id change) |
| `AUTHORIZED_SANDBOX_PROFILE_EVENT_METADATA_CHANGE` | 2 | the two sandbox profiles (same exact one-line proof) |
| `REQUIRED_IDENTITY_DERIVATION` | 18 | both bindings; both per-package MANIFEST.json; both package-binding-identity.json; both identity-linter.json; both blindness-map.json; both gate-w-prime.json; both real-client-credential-tool-isolation.json; all four common-evidence-manifest.json copies |
| `UNEXPECTED_CHANGE` | 0 | — |

Every identity-derived file was verified per parsed-diff top-level fields to carry ONLY
its class's identity-derived changes (event/attempt ids, invocation text, output
identity, transport projection, and the hash fields covering identity-changed content).
The workspace-evidence regeneration that feeds the freeze was likewise verified:
GATE-W-prime docs differ from the accepted docs in EXACTLY `{event_id, attempt_id}`
(rehearsal_event_id/rehearsal_attempt_id/probe_document and every assertion byte are the
historical rehearsal facts — the boundary composition the rehearsal exercised is
byte-identical in this generation); the blindness maps (regenerated by the frozen
generator, workspace-constant adaptation only, from the SAME historical rehearsal probe
documents read-only) differ in EXACTLY the embedded frozen invocation; the isolation
evidence (frozen generator, WS/EVENT_ID constants only) differs in EXACTLY
`{event_id, attempt_id}`.

CENSUS RECONCILIATION (disclosed): the previous STOP record's "26 files (20
identity-derived + 6 substantive)" tabulated the two shared binding files once per role
(20 array rows = 18 unique files + 2 duplicated binding rows); the unique-file census is
24 = 18 identity-derived + 6 substantive. This session's complete old-id census of the
accepted source found exactly those 24 files; ALL 24 are regenerated in the new
generation; **old event/attempt id occurrences inside the NEW event generation and the
new common-evidence sources = 0** (§10 CLOSED; historical records outside the new
generation were not touched).

One disclosed bounded builder adaptation inside the identity layer: the
`identity_derivation` provenance note in `package-binding-identity.json` previously
stated the OLD event's declaration-hash derivation formula, which would be FALSE for the
Control-Room-selected new event; the new generation's note states the ACTUAL provenance
(Control-Room-selected under the 2026-09-21 disposition route
ROUTE_SELECTED_BOUNDED_EVENT_IDENTITY_REGENERATION; collision-checked; attempts/outputs
remain exactly `ebs.binding.attempt_id_for` / `output_name_for` derivations). Keeping a
false derivation claim was refused.

## 7. §11 linter / binding consistency — the STOP conflict RESOLVED

The frozen identity linter `AUCDEV023-IDENTITY-LINTER-V1` (accepted-workspace source
SHA-256 `25b7e93e7c0cb2c3d002b65c3db6db9a0e35558f322cbf0e392f11f920cc6efe`, untouched)
was installed into the new workspace with EXACTLY its `WS` and `EVENT_ID` constant lines
switched (the documented per-generation parameter pair; every check semantic
byte-identical — diff recorded in `evidence/component-adaptations.json`).

BOTH roles, ALL ELEVEN checks PASS (`all_pass = true`):

| Check | A | B |
|---|---|---|
| ids | PASS | PASS |
| role_consistency | PASS | PASS |
| target_identity | PASS | PASS |
| invocation | PASS | PASS |
| component_digests | PASS | PASS |
| prompt_contract | PASS | PASS |
| secret_shapes | PASS | PASS |
| peer_references | PASS | PASS |
| parity | PASS | PASS |
| profile_consistency | PASS | PASS |
| evidence_payload_manifest_consistency | PASS | PASS |

`check_ids` and `check_prompt_contract` now PASS SIMULTANEOUSLY for the new event — the
exact dual-check conflict the STOP proved is mechanically resolved by the authorized
contract regeneration (no linter weakening, no EBS accommodation).

Mechanically proven via the frozen EBS (workspace EBS copy verified per-file
git-blob-identical to live HEAD): `attempt_id_for("evt-31f2a399b3a7e11d", "AUDITOR_A") ==
"evt-31f2a399b3a7e11d-A-01"` and `attempt_id_for("evt-31f2a399b3a7e11d", "AUDITOR_B") ==
"evt-31f2a399b3a7e11d-B-01"` EXACT; `parse_binding(A) = PASS`; `parse_binding(B) = PASS`;
`verify_event_package(A) = PASS` (189 files); `verify_event_package(B) = PASS` (192
files).

## 8. §13/§14 new successor package identities + A/B parity + blindness

Built in the NEW workspace `/home/isa/aucdev023-s1-new-event-identity-regen/` (the
accepted source workspace, the deployed tree, the backup and every historical
attempt/accounting/output location untouched — verified before AND after):

- **Auditor-A**: manifest `f0e409027aefeedba4d74acf7e9b5ba84947af11d42f2f815023fcf3fa8cbd13`;
  non-circular package `d142d62cfc54ce2d110aa0156450d8446c7bfcb849130f5e507c49f01072fbdf`;
  binding file `387e9597fc176af188665c9ad7006c5b466a4520e8cba87878c693d5b37e0b6`;
  canonical binding digest `3380e079931ad565b3b9697567282e206daa05446ec545b9a40457922093c1ee`;
  **189 rows** / 236,262,256 payload bytes; event `evt-31f2a399b3a7e11d`; attempt
  `evt-31f2a399b3a7e11d-A-01`; output identity
  `evt-31f2a399b3a7e11d-A-01.first-pass-report.json`.
- **Auditor-B**: manifest `49c275d1304c38511e001b1dda0b9b7ca8c46284f27e44bc21dc4a2eea0e9127`;
  non-circular package `9fd5a36ce00c3ae7b773f4ae4a6fdecc3b3e4dc876d2dfa25da81e0f10e7bc25`;
  binding file `a83f962b036ea30b18e0fe6ec9af81af2e76572ae03c43d0fdbe318370d3fa51`;
  canonical binding digest `6600241f4233aec1c5df2097f6a6b9971bbbb137ef4d662b2a54d1a49a24639e`;
  **192 rows** / 343,393,217 payload bytes; event `evt-31f2a399b3a7e11d`; attempt
  `evt-31f2a399b3a7e11d-B-01`; output identity
  `evt-31f2a399b3a7e11d-B-01.first-pass-report.json`.

- Both row counts are EXACTLY the required 189/192 (no mechanically required reason
  arose); every manifest row's actual byte SHA/size verified; exact payload-set
  equality; manifest `transport_binding` == the binding projection both roles
  (non-circular package identity recomputed per the frozen composition).
- Shared-plane identities: prompt contract `e4204e673e56d62d4e4ba0aceb44cc5ca599cf2ddb4e774568977544ac3fdd73`
  (byte-identical A↔B); common-evidence manifest `e5bae46141b29a19b6e1184c0d428ffb1ce4d7ed88b600f99c9a8a14db332fab`
  (byte-identical A↔B, 167 members).
- A/B parity: `payload/evidence/**` = 169 files per role, same path set, **169/169
  byte-identical** (the accepted generation's parity holds).
- Blindness: no peer report/substance in either visible surface (peer-id occurrence is
  ONLY the frozen linter's own scan parameter inside `identity-linter.json`; zero
  elsewhere — verified); both role packages share the same new-event prompt contract.
- Semantic hold (`evidence/semantic-hold-proof.json`): PROMPT CONTRACT differs only in
  top-level event_id value; SANDBOX PROFILES differ only in top-level event_id metadata;
  OTHER AUDITOR-VISIBLE SUBSTANCE byte-identical unless mechanically identity-derived
  and explicitly classified; AUDIT TARGET unchanged (frozen five-field identity);
  REVIEW REQUIREMENTS unchanged; NEUTRALITY unchanged (expectation-token scan PASS both
  roles); EXPECTED FINDINGS/SEVERITY/VERDICT: none introduced.

## 9. §15 RESOURCE_GATE remediation HELD + positive fd-exec regression

The frozen gate bytes in BOTH new packages hash EXACTLY the accepted remediated gate
`27948980653f4c0639041243d9f117087f0987c5cc53623abbfa39cbb143adaf` (asserted before the
regression ran); launcher `2efb666042e44d272a53f9ad4ac93a19c14f1687a33fb38ed84f9823d9bc44a7`,
NETWORK_READINESS `20f37e9191d3e1e025962723328c5f8a2849f664cf1bf215715ccf8da9fc7235`,
auditor executables A `15e2d05148f801b5774032faad87e624ecd172e9903288bda448b892eb58fa07` /
B `3188814c35471432d4123203e0eb38e5bddc60226e3d7ddf0e59e649ea140022` byte-identical.
EXEC02-001/002 were NOT reopened; the accepted ARGV-1…ARGV-6 evidence remains the
retained mandatory gate evidence.

New §15 regression through the EXACT accepted EBS internal path
(`launch._run_runtime_gate → launch._gate_child → launch.fd_exec`, verified-open fd, env
exactly `{PATH:/usr/bin:/bin, LANG:C}`, the four-element EBS argv construction), with the
live EBS imported at the exact repository HEAD `eba943d7` + protected tree
`09f3d6c7…` asserted at run time, using the unmistakably synthetic
`evt-idegenprobe-*` namespace (disjoint from every reserved real attempt id)
(`evidence/fdexec-regression.json`, ALL PASS):

- **R1** historical negative: the OLD deployed gate bytes (`e8f85391…`) through the same
  path REFUSED `RESOURCE_GATE_NONZERO_EXIT: exited 3` BEFORE sampling (harness fidelity);
- **R2** positive BOTH roles on the NEW packages' gate bytes: strict envelope
  `AUCDEV-023-RESOURCE-GATE-RESULT-V1`, status PASS, exact NEW event/role/attempt echo,
  EXACTLY three samples ALL PASS (workspace/memory/process), probe workspace
  {staging, custody-out, accounting} created under the ACTUAL launcher root;
- **R3** the EXACT EBS `_validate_resource_gate_result` accepts the positive and REFUSES
  a context-tampered result;
- **R4** no reserved-attempt effect: historical old A-01/B-01 byte-unchanged vs the
  session baseline pin, NEW attempt dirs ABSENT before and after, only the two synthetic
  probe dirs appeared, no credential fd on the gate path, no provider/model process;
- **R5** complete cleanup: both probe dirs removed, attempts listing byte-restored.

Real NETWORK_READINESS was NOT run (zero network under this authority apart from the git
fetch/push of the canonical publication).

## 10. §16 future launch plans (DATA ONLY)

Per-role data-only launch plans recorded
(`evidence/launch-plan-auditor-{a,b}.json`), all mechanical checks PASS: deployment
source root (this workspace), future deployed package/binding/launcher/executable paths
under the unchanged future launcher root `/home/isa/aucdev023-s1-prep002-rem002/event/`,
exact report staging paths, custody-out roots, accounting roots, the future
`run_attempt` composition, the deployment precondition (a FUTURE operator action under a
NEW explicit execution authority: deploy at the launcher root's event/ location with the
currently deployed generation preserved by dated backup, and mechanically reverify the
deployed bytes to EXACTLY the new identities BEFORE any AccountingStore creation,
credential read, dynamic runtime gate, GATES_PASSED, CONSUMED_PRE_EXEC or provider/model
execution), and the ONE-BARRIER constraint (both blind passes MUST share the NEW event;
the historical old-event attempts MUST NOT be used; the historical execution authority
remains NO FURTHER EXECUTION / NO RETRY / NON-TRANSFERABLE). NOTHING was deployed; NO
attempt directory or accounting store was created; NOTHING was executed.

## 11. §17 historical immutability (before AND after — ALL EXACT)

Both phases recorded (`evidence/historical-immutability-{before,after}.json`; the
before-run pinned the byte baseline the after-run enforces):

- Historical A-01 accounting record SHA-256
  `d753df0274439019521a62a9456f64daa7d1bbe0f63c42df872fb5815867085d` byte-EXACT, states
  EXACTLY `PREPARED` → `TERMINAL_PREEXEC_STOP`, attempt tree exactly its accounting
  record with empty staging/custody; historical B-01 entirely EMPTY (NOT STARTED); all
  historical rehearsal attempt dirs byte-unchanged; the NEW attempts ABSENT throughout.
- Deployed historical event generation `/home/isa/aucdev023-s1-prep002-rem002/event/`
  (gate `e8f85391109d8f552294e9f887d2d3e90c145da87e1d0a648917cd681f71d6a6`; A 189 rows /
  236,260,421 B; B 192 rows / 343,391,382 B) fully row-verified byte-identical.
- Backup `event.backup.pre-exec02` (gate
  `960058b32b205eae5a46bc525cfa57b988315f3620191871044df03c6088d36d`; A 189 /
  236,260,424 B; B 192 / 343,391,385 B) fully row-verified byte-identical.
- The ACCEPTED EXEC02 argv-remediation source generation verified EXACT against every §5
  operator constant before AND after (A manifest `5b6bb4dc…` / package `0670817a…` /
  binding file `140c43e4…` / digest `5de31410…`, 189 rows / 236,262,080 B; B manifest
  `9c692e86…` / package `e56708f9…` / binding file `2e192073…` / digest `4f5624be…`,
  192 rows / 343,393,041 B; gate `27948980…`; launcher/NETWORK_READINESS/executables
  byte-identical).
- Historical prompt contract SHA `7973d643…` verified in all five accepted-copy
  locations before AND after.

The ONLY writes under the launcher root during the whole session were the two synthetic
`evt-idegenprobe-*` probe dirs created BY the gate during R2 and completely removed by
R5 (final listing byte-restored).

## 12. §18 deterministic regression (all PASS; protected sources UNCHANGED)

Executed in an isolated detached git worktree at the EXACT base `eba943d7` (worktree
removed after the run; host CPython 3.14.7 + pytest 9.1.1, the same isolated venv reused
as the accepted battery environment; zero network beyond git):

- `python -m compileall -q bootstrap-supervisor qualification-harness` → **rc 0** (one
  pre-existing historical SyntaxWarning in `qualification-harness/qh/statemachine.py`,
  unrelated, non-fatal);
- EBS deterministic battery → **489/489 PASS** (37.19 s; 0 failed / 0 skipped — exactly
  the accepted baseline, no count change);
- qh deterministic battery → **221/221 PASS** (27.24 s; 0 failed / 0 skipped — exactly
  the accepted baseline, no count change).

Classification: REGRESSION VERIFICATION ONLY — protected sources UNCHANGED (identity
regeneration builds workspace artifacts only); TEST_ENVIRONMENT_DIVERGENCE retained.

Validation sweep (`evidence/validation-sweep.json`, ALL PASS): hygiene census clean both
packages (189/189 and 192/192 regular == manifest set; symlinks/specials/hardlinks 0);
secret-shape scan over workspace evidence + components + event trees ZERO hits;
protected trees re-verified EXACT at the exact base; the unchanged frozen
output-validator executed offline against an unmistakably synthetic probe (fail-closed
rc 3 on the deliberately minimal probe); workspace-contract EXACT_MATCH both roles
(RESOURCE_GATE ROOT == LAUNCHER_ROOT == `/home/isa/aucdev023-s1-prep002-rem002`); blindness-map
consistency vs the frozen profile declarations both roles.

## 13. Zero-execution attestation (authority §19)

Provider/model/frontier inference ZERO; real credential bytes ZERO (no credential path
read; no custody ingest); Auditor-A/B//audit-council executions ZERO;
`Supervisor.run_attempt` ZERO; AccountingStore creation ZERO;
GATES_PASSED/CONSUMED_PRE_EXEC/EXEC_ATTEMPTED ZERO; real attempt ids sampled by any gate
ZERO (gate executions were EXACTLY the two synthetic `evt-idegenprobe-*` positive probes
plus the R1 historical-gate negative refusal, completely cleaned); real NETWORK_READINESS
NOT run; real attempt directories created ZERO; deployment ZERO; qualification NONE;
installation NONE. Replacement-event model engagements used **0 / 2**.
`MODEL_ENGAGEMENTS_USED_UNDER_THIS_AUDIT_POLICY = 0`.

## 14. Resulting state

- `AUCDEV-023-S1-NEW-EVENT-IDENTITY-REGEN-20260921-01` = PREPARED (this disposition);
  the new event generation is FROZEN read-only in the session workspace with the
  identities of §8; AWAITING_CONTROL_ROOM_READBACK.
- The candidate event `evt-31f2a399b3a7e11d` now HAS a complete frozen event-specific
  generation (packages + bindings + contract + evidence) but remains NOT DEPLOYED and
  NOT EXECUTED; both fresh attempts NOT STARTED.
- Historical everything IMMUTABLE (§11); the previous STOP record and every earlier
  record NOT rewritten; the historical prompt contract remains frozen historical
  evidence at `7973d643…`.
- INDEPENDENT FIRST-PASS EXECUTION remains NOT AUTHORIZED (a future explicit operator
  execution authority + deployment + pre-execution reverification are required; the
  historical execution authority remains NO FURTHER EXECUTION / NO RETRY /
  NON-TRANSFERABLE).
- AUCDEV-023 remains P1 / READY / NOT DONE with NO backlog count/status change
  (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11 unchanged — no mechanical
  backlog-row transition; no backlog item DONE; NO new finding minted).

## 15. Publication scope (this commit)

Exactly 3 changed paths: THIS NEW canonical record +
`docs/chatgpt-project/AUCDEV-CURRENT-STATE.md` (header + current-facing fields + dated
record + next-operator-action rotation) + `docs/chatgpt-project/AUCDEV-BACKLOG.md`
(dated record). ARCHITECTURE-SUMMARY UNCHANGED (identity regeneration changes no
architecture; the new-event-required planning constraint already recorded there stands).
No protected source change. The STOP record, the EXEC02 remediation/readback records
and every earlier record NOT rewritten. NO qualification-history row added. Pre-existing
smoke-fixture gitlink drift + evidence directories preserved unstaged. Exactly ONE
bounded fast-forward publication commit whose sole parent is `eba943d7…`, created only
after re-resolving live master at that exact SHA; post-push GitHub readback recorded in
the session evidence. The generated-LAST session handoff archive is produced AFTER this
publication at `/home/isa/aucdev023-s1-new-event-identity-regen/handoff/` with exactly
one SHA256SUMS covering every payload regular file except itself; nothing mutates
afterward.

## 16. NEXT ACTION EXACTLY ONE

**INDEPENDENT CONTROL ROOM READBACK OF THE NEW-EVENT IDENTITY-REGENERATED CONTRACT,
COMPLETE A/B SUCCESSOR PACKAGE BYTES, AND FUTURE LAUNCH-PLAN DATA.** NO deployment, NO
execution, NO event/attempt consumption and NO remediation is authorized by this
publication.
