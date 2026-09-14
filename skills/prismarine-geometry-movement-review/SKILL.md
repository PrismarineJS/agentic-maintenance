---
name: prismarine-geometry-movement-review
description: Review PrismarineJS block picking, placement and entity reach geometry, movement physics, teleport transforms and pathfinder action completion. Use for coordinate, collision, locomotion or movement-controller regressions; use lifecycle-action review for protocol phase and queued-reply ownership.
---

# Geometry and movement review

Start at the representation consumed by the changed operation: a block's local shapes, an entity's feet/eye/bounds, a protocol rotation, or a simulated `PlayerState`. Inspect the reviewed revision before using these entry points. The linked [recipes and source record](references/recipes.md) distinguish released dependencies from pending PR examples and provide concrete probes.

## Block picking and interaction coordinates

Mineflayer's `lib/plugins/generic_place.js::_genericPlace`, `inventory.js` interaction methods, `ray_trace.js`, and `physics.js::lookAt` connect camera geometry to packets. Prismarine-world's `raycast`/`RaycastIterator.intersect` intersects `block.shapes`: arrays `[minX,minY,minZ,maxX,maxY,maxZ]` relative to the block position. A block coordinate identifies a cell, not a solid unit cube. Slabs, stairs and fences require their actual shapes; sample points on a unit cube can miss a visible surface even while the bot stands still.

For a pick, preserve the tuple **eye origin, ray direction, hit block, hit face, intersection**. Cursor coordinates are `hit.intersect - block.position`; placement location is the reference block, not the destination cell. Face numbers are down/up/north/south/west/east = 0/1/2/3/4/5. A bottom slab's top cursor has `y=0.5`, not 1. Older placement branches quantize cursor components with `floor(component*16)`; later branches write floats. Select the actual feature branch and serializer when checking packets.

The view direction in Mineflayer radians is `(-sin(yaw)*cos(pitch), sin(pitch), -cos(yaw)*cos(pitch))`: yaw zero faces negative Z and positive pitch looks up. Wire degrees/bytes pass through `lib/conversions.js`; adding protocol degrees directly to model radians is invalid. Compare each caller's eye origin: `position` is feet, `eyeHeight` differs from full `height`, and crouching changes it. Do not copy a neighboring helper's origin without checking it. A hit computed before awaited `lookAt` can become stale after movement or a world update; recheck the post-await ray when that await is part of the changed path.

In pending Mineflayer #4115, `placeFaceStrict`, `strictFace`, and face sampling are proposed behavior, not universal released APIs. Its nine cube-oriented tests passed while a bottom slab failed. Respect explicit `delta` and `forceLook: 'ignore'` bypasses and distinguish a new strict rejection from inherited fallback behavior.

## Entity bounds and effective attributes

Entity ray bounds are centered in X/Z and start at feet Y: `[-width/2,0,-width/2,width/2,height,width/2]`. Interaction hit vectors can be entity-relative; trace `inventory.js::activateEntityAt` before subtracting position, and preserve caller-owned vectors. For reach predicates, closest-point distance to an AABB and distance to an entity center answer different questions.

`entities.js` receives attribute base/modifier records. Pending #4118 adds `lib/attributes.js::{getAttributeValue,findAttribute,attributeValue}` and interaction-range helpers. Its arithmetic applies operation 0 additions, operation 1 additions relative to that subtotal, then operation 2 multipliers. Effective values also need the registered attribute bounds: the tested 1.21.1 interaction ranges are `[0,64]`. Clamp the final total before squaring a reach distance; raw `-1` becomes a false positive after squaring. Check namespaced/legacy keys and absent-attribute fallbacks against the target registry. Do not impose interaction-range bounds on unrelated attributes.

## Teleports and simulation branches

Keep self-position handling in Mineflayer `physics.js` distinct from other-entity teleport handlers in `entities.js`. Legacy packets may use fixed-point positions, byte angles or numeric flag masks; newer packets use double positions, degree angles and flag objects. Relative position axes, relative velocity axes and rotation of the old velocity are separate operations. A zero-velocity fixture cannot expose an omitted `ROTATE_DELTA` transformation. Use a nonzero asymmetric vector and nonzero rotation, checking the applicable feature's actual released availability.

Prismarine-physics `index.js::Physics`, `simulatePlayer`, `moveEntityWithHeading`, and `PlayerState` own local motion. Read the water/lava branch before concluding that a fix to normal movement implements flight. Pending #142 added `flying`/`flyingSpeed` state, yet forty idle ticks held altitude in air and sank in source water/lava. Exercise the changed branch with real block/data fixtures; this does not establish released Mineflayer abilities integration or server-authoritative movement.

## Pathfinder completion and cancellation

For ordinary pathfinding inspect goals, movement costs, and the caller's success contract. Pending human-controller APIs live in `mineflayer-pathfinder/lib/human.js`, with declarations in `index.d.ts`: `walkTo`, `lookAt`, `bridgeTo`, and `stop` are branch-specific. Trace planning, reaction delay, movement, settlement, and terminal cleanup separately. An empty path can mean already at the goal; a partial path's last node is not necessarily the goal. Check success after the final permitted bridge step, not only at loop entry.

Joining requests by target alone loses differing radius, facing or timeout requirements. A timeout or quiet-period cap must not manufacture successful settlement. After an awaited reaction delay, cancellation/setback identity still matters before changing controls. Prefer the existing pathfinder `test/internalTest.js` or a real-physics adapter for these traces; require a server observation when the claim specifically concerns accepted placement or authoritative movement. Existing focused model coverage can suffice, and an unrelated controller refactor need not block a bounded correction.
