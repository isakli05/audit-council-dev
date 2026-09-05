# Audit Council Dev

Audit Council is an independent audit skill and deterministic Python harness for
reviewing a Git repository against a frozen brief. Claude Opus and Codex perform
separate reviews, challenge each other's findings, preserve disagreements, and
produce a report with explicit evidence, completeness, and a GO/NO-GO recommendation.

This is the owner's development source and knowledge base for Audit Council itself.
The **Audit Council Dev** ChatGPT Project is its human-in-the-loop development
control room. This repository is not an open-maintainer community project.

## Current maturity

The current runtime source includes v2.0.1 operational hardening; its public protocol
version remains **2.0**. Deterministic tests and historical implementation evidence
exist. See [current state](docs/chatgpt-project/AUCDEV-CURRENT-STATE.md) for exact
SHAs, installed identity, validation, and the unresolved qualification-record gap.
Do not interpret the latest branch or passing unit tests as release qualification.

Mechanical blindness between independent-stage filesystem views is still open.
The evidence store's API visibility policy does not isolate raw files. Claude's
path guard is a lexical detection/hardening layer; Codex's stronger read confinement
requires bubblewrap and still exposes its documented bind set, including its own
auth/session directory. Read the [known limitations](AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md).

## Use and development model

The installed Claude Code skill is invoked explicitly with `/audit-council`.
Opus is the interactive orchestrator; the harness launches Codex directly and
resumes a stored explicit session ID. The audited source stays immutable.
Environment modes are AUTO, CURRENT, RELEASE, and HISTORICAL. RELEASE/HISTORICAL
use detached exact-target worktrees, verified bindings, authorized evidence staging,
and archive-before-removal. Runtime registry and lifecycle roots are managed separately.

The supported/probed baseline is Linux, Python 3.14 standard library, Git worktrees,
Claude Code, Codex CLI with subscription authentication, and bubblewrap with working
user namespaces. Historical qualification used Codex CLI 0.153.0 and bubblewrap
0.12.0. This is not a claim that all OS/CLI versions are qualified.
The runner rejects PAYG credential fallback. See the
[canonical human contract](skill/PUBLIC-CONTRACT.md) and [skill instructions](skill/SKILL.md).

A previously installed qualified Audit Council audits each candidate in a fresh
Claude Opus session. A candidate must not qualify itself. Implementation, independent
audit, operator acceptance, and installation are distinct transitions with exact
SHAs and evidence. Follow the [control-room runbook](docs/chatgpt-project/AUCDEV-CONTROL-ROOM-RUNBOOK.md).

Non-goals: apply product fixes during audits, silently turn partial audits into
complete ones, manufacture consensus, replace independent evidence with model
agreement, or build a fully autonomous coding/remediation lifecycle now.
STANDARD/RELEASE/FORENSIC effort policies are future design work, not current flags.

## Repository layout

| Path | Purpose |
|---|---|
| `skill/SKILL.md` | Installable Opus orchestration policy |
| `skill/PUBLIC-CONTRACT.md` | Canonical human-facing contract; no duplicate root copy |
| `skill/protocols/`, `skill/prompts/` | Audit stages and model prompts |
| `skill/scripts/`, `skill/hooks/`, `skill/schemas/` | Deterministic lifecycle, guards, validation |
| `skill/tests/`, `skill/eval/` | Unit/regression, seeded scoring, historical replay tools |
| `docs/chatgpt-project/` | Project instructions, current state, backlog, workflow, Sources manifest |
| `AUDIT-COUNCIL-V2-*.md`, `plans/`, `repro/` | Dated design/implementation/evaluation/migration evidence |
| `smoke-fixture`, `smoke-fixture-103` | Historical gitlinks; local run data is not published by these pointers |

Ordinary clones contain all deterministic skill tests. The two historical gitlinks
have no `.gitmodules` mapping; do not use recursive submodule initialization to
recover them. Their portability is tracked in the backlog; local originals remain intact.

Run the deterministic suite from the repository root:

```sh
python3 -m unittest discover -s skill/tests
git diff --check
```

No paid model audit is implied by these checks. Historical replay and real-model
evaluation require their own explicit scope and budget. Read
[architecture orientation](docs/chatgpt-project/AUCDEV-ARCHITECTURE-SUMMARY.md),
[documentation map](docs/REPOSITORY-DOCUMENTATION-MAP.md), and
[engineering backlog](docs/chatgpt-project/AUCDEV-BACKLOG.md).

## ChatGPT Project setup

Copy [Project Instructions](docs/chatgpt-project/AUDIT-COUNCIL-DEV-PROJECT-INSTRUCTIONS.md)
into **Audit Council Dev → Project settings → Instructions**. Keep the operator's
PROJECT-ONLY MEMORY configuration. Add the exact compact files listed in
[Project Sources Manifest](docs/chatgpt-project/PROJECT-SOURCES-MANIFEST.md).
Prefer connected GitHub for live code and verify the retrieved SHA. Uploaded Sources
are manually refreshed snapshots. The baseline ZIP is historical and needs no
replacement after each development cycle.

## Ownership, license, and reporting

Public visibility permits reading and GitHub forking; it grants no collaborator,
push, or merge authority. Unsolicited maintenance/contribution workflows are
restricted. See [contribution policy](CONTRIBUTING.md), [security policy](SECURITY.md),
and the [verified publication record](docs/REPOSITORY-PUBLICATION-RECORD.md).

No LICENSE has been selected. No additional reuse/distribution license is granted
by this repository; the owner decision is AUCDEV-014. Do not assume public visibility
means an open-source license or public-maintainer governance.
