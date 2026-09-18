"""Provider credential-custody adapters (IR remediation §14).

Every adapter declares the EXACT child-side materialization layout for one
provider role and is bound into the trusted launch spec by id; the bytes
themselves always travel through the authority-root custody channel (never
a controller-visible surface).

Implemented against SYNTHETIC inert fixtures only; no real credential is
ever read, parsed, inferred or contacted by this harness.

Evidence basis for each concrete adapter (existing non-secret frozen
evidence only):

* ``codex_chatgpt_oauth_v1`` — Campaign-2 harness preflight correction
  (role-B auth/config enters from a minimal staging set census-enforced to
  EXACTLY ``auth.json`` + minimal ``config.toml``; ``CODEX_HOME`` must be
  WRITABLE at init — the read-only CODEX_HOME attempt failed with
  ``B_ATTEMPT1_LOCAL_INIT_FAILURE_READONLY_CODEX_HOME``; final-home shape
  ``CODEX_HOME=/auditor-home/.codex`` composed before the provider process)
  and the accepted AUCDEV-023 G-2 closure (auth.json is the required runtime
  interface and is NEVER a model-command permission-profile entry; only the
  documented arg0-helper READ entry exists).  The adapter therefore
  materializes the custody bytes as ``auth.json`` inside a BOUNDARY-PRIVATE
  CODEX_HOME composed on ephemeral namespace-local storage.
* ``claude_firstparty_oauth_v1`` — Campaign-2 static preflight parity
  closure (``AUDITOR_A_FIRST_PARTY_EXECUTION_ENVIRONMENT_MECHANICALLY_
  ESTABLISHED``: in a fresh dedicated ``CLAUDE_CONFIG_DIR`` the credential
  surface is ``.credentials.json`` ALONE — ``claudeAiOauth`` key shape,
  mode 0600 — with no settings/projects/plugins/skills present) and the
  Campaign-2 preflight correction (dedicated ``CLAUDE_CONFIG_DIR``; operator
  places real auth; credential values never read).  The adapter materializes
  the custody bytes as ``.credentials.json`` mode 0600 inside a
  boundary-private ``CLAUDE_CONFIG_DIR``.

Any provider role whose exact materialization interface is NOT established
by existing non-secret evidence MUST remain unimplemented here (bounded
blocker; no format is invented).
"""
from __future__ import annotations

from dataclasses import dataclass, field

PROVIDER_ADAPTER_INTEGRATION_STATUS = (
    "SYNTHETIC_ONLY — concrete adapters for codex_chatgpt_oauth and "
    "claude_firstparty_oauth are implemented against synthetic inert bytes "
    "from frozen non-secret evidence; no real credential is read, parsed or "
    "contacted; unestablished provider roles remain explicit blockers")

# The single inert rehearsal adapter (GATE-W / gate-only launches keep the
# accepted matrix: custody channel verified at an inert path, provider
# credential file ABSENT from the provider home).
INERT_ADAPTER_ID = "synthetic_inert_v1"


class AdapterError(RuntimeError):
    """Unknown/unsupported credential adapter — fail closed."""


@dataclass(frozen=True)
class ProviderAdapter:
    adapter_id: str
    provider_role: str
    version: int
    credential_target: str            # inner-boundary materialization path
    env: dict = field(default_factory=dict)
    extra_files: tuple = ()           # (kind, inner_path) e.g. config.toml
    credential_mode: int = 0o600      # defense-in-depth restrictive mode

    def child_target_path(self) -> str:
        return self.credential_target


SYNTHETIC_INERT = ProviderAdapter(
    adapter_id=INERT_ADAPTER_ID, provider_role="synthetic_inert",
    version=1, credential_target="/tmp/qh-custody/inert-credential")

CODEX_CHATGPT_OAUTH = ProviderAdapter(
    adapter_id="codex_chatgpt_oauth_v1",
    provider_role="codex_chatgpt_oauth",
    version=1,
    credential_target="/run-qh/codex-home/auth.json",
    env={"CODEX_HOME": "/run-qh/codex-home"},
    extra_files=(("config", "/run-qh/codex-home/config.toml"),),
    credential_mode=0o600)

CLAUDE_FIRSTPARTY_OAUTH = ProviderAdapter(
    adapter_id="claude_firstparty_oauth_v1",
    provider_role="claude_firstparty_oauth",
    version=1,
    credential_target="/run-qh/claude-config/.credentials.json",
    env={"CLAUDE_CONFIG_DIR": "/run-qh/claude-config"},
    extra_files=(),
    credential_mode=0o600)

_REGISTRY = {a.adapter_id: a for a in (
    SYNTHETIC_INERT, CODEX_CHATGPT_OAUTH, CLAUDE_FIRSTPARTY_OAUTH)}

# Provider roles whose exact materialization interface is NOT established by
# existing non-secret evidence: explicit bounded blockers, never invented.
UNESTABLISHED_PROVIDER_ROLES = (
    "no other provider-capable child launch role is established by the "
    "frozen qualification/package/runtime evidence beyond the two above")


def get_adapter(adapter_id: str) -> ProviderAdapter:
    try:
        return _REGISTRY[adapter_id]
    except KeyError:
        raise AdapterError(
            f"CREDENTIAL_ADAPTER_UNKNOWN:{adapter_id} — the trusted launch "
            "spec must bind a registered adapter id") from None
