"""Append-only OBSERVABILITY ledger.

IMPORTANT (G-1 accepted design): an ordinary same-UID file is
observability ONLY — it is NOT the launch-authority boundary.  Attempt
authority is process-bound (see qh/authority.py).  Deleting, forging or
recreating ledger rows can never mint, restore or reset authority; the
ledger exists so operators and auditors can observe grant lifecycle
events.  No secret or credential-derived value is ever written here.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .util import utc_now_iso


class ObservabilityLedger:
    """JSONL append log.  Failures to append are reported, never fatal to
    the authority state (the authoritative state is process memory)."""

    def __init__(self, operator_state_dir: str) -> None:
        self.path = os.path.join(operator_state_dir, "ledger.jsonl")
        Path(operator_state_dir).mkdir(parents=True, exist_ok=True)

    def append(self, event: str, **facts) -> dict:
        record = {"event": event, "at": utc_now_iso(), **facts}
        line = json.dumps(record, sort_keys=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        return record

    def read_all(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        out: list[dict] = []
        with open(self.path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

    def attempt_ids_minted(self) -> set[str]:
        return {r["attempt_id"] for r in self.read_all()
                if r.get("event") == "MINTED"}
