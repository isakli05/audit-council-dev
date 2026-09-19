#!/usr/bin/python3
"""EBS-INERT-SYNTHETIC-BOUNDARY-FIXTURE-NOT-A-PROVIDER runtime network
readiness gate (S1-002 preexec-gate remediation).

Unmistakably synthetic/inert LOCAL fixture for the AUCDEV-023 EBS
zero-provider battery.  It performs NO network access of ANY kind — no
socket, no DNS resolution, no route lookup, no provider endpoint policy:
it stands in for the FUTURE event-package-side NETWORK_READINESS artifact
(the real one is built later, under the separately authorized S1
event-package preparation, and its design obligation is a NON-INFERENCE
route/resolver preflight).  Behavior modes come from an EXTERNAL
attempt-keyed /tmp state file (absent = honest PASS), never from package
bytes: the SAME frozen artifact PASSes or FAILs on state sampled at
EXECUTION time.  The gate writes an attempt-keyed sentinel + counter under
/tmp so tests can prove WHETHER, HOW OFTEN, and (with the resource gate's
own tracks) IN WHICH ORDER the EBS executed it.

argv contract (bound by the EBS to this attempt's non-secret binding
facts): identity, event_id, auditor_role, attempt_id, provider_role,
boundary_launcher_sha256, sandbox_profile_id.
"""
import json
import os
import sys
import time

SCHEMA = "AUCDEV-023-NETWORK-READINESS-RESULT-V1"
BASE = "/tmp/aucdev023-nr-"


def paths(attempt):
    return (BASE + "state-" + attempt + ".json",
            BASE + "sentinel-" + attempt,
            BASE + "count-" + attempt)


def envelope(event, role, attempt, provider, launcher_sha, profile):
    """The strict result envelope; every detail is honestly synthetic/inert
    local state (no network was touched to produce it)."""
    return {"schema": SCHEMA, "status": "PASS", "event_id": event,
            "auditor_role": role, "attempt_id": attempt,
            "provider_role": provider,
            "boundary_launcher_sha256": launcher_sha,
            "sandbox_profile_id": profile,
            "checks": {
                "route": {"status": "PASS",
                          "detail": {"synthetic_inert": True,
                                     "sampled": "external-live-state"}},
                "resolver": {"status": "PASS",
                             "detail": {"synthetic_inert": True,
                                        "sampled": "external-live-state"}}}}


def main():
    if len(sys.argv) != 7:
        return 3
    (event, role, attempt, provider, launcher_sha,
     profile) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                 sys.argv[5], sys.argv[6])
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
    env = envelope(event, role, attempt, provider, launcher_sha, profile)
    if mode == "hang":
        time.sleep(600)
        return 0
    if mode == "empty-output":
        return 0
    if mode == "exit-nonzero":
        print(json.dumps(env))
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
            '","attempt_id":"' + attempt + '","provider_role":"' +
            provider + '","boundary_launcher_sha256":"' + launcher_sha +
            '","sandbox_profile_id":"' + profile + '","checks":{}}')
        return 0
    if mode == "fail-status":
        env["status"] = "FAIL"               # top-level FAIL outright
    elif mode == "route-fail":
        env["checks"]["route"]["status"] = "FAIL"   # under top-level PASS
    elif mode == "resolver-fail":
        env["checks"]["resolver"]["status"] = "FAIL"
    elif mode == "check-missing":
        del env["checks"]["resolver"]        # not the exact key set
    elif mode == "check-extra":
        env["checks"]["dns"] = dict(env["checks"]["route"])
    elif mode == "check-status-nonpass":
        env["checks"]["route"]["status"] = "WARN"
    elif mode == "detail-not-object":
        env["checks"]["route"]["detail"] = "a string is not an object"
    elif mode == "detail-missing":
        env["checks"]["route"].pop("detail")
    elif mode == "wrong-schema":
        env["schema"] = "AUCDEV-023-NETWORK-READINESS-RESULT-V0"
    elif mode == "wrong-event":
        env["event_id"] = "evt-ffffffffffffffff"
    elif mode == "wrong-role":
        env["auditor_role"] = ("AUDITOR_B" if role != "AUDITOR_B"
                               else "AUDITOR_A")
    elif mode == "wrong-attempt":
        env["attempt_id"] = attempt + "-x"
    elif mode == "wrong-provider":
        env["provider_role"] = "MYSTERY-PROVIDER"
    elif mode == "wrong-launcher-sha":
        env["boundary_launcher_sha256"] = "f" * 64
    elif mode == "wrong-profile":
        env["sandbox_profile_id"] = "SYNTHETIC-INERT-OTHER-SANDBOX"
    print(json.dumps(env))
    return 0


if __name__ == "__main__":
    sys.exit(main())
