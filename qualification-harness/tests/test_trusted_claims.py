"""IR-002 — controller claims vs the trusted launch spec (§8/§9/§10/§11/
§19): every mutated controller claim is REFUSED (the claim-only schema
has no authority fields at all), and every post-authorization mutation of
a security-critical source is refused at TRUSTED_SPEC_VERIFY with
mechanical evidence that no attacker-selected bind/code/executable was
used."""
from __future__ import annotations

import json
import shutil

import pytest

from conftest import HARNESS_ROOT, requires_bwrap, requires_userns

from qh.compose import CompositionEnv

# every security-critical field the OLD controller request supplied
REMOVED_AUTHORITY_FIELDS = [
    "harness_root",
    "boundary_child",
    "evidence_src",
    "target_src",
    "auditor_output_src",
    "codex_home",
    "config_path",
    "identity_version",
    "identity_sha256",
    "identity_exe_path",
    "profile_name",
    "model_name",
    "credential_adapter",
    "root",
    "manifest_id",
    "controller_pid",
]


@requires_bwrap
@requires_userns
@pytest.mark.parametrize("field", REMOVED_AUTHORITY_FIELDS)
def test_mutated_controller_claim_refused(env, field):
    """§19: each controller-claim mutation against ONE legitimately
    operator-rooted attempt => TERMINAL refusal (the field no longer
    exists in the request schema; supplying it is a claim violation)."""
    env.author_spec(f"claim-{field}")
    root = env.spawn_root()
    mint = env.root_mint(f"claim-{field}")
    assert mint.get("ok"), mint
    resp = env.controller_request(
        f"claim-{field}", overrides={field: "/tmp/attacker-controlled"},
        own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert not resp.get("ok")
    assert "UNKNOWN_CLAIM_FIELD" in resp.get("reason", "")
    assert field in resp.get("reason", "")
    assert resp["state"] == "TERMINAL_PREEXEC_STOP"


@requires_bwrap
@requires_userns
def test_control_arbitrary_executable_plus_matching_sha_refused(env):
    """Mandatory control: controller supplies arbitrary executable E and
    SHA256(E) => REFUSED (self-asserted identity pins are structurally
    impossible: the request schema carries no executable/hash fields)."""
    exe = env.base / "attacker-executable"
    exe.write_text("#!/bin/sh\necho attacker\n", encoding="utf-8")
    exe.chmod(0o755)
    import hashlib
    sha = hashlib.sha256(exe.read_bytes()).hexdigest()
    env.author_spec("claim-exe-sha")
    root = env.spawn_root()
    mint = env.root_mint("claim-exe-sha")
    assert mint.get("ok")
    resp = env.controller_request(
        "claim-exe-sha",
        overrides={"identity_exe_path": str(exe), "identity_sha256": sha},
        own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert not resp.get("ok")
    assert "UNKNOWN_CLAIM_FIELD" in resp.get("reason", "")
    assert "identity_exe_path" in resp.get("reason", "")


@requires_bwrap
@requires_userns
def test_control_arbitrary_rw_dir_auditor_output_not_bound(env):
    """Mandatory control: an arbitrary host RW directory requested as
    auditor-output is NOT BOUND — the launch (if any) writes only to the
    spec-bound auditor-output."""
    attacker_dir = env.base / "attacker-auditor-output"
    attacker_dir.mkdir()
    result = env.run_attempt(
        "claim-rw", overrides={"auditor_output_src": str(attacker_dir)})
    assert not result["ok"]
    assert "UNKNOWN_CLAIM_FIELD" in \
        result["response"].get("reason", "")
    assert list(attacker_dir.iterdir()) == [], \
        "attacker-selected RW directory must never be bound"


@requires_bwrap
@requires_userns
def test_control_arbitrary_harness_root_not_executed(env):
    """Mandatory control: an arbitrary controller harness_root is NOT
    EXECUTED — claim refused; and the in-boundary /opt/qh tree is the
    verified snapshot (proven by the happy-path gatew/launch payloads
    running from the spec-pinned bytes)."""
    fake = env.base / "attacker-harness"
    (fake / "qh").mkdir(parents=True)
    (fake / "qh" / "boundary_child.py").write_text(
        "#!/usr/bin/env python3\nimport os\nos._exit(66)\n",
        encoding="utf-8")
    result = env.run_attempt(
        "claim-hroot", overrides={"harness_root": str(fake)})
    assert not result["ok"]
    assert "UNKNOWN_CLAIM_FIELD" in \
        result["response"].get("reason", "")


def _drive_after_mutation(env, attempt, mutate, *, pre_author=None):
    """(pre_author or author default) -> apply the post-authorization
    mutation -> root up -> mint -> controller request -> outcomes."""
    if pre_author is not None:
        pre_author()
    else:
        env.author_spec(attempt)
    mutate()
    root = env.spawn_root()
    mint = env.root_mint(attempt)
    assert mint.get("ok"), mint
    resp = env.controller_request(attempt, own_session_slug="s")
    env.root_outcome(root, timeout=300)
    return resp


@requires_bwrap
@requires_userns
def test_trusted_executable_changed_after_spec_creation_refused(env):
    """§11: the trusted executable changed after spec creation =>
    REFUSED (TRUSTED_SPEC_VERIFY fails on the spec-bound identity)."""
    from pathlib import Path
    exe = Path(env.codex_bin)

    def mutate():
        exe.write_text("#!/bin/sh\necho tampered-exe\n", encoding="utf-8")
        exe.chmod(0o755)
    resp = _drive_after_mutation(env, "drift-exe", mutate)
    assert not resp.get("ok")
    reason = resp.get("reason", "")
    assert "TRUSTED_SPEC_VERIFY_FAIL" in reason
    assert "CODEX_EXE" in reason


@requires_bwrap
@requires_userns
def test_evidence_changed_after_spec_creation_refused(env):
    def mutate():
        (env.evidence / "evidence.md").write_text("swapped\n",
                                                  encoding="utf-8")
    resp = _drive_after_mutation(env, "drift-evidence", mutate)
    assert not resp.get("ok")
    reason = resp.get("reason", "")
    assert "TRUSTED_SPEC_VERIFY_FAIL" in reason
    assert "EVIDENCE" in reason


@requires_bwrap
@requires_userns
def test_harness_code_changed_after_spec_creation_refused(env, tmp_path):
    """Harness code mutated BETWEEN spec authorization and root start is
    caught EARLIER under the hardened bootstrap: the root's privileged-
    bootstrap freeze compares the host tree to the spec-bound identity and
    refuses BEFORE any trigger is exposed (CR-REMED-002 §10 outcome B)."""
    copy = tmp_path / "harness-copy-drift"
    shutil.copytree(str(HARNESS_ROOT), str(copy),
                    ignore=shutil.ignore_patterns(
                        "__pycache__", "test-outputs", "*.pyc"))
    env.author_spec("drift-harness", harness_root=str(copy))
    with open(f"{copy}/qh/boundary_child.py", "a") as fh:
        fh.write("# controller mutation post-authorization\n")
    with pytest.raises(RuntimeError, match="ROOT_STARTUP_FAILED"):
        env.spawn_root()


@requires_bwrap
@requires_userns
def test_config_digest_drift_refused(env):
    """The rendered config must match the spec-bound digest exactly: a
    spec whose bound digest does not match its own profile parameters
    fails closed at profile freeze."""
    env.author_spec("drift-config")
    bad = json.loads(json.dumps(env.template))
    bad["codex"]["config_sha256"] = "0" * 64
    root = env.spawn_root(template=bad)
    mint = env.root_mint("drift-config")
    assert mint.get("ok"), mint
    resp = env.controller_request("drift-config", own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert not resp.get("ok")
    reason = resp.get("reason", "")
    assert "PROFILE" in reason, reason


@requires_bwrap
@requires_userns
def test_wrong_adapter_id_terminal_stop(env):
    """Adapter identity is spec-bound: an unregistered adapter id stops
    terminally at the credential-adapter gate."""
    env.author_spec("adapter-wrong")
    bad = json.loads(json.dumps(env.template))
    bad["credential_adapter"]["id"] = "attacker_adapter_v9"
    root = env.spawn_root(template=bad)
    mint = env.root_mint("adapter-wrong")
    assert mint.get("ok"), mint
    resp = env.controller_request("adapter-wrong", own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert not resp.get("ok")
    assert "CREDENTIAL_ADAPTER_INVALID" in resp.get("reason", "")
    assert resp["state"] == "TERMINAL_PREEXEC_STOP"


@requires_bwrap
@requires_userns
def test_wrong_attempt_claim_refused(env):
    env.author_spec("claim-attempt")
    root = env.spawn_root()
    mint = env.root_mint("claim-attempt")
    assert mint.get("ok")
    resp = env.controller_request(
        "claim-attempt", overrides={"attempt_id": "other-attempt"},
        own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert not resp.get("ok")
    assert resp.get("reason") == "WRONG_ATTEMPT"


@requires_bwrap
@requires_userns
def test_payload_kind_claim_mismatch_refused(env):
    env.author_spec("claim-pk")
    root = env.spawn_root()
    mint = env.root_mint("claim-pk")
    assert mint.get("ok")
    resp = env.controller_request(
        "claim-pk", overrides={"payload_kind": "attacker-payload"},
        own_session_slug="s")
    env.root_outcome(root, timeout=300)
    assert not resp.get("ok")
    assert "PAYLOAD_KIND_CLAIM_MISMATCH" in resp.get("reason", "")


@requires_bwrap
@requires_userns
def test_spec_bytes_swapped_in_transit_refused(env):
    """The supervisor receives the spec from the ROOT pipe: a spec whose
    canonical id differs from the GRANT-BOUND id is refused at startup
    (a controller cannot reach the root→supervisor channel at all)."""
    env.author_spec("transit-0001")
    env.spawn_root()
    mint = env.root_mint("transit-0001")
    assert mint.get("ok")
    grant = env.mint("transit-0001x")
    grant.spec_id = "f" * 64  # the root-bound canonical id
    bad_spec = json.loads(json.dumps(env.spec))
    bad_spec["codex"]["version"] = "tampered-version"
    proc = env.spawn_supervisor(grant, expect_spec=__import__(
        "qh.trusted_spec", fromlist=["canonical_spec_bytes"])
        .canonical_spec_bytes(bad_spec))
    line = proc.stdout.readline().decode().strip()
    rc, err = env.supervisor_outcome(proc)
    assert not line.startswith("READY")
    assert rc == 13
    assert "SPEC_ID_MISMATCH" in err
    env.cleanup_procs()
