"""AUCDEV-023 External Bootstrap Supervisor (EBS) — final launch-seam
remediation candidate.  Bounded implementation of the operator-adopted
R1 architecture (CONTROLLERLESS / PROCESS-BOUND / TARGET-INDEPENDENT /
ONE-SHOT) as a minimal bootstrap TCB: findings CR-EBS-001/-002/-003,
CR-EBS-REM-001 and CR-EBS-REM2-001 closed at implementation-readback
strength on the exact prior candidate SHA, CR-EBS-S1-001 closed on
8e952d81, CR-EBS-S1-002/-003 closed on 6cf30f90; under the 2026-09-20
final launch-seam remediation authority, CR-EBS-S1-004/-005/-006 are
remediated at implementer strength ONLY: the ONE public authority
operation run_attempt(credential_source_fd, launcher_path,
auditor_executable_path) owns the sealed exact-role credential custody
BEFORE gates and consumption, collapses durable GATES_PASSED ->
CONSUMED_PRE_EXEC -> IMMEDIATE fork/exec into ONE caller-uninterruptible
call with NO grant and NO consume()/execute() split, verifies and HOLDS
the live auditor executable against the binding SHA (V4 adds
executable_version + the exact frozen auditor_invocation argv, carried
to the boundary launcher on a sealed fd under the fixed child fd
contract CRED_FD=3 / FAIL_FD=4 / AUDITOR_EXEC_FD=5 /
AUDITOR_INVOCATION_FD=6), and admits NO caller argv tail or environment
override.  Synthetic/inert fixtures only — no real event package. NOT
Audit Council, NOT qualified, NOT installed, NO execution authority, NO
real provider or bootstrap event; a fresh Control Room readback is
pending.
"""
VERSION = "0.6.0-final-launch-seam-candidate"

__all__ = ["binding", "statemachine", "accounting", "custody", "launch",
           "reportcustody", "cli"]
