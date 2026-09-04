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

try:
    import env_binding  # noqa: E402
    import path_guard  # noqa: E402
    _GUARD_IMPORT_ERROR = None
except Exception as _exc:  # R4: guard modules damaged/unreadable — never
    # crash open (a bare import failure would exit 1 = NON-blocking in
    # Claude Code hook semantics); fall back to deny-everything
    _GUARD_IMPORT_ERROR = repr(_exc)
    env_binding = None  # type: ignore[assignment]
    path_guard = None  # type: ignore[assignment]


def _active_runs(cache: str) -> list[tuple[str, str]]:
    """(run_dir, pinned_binding_digest) registered under
    <cache>/active-runs/<run-id>. The registry lives OUTSIDE the frozen
    root — a confined session cannot rewrite the pin (R3-N3)."""
    active = os.path.join(cache, "active-runs")
    if not os.path.isdir(active):
        return []
    runs: list[tuple[str, str]] = []
    for name in sorted(os.listdir(active)):
        entry = os.path.join(active, name)
        if not os.path.isfile(entry):
            continue
        try:
            with open(entry, "r", encoding="utf-8") as fh:
                lines = fh.read().strip().splitlines()
        except OSError:
            runs.append(("", ""))  # unreadable registration: fail closed
            continue
        run_dir = lines[0].strip() if lines else ""
        pinned = lines[1].strip() if len(lines) > 1 else ""
        runs.append((run_dir, pinned))
    return runs


def _active_run_dirs(cache: str) -> list[str]:
    """Run-dir-only view (back-compat for tests)."""
    return [run_dir for run_dir, _ in _active_runs(cache)]


def _load_binding(run_dir: str,
                  pinned_digest: str | None = None) -> dict[str, Any]:
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
    # R3-N3: the registry-pinned digest anchors the policy source — an
    # in-root rewrite of the binding (even with a regenerated self-digest)
    # no longer widens the hook's allowlist
    if pinned_digest and binding.get("binding_digest") != pinned_digest:
        raise env_binding.EnvironmentBindingError(
            "BINDING_DIGEST_MISMATCH",
            {"path": path,
             "detail": "binding no longer matches the digest pinned in the "
                       "out-of-root active-run registry"})
    if not isinstance(binding.get("repo_root_realpath"), str) \
            or not isinstance(binding.get("allowed_disposable_roots"), list):
        raise env_binding.EnvironmentBindingError("BINDING_UNREADABLE",
                                                  {"path": path})
    return binding


def _cache_root_fallback() -> str:
    """cache_root() without env_binding (pure stdlib) — used when the guard
    modules are damaged so the no-active-run exemption still works."""
    override = os.environ.get("AUDIT_COUNCIL_CACHE_HOME")
    if override:
        return os.path.expanduser(override)
    base = os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
    return os.path.join(base, "audit-council")


def process(doc: Any) -> tuple[int, str | None]:
    """Decide one hook document. Returns (exit_code, stderr_message)."""
    if not isinstance(doc, dict):
        return 2, "malformed hook input: expected a JSON object"
    tool = doc.get("tool_name")
    tool_input = doc.get("tool_input")
    if not isinstance(tool, str) or not isinstance(tool_input, dict):
        return 2, ("malformed hook input: tool_name (str) and tool_input "
                   "(object) are required")
    cache = (env_binding.cache_root() if env_binding is not None
             else _cache_root_fallback())
    runs = _active_runs(cache)
    if not runs:
        return 0, None  # no active audit run: zero impact on any session
    if _GUARD_IMPORT_ERROR is not None or path_guard is None:
        # an ACTIVE run exists but the guard machinery is damaged: deny
        # everything rather than crash open (exit 1 = non-blocking)
        return 2, ("path guard unavailable "
                   f"({_GUARD_IMPORT_ERROR}); failing closed")
    try:
        for run_dir, pinned in runs:
            binding = _load_binding(run_dir, pinned_digest=pinned)
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
