#!/usr/bin/env python3
"""Repository fingerprint capture/verify for audit-council.

Library + CLI (`capture --repo R` / `verify --repo R --state FILE`
/ `identity-manifest --repo R [--out F]`). Read-only with respect to the
repository: only git plumbing queries are run; nothing is ever mutated,
reset, committed, or deleted.

Material-change rule (CONTRACTS.md): any tracked-file sha/mode change, any
HEAD/branch change, tracked-file add/remove, porcelain status change for a
tracked path, or untracked file appearing/disappearing outside `audit-output/`.

Fingerprint v2 (F-A-08/B-004): the untracked inventory is captured with
`git status --porcelain -uall` (no untracked-directory collapse: every file
is its own entry) and each entry carries the CONTENT sha256 of the file (a
same-size byte replacement can no longer evade freshness detection); every
tracked path that porcelain flags as dirty additionally records the sha256
of its current WORKING-TREE bytes, so material tracked byte changes drift
the fingerprint even when the git index blob sha is unchanged. `diff_fingerprints`
normalizes v1-era documents (untracked entries that are bare integers) so
historical fingerprints still compare by what they recorded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from state_store import atomic_write_json, load_json, sha256_bytes, \
    sha256_file, utc_now_iso

EXCLUDED_PREFIX = "audit-output/"  # excluded from change detection
FINGERPRINT_VERSION = 2


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


def _untracked_entry(repo: str, path: str) -> dict[str, Any]:
    """Content-aware untracked entry (F-A-08/B-004): size + sha256 of the
    file's bytes (a same-size replacement changes the digest); symlinks and
    special objects record their kind/target instead of being read."""
    full = os.path.join(repo, path)
    entry: dict[str, Any] = {"path": path}
    try:
        st = os.lstat(full)
    except OSError:
        return {"path": path, "kind": "unlstatable", "size": -1}
    entry["size"] = st.st_size
    import stat as _stat
    if _stat.S_ISLNK(st.st_mode):
        entry["kind"] = "symlink"
        try:
            entry["target"] = os.readlink(full)
        except OSError:
            entry["target"] = None
    elif _stat.S_ISREG(st.st_mode):
        entry["kind"] = "file"
        try:
            entry["sha256"] = sha256_file(full)
        except OSError:
            entry["sha256"] = None
    else:
        entry["kind"] = "special"
    return entry


def _parse_untracked(porcelain: str, repo: str) -> dict[str, Any]:
    """Untracked entries from porcelain -uall `??` lines: per-FILE,
    content-addressed (no untracked-directory collapse)."""
    untracked: dict[str, Any] = {}
    for line in porcelain.splitlines():
        if not line.startswith("?? "):
            continue
        path = line[3:].strip('"')
        if path.startswith(EXCLUDED_PREFIX):
            continue
        untracked[path] = _untracked_entry(repo, path)
    return untracked


def _dirty_worktree_bytes(porcelain: str, repo: str) -> dict[str, str]:
    """sha256 of the CURRENT working-tree bytes of every tracked path
    porcelain flags (F-A-08/B-004): a dirty file's byte edits drift the
    fingerprint even when the git index blob sha is unchanged. Deleted
    paths (D) are skipped — the porcelain change itself already drifts."""
    dirty: dict[str, str] = {}
    for line in porcelain.splitlines():
        if not line or line.startswith("?? "):
            continue
        path = line[3:].strip('"')
        if path.startswith(EXCLUDED_PREFIX):
            continue
        full = os.path.join(repo, path)
        try:
            if os.path.isfile(full) and not os.path.islink(full):
                dirty[path] = sha256_file(full)
        except OSError:
            continue
    return dirty


def capture(repo: str) -> dict[str, Any]:
    """Capture the fingerprint document for `repo` (never mutates the repo)."""
    repo = os.path.abspath(repo)
    if not _is_git_worktree(repo):
        raise FingerprintError(f"{repo} is not a git worktree")

    head = _git(repo, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise FingerprintError("repository has no HEAD commit (empty repo?)")
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    porcelain = _git(repo, "status", "--porcelain", "-uall")
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
        "dirty_worktree": _dirty_worktree_bytes(porcelain.stdout, repo),
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


def _untracked_equal(old_entry: Any, new_entry: Any) -> bool:
    """Cross-version equality for untracked inventory entries: v1
    documents recorded a bare integer size; v2 records a content-addressed
    object. A v1 integer compares only by size (v1 recorded nothing else —
    historical fingerprints verify by exactly what they captured, never
    more); v2 objects compare by full content (size + sha256 + kind)."""
    if isinstance(old_entry, int) or isinstance(new_entry, int):
        old_size = old_entry if isinstance(old_entry, int) \
            else old_entry.get("size")
        new_size = new_entry if isinstance(new_entry, int) \
            else new_entry.get("size")
        return old_size == new_size
    return _untracked_key(old_entry) == _untracked_key(new_entry)


def _untracked_key(entry: Any) -> Any:
    """Comparison key for a v2 untracked inventory entry (the content
    fields without the path key)."""
    if isinstance(entry, dict):
        return {k: v for k, v in entry.items() if k != "path"}
    return entry


def diff_fingerprints(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """Structured diff; empty lists + changed=False means match."""
    d: dict[str, Any] = {
        "changed": False,
        "head_sha": {"old": old.get("head_sha"), "new": new.get("head_sha")},
        "branch": {"old": old.get("branch"), "new": new.get("branch")},
        "changed_tracked": [],
        "added_tracked": [],
        "removed_tracked": [],
        "changed_untracked": [],
        "added_untracked": [],
        "removed_untracked": [],
        "changed_dirty_worktree": [],
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
        if path not in old_u:
            d["added_untracked"].append(path)
        elif path not in new_u:
            d["removed_untracked"].append(path)
        elif not _untracked_equal(old_u[path], new_u[path]):
            d["changed_untracked"].append(path)

    # F-A-08/B-004: dirty tracked working-tree byte changes must drift the
    # fingerprint even when the index blob sha is unchanged
    old_d = old.get("dirty_worktree", {})
    new_d = new.get("dirty_worktree", {})
    for path in sorted(set(old_d) | set(new_d)):
        if old_d.get(path) != new_d.get(path):
            d["changed_dirty_worktree"].append(path)

    old_p = _tracked_porcelain_paths(old.get("porcelain", ""))
    new_p = _tracked_porcelain_paths(new.get("porcelain", ""))
    d["porcelain_status_changes"] = sorted(old_p ^ new_p)

    if any(d[k] for k in ("changed_tracked", "added_tracked", "removed_tracked",
                          "changed_untracked", "added_untracked",
                          "removed_untracked", "changed_dirty_worktree",
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
# Full-target identity manifest (F-A-11 / B-007)
# ---------------------------------------------------------------------------
def identity_manifest(repo: str) -> dict[str, Any]:
    """Complete, files-only-verifiable target identity.

    The binding-v2 lesson: blind product evidence and full-target identity
    proof are separate concerns. This manifest gives an auditor who receives
    ONLY the target's files everything needed to complete mandatory identity
    work without inaccessible repository state:

      - `head_sha` / `tree_sha`: the git identity (trust-anchored to the
        frozen binding/transport, as in binding v2);
      - `tracked`: one entry per `git ls-files` path with the COMMIT blob
        sha AND the sha256 of the current working-tree BYTES — recomputable
        from the handed-off files alone;
      - `untracked_digest`: sha256 over the canonicalized v2 untracked
        inventory (content-addressed);
      - `file_count` / `total_bytes`: fast cross-checks.

    Deterministic: two invocations on an unchanged tree produce identical
    documents except `generated_at`.
    """
    repo = os.path.abspath(repo)
    if not _is_git_worktree(repo):
        raise FingerprintError(f"{repo} is not a git worktree")
    head = _git(repo, "rev-parse", "HEAD")
    tree = _git(repo, "rev-parse", "HEAD^{tree}")
    porcelain = _git(repo, "status", "--porcelain", "-uall")
    lsfiles = _git(repo, "ls-files", "-s")
    if head.returncode or tree.returncode or porcelain.returncode \
            or lsfiles.returncode:
        raise FingerprintError("git inventory commands failed")
    tracked: dict[str, dict[str, Any]] = {}
    total_bytes = 0
    for path, meta in sorted(_parse_ls_files(lsfiles.stdout).items()):
        entry = {"mode": meta["mode"], "blob_sha": meta["sha"]}
        full = os.path.join(repo, path)
        try:
            if os.path.isfile(full) and not os.path.islink(full):
                entry["worktree_sha256"] = sha256_file(full)
                total_bytes += os.path.getsize(full)
            elif os.path.islink(full):
                entry["worktree_sha256"] = None
                entry["kind"] = "symlink"
            else:
                entry["worktree_sha256"] = None
        except OSError:
            entry["worktree_sha256"] = None
        tracked[path] = entry
    untracked = _parse_untracked(porcelain.stdout, repo)
    doc: dict[str, Any] = {
        "manifest_kind": "audit-council-full-target-identity",
        "manifest_version": 1,
        "generated_at": utc_now_iso(),
        "repo_root": repo,
        "head_sha": head.stdout.strip(),
        "tree_sha": tree.stdout.strip(),
        "tracked": tracked,
        "tracked_count": len(tracked),
        "untracked_inventory": untracked,
        "untracked_digest": sha256_bytes(
            canonical_json(untracked).encode("utf-8")),
        "total_tracked_bytes": total_bytes,
    }
    doc["manifest_sha256"] = sha256_bytes(
        canonical_json({k: v for k, v in doc.items()
                        if k != "manifest_sha256"}).encode("utf-8"))
    return doc


def verify_files_against_manifest(files_root: str,
                                  manifest: dict[str, Any]) -> list[str]:
    """Recompute per-file sha256 for every tracked entry under `files_root`
    (a handed-off copy of the target) and report mismatches. This is the
    check an ISOLATED auditor can execute: no git objects, no repository
    state — only the handed-off bytes plus the manifest."""
    errors: list[str] = []
    tracked = manifest.get("tracked", {})
    if not tracked:
        return ["manifest has no tracked entries"]
    for path, entry in sorted(tracked.items()):
        expected = entry.get("worktree_sha256")
        if expected is None:
            continue  # symlink/unreadable at capture: not byte-checkable
        full = os.path.join(files_root, path)
        try:
            actual = sha256_file(full)
        except OSError:
            errors.append(f"{path}: missing or unreadable in handed-off "
                          f"files")
            continue
        if actual != expected:
            errors.append(f"{path}: sha256 mismatch (manifest "
                          f"{expected[:12]}…, files {actual[:12]}…)")
    return errors


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

    m = sub.add_parser(
        "identity-manifest",
        help="emit the full-target identity manifest (files-only "
             "verifiable: per-file blob sha + worktree sha256)")
    m.add_argument("--repo", required=True)
    m.add_argument("--out", help="optional output file (atomic write)")

    mv = sub.add_parser(
        "verify-manifest-files",
        help="recompute per-file sha256 under a handed-off files root and "
             "compare against an identity manifest (the isolated-auditor "
             "identity check)")
    mv.add_argument("--files-root", required=True)
    mv.add_argument("--manifest", required=True)

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
        if args.cmd == "identity-manifest":
            doc = identity_manifest(args.repo)
            if args.out:
                atomic_write_json(args.out, doc)
                print(args.out)
            else:
                print(json.dumps(doc, indent=2, ensure_ascii=False))
            return 0
        if args.cmd == "verify-manifest-files":
            errors = verify_files_against_manifest(
                args.files_root, load_json(args.manifest))
            print(json.dumps({"ok": not errors, "errors": errors},
                             indent=2, ensure_ascii=False))
            return 0 if not errors else 4
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
