#!/usr/bin/python3
"""EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER synthetic
structural output validator (S1-007 final execution-lifecycle
remediation).

Unmistakably synthetic/inert LOCAL stand-in for the future REAL frozen
first-pass structural validator (which will be materialized during the
separately authorized S1 event-package preparation).  It performs NO
network access, contains NO audit-substance logic, and is driven ONLY
by the sealed read-only report snapshot inherited at fd 3 plus the
frozen non-secret argv context the EBS binds (identity, event, role,
attempt, output name, report sha256, report size).  Its behavior is
additionally driven by an EXTERNAL /tmp state file keyed by attempt id
(absent = honest PASS), so the SAME frozen artifact PASSes or FAILs
deterministically per test.  It is NOT qualification-harness code, NOT
the Audit Council, and NEVER a provider client.
"""
import hashlib
import json
import os
import sys
import time

MARKER = "EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER"
SCHEMA = "AUCDEV-023-REPORT-VALIDATOR-RESULT-V1"
STATE_BASE = "/tmp/aucdev023-val-state-"


def read_fd(fd):
    data = b""
    while True:
        chunk = os.read(fd, 65536)
        if not chunk:
            break
        data += chunk
    return data


def main() -> int:
    # shebang semantics: the kernel replaces the exec argv[0] (the bound
    # descriptor identity) with the interpreter, so the script sees
    # [script, event, role, attempt, output_name, sha, size]
    event_id, role, attempt_id, output_name, sha, size = sys.argv[1:7]
    # In-fixture fail-closed proof that the validator NEVER inherits the
    # sealed credential custody (or any EBS-held execution fd): any
    # ebs-credential-custody / ebs-auditor-invocation memfd in our fd
    # table is a leak and refuses execution.
    for entry in os.listdir("/proc/self/fd"):
        try:
            target = os.readlink(f"/proc/self/fd/{entry}")
        except OSError:
            continue
        if "ebs-credential-custody" in target or \
                "ebs-auditor-invocation" in target:
            return 4
    state_path = STATE_BASE + attempt_id + ".json"
    mode = "pass"
    if os.path.exists(state_path):
        with open(state_path) as handle:
            mode = json.load(handle).get("mode", "pass")
    if mode == "hang":
        time.sleep(600)                     # never returns on its own
    snapshot = read_fd(3)                   # the sealed immutable report
    result = {
        "schema": SCHEMA,
        "status": "FAIL",
        "event_id": event_id,
        "auditor_role": role,
        "attempt_id": attempt_id,
        "output_name": output_name,
        "report_sha256": hashlib.sha256(snapshot).hexdigest(),
        "report_size": len(snapshot),
    }
    if mode == "mismatch-sha":
        result["report_sha256"] = "f" * 64
    if mode == "mismatch-size":
        result["report_size"] = len(snapshot) + 1
    if mode == "wrong-context":
        result["event_id"] = "evt-ffffffffffffffff"
    if mode in ("pass", "mismatch-sha", "mismatch-size", "wrong-context"):
        honest = (result["report_sha256"] == sha
                  and result["report_size"] == int(size)
                  and result["event_id"] == event_id)
        result["status"] = "PASS" if honest and mode == "pass" else "FAIL"
    if mode == "malformed":
        sys.stdout.write("this is not json\n")
        return 0
    sys.stdout.write(json.dumps(result) + "\n")
    if mode == "nonzero":
        return 3
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
