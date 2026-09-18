#!/usr/bin/env python3
"""Persistent synthetic CONTROLLER fixture for the hardened flows.

The trusted launch spec binds the OPERATOR-AUTHORIZED controller instance
(uid + pid + /proc starttime).  This process plays that role: the spawner
(the operator side of the test) starts it BEFORE the spec is authored,
controls its environment (notably CLAUDE_CONFIG_DIR for C4') and then
drives it with one JSON command per stdin line:

    {"cmd": "mint",    "socket": "qh-root-<id16>", "payload": {...}}
    {"cmd": "request", "socket": "qh-<id16>",      "payload": {...}}
    {"cmd": "exit"}

Exactly one JSON response line is printed per command:

    {"type": "mint", "resp": {...}} / {"type": "request", "resp": {...}}

The abstract socket names are passed WITHOUT the leading NUL; this
process prepends it.  It NEVER receives or carries any authority value —
every request payload is a CLAIM, and all authority lives in the
authority root it talks to.
"""
from __future__ import annotations

import json
import socket
import sys


def _send_once(name_base: str, payload: dict) -> dict:
    """One connect/send/recv round trip.  ANY socket failure — refused,
    reset, timeout, peer death mid-handshake — is a fail-closed response;
    the controller fixture itself must never die on a peer's teardown
    (an abortively-closed peer raises ConnectionResetError on recv)."""
    name = "\0" + name_base
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(300)
    try:
        s.connect(name)
    except OSError as exc:
        return {"ok": False,
                "reason": f"CONNECT_FAILED:{type(exc).__name__}",
                "detail": str(exc)[:200]}
    with s:
        try:
            s.sendall((json.dumps(payload, sort_keys=True) + "\n")
                      .encode("utf-8"))
            data = b""
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    break
                data += chunk
        except OSError as exc:
            return {"ok": False,
                    "reason": f"PEER_FAILED:{type(exc).__name__}",
                    "detail": str(exc)[:200]}
    try:
        return json.loads(data.decode("utf-8", "replace").strip())
    except json.JSONDecodeError:
        return {"ok": False, "reason": "NO_RESPONSE"}


def main() -> int:
    print(json.dumps({"type": "ready", "pid": __import__("os").getpid()}),
          flush=True)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            cmd = json.loads(line)
        except json.JSONDecodeError:
            print(json.dumps({"type": "error",
                              "reason": "BAD_COMMAND"}), flush=True)
            continue
        op = cmd.get("cmd")
        if op == "exit":
            break
        if op in ("mint", "request"):
            resp = _send_once(cmd["socket"], cmd.get("payload") or {})
            print(json.dumps({"type": op, "resp": resp}), flush=True)
        else:
            print(json.dumps({"type": "error",
                              "reason": f"UNKNOWN_CMD:{op}"}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
