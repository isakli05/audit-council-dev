# A0 — Codex Confinement Spike (docs/A0-CODEX-CONFINEMENT.md)

Date: 2026-09-04. Method: current Codex CLI documentation (primary) +
deterministic local probes (no model inference was invoked for any probe;
`codex login status` is a local auth check the v1 preflight already runs).
Environment: codex-cli 0.153.0 (ChatGPT subscription login), git 2.55.0,
Linux 6.x/7.2.2-cachyos (Landlock kernel symbols + `linux/landlock.h`
present), bubblewrap 0.12.0 at `/usr/sbin/bwrap`, node via nvm v24.14.0.

## 1. Established facts

| Fact | Evidence |
|---|---|
| Fresh sandbox argv: `codex exec -C <repo> --model gpt-5.6-sol --sandbox read-only --json --output-schema <s> -c model_reasoning_effort="xhigh" -o <out> -` | `codex exec --help` (v2 runner argv unchanged) |
| Resume has NO `-s`; sandbox via `-c sandbox_mode="read-only"` (D1 stands) | `codex exec resume --help` |
| `--sandbox read-only` policy selects the sandbox "for model-generated shell commands" | docs (developer-commands reference) |
| Docs frame the modes in WRITE terms only (`read-only` / `workspace-write` / `danger-full-access`, `--add-dir` grants extra WRITE dirs); Linux read-root options DO NOT EXIST (a read-dir flag exists only on Windows) | docs, primary |
| **Codex's sandbox does NOT confine reads to `-C <repo>`**: under `codex sandbox` (the same Linux Landlock+seccomp sandbox, no model involved) `cat /etc/passwd` and `cat /tmp/<user-secret>` both SUCCEED | local probe, deterministic |
| Writes ARE OS-prevented by codex's sandbox: `sh -c 'echo x > /tmp/f'` fails ("read-only file system"), file not created | local probe |
| A Codex-provided `codex sandbox` subcommand exists and runs arbitrary commands under Landlock+seccomp — used here for probing | `codex sandbox --help` |
| bubblewrap 0.12.0 is installed and functional (user namespaces) | probes below |

## 2. The bubblewrap boundary (probe matrix, all deterministic)

Bind set: `--ro-bind /usr /usr` (+/lib,/lib64), `--ro-bind /etc /etc`,
`--bind ~/.codex ~/.codex` (codex writes session/auth state there on the
host too), `--ro-bind <nvm-version-root>` (toolchain; resolved from the
real `codex` path), `--tmpfs /tmp`, then `--ro-bind <repo> <repo>`,
`--bind <run_dir> <run_dir>`, `--dev /dev --proc /proc`, `HOME`/`PATH`
setenv (toolchain bin FIRST — a broken `/usr/bin/node` shadowed nvm's
when `/usr/bin` led). Network is deliberately NOT unshared (subscription
API must be reachable).

Results (reproduced multiple times):

| Probe | Result |
|---|---|
| read repo file inside | OK |
| read `~/audit-council-dev/CONTRACTS.md` (other user data) | **BLOCKED** |
| read `~/.zcode/…`, `~/.ssh/config` (user data) | **BLOCKED** |
| read `/etc/passwd`, `/usr/*` (system) | visible — documented boundary |
| `codex --version` inside | codex-cli 0.153.0 |
| `codex login status` inside (auth + network preserved) | Logged in using ChatGPT |
| write into run dir (codex `-o` output, logs) | OK |
| write into repo source | **BLOCKED** (read-only bind) |
| `/tmp` | fresh tmpfs; authorized fixture roots bind individually |

## 3. Enforcement classification (per the operator's taxonomy)

| Property | WITHOUT wrapper (v2 as of 081b039) | WITH `codex_sandbox.py` wrapper (this change) |
|---|---|---|
| Prevent codex process writes to audited repo | OS-enforced (codex Landlock sandbox) | **OS-enforced (bwrap ro-bind; independent of codex's own sandbox)** |
| Prevent model-command writes to repo | OS-enforced (codex sandbox) | OS-enforced (both layers) |
| Prevent reads outside `-C` repo (user data: other repos, ~/.ssh, dev trees, other runs) | **NOT ENFORCED** (runner validates argv/output only = runner policy/detection) | **OS-enforced EXCEPT the documented bind set** (system dirs /etc,/usr,/lib, `~/.codex`, the resolved toolchain root, run dir, explicitly authorized fixture roots) |
| Subscription auth | unchanged | unchanged (rw `~/.codex`, network on) |
| Executable/toolchain + libs | unchanged | unchanged (toolchain root + /usr ro) |
| Run-artifact output (`-o`, logs) | unchanged | unchanged (run dir rw-bound at its real path) |
| Explicit-session resume | unchanged | unchanged (same wrapper on resume argv; `~/.codex` sessions writable) |
| Read isolation of OTHER `/tmp` content | not enforced | **OS-enforced** (tmpfs; authorized fixture roots bound individually) |

Statement discipline: repo-root READ confinement is claimed ONLY as
"OS-enforced exclusion of everything outside the enumerated bind set
(plus system directories)". `/etc` and `/usr` remain readable inside —
that is inherent (SSL CA roots, resolv.conf, the toolchain) and is
recorded, not hidden. A model command CAN still read system files and
`~/.codex` (its own auth) inside the wrapper — identical to what the
codex process itself can read on the host.

## 4. Deployment decision

IMPLEMENTED (see `skill/scripts/codex_sandbox.py` + wiring in
`codex_runner.launch`): the wrapper is applied automatically to every
codex launch (fresh AND resume) when bwrap is present and
`AC_CODEX_BWRAP != "0"`. Opt-out env `AC_CODEX_BWRAP=0` exists for
environments without user namespaces; in that case the honest posture is
the WITHOUT-wrapper column above (runner policy/detection only) and the
run record states so. Regressions: `tests/test_codex_sandbox.py` builds a
fake toolchain + fake codex under a real bwrap invocation and proves:
outside-root read BLOCKED, repo read OK, run-dir write OK, repo write
BLOCKED, wrapper argv shape for fresh + resume, and clean opt-out.

## 5. Landlock alternative (not implemented)

Landlock (kernel + headers present) could enforce similar read/write
scoping without bwrap, but requires a native launcher (syscall ABI via
C/Rust; Python has no stdlib binding). bwrap delivers the same boundary
today with a maintained tool; a native Landlock launcher remains an
optional future hardening (smaller attack surface than a setuid-free
bubblewrap, at the cost of custom code we would own).

## 6. Reproducing the probes

All probes are deterministic shell one-liners; the canonical matrix lives
as regressions in `skill/tests/test_codex_sandbox.py`, and the raw probe
commands are preserved in this document's history (session log). No real
model inference was used anywhere in this spike.
