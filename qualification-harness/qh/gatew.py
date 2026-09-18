"""GATE-W — deterministic zero-provider pre-inference write rehearsal.

Proves the effective application-policy semantics for the EXACT generated
profile before any provider-capable launch:

* static: the generated named restricted permission profile content
  satisfies the accepted policy matrix (exactly ONE persistent model-write
  root = the auditor-output role; no root-wide read entry; evidence read
  only; network disabled; no CODEX_HOME/auth entry);
* dynamic: a LOCAL deterministic payload (never a model, never codex, no
  provider inference) executes the semantic operation matrix INSIDE the
  composed outer boundary under hard no-egress with synthetic/inert
  custody material — auditor-output create/write/modify/delete ALLOWED;
  evidence read ALLOWED and evidence create/write/modify/delete/rename
  REFUSED; target/source writes REFUSED; unrelated host paths
  REFUSED/ABSENT; CODEX_HOME config readable but auth ABSENT; persistent
  writable roots exactly the authorized auditor-output role.

A failed GATE-W is a PREEXEC_STOP: no provider-capable auditor may launch
afterward.  The cosmetic CLI banner is never consulted — the managed
profile and the observed boundary semantics are.
"""
from __future__ import annotations

# The semantic matrix the dynamic payload executes (inner boundary paths).
# (name, path, action, expect) — expect is "allowed" or "refused".
MATRIX_OPS: list[tuple[str, str, str, str]] = [
    ("auditor-output create", "/auditor-output/probe-create.txt", "create", "allowed"),
    ("auditor-output write", "/auditor-output/probe-create.txt", "write", "allowed"),
    ("auditor-output modify", "/auditor-output/probe-create.txt", "append", "allowed"),
    ("auditor-output nested mkdir", "/auditor-output/probe-dir/nested", "mkdir", "allowed"),
    ("auditor-output delete", "/auditor-output/probe-create.txt", "delete", "allowed"),
    ("evidence read", "/evidence/evidence.md", "read", "allowed"),
    ("evidence create", "/evidence/new-file.txt", "create", "refused"),
    ("evidence write", "/evidence/evidence.md", "write", "refused"),
    ("evidence modify", "/evidence/evidence.md", "append", "refused"),
    ("evidence delete", "/evidence/evidence.md", "delete", "refused"),
    ("evidence rename", "/evidence/evidence.md", "rename", "refused"),
    ("target write", "/target/t.txt", "create", "refused"),
    ("host /etc write", "/etc/qh-gatew-probe", "create", "refused"),
    ("host /root access", "/root/qh-probe", "create", "refused"),
    ("host home absent", "/home/qh-probe", "create", "refused"),
    ("codex config read", "/codex-home/config.toml", "read", "allowed"),
    ("codex auth absent", "/codex-home/auth.json", "read", "refused"),
]


def evaluate_payload_result(payload: dict, *,
                            custody_required: bool = True) -> list[str]:
    """Evaluate a gatew payload result record; returns failure list."""
    failures: list[str] = []
    ops = payload.get("ops", [])
    if not ops:
        return ["GATEW_NO_OPS_RECORDED"]
    for op in ops:
        ok = op.get("ok")
        if ok is None:
            ok = op.get("expect") == op.get("actual")
        if not ok:
            failures.append(
                f"GATEW_OP:{op.get('name')}:{op.get('path')}"
                f":expect={op.get('expect')}:actual={op.get('actual')}"
                f":{op.get('detail', '')}")
    if custody_required and not payload.get("custody_file_present"):
        failures.append("GATEW_CUSTODY_FILE_ABSENT")
    return failures


def run_static(config_path: str, spec) -> list[str]:
    """Static profile validation (thin wrapper over codex_profile)."""
    from .codex_profile import validate_profile_semantics
    return validate_profile_semantics(config_path, spec)
