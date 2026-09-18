#!/usr/bin/env python3
"""Synthetic controller fixture — plays the controller role for
deterministic C-1/C-2 tests.  Connects to the supervisor's abstract
unix socket, sends one launch request, prints the JSON response.

The spawner controls this process's environment (notably
CLAUDE_CONFIG_DIR) so C4' can verify the ACTUAL /proc/<pid>/environ
binding.
"""
from __future__ import annotations

import json
import socket
import sys


def socket_name(attempt_id: str) -> str:
    import hashlib
    digest = hashlib.sha256(
        json.dumps({"attempt": attempt_id},
                   sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return "\0qh-" + digest[:16]


def main() -> int:
    args = sys.argv[1:]
    req_path = args[args.index("--request") + 1]
    attempt_id = args[args.index("--attempt") + 1]
    with open(req_path, "r", encoding="utf-8") as fh:
        request = json.load(fh)
    name = socket_name(attempt_id)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(120)
    try:
        s.connect(name)
    except OSError as exc:
        print(json.dumps({"ok": False,
                          "reason": f"CONNECT_FAILED:{type(exc).__name__}",
                          "detail": str(exc)[:200]}, sort_keys=True))
        return 2
    with s:
        s.sendall((json.dumps(request, sort_keys=True) + "\n")
                  .encode("utf-8"))
        data = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            data += chunk
    print(data.decode("utf-8", "replace").strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
