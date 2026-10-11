# World block state and reusable queries

Date: 2026-10-11. Author: Astra agent. Status: **proposed architecture assessment**,
not an accepted API design or permission to change runtime code.
Principles: [P1–P6](../../PRINCIPLES.md). Adoption design:
[principles and system review](principles_and_system_review.md).

## Scope and evidence

Assess existing block storage, query computation and Mineflayer adaptation.
This is a default-branch source assessment at these revisions:

| Repository | Revision | Source package version / relevant dependency |
|---|---|---|
| Mineflayer | `7b4bb8d2b56be9cdb832474af873acd37e609746` | Declares world `^3.6.0`, chunk `^1.41.0`, registry `^1.10.0` |
| prismarine-world | `f375ea9c5bc4e04c4f3e35cb1499603a0b8bbe06` | Source package 3.7.0; chunk is a dev dependency `^1.31.0` |
| prismarine-chunk | `a08dc2c689005c9630335c289d5c34175916f21a` | Inspect loader plus Java common/1.18 implementation and shared tests |

These are independently inspected source tips, **not an installed dependency
combination**. No downstream compatibility or released-version claim follows
from the source package version or a semver range. Viewer/worker integration,
entity movement, live inventories and comprehensive Bedrock behavior are outside
this first slice. Potential consumers below are explicitly distinguished from
ones inspected.

## Maintainer direction and current proposal status

[Mineflayer #334](https://github.com/PrismarineJS/mineflayer/issues/334) establishes
the shared-world direction. The
[2022 plan](https://github.com/PrismarineJS/mineflayer/issues/334#issuecomment-1030719439)
places model state below Mineflayer and describes Mineflayer as a packet/action
synchronization layer. Later
[inventory proposals](https://github.com/PrismarineJS/mineflayer/issues/334#issuecomment-3263942975)
change some proposed storage details; do not treat every historical snippet as
one simultaneously accepted schema.

[World #164](https://github.com/PrismarineJS/prismarine-world/pull/164) was open and
unmerged at head `75239a6af1f8dcb17047d371aff72a4a9f11b018` when inspected.
Its raw accessors and transient inventory observations are not in the assessed
world default branch. Its description reports new validation, but this assessment
does not revalidate that PR or repeat an earlier review verdict about an older
head. Observation provenance and authoritative state remain distinct questions.

## Current ownership map

| Responsibility | Observed owner and boundary |
|---|---|
| Block interpretation / version specialization | Mineflayer passes its registry to Block and Chunk factories. Chunk's loader selects Java/Bedrock implementations; multiple releases share implementations. |
| Column and block-entity storage | Chunk columns own their storage. The inspected Java common column owns `blockEntities`; Java 1.18 exposes the block entity through the block model. |
| Loaded columns, provider loading and persistence scheduling | `World` owns `columns`, saving/unload queues and provider calls. `WorldSync` delegates loaded-column access to that same world; it is not a second column store. |
| Traversal and ray intersection | Public world iterators supply reusable computation. Sync/async worlds orchestrate block reads and expose raycast methods. |
| Network adaptation and application queries | Mineflayer's blocks plugin handles packets, updates columns/world, forwards events, decorates blocks with paintings, and implements `findBlocks`/`findBlock`. |

Evidence: [blocks plugin][blocks], [World][world], [WorldSync][sync],
[chunk loader][chunk-loader], [Java column][column]. The world factory currently
returns `World` without using its version argument; registry-dependent block
interpretation is supplied by the columns. Passing `bot.registry` to this factory
alone is not evidence that World owns or synchronizes the registry.

## Findings against the principles

### W1 — A reusable query is still coupled to the application

**Architectural cost; P2, P3, P5.** `findBlocks` in the [blocks plugin][blocks]
combines traversal/matching with `bot.entity.position`, `bot.game.minY/height`,
`bot.blockAt`, column sections and palette inspection. A standalone consumer of
prismarine-world cannot use that implementation through the world API. Changing
section/query assumptions requires reasoning inside the network application's
plugin, even though the calculation itself need not communicate with a server.

Propose a world-query operation accepting explicit origin, bounds and a read
interface, with Mineflayer retaining its convenience defaults and extra-info
adapter. Start within prismarine-world; a separate package needs evidence of an
independent contract. Mineflayer is the inspected consumer; servers and offline
analysis are plausible beneficiaries, not verified adopters in this assessment.

### W2 — Similar query implementations have different observable contracts

**Contract/documentation cost; P3, P5, P6.** Compare `raycast` in [World][world]
and [WorldSync][sync]. Async raycast applies a block matcher and then intersects
shapes. Sync raycast with a matcher passes the iterator and returns on the
matcher's decision. Mineflayer's `canSeeBlock` uses that iterator-aware callback.
The [API documentation][api] describes a block matcher and says the sync world
exposes the same methods; it does not make this callback difference explicit.

The source establishes a difference, not that either behavior is incorrect.
First document and characterize both contracts, including missing-column/loading
semantics. Extract common traversal only if compatibility can be preserved.
Silently making both methods identical could break an existing consumer.

### W3 — Independent tests exist, but world-level coverage is narrower than the abstraction

**Validation gap; P2, P4.** World has real storage/provider tests using 1.8,
raycast/world tests using 1.16.4, and version-independent iterator/intersection
tests. Those are valuable independent tests, not fake bot tests. The inspected
world test files do not establish the same query/update contracts over modern
negative-height columns and the broader chunk implementation matrix.

[Chunk's shared tests][chunk-tests] use `allVersions` and explicitly skip two
legacy Bedrock cases with a TODO; that is a visible gap, not full all-version
proof. Mineflayer's internal tests iterate its own `testedVersions`. Extend
world's existing tests at relevant representation boundaries and retain the
consumer tests. Do not create a release-named duplicate suite or mistake Node's
CI matrix for a Minecraft-version matrix.

### Existing strengths and limits

P1: the inspected factories reuse registry-backed block interpretation; no new
Minecraft-data defect is established. A map selecting source implementations is
package routing, not automatically Minecraft data to move elsewhere.

P2/P3/P5: shared column storage and independent iterators already provide useful
separation. Preserve them. Mutable columns and the sync facade are not evidence
that a second state framework is needed.

P6: coordinate and callback contracts can become useful portable specifications.
This pilot does not audit all serialization or establish cross-language adoption.

## Coherent target and incremental path

Keep **chunk storage → world ownership/access → query computation → application
adaptation** explicit. Queries use explicit inputs and do not own networking,
saving timers or a second authoritative column map. World access decides whether
missing data stays unknown or may be loaded. Mineflayer translates packets/actions
and supplies application defaults. Preserve model state independently of any
single client; a client's partial observations must not silently become complete
server truth.

1. **Characterize existing contracts.** Extend existing world tests/docs for
   sync versus async matching, loaded versus missing columns, event behavior,
   negative coordinates and modern height bounds. Specify expected differences.
2. **Extract one capability: block search.** Design the smallest read contract
   around current search needs; preserve ordering, radius, count, extra-info
   semantics and unloaded-column behavior. Keep section/palette optimization
   behind an appropriate column/query boundary. Compare behavior and cost before
   removing the old implementation; independent tests must use actual models.
3. **Make Mineflayer delegate.** Retain current bot-facing defaults/API and test
   the adapter with the established protocol harness. Land/release the reusable
   capability before depending on it; verify the candidate dependency explicitly.
4. **Publish portable behavioral fixtures.** Describe query inputs/results,
   floor semantics at negative coordinates, missing data and callback policies.
   Keep JavaScript implementation fixtures separate from portable contract cases.

These are proposed steps, not runtime changes made by this maintenance task.
Broader entity/painting/inventory ownership remains a separate roadmap decision.
Revisit that scope when those capabilities are migrated or a concrete shared-world
consumer needs them; no maintainer-approved exception is inferred here.

## PR implications

- Advance this direction with independent world-query behavior, meaningful shared
  model tests, explicit state ownership and compatible Mineflayer delegation.
- Question new copies of search logic or another authoritative column map. State
  the repeated responsibility and consumer cost, rather than demanding extraction
  merely because a helper is new.
- A bounded block decoding, ray intersection or version-support fix can land
  before the search migration if its own contract and tests are sound. This
  proposed assessment does not add a requirement to finish the whole roadmap.
- Do not remove `bot.blockAt`, unify matcher behavior or treat world #164 as
  accepted architecture on the authority of this agent-authored document.

[blocks]: https://github.com/PrismarineJS/mineflayer/blob/7b4bb8d2b56be9cdb832474af873acd37e609746/lib/plugins/blocks.js
[world]: https://github.com/PrismarineJS/prismarine-world/blob/f375ea9c5bc4e04c4f3e35cb1499603a0b8bbe06/src/world.js
[sync]: https://github.com/PrismarineJS/prismarine-world/blob/f375ea9c5bc4e04c4f3e35cb1499603a0b8bbe06/src/worldsync.js
[api]: https://github.com/PrismarineJS/prismarine-world/blob/f375ea9c5bc4e04c4f3e35cb1499603a0b8bbe06/docs/API.md
[chunk-loader]: https://github.com/PrismarineJS/prismarine-chunk/blob/a08dc2c689005c9630335c289d5c34175916f21a/src/index.js
[column]: https://github.com/PrismarineJS/prismarine-chunk/blob/a08dc2c689005c9630335c289d5c34175916f21a/src/pc/1.18/ChunkColumn.js
[chunk-tests]: https://github.com/PrismarineJS/prismarine-chunk/blob/a08dc2c689005c9630335c289d5c34175916f21a/test/ChunkColumn.test.js
