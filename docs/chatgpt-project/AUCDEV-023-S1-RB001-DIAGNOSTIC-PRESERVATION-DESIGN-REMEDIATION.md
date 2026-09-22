# AUCDEV-023 S1 — RB-001 DIAGNOSTIC-PRESERVATION DESIGN REMEDIATION + EVIDENCE COMPLETION

- **Authority (operator-granted, design-remediation + evidence-completion only):** `AUCDEV-023-S1-RB001-DESIGN-REMEDIATION-EVIDENCE-COMPLETION-20260922-01`
- **Target finding (unchanged, never rewritten):** `AUCDEV023-CR-S1-EXEC05-RB-001` = `AUDITOR_B_REPORT_MISSING_RC1_ROOT_CAUSE_NOT_PRESERVED_IN_MECHANICAL_HANDOFF` (COMPLETENESS LIMITATION / FAILURE-DIAGNOSTIC EVIDENCE GAP / OBSERVED FACT / ROOT_CAUSE_UNRESOLVED / NO_PRODUCT_DEFECT_CONCLUSION_YET)
- **Predecessor design record (immutable):** `docs/chatgpt-project/AUCDEV-023-S1-RB001-DIAGNOSTIC-PRESERVATION-DESIGN.md` (Git blob `52e3b291d8d532d389ef78dd25a8129a76be79cd`), disposition `MINIMAL_BOUNDARY_STRUCTURAL_REMEDIATION_REQUIRED / EBS_CHANGE_NOT_REQUIRED / ZERO IMPLEMENTATION / RB-001 OPEN AT DESIGN STRENGTH`
- **Session role:** BOUNDED DESIGN REMEDIATOR + EVIDENCE-COMPLETION PUBLISHER ONLY. NOT Auditor-A/B, NOT an execution controller, NOT a replacement-execution / implementation / event-package-preparation / qualification / installation authority.
- **Activity class:** ZERO-RUNTIME / ZERO-AUDITOR / ZERO-PROVIDER design remediation + read-only evidence completion + deterministic synthetic design validation (local fixtures only) + canonical governance publication.
- **Date:** authority granted 2026-09-22; this record published 2026-09-23 (Europe/Istanbul; session began 2026-09-22 late evening).
- **RB-001 status after this record:** **OPEN at DESIGN-REMEDIATION strength.** The remediated design is specified and synthetically validated at design strength; ZERO implementation occurred; no replacement execution is authorized by this record.

---

## 1. Bootstrap verification (performed BEFORE design work)

- Live `origin/master` = `f36f36498aba497566dfe9ec9a1e72efc06d3ccd` = local HEAD (EXACT equality, 0/0 divergence after fetch; STOP-WITHOUT-MUTATION clause not triggered).
- Root tree `18b16b75abc9b5606158e16d4b45b00d02036c19`; sole parent `6e1f86c393708cef39eb1b80dbad97a23db18cc8` (both EXACT).
- Canonical blobs at the base, all EXACT: CURRENT-STATE `8baa38407b50b1e311d8b138bca53119a84364e8`; BACKLOG `f42b5d92d04ca7b8b46bed244a730ddb5d90f66e`; predecessor design record `52e3b291d8d532d389ef78dd25a8129a76be79cd`.
- Protected trees at the base, all EXACT and byte-unchanged by this session: `bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0` (the remediated EBS); `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`; `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f` (the latter two equal the frozen audit target `d4d584ffa47ad2848268ba947247f81a845b2322`).
- Tracked working-tree drift at bootstrap: only the long-known pre-existing `smoke-fixture`/`smoke-fixture-103` gitlink drift (outside every protected/docs path; preserved unstaged, unchanged by this session).

## 2. Read-only artifact identity verification (nothing executed)

| Artifact | Identity (re-hashed/verified by this session) | Status |
|---|---|---|
| EXEC-05 driver `aucdev023-firstpass-exec05.py` | SHA-256 `d4d1eca2baa3b8f50aa7f666986cf4d1e6ca4cf2bc09ea2dfe6feca503032357`, 117120 B, mode 0700 | EXACT, NOT executed, NOT altered |
| EXEC-05 wrapper `run-aucdev023-firstpass-exec05.sh` | SHA-256 `17e0abcd34303d0defda2326587cb80550872e8ebdb55b1055fb880e6d06534c`, 2836 B, mode 0700 | EXACT, NOT executed, NOT altered |
| Frozen boundary launcher (BOTH role packages) `event/package-auditor-{a,b}/boundary/networked-boundary-launcher.py` | SHA-256 `2efb666042e44d272a53f9ad4ac93a19c14f1687a33fb38ed84f9823d9bc44a7`, 27719 B, 578 lines — `cmp` byte-identical A↔B | EXACT, read-only, NOT altered |
| MANIFEST A / B | `2f8efbd65c930da9f6ab68b3921bf74961d0cb8eaf0324b0d14ef439107d8e8d` (191 file rows) / `15729d8bac5ee61f0c317c15fe9318100f942751802bb87e9f7a754ded9d7440` (194 file rows), schema `AUCDEV-023-EVENT-PACKAGE-MANIFEST-V5`; each contains EXACTLY ONE row `boundary/networked-boundary-launcher.py` = `2efb6660…`/27719 B; `package_sha256` A `87fd285e13fc2a6c8bfd5e64f7a642d3a275b302a2d77183d92d02814195b8c4` / B `072d0087f950bd7495d29685065133ee405e60876bc35fa26fe1f2100b4a406d` | EXACT, read-only |
| Binding A / B (non-secret, mechanical scalars only read) | `5204d90e451df4098423a0b4a9b4bd97859496dee1ad384da2e1c49f48a3efe3` / `489a3c911d00d109054e108fa0c89e878fa14f908e01f320022b6bbd1888ade4`; BOTH pin `boundary_launcher.sha256 = 2efb6660…` | EXACT, read-only |
| Remediated EBS source | `ebs/launch.py` SHA-256 `dfc63f0033aad802e5355e9dad652499d27a602122c7cfa1e2fa4d252947e9b7` (Git blob `063b6ce1f4c726bd6ba809f605a115511667fb09`, 1685 lines); `ebs/reportcustody.py` `e83b5d53d607f9e2a046146165cdf23de9319abe1e330e87ef1d4edf11826f59` (blob `18f1cc600c684e520b72026e0b4cdf8ba6287cb9`); `ebs/binding.py` (blob at protected tree) | read-only source analysis only |
| Invocation digests (recomputed this session from the bindings' canonical compact-JSON `auditor_invocation`) | B `48acda37d12524fd8246150410695238505c25bf2860c9f8718f57fa7222b371` (EXACT match to the recorded EXEC-05 invocation sha); A `6083b78d35ca6fae1c6805c3f5ae2e01cf35cbfe84d5bc398f9bc0ba313e3171` (newly recorded mechanical fact) | EXACT |
| Event-id derivation (recomputed this session) | `SHA256("AUCDEV-023-S1-EVENT-DECLARATION-V1|isakli05/audit-council-dev|d4d584ffa47ad2848268ba947247f81a845b2322|2026-09-22")[:16]` = `79182989824ce966` → `evt-79182989824ce966` EXACT (upgraded from recorded CR fact to independently recomputed OBSERVED fact) | EXACT |
| Auditor-A frozen report | identity only: `ba8a29a12867273616143e48a86f101f14f6e0e207136d83b31e7fd2426ec1a0` / 23727 B / 0444 | referenced mechanically ONLY; NOT opened, read, hashed, copied or packaged by this session |

## 3. Control Room readback findings — independent dispositions

### 3.1 `AUCDEV023-CR-S1-RB001-DESIGN-RB-001` — **CONFIRMED**

**Claim:** the predecessor design's rule *"zero bytes + EOF + client_returncode ≥ 0 → client_exec_reached: true"* produces a false positive when the composition (bwrap / python3 interpreter) fails BEFORE any trusted INNER code writes.

**Independent source-level reproduction (OBSERVED SOURCE FACTS):**
1. The write end of the proposed exec-status pipe is inherited by EVERY composition process (that is the mechanism). Its close is produced by ANY holder's process death, not only by CLOEXEC-at-execve. A bwrap that fails while constructing namespaces/mounts exits nonzero (host-analog observed in this session's synthetic validation: a namespace-construction failure exits `1` — and the earlier mis-composed analog reproduced exactly this cell) with ZERO bytes written → empty EOF + nonnegative rc.
2. A `python3` interpreter that fails to start inside the sandbox produces the same empty-EOF + nonnegative composition status.
3. INNER hard-killed before its first write produces the same observation.
4. Therefore the predecessor §11.1 proof sketch ("zero-byte EOF with rc ≥ 0 ⇒ the exec transition happened") fails the required "valid for every reachable predecessor failure path" test, and the rule would misclassify all of 1–3 as `client_exec_reached: true` — failing the central D-vs-E invariant the design exists to close.

**Remediation applied to the design (§5):** the handshake is corrected to an explicit three-token protocol in which SILENCE PROVES NOTHING POSITIVE — an explicit trusted `S` (INNER-entered) token and an explicit trusted `E` (execv-imminent) token precede the exec transition, and every token-bearing stream proves exec-reach FALSE unless `E` was written. Empty EOF now proves `PRE_INNER_COMPOSITION_FAILURE` (exec PROVEN_FALSE — see §5 proof sketch).

### 3.2 SIGNAL / PROCESS-DEATH AMBIGUITY — **CONFIRMED (the prior inference is REJECTED)**

**Claim:** the predecessor rule *"zero bytes + negative composition returncode → client_exec_reached: false"* is invalid because a negative composition status can ALSO occur after a successful exec.

**Independent determination (OBSERVED FACTS + honest residual):**
- A signal death INSIDE the sandbox can surface as the composition status in either convention: the HOST-bwrap analog probed deterministically in this session's validation reports a SIGKILLed sandbox child as exit code **137 (positive 128+9)**, and passes child exit codes through exactly (`exit 7 → 7`); whether the VENDORED bwrap self-signals (negative) instead is NOT derivable from the frozen binary bytes and is recorded as an implementation-time verification requirement.
- Therefore rc<0 alone cannot prove pre-exec position (bwrap itself signal-killed at ANY stage — including post-exec), and rc≥0 alone cannot exclude signal death (137 ≥ 0). **No rc-value inference is used anywhere in the corrected design.**
- Corrected semantics: exec stage is determined by TOKENS; rc<0 combined with the exec-imminent token `SE` yields the honest finite class `SIGNAL_EXEC_STAGE_UNDETERMINED` (exec UNDETERMINED, never guessed); token streams `""`/`S`/`SI`/`SEX` prove exec FALSE for ANY rc sign (see §5 proofs); `SE`+rc≥0 proves exec TRUE with the kill-window residual stated in §5.4.

### 3.3 `AUCDEV023-CR-S1-RB001-DESIGN-RB-002` — **CONFIRMED**

**Claim:** the predecessor §12 "always"-required field set contradicts the partial metadata shapes the launcher mechanically produces at rc=2/rc=3.

**Independent source-level reproduction (OBSERVED SOURCE FACTS, exact lines):**
- **rc=2 shape is exactly `{launcher, error:"ARGV_CONTRACT_INVALID"}`** (`:511-514`) — it does NOT contain `launcher_version`, `role`, `attempt`, `event`, `credential_printed` (all assigned only at `:515-517` AFTER the argv check) nor any progressive field. An "always-required" schema containing those keys would fail-closed exactly the variant it claims to classify.
- **rc=3 shapes are prefix-dependent**: the base 6-key dict (`:515-517`) is extended progressively at `:519/:521/:524→inode_checked/:531→frozen-payload flag/:533→invocation_sha256/:535→staging_dir/:538→output_name/:558→client_returncode`; an exception at ANY point yields that prefix + `error="LAUNCHER_FAILURE:{exc!r}"[:512]` (`:569-574`). Distinct mechanically-guaranteed sub-shapes exist at every assignment boundary, including the post-composition boundary (exception after `:558`).
- **Remediation applied:** the single schema is replaced by an outcome-specific DISCRIMINATED UNION (`V-*` variants, §6) with per-variant allowed/required/forbidden keys, discriminated by (EBS flags, rc, exact error token, key shape, exec tokens). Raw `error` text remains non-persistable (error_class only).

### 3.4 `AUCDEV023-CR-S1-RB001-DESIGN-RB-003` — **CONFIRMED**

**Claim:** the predecessor generated-LAST handoff (21 members; integrity-verified but content-sanitized) did not contain the exact complete non-secret bytes needed for independent source-level reproduction of the design's claims.

**Verification:** the EXEC-05 driver `build_handoff` (`:2160-2198`) packages evidence summaries, accounting JSONL, bindings and manifests — but NO driver bytes, NO wrapper bytes, NO boundary-launcher bytes, NO EBS source, NO invocation/profile metadata. **CONFIRMED.**

**Evidence completion (performed by this session):** the generated-LAST review handoff (§10) now contains exact complete NON-SECRET reviewer copies of: the EXEC-05 driver + wrapper; the frozen boundary launcher (one complete copy + mechanically demonstrated A/B byte-equality this session via `cmp`); both package MANIFESTs; both bindings; the exact EBS source files relied on (`launch.py`, `reportcustody.py`, `binding.py`) with their canonical Git blobs; both boundary sandbox profiles; the invocation-digest recomputation evidence; the design-validation suite + results; the failure-stage matrix, corrected protocol, variant schema and blast-radius matrix (embedded in this record, which is itself packaged); the publication diff and post-push readback evidence; the provenance inventory (every evidence file with source path, provenance class, SHA-256, size, disclosure-safety rationale and the design claim it supports). EXCLUDED (attested): credentials/credential-derived material, Auditor-A report bytes, any report substance, provider logs, raw auditor stdout/stderr, prompts with report substance, sealed/unread content, whole event/package trees (narrow files only), unsafe paths, symlinks, hardlinks, special files.

## 4. §4 exact-source re-verification results (standalone confirmations)

**A. EBS transport — RE-CONFIRMED (all claims re-verified at exact lines):** fd 1 = metadata pipe (`launch.py:984`); fd 2 = `/dev/null` opened **O_RDONLY** (`:1321`, `:985` — NEW OBSERVED SOURCE FACT: composition stderr writes fail `EBADF`; stderr was never a capture surface in any case); pipes nonblocking (`:1340-1341`); concurrent bounded drain with `METADATA_MAX=65536` (`:1378-1388`, `:150`); 0.5 s grace final drain (`:1389-1398`, `:151`); whole-buffer `json.loads` with silent `None` collapse (`:1447-1452`); `core=(exitcode, exec_failed, metadata or {})` (`:1453-1454`); the SAME dict through `AttemptResult.metadata` (`:1584`, `:1667-1670`); timeout kills the attempt group and returns `AttemptResult(…, {}, True, …)` — metadata discarded by construction (`:1429-1446`); `snapshot_staging()` → `None` settles REPORT_MISSING BEFORE the validator (`:1595-1600`; `reportcustody.py:48-59`). **`EBS_CHANGE_NOT_REQUIRED` STANDS.** No EBS byte was touched.

**B. Driver value-loss — RE-CONFIRMED against the COMPLETE driver:** the driver's ONLY consumption of `result.metadata` is `:1798` (`"metadata_keys": sorted(result.metadata or {})`); every downstream surface carries only that reduced summary: attempt summary `:1789-1838` → evidence member `04/05-attempt-*-summary.json` (`:1855-1856`) → `build_handoff` (`:2160-2198`). NEW OBSERVED SOURCE FACT (informational, out of the boundary-metadata path but recorded for the future driver revision): the driver's own failure-path summary persists `repr(exc)[:2000]` (`:1869`) — arbitrary exception text in the evidence plane; the future driver revision under this design SHALL apply the same finite-class sanitization to its own failure paths.

**C. Boundary composition/stdio — RE-CONFIRMED from the complete 578-line source:** `subprocess.run(args, pass_fds=(cred_r, inv_r), timeout=None)` (`:554-555`) with NO stdout redirection → bwrap, `python3 -c INNER` and (after `os.execv` `:260`) the auditor client all inherit fd 1 = the EBS metadata pipe; the launcher's single metadata line is written only AFTER `subprocess.run` returns (`:562-566`), so client stdout PRECEDES it in one buffer — the contamination loss mode (the source-consistent explanation of Auditor-A's observed `metadata_keys: []`, preserved as INFERENCE). INNER has no exception handler and no distinct exit code (`:228-261`). Corrected minimal channel isolation: **`stdout=subprocess.DEVNULL` on the composition only** (fd 1); stderr left INHERITED — the existing fd 2 is already the EBS-provided O_RDONLY `/dev/null` (zero behavioral change; a writable-DEVNULL normalization is recorded as an available but NOT required option). Nothing the evidence contract requires is lost: client stdout/stderr were never legitimate evidence inputs and must never be persisted.

## 5. Corrected handshake protocol (design v2 — "three-token CLOEXEC exec-status handshake")

### 5.1 Mechanism

- The OUTER launcher creates the exec-status anonymous pipe as the FIRST fd-allocating operation of `main()` and normalizes the WRITE end to the FIXED inherited fd `EXEC_STATUS_FD = 8` (fd 7 read-end relocation handled defensively; fds 3-6 are occupied by the EBS child contract `:129-131`, so 7/8 are the first free pair — deterministic numbering; the data memfds are created afterwards as today).
- `subprocess.run(args, pass_fds=(cred_r, inv_r, 8), stdout=subprocess.DEVNULL, timeout=None)`.
- INNER (revised embedded trusted bootstrap), in EXACT order:
  1. `os.set_inheritable(8, False)` — FD_CLOEXEC (survives fork, closes exactly at execve);
  2. write `b"S"` — INNER-ENTERED (trusted producer);
  3. ALL existing setup under `except BaseException:` → write `b"I"` (INNER-SETUP-FAILED), re-raise (uncaught → exit 1);
  4. write `b"E"` — EXECV-IMMINENT, immediately before the exec call with nothing in between;
  5. `os.execv(...)`; on `BaseException` → write `b"X"` (INNER-EXEC-FAILED), re-raise.
- OUTER, immediately after `subprocess.run` returns and INSIDE the existing try (so later exceptions still preserve the tokens in metadata): **close its own write end FIRST** (ordering requirement — otherwise EOF can never be observed), then a bounded nonblocking read of the read end (≤ 0.5 s grace, cap 3 bytes; more-than-3 bytes observed = `EXEC_STATUS_PROTOCOL_VIOLATION`, distinct from grace expiry), then close; assign `exec_status_tokens` / `exec_status_transport` / `client_exec_reached` / `exec_stage_class` into `metadata` immediately after `client_returncode` (BEFORE `report_present`).
- Token grammar (CORRECTED DURING THIS SESSION'S SYNTHETIC VALIDATION — see §8): valid streams are EXACTLY `""`, `"S"`, `"SI"`, `"SE"`, `"SEX"`; `"SX"` is UNREACHABLE by construction (E always precedes X) and any other byte sequence or length > 3 is a protocol violation. 1-byte pipe writes are atomic (≤ PIPE_BUF) and durable once written.

### 5.2 Finite classification table (tokens × rc-sign)

| Token stream | Composition rc | `exec_stage_class` | `client_exec_reached` |
|---|---|---|---|
| `""` | any | `PRE_INNER_COMPOSITION_FAILURE` | **PROVEN_FALSE** |
| `"S"` | any | `INNER_STARTED_ABNORMAL_DEATH` | **PROVEN_FALSE** |
| `"SI"` | any | `INNER_SETUP_FAILED` | **PROVEN_FALSE** |
| `"SEX"` | any | `INNER_EXEC_FAILED` | **PROVEN_FALSE** |
| `"SE"` | ≥ 0 | `CLIENT_EXECUTED` | **PROVEN_TRUE** (residual §5.4) |
| `"SE"` | < 0 | `SIGNAL_EXEC_STAGE_UNDETERMINED` | UNDETERMINED |
| no EOF within grace | any | `EXEC_STATUS_UNDETERMINED_GRACE_EXPIRED` | UNDETERMINED (fail-closed) |
| grammar/oversize violation | any | `EXEC_STATUS_PROTOCOL_VIOLATION` | UNDETERMINED (fail-closed) |

### 5.3 Proof sketches (trusted producer named for every claimed transition)

- **Trusted producer:** INNER is the ONLY writer of fd 8 before exec (the outer closed its copy before reading; bwrap and the interpreter never write it; after a successful execve the client holds NO write end — CLOEXEC closed it; the client runs inside `--unshare-pid` bwrap with namespace-local `/proc` and cannot reach the outer launcher's or bwrap's fd tables — the launcher is `PR_SET_DUMPABLE=0` `:264-269/:499`). Non-forgeable: anonymous pipe; fixed 1-byte tokens; no timing, no stdio parsing, no model text, no report content, no credential inference.
- **`""` ⇒ exec PROVEN_FALSE:** `execv` is called at exactly ONE site (INNER), strictly AFTER the `S` and `E` writes in program order; pipe writes complete atomically and remain readable in the pipe buffer after writer death; the outer drains to EOF (or grace) after the composition exits; therefore NO `S` byte ⇒ the exec call was never reached, for EVERY reachable predecessor failure path (bwrap pre-INNER failure, interpreter startup failure, pre-S hard kill). This closes the CR-DESIGN-RB-001 false positive.
- **`"S"` (no `E`) ⇒ PROVEN_FALSE:** the `E` write strictly precedes the exec call; no `E` ⇒ exec not invoked; the death between S and E was not an exception (handlers write `I`), i.e. an uncatchable kill/abort — recorded as `INNER_STARTED_ABNORMAL_DEATH`.
- **`"SI"` / `"SEX"` ⇒ PROVEN_FALSE:** trusted handler tokens written by INNER immediately before the re-raised failure.
- **`"SE"` + rc≥0 ⇒ PROVEN_TRUE:** every pre-exec failure path provably writes a further byte (`I`/`X`) or dies before `E` (`"S"`/`""`); the only remaining producers of EOF-after-`E` are (a) CLOEXEC close at a successful execve, and (b) an uncatchable kill in the microscopic `[E, execve]` window whose composition status must additionally surface nonnegatively.
- **rc=0 ⇒ client executed and exited 0** (source control flow: the composition status is the sandbox tree's status; INNER cannot exit 0 without a successful execve; execv failure exits 1) — used ONLY as a cross-check (a KNOWN exec stage other than `CLIENT_EXECUTED` at rc=0 is an impossible combination, rejected fail-closed), never to override tokens; UNDETERMINED stages (grace/violation) do not contradict rc=0 and are accepted honestly.

### 5.4 Residual ambiguity (stated honestly, ACCEPTED RESIDUAL)

1. **Kill-window residual:** an uncatchable (SIGKILL-class) termination in the `[E, execve]` window classified with (a) is misclassified `CLIENT_EXECUTED`. Bounded to a few syscalls; requires an external hard kill at that exact point; characterized precisely at implementation time by the mandatory vendored-bwrap probes (§8). NOT closable without kernel support (no atomic write+exec exists).
2. **Pre-INNER 4-vs-5 indistinguishability:** bwrap-construction failure vs interpreter-startup failure are mutually indistinguishable in the mechanical evidence plane (both `""`, nonnegative rc); distinguishing them would require capturing composition stderr — REJECTED (raw output non-persistable; and unnecessary for the D-vs-E invariant: both prove exec FALSE).
3. **WHY a reached client exited nonzero:** client/provider-internal cause — out of RB-001 scope by authority.
4. **Timeout metadata:** discarded by EBS construction (`launch.py:1445`) and separately marked `timed_out=true` — its own terminal class, not an RB-001 gap.
5. **Vendored-bwrap conventions** (fd passthrough; child-signal-death exit convention): NOT derivable from frozen binary bytes; host-bwrap analog CONFIRMED this session (§8); the vendored-binary equivalents are mandatory implementation-time fixtures.

## 6. Corrected outcome-specific variant schema (discriminated union; fail-closed)

Discriminator chain: EBS flags (`exec_failed`, `timed_out`) → transport verdict (parse) → rc → exact `error` token → key-shape → exec tokens. The complete normative specification (per-variant allowed/required/forbidden keys, types, bounds, identity cross-checks, impossible combinations, sanitization) is the reference model implemented and validated by `aucdev023-rb001-design-remediation-evidence/design-validation-tests.py` (SHA-256 `6a73b002d242f1cbcb90489929455ad07f56c99826143622be678a018b7c90be`); its validator is the implementation contract. Summary of variants:

| Variant | Discriminator (exact) | Key shape (exact) | exec reach | Handoff-safe |
|---|---|---|---|---|
| `V-EBS-EXEC-FAILURE` | `exec_failed=true` (rc 98, `launch.py:1001-1006`) | metadata `{}` | PROVEN_FALSE | yes |
| `V-TIMEOUT` | `timed_out=true` (metadata discarded `:1445`) | metadata `{}` | UNDETERMINED_TIMEOUT | yes |
| `V-TRANSPORT-FAILURE` | unparseable/empty buffer (post-isolation residual; fail-closed) | — (`metadata_transport=UNPARSEABLE_FAIL_CLOSED`) | UNDETERMINED | yes |
| `V-ARGV-REFUSAL` | rc=2 ∧ `error=="ARGV_CONTRACT_INVALID"` | EXACTLY `{launcher, error}` | PROVEN_FALSE | yes |
| `V-OUTER-PRE-COMPOSITION` | rc=3 ∧ no `client_returncode` | base-6 + contiguous progressive prefix + `error` | PROVEN_FALSE | yes |
| `V-OUTER-POST-COMPOSITION` | rc=3 ∧ `client_returncode` present | prefix incl. `client_returncode` (+ exec keys if read) | token-determined | yes |
| `V-METADATA-OVERSIZE` | `error=="METADATA_OVERSIZE"` (any rc ∉ {2,3}) | EXACTLY `{launcher, error}` | UNDETERMINED (values lost by fallback) | yes |
| `V-COMPOSITION/<exec_stage_class>` | rc ∉ {2,3}, clean parse | full 14-key (present gen) / 18-key (future gen) shape | per §5.2 table | yes |

Identity cross-checks (every PRESENT key, before equality: type + length bound + sha grammar): `launcher` ≤64 == binding identity; `launcher_version` ≤32 == generation-pinned version (present `S1-PREP002-REM2-1`; future `S1-PREP002-REM2-2`); `role`/`event`/`attempt` ≤64 == binding (+pattern); `output_name` ≤256 == binding; `staging_dir` ≤512 == driver plan path; `invocation_sha256` == sha256(binding canonical compact invocation). Impossible combinations (each rejected fail-closed): rc=2 with any other key set; rc=2/rc=3 with wrong error token; rc=3 without `error`; rc=3 non-prefix progressive shape; `error` key at rc ∉ {2,3} (except the exact `METADATA_OVERSIZE` variant); rc=0 with a KNOWN exec stage ≠ `CLIENT_EXECUTED`; token/class/reached triple inconsistency (including unreachable `"SX"`); `credential_printed=true` (fail-closed escalation); `report_present` contradicting EBS `report_state`; `timed_out`/`exec_failed` with nonempty metadata; non-dict metadata. Sanitization: the raw `error` string is NEVER persisted — only `error_class ∈ {ARGV_CONTRACT_INVALID, LAUNCHER_FAILURE, METADATA_OVERSIZE, NONE}`; exec tokens are ≤3 ASCII bytes; every persisted field is a trusted-mechanics scalar; no raw metadata JSON, no raw stdout/stderr, no arbitrary exception text, no report bytes, no credential material, no provider text is ever durable.

## 7. Driver persistence structure (future revision; replaces `:1798`)

Persist per attempt: `metadata_keys` (continuity) + `metadata_transport ∈ {CLEAN_JSON_PARSED, NOT_PRODUCED_EXEC_FAILED, DISCARDED_ON_TIMEOUT, UNPARSEABLE_FAIL_CLOSED, OVERSIZE_FALLBACK}` + the validated variant + the per-variant allowlisted `boundary_metadata` object + `error_class`. On ANY validation failure: keys-only + `metadata_schema_validation: "REJECTED_FAIL_CLOSED"` + the enumerated violation class — never raw values, never best-effort fallback. The future driver revision SHALL additionally sanitize its own failure-path exception repr (§4.B informational). Present-generation (`S1-PREP002-REM2-1`) records validate under the subset model (no exec keys; exec stage `LEGACY_NO_EXEC_STAGE`), preserving analysis of the historical EXEC-05 evidence.

## 8. Synthetic design validation (performed; DESIGN strength only)

`aucdev023-rb001-design-remediation-evidence/design-validation-tests.py` (SHA-256 `6a73b002…`; results `validation-results.json` SHA-256 `8c21b20f…`): **83/83 PASS, 0 FAIL** — protocol simulation 18 (incl. pre-INNER failure/exit-0/signal variants, INNER setup/exec failures incl. the corrected `"SEX"` stream, post-S abnormal death, exec+rc=0/rc=1, client signal death, kill-in-window, grace expiry, oversize-violation-vs-grace distinction, CLOEXEC-closes-at-execve fd proof, stdout-DEVNULL isolation + no-isolation negative control reproducing the Auditor-A loss mode, D-vs-E discrimination on the identical rc=1 cell, host-bwrap fd-passthrough CONFIRMED, host-bwrap exit-convention probe: child SIGKILL → composition rc **137** positive-128+n, child exit code exact passthrough); variant schema 58 (all valid forms incl. every rc=3 assignment-boundary prefix sub-shape and post-composition form; every rejection class incl. unreachable-stream claims, identity/type/bound/grammar mismatches, impossible combinations, rc=0 honesty rule); sanitization/canary 7 (raw exception sanitized; stdout/stderr/credential/report canaries absent from the persisted representation; persisted-key allowlist). All fixtures are local deterministic python3//bin/sh processes under a fresh tempdir; ZERO provider/client/model calls; ZERO network; ZERO real-attempt-namespace access. **The validation itself corrected the design**: the first reference-model pass retained an `"SX"` stream that construction makes unreachable (E always precedes X) and a 2-byte cap that rejected the real `"SEX"` exec-failure stream — both defects were caught by the fixtures and fixed; this is recorded as proof the validation is substantive, and as a reminder that the same fixtures are mandatory at implementation time. Fixture success is NOT an implementation claim; the vendored-bwrap fd-passthrough and exit-convention probes against the FROZEN package bytes are mandatory implementation-time requirements (host analog CONFIRMED only).

## 9. Identity / blast-radius recheck (from exact complete evidence)

| Identity | Effect of the corrected boundary revision | Classification |
|---|---|---|
| Boundary launcher SHA `2efb6660…` | CHANGES (file edited; `launcher_version` bump `S1-PREP002-REM2-2`) | OBSERVED FACT |
| MANIFEST A/B | each has EXACTLY ONE `boundary/networked-boundary-launcher.py` row (`2efb6660…`/27719 B — verified in both files this session) ⇒ both manifest SHAs CHANGE | OBSERVED FACT |
| Package A `87fd285e…` / B `072d0087…` | CHANGE (package bytes include the boundary row) | OBSERVED FACT (structure) + REQUIREMENT (recompute at future preparation) |
| Bindings A `5204d90e…`/B `489a3c91…` + canonical digests A `4adb47a7…`/B `7846ad8e…` | CHANGE (both bindings pin `boundary_launcher.sha256 = 2efb6660…` — verified in both files this session) | OBSERVED FACT + REQUIREMENT |
| EBS manifest/package `d683f64d…`/`d42aa9e3…` | UNCHANGED — `bootstrap-supervisor` carries NO boundary-launcher bytes (only `tests/fixtures/inert_*boundary_launcher*.py`; string references only in `ebs/binding.py`/tests); no EBS source is touched | OBSERVED FACT |
| Prompt contract `cc6ec29d…` | NOT forced to change (render inputs = event id + coverage rule; invocation argv embeds event/attempt ids, not package hashes) — MUST be re-verified at future preparation | INFERENCE + REQUIREMENT |
| Frozen audit target `d4d584ff…` (qh `5b8d5e54…` + skill `c792933a…`) | UNCHANGED | OBSERVED FACT |
| Event id `evt-79182989824ce966` | derivation formula recomputed EXACT this session (§2); excludes package hashes ⇒ not forced to change; HOWEVER the EBS attempt derivation is `attempt_id_for(event_id, role) = f"{event_id}-{A|B}-01"` (`ebs/binding.py:208-210`) and the loader REFUSES any other attempt id (`:388-393`) — UPGRADED from recorded CR fact to OBSERVED SOURCE FACT — and attempts `-A-01`/`-B-01` are TERMINAL/CONSUMED ⇒ same-event new attempts NOT EXPRESSIBLE ⇒ ANY future first-pass requires a NEW EVENT generation with fresh A/B identities + full successor preparation + Control Room readback + NEW explicit operator authority; the boundary revision necessarily rides that regeneration | OBSERVED FACT + REQUIREMENT (nothing granted by this session) |
| EXEC-05 driver/wrapper/attempt/accounting/deployed event/historical backups | UNCHANGED by this session | OBSERVED FACT |

## 10. Acceptance invariant (falsifiable; future implementation)

After the future remediated generation is implemented, prepared, read-back and executed under its own explicit authority, for ANY first-pass attempt terminalizing with `report_state ≠ REPORT_FROZEN` OR `returncode ≠ 0`, the generated-LAST mechanical handoff ALONE — with ZERO raw client stdout/stderr, ZERO report bytes (when absent), ZERO credential material — lets the Control Room mechanically determine: (i) EBS-exec of the boundary (class A / `V-EBS-EXEC-FAILURE`); (ii) argv-contract refusal vs outer setup failure, INCLUDING which progressive assignment prefix failed (rc=2/rc=3 variants); (iii) whether the composition reached INNER (`S`+), and if not, that exec is PROVEN_FALSE (D-class cell CLOSED); (iv) INNER setup failure (`SI`) vs exec failure (`SEX`) vs abnormal death (`S`); (v) whether the auditor-exec transition was reached and the client's own exit status (`SE`+rc, `CLIENT_EXECUTED`) — the historical D-vs-E collision cell is CLOSED for every non-signal path; (vi) report existence at boundary completion (cross-checked against the EBS lifecycle); (vii) validator reach and outcome (REPORT_MISSING/SCREEN_FAIL/INVALID/FROZEN + pinned identity); (viii) the exact finite structural class, with every inherently-ambiguous cell surfaced as an explicit UNDETERMINED/FAIL_CLOSED state (§5.4 residuals) rather than guessed.

## 11. Attestations + resulting state

ZERO runtime implementation; ZERO auditor/provider/frontier execution; ZERO network or provider probe; ZERO credential read (credential fd contract read as SOURCE only); ZERO report-substance read (Auditor-A frozen report never opened; zero first-pass report bytes in any surface this session produced); ZERO mutation of EXEC-05 attempt/accounting state, deployed successor event, historical backups, EXEC-05 launcher, EBS, boundary-launcher bytes, or successor packages/bindings/manifests; ZERO new event/attempt identities; ZERO package/binding regeneration; ZERO qualification; ZERO installation; ZERO replacement-execution authority granted. The only writes by this session are the three canonical governance paths, the untracked evidence directory `aucdev023-rb001-design-remediation-evidence/`, and the generated-LAST review handoff. Historical RB-001 classification and the predecessor design record are preserved verbatim and NOT rewritten; this record REMEDIATES the predecessor's design errors (CR-DESIGN-RB-001/-002/-003 all CONFIRMED and corrected) without altering its EBS/driver/loss-point determinations, which this session independently RE-CONFIRMED. `MINIMAL_BOUNDARY_STRUCTURAL_REMEDIATION_REQUIRED` remains the governing disposition, now with the corrected three-token handshake, discriminated-union schema and evidence-completion contract; `EBS_CHANGE_NOT_REQUIRED` STANDS (re-verified). **RB-001 remains OPEN — at DESIGN-REMEDIATION strength. NEXT ACTION EXACTLY ONE: CONTROL ROOM VERIFICATION OF THIS DESIGN-REMEDIATION + EVIDENCE-COMPLETION PUBLICATION BEFORE ANY IMPLEMENTATION AUTHORITY.**
