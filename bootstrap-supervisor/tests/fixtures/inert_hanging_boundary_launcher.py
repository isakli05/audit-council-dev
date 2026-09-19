#!/usr/bin/python3
"""EBS INERT SYNTHETIC HANGING BOUNDARY FIXTURE - NOT A PROVIDER.

Unmistakably synthetic local deterministic test double for
CR-EBS-S1-008: it writes its (honest, non-secret) metadata line to
stdout, records its process identities to an external /tmp track file
keyed by the attempt id, forks a DESCENDANT that also never exits, and
then never exits itself — standing in for a hung boundary/provider
client process tree the EBS must terminate via its frozen
auditor_timeout_seconds process-group discipline.  NO network access,
NO credential logic, NO audit substance; the credential fd 3 is never
read (its byte length alone would be irrelevant here).
"""
import json
import os
import sys
import time

MARKER = "EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER"
VARIANT = "INERT-HANGING-FIXTURE"
TRACK_BASE = "/tmp/aucdev023-hang-"


def main() -> int:
    attempt = sys.argv[sys.argv.index("--attempt") + 1]
    out = {
        "synthetic_marker": MARKER,
        "variant": VARIANT,
        "argv": sys.argv[1:],
    }
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()
    pid = os.fork()
    if pid == 0:                     # descendant: outlives the launcher
        time.sleep(600)
        os._exit(0)
    with open(TRACK_BASE + attempt, "w") as handle:
        handle.write(json.dumps({"launcher_pid": os.getpid(),
                                 "descendant_pid": pid}))
    time.sleep(600)                  # the launcher itself never exits
    return 0


if __name__ == "__main__":
    sys.exit(main())
