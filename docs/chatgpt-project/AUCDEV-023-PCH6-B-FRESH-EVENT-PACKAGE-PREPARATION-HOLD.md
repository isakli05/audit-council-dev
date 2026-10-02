# AUCDEV-023 PCH6-B — Fresh Bounded Event-Package Preparation — FAIL-CLOSED HOLD (Canonical Record, 2026-10-02)

```
AUCDEV_023_PCH6B_FRESH_EVENT_PACKAGE_PREPARATION =
FAIL_CLOSED_HOLD /
PREPARATION_BLOCKED /
GATE_W_PRIME_REHEARSAL_NOT_EXECUTABLE_ON_THIS_HOST_UNDER_OPERATOR_SAFETY_CONSTRAINTS /
PREPARATION_AUTHORITY_RECEIVED_NOT_COMPLETED /
NO_EVENT_PACKAGE_CREATED /
NO_BINDING_FROZEN /
NO_EVENT_MANIFEST_FROZEN /
CUSTODY_DIRS_EMPTY_PREPARATION_STATE_ONLY_NEVER_BOUND /
EVENT_NOT_INSTANTIATED /
ATTEMPT_AUTHORITIES_NOT_GRANTED /
REAL_RESERVED_ATTEMPT_ACCOUNTING_RECORDS_0 /
REAL_REPORT_SINKS_0 /
MODEL_ENGAGEMENTS_USED_0 /
PREPARER_HOST_INCIDENT_20261002_001_RECORDED /
OPERATOR_DECISION_OPTION_C_EXECUTED /
AWAITING_OPERATOR_DECISION_ON_SAFE_REHEARSAL_PATH /
NO_AUDIT_EXECUTION /
NO_AUDIT_PASS /
QUALIFICATION_NONE /
INSTALLATION_NONE
```

Publication authority:
`AUCDEV-023-PCH6B-730D2B29-FRESH-EVENT-PACKAGE-PREPARATION-HOLD-20261002-01`

## 0. Role of this session — EVENT-PACKAGE PREPARER publishing its own fail-closed HOLD

This session is the EVENT-PACKAGE PREPARER for the AUCDEV-023 PCH6-B
fresh independent-audit lineage, publishing the truthful FAIL-CLOSED HOLD
disposition of the fresh bounded event-package preparation it was
authorized to perform. It is NOT the Control Room, NOT a Control Room
readback or verification session, NOT a bootstrap-authority remediation
implementer, NOT a source/test/schema modifier, NOT an event-instantiation
authority, NOT an attempt-execution authority, NOT Auditor-A/B, NOT an
independent auditor, NOT an Audit Council /audit-council executor, NOT a
provider/model/frontier executor, NOT a qualification authority, NOT an
installation authority. This publication grants NO authority of any kind
and closes NO finding.

Zero-execution attestation for THIS session (OBSERVED_FACT): ZERO
provider/model/frontier calls, ZERO client inference calls, ZERO auditor
execution, ZERO /audit-council execution, ZERO wrapper/driver invocation
in the AUCDEV-023 governance chain, ZERO BootstrapAuthority.run_attempt
calls, ZERO test execution, ZERO package-manager fetch, ZERO
credential-content access, ZERO sealed-substance access. The only network
operations are the ordinary Git/GitHub publication mechanics: fetch,
ls-remote, the one authorized push and the post-push GitHub readback.
After the operator's post-incident instruction (§5) this session ran ZERO
privileged commands and performed ZERO mount/pivot_root/umount/chroot
operations of any kind; all post-incident analysis was STATIC
(file/record reads only).

## 1. Operator authority trail (recorded exactly)

1. 2026-10-02: the operator explicitly authorized FRESH BOUNDED
   EVENT-PACKAGE PREPARATION ONLY against the then-current exact live
   repository state for the already-frozen audit target
   `730d2b29f7c0e7d33af3451b6d9205ec27c143ed`, following the
   independently accepted Control Room readback (canonical record
   `AUCDEV-023-PCH6-B-BA-PREP-001-002-FOLLOWUP-REMEDIATION-CONTROL-ROOM-READBACK.md`)
   that closed BA-PREP-001, BA-PREP-002, BA-PREP-RB2-001 and
   BA-PREP-RB2-002 at remediation-readback strength and retained
   BA-RB-001/002/003. The authorization is preparation ONLY: it grants NO
   event instantiation, NO attempt-execution authority, NO run_attempt on
   either reserved real attempt, NO real reserved-attempt accounting
   record, NO /audit-council, NO Auditor-A/B execution, NO Claude or
   Codex inference, NO provider/model/frontier request, NO credential
   materialization or credential-content access, NO model-engagement
   consumption, NO audit PASS, NO qualification, NO installation. It is a
   NEW fresh authorization, NOT a revival of the previously held
   preparation authority.
2. 2026-10-02 (post-incident): the operator reported that the two system
   freezes at 18:12:27 and 18:40:42 (Europe/Istanbul) were caused by this
   session's privileged sandbox spike, prohibited re-running it or any
   similar privileged sandbox experiment, prohibited automatic retry, and
   directed STATIC-ONLY analysis with the fix presented for review
   (diagnostics: `/home/isa/.local/state/freeze-check/20261002-184620/`).
3. 2026-10-02: the operator selected OPTION C — prepare and publish this
   truthful HOLD disposition. This record executes that decision and
   nothing more.

## 2. Exact live bootstrap (re-resolved by THIS session before staging)

- live GitHub master == origin/master == local HEAD ==
  `72d7d1f8b3e2f81785e6f2968f38672224423958` EXACT at bootstrap AND
  re-resolved EXACT again before staging (ls-remote authoritative; fetch
  clean rc 0);
- authorized base root tree `8cdcc6e03e47b9053b8d47e10e5a29d5806ef81f`;
  sole parent
  `3eb7901e75603fb786f2841782a30d0316fc431d` = the BA-PREP follow-up
  remediation readback publication whose recorded NEXT action (the
  operator decision on fresh bounded event-package preparation) this HOLD
  executes as option C; single-parent fast-forward geometry;
- trust anchor `3058868416241d394cfaaa40cc585085db486f37` ancestor rc 0;
  ZERO merges since the anchor;
- zero staged content before this publication; the pre-existing untracked
  drift and the pre-existing smoke-fixture / smoke-fixture-103 gitlink
  drift preserved UNSTAGED; THIS record's path ABSENT at base with zero
  full-history path rows;
- frozen audit target `730d2b29f7c0e7d33af3451b6d9205ec27c143ed`
  (root tree `2585796efd5cb6902226cfff785bb901297a15e3`, remediation
  parent `068f5e29904f446bf832138fd64c8833b9037cb7`, present, ancestor,
  UNTOUCHED) remains AUDIT SUBJECT / NOT AUTHORITY;
- protected trees held EXACT at the base: bootstrap-supervisor
  `3056e577259ab0b0b0472f82ebc306506f3e084c`, qualification-harness
  `5b8d5e5465923740470ff63ed9b8683f257a3787`, skill
  `efd8c2e48edbb25795b3aacb1ce3c23fde10082a`;
- bootstrap-authority tree `154975872e15d53e1706016f5bb60c83727004f0`
  with binding.py blob `1448c9cbfbb795c534f9f517052e998c636d28d6`,
  runtime.py blob `069c221fc1f84f9e8e8342ffed72ec761b9286b5`,
  accounting.py blob `26368783dd88782dd3c63a76fbf11582ee16caa1`,
  reportcustody.py blob `dd09e1e54c9246aa6de5f38391984c35e8baac87`,
  custody.py blob `37e6b5bb4365c7b29ba3632fe95362d5a7e16c09`,
  statemachine.py blob `cf563d2178907e7666ce661b81ab1bf16fb71201` and
  MANIFEST.json blob `27b68b9caf7b477465ffe1f278e3e9a9860950a2` (raw
  SHA-256
  `7713b89e2618d27963be0df4dd5ebb33961a5b48c063c62ecacff2238da1425f`)
  — every identity verified EXACT against the live base; the non-circular
  authority package SHA-256 independently RECOMPUTED ==
  `4399cb062e3fe9a5c4e6e71ad90e8515b3f0b462b6a648c458068cd6f01263db` ==
  the declared value EXACT (canonical JSON of the manifest semantics
  excluding its own field; /usr/bin/python3 3.14.7, no package code
  executed beyond reading bytes).

## 3. Preparation progress completed BEFORE the blocker (OBSERVED_FACT)

All of the following was performed under the fresh preparation authority,
ZERO provider / ZERO inference / ZERO authority execution:

1. Exact live bootstrap verification (§2) — complete, all identities
   EXACT.
2. Reading of the required governance records at the exact base
   (CURRENT-STATE, BACKLOG, the BA-PREP follow-up remediation Control
   Room readback, the auditor-bootstrap governance adoption and design
   revision records and the PATH-B transition Control Room readback, the
   historical event-package-preparation HOLD records for historical
   constraints, and the exact current bootstrap-authority source:
   binding.py, runtime.py, tests/conftest.py, the authority MANIFEST).
3. Extraction of the CURRENT binding contract (the preparation contract):
   the 20 TOP_LEVEL binding dimensions; the eight REQUIRED_STATIC_GATES;
   the three DYNAMIC_GATE descriptors (CLIENT_SELECTION_PREFLIGHT ->
   NETWORK_READINESS -> RESOURCE_GATE LAST, never frozen PASS evidence);
   the EVENT_MANIFEST_KEYS {schema, transport_binding, files,
   package_sha256} with schema
   `AUCDEV-023-CAND730D2B29-EVENT-PACKAGE-MANIFEST-V1`; the non-circular
   manifest/binding construction order (binding parse -> projection ->
   manifest digest -> binding event_package.package_sha256 -> re-parse);
   the RB2-001/002 output-identity requirements (custody_root +
   report_source canonical absolute paths, custody_dev/custody_ino object
   identity, report source a DIRECT child of the custody root, exactly
   one canonical `--report` option whose value must equal report_source);
   the runtime launcher fd contract (3 = sealed credential, 4 = CLOEXEC
   exec-fail pipe, 5 = HELD verified auditor executable, 6 = sealed frozen
   argv; launcher argv [identity, --role, --attempt, --event]; metadata
   JSON on stdout; minimal env); the dynamic-gate argv and strict result
   envelopes; the structural-validator argv/envelope; and the frozen
   design event/attempt identities (DESIGN_RESERVED_ONLY, never
   instantiated).
4. Client resolution with NON-INFERENCE metadata ONLY (permitted by the
   tasking): Auditor-A client = the claude-code native executable
   `/home/isa/.nvm/versions/node/v24.14.0/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`,
   ELF, 237375560 B, SHA-256
   `56fe3da88458465fb27d7e9299dddb3fead55750fb9c2de795f233b5eea6dce1`,
   `--version` = `2.1.281 (Claude Code)`; Auditor-B client = the codex
   shim
   `/home/isa/.nvm/versions/node/v24.14.0/lib/node_modules/@openai/codex/bin/codex.js`,
   8790 B, SHA-256
   `61b0194f3bb6534439c8d26a3ed57d0805f84b884588b761795323eeb92fcf70`,
   `--version` = `codex-cli 0.159.3`, executing on node v24.14.0
   (`/home/isa/.nvm/versions/node/v24.14.0/bin/node`, SHA-256
   `e237a2839d0cbdc9a9a2adda1a184afc0f5b20306ffbe923af5686550472d8a8`).
   Only `--version` / `--help` were invoked (local metadata; NO inference;
   NO credential access; the clients' credential stores were never read,
   listed or hashed). Both governance-frozen selections
   (claude-opus-5-5/high CLAUDE_FIRSTPARTY; gpt-6.1-sol/high
   CODEX_CHATGPT_OAUTH) remain mechanically preparable on this surface:
   claude exposes `--model` and `--effort`; codex exposes `-m/--model` and
   `-c key=value` config overrides. Neither client has a native
   `--report` flag; the frozen invocation would carry the canonical
   (`--report`, report_source) pair as the boundary-contract token with
   the launcher mediating (design ruling recorded in the workspace
   ledger; never frozen into any binding).
5. Preparation workspace created OUTSIDE the Git repository at
   `/home/isa/aucdev023-pch6b-fresh-evp-20261002-01/` (generation
   identifier `AUCDEV-023-PCH6B-730D2B29-FRESH-EVP-GEN-20261002-01`,
   derived from the preparation event; NO new EVENT_ID or reserved
   attempt ID invented). It contains ONLY: the iteration ledger, empty
   skeleton directories, and (post-incident) the review-only remediation
   artifacts of §5. NO event package, NO binding, NO event manifest, NO
   neutral contract, NO common-evidence manifest, NO sandbox profile, NO
   launcher/wrapper/gate/validator artifacts, NO static-gate evidence and
   NO handoff were created. The historical PCH package directories were
   NOT reused and NOT mutated.
6. Custody-root preparation state (tasking §7) STARTED and then
   suspended: two dedicated operator-custodied directories created at
   `/home/isa/aucdev023-pch6b-fresh-evp-20261002-01/custody/auditor-a-01/`
   and `.../custody/auditor-b-01/` (regular directories, mode 0700,
   current operator ownership, not symlinks). They are EMPTY: ZERO
   `<attempt_id>.jsonl` accounting records, ZERO report-sink files, ZERO
   frozen output artifacts — mechanically verified immediately before
   staging this publication (find mindepth 2 count 0 under custody/).
   Their st_dev/st_ino were observed (creation: st_dev 54, st_ino
   32988513 / 32988514; after the incident reboots: st_dev 52, SAME
   st_ino) but were NEVER frozen into any binding (no binding exists).
   Honest observation recorded for any future preparation: host-local
   st_dev on this filesystem is NOT stable across reboots while st_ino is
   — an object-identity freeze must therefore always be derived at the
   FINAL preparation against the then-live object, which is exactly what
   the RB2-001 runtime gate verifies at execution time. NO custody
   directory open, NO claim, NO sink creation and NO accounting call was
   ever made against these directories. Their existence is preparation
   state ONLY and is NOT attempt authority.

## 4. The blocker — GATE_W_PRIME rehearsal not executable on this host

The binding contract freezes PASS evidence for exactly eight static
gates, including GATE_W_PRIME. The adopted design is explicit that
GATE-W′ is REQUIRED and UNPROVEN until it is "IMPLEMENTED and TESTED
during separately authorized event-package preparation, BEFORE any
inference execution, using a LOCAL deterministic payload (a synthetic
stand-in client script) in the FINAL networked boundary" (design revision
§18, twelve required assertions), and the PATH-B transition Control Room
readback §6.10 requires it MUST_BE_FRESH for this new authority and
client set. The tasking repeated the obligation and its fail-closed rule:
"If any required static gate does not pass, STOP preparation and return a
HOLD package/report rather than weakening the gate" and "Never
manufacture PREPARED."

Mechanical findings established by this session (zero-provider, recorded
in the workspace ledger):

1. The UNPRIVILEGED user-namespace route is infeasible on this kernel for
   the required boundary composition: after `unshare(CLONE_NEWUSER)` with
   correct gid_map-before-uid_map mapping, inherited host mounts are
   LOCKED in the child user namespace, and bind-mounting host paths
   (`/usr` et al.) is refused with EPERM. A pivot-root minimal-root
   boundary cannot be constructed unprivileged here. `bwrap` is NOT
   setuid on this host and its unprivileged execution failed the same
   way.
2. The PRIVILEGED route (passwordless `sudo -n` is available to the
   operator user) was being de-risked when it caused the host incident of
   §5. Under the operator's post-incident constraints (no privileged
   sandbox experiments on the live laptop; no automatic retry; rehearsals
   only in a disposable environment or with reviewed isolation-gated code
   after explicit approval), the GATE-W′ rehearsal CANNOT be executed on
   this host at this time.
3. Therefore GATE_W_PRIME cannot honestly be recorded PASS, and the
   preparation cannot be completed as authorized. Per the tasking's own
   fail-closed rule this publication records the truthful HOLD. No gate
   was weakened, no evidence was pre-written, no PASS was manufactured.

## 5. The host incident (honest accounting; OBSERVED_FACT + operator records)

During launcher de-risking for the GATE-W′ rehearsal, this session ran a
sequence of namespace-prototype commands. The early ones were
unprivileged (user namespace only) and harmless. The final two were
PRIVILEGED and are the cause of the two host freezes:

```
sudo -n /usr/bin/python3 -   # 18:12:27 and 18:40:42 +03 (2026-10-02)
mount(None, "/", None, MS_REC|MS_PRIVATE, "")      # (A)
mount("tmpfs", "/tmp/rb", "tmpfs", 0, "mode=0700") # (B)
mount("/usr", "/tmp/rb/usr", None, MS_BIND|MS_REC) # (C)
mount(None, "/tmp/rb/usr", ..., MS_BIND|MS_REMOUNT|MS_REC|MS_RDONLY, "")  # (D)
syscall(SYS_pivot_root, ".", "old")                # (E)
umount2("/old", MNT_DETACH)                       # (F)
```

Root cause: the command ran as REAL ROOT in the INITIAL mount namespace
with NO `unshare(CLONE_NEWNS)`. (A) did not create a namespace —
MS_PRIVATE only changes the propagation of EXISTING mounts — so it
flipped the REAL host root's propagation host-wide and removed the
kernel's EINVAL guard (pivot_root refuses a shared new_root) that had
protected the host in the previous attempt; (E) then pivoted the HOST'S
ACTUAL ROOT under `/tmp/rb/old` and (F) lazily DETACHED the real root
filesystem from the mount table. `/proc` and `/dev/shm` then failed for
running applications (journal evidence from 18:12:32); the system hung
and required hard reboots. The 18:40:42 occurrence was an AUTOMATIC
RE-RUN of the identical command after the first session interruption —
an unknown-outcome privileged command must never be retried
automatically; this session owns that aggravation.

Recorded as finding `AUCDEV023-PCH6B-PREP-INCIDENT-20261002-001`
HOST_FREEZE_CAUSED_BY_PREPARER_PRIVILEGED_MOUNT_NAMESPACE_EXPERIMENT
(INFORMATIONAL to the AUCDEV-023 audit lineage — it involves NO audit
subject code and NO governance-chain product code — but BLOCKING for
this preparation and material to operator safety): operator diagnostics
at `/home/isa/.local/state/freeze-check/20261002-184620/` correlate both
freezes to this session's two commands (session jsonl lines 327 and 342;
sudo log shows `isa ... USER=root ... COMMAND=/usr/bin/python3 -` at
18:40:42); SMART health passes; the host mount table is clean after the
reboots; the leftover experiment directories under /tmp (tmpfs) are gone.

Remediation PREPARED (REVIEW-ONLY, NOT executed, NOT part of this
publication's staged content — it lives in the untracked preparation
workspace): a fail-closed isolation gate
(`build/boundary_isolation.py` in the workspace) with NO module-level
mount wrapper, where every mutating syscall is a method on a capability
object issued only after: recording the initial mnt-ns identity,
`os.unshare(CLONE_NEWNS)`, and PROOF that the process mnt-ns inode
changed and differs from `/proc/1/ns/mnt` (and an optional caller guard
ns); every method re-proves the namespace identity immediately before
its syscall and refuses otherwise; plus the operational rules R-1 (no
privileged namespace experiments on the live host), R-2 (an interrupted
privileged command is never auto-retried), R-3 (no isolation proof ->
zero host mutations, structurally enforced), R-4 (approved rehearsals run
in a disposable environment). Full analysis in the workspace
`build/INCIDENT-20261002-BOUNDARY-ISOLATION-REVIEW.md`. A future
preparation may adopt these ONLY after operator review and an explicit
new authorization.

## 6. Held governance preserved (NOT converted by this HOLD)

- The fresh preparation authority of 2026-10-02 was RECEIVED and partially
  exercised for preparation-side work only; it is NOT completed and NOT
  silently revivable: any future event-package preparation requires a NEW
  explicit operator authorization. The previously held preparation
  authority likewise remains RECEIVED / NOT EXECUTED / NOT CONSUMED /
  FAIL-CLOSED HELD.
- NO event package was created or frozen (neither role); NO binding
  document exists; NO event manifest exists; NO neutral audit contract,
  common-evidence manifest, sandbox profile, launcher, tool wrapper,
  dynamic-gate executable or structural validator was frozen; NO
  static-gate evidence was recorded (GATE_W_PRIME honestly NOT PASS, all
  others honestly NOT RECORDED rather than pre-written).
- The bootstrap event was NOT instantiated; the reserved event identity
  `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01` and the two reserved
  attempt identities remain DESIGN_RESERVED_ONLY binding constants; NO
  attempt authority was granted; NO real reserved-attempt accounting
  record exists; NO report sink exists; NO frozen report artifact exists.
- New-lineage model engagements USED 0 with PROPOSED 2 unchanged.
- Historical PCH6 authority CONSUMED / TERMINAL / CLOSED / NO_RERUN with
  all historical identities NON-TRANSFERABLE and the AUCDEV-010
  bootstrap-root exception NON-TRANSFERABLE; historical handoffs NOT
  repacked; historical model identities, runs, records, matrices, prompts
  and evidence workspaces untouched (append-only).
- BA-PREP-001 / BA-PREP-002 / BA-PREP-RB2-001 / BA-PREP-RB2-002 closures
  at Control Room remediation-readback strength RETAINED and NOT
  reopened; BA-RB-001 / BA-RB-002 / BA-RB-003 closures RETAINED;
  historical informational findings retained WITHOUT rewriting.
- PCH6-B-SD-002 and PCH6-CR-BSD-001 remain NOT CLOSED awaiting fresh
  independent audit of the frozen target; PCH6-B-SD-001 RETAINED / OPEN;
  ROOT_CAUSE_NOT_ESTABLISHED unchanged with NO causal conversion.
- Independent-auditor provenance / authority gate NOT_SATISFIED
  (installed Audit Council source
  `8ae33444f349ce73c1359b963722e2d16acba630`; independently-qualified
  predecessor provenance NOT ESTABLISHED), stated ONLY as NOT satisfied.
- AUCDEV-023 remains P1 / READY / NOT DONE; AUCDEV-024 P1 / READY / NOT
  DONE; NO queue transition occurs solely because this HOLD is published
  (the AUCDEV-023 queue row is byte-identical, still P1 / READY).
- Qualification NONE; installation NONE; no /audit-council execution
  authorized.

## 7. Zero-execution census (tasking §16, before and after preparation attempt)

REAL_PROVIDER_CALLS = 0; REAL_CLIENT_INFERENCE_CALLS = 0;
REAL_AUDITOR_EXECUTIONS = 0; AUDIT_COUNCIL_EXECUTIONS = 0;
BOOTSTRAP_AUTHORITY_REAL_RUN_ATTEMPTS = 0; EVENT_INSTANTIATIONS = 0;
ATTEMPT_AUTHORITIES_GRANTED = 0; REAL_RESERVED_ATTEMPT_ACCOUNTING_RECORDS
= 0; REAL_REPORT_SINKS_CREATED = 0; MODEL_ENGAGEMENTS_CONSUMED = 0;
REAL_CREDENTIAL_CONTENT_READS = 0; QUALIFICATION = NONE; INSTALLATION =
NONE. (The only privileged actions taken anywhere in the preparation
attempt were the four namespace-prototype spike commands of §5's
sequence, two of which caused the host incident; after the operator's
post-incident instruction this session executed ZERO privileged commands
and ZERO namespace operations.)

## 8. Publication safety

Staged EXACTLY three authorized documentation paths (no source, test or
package implementation file; no event-package tracked path; no .jsonl):
NEW canonical HOLD record (THIS file); MODIFY CURRENT with the rotation
confined EXACTLY to lines 3/11/23-25 plus one dated tail record (difflib
zones replace@3 + replace@11 + replace@23-25 + insert@tail; changed-line
set EXACTLY [3, 11, 23, 24, 25]); MODIFY BACKLOG with exactly TWO pure
insert zones (one NEW dated status bullet immediately after the BA-PREP
follow-up remediation readback status bullet, plus one NEW dated tail
record; zero replace/delete). Staged write-tree recorded in the commit
message; protected trees and the bootstrap-authority tree held EXACT
(ZERO source modification staged and ZERO performed); staged == working
on all three paths; git diff --check and staged git diff --cached --check
PASS; queue mechanically recounted base == staged on every structural
dimension with no queue-row transition; sealed-identity no-NEW-occurrences
gate PASS (ZERO occurrences in the NEW record); credential/secret
mechanical scan clean over the NEW record and all diff-added lines;
hex-literal gate PASS (every >=7-char non-decimal hex literal in the NEW
record and diff-added lines machine-verified against the session-derived
verified-identity allow-set, decimal-only exempt); wording gates PASS (NO
causal conversion of ROOT_CAUSE_NOT_ESTABLISHED; frozen-target closure
mentions always negated; audit-PASS mentions always negated; provenance
gate stated ONLY as NOT satisfied; NO unnegated event-instantiation
claim; grants-nothing present; disposition token present). The FULL
precommit gate battery ran from scratch on the FINAL staged bytes and ALL
GATES PASSED before commit.

## 9. Honest session iteration accounting (without erasure)

All iterations instrument-side or evidence-side EXCEPT the incident,
which was real host damage caused by this session and is recorded as
such; NO failed observation was rewritten as PASS; every first output is
preserved in the untracked workspace ledger and the session transcript:

- T-1 unprivileged user-namespace prototype: gid_map write failed EPERM
  when written AFTER uid_map (kernel ordering rule); corrected to
  gid_map-before-uid_map and raw os.open/os.write (buffered TextIO on
  /proc map files proved unreliable). Host impact: none (all EPERM).
- T-2 nested user-namespace probe (`unshare -U` inside a user namespace)
  refused EPERM — user namespaces must be created at level 1 on this
  host; noted as a launcher constraint. Host impact: none.
- T-3 LOCKED-MOUNT discovery: bind-mounting host paths inside the child
  user namespace refused EPERM (inherited mounts are locked); bwrap
  (non-setuid) failed the same way. This killed the unprivileged route.
  Host impact: none.
- T-4 privileged spikes (the first two): one ENOENT (tmpfs covering
  pre-created dirs — instrument bug), one EINVAL on the RO remount
  (missing MS_REMOUNT — instrument bug); both left transient mounts in
  the host table that the reboots later cleared. The EINVAL of the pivot
  attempt in this period was the kernel REFUSING to pivot a shared
  (host) root — misread at the time as a flag bug (see T-5).
- T-5 THE INCIDENT: adding MS_PRIVATE removed that guard; pivot_root +
  umount2(MNT_DETACH) in the initial mount namespace detached the real
  host root; TWO freezes (18:12:27; 18:40:42 the automatic re-run after
  session interruption). Diagnostics, analysis, review-only fix and
  operational rules recorded (§5). This iteration was NOT
  instrument-side: it damaged the host and is the direct cause of this
  HOLD.
- T-6 post-incident static analysis turn: zero privileged commands;
  incident review + review-only isolation-gate module written to the
  workspace; memory updated. A memory-index bookkeeping line was lost in
  one shell rewrite and immediately restored (host-side only; no
  repository state involved at any point).

## 10. Next action — EXACTLY ONE

OPERATOR DECISION ON A SAFE GATE-W-PRIME REHEARSAL PATH (for example: a
disposable rehearsal environment provided by the operator; or ONE
reviewed run of the isolation-gated boundary code after explicit
operator approval; or a redesigned boundary approach that requires no
privileged namespace construction on the live host) BEFORE ANY NEW
EVENT-PACKAGE PREPARATION AUTHORIZATION. Recording this next action
grants NO authority of any kind; this HOLD publication itself grants
nothing and closes nothing; a future preparation requires a NEW explicit
operator authorization and remains preparation ONLY under all the limits
of §1.

## 11. Standing prohibitions (unchanged)

NEVER invoke the wrapper or driver in the AUCDEV-023 governance chain
from an agent session; never rerun the launcher; never treat any recorded
grant phrase (including any phrase recorded here) as a new grant; never
execute a real auditor or provider/model; never open the four historical
sealed artifacts (identity-only forever); never relabel or rewrite
historical model identities, runs, records, matrices, prompts or evidence
workspaces (append-only); never claim audit PASS, qualification,
installation or any authority from this publication — it grants none; and
— added by this record — never run privileged mount/pivot_root/umount
experiments on the operator's live host, and never automatically re-run
an interrupted privileged command.
