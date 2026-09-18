#!/usr/bin/env python3
"""GATE-W local dynamic payload — runs INSIDE the composed boundary.

Deterministic, zero-provider: plain filesystem operations that stand in
for model-generated commands, proving the EFFECTIVE outer-boundary and
generated-profile environment semantics.  Reports through the fixed
result fd.  Never prints or reads custody VALUES (existence + length
only).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, "/opt/qh")  # noqa: E402 — harness package inside boundary
from qh.gatew import MATRIX_OPS  # noqa: E402

CODEX_HOME = os.environ.get("CODEX_HOME", "/codex-home")
CUSTODY_PATH = os.environ.get("QH_CUSTODY_TARGET",
                              "/tmp/qh-custody/inert-credential")


def _result_file() -> str:
    args = sys.argv[1:]
    return args[args.index("--result-file") + 1]


def op_create(path: str) -> str:
    try:
        with open(path, "x", encoding="utf-8") as fh:
            fh.write("qh-gatew\n")
        return "allowed"
    except OSError as exc:
        return f"refused:{exc.errno}"


def op_write(path: str) -> str:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("qh-gatew-write\n")
        return "allowed"
    except OSError as exc:
        return f"refused:{exc.errno}"


def op_append(path: str) -> str:
    try:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("qh-gatew-append\n")
        return "allowed"
    except OSError as exc:
        return f"refused:{exc.errno}"


def op_read(path: str) -> str:
    try:
        with open(path, "rb") as fh:
            data = fh.read()
        return "allowed" if data else "allowed:empty"
    except OSError as exc:
        return f"refused:{exc.errno}"


def op_delete(path: str) -> str:
    try:
        os.unlink(path)
        return "allowed"
    except OSError as exc:
        return f"refused:{exc.errno}"


def op_rename(path: str) -> str:
    try:
        os.rename(path, path + ".renamed")
        os.rename(path + ".renamed", path)  # restore if allowed
        return "allowed"
    except OSError as exc:
        return f"refused:{exc.errno}"


def op_mkdir(path: str) -> str:
    try:
        os.makedirs(path, exist_ok=True)
        return "allowed"
    except OSError as exc:
        return f"refused:{exc.errno}"


_ACTIONS = {"create": op_create, "write": op_write, "append": op_append,
            "read": op_read, "delete": op_delete, "rename": op_rename,
            "mkdir": op_mkdir}


def main() -> int:
    result_file = _result_file()
    ops = []
    for name, path, action, expect in MATRIX_OPS:
        # CODEX_HOME-referencing matrix entries follow the configured
        # boundary-private provider home (path-shape preserved)
        if path.startswith("/codex-home/"):
            path = CODEX_HOME + path[len("/codex-home"):]
        actual = _ACTIONS[action](path)
        ok = (actual == "allowed" or actual.startswith("allowed")) \
            if expect == "allowed" else actual.startswith("refused")
        ops.append({"name": name, "path": path, "action": action,
                    "expect": expect, "actual": actual, "ok": ok})
    custody_present = os.path.isfile(CUSTODY_PATH)
    custody_len = (os.path.getsize(CUSTODY_PATH)
                   if custody_present else None)
    record = {"phase": "payload_result", "kind": "gatew",
              "ops": ops,
              "all_expected": all(o["ok"] for o in ops),
              "custody_file_present": custody_present,
              "custody_length": custody_len}
    with open(result_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    return 0 if record["all_expected"] else 3


if __name__ == "__main__":
    sys.exit(main())
