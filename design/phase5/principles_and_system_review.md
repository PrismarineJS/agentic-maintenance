# Principles and whole-system architectural review

Date: 2026-10-11. Source: rom1504's six principles and approval in this conversation;
[MATTER](https://rom1504.github.io/matter.png); the existing PrismarineJS review skills.
Status: implemented; see the [implementation and pilot report](../../implementation/phase5/principles_and_system_review.md).
This design was written before the principles and skill changes.

## Problem and intended behavior

Individually reasonable PRs can accumulate into a poorly structured system.
Existing review skills identify many local ownership and integration problems,
but begin with a proposed diff. Maintenance also needs an explicit architectural
direction and assessments of existing capabilities across package boundaries.

Create a permanent, maintainer-authored foundation in `PRINCIPLES.md`, separate
from dated project phases. Preserve the six principles: shared Minecraft data,
independently reusable modules, computation separated from state, all-version
support as a forcing function, library capabilities for diverse applications,
and cross-language standards. Explain their practical consequences and tensions.
Distinguish intended architecture from current compliance; computation/state
separation is explicitly an incompletely realized direction.

Add `skills/prismarine-system-review/SKILL.md` to examine an existing capability,
reuse relevant domain skills, and propose a coherent target with incremental
migration. Link the common PR review and architecture skills to the principles
and relevant dated assessments. The new workflow must not turn every PR review
into an ecosystem audit or make an agent's proposed target a maintainer decision.

## Deliverables and first application

- Top-level principles, linked prominently from README; stable principle anchors.
- One focused system-review skill with an output contract, evidence requirements,
  treatment of exceptions, and routing to the existing domain skills.
- Integration into PR review: assess direction against the principles and any
  relevant accepted design, distinguish introduced debt from pre-existing debt.
- A first assessment of **world block state and queries**: trace Mineflayer,
  prismarine-world and prismarine-chunk; include registry/rendering consumers
  only where inspected evidence makes them relevant. Start from existing code,
  not a pending PR. Read the maintainer's world-state plan and related discussion.
- Record the target proposal under `design/phase5/`; put the investigation,
  validation, limits and resulting follow-ups under `implementation/phase5/`.

The first assessment is a proposal, not authorization to change runtime code,
create issues, post PR reviews or adopt a new public API. Existing functionality
and local constraints must inform the target. Avoid package extraction without
an independent useful contract. Do not require every feature on versions where
Minecraft itself lacks that feature.

## Validation and iteration

Validate new/updated skill frontmatter with the skill-creator validator, check
local links, and apply the system skill to pinned source revisions. The pilot
must yield a traceable ownership map, concrete architectural costs, a target
proposal, bounded steps and validation criteria. Look for conforming behavior
as well as gaps. Record what was actually exercised; reading code cannot prove
runtime compatibility. Check the PR-review instructions on a bounded-change
scenario to ensure existing architectural debt does not automatically block it.

Improve the workflow if its first use exposes missing guidance. Do not introduce
wording-matching tests for prose. Run the repository's existing required checks
and publish through a maintenance PR. Keep temporary source fetches small and
remove them after recording useful evidence; do not install dependency trees.
