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

SESSION = os.environ.get("FAKE_CODEX_SESSION", "fake-session-123")


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
        "repository_fingerprint_sha256": os.environ.get(
            "FAKE_CODEX_FINGERPRINT", "deadbeefdeadbeef"),
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
    mode = os.environ.get("FAKE_CODEX_MODE", "ok")
    # consume stdin (the prompt) so the parent never blocks on the pipe
    try:
        sys.stdin.buffer.read()
    except Exception:
        pass

    if mode == "slow":
        time.sleep(float(os.environ.get("FAKE_CODEX_SLEEP", "2")))
        mode = "ok"

    if mode == "quota":
        if os.environ.get("FAKE_CODEX_USAGE_FIRST"):
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
