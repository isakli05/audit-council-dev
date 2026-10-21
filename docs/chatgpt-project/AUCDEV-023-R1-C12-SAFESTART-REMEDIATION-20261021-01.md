# AUCDEV-023 R1 C12 + safe-start remediation — final consolidated record (2026-10-21)

Record-only consolidation by the GLM-5.3 implementer (Lanes A+B ended
normal 0). Codex Control Room owns independent review, publication and the
final archive. Nothing here grants authority; no protected operation was
performed. Baseline checkpoint `2685205a607f844d3fea1516fbe9549d88448f2d`
(last Codex-verified GitHub master; no own-commit SHA referenced).

## C12 disposition: CLOSED_AT_REVIEWED_PREPARATION_TARGET

- Codex fresh review (`CONTROL-ROOM-C12-REVIEW.json`, disposition
  CLOSED_AT_REVIEWED_PREPARATION_TARGET, effective on publication)
  independently reviewed the exact sources/evidence and verified every
  immutable Git citation in the binding descriptor; technical closure is
  NOT runtime admission.
- Reviewed tuple, all byte-exact at the local paths:
  adapter `568a965af25a20e30bb3e9c00cde2f739266c39dc23056bde6b127be9d633090`
  and test `f3f9145f2ad46c23d95f26a97475a26864b96b474d7746b6c45ceaf3a4f52e92`
  in `/home/isa/aucdev023-prelaunch-remediation-20261021-01/section-a/`;
  descriptor `8c5c4b64c22e312fe5948cdb9a8a3d91e2ada16fa02ac84c36dca447bf75dcf8`
  (5349 B, `docs/chatgpt-project/AUCDEV-023-R1-GENUINE-XML-BINDING-20261021-01.json`;
  byte-exact frozen copy in `section-a/c12/fixtures/genuine/`).
  Pre-C12 baselines `4702daac…`/`aae40fc0…` preserved read-only in
  `section-a/c12/baseline/` (exact).
- Current evidence: focused v2.5 battery 33/0/0, rc 0, result
  `section-a/c12/results/BATTERY-FOCUSED-C12-V2.5-20261021T133758.json`
  (sha256 `6d8e6d79b7c5e67526d51d635f181712f4deaf7a8183fed6222e99524a4a77c3`);
  the v2.4 full 107/0/0 belongs to the older source `d72ba84c…` and is NOT
  current-source evidence; v2.3/v2.4 results, all failure history and the
  RED→GREEN namespace transcripts are retained as lineage.
- Closure shape: only the exact reviewed target + descriptor with the
  accepted persistent XML `065096925d…`/4417 B is admitted; any physically
  live XML divergence (runtime-added fields included) REFUSES pending
  exact fresh review — never normalized, never a historical substitute.
  Seam domain item is the bound UUID; the domain name token class stays
  forbidden by the frozen builder.
- Authority: existing G12/credential scope NOT expanded. The immutable
  credential request's `reviewed_preparation_sources_sha256` old
  adapter/test hashes remain untouched historical reviewed-source context;
  the new tuple received Codex FRESH review — no inherited old PASS, no
  automatic real use. G9 package, grant, G10 receipt and the historical
  G11 static-only verdict are exact and unchanged. No repeated
  G12/credential/VM-cycle approval is requested.
- Lifecycle interpretation (Codex `CONTROL-ROOM-AUTHORITY-INTERPRETATION.json`):
  future exact-domain define → ONE conditional start → permitted
  read-only checks → clean shutdown → undefine mechanics are COVERED by
  the existing `AUCDEV-023-R1-VMQGA-LIVE-PREFLIGHT-20261021-01` authority,
  conditional on pre-start safety evidence and the SAME accepted
  VM/disk/XML identities. This remediation itself forbids ALL such
  actions and performed NONE — zero lifecycle operations occurred.

## Safe-start: PARTIAL, never PROVEN

- Host/container metadata and full disk provenance are known for the exact
  current disk `d1de371a…`/1747124224 B; every guest-internal startup
  mechanism class for these bytes remains UNPROVEN; NO content inspection
  of the real disk was performed or authorized. Evidence:
  `/home/isa/aucdev023-r1-c12-safestart-remediation-20261021-01/safe-start/SAFE-START-EVIDENCE.json`
  (PARTIAL).
- A validated persistent root-context NBD/FUSE read-only inspection method
  exists — NO whole-image/partition copy; the only disk bytes held outside
  the read-only exports are ONE bounded <=1 MiB partition-metadata buffer,
  parsed locally then deleted (proved end-to-end on inert scratch only:
  `SCRATCH-VERIFICATION.json`, final chain COMPLETE; real inspection NOT
  authorized, NOT performed; the inert proof used manual follow-up steps
  under the foreground FUSE — not claimed as one automated script).
- Final corrected proposal — Lane B rev5 + Control Room review corrections
  under the operator remediation mandate (NOT an operator approval of the
  proposed scope), local copy synchronized byte-exact:
  `docs/chatgpt-project/AUCDEV-023-R1-OFFLINE-STARTUP-INSPECTION-REQUEST-20261021-01.json`
  sha256 `90fb50fcac1598df67fd2d044f0e9a03dce32fc672211469020f5c43184800e5`,
  22178 B; proposed authority
  `AUCDEV-023-R1-C12-SAFESTART-OFFLINE-INSPECTION-20261021-01` (NO approval
  issued; no self-hash; no future commit). Corrections: runnable `h.pread`
  minimal-metadata probe (bounded <=1 MiB buffer, only required MBR/GPT
  blocks, parsed locally then deleted; unknown map => STOP); absolute 0700
  work-root paths; explicit qcow2; pre-read component-safe source identity
  (UID 0/nlink 1/quiescence, hash before/after, no force-share); partition
  bounds within 40 GiB; NO persistent host-configuration or unrelated
  host-state change (only the named ephemeral read-only NBD/FUSE/PID/work
  artifacts plus exact teardown); exact-PID teardown with starttime
  recheck before signal; secret-looking/unknown-ref STOP rules; debugfs
  path validation; bounds 2048 reads / 256 KiB / 16 MiB; decision fields
  APPROVE_ONE_READ_ONLY_OFFLINE_STARTUP_INSPECTION or WITHHOLD (single
  conditional invocation after prechecks; no second go-marker;
  OPERATOR_SEND_NOW stays forbidden).

## Visible scope deviation (one row; full ledger in SCRATCH-VERIFICATION)

- Lane B inert-scratch teardowns executed 4× `sudo -n pkill -x qemu-nbd` and
  1× `sudo -n pkill -x nbdfuse` host-wide name kills (Codex independently
  counted the executed scripts); corrected permanently to exact owned-PID
  identity-validated cleanup. No per-moment pre-kill census was retained:
  no unrelated impact or victim established, NO universal no-impact claim;
  no raw logs enter this public record — full ledger in SCRATCH-VERIFICATION.

## Status

- Real/protected counters ALL 0 (VM starts, define/undefine/shutdown,
  QGA, PREARM, credential operations incl. sender/marker/window/budget,
  auditor/model executions, run_attempt, installs); qualification and
  installation unchanged, provenance NOT_ESTABLISHED; the historical LOST
  pre-freeze observation remains LOST. AUCDEV-023 remains **P1 / READY /
  NOT DONE**.
- Remaining blocker: guest-internal startup inventory for the exact current
  disk `d1de371a…` (NOT_ESTABLISHED). ONE next action: the operator decides
  on the EXACT offline inspection request above — nothing else requested.
- No final archive created. Codex checks the diff, publishes, and builds
  the final tar LAST.
