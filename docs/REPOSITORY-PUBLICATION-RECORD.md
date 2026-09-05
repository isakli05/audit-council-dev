# Repository governance and publication record

Date: 2026-09-05. Repository: `/home/isa/audit-council-dev`.
Starting HEAD: `8ae33444f349ce73c1359b963722e2d16acba630`; branch `master`.
Initial remotes: none. Initial tag: `v1.0.3-baseline` at
`1a9023714da3a223c009668569d4bfd0ece5dd22`. All 33 starting commits are retained.

## Public-safety gate — PASS for inspected starting history

No probable credential/secret or clearly private customer/project/conversation data
was found in the reviewed parent repository tree and reachable history. This is a
bounded inspection result, not a guarantee of absence of all possible sensitive data.

Installed secret scanners (`gitleaks`, `trufflehog`, `detect-secrets`) were not found
on PATH. Used a local stdlib Git scanner plus manual review, without sending source
to an external scanning backend. Method: enumerate `git rev-list --all`, resolve
every tree/path with `git ls-tree -rz`, inspect all reachable blobs and commit/tag
metadata with `git cat-file --batch`; include deleted historical files. Check known
provider tokens, private-key blocks, credential URLs, JWT/bearer values, quoted and
unquoted credential assignments, suspicious filenames, high-entropy candidates,
emails/home paths and private-data markers. Detect archive signatures and inspect
members in memory if present; none existed in this history.

Starting scan coverage: **33 commits, 781 objects, 526 blobs, 222 trees,
408 distinct historical paths, 4,397 historical tree entries, 3,997,334 bytes** of
blob/commit content. No binary samples, archive members, tracked .env/.npmrc/auth
files, private keys or credential-formatted values were found.

Candidate dispositions:

- 302 entropy hits: 298 generated fixture run paths and four telemetry fixture
  exit-code paths. No opaque credential candidate remained.
- 31 unquoted “secret” rule hits: six unique ordinary code expressions using
  `tokens`, `agg_tokens`, or `real_token = state_store.secrets.token_hex` across
  historical revisions; not assigned credential values.
- 113 home-path and 128 email matches: local path metadata, existing Git author
  identity, and synthetic test identities. Publishing preserved history exposes
  the existing author email and username/path structure; moderate identity privacy
  impact, no authentication authority. No history rewrite was performed.
- 83 private-data keyword hits were reviewed as tool/harness descriptions, synthetic
  fixtures, historical technical reports and owner-product audit evidence.
  The two tracked `skill/tests/fixtures/fifth-*.json` files contain technical findings
  and source references, not credentials, customer records or raw conversation logs.
  Their source repository `isakli05/llm_council_orchestrator` and referenced commit
  `f8c2b2c6955d19df7902cf2efc140ba558af044e` were confirmed publicly accessible via
  GitHub API. This is disclosure of technical audit history of public owner source;
  it is not inferred private merely from a product name. Future minimal sanitized
  fixtures are tracked as AUCDEV-005.
- Historical test-generated active-run registry/job artifacts remain in old Git
  commits. Inspected values are synthetic test paths/state, not host authentication
  material. They were not removed or rewritten for cosmetic cleanup.
- `smoke-fixture` and `smoke-fixture-103` are gitlinks. Their untracked runtime
  archives and nested Git objects are outside the parent publication set and
  remain local. No ~/.codex auth/session files were opened or staged.

Local scanner/report provenance (temporary, not a runtime dependency):
`/tmp/audit-council-public-safety.gGyM3v/scan.py`, `scan.jsonl`, `triage.py`.
The committed governance checkpoint was rescanned before push: **PASS**, 34 commits,
813 objects, 553 blobs, 421 historical paths, 4,277,482 bytes. The six new
credential-filename mentions are exclusion patterns in .gitignore and this report,
not credential files. Entropy/assignment candidate counts were unchanged.
No probable secret or clearly private data was introduced by the new documents.

## Validation

- Deterministic suite: `python3 -m unittest discover -s tests` from `skill/`:
  **574 tests OK in 94.050 s**; no paid model calls. Existing unclosed-file
  ResourceWarnings remain and are tracked in AUCDEV-019.
- Installed identity: **84/84** tracked skill files match starting HEAD, with no
  extra non-cache installed files. No source, test, schema, hook, prompt or executable
  protocol file under `skill/` is changed by this task.
- Markdown links, Project manifest paths, backlog references/counts and
  `git diff --check`: **PASS**. Checked 13 new documents and 51 relative links;
  all manifest paths exist. Backlog: 19 open (P1 8/P2 11), three deferred,
  eight accepted residuals, four bounded evidenced closures. Project Instructions
  are 7,863 characters; architecture summary is 203 lines.
- No installation, Audit Council qualification campaign or historical replay is
  performed. Full suite was run once; test output is not a release certificate.

## GitHub settings and publication

Authenticated active account: `isakli05` (personal account, verified by `gh auth status`
and `/user`). Inactive `isakayadev` account was not selected. GitHub lookup returned
404 for `isakli05/audit-council-dev`, so no existing remote repository was hijacked.

Repository created empty under verified owner before any source push:
`https://github.com/isakli05/audit-council-dev`, ID `1358379094`, GraphQL ID
`R_kgDOUPc4Vg`. Visibility **public**, default branch **master**.
Remote **origin**: `https://github.com/isakli05/audit-council-dev.git`.

Settings were applied and independently read back through GitHub REST/GraphQL:

| Setting | Actual readback |
|---|---|
| Collaborators/write access | Only `isakli05`, role admin; no unexpected write/maintain/admin users |
| Invitations / deploy keys / webhooks | 0 / 0 / 0; no invitations sent |
| Teams | Not applicable: personal-account repository |
| Pull requests | Enabled, `pullRequestCreationPolicy: COLLABORATORS_ONLY` |
| Issues | `has_issues: false` |
| Discussions | `has_discussions: false` |
| Wiki | `has_wiki: false` |
| Repository Projects | `has_projects: false` |
| Branch ruleset | ID `22343195`, **active**, target `refs/heads/master` |
| Rules | `deletion`, `non_fast_forward`; empty bypass actor list |
| Owner workflow | Normal authenticated fast-forward pushes allowed; no PR/review or third-party approval requirement |
| Actions token default | `default_workflow_permissions: read` |
| Actions PR approval | `can_approve_pull_request_reviews: false` |
| Actions execution | Enabled; existing platform `allowed_actions: all`, no workflow files in this repository |

The repository has no fork workflow that receives secrets or an explicit write
token. No CI workflow was added or existing CI requirement removed. Future workflows
must keep explicit permissions minimal and avoid privileged untrusted fork execution.
All requested repository settings were automated; no unsupported-setting fallback
was needed. ChatGPT settings/Sources and account-specific GitHub connection remain
operator UI actions, not GitHub protection failures.

Published source checkpoint: **`ce16d284b9968a9b6e970197cd1f5e8307c35937`**,
commit `docs: establish Audit Council Dev control room, backlog and owner governance`.
Push used `git push --recurse-submodules=no -u origin master refs/tags/v1.0.3-baseline`.
Remote refs read back exactly: master → that checkpoint; baseline tag →
`1a9023714da3a223c009668569d4bfd0ece5dd22`. No other branch/tag existed to publish.

Post-push GitHub branch API reports **protected: true**. The effective branch-rule
API returns both `deletion` and `non_fast_forward` from ruleset `22343195`.
Collaborator, PR, disabled-feature and Actions permissions were read back again.

This follow-up record necessarily lives in a descendant documentation commit;
resolve the final publication tip from `refs/heads/master` or the operator handoff.
The final tip is rechecked before its normal push. No force push, history rewrite,
secret removal/rewrite, collaborator invitation, runtime change or installation occurred.

Git status after the source push: no parent tracked/staged changes; only the two
pre-existing dirty gitlinks (`? smoke-fixture`, `? smoke-fixture-103`) reflecting
their local untracked output. They were preserved and not published recursively.
Repository readiness does not resolve AUCDEV-010's runtime qualification evidence gap.

Current GitHub capability evidence: GraphQL schema exposes
`hasPullRequestsEnabled` and `pullRequestCreationPolicy` with `COLLABORATORS_ONLY`.
Official [pull-request settings documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/disabling-pull-requests)
describes collaborator-only and disabled options. The readbacks above establish
the actual policy, beyond the mutation command's success response.
