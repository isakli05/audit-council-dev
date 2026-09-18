"""Shared deterministic test fixtures for the AUCDEV-023 EBS test battery.

Every credential byte in this battery is SYNTHETIC and INERT.  Every
launched child is a repository test fixture.  No provider client, network
call, or real credential exists anywhere in this battery.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

EBS_ROOT = Path(__file__).resolve().parents[1]
if str(EBS_ROOT) not in sys.path:
    sys.path.insert(0, str(EBS_ROOT))

from ebs.binding import (REQUIRED_GATES, parse_binding,  # noqa: E402
                         valid_binding_document)

# The one synthetic inert credential literal used by the whole battery.
SYNTH_CRED = b"EBS-SYNTHETIC-INERT-CREDENTIAL-7c31d9f0-NOT-REAL-0001"

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def sha_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pipe_source(data: bytes = SYNTH_CRED) -> int:
    """Operator-style pipe credential source (writer closes after write)."""
    r, w = os.pipe()
    os.write(w, data)
    os.close(w)
    return r


def sealed_memfd_source(data: bytes = SYNTH_CRED, seals: int = 0x0F) -> int:
    """Fully (or partially) sealed memfd credential source."""
    from ebs.custody import (MFD_ALLOW_SEALING, MFD_CLOEXEC, F_ADD_SEALS,
                             memfd_create)
    fd = memfd_create("ebs-test-source", MFD_CLOEXEC | MFD_ALLOW_SEALING)
    os.write(fd, data)
    if seals:
        import fcntl
        fcntl.fcntl(fd, F_ADD_SEALS, seals)
    return fd


def make_launcher(tmp_path: Path, variant: str = "a") -> "tuple[Path, str]":
    """Materialize an inert fixture launcher with a runnable shebang.

    Returns (path, sha256).  The shebang is rewritten to the current
    interpreter so the fixture is executable on this host deterministically.
    """
    src = FIXTURES / f"inert_boundary_launcher_{variant}.py"
    dst = tmp_path / f"launcher_{variant}.py"
    text = src.read_text()
    text = text.replace("#!/usr/bin/python3\n", f"#!{sys.executable}\n", 1)
    dst.write_text(text)
    os.chmod(dst, 0o755)
    return dst, sha_hex(dst.read_bytes())


def binding_for(launcher_sha: str, **overrides) -> dict:
    doc = valid_binding_document(
        event_id="evt-0011223344556677",
        role="AUDITOR_A",
        launcher_sha256=launcher_sha,
    )
    for key, value in overrides.items():
        doc[key] = value
    return doc


def write_binding(tmp_path: Path, doc: dict) -> Path:
    path = tmp_path / "binding.json"
    path.write_text(json.dumps(doc, indent=2, sort_keys=True))
    return path


@pytest.fixture
def cust_dir(tmp_path):
    root = tmp_path / "accounting"
    root.mkdir(mode=0o700)
    os.chmod(root, 0o700)
    return root


@pytest.fixture
def out_dir(tmp_path):
    root = tmp_path / "custody-out"
    root.mkdir(mode=0o700)
    os.chmod(root, 0o700)
    return root


@pytest.fixture
def launcher(tmp_path):
    return make_launcher(tmp_path, "a")


@pytest.fixture
def launcher_b(tmp_path):
    return make_launcher(tmp_path, "b")


@pytest.fixture
def binding_doc(launcher):
    return binding_for(launcher[1])


@pytest.fixture
def parsed_binding(binding_doc):
    return parse_binding(json.dumps(binding_doc).encode())


def scan_tree_for(root: Path, needle: bytes) -> "list[Path]":
    """Return files under root whose content contains needle."""
    hits = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            if needle in path.read_bytes():
                hits.append(path)
    return hits
