"""GAP-D import-gate synthetic tests: the STATIC-V2 census (positives
on the real pinned modules; negatives on disposable mutated mirrors),
the D4 caller-purity gate, D5 blob pinning, and the GAP-D-BEHAV-V2
fresh-interpreter behavioral gate with bounded OS-level process and
network observation.  strace is ABSENT on this host: the designed
supplementary syscall trace is substituted by an LD_PRELOAD
interposition shim (fork/execve/socket/connect + a SHIM_LOADED marker
whose absence is a monitoring gap -> fail closed), a Python audit-hook
channel, /proc children polling, and unshare -Urn network-namespace
confinement; the glibc-internal posix_spawn path is not
PLT-interceptable and is disclosed as a residual covered by the audit
hook and /proc polling.  Disposable sandboxes and synthetic non-secret
bytes only."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

LC_ROOT = Path(__file__).resolve().parents[1]
if str(LC_ROOT) not in sys.path:
    sys.path.insert(0, str(LC_ROOT))
sys.dont_write_bytecode = True   # never leave bytecode in the frozen tree
import lifecycle_caller as lc  # noqa: E402

REPO_ROOT = LC_ROOT.parent
PKG_DIR = REPO_ROOT / "bootstrap-authority"
PKG_SUB = PKG_DIR / "bootstrap_authority"

# ------------------------------------------------- STATIC-V2 census

def test_census_accepts_real_pinned_modules():
    result = lc.static_census(PKG_DIR)
    assert result == {"pinned_sites": 42, "modules": 8}


def mirror(tmp_path, module, appendix):
    """Disposable mutated mirror of the real package (one module's
    source changed); for refusal testing only."""
    target = tmp_path / "mirror" / "bootstrap_authority"
    target.mkdir(parents=True)
    for name in os.listdir(PKG_SUB):
        if not (PKG_SUB / name).is_file():
            continue
        data = (PKG_SUB / name).read_bytes()
        if name == module:
            data = data + appendix.encode()
        (target / name).write_bytes(data)
    return tmp_path / "mirror"


# every appendix below is STATIC SOURCE TEXT appended to a disposable
# mirror and parsed by the data-only census; none of it is ever
# executed (the eval()/__import__/getattr strings exist precisely to
# prove the census refuses these import-time forms)
@pytest.mark.parametrize("module,appendix", [
    ("runtime.py", "\nimport os\nRESULT = os.getcwd()\n"),          # D2a
    ("runtime.py", "\nopen('/tmp/gate-d2a', 'w')\n"),               # D2a
    ("runtime.py", "\nimport subprocess\nP = subprocess.run\n"),    # attr ref
    ("runtime.py", "\nX = eval('1')\n"),                            # D2a
    ("runtime.py", "\nX = getattr(PKG, 'name')\n"),                 # dispatch
    ("runtime.py", "\nX = unknown_callee()\n"),                     # D2a
    ("runtime.py", "\ndef load():\n    return {}\nX = dict(load())\n"),   # D2c
    ("runtime.py", "\nX = __import__('os').getcwd()\n"),            # dynamic
    ("binding.py", "\nimport re\nDYN = re.compile(PATTERN)\n"),     # D2c
    ("binding.py", "\nimport os\nL = frozenset(os.listdir('/'))\n"),      # D2c
    ("binding.py", "\nX = __import__('ctypes').CDLN = 1\n"),
    ("statemachine.py", "\nEXTRA = frozenset((1, 2))\n"),           # D2b
    ("statemachine.py", "\nNEWSTATE = 'x'\nSTATES = frozenset({NEWSTATE, 'y'})\n"),
    ("runtime.py", "\nif True:\n    X = frozenset((1,))\n"),        # D2d
    ("runtime.py", "\nwith open('/dev/null') as H:\n    pass\n"),   # D2d
    ("runtime.py", "\ntry:\n    X = 1\nexcept OSError:\n    pass\n"),      # D2d
    ("custody.py", "\nUNBOUND['k'] = {}\n"),                       # unbound
    ("custody.py", "\nD = {}\nD.items()\n"),                       # PF-2 pos
    ("custody.py", "\nimport ctypes\nLIB = ctypes.CDLL(None)\n"),  # ctypes
    ("accounting.py", "\ndef f(x=os.getcwd()):\n    return x\n"),  # default
    ("accounting.py", "\nX = 1 << 2\n"),                           # operator
    ("__init__.py", "\n@cache\ndef cached():\n    return 1\n"),    # PF-5
    ("__init__.py", "\nfrom dataclasses import dataclass\n"
                    "@dataclass(frozen=False)\nclass Loose:\n    a: int\n"),
])
def test_census_refuses_mutated_mirrors(tmp_path, module, appendix):
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.static_census(mirror(tmp_path, module, appendix))
    assert ei.value.code == lc.IMPORT_TIME_STATIC_REFUSED


def test_census_refuses_minus_one_pinned_site(monkeypatch, tmp_path):
    pruned = set(lc.PINNED_IMPORT_SITES)
    pruned.discard(sorted(pruned)[0])
    monkeypatch.setattr(lc, "PINNED_IMPORT_SITES", frozenset(pruned))
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.static_census(mirror(tmp_path, "runtime.py", ""))
    assert ei.value.code == lc.IMPORT_TIME_STATIC_REFUSED


def test_census_refuses_class_base_and_import_position(tmp_path):
    with pytest.raises(lc.LifecycleCallerError):
        lc.static_census(mirror(tmp_path / "a", "runtime.py",
                                "\nimport os\nclass Derived("
                                "os.getcwd().__class__):\n    pass\n"))
    with pytest.raises(lc.LifecycleCallerError):
        lc.static_census(mirror(tmp_path / "b", "binding.py",
                                "\nfrom dataclasses import dataclass\n"
                                "D = dataclass(frozen=True)\n"))


def test_census_refuses_network_import_time_use(tmp_path):
    # an import STATEMENT alone is the disclosed surface; module-level
    # socket USE is refused by the call census (D2a form)
    with pytest.raises(lc.LifecycleCallerError):
        lc.static_census(mirror(tmp_path, "runtime.py",
                                "\nimport socket\nS = socket.socket()\n"))


# ------------------------------------------------- D4 caller purity

def test_caller_purity_real_source_passes():
    lc.check_caller_purity(Path(lc.__file__).read_bytes())


@pytest.mark.parametrize("mutation", [
    b"import bootstrap_authority.runtime\n",
    b"from bootstrap_authority.runtime import thing\n",
    b"X = BootstrapAuthority()\n",
    b"Y = run_attempt()\n",
    b"Z = accounting.create()\n",
    b"W = obj.custody\n",
    b"V = statemachine.states\n",
])
def test_caller_purity_refuses_runtime_surface(mutation):
    source = Path(lc.__file__).read_bytes() + b"\n" + mutation
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.check_caller_purity(source)
    assert ei.value.code == lc.CALLER_SOURCE_REFUSED


# ------------------------------------------------- D5 blob pinning

def _world_with_package(tmp_path):
    repo = tmp_path / "world"
    repo.mkdir()
    subprocess.run(("git", "-C", str(repo), "init", "-q", "-b", "master"),
                   capture_output=True, check=True)
    for path in PKG_DIR.rglob("*"):
        if path.is_file():
            rel = path.relative_to(PKG_DIR)
            (repo / "bootstrap-authority" / rel).parent.mkdir(
                parents=True, exist_ok=True)
            (repo / "bootstrap-authority" / rel).write_bytes(path.read_bytes())
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    subprocess.run(("git", "-C", str(repo), "add", "-A"),
                   capture_output=True, check=True)
    subprocess.run(("git", "-C", str(repo), "commit", "-q", "-m", "pkg"),
                   capture_output=True, check=True, env=env)
    tip = subprocess.run(("git", "-C", str(repo), "rev-parse", "HEAD"),
                         capture_output=True, check=True)
    return repo, tip.stdout.decode().strip()


def test_import_gate_happy_path(tmp_path):
    repo, tip = _world_with_package(tmp_path)
    gate = lc.verify_import_gate(repo, tip, repo / "bootstrap-authority")
    assert gate["package_identity"]["pinned_blobs"] == 9
    assert gate["static_census"] == {"pinned_sites": 42, "modules": 8}
    module = lc.import_verified_package(repo, tip,
                                        repo / "bootstrap-authority")
    assert hasattr(module, "G6_IDENTITY_FIELDS")


def test_d5_blob_pin_mismatch_refuses_before_import(tmp_path):
    repo, tip = _world_with_package(tmp_path)
    victim = repo / "bootstrap-authority" / "bootstrap_authority" \
        / "statemachine.py"
    victim.write_bytes(victim.read_bytes() + b"\n# drift\n")
    with pytest.raises(lc.LifecycleCallerError) as ei:
        lc.verify_import_gate(repo, tip, repo / "bootstrap-authority")
    assert ei.value.code == lc.SOURCE_BLOB_PIN_MISMATCH


# ------------------------------------------- GAP-D-BEHAV-V2 gate
# strace is absent on this host; the supplementary syscall trace is
# substituted by PLT interposition (fork/execve/socket/connect) plus a
# constructor SHIM_LOADED marker (absence == monitoring gap == fail
# closed), an in-child audit hook, /proc children polling and unshare
# network-namespace confinement.  posix_spawn via a glibc-internal
# path is not PLT-interceptable (disclosed residual; the audit hook
# and /proc polling cover Python-level spawning).
SHIM_C = r"""
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
static void log_ev(const char *kind, const char *arg){
    const char *path = getenv("OBS_LOG");
    if(!path) return;
    FILE *f = fopen(path, "a");
    if(f){ fprintf(f, "%s %s\n", kind, arg ? arg : "-"); fclose(f); }
}
__attribute__((constructor)) static void shim_init(void){
    log_ev("SHIM_LOADED", "");
}
int execve(const char *p, char *const av[], char *const ev[]){
    static int (*real)(const char *, char *const[], char *const []);
    log_ev("EXECVE", p);
    if(!real) real = (int (*)(const char *, char *const[],
            char *const []))dlsym(RTLD_NEXT, "execve");
    return real(p, av, ev);
}
pid_t fork(void){
    static pid_t (*real)(void);
    log_ev("FORK", "");
    if(!real) real = (pid_t (*)(void))dlsym(RTLD_NEXT, "fork");
    return real();
}
int socket(int d, int t, int p){
    static int (*real)(int, int, int);
    log_ev("SOCKET", "");
    if(!real) real = (int (*)(int, int, int))dlsym(RTLD_NEXT, "socket");
    return real(d, t, p);
}
int connect(int fd, const struct sockaddr *a, socklen_t l){
    static int (*real)(int, const struct sockaddr *, socklen_t);
    log_ev("CONNECT", "");
    if(!real) real = (int (*)(int, const struct sockaddr *,
            socklen_t))dlsym(RTLD_NEXT, "connect");
    return real(fd, a, l);
}
"""

CHILD = r"""
import gc, hashlib, json, os, sys
events = []
WATCH = ("subprocess.Popen", "os.exec", "os.posix_spawn", "os.fork",
         "socket.socket", "socket.connect")
def hook(name, args):
    if name.startswith(WATCH):
        events.append(name)
sys.addaudithook(hook)
pkg = os.environ["GATE_PKG_DIR"]
if os.environ.get("GATE_NO_IMPORT") != "1":
    for rel, want in json.loads(os.environ["GATE_EXPECTED"]).items():
        data = open(os.path.join(pkg, rel), "rb").read()
        got = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        assert got == want, rel
sys.path.insert(0, pkg)
if os.environ.get("GATE_NO_IMPORT") != "1":
    import bootstrap_authority.receiptidentity
loaded = sorted(m for m in sys.modules if m == "bootstrap_authority"
                or m.startswith("bootstrap_authority."))
result = {
    "loaded": loaded,
    "network_modules": [m for m in ("socket", "urllib.request",
                                    "http.client", "requests")
                        if m in sys.modules],
    "instances": sorted({type(o).__module__ + "." + type(o).__name__
                         for o in gc.get_objects()
                         if type(o).__module__.startswith(
                             "bootstrap_authority.")}),
    "audit_events": sorted(set(events)),
    "runtime_loaded": "bootstrap_authority.runtime" in sys.modules}
sys.stdout.write("BEHAV_RESULT " + json.dumps(result) + "\n")
"""


def _compile_shim(tmp_path):
    shim_c = tmp_path / "shim.c"
    shim_c.write_text(SHIM_C)
    shim_so = tmp_path / "shim.so"
    out = subprocess.run(("gcc", "-shared", "-fPIC", "-O2", "-o",
                          str(shim_so), str(shim_c)), capture_output=True)
    if out.returncode != 0:
        pytest.fail("MONITORING OBSERVABILITY UNAVAILABLE (fail closed): "
                    + out.stderr.decode()[:200])
    return shim_so


def _snapshot(root):
    state = {}
    for path in sorted(Path(root).rglob("*")):
        st = path.lstat()
        entry = [str(path), st.st_mode, st.st_size, st.st_mtime_ns]
        if path.is_file() and st.st_size < 1 << 20:
            import hashlib
            entry.append(hashlib.sha256(path.read_bytes()).hexdigest())
        state[str(path)] = entry
    return state


def _tip_pins(repo=None):
    repo = repo or REPO_ROOT
    tip = subprocess.run(("git", "-C", str(repo), "rev-parse", "HEAD"),
                         capture_output=True, check=True).stdout.decode()
    pins = {}
    for rel in ["MANIFEST.json"] + [f"bootstrap_authority/{m}" for m in
                                    lc.PRODUCTION_MODULES]:
        want = subprocess.run(("git", "-C", str(repo), "rev-parse",
                               f"{tip.strip()}:{'bootstrap-authority/' + rel}"),
                              capture_output=True, check=True)
        pins[rel] = want.stdout.decode().strip()
    return pins


def _run_child(tmp_path, shim_so, pkg_dir, pins, *, no_import=False,
               extra_env=None):
    sandbox = tmp_path / "sandbox"
    home = sandbox / "home"
    tmp = sandbox / "tmp"
    home.mkdir(parents=True)
    tmp.mkdir()
    obs_log = tmp_path / "obs.log"
    obs_log.write_bytes(b"")
    child = sandbox / "child.py"
    child.write_text(CHILD)
    repo_status = subprocess.run(
        ("git", "-C", str(REPO_ROOT), "status", "--porcelain"),
        capture_output=True, check=True).stdout
    before = (_snapshot(sandbox), _snapshot(pkg_dir))
    env = {"PATH": os.environ["PATH"], "HOME": str(home),
           "TMPDIR": str(tmp), "PYTHONPATH": str(pkg_dir),
           "PYTHONDONTWRITEBYTECODE": "1", "LD_PRELOAD": str(shim_so),
           "OBS_LOG": str(obs_log), "GATE_PKG_DIR": str(pkg_dir),
           "GATE_EXPECTED": json.dumps(pins)}
    if no_import:
        env["GATE_NO_IMPORT"] = "1"
    if extra_env:
        env.update(extra_env)
    proc = subprocess.Popen(("unshare", "-Urn", sys.executable, "-B",
                             str(child)), cwd=sandbox, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    children_seen = []
    while proc.poll() is None:
        task_dir = Path(f"/proc/{proc.pid}/task")
        if task_dir.is_dir():
            for task in task_dir.iterdir():
                try:
                    seen = (task / "children").read_text().split()
                except OSError:
                    continue
                children_seen.extend(seen)
        time.sleep(0.002)
    stdout = proc.stdout.read().decode()
    stderr = proc.stderr.read().decode()
    after = (_snapshot(sandbox), _snapshot(pkg_dir))
    repo_status_after = subprocess.run(
        ("git", "-C", str(REPO_ROOT), "status", "--porcelain"),
        capture_output=True, check=True).stdout
    log_lines = obs_log.read_text().splitlines()
    return {"rc": proc.returncode, "stdout": stdout, "stderr": stderr,
            "log": log_lines, "children": sorted(set(children_seen)),
            "sandbox_equal": before[0] == after[0],
            "package_equal": before[1] == after[1],
            "repo_equal": repo_status == repo_status_after,
            "sandbox": sandbox}


def _require_confinement():
    probe = subprocess.run(("unshare", "-Urn", "true"), capture_output=True)
    if probe.returncode != 0:
        pytest.fail("INCOMPLETE VALIDATION (fail closed): the mandatory "
                    "network-namespace confinement is unavailable: "
                    + probe.stderr.decode()[:120])


EXPECTED_MODULES = ["bootstrap_authority",
                    "bootstrap_authority.accounting",
                    "bootstrap_authority.binding",
                    "bootstrap_authority.custody",
                    "bootstrap_authority.receiptidentity",
                    "bootstrap_authority.reportcustody",
                    "bootstrap_authority.runtime",
                    "bootstrap_authority.statemachine"]


def test_behav_d1_d3_real_package_pass_with_observation(tmp_path):
    _require_confinement()
    shim = _compile_shim(tmp_path)
    pins = _tip_pins()
    control = _run_child(tmp_path / "ctl", shim, PKG_DIR, pins,
                         no_import=True)
    subject = _run_child(tmp_path / "sub", shim, PKG_DIR, pins)
    assert subject["rc"] == 0, subject["stderr"][:400]
    result = json.loads([line for line in subject["stdout"].splitlines()
                         if line.startswith("BEHAV_RESULT ")][0][13:])
    assert result["runtime_loaded"] is True            # D12 disclosure
    assert result["loaded"] == EXPECTED_MODULES        # D1 transitive load
    assert result["network_modules"] == []             # negative space
    assert result["instances"] == []                   # no authority object
    assert result["audit_events"] == []                # no os-level effects
    assert subject["sandbox_equal"] and subject["package_equal"]
    assert subject["repo_equal"]
    assert subject["children"] == []
    # the constructor marker fires once per loader pass (unshare itself
    # and the exec'd python); ONLY marker lines may appear, and the
    # subject must equal the no-import control baseline exactly
    kinds = lambda log: sorted(line.split()[0] for line in log)
    assert set(kinds(subject["log"])) == {"SHIM_LOADED"}
    assert kinds(subject["log"]) == kinds(control["log"])
    assert control["sandbox_equal"] and control["repo_equal"]


def test_behav_monitoring_gap_fails_closed(tmp_path):
    _require_confinement()
    pins = _tip_pins()
    run = _run_child(tmp_path, tmp_path / "absent-shim.so", PKG_DIR, pins)
    kinds = [line.split()[0] for line in run["log"]]
    # the marker is ABSENT: a monitoring gap that must fail closed
    assert "SHIM_LOADED" not in kinds


def _behavioral_mirror(tmp_path, module, appendix):
    mirror_root = tmp_path / "mpkg"
    sub = mirror_root / "bootstrap_authority"
    sub.mkdir(parents=True)
    for name in os.listdir(PKG_SUB):
        data = (PKG_SUB / name).read_bytes()
        if name == module:
            data += appendix.encode()
        (sub / name).write_bytes(data)
    import hashlib as _h
    pins = {}
    for name in os.listdir(sub):
        if not (sub / name).is_file():
            continue
        data = (sub / name).read_bytes()
        pins[f"bootstrap_authority/{name}"] = _h.sha1(
            b"blob %d\0" % len(data) + data).hexdigest()
    return mirror_root, pins


def test_behav_d8_network_module_refused(tmp_path):
    _require_confinement()
    shim = _compile_shim(tmp_path)
    root, pins = _behavioral_mirror(tmp_path, "reportcustody.py",
                                    "\nimport socket\n")
    run = _run_child(tmp_path, shim, root, pins)
    assert run["rc"] == 0
    result = json.loads([line for line in run["stdout"].splitlines()
                         if line.startswith("BEHAV_RESULT ")][0][13:])
    assert "socket" in result["network_modules"]   # negative-space refusal


def test_behav_d9_instance_construction_refused(tmp_path):
    _require_confinement()
    shim = _compile_shim(tmp_path)
    root, pins = _behavioral_mirror(tmp_path, "reportcustody.py",
                                    "\nclass _M:\n    pass\n"
                                    "M_INSTANCE = _M()\n")
    run = _run_child(tmp_path, shim, root, pins)
    assert run["rc"] == 0
    result = json.loads([line for line in run["stdout"].splitlines()
                         if line.startswith("BEHAV_RESULT ")][0][13:])
    assert result["instances"]


def test_behav_d10_filesystem_write_refused(tmp_path):
    _require_confinement()
    shim = _compile_shim(tmp_path)
    root, pins = _behavioral_mirror(tmp_path, "reportcustody.py",
                                    '\nopen("side-effect.txt", "w")'
                                    '.write("x")\n')
    run = _run_child(tmp_path, shim, root, pins)
    assert run["rc"] == 0
    assert not run["sandbox_equal"]          # snapshot mismatch refusal


def test_behav_d7_bytecode_disabled(tmp_path):
    _require_confinement()
    shim = _compile_shim(tmp_path)
    run = _run_child(tmp_path, shim, PKG_DIR, _tip_pins())
    pycache = [p for p in run["sandbox"].rglob("*") if "__pycache__" in
               p.parts or p.suffix == ".pyc"]
    assert run["package_equal"] and not pycache
