# Review — mineflayer PR #3852

> *fix: auto-detect activateBlock face direction from bot position*

- **Date:** 2026-05-23
- **PR:** [PrismarineJS/mineflayer#3852](https://github.com/PrismarineJS/mineflayer/pull/3852) · fixes [#3851](https://github.com/PrismarineJS/mineflayer/issues/3851)
- **Author:** jerry1091
- **Size:** +159/−1 over 3 files · 🧪 tests included · CI ✅ all green · MERGEABLE · no review comments yet
- **Files:** `lib/plugins/inventory.js` (+18/−1), `test/internalTest.js` (+81), `test/externalTests/activateBlockFace.js` (+60)

## Verdict

**Sound idea, fixes a real bug, well-tested — but not mergeable as-is.** It silently changes a *documented* default without updating the docs, and it leaves a pre-existing `direction`/`cursorPos` geometric inconsistency in place (arguably making it more visible). Recommend: request doc update + decide whether to also fix `cursorPos`. The heuristic is a reasonable pragmatic choice over a full raycast.

---

## What it does

`activateBlock(block, direction, cursorPos)` previously defaulted `direction` to `Vec3(0,1,0)` (UP / face 1). The PR replaces that default with a position-based heuristic: when `direction` is omitted, it computes the vector from the block center to the bot, finds the dominant axis, and uses that face.

```js
if (direction == null) {
  const botPos = bot.entity.position
  const dx = botPos.x - (block.position.x + 0.5)
  const dz = botPos.z - (block.position.z + 0.5)
  const dy = (botPos.y + (bot.entity.height ?? 1.8) * 0.5) - (block.position.y + 0.5)
  const adx = Math.abs(dx), ady = Math.abs(dy), adz = Math.abs(dz)
  if (adx >= adz && adx >= ady) direction = new Vec3(dx > 0 ? 1 : -1, 0, 0)
  else if (adz >= adx && adz >= ady) direction = new Vec3(0, 0, dz > 0 ? 1 : -1)
  else direction = new Vec3(0, dy > 0 ? 1 : -1, 0)
}
```

The `directionNum` then flows into the `block_place` packet via the existing `vectorToDirection()` mapping (`0=down 1=up 2=north 3=south 4=west 5=east`).

## Why it makes sense

1. **It fixes a genuine, silent bug (#3851).** For 2-block-tall interactables (`bamboo_door`, etc.), the old UP default clicks the top face of the lower half — which the server rejects because `y+1` is occupied by the upper half. The door doesn't open and **no error is raised**, so it's hard to diagnose. Picking a side face (the normal approach for a door) sidesteps this.
2. **The new behavior is more physically realistic.** Clicking the face you approached from mirrors how a player/vanilla client interacts, rather than always reaching over the top.
3. **Backward-compatible at the API surface.** Callers passing an explicit `direction` are untouched; only default-relying callers change.
4. **No crash path.** Each branch always emits a unit vector with exactly one non-zero component (ternaries never yield `0`), so `vectorToDirection`'s `assert(false)` fallback can't be hit — even the degenerate "bot at block center" case resolves to a valid face.
5. **Thoughtful detail: bot midpoint Y.** Using `botPos.y + height*0.5` (not feet, not eyes) as the vertical reference is a deliberate choice to stop eye-level horizontal interactions from being misread as UP/DOWN. The reasoning is documented in a code comment.
6. **Real test coverage that actually runs.** The internal tests deterministically assert all 6 faces against the emitted packet. The external test runner auto-discovers `externalTests/*.js` (`fs.readdirSync(...).forEach(...)`), so the new external test genuinely executes in CI — green here means *passed*, not *skipped*.

## Problems & risks

### 1. Documented default is now wrong — **should-fix before merge**
`docs/api.md` still states:
> `direction` Optional defaults to `new Vec3(0, 1, 0)` (up).

The PR changes this behavioral contract but does not touch the docs. At minimum the docs must be updated to describe the auto-detection (and that passing an explicit `direction` restores the old fixed behavior).

### 2. `direction` and `cursorPos` are now geometrically inconsistent — **design gap**
`cursorPos` still defaults to `Vec3(0.5, 0.5, 0.5)` (block center), independent of the chosen face. So the packet says "I clicked the **east** face" but "the cursor is at the block **center**." The two no longer describe the same point on the same face.
- This is *pre-existing* (UP + center was already off-face), so it isn't a regression — but the PR makes it more conspicuous by varying the face per-call, and it's the natural place to fix it.
- Vanilla servers are lenient about `cursorPos` for pure interactions, so this likely won't break the door fix. But face-sensitive servers / anti-cheat could care. Ideally, when auto-detecting, set `cursorPos` onto the chosen face (e.g. east → `cursorX≈1.0`).

### 3. Heuristic, not a raycast — **acceptable, but worth a note**
The dominant-axis nearest-face heuristic ignores obstruction and the bot's actual look ray. A more robust solution is the block face from `bot.world.raycast()` (bot eye → block), which would also yield a *consistent* `cursorPos` for free. The heuristic is a fair pragmatic trade-off (cheaper, no raycast dependency), and it covers the reported case; just flag raycast as the more correct long-term approach. Note `lookAt` still targets the block center while a side face is reported — same center-vs-face mismatch as #2.

### 4. Behavior change when activating *while holding a placeable item* — **low risk**
`activateBlock` forwards `heldItem`/`hand`, so the direction also dictates where a held block would be placed. A bot that relied on the UP default to place a held item on top while "activating" would now place it on the side facing the bot. This is niche (`placeBlock` is the intended placement API), but it's a real semantic change beyond the "only broken cases change" claim in the PR description.

### 5. External test gaps — **minor**
- Covers only the 4 horizontal faces; the internal tests do cover UP/DOWN, so net coverage is fine, but the external (real-server) path doesn't exercise vertical.
- Uses a `stone` block and asserts the **packet direction**, not the **actual outcome** (door opening). It validates the mechanism, not the #3851 regression itself. A test against a real 2-tall block confirming it opens would more directly guard the bug.
- It monkeypatches `bot._client.write` to capture the packet (restores it after). Functional, slightly hacky.

### 6. Tie-breaking is arbitrary — **cosmetic**
`>=` makes ties resolve X → Z → Y. Fine in practice (exact ties are physically rare), just undocumented.

## Recommendations

| # | Action | Priority |
|---|--------|----------|
| 1 | Update `docs/api.md` to document the new auto-detection default | Should-fix (blocking) |
| 2 | Decide on `cursorPos`: set it onto the detected face, or explicitly document that it stays at center | Should-fix |
| 3 | Consider `bot.world.raycast()` for face + consistent cursor (or note as follow-up) | Nice-to-have |
| 4 | Note the held-item placement behavior change in the PR description / changelog | Nice-to-have |
| 5 | Add an external test that asserts a 2-tall block actually opens (the real #3851 case) | Nice-to-have |

**Bottom line:** approve the direction (pun intended), but block on the docs update and a `cursorPos` decision. The core change is small, correct for the reported bug, and properly tested.
