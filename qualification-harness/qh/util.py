"""Shared mechanical helpers: hashing, canonical JSON, /proc access, redaction."""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj) -> bytes:
    """Deterministic serialization used for every content address in the
    harness (sorted keys, compact separators, UTF-8)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def content_id(obj) -> str:
    return sha256_bytes(canonical_json(obj))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


# ---------------------------------------------------------------- /proc ----

def proc_starttime(pid: int) -> str | None:
    """Field 22 of /proc/<pid>/stat (process start time) — pid-reuse defense.

    Comm may contain spaces/parens; parse after the LAST ')'.
    """
    try:
        with open(f"/proc/{pid}/stat", "rb") as fh:
            data = fh.read().decode("utf-8", "replace")
    except OSError:
        return None
    idx = data.rfind(")")
    if idx < 0:
        return None
    fields = data[idx + 1:].split()
    # fields[0] is state (field 3); starttime is field 22 -> index 19
    if len(fields) < 20:
        return None
    return fields[19]


def proc_environ(pid: int) -> dict[str, str] | None:
    """Initial environment of a live process (immutable after exec)."""
    try:
        with open(f"/proc/{pid}/environ", "rb") as fh:
            raw = fh.read()
    except OSError:
        return None
    env: dict[str, str] = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        k, _, v = item.partition(b"=")
        env[k.decode("utf-8", "replace")] = v.decode("utf-8", "replace")
    return env


def proc_exe(pid: int) -> str | None:
    try:
        return os.path.realpath(f"/proc/{pid}/exe")
    except OSError:
        return None


def read_yama_ptrace_scope() -> int | None:
    """Yama ptrace_scope value, None when the knob is absent."""
    try:
        with open("/proc/sys/kernel/yama/ptrace_scope") as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return None


# -------------------------------------------------------------- redaction --

class Redactor:
    """Registry of secret VALUES that must never appear in any harness log,
    report, ledger or artifact.  Every synthetic credential registers here;
    ``scrub`` replaces occurrences with a label.  Only the label/length ever
    reach output — never the value and never a hash of it."""

    def __init__(self) -> None:
        self._secrets: dict[str, str] = {}

    def register(self, value: str, label: str) -> None:
        if value:
            self._secrets[value] = label

    def scrub(self, text: str) -> str:
        for value, label in self._secrets.items():
            text = text.replace(value, f"<REDACTED:{label}>")
        return text

    def contains_any(self, text: str) -> str | None:
        for value in self._secrets:
            if value in text:
                return value
        return None

    def known_labels(self) -> list[str]:
        return sorted(self._secrets.values())


def assert_no_secrets(text: str, redactor: Redactor, what: str) -> None:
    hit = redactor.contains_any(text)
    if hit is not None:
        raise AssertionError(
            f"secret material present in {what} (registered value matched); "
            "harness contract forbids credential values in any output")


_SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def safe_token(name: str) -> bool:
    return bool(_SAFE_NAME.match(name))
