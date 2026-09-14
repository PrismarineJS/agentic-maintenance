---
name: prismarine-world-render-review
description: Review PrismarineJS world-to-viewer integration, registry and dimension state, chunk/section coordinates, entity update rendering, worker and asset lifetimes, readiness and host contracts. Use for prismarine-viewer or its world/entity producers; use item-inventory review for item wire/model conversion.
---

# World and rendering review

Follow the producer and consumer together: Mineflayer world/entity events, `WorldView` transport, `Viewer` forwarding, `WorldRenderer`/`Entities`, and worker/asset completion. Review the contract at the actual head; several examples below are pending PR APIs. Read [recipes and source record](references/recipes.md) for executable checks, immutable sources and version limits.

## Registry and world identity

Entry points are Mineflayer `lib/plugins/blocks.js` and `game.js`; viewer `viewer/lib/worldView.js::{listenToBot,loadChunk,unloadChunk}`, `viewer.js`, `world.js`, and `worker.js`. A registry constructed from a version string reproduces static data, not a live registry's packet-driven state. If a change passes a registry into one constructor, trace subsequent world/column construction and worker messages too. Worker-local copies need a defined snapshot/update transport; they do not acquire updates by sharing the same version name. [Viewer #307](https://github.com/PrismarineJS/prismarine-viewer/pull/307#discussion_r995182554) documents this ownership problem and the subsequent reconsideration of initial approval.

`WorldView` holds a world reference while `bot.world` may be replaced. Trace the actual replacement event order before alleging a timing bug. Pending #513 follows replacement on `login` and unloads ordinary completed loads correctly, but an earlier awaited `getColumnAt` can still return an old-world column after unload/login. Clearing `loadedChunks` alone does not cancel that operation. Completion needs current world/generation and per-column intent checks. A global world generation alone misses unload/reload of the same coordinate within one world.

## Dimension and section coordinates

`WorldView` load events use block-origin X/Z coordinates; `simpleUtils.js::chunkPos` yields chunk indices. Preserve floor semantics at negative coordinates: block -1 belongs to chunk -1, origin -16. `WorldRenderer::{addColumn,removeColumn,setSectionDirty}` schedules section origins in increments of 16. In the inspected worker, Y is quantized before indexing `chunk.sections[(y - chunk.minY)/16]`; inspect upstream quantization before calling removal of a nearby `Math.floor` a bug.

Dimension bounds belong to the world/column contract, not a universal 0..255 range. Walk `minY` through `minY + worldHeight` exclusively for scheduling and removal, including neighboring sections dirtied by border edits. Test default public callers that omit new arguments as well as callers supplying custom bounds. In pending #488, default `addColumn(..., minY=0, worldHeight=256)` and downstream reconstruction can disagree with negative/custom column bounds. In #484, bounds loaded asynchronously postpone dirty registration: `sectionsOutstanding.size === 0` before registration is not evidence rendering finished.

## Entity updates are patches

`WorldView::listenToBot` emits different field subsets for spawn, movement, attachment, hurt, metadata and deletion. `entities.js::Entities.update` must retain logical state independently of whether a THREE object exists. An absent `invisible` field in a movement update does not mean false. Pending #514 removes an invisible entity's mesh, then a position-only update can recreate it unless invisibility survives separately. Test invisible spawn → movement → visible metadata → movement, including initial enumeration and listener removal. Scope the expectation to the viewer's promised model visibility; do not infer all vanilla glowing/team/name-tag behavior.

Dropped-item rendering crosses metadata parsing in `WorldView`, item-name lookup, `Entities.update`, and `entity/Item.js`. Missing stack data, an unsupported texture entry and a load still pending are distinct states. Check both unsupported-item fallback and supported-item geometry. In pending #506, released 1.21.4 assets contain no usable texture for some resolved items; registering an empty group prevents later updates from recovering the prior drawable fallback. Additional asset coverage is separate from preserving that fallback.

## Asynchronous assets, readiness and ownership

Inspect `worldrenderer.js::setVersion`, worker message handlers, `entity/Entity.js`, `entity/Item.js`, `textures.js`, and `dispose.js::dispose3`. Suspend asset loads or worker responses, change version/remove the entity/dispose the viewer, then finish the old job. Check that stale completion cannot attach geometry or mutate current materials, and determine who disposes any allocation made after cancellation. Shared cached textures and per-object geometry have different owners; blindly disposing every referenced texture can break another live object.

Readiness is a promised set of completed work, not just an empty queue. Pending #503's `waitForReady` waits on atlas and registered chunk work, while entity texture requests start at `onBeforeRender`. A screenshot caller may need those requests scheduled before its first frame. Required atlas rejection must be distinguishable from optional texture fallback; `catch(() => null)` can make a failed required resource appear ready. Check successful delayed loading as a control before criticizing the barrier.

Host abstraction changes cross runtime factories, renderer calls, tests, and public `index.d.ts`. In pending #511, runtime requires `host.loadText`, while `Host` and factory return types omit it: valid TypeScript hosts fail at `setVersion`, and built-in hosts' method is inaccessible by type. Use the existing `test/host.test.js` and a temporary consumer probe; propose extending coverage when this boundary needs it. Inspect the checkout's test scripts; some archived viewer heads have recursive `npm test`. Use the actual Jest target and generated fixtures it needs. Real THREE object/geometry checks suffice for local lifetime claims; browser/WebGL evidence is needed when the claim concerns pixels or first-frame fidelity.
