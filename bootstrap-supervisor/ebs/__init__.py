"""AUCDEV-023 External Bootstrap Supervisor (EBS) — implemented candidate.

Bounded implementation of the operator-adopted R1 governance architecture
(CONTROLLERLESS / PROCESS-BOUND / TARGET-INDEPENDENT / ONE-SHOT) for the
AUCDEV-023 exceptional auditor-bootstrap path, as a minimal bootstrap TCB.

Linux-only by governance.  Python 3 standard library only.  This package
is NOT Audit Council, is NOT qualified, is NOT installed, carries NO
execution authority, and supports NO real provider or bootstrap event:
GATE-W-prime and real-client credential/tool isolation remain unproven
future event-preparation gates.  Implementation claims are not audit
truth; independent Control Room readback is pending.
"""
VERSION = "0.1.0-implemented-candidate"

__all__ = ["binding", "statemachine", "accounting", "custody", "launch",
           "reportcustody", "cli"]
