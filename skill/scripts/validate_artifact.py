#!/usr/bin/env python3
"""Minimal JSON Schema validator + artifact invariant checks.

Library + CLI (`validate --file F --schema S`). Stdlib only.

Supported keywords: type, enum, const, required, properties,
additionalProperties (bool or schema), items, minItems, maxItems, minLength,
maxLength, minimum, maximum, pattern, $ref (LOCAL ONLY: sibling schema files
or `#/$defs/...` within the same document), $defs. Meta keywords ($id,
$schema, title, format) are recognized and ignored. Any other keyword raises
UnsupportedKeywordError — we control all schemas, so fail loudly in dev.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"

META_KEYWORDS = {"$id", "$schema", "title", "description", "format",
                 "$comment"}
SUPPORTED_KEYWORDS = {
    "type", "enum", "const", "required", "properties",
    "additionalProperties", "items", "minItems", "maxItems",
    "minLength", "maxLength", "minimum", "maximum", "pattern",
    "$ref", "$defs",
} | META_KEYWORDS

_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


class UnsupportedKeywordError(Exception):
    pass


class SchemaError(Exception):
    pass


def _check_type(value: Any, t: str, path: str, errors: list[str]) -> None:
    if t == "integer":
        ok = isinstance(value, int) and not isinstance(value, bool)
    elif t == "number":
        ok = isinstance(value, (int, float)) and not isinstance(value, bool)
    elif t == "boolean":
        ok = isinstance(value, bool)
    elif t in _TYPES:
        py = _TYPES[t]
        # bool is not a valid "string"/"array"/"object"/"null"
        ok = isinstance(value, py) and not (
            t != "boolean" and isinstance(value, bool))
    else:
        raise SchemaError(f"unknown type {t!r} at {path}")
    if not ok:
        errors.append(f"{path}: expected type {t}, got "
                      f"{type(value).__name__}")


def _resolve_ref(ref: str, schema: dict[str, Any],
                 base_dir: Path) -> tuple[Any, Path]:
    """Resolve LOCAL refs only: `#/$defs/...` or a sibling schema filename."""
    if ref.startswith("#/"):
        node: Any = schema
        for part in ref[2:].split("/"):
            if not isinstance(node, dict) or part not in node:
                raise SchemaError(f"unresolvable local ref {ref!r}")
            node = node[part]
        return node, base_dir
    if "://" in ref or ref.startswith("#"):
        raise SchemaError(f"only local refs are supported, got {ref!r}")
    fname = ref.split("#", 1)[0]
    path = (base_dir / fname).resolve()
    if not path.is_file():
        raise SchemaError(f"ref target not found: {path}")
    doc = json.loads(path.read_text(encoding="utf-8"))
    frag = ref.split("#", 1)[1] if "#" in ref else ""
    if frag.startswith("/"):
        for part in frag[1:].split("/"):
            doc = doc[part]
    return doc, path.parent


def validate(instance: Any, schema: Any, *, base_dir: Path | None = None,
             _depth: int = 0) -> list[str]:
    """Validate instance against schema; return list of error strings."""
    if _depth > 64:
        return ["<maximum $ref nesting exceeded>"]
    base_dir = base_dir or SCHEMAS_DIR
    errors: list[str] = []

    if isinstance(schema, bool):
        if schema is False:
            errors.append("<schema is false: nothing is valid>")
        return errors
    if not isinstance(schema, dict):
        raise SchemaError(f"schema must be object or bool, got {type(schema)!r}")

    unknown = set(schema) - SUPPORTED_KEYWORDS
    if unknown:
        raise UnsupportedKeywordError(
            f"unsupported schema keywords {sorted(unknown)}; we control all "
            f"schemas — extend the validator deliberately, not silently")

    if "$ref" in schema:
        target, new_base = _resolve_ref(schema["$ref"], schema, base_dir)
        merged = {k: v for k, v in target.items() if k != "$id"}
        return validate(instance, merged, base_dir=new_base,
                        _depth=_depth + 1)

    if "type" in schema:
        types = schema["type"]
        types = types if isinstance(types, list) else [types]
        probes: list[list[str]] = []
        for t in types:
            probe: list[str] = []
            _check_type(instance, t, "<root>", probe)
            if not probe:
                probes = []
                break
            probes.append(probe)
        if probes:  # no type matched
            errors.append(f"<root>: expected type "
                          f"{'|'.join(types)}, got {type(instance).__name__}")

    if "const" in schema and instance != schema["const"]:
        errors.append(f"<root>: expected const {schema['const']!r}, "
                      f"got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"<root>: {instance!r} not in enum {schema['enum']!r}")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"<root>: missing required property {key!r}")
        props = schema.get("properties", {})
        ap = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in props:
                errors.extend(
                    _prefix(validate(value, props[key], base_dir=base_dir,
                                     _depth=_depth + 1), f".{key}"))
            elif ap is False:
                errors.append(f"<root>: additional property {key!r} not allowed")
            elif isinstance(ap, dict):
                errors.extend(
                    _prefix(validate(value, ap, base_dir=base_dir,
                                     _depth=_depth + 1), f".{key}"))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"<root>: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"<root>: more than {schema['maxItems']} items")
        items = schema.get("items")
        if items is not None:
            for i, item in enumerate(instance):
                errors.extend(
                    _prefix(validate(item, items, base_dir=base_dir,
                                     _depth=_depth + 1), f"[{i}]"))

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"<root>: string shorter than {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"<root>: string longer than {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"<root>: {instance!r} does not match "
                          f"pattern {schema['pattern']!r}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"<root>: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"<root>: {instance} > maximum {schema['maximum']}")

    return errors


def _prefix(errors: list[str], prefix: str) -> list[str]:
    return [e.replace("<root>", f"<root>{prefix}", 1) for e in errors]


def validate_file(file_path: str, schema_path: str) -> list[str]:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    instance = json.loads(Path(file_path).read_text(encoding="utf-8"))
    return validate(instance, schema, base_dir=Path(schema_path).resolve().parent)


# ---------------------------------------------------------------------------
# Ledger / final artifact invariants
# ---------------------------------------------------------------------------
def check_ledger_invariants(ledger: dict[str, Any]) -> list[str]:
    """(i) cluster ids unique; member finding ids unique across clusters."""
    errors: list[str] = []
    clusters = ledger.get("clusters", []) if isinstance(ledger, dict) else []
    seen_clusters: set[str] = set()
    seen_members: dict[str, str] = {}
    for c in clusters:
        cid = c.get("cluster_id")
        if cid in seen_clusters:
            errors.append(f"duplicate cluster id {cid}")
        seen_clusters.add(cid)
        for fid in c.get("member_finding_ids", []):
            if fid in seen_members:
                errors.append(
                    f"finding {fid} appears in both {seen_members[fid]} "
                    f"and {cid}")
            seen_members[fid] = cid
    return errors


def _iter_final_findings(final: dict[str, Any]):
    for f in final.get("findings", []) or []:
        if isinstance(f, dict):
            yield f


def check_final_invariants(final: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rejected_clusters = {
        r.get("cluster_id") for r in final.get("rejected_appendix", []) or []
        if isinstance(r, dict)
    }

    for f in _iter_final_findings(final):
        cid = f.get("cluster_id")
        prov = f.get("provenance") or {}

        # (i) REJECTED may appear only in the rejected appendix.
        if prov.get("final_status") == "REJECTED":
            errors.append(
                f"{cid}: provenance.final_status REJECTED in primary findings; "
                f"rejected findings belong only in rejected_appendix")
        if prov.get("adjudication") == "REJECTED" and cid not in rejected_clusters:
            errors.append(
                f"{cid}: adjudication REJECTED but cluster is not in "
                f"rejected_appendix")
        if cid in rejected_clusters:
            errors.append(
                f"{cid}: appears in both primary findings and "
                f"rejected_appendix")

        # (iv) every primary finding has non-empty provenance.origin.
        origin = prov.get("origin")
        if not isinstance(origin, list) or not origin:
            errors.append(f"{cid}: provenance.origin missing or empty")

    # (ii) unresolved CRITICAL/HIGH findings and risks must stay in sync:
    # every risk entry maps to an UNRESOLVED finding, and every UNRESOLVED
    # CRITICAL/HIGH finding is explicitly listed as an unresolved risk.
    unresolved_clusters = {
        f.get("cluster_id") for f in _iter_final_findings(final)
        if f.get("final_status") == "UNRESOLVED"
    }
    risk_clusters = {
        r.get("cluster_id") for r in final.get("unresolved_risks", []) or []
        if isinstance(r, dict)
    }
    for r in final.get("unresolved_risks", []) or []:
        if not isinstance(r, dict):
            continue
        if r.get("severity") in ("CRITICAL", "HIGH"):
            cid = r.get("cluster_id")
            if cid not in unresolved_clusters:
                errors.append(
                    f"{cid}: unresolved risk with severity "
                    f"{r.get('severity')} has no UNRESOLVED finding "
                    f"(not explicitly listed as unresolved)")
    for f in _iter_final_findings(final):
        if (f.get("final_status") == "UNRESOLVED"
                and f.get("severity") in ("CRITICAL", "HIGH")
                and f.get("cluster_id") not in risk_clusters):
            errors.append(
                f"{f.get('cluster_id')}: UNRESOLVED finding with severity "
                f"{f.get('severity')} is not listed in unresolved_risks "
                f"(unresolved high-risk issues must stay explicitly visible)")
    return errors


def _collect_late_findings(ledger_or_crossex: Any) -> dict[str, dict[str, Any]]:
    """Best-effort gathering of late/PROVISIONAL findings keyed by id."""
    docs = ledger_or_crossex if isinstance(ledger_or_crossex, list) \
        else [ledger_or_crossex]
    late: dict[str, dict[str, Any]] = {}
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        for f in doc.get("late_findings", []) or []:
            if isinstance(f, dict) and f.get("id"):
                late[f["id"]] = f
        # normalized-findings style: any finding flagged late
        for f in doc.get("findings", []) or []:
            if isinstance(f, dict) and f.get("late_finding") and f.get("id"):
                late[f["id"]] = f
    return late


def check_late_findings(ledger_or_crossex: Any,
                        final: dict[str, Any]) -> list[str]:
    """(iii) late/PROVISIONAL findings promoted to the final report must be
    validated by the other model or remain UNRESOLVED. Best-effort: operates
    on the (ledger|cross-examination, final) pair."""
    errors: list[str] = []
    late = _collect_late_findings(ledger_or_crossex)
    for f in _iter_final_findings(final):
        if f.get("final_status") == "UNRESOLVED":
            continue
        origin_ids = (f.get("provenance") or {}).get("origin") or []
        hit = [oid for oid in origin_ids if oid in late]
        if not hit:
            continue
        src = late[hit[0]]
        prov = src.get("provenance") or {}
        validated_by = prov.get("validated_by")
        discovered_by = prov.get("discovered_by")
        if validated_by not in ("OPUS", "CODEX"):
            errors.append(
                f"{hit[0]}: late finding promoted into final findings without "
                f"provenance.validated_by set to the other model")
        elif discovered_by is not None and validated_by == discovered_by:
            errors.append(
                f"{hit[0]}: late finding validated_by {validated_by} equals "
                f"discovered_by; independent validation by the other model "
                f"is required")
    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _cli() -> int:
    ap = argparse.ArgumentParser(prog="validate_artifact")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("--file", required=True)
    v.add_argument("--schema", required=True)
    lf = sub.add_parser("check-late-findings")
    lf.add_argument("--source", required=True,
                    help="ledger or cross-examination JSON file")
    lf.add_argument("--final", required=True)

    args = ap.parse_args()
    if args.cmd == "validate":
        try:
            errors = validate_file(args.file, args.schema)
        except (UnsupportedKeywordError, SchemaError,
                json.JSONDecodeError, OSError) as exc:
            print(json.dumps({"ok": False, "errors": [str(exc)]}))
            return 1
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
        return 0 if not errors else 1
    if args.cmd == "check-late-findings":
        src = json.loads(Path(args.source).read_text(encoding="utf-8"))
        fin = json.loads(Path(args.final).read_text(encoding="utf-8"))
        errors = check_late_findings(src, fin)
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
        return 0 if not errors else 1
    return 2


if __name__ == "__main__":
    sys.exit(_cli())
