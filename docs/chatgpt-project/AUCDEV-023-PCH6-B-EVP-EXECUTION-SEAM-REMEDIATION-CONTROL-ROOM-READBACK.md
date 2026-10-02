# AUCDEV-023 PCH6-B — EVP execution-seam remediation — Control Room readback PARTIALLY_ACCEPTED publication record

Publication authority `AUCDEV-023-PCH6B-730D2B29-EVP-CR-READBACK-PUB-20261003-01` (record-only).
Canonical date 2026-10-03 (Europe/Istanbul). Canonical record path: `docs/chatgpt-project/AUCDEV-023-PCH6-B-EVP-EXECUTION-SEAM-REMEDIATION-CONTROL-ROOM-READBACK.md`.

## 1. Disposition — recorded EXACTLY at the independently reached strength

```
AUCDEV_023_PCH6B_EVP_EXECUTION_SEAM_REMEDIATION_CONTROL_ROOM_READBACK =
PARTIALLY_ACCEPTED /
LIVE_PUBLICATION_05023A27_VERIFIED /
HANDOFF_INTEGRITY_VERIFIED /
RED_REPRODUCTIONS_VERIFIED /
EVP_RB_001_CLOSED_AT_CONTROL_ROOM_REMEDIATION_READBACK_STRENGTH /
EVP_RB_002_CLOSED_AT_CONTROL_ROOM_REMEDIATION_READBACK_STRENGTH /
EVP_RB_003_CLOSED_AT_CONTROL_ROOM_REMEDIATION_READBACK_STRENGTH /
EVP_RB_004_OPEN_BLOCKING /
AUDITOR_A_BOUNDARY_EVIDENCE_RETAINED /
AUDITOR_B_FAIL_CLOSED_NO_CREDENTIAL_EXPOSURE /
FRESH_GATE_W_PRIME_17_OF_19_FAIL /
CODEX_SECCOMP_ROOT_CAUSE_NOT_YET_ESTABLISHED_AT_CONTROL_ROOM_RAW_EVIDENCE_STRENGTH /
SUCCESSOR_PACKAGES_NOT_FROZEN /
OLD_PACKAGES_SUPERSEDED_PREPARATION_EVIDENCE_ONLY /
EVENT_NOT_INSTANTIATED /
ATTEMPT_AUTHORITIES_NOT_GRANTED /
MODEL_ENGAGEMENTS_USED_0 /
NO_AUDIT_EXECUTION /
NO_AUDIT_PASS /
QUALIFICATION_NONE /
INSTALLATION_NONE
```

This is a Control Room readback disposition over EVENT-PACKAGE REMEDIATION ARTIFACTS ONLY.
It is NOT an audit verdict. No frozen-target product finding is established by it, and none is closed by it.

## 2. Role and zero-execution boundary of THIS session

This session is the RECORD-ONLY CONTROL ROOM PUBLISHER of the ALREADY-completed independent
Control Room readback of publication `05023a273fd3b39a2389fa76051725b38070dab1`. It verifies the
exact live publication identity and the generated-LAST handoff DATA-ONLY, records the
already-reached disposition at exactly the reached strength (neither weakened nor strengthened),
corrects the CURRENT top-level active NEXT state, publishes exactly one bounded documentation-only
commit of exactly three paths, performs the post-push GitHub readback and generates exactly one
final non-secret handoff.

This session is NOT authorized to remediate the remaining Auditor-B blocker and remediates nothing.
It is NOT the Control Room decision-maker of the substantive readback (already completed), NOT an
event-package preparer, NOT a source/test/schema modifier, NOT an event-instantiation authority,
NOT an attempt-execution authority, NOT Auditor-A/B, NOT an independent auditor, NOT an Audit
Council `/audit-council` executor, NOT a provider/model/frontier executor, NOT a qualification
authority, NOT an installation authority. This publication grants NO authority of any kind and
closes nothing beyond the three remediation-readback closures recorded in sections 5-7.

Zero-execution boundary of THIS publication session: NO VM rehearsal executed; NO Codex or Claude
client executed; NO package binary executed (every executable verification below is byte-hash and
ELF-magic only, never execution); NO `/audit-council`; NO wrapper/driver invocation in the
AUCDEV-023 governance chain; NO BootstrapAuthority.run_attempt; NO source test; NO package-manager
fetch; NO credential-content access; NO sealed-substance access; ZERO privileged host operations of
any kind (no mount/pivot_root/umount/unshare/chroot/bwrap/nsenter); the input handoff inspected
DATA-ONLY in-memory with ZERO members extracted into the repository and ZERO members executed. The
only network operations are the ordinary Git/GitHub publication mechanics (fetch, ls-remote, the
one authorized push, the post-push GitHub readback).

## 3. Exact live bootstrap verification (performed BEFORE any edit)

- Live GitHub `master` == `origin/master` == local canonical HEAD ==
  `05023a273fd3b39a2389fa76051725b38070dab1` EXACT (ls-remote authoritative; fetch clean rc 0),
  re-resolved EXACT immediately before staging and immediately before commit.
- Authorized base root tree `f38876ee17ee761ab78189b54624ad6c18e26574` EXACT; sole parent
  `4b5a8010cb914c917d7f21e89d184185ef1193d7` = the EVP execution-seam remediation FAIL_CLOSED_HOLD
  whose recorded NEXT action — the independent Control Room readback — this record implements;
  single-parent fast-forward geometry.
- Trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor (rc 0).
- Frozen audit target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed` (root
  `2585796efd5cb6902226cfff785bb901297a15e3`) present, ancestor, UNTOUCHED, AUDIT SUBJECT /
  NOT AUTHORITY.
- Protected trees held EXACT at base AND in the staged write-tree: bootstrap-supervisor
  `3056e577259ab0b0b0472f82ebc306506f3e084c`, qualification-harness
  `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill `efd8c2e48edbb25795b3aacb1ce3c23fde10082a`,
  and the bootstrap-authority package tree `154975872e15d53e1706016f5bb60c83727004f0`
  (binding.py `1448c9cbfbb795c534f9f517052e998c636d28d6`, runtime.py
  `069c221fc1f84f9e8e8342ffed72ec761b9286b5`, custody.py
  `37e6b5bb4365c7b29ba3632fe95362d5a7e16c09`) — the bootstrap-authority source itself is
  UNCHANGED (a closure basis for sections 5-7).
- Zero staged content before this publication; the pre-existing untracked drift preserved
  UNSTAGED; this record's path ABSENT at base with zero full-history path rows.
- Read at the exact base: CURRENT, BACKLOG, the EVP execution-seam remediation report
  (Git-blob-equal to the handoff copy — section 4), the prior EVP Control Room HOLD
  (`docs/chatgpt-project/AUCDEV-023-PCH6-B-FRESH-KVM-EVENT-PACKAGE-PREPARATION-CONTROL-ROOM-HOLD.md`),
  and the live bootstrap-authority runtime/binding, whose execution ABI was re-derived statically:
  `_execute_dynamic_gate` builds argv `[descriptor identity, event_id, auditor_role, attempt, +
  gate-specific frozen identity values]`; `_run_validator(snapshot: bytes)` consumes the sealed
  report-snapshot bytes, never a pathname; `_child_setup` implements the fixed fd contract
  CRED_FD=3 sealed custody, FAIL_FD=4 CLOEXEC exec-fail pipe, AUDITOR_EXEC_FD=5 HELD verified
  auditor, AUDITOR_INVOCATION_FD=6 sealed frozen argv, then exec of the held fd (alias-safe).

## 4. Input generated-LAST handoff — DATA-ONLY integrity verification

Input: `AUCDEV-023-PCH6B-EVP-EXECUTION-SEAM-REMEDIATION-HANDOFF-20261003-01.tar.gz`

- Size 4148200 EXACT; outer SHA-256
  `e39afda54043422434686677036570e9166cba7c4cd5b3520b22839dc4d0c5d0` EXACT.
- Census 90 total members = 76 regular + 14 directories; 0 symlinks, 0 hardlinks, 0 special
  members, 0 duplicate names, 0 unsafe/traversal members.
- SHA256SUMS: 75 rows, NO self-row, exact payload-set equality TRUE, 75/75 independently
  recomputed PASS (in-memory; no extraction, no execution).
- Git-blob equality: the handoff's copies of the canonical remediation report, CURRENT and
  BACKLOG are byte-equal to the live Git blobs at the base.

## 5. EVP-RB-001 — CLOSED at Control Room remediation-readback strength

```
AUCDEV023-CR-PCH6B-EVP-RB-001 = CLOSED_AT_CONTROL_ROOM_REMEDIATION_READBACK_STRENGTH
```

Basis independently verified DATA-ONLY (readback basis re-verified from the handoff bytes by this
record-only session):

- The OLD RED reproduction is retained in the handoff: the old frozen gates driven with the EXACT
  authority argv — the old client-selection gate fails at its argv check (rc 2 usage error), and
  the old network-readiness gate's `{schema, gate, status, facts}` output is REFUSED by the LIVE
  runtime validator (`NETWORK_READINESS_RESULT_KEYS_INVALID`, missing `attempt_id`/`auditor_role`).
- All final executable artifacts are ELF (magic verified byte-side; identities in section 8).
- The client-selection, network-readiness and resource gates implement the current exact authority
  argv and emit the strict event/role/attempt-bound result envelopes accepted by the CURRENT live
  runtime validators: raw seam evidence (`instruments/green-rb001-network-seam.txt`,
  `vm-evidence/component-gates.json`) records the final gate results ALL-GREEN through the live
  validators for BOTH auditor roles with the exact evidence key sets, and the wrong-client-SHA
  negative REFUSED fail-closed (`CLIENT_SELECTION_PREFLIGHT_NONZERO_EXIT`, exited 4 — no fallback).
- Result key sets/schemas match the current runtime.
- The bootstrap-authority source itself is unchanged (protected tree held EXACT, section 3).

This is a harness/event-package remediation closure at remediation-readback strength. It is NOT an
audit PASS and NOT a frozen-target product verdict.

## 6. EVP-RB-002 — CLOSED at Control Room remediation-readback strength

```
AUCDEV023-CR-PCH6B-EVP-RB-002 = CLOSED_AT_CONTROL_ROOM_REMEDIATION_READBACK_STRENGTH
```

Basis independently verified DATA-ONLY:

- The final launcher is native ELF, exact SHA-256
  `df5221bfd19907055bb43d6c0114f25248a8a789a5f8a098bc0efa85d130550e`.
- Production argv matches the authority: identity / `--role` `AUDITOR_A|AUDITOR_B` / `--attempt`
  / `--event`.
- FD3 is the credential channel; FD5 is the HELD auditor executable; FD6 is the sealed
  invocation; NO caller client pathname/tail is authoritative.
- Client exec uses held-fd `execveat(..., AT_EMPTY_PATH, ...)`; the handoff retains the fd-exec
  seam proof that shebang scripts cannot be exec'd through that seam (the old Python artifacts
  were therefore mechanically unexecutable through the authority seam at all).
- The synthetic composition passes through the SAME runtime `_child_setup()` seam
  (`vm-evidence/component-launch.json`): returncode 0; EXACTLY ONE bounded launcher metadata JSON
  object on stdout; client writable set EXACTLY `{/, /cred, /home, /out, /tmp}`; tool set EXACTLY
  `{/, /home, /out, /tmp}`; credential read+refresh succeed at the sealed role layout while the
  tool credential read is ABSENT; client processes invisible in the fresh tool PID namespace;
  sink append lands in the authority-bound sink; credential teardown DETACHED.
- The held-fd alias test (`vm-evidence/component-alias.json`) proves pathname replacement cannot
  substitute the executable: ELF A exec'd with A's pathname replaced by B — the exit code proves
  the HELD A ran, not the pathname.

No real reserved `run_attempt` occurred (zero-execution census, section 15).

## 7. EVP-RB-003 — CLOSED at Control Room remediation-readback strength

```
AUCDEV023-CR-PCH6B-EVP-RB-003 = CLOSED_AT_CONTROL_ROOM_REMEDIATION_READBACK_STRENGTH
```

Basis independently verified DATA-ONLY:

- The final validator is native ELF, exact SHA-256
  `b38d12b5bd8361bce44af16939fb1edf3cf55aaf3953baecf50c1f5cbe8fa65c`.
- Exact authority argv shape; report snapshot read from FD3; NO report-path reopen.
- Correct result schema/key set; at the exact `_run_child_once()` +
  `_validate_validator_result()` seam the valid case PASSES.
- The full negative matrix REFUSES fail-closed with bounded `structural_error` tokens
  (`instruments/green-rb003-validator-seam.txt`): digest mismatch; size mismatch; malformed JSON;
  non-object root; trailing bytes; missing/bad FD channel.

## 8. EVP-RB-004 — remains OPEN / BLOCKING

```
AUCDEV023-CR-PCH6B-EVP-RB-004 = OPEN / BLOCKING
```

The final raw formal aggregate is `formal-20261002T221142`. Recomputed EXACTLY by this session
from the handoff's `vm-evidence/gatew/combined.json` (19 rows, `statuses_exact_equality_only`,
aggregation `overall = "PASS" if all(s == "PASS") else "FAIL"`):

- OVERALL: FAIL. 17 / 19 rows PASS.
- The two FAIL rows are GWP-10 (the exact pinned codex sandbox application-profile row:
  positive, negative-etc and negative-opt all refuse with launch rc 126, no files, nothing
  written; undefined profile rc 1) and the Codex-dispatch GWP-07 row
  (`real_codex_tool_domain`: dispatch-cred and dispatch-sink both launch rc 126 with
  `cred_read_rc` ABSENT and `sink_read_rc` ABSENT). GWP-07 carries three rows in this run — the
  client-domain row and the wrapper-covered tool row PASS; only the real-codex row FAILs.
- Both final Codex cases REFUSE with launch rc 126. This is FAIL-CLOSED. NO credential exposure
  is established (the raw rows show absent reads).
- Because Auditor-B has no functional accepted tool domain, final
  REAL_CLIENT_CREDENTIAL_TOOL_ISOLATION PASS is NOT established for Auditor-B.
- Auditor-A boundary evidence is RETAINED at the strength reached by the remediation session
  (exact writable sets in both domains; GWP-11 net-vs-noegress writable sets byte-equal; GWP-12
  exact frozen screen fires on the planted synthetic marker and passes the clean report).

Final executable identities verified this session (SHA-256 recomputed from the handoff bytes;
ELF magic verified; never executed): client-selection gate
`1029e9c2bc68c1b6c5baf63287572ac3d70e6bdf106f27bb349c38772d441093`, network-readiness gate
`b2407af19167b82e7c89e11f8b4071a7052d4d4c7fb0400ca648e863db44a0c0`, resource gate
`034abc6019193933d2011733725da573e118bcec3e4b23bf834c2a651db999a1`, validator
`b38d12b5bd8361bce44af16939fb1edf3cf55aaf3953baecf50c1f5cbe8fa65c`, launcher
`df5221bfd19907055bb43d6c0114f25248a8a789a5f8a098bc0efa85d130550e`, tool wrapper
`52d1864faf3bea456a9d7380aaeaab093a1ae109eaa3d0d6531be554fea80d5c`; profiles V2 Auditor-A
`b552e40bc748e43938b9573d9f346a57192d112ff0666bf93de1d2f61f1d3cc7` and Auditor-B
`286365281fa64ed8addfa6c77cb63663d8f0561cde1d2cf5ee6689fb0ec4ac1b`.

## 9. Root-cause evidence precision

The implementation report/session ledger states
`AUDITOR_B_CODEX_TOOL_DOMAIN_NS_SPLIT_BLOCKED_BY_SANDBOX_SECCOMP` and describes wrapper
interception with actual `sh -c` Codex argv capture, `Seccomp:2`, `unshare(CLONE_NEWNS)` EPERM,
root-level credential-path readability, and a bwrap route observed in another environment.
HOWEVER the generated-LAST handoff does NOT contain the raw wrapper journal / raw
seccomp-process-status artifact that independently establishes those load-bearing observations
(observed archive fact — section 10). Therefore the Control Room records:

```
AUDITOR_B_CODEX_TOOL_DOMAIN_BLOCKER = OBSERVED_FINAL_FUNCTIONAL_FAILURE
SANDBOX_SECCOMP_AS_EXACT_ROOT_CAUSE =
INFERENCE / IMPLEMENTER_REPORTED /
NOT_YET_ESTABLISHED_AT_CONTROL_ROOM_RAW_EVIDENCE_STRENGTH
```

The omitted raw evidence is NOT fabricated. The standing finding ROOT_CAUSE_NOT_ESTABLISHED is
unchanged; NO causal conversion is made anywhere by this record.

## 10. Exact Codex 0.159.3 external-source orientation (classification)

The substantive readback additionally inspected the exact upstream source at the OpenAI Codex tag
`rust-v0.159.3`. This is EXTERNAL ORIENTATION, not package evidence. It establishes that
`codex sandbox -P ...` uses the permission-profile surface; that the Linux sandbox construction
has a normal outer bubblewrap path; that the helper's `--apply-seccomp-then-exec` mode is an inner
stage AFTER bubblewrap has already established the filesystem view; and that legacy Landlock is a
separately selected path. Therefore the narrow next investigation SHOULD first determine whether
the credential/tool split can be moved to or composed with the PRE-SECCOMP / OUTER-BWRAP seam of
the exact pinned client. This does NOT prove that such remediation will succeed; it means broad
Auditor-B rerole/redesign is NOT yet forced by current evidence. Classification: EXTERNAL SOURCE
ORIENTATION / REMEDIATION HYPOTHESIS — not established repository fact. (This orientation was
performed by the substantive readback session; THIS record-only session performed no external
fetch beyond the ordinary Git publication mechanics.)

## 11. Evidence residual EVP-RB-EV-001

```
AUCDEV023-CR-PCH6B-EVP-RB-EV-001
Title:    AUDITOR_B_RAW_WRAPPER_SECCOMP_JOURNAL_ABSENT_FROM_GENERATED_LAST_HANDOFF
Classification: COMPLETENESS LIMITATION
Support:  OBSERVED ARCHIVE FACT
```

Verified archive fact: no member of the generated-LAST handoff is a raw wrapper journal or a raw
seccomp/process-status capture, and no member contains raw process-status field lines; only
narrative references (report, session ledger, FINAL-RETURN) and the diagnostic instrument that
would have produced the observations are present. Effect: does NOT invalidate the HOLD; does NOT
reopen EVP-RB-001..003; prevents the Control Room from independently establishing the claimed
precise seccomp root cause (hence the precision split in section 9).

## 12. Governance-record precision correction (CURRENT top-level active state)

At the publication base, CURRENT's top-level active section contained BOTH the stale
pre-remediation NEXT (asking whether to authorize EVP-RB-001..004 remediation — remediation that
the operator had already explicitly authorized and that has been executed) AND the then-current
NEXT (requesting this readback and the subsequent decision). This publication REMOVES the stale
superseded NEXT so that the top-level active state contains EXACTLY ONE current NEXT (section 16).
Historical dated records are NOT rewritten (an evidence-precision observation is recorded here:
at the base, the remediation session's own CURRENT tail entry was appended as a bare
disposition-token line without its own dated-section header; that historical formatting residual
is retained unmodified under the append-only rule).

## 13. Governance state after readback (retained exactly)

- AUCDEV-023 = P1 / READY / NOT DONE (no queue transition solely because this readback is
  published).
- GATE_W_PRIME = FAIL at final event-boundary strength.
- EVP-RB-001 = CLOSED at remediation-readback strength; EVP-RB-002 = CLOSED at
  remediation-readback strength; EVP-RB-003 = CLOSED at remediation-readback strength.
- EVP-RB-004 = OPEN / BLOCKING.
- Successor event packages = NOT FROZEN. Old packages = SUPERSEDED PREPARATION EVIDENCE /
  NO EXECUTION AUTHORITY.
- Event = NOT INSTANTIATED. Attempt authorities = NONE. Engagements used = 0 (PROPOSED 2
  unchanged).
- Independent-auditor provenance / authority gate = NOT_SATISFIED (stated ONLY as NOT satisfied;
  installed source `8ae33444f349ce73c1359b963722e2d16acba630`, independently-qualified predecessor
  provenance NOT ESTABLISHED).
- PCH6-B-SD-002 = NOT CLOSED. PCH6-CR-BSD-001 = NOT CLOSED. PCH6-B-SD-001 = RETAINED / OPEN.
- ROOT_CAUSE_NOT_ESTABLISHED = unchanged (NO causal conversion).
- Qualification = NONE. Installation = NONE.
- Historical PCH6 authority CONSUMED / TERMINAL / CLOSED / NO_RERUN with all historical
  identities NON-TRANSFERABLE and the AUCDEV-010 bootstrap-root exception NON-TRANSFERABLE.
- Prior BA-PREP/BA-RB and prior EVP preparation/readback records RETAINED and NOT reopened;
  historical records and handoffs NOT rewritten, NOT repacked.

## 14. Publication safety (this record-only session)

- Staged EXACTLY the three authorized documentation paths: NEW canonical readback record (this
  file); CURRENT modified with the rotation confined to the top-level active lines (last-updated
  line, canonical-base line, AUCDEV-023 status bullet, and the two superseded NEXT lines replaced
  by EXACTLY ONE new NEXT) plus one NEW dated tail record; BACKLOG modified with EXACTLY two pure
  insert zones (one NEW dated status bullet immediately after the EVP remediation status bullet,
  plus one NEW dated tail record), zero replace/delete.
- Both CURRENT and BACKLOG edits were computed-before-write by assertion-guarded builders and the
  zone sets were re-asserted FROM the staged blobs.
- The staged write-tree holds the protected trees and the bootstrap-authority package tree EXACT;
  therefore ZERO source modification staged and ZERO performed.
- Staged == working on all three paths; `git diff --check` and staged `git diff --cached --check`
  PASS; no source/test/package path staged, no `.jsonl`, no event-package tracked path, no
  VM/binary artifact committed.
- Queue mechanically recounted base == staged on every structural dimension (queue table rows
  byte-identical still AUCDEV-023 P1/READY; no queue-row status transition; no backlog item
  marked DONE; the one new `##` section is the dated tail record).
- Wording gates PASS wrap-aware (NO causal conversion of ROOT_CAUSE_NOT_ESTABLISHED;
  frozen-target closure mentions always negated; audit-PASS mentions always negated; provenance
  gate stated ONLY as NOT satisfied; NO unnegated event-instantiation claim; grants-nothing
  present; disposition token present in the record and in CURRENT).
- Credential/secret mechanical scan clean over the NEW record and all diff-added lines; hex-literal
  gate PASS with every >=7-char non-decimal hex literal machine-verified case-insensitively
  against the session-derived independently-verified identity allow-set (decimal-only exempt).
- The FULL record-only precommit gate battery ran from scratch on the FINAL staged bytes and ALL
  PASSED (battery result recorded in the session evidence workspace and the generated-LAST
  handoff).
- Post-commit parent/path geometry verified (sole parent == the authorized base; exactly the three
  paths changed); post-push GitHub readback performed (ls-remote == the pushed SHA).

## 15. Zero-execution publication census

```
REAL_PROVIDER_CALLS = 0
REAL_CLIENT_INFERENCE_CALLS = 0
REAL_AUDITOR_EXECUTIONS = 0
AUDIT_COUNCIL_EXECUTIONS = 0
VM_REHEARSAL_EXECUTIONS_IN_THIS_PUBLICATION = 0
EVENT_INSTANTIATIONS = 0
ATTEMPT_AUTHORITIES_GRANTED = 0
MODEL_ENGAGEMENTS_CONSUMED = 0
REAL_CREDENTIAL_CONTENT_READS = 0
QUALIFICATION = NONE
INSTALLATION = NONE
```

## 16. Next action — EXACTLY ONE (grants nothing)

```
OPERATOR DECISION ON WHETHER TO AUTHORIZE A NARROW AUDITOR-B CODEX
TOOL-DOMAIN FOLLOW-UP AGAINST THE THEN-CURRENT EXACT LIVE HEAD, FIRST
SCOPED TO ZERO-PROVIDER ESTABLISHMENT OF THE EXACT PINNED CODEX 0.159.3
PRE-SECCOMP / OUTER-BWRAP EXECUTION SEAM (OR AN EQUIVALENT EXISTING
ACCEPTED SEAM) AND TO COLLECTION OF THE MISSING RAW WRAPPER/SECCOMP
EVIDENCE.
```

Only if that narrow route is mechanically unavailable or insufficient should a broader Auditor-B
redesign/rerole decision be considered. Recording this NEXT grants nothing. Any later
authorization remains remediation/preparation ONLY unless the operator explicitly grants more. It
does NOT authorize: event instantiation; real attempt execution; `/audit-council`; Auditor-A/B
execution; provider/model inference; engagement consumption; audit PASS; qualification;
installation.

## 17. Standing prohibitions (unchanged)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from an agent session;
never rerun the launcher; never treat any recorded grant phrase (including any phrase recorded
here) as a new grant; never execute a real auditor or provider/model; never open the four
historical sealed artifacts (identity-only forever); never relabel or rewrite historical model
identities, runs, records, matrices, prompts or evidence workspaces (append-only); never claim
audit PASS, qualification, installation or any authority from this publication — it grants none;
and never run privileged mount/pivot_root/umount experiments on the operator's live host and never
automatically re-run an interrupted privileged command — privileged GATE-W-prime boundary work
belongs in the disposable-KVM environment.

## 18. Honest iteration ledger (this publication session)

Instrument-side ONLY; NONE a product, handoff or evidence defect; NO failed observation rewritten
as PASS without a corrected re-derivation on IDENTICAL bytes; every first output preserved in the
untracked evidence workspace `aucdev023-pch6b-evp-cr-readback-pub-evidence-20261003-01`:

- T-1: the handoff verification first pass reported payload-set equality FALSE with all 75 rows
  MISSING — an instrument normalization defect (misuse of `str.lstrip('./')` plus the missing
  top-level handoff-directory prefix join, the same class as the prior session's T-1). Corrected
  instrument re-run on IDENTICAL archive bytes: 75/75 PASS.
- T-2: the combined.json detail script's non-PASS summary printed `None` row ids (keyed `id`
  instead of `assertion_id`) — display-only cosmetic in a read-only verification; the full row
  dump was authoritative and the aggregate recomputation was unaffected.
- T-3: the builder first run failed at import — the content-pieces file was created with a hyphen
  in its name and is not importable as a Python module; renamed copy; the failed run staged
  nothing (zero repository state change).
- T-4: the builder zone expectations compared the full difflib opcode lists INCLUDING the 'equal'
  blocks (CURRENT twice, then the BACKLOG append-only check); each assertion fired BEFORE any
  write — the constructed bytes were already correct; the comparison now filters 'equal' blocks.
- T-5: the battery's protected-tree gate crashed resolving the staged write-tree (output not
  stripped before interpolation) — a read-only crash with zero state change; fixed with a strip.
- T-6: battery v1 reported five FAILs — four were instrument defects of the known false-FAIL
  class (the `NO_` prefix-adjacency missed inside the `NO_AUDIT_PASS` disposition token; negator
  windows 45/60 chars too narrow for the governing `does NOT authorize ...` list form and for the
  `= 0` census zero-form; a raw-text needle check breaking on wrapped lines; the preserved-form
  detector missing the `NO causal conversion` form); ONE was a real content-fidelity fix on the
  staged bytes — the CURRENT NEXT line now restores the tasking sentence boundary after
  `...SECCOMP EVIDENCE.` before the `Only if ...` sentence. After the corrections the builder
  re-staged and battery v2 re-ran on the corrected FINAL staged bytes: 24/24 PASS.
