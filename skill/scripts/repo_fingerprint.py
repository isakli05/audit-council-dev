#!/usr/bin/env python3
"""Repository fingerprint capture/verify for audit-council.

Library + CLI (`capture --repo R` / `verify --repo R --state FILE`).
Read-only with respect to the repository: only git plumbing queries are run;
nothing is ever mutated, reset, committed, or deleted.

Material-change rule (CONTRACTS.md): any tracked-file sha/mode change, any
HEAD/branch change, tracked-file add/remove, porcelain status change for a
tracked path, or untracked file appearing/disappearing outside `audit-output/`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from state_store import atomic_write_json, load_json, sha256_bytes, utc_now_iso

EXCLUDED_PREFIX = "audit-output/"  # excluded from change detection
FINGERPRINT_VERSION = 1


class FingerprintError(Exception):
    pass


def _git(repo: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, timeout=60, check=False)


def _is_git_worktree(repo: str) -> bool:
    return _git(repo, "rev-parse", "--git-dir").returncode == 0


def _tool_version(argv: list[str]) -> str | None:
    """Best-effort first line of `argv --version`. Never raises."""
    try:
        proc = subprocess.run(argv + ["--version"], capture_output=True,
                              text=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    line = (proc.stdout or proc.stderr).strip().splitlines()
    return line[0] if line else None


def tool_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for name, argv in (
        ("git", ["git"]),
        ("codex", ["codex"]),
        ("claude", ["claude"]),
    ):
        v = _tool_version(argv)
        if v:
            versions[name] = v
    return versions


def _parse_ls_files(out: str) -> dict[str, dict[str, str]]:
    """`git ls-files -s` lines: `<mode> <sha> <stage>\t<path>`."""
    tracked: dict[str, dict[str, str]] = {}
    for line in out.splitlines():
        if not line.strip():
            continue
        meta, _, path = line.partition("\t")
        parts = meta.split()
        if len(parts) < 3 or not path:
            continue
        mode, sha, _stage = parts[0], parts[1], parts[2]
        tracked[path] = {"mode": mode, "sha": sha}
    return tracked


def _parse_untracked(porcelain: str, repo: str) -> dict[str, int]:
    """Untracked entries from porcelain `??` lines: name+size only."""
    untracked: dict[str, int] = {}
    for line in porcelain.splitlines():
        if not line.startswith("?? "):
            continue
        path = line[3:].strip('"')
        if path.startswith(EXCLUDED_PREFIX):
            continue
        full = os.path.join(repo, path)
        try:
            size = os.lstat(full).st_size
        except OSError:
            size = -1
        untracked[path] = size
    return untracked


def capture(repo: str) -> dict[str, Any]:
    """Capture the fingerprint document for `repo` (never mutates the repo)."""
    repo = os.path.abspath(repo)
    if not _is_git_worktree(repo):
        raise FingerprintError(f"{repo} is not a git worktree")

    head = _git(repo, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise FingerprintError("repository has no HEAD commit (empty repo?)")
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    porcelain = _git(repo, "status", "--porcelain")
    lsfiles = _git(repo, "ls-files", "-s")
    if branch.returncode or porcelain.returncode or lsfiles.returncode:
        raise FingerprintError("git inventory commands failed")

    doc: dict[str, Any] = {
        "fingerprint_version": FINGERPRINT_VERSION,
        "captured_at": utc_now_iso(),
        "repo_root": repo,
        "head_sha": head.stdout.strip(),
        "branch": branch.stdout.strip(),
        "porcelain": porcelain.stdout,
        "tracked_inventory": _parse_ls_files(lsfiles.stdout),
        "untracked_inventory": _parse_untracked(porcelain.stdout, repo),
        "tool_versions": tool_versions(),
    }
    doc["fingerprint_sha256"] = fingerprint_digest(doc)
    return doc


def canonical_json(doc: Any) -> str:
    return json.dumps(doc, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def fingerprint_digest(doc: dict[str, Any]) -> str:
    body = {k: v for k, v in doc.items() if k != "fingerprint_sha256"}
    return sha256_bytes(canonical_json(body).encode("utf-8"))


def _tracked_porcelain_paths(porcelain: str) -> set[str]:
    paths = set()
    for line in porcelain.splitlines():
        if not line or line.startswith("?? "):
            continue
        path = line[3:].strip('"')
        if path.startswith(EXCLUDED_PREFIX):
            continue
        paths.add(path)
    return paths


def diff_fingerprints(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """Structured diff; empty lists + changed=False means match."""
    d: dict[str, Any] = {
        "changed": False,
        "head_sha": {"old": old.get("head_sha"), "new": new.get("head_sha")},
        "branch": {"old": old.get("branch"), "new": new.get("branch")},
        "changed_tracked": [],
        "added_tracked": [],
        "removed_tracked": [],
        "added_untracked": [],
        "removed_untracked": [],
        "porcelain_status_changes": [],
    }
    if old.get("head_sha") != new.get("head_sha"):
        d["changed"] = True
    if old.get("branch") != new.get("branch"):
        d["changed"] = True

    old_t = old.get("tracked_inventory", {})
    new_t = new.get("tracked_inventory", {})
    for path in sorted(set(old_t) | set(new_t)):
        if path.startswith(EXCLUDED_PREFIX):
            continue
        if path not in new_t:
            d["removed_tracked"].append(path)
        elif path not in old_t:
            d["added_tracked"].append(path)
        elif old_t[path] != new_t[path]:
            d["changed_tracked"].append(path)

    old_u = old.get("untracked_inventory", {})
    new_u = new.get("untracked_inventory", {})
    for path in sorted(set(old_u) | set(new_u)):
        if old_u.get(path) != new_u.get(path):
            if path not in old_u:
                d["added_untracked"].append(path)
            else:
                d["removed_untracked"].append(path)

    old_p = _tracked_porcelain_paths(old.get("porcelain", ""))
    new_p = _tracked_porcelain_paths(new.get("porcelain", ""))
    d["porcelain_status_changes"] = sorted(old_p ^ new_p)

    if any(d[k] for k in ("changed_tracked", "added_tracked", "removed_tracked",
                          "added_untracked", "removed_untracked",
                          "porcelain_status_changes")):
        d["changed"] = True
    return d


def verify(repo: str, state_file: str) -> tuple[bool, dict[str, Any]]:
    """Recompute the fingerprint and diff against the one stored in state_file.

    The state document either is a fingerprint document or contains one under
    the key `fingerprint` (the 01-repository-state.json shape).
    """
    stored = load_json(state_file)
    if isinstance(stored, dict) and isinstance(stored.get("fingerprint"), dict):
        stored = stored["fingerprint"]
    if not isinstance(stored, dict) or "head_sha" not in stored:
        raise FingerprintError(f"{state_file} contains no fingerprint document")
    fresh = capture(repo)
    diff = diff_fingerprints(stored, fresh)
    return (not diff["changed"]), diff


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _cli() -> int:
    ap = argparse.ArgumentParser(prog="repo_fingerprint")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("capture", help="capture fingerprint to stdout")
    c.add_argument("--repo", required=True)
    c.add_argument("--out", help="optional output file (atomic write)")

    v = sub.add_parser("verify", help="verify repo vs stored fingerprint")
    v.add_argument("--repo", required=True)
    v.add_argument("--state", required=True)

    args = ap.parse_args()
    try:
        if args.cmd == "capture":
            doc = capture(args.repo)
            text = json.dumps(doc, indent=2, ensure_ascii=False)
            if args.out:
                atomic_write_json(args.out, doc)
                print(args.out)
            else:
                print(text)
            return 0
        if args.cmd == "verify":
            ok, diff = verify(args.repo, args.state)
            diff["ok"] = ok
            print(json.dumps(diff, indent=2, ensure_ascii=False))
            return 0 if ok else 4
    except FingerprintError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(_cli())
