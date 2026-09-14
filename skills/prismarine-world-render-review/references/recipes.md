# World/render recipes and evidence

The [2026-09-14 re-reviews](../../../implementation/phase3/u9g_rereviews.json) record head SHAs and the [independent checks](../../../implementation/phase3/u9g_independent_checks.json) independently revisit #506. Recent Astra reviews are concrete engineering evidence, not independent manual maintainer policy. These checks exercise archived pending heads separately; a proposed API is not assumed available in another PR or release.

## Deferred columns and partial entities

Sources: [#513 WorldView](https://github.com/PrismarineJS/prismarine-viewer/blob/814b753c96bbb311c4fc020a9c74e445abb642df/viewer/lib/worldView.js), [#514 WorldView](https://github.com/PrismarineJS/prismarine-viewer/blob/45f7de5cec3e9db3097b5e95bb43ba16331eb3f8/viewer/lib/worldView.js), [#514 Entities](https://github.com/PrismarineJS/prismarine-viewer/blob/45f7de5cec3e9db3097b5e95bb43ba16331eb3f8/viewer/lib/entities.js).

This adaptable Node check uses actual `WorldView` and a deliberately deferred column provider. Run from a checkout with its declared dependencies; it fails on archived #513 because stale load repopulates the unloaded column:

```js
const assert = require('assert/strict')
const { EventEmitter } = require('events')
const { Vec3 } = require('vec3')
const { WorldView } = require('./viewer/lib/worldView')
async function check () {
  let resolveOld
  const oldWorld = { getColumnAt: () => new Promise(r => { resolveOld = r }) }
  const bot = new EventEmitter()
  Object.assign(bot, { username: 'probe', entity: {}, entities: {}, world: oldWorld })
  const view = new WorldView(oldWorld, 2)
  view.listenToBot(bot)
  const loads = []
  view.on('loadChunk', chunk => loads.push(chunk))
  const pos = new Vec3(0, 0, 0)
  const pending = view.loadChunk(pos)
  bot.emit('chunkColumnUnload', pos)
  bot.world = { getColumnAt: async () => ({ toJson: () => 'new' }) }
  bot.emit('login')
  resolveOld({ toJson: () => 'old' })
  await pending
  assert.equal(loads.length, 0)
  assert.equal(view.loadedChunks['0,0'], undefined)
  await view.loadChunk(pos)
  assert.equal(loads[0].chunk, 'new')
  view.removeListenersFromBot(bot)
  assert.equal(bot.listenerCount('login'), 0)
  assert.equal(bot.listenerCount('chunkColumnUnload'), 0)
}
check().catch(error => { console.error(error); process.exitCode = 1 })
```

Also run completed load → unload and replacement login → new load as success controls. For same-world unload/reload, defer two loads for the same coordinate and resolve the older one last. A cancellation design must preserve the newer result.

For visibility, wire actual `WorldView` entity events into `Entities.update`, create entity metadata `{0: 0x20}`, emit spawn then position-only movement. Assert no model is created while invisible. Set metadata byte to zero and emit `entityUpdate`; the entity should become drawable according to the implementation's update contract. Moving an initially visible entity is the control. This tests persistent state, not rendered pixels. Follow `removeListenersFromBot` to ensure the new metadata listener leaves with its owner.

## Bounds and worker completion

Sources: [#488 renderer](https://github.com/PrismarineJS/prismarine-viewer/blob/8049729deabbfe39d5beb14af5a543c927bb66a3/viewer/lib/worldrenderer.js), [worker](https://github.com/PrismarineJS/prismarine-viewer/blob/8049729deabbfe39d5beb14af5a543c927bb66a3/viewer/lib/worker.js), [#484 renderer](https://github.com/PrismarineJS/prismarine-viewer/blob/dc777aa049507363ecefbb5e1dc8dba2c2160a11/viewer/lib/worldrenderer.js).

Create real prismarine-chunk columns for an old dimension (`minY=0,height=256`), negative-height dimension (`-64,384`), and a custom supported bound. Intercept worker messages rather than invoking WebGL. Compare scheduled/removal Y origins with the actual column; include `x/z=-1,-16,-17` at the block-input boundary. Worker section origins are already floored, so `(y-minY)/16` should be integral for aligned bounds. A real block at `minY+1` must produce geometry through `models.js`/`world.js` and `worker.js` meshing; the archived geometry check uses a small cube atlas/model fixture and expects six faces/24 vertices for 1.16.4, 1.21.4 and 26.1.

For #484, hold the `worldBounds.json` loader callback, call `setVersion('1.21.4')`, `addColumn`, then `waitForChunksToRender`. Record whether the promise resolves before any dirty messages. Release bounds and confirm registration: archived behavior schedules 120 entries, five columns/neighbors × 24 Y sections, from -64 through 304. A fixed barrier must include registration as well as worker completion. Preserve a synchronous-bounds control. This fixture tests scheduling and minimal geometry, not a complete assets atlas or vanilla rendering equivalence.

## Readiness, supported fallback and Host types

Sources: [#503 readiness implementation](https://github.com/PrismarineJS/prismarine-viewer/blob/af9075bb69c4a8d895ea8710898c56cf25db2f42/viewer/lib/worldrenderer.js), [lazy Entity loading](https://github.com/PrismarineJS/prismarine-viewer/blob/af9075bb69c4a8d895ea8710898c56cf25db2f42/viewer/lib/entity/Entity.js), [#506 Item](https://github.com/PrismarineJS/prismarine-viewer/blob/4c2502419e916aec7cba4e5f2005d745ef30eae0/viewer/lib/entity/Item.js), [released 1.17.0 item texture index](https://github.com/PrismarineJS/minecraft-assets/blob/1.17.0/data/1.21.4/items_textures.json), [#511 declarations](https://github.com/PrismarineJS/prismarine-viewer/blob/05bd6ecb5578ecc72ac45abc52c819f8e59f2422/index.d.ts).

Reuse viewer `test/host.test.js` for injected host tests and `test/viewer.test.js`/`test/simple.test.js` for browser expectations. With actual THREE 0.128.0, inject deferred `host.loadImage` and no mesher workers. Confirm `waitForReady` stays pending until successful atlas load installs a `DataTexture`; separately reject the required atlas and observe whether readiness wrongly fulfills without a map. Construct an `Entity`, count load requests before and after `onBeforeRender`: a zero count before rendering shows that waiting on already-started work cannot guarantee entity textures for a first-frame consumer.

For item fallback, use registry-resolved 1.21.4 `pale_oak_planks` (missing texture) and `decorated_pot` (unsupported `entity/` entry) through actual WorldView → Entities → Item. Count drawable geometry at base and head, then send further metadata/movement. Archived #506 changes one fallback geometry into a persistent empty group. `oak_planks` with controlled opaque pixel data is a supported-item success control. Use actual released assets satisfying the branch's range; do not apply another pending assets PR to conceal missing fallback.

For ownership, defer the supported-item load, remove its entity, resolve pixels, and count allocations/disposals. Repeat after world version replacement for atlas/worker jobs; assert the new scene/material is unchanged. Pixel data can be controlled while actual THREE resource objects and production cleanup run.

Compile a consumer accessing `createNodeHost().loadText` and another implementing exported `Host` without it. At archived #511, TypeScript 5.9.3 rejects the built-in method but accepts the incomplete host, which throws at runtime `setVersion`. The correct regression checks both sides of this contract. The historical eight focused Jest host/texture tests pass despite that mismatch; excluded tests require generated fixtures or timing measurements.

Archived executable probes are optional workspace evidence. These caches split dependencies across directories, so include all three; select the installed Node executable if `node` is not on PATH:

```bash
export NODE_PATH=/tmp/prismarine-phase3/u9g/work/movement/runtime/node_modules:/tmp/prismarine-phase3/u9g/work/viewer_core/deps/node_modules:/tmp/prismarine-phase3/u9g/work/viewer_stack_items/deps/node_modules
node /tmp/prismarine-phase3/u9g/work/viewer_core/lifecycle.cjs
node /tmp/prismarine-phase3/u9g/work/viewer_stack_items/484/bounds-check.cjs
node /tmp/prismarine-phase3/u9g/work/viewer_stack_items/503/readiness-check.cjs
node /tmp/prismarine-phase3/u9g/work/viewer_core/fallback.cjs
```

The probes mix success controls with confirmation of archived defects; exit zero alone does not mean a fix passes. The independent #506 check used THREE 0.128.0, assets 1.17.0 and data 3.114.0. No browser/WebGL, live transfer server, full generated-assets suite or held-out performance/accuracy benchmark is implied.
