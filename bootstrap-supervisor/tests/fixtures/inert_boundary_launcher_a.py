#!/usr/bin/python3
"""EBS INERT SYNTHETIC BOUNDARY FIXTURE (variant A) - NOT A PROVIDER.

Unmistakably synthetic local deterministic test double standing in for the
future frozen networked boundary launcher.  It performs NO network access,
contains NO real credential logic, and implements NO audit substance.  It
reads inherited credential fd 3 ONLY to report its byte length; the
credential bytes themselves are never printed, persisted, or hashed.
Under the S1-006 fixed child fd contract it additionally observes the
HELD verified auditor executable (fd 5 — hashed, since it is NOT a
credential, to prove the delivered live identity) and the sealed
canonical frozen-argv spec (fd 6 — parsed and reported verbatim, proving
the exact binding-frozen auditor argv reached the boundary unchanged).
"""
import hashlib
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


def _read_fd(fd):
    data = b""
    while True:
        chunk = os.read(fd, 65536)
        if not chunk:
            break
        data += chunk
    return data


def main() -> int:
    out = {
        "synthetic_marker": MARKER,
        "variant": VARIANT,
        "argv": sys.argv[1:],
        "env": dict(os.environ),
        "fd_map": _fd_map(),
    }
    try:
        out["credential_fd3_len"] = len(_read_fd(3))
        out["credential_printed"] = False
    except OSError:
        out["credential_fd3_len"] = -1
    try:
        auditor_bytes = _read_fd(5)      # held verified auditor executable
        out["auditor_exec_fd5_len"] = len(auditor_bytes)
        out["auditor_exec_fd5_sha256"] = hashlib.sha256(
            auditor_bytes).hexdigest()
    except OSError:
        out["auditor_exec_fd5_len"] = -1
    try:
        invocation_raw = _read_fd(6)     # sealed canonical frozen-argv spec
        out["invocation_fd6_sha256"] = hashlib.sha256(
            invocation_raw).hexdigest()
        out["invocation_fd6_argv"] = json.loads(invocation_raw.decode())
    except OSError:
        out["invocation_fd6_present"] = False
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
