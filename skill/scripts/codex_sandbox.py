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
  pid+ipc+uts namespaces: unshared (F-A-01/B-001) — /proc inside the
       sandbox shows only sandbox processes, so /proc/<pid>/root can no
       longer be used to reach the host filesystem, and process state
       (host PIDs, IPC objects, hostname) is not exposed
  env:  CLEARED, then explicitly set (HOME/PATH/TERM/LANG) — the host
       environment does not flow into the sandbox (B-001)
  net:  deliberately NOT unshared (subscription API must work)

Blind paths (B-003): `blind_paths` ro-binds /dev/null OVER a path inside
the run dir, so a first-pass codex auditor cannot read the peer auditor's
already-checkpointed artifact through the rw run-dir bind.

Opt-out: AC_CODEX_BWRAP=0 (or bwrap absent) → confinement degrades to the
runner policy/detection posture, recorded per job as sandbox.active=false.
"""
from __future__ import annotations

import os
import shutil
import stat
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
                       bwrap: str | None = None,
                       blind_paths: list[str] | None = None) -> list:
    """Wrap codex_argv in a bubblewrap confinement invocation.

    F-A-01/B-001: PID+IPC+UTS namespaces are unshared (net stays shared by
    design) and the environment is cleared to an explicit minimal set —
    see the module docstring for the exact advertised boundary.
    B-003: paths in `blind_paths` are shadowed with an empty ro-bound
    /dev/null so the sandboxed process cannot read them (first-pass
    independence for the codex independent stage).
    """
    bwrap = bwrap or bwrap_available()
    if not bwrap:
        return list(codex_argv)
    home = os.path.expanduser("~")
    argv = [bwrap]
    # F-A-01: namespaces must be unshared BEFORE /proc is mounted so the
    # in-sandbox procfs describes only the sandbox's PID namespace
    argv += ["--unshare-pid", "--unshare-ipc", "--unshare-uts"]
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
    # B-003: blind AFTER the run-dir rw bind so the mask shadows it
    for blind in (blind_paths or []):
        argv += ["--ro-bind", "/dev/null", os.path.abspath(blind)]
    for root in (allowed_roots or []):
        argv += ["--ro-bind", root, root]
    argv += ["--dev", "/dev", "--proc", "/proc"]
    # B-001: the host environment does NOT flow into the sandbox — clear
    # it, then set exactly what the toolchain needs (auth state is on disk
    # in ~/.codex, never in env vars)
    argv += ["--clearenv"]
    argv += ["--setenv", "HOME", home]
    # da27c0 fix: the resolved toolchain bin dirs MUST lead PATH — bare
    # `codex` / `env node` inside the sandbox previously resolved to
    # nothing (execvp failure) or to the broken system node (libada.so.3)
    tool_bins = _toolchain_bindirs(tool_dirs)
    path = os.pathsep.join(tool_bins + ["/usr/bin", "/bin"])
    argv += ["--setenv", "PATH", path]
    argv += ["--setenv", "TERM", "dumb"]
    argv += ["--setenv", "LANG", "C.UTF-8"]
    argv += codex_argv
    return argv


def wrap_codex_argv(codex_argv: list, repo_root: str, run_dir: str,
                    allowed_roots: list[str] | None = None,
                    blind_paths: list[str] | None = None) -> tuple:
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
                              allowed_roots, blind_paths=blind_paths), True


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


def _create_probe_fixture(path: str, content: bytes,
                          created: list) -> None:
    """F-A1 hardening: create a probe file this invocation OWNS.

    Atomic exclusive creation (O_CREAT|O_EXCL, plus O_NOFOLLOW where
    supported): a pre-existing object at the predictable probe path —
    regular file OR symlink — fails with EEXIST instead of being
    followed, truncated, or written through. The (st_dev, st_ino)
    identity of the object WE created is recorded so cleanup removes
    exactly that object and nothing else."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    try:
        os.write(fd, content)
    finally:
        os.close(fd)
    st = os.lstat(path)
    created.append((path, st.st_dev, st.st_ino))


def _cleanup_probe_fixtures(created: list) -> None:
    """F-A1 hardening: unlink only objects whose recorded (st_dev,
    st_ino) identity still matches the fixture this invocation created;
    a path that was swapped — or was never ours — is left alone."""
    for path, dev, ino in reversed(created):
        try:
            st = os.lstat(path)
        except OSError:
            continue
        if (st.st_dev, st.st_ino) != (dev, ino):
            continue
        if not stat.S_ISREG(st.st_mode):
            continue
        try:
            os.unlink(path)
        except OSError:
            pass


def _first_existing_repo_file(repo_root: str) -> str | None:
    """An EXISTING regular file inside repo_root for the read probe (no
    repository byte is ever created or written by preflight). Prefer
    .git/HEAD (present in every git worktree — a file in plain repos, a
    gitdir pointer in linked worktrees), else the first regular file of a
    deterministic bounded walk that skips .git and audit-output."""
    head = os.path.join(repo_root, ".git", "HEAD")
    try:
        if os.path.isfile(head):
            return head
    except OSError:
        pass
    visited = 0
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in (".git", "audit-output"))
        for name in sorted(filenames):
            cand = os.path.join(dirpath, name)
            try:
                if os.path.isfile(cand):
                    return cand
            except OSError:
                continue
        visited += 1
        if visited > 500:  # bounded walk; repos always have shallow files
            break
    return None


def sandbox_preflight(repo_root: str, run_dir: str,
                      allowed_roots: list[str] | None = None,
                      timeout: int = 60,
                      codex_bin: str = "codex",
                      dns_probe_host: str = "chatgpt.com") -> dict:
    """da27c0 hardening: ZERO-INFERENCE viability proof of the exact
    production bubblewrap environment, BEFORE any frontier invocation is
    launched or counted. Nine probes, all through build_sandbox_argv:

      1 codex executable works          (<codex_bin> --version)
      2 intended node runtime works     (node --version; NOT /usr/bin/node)
      3 codex login status succeeds     (subscription auth)
      4 chatgpt.com resolution works    (resolver, incl. symlinked conf)
      5 repo read succeeds              (an EXISTING repo file)
      6 repo write FAILS                (read-only bind; attempted creation
                                         of .ac-sbx-write-probe at the repo
                                         root must be refused by the OS)
      7 outside-root read FAILS         (preflight-owned tempdir sentinel)
      7b /proc/<pid>/root escape FAILS  (PID namespace confinement)
      8 run-dir output write succeeds   (inside the sanctioned writable
                                         subtree only)

    F-A-02/B-002: preflight creates NO probe file in the frozen repository
    or in the operator's home. The repo-read probe reads an existing file;
    the only created fixtures are (a) the outside sentinel in a
    preflight-owned `tempfile.mkdtemp` and (b) the run-dir probe inside the
    run's own sanctioned writable directory. The repo-write probe attempts
    to CREATE `<repo_root>/.ac-sbx-write-probe` and requires the OS to
    refuse; the only situation in which that file can appear is an already
    broken read-only bind, which is itself the reported failure.

    F-A-03: every probe is an argv VECTOR — no shell string concatenation,
    so whitespace in any path can never vacate a proof.

    F-A-06: probes 1 and 3 use `codex_bin` — the exact binary the run will
    launch — never an implicitly host-PATH-resolved codex.

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

    resolved_codex = shutil.which(codex_bin) or codex_bin
    # the node-runtime probe validates the PRODUCTION toolchain (the
    # PATH-resolved codex and its node). When the run launches an
    # explicitly supplied alternative binary (e.g. a test fixture), that
    # binary's runtime is its own business and the probe is recorded as
    # not applicable instead of fabricating a host-node dependence.
    default_codex = shutil.which("codex")
    node_probe_applies = (codex_bin == "codex"
                          or (default_codex is not None
                              and os.path.realpath(resolved_codex)
                              == os.path.realpath(default_codex)))
    # operator-visible probe-host override (default chatgpt.com; the
    # subscription API domain the launch needs to resolve)
    dns_host = os.environ.get("AC_SANDBOX_DNS_PROBE_HOST") or dns_probe_host
    repo_candidate = _first_existing_repo_file(repo_root)
    if repo_candidate is None:
        return {"ok": False,
                "failures": ["repo_read_no_candidate"],
                "details": {"note": "no existing regular file found in "
                                    "the repo root to read-probe with"}}

    import tempfile
    with tempfile.TemporaryDirectory(prefix="ac-sbx-probe-") as probe_root:
        outside = os.path.join(probe_root, "outside-secret.txt")
        run_file = os.path.join(run_dir, ".ac-sbx-probe")
        repo_write_probe = os.path.join(repo_root, ".ac-sbx-write-probe")

        def run(payload, input_text=None):
            argv = build_sandbox_argv(payload, repo_root, run_dir,
                                      allowed_roots or [])
            return subprocess.run(argv, capture_output=True, text=True,
                                  timeout=timeout, input=input_text,
                                  stdin=subprocess.DEVNULL
                                  if input_text is None else None)

        # fresh probe fixtures — atomic, exclusive, ownership-tracked (F-A1)
        created: list = []
        try:
            try:
                _create_probe_fixture(outside, b"outside-probe\n", created)
                _create_probe_fixture(run_file, b"run-probe\n", created)
            except OSError as exc:
                # v2.0.1 N1 / F-A1: a planted or conflicting probe path
                # (symlink OR regular file) must produce a sanctioned
                # preflight failure — never a traceback, never a
                # write-through or truncation of the pre-existing object
                return {"ok": False,
                        "failures": ["preflight_probe_conflict"],
                        "details": {"probe_error": repr(exc)[:120]}}

            try:
                p = run([resolved_codex, "--version"])
                details["codex_version"] = p.stdout.strip()[:60]
                if p.returncode != 0 or "codex-cli" not in p.stdout:
                    failures.append("codex_executable")
            except Exception as exc:
                failures.append("codex_executable")
                details["codex_version"] = repr(exc)[:80]

            try:
                if node_probe_applies:
                    p = run(["sh", "-c", "command -v node && node --version"])
                    details["node"] = p.stdout.strip().replace("\n", " ")[:100]
                    resolved = p.stdout.splitlines()[0].strip() if p.stdout else ""
                    if p.returncode != 0 or resolved == "/usr/bin/node":
                        failures.append("node_runtime")
                else:
                    details["node"] = ("not applicable: non-default "
                                       "codex binary (its runtime is its "
                                       "own)")
            except Exception as exc:
                if node_probe_applies:
                    failures.append("node_runtime")
                    details["node"] = repr(exc)[:80]

            try:
                p = run([resolved_codex, "login", "status"])
                details["login"] = (p.stdout + p.stderr).strip()[:80]
                if p.returncode != 0 or "Logged in" not in (p.stdout + p.stderr):
                    failures.append("codex_login")
            except Exception as exc:
                failures.append("codex_login"); details["login"] = repr(exc)[:80]

            try:
                p = run(["python3", "-c",
                         "import socket,sys;"
                         "sys.stdout.write(socket.gethostbyname("
                         + repr(dns_host) + "))"])
                details["dns"] = p.stdout.strip()[:60]
                if p.returncode != 0 or not p.stdout.strip():
                    failures.append("dns_resolution")
            except Exception as exc:
                failures.append("dns_resolution"); details["dns"] = repr(exc)[:80]

            try:
                p = run(["cat", repo_candidate])
                if p.returncode != 0:
                    failures.append("repo_read")
            except Exception:
                failures.append("repo_read")

            try:
                p = run(["touch", repo_write_probe])
                if p.returncode == 0:
                    failures.append("repo_write_must_fail")
            except Exception:
                pass  # an exception here means no write happened: pass

            try:
                p = run(["cat", outside])
                if p.returncode == 0:
                    failures.append("outside_read_must_fail")
            except Exception:
                pass

            try:
                # F-A-01: a mount-namespace-only sandbox without PID
                # isolation exposes the HOST root through /proc/1/root;
                # with --unshare-pid the escape path must be absent.
                # (`outside` is absolute, so plain concatenation — join
                # would discard the /proc/1/root prefix.)
                p = run(["cat", "/proc/1/root" + outside])
                if p.returncode == 0:
                    failures.append("proc_root_escape_must_fail")
            except Exception:
                pass

            try:
                p = run(["tee", run_file], input_text="x\n")
                if p.returncode != 0:
                    failures.append("run_dir_write")
            except Exception:
                failures.append("run_dir_write")
        finally:
            # F-A1: remove ONLY fixtures this invocation created, by inode
            # identity — never a path merely because its name is predictable
            _cleanup_probe_fixtures(created)

    return {"ok": not failures, "failures": failures, "details": details}
