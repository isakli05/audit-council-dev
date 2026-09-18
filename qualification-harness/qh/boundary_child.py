#!/usr/bin/env python3
"""Boundary child entry — runs INSIDE the composed namespace, before the
payload exec.

Order (fail-closed):
  1. read the launch spec from the read-bound spec file;
  2. evaluate the hard no-egress gate over the OBSERVED environment —
     on failure append the result record and exit WITHOUT executing the
     payload (zero provider-capable launch);
  3. verify the materialized TRUSTED BYTES: code/config/executable data
     files must hash to their spec-bound SHA-256 (the materialized /opt/qh
     tree is exactly the operator-verified snapshot — a host-side swap
     racing the pre-launch window is caught HERE); custody secrets are
     verified by LENGTH ONLY (values are never read or printed);
  4. re-verify the SPEC-BOUND source digests (evidence/target) over the
     MOUNTED trees — in-place content substitution between the
     supervisor-side verification and this moment fails closed;
  5. exec the payload (which reports through the write-bound result
     file), or exit 0 for a gate-only launch.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, "/opt/qh")  # noqa: E402 — harness package inside boundary

GATE_FAIL_EXIT = 78


def emit(result_file: str, record: dict) -> None:
    with open(result_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_data_files(spec: dict, result_file: str) -> None:
    ephemeral = list(spec.get("tmpfs_paths", ["/tmp"])) + \
        list(spec.get("rw_inner", []))
    # non-secret trusted code/config bytes additionally materialize on the
    # bwrap tmpfs-root scaffold (/opt/qh tree and the /run-qh scaffold the
    # launcher always creates as tmpfs) — namespace-local ephemeral
    code_allowed = ephemeral + ["/opt/qh", "/run-qh"]
    for df in spec.get("data_files", []):
        target = df["inner_path"]
        allowed = ephemeral if df.get("secret") else code_allowed
        if not any(target == a or target.startswith(a.rstrip("/") + "/")
                   for a in allowed):
            emit(result_file, {"phase": "trusted_bytes", "ok": False,
                               "target": target,
                               "error": "TARGET_NOT_ALLOWED_PATH"})
            os._exit(GATE_FAIL_EXIT)
        if not os.path.isfile(target) or \
                os.path.getsize(target) != df["length"]:
            emit(result_file, {"phase": "trusted_bytes", "ok": False,
                               "target": target,
                               "error": "MATERIALIZATION_INVALID"})
            os._exit(GATE_FAIL_EXIT)
        if df.get("secret"):
            # length only — NEVER the value
            emit(result_file, {"phase": "custody", "ok": True,
                               "target": target, "length": df["length"]})
            continue
        actual = _sha256_file(target)
        if actual != df["sha256"]:
            emit(result_file, {"phase": "trusted_bytes", "ok": False,
                               "target": target,
                               "error": "TRUSTED_BYTES_DRIFT",
                               "expected": df["sha256"], "actual": actual})
            os._exit(GATE_FAIL_EXIT)
        emit(result_file, {"phase": "trusted_bytes", "ok": True,
                           "target": target, "sha256": actual})
    # legacy custody plans (secret_plans) kept for compatibility
    for plan in spec.get("secret_plans", []):
        target = plan["target_path"]
        if not any(target == a or target.startswith(a.rstrip("/") + "/")
                   for a in ephemeral):
            emit(result_file, {"phase": "custody", "ok": False,
                               "label": plan["label"],
                               "error": "TARGET_NOT_EPHEMERAL"})
            os._exit(GATE_FAIL_EXIT)
        if not os.path.isfile(target) or \
                os.path.getsize(target) != plan["length"]:
            emit(result_file, {"phase": "custody", "ok": False,
                               "label": plan["label"],
                               "error": "MATERIALIZATION_INVALID"})
            os._exit(GATE_FAIL_EXIT)
        # length only — NEVER the value
        emit(result_file, {"phase": "custody", "ok": True,
                           "label": plan["label"],
                           "target": target, "length": plan["length"]})


def verify_source_digests(spec: dict, result_file: str) -> None:
    """In-child re-verification of the SPEC-BOUND source tree digests over
    the MOUNTED trees (path-independent digest — same content here and on
    the host at verification time)."""
    from qh.trusted_spec import dir_tree_digest
    mounted = {"evidence": "/evidence", "target": "/target"}
    for name, expected in (spec.get("source_digests") or {}).items():
        inner = mounted.get(name)
        if inner is None or not os.path.isdir(inner):
            continue
        try:
            actual = dir_tree_digest(inner)
        except Exception as exc:  # noqa: BLE001 — any failure fails closed
            emit(result_file, {"phase": "source_verify", "ok": False,
                               "source": name, "error": repr(exc)[:200]})
            os._exit(GATE_FAIL_EXIT)
        if actual != expected:
            emit(result_file, {"phase": "source_verify", "ok": False,
                               "source": name,
                               "error": "SOURCE_CONTENT_DRIFT_IN_CHILD"})
            os._exit(GATE_FAIL_EXIT)
        emit(result_file, {"phase": "source_verify", "ok": True,
                           "source": name})


def main() -> int:
    args = sys.argv[1:]
    spec_file = args[args.index("--spec-file") + 1]
    result_file = args[args.index("--result-file") + 1]
    with open(spec_file, "r", encoding="utf-8") as fh:
        spec = json.load(fh)

    # NOTE: the fresh network namespace (loopback DOWN — the frozen
    # demonstrated no-egress profile) is established OUTSIDE bwrap by
    # the launcher chain (unshare --user --map-root-user --net ...),
    # because bwrap drops capabilities in the child (an in-child
    # unshare would be EPERM) and bwrap's own --unshare-net raises lo.

    if spec.get("noegress"):
        from qh.noegress import NoEgressSpec, check_noegress, \
            collect_net_facts
        nspec = NoEgressSpec()
        facts = collect_net_facts(
            nspec, parent_mntns_inode=spec.get("parent_mntns_inode"))
        gate = check_noegress(facts, nspec)
        emit(result_file, {
            "phase": "noegress",
            "passed": gate.passed,
            "failures": gate.failures,
            "netns_inode": facts.netns_inode,
            "mntns_inode": facts.mntns_inode,
            "inherited_socket_fd_count": len(facts.inherited_socket_fds),
            "lo_state": facts.lo_state,
            "setns_regain": facts.setns_regain,
        })
        if not gate.passed:
            os._exit(GATE_FAIL_EXIT)

    verify_data_files(spec, result_file)
    verify_source_digests(spec, result_file)

    payload_argv = spec.get("payload_argv")
    if payload_argv:
        emit(result_file, {"phase": "payload_exec",
                           "argv": [payload_argv[0]]})
        os.execv(payload_argv[0], payload_argv)
        os._exit(126)  # exec failed

    emit(result_file, {"phase": "gate_only_done"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
