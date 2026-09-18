"""Provider credential-custody adapters — synthetic-only adversarial
tests (§14/§15/§21).  No real credential is ever read or contacted."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

import pytest

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns

from qh.adapters import (CLAUDE_FIRSTPARTY_OAUTH, CODEX_CHATGPT_OAUTH,
                         SYNTHETIC_INERT, get_adapter)
from qh.compose import CompositionEnv

UNIQUE_CRED_CODEX = ("SYNTHETIC-CODEX-OAUTH-CREDENTIAL-probe-"
                     "7f3a9c1d5e2b8a64")
UNIQUE_CRED_CLAUDE = ("SYNTHETIC-CLAUDE-CREDENTIALS-JSON-probe-"
                      "1d2c3b4a5f6e7d8c")


def _scan_tree(base, needle: str) -> list[str]:
    hits = []
    for path, _dirs, files in os.walk(base):
        for name in files:
            p = os.path.join(path, name)
            try:
                if os.path.getsize(p) > (4 << 20):
                    continue
                with open(p, "rb") as fh:
                    if needle.encode() in fh.read():
                        hits.append(p)
            except OSError:
                pass
    return hits


def _run_adapter_attempt(env, attempt, role, credential):
    env.author_spec(attempt, role=role)
    root = env.spawn_root(custody_value=credential)
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    resp = env.controller_request(attempt, own_session_slug="s")
    env.root_outcome(root, timeout=300)
    return resp


@requires_bwrap
@requires_userns
def test_codex_chatgpt_oauth_adapter_synthetic_flow(env):
    """Codex ChatGPT-OAuth: auth.json materializes ONLY inside the
    boundary-private CODEX_HOME with mode 0600; the child receives the
    synthetic bytes through the trusted adapter; the model-command view
    has no profile read entry for them."""
    resp = _run_adapter_attempt(env, "ad-codex-0001", "codex",
                                UNIQUE_CRED_CODEX)
    assert resp.get("ok"), resp
    launch = resp["launch"]
    assert launch["adapter_id"] == CODEX_CHATGPT_OAUTH.adapter_id
    assert launch["adapter_target"] == \
        CODEX_CHATGPT_OAUTH.credential_target
    assert launch["adapter_target"].endswith("/auth.json")
    assert "/run-qh/codex-home" in launch["adapter_target"]
    assert launch["custody_length"] == len(UNIQUE_CRED_CODEX)
    assert launch["custody_mode"] == "0o600"
    assert launch["custody_file_present"] is True
    assert launch.get("profile_grants_credential_read") is False
    assert launch.get("provider_runtime_read_len") == len(UNIQUE_CRED_CODEX)
    assert launch.get("evidence_len", 0) > 0
    assert (env.auditor_output / "launch-sim-marker.txt").is_file()


@requires_bwrap
@requires_userns
def test_claude_firstparty_oauth_adapter_synthetic_flow(env):
    """Claude first-party OAuth: .credentials.json materializes ONLY
    inside the boundary-private CLAUDE_CONFIG_DIR with mode 0600."""
    resp = _run_adapter_attempt(env, "ad-claude-0001", "claude",
                                UNIQUE_CRED_CLAUDE)
    assert resp.get("ok"), resp
    launch = resp["launch"]
    assert launch["adapter_id"] == CLAUDE_FIRSTPARTY_OAUTH.adapter_id
    assert launch["adapter_target"] == \
        CLAUDE_FIRSTPARTY_OAUTH.credential_target
    assert launch["adapter_target"].endswith("/.credentials.json")
    assert launch["custody_length"] == len(UNIQUE_CRED_CLAUDE)
    assert launch["custody_mode"] == "0o600"
    assert launch.get("custody_file_present") is True
    assert launch.get("claude_config_dir_files") == [".credentials.json"]


@requires_bwrap
@requires_userns
def test_no_host_ordinary_file_plaintext_after_flow(env):
    """§21: after a full flow, the synthetic credential value appears in
    ZERO ordinary files (host plaintext = none; secret-scan)."""
    resp = _run_adapter_attempt(env, "ad-plain-0001", "codex",
                                UNIQUE_CRED_CODEX)
    assert resp.get("ok"), resp
    assert _scan_tree(env.base, UNIQUE_CRED_CODEX) == []
    # the operator-state ledger/specs/request files never carry it either
    assert _scan_tree(str(env.operator_state), UNIQUE_CRED_CODEX) == []


@requires_bwrap
@requires_userns
def test_controller_never_receives_credential_value(env):
    """§15: the controller request file, response payload, ledger records
    and controller-visible config tree contain no credential material."""
    env.author_spec("ad-ctrl-0001")
    root = env.spawn_root(custody_value=UNIQUE_CRED_CODEX)
    mint = env.root_mint("ad-ctrl-0001")
    assert mint.get("ok")
    resp = env.controller_request("ad-ctrl-0001", own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert resp.get("ok"), resp
    assert UNIQUE_CRED_CODEX not in json.dumps(resp)
    assert _scan_tree(str(env.config_dir), UNIQUE_CRED_CODEX) == []
    ledger_text = json.dumps(env.ledger_records())
    assert UNIQUE_CRED_CODEX not in ledger_text
    for rec in env.ledger_records():
        assert rec.get("length") in (None, len(UNIQUE_CRED_CODEX)) or \
            not isinstance(rec.get("length"), int)


@requires_bwrap
@requires_userns
def test_controller_env_has_no_provider_credential(env):
    """§15: a process launched with the controller's environment shape
    carries no provider credential value."""
    env.author_spec("ad-env-0001")
    controller_env = {**os.environ,
                      "CLAUDE_CONFIG_DIR": str(env.config_dir),
                      "PYTHONPATH": str(HARNESS_ROOT)}
    probe = subprocess.run(
        [sys.executable, "-c",
         "import json,os;print(json.dumps(dict(os.environ)))"],
        capture_output=True, text=True, env=controller_env, timeout=30)
    assert UNIQUE_CRED_CODEX not in probe.stdout
    assert UNIQUE_CRED_CODEX not in probe.stderr
    for key, value in controller_env.items():
        assert UNIQUE_CRED_CODEX not in value


@requires_bwrap
@requires_userns
def test_controller_cannot_read_root_custody_memfd(env):
    """§15: the authority root's custody memfd is unreachable through
    same-UID /proc inspection (non-dumpable process)."""
    env.author_spec("ad-proc-0001")
    root = env.spawn_root(custody_value=UNIQUE_CRED_CODEX)
    try:
        # same-UID non-parent: /proc/<pid>/fd listing must be denied
        try:
            fds = os.listdir(f"/proc/{root.pid}/fd")
        except OSError:
            fds = []
        assert not fds, "root fd list must not be same-UID readable"
        # direct open attempts on plausible fd numbers must fail
        read_ok = False
        for n in (0, 1, 2, 3, 4, 5):
            try:
                with open(f"/proc/{root.pid}/fd/{n}", "rb") as fh:
                    if UNIQUE_CRED_CODEX.encode() in fh.read(4096):
                        read_ok = True
            except OSError:
                pass
        assert not read_ok, "custody bytes must not be /proc-readable"
    finally:
        env.cleanup_procs()


@requires_bwrap
@requires_userns
def test_ephemeral_material_removed_with_namespace(env):
    """§21: cleanup removes ephemeral material — no auth.json /
    .credentials.json exists anywhere on the host after teardown."""
    resp = _run_adapter_attempt(env, "ad-teardown-0001", "codex",
                                UNIQUE_CRED_CODEX)
    assert resp.get("ok"), resp
    leftovers = []
    for path, _dirs, files in os.walk(env.base):
        for name in files:
            if name in ("auth.json", ".credentials.json"):
                leftovers.append(os.path.join(path, name))
    assert leftovers == []


@requires_bwrap
@requires_userns
def test_adapter_identity_bound_in_trusted_spec(env):
    """§21: the adapter id/provider_role/version are bound in the
    trusted launch spec and recorded at the adapter gate."""
    spec = env.author_spec("ad-bind-0001", role="claude")
    a = get_adapter(spec["credential_adapter"]["id"])
    assert a is CLAUDE_FIRSTPARTY_OAUTH
    assert spec["credential_adapter"]["provider_role"] == \
        a.provider_role
    assert spec["credential_adapter"]["version"] == a.version
    resp = _run_adapter_attempt.__wrapped__ if False else None
    root = env.spawn_root(custody_value=UNIQUE_CRED_CLAUDE)
    mint = env.root_mint("ad-bind-0001")
    assert mint.get("ok")
    resp = env.controller_request("ad-bind-0001", own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert resp.get("ok"), resp
    events = [r for r in env.ledger_records()
              if r.get("event") == "CREDENTIAL_ADAPTER_BOUND"]
    assert events and events[-1]["adapter_id"] == a.adapter_id


@requires_bwrap
@requires_userns
def test_fake_root_cannot_materialize_legitimate_bytes(env):
    """§15: a controller-created fake root never causes the legitimate
    credential bytes to materialize anywhere outside the trusted bound
    launch."""
    legit = UNIQUE_CRED_CODEX
    env.author_spec("ad-legit-0001")
    root = env.spawn_root(custody_value=legit)
    mint = env.root_mint("ad-legit-0001")
    assert mint.get("ok")
    resp = env.controller_request("ad-legit-0001", own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert resp.get("ok"), resp
    # fake root with controller-owned bytes
    fake = CompositionEnv(str(env.base / "fake-root"))
    fake.author_spec("ad-fake-0001")
    fake_root = fake.spawn_root(custody_value="CONTROLLER-OWNED")
    fake_mint = fake.root_mint("ad-fake-0001")
    assert fake_mint.get("ok")
    fake_resp = fake.controller_request("ad-fake-0001",
                                        own_session_slug="s")
    fake.root_outcome(fake_root, timeout=300)
    fake.cleanup_procs()
    if fake_resp.get("ok"):
        assert fake_resp["launch"]["custody_length"] == \
            len("CONTROLLER-OWNED")
    # the legitimate value never leaked into the fake workspace
    assert _scan_tree(str(env.base / "fake-root"), legit) == []


def test_registry_shape_and_inert_adapter():
    """The registry binds exactly the implemented synthetic adapters; the
    inert rehearsal adapter keeps the accepted GATE-W target."""
    assert SYNTHETIC_INERT.credential_target == \
        "/tmp/qh-custody/inert-credential"
    assert CODEX_CHATGPT_OAUTH.credential_target == \
        "/run-qh/codex-home/auth.json"
    assert CLAUDE_FIRSTPARTY_OAUTH.credential_target == \
        "/run-qh/claude-config/.credentials.json"
    assert CODEX_CHATGPT_OAUTH.credential_mode == 0o600
    assert CLAUDE_FIRSTPARTY_OAUTH.credential_mode == 0o600
    with pytest.raises(Exception):
        get_adapter("unknown_adapter_v0")
