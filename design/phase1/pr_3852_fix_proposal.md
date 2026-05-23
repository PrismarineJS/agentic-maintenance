# Fix proposal — mineflayer PR #3852

> How to bring *fix: auto-detect activateBlock face direction from bot position*
> to a mergeable state.

- **Date:** 2026-05-23
- **PR:** [PrismarineJS/mineflayer#3852](https://github.com/PrismarineJS/mineflayer/pull/3852) · fixes [#3851](https://github.com/PrismarineJS/mineflayer/issues/3851)
- **Companion doc:** [`pr_3852_review.md`](./pr_3852_review.md)

## Goal

Address the blocking items from the review while keeping the PR's good core idea:

1. Docs no longer match the changed default. *(blocking)*
2. `direction` and `cursorPos` are geometrically inconsistent. *(design gap)*
3. The dominant-axis heuristic can disagree with what the **server** actually ray-traces. *(robustness)*

## Root cause (why this guides the fix)

The UP default doesn't fail for tall blocks because "the API picked a bad number" — it fails because the **server ray-traces the interaction** and rejects a click whose face/cursor don't match a surface it can actually reach. For `bamboo_door`, the top face of the lower half is occluded by the upper half, so the server's trace lands elsewhere → mismatch → silently dropped.

That means the most reliable fix is to **reproduce the server's ray-trace on the client**: send the face and cursor that a real ray from the bot's eyes would produce. mineflayer already does exactly this for digging.

## Prior art in the codebase

`bot.dig(block, forceLook, 'raycast')` already implements eye→block raycasting to pick a server-acceptable face — documented as *"raycast checks if there is a face visible by the bot and mines that face. Useful for servers with anti cheat."*

- `lib/plugins/digging.js:48-110` — the `digFace === 'raycast'` branch: enumerate candidate faces from eye-position deltas, raycast each, validate the hit is the target block, pick the closest, then use `rayBlock.face` and `rayBlock.intersect`.
- `lib/plugins/blocks.js:229-240` — `canSeeBlock` shows the `bot.world.raycast(headPos, dir, range, match)` call and that the result carries `.intersect` (world-space hit point) and `.face`.

The raycast result gives us **both** the face *and* the exact hit point — solving issues #2 and #3 in one shot.

---

## Recommended fix — raycast primary, heuristic fallback

Keep the PR's heuristic as a *fallback* (so behavior never regresses to "throw / send nothing" when the block isn't visible), but make raycast the primary path. This is one cohesive design that mirrors `dig`.

### `lib/plugins/inventory.js` — `activateBlock`

```js
// face index (matches both prismarine raycast .face and the block_place
// `direction` field): 0=down -Y, 1=up +Y, 2=north -Z, 3=south +Z, 4=west -X, 5=east +X
const FACE_VECTORS = [
  new Vec3(0, -1, 0), new Vec3(0, 1, 0),
  new Vec3(0, 0, -1), new Vec3(0, 0, 1),
  new Vec3(-1, 0, 0), new Vec3(1, 0, 0)
]

// Reproduce the server ray-trace: returns { direction, cursorPos } on the
// visible face, or null if the block can't be seen from the bot's eyes.
function raycastInteractFace (block) {
  const eye = bot.entity.position.offset(0, bot.entity.eyeHeight, 0)
  const center = block.position.offset(0.5, 0.5, 0.5)
  // range = actual distance (+ margin) so we always reach the intended block,
  // while the hit-is-target check below still rejects occluded clicks.
  const range = eye.distanceTo(center) + 0.5
  const hit = bot.world.raycast(eye, center.minus(eye).normalize(), range)
  if (!hit || !hit.position.equals(block.position)) return null
  return {
    direction: FACE_VECTORS[hit.face],
    cursorPos: hit.intersect.minus(block.position) // block-relative [0,1]
  }
}

async function activateBlock (block, direction, cursorPos) {
  if (direction == null) {
    const hit = raycastInteractFace(block)
    if (hit) {
      direction = hit.direction
      cursorPos = cursorPos ?? hit.cursorPos        // keep explicit cursorPos if given
    } else {
      direction = approachFaceHeuristic(block)      // the PR's existing dominant-axis logic
    }
  }
  const directionNum = vectorToDirection(direction)
  cursorPos = cursorPos ?? new Vec3(0.5, 0.5, 0.5)
  // look at the actual click point (not block center) so look ⇄ face ⇄ cursor agree
  await bot.lookAt(block.position.plus(cursorPos), false)
  // ... existing block_place packet writing unchanged ...
}
```

`approachFaceHeuristic` is just the PR's current dominant-axis code lifted into a helper.

### Why this resolves each issue

- **#2 cursorPos consistency** — `hit.intersect` is the exact point on the chosen face; the packet's face, cursor, and `lookAt` now describe the same point.
- **#3 robustness / anti-cheat** — the face is what the server's own trace would hit; occluded faces are rejected client-side by the `hit.position.equals(block.position)` check, so we never send a face the server will drop.
- **#3851 (bamboo_door)** — raycasting the door's real collision shape yields the visible side face + matching cursor → accepted.
- **No regression** — explicit-`direction` callers skip the block entirely; explicit-`cursorPos` callers are still honored; if the block isn't visible we fall back to the old heuristic (still always sends a packet).

### Things to verify during implementation

- **Face-enum match.** Confirm prismarine `raycast().face` uses the same 0–5 numbering as the `block_place` `direction` field. Evidence it does: `dig` assigns `bot.targetDigFace = rayBlock.face` directly. The `FACE_VECTORS` table above is ordered to that convention and round-trips through the existing `vectorToDirection`; if the enum differs, fix the table only.
- **Range.** Using distance-derived range (not `dig`'s hardcoded `5`) matters: e.g. a bot directly above a block can sit >5 blocks from the top face at eye height and a fixed `5` would miss it.
- **Block shapes loaded.** raycast needs the block's bounding shapes; fine in normal play and in the internal test (chunk is built before activating).

---

## Alternative — minimal fix (if maintainers prefer to keep it tiny)

If the team wants the smallest possible diff over the current PR, keep the heuristic and only make it self-consistent + documented:

```js
// after the existing dominant-axis block produces `direction`:
cursorPos = cursorPos ?? new Vec3(0.5, 0.5, 0.5).add(direction.scaled(0.5))
await bot.lookAt(block.position.plus(cursorPos), false)
```

This snaps the cursor onto the chosen face (e.g. east → `(1, 0.5, 0.5)`) and aims `lookAt` there. It fixes #1 (with docs) and #2, but **not** #3 — a pure heuristic can still pick a face the server's trace disagrees with for occluded or oddly-shaped blocks. Acceptable as a first step; raycast as a follow-up.

**Recommendation:** ship the raycast version. It's only modestly larger, fixes the root cause, and reuses an established, anti-cheat-friendly pattern.

---

## Docs changes (required either way)

`docs/api.md` (~line 1965) currently reads:
> `direction` Optional defaults to `new Vec3(0, 1, 0)` (up).

Replace with something like:
> `direction` Optional. If omitted, mineflayer raycasts from the bot's eyes to choose the face the bot can actually see (falling back to the nearest face by bot position when the block isn't visible), and sets a matching `cursorPos`. Pass an explicit `Vec3` to force a specific face. *(Previously defaulted to `new Vec3(0, 1, 0)` / up.)*

Also fix the existing `cursorPos` line typo ("curos position") and note it now defaults to the raycast hit point when `direction` is auto-detected.

## Test plan

- **Keep** the PR's internal tests (`test/internalTest.js`) — they assert the per-position face from the emitted `block_place` packet, and the raycast path produces the same intuitive faces for the 6 cardinal positions, so they become a useful cross-check. Re-run to confirm the distance-based range keeps the above/below (UP/DOWN) cases passing.
- **Strengthen** the external test (`test/externalTests/activateBlockFace.js`): in addition to asserting packet direction, add a case that `/setblock`s a real **2-tall `bamboo_door`**, calls `bot.activateBlock(lowerHalf)` with no direction, and asserts the block's `open` property flips — this directly guards the #3851 regression rather than just the mechanism.
- **Add** a `cursorPos`-consistency assertion: the captured `cursorX/Y/Z` should lie on the reported face (e.g. east ⇒ cursorX ≈ 1.0).

## Backward-compatibility notes (for the PR description / changelog)

- Calls passing an explicit `direction` are unchanged.
- Calls relying on the default now interact with the bot-facing/visible face instead of the top. For pure interactions (doors, buttons, chests) the server ignores the face, so behavior is unchanged in practice; the visible difference is for **`activateBlock` while holding a placeable item**, where a held block would now be placed on the facing side rather than on top. `placeBlock` remains the intended placement API; call out this nuance.

## Checklist (maps to review findings)

| Review item | Addressed by |
|-------------|--------------|
| 1. Docs wrong | Docs rewrite above *(blocking)* |
| 2. direction/cursorPos inconsistent | `cursorPos = hit.intersect - block.position` + `lookAt` hit point |
| 3. heuristic vs raycast | raycast primary, heuristic fallback |
| 4. held-item behavior change | documented in changelog/notes |
| 5. external test gap | real bamboo_door open-state test + cursor assertion |

## Effort & risk

- **Effort:** ~30–40 lines in `inventory.js` (most of it the helper), a docs paragraph, and ~1 external test case. Roughly a half-day including a real-server check.
- **Risk:** low–medium. Main risk is the face-enum assumption and raycast edge cases (occlusion, range) — both bounded by the heuristic fallback and the existing test matrix.
- **Sequencing option:** land the minimal Option A now to unblock the bug, file a follow-up for the raycast upgrade — or do raycast directly. Prefer raycast directly given the prior art already exists.
