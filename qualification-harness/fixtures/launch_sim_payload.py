#!/usr/bin/env python3
"""Protected local launch simulation payload — the zero-provider launch
the one-shot grant is CONSUMED for.  Writes the launch marker into the
authorized auditor-output role, reads evidence, confirms the SPEC-BOUND
provider-adapter custody materialization reached the authorized child
path with the expected mode, and proves the MODEL-COMMAND VIEW cannot see
the credential through the generated permission profile (no CODEX_HOME /
CLAUDE_CONFIG_DIR read entry exists).  Deterministic; never contacts any
provider; never prints credential VALUES (existence + length only)."""
from __future__ import annotations

import json
import os
import stat
import sys

MARKER = "/auditor-output/launch-sim-marker.txt"


def _verify_adapter(detail: dict) -> bool:
    adapter_id = os.environ.get("QH_ADAPTER_ID", "synthetic_inert_v1")
    target = os.environ.get(
        "QH_ADAPTER_TARGET", "/tmp/qh-custody/inert-credential")
    want_len = int(os.environ.get("QH_CUSTODY_LENGTH", "0"))
    want_mode = int(os.environ.get("QH_ADAPTER_MODE", "0o600"), 8)
    ok = True
    detail["adapter_id"] = adapter_id
    detail["adapter_target"] = target
    detail["custody_file_present"] = os.path.isfile(target)
    if not detail["custody_file_present"]:
        return False
    size = os.path.getsize(target)
    detail["custody_length"] = size
    if want_len and size != want_len:
        ok = False
        detail["custody_length_mismatch"] = True
    mode = stat.S_IMODE(os.stat(target).st_mode)
    detail["custody_mode"] = oct(mode)
    if mode != want_mode:
        ok = False
        detail["custody_mode_mismatch"] = True
    if adapter_id == "codex_chatgpt_oauth_v1":
        # provider-runtime simulation: the runtime READS its auth file
        try:
            with open(target, "rb") as fh:
                detail["provider_runtime_read_len"] = len(fh.read())
        except OSError as exc:
            ok = False
            detail["provider_runtime_read_error"] = repr(exc)
        # model-command view: the generated restricted permission profile
        # must grant NO read of the credential surface (auth is never a
        # permission entry — accepted G-2 semantics)
        home = os.environ.get("CODEX_HOME", "")
        cfg = os.path.join(home, "config.toml")
        try:
            with open(cfg, "r", encoding="utf-8") as fh:
                body = fh.read()
            leaked = (home in body) or "auth.json" in body or \
                '"CODEX_HOME"' in body
            detail["profile_grants_credential_read"] = leaked
            if leaked:
                ok = False
        except OSError as exc:
            ok = False
            detail["config_read_error"] = repr(exc)
    if adapter_id == "claude_firstparty_oauth_v1":
        home = os.environ.get("CLAUDE_CONFIG_DIR", "")
        detail["claude_config_dir_files"] = sorted(
            os.listdir(home)) if os.path.isdir(home) else None
    return ok


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
    if not _verify_adapter(detail):
        ok = False
    record = {"phase": "payload_result", "kind": "launch_sim",
              "ok": ok, **detail}
    with open(result_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    return 0 if ok else 4


if __name__ == "__main__":
    sys.exit(main())
