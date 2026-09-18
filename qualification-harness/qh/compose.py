"""Composition — the integrated zero-provider C1 -> C2 -> C3 rehearsal.

Proves the ACCEPTED ORDER (not isolated component passes):

  1. pre-controller bootstrap manifest created;
  2. controller binding established;
  3. C4' process/provenance verification passes;
  4. one-shot attempt authority bound;
  5. credential custody established with synthetic credentials;
  6. no-egress gate passes;
  7. exact Codex identity/profile frozen;
  8. GATE-W passes;
  9. grant consumed exactly once for the protected local launch
     simulation;
 10. any subsequent reuse fails closed.

and every fail-closed branch (C4' failure, custody failure, Yama
failure simulation, no-egress failure, inherited socket FD, GATE-W
failure, policy drift, Codex binary identity drift, replay, ledger/file
deletion).  NO real provider process is ever launched: payloads are
local deterministic scripts, credentials are synthetic inert fixtures,
and every boundary launch runs under hard no-egress.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from .authority import Grant, mint_attempt_grant
from .bootstrap import capture_bootstrap_manifest
from .campaign import EngagementLedger
from .codex_profile import ProfileSpec, generate_codex_home
from .custody import SyntheticInertAdapter
from .ledger import ObservabilityLedger
from .util import sha256_bytes, sha256_file

HARNESS_ROOT = str(Path(__file__).resolve().parent.parent)
PY = sys.executable or "/usr/bin/python3"

SYNTHETIC_CREDENTIAL = ("SYNTHETIC-INERT-CREDENTIAL-do-not-use-"
                        "qh-0f1e2d3c4b5a")


def synthetic_credential(nonce: str = "") -> str:
    """Deterministic synthetic inert credential fixtures only — never a
    real provider credential."""
    return SYNTHETIC_CREDENTIAL + nonce


class CompositionEnv:
    """Deterministic full-environment builder for tests and the demo."""

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
        self.codex_artifact = generate_codex_home(
            self.profile_spec, str(self.codex_home_dir))
        self.codex_bin = self._make_synthetic_codex_binary()
        self.engagements = EngagementLedger(str(self.operator_state))
        self.engagements.authorize(2, note="composition test baseline")
        self._spawned_procs: list = []
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
        """A synthetic codex-like executable whose sha256 the harness
        pins (identity pinning is generic — it pins whatever executable
        the operator supplies)."""
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

    def mint(self, attempt_id: str) -> Grant:
        import io
        buf = io.StringIO()
        # in-process OPERATOR mint (explicitly labeled channel); the
        # subprocess CLI path enforces the real pipe contract
        grant = mint_attempt_grant(
            attempt_id=attempt_id, root=str(self.root),
            manifest_id=self.manifest.manifest_id,
            operator_state_dir=str(self.operator_state),
            out_stream=buf, operator_inmemory=True)
        return grant

    def spawn_supervisor(self, grant: Grant, *,
                         custody_value: str | None = SYNTHETIC_CREDENTIAL,
                         yama_override: int | None = None,
                         faults: list[str] | None = None,
                         operator_pid: int | None = None,
                         grant_stdin_file: str | None = None,
                         custody_file: str | None = None) \
            -> subprocess.Popen:
        """Spawn the supervisor as a REAL subprocess (dumpable=0,
        process-bound authority) WITHOUT waiting for readiness."""
        argv = [PY, "-m", "qh.cli", "supervisor",
                "--operator-state", str(self.operator_state)]
        pass_fds = []
        kwargs: dict = {}
        if custody_value is not None:
            r, w = os.pipe()
            os.write(w, custody_value.encode("utf-8"))
            os.close(w)
            argv += ["--custody-fd", str(r)]
            pass_fds.append(r)
        if custody_file is not None:
            # custody arriving via an ORDINARY FILE — the copied/persisted
            # channel the custody contract refuses (negative test path)
            fh = open(custody_file, "rb")  # noqa: SIM115
            argv += ["--custody-fd", str(fh.fileno())]
            pass_fds.append(fh.fileno())
            self._custody_fh = fh
        if yama_override is not None:
            argv += ["--yama-override", str(yama_override)]
        for f in faults or []:
            argv += ["--fault", f]
        if operator_pid is not None:
            argv += ["--operator-pid", str(operator_pid)]
        env = dict(os.environ,
                   PYTHONPATH=HARNESS_ROOT + os.pathsep +
                   os.environ.get("PYTHONPATH", ""))
        if grant_stdin_file is not None:
            stdin = open(grant_stdin_file, "rb")  # noqa: SIM115
            kwargs["stdin"] = stdin
        else:
            r, w = os.pipe()
            os.write(w, (json.dumps(grant.full_doc()) + "\n")
                     .encode("utf-8"))
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
        """Kill any supervisor this env spawned that is still alive
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
        import time as _time
        proc = self.spawn_supervisor(grant, **kwargs)
        deadline = _time.monotonic() + 30
        line = ""
        while _time.monotonic() < deadline:
            line = proc.stdout.readline().decode("utf-8", "replace").strip()
            if line.startswith("READY") or not line:
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

    def controller_request(self, attempt_id: str, *,
                           overrides: dict | None = None,
                           env_claims: dict | None = None,
                           own_session_slug: str | None = None,
                           wait_proc: subprocess.Popen | None = None,
                           timeout: float = 180.0) -> dict:
        """Spawn the synthetic controller and run one launch request.
        ``own_session_slug`` pre-creates the controller-runtime-shaped
        current-session tree (projects/<slug>/...) exactly as an
        auto-creating controller runtime would."""
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
        req_path = self.base / f"request-{attempt_id}.json"
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
        ident = self.identity
        return {
            "attempt_id": attempt_id,
            "root": str(self.root),
            "manifest_id": self.manifest.manifest_id,
            "controller_pid": None,  # derived from SO_PEERCRED
            "env_claims": {},
            "codex_home": str(self.codex_home_dir),
            "config_path": self.codex_artifact["config_path"],
            "profile_name": self.profile_spec.profile_name,
            "model_name": self.profile_spec.model_name,
            "identity_version": ident["version"],
            "identity_sha256": ident["sha256"],
            "identity_exe_path": ident["exe_path"],
            "harness_root": HARNESS_ROOT,
            "evidence_src": str(self.evidence),
            "auditor_output_src": str(self.auditor_output),
            "target_src": str(self.target),
            "payload_kind": "launch_sim",
        }

    def ledger_records(self) -> list[dict]:
        return ObservabilityLedger(str(self.operator_state)).read_all()


def run_composition_demo(out_dir: str) -> dict:
    """The zero-provider integrated rehearsal demo (happy path + reuse
    refusal + engagement-accounting separation)."""
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    report: dict = {"composition_order": [
        "manifest", "controller_binding", "c4p", "authority_bound",
        "custody", "noegress", "identity_profile_frozen", "gatew",
        "consumed_launch", "reuse_refused"]}
    env = CompositionEnv(os.path.join(out_dir, "workspace"))
    attempt = "demo-attempt-0001"
    grant = env.mint(attempt)
    eng_before = env.engagements.snapshot()
    sup = env.start_supervisor(grant)
    # controller with its own current-session tree already created
    response = env.controller_request(
        attempt, own_session_slug="own-project-slug")
    sup.wait(timeout=30)
    marker = env.auditor_output / "launch-sim-marker.txt"
    eng_after = env.engagements.snapshot()
    reuse = env.controller_request(attempt)
    report["happy_path"] = {
        "ok": bool(response.get("ok")),
        "response": response,
        "marker_present": marker.is_file(),
        "engagements_before": eng_before,
        "engagements_after": eng_after,
        "engagements_untouched": eng_before == eng_after,
        "reuse_refused": not reuse.get("ok"),
        "reuse_response": reuse,
    }
    report["ledger"] = env.ledger_records()
    return report
