"""AUCDEV-023 External Bootstrap Supervisor (EBS) — second remediation
candidate.

Bounded implementation of the operator-adopted R1 architecture
(CONTROLLERLESS / PROCESS-BOUND / TARGET-INDEPENDENT / ONE-SHOT) as a
minimal bootstrap TCB, remediating Control Room findings
AUCDEV023-CR-EBS-001/-002/-003 (complete mandatory transport binding;
structurally closed one-shot authority without revival; runtime package
self-identity verification) and, under the 2026-09-19 second bounded
remediation authority, AUCDEV023-CR-EBS-REM-001 (generic fail-closed
frozen event-package verification + transport cross-binding BEFORE
GATES_PASSED; synthetic/inert fixtures only — no real event package).
NOT Audit Council, NOT qualified, NOT installed, NO execution authority,
NO real provider or bootstrap event; a fresh independent Control Room
readback is pending (see README.md).
"""
VERSION = "0.3.0-second-remediation-candidate"

__all__ = ["binding", "statemachine", "accounting", "custody", "launch",
           "reportcustody", "cli"]
