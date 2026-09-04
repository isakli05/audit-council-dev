#!/usr/bin/env python3
"""Mechanical root confinement for audit-council v2 (PKG-A0 Task A0.3).

Pure path mechanics — no inference, no model calls. Every referenced path
is canonicalized (realpath) and must sit component-wise inside the frozen
worktree root or one of the authorized disposable roots. Bash commands are
SEGMENTED (&&, ||, ;, |, newlines, subshells, command substitution) and
every segment is validated, so ordinary in-root compound usage stays
allowed while any single escaping segment denies the whole command.

Fail-closed: ambiguous or unparseable shell input is denied with
PATH_ESCAPE_ATTEMPT. Reason codes come from the §3.4.2 taxonomy:

  PATH_ESCAPE_ATTEMPT      generic outside-root reference / unparseable
  CWD_OUTSIDE_FROZEN_ROOT   Bash cwd or `cd` segment escapes the root
  UNAUTHORIZED_TMP_ACCESS  /tmp (or /var/tmp) path outside allowed roots
  SYMLINK_ESCAPE           lexically inside a root, realpath outside it
  ALTERNATE_WORKTREE_ACCESS  a DIFFERENT worktree of the SAME repository
"""
from __future__ import annotations

import os
import re
import shlex
import subprocess
from typing import Any

import env_binding

TOOLS = ("Read", "Grep", "Glob", "Bash")
_MAX_DEPTH = 16
_SUBST_PLACEHOLDER = "SUBSTITUTEDTEXT"
_PATH_PREFIXES = ("./", "../", "~/")
_REDIRECTION_RE = re.compile(r"^(?:\d*)>>|^(?:\d*)>|^(?:\d*)<<|^(?:\d*)<")
_ENV_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"
                     r"|\$([A-Za-z_][A-Za-z0-9_]*)")
# args whose following value is always treated as a path
_PATH_ARG_FLAGS = {"-C", "--git-dir", "--work-tree", "--exec-path"}


# ---------------------------------------------------------------------------
# Canonicalization / containment
# ---------------------------------------------------------------------------
def canonicalize(path: str) -> str:
    """realpath-resolved absolute form of `path`."""
    return os.path.realpath(os.path.abspath(path))


def _within(path: str, root: str) -> bool:
    """Component-wise containment of canonical `path` in canonical `root`."""
    if root == os.sep:
        return path == os.sep or path.startswith(os.sep)
    return path == root or path.startswith(root + os.sep)


def is_within(path: str, root: str) -> bool:
    """True iff canonicalize(path) == canonicalize(root) or lies beneath it
    (component-wise — NEVER a raw string prefix match)."""
    return _within(canonicalize(path), canonicalize(root))


# ---------------------------------------------------------------------------
# Environment-variable expansion (conservative)
# ---------------------------------------------------------------------------
def _expand_env(token: str) -> tuple[bool, str]:
    """Expand $NAME / ${NAME} via os.environ.

    Returns (fully_resolved, expanded). Any unresolved variable leaves a
    literal `$...` behind, so fully_resolved is False (the caller treats
    such path-shaped tokens as UNKNOWN and denies them — fail-closed).
    """
    def sub(match: re.Match[str]) -> str:
        name = match.group(1) or match.group(2)
        return os.environ.get(name, match.group(0))

    expanded = _ENV_RE.sub(sub, token)
    return ("$" not in expanded, expanded)


def _looks_like_path(candidate: str) -> bool:
    if not candidate:
        return False
    if candidate.startswith("/") or candidate.startswith(_PATH_PREFIXES):
        return True
    if "/" in candidate:
        return True
    return candidate in (".", "..")


def _token_candidates(token: str) -> list[str]:
    """Path-bearing substrings of a shell word: the bare word, the value
    side of KEY=VALUE, and redirection targets (> f, 2>> f, < f, ...)."""
    candidates: list[str] = []
    body = token
    match = _REDIRECTION_RE.match(body)
    if match:
        body = body[match.end():]
    if "=" in body and not body.startswith("-"):
        _, _, value = body.partition("=")
        if value:
            candidates.append(value)
    candidates.append(body)
    return [c for c in candidates if c]


# ---------------------------------------------------------------------------
# Alternate-worktree detection (git plumbing only)
# ---------------------------------------------------------------------------
_FROZEN_COMMON_DIR_CACHE: dict[str, str | None] = {}


def _git_common_dir_of(root: str) -> str | None:
    if root in _FROZEN_COMMON_DIR_CACHE:
        return _FROZEN_COMMON_DIR_CACHE[root]
    proc = subprocess.run(
        ["git", "-C", root, "rev-parse", "--git-common-dir"],
        capture_output=True, text=True, timeout=30, check=False)
    common: str | None = None
    if proc.returncode == 0 and proc.stdout.strip():
        out = proc.stdout.strip()
        if not os.path.isabs(out):
            out = os.path.join(root, out)
        common = os.path.realpath(out)
    _FROZEN_COMMON_DIR_CACHE[root] = common
    return common


def _nearest_existing_dir(path: str) -> str | None:
    current = path
    while True:
        if os.path.isdir(current):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def _alternate_worktree(canonical_path: str, frozen_root: str) -> bool:
    """True when `canonical_path` sits inside a DIFFERENT worktree of the
    same repository as `frozen_root` (same git common dir, different
    toplevel) — the same-HEAD alternate-worktree escape."""
    nearest = _nearest_existing_dir(canonical_path)
    if nearest is None:
        return False
    try:
        toplevel = env_binding.repo_root_from(nearest)
    except env_binding.EnvironmentBindingError:
        return False
    if toplevel == frozen_root:
        return False
    frozen_common = _git_common_dir_of(frozen_root)
    path_common = _git_common_dir_of(toplevel)
    if frozen_common is None or path_common is None:
        return False
    return path_common == frozen_common


# ---------------------------------------------------------------------------
# Path classification
# ---------------------------------------------------------------------------
def _classify_path(candidate: str, cwd: str, frozen_root: str,
                   allowed_roots: list[str]) -> str | None:
    """Classify one path-shaped token; None means authorized."""
    if not candidate:
        return None
    resolved, expanded = _expand_env(candidate)
    if not resolved:
        # UNKNOWN env form: deny when path-shaped, ignore bare words
        return "PATH_ESCAPE_ATTEMPT" if _looks_like_path(candidate) else None
    path = expanded
    if path.startswith("~"):
        path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    lexical = os.path.normpath(path)        # no symlink resolution
    resolved_path = os.path.realpath(lexical)
    roots = [frozen_root, *allowed_roots]
    if any(_within(resolved_path, r) for r in roots):
        return None
    if any(_within(lexical, r) for r in roots):
        return "SYMLINK_ESCAPE"
    if resolved_path == "/tmp" or resolved_path.startswith("/tmp/") \
            or resolved_path == "/var/tmp" \
            or resolved_path.startswith("/var/tmp/"):
        return "UNAUTHORIZED_TMP_ACCESS"
    if _alternate_worktree(resolved_path, frozen_root):
        return "ALTERNATE_WORKTREE_ACCESS"
    return "PATH_ESCAPE_ATTEMPT"


# ---------------------------------------------------------------------------
# Bash command scanning
# ---------------------------------------------------------------------------
def scan_bash_command(cmd: str, cwd: str, frozen_root: str,
                      allowed_roots: list[str]) -> list[str]:
    """Segment and validate a Bash command; [] means authorized.

    Compound constructs (&&, ||, ;, |, newlines), subshells `( ... )` and
    command substitutions `$(...)` / backticks are split recursively and
    every segment's path-bearing tokens are validated; relative tokens
    resolve against the segment's effective cwd (tracked across `cd`).
    """
    reasons, _ = _scan_command_list(
        cmd, canonicalize(cwd), canonicalize(frozen_root),
        [canonicalize(r) for r in allowed_roots], depth=0)
    return reasons


def _dedupe(reasons: list[str]) -> list[str]:
    seen: set[str] = set()
    out = []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def _read_balanced(text: str, start: int) -> tuple[str | None, int]:
    """Read until the `)` matching an already-opened `(` at depth 1.
    Returns (inner, index_after_close) or (None, len(text))."""
    depth = 1
    i = start
    in_single = in_double = False
    while i < len(text):
        ch = text[i]
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "\\" and not in_single and i + 1 < len(text):
            i += 2
            continue
        elif not in_single and not in_double:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return text[start:i], i + 1
        i += 1
    return None, len(text)


def _replace_substitutions(text: str, cwd: str, frozen_root: str,
                           allowed_roots: list[str], depth: int
                           ) -> tuple[str, list[str]]:
    """Scan `$(...)` and backtick substitutions (recursively), replacing
    each with an inert placeholder word."""
    reasons: list[str] = []
    out: list[str] = []
    i = 0
    n = len(text)
    in_single = in_double = False
    while i < n:
        ch = text[i]
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
            i += 1
            continue
        if ch == "\\" and not in_single and i + 1 < n:
            out.append(text[i:i + 2])
            i += 2
            continue
        if not in_single and ch == "$" and i + 1 < n and text[i + 1] == "(":
            inner, after = _read_balanced(text, i + 2)
            if inner is None:  # unbalanced: ambiguous -> fail closed
                reasons.append("PATH_ESCAPE_ATTEMPT")
                out.append(_SUBST_PLACEHOLDER)
                i = n
                break
            sub_reasons, _ = _scan_command_list(inner, cwd, frozen_root,
                                                allowed_roots, depth + 1)
            reasons.extend(sub_reasons)
            out.append(_SUBST_PLACEHOLDER)
            i = after
            continue
        if not in_single and ch == "`":
            end = text.find("`", i + 1)
            if end == -1:  # unbalanced backtick: ambiguous -> fail closed
                reasons.append("PATH_ESCAPE_ATTEMPT")
                out.append(_SUBST_PLACEHOLDER)
                i = n
                break
            sub_reasons, _ = _scan_command_list(text[i + 1:end], cwd,
                                                frozen_root, allowed_roots,
                                                depth + 1)
            reasons.extend(sub_reasons)
            out.append(_SUBST_PLACEHOLDER)
            i = end + 1
            continue
        out.append(ch)
        i += 1
    return "".join(out), reasons


def _split_segments(text: str) -> tuple[list[tuple[str, str]] | None, bool]:
    """Split a substitution-free command string into top-level items.

    Items are ("cmd", simple_command_text) or ("sub", subshell_body).
    Returns (None, False) on ambiguous/unparseable structure.
    """
    items: list[tuple[str, str]] = []
    current: list[str] = []
    i = 0
    n = len(text)
    in_single = in_double = False
    while i < n:
        ch = text[i]
        if ch == "'" and not in_double:
            in_single = not in_single
            current.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            current.append(ch)
            i += 1
            continue
        if ch == "\\" and not in_single and i + 1 < n:
            current.append(text[i:i + 2])
            i += 2
            continue
        if not in_single and not in_double:
            pair = text[i:i + 2]
            if pair in ("&&", "||"):
                items.append(("cmd", "".join(current)))
                current = []
                i += 2
                continue
            if ch in (";", "|", "\n"):
                items.append(("cmd", "".join(current)))
                current = []
                i += 1
                continue
            if ch == "&":  # background separator only as a standalone word
                before = text[i - 1] if i > 0 else " "
                after = text[i + 1] if i + 1 < n else " "
                if before.isspace() and after.isspace():
                    items.append(("cmd", "".join(current)))
                    current = []
                    i += 1
                    continue
                current.append(ch)
                i += 1
                continue
            if ch == "(":
                if "".join(current).strip():
                    return None, False  # stray paren inside a word: ambiguous
                inner, after = _read_balanced(text, i + 1)
                if inner is None:
                    return None, False
                items.append(("sub", inner))
                i = after
                continue
            if ch == ")":
                return None, False  # unmatched close: ambiguous
        current.append(ch)
        i += 1
    if in_single or in_double:
        return None, False  # unbalanced quotes: shlex would fail anyway
    tail = "".join(current)
    if tail.strip():
        items.append(("cmd", tail))
    return items, True


def _scan_command_list(text: str, cwd: str, frozen_root: str,
                       allowed_roots: list[str], depth: int
                       ) -> tuple[list[str], str]:
    if depth > _MAX_DEPTH:
        return ["PATH_ESCAPE_ATTEMPT"], cwd
    reasons: list[str] = []
    replaced, subst_reasons = _replace_substitutions(
        text, cwd, frozen_root, allowed_roots, depth)
    reasons.extend(subst_reasons)
    items, ok = _split_segments(replaced)
    if not ok:
        reasons.append("PATH_ESCAPE_ATTEMPT")
        return _dedupe(reasons), cwd
    cur_cwd, prev_cwd = cwd, cwd
    for kind, body in items:
        if kind == "sub":
            sub_reasons, _ = _scan_command_list(body, cur_cwd, frozen_root,
                                                allowed_roots, depth + 1)
            reasons.extend(sub_reasons)
            continue
        seg_reasons, cur_cwd, prev_cwd = _scan_segment(
            body, cur_cwd, prev_cwd, frozen_root, allowed_roots)
        reasons.extend(seg_reasons)
    return _dedupe(reasons), cur_cwd


def _scan_segment(segment: str, cur_cwd: str, prev_cwd: str,
                  frozen_root: str, allowed_roots: list[str]
                  ) -> tuple[list[str], str, str]:
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        return ["PATH_ESCAPE_ATTEMPT"], cur_cwd, prev_cwd
    if not tokens:
        return [], cur_cwd, prev_cwd

    if tokens[0] in ("cd", "pushd"):
        return _scan_cd(tokens, cur_cwd, prev_cwd, frozen_root,
                        allowed_roots)

    reasons: list[str] = []
    for idx, token in enumerate(tokens):
        forced = idx > 0 and tokens[idx - 1] in _PATH_ARG_FLAGS
        for candidate in _token_candidates(token):
            if not forced and not _looks_like_path(candidate):
                continue
            reason = _classify_path(candidate, cur_cwd, frozen_root,
                                    allowed_roots)
            if reason:
                reasons.append(reason)
    return reasons, cur_cwd, prev_cwd


def _scan_cd(tokens: list[str], cur_cwd: str, prev_cwd: str,
             frozen_root: str, allowed_roots: list[str]
             ) -> tuple[list[str], str, str]:
    # first argument that is either the literal "-" (previous dir) or a
    # non-flag operand; cd flags like -L are skipped
    target = "~"  # bare cd (or flags only) goes to $HOME
    for token in tokens[1:]:
        if token == "-" or not token.startswith("-"):
            target = token
            break
    if target == "-":
        target_dir: str = prev_cwd
        candidate = target_dir
    else:
        candidate = target
    reason = _classify_path(candidate, cur_cwd, frozen_root, allowed_roots)
    if reason is None:
        resolved, expanded = _expand_env(candidate)
        path = expanded
        if path.startswith("~"):
            path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.join(cur_cwd, path)
        return [], os.path.realpath(path), cur_cwd
    # a cd segment IS a cwd change: report the cwd-specific reason unless
    # a more precise one applies (symlink / alternate worktree)
    if reason in ("SYMLINK_ESCAPE", "ALTERNATE_WORKTREE_ACCESS"):
        return [reason], cur_cwd, prev_cwd
    return ["CWD_OUTSIDE_FROZEN_ROOT"], cur_cwd, prev_cwd


# ---------------------------------------------------------------------------
# Tool-call checking
# ---------------------------------------------------------------------------
def check_tool_call(tool: str, tool_input: dict[str, Any],
                    frozen_root: str,
                    allowed_roots: list[str]) -> tuple[bool, str | None]:
    """Decide one tool call against the frozen root + allowed roots.

    Returns (True, None) when authorized, else (False, reason) with a
    §3.4.2 reason code. Unknown tools / malformed inputs are denied
    fail-closed with PATH_ESCAPE_ATTEMPT.
    """
    frozen = canonicalize(frozen_root)
    allowed = [canonicalize(r) for r in allowed_roots]
    if not isinstance(tool_input, dict):
        return (False, "PATH_ESCAPE_ATTEMPT")

    if tool == "Read":
        file_path = tool_input.get("file_path")
        if not isinstance(file_path, str) or not file_path:
            return (False, "PATH_ESCAPE_ATTEMPT")
        reason = _classify_path(file_path, os.getcwd(), frozen, allowed)
        return (True, None) if reason is None else (False, reason)

    if tool in ("Grep", "Glob"):
        # absent path defaults to the session cwd (in-root); when present
        # it must be confined like any other referenced path
        path = tool_input.get("path")
        if path is None:
            return (True, None)
        if not isinstance(path, str) or not path:
            return (False, "PATH_ESCAPE_ATTEMPT")
        reason = _classify_path(path, os.getcwd(), frozen, allowed)
        return (True, None) if reason is None else (False, reason)

    if tool == "Bash":
        command = tool_input.get("command")
        if not isinstance(command, str) or not command:
            return (False, "PATH_ESCAPE_ATTEMPT")
        cwd = tool_input.get("cwd")
        if cwd is None:
            cwd = frozen  # session cwd assumed to be the frozen root
        if not isinstance(cwd, str) or not cwd:
            return (False, "PATH_ESCAPE_ATTEMPT")
        cwd_canonical = canonicalize(cwd)
        if not any(_within(cwd_canonical, r)
                   for r in [frozen, *allowed]):
            return (False, "CWD_OUTSIDE_FROZEN_ROOT")
        reasons = scan_bash_command(command, cwd_canonical, frozen, allowed)
        if reasons:
            return (False, reasons[0])
        return (True, None)

    return (False, "PATH_ESCAPE_ATTEMPT")
