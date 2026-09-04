#!/usr/bin/env python3
"""OS-level codex confinement wrapper (v2 A0 spike — see
docs/A0-CODEX-CONFINEMENT.md).

Codex's own `--sandbox read-only` (Landlock+seccomp) prevents WRITES but
does NOT confine reads to `-C <repo>` (probed: /etc/passwd and arbitrary
/tmp secrets are readable). This module wraps every codex launch in
bubblewrap so that reads outside an enumerated bind set are
OS-ENFORCED-BLOCKED:

  ro:  /usr /lib /lib64 /etc  (toolchain + system — documented boundary)
  rw:  ~/.codex               (codex session/auth state, as on the host)
  ro:  resolved toolchain root(s) for the codex binary (e.g. an nvm
       version tree) + their bin dirs first on PATH
  ro:  the frozen repo root
  rw:  the run dir (codex -o output + run artifacts)
  ro:  explicitly authorized fixture roots (allowed_disposable_roots)
  tmpfs: /tmp (everything else under /tmp is absent)
  net:  deliberately NOT unshared (subscription API must work)

Opt-out: AC_CODEX_BWRAP=0 (or bwrap absent) → confinement degrades to the
runner policy/detection posture, recorded per job as sandbox.active=false.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def bwrap_available() -> str | None:
    if os.environ.get("AC_CODEX_BWRAP") == "0":
        return None
    return shutil.which("bwrap")


def _toolchain_roots(codex_bin: str) -> list[str]:
    """DIRECTORY bind roots for the REAL codex toolchain only (resolved
    via `which codex`): its bin dir, realpath dir, and an enclosing
    version-style root (…/versions/<v>/…) when present.

    R5 NEW-1: a caller-supplied --codex-bin NEVER contributes a DIRECTORY
    bind (its siblings would become readable); a non-standard binary is
    bound as a single FILE by _tool_file instead."""
    roots: list[str] = []
    seen: set[str] = set()

    def add(p: str | None) -> None:
        if p and p not in seen and os.path.isdir(p):
            seen.add(p)
            roots.append(p)

    real = shutil.which("codex")
    if real:
        add(os.path.dirname(os.path.abspath(real)))
        try:
            rp = os.path.realpath(real)
            add(os.path.dirname(rp))
            from pathlib import Path
            parts = Path(rp).resolve().parts
            for i, part in enumerate(parts):
                if part == "versions" and i + 2 < len(parts):
                    add(os.path.join(*parts[:i + 2]))
        except OSError:
            pass
    return roots


def _tool_file(codex_bin: str) -> str | None:
    """A non-standard --codex-bin is bound as a single FILE (read+exec of
    that file only — never its directory or siblings)."""
    try:
        real = os.path.realpath(shutil.which("codex") or "")
    except OSError:
        real = ""
    bin_path = shutil.which(codex_bin) or codex_bin
    if os.path.realpath(bin_path) == real:
        return None  # the real toolchain (already dir-bound)
    return bin_path if os.path.isfile(bin_path) else None


def build_sandbox_argv(codex_argv: list, repo_root: str, run_dir: str,
                       allowed_roots: list[str] | None = None,
                       bwrap: str | None = None) -> list:
    """Wrap codex_argv in a bubblewrap confinement invocation."""
    bwrap = bwrap or bwrap_available()
    if not bwrap:
        return list(codex_argv)
    home = os.path.expanduser("~")
    argv = [bwrap]
    argv += ["--ro-bind", "/usr", "/usr"]
    for lib in ("/lib", "/lib64", "/lib32"):
        if os.path.isdir(lib):
            argv += ["--ro-bind-try", lib, lib]
    argv += ["--ro-bind", "/etc", "/etc"]
    codex_home = os.path.join(home, ".codex")
    if os.path.isdir(codex_home):
        argv += ["--bind", codex_home, codex_home]
    tool_dirs = _toolchain_roots(codex_argv[0])
    for root in tool_dirs:
        argv += ["--ro-bind", root, root]
    covered = ["/usr", "/etc", "/lib", "/lib64", "/lib32", *tool_dirs]
    tool_file = _tool_file(codex_argv[0])
    if tool_file:
        real_tf = os.path.realpath(tool_file)
        if not any(real_tf == c or real_tf.startswith(c + os.sep)
                   for c in covered if os.path.isdir(c)):
            # only bind files the standard/dir binds do not already cover
            # (mounting onto a symlink destination would fail anyway)
            argv += ["--ro-bind", tool_file, tool_file]
    argv += ["--tmpfs", "/tmp"]
    argv += ["--ro-bind", repo_root, repo_root]
    # the run dir sits inside the repo (audit-output/...) and must be the
    # ONE writable subtree of the repository
    argv += ["--bind", run_dir, run_dir]
    for root in (allowed_roots or []):
        argv += ["--ro-bind", root, root]
    argv += ["--dev", "/dev", "--proc", "/proc"]
    argv += ["--setenv", "HOME", home]
    tool_bins = [os.path.join(r, "bin") for r in tool_dirs]
    tool_bins = [b for b in tool_bins if os.path.isdir(b)]
    path = os.pathsep.join(tool_bins + ["/usr/bin", "/bin"])
    argv += ["--setenv", "PATH", path]
    argv += codex_argv
    return argv


def wrap_codex_argv(codex_argv: list, repo_root: str, run_dir: str,
                    allowed_roots: list[str] | None = None) -> tuple:
    """Decision helper for the runner: returns (argv, active_flag).
    R5 NEW-2: the run dir must REALLY live under the repo root at wrap
    time (realpath containment) — a symlinked/moved run dir must not turn
    the rw bind into an arbitrary write grant."""
    if not bwrap_available():
        return list(codex_argv), False
    real_run = os.path.realpath(run_dir)
    real_repo = os.path.realpath(repo_root)
    if real_run != real_repo and not real_run.startswith(
            real_repo + os.sep):
        raise RuntimeError(
            f"refusing to launch: run dir {real_run} is not under the "
            f"frozen repo root {real_repo}")
    return build_sandbox_argv(codex_argv, repo_root, run_dir,
                              allowed_roots), True


def probe(bwrap: str | None = None) -> dict:
    """Deterministic capability probe (no model calls): can the wrapper
    block an outside read while allowing a repo read?"""
    import tempfile
    bwrap = bwrap or bwrap_available()
    if not bwrap:
        return {"available": False, "outside_read_blocked": None}
    with tempfile.TemporaryDirectory(prefix="ac-sbx-probe-") as base:
        repo = os.path.join(base, "repo")
        run = os.path.join(base, "run")
        os.makedirs(repo)
        os.makedirs(run)
        sentinel = os.path.join(repo, "f.txt")
        with open(sentinel, "w") as fh:
            fh.write("x\n")
        outside = os.path.join(base, "outside.txt")
        with open(outside, "w") as fh:
            fh.write("secret\n")
        argv = build_sandbox_argv(
            ["/usr/bin/cat", sentinel], repo, run, bwrap=bwrap)
        inside_ok = subprocess.run(
            argv, capture_output=True, check=False).returncode == 0
        argv_out = build_sandbox_argv(
            ["/usr/bin/cat", outside], repo, run, bwrap=bwrap)
        outside_rc = subprocess.run(
            argv_out, capture_output=True, check=False).returncode
        return {"available": True,
                "repo_read_ok": inside_ok,
                "outside_read_blocked": outside_rc != 0}
