"""AUCDEV-023 PCH6-B TRUSTROOT-001 P3 lifecycle caller — synthetic
acceptance tests (disposable worlds; non-secret bytes only).

Covers GAP B trust root T1-T8 (record A 8b31d8e5 Section 5), GAP A G6
Layer-1/K1-K14/layer-2 (Section 4), GRANT_ISSUED evidence verification
(R-EVID), GAP C handoff content identity (Section 6), and the glue.
No operative lifecycle data is ever touched."""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

LC_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LC_ROOT.parents[0]
if str(LC_ROOT) not in sys.path:
    sys.path.insert(0, str(LC_ROOT))

sys.dont_write_bytecode = True   # never leave bytecode in the frozen tree
import lifecycle_caller as lc  # noqa: E402

CONFIG_FIELDS = ("schema", "canonical_owner", "canonical_repository",
                 "canonical_provider_repository_id", "canonical_remote_url",
                 "expected_default_branch", "trust_anchor_commit",
                 "transport_mode")

CANONICAL_CONFIG = {
    "schema": "AUCDEV-023-LIFECYCLE-CALLER-TRUST-ROOT-CONFIG-V1",
    "canonical_owner": "isakli05",
    "canonical_repository": "audit-council-dev",
    "canonical_provider_repository_id": "1358379094",
    "canonical_remote_url": "https://github.com/isakli05/audit-council-dev.git",
    "expected_default_branch": "master",
    "trust_anchor_commit": "3058868416241d394cfaaa40cc585085db486f37",
    "transport_mode": "HTTPS_TLS_NO_REDIRECT",
}


def canon_bytes(doc, fields):
    return json.dumps({k: doc[k] for k in fields},
                      separators=(",", ":")).encode()


def write_config(tmp_path, doc, *, raw=None, name="trust-root.json"):
    p = tmp_path / name
    p.write_bytes(raw if raw is not None else canon_bytes(doc, CONFIG_FIELDS))
    return p


def git(cwd, *args, check=True):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    out = subprocess.run(("git", "-C", str(cwd), *args), capture_output=True,
                         env=env)
    if check and out.returncode != 0:
        raise AssertionError(out.stderr.decode())
    return out.stdout.decode()


def build_world(tmp_path, commits):
    """Disposable synthetic git world: list of (message, {path: bytes})."""
    repo = tmp_path / "world"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "master")
    for msg, files in commits:
        for rel, data in files.items():
            target = repo / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data if isinstance(data, bytes)
                               else data.encode())
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", msg)
    return repo


LS_REMOTE_OK = ("ref: refs/heads/master\tHEAD\n"
                "0123456789abcdef0123456789abcdef01234567\tHEAD\n"
                "0123456789abcdef0123456789abcdef01234567\trefs/heads/master\n")
TIP = "0123456789abcdef0123456789abcdef01234567"


def api_result(tip=TIP, **over):
    result = {"full_name": "isakli05/audit-council-dev",
              "id": 1358379094, "default_branch": "master", "tip": tip}
    result.update(over)
    return result


class ApiDouble:
    """Queue of per-call results (each call pops; single result = all
    calls see it)."""

    def __init__(self, *results, **over):
        self.results = list(results) or [api_result(**over)]
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        return dict(self.results.pop(0) if len(self.results) > 1
                    else self.results[0])


class TransportDouble:
    def __init__(self, texts):
        self.texts = list(texts)
        self.calls = []

    def __call__(self, url, branch):
        self.calls.append((url, branch))
        return self.texts.pop(0)


# ---------------------------------------------------------------- config

def test_config_accepts_canonical_bytes(tmp_path):
    cfg = write_config(tmp_path, CANONICAL_CONFIG)
    assert lc.load_trust_root_config(cfg, REPO_ROOT) == CANONICAL_CONFIG


def test_tracked_example_file_is_non_authority():
    example = LC_ROOT / "trust-root-config.example.json"
    assert example.read_bytes() == canon_bytes(CANONICAL_CONFIG, CONFIG_FIELDS)
    # the in-repository example NEVER loads as an operative config source
    # (record A 5.1 circularity guard: the repo cannot vouch for itself)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.load_trust_root_config(example, REPO_ROOT)
    assert ei.value.code == lc.TRUST_ROOT_CONFIG_SOURCE_REFUSED


def test_config_source_refused_when_relative(tmp_path):
    cfg = write_config(tmp_path, CANONICAL_CONFIG)
    rel = Path(os.path.relpath(cfg, tmp_path))
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.load_trust_root_config(rel, REPO_ROOT)
    assert ei.value.code == lc.TRUST_ROOT_CONFIG_SOURCE_REFUSED


def test_config_source_refused_inside_repository(tmp_path):
    inside = REPO_ROOT / "lifecycle-caller" / "in-repo-config.json"
    inside.write_bytes(canon_bytes(CANONICAL_CONFIG, CONFIG_FIELDS))
    try:
        with pytest.raises(lc.LifecycleCallerError) as ei:
            lc.load_trust_root_config(inside, REPO_ROOT)
        assert ei.value.code == lc.TRUST_ROOT_CONFIG_SOURCE_REFUSED
    finally:
        inside.unlink()


def test_config_unavailable(tmp_path):
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.load_trust_root_config(tmp_path / "absent.json", REPO_ROOT)
    assert ei.value.code == lc.TRUST_ROOT_CONFIG_UNAVAILABLE


@pytest.mark.parametrize("field,value", [
    ("schema", "AUCDEV-023-TRUST-ROOT-CONFIG-V2"),
    ("canonical_owner", "attacker"),
    ("canonical_repository", "audit-council-decoy"),
    ("canonical_provider_repository_id", "1358379095"),
    ("canonical_remote_url", "http://github.com/isakli05/audit-council-dev.git"),
    ("canonical_remote_url", "https://github.com/isakli05/decoy.git"),
    ("expected_default_branch", "main"),
    ("expected_default_branch", "feature-x"),
    ("trust_anchor_commit", "ffffffffffffffffffffffffffffffffffffffff"),
    ("trust_anchor_commit", "not-hex"),
    ("transport_mode", "SSH_HOSTKEY_PINNED"),
])
def test_config_invalid_values(tmp_path, field, value):
    doc = dict(CANONICAL_CONFIG)
    doc[field] = value
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.load_trust_root_config(write_config(tmp_path, doc), REPO_ROOT)
    assert ei.value.code == lc.TRUST_ROOT_CONFIG_INVALID


def test_config_non_canonical_bytes(tmp_path):
    doc = dict(CANONICAL_CONFIG)
    raw = canon_bytes(doc, CONFIG_FIELDS) + b"\n"
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.load_trust_root_config(write_config(tmp_path, doc, raw=raw),
                                  REPO_ROOT)
    assert ei.value.code == lc.TRUST_ROOT_CONFIG_INVALID
    reordered = json.dumps({k: doc[k] for k in reversed(CONFIG_FIELDS)},
                           separators=(",", ":")).encode()
    with pytest.raises(lc.LifecycleCallerError):
        lc.load_trust_root_config(
            write_config(tmp_path, doc, raw=reordered, name="r.json"),
            REPO_ROOT)


def test_config_duplicate_key_refused(tmp_path):
    base = canon_bytes(CANONICAL_CONFIG, CONFIG_FIELDS)
    dup = base[:-1] + b',"canonical_owner":"other"}'
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.load_trust_root_config(
            write_config(tmp_path, CANONICAL_CONFIG, raw=dup, name="d.json"),
            REPO_ROOT)
    assert ei.value.code == lc.TRUST_ROOT_CONFIG_INVALID


def test_config_closed_world(tmp_path):
    extra = json.dumps({**CANONICAL_CONFIG, "extra": "x"},
                       separators=(",", ":")).encode()
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.load_trust_root_config(
            write_config(tmp_path, CANONICAL_CONFIG, raw=extra,
                         name="e.json"), REPO_ROOT)
    assert ei.value.code == lc.TRUST_ROOT_CONFIG_INVALID
    missing = json.dumps({k: v for k, v in CANONICAL_CONFIG.items()
                          if k != "transport_mode"},
                         separators=(",", ":")).encode()
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.load_trust_root_config(
            write_config(tmp_path, CANONICAL_CONFIG, raw=missing,
                         name="m.json"), REPO_ROOT)
    assert ei.value.code == lc.TRUST_ROOT_CONFIG_INVALID


def test_canonical_json_shape():
    doc = {"b": 1, "a": "x"}
    out = lc._canonical_json(doc, ("b", "a"))
    assert out == b'{"b":1,"a":"x"}'
    assert not out.endswith(b"\n")


# ---------------------------------------------------- ls-remote parsing

def test_parse_ls_remote_canonical():
    symref, tip = lc._parse_ls_remote(LS_REMOTE_OK, "master")
    assert symref == "refs/heads/master" and tip == TIP


def test_parse_ls_remote_default_branch_mismatch():
    text = LS_REMOTE_OK.replace("refs/heads/master", "refs/heads/feature")
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc._parse_ls_remote(text, "master")
    assert ei.value.code == lc.DEFAULT_BRANCH_MISMATCH


def test_parse_ls_remote_no_symref():
    text = f"{TIP}\trefs/heads/master\n"
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc._parse_ls_remote(text, "master")
    assert ei.value.code == lc.DEFAULT_BRANCH_MISMATCH


def test_parse_ls_remote_absent_ref():
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc._parse_ls_remote("ref: refs/heads/master\tHEAD\n", "master")
    assert ei.value.code == lc.AUTHORITATIVE_REF_NOT_RESOLVED


def test_parse_ls_remote_malformed_row():
    text = ("ref: refs/heads/master\tHEAD\n"
            "nothex\trefs/heads/master\n")
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc._parse_ls_remote(text, "master")
    assert ei.value.code == lc.AUTHORITATIVE_REF_NOT_RESOLVED


def test_parse_ls_remote_ambiguous_rows():
    text = LS_REMOTE_OK + f"{TIP[:-1]}1\trefs/heads/master\n"
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc._parse_ls_remote(text, "master")
    assert ei.value.code == lc.AUTHORITATIVE_REF_AMBIGUOUS


def test_parse_ls_remote_head_disagrees_with_branch():
    text = LS_REMOTE_OK.replace(
        f"{TIP}\tHEAD", f"{'a' * 40}\tHEAD")
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc._parse_ls_remote(text, "master")
    assert ei.value.code == lc.AUTHORITATIVE_REF_AMBIGUOUS


# ------------------------------------------------------- trust root T1-T8

REAL_ANCHOR = "3058868416241d394cfaaa40cc585085db486f37"


@pytest.fixture(scope="session")
def anchor_template(tmp_path_factory):
    """One world whose first-parent history genuinely descends from the
    REAL canonical trust anchor (objects imported read-only from the
    live repository under a hidden ref); per-test worlds are cheap
    shared clones of this template."""
    repo = tmp_path_factory.mktemp("anchor-template") / "template"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "master")
    git(repo, "fetch", "-q", str(REPO_ROOT),
        "+refs/heads/master:refs/hidden/canonical")
    (repo / "seed.txt").write_bytes(b"seed")
    git(repo, "add", "-A")
    tree = git(repo, "write-tree").strip()
    tip = git(repo, "commit-tree", tree, "-p", REAL_ANCHOR,
              "-m", "synthetic tip").strip()
    git(repo, "update-ref", "refs/heads/master", tip)
    return repo


def build_anchor_world(tmp_path, template):
    repo = tmp_path / "aworld"
    out = subprocess.run(("git", "clone", "-q", "--shared",
                          str(template), str(repo)), capture_output=True)
    assert out.returncode == 0, out.stderr
    return repo, git(repo, "rev-parse", "HEAD").strip()


def _local_world(tmp_path, anchor_template):
    repo, tip = build_anchor_world(tmp_path, anchor_template)
    cfg = write_config(tmp_path, CANONICAL_CONFIG, name="cfg.json")
    remote = LS_REMOTE_OK.replace(TIP, tip)
    return repo, cfg, tip, remote


def test_trust_root_b0_canonical_success(tmp_path, anchor_template):
    repo, cfg, tip, remote = _local_world(tmp_path, anchor_template)
    api = ApiDouble(tip=tip)
    transport = TransportDouble([remote, remote])
    had_package = "bootstrap_authority" in sys.modules
    binding = lc.verify_trust_root(cfg, repo, ls_remote=transport,
                                   api_read=api)
    assert binding["authoritative_tip"] == tip
    assert binding["canonical_provider_repository_id"] == "1358379094"
    assert binding["config_source_path"] == str(cfg.resolve())
    # trust-root verification itself imports no package module
    assert ("bootstrap_authority" in sys.modules) == had_package
    assert transport.calls == [(CANONICAL_CONFIG["canonical_remote_url"],
                                "master")] * 2          # B4: exact URL only


def test_trust_root_b1_same_anchor_decoy_repository(tmp_path, anchor_template):
    repo, cfg, tip, remote = _local_world(tmp_path, anchor_template)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_trust_root(cfg, repo,
                             ls_remote=TransportDouble([remote] * 2),
                             api_read=ApiDouble(tip=tip, id=1358379095))
    assert ei.value.code == lc.IDENTITY_DISAGREEMENT_REFUSED


def test_trust_root_b2_alternate_owner_name(tmp_path, anchor_template):
    repo, cfg, tip, remote = _local_world(tmp_path, anchor_template)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_trust_root(cfg, repo,
                             ls_remote=TransportDouble([remote] * 2),
                             api_read=ApiDouble(
                                 tip=tip,
                                 full_name="attacker/audit-council-dev"))
    assert ei.value.code == lc.IDENTITY_DISAGREEMENT_REFUSED


def test_trust_root_b5_api_disagreement_per_field(tmp_path, anchor_template):
    repo, cfg, tip, remote = _local_world(tmp_path, anchor_template)
    for over in ({"default_branch": "main"}, {"tip": "b" * 40}):
        with pytest.raises(lc.LifecycleCallerError) as ei:
            lc.verify_trust_root(
                cfg, repo, ls_remote=TransportDouble([remote] * 2),
                api_read=ApiDouble(api_result(**{**{"tip": tip},
                                                  **over})))
        assert ei.value.code == lc.IDENTITY_DISAGREEMENT_REFUSED


def test_trust_root_b6_tip_moves_during_verification(tmp_path, anchor_template):
    repo, cfg, tip, remote = _local_world(tmp_path, anchor_template)
    moved = remote.replace(tip, "c" * 40)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_trust_root(
            cfg, repo,
            ls_remote=TransportDouble([remote, moved]),
            api_read=ApiDouble(api_result(tip), api_result("c" * 40)))
    assert ei.value.code == lc.AUTHORITATIVE_TIP_MOVED_DURING_VERIFICATION


def test_trust_root_b6_api_tip_moves(tmp_path, anchor_template):
    repo, cfg, tip, remote = _local_world(tmp_path, anchor_template)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_trust_root(
            cfg, repo, ls_remote=TransportDouble([remote, remote]),
            api_read=ApiDouble(api_result(tip), api_result("d" * 40)))
    assert ei.value.code == lc.AUTHORITATIVE_TIP_MOVED_DURING_VERIFICATION


def test_trust_root_b7_tip_not_a_local_commit(tmp_path, anchor_template):
    repo, cfg, tip, remote = _local_world(tmp_path, anchor_template)
    absent = remote.replace(tip, "e" * 40)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_trust_root(
            cfg, repo, ls_remote=TransportDouble([absent] * 2),
            api_read=ApiDouble(tip="e" * 40))
    assert ei.value.code == lc.AUTHORITATIVE_TIP_NOT_A_LOCAL_COMMIT


def test_trust_root_anchor_not_ancestor(tmp_path):
    repo = build_world(tmp_path, [("a", {"x": b"1"})])  # anchor not present
    tip = git(repo, "rev-parse", "HEAD").strip()
    cfg = write_config(tmp_path, CANONICAL_CONFIG, name="cfg2.json")
    remote = LS_REMOTE_OK.replace(TIP, tip)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_trust_root(cfg, repo,
                             ls_remote=TransportDouble([remote] * 2),
                             api_read=ApiDouble(tip=tip))
    assert ei.value.code == lc.TRUST_ANCHOR_NOT_ANCESTOR


# ================================================ GAP A: G6 publication
G5_PATH = ("docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-"
           "REPLACEMENT-AUDITOR-A-PACKAGE-BINDING-AUTHORITY.md")
G6_PATH = G5_PATH[:-3] + "-READBACK-PUBLICATION.md"
G7_PATH = ("docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-"
           "REPLACEMENT-AUDITOR-A-GRANT-MINT-PUBLICATION.md")
PKG_DIR = REPO_ROOT / "bootstrap-authority"
GRANT_ID = "a" * 64


def pkg_files():
    return {str(p.relative_to(PKG_DIR)): p.read_bytes()
            for p in PKG_DIR.rglob("*") if p.is_file()}


def g6_doc(g5, **over):
    doc = {
        "schema": "AUCDEV-023-PACKAGE-BINDING-AUTHORITY-READBACK-PUBLICATION-V1",
        "publication_semantics": "NON_EXECUTION_CONTROL_ROOM_READBACK_RECORD",
        "governance_event_id": "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01",
        "auditor_role": "AUDITOR_A",
        "attempt_slot": "AUDITOR_A_REPLACEMENT_1",
        "readback_authority_id": "TEST-G6-AUTHORITY-001",
        "package_binding_authority_target_commit_sha": g5["commit"],
        "package_binding_authority_target_record_path": g5["record_path"],
        "package_binding_authority_target_record_blob_sha1": g5["record_blob_sha1"],
        "package_binding_authority_target_record_sha256": g5["record_sha256"],
        "package_binding_authority_readback_disposition":
            "PERMIT_GRANT_MINT_CONSIDERATION",
        "grant_mint_consideration_permitted": True,
        "execution_authority": "NONE",
        "auditor_b_authority": "NONE",
        "secret_material": "NONE"}
    doc.update(over)
    return doc


def g6_bytes(doc):
    return json.dumps({k: doc[k] for k in lc.G6_LAYER1_FIELDS},
                      separators=(",", ":")).encode()


def commit_files(repo, files, msg):
    for rel, data in files.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data if isinstance(data, bytes)
                           else data.encode())
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg)


def tree_identity(repo, path):
    row = git(repo, "ls-tree", "HEAD", "--", path).split("\t")
    return row[0].split()[2]


def commit_g5(repo, content=b"G5 publication record\n"):
    commit_files(repo, {G5_PATH: content}, "g5")
    return {"commit": git(repo, "rev-parse", "HEAD").strip(),
            "record_path": G5_PATH,
            "record_blob_sha1": tree_identity(repo, G5_PATH),
            "record_sha256": hashlib.sha256(content).hexdigest()}


def commit_g6(repo, g5, **over):
    commit_files(repo, {G6_PATH: g6_bytes(g6_doc(g5, **over))}, "g6")


@pytest.fixture(scope="session")
def pkg_blob_files():
    return pkg_files()


def _gated(repo):
    """Run the FULL import gate for this world (blob pin + census),
    then return its tip — selector reuse is reachable only after it."""
    tip = git(repo, "rev-parse", "HEAD").strip()
    lc.import_verified_package(repo, tip, repo / "bootstrap-authority")
    return tip


def build_g6_world(tmp_path, pkg_blob_files, *, g5=True, g6=True,
                   g6_over=None, g6_twice=False, g5_first=True,
                   g6_before_g5=False):
    repo = tmp_path / "g6world"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "master")
    commit_files(repo, {f"bootstrap-authority/{rel}": data for rel, data
                        in pkg_blob_files.items()}, "package")
    g5_id = None
    if g6_before_g5:
        assert g6 and g5
        commit_g6(repo, {"commit": "0" * 40, "record_path": G5_PATH,
                         "record_blob_sha1": "0" * 40,
                         "record_sha256": "0" * 64}, **(g6_over or {}))
        g5_id = commit_g5(repo)
        return repo, git(repo, "rev-parse", "HEAD").strip(), g5_id
    if g5:
        g5_id = commit_g5(repo)
    if g6:
        over = dict(g6_over or {})
        g5_id = g5_id or {"commit": "0" * 40, "record_path": G5_PATH,
                          "record_blob_sha1": "0" * 40,
                          "record_sha256": "0" * 64}
        if g6_twice:
            commit_g6(repo, g5_id, **over)
            git(repo, "rm", "-q", G6_PATH)
            git(repo, "commit", "-q", "-m", "remove g6")
            commit_g6(repo, g5_id, **over)
        else:
            commit_g6(repo, g5_id, **over)
    return repo, git(repo, "rev-parse", "HEAD").strip(), g5_id


def g6_parse_ok(g5):
    return lc.parse_g6_publication(g6_bytes(g6_doc(g5)))


def test_g6_parser_canonical():
    g5 = {"commit": "1" * 40, "record_path": G5_PATH,
          "record_blob_sha1": "2" * 40, "record_sha256": "3" * 64}
    parsed = g6_parse_ok(g5)
    assert parsed["readback_authority_id"] == "TEST-G6-AUTHORITY-001"
    assert list(parsed) == list(lc.G6_LAYER1_FIELDS)


@pytest.mark.parametrize("over,code", [
    ({"schema": "...-V2"}, lc.G6_LAYER1_INVALID),
    ({"publication_semantics": "EXECUTION"}, lc.G6_LAYER1_INVALID),
    ({"governance_event_id": "OTHER-EVENT"}, lc.G6_LAYER1_INVALID),
    ({"auditor_role": "AUDITOR_B"}, lc.G6_LAYER1_INVALID),
    ({"attempt_slot": "AUDITOR_A_REPLACEMENT_2"}, lc.G6_LAYER1_INVALID),
    ({"readback_authority_id": ""}, lc.G6_LAYER1_INVALID),
    ({"package_binding_authority_target_commit_sha": "xyz"}, lc.G6_LAYER1_INVALID),
    ({"package_binding_authority_target_record_path": G5_PATH + "x"},
     lc.G6_LAYER1_INVALID),
    ({"package_binding_authority_target_record_blob_sha1": "z" * 40},
     lc.G6_LAYER1_INVALID),
    ({"package_binding_authority_target_record_sha256": "q" * 64},
     lc.G6_LAYER1_INVALID),
    ({"package_binding_authority_readback_disposition": "ALLOW"},
     lc.G6_LAYER1_INVALID),
    ({"grant_mint_consideration_permitted": "true"},
     lc.G6_LAYER1_INVALID),
    ({"execution_authority": "SOME"}, lc.G6_LAYER1_INVALID),
    ({"auditor_b_authority": "SOME"}, lc.G6_LAYER1_INVALID),
    ({"secret_material": "SOME"}, lc.G6_LAYER1_INVALID),
])
def test_g6_parser_field_refusals(over, code):
    g5 = {"commit": "1" * 40, "record_path": G5_PATH,
          "record_blob_sha1": "2" * 40, "record_sha256": "3" * 64}
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.parse_g6_publication(g6_bytes(g6_doc(g5, **over)))
    assert ei.value.code == code


def test_g6_parser_coherence_refused():
    g5 = {"commit": "1" * 40, "record_path": G5_PATH,
          "record_blob_sha1": "2" * 40, "record_sha256": "3" * 64}
    bad = g6_doc(g5, package_binding_authority_readback_disposition="REFUSE",
                 grant_mint_consideration_permitted=True)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.parse_g6_publication(g6_bytes(bad))
    assert ei.value.code == lc.G6_LAYER1_INVALID
    with pytest.raises(lc.LifecycleCallerError):
        lc.parse_g6_publication(g6_bytes(
            g6_doc(g5, grant_mint_consideration_permitted=False)))


def test_g6_parser_non_canonical_bytes():
    g5 = {"commit": "1" * 40, "record_path": G5_PATH,
          "record_blob_sha1": "2" * 40, "record_sha256": "3" * 64}
    raw = g6_bytes(g6_doc(g5))
    reordered = json.dumps(
        {k: g6_doc(g5)[k] for k in reversed(lc.G6_LAYER1_FIELDS)},
        separators=(",", ":")).encode()
    for mutated in (raw + b"\n", raw.replace(b",", b", "), reordered):
        with pytest.raises(lc.LifecycleCallerError):
            lc.parse_g6_publication(mutated)
    with pytest.raises(lc.LifecycleCallerError):
        lc.parse_g6_publication(raw[:-1] + b',"schema":"x"}')


# ------------------------------------------- canonical G6 selection
def test_g6_selection_a1_favorable(tmp_path, pkg_blob_files):
    repo, tip, g5_id = build_g6_world(tmp_path, pkg_blob_files)
    ri = lc.import_verified_package(repo, tip, repo / "bootstrap-authority")
    selection = lc.select_canonical_g6_publication(repo, tip)
    layer2 = lc.derive_g6_layer2(selection)
    assert list(layer2) == list(ri.G6_IDENTITY_FIELDS)
    assert layer2[ri.G6_IDENTITY_FIELDS[0]] == selection["commit"]
    assert layer2["package_binding_authority_readback_target_commit_sha"] \
        == g5_id["commit"]
    assert layer2["grant_mint_consideration_permitted"] is True


@pytest.mark.parametrize("disposition", ["REFUSE", "BLOCK",
                                         "REMEDIATION_REQUIRED"])
def test_g6_selection_a2_adverse_first_class(tmp_path, pkg_blob_files,
                                              disposition):
    repo, tip, _ = build_g6_world(
        tmp_path, pkg_blob_files,
        g6_over={"package_binding_authority_readback_disposition": disposition,
                 "grant_mint_consideration_permitted": False})
    tip = _gated(repo)
    selection = lc.select_canonical_g6_publication(repo, tip)
    layer2 = lc.derive_g6_layer2(selection)
    assert layer2["package_binding_authority_readback_disposition"] \
        == disposition
    assert layer2["grant_mint_consideration_permitted"] is False


def test_g6_selection_a3_missing(tmp_path, pkg_blob_files):
    repo, tip, _ = build_g6_world(tmp_path, pkg_blob_files, g6=False)
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND


def test_g6_selection_g5_unresolvable(tmp_path, pkg_blob_files):
    repo, tip, _ = build_g6_world(tmp_path, pkg_blob_files, g5=False)
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.G5_TARGET_NOT_RESOLVABLE


def test_g6_selection_a4_stale_g5_introduced_later(tmp_path, pkg_blob_files):
    repo, tip, _ = build_g6_world(tmp_path, pkg_blob_files,
                                  g6_before_g5=True)
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.G6_STALE_REFUSED


def test_g6_selection_a4_stale_target_drift(tmp_path, pkg_blob_files):
    repo, tip, g5_id = build_g6_world(
        tmp_path, pkg_blob_files,
        g6_over={"package_binding_authority_target_record_blob_sha1":
                 "9" * 40})
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.G6_STALE_REFUSED


def test_g6_selection_a5_republished_ambiguous(tmp_path, pkg_blob_files):
    repo, tip, _ = build_g6_world(tmp_path, pkg_blob_files, g6_twice=True)
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.CANONICAL_G6_READBACK_PUBLICATION_AMBIGUOUS


def test_g6_selection_a6_g5_path_confusion(tmp_path, pkg_blob_files):
    # G6-shaped bytes at the G5 path; nothing at the G6 path
    repo = tmp_path / "confused"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "master")
    commit_files(repo, {f"bootstrap-authority/{rel}": data for rel, data
                        in pkg_blob_files.items()}, "package")
    g5_id = commit_g5(repo, g6_bytes(g6_doc(
        {"commit": "1" * 40, "record_path": G5_PATH,
         "record_blob_sha1": "2" * 40, "record_sha256": "3" * 64})))
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND


def test_g6_selection_a7_noncanonical_original(tmp_path, pkg_blob_files):
    # the introduction itself carries non-canonical bytes: K5 fails the
    # record as non-qualifying and selection finds NOTHING (fail closed)
    repo, tip, g5_id = build_g6_world(tmp_path, pkg_blob_files, g6=False)
    spaced = g6_bytes(g6_doc(g5_id)).replace(b",", b", ")
    commit_files(repo, {G6_PATH: spaced}, "g6 noncanonical")
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND


def test_g6_selection_a8_incoherent_record(tmp_path, pkg_blob_files):
    repo, tip, _ = build_g6_world(
        tmp_path, pkg_blob_files,
        g6_over={"grant_mint_consideration_permitted": True,
                 "package_binding_authority_readback_disposition": "REFUSE"})
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND


def test_g6_selection_a9_merge_introduced(tmp_path, pkg_blob_files):
    repo, tip, g5_id = build_g6_world(tmp_path, pkg_blob_files, g6=False)
    git(repo, "checkout", "-q", "-b", "side")
    commit_g6(repo, g5_id)
    git(repo, "checkout", "-q", "master")
    git(repo, "merge", "-q", "--no-ff", "-m", "merge g6", "side")
    tip = _gated(repo)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(repo, tip)
    assert ei.value.code == lc.CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND


def test_g6_selection_a10_no_caller_supplied_expected_set():
    import inspect
    params = inspect.signature(
        lc.select_canonical_g6_publication).parameters
    assert list(params) == ["repo", "tip"]


def test_g6_selection_a4_current_g5_modified_after_g6(tmp_path,
                                                      pkg_blob_files):
    repo, tip, g5_id = build_g6_world(tmp_path, pkg_blob_files)
    commit_files(repo, {G5_PATH: b"G5 publication record v2\n"}, "g5 edit")
    tip = _gated(repo)
    selection = lc.select_canonical_g6_publication(repo, tip)
    assert selection["record"]["package_binding_authority_target_commit_sha"] \
        == g5_id["commit"]


# ------------------------------------- GRANT_ISSUED evidence (R-EVID)
def evidence_doc(g6_layer2, grant_identity=GRANT_ID):
    return {"schema": "AUCDEV-023-GRANT-ISSUED-EVIDENCE-V1",
            "evidence_semantics":
                "IMMUTABLE_NON_EXECUTION_GRANT_ISSUED_EVIDENCE",
            "governance_event_id": "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01",
            "auditor_role": "AUDITOR_A",
            "attempt_slot": "AUDITOR_A_REPLACEMENT_1",
            "future_machine_attempt_id": "FUTURE-ATTEMPT-ID",
            "grant_identity": grant_identity,
            "grant_document_sha256": "b" * 64,
            **{name: g6_layer2[name]
               for name in ("package_binding_authority_readback_commit_sha",
                            "package_binding_authority_readback_root_tree",
                            "package_binding_authority_readback_record_path",
                            "package_binding_authority_readback_record_blob_sha1",
                            "package_binding_authority_readback_record_sha256",
                            "package_binding_authority_readback_target_commit_sha",
                            "package_binding_authority_readback_disposition")},
            "grant_mint_consideration_permitted": True,
            "execution_authority": "NONE",
            "secret_material": "NONE"}


def g7_record_doc(layer2, *, gid=GRANT_ID, pinned_bytes=b"",
                  size_delta=0, path_override=None, evidence_root=None):
    """The canonical 21-field G7 mint record payload (synthetic)."""
    return {
        "schema": "AUCDEV-023-GRANT-MINT-PUBLICATION-V1",
        "governance_event_id": "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01",
        "auditor_role": "AUDITOR_A",
        "attempt_slot": "AUDITOR_A_REPLACEMENT_1",
        "future_machine_attempt_id": "FUTURE-ATTEMPT-ID",
        "grant_identity": gid,
        "grant_document_sha256": "b" * 64,
        "grant_issued_evidence_path": path_override or str(
            evidence_root / f"grant-issued-{gid}.json"),
        "grant_issued_evidence_sha256": hashlib.sha256(
            pinned_bytes).hexdigest(),
        "grant_issued_evidence_size": len(pinned_bytes) + size_delta}


def build_evidence_world(tmp_path, pkg_blob_files, *, evidence=True,
                         mutate=None, size_delta=0, path_override=None,
                         other_grant=False, doc_mutate=None,
                         pin_mutated=False):
    """doc_mutate: mutate the 18-field semantic document BEFORE
    serialization; pin_mutated: the G7 record pins the POST-mutation
    bytes (the T55 form — byte checks pass, semantics must catch)."""
    repo, tip, g5_id = build_g6_world(tmp_path, pkg_blob_files)
    lc.import_verified_package(repo, tip, repo / "bootstrap-authority")
    selection = lc.select_canonical_g6_publication(repo, tip)
    layer2 = lc.derive_g6_layer2(selection)
    gid = "c" * 64 if other_grant else GRANT_ID
    doc = evidence_doc(layer2, gid)
    if doc_mutate is not None:
        doc = doc_mutate(doc)
    pinned_bytes = json.dumps(doc, separators=(",", ":")).encode() + b"\n"
    evidence_bytes = mutate(pinned_bytes) if mutate else pinned_bytes
    evidence_root = tmp_path / "evidence"
    evidence_root.mkdir()
    if evidence:
        (evidence_root / f"grant-issued-{gid}.json").write_bytes(
            evidence_bytes)
    record = g7_record_doc(
        layer2, pinned_bytes=evidence_bytes if pin_mutated
        else pinned_bytes, size_delta=size_delta,
        path_override=path_override, evidence_root=evidence_root)
    ri = lc._package_module()
    for name in ri.G6_IDENTITY_FIELDS:
        record[name] = layer2[name]
    record["grant_mint_consideration_permitted"] = True
    record["execution_authority"] = "NONE"
    record["secret_material"] = "NONE"
    record["publication_semantics"] = \
        "NON_EXECUTION_MINT_EVIDENCE_IDENTITY_RECORD"
    raw = json.dumps({k: record[k] for k in ri.G7_MINT_PUBLICATION_FIELDS},
                     separators=(",", ":")).encode()
    commit_files(repo, {G7_PATH: raw}, "g7")
    tip = git(repo, "rev-parse", "HEAD").strip()
    return repo, tip, layer2, evidence_root


def test_evidence_happy_path(tmp_path, pkg_blob_files):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files)
    result = lc.verify_grant_issued_evidence(
        repo, tip, evidence_root, GRANT_ID, layer2)
    assert result["evidence_sha256"] == hashlib.sha256(
        (evidence_root / f"grant-issued-{GRANT_ID}.json").read_bytes()
    ).hexdigest()
    assert result["evidence_size"] > 0


def test_evidence_r_evid_1_mutation_detected(tmp_path, pkg_blob_files):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files,
        mutate=lambda raw: raw.replace(b'"NONE"', b'"SOME"', 1))
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.EVIDENCE_BYTE_MISMATCH


def test_evidence_r_evid_2_size_mismatch(tmp_path, pkg_blob_files):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files, size_delta=1)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.EVIDENCE_BYTE_MISMATCH


def test_evidence_r_evid_3_path_mismatch(tmp_path, pkg_blob_files):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files,
        path_override=str(tmp_path / "other-root"
                           / f"grant-issued-{GRANT_ID}.json"))
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.EVIDENCE_PATH_CUSTODY_REFUSED


def test_evidence_r_evid_8_cross_grant_substitution(tmp_path,
                                                    pkg_blob_files):
    # evidence bytes belong to a DIFFERENT grant identity
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files, other_grant=True)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.EVIDENCE_UNAVAILABLE


def test_evidence_missing_file(tmp_path, pkg_blob_files):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files, evidence=False)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.EVIDENCE_UNAVAILABLE


def test_evidence_missing_g7_record(tmp_path, pkg_blob_files):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files)
    # remove the G7 introduction from the history domain by rebuilding
    (tmp_path / "b").mkdir()
    repo2, tip2, g5_id = build_g6_world(tmp_path / "b", pkg_blob_files)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo2, tip2, evidence_root,
                                        GRANT_ID, layer2)
    assert ei.value.code == lc.EVIDENCE_UNAVAILABLE


# ------------------------------------------- GAP C handoff identity
def test_handoff_single_creation_and_reread_identity(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    payload = b'{"binding":"synthetic"}'
    identity = lc.create_lifecycle_handoff(root, "f" * 40, payload)
    path = root / ("lifecycle-caller-handoff-" + "f" * 40 + ".json")
    assert identity["handoff_sha256"] == hashlib.sha256(payload).hexdigest()
    assert identity["handoff_size"] == len(payload)
    assert path.read_bytes() == payload
    assert (path.stat().st_mode & 0o777) == 0o600
    assert lc.read_lifecycle_handoff(root, "f" * 40)["handoff_bytes"] \
        == payload


def test_handoff_duplicate_refused(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    lc.create_lifecycle_handoff(root, "f" * 40, b"x")
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.create_lifecycle_handoff(root, "f" * 40, b"y")
    assert ei.value.code == lc.DUPLICATE_HANDOFF_EVIDENCE_REFUSED
    assert (root / ("lifecycle-caller-handoff-" + "f" * 40
                    + ".json")).read_bytes() == b"x"   # never replaced


def test_handoff_name_refused(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    for bad in ("short", "Z" * 40, "f" * 41, "../" + "f" * 40, 123):
        with pytest.raises(lc.LifecycleCallerError) as ei:
            lc.create_lifecycle_handoff(root, bad, b"x")
        assert ei.value.code == lc.HANDOFF_NAME_REFUSED


def test_handoff_owner_mutation_detected_c5(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    tip = "a" * 40
    original = lc.create_lifecycle_handoff(root, tip, b"original bytes")
    # owner-level in-place mutation after creation IS possible (the
    # owner write bit remains) and is DETECTED at consumption
    (root / f"lifecycle-caller-handoff-{tip}.json").write_bytes(b"tampered")
    current = lc.read_lifecycle_handoff(root, tip)
    assert current["handoff_sha256"] != original["handoff_sha256"]
    assert current["handoff_bytes"] == b"tampered"


def test_handoff_stale_by_name(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    lc.create_lifecycle_handoff(root, "a" * 40, b"x")
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.require_current_handoff(root, "a" * 40, "b" * 40)
    assert ei.value.code == lc.HANDOFF_STALE_REFUSED


def test_handoff_root_unavailable(tmp_path):
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.create_lifecycle_handoff(tmp_path / "absent", "a" * 40, b"x")
    assert ei.value.code == lc.HANDOFF_ROOT_UNAVAILABLE


# ------------------------------------- R1a G5 disclosure (AM-1/AM-2)
@pytest.mark.parametrize("content", [
    b"definitely not a G5 record: \x00\x01 arbitrary garbage bytes",
    b'{"operator_authority_id": "WRONG-AUTHORITY", "g2_commit": "'
    b'0000000000000000000000000000000000000000", "g3_commit": "deadbeef"}',
])
def test_am1_am2_arbitrary_g5_bytes_identity_only_disclosed(
        tmp_path, pkg_blob_files, content):
    """AM-1/AM-2: arbitrary (or G2/G3-incoherent) bytes at the canonical
    G5 path still pass IDENTITY derivation AS DESIGNED, and the result
    carries the explicit NON-AUTHORITY disclosure — no content-verified
    claim exists anywhere in the caller."""
    repo = tmp_path / "r1aworld"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "master")
    commit_files(repo, {f"bootstrap-authority/{rel}": data for rel, data
                        in pkg_blob_files.items()}, "package")
    g5_id = commit_g5(repo, content)
    commit_g6(repo, g5_id)
    tip = _gated(repo)
    g5 = lc.derive_g5_identity(repo, tip)
    assert g5["commit"] == g5_id["commit"]
    assert g5["verification_status"] == (
        lc.G5_GIT_IDENTITY_DERIVED,
        lc.G5_CONTENT_VERIFICATION_NOT_ESTABLISHED,
        lc.UPSTREAM_V1_V17_NOT_VERIFIED)
    selection = lc.select_canonical_g6_publication(repo, tip)
    assert selection["record"][
        "package_binding_authority_target_commit_sha"] == g5["commit"]


# --------------------------------- R2 evidence content (AM-3..AM-6)
@pytest.mark.parametrize("field,value", [
    ("package_binding_authority_readback_disposition", "REFUSE"),
    ("package_binding_authority_readback_target_commit_sha", "9" * 40),
])
def test_am3_evidence_g6_set_mismatch_refused(tmp_path, pkg_blob_files,
                                              field, value):
    # the T55 form: the G7 record PINS the semantically wrong evidence
    # bytes, so R-EVID-1/2 pass — the G6 cross-bind must catch them
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files, doc_mutate=lambda d, f=field, v=value:
        {**d, f: v}, pin_mutated=True)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.EVIDENCE_G6_IDENTITY_MISMATCH


@pytest.mark.parametrize("doc_mutate", [
    lambda d: {k: v for k, v in d.items() if k != "execution_authority"},
    lambda d: {**d, "extra_field": "x"},
    lambda d: {**d, "grant_issued_evidence_sha256": "a" * 64},
    lambda d: {**d, "governance_event_id": "OTHER-EVENT"},
    lambda d: {**d, "auditor_role": "AUDITOR_B"},
    lambda d: {**d, "attempt_slot": "AUDITOR_A_REPLACEMENT_2"},
    lambda d: {**d, "grant_mint_consideration_permitted": "true"},
    lambda d: {**d, "grant_mint_consideration_permitted": 1},
    lambda d: {**d, "execution_authority": "SOME"},
    lambda d: {**d, "secret_material": "SOME"},
])
def test_am4_evidence_schema_refusals(tmp_path, pkg_blob_files, doc_mutate):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files, doc_mutate=doc_mutate, pin_mutated=True)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.EVIDENCE_SCHEMA_INVALID


@pytest.mark.parametrize("mutate,code", [
    (lambda raw: json.dumps(json.loads(raw), sort_keys=True,
                            separators=(",", ":")).encode() + b"\n",
     lc.EVIDENCE_CANONICAL_BYTES_INVALID),
    (lambda raw: raw.replace(b",", b", "),
     lc.EVIDENCE_CANONICAL_BYTES_INVALID),
    (lambda raw: raw[:-1], lc.EVIDENCE_CANONICAL_BYTES_INVALID),
    (lambda raw: raw + b"\n", lc.EVIDENCE_CANONICAL_BYTES_INVALID),
    (lambda raw: raw[:-1] + b',"grant_identity":"' + GRANT_ID.encode()
     + b'"}', lc.EVIDENCE_SCHEMA_INVALID),
])
def test_am5_evidence_canonical_bytes_refusals(tmp_path, pkg_blob_files,
                                               mutate, code):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files, mutate=mutate, pin_mutated=True)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == code


@pytest.mark.parametrize("field,value", [
    ("grant_document_sha256", "c" * 64),
    ("future_machine_attempt_id", "OTHER-ATTEMPT-ID"),
])
def test_am6_evidence_g7_cross_bind_refused(tmp_path, pkg_blob_files,
                                            field, value):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files, doc_mutate=lambda d, f=field, v=value:
        {**d, f: v}, pin_mutated=True)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.EVIDENCE_CROSS_BIND_MISMATCH


def test_r2_evidence_happy_path_still_green(tmp_path, pkg_blob_files):
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files)
    result = lc.verify_grant_issued_evidence(
        repo, tip, evidence_root, GRANT_ID, layer2)
    assert result["evidence_size"] > 0
    doc = json.loads((evidence_root / f"grant-issued-{GRANT_ID}.json")
                     .read_bytes())
    assert list(doc) == list(lc.EVIDENCE_DOCUMENT_FIELDS)


# --------------------------- R4 anchored handoff consumption (AM-9/10)
def test_am9_anchored_consumer_refuses_mutation(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    tip = "a" * 40
    original = lc.create_lifecycle_handoff(root, tip, b"original payload")
    (root / f"lifecycle-caller-handoff-{tip}.json").write_bytes(b"tampered")
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.consume_lifecycle_handoff(
            root, tip, tip, original["handoff_path"],
            original["handoff_sha256"], original["handoff_size"])
    assert ei.value.code == lc.HANDOFF_EVIDENCE_BYTE_MISMATCH
    # the unanchored informational read still SUCCEEDS and is explicit
    info = lc.read_lifecycle_handoff(root, tip)
    assert info["trust_status"] == "UNANCHORED_INFORMATIONAL_READ"
    assert info["handoff_bytes"] == b"tampered"


def test_am10_anchored_consumer_happy_and_anchor_refusals(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    tip = "b" * 40
    original = lc.create_lifecycle_handoff(root, tip, b"anchored payload")
    consumed = lc.consume_lifecycle_handoff(
        root, tip, tip, original["handoff_path"],
        original["handoff_sha256"], original["handoff_size"])
    assert consumed["trust_status"] == "ANCHORED_IDENTITY_VERIFIED"
    assert consumed["handoff_sha256"] == original["handoff_sha256"]
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.consume_lifecycle_handoff(
            root, tip, tip, original["handoff_path"], "c" * 64,
            original["handoff_size"])
    assert ei.value.code == lc.HANDOFF_EVIDENCE_BYTE_MISMATCH
    for path, digest, size in (
            (str(root / "elsewhere.json"), original["handoff_sha256"],
             original["handoff_size"]),
            (original["handoff_path"], "not-hex", original["handoff_size"]),
            (original["handoff_path"], original["handoff_sha256"], -1)):
        with pytest.raises(lc.LifecycleCallerError) as ei:
            lc.consume_lifecycle_handoff(root, tip, tip, path, digest,
                                         size)
        assert ei.value.code == lc.HANDOFF_ANCHOR_REFUSED
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.consume_lifecycle_handoff(
            root, tip, "e" * 40, original["handoff_path"],
            original["handoff_sha256"], original["handoff_size"])
    assert ei.value.code == lc.HANDOFF_STALE_REFUSED


# --------------------------------- R6 object custody (AM-11/AM-12)
def test_am11_fifo_evidence_refused(tmp_path, pkg_blob_files):
    # a writer-controlled FIFO cannot stream the pinned bytes past the
    # checks: the open is nonblocking and S_ISREG refuses before reads
    repo, tip, layer2, evidence_root = build_evidence_world(
        tmp_path, pkg_blob_files)
    name = f"grant-issued-{GRANT_ID}.json"
    (evidence_root / name).unlink()
    os.mkfifo(evidence_root / name)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_grant_issued_evidence(repo, tip, evidence_root, GRANT_ID,
                                        layer2)
    assert ei.value.code == lc.OBJECT_CUSTODY_REFUSED


def test_am11b_fifo_handoff_refused(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    os.mkfifo(root / f"lifecycle-caller-handoff-{'a' * 40}.json")
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.read_lifecycle_handoff(root, "a" * 40)
    assert ei.value.code == lc.OBJECT_CUSTODY_REFUSED


def test_am12_special_object_refused(tmp_path):
    root = tmp_path / "handoff"
    root.mkdir()
    (root / f"lifecycle-caller-handoff-{'a' * 40}.json").mkdir()
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.read_lifecycle_handoff(root, "a" * 40)
    assert ei.value.code == lc.OBJECT_CUSTODY_REFUSED


# ------------------------------------------------------------- glue
def test_run_authenticated_binding_smoke(tmp_path, anchor_template,
                                         pkg_blob_files):
    repo, _ = build_anchor_world(tmp_path, anchor_template)
    commit_files(repo, {f"bootstrap-authority/{rel}": data for rel, data
                        in pkg_blob_files.items()}, "package")
    tip = git(repo, "rev-parse", "HEAD").strip()
    cfg = write_config(tmp_path, CANONICAL_CONFIG)
    remote = LS_REMOTE_OK.replace(TIP, tip)
    result = lc.run_authenticated_binding(
        cfg, repo, repo / "bootstrap-authority",
        ls_remote=TransportDouble([remote, remote]),
        api_read=ApiDouble(api_result(tip)))
    assert result["binding"]["authoritative_tip"] == tip
    assert "bootstrap_authority.runtime" in sys.modules
    assert hasattr(result["receiptidentity"], "G6_IDENTITY_FIELDS")


# ------------------------------------- R5 pipeline (AM-14..AM-16)
def _pipeline_world(tmp_path, anchor_template, pkg_blob_files, *,
                    g6=True, g6_over=None, g6_before_g5=False):
    """Anchor-descended synthetic world: package, then G5, then G6."""
    repo, _ = build_anchor_world(tmp_path, anchor_template)
    commit_files(repo, {f"bootstrap-authority/{rel}": data for rel, data
                        in pkg_blob_files.items()}, "package")
    if g6_before_g5:
        assert g6 and not g6_over
        commit_g6(repo, {"commit": "0" * 40, "record_path": G5_PATH,
                         "record_blob_sha1": "0" * 40,
                         "record_sha256": "0" * 64})
        commit_g5(repo)
        return repo
    g5_id = commit_g5(repo)
    if g6:
        commit_g6(repo, g5_id, **(g6_over or {}))
    return repo


def _pipeline_setup(tmp_path, repo):
    """Complete the world through G7 + evidence; return the run inputs."""
    tip = git(repo, "rev-parse", "HEAD").strip()
    lc.import_verified_package(repo, tip, repo / "bootstrap-authority")
    layer2 = lc.derive_g6_layer2(lc.select_canonical_g6_publication(
        repo, tip))
    evidence_root = tmp_path / "evidence"
    evidence_root.mkdir()
    doc = evidence_doc(layer2)
    pinned = json.dumps(doc, separators=(",", ":")).encode() + b"\n"
    (evidence_root / f"grant-issued-{GRANT_ID}.json").write_bytes(pinned)
    record = g7_record_doc(layer2, pinned_bytes=pinned,
                           evidence_root=evidence_root)
    ri = lc._package_module()
    for name in ri.G6_IDENTITY_FIELDS:
        record[name] = layer2[name]
    record.update(grant_mint_consideration_permitted=True,
                  execution_authority="NONE", secret_material="NONE",
                  publication_semantics="NON_EXECUTION_MINT_EVIDENCE_"
                                        "IDENTITY_RECORD")
    raw = json.dumps({k: record[k] for k in ri.G7_MINT_PUBLICATION_FIELDS},
                     separators=(",", ":")).encode()
    commit_files(repo, {G7_PATH: raw}, "g7")
    tip = git(repo, "rev-parse", "HEAD").strip()
    cfg = write_config(tmp_path, CANONICAL_CONFIG, name="pcfg.json")
    remote = LS_REMOTE_OK.replace(TIP, tip)
    handoff_root = tmp_path / "handoff"
    handoff_root.mkdir()
    return cfg, remote, tip, evidence_root, handoff_root


def test_am16_pipeline_full_synthetic_success(tmp_path, anchor_template,
                                              pkg_blob_files):
    repo = _pipeline_world(tmp_path, anchor_template, pkg_blob_files)
    cfg, remote, tip, evidence_root, handoff_root = _pipeline_setup(
        tmp_path, repo)
    result = lc.run_authenticated_lifecycle(
        cfg, repo, repo / "bootstrap-authority", evidence_root,
        handoff_root, GRANT_ID,
        ls_remote=TransportDouble([remote, remote]),
        api_read=ApiDouble(api_result(tip)))
    assert result["binding"]["authoritative_tip"] == tip
    assert lc.G5_CONTENT_VERIFICATION_NOT_ESTABLISHED \
        in result["g5"]["verification_status"]
    payload = json.dumps(
        {k: result["binding"][k] for k in lc.INVOCATION_EVIDENCE_FIELDS},
        separators=(",", ":")).encode()
    assert (handoff_root / f"lifecycle-caller-handoff-{tip}.json"
            ).read_bytes() == payload
    consumed = lc.consume_lifecycle_handoff(
        handoff_root, tip, tip, result["handoff"]["handoff_path"],
        result["handoff"]["handoff_sha256"],
        result["handoff"]["handoff_size"])
    assert consumed["trust_status"] == "ANCHORED_IDENTITY_VERIFIED"
    assert result["stages"] == ("trust_root", "import_gate", "g5_identity",
                                "g6_selection", "g6_hard_barrier",
                                "g7_selection", "evidence_validation",
                                "handoff")
    expected_evidence = json.dumps(evidence_doc(result["g6_layer2"]),
                                   separators=(",", ":")).encode() + b"\n"
    assert result["evidence"]["evidence_sha256"] == hashlib.sha256(
        expected_evidence).hexdigest()


@pytest.mark.parametrize("disposition", ["REFUSE", "BLOCK",
                                         "REMEDIATION_REQUIRED"])
def test_am15_pipeline_adverse_g6_hard_barrier(tmp_path, anchor_template,
                                               pkg_blob_files, disposition):
    repo = _pipeline_world(
        tmp_path, anchor_template, pkg_blob_files,
        g6_over={"package_binding_authority_readback_disposition": disposition,
                 "grant_mint_consideration_permitted": False})
    tip = git(repo, "rev-parse", "HEAD").strip()
    cfg = write_config(tmp_path, CANONICAL_CONFIG, name="pcfg2.json")
    remote = LS_REMOTE_OK.replace(TIP, tip)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.run_authenticated_lifecycle(
            cfg, repo, repo / "bootstrap-authority", tmp_path / "ev",
            tmp_path / "ho", GRANT_ID,
            ls_remote=TransportDouble([remote, remote]),
            api_read=ApiDouble(api_result(tip)))
    assert ei.value.code == lc.G6_BARRIER_REFUSED


def test_am14_pipeline_stage_sequence(tmp_path, anchor_template,
                                      pkg_blob_files):
    # no G6 at all: the pipeline fails closed at stage 4 (selection),
    # never reaching the barrier or later stages
    repo = _pipeline_world(tmp_path, anchor_template, pkg_blob_files,
                           g6=False)
    tip = git(repo, "rev-parse", "HEAD").strip()
    cfg = write_config(tmp_path, CANONICAL_CONFIG, name="pcfg3.json")
    remote = LS_REMOTE_OK.replace(TIP, tip)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.run_authenticated_lifecycle(
            cfg, repo, repo / "bootstrap-authority", tmp_path / "ev",
            tmp_path / "ho", GRANT_ID,
            ls_remote=TransportDouble([remote, remote]),
            api_read=ApiDouble(api_result(tip)))
    assert ei.value.code == lc.CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND
    # stale G5 (G6 introduced before its target): stage 4 STALE refusal
    repo = _pipeline_world(tmp_path / "s", anchor_template, pkg_blob_files,
                           g6_before_g5=True)
    tip = git(repo, "rev-parse", "HEAD").strip()
    remote = LS_REMOTE_OK.replace(TIP, tip)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.run_authenticated_lifecycle(
            write_config(tmp_path / "s", CANONICAL_CONFIG, name="c.json"),
            repo, repo / "bootstrap-authority", tmp_path / "ev2",
            tmp_path / "ho2", GRANT_ID,
            ls_remote=TransportDouble([remote, remote]),
            api_read=ApiDouble(api_result(tip)))
    assert ei.value.code == lc.G6_STALE_REFUSED


# ------------------------------------------- budgets (AM-18)
def test_am18_loc_budgets_and_zero_bytecode():
    production = len(Path(lc.__file__).read_text().splitlines())
    tests = sum(len(p.read_text().splitlines()) for p in (
        Path(__file__).with_name("test_lifecycle_caller.py"),
        Path(__file__).with_name("test_import_gate.py")))
    assert production <= 1250, production
    assert tests <= 2000, tests
    for base in (REPO_ROOT / "bootstrap-authority", LC_ROOT):
        assert not list(base.rglob("__pycache__"))


def test_real_repository_g6_evaluation_refuses():
    """NO real favorable G6 evidence exists: against the LIVE canonical
    repository at its verified tip, G6 selection must fail closed."""
    lc.import_verified_package(REPO_ROOT, _live_tip(), PKG_DIR)
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.select_canonical_g6_publication(REPO_ROOT, _live_tip())
    assert ei.value.code in (lc.G5_TARGET_NOT_RESOLVABLE,
                             lc.CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND)


def _live_tip():
    out = subprocess.run(("git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"),
                         capture_output=True)
    assert out.returncode == 0
    return out.stdout.decode().strip()
