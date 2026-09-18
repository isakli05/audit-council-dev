"""Operator CLI entry points (IR-003 remediated production surface).

Production authority flow — everything security-critical originates at the
OPERATOR authority root, never at a controller request:

    qh authority --operator-state D --custody-fd 3 --finalization-fd 4 \
        < pre-controller-template.json 3< <(printf 'SYNTHETIC-INERT-...') \
        4< <(printf '{"template_id": ..., "authorized_controller": ...}')

The authority (started by the operator BEFORE any controller exists)
executes the PRE-CONTROLLER TRUST FREEZE from the operator-selected
identity (template + custody on operator capability channels; the live
harness tree verified, the privileged byte set frozen+sealed, every
privileged module loaded with code-object provenance; prints
PRECONTROLLER_READY), and only after the operator starts the authorized
controller and sends the finalization delta on the retained operator
channel does it finalize the final spec, expose the trigger, serve
EXACTLY ONE mint on its abstract socket, and fork the one-shot supervisor
from the frozen state.  The controller then connects to the supervisor's
abstract socket with a CLAIM-ONLY request (attempt id, starttime claim,
env claims, payload kind) — every security-critical value comes from the
trusted spec.

NO production trust-check overrides exist: ``--yama-override`` and every
``--fault``-style hook are REJECTED by the production parser (deterministic
test fault injection lives ONLY in the test suite, via monkeypatched
internal seams — never on the operational CLI path).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from .util import read_yama_ptrace_scope

# Flags that must NEVER reappear on the operational CLI (IR-003).  Any
# occurrence — even as a value of another flag — is refused before parsing.
_FORBIDDEN_PRODUCTION_FLAGS = ("--yama-override", "--fault",
                               "--fault-noegress", "--fault-gatew",
                               "--fault-identity", "--fault-policy")

PRODUCTION_SUBCOMMANDS = ("authority", "supervisor", "compose-demo",
                          "selfcheck")


def _reject_forbidden_flags(argv: list[str]) -> None:
    for arg in argv:
        if arg.split("=", 1)[0] in _FORBIDDEN_PRODUCTION_FLAGS:
            print(
                f"PRODUCTION_CLI_REFUSED: {arg.split('=', 1)[0]} is not "
                "accepted on the production CLI — production trust checks "
                "have no override (test fault injection is test-surface "
                "only)", file=sys.stderr)
            raise SystemExit(2)


def _cmd_authority(args: argparse.Namespace) -> int:
    """The TWO-PHASE production authority entry (CR-HARDEN-001):

    PHASE A — ``pre_controller_startup`` (the authorized controller does
    NOT exist yet): the pre-controller launch template + the operator
    finalization channel + the provider custody must ALL be operator-held
    capability channels (PIPE or mechanically identified FULLY SEALED
    memfd; ordinary regular files — including stdin redirected from a
    file — are REFUSED before any byte is read, CR-REMED-003); the live
    harness tree is verified against the OPERATOR-SELECTED template
    identity; the privileged byte set is frozen+sealed, every privileged
    module imported with code-object provenance and the import guard
    armed; ``PRECONTROLLER_READY`` is printed only after
    PRE_CONTROLLER_BOOTSTRAP_FROZEN.

    PHASE B — the operator (who started the authorized controller only
    after observing ``PRECONTROLLER_READY``) sends the finalization delta
    on the retained finalization channel; the final spec is derived
    in-process from the frozen template + controller identity, the
    frozen-harness-id equality is proven, and only then (``READY``) is
    the controller trigger exposed."""
    from .rootauth import AuthorityRoot
    from .util import (SealUnavailableError, read_bounded,
                       require_trusted_spec_fd)
    # CR-REMED-003 (both operator input channels gated before ANY byte
    # is read): template channel + finalization channel.
    try:
        channel = require_trusted_spec_fd(args.template_fd)
        fin_channel = require_trusted_spec_fd(args.finalization_fd)
    except (OSError, SealUnavailableError) as exc:
        print(f"ROOT_REFUSED: {exc}", file=sys.stderr)
        return 15
    try:
        template_bytes = read_bounded(args.template_fd)
    except (OSError, SealUnavailableError) as exc:
        print(f"ROOT_REFUSED: cannot read template fd: {exc}",
              file=sys.stderr)
        return 15
    if not template_bytes:
        print("ROOT_REFUSED: empty pre-controller launch template",
              file=sys.stderr)
        return 15
    root = AuthorityRoot(
        operator_state_dir=args.operator_state,
        template_bytes=template_bytes, custody_fd=args.custody_fd,
        finalization_fd=args.finalization_fd)
    # -------- PHASE A (no controller exists) --------------------------
    root.pre_controller_startup()
    if root.exit_code != 0:
        print(f"ROOT_STARTUP_FAILED code={root.exit_code} "
              f"reason={root.fail_reason}", file=sys.stderr)
        root.shutdown()
        return root.exit_code
    print("PRECONTROLLER_READY", flush=True)
    # -------- PHASE B (operator finalization over the retained channel) --
    try:
        delta_bytes = read_bounded(args.finalization_fd, limit=1 << 16)
    except (OSError, SealUnavailableError) as exc:
        print(f"ROOT_FINALIZATION_FAILED code=18 reason={exc}",
              file=sys.stderr)
        root.shutdown()
        return 18
    root.finalize_controller_binding(delta_bytes)
    if root.exit_code != 0:
        print(f"ROOT_FINALIZATION_FAILED code={root.exit_code} "
              f"reason={root.fail_reason}", file=sys.stderr)
        root.shutdown()
        return root.exit_code
    name = root.bind_socket()
    print(f"READY {name[1:]}", flush=True)
    response = root.serve_mint_once(timeout=args.mint_timeout)
    rc = root.wait_for_supervisor()
    root.shutdown()
    if not response.get("ok"):
        return root.exit_code or 16
    print(f"ROOT_DONE code={root.exit_code} supervisor_rc={rc}",
          flush=True)
    # the root's exit reflects the supervised attempt lifecycle (a
    # terminal preexec stop in the supervisor is visible in the root's
    # exit code)
    return root.exit_code if root.exit_code else (rc or 0)


def _cmd_supervisor(args: argparse.Namespace) -> int:
    # grant + trusted spec arrive on a PIPE — a file-carried grant is a
    # copied grant and is refused
    import stat as _stat
    st = os.fstat(0)
    if not _stat.S_ISFIFO(st.st_mode):
        print("SUPERVISOR_REFUSED: grant stdin is not a pipe "
              "(copied/persisted grants have no authority)",
              file=sys.stderr)
        return 3
    grant_doc = json.loads(sys.stdin.readline())
    spec_bytes = sys.stdin.readline().strip().encode("utf-8")
    if not spec_bytes:
        print("SUPERVISOR_REFUSED: trusted launch spec line missing",
              file=sys.stderr)
        return 3
    from .authority import Grant, Supervisor
    from .trusted_spec import parse_spec_bytes, spec_id
    grant = Grant(**grant_doc)
    spec = parse_spec_bytes(spec_bytes)
    computed = spec_id(spec)
    if grant.spec_id is not None and computed != grant.spec_id:
        print("SUPERVISOR_STARTUP_FAILED SPEC_ID_MISMATCH "
              f"(grant-bound {grant.spec_id[:12]}… != pipe {computed[:12]}…)",
              file=sys.stderr)
        return 13
    sup = Supervisor(grant=grant, spec=spec, spec_id=computed,
                     operator_state_dir=args.operator_state,
                     custody_fd=args.custody_fd)
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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="qh")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_auth = sub.add_parser(
        "authority", help="two-phase operator authority root: freezes the "
        "pre-controller trusted bootstrap (template + custody, verified "
        "against the operator-selected identity), then finalizes the "
        "final spec over the operator finalization channel and performs "
        "the ONE production mint")
    p_auth.add_argument("--operator-state", required=True)
    p_auth.add_argument("--template-fd", type=int, default=0,
                        help="operator-held CAPABILITY fd carrying the "
                             "complete PRE-CONTROLLER LAUNCH TEMPLATE: a "
                             "PIPE or a fully SEALED memfd (an ordinary "
                             "file — including stdin redirected from a "
                             "file — is REFUSED; default: stdin)")
    p_auth.add_argument("--custody-fd", type=int, required=True,
                        help="operator pipe/memfd carrying the provider "
                             "credential bytes (an ordinary file is "
                             "refused)")
    p_auth.add_argument("--finalization-fd", type=int, required=True,
                        help="operator-held CAPABILITY fd for the "
                             "controller-binding finalization delta (a "
                             "PIPE created before controller startup "
                             "whose WRITE end the operator keeps, or a "
                             "fully SEALED memfd; never an ordinary "
                             "file, never argv/env)")
    p_auth.add_argument("--mint-timeout", type=float, default=300.0)
    p_auth.set_defaults(func=_cmd_authority)

    p_sup = sub.add_parser("supervisor", help="one-shot supervising "
                           "gatekeeper — TEST/DIAGNOSTIC entry (grant + "
                           "trusted launch spec on stdin pipe).  "
                           "PRODUCTION supervisors are created by the "
                           "authority root via fork() from the frozen "
                           "privileged bootstrap, never by a fresh host-"
                           "tree import")
    p_sup.add_argument("--operator-state", required=True)
    p_sup.add_argument("--custody-fd", type=int, default=None,
                       help="inherited custody memfd/pipe fd carrying the "
                            "provider credential bytes")
    p_sup.set_defaults(func=_cmd_supervisor)

    p_demo = sub.add_parser("compose-demo",
                            help="zero-provider integrated C1->C2->C3 "
                            "rehearsal demo (authority-root flow)")
    p_demo.add_argument("--out", required=True)
    p_demo.set_defaults(func=_cmd_compose_demo)

    p_chk = sub.add_parser("selfcheck", help="environment capability "
                           "check (read-only)")
    p_chk.set_defaults(func=_cmd_selfcheck)
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    _reject_forbidden_flags(argv)
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
