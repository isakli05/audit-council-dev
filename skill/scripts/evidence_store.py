#!/usr/bin/env python3
"""Provenance-bound Evidence Store & Cache (audit-council v2, pillar B).

Implements EvidenceRecord (AUDIT-COUNCIL-V2-ARCHITECTURE §3.4.4): a
per-run cache that stores EVIDENCE ONLY — never findings, verdicts or
conclusions — bound to repository fingerprint + environment binding digest
+ tool identity + input digest, with visibility classes enforced across the
first-pass independence barrier and freshness policies under which
FRESH_REQUIRED records can NEVER be satisfied from cache (retention for
audit history is not reuse).

Layout (everything lives under <run_dir>/evidence/):
  index.jsonl          one canonical record per line (the records index)
  objects/<digest>.json  content-addressed result payloads
  access-log.jsonl     append-only record of exactly which evidence each
                       consumer saw (and every denial, with a reason)

Determinism: the clock is injectable (`now=`), the barrier state is a
zero-arg callable supplied by the caller, and `produced_at` is part of the
record itself — this module never sleeps and never consults wall-clock time
outside the injected clock.
"""
from __future__ import annotations

import calendar
import json
import os
import time
from pathlib import Path
from typing import Any, Callable

from state_store import atomic_write_json, sha256_bytes, utc_now_iso
from validate_artifact import validate

SCHEMA_VERSION = 2
SCHEMA_PATH = (Path(__file__).resolve().parent.parent / "schemas"
               / "evidence-record.schema.json")

INDEX_NAME = os.path.join("evidence", "index.jsonl")
OBJECTS_DIR = os.path.join("evidence", "objects")
ACCESS_LOG_NAME = os.path.join("evidence", "access-log.jsonl")

KIND_ENUM = (
    "REPO_FACT", "FILE_EXCERPT", "SEARCH_RESULT", "DEPENDENCY_QUERY",
    "GRAPH_RESULT", "BUILD_RESULT", "LINT_RESULT", "TEST_RESULT",
    "COVERAGE_RESULT", "GIT_DIFF", "DETERMINISTIC_PROBE", "PACKAGE_SMOKE",
    "TOOL_VERSION",
)
VISIBILITY_CLASSES = ("SHARED_MECHANICAL", "AUDITOR_PRIVATE",
                      "POST_BARRIER_SHARED")
FRESHNESS_CLASSES = ("FRESH_REQUIRED", "CACHEABLE")
INVALIDATION_TRIGGERS = ("tracked_change", "head_change", "binding_change")

# Enough finding markers to catch finding-shaped payloads (a real v2
# finding carries id + severity + claim; cross-exam adds verdict; final
# findings add final_status). Two or more of these in ONE object, anywhere
# in a payload, is conclusion-shaped and rejected fail-closed.
FINDING_SHAPE_KEYS = {"id", "severity", "claim", "verdict", "final_status"}
FINDING_MARKER_THRESHOLD = 2

_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class EvidenceStoreError(Exception):
    """Raised on invalid records, conclusion-shaped payloads, provenance
    digest mismatches, and store corruption. Always fail-closed: when this
    is raised, nothing was stored."""


# ---------------------------------------------------------------------------
# Canonicalization / digests
# ---------------------------------------------------------------------------
def _canonical_json(doc: Any) -> str:
    """Same canonical form as repo_fingerprint/env_binding (sorted keys,
    compact separators). The basis of every content digest in this module."""
    return json.dumps(doc, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def compute_input_digest(command_or_query: str, tool: dict[str, Any]) -> str:
    """sha256 over the canonicalized command/query bound to the exact tool
    identity (name + version). This is the digest put() records and
    revalidate() recomputes — same inputs, same algorithm, always."""
    if not isinstance(command_or_query, str):
        raise EvidenceStoreError(
            "command_or_query must be a string, got %r"
            % type(command_or_query).__name__)
    if not isinstance(tool, dict):
        raise EvidenceStoreError(
            "tool must be an object with name+version, got %r"
            % type(tool).__name__)
    doc = {"command_or_query": command_or_query,
           "tool": {"name": tool.get("name"),
                    "version": tool.get("version")}}
    return sha256_bytes(_canonical_json(doc).encode("utf-8"))


def compute_result_digest(result: Any) -> str:
    """sha256 over the canonical result payload; content-addresses the
    object stored at evidence/objects/<digest>.json."""
    return sha256_bytes(_canonical_json(result).encode("utf-8"))


def evidence_id_for(record: dict[str, Any]) -> str:
    """"ev-" + first 16 hex of the sha256 over the canonical record.
    `evidence_id` itself never participates in its own digest."""
    body = {k: v for k, v in record.items() if k != "evidence_id"}
    return "ev-" + sha256_bytes(_canonical_json(body).encode("utf-8"))[:16]


def _marker_count(obj: dict[str, Any]) -> int:
    return sum(1 for key in FINDING_SHAPE_KEYS if key in obj)


def _is_conclusion_shaped(node: Any) -> bool:
    """Anti-conclusion guard: True when the payload carries finding-shaped
    content — any object (at any depth) with >= FINDING_MARKER_THRESHOLD
    finding-marker keys, or a "findings" array of such objects. Tuned to be
    a real finding detector, not a keyword panic: a bare "id" (one marker)
    is routine in evidence payloads and stays acceptable."""
    if isinstance(node, dict):
        if _marker_count(node) >= FINDING_MARKER_THRESHOLD:
            return True
        for key, value in node.items():
            if key == "findings" and isinstance(value, list):
                if any(isinstance(item, dict)
                       and _marker_count(item) >= FINDING_MARKER_THRESHOLD
                       for item in value):
                    return True
            if _is_conclusion_shaped(value):
                return True
    elif isinstance(node, list):
        return any(_is_conclusion_shaped(item) for item in node)
    return False


def _parse_timestamp(value: str) -> int:
    return calendar.timegm(time.strptime(value, _TIMESTAMP_FORMAT))


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------
class EvidenceStore:
    """Per-run provenance-bound evidence cache.

    `barrier_state` is a zero-arg callable returning True once the
    first-pass independence barrier is OPEN (both independent audits
    complete). `now` (keyword-only, injectable) supplies every timestamp
    the store writes; it defaults to state_store.utc_now_iso.
    """

    def __init__(self, run_dir: str,
                 barrier_state: Callable[[], bool],
                 *, now: Callable[[], str] | None = None):
        self.run_dir = os.path.abspath(os.fspath(run_dir))
        self._barrier_state = barrier_state
        self._now = now or utc_now_iso
        self._index_path = os.path.join(self.run_dir, INDEX_NAME)
        self._objects_root = os.path.join(self.run_dir, OBJECTS_DIR)
        self._log_path = os.path.join(self.run_dir, ACCESS_LOG_NAME)
        self._records: dict[str, dict[str, Any]] = {}
        self._log: list[dict[str, Any]] = []
        self._schema: dict[str, Any] | None = None
        self._load_index()
        self._load_log()

    # -- persistence --------------------------------------------------------
    def _load_index(self) -> None:
        if not os.path.isfile(self._index_path):
            return
        try:
            with open(self._index_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    record = json.loads(line)
                    if not isinstance(record, dict):
                        raise ValueError("index line is not an object")
                    self._records[record.get("evidence_id", "")] = record
        except (OSError, ValueError) as exc:
            raise EvidenceStoreError(
                "corrupt evidence index %s: %s" % (self._index_path, exc)
            ) from None

    def _load_log(self) -> None:
        if not os.path.isfile(self._log_path):
            return
        try:
            with open(self._log_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    entry = json.loads(line)
                    if isinstance(entry, dict):
                        self._log.append(entry)
        except (OSError, ValueError) as exc:
            raise EvidenceStoreError(
                "corrupt evidence access log %s: %s" % (self._log_path, exc)
            ) from None

    def _append_index(self, record: dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self._index_path), exist_ok=True)
        line = _canonical_json(record) + "\n"
        with open(self._index_path, "a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())

    def _write_object(self, result_digest: str, result: Any) -> None:
        os.makedirs(self._objects_root, exist_ok=True)
        atomic_write_json(os.path.join(self._objects_root,
                                       result_digest + ".json"), result)

    def _object_path(self, record: dict[str, Any]) -> str | None:
        """Absolute path of the payload, only when it lives inside this
        store's content-addressed objects root (result_location values that
        escape the store never resolve to content)."""
        location = record.get("result_location")
        if not isinstance(location, str) or not location:
            return None
        candidate = os.path.realpath(os.path.join(self.run_dir, location))
        root = os.path.realpath(self._objects_root) + os.sep
        if not candidate.startswith(root):
            return None
        return candidate if os.path.isfile(candidate) else None

    def _log_access(self, evidence_id: str, consumer: str, *,
                    served: bool, reason: str | None = None) -> None:
        entry: dict[str, Any] = {"evidence_id": evidence_id,
                                 "consumer": consumer,
                                 "at": self._now(),
                                 "served": served}
        if reason is not None:
            entry["reason"] = reason
        self._log.append(entry)
        os.makedirs(os.path.dirname(self._log_path), exist_ok=True)
        with open(self._log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, sort_keys=True, ensure_ascii=False)
                     + "\n")
            fh.flush()
            os.fsync(fh.fileno())

    # -- schema -------------------------------------------------------------
    def _schema_doc(self) -> dict[str, Any]:
        if self._schema is None:
            try:
                self._schema = json.loads(
                    SCHEMA_PATH.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise EvidenceStoreError(
                    "evidence-record schema unreadable (%s): %s"
                    % (SCHEMA_PATH, exc)) from None
        return self._schema

    # -- put ----------------------------------------------------------------
    def put(self, record: dict[str, Any]) -> str:
        """Validate + store one EvidenceRecord; returns the evidence_id.

        The record may carry a "result" key (the evidence payload); it is
        content-addressed into evidence/objects/ and never stored inline in
        the index. Idempotent by content: putting the same record twice
        returns the same id and does not duplicate. Fail-closed: any
        validation failure (schema, digest provenance, conclusion-shaped
        payload) raises EvidenceStoreError with NOTHING stored.
        """
        if not isinstance(record, dict):
            raise EvidenceStoreError(
                "evidence record must be a JSON object, got %r"
                % type(record).__name__)
        rec = json.loads(json.dumps(record))  # deep copy; caller keeps theirs
        result = rec.pop("result", None)

        version = rec.pop("schema_version", None)
        if version is not None and version != SCHEMA_VERSION:
            raise EvidenceStoreError(
                "unsupported evidence record schema_version %r" % (version,))
        rec["schema_version"] = SCHEMA_VERSION

        # provenance: the input digest must bind the recorded command+tool
        if "command_or_query" in rec and "tool" in rec:
            computed_input = compute_input_digest(rec["command_or_query"],
                                                  rec["tool"])
            claimed_input = rec.get("input_digest")
            if claimed_input is not None \
                    and claimed_input != computed_input:
                raise EvidenceStoreError(
                    "input_digest does not match the recorded "
                    "command_or_query + tool (provenance mismatch)")
            rec["input_digest"] = computed_input

        # payload: content-addressed, and NEVER conclusion-shaped
        if result is not None:
            if _is_conclusion_shaped(result):
                raise EvidenceStoreError(
                    "conclusions are not evidence: the result payload is "
                    "finding-shaped (markers %s)" % sorted(FINDING_SHAPE_KEYS))
            result_digest = compute_result_digest(result)
            claimed_digest = rec.get("result_digest")
            if claimed_digest is not None and claimed_digest != result_digest:
                raise EvidenceStoreError(
                    "result_digest does not match the result payload "
                    "(provenance mismatch)")
            rec["result_digest"] = result_digest
            rec["result_location"] = "evidence/objects/%s.json" % result_digest

        claimed_id = rec.pop("evidence_id", None)
        evidence_id = evidence_id_for(rec)
        rec["evidence_id"] = evidence_id

        errors = validate(rec, self._schema_doc(),
                          base_dir=SCHEMA_PATH.parent)
        if errors:
            raise EvidenceStoreError(
                "invalid evidence record: %s" % "; ".join(errors[:5]))
        if claimed_id is not None and claimed_id != evidence_id:
            raise EvidenceStoreError(
                "evidence_id does not match the canonical record content")

        if evidence_id in self._records:
            return evidence_id  # idempotent by content — no duplicate entry

        if result is not None:
            self._write_object(rec["result_digest"], result)
        self._append_index(rec)
        self._records[evidence_id] = rec
        return evidence_id

    # -- barrier / visibility ----------------------------------------------
    def _barrier_open(self) -> bool:
        try:
            return bool(self._barrier_state())
        except Exception:
            return False  # fail-closed: an unusable barrier is a closed one

    @staticmethod
    def _private_serves(producer: Any, consumer: Any) -> bool:
        """AUDITOR_PRIVATE pre-barrier family rule: OPUS-produced serves an
        OPUS consumer, CODEX serves CODEX, and HARNESS / SPECIALIST-<domain>
        producers are harness-ONLY (specialists are harness-side machinery,
        not an auditor family — one specialist never reads another's private
        probes). Unknown principals never family-match."""
        if not isinstance(producer, str) or not isinstance(consumer, str):
            return False
        if producer in ("OPUS", "CODEX"):
            return consumer == producer
        if producer == "HARNESS" or producer.startswith("SPECIALIST-"):
            return consumer == "HARNESS"
        return False

    def _visible(self, record: dict[str, Any], consumer: str) -> bool:
        visibility = record.get("visibility")
        if visibility == "SHARED_MECHANICAL":
            return True
        if self._barrier_open():
            return True  # the barrier opens both private and post-barrier
        if visibility == "AUDITOR_PRIVATE":
            return self._private_serves(record.get("producer"), consumer)
        return False

    def visible_to(self, evidence_id: str, consumer: str) -> bool:
        """Policy check only: would the visibility class + current barrier
        state allow `consumer` to see this record? No logging, no content,
        and deliberately NOT the FRESH_REQUIRED gate (that is a freshness
        question for get()/revalidate(), not a visibility question)."""
        record = self._records.get(evidence_id)
        if record is None:
            return False
        return self._visible(record, consumer)

    # -- get ----------------------------------------------------------------
    def get(self, evidence_id: str, consumer: str,
            include_content: bool = False) -> dict[str, Any] | None:
        """Serve an evidence REF (or, with include_content=True, the full
        record + payload) to `consumer` under visibility + freshness law.

        THE security boundary: SHARED_MECHANICAL always served;
        AUDITOR_PRIVATE only to the producer's family (or post-barrier);
        POST_BARRIER_SHARED only post-barrier; FRESH_REQUIRED NEVER served
        from cache regardless of everything else. Every lookup — served or
        denied — is appended to the access log (consumers never see the log
        through get()).
        """
        record = self._records.get(evidence_id)
        if record is None:
            self._log_access(evidence_id, consumer, served=False,
                             reason="not_found")
            return None
        policy = record.get("freshness_policy") or {}
        if policy.get("class") == "FRESH_REQUIRED":
            # the fresh gate can never be satisfied from cache; the record
            # is retained for audit history — retention is not reuse
            self._log_access(evidence_id, consumer, served=False,
                             reason="fresh_required")
            return None
        if not self._visible(record, consumer):
            self._log_access(evidence_id, consumer, served=False,
                             reason="barrier_closed")
            return None
        self._log_access(evidence_id, consumer, served=True)
        if not include_content:
            # just-in-time ref: id + digest + policy, no payload dumps
            return {key: record[key] for key in
                    ("evidence_id", "kind", "result_digest",
                     "freshness_policy", "visibility")}
        served = dict(record)
        obj_path = self._object_path(record)
        if obj_path is not None:
            try:
                with open(obj_path, "r", encoding="utf-8") as fh:
                    served["result"] = json.load(fh)
            except (OSError, ValueError) as exc:
                raise EvidenceStoreError(
                    "evidence payload unreadable (%s): %s"
                    % (obj_path, exc)) from None
        return served

    # -- freshness / reuse ----------------------------------------------------
    def revalidate(self, record: dict[str, Any],
                   current_fingerprint: str,
                   current_binding_digest: str,
                   changes: list[str] | None = None) -> bool:
        """Is reusing this cached record legal RIGHT NOW?

        True only when ALL hold:
          - repository_fingerprint_sha256 == current_fingerprint;
          - environment_binding_digest == current_binding_digest;
          - input_digest == a freshly recomputed digest of the recorded
            command_or_query + tool (tool name+version equality is bound
            inside this digest — a drifted tool changes the digest);
          - freshness class is CACHEABLE (FRESH_REQUIRED is never reusable);
          - ttl unexpired: record age from produced_at vs ttl_sec, measured
            on the injected store clock (ttl_sec null = no time limit);
          - no invalidation trigger the caller reports (`changes`) appears
            in the record's own invalidated_by list.
        Malformed/unparseable records fail closed to False.
        """
        if not isinstance(record, dict):
            return False
        try:
            if record.get("repository_fingerprint_sha256") \
                    != current_fingerprint:
                return False
            if record.get("environment_binding_digest") \
                    != current_binding_digest:
                return False
            tool = record.get("tool")
            command = record.get("command_or_query")
            if compute_input_digest(command, tool) \
                    != record.get("input_digest"):
                return False
            policy = record.get("freshness_policy")
            if not isinstance(policy, dict) \
                    or policy.get("class") != "CACHEABLE":
                return False
            invalidated_by = policy.get("invalidated_by") or []
            changes = changes or []
            if any(trigger in invalidated_by for trigger in changes):
                return False
            ttl_sec = policy.get("ttl_sec")
            if ttl_sec is not None:
                produced = _parse_timestamp(record["produced_at"])
                age = max(0, _parse_timestamp(self._now()) - produced)
                if age > ttl_sec:
                    return False
        except (EvidenceStoreError, KeyError, TypeError, ValueError):
            return False  # unprovable reuse is disallowed reuse
        return True

    # -- audit history --------------------------------------------------------
    def access_log(self, consumer: str | None = None) -> list[dict[str, Any]]:
        """Every get() ever issued against this store (served AND denied),
        optionally filtered by consumer. Harness-side audit API: consumers
        never see the log through get()."""
        if consumer is None:
            return [dict(entry) for entry in self._log]
        return [dict(entry) for entry in self._log
                if entry.get("consumer") == consumer]
