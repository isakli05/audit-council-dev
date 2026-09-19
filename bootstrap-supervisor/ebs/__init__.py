"""AUCDEV-023 External Bootstrap Supervisor (EBS) — narrow manifest
row-type remediation candidate.

Bounded implementation of the operator-adopted R1 architecture
(CONTROLLERLESS / PROCESS-BOUND / TARGET-INDEPENDENT / ONE-SHOT) as a
minimal bootstrap TCB: Control Room findings AUCDEV023-CR-EBS-001/
-002/-003 and AUCDEV023-CR-EBS-REM-001 remediated and closed at
implementation-readback strength on the exact prior candidate SHA; under
the 2026-09-19 narrow remediation authority, AUCDEV023-CR-EBS-REM2-001
(files[].bytes: exact non-negative int, bool refused, at manifest-row
validation).  Synthetic/inert fixtures only — no real event package.
NOT Audit Council, NOT qualified, NOT installed, NO execution
authority, NO real provider or bootstrap event; a fresh independent
Control Room readback is pending (see README.md).
"""
VERSION = "0.3.1-narrow-manifest-type-candidate"

__all__ = ["binding", "statemachine", "accounting", "custody", "launch",
           "reportcustody", "cli"]
