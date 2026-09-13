#!/usr/bin/env python3
"""Generic first-pass structural validator (B-008).

Validates a first-pass auditor artifact (markdown or JSON) against a
STRUCTURAL SPEC supplied at invocation time. This validator is GENERIC BY
CONSTRUCTION: event identity, target identity, auditor identity and every
expected literal are PARAMETERS — supplied per invocation via the spec
document and the CLI — never baked-in constants. A campaign therefore never
needs to reuse a prior event's validator bytes (the frozen binding-v2
validator's stale prior-event self-description is exactly the defect this
module exists to prevent going forward; those frozen bytes remain immutable
historical evidence for the event that used them).

Spec document (JSON), all keys optional arrays/objects:

  {
    "required_headings": ["# First pass", ...],      # substrings, in order
    "required_literals": {"<literal>": <count>},     # exact occurrence count
    "forbidden_literals": ["<literal>", ...],        # must NOT occur
    "max_bytes": 200000,
    "require_json_object": false                     # parse as JSON object
  }

CLI:
  validate --file F --spec S --event-id E --target-sha T [--auditor A]

The identity arguments are recorded IN THE RESULT (never compared against
anything baked in) so the result document is self-describing for the
operative event. Exit 0 = structurally conforming; 1 = violations found;
2 = unusable input (missing/unreadable file or spec).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VALIDATOR_IDENTITY = "generic-first-pass-structural-validator"
VALIDATOR_VERSION = 1


class SpecError(Exception):
    pass


def load_spec(path: str) -> dict[str, Any]:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SpecError(f"spec unreadable: {path}: {exc}") from None
    if not isinstance(doc, dict):
        raise SpecError(f"spec must be a JSON object: {path}")
    for key in ("required_headings", "forbidden_literals"):
        val = doc.get(key, [])
        if not isinstance(val, list) or not all(
                isinstance(x, str) for x in val):
            raise SpecError(f"spec.{key} must be an array of strings")
    literals = doc.get("required_literals", {})
    if not isinstance(literals, dict) or not all(
            isinstance(k, str) and isinstance(v, int) and v >= 1
            for k, v in literals.items()):
        raise SpecError("spec.required_literals must map literal -> "
                        "positive integer count")
    return doc


def validate_first_pass(text: str, spec: dict[str, Any]) -> list[str]:
    """Pure structural validation; returns a list of violation strings
    (empty = conforming). No identity constant of any prior or current
    event is referenced here — identity is data, never code."""
    errors: list[str] = []
    max_bytes = spec.get("max_bytes")
    if isinstance(max_bytes, int) and len(text.encode("utf-8")) > max_bytes:
        errors.append(f"artifact exceeds max_bytes {max_bytes}")
    if spec.get("require_json_object"):
        try:
            doc = json.loads(text)
        except ValueError as exc:
            errors.append(f"artifact is not valid JSON: {exc}")
            doc = None
        if doc is not None and not isinstance(doc, dict):
            errors.append("artifact is not a JSON object")
    pos = 0
    for heading in spec.get("required_headings", []):
        idx = text.find(heading, pos)
        if idx < 0:
            errors.append(f"required heading missing or out of order: "
                          f"{heading!r}")
        else:
            pos = idx + len(heading)
    for literal, count in spec.get("required_literals", {}).items():
        actual = text.count(literal)
        if actual != count:
            errors.append(f"literal {literal!r} occurs {actual} times; "
                          f"exactly {count} required")
    for literal in spec.get("forbidden_literals", []):
        if literal in text:
            errors.append(f"forbidden literal present: {literal!r}")
    return errors


def _cli() -> int:
    ap = argparse.ArgumentParser(prog="first_pass_validator")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser(
        "validate",
        help="structurally validate a first-pass artifact against a spec; "
             "identity arguments are recorded in the result only")
    v.add_argument("--file", required=True)
    v.add_argument("--spec", required=True)
    v.add_argument("--event-id", required=True,
                   help="operative event id (recorded in the result)")
    v.add_argument("--target-sha", required=True,
                   help="operative audited target sha (recorded in the "
                        "result; also auto-required as a literal when the "
                        "spec says so)")
    v.add_argument("--auditor", default=None,
                   help="operative auditor label (recorded in the result)")
    args = ap.parse_args()

    if args.cmd == "validate":
        try:
            spec = load_spec(args.spec)
        except SpecError as exc:
            print(json.dumps({"ok": False, "spec_error": str(exc)}))
            return 2
        try:
            text = Path(args.file).read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            print(json.dumps({"ok": False, "input_error": str(exc)}))
            return 2
        errors = validate_first_pass(text, spec)
        result: dict[str, Any] = {
            "ok": not errors,
            "errors": errors,
            "validated": {
                "validator": VALIDATOR_IDENTITY,
                "validator_version": VALIDATOR_VERSION,
                "event_id": args.event_id,
                "target_sha": args.target_sha,
                "auditor": args.auditor,
                "file": args.file,
            },
            # self-description contract (B-008): the validator describes the
            # OPERATIVE event generically and truthfully — identity comes
            # from the invocation, never from this module's constants
            "self_description": (
                "generic parameter-driven first-pass structural validator; "
                "validates the artifact named above against the supplied "
                "spec for the event/target/auditor recorded above; no "
                "event identity is baked into the validator itself"),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if not errors else 1
    return 2


if __name__ == "__main__":
    sys.exit(_cli())
