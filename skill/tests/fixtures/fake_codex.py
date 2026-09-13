#!/usr/bin/env python3
"""fake_codex.py — mock `codex` executable for audit-council tests.

Driven by FAKE_CODEX_MODE (default "ok"):
  ok               write valid -o output + JSONL events (thread.started with
                   session id, turn.completed with token usage), exit 0
  exit0_no_output  exit 0 without writing -o output          (scenario G)
  malformed_json   write invalid JSON to -o, exit 0           (scenario H)
  partial_jsonl    valid -o output, truncated/partial JSONL   (scenario I)
  quota            stderr mentions usage limit, exit 1        (scenario K)
  auth             stderr "not logged in", exit 1             (scenario L)
  crash            exit 137                                   (scenario J)
  slow             sleep FAKE_CODEX_SLEEP (float seconds), then behave as ok

FAKE_CODEX_SESSION overrides the emitted session id (default fake-session-123).
"""
import os
import sys
import time


def _control_file_values():
    """B-001 fixture channel: the production sandbox clears the
    environment (--clearenv), so test control knobs are delivered via a
    <run-dir>/fake-codex-control KEY=VALUE file (written by the test
    harness next to the -o output path) instead of env vars. Env vars
    remain supported for direct, unsandboxed invocations."""
    ctrl = {}
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a in ("-o", "--output-last-message") and i + 1 < len(argv):
            run_dir = os.path.dirname(os.path.dirname(
                os.path.abspath(argv[i + 1])))
            path = os.path.join(run_dir, "fake-codex-control")
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    for line in fh:
                        if "=" in line:
                            key, val = line.strip().split("=", 1)
                            if key and val:
                                ctrl[key] = val
            except OSError:
                pass
            break
    return ctrl


_CTRL = _control_file_values()
SESSION = _CTRL.get("SESSION") or os.environ.get(
    "FAKE_CODEX_SESSION", "fake-session-123")
MODE = _CTRL.get("MODE") or os.environ.get("FAKE_CODEX_MODE", "ok")
FINGERPRINT = _CTRL.get("FINGERPRINT") or os.environ.get(
    "FAKE_CODEX_FINGERPRINT")
USAGE_FIRST = _CTRL.get("USAGE_FIRST") or os.environ.get(
    "FAKE_CODEX_USAGE_FIRST")
SLEEP = _CTRL.get("SLEEP") or os.environ.get("FAKE_CODEX_SLEEP")


def out_path_from_argv(argv):
    for i, a in enumerate(argv):
        if a in ("-o", "--output-last-message") and i + 1 < len(argv):
            return argv[i + 1]
    return None


def schema_kind(argv):
    for i, a in enumerate(argv):
        if a == "--output-schema" and i + 1 < len(argv):
            p = argv[i + 1]
            if "independent" in p:
                return "independent"
            if "cross" in p:
                return "cross"
            if "adjudication" in p:
                return "adjudication"
    return "independent"


def valid_output(kind):
    if kind == "cross":
        return {"examiner": "CODEX", "examined": "OPUS", "challenges": []}
    if kind == "adjudication":
        return {"rounds": [{
            "cluster_id": "CLUSTER-001",
            "evidence_packet": {"claim": "c"},
            "opus_verdict": "CONFIRMED",
            "codex_verdict": "CONFIRMED",
            "final_status": "CONFIRMED",
            "rationale": "r",
        }]}
    doc = {
        "model": "gpt-5.6-sol",
        "repository_fingerprint_sha256": FINGERPRINT or "deadbeefdeadbeef",
        "audit_summary": "fake independent audit",
        "findings": [],
    }
    return doc


def emit_events(partial=False):
    w = sys.stdout.write
    if partial:
        w('{"type":"thread.started","thread_id":"%s"' % SESSION)  # truncated line
        return
    w('{"type":"thread.started","thread_id":"%s"}\n' % SESSION)
    w('{"type":"turn.completed","usage":{"input_tokens":100,'
      '"cached_input_tokens":50,"output_tokens":200,'
      '"reasoning_output_tokens":80}}\n')


def main():
    argv = sys.argv[1:]
    mode = MODE
    # consume stdin (the prompt) so the parent never blocks on the pipe
    try:
        sys.stdin.buffer.read()
    except Exception:
        pass

    # F-A-06: serve the sandbox-preflight probes deterministically so the
    # suite never depends on a host-installed, logged-in real codex
    if argv[:1] == ["--version"]:
        sys.stdout.write("codex-cli 0.153.4 (fake)\n")
        return 0
    if argv[:2] == ["login", "status"]:
        sys.stdout.write("Logged in using ChatGPT subscription (fake)\n")
        return 0

    if mode == "slow":
        time.sleep(float(SLEEP or "2"))
        mode = "ok"

    if mode == "quota":
        if USAGE_FIRST:
            # real-world shape: a completed usage-bearing turn, THEN quota
            emit_events()
        sys.stderr.write("codex: usage limit reached for your plan (429)\n")
        return 1
    if mode == "auth":
        sys.stderr.write("codex: error: not logged in (run codex login), 401\n")
        return 1
    if mode == "crash":
        return 137

    outp = out_path_from_argv(argv)
    if mode == "exit0_no_output":
        emit_events()
        return 0
    if mode == "malformed_json":
        if outp:
            with open(outp, "w") as f:
                f.write('{"model": "gpt-5.6-sol", "broken": ')
        emit_events()
        return 0
    if mode == "partial_jsonl":
        if outp:
            import json
            with open(outp, "w") as f:
                json.dump(valid_output(schema_kind(argv)), f)
                f.write("\n")
        emit_events(partial=True)
        return 0
    # ok
    if outp:
        import json
        with open(outp, "w") as f:
            json.dump(valid_output(schema_kind(argv)), f)
            f.write("\n")
    emit_events()
    return 0


if __name__ == "__main__":
    sys.exit(main())
