#!/usr/bin/env python3
"""Audit Council v2.0 eval suite (pillar D).

Four tiers (ARCHITECTURE §3.4.8):
  1. harness-deterministic   -> tier1_harness  (this program phase)
  2. seeded fixture corpus   -> tier2_fixtures (deterministic builds; the
                                 real-model scoring runs are budgeted
                                 separately and are NOT part of this module)
  3. historical replay       -> tier3_replay   (approval-gated, READ-ONLY)
  4. real release-audit observations          (out of scope here)

Shared scoring semantics live in `scoring`. The CLI entry point is
`eval_cli.py`. No module in this package may make a real model call.
"""
from __future__ import annotations

__all__ = ["scoring", "tier1_harness", "tier2_fixtures", "tier3_replay"]
