# PR prioritization skill and first application

Date: 2026-10-03. Source: rom1504's explicit ranking preference, the existing reviewed queue, fresh GitHub API reads, current PR discussions/diffs and isolated integration checks.

## Changes

Added [prismarine-pr-prioritization](../../skills/prismarine-pr-prioritization/SKILL.md), with routing from the common review skill and README. The [design](../../design/phase3/pr_prioritization.md) preceded implementation.

The skill puts new version support, new Minecraft functionality, broad capabilities and abstraction quality in one leading group. It introduces neither numerical weights nor a fixed ordering inside that group. Correctness and maintenance can rise when they enable those outcomes or address exceptional concrete urgency. Readiness remains a separate review decision, including repository testing standards and outstanding maintainer requests.

## Scope and practical evaluation

Refreshed all 137 entries previously marked ready: 127 remain open, and the previous ten recommendations are confirmed merged. None of those 137 heads changed. This is selection from the reviewed queue, not a new census or full re-review of every pending ecosystem PR. Read complete current discussions, review comments and changed-file inventories for 17 higher-priority candidates; checked seven related producer/wrapper/consumer PRs. The final ten received another head/state/discussion refresh before recommendation.

Application checks:

- Version-support work and shared APIs outrank routine development dependency upgrades despite the upgrades' green checks.
- `prismarine-chunk` #331 and #333 are excluded: current merge conflicts make the previous ready classification stale. Their overlapping version dispatch cannot count as two independent advances.
- Select physics #138 for its gravity **and climbing** entries. #145 overlaps gravity and additionally covers 26.3; preserve its unique entry when reconciling later rather than merging both unchanged in one batch.
- A local sequence of data #1308 followed by #1331 conflicts in `data/dataPaths.json`. Recommend the broader tags foundation this round; crafter metadata remains useful after reconciliation. This is a batch interaction, not a claim that #1331 alone is defective.
- Shared world, block and transport APIs can merge independently where compatible fallbacks or additive contracts exist. Their pending consumers are not implicitly approved. In particular, Mineflayer #4098 currently conflicts, and node-minecraft-data #457 retains the previously reported testing concern.
- Missing-content assets rank above routine maintenance because they make additional Minecraft blocks renderable. Scanner success is not presented as a renderer test.

Both changed SKILL.md files pass `quick_validate.py`; relative links resolve and `git diff --check` passes. These structural checks do not establish ranking quality; the concrete selections, exclusions and dependency distinctions above are the practical evaluation.

## Recommended batch

All entries below were open, nondraft and at their previously reviewed heads on final refresh. GitHub reports them mergeable. A `REVIEW_REQUIRED` branch-protection gate is left to the maintainer and does not imply an outstanding code finding. The generator targets `bump`; the other nine target `master`.

| Rank | PR / reviewed head | Why it leads | Landing or release scope |
|---|---|---|---|
| 1 | [minecraft-data-generator #78](https://github.com/PrismarineJS/minecraft-data-generator/pull/78) / `d3058be` | Repairs the 26.2 data generator build and entity classification. | Targets the bump integration branch; native 26.2 CI passed. |
| 2 | [prismarine-physics #138](https://github.com/PrismarineJS/prismarine-physics/pull/138) / `e5597f7` | Enables 26.2 liquid gravity and climbing in the shared physics model. | Merge this before reconciling overlapping #145, which also adds 26.3 gravity. |
| 3 | [node-nethernet #32](https://github.com/PrismarineJS/node-nethernet/pull/32) / `77a0b38` | Adds HTTP discovery and authenticated signalling at the transport owner. | Coordinate bedrock-protocol #831 and release integration; this is not an automatic release request. |
| 4 | [prismarine-world #164](https://github.com/PrismarineJS/prismarine-world/pull/164) / `42eea12` | Adds shared block-entity access and memory-only observed inventories to world APIs. | Mineflayer #4098 is a separate consumer and currently conflicts; model API can land independently. |
| 5 | [node-protodef #169](https://github.com/ProtoDef-io/node-protodef/pull/169) / `3c55480` | Lets compiled custom writers reuse size calculations for length-prefixed containers. | 507 tests pass on a local merge with current master; no GitHub CI reported. |
| 6 | [prismarine-loottable #15](https://github.com/PrismarineJS/prismarine-loottable/pull/15) / `839d8b0` | Reads modern loot formats and unblocks generation of newer loot data. | Existing approximate-drop API scope; does not implement a complete loot evaluator. |
| 7 | [minecraft-data #1308](https://github.com/PrismarineJS/minecraft-data/pull/1308) / `2eb69db` | Introduces reproducible namespaced vanilla tags across 46 release mappings. | Node wrapper #457 remains a separate prerequisite for automatic consumer exposure; reconcile shared schema work #1194. |
| 8 | [prismarine-block #127](https://github.com/PrismarineJS/prismarine-block/pull/127) / `528850d` | Uses shared block tags for dig-time tool selection instead of a single material classification. | Data #1308 plus wrapper #457 activate it; existing-data fallback allows independent merge. |
| 9 | [prismarine-block #125](https://github.com/PrismarineJS/prismarine-block/pull/125) / `1b839c7` | Adds selection geometry separately from physical collision shapes. | Selection data #1296 plus wrapper #468 activate it; collision fallback remains available. |
| 10 | [minecraft-assets #51](https://github.com/PrismarineJS/minecraft-assets/pull/51) / `6aef050` | Makes 45 missing 1.21.8 blocks available through asset indexes. | Existing model/texture files are reused; prior semantic checks, scanner-only CI. |

## Validation and limits

Fresh local merges account for GitHub test-merge refs that still pointed at earlier target commits. Physics #138 merged onto `a4fbb863c227340198df5b830cea49dcf1538ccd`; `npm test` passed lint and all 44 tests. This does not claim a fresh live 26.2 server comparison. ProtoDef #169 merged onto `09381130091b6d49cdfde2fe1ef1594f87cb69dd`; after initializing its schema submodule, `npm test` passed lint and all 507 tests. Earlier exact-head custom-writer probes remain the focused evidence for the new sizing API.

Data #1308 merged cleanly onto `095709f3ad62b043069141dc127fc80ef6cd10fa`. Fresh dependencies include the newly required ajv-keywords; initial cached-dependency and lint-cache setup errors were environmental and resolved before the full suite. The candidate passed lint and 3,048 behavioral/schema cases with 90 pending; its command exited nonzero solely because the global 40-second suite guard measured 45.863 seconds. Current master with the same dependencies passed lint and 3,021 cases with the same 90 pending, and also failed only that guard at 44.734 seconds. This is not an all-green local command, but the timing failure reproduces without the PR and all 27 added schema cases pass.

For unchanged remaining packages, retained the earlier exact-head validation rather than claiming another full suite execution. Generator CI includes its native 26.2 build. Nethernet CI passes on three platforms; this pass did not repeat BDS, authenticated online or NAT interoperability. World validation remains the earlier 11-case focused file plus lint, with current-base iterator changes separate from this API. Block #127 retains its 8,190-case earlier suite and candidate-tag checks; #125 retains seven getter cases and the actual data/wrapper/registry check across 553,340 states and 28 versions. Loot retains seven production parser tests plus arithmetic controls. Assets retain semantic registry/index/model-reference comparisons; the original client extraction and full rendering pass were not independently repeated. Assets has scanner-only GitHub checks; ProtoDef has no GitHub CI rollup.

Both block PRs affect distinct APIs in the same source file; refresh the second after landing the first, as with any merge batch. Tags/schema #1194 and selection-shape data/wrapper releases remain coordination tasks, not evidence that the downstream features are already available through npm.

Existing review evidence:

- [minecraft-data-generator #78](https://github.com/PrismarineJS/minecraft-data-generator/pull/78#pullrequestreview-5401745067)
- [prismarine-physics #138](https://github.com/PrismarineJS/prismarine-physics/pull/138#pullrequestreview-5401558983)
- [node-nethernet #32](https://github.com/PrismarineJS/node-nethernet/pull/32#pullrequestreview-5401665533)
- [prismarine-world #164](https://github.com/PrismarineJS/prismarine-world/pull/164#pullrequestreview-5401563169)
- [node-protodef #169](https://github.com/ProtoDef-io/node-protodef/pull/169#pullrequestreview-5401800564)
- [prismarine-loottable #15](https://github.com/PrismarineJS/prismarine-loottable/pull/15#pullrequestreview-5401542503)
- [minecraft-data #1308](https://github.com/PrismarineJS/minecraft-data/pull/1308#pullrequestreview-5401559499)
- [prismarine-block #127](https://github.com/PrismarineJS/prismarine-block/pull/127#pullrequestreview-5268267244)
- [prismarine-block #125](https://github.com/PrismarineJS/prismarine-block/pull/125#pullrequestreview-5268189779)
- [minecraft-assets #51](https://github.com/PrismarineJS/minecraft-assets/pull/51#pullrequestreview-5401569921)

No PR comments, approvals, merges or central issue-table edits were made in this task. Temporary checkouts and logs are under `/tmp/prismarine-pr-prioritization/`. Unrelated phase2 draft files are excluded from the commit.
