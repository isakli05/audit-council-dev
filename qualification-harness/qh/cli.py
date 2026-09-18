"""Operator CLI entry points.

Operator (Control-Room-side) flow — the mint and the supervisor run
OUTSIDE the controller session; the grant travels only through a pipe:

    python -m qh.cli mint --attempt A --root R --manifest M \
        --operator-state D | \
    python -m qh.cli supervisor --operator-state D \
        --custody-fd 3 3< <(printf 'SYNTHETIC-INERT-...')

The controller then connects to the abstract socket ``qh-<hash16>``
(hash of the attempt id) with the request protocol.

``--yama-override`` and ``--fault`` are deterministic TEST fault
injection hooks; each use is recorded in the observability ledger.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from .authority import Supervisor, mint_attempt_grant
from .ledger import ObservabilityLedger
from .util import read_yama_ptrace_scope


def _cmd_mint(args: argparse.Namespace) -> int:
    try:
        grant = mint_attempt_grant(
            attempt_id=args.attempt, root=os.path.abspath(args.root),
            manifest_id=args.manifest,
            operator_state_dir=args.operator_state)
    except Exception as exc:  # noqa: BLE001 — operator-facing CLI
        print(f"MINT_REFUSED: {exc}", file=sys.stderr)
        return 1
    # grant already written to (verified-pipe) stdout by the mint
    print(f"MINTED attempt={grant.attempt_id} grant={grant.grant_id}",
          file=sys.stderr)
    return 0


def _cmd_supervisor(args: argparse.Namespace) -> int:
    # grant must arrive on a PIPE — a file-carried grant is a copied
    # grant and is refused
    import stat as _stat
    st = os.fstat(0)
    if not _stat.S_ISFIFO(st.st_mode):
        print("SUPERVISOR_REFUSED: grant stdin is not a pipe "
              "(copied/persisted grants have no authority)",
              file=sys.stderr)
        return 3
    grant_doc = json.loads(sys.stdin.readline())
    from .authority import Grant
    grant = Grant(**grant_doc)
    policy_kwargs = {}
    if args.yama_override is not None:
        policy_kwargs["yama_value"] = args.yama_override
    faults = set(args.fault or [])
    policy_kwargs["fault_noegress_fail"] = "noegress" in faults
    policy_kwargs["fault_gatew_fail"] = "gatew" in faults
    policy_kwargs["fault_identity_drift"] = "identity" in faults
    policy_kwargs["fault_policy_drift"] = "policy" in faults
    if args.operator_pid is not None:
        policy_kwargs["operator_pid"] = args.operator_pid
    from .authority import SupervisorPolicy
    policy = SupervisorPolicy(**policy_kwargs)
    sup = Supervisor(grant=grant, operator_state_dir=args.operator_state,
                     custody_fd=args.custody_fd, policy=policy)
    sup.startup()
    if sup.exit_code != 0:
        print(f"SUPERVISOR_STARTUP_FAILED code={sup.exit_code}",
              file=sys.stderr)
        return sup.exit_code
    name = sup.bind_socket()
    print(f"READY {name[1:]}", flush=True)
    sup.serve_once()
    print(f"SUPERVISOR_DONE code={sup.exit_code} "
          f"state={sup.machine.state}", flush=True)
    return sup.exit_code


def _cmd_compose_demo(args: argparse.Namespace) -> int:
    from .compose import run_composition_demo
    report = run_composition_demo(args.out)
    with open(os.path.join(args.out, "composition-report.json"), "w",
              encoding="utf-8") as fh:
        json.dump(report, fh, sort_keys=True, indent=1)
    print(json.dumps({"ok": report.get("happy_path", {}).get("ok"),
                      "report": "composition-report.json"},
                     sort_keys=True))
    return 0 if report.get("happy_path", {}).get("ok") else 1


def _cmd_selfcheck(args: argparse.Namespace) -> int:  # noqa: ARG001
    checks = {
        "yama_ptrace_scope": read_yama_ptrace_scope(),
        "bwrap": bool(__import__("shutil").which("bwrap")),
        "userns_net": _userns_net_ok(),
    }
    print(json.dumps(checks, sort_keys=True))
    ok = checks["yama_ptrace_scope"] is not None and \
        checks["yama_ptrace_scope"] >= 1 and checks["bwrap"]
    return 0 if ok else 1


def _userns_net_ok() -> bool:
    import shutil
    import subprocess
    unshare = shutil.which("unshare")
    if not unshare:
        return False
    try:
        return subprocess.run(
            [unshare, "--user", "--map-root-user", "--net", "/bin/true"],
            timeout=10, capture_output=True).returncode == 0
    except Exception:  # noqa: BLE001
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qh")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_mint = sub.add_parser("mint", help="operator-side grant mint "
                             "(pipe output only)")
    p_mint.add_argument("--attempt", required=True)
    p_mint.add_argument("--root", required=True)
    p_mint.add_argument("--manifest", required=True)
    p_mint.add_argument("--operator-state", required=True)
    p_mint.set_defaults(func=_cmd_mint)

    p_sup = sub.add_parser("supervisor", help="one-shot supervising "
                           "gatekeeper (grant on stdin pipe)")
    p_sup.add_argument("--operator-state", required=True)
    p_sup.add_argument("--custody-fd", type=int, default=None,
                       help="operator pipe fd carrying the synthetic "
                            "credential for custody")
    p_sup.add_argument("--yama-override", type=int, default=None,
                       help="TEST fault injection: simulate Yama value")
    p_sup.add_argument("--fault", action="append", default=None,
                       choices=["noegress", "gatew", "identity", "policy"],
                       help="TEST fault injection hook (recorded in "
                            "ledger)")
    p_sup.add_argument("--operator-pid", type=int, default=None,
                       help="optional: require the supervisor's parent "
                            "to be this operator pid")
    p_sup.set_defaults(func=_cmd_supervisor)

    p_demo = sub.add_parser("compose-demo",
                            help="zero-provider integrated C1->C2->C3 "
                            "rehearsal demo")
    p_demo.add_argument("--out", required=True)
    p_demo.set_defaults(func=_cmd_compose_demo)

    p_chk = sub.add_parser("selfcheck", help="environment capability "
                           "check (read-only)")
    p_chk.set_defaults(func=_cmd_selfcheck)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
