"""C-2 / G-1 — process-bound single-use launch authority (supervising
gatekeeper).

Accepted design (G-1 DESIGN_PROBE_CLOSURE_ACCEPTED):

* authority is minted only through an operator/Control-Room-side path
  OUTSIDE the controller's writable authority surface: the mint writes
  the grant ONLY to a PIPE (a persisted ordinary-file grant is refused),
  and the supervisor accepts the grant ONLY on a pipe — the grant blob
  never exists in any controller-readable ordinary file;
* kernel/process-bound authority: the supervisor immediately sets
  PR_SET_DUMPABLE=0 (same-UID processes cannot ptrace/inspect it or read
  its memory/fds) and requires Yama ptrace_scope >= 1 (no same-UID
  non-parent ptrace); the authority lives ONLY in supervisor process
  memory — ordinary files (the observability ledger) grant nothing;
* exact attempt/root binding (attempt id + root dev/inode + manifest
  id from the C-1 bootstrap);
* one-shot consumption; replay/second-use refusal; copied-grant refusal
  (file-carried grant rejected); wrong-root/wrong-attempt refusal;
* terminal PREEXEC_STOP: any failed mandatory preexec gate transitions
  the attempt to TERMINAL_PREEXEC_STOP and the supervisor exits — the
  same attempt/root can never launch again, and filesystem
  deletion/recreation (of the ledger, socket or any state file) cannot
  restore launch authority because authority was never in a file;
* supervisor SIGKILL is fail-closed denial (DoS) only — authority dies
  with the process and is never recoverable;
* a genuinely new attempt requires a NEW out-of-band mint (the mint
  refuses duplicate attempt ids); pre-inference PREEXEC stop does NOT
  consume campaign auditor/model authority (qh/campaign.py is never
  touched by this lifecycle).
"""
from __future__ import annotations

import ctypes
import json
import os
import secrets as _secrets
import socket
import stat
import struct
from dataclasses import dataclass, field

from . import boundary as boundary_mod
from .boundary import BoundarySpec, launch as boundary_launch
from .campaign import EngagementLedger
from .codex_profile import (CodexIdentity, IdentityDrift, PolicyDrift,
                            freeze_profile, validate_profile_semantics,
                            verify_codex_identity, verify_frozen_profile)
from .bootstrap import ControllerBinding, load_manifest, verify_c4p
from .custody import CredentialCustody, CustodyError
from .ledger import ObservabilityLedger
from .statemachine import (AttemptState, AttemptStateMachine,
                           InvalidTransition)
from .util import (Redactor, content_id, proc_starttime as _proc_starttime,
                   read_yama_ptrace_scope, utc_now_iso)

PR_SET_DUMPABLE = 4
SO_PEERCRED = 17


class AuthorityError(RuntimeError):
    """Fail-closed authority refusal."""


def pr_set_dumpable(value: int) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(PR_SET_DUMPABLE, value, 0, 0, 0) != 0:
        raise AuthorityError("PR_SET_DUMPABLE_FAILED")


# ------------------------------------------------------------------ mint --

@dataclass
class Grant:
    grant_id: str
    attempt_id: str
    root: str
    root_dev: int
    root_ino: int
    manifest_id: str
    secret: str
    created_at: str

    def public_doc(self) -> dict:
        """Ledger-safe projection: NO secret."""
        return {"grant_id": self.grant_id, "attempt_id": self.attempt_id,
                "root": self.root, "root_dev": self.root_dev,
                "root_ino": self.root_ino, "manifest_id": self.manifest_id,
                "created_at": self.created_at}

    def full_doc(self) -> dict:
        return {**self.public_doc(), "secret": self.secret}


def mint_attempt_grant(*, attempt_id: str, root: str, manifest_id: str,
                       operator_state_dir: str,
                       out_stream=None,
                       redactor: Redactor | None = None,
                       operator_inmemory: bool = False) -> Grant:
    """Operator/Control-Room-side mint.  The grant is written ONLY to a
    PIPE-style stream (default: stdout when stdout is a pipe/FIFO); a
    regular-file output is refused — persisted grants would sit in the
    controller-writable ordinary-file surface this design exists to
    avoid.  Duplicate attempt ids are refused (a genuinely new attempt
    requires a NEW out-of-band mint with a fresh attempt id).
    ``operator_inmemory=True`` is the explicit in-process OPERATOR path
    used by tests/composition (the CLI enforces the real pipe contract
    for operational mints; the choice is recorded in the ledger)."""
    ledger = ObservabilityLedger(operator_state_dir)
    if attempt_id in ledger.attempt_ids_minted():
        raise AuthorityError(
            f"ATTEMPT_ALREADY_MINTED: {attempt_id} — a new attempt "
            "requires a NEW out-of-band mint with a fresh attempt id")
    if not os.path.isdir(root):
        raise AuthorityError(f"ROOT_NOT_A_DIRECTORY: {root}")
    st = os.lstat(root)
    grant = Grant(
        grant_id=_secrets.token_hex(16),
        attempt_id=attempt_id,
        root=root,
        root_dev=st.st_dev,
        root_ino=st.st_ino,
        manifest_id=manifest_id,
        secret=_secrets.token_urlsafe(32),
        created_at=utc_now_iso())
    channel = "pipe"
    if out_stream is None:
        out_stream = sys_stdout_checked()
    elif not _stream_is_pipe_like(out_stream):
        if not operator_inmemory:
            raise AuthorityError(
                "MINT_OUTPUT_MUST_BE_PIPE: refusing to persist a grant "
                "to an ordinary file")
        channel = "inmemory-operator"
    if redactor is not None:
        redactor.register(grant.secret, "grant-secret")
    out_stream.write(json.dumps(grant.full_doc()) + "\n")
    out_stream.flush()
    ledger.append("MINTED", channel=channel, **grant.public_doc())
    return grant


def sys_stdout_checked():
    import sys
    if not _stream_is_pipe_like(sys.stdout):
        raise AuthorityError(
            "MINT_OUTPUT_MUST_BE_PIPE: stdout is not a pipe; pipe the "
            "mint output directly into the supervisor "
            "(mint ... | supervisor ...)")
    return sys.stdout


def _stream_is_pipe_like(stream) -> bool:
    try:
        st = os.fstat(stream.fileno())
    except (OSError, ValueError):
        return False
    return stat.S_ISFIFO(st.st_mode)


# ------------------------------------------------------------- supervisor --

@dataclass
class SupervisorPolicy:
    """Injectable environment facts.  Production reads the REAL values;
    the fault_* fields exist ONLY for deterministic adversarial tests and
    are recorded in the ledger when used."""
    yama_value: int | None = None          # None -> read the real knob
    env_reader=None                        # None -> /proc/<pid>/environ
    stat_reader=None                       # None -> /proc/<pid>/stat
    walker=None                            # None -> real scope walk
    set_dumpable: bool = True
    require_custody: bool = True
    fault_noegress_fail: bool = False
    fault_gatew_fail: bool = False
    fault_identity_drift: bool = False
    fault_policy_drift: bool = False
    operator_pid: int | None = None
    boundary_launcher=None                 # None -> real boundary launch


@dataclass
class RequestDoc:
    attempt_id: str
    root: str
    manifest_id: str
    controller_pid: int
    controller_starttime: str | None
    env_claims: dict[str, str]
    codex_home: str
    config_path: str
    identity_version: str
    identity_sha256: str
    identity_exe_path: str
    harness_root: str
    evidence_src: str
    auditor_output_src: str
    target_src: str | None = None
    payload_kind: str = "launch_sim"       # launch_sim | gatew-only


class Supervisor:
    """The one-shot supervising gatekeeper.  Run as a dedicated process
    started by the OPERATOR (never by the controller); the grant arrives
    on a pipe."""

    def __init__(self, *, grant: Grant, operator_state_dir: str,
                 custody_fd: int | None,
                 policy: SupervisorPolicy | None = None) -> None:
        self.grant = grant
        self.operator_state_dir = operator_state_dir
        self.custody_fd = custody_fd
        self.policy = policy or SupervisorPolicy()
        self.redactor = Redactor()
        self.redactor.register(grant.secret, "grant-secret")
        self.ledger = ObservabilityLedger(operator_state_dir)
        self.engagements = EngagementLedger(operator_state_dir)
        self.machine = AttemptStateMachine()
        self.custody: CredentialCustody | None = None
        self.frozen_profile: dict | None = None
        self._socket: socket.socket | None = None
        self.exit_code = 0

    # -- lifecycle ----------------------------------------------------

    def startup(self) -> None:
        self._record("SUPERVISOR_UP", grant=self.grant.grant_id,
                     pid=os.getpid(), ppid=os.getppid())
        if self.policy.operator_pid is not None and \
                os.getppid() != self.policy.operator_pid:
            self._fail_closed("OPERATOR_PID_MISMATCH", exit_code=5)
        if self.policy.set_dumpable:
            pr_set_dumpable(0)
            self._record("PR_SET_DUMPABLE_0")
        yama = self.policy.yama_value \
            if self.policy.yama_value is not None \
            else read_yama_ptrace_scope()
        if yama is None or yama < 1:
            # MANDATORY environmental gate: fail closed when absent.
            self.machine.force_terminal_preexec_stop("YAMA_PTRACE_SCOPE_LT_1")
            self._record("TERMINAL_PREEXEC_STOP",
                         reason="YAMA_PTRACE_SCOPE_LT_1", yama=yama)
            self.exit_code = 6
            return
        self._record("YAMA_GATE_PASS", yama=yama)

    def socket_name(self) -> str:
        return "\0qh-" + content_id({"attempt": self.grant.attempt_id})[:16]

    def bind_socket(self) -> str:
        name = self.socket_name()
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(name)  # abstract namespace: no filesystem object to tamper
        s.listen(1)
        self._socket = s
        self._record("SOCKET_BOUND", name=name[1:])
        return name

    def serve_once(self, *, timeout: float = 120.0) -> dict:
        """Accept exactly one controller connection, run the preexec
        pipeline, respond, and terminate."""
        assert self._socket is not None
        self._socket.settimeout(timeout)
        try:
            conn, _ = self._socket.accept()
        except (OSError, socket.timeout) as exc:
            self._fail_closed(f"ACCEPT_FAILED:{exc!r}", exit_code=7)
            return {"ok": False, "reason": "accept_failed"}
        with conn:
            conn.settimeout(timeout)
            peer_pid, _uid, _gid = _peer_cred(conn)
            try:
                line = conn.makefile("r").readline()
                request = json.loads(line)
            except Exception as exc:  # noqa: BLE001
                self._fail_closed(f"REQUEST_UNPARSEABLE:{exc!r}",
                                  exit_code=8)
                return {"ok": False, "reason": "request_unparseable"}
            response = self.handle_request(request, peer_pid=peer_pid)
            try:
                conn.sendall((json.dumps(response, sort_keys=True) + "\n")
                             .encode("utf-8"))
            except OSError:
                pass
        self.shutdown()
        return response

    # -- request pipeline (the recorded composition order) -------------

    def handle_request(self, request: dict, *, peer_pid: int) -> dict:
        self._record("REQUEST_RECEIVED", peer_pid=peer_pid,
                     payload_kind=request.get("payload_kind"))
        if self.machine.state != AttemptState.MINTED:
            return self._refuse("REPLAY_OR_TERMINAL_STATE",
                                state=self.machine.state)

        # exact attempt/root/manifest binding vs the minted grant
        if request.get("attempt_id") != self.grant.attempt_id:
            return self._refuse_terminal("WRONG_ATTEMPT")
        if os.path.realpath(request.get("root", "")) != \
                os.path.realpath(self.grant.root):
            return self._refuse_terminal("WRONG_ROOT")
        try:
            st = os.lstat(self.grant.root)
            if (st.st_dev, st.st_ino) != \
                    (self.grant.root_dev, self.grant.root_ino):
                # deleted/recreated root = different object = refusal
                return self._refuse_terminal("ROOT_IDENTITY_CHANGED")
        except OSError:
            return self._refuse_terminal("ROOT_IDENTITY_CHANGED")
        if request.get("manifest_id") != self.grant.manifest_id:
            return self._refuse_terminal("MANIFEST_ID_MISMATCH")

        # [composition 2] controller binding established
        starttime = (self.policy.stat_reader or _proc_starttime)(peer_pid)
        claimed_starttime = request.get("controller_starttime")
        if claimed_starttime is not None and \
                claimed_starttime != starttime:
            return self._refuse_terminal("CONTROLLER_STARTTIME_MISMATCH")
        binding = ControllerBinding(
            attempt_id=self.grant.attempt_id,
            root=self.grant.root,
            manifest_id=self.grant.manifest_id,
            pid=peer_pid,
            starttime=starttime or "",
            env_claims=request.get("env_claims") or {})
        self._record("CONTROLLER_BINDING_ESTABLISHED", pid=binding.pid,
                     starttime=binding.starttime,
                     env_keys=sorted(binding.env_claims))

        # [composition 3] C4' — actual process/scope verification
        manifest_doc = load_manifest(self.operator_state_dir,
                                     self.grant.manifest_id)
        if manifest_doc is None:
            return self._refuse_terminal("MANIFEST_NOT_FOUND")
        c4 = verify_c4p(manifest_doc, binding, peer_pid=peer_pid,
                        env_reader=self.policy.env_reader,
                        stat_reader=self.policy.stat_reader,
                        walker=self.policy.walker)
        self._record("C4P_RESULT", passed=c4.passed,
                     failures=c4.failures)
        if not c4.passed:
            return self._refuse_terminal(
                "C4P_FAIL:" + ",".join(c4.failures))

        # [composition 4] one-shot attempt authority bound
        try:
            self.machine.transition(AttemptState.BOUND,
                                    "controller-verified grant binding")
        except InvalidTransition as exc:
            return self._refuse_terminal(f"STATE:{exc}")
        self._record("AUTHORITY_BOUND", controller_pid=peer_pid)

        # [composition 5] credential custody (MANDATORY)
        try:
            self.machine.transition(AttemptState.PREEXEC_CHECKING,
                                    "preexec gates")
        except InvalidTransition as exc:
            return self._refuse_terminal(f"STATE:{exc}")
        if self.policy.require_custody:
            if self.custody_fd is None:
                return self._refuse_terminal("CUSTODY_FD_NOT_PROVIDED")
            try:
                self.custody = CredentialCustody.establish(
                    self.custody_fd, label=f"attempt-{self.grant.attempt_id}",
                    redactor=self.redactor)
            except CustodyError as exc:
                return self._refuse_terminal(f"CUSTODY_ESTABLISH_FAILED:"
                                             f"{exc}")
            self._record("CUSTODY_ESTABLISHED",
                         label=self.custody.label,
                         length=self.custody.length)

        # [composition 6] hard no-egress gate
        noegress = self._run_noegress(request)
        if not noegress["passed"]:
            return self._refuse_terminal(
                "NOEGRESS_FAIL:" + ",".join(noegress["failures"]))

        # [composition 7] exact Codex identity/profile frozen
        try:
            frozen = self._freeze_profile(request)
        except IdentityDrift as exc:
            return self._refuse_terminal(f"CODEX_IDENTITY_DRIFT:{exc}")
        except PolicyDrift as exc:
            return self._refuse_terminal(f"PROFILE_POLICY_DRIFT:{exc}")
        self._record("PROFILE_FROZEN", **frozen)

        # [composition 8] GATE-W zero-provider rehearsal
        gatew = self._run_gatew(request)
        if not gatew["passed"]:
            return self._refuse_terminal(
                "GATEW_FAIL:" + ",".join(gatew["failures"]))

        # [composition 9] consume exactly once + protected local launch
        try:
            self.machine.transition(AttemptState.CONSUMED_FOR_LAUNCH,
                                    "protected local launch simulation")
        except InvalidTransition as exc:
            return self._refuse_terminal(f"STATE:{exc}")
        self._record("CONSUMED_FOR_LAUNCH")
        launch = self._protected_launch(request)
        if not launch["ok"]:
            self.machine.transition(AttemptState.TERMINAL,
                                    "protected launch failed post-"
                                    "consumption")
            self._record("TERMINAL", reason="LAUNCH_FAILED")
            self.exit_code = 10
            return {"ok": False, "state": self.machine.state,
                    "phase": "protected_launch",
                    "failures": launch.get("failures", [])}
        self.machine.transition(AttemptState.LAUNCHED, "payload executed")
        self.machine.transition(AttemptState.TERMINAL, "run complete")
        self._record("LAUNCHED")
        self._record("TERMINAL", reason="complete")
        return {"ok": True, "state": self.machine.state,
                "phase": "complete",
                "launch": launch.get("payload"),
                "engagements": self.engagements.snapshot()}

    # -- gates ---------------------------------------------------------

    def _boundary_spec(self, request: dict, payload_argv,
                       noegress: bool) -> BoundarySpec:
        from .custody import SyntheticInertAdapter
        adapter = SyntheticInertAdapter()
        plans = []
        if self.custody is not None:
            plans.append(self.custody.child_plan(adapter.child_target_path()))
        ro_binds = [(request["evidence_src"], "/evidence"),
                    (request["codex_home"], "/codex-home")]
        if request.get("target_src"):
            ro_binds.append((request["target_src"], "/target"))
        spec = BoundarySpec(
            harness_root=request["harness_root"],
            payload_argv=payload_argv,
            ro_binds=ro_binds,
            rw_binds=[(request["auditor_output_src"], "/auditor-output")],
            tmpfs_paths=["/tmp", "/run-qh"],
            env={"CODEX_HOME": "/codex-home"},
            secret_plans=plans,
            noegress=None,
            pass_fds=[p.fd for p in plans])
        if noegress:
            from .noegress import NoEgressSpec
            spec.noegress = NoEgressSpec()
        return spec

    def _launch(self, request: dict, payload_argv, *, noegress: bool) \
            -> boundary_mod.BoundaryResult:
        launcher = self.policy.boundary_launcher or boundary_launch
        spec = self._boundary_spec(request, payload_argv, noegress)
        return launcher(spec, timeout=120.0)

    def _run_noegress(self, request: dict) -> dict:
        if self.policy.fault_noegress_fail:
            return {"passed": False,
                    "failures": ["FAULT_INJECTION:noegress"]}
        result = self._launch(request, None, noegress=True)
        gate = result.gate
        if gate is None:
            return {"passed": False,
                    "failures": [f"NO_GATE_RECORD:rc={result.returncode}",
                                 result.stderr[:300]]}
        self._record("NOEGRESS_GATE", passed=gate.get("passed"),
                     failures=gate.get("failures", []),
                     netns=gate.get("netns_inode"))
        return {"passed": bool(gate.get("passed")),
                "failures": gate.get("failures", [])}

    def _freeze_profile(self, request: dict) -> dict:
        identity = CodexIdentity(
            version=request["identity_version"],
            sha256=request["identity_sha256"],
            exe_path=request["identity_exe_path"])
        verify_codex_identity(identity)
        failures = validate_profile_semantics(request["config_path"],
                                              _spec_from_request(request))
        if failures:
            raise PolicyDrift(
                "PROFILE_SEMANTICS_INVALID:" + ",".join(failures))
        artifact = {"config_sha256": _config_sha(request["config_path"])}
        frozen = freeze_profile(artifact, identity)
        if self.policy.fault_identity_drift:
            raise IdentityDrift("FAULT_INJECTION:identity-drift")
        if self.policy.fault_policy_drift:
            raise PolicyDrift("FAULT_INJECTION:policy-drift")
        # freeze-verify round trip (detects drift between generation and
        # launch composition)
        verify_frozen_profile(frozen, artifact, identity)
        self.frozen_profile = frozen
        return frozen

    def _run_gatew(self, request: dict) -> dict:
        if self.policy.fault_gatew_fail:
            return {"passed": False, "failures": ["FAULT_INJECTION:gatew"]}
        payload_argv = ["/usr/bin/python3",
                        "/opt/qh/fixtures/gatew_payload.py",
                        "--result-file", boundary_mod.RESULT_FILE_INNER]
        result = self._launch(request, payload_argv, noegress=True)
        gate = result.gate
        payload = result.payload_result
        failures: list[str] = []
        if gate is None or not gate.get("passed"):
            failures.append("GATEW_NOEGRESS_FAILED")
        if payload is None:
            failures.append(f"GATEW_PAYLOAD_ABSENT:rc={result.returncode}")
        else:
            if not payload.get("all_expected"):
                for op in payload.get("ops", []):
                    if op.get("expect") != op.get("actual"):
                        failures.append(
                            f"GATEW_OP:{op.get('name')}:{op.get('path')}"
                            f":expect={op.get('expect')}"
                            f"actual={op.get('actual')}")
            if self.custody is not None and \
                    not payload.get("custody_file_present"):
                failures.append("GATEW_CUSTODY_FILE_ABSENT")
        self._record("GATEW_RESULT", passed=not failures, failures=failures)
        return {"passed": not failures, "failures": failures}

    def _protected_launch(self, request: dict) -> dict:
        payload_argv = ["/usr/bin/python3",
                        "/opt/qh/fixtures/launch_sim_payload.py",
                        "--result-file", boundary_mod.RESULT_FILE_INNER]
        result = self._launch(request, payload_argv, noegress=True)
        payload = result.payload_result
        if payload is None or not payload.get("ok"):
            return {"ok": False,
                    "failures": [f"rc={result.returncode}",
                                 result.stderr[:300]]}
        return {"ok": True, "payload": payload}

    # -- plumbing -------------------------------------------------------

    def _refuse(self, reason: str, **extra) -> dict:
        self._record("REFUSED", reason=reason, **extra)
        return {"ok": False, "reason": reason,
                "state": self.machine.state}

    def _refuse_terminal(self, reason: str) -> dict:
        self.machine.force_terminal_preexec_stop(reason)
        self._record("TERMINAL_PREEXEC_STOP", reason=reason)
        self._record("REFUSED", reason=reason)
        self.exit_code = 9
        return {"ok": False, "reason": reason,
                "state": self.machine.state}

    def _fail_closed(self, reason: str, *, exit_code: int) -> None:
        self._record("FAIL_CLOSED", reason=reason)
        self.exit_code = exit_code

    def _record(self, event: str, **facts) -> None:
        scrubbed = {k: (self.redactor.scrub(str(v)) if isinstance(v, str)
                        else v) for k, v in facts.items()}
        try:
            self.ledger.append(event, attempt_id=self.grant.attempt_id,
                               **scrubbed)
        except OSError:
            pass  # observability only — never an authority decision

    def shutdown(self) -> None:
        if self.custody is not None:
            self.custody.teardown()
            self.custody = None
        if self._socket is not None:
            try:
                self._socket.close()
            except OSError:
                pass
            self._socket = None
        self._record("SUPERVISOR_EXIT", code=self.exit_code,
                     state=self.machine.state)


def _peer_cred(conn: socket.socket) -> tuple[int, int, int]:
    data = conn.getsockopt(socket.SOL_SOCKET, SO_PEERCRED,
                           struct.calcsize("iHH"))
    pid, uid, gid = struct.unpack("iHH", data)
    return pid, uid, gid


def _config_sha(config_path: str) -> str:
    from .util import sha256_file
    return sha256_file(config_path)


def _spec_from_request(request: dict):
    from .codex_profile import ProfileSpec
    return ProfileSpec(
        profile_name=request.get("profile_name", "auditor-restricted"),
        model_name=request.get("model_name", "probe"),
        evidence_read_paths=tuple(
            request.get("evidence_read_paths", ("/evidence",))),
        extra_read_paths=tuple(request.get("extra_read_paths", ())),
        target_read_paths=tuple(request.get("target_read_paths", ())))
