# Default-branch policy preparation

Date: 2026-10-06. Source: GET-only GitHub audit and local validation.
Status: prepared locally; no GitHub settings, workflows, branches, or PRs changed.

This is the historical preparation snapshot, before rollout approval. See the
[rollout report](default_branch_policy_rollout.md) for subsequent changes.

The [design](../../design/phase4/default_branch_policy.md) and
[policy JSON](../../policies/default_branch.json) preserve the requested admin
review bypass while separating it from mandatory CI. Two rulesets per included
repository target the actual default branch. The policy does not require a paid
organization plan.

The [per-repository diff](default_branch_policy.md) and
[replayable evidence](default_branch_policy.json) cover 98 repositories: 94 public
and unarchived, three archived exclusions, and one redacted private exclusion.
The target configuration needs 188 new rulesets and reconciliation of 30 classic
protections. Sixty-four default branches have no classic protection; 29 require
a PR and only ten have named required checks. No included API read failed.

For non-admins, 65 additional repositories would require a PR with one approval.
Admins retain the ability to merge an unapproved PR, but lose blanket bypass of
CI. This is a proposal for activation after CI and automation prerequisites, not
a claim that any of the 94 repositories is ready for immediate enforcement.

Added a standalone Python/`gh` audit script with no apply mode. It only sends GET
requests, preserves errors as unknown settings, handles paginated lists, checks
existing managed ruleset payloads, reports inherited/name collisions for manual
reconciliation, and redacts private repository details from public artifacts.
It can replay the stored JSON without network access. It does not inspect every
workflow's test semantics or execute live GitHub enforcement checks.

Validation completed:

- `python3 -m unittest discover -s tests -v`: nine passing offline tests, covering
  policy permission boundaries, GET-only pagination, bypass drift, exclusions,
  redaction, permission failures, missing rule details, and timeouts.
- Live audit: all 94 included repositories read successfully; no mutation calls.
- Offline replay: the live summary is reproduced from the stored evidence.
- `git diff --check`: passed.

Repository-specific `ci` workflow changes, automation migration, disabled-ruleset
staging, activation, classic-rule reconciliation, and enforcement verification
remain future rollout work. No commit or push was made. The three preexisting
untracked phase-2 design drafts were left untouched.
