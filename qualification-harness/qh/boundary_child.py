#!/usr/bin/env python3
"""Boundary child entry — runs INSIDE the composed namespace, before the
payload exec.

Order (fail-closed):
  1. read the launch spec from the read-bound spec file;
  2. evaluate the hard no-egress gate over the OBSERVED environment —
     on failure append the result record and exit WITHOUT executing the
     payload (zero provider-capable launch);
  3. verify custody materialization (bwrap --bind-data files exist with
     exactly the expected lengths; values are never read or printed
     here);
  4. exec the payload (which reports through the write-bound result
     file), or exit 0 for a gate-only launch.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, "/opt/qh")  # noqa: E402 — harness package inside boundary

GATE_FAIL_EXIT = 78


def emit(result_file: str, record: dict) -> None:
    with open(result_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def verify_secrets(spec: dict, result_file: str) -> None:
    allowed = list(spec.get("tmpfs_paths", ["/tmp"])) + \
        list(spec.get("rw_inner", []))
    for plan in spec.get("secret_plans", []):
        target = plan["target_path"]
        if not any(target == a or target.startswith(a.rstrip("/") + "/")
                   for a in allowed):
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

    verify_secrets(spec, result_file)

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
