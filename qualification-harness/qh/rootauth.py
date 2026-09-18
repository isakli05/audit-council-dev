"""IR-001 remediation + CR-REMED-002/003/004 hardening — the mechanically
rooted OPERATOR AUTHORITY ROOT.

The production launch authority has an actual mechanical root of trust
OUTSIDE the untrusted same-UID controller:

* the operator establishes ``qh root`` BEFORE controller-controlled request
  execution, delivering the two out-of-band inputs a controller cannot
  manufacture — the COMPLETE pre-authorized trusted launch spec and the
  provider credential bytes (both ONLY through operator-held capability
  channels: pipes or fully sealed memfds — CR-REMED-003);

* the root immediately becomes non-dumpable (PR_SET_DUMPABLE=0) and
  requires Yama ptrace_scope >= 1 (real kernel read; no override exists
  anywhere on the production path);

* authority-critical state (the canonical spec bytes and the credential
  custody bytes) is held ONLY in MANDATORILY SEALED memfds (the corrected
  four-seal UAPI representation, CR-REMED-001) inside the non-dumpable
  root process — sealing is never optional and never downgraded;

* the COMPLETE privileged bootstrap byte set is verified against the
  trusted spec identity, IMPORTED into the root process, and frozen into
  a sealed authority-held bundle BEFORE the controller-accessible trigger
  is exposed (CR-REMED-002); from that moment a meta_path guard refuses
  every NEW qh.* import, so later host-tree mutation can never load
  attacker code into the authority process;

* the authorized CONTROLLER identity (uid/pid/starttime) is OPERATOR-
  authored inside the trusted spec (CR-REMED-004); the root enforces the
  exact SO_PEERCRED uid/pid plus the ACTUAL /proc starttime of the mint
  peer BEFORE minting — the first compatible same-UID peer can no longer
  define itself as the controller (a wrong peer terminally consumes the
  one-shot root: acceptable fail-closed DoS, recorded);

* the one-shot supervisor is created by ``fork()`` from the ALREADY-LOADED
  trusted root process — privileged code bytes are NEVER re-imported from
  the ordinary mutable host harness tree after the trigger is exposed
  (the previous fresh-interpreter supervisor spawn with a host-tree
  module search path is REMOVED from the production path);

* the public unrestricted ``qh mint`` surface is REMOVED from production:
  the only production mint is performed by THIS root, for EXACTLY the one
  attempt id bound in its spec, at most ONCE;

* a controller-created parallel root can at most mint a powerless
  imitation: it holds no real credential bytes and no operator-authorized
  spec, so nothing it spawns can perform a provider-capable launch;

* root SIGKILL is fail-closed denial (DoS) only — authority dies with the
  process and nothing on the filesystem can restore it.
"""
from __future__ import annotations

import importlib
import json
import os
import select
import socket
import struct
import sys
import time

from . import trusted_spec
from .authority import Grant, mint_attempt_grant
from .ledger import ObservabilityLedger
from .trusted_spec import HARNESS_EXEC_RELPATHS
from .util import (Redactor, SealUnavailableError, fd_source_kind,
                   hold_bytes_memfd,
                   memfd_seal_capability as _memfd_seal_capability,
                   proc_starttime, read_yama_ptrace_scope, sha256_bytes)

SO_PEERCRED = 17
MAX_CUSTODY_BYTES = 65536
ROOT_CUSTODY_LABEL = "root-provider-custody"

# The privileged byte set = the spec's exact executable byte set (19 qh
# modules + the two in-boundary payload fixtures).  Every harness-local
# module that can influence root authority, grant creation, supervisor
# startup, spec verification, C4', custody, no-egress, policy freezing,
# GATE-W, boundary construction and the protected launch is in this set.
PRIVILEGED_BOOTSTRAP_RELPATHS = HARNESS_EXEC_RELPATHS
PRIVILEGED_MODULES = tuple(
    ("qh" if rel == "qh/__init__.py"
     else "qh." + rel[len("qh/"):-len(".py")].replace("/", "."))
    for rel in PRIVILEGED_BOOTSTRAP_RELPATHS
    if rel.startswith("qh/") and rel.endswith(".py"))

# External trusted-computing-base assumptions (documented, NOT loaded from
# the ordinary harness tree): the Python interpreter + stdlib (importlib,
# json, os, socket, struct, subprocess, ctypes, select, hashlib, ...),
# bwrap(1), unshare(1) and the host /proc, /usr, /lib trees the boundary
# read-only binds at launch.  Only harness-LOCAL code is frozen here.
EXTERNAL_TCB_ASSUMPTIONS = (
    "python interpreter + stdlib", "bwrap", "unshare",
    "host /usr,/lib,/etc,/proc (boundary RO binds)")


class RootInitError(RuntimeError):
    """Fail-closed authority-root initialization failure."""


PR_SET_DUMPABLE = 4


def pr_set_dumpable(value: int) -> None:
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(PR_SET_DUMPABLE, value, 0, 0, 0) != 0:
        raise RootInitError("PR_SET_DUMPABLE_FAILED")


def memfd_seal_capability() -> str:
    return _memfd_seal_capability()  # re-export of the corrected probe


def hold_authority_bytes(data: bytes, *, name: str) -> tuple[int, str]:
    """Hold authority-critical bytes in a MANDATORILY SEALED process-bound
    memfd (corrected four-seal UAPI representation; fail closed through
    RootInitError — there is no optional downgrade)."""
    try:
        return hold_bytes_memfd(data, name=name)
    except SealUnavailableError as exc:
        raise RootInitError(str(exc)) from exc


# ------------------------------------------------- privileged bootstrap ----

def _bundle_pack(files: dict[str, bytes]) -> bytes:
    """Deterministic length-prefixed container for the frozen byte set."""
    out = bytearray()
    for rel in sorted(files):
        raw_rel = rel.encode("utf-8")
        out += struct.pack(">I", len(raw_rel)) + raw_rel
        out += struct.pack(">Q", len(files[rel])) + files[rel]
    return bytes(out)


def _bundle_unpack(blob: bytes) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    i = 0
    while i < len(blob):
        (rl,) = struct.unpack_from(">I", blob, i)
        i += 4
        rel = blob[i:i + rl].decode("utf-8")
        i += rl
        (dl,) = struct.unpack_from(">Q", blob, i)
        i += 8
        files[rel] = blob[i:i + dl]
        i += dl
    return files


class _FrozenImportGuard:
    """meta_path finder that refuses every NEW qh/qh.* import after the
    privileged bootstrap freeze (planted modules and lazy host re-imports
    fail closed instead of loading possibly-attacker-controlled code)."""

    def find_spec(self, fullname, path=None, target=None):  # noqa: ARG002
        if fullname == "qh" or fullname.startswith("qh."):
            if fullname not in sys.modules:
                raise ImportError(
                    f"QH_IMPORT_FROZEN: {fullname} — the privileged "
                    "bootstrap is frozen; new harness-local imports from "
                    "the ordinary host tree are refused")
        return None


class PrivilegedBootstrap:
    """The immutable authority-held representation of the COMPLETE
    privileged code byte set (CR-REMED-002).

    ``freeze`` reads the exact spec-pinned byte set from the harness root,
    verifies it against the trusted spec identity, imports every
    privileged module into THIS process, packs the bytes into a
    MANDATORILY SEALED memfd and records per-module identities.  The root
    exposes its controller trigger only AFTER a successful freeze; the
    supervisor is then forked from this already-loaded state."""

    def __init__(self, *, harness_root: str, files: dict[str, bytes],
                 bundle_fd: int, bundle_digest: str,
                 spec_tree_digest: str, module_ids: dict[str, str]) -> None:
        self.harness_root = harness_root
        self.files = files
        self.bundle_fd = bundle_fd
        self.bundle_digest = bundle_digest
        self.spec_tree_digest = spec_tree_digest
        self.module_ids = module_ids
        self._guard_installed = False

    # -- freeze -----------------------------------------------------------

    @classmethod
    def freeze(cls, *, harness_root: str, spec: dict) -> "PrivilegedBootstrap":
        harness_root = str(harness_root)
        files: dict[str, bytes] = {}
        for rel in PRIVILEGED_BOOTSTRAP_RELPATHS:
            full = os.path.join(harness_root, rel)
            if not os.path.isfile(full):
                raise RootInitError(
                    f"BOOTSTRAP_FILE_MISSING: {rel}")
            with open(full, "rb") as fh:
                files[rel] = fh.read()
        # compare the byte set to the TRUSTED SPEC IDENTITY before
        # anything is loaded or exposed
        digest = trusted_spec.harness_digest_from_files(harness_root, files)
        spec_digest = spec["harness"]["tree_digest"]
        if digest != spec_digest:
            raise RootInitError(
                f"BOOTSTRAP_HARNESS_TREE_DRIFT: frozen set digest "
                f"{digest[:12]}… != spec-bound {spec_digest[:12]}… "
                "(host harness tree drifted from the trusted spec)")
        # import the complete privileged module set NOW (before any
        # controller-accessible trigger exists)
        module_ids: dict[str, str] = {}
        real_root = os.path.realpath(harness_root)
        for name, rel in zip(PRIVILEGED_MODULES,
                             (r for r in PRIVILEGED_BOOTSTRAP_RELPATHS
                              if r.startswith("qh/") and r.endswith(".py"))):
            mod = importlib.import_module(name)
            mod_file = os.path.realpath(getattr(mod, "__file__", ""))
            if not mod_file.startswith(real_root + os.sep):
                raise RootInitError(
                    f"BOOTSTRAP_MODULE_NOT_FROM_PINNED_TREE: {name} -> "
                    f"{mod_file}")
            module_ids[name] = sha256_bytes(files[rel])
        # freeze the bytes into the MANDATORILY SEALED authority bundle
        blob = _bundle_pack(files)
        bundle_fd, seal_status = hold_authority_bytes(
            blob, name="qh-privileged-bootstrap-bundle")
        assert seal_status == "sealed"
        return cls(harness_root=harness_root, files=files,
                   bundle_fd=bundle_fd,
                   bundle_digest=sha256_bytes(blob),
                   spec_tree_digest=spec_digest,
                   module_ids=module_ids)

    # -- guards -----------------------------------------------------------

    def install_import_guard(self) -> None:
        if not self._guard_installed:
            sys.meta_path.insert(0, _FrozenImportGuard())
            self._guard_installed = True

    def verify_loaded_modules(self) -> None:
        """Every privileged module currently loaded in THIS process must
        still be the frozen one (identity by recorded digest entry)."""
        for name in PRIVILEGED_MODULES:
            if name not in sys.modules:
                raise RootInitError(
                    f"BOOTSTRAP_MODULE_UNLOADED: {name}")
        for name, _sha in self.module_ids.items():
            mod = sys.modules.get(name)
            if mod is None:
                raise RootInitError(f"BOOTSTRAP_MODULE_UNLOADED: {name}")
            mod_file = os.path.realpath(getattr(mod, "__file__", ""))
            if not mod_file.startswith(
                    os.path.realpath(self.harness_root) + os.sep):
                raise RootInitError(
                    f"BOOTSTRAP_MODULE_REROOTED: {name} -> {mod_file}")

    def verify_bundle_sealed(self) -> None:
        from .util import has_required_seals
        if not has_required_seals(self.bundle_fd):
            raise RootInitError("BOOTSTRAP_BUNDLE_NOT_SEALED")

    def digest_from_files(self) -> str:
        return trusted_spec.harness_digest_from_files(self.harness_root,
                                                      self.files)

    def close(self) -> None:
        try:
            os.close(self.bundle_fd)
        except OSError:
            pass


# ------------------------------------------------------------ authority root --

def _peer_cred(conn: socket.socket) -> tuple[int, int, int]:
    data = conn.getsockopt(socket.SOL_SOCKET, SO_PEERCRED,
                           struct.calcsize("iHH"))
    pid, uid, gid = struct.unpack("iHH", data)
    return pid, uid, gid


class _ForkedSupervisor:
    """Waitable handle for the forked supervisor child (production:
    created by ``fork()`` from the frozen root process)."""

    def __init__(self, pid: int) -> None:
        self.pid = pid
        self._waited = False

    def poll(self) -> int | None:
        if self._waited:
            return self.returncode
        try:
            got, status = os.waitpid(self.pid, os.WNOHANG)
        except ChildProcessError:
            return None
        if got == 0:
            return None
        self._waited = True
        self.returncode = os.waitstatus_to_exitcode(status)
        return self.returncode

    def wait(self, timeout: float | None = None) -> int | None:
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            rc = self.poll()
            if rc is not None:
                return rc
            if deadline is not None and time.monotonic() >= deadline:
                return None
            time.sleep(0.05)


class AuthorityRoot:
    """The operator-established authority root.  One root = one trusted
    launch spec = one attempt = at most one mint = one supervisor."""

    def __init__(self, *, operator_state_dir: str, spec_bytes: bytes,
                 custody_fd: int, redactor: Redactor | None = None,
                 supervisor_factory=None) -> None:
        self.operator_state_dir = operator_state_dir
        self.redactor = redactor or Redactor()
        # test seam for the supervisor spawn (production: fork of THIS
        # already-loaded process from the frozen bootstrap)
        self._supervisor_factory = supervisor_factory or _fork_supervisor
        self.ledger = ObservabilityLedger(operator_state_dir)
        self.spec: dict | None = None
        self.spec_identity: str | None = None
        self.spec_memfd: int | None = None
        self.custody_memfd: int | None = None
        self.custody_length: int = 0
        self.seal_status: str | None = None
        self.bootstrap: PrivilegedBootstrap | None = None
        self._raw_spec_bytes = spec_bytes
        self._custody_source_fd = custody_fd
        self._socket: socket.socket | None = None
        self._active_conn: socket.socket | None = None
        self.supervisor_proc = None
        self.exit_code = 0
        self.fail_reason: str | None = None

    # -- lifecycle ------------------------------------------------------

    def startup(self) -> None:
        self._record("ROOT_UP", pid=os.getpid(), ppid=os.getppid())
        pr_set_dumpable(0)
        self._record("PR_SET_DUMPABLE_0")
        yama = read_yama_ptrace_scope()
        if yama is None or yama < 1:
            # MANDATORY environmental gate — no override exists on any
            # production path.
            self._fail_closed("YAMA_PTRACE_SCOPE_LT_1", 6)
            return
        self._record("YAMA_GATE_PASS", yama=yama)
        # MANDATORY authority-critical sealing (CR-REMED-001): the
        # corrected four-seal representation must be establishable or the
        # root refuses to come up at all — never a silent downgrade.
        if memfd_seal_capability() != "sealed":
            self._fail_closed(
                "AUTHORITY_CRITICAL_SEALING_UNAVAILABLE: the required "
                "F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE "
                "representation cannot be established on this host "
                "(corrected UAPI probe); refusing to hold authority-"
                "critical state unsealed", 13)
            return
        # trusted launch spec arrives ONLY through the operator-held
        # capability channel gated by the CLI (pipe or fully sealed
        # memfd — never a controller field, never an ordinary file)
        try:
            self.spec = trusted_spec.parse_spec_bytes(self._raw_spec_bytes)
            trusted_spec.validate_spec(self.spec)
            self.spec_identity = trusted_spec.spec_id(self.spec)
        except trusted_spec.SpecError as exc:
            self._fail_closed(f"SPEC_INVALID:{exc}", 11)
            return
        try:
            self.spec_memfd, _status = hold_authority_bytes(
                trusted_spec.canonical_spec_bytes(self.spec),
                name="qh-root-trusted-spec")
        except RootInitError as exc:
            self._fail_closed(str(exc), 13)
            return
        self._write_spec_observability_copy()
        self._record("SPEC_BOUND", spec_id=self.spec_identity,
                     attempt_id=self.spec["attempt_id"])
        self._record("SPEC_BYTES_SEALED", seal_status="sealed",
                     spec_id=self.spec_identity)
        # provider credential bytes: pipe/memfd ONLY (ordinary file refused)
        kind = fd_source_kind(self._custody_source_fd)
        if kind not in ("pipe", "memfd"):
            self._fail_closed(
                f"CUSTODY_SOURCE_KIND_REFUSED:{kind}", 12)
            return
        data = b""
        while len(data) <= MAX_CUSTODY_BYTES:
            try:
                chunk = os.read(self._custody_source_fd, 4096)
            except OSError:
                break
            if not chunk:
                break
            data += chunk
        if not 1 <= len(data) <= MAX_CUSTODY_BYTES:
            self._fail_closed(f"CUSTODY_LENGTH_INVALID:{len(data)}", 12)
            return
        try:
            fd, status = hold_authority_bytes(
                data, name=f"qh-root-{ROOT_CUSTODY_LABEL}")
        except RootInitError as exc:
            self._fail_closed(str(exc), 13)
            return
        self.custody_memfd = fd
        self.custody_length = len(data)
        self.seal_status = status
        self.redactor.register(data.decode("utf-8", "surrogateescape"),
                               ROOT_CUSTODY_LABEL)
        try:
            os.close(self._custody_source_fd)
        except OSError:
            pass
        self._record("ROOT_CUSTODY_ESTABLISHED", label=ROOT_CUSTODY_LABEL,
                     length=len(data), seal_status=status)
        # CR-REMED-002: freeze the COMPLETE privileged bootstrap BEFORE
        # any controller-accessible trigger exists, then lock the process
        # against new harness-local imports.
        try:
            self.bootstrap = PrivilegedBootstrap.freeze(
                harness_root=self.spec["harness"]["root"], spec=self.spec)
        except (RootInitError, trusted_spec.SpecError,
                SealUnavailableError) as exc:
            self._fail_closed(f"BOOTSTRAP_FREEZE_FAILED:{exc}", 17)
            return
        self.bootstrap.install_import_guard()
        self._record(
            "BOOTSTRAP_FROZEN",
            bundle_digest=self.bootstrap.bundle_digest,
            files=len(self.bootstrap.files),
            modules=len(self.bootstrap.module_ids),
            spec_tree_digest_match=(
                self.bootstrap.digest_from_files()
                == self.spec["harness"]["tree_digest"]),
            bundle_seal_status="sealed")

    def _write_spec_observability_copy(self) -> None:
        """Persisted copy is OBSERVABILITY ONLY: the id is self-certifying
        (tampering detectable by recomputing the canonical content
        address); no authority lives in this file."""
        import pathlib
        sdir = os.path.join(self.operator_state_dir, "specs")
        pathlib.Path(sdir).mkdir(parents=True, exist_ok=True)
        path = os.path.join(sdir, f"{self.spec_identity}.json")
        with open(path, "wb") as fh:
            fh.write(trusted_spec.canonical_spec_bytes(self.spec))
        self._record("SPEC_OBSERVABILITY_COPY", path=path)

    def socket_name(self) -> str:
        return "\0qh-root-" + self.spec_identity[:16]

    def bind_socket(self) -> str:
        # the controller-accessible trigger may exist ONLY after the
        # privileged bootstrap is frozen (CR-REMED-002)
        if self.bootstrap is None:
            raise RootInitError(
                "ROOT_TRIGGER_BEFORE_BOOTSTRAP_FREEZE: refusing to expose"
                " the controller trigger before the privileged bootstrap"
                " is frozen")
        name = self.socket_name()
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(name)  # abstract namespace: no filesystem object to tamper
        s.listen(1)
        self._socket = s
        self._record("ROOT_SOCKET_BOUND", name=name[1:])
        return name

    # -- the single mint -------------------------------------------------

    def serve_mint_once(self, *, timeout: float = 300.0) -> dict:
        """Accept EXACTLY ONE mint request.  The request carries NO
        authority values; the peer must be the OPERATOR-AUTHORIZED
        controller instance bound in the trusted spec (exact uid/pid +
        actual starttime), and the only accepted attempt id is the one
        bound in the root's spec."""
        assert self._socket is not None
        self._socket.settimeout(timeout)
        try:
            conn, _ = self._socket.accept()
        except (OSError, socket.timeout) as exc:
            self._fail_closed(f"ROOT_ACCEPT_FAILED:{exc!r}", 7)
            return {"ok": False, "reason": "root_accept_failed"}
        self._active_conn = conn
        try:
            with conn:
                conn.settimeout(timeout)
                peer_pid, peer_uid, _gid = _peer_cred(conn)
                try:
                    line = conn.makefile("r").readline()
                    request = json.loads(line)
                except Exception as exc:  # noqa: BLE001
                    self._fail_closed(
                        f"MINT_REQUEST_UNPARSEABLE:{exc!r}", 8)
                    return {"ok": False,
                            "reason": "mint_request_unparseable"}
                response = self.handle_mint_request(
                    request, peer_pid=peer_pid, peer_uid=peer_uid)
                try:
                    conn.sendall(
                        (json.dumps(response, sort_keys=True) + "\n")
                        .encode("utf-8"))
                except OSError:
                    pass
            return response
        finally:
            self._active_conn = None

    def _verify_authorized_controller(self, *, peer_pid: int,
                                      peer_uid: int) -> str | None:
        """CR-REMED-004: exact match of the operator-authorized controller
        identity (spec-bound uid/pid + the peer's ACTUAL /proc starttime)
        — reject before mint on ANY mismatch.  PID alone is never
        sufficient; knowledge of attempt id/socket/manifest is not the
        capability."""
        ac = self.spec["authorized_controller"]
        actual_start = proc_starttime(peer_pid)
        if peer_uid != ac["uid"]:
            return (f"AUTHORIZED_CONTROLLER_MISMATCH:uid"
                    f" peer={peer_uid} bound={ac['uid']}")
        if peer_pid != ac["pid"]:
            return (f"AUTHORIZED_CONTROLLER_MISMATCH:pid"
                    f" peer={peer_pid} bound={ac['pid']}")
        if actual_start is None or actual_start != str(ac["starttime"]):
            return (f"AUTHORIZED_CONTROLLER_MISMATCH:starttime"
                    f" actual={actual_start} bound={ac['starttime']}")
        return None

    def handle_mint_request(self, request: dict, *, peer_pid: int,
                            peer_uid: int | None = None) -> dict:
        self._record("MINT_REQUEST_RECEIVED", peer_pid=peer_pid,
                     claimed_attempt_id=request.get("attempt_id"))
        # [CR-REMED-004] the peer must BE the operator-authorized
        # controller instance BEFORE any mint is considered
        if peer_uid is None:
            self._fail_closed("AUTHORIZED_CONTROLLER_PEER_UID_UNREADABLE",
                              9)
            return {"ok": False, "reason":
                    "AUTHORIZED_CONTROLLER_MISMATCH:uid_unreadable"}
        mismatch = self._verify_authorized_controller(
            peer_pid=peer_pid, peer_uid=peer_uid)
        if mismatch is not None:
            # wrong same-UID peer: terminally consume the one-shot root —
            # acceptable fail-closed DoS, recorded; NO auto-recovery.
            self._fail_closed(mismatch, 9)
            return {"ok": False, "reason": mismatch}
        self._record("AUTHORIZED_CONTROLLER_VERIFIED", pid=peer_pid,
                     uid=peer_uid)
        attempt_id = self.spec["attempt_id"]
        if request.get("attempt_id") != attempt_id:
            self._fail_closed("MINT_WRONG_ATTEMPT", 9)
            return {"ok": False, "reason": "MINT_WRONG_ATTEMPT"}
        try:
            grant = mint_attempt_grant(
                attempt_id=attempt_id,
                root=self.spec["attempt_root"]["path"],
                manifest_id=self.spec["bootstrap_manifest"]["manifest_id"],
                operator_state_dir=self.operator_state_dir,
                out_stream=_NullStream(), operator_inmemory=True,
                redactor=self.redactor)
        except Exception as exc:  # noqa: BLE001 — fail closed
            self._fail_closed(f"MINT_REFUSED:{exc}", 9)
            return {"ok": False, "reason": f"MINT_REFUSED:{exc}"}
        # bind the canonical trusted-spec id into the grant: the spawned
        # supervisor refuses any spec whose canonical id differs
        grant.spec_id = self.spec_identity
        self._record("ROOT_MINTED", grant_id=grant.grant_id,
                     attempt_id=attempt_id, spec_id=grant.spec_id)
        try:
            spawn = self._spawn_supervisor(grant)
        except Exception as exc:  # noqa: BLE001 — report, fail closed
            self._fail_closed(f"SUPERVISOR_SPAWN_FAILED:{exc!r}", 14)
            return {"ok": False,
                    "reason": f"SUPERVISOR_SPAWN_FAILED:{exc!r}"}
        if not spawn.get("ok"):
            self._fail_closed(spawn.get("reason", "SPAWN_FAILED"), 14)
            return spawn
        response = {"ok": True, "attempt_id": attempt_id,
                    "supervisor_socket": spawn["socket_name"],
                    "supervisor_pid": spawn["pid"],
                    "grant_id": grant.grant_id}
        return response

    def _spawn_supervisor(self, grant: Grant) -> dict:
        """The root itself constructs the one-shot supervisor from the
        FROZEN trusted process state: ``fork()`` with NO exec and NO host
        re-import — grant/spec/custody/bundle cross by process
        inheritance only."""
        assert self.spec is not None and self.custody_memfd is not None
        assert self.bootstrap is not None, "bootstrap must be frozen"
        proc, socket_name = self._supervisor_factory(
            self, grant)
        self.supervisor_proc = proc
        self._record("ROOT_SPAWNED_SUPERVISOR", pid=proc.pid,
                     socket=socket_name[1:],
                     channel="fork-frozen-bootstrap")
        return {"ok": True, "pid": proc.pid, "socket_name": socket_name}

    def wait_for_supervisor(self, timeout: float = 600.0) -> int | None:
        if self.supervisor_proc is None:
            return None
        return self.supervisor_proc.wait(timeout=timeout)

    # -- plumbing ---------------------------------------------------------

    def _fail_closed(self, reason: str, exit_code: int) -> None:
        self._record("ROOT_FAIL_CLOSED", reason=reason)
        self.fail_reason = reason
        self.exit_code = exit_code

    def _record(self, event: str, **facts) -> None:
        scrubbed = {k: (self.redactor.scrub(str(v)) if isinstance(v, str)
                        else v) for k, v in facts.items()}
        try:
            self.ledger.append(event, **scrubbed)
        except OSError:
            pass  # observability only — never an authority decision

    def shutdown(self) -> None:
        if self.spec_memfd is not None:
            try:
                os.close(self.spec_memfd)
            except OSError:
                pass
            self.spec_memfd = None
        if self.custody_memfd is not None:
            try:
                os.close(self.custody_memfd)
            except OSError:
                pass
            self.custody_memfd = None
        if self.bootstrap is not None:
            self.bootstrap.close()
            self.bootstrap = None
        if self._socket is not None:
            try:
                self._socket.close()
            except OSError:
                pass
            self._socket = None
        rc = (self.supervisor_proc.poll()
              if self.supervisor_proc is not None else None)
        self._record("ROOT_EXIT", code=self.exit_code,
                     supervisor_rc=rc)


class _NullStream:
    """The root mints in-process; the grant never exists in any ordinary
    file (the in-memory operator channel is ledger-recorded)."""
    def write(self, _s) -> None:
        pass

    def flush(self) -> None:
        pass

    def fileno(self) -> int:
        raise OSError("null stream has no fd")


def _fork_supervisor(root: "AuthorityRoot", grant: Grant):
    """PRODUCTION supervisor creation: fork the already-loaded root
    process.  The child NEVER re-imports privileged code from the host
    tree — it runs the frozen modules loaded before the trigger was
    exposed, verifies the inherited frozen bootstrap, and serves exactly
    one controller request."""
    from .authority import Supervisor  # preloaded pre-freeze; guard-safe

    ready_r, ready_w = os.pipe()
    pid = os.fork()
    if pid == 0:
        # ---- child: the one-shot supervisor (no exec, no host import) --
        rc = 1
        try:
            os.close(ready_r)
            # close root-owned fds the supervisor must not hold
            if root._socket is not None:
                try:
                    root._socket.close()
                except OSError:
                    pass
            if root._active_conn is not None:
                try:
                    root._active_conn.close()
                except OSError:
                    pass
            # the inherited frozen bootstrap must still be the sealed,
            # spec-matching representation
            root.bootstrap.verify_bundle_sealed()
            root.bootstrap.verify_loaded_modules()
            sup = Supervisor(
                grant=grant, spec=root.spec,
                spec_id=root.spec_identity,
                operator_state_dir=root.operator_state_dir,
                custody_fd=root.custody_memfd,
                bootstrap=root.bootstrap)
            sup.startup()
            if sup.exit_code != 0:
                os.write(ready_w, (f"FAILED code={sup.exit_code}\n")
                         .encode("utf-8"))
                rc = sup.exit_code
            else:
                name = sup.bind_socket()
                os.write(ready_w, (f"READY {name[1:]}\n").encode("utf-8"))
                sup.serve_once()
                rc = sup.exit_code
        except BaseException as exc:  # noqa: BLE001 — report, fail closed
            try:
                os.write(ready_w,
                         (f"FAILED {type(exc).__name__}:{exc}\n")
                         .encode("utf-8"))
            except OSError:
                pass
            rc = 14
        finally:
            try:
                os.close(ready_w)
            except OSError:
                pass
            os._exit(rc)
    # ---- parent: wait for the supervisor READY line -------------------
    os.close(ready_w)
    line = b""
    deadline = time.monotonic() + 60.0
    try:
        while b"\n" not in line and time.monotonic() < deadline:
            r, _w, _x = select.select([ready_r], [], [], 1.0)
            if not r:
                continue
            chunk = os.read(ready_r, 4096)
            if not chunk:
                break
            line += chunk
    finally:
        os.close(ready_r)
    text = line.decode("utf-8", "replace").strip()
    if not text.startswith("READY"):
        # reap the failed child so no zombie remains
        _ForkedSupervisor(pid).wait(timeout=10)
        raise RootInitError(f"SUPERVISOR_STARTUP_FAILED: {text!r}")
    # the READY line carries the abstract-socket name without the NUL
    return _ForkedSupervisor(pid), "\0" + text.split(None, 1)[1]
