# AUCDEV-010 D77333E8 — Campaign-2 Harness / Provider-Route Preflight Correction (PARTIAL BLOCKED)

| Field | Value |
|---|---|
| Session class | ZERO-MODEL HARNESS / PROVIDER-ROUTE PREFLIGHT IMPLEMENTER ONLY — NOT Auditor A/B, NOT the Control Room, NOT a qualification/installation authority |
| Date | 2026-09-15 (Europe/Istanbul) |
| Governance base | live master `f74f2e1214b5711f4495ad876aeb5efad8d445db` (verified EXACT at bootstrap; sole parent of this publication commit) |
| Input authority | `AUCDEV_010_D77333E8_CAMPAIGN1_EXECUTION_FAILURE_PUBLICATION_READBACK_ACCEPTED / … / BOUNDED_HARNESS_PROVIDER_ROUTE_PREFLIGHT_CORRECTION_AUTHORIZED / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE` |
| Frozen target | `d77333e86aa091d2ac003e9a2ad26c88dff56aeb` UNCHANGED (tree `de7261e3c912fa74e3a06d3f114b7e489c66225c`; skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`; re-verified live during the battery) |
| Provider/model inference | ZERO — no Claude Opus, no GPT-5.6/Codex inference, no `/audit-council`, no completion/messages/responses request; only `--version`, sanitized config inspection, unauthenticated GET reachability probes, and a network-disconnected Codex local-init test (explicitly NOT an engagement) |
| Campaign accounting | `D77333E8_CAMPAIGNS_USED = 1` of max 2; remaining 1; NO Campaign 2 created; NO new event ID; NO new transports; Campaign-1 historical evidence untouched (transports A=B `68ac889b…` immutable) |
| Outcome | **`AUCDEV_010_D77333E8_CAMPAIGN2_HARNESS_PREFLIGHT_CORRECTION_PARTIAL_BLOCKED`** — all A–F mechanisms implemented and machine-validated; THREE exact operator-decision blockers remain (below) |
| Acceptance battery | 25 gates (machine-derived from the declared gate table), 22 PASS / 3 FAIL (`PREFLIGHT_CORRECTION_FAILED = 3`) |
| Qualification/installation | readiness BLOCKED / qualification NONE / installation NONE |

## 1. Scope and bootstrap

Mandatory live bootstrap verified: `refs/heads/master` = `f74f2e1214b5711f4495ad876aeb5efad8d445db` EXACT; the seven required documents were fetched at that SHA and hashed (recorded in the handoff archive `00-bootstrap/`); the target commit/root tree/skill tree identities were re-verified; canonical Campaign-1 accounting (engagements 2/2 consumed/closed; zero conforming first passes; barrier NOT opened; campaigns 1/2 used; Campaign 2 NOT authorized) was verified against CURRENT-STATE record 57 and BACKLOG record 59. Working-tree noise present at bootstrap (`smoke-fixture`, `smoke-fixture-103` modified; `aucdev019-evidence/` untracked) was left untouched and is excluded from this publication.

## 2. Blocker A — Claude provider-route binding (mechanism PASS; identity route NOT established)

Mechanically established, without exposing credential values (`01-claude-route/`):

- Executable `/home/isa/.nvm/versions/node/v24.14.0/bin/claude` → native `claude.exe` (215662064 B), version output `2.1.263 (Claude Code)` — EXACTLY the frozen Campaign-1 Auditor-A runtime version.
- **Ambient working route: third-party gateway** — `ANTHROPIC_BASE_URL=https://api.z.ai/…` with `ANTHROPIC_AUTH_TOKEN` (49 chars, value never recorded) and ALL model slots pinned to `glm-5.3[1m]` (`ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL`). Classification `THIRD_PARTY_OR_GATEWAY_OVERRIDE`.
- **First-party surface present**: `~/.claude/.credentials.json` (0600, `claudeAiOauth` key shape: accessToken/refreshToken/expiresAt/scopes/…) plus an `oauthAccount` record in `~/.claude.json`. With the ambient overrides absent, the CLI default route is `api.anthropic.com`.
- Non-inference readiness probes (framework `lib/route_probes.py`; GET-only; no request body; acceptable codes 2xx/3xx/401/403/404; fail-closed on DNS/TCP/TLS/route mismatch): `api.anthropic.com` DNS 3/3, TCP 3/3, TLS 3/3 (cert `CN=api.anthropic.com`, SAN match, GTS issuer), HTTP 3/3 (`/v1/models` → 401 unauth) and `api.z.ai` 3/3/3/3 (`/v1/models` → 404). NO inference endpoint was invoked.
- Sanitized manifest: `CLAUDE-PROVIDER-ROUTE-MANIFEST.json` (executable/auth-class/config/env-names/routes/identity verdict + probe-result hashes).
- **Verdict**: the host's working configuration does NOT establish the required Claude Opus first-party-equivalent identity → `CLAUDE_REQUIRED_PROVIDER_IDENTITY_ROUTE_NOT_ESTABLISHED` recorded and launch-readiness acceptance for this blocker STOPPED. No alternate endpoint was silently adopted. The first-party OAuth route is configuration-available and reachable (3/3), but authorizing it for the future Auditor-A launch — and any actual Opus-serving verification, which inherently requires inference — is an OPERATOR decision.

## 3. Blocker B — Codex final writable home BEFORE final validation (PASS)

Implemented and proven (`02-codex-home/`, exercised inside a real bubblewrap boundary):

1. Role-B auth/config enters ONLY from a minimal READ-ONLY staging mount (`/auditor-auth/codex-ro`, census-enforced: exactly `auth.json` + minimal `config.toml`).
2. A fresh ephemeral writable `/auditor-home/.codex` is created INSIDE the boundary (pre-existence fails closed).
3. ONLY the approved set is copied; modes enforced 0700 (dir) / 0600 (files); ownership recorded.
4. `CODEX_HOME=/auditor-home/.codex` is set once (single env source file).
5. ONLY THEN `codex_final_env_validator.py` runs: approved-file census (names/sha256/modes), no host-sourced material (`AGENTS.md`, `history.jsonl`, `memories`, `skills/graphify`, `agents/`, `plugins/`), codex-owned state allowlisted (`sessions`, `state_*`, `tmp`, `skills/.system` — with `skills` restricted to `.system` only), forbidden env names absent, host trees invisible, writability probe → `ENVIRONMENT_VERIFIED` + provider-environment digest (sha256 over the canonical env record, timestamps excluded).
6. `codex_provider_entry.sh` re-verifies the digest IMMEDIATELY before exec and refuses on mismatch (`DIGEST_VERIFIED` observed; refusal path also demonstrated).

Mutation policy enforced: the controller may not mutate `CODEX_HOME` approved set / auth / provider env / mounts / cwd after validation; the provider's OWN state writes are expected and proven NOT to touch the approved set (digest stable across a full codex startup).

## 4. §6 — Codex local-initialization proof without provider inference (PASS)

The exact future executable (`codex-cli 0.153.4`) ran inside `bwrap --unshare-net --unshare-pid` with a synthetic inert `auth.json` (no real credentials anywhere in the evidence):

- **EROFS ELIMINATED**: zero `Read-only file system` / `os error 30` occurrences; 90+ writable-state files created ONLY under `/auditor-home/.codex` (session rollout file, `state_5.sqlite*`, `thread_history_1.sqlite*`, codex-owned `skills/.system/*`, `tmp/arg0/*` incl. `codex-linux-sandbox`).
- **Zero outbound mechanically proven**: netns route table empty (`/proc/net/route` — netns-authoritative); DNS lookups fail (`Errno -3`); direct connect attempts fail; the provider's own stderr shows the expected network denial on its real route (`wss://api.openai.com/v1/responses` reconnect failures 2/5..5/5, WebSocket→HTTPS fallback message).
- **Host trees invisible** inside the boundary: `~/.codex/skills/graphify/SKILL.md`, `~/.codex/config.toml`, `~/.claude/*`, repo `.git` — all nonexistent (the Campaign-1 parity-defect path is hidden by construction).
- Process record: start `08:56:45Z`, end `08:57:45Z`, rc 124 (timeout under permanent network denial — expected), stdout 0 B (banner on stderr; explicit justification recorded), stderr 2011 B sha256 `e181ccfdf554b697529221c4a545abf2fe615d4f024b228958c88531559d2342`.
- NOT claimed as an audit request; NOT counted as a model/provider engagement.
- Runtime discovery: with this auth shape codex targeted `api.openai.com` — the role-B frozen hostname set therefore includes BOTH `chatgpt.com` (Campaign-1 observed) and `api.openai.com` (runtime-discovered; paths must be re-derived at future prelaunch, never assumed).

## 5. Blocker C — provider-route connectivity preflight (mechanism PASS; role-B current route FAIL)

Shared framework: `lib/route_probes.py` + `route_readiness.py` with frozen per-role configs (`role-claude.json`, `role-codex.json`), 3/3 DNS/TCP/TLS/HTTP required per hostname within one bounded window, GET-only unauthenticated, authentication-success and reachability recorded as DISTINCT properties (auth NOT tested without inference; auth MATERIAL presence is the final-env validator's job), and a same-network-namespace operational requirement for the future controller.

- Role A: PASS (both `api.anthropic.com` and `api.z.ai` 3/3 on all four properties).
- Role B: **FAIL — `chatgpt.com/backend-api/ps/mcp` returns `HTTP 451 Unavailable For Legal Reasons` 3/3** (Cloudflare edge `CF-RAY …-IST`), i.e. the ChatGPT backend route family is legally/geo-blocked from this host's egress; `chatgpt.com/` itself serves 200 and `api.openai.com` passes 3/3 (`/v1/models` → 401). This mechanically establishes the exact route condition behind the Campaign-1 Auditor-B observed network failure and is NOT fixable by harness code alone: the operator must provide an unblocked egress for the ChatGPT-OAuth backend or authorize the `api.openai.com` backend auth shape for Auditor B.

## 6. Blocker D — host resource preflight gate (mechanism PASS; CURRENT host FAIL)

`04-resource-gate/resource_gate.py` freezes the conservative fail-closed policy: `MemAvailable ≥ max(8 GiB, 20% MemTotal)`; `SwapFree ≥ 50% SwapTotal` (when swap exists); memory PSI some-avg60 < 20%; cgroup usage < 95% of limit; `load15 ≤ 2×cpu`; no known competing audit/provider process; kernel-OOM evidence read without elevated authority and recorded honestly (`OOM_EVIDENCE_UNREADABLE_WITHOUT_ELEVATED_AUTHORITY`). Three samples, all must pass; the tool never kills anything.

Current host (3 samples, 5 s interval): MemAvailable ≈ 9.6 GiB (PASS), PSI 0.0 (PASS), load 1.7 ≤ 24 (PASS) — but **SwapFree ≈ 5.04 of 31.05 GiB (~16%, FAIL vs ≥50%)** and a **live provider process is running** (`claude --settings …/profiles/zai.json`, FAIL). The gate therefore fails closed today. No OOM-cause claim is made (Campaign-1 root cause remains NOT independently established); the host must re-satisfy the gate at future prelaunch.

## 7. Blocker E — controller-scope enforcement (PASS)

`05-controller-scope/controller_scope_launcher.sh` + `controller_scope_preflight.py` mechanically enforce, BEFORE any campaign work: cwd outside `/home/isa/audit-council-dev` and outside every registered AUCDEV worktree; fresh dedicated controller root (no prior-campaign pattern); dedicated `CLAUDE_CONFIG_DIR` under the controller root containing NO `skills/` and NO `projects/` auto-memory (minimal GLM-5.3 controller config skeleton; operator places real auth; credential values never read); no prior Campaign-1 controller workspace mounted; no peer substantive artifact exposed (env/mounts); role-B `ZERO_CURRENT_EVENT_AUDITOR_A_SUBSTANCE_IN_CONTROLLER_CONTEXT` attestation required COMPLETE (template sentinels fail closed). Validated NEGATIVE (repo cwd + ambient env → FAIL on C1–C4, exactly the Campaign-1 DEV-001 class), POSITIVE role A (PASS), RED role B (unfilled attestation → FAIL C7), GREEN role B (PASS).

## 8. Blocker F — execution evidence and authority-marker precision (PASS)

- Five emission-point-bound, mutually non-inferable markers: `LOCAL_INFERENCE_CAPABLE_CLI_EXEC_START`, `LOCAL_CLI_INITIALIZED`, `PROVIDER_ROUTE_ACTIVITY_OBSERVED`, `MODEL_OUTPUT_FIRST_BYTE_OBSERVED`, `PROCESS_TERMINATED`; `PROVIDER_REQUEST_INITIATED` is RETIRED (Campaign-1 emitted it before `exec` without provider activity).
- Termination-evidence contract: start/end UTC, pid, rc-or-signal (+signal number), raw wait status, session id or explicit absence reason, stdout/stderr refs with size+sha256, first-pass presence/absence record; **zero-byte placeholders are rejected** unless an explicit machine-recorded justification exists. Selftest 7/7 (positive + six negatives).
- `FINAL-REPORT.md` is a mandatory handoff member (section contract checker `final_report_check.py`; this session's own handoff conforms).
- Proposed future authority rule — **NOT GRANTED, operator approval required**: `SINGLE_USE_AUTHORITY_CONSUMED when the inference-capable auditor CLI is exec'd AFTER all final mechanical gates have passed.`

## 9. §11 — final-environment attestation mechanism (PASS)

`07-final-env-manifest/final_env_manifest.py` (capture/verify) records per role: cwd, executable path/size/mode/sha256 + version output, model/effort requested, transport hash, boundary artifact hashes, PID-namespace state (self/pid1 inodes), host-sentinel result, auth mount role, final HOME, final `CLAUDE_CONFIG_DIR`/`CODEX_HOME`, sanitized provider env names, route-manifest hash, route-readiness result hash, resource-gate result hash, controller-scope result hash; per-process volatile facts (PID census) are recorded but excluded from the digest. Verified inside a boundary: capture → `FINAL_ENV_MANIFEST_VERIFIED`; deliberate post-manifest `CODEX_HOME` mutation → `FINAL_ENV_MANIFEST_MISMATCH` (fail-closed); PID census 3 inside; host sentinel invisible.

## 10. Acceptance battery (§12)

Declared-as-data gate table, total derived mechanically: **25 gates** (CLAUDE 9 / CODEX 8 / SHARED 8), **22 PASS / 3 FAIL** → `PREFLIGHT_CORRECTION_FAILED = 3`. Full per-gate results with evidence file references: `08-battery/battery-result.json`. Failed gates:

1. `CLAUDE-1 required identity/route classification established AND required identity route established` — `CLAUDE_REQUIRED_PROVIDER_IDENTITY_ROUTE_NOT_ESTABLISHED` (ambient z.ai gateway; operator route decision pending).
2. `CODEX-7 route readiness 3/3 (frozen role-B hostname set)` — `chatgpt.com/backend-api/ps/mcp` HTTP 451 (legal/geo) 3/3 from this egress.
3. `SHARED-3b CURRENT host satisfies frozen resource gate` — swap ~16% free vs ≥50% policy + live provider process (recoverable at future prelaunch).

Per the frozen rule, Campaign-2 preflight is NOT marked ready; the result is published honestly as `CAMPAIGN2_PREFLIGHT_CORRECTION_PARTIAL_BLOCKED`. The three blockers are operator decisions/conditions that this implementer is NOT authorized to resolve: (1) authorize the Claude first-party OAuth route (or provide an equivalent Claude-Opus-identity route config) for the future Auditor-A launch; (2) provide an unblocked egress for the ChatGPT backend or authorize the api.openai.com backend auth shape for Auditor B; (3) host resource headroom must re-satisfy the frozen gate at future prelaunch.

## 11. Dispositions recorded

`AUCDEV_010_D77333E8_CAMPAIGN2_HARNESS_PREFLIGHT_CORRECTION_PARTIAL_BLOCKED / BASE_f74f2e1214b5711f4495ad876aeb5efad8d445db / TARGET_d77333e86aa091d2ac003e9a2ad26c88dff56aeb_UNCHANGED / ZERO_PROVIDER_MODEL_INFERENCE / BLOCKER_A_MECHANISM_PASS_IDENTITY_ROUTE_NOT_ESTABLISHED / BLOCKER_B_WRITABLE_HOME_BEFORE_VALIDATION_PASS / CODEX_LOCAL_INIT_ZERO_NETWORK_NO_EROFS_PASS / BLOCKER_C_FRAMEWORK_PASS_ROLE_B_451_GEO_LEGAL_BLOCK / BLOCKER_D_GATE_MACHINE_ENFORCED_CURRENT_HOST_FAIL / BLOCKER_E_CONTROLLER_SCOPE_ENFORCED_PASS / BLOCKER_F_EVIDENCE_MARKER_CONTRACT_PASS / FINAL_ENV_MANIFEST_MECHANISM_PASS / BATTERY_25_GATES_3_FAILED / CAMPAIGNS_USED_1_OF_2 / CAMPAIGNS_REMAINING_1 / CAMPAIGN2_NOT_CREATED / CAMPAIGN2_NOT_AUTHORIZED / NO_NEW_EVENT_ID / NO_NEW_TRANSPORTS / PROPOSED_AUTHORITY_RULE_NOT_GRANTED / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

Campaign accounting (bookkeeping only, frozen retry policy unchanged): `D77333E8_CAMPAIGNS_USED = 1`; remaining 1; no Campaign 2 created; no event ID allocated; no A/B transports instantiated; no execution authority requested; no auditors invoked.

## 12. Target / product immutability

`d77333e86aa091d2ac003e9a2ad26c88dff56aeb` untouched (commit/tree/skill-tree re-verified live during the battery; tracked diff since the base is limited to the three governance paths of this publication). No product source/test modified; no qualification-history row added (no audit RECEIVED); Campaign-1 historical reports and archives untouched.

## 13. Immediate next action

Independent Control Room readback of THIS publication and the handoff archive, then operator resolution of the three named blockers (Claude identity route authorization; Codex route egress or backend decision; resource-headroom re-satisfaction). Only after readback acceptance AND blocker resolution may a fresh D77333E8 Campaign 2 (NEW event ID + freshly instantiated package + separate explicit operator execution authority) be considered — NOT created or authorized by this record.
