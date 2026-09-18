"""Credential custody tests (synthetic inert fixtures ONLY)."""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from qh.custody import (CredentialCustody, CustodyError,
                        SyntheticInertAdapter)
from qh.util import Redactor

SYNTH = "SYNTHETIC-INERT-CREDENTIAL-abcd1234-do-not-use"


def _pipe_with(value: str) -> int:
    r, w = os.pipe()
    os.write(w, value.encode())
    os.close(w)
    return r


def test_establish_from_pipe_ok():
    red = Redactor()
    fd = _pipe_with(SYNTH)
    custody = CredentialCustody.establish(fd, label="synthetic", redactor=red)
    assert custody.label == "synthetic"
    assert custody.length == len(SYNTH)
    assert red.scrub(f"leak {SYNTH} end") == \
        "leak <REDACTED:synthetic> end"
    custody.teardown()
    with pytest.raises(CustodyError):
        custody.fd


def test_establish_refuses_ordinary_file(tmp_path):
    p = tmp_path / "cred.txt"
    p.write_text(SYNTH)
    red = Redactor()
    with pytest.raises(CustodyError, match="ORDINARY_FILE"):
        CredentialCustody.establish(os.open(p, os.O_RDONLY),
                                    label="synthetic", redactor=red)


def test_establish_refuses_empty(tmp_path):
    red = Redactor()
    r, w = os.pipe()
    os.close(w)  # empty pipe
    with pytest.raises(CustodyError, match="LENGTH_INVALID"):
        CredentialCustody.establish(r, label="synthetic", redactor=red)


def test_child_plan_and_teardown_deterministic():
    red = Redactor()
    fd = _pipe_with(SYNTH)
    custody = CredentialCustody.establish(fd, label="synthetic", redactor=red)
    adapter = SyntheticInertAdapter()
    plan = custody.child_plan(adapter.child_target_path())
    assert plan.fd == custody.fd
    assert plan.length == len(SYNTH)
    assert plan.target_path.startswith("/tmp/")
    custody.teardown()
    custody.teardown()  # idempotent bounded cleanup


def test_dumpable_supervisor_memory_not_same_uid_readable():
    """Kernel-process-bound proof: a supervisor subprocess that set
    PR_SET_DUMPABLE=0 cannot be inspected by a SAME-UID process (the
    controller's position) — /proc/<pid>/environ, /proc/<pid>/mem and
    /proc/<pid>/fd listing must all be denied."""
    code = (
        "import ctypes, os, time\n"
        "libc = ctypes.CDLL(None)\n"
        "assert libc.prctl(4, 0, 0, 0, 0) == 0\n"  # PR_SET_DUMPABLE=0
        "print(os.getpid(), flush=True)\n"
        "time.sleep(60)\n"
    )
    sup = subprocess.Popen([sys.executable, "-c", code],
                           stdout=subprocess.PIPE)
    pid = int(sup.stdout.readline().decode().strip())
    try:
        attacker = (
            "import os, sys, json\n"
            f"pid = {pid}\n"
            "results = {}\n"
            "try:\n"
            "    open(f'/proc/{pid}/environ','rb').read(); "
            "results['environ']='READ'\n"
            "except OSError as e: results['environ']=type(e).__name__\n"
            "try:\n"
            "    open(f'/proc/{pid}/mem','rb'); results['mem']='READ'\n"
            "except OSError as e: results['mem']=type(e).__name__\n"
            "try:\n"
            "    os.listdir(f'/proc/{pid}/fd'); results['fdlist']='READ'\n"
            "except OSError as e: results['fdlist']=type(e).__name__\n"
            "print(json.dumps(results))\n"
        )
        out = subprocess.run([sys.executable, "-c", attacker],
                             capture_output=True, text=True, timeout=30)
        results = json.loads(out.stdout.strip().splitlines()[-1])
        assert results["environ"] != "READ"
        assert results["mem"] != "READ"
        assert results["fdlist"] != "READ"
    finally:
        sup.kill()
        sup.wait(timeout=10)


def test_no_plaintext_in_ledger_or_outputs(env):
    """After a full flow, no synthetic credential value may appear in any
    ordinary-file output of the harness."""
    from qh.compose import SYNTHETIC_CREDENTIAL
    attempt = "custody-sec-0001"
    env.author_spec(attempt)
    grant = env.mint(attempt)
    sup = env.start_supervisor(grant)
    response = env.controller_request(attempt,
                                      own_session_slug="own-slug")
    rc, err = env.supervisor_outcome(sup)
    assert response.get("ok"), (response, err)
    needle = SYNTHETIC_CREDENTIAL.encode()
    for root, _dirs, files in os.walk(env.operator_state):
        for f in files:
            data = open(os.path.join(root, f), "rb").read()
            assert needle not in data, f"credential leak in {f}"
    assert needle not in err.encode()
