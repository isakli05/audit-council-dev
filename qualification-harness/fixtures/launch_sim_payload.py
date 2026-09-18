#!/usr/bin/env python3
"""Protected local launch simulation payload — the zero-provider launch
the one-shot grant is CONSUMED for.  Writes the launch marker into the
authorized auditor-output role, reads evidence, confirms custody
material reached the authorized child path, and reports.  Deterministic;
never contacts any provider."""
from __future__ import annotations

import json
import os
import sys

CUSTODY_PATH = "/tmp/qh-custody/inert-credential"
MARKER = "/auditor-output/launch-sim-marker.txt"


def main() -> int:
    args = sys.argv[1:]
    result_file = args[args.index("--result-file") + 1]
    ok = True
    detail: dict = {}
    try:
        with open(MARKER, "w", encoding="utf-8") as fh:
            fh.write("qh-protected-launch-simulation\n")
        detail["marker"] = MARKER
    except OSError as exc:
        ok = False
        detail["marker_error"] = repr(exc)
    try:
        with open("/evidence/evidence.md", "rb") as fh:
            detail["evidence_len"] = len(fh.read())
    except OSError as exc:
        ok = False
        detail["evidence_error"] = repr(exc)
    detail["custody_file_present"] = os.path.isfile(CUSTODY_PATH)
    if not detail["custody_file_present"]:
        ok = False
    record = {"phase": "payload_result", "kind": "launch_sim",
              "ok": ok, **detail}
    with open(result_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    return 0 if ok else 4


if __name__ == "__main__":
    sys.exit(main())
