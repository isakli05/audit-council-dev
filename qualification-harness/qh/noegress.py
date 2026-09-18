"""Hard no-egress prelaunch gate (AUCDEV-023 G-2 clean reproduction).

Must run BEFORE any provider-capable launch, INSIDE the environment that
would launch (the boundary child evaluates it after namespace creation
and before payload exec).

Verified properties for the demonstrated Linux host class:

* fresh network namespace;
* fresh/private mount namespace where required (AF_UNIX host paths are
  NOT mediated by a network namespace — the SYSTEMD_RESOLVED_AF_UNIX_
  ESCAPE_SURFACE finding: a bare netns left host systemd-resolved
  reachable over /run/systemd/resolve/io.systemd.Resolve and DNS names
  RESOLVED despite zero interfaces/routes);
* no usable IPv4/IPv6 address; no usable route (the unconditional
  multicast/local IPv6 stub routes present in every netns are not
  usable routes);
* loopback DOWN (frozen demonstrated profile);
* DNS resolution blocked; representative external TCP blocked;
* /run/systemd/resolve inaccessible/masked; /run/dbus masked;
* inherited socket FD count == ZERO
  (HARD_NO_EGRESS_GATE_MUST_REQUIRE_ZERO_INHERITED_SOCKET_FDS — the v1
  finding also exposed an inherited socket descriptor on fd 0);
* no inherited foreign network-namespace FD;
* descendants cannot regain the host network namespace (setns probe).

A bare ``unshare --net`` is NOT sufficient evidence; the gate checks the
escape surfaces mechanically, fail-closed.
"""
from __future__ import annotations

import os
import socket
import stat
from dataclasses import dataclass, field

# demonstrated frozen probe set (data, not behavior)
DEFAULT_DNS_HOSTS = ("api.openai.com", "chatgpt.com", "one.one.one.one")
DEFAULT_TCP_TARGETS = (("1.1.1.1", 443), ("1.1.1.1", 53),
                       ("8.8.8.8", 443), ("api.openai.com", 443))
DEFAULT_MASK_PATHS = ("/run/systemd/resolve", "/run/dbus")


@dataclass
class NoEgressSpec:
    dns_hosts: tuple[str, ...] = DEFAULT_DNS_HOSTS
    tcp_targets: tuple[tuple[str, int], ...] = DEFAULT_TCP_TARGETS
    loopback_required_state: str = "down"     # frozen demonstrated profile
    require_mountns_isolated: bool = True
    mask_paths: tuple[str, ...] = DEFAULT_MASK_PATHS
    tcp_timeout: float = 0.6


@dataclass
class NetFacts:
    """Observed facts (collected inside the gated environment, or injected
    as fixtures by deterministic tests)."""
    netns_inode: str | None = None
    mntns_inode: str | None = None
    parent_mntns_inode: str | None = None
    inherited_socket_fds: list[int] = field(default_factory=list)
    ns_fds: list[int] = field(default_factory=list)
    ifaces: dict[str, dict] = field(default_factory=dict)
    route4_rows: list[str] = field(default_factory=list)
    route6_usable: list[str] = field(default_factory=list)
    lo_state: str | None = None
    dns_results: list[dict] = field(default_factory=list)
    tcp_results: list[dict] = field(default_factory=list)
    mask_results: list[dict] = field(default_factory=list)
    setns_regain: str = "not_probed"


def _readlink(path: str) -> str | None:
    try:
        return os.readlink(path)
    except OSError:
        return None


def collect_net_facts(spec: NoEgressSpec, *,
                      parent_mntns_inode: str | None = None) -> NetFacts:
    """Collect observed network-environment facts from the CURRENT
    (already namespaced) process."""
    facts = NetFacts()
    facts.netns_inode = _readlink("/proc/self/ns/net")
    facts.mntns_inode = _readlink("/proc/self/ns/mnt")
    facts.parent_mntns_inode = parent_mntns_inode

    # 1) inherited descriptors FIRST (before this collector opens anything)
    try:
        fds = sorted(os.listdir("/proc/self/fd"))
    except OSError:
        fds = []
    for fd in fds:
        try:
            n = int(fd)
        except ValueError:
            continue
        try:
            st = os.fstat(n)
        except OSError:
            continue
        if stat.S_ISSOCK(st.st_mode):
            facts.inherited_socket_fds.append(n)
        else:
            tgt = _readlink(f"/proc/self/fd/{n}") or ""
            if "/ns/" in tgt:
                facts.ns_fds.append(n)

    # 2) interfaces / addresses / routes via /proc (no iproute2 needed)
    try:
        with open("/proc/net/dev") as fh:
            lines = fh.read().splitlines()[2:]
        names = [ln.split(":", 1)[0].strip() for ln in lines if ":" in ln]
    except OSError:
        names = []
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        import fcntl
        import struct
        for name in names:
            info: dict = {"up": False, "addr4": [], "addr6": []}
            # a full ifreq: name[16] + sockaddr storage (40 bytes)
            buf = name.encode()[:15].ljust(16, b"\0") + b"\0" * 24
            try:
                res = fcntl.ioctl(s.fileno(), 0x8913, buf)  # SIOCGIFFLAGS
                flags = struct.unpack("16sH2x", res[:20])[1]
                info["up"] = bool(flags & 0x1)  # IFF_UP
            except (OSError, struct.error):
                pass
            try:
                res = fcntl.ioctl(s.fileno(), 0x8915, buf)  # SIOCGIFADDR
                raw = res[20:24]
                info["addr4"] = [socket.inet_ntoa(raw)]
            except (OSError, struct.error, ValueError):
                pass
            facts.ifaces[name] = info
            if name == "lo":
                facts.lo_state = "up" if info["up"] else "down"
    finally:
        if s is not None:
            s.close()
    try:
        with open("/proc/net/route") as fh:
            facts.route4_rows = [ln.strip() for ln in fh.read().splitlines()[1:]
                                 if ln.strip()]
    except OSError:
        facts.route4_rows = ["<unreadable>"]
    try:
        with open("/proc/net/if_inet6") as fh:
            for ln in fh.read().splitlines():
                parts = ln.split()
                if len(parts) >= 6:
                    addr, _, _, _, _, iface = parts[:6]
                    facts.ifaces.setdefault(iface, {"up": False,
                                                    "addr4": [],
                                                    "addr6": []})
                    facts.ifaces[iface]["addr6"].append(addr.lower())
    except OSError:
        pass
    try:
        with open("/proc/net/ipv6_route") as fh:
            for ln in fh.read().splitlines():
                parts = ln.split()
                if len(parts) < 10:
                    continue
                try:
                    dst_bin = bytes.fromhex(parts[0].zfill(32))
                    plen = int(parts[1])
                except ValueError:
                    facts.route6_usable.append(ln.strip())
                    continue
                usable = False
                if any(dst_bin):
                    # ff00::/8 multicast and fe80::/10 link-local stubs are
                    # unconditional in every netns — not usable routes
                    if not (dst_bin[0] == 0xFF and plen <= 8) and \
                       not (dst_bin[0] == 0xFE and (dst_bin[1] & 0xC0) == 0x80
                            and plen <= 10):
                        usable = True
                if usable:
                    facts.route6_usable.append(ln.strip())
    except OSError:
        facts.route6_usable = ["<unreadable>"]

    # 3) masked AF_UNIX host escape surfaces
    for path in spec.mask_paths:
        exists = os.path.lexists(path)
        connectable = False
        if exists and os.path.isdir(path):
            probe = os.path.join(path, "io.systemd.Resolve")
            if os.path.exists(probe):
                connectable = _unix_connectable(probe)
            else:
                probe2 = os.path.join(path, "system_bus_socket")
                if os.path.exists(probe2):
                    connectable = _unix_connectable(probe2)
        elif exists:
            connectable = _unix_connectable(path)
        facts.mask_results.append({"path": path, "exists": exists,
                                   "connectable": connectable})

    # 4) DNS / external TCP reachability — every probe MUST fail here
    import signal
    for host in spec.dns_hosts:
        try:
            old = signal.signal(signal.SIGALRM, _alarm_handler)
            signal.alarm(4)
            try:
                socket.getaddrinfo(host, 443)
                resolved = True
                err = ""
            except Exception as exc:  # noqa: BLE001 — any failure = blocked
                resolved = False
                err = f"{type(exc).__name__}: {exc}"
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old)
        except (ValueError, OSError):
            resolved, err = False, "signal-unsupported"
        facts.dns_results.append({"host": host, "resolved": resolved,
                                  "error": err})
    for host, port in spec.tcp_targets:
        try:
            sock = socket.create_connection((host, port),
                                            timeout=spec.tcp_timeout)
            sock.close()
            connected = True
            err = ""
        except Exception as exc:  # noqa: BLE001 — any failure = blocked
            connected = False
            err = f"{type(exc).__name__}: {exc}"
        facts.tcp_results.append({"host": host, "port": port,
                                  "connected": connected, "error": err})

    # 5) can a descendant regain the host network namespace?
    facts.setns_regain = _probe_setns_regain()
    return facts


def _alarm_handler(signum, frame):  # noqa: ARG001
    raise TimeoutError("dns-probe-timeout")


def _unix_connectable(path: str) -> bool:
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.settimeout(0.5)
            s.connect(path)
            return True
        finally:
            s.close()
    except OSError:
        return False


def _probe_setns_regain() -> str:
    """Attempt, in a forked probe child, to setns into /proc/1/ns/net when
    it is a FOREIGN netns.  Outcomes: denied | no_foreign_pid1 | regained."""
    own = _readlink("/proc/self/ns/net")
    pid1 = _readlink("/proc/1/ns/net")
    if pid1 is None or pid1 == own:
        return "no_foreign_pid1"
    pid = os.fork()
    if pid == 0:
        try:
            fd = os.open("/proc/1/ns/net", os.O_RDONLY)
            try:
                import ctypes
                libc = ctypes.CDLL(None, use_errno=True)
                if libc.setns(fd, 0) != 0:
                    os._exit(3)
                os._exit(0)  # REGAINED — hard failure
            finally:
                os.close(fd)
        except OSError:
            os._exit(2)  # inaccessible -> denied
        except BaseException:
            os._exit(4)
    _, status = os.waitpid(pid, 0)
    code = os.waitstatus_to_exitcode(status)
    if code == 0:
        return "regained"
    if code == 2:
        return "denied-inaccessible"
    return "denied"


@dataclass
class GateResult:
    passed: bool
    failures: list[str] = field(default_factory=list)
    checks: list[dict] = field(default_factory=list)
    facts: NetFacts | None = None


def check_noegress(facts: NetFacts, spec: NoEgressSpec) -> GateResult:
    """Evaluate the no-egress invariant over observed facts.  Fail closed:
    every check must hold."""
    checks: list[dict] = []

    def chk(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    chk("ZERO_INHERITED_SOCKET_FDS",
        len(facts.inherited_socket_fds) == 0,
        f"inherited_socket_fd_count={len(facts.inherited_socket_fds)} "
        f"fds={facts.inherited_socket_fds}")
    chk("NO_INHERITED_NETNS_FD", len(facts.ns_fds) == 0,
        f"ns_fds={facts.ns_fds}")
    chk("FRESH_MOUNT_NAMESPACE",
        (not spec.require_mountns_isolated)
        or (facts.mntns_inode is not None
            and facts.parent_mntns_inode is not None
            and facts.mntns_inode != facts.parent_mntns_inode),
        f"mnt={facts.mntns_inode} parent={facts.parent_mntns_inode}")

    addr4 = [a for info in facts.ifaces.values() for a in info["addr4"]]
    chk("NO_USABLE_IPV4_ADDRESS", len(addr4) == 0, f"addr4={addr4}")
    addr6 = [a for info in facts.ifaces.values() for a in info["addr6"]
             if not a.startswith("fe80")]
    chk("NO_USABLE_IPV6_ADDRESS", len(addr6) == 0, f"addr6={addr6}")
    chk("NO_USABLE_ROUTE",
        len(facts.route4_rows) == 0 and len(facts.route6_usable) == 0,
        f"route4={len(facts.route4_rows)} "
        f"route6_usable={len(facts.route6_usable)}")
    if spec.loopback_required_state == "down":
        chk("LOOPBACK_DOWN",
            facts.lo_state in (None, "down"),
            f"lo_state={facts.lo_state}")
    for r in facts.mask_results:
        chk(f"MASKED:{r['path']}",
            not r["connectable"],
            f"exists={r['exists']} connectable={r['connectable']}")
    for r in facts.dns_results:
        chk(f"DNS_BLOCKED:{r['host']}", not r["resolved"], r["error"])
    for r in facts.tcp_results:
        chk(f"TCP_BLOCKED:{r['host']}:{r['port']}", not r["connected"],
            r["error"])
    chk("DESCENDANTS_CANNOT_REGAIN_HOST_NETNS",
        facts.setns_regain in ("denied", "denied-inaccessible",
                               "no_foreign_pid1"),
        f"setns={facts.setns_regain}")

    failures = [c["name"] for c in checks if not c["ok"]]
    return GateResult(passed=not failures, failures=failures,
                      checks=checks, facts=facts)


def run_noegress_gate(spec: NoEgressSpec, *,
                      parent_mntns_inode: str | None = None) -> GateResult:
    facts = collect_net_facts(spec, parent_mntns_inode=parent_mntns_inode)
    return check_noegress(facts, spec)
