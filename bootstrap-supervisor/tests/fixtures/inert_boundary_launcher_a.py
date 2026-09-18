#!/usr/bin/python3
"""EBS INERT SYNTHETIC BOUNDARY FIXTURE (variant A) - NOT A PROVIDER.

Unmistakably synthetic local deterministic test double standing in for the
future frozen networked boundary launcher.  It performs NO network access,
contains NO real credential logic, and implements NO audit substance.  It
reads inherited credential fd 3 ONLY to report its byte length; the
credential bytes themselves are never printed, persisted, or hashed.
"""
import json
import os
import sys

VARIANT = "INERT-FIXTURE-A"
MARKER = "EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER"


def _fd_map():
    """Snapshot fd -> link target; the listing fd itself may vanish
    between listdir and readlink (transient), which is recorded honestly."""
    mapping = {}
    for fd in sorted(int(x) for x in os.listdir("/proc/self/fd")):
        try:
            mapping[fd] = os.readlink(f"/proc/self/fd/{fd}")
        except OSError:
            mapping[fd] = "<vanished-during-listing>"
    return mapping


def main() -> int:
    out = {
        "synthetic_marker": MARKER,
        "variant": VARIANT,
        "argv": sys.argv[1:],
        "env": dict(os.environ),
        "fd_map": _fd_map(),
    }
    try:
        data = b""
        while True:
            chunk = os.read(3, 65536)
            if not chunk:
                break
            data += chunk
        out["credential_fd3_len"] = len(data)
        out["credential_printed"] = False
    except OSError:
        out["credential_fd3_len"] = -1
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()
    args = sys.argv[1:]
    if "--staging-report" in args:
        path = args[args.index("--staging-report") + 1]
        with open(path, "w") as handle:
            handle.write(json.dumps({
                "synthetic_marker": MARKER,
                "variant": VARIANT,
            }) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
