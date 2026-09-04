#!/usr/bin/env python3
"""Tier-2 seeded fixture corpus generator (pillar D, Task D.2).

Deterministic, NO models: builds ten tiny git repositories, each carrying
one REAL seeded defect (or, for negative-controls, deliberately
suspicious-looking-but-correct patterns that MUST stay unfound), plus a
sealed ground-truth file written OUTSIDE the fixture repo at
<fixtures-root>/sealed/<name>.json so it never enters auditor context.

Every build is fast (<2 s each), offline, and byte-deterministic (pinned
git identity eval@local + pinned commit dates). Real-model scoring runs
against these fixtures are budgeted separately and are NOT performed here.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from typing import Any, Callable

GIT_ENV = dict(os.environ)
GIT_ENV.update({
    "GIT_AUTHOR_NAME": "Audit Council Eval",
    "GIT_AUTHOR_EMAIL": "eval@local",
    "GIT_COMMITTER_NAME": "Audit Council Eval",
    "GIT_COMMITTER_EMAIL": "eval@local",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00",
    "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00",
})

SCHEMA_VERSION = 2


class FixtureError(RuntimeError):
    pass


def _git(repo: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, env=GIT_ENV, check=False)
    if proc.returncode != 0:
        raise FixtureError("git %s failed: %s" % (args, proc.stderr.strip()))
    return proc.stdout


def _write(root: str, relpath: str, content: str) -> None:
    path = os.path.join(root, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def _init_repo(dir_: str) -> None:
    os.makedirs(dir_, exist_ok=True)
    _git(dir_, "init", "-q", "-b", "main")
    _git(dir_, "config", "user.email", "eval@local")
    _git(dir_, "config", "user.name", "Audit Council Eval")


def _commit(repo: str, message: str) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)


def _truth(fixture: str, defects: list[dict], protected_controls: list[str],
           severity_range: str, environment_expectations: dict,
           cost_ceiling: dict, extra: dict | None = None) -> dict:
    doc = {
        "schema_version": SCHEMA_VERSION,
        "fixture": fixture,
        "defects": defects,
        "protected_controls": protected_controls,
        "severity_range": severity_range,
        "environment_expectations": environment_expectations,
        "cost_ceiling": cost_ceiling,
    }
    if extra:
        doc.update(extra)
    return doc


# ---------------------------------------------------------------------------
# 1. auth-bypass
# ---------------------------------------------------------------------------
_AUTH_DOCS = """// Document routes. Read access is owner-scoped via requireOwnership.
const express = require('express');
const { requireOwnership } = require('../domain/ownership');

module.exports = function documents(db) {
  const router = express.Router();


  // ownership check that every other mutating route enforces, so any
  // authenticated user can read arbitrary document ids.
  router.get('/:id', async (req, res) => {
    const doc = await db.documents.findById(req.params.id);
    if (!doc) return res.status(404).end();
    return res.json(doc);
  });

  router.delete('/:id', requireOwnership(req => req.params.id), async (req, res) => {
    await db.documents.remove(req.params.id);
    return res.status(204).end();
  });

  return router;
};
"""
_AUTH_OWNERSHIP = """// Ownership enforcement helper (protected control).
function requireOwnership(idOf) {
  return async (req, res, next) => {
    const id = idOf(req);
    const owned = await req.app.locals.db.documents.isOwnedBy(id, req.user.id);
    if (!owned) return res.status(403).json({ error: 'forbidden' });
    return next();
  };
}
module.exports = { requireOwnership };
"""
_AUTH_AUTH = """// JWT authentication (protected control): verifies and attaches req.user.
const jwt = require('./jwt');
module.exports = function authenticate(req, res, next) {
  const claims = jwt.verify(req.headers.authorization);
  if (!claims) return res.status(401).end();
  req.user = claims;
  return next();
};
"""


def _build_auth_bypass(dir_: str) -> None:
    _init_repo(dir_)
    _write(dir_, "package.json",
           '{\n  "name": "docservice",\n  "version": "1.4.0",\n'
           '  "main": "src/server.js"\n}\n')
    _write(dir_, "src/server.js",
           "const express = require('express');\n"
           "const authenticate = require('./middleware/authenticate');\n"
           "const documents = require('./routes/documents');\n"
           "const db = require('./db');\n"
           "const app = express();\n"
           "app.use(authenticate);\n"
           "app.use('/documents', documents(db));\n"
           "app.listen(8080);\n")
    _write(dir_, "src/middleware/authenticate.js", _AUTH_AUTH)
    _write(dir_, "src/domain/ownership.js", _AUTH_OWNERSHIP)
    _write(dir_, "src/routes/documents.js", _AUTH_DOCS)
    _write(dir_, "README.md",
           "# docservice\nOwner-scoped document store (eval fixture).\n")
    _commit(dir_, "feat: document routes with ownership enforcement")


def _truth_auth_bypass(dir_: str) -> dict:
    return _truth(
        "auth-bypass",
        defects=[{
            "id": "AUTH-BYPASS-1",
            "category": "AUTHORIZATION",
            "severity": "CRITICAL",
            "path": "src/routes/documents.js",
            "lines": "7-13",
            "snippet": "router.get('/:id', async (req, res) => {",
            "root_cause": "GET /documents/:id handler omits the "
                          "requireOwnership check enforced by the sibling "
                          "delete route; authentication is treated as "
                          "authorization",
            "expected_finding": "broken access control / IDOR on document "
                                "read path"}],
        protected_controls=["authenticate-jwt",
                            "ownership-delete-route-check"],
        severity_range=["CRITICAL", "HIGH"],
        environment_expectations={
            "mode": "CURRENT",
            "binding": "repo_root must equal the fixture root",
            "matrix_cases": ["1", "9", "10"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 2. stale-transaction-recovery
# ---------------------------------------------------------------------------
_RECOVERY_FILES = {
"journal.py": '''"""Append-only transaction journal (protected control)."""
class Journal:
    def __init__(self):
        self.entries = []       # [{txid, op, args}]
        self.commit_index = -1  # highest committed entry index

    def append(self, txid, op, args):
        self.entries.append({"txid": txid, "op": op, "args": args})
        return len(self.entries) - 1

    def commit(self, upto_index):
        self.commit_index = max(self.commit_index, upto_index)
''',
"checkpoint.py": '''"""Last-applied checkpoint, written at transaction START."""
class Checkpoint:
    def __init__(self):
        self.last_applied = -1

    def begin(self, journal_index):
        self.last_applied = journal_index  # stale after the tx commits
''',
"recovery.py": '''"""Crash recovery: replay journal entries past the checkpoint.

"""
def recover(journal, checkpoint, apply):
    for entry in journal.entries[checkpoint.last_applied + 1:]:
        apply(entry.op, entry.args)
    return len(journal.entries) - checkpoint.last_applied - 1
''',
"worker.py": '''from journal import Journal
from checkpoint import Checkpoint
from recovery import recover

journal = Journal()
checkpoint = Checkpoint()

def process(op, args):
    checkpoint.begin(len(journal.entries) - 1)
    idx = journal.append("tx", op, args)
    result = apply_once(op, args)
    journal.commit(idx)          # durable commit marker
    return result

def crash_restart(apply):
    return recover(journal, checkpoint, apply)

def apply_once(op, args):
    return (op, args)
''',
}


def _build_stale_tx(dir_: str) -> None:
    _init_repo(dir_)
    for name, content in _RECOVERY_FILES.items():
        _write(dir_, name, content)
    _write(dir_, "README.md",
           "# txworker\nJournal-based worker with crash recovery "
           "(eval fixture).\n")
    _commit(dir_, "feat: journal recovery path")


def _truth_stale_tx(dir_: str) -> dict:
    return _truth(
        "stale-transaction-recovery",
        defects=[{
            "id": "STALE-TX-1",
            "category": "STATE_INTEGRITY",
            "severity": "HIGH",
            "path": "recovery.py",
            "lines": "9-11",
            "snippet": "for entry in journal.entries[checkpoint.last_applied + 1:]:",
            "root_cause": "recovery replays from a checkpoint written at "
                          "transaction start and ignores the durable "
                          "commit_index, re-applying already-committed "
                          "transactions after a crash",
            "expected_finding": "post-commit stale state resurrection / "
                                "duplicate application on recovery"}],
        protected_controls=["journal-append-only",
                            "checkpoint-begin-marking"],
        severity_range=["CRITICAL", "HIGH"],
        environment_expectations={
            "mode": "CURRENT",
            "binding": "repo_root must equal the fixture root",
            "matrix_cases": ["1", "10"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 3. path-escape-toctou
# ---------------------------------------------------------------------------
_PATH_FILES = {
"storage.py": '''"""Attachment storage (protected control): open the RESOLVED path."""
import os

ATTACHMENT_DIR = "/srv/attachments"

def safe_open(root, name):
    resolved = os.path.realpath(os.path.join(root, name))
    if not resolved.startswith(os.path.realpath(root) + os.sep):
        raise PermissionError("path escapes root")
    return open(resolved, "rb")  # use the checked path itself
''',
"serve.py": '''"""HTTP attachment endpoints."""
import os
from storage import safe_open, ATTACHMENT_DIR

# validates `path`, but the handler then opens the ORIGINAL `path`; a
# symlink swapped between the two steps (or named with an embedded
# "../" segment the basename guard does not catch) escapes the
# attachment root.
def read_attachment(att_name):
    path = os.path.join(ATTACHMENT_DIR, att_name)
    if not os.path.basename(att_name).startswith(".."):
        if os.path.realpath(path).startswith(ATTACHMENT_DIR):
            os.stat(path)
        return open(path, "rb")
    raise PermissionError("bad attachment name")

def download_document(name):
    return safe_open(ATTACHMENT_DIR, name)
''',
}


def _build_path_escape(dir_: str) -> None:
    _init_repo(dir_)
    for name, content in _PATH_FILES.items():
        _write(dir_, name, content)
    _write(dir_, "app.py",
           "from serve import read_attachment\n\n"
           "def handler(env, start_response):\n"
           "    body = read_attachment(env.get('ATT_NAME', ''))\n"
           "    start_response('200 OK', [])\n"
           "    return [body.read()]\n")
    _write(dir_, "README.md",
           "# attachments\nAttachment service (eval fixture).\n")
    _commit(dir_, "feat: attachment serving")


def _truth_path_escape(dir_: str) -> dict:
    return _truth(
        "path-escape-toctou",
        defects=[{
            "id": "PATH-TOCTOU-1",
            "category": "PATH_TRAVERSAL",
            "severity": "CRITICAL",
            "path": "serve.py",
            "lines": "9-17",
            "snippet": "return open(path, \"rb\")",
            "root_cause": "containment is checked on os.path.realpath(path) "
                          "but the file is opened via the original "
                          "unresolved path, leaving a symlink-swap TOCTOU "
                          "window; the basename guard also misses embedded "
                          "'../' segments",
            "expected_finding": "TOCTOU path escape in attachment read"}],
        protected_controls=["safe-open-resolved-path",
                            "download-document-uses-safe-open"],
        severity_range=["CRITICAL", "HIGH"],
        environment_expectations={
            "mode": "CURRENT",
            "binding": "repo_root must equal the fixture root",
            "matrix_cases": ["3", "5", "6", "7"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 4. cross-tenant-access
# ---------------------------------------------------------------------------
_TENANT_FILES = {
"cache.py": '''"""Shared multi-tenant cache (protected on write)."""
class Cache:
    def __init__(self, backend):
        self.backend = backend

    def put(self, tenant_id, key, value, ttl=60):
        return self.backend.set("t:%s:%s" % (tenant_id, key),
                                value, ttl)

        # uses the bare key, so tenant B can observe tenant A's cached value
    # (and vice versa) whenever keys collide.
    def get(self, tenant_id, key):
        return self.backend.get(key)
''',
"api.py": '''from cache import Cache

class TenantAPI:
    def __init__(self, backend):
        self.cache = Cache(backend)

    def save_report(self, tenant_id, report_id, payload):
        return self.cache.put(tenant_id, "report:%s" % report_id, payload)

    def load_report(self, tenant_id, report_id):
        return self.cache.get(tenant_id, "report:%s" % report_id)
''',
}


def _build_cross_tenant(dir_: str) -> None:
    _init_repo(dir_)
    for name, content in _TENANT_FILES.items():
        _write(dir_, name, content)
    _write(dir_, "backend.py",
           "class MemoryBackend:\n"
           "    def __init__(self):\n"
           "        self.store = {}\n\n"
           "    def set(self, k, v, ttl):\n"
           "        self.store[k] = v\n\n"
           "    def get(self, k):\n"
           "        return self.store.get(k)\n")
    _write(dir_, "README.md",
           "# reports-api\nMulti-tenant reporting cache (eval fixture).\n")
    _commit(dir_, "feat: tenant report cache")


def _truth_cross_tenant(dir_: str) -> dict:
    return _truth(
        "cross-tenant-access",
        defects=[{
            "id": "TENANT-1",
            "category": "TENANT_ISOLATION",
            "severity": "CRITICAL",
            "path": "cache.py",
            "lines": "12-14",
            "snippet": "return self.backend.get(key)",
            "root_cause": "cache reads drop the 't:<tenant>:' scope that "
                          "writes apply, letting one tenant read another "
                          "tenant's cached report by reusing the key",
            "expected_finding": "cross-tenant data exposure via "
                                "unscoped cache read"}],
        protected_controls=["cache-put-tenant-scoping"],
        severity_range=["CRITICAL", "HIGH"],
        environment_expectations={
            "mode": "CURRENT",
            "binding": "repo_root must equal the fixture root",
            "matrix_cases": ["3", "4", "5"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 5. unsafe-migration
# ---------------------------------------------------------------------------
_MIGRATION_FILES = {
"migrations/0014_drop_audit_log.py": '''"""Drop the legacy audit log table (one-shot maintenance migration).

"""
import os

def up(conn):
    conn.autocommit = True
    conn.execute("DROP TABLE IF EXISTS audit_events")
    conn.execute("TRUNCATE TABLE audit_archive")
    conn.execute("DELETE FROM migration_lock WHERE id = 1")

def should_run():
    return os.environ.get("FORCE_DROP", "1") == "1"
''',
"migrations/runner.py": '''import importlib

def run_all(conn, names):
    for name in names:
        mod = importlib.import_module(name)
        if not mod.should_run():
            continue
        mod.up(conn)   # no transaction wrapping, no dry-run mode
''',
}


def _build_unsafe_migration(dir_: str) -> None:
    _init_repo(dir_)
    for name, content in _MIGRATION_FILES.items():
        _write(dir_, name, content)
    _write(dir_, "migrations/__init__.py", "")
    _write(dir_, "README.md",
           "# migrations\nSchema migrations (eval fixture).\n")
    _commit(dir_, "chore: drop legacy audit log")


def _truth_unsafe_migration(dir_: str) -> dict:
    return _truth(
        "unsafe-migration",
        defects=[{
            "id": "MIGRATION-1",
            "category": "DATA_LOSS",
            "severity": "HIGH",
            "path": "migrations/0014_drop_audit_log.py",
            "lines": "9-14",
            "snippet": "conn.autocommit = True",
            "root_cause": "destructive DROP/TRUNCATE/DELETE run with "
                          "autocommit outside any transaction, without a "
                          "pre-existence check or backup, gated by a flag "
                          "defaulting to destructive",
            "expected_finding": "irreversible data-loss migration without "
                                "transactional guard"}],
        protected_controls=["migration-runner-module-selection"],
        severity_range=["HIGH", "MEDIUM"],
        environment_expectations={
            "mode": "CURRENT",
            "binding": "repo_root must equal the fixture root",
            "matrix_cases": ["1", "10"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 6. api-drift
# ---------------------------------------------------------------------------
_API_SPEC = """openapi: 3.0.3
info:
  title: reports
  version: "2"
paths:
  /v2/reports:
    get:
      parameters:
        - name: pageSize
          in: query
          required: true
          schema: {type: integer}
      responses:
        "200":
          description: paginated reports
          content:
            application/json:
              schema:
                type: object
                required: [items, total]
                properties:
                  items: {type: array}
                  total: {type: integer}
"""
_API_HANDLER = '''
// route moved to /reports (spec: /v2/reports), query param renamed to
// `limit` (spec: pageSize, required), and the response envelope uses
// {data, count} (spec: {items, total}).
const express = require('express');

module.exports = function reports(db) {
  const router = express.Router();

  router.get('/reports', async (req, res) => {
    const limit = req.query.limit || 20;
    const rows = await db.reports.list(limit);
    return res.json({ data: rows, count: rows.length });
  });

  return router;
};
'''


def _build_api_drift(dir_: str) -> None:
    _init_repo(dir_)
    _write(dir_, "api/openapi.yaml", _API_SPEC)
    _write(dir_, "src/routes/reports.js", _API_HANDLER)
    _write(dir_, "package.json",
           '{\n  "name": "reports-api",\n  "version": "2.3.1",\n'
           '  "main": "src/routes/reports.js"\n}\n')
    _write(dir_, "README.md",
           "# reports-api\nContract-first reports service (eval fixture).\n")
    _commit(dir_, "feat: reports listing endpoint")


def _truth_api_drift(dir_: str) -> dict:
    return _truth(
        "api-drift",
        defects=[{
            "id": "API-DRIFT-1",
            "category": "CONTRACT_DRIFT",
            "severity": "HIGH",
            "path": "src/routes/reports.js",
            "lines": "10-13",
            "snippet": "router.get('/reports', async (req, res) => {",
            "root_cause": "implementation no longer satisfies the frozen "
                          "OpenAPI contract: path /reports vs /v2/reports, "
                          "param `limit` vs required `pageSize`, envelope "
                          "{data,count} vs {items,total}",
            "expected_finding": "published API contract drift between spec "
                                "and handler"}],
        protected_controls=["openapi-spec-frozen-as-contract"],
        severity_range=["HIGH", "MEDIUM"],
        environment_expectations={
            "mode": "CURRENT",
            "binding": "repo_root must equal the fixture root",
            "matrix_cases": ["1", "10"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 7. release-supply-chain
# ---------------------------------------------------------------------------
_RELEASE_SH = """#!/bin/sh
# Release packaging (eval fixture).
set -eu

# supply-chain inputs — a piped-to-shell installer from an unversioned
# URL and a floating base image tag — and the repo ships no lockfile or
# digest pinning, so released artifacts are not reproducible.
curl -fsSL https://get.example-infra.dev/install.sh | bash
docker pull example/build:latest
npm install --no-package-lock
tar -czf "release-$(date +%s).tgz" dist/
"""
_RELEASE_WORKFLOW = """name: release
on: { push: { tags: ['*'] } }
jobs:
  build:
    runs-on: ubuntu-latest
    container: example/build:latest   # floating tag, no digest pin
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/release.sh
"""


def _build_supply_chain(dir_: str) -> None:
    _init_repo(dir_)
    _write(dir_, "scripts/release.sh", _RELEASE_SH)
    os.chmod(os.path.join(dir_, "scripts/release.sh"), 0o755)
    _write(dir_, ".github/workflows/release.yml", _RELEASE_WORKFLOW)
    _write(dir_, "package.json",
           '{\n  "name": "svc",\n  "version": "0.9.0",\n'
           '  "dependencies": { "leftpad-utils": "^1.0.0" }\n}\n')
    _write(dir_, "README.md",
           "# svc\nService with release pipeline (eval fixture).\n")
    _commit(dir_, "ci: tag release pipeline")


def _truth_supply_chain(dir_: str) -> dict:
    return _truth(
        "release-supply-chain",
        defects=[{
            "id": "SUPPLY-CHAIN-1",
            "category": "SUPPLY_CHAIN",
            "severity": "HIGH",
            "path": "scripts/release.sh",
            "lines": "10-12",
            "snippet": "curl -fsSL https://get.example-infra.dev/install.sh | bash",
            "root_cause": "release path executes an unpinned remote "
                          "installer piped to a shell, pulls a floating "
                          "image tag, and installs dependencies without a "
                          "committed lockfile or digest pinning",
            "expected_finding": "unreproducible, attacker-controllable "
                                "release supply chain"}],
        protected_controls=["release-script-set-eu-fail-fast"],
        severity_range=["HIGH", "MEDIUM"],
        environment_expectations={
            "mode": "RELEASE",
            "binding": "isolated detached worktree at the tagged commit",
            "matrix_cases": ["11"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 8. evidence-provenance-mismatch
# ---------------------------------------------------------------------------
_LEDGER = '''"""Audit event ledger (protected control)."""
def append(events, kind, payload):
    events.append({"kind": kind, "payload": payload})
    return len(events) - 1


def summarize(events):
    return {"total": len(events),
            "kinds": sorted({e["kind"] for e in events})}
'''
_ADJUDICATION = '''{
  "schema_version": 2,
  "rounds": [
    {
      "round": 1,
      "resolutions": [
        {
          "finding_id": "F-002",
          "verdict": "CONFIRMED",
          "evidence": [
            {
              "kind": "OBSERVED_FACT",
              "path": "src/ledger.py",
              "lines": "120-132",
              "description": "append() double-writes the kind field",
              "artifact_hash": "8899aabbccddeeff0011223344556677aabbccdd"
            },
            {
              "kind": "OBSERVED_FACT",
              "path": "src/ledger.py",
              "lines": "12-14",
              "description": "summarize() counts kinds correctly",
              "artifact_hash": "3c2b7d09a1f4e5d6"
            }
          ]
        }
      ]
    }
  ]
}
'''


def _build_provenance(dir_: str) -> None:
    _init_repo(dir_)
    _write(dir_, "src/ledger.py", _LEDGER)
    _write(dir_, "audit-output/50-targeted-adjudication.json",
           _ADJUDICATION)
    _write(dir_, "docs/evidence-policy.md",
           "# Evidence policy\nEvery evidence item must cite a path, "
           "lines, and the artifact hash of the cited file as it exists "
           "in the audited tree.\n")
    _commit(dir_, "chore: checkpoint adjudication artifact")


def _truth_provenance(dir_: str) -> dict:
    return _truth(
        "evidence-provenance-mismatch",
        defects=[{
            "id": "PROVENANCE-1",
            "category": "EVIDENCE_INTEGRITY",
            "severity": "HIGH",
            "path": "audit-output/50-targeted-adjudication.json",
            "lines": "15-21",
            "snippet": "\"lines\": \"120-132\"",
            "root_cause": "committed adjudication artifact cites evidence "
                          "at src/ledger.py lines 120-132 with an "
                          "artifact_hash that does not match the file: the "
                          "ledger is only ~15 lines long, so the citation "
                          "cannot resolve in this tree",
            "expected_finding": "artifact evidence provenance does not "
                                "match the repository it claims to audit"}],
        protected_controls=["resolving-evidence-item-lines-12-14",
                            "evidence-policy-documented"],
        severity_range=["HIGH", "MEDIUM"],
        environment_expectations={
            "mode": "CURRENT",
            "binding": "repo_root must equal the fixture root",
            "matrix_cases": ["1", "10"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 9. structural-identity-mismatch
# ---------------------------------------------------------------------------
_MANIFEST = """{
  "name": "corelib",
  "version": "3.1.0",
  "modules": [
    "core/engine.py",
    "core/bridge.py",
    "adapters/http.py"
  ],
  "structure_sha256": "5f4dcc3b5aa765d61d8327deb882cf99"
}
"""
_ENGINE = '''"""Core engine (protected control)."""
class Engine:
    def __init__(self, bridge):
        self.bridge = bridge

    def run(self, task):
        return self.bridge.submit(task)
'''
_BRIDGE = '''"""Legacy bridge -- renamed in 3.1, name kept stale in manifest."""
class Bridge:
    def submit(self, task):
        return {"accepted": True, "task": task}
'''
_HTTP_ADAPTER = '''"""HTTP adapter (protected control)."""
from core.bridge import Bridge

def make_adapter():
    b = Bridge()
    return lambda req: b.submit(req)
'''


def _build_structural_identity(dir_: str) -> None:
    _init_repo(dir_)
    _write(dir_, "manifest.json", _MANIFEST)
    _write(dir_, "core/engine.py", _ENGINE)
    # NOTE: the manifest declares core/bridge.py, the tree ships the
    # renamed core/bridge_v2.py — the declared structural identity is
    # stale and the recorded digest matches neither.
    _write(dir_, "core/bridge_v2.py", _BRIDGE)
    _write(dir_, "adapters/http.py", _HTTP_ADAPTER)
    _write(dir_, "README.md",
           "# corelib\nModule manifest pinned at release (eval fixture).\n")
    _commit(dir_, "refactor: rename bridge module")


def _truth_structural_identity(dir_: str) -> dict:
    return _truth(
        "structural-identity-mismatch",
        defects=[{
            "id": "STRUCTURAL-1",
            "category": "IDENTITY_INTEGRITY",
            "severity": "HIGH",
            "path": "manifest.json",
            "lines": "4-10",
            "snippet": "\"core/bridge.py\"",
            "root_cause": "the declared module inventory still lists "
                          "core/bridge.py while the tree ships the renamed "
                          "core/bridge_v2.py, and the recorded "
                          "structure_sha256 was not recomputed — declared "
                          "structural identity diverges from the actual "
                          "tree, defeating manifest-based identity checks",
            "expected_finding": "declared structural identity does not "
                                "match repository contents"}],
        protected_controls=["engine-bridge-wiring",
                            "http-adapter-import-path"],
        severity_range=["HIGH", "MEDIUM"],
        environment_expectations={
            "mode": "RELEASE",
            "binding": "fingerprint must be derived from the ACTUAL tree, "
                       "never from the manifest",
            "matrix_cases": ["11", "12"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900})


# ---------------------------------------------------------------------------
# 10. negative-controls
# ---------------------------------------------------------------------------
_NEG_FILES = {
"src/sanitize.py": '''"""Log sanitization
correct by construction — the user value only ever passes through
re.escape before being embedded, so it can never act as a pattern)."""
import re

def sanitize_for_log(user_value):
    safe = re.escape(user_value)
    return re.sub(r"[\\x00-\\x1f]", "?", safe)
''',
"src/paths.py": '''"""Path joining
result is normalized and containment-checked BEFORE any use, and the
checked value is what gets opened)."""
import os

BASE = "/srv/share"

def read_shared(user_path):
    resolved = os.path.realpath(os.path.join(BASE, user_path))
    if not resolved.startswith(BASE + os.sep):
        raise PermissionError("escape")
    with open(resolved) as fh:   # opens the RESOLVED, checked path
        return fh.read()
''',
"src/sql.py": '''"""SQL construction
statement is assembled from in-repo constants only; user values stay
parameterized)."""
COLUMNS = ["id", "name", "created_at"]

def find_by(conn, column, value):
    assert column in COLUMNS
    stmt = "SELECT " + ", ".join(COLUMNS) + " FROM users WHERE " \\
           + column + " = ?"
    return conn.execute(stmt, (value,)).fetchall()
''',
"src/legacy.py": '''"""Historical code kept for reference
insecure call is fully commented out — dead text, not live code)."""

def modern_check(token, expected):
    import hmac
    return hmac.compare_digest(token, expected)

# def legacy_check(token, expected):    # removed 2024-audit
#     return token == expected          # timing-unsafe; dead code
''',
}


def _build_negative_controls(dir_: str) -> None:
    _init_repo(dir_)
    for name, content in _NEG_FILES.items():
        _write(dir_, name, content)
    _write(dir_, "README.md",
           "# clean-svc\n "
           "suspicious-looking but correct patterns (eval fixture).\n")
    _commit(dir_, "feat: clean service")


def _truth_negative_controls(dir_: str) -> dict:
    return _truth(
        "negative-controls",
        defects=[],
        protected_controls=["sanitize-re-escape",
                            "paths-resolved-containment",
                            "sql-constant-statement",
                            "legacy-commented-dead-code",
                            "hmac-compare-digest"],
        severity_range=[],
        environment_expectations={
            "mode": "CURRENT",
            "binding": "repo_root must equal the fixture root",
            "matrix_cases": ["1", "10"]},
        cost_ceiling={"input_tokens": 400000, "cached_input_tokens": 300000,
                      "output_tokens": 20000, "elapsed_sec": 900},
        extra={
            "must_not_flag": [
                {"path": "src/sanitize.py",
                 "pattern": "user-controlled regex lookalike; re.escape "
                            "makes it literal",
                 "expected_verdict": "SAFE"},
                {"path": "src/paths.py",
                 "pattern": "user input in os.path.join; normalized + "
                            "containment-checked before use",
                 "expected_verdict": "SAFE"},
                {"path": "src/sql.py",
                 "pattern": "string-built SQL over validated constant "
                            "column names; values parameterized",
                 "expected_verdict": "SAFE"},
                {"path": "src/legacy.py",
                 "pattern": "commented-out insecure comparison (dead "
                            "code, not a live finding)",
                 "expected_verdict": "SAFE"},
                {"path": "src/legacy.py",
                 "pattern": "hmac.compare_digest token check",
                 "expected_verdict": "SAFE"},
            ],
            "note": "protected negatives MUST stay unfound; any finding "
                    "against these patterns is a false positive",
        })


# ---------------------------------------------------------------------------
# registry + build_all + sealed truth loader
# ---------------------------------------------------------------------------
FIXTURE_SPECS: list[dict[str, Any]] = [
    {"name": "auth-bypass",
     "description": "express-style route returns a document without the "
                    "ownership check its sibling routes enforce",
     "severity_range": ["CRITICAL", "HIGH"],
     "protected_controls": ["authenticate-jwt",
                            "ownership-delete-route-check"],
     "environment_expectations": {"mode": "CURRENT",
                                  "matrix_cases": ["1", "9", "10"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_auth_bypass,
     "ground_truth": _truth_auth_bypass},
    {"name": "stale-transaction-recovery",
     "description": "crash recovery replays already-committed journal "
                    "entries from a stale checkpoint",
     "severity_range": ["CRITICAL", "HIGH"],
     "protected_controls": ["journal-append-only",
                            "checkpoint-begin-marking"],
     "environment_expectations": {"mode": "CURRENT",
                                  "matrix_cases": ["1", "10"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_stale_tx,
     "ground_truth": _truth_stale_tx},
    {"name": "path-escape-toctou",
     "description": "attachment read checks realpath containment but "
                    "opens the original path (symlink-swap TOCTOU)",
     "severity_range": ["CRITICAL", "HIGH"],
     "protected_controls": ["safe-open-resolved-path",
                            "download-document-uses-safe-open"],
     "environment_expectations": {"mode": "CURRENT",
                                  "matrix_cases": ["3", "5", "6", "7"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_path_escape,
     "ground_truth": _truth_path_escape},
    {"name": "cross-tenant-access",
     "description": "multi-tenant cache read drops the tenant scope that "
                    "writes apply",
     "severity_range": ["CRITICAL", "HIGH"],
     "protected_controls": ["cache-put-tenant-scoping"],
     "environment_expectations": {"mode": "CURRENT",
                                  "matrix_cases": ["3", "4", "5"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_cross_tenant,
     "ground_truth": _truth_cross_tenant},
    {"name": "unsafe-migration",
     "description": "destructive DDL with autocommit, no backup, "
                    "flag defaulting to destructive",
     "severity_range": ["HIGH", "MEDIUM"],
     "protected_controls": ["migration-runner-module-selection"],
     "environment_expectations": {"mode": "CURRENT",
                                  "matrix_cases": ["1", "10"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_unsafe_migration,
     "ground_truth": _truth_unsafe_migration},
    {"name": "api-drift",
     "description": "handler no longer satisfies the frozen OpenAPI "
                    "contract (path, param, envelope)",
     "severity_range": ["HIGH", "MEDIUM"],
     "protected_controls": ["openapi-spec-frozen-as-contract"],
     "environment_expectations": {"mode": "CURRENT",
                                  "matrix_cases": ["1", "10"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_api_drift,
     "ground_truth": _truth_api_drift},
    {"name": "release-supply-chain",
     "description": "release pipeline consumes unpinned remote installer, "
                    "floating image tag, no lockfile",
     "severity_range": ["HIGH", "MEDIUM"],
     "protected_controls": ["release-script-set-eu-fail-fast"],
     "environment_expectations": {"mode": "RELEASE",
                                  "matrix_cases": ["11"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_supply_chain,
     "ground_truth": _truth_supply_chain},
    {"name": "evidence-provenance-mismatch",
     "description": "committed adjudication artifact cites evidence "
                    "(path/lines/hash) that does not resolve in the tree",
     "severity_range": ["HIGH", "MEDIUM"],
     "protected_controls": ["resolving-evidence-item-lines-12-14",
                            "evidence-policy-documented"],
     "environment_expectations": {"mode": "CURRENT",
                                  "matrix_cases": ["1", "10"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_provenance,
     "ground_truth": _truth_provenance},
    {"name": "structural-identity-mismatch",
     "description": "manifest module inventory and structure digest are "
                    "stale after a rename",
     "severity_range": ["HIGH", "MEDIUM"],
     "protected_controls": ["engine-bridge-wiring",
                            "http-adapter-import-path"],
     "environment_expectations": {"mode": "RELEASE",
                                  "matrix_cases": ["11", "12"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_structural_identity,
     "ground_truth": _truth_structural_identity},
    {"name": "negative-controls",
     "description": "clean code with protected suspicious-looking-but-"
                    "correct patterns that MUST stay unfound",
     "severity_range": [],
     "protected_controls": ["sanitize-re-escape",
                            "paths-resolved-containment",
                            "sql-constant-statement",
                            "legacy-commented-dead-code",
                            "hmac-compare-digest"],
     "environment_expectations": {"mode": "CURRENT",
                                  "matrix_cases": ["1", "10"]},
     "cost_ceiling": {"input_tokens": 400000, "output_tokens": 20000,
                      "elapsed_sec": 900},
     "build": _build_negative_controls,
     "ground_truth": _truth_negative_controls},
]

FIXTURE_NAMES = tuple(spec["name"] for spec in FIXTURE_SPECS)


def sealed_root_for(root: str) -> str:
    """Sealed ground-truth directory for a fixtures root (outside every
    individual fixture repo, never served into auditor context)."""
    return os.path.join(os.path.abspath(root), "sealed")


def _seal(root: str, name: str, truth: dict) -> str:
    sealed_dir = sealed_root_for(root)
    os.makedirs(sealed_dir, exist_ok=True)
    path = os.path.join(sealed_dir, name + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(truth, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return path


def _repo_stats(repo: str) -> tuple[int, int]:
    files, lines = 0, 0
    for dirpath, _dirnames, filenames in os.walk(repo):
        if ".git" in os.path.relpath(dirpath, repo).split(os.sep):
            continue
        for fn in filenames:
            files += 1
            try:
                with open(os.path.join(dirpath, fn), "r",
                          encoding="utf-8") as fh:
                    lines += sum(1 for _ in fh)
            except (OSError, UnicodeDecodeError):
                pass
    return files, lines


def build_all(root: str) -> dict[str, Any]:
    """Build every fixture repo + its sealed truth under `root`.

    Repos land at <root>/<name>; sealed truths at <root>/sealed/<name>.json
    (i.e. <dir>/../sealed/<name>.json relative to each repo — outside the
    repo, so the truth can never enter auditor context). Deterministic:
    pinned identity and dates make rebuilds byte-identical.
    """
    root = os.path.abspath(root)
    os.makedirs(root, exist_ok=True)
    summary: dict[str, Any] = {"root": root,
                               "sealed_root": sealed_root_for(root),
                               "fixtures": {}}
    for spec in FIXTURE_SPECS:
        name = spec["name"]
        repo = os.path.join(root, name)
        if os.path.exists(repo):
            shutil.rmtree(repo)
        spec["build"](repo)
        truth = spec["ground_truth"](repo)
        sealed_path = _seal(root, name, truth)
        files, lines = _repo_stats(repo)
        head = _git(repo, "rev-parse", "HEAD").strip()
        summary["fixtures"][name] = {
            "repo": repo,
            "git_head": head,
            "files": files,
            "lines": lines,
            "sealed_truth": sealed_path,
            "defect_count": len(truth["defects"]),
            "protected_controls": truth["protected_controls"],
        }
    return summary


def load_ground_truth(name: str, root: str) -> dict:
    """Load a sealed ground truth, reading ONLY from the sealed root.

    Fail-closed: the fixture name must be a bare identifier (no path
    separators, no '..'), and the resolved path must stay inside
    <root>/sealed even after realpath resolution (symlink escapes are
    refused). Anything resolving outside the sealed root raises.
    """
    if (not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*",
                                                      name)
            or name in {".", ".."}):
        raise ValueError("invalid fixture name for sealed truth: %r" % (name,))
    sealed = sealed_root_for(root)
    path = os.path.join(sealed, name + ".json")
    real_sealed = os.path.realpath(sealed)
    real_path = os.path.realpath(path)
    if real_path != os.path.join(real_sealed, name + ".json"):
        raise PermissionError(
            "sealed ground truth must be read only from the sealed root "
            "(%s resolves outside %s)" % (path, real_sealed))
    if not os.path.isfile(real_path):
        raise FileNotFoundError("no sealed truth for fixture %r" % name)
    with open(real_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv: list[str] | None = None) -> int:
    import sys
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2 or argv[0] != "tier2-build":
        print("usage: tier2_fixtures.py tier2-build <root>", file=sys.stderr)
        return 2
    print(json.dumps(build_all(argv[1]), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
