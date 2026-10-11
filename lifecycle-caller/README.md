# AUCDEV-023 PCH6-B Path-B — TRUSTROOT-001 authenticated lifecycle caller (P3)

`lifecycle_caller.py` is the P3 NON-RUNTIME authenticated lifecycle caller
for the AUCDEV-023 Path-B replacement Auditor-A authority protocol. It is
an IMPLEMENTATION CANDIDATE implementing the accepted design-layer
contracts (records `8b31d8e5...` and `8bf12dea...`, Control Room dispositions
`86f4e7c0...` and `bed8f50f...`) and it GRANTS NOTHING: it creates no grant,
no GRANT_ISSUED evidence, no G5/G6/G7/G10/G11 publication, no receipt and
no package, and performs no operative lifecycle action.

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
- **GRANT_ISSUED evidence (R-EVID)** — re-selects the canonical G7 mint
  publication with the INDEPENDENTLY derived G6 identity set, enforces
  the deterministic evidence path under the held-dirfd discipline, and
  verifies the original bytes against the pinned digest and size.
- **Handoff content identity (GAP C)** — SINGLE_CREATION /
  CONTENT_IDENTITY_PINNED / TAMPER_EVIDENT terminal NON-AUTHORITY
  handoff records with deterministic tip-derived naming; tampering is
  DETECTED at re-read, never prevented (no immutability claim).
- **GAP-D import boundary** — exact blob pinning of the eight production
  modules and MANIFEST against the verified tip, the GAP-D-STATIC-V2
  closed-world census (42 pinned import-time sites, PF-1..PF-5, PF-ARG
  purity, default-deny statement grammar), the caller's own D4 purity
  gate, and only then an ORDINARY lazy import of
  `bootstrap_authority.receiptidentity` with the transitive runtime load
  disclosed positively. No runtime authority is ever invoked.

## Status

`P3_IMPLEMENTED_AS_CANDIDATE / AWAITING_INDEPENDENT_CONTROL_ROOM_READBACK`
— NOT implementation-closed, NOT qualified, NOT installed. G4 FORBIDDEN;
`package_binding_consideration_permitted = FALSE`; Auditor-B authority
NONE. TRUSTROOT-001 remains CONFIRMED / NOT OPERATIVELY CLOSED.

## Usage (synthetic only)

The tracked `trust-root-config.example.json` is NON-AUTHORITY
documentation — it never loads as an operative config source (the loader
refuses in-repository paths; the real config is operator-held outside the
repository). The test suite exercises every contract surface against
disposable synthetic Git worlds, local bare remotes and synthetic
non-secret bytes only; the GAP-D-BEHAV-V2 behavioral gate runs a fresh
interpreter under network-namespace confinement with LD_PRELOAD
interposition observation (see `tests/test_import_gate.py` for the
strace-substitution disclosure on this host).

Budgets: production `lifecycle_caller.py` 1000/1000 physical LOC (zero
headroom); tests 1448/2000. The frozen package budgets
(3577/900/4477) are untouched.
