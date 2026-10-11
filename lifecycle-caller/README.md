# AUCDEV-023 PCH6-B Path-B — TRUSTROOT-001 authenticated lifecycle caller (P3)

`lifecycle_caller.py` is the P3 NON-RUNTIME authenticated lifecycle caller
for the AUCDEV-023 Path-B replacement Auditor-A authority protocol. It is
an IMPLEMENTATION CANDIDATE (post-remediation R1a+R2..R7 over the CR-P3
readback findings) implementing the accepted design-layer contracts
(records `8b31d8e5...` and `8bf12dea...`, Control Room dispositions
`86f4e7c0...` and `bed8f50f...`) and it GRANTS NOTHING: it creates no
grant, no GRANT_ISSUED evidence, no G5/G6/G7/G10/G11 publication, no
receipt and no package, and performs no operative lifecycle action.

## What it does

- **Trust root T1-T8 (GAP B)** — loads an operator-held configuration
  (`AUCDEV-023-LIFECYCLE-CALLER-TRUST-ROOT-CONFIG-V1`) from OUTSIDE the
  repository under verification, resolves the authoritative tip at the
  exact configured URL (`git ls-remote --symref`, HTTPS, redirects
  refused), requires the remote-answered default branch, corroborates
  identity through the mandatory public GitHub API channel
  (`full_name` + stable numeric repository id + `default_branch` + tip;
  ANY disagreement refused), checks local-history correspondence with the
  trust anchor as CORROBORATION ONLY, re-resolves the tip immediately
  before binding, and returns the closed-world invocation evidence whose
  exact tip is the single history domain for all later selection.
- **G6 provenance (GAP A)** — the closed-world 15-field Layer-1 parser
  with byte-canonical serialization, the K1-K14 canonical historical
  selector over the SHARED `_qualifying_introductions` core (reused from
  `bootstrap_authority.receiptidentity` under the GAP-D rebind), the
  independently re-derived G5 targets (K9, with stale refusal), and the
  eight Layer-2 identities at their exact implemented names. NO real
  favorable G6 record exists; real-repository evaluation fails closed.
- **G5 limitation disclosure (R1a)** — the caller derives the canonical
  G5 GIT identity only (`G5_GIT_IDENTITY_DERIVED`); it explicitly
  records `G5_CONTENT_VERIFICATION_NOT_ESTABLISHED` and
  `UPSTREAM_V1_V17_NOT_VERIFIED` (non-authority statuses) — G5 content
  and upstream provenance verification remain assigned to the future G7
  mint-time verifier (V1-V17). No G5 content parser exists here.
- **GRANT_ISSUED evidence (R-EVID complete with R2)** — re-selects the
  canonical G7 mint publication with the INDEPENDENTLY derived G6
  identity set, enforces the deterministic evidence path under the
  held-dirfd discipline, verifies the original bytes against the pinned
  digest and size, and validates the accepted 18-field closed-world
  `AUCDEV-023-GRANT-ISSUED-EVIDENCE-V1` document (exact literals,
  canonical byte serialization with exactly one trailing LF, duplicate
  keys and self-digest fields refused) cross-bound to the canonical G7
  record and the independently derived G6 values.
- **Handoff content identity (GAP C + R4)** — SINGLE_CREATION /
  CONTENT_IDENTITY_PINNED / TAMPER_EVIDENT terminal NON-AUTHORITY
  handoff records with deterministic tip-derived naming; tampering is
  DETECTED at re-read, never prevented (no immutability claim). The
  unanchored read is explicitly informational (untrusted claims);
  `consume_lifecycle_handoff` is the anchored consumer form requiring
  the independently retained original path/SHA-256/size/tip and
  refusing any mismatch (`HANDOFF_EVIDENCE_BYTE_MISMATCH`).
- **GAP-D import boundary (with R3)** — exact blob pinning of the eight
  production modules and MANIFEST against the verified tip, the
  GAP-D-STATIC-V2 closed-world census (42 pinned import-time sites,
  PF-1..PF-5, PF-ARG purity, default-deny statement grammar), the
  caller's own D4 purity gate, and only then an ORDINARY lazy import of
  `bootstrap_authority.receiptidentity` with the transitive runtime load
  disclosed positively. R3: preloaded `bootstrap_authority` cache
  objects are refused unless this gate imported earlier in the same
  process AND every cached object's source at its actual load origin is
  byte-identical to the pinned verified source; the pinned parent is
  always the FIRST `sys.path` entry and the imported origin is asserted
  after import. A dedicated fresh interpreter remains the preferred
  OPERATIONAL precondition for real invocations.
- **The one bounded pipeline (R5)** — `run_authenticated_lifecycle`
  enforces the exact fail-closed sequence trust root -> import gate ->
  G5 identity (with the R1a disclosure) -> G6 selection -> the EXPLICIT
  favorable-G6 hard barrier (disposition
  `PERMIT_GRANT_MINT_CONSIDERATION` AND permitted TRUE, else
  `G6_BARRIER_REFUSED`; adverse dispositions are correct fail-closed
  outcomes) -> G7 re-selection -> complete evidence validation ->
  terminal NON-AUTHORITY handoff of the canonical 12-field
  invocation-evidence binding, anchor returned. No stage is skippable;
  the pipeline selects and verifies only — it mints and publishes
  nothing and confers no authority.
- **Object custody (R6)** — evidence/handoff objects are opened
  relative to the held directory fd with `O_NOFOLLOW|O_NONBLOCK` and
  proven regular files by `fstat`/`S_ISREG` on the OPENED object before
  any bounded read (FIFO/device/special files refused).

## Status

`P3_REMEDIATION_IMPLEMENTED_AS_CANDIDATE /
AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK` — NOT
implementation-closed, NOT qualified, NOT installed. G4 FORBIDDEN;
`package_binding_consideration_permitted = FALSE`; Auditor-B authority
NONE. TRUSTROOT-001 remains CONFIRMED / NOT OPERATIVELY CLOSED;
CR-P3-G5-001 remains OPEN / contract-dependent (Option B not decided).

## Usage (synthetic only)

The tracked `trust-root-config.example.json` is NON-AUTHORITY
documentation — it never loads as an operative config source (the loader
refuses in-repository paths; the real config is operator-held outside
the repository). The test suite exercises every contract surface against
disposable synthetic Git worlds, local bare remotes and synthetic
non-secret bytes only; the GAP-D-BEHAV-V2 behavioral gate runs a fresh
interpreter under network-namespace confinement with LD_PRELOAD
interposition observation (see `tests/test_import_gate.py` for the
strace-substitution disclosure on this host).

Budgets: production `lifecycle_caller.py` 1227/1250 physical LOC
(operator rebound 1000 -> 1250 for this remediation); tests 1912/2000
combined. Reporting correction (R7, CR-P3-EVID-007): the pre-remediation
baseline was 1450/2000 test LOC (969 + 481), not the previously
published 1448 (a stale per-file figure 967 + 481); historical records
are append-only and are not rewritten. The frozen package budgets
(3577/900/4477, zero headroom) are untouched.
