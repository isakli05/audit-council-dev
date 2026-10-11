"""AUCDEV-023 PCH6-B Path-B TRUSTROOT-001 authenticated lifecycle
caller (P3 non-runtime; IMPLEMENTATION CANDIDATE granting nothing).

Accepted design contracts (records 8b31d8e5... / 8bf12dea..., readbacks
86f4e7c0... / bed8f50f...): trust-root T1-T8 (GAP B), canonical G6
sourcing K1-K14 with independently derived G5 targets and Layer-2
identity (GAP A), GRANT_ISSUED original-evidence verification
(R-EVID), terminal NON-AUTHORITY handoff content identity (GAP C),
and the GAP-D import boundary — blob pinning + GAP-D-STATIC-V2 census
BEFORE an ORDINARY lazy import of bootstrap_authority.receiptidentity
(transitive runtime load disclosed; never any runtime authority).
NON-AUTHORITY: creates no grant/evidence/publication/receipt/package;
every verification fail-closed, no retry, no fallback."""

import ast
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import urllib.error
import urllib.request

# --- canonical identity constants (operator tasking Section 4; the
# stable provider repository id is the anti-substitution core) ------
CANONICAL_OWNER = "isakli05"
CANONICAL_REPOSITORY = "audit-council-dev"
CANONICAL_PROVIDER_REPOSITORY_ID = "1358379094"
CANONICAL_REMOTE_URL = "https://github.com/isakli05/audit-council-dev.git"
EXPECTED_DEFAULT_BRANCH = "master"; TRUST_ANCHOR_COMMIT = "3058868416241d394cfaaa40cc585085db486f37"
TRANSPORT_MODE = "HTTPS_TLS_NO_REDIRECT"

_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_HEX40_RE = _SHA1_RE

# --- refusal codes (fail-closed; first-class categories) -----------
TRUST_ROOT_CONFIG_SOURCE_REFUSED = "TRUST_ROOT_CONFIG_SOURCE_REFUSED"
TRUST_ROOT_CONFIG_UNAVAILABLE = "TRUST_ROOT_CONFIG_UNAVAILABLE"; TRUST_ROOT_CONFIG_INVALID = "TRUST_ROOT_CONFIG_INVALID"
TRANSPORT_REDIRECT_REFUSED = "TRANSPORT_REDIRECT_REFUSED"; TRANSPORT_REFUSED = "TRANSPORT_REFUSED"
DEFAULT_BRANCH_MISMATCH = "DEFAULT_BRANCH_MISMATCH"; TRUST_ANCHOR_NOT_ANCESTOR = "TRUST_ANCHOR_NOT_ANCESTOR"
AUTHORITATIVE_REF_NOT_RESOLVED = "AUTHORITATIVE_REF_NOT_RESOLVED"; AUTHORITATIVE_REF_AMBIGUOUS = "AUTHORITATIVE_REF_AMBIGUOUS"
IDENTITY_DISAGREEMENT_REFUSED = "IDENTITY_DISAGREEMENT_REFUSED"
AUTHORITATIVE_TIP_NOT_A_LOCAL_COMMIT = "AUTHORITATIVE_TIP_NOT_A_LOCAL_COMMIT"
AUTHORITATIVE_TIP_MOVED_DURING_VERIFICATION = "AUTHORITATIVE_TIP_MOVED_DURING_VERIFICATION"
GIT_PLUMBING_FAILED = "GIT_PLUMBING_FAILED"; SOURCE_BLOB_PIN_MISMATCH = "SOURCE_BLOB_PIN_MISMATCH"
IMPORT_TIME_STATIC_REFUSED = "IMPORT_TIME_STATIC_REFUSED"; CALLER_SOURCE_REFUSED = "CALLER_SOURCE_REFUSED"
G5_TARGET_NOT_RESOLVABLE = "G5_TARGET_NOT_RESOLVABLE"; G6_STALE_REFUSED = "G6_STALE_REFUSED"; G6_LAYER1_INVALID = "G6_LAYER1_INVALID"
CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND = "CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND"
CANONICAL_G6_READBACK_PUBLICATION_AMBIGUOUS = "CANONICAL_G6_READBACK_PUBLICATION_AMBIGUOUS"
EVIDENCE_UNAVAILABLE = "EVIDENCE_UNAVAILABLE"; EVIDENCE_BYTE_MISMATCH = "EVIDENCE_BYTE_MISMATCH"
EVIDENCE_PATH_CUSTODY_REFUSED = "EVIDENCE_PATH_CUSTODY_REFUSED"; EVIDENCE_IDENTITY_MISMATCH = "EVIDENCE_IDENTITY_MISMATCH"
HANDOFF_NAME_REFUSED = "HANDOFF_NAME_REFUSED"; HANDOFF_ROOT_UNAVAILABLE = "HANDOFF_ROOT_UNAVAILABLE"
HANDOFF_UNAVAILABLE = "HANDOFF_UNAVAILABLE"; HANDOFF_STALE_REFUSED = "HANDOFF_STALE_REFUSED"
DUPLICATE_HANDOFF_EVIDENCE_REFUSED = "DUPLICATE_HANDOFF_EVIDENCE_REFUSED"
HANDOFF_EVIDENCE_BYTE_MISMATCH = "HANDOFF_EVIDENCE_BYTE_MISMATCH"
IMPORT_GATE_NOT_RUN = "IMPORT_GATE_NOT_RUN"; IMPORT_DISCLOSURE_REFUSED = "IMPORT_DISCLOSURE_REFUSED"

class LifecycleCallerError(Exception):
    """Fail-closed refusal carrying the exact contract refusal code."""

    def __init__(self, code, detail=""):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail

def _fail(code, detail=""):
    raise LifecycleCallerError(code, detail)

def _canonical_json(document, fields):
    """RIP-form canonical serialization (record A 4.3): fixed key
    order, compact separators, printable-ASCII, no BOM/newline."""
    if not isinstance(document, dict) or set(document) != set(fields):
        _fail("CANONICAL_JSON_FIELDS_INVALID", sorted(map(str, document)))
    text = json.dumps({name: document[name] for name in fields},
                      separators=(",", ":"), ensure_ascii=False)
    raw = text.encode()
    if any(byte < 0x20 or byte > 0x7E for byte in raw):
        _fail("CANONICAL_JSON_NOT_PRINTABLE_ASCII", raw[:80])
    return raw

def _strict_loads(raw, invalid_code):
    """Strict JSON with duplicate-key refusal (closed world)."""

    def hook(pairs):
        seen = set()
        for key, _ in pairs:
            if key in seen:
                _fail(invalid_code, f"duplicate key {key!r}")
            seen.add(key)
        return dict(pairs)
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=hook)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(invalid_code, repr(exc))

# --- GAP B: the operator-held trust-root configuration (T1/T2) -----
CONFIG_SCHEMA = "AUCDEV-023-LIFECYCLE-CALLER-TRUST-ROOT-CONFIG-V1"
CONFIG_FIELDS = ("schema", "canonical_owner", "canonical_repository",
                 "canonical_provider_repository_id", "canonical_remote_url",
                 "expected_default_branch", "trust_anchor_commit",
                 "transport_mode")

def load_trust_root_config(path, repo):
    """T1/T2: operator-held config OUTSIDE the unverified repository
    (relative/in-repo paths refused — the repo can never vouch for the
    standard verifying it); closed-world shape, canonical bytes."""
    config_path = os.fspath(path)
    if not os.path.isabs(config_path):
        _fail(TRUST_ROOT_CONFIG_SOURCE_REFUSED, "relative path")
    resolved = os.path.realpath(config_path)
    tree_root = os.path.realpath(_git(
        repo, "rev-parse", "--show-toplevel").strip())
    if os.path.commonpath([resolved, tree_root]) == tree_root:
        _fail(TRUST_ROOT_CONFIG_SOURCE_REFUSED,
              f"{resolved} is inside the repository under verification")
    try:
        with open(config_path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        _fail(TRUST_ROOT_CONFIG_UNAVAILABLE, repr(exc))
    doc = _strict_loads(raw, TRUST_ROOT_CONFIG_INVALID)
    if not isinstance(doc, dict) or set(doc) != set(CONFIG_FIELDS):
        _fail(TRUST_ROOT_CONFIG_INVALID, "not the closed-world set")
    pairs = {"schema": CONFIG_SCHEMA, "canonical_owner": CANONICAL_OWNER,
             "canonical_repository": CANONICAL_REPOSITORY,
             "canonical_provider_repository_id":
                 CANONICAL_PROVIDER_REPOSITORY_ID,
             "canonical_remote_url": CANONICAL_REMOTE_URL,
             "expected_default_branch": EXPECTED_DEFAULT_BRANCH,
             "trust_anchor_commit": TRUST_ANCHOR_COMMIT,
             "transport_mode": TRANSPORT_MODE}
    for field, expected in pairs.items():
        if doc[field] != expected:
            _fail(TRUST_ROOT_CONFIG_INVALID, f"{field}={doc[field]!r}")
    if _canonical_json(doc, CONFIG_FIELDS) != raw:
        _fail(TRUST_ROOT_CONFIG_INVALID, "non-canonical bytes")
    return {name: doc[name] for name in CONFIG_FIELDS}

# --- GAP B: transport (T3/T4) --------------------------------------
def _parse_ls_remote(text, branch):
    """T3/T4 parsing: HEAD symref target must be refs/heads/<branch>;
    exactly one 40-hex branch row (shape necessary, never sufficient)."""
    want_ref = f"refs/heads/{branch}"
    symref, rows = None, []
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.startswith("ref: "):
            symref = line.split("\t")[0][len("ref: "):].strip()
            continue
        parts = line.split("\t")
        if len(parts) != 2 or not _SHA1_RE.match(parts[0].strip()) \
                or not parts[1].strip():
            _fail(AUTHORITATIVE_REF_NOT_RESOLVED, line)
        rows.append((parts[0].strip(), parts[1].strip()))
    if symref != want_ref:
        _fail(DEFAULT_BRANCH_MISMATCH, repr(symref))
    branch_rows = [sha for sha, ref in rows if ref == want_ref]
    if not branch_rows:
        _fail(AUTHORITATIVE_REF_NOT_RESOLVED, want_ref)
    if len(branch_rows) > 1 or any(
            sha != branch_rows[0] for sha, ref in rows if ref == "HEAD"):
        _fail(AUTHORITATIVE_REF_AMBIGUOUS, branch_rows)
    return symref, branch_rows[0]

def default_ls_remote(url, branch):
    """Real transport at the EXACT config URL (local aliases never
    consulted): verified TLS, redirects refused."""
    out = subprocess.run(
        ("git", "-c", "http.followRedirects=false",
         "-c", "http.sslVerify=true", "ls-remote", "--symref", url,
         "HEAD", f"refs/heads/{branch}"), capture_output=True)
    if out.returncode != 0:
        err = out.stderr.decode("utf-8", "replace")
        _fail(TRANSPORT_REDIRECT_REFUSED if "redirect" in err.lower()
              else TRANSPORT_REFUSED, err.strip()[:200])
    return out.stdout.decode("utf-8", "replace")

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None
_API_OPENER = urllib.request.build_opener(_NoRedirect)
def default_api_read(url):
    """T5: MANDATORY independent second channel — public GitHub API
    over HTTPS, verified TLS, no redirects; metadata + branch tip."""
    base = (f"https://api.github.com/repos/{CANONICAL_OWNER}/"
            f"{CANONICAL_REPOSITORY}")

    def get(target):
        request = urllib.request.Request(
            target, headers={"Accept": "application/vnd.github+json"})
        try:
            with _API_OPENER.open(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            _fail(TRANSPORT_REDIRECT_REFUSED if exc.code < 400
                  else TRANSPORT_REFUSED, f"HTTP {exc.code}")
        except (urllib.error.URLError, OSError, ValueError) as exc:
            _fail(TRANSPORT_REFUSED, repr(exc))
    meta = get(base)
    commit = get(f"{base}/commits/{EXPECTED_DEFAULT_BRANCH}")
    return {"full_name": meta.get("full_name"), "id": meta.get("id"),
            "default_branch": meta.get("default_branch"),
            "tip": commit.get("sha")}
def _git_proc(repo, *args):
    return subprocess.run(("git", "-C", os.fspath(repo), *args),
                          capture_output=True)
def _git(repo, *args):
    """Read-only git plumbing wrapper (fail-closed)."""
    out = _git_proc(repo, *args)
    if out.returncode != 0:
        _fail(GIT_PLUMBING_FAILED, f"git {' '.join(args)}: " + out.stderr
              .decode("utf-8", "replace").strip()[:200])
    return out.stdout.decode("utf-8", "replace")

# --- GAP B: the verification procedure T1-T8 ------------------------
INVOCATION_EVIDENCE_SCHEMA = \
    "AUCDEV-023-LIFECYCLE-CALLER-INVOCATION-EVIDENCE-V1"
INVOCATION_EVIDENCE_FIELDS = (
    "schema", "canonical_owner", "canonical_repository",
    "canonical_provider_repository_id", "canonical_remote_url",
    "expected_default_branch", "authoritative_tip", "trust_anchor_commit",
    "transport_mode", "config_source_path", "git_channel", "api_channel")

def _api_agrees(info, branch, tip):
    return (info.get("full_name")
            == f"{CANONICAL_OWNER}/{CANONICAL_REPOSITORY}"
            and str(info.get("id")) == CANONICAL_PROVIDER_REPOSITORY_ID
            and info.get("default_branch") == branch
            and info.get("tip") == tip)
def verify_trust_root(config_path, repo, *, ls_remote=None, api_read=None):
    """T1-T8 (record A 5.2; fail-closed, refusals final): config source
    discipline; transport at the exact config URL; default branch BY
    the remote; MANDATORY API corroboration (full_name + numeric id +
    default branch + tip; ANY disagreement refused); local
    correspondence (anchor ancestry CORROBORATION ONLY); immediate
    tip re-resolution; returns the invocation evidence."""
    config = load_trust_root_config(config_path, repo)
    url, branch = (config["canonical_remote_url"],
                   config["expected_default_branch"])
    transport = ls_remote or default_ls_remote
    api = api_read or default_api_read
    _, tip = _parse_ls_remote(transport(url, branch), branch)
    info = api(url)
    if not _api_agrees(info, branch, tip):
        _fail(IDENTITY_DISAGREEMENT_REFUSED, repr(info))
    try:
        object_type = _git(repo, "cat-file", "-t", tip).strip()
    except LifecycleCallerError:
        object_type = None          # unresolvable locally == not local
    if object_type != "commit":
        _fail(AUTHORITATIVE_TIP_NOT_A_LOCAL_COMMIT, tip)
    if _git_proc(repo, "merge-base", "--is-ancestor",
                 config["trust_anchor_commit"], tip).returncode:
        _fail(TRUST_ANCHOR_NOT_ANCESTOR, config["trust_anchor_commit"])
    _git(repo, "rev-parse", f"{tip}^{{tree}}")
    _, tip_again = _parse_ls_remote(transport(url, branch), branch)
    info_again = api(url)
    if tip_again != tip or info_again.get("tip") != tip:
        _fail(AUTHORITATIVE_TIP_MOVED_DURING_VERIFICATION, tip_again)
    if not _api_agrees(info_again, branch, tip):
        _fail(IDENTITY_DISAGREEMENT_REFUSED, repr(info_again))
    return dict(zip(INVOCATION_EVIDENCE_FIELDS, (
        INVOCATION_EVIDENCE_SCHEMA, CANONICAL_OWNER, CANONICAL_REPOSITORY,
        CANONICAL_PROVIDER_REPOSITORY_ID, url, branch, tip,
        config["trust_anchor_commit"], TRANSPORT_MODE,
        os.path.realpath(config_path), "git-ls-remote-HTTPS_TLS_NO_REDIRECT",
        "github-api-public-unauthenticated")))

# --- GAP A: the canonical G6 publication (record A Section 4) -------
GOVERNANCE_EVENT_ID = "AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01"
G6_LAYER1_SCHEMA = "AUCDEV-023-PACKAGE-BINDING-AUTHORITY-READBACK-PUBLICATION-V1"
G6_LAYER1_SEMANTICS = "NON_EXECUTION_CONTROL_ROOM_READBACK_RECORD"
G6_PUBLICATION_DISPOSITION_PERMIT = "PERMIT_GRANT_MINT_CONSIDERATION"
G6_DISPOSITIONS = (G6_PUBLICATION_DISPOSITION_PERMIT, "REFUSE", "BLOCK",
                   "REMEDIATION_REQUIRED")
G5_PUBLICATION_RECORD_PATH = (
    "docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-AUDITOR-"
    "A-PACKAGE-BINDING-AUTHORITY.md")
G6_PUBLICATION_RECORD_PATH = G5_PUBLICATION_RECORD_PATH[:-3] \
    + "-READBACK-PUBLICATION.md"
_T = "package_binding_authority_target_"
G6_LAYER1_FIELDS = (
    "schema", "publication_semantics", "governance_event_id",
    "auditor_role", "attempt_slot", "readback_authority_id",
    _T + "commit_sha", _T + "record_path", _T + "record_blob_sha1",
    _T + "record_sha256", "package_binding_authority_readback_"
    "disposition", "grant_mint_consideration_permitted",
    "execution_authority", "auditor_b_authority", "secret_material")
del _T

def parse_g6_publication(data):
    """Closed-world 15-field Layer-1 parser (K5-K8/K10/K11): strict
    JSON, dup-key refusal, exact literals, disposition enum + coherence
    rule, canonical-bytes equality (K5)."""
    raw = data.encode() if isinstance(data, str) else data
    doc = _strict_loads(raw, G6_LAYER1_INVALID)
    if not isinstance(doc, dict) or set(doc) != set(G6_LAYER1_FIELDS):
        _fail(G6_LAYER1_INVALID, "not the closed-world 15-field set")
    pairs = {"schema": G6_LAYER1_SCHEMA,
             "publication_semantics": G6_LAYER1_SEMANTICS,
             "governance_event_id": GOVERNANCE_EVENT_ID,
             "auditor_role": "AUDITOR_A",
             "attempt_slot": "AUDITOR_A_REPLACEMENT_1",
             "package_binding_authority_target_record_path":
                 G5_PUBLICATION_RECORD_PATH,
             "execution_authority": "NONE", "auditor_b_authority": "NONE",
             "secret_material": "NONE"}
    for field, expected in pairs.items():
        if doc[field] != expected:
            _fail(G6_LAYER1_INVALID, f"{field}={doc[field]!r}")
    authority = doc["readback_authority_id"]
    if not isinstance(authority, str) or not authority or any(
            not 0x20 <= ord(c) <= 0x7E for c in authority):
        _fail(G6_LAYER1_INVALID, "readback_authority_id not printable ASCII")
    for field in ("package_binding_authority_target_commit_sha",
                  "package_binding_authority_target_record_blob_sha1"):
        if not isinstance(doc[field], str) or not _SHA1_RE.match(doc[field]):
            _fail(G6_LAYER1_INVALID, f"{field} not 40 lowercase hex")
    sha256_field = doc["package_binding_authority_target_record_sha256"]
    if not _SHA256_RE.match(str(sha256_field)):
        _fail(G6_LAYER1_INVALID, "target_record_sha256 not 64 hex")
    disposition = doc["package_binding_authority_readback_disposition"]
    if disposition not in G6_DISPOSITIONS:
        _fail(G6_LAYER1_INVALID, f"disposition {disposition!r}")
    permitted = doc["grant_mint_consideration_permitted"]
    if not isinstance(permitted, bool):
        _fail(G6_LAYER1_INVALID, "permitted not a JSON boolean")
    if permitted != (disposition == G6_PUBLICATION_DISPOSITION_PERMIT):
        _fail(G6_LAYER1_INVALID, "boolean-coherence rule violated")
    if _canonical_json(doc, G6_LAYER1_FIELDS) != raw:
        _fail(G6_LAYER1_INVALID, "not the canonical serialization (K5)")
    return {name: doc[name] for name in G6_LAYER1_FIELDS}

def _package_module():
    """Gated surface: only reachable after the gate passed."""
    module = sys.modules.get("bootstrap_authority.receiptidentity")
    if module is None:
        _fail(IMPORT_GATE_NOT_RUN,
              "the import gate must pass before any selector reuse")
    return module

def derive_g5_identity(repo, tip):
    """K9 support: canonical G5 identity by the SAME first-parent
    exact-one raw-ADD discipline through the SHARED core; missing or
    ambiguous FAILS CLOSED."""
    package = _package_module()
    candidates = list(package._qualifying_introductions(
        repo, tip, G5_PUBLICATION_RECORD_PATH, lambda raw: {"raw": raw}))
    if len(candidates) != 1:
        _fail(G5_TARGET_NOT_RESOLVABLE,
              [candidate["commit"] for candidate in candidates])
    selected = candidates[0]
    return {key: selected[key] for key in
            ("commit", "record_path", "record_blob_sha1", "record_sha256")}

def select_canonical_g6_publication(repo, tip):
    """K1-K14 over the SHARED core on the FIRST-PARENT history of the
    verified tip (K1-K4 core; K5-K11 parser; K9 G5 targets == the
    INDEPENDENTLY re-derived identities BY VALUE, drift or later-G5 ->
    STALE; K12 domain; K13 exact-one; K14 no caller/package input)."""
    package = _package_module()

    def parse(raw):
        try:
            return parse_g6_publication(raw)
        except LifecycleCallerError as exc:
            raise package.ReceiptIdentityError(str(exc)) from None
    g5 = derive_g5_identity(repo, tip)
    qualifying = []
    for candidate in package._qualifying_introductions(
            repo, tip, G6_PUBLICATION_RECORD_PATH, parse):
        record = candidate["record"]
        prefix = "package_binding_authority_target_"
        targets = tuple(record[prefix + part] for part in
                        ("commit_sha", "record_path", "record_blob_sha1",
                         "record_sha256"))
        stale = targets != (g5["commit"], g5["record_path"],
                            g5["record_blob_sha1"], g5["record_sha256"])
        if stale or _git_proc(repo, "merge-base", "--is-ancestor",
                              g5["commit"],
                              candidate["commit"]).returncode:
            _fail(G6_STALE_REFUSED,
                  "G5 target drift or later-introduced G5 (R-G6-1 form)")
        qualifying.append(candidate)
    if not qualifying:
        _fail(CANONICAL_G6_READBACK_PUBLICATION_NOT_FOUND, tip)
    if len(qualifying) > 1:
        _fail(CANONICAL_G6_READBACK_PUBLICATION_AMBIGUOUS,
              [candidate["commit"] for candidate in qualifying])
    return qualifying[0]

def derive_g6_layer2(selection):
    """The eight Layer-2 identities at their EXACT implemented names
    (`G6_IDENTITY_FIELDS`): 1-5 post-hoc Git observations, 6-8 from
    the Layer-1 payload (whose target field has no `readback`)."""
    names = _package_module().G6_IDENTITY_FIELDS
    record = selection["record"]
    return dict(zip(names, (
        selection["commit"], selection["root_tree"],
        selection["record_path"], selection["record_blob_sha1"],
        selection["record_sha256"],
        record["package_binding_authority_target_commit_sha"],
        record["package_binding_authority_readback_disposition"],
        record["grant_mint_consideration_permitted"])))

# --- GRANT_ISSUED original-evidence verification (R-EVID) ----------
def verify_grant_issued_evidence(repo, tip, evidence_root, grant_identity,
                                 g6_layer2):
    """Exact G7 mint-time evidence identity: G7 re-selected with the
    INDEPENDENTLY derived G6 set; path must equal
    <root>/grant-issued-<gid>.json (R-EVID-3); ORIGINAL bytes re-read
    via held-dirfd must match pinned digest/size (R-EVID-1/2) and
    grant_identity (R-EVID-4)."""
    package = _package_module()
    try:
        g7 = package.select_canonical_g7_publication(repo, tip, {
            "grant_identity": grant_identity,
            "g6_identity_set": {name: g6_layer2[name]
                                for name in package.G6_IDENTITY_FIELDS}})
    except package.ReceiptIdentityError as exc:
        _fail(EVIDENCE_UNAVAILABLE, str(exc))
    record = g7["record"]
    expected_name = f"grant-issued-{grant_identity}.json"
    root = os.path.realpath(os.fspath(evidence_root))
    if record["grant_issued_evidence_path"] != os.path.join(
            root, expected_name):
        _fail(EVIDENCE_PATH_CUSTODY_REFUSED,
              record["grant_issued_evidence_path"])
    dir_fd = _held_dir_fd(root, EVIDENCE_UNAVAILABLE)
    try:
        try:
            current = _read_at(dir_fd, expected_name)
        except OSError as exc:
            _fail(EVIDENCE_UNAVAILABLE, repr(exc))
    finally:
        os.close(dir_fd)
    digest = hashlib.sha256(current).hexdigest()
    if digest != record["grant_issued_evidence_sha256"]:
        _fail(EVIDENCE_BYTE_MISMATCH, "SHA-256 mismatch (R-EVID-1)")
    if len(current) != record["grant_issued_evidence_size"]:
        _fail(EVIDENCE_BYTE_MISMATCH, "size mismatch (R-EVID-2)")
    try:
        evidence_doc = json.loads(current.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail(EVIDENCE_IDENTITY_MISMATCH, "not JSON")
    if not isinstance(evidence_doc, dict) \
            or evidence_doc.get("grant_identity") != grant_identity:
        _fail(EVIDENCE_IDENTITY_MISMATCH, "grant_identity (R-EVID-4)")
    return {"g7_commit": g7["commit"], "g7_record_path": g7["record_path"],
            "evidence_path": os.path.join(root, expected_name),
            "evidence_sha256": digest, "evidence_size": len(current)}

# --- GAP C: terminal NON-AUTHORITY handoff content identity --------
HANDOFF_PREFIX = "lifecycle-caller-handoff-"

def handoff_name(tip):
    """Deterministic TIP-DERIVED naming (variable part exactly 40
    hex; nonconforming arguments refused)."""
    if not isinstance(tip, str) or not _SHA1_RE.match(tip):
        _fail(HANDOFF_NAME_REFUSED, repr(tip))
    return f"{HANDOFF_PREFIX}{tip}.json"
def _held_dir_fd(root, code):
    """R-NS-4/R-NS-5: the namespace opened ONCE by frozen absolute
    path with O_DIRECTORY|O_NOFOLLOW, fstat-verified, fd HELD."""
    try:
        fd = os.open(os.path.realpath(os.fspath(root)),
                     os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as exc:
        _fail(code, repr(exc))
    if not stat.S_ISDIR(os.fstat(fd).st_mode):
        os.close(fd)
        _fail(code, "held namespace object is not a directory")
    return fd

def _read_at(dir_fd, name):
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
    try:
        chunks = []
        while chunk := os.read(fd, 65536):
            chunks.append(chunk)
    finally:
        os.close(fd)
    return b"".join(chunks)

def create_lifecycle_handoff(root, tip, payload):
    """SINGLE_CREATION / CONTENT_IDENTITY_PINNED / TAMPER_EVIDENT —
    NEVER immutable (tampering DETECTED at re-read, never prevented);
    one write, fsync file then directory, digest over RE-READ bytes."""
    if not isinstance(payload, (bytes, bytearray)):
        _fail(HANDOFF_NAME_REFUSED, "payload not bytes")
    payload, name = bytes(payload), handoff_name(tip)
    root = os.path.realpath(os.fspath(root))
    dir_fd = _held_dir_fd(root, HANDOFF_ROOT_UNAVAILABLE)
    try:
        try:
            fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
        except FileExistsError:
            _fail(DUPLICATE_HANDOFF_EVIDENCE_REFUSED, name)
        try:
            written = 0
            while written < len(payload):
                written += os.write(fd, payload[written:])
            os.fsync(fd)
        finally:
            os.close(fd)
        os.fsync(dir_fd)    # durability of the creation event only
        reread = _read_at(dir_fd, name)
    finally:
        os.close(dir_fd)
    if reread != payload:
        _fail(HANDOFF_EVIDENCE_BYTE_MISMATCH, "re-read bytes differ")
    return {"handoff_path": os.path.join(root, name),
            "handoff_sha256": hashlib.sha256(reread).hexdigest(),
            "handoff_size": len(reread)}

def read_lifecycle_handoff(root, tip):
    """Consumer re-read through the identical held-dirfd discipline."""
    name = handoff_name(tip)
    root = os.path.realpath(os.fspath(root))
    dir_fd = _held_dir_fd(root, HANDOFF_ROOT_UNAVAILABLE)
    try:
        try:
            current = _read_at(dir_fd, name)
        except OSError as exc:
            _fail(HANDOFF_UNAVAILABLE, repr(exc))
    finally:
        os.close(dir_fd)
    return {"handoff_path": os.path.join(root, name),
            "handoff_sha256": hashlib.sha256(current).hexdigest(),
            "handoff_size": len(current), "handoff_bytes": current}
def require_current_handoff(root, tip, current_tip):
    """Stale-by-name refusal: the tip is the correlation key."""
    if tip != current_tip:
        _fail(HANDOFF_STALE_REFUSED, (tip, current_tip))
    return read_lifecycle_handoff(root, tip)


# --- GAP D: the closed-world static census (GAP-D-STATIC-V2) -------
PRODUCTION_MODULES = ("__init__.py", "accounting.py", "binding.py",
                      "custody.py", "receiptidentity.py", "reportcustody.py",
                      "runtime.py", "statemachine.py")
_PACKAGE_DIR_NAME = "bootstrap_authority"
MANIFEST_NAME = "MANIFEST.json"

# the FORTY-TWO pinned exact sites (record B Section 3 machine
# enumeration: 21 PF-1 / 2 PF-2 / 6 PF-3 / 2 PF-4 / 11 PF-5).
_PINNED_SITE_ROWS = (
    ("accounting.py", "PF3", (29,)), ("accounting.py", "PF5",
    (78, 81, 85, 88, 123)), ("binding.py", "PF1",
    (207, 214, 230, 234, 236, 723)), ("binding.py", "PF3",
    (153, 154, 155, 156, 157)), ("binding.py", "PF4", (400,)),
    ("custody.py", "PF5", (149, 155, 159)), ("runtime.py", "PF1", (89, 144)),
    ("runtime.py", "PF2", (148, 153)), ("runtime.py", "PF4", (1019,)),
    ("runtime.py", "PF5", (1076, 1079)),
    ("statemachine.py", "PF1", (20, 26, 30, 35, 36, 37, 38, 41, 42, 43, 44,
                                45, 46)), ("statemachine.py", "PF5", (64,)))
PINNED_IMPORT_SITES = frozenset(
    (module, line, form) for module, form, lines in _PINNED_SITE_ROWS
    for line in lines)

_PF1_CALLEES = frozenset(("dict", "frozenset", "tuple", "list", "set"))
_PF5_DECORATORS = frozenset(("property", "classmethod", "staticmethod"))
_PURE_BINOPS = (ast.BitOr, ast.Add, ast.Mult)
_COMPARISON_OPS = (ast.Eq, ast.NotEq, ast.In, ast.NotIn)

class _ModuleCensus:
    """Import-time census of ONE pinned module (data-only ast.parse;
    never imported here); grammar default-deny, PF-1..PF-5, PF-ARG."""
    def __init__(self, name, tree):
        self.name, self.tree = name, tree
        self.bound = set()              # names bound earlier in the module
        self.literal_containers = set()  # names bound to constant displays
        self.dict_names = set()           # names bound to pure dict values
        self.sites = []                  # (line, form) import-time sites
        self.annotations_used = self.future_annotations = False
    def fail(self, why):
        _fail(IMPORT_TIME_STATIC_REFUSED, f"{self.name}: {why}")
    # -- PF-ARG (record B Section 4.4) -------------------------------
    def pure(self, node, loop_vars=frozenset()):
        if node is None or isinstance(node, ast.Constant):
            return True
        if isinstance(node, ast.Name):
            return node.id in self.bound or node.id in loop_vars
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
            return all(self.pure(i, loop_vars) for i in node.elts)
        if isinstance(node, ast.Dict):
            return all(self.pure(k, loop_vars) for k in node.keys
                       if k is not None) and all(
                self.pure(v, loop_vars) for v in node.values)
        if isinstance(node, ast.JoinedStr):
            return all(isinstance(v, ast.Constant) or (
                isinstance(v, ast.FormattedValue)
                and v.format_spec is None and v.conversion == -1
                and isinstance(v.value, ast.Name)
                and (v.value.id in self.bound
                     or v.value.id in loop_vars)) for v in node.values)
        if isinstance(node, ast.Subscript):
            return (isinstance(node.value, ast.Name)
                    and node.value.id in self.literal_containers
                    and self._constant_slice(node.slice))
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp)):
            loop = set(loop_vars)
            if not self._comprehension_ok(node.generators, loop):
                return False
            if isinstance(node, ast.DictComp):
                return self.pure(node.key, loop) \
                    and self.pure(node.value, loop)
            return self.pure(node.elt, loop)
        if isinstance(node, ast.BinOp):
            return (isinstance(node.op, _PURE_BINOPS)
                    and self.pure(node.left, loop_vars)
                    and self.pure(node.right, loop_vars))
        return isinstance(node, ast.Call) \
            and self.pf_call(node) in ("PF1", "PF3")
    def _constant_slice(self, node):
        if isinstance(node, ast.Constant):
            return isinstance(node.value, (int, str))
        if isinstance(node, ast.Slice):
            return all(b is None or (isinstance(b, ast.Constant)
                                     and isinstance(b.value, int))
                       for b in (node.lower, node.upper, node.step))
        return False
    def _destructure_names(self, node, names):
        """A Name or (nested) tuple destructure of Names target."""
        if isinstance(node, ast.Name):
            names.add(node.id)
            return True
        if isinstance(node, (ast.Tuple, ast.List)):
            return all(self._destructure_names(item, names)
                       for item in node.elts)
        return False
    def _comparison_only(self, node):
        return (isinstance(node, ast.Compare)
                and len(node.ops) == len(node.comparators) == 1
                and isinstance(node.ops[0], _COMPARISON_OPS)
                and all(isinstance(side, (ast.Name, ast.Constant))
                        for side in (node.left, node.comparators[0])))

    def _comprehension_ok(self, generators, loop):
        for index, gen in enumerate(generators):
            if index and not self.pure(gen.iter, frozenset(loop)):
                return False
            if isinstance(gen.target, ast.Name):
                loop.add(gen.target.id)
            elif isinstance(gen.target, (ast.Tuple, ast.List)) and all(
                    isinstance(item, ast.Name)
                    for item in gen.target.elts):
                loop.update(item.id for item in gen.target.elts)
            else:
                return False
            if not all(self._comparison_only(c) for c in gen.ifs):
                return False
        return True
    def _generator_ok(self, node):
        """Generator expression consumed inline by an enclosing PF-1
        constructor (comparison-only filters; literal or constant
        iterable)."""
        loop = set()
        return isinstance(node, ast.GeneratorExp) \
            and self._comprehension_ok(node.generators, loop) \
            and self.pure(node.elt, loop)
    # -- PF-1..PF-4 classification (record B Section 4.3) ------------
    def pf_call(self, node):
        func = node.func
        if isinstance(func, ast.Name) and func.id in _PF1_CALLEES:
            for arg in node.args:
                if isinstance(arg, ast.Starred) or not (
                        self.pure(arg) or self._generator_ok(arg)):
                    self.fail(f"PF-1 argument form at "
                              f"{getattr(arg, 'lineno', node.lineno)}")
            unpacking = [kw for kw in node.keywords if kw.arg is None]
            named = [kw for kw in node.keywords if kw.arg is not None]
            if len(unpacking) > 1 or (unpacking and func.id != "dict"):
                self.fail(f"PF-1 **-unpacking at {node.lineno}")
            for keyword in named:
                if not self.pure(keyword.value):
                    self.fail(f"PF-1 keyword at {keyword.value.lineno}")
            if unpacking and not (isinstance(
                    unpacking[0].value, (ast.Dict, ast.DictComp))
                    and self.pure(unpacking[0].value)):
                self.fail(f"PF-1 ** value not a pure dict at {node.lineno}")
            self.sites.append((node.lineno, "PF1"))
            return "PF1"
        if isinstance(func, ast.Attribute) and func.attr == "compile" \
                and isinstance(func.value, ast.Name) \
                and func.value.id == "re":
            if len(node.args) != 1 \
                    or not isinstance(node.args[0], ast.Constant) \
                    or not isinstance(node.args[0].value, str) \
                    or any(kw.arg != "flags"
                           or not isinstance(kw.value, ast.Constant)
                           for kw in node.keywords):
                self.fail(f"PF-3 re.compile form at line {node.lineno}")
            self.sites.append((node.lineno, "PF3"))
            return "PF3"
        if isinstance(func, ast.Name) and func.id == "dataclass":
            if node.args or len(node.keywords) != 1 \
                    or node.keywords[0].arg != "frozen" \
                    or not isinstance(node.keywords[0].value, ast.Constant) \
                    or node.keywords[0].value.value is not True:
                self.fail(f"PF-4 dataclass(frozen=True) form at "
                          f"line {node.lineno}")
            return "PF4"        # site recorded at decorator position
        if isinstance(func, ast.Attribute) and func.attr == "items" \
                and not node.args and not node.keywords:
            return "PF2"      # permitted ONLY in the for-iterable position
        self.fail(f"unrecognized import-time call at {node.lineno}: "
                  f"{ast.unparse(node)[:80]}")
    # -- statement grammar (record B Section 4.2, default-deny) ------
    def _bind(self, target, value):
        if isinstance(target, ast.Name):
            self.bound.add(target.id)
            if isinstance(value, (ast.Dict, ast.DictComp)) \
                    and self.pure(value):
                self.dict_names.add(target.id)
            if (isinstance(value, (ast.Tuple, ast.List, ast.Set))
                    and all(isinstance(i, ast.Constant)
                            for i in value.elts)) or (
                    isinstance(value, ast.Dict) and all(
                        k is not None and isinstance(k, ast.Constant)
                        and isinstance(v, ast.Constant)
                        for k, v in zip(value.keys, value.values))):
                self.literal_containers.add(target.id)
        elif isinstance(target, ast.Subscript) \
                and isinstance(target.value, ast.Name) \
                and target.value.id in self.bound \
                and self.pure(target.slice):
            return           # module-local dict construction (L159 form)
        else:
            self.fail(f"assignment target at {target.lineno}")
    def _assign(self, stmt, class_body):
        """Assign/AnnAssign: value gate + target binding (module level
        allows the pinned subscript form; class bodies only Names)."""
        targets = stmt.targets if isinstance(stmt, ast.Assign) \
            else (stmt.target,)
        if isinstance(stmt, ast.AnnAssign):
            self._annotation(stmt.annotation)
            if not isinstance(stmt.target, ast.Name):
                self.fail(f"AnnAssign target at {stmt.lineno}")
        if stmt.value is not None:
            if isinstance(stmt.value, ast.Call):
                form = self.pf_call(stmt.value)
                if form in ("PF2", "PF4"):
                    self.fail(f"{form} outside its only permitted position "
                              f"at {stmt.lineno}")
            elif not self.pure(stmt.value):
                self.fail(f"value not in the PF-ARG grammar at "
                          f"{stmt.lineno}")
        for target in targets:
            if class_body:
                if not isinstance(target, ast.Name):
                    self.fail(f"class-body target at {stmt.lineno}")
                self.bound.add(target.id)
            else:
                self._bind(target, stmt.value)
    def _annotation(self, node):
        if node is None:
            return
        if not (isinstance(node, ast.Constant)
                and isinstance(node.value, (str, type(None)))) \
                and not isinstance(node, ast.Name):
            self.fail(f"annotation form at {node.lineno}")
        self.annotations_used = True
    def check_module_body(self, body):
        for stmt in body:
            if isinstance(stmt, ast.Expr) and isinstance(
                    stmt.value, ast.Constant) \
                    and isinstance(stmt.value.value, str):
                continue                                   # docstring
            if isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    self.bound.add(alias.asname or alias.name.split(".")[0])
                continue
            if isinstance(stmt, ast.ImportFrom):
                if stmt.module == "__future__" and any(
                        alias.name == "annotations"
                        for alias in stmt.names):
                    self.future_annotations = True
                for alias in stmt.names:
                    self.bound.add(alias.asname or alias.name)
                continue
            if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                self._assign(stmt, class_body=False)
            elif isinstance(stmt, ast.For):
                self._check_pf2_for(stmt)
            elif isinstance(stmt, ast.ClassDef):
                self._check_class(stmt)
            elif isinstance(stmt, ast.FunctionDef):
                self._check_function(stmt, class_body=False)
            else:
                self.fail(f"module-level statement outside the grammar at "
                          f"{stmt.lineno}: {type(stmt).__name__}")
    def _check_pf2_for(self, stmt):
        iterable = stmt.iter
        if not (isinstance(iterable, ast.Call)
                and isinstance(iterable.func, ast.Attribute)
                and iterable.func.attr == "items"
                and isinstance(iterable.func.value, ast.Name)
                and iterable.func.value.id in self.dict_names
                and not iterable.args and not iterable.keywords):
            self.fail(f"For iterable not the PF-2 form at {stmt.lineno}")
        self.sites.append((iterable.lineno, "PF2"))
        if stmt.orelse:
            self.fail(f"PF-2 for/else not permitted at {stmt.lineno}")
        loop_vars = set()
        if not self._destructure_names(stmt.target, loop_vars):
            self.fail(f"PF-2 target form at {stmt.lineno}")
        for body_stmt in stmt.body:
            target = body_stmt.targets[0] if isinstance(
                body_stmt, ast.Assign) and len(body_stmt.targets) == 1 \
                else None
            if not (isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Name)
                    and target.value.id in self.bound
                    and self.pure(target.slice, loop_vars)
                    and isinstance(body_stmt.value, ast.Dict)
                    and self.pure(body_stmt.value, loop_vars)):
                self.fail(f"PF-2 body form at {body_stmt.lineno}")
    def _check_decorators(self, stmt, class_body, class_decorator):
        for decorator in stmt.decorator_list:
            if class_decorator and isinstance(decorator, ast.Call):
                if self.pf_call(decorator) != "PF4":
                    self.fail(f"class decorator not PF-4 at "
                              f"{decorator.lineno}")
                self.sites.append((decorator.lineno, "PF4"))
            elif class_body and isinstance(decorator, ast.Name) \
                    and decorator.id in _PF5_DECORATORS:
                self.sites.append((decorator.lineno, "PF5"))
            else:
                self.fail(f"decorator form at {decorator.lineno}")
    def _check_class(self, stmt):
        self._check_decorators(stmt, class_body=False, class_decorator=True)
        for base in stmt.bases:
            if not isinstance(base, ast.Name) and not (
                    isinstance(base, ast.Attribute)
                    and isinstance(base.value, ast.Name)
                    and base.value.id in self.bound):
                self.fail(f"class base form at {base.lineno}")
        if stmt.keywords:
            self.fail(f"no metaclass/keyword bases at {stmt.lineno}")
        for inner in stmt.body:
            if isinstance(inner, ast.Expr) and isinstance(
                    inner.value, ast.Constant) \
                    and isinstance(inner.value.value, str):
                continue                       # class docstring
            if isinstance(inner, ast.Pass):
                continue
            if isinstance(inner, (ast.Assign, ast.AnnAssign)):
                self._assign(inner, class_body=True)
            elif isinstance(inner, ast.FunctionDef):
                self._check_function(inner, class_body=True)
            else:
                self.fail(f"class-body statement outside the grammar at "
                          f"{inner.lineno}: {type(inner).__name__}")
        self.bound.add(stmt.name)
    def _check_function(self, stmt, class_body):
        if stmt.decorator_list:
            self._check_decorators(stmt, class_body=class_body,
                                   class_decorator=False)
        self._annotation(stmt.returns)
        for arg in (*stmt.args.posonlyargs, *stmt.args.args,
                    *stmt.args.kwonlyargs):
            self._annotation(arg.annotation)
        for default in (*stmt.args.defaults, *stmt.args.kw_defaults):
            if default is not None and not self.pure(default):
                self.fail(f"default not PF-ARG at {stmt.lineno}")
        if not class_body:
            self.bound.add(stmt.name)
    def run(self):
        self.check_module_body(self.tree.body)
        if self.annotations_used and not self.future_annotations:
            self.fail("annotations used without the per-module "
                      "__future__ annotations import (PEP 563)")

def static_census(package_dir):
    """GAP-D-STATIC-V2 over the eight pinned modules (data-only
    ast.parse): passes iff every observed import-time call/decorator
    matches a pinned site in EVERY component AND every pinned site is
    observed; any drift fails closed."""
    package_path = os.path.join(os.path.realpath(os.fspath(package_dir)),
                                _PACKAGE_DIR_NAME)
    observed = set()
    for name in PRODUCTION_MODULES:
        try:
            with open(os.path.join(package_path, name), "rb") as handle:
                source = handle.read()
            tree = ast.parse(source, filename=name)
        except (OSError, SyntaxError) as exc:
            _fail(IMPORT_TIME_STATIC_REFUSED, f"{name}: {exc!r}")
        census = _ModuleCensus(name, tree)
        census.run()
        observed.update((name, line, form) for line, form in census.sites)
    missing, unknown = (PINNED_IMPORT_SITES - observed,
                        observed - PINNED_IMPORT_SITES)
    if missing or unknown:
        _fail(IMPORT_TIME_STATIC_REFUSED,
              f"site drift: missing={sorted(missing)} "
              f"unpinned={sorted(unknown)}")
    return {"pinned_sites": len(PINNED_IMPORT_SITES),
            "modules": len(PRODUCTION_MODULES)}

# --- GAP D: the caller's own AST gate (D4) --------------------------
_FORBIDDEN_REFERENCES = frozenset(("BootstrapAuthority", "run_attempt",
                                   "accounting", "custody", "statemachine"))
def check_caller_purity(source):
    """D4 gate over the caller's source: refuse direct runtime imports
    and runtime-authority surface references; the sanctioned surface
    is the receiptidentity selector import."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        _fail(CALLER_SOURCE_REFUSED, repr(exc))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "bootstrap_authority.runtime":
                    _fail(CALLER_SOURCE_REFUSED,
                          f"direct runtime import: {alias.name}")
        if isinstance(node, ast.ImportFrom) and node.module \
                and node.module.startswith("bootstrap_authority.runtime"):
            _fail(CALLER_SOURCE_REFUSED, "direct runtime import")
        if isinstance(node, ast.Name) and node.id in _FORBIDDEN_REFERENCES:
            _fail(CALLER_SOURCE_REFUSED, f"forbidden reference: {node.id}")
        if isinstance(node, ast.Attribute) \
                and node.attr in _FORBIDDEN_REFERENCES:
            _fail(CALLER_SOURCE_REFUSED,
                  f"forbidden reference: {node.attr}")

def _blob_sha1(data):
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()
def verify_package_identity(repo, tip, package_dir):
    """GAP-D condition 1: the eight modules' and MANIFEST's working
    bytes pinned against the verified tip's tree + every MANIFEST
    files[] row digest re-verified; mismatch refuses BEFORE import."""
    root = os.path.realpath(
        _git(repo, "rev-parse", "--show-toplevel").strip())
    prefix = os.path.relpath(os.path.realpath(os.fspath(package_dir)),
                             root)
    if prefix.startswith(".."):
        _fail(SOURCE_BLOB_PIN_MISMATCH, "package_dir outside repo")
    rel_paths = [f"{prefix}/{MANIFEST_NAME}"] + [
        f"{prefix}/{_PACKAGE_DIR_NAME}/{name}" for name in PRODUCTION_MODULES]
    for rel in rel_paths:
        try:
            pinned = _git(repo, "rev-parse", f"{tip}:{rel}").strip()
            with open(os.path.join(root, rel), "rb") as handle:
                data = handle.read()
        except (LifecycleCallerError, OSError) as exc:
            _fail(SOURCE_BLOB_PIN_MISMATCH, f"{rel}: {exc!r}")
        if _blob_sha1(data) != pinned:
            _fail(SOURCE_BLOB_PIN_MISMATCH, f"blob drift: {rel}")
    with open(os.path.join(root, prefix, MANIFEST_NAME), "rb") as handle:
        manifest = json.loads(handle.read())
    rows = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(rows, list) or not rows:
        _fail(SOURCE_BLOB_PIN_MISMATCH, "MANIFEST files rows absent")
    for row in rows:
        with open(os.path.join(root, prefix, row["path"]), "rb") as handle:
            data = handle.read()
        if hashlib.sha256(data).hexdigest() != row["sha256"] \
                or len(data) != row["bytes"]:
            _fail(SOURCE_BLOB_PIN_MISMATCH,
                  f"MANIFEST row drift: {row['path']}")
    return {"pinned_blobs": len(rel_paths), "manifest_rows": len(rows)}

def verify_import_gate(repo, tip, package_dir):
    """Full GAP-D gate: blob pin + STATIC-V2 census + D4 purity."""
    identity = verify_package_identity(repo, tip, package_dir)
    census = static_census(package_dir)
    with open(os.path.abspath(__file__), "rb") as handle:
        check_caller_purity(handle.read())
    return {"package_identity": identity, "static_census": census}
def import_verified_package(repo, tip, package_dir):
    """The ONLY import path: the gate MUST pass first, then an ORDINARY
    import (no synthetic parent / sys.modules substitution / custom
    loader / copy) with the transitive load asserted POSITIVELY."""
    verify_import_gate(repo, tip, package_dir)
    parent = os.path.realpath(os.fspath(package_dir))
    if parent not in sys.path:
        sys.path.insert(0, parent)
    import bootstrap_authority.receiptidentity as receiptidentity
    if "bootstrap_authority.runtime" not in sys.modules:
        _fail(IMPORT_DISCLOSURE_REFUSED,
              "the disclosed transitive runtime load is absent")
    return receiptidentity

def run_authenticated_binding(config_path, repo, package_dir, *,
                              ls_remote=None, api_read=None):
    """Bounded glue (T8): trust root -> gate -> import; grants
    NOTHING; later stages receive the SAME verified tip."""
    binding = verify_trust_root(config_path, repo, ls_remote=ls_remote,
                                api_read=api_read)
    module = import_verified_package(repo, binding["authoritative_tip"],
                                     package_dir)
    return {"binding": binding, "receiptidentity": module}
