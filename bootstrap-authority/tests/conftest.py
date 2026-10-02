"""Synthetic ZERO-PROVIDER / ZERO-NETWORK test fixtures for the
bootstrap-authority package.

Every artifact built here is SYNTHETIC / NON-AUTHORITATIVE /
NON-PERSISTENT: inert gate/launcher/auditor/validator scripts, a
temporary synthetic event package, synthetic non-secret credential
bytes, and temporary accounting/output directories inside
test-controlled temporary directories.  No fixture invokes Claude,
Codex, ChatGPT, any provider endpoint or any network route; no
synthetic fixture is canonical event instantiation; the
design-reserved event/attempt identity strings appear only as binding
CONSTRAINTS inside these throwaway worlds; all temporary state
disappears with the test workspace.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

AUTHORITY_ROOT = Path(__file__).resolve().parents[1]      # bootstrap-authority/
REPO_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(AUTHORITY_ROOT))

from bootstrap_authority import binding as bab                    # noqa: E402
from bootstrap_authority import runtime as bar                    # noqa: E402

SYNTHETIC_CREDENTIAL_PREFIX = b"SYNTHETIC-NOT-A-SECRET-CREDENTIAL-"
GATE_HEADER = "#!/usr/bin/python3\nimport json, sys\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True,
                      separators=(",", ":")).encode()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def authority_package_pins() -> dict:
    """Live pins of the REAL executing authority package MANIFEST."""
    raw = (AUTHORITY_ROOT / "MANIFEST.json").read_bytes()
    doc = json.loads(raw.decode("utf-8"))
    return {"manifest_sha256": sha256_bytes(raw),
            "package_sha256": doc["package_sha256"]}


def _write_exec(path: Path, text: str) -> bytes:
    data = text.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    os.chmod(path, 0o755)
    return data


def _write_bytes(path: Path, data: bytes) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    os.chmod(path, 0o644)
    return data


def gate_script(gate: str, order_file: Path, result_schema: str,
                tweak: dict = None) -> str:
    """Inert dynamic-gate script: binds its result to the argv context,
    appends its name to the shared ORDER file (execution-order and
    exactly-once evidence), and for NETWORK_READINESS embeds the
    child-side fd inventory (credential-leak evidence: no sealed memfd
    may ever be inherited by a gate).  `tweak` may force a wrong model
    echo for the client-selection preflight."""
    tweak = tweak or {}
    parts = [GATE_HEADER,
             "EVENT, ROLE, ATTEMPT = sys.argv[1:4]\n",
             "with open(%r, 'a') as order:\n    order.write(%r + '\\n')\n"
             % (str(order_file), gate),
             "base = {'schema': %r, 'status': 'PASS', 'event_id': EVENT,\n"
             "        'auditor_role': ROLE, 'attempt_id': ATTEMPT}\n"
             % result_schema]
    if gate == "CLIENT_SELECTION_PREFLIGHT":
        parts.append("PROVIDER, FAMILY, MODEL, EFFORT, CLI_ID, CLI_VER, "
                     "CLI_SHA = sys.argv[4:11]\n")
        if "model" in tweak:
            parts.append("MODEL = %r\n" % tweak["model"])
        parts.append(
            "result = dict(base, provider_role=PROVIDER, "
            "client_family=FAMILY,\n"
            "                model=MODEL, effort=EFFORT,\n"
            "                client_executable_identity=CLI_ID,\n"
            "                client_executable_version=CLI_VER,\n"
            "                client_executable_sha256=CLI_SHA)\n")
    elif gate == "NETWORK_READINESS":
        parts.append(
            "import os\n"
            "PROVIDER, LAUNCHER_SHA, PROFILE = sys.argv[4:7]\n"
            "fds = []\n"
            "for _name in os.listdir('/proc/self/fd'):\n"
            "    try:\n"
            "        fds.append(os.readlink('/proc/self/fd/' + _name))\n"
            "    except OSError:\n"
            "        pass\n"
            "fds.sort()\n"
            "result = dict(base, provider_role=PROVIDER,\n"
            "                boundary_launcher_sha256=LAUNCHER_SHA,\n"
            "                sandbox_profile_id=PROFILE,\n"
            "                checks={'route': {'status': 'PASS',\n"
            "                                   'detail': {'fd_inventory': "
            "fds}},\n"
            "                         'resolver': {'status': 'PASS',\n"
            "                                      'detail': {}}})\n")
    else:                                   # RESOURCE_GATE
        parts.append(
            "result = dict(base, samples=[{'status': 'PASS',\n"
            "                                 'detail': {'sample': n}}\n"
            "                              for n in range(3)])\n")
    parts.append("print(json.dumps(result))\n")
    return "".join(parts)


VALIDATOR_SCRIPT = GATE_HEADER + """import hashlib, json, os, sys
EVENT, ROLE, ATTEMPT, OUT_NAME, DIGEST, SIZE = sys.argv[1:7]
data = b""
while True:
    chunk = os.read(3, 65536)
    if not chunk:
        break
    data += chunk
if hashlib.sha256(data).hexdigest() != DIGEST or str(len(data)) != SIZE:
    sys.stderr.write("VALIDATION_ERROR: SNAPSHOT_MISMATCH")
    sys.exit(1)
try:
    doc = json.loads(data.decode("utf-8"))
    ok = isinstance(doc, dict) and all(k in doc for k in (
        "target_commit", "event_id", "auditor_role", "attempt_id",
        "findings"))
except Exception:
    ok = False
if not ok:
    sys.stderr.write("VALIDATION_ERROR: REPORT_NOT_JSON")
    sys.exit(1)
print(json.dumps({"schema": %r, "status": "PASS", "event_id": EVENT,
                  "auditor_role": ROLE, "attempt_id": ATTEMPT,
                  "output_name": OUT_NAME, "report_sha256": DIGEST,
                  "report_size": int(SIZE)}))
""" % bab.VALIDATOR_RESULT_SCHEMA


def launcher_script(mode: str = "ok", report_bytes: bytes = None,
                    cred_bytes: bytes = b"",
                    pid_file: Path = None) -> str:
    """Inert boundary launcher: reads the sealed invocation spec (fd 6),
    hashes the held auditor executable (fd 5), records its OWN argv +
    environment + fd observations as stdout metadata (the exact
    no-caller-override evidence), then behaves per mode: ok (write the
    embedded report into the invocation sink), none (no report), contam
    (report prefixed with the synthetic credential), replace (RB2-002
    adversarial: UNLINK the authority-created sink and write a fresh
    replacement object at the exact same pathname — never the held
    object), sleep (spawn a long-lived same-process-group child and
    hang), broken (unusable interpreter — handled by the caller writing
    a bad shebang)."""
    prep = ""
    if mode in ("ok", "sleep", "replace"):
        prep += "_REPORT = %r\n" % (report_bytes or b"{}\n")
    if mode == "contam":
        prep += "_CREDS = %r\n_REPORT = %r\n" % (cred_bytes,
                                                 report_bytes or b"{}\n")
    write_report = {
        "ok": ('    path = inv[inv.index("--report") + 1]\n'
               '    with open(path, "wb") as handle:\n'
               '        handle.write(_REPORT)\n'),
        "contam": ('    path = inv[inv.index("--report") + 1]\n'
                   '    with open(path, "wb") as handle:\n'
                   '        handle.write(_CREDS + _REPORT)\n'),
        "replace": ('    path = inv[inv.index("--report") + 1]\n'
                    '    os.unlink(path)\n'
                    '    with open(path, "wb") as handle:\n'
                    '        handle.write(_REPORT)\n'),
        "none": "", "sleep": "",
    }[mode]
    spawn = ('child = os.posix_spawn("/usr/bin/sleep", '
             '["/usr/bin/sleep", "300"], {"PATH": "/usr/bin:/bin"})\n'
             'meta["sleep_child_pid"] = child\n'
             'with open(%r, "w") as pid_file:\n'
             '    pid_file.write(str(child))\n'
             % str(pid_file)) if mode == "sleep" else ""
    sleep = ('if True:\n    import time\n    time.sleep(120)\n') \
        if mode == "sleep" else ""
    write_block = ("if True:\n" + write_report) if write_report else ""
    return GATE_HEADER + "import hashlib, json, os, sys\n" + prep + '''
invocation = b""
while True:
    chunk = os.read(6, 65536)
    if not chunk:
        break
    invocation += chunk
aud_sha = ""
try:
    h = hashlib.sha256()
    os.lseek(5, 0, os.SEEK_SET)
    while True:
        chunk = os.read(5, 65536)
        if not chunk:
            break
        h.update(chunk)
    aud_sha = h.hexdigest()
except OSError:
    pass
inv = json.loads(invocation)
meta = {"argv": list(sys.argv), "env": dict(os.environ),
        "invocation": inv, "auditor_fd_sha256": aud_sha,
        "cred_fd_link": os.readlink("/proc/self/fd/3")}
''' + spawn + '''sys.stdout.write(json.dumps(meta))
sys.stdout.flush()
''' + write_block + sleep


class World:
    """One synthetic attempt world (all inside one tmp directory)."""

    def __init__(self, root: Path, role: str, doc: dict, binding,
                 event_root: Path, output_root: Path, staging: Path,
                 order_file: Path, launcher_path: Path,
                 auditor_path: Path, credential: bytes,
                 sleep_pid_file: Path = None) -> None:
        self.root = root
        self.sleep_pid_file = sleep_pid_file
        self.role = role
        self.doc = doc
        self.binding = binding
        self.event_root = event_root
        self.output_root = output_root
        self.staging = staging
        self.order_file = order_file
        self.launcher_path = launcher_path
        self.auditor_path = auditor_path
        self.credential = credential
        self.metadata = None

    def attempt_name(self) -> str:
        return bar.accounting_name(self.binding)

    def inspect_record(self) -> dict:
        from bootstrap_authority.accounting import inspect_accounting_record
        return inspect_accounting_record(self.output_root,
                                         self.attempt_name(),
                                         self.binding.digest)

    def authority(self) -> "bar.BootstrapAuthority":
        return bar.BootstrapAuthority(self.binding, self.event_root)

    def run(self, launcher_path=None, auditor_path=None,
            source="pipe", authority=None):
        """Drive ONE full run_attempt with synthetic credentials from a
        pipe (default) or a fully sealed memfd; returns the
        AttemptResult or re-raises the refusal."""
        authority = authority or self.authority()
        if source == "pipe":
            r, w = os.pipe()
            os.write(w, self.credential)
            os.close(w)
        else:
            import fcntl
            r = os.memfd_create("synthetic-credential",
                                os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING)
            os.write(r, self.credential)
            os.lseek(r, 0, os.SEEK_SET)
            fcntl.fcntl(r, fcntl.F_ADD_SEALS, 15)
        try:
            return authority.run_attempt(
                r, launcher_path or self.launcher_path,
                auditor_path or self.auditor_path, self.staging,
                self.output_root)
        finally:
            try:
                os.close(r)
            except OSError:
                pass

    def make_report(self, **overrides) -> bytes:
        return make_report(self.binding, **overrides)


def make_report(binding, target_commit=None, event_id=None,
                auditor_role=None, attempt_id=None,
                findings="[]") -> bytes:
    doc = {
        "target_commit": target_commit or binding.target["commit"],
        "event_id": event_id or binding.event_id,
        "auditor_role": auditor_role or binding.auditor_role,
        "attempt_id": attempt_id or binding.attempt_id,
        "findings": findings,
    }
    return canonical(doc) + b"\n"


def build_world(tmp_path, role="AUDITOR_A", preflight_tweak=None,
                launcher_mode="ok", report=None, wall_timeout=60,
                authority_pins=None, output_root=None) -> World:
    """Assemble one complete synthetic world: event package + binding
    document pinned to the REAL executing authority package + inert
    executables + synthetic credential.  `report` defaults to a correct
    first-pass report for the role.  `output_root` may override the
    operator custody root (shared-root worlds) — the SAME path is then
    FROZEN into the binding's output_identity.custody_root."""
    root = Path(tmp_path) / "world"
    event_root = root / "event"
    output_root = Path(output_root) if output_root is not None \
        else Path(tmp_path) / "output"
    output_root.mkdir(parents=True, exist_ok=True)
    os.chmod(output_root, 0o700)
    # RB2: the report source is the authority-created attempt-owned sink,
    # a DIRECT child of the frozen custody root (one custody domain), and
    # the binding also freezes the custody directory OBJECT identity
    # (st_dev/st_ino at build time).
    staging = output_root / ("%s.staging-report.json"
                             % bab.RESERVED_ATTEMPT_IDS[role])
    custody_stat = os.stat(output_root)
    order_file = Path(tmp_path) / "order.log"
    sleep_pid_file = Path(tmp_path) / "sleep_child.pid"

    credential = SYNTHETIC_CREDENTIAL_PREFIX + role.encode()
    report = make_report_for_role(role) if report is None else report

    auditor_path = event_root / "client" / "auditor.bin"
    auditor_bytes = _write_exec(
        auditor_path,
        "#!/usr/bin/python3\nprint('INERT-SYNTHETIC-AUDITOR-EXECUTABLE')\n")
    launcher_path = event_root / "boundary" / "launcher.bin"
    if launcher_mode == "broken":
        launcher_bytes = _write_exec(launcher_path,
                                     "#!/nonexistent/interpreter\n")
    else:
        launcher_bytes = _write_exec(
            launcher_path, launcher_script(launcher_mode, report,
                                          credential, sleep_pid_file))
    wrapper_path = event_root / "tools" / "wrapper.bin"
    wrapper_bytes = _write_bytes(wrapper_path, b"INERT-TOOL-WRAPPER\n")

    gate_bytes = {}
    for gate in bab.DYNAMIC_GATE_ORDER:
        tweak = preflight_tweak if gate == "CLIENT_SELECTION_PREFLIGHT" \
            else None
        gate_bytes[gate] = _write_exec(
            event_root / "gates" / f"{gate.lower()}.py",
            gate_script(gate, order_file,
                        bab.DYNAMIC_GATE_RESULT_SCHEMAS[gate], tweak))
    validator_bytes = _write_exec(event_root / "validator" / "validator.py",
                                  VALIDATOR_SCRIPT)

    files = []
    for rel, data in (
            ("client/auditor.bin", auditor_bytes),
            ("boundary/launcher.bin", launcher_bytes),
            ("tools/wrapper.bin", wrapper_bytes),
            ("validator/validator.py", validator_bytes),
            *[(f"gates/{g.lower()}.py", b) for g, b in
              gate_bytes.items()]):
        files.append({"path": rel, "bytes": len(data),
                      "sha256": sha256_bytes(data)})

    doc = minimal_binding_doc(role, files, staging=staging,
                              auditor_sha=sha256_bytes(auditor_bytes),
                              wall_timeout=wall_timeout,
                              authority_pins=authority_pins,
                              output_root=output_root,
                              custody_dev=custody_stat.st_dev,
                              custody_ino=custody_stat.st_ino)
    binding = bab.parse_binding(canonical(doc))
    manifest = {"schema": bab.EVENT_MANIFEST_SCHEMA,
                "transport_binding": bab.binding_projection(binding),
                "files": files}
    manifest["package_sha256"] = sha256_bytes(canonical(manifest))
    (event_root / "MANIFEST.json").write_bytes(canonical(manifest) + b"\n")
    doc["event_package"]["package_sha256"] = manifest["package_sha256"]
    binding = bab.parse_binding(canonical(doc))
    return World(root, role, doc, binding, event_root, output_root,
                 staging, order_file, launcher_path, auditor_path,
                 credential, sleep_pid_file)


def make_report_for_role(role: str) -> bytes:
    return canonical({"attempt_id": bab.RESERVED_ATTEMPT_IDS[role],
                      "auditor_role": role, "event_id": bab.EVENT_ID,
                      "findings": "[]",
                      "target_commit": bab.FROZEN_TARGET["commit"]}) + b"\n"


def minimal_binding_doc(role="AUDITOR_A", event_files=None, staging=None,
                        auditor_sha=None, wall_timeout=60,
                        authority_pins=None, output_root=None,
                        custody_dev=2049, custody_ino=1048577) -> dict:
    """A complete VALID binding document for `role` with synthetic
    digests (or real artifact pins when supplied).  event_files may be
    None for pure parse-level tests.  output_identity freezes the
    attempt output custody root, the attempt-owned report sink (a
    DIRECT child of the custody root; RB2-002) and the custody
    directory OBJECT identity st_dev/st_ino (RB2-001): the real world
    values when supplied, synthetic canonical values otherwise."""
    hex64 = "a" * 64
    if auditor_sha is None:
        auditor_sha = hex64
    custody_root = str(output_root) if output_root is not None \
        else "/synthetic-operator-custody/output"
    report_source = str(staging) if staging is not None \
        else "%s/%s.staging-report.json" % (
            custody_root, bab.RESERVED_ATTEMPT_IDS[role])
    selection = dict(bab.AUDITOR_SELECTIONS[role])
    selection["client_executable"] = {
        "identity": "SYNTHETIC-INERT-CLIENT-V1",
        "version": "1.2.3-synthetic", "sha256": auditor_sha}
    doc = {
        "schema": bab.BINDING_SCHEMA,
        "policy_id": bab.POLICY_ID,
        "event_id": bab.EVENT_ID,
        "auditor_role": role,
        "attempt_id": bab.RESERVED_ATTEMPT_IDS[role],
        "target": dict(bab.FROZEN_TARGET),
        "common_evidence_manifest_digest": hex64,
        "prompt_contract_digest": hex64,
        "auditor_selection": selection,
        "boundary_launcher": {"identity": "INERT-LOCAL-FIXTURE-LAUNCHER-V1",
                              "path": "boundary/launcher.bin",
                              "sha256": hex64, "bytes": 1},
        "sandbox_profile_id": "SYNTHETIC-SANDBOX-PROFILE-V1",
        "tool_wrapper": {"identity": "INERT-LOCAL-FIXTURE-WRAPPER-V1",
                         "path": "tools/wrapper.bin",
                         "sha256": hex64, "bytes": 1},
        "authority_package": authority_pins or authority_package_pins(),
        "event_package": {"manifest_schema": bab.EVENT_MANIFEST_SCHEMA,
                          "package_sha256": hex64},
        "output_identity": {"kind": "FIRST_PASS_REPORT",
                            "name": "%s.first-pass-report.json"
                                    % bab.RESERVED_ATTEMPT_IDS[role],
                            "custody_root": custody_root,
                            "report_source": report_source,
                            "custody_dev": custody_dev,
                            "custody_ino": custody_ino},
        "static_gate_evidence": {
            gate: {"status": "PASS", "evidence_sha256": hex64,
                   "evidence_size": 1024, "auditor_role": role,
                   "attempt_id": bab.RESERVED_ATTEMPT_IDS[role]}
            for gate in bab.REQUIRED_STATIC_GATES},
        "dynamic_gates": {
            gate: {"identity": "SYNTHETIC-%s-V1" % gate,
                   "path": "gates/%s.py" % gate.lower(),
                   "sha256": hex64, "bytes": 1,
                   "result_schema": bab.DYNAMIC_GATE_RESULT_SCHEMAS[gate],
                   "timeout_seconds": 30, "max_result_bytes": 65536}
            for gate in bab.DYNAMIC_GATE_ORDER},
        "auditor_invocation": [
            "SYNTHETIC-INERT-CLIENT-V1", "--model",
            bab.AUDITOR_SELECTIONS[role]["model"], "--effort", "high",
            "--report", report_source],
        "output_validator": {"identity": "SYNTHETIC-VALIDATOR-V1",
                             "path": "validator/validator.py",
                             "sha256": hex64, "bytes": 1,
                             "result_schema": bab.VALIDATOR_RESULT_SCHEMA,
                             "timeout_seconds": 30,
                             "max_result_bytes": 65536},
        "execution_limits": {"auditor_timeout_seconds": wall_timeout,
                             "validator_timeout_seconds": 30,
                             "max_report_bytes": 1048576},
    }
    if event_files is not None:
        rows = {row["path"]: row for row in event_files}
        for key, rel in (("boundary_launcher", "boundary/launcher.bin"),
                         ("tool_wrapper", "tools/wrapper.bin"),
                         ("output_validator", "validator/validator.py")):
            doc[key]["sha256"] = rows[rel]["sha256"]
            doc[key]["bytes"] = rows[rel]["bytes"]
        for gate in bab.DYNAMIC_GATE_ORDER:
            row = rows["gates/%s.py" % gate.lower()]
            doc["dynamic_gates"][gate]["sha256"] = row["sha256"]
            doc["dynamic_gates"][gate]["bytes"] = row["bytes"]
    return doc


def variant(doc: dict, mutate) -> bytes:
    """Deep-copy a binding doc, apply mutate(copy), return canonical
    bytes of the mutated document."""
    import copy
    mutated = copy.deepcopy(doc)
    mutate(mutated)
    return canonical(mutated)


@pytest.fixture
def world_a(tmp_path):
    return build_world(tmp_path, "AUDITOR_A")


@pytest.fixture
def world_b(tmp_path):
    return build_world(tmp_path, "AUDITOR_B")
