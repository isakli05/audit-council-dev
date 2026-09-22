# AUCDEV-023 S1 — RB-001 DIAGNOSTIC-PRESERVATION REMEDIATION DESIGN

- **Authority (operator-granted, design-only):** `AUCDEV-023-S1-RB001-DIAGNOSTIC-PRESERVATION-DESIGN-20260922-01`
- **Target finding:** `AUCDEV023-CR-S1-EXEC05-RB-001` = `AUDITOR_B_REPORT_MISSING_RC1_ROOT_CAUSE_NOT_PRESERVED_IN_MECHANICAL_HANDOFF` (COMPLETENESS LIMITATION / FAILURE-DIAGNOSTIC EVIDENCE GAP / OBSERVED FACT / ROOT_CAUSE_UNRESOLVED / NO_PRODUCT_DEFECT_CONCLUSION_YET)
- **Session role:** BOUNDED DIAGNOSTIC-PRESERVATION DESIGNER + RECORD PUBLISHER ONLY. NOT Auditor-A/B, NOT an execution controller, NOT a replacement execution / implementation / qualification / installation authority.
- **Activity class:** DESIGN-ONLY / ZERO-AUDITOR-PROVIDER. Exact frozen/mechanical artifacts were inspected read-only; the remediation was NOT implemented; no auditor/provider/frontier client was executed; no replacement execution is authorized by this record.
- **Date:** 2026-09-22 (Europe/Istanbul)
- **Canonical base:** `6e1f86c393708cef39eb1b80dbad97a23db18cc8` (tree `56192d04307192024709bc6f2da7241c0e97fd68`; sole parent `6137423e2ac3735788ddf6f731c31cd12ba6c3b9`) — verified EXACT as live GitHub master at bootstrap and re-resolved immediately before staging and push.
- **RB-001 status after this record:** **OPEN at DESIGN strength.** Not fixed, not closed. No implementation has occurred.

---

## 1. Bootstrap verification (performed BEFORE design work)

- Remote `origin` = `https://github.com/isakli05/audit-council-dev.git`; live `refs/heads/master` = `6e1f86c393708cef39eb1b80dbad97a23db18cc8` = local HEAD (EXACT equality; STOP-WITHOUT-MUTATION clause not triggered).
- Root tree `56192d04307192024709bc6f2da7241c0e97fd68`; sole parent `6137423e2ac3735788ddf6f731c31cd12ba6c3b9` (both EXACT).
- Protected trees at the base, all EXACT and byte-unchanged by this session: `bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0` (the remediated EBS), `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`, `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f` (the latter two equal the frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322`).
- Tracked working-tree drift at bootstrap: only the long-known pre-existing `smoke-fixture` / `smoke-fixture-103` gitlink drift (outside every protected/docs path; preserved unstaged, unchanged by this session).
- The seven required governance docs were fetched at the base SHA; canonical EXEC-05 mechanical-readback blob verified EXACT: `docs/chatgpt-project/AUCDEV-023-S1-EXEC05-FIRSTPASS-MECHANICAL-READBACK.md` = Git blob `606c855d59e2c49fe75a7f7d53139dfbbec0e6e1`.

## 2. Read-only artifact identity verification (nothing executed)

| Artifact | Identity | Verification |
|---|---|---|
| EXEC-05 driver `aucdev023-firstpass-exec05.py` | SHA-256 `d4d1eca2baa3b8f50aa7f666986cf4d1e6ca4cf2bc09ea2dfe6feca503032357`, 117120 B, mode 0700, `wc -l` 2448 (trailing newline) | EXACT, NOT executed, NOT altered |
| EXEC-05 wrapper `run-aucdev023-firstpass-exec05.sh` | SHA-256 `17e0abcd34303d0defda2326587cb80550872e8ebdb55b1055fb880e6d06534c`, 2836 B, mode 0700 | EXACT, NOT executed, NOT altered |
| EXEC-05 mechanical handoff `AUCDEV-023-S1-FIRSTPASS-EXEC-20260922-05-MECHANICAL-HANDOFF.tar.gz` | outer SHA-256 `1cf24887790a5a11e7415d042628fde4c9fc28e26b6036830108f4f17daa2bda`, 38388 B | streamed census+checksum re-verified: 21 members = 21 regular files, exactly one SHA256SUMS, 20 rows **20/20 PASS**; nothing extracted to durable paths, nothing executed |
| Frozen boundary launcher `event/package-auditor-{a,b}/boundary/networked-boundary-launcher.py` | SHA-256 `2efb666042e44d272a53f9ad4ac93a19c14f1687a33fb38ed84f9823d9bc44a7`, 27719 B — byte-identical at BOTH role packages | EXACT, read-only, NOT altered |
| Auditor-B binding `event/binding-auditor-b.json` | SHA-256 `489a3c911d00d109054e108fa0c89e878fa14f908e01f320022b6bbd1888ade4` | EXACT (non-secret binding; mechanical scalars only were read) |
| Remediated EBS `bootstrap-supervisor/ebs/` | protected tree `732b8def9f22d7c466ce77f3d3049da53bfff3d0`; `launch.py` 84365 B / 1685 lines | read-only source analysis only |
| Deployed successor event root `/home/isa/aucdev023-s1-prep002-rem002/event` | accepted successor generation (contract `cc6ec29d…`, gate `27948980…`, validator `6aff0e7e…`, MANIFEST A `2f8efbd6…` / B `15729d8b…`, boundary `2efb6660…`, tool wrapper `0ed2ba48…`) | verified read-only, NOT altered by this session |

Auditor-A frozen report identity `ba8a29a12867273616143e48a86f101f14f6e0e207136d83b31e7fd2426ec1a0` / 23727 B / 0444 is carried forward as **mechanical reference ONLY**; the report was NOT opened, read, hashed, or copied by this session.

## 3. Observed EXEC-05 mechanical facts this design must explain (from the verified handoff)

- Auditor-A `evt-79182989824ce966-A-01`: rc=0, exec_failed=false, timed_out=false, REPORT_FROZEN, conforming — **`metadata_keys: []`** (empty).
- Auditor-B `evt-79182989824ce966-B-01`: rc=1, exec_failed=false, timed_out=false, REPORT_MISSING, nonconforming — **`metadata_keys` = exactly 14 keys**: `attempt, auditor_executable_inode_checked, auditor_executable_is_frozen_package_payload, client_returncode, credential_printed, elapsed_seconds, event, invocation_sha256, launcher, launcher_version, output_name, report_present, role, staging_dir`; B `staging/` and `custody-out/` EMPTY; validator never reached.
- Neither VALUES of B's metadata nor any raw stdout/stderr was preserved anywhere — that omission IS RB-001.

## 4. §6 analysis — the EBS DOES transport parsed metadata values intact

Independently re-established from the exact remediated EBS source (`bootstrap-supervisor/ebs/launch.py`, protected tree `732b8def…`):

- `_child_setup` (`launch.py:964-1006`): child fd 1 = `dup2(metadata_w, 1)` — the boundary child's stdout IS the EBS metadata pipe (`:984`); fd 2 = devnull (`:985`); FAIL_FD=4 is CLOEXEC (`:993`); on any child-setup/exec failure the child writes `b"E"` to fd 4 and `_exit(CHILD_EXIT_EXEC_FAIL)` with `CHILD_EXIT_EXEC_FAIL = 98` (`:1001-1006`, `:149`).
- `_fork_and_launch` (`:1293-1455`): both parent pipes are set NONBLOCKING (`:1340-1341`); the metadata pipe is drained CONCURRENTLY with the running child, accumulating into `metadata_raw` while `len(metadata_raw) < METADATA_MAX` with `METADATA_MAX = 65536` (`:1378-1388`, `:150`); after reap there is a bounded `METADATA_GRACE = 0.5 s` final drain for a descendant that may still hold the write end (`:1389-1398`, `:151`); `json.loads(metadata_raw.decode())` parses the WHOLE buffer, with a silent `metadata = None` on `UnicodeDecodeError/JSONDecodeError` (`:1447-1452`); `core = (exitcode, fail_byte == b"E", metadata or {})` (`:1453`).
- `_report_and_terminalize(core)` (`:1575-1670`) unpacks `returncode, exec_failed, metadata` (`:1584`) and returns `AttemptResult(returncode, exec_failed, metadata, False, …)` (`:1667-1670`) — the SAME parsed dictionary, intact.
- Timeout path (`:1429-1446`): kills the attempt group and returns `AttemptResult(exitcode, False, {}, True, "", "", 0)` — metadata is discarded on timeout, and `timed_out=True` marks it externally.
- `snapshot_staging()` returns `None` when no staging report exists → REPORT_MISSING is settled BEFORE the validator (`:1595-1600`; `reportcustody.py:48-59`) — matching B's observed chain.

**Determination (OBSERVED SOURCE FACT): the EBS already transports the boundary launcher's parsed metadata VALUES intact through `AttemptResult.metadata`. The EXEC-05 value loss did NOT occur in the EBS. Per §19: `EBS_CHANGE_NOT_REQUIRED`.** Two informational EBS-side residuals are recorded and are externally derivable WITHOUT any EBS change: (a) an unparseable metadata buffer silently collapses to `{}` (indistinguishable from empty) — but `exec_failed`/`timed_out` flags plus the (future) channel isolation make this cell self-describing; (b) the timeout path discards metadata by construction and is separately marked by `timed_out=true`.

## 5. §7 analysis — the exact driver value-loss point

From the exact EXEC-05 driver bytes (`aucdev023-firstpass-exec05.py`, `d4d1eca2…`):

- The driver's ONLY consumption of `result.metadata` is `aucdev023-firstpass-exec05.py:1798`:
  `"metadata_keys": sorted(result.metadata or {})` inside the attempt summary (`:1789-1838`).
- The summary is written as evidence member `04-attempt-a-summary.json` / `05-attempt-b-summary.json` (`:1855-1856`) and included in the generated-LAST mechanical handoff by `build_handoff` (`:2172-2178`).
- Therefore the complete loss path is: boundary stdout JSON → EBS pipe → `json.loads` (`launch.py:1450`) → `AttemptResult.metadata` (values intact) → **driver `:1798` reduces to sorted key names — VALUES DISCARDED HERE** → summary JSON → mechanical handoff.

**Determination (OBSERVED SOURCE FACT): the value-loss point is the deterministic operator driver at `:1798`, not the EBS and not the boundary.** This is an observed source fact, not a root-cause inference about B's rc=1.

## 6. §8 analysis — frozen boundary-launcher semantics (reconstructed from exact source)

`networked-boundary-launcher.py` (`2efb6660…`), all line citations exact:

1. **Argv contract** (`:504-514`): parses `--role/--attempt/--event` pairs; if `role not in ROLE_LAYOUTS` or attempt/event missing → stdout `{"launcher": IDENTITY, "error": "ARGV_CONTRACT_INVALID"}` and **return 2** (fixed).
2. **Normal init** (`:515-517`): `metadata = {"launcher": IDENTITY, "launcher_version": VERSION ("S1-PREP002-REM2-1", :110), "role", "attempt", "event", "credential_printed": False}`.
3. **Deterministic setup before composition** (`:519-538`): bounded credential read from fd 3 ≤ 65536 (`:133`, `:519-520`); bounded invocation read from fd 6 ≤ 8192 + `json.loads` parse (`:521-523`); `resolve_auditor_path(fd 5)` inode check (`:524`, `:294-309`) → `auditor_executable_inode_checked: True`; `auditor_executable_is_frozen_package_payload` = exact-path comparison (`:531-532`); `invocation_sha256 = sha256(invocation_raw)` (`:533-534`); `staging_dir = ROOT/attempts/<attempt>/staging` + makedirs (`:535-537`); `output_name = f"{attempt}.first-pass-report.json"` (`:538`, `:493-494`).
4. **Composition** (`:546-555`): credential/invocation delivered as fresh anonymous memfds consumed by the PACKAGE-PINNED vendored bwrap; composition argv ends `-- /usr/bin/python3 -c INNER` (`:553`); executed as **`subprocess.run(args, pass_fds=(cred_r, inv_r), timeout=None)` (`:554-555`) — with NO stdout/stderr redirection.**
5. **On completion** (`:558-568`): `client_returncode = completed.returncode` (`:558`); `report_present = os.path.isfile(staging_report)` (`:559-560`); `elapsed_seconds = round(monotonic_delta, 3)` (`:561`); emits ONE `json.dumps(metadata, sort_keys=True) + "\n"` line ≤ `METADATA_MAX_BYTES = 65536` (`:134`, `:562-566`, with a `METADATA_OVERSIZE` fixed-token fallback `:563-565`) and **returns `completed.returncode`** (`:568`).
6. **On outer exception** (`:569-574`): `metadata["error"] = f"LAUNCHER_FAILURE: {exc!r}"[:512]`; `credential_printed = False`; emits the metadata line and **returns 3** (fixed).
7. **INNER** (`:228-261`, embedded, runs INSIDE bwrap in the client domain): materializes the role home/config from the staged memfd data, clears/sets the frozen client env, `os.chdir("/auditor-output")`, then **`os.execv("/auditor-init/auditor-executable", list(argv))` (`:260`) — with NO exception handler and NO distinct exit code anywhere in INNER.**

Launcher exit-code classes seen by the EBS: **2** = argv-contract refusal; **3** = outer deterministic setup/exception failure; any other N = the bwrap composition's exit status.

## 7. §9 analysis — stdio/metadata-channel provenance (the transport-separation question)

- **OBSERVED SOURCE FACT:** the EBS child contract makes boundary stdout the metadata pipe (`launch.py:984`) and boundary stderr `/dev/null` (`:985`); the frozen boundary launcher composes via `subprocess.run(...)` WITHOUT explicit stdout/stderr redirection (`:554-555`), so the bwrap process, the `python3 -c INNER` process, and — after INNER's `os.execv` (`:260`) — the AUDITOR CLIENT ITSELF all inherit fd 1 = the EBS metadata pipe. The EBS concurrently accumulates the whole pipe into one bounded buffer (`launch.py:1378-1388`) and parses the ENTIRE buffer as one JSON document (`:1450`).
- **OBSERVED SOURCE FACT (consequence):** the launcher writes its metadata line only AFTER `subprocess.run` returns (`:558-566`), i.e. AFTER the client has exited; therefore any non-whitespace bytes the client wrote to stdout PRECEDE the metadata JSON in the same buffer, and `json.loads` over `client_bytes + json_line` fails ("Extra data") → `metadata = None` → `{}` (`launch.py:1451-1454`) — silently, with no key names preserved either. Independently, if the client writes ≥ `METADATA_MAX` (65536) bytes the accumulate guard stops reading (`:1378`) and the launcher's JSON tail may never be read at all. (No deadlock exists: the drain is concurrent and nonblocking.)
- **INFERENCE (source-consistent, unconfirmable — precisely because of RB-001):** Auditor-A's observed rc=0 + `metadata_keys: []` is source-consistent ONLY with a metadata buffer that failed to parse (the launcher provably writes exactly one line on every non-timeout exit path 0/2/3), best explained by Auditor-A client stdout contaminating the pipe; Auditor-B's clean 14-key parse implies the codex client emitted no stdout. This cannot be CONFIRMED because neither the values nor the raw stream were preserved. It is recorded as an inference, not a fact.
- **HYPOTHESIS: none required.** No timing/text heuristics were used or needed.
- **Verdict: the current mechanical metadata transport is NOT mechanically isolated — metadata survival depends on the uncontrolled stdout behavior of the auditor client.** Any RB-001 remediation that only preserves parsed values would still lose ALL metadata whenever a client writes stdout (the inferred Auditor-A mode), so the channel question is IN scope for the remediation (§15).

## 8. §10 field-by-field provenance / safety table

| Field | Producer / assignment point | Type / domain | Pre/post client | Can contain model/provider text | Can contain secrets | Safe to persist (strict allowlist) |
|---|---|---|---|---|---|---|
| `launcher` | boundary `:512/:515`, constant `NETWORKED-BOUNDARY-LAUNCHER-V1` | str, 1 finite value | pre | no | no | YES — must equal `binding.boundary_launcher.identity` |
| `launcher_version` | boundary `:110/:515`, finite constant (today `S1-PREP002-REM2-1`) | str, finite set pinned per generation | pre | no | no | YES — pinned per generation |
| `role` | boundary `:516`, from argv, validated ∈ `{AUDITOR_A, AUDITOR_B}` | str, 2 values | pre | no | no | YES — must equal binding role |
| `event` | boundary `:516`, from argv (launcher does NOT format-validate) | str, pattern `^evt-[0-9a-f]{16}$` | pre | no | no | YES — must equal binding event id |
| `attempt` | boundary `:516`, from argv (not format-validated) | str, pattern `^evt-[0-9a-f]{16}-[AB]-[0-9]{2}$` | pre | no | no | YES — must equal binding attempt id |
| `output_name` | boundary `:538` (`:493-494`) | str ≤ 256 B, deterministic from attempt | pre | no | no | YES — must equal `binding.output_identity.name` |
| `staging_dir` | boundary `:535` | str ≤ 512 B, deterministic path | pre | no | no | YES — must equal driver plan staging path |
| `invocation_sha256` | boundary `:533-534` | str `^[0-9a-f]{64}$` | pre | no | no | YES — must equal sha256 of the binding's canonical compact-JSON invocation (B: `48acda37d12524fd…`; mechanically recomputed this session from `binding.auditor_invocation`) |
| `auditor_executable_inode_checked` | boundary `:525` | bool (true on completed path) | pre | no | no | YES |
| `auditor_executable_is_frozen_package_payload` | boundary `:531-532` | bool | pre | no | no | YES |
| `credential_printed` | boundary `:517/:571` — constant False in the frozen source | bool, domain {false} | pre | no | no (a boolean attestation, never material) | YES — value true ⇒ immediate fail-closed escalation |
| `client_returncode` | boundary `:558` — the bwrap COMPOSITION exit status, NOT mechanically the client's own | int ∈ [-64, 255] | post | no | no | YES with corrected semantics (see §9/§10 of the design) |
| `report_present` | boundary `:559-560`, `os.path.isfile` on the staging report | bool | post | no | no | YES |
| `elapsed_seconds` | boundary `:561` | float ∈ [0.0, auditor_timeout + 60], ≤ 3 decimals | post | no | no | YES |
| `error` | boundary `:513` (fixed token `ARGV_CONTRACT_INVALID`) OR `:570` (`f"LAUNCHER_FAILURE: {exc!r}"[:512]` — arbitrary Python exception repr, may embed paths/OS text) | str ≤ 512 B but UNBOUNDED content | pre/outer | indirectly yes (exception text) | indirectly possible | **NO — raw text must NOT be persisted.** Only the derived finite class `{ARGV_CONTRACT_INVALID, LAUNCHER_FAILURE, NONE}` is persistable (exact-token / exact-prefix match, else `UNCLASSIFIED_REJECTED`) |

**Conclusion:** every existing field except raw `error` text is a trusted-launcher-produced scalar that is strictly allowlistable, type-validatable, bounded and cross-checkable; `error` is safe only as a derived finite structural class.

## 9. §11 analysis — existing-metadata sufficiency matrix (classes A–H)

Central question: **are the existing parsed values, strictly allowlisted in the driver, sufficient to distinguish the relevant failure classes?**

| Class | Existing-field signature (with values preserved) | Distinguished? |
|---|---|---|
| A. EBS child exec failure before boundary exec | `exec_failed=true` (fail-pipe `b"E"`, `launch.py:1003`), rc=98 | **YES** (already persisted today) |
| B. Boundary outer argv-contract refusal | rc=2 + `error` exactly `ARGV_CONTRACT_INVALID`, 2-key metadata shape | **YES** |
| C. Boundary outer deterministic setup/exception failure | rc=3 + `error` prefix `LAUNCHER_FAILURE:` (partial field set = fields assigned before the exception point) | **YES** |
| D. bwrap/INNER failure BEFORE the auditor executable is reached | `client_returncode = 1` (or other nonzero), `report_present=false` | **NO — collides with E** |
| E. INNER exec succeeded; the AUDITOR CLIENT itself exits nonzero | `client_returncode = N≠0`, `report_present=false` (B's exact observed cell) | **NO — collides with D** |
| F. Client rc=0, no report | rc=0 + `report_present=false` + EBS REPORT_MISSING | **YES** (rc=0 mechanically implies exec reached: the ONLY rc=0 path is a successful `execv` of the fd-verified executable whose process then exits 0 — INNER's uncaught failures exit 1) |
| G. Client nonzero but report exists | rc≠0 + `report_present=true` | **YES** (only the client can create the staging report via the `/auditor-output` rw bind ⇒ the client ran; transitively distinguishes D-vs-E in this cell) |
| H. Report exists, validator/custody fail | EBS `report_state` REPORT_SCREEN_FAIL / REPORT_INVALID (+ pinned snapshot sha/size) | **YES** (already separate) |

**The D-vs-E collision is SOURCE-PROVEN, not assumed:** INNER has no exception handler and no distinct exit code (`:228-261`), so ANY INNER setup failure and ANY `os.execv` failure dies as an uncaught Python traceback with **exit 1**; bwrap's own setup failures also exit nonzero (typically 1); and a genuinely executed client may itself exit 1. `client_returncode` is assigned from the composition status (`:558`) and is therefore NOT mechanically guaranteed to be the client's own return code. D and E are NOT equivalent and MUST NOT be collapsed — but with the existing fields they are indistinguishable exactly in the `rc≠0 ∧ report_present=false` cell, which is precisely Auditor-B's observed terminal cell. **Answer: EXISTING VALUES ARE NOT SUFFICIENT.**

## 10. §12 decision — the DRIVER-ONLY path

- (1) EBS transports parsed values intact: **PASS** (§4).
- (2) Transport cannot mix arbitrary auditor/model output into the parse source, or a driver-only mechanism can reject contamination without losing the distinction: **FAIL** — the channel is shared (§7), the driver receives only the already-parsed dict (`{}` after a parse failure) and cannot decontaminate without persisting raw stdout, which the authority forbids.
- (3) Existing fields distinguish composition refusal from a genuinely executed client nonzero exit: **FAIL** — D/E collision source-proven (§9).
- (4) Every persisted value strictly allowlistable/type-validatable/bounded: **PASS** (§8).
- (5) No raw stdout/stderr/error text/report/credential/provider output needed: **PASS** — but moot given (2)/(3).

**DRIVER-ONLY REMEDIATION IS NOT RECOMMENDED — REJECTED AS INSUFFICIENT.** (It would fix only the observed value loss, i.e. B's 14 keys→values, while leaving both the D/E ambiguity and the channel-contamination loss mode open.)

## 11. §13/§14 selected design — MINIMAL boundary structural remediation (SPECIFIED, NOT IMPLEMENTED)

### 11.1 B2 — exec-status CLOEXEC pipe (proves "auditor executable exec was reached")

- The OUTER boundary launcher creates an anonymous `os.pipe()`; the write end is passed into the composition via `pass_fds` at a FIXED inherited fd (e.g. fd 7) alongside the existing data memfds.
- INNER (revised, still embedded/trusted) does, in order: set `FD_CLOEXEC` on fd 7 immediately; on ANY pre-exec setup exception write the fixed 1-byte token `b"I"` then re-raise (uncaught → exit 1); wrap `os.execv(...)` and on `OSError` write `b"X"` then re-raise (uncaught → exit 1); a SUCCESSFUL `execve` closes fd 7 via CLOEXEC → the outer read end sees EOF with ZERO bytes.
- The OUTER launcher, AFTER `subprocess.run` returns (whole attempt tree exited), performs a bounded nonblocking read of the exec-status pipe with a ≤ 0.5 s grace window (mirroring the EBS `METADATA_GRACE` pattern, `launch.py:151`), then closes it. Read semantics (finite, deterministic):
  - zero bytes + EOF + `client_returncode ≥ 0` → `client_exec_reached: true`;
  - token `b"I"` → `inner_failure_class: "INNER_SETUP_FAILED"`, `client_exec_reached: false` (rc will be 1);
  - token `b"X"` → `inner_failure_class: "INNER_EXEC_FAILED"`, `client_exec_reached: false` (rc will be 1);
  - zero bytes + `client_returncode < 0` → `client_exec_reached: false` (composition killed by signal pre-exec-completion);
  - EOF not reached within grace → `exec_status_transport: "GRACE_EXPIRED_UNDETERMINED"` (fail-closed; recorded honestly, never guessed).
- **Why this closes D-vs-E:** the write-end handle exists ONLY in the trusted INNER process image before `execve`; after a successful exec the client holds NO handle (CLOEXEC closed it), and before exec only trusted INNER code can write. A token ⇒ class D (with sub-class); zero-byte EOF with rc ≥ 0 ⇒ the exec transition happened ⇒ class E/F/G by rc/report_present.
- **Non-forgeability / fail-closed:** the pipe is anonymous; the launcher is `PR_SET_DUMPABLE=0` (`:499`, `:264-269`) so its own fds are not reachable via `/proc`; the client runs inside bwrap with `--unshare-pid` and a namespace-local `/proc`, so host/launcher processes are invisible to it; the token set is fixed 1-byte, produced only by trusted launcher/INNER mechanics. NO timing heuristics, NO stdout/stderr parsing, NO model messages, NO report content, NO credential inference (§14's prohibitions hold).

### 11.2 B1 — metadata-channel isolation

- `subprocess.run(args, pass_fds=(cred_r, inv_r, exec_status_w), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=None)` — the composition's stdout/stderr are directed to `/dev/null`, RESERVING the outer launcher's stdout (the EBS metadata pipe) solely for the single mechanical metadata JSON line.
- Nothing permissible is lost: client stdout was never a legitimate evidence input (it was discarded unparseably at best), and raw auditor stdout/stderr MUST NOT be persisted anyway. The EBS fd contract (fd1 = metadata pipe, fd2 = devnull) is UNCHANGED — no EBS edit.
- Rejected alternatives (§15): a dedicated metadata fd not inherited by the client would change the EBS `_child_setup` fd contract (EBS blast radius — rejected); persisting any mixed stream (rejected — authority conflict).

### 11.3 Boundary metadata additions (finite, non-substantive)

- `client_exec_reached: bool` (per 11.1);
- `inner_failure_class: null | "INNER_SETUP_FAILED" | "INNER_EXEC_FAILED"`;
- `exec_status_transport: "READ" | "GRACE_EXPIRED_UNDETERMINED"`;
- `launcher_version` bumped to a NEW finite value chosen at implementation (identity hook for the revision);
- exit-code semantics unchanged (2 / 3 / composition status); every existing field and its producer unchanged; `METADATA_MAX_BYTES` bound and `METADATA_OVERSIZE` fallback retained.

### 11.4 Driver-side strict-allowlist persistence (the driver component)

- Replace `:1798` keys-only reduction with a strict-allowlist validated persistence block and a derived transport verdict:
  `metadata_transport ∈ {CLEAN_JSON_PARSED, NOT_PRODUCED_EXEC_FAILED, DISCARDED_ON_TIMEOUT, UNPARSEABLE_FAIL_CLOSED}` (derived: `exec_failed` → NOT_PRODUCED; `timed_out` → DISCARDED (EBS `:1445-1446`); non-empty validated parse → CLEAN; otherwise → UNPARSEABLE_FAIL_CLOSED — with channel isolation the boundary always writes exactly one line on every non-timeout path, so the residual empty/unparseable ambiguity collapses to a fail-closed flag).
- Persist `metadata_keys` (continuity) AND the validated `boundary_metadata` object per §12's schema; on ANY validation failure persist keys-only + `metadata_schema_validation: "REJECTED_FAIL_CLOSED"` + the enumerated violation class — never raw values, never raw JSON, never raw text.

## 12. §16 strict allowlist schema (future implementation contract; fail-closed)

For every persisted field: wrong type / overlong value / unexpected key / malformed SHA / authority-event-attempt mismatch / role mismatch / output-name mismatch / launcher identity-version mismatch / impossible stage-class combination ⇒ validation FAILURE (fail closed; no raw fallback; no best-effort preservation).

| Field | Source producer | Type / bound | Allowed values / pattern | Required | Cross-check | Classification | Handoff-safe |
|---|---|---|---|---|---|---|---|
| `launcher` | boundary `:515` | str ≤ 64 | `NETWORKED-BOUNDARY-LAUNCHER-V1` | always | == binding identity | mechanical | yes |
| `launcher_version` | boundary `:110` | str ≤ 32 | generation-pinned finite set | always | == pinned version | mechanical | yes |
| `role` | boundary `:516` | str | `{AUDITOR_A, AUDITOR_B}` | always | == binding role AND == authority role | mechanical | yes |
| `event` | boundary `:516` | str ≤ 64 | `^evt-[0-9a-f]{16}$` | always | == binding event id | mechanical | yes |
| `attempt` | boundary `:516` | str ≤ 64 | `^evt-[0-9a-f]{16}-[AB]-[0-9]{2}$` | always | == binding attempt id | mechanical | yes |
| `output_name` | boundary `:538` | str ≤ 256 | == `f"{attempt}.first-pass-report.json"` | always | == binding output name | mechanical | yes |
| `staging_dir` | boundary `:535` | str ≤ 512 | == `ROOT/attempts/<attempt>/staging` | always | == driver plan staging path | mechanical | yes |
| `invocation_sha256` | boundary `:533` | str = 64 | `^[0-9a-f]{64}$` | always | == sha256(binding canonical compact invocation) | mechanical | yes |
| `auditor_executable_inode_checked` | boundary `:525` | bool | true on completed form | completed | — | mechanical | yes |
| `auditor_executable_is_frozen_package_payload` | boundary `:531` | bool | expected true | completed | role-derived expected path | mechanical | yes |
| `credential_printed` | boundary `:517/:571` | bool | `{false}` | always | true ⇒ fail-closed escalation | mechanical attestation | yes |
| `client_returncode` | boundary `:558` | int | −64…255 | completed | semantics = composition status (see `client_exec_reached`) | mechanical | yes |
| `report_present` | boundary `:560` | bool | — | completed | contradiction check vs EBS report_state | mechanical | yes |
| `elapsed_seconds` | boundary `:561` | float ≤ 3 dp | 0.0…(timeout+60) | completed | ≤ binding auditor_timeout + margin | mechanical | yes |
| `client_exec_reached` | future boundary (11.1) | bool | — | completed (future gen) | rc=0 ⇒ must be true; token ⇒ false | mechanical | yes |
| `inner_failure_class` | future boundary (11.1) | null / enum | `{INNER_SETUP_FAILED, INNER_EXEC_FAILED}` | completed (future gen) | non-null ⇒ client_exec_reached false | mechanical | yes |
| `exec_status_transport` | future boundary (11.1) | enum | `{READ, GRACE_EXPIRED_UNDETERMINED}` | completed (future gen) | — | mechanical | yes |
| `error_class` (derived) | driver, from `error` | enum | `{ARGV_CONTRACT_INVALID, LAUNCHER_FAILURE, NONE}` | always | rc=2 ⇒ ARGV_CONTRACT_INVALID; rc=3 ⇒ LAUNCHER_FAILURE; else NONE | mechanical (raw text NEVER persisted) | yes |

Impossible-combination checks (all ⇒ fail-closed rejection): `error_class ≠ NONE` with rc ∉ {2,3}; rc=2 with `error_class ≠ ARGV_CONTRACT_INVALID`; rc=3 with `error_class ≠ LAUNCHER_FAILURE`; completed form missing any required field; `report_present=true ∧` EBS `report_state=REPORT_MISSING`; `client_exec_reached=false ∧ rc=0`; `client_exec_reached=true ∧ inner_failure_class ≠ null`. Confidentiality: every field is a trusted-mechanics scalar; no field can carry model text, report bytes, credential material or prompt text. No raw metadata JSON, no raw stdout/stderr, no arbitrary `error` string is ever persisted.

## 13. §17 blindness / non-substantive invariant

The schema contains ZERO report-substance, prompt, credential or provider-output fields and remains fully useful when all audit-report substance is sealed. The Auditor-A frozen report (`ba8a29a1…`/23727/0444) was referenced by identity only and NEVER opened. The future mechanism likewise persists only finite tokens and booleans produced by trusted launcher mechanics.

## 14. §18 identity / blast-radius matrix

| Identity | Effect of the selected boundary revision | Classification |
|---|---|---|
| Boundary launcher SHA | CHANGES (the file is edited) | OBSERVED FACT (direct consequence) |
| Package MANIFEST rows — both roles | `boundary/networked-boundary-launcher.py` row (sha `2efb6660…`, 27719 B) exists in BOTH `package-auditor-a` and `package-auditor-b` manifests (verified in the EXEC-05 handoff manifest members) ⇒ both manifest SHAs CHANGE | OBSERVED FACT |
| Event package identities (A `87fd285e…` / B `072d0087…`) | CHANGE (package bytes include the boundary row) | OBSERVED FACT (structure) + REQUIREMENT (recompute at future preparation) |
| Binding files / canonical digests (A `5204d90e…`/`4adb47a7…`, B `489a3c91…`/`7846ad8e…`) | CHANGE (bindings pin `boundary_launcher.sha256` = `2efb6660…`, verified in `binding-auditor-b.json`) | OBSERVED FACT (pin exists) + REQUIREMENT (regenerate) |
| EBS package / manifest (`d683f64d…`/`d42aa9e3…`) | UNCHANGED — `bootstrap-supervisor` contains NO boundary-launcher bytes (only inert test fixtures `tests/fixtures/inert_*boundary_launcher*.py`); no EBS source is touched by this design | OBSERVED FACT |
| Prompt contract `cc6ec29d…` | NOT forced to change (template render inputs are event_id + coverage boolean rule, not the boundary sha) — MUST be re-verified at future preparation | INFERENCE + REQUIREMENT |
| Frozen audit target `d4d584ff…` (qh `5b8d5e54…` + skill `c792933a…`) | UNCHANGED | OBSERVED FACT |
| Successor event id `evt-79182989824ce966` | The declaration formula excludes package hashes (recorded Control Room fact: `SHA256("AUCDEV-023-S1-EVENT-DECLARATION-V1|isakli05/audit-council-dev|d4d584ffa47…|2026-09-22")`, successor readback :90) so the ID itself is not forced to change by a boundary edit; HOWEVER attempts `-A-01`/`-B-01` are TERMINAL/CONSUMED and a same-event NEW attempt is NOT EXPRESSIBLE under the frozen EBS attempt derivation (recorded Control Room fact, EXEC-02 readback) ⇒ any future first-pass requires a NEW EVENT generation with fresh identities, full successor-package preparation, Control Room readback and a NEW explicit execution authority — the boundary revision necessarily rides that regeneration | RECORDED CR FACT + REQUIREMENT (nothing granted by this session) |
| EXEC-05 driver / wrapper / attempt state / accounting | UNCHANGED by this design (driver revision belongs to the FUTURE launcher preparation under a new authority) | REQUIREMENT |
| Deployed event / historical backup | UNCHANGED | OBSERVED FACT (verified read-only this session) |

## 15. §19 EBS change barrier

`EBS_CHANGE_NOT_REQUIRED` — CONFIRMED (§4): the EBS already transports parsed values intact, and every enforcement the design needs (allowlist validation, cross-checks, transport verdict derivation) lives in the future driver; the boundary revision keeps emitting the same one-line stdout JSON the EBS already parses. No EBS byte is to change.

## 16. §20 options / rejection record

| Option | Resolves | Does NOT resolve | Trust-boundary change | Blast radius | Blindness | Scope | Verdict |
|---|---|---|---|---|---|---|---|
| **A — driver-only allowlist of existing parsed values** | The observed B value loss (14 keys → values) | D-vs-E (source-proven collision); channel contamination (client stdout can silently destroy ALL metadata — the inferred Auditor-A mode) | none (driver only) | launcher/evidence plane only | preserved | smallest, but leaves the RB-001 invariant unmet | **REJECTED — INSUFFICIENT (§12 conditions 2 and 3 FAIL)** |
| **B — driver allowlist + minimal boundary structural tokens + channel isolation** (selected) | Value preservation; D-vs-E via `client_exec_reached`/`inner_failure_class`; metadata reliability via DEVNULL isolation | WHY a reached client exited nonzero (client/provider-internal — out of scope by authority); timeout-path metadata (separately marked by `timed_out`) | boundary launcher + INNER (declared TCB component, design revision S32) + both package/binding identity regenerations; NO EBS, NO client | packages/manifests/bindings (§14); rides the required future new-event generation | preserved (finite tokens/booleans only) | bounded, spec-complete (§11) | **SELECTED — smallest option that actually closes RB-001's demonstrated invariant** |
| **C — broader EBS / raw-output capture** | Would expose raw streams | — | EBS (protected remediated tree, 520-test requalification) + evidence plane | EBS package identity + event packages | VIOLATED (raw auditor/provider output must never be durable mechanical evidence) | large | **REJECTED — conflicts with the granted authority and is unnecessary given B** |
| Sub-variant: dedicated metadata fd | channel isolation | — | EBS `_child_setup` fd-contract change | EBS tree | preserved | — | **REJECTED (EBS blast radius; DEVNULL suffices)** |
| Sub-variant: staging marker file as exec-reach proof | exec-reach | — | boundary | packages | preserved | — | **REJECTED — client-forgeable (client writes `/auditor-output`); not process-bound** |

## 17. §21 acceptance invariant for the future implementation

**Falsifiable invariant:** after the future remediated generation is implemented, prepared, read-back and executed under its own explicit authority, for ANY first-pass attempt that terminalizes with `report_state ≠ REPORT_FROZEN` or `returncode ≠ 0`, the generated-LAST mechanical handoff ALONE — with ZERO raw client stdout/stderr, ZERO report bytes (when absent), ZERO credential material — lets the Control Room mechanically determine: (i) whether the EBS exec'd the frozen boundary launcher (`exec_failed`, rc=98 class A); (ii) whether the boundary completed outer deterministic setup or refused at the argv contract / outer exception (rc=2 / rc=3 + `error_class`); (iii) whether the composition reached the auditor-exec transition (`client_exec_reached`, `inner_failure_class`); (iv) whether the auditor client itself returned nonzero, and which value (`client_returncode` with `client_exec_reached=true`); (v) whether a report existed when the boundary completed (`report_present`, cross-checked against the EBS report lifecycle); (vi) whether the validator was reached (EBS `report_state` ∈ REPORT_MISSING / REPORT_SCREEN_FAIL / REPORT_INVALID / REPORT_FROZEN with pinned snapshot identity); (vii) the exact finite structural failure class overall. **Intentionally-impossible residual distinctions, stated explicitly:** WHY a reached client exited nonzero (client/provider-internal cause — would require raw provider output, outside RB-001 and outside the evidence-plane rules); metadata of a timeout-killed attempt (EBS discards it by construction and marks `timed_out=true` — its own terminal class, not an RB-001 gap); exec-status after a grace-expired read (`GRACE_EXPIRED_UNDETERMINED`, fail-closed and recorded honestly).

## 18. §22 design-only test plan (specified, NOT executed)

All synthetic, zero-provider, zero-network cases against the FUTURE implementation (mock INNER/clients only): (1) valid full metadata schema accepted; (2) unexpected key rejected; (3) wrong type rejected; (4) oversize value rejected; (5) malformed SHA rejected; (6) authority/event/attempt mismatch rejected; (7) role mismatch rejected; (8) output-name/staging-dir/invocation-sha cross-check mismatch rejected; (9) rc=2 argv-refusal form classified B; (10) rc=3 outer-exception form classified C with `error_class=LAUNCHER_FAILURE` and raw repr NOT persisted; (11) INNER pre-exec setup failure → token `b"I"` → class D/INNER_SETUP_FAILED; (12) INNER `execv` failure → token `b"X"` → class D/INNER_EXEC_FAILED; (13) successful exec + mock client rc=1 + no report → `client_exec_reached=true`, class E, values persisted; (14) successful exec + rc=0 + no report → class F; (15) rc≠0 + report present → class G; (16) report-present path through validator REPORT_INVALID/REPORT_FROZEN → class H separation; (17) arbitrary mock-client STDOUT emitted → never durable, metadata still CLEAN (isolation proof); (18) arbitrary mock-client STDERR emitted → never durable; (19) generated-LAST handoff contains ONLY sanitized allowlisted metadata (byte scan for mock stdout/stderr canaries = zero); (20) zero credentials/report bytes/provider text in every evidence surface (canary scan); (21) CLOEXEC semantics: fd closes exactly at successful `execve` (zero-byte EOF), token survives INNER exception paths, fd NOT closeable by the post-exec client image; (22) `pass_fds` inheritance through the vendored bwrap into INNER; (23) grace-expiry path yields `GRACE_EXPIRED_UNDETERMINED` fail-closed; (24) killed-by-signal composition yields `client_exec_reached=false` via negative rc; (25) impossible-combination rows each rejected fail-closed; (26) METADATA_OVERSIZE fallback still parses as valid minimal JSON.

## 19. §23 canonical design disposition

**`MINIMAL_BOUNDARY_STRUCTURAL_REMEDIATION_REQUIRED`** — because: (1) the EBS already transports parsed values intact, so the loss is not an EBS defect; (2) the observed value loss sits at the driver (`:1798`) and is necessary-but-not-sufficient to fix; (3) INNER/composition pre-client failure and a genuinely-executed client nonzero exit are SOURCE-PROVEN indistinguishable in the `rc≠0 ∧ report_present=false` cell (exactly Auditor-B's terminal cell), so no driver-only change can satisfy §11; (4) the shared stdout channel makes even parsed metadata survival contingent on uncontrolled client stdout (the inferred Auditor-A mode), so the acceptance invariant additionally requires composition-stdout isolation. The minimum remediation is therefore: **exec-status CLOEXEC pipe + `client_exec_reached`/`inner_failure_class`/`exec_status_transport` tokens + `launcher_version` bump + composition stdout/stderr → DEVNULL + driver strict-allowlist persistence — all boundary/driver-level, with `EBS_CHANGE_NOT_REQUIRED`.** RB-001 remains **OPEN at DESIGN strength**; nothing was implemented; no replacement execution is authorized.

## 20. Attestations

ZERO implementation; ZERO auditor/provider/frontier execution; ZERO network or provider probe; ZERO credential read (the credential fd contract was read as SOURCE only); ZERO report-substance read (Auditor-A frozen report never opened; ZERO first-pass report bytes exist in any surface this session produced); ZERO mutation of EXEC-05 attempt/accounting state, deployed successor event, historical EXEC-03 backup, EXEC-05 launcher, EBS, boundary-launcher bytes, or successor packages/bindings/manifests; ZERO new event/attempt creation; ZERO replacement execution authority granted; ZERO qualification/installation. The only writes by this session are the three canonical governance paths and the generated-LAST design handoff.
