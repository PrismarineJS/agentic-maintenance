# Default-branch policy for public PrismarineJS repositories

Date: 2026-10-06. Sources: rom1504's instructions in this session, the read-only
GitHub settings audit, and the GitHub documentation linked below.
Status: rollout authorized by rom1504 on 2026-10-06 ("Ok make the change").
The preparation snapshot below is retained; rollout receipts record actual changes.

## Intended behavior

Every change to a public, unarchived PrismarineJS repository's default branch
goes through a PR and passes the repository's real validation. Administrators
can merge a PR without another person's approval. They cannot use that review
bypass to skip CI or push directly. Stay on GitHub Free.

Use two repository-level rulesets from
[the policy](../../policies/default_branch.json), targeting `~DEFAULT_BRANCH`.
This covers `master`, `main`, and the website's `src` without renaming branches.
The policy includes forks owned by the organization. Archived repositories stay
read-only. Private repositories are reported as excluded because this plan does
not provide their enforced branch protections; do not make them public.

| Ruleset | Rules | Bypass |
|---|---|---|
| `pjs-ci-and-history` | Require the `ci` check from GitHub Actions, require the branch to be up to date, prevent force pushes and deletion | None |
| `pjs-pr-and-review` | Require a PR and normally one approval | Repository admins, only through a PR |

Repository admin is GitHub's built-in `RepositoryRole` ID 5. GitHub Actions is
integration ID 15368, also observed on live Mineflayer check runs in this audit.
Organization owners have repository administrator access. Do not add write or
maintain roles, bots, deploy keys, or an `always` bypass to either ruleset.

The review settings otherwise remain minimal: no new code-owner requirement,
stale-approval dismissal, last-push approval, or conversation-resolution rule.
Do not change allowed merge methods. One approval for ordinary mergers on repos
that currently require none is an explicit proposed change; admins retain the
requested exception. Bypass is ruleset-wide: the review bypass may also override
blocking review decisions, not just the absence of an approval. It is not a
permission to bypass the separate CI ruleset.

This protects ordinary push/merge operations. Administrators still possess
permission to edit or remove repository rules; this is not an immutable policy
against organization owners.

GitHub expands omitted PR-rule parameters when reading the rule back. The
2026-10-06 rollout observed empty `required_reviewers`, disabled
`dismissal_restriction`, all three `allowed_merge_methods`, and
`require_extra_approval_for_unattributed_changes: true`. These server defaults
are preserved, not explicitly changed by the policy payload. Repository-level
merge-method settings still apply. The audit normalizes these observed defaults
on both sides, but flags different values or new unknown parameters for review.

## The `ci` check must represent real validation

Retain each repository's established test harness and version/edition matrix.
Do not replace Mineflayer's NMP/server tests or the data schema/consumer checks
with a placeholder. Code repositories need actual tests. Documentation and
design repositories need useful Markdown, link, JSON/schema, or other applicable
validation, not an empty `echo success` job. Agentic-maintenance must validate its
policy and audit tool as part of its own eventual CI.

Use the unique final check name `ci`, independent of Node and Minecraft version
numbers. A small repository may name its real test job `ci`. A matrix repository
should add an aggregate job with `if: ${{ always() }}` and explicit `needs` for
all mandatory jobs, including matrix preparation. The aggregate must fail on
failed, cancelled, missing, or unexpectedly skipped dependencies. Validate that
the expected version matrix is nonempty and complete. Mandatory tests must not
use `continue-on-error` or swallowed exit codes. Report-only jobs may stay outside
the gate, with their exclusion documented.

GitHub accepts skipped/neutral required check results. Therefore never put a
conditional skip on the gate itself. Avoid PR path/branch filters that prevent
the required workflow from starting. Inspect fork-PR permissions and workflow
approval behavior. Do not execute untrusted PR code with a privileged
`pull_request_target` token just to make required checks run.

Do not merely rename a check without inspecting its assertion and test-discovery
behavior. Binding to GitHub Actions establishes the check's source, not that its
workflow is immutable. Before activation, demonstrate a passing case and cases
where a required test fails or is skipped; the gate must distinguish them.

## Rollout and exact setting changes

The JSON contains the desired *active* configuration. The subsequent user approval
authorizes rollout after the prerequisites below. The audit script performs GET requests only and has no apply mode.
The generated report distinguishes setting drift from rollout readiness; it
does not certify a repository's tests or authorize activation.

1. Refresh the settings and workflow inventory. Save the exact existing rules
   for rollback before any later authorized mutation. Treat 403/errors as
   unknown, never as evidence that a branch is unprotected.
2. Prepare repository-specific CI PRs. Preserve the existing mandatory jobs and
   add a final `ci` gate. Require a passing run of the repository's actual suite
   before activation. Test the shared gate against failed, cancelled, skipped,
   missing and empty-matrix inputs, and verify failure/skip behavior on a
   temporary pilot PR. A green lint-only or install-only workflow does not
   establish behavioral test coverage for a code repository.
3. Inspect release, data-update, formatting, deployment, and synchronization
   automation for direct default-branch pushes. Change those paths to PRs where
   necessary. Tag publishing and other unprotected branches are outside scope.
   No blanket automation bypass is proposed.
4. Create the two rulesets disabled and inspect their payloads and target branch.
   Enable the PR/review rule after checking automation. Enable the separate CI
   rule only when its prerequisite passes. Record this intermediate state as
   **partial**, not compliant: PRs are required, but CI is not yet enforced by
   the new policy. This allows the no-direct-push requirement to take effect
   without requiring a nonexistent or permanently failing check. Keep existing
   protection until its replacement is active, so there is no unprotected interval.
5. Reconcile overlapping classic protection. Determine the actual rule pattern
   and other matching branches before changing it. Preserve any unrelated
   protection or stricter intentional rule. Do not delete a wildcard rule just
   because its default-branch settings overlap. In this snapshot, 30 default
   branches have classic protection to reconcile; that is not a list of 30
   preauthorized DELETE requests. Obsolete required contexts must be retired so
   they cannot continue blocking otherwise passing PRs.
6. Verify ordinary merges need approval, admins can merge a passing unapproved
   PR, neither can merge failing CI, and direct/force pushes are rejected. Use
   controlled rollout checks; do not rewrite a real default branch to test force
   push denial. CI/source evidence alone does not test GitHub's enforcement.
7. Run the read-only audit periodically and when adding repositories. A scheduled
   audit is a later change, not created by this preparation. Rulesets on Free
   must be installed per repository; newly created repos are not automatically
   covered until provisioned. Leave broad organization rules and billing alone.

The rollout record is in
[implementation/phase4/default_branch_policy_rollout.md](../../implementation/phase4/default_branch_policy_rollout.md).
It distinguishes observed CI results and settings readback from live permission
tests. No default branch is rewritten to probe enforcement. A temporary negative
control PR is closed without merging; normal-user behavior is not claimed to
have been tested using the administrator's credentials.

## Preparation and validation

Store the policy under `policies/`, the GET-only audit under `scripts/`, and its
offline regression tests under `tests/`. Record the fresh per-repository diff
under `implementation/phase4/`. Tests should catch incorrect unknown/unprotected
classification, private/archive exclusions, bypass drift, and loss of the
separation between review and CI. Do not test by mutating live settings.

## References

- [Public repository rulesets on Free and PR-only bypass](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- [Rulesets layer with each other and classic protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [REST ruleset payloads](https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset)
- [Built-in repository role IDs](https://registry.terraform.io/providers/integrations/github/latest/docs/resources/repository_ruleset)
- [Required checks, skipped results, and strict mode](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
