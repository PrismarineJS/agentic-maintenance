# Booting Paper (+ plugins) in mineflayer's test infra

> How to wire the [FaceCheck](../../implementation/phase1/facecheck-plugin/) Paper
> integration test into mineflayer's harness: extend `node-minecraft-wrap`, make a
> new repo, or keep it in mineflayer? Investigation + options.

- **Date:** 2026-05-23
- **Context:** Implements "Tier 2" from
  [`anticheat_testing.md`](./anticheat_testing.md) — an end-to-end test that boots
  Paper + a validation plugin and checks `activateBlock` against strict
  face/raytrace validation.
- **Prereq finding:** the bug only reproduces under server-side face validation;
  the deterministic stand-in is the FaceCheck Paper plugin.

## What we actually need

Three distinct sub-problems — they live at different layers, which is the crux of
the "extend vs new repo" decision:

| # | Need | Layer |
|---|------|-------|
| 1 | Obtain a **Paper** server jar for a given MC version | download |
| 2 | Boot it (offline, flat, plugin loaded) and drive it | run |
| 3 | **Build** the FaceCheck plugin jar (`javac` + `jar`) | build (Java) |

## How `node-minecraft-wrap` works today (investigation)

`minecraft-wrap@1.7.0` (actively maintained — 1.7.0 released 2026-03, CI on Node 24).

- **Run layer is already jar-agnostic.** `new Wrap(jar, dir, OPTIONS).startServer(props, cb)` just spawns `java -jar <jar> nogui` with `cwd=dir`. It writes `server.properties`, `eula.txt`, and empty `ops.json`/`whitelist.json`/etc. `OPTIONS` supports `minMem`/`maxMem`, **`doneRegex`**, **`noOverride`** (skip writing the config files), and `javaPath`. PRs #6/#7 added these *specifically for non-vanilla jars*; HISTORY notes "improve default done regex to support both spigot and vanilla."
  - ✅ Paper boots unchanged — verified. Paper's "Done" line matches the default `doneRegex` (`/\[.+\]: Done/`).
- **Plugins: no API, but it already works.** Since the jar runs with `cwd=dir`, dropping jars into `dir/plugins/` before `startServer` loads them. `startServer` does **not** wipe the dir (only `deleteServerData` does), so pre-seeding `plugins/` is safe.
- **Download layer is vanilla-only.** `download(version, file, cb)` → `getServer` reads Mojang's `version_manifest.json` and downloads `versionInfo.downloads.server`. There is **no** Paper/Spigot fetch.
- **Open issue [#45 "Spigot support"](https://github.com/PrismarineJS/node-minecraft-wrap/issues/45)** (since 2020) asks for exactly this; rom1504 commented favorably (referencing itzg/docker-minecraft-server). So extending the download layer has a standing request and maintainer buy-in.

**Net:** problems #2 (run) and #1-as-plugins are already solved by the existing
library. The only true gap in `minecraft-wrap` is #1 for Paper. Problem #3 (Java
compile) is outside any JS download/run library's scope.

## How mineflayer uses it today

`test/externalTest.js` loops `mineflayer.testedVersions`, calls
`download(minecraftVersion, jar)`, then `new Wrap(...).startServer(propOverrides)`
with vanilla servers, and auto-discovers `test/externalTests/*.js`. A Paper+plugin
test does **not** fit this per-version vanilla matrix (Paper-only, needs a built
plugin) — it should be a **separate, opt-in path**, not shoehorned into the matrix.

## Getting a Paper jar (the #1 gap)

Paper has a clean HTTP API — no BuildTools/compile needed (that's Spigot):

```
GET https://api.papermc.io/v2/projects/paper/versions/{ver}/builds   -> pick latest build
GET .../versions/{ver}/builds/{build}/downloads/paper-{ver}-{build}.jar
```

(verified working earlier for 1.21.1 and 1.21.11). Note PaperMC is migrating to a
v3 "Fill" API; whatever lands should pin/version this.

## Options

### Option A — Extend `node-minecraft-wrap`
Add `downloadPaper(version, filename, cb)` (PaperMC API) alongside `download`, and
document `plugins/` + `noOverride`. Optionally a small `plugins: [jarPaths]`
convenience that copies jars into `dir/plugins/` on `startServer`.

- **Pros:** closes existing issue #45; maintainer already interested; run layer
  already supports it; one cohesive dependency the whole PrismarineJS ecosystem
  (and mineflayer) already has; smallest surface area.
- **Cons:** broadens a "vanilla" library's scope; Paper API differs from Mojang's
  and evolves (v3); does **not** address #3 (plugin compile) — that stays in the
  consumer.

### Option B — New repo / package (e.g. `node-minecraft-paper`)
A dedicated package owning Paper specifics (PaperMC API download, plugin install,
maybe even a plugin-build helper), wrapping or reusing `minecraft-wrap`'s `Wrap`.

- **Pros:** keeps `minecraft-wrap` vanilla-pure; can own Paper/plugin concerns and
  release independently; natural home if plugin-build helpers grow.
- **Cons:** another repo to maintain + publish; ecosystem fragmentation and
  discoverability; largely duplicates run logic or adds a dependency hop;
  overkill for one ~40-line plugin and one test.

### Option C — Keep everything in mineflayer's test dir
Add a `test/paper/` helper that downloads Paper (inline PaperMC fetch), builds
FaceCheck, and boots via the existing `Wrap`. No library changes.

- **Pros:** zero external changes; fastest to ship; self-contained.
- **Cons:** not reusable by other PrismarineJS projects; Paper-download logic
  rots in test fixtures; duplicates what #45 wants in the shared lib.

### Option D — Hybrid (recommended)
Split by layer, matching where each concern belongs:
1. **`minecraft-wrap`:** add `downloadPaper` (Option A core) — closes #45, reusable.
2. **mineflayer test infra:** owns the plugin **build** (#3) and the assertions —
   a dedicated `test/externalPaper.js` (or a CI job) that builds `facecheck.jar`,
   downloads Paper via `downloadPaper`, boots with the plugin, and runs the door
   open/close check.

This keeps `minecraft-wrap` as "fetch & run any server jar (vanilla or Paper)"
and leaves Java compilation — which no JS server lib should own — in the consumer.

## Problem #3: building / shipping the FaceCheck jar

| Approach | Pros | Cons |
|---|---|---|
| **Build in CI** (JDK + extract Paper API + `javac`/`jar`) | no binaries in git; always matches API | adds a JDK + build step to the job |
| **Commit a prebuilt jar** | simplest job | binary in repo (trust/review/size); version drift |
| **Release artifact** (attach jar to a release/tag) | no repo binary; cached | release plumbing; provenance |

The plugin uses only stable Bukkit API (`PlayerInteractEvent`, `rayTraceBlocks`),
so one jar is portable across many MC versions via `api-version`. **Recommend
build-in-CI** (a few lines, no committed binary); the build recipe is already in
the [plugin README](../../implementation/phase1/facecheck-plugin/README.md).

## Concrete sketch (recommended path)

`minecraft-wrap` addition:
```js
// lib/paper_download.js
const fetch = require('node-fetch')
async function downloadPaper (version, filename) {
  const api = 'https://api.papermc.io/v2/projects/paper/versions/' + version
  const builds = (await (await fetch(api + '/builds')).json()).builds
  const b = builds[builds.length - 1].build
  const name = `paper-${version}-${b}.jar`
  const res = await fetch(`${api}/builds/${b}/downloads/${name}`)
  // ...stream to filename, return { build: b }
}
```

mineflayer `test/externalPaper.js` (opt-in, single modern version):
```js
// 1. build facecheck.jar (javac against extracted Paper API)  [or use cached]
// 2. await downloadPaper('1.21.1', paperJar)
// 3. fs.mkdirSync(dir/plugins); copy facecheck.jar in
// 4. new Wrap(paperJar, dir, { noOverride:false }).startServer({'online-mode':'false','level-type':'FLAT', gamemode:'0'})
// 5. connect a NON-opped bot; place a 2-tall door via console
// 6. assert activateBlock(door, Vec3(0,1,0)) leaves it shut; activateBlock(door) opens it
```

## Where it runs in CI

- **Primary regression guard stays Tier 1** (no server: internal tests assert the
  packet face/cursor match the bot's own eye→block raytrace). Cheap, per-version,
  already green for the raycast PR.
- **Paper+FaceCheck = a separate optional job** (`paper-integration`), one modern
  MC version, manual/nightly or label-gated — not the per-version matrix (Paper
  boot + JDK build is too heavy to multiply across 27 versions).

## Recommendation

1. **Adopt Option D.** Land a small `downloadPaper` in `node-minecraft-wrap`
   (closing #45 — there's appetite), and keep the plugin build + assertions in a
   dedicated, opt-in mineflayer test.
2. **Build FaceCheck in CI**, don't commit the jar.
3. **Don't put Paper in the main version matrix** — one modern version, opt-in.
4. If Paper/plugin tooling later grows beyond a download helper (multiple plugins,
   build helpers, Spigot via BuildTools), revisit **Option B** (dedicated repo).

## Open questions / follow-ups
- Scope of the `minecraft-wrap` change: just `downloadPaper`, or also a `plugins:`
  copy-in option? (Lean minimal: just the download; document plugin placement.)
- Pin PaperMC API version (v2 today; v3 "Fill" incoming) and handle "no build for
  this MC version yet."
- Should `downloadPaper` cache by `{version, build}` like vanilla jars are cached
  in CI to avoid re-downloads?
- Confirm whether maintainers want Spigot (BuildTools) too, or Paper-only.
