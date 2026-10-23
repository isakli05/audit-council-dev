# AUCDEV-023 CGR-001 source remediation review — 2026-10-23

**Control Room disposition: CGR-001 RESOLVED_AT_SCOPED_INERT_ONLY_STRENGTH for the exact successor collector/test hashes below.** This is a technical review and PM record, not the independent release audit or full collector acceptance. Live GitHub master was refreshed at `166ffcd6e545550e0d7e77a8a3f8ec9bfdca0df7`; CURRENT-STATE, BACKLOG and the [original failed review](AUCDEV-023-R1-GPT-COLLECTOR-GUARD-REVIEW-20261023-01.md) were read at that SHA, with connector blob IDs matching complete local Git bytes. No Graphify graph exists. No correction was needed or implemented in this review.

Candidate: `/home/isa/aucdev023-cgr001-source-remediation-20261023T062830Z/candidate/`. The documentation HEAD is not candidate identity.

| Exact artifact | SHA-256 |
| --- | --- |
| New `implementation/gpt_metadata_collector.py` | `4547f96361f7519754d44799d53eba8d1df806ee460ef047c89947c266911ae2` |
| New `tests/run_collector_checks.py` | `95b3147bc85691138d09902b8daa56d94d4eab13fb0b140592485fe5851649b9` |
| Frozen predecessor collector | `ed78d98f97b9f6b979f04a842d974bb1f646d1c26cc4b64a6bed1e581e7a6269` |
| Frozen predecessor tests | `82d27ec8d214933d06ad9d11ab680fb5eb958e0df244d6e522fa7d5a9ba5aec2` |
| Unchanged executor library | `98bdac4ef805498b31a7374deaa4fe121c3642f4f48e6f2bc66dd7d82439244c` |
| Supplied `aucdev023-cgr001-source-remediation-20261023T062830Z-HANDOFF.tar.gz` | `b58d276fddf7b5921a86f786dde6034875e2a48614079ac7f6b7e6f950cce319` |

The archive hash, safe member paths/types, all 90 manifest payloads, inventory, nested evidence manifests and archived/local bytes match. Three local files outside the archive (two raw provider streams and launcher UI metadata) are excluded from reliance and this handoff. Frozen originals, original review archive, run007 evidence `7928b035…` and original producer result `202500ea…` still match their prior hashes. This establishes present binding, not complete historical write provenance.

The complete predecessor diff contains exactly two candidate files: collector **+3/-0**, tests **+520/-14**. Production adds only the conditional `launch_exe is not None` deadline tick in `Machine.capture_child`, after child registration validation and before `capture_birth`. Existing post-capture admission, own-child registration, identity checks, cleanup, post-identity logic, every production assignment/budget/deny-list and all 58 original test bodies are unchanged. Tests add six fake-clock groups, counters, fixture factoring, candidate path and result metadata; the full-suite admission gate remains unchanged.

Supplied immutable run inputs, source/driver snapshots, commands, stdout/stderr, process exits and JSON results support:

- **RED-001: 14 PASS / 2 actual behavioral FAIL / 0 BLOCKED**, subprocess exit 1. Exact predecessor `ed78…` and final tests `95b3147b…` are bound before/after. C1 and C2 each actually enter capture once and sleep 51 times / 1.02 virtual seconds. Failure assertions concern acquisition ordering; there are no TypeErrors.
- **GREEN-001: 16 PASS / 0 FAIL / 0 BLOCKED**, subprocess exit 0, using the same final test bytes. Already-expired and exactly-zero walls refuse at `map_child_capture`: **0 capture calls, 0 acquisition exe/argv/starttick reads, 0 sleeps/elapsed virtual time, 0 capabilities, 0 signals**, and no post-capture fd/read-plan work. The one preceding spawn is fake; the registered child remains.
- Expiry during acquisition still runs the unchanged library: C3 records 1 capture, 30 sleeps / 0.6 virtual seconds, then refuses at `map_child_capture_admission` before storing a capability. C1–C3 retain `ALIVE_NO_CAP_RESIDUAL`, live endpoint/marker, incomplete teardown and suppressed post-identity; cleanup neither recaptures nor signals. Positive exact admission and reordered/non-UTF8 argv refusals pass. Supplied separate Codex probe RED/GREEN supports the same ordering; its during-capture case uses 1 sleep / 0.02 seconds.

Evidence strength is source inspection plus verified existing deterministic offline records, with fake clock/process/readers around the pinned library. No tests were rerun: there was no essential behavioral verification gap. Driver records report zero forbidden actual spawn/socket/signal attempts. The `nbd_connections=0` group field is structural, supported by refusal before the instrumented fd boundary; it is not live transport evidence. The fix does not bind internal acquisition waits to the collector wall when capture starts within budget.

Earlier findings remain: CGR-002 coverage limits outside these probes; **CGR-003's unreconstructable interim chronology is not retroactively repaired by the new reproducible RED**; CGR-004 terminology/environment limits; CGR-005 live-child bounded-termination and operational-safety gap. Historical io_uring ENOMEM remains an external observation, with exec/proc race unproved. The original failed review and original **TEARDOWN_INCOMPLETE_STOP**, empty birth-argv FAILED evidence, missing post-hash and 1890.639 s >900 s violation remain unchanged. Disk immutability, startup safety and independent qualification remain unresolved, as do incidents/LOST, frozen G5–G12 and credential holds. The cleanup allowance remains consumed; this record grants no execution, credential, qualification or installation authority. AUCDEV-023 remains **P1 / READY / NOT_DONE**, with counts unchanged.

Publication is limited to this dated record and minimal CURRENT-STATE/BACKLOG insertions; candidate executable code remains outside master. No protected execution, process signal, Root operation, target-disk access, QEMU/NBD/VM/QGA/PREARM, credential operation, original g01–g58 suite, real transport test, release audit, qualification or installation occurred. Full verification, evidence references, exact diff, inventory, manifest and publication outcome are in `/home/isa/aucdev023-cgr001-control-room-review-20261023-01/`.

**Next recommended action:** separately scope a source-only design review of the live-child bounded-termination gap under the existing identity-verification constraints, before considering any new execution or qualification. This recommendation grants no authority.
