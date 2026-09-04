#!/usr/bin/env python3
"""evidence_migration.py — deterministic v1 -> v2 evidence model reader.

schema_version 2 replaces the single-range string evidence field `lines`
with typed multi-range `line_ranges` (ARCHITECTURE §3.4.3). v1 artifacts
are read through this module; they are NEVER rewritten on disk — the
migration runs in memory and returns a new document.

Authority split: canonical validation (validate_artifact) enforces
integer type, minimum 1, maxItems 32, and strict range objects
(additionalProperties: false), but the validator's keyword subset cannot
express `end >= start`. `normalize_ranges` is the second half of the
authority: canonical validation + normalization together define a valid
canonical line_ranges value. Callers that accept external input should
normalize (or validate a normalized document), not trust the schema
alone.

No comma-separated parsing, ever (ARCHITECTURE §3.4.3): a v1-style
multi-range string such as "184-185, 240-273" raises MigrationError; it
exists only inside raw logs of failed attempts, which are preserved
untouched. Callers decide policy on MigrationError.
"""
from __future__ import annotations

import re
from typing import Any

__all__ = [
    "MigrationError",
    "lines_to_ranges",
    "normalize_ranges",
    "migrate_artifact",
    "is_v1_artifact",
]

_SINGLE = re.compile(r"^([0-9]+)$")
_RANGE = re.compile(r"^([0-9]+)-([0-9]+)$")

MAX_RANGES = 32  # mirrors line_ranges maxItems in the five schemas


class MigrationError(ValueError):
    """A legacy `lines` value or `line_ranges` list is not migratable."""


def lines_to_ranges(lines: str) -> list[dict]:
    """'^\\d+$' -> [{"start": N, "end": N}]; '^\\d+-\\d+$' ->
    [{"start": N, "end": M}]. ANY other shape — comma lists, empty string,
    reversed "5-3", zero "0-3", whitespace, garbage, non-strings — raises
    MigrationError. NEVER splits on commas."""
    if not isinstance(lines, str):
        raise MigrationError(
            "legacy lines value must be a string, got "
            f"{type(lines).__name__}: {lines!r}")
    m = _SINGLE.match(lines)
    if m:
        n = int(m.group(1))
        if n < 1:
            raise MigrationError(f"legacy lines value {lines!r}: zero line")
        return [{"start": n, "end": n}]
    m = _RANGE.match(lines)
    if m:
        start, end = int(m.group(1)), int(m.group(2))
        if start < 1 or end < 1:
            raise MigrationError(
                f"legacy lines value {lines!r}: zero line number")
        if end < start:
            raise MigrationError(
                f"legacy lines value {lines!r}: reversed range")
        return [{"start": start, "end": end}]
    raise MigrationError(f"legacy lines value {lines!r}: unsupported shape "
                         "(single 'N' or range 'N-M' only; no comma lists)")


def normalize_ranges(ranges: list[dict]) -> list[dict]:
    """Validate range members (int, start >= 1, end >= start, exactly the
    keys start/end), sort by (start, end), return a NEW list of new dicts.
    Raises MigrationError on any invalid member or non-list input."""
    if not isinstance(ranges, list):
        raise MigrationError(
            f"line_ranges must be a list, got {type(ranges).__name__}")
    if len(ranges) > MAX_RANGES:
        raise MigrationError(
            f"line_ranges has {len(ranges)} items, max is {MAX_RANGES}")
    out: list[dict] = []
    for r in ranges:
        if not isinstance(r, dict):
            raise MigrationError(
                f"line_ranges member must be an object, got "
                f"{type(r).__name__}: {r!r}")
        if set(r.keys()) != {"start", "end"}:
            raise MigrationError(
                f"line_ranges member must have exactly keys start/end, "
                f"got {sorted(r.keys())}")
        start, end = r["start"], r["end"]
        for name, value in (("start", start), ("end", end)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise MigrationError(
                    f"line_ranges.{name} must be an integer, got "
                    f"{type(value).__name__}: {value!r}")
        if start < 1:
            raise MigrationError(f"line_ranges.start {start} < 1")
        if end < start:
            raise MigrationError(
                f"line_ranges end {end} < start {start}")
        out.append({"start": start, "end": end})
    out.sort(key=lambda r: (r["start"], r["end"]))
    return out


def migrate_artifact(doc: dict) -> dict:
    """Walk any artifact tree; for every dict carrying a legacy string
    `lines` key, replace it with typed `line_ranges` via lines_to_ranges +
    normalize_ranges. Recursive into dicts and lists. Returns a NEW dict
    (the input is never mutated, and no on-disk file is rewritten by this
    API). Idempotent: a v2 document passes through unchanged (as a new
    equal dict). Raises MigrationError on multi-range/invalid strings —
    callers decide policy. A `lines` key with a non-string value also
    raises (fail-closed; canonical v1 artifacts only ever carry strings)."""
    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            out: dict = {}
            for key, value in node.items():
                if key == "lines":
                    if not isinstance(value, str):
                        raise MigrationError(
                            "legacy lines value must be a string, got "
                            f"{type(value).__name__}: {value!r}")
                    out["line_ranges"] = normalize_ranges(
                        lines_to_ranges(value))
                else:
                    out[key] = walk(value)
            return out
        if isinstance(node, list):
            return [walk(item) for item in node]
        return node

    return walk(doc)


def is_v1_artifact(doc: Any) -> bool:
    """True iff any dict in the tree carries a legacy `lines` key."""
    def walk(node: Any) -> bool:
        if isinstance(node, dict):
            if "lines" in node:
                return True
            return any(walk(v) for v in node.values())
        if isinstance(node, list):
            return any(walk(x) for x in node)
        return False

    return walk(doc)
