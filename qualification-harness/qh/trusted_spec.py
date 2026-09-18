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

import os
import stat
from pathlib import Path

from .util import canonical_json, content_id, sha256_bytes, sha256_file

SPEC_SCHEMA_VERSION = 1

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
    """Digest over the exact executable harness byte set."""
    root = Path(harness_root)
    entries = {}
    for rel in sorted(HARNESS_EXEC_RELPATHS):
        full = root / rel
        if not full.is_file():
            raise SpecError(f"HARNESS_SNAPSHOT_FILE_MISSING: {rel}")
        entries[rel] = sha256_file(str(full))
    return content_id({"kind": "qh-harness-tree/1", "root": str(root),
                       "files": entries})


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


def build_spec(*, attempt_id: str, attempt_root: str, config_dir: str,
               manifest_id: str, evidence_src: str, auditor_output_src: str,
               target_src: str | None, codex_exe: str, codex_version: str,
               profile: dict, config_sha256: str,
               credential_adapter: dict, harness_root: str,
               payload_kind: str = "launch_sim") -> dict:
    """OPERATOR-side authoring helper: compose the complete trusted launch
    spec with freshly captured source identities.  The caller (operator)
    then pipes the canonical bytes into the authority root."""
    root_id = capture_dir_identity(attempt_root)
    spec = {
        "spec_version": SPEC_SCHEMA_VERSION,
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
            "tree_digest": harness_tree_digest(harness_root)},
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
        spec["sources"]["target"] = capture_dir_identity(target_src)
    validate_spec(spec)
    return spec


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


def validate_spec(spec: dict) -> None:
    """Schema-completeness validation (every §7 security-critical field)."""
    _need(spec, "spec_version", "spec", int)
    if spec["spec_version"] != SPEC_SCHEMA_VERSION:
        raise SpecError(
            f"SPEC_VERSION_UNSUPPORTED: {spec['spec_version']} "
            f"(expected {SPEC_SCHEMA_VERSION})")
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
