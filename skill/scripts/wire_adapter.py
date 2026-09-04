#!/usr/bin/env python3
"""Deterministic adapter between Codex strict wire schemas/instances and
Audit Council canonical schemas/instances (v1.0.3 Defect 1).

Two directions, one boundary:

  canonical_to_wire(schema)   canonical schema -> OpenAI/Codex strict schema
  wire_to_canonical(doc, s)   wire instance + canonical schema -> canonical
                              candidate (schema-aware; NEVER a blind
                              strip-nulls pass)

Semantics:
- A canonically OPTIONAL property is represented on the wire as a nullable
  property (still listed in wire `required`, as strict outputs demand); the
  model emits null when the property legitimately does not apply.
- wire_to_canonical omits an optional property whose wire value is null.
- A REQUIRED non-nullable canonical property receiving null is an ERROR
  (fail-closed; never silently omitted or repaired).
- A canonical property that genuinely permits null keeps null.
- No defaults are invented; null never becomes "", [], {}, 0, or false.
- Canonical validation (performed by the caller, against the ORIGINAL
  canonical schema) remains the final authority: unsupported canonical
  constraints (e.g. pattern) are dropped on the wire only because the
  canonical validator re-imposes them after normalization.

Supported canonical subset: type, enum, const, required, properties,
additionalProperties, items, minItems, maxItems, minLength, pattern, $ref
(local sibling files), plus anyOf-free unions expressed as type arrays or
enums containing null.
"""
from __future__ import annotations

import copy
import json
import os

_STRICT_KEEP = {
    "type", "properties", "required", "items", "additionalProperties",
    "enum", "anyOf", "description", "title",
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _is_nullable(schema: dict) -> bool:
    """Does this (canonical) subschema explicitly permit null?"""
    t = schema.get("type")
    if isinstance(t, list) and "null" in t:
        return True
    if isinstance(schema.get("enum"), list) and None in schema["enum"]:
        return True
    return False


def _nullable_wire(sub: dict) -> dict:
    """Wrap a strict subschema so it also accepts null."""
    if _is_nullable_strict(sub):
        return sub
    return {"anyOf": [sub, {"type": "null"}]}


def _is_nullable_strict(sub: dict) -> bool:
    if "anyOf" in sub:
        return any(b == {"type": "null"} or b.get("type") == "null"
                   for b in sub["anyOf"] if isinstance(b, dict))
    return False


def _load_ref(base_dir: str, ref: str) -> dict:
    with open(os.path.join(base_dir, ref), "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# canonical -> wire
# ---------------------------------------------------------------------------

def canonical_to_wire(canon: dict, canon_dir: str) -> dict:
    """Canonical schema document -> self-contained strict wire schema.

    Steps: inline local $refs; drop unsupported keywords; make every object
    additionalProperties:false with all properties required; convert type
    arrays and null-bearing enums to anyOf; make canonically OPTIONAL
    properties nullable (null is the wire representation of 'absent');
    drop the finding.cluster_id property (clustering is Opus Phase-3 work
    and the strict wire subset cannot express its pattern)."""
    def inline(node, seen):
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str):
                target = _load_ref(canon_dir, ref)
                marker = (ref, id(target))
                if marker in seen:
                    return {}
                merged = inline(target, seen | {marker})
                merged.update({k: v for k, v in node.items() if k != "$ref"})
                return merged
            return {k: inline(v, seen) for k, v in node.items() if k != "$id"}
        if isinstance(node, list):
            return [inline(x, seen) for x in node]
        return node

    schema = inline(copy.deepcopy(canon), frozenset())
    return _strictify(schema, canonical_root=canon)


def _strictify(node, canonical_root=None):
    if isinstance(node, list):
        return [_strictify(x, canonical_root) for x in node]
    if not isinstance(node, dict):
        return node
    if "$ref" in node:
        return _strictify({k: v for k, v in node.items() if k != "$ref"},
                          canonical_root)
    out = {}
    for k, v in node.items():
        if k == "properties" and isinstance(v, dict):
            req = set(node.get("required") or [])
            props = {}
            for pk, pv in v.items():
                pv = _strictify(pv, canonical_root)
                if pk not in req:
                    # canonically optional -> nullable on the wire
                    pv = _nullable_wire(pv)
                props[pk] = pv
            out[k] = props
            continue
        if k not in _STRICT_KEEP:
            continue  # pattern, minLength, minItems, maximum, const, ...
        if k == "type" and isinstance(v, list):
            out["anyOf"] = [{"type": t} for t in v]
            continue
        if k == "enum" and any(x is None for x in v):
            vals = [x for x in v if x is not None]
            out["anyOf"] = ([{"enum": vals}] if vals else []) + \
                [{"type": "null"}]
            continue
        out[k] = _strictify(v, canonical_root)
    if out.get("type") == "object" and "properties" in out:
        out["additionalProperties"] = False
        out["required"] = sorted(out["properties"].keys())
    return out


def drop_wire_property(wire: dict, name: str) -> None:
    """Recursively remove a property from every object schema."""
    if isinstance(wire, list):
        for x in wire:
            drop_wire_property(x, name)
        return
    if not isinstance(wire, dict):
        return
    props = wire.get("properties")
    if isinstance(props, dict) and name in props:
        del props[name]
        req = wire.get("required")
        if isinstance(req, list) and name in req:
            req.remove(name)
    for v in wire.values():
        drop_wire_property(v, name)


def drop_wire_property_under(wire, name: str, under: tuple) -> None:
    """Remove `name` ONLY from object schemas reached beneath a property
    named in `under` (e.g. findings/late_findings). v1.0.3 review F1: a
    global drop deleted the canonically REQUIRED rounds[].cluster_id from
    the adjudication wire schema; the drop is needed only where the
    property is optional-but-unrepresentable (finding.cluster_id, whose
    CLUSTER-nnn pattern the strict wire subset cannot express)."""
    if isinstance(wire, list):
        for x in wire:
            drop_wire_property_under(x, name, under)
        return
    if not isinstance(wire, dict):
        return
    props = wire.get("properties")
    if isinstance(props, dict):
        for key in under:
            if key in props:
                drop_wire_property(props[key], name)
    for k, v in wire.items():
        if isinstance(props, dict) and k in under:
            continue  # already handled above with the scoped drop
        drop_wire_property_under(v, name, under)


# ---------------------------------------------------------------------------
# wire -> canonical
# ---------------------------------------------------------------------------

def wire_to_canonical(doc, canon_schema: dict, canon_dir: str):
    """Wire instance + canonical schema -> (canonical_candidate, errors).

    Schema-aware null handling ONLY:
    - optional property with wire null  -> omitted
    - required nullable property null   -> preserved
    - required non-nullable null        -> error (fail-closed, kept as-is
                                           so canonical validation also sees
                                           and rejects it)
    Everything else passes through untouched — the ORIGINAL canonical
    schema (validated by the caller) stays the final authority."""
    resolved = _resolve(canon_schema, canon_dir)

    def walk(node, schema, path):
        if isinstance(schema, dict) and "$ref" in schema:
            schema = _resolve(schema, canon_dir)
        if isinstance(node, dict) and isinstance(schema, dict):
            props = schema.get("properties") or {}
            req = set(schema.get("required") or [])
            errors = []
            out = {}
            for key, value in node.items():
                sub = props.get(key)
                if value is None and key in props:
                    if key not in req:
                        continue  # optional + null -> omitted
                    if not _is_nullable(sub):
                        errors.append(
                            "%s%s: required non-nullable property %r "
                            "received null" % (path, key, key))
                        out[key] = value  # keep for canonical rejection
                        continue
                    out[key] = value  # genuinely nullable
                    continue
                if sub is not None:
                    sub_errors, sub_value = walk(
                        value, sub, "%s%s." % (path, key))
                    errors.extend(sub_errors)
                    out[key] = sub_value
                else:
                    out[key] = value  # unknown key: canonical validator's job
            return errors, out
        if isinstance(node, list) and isinstance(schema, dict) and \
                "items" in schema:
            errors = []
            out = []
            for i, item in enumerate(node):
                e, v = walk(item, schema["items"], "%s[%d]." % (path, i))
                errors.extend(e)
                out.append(v)
            return errors, out
        return [], node

    errors, candidate = walk(doc, resolved, "<root>.")
    return candidate, errors


def _resolve(schema: dict, canon_dir: str) -> dict:
    while isinstance(schema, dict) and "$ref" in schema:
        schema = _load_ref(canon_dir, schema["$ref"])
    return schema
