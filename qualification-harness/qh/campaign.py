"""Campaign-level auditor/model engagement accounting — SEPARATE from the
C-2 attempt lifecycle.

Mandatory separation (accepted C-2 property): a pre-inference PREEXEC stop
must NOT consume campaign auditor/model authority, and attempt-grant
consumption must NOT be equated with campaign model-engagement consumption.
The supervisor/preexec state machine NEVER calls into this module; the
separation is mechanically asserted by tests.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .util import utc_now_iso


class EngagementLedger:
    """Operator-side accounting of campaign model engagements.  Written
    ONLY by explicit operator/Control-Room action, never by the launch
    authority lifecycle."""

    def __init__(self, operator_state_dir: str) -> None:
        self.path = os.path.join(operator_state_dir, "engagements.json")
        Path(operator_state_dir).mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict:
        if not os.path.exists(self.path):
            return {"authorized": 0, "used": 0, "events": []}
        with open(self.path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def snapshot(self) -> dict:
        data = self._load()
        return {"authorized": data["authorized"], "used": data["used"]}

    def authorize(self, n: int, note: str = "") -> None:
        data = self._load()
        data["authorized"] += n
        data["events"].append({"event": "AUTHORIZED", "n": n,
                               "note": note, "at": utc_now_iso()})
        self._save(data)

    def record_engagement(self, note: str) -> None:
        data = self._load()
        data["used"] += 1
        data["events"].append({"event": "ENGAGED", "note": note,
                               "at": utc_now_iso()})
        self._save(data)

    def _save(self, data: dict) -> None:
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, sort_keys=True, indent=1)
        os.replace(tmp, self.path)
