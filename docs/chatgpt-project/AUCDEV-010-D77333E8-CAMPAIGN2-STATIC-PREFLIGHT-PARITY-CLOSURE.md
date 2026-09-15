# AUCDEV-010 D77333E8 — Campaign-2 Static Preflight / Working-Codex Parity Closure (APPEND-ONLY CORRECTION)

| Field | Value |
|---|---|
| Session class | ZERO-MODEL HARNESS / PROVIDER-RUNTIME PREFLIGHT IMPLEMENTER ONLY — NOT Auditor A/B, NOT the Control Room, NOT a qualification/installation authority |
| Date | 2026-09-15 (Europe/Istanbul) |
| Governance base | live master `ecba509bc81eb4a4df51d60b6cc9053acd894637` (verified EXACT at bootstrap; sole parent of this publication commit) |
| Input authority | Control Room correction mandate of 2026-09-15 (operator observation: normal authenticated Codex with GPT-5.6 Sol xhigh working on the SAME host/egress), superseding the prior 451-based general-block interpretation of the ecba509 preflight |
| Frozen target | `d77333e86aa091d2ac003e9a2ad26c88dff56aeb` UNCHANGED (tree `de7261e3c912fa74e3a06d3f114b7e489c66225c`; skill tree `c792933a862d9a5434681a88d183470dd8b15d2f`; re-verified live during the battery) |
| Provider/model inference | ZERO — no Claude Opus, no GPT-5.6/Codex model turn, no `/audit-council`, no completion/messages/responses request; only `--version` outputs, sanitized metadata inspection, GET-only unauthenticated reachability probes, read-only `/proc`/filesystem observation, and network-disconnected Codex local-init runs (explicitly NOT engagements) |
| Campaign accounting | `D77333E8_CAMPAIGNS_USED = 1` of max 2; remaining 1; NO Campaign 2 created; NO new event ID; NO new transports; NO execution authority requested; Campaign-1 evidence untouched |
| Outcome | **`AUCDEV_010_D77333E8_CAMPAIGN2_STATIC_PREFLIGHT_PARITY_CLOSED_AWAITING_CONTROL_ROOM_READBACK`** |
| Acceptance battery | successor battery 24 gates, 24 PASS / 0 FAIL / 1 deferred item (dynamic resource state, `DEFERRED_TO_EXECUTION_GATE` per policy) |
| Qualification/installation | readiness BLOCKED / qualification NONE / installation NONE |

## 1. Mandatory append-only correction statements (§14)

1. The same-host normal authenticated Codex GPT-5.6-Sol-xhigh working status is **OPERATOR_OBSERVED**. It is independently SUPPORTED — not converted to independent proof — by provider-written artifacts (§4).
2. The prior direct **unauthenticated** HTTP 451 probe of `chatgpt.com/backend-api/ps/mcp` did **NOT** establish general geo/egress blockage, ChatGPT account blockage, regional inability to run Codex, or inability to run GPT-5.6 Sol. Its historical token `DIRECT_UNAUTHENTICATED_PREFLIGHT_PROBE_HTTP_451_OBSERVED` stands unchanged; its scope is corrected to UNAUTHENTICATED-REQUEST-CLASS-SPECIFIC edge behavior (§5/§7).
3. The corrected classification derived from this session's evidence is `HARNESS / AUTH-CONFIG-RUNTIME-PARITY DIFFERENCE CONFIRMED`: the Campaign-1 Auditor-B network failure is mechanically reproduced and explained by a **resolver defect inside the corrected launch boundary** (§6), and route selection is auth-shape-dependent (§7).
4. The Auditor-A route policy was already established by the operator: `AUDITOR_A_ROUTE_POLICY_ESTABLISHED = PLAIN_CLAUDE / FIRST_PARTY_ANTHROPIC` (cc-zai/GLM-5.3 is the controller environment only; Auditor A MUST use plain `claude` with Anthropic Claude Opus and MUST NOT inherit controller z.ai route/model overrides). The ecba509 blocker-A route-choice question is therefore CLOSED as an operator decision; this session proves the future A environment mechanically (§2).

The historical report `AUCDEV-010-D77333E8-CAMPAIGN2-HARNESS-PREFLIGHT-CORRECTION.md` is NOT rewritten; this record corrects its interpretation append-only.

## 2. Auditor-A first-party environment — MECHANICALLY ESTABLISHED

`AUDITOR-A-FIRST-PARTY-ENV-PROOF.json` (zero inference): the full controller override census (8 route/model overrides incl. `ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic`, `ANTHROPIC_AUTH_TOKEN` name-only, all five model slots + `CLAUDE_CODE_SUBAGENT_MODEL` pinned `glm-5.3[1m]`, plus session-contamination names, `profiles/zai.json` env-block and zai plugin marketplace) was enumerated live; a clean construction (fresh `CLAUDE_CONFIG_DIR` + fresh `HOME`, explicit env whitelist) mechanically shows ALL forbidden names ABSENT, the credential surface reduced to `.credentials.json` alone (`claudeAiOauth`, subscriptionType `pro`, scope `user:inference`, unexpired today, mode 0600), no `CLAUDE.md`/`projects`/`plugins`/`skills`/`settings` in the config dir, plain `claude` identity `2.1.263 (Claude Code)` (native exe SHA-256 recorded; only `--version` executed), and first-party `api.anthropic.com` GET-reachable 3/3 (401 unauth; DNS+TLS cert match). Verdict: `AUDITOR_A_FIRST_PARTY_EXECUTION_ENVIRONMENT_MECHANICALLY_ESTABLISHED`. Actual Opus-serving verification inherently requires inference and was NOT performed.

## 3. Working normal Codex — observation status

No live operator Codex process existed during the session window (12:04Z–13:26Z): full `/proc` scans (comm + open-fd under `~/.codex`) found none; a read-only appear/disappear watcher stayed armed all session and captured only THIS session's own sandboxed codex runs (cwd `/auditor-home`). Recorded honestly: `LIVE_WORKING_CODEX_RUNTIME_OBSERVATION_UNAVAILABLE`; full live runtime parity NOT claimed. The working session itself is evidenced by sanitized metadata: npm `@openai/codex` updated to **0.154.0** at 12:32Z (binary identity + SHA-256 recorded), newest session rollout filename timestamped 12:32:43Z (filename only; content never read), provider state written through 12:43:52Z, and `models_cache.json` **written by the authenticated runtime at 12:41:44Z** (client 0.154.0, etag present) listing the account's entitled models including `gpt-5.6-sol` — a TRUE non-inference entitlement artifact. `NORMAL-WORKING-CODEX-RUNTIME-MANIFEST.json` records the sanitized facts (executable/auth-class `chatgpt`/config keys/state classes/`.system` skill inventory/redaction list); conversation material was never read.

## 4. Route determination — auth-shape-dependent (NOT one unauthenticated GET)

Zero-network runs of the exact 0.154.0 binary inside the corrected architecture (bwrap `--unshare-net`): with the REAL auth shape (`auth_mode: chatgpt`) codex attempts exactly the Campaign-1 Auditor-B signature — `https://chatgpt.com/backend-api/ps/mcp` (rmcp) and `wss://chatgpt.com/backend-api/codex/responses` (reconnect 2/5..5/5, WebSocket→HTTPS fallback) — while the synthetic/absent-auth control targets only `wss://api.openai.com/v1/responses` (no ps/mcp). Debug references add `ab.chatgpt.com`. Same-day coexistence on the same egress: unauthenticated GET 451 ×3 at 12:04Z (persisting probe) vs authenticated models-refresh success at 12:41:44Z.

## 5. Prior 451 — precise reclassification

`DIRECT_UNAUTHENTICATED_PREFLIGHT_PROBE_HTTP_451_OBSERVED` (historical token unchanged) is UNAUTHENTICATED-EDGE-SPECIFIC for the ps/mcp path (Cloudflare edge; `chatgpt.com/` root 403, `api.openai.com` 401 unauth — both reachable). It does NOT evidence general egress blockage. The ecba509 conclusion "the ChatGPT backend route family is legally/geo-blocked from this host's egress … mechanically establishes the exact route condition behind the Campaign-1 Auditor-B observed network failure" is corrected append-only: the Campaign-1 failure condition is explained by §6 below.

## 6. Campaign-1 Auditor-B failure root cause — MECHANICALLY ESTABLISHED (harness resolver defect)

Host `/etc/resolv.conf` is a symlink to `/run/systemd/resolve/stub-resolv.conf`. The corrected launcher `f3085085…` ro-binds `/etc` but mounts `--tmpfs /run`, so inside the boundary the symlink DANGLES: no resolver exists and every lookup fails with exactly Campaign-1's observed `failed to lookup address information: Try again` (EAI_AGAIN). Reproduced today inside the exact boundary shape with network ENABLED (T1: `/etc/resolv.conf: No such file or directory`, all DNS fails); discriminated by T2: adding `--ro-bind /run/systemd/resolve /run/systemd/resolve` restores DNS (`DNS_OK_VIA_STUB`) and the same boundary completes TLS/HTTP to the chatgpt.com edge (451) and `api.openai.com` (401) — network namespace, routing, TCP and TLS were never blocked. Recorded: `CORRECTED_BOUNDARY_RESOLVER_DEFECT` (REQUIRED_NONSECRET_CONFIG class); successor launcher MUST provide a working resolver. This supersedes the geo-block explanation for Campaign-1 B; the historical OBSERVED-FACT records stand unmodified.

## 7. Provider `.system` skills — substantive input PRESENT; safely neutralizable; neutralization MANDATORY

Zero-network marker test inside the ephemeral CODEX_HOME (inert markers confined to the ephemeral copy; no network possible): every skill under `skills/.system` has its **name + description + file path automatically inserted into every turn's assembled request** as a `developer`-role `<skills_instructions>` message (an injected marker skill appeared verbatim; unmodified `imagegen`/`openai-docs` descriptions present; telemetry instruments `skills.enabled/kept/truncated`, `skills.description_truncated_chars` corroborate). Bodies are NOT auto-inserted (body marker absent). Recorded: `CODEX_SYSTEM_SKILLS_SUBSTANTIVE_RUNTIME_INPUT_PRESENT` (class C at advertisement level). **Safe disable PROVEN**: six `[[skills.config]] path=… enabled=false` entries (recognized under `--strict-config` on 0.154.0) remove the block entirely, leaving only the provider-native `<permissions instructions>` message (unavoidable, identical for every codex run, preserved separately from user/host methodology). Successor staging MUST generate these entries from the live `.system` census and FAIL CLOSED on any uncovered `.system` skill. The skills themselves are PROVIDER_CREATED_STATE (embedded in the binary; recreated at init without network).

## 8. Zero-network successor staging — minimum set + proofs

Minimum successor role-B set (no wholesale `~/.codex` copy): `auth.json` (REQUIRED_AUTH_MATERIAL; ro-staged → ephemeral copy; values never recorded; copy shredded after use) + `config.toml` (`model`, `model_reasoning_effort`, `[[skills.config]]` disable-all) + boundary resolver provision. Proven in this session's runs: writable-home-BEFORE-validation with `ENVIRONMENT_VERIFIED` then `DIGEST_VERIFIED` stability across full codex startups; EROFS absent; 30+ state files confined to the ephemeral CODEX_HOME; netns route table empty (zero outbound mechanically possible); host methodology (graphify/AGENTS.md/CLAUDE.md/repo) invisible; user history and peer artifacts absent by construction. Full classification: `CODEX-RUNTIME-PARITY-DIFF.json` (21 items across the 9-class taxonomy).

## 9. Resource gate — reclassified dynamic execution precondition

`RESOURCE_GATE_CURRENT_HOST_FAIL` → `DYNAMIC_EXECUTION_PRECONDITION_NOT_CURRENTLY_SATISFIED`. Frozen fail-closed thresholds unchanged (MemAvailable ≥ max(8 GiB,20%); SwapFree ≥ 50%; PSI < 20%; cgroup < 95%; load15 ≤ 2×cpu; no competing provider process; OOM evidence honestly unreadable-without-elevation). Today: 3/3 samples FAIL (swap ≈16% free; live provider process = this controller session); MemAvailable 9.0–10.0 GiB PASSES. Campaign-2 PACKAGE PREPARATION may proceed; future Auditor A/B EXECUTION must still fail closed unless immediately prelaunch 3 consecutive PASS + no competing process + frozen thresholds. No threshold weakening; no automatic termination.

## 10. Successor battery (§12)

24 gates (A 5 / B 11 / S 8), machine-derived: **24 PASS / 0 FAIL**, one deferred item (dynamic resource state, `DEFERRED_TO_EXECUTION_GATE`). The prior 25-gate battery (22/3) is superseded as classification, NOT overwritten. Live-codex observation remains an explicit limitation (gate B1 disjunction "obtained OR explicitly limited" satisfied via sanitized artifacts; watcher evidence archived).

## 11. Dispositions

`AUCDEV_010_D77333E8_CAMPAIGN2_STATIC_PREFLIGHT_PARITY_CLOSED_AWAITING_CONTROL_ROOM_READBACK / BASE_ecba509bc81eb4a4df51d60b6cc9053acd894637 / TARGET_d77333e86aa091d2ac003e9a2ad26c88dff56aeb_UNCHANGED / ZERO_PROVIDER_MODEL_INFERENCE / OPERATOR_GPT56_SOL_WORKING_STATUS_OPERATOR_OBSERVED / PRIOR_451_UNAUTHENTICATED_EDGE_SPECIFIC_GENERAL_BLOCK_NOT_ESTABLISHED / CAMPAIGN1_B_FAILURE_ROOT_CAUSE_CORRECTED_BOUNDARY_RESOLVER_DEFECT_MECHANICALLY_ESTABLISHED / AUDITOR_A_ROUTE_POLICY_ESTABLISHED_PLAIN_CLAUDE_FIRST_PARTY_ANTHROPIC / AUDITOR_A_FIRST_PARTY_EXECUTION_ENVIRONMENT_MECHANICALLY_ESTABLISHED / LIVE_WORKING_CODEX_RUNTIME_OBSERVATION_UNAVAILABLE / ROUTE_SELECTION_AUTH_SHAPE_DEPENDENT_CHATGPT_COM_BACKEND_VS_API_OPENAI_COM / CODEX_SYSTEM_SKILLS_SUBSTANTIVE_RUNTIME_INPUT_PRESENT_SAFELY_DISABLED_PROVEN_NEUTRALIZATION_MANDATORY / MINIMUM_SUCCESSOR_ROLE_B_SET_ESTABLISHED / RESOURCE_GATE_RECLASSIFIED_DYNAMIC_EXECUTION_PRECONDITION_DEFERRED_TO_EXECUTION_GATE / BATTERY_24_GATES_24_PASS_0_FAIL_1_DEFERRED / CAMPAIGNS_USED_1_OF_2 / CAMPAIGNS_REMAINING_1 / CAMPAIGN2_NOT_CREATED / CAMPAIGN2_NOT_AUTHORIZED / NO_NEW_EVENT_ID / NO_NEW_TRANSPORTS / QUALIFICATION_READINESS_BLOCKED / QUALIFICATION_NONE / INSTALLATION_NONE`

This closure does NOT create Campaign 2, does NOT allocate an event ID, does NOT grant execution authority, and does NOT authorize any auditor/model call.

## 12. Publication mechanics

Exactly ONE governance commit over exact base `ecba509bc81eb4a4df51d60b6cc9053acd894637`; changed paths EXACTLY `AUCDEV-CURRENT-STATE.md`, `AUCDEV-BACKLOG.md`, NEW THIS file. One fast-forward push after immediate prepush live-master re-resolution requiring exactly `ecba509…`; no retry; no force; no tags. Working-tree noise (`smoke-fixture*`, `aucdev019-evidence/`) left untouched and excluded.

## 13. Immediate next action

Independent Control Room readback of THIS publication and its handoff archive. On acceptance, the operator may authorize Campaign-2 PACKAGE PREPARATION (corrected launcher v3 with resolver provision; `[[skills.config]]` neutralization; frozen 0.154.0-or-later executable fingerprint re-derivation; resource gate re-evaluated immediately prelaunch as an execution precondition). Campaign-2 creation (NEW event ID + fresh package + SEPARATE explicit operator execution authority) remains a distinct later decision — NOT made by this record.
