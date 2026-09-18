"""C-3 / G-2 — Auditor-B Codex application write policy (generic).

Accepted design (AUCDEV-023 G-2 closure record):

* primary workspace role = auditor-output (exactly ONE persistent
  model-write root);
* CLI shape: ``codex exec -C <auditor-output> ...`` with NO ``--add-dir``
  and NO CLI ``-s``/``--sandbox workspace-write``;
* the write capability comes from the NAMED RESTRICTED PERMISSION PROFILE
  in the generated disposable CODEX_HOME ``config.toml``
  (``default_permissions`` selecting a ``[permissions.<name>]`` profile
  with ``workspace_roots`` = the auditor-output role, a ``filesystem``
  map whose only ``write`` entry is that role, enumerated read surfaces
  only, ``network.enabled = false``, and a ``[projects.<role>]`` trust
  key);
* NO root-wide read entry (``/`` absent from the filesystem map);
* evidence readable only where explicitly required; target/source
  read-only or absent per the outer boundary;
* CODEX_HOME/auth unavailable to model-generated commands (auth is never
  a permission entry — credential delivery is the custody mechanism's
  child-side concern, never a model-command-readable config surface);
* the cosmetic CLI banner (``sandbox: workspace-write``) is NOT
  authoritative proof — the effective managed permission profile is.
  Without spending a provider call, the harness proves the GENERATED
  PROFILE CONTENT (static semantic validation here + GATE-W) and the
  OUTER boundary semantics; Codex-internal Landlock enforcement itself is
  a documented residual verified only by a future authorized campaign.

All demonstrated identity/profile values are DATA supplied by callers
(see fixtures/demonstrated-profile.json); nothing historical is baked in.
"""
from __future__ import annotations

import os
import stat
from dataclasses import dataclass, field

from .util import sha256_bytes, sha256_file

FORBIDDEN_CLI_FLAGS = ("--add-dir", "-s", "--sandbox",
                       "--dangerously-bypass-approvals-and-sandbox",
                       "--full-auto", "--dangerously-bypass-approvals",
                       "--yolo")

# demonstrated restricted-profile system read set (policy-semantic constant
# of the accepted v6 named profile — toolchain/interpreter reads only)
DEMONSTRATED_SYSTEM_READ_PATHS = ("/usr", "/bin", "/lib", "/lib64",
                                  "/sbin", "/etc")


class IdentityDrift(RuntimeError):
    """Codex binary identity does not match the pinned identity."""


class PolicyDrift(RuntimeError):
    """Generated/observed profile drifted from the frozen profile."""


@dataclass
class CodexIdentity:
    """Pinned executable identity (version + SHA-256), supplied as data."""
    version: str
    sha256: str
    exe_path: str


@dataclass
class ProfileSpec:
    """Generic restricted-permission profile specification."""
    profile_name: str = "auditor-restricted"
    description: str = "restricted auditor profile"
    model_name: str = "probe"
    workspace_role: str = "/auditor-output"        # inner boundary path
    evidence_read_paths: tuple[str, ...] = ("/evidence",)
    target_read_paths: tuple[str, ...] = ()        # outer policy decides
    system_read_paths: tuple[str, ...] = DEMONSTRATED_SYSTEM_READ_PATHS
    extra_read_paths: tuple[str, ...] = ()
    network_enabled: bool = False


def verify_codex_identity(identity: CodexIdentity,
                          exe_path: str | None = None) -> dict:
    """Exact binary identity check — fails closed on drift."""
    path = exe_path or identity.exe_path
    result = {"exe_path": path, "expected_version": identity.version,
              "expected_sha256": identity.sha256}
    if not os.path.isfile(path):
        raise IdentityDrift(f"CODEX_BINARY_ABSENT: {path}")
    actual = sha256_file(path)
    result["actual_sha256"] = actual
    if actual != identity.sha256:
        raise IdentityDrift(
            f"CODEX_BINARY_IDENTITY_DRIFT: expected {identity.sha256} "
            f"got {actual}")
    st = os.lstat(path)
    result["mode"] = oct(stat.S_IMODE(st.st_mode))
    return result


def render_config_toml(spec: ProfileSpec) -> str:
    """Render the disposable CODEX_HOME config.toml with the named
    restricted permission profile (byte-stable output)."""
    role = spec.workspace_role
    lines = [
        f'model = "{spec.model_name}"',
        f'default_permissions = "{spec.profile_name}"',
        "",
        f"[permissions.{spec.profile_name}]",
        f'description = "{spec.description}"',
        "",
        f"[permissions.{spec.profile_name}.workspace_roots]",
        f'"{role}" = true',
        "",
        f"[permissions.{spec.profile_name}.filesystem]",
        f'"{role}" = "write"',
    ]
    for p in spec.evidence_read_paths:
        lines.append(f'"{p}" = "read"')
    for p in spec.target_read_paths:
        lines.append(f'"{p}" = "read"')
    for p in spec.system_read_paths:
        lines.append(f'"{p}" = "read"')
    for p in spec.extra_read_paths:
        lines.append(f'"{p}" = "read"')
    lines += [
        "",
        f"[permissions.{spec.profile_name}.network]",
        f"enabled = {'true' if spec.network_enabled else 'false'}",
        "",
        f'[projects."{role}"]',
        'trust_level = "trusted"',
        "",
    ]
    return "\n".join(lines)


def generate_codex_home(spec: ProfileSpec, dest_dir: str) -> dict:
    """Generate the disposable CODEX_HOME: config.toml ONLY (plus an empty
    state dir marker).  NO auth material is generated here — synthetic
    inert auth fixtures are custody's concern, never this config."""
    os.makedirs(dest_dir, exist_ok=True)
    config = render_config_toml(spec)
    config_path = os.path.join(dest_dir, "config.toml")
    with open(config_path, "w", encoding="utf-8") as fh:
        fh.write(config)
    os.makedirs(os.path.join(dest_dir, "sessions"), exist_ok=True)
    return {"codex_home": dest_dir, "config_path": config_path,
            "config_sha256": sha256_bytes(config.encode("utf-8")),
            "config_bytes": len(config.encode("utf-8"))}


def parse_profile(config_path: str) -> dict:
    import tomllib
    with open(config_path, "rb") as fh:
        return tomllib.load(fh)


def validate_profile_semantics(config_path: str, spec: ProfileSpec) -> list[str]:
    """Static semantic validation of the generated profile against the
    accepted application-policy intent.  Returns failure list (empty=OK)."""
    failures: list[str] = []
    try:
        doc = parse_profile(config_path)
    except Exception as exc:  # noqa: BLE001 — any parse failure is drift
        return [f"PROFILE_UNPARSEABLE: {exc!r}"]
    name = spec.profile_name
    if doc.get("default_permissions") != name:
        failures.append(f"DEFAULT_PERMISSIONS_NOT_{name}")
    perms = doc.get("permissions", {}).get(name)
    if not isinstance(perms, dict):
        return failures + [f"PROFILE_{name}_ABSENT"]
    roots = perms.get("workspace_roots", {})
    if list(roots.keys()) != [spec.workspace_role]:
        failures.append(
            f"WORKSPACE_ROOTS_NOT_EXACTLY_ONE_ROLE: {sorted(roots)}")
    fs_map = perms.get("filesystem", {})
    write_roots = sorted(k for k, v in fs_map.items() if v == "write")
    if write_roots != [spec.workspace_role]:
        failures.append(f"WRITE_ROOTS_NOT_EXACTLY_ONE_ROLE: {write_roots}")
    if "/" in fs_map:
        failures.append("ROOT_WIDE_READ_ENTRY_PRESENT")
    for p in spec.evidence_read_paths:
        if fs_map.get(p) != "read":
            failures.append(f"EVIDENCE_READ_MISSING:{p}")
    net = perms.get("network", {})
    if net.get("enabled") is not False:
        failures.append("NETWORK_NOT_DISABLED_IN_PROFILE")
    if any("auth" in k.lower() or "codex_home" in k.lower()
           for k in fs_map):
        failures.append("CODEX_HOME_OR_AUTH_ENTRY_IN_PROFILE")
    projects = doc.get("projects", {})
    if spec.workspace_role not in projects:
        failures.append("PROJECT_TRUST_KEY_MISSING")
    return failures


def build_exec_cli(codex_exe: str, workspace: str, *,
                   extra_args: tuple[str, ...] = ("--skip-git-repo-check",)
                   ) -> list[str]:
    """CLI construction with the accepted shape: -C <auditor-output>, NO
    --add-dir, NO CLI -s/--sandbox.  The write capability is the named
    profile's, not a CLI flag's."""
    argv = [codex_exe, "exec", "-C", workspace, *extra_args]
    bad = [a for a in argv if a in FORBIDDEN_CLI_FLAGS]
    if bad:
        raise PolicyDrift(f"FORBIDDEN_CLI_FLAG_PRESENT: {bad}")
    if "--add-dir" in argv:
        raise PolicyDrift("FORBIDDEN_CLI_FLAG_PRESENT: --add-dir")
    return argv


def freeze_profile(artifact: dict, identity: CodexIdentity) -> dict:
    """Freeze the exact generated profile + binary identity for the
    attempt (recorded into the grant binding)."""
    return {
        "config_sha256": artifact["config_sha256"],
        "identity_version": identity.version,
        "identity_sha256": identity.sha256,
        "identity_exe_path": identity.exe_path,
    }


def verify_frozen_profile(frozen: dict, artifact: dict,
                          identity: CodexIdentity,
                          exe_path: str | None = None) -> None:
    """Re-verify the frozen profile/binary right before launch.  Raises
    PolicyDrift / IdentityDrift fail-closed."""
    verify_codex_identity(identity, exe_path)
    if artifact["config_sha256"] != frozen["config_sha256"]:
        raise PolicyDrift(
            f"PROFILE_CONFIG_DRIFT: frozen {frozen['config_sha256']} "
            f"actual {artifact['config_sha256']}")
