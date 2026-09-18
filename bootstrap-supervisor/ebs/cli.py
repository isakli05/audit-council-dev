"""Inspection-only EBS command line interface.

Deliberately read-only: it validates binding documents and inspects
accounting history.  Authority operations exist ONLY as in-process
state-machine control flow inside a supervisor object and are
intentionally not exposed here as command invocations.
"""
from __future__ import annotations

import argparse
import json
import sys

from .accounting import AccountingStore
from .binding import REQUIRED_GATES, parse_binding


def _validate_binding(path: str) -> int:
    with open(path, "rb") as handle:
        binding = parse_binding(handle.read())
    summary = {
        "ok": True,
        "policy_id": binding.policy_id,
        "event_id": binding.event_id,
        "auditor_role": binding.auditor_role,
        "attempt_id": binding.attempt_id,
        "target_commit": binding.target["commit"],
        "binding_digest": binding.digest,
        "gates_all_pass": sorted(REQUIRED_GATES),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def _inspect_accounting(root: str, attempt_id: str,
                        binding_digest: str) -> int:
    store = AccountingStore.attach(root, attempt_id, binding_digest)
    summary = {
        "ok": True,
        "attempt_id": attempt_id,
        "record_count": len(store.records),
        "last_state": store.last_state,
        "binding_digest": store.binding_digest,
        "states": [rec["state"] for rec in store.records],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="ebs",
        description="AUCDEV-023 EBS inspection tool (read-only)")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser(
        "validate-binding", help="parse + fully validate a binding document")
    validate.add_argument("document")
    inspect = commands.add_parser(
        "inspect-accounting", help="validate an attempt record chain")
    inspect.add_argument("root")
    inspect.add_argument("attempt_id")
    inspect.add_argument("binding_digest")
    args = parser.parse_args(argv)
    try:
        if args.command == "validate-binding":
            return _validate_binding(args.document)
        return _inspect_accounting(args.root, args.attempt_id,
                                   args.binding_digest)
    except Exception as exc:  # fail closed, single refusal line
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
