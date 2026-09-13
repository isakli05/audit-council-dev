#!/usr/bin/env python3
"""Environment binding freeze/verify for audit-council v2 (PKG-A0).

Implements AuditEnvironmentBinding (AUDIT-COUNCIL-V2-ARCHITECTURE §3.4.1):
an immutable identity of the audited git WORKTREE (not just its HEAD),
frozen before any inference and re-verified at lifecycle boundaries.

Identity rules:
  - `binding_digest` covers every field of the binding document EXCEPT
    `binding_digest` and `frozen_at` (freeze time is metadata); two captures
    with otherwise identical inputs produce identical digests.
  - HEAD alone is NOT identity: two worktrees at one commit differ by
    `worktree_identity` = sha256(git_dir_realpath + "\\n" + repo_root_realpath).
  - The repository fingerprint component is computed with the v1 digest
    algorithm over the v1 fingerprint document minus its `captured_at`
    timestamp, so the binding identity is time-independent.

All git facts come from plumbing (`git rev-parse`, `git config --get`);
there is no `.git`-directory sniffing anywhere in this module (pre-freeze
clarification 2).
"""
from __future__ import annotations

import json
import os
import subprocess
from typing import Any

import repo_fingerprint
from state_store import load_json, sha256_bytes, sha256_file, utc_now_iso

BINDING_VERSION = 2
BINDING_NAME = "01-environment-binding.json"
BRIEF_MATERIALISED_NAME = os.path.join("inputs", "original-audit-brief.md")

# reason codes from §3.4.2 plus non-taxonomy integrity/discovery errors
REASON_TAXONOMY = (
    "BRIEF_ROOT_MISMATCH", "BRIEF_HEAD_MISMATCH", "WORKTREE_IDENTITY_CHANGED",
    "CWD_OUTSIDE_FROZEN_ROOT", "PATH_ESCAPE_ATTEMPT",
    "ALTERNATE_WORKTREE_ACCESS", "UNAUTHORIZED_TMP_ACCESS",
    "REPO_ROOT_REPLACED", "SYMLINK_ESCAPE",
)


class EnvironmentBindingError(Exception):
    """Raised on binding capture/verify/gate failures.

    `reason` is a §3.4.2 taxonomy code for environment failures; a few
    non-environment conditions use their own codes (NOT_A_REPOSITORY,
    BRIEF_UNREADABLE, BINDING_UNREADABLE, BINDING_DIGEST_MISMATCH,
    BRIEF_DIGEST_MISMATCH, GIT_QUERY_FAILED).
    """

    def __init__(self, reason: str, detail: dict[str, Any] | None = None):
        message = reason if not detail else f"{reason}: {detail}"
        super().__init__(message)
        self.reason = reason
        self.detail = detail or {}


# ---------------------------------------------------------------------------
# git plumbing helpers
# ---------------------------------------------------------------------------
def _git(repo: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", repo, *args],
                          capture_output=True, text=True, timeout=60,
                          check=False)


def _git_out(repo: str, *args: str) -> str:
    proc = _git(repo, *args)
    if proc.returncode != 0:
        raise EnvironmentBindingError(
            "GIT_QUERY_FAILED",
            {"repo": repo, "args": list(args), "stderr": proc.stderr.strip()})
    return proc.stdout.strip()


def _identity(git_dir_realpath: str, repo_root_realpath: str) -> str:
    return sha256_bytes(
        (git_dir_realpath + "\n" + repo_root_realpath).encode("utf-8"))


def repo_root_from(path: str) -> str:
    """Worktree-aware repository discovery via git plumbing ONLY.

    `git -C <path> rev-parse --show-toplevel`; never sniffs for a `.git`
    directory. Raises EnvironmentBindingError("NOT_A_REPOSITORY") when the
    path is not inside a git worktree.
    """
    proc = _git(path, "rev-parse", "--show-toplevel")
    out = proc.stdout.strip()
    if proc.returncode != 0 or not out:
        raise EnvironmentBindingError(
            "NOT_A_REPOSITORY",
            {"path": os.path.abspath(path), "stderr": proc.stderr.strip()})
    return os.path.realpath(out)


def cache_root() -> str:
    """Cache home: AUDIT_COUNCIL_CACHE_HOME if set, else
    ${XDG_CACHE_HOME:-~/.cache}/audit-council/ (expanduser applied)."""
    override = os.environ.get("AUDIT_COUNCIL_CACHE_HOME")
    if override:
        return os.path.expanduser(override)
    base = os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
    return os.path.join(base, "audit-council")


def _canonical(path: str) -> str:
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))


def _git_facts(repo_root: str) -> dict[str, Any]:
    toplevel = os.path.realpath(_git_out(repo_root, "rev-parse",
                                         "--show-toplevel"))
    git_dir = os.path.realpath(_git_out(repo_root, "rev-parse",
                                        "--absolute-git-dir"))
    common_raw = _git_out(repo_root, "rev-parse", "--git-common-dir")
    if not os.path.isabs(common_raw):
        common_raw = os.path.join(toplevel, common_raw)
    common_dir = os.path.realpath(common_raw)
    head = _git_out(repo_root, "rev-parse", "HEAD")
    abbrev = _git_out(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    remote_proc = _git(repo_root, "config", "--get", "remote.origin.url")
    remote_url = remote_proc.stdout.strip() if (
        remote_proc.returncode == 0 and remote_proc.stdout.strip()) else None
    return {
        "repo_root_realpath": repo_root,
        "git_toplevel_realpath": toplevel,
        "git_dir_realpath": git_dir,
        "git_common_dir_realpath": common_dir,
        "head_sha": head,
        "detached_head": abbrev == "HEAD",
        "remote_url": remote_url,
    }


def _repo_fingerprint_digest(repo_root: str,
                             algorithm: int = 2) -> str:
    """Fingerprint digest for the binding, applied time-independently and
    audit-output-stably.

    `repo_fingerprint.capture` includes its `captured_at` timestamp inside
    the digest; the binding identity must not depend on wall-clock time
    (pre-freeze clarification 1), so the digest here is computed over the
    fingerprint document minus `captured_at` — same canonical-JSON sha256
    algorithm, same content fields.

    The binding identity must ALSO be stable while the audit itself writes
    its own artifacts: the material-change rule excludes `audit-output/`
    (stateStore EXCLUDED_PREFIX), so the digest normalizes the fingerprint
    document the same way — porcelain lines and inventory entries under
    `audit-output/` are dropped before hashing. Without this, creating the
    run directory after capture would flip the binding digest and every
    later gate call would misreport WORKTREE_IDENTITY_CHANGED.

    B-004: algorithm 2 (the default for NEW bindings) keeps the v2
    content-aware untracked entries and the dirty-worktree byte map, so
    untracked/dirty byte replacements drift the binding identity.
    Algorithm 1 reproduces the LEGACY {path: size} normalization — used
    ONLY when verifying a binding frozen before algorithm 2 existed
    (bindings record `fingerprint_algorithm`; absent means 1)."""
    excluded = repo_fingerprint.EXCLUDED_PREFIX
    if algorithm < 2:
        # legacy reproduction: collapsed porcelain (no -uall) and
        # {path: size} untracked entries — byte-exact with what a v1-era
        # capture recorded
        collapsed = _git(repo_root, "status", "--porcelain")
        if collapsed.returncode != 0:
            raise EnvironmentBindingError(
                "GIT_QUERY_FAILED",
                {"repo": repo_root, "args": ["status", "--porcelain"],
                 "stderr": collapsed.stderr.strip()})
        kept = [line for line in collapsed.stdout.splitlines()
                if line and not line[3:].strip('"').startswith(excluded)]
        porcelain = "\n".join(kept) + ("\n" if kept else "")
        untracked: dict[str, Any] = {}
        for line in kept:
            if not line.startswith("?? "):
                continue
            path = line[3:].strip('"')
            try:
                untracked[path] = os.lstat(
                    os.path.join(repo_root, path)).st_size
            except OSError:
                untracked[path] = -1
        doc = repo_fingerprint.capture(repo_root)
        tracked = {path: meta for path, meta in
                   doc.get("tracked_inventory", {}).items()
                   if not path.startswith(excluded)}
        body = {k: v for k, v in doc.items()
                if k not in ("fingerprint_sha256", "captured_at",
                             "tool_versions", "porcelain",
                             "untracked_inventory", "dirty_worktree")}
        body["porcelain"] = porcelain
        body["tracked_inventory"] = tracked
        body["untracked_inventory"] = untracked
        return sha256_bytes(
            repo_fingerprint.canonical_json(body).encode("utf-8"))

    doc = repo_fingerprint.capture(repo_root)
    kept = [line for line in doc.get("porcelain", "").splitlines()
            if line and not line[3:].strip('"').startswith(excluded)]
    porcelain = "\n".join(kept) + ("\n" if kept else "")
    tracked = {path: meta for path, meta in
               doc.get("tracked_inventory", {}).items()
               if not path.startswith(excluded)}
    untracked = {path: entry for path, entry in
                 doc.get("untracked_inventory", {}).items()
                 if not path.startswith(excluded)}
    dirty = {path: digest for path, digest in
             doc.get("dirty_worktree", {}).items()
             if not path.startswith(excluded)}
    body = {k: v for k, v in doc.items()
            if k not in ("fingerprint_sha256", "captured_at",
                         "tool_versions")}
    body["porcelain"] = porcelain
    body["tracked_inventory"] = tracked
    body["untracked_inventory"] = untracked
    body["dirty_worktree"] = dirty
    return sha256_bytes(repo_fingerprint.canonical_json(body).encode("utf-8"))


def _normalize_brief_target(
        brief_target: dict[str, Any] | None) -> dict[str, Any]:
    bt = brief_target if isinstance(brief_target, dict) else {}
    return {
        "declared_repository_root": bt.get("declared_repository_root"),
        "declared_expected_head": bt.get("declared_expected_head"),
    }


# ---------------------------------------------------------------------------
# Binding assembly
# ---------------------------------------------------------------------------
def _build_binding(repo_root: str, brief_sha256: str,
                   brief_target: dict[str, Any],
                   allowed_disposable_roots: list[str],
                   expected_head: str | None,
                   frozen_at: str,
                   fingerprint_algorithm: int = 2) -> dict[str, Any]:
    facts = _git_facts(repo_root)
    linked = facts["git_dir_realpath"] != facts["git_common_dir_realpath"]
    doc: dict[str, Any] = {
        "binding_version": BINDING_VERSION,
        "frozen_at": frozen_at,
        "repo_root_realpath": facts["repo_root_realpath"],
        "git_toplevel_realpath": facts["git_toplevel_realpath"],
        "git_dir_realpath": facts["git_dir_realpath"],
        "git_common_dir_realpath": facts["git_common_dir_realpath"],
        "head_sha": facts["head_sha"],
        "detached_head": facts["detached_head"],
        "worktree_identity": _identity(facts["git_dir_realpath"],
                                       facts["repo_root_realpath"]),
        "source_repository_identity": {
            "common_dir_realpath": facts["git_common_dir_realpath"]
            if linked else facts["git_dir_realpath"],
            "remote_url": facts["remote_url"],
        },
        "brief_sha256": brief_sha256,
        "brief_target": brief_target,
        "expected_head": expected_head or facts["head_sha"],
        "allowed_disposable_roots": list(dict.fromkeys(
            _canonical(r) for r in allowed_disposable_roots)),
        # B-004: 2 = content-aware fingerprint (untracked sha256 +
        # dirty-worktree byte map). Bindings frozen before this field
        # exists have no entry and verify under the legacy algorithm 1
        # (reproduced byte-exactly, key omitted for them).
        "repo_fingerprint_sha256": _repo_fingerprint_digest(
            repo_root, algorithm=fingerprint_algorithm),
    }
    if fingerprint_algorithm >= 2:
        doc["fingerprint_algorithm"] = fingerprint_algorithm
    doc["binding_digest"] = digest(doc)
    return doc


def capture(repo_root: str, run_id: str, brief_path: str,
            brief_target: dict[str, Any] | None,
            allowed_disposable_roots: list[str]) -> dict[str, Any]:
    """Freeze the environment binding for the worktree containing
    `repo_root`.

    `run_id` is accepted for lifecycle symmetry (the caller registers the
    active run) but is not part of the binding document. `brief_path` is
    the run-owned materialized brief; its sha256 participates in the
    identity. Brief PROSE is never parsed.
    """
    root = repo_root_from(repo_root)
    try:
        brief_sha = sha256_file(brief_path)
    except OSError as exc:
        raise EnvironmentBindingError(
            "BRIEF_UNREADABLE",
            {"brief_path": os.path.abspath(brief_path),
             "error": str(exc)}) from None
    return _build_binding(root, brief_sha,
                          _normalize_brief_target(brief_target),
                          list(allowed_disposable_roots or []),
                          expected_head=None, frozen_at=utc_now_iso())


def canonical_json(doc: Any) -> str:
    """Same canonical form as repo_fingerprint.canonical_json."""
    return json.dumps(doc, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def digest(binding: dict[str, Any]) -> str:
    """sha256 over canonical JSON of every field except `binding_digest`
    and `frozen_at`."""
    body = {k: v for k, v in binding.items()
            if k not in ("binding_digest", "frozen_at")}
    return sha256_bytes(canonical_json(body).encode("utf-8"))


# ---------------------------------------------------------------------------
# Verify / gate / reconstruct
# ---------------------------------------------------------------------------
_IDENTITY_FIELDS = ("repo_root_realpath", "git_toplevel_realpath",
                    "git_dir_realpath", "git_common_dir_realpath",
                    "worktree_identity", "source_repository_identity")


def _capture_live(binding: dict[str, Any]) -> dict[str, Any]:
    """Recompute the binding for the frozen root, carrying over the
    run-owned inputs (brief hash/target, allowed roots, expectations) and
    the frozen fingerprint algorithm (B-004: a pre-algorithm-2 binding
    verifies under the legacy algorithm it was frozen with)."""
    return _build_binding(
        binding["repo_root_realpath"],
        binding["brief_sha256"],
        _normalize_brief_target(binding.get("brief_target")),
        list(binding.get("allowed_disposable_roots") or []),
        expected_head=binding.get("expected_head"),
        frozen_at=binding.get("frozen_at", ""),
        fingerprint_algorithm=binding.get("fingerprint_algorithm")
        if isinstance(binding.get("fingerprint_algorithm"), int) else 1)


def verify_frozen(binding: dict[str, Any]) -> dict[str, Any]:
    """Recompute the live binding for binding["repo_root_realpath"].

    Returns {"ok": bool, "reason": str|None, "frozen": {...}, "live":
    {...}}. Reason precedence (most precise first): REPO_ROOT_REPLACED
    (root missing / recreated / git facts unobtainable), BRIEF_HEAD_MISMATCH
    (a DECLARED expected head no longer matches the live head), then
    WORKTREE_IDENTITY_CHANGED (any other environment drift, including pure
    HEAD movement since freeze — HEAD alone is not identity).
    """
    result: dict[str, Any] = {"ok": False, "reason": None,
                              "frozen": binding, "live": None}
    if not isinstance(binding, dict):
        result["reason"] = "BINDING_UNREADABLE"
        return result
    if digest(binding) != binding.get("binding_digest"):
        result["reason"] = "BINDING_DIGEST_MISMATCH"
        return result
    root = binding.get("repo_root_realpath")
    if not isinstance(root, str) or not root:
        result["reason"] = "REPO_ROOT_REPLACED"
        return result
    if not os.path.isdir(root) or os.path.realpath(root) != root:
        result["reason"] = "REPO_ROOT_REPLACED"
        return result
    try:
        live = _capture_live(binding)
    except EnvironmentBindingError as exc:
        # root exists but git facts are unobtainable: the environment the
        # binding was frozen against has been replaced or broken
        result["reason"] = "REPO_ROOT_REPLACED"
        result["detail"] = exc.detail
        return result
    result["live"] = live

    declared_head = _normalize_brief_target(
        binding.get("brief_target")).get("declared_expected_head")
    if isinstance(declared_head, str) and declared_head != live["head_sha"]:
        result["reason"] = "BRIEF_HEAD_MISMATCH"
        return result
    drifted = [f for f in _IDENTITY_FIELDS if live[f] != binding.get(f)]
    drifted += [f for f in ("head_sha", "detached_head",
                            "repo_fingerprint_sha256")
                if live[f] != binding.get(f)]
    if drifted or live["binding_digest"] != binding.get("binding_digest"):
        result["reason"] = "WORKTREE_IDENTITY_CHANGED"
        result["detail"] = {"changed_fields": sorted(set(drifted))}
        return result
    result["ok"] = True
    return result


def assert_consistent(binding: dict[str, Any]) -> None:
    """A0.2 gate: zero-inference brief/environment consistency check.

    Raises EnvironmentBindingError with the most precise §3.4.2 reason.
    Only the EXPLICIT brief_target metadata participates; prose absolute
    paths inside the brief are inert text (never parsed).
    """
    bt = binding.get("brief_target")
    bt = bt if isinstance(bt, dict) else {}
    declared_root = bt.get("declared_repository_root")
    if isinstance(declared_root, str):
        resolved = os.path.realpath(os.path.expanduser(declared_root))
        if resolved != binding.get("repo_root_realpath"):
            raise EnvironmentBindingError(
                "BRIEF_ROOT_MISMATCH",
                {"declared_repository_root": declared_root,
                 "resolved": resolved,
                 "repo_root_realpath": binding.get("repo_root_realpath")})
    declared_head = bt.get("declared_expected_head")
    if isinstance(declared_head, str) \
            and declared_head != binding.get("head_sha"):
        raise EnvironmentBindingError(
            "BRIEF_HEAD_MISMATCH",
            {"declared_expected_head": declared_head,
             "head_sha": binding.get("head_sha")})
    if binding.get("expected_head") != binding.get("head_sha"):
        raise EnvironmentBindingError(
            "BRIEF_HEAD_MISMATCH",
            {"expected_head": binding.get("expected_head"),
             "head_sha": binding.get("head_sha")})
    res = verify_frozen(binding)
    if not res["ok"]:
        raise EnvironmentBindingError(res["reason"],
                                      res.get("detail", {}))


def reconstruct(run_dir: str) -> dict[str, Any]:
    """Rebuild the binding from disk after a restart.

    Loads <run_dir>/01-environment-binding.json, re-derives every input
    it can from disk state (the run-owned materialized brief under
    inputs/, git facts via plumbing) and recomputes the document; the
    result equals the frozen doc except `frozen_at`, so the digest is
    identical. Any tampering with the stored doc raises.
    """
    path = os.path.join(run_dir, BINDING_NAME)
    try:
        binding = load_json(path)
    except (OSError, ValueError) as exc:
        raise EnvironmentBindingError(
            "BINDING_UNREADABLE", {"path": path, "error": str(exc)}) from None
    if not isinstance(binding, dict):
        raise EnvironmentBindingError("BINDING_UNREADABLE",
                                      {"path": path})
    if digest(binding) != binding.get("binding_digest"):
        raise EnvironmentBindingError("BINDING_DIGEST_MISMATCH",
                                      {"path": path})
    brief_sha = binding.get("brief_sha256")
    materialized = os.path.join(run_dir, BRIEF_MATERIALISED_NAME)
    if os.path.isfile(materialized):
        recomputed = sha256_file(materialized)
        if recomputed != brief_sha:
            raise EnvironmentBindingError(
                "BRIEF_DIGEST_MISMATCH",
                {"path": materialized, "expected": brief_sha,
                 "actual": recomputed})
        brief_sha = recomputed
    live = _build_binding(
        binding["repo_root_realpath"],
        brief_sha,
        _normalize_brief_target(binding.get("brief_target")),
        list(binding.get("allowed_disposable_roots") or []),
        expected_head=binding.get("expected_head"),
        frozen_at=utc_now_iso(),
        fingerprint_algorithm=binding.get("fingerprint_algorithm")
        if isinstance(binding.get("fingerprint_algorithm"), int) else 1)
    return live
