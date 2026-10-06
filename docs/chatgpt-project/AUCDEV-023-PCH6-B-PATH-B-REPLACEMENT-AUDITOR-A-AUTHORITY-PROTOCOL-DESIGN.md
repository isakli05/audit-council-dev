# AUCDEV-023 PCH6-B Path-B Replacement Auditor-A Authority-Protocol Design (DESIGN ONLY — NOT IMPLEMENTED)

AUCDEV_023_PCH6B_REPLACEMENT_AUDITOR_A_AUTHORITY_PROTOCOL_DESIGN =
DESIGN_COMPLETED_AS_CANDIDATE /
EXISTING_GOVERNANCE_EVENT_PRESERVED /
REPLACEMENT_IDENTITY_PROTOCOL_DESIGNED /
NON_EXECUTION_PACKAGE_GRANT_PROTOCOL_DESIGNED /
HISTORICAL_V1_SEMANTICS_PRESERVED /
ONE_SHOT_NO_RETRY_PRESERVED /
PACKAGE_BINDING_EXECUTION_AUTHORITY_SEPARATION_PRESERVED /
PKGIDENT_001_REMAINS_OPEN /
PKGIDENT_002_REMAINS_OPEN /
NO_PROTECTED_SOURCE_MODIFICATION /
NO_ATTEMPT_ID_CREATED /
NO_AUTHORITY_TOKEN_MINTED /
NO_ACCOUNTING_STATE /
NO_PACKAGE_COMPLETION /
NO_EXECUTION_AUTHORITY /
AUDITOR_B_AUTHORITY_NONE /
AUDIT_VERDICT_NONE /
QUALIFICATION_NONE /
INSTALLATION_NONE /
AWAITING_INDEPENDENT_CONTROL_ROOM_DESIGN_READBACK

DESIGN_ONLY / NON_AUTHORITY / NO_ATTEMPT_ID_CREATED / NO_AUTHORITY_TOKEN_MINTED /
NO_EXECUTION_AUTHORITY / NO_IMPLEMENTATION_AUTHORITY / NOT_VALID_FOR_INVOCATION

THIS DESIGN GRANTS NOTHING. IT IS NOT AN IMPLEMENTATION, NOT AN ATTEMPT
AUTHORITY, NOT AN EXECUTION AUTHORITY, AND CLOSES NEITHER PKGIDENT-001 NOR
PKGIDENT-002 (both remain OPEN / BLOCKING).

## 1. Authority

Implementation authority: AUCDEV-023-PCH6B-REPLACEMENT-AUDITOR-A-AUTHORITY-PROTOCOL-DESIGN-20261006-01
(dated 2026-10-06). The operator authorized ONLY:

"AUTHORIZE AUCDEV-023 a bounded zero-model AUTHORITY-PROTOCOL DESIGN ONLY
for exactly ONE future replacement Auditor-A attempt within the existing
governance event
AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01,
addressing PKGIDENT-001 and PKGIDENT-002 by defining, without
implementation or execution: (A) the minimum protected bootstrap-authority
contract representation for one new single-use replacement Auditor-A machine
attempt identity without reusing the spent AUDITOR-A-01 identity or creating a
second governance event, and (B) the canonical NON-EXECUTION package
authority/grant-token schema, derivation/minting semantics, verification
semantics, lifetime and one-shot binding required by active-v3. The design must
preserve the frozen target, one-event boundary, one-shot/no-retry semantics,
protected-authority separation, fail-closed accounting discipline, and the
strict separation between package-binding authority and later execution
authority. This authority grants NO protected-source modification, NO attempt
identity creation/reservation/allocation, NO authority-token minting, NO
accounting/runtime state, NO package completion, NO
successor/wrapper/driver execution, NO credential access, NO
channel/VM/QGA/run_attempt/model execution, and NO Auditor-B authority.
PKGIDENT-001 and PKGIDENT-002 remain OPEN until a separately authorized
implementation is independently reviewed."

THIS IS DESIGN AUTHORITY ONLY. It does NOT authorize implementation of the
design. This session is the bounded DESIGNER: NOT the Control Room, NOT an
implementer, NOT an attempt-id allocator, NOT a token minter, NOT an attempt
executor, NOT an execution-authority grantor, NOT an auditor, NOT an
/audit-council executor, NOT an Auditor-A or Auditor-B attempt executor, NOT
an attempt authority, NOT a provider/model/frontier executor, NOT starting or
defining the event-host VM, NOT running virsh/QGA, NOT running send_once_v2.py
or bridge-v2.py or any channel helper, NOT creating or consuming
OPERATOR_SEND_NOW, NOT connecting to or probing the credential channel, NOT
inspecting any real credential, NOT constructing or importing
BootstrapAuthority, NOT calling run_attempt, NOT executing Claude, Codex or any
provider/model, NOT granting Auditor-A or Auditor-B authority, NOT a
qualification or installation authority.

## 2. Exact live bootstrap (verified this session, read-only)

Live GitHub master == origin/master == local HEAD ==
01da201367f041ef59daa22abd9e0ffcd5e3dcc2 EXACT (ls-remote authoritative;
fetch rc 0), re-resolved again immediately before staging and immediately
before commit. Root tree 60bce73c1730fd21a2b981f6cb9e79d3015e1396 EXACT; sole
parent a494d3df425ae6d2a6f198b21bc9c30866c06283 EXACT (single-parent
fast-forward geometry). Canonical blobs verified at the exact base: CURRENT
b0f834b8d2b69e15f41e2010b768a6b6a6971840; BACKLOG
384dc4f6d1fa0df9df9d8baeeaa41206800a15ff; accepted minimum-identity/binding
Control Room readback 29f8c3261740e006b4c932e6416c94ffc8e696a9; update
protocol 42955b85710f09579cd0fd9174d042de231d060d. Protected
bootstrap-authority tree 154975872e15d53e1706016f5bb60c83727004f0 EXACT with
source blobs binding.py 1448c9cbfbb795c534f9f517052e998c636d28d6, runtime.py
069c221fc1f84f9e8e8342ffed72ec761b9286b5, accounting.py
26368783dd88782dd3c63a76fbf11582ee16caa1, statemachine.py
cf563d2178907e7666ce661b81ab1bf16fb71201. Frozen audit target
730d2b29f7c0e7d33af3451b6d9205ec27c143ed (tree
2585796efd5cb6902226cfff785bb901297a15e3) present, ancestor, UNTOUCHED,
AUDIT SUBJECT / NOT AUTHORITY. Trust anchor 3058868416241d394cfaaa40cc585085db486f37
ancestor rc 0. This record's path ABSENT at base with zero full-history path
rows. CURRENT/BACKLOG working copies verified byte-identical to the base blobs
before editing. Repository drift (pre-existing untracked workspaces/handoffs
and the two pre-existing smoke-fixture gitlink rows) preserved UNSTAGED.
Session euid 1000 (ordinary non-root isa).

## 3. Held governance state (unchanged)

AUCDEV-023 P1 / READY / NOT DONE. Governance event
AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01 INSTANTIATED / PATH-B BOUND /
NO_SECOND_EVENT — preserved; the design represents NO second event. Existing
Auditor-A machine attempt ...-AUDITOR-A-01 SPENT / SINGLE-USE / NO-RETRY —
NOT reused, NOT revived, and mechanically EXCLUDED from replacement use by the
selected design. NO replacement Auditor-A attempt exists, is reserved, is
allocated or is minted. PKGIDENT-001 OPEN / BLOCKING_VALID_REPLACEMENT_PACKAGE_IDENTITY_BINDING;
PKGIDENT-002 OPEN / BLOCKING_VALID_REPLACEMENT_PACKAGE_AUTHORITY_BINDING
(both remain OPEN / BLOCKING_IMPLEMENTATION / DESIGN_CANDIDATE_AVAILABLE /
NOT_CLOSED after this design). PREARM-001 / ACTIVATION-001 / OPADOPT-PREP-001 /
HANDOFF-001/002 / INT-001/002 CLOSED (retained). Successor
CONTROL_ROOM_ACCEPTED_ACTIVE_SUCCESSOR_GATE / MODE_0500 /
NOT_ATTEMPT_AUTHORITY. Auditor-B authority NONE; FIRST_PASS_A ABSENT; audit
verdict NONE; qualification NONE; installation NONE.

## 4. Observed protected contract facts (re-derived DATA-ONLY at the exact base; modules NEVER imported or executed)

binding.py (blob 1448c9cb, content SHA-256
fa94691d23a84a917e98d38f57eeda4bb15fadbd8012f4d83515b9f18c4715c0, 605 lines):
EVENT_ID assigned exactly once (line 72); RESERVED_ATTEMPT_IDS assigned once
(lines 73-78; the AUDITOR_A entry at line 75 IS the spent single-use identity);
ROLES (line 79); POLICY_ID (lines 47-48); BINDING_SCHEMA V1 (line 146);
AUTHORITY_MANIFEST_SCHEMA V1 (line 187) with closed AUTHORITY_MANIFEST_KEYS
(lines 188-192) including design_event_id and design_attempt_ids; strict parse
gates at lines 411-425 (BINDING_SCHEMA_UNEXPECTED / POLICY_ID_UNEXPECTED /
EVENT_ID_UNEXPECTED / AUDITOR_ROLE_UNKNOWN / ATTEMPT_ID_NOT_THE_RESERVED_IDENTITY_FOR_ROLE).

runtime.py (blob 069c221f, content SHA-256
f90338087f214ce0b4af5659afff9b4001398c5896a4dc97ffeae6885225427a, 1662 lines):
lines 13-24 the NON-EXPORTABLE AUTHORITY PROCESS STATE model with the whole
irreversible lifecycle inside the ONE public operation
BootstrapAuthority.run_attempt(...) and NO
grant/consume/resume/retry/adopt_report/finish/mint_attempt/create_event
surface; AST census: public surface exactly {state, store, run_attempt} and
NONE of the eight forbidden names defined anywhere; authority-manifest
verification at lines 413-440 (closed key world, schema, policy_id, target,
design_event_id == EVENT_ID at lines 435-436, design_attempt_ids ==
RESERVED_ATTEMPT_IDS at lines 437-440); accounting_name(binding) returns
exactly binding.attempt_id (lines 184-188) — ONE machine attempt id = ONE
global runtime accounting claim.

accounting.py (blob 26368783, content SHA-256
4ea6d871b175a5354448b650fbbbd03ff77f6e98940a343ccc95eca50382b2b4, 239 lines):
AccountingStore.create_at opens the per-attempt record with
O_WRONLY | O_APPEND | O_CREAT | O_EXCL | O_NOFOLLOW (lines 103-106), appends
the initial state (line 121), refuses any non-PREPARED first record
(FIRST_RECORD_MUST_BE_PREPARED, lines 139-140); create wraps create_at.

statemachine.py (blob cf563d21, content SHA-256
f60fcb9108d353a11f3ff8916780b3e91108a1d2c2d278e0b2c40e2b6643c57a, 102 lines):
PREPARED -> GATES_PASSED -> CONSUMED_PRE_EXEC -> EXEC_ATTEMPTED -> ... ->
TERMINAL with TERMINAL_PREEXEC_STOP / TERMINAL absorbing; no reset, retry or
resume.

## 5. Design Problem A — replacement attempt identity (PKGIDENT-001)

Options scored against historical stability / mechanical one-shot strength /
execution-authority separation / implementation size / parser simplicity /
replay resistance / auditability / failure clarity / future-extension risk
(full machine-readable table in the external workspace evidence/option-analysis.json):

- ID-OPT-A IN_PLACE_V1_EXPANSION — REJECTED. Decisive defect: runtime.py
  lines 437-440 require manifest["design_attempt_ids"] == RESERVED_ATTEMPT_IDS,
  so expanding the mapping retroactively changes the required manifest content
  set and breaks re-verification of every historical V1 authority manifest;
  it also implies A-01 was always one entry of a larger registry, which was
  never the contract (Section 18 violation); no era signal invites unbounded
  growth.
- ID-OPT-C FIELD_PRESENCE_DISPATCH (optional field, no version tag) —
  REJECTED. Decisive defect: schema ambiguity; absence-vs-rejection ambiguity
  lets a dropped field silently downgrade a replacement manifest to V1
  interpretation instead of failing closed (the dynamic-fallback shape the
  authority constraints forbid).
- ID-OPT-B ADDITIVE_VERSIONED_V2_SINGLE_SLOT_REPLACEMENT_CONTRACT — SELECTED.

Selected identity contract (full specification in the external workspace
design/IDENTITY-CONTRACT-DESIGN.md): every V1 byte, check, manifest equality
and historical evidence meaning preserved unchanged; a NEW additive,
version-tagged V2 binding/authority-manifest representation carrying exactly
ONE new role slot key AUDITOR_A_REPLACEMENT_1 whose attempt-id value is a
single strict module constant REPLACEMENT_ATTEMPT_SLOTS with exactly one
entry; identity grammar (closed derivation, the only place the suffix literal
appears): replacement_slot_value := EVENT_ID + "-AUDITOR-A-R1", where the
suffix is an OPAQUE FIXED LITERAL — no ordinal arithmetic, no R2 or any
further slot, no enumeration, no discovery, no fallback; every concrete design
example uses ONLY the symbolic marker FUTURE_REPLACEMENT_AUDITOR_A_ATTEMPT_ID
and the concrete concatenated value is NOT instantiated, emitted, reserved or
made operative by this session — it becomes real only inside protected source
at a separately authorized implementation, assigned exactly once and compared
only by equality. V2 parse gates (all fail-closed, distinct tokens): schema
must equal BINDING_SCHEMA_V2; policy_id must equal the UNCHANGED POLICY_ID;
event_id must equal the UNCHANGED EVENT_ID (no second event is representable);
auditor_role values AUDITOR_A / AUDITOR_B are refused with
AUDITOR_ROLE_NOT_PERMITTED_IN_V2 — this is the MECHANICAL EXCLUSION of the
spent A-01 identity from replacement use (its role is not representable in V2
and its value never equals the slot constant); attempt_id must equal the slot
constant or ATTEMPT_ID_NOT_THE_RESERVED_IDENTITY_FOR_ROLE refuses every
arbitrary caller-selected, hash-derived, timestamp-derived, UUID-shaped,
TEST-ONLY or free-form value (an attacker-minted ordinal variant such as an
"A-02"-shaped hypothetical is just another non-equal string); closed-world key
sets. V2 manifest: every V1 key with UNCHANGED checks (including
design_event_id == EVENT_ID and design_attempt_ids == RESERVED_ATTEMPT_IDS,
preserving historical meaning verbatim) plus the additive
design_replacement_attempt_ids == REPLACEMENT_ATTEMPT_SLOTS equality (and the
package_grant reference of Problem B when implemented). Accounting, output
identity, gate evidence and transport projection semantics UNCHANGED —
accounting_name(binding) == binding.attempt_id still makes ONE machine attempt
id = ONE global O_EXCL accounting claim, so the slot constant is claimable
exactly once with initial PREPARED state and absorbing terminal semantics.
After the future replacement attempt is spent: immutable accounting evidence,
slot remains spent exactly as A-01 does, no reset/revival, no second slot
inferable — any further replacement requires a new protected-contract change,
a new operator decision and an independent Control Room readback.

## 6. Design Problem B — canonical NON-EXECUTION package authority/grant token (PKGIDENT-002)

Options (same criteria; full table in evidence/option-analysis.json):

- GR-OPT-A PURE_CONTENT_DIGEST_ONLY — REJECTED as the SOLE mechanism: content
  binding cannot mechanically prevent two frozen packages embedding the same
  grant digest; one-shot would be narrated, not enforced. Retained as the
  token-identity mechanism inside the selected design.
- GR-OPT-C INDEPENDENT OPAQUE RANDOM IDENTIFIER + grant document — REJECTED:
  for a NON-SECRET document a nonce adds entropy management, secret-adjacent
  handling and extra replay-check state while weakening auditability;
  randomness is unnecessary (no entropy requirement; nothing secret to
  persist; replay checks are content equality + ledger existence).
- GR-OPT-B CANONICAL CONTENT-ADDRESSED GRANT DOCUMENT + APPEND-ONLY
  NON-RUNTIME ONE-SHOT BINDING RECEIPT — SELECTED.

The design defines what "authority token" means in active-v3 for package
preparation: a NON-SECRET, CONTENT-ADDRESSED PACKAGE-BINDING GRANT — the
SHA-256 digest of a strictly-schema'd canonical grant DOCUMENT (schema tag
AUCDEV-023-PACKAGE-BINDING-GRANT-V1, closed world) binding: purpose constant
NON_EXECUTION_PACKAGE_BINDING; operator_authority_provenance (the exact
operator authority id, decision-record path and publication SHA);
governance_event_id == the protected EVENT_ID; auditor_role_slot ==
AUDITOR_A_REPLACEMENT_1; future_machine_attempt_binding — SYMBOLIC
FUTURE_REPLACEMENT_AUDITOR_A_ATTEMPT_ID everywhere in design text, at
implementation equal to the V2 slot constant exactly, never a caller value;
frozen_target (commit 730d2b29f7c0e7d33af3451b6d9205ec27c143ed, tree
2585796efd5cb6902226cfff785bb901297a15e3 — unchanged, AUDIT SUBJECT / NOT
AUTHORITY); accepted_active_v3 identities (procedure SHA-256
32460cd5011c29efd042e2a4c79f09efabb2662a211f2822410e6ee309f7852e, binding
SHA-256 801279b546ec0c0b590a9d7a3cf9993cb0cbd51c99a84830ee870cac945cae12, as
accepted by the prior readbacks); one_package_only true; execution_authority
constant "NONE" (ANY other value rejected AT PARSE with
GRANT_EXECUTION_AUTHORITY_CLAIM_INVALID — a grant document can never even
textually claim execution capability); secret_material constant "NONE";
forward-only lifecycle MINTED -> BOUND -> FROZEN -> READ_BACK (no RESET, no
backwards transition); expiry_policy NO_EXPIRY (staleness prevented by
exact-identity bindings re-verified live, not clocks). Canonical
serialization: strict JSON, UTF-8, fixed key order, LF, no insignificant
whitespace, closed world. Token identity := SHA-256(canonical bytes) —
deterministic, non-secret, recomputable by any verifier; the grant uniqueness
input is the ordered field tuple, so a duplicate mint self-collides onto the
same digest and the same ledger key and is refused mechanically. Minting:
conceptually by the future bounded implementer session holding an EXPLICIT
operator package-grant minting authority, immediately AFTER the operator
decision authorizing package preparation and BEFORE package construction —
the governance transitions are preserved and NOT collapsed: operator decision
-> package-binding grant mint -> package construction/freeze (+ receipt bind)
-> independent Control Room readback -> only later, a SEPARATELY authorized
single-use execution decision. NOTHING is minted in this session.

One-shot package-binding enforcement (why "this grant may bind exactly one
frozen package for exactly one future attempt" is mechanical, not narrated):
pure content binding (A) alone cannot enforce it; runtime AccountingStore
state (D) is categorically NOT used; the selected mechanism is a durable
NON-RUNTIME append-only receipt ledger (B) — one receipt file per grant
identity, owned by the protected package-preparation authority plane in a
dedicated disjoint namespace (never AccountingStore, never attempt
accounting, never the frozen external event root, never a Git-tracked
operative path), created O_WRONLY | O_CREAT | O_EXCL | O_APPEND | O_NOFOLLOW
mode 0600 with a single canonical record (grant identity, package digest,
role slot, event id, operator authority id, lifecycle BOUND); duplicate or
replay bind -> EEXIST -> DUPLICATE_PACKAGE_BINDING_REFUSED; no update/delete
surface; a rewrite is detectable because the Control Room readback publishes
the receipt hash. Control Room canonical publication uniqueness (C)
corroborates. Mutual binding completes at the receipt (the grant precedes the
package, so it cannot contain the package digest): the package embeds the
grant identity; the receipt binds grant identity <-> package digest; the
verifier recomputes both digests and cross-checks the receipt
(PACKAGE_SUBSTITUTION_REFUSED on mismatch). Verification semantics are
fail-closed with distinct tokens (GRANT_SCHEMA_UNEXPECTED /
GRANT_FIELD_UNKNOWN_OR_MISSING / GRANT_PURPOSE_INVALID / GRANT_EVENT_MISMATCH
/ GRANT_ROLE_SLOT_MISMATCH / GRANT_ATTEMPT_SLOT_MISMATCH /
GRANT_TARGET_MISMATCH / GRANT_ACTIVE_V3_STALE / GRANT_CANONICALIZATION_INVALID
/ GRANT_LIFECYCLE_INVALID / DUPLICATE_PACKAGE_BINDING_REFUSED /
PACKAGE_SUBSTITUTION_REFUSED); the successor-gate identity remains a
FUTURE-LIVE-PREFLIGHT obligation of the attempt-specific package per the
accepted REQUIRED-BINDINGS matrix — the grant never substitutes for it.

## 7. Negative semantics — the grant is NOT execution authority

(1) A grant document textually CANNOT claim execution (constant
execution_authority "NONE"; any other value rejected at parse). (2) The
runtime authority class has NO grant-consuming surface — an AST-verified
property of the current protected source — and this design ADDS none; the
grant is verified by package tooling and the readback, never by
BootstrapAuthority. (3) Grant verification creates NO AccountingStore state,
NO GATES_PASSED, NO CONSUMED_PRE_EXEC, attaches NO credentials, reserves NO
provider/model capacity and counts as NO engagement. (4) A frozen package
plus its package grant remains NON-EXECUTABLE absent a later explicit
single-use operator execution authority. (5) The future execution authority
MAY reference the grant identity and package digest as EVIDENCE but MUST be a
distinct authority event. Therefore PACKAGE_BINDING_GRANT and
ATTEMPT_EXECUTION_AUTHORITY are mechanically disjoint representations
connected only by evidence reference: BootstrapAuthority.run_attempt cannot
be invoked merely because a package grant exists — structurally, not just
by policy.

## 8. Threat model (full T1-T16 table in the external workspace design/THREAT-MODEL.md)

T1 spent A-01 reuse — excluded mechanically (V1 roles not representable in
V2; grammar-disjoint constant; absorbing accounting). T2 arbitrary/free-form
identity injection (incl. attacker-minted ordinal variants such as an
"A-02"-shaped hypothetical) — strict-constant equality refusal. T3 second
event disguised as replacement identity — EVENT_ID equality everywhere; no
other event representable. T4 one identity bound to two package digests —
O_EXCL one-receipt-per-grant + immutable receipt cross-check. T5 grant reused
across two attempt identities — attempt-slot equality. T6 across two roles —
role-slot equality. T7 across two events — event equality. T8 package digest
changed after binding — receipt-vs-recomputed-digest mismatch refusal. T9
stale active-v3 — recorded-vs-live identity equality refusal. T10 stale
successor-gate identity — remains future-live-preflight, grant never
substitutes. T11 historical execution grant reused as package grant — schema
tag + closed world + purpose + provenance parse refusal. T12 grant read as
execution capability — textual claim refusal + structural no-runtime-path +
distinct execution authority event. T13 runtime accounting created during
package binding — grant tooling cannot reach AccountingStore; disjoint ledger
namespace. T14 receipt rewritten — append-only, no update surface, published
receipt hash. T15 duplicate package freeze — receipt existence + digest
equality conflict refusal. T16 publication record replay after supersession
— append-only dated records; the design carries DESIGN_COMPLETED_AS_CANDIDATE
/ NOT_IMPLEMENTED status; fresh readback re-derives hash-bound identities
from live sources. Each row names its preventive invariant, verification
point, fail-closed result and evidence produced.

## 9. Prospective contract-delta map (full map in design/CONTRACT-DELTA-MAP.json; NO PATCH, NO SOURCE FILES)

UNCHANGED: POLICY_ID; EVENT_ID; RESERVED_ATTEMPT_IDS (byte-identical, V1
manifest equality preserved verbatim); ROLES; BINDING_SCHEMA V1; the V1
parse path and every V1 failure token; AUTHORITY_MANIFEST_SCHEMA V1;
AUTHORITY_MANIFEST_KEYS V1; design_event_id check; design_attempt_ids check;
binding transport projection semantics; gate evidence attempt_id; output
identity; accounting_name; accounting.py; statemachine.py; the frozen audit
target. FUTURE_IMPLEMENTATION_CHANGE_REQUIRED (additive only): the V2
binding/manifest schema constants and key set; REPLACEMENT_ATTEMPT_SLOTS;
the V2 strict parse branch; the design_replacement_attempt_ids equality
check; the narrow additive runtime.py verification (admit the parsed V2
binding, check the new manifest equality and, with Problem B, the grant
digest cross-check) — with the BootstrapAuthority public surface UNCHANGED
at exactly {state, store, run_attempt} and NO new capability name; the grant
schema and the NON-RUNTIME receipt ledger. active-v3 procedure/binding:
FUTURE_CONTRACT_UPDATE_REQUIRED_LATER (design-only conceptual update; the
active-v3 bytes are NOT modified now).

## 10. Accounting / state-machine invariants — NO MAJOR TRUST-BOUNDARY CHANGE

The selected design requires NO change to accounting.py or statemachine.py:
the O_EXCL attempt-global claim, initial PREPARED durable state,
GATES_PASSED -> CONSUMED_PRE_EXEC ordering, immediate irreversible execution
after consumption, TERMINAL_PREEXEC_STOP / TERMINAL absorbing semantics, no
reset / retry / resume / attempt-mint surface are all preserved and are
precisely what enforces the replacement attempt's one-shot lifecycle once its
identity exists. The runtime.py delta is narrow additive verification only
and introduces no new public operation, therefore it is NOT a major
trust-boundary change; had the design required accounting or state-machine
changes, it would have been classified a MAJOR TRUST-BOUNDARY CHANGE and
returned for a narrower alternative.

## 11. Historical / compatibility decision

HISTORICAL_V1_SEMANTICS_PRESERVED = TRUE. Historical V1 records and source
identities remain historical truth; the design never claims the spent A-01
identity was part of a multi-attempt registry (the V1 contract at the time
reserved exactly one identity per role, and that meaning is byte-preserved);
no old verdict, package or attempt inherits the future design; a future V2
authority package has its own exact identity (version-tagged schema, slot
constant, grant identity); the spent A-01 accounting record remains immutable
evidence; SECOND_GOVERNANCE_EVENT_REQUIRED = FALSE.

## 12. Auditor-B non-impact

Auditor-B authority remains NONE. RESERVED_ATTEMPT_IDS["AUDITOR_B"] and ROLES
are UNCHANGED; REPLACEMENT_ATTEMPT_SLOTS contains no Auditor-B key; the V2
representation admits ONLY the single Auditor-A replacement slot; no
Auditor-B identity is allocated, no B package authority or state is created,
no B execution semantics are modified for symmetry. The only schema-level
effect on the shared role shape is the role-agnostic V2 manifest key set;
admission is by slot-constant equality, so B's operative authority remains
NONE.

## 13. Active-v3 conceptual integration (DESIGN ONLY — active-v3 NOT modified now)

The minimal future active-v3 update must distinguish four value classes with
no field substitutable for another: (1) FUTURE MACHINE ATTEMPT IDENTITY (the
V2 slot constant, symbolic FUTURE_REPLACEMENT_AUDITOR_A_ATTEMPT_ID); (2)
PACKAGE-BINDING GRANT IDENTITY (grant digest + receipt binding); (3) LATER
EXECUTION-AUTHORITY IDENTITY/STATE (a distinct future operator authority
event, never created by package preparation); (4) PREARM OPERATIONAL
CORRELATION CONTEXT (live session state, never a package value). Bound
before freeze: governance event id; attempt id (the slot constant, once
operative); grant identity + receipt binding; package digest (at freeze);
frozen target identities; accepted active-v3 procedure/binding identities;
the successor-gate identity at its freshest pre-freeze observation.
Remaining FUTURE-LIVE-PREFLIGHT values per the accepted REQUIRED-BINDINGS
matrix: then-live gate identity including then-current ctime, domain
identity/XML digest, guest-runner identity/bytes, QGA mechanism/topology,
downstream interpreter identity, exact downstream argv, frozen runtime
identity, canonical runtime root state, operational correlation context
value, and PREARM live session/readiness state.

## 14. Future implementation acceptance criteria (DEFINED, NOT EXECUTED)

The 24-row matrix AC-01..AC-24 and the add/modify/do-not-weaken test
identification live in the external workspace
design/IMPLEMENTATION-ACCEPTANCE-CRITERIA.md. Highlights a later
implementation MUST prove: historical V1 exact semantics preserved; the
replacement identity accepted only under the exact V2 contract; the spent
A-01 still cannot become a replacement; arbitrary ids rejected; the same
governance EVENT_ID retained with no second event; grant exact-schema
parsing with malformed/unknown fields rejected; cross-event / cross-role /
cross-attempt grants rejected; replay/duplicate binding and package
substitution rejected; stale active-v3 rejected; the grant cannot invoke
run_attempt and creates no AccountingStore state; the runtime public surface
unchanged with no split authority surface; one-shot/no-retry preserved;
Auditor-B NONE preserved; the frozen target unchanged; accounting.py and
statemachine.py unchanged. NO test is run in this session.

## 15. Required design decision (exact; also in design/DESIGN-DECISION.json)

IDENTITY_PROTOCOL_DESIGN = ADDITIVE_VERSIONED_V2_SINGLE_SLOT_REPLACEMENT_CONTRACT
PACKAGE_GRANT_PROTOCOL_DESIGN = CANONICAL_CONTENT_ADDRESSED_NON_EXECUTION_PACKAGE_GRANT_WITH_APPEND_ONLY_NON_RUNTIME_BINDING_RECEIPT
HISTORICAL_V1_SEMANTICS_PRESERVED = TRUE
SECOND_GOVERNANCE_EVENT_REQUIRED = FALSE
RUNTIME_MINT_API_REQUIRED = FALSE
RUNTIME_ACCOUNTING_CHANGE_REQUIRED = FALSE
STATE_MACHINE_CHANGE_REQUIRED = FALSE
PACKAGE_GRANT_CONFERS_EXECUTION_AUTHORITY = FALSE
FUTURE_IMPLEMENTATION_CAN_BE_NARROWLY_SCOPED = TRUE

No operator constraint is violated; DESIGN_INCOMPATIBLE_WITH_HELD_INVARIANTS
was NOT triggered (none of the Section 28 stop conditions is required for
coherence).

## 16. Zero-implementation / zero-runtime census (all-zero)

Protected-source modifications 0; bootstrap-authority imports 0;
BootstrapAuthority constructions 0; run_attempt calls 0; attempt-id
creation/reservation/allocation 0; authority-token minting 0;
package-grant minting 0; package completion/freeze 0; AccountingStore
create/create_at 0; attempt accounting 0; attempt directories 0; report
sinks 0; successor execution 0; permission transition/chmod 0;
wrapper/driver execution 0; real PREARM sessions 0; credential access
(incl. metadata) 0; credential-channel connection/probe 0; VM start/reopen
0; virsh 0; QGA 0; guest-runner execution 0; provider/model calls 0; Claude
0; Codex 0; /audit-council 0; Auditor-B execution or authority 0. The only
executions this session: ordinary Git/GitHub publication mechanics and local
data-only python text/hash/AST tooling on non-secret bytes. Permitted-only
actions used: live Git/GitHub read-only verification; data-only source
inspection (blob reads + ast.parse; the modules were NEVER imported or
executed); static text analysis; design documents with symbolic placeholders
only; docs-only publication.

## 17. Honest session iteration without erasure (instrument-side ONLY; every first output preserved under the external evidence workspace)

Bootstrap instrument run-001-defective (the tracked-cleanliness gate did not
allow the two PRE-EXISTING smoke-fixture gitlink drift rows), run-002-defective
(the output normalization stripped the leading status-space of the first
porcelain line, misreading " M smoke-fixture" as "M smoke-fixture") before
run-003 FINAL ALL-PASS on identical repository state. Source-identity
instrument run-001 FINAL (first output; all facts derived on first run).
Rotation-builder and precommit-battery iterations are recorded verbatim in
the external evidence workspace evidence/honest-iteration-ledger.md and the
generated-LAST handoff. NO failed observation was rewritten as PASS without
a corrected re-derivation on IDENTICAL bytes/state; no subject bytes were
mutated by any defective instrument run.

## 18. Finding status (NOT CLOSED)

PKGIDENT-001 = OPEN / BLOCKING_IMPLEMENTATION / DESIGN_CANDIDATE_AVAILABLE / NOT_CLOSED
PKGIDENT-002 = OPEN / BLOCKING_IMPLEMENTATION / DESIGN_CANDIDATE_AVAILABLE / NOT_CLOSED

Only independently reviewed implementation evidence may support future
closure; this design session closes nothing.

## 19. External design workspace (NON-AUTHORITY; NOT Git-tracked)

/home/isa/aucdev023-pch6b-replacement-auditor-a-authority-protocol-design-20261006-01/
with design/ and evidence/ and instruments/ and per-run evidence subdirectories.
Key artifact SHA-256 identities: AUTHORITY-PROTOCOL-DESIGN.md
735831d56be31c0cf2b55c81f49cafd1dbd2f17b38800e071d4626d576614780;
IDENTITY-CONTRACT-DESIGN.md
42ad71fa4b08df1bcec82c6003318860b023a86e8be17ca953bc7c400c4ef581;
PACKAGE-GRANT-PROTOCOL-DESIGN.md
a5f37f257016e959620311457385dc7e921514ddbe03cd026cf2e3bcf49b2583;
THREAT-MODEL.md a3c1f90c1962135cbbabf8d8b2f5ee89980d1a9fa1264b1e980301f2ac1da10c;
CONTRACT-DELTA-MAP.json
ee6aa758b15da7053e6dc524377dd2a37a5e450e8cc1f1cc2b22b7ef1fc33874;
DESIGN-DECISION.json
28369aba2df86d71a60ca4de65cf501c88b18b96d16bbb53dfe84fc5997cc542;
IMPLEMENTATION-ACCEPTANCE-CRITERIA.md
60e9f63d055852338887c7557339625e865f92445ea05f36fffa5d013396d8a5;
live-source-identities.json
ed171423e4f2d004af6e2d3974e7a0d11fa56488a13faf7eef1782c19d8f917b;
source-constraint-excerpts.txt
9291e39390865be208667850a536b59aaee2cfcdb24737b53f5754bbe543bdd7;
option-analysis.json
95481c911bff2ff3156548b05d18610085519214baf779a87cd31882aaef5614;
held-invariants.json
40230c20e1b9b58a7e219e2197754e7e0410164da225a2383b2d642746181564.
Every design artifact carries DESIGN_ONLY / NON_AUTHORITY /
NO_ATTEMPT_ID_CREATED / NO_AUTHORITY_TOKEN_MINTED / NO_EXECUTION_AUTHORITY /
NO_IMPLEMENTATION_AUTHORITY / NOT_VALID_FOR_INVOCATION. No design workspace
file, schema example or instrument is Git-tracked; all examples contain
symbolic placeholders only; the generated-LAST handoff is created after
commit/push.

## 20. NEXT — EXACTLY ONE, GRANTS NOTHING

INDEPENDENT CONTROL ROOM READBACK OF THE EXACT AUTHORITY-PROTOCOL DESIGN
CANDIDATE FOR PKGIDENT-001 AND PKGIDENT-002, INCLUDING THE SELECTED
REPLACEMENT-IDENTITY REPRESENTATION, HISTORICAL-V1 COMPATIBILITY MODEL,
CANONICAL NON-EXECUTION PACKAGE-GRANT SCHEMA AND LIFECYCLE, ONE-SHOT /
REPLAY ENFORCEMENT, EXECUTION-AUTHORITY SEPARATION, CONTRACT-DELTA MAP,
THREAT MODEL AND FUTURE IMPLEMENTATION ACCEPTANCE CRITERIA, BEFORE ANY
PROTECTED-SOURCE REMEDIATION, ATTEMPT IDENTITY CREATION, AUTHORITY-TOKEN
MINTING, PACKAGE COMPLETION OR EXECUTION-AUTHORITY DECISION IS
CONSIDERED.

Recording this NEXT grants NOTHING.

## 21. Standing prohibitions (unchanged house rules)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain from an
agent session absent an explicit single-use operator attempt authority (and
even then at most the ONE authorized call, never a second); never rerun the
launcher; never treat any recorded grant phrase (including any phrase
recorded here) as a new grant; never execute a real auditor or
provider/model; never open, read, hash, log, persist or stat any real
credential byte; never open the four historical sealed artifacts
(identity-only forever); never relabel or rewrite historical model
identities, runs, records, matrices, prompts or evidence workspaces
(append-only); never claim audit PASS, qualification, installation or any
authority from this publication — it grants none; never rewrite, repack,
replace or delete a historical subject archive and never publish a corrected
archive under a historical archive's filename; never repack any historical
generated-LAST handoff archive; never edit the accepted v2 remediation
source or the accepted PREARM/sender bytes; never chmod the now-mode-0500
activated authoritative object (or the historical 0600 candidate) absent
separate operator authority after independent Control Room readback — both
single-use activation transitions have been SPENT and performed, and NO
further permission transition (including any de-activation or re-transition)
is authorized by this publication; never use root to defeat the
activated-state DAC boundary; never use a TEST-ONLY context for any future
real launch; never mutate the canonical runtime root or restage the event
host after event instantiation absent a separate explicit operator
remediation authority; never rewrite or repack the frozen external event
root; never delete or repurpose the rehearsal-derived artifacts under
/srv/frevp/; never start or reopen the event-host VM or connect to the
candidate credential channel from a preparation, design or record-only
session; and never run privileged mount/pivot_root/umount experiments on the
operator's live host and never automatically re-run an interrupted privileged
command — privileged GATE-W-prime boundary work belongs in the
disposable-KVM environment.
