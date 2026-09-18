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
from .trusted_spec import canonical_spec_bytes, spec_id, build_spec
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


def synthetic_credential(nonce: str = "") -> str:
    """Deterministic synthetic inert credential fixtures only — never a
    real provider credential."""
    return SYNTHETIC_CREDENTIAL + nonce


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
        self._spec: dict | None = None
        self._attempt: str | None = None
        self.manifest = capture_bootstrap_manifest(
            str(self.config_dir), str(self.operator_state))
        if not self.manifest.ok:
            raise RuntimeError(
                f"bootstrap capture failed: {self.manifest.reason}")

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

    # -- operator side: trusted launch spec + authority root ------------

    def author_spec(self, attempt_id: str, *,
                    role: str = "codex",
                    payload_kind: str = "launch_sim",
                    harness_root: str | None = None,
                    adapter_id: str | None = None) -> dict:
        adapter = ADAPTERS_BY_ROLE[role]
        if adapter_id is not None:
            from .adapters import get_adapter
            adapter = get_adapter(adapter_id)
        config = render_config_toml(self.profile_spec)
        self._spec = build_spec(
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
            harness_root=harness_root or HARNESS_ROOT,
            payload_kind=payload_kind)
        self._attempt = attempt_id
        return self._spec

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
    def spec(self) -> dict:
        if self._spec is None:
            raise RuntimeError("author_spec() not called yet")
        return self._spec

    def spawn_root(self, spec: dict | None = None, *,
                   custody_value: str | None = SYNTHETIC_CREDENTIAL,
                   require_seals: bool = False,
                   mint_timeout: float = 300.0) -> subprocess.Popen:
        """Start the AUTHORITY ROOT as a real subprocess (non-dumpable,
        process-bound spec + custody) and wait until its socket is bound."""
        spec = spec if spec is not None else self.spec
        cr, cw = os.pipe()
        if custody_value is not None:
            os.write(cw, custody_value.encode("utf-8"))
        os.close(cw)
        argv = [PY, "-m", "qh.cli", "root",
                "--operator-state", str(self.operator_state),
                "--custody-fd", str(cr),
                "--mint-timeout", str(mint_timeout)]
        if require_seals:
            argv.append("--require-seals")
        env = dict(os.environ,
                   PYTHONPATH=HARNESS_ROOT + os.pathsep +
                   os.environ.get("PYTHONPATH", ""))
        proc = subprocess.Popen(
            argv, pass_fds=(cr,), stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
            cwd=str(self.base))
        os.close(cr)
        proc.stdin.write(canonical_spec_bytes(spec))
        proc.stdin.close()
        self._spawned_procs.append(proc)
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
                f"authority root startup failed: {line!r} stderr={err!r}")
        return proc

    def root_socket_name(self, spec: dict | None = None) -> str:
        spec = spec if spec is not None else self.spec
        return "\0qh-root-" + spec_id(spec)[:16]

    def root_mint(self, attempt_id: str | None = None, *,
                  spec: dict | None = None,
                  request: dict | None = None,
                  timeout: float = 60.0) -> dict:
        """One mint request against the live authority root (as the
        controller or operator would send it — the request carries NO
        authority values)."""
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
        """Kill any root/supervisor this env spawned that is still alive
        (test teardown hygiene — prevents abstract-socket leaks)."""
        import subprocess as _sp
        for proc in getattr(self, "_spawned_procs", []):
            if proc.poll() is None:
                proc.kill()
                try:
                    proc.wait(timeout=5)
                except _sp.TimeoutExpired:
                    pass

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
        """Spawn the synthetic controller and run one CLAIM-ONLY launch
        request against the supervisor socket."""
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
        req_path = self.base / f"request-{attempt_id}-{time.monotonic_ns()}.json"
        req_path.write_text(json.dumps(request, sort_keys=True),
                            encoding="utf-8")
        argv = [PY, str(Path(HARNESS_ROOT) / "fixtures" /
                        "fake_controller.py"),
                "--request", str(req_path), "--attempt", attempt_id]
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(self.config_dir),
                   PYTHONPATH=HARNESS_ROOT + os.pathsep +
                   os.environ.get("PYTHONPATH", ""))
        proc = subprocess.run(argv, capture_output=True, text=True,
                              timeout=timeout, env=env)
        try:
            return json.loads(proc.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            return {"ok": False, "reason": "CONTROLLER_NO_RESPONSE",
                    "stdout": proc.stdout[-400:], "stderr": proc.stderr[-400:]}

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
