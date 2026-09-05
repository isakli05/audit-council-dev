# Security and sensitive evidence

Do not post credentials, private repository content, audit ZIPs, authentication or
session state, or sensitive exploit evidence in public GitHub content.
The repository does not operate a public issue queue, bounty program, or guaranteed
response-time service. No dedicated security contact address is established here.
Use an existing private channel with the owner for an authorized security report.
If no such channel exists, do not publish sensitive evidence to obtain attention.

Audit Council is not a fully isolated hostile-code analysis environment. Read
[known limitations](AUDIT-COUNCIL-V2-KNOWN-LIMITATIONS.md) before relying on its
confinement, independence, integrity, or completeness claims. Version labels alone
do not establish qualification; use the exact installed source and evidence record.

Before any publication, review both the intended tree and reachable Git history.
If a probable credential or clearly private data is present, stop before push.
Preserve evidence; arrange credential revocation/rotation where needed, and obtain
the owner's explicit decision about disclosure or a separately planned history
remediation. Removing a file in a new commit does not remove its historical content.
Never rewrite Git history automatically to pass a scan.

Prefer sanitized deterministic reproductions of production harness failures.
Keep original runtime archives in their existing private locations. Check provenance,
realpaths, symlinks, digests and audience before any evidence ingestion; do not
weaken deny-lists as a shortcut.
