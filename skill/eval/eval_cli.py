#!/usr/bin/env python3
"""Thin eval CLI dispatch (pillar D).

  python3 eval/eval_cli.py tier1
  python3 eval/eval_cli.py tier2-build <root>
  python3 eval/eval_cli.py tier3 <seed> \
      --i-have-operator-approval --approver NAME --approved-at ISO

tier3 refuses without the full explicit operator-approval flag set and
prints the gate text. Output is JSON on stdout; nothing is written to disk
by tier1/tier3 (tier2-build writes only under the caller-given root).
"""
from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.realpath(__file__))
_SKILL = os.path.dirname(_HERE)
if _SKILL not in sys.path:
    sys.path.insert(0, _SKILL)  # make the `eval` package importable

from eval import tier1_harness, tier2_fixtures, tier3_replay  # noqa: E402

USAGE = ("usage: eval_cli.py tier1 | tier2-build <root> | tier3 <seed> "
         "[--i-have-operator-approval --approver NAME "
         "--approved-at ISO]")


def _flag(argv: list[str], name: str) -> str | None:
    try:
        i = argv.index(name)
        return argv[i + 1]
    except (ValueError, IndexError):
        return None


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(USAGE, file=sys.stderr)
        return 2
    cmd, rest = argv[0], argv[1:]

    if cmd == "tier1" and not rest:
        print(json.dumps(tier1_harness.tier1(), indent=2, sort_keys=True))
        return 0

    if cmd == "tier2-build" and len(rest) == 1:
        print(json.dumps(tier2_fixtures.build_all(rest[0]),
                         indent=2, sort_keys=True))
        return 0

    if cmd == "tier2-score" and len(rest) == 1:
        from eval import tier2_scoring
        print(json.dumps(tier2_scoring.tier2_score(rest[0]),
                         indent=2, sort_keys=True))
        return 0

    if cmd == "tier3" and len(rest) >= 1:
        seed = rest[0]
        if "--i-have-operator-approval" not in rest:
            refusal = {"status": "refused", "seed": seed,
                       "gate": tier3_replay.GATE_TEXT}
            print(json.dumps(refusal, indent=2, sort_keys=True))
            print(tier3_replay.GATE_TEXT, file=sys.stderr)
            return 3
        approver = _flag(rest, "--approver")
        approved_at = _flag(rest, "--approved-at")
        if not approver or not approved_at:
            print(USAGE, file=sys.stderr)
            print(tier3_replay.GATE_TEXT, file=sys.stderr)
            return 3
        approval = {"operator_approval": True,
                    "approver": approver,
                    "approved_at": approved_at}
        result = tier3_replay.replay(seed, approval)
        print(json.dumps(result, indent=2, sort_keys=True))
        if result.get("status") == "refused":
            print(tier3_replay.GATE_TEXT, file=sys.stderr)
            return 3
        return 0

    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
