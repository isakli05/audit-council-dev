"""Hard no-egress gate tests: deterministic fixture evaluation, REAL
namespace regression (bare-netns AF_UNIX escape) and boundary gating."""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from qh.noegress import (NetFacts, NoEgressSpec, check_noegress,
                         collect_net_facts)

from conftest import HAVE_USERNS_NET, HARNESS_ROOT, requires_bwrap, \
    requires_userns


def _clean_facts(**over) -> NetFacts:
    facts = NetFacts(
        netns_inode="net:[1111]", mntns_inode="mnt:[2222]",
        parent_mntns_inode="mnt:[9999]",
        inherited_socket_fds=[], ns_fds=[],
        ifaces={"lo": {"up": False, "addr4": [], "addr6": []}},
        route4_rows=[], route6_usable=[], lo_state="down",
        mask_results=[{"path": p, "exists": False, "connectable": False}
                      for p in NoEgressSpec().mask_paths],
        dns_results=[{"host": h, "resolved": False, "error": "blocked"}
                     for h in NoEgressSpec().dns_hosts],
        tcp_results=[{"host": h, "port": p, "connected": False,
                      "error": "blocked"}
                     for h, p in NoEgressSpec().tcp_targets],
        setns_regain="denied")
    for k, v in over.items():
        setattr(facts, k, v)
    return facts


def test_clean_facts_pass():
    gate = check_noegress(_clean_facts(), NoEgressSpec())
    assert gate.passed, gate.failures


def test_inherited_socket_fd_fails():
    gate = check_noegress(_clean_facts(inherited_socket_fds=[0]),
                          NoEgressSpec())
    assert not gate.passed
    assert "ZERO_INHERITED_SOCKET_FDS" in gate.failures


def test_inherited_netns_fd_fails():
    gate = check_noegress(_clean_facts(ns_fds=[7]), NoEgressSpec())
    assert "NO_INHERITED_NETNS_FD" in gate.failures


def test_shared_mountns_fails():
    gate = check_noegress(
        _clean_facts(mntns_inode="mnt:[9999]", parent_mntns_inode="mnt:[9999]"),
        NoEgressSpec())
    assert "FRESH_MOUNT_NAMESPACE" in gate.failures


def test_address_or_route_fails():
    g1 = check_noegress(_clean_facts(
        ifaces={"lo": {"up": False, "addr4": ["10.0.0.5"], "addr6": []}}),
        NoEgressSpec())
    assert "NO_USABLE_IPV4_ADDRESS" in g1.failures
    g2 = check_noegress(_clean_facts(route4_rows=["default via 1.2.3.4"]),
                        NoEgressSpec())
    assert "NO_USABLE_ROUTE" in g2.failures
    g3 = check_noegress(_clean_facts(route6_usable=["2001:db8::/32"]),
                        NoEgressSpec())
    assert "NO_USABLE_ROUTE" in g3.failures


def test_loopback_up_fails_frozen_profile():
    gate = check_noegress(_clean_facts(
        ifaces={"lo": {"up": True, "addr4": [], "addr6": []}},
        lo_state="up"), NoEgressSpec())
    assert "LOOPBACK_DOWN" in gate.failures


def test_systemd_resolved_escape_surface_fails():
    """Deterministic regression check for the historical finding
    SYSTEMD_RESOLVED_AF_UNIX_ESCAPE_SURFACE: a connectable
    /run/systemd/resolve socket (bare netns without mount isolation)
    must FAIL the gate."""
    mask = [{"path": "/run/systemd/resolve", "exists": True,
             "connectable": True},
            {"path": "/run/dbus", "exists": False, "connectable": False}]
    gate = check_noegress(_clean_facts(mask_results=mask), NoEgressSpec())
    assert not gate.passed
    assert "MASKED:/run/systemd/resolve" in gate.failures


def test_dns_or_tcp_success_fails():
    dns = [dict(r, resolved=True) for r in _clean_facts().dns_results]
    g1 = check_noegress(_clean_facts(dns_results=dns), NoEgressSpec())
    assert any(f.startswith("DNS_BLOCKED") for f in g1.failures)
    tcp = [dict(r, connected=True) for r in _clean_facts().tcp_results]
    g2 = check_noegress(_clean_facts(tcp_results=tcp), NoEgressSpec())
    assert any(f.startswith("TCP_BLOCKED") for f in g2.failures)


def test_setns_regain_fails_denied_passes():
    g1 = check_noegress(_clean_facts(setns_regain="regained"),
                        NoEgressSpec())
    assert "DESCENDANTS_CANNOT_REGAIN_HOST_NETNS" in g1.failures
    for ok in ("denied", "denied-inaccessible", "no_foreign_pid1"):
        g = check_noegress(_clean_facts(setns_regain=ok), NoEgressSpec())
        assert "DESCENDANTS_CANNOT_REGAIN_HOST_NETNS" not in g.failures


# ------------------------------------------------------- live checks ----

@requires_userns
def test_bare_netns_escape_regression_live():
    """REAL regression: inside a bare user+net namespace WITHOUT a
    private mount namespace the host systemd-resolved AF_UNIX socket is
    still connectable and the gate FAILS (the historical v1 finding).
    No external DNS query is performed — only local socket
    connectability is probed (dns/tcp probes disabled)."""
    script = (
        "import json,sys; sys.path.insert(0, %r)\n"
        "from qh.noegress import NetFacts, NoEgressSpec, check_noegress, "
        "collect_net_facts\n"
        "spec = NoEgressSpec(dns_hosts=(), tcp_targets=())\n"
        "facts = collect_net_facts(spec)\n"
        "gate = check_noegress(facts, spec)\n"
        "print(json.dumps({'passed': gate.passed, 'failures': "
        "gate.failures, 'lo': facts.lo_state}))\n" % str(HARNESS_ROOT)
    )
    out = subprocess.run(
        ["unshare", "--user", "--map-root-user", "--net",
         sys.executable, "-c", script],
        capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    result = json.loads(out.stdout.strip().splitlines()[-1])
    assert not result["passed"]
    assert "MASKED:/run/systemd/resolve" in result["failures"]
    # and the fresh netns basics really held
    assert result["lo"] in (None, "down")


@requires_userns
def test_bare_netns_ipv4_and_lo_observed():
    """Sanity for the collector itself inside a real fresh netns."""
    script = (
        "import json,sys; sys.path.insert(0, %r)\n"
        "from qh.noegress import NoEgressSpec, collect_net_facts\n"
        "f = collect_net_facts(NoEgressSpec(dns_hosts=(), tcp_targets=()))\n"
        "print(json.dumps({'ifaces': f.ifaces, 'route4': f.route4_rows, "
        "'route6_usable': f.route6_usable, 'lo': f.lo_state, "
        "'sock_fds': f.inherited_socket_fds}))\n" % str(HARNESS_ROOT)
    )
    out = subprocess.run(
        ["unshare", "--user", "--map-root-user", "--net",
         sys.executable, "-c", script],
        capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    f = json.loads(out.stdout.strip().splitlines()[-1])
    assert set(f["ifaces"]) == {"lo"}
    assert f["lo"] == "down"
    assert f["route4"] == []
    assert f["route6_usable"] == []


@requires_bwrap
@requires_userns
def test_boundary_gate_pass_live(tmp_path):
    """Full boundary (bwrap, private mount ns, masked by absence):
    the gate PASSES inside the composed environment."""
    from qh.boundary import BoundarySpec, launch
    spec = BoundarySpec(harness_root=str(HARNESS_ROOT), payload_argv=None,
                        noegress=NoEgressSpec())
    result = launch(spec, timeout=90)
    gate = result.gate
    assert gate is not None, (result.returncode, result.stderr[:400])
    assert gate["passed"], gate["failures"]
    assert result.returncode == 0


@requires_userns
def test_inherited_socket_fd_fails_live():
    """REAL mechanism for the zero-inherited-socket-FD invariant (v1
    finding regression: the first wrapper exposed an inherited socket
    descriptor on fd 0): with a socket descriptor actually present in
    the gated process, the gate FAILS before any launch."""
    script = (
        "import json,socket,sys; sys.path.insert(0, %r)\n"
        "a,b = socket.socketpair()  # the 'inherited' socket fd\n"
        "from qh.noegress import NoEgressSpec, check_noegress, "
        "collect_net_facts\n"
        "spec = NoEgressSpec(dns_hosts=(), tcp_targets=())\n"
        "facts = collect_net_facts(spec)\n"
        "gate = check_noegress(facts, spec)\n"
        "print(json.dumps({'passed': gate.passed, 'failures': "
        "gate.failures, 'sock_count': len(facts.inherited_socket_fds)}))\n"
        % str(HARNESS_ROOT)
    )
    out = subprocess.run(
        ["unshare", "--user", "--map-root-user", "--net",
         sys.executable, "-c", script],
        capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    result = json.loads(out.stdout.strip().splitlines()[-1])
    assert result["sock_count"] >= 1
    assert not result["passed"]
    assert "ZERO_INHERITED_SOCKET_FDS" in result["failures"]


@requires_bwrap
@requires_userns
def test_boundary_noegress_with_payload_reports_zero_egress(env):
    """Gate + gatew payload over the full role layout: no-egress holds
    for the whole rehearsal environment (DNS/TCP probes execute inside
    and must fail; custody not required for the ops matrix)."""
    from qh.boundary import RESULT_FILE_INNER, BoundarySpec, launch
    spec = BoundarySpec(
        harness_root=str(HARNESS_ROOT),
        payload_argv=["/usr/bin/python3",
                      "/opt/qh/fixtures/gatew_payload.py",
                      "--result-file", RESULT_FILE_INNER],
        ro_binds=[(str(env.evidence), "/evidence"),
                  (str(env.codex_home_dir), "/codex-home"),
                  (str(env.target), "/target")],
        rw_binds=[(str(env.auditor_output), "/auditor-output")],
        noegress=NoEgressSpec())
    result = launch(spec, timeout=120)
    assert result.gate and result.gate["passed"], \
        (result.gate, result.stderr[:400])
    payload = result.payload_result
    assert payload is not None and payload["all_expected"], payload
