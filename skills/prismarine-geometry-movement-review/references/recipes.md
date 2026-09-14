# Geometry/movement recipes and evidence

These are adaptable checks against specific reviewed code, not tests promised in every release. The [2026-09-14 re-review records](../../../implementation/phase3/u9g_rereviews.json) contain exact heads, dependencies, observations and limits. Recent Astra findings are engineering examples, not independent manual maintainer policy. The [independent checks](../../../implementation/phase3/u9g_independent_checks.json) withdrew the #4089 numeric-hand serialization objection: released compiled ProtoDef accepts it. That withdrawal does not validate missing released feature flags or the entire 26.1 interaction path.

## Pick a partial block through the existing harness

Source: Mineflayer [generic_place.js at #4115 head](https://github.com/PrismarineJS/mineflayer/blob/27805567aa88bbc140c5b3d91766fe8a47fd105b/lib/plugins/generic_place.js), its [genericPlaceRaycastTest.js](https://github.com/PrismarineJS/mineflayer/blob/27805567aa88bbc140c5b3d91766fe8a47fd105b/test/genericPlaceRaycastTest.js), and [finding](https://github.com/PrismarineJS/mineflayer/pull/4115#discussion_r4003948084).

Extend that harness's `fakeBot`, `setBlock` and `crosshairHit` fixtures:

```js
const bot = fakeBot()
const pos = new Vec3(0, 63, 0)
setBlock(bot, pos, 'oak_slab') // Verify getProperties().type === 'bottom'.
bot.entity.position = new Vec3(0.5, 64, -3)
const block = bot.world.getBlock(pos)
const eye = bot.entity.position.offset(0, bot.entity.eyeHeight, 0)
const direction = pos.offset(0.5, 0.5, 0.5).minus(eye).normalize()
const visible = bot.world.raycast(eye, direction, 6)
assert(visible.position.equals(pos))
assert.equal(visible.face, 1)
await bot._genericPlace(block, new Vec3(0, 1, 0), {
  forceLook: true, strictFace: true
})
assertPacketMatchesCrosshair(bot)
```

At the archived head the direct ray hits the slab top, but strict placement throws; non-strict fallback writes a cursor whose crosshair misses. Keep a full-cube success control, then adapt for stairs and an actual occluder only if relevant. Separately suspend `lookAt`, change the bot position, resume, and compare the sent cursor with the new eye ray to isolate stale geometry. Do not combine these into one ambiguous assertion.

Packet interaction tests can use Mineflayer `test/internalTest.js`; verify a real world update for a claim of placement success. [#3743's activation discussion](https://github.com/PrismarineJS/mineflayer/pull/3743#discussion_r2365596080) explains why a local call alone does not prove a server acted. [#3102](https://github.com/PrismarineJS/mineflayer/pull/3102#issuecomment-1646580592) accepts existing downstream coverage; neither implies a universal server-test demand.

## Attribute and teleport matrices

Source: [#4118 entities.js](https://github.com/PrismarineJS/mineflayer/blob/e0f82108183ceff1aeb9c8721720b68726d23c23/lib/plugins/entities.js), [attribute arithmetic](https://github.com/PrismarineJS/mineflayer/blob/e0f82108183ceff1aeb9c8721720b68726d23c23/lib/attributes.js), and the [attribute bounds reference](https://docs.neoforged.net/docs/1.21.4/entities/attributes/). Also inspect the installed minecraft-data 3.116.0 file `minecraft-data/data/pc/1.21.1/attributes.json`, which records both ranges as min 0/max 64. The recorded vanilla comparison is 1.21.1; packet/plugin probes ran 1.21.1 and 1.21.4 with NMP 1.67.0/data 3.114.0/ProtoDef 1.19.0.

Drive the actual `entity_update_attributes` handler with base reach 3 and operation-0 amounts `2`, `-4`, `100`. Expected effective ranges are 5, 0, 64. Use a target with nonzero closest-point distance below 1 to distinguish negative-total squaring from zero reach, and a distant target to distinguish unclamped upper totals. Repeat block base 4.5 with amounts 1.5, -5.5, 100. Include mixed modifier operations when arithmetic changes.

For teleports, [#4062's handler](https://github.com/PrismarineJS/mineflayer/blob/cb6e354d203dc3cdf39deff6b171918041e137b4/lib/plugins/entities.js) is a pending relative-packet implementation. Feed the production handler old velocity `(1,2,3)`, a nonzero yaw/pitch delta, and independent position/velocity-relative flags. Compare the applicable rotation formula with its source/packet contract; assert one final `entityMoved` observation and the resulting position, angles and velocity. Test the legacy packet branch separately. Supplying a feature override can isolate arithmetic but cannot prove a released dependency selects this handler.

## Real simulation and controller limits

Sources: physics [#142 index.js](https://github.com/PrismarineJS/prismarine-physics/blob/73252f2cc9081751e9ae88e7c7b6fcd5c9f077ca/index.js), [flying.test.js](https://github.com/PrismarineJS/prismarine-physics/blob/73252f2cc9081751e9ae88e7c7b6fcd5c9f077ca/test/flying.test.js), pathfinder [#382 human.js](https://github.com/PrismarineJS/mineflayer-pathfinder/blob/c59be20d646a23fe1be0b14413de944d5edbab19/lib/human.js). Other controller cases: [#376 settlement](https://github.com/PrismarineJS/mineflayer-pathfinder/pull/376#discussion_r4003064192), [#377 request options](https://github.com/PrismarineJS/mineflayer-pathfinder/pull/377#discussion_r4003066664), [#379 delayed setback](https://github.com/PrismarineJS/mineflayer-pathfinder/pull/379#discussion_r4003076403).

Reuse `flying.test.js`'s `fakePlayer` and idle controls; replace the world's `getBlock` with actual registry-created air, water, then lava blocks. Start at Y=80 with zero velocity and `flying: true`; run forty `simulatePlayer(state, world).apply(player)` ticks. Air is a positive control. The archived head yields 80, 79.12498338465008, 78.47999999999993 on both tested versions 1.13.2/1.20.4. Its five added tests pass. Vanilla source comparison used 1.20.3-pre1, not either executed version; this supports the missing fluid branch without claiming exhaustive cross-version equivalence.

For `bridgeTo`, use the existing controller and a bot adapter whose ticks run released physics on a flat solid floor. `blocks: 1, radius: 0.6` must fulfill if the final step enters the radius. Archived #382 instead rejects after reaching distance 0.16770881824918615. This control needs no placement, so it isolates completion from server acceptance.

The original local probes can be rerun if the phase3 archive exists (paths are workspace evidence, not installed-skill dependencies):

```bash
NODE_PATH=/tmp/prismarine-phase3/u9g/work/movement/runtime/node_modules node /tmp/prismarine-phase3/u9g/work/interactions/4115-partial-shape.cjs
NODE_PATH=/tmp/prismarine-phase3/u9g/work/movement/runtime/node_modules node /tmp/prismarine-phase3/u9g/work/pathfinder_physics/142/repro.cjs 1.20.4
NODE_PATH=/tmp/prismarine-phase3/u9g/work/movement/runtime/node_modules node /tmp/prismarine-phase3/u9g/work/pathfinder_physics/382/repro.cjs
```

These probes intentionally confirm archived failures; their zero exit status is not a candidate-fix pass. Convert the failure observation into the desired assertion in the target checkout's harness. Dependencies in these movement probes were data 3.116.0, block 1.23.0, world 3.7.0, chunk 1.41.0; controller simulation used released physics 1.11.1. No live server or full suite was claimed.
