"""AUCDEV-023 External Bootstrap Supervisor (EBS) — preexec-gate
remediation candidate.  Bounded implementation of the operator-adopted R1 architecture
(CONTROLLERLESS / PROCESS-BOUND / TARGET-INDEPENDENT / ONE-SHOT) as a
minimal bootstrap TCB: findings CR-EBS-001/-002/-003, CR-EBS-REM-001
and CR-EBS-REM2-001 closed at implementation-readback strength on the
exact prior candidate SHA, and CR-EBS-S1-001 closed on 8e952d81;
under the 2026-09-19 preexec-gate remediation authority,
CR-EBS-S1-002 and CR-EBS-S1-003 are remediated at implementer strength
ONLY: the six STATIC preparation gates remain
frozen PASS evidence, the TWO DYNAMIC runtime gates (NETWORK_READINESS
first, RESOURCE_GATE last) are bound as exact frozen executable-artifact
descriptors and EXECUTED by the EBS exactly once each inside the ONE
public preexec-consumption operation consume(launcher_path), with
durable GATES_PASSED (both evidence sets) immediately followed by
durable CONSUMED_PRE_EXEC and NO caller-visible GATES_PASSED state.
Synthetic/inert fixtures only — no real event package. NOT Audit
Council, NOT qualified, NOT installed, NO execution authority, NO real
provider or bootstrap event; a fresh Control Room readback is pending.
"""
VERSION = "0.5.0-preexec-gate-candidate"

__all__ = ["binding", "statemachine", "accounting", "custody", "launch",
           "reportcustody", "cli"]
