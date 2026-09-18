"""Outer boundary — merged-usr-aware minimal-bind namespace composition.

Carries forward the demonstrated boundary mechanics (A0 spike + the
accepted AUCDEV-023 G-2 closure), adapted to bubblewrap >= 0.10 fd
semantics, and the IR-002 remediation delta:

* TRUSTED CODE/CONFIG/EXECUTABLE BYTES enter ONLY as memfd-backed data
  files (``--ro-bind-data`` from supervisor-held fds): the harness tree
  materialized at ``/opt/qh``, the rendered restricted profile config and
  the verified provider executable are the EXACT verified snapshot bytes
  — no host-path code executes inside the protected launch, closing the
  controller-selected ``harness_root``/boundary-child substitution window
  mechanically (bwrap copies the fd bytes at sandbox setup; later
  host-side writes cannot reach the materialized files);
* evidence/target mount from SPEC-BOUND host sources (object identity +
  content digest verified by the supervisor immediately before launch and
  re-verified INSIDE the boundary before payload exec); auditor-output is
  the ONE rw bind, its host source SPEC-bound;
* credential bytes materialize from the sealed-custody memfd via
  ``--bind-data`` at the SPEC-BOUND adapter target path inside the
  boundary-private provider home (ephemeral, removed with the namespace);
* network namespace unshared with loopback DOWN (hard no-egress frozen
  profile — the boundary wraps bwrap in ``unshare --user --map-root-user
  --net`` because bwrap's own ``--unshare-net`` raises lo); PID/IPC/UTS
  unshared; host AF_UNIX escape paths masked by absence; environment
  cleared then set; the no-egress gate runs INSIDE this environment
  BEFORE the payload exec and inherited socket FD count must be ZERO.
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
class DataFile:
    """One memfd-backed immutable file materialized inside the boundary.
    ``secret=True`` files are verified by LENGTH ONLY in-child (values are
    never read/printed); non-secret code/config bytes are verified by
    SHA-256 in-child as a second integrity proof."""
    fd: int
    inner_path: str
    sha256: str
    secret: bool
    mode: int = 0o600
    length: int = 0
    readonly: bool = True

    def __post_init__(self) -> None:
        if not self.length:
            try:
                self.length = os.fstat(self.fd).st_size
            except OSError:
                self.length = 0


@dataclass
class BoundarySpec:
    harness_root: str                       # provenance data (identity)
    payload_argv: list[str] | None = None   # None => gate-only launch
    ro_binds: list[tuple[str, str]] = field(default_factory=list)
    rw_binds: list[tuple[str, str]] = field(default_factory=list)
    tmpfs_paths: list[str] = field(default_factory=lambda: ["/tmp"])
    env: dict[str, str] = field(default_factory=dict)
    secret_plans: list[ChildSecretPlan] = field(default_factory=list)
    data_files: list[DataFile] = field(default_factory=list)
    source_digests: dict[str, str] = field(default_factory=dict)
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


def snapshot_data_files(harness_root: str, *,
                        config: bytes | None = None,
                        config_target: str = "/run-qh/codex-home/config.toml",
                        extra: list[DataFile] | None = None) -> list[DataFile]:
    """Snapshot the harness executable byte set (and optionally the
    rendered config) into process-bound memfds for a boundary launch.
    Used by the supervisor at verification time and by deterministic
    tests that drive the boundary directly."""
    import hashlib
    from .trusted_spec import harness_snapshot_files
    files: list[DataFile] = []
    for rel, abspath in harness_snapshot_files(harness_root):
        with open(abspath, "rb") as fh:
            data = fh.read()
        files.append(DataFile(
            fd=_memfd_hold(data, f"qh-code-{rel.replace('/', '-')}"),
            inner_path=f"/opt/qh/{rel}",
            sha256=hashlib.sha256(data).hexdigest(),
            secret=False, mode=0o644))
    files.extend(_config_and_extra_data_files(
        config, config_target, extra))
    return files


def snapshot_data_files_from_files(bundle_files: dict[str, bytes], *,
                                   config: bytes | None = None,
                                   config_target: str =
                                   "/run-qh/codex-home/config.toml",
                                   extra: list[DataFile] | None = None
                                   ) -> list[DataFile]:
    """The SAME trusted snapshot built from an IN-MEMORY frozen byte set
    (the authority root's sealed bootstrap bundle — CR-REMED-002): NO
    host harness read occurs at all; the code bytes that execute inside
    the boundary are exactly the frozen verified bytes."""
    import hashlib
    from .trusted_spec import HARNESS_EXEC_RELPATHS
    files: list[DataFile] = []
    for rel in sorted(HARNESS_EXEC_RELPATHS):
        if rel not in bundle_files:
            raise BoundaryError(f"FROZEN_BUNDLE_INCOMPLETE: {rel}")
        data = bundle_files[rel]
        files.append(DataFile(
            fd=_memfd_hold(data, f"qh-code-{rel.replace('/', '-')}"),
            inner_path=f"/opt/qh/{rel}",
            sha256=hashlib.sha256(data).hexdigest(),
            secret=False, mode=0o644))
    files.extend(_config_and_extra_data_files(
        config, config_target, extra))
    return files


def _config_and_extra_data_files(config, config_target, extra
                                 ) -> list[DataFile]:
    import hashlib
    files: list[DataFile] = []
    if config is not None:
        files.append(DataFile(
            fd=_memfd_hold(config, "qh-config-toml"),
            inner_path=config_target,
            sha256=hashlib.sha256(config).hexdigest(),
            secret=False, mode=0o644))
    files.extend(extra or [])
    return files


def _memfd_hold(data: bytes, name: str) -> int:
    from .util import hold_bytes_memfd
    fd, _status = hold_bytes_memfd(data, name=name)
    return fd


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
    # NOTE: NO host harness-root bind: the /opt/qh tree inside the
    # boundary is materialized EXCLUSIVELY from the verified memfd
    # snapshot (data_files below) — controller-selected code paths are
    # mechanically unreachable (IR-002).
    for src, dst in spec.ro_binds:
        argv += ["--ro-bind", os.path.abspath(src), dst]
    for src, dst in spec.rw_binds:
        argv += ["--bind", os.path.abspath(src), dst]
    argv += ["--tmpfs", "/tmp", "--tmpfs", "/run-qh"]
    for t in spec.tmpfs_paths:
        if t not in ("/tmp", "/run-qh"):
            argv += ["--tmpfs", t]
    # trusted-bytes materialization: code/config/executable (readonly
    # bind-data of the verified snapshot) and custody secrets
    for df in spec.data_files:
        argv += ["--perms", f"{df.mode:04o}"]
        kind = "--ro-bind-data" if df.readonly else "--bind-data"
        argv += [kind, str(df.fd), df.inner_path]
    for plan in spec.secret_plans:
        argv += ["--perms", f"{0o600:04o}"]
        argv += ["--bind-data", str(plan.fd), plan.target_path]
    # launch spec (no secrets) read-only inside
    argv += ["--ro-bind", spec_src, SPEC_FILE_INNER]
    # result channel: append-only file write-bound back to the launcher
    argv += ["--bind", result_src, RESULT_FILE_INNER]
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
    gate, verifies the materialized trusted bytes and custody, re-verifies
    the source digests and execs the payload.  All results come back as
    JSON lines in the write-bound result file."""
    bwrap = bwrap_path()
    if not bwrap:
        raise BoundaryError("BWRAP_UNAVAILABLE")
    parent_mntns = os.readlink("/proc/self/ns/mnt")
    spec_doc = {
        "payload_argv": spec.payload_argv,
        "tmpfs_paths": spec.tmpfs_paths,
        "rw_inner": [dst for _, dst in spec.rw_binds],
        "data_files": [{"inner_path": df.inner_path,
                        "sha256": df.sha256, "secret": df.secret,
                        "length": df.length} for df in spec.data_files],
        "secret_plans": [{"label": p.label,
                          "target_path": p.target_path,
                          "length": p.length} for p in spec.secret_plans],
        "source_digests": spec.source_digests,
        "noegress": bool(spec.noegress is not None),
        "parent_mntns_inode": parent_mntns,
        "unshare_net_in_child": spec.noegress is not None,
        "result_file": RESULT_FILE_INNER,
    }
    all_fds = [p.fd for p in spec.secret_plans] + \
        [df.fd for df in spec.data_files]
    with tempfile.TemporaryDirectory(prefix="qh-bnd-") as tdir:
        spec_src = os.path.join(tdir, "spec.json")
        result_src = os.path.join(tdir, "result.jsonl")
        # memfds are consumed by --bind-data at each launch; rewind them
        # so repeated launches materialize the full bytes
        for fd in all_fds:
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
            argv, pass_fds=tuple(all_fds),
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
