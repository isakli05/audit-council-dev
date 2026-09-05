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
    """Bind-mount roots for the REAL codex toolchain only (resolved
    via `which codex`): its bin dir, its realpath dir, and the enclosing
    version-style root (…/versions/<node-dir>/<version>/…) when present.

    R5 NEW-1 / da27c0: a caller-supplied --codex-bin NEVER contributes a
    DIRECTORY bind (its siblings would become readable); a non-standard
    binary is bound as a single FILE by _tool_file instead.

    da27c0 fix: the nvm version walk sliced one component short
    (…/versions/node instead of …/versions/node/v24.14.0) and dirs that
    already end in /bin were later suffixed again (/bin/bin), leaving the
    toolchain out of PATH — the production execvp/libada failures."""
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
            parts = Path(rp).resolve().parts
            for i, part in enumerate(parts):
                # nvm-style layout: …/versions/<node-dir>/<version>/…
                if part == "versions":
                    if i + 3 < len(parts):
                        add(os.path.join(*parts[:i + 3]))
                    elif i + 2 < len(parts):
                        add(os.path.join(*parts[:i + 2]))
        except OSError:
            pass
    return roots


def _toolchain_bindirs(tool_dirs: list[str]) -> list[str]:
    """PATH entries derived from the resolved toolchain: every bound dir
    that IS a bin dir (basename 'bin', realpath-resolved) plus the bin dir
    of the resolved `node` binary. Deterministic, toolchain FIRST — the
    broken system node (/usr/bin/node on this host) must never shadow it
    (da27c0 root cause 2)."""
    bins: list[str] = []
    for d in tool_dirs:
        real = os.path.realpath(d)
        if os.path.basename(real) == "bin" and real not in bins:
            bins.append(real)
    node = shutil.which("node")
    if node:
        nd = os.path.realpath(os.path.dirname(os.path.abspath(node)))
        if os.path.basename(nd) == "bin" and nd not in bins:
            bins.append(nd)
    return bins


def _resolver_binds() -> list[tuple[str, str]]:
    """da27c0 DNS fix: /etc/resolv.conf is typically a symlink into the
    host runtime (here /run/systemd/resolve/stub-resolv.conf). Binding
    /etc read-only binds the SYMLINK, not its target — inside bwrap it
    dangles and every lookup fails (the observed codex_models_manager
    refresh timeouts). Minimal fix: bind exactly the resolved target FILE
    at its real path, read-only. Nothing else under /run is exposed."""
    binds: list[tuple[str, str]] = []
    for conf in ("/etc/resolv.conf",):
        try:
            if not os.path.islink(conf):
                continue
            target = os.path.realpath(conf)
            if os.path.isfile(target) and not target.startswith("/etc/"):
                binds.append((target, target))
        except OSError:
            continue
    return binds


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
    for target in _resolver_binds():
        argv += ["--ro-bind", target[0], target[1]]
    codex_home = os.path.join(home, ".codex")
    if os.path.isdir(codex_home):
        argv += ["--bind", codex_home, codex_home]
    tool_dirs = _toolchain_roots(codex_argv[0])
    argv += ["--tmpfs", "/tmp"]
    for root in tool_dirs:
        argv += ["--ro-bind", root, root]
    # v2.0.1 N2: the resolved node bin dir must be BOUND, not merely on
    # PATH — when codex and node resolve from different trees the PATH
    # entry would otherwise be dead and node would fall back to the
    # broken system node
    for bdir in _toolchain_bindirs(tool_dirs):
        if not any(os.path.realpath(bdir) == os.path.realpath(d)
                   for d in tool_dirs):
            argv += ["--ro-bind-try", bdir, bdir]
    covered = ["/usr", "/etc", "/lib", "/lib64", "/lib32", *tool_dirs]
    tool_file = _tool_file(codex_argv[0])
    if tool_file:
        real_tf = os.path.realpath(tool_file)
        if not any(real_tf == c or real_tf.startswith(c + os.sep)
                   for c in covered if os.path.isdir(c)):
            # only bind files the standard/dir binds do not already cover
            # (mounting onto a symlink destination would fail anyway); kept
            # AFTER --tmpfs /tmp so a tool file under /tmp is not shadowed
            argv += ["--ro-bind", tool_file, tool_file]
    argv += ["--ro-bind", repo_root, repo_root]
    # the run dir sits inside the repo (audit-output/...) and must be the
    # ONE writable subtree of the repository
    argv += ["--bind", run_dir, run_dir]
    for root in (allowed_roots or []):
        argv += ["--ro-bind", root, root]
    argv += ["--dev", "/dev", "--proc", "/proc"]
    argv += ["--setenv", "HOME", home]
    # da27c0 fix: the resolved toolchain bin dirs MUST lead PATH — bare
    # `codex` / `env node` inside the sandbox previously resolved to
    # nothing (execvp failure) or to the broken system node (libada.so.3)
    tool_bins = _toolchain_bindirs(tool_dirs)
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


def sandbox_preflight(repo_root: str, run_dir: str,
                      allowed_roots: list[str] | None = None,
                      timeout: int = 60) -> dict:
    """da27c0 hardening: ZERO-INFERENCE viability proof of the exact
    production bubblewrap environment, BEFORE any frontier invocation is
    launched or counted. Eight probes, all through build_sandbox_argv
    with the resolved qualified toolchain:

      1 codex executable works          (codex --version)
      2 intended node runtime works     (node --version; NOT /usr/bin/node)
      3 codex login status succeeds     (subscription auth)
      4 chatgpt.com resolution works    (resolver, incl. symlinked conf)
      5 repo read succeeds
      6 repo write FAILS                (read-only bind)
      7 outside-root user-data read FAILS
      8 run-dir output write succeeds

    Returns {"ok": bool, "failures": [names], "details": {...}}. A
    failure is an Audit Council environment/harness failure
    (INVALID_AUDIT_ENVIRONMENT:SANDBOX_PREFLIGHT_*) — never a model
    attempt and never a product verdict."""
    failures: list[str] = []
    details: dict = {}

    if not bwrap_available():
        return {"ok": False,
                "failures": ["bwrap_missing"],
                "details": {"note": "AC_CODEX_BWRAP=0 or bwrap absent — "
                                    "confinement degraded posture; "
                                    "preflight cannot prove viability"}}

    home = os.path.expanduser("~")
    probe_outside = os.path.join(home, ".audit-council-sbx-probe-secret")
    repo_file = os.path.join(repo_root, ".ac-sbx-probe")
    run_file = os.path.join(run_dir, ".ac-sbx-probe")

    def run(payload):
        argv = build_sandbox_argv(payload, repo_root, run_dir,
                                  allowed_roots or [])
        return subprocess.run(argv, capture_output=True, text=True,
                              timeout=timeout)

    # fresh probe fixtures (removed afterwards)
    try:
        try:
            with open(repo_file, "w") as fh:
                fh.write("repo-probe\n")
            with open(probe_outside, "w") as fh:
                fh.write("user-data-probe\n")
        except OSError as exc:
            # v2.0.1 N1: a planted/conflicting probe path must produce a
            # sanctioned preflight failure, never a traceback
            return {"ok": False,
                    "failures": ["preflight_probe_conflict"],
                    "details": {"probe_error": repr(exc)[:120]}}

        try:
            p = run(["codex", "--version"])
            details["codex_version"] = p.stdout.strip()[:60]
            if p.returncode != 0 or "codex-cli" not in p.stdout:
                failures.append("codex_executable")
        except Exception as exc:
            failures.append("codex_executable"); details["codex_version"] = repr(exc)[:80]

        try:
            p = run(["sh", "-c", "command -v node && node --version"])
            details["node"] = p.stdout.strip().replace("\n", " ")[:100]
            resolved = p.stdout.splitlines()[0].strip() if p.stdout else ""
            if p.returncode != 0 or resolved == "/usr/bin/node":
                failures.append("node_runtime")
        except Exception as exc:
            failures.append("node_runtime"); details["node"] = repr(exc)[:80]

        try:
            p = run(["codex", "login", "status"])
            details["login"] = (p.stdout + p.stderr).strip()[:80]
            if p.returncode != 0 or "Logged in" not in (p.stdout + p.stderr):
                failures.append("codex_login")
        except Exception as exc:
            failures.append("codex_login"); details["login"] = repr(exc)[:80]

        try:
            p = run(["/usr/bin/python3", "-c",
                     "import socket,sys;"
                     "sys.stdout.write(socket.gethostbyname("
                     "'chatgpt.com'))"])
            details["dns"] = p.stdout.strip()[:60]
            if p.returncode != 0 or not p.stdout.strip():
                failures.append("dns_resolution")
        except Exception as exc:
            failures.append("dns_resolution"); details["dns"] = repr(exc)[:80]

        try:
            p = run(["cat", repo_file])
            if p.returncode != 0:
                failures.append("repo_read")
        except Exception:
            failures.append("repo_read")

        try:
            p = run(["sh", "-c", "echo x >> " + repo_file])
            if p.returncode == 0:
                failures.append("repo_write_must_fail")
        except Exception:
            pass  # an exception here means no write happened: pass

        try:
            p = run(["cat", probe_outside])
            if p.returncode == 0:
                failures.append("outside_read_must_fail")
        except Exception:
            pass

        try:
            p = run(["sh", "-c", "echo x > " + run_file])
            if p.returncode != 0:
                failures.append("run_dir_write")
        except Exception:
            failures.append("run_dir_write")
    finally:
        for path in (repo_file, run_file, probe_outside):
            try:
                os.unlink(path)
            except OSError:
                pass

    return {"ok": not failures, "failures": failures, "details": details}
