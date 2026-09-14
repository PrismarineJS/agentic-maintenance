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
```

- **`design/phaseN/`** — Investigation and planning documents. Status reports,
  triage, proposals, and the rationale for what to work on. Written *before*
  the work.
- **`implementation/phaseN/`** — Records of the work itself: what changed, links
  to the PRs/commits that resulted, decisions made along the way, and follow-ups.
  Written *during/after* the work.
- **`skills/`** — Reusable review skills. Start with
  [prismarine-review](skills/prismarine-review/SKILL.md), then select the relevant
  code quality, architecture, protocol/data, or behavior/test skill. These files
  can be read directly; this repository does not install them globally.

A `design/phaseN/` document typically motivates one or more
`implementation/phaseN/` documents in the same phase.

## Phases

| Phase | Focus | Design | Implementation |
|-------|-------|--------|----------------|
| 1 | mineflayer PR backlog triage | [design/phase1](design/phase1) | [implementation/phase1](implementation/phase1) |
| 2 | U9G PR classification and inline reviews | [design/phase2](design/phase2) | [implementation/phase2](implementation/phase2) |
| 3 | Historical review survey, skills, evaluation, and U9G re-review | [design/phase3](design/phase3/survey_for_review_skills.md) | [implementation/phase3](implementation/phase3/report.md) |

## Conventions

- One topic per Markdown file; use descriptive `snake_case` names
  (e.g. `mineflayer_pr_status.md`).
- Lead each document with a short header noting its **date** and **source** of
  data, since status snapshots go stale.
- Keep documents self-contained and link out to the relevant GitHub PRs/issues.
