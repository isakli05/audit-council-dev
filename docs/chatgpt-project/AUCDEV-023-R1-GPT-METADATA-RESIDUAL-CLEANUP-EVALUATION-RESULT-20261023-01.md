# R1 residual cleanup evaluation — 2026-10-23 Europe/Istanbul

Root evaluated the ONE remaining previously authorized invocation at `2026-10-22T21:26:07.644979+00:00` (2026-10-23 local date), under existing authority `AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-20261022-01` and its published representation-only amendment. **ONE_VERIFIED_SIGTERM_EXIT_OBSERVED**: unchanged `signal_verified` returned `signalled_exited`. The original remaining one-shot is **USED**; no retry, continuation, permission refresh or new execution authority follows.

Before evaluation, local `master` HEAD was independently refreshed as `1c1673ae582805c84df740663dc3df6a906c38f4`. CURRENT-STATE and BACKLOG were byte-equal to that commit. There is no `graphify-out/graph.json` in this checkout; direct scoped evidence/source review was used. Protected work stayed in Codex Root's primary context; no GLM or subagent execution.

All 18 original approval/source/evidence bindings matched immediately before the operation and after it. The bound producer is `GPT-METADATA-OBSERVATION-RESULT.json`; the separately derived `OBSERVED-GPT-METADATA.json` view is not that producer artifact. Original cleanup decision `af51b1c3853aec799750c99863952ab66aef6f9cdfa28b924ae6417cc0a4a034` and prior stop/result were preserved unchanged. The amendment changes only the cleanup capability's argv representation and comparison descriptor from tuple to list; all eight encoded elements, their order and terminal NUL remain exact.

| Binding | Verified SHA-256 |
| --- | --- |
| Original cleanup request | `87cc793c5460625d50911d2502c5ec688ee3f609d728563e2287ecdffce73351` |
| Amendment request | `38f2c63bcedab7a4f9106c32147b06207d59942e129060d797224ca636b46527` |
| Amendment decision JSON | `dae754e93a175e4613e1a4369e064798aa34bc49f886da2238bccc029aa065b1` |
| Unchanged executor library | `98bdac4ef805498b31a7374deaa4fe121c3642f4f48e6f2bc66dd7d82439244c` |
| Original producer result | `202500ea0cbb9a4ebf3b50c4e5c20a08384adab7cf7b12f72173cb75fcc01bf0` |
| Original observation report | `2efef15febf25d42d4d0cc0205a01ab048bb7dfb552cbb5d264767c42fff6656` |
| Original read-only review | `d7c8bfd83d176aa3e39d98dd97b69bf445073c06aedb4e8340479da7f88f2889` |
| Original entry invocation | `fb4c0903011ec1ece47109a06617a2da28549a56d0da6804319d30fe1e1c366a` |
| Original handoff birth/state | `57b2954513975eda442d3a229c6eb95a595cda146248db84c803ce045bcc9e56` |
| Fresh Root evaluation JSON | `d5172582452ff98a810094a61aff9ef8d7c40de35be4031835668b5f61ba0a28` |
| Exact Root orchestration source | `9a37073819e78c3cb214363301c57f0f691f4579be617592530252f579e3d2db` |

Root first matched original PID `2063940`, boot ID `2980de59-4632-4e7a-a253-5498c094f169`, startticks `80682543`; only then read UID, exe and full argv. Three complete birth-first checks (initial, immediately before library entry, immediately at its signal syscall) each matched UID 0 (all four UID fields zero), exact executable `/usr/bin/qemu-nbd` and byte-identical full launch argv: 8 elements, 134 raw bytes including terminal NUL, SHA-256 `c06d31cd7abb171ed5004e08d47ff96414aa8a499b6b85320aa222434c8dd24d`. Each full check included a final birth recheck. The unchanged library also performed its own mandatory birth/exe/argv/birth checks. A caller audit guard blocked helper/fallback spawns and allowed only this one verified SIGTERM; no library source, functions or policy globals were changed.

Exactly one Root-controlled evaluation entry, one `signal_verified(cleanup_cap, sig=SIGTERM, wait=10.0)` invocation and one verified SIGTERM occurred at `2026-10-22T21:26:07.686266+00:00`. The library observed the PID absent during its wait and returned `signalled_exited`; Root ended at `2026-10-22T21:26:07.736829+00:00`. Root operation elapsed **0.091889 seconds**; the complete terminal entry took 0.634851 seconds. The 10-second wait and 60-second total limits were satisfied. This establishes the observed process exit at that point; no perpetual process-state or resource-namespace claim is made. Root made no further process query after the library returned.

Retries, SIGKILL, fallback, escalation/permission refresh, recapture, manual cleanup, disk stat/hash/read, NBD connection, VM/QGA/PREARM, credential access and auditor execution: **0** in this evaluation. Paths appearing inside argv were compared only as bytes. Socket/workroot contents were neither inspected nor removed; their later state remains unverified. No collector entry, observation continuation or post-disk hash occurred.

The original metadata observation remains **TEARDOWN_INCOMPLETE_STOP**. Its empty birth-argv capture (`e3b0c44298fc1c14`) stays FAILED evidence, full initial argv NOT_ESTABLISHED; the later approved launch baseline does not repair it. The missing post-disk hash, original 1890.639 s > 900 s resource-lifetime violation, exec/proc-race hypothesis, startup-safety and disk-immutability unknowns, installed-auditor qualification NOT_ESTABLISHED, historical incidents/LOST and frozen G5–G12/credential state are preserved. This is **not a successful metadata audit**, disk-unchanged proof, safe-start decision or qualification.

Machine evidence: [AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-EVALUATION-RESULT-20261023-01.json](AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-EVALUATION-RESULT-20261023-01.json). Non-secret evidence workspace: `/home/isa/aucdev023-r1-gpt-residual-cleanup-evaluation-20261023-01/`; pre/post binding verification, exact invocation source and record, original producer/launch/read-only evidence, source excerpts, committed diff and checksum inventory are packaged by explicit allowlist. Secrets, credentials, sealed and unread material are excluded. AUCDEV-023 remains **P1 / READY / NOT_DONE**.
