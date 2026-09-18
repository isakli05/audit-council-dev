"""AUCDEV-023 qualification harness (C-1 / C-2 / C-3 fail-closed mechanisms).

Durable, reusable, NON-PRODUCT harness component implementing the accepted
readiness criteria recorded in
docs/chatgpt-project/AUCDEV-023-G2-CLEAN-EXEC-POLICY-EQUIVALENCE-REPRODUCTION-READBACK.md
(parallel BACKLOG record):

* C-1  pre-controller controller-scope provenance + C4' actual
  process-binding evidence (bootstrap manifest; current tree is a subset of
  manifest plus the controller's OWN current-session project slug);
* C-2 / G-1  process-bound one-shot supervising launch authority
  (PR_SET_DUMPABLE=0 kernel-process-bound authority; one-shot exact
  attempt/root binding; terminal PREEXEC_STOP; replay/reuse/binding
  rejection; new attempt only via a new out-of-band operator mint;
  credential custody mandatory; Yama ptrace_scope >= 1 environmental gate);
* C-3 / G-2  primary workspace = auditor-output role; NO --add-dir; NO CLI
  -s/--sandbox workspace-write; named restricted permission profile from a
  disposable CODEX_HOME; hard no-egress gate (systemd-resolved/D-Bus
  AF_UNIX masking, ZERO inherited socket FDs); pre-inference GATE-W
  zero-provider rehearsal.

The harness is GENERIC: no historical target, attempt, auditor or finding
identity is baked into behavior.  Demonstrated profile values live only as
DATA in fixtures/demonstrated-profile.json.

Ordinary files (ledgers, manifests) are OBSERVABILITY ONLY — authority is
process-bound.  See README.md for the threat model and residuals.
"""

__version__ = "1.0.0"

# G-1 mandatory implementation invariant (readiness record, 2026-09-18).
CREDENTIAL_CUSTODY_IS_REQUIRED_FOR_G1_ENFORCEMENT = True

# Historical no-egress preflight finding that must have a deterministic
# regression (AUCDEV-023 G-2 clean reproduction readback, section 5).
HARD_NO_EGRESS_GATE_MUST_REQUIRE_ZERO_INHERITED_SOCKET_FDS = True
SYSTEMD_RESOLVED_AF_UNIX_ESCAPE_SURFACE = "SYSTEMD_RESOLVED_AF_UNIX_ESCAPE_SURFACE"
