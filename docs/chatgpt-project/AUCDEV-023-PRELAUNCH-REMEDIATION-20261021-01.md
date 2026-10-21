# AUCDEV-023 prelaunch remediation — final preparation / Control Room integration record (2026-10-21, nonsecret)

One concise dated record of the completed prelaunch technical preparation in
workspace `/home/isa/aucdev023-prelaunch-remediation-20261021-01` and its
final Control Room integration review. This is NOT a new campaign or stage
publication; the G5–G12 governance sequence remains recorded in
[AUCDEV-023-CODEX-G5-G12-CAMPAIGN-20261020-01.md](AUCDEV-023-CODEX-G5-G12-CAMPAIGN-20261020-01.md).
Recorder: GLM-5.3 bounded documentation/state implementer, final nonsecret
task only; Codex Control Room owns review and Git publication. Grants
nothing.

## Precondition verification (actual, at recording time 2026-10-21)

- Final Control Room assessment present:
  `/home/isa/aucdev023-prelaunch-remediation-20261021-01/CONTROL-ROOM-ASSESSMENT.json`
  — SHA-256 `fe601b15c0718f8c9ce7885da61e1f4d43c1eabfb7f0e4287b406879f8b1aa80`,
  11600 bytes, disposition
  `TECHNICAL_PREPARATION_COMPLETE_LIVE_ADMISSION_AND_CREDENTIAL_AUTHORITY_PENDING`
  at verified checkpoint `b2872137d5597ec95136ce1a6ffca3fdc9cd342d` (==
  live local HEAD re-resolved here).
- All 8 assessed source targets and all 6 assessed result JSONs were re-hashed
  by this session EXACT to the assessment pins (table below) — no drift, no
  substitution. All five protected trees and the immutable
  grant/evidence/package/receipt/G12 bytes were verified UNCHANGED by the
  Control Room at 2026-10-21T09:55:47Z; the G7 campaign record and all other
  existing reports/results remain byte-untouched by this task.

## Four-row exact disposition (from the final assessment — preparation vs then-live explicitly separated)

| # | Blocker | Disposition | Strength (exact) |
|---|---|---|---|
| 1 | `1_launcher_identity_timing` | CLOSED | `PREPARATION_SOURCE_REVIEW_AND_SYNTHETIC_MECHANICS` — exact reviewed downstream launcher selected; external runtime binding permitted by active-v3/G12 over the unchanged NON_RUNTIME_STATIC_G9_ONLY package; sealed executed bytes cannot be substituted by path replacement. Fresh source/metadata binding still due at actual use. |
| 2 | `2_active_v3_admission` | CLOSED | `IMPLEMENTATION_AND_SYNTHETIC_INTEGRATION_ONLY` — callable single-use trusted intake, R1 cross-binding, context-bound PREARM session, derived argv, enforced seam fd, strict 20-key contract, final 0500/uid1000/nlink1 check, sealed interpreter/script/contract fd handoff. NO actual live admission or execution occurred. |
| 3 | `3_live_preflight_prearm` | READY_FOR_THEN_LIVE_CHECK | `STATIC_A_AND_SAFE_SYNTHETIC_B_COMPLETE_C_NOT_PERFORMED` — fail-closed admission path exercised only with accepted gate COPY, reviewed launcher and inert ELF; ALL class-C conditions must be re-verified then-live in a future separately authorized boundary run, otherwise STOP. |
| 4 | `4_credential_authority` | PENDING_OPERATOR | `NO_CREDENTIAL_AUTHORITY_ISSUED` — channel-v2 mechanics/sender source reconciled with limited historical synthetic-verification strength; G12 grants no credential authority; separate operator decision required (request prepared below, NOT authority). |

Rows 1–2 are preparation-layer implementation/synthetic review strengths
only; no row asserts then-live admission. Codex primary plus a separate
read-only Codex review found no material remaining adapter/handoff gap on the
exact `4702…`/`aae4…` target; same model-family review, not a
qualified-auditor verdict.

## Actual source / test / evidence identities (exact; counts are this preparation's own)

| Artifact | SHA-256 | Size | Result (pass/fail/skip) |
|---|---|---|---|
| preparation.py | `0de4280063267bdc530710189dcbf06388cf0bb38a6d459e992a48074dfbbfb8` | 40494 | — |
| test_preparation.py | `3e96c7b35e2aeae338da566c24919383e04b68eb1f18dc9f1bb7be34ef2ed2fd` | 56455 | — |
| launcher-candidate/launcher_r1.py | `076cab42b8539c831b8839938078a44fd3fa4bb23205b7ca40efb7d6be95a19a` | 3716 | — |
| launcher-candidate/prepare_integration_r1.py | `63602a80575ccc040136ec86b605a5e83b2d97c8e46467f29992caae6281db34` | 45506 | — |
| launcher-candidate/test_candidate.py | `e5cec99b1a8d57f0bb7c5b9d67b65b5ddbe0788c2f8ee7e64dd8a1db44a6d522` | 38039 | — |
| launcher-candidate/fixtures/src/inert_surrogate_seam_v1.c | `939ebe7f9969840f83d58054b86632494e454e417e85c2f89ad548bab3ece4e9` | 2770 | — |
| section-a/section_a_adapter.py | `4702daaca5308513755a19e69c3030a1df20e0a0e8df4414fa336e85b93a6b7a` | 75677 | — |
| section-a/test_section_a.py | `aae40fc0c7b1d88a82383f680676efa5ba46ad8190e6bba06de9eda67754b68c` | 97428 | — |
| root I/O predecessor run | `eb7302ab56ecf1fcd67ffb9f545eb3d775d4c4a86932f33c813c4768ff40e214` | 5339 | 14/0/0 |
| root marker current run | `5eaa093e488361b8432558f4d4f31c49e3906e6c75959d1ba53187073ceb551e` | 1597 | 3/0/0 |
| builder current run | `62964330d213210ab0a335516f4f3247a3a642a0647fb7b9f47c0395138601d8` | 6859 | 23/0/0 |
| section-a v2 predecessor run | `6f1d4b40946984f2694581a284e64c8778c7c28e89f830ff4d6a3349f6514020` | 13942 | 73/0/0 |
| section-a v2.1 predecessor run | `800aab45790e0a2616a40a2ce5f02778a89af1d63c6943a73576d48cd759c963` | 5557 | 7/0/0 |
| section-a v2.2 CURRENT run | `ddc6fc86c34458338931f1e49bf22dda34023e5ed61cd68fe0f42c1693781834` | 4676 | 4/0/0 |

Lineage (exact, no verdict inheritance across changed bytes): the CURRENT
adapter `4702daac…`/test `aae40fc0…` has the 4 focused v2.2 cases
(ddc6fc86…, 4/0/0, exit 0). The prior 7/0/0 belongs to the v2.1 adapter
`9eb4ae84…` (result 800aab45…); the prior 73/0/0 belongs to the OLD frozen
v2 adapter `6e6d…` (result 6f1d4b40…, preserved under
`section-a/history/v2/` and NOT rerun). No assertion is made anywhere that
the current target passed 73; frozen-source suites were not redundantly
rerun.

## Launcher, host seam, accepted IDs, immutables (role separation explicit)

- Reviewed downstream launcher (preparation artifact):
  `launcher-candidate/launcher_r1.py` — SHA-256 `076cab42…5a19a`, 3716 B,
  `regular_non_symlink`, mode `0500`, uid 1000, nlink 1 (dev 54, ino
  34600632, ctime_ns 1792569379143005037).
- Host launch seam (external trusted host tool, NOT this workspace's code):
  `/usr/bin/virsh` — SHA-256 `525c340f463c64efc5abe6e2bf2406d1daf3b9f1c718a54e9d181e8690bf0334`,
  976608 B, mode `0755`, uid 0, nlink 1, `ELF64_ET_DYN`, observed read-only
  and sealed in synthetic tests and NEVER EXECUTED; identity must be
  re-verified at real use.
- Accepted identities verified ACTUAL by the Control Room (must be
  re-verified at use): gate `prelaunch_prearm_gate_opadopt_v1.py`
  SHA-256 `410b141054c347f42422e402dde22a966f608adf1f83605eab539656d29cebf4`
  (mode 0500/uid 1000/nlink 1, 20535 B); active-v3 procedure
  `32460cd5011c29efd042e2a4c79f09efabb2662a211f2822410e6ee309f7852e`;
  binding `801279b546ec0c0b590a9d7a3cf9993cb0cbd51c99a84830ee870cac945cae12`.
- Immutable and UNCHANGED (verified 2026-10-21T09:55:47Z): grant identity
  `b4c8fb7c41af4fedf51108ac75056c6dd12cdcd5649e3d36e9dd7e758191cbde`;
  genuine GRANT_ISSUED `83cc20a32fb0e1a7b2e7b171c25b760c9d39926697c07258a2d0f2e2ba072780`;
  package `f5dbde97148cf585aa4d13da4235471c61166e2f36bc877c52b99aeaca6138e2`
  (593920 B); receipt
  `8a72b50bae5f59e9e8ef1e5128e167f7aa92afe564e925cdd16069e9fa4d4482`;
  G12 conditional decision record at `b2872137d5597ec95136ce1a6ffca3fdc9cd342d`;
  five protected trees UNCHANGED.
- Boundary legality, as accepted: the launcher/adapter relationship is an
  EXTERNAL runtime binding OUTSIDE the frozen G9 static package, which is
  exactly what accepted active-v3/G12 permit over the unchanged
  NON_RUNTIME_STATIC_G9_ONLY package. The OLD G11 static-only verdict
  authenticates ONLY the unchanged frozen G9 bytes/receipt and does NOT
  authenticate the new outside code; that code carries its own exact
  preparation review (table above) and still requires all class-C then-live
  checks.

## Trusted observer CALLER boundary (explicit)

The callable injected-observer interface is COMPLETE and TESTED at
preparation strength (per-item fresh single invocation, shape enforcement,
refusal semantics; full recipe preserved in the workspace checklist). The
PHYSICAL collection, fidelity, freshness and actual values of every live
fact (live domain XML, guest-runner bytes, QGA topology/readiness, runtime
root, PREARM session) are then-live CONTROLLER duties at the authorized
boundary; no historical or synthetic PASS substitutes for them. Accepted
active-v3 mandates fresh then-live observations and does NOT mandate a
physical collector backend inside this artifact: the missing physical
observations are a proper EXTERNAL caller dependency, not missing adapter
code — and that dependency is not waived either; without the authorized
caller's real observations the boundary refuses (real mode never falls back
to synthetic values).

## Retained failure/correction ledger and LOST observation (concise)

- Original pre-freeze successor observation document: LOST (G9 freeze-facts
  serialization TypeError; worker return never emitted). Preserved as LOST —
  truthful post-artifact/pre-Git-pin recovery does NOT reconstruct or erase
  the historical freshness limit. G12 condition 4 acknowledged it; it stays
  open.
- This preparation's corrected defects (all disclosed in place; originals in
  workspace `history/` and dated result reports): initial unsupported
  placement claims and count errors (contract key count 18→20); unsafe
  IO/fd placeholders; unbound correlation/path-reopen gap (closed by
  observed-then-bound sealed-memfd binding, v2.1); final-observation
  source-class gap (closed by the v2.2 mode+uid+nlink final guard; the
  RED→GREEN negatives were a metadata-only mocked foreign uid and a real
  hardlink on an inert gate COPY — never an actual foreign-owned gate);
  launcher/builder guard
  corrections and IO read-scope guards. Historical G8 synthetic-marker scope
  incident and G9/G10 failures remain recorded in the campaign doc; no
  historical favorable rewrite, no invented evidence.

## Actual status (no authority, no qualification claim)

- `actual_execution` NOT_OCCURRED; `credential_authority` NONE;
  `auditor_b_authority` NONE; REAL/OPERATIVE VM/QGA/virsh/channel/marker
  operations 0 (synthetic fixtures and negative marker test cases existed in
  the batteries and are excluded from this count).
- Installed/source unchanged: installed source
  `8ae33444f349ce73c1359b963722e2d16acba630`; installed qualification
  provenance NOT_ESTABLISHED; qualification/installation change FALSE.
- AUCDEV-023: **P1 / READY / NOT DONE**. Not a release qualification, not an
  audit verdict, not installation acceptance.

## Credential decision REQUEST prepared (STILL NOT AUTHORITY)

Per the assessment (`AUTHORIZED_TO_PREPARE_ONLY_NOW_NOT_YET_ISSUED_AUTHORITY`)
one minimal canonical operator decision request is prepared:

- Path: `docs/chatgpt-project/AUCDEV-023-AUDITOR-A-R1-CREDENTIAL-AUTHORITY-REQUEST-20261021-01.json`
- Proposed credential authority ID:
  `AUCDEV-023-CRED-DELIVERY-AUDITOR-A-R1-20261021-01`
- Canonical bytes: SHA-256
  `014eda5dad2a89bc3a11ad420cbfeee6ff53ec4fc01931a8962bbce54c4a0b68`,
  8882 bytes (hash computed over the exact corrected file bytes — draft-1
  bytes `2e252654…`/8503 preserved under workspace
  `history/CREDENTIAL-AUTHORITY-REQUEST-20261021-01-draft1-superseded.json`;
  the request itself deliberately contains no self-hash field; the operator
  confirms the SHA supplied externally with the request). No duplicate copy
  exists.
- Status `PENDING_OPERATOR_NO_AUTHORITY_ISSUED`, `operator_decision: null`.
  Sole permitted operation if approved: operator-controlled
  credential-channel-v2 delivery only — ONE OPERATOR_SEND_NOW for ONE fresh
  R1-bound PREARM session, then ONE host AF_UNIX connect + single FRAMED_V2
  transfer via the accepted waiter `b0ec4e7e…` + sender `1cc6e22e…` + bridge
  `93bb97b7…` path (payload 1..65536 B; no retry/reprobe/second connect; a
  failed first connect still consumes the one-connect budget; ≤600 s waiter
  limit proposed as an explicit authority-scope initiation window only; old
  SPENT Auditor-A channel state never recycled). Custody stays entirely with
  the operator; no credential-path/content field exists in the request;
  credential-copy prohibition covers additional/persistent/out-of-path
  copies only — the transient memory/pipe/framing flow strictly necessary
  for the ONE approved transfer along the accepted operator → waiter/sender
  → bridge → driver custody path is the sole excepted flow, and the
  operator's original credential source stays operator-controlled (agents
  never open/stat/read/hash/log it).
  Historical provenance of the accepted channel mechanics: publication
  commit `2eab6deaaf2eef26fb748381795852c4e0830d5e` —
  [AUCDEV-023-PCH6-B-PATH-B-CREDENTIAL-CHANNEL-V2-CLEAN-VERIFICATION-REPORT.md](AUCDEV-023-PCH6-B-PATH-B-CREDENTIAL-CHANNEL-V2-CLEAN-VERIFICATION-REPORT.md)
  with its accepted limited Control Room readback
  [AUCDEV-023-PCH6-B-PATH-B-CREDENTIAL-CHANNEL-V2-CLEAN-VERIFICATION-CONTROL-ROOM-READBACK.md](AUCDEV-023-PCH6-B-PATH-B-CREDENTIAL-CHANNEL-V2-CLEAN-VERIFICATION-CONTROL-ROOM-READBACK.md);
  those carry limited SYNTHETIC mechanics strength only and establish NO
  actual credential readiness.
- Remaining actual decision: the OPERATOR's
  `APPROVE_CONDITIONAL_ONE_SHOT_CREDENTIAL_DELIVERY` or `WITHHOLD` reply on
  the exact request SHA and ID. Approval would enable only that conditional
  credential operation inside a future legitimately authorized, live-admitted
  chain; it does not start execution, manufacture readiness, or waive any
  separate VM/runtime/execution authority, G12 condition or class-C check.

Workspace checklist updated to this final truth (prior dated copy preserved
under `history/EXECUTION-BOUNDARY-CHECKLIST-20261021-prefinal.md`). No
archive created here; Codex reviews, publishes, and generates the final
archive last.
