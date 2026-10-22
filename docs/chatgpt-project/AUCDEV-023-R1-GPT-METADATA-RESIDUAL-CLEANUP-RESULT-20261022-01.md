# AUCDEV-023-R1 GPT Metadata Residual Cleanup — Result 2026-10-22

## Observed outcome

- Operator approval was issued for request `AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-REQUEST-20261022-01.json` (SHA-256 `87cc793c5460625d50911d2502c5ec688ee3f609d728563e2287ecdffce73351`), authority `AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-20261022-01`, action `AUTHORIZE_ONE_KNOWN_PROCESS_CLEANUP_WITH_LAUNCH_ARGV_RECONCILIATION` (transcription: DECISION JSON, same date).
- Execution outcome: **STOP_BEFORE_PROTECTED_INVOCATION_ARGV_CONTAINER_TYPE_MISMATCH**. Protected invocations 0, signals 0, /proc reads 1, disk access 0, budget consumed 0, no retry consumed, no signal wait begun. Actual current state of PID 2063940: `SAME_ORIGINAL_BIRTH_PRESENT_AT_2026-10-22T19:30:27.739878+00:00` (state S, UID 0; no full signal identity verification) — point-in-time snapshot only; no persistent or current/future state claim.
- Post-review readonly check: after the initial review, Root made ONE authorized readonly birth/state/UID check at 2026-10-22T19:30:27.739878+00:00: PID 2063940 present with matching boot `2980de59-4632-4e7a-a253-5498c094f169` and startticks 80682543, UID 0, state S — same original birth present. No exe/argv reads; target exe and launch argv remain the approved expected values, NOT freshly re-observed.

## Review finding — the defect is in OUR approved request, not a process observation

- The approved request mandates capability argv encoding `tuple(os.fsencode(arg) for arg in exact_target.expected_launch_argv)`.
- The exact unchanged reviewed library `/home/isa/aucdev023-r1-executor-remediation-20261021-01/implementation/offline_inspection_executor.py` (SHA-256 `98bdac4ef805498b31a7374deaa4fe121c3642f4f48e6f2bc66dd7d82439244c`) returns argv as a **list** of bytes from `argv_list` (line 1374), and `signal_verified` (line 1047) compares `argv != cap.argv` directly.
- In Python a list and a tuple compare unequal even when every byte element is identical; the synthetic literal check result `PASS_DEMONSTRATES_MANDATORY_REFUSAL` confirms the mandatory rejection.
- Conclusion: the approved capability encoding as written can never pass the library's mandatory equality gate — a compatibility defect in the request itself. No actual process mismatch was observed and none is claimed. Root stopped correctly before any protected invocation.

## Exact identities

- Approved request: `AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-REQUEST-20261022-01.json`, SHA-256 `87cc793c5460625d50911d2502c5ec688ee3f609d728563e2287ecdffce73351`.
- Authority `AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-20261022-01`; Root-only through the unchanged `signal_verified` library above.
- Target: pid 2063940, boot `2980de59-4632-4e7a-a253-5498c094f169`, startticks 80682543 (same original birth confirmed present by the one readonly check above); exe `/usr/bin/qemu-nbd` and expected launch argv SHA-256 `c06d31cd7abb171ed5004e08d47ff96414aa8a499b6b85320aa222434c8dd24d` remain the approved expected values, NOT freshly re-observed this operation; UID 0 required before signal.
- Pre-invocation review evidence: `evidence/CONTROL-ROOM-PREINVOCATION-REVIEW.json`, observed 2026-10-22T19:29:10.894511+00:00; seven retained binding hashes all match; no source changes.

## Preserved unchanged

- Original observation outcome `TEARDOWN_INCOMPLETE_STOP`, missing post-hash, resource lifetime violation 1890.639 s > 900 s.
- The original empty birth-argv capture (digest `e3b0c44298fc1c14`) stays FAILED evidence; the new cleanup basis does not repair historical evidence.
- All prior incidents/LOST/frozen G5–G12, conditional G12/UNACTIVATED credential: unchanged. Disk safety/immutability/qualification: NOT_ESTABLISHED.

## Correct next action — only

A narrow operator amendment of the cleanup-only capability argv encoding from `tuple(...)` to `list(os.fsencode(arg) for arg in exact original expected_launch_argv)` with byte-identical elements, count, and order — nothing else. All other approved identities, preconditions, target checks, and limits are retained exactly: original PID/boot/start/exe, UID 0, byte-exact argv digest, unchanged library hash/path, Root-only invocation, one invocation, one SIGTERM, 10-second wait, 60-second total, no retry/fallback/SIGKILL/recapture, mismatch ⇒ no signal STOP. **No budget refresh.** Proposed (NOT authority) in `AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-ENCODING-AMENDMENT-REQUEST-20261022-01.json`.
