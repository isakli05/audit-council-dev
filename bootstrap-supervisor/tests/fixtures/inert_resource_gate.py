#!/usr/bin/python3
"""EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER runtime resource gate.

Unmistakably synthetic/inert gate artifact for the AUCDEV-023 EBS
zero-provider battery (S1-001 gate-timing remediation).  NOT a provider,
NOT a real resource policy: it samples DETERMINISTIC LOCAL "live" state —
a mode file keyed by attempt id under /tmp plus two trivial local system
samples — and emits the strict AUCDEV-023-RESOURCE-GATE-RESULT-V1
envelope.  Behavior modes come from the EXTERNAL state file (absent =
honest PASS with three fresh PASS samples), never from package bytes:
the SAME frozen artifact PASSes or FAILs based on conditions sampled at
EXECUTION time, which is exactly the freshness property under test.

The gate writes an attempt-keyed execution sentinel + counter under /tmp
so tests can prove WHETHER and HOW OFTEN the EBS actually executed it.
"""
import json
import os
import sys
import time

SCHEMA = "AUCDEV-023-RESOURCE-GATE-RESULT-V1"
BASE = "/tmp/aucdev023-rg-"


def paths(attempt):
    return (BASE + "state-" + attempt + ".json",
            BASE + "sentinel-" + attempt,
            BASE + "count-" + attempt)


def live_samples(mode):
    """Three FRESH samples of deterministic local live state."""
    ok1 = mode in (None, "pass")            # external live-state oracle
    try:
        free = os.statvfs("/tmp").f_bavail > 0
    except OSError:
        free = False
    try:
        with open("/proc/meminfo") as handle:
            mem = "MemAvailable" in handle.read()
    except OSError:
        mem = False
    return [
        {"status": "PASS" if ok1 else "FAIL",
         "detail": {"sampled": "external-live-state", "mode": mode}},
        {"status": "PASS" if free else "FAIL",
         "detail": {"sampled": "statvfs-tmp", "free": free}},
        {"status": "PASS" if mem else "FAIL",
         "detail": {"sampled": "proc-meminfo", "readable": mem}},
    ]


def main():
    if len(sys.argv) < 4:
        return 3
    event, role, attempt = sys.argv[1], sys.argv[2], sys.argv[3]
    state_path, sentinel, count = paths(attempt)
    try:
        with open(sentinel, "w") as handle:
            handle.write(event + " " + role + " " + attempt + "\n")
        seen = 0
        if os.path.exists(count):
            with open(count) as handle:
                seen = int(handle.read().strip() or 0)
        with open(count, "w") as handle:
            handle.write(str(seen + 1) + "\n")
    except OSError:
        return 4
    mode = None
    try:
        with open(state_path) as handle:
            mode = json.load(handle).get("mode")
    except (OSError, ValueError):
        mode = None
    envelope = {"schema": SCHEMA, "status": "PASS", "event_id": event,
                "auditor_role": role, "attempt_id": attempt,
                "samples": live_samples(mode)}
    if mode == "hang":
        time.sleep(600)
        return 0
    if mode == "empty-output":
        return 0
    if mode == "exit-nonzero":
        print(json.dumps(envelope))
        return 3
    if mode == "oversized":
        sys.stdout.write("X" * 70000)
        return 0
    if mode == "malformed":
        sys.stdout.write('{"schema": "x" this is not json')
        return 0
    if mode == "dup-key":
        sys.stdout.write(
            '{"schema":"x","schema":"' + SCHEMA + '","status":"PASS",'
            '"event_id":"' + event + '","auditor_role":"' + role +
            '","attempt_id":"' + attempt + '","samples":[]}')
        return 0
    if mode == "fail-state":
        envelope["status"] = "FAIL"         # live condition turned bad
    elif mode == "fail-status":
        envelope["status"] = "FAIL"         # top-level FAIL outright
    elif mode == "sample-fail":
        envelope["samples"][0]["status"] = "FAIL"   # under top-level PASS
    elif mode == "wrong-schema":
        envelope["schema"] = "AUCDEV-023-RESOURCE-GATE-RESULT-V0"
    elif mode == "wrong-event":
        envelope["event_id"] = "evt-ffffffffffffffff"
    elif mode == "wrong-role":
        envelope["auditor_role"] = ("AUDITOR_B" if role != "AUDITOR_B"
                                    else "AUDITOR_A")
    elif mode == "wrong-attempt":
        envelope["attempt_id"] = attempt + "-x"
    elif mode == "sample-count-2":
        envelope["samples"] = envelope["samples"][:2]
    elif mode == "sample-count-4":
        envelope["samples"] = envelope["samples"] + [
            dict(envelope["samples"][0])]
    print(json.dumps(envelope))
    return 0


if __name__ == "__main__":
    sys.exit(main())
