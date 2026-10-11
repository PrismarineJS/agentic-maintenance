# Principles and system-review implementation

Date: 2026-10-11. Author: Astra agent, on rom1504's behalf.
Source: approved [adoption design](../../design/phase5/principles_and_system_review.md),
maintainer principles in the conversation, and pinned GitHub source/discussion.

## What changed

Added [PRINCIPLES.md](../../PRINCIPLES.md) as the permanent architectural direction,
with stable P1–P6 anchors. It preserves the maintainer's six principles and marks
computation/state separation as an incompletely realized direction. Explanatory
text is attributed to Astra, not presented as historical maintainer quotation.
MATTER supplies motivation without importing its separate infrastructure agenda.

Added [prismarine-system-review](../../skills/prismarine-system-review/SKILL.md)
to assess an existing capability across package boundaries, recognize strengths
and concrete costs, and propose one target with a bounded migration. Updated the
common PR and architecture skills to use the principles and relevant assessments.
README links the foundation, workflow and first assessment; normal phase-based
design and implementation organization is preserved.

No runtime implementation, issue or PR review comment was changed by this task.
The pilot design remains an agent proposal even when this maintenance PR is merged.

## Pilot: world block state and queries

Applied the new system-review skill with the existing architecture and world/render
skills to [this assessment](../../design/phase5/world_block_state_and_queries.md).
Read 26 selected source, manifest, workflow and test files at the three revisions
recorded there. Read Mineflayer #334 and its later comments, and world #164's
current description/state and review history. World #164 was open/unmerged; its
latest implementation was not re-reviewed or treated as default-branch code.

The assessment retained three concrete observations:

- Block search remains coupled to Mineflayer's application state and column
  layout. A world query with explicit inputs is a useful bounded first migration.
- Sync/async raycast matcher semantics differ, with an inspected Mineflayer caller
  using the sync iterator-aware form. Characterize that contract before sharing
  more implementation; identical behavior is not automatically the correct target.
- World has meaningful independent model/provider and geometry tests, but the
  inspected world-level coverage is narrower than the chunk/version abstraction.
  Extend the existing harness instead of adding a fake bot or copied suites.

It rejected overbroad conclusions: the sync facade does not duplicate the column
store; mutable columns alone do not violate P3; implementation-selection maps
need not be moved into Minecraft-data; the world factory's registry argument is
not proof that World owns registry state; an open proposal is not deployed code.

## Skill trial and refinement

This was a **manual source-based trial by the author**, not an independent or
blind evaluation and not runtime verification. The trial exposed a missing
explicit check: similar-looking APIs can deliberately have different loading or
callback semantics. Added that check to system review before proposing extraction.

| Trial case | Result of applying the instructions |
|---|---|
| Assess existing world capability without an open diff | Produced an ownership map, evidence-backed costs, one target and ordered steps. |
| Consolidate sync/async raycasts because their loops look similar | Existing callback differences and `canSeeBlock` prevent an unconditional unification recommendation. |
| Review a bounded ray-intersection fix while search remains bot-coupled | Existing search debt does not itself block the fix; review its own contract and established geometry tests. |
| Treat all runtime facts as static Minecraft-data | Runtime registries/world state remain distinct from shared version facts. |
| Use old world #164 feedback as a verdict on its latest head | Record current unmerged status and inspection limit; do not repeat stale objections or assert readiness. |

The first case used actual pinned code. The bounded-change and data-placement
cases are decision walkthroughs, not fresh PR reviews. These results provide an
initial check of usefulness; future assessments should refine the instructions
when they reveal a concrete failure, without accumulating blanket rules.

## Validation and limits

- Skill-creator frontmatter validation for the new system skill and the two
  updated review skills.
- Local Markdown file-link checks across changed/new documents; explicit stable
  principle anchors checked separately.
- Existing 16 offline maintenance tests and `git diff --check`.
- Read world test discovery (`npm test` / Mocha), all four world test files,
  chunk's shared version list/column tests and Mineflayer's version-driven harness.
  **No Minecraft/runtime suites, browser tests, benchmarks or installed cross-repo
  integration were run.** No dependency trees were installed.

Immutable testing evidence:
[world storage tests](https://github.com/PrismarineJS/prismarine-world/blob/f375ea9c5bc4e04c4f3e35cb1499603a0b8bbe06/test/test.js),
[world raycast tests](https://github.com/PrismarineJS/prismarine-world/blob/f375ea9c5bc4e04c4f3e35cb1499603a0b8bbe06/test/raycast.test.js),
[geometry boundary tests](https://github.com/PrismarineJS/prismarine-world/blob/f375ea9c5bc4e04c4f3e35cb1499603a0b8bbe06/test/raycast-parallel.test.js),
[chunk versions](https://github.com/PrismarineJS/prismarine-chunk/blob/a08dc2c689005c9630335c289d5c34175916f21a/test/versions.js),
[Mineflayer internal harness](https://github.com/PrismarineJS/mineflayer/blob/7b4bb8d2b56be9cdb832474af873acd37e609746/test/internalTest.js).

## Follow-up

The proposed next engineering slice is to characterize the world-query contracts
and design reusable block search while preserving Mineflayer behavior. That work
requires its own scoped implementation decision. Entity/inventory ownership and
viewer synchronization need their own evidence before expanding this pilot.

Temporary source fetches are removed after publication; durable evidence is the
small assessment and immutable links, not duplicated repository snapshots. The
three unrelated phase2 drafts remain untouched.
