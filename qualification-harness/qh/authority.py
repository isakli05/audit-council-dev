"""C-2 / G-1 — process-bound single-use launch authority (supervising
gatekeeper), IR-002-remediated: SPEC-AUTHORITATIVE launch values.

Accepted design (G-1 DESIGN_PROBE_CLOSURE_ACCEPTED) — preserved:

* authority is minted only through an operator/Control-Room-side path
  OUTSIDE the controller's writable authority surface (remediated: the
  ONLY production mint is performed by the authority root, which receives
  the trusted launch spec + provider custody through operator-held FDs —
  see qh/rootauth.py; the grant blob never exists in any ordinary file);
* kernel/process-bound authority: the supervisor immediately sets
  PR_SET_DUMPABLE=0 and requires Yama ptrace_scope >= 1 (a REAL kernel
  read — no override exists on any production path);
* exact attempt/root binding; one-shot consumption; replay/second-use
  refusal; copied-grant refusal (pipe-only);
* terminal PREEXEC_STOP: any failed mandatory preexec gate transitions the
  attempt to TERMINAL_PREEXEC_STOP and the supervisor exits — filesystem
  deletion/recreation cannot restore launch authority;
* supervisor SIGKILL is fail-closed denial (DoS) only;
* a genuinely new attempt requires a NEW operator/root authorization;
  pre-inference PREEXEC stop does NOT consume campaign auditor/model
  authority (qh/campaign.py is never touched by this lifecycle).

IR-002 remediation delta:

* the supervisor receives the COMPLETE TRUSTED LAUNCH SPEC from the
  authority root (pipe) and treats every request value as a CLAIM: the
  request schema carries ONLY attempt id, starttime claim, env claims and
  payload kind — harness_root, boundary child, evidence/target/auditor-
  output sources, codex home/config/exe/sha, profile and mount policy are
  NO LONGER request fields at all;
* the full spec is re-verified against the live filesystem at launch
  (TRUSTED_SPEC_VERIFY) and a NEW mandatory gate verifies claim/spec
  agreement;
* trusted harness/boundary/config/executable BYTES are snapshotted into
  process-bound memfds at verification time and materialized inside the
  boundary via bwrap --bind-data — the protected launch never executes
  host-path code, closing the controller-selected harness_root defect
  mechanically (no check-to-use window on code bytes);
* the Codex identity pin is the SPEC-BOUND expected identity checked
  against the ACTUAL executable bytes — a controller can no longer supply
  both the executable and its matching hash.
"""
from __future__ import annotations

import ctypes
import json
import os
import socket
import stat
import struct
import tempfile
from dataclasses import dataclass, field

from . import boundary as boundary_mod
from . import trusted_spec
from .adapters import get_adapter
from .boundary import BoundarySpec, DataFile, launch as boundary_launch
from .campaign import EngagementLedger
from .codex_profile import (CodexIdentity, IdentityDrift, PolicyDrift,
                            ProfileSpec, freeze_profile, render_config_toml,
                            validate_profile_semantics,
                            verify_codex_identity, verify_frozen_profile)
from .bootstrap import ControllerBinding, load_manifest, verify_c4p
from .custody import CredentialCustody, CustodyError
from .ledger import ObservabilityLedger
from .statemachine import (AttemptState, AttemptStateMachine,
                           InvalidTransition)
from .util import (Redactor, content_id, hold_bytes_memfd,
                   proc_starttime as _proc_starttime,
                   read_yama_ptrace_scope, sha256_bytes, utc_now_iso)

PR_SET_DUMPABLE = 4
PR_SET_PDEATHSIG = 1
SO_PEERCRED = 17


def _pr_set_pdeathsig() -> None:
    """Die with the authority root (SIGKILL when parent dies): the
    supervisor's authority never outlives the root that minted it, and a
    killed root cannot leave a listening supervisor behind."""
    import signal
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(PR_SET_PDEATHSIG, signal.SIGKILL, 0, 0, 0) != 0:
        raise AuthorityError("PR_SET_PDEATHSIG_FAILED")

# claim-only request schema: nothing in a controller request is authority
ALLOWED_CLAIM_FIELDS = frozenset(
    {"attempt_id", "controller_starttime", "env_claims", "payload_kind"})


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
    root_pid: int | None = None
    spec_id: str | None = None

    def public_doc(self) -> dict:
        """Ledger-safe projection: NO secret."""
        return {"grant_id": self.grant_id, "attempt_id": self.attempt_id,
                "root": self.root, "root_dev": self.root_dev,
                "root_ino": self.root_ino, "manifest_id": self.manifest_id,
                "created_at": self.created_at}

    def full_doc(self) -> dict:
        return {**self.public_doc(), "secret": self.secret,
                "root_pid": self.root_pid, "spec_id": self.spec_id}


def mint_attempt_grant(*, attempt_id: str, root: str, manifest_id: str,
                       operator_state_dir: str,
                       out_stream=None,
                       redactor: Redactor | None = None,
                       operator_inmemory: bool = False) -> Grant:
    """Operator/Control-Room-side mint.  PRODUCTION callers are the
    authority root ONLY (the unrestricted public CLI mint is removed);
    ``operator_inmemory=True`` is the explicit in-process OPERATOR path
    used by the root, tests and composition (recorded in the ledger).
    The grant is written ONLY to a PIPE-style stream; a regular-file
    output is refused.  ``root_pid`` records the MINTING process so the
    spawned supervisor can mechanically require its parent to be the
    minting root (never a caller-supplied CLI value).  Duplicate attempt
    ids are refused (a genuinely new attempt requires a NEW out-of-band
    root authorization)."""
    ledger = ObservabilityLedger(operator_state_dir)
    if attempt_id in ledger.attempt_ids_minted():
        raise AuthorityError(
            f"ATTEMPT_ALREADY_MINTED: {attempt_id} — a new attempt "
            "requires a NEW out-of-band operator/root authorization with "
            "a fresh attempt id")
    if not os.path.isdir(root):
        raise AuthorityError(f"ROOT_NOT_A_DIRECTORY: {root}")
    st = os.lstat(root)
    grant = Grant(
        grant_id=_new_grant_id(),
        attempt_id=attempt_id,
        root=root,
        root_dev=st.st_dev,
        root_ino=st.st_ino,
        manifest_id=manifest_id,
        secret=_new_grant_secret(),
        created_at=utc_now_iso(),
        root_pid=os.getpid())
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
    if channel == "pipe":
        out_stream.write(json.dumps(grant.full_doc()) + "\n")
        out_stream.flush()
    ledger.append("MINTED", channel=channel, **grant.public_doc())
    return grant


def _new_grant_id() -> str:
    import secrets as _secrets
    return _secrets.token_hex(16)


def _new_grant_secret() -> str:
    import secrets as _secrets
    return _secrets.token_urlsafe(32)


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
    """Injectable VERIFICATION seams for deterministic adversarial tests
    (readers/launcher only).  NO fault-injection or trust-decision override
    exists here: production reads REAL values and every gate failure is
    real (test fault injection monkeypatches these seams or the module's
    real readers — never a production CLI flag)."""
    env_reader: object = None              # None -> /proc/<pid>/environ
    stat_reader: object = None             # None -> /proc/<pid>/stat
    walker: object = None                  # None -> real scope walk
    set_dumpable: bool = True
    require_custody: bool = True
    boundary_launcher: object = None       # None -> real boundary launch


@dataclass
class RequestClaims:
    """The controller request is a CLAIM, never authority (IR-002)."""
    attempt_id: str
    controller_starttime: str | None
    env_claims: dict[str, str]
    payload_kind: str


class Supervisor:
    """The one-shot supervising gatekeeper.  Production instances are
    spawned by the AUTHORITY ROOT (their parent is the root process — the
    grant's root_pid binding is enforced at startup); the grant and the
    complete trusted launch spec arrive on a pipe and the custody memfd is
    inherited from the root."""

    def __init__(self, *, grant: Grant, spec: dict, spec_id: str,
                 operator_state_dir: str,
                 custody_fd: int | None,
                 policy: SupervisorPolicy | None = None,
                 bootstrap=None) -> None:
        self.grant = grant
        self.spec = spec
        self.spec_id = spec_id
        self.operator_state_dir = operator_state_dir
        self.custody_fd = custody_fd
        self.bootstrap = bootstrap  # frozen PrivilegedBootstrap (CR-REMED-002)
        self.policy = policy or SupervisorPolicy()
        self.redactor = Redactor()
        self.redactor.register(grant.secret, "grant-secret")
        self.ledger = ObservabilityLedger(operator_state_dir)
        self.engagements = EngagementLedger(operator_state_dir)
        self.machine = AttemptStateMachine()
        self.custody: CredentialCustody | None = None
        self.frozen_profile: dict | None = None
        self._socket: socket.socket | None = None
        self._snapshot: list[DataFile] | None = None
        self.exit_code = 0

    # -- lifecycle ----------------------------------------------------

    def startup(self) -> None:
        self._record("SUPERVISOR_UP", grant=self.grant.grant_id,
                     pid=os.getpid(), ppid=os.getppid())
        if self.grant.root_pid is not None and \
                os.getppid() != self.grant.root_pid:
            self._fail_closed("ROOT_PID_MISMATCH", exit_code=5)
            return
        _pr_set_pdeathsig()
        if os.getppid() == 1 and self.grant.root_pid is not None:
            # parent already died between fork and prctl — refuse
            self._fail_closed("ROOT_PID_GONE", exit_code=5)
            return
        if self.policy.set_dumpable:
            pr_set_dumpable(0)
            self._record("PR_SET_DUMPABLE_0")
        yama = read_yama_ptrace_scope()
        if yama is None or yama < 1:
            # MANDATORY environmental gate: fail closed when absent.  The
            # REAL kernel knob is always read; no override exists.
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
            peer_pid, peer_uid, _gid = _peer_cred(conn)
            try:
                line = conn.makefile("r").readline()
                request = json.loads(line)
            except Exception as exc:  # noqa: BLE001
                self._fail_closed(f"REQUEST_UNPARSEABLE:{exc!r}",
                                  exit_code=8)
                return {"ok": False, "reason": "request_unparseable"}
            response = self.handle_request(request, peer_pid=peer_pid,
                                           peer_uid=peer_uid)
            try:
                conn.sendall((json.dumps(response, sort_keys=True) + "\n")
                             .encode("utf-8"))
            except OSError:
                pass
        self.shutdown()
        return response

    # -- request pipeline (the recorded composition order) -------------

    def handle_request(self, request: dict, *, peer_pid: int,
                       peer_uid: int | None = None) -> dict:
        self._record("REQUEST_RECEIVED", peer_pid=peer_pid)
        if self.machine.state != AttemptState.MINTED:
            return self._refuse("REPLAY_OR_TERMINAL_STATE",
                                state=self.machine.state)

        # [IR-002] the request is a CLAIM, never authority: unknown
        # security-critical fields are refused outright (they can no
        # longer supply harness_root / binds / executable / config /
        # profile / adapter values — those fields do not exist).
        unknown = sorted(set(request) - ALLOWED_CLAIM_FIELDS)
        if unknown:
            return self._refuse_terminal(
                "UNKNOWN_CLAIM_FIELD:" + ",".join(unknown))
        if request.get("attempt_id") != self.grant.attempt_id:
            return self._refuse_terminal("WRONG_ATTEMPT")
        if request.get("payload_kind") != self.spec["payload"]["kind"]:
            return self._refuse_terminal("PAYLOAD_KIND_CLAIM_MISMATCH")

        # exact root binding vs the minted grant (root is grant-bound,
        # never request-supplied)
        try:
            st = os.lstat(self.grant.root)
            if (st.st_dev, st.st_ino) != \
                    (self.grant.root_dev, self.grant.root_ino):
                # deleted/recreated root = different object = refusal
                return self._refuse_terminal("ROOT_IDENTITY_CHANGED")
        except OSError:
            return self._refuse_terminal("ROOT_IDENTITY_CHANGED")

        # [CR-REMED-004] the peer must be the SAME pre-bound authorized
        # controller instance the OPERATOR authored into the trusted spec
        # (and that the root already verified at the mint trigger): exact
        # uid/pid + the peer's ACTUAL /proc starttime.  The connected
        # peer never defines its own authorization; knowledge of the
        # attempt/socket/manifest or a reproduced CLAUDE_CONFIG_DIR tree
        # is not the capability.
        if "authorized_controller" not in self.spec:
            return self._refuse_terminal(
                "AUTHORIZED_CONTROLLER_NOT_BOUND_IN_SPEC")
        ac = self.spec["authorized_controller"]
        actual_start = (self.policy.stat_reader or _proc_starttime)(peer_pid)
        if peer_uid is not None and peer_uid != ac["uid"]:
            return self._refuse_terminal(
                f"AUTHORIZED_CONTROLLER_MISMATCH:uid peer={peer_uid} "
                f"bound={ac['uid']}")
        if peer_pid != ac["pid"]:
            return self._refuse_terminal(
                f"AUTHORIZED_CONTROLLER_MISMATCH:pid peer={peer_pid} "
                f"bound={ac['pid']}")
        if actual_start is None or str(actual_start) != str(ac["starttime"]):
            return self._refuse_terminal(
                f"AUTHORIZED_CONTROLLER_MISMATCH:starttime "
                f"actual={actual_start} bound={ac['starttime']}")

        # [composition 2] controller binding established
        starttime = actual_start
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

        # [IR-002] TRUSTED SPEC VERIFY — the complete security-critical
        # launch specification is checked against the LIVE filesystem,
        # EXCEPT the harness-tree identity when a frozen privileged
        # bootstrap exists (CR-REMED-002): the harness check is then made
        # against the FROZEN sealed bundle bytes, so later ordinary
        # host-tree mutation cannot derail or alter the protected flow.
        harness_override = (self.bootstrap.digest_from_files()
                            if self.bootstrap is not None else None)
        spec_failures = trusted_spec.verify_spec(
            self.spec, expected_spec_id=self.spec_id,
            harness_digest_override=harness_override)
        self._record("TRUSTED_SPEC_VERIFY",
                     passed=not spec_failures, failures=spec_failures)
        if spec_failures:
            return self._refuse_terminal(
                "TRUSTED_SPEC_VERIFY_FAIL:" + ",".join(spec_failures))

        # [composition 4] one-shot attempt authority bound
        try:
            self.machine.transition(AttemptState.BOUND,
                                    "controller-verified grant binding")
        except InvalidTransition as exc:
            return self._refuse_terminal(f"STATE:{exc}")
        self._record("AUTHORITY_BOUND", controller_pid=peer_pid)

        # [composition 5] credential custody (MANDATORY, spec-bound
        # adapter identity)
        try:
            self.machine.transition(AttemptState.PREEXEC_CHECKING,
                                    "preexec gates")
        except InvalidTransition as exc:
            return self._refuse_terminal(f"STATE:{exc}")
        try:
            adapter = get_adapter(self.spec["credential_adapter"]["id"])
            self._record("CREDENTIAL_ADAPTER_BOUND",
                         adapter_id=adapter.adapter_id,
                         provider_role=adapter.provider_role,
                         version=adapter.version)
        except Exception as exc:  # noqa: BLE001 — AdapterError, fail closed
            return self._refuse_terminal(f"CREDENTIAL_ADAPTER_INVALID:"
                                         f"{exc}")
        if self.policy.require_custody:
            if self.custody_fd is None:
                return self._refuse_terminal("CUSTODY_FD_NOT_PROVIDED")
            try:
                self.custody = CredentialCustody.establish(
                    self.custody_fd,
                    label=f"attempt-{self.grant.attempt_id}",
                    redactor=self.redactor)
            except CustodyError as exc:
                return self._refuse_terminal(f"CUSTODY_ESTABLISH_FAILED:"
                                             f"{exc}")
            self._record("CUSTODY_ESTABLISHED",
                         label=self.custody.label,
                         length=self.custody.length)

        # [composition 6] trusted-bytes snapshot (AFTER spec verify, so
        # the snapshot is exactly the verified bytes; memfd-held so no
        # host-path code executes inside the protected launch)
        try:
            self._snapshot = self._build_trusted_snapshot()
        except (trusted_spec.SpecError, OSError, PolicyDrift,
                IdentityDrift) as exc:
            return self._refuse_terminal(f"TRUSTED_SNAPSHOT_FAILED:{exc}")
        self._record("TRUSTED_BYTES_SNAPSHOTTED",
                     files=len(self._snapshot))

        # [composition 7] hard no-egress gate
        noegress = self._run_noegress()
        if not noegress["passed"]:
            return self._refuse_terminal(
                "NOEGRESS_FAIL:" + ",".join(noegress["failures"]))

        # [composition 8] exact Codex identity/profile frozen (SPEC-bound)
        try:
            frozen = self._freeze_profile()
        except IdentityDrift as exc:
            return self._refuse_terminal(f"CODEX_IDENTITY_DRIFT:{exc}")
        except PolicyDrift as exc:
            return self._refuse_terminal(f"PROFILE_POLICY_DRIFT:{exc}")
        self._record("PROFILE_FROZEN", **frozen)

        # [composition 9] GATE-W zero-provider rehearsal
        gatew = self._run_gatew()
        if not gatew["passed"]:
            return self._refuse_terminal(
                "GATEW_FAIL:" + ",".join(gatew["failures"]))

        # [composition 10] consume exactly once + protected local launch
        try:
            self.machine.transition(AttemptState.CONSUMED_FOR_LAUNCH,
                                    "protected local launch simulation")
        except InvalidTransition as exc:
            return self._refuse_terminal(f"STATE:{exc}")
        self._record("CONSUMED_FOR_LAUNCH")
        launch = self._protected_launch()
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

    # -- trusted-bytes snapshot -----------------------------------------

    def _build_trusted_snapshot(self) -> list[DataFile]:
        """Snapshot the VERIFIED harness executable byte set, the rendered
        config and the verified provider executable into process-bound
        MANDATORILY SEALED memfds.  These bytes — and only these —
        execute/apply inside the boundary (materialized via bwrap
        --bind-data).

        CR-REMED-002: when the supervisor was forked from the authority
        root's frozen bootstrap, the harness code bytes come from the
        FROZEN SEALED BUNDLE — never from a fresh host read."""
        hroot = self.spec["harness"]["root"]
        # rendered restricted profile config from SPEC parameters
        config = render_config_toml(self._profile_spec())
        config_sha = sha256_bytes(config.encode("utf-8"))
        if config_sha != self.spec["codex"]["config_sha256"]:
            raise PolicyDrift(
                f"PROFILE_CONFIG_DIGEST_MISMATCH: spec-bound "
                f"{self.spec['codex']['config_sha256']} rendered "
                f"{config_sha}")
        adapter = get_adapter(self.spec["credential_adapter"]["id"])
        config_targets = [t for kind, t in adapter.extra_files
                          if kind == "config"]
        # the rendered restricted profile config is ALWAYS materialized at
        # the generic rehearsal CODEX_HOME (the GATE-W matrix reads it
        # regardless of provider role); a role-specific config target
        # takes precedence when the adapter declares one
        config_target = (config_targets[0] if config_targets
                         else "/run-qh/codex-home/config.toml")
        # verified provider executable (identity-checked bytes)
        exe = self.spec["codex"]["exe"]["path"]
        exe_data = _read_file(exe)
        if sha256_bytes(exe_data) != self.spec["codex"]["exe"]["sha256"]:
            raise IdentityDrift("CODEX_BINARY_IDENTITY_DRIFT")
        extra = [DataFile(
            fd=_hold(exe_data, "qh-trusted-exe"),
            inner_path="/run-qh/trusted-provider-exe",
            sha256=sha256_bytes(exe_data), secret=False, mode=0o755)]
        if self.bootstrap is not None:
            return boundary_mod.snapshot_data_files_from_files(
                self.bootstrap.files,
                config=config.encode("utf-8"),
                config_target=config_target, extra=extra)
        return boundary_mod.snapshot_data_files(
            hroot, config=config.encode("utf-8"),
            config_target=config_target, extra=extra)

    def _profile_spec(self) -> ProfileSpec:
        p = dict(self.spec["codex"]["profile"])
        for k in ("evidence_read_paths", "target_read_paths",
                  "system_read_paths", "extra_read_paths"):
            if k in p:
                p[k] = tuple(p[k])
        return ProfileSpec(**p)

    # -- boundary composition (SPEC-authoritative) ----------------------

    def _boundary_spec(self, phase: str) -> BoundarySpec:
        """phase: "gate" (noegress), "gatew" (rehearsal, inert custody
        target — the accepted GATE-W matrix), or "protected" (spec-bound
        provider adapter target)."""
        from .adapters import INERT_ADAPTER_ID, get_adapter as _ga
        adapter = _ga(self.spec["credential_adapter"]["id"])
        inert = _ga(INERT_ADAPTER_ID)
        target = (adapter.credential_target if phase == "protected"
                  else inert.credential_target)
        secret_plans = []
        if self.custody is not None:
            secret_plans.append(self.custody.child_plan(target))
        env = {"CODEX_HOME": "/run-qh/codex-home"}
        if phase == "protected":
            env.update(adapter.env)
            env.update({
                "QH_ADAPTER_ID": adapter.adapter_id,
                "QH_ADAPTER_PROVIDER_ROLE": adapter.provider_role,
                "QH_ADAPTER_TARGET": adapter.credential_target,
                "QH_ADAPTER_MODE": oct(adapter.credential_mode),
                "QH_CUSTODY_LENGTH": str(self.custody.length
                                         if self.custody else 0),
                "QH_TRUSTED_EXE": "/run-qh/trusted-provider-exe",
                "QH_TRUSTED_EXE_SHA256":
                    self.spec["codex"]["exe"]["sha256"],
            })
        else:
            env["QH_CUSTODY_TARGET"] = inert.credential_target
        ro_binds = [(self.spec["sources"]["evidence"]["path"], "/evidence")]
        if self.spec["sources"].get("target") is not None:
            ro_binds.append((self.spec["sources"]["target"]["path"],
                             "/target"))
        spec = BoundarySpec(
            harness_root=self.spec["harness"]["root"],
            payload_argv=None,  # set by the caller per phase
            ro_binds=ro_binds,
            rw_binds=[(self.spec["sources"]["auditor_output"]["path"],
                       "/auditor-output")],
            tmpfs_paths=["/tmp", "/run-qh"],
            env=env,
            secret_plans=secret_plans,
            data_files=list(self._snapshot or []),
            source_digests={
                "evidence": self.spec["sources"]["evidence"]["tree_digest"],
                **({"target": self.spec["sources"]["target"]["tree_digest"]}
                   if self.spec["sources"].get("target") is not None else {}),
            },
            noegress=None,
            pass_fds=[p.fd for p in secret_plans])
        if self.spec["noegress"]["required"]:
            from .noegress import NoEgressSpec
            spec.noegress = NoEgressSpec()
        return spec

    def _launch(self, payload_argv, *, phase: str) \
            -> boundary_mod.BoundaryResult:
        launcher = self.policy.boundary_launcher or boundary_launch
        spec = self._boundary_spec(phase)
        spec.payload_argv = payload_argv
        return launcher(spec, timeout=180.0)

    def _run_noegress(self) -> dict:
        result = self._launch(None, phase="gate")
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

    def _freeze_profile(self) -> dict:
        identity = CodexIdentity(
            version=self.spec["codex"]["version"],
            sha256=self.spec["codex"]["exe"]["sha256"],
            exe_path=self.spec["codex"]["exe"]["path"])
        verify_codex_identity(identity)
        config = render_config_toml(self._profile_spec())
        artifact = {"config_sha256":
                    sha256_bytes(config.encode("utf-8"))}
        with tempfile.TemporaryDirectory(prefix="qh-profile-") as tdir:
            cpath = os.path.join(tdir, "config.toml")
            with open(cpath, "w", encoding="utf-8") as fh:
                fh.write(config)
            failures = validate_profile_semantics(cpath,
                                                  self._profile_spec())
        if failures:
            raise PolicyDrift(
                "PROFILE_SEMANTICS_INVALID:" + ",".join(failures))
        frozen = freeze_profile(artifact, identity)
        # freeze-verify round trip (detects drift between generation and
        # launch composition)
        verify_frozen_profile(frozen, artifact, identity)
        self.frozen_profile = frozen
        return frozen

    def _run_gatew(self) -> dict:
        payload_argv = ["/usr/bin/python3",
                        "/opt/qh/fixtures/gatew_payload.py",
                        "--result-file", boundary_mod.RESULT_FILE_INNER]
        result = self._launch(payload_argv, phase="gatew")
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

    def _protected_launch(self) -> dict:
        payload_argv = ["/usr/bin/python3",
                        "/opt/qh/fixtures/launch_sim_payload.py",
                        "--result-file", boundary_mod.RESULT_FILE_INNER]
        result = self._launch(payload_argv, phase="protected")
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
        if self._snapshot is not None:
            for df in self._snapshot:
                try:
                    os.close(df.fd)
                except OSError:
                    pass
            self._snapshot = None
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


def _read_file(path: str) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


def _hold(data: bytes, name: str) -> int:
    fd, _status = hold_bytes_memfd(data, name=name)
    return fd
