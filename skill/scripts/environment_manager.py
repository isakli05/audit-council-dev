#!/usr/bin/env python3
"""Integrated Audit Environment Manager + artifact lifecycle
(PKG-ENV Tasks ENV.1/ENV.2 — pillars A1/A2, ARCHITECTURE §3.4.9).

Mode resolution (`resolve_mode`) — AUTO is the SAFEST derivation and never
silently downgrades isolation:

  - HISTORICAL when brief_meta["historical"] is true;
  - RELEASE when the contract cannot be audited on the live tree: it declares
    an expected head that is not the live repo HEAD, declares a repository
    root different from the live repo (the live repo is the worktree containing
    the process CWD, discovered via git plumbing), carries an explicit
    isolation requirement, or brief_meta carries a target_ref;
  - CURRENT only when nothing above applies.

An explicit brief_meta["mode"] is validated against the same safety rule: a
requested CURRENT that would violate isolation raises
EnvironmentManagerError("AUTO-safety violation"). Explicit RELEASE/HISTORICAL
are always honored (they are at least as isolated as the AUTO derivation).

Preparation (`prepare`) — CURRENT validates the live repository and freezes a
binding on it; RELEASE/HISTORICAL create a DETACHED linked worktree
(`git -C <source> worktree add --detach <root> <ref>`) and freeze the binding
ON the worktree. Worktrees never live under the cache root: they go to
<env_root()>/<run-id>/worktree where env_root() is AUDIT_COUNCIL_ENV_ROOT if
set, else ${XDG_DATA_HOME:-~/.local/share}/audit-council/worktrees (tests
inject AUDIT_COUNCIL_ENV_ROOT — the real user home is never written in tests).
HISTORICAL stages ONLY explicitly allow-listed evidence files, copied to the
worktree's sibling <env_root()>/<run-id>/staged-evidence/ (= <worktree-root>/..
/staged-evidence) with sha256 recorded; the deny-list (git internals, the
audit's own audit-output/) wins over the allow-list. The SOURCE working tree
is left byte-identical: `git status --porcelain` is captured before and after
and must compare equal.

Lifecycle (`archive_run` / `remove_worktree` / `list_runs` / `cleanup`) —
run artifacts are archived to the long-term-history root BEFORE any worktree
removal, by atomic directory swap (copy to <dest>.tmp-<pid>, then os.rename;
on failure the original is untouched and no partial archive is visible under
the final name). After the archive is durable, the run dir is deleted from
inside the worktree so a plain `git worktree remove` succeeds.
`remove_worktree` uses git only — NEVER shutil.rmtree on a worktree — and
refuses ("unarchived artifacts present") while untracked audit-output
artifacts remain. `cleanup` is dry-run by default; long-term history is never
removed by it (see MIGRATION-RETENTION-RECOMMENDATION.md).
"""
from __future__ import annotations

import os
import shutil
import subprocess
from typing import Any

import artifact_layout
import env_binding
import path_guard
from state_store import RUN_ID_RE, atomic_write_json, load_json, sha256_file, utc_now_iso

RECORD_VERSION = 2
RECORD_NAME = "environment-record.json"
PREPARATION_BRIEF_NAME = "preparation-brief.md"
WORKTREE_DIRNAME = "worktree"
STAGED_EVIDENCE_DIRNAME = "staged-evidence"
ACTIVE_RUNS_DIRNAME = "active-runs"

MODES = ("AUTO", "CURRENT", "RELEASE", "HISTORICAL")
PREPARED_MODES = ("CURRENT", "RELEASE", "HISTORICAL")

# HISTORICAL evidence staging: the deny-list WINS over the allow-list. Git
# internals and the audit's own output are never staged as evidence
# (repo-relative prefixes; ".git" is additionally denied as any path
# component, covering worktree git-link files).
EVIDENCE_DENYLIST = (".git/", "audit-output/")

_PREPARATION_BRIEF = (
    "# audit-council environment preparation\n"
    "Synthetic placeholder brief; the run's real brief is hashed into the\n"
    "binding at init-run time.\n"
)


class EnvironmentManagerError(Exception):
    """Raised on mode-resolution, preparation, or lifecycle failures."""


# ---------------------------------------------------------------------------
# git plumbing helpers
# ---------------------------------------------------------------------------
def _git(repo: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", repo, *args],
                          capture_output=True, text=True, timeout=60,
                          check=False)


def _head_at(root: str) -> str | None:
    proc = _git(root, "rev-parse", "HEAD")
    return proc.stdout.strip() if proc.returncode == 0 else None


def env_root() -> str:
    """Ephemeral-worktree env root: AUDIT_COUNCIL_ENV_ROOT if set, else
    ${XDG_DATA_HOME:-~/.local/share}/audit-council/worktrees (expanduser
    applied). Worktrees must NOT live under the cache root."""
    injected = os.environ.get("AUDIT_COUNCIL_ENV_ROOT")
    if injected:
        return os.path.expanduser(injected)
    base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(base, "audit-council", "worktrees")


def run_env_dir(run_id: str) -> str:
    """Per-run environment directory <env-root>/<run-id>/."""
    return os.path.join(env_root(), run_id)


def worktree_dir(run_id: str) -> str:
    """Detached worktree path <env-root>/<run-id>/worktree."""
    return os.path.join(run_env_dir(run_id), WORKTREE_DIRNAME)


def staged_evidence_dir(run_id: str) -> str:
    """Staged-evidence path: sibling of the worktree
    (<worktree-root>/../staged-evidence)."""
    return os.path.join(run_env_dir(run_id), STAGED_EVIDENCE_DIRNAME)


# ---------------------------------------------------------------------------
# Mode resolution (A1)
# ---------------------------------------------------------------------------
def _live_repo() -> tuple[str | None, str | None]:
    """(root, head) of the repository containing the CWD; (None, None) when
    the CWD is not inside a git worktree."""
    try:
        root = env_binding.repo_root_from(os.getcwd())
    except env_binding.EnvironmentBindingError:
        return None, None
    return root, _head_at(root)


def _isolation_reasons(contract: Any, brief_meta: dict[str, Any]) -> list[str]:
    """Why the contract/brief cannot be audited on the live tree."""
    reasons: list[str] = []
    if brief_meta.get("target_ref") is not None:
        reasons.append("brief carries a target_ref")
    contract = contract if isinstance(contract, dict) else {}
    if contract.get("requires_isolation"):
        reasons.append("contract declares an isolation requirement")
    target = contract.get("target_repository")
    target = target if isinstance(target, dict) else {}
    declared_root = target.get("root")
    declared_head = target.get("head_sha")
    live_root, _live_head = _live_repo()
    if isinstance(declared_root, str) and declared_root.strip():
        root_real = os.path.realpath(os.path.expanduser(declared_root))
        if live_root is not None and root_real != live_root:
            reasons.append(
                "contract declares a different repository root than the "
                "live repo")
        if isinstance(declared_head, str) and declared_head.strip():
            head_at_root = _head_at(root_real)
            if head_at_root is not None and declared_head.strip() != head_at_root:
                reasons.append(
                    "contract expects a head that is not the live repo HEAD")
    return reasons


def resolve_mode(contract: dict, brief_meta: dict | None = None) -> str:
    """Resolve AUTO|CURRENT|RELEASE|HISTORICAL (see module docstring)."""
    brief_meta = dict(brief_meta or {})
    requested = brief_meta.get("mode") or "AUTO"
    if requested not in MODES:
        raise EnvironmentManagerError(
            f"unknown mode {requested!r}; expected one of {MODES}")
    historical = bool(brief_meta.get("historical"))
    reasons = _isolation_reasons(contract, brief_meta)
    auto = "HISTORICAL" if historical else ("RELEASE" if reasons else "CURRENT")
    if requested == "AUTO":
        return auto
    if requested == "CURRENT" and (reasons or historical):
        raise EnvironmentManagerError(
            "AUTO-safety violation: requested CURRENT but isolation is "
            "required (" + "; ".join(reasons or ["historical flag"]) + ")")
    return requested


# ---------------------------------------------------------------------------
# Preparation (A1)
# ---------------------------------------------------------------------------
def _evidence_relpath(source: str, raw: str) -> str:
    """Normalize an allow-list entry to a repo-relative path; absolute paths
    must resolve INSIDE the source repository (fail-closed on escape)."""
    text = str(raw)
    expanded = os.path.expanduser(text)
    if os.path.isabs(expanded):
        real = os.path.realpath(expanded)
        if not path_guard.is_within(real, source):
            raise EnvironmentManagerError(
                f"evidence path escapes the source repository: {raw!r}")
        return os.path.relpath(real, source)
    norm = os.path.normpath(expanded)
    if os.path.isabs(norm) or norm.startswith(".."):
        raise EnvironmentManagerError(
            f"evidence path escapes the source repository: {raw!r}")
    return norm


def _is_denylisted(rel: str) -> bool:
    if ".git" in rel.split(os.sep):
        return True
    for prefix in EVIDENCE_DENYLIST:
        stem = prefix.rstrip("/")
        if rel == stem or rel.startswith(prefix):
            return True
    return False


def _stage_evidence(source: str, run_id: str,
                    allowlist: list[str]) -> list[dict[str, Any]]:
    """Copy ONLY allow-listed, non-deny-listed files into the run's
    staged-evidence dir, recording sha256 per file.

    R5 NEW-3: relative entries are resolved through REALPATH before any
    check/copy — an in-repo symlink (attacker-controllable content) can
    no longer stage host files or deny-listed paths; the RESOLVED path
    must stay inside the source repo and re-pass the deny-list."""
    staged_root = staged_evidence_dir(run_id)
    entries: list[dict[str, Any]] = []
    source_real = os.path.realpath(source)
    for raw in allowlist:
        rel = _evidence_relpath(source, raw)
        src = os.path.join(source, rel)
        resolved = os.path.realpath(src)
        if not path_guard.is_within(resolved, source_real):
            raise EnvironmentManagerError(
                f"evidence path resolves outside the source repository "
                f"(symlink escape): {raw!r} -> {resolved}")
        resolved_rel = os.path.relpath(resolved, source_real)
        if _is_denylisted(rel) or _is_denylisted(resolved_rel):
            raise EnvironmentManagerError(
                f"evidence deny-list violation: {rel!r} (resolved "
                f"{resolved_rel!r}) matches EVIDENCE_DENYLIST "
                f"{EVIDENCE_DENYLIST}")
        if not os.path.isfile(resolved):
            raise EnvironmentManagerError(
                f"allow-listed evidence file missing: {raw!r}")
        dest = os.path.join(staged_root, resolved_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(resolved, dest)
        entries.append({"path": resolved_rel,
                        "sha256": sha256_file(dest),
                        "allowed": True})
    entries.sort(key=lambda e: e["path"])
    return entries


def prepare(mode: str, source_repo: str, run_id: str,
            target_ref: str | None = None,
            evidence_allowlist: list[str] | None = None) -> dict:
    """Prepare the audit environment and return the EnvironmentRecord
    (schemas/environment-record.schema.json), also persisted at
    <env-root>/<run-id>/environment-record.json."""
    if mode not in PREPARED_MODES:
        raise EnvironmentManagerError(
            f"prepare() needs a concrete mode {PREPARED_MODES}; resolve AUTO "
            f"first via resolve_mode(); got {mode!r}")
    if not RUN_ID_RE.match(str(run_id or "")):
        raise EnvironmentManagerError(f"malformed run_id {run_id!r}")
    if mode == "CURRENT" and target_ref is not None:
        raise EnvironmentManagerError(
            "AUTO-safety violation: CURRENT audits the live tree and cannot "
            "honor a target_ref")
    try:
        source = env_binding.repo_root_from(source_repo)
    except env_binding.EnvironmentBindingError as exc:
        raise EnvironmentManagerError(
            f"source repository unusable: {exc}") from None

    porcelain_before = _git(source, "status", "--porcelain")
    if porcelain_before.returncode != 0:
        raise EnvironmentManagerError(
            f"git status failed in source repo: {porcelain_before.stderr.strip()}")

    env_dir = run_env_dir(run_id)
    if os.path.exists(env_dir):
        raise EnvironmentManagerError(
            f"environment dir already exists for run {run_id}: {env_dir}")
    os.makedirs(env_dir)

    worktree_root: str | None = None
    worktree_created = False
    try:
        brief_path = os.path.join(env_dir, PREPARATION_BRIEF_NAME)
        with open(brief_path, "w", encoding="utf-8") as fh:
            fh.write(_PREPARATION_BRIEF)

        notes: list[str] = []
        staged: list[dict[str, Any]] = []
        if mode == "CURRENT":
            binding = env_binding.capture(source, run_id, brief_path, None, [])
            detached = bool(binding["detached_head"])
            notes.append("CURRENT: live tree audited in place; no worktree")
        else:
            ref = target_ref or "HEAD"
            worktree_root = worktree_dir(run_id)
            proc = _git(source, "worktree", "add", "--detach",
                        worktree_root, ref)
            if proc.returncode != 0:
                raise EnvironmentManagerError(
                    f"git worktree add failed for ref {ref!r}: "
                    f"{proc.stderr.strip()}")
            worktree_created = True
            abbrev = _git(worktree_root, "rev-parse", "--abbrev-ref", "HEAD")
            if abbrev.returncode != 0 or abbrev.stdout.strip() != "HEAD":
                raise EnvironmentManagerError(
                    "prepared worktree is not detached "
                    f"(abbrev-ref={abbrev.stdout.strip()!r})")
            binding = env_binding.capture(worktree_root, run_id, brief_path,
                                          None, [])
            detached = True
            notes.append(f"{mode}: detached worktree at ref {ref}")
            if evidence_allowlist:
                # da27c0 fix: the public contract promises authorized
                # evidence staging for RELEASE *and* HISTORICAL; both
                # now stage (realpath-resolved, containment + deny-list
                # re-applied post-resolution). Copies land in a
                # run-owned staged-evidence dir so Opus and the
                # bubblewrapped Codex (run dir rw) receive identical
                # authorized evidence.
                staged = _stage_evidence(source, run_id,
                                         list(evidence_allowlist))
                notes.append(
                    f"{mode}: staged {len(staged)} allow-listed "
                    f"evidence file(s); deny-list enforced")
            else:
                notes.append(f"{mode}: no evidence allow-list given")

        porcelain_after = _git(source, "status", "--porcelain")
        if porcelain_after.returncode != 0 \
                or porcelain_after.stdout != porcelain_before.stdout:
            raise EnvironmentManagerError(
                "source working tree changed during prepare() — the live "
                "tree must remain byte-identical")

        record = {
            "schema_version": RECORD_VERSION,
            "mode": mode,
            "run_id": run_id,
            "created_at": utc_now_iso(),
            "source_repo_realpath": source,
            "worktree_root": worktree_root,
            "worktree_detached": detached,
            "target_ref": target_ref,
            "binding_digest": binding["binding_digest"],
            "staged_evidence": staged,
            "archive_root": artifact_layout.resolve_roots()[
                "long_term_history"],
            "notes": "; ".join(notes) + f"; source_head={_head_at(source)}",
        }
        atomic_write_json(os.path.join(env_dir, RECORD_NAME), record)
        return record
    except BaseException:
        # leave nothing half-prepared behind; a created worktree is removed
        # via GIT (never raw deletion), the rest of the env dir via rmtree
        if worktree_created and worktree_root and os.path.isdir(worktree_root):
            _git(source, "worktree", "remove", "--force", worktree_root)
        shutil.rmtree(env_dir, ignore_errors=True)
        raise


# ---------------------------------------------------------------------------
# Archive / remove / list / cleanup (A2)
# ---------------------------------------------------------------------------
def _copy_tree(src: str, dst: str) -> None:
    """Copy helper indirection (crash-injection point for tests)."""
    shutil.copytree(src, dst, dirs_exist_ok=True)


def _prune_empty_parents(path: str, stop: str) -> None:
    """Best-effort removal of now-empty parent directories up to (excluding)
    `stop` — empty dirs are invisible to git, this is hygiene only."""
    current = os.path.dirname(os.path.abspath(path))
    stop = os.path.realpath(stop)
    while os.path.realpath(current) != stop and current not in (os.sep, ""):
        try:
            os.rmdir(current)
        except OSError:
            return
        current = os.path.dirname(current)


def archive_run(run_dir: str, worktree_root: str | None) -> str:
    """Copy the run dir into <archive_root>/<run-id>/ BEFORE any worktree
    removal; atomic directory swap. Returns the archive path.

    The copy goes to <dest>.tmp-<pid> first and is swapped into place with
    os.rename; on any failure the tmp dir is removed, a displaced previous
    archive is restored, and the ORIGINAL run dir is untouched. After the
    swap is durable, a run dir living INSIDE the worktree is deleted from it
    (so a plain `git worktree remove` succeeds afterwards).
    """
    run_dir = os.path.abspath(run_dir)
    if not os.path.isdir(run_dir):
        raise EnvironmentManagerError(f"run dir not found: {run_dir}")
    run_id = os.path.basename(os.path.normpath(run_dir))
    archive_root = artifact_layout.resolve_roots()["long_term_history"]
    os.makedirs(archive_root, exist_ok=True)
    dest = os.path.join(archive_root, run_id)
    tmp = f"{dest}.tmp-{os.getpid()}"

    if os.path.exists(tmp):
        # stale temp of a crashed same-pid attempt; it is not the archive
        # itself (tmp naming) and is safe to discard
        shutil.rmtree(tmp)
    previous: str | None = None
    if os.path.exists(dest):
        previous = f"{dest}.old-{os.getpid()}"
        if os.path.exists(previous):
            shutil.rmtree(previous)
        os.rename(dest, previous)
    try:
        os.makedirs(tmp)
        _copy_tree(run_dir, tmp)
        os.rename(tmp, dest)  # atomic swap into the final name
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        if previous is not None and not os.path.exists(dest):
            os.rename(previous, dest)  # restore the displaced old archive
        raise
    if previous is not None:
        shutil.rmtree(previous, ignore_errors=True)

    if worktree_root:
        wt = os.path.realpath(worktree_root)
        if path_guard.is_within(run_dir, wt) and os.path.exists(run_dir):
            shutil.rmtree(run_dir)
            _prune_empty_parents(run_dir, wt)
    return dest


def _source_of_worktree(worktree_root: str) -> str:
    """Main-worktree root owning this linked worktree, via git plumbing."""
    proc = _git(worktree_root, "rev-parse", "--git-common-dir")
    if proc.returncode != 0:
        raise EnvironmentManagerError(
            f"cannot resolve worktree git-common-dir: {proc.stderr.strip()}")
    common = proc.stdout.strip()
    if not os.path.isabs(common):
        common = os.path.join(worktree_root, common)
    source = os.path.dirname(os.path.realpath(common))
    if not os.path.isdir(source):
        raise EnvironmentManagerError(
            f"cannot resolve owning repository for worktree {worktree_root}")
    return source


def _unarchived_artifacts(worktree_root: str) -> list[str]:
    """UNTRACKED audit-output paths inside the worktree (archive_run deletes
    run dirs after copying, so anything still present is unarchived)."""
    proc = _git(worktree_root, "status", "--porcelain")
    if proc.returncode != 0:
        raise EnvironmentManagerError(
            f"git status failed in worktree: {proc.stderr.strip()}")
    hits: list[str] = []
    for line in proc.stdout.splitlines():
        if not line.startswith("?? "):
            continue
        path = line[3:].strip().strip('"')
        if path == "audit-output" or path.startswith("audit-output" + os.sep):
            hits.append(path)
    return sorted(set(hits))


def remove_worktree(worktree_root: str) -> None:
    """Remove a linked worktree using `git worktree remove` ONLY (never
    shutil.rmtree). Refuses with "unarchived artifacts present" while
    untracked audit-output artifacts remain; falls back to --force only when
    the plain removal fails (residual untracked dirt)."""
    wt = os.path.realpath(worktree_root)
    if not os.path.isdir(wt):
        raise EnvironmentManagerError(f"worktree not found: {worktree_root}")
    unarchived = _unarchived_artifacts(wt)
    if unarchived:
        raise EnvironmentManagerError(
            "unarchived artifacts present: "
            + ", ".join(unarchived[:8]))
    source = _source_of_worktree(wt)
    proc = _git(source, "worktree", "remove", wt)
    if proc.returncode != 0:
        proc = _git(source, "worktree", "remove", "--force", wt)
        if proc.returncode != 0:
            raise EnvironmentManagerError(
                f"git worktree remove failed: {proc.stderr.strip()}")
    if os.path.exists(wt):
        raise EnvironmentManagerError(
            f"git worktree remove reported success but {wt} still exists")


def _active_run_ids() -> set[str]:
    registry = os.path.join(env_binding.cache_root(), ACTIVE_RUNS_DIRNAME)
    if not os.path.isdir(registry):
        return set()
    return {name for name in os.listdir(registry)
            if os.path.isfile(os.path.join(registry, name))}


def _load_record(env_dir: str) -> dict[str, Any]:
    path = os.path.join(env_dir, RECORD_NAME)
    if not os.path.isfile(path):
        return {}
    try:
        doc = load_json(path)
    except (OSError, ValueError):
        return {}
    return doc if isinstance(doc, dict) else {}


def list_runs() -> list[dict]:
    """Scan the env root and the archive root for known runs.
    Entries: {run_id, repo, mode, archived, worktree_root}; worktree_root
    reports on-disk reality (None once removed); archive-only runs carry
    repo/mode None."""
    archive_root = artifact_layout.resolve_roots()["long_term_history"]
    runs: dict[str, dict] = {}
    eroot = env_root()
    if os.path.isdir(eroot):
        for name in sorted(os.listdir(eroot)):
            env_dir = os.path.join(eroot, name)
            if not os.path.isdir(env_dir):
                continue
            rec = _load_record(env_dir)
            worktree = rec.get("worktree_root")
            if not (isinstance(worktree, str) and os.path.isdir(worktree)):
                worktree = None
            runs[name] = {
                "run_id": name,
                "repo": rec.get("source_repo_realpath"),
                "mode": rec.get("mode"),
                "archived": os.path.isdir(os.path.join(archive_root, name)),
                "worktree_root": worktree,
            }
    if os.path.isdir(archive_root):
        for name in sorted(os.listdir(archive_root)):
            if name in runs or not os.path.isdir(os.path.join(archive_root,
                                                              name)):
                continue
            runs[name] = {"run_id": name, "repo": None, "mode": None,
                          "archived": True, "worktree_root": None}
    return [runs[key] for key in sorted(runs)]


def cleanup(dry_run: bool = True) -> dict:
    """Hygiene pass. Returns {would_remove, removed, kept}.

    Dry-run BY DEFAULT. Even with dry_run=False, only ephemeral worktrees of
    runs without an active-run registry entry and without unarchived
    artifacts are removed (via remove_worktree — git only). Long-term history
    / archives are NEVER removed by cleanup; acting on them is an explicit
    operator decision (MIGRATION-RETENTION-RECOMMENDATION.md)."""
    result: dict[str, list[str]] = {"would_remove": [], "removed": [],
                                    "kept": []}
    active = _active_run_ids()
    eroot = env_root()
    if os.path.isdir(eroot):
        for name in sorted(os.listdir(eroot)):
            env_dir = os.path.join(eroot, name)
            if not os.path.isdir(env_dir):
                continue
            worktree = _load_record(env_dir).get("worktree_root")
            if not (isinstance(worktree, str) and os.path.isdir(worktree)):
                # record-only (or already-removed) env dir: history, keep
                result["kept"].append(env_dir)
                continue
            if name in active:
                result["kept"].append(worktree)
                continue
            if _unarchived_artifacts(worktree):
                result["kept"].append(worktree)
                continue
            if dry_run:
                result["would_remove"].append(worktree)
            else:
                remove_worktree(worktree)
                result["removed"].append(worktree)
    archive_root = artifact_layout.resolve_roots()["long_term_history"]
    if os.path.isdir(archive_root):
        for name in sorted(os.listdir(archive_root)):
            path = os.path.join(archive_root, name)
            if os.path.isdir(path):
                result["kept"].append(path)
    return result
