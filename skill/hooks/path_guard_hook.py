#!/usr/bin/env python3
"""Claude Code PreToolUse hook: deny-before-exec path confinement (A0.4).

Reads one JSON object from stdin: {"tool_name": str, "tool_input": dict}
(extra keys such as hook_event_name are ignored). Behavior:

  - No active run registered under <cache_root()>/active-runs/ -> exit 0
    with no output (zero impact on normal sessions).
  - Active runs: each <active-runs>/<run-id> FILE contains the run dir
    path; the run's 01-environment-binding.json is loaded (digest-checked)
    and every tool call is validated with path_guard.check_tool_call.
    Allowed -> exit 0. Denied -> exit 2 with the reason on stderr
    (exit 2 = block in Claude Code hook semantics).
  - With MULTIPLE active runs the most restrictive policy wins: a call is
    allowed only if it violates no active binding.
  - Malformed stdin, unreadable/tampered bindings, or any unexpected
    error -> exit 2 (fail-closed).

cache_root() honors AUDIT_COUNCIL_CACHE_HOME -> ${XDG_CACHE_HOME:-~/.cache}
/audit-council/ (env_binding.cache_root). Deterministic, stdlib only.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

_HOOK_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _HOOK_DIR.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import env_binding  # noqa: E402
import path_guard  # noqa: E402


def _active_run_dirs(cache: str) -> list[str]:
    """Run dir paths registered under <cache>/active-runs/<run-id> files."""
    active = os.path.join(cache, "active-runs")
    if not os.path.isdir(active):
        return []
    runs: list[str] = []
    for name in sorted(os.listdir(active)):
        entry = os.path.join(active, name)
        if not os.path.isfile(entry):
            continue
        try:
            with open(entry, "r", encoding="utf-8") as fh:
                runs.append(fh.read().strip())
        except OSError:
            runs.append("")  # unreadable registration: fail closed
    return runs


def _load_binding(run_dir: str) -> dict[str, Any]:
    if not run_dir or not os.path.isdir(run_dir):
        raise env_binding.EnvironmentBindingError(
            "ACTIVE_RUN_UNREADABLE", {"run_dir": run_dir or "<empty>"})
    path = os.path.join(run_dir, env_binding.BINDING_NAME)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            binding = json.load(fh)
    except (OSError, ValueError) as exc:
        raise env_binding.EnvironmentBindingError(
            "BINDING_UNREADABLE", {"path": path, "error": str(exc)}) from None
    if not isinstance(binding, dict):
        raise env_binding.EnvironmentBindingError("BINDING_UNREADABLE",
                                                  {"path": path})
    if env_binding.digest(binding) != binding.get("binding_digest"):
        raise env_binding.EnvironmentBindingError("BINDING_DIGEST_MISMATCH",
                                                  {"path": path})
    if not isinstance(binding.get("repo_root_realpath"), str) \
            or not isinstance(binding.get("allowed_disposable_roots"), list):
        raise env_binding.EnvironmentBindingError("BINDING_UNREADABLE",
                                                  {"path": path})
    return binding


def process(doc: Any) -> tuple[int, str | None]:
    """Decide one hook document. Returns (exit_code, stderr_message)."""
    if not isinstance(doc, dict):
        return 2, "malformed hook input: expected a JSON object"
    tool = doc.get("tool_name")
    tool_input = doc.get("tool_input")
    if not isinstance(tool, str) or not isinstance(tool_input, dict):
        return 2, ("malformed hook input: tool_name (str) and tool_input "
                   "(object) are required")
    runs = _active_run_dirs(env_binding.cache_root())
    if not runs:
        return 0, None  # no active audit run: zero impact
    try:
        for run_dir in runs:
            binding = _load_binding(run_dir)
            ok, reason = path_guard.check_tool_call(
                tool, tool_input, binding["repo_root_realpath"],
                binding["allowed_disposable_roots"])
            if not ok:
                return 2, reason
    except env_binding.EnvironmentBindingError as exc:
        return 2, exc.reason
    except Exception as exc:  # never crash open: fail closed
        return 2, f"path_guard_hook failure: {exc!r}"
    return 0, None


def main(argv: list[str] | None = None) -> int:
    raw = sys.stdin.read()
    try:
        doc = json.loads(raw)
    except ValueError:
        print("path_guard_hook: malformed stdin JSON", file=sys.stderr)
        return 2
    code, message = process(doc)
    if message:
        print(f"path_guard_hook: {message}", file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
