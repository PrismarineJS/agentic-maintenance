# agentic-maintenance

Planning and tracking for **agent-assisted maintenance work** across the
[PrismarineJS](https://github.com/PrismarineJS) ecosystem (mineflayer,
prismarine-* libraries, node-minecraft-protocol, and friends).

This repo holds the *thinking* behind maintenance work — analysis, plans, and
implementation records — as plain Markdown so it can be reviewed, versioned, and
picked up by humans or agents.

## Structure

Work is organized into **phases**. Each phase has a planning side and an
execution side:

```
design/
  phase1/        ← analysis & plans: what's the current state, what should we do
  phase2/
  ...
implementation/
  phase1/        ← execution records: what we actually did, decisions, outcomes
  phase2/
  ...
skills/         ← reusable review instructions, one SKILL.md per skill
policies/       ← shared repository settings
scripts/        ← read-only policy audits and CI gate generation
tests/          ← offline checks for maintenance tooling
```

- **`design/phaseN/`** — Investigation and planning documents. Status reports,
  triage, proposals, and the rationale for what to work on. Written *before*
  the work.
- **`implementation/phaseN/`** — Records of the work itself: what changed, links
  to the PRs/commits that resulted, decisions made along the way, and follow-ups.
  Written *during/after* the work.
- **`skills/`** — Reusable review skills. Start with
  [prismarine-review](skills/prismarine-review/SKILL.md), then select the relevant
  protocol/data, lifecycle/actions, items/inventory, geometry/movement,
  world/rendering, or architecture/public API skill. Code quality and regression
  checks are included in the domain where they matter. Use
  [PR prioritization](skills/prismarine-pr-prioritization/SKILL.md) to select the
  most important work or the next ready merge batch. These files
  can be read directly; this repository does not install them globally.

A `design/phaseN/` document typically motivates one or more
`implementation/phaseN/` documents in the same phase.

## Phases

| Phase | Focus | Design | Implementation |
|-------|-------|--------|----------------|
| 1 | mineflayer PR backlog triage | [design/phase1](design/phase1) | [implementation/phase1](implementation/phase1) |
| 2 | U9G PR classification and inline reviews | [design/phase2](design/phase2) | [implementation/phase2](implementation/phase2) |
| 3 | Historical review survey, skills, evaluation, and U9G re-review | [design/phase3](design/phase3/survey_for_review_skills.md) | [implementation/phase3](implementation/phase3/report.md) |
| 4 | Default-branch policy and repository settings | [Policy design](design/phase4/default_branch_policy.md) | [Rollout and remaining prerequisites](implementation/phase4/default_branch_policy_rollout.md) |

The current domain-specific skills are described in the
[revision design](design/phase3/domain_specific_review_skills.md) and
[implementation report](implementation/phase3/domain_specific_review_skills.md).
The original survey/evaluation report records the previous five-skill set.

The [September 21 standards update](implementation/phase3/extremeheat_review_standards.md)
strengthens maintainability review, upstream data consistency and packet-test
selection using extremeheat's review decisions.

## Default-branch policy

[The policy](policies/default_branch.json) separates required CI from the review
exception: repository admins may bypass approval **through a PR only**, while
CI, current-base validation, force-push and deletion protections have no bypass.
See the [design](design/phase4/default_branch_policy.md) and
[rollout report](implementation/phase4/default_branch_policy_rollout.md) for
actual coverage and outstanding CI prerequisites. Repositories with only the
PR rule enabled are reported as partial; their new CI rule remains disabled.

The audit uses Python 3's standard library and an authenticated `gh`. It only
issues GET requests and has no apply mode. It reports drift, not proof that a
repository's tests are ready for enforcement. A read error gives a nonzero exit;
setting differences are recorded in the report. Reports redact private repos.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/audit_branch_policy.py --live --output /tmp/pjs-policy
python3 scripts/audit_branch_policy.py --snapshot implementation/phase4/default_branch_policy.json --output /tmp/pjs-policy-replay
```

Each audit writes a Markdown diff and replayable JSON evidence at the output
prefix. No dependencies or global skills need installing in this repository.
`scripts/required_ci.py` renders the tested final gate used by rollout PRs;
it does not modify repositories or contact GitHub.

## Conventions

- One topic per Markdown file; use descriptive `snake_case` names
  (e.g. `mineflayer_pr_status.md`).
- Lead each document with a short header noting its **date** and **source** of
  data, since status snapshots go stale.
- Keep documents self-contained and link out to the relevant GitHub PRs/issues.
