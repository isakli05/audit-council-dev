"""AUCDEV-023 External Bootstrap Supervisor (EBS) — remediation candidate.

Bounded implementation of the operator-adopted R1 architecture
(CONTROLLERLESS / PROCESS-BOUND / TARGET-INDEPENDENT / ONE-SHOT) as a
minimal bootstrap TCB, remediating Control Room findings
AUCDEV023-CR-EBS-001/-002/-003 (complete mandatory transport binding;
structurally closed one-shot authority without revival; runtime package
self-identity verification).  NOT Audit Council, NOT qualified, NOT
installed, NO execution authority, NO real provider or bootstrap event;
a fresh independent Control Room readback is pending (see README.md).
"""
VERSION = "0.2.0-remediation-candidate"

__all__ = ["binding", "statemachine", "accounting", "custody", "launch",
           "reportcustody", "cli"]
