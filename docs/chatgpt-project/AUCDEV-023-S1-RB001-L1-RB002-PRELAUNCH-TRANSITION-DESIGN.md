# AUCDEV-023 S1 RB-001 L1 RB-002 — Prelaunch Transition Design (Executable-Mode Activation, Deployment, and Single-Use Replacement Execution-Authority Transition)

- **Publication date:** 2026-09-24 (Europe/Istanbul)
- **Design authority:** `AUCDEV-023-S1-RB001-L1-RB002-PRELAUNCH-TRANSITION-DESIGN-20260924-01`
- **Session class:** BOUNDED PRELAUNCH TRANSITION DESIGNER / READ-ONLY EVIDENCE COLLECTOR ONLY. This session DESIGNS — but does NOT perform — the executable-mode activation (chmod 0600→0700), the deployment transition, and the single-use replacement execution-authority transition for the Control-Room-accepted operator-launcher artifacts. This session is NOT the Control Room decision-maker, NOT the grant publisher, NOT the human operator granting execution, NOT the adaptation implementer, NOT an execution controller, NOT Auditor-A/B, NOT a deployment authority, NOT an attempt-creation authority, NOT a credential-custody authority, NOT a qualification authority, NOT an installation authority.
- **Zero-runtime attestation:** NOTHING in this task was chmod'd, deployed, staged, attempted, accounted, credential-read, gated, launched or executed. The driver was NEVER imported or executed (full read of the source bytes only). The wrapper was NEVER executed (full read only). NO execution authority was granted. Writing the future GRANT phrase inside THIS design record DOES NOT GRANT IT.

## 0. Design disposition

**`PRELAUNCH_TRANSITION_DESIGN_READY_FOR_CONTROL_ROOM_READBACK / FUTURE_OPERATOR_GRANT_REQUIRED_SEPARATELY / NO_AUTHORITY_GRANTED / NO_RUNTIME_MUTATION`**

No STOP condition was reached. Every Section-2 held state was re-verified read-only EXACT. The runtime-evidence provenance review (Section 11) closed with UNKNOWN = 0 and NO blocking defect: the invocation-marker grant-status clause is classified `EVIDENCE_REPORTING_PRECISION_RESIDUAL_NONBLOCKING` (Residual R-1), the lineage shorthand `INFORMATIONAL_LINEAGE_LABEL_ACCEPTABLE`.

## 1. Mandatory live bootstrap (verified EXACT)

Resolved live from GitHub (`git ls-remote origin master`) at session bootstrap:

| Identity | Value | Result |
|---|---|---|
| Live branch | `master` | EXACT |
| Live HEAD | `049b71c83309d1f5616a8ca2828a1fc8400b5042` | EXACT |
| Root tree | `8d1ea17c090559a0c1b7fcc5969358a5b79b31fe` | EXACT |
| Sole parent | `a2a28898ba77320b4e1eef362f8ced1cfc949864` | EXACT |
| Local HEAD | `049b71c83309d1f5616a8ca2828a1fc8400b5042` | EXACT (equals live) |
| Tracked working-tree drift vs HEAD | 0 paths | EXACT (untracked files only) |

Canonical blobs at that SHA (all EXACT):

| Record | Blob |
|---|---|
| `AUCDEV-CURRENT-STATE.md` | `ff376e5af137e4a327d3164e5f3b49fc690455d8` |
| `AUCDEV-BACKLOG.md` | `89d30c7cd96d86f834d47d7be1fabc3613b3e29d` |
| implementation Control Room readback | `c0ecfbdee63e253bf0b5f8f37588d6a617d7a40d` |
| implementation record | `c3876c38cb4b446ade7bd1376f749138a90c4384` |
| design-revision Control Room readback | `776a039a221a6d74bf98b17a4ccd8f59cd88f07a` |
| accepted successor-package Control Room readback | `83951286cf74b33e9836147f4d7656be6e76d257` |

Protected trees at that SHA (all EXACT): `bootstrap-supervisor` = `732b8def9f22d7c466ce77f3d3049da53bfff3d0`; `qualification-harness` = `5b8d5e5465923740470ff63ed9b8683f257a3787`; `skill` = `c792933a862d9a5434681a88d183470dd8b15d2f`. Pre-existing smoke-fixture gitlink drift preserved unstaged (outside every governed path).

Historical precedent blobs fetched and studied read-only (Section 4): `a4c61462849219e5811236095e721d2da9dcf8f4`, `aaadf32d18eb2f68793bcd554b029a1784c4fc9e`, `a4a0f7d5ce1a582d82b6e8a5adf1357b565b06a0`, `5694d2c526e83f0ca1c2a7271d1f6cf6312973d9` — all EXACT.

## 2. Held accepted state (re-verified read-only EXACT this session)

| Item | Identity | Verified |
|---|---|---|
| operator-launcher implementation | `ACCEPTED_AT_CONTROL_ROOM_FINAL_BYTES_READBACK_STRENGTH` | held |
| Driver `/home/isa/audit-council-dev/aucdev023-firstpass-rb001-l1-rb002-60636835.py` | SHA-256 `fd977a9d6c6b819d1d3af055fb3073ae2a01a00e5f2c665697056914d530b784` / 163646 B / mode 0600 / isa:isa / regular | EXACT |
| Wrapper `/home/isa/audit-council-dev/run-aucdev023-firstpass-rb001-l1-rb002-60636835.sh` | SHA-256 `3276742d4c18bd7b819107d51692f55252a13645d4bfa3632f6eb6d213b4b7b4` / 3408 B / mode 0600 / isa:isa / regular | EXACT |
| Wrapper frozen runtime condition | `REQUIRED_DRIVER_SHA256 = fd977a9d6c6b819d1d3af055fb3073ae2a01a00e5f2c665697056914d530b784`; `REQUIRED_DRIVER_MODE = 700` | runtime barrier CURRENTLY **CLOSED** (driver is 0600) |
| Fresh event | `evt-60636835d5fd6f37` PREPARED_ONLY / NOT_DEPLOYED / NO_RUNTIME_ATTEMPT | held |
| Fresh attempts | `evt-60636835d5fd6f37-A-01`, `evt-60636835d5fd6f37-B-01` | NOT STARTED / ABSENT (verified below) |
| Reserved future authority | `AUCDEV-023-S1-RB001-L1-RB002-FIRSTPASS-EXEC-20260924-01` = RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE | held; THIS design grants nothing |
| EXEC-RB-001 | OPEN / ROOT_CAUSE_UNRESOLVED | held |
| EXEC-RB-002 | CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH | held |
| Qualification / Installation | NONE / NONE | held |

## 3. Historical precedent — READ-ONLY, NON-TRANSFERABLE

The RB-001 L1 chain (readback `a4c61462…`, grant-prelaunch `aaadf32d…`, grant-prelaunch readback `a4a0f7d5…`, mechanical readback `5694d2c5…`) establishes the TWO-STAGE pattern as executed precedent: (1) the human operator's explicit GRANT canonicalized by a bounded grant/prelaunch session that, only after every read-only gate passes, applies chmod 0700 EXACTLY to driver+wrapper, re-hashes both (bytes unchanged), executes NEITHER, and publishes `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED`; (2) Control Room readback of that publication; (3) exactly one HUMAN-OPERATOR-DIRECT wrapper invocation. The historical authority `AUCDEV-023-S1-RB001-L1-FIRSTPASS-EXEC-20260923-01` is CONSUMED / TERMINAL / CLOSED / NO_RERUN and MUST NOT be revived or transferred; its invocation also produced the terminal A REPORT_FROZEN / B REPORT_MISSING outcome and left EXEC-RB-001 OPEN — precedent, NOT authority, and NOT a prediction of outcome.

## 4. Final driver/wrapper static contract (mechanically established read-only; NEVER imported/executed)

### 4A. Wrapper (82 lines read in full)

- **No CLI argument/authority override surface:** no `$1`/`$@`/`$*` anywhere; the only operator inputs are the two documented PATH-only credential-source env locators (Section 10), which the wrapper itself never reads, prints or hashes; `DRIVER`, `REQUIRED_DRIVER_SHA256`, `REQUIRED_DRIVER_MODE` are hardcoded (lines 44–46) and unreachable from any argument.
- **Exact driver SHA pin:** line 45 = `fd977a9d6c6b819d1d3af055fb3073ae2a01a00e5f2c665697056914d530b784`, enforced fail-closed lines 69–75.
- **Exact driver-mode requirement:** line 46 = `REQUIRED_DRIVER_MODE="700"`, exact-match enforced lines 63–68 (current 0600 → refusal → barrier CLOSED).
- **Root refusal** (lines 39–42); **owner check** uid==operator (57–62); **regular non-symlink check** (49–56).
- **xtrace disabled** (`set +x` line 32, never enabled; BASH_XTRACEFD/ZSH_XTRACEFD/SHELLOPTS/BASHOPTS unset line 35); **core dumps disabled** (`ulimit -c 0` fail-closed line 34); `set -euo pipefail`, `umask 077`.
- **Fixed PATH** pinned before any external call (`/usr/bin:/bin`, line 37); all utilities absolute-pathed.
- **Isolated Python exec:** PYTHONPATH/PYTHONHOME/PYTHONSTARTUP unset (line 80); `exec /usr/bin/python3 -I "$DRIVER"` (line 82) — NO arguments forwarded to the driver.

### 4B. Driver (3305 lines read in full; ast/import/execution NONE)

- `main()` (L3293) accepts NO arguments: `len(sys.argv) != 1` → REFUSED.
- `run_pipeline()` (L3244) order is EXACTLY: Phase 0 operator/host/repository checks (`phase0_operator_host_check`, L1191, incl. invocation-evidence-context creation BEFORE Git admission) → Phase 1 source verification (`phase1_verify_source`, L1462) → Phase 2 deployment (`phase2_deploy`/`deploy_generation`, L1606/L1514) → Phase 3 deployed re-verification (`phase3_reverify_deployed`, L1623) → Auditor-A one-shot attempt (`run_attempt_for_role(ctx,"A")`, L2697) → Auditor-B ONLY if A mechanically conforms (L3257 conditional AND the independent guard `AUDITOR_B_REFUSED_WITHOUT_CONFORMING_AUDITOR_A` at L2703) → Phase 6 mechanical barrier evidence (`phase6_mechanical_check`, L2851) → generated-LAST mechanical handoff (`build_handoff`, L2986, invoked in the `finally` so it is produced on EVERY terminal path once the evidence context exists).
- `create_invocation_evidence_context()` (L952) is NON-OVERWRITING: pre-existing `rb002-l1-run-evidence/<AUTHORITY_ID>/` → `EVIDENCE_CONTEXT_ALREADY_EXISTS_NON_OVERWRITING` refusal ("A SECOND invocation under authority … is refused"); `FileExistsError` race handled identically; created BEFORE any fail-able Git-admission check (L1222 vs L1230).
- Deployment occurs INSIDE the one wrapper invocation: `deploy_generation` is reachable ONLY from `phase2_deploy` ← `run_pipeline` ← `main` ← the single wrapper `exec`. No separate deployment entry point exists in the file.
- Attempt creation occurs only later inside `prepare_attempt()` (L1648, called from `run_attempt_for_role` L2709, after Phases 0–3).
- `AccountingStore` is created only inside `execute_one_shot_attempt()` (L1753, `AccountingStore.create` with O_EXCL semantics).
- Credential CONTENT is read only after the custody precondition: `establish_custody_precondition` (L1771, non-dumpable mechanically verified) precedes `make_credential_pipe` (L1777); the producer thread reads the source bytes ONCE at authorized-attempt start and writes exclusively into the EBS custody pipe; `resolve_credential_source` (L800) is METADATA-ONLY.
- Dynamic real gates run only through `Supervisor.run_attempt()` (single call site L1786; the Supervisor holds the runtime-gate fds; Phases 0/1 verify gate bytes/ROOT without executing gates); NETWORK_READINESS / RESOURCE_GATE are never executed by driver code.
- No retry/resume authority exists: `DriverStop` is fail-closed with `STOP_SUFFIX` ("DO NOT RE-RUN THIS AUTHORITY…"); phase-0 refuses any existing fresh-attempt root (`RETRY_REFUSED_ATTEMPT_*_ROOT_PRESENT`), any existing handoff (`HANDOFF_ALREADY_EXISTS`), any existing invocation context; `retry_authorized: false` everywhere; no loop/retry construct exists.

## 5. Deployment MUST remain inside the one human-direct wrapper invocation (mechanical proof)

`deploy_generation()` (L1514) classifies the destination via `classify_destination()` (L1494): `EXPECTED_HISTORICAL` / `ALREADY_NEW` / `UNKNOWN`(`UNKNOWN_ABSENT`). The ONLY authorized mutation case is `EXPECTED_HISTORICAL`. If ANY separate prelaunch task deployed the fresh generation first, the later authorized driver invocation would fail closed at TWO independent layers:

1. **Phase 0** (L1283–1290): the deployed root is classified read-only and must be `EXPECTED_HISTORICAL`, else `DEPLOYED_EVENT_NOT_EXPECTED_HISTORICAL_PREDECESSOR` STOP — an `ALREADY_NEW` destination fails here already.
2. **Phase 2** (L1537–1553): `classification == "ALREADY_NEW"` → `DESTINATION_ALREADY_NEW_GENERATION` STOP — "This driver does NOT silently treat an already-deployed new generation as authorization to continue."

A pre-deployment would therefore strand the granted authority: the mutation (deployment + non-overwriting backup creation) would already have happened under no grant surface, and the one authorized invocation would be mechanically unable to proceed or to resume (`ALREADY_NEW` is a refusal, NOT resume authority). **Therefore the correct lifecycle is NOT `activate → deploy → readback → execute`; it is** (Section 6): future explicit GRANT → bounded 0600→0700 activation ONLY → Control Room granted-prelaunch readback → exactly ONE human-operator-direct wrapper invocation which ITSELF performs deployment and the attempt lifecycle. No design alternative in this record pre-deploys.

## 6. Proposed future GRANT semantics — DESIGN ONLY (nothing granted here)

The exact human statement to be required later (ONLY as a future explicit human-operator message, after Control Room acceptance of THIS design):

```
GRANT AUCDEV-023-S1-RB001-L1-RB002-FIRSTPASS-EXEC-20260924-01
```

**Writing that phrase in THIS design record DOES NOT GRANT IT.** THIS task did NOT grant it (explicit confirmation: operator GRANT NONE).

The future grant must be defined as exact-target specific:

| Component | Exact identity |
|---|---|
| Driver | `fd977a9d6c6b819d1d3af055fb3073ae2a01a00e5f2c665697056914d530b784` / 163646 B |
| Wrapper | `3276742d4c18bd7b819107d51692f55252a13645d4bfa3632f6eb6d213b4b7b4` / 3408 B |
| Event | `evt-60636835d5fd6f37` |
| Attempt A | `evt-60636835d5fd6f37-A-01` |
| Attempt B | `evt-60636835d5fd6f37-B-01` |
| Model engagement budget | 2 TOTAL; Auditor-A FIRST; Auditor-B ONLY after a mechanically conforming Auditor-A |

Grant properties (one-shot, exactly as required): **one-shot; exactly one HUMAN-DIRECT wrapper invocation maximum; non-transferable; no-retry; no alternate attempts; no alternate driver/wrapper; no authority for qualification or installation.** A malformed or partial grant (wrong ID, wrong target identity, hedged phrasing) is NOT a grant; the grant/prelaunch session must present the exact target table and refuse on any mismatch (precedent: the RB-001 L1 GRANT-ID-001 identity-correction chain).

**Terminal rule:** ONCE the human-direct wrapper invocation has BEGUN (durable mechanical marker: creation of `rb002-l1-run-evidence/<AUTHORITY_ID>/` by `create_invocation_evidence_context`), a second invocation under the same authority is NOT permitted, regardless of whether a provider/model engagement was reached. The marker is non-overwriting and the driver refuses a second invocation outright; additionally any later re-invocation would independently fail closed at the phase-0 destination classification (`ALREADY_NEW`), the handoff-existence check, and the fresh-attempt-root checks. Any STOP/failure returns to Control Room. NO automatic retry is designed or permitted.

**State transition authorized by the future grant:** `RESERVED_IDENTITY_PROPOSED_ONLY / NOT_GRANTED / NOT_CONSUMED / NOT_EXECUTABLE` → `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED` (and, after the separately-gated prelaunch activation of Section 7, `DRIVER_WRAPPER_0700_ACTIVATED`). The grant authorizes EXACTLY: (a) one bounded chmod-only prelaunch activation of the two named artifacts; (b) one human-direct wrapper invocation whose internals perform deployment + the one-shot A/B lifecycle up to the 2-engagement budget. Nothing else — no second invocation, no alternate artifacts, no qualification/installation.

## 7. Future prelaunch activation — DESIGN ONLY (chmod-only, after the separate human GRANT)

A future GRANT/PRELAUNCH session, only AFTER the separate human GRANT exists and only AFTER Control Room acceptance of THIS design, may perform, in order:

1. **Mandatory live bootstrap** (resolve live `master` from GitHub; verify the then-current publication chain: the design readback → the grant publication; STOP on drift).
2. **Exact prepared driver/wrapper verification:** SHA-256 / size / owner / path / CURRENT mode 0600 for BOTH artifacts (`fd977a9d…`/163646/0600 and `3276742d…`/3408/0600, isa:isa, regular non-symlink), and wrapper pins `REQUIRED_DRIVER_SHA256 == fd977a9d…` and `REQUIRED_DRIVER_MODE == 700` present exactly as accepted.
3. **Exact package/source/historical-destination verification:** fresh source root `/home/isa/aucdev023-s1-rb001-l1-rb002-successor-package-prep-20260924-01/event` bindings `255dd7db…`/`d9de33cb…`, MANIFESTs `161faca0…`/`f6801960…`, runtime mode table 0555 (spot-verified this session at launcher/gate); deployed root classifying `EXPECTED_HISTORICAL` against the EXPECT_OLD pins (verified this session: bindings `ef0428c4…`/`4a97ced6…`, MANIFESTs `b9572520…`/`7fe23950…`, launcher `011a8713…` and gate `2794898065…` both packages).
4. **Exact fresh-namespace absence verification** (all verified ABSENT this session): `event.backup.pre-rb002-successor-event`, `event.staging.rb001-l1-rb002-60636835`, `attempts/evt-60636835d5fd6f37-A-01`, `attempts/evt-60636835d5fd6f37-B-01`, `rb002-l1-run-evidence`, `AUCDEV-023-S1-RB001-L1-RB002-FIRSTPASS-EXEC-20260924-01-MECHANICAL-HANDOFF.tar.gz`.
5. **Exact repository-lineage admission verification** (Section 8 facts, re-resolved live at prelaunch time).
6. **Credential SOURCE metadata/path admissibility ONLY:** lstat-only checks per the Section-10 contract (existence, exactly-one candidate per role, regular non-symlink, operator-owned, 1..65536 bytes) — WITHOUT opening or reading credential contents and WITHOUT hashing them.
7. **Only after every read-only gate passes:** `chmod 0700` EXACTLY the driver and the wrapper — NO other mode changes.
8. **Immediately re-hash both** and prove bytes unchanged (`fd977a9d…`/163646, `3276742d…`/3408 at mode 0700).
9. **Execute NEITHER artifact.**
10. **Publish the granted/not-yet-consumed prelaunch state** (docs-only fast-forward; exactly the canonical grant-prelaunch record + CURRENT + BACKLOG), no stronger than `GRANTED / NOT_YET_CONSUMED / EXECUTION_NOT_YET_STARTED / DRIVER_WRAPPER_0700_ACTIVATED`.
11. **Generate reviewer handoff LAST.**

No deployment. No attempt creation. No AccountingStore. No credentials opened/read. No dynamic gates. No boundary/auditor/provider execution. The barrier remains procedurally closed after activation: the ONLY permitted next step is Control Room readback of the granted-prelaunch publication, and then the single human-direct command (Section 9). No inference-capable controller may invoke the wrapper.

## 8. Repository-lineage contract (reproduced read-only at the current base)

The accepted final driver contains `SOURCE_TRUST_ANCHOR_COMMIT = 3058868416241d394cfaaa40cc585085db486f37` and the exact five pinned immutable record blobs (`9f7599fe…`, `578b58c8…`, `83951286…`, `7ba8910e…`, `776a039a…`). The driver intentionally admits canonical docs-only descendants of the anchor; THIS design does NOT propose changing the driver (later governance records existing is NOT a source-mutation reason — the lineage contract exists precisely to admit them).

Reproduced at base `049b71c…` (all facts the driver's `admit_repository()` will re-derive at invocation time): local HEAD == live origin/master EXACT; anchor IS an ancestor; **0** merge commits since anchor; committed path delta since anchor = exactly 4 paths, ALL under `docs/chatgpt-project/` (0 offending); protected trees EXACT (3/3); protected-path working-tree drift **0 rows**; all five pinned record blobs EXACT at HEAD.

**Result: `LINEAGE_ADMISSION_HELD` — the current base is admissible, and the grant/prelaunch publications (including THIS design publication) must remain docs-only fast-forward descendants touching ONLY `docs/chatgpt-project/` so the frozen driver admits them without source mutation.** The future prelaunch verification must reproduce these facts read-only immediately before the chmod step, and the future human-direct invocation re-derives them again at phase 0 and before each attempt.

## 9. Current destination / historical immutability gates (read-only, verified this session)

- Deployed event root `/home/isa/aucdev023-s1-prep002-rem002/event` = the exact historical generation `evt-f3136c29213a1d4d` (EXPECT_OLD pins verified: bindings `ef0428c4…`/`4a97ced6…` mode 0644; MANIFESTs `b9572520…`/`7fe23950…`; launcher `011a8713…` and RESOURCE_GATE `27948980653f4c0639041243d9f117087f0987c5cc53623abbfa39cbb143adaf` identical in both packages) → classifies `EXPECTED_HISTORICAL`; fresh source root classifies `EXPECT_NEW` (accepted fresh generation pins verified: `255dd7db…`/`d9de33cb…`/`161faca0…`/`f6801960…`, executables mode 0555).
- Historical predecessor attempts IMMUTABLE (verified): A `evt-f3136c29213a1d4d-A-01` accounting `5e3aac7cd73a89ab7031e9f586e456d1ad1ae5609e8e6f9cbc931ce9434fbfc7`/5617/0600 with terminal sequence `PREPARED → GATES_PASSED → CONSUMED_PRE_EXEC → EXEC_ATTEMPTED → REPORT_FROZEN → TERMINAL`; frozen report MECHANICAL IDENTITY ONLY `058a611f4b4b575ba1356d513e47c5585a30d012f70d0d4bb55211ed91dbe71f`/26314/0444 — substance NEVER opened (hash/stat only). B `evt-f3136c29213a1d4d-B-01` accounting `02d7c15dd0976c4c7bb5e219f8446fb13abb92f423a46d4403ab073700852c9c`/5482/0600 with terminal sequence `… → REPORT_MISSING → TERMINAL`; report remains ABSENT (0 found).
- All FOUR historical backups present: `event.backup.pre-successor-event`, `pre-exec03-new-event`, `pre-exec02`, `pre-rb001-l1-successor-event`.
- Required NEW backup target ABSENT (`event.backup.pre-rb002-successor-event`); future staging ABSENT; both fresh attempt roots ABSENT; future evidence root ABSENT; future execution handoff ABSENT. Attempts census: 22 entries, ZERO `60636835` roots.
- **Design rule:** if ANY unexpected path exists at prelaunch time, the prelaunch session does NOT normalize or delete anything — it returns a STOP disposition (`UNEXPECTED_RUNTIME_STATE_PRESENT`) to Control Room.

## 10. Credential locator contract — METADATA ONLY

The wrapper exposes PATH-only credential-source locators `AUCDEV_A_CREDENTIAL_FILE` / `AUCDEV_B_CREDENTIAL_FILE` with source-defined defaults; the wrapper itself never reads, prints or hashes them (they pass through the environment to the driver). Static resolution rules (`resolve_credential_source`, L800–846): env var set → that single PATH candidate (`source=environment`); else the single conventional candidate (`A: /home/isa/.claude/.credentials.json`, `B: /home/isa/.codex/auth.json`); EXACTLY ONE existing candidate required (0 or >1 → `CREDENTIAL_SOURCE_{role}_AMBIGUOUS_OR_ABSENT` fail-closed with an anti-retry factual note); lstat checks: NOT a symlink, regular file, operator-owned, size within 1..65536; the resolution record carries path/size/mtime ONLY — contents, and any content hash, NEVER enter any record. Content bytes are read exactly once by the pipe producer thread at authorized-attempt start, inside the already non-dumpable process, exclusively into the EBS custody pipe.

Host metadata (lstat ONLY, this session — never opened, never read, never hashed): `/home/isa/.claude/.credentials.json` exists, regular, isa:isa, mode 0600, 519 B (within bounds); `/home/isa/.codex/auth.json` exists, regular, isa:isa, mode 0600, 4231 B (within bounds); NO `AUCDEV_*_CREDENTIAL_FILE` override currently set (resolution will take the conventional candidates).

**Design rule:** the transition design does NOT broaden the credential surface. If a future override is ever required, it must be an EXPLICIT, prelaunch-reviewed PATH-only locator (env var set by the human operator at invocation time and recorded as metadata) — never a silently added locator, never a content-reading surface, never a copy into evidence. The prelaunch gate (Section 7 step 6) checks metadata admissibility only; this snapshot is time-of-design and MUST be re-verified at prelaunch time (Residual R-3).

## 11. Prelaunch runtime-evidence provenance review (UNKNOWN = 0; NO blocking defect)

### 11.1 Invocation-marker record field (`00-invocation-marker.json`, L988–991)

The human-readable record template reads:

> `RB-001 L1 FIRST-PASS INVOCATION EVIDENCE CONTEXT (RUN-002 pre-phase remediation; authority is RESERVED and NOT GRANTED until explicitly operator-granted)`

At actual invocation time the exact RB-002 authority will already be GRANTED (the invocation is only reachable after grant + activation + readback). Classification:

- **Lineage label "RB-001 L1 … (RUN-002 pre-phase remediation)":** `INFORMATIONAL_LINEAGE_LABEL_ACCEPTABLE` — the driver IS the adapted RB-001 L1 launcher (module docstring: "the adapted RB-001 L1 RB-002 successor launcher"); the label names launcher/remediation lineage, not the event or authority identity; it is corroborated by the truthful `[rb002-l1 …]` log prefix (L435), the truthful handoff README title "AUCDEV-023 S1 RB002-L1 FIRST-PASS EXECUTION (historical predecessor generation evt-f3136c29213a1d4d)" (L3057–3059) and the exact structured fields.
- **Grant-status clause "authority is RESERVED and NOT GRANTED until explicitly operator-granted":** `EVIDENCE_REPORTING_PRECISION_RESIDUAL_NONBLOCKING` (Residual R-1). Basis: (a) the "until" clause explicitly BOUNDS the not-granted state by the grant — after the grant the sentence remains a true description of the reservation protocol (the authority WAS reserved and not granted UNTIL the operator granted it; the invocation could not otherwise have occurred) and does not assert that no grant exists as of the invocation; (b) the marker carries the EXACT `authority_id` / `event_id` / `reserved_attempts` structured fields, so no readback ambiguity about WHO/WHAT can arise; (c) the grant state is independently established by the Control-Room-published granted-prelaunch record, which the readback reads alongside the marker; (d) the driver is deterministic ordinary Python with NO grant-verification logic — a frozen, temporally-bounded preparation-time formulation is the correct deterministic design, and the structured channel carries the operative identity; (e) NO wrong-campaign provenance is claimed (unlike the remediated OLA-DESIGN-001 EXEC05 case, where predecessor evidence would have been labeled with a false campaign name). It is a precision residual because a pedantic present-tense reading could read as stale; it is NON-BLOCKING because it cannot mislead a Control Room readback on identity, target or grant occurrence. NO source modification is proposed (the final bytes are Control-Room-accepted; this residual is recorded prospectively, like the 050-publication precision residual precedent).

### 11.2 Other future serialized/log/operator-visible static wording — inventory (all classified)

| Surface | Wording | Classification |
|---|---|---|
| `log()` prefix (L435) | `[rb002-l1 HH:MM:SS]` | TRUTHFUL (event-scoped) |
| phase-0 refusal tokens | `DEPLOYED_EVENT_NOT_EXPECTED_HISTORICAL_PREDECESSOR`, `HISTORICAL_PREDECESSOR_{role}_ACCOUNTING_ABSENT_REFUSED`, `HISTORICAL_PREDECESSOR_{role}_STATE_MUTATED_REFUSED`, `HISTORICAL_PREDECESSOR_A_REPORT_IDENTITY_REFUSED`, `HISTORICAL_PREDECESSOR_B_REPORT_MUST_REMAIN_ABSENT` | TRUTHFUL (remediated vocabulary) |
| serialized evidence keys | `historical_predecessor_{role}_accounting_sha256/_size/_state_sequence`, `historical_predecessor_A_report_identity`, `historical_predecessor_B_report_paths`, `historical_predecessor_state_immutable` | TRUTHFUL |
| deploy refusals | `DESTINATION_ALREADY_NEW_GENERATION`, `DESTINATION_UNKNOWN_REFUSED`, `DESTINATION_RECLASSIFIED_BEFORE_RENAME_REFUSED`, `BACKUP_DIR_EXISTS_NON_OVERWRITING`, `STAGING_DIR_EXISTS` | TRUTHFUL |
| handoff README (L3057–3074) | RB002-L1 title + correct historical-predecessor generation identity + custody/blindness statements | TRUTHFUL |
| `authority-summary.json` (L3080–3153) | exact authority/event/attempts, budget semantics, lineage model, pins | TRUTHFUL |
| marker `zero_state_at_creation` (L1001–1007) | deployment/accounting/credential/gate/auditor NONE, budget 0/2 | TRUE at creation time (created before any phase) |
| credential refusals (L818–841) | `CREDENTIAL_SOURCE_{role}_AMBIGUOUS_OR_ABSENT` + anti-retry factual note | TRUTHFUL |
| `STOP_SUFFIX` (L399) | "STOP. DO NOT RE-RUN THIS AUTHORITY…" | TRUTHFUL |
| `00-preflight.json` closed-authorities enumeration (L1428–1433) | "the EXEC-02, EXEC-03, EXEC-04 and EXEC-05 first-pass authorities are CLOSED / TERMINAL / NO RETRY / NON-TRANSFERABLE…" | TRUE HISTORICAL FACT (the accepted preserved set; EXEC-05's closure is factually correct) |
| barrier states (L383–397) | `BARRIER_CONDITIONS_SATISFIED_PENDING_CONTROL_ROOM_READBACK` / `CLOSED_PENDING_CONTROL_ROOM_MECHANICAL_READBACK` | MECHANICAL/TRUTHFUL |
| `deploy_generation` docstring (L1517) | "STRICT EXEC-04 classification" | SOURCE_DOCUMENTATION_ONLY — a docstring, never serialized into any runtime evidence surface (distinguished from serialized runtime evidence) |
| module docstring (L6–9) / L117 comment | "RESERVED FUTURE EXECUTION AUTHORITY, NOT YET GRANTED…" | SOURCE_DOCUMENTATION_ONLY — never serialized |
| driver stale-token census | `exec05` 0 / `EXEC05` 19 / `EXEC-05` 3 — reproduced this session EXACTLY the accepted Control Room-recorded remainder (18 `HISTORICAL_EXEC05_*` legacy internal identifiers, never serialized as provenance — accepted decision A; 3 true historical EXEC-05 facts incl. the preflight enumeration; 1 legacy-identifier documentation note) | ACCEPTED (no change) |

**Result: UNKNOWN = 0. NO runtime-generated evidence would assert a materially false CURRENT authority/event state. `PRELAUNCH_RUNTIME_EVIDENCE_PROVENANCE_DEFECT` did NOT occur.** No bounded source remediation is required before the grant.

## 12. Human-direct execution contract — DESIGN ONLY

If the eventual grant/prelaunch publication is independently accepted by Control Room, the ONLY proposed runtime invocation (quoted here; THIS task did NOT execute it and no agent/controller may):

```
cd /home/isa/audit-council-dev
./run-aucdev023-firstpass-rb001-l1-rb002-60636835.sh
```

No arguments (the driver refuses any). No inference-capable controller. No agent/controller standing authority. No automatic relaunch. No retry. The wrapper verifies the final driver identity/mode and then execs Python directly (`python3 -I`); the driver itself performs the deployment and the one-shot A/B lifecycle. THE RECORD QUOTING THIS COMMAND GRANTS NO AUTHORITY TO EXECUTE IT.

## 13. Post-deployment / failure semantics (explicit)

The driver deploys BEFORE Auditor-A (Phase 2 precedes Phase 4). Therefore:

- Deployment is an INTENDED mutation of the single human-direct invocation (not a prelaunch mutation).
- The historical predecessor `evt-f3136c29213a1d4d` moves to the fixed NON-OVERWRITING backup `event.backup.pre-rb002-successor-event` (created exactly once; existence pre-checked at phase 0 AND immediately before the rename layer).
- The fresh generation `evt-60636835d5fd6f37` becomes live via the verified-staging + atomic same-filesystem rename pair.
- Deployment is FULLY verified before Auditor-A (Phase 3 full reverify, pre-accounting and pre-credential).
- NO automatic rollback exists (none is designed; the driver has none; the historical backups are never touched).
- If a later preexec/attempt failure occurs, the deployed fresh generation MAY remain live; that is expected one-shot behavior, not a retry mechanism.
- A second invocation under the same authority is PROHIBITED (non-overwriting invocation context; plus independent `ALREADY_NEW`/handoff/attempt-root refusals).
- Any STOP returns to Control Room for evidence review with the generated-LAST mechanical handoff.
- `ALREADY_NEW` on a later invocation is a REFUSAL, never resume authority.

## 14. Model-engagement / barrier accounting (designed exactly)

- **Maximum 2 engagements TOTAL**; order A first; B ONLY after a mechanically conforming A (guarded at both `run_pipeline` and `run_attempt_for_role`).
- **Fail-closed budget:** `CONSUMED_PRE_EXEC` charges the authority budget conservatively; `EXEC_ATTEMPTED` records inference-capable execution; consumed-without-exec retains the fail-closed charge and is recorded `CONTROL_ROOM_ADJUDICATION_REQUIRED` (the driver never infers provider/model substance); `engagement_accounting` preserves the two facts separately; a conforming `REPORT_FROZEN` first pass establishes its engagement; maximum stays 2; historical old-event attempts do NOT count.
- Any nonconforming A prevents B. No report is manufactured from stdout/stderr. First-pass report substance remains blinded (stat + SHA-256 only). No peer access before both mandatory first-pass conditions are satisfied (nothing Auditor-A-derived enters the Auditor-B attempt). No retry/reconciliation authority is implied (`reconciliation_authorized: false`, `retry_authorized: false` in the barrier record).

## 15. Required design decision — explicit answers

1. **Is the historical two-stage pattern still correct?** YES: future GRANT + chmod-only prelaunch → Control Room granted-prelaunch readback → human-direct wrapper invocation. It matches the mode-0600 barrier design, the non-overwriting invocation context, the wrapper's exact-SHA/exact-mode gate, and the successfully executed RB-001 L1 precedent; every mutation stays inside one authorized, separately-reviewed chain.
2. **Why must deployment remain inside the wrapper invocation?** Section 5: a pre-deployed destination classifies `ALREADY_NEW` and the authorized invocation fails closed at phase 0 (`DEPLOYED_EVENT_NOT_EXPECTED_HISTORICAL_PREDECESSOR`) and again at phase 2 (`DESTINATION_ALREADY_NEW_GENERATION`) — the authority would be stranded with an unauthorized mutation already on disk.
3. **What exact state transition does the future GRANT authorize?** Section 6: RESERVED/NOT_GRANTED/NOT_CONSUMED/NOT_EXECUTABLE → GRANTED/NOT_YET_CONSUMED/EXECUTION_NOT_YET_STARTED (+ DRIVER_WRAPPER_0700_ACTIVATED after the separately-gated prelaunch); it authorizes exactly one chmod-only activation and exactly one human-direct invocation, nothing else.
4. **When is the authority no longer reusable?** From the BEGINNING of the human-direct invocation (durable marker: invocation-evidence-context creation); one invocation consumes the authority regardless of outcome, engagement-reached or not; terminal CONSUMED/TERMINAL after the single invocation ends.
5. **What happens on preexec STOP before a model engagement?** Sanitized mechanical handoff generated LAST; no retry; Control Room review. Budget: no attempt reached ⇒ no AccountingStore ⇒ 0/2 charged mechanically, authority still consumed (one-shot); an attempt that reached CONSUMED_PRE_EXEC without EXEC_ATTEMPTED ⇒ fail-closed charge retained + CONTROL_ROOM_ADJUDICATION_REQUIRED.
6. **What if deployment succeeds but Auditor-A later fails?** Fresh generation remains live (no rollback); predecessor preserved in the fixed backup; Auditor-B does NOT run (double guard); Phase 6 records the barrier CLOSED; handoff generated; authority consumed; return to Control Room; any second invocation independently fails closed (context/ALREADY_NEW/handoff barriers).
7. **What evidence must Control Room verify before the human command?** The granted-prelaunch publication + generated-LAST handoff establishing: live bootstrap EXACT; grant statement canonicalized against the exact target table; driver/wrapper 0700 with bytes unchanged; wrapper pins exact; source/package verification; `EXPECTED_HISTORICAL` destination classification facts; fresh-namespace absence; repository-lineage admission (docs-only descendant, protected trees/pins exact); credential metadata admissibility (no contents); zero runtime state.
8. **Invocation-marker wording: acceptable, residual, or blocking?** Lineage label `INFORMATIONAL_LINEAGE_LABEL_ACCEPTABLE`; grant-status clause `EVIDENCE_REPORTING_PRECISION_RESIDUAL_NONBLOCKING` (R-1); combined record-field classification = `EVIDENCE_REPORTING_PRECISION_RESIDUAL_NONBLOCKING`; NOT blocking; no source remediation required.

## 16. Residuals (non-blocking, recorded prospectively)

- **R-1 INVOCATION_MARKER_GRANT_STATUS_CLAUSE_PRECISION** — the marker's "authority is RESERVED and NOT GRANTED until explicitly operator-granted" reads preparation-time status into a runtime record; truthfully bounded by the "until" clause and disambiguated by exact structured fields + the granted-prelaunch publication; classified EVIDENCE_REPORTING_PRECISION_RESIDUAL_NONBLOCKING; historical evidence/frozen driver bytes NOT modified; no remediation proposed.
- **R-2 INVOCATION_MARKER_LINEAGE_SHORTHAND** — "RB-001 L1" in the marker names launcher lineage (the adapted RB-001 L1 driver) while the operative identities are RB-002 in structured fields and corroborating surfaces; INFORMATIONAL_LINEAGE_LABEL_ACCEPTABLE.
- **R-3 CREDENTIAL_METADATA_TIME_OF_DESIGN** — the lstat-only credential-locator snapshot (both conventional candidates present, in-bounds, 0600, isa:isa; no overrides set) is time-of-design; the prelaunch session MUST re-verify metadata admissibility immediately before activation.
- **R-4 LEGACY_INTERNAL_IDENTIFIER_NAMES** — the 18 `HISTORICAL_EXEC05_*` names are retained accepted legacy internal identifiers (decision A), never serialized as provenance; unchanged.

## 17. Resulting state / next action

**Resulting state (this publication):** `PRELAUNCH_TRANSITION_DESIGN = PROPOSED_FOR_CONTROL_ROOM_READBACK / OPERATOR_GRANT_REQUIRED_SEPARATELY / NO_CHMOD / NO_DEPLOYMENT / NO_EXECUTION_AUTHORITY`. Operator GRANT NONE; chmod NONE; driver execution NONE; wrapper execution NONE; deployment NONE; runtime attempts NONE; AccountingStore NONE; credential read NONE; dynamic real gates NONE; boundary execution NONE; auditor/provider/model execution NONE; replacement execution authority NONE; qualification NONE; installation NONE. EXEC-RB-001 OPEN/ROOT_CAUSE_UNRESOLVED; EXEC-RB-002 CLOSED_AT_CONTROL_ROOM_MECHANICAL_READBACK_STRENGTH; fresh packages ACCEPTED_AT_CONTROL_ROOM_BYTE_COMPLETE_READBACK_STRENGTH; fresh event PREPARED_ONLY/NOT_DEPLOYED/NO_RUNTIME_ATTEMPT; prepared driver+wrapper 0600/NON_EXECUTABLE; audit completeness INCOMPLETE; qualification readiness BLOCKED_BY_MISSING_MANDATORY_AUDITOR_B_FIRST_PASS; AUCDEV-023 remains P1 / READY / NOT DONE (READY 9 / OPEN 7 / BLOCKED 3 = 19 open; P0 2 / P1 7 / P2 11).

**NEXT ACTION EXACTLY ONE:** CONTROL ROOM READBACK OF THE PRELAUNCH TRANSITION DESIGN BEFORE ANY HUMAN OPERATOR GRANT, CHMOD-TO-0700 ACTIVATION, DEPLOYMENT, RUNTIME ATTEMPT CREATION, CREDENTIAL READ, DYNAMIC REAL GATE, REPLACEMENT EXECUTION AUTHORITY, OR REAL AUDITOR/PROVIDER EXECUTION.
