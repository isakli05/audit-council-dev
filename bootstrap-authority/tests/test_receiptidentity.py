"""RECEIPTIMMUT-001 implementation acceptance tests (RI-AC-01..RI-AC-44):
the NON-RUNTIME canonical G10 original receipt content-identity
mechanism (G10.1-G10.6 + G11) exercised exclusively in SYNTHETIC,
NON-SECRET, disposable tmp worlds — synthetic grants / verified G7
contexts / receipt namespaces / package artifacts / frozen package
copies, and disposable LOCAL scratch Git repositories (git init in
tmp_path; the ONLY remote used anywhere is a LOCAL bare repository
created in tmp_path; NO network, NO live governance repository, NO
real credentials, NO execution authority).

A mapped requirement is NOT a tested requirement until the mapped
assertion actually passes: RI_AC_TESTS at the tail of this file maps
every criterion to the tests whose assertions establish it, and
test_ri_ac_matrix_complete_and_mapped enforces that the map covers
exactly RI-AC-01..RI-AC-44 with real, callable test functions."""
from __future__ import annotations

import hashlib
import inspect
import json
import os
import subprocess
from pathlib import Path

import pytest

from conftest import (REPO_ROOT, build_receipt_namespace,
                      synthetic_g7_context, synthetic_grant_bytes,
                      synthetic_package_artifact)
from bootstrap_authority import binding as bab
from bootstrap_authority import receiptidentity as ri

MODULE_SOURCE = (Path(__file__).resolve().parent.parent
                 / "bootstrap_authority" / "receiptidentity.py").read_text()
FIXED_PATH = ri.RECEIPT_IDENTITY_PUBLICATION_RECORD_PATH
EXPECTED_RESERVED_PATH = ("docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-"
                          "REPLACEMENT-AUDITOR-A-PACKAGE-BINDING-RECEIPT-"
                          "IDENTITY-PUBLICATION.md")


def _git(world, *args, check=True):
    out = subprocess.run(("git", "-C", str(world), *args),
                         capture_output=True, text=True)
    if check:
        assert out.returncode == 0, (args, out.stderr)
    return out


def _commit_all(world, message):
    _git(world, "add", "-A")
    _git(world, "commit", "-qm", message)


def _receipt_file(original) -> Path:
    return (Path(original["context"]["receipt_namespace_path"])
            / original["receipt_name"])


G6_SET = {
    "package_binding_authority_readback_commit_sha": "1" * 40,
    "package_binding_authority_readback_root_tree": "2" * 40,
    "package_binding_authority_readback_record_path":
        "docs/synthetic/G6-READBACK-RECORD.md",
    "package_binding_authority_readback_record_blob_sha1": "3" * 40,
    "package_binding_authority_readback_record_sha256": "4" * 64,
    "package_binding_authority_readback_target_commit_sha": "5" * 40,
    "package_binding_authority_readback_disposition":
        "SYNTHETIC_FAVORABLE_G6_DISPOSITION",
    "grant_mint_consideration_permitted": True,
}


def _g7_record(grant_identity) -> dict:
    """One complete SYNTHETIC G7 mint-publication record (every value
    synthetic and non-secret; NEVER created in any live repository —
    the reserved canonical G7 path stays absent there)."""
    return {
        "schema": ri.G7_MINT_PUBLICATION_SCHEMA,
        "governance_event_id": bab.EVENT_ID,
        "auditor_role": "AUDITOR_A",
        "attempt_slot": "AUDITOR_A_REPLACEMENT_1",
        "future_machine_attempt_id":
            bab.REPLACEMENT_ATTEMPT_SLOTS["AUDITOR_A_REPLACEMENT_1"],
        "grant_identity": grant_identity,
        "grant_document_sha256": "6" * 64,
        "grant_issued_evidence_path":
            "/synthetic/evidence-root/grant-issued-"
            + grant_identity + ".json",
        "grant_issued_evidence_sha256": "7" * 64,
        "grant_issued_evidence_size": 234,
        **G6_SET,
        "execution_authority": "NONE",
        "secret_material": "NONE",
        "publication_semantics": ri.G7_MINT_PUBLICATION_SEMANTICS,
    }


def _world(tmp_path, publish=True, receipt=True, push=True):
    """One complete SYNTHETIC RECEIPTIMMUT-001 world: receipt namespace,
    synthetic grant, synthetic package artifact, a disposable LOCAL
    scratch Git repository with a LOCAL bare remote `origin` whose
    branch `main` is the AUTHORITATIVE domain, a SYNTHETIC G7 mint
    publication of the reserved G7 path whose GIT-DERIVED five-value
    identity feeds the verified G7 context, the G10.1-G10.4 receipt
    (unless receipt=False) and exactly one canonical G10 publication
    introduction (unless publish=False).  Unless push=False everything
    is PUSHED to the bare remote (the ls-remote-authoritative tip);
    with push=False the publications exist LOCALLY ONLY and are NOT
    authority."""
    ns = build_receipt_namespace(tmp_path)
    grant = synthetic_grant_bytes()
    artifact = synthetic_package_artifact(tmp_path)
    identity = bab.grant_identity(grant)
    g7_record = _g7_record(identity)
    repo = Path(tmp_path) / "repo"
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "synthetic@test.invalid")
    _git(repo, "config", "user.name", "synthetic")
    (repo / "seed.txt").write_bytes(b"SYNTHETIC-SEED")
    _commit_all(repo, "seed")
    remote = Path(tmp_path) / "origin.git"
    remote.mkdir(parents=True)
    _git(remote, "init", "-q", "--bare", "-b", "main")
    _git(repo, "remote", "add", "origin", str(remote))
    g7_path = repo.joinpath(
        *bab.G7_MINT_PUBLICATION_RECORD_PATH.split("/"))
    g7_path.parent.mkdir(parents=True, exist_ok=True)
    g7_bytes = json.dumps(g7_record, separators=(",", ":")).encode()
    g7_path.write_bytes(g7_bytes)
    _commit_all(repo, "synthetic G7 mint publication")
    g7_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    context = synthetic_g7_context(
        ns, grant,
        grant_mint_publication_commit_sha=g7_commit,
        grant_mint_publication_root_tree=_git(
            repo, "rev-parse", "HEAD^{tree}").stdout.strip(),
        grant_mint_publication_record_blob_sha1=_git(
            repo, "rev-parse",
            "HEAD:" + bab.G7_MINT_PUBLICATION_RECORD_PATH
        ).stdout.strip(),
        grant_mint_publication_record_sha256=hashlib.sha256(
            g7_bytes).hexdigest())
    original = ri.derive_original_receipt_identity(context, grant,
                                                   artifact)
    if receipt:
        ri.execute_g10_creation_and_readback(context, grant, artifact)
    record = ri.construct_g10_publication_record(original)
    data = ri.receipt_identity_publication_canonical_bytes(record)
    if publish:
        ri.stage_receipt_identity_publication(repo, data)
        _commit_all(repo, "synthetic G10 publication")
    if push:
        _git(repo, "push", "-q", "origin", "main")
    return {"ns": ns, "grant": grant, "context": context,
            "artifact": artifact, "original": original,
            "record": record, "data": data, "repo": repo,
            "remote": remote, "branch": "main", "g7_record": g7_record,
            "g7_commit": g7_commit, "g7_bytes": g7_bytes}


# --- G10.1/G10.2: original identity BEFORE filesystem trust ----------


def test_g10_1_2_original_identity_derived_in_memory_only(tmp_path):
    """RI-AC-01: the canonical receipt bytes are derived from verified
    inputs only; NO receipt file needs to exist (and none is created)."""
    world = _world(tmp_path, publish=False, receipt=False)
    original = world["original"]
    assert not _receipt_file(original).exists()
    assert original["receipt_bytes"] == bab.receipt_canonical_bytes(
        original["receipt_document"])
    assert original["receipt_bytes"] == json.dumps(
        {name: original["receipt_document"][name]
         for name in bab.RECEIPT_FIELDS},
        separators=(",", ":")).encode()
    assert not _receipt_file(original).exists()


def test_g10_2_sha256_and_size_fixed_before_filesystem_trust(tmp_path):
    """RI-AC-02/03: receipt_sha256/receipt_size are derived from the
    G10.1 bytes and NEVER from the receipt file — a mutated file does
    not move the derived ORIGINAL identity."""
    world = _world(tmp_path, publish=False)
    original = world["original"]
    assert original["receipt_sha256"] == hashlib.sha256(
        original["receipt_bytes"]).hexdigest()
    assert original["receipt_size"] == len(original["receipt_bytes"])
    target = _receipt_file(original)
    target.write_bytes(b"GARBAGE-NOT-CANONICAL")
    again = ri.derive_original_receipt_identity(
        world["context"], world["grant"], world["artifact"])
    assert again["receipt_sha256"] == original["receipt_sha256"]
    assert again["receipt_size"] == original["receipt_size"]
    assert again["receipt_bytes"] == original["receipt_bytes"]


# --- G10.3/G10.4: one-shot creation + immediate verified readback -----


def test_g10_3_accepted_one_shot_writer_reused_unchanged(tmp_path):
    """RI-AC-04: G10.3 reuses the ACCEPTED writer exactly — one receipt
    per grant_identity created O_EXCL mode 0600 with fsync semantics;
    a second creation FAILS CLOSED with the accepted duplicate constant."""
    world = _world(tmp_path, publish=False)
    original = world["original"]
    target = _receipt_file(original)
    info = os.lstat(target)
    assert info.st_mode & 0o777 == 0o600
    assert target.read_bytes() == original["receipt_bytes"]
    with pytest.raises(bab.BindingError,
                       match="DUPLICATE_PACKAGE_BINDING_REFUSED"):
        ri.execute_g10_creation_and_readback(world["context"],
                                             world["grant"],
                                             world["artifact"])


def test_g10_4_readback_equality_and_writer_return(tmp_path):
    """RI-AC-05/06/07/08: the exact post-write re-read is performed and
    byte/SHA/size equality required; the writer return must equal the
    independently derived values on every component."""
    world = _world(tmp_path, publish=False)
    original = world["original"]
    good = {"path": original["receipt_name"],
            "sha256": original["receipt_sha256"],
            "size": original["receipt_size"],
            "grant_identity": original["grant_identity"],
            "package_sha256": world["original"]["package_sha256"]}
    ri._g10_4_readback(original, good)
    bad = dict(good, sha256="0" * 64)
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G10_POSTWRITE_READBACK_MISMATCH"):
        ri._g10_4_readback(original, bad)


def test_g10_4_refuses_mutated_receipt_window(tmp_path):
    """RI-T06/RI-AC-06: mutation between G10.3 and G10.4 — garbage
    current bytes FAIL the canonicalization gate first, and a VALID
    canonical receipt for a DIFFERENT package (same-size class) FAILS
    the original-identity comparison."""
    world = _world(tmp_path, publish=False)
    original = world["original"]
    target = _receipt_file(original)
    good = {"path": original["receipt_name"],
            "sha256": original["receipt_sha256"],
            "size": original["receipt_size"],
            "grant_identity": original["grant_identity"],
            "package_sha256": original["package_sha256"]}
    target.write_bytes(b"GARBAGE-NOT-EVEN-JSON")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="RECEIPT_CANONICALIZATION_INVALID"):
        ri._g10_4_readback(original, good)
    package_b = synthetic_package_artifact(tmp_path,
                                           payload=b"WINDOW-PACKAGE-B")
    original_b = ri.derive_original_receipt_identity(world["context"],
                                                     world["grant"],
                                                     package_b)
    target.write_bytes(original_b["receipt_bytes"])
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G10_POSTWRITE_READBACK_MISMATCH"):
        ri._g10_4_readback(original, good)


# --- G10.5: the 24-field publication record ---------------------------


def test_publication_schema_closed_world(tmp_path):
    """RI-AC-10: EXACTLY the 24 closed-world fields; any extra, missing
    or duplicate key is refused."""
    world = _world(tmp_path, publish=False)
    assert len(ri.RIP_FIELDS) == 24
    assert len(set(ri.RIP_FIELDS)) == 24
    doc = dict(world["record"])
    doc["extra"] = 1
    with pytest.raises(ri.ReceiptIdentityError, match="RIP_KEYS_INVALID"):
        ri.receipt_identity_publication_canonical_bytes(doc)
    del doc["extra"]
    del doc["receipt_size"]
    with pytest.raises(ri.ReceiptIdentityError, match="RIP_KEYS_INVALID"):
        ri.receipt_identity_publication_canonical_bytes(doc)
    raw = world["data"].decode()
    duplicated = raw.replace('"schema":', '"schema":"X","schema":', 1)
    with pytest.raises(bab.BindingError, match="DUPLICATE_KEY"):
        ri.parse_receipt_identity_publication(duplicated.encode())


def test_publication_field_order_normative(tmp_path):
    """RI-AC-11: the EXACT fixed field order is normative — a
    lexicographically re-sorted serialization is NON-canonical."""
    world = _world(tmp_path, publish=False)
    sorted_bytes = json.dumps(world["record"], sort_keys=True,
                              separators=(",", ":")).encode()
    assert sorted_bytes != world["data"]
    with pytest.raises(ri.ReceiptIdentityError,
                       match="RIP_CANONICALIZATION_INVALID"):
        ri.parse_receipt_identity_publication(sorted_bytes)


def test_publication_canonical_serialization_deterministic(tmp_path):
    """RI-AC-12: ONE canonical serialization rule — two independent
    serializations are byte-identical, compact, pure ASCII, no trailing
    newline; re-serialization of the parse equals the bytes."""
    world = _world(tmp_path, publish=False)
    data = world["data"]
    again = ri.receipt_identity_publication_canonical_bytes(
        dict(world["record"]))
    assert data == again
    assert not data.endswith(b"\n") and b": " not in data \
        and b", " not in data
    data.decode("ascii")
    parsed = ri.parse_receipt_identity_publication(data)
    assert ri.receipt_identity_publication_canonical_bytes(parsed) == data


@pytest.mark.parametrize("mutate", [
    lambda raw: raw + b"\n",
    lambda raw: b" " + raw,
    lambda raw: raw.replace(b",", b", ", 1),
    lambda raw: raw[:-1] + b" }",
])
def test_publication_noncanonical_bytes_refused(tmp_path, mutate):
    """RI-AC-12: any non-canonical byte sequence (trailing newline,
    leading whitespace, insignificant whitespace) is refused."""
    world = _world(tmp_path, publish=False)
    with pytest.raises(ri.ReceiptIdentityError,
                       match="RIP_CANONICALIZATION_INVALID"):
        ri.parse_receipt_identity_publication(mutate(world["data"]))


@pytest.mark.parametrize("field,bad", [
    ("governance_event_id", "OTHER-EVENT-20261002-01"),
    ("auditor_role", "AUDITOR_A_REPLACEMENT_1"),
    ("attempt_slot", "AUDITOR_A"),
    ("attempt_id", "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-"
                   "AUDITOR-A-01"),
    ("g7_mint_publication_record_path", "docs/chatgpt-project/OTHER.md"),
    ("execution_authority", "ALL"),
    ("secret_material", "PRESENT"),
    ("binding_semantics", "ONE_SHOT_IMMUTABLE_NON_RUNTIME_PACKAGE_BINDING"),
    ("grant_identity", "z" * 64),
    ("receipt_sha256", "1" * 40),
    ("g7_mint_publication_commit_sha", "1" * 64),
    ("g7_mint_publication_record_blob_sha1", "not-hex"),
    ("receipt_size", True),
    ("receipt_size", -1),
    ("receipt_namespace_st_dev", "2049"),
    ("receipt_namespace_st_ino", 0),
    ("one_receipt_only", False),
    ("one_receipt_only", "true"),
    ("operator_authority_id", "not a safe identity!"),
    ("receipt_path", "relative/receipt.json"),
    ("receipt_namespace_path", "/ns//double"),
])
def test_publication_field_shape_gates(tmp_path, field, bad):
    """RI-AC-10: per-field fail-closed shape gates (RIP_<FIELD>_*)."""
    world = _world(tmp_path, publish=False)
    doc = dict(world["record"])
    doc[field] = bad
    raw = json.dumps({name: doc[name] for name in ri.RIP_FIELDS},
                     separators=(",", ":")).encode()
    with pytest.raises(ri.ReceiptIdentityError):
        ri.parse_receipt_identity_publication(raw)


def test_publication_exact_value_gates(tmp_path):
    """RI-AC-10: exact schema/purpose tags carry their own constants."""
    world = _world(tmp_path, publish=False)
    for field, value, constant in (
            ("schema", "AUCDEV-023-PACKAGE-BINDING-RECEIPT-IDENTITY"
                       "-PUBLICATION-V2", "RIP_SCHEMA_UNEXPECTED"),
            ("purpose", "EXECUTION_RECEIPT_IDENTITY",
             "RIP_PURPOSE_UNEXPECTED")):
        doc = dict(world["record"])
        doc[field] = value
        raw = json.dumps({name: doc[name] for name in ri.RIP_FIELDS},
                         separators=(",", ":")).encode()
        with pytest.raises(ri.ReceiptIdentityError, match=constant):
            ri.parse_receipt_identity_publication(raw)


def test_no_self_git_identity_in_record(tmp_path):
    """RI-AC-13: the record contains NO self-Git identity field."""
    world = _world(tmp_path, publish=False)
    for field in ri.RIP_FIELDS:
        assert not field.startswith("receipt_identity_publication_")
    assert "receipt_identity_publication_commit_sha" not in \
        world["record"]
    assert "self" not in " ".join(ri.RIP_FIELDS).lower()


def test_dependency_graph_acyclic(tmp_path):
    """RI-AC-14: acyclicity by construction — record construction takes
    ONLY the pre-publication original identity (no Git identity input);
    the five-value post-publication identity is derived ONLY from a
    selection over an already-existing commit and is disjoint from the
    record's field set (a leaf; no readback-of-readback chain)."""
    world = _world(tmp_path)
    assert list(inspect.signature(
        ri.construct_g10_publication_record).parameters) == ["original"]
    selection = ri.select_canonical_g10_publication(
        world["repo"], "HEAD", world["record"])
    post = ri.derive_post_publication_identity(selection)
    assert set(post).isdisjoint(set(ri.RIP_FIELDS))
    assert post["receipt_identity_publication_commit_sha"] == \
        selection["commit"]


# --- R-NS verified-namespace rule --------------------------------------


def test_absolute_receipt_path_is_identity_field_only(tmp_path):
    """R-NS-1/2/3: the absolute receipt_path is DERIVED (namespace path
    + '/' + deterministic name); the writer return carries the
    namespace-RELATIVE name only and G10.4 compares name-to-name."""
    world = _world(tmp_path, publish=False, receipt=False)
    original = world["original"]
    assert original["receipt_path"] == \
        original["context"]["receipt_namespace_path"] + "/" \
        + original["receipt_name"]
    result = ri.execute_g10_creation_and_readback(
        world["context"], world["grant"], world["artifact"])
    assert result["writer_return"]["path"] == original["receipt_name"]
    assert "/" not in result["writer_return"]["path"]
    assert bab.receipt_name(original["grant_identity"]) == \
        original["receipt_name"]
    assert world["record"]["receipt_path"] == original["receipt_path"]


def test_receipt_reads_exclusively_dir_fd_relative():
    """R-NS-4/5/6 (static side): the module contains NO
    absolute-path receipt read — every os.open call site is
    dir_fd-relative (the only receipt access path is the held,
    fstat-verified namespace fd + deterministic name O_NOFOLLOW)."""
    lines = MODULE_SOURCE.splitlines()
    opens = [line for line in lines if "os.open(" in line]
    assert opens, "expected at least one verified receipt open"
    for line in opens:
        assert "dir_fd=" in line, line


def test_receipt_symlink_refused(tmp_path):
    """R-NS-5 (behavioral): a symlink at the deterministic receipt name
    is refused by the dir_fd-relative O_NOFOLLOW open."""
    world = _world(tmp_path, publish=False)
    original = world["original"]
    target = _receipt_file(original)
    copy = target.with_name(target.name + ".copy")
    copy.write_bytes(target.read_bytes())
    target.unlink()
    os.symlink(copy.name, target)
    with pytest.raises(ri.ReceiptIdentityError,
                       match="RECEIPT_ABSENT_OR_UNOPENABLE"):
        ri._read_current_receipt(original["context"],
                                 original["receipt_name"])


def test_g11_refuses_namespace_replacement(tmp_path):
    """RI-AC-36 / RI-T15 / CASE G: a REPLACED namespace directory at the
    same pathname is a different OBJECT — the st_dev/st_ino pin refuses
    even byte-identical receipts inside the replacement."""
    world = _world(tmp_path)
    original = world["original"]
    ns_path = Path(original["context"]["receipt_namespace_path"])
    parent = ns_path.parent
    moved = parent / "namespace-moved-away"
    ns_path.rename(moved)
    replacement = parent / ns_path.name
    replacement.mkdir()
    os.chmod(replacement, 0o700)
    (replacement / original["receipt_name"]).write_bytes(
        original["receipt_bytes"])
    assert os.stat(moved).st_ino != os.stat(replacement).st_ino
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G11_REFUSED:.*"
                             "RECEIPT_NAMESPACE_IDENTITY_MISMATCH"):
        ri.g11_independent_rederivation(world["context"], world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G10_POST_PUSH_READBACK_FAILED"):
        ri.execute_g10_publication_readback(world["repo"], world["remote"],
                                          world["branch"],
                                            original)


# --- R1-R22 canonical selector -----------------------------------------


def test_selector_exact_one_cardinality(tmp_path):
    """RI-AC-22: exactly one qualifying candidate; every selection
    identity is independently re-derived from Git."""
    world = _world(tmp_path)
    selection = ri.select_canonical_g10_publication(world["repo"],
                                                    "HEAD", world["record"])
    head = _git(world["repo"], "rev-parse", "HEAD").stdout.strip()
    assert selection["commit"] == head           # sole introduction
    assert selection["parent"] == _git(world["repo"], "rev-parse",
                                       "HEAD^").stdout.strip()
    assert selection["root_tree"] == _git(world["repo"], "rev-parse",
                                          "HEAD^{tree}").stdout.strip()
    blob = _git(world["repo"], "ls-tree", "HEAD", "--", FIXED_PATH
                ).stdout.split("\t")[0].split()[2]
    assert selection["record_blob_sha1"] == blob
    assert selection["record"] == world["record"]
    assert selection["record_bytes"] == world["data"]


def test_selector_tree_state_probes(tmp_path):
    """RI-AC-17/18: R2/R3 are verified from the ACTUAL trees (absent in
    the parent, present in the candidate), never from diff output."""
    world = _world(tmp_path)
    selection = ri.select_canonical_g10_publication(world["repo"],
                                                    "HEAD", world["record"])
    assert not ri._tree_has_path(world["repo"], selection["parent"],
                                 FIXED_PATH)
    assert ri._tree_has_path(world["repo"], selection["commit"],
                             FIXED_PATH)


def test_selector_raw_add_classification(tmp_path):
    """RI-AC-19: the canonical RAW ADD classification — the selector's
    fixed-path delta is exactly one entry with status A under
    no-renames semantics with rename/copy detection disabled."""
    world = _world(tmp_path)
    selection = ri.select_canonical_g10_publication(world["repo"],
                                                    "HEAD", world["record"])
    out = _git(world["repo"], "-c", "diff.renames=false", "diff-tree",
               "--no-renames", "--name-status", "--no-commit-id", "-r",
               selection["parent"], selection["commit"], "--",
               FIXED_PATH).stdout.strip()
    assert out == f"A\t{FIXED_PATH}"


def test_selector_rename_presentation_invariance(tmp_path, monkeypatch):
    """RI-AC-19/20: an introduction PRESENTED as a rename (R100 under
    -M) is still the canonical raw A under --no-renames; the selector
    lands on exactly that introduction; a rename/copy-status delta is
    refused outright (C4_RENAME_COPY_INFERENCE_PRESENT)."""
    world = _world(tmp_path, publish=False)
    repo = world["repo"]
    other = "docs/chatgpt-project/other-staging.md"
    staged = repo / other
    staged.parent.mkdir(parents=True, exist_ok=True)
    staged.write_bytes(world["data"])
    _commit_all(repo, "staged elsewhere")
    _git(repo, "mv", other, FIXED_PATH)
    _commit_all(repo, "rename-presented introduction")
    parent = _git(repo, "rev-parse", "HEAD^").stdout.strip()
    rename_aware = _git(repo, "-c", "diff.renames=true", "diff-tree",
                        "-M", "--name-status", "--no-commit-id", "-r",
                        parent, "HEAD").stdout
    assert any(line.startswith("R100") for line in
               rename_aware.splitlines()), rename_aware
    selection = ri.select_canonical_g10_publication(repo, "HEAD",
                                                    world["record"])
    assert selection["commit"] == _git(repo, "rev-parse",
                                       "HEAD").stdout.strip()
    monkeypatch.setattr(ri, "_git",
                        lambda *args, **kwargs:
                        f"R100\t{other}\t{FIXED_PATH}\n")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="C4_RENAME_COPY_INFERENCE_PRESENT"):
        ri._require_raw_add(repo, parent, selection["commit"],
                            FIXED_PATH)


def test_selector_tree_state_contradiction_defensive(tmp_path,
                                                     monkeypatch):
    """RI-AC-21: a displayed A that contradicts the R2/R3 tree facts is
    refused C4_TREE_STATE_CONTRADICTION (mandatory cross-check)."""
    world = _world(tmp_path)
    monkeypatch.setattr(ri, "_tree_has_path", lambda *a, **k: True)
    with pytest.raises(ri.ReceiptIdentityError,
                       match="C4_TREE_STATE_CONTRADICTION"):
        ri.select_canonical_g10_publication(world["repo"], "HEAD",
                                            world["record"])


def test_selector_zero_candidates_not_found(tmp_path):
    """RI-AC-23: zero qualifying introductions FAIL CLOSED
    (..._NOT_FOUND); no fallback, no partial result."""
    world = _world(tmp_path, publish=False)
    with pytest.raises(ri.ReceiptIdentityError,
                       match="CANONICAL_G10_RECEIPT_IDENTITY_"
                             "PUBLICATION_NOT_FOUND"):
        ri.select_canonical_g10_publication(world["repo"], "HEAD",
                                            world["record"])


def test_selector_delete_readd_ambiguous(tmp_path):
    """RI-AC-24/RI-AC-27/RI-T09/RI-T10: delete + re-add yields a SECOND
    qualifying introduction — AMBIGUOUS fail-closed; NO supersession
    mechanism exists to resolve it."""
    world = _world(tmp_path)
    repo = world["repo"]
    first = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "rm", "-q", FIXED_PATH)
    _commit_all(repo, "delete")
    ri.stage_receipt_identity_publication(repo, world["data"])
    _commit_all(repo, "re-add")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="CANONICAL_G10_RECEIPT_IDENTITY_"
                             "PUBLICATION_AMBIGUOUS") as caught:
        ri.select_canonical_g10_publication(repo, "HEAD", world["record"])
    assert first in str(caught.value)     # the original is enumerated


def test_selector_modification_never_replaces_R(tmp_path):
    """RI-AC-25/RI-T24: a later modification of the publication content
    NEVER replaces the path-INTRODUCTION commit R and creates NO new
    candidate — verification reads R's blob; HEAD-side content is
    non-authoritative (no latest-HEAD authority)."""
    world = _world(tmp_path)
    repo = world["repo"]
    first = _git(repo, "rev-parse", "HEAD").stdout.strip()
    doctored = dict(world["record"], receipt_size=world["record"]
                    ["receipt_size"] + 1)
    ri.stage_receipt_identity_publication(
        repo, ri.receipt_identity_publication_canonical_bytes(doctored))
    _commit_all(repo, "later modification")
    assert _git(repo, "cat-file", "blob",
                f"HEAD:{FIXED_PATH}").stdout.encode() != world["data"]
    selection = ri.select_canonical_g10_publication(repo, "HEAD",
                                                    world["record"])
    assert selection["commit"] == first
    assert selection["record_bytes"] == world["data"]


def test_selector_first_parent_domain_only(tmp_path):
    """RI-AC-15/22: only the authoritative FIRST-PARENT history counts —
    a duplicate introduction on a merged side branch does not create a
    second candidate."""
    world = _world(tmp_path)
    repo = world["repo"]
    first = _git(repo, "rev-parse", "HEAD").stdout.strip()
    seed = _git(repo, "rev-parse", "HEAD^").stdout.strip()
    _git(repo, "checkout", "-q", "-b", "side", seed)
    ri.stage_receipt_identity_publication(repo, world["data"])
    _commit_all(repo, "side introduction")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "--no-ff", "-q", "-m", "merge side", "side")
    assert _git(repo, "cat-file", "-e", f"HEAD:{FIXED_PATH}"
                ).returncode == 0
    selection = ri.select_canonical_g10_publication(repo, "HEAD",
                                                    world["record"])
    assert selection["commit"] == first


def test_selector_merge_introduction_ineligible(tmp_path):
    """RI-AC-16/R1: a path introduced ONLY by a merge commit is
    INELIGIBLE (merge commits are not qualifying candidates) — the
    selector FAILS CLOSED with NOT_FOUND rather than falling back."""
    world = _world(tmp_path, publish=False)
    repo = world["repo"]
    seed = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "checkout", "-q", "-b", "side", seed)
    ri.stage_receipt_identity_publication(repo, world["data"])
    _commit_all(repo, "side introduction")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "--no-ff", "-q", "-m", "merge side", "side")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="CANONICAL_G10_RECEIPT_IDENTITY_"
                             "PUBLICATION_NOT_FOUND"):
        ri.select_canonical_g10_publication(repo, "HEAD", world["record"])


def test_selector_against_local_bare_remote(tmp_path):
    """The publication workflow's remote shape, exercised against a
    disposable LOCAL bare repository ONLY (no network, no live
    governance repository): after one push the selector over the bare
    repository resolves the SAME canonical introduction."""
    world = _world(tmp_path)
    bare = Path(tmp_path) / "remote.git"
    bare.mkdir(parents=True)
    _git(bare, "init", "-q", "--bare", "-b", "main")
    _git(world["repo"], "push", "-q", str(bare), "main")
    selection = ri.select_canonical_g10_publication(bare, "main",
                                                    world["record"])
    assert selection["commit"] == _git(world["repo"], "rev-parse",
                                       "main").stdout.strip()


def test_selector_no_package_provided_authority():
    """RI-AC-26 + CR-IMPL-004: G11/selector accept NO package-provided
    R, no cached selector input and NO caller-selected arbitrary local
    ref — the signatures carry repo / the (remote, branch) authoritative
    binding / expected DERIVED values only (never a commit identity)."""
    assert list(inspect.signature(
        ri.select_canonical_g10_publication).parameters) == \
        ["repo", "ref", "expected"]
    assert list(inspect.signature(
        ri.select_canonical_g7_publication).parameters) == \
        ["repo", "tip", "expected"]
    assert list(inspect.signature(
        ri.resolve_authoritative_tip).parameters) == \
        ["repo", "remote", "branch"]
    assert list(inspect.signature(
        ri.g11_independent_rederivation).parameters) == \
        ["verified_g7_context", "grant_bytes", "package_artifact",
         "repo", "remote", "branch", "expected_g6_identity_set"]
    assert list(inspect.signature(
        ri.execute_g10_publication_readback).parameters) == \
        ["repo", "remote", "branch", "original"]


# --- G10.6: post-push readback ------------------------------------------


def test_g10_6_readback_requires_exact_publication_bytes(tmp_path):
    """RI-AC-28: G10 completion requires the selector-derived
    publication whose bytes EQUAL the G10.5 canonical construction — a
    repository whose record differs from the expected construction
    yields NOT_FOUND (no fallback, no partial completion)."""
    world = _world(tmp_path, publish=False)
    other = ri.construct_g10_publication_record(
        ri.derive_original_receipt_identity(
            world["context"], world["grant"],
            synthetic_package_artifact(tmp_path,
                                       payload=b"OTHER-PACKAGE-BYTES")))
    ri.stage_receipt_identity_publication(
        world["repo"], ri.receipt_identity_publication_canonical_bytes(
            other))
    _commit_all(world["repo"], "publication of a different identity")
    _git(world["repo"], "push", "-q", "origin", "main")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="CANONICAL_G10_RECEIPT_IDENTITY_"
                             "PUBLICATION_NOT_FOUND"):
        ri.execute_g10_publication_readback(world["repo"],
                                            world["remote"],
                                            world["branch"],
                                            world["original"])


def test_g10_6_post_push_current_receipt_equality(tmp_path):
    """RI-AC-29/RI-T07: after publication, CURRENT must still equal
    ORIGINAL — mutation after G10.4 but before G10.6 completion leaves
    G10 FAIL CLOSED; the restored original completes G10."""
    world = _world(tmp_path)
    target = _receipt_file(world["original"])
    target.write_bytes(world["original"]["receipt_bytes"] + b"X")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G10_POST_PUSH_READBACK_FAILED"):
        ri.execute_g10_publication_readback(world["repo"],
                                            world["remote"],
                                            world["branch"],
                                            world["original"])
    target.write_bytes(world["original"]["receipt_bytes"])
    out = ri.execute_g10_publication_readback(world["repo"],
                                           world["remote"],
                                           world["branch"],
                                              world["original"])
    assert out["current_receipt_sha256"] == \
        world["original"]["receipt_sha256"]


# --- G11: independent re-derivation -------------------------------------


def test_g11_independent_rederivation_success(tmp_path):
    """RI-AC-30: G11 independently re-derives everything (grant,
    package, namespace, selector, publication, current receipt) and
    PASSES on the intact synthetic world; the five-value post-hoc
    identity agrees with Git."""
    world = _world(tmp_path)
    out = ri.g11_independent_rederivation(world["context"],
                                          world["grant"],
                                          world["artifact"],
                                          world["repo"], world["remote"],
                                          world["branch"], G6_SET)
    post = out["post_publication_identity"]
    assert post["receipt_identity_publication_commit_sha"] == \
        _git(world["repo"], "rev-parse", "HEAD").stdout.strip()
    assert post["receipt_identity_publication_record_path"] == FIXED_PATH
    g7 = out["g7_post_publication_identity"]
    assert g7["grant_mint_publication_commit_sha"] == world["g7_commit"]
    assert g7["grant_mint_publication_record_path"] == \
        bab.G7_MINT_PUBLICATION_RECORD_PATH
    assert out["authoritative_binding"]["tip"] == \
        _git(world["repo"], "rev-parse", "HEAD").stdout.strip()
    assert out["current_receipt_sha256"] == \
        world["original"]["receipt_sha256"]
    assert out["current_receipt_size"] == \
        world["original"]["receipt_size"]


def test_g11_refuses_byte_flip_same_size(tmp_path):
    """RI-AC-31/RI-T01/RI-T22: same-size different bytes REFUSED."""
    world = _world(tmp_path)
    data = bytearray(world["original"]["receipt_bytes"])
    data[-2] ^= 0x01
    _receipt_file(world["original"]).write_bytes(bytes(data))
    with pytest.raises(ri.ReceiptIdentityError, match="G11_REFUSED"):
        ri.g11_independent_rederivation(world["context"], world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)


def test_g11_refuses_truncation_and_append(tmp_path):
    """RI-AC-32/RI-T02/RI-T03: truncate (size) and append (size+SHA)
    each REFUSED independently of the SHA/size split."""
    world = _world(tmp_path)
    target = _receipt_file(world["original"])
    target.write_bytes(world["original"]["receipt_bytes"][:-3])
    with pytest.raises(ri.ReceiptIdentityError, match="G11_REFUSED"):
        ri.g11_independent_rederivation(world["context"], world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)
    target.write_bytes(world["original"]["receipt_bytes"] + b"PAD")
    with pytest.raises(ri.ReceiptIdentityError, match="G11_REFUSED"):
        ri.g11_independent_rederivation(world["context"], world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)


def test_g11_refuses_deletion(tmp_path):
    """RI-T23: publication present but the CURRENT receipt missing —
    the pinned-namespace open FAILS CLOSED."""
    world = _world(tmp_path)
    _receipt_file(world["original"]).unlink()
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G11_REFUSED:.*RECEIPT_ABSENT_OR_UNOPENABLE"):
        ri.g11_independent_rederivation(world["context"], world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)


def test_g11_refuses_package_b_substitution(tmp_path):
    """RI-AC-34/CASE D/RI-T12: after PACKAGE_A's original receipt, an
    owner rewrite binding PACKAGE_B can NEVER be accepted — neither the
    current-receipt comparison (mutated file) nor the cross-binding
    (PACKAGE_B artifact) passes."""
    world = _world(tmp_path)
    package_b = synthetic_package_artifact(tmp_path,
                                           payload=b"PACKAGE-B-BYTES")
    original_b = ri.derive_original_receipt_identity(world["context"],
                                                     world["grant"],
                                                     package_b)
    assert original_b["receipt_bytes"] != world["original"]["receipt_bytes"]
    _receipt_file(world["original"]).write_bytes(
        original_b["receipt_bytes"])
    with pytest.raises(ri.ReceiptIdentityError, match="G11_REFUSED"):
        ri.g11_independent_rederivation(world["context"], world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)
    with pytest.raises(ri.ReceiptIdentityError):
        ri.g11_independent_rederivation(world["context"], world["grant"],
                                        package_b, world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)


def test_g11_accepts_byte_identical_new_inode(tmp_path):
    """RI-AC-44/CASE C (accepted DESIGN-001 disposition): a re-created
    receipt file with BYTE-IDENTICAL canonical content at the canonical
    name (new inode) is SEMANTICALLY INERT — every pinned identity is
    unchanged and G11 still passes; receipt FILE object continuity is
    NOT a held invariant."""
    world = _world(tmp_path)
    target = _receipt_file(world["original"])
    first_ino = os.lstat(target).st_ino
    payload = target.read_bytes()
    target.unlink()
    target.write_bytes(payload)
    assert os.lstat(target).st_ino != first_ino
    ri.g11_independent_rederivation(world["context"], world["grant"],
                                    world["artifact"], world["repo"],
                                    world["remote"], world["branch"],
                                    G6_SET)


def test_g11_refuses_grant_substitution(tmp_path):
    """RI-AC-33/RI-T13: a different grant (different derived identity
    than the context names) is refused at re-derivation."""
    world = _world(tmp_path)
    other_grant = synthetic_grant_bytes(
        operator_authority_id="SYNTHETIC-OTHER-OPERATOR-20261009-01")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G10_RECEIPT_BYTES_DERIVATION_REFUSED"):
        ri.g11_independent_rederivation(world["context"], other_grant,
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)


def test_g11_refuses_g7_and_crossbinding_substitution(tmp_path):
    """RI-AC-35/RI-T14 + the Section 8 cross-binding refusal groups +
    CR-IMPL-002: a SHAPE-VALID context whose G7 five-value identity
    does NOT equal the independently Git-derived identity is refused
    by the G7_CONTEXT_IDENTITY_MISMATCH comparison (a matching
    caller-supplied context is NOT itself proof of derived identity);
    the published-vs-derived cross-check refuses each group by
    constant."""
    world = _world(tmp_path)
    altered = dict(world["context"],
                   grant_mint_publication_commit_sha="8" * 40)
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G11_REFUSED:.*G7_CONTEXT_IDENTITY_MISMATCH"):
        ri.g11_independent_rederivation(altered, world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)
    doctored = dict(world["record"])
    for constant, field, value in (
            ("RIP_RECEIPT_ORIGINAL_MISMATCH", "receipt_sha256", "9" * 64),
            ("RIP_GRANT_CONTEXT_MISMATCH", "grant_identity", "a" * 64),
            ("RIP_PACKAGE_MISMATCH", "package_sha256", "b" * 64),
            ("RIP_G7_CONTEXT_MISMATCH",
             "g7_mint_publication_commit_sha", "c" * 40),
            ("RIP_NAMESPACE_MISMATCH", "receipt_namespace_st_ino",
             doctored["receipt_namespace_st_ino"] + 1)):
        bad = dict(doctored)
        bad[field] = value
        with pytest.raises(ri.ReceiptIdentityError, match=constant):
            ri._require_published_matches_derived(bad, world["original"])


# --- governance / held-invariant non-expansion --------------------------


def test_reserved_publication_path_absent_in_live_repo():
    """RI-AC-09: the future operative canonical publication path stays
    RESERVED and ABSENT until the separately authorized G10 execution
    (on disk, tracked, and across ALL history of the live repository)."""
    assert ri.RECEIPT_IDENTITY_PUBLICATION_RECORD_PATH == \
        EXPECTED_RESERVED_PATH
    assert not (REPO_ROOT / EXPECTED_RESERVED_PATH).exists()
    history = subprocess.run(
        ["git", "log", "--oneline", "--", EXPECTED_RESERVED_PATH],
        cwd=REPO_ROOT, capture_output=True, text=True)
    assert history.stdout == "", history.stdout


def test_grant_and_receipt_schemas_unchanged():
    """RI-AC-37/42: the 20-field grant schema and the 10-field receipt
    schema are unchanged; the G10.1 record IS the accepted receipt."""
    assert len(bab.GRANT_FIELDS) == 20
    assert bab.RECEIPT_FIELDS == (
        "schema", "grant_identity", "package_sha256",
        "governance_event_id", "auditor_role", "attempt_slot",
        "attempt_id", "operator_authority_id",
        "created_under_package_binding_authority", "binding_semantics")
    assert len(bab.RECEIPT_FIELDS) == 10


def test_public_surface_and_execution_authority_nonexpansion(tmp_path):
    """RI-AC-38/41: BootstrapAuthority stays exactly {state, store,
    run_attempt} with NO receipt functionality; runtime.py/__init__.py
    never IMPORT or CALL the receipt-identity module (AST-enforced —
    the 2026-10-10 operator-authorized provenance rebind necessarily
    names the module PATH as a provenance DATA record inside
    EXPECTED_PROVENANCE, which is admission data, not module coupling);
    the publication pins execution_authority = NONE."""
    from bootstrap_authority import runtime as barmod
    import ast as _rast
    public = {name for name, member in
              vars(barmod.BootstrapAuthority).items()
              if not name.startswith("_")
              and not isinstance(member, (classmethod, staticmethod))}
    assert public == {"state", "store", "run_attempt"}
    for module_name in ("runtime.py", "__init__.py"):
        source = (Path(__file__).resolve().parent.parent
                  / "bootstrap_authority" / module_name).read_text()
        for node in _rast.walk(_rast.parse(source)):
            if isinstance(node, _rast.ImportFrom) \
                    and (node.module or "").endswith("receiptidentity"):
                raise AssertionError(
                    f"{module_name} imports the receipt-identity module")
            if isinstance(node, _rast.Import) and any(
                    alias.name.endswith("receiptidentity")
                    for alias in node.names):
                raise AssertionError(
                    f"{module_name} imports the receipt-identity module")
            if isinstance(node, _rast.Attribute) \
                    and node.attr == "receiptidentity":
                raise AssertionError(
                    f"{module_name} references the receipt-identity module")
    world = _world(tmp_path, publish=False)
    assert world["record"]["execution_authority"] == "NONE"


def test_accountingstore_unused_and_stage_nonexpansion():
    """RI-AC-39/40: AccountingStore is unused for receipt identity (no
    accounting state, no .jsonl anywhere in the module); G10 is refined
    internally ONLY — no new top-level governance stage (no G13, no
    supersession MACHINERY: no supersession constant, function or
    protocol identifier) is defined."""
    import ast as _ast
    for node in _ast.walk(_ast.parse(MODULE_SOURCE)):
        if isinstance(node, _ast.ImportFrom):
            assert not (node.module or "").partition(".")[
                0] == "accounting"
        elif isinstance(node, _ast.Import):
            assert not any(alias.name.split(".")[0] == "accounting"
                           for alias in node.names)
    assert "AccountingStore" not in dir(ri)
    assert "open_custody_dir" not in dir(ri)
    assert ".jsonl" not in MODULE_SOURCE
    assert "G13" not in MODULE_SOURCE
    assert "SUPERSEDE" not in MODULE_SOURCE.upper().replace(
        "SUPERSESSION", "")
    assert "def supersede" not in MODULE_SOURCE.lower()
    assert not [name for name in dir(ri)
                if "supersede" in name.lower()]


def test_publication_flags_exact(tmp_path):
    """RI-AC-43: one_receipt_only = true / execution_authority = NONE /
    secret_material = NONE / the exact binding semantics constant."""
    world = _world(tmp_path, publish=False)
    record = world["record"]
    assert record["one_receipt_only"] is True
    assert record["execution_authority"] == "NONE"
    assert record["secret_material"] == "NONE"
    assert record["binding_semantics"] == \
        "ORIGINAL_CREATION_TIME_NON_RUNTIME_RECEIPT_IDENTITY"
    assert ri.RIP_BINDING_SEMANTICS == \
        "ORIGINAL_CREATION_TIME_NON_RUNTIME_RECEIPT_IDENTITY"


def test_mutation_class_matrix(tmp_path):
    """RI-AC-44 (table form): every Section 15 mutation class maps to at
    least one fail-closed verification stage actually exercised here."""
    world = _world(tmp_path)
    target = _receipt_file(world["original"])
    cases = [
        (b"OWNER-REWRITE-DIFFERENT-BYTES", "G11_REFUSED"),
        (world["original"]["receipt_bytes"][:100], "G11_REFUSED"),
        (world["original"]["receipt_bytes"] + b"APPEND", "G11_REFUSED"),
    ]
    for payload, constant in cases:
        target.write_bytes(payload)
        with pytest.raises(ri.ReceiptIdentityError, match=constant):
            ri.g11_independent_rederivation(world["context"],
                                            world["grant"],
                                            world["artifact"],
                                            world["repo"], world["remote"],
                                            world["branch"], G6_SET)
    target.unlink()
    with pytest.raises(ri.ReceiptIdentityError, match="G11_REFUSED"):
        ri.g11_independent_rederivation(world["context"], world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)
    target.write_bytes(world["original"]["receipt_bytes"])


# --- CR-IMPL-002: the independent canonical G7 mint-publication
# selector (accepted PUBID-001 C1-C15 + DIFFSEM canonical C4) ---------


def _publish_g7_only(tmp_path, record, name="g7repo"):
    """A disposable LOCAL repo carrying exactly ONE synthetic G7 mint
    publication introduction of the reserved G7 path (nothing else)."""
    repo = Path(tmp_path) / name
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "synthetic@test.invalid")
    _git(repo, "config", "user.name", "synthetic")
    (repo / "seed.txt").write_bytes(b"SYNTHETIC-SEED")
    _commit_all(repo, "seed")
    path = repo.joinpath(*bab.G7_MINT_PUBLICATION_RECORD_PATH.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(record, separators=(",", ":")).encode())
    _commit_all(repo, "synthetic G7 mint publication")
    return repo, path


def test_g7_record_parser_closed_world_and_shapes():
    """C5/C7/C9-C14 parse surface: the EXACT closed-world 21-field set
    (added/missing keys refused), fixed constants, the deterministic
    evidence-path suffix, and per-field shape gates — all fail closed."""
    identity = "f" * 64
    record = _g7_record(identity)
    data = json.dumps(record, separators=(",", ":")).encode()
    parsed = ri.parse_g7_mint_publication(data)
    assert parsed == {name: record[name]
                      for name in ri.G7_MINT_PUBLICATION_FIELDS}
    assert len(ri.G7_MINT_PUBLICATION_FIELDS) == 21
    for mutated, constant in (
            (dict(record, surprise=1), "G7MP_KEYS_INVALID"),
            ({k: v for k, v in record.items() if k != "schema"},
             "G7MP_KEYS_INVALID"),
            (dict(record, grant_issued_evidence_path=
                  "/synthetic/evidence-root/other.json"),
             "G7MP_GRANT_ISSUED_EVIDENCE_PATH_INVALID"),
            (dict(record, grant_issued_evidence_size=0),
             "G7MP_GRANT_ISSUED_EVIDENCE_SIZE_INVALID"),
            (dict(record, grant_issued_evidence_sha256="zz" * 32),
             "G7MP_GRANT_ISSUED_EVIDENCE_SHA256_INVALID"),
            (dict(record, future_machine_attempt_id=""),
             "G7MP_FUTURE_MACHINE_ATTEMPT_ID_INVALID"),
            (dict(record, grant_mint_consideration_permitted=False),
             "G7MP_GRANT_MINT_CONSIDERATION_PERMITTED_INVALID"),
            (dict(record, execution_authority="FULL"),
             "G7MP_EXECUTION_AUTHORITY_INVALID"),
            (dict(record, secret_material="PRESENT"),
             "G7MP_SECRET_MATERIAL_INVALID"),
            (dict(record, governance_event_id="OTHER-EVENT"),
             "G7MP_GOVERNANCE_EVENT_ID_INVALID"),
            (dict(record, auditor_role="AUDITOR_B"),
             "G7MP_AUDITOR_ROLE_INVALID"),
            (dict(record, attempt_slot="AUDITOR_A_REPLACEMENT_2"),
             "G7MP_ATTEMPT_SLOT_INVALID"),
            (dict(record, schema="AUCDEV-023-GRANT-MINT-PUBLICATION-V2"),
             "G7MP_SCHEMA_INVALID")):
        with pytest.raises(ri.ReceiptIdentityError, match=constant):
            ri.parse_g7_mint_publication(
                json.dumps(mutated, separators=(",", ":")).encode())
    duplicated = data.replace(
        b'"grant_identity":"' + identity.encode() + b'"',
        b'"grant_identity":"' + identity.encode()
        + b'","grant_identity":"' + identity.encode() + b'"')
    with pytest.raises(bab.BindingError):
        ri.parse_g7_mint_publication(duplicated)


def test_g7_selector_exact_one_and_five_value_identity(tmp_path):
    """C1-C15 happy path: exactly one qualifying introduction; the
    post-hoc FIVE-VALUE identity equals the actual Git facts (the same
    values the world's verified G7 context carries)."""
    world = _world(tmp_path, publish=False)
    tip = _git(world["repo"], "rev-parse", "HEAD").stdout.strip()
    selection = ri.select_canonical_g7_publication(world["repo"], tip, {
        "grant_identity": bab.grant_identity(world["grant"]),
        "g6_identity_set": G6_SET})
    assert selection["commit"] == world["g7_commit"]
    five = ri.derive_g7_post_publication_identity(selection)
    assert five == {key: world["context"][key] for key in five}
    assert five["grant_mint_publication_record_path"] == \
        bab.G7_MINT_PUBLICATION_RECORD_PATH
    wrong_g6 = dict(G6_SET,
                    package_binding_authority_readback_disposition="OTHER")
    for expected in ({"grant_identity": "e" * 64,
                      "g6_identity_set": G6_SET},
                     {"grant_identity": bab.grant_identity(
                         world["grant"]), "g6_identity_set": wrong_g6}):
        with pytest.raises(ri.ReceiptIdentityError,
                           match="CANONICAL_G7_MINT_PUBLICATION_NOT_FOUND"):
            ri.select_canonical_g7_publication(world["repo"], tip,
                                               expected)


@pytest.mark.parametrize("field,value", [
    ("schema", "AUCDEV-023-GRANT-MINT-PUBLICATION-V2"),        # C5
    ("grant_identity", "e" * 64),                              # C6
    ("grant_issued_evidence_path",
     "/synthetic/evidence-root/other.json"),                   # C7
    ("grant_issued_evidence_size", 0),                         # C7
    ("package_binding_authority_readback_disposition",
     "OTHER_DISPOSITION"),                                     # C8
    ("grant_mint_consideration_permitted", False),             # C9
    ("execution_authority", "FULL"),                           # C10
    ("secret_material", "PRESENT"),                            # C11
    ("governance_event_id", "OTHER-EVENT"),                    # C12
    ("auditor_role", "AUDITOR_B"),                             # C13
    ("attempt_slot", "AUDITOR_A_REPLACEMENT_2"),               # C14
])
def test_g7_selector_c5_through_c14_predicates(tmp_path, field, value):
    """Each C5-C14 predicate DISCRIMINATES: a record mutated on exactly
    that predicate never qualifies (NOT_FOUND, fail closed)."""
    identity = bab.grant_identity(synthetic_grant_bytes())
    record = _g7_record(identity)
    record[field] = value
    repo, _path = _publish_g7_only(tmp_path, record)
    tip = _git(repo, "rev-parse", "HEAD").stdout.strip()
    with pytest.raises(ri.ReceiptIdentityError,
                       match="CANONICAL_G7_MINT_PUBLICATION_NOT_FOUND"):
        ri.select_canonical_g7_publication(repo, tip, {
            "grant_identity": identity, "g6_identity_set": G6_SET})


def test_g7_selector_zero_delete_readd_and_modification(tmp_path):
    """Cardinality semantics: zero candidates -> NOT_FOUND; delete +
    re-add of the SAME qualifying record -> AMBIGUOUS; a later
    modification NEVER replaces the original introduction C."""
    identity = bab.grant_identity(synthetic_grant_bytes())
    expected = {"grant_identity": identity, "g6_identity_set": G6_SET}
    # zero: a seed-only repo has no G7 publication at all
    repo0 = Path(tmp_path) / "seedonly"
    repo0.mkdir(parents=True)
    _git(repo0, "init", "-q", "-b", "main")
    _git(repo0, "config", "user.email", "synthetic@test.invalid")
    _git(repo0, "config", "user.name", "synthetic")
    (repo0 / "seed.txt").write_bytes(b"SYNTHETIC-SEED")
    _commit_all(repo0, "seed")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="CANONICAL_G7_MINT_PUBLICATION_NOT_FOUND"):
        ri.select_canonical_g7_publication(
            repo0, "HEAD", expected)
    # delete + re-add -> two qualifying introductions -> AMBIGUOUS
    record = _g7_record(identity)
    repo, path = _publish_g7_only(tmp_path, record)
    payload = path.read_bytes()
    path.unlink()
    _commit_all(repo, "delete")
    path.write_bytes(payload)
    _commit_all(repo, "re-add same bytes")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="CANONICAL_G7_MINT_PUBLICATION_AMBIGUOUS"):
        ri.select_canonical_g7_publication(repo, "HEAD", expected)
    # modification never replaces the ORIGINAL introduction
    repo2, path2 = _publish_g7_only(tmp_path, record, name="g7repo2")
    original_commit = _git(repo2, "rev-parse", "HEAD").stdout.strip()
    path2.write_bytes(json.dumps(
        dict(record, grant_document_sha256="9" * 64),
        separators=(",", ":")).encode())
    _commit_all(repo2, "modify non-predicate field")
    selection = ri.select_canonical_g7_publication(repo2, "HEAD",
                                                   expected)
    assert selection["commit"] == original_commit
    assert selection["record"]["grant_document_sha256"] == \
        record["grant_document_sha256"]


def test_g7_selector_first_parent_domain_only(tmp_path):
    """C15: an introduction living ONLY on a side branch is NOT in the
    authoritative first-parent domain — selection over main FAILS
    CLOSED with NOT_FOUND (no side-branch reachability authority)."""
    identity = bab.grant_identity(synthetic_grant_bytes())
    repo = Path(tmp_path) / "repo"
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "synthetic@test.invalid")
    _git(repo, "config", "user.name", "synthetic")
    (repo / "seed.txt").write_bytes(b"SYNTHETIC-SEED")
    _commit_all(repo, "seed")
    _git(repo, "checkout", "-q", "-b", "side")
    path = repo.joinpath(*bab.G7_MINT_PUBLICATION_RECORD_PATH.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(_g7_record(identity),
                                separators=(",", ":")).encode())
    _commit_all(repo, "side-branch-only G7 publication")
    _git(repo, "checkout", "-q", "main")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="CANONICAL_G7_MINT_PUBLICATION_NOT_FOUND"):
        ri.select_canonical_g7_publication(repo, "HEAD", {
            "grant_identity": identity, "g6_identity_set": G6_SET})


# --- CR-IMPL-004: the authoritative (remote, branch) tip binding -------


def test_authoritative_ref_resolution_success_and_refusals(tmp_path):
    """resolve_authoritative_tip returns the exact remote tip and
    refuses a missing branch, an empty remote and an absent remote."""
    world = _world(tmp_path)
    binding = ri.resolve_authoritative_tip(world["repo"], world["remote"],
                                           world["branch"])
    assert binding["tip"] == _git(world["repo"], "rev-parse",
                                  "main").stdout.strip()
    assert binding["ref"] == "refs/heads/main"
    with pytest.raises(ri.ReceiptIdentityError,
                       match="AUTHORITATIVE_REF_NOT_RESOLVED"):
        ri.resolve_authoritative_tip(world["repo"], world["remote"],
                                     "nonexistent-branch")
    empty_world = _world(tmp_path / "empty", publish=False, push=False)
    with pytest.raises(ri.ReceiptIdentityError,
                       match="AUTHORITATIVE_REF_NOT_RESOLVED"):
        ri.resolve_authoritative_tip(empty_world["repo"],
                                     empty_world["remote"], "main")
    with pytest.raises(ri.ReceiptIdentityError,
                       match="SELECTOR_GIT_INVOCATION_FAILED"):
        ri.resolve_authoritative_tip(
            world["repo"], str(Path(tmp_path) / "absent.git"), "main")


def test_authoritative_ref_binds_remote_not_divergent_local(tmp_path):
    """A DIVERGENT local branch is never the authority: after local-only
    commits the binding (and G11's whole enumeration domain) stays the
    REMOTE tip; G11 still succeeds against the intact remote world."""
    world = _world(tmp_path)
    (world["repo"] / "local-only.txt").write_bytes(b"LOCAL-DIVERGENCE")
    _commit_all(world["repo"], "local-only divergence, never pushed")
    binding = ri.resolve_authoritative_tip(world["repo"], world["remote"],
                                           world["branch"])
    assert binding["tip"] != _git(world["repo"], "rev-parse",
                                  "HEAD").stdout.strip()
    out = ri.g11_independent_rederivation(world["context"],
                                          world["grant"],
                                          world["artifact"],
                                          world["repo"], world["remote"],
                                          world["branch"], G6_SET)
    assert out["authoritative_binding"] == binding


def test_unpushed_local_publication_is_not_authority(tmp_path):
    """A publication that exists ONLY locally is NOT authority: with the
    G10 publication committed but NOT pushed, the primitive selector
    over the local HEAD finds it, while the BOUND G10.6 readback /
    G11 (which enumerate the ls-remote remote tip only) FAIL CLOSED
    with NOT_FOUND — the authoritative-ref binding, not the caller's
    local ref, defines the domain."""
    world = _world(tmp_path, publish=False, push=True)
    ri.stage_receipt_identity_publication(world["repo"], world["data"])
    _commit_all(world["repo"], "local-only G10 publication, never pushed")
    selection = ri.select_canonical_g10_publication(
        world["repo"], "HEAD", world["record"])
    assert selection["commit"] == _git(world["repo"], "rev-parse",
                                       "HEAD").stdout.strip()
    for call in (
            lambda: ri.execute_g10_publication_readback(
                world["repo"], world["remote"], world["branch"],
                world["original"]),
            lambda: ri.g11_independent_rederivation(
                world["context"], world["grant"], world["artifact"],
                world["repo"], world["remote"], world["branch"], G6_SET)):
        with pytest.raises(ri.ReceiptIdentityError,
                           match="CANONICAL_G10_RECEIPT_IDENTITY_"
                                 "PUBLICATION_NOT_FOUND"):
            call()


def test_g11_g7_identity_independent_of_caller_context(tmp_path):
    """CR-IMPL-002 core: a caller-supplied context that is fully
    SHAPE-VALID (it parses cleanly) but whose G7 five-value identity
    does NOT equal the independently Git-derived identity is REFUSED —
    shape validation alone is never sufficient proof."""
    world = _world(tmp_path)
    forged = synthetic_g7_context(
        world["ns"], world["grant"],
        grant_mint_publication_commit_sha="a" * 40,
        grant_mint_publication_root_tree="b" * 40,
        grant_mint_publication_record_blob_sha1="c" * 40,
        grant_mint_publication_record_sha256="d" * 64)
    assert bab.parse_verified_g7_context(forged) == forged
    with pytest.raises(ri.ReceiptIdentityError,
                       match="G7_CONTEXT_IDENTITY_MISMATCH"):
        ri.g11_independent_rederivation(forged, world["grant"],
                                        world["artifact"], world["repo"],
                                        world["remote"], world["branch"],
                                        G6_SET)


# --- RI-AC matrix (criterion-by-criterion; each entry names the tests
# whose PASSING assertions establish the criterion) -----------------------

RI_AC_TESTS = {
    "RI-AC-01": ["test_g10_1_2_original_identity_derived_in_memory_only"],
    "RI-AC-02": ["test_g10_2_sha256_and_size_fixed_before_filesystem_trust"],
    "RI-AC-03": ["test_g10_2_sha256_and_size_fixed_before_filesystem_trust"],
    "RI-AC-04": ["test_g10_3_accepted_one_shot_writer_reused_unchanged"],
    "RI-AC-05": ["test_g10_4_readback_equality_and_writer_return"],
    "RI-AC-06": ["test_g10_4_readback_equality_and_writer_return",
                 "test_g10_4_refuses_mutated_receipt_window"],
    "RI-AC-07": ["test_g10_4_readback_equality_and_writer_return",
                 "test_g10_4_refuses_mutated_receipt_window"],
    "RI-AC-08": ["test_g10_4_readback_equality_and_writer_return",
                 "test_g10_4_refuses_mutated_receipt_window"],
    "RI-AC-09": ["test_reserved_publication_path_absent_in_live_repo"],
    "RI-AC-10": ["test_publication_schema_closed_world",
                 "test_publication_field_shape_gates",
                 "test_publication_exact_value_gates"],
    "RI-AC-11": ["test_publication_field_order_normative"],
    "RI-AC-12": ["test_publication_canonical_serialization_deterministic",
                 "test_publication_noncanonical_bytes_refused"],
    "RI-AC-13": ["test_no_self_git_identity_in_record"],
    "RI-AC-14": ["test_dependency_graph_acyclic"],
    "RI-AC-15": ["test_selector_first_parent_domain_only"],
    "RI-AC-16": ["test_selector_merge_introduction_ineligible"],
    "RI-AC-17": ["test_selector_tree_state_probes"],
    "RI-AC-18": ["test_selector_tree_state_probes"],
    "RI-AC-19": ["test_selector_raw_add_classification",
                 "test_selector_rename_presentation_invariance"],
    "RI-AC-20": ["test_selector_rename_presentation_invariance"],
    "RI-AC-21": ["test_selector_tree_state_contradiction_defensive"],
    "RI-AC-22": ["test_selector_exact_one_cardinality"],
    "RI-AC-23": ["test_selector_zero_candidates_not_found"],
    "RI-AC-24": ["test_selector_delete_readd_ambiguous"],
    "RI-AC-25": ["test_selector_modification_never_replaces_R"],
    "RI-AC-26": ["test_selector_no_package_provided_authority"],
    "RI-AC-27": ["test_selector_delete_readd_ambiguous"],
    "RI-AC-28": ["test_g10_6_readback_requires_exact_publication_bytes"],
    "RI-AC-29": ["test_g10_6_post_push_current_receipt_equality"],
    "RI-AC-30": ["test_g11_independent_rederivation_success",
                 "test_g11_refuses_grant_substitution"],
    "RI-AC-31": ["test_g11_refuses_byte_flip_same_size"],
    "RI-AC-32": ["test_g11_refuses_truncation_and_append"],
    "RI-AC-33": ["test_g11_refuses_grant_substitution",
                 "test_g11_refuses_g7_and_crossbinding_substitution"],
    "RI-AC-34": ["test_g11_refuses_package_b_substitution"],
    "RI-AC-35": ["test_g11_refuses_g7_and_crossbinding_substitution"],
    "RI-AC-36": ["test_g11_refuses_namespace_replacement"],
    "RI-AC-37": ["test_grant_and_receipt_schemas_unchanged"],
    "RI-AC-38": ["test_public_surface_and_execution_authority_nonexpansion"],
    "RI-AC-39": ["test_accountingstore_unused_and_stage_nonexpansion"],
    "RI-AC-40": ["test_accountingstore_unused_and_stage_nonexpansion"],
    "RI-AC-41": ["test_public_surface_and_execution_authority_nonexpansion",
                 "test_publication_flags_exact"],
    "RI-AC-42": ["test_grant_and_receipt_schemas_unchanged"],
    "RI-AC-43": ["test_publication_flags_exact"],
    "RI-AC-44": ["test_mutation_class_matrix",
                 "test_g11_refuses_truncation_and_append",
                 "test_g11_refuses_deletion",
                 "test_g11_accepts_byte_identical_new_inode",
                 "test_g11_refuses_namespace_replacement"],
}


def test_ri_ac_matrix_complete_and_mapped():
    assert set(RI_AC_TESTS) == {f"RI-AC-{n:02d}" for n in range(1, 45)}
    for criterion, tests in RI_AC_TESTS.items():
        assert tests, criterion
        for name in tests:
            assert callable(globals().get(name)), (criterion, name)
