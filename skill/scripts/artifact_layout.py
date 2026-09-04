#!/usr/bin/env python3
"""Artifact layout roots for audit-council v2 (PKG-ENV Task ENV.2, pillar A2).

Resolves the five artifact categories of AUDIT-COUNCIL-V2-ARCHITECTURE §3.4.9:

  PROJECT EVIDENCE     <repo>/audit-output                      (default)
  RUN ARTIFACTS        <repo>/audit-output/audit-council        (default)
  EPHEMERAL WORKTREES  ${XDG_CACHE_HOME:-~/.cache}/audit-council/worktrees
  BENCHMARK CORPUS     ${XDG_DATA_HOME:-~/.local/share}/audit-council/benchmark
  LONG-TERM HISTORY    ${XDG_DATA_HOME:-~/.local/share}/audit-council/history

Defaults PRESERVE v1 behavior: run artifacts stay project-local next to the
audited repository (policy flag "project_local"); existing project-owned
audit-output/ and eval-live-output directories are never relocated. An
optional JSON config file overrides any root:

  {"repo": "/abs/repo",
   "roots": {"long_term_history": "/abs/path", ...},
   "run_artifacts": "/abs/path"}}

Resolution is PURE: no directory is ever created here. All roots honor the
standard injections so deterministic tests never write the real user home:
XDG_DATA_HOME / XDG_CACHE_HOME and AUDIT_COUNCIL_ENV_ROOT (the same override
environment_manager uses for its worktrees; when set it takes precedence over
the XDG cache default for EPHEMERAL WORKTREES).

Note (open wiring decision, see MIGRATION-RETENTION-RECOMMENDATION.md):
environment_manager's own un-injected default places worktrees under
${XDG_DATA_HOME}/audit-council/worktrees; this module's documented default is
the XDG cache one from the frozen A2 contract. Under AUDIT_COUNCIL_ENV_ROOT
injection (all tests, and any operator config) the two always agree.
"""
from __future__ import annotations

import json
import os
from typing import Any

import env_binding
import path_guard

CATEGORIES = (
    "project_evidence",
    "run_artifacts",
    "ephemeral_worktrees",
    "benchmark_corpus",
    "long_term_history",
)
PROJECT_EVIDENCE_DIRNAME = "audit-output"
RUN_ARTIFACTS_RELPATH = os.path.join("audit-output", "audit-council")


class ArtifactLayoutError(Exception):
    """Raised on unreadable/invalid layout configuration."""


def _data_home() -> str:
    return os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")


def _cache_home() -> str:
    return os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")


def _canonical(path: str) -> str:
    return os.path.realpath(os.path.expanduser(path))


def _load_config(config_path: str) -> dict[str, Any]:
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        raise ArtifactLayoutError(
            f"layout config unreadable: {config_path}: {exc}") from None
    if not isinstance(doc, dict):
        raise ArtifactLayoutError(
            f"layout config must be a JSON object: {config_path}")
    # keys under an optional "roots" subsection behave like top-level keys;
    # top-level wins on collision
    merged: dict[str, Any] = {}
    roots_section = doc.get("roots")
    if isinstance(roots_section, dict):
        merged.update(roots_section)
    merged.update({k: v for k, v in doc.items() if k != "roots"})
    return merged


def _discover_repo() -> str | None:
    """Repository containing the CWD via git plumbing; None if not a repo."""
    try:
        return env_binding.repo_root_from(os.getcwd())
    except env_binding.EnvironmentBindingError:
        return None


def resolve_roots(config_path: str | None = None) -> dict:
    """Resolve the artifact-root layout (pure; creates nothing).

    Returns {"project_evidence", "run_artifacts", "ephemeral_worktrees",
    "benchmark_corpus", "long_term_history", "run_artifacts_policy"}.
    Project-local roots are None when no repository is known (config "repo"
    key or CWD discovery); the policy flag records whether "run_artifacts"
    is the v1-preserving project-local default ("project_local") or a config
    override ("config_override").
    """
    config = _load_config(config_path) if config_path is not None else {}
    override = {k: _canonical(str(config[k])) for k in CATEGORIES
                if isinstance(config.get(k), str) and config[k].strip()}

    repo: str | None = None
    if isinstance(config.get("repo"), str) and config["repo"].strip():
        repo = _canonical(config["repo"])
    else:
        repo = _discover_repo()

    roots: dict[str, Any] = {
        "project_evidence": override.get(
            "project_evidence",
            os.path.join(repo, PROJECT_EVIDENCE_DIRNAME) if repo else None),
        "run_artifacts": override.get(
            "run_artifacts",
            os.path.join(repo, RUN_ARTIFACTS_RELPATH) if repo else None),
        "ephemeral_worktrees": override.get(
            "ephemeral_worktrees", _default_ephemeral_worktrees()),
        "benchmark_corpus": override.get(
            "benchmark_corpus",
            os.path.join(_data_home(), "audit-council", "benchmark")),
        "long_term_history": override.get(
            "long_term_history",
            os.path.join(_data_home(), "audit-council", "history")),
        "run_artifacts_policy": ("config_override" if "run_artifacts"
                                 in override else "project_local"),
    }
    return roots


def _default_ephemeral_worktrees() -> str:
    """AUDIT_COUNCIL_ENV_ROOT (tests + operator config), else the frozen A2
    default ${XDG_CACHE_HOME:-~/.cache}/audit-council/worktrees."""
    injected = os.environ.get("AUDIT_COUNCIL_ENV_ROOT")
    if injected:
        return os.path.expanduser(injected)
    return os.path.join(_cache_home(), "audit-council", "worktrees")


def category_of(path: str, roots: dict) -> str | None:
    """Which artifact category `path` belongs to, or None.

    Containment is component-wise on canonicalized paths (never a string
    prefix match). run_artifacts is checked before its parent category
    project_evidence so nested paths report the most specific category.
    Roots that are None/empty are skipped.
    """
    order = ("run_artifacts", "project_evidence", "ephemeral_worktrees",
             "benchmark_corpus", "long_term_history")
    for category in order:
        root = roots.get(category)
        if isinstance(root, str) and root.strip():
            if path_guard.is_within(path, root):
                return category
    return None
