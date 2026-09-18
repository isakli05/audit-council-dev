"""TRUSTED LAUNCH SPEC — the one canonical versioned security-critical
launch specification (IR-002 remediation).

The spec is established by the legitimate OPERATOR/ROOT authority, NEVER by
the controller:

* the operator authors the complete spec out-of-band and delivers it to the
  authority root through an operator-held PIPE (never a controller request
  field); the root binds the canonical spec id in its non-dumpable process
  memory and hands the exact same bytes to the one-shot supervisor;
* the persisted ``operator-state/specs/<spec_id>.json`` copy is
  OBSERVABILITY ONLY — tampering is detectable by recomputing the canonical
  content address (the id is self-certifying; no authority lives in files);
* every security-critical source is identity-bound at authoring time
  (realpath + dev + ino + content digest) and re-verified at launch:
  delete/recreate substitution (dev/ino change), in-place content swap
  (digest change) and path mismatch are all refused;
* harness code identity is a recursive digest over the exact executable
  byte set (qh modules + in-boundary payload fixtures); at launch the
  supervisor snapshots the VERIFIED bytes into process-bound memfds and the
  boundary materializes them via bwrap --bind-data, so no host-path code is
  ever executed inside the protected launch (immutable-bytes mechanism for
  the same-UID threat model);
* the controller request carries NONE of these values; any claim it does
  carry is compared against this spec and a mismatch is terminal.

Minimum security-critical content (remediation §7): spec version; attempt
id; attempt/root identity; bootstrap manifest identity; expected
controller-scope binding inputs; trusted harness implementation identity;
trusted boundary-child identity; evidence source identity; target/source
identity; auditor-output role/identity; exact Codex executable identity and
expected SHA-256; expected Codex version/profile identity; exact generated
config digest; allowed mount/read/write roles; credential-custody adapter
identity/version; provider role; required no-egress policy; exact
payload/launch role.
"""
from __future__ import annotations

import json
import os
import stat
from pathlib import Path

from .util import canonical_json, content_id, sha256_bytes, sha256_file

SPEC_SCHEMA_VERSION = 3
TEMPLATE_SCHEMA_VERSION = 1

# The exact byte set whose bytes may execute inside the boundary.  Anything
# else under qualification-harness/ is data/tests/docs and is deliberately
# NOT part of the executable identity.
HARNESS_EXEC_RELPATHS = (
    "qh/__init__.py", "qh/__main__.py", "qh/util.py", "qh/ledger.py",
    "qh/statemachine.py", "qh/bootstrap.py", "qh/campaign.py",
    "qh/custody.py", "qh/noegress.py", "qh/boundary.py",
    "qh/boundary_child.py", "qh/codex_profile.py", "qh/gatew.py",
    "qh/authority.py", "qh/compose.py", "qh/cli.py", "qh/trusted_spec.py",
    "qh/rootauth.py", "qh/adapters.py",
    "fixtures/gatew_payload.py", "fixtures/launch_sim_payload.py",
)

SENSITIVE_NAME_MARKERS = ("credential", "token", "secret", "auth.json")
MAX_TREE_ENTRIES = 8192
MAX_TREE_DEPTH = 10


class SpecError(RuntimeError):
    """Fail-closed trusted-spec validation/verification failure."""


# ------------------------------------------------------------- authoring --

def _is_sensitive(relpath: str) -> bool:
    name = relpath.rsplit("/", 1)[-1].lower()
    return any(m in name for m in SENSITIVE_NAME_MARKERS)


def dir_tree_digest(path: str, *, max_entries: int = MAX_TREE_ENTRIES,
                    max_depth: int = MAX_TREE_DEPTH) -> str:
    """Deterministic recursive content digest over a directory.
    Sensitive-named files are recorded by metadata ONLY (size/mode) — no
    credential value is ever hashed into a spec (G-1 invariant)."""
    base = Path(path)
    entries: dict[str, dict] = {}
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames.sort()
        rel_dir = os.path.relpath(dirpath, path)
        depth = 0 if rel_dir == "." else rel_dir.count(os.sep) + 1
        if depth >= max_depth:
            dirnames[:] = []
        for name in sorted(dirnames) + sorted(filenames):
            rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            full = os.path.join(dirpath, name)
            st = os.lstat(full)
            if stat.S_ISDIR(st.st_mode):
                entries[rel] = {"type": "dir"}
            elif stat.S_ISLNK(st.st_mode):
                entries[rel] = {"type": "symlink",
                                "target": os.readlink(full)}
            elif stat.S_ISREG(st.st_mode):
                ent = {"type": "file", "size": st.st_size,
                       "mode": stat.S_IMODE(st.st_mode)}
                if _is_sensitive(rel):
                    ent["sha256"] = None
                    ent["sensitive"] = True
                else:
                    ent["sha256"] = sha256_file(full)
                entries[rel] = ent
            else:
                entries[rel] = {"type": "special"}
            if len(entries) > max_entries:
                raise SpecError(f"TREE_TOO_LARGE: {path}")
    # NOTE: the digest input is path-INDEPENDENT (entries only) so the
    # same digest can be recomputed INSIDE the boundary at the mounted
    # inner path and compared against the spec-bound value.
    return content_id({"kind": "qh-dir-tree/1", "entries": entries})


def capture_dir_identity(path: str) -> dict:
    real = os.path.realpath(path)
    st = os.lstat(real)
    return {"path": real, "dev": st.st_dev, "ino": st.st_ino,
            "tree_digest": dir_tree_digest(real)}


def capture_file_identity(path: str) -> dict:
    real = os.path.realpath(path)
    st = os.lstat(real)
    return {"path": real, "dev": st.st_dev, "ino": st.st_ino,
            "sha256": sha256_file(real)}


def harness_tree_digest(harness_root: str) -> str:
    """Digest over the exact executable harness byte set.

    PATH-INDEPENDENT (entries only, ``qh-harness-tree/2``): the operator
    may compute the expected identity from ANY trusted pristine copy of
    the same source (or from Git object bytes) and it binds CONTENT only;
    the root PATH is pinned separately (spec.harness.root + the bootstrap
    module-provenance checks).  This is what makes a pre-authorized,
    independently established expected identity possible at all."""
    root = Path(harness_root)
    entries = {}
    for rel in sorted(HARNESS_EXEC_RELPATHS):
        full = root / rel
        if not full.is_file():
            raise SpecError(f"HARNESS_SNAPSHOT_FILE_MISSING: {rel}")
        entries[rel] = sha256_file(str(full))
    return content_id({"kind": "qh-harness-tree/2", "files": entries})


def harness_digest_from_files(harness_root: str,
                              files: dict[str, bytes]) -> str:
    """The SAME harness-tree digest computed over an IN-MEMORY byte set
    (relpath -> bytes) instead of host reads.  The authority root uses
    this at privileged-bootstrap freeze time to compare the frozen byte
    set to the operator-provided expected identity; the forked supervisor
    uses it to re-verify the frozen representation without touching the
    host tree."""
    missing = [rel for rel in HARNESS_EXEC_RELPATHS if rel not in files]
    if missing:
        raise SpecError(f"HARNESS_BUNDLE_INCOMPLETE: {','.join(missing)}")
    entries = {rel: sha256_bytes(files[rel])
               for rel in sorted(HARNESS_EXEC_RELPATHS)}
    return content_id({"kind": "qh-harness-tree/2", "files": entries})


def harness_snapshot_files(harness_root: str) -> list[tuple[str, str]]:
    """[(relpath, abspath)] of the exact executable byte set (sorted)."""
    root = Path(harness_root).resolve()
    out = []
    for rel in sorted(HARNESS_EXEC_RELPATHS):
        full = root / rel
        if not full.is_file():
            raise SpecError(f"HARNESS_SNAPSHOT_FILE_MISSING: {rel}")
        out.append((rel, str(full)))
    return out


def build_pre_controller_template(*, attempt_id: str, attempt_root: str,
                                  config_dir: str, manifest_id: str,
                                  evidence_src: str,
                                  auditor_output_src: str,
                                  target_src: str | None, codex_exe: str,
                                  codex_version: str, profile: dict,
                                  config_sha256: str,
                                  credential_adapter: dict,
                                  harness_root: str,
                                  expected_harness_tree_digest: str,
                                  harness_provenance: dict | None = None,
                                  payload_kind: str = "launch_sim") -> dict:
    """OPERATOR-side authoring of the PRE-CONTROLLER LAUNCH TEMPLATE (the
    two-stage trusted data model, remediation §8): every security-critical
    value that does NOT require the controller PID, authored and frozen
    while the untrusted controller does NOT yet exist.

    CR-HARDEN-001: ``expected_harness_tree_digest`` is the OPERATOR-
    SELECTED privileged harness identity — a value the operator establishes
    INDEPENDENTLY (trusted pristine copy / Git object bytes of the
    operator-selected harness commit or tree).  It is REQUIRED and is used
    VERBATIM: this helper NEVER recomputes a digest from the live ordinary
    tree (a later controller-writable tree can never define its own
    expected identity).  A future operator-selected harness commit/tree is
    supported by supplying its digest here.

    ``harness_provenance`` (optional) records the source-identity tuple
    (e.g. repository full name, exact source commit, qualification-harness
    Git tree SHA) as mechanically bound provenance EVIDENCE alongside the
    content digest that governs the trust decision."""
    if not expected_harness_tree_digest:
        raise SpecError(
            "TEMPLATE_EXPECTED_IDENTITY_REQUIRED: the operator must supply "
            "the pre-authorized harness tree digest (self-pinning from the "
            "live tree is not permitted)")
    root_id = capture_dir_identity(attempt_root)
    template = {
        "template_version": TEMPLATE_SCHEMA_VERSION,
        "attempt_id": attempt_id,
        "attempt_root": {"path": root_id["path"], "dev": root_id["dev"],
                         "ino": root_id["ino"]},
        "bootstrap_manifest": {
            "manifest_id": manifest_id,
            "config_dir": os.path.realpath(config_dir)},
        "controller_scope": {
            "env": {"CLAUDE_CONFIG_DIR": os.path.realpath(config_dir)}},
        "harness": {
            "root": str(Path(harness_root).resolve()),
            "tree_digest": str(expected_harness_tree_digest)},
        "boundary_child": {"relpath": "qh/boundary_child.py"},
        "sources": {
            "evidence": capture_dir_identity(evidence_src),
            "auditor_output": capture_dir_identity(auditor_output_src),
        },
        "codex": {
            "exe": capture_file_identity(codex_exe),
            "version": codex_version,
            "profile": profile,
            "config_sha256": config_sha256,
        },
        "credential_adapter": dict(credential_adapter),
        "noegress": {"required": True},
        "mount_roles": {
            "harness": "ro-immutable-snapshot",
            "evidence": "ro", "auditor_output": "rw",
            "target": "ro" if target_src else "absent",
            "codex_home": "boundary-private",
        },
        "payload": {"kind": payload_kind},
    }
    if target_src:
        template["sources"]["target"] = capture_dir_identity(target_src)
    if harness_provenance is not None:
        template["harness"]["provenance"] = dict(harness_provenance)
    validate_template(template)
    return template


def canonical_template_bytes(template: dict) -> bytes:
    return canonical_json(template)


def template_id(template: dict) -> str:
    """Self-certifying content address of the pre-controller template."""
    return sha256_bytes(canonical_template_bytes(template))


def parse_template_bytes(data: bytes) -> dict:
    doc = parse_spec_bytes(data)
    if doc.get("template_version") != TEMPLATE_SCHEMA_VERSION:
        raise SpecError(
            f"TEMPLATE_VERSION_UNSUPPORTED: {doc.get('template_version')!r} "
            f"(expected {TEMPLATE_SCHEMA_VERSION})")
    if "authorized_controller" in doc:
        raise SpecError(
            "TEMPLATE_MUST_NOT_CARRY_CONTROLLER_IDENTITY: the pre-"
            "controller template is authored before the controller exists")
    return doc


# --------------------------------------------- controller-binding finalization --

def finalize_spec(template: dict, *, controller_uid: int,
                  controller_pid: int,
                  controller_starttime: str) -> dict:
    """PHASE B finalization: compose the FINAL trusted launch spec from
    the frozen pre-controller template by adding ONLY the controller-
    dependent identity (remediation §10).  The privileged harness identity
    is COPIED VERBATIM from the template — never recomputed from the live
    ordinary tree (CR-HARDEN-001 §7: no live-tree self-pinning remains on
    the finalization path)."""
    validate_template(template)
    spec = json.loads(canonical_template_bytes(template))  # private copy
    spec.pop("template_version", None)
    spec["spec_version"] = SPEC_SCHEMA_VERSION
    spec["pre_controller_template"] = {"template_id":
                                       template_id(template)}
    spec["authorized_controller"] = {
        "uid": int(controller_uid),
        "pid": int(controller_pid),
        "starttime": str(controller_starttime)}
    validate_spec(spec)
    return spec


def finalized_spec_id(template: dict, *, controller_uid: int,
                      controller_pid: int,
                      controller_starttime: str) -> str:
    return spec_id(finalize_spec(
        template, controller_uid=controller_uid,
        controller_pid=controller_pid,
        controller_starttime=controller_starttime))


def build_spec(*, attempt_id: str, attempt_root: str, config_dir: str,
               manifest_id: str, evidence_src: str, auditor_output_src: str,
               target_src: str | None, codex_exe: str, codex_version: str,
               profile: dict, config_sha256: str,
               credential_adapter: dict, harness_root: str,
               expected_harness_tree_digest: str,
               controller_pid: int, controller_starttime: str,
               controller_uid: int | None = None,
               harness_provenance: dict | None = None,
               payload_kind: str = "launch_sim") -> dict:
    """OPERATOR-side authoring helper for the COMPLETE final spec
    (template + controller finalization in one step, for environments
    where the controller identity is already known).

    CR-HARDEN-001: ``expected_harness_tree_digest`` is REQUIRED and used
    verbatim — this helper performs NO live-tree digest computation
    anywhere; the operator establishes the expected value independently
    (trusted pristine copy / Git object bytes) in the pre-controller
    trusted phase, and the authority re-verifies the live tree against the
    supplied value at Phase A before any controller exists."""
    template = build_pre_controller_template(
        attempt_id=attempt_id, attempt_root=attempt_root,
        config_dir=config_dir, manifest_id=manifest_id,
        evidence_src=evidence_src, auditor_output_src=auditor_output_src,
        target_src=target_src, codex_exe=codex_exe,
        codex_version=codex_version, profile=profile,
        config_sha256=config_sha256, credential_adapter=credential_adapter,
        harness_root=harness_root,
        expected_harness_tree_digest=expected_harness_tree_digest,
        harness_provenance=harness_provenance,
        payload_kind=payload_kind)
    return finalize_spec(
        template,
        controller_uid=(os.getuid() if controller_uid is None
                        else controller_uid),
        controller_pid=controller_pid,
        controller_starttime=controller_starttime)


# ---------------------------------------------------------- canonical form --

def canonical_spec_bytes(spec: dict) -> bytes:
    return canonical_json(spec)


def spec_id(spec: dict) -> str:
    return sha256_bytes(canonical_spec_bytes(spec))


def parse_spec_bytes(data: bytes) -> dict:
    import json
    try:
        doc = json.loads(data.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SpecError(f"SPEC_UNPARSEABLE: {exc!r}") from exc
    if not isinstance(doc, dict):
        raise SpecError("SPEC_NOT_AN_OBJECT")
    return doc


# ------------------------------------------------------------ validation --

def _need(d: dict, key: str, where: str, typ=None) -> None:
    if key not in d or d[key] is None:
        raise SpecError(f"SPEC_FIELD_MISSING: {where}.{key}")
    if typ is not None and not isinstance(d[key], typ):
        raise SpecError(f"SPEC_FIELD_TYPE_INVALID: {where}.{key}")


def validate_template(template: dict) -> None:
    """Schema-completeness validation of the PRE-CONTROLLER LAUNCH
    TEMPLATE (every security-critical field that does not require the
    controller PID, remediation §8).  The template must NOT carry any
    controller identity."""
    _need(template, "template_version", "template", int)
    if template["template_version"] != TEMPLATE_SCHEMA_VERSION:
        raise SpecError(
            f"TEMPLATE_VERSION_UNSUPPORTED: {template['template_version']} "
            f"(expected {TEMPLATE_SCHEMA_VERSION})")
    if "authorized_controller" in template or \
            "pre_controller_template" in template:
        raise SpecError(
            "TEMPLATE_MUST_NOT_CARRY_CONTROLLER_IDENTITY")
    _need(template, "attempt_id", "template", str)
    _need(template, "attempt_root", "template", dict)
    _need(template["attempt_root"], "path", "template.attempt_root", str)
    _need(template["attempt_root"], "dev", "template.attempt_root", int)
    _need(template["attempt_root"], "ino", "template.attempt_root", int)
    _need(template, "bootstrap_manifest", "template", dict)
    _need(template["bootstrap_manifest"], "manifest_id",
          "template.bootstrap_manifest")
    _need(template["bootstrap_manifest"], "config_dir",
          "template.bootstrap_manifest", str)
    _need(template, "controller_scope", "template", dict)
    _need(template["controller_scope"], "env", "template.controller_scope",
          dict)
    _need(template["controller_scope"]["env"], "CLAUDE_CONFIG_DIR",
          "template.controller_scope.env", str)
    _need(template, "harness", "template", dict)
    _need(template["harness"], "root", "template.harness", str)
    _need(template["harness"], "tree_digest", "template.harness", str)
    if len(template["harness"]["tree_digest"]) != 64 or \
            not all(c in "0123456789abcdef"
                    for c in template["harness"]["tree_digest"]):
        raise SpecError(
            "TEMPLATE_EXPECTED_IDENTITY_INVALID: harness.tree_digest must "
            "be a 64-hex-char sha256 (the operator-selected pre-"
            "controller identity)")
    if "provenance" in template["harness"]:
        prov = template["harness"]["provenance"]
        if not isinstance(prov, dict) or not all(
                isinstance(v, str) for v in prov.values()):
            raise SpecError("TEMPLATE_PROVENANCE_INVALID")
    _need(template, "boundary_child", "template", dict)
    _need(template["boundary_child"], "relpath", "template.boundary_child",
          str)
    _need(template, "sources", "template", dict)
    for src in ("evidence", "auditor_output"):
        _need(template["sources"], src, f"template.sources.{src}", dict)
        for f in ("path", "dev", "ino", "tree_digest"):
            _need(template["sources"][src], f,
                  f"template.sources.{src}",
                  (int if f in ("dev", "ino") else str))
    if template["sources"].get("target") is not None:
        for f in ("path", "dev", "ino", "tree_digest"):
            _need(template["sources"]["target"], f,
                  "template.sources.target",
                  (int if f in ("dev", "ino") else str))
    _need(template, "codex", "template", dict)
    _need(template["codex"], "exe", "template.codex", dict)
    for f in ("path", "sha256"):
        _need(template["codex"]["exe"], f, "template.codex.exe", str)
    _need(template["codex"], "version", "template.codex", str)
    _need(template["codex"], "profile", "template.codex", dict)
    _need(template["codex"], "config_sha256", "template.codex", str)
    _need(template, "credential_adapter", "template", dict)
    _need(template["credential_adapter"], "id",
          "template.credential_adapter", str)
    _need(template["credential_adapter"], "provider_role",
          "template.credential_adapter", str)
    _need(template["credential_adapter"], "version",
          "template.credential_adapter", int)
    _need(template, "noegress", "template", dict)
    _need(template["noegress"], "required", "template.noegress", bool)
    if not template["noegress"]["required"]:
        raise SpecError("TEMPLATE_NOEGRESS_MUST_BE_REQUIRED")
    _need(template, "mount_roles", "template", dict)
    _need(template, "payload", "template", dict)
    _need(template["payload"], "kind", "template.payload", str)
    if template["mount_roles"].get("auditor_output") != "rw":
        raise SpecError("TEMPLATE_AUDITOR_OUTPUT_MUST_BE_RW")
    if template["mount_roles"].get("evidence") != "ro":
        raise SpecError("TEMPLATE_EVIDENCE_MUST_BE_RO")


def validate_spec(spec: dict) -> None:
    """Schema-completeness validation (every §7 security-critical field).
    Schema v3 = v2 + the REQUIRED pre-controller template identity (the
    final spec mechanically preserves the frozen pre-controller template,
    CR-HARDEN-001 §10)."""
    _need(spec, "spec_version", "spec", int)
    if spec["spec_version"] != SPEC_SCHEMA_VERSION:
        raise SpecError(
            f"SPEC_VERSION_UNSUPPORTED: {spec['spec_version']} "
            f"(expected {SPEC_SCHEMA_VERSION})")
    _need(spec, "pre_controller_template", "spec", dict)
    _need(spec["pre_controller_template"], "template_id",
          "spec.pre_controller_template", str)
    _need(spec, "attempt_id", "spec", str)
    _need(spec, "attempt_root", "spec", dict)
    _need(spec["attempt_root"], "path", "spec.attempt_root", str)
    _need(spec["attempt_root"], "dev", "spec.attempt_root", int)
    _need(spec["attempt_root"], "ino", "spec.attempt_root", int)
    _need(spec, "bootstrap_manifest", "spec", dict)
    _need(spec["bootstrap_manifest"], "manifest_id", "spec.bootstrap_manifest")
    _need(spec["bootstrap_manifest"], "config_dir",
          "spec.bootstrap_manifest", str)
    _need(spec, "controller_scope", "spec", dict)
    _need(spec["controller_scope"], "env", "spec.controller_scope", dict)
    _need(spec["controller_scope"]["env"], "CLAUDE_CONFIG_DIR",
          "spec.controller_scope.env", str)
    # CR-REMED-004: the operator-authored authorized controller identity
    # (uid + pid + /proc starttime) is a REQUIRED spec field — the first
    # compatible same-UID peer can never define itself as the controller.
    _need(spec, "authorized_controller", "spec", dict)
    _need(spec["authorized_controller"], "uid",
          "spec.authorized_controller", int)
    _need(spec["authorized_controller"], "pid",
          "spec.authorized_controller", int)
    _need(spec["authorized_controller"], "starttime",
          "spec.authorized_controller", str)
    if not spec["authorized_controller"]["starttime"].isdigit():
        raise SpecError(
            "SPEC_FIELD_TYPE_INVALID: spec.authorized_controller.starttime"
            " must be the decimal /proc/<pid>/stat field 22")
    _need(spec, "harness", "spec", dict)
    _need(spec["harness"], "root", "spec.harness", str)
    _need(spec["harness"], "tree_digest", "spec.harness", str)
    _need(spec, "boundary_child", "spec", dict)
    _need(spec["boundary_child"], "relpath", "spec.boundary_child", str)
    _need(spec, "sources", "spec", dict)
    for src in ("evidence", "auditor_output"):
        _need(spec["sources"], src, "spec.sources", dict)
        for f in ("path", "dev", "ino", "tree_digest"):
            _need(spec["sources"][src], f, f"spec.sources.{src}", (
                int if f in ("dev", "ino") else str))
    if spec["sources"].get("target") is not None:
        for f in ("path", "dev", "ino", "tree_digest"):
            _need(spec["sources"]["target"], f, "spec.sources.target",
                  (int if f in ("dev", "ino") else str))
    _need(spec, "codex", "spec", dict)
    _need(spec["codex"], "exe", "spec.codex", dict)
    for f in ("path", "sha256"):
        _need(spec["codex"]["exe"], f, "spec.codex.exe", str)
    _need(spec["codex"], "version", "spec.codex", str)
    _need(spec["codex"], "profile", "spec.codex", dict)
    _need(spec["codex"], "config_sha256", "spec.codex", str)
    _need(spec, "credential_adapter", "spec", dict)
    _need(spec["credential_adapter"], "id", "spec.credential_adapter", str)
    _need(spec["credential_adapter"], "provider_role",
          "spec.credential_adapter", str)
    _need(spec["credential_adapter"], "version",
          "spec.credential_adapter", int)
    _need(spec, "noegress", "spec", dict)
    _need(spec["noegress"], "required", "spec.noegress", bool)
    if not spec["noegress"]["required"]:
        raise SpecError("SPEC_NOEGRESS_MUST_BE_REQUIRED")
    _need(spec, "mount_roles", "spec", dict)
    _need(spec, "payload", "spec", dict)
    _need(spec["payload"], "kind", "spec.payload", str)
    if spec["mount_roles"].get("auditor_output") != "rw":
        raise SpecError("SPEC_AUDITOR_OUTPUT_MUST_BE_RW")
    if spec["mount_roles"].get("evidence") != "ro":
        raise SpecError("SPEC_EVIDENCE_MUST_BE_RO")


# ----------------------------------------------------------- verification --

def _check_dir_identity(spec_id_path: dict, label: str,
                        failures: list[str], *,
                        require_digest: bool = True) -> None:
    path = spec_id_path["path"]
    try:
        real = os.path.realpath(path)
        st = os.lstat(real)
    except OSError:
        failures.append(f"{label}_SOURCE_ABSENT:{path}")
        return
    if real != path:
        failures.append(f"{label}_PATH_MISMATCH:{path}->{real}")
        return
    if (st.st_dev, st.st_ino) != (spec_id_path["dev"], spec_id_path["ino"]):
        # delete/recreate (or any different filesystem object) = substitution
        failures.append(f"{label}_OBJECT_IDENTITY_CHANGED:{path}")
        return
    if not require_digest:
        return  # object identity only (e.g. the attempt root)
    try:
        digest = dir_tree_digest(real)
    except SpecError as exc:
        failures.append(f"{label}_TREE_UNREADABLE:{exc}")
        return
    if digest != spec_id_path["tree_digest"]:
        failures.append(f"{label}_CONTENT_DRIFT:{path}")


def _check_file_identity(spec_file: dict, label: str,
                         failures: list[str]) -> None:
    path = spec_file["path"]
    try:
        real = os.path.realpath(path)
        st = os.lstat(real)
        digest = sha256_file(real)
    except OSError:
        failures.append(f"{label}_ABSENT:{path}")
        return
    if real != path:
        failures.append(f"{label}_PATH_MISMATCH:{path}->{real}")
        return
    if (st.st_dev, st.st_ino) != (spec_file.get("dev"), spec_file.get("ino")):
        if "dev" in spec_file:
            failures.append(f"{label}_OBJECT_IDENTITY_CHANGED:{path}")
            return
    if digest != spec_file["sha256"]:
        failures.append(f"{label}_CONTENT_DRIFT:{path}")


def verify_spec(spec: dict, *, expected_spec_id: str | None = None,
                harness_digest_override: str | None = None) -> list[str]:
    """Launch-time verification of the COMPLETE spec against the live
    filesystem.  Returns a failure list (empty == verified)."""
    failures: list[str] = []
    try:
        validate_spec(spec)
    except SpecError as exc:
        return [str(exc)]
    if expected_spec_id is not None and spec_id(spec) != expected_spec_id:
        failures.append("SPEC_ID_MISMATCH")
        return failures
    _check_dir_identity(spec["attempt_root"], "ATTEMPT_ROOT", failures,
                        require_digest=False)
    _check_dir_identity(spec["sources"]["evidence"], "EVIDENCE", failures)
    _check_dir_identity(spec["sources"]["auditor_output"],
                        "AUDITOR_OUTPUT", failures)
    if spec["sources"].get("target") is not None:
        _check_dir_identity(spec["sources"]["target"], "TARGET", failures)
    _check_file_identity(spec["codex"]["exe"], "CODEX_EXE", failures)
    # harness executable byte set
    hroot = spec["harness"]["root"]
    try:
        digest = (harness_tree_digest(hroot)
                  if harness_digest_override is None
                  else harness_digest_override)
        if digest != spec["harness"]["tree_digest"]:
            failures.append("HARNESS_TREE_DRIFT")
    except SpecError as exc:
        failures.append(f"HARNESS_TREE_UNREADABLE:{exc}")
    # boundary child must be part of the pinned executable byte set
    rel = spec["boundary_child"]["relpath"]
    if rel not in HARNESS_EXEC_RELPATHS:
        failures.append(f"BOUNDARY_CHILD_NOT_IN_PINNED_SET:{rel}")
    return failures
