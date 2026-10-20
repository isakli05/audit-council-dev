# AUCDEV-023 replacement Auditor-A package-binding authority

Publication condition: these exact bytes require a separate explicit operator
G5 publication decision under proposed ID
`AUCDEV-023-G5-PUB-AUDITOR-A-R1-20261020-01` and one canonical raw-ADD
publication at
`docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-AUDITOR-A-PACKAGE-BINDING-AUTHORITY.md`.
The publishing Control Room must retain the actual operator decision in the
campaign record. This condition does not assert that approval has occurred.
An external candidate copy has no operative authority. No own future commit,
root tree, blob identity or digest is asserted here.

## Scope and authority

| Field | Value |
|---|---|
| existing_governance_event_id | `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01` |
| auditor_role | `AUDITOR_A` |
| attempt_slot | `AUDITOR_A_REPLACEMENT_1` |
| protected_replacement_attempt_id | `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-R1` |
| operator_authority_id | `AUCDEV-023-G4-PBONLY-AUDITOR-A-R1-20261014-01` |
| scope | `PACKAGE_BINDING_ONLY` |
| package_binding_permitted | `TRUE` |
| grant_mint_permitted | `TRUE` |
| execution_authority | `NONE` |
| credential_authority | `NONE` |
| auditor_b_authority | `NONE` |

The replacement attempt value is referenced verbatim from the G2-protected
binding constants; this record allocates no attempt or accounting state.
The G4 authority ID above is the mint-time V11 value; it is distinct from the
separate proposed G5 publication authority ID. `grant_mint_permitted = TRUE`
is the conditional G4/G5 decision-layer declaration, never immediate mint
authority: favorable independent G6, all V1-V35 checks and a separate explicit
G7 operator mint decision must precede any mint. No grant, mint evidence,
package, receipt, credential access or execution follows from G5 alone.

## Exact existing G2 prerequisite (eight fields)

| Field | Value |
|---|---|
| protected_v2_implementation_commit_sha | `07f8cdddb34fb37503e524e46f4cb23bf3f26d4c` |
| protected_v2_implementation_root_tree | `f498d2fcc188febfb0e7b87d569fbf36cbf07c24` |
| protected_v2_implementation_record_path | `docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-AUDITOR-A-AUTHORITY-PROTOCOL-RECEIPTIMMUT-001-IMPLEMENTATION-REMEDIATION-001.md` |
| protected_v2_implementation_record_blob_sha1 | `563985e45770d5a00bd5a76697201c981d913403` |
| protected_v2_implementation_record_sha256 | `2c358ccc81f12139848dc6621bde3fdea95f409f6838dd3474c44c755946cea2` |
| protected_v2_source_tree_identity | `795dc0ee1436cd42ef678971ea5d850f689587cb` |
| protected_v2_binding_source_blob_sha1 | `eb2301812b53f91e49805bf4bac2f47dd87d46c9` |
| protected_v2_runtime_source_blob_sha1 | `d5e353ef4ada0c176af7cc96eb65290cab943037` |

## Exact existing G3 prerequisite (seven fields)

| Field | Value |
|---|---|
| protected_v2_readback_commit_sha | `4492dde092178a1ffa6fcc355ade40d418265830` |
| protected_v2_readback_record_path | `docs/chatgpt-project/AUCDEV-023-PCH6B-G3-FRESH-07F8CDD-IMPLEMENTATION-READBACK-PUBLICATION-20261013-01.md` |
| protected_v2_readback_record_blob_sha1 | `c99da2118a5b12a08b1535a587a33169a3d3e70b` |
| protected_v2_readback_record_sha256 | `cab8620bd1b6c6c4862d9f2074baa77165b3d4a97fed901714b7d5c0b2f63eb2` |
| protected_v2_readback_target_commit_sha | `07f8cdddb34fb37503e524e46f4cb23bf3f26d4c` |
| protected_v2_readback_disposition | `G3_IMPLEMENTATION_READBACK_PERMIT_CONSIDERATION` |
| package_binding_consideration_permitted | `TRUE` |

The G3 reviewed target equals the G2 implementation commit by value.
G3 permits only consideration of G4; the G4 decision is separately recorded.

## Exact existing G4 decision and design prerequisites

G4 decision identity:

| Field | Value |
|---|---|
| commit | `14678a6a0103428c194774510c5346335c595e29` |
| root_tree | `0f9e2a6c3ad1ffc24b0d09a37cf360a85832b3ee` |
| record_path | `docs/chatgpt-project/AUCDEV-023-PCH6B-G4-PACKAGE-BINDING-OPERATOR-DECISION-20261014-01.md` |
| record_blob_sha1 | `7d76cf9e82b4cbafe10da8ce37f220b39f7021f0` |
| record_sha256 | `decf72f667ac753a555252933a996c9dcf14f0d590aa5c52f89a3a6604e937c0` |

G0 order-correction readback identity (accepted direction with its historical
G6 residual preserved):

| Field | Value |
|---|---|
| commit | `ac5b20b5b3a9b6b72128366580bd0ba1b342782e` |
| root_tree | `75f6ea85bd962ef3c9250d59fde2011ddc82f397` |
| record_path | `docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-AUDITOR-A-AUTHORITY-PROTOCOL-DESIGN-REMEDIATION-AUTHDESIGN-003-ORDER-CORRECTION-CONTROL-ROOM-READBACK.md` |
| record_blob_sha1 | `e884fee765f7ee295cd185eb2d6e5360dda487f0` |
| record_sha256 | `6e02a38f102d667a3b984ec65fe1ba2d0e08d7de3e61aaad7a2c51960cc9e8ba` |

Subsequent accepted design-closure readback for AUTHDESIGN-003 and its nested
G6/EVIDENCE/PUBID/DIFFSEM residuals (design closure only):

| Field | Value |
|---|---|
| commit | `c8ffd8b1be008dd0e8ddc2aafb509a39d7af150f` |
| root_tree | `253049fa948312a363f98c401e31bbc61492e4da` |
| record_path | `docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-AUDITOR-A-AUTHORITY-PROTOCOL-DESIGN-REMEDIATION-AUTHDESIGN-003-G6-001-EVIDENCE-001-PUBID-001-DIFFSEM-001-CONTROL-ROOM-READBACK.md` |
| record_blob_sha1 | `0241512a25a04f77aeb11e7f566845506314536c` |
| record_sha256 | `f351503371382b672ed7b269073c2d0db1d483f243af2ee6104dd7dde3dbc655` |

G5 content follows the accepted prerequisite contract (SHA-256
`ad064b95755440f48ac6d7f0e49c79e2006c6d72cd48cde63cb6914021583dc4`).
Option A remains the governing P3 design: G5 identity derivation alone proves
no content/provenance verification; G6 must substantively review these bytes,
and G7 must mechanically verify V1-V35. Optional B2 remains deferred; no G5
closed-world schema or parser is adopted here.

## One-shot scope and fail-closed conditions

Exactly one G5 publication lineage and its corresponding grant/package/receipt
lifecycle within the existing event and replacement slot. No second event,
second replacement identity, spent A-01 reuse or additional lineage.
All exact prerequisites must remain reachable and unchanged on authoritative
master; later development HEAD is never substituted for any prerequisite.
R1-R8 apply: superseding G2; protected-source drift after G3; G3/G2 target
mismatch; conflicting G5 prerequisite lineage; modified published records;
unreachable prerequisites; a superseded-prerequisite grant; exhausted stage
authority each refuses the affected transition. R1/R2/R4/R8 exhaust authority
as prescribed by the accepted contract. No delete/re-add, amendment, retry,
rebind or supersession bypasses exact-one introduction or stale-target rules.
G5, G6 and G7 remain separate ordered publications; no favorable G6 result is
predetermined. G7's immutable grant must bind the actual published G5
commit/path/blob/SHA-256 and thereby the G2/G3 sets above, never future IDs.

## Preserved findings and evidence limits

G4 provenance remains source-attributed: the complete primary operator
submission was not independently examined, its disclosed affirmative-clause /
stale-draft-marker contradiction remains preserved and unresolved, external
uniqueness claims are only partially reproduced, and Git cannot prove zero
external runtime activity. No unconditional provenance PASS is asserted.
This record does not rewrite or strengthen the G4 decision/readback.

PKGIDENT-001 and PKGIDENT-002 remain OPEN; RECEIPTIMMUT-001 remains
readback-supported / NOT OPERATIVELY CLOSED; RECEIPTCTX-001 PARTIALLY
REMEDIATED; TRUSTROOT-001 NOT OPERATIVELY CLOSED; CR-P3-G5-001 OPEN /
CONTRACT-DEPENDENT. G7 record serialization residual, parse-as-filter
boundary, G11 verification of genuine original GRANT_ISSUED evidence, and
3577/900/4477 LOC ceilings are retained. No finding is closed by G5.
AUCDEV-023 remains P1 / READY / NOT DONE; installed source remains
`8ae33444f349ce73c1359b963722e2d16acba630`, with qualification provenance
NOT ESTABLISHED. This record is no independent audit verdict, qualification,
installation authorization or G12 execution decision.
