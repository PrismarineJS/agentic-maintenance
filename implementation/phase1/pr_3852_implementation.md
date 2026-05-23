# Implementation report — mineflayer PR #3852 fix

> Implementing the raycast-based `activateBlock` face detection from
> [`design/phase1/pr_3852_fix_proposal.md`](../../design/phase1/pr_3852_fix_proposal.md),
> and what testing it against real servers revealed.

- **Date:** 2026-05-23
- **PR:** [PrismarineJS/mineflayer#3852](https://github.com/PrismarineJS/mineflayer/pull/3852) · issue [#3851](https://github.com/PrismarineJS/mineflayer/issues/3851)
- **Where the code lives:** local clone at `mineflayer/`, branch `fix/activateBlock-raycast-impl` (committed locally, **not pushed to the PR**, per instruction). Diff also saved as [`pr_3852_fix.patch`](./pr_3852_fix.patch).
- **Companion docs:** [`pr_3852_review.md`](../../design/phase1/pr_3852_review.md) · [`pr_3852_fix_proposal.md`](../../design/phase1/pr_3852_fix_proposal.md)

## TL;DR

The raycast fix is **implemented, lint-clean, and passes 162 internal tests** across all 27 supported versions. End-to-end it opens a real 2-tall door via auto-detect.

**But the headline finding is about the bug, not the fix:** I could **not reproduce the reported silent failure** on vanilla *or* Paper at *either* 1.21.1 or 1.21.11 — the old `UP` default opens the door in every case I tried. The bug almost certainly needs an **anti-cheat plugin** that enforces face/look-ray consistency (the reporter ran Paper, likely with such a plugin). That changes how this PR should be evaluated and tested — details below.

## What was implemented

Per the proposal: raycast primary, positional-heuristic fallback. In `lib/plugins/inventory.js`, when `activateBlock` is called without a `direction`:

1. Raycast from the bot's eyes to the block center; if it hits the target block, use `hit.face` for the direction and `hit.intersect` for a cursor **on that face**.
2. If the block isn't directly visible (occluded / out of reach), fall back to the PR's dominant-axis heuristic.
3. `lookAt` now targets the actual click point, so **look direction, face, and cursor all agree** (this is the part anti-cheat validates).

Key helper (full diff in the patch):

```js
function raycastInteractFace (block) {
  const eye = bot.entity.position.offset(0, bot.entity.eyeHeight, 0)
  const center = block.position.offset(0.5, 0.5, 0.5)
  const range = eye.distanceTo(center) + 0.5 // distance-based, not a fixed 5
  const hit = bot.world.raycast(eye, center.minus(eye).normalize(), range)
  if (!hit || !hit.position.equals(block.position)) return null
  return { direction: faceToVector[hit.face], cursorPos: hit.intersect.minus(block.position) }
}
```

Verified facts that de-risked the implementation:
- `prismarine-world` `BlockFace` is `{BOTTOM:0, TOP:1, NORTH:2, SOUTH:3, WEST:4, EAST:5}` — identical to the `block_place` `direction` field and `vectorToDirection()`, so the `faceToVector` table round-trips correctly.
- `bot.world.raycast(...)` is synchronous and returns the block augmented with `.face` and `.intersect` (confirmed in `node_modules/prismarine-world/src/worldsync.js` and the existing `bot.dig(..., 'raycast')` usage).
- Distance-based `range` matters: a bot above a block sits >5 blocks from the top face at eye height, so `dig`'s hardcoded `5` would have missed it. My UP/DOWN tests pass because of this.

### Files changed (`+125 / −26`)

| File | Change |
|------|--------|
| `lib/plugins/inventory.js` | raycast detection + heuristic fallback + lookAt hit point |
| `docs/api.md` | document the new auto-detection default (old docs said "defaults to UP") |
| `test/internalTest.js` | add cursor-on-face assertion to the 6 existing face tests |
| `test/externalTests/activateBlockFace.js` | capture full packet + cursor-on-face check + real door open/close regression |

## Validation

### Lint — pass
`standard` (JS) and `standard-markdown` (docs) both clean on all changed files.

### Internal tests — 162/162 pass
`mocha test/internalTest.js --grep "activateBlock face direction"` → all 6 faces × 27 versions. These run against a mocked server but use the **real** `bot.world.raycast` against real block shapes from the registry, so they genuinely validate face selection. The new cursor assertion passes for both the old scaled-by-16 cursor encoding (e.g. 1.8.8) and the modern raw `[0,1]` encoding.

### End-to-end — real servers (the revealing part)
A/B script: place a closed 2-tall `bamboo_door`, bot 2 blocks to the west, then (A) `activateBlock(door, Vec3(0,1,0))` = old UP default, and (B) `activateBlock(door)` = new auto-detect. Expected per the issue: A stays shut, B opens.

| Server | Build | A: explicit UP | B: auto-detect |
|--------|-------|----------------|----------------|
| Vanilla | 1.21.1 | **opens** ❌(expected shut) | opens ✅ |
| Paper | 1.21.1 (#133) | **opens** ❌ | opens ✅ |
| Vanilla | 1.21.11 | **opens** ❌ | opens ✅ |
| Paper | 1.21.11 (#69) | **opens** ❌ | opens ✅ |

The fix's path (B) works everywhere. But (A) — the supposedly-broken old behavior — **also opens the door everywhere**, including on the reporter's exact version/family (Paper 1.21.11). I could not reproduce the bug.

## Why the bug doesn't reproduce (analysis)

In Minecraft, a *right-click-to-use* (door toggle) is processed server-side largely **independent of the clicked face** — the face matters for block *placement*, not interaction. So on a stock server, clicking any face (including the "occluded" top face of the lower door half) toggles the door. The issue's stated root cause — *"the server rejects clicking the top face because the upper half occupies y+1"* — does not hold on vanilla or stock Paper.

What *does* reject a face/look mismatch: **anti-cheat plugins** (Grim, NCP, Spartan, etc.) that raytrace from the player's eyes and verify the claimed face/cursor matches what the player is actually looking at. The reporter's server was Paper "offline-mode" — very likely with such a plugin. Under that validation:
- Old code: face `UP` + `lookAt(center)` → the eye ray to center hits a **side** face → claimed `UP` ≠ raytraced side face → **rejected**. ✔ matches the report.
- This PR's heuristic: side face + `lookAt(center)` → ray hits the side face → matches → accepted.
- **This implementation:** raycast face + cursor on face + `lookAt(hit point)` → fully self-consistent → accepted, and most robust of the three.

So the bug is real but **environment-specific (anti-cheat servers)**, and the raycast approach is the best-shaped fix for it because it *reproduces the server's own raytrace*.

## Implications

1. **The fix is safe to merge.** It does not regress stock servers (door still opens in all 4 tests) and is strictly better on strict/anti-cheat servers. Low risk.
2. **The external door-open regression test I added does NOT guard the regression in CI.** Because UP also opens the door on vanilla (which is what CI runs), the door test passes with *or without* the fix. Its real value is reduced to an integration sanity check (the auto-detected face/cursor produce a server-accepted interaction). The **packet-direction and cursor-on-face assertions remain meaningful**. I kept the door test but this limitation should be understood — a true regression test would need an anti-cheat-enabled server, which isn't feasible in standard CI.
3. **The issue/PR description is slightly mis-rooted.** The "server rejects occluded top face" explanation isn't what happens on stock servers; the real trigger is face/look-ray anti-cheat validation. Worth a note on the PR so future readers aren't misled.

## Comparison with the original PR

| Aspect | PR #3852 (heuristic) | This implementation (raycast) |
|--------|----------------------|-------------------------------|
| Face selection | dominant-axis heuristic | server raytrace (heuristic only as fallback) |
| Cursor | left at block center (inconsistent) | on the chosen face (`hit.intersect`) |
| lookAt | block center | actual click point |
| Anti-cheat robustness | works if heuristic face == look-ray face | always consistent by construction |
| Docs updated | no | yes |
| Tests | face direction only | + cursor-on-face + real door open/close |

Both fix the reported case on anti-cheat servers (because both make the face match the look ray). This implementation additionally makes the cursor and look point consistent and documents the change.

## Recommendation

- **Merge the raycast version** (this branch) over the heuristic-only PR, or ask the PR author to fold in raycast + cursor + docs. It's only modestly larger and reuses the established `bot.dig(..., 'raycast')` pattern.
- **Add a note to the PR/issue** correcting the root cause (anti-cheat face validation, not vanilla occlusion) and stating that the fix is verified to not regress stock servers but the original failure requires an anti-cheat plugin to observe.
- **Don't rely on the door test as a CI regression guard;** keep it as an integration check and lean on the internal face/cursor tests.

## How to apply / reproduce

```bash
# code (local branch, not pushed to PR)
cd mineflayer && git checkout fix/activateBlock-raycast-impl
# or apply the patch onto the PR branch
git apply implementation/phase1/pr_3852_fix.patch

# internal tests (no server needed)
npx mocha test/internalTest.js --grep "activateBlock face direction" --exit

# end-to-end A/B (needs Java; downloads a vanilla server via minecraft-wrap)
# script kept out of the repo; see report for the setup
```

## Open questions / follow-ups

- Confirm with the reporter which anti-cheat plugin was running, and ideally reproduce against it once to validate the fix end-to-end in the failing environment.
- Decide whether `activateItem` (PR #3695, related) should share the same raycast helper for consistency.
- The held-item behavior change (activating while holding a placeable item now targets the visible face, not the top) should be called out in the changelog.
