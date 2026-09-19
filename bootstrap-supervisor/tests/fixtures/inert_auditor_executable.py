#!/usr/bin/python3
"""EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER synthetic auditor
executable (S1-006 final launch-seam remediation).

Unmistakably synthetic/inert LOCAL stand-in for the future REAL auditor
provider-client executable.  Under this remediation it is NEVER
EXECUTED and performs NO network access of any kind: the EBS only
OPENS it (no final symlink), requires regular+executable mode, hashes
the already-open fd against binding.auditor_identity's exact SHA-256,
and HOLDS the verified fd as AUDITOR_EXEC_FD=5 for the boundary
launcher, whose inert fixture reads those bytes solely to OBSERVE the
delivered identity.  The REAL provider client is never invoked here.
"""
MARKER = "EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER"
IDENTITY = "SYNTHETIC-INERT-AUDITOR-EXECUTABLE-V1"

if __name__ == "__main__":
    raise SystemExit(
        "EBS inert synthetic auditor executable: a test fixture, never a "
        "provider client; the EBS launches only the boundary launcher.")
