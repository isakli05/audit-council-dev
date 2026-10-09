"""AUCDEV-023 PCH6-B PATH-B RECEIPTIMMUT-001 implementation-layer
remediation — the NON-RUNTIME canonical G10 original receipt
content-identity mechanism (G10.1-G10.6 + G11), implemented from the
Control Room design-readback-ACCEPTED design sequence (design
remediation + design reconciliation + verified-namespace-fd correction
+ independent Control Room design readback, blobs 1a55f55b... /
5246833a... / 4541c16e... / 13d1ffae...).

IMPLEMENTATION_CANDIDATE_ONLY / NO_EXECUTION_AUTHORITY: this module
establishes ORIGINAL_CREATION_TIME_NON_RUNTIME_RECEIPT_IDENTITY — the
original canonical receipt bytes are constructed in memory from
verified inputs only (G10.1), their SHA-256/size are fixed BEFORE
filesystem trust (G10.2), the accepted one-shot writer is reused
UNCHANGED (G10.3), an immediate verified-namespace-fd readback
compares CURRENT to ORIGINAL (G10.4), a canonical NON-EXECUTION
24-field receipt-identity publication record pins that original
identity (G10.5) and is verified after publication (G10.6 readback
half), with G11 independently re-deriving everything from verified
inputs and the first-parent Git history.  The module creates NO
execution authority, NO grant, NO package, NO attempt, NO
AccountingStore state and NO supersession mechanism; it is NOT
imported by __init__.py or runtime.py (the BootstrapAuthority public
surface stays exactly {state, store, run_attempt}) and confers ZERO
authority on import.  Git operations are READ-ONLY (log / diff-tree /
ls-tree / cat-file / rev-list): this module NEVER commits, pushes or
mutates any repository; the separately authorized future G10.6
publication execution (commit ONCE / push ONCE against the live
governance repository) is NOT part of this code — tests exercise the
selector/readback machinery against disposable synthetic LOCAL Git
worlds only.

Verified-namespace rule (R-NS-1..R-NS-10) is enforced mechanically:
the published absolute receipt_path is a DERIVED identity field only
(R-NS-1); every G10.4/G10.6/G11 receipt content read opens the
canonical namespace ONCE by its frozen absolute path
O_RDONLY|O_DIRECTORY|O_NOFOLLOW, fstat-verifies THE OPENED object
against the pinned st_dev/st_ino plus the owner/group/world gates and
opens the deterministic receipt name relative to THAT held fd with
O_NOFOLLOW (R-NS-4/R-NS-5, reusing the accepted binding primitive);
an independent absolute-path receipt open does not exist here and is
NOT an equivalent or fallback (R-NS-6).  Receipt FILE inode continuity
is NOT a held invariant (accepted DESIGN-001 disposition); the
namespace DIRECTORY object identity IS.

Residual boundary (honest scope): the G7 five-value identity is
carried by the VERIFIED G7 context supplied by the caller (strict
shape + cross-binding verified here); an independent G7-selector
re-derivation over Git is future Control Room tooling — no G7
selector primitive exists in the accepted source to call.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess

from . import binding as bab


class ReceiptIdentityError(bab.BindingError):
    """Refused receipt-identity operation (fail closed; the message
    carries the exact design-level refusal constant)."""


# --- G10 refusal constants (design Section 18; defined, mechanically
# raised by the corresponding verification stage) -----------------------
G10_RECEIPT_BYTES_DERIVATION_REFUSED = \
    "G10_RECEIPT_BYTES_DERIVATION_REFUSED"
G10_ORIGINAL_IDENTITY_DERIVATION_REFUSED = \
    "G10_ORIGINAL_IDENTITY_DERIVATION_REFUSED"
G10_POSTWRITE_READBACK_MISMATCH = "G10_POSTWRITE_READBACK_MISMATCH"
G10_PUBLICATION_CONSTRUCTION_INVALID = \
    "G10_PUBLICATION_CONSTRUCTION_INVALID"
G10_POST_PUSH_READBACK_FAILED = "G10_POST_PUSH_READBACK_FAILED"
G10_INCOMPLETE_FAIL_CLOSED = "G10_INCOMPLETE_FAIL_CLOSED"
G11_REFUSED = "G11_REFUSED"

# --- canonical G10 publication selector refusal constants (design
# Sections 12/18; the C4 family adopts the accepted DIFFSEM semantics) --
CANONICAL_G10_RECEIPT_IDENTITY_PUBLICATION_NOT_FOUND = \
    "CANONICAL_G10_RECEIPT_IDENTITY_PUBLICATION_NOT_FOUND"
CANONICAL_G10_RECEIPT_IDENTITY_PUBLICATION_AMBIGUOUS = \
    "CANONICAL_G10_RECEIPT_IDENTITY_PUBLICATION_AMBIGUOUS"
C4_ADD_ENTRY_MISSING = "C4_ADD_ENTRY_MISSING"
C4_ADD_ENTRY_AMBIGUOUS = "C4_ADD_ENTRY_AMBIGUOUS"
C4_NOT_RAW_ADD = "C4_NOT_RAW_ADD"
C4_PARSE_FAILURE = "C4_PARSE_FAILURE"
C4_RENAME_COPY_INFERENCE_PRESENT = "C4_RENAME_COPY_INFERENCE_PRESENT"
C4_TREE_STATE_CONTRADICTION = "C4_TREE_STATE_CONTRADICTION"

# --- the strict closed-world 24-field receipt-identity publication
# schema AUCDEV-023-PACKAGE-BINDING-RECEIPT-IDENTITY-PUBLICATION-V1
# (design Section 8; the EXACT fixed field order is normative) ---------
RECEIPT_IDENTITY_PUBLICATION_SCHEMA = ("AUCDEV-023-PACKAGE-BINDING-"
                                       "RECEIPT-IDENTITY-PUBLICATION-V1")
RECEIPT_IDENTITY_PUBLICATION_PURPOSE = \
    "NON_EXECUTION_ORIGINAL_RECEIPT_CONTENT_IDENTITY"
RIP_BINDING_SEMANTICS = \
    "ORIGINAL_CREATION_TIME_NON_RUNTIME_RECEIPT_IDENTITY"
RIP_FIELDS = ("schema", "purpose", "governance_event_id", "auditor_role",
              "attempt_slot", "attempt_id", "operator_authority_id",
              "grant_identity", "package_sha256", "receipt_path",
              "receipt_sha256", "receipt_size", "receipt_namespace_path",
              "receipt_namespace_st_dev", "receipt_namespace_st_ino",
              "g7_mint_publication_commit_sha",
              "g7_mint_publication_root_tree",
              "g7_mint_publication_record_path",
              "g7_mint_publication_record_blob_sha1",
              "g7_mint_publication_record_sha256", "one_receipt_only",
              "execution_authority", "secret_material", "binding_semantics")
RIP_SHA256_FIELDS = ("grant_identity", "package_sha256", "receipt_sha256",
                     "g7_mint_publication_record_sha256")
RIP_SHA1_FIELDS = ("g7_mint_publication_commit_sha",
                   "g7_mint_publication_root_tree",
                   "g7_mint_publication_record_blob_sha1")
RIP_INT_FIELDS = (("receipt_size", 0), ("receipt_namespace_st_dev", 0),
                  ("receipt_namespace_st_ino", 1))
# the RESERVED future operative canonical record path (design Section 7):
# a strict VERBATIM constant only — creating the path at any live
# governance repository is the separately authorized future G10.6
# execution, NEVER this module.
RECEIPT_IDENTITY_PUBLICATION_RECORD_PATH = (
    "docs/chatgpt-project/AUCDEV-023-PCH6-B-PATH-B-REPLACEMENT-AUDITOR-"
    "A-PACKAGE-BINDING-RECEIPT-IDENTITY-PUBLICATION.md")


def _rip_error(field: str, detail) -> ReceiptIdentityError:
    return ReceiptIdentityError(
        f"RIP_{field.upper()}_INVALID: {detail!r}")


def receipt_identity_publication_canonical_bytes(document: dict) -> bytes:
    """EXACT canonical publication serialization (design Section 9,
    exactly one rule): strict JSON, UTF-8 pure ASCII, single top-level
    object, the EXACT closed-world 24-field set in the EXACT fixed
    order (NOT lexicographic), compact separators, no BOM, no comments,
    no duplicate keys, NO trailing newline."""
    if not isinstance(document, dict):
        raise ReceiptIdentityError("RIP_NOT_AN_OBJECT")
    try:
        bab._exact_keys(document, RIP_FIELDS, "RIP")
    except bab.BindingError:
        raise ReceiptIdentityError(
            "RIP_KEYS_INVALID: the record is not the exact closed-world "
            "24-field set") from None
    return json.dumps({name: document[name] for name in RIP_FIELDS},
                      separators=(",", ":")).encode()


def parse_receipt_identity_publication(data) -> dict:
    """Parse and fully validate ONE receipt-identity publication record
    (fail closed): strict JSON with duplicate-key refusal, exact
    closed-world key set, exact schema/purpose tags, per-field shape
    gates (exact-string fields; 64-hex/40-hex identity fields; plain
    non-negative ints with bool refused; one_receipt_only JSON true)
    and canonical-bytes re-serialization equality."""
    raw = data.encode() if isinstance(data, str) else data
    doc = bab.strict_loads(raw)
    if not isinstance(doc, dict):
        raise ReceiptIdentityError("RIP_NOT_AN_OBJECT")
    try:
        bab._exact_keys(doc, RIP_FIELDS, "RIP")
    except bab.BindingError:
        raise ReceiptIdentityError(
            "RIP_KEYS_INVALID: the record is not the exact closed-world "
            "24-field set") from None
    if doc["schema"] != RECEIPT_IDENTITY_PUBLICATION_SCHEMA:
        raise ReceiptIdentityError(
            f"RIP_SCHEMA_UNEXPECTED: {doc['schema']!r}")
    if doc["purpose"] != RECEIPT_IDENTITY_PUBLICATION_PURPOSE:
        raise ReceiptIdentityError(
            f"RIP_PURPOSE_UNEXPECTED: {doc['purpose']!r}")
    for field, expected in (
            ("governance_event_id", bab.EVENT_ID),
            ("auditor_role",
             bab.REPLACEMENT_SLOT_ROLES["AUDITOR_A_REPLACEMENT_1"]),
            ("attempt_slot", "AUDITOR_A_REPLACEMENT_1"),
            ("attempt_id",
             bab.REPLACEMENT_ATTEMPT_SLOTS["AUDITOR_A_REPLACEMENT_1"]),
            ("g7_mint_publication_record_path",
             bab.G7_MINT_PUBLICATION_RECORD_PATH),
            ("execution_authority", "NONE"),
            ("secret_material", "NONE"),
            ("binding_semantics", RIP_BINDING_SEMANTICS)):
        if doc[field] != expected:
            raise _rip_error(field, doc[field])
    for field in RIP_SHA256_FIELDS:
        if not isinstance(doc[field], str) \
                or not bab.SHA256_RE.match(doc[field]):
            raise _rip_error(field, doc[field])
    for field in RIP_SHA1_FIELDS:
        if not isinstance(doc[field], str) \
                or not bab.SHA1_RE.match(doc[field]):
            raise _rip_error(field, doc[field])
    for field, minimum in RIP_INT_FIELDS:
        if isinstance(doc[field], bool) or not isinstance(doc[field], int) \
                or doc[field] < minimum:
            raise _rip_error(field, doc[field])
    if doc["one_receipt_only"] is not True:
        raise _rip_error("one_receipt_only", doc["one_receipt_only"])
    try:
        bab._identity_field(doc["operator_authority_id"],
                            "RIP_OPERATOR_AUTHORITY_ID")
        bab._frozen_abs_path(doc["receipt_path"], "RIP_RECEIPT_PATH")
        bab._frozen_abs_path(doc["receipt_namespace_path"],
                             "RIP_RECEIPT_NAMESPACE_PATH")
    except bab.BindingError:
        raise _rip_error("operator_authority_id-or-path-shape",
                         doc) from None
    if receipt_identity_publication_canonical_bytes(doc) != raw:
        raise ReceiptIdentityError(
            "RIP_CANONICALIZATION_INVALID: the bytes are not the exact "
            "canonical serialization (fixed field order, compact "
            "separators, no whitespace/BOM/trailing newline)")
    return {name: doc[name] for name in RIP_FIELDS}


def derive_original_receipt_identity(verified_g7_context, grant_bytes,
                                     package_artifact) -> dict:
    """G10.1 + G10.2: construct the exact canonical receipt bytes IN
    MEMORY from verified inputs ONLY — the VERIFIED canonical G7
    context, the EXACT canonical grant bytes (re-parsed; the derived
    grant_identity MUST equal the context's) and the EXACT frozen
    package artifact (digest derived from the artifact bytes, never a
    naked digest) — and fix receipt_sha256/receipt_size BEFORE any
    filesystem receipt content can influence identity.  NO receipt
    file is opened, read or trusted here."""
    try:
        context = bab.parse_verified_g7_context(verified_g7_context)
        document, canonical = bab._validated_grant_document(grant_bytes)
        identity = bab.grant_identity(canonical)
        if identity != context["grant_identity"]:
            raise bab.BindingError(
                "RECEIPT_GRANT_CONTEXT_MISMATCH: the verified G7 context "
                "does not name the exact supplied grant identity")
        package_sha256 = bab.derive_frozen_package_sha256(
            package_artifact)
    except bab.BindingError as exc:
        raise ReceiptIdentityError(
            f"{G10_RECEIPT_BYTES_DERIVATION_REFUSED}: {exc}") from exc
    record = {
        "schema": bab.RECEIPT_SCHEMA,
        "grant_identity": identity,
        "package_sha256": package_sha256,
        "governance_event_id": document["governance_event_id"],
        "auditor_role": document["auditor_role"],
        "attempt_slot": document["attempt_slot"],
        "attempt_id": document["future_machine_attempt_id"],
        "operator_authority_id": document["operator_authority_id"],
        "created_under_package_binding_authority": True,
        "binding_semantics": bab.RECEIPT_BINDING_SEMANTICS,
    }
    receipt_bytes = bab.receipt_canonical_bytes(record)
    try:
        bab._crosscheck_receipt(
            bab.parse_package_binding_receipt(receipt_bytes), document,
            identity, package_sha256)
    except bab.BindingError as exc:
        raise ReceiptIdentityError(
            f"{G10_RECEIPT_BYTES_DERIVATION_REFUSED}: {exc}") from exc
    name = bab.receipt_name(identity)
    return {"context": context, "grant_document": document,
            "grant_identity": identity, "package_sha256": package_sha256,
            "receipt_document": record, "receipt_bytes": receipt_bytes,
            "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
            "receipt_size": len(receipt_bytes), "receipt_name": name,
            # R-NS-1: the absolute receipt_path is the DERIVED identity
            # field (namespace path + "/" + deterministic name), never
            # a read handle.
            "receipt_path": context["receipt_namespace_path"]
            + "/" + name}


def _read_current_receipt(context: dict, name: str) -> bytes:
    """R-NS-4/R-NS-5 CURRENT-receipt content read: open the canonical
    namespace ONCE by its frozen absolute path with O_DIRECTORY|
    O_NOFOLLOW (the accepted binding primitive fstat-verifies THE
    OPENED object against the pinned st_dev/st_ino plus the
    owner/group/world gates), HOLD that fd and open the deterministic
    receipt name relative to it with O_NOFOLLOW, reading from the
    opened file object.  An independent absolute-path receipt open
    does not exist in this module (R-NS-6)."""
    dir_fd = bab._open_verified_receipt_namespace(context)
    try:
        try:
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
        except OSError as exc:
            raise ReceiptIdentityError(
                f"RECEIPT_ABSENT_OR_UNOPENABLE: {exc!r}") from exc
        try:
            chunks = []
            while True:
                chunk = os.read(fd, 65536)
                if not chunk:
                    break
                chunks.append(chunk)
        finally:
            os.close(fd)
    finally:
        os.close(dir_fd)
    return b"".join(chunks)


def _require_current_equals_original(current: bytes, original: dict,
                                     constant: str) -> None:
    """Original-vs-current comparison (content identity: bytes, SHA-256
    and exact byte size; RI-T01..RI-T08/RI-T21/RI-T22)."""
    digest = hashlib.sha256(current).hexdigest()
    if current != original["receipt_bytes"] \
            or digest != original["receipt_sha256"] \
            or len(current) != original["receipt_size"]:
        raise ReceiptIdentityError(
            f"{constant}: CURRENT receipt != ORIGINAL identity "
            f"(bytes-equal={current == original['receipt_bytes']}, "
            f"size {len(current)} vs {original['receipt_size']}, "
            f"sha256 {digest} vs {original['receipt_sha256']})")


def execute_g10_creation_and_readback(verified_g7_context, grant_bytes,
                                      package_artifact) -> dict:
    """G10.3 + G10.4: create the ONE receipt via the ACCEPTED one-shot
    writer (reused UNCHANGED — O_CREAT|O_EXCL|O_NOFOLLOW mode 0600,
    fsync file then directory, DUPLICATE_PACKAGE_BINDING_REFUSED
    propagates), then perform the immediate post-write exact readback
    per R-NS-4/R-NS-5 and require: current bytes/SHA-256/size == the
    G10.1/G10.2 ORIGINAL values and the writer's returned dict equal
    to the independently derived values (the returned path comparing
    EXACTLY to the re-derived deterministic receipt NAME, name-to-name
    per R-NS-2/R-NS-3).  G10 FAILS CLOSED on any mismatch."""
    original = derive_original_receipt_identity(
        verified_g7_context, grant_bytes, package_artifact)
    writer_return = bab.write_package_binding_receipt(
        verified_g7_context, grant_bytes, package_artifact,
        original["receipt_document"])
    _g10_4_readback(original, writer_return)
    return {"writer_return": writer_return, "original": original,
            "receipt_path": original["receipt_path"]}


def _g10_4_readback(original: dict, writer_return: dict) -> None:
    """The G10.4 immediate post-write exact readback (corrected
    wording): CURRENT receipt read per R-NS-4/R-NS-5, canonicalization
    re-checked, CURRENT bytes/SHA-256/size == the G10.1/G10.2 ORIGINAL
    values and the writer's returned dict equal to the independently
    derived values (the returned path comparing EXACTLY to the
    re-derived deterministic receipt NAME, name-to-name per
    R-NS-2/R-NS-3)."""
    current = _read_current_receipt(original["context"],
                                    original["receipt_name"])
    try:
        bab.parse_package_binding_receipt(current)
    except bab.BindingError as exc:
        raise ReceiptIdentityError(
            f"RECEIPT_CANONICALIZATION_INVALID: {exc}") from exc
    expected_return = {
        "path": original["receipt_name"],
        "sha256": original["receipt_sha256"],
        "size": original["receipt_size"],
        "grant_identity": original["grant_identity"],
        "package_sha256": original["package_sha256"]}
    if writer_return != expected_return:
        raise ReceiptIdentityError(
            f"{G10_POSTWRITE_READBACK_MISMATCH}: writer return "
            f"{writer_return!r} != the G10.1/G10.2 derived values "
            f"{expected_return!r}")
    _require_current_equals_original(current, original,
                                     G10_POSTWRITE_READBACK_MISMATCH)


def construct_g10_publication_record(original: dict) -> dict:
    """G10.5: construct the canonical NON-EXECUTION publication record
    pinning the ORIGINAL G10.1/G10.2 identity together with the
    grant/package/G7/namespace cross-bindings (every value from the
    verified inputs, NEVER from the receipt file; NO self-Git-identity
    field — the post-hoc five-value publication identity is derived
    only AFTER the publication commit exists and lives OUTSIDE the
    record).  The construction is validated by a full canonical
    round-trip before it is returned."""
    context, document = original["context"], original["grant_document"]
    record = {
        "schema": RECEIPT_IDENTITY_PUBLICATION_SCHEMA,
        "purpose": RECEIPT_IDENTITY_PUBLICATION_PURPOSE,
        "governance_event_id": document["governance_event_id"],
        "auditor_role": document["auditor_role"],
        "attempt_slot": document["attempt_slot"],
        "attempt_id": document["future_machine_attempt_id"],
        "operator_authority_id": document["operator_authority_id"],
        "grant_identity": original["grant_identity"],
        "package_sha256": original["package_sha256"],
        "receipt_path": original["receipt_path"],
        "receipt_sha256": original["receipt_sha256"],
        "receipt_size": original["receipt_size"],
        "receipt_namespace_path": context["receipt_namespace_path"],
        "receipt_namespace_st_dev": context["receipt_namespace_st_dev"],
        "receipt_namespace_st_ino": context["receipt_namespace_st_ino"],
        "g7_mint_publication_commit_sha":
            context["grant_mint_publication_commit_sha"],
        "g7_mint_publication_root_tree":
            context["grant_mint_publication_root_tree"],
        "g7_mint_publication_record_path":
            context["grant_mint_publication_record_path"],
        "g7_mint_publication_record_blob_sha1":
            context["grant_mint_publication_record_blob_sha1"],
        "g7_mint_publication_record_sha256":
            context["grant_mint_publication_record_sha256"],
        "one_receipt_only": True,
        "execution_authority": "NONE",
        "secret_material": "NONE",
        "binding_semantics": RIP_BINDING_SEMANTICS,
    }
    try:
        data = receipt_identity_publication_canonical_bytes(record)
        if parse_receipt_identity_publication(data) != record:
            raise bab.BindingError("round-trip mismatch")
    except bab.BindingError as exc:
        raise ReceiptIdentityError(
            f"{G10_PUBLICATION_CONSTRUCTION_INVALID}: {exc}") from exc
    return record


# --- read-only Git selector machinery (R1-R22; disposable synthetic
# LOCAL repositories in tests; NO commit/push/remote surface here) ------

def _git(repo, *args) -> str:
    out = subprocess.run(("git", "-C", os.fspath(repo), *args),
                         capture_output=True)
    if out.returncode != 0:
        raise ReceiptIdentityError(
            f"SELECTOR_GIT_INVOCATION_FAILED: git {' '.join(args)}: "
            + out.stderr.decode("utf-8", errors="replace").strip()[:200])
    return out.stdout.decode("utf-8", errors="replace")


def _git_bytes(repo, *args) -> bytes:
    out = subprocess.run(("git", "-C", os.fspath(repo), *args),
                         capture_output=True)
    if out.returncode != 0:
        raise ReceiptIdentityError(
            f"SELECTOR_GIT_INVOCATION_FAILED: git {' '.join(args)}: "
            + out.stderr.decode("utf-8", errors="replace").strip()[:200])
    return out.stdout


def _tree_has_path(repo, rev, path) -> bool:
    """Tree-state existence probe from the ACTUAL tree (R2/R3 never
    rely on diff output)."""
    return _git(repo, "ls-tree", rev, "--", path).strip() != ""


def _require_raw_add(repo, parent, commit, path) -> None:
    """R4: the canonical RAW ADD under the accepted DIFFSEM semantics
    RAW_PATH_ADDITION_WITH_RENAME_AND_COPY_DETECTION_DISABLED — exactly
    one normalized fixed-path entry with status exactly A, ambient Git
    configuration overridden (-c diff.renames=false --no-renames), any
    rename/copy presentation refused, NO rename-aware retry."""
    out = _git(repo, "-c", "diff.renames=false", "diff-tree",
               "--no-renames", "--name-status", "--no-commit-id", "-r",
               parent, commit, "--", path)
    rows = [line for line in out.splitlines() if line.strip()]
    if not rows:
        raise ReceiptIdentityError(
            f"{C4_ADD_ENTRY_MISSING}: no fixed-path delta entry")
    if len(rows) > 1:
        raise ReceiptIdentityError(
            f"{C4_ADD_ENTRY_AMBIGUOUS}: {len(rows)} fixed-path entries")
    parts = rows[0].split("\t")
    status = parts[0]
    if status.startswith("R") or status.startswith("C"):
        raise ReceiptIdentityError(
            f"{C4_RENAME_COPY_INFERENCE_PRESENT}: {rows[0]!r}")
    if status != "A" or len(parts) != 2 or parts[1] != path:
        if status != "A":
            raise ReceiptIdentityError(f"{C4_NOT_RAW_ADD}: {rows[0]!r}")
        raise ReceiptIdentityError(f"{C4_PARSE_FAILURE}: {rows[0]!r}")


def _first_parent_introductions(repo, ref, path) -> list:
    """Enumerate displayed-A fixed-path transitions over the
    authoritative FIRST-PARENT history domain (R22); every enumerated
    candidate is then independently verified by R1-R4 tree facts."""
    out = _git(repo, "log", "--first-parent", "--no-renames",
               "--name-status", "--format=intro %H %P", ref, "--", path)
    introductions, current = [], None
    for line in out.splitlines():
        if line.startswith("intro "):
            header = line.split()
            current = (header[1], header[2:])
        elif line.strip() and current is not None:
            fields = line.split("\t")
            if fields[0] == "A" and fields[-1] == path:
                introductions.append(current)
    return introductions


def select_canonical_g10_publication(repo, ref, expected: dict) -> dict:
    """The canonical G10 publication selector R (design Section 12):
    derived ONLY from the authoritative default-branch FIRST-PARENT
    history of `ref`; a candidate qualifies when it satisfies ALL of
    R1-R22 — exactly one parent (R1); the fixed path ABSENT in the
    parent TREE and PRESENT in the candidate TREE (R2/R3, verified
    from the actual trees, with a displayed-A contradiction refused
    C4_TREE_STATE_CONTRADICTION); the canonical no-renames RAW ADD
    (R4, `_require_raw_add`); the full record predicate set R5-R21
    (the parsed publication record at the candidate EQUALS `expected`
    on every closed-world field — schema/purpose/event/role/slot/
    attempt/operator/grant/package/path/SHA/size/namespace/G7/
    one_receipt_only/execution_authority/secret_material/
    binding_semantics); R22 holds by the enumeration domain.
    Cardinality MUST be EXACTLY ONE: zero -> NOT_FOUND, more than one
    -> AMBIGUOUS, both FAIL CLOSED; NO first/latest fallback, NO
    latest-HEAD authority, NO package-provided R."""
    path = RECEIPT_IDENTITY_PUBLICATION_RECORD_PATH
    candidates = []
    for commit_id, parents in _first_parent_introductions(repo, ref,
                                                          path):
        if len(parents) != 1:
            continue                       # R1: merge/root ineligible
        parent = parents[0]
        if _tree_has_path(repo, parent, path):
            raise ReceiptIdentityError(
                f"{C4_TREE_STATE_CONTRADICTION}: displayed A but the "
                f"path EXISTS in the parent tree of {commit_id}")
        if not _tree_has_path(repo, commit_id, path):
            raise ReceiptIdentityError(
                f"{C4_TREE_STATE_CONTRADICTION}: displayed A but the "
                f"path is ABSENT from the candidate tree {commit_id}")
        _require_raw_add(repo, parent, commit_id, path)
        blob_sha1 = _git(repo, "ls-tree", commit_id, "--", path
                         ).split("\t")[0].split()[2]
        record_bytes = _git_bytes(repo, "cat-file", "blob",
                                  f"{commit_id}:{path}")
        try:
            parsed = parse_receipt_identity_publication(record_bytes)
        except ReceiptIdentityError:
            continue                       # R5: non-qualifying content
        if parsed != expected:
            continue                       # R6-R21 predicate mismatch
        candidates.append({
            "commit": commit_id, "parent": parent,
            "root_tree": _git(repo, "rev-parse",
                              f"{commit_id}^{{tree}}").strip(),
            "record_path": path, "record_blob_sha1": blob_sha1,
            "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
            "record_bytes": record_bytes, "record": parsed})
    if not candidates:
        raise ReceiptIdentityError(
            f"{CANONICAL_G10_RECEIPT_IDENTITY_PUBLICATION_NOT_FOUND}: "
            f"zero qualifying introductions on the first-parent "
            f"history of {ref!r}")
    if len(candidates) > 1:
        raise ReceiptIdentityError(
            f"{CANONICAL_G10_RECEIPT_IDENTITY_PUBLICATION_AMBIGUOUS}: "
            f"{[c['commit'] for c in candidates]}")
    return candidates[0]


def derive_post_publication_identity(selection: dict) -> dict:
    """The post-hoc FIVE-VALUE publication identity, derived ONLY AFTER
    the publication commit exists and recorded OUTSIDE the publication
    record itself (design Section 10 acyclicity: it enters no
    canonical bytes and creates no readback-of-readback chain)."""
    return {
        "receipt_identity_publication_commit_sha": selection["commit"],
        "receipt_identity_publication_root_tree":
            selection["root_tree"],
        "receipt_identity_publication_record_path":
            selection["record_path"],
        "receipt_identity_publication_record_blob_sha1":
            selection["record_blob_sha1"],
        "receipt_identity_publication_record_sha256":
            selection["record_sha256"]}


def execute_g10_publication_readback(repo, ref, original: dict) -> dict:
    """G10.6 post-push READBACK half (the commit/push itself is the
    separately authorized future execution; this function performs NO
    git mutation): derive the canonical publication commit R
    independently by the R1-R22 selector; re-read the publication
    bytes from the EXACT publication commit R and require them
    byte-equal to the G10.5 canonical construction; re-read the
    CURRENT receipt per R-NS-4/R-NS-5 and require CURRENT == ORIGINAL
    (bytes, SHA-256, size).  G10 is NOT COMPLETE unless this readback
    succeeds; any failure leaves G10 FAIL CLOSED."""
    expected = construct_g10_publication_record(original)
    expected_bytes = receipt_identity_publication_canonical_bytes(
        expected)
    selection = select_canonical_g10_publication(repo, ref, expected)
    if selection["record_bytes"] != expected_bytes:
        raise ReceiptIdentityError(
            f"{G10_POST_PUSH_READBACK_FAILED}: the bytes at the "
            f"canonical publication commit are not the G10.5 canonical "
            f"construction")
    current = _read_via_verified_namespace(original,
                                           G10_POST_PUSH_READBACK_FAILED)
    _require_current_equals_original(current, original,
                                     G10_POST_PUSH_READBACK_FAILED)
    return {"selection": selection,
            "post_publication_identity":
                derive_post_publication_identity(selection),
            "current_receipt_sha256":
                hashlib.sha256(current).hexdigest(),
            "current_receipt_size": len(current)}


def _read_via_verified_namespace(original: dict, constant: str) -> bytes:
    """The R-NS-4/R-NS-5 CURRENT-receipt read for the G10.6/G11
    original-vs-current comparisons, with any refusal of the accepted
    namespace/read primitives surfaced under the caller's stage-level
    FAIL-CLOSED constant (the specific underlying constant retained)."""
    try:
        return _read_current_receipt(original["context"],
                                     original["receipt_name"])
    except bab.BindingError as exc:
        raise ReceiptIdentityError(f"{constant}: {exc}") from exc


def _require_published_matches_derived(published: dict,
                                       original: dict) -> None:
    """The Section 8 cross-binding refusal groups: every published
    field must equal the value independently re-derived from the exact
    verified grant/package/G7/namespace context."""
    context = original["context"]
    groups = (
        ("RIP_RECEIPT_ORIGINAL_MISMATCH",
         (("receipt_path", original["receipt_path"]),
          ("receipt_sha256", original["receipt_sha256"]),
          ("receipt_size", original["receipt_size"]))),
        ("RIP_GRANT_CONTEXT_MISMATCH",
         (("grant_identity", original["grant_identity"]),
          ("operator_authority_id",
           original["grant_document"]["operator_authority_id"]),
          ("attempt_id",
           original["grant_document"]["future_machine_attempt_id"]))),
        ("RIP_PACKAGE_MISMATCH",
         (("package_sha256", original["package_sha256"]),)),
        ("RIP_G7_CONTEXT_MISMATCH",
         (("g7_mint_publication_commit_sha",
           context["grant_mint_publication_commit_sha"]),
          ("g7_mint_publication_root_tree",
           context["grant_mint_publication_root_tree"]),
          ("g7_mint_publication_record_path",
           context["grant_mint_publication_record_path"]),
          ("g7_mint_publication_record_blob_sha1",
           context["grant_mint_publication_record_blob_sha1"]),
          ("g7_mint_publication_record_sha256",
           context["grant_mint_publication_record_sha256"]))),
        ("RIP_NAMESPACE_MISMATCH",
         (("receipt_namespace_path", context["receipt_namespace_path"]),
          ("receipt_namespace_st_dev",
           context["receipt_namespace_st_dev"]),
          ("receipt_namespace_st_ino",
           context["receipt_namespace_st_ino"]))),
    )
    for constant, fields in groups:
        for field, derived in fields:
            if published[field] != derived:
                raise ReceiptIdentityError(
                    f"{constant}: published {field} != re-derived value")


def g11_independent_rederivation(verified_g7_context, grant_bytes,
                                 package_artifact, repo, ref) -> dict:
    """G11 independent re-derivation (design Section 14): trusts NO
    package-provided R, NO latest HEAD, NO cached G10 selector result,
    NO cached receipt digest and NO current-only receipt file.  It
    independently (1)-(3) re-parses the exact grant bytes, re-derives
    grant_identity and the package digest from the exact frozen
    artifact; (5) re-verifies the canonical receipt namespace by the
    R-NS-4 rule; (6)-(7) enumerates authoritative first-parent history
    and re-derives R by R1-R22; (8)-(9) re-reads the publication bytes
    from R and extracts the ORIGINAL receipt identity; (10)-(11)
    re-reads the CURRENT receipt per R-NS-4/R-NS-5 and recomputes its
    SHA-256/size; (12) requires CURRENT == ORIGINAL on bytes/SHA-256/
    size AND the full canonical re-derivation AND every Section 8
    cross-binding.  ANY mismatch: G11_REFUSED (fail closed, no partial
    acceptance)."""
    try:
        original = derive_original_receipt_identity(
            verified_g7_context, grant_bytes, package_artifact)
        expected = construct_g10_publication_record(original)
        selection = select_canonical_g10_publication(repo, ref,
                                                     expected)
        _require_published_matches_derived(selection["record"],
                                           original)
        current = _read_via_verified_namespace(original, G11_REFUSED)
        _require_current_equals_original(current, original, G11_REFUSED)
        bab.parse_package_binding_receipt(current)
    except bab.BindingError as exc:
        raise ReceiptIdentityError(f"{G11_REFUSED}: {exc}") from exc
    return {"selection": selection,
            "post_publication_identity":
                derive_post_publication_identity(selection),
            "current_receipt_sha256":
                hashlib.sha256(current).hexdigest(),
            "current_receipt_size": len(current)}


def stage_receipt_identity_publication(destination_root,
                                       canonical_bytes: bytes) -> str:
    """Callable NON-RUNTIME staging helper for the SEPARATELY
    AUTHORIZED future G10.6 publication workflow: write the canonical
    publication bytes at the RESERVED canonical record path under
    `destination_root`.  This function performs NO git operation, NO
    commit and NO push, and is exercised ONLY against disposable
    synthetic LOCAL repositories — it must NEVER be pointed at a live
    governance repository (that is the future operator-authorized G10
    execution, not this module)."""
    destination = os.path.join(
        os.fspath(destination_root),
        *RECEIPT_IDENTITY_PUBLICATION_RECORD_PATH.split("/"))
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as handle:
        handle.write(canonical_bytes)
    return destination
