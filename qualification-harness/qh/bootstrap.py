"""C-1 — pre-controller controller-scope provenance and C4' verification.

Accepted semantics (AUCDEV-023 readiness record + RC-1 root cause):

* controller-scope provenance is captured BEFORE the controller starts,
  as an immutable, content-addressed bootstrap manifest over the relevant
  controller configuration scope (the dedicated CLAUDE_CONFIG_DIR);
* capture FAILS on pre-existing disallowed ``skills/`` entries and on any
  pre-existing foreign ``projects/`` state;
* the manifest identity is bound into the attempt/relaunch binding;
* AFTER controller start, C4' verifies the ACTUAL controller process
  binding through ``/proc/<pid>/environ`` (CLAUDE_CONFIG_DIR exact match),
  the pid/starttime binding (pid-reuse defense) and scope consistency;
* pre-existing state and current-session-created state are DISTINGUISHED:
  the controller's own current-session project tree (the single new
  ``projects/<slug>/`` subtree the runtime created after start) is allowed
  — the accepted rule is  current tree  ⊆  manifest ∪ {own current-session
  slug}.  The harness does NOT assume every runtime/version always creates
  any particular tree: it compares OBSERVED state against the bound
  manifest, so an absent session tree also passes;
* manifest mismatch/tamper, modified/deleted manifest entries, new
  ``skills/`` entries and any other unbound extra project/session state
  are rejected.
"""
from __future__ import annotations

import os
import stat
from dataclasses import dataclass, field
from pathlib import Path

from .util import content_id, proc_environ, proc_starttime, utc_now_iso

SCHEMA = "qh-bootstrap-manifest/1"
SENSITIVE_NAME_MARKERS = ("credential", "token", "secret", "auth.json")
MAX_ENTRIES = 4096
MAX_DEPTH = 8


class BootstrapCaptureError(RuntimeError):
    """Fail-closed capture rejection (pre-existing disallowed state)."""


@dataclass
class CaptureResult:
    ok: bool
    manifest_id: str | None = None
    manifest_path: str | None = None
    reason: str | None = None


def _is_sensitive(relpath: str) -> bool:
    name = relpath.rsplit("/", 1)[-1].lower()
    return any(marker in name for marker in SENSITIVE_NAME_MARKERS)


def walk_scope(config_dir: str, *, max_entries: int = MAX_ENTRIES,
               max_depth: int = MAX_DEPTH) -> dict[str, dict]:
    """Bounded deterministic walk of the configuration scope.  Entries carry
    content hashes EXCEPT sensitive-named files, which are recorded by
    metadata only (size/mode/mtime) — no credential value is ever hashed
    into a manifest."""
    entries: dict[str, dict] = {}
    base = Path(config_dir)
    for dirpath, dirnames, filenames in os.walk(config_dir):
        dirnames.sort()
        rel_dir = os.path.relpath(dirpath, config_dir)
        depth = 0 if rel_dir == "." else rel_dir.count(os.sep) + 1
        if depth >= max_depth:
            dirnames[:] = []
        for name in sorted(dirnames):
            rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            st = os.lstat(os.path.join(dirpath, name))
            entries[rel] = {"type": "dir", "mode": stat.S_IMODE(st.st_mode),
                            "mtime_ns": st.st_mtime_ns}
        for name in sorted(filenames):
            rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            full = os.path.join(dirpath, name)
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                entries[rel] = {"type": "symlink",
                                "target": os.readlink(full),
                                "mode": stat.S_IMODE(st.st_mode)}
            elif stat.S_ISREG(st.st_mode):
                entry = {"type": "file", "mode": stat.S_IMODE(st.st_mode),
                         "size": st.st_size, "mtime_ns": st.st_mtime_ns}
                if _is_sensitive(rel):
                    entry["sha256"] = None
                    entry["sensitive"] = True
                else:
                    from .util import sha256_file
                    entry["sha256"] = sha256_file(full)
                entries[rel] = entry
            else:
                entries[rel] = {"type": "special",
                                "mode": stat.S_IMODE(st.st_mode)}
        if len(entries) > max_entries:
            raise BootstrapCaptureError(
                f"scope too large (> {max_entries} entries) — refusing")
    return entries


def capture_bootstrap_manifest(config_dir: str, operator_state_dir: str, *,
                               allowed_skills: tuple[str, ...] = (),
                               note: str = "") -> CaptureResult:
    """Capture the controller configuration scope BEFORE controller start.

    Fails closed (BootstrapCaptureError -> CaptureResult(ok=False)) on:
      * a missing/non-directory/symlinked config dir;
      * pre-existing disallowed ``skills/`` entries;
      * ANY pre-existing ``projects/`` state (foreign controller state).
    """
    try:
        real = os.path.realpath(config_dir)
        st = os.lstat(config_dir)
        if not os.path.isdir(config_dir) or os.path.islink(config_dir):
            raise BootstrapCaptureError(
                "CLAUDE_CONFIG_DIR is not a real directory "
                f"(symlink or missing): {config_dir}")
        if os.path.realpath(config_dir) != config_dir:
            raise BootstrapCaptureError(
                f"CLAUDE_CONFIG_DIR must be passed resolved ({real})")
        entries = walk_scope(config_dir)
    except BootstrapCaptureError as exc:
        return CaptureResult(ok=False, reason=str(exc))

    skills = sorted(k for k in entries if k == "skills"
                    or k.startswith("skills/"))
    # allowed_skills names skill ENTRIES the operator explicitly permits
    # pre-existing (default: none — the demonstrated disable-all posture).
    bad_skills = [s for s in skills
                  if s != "skills" and s.split("/")[1] not in allowed_skills]
    if bad_skills:
        return CaptureResult(
            ok=False,
            reason="PRE_EXISTING_SKILLS_PRESENT: " + ",".join(bad_skills))
    projects = sorted(k for k in entries if k == "projects"
                      or k.startswith("projects/"))
    if projects:
        return CaptureResult(
            ok=False,
            reason="PRE_EXISTING_PROJECTS_STATE_PRESENT: " + ",".join(projects))

    body = {"schema": SCHEMA, "config_dir": config_dir,
            "entries": entries, "note": note}
    manifest_id = content_id(body)
    doc = {**body, "id": manifest_id, "captured_at": utc_now_iso()}
    mdir = os.path.join(operator_state_dir, "manifests")
    Path(mdir).mkdir(parents=True, exist_ok=True)
    mpath = os.path.join(mdir, f"{manifest_id}.json")
    if os.path.exists(mpath):
        # content-addressed: same id must mean same bytes
        from .util import sha256_file
        import json
        with open(mpath, "r", encoding="utf-8") as fh:
            existing = json.load(fh)
        if existing.get("id") != manifest_id:
            return CaptureResult(ok=False, reason="MANIFEST_STORE_CONFLICT")
    else:
        import json
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, sort_keys=True, indent=1)
    return CaptureResult(ok=True, manifest_id=manifest_id,
                         manifest_path=mpath)


def load_manifest(operator_state_dir: str, manifest_id: str) -> dict | None:
    mpath = os.path.join(operator_state_dir, "manifests",
                         f"{manifest_id}.json")
    if not os.path.exists(mpath):
        return None
    import json
    with open(mpath, "r", encoding="utf-8") as fh:
        return json.load(fh)


def manifest_integrity(doc: dict) -> str | None:
    """Recompute the content address; None when the stored document was
    tampered with."""
    body = {k: v for k, v in doc.items()
            if k not in ("id", "captured_at")}
    if content_id(body) != doc.get("id"):
        return "MANIFEST_TAMPER_DIGEST_MISMATCH"
    return None


@dataclass
class ControllerBinding:
    """Attempt/relaunch binding of the controller process (C-1 step C)."""
    attempt_id: str
    root: str
    manifest_id: str
    pid: int
    starttime: str
    env_claims: dict[str, str] = field(default_factory=dict)


@dataclass
class C4pResult:
    passed: bool
    checks: list[dict] = field(default_factory=list)
    @property
    def failures(self) -> list[str]:
        return [c["name"] for c in self.checks if not c["ok"]]


def _check(name: str, ok: bool, detail: str = "") -> dict:
    return {"name": name, "ok": ok, "detail": detail}


def verify_c4p(manifest_doc: dict, binding: ControllerBinding, *,
               peer_pid: int,
               env_reader=None, stat_reader=None,
               walker=None,
               allowed_new_under: tuple[str, ...] = ("projects",)) -> C4pResult:
    """C4' — verify the ACTUAL controller process binding after start.

    Verifies (all must pass; every failure is a named check):
      PEER_PID_MATCH      the kernel-provided socket peer pid equals the
                          bound controller pid (SO_PEERCRED — unforgeable);
      PID_STARTTIME_MATCH /proc/<pid>/stat starttime equals the bound value
                          (pid-reuse defense);
      ENV_CLAUDE_CONFIG_DIR  the ACTUAL /proc/<pid>/environ carries
                          CLAUDE_CONFIG_DIR equal to the manifest scope dir;
      ENV_BINDING_KEYS    every other bound env key matches the ACTUAL
                          initial environment;
      MANIFEST_INTEGRITY  the stored manifest still hashes to its bound id;
      SCOPE_CONSISTENCY   current observed tree is a subset of the manifest
                          plus the controller's OWN current-session project
                          slug subtree (single new projects/<slug>/ tree);
                          modified/deleted manifest entries are tamper;
      NO_NEW_SKILLS       no skills/ entries exist beyond the manifest.
    """
    checks: list[dict] = []
    env_reader = env_reader or proc_environ
    stat_reader = stat_reader or proc_starttime
    walker = walker or walk_scope

    checks.append(_check("PEER_PID_MATCH", peer_pid == binding.pid,
                         f"peer={peer_pid} bound={binding.pid}"))

    starttime = stat_reader(binding.pid)
    checks.append(_check(
        "PID_STARTTIME_MATCH",
        starttime is not None and starttime == binding.starttime,
        f"actual={starttime} bound={binding.starttime}"))

    environ = env_reader(binding.pid)
    if environ is None:
        checks.append(_check("ENV_CLAUDE_CONFIG_DIR", False,
                             "controller /proc/<pid>/environ unreadable"))
        checks.append(_check("ENV_BINDING_KEYS", False,
                             "controller /proc/<pid>/environ unreadable"))
    else:
        actual_ccd = environ.get("CLAUDE_CONFIG_DIR")
        checks.append(_check(
            "ENV_CLAUDE_CONFIG_DIR",
            actual_ccd == manifest_doc["config_dir"]
            and binding.env_claims.get("CLAUDE_CONFIG_DIR")
            == manifest_doc["config_dir"],
            f"actual={actual_ccd!r} manifest={manifest_doc['config_dir']!r}"))
        for key, claimed in binding.env_claims.items():
            if key == "CLAUDE_CONFIG_DIR":
                continue
            checks.append(_check(
                f"ENV_BINDING_KEYS:{key}",
                environ.get(key) == claimed,
                f"actual={environ.get(key)!r} claimed={claimed!r}"))

    tamper = manifest_integrity(manifest_doc)
    checks.append(_check("MANIFEST_INTEGRITY", tamper is None, tamper or ""))

    try:
        current = walker(manifest_doc["config_dir"])
    except Exception as exc:  # noqa: BLE001 — any walk failure fails closed
        checks.append(_check("SCOPE_CONSISTENCY", False, repr(exc)))
        current = None
    if current is not None:
        manifest_entries = manifest_doc["entries"]
        problems: list[str] = []
        for rel, entry in sorted(manifest_entries.items()):
            cur = current.get(rel)
            if cur is None:
                problems.append(f"DELETED:{rel}")
                continue
            for key in ("type", "mode", "size"):
                if entry.get(key) is not None and entry[key] != cur.get(key):
                    problems.append(f"MODIFIED:{rel}:{key}")
            if entry["type"] == "file":
                if entry.get("sensitive"):
                    if entry["mtime_ns"] != cur.get("mtime_ns"):
                        problems.append(f"MODIFIED:{rel}:mtime_sensitive")
                elif entry.get("sha256") != cur.get("sha256"):
                    problems.append(f"MODIFIED:{rel}:content")
                if entry.get("mtime_ns") != cur.get("mtime_ns") and \
                        entry.get("sha256") == cur.get("sha256") and \
                        not entry.get("sensitive"):
                    # content-identical touch of a non-sensitive file is a
                    # metadata-only change; recorded, not fatal
                    pass
            if entry["type"] == "symlink" and entry.get("target") != cur.get(
                    "target"):
                problems.append(f"MODIFIED:{rel}:target")
        new_paths = sorted(set(current) - set(manifest_entries))
        new_skills = [p for p in new_paths
                      if p == "skills" or p.startswith("skills/")]
        tops = {p.split("/")[0] for p in new_paths}
        allowed_roots = set(allowed_new_under)
        problems_here: list[str] = []
        for top in allowed_roots:
            under = [p for p in new_paths if p.split("/")[0] == top]
            if top == "projects" and under:
                # entries strictly UNDER projects/ (the projects/ dir
                # node itself is the container, not a slug); exactly ONE
                # new slug — the controller's OWN current-session tree
                slugs = {p.split("/")[1] for p in under if "/" in p}
                if len(slugs) != 1 or any("/" not in p and p != "projects"
                                          for p in under):
                    problems_here.append(
                        "UNBOUND_EXTRA_PROJECT_STATE:" + ",".join(
                            sorted(slugs | {p for p in under
                                            if "/" not in p})))
        if any(t not in allowed_roots for t in tops):
            problems_here.append(
                "UNBOUND_EXTRA_STATE_TOPS:" + ",".join(
                    sorted(t for t in tops if t not in allowed_roots)))
        problems.extend(problems_here)
        checks.append(_check(
            "NO_NEW_SKILLS", not new_skills,
            ",".join(new_skills)))
        checks.append(_check(
            "SCOPE_CONSISTENCY", not problems, ";".join(problems[:20])))

    passed = all(c["ok"] for c in checks)
    return C4pResult(passed=passed, checks=checks)
