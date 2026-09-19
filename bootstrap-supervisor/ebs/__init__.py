"""AUCDEV-023 External Bootstrap Supervisor (EBS) — gate-timing
remediation candidate.

Bounded implementation of the operator-adopted R1 architecture
(CONTROLLERLESS / PROCESS-BOUND / TARGET-INDEPENDENT / ONE-SHOT) as a
minimal bootstrap TCB: Control Room findings AUCDEV023-CR-EBS-001/
-002/-003, AUCDEV023-CR-EBS-REM-001 and AUCDEV023-CR-EBS-REM2-001
remediated and closed at implementation-readback strength on the exact
prior candidate SHA; under the 2026-09-19 gate-timing remediation
authority, AUCDEV023-CR-EBS-S1-001 is remediated at implementer
strength ONLY: the six STATIC preparation gates remain frozen PASS
evidence, while the DYNAMIC RESOURCE_GATE is bound as an exact frozen
executable-artifact descriptor and EXECUTED by the EBS exactly once
during the live attempt — after startup identity checks, BEFORE
GATES_PASSED — with only a freshly validated result able to pass.
Synthetic/inert fixtures only — no real event package. NOT Audit
Council, NOT qualified, NOT installed, NO execution authority, NO real
provider or bootstrap event; a fresh independent Control Room readback
is pending (see README.md).
"""
VERSION = "0.4.0-gate-timing-candidate"

__all__ = ["binding", "statemachine", "accounting", "custody", "launch",
           "reportcustody", "cli"]
