"""IR-001 remediation — the mechanically-rooted OPERATOR AUTHORITY ROOT.

The production launch authority now has an actual mechanical root of trust
OUTSIDE the untrusted same-UID controller:

* the operator establishes ``qh root`` BEFORE controller-controlled request
  execution, delivering the two out-of-band inputs a controller cannot
  manufacture — the COMPLETE pre-authorized trusted launch spec (operator
  pipe) and the provider credential bytes (operator pipe/memfd custody
  channel);
* the root immediately becomes non-dumpable (PR_SET_DUMPABLE=0: same-UID
  processes cannot read its memory or fds) and requires Yama ptrace_scope
  >= 1 (real kernel read; no override exists anywhere on the production
  path);
* the canonical spec id and the credential bytes are bound ONLY in root
  process memory; persisted spec copies are observability (tamper-evident
  via the self-certifying content address) and no ordinary file is ever the
  root capability;
* the public unrestricted ``qh mint`` surface is REMOVED from production:
  the only production mint is performed by THIS root, for EXACTLY the one
  attempt id bound in its spec, at most ONCE (in-memory minted-set +
  observability ledger);
* the root itself constructs and spawns the one-shot supervisor, passing
  grant, spec and custody ONLY through inherited pipes/fds — the
  supervisor's parent is mechanically the root (ppid binding from the
  minting process, not a caller-supplied flag);
* a controller-created parallel root can at most mint a powerless
  imitation: it holds no real credential bytes and no operator-authorized
  spec, so nothing it spawns can perform a provider-capable launch;
* root SIGKILL is fail-closed denial (DoS) only — authority dies with the
  process and nothing on the filesystem can restore it.

Sealed-state policy (remediation §6): authority-critical bytes are held in
anonymous process-bound memfds; the four-seal representation is REQUIRED in
strict mode (``--require-seals``) and root initialization FAILS CLOSED when
the host cannot produce it.  On the demonstrated host class the four-seal
representation is mechanically unavailable (an MFD_ALLOW_SEALING memfd
cannot be populated — write/ftruncate EINVAL; F_ADD_SEALS on a plain memfd
is EINVAL), reconciling with the previously demonstrated G-1 mechanism:
the default posture keeps authority state as non-dumpable process-bound
memory with the seal outcome RECORDED, never silently downgraded.
"""
from __future__ import annotations

import ctypes
import json
import os
import secrets as _secrets
import socket
import stat as _stat
import struct
import subprocess
import sys

from . import trusted_spec
from .authority import Grant, mint_attempt_grant
from .custody import _fd_kind
from .ledger import ObservabilityLedger
from .util import (Redactor, SealUnavailableError, hold_bytes_memfd,
                   memfd_seal_capability as _memfd_seal_capability,
                   read_yama_ptrace_scope)

SO_PEERCRED = 17
MAX_CUSTODY_BYTES = 65536
ROOT_CUSTODY_LABEL = "root-provider-custody"


class RootInitError(RuntimeError):
    """Fail-closed authority-root initialization failure."""


PR_SET_DUMPABLE = 4


def pr_set_dumpable(value: int) -> None:
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(PR_SET_DUMPABLE, value, 0, 0, 0) != 0:
        raise RootInitError("PR_SET_DUMPABLE_FAILED")


def memfd_seal_capability() -> str:
    return _memfd_seal_capability()


def hold_authority_bytes(data: bytes, *, name: str,
                         require_seals: bool = False) -> tuple[int, str]:
    """Hold authority-critical bytes in an anonymous process-bound memfd
    (see qh/util.py; strict mode fails closed through RootInitError)."""
    try:
        return hold_bytes_memfd(data, name=name, require_seals=require_seals)
    except SealUnavailableError as exc:
        raise RootInitError(str(exc)) from exc


# ------------------------------------------------------------ authority root --

def _peer_cred(conn: socket.socket) -> tuple[int, int, int]:
    data = conn.getsockopt(socket.SOL_SOCKET, SO_PEERCRED,
                           struct.calcsize("iHH"))
    pid, uid, gid = struct.unpack("iHH", data)
    return pid, uid, gid


class AuthorityRoot:
    """The operator-established authority root.  One root = one trusted
    launch spec = one attempt = at most one mint = one supervisor."""

    def __init__(self, *, operator_state_dir: str, spec_bytes: bytes,
                 custody_fd: int, require_seals: bool = False,
                 redactor: Redactor | None = None,
                 supervisor_factory=None) -> None:
        self.operator_state_dir = operator_state_dir
        self.require_seals = require_seals
        self.redactor = redactor or Redactor()
        # test seam for the supervisor subprocess (production: qh.cli)
        self._supervisor_factory = supervisor_factory or _spawn_supervisor_cli
        self.ledger = ObservabilityLedger(operator_state_dir)
        self.spec: dict | None = None
        self.spec_identity: str | None = None
        self.custody_memfd: int | None = None
        self.custody_length: int = 0
        self.seal_status: str | None = None
        self._raw_spec_bytes = spec_bytes
        self._custody_source_fd = custody_fd
        self._socket: socket.socket | None = None
        self.supervisor_proc: subprocess.Popen | None = None
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
        # strict authority-state policy: fail closed UP FRONT when the
        # four-seal representation is unavailable on this host
        if self.require_seals and memfd_seal_capability() != "sealed":
            self._fail_closed(
                "SEALED_REPRESENTATION_UNAVAILABLE_ON_THIS_HOST: strict "
                "authority-state policy requires F_SEAL_WRITE|F_SEAL_GROW|"
                "F_SEAL_SHRINK|F_SEAL_SEAL and this host cannot produce a "
                "populated sealed memfd (refusing to downgrade)", 13)
            return
        # trusted launch spec arrives ONLY through the operator pipe bytes
        # handed to this process (never a controller field)
        try:
            self.spec = trusted_spec.parse_spec_bytes(self._raw_spec_bytes)
            trusted_spec.validate_spec(self.spec)
            self.spec_identity = trusted_spec.spec_id(self.spec)
        except trusted_spec.SpecError as exc:
            self._fail_closed(f"SPEC_INVALID:{exc}", 11)
            return
        self._write_spec_observability_copy()
        self._record("SPEC_BOUND", spec_id=self.spec_identity,
                     attempt_id=self.spec["attempt_id"])
        # provider credential bytes: pipe/memfd ONLY (ordinary file refused)
        kind = _fd_kind(self._custody_source_fd)
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
                data, name=f"qh-root-{ROOT_CUSTODY_LABEL}",
                require_seals=self.require_seals)
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
        name = self.socket_name()
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(name)  # abstract namespace: no filesystem object to tamper
        s.listen(1)
        self._socket = s
        self._record("ROOT_SOCKET_BOUND", name=name[1:])
        return name

    # -- the single mint -------------------------------------------------

    def serve_mint_once(self, *, timeout: float = 300.0) -> dict:
        """Accept EXACTLY ONE mint request.  The request may come from the
        operator or the controller — it carries NO authority values; the
        only accepted attempt id is the one bound in the root's spec, and
        the mint itself is performed by THIS root process."""
        assert self._socket is not None
        self._socket.settimeout(timeout)
        try:
            conn, _ = self._socket.accept()
        except (OSError, socket.timeout) as exc:
            self._fail_closed(f"ROOT_ACCEPT_FAILED:{exc!r}", 7)
            return {"ok": False, "reason": "root_accept_failed"}
        with conn:
            conn.settimeout(timeout)
            peer_pid, _uid, _gid = _peer_cred(conn)
            try:
                line = conn.makefile("r").readline()
                request = json.loads(line)
            except Exception as exc:  # noqa: BLE001
                self._fail_closed(f"MINT_REQUEST_UNPARSEABLE:{exc!r}", 8)
                return {"ok": False, "reason": "mint_request_unparseable"}
            response = self.handle_mint_request(request,
                                                peer_pid=peer_pid)
            try:
                conn.sendall((json.dumps(response, sort_keys=True) + "\n")
                             .encode("utf-8"))
            except OSError:
                pass
        return response

    def handle_mint_request(self, request: dict, *, peer_pid: int) -> dict:
        self._record("MINT_REQUEST_RECEIVED", peer_pid=peer_pid,
                     claimed_attempt_id=request.get("attempt_id"))
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
        """The root itself constructs and spawns the one-shot supervisor;
        grant + spec travel on a pipe, custody on the inherited memfd."""
        assert self.spec is not None and self.custody_memfd is not None
        grant_line = json.dumps(grant.full_doc()) + "\n"
        spec_line = (trusted_spec.canonical_spec_bytes(self.spec)
                     .decode("utf-8")) + "\n"
        r, w = os.pipe()
        os.write(w, (grant_line + spec_line).encode("utf-8"))
        os.close(w)
        try:
            proc, socket_name = self._supervisor_factory(
                self.operator_state_dir, stdin_fd=r,
                custody_fd=self.custody_memfd,
                harness_root=self.spec["harness"]["root"])
        finally:
            os.close(r)
        self.supervisor_proc = proc
        self._record("ROOT_SPAWNED_SUPERVISOR", pid=proc.pid,
                     socket=socket_name[1:])
        return {"ok": True, "pid": proc.pid, "socket_name": socket_name}

    def wait_for_supervisor(self, timeout: float = 600.0) -> int | None:
        if self.supervisor_proc is None:
            return None
        try:
            return self.supervisor_proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            return None

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
        if self.custody_memfd is not None:
            try:
                os.close(self.custody_memfd)
            except OSError:
                pass
            self.custody_memfd = None
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


def _spawn_supervisor_cli(operator_state_dir: str, *, stdin_fd: int,
                          custody_fd: int, harness_root: str):
    argv = [sys.executable, "-m", "qh.cli", "supervisor",
            "--operator-state", operator_state_dir,
            "--custody-fd", str(custody_fd)]
    env = dict(os.environ, PYTHONPATH=harness_root + os.pathsep +
               os.environ.get("PYTHONPATH", ""))
    proc = subprocess.Popen(
        argv, pass_fds=(stdin_fd, custody_fd), stdin=stdin_fd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    line = proc.stdout.readline().decode("utf-8", "replace").strip()
    if not line.startswith("READY"):
        try:
            err = proc.stderr.read(4096).decode("utf-8", "replace")
            proc.wait(timeout=10)
        except Exception:  # noqa: BLE001
            proc.kill()
            proc.wait(timeout=10)
            err = "<unreadable>"
        raise RootInitError(
            f"SUPERVISOR_STARTUP_FAILED: {line!r} stderr={err!r}")
    # the CLI prints the abstract-socket name without its leading NUL
    return proc, "\0" + line.split(None, 1)[1]
