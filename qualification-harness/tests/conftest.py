"""Shared fixtures for the qualification-harness deterministic tests.

All tests are local/deterministic and NEVER contact external providers:
payloads are local scripts, credentials are synthetic inert fixtures,
and every boundary launch runs under hard no-egress namespaces.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

HARNESS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HARNESS_ROOT))

from qh.boundary import bwrap_path  # noqa: E402
from qh.compose import CompositionEnv  # noqa: E402

HAVE_BWRAP = bwrap_path() is not None
HAVE_USERNS_NET = False
try:
    import shutil
    _un = shutil.which("unshare")
    if _un:
        HAVE_USERNS_NET = subprocess.run(
            [_un, "--user", "--map-root-user", "--net", "/bin/true"],
            capture_output=True, timeout=10).returncode == 0
except Exception:  # noqa: BLE001
    HAVE_USERNS_NET = False


@pytest.fixture()
def env(tmp_path):
    e = CompositionEnv(str(tmp_path / "workspace"))
    yield e
    e.cleanup_procs()


@pytest.fixture()
def live_controller():
    """Spawn a synthetic live controller process whose ACTUAL
    /proc/<pid>/environ carries the given CLAUDE_CONFIG_DIR (and any
    extra env); yield (proc, pid, starttime)."""
    procs = []

    def _spawn(claude_config_dir: str, extra_env: dict | None = None,
               hold_seconds: int = 120):
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
               "CLAUDE_CONFIG_DIR": claude_config_dir}
        if extra_env:
            env.update(extra_env)
        proc = subprocess.Popen(
            [sys.executable, "-c",
             f"import time; time.sleep({hold_seconds})"],
            env=env)
        procs.append(proc)
        from qh.util import proc_starttime
        st = proc_starttime(proc.pid)
        assert st is not None
        return proc, proc.pid, st

    yield _spawn
    for p in procs:
        p.kill()
        p.wait(timeout=10)


requires_bwrap = pytest.mark.skipif(
    not HAVE_BWRAP, reason="bubblewrap not available")
requires_userns = pytest.mark.skipif(
    not HAVE_USERNS_NET, reason="unprivileged user+net namespaces "
    "unavailable")
