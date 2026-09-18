"""Composition — the integrated zero-provider C1 -> C2 -> C3 rehearsal
over the REMEDIATED authority-root flow.

Proves the ACCEPTED ORDER (not isolated component passes):

  1. legitimate authority root initialized from operator-only capability
     (spec + custody arrive on operator pipes, BEFORE any controller
     request);
  2. trusted launch spec frozen/bound before controller-triggered launch;
  3. bootstrap/controller binding validated (C4');
  4. controller request authenticated/bound (CLAIM-ONLY schema);
  5. request claims cannot change the trusted spec (unknown fields are
     terminal);
  6. credential custody established through the root channel;
  7. hard no-egress gate passes;
  8. trusted executable/profile identity passes (spec-bound);
  9. GATE-W passes;
 10. one-shot launch authority consumed;
 11. protected LOCAL synthetic payload launch succeeds;
 12. any subsequent reuse fails closed;
 13. fresh controller-created authority imitations cannot launch with
     legitimate custody/spec.

and every fail-closed branch.  NO real provider process is ever launched:
payloads are local deterministic scripts, credentials are synthetic inert
fixtures, and every boundary launch runs under hard no-egress.
"""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

from .adapters import (CODEX_CHATGPT_OAUTH, CLAUDE_FIRSTPARTY_OAUTH,
                       SYNTHETIC_INERT)
from .authority import Grant, mint_attempt_grant
from .bootstrap import capture_bootstrap_manifest
from .campaign import EngagementLedger
from .codex_profile import ProfileSpec, generate_codex_home, \
    render_config_toml
from .custody import SyntheticInertAdapter
from .ledger import ObservabilityLedger
from .trusted_spec import (build_pre_controller_template, canonical_spec_bytes,
                           canonical_template_bytes, finalize_spec, spec_id,
                           template_id)
from .util import sha256_bytes, sha256_file

HARNESS_ROOT = str(Path(__file__).resolve().parent.parent)
PY = sys.executable or "/usr/bin/python3"

SYNTHETIC_CREDENTIAL = ("SYNTHETIC-INERT-CREDENTIAL-do-not-use-"
                        "qh-0f1e2d3c4b5a")

ADAPTERS_BY_ROLE = {
    "codex": CODEX_CHATGPT_OAUTH,
    "claude": CLAUDE_FIRSTPARTY_OAUTH,
    "inert": SYNTHETIC_INERT,
}


class BoundController:
    """A live controller process the OPERATOR can authorize into the
    trusted launch spec (CR-REMED-004): started BEFORE the spec is
    authored, driven by one command per stdin line (mint/request via
    fixtures/bound_controller.py).  Every request payload it carries is a
    CLAIM; it never holds authority values."""

    def __init__(self, *, claude_config_dir: str,
                 extra_env: dict | None = None,
                 hold_argv: list[str] | None = None) -> None:
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
               "CLAUDE_CONFIG_DIR": claude_config_dir}
        if extra_env:
            env.update(extra_env)
        self.proc = subprocess.Popen(
            [PY, str(Path(HARNESS_ROOT) / "fixtures" /
                     "bound_controller.py")],
            env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, cwd="/tmp")
        line = self.proc.stdout.readline()
        ready = json.loads(line)
        assert ready.get("type") == "ready", ready
        self.pid: int = ready["pid"]
        from .util import proc_starttime
        st = proc_starttime(self.pid)
        assert st is not None, "controller starttime unreadable"
        self.starttime: str = st
        self.uid = os.getuid()
        self._stopped = False

    def _cmd(self, op: str, socket_base: str, payload: dict) -> dict:
        assert not self._stopped and self.proc.poll() is None
        self.proc.stdin.write(json.dumps(
            {"cmd": op, "socket": socket_base, "payload": payload}) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            return {"ok": False, "reason": "CONTROLLER_NO_RESPONSE"}
        return json.loads(line).get("resp", {"ok": False,
                                             "reason": "BAD_RESP"})

    def mint(self, root_socket_base: str, payload: dict) -> dict:
        return self._cmd("mint", root_socket_base, payload)

    def request(self, supervisor_socket_base: str, payload: dict) -> dict:
        return self._cmd("request", supervisor_socket_base, payload)

    def stop(self) -> None:
        if not self._stopped:
            self._stopped = True
            try:
                if self.proc.poll() is None:
                    self.proc.stdin.write('{"cmd": "exit"}\n')
                    self.proc.stdin.flush()
                self.proc.wait(timeout=10)
            except Exception:  # noqa: BLE001 — teardown best effort
                self.proc.kill()
                try:
                    self.proc.wait(timeout=5)
                except Exception:  # noqa: BLE001
                    pass


def synthetic_credential(nonce: str = "") -> str:
    """Deterministic synthetic inert credential fixtures only — never a
    real provider credential."""
    return SYNTHETIC_CREDENTIAL + nonce


def _git_provenance(harness_root: str) -> dict | None:
    """Best-effort operator-side Git source-identity capture for the §18
    provenance tuple (repository full name, exact source commit,
    qualification-harness Git tree SHA).  Purely EVIDENCE: the trust
    decision binds to the operator-selected content digest; a version
    string alone is never provenance.  Returns None outside a Git
    worktree."""
    import subprocess as _sp
    repo = str(Path(harness_root).resolve().parent)
    try:
        def _git(*args: str) -> str:
            return _sp.run(["git", "-C", repo, *args],
                           capture_output=True, text=True,
                           timeout=10).stdout.strip()
        commit = _git("rev-parse", "HEAD")
        if not commit:
            return None
        url = _git("remote", "get-url", "origin")
        harness_tree = _git("rev-parse", "HEAD:qualification-harness")
        return {"source_role": "qualification-harness",
                "repository": url or repo,
                "source_commit": commit,
                "harness_git_tree": harness_tree or ""}
    except Exception:  # noqa: BLE001 — provenance evidence is optional
        return None


class CompositionEnv:
    """Deterministic full-environment builder for tests and the demo
    (operator side: authors the trusted launch spec and starts the
    authority root; controller side: claim-only requests)."""

    def __init__(self, base_dir: str, *,
                 profile_spec: ProfileSpec | None = None) -> None:
        self.base = Path(base_dir).resolve()
        self.root = self.base / "attempt-root"
        self.config_dir = self.base / "controller-config"
        self.evidence = self.base / "evidence"
        self.auditor_output = self.base / "auditor-output"
        self.codex_home_dir = self.base / "codex-home"
        self.operator_state = self.base / "operator-state"
        self.target = self.base / "target"
        for d in (self.root, self.config_dir, self.evidence,
                  self.auditor_output, self.operator_state, self.target):
            d.mkdir(parents=True, exist_ok=True)
        (self.evidence / "evidence.md").write_text(
            "# synthetic evidence fixture\nqh deterministic evidence\n",
            encoding="utf-8")
        (self.target / "target-source.txt").write_text(
            "synthetic target/source fixture\n", encoding="utf-8")
        self.profile_spec = profile_spec or self.default_profile_spec()
        # generated restricted-profile home (static-validation surface for
        # tests; the supervisor renders its own spec-bound copy at launch)
        self.codex_artifact = generate_codex_home(
            self.profile_spec, str(self.codex_home_dir))
        self.codex_bin = self._make_synthetic_codex_binary()
        self.engagements = EngagementLedger(str(self.operator_state))
        self.engagements.authorize(2, note="composition test baseline")
        self._spawned_procs: list = []
        self._controllers: list = []
        self._controller: BoundController | None = None
        self._spec: dict | None = None
        self._template: dict | None = None
        self._attempt: str | None = None
        self._bound: BoundController | None = None
        self._authority_proc = None
        self.finalization_w: int | None = None
        self.phase_line: str | None = None
        self.manifest = capture_bootstrap_manifest(
            str(self.config_dir), str(self.operator_state))
        if not self.manifest.ok:
            raise RuntimeError(
                f"bootstrap capture failed: {self.manifest.reason}")

    # -- the operator-authorized controller instance (CR-REMED-004) ------

    @property
    def controller(self) -> BoundController:
        """The DEFAULT controller instance for this environment (lazy):
        the process whose uid/pid/starttime the operator authors into the
        trusted launch spec."""
        if self._controller is None:
            self._controller = self.spawn_controller(
                claude_config_dir=str(self.config_dir))
        return self._controller

    def spawn_controller(self, *, claude_config_dir: str,
                         extra_env: dict | None = None) -> BoundController:
        ctrl = BoundController(claude_config_dir=claude_config_dir,
                               extra_env=extra_env)
        self._controllers.append(ctrl)
        return ctrl

    @staticmethod
    def default_profile_spec() -> ProfileSpec:
        return ProfileSpec(profile_name="audit",
                           description="auditor-b restricted",
                           model_name="probe")

    def _make_synthetic_codex_binary(self) -> str:
        """A synthetic codex-like executable whose sha256 the SPEC pins
        (identity pinning is generic — it pins the operator-authorized
        executable identity)."""
        path = self.base / "codex-like-binary"
        path.write_text(
            "#!/bin/sh\n# synthetic codex-like executable (zero-provider "
            "fixture)\necho 'codex-cli synthetic-fixture'\n",
            encoding="utf-8")
        path.chmod(0o755)
        return str(path)

    @property
    def identity(self) -> dict:
        return {"version": "codex-cli synthetic-fixture",
                "sha256": sha256_file(self.codex_bin),
                "exe_path": self.codex_bin}

    # -- operator side: pre-controller template + two-phase authority ---

    def author_template(self, attempt_id: str, *,
                        role: str = "codex",
                        payload_kind: str = "launch_sim",
                        harness_root: str | None = None,
                        adapter_id: str | None = None,
                        expected_harness_tree_digest: str | None = None,
                        harness_provenance: dict | None = None) -> dict:
        """Author the PRE-CONTROLLER LAUNCH TEMPLATE (CR-HARDEN-001): all
        security-critical values except the controller identity.  The
        expected harness identity defaults to the operator's computation
        from the harness source AT AUTHORING TIME in the trusted
        pre-controller phase; an independently established value (trusted
        pristine copy / Git object bytes) can be supplied explicitly —
        the authority always verifies the LIVE tree against the supplied
        value before any controller exists."""
        from .trusted_spec import harness_tree_digest
        adapter = ADAPTERS_BY_ROLE[role]
        if adapter_id is not None:
            from .adapters import get_adapter
            adapter = get_adapter(adapter_id)
        hroot = harness_root or HARNESS_ROOT
        if expected_harness_tree_digest is None:
            expected_harness_tree_digest = harness_tree_digest(hroot)
        if harness_provenance is None:
            harness_provenance = _git_provenance(hroot)
        config = render_config_toml(self.profile_spec)
        self._template = build_pre_controller_template(
            attempt_id=attempt_id,
            attempt_root=str(self.root),
            config_dir=str(self.config_dir),
            manifest_id=self.manifest.manifest_id,
            evidence_src=str(self.evidence),
            auditor_output_src=str(self.auditor_output),
            target_src=str(self.target),
            codex_exe=self.codex_bin,
            codex_version=self.identity["version"],
            profile=self._profile_dict(),
            config_sha256=sha256_bytes(config.encode("utf-8")),
            credential_adapter={
                "id": adapter.adapter_id,
                "provider_role": adapter.provider_role,
                "version": adapter.version},
            harness_root=hroot,
            expected_harness_tree_digest=expected_harness_tree_digest,
            harness_provenance=harness_provenance,
            payload_kind=payload_kind)
        self._attempt = attempt_id
        self._spec = None
        return self._template

    def author_spec(self, attempt_id: str, **kwargs) -> dict:
        """Backward-compatible alias: author the pre-controller template
        (the final spec is completed by Phase-B finalization — see
        ``finalize``).  Returns the TEMPLATE."""
        return self.author_template(attempt_id, **kwargs)

    def _profile_dict(self) -> dict:
        p = self.profile_spec
        return {"profile_name": p.profile_name,
                "description": p.description,
                "model_name": p.model_name,
                "workspace_role": p.workspace_role,
                "evidence_read_paths": list(p.evidence_read_paths),
                "target_read_paths": list(p.target_read_paths),
                "system_read_paths": list(p.system_read_paths),
                "extra_read_paths": list(p.extra_read_paths),
                "network_enabled": p.network_enabled}

    @property
    def template(self) -> dict:
        if self._template is None:
            raise RuntimeError("author_template() not called yet")
        return self._template

    @property
    def spec(self) -> dict:
        if self._spec is not None:
            return self._spec
        if self._template is not None:
            # lazy derivation against the (default or already-bound)
            # controller identity — the production authority performs this
            # finalization itself inside its trusted process
            ctrl = self._bound or self.controller
            self._bound = ctrl
            self._spec = finalize_spec(
                self._template, controller_uid=ctrl.uid,
                controller_pid=ctrl.pid,
                controller_starttime=ctrl.starttime)
            return self._spec
        raise RuntimeError("author_template() not called yet")

    def spawn_authority(self, template: dict | None = None, *,
                        custody_value: str | None = SYNTHETIC_CREDENTIAL,
                        mint_timeout: float = 300.0,
                        template_fd: int | None = None) \
            -> subprocess.Popen:
        """PHASE A: start the AUTHORITY as a real subprocess while NO
        controller exists, and wait until it reports PRECONTROLLER_READY
        (the pre-controller trusted freeze is complete: template sealed,
        live tree verified against the operator identity, privileged byte
        set frozen+sealed, all privileged modules loaded with code-object
        provenance, import guard armed).  The finalization pipe is
        created HERE (before controller startup): the write end stays
        with the operator (``self.finalization_w``) and is never passed
        to any controller."""
        tpl = template if template is not None else self.template
        # the DELIVERED template is the operative one for all later
        # derivation (finalization delta id, lazy final spec)
        self._template = tpl
        self._spec = None
        cr, cw = os.pipe()
        if custody_value is not None:
            os.write(cw, custody_value.encode("utf-8"))
        os.close(cw)
        fin_r, fin_w = os.pipe()
        self.finalization_w = fin_w
        argv = [PY, "-m", "qh.cli", "authority",
                "--operator-state", str(self.operator_state),
                "--custody-fd", str(cr),
                "--finalization-fd", str(fin_r),
                "--mint-timeout", str(mint_timeout)]
        pass_fds = [cr, fin_r]
        if template_fd is not None:
            argv += ["--template-fd", str(template_fd)]
            pass_fds.append(template_fd)
        # production semantics: the authority process loads its privileged
        # code from EXACTLY the harness tree the template pins (the
        # pre-controller freeze verifies this mechanically and refuses
        # any mismatch)
        harness_root = tpl["harness"]["root"]
        env = dict(os.environ,
                   PYTHONPATH=harness_root + os.pathsep +
                   os.environ.get("PYTHONPATH", ""))
        proc = subprocess.Popen(
            argv, pass_fds=tuple(pass_fds), stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
            cwd=str(self.base))
        os.close(cr)
        os.close(fin_r)
        if template_fd is None:
            proc.stdin.write(canonical_template_bytes(tpl))
            proc.stdin.close()
        self._spawned_procs.append(proc)
        self._authority_proc = proc
        line = self._wait_phase(proc, "PRECONTROLLER_READY",
                                "authority pre-controller startup failed")
        self.phase_line = line
        return proc

    def finalize(self, *, controller: BoundController | None = None,
                 delta: dict | None = None, expect_ready: bool = True) -> None:
        """PHASE B: after the operator has started the authorized
        controller (post-PRECONTROLLER_READY), send the finalization
        delta over the operator-held finalization channel.  ``delta``
        defaults to the frozen template id + the bound controller's
        actual uid/pid/starttime."""
        assert self.finalization_w is not None, \
            "spawn_authority() must run first"
        ctrl = controller if controller is not None else \
            (self._bound or self.controller)
        if delta is None:
            delta = {"template_id": template_id(self.template),
                     "authorized_controller": {
                         "uid": ctrl.uid, "pid": ctrl.pid,
                         "starttime": ctrl.starttime}}
        self._bound = ctrl
        os.write(self.finalization_w,
                 (json.dumps(delta, sort_keys=True) + "\n").encode())
        os.close(self.finalization_w)
        self.finalization_w = None
        self._spec = finalize_spec(
            self.template, controller_uid=ctrl.uid, controller_pid=ctrl.pid,
            controller_starttime=ctrl.starttime)
        if expect_ready:
            line = self._wait_phase(self._authority_proc, "READY",
                                    "authority finalization failed")
            self.phase_line = line

    def _wait_phase(self, proc, needle: str, what: str) -> str:
        deadline = time.monotonic() + 30
        line = ""
        while time.monotonic() < deadline:
            line = proc.stdout.readline().decode("utf-8", "replace").strip()
            if line.startswith(needle) or not line or \
                    proc.poll() is not None:
                break
        if not line.startswith(needle):
            try:
                err = proc.stderr.read(4096).decode("utf-8", "replace")
                proc.wait(timeout=10)
            except Exception:  # noqa: BLE001
                err = "<unreadable>"
                proc.kill()
                proc.wait(timeout=10)
            raise RuntimeError(f"{what}: {line!r} stderr={err!r}")
        return line

    def spawn_root(self, template: dict | None = None, *,
                   spec: dict | None = None,
                   custody_value: str | None = SYNTHETIC_CREDENTIAL,
                   mint_timeout: float = 300.0,
                   template_fd: int | None = None,
                   controller: BoundController | None = None) \
            -> subprocess.Popen:
        """Backward-compatible one-shot driver of the COMPLETE two-phase
        flow (PHASE A spawn_authority → controller start → PHASE B
        finalize → READY).  ``template``/``spec`` accept a template
        override (the old final-spec override surface is gone: the final
        spec is authority-derived)."""
        if template is None and spec is not None:
            template = spec
        if template is None:
            if self._template is None:
                raise RuntimeError("author_template() not called yet")
            template = self._template
        proc = self.spawn_authority(
            template, custody_value=custody_value,
            mint_timeout=mint_timeout, template_fd=template_fd)
        self.finalize(controller=controller)
        return proc

    def root_socket_name(self, spec: dict | None = None) -> str:
        spec = spec if spec is not None else self.spec
        return "\0qh-root-" + spec_id(spec)[:16]

    def root_mint(self, attempt_id: str | None = None, *,
                  spec: dict | None = None,
                  request: dict | None = None,
                  timeout: float = 60.0) -> dict:
        """One mint request sent BY THE OPERATOR-AUTHORIZED CONTROLLER
        INSTANCE bound in the current spec (CR-REMED-004: the root
        enforces exact uid/pid/starttime at the trigger — the mint must
        come from the bound controller process or it is refused)."""
        name = self.root_socket_name(spec)
        payload = request if request is not None else {
            "attempt_id": attempt_id or self._attempt}
        ctrl = self._bound or self.controller
        return ctrl.mint(name[1:], payload)

    def raw_root_mint(self, attempt_id: str | None = None, *,
                      spec: dict | None = None,
                      request: dict | None = None,
                      timeout: float = 60.0) -> dict:
        """ATTACK CHANNEL (tests): the calling process itself connects to
        the root trigger — a same-UID peer that is NOT the pre-bound
        controller.  The hardened root must refuse it."""
        name = self.root_socket_name(spec)
        payload = request if request is not None else {
            "attempt_id": attempt_id or self._attempt}
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect(name)
        except OSError as exc:
            return {"ok": False,
                    "reason": f"ROOT_CONNECT_FAILED:{type(exc).__name__}"}
        with s:
            s.sendall((json.dumps(payload, sort_keys=True) + "\n")
                      .encode("utf-8"))
            data = b""
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    break
                data += chunk
        try:
            return json.loads(data.decode("utf-8", "replace").strip())
        except json.JSONDecodeError:
            return {"ok": False, "reason": "ROOT_NO_RESPONSE"}

    # -- in-process operator mint (explicitly-labeled TEST channel) -----

    def mint(self, attempt_id: str) -> Grant:
        import io
        buf = io.StringIO()
        grant = mint_attempt_grant(
            attempt_id=attempt_id, root=str(self.root),
            manifest_id=self.manifest.manifest_id,
            operator_state_dir=str(self.operator_state),
            out_stream=buf, operator_inmemory=True)
        return grant

    def spawn_supervisor(self, grant: Grant, spec: dict | None = None, *,
                         custody_value: str | None = SYNTHETIC_CREDENTIAL,
                         grant_stdin_file: str | None = None,
                         custody_file: str | None = None,
                         expect_spec: bytes | None = None) \
            -> subprocess.Popen:
        """Spawn the supervisor as a REAL subprocess (dumpable=0,
        process-bound authority) WITHOUT waiting for readiness.  Grant and
        trusted launch spec arrive on the stdin pipe; custody on an
        inherited pipe/memfd fd."""
        spec = spec if spec is not None else self.spec
        argv = [PY, "-m", "qh.cli", "supervisor",
                "--operator-state", str(self.operator_state)]
        pass_fds = []
        kwargs: dict = {}
        if custody_value is not None or custody_file is not None:
            if custody_file is not None:
                fh = open(custody_file, "rb")  # noqa: SIM115
                argv += ["--custody-fd", str(fh.fileno())]
                pass_fds.append(fh.fileno())
                self._custody_fh = fh
            else:
                r, w = os.pipe()
                os.write(w, custody_value.encode("utf-8"))
                os.close(w)
                argv += ["--custody-fd", str(r)]
                pass_fds.append(r)
        env = dict(os.environ,
                   PYTHONPATH=HARNESS_ROOT + os.pathsep +
                   os.environ.get("PYTHONPATH", ""))
        spec_bytes = (expect_spec if expect_spec is not None
                      else canonical_spec_bytes(spec))
        if grant_stdin_file is not None:
            stdin = open(grant_stdin_file, "rb")  # noqa: SIM115
            kwargs["stdin"] = stdin
        else:
            r, w = os.pipe()
            os.write(w, (json.dumps(grant.full_doc()) + "\n").encode()
                     + spec_bytes + b"\n")
            os.close(w)
            kwargs["stdin"] = r
            pass_fds.append(r)
        proc = subprocess.Popen(
            argv, pass_fds=tuple(pass_fds), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env,
            cwd=str(self.base), **kwargs)
        if grant_stdin_file is None:
            os.close(r)
        self._spawned_procs.append(proc)
        return proc

    def cleanup_procs(self) -> None:
        """Kill any root/supervisor/controller this env spawned that is
        still alive (test teardown hygiene — prevents abstract-socket
        leaks)."""
        import subprocess as _sp
        for proc in getattr(self, "_spawned_procs", []):
            if proc.poll() is None:
                proc.kill()
                try:
                    proc.wait(timeout=5)
                except _sp.TimeoutExpired:
                    pass
        for ctrl in getattr(self, "_controllers", []):
            ctrl.stop()
        if getattr(self, "finalization_w", None) is not None:
            try:
                os.close(self.finalization_w)
            except OSError:
                pass
            self.finalization_w = None

    def bootstrap_provenance(self) -> dict:
        """The authority's recorded §18 provenance tuple + module-load
        inventory (observability copy written at Phase A)."""
        assert self._template is not None
        path = self.operator_state / "bootstrap" / \
            f"{template_id(self._template)[:16]}.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def start_supervisor(self, grant: Grant, **kwargs) \
            -> subprocess.Popen:
        """Spawn and wait until the abstract socket is bound (READY)."""
        proc = self.spawn_supervisor(grant, **kwargs)
        deadline = time.monotonic() + 30
        line = ""
        while time.monotonic() < deadline:
            line = proc.stdout.readline().decode("utf-8", "replace").strip()
            if line.startswith("READY") or not line or proc.poll() is not None:
                break
        if not line.startswith("READY"):
            try:
                err = proc.stderr.read(4096).decode("utf-8", "replace")
                proc.wait(timeout=10)
            except Exception:  # noqa: BLE001
                err = "<unreadable>"
                proc.kill()
                proc.wait(timeout=10)
            raise RuntimeError(
                f"supervisor startup failed: {line!r} stderr={err!r}")
        return proc

    def supervisor_outcome(self, proc: subprocess.Popen,
                           timeout: float = 60.0) -> tuple[int, str]:
        """Wait for exit; return (returncode, collected stderr)."""
        import selectors
        sel = selectors.DefaultSelector()
        sel.register(proc.stderr, selectors.EVENT_READ)
        chunks = b""
        while sel.select(timeout):
            chunk = proc.stderr.read1(65536)
            if not chunk:
                break
            chunks += chunk
        proc.wait(timeout=timeout)
        return proc.returncode, chunks.decode("utf-8", "replace")

    def root_outcome(self, proc: subprocess.Popen,
                     timeout: float = 120.0) -> tuple[int, str]:
        return self.supervisor_outcome(proc, timeout=timeout)

    def controller_request(self, attempt_id: str, *,
                           overrides: dict | None = None,
                           env_claims: dict | None = None,
                           own_session_slug: str | None = None,
                           timeout: float = 300.0) -> dict:
        """Run one CLAIM-ONLY launch request FROM THE OPERATOR-AUTHORIZED
        CONTROLLER INSTANCE (the persistent bound controller process —
        CR-REMED-004: the supervisor enforces the same pre-bound
        uid/pid/starttime at request acceptance)."""
        if own_session_slug is not None:
            slug_dir = self.config_dir / "projects" / own_session_slug
            slug_dir.mkdir(parents=True, exist_ok=True)
            (slug_dir / "session-abc123.jsonl").write_text(
                '{"synthetic":"current-session"}\n', encoding="utf-8")
        request = self.build_request(attempt_id)
        if overrides:
            request.update(overrides)
        claims = {"CLAUDE_CONFIG_DIR": str(self.config_dir)}
        if env_claims:
            claims.update(env_claims)
        request["env_claims"] = claims
        ctrl = self._bound or self.controller
        self._bound = ctrl
        name_base = self.supervisor_socket_name(attempt_id)[1:]
        return ctrl.request(name_base, request)

    def raw_controller_request(self, supervisor_socket: str,
                               request: dict,
                               timeout: float = 60.0) -> dict:
        """ATTACK CHANNEL (tests): the calling process itself connects to
        the supervisor socket — a same-UID peer that is NOT the pre-bound
        controller.  The hardened supervisor must refuse it."""
        name = (supervisor_socket if supervisor_socket.startswith("\0")
                else "\0" + supervisor_socket)
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect(name)
        except OSError as exc:
            return {"ok": False,
                    "reason": f"CONNECT_FAILED:{type(exc).__name__}"}
        with s:
            s.sendall((json.dumps(request, sort_keys=True) + "\n")
                      .encode("utf-8"))
            data = b""
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    break
                data += chunk
        try:
            return json.loads(data.decode("utf-8", "replace").strip())
        except json.JSONDecodeError:
            return {"ok": False, "reason": "NO_RESPONSE"}

    def supervisor_socket_name(self, attempt_id: str) -> str:
        import hashlib
        digest = hashlib.sha256(
            json.dumps({"attempt": attempt_id}, sort_keys=True,
                       separators=(",", ":")).encode()).hexdigest()
        return "\0qh-" + digest[:16]

    def build_request(self, attempt_id: str) -> dict:
        """CLAIM-ONLY request schema: no security-critical values."""
        return {
            "attempt_id": attempt_id,
            "controller_starttime": None,
            "env_claims": {},
            "payload_kind": "launch_sim",
        }

    def run_attempt(self, attempt_id: str, *, role: str = "codex",
                    own_slug: str = "own-slug",
                    overrides: dict | None = None) -> dict:
        """The full remediated happy path: root up -> mint -> controller
        request -> outcomes.  The supervisor is the ROOT's child, so the
        root's exit reflects the supervised attempt lifecycle."""
        self.author_spec(attempt_id, role=role)
        root = self.spawn_root()
        mint = self.root_mint(attempt_id)
        if not mint.get("ok"):
            rc, err = self.root_outcome(root)
            return {"ok": False, "phase": "mint", "mint": mint,
                    "root_rc": rc, "root_stderr": err[-400:]}
        response = self.controller_request(attempt_id, overrides=overrides,
                                           own_session_slug=own_slug)
        rc, err = self.root_outcome(root, timeout=300)
        marker = self.auditor_output / "launch-sim-marker.txt"
        return {"ok": bool(response.get("ok")), "response": response,
                "root_rc": rc, "root_stderr": err[-400:],
                "marker_present": marker.is_file()}

    def ledger_records(self) -> list[dict]:
        return ObservabilityLedger(str(self.operator_state)).read_all()


def run_composition_demo(out_dir: str) -> dict:
    """The zero-provider integrated rehearsal demo over the authority-root
    flow (happy path + reuse refusal + engagement-accounting separation +
    controller imitation powerlessness)."""
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    report: dict = {"composition_order": [
        "authority_root_initialized_from_operator_capability",
        "trusted_spec_frozen_before_controller_trigger",
        "controller_binding", "c4p", "trusted_spec_verify",
        "authority_bound", "adapter_bound", "custody",
        "trusted_bytes_snapshot", "noegress", "identity_profile_frozen",
        "gatew", "consumed_launch", "reuse_refused"]}
    env = CompositionEnv(os.path.join(out_dir, "workspace"))
    attempt = "demo-attempt-0001"
    result = env.run_attempt(attempt)
    eng_before = env.engagements.snapshot()
    reuse = env.controller_request(attempt)
    eng_after = env.engagements.snapshot()
    # a controller-created imitation root: its own spec, own state dir,
    # own credential — it can only produce a powerless imitation
    fake_dir = env.base / "fake-controller-root"
    fake_env = CompositionEnv(str(fake_dir))
    fake_spec = fake_env.author_spec("controller-imitation-0001")
    fake_root = fake_env.spawn_root(fake_spec,
                                    custody_value="CONTROLLER-OWNED-FAKE")
    fake_mint = fake_env.root_mint("controller-imitation-0001")
    fake_resp = (fake_env.controller_request("controller-imitation-0001")
                 if fake_mint.get("ok") else {"ok": False})
    fake_env.root_outcome(fake_root, timeout=300)
    fake_env.cleanup_procs()
    report["happy_path"] = {
        "ok": bool(result.get("ok")),
        "response": result.get("response"),
        "marker_present": result.get("marker_present"),
        "engagements_before": eng_before,
        "engagements_after": eng_after,
        "engagements_untouched": eng_before == eng_after,
        "reuse_refused": not reuse.get("ok"),
        "reuse_response": reuse,
    }
    report["controller_imitation"] = {
        "mint_ok": bool(fake_mint.get("ok")),
        "launch_ok": bool(fake_resp.get("ok")),
        "used_controller_owned_fake_custody": True,
        "legitimate_custody_value_used": False,
    }
    report["ledger"] = env.ledger_records()
    env.cleanup_procs()
    return report
