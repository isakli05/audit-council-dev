# AUCDEV-023 R1 — Inert GPT diagnostic remediation

2026-10-22 · Verified baseline `6d397de463dccd60e7a5a1dd2dde4b19343d71a9`, master. W = `/home/isa/aucdev023-r1-gpt-diagnostic-20261022-01`. GLM-5.3 implemented through `cc-zai --dangerously-skip-permissions`; Codex separately reviewed source, predicates, tests and actual tool events. This is the managing Control Room assessment, not an external qualified audit.

| Required outcome | Disposition |
|---|---|
| Root cause | **CONFIRMED** diagnostic limitation: frozen executor counts ONLY generic Linux filesystem GUID entries and refuses unless count equals one; non-generic types are collapsed to `other_typed`, losing useful type/range evidence. The observed 0/3 refusal is valid fail-closed behavior; whether the ACTUAL layout is valid/unsupported/ambiguous remains UNKNOWN. |
| GPT diagnostic | **ACCEPTED_INERT** for exact new pure component only; no operational integration or inherited runtime verdict. |
| Synthetic tests | **PASS: 26/26 named groups**, 0 failures, runner exit 0 and GLM CLI exit 0. Additional independent Codex probes 5/5; guard-core checks 2/2; one native denied-command probe PASS. Counts are groups/probes, not an invented assertion total. |
| Actual disk startup safety | **NOT_ESTABLISHED**. Actual GPT GUIDs/ranges remain unavailable; no current disk was inspected. |
| Real-disk access | **ZERO** reads, hashes, stats, NBD or FUSE. VM/QGA, PREARM, credential, auditor execution and protected-attempt consumption all 0. |
| Next evidence step | Prepare and independently review the exact source-bound metadata-only collection entry, then complete its producer binding in the existing scoped request before seeking the one new operator decision. |

## Exact reviewed output

- New `W/implementation/gpt_diagnostic.py`: **20534 B**, SHA-256 `78d3fde645f532e5f1d257b547fe89d4e48be5062883d0fd5740476c1eae96f3`.
- `W/tests/run_inert_checks.py`: SHA-256 `7b4f2fef2d2cb713645e095dc5d38317b588fda192ce2678c92f858b9bfe7317`; source-only loader, synthetic in-memory buffers, only fixed code/evidence IO. No operational executor import. Before/after reviewed pins equal.
- Validation JSON: SHA-256 `fbc5382f618daf6cbcde7bf35bced3e3807e2f0479c67d89e9f49df70929eba4`; evidence `W/evidence/INERT-VALIDATION.json`, `SYNTHETIC-DIAGNOSTICS.json`, `ROOT-INDEPENDENT-INERT-PROBES.json`, `ROOT-FINAL-TECHNICAL-REVIEW.json`.
- Original executor remains byte-identical at `98bdac4ef805498b31a7374deaa4fe121c3642f4f48e6f2bc66dd7d82439244c`. It was NOT patched or re-executed; Codex AST-executed only its two pure GPT functions/constants against synthetic bytes for independent predicate checks. No G5–G12, grant, package, receipt or existing approval changes.

## Semantics and meaningful coverage

The new pure function takes explicit MBR/header/table bytes and declared virtual size; it cannot open files, invoke tools or select a root. It retains canonical type GUIDs, partition numbers, LBAs, lengths, classifications and validation/refusal reasons. Generic Linux FS, discoverable x86-64/ARM64 root variants, LVM, ESP, BIOS boot and swap are labeled; unknowns remain unknown/unsupported. A type label never proves filesystem, architecture or root identity. `root_partition=null` and `operational_admission=false` always; LVM containers, unknown types and ambiguous candidates have explicit refusal reasons.

Coverage includes positive generic/typed/relocated arrays; two DIFFERENT synthetic type layouts that both produce the actual old predicate's 0/3 count; multiple candidates; unknown/mixed types; corrupted header/table CRCs; malformed/hybrid PMBR and exact PMBR size; truncated/excess/oversized buffers; geometry/reserve/device bounds; ALL-entry invalid ranges and overlaps including unknown types; 512-entry worst-case overlap (exact 130816 pair count, only 16 pair details); no partition-name/unique-GUID/raw-byte leakage. Oversized inputs refuse BEFORE CRC; CRC consistency is not authenticity.

Profile is 512-byte sectors, 92-byte header body, 128-byte entries, <=512 entries and <=1 MiB total input metadata. Only supplied primary structures are checked; backup GPT, unique-GUID uniqueness and full UEFI conformance are not certified. No filesystem inspection or actual-source authentication is supplied by this pure consumer.

Primary references: [UEFI GPT](https://uefi.org/specs/UEFI/2.10/05_GUID_Partition_Table_Format.html), [Discoverable Partitions Specification](https://uapi-group.org/specifications/specs/discoverable_partitions_specification/), [util-linux type GUID table](https://raw.githubusercontent.com/util-linux/util-linux/master/include/pt-gpt-partnames.h). These justify metadata validation/type labels, not R1 root selection or permission.

## Rejected drafts and control limitation — preserved

Initial draft `41cd66176bd2c40dfad4289037e6ee2107a8e6c12c38342af7dc91317da9e4df` still CRC-scanned oversized input; independent synthetic probe demonstrated this before acceptance. Revision-2 `5c78b22d5df77a483fdacfa017d6f661289b101b0f58688ed49f07052a90a450` lost an array-placement check; synthetic counterexample demonstrated it. GLM fixed both and test-fixture/prefix-matching defects before the single 26-group run. Failed draft bytes/findings remain in W/evidence; no test failures or source history were rewritten. Minor comment correction: the restored array-end rule came from the first diagnostic draft, not the frozen executor; no stronger historical check is claimed.

The 26-group run's custom plugin DID NOT load; Codex detected the missing enforcement only after completion. Actual command was the exact safe runner and root-readonly source pins were unchanged, so results stand, but there is NO retroactive hook-enforcement claim. GLM removed only the erroneous manifest hooks field; Codex then confirmed plugin startup BEFORE the native `:` probe, which was denied before execution and latched STOP. The expected negative-test latch is preserved. No unchanged diagnostic suite rerun. Exact evidence: `ROOT-PLUGIN-CONTROL-GAP.json`, `ROOT-GUARD-REMEDIATION-VERIFICATION.json`, `SANITIZED-TOOL-AUDIT.json`. Review observes outer tool events and pinned source/results, not a separate kernel/per-read audit.

## Authority and remaining boundary

The prior real inspection is USED. [GPT metadata observation scope request](AUCDEV-023-R1-GPT-METADATA-OBSERVATION-REQUEST-20261022-01.json) is **PREPARED_SCOPE_REQUEST_NOT_EXECUTION_READY / NOT_READY_FOR_OPERATOR_APPROVAL**, not issued authority. The current work is an inert consumer; no reviewed source-bound metadata-only collector exists. Its source field remains null explicitly. The draft preserves exact disk/event/attempt, limited metadata scope and proposed limits; no old spent entry/marker/budget is reset and no unknown producer is approved. Complete the missing producer source/test binding and fresh review before finalizing that one exact request. No premature approval question or repeated G12/credential decision.

All earlier incidents and unknown impacts remain, including out-of-order reads, missed detection, broad/process-cleanup deviations, missing historical sources, unrelated writes/lookups and permanently LOST pre-freeze observation. Credential authority remains UNACTIVATED, window NOT_STARTED, transfer budget NOT_CONSUMED. Qualification NOT_ESTABLISHED; no installation performed; AUCDEV-023 remains P1/READY/NOT_DONE.
