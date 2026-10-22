# AUCDEV-023-R1 GPT Metadata Observation Result — 2026-10-22

Single authorized invocation of `AUCDEV-023-R1-GPT-METADATA-OBSERVATION-20261022-01`; final disposition **TEARDOWN_INCOMPLETE_STOP**. Record-only document; no completion, disk-unchanged, or safe-start claim is made here.

## Invocation and binding

- Launched **EXACTLY ONCE** by Codex Root-controlled orchestration of the immutable collector; GLM file-preparation tools had no shell access. `invocation 1`, `retries 0`.
- Command: `sudo -n /usr/bin/python3 /home/isa/aucdev023-r1-gpt-collector-20261022-01/implementation/gpt_metadata_collector.py`
- Started `2026-10-22T18:28:26.869665+00:00`, ended `2026-10-22T18:28:29.570985+00:00`; **exit 1 in 2.701 s**.
- Observed pre-entry repository checkpoint `3c9a5e3d9d53808dd48a33bb08cae6f8ed5d1dca` (recording commit may descend); immutable source/deps unchanged (all six reviewed-source pins verified at the pre-entry pure gate, which passed: `PURE_GATE_PASS_NO_REAL_ENTRY`, gate facts valid).
- Binding: authority `AUCDEV-023-R1-GPT-METADATA-OBSERVATION-20261022-01`; attempt `AUCDEV-023-CAND730D2B29-FRESH-AUDIT-20261002-01-AUDITOR-A-R1`; observation session `20261022T182826Z-45d0e8f6abed4235`; approved request SHA-256 `31bafb03733444ce7d8271cccdfbb934a3cf40383f6676d8820e593eb13fff59`; operator decision SHA-256 `9441f783883ac82562abb6e10dee2f75e5cf0e2b8ef2097ae5c8d1504bf1276c`; collector source SHA-256 `ca3bdcc5de98c816512b23d8f1057f521b5afb19bd01cb5b32ad0012d94dfc2c`; producer result SHA-256 `202500ea0cbb9a4ebf3b50c4e5c20a08384adab7cf7b12f72173cb75fcc01bf0`.
- The existing decision is **USED** for this invocation; no retry, resume, or remint.

## Pre-content admission passed; format check within the first authorized hash

Genuine kernel no-atime proof on the HELD source fd (`kernel_fstatvfs_ST_NOATIME`, `noatime_fs: true`); source metadata uid 0 / nlink 1 / size 1747124224 with zero content reads before prechecks; qcow2 standalone-format precheck with declared virtual size 42949672960 verified via header prefix (no extra read); quiescence via REAL_FIXED_FORMS readonly domain queries (name and UUID both absent, healthy); accepted XML verified (4417 B, domain pins exact, required state UNDEFINED); workroot held dirfd uid 1000 mode 0700 with marker `GPT-METADATA-OBSERVATION-ADMISSION.json` retained.

## Identity hash (first content read)

One full streaming SHA-256 over exactly 1747124224 bytes performed BEFORE the map, as the FIRST original-disk content read: **verified equal** to `d1de371a0d07ef97fd1d55c794c9a05a4972b9119f3f55fda86e119dbbda321e`. `hashes_performed: 1`.

## NBD map and metadata reads

ONE read-only, persistent, foreground qcow2 NBD map through the held O_NOATIME/O_NOFOLLOW fd (`socket map.sock`), then exactly **3 metadata reads, 17408 aggregate bytes** (MBR 512 + GPT header 512 + entry array 16384; `crc_ok: true`, `reads_used: 3`). Protective MBR valid (`protective: true`, protective size LBA 83886079); header geometry validated BEFORE the entry read (`entries_start_lba 2`, `first_usable_lba 34`, `last_usable_lba 83886046`, `n_entries 128`, `backup_lba 83886079`); bounds valid and **no overlaps** (`overlap_pair_count: 0`). The **backup GPT was NOT read and NOT verified** — only primary structures were examined.

## Observed primary GPT data (exact copy from `evidence/OBSERVED-GPT-METADATA.json`)

```json
"rows": [
  {
    "classification": "bios_boot",
    "classification_reason": "BIOS boot partition type GUID (util-linux pt-gpt-partnames); recognized type, never a root candidate.",
    "first_lba": 2048,
    "last_lba": 4095,
    "length_bytes": 1048576,
    "length_sectors": 2048,
    "overlaps_other": false,
    "partition_number": 1,
    "range_valid": true,
    "recognized": true,
    "root_capable_type": false,
    "type_guid": "21686148-6449-6e6f-744e-656564454649",
    "within_usable": true
  },
  {
    "classification": "esp",
    "classification_reason": "EFI System Partition type GUID; recognized type, never a root candidate.",
    "first_lba": 4096,
    "last_lba": 618495,
    "length_bytes": 314572800,
    "length_sectors": 614400,
    "overlaps_other": false,
    "partition_number": 2,
    "range_valid": true,
    "recognized": true,
    "root_capable_type": false,
    "type_guid": "c12a7328-f81f-11d2-ba4b-00a0c93ec93b",
    "within_usable": true
  },
  {
    "classification": "root_x86_64",
    "classification_reason": "Discoverable Partitions root x86_64 variant type GUID; describes partition type only — no architecture or filesystem-root proof.",
    "first_lba": 618496,
    "last_lba": 83886046,
    "length_bytes": 42632986112,
    "length_sectors": 83267551,
    "overlaps_other": false,
    "partition_number": 3,
    "range_valid": true,
    "recognized": true,
    "root_capable_type": true,
    "type_guid": "4f68bce3-e8cd-4db1-96e7-fbcaf984b709",
    "within_usable": true
  }
]
```

Geometry (exact): `disk_lbas 83886080`, `declared_disk_size_bytes 42949672960`, `entry_size 128`, `num_entries 128`, `entry_array_bytes 16384`, `entry_array_sectors 32`, `array_reserve_sectors 32`, `metadata_bytes 16988`, `first_usable_lba 34`, `last_usable_lba 83886046`, `backup_lba 83886079`, `entries_start_lba 2`.

## Layout assessment — limits of the claim

- Partition 3 is a **recognized `root_x86_64` TYPE only** (Discoverable Partitions root x86-64 variant GUID `4f68bce3-e8cd-4db1-96e7-fbcaf984b709`). This describes the partition TYPE — **no actual filesystem was identified, no root was selected, and no SAFE claim is made**: `root_partition: null`, `operational_admission: false`, `supported_root_layout: false`, `ambiguity: single_candidate_never_selected`, refusals `single_candidate_diagnostic_only_never_admitted`, `layout_assessment: recognized_types_only`, `row_count_used: 3`.
- The old generic-Linux predicate result (`count 0`, `other_typed 3`, refusal `ROOT_NOT_UNIQUE gpt_linux_candidates=0 other_typed=3`, guid `0fc63daf-8483-4772-8e79-3d69d8477de4`, `would_admit false`) is now **explained by the recognized root-type variant**: the root-capable partition carries the Discoverable-Partitions root x86-64 GUID rather than the generic Linux filesystem GUID.
- `safe_start: NOT_ESTABLISHED`; `status: validated_primary_only`.

## Teardown refusal and residual process

Cleanup of the qemu-nbd map child **PID 2063940** was REFUSED — `SIGNAL_REFUSED_IDENTITY_MISMATCH`, `stage=argv`:

`diag_own_child(initial_exe=/usr/bin/qemu-nbd initial_argv_digest=e3b0c44298fc1c14 initial_ticks=80682543 boot=2980de59-4632-4e7a-a253-5498c094f169 current_exe=/usr/bin/qemu-nbd popen_args=/usr/bin/qemu-nbd --read-only --persistent -f qcow2 -k /home/isa/aucdev023-r1-gpt-collector-20261022-01/work/map.sock /proc/self/fd/4)`

- The birth argv digest `e3b0c44298fc1c14` is the **empty-input digest**: the **full initial argv was NOT_ESTABLISHED** at capture (`EMPTY_CAPTURE_NOT_ESTABLISHED`). Original boot/startticks/exe WERE recorded.
- The later **read-only known-process review** (`evidence/KNOWN-PROCESS-READONLY-REVIEW.json`; not a new capability) confirmed **SAME birth** (boot `2980de59-4632-4e7a-a253-5498c094f169`, startticks `80682543`, `SAME_RECORDED_BIRTH_PRESENT`, state `S`), **same exe** `/usr/bin/qemu-nbd`, and current argv **exactly matching the reviewed launch argv** (`current_argv_matches_reviewed_launch: true`, argv SHA-256 `c06d31cd7abb171ed5004e08d47ff96414aa8a499b6b85320aa222434c8dd24d`); `birth_still_matches_after_review: true`. Reviewed launch argv (exact):
  1. `/usr/bin/qemu-nbd`
  2. `--read-only`
  3. `--persistent`
  4. `-f`
  5. `qcow2`
  6. `-k`
  7. `/home/isa/aucdev023-r1-gpt-collector-20261022-01/work/map.sock`
  8. `/proc/self/fd/4`
- The underlying exec/proc race remains a **HYPOTHESIS** — arbitrary argv tampering is NOT confirmed and is not claimed.
- The existing immutable `capture_birth` code path allows two matching empty samples; the code is unchanged and is not edited.
- The QEMU process was **live at the last read-only snapshot**; the full-argv observation applies to that snapshot only; a separate later handoff birth/state check is recorded below. **No corrective signal was issued** (`signals: 0`, `original_disk_operations: 0` in the review).
- All other children had already exited; `map.sock` left to the live process; marker retained; source fd stable through cleanup.

## Post-identity and claims NOT made

- `post_identity: NOT_PERFORMED_TEARDOWN_INCOMPLETE` — the second full hash was NOT performed; **no completion claim, no disk-unchanged claim, and no safe-start claim**.

## Operation counters

Real disk full hashes 1; NBD maps 1; metadata reads 3; guest filesystem access 0; FUSE 0; VM lifecycle mutations 0; QGA 0; PREARM 0; credential access 0; auditor execution 0 (`protected_auditor_execution: false`); qualification/installation changes 0 (`qualification_installation_changed: false`).

## Preserved history

All historical incidents, the LOST pre-freeze observation limitation, and qualification NOT_ESTABLISHED status remain unchanged and preserved; frozen G12/credential scope unchanged.

## Proposed next step (NOT authority, NOT executed)

One minimal proposed residual-cleanup disposition request: [AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-REQUEST-20261022-01.json](AUCDEV-023-R1-GPT-METADATA-RESIDUAL-CLEANUP-REQUEST-20261022-01.json). Until an actual human decision, the STOP remains in force; no retry, resume, or continuation of the observation.

## Evidence index

- `evidence/PREENTRY-IDENTITY-AND-AUTHORITY.json` (workspace `/home/isa/aucdev023-r1-gpt-metadata-observation-20261022-01/`)
- `evidence/ENTRY-INVOCATION.json`
- `evidence/ENTRY-EXIT.json`
- `evidence/OBSERVED-GPT-METADATA.json` (producer result SHA-256 `202500ea0cbb9a4ebf3b50c4e5c20a08384adab7cf7b12f72173cb75fcc01bf0`)
- `evidence/KNOWN-PROCESS-READONLY-REVIEW.json`

AUCDEV-023 P1/READY/NOT_DONE.

## Independent Control Room assessment

Codex independently checked the exact approved request/decision/source/control hashes, actual single-entry call and exit, producer record, phase ordering, all GUID/range/length values, and the birth-first read-only known-process review. Primary-GPT integrity is supported by the observed header/table CRC and bounds; end-to-end disposition remains **TEARDOWN_INCOMPLETE_STOP**, not completion or safe-start. The original full argv was not established; current launch-argv equality does not retroactively repair it. The prior inert tests and Control Room review did not catch acceptance of an empty birth-argv capture; the real run exposed this missing negative case. The underlying exec/proc mechanism remains a hypothesis. No source changes, retries, corrective signals or second disk hash occurred. Read-only domain queries: 2; VM lifecycle/guest/QGA/PREARM/credential/auditor operations: 0. Existing stopped invocation is USED. The proposed cleanup disposition is a separate permission to adopt a cleanup-only identity basis, not an authority already granted and not an amendment of the failed observation.

## Later handoff resource-lifetime failure

At `2026-10-22T18:59:59.900016+00:00`, an additional **read-only original-PID birth/state check** found PID2063940 still in state `S`, with the same original boot/startticks. No exe/argv was re-read in that check, no signal or original-disk operation occurred. Its measured lifetime was **1890.639 seconds**, exceeding the **900-second** operation/resource bound. The collector entry finished in2.701seconds, but that does **not** establish bounded lifetime or successful teardown of its residual exporter. The resource-lifetime limit is **NOT SATISFIED**; this is retained as an observed failure, not relabeled as compliance. STOP remains; the pending request is a new narrow identity-basis decision for cleanup only.
