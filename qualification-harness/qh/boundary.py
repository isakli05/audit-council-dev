"""Outer boundary — merged-usr-aware minimal-bind namespace composition.

Carries forward the demonstrated boundary mechanics (A0 spike + the
accepted AUCDEV-023 G-2 closure), adapted to bubblewrap >= 0.10 fd
semantics (--pass-fd was removed; secret material enters via
``--bind-data`` from the custody memfd, the launch spec via a read-only
bound file, and results return via a write-bound result file):

* bubblewrap assembles a fresh inner root (tmpfs scaffold — the accepted
  EPHEMERAL namespace-local residual, never a persistent host-backed
  model-write surface): only the real directories/interpreter/toolchain
  binds mechanically required for the exact executable/runtime are
  supplied (``/usr``, ``/lib*``, ``/etc`` read-only + spec-provided
  evidence/toolchain roots); NO broad host directory binds;
* network namespace unshared (hard no-egress); PID/IPC/UTS unshared;
* AF_UNIX host escape paths (``/run/systemd/resolve``, ``/run/dbus``)
  are simply NOT bound — inside the boundary they are absent, which the
  no-egress gate verifies mechanically (masking by absence under a
  private mount namespace; a bare netns would leave them reachable);
* evidence RO; target/source RO or absent per spec; auditor-output is
  the ONE rw bind; ``/tmp`` is a fresh tmpfs;
* environment CLEARED then set explicitly (env -i discipline);
* the no-egress gate runs INSIDE this environment BEFORE the payload
  exec; inherited socket FD count must be ZERO — bwrap closes every
  descriptor except stdio, so no socket can leak in with the launch;
* custody memfds are materialized by bwrap itself (``--bind-data``)
  into the boundary's ephemeral paths for the authorized child only;
  the child entry verifies presence/length and NEVER sees the fd.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field

from .custody import ChildSecretPlan
from .noegress import NoEgressSpec

RESULT_FILE_INNER = "/run-qh/result.jsonl"
SPEC_FILE_INNER = "/run-qh/spec.json"
GATE_FAIL_EXIT = 78


class BoundaryError(RuntimeError):
    pass


@dataclass
class BoundarySpec:
    harness_root: str                       # qualification-harness/ dir
    payload_argv: list[str] | None = None   # None => gate-only launch
    ro_binds: list[tuple[str, str]] = field(default_factory=list)
    rw_binds: list[tuple[str, str]] = field(default_factory=list)
    tmpfs_paths: list[str] = field(default_factory=lambda: ["/tmp"])
    env: dict[str, str] = field(default_factory=dict)
    secret_plans: list[ChildSecretPlan] = field(default_factory=list)
    noegress: NoEgressSpec | None = None
    pass_fds: list[int] = field(default_factory=list)
    unshare_pid: bool = True


@dataclass
class BoundaryResult:
    returncode: int
    records: list[dict]
    stdout: str = ""
    stderr: str = ""
    @property
    def gate(self) -> dict | None:
        for r in self.records:
            if r.get("phase") == "noegress":
                return r
        return None
    @property
    def gate_passed(self) -> bool | None:
        g = self.gate
        return None if g is None else bool(g.get("passed"))
    @property
    def payload_result(self) -> dict | None:
        for r in self.records:
            if r.get("phase") == "payload_result":
                return r
        return None
    @property
    def custody_records(self) -> list[dict]:
        return [r for r in self.records if r.get("phase") == "custody"]


def bwrap_path() -> str | None:
    return shutil.which("bwrap")


def _bwrap_argv(spec: BoundarySpec, *, spec_src: str, result_src: str,
                bwrap: str) -> list[str]:
    # NOTE: no --unshare-net here — bwrap brings the new-netns loopback
    # UP, while the frozen demonstrated no-egress profile requires lo
    # DOWN; the child entry unshares the network namespace itself
    # (fresh netns, loopback untouched/DOWN — same as the demonstrated
    # `unshare --user --map-root-user --net` environment).
    argv = [bwrap, "--unshare-ipc", "--unshare-uts"]
    if spec.unshare_pid:
        argv += ["--unshare-pid"]
    argv += ["--ro-bind", "/usr", "/usr"]
    for lib in ("/lib", "/lib64", "/lib32"):
        if os.path.isdir(lib):
            argv += ["--ro-bind-try", lib, lib]
    argv += ["--ro-bind", "/etc", "/etc"]
    # harness code itself is non-secret and read-only inside
    argv += ["--ro-bind", os.path.abspath(spec.harness_root), "/opt/qh"]
    for src, dst in spec.ro_binds:
        argv += ["--ro-bind", os.path.abspath(src), dst]
    for src, dst in spec.rw_binds:
        argv += ["--bind", os.path.abspath(src), dst]
    argv += ["--tmpfs", "/tmp", "--tmpfs", "/run-qh"]
    for t in spec.tmpfs_paths:
        if t not in ("/tmp", "/run-qh"):
            argv += ["--tmpfs", t]
    # launch spec (no secrets) read-only inside
    argv += ["--ro-bind", spec_src, SPEC_FILE_INNER]
    # result channel: append-only file write-bound back to the launcher
    argv += ["--bind", result_src, RESULT_FILE_INNER]
    # custody materialization by bwrap from the sealed memfds
    for plan in spec.secret_plans:
        argv += ["--bind-data", str(plan.fd), plan.target_path]
    argv += ["--dev", "/dev", "--proc", "/proc", "--clearenv"]
    env = {"PATH": "/usr/bin:/bin", "HOME": "/tmp", "LANG": "C.UTF-8",
           "LC_ALL": "C.UTF-8", **spec.env}
    for k in sorted(env):
        argv += ["--setenv", k, env[k]]
    argv += ["/usr/bin/python3", "/opt/qh/qh/boundary_child.py",
             "--spec-file", SPEC_FILE_INNER,
             "--result-file", RESULT_FILE_INNER]
    return argv


def launch(spec: BoundarySpec, *, timeout: float = 60.0) -> BoundaryResult:
    """Run one boundary launch.  The child entry evaluates the no-egress
    gate, verifies custody materialization and execs the payload.  All
    results come back as JSON lines in the write-bound result file."""
    bwrap = bwrap_path()
    if not bwrap:
        raise BoundaryError("BWRAP_UNAVAILABLE")
    parent_mntns = os.readlink("/proc/self/ns/mnt")
    spec_doc = {
        "payload_argv": spec.payload_argv,
        "tmpfs_paths": spec.tmpfs_paths,
        "rw_inner": [dst for _, dst in spec.rw_binds],
        "secret_plans": [{"fd": p.fd, "label": p.label,
                          "target_path": p.target_path,
                          "length": p.length} for p in spec.secret_plans],
        "noegress": bool(spec.noegress is not None),
        "parent_mntns_inode": parent_mntns,
        "unshare_net_in_child": spec.noegress is not None,
        "result_file": RESULT_FILE_INNER,
    }
    with tempfile.TemporaryDirectory(prefix="qh-bnd-") as tdir:
        spec_src = os.path.join(tdir, "spec.json")
        result_src = os.path.join(tdir, "result.jsonl")
        # custody memfds are consumed by --bind-data at each launch;
        # rewind them so repeated launches materialize the full bytes
        for fd in spec.pass_fds:
            try:
                os.lseek(fd, 0, os.SEEK_SET)
            except OSError:
                pass  # pipes are not seekable — nothing to rewind
        with open(spec_src, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(spec_doc))
        open(result_src, "w").close()
        argv = _bwrap_argv(spec, spec_src=spec_src, result_src=result_src,
                           bwrap=bwrap)
        if spec.noegress is not None:
            # fresh network namespace with loopback DOWN (frozen
            # demonstrated profile), established OUTSIDE bwrap: bwrap's
            # --unshare-net raises lo, and in-child unshare is EPERM
            # (bwrap drops capabilities).  Same chain shape as the
            # demonstrated wrapper (unshare --user --map-root-user
            # --net ...).
            unshare = shutil.which("unshare")
            if not unshare:
                raise BoundaryError("UNSHARE_UNAVAILABLE")
            argv = [unshare, "--user", "--map-root-user", "--net",
                    *argv]
        proc = subprocess.run(
            argv, pass_fds=tuple(spec.pass_fds),
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=timeout)
        records: list[dict] = []
        with open(result_src, "r", encoding="utf-8") as fh:
            for line in fh.read().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    records.append({"phase": "unparseable",
                                    "raw": line[:400]})
    return BoundaryResult(
        returncode=proc.returncode, records=records,
        stdout=proc.stdout.decode("utf-8", "replace"),
        stderr=proc.stderr.decode("utf-8", "replace"))
