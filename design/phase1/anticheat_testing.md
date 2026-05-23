# Anti-cheat reproduction & testing for the activateBlock face bug

> Which anti-cheat reproduces mineflayer #3851, and how (or whether) to get that
> validation into our test setup.

- **Date:** 2026-05-23
- **Context:** Follow-up to the PR #3852 work — see
  [`pr_3852_review.md`](./pr_3852_review.md),
  [`pr_3852_fix_proposal.md`](./pr_3852_fix_proposal.md), and the
  [implementation report](../../implementation/phase1/pr_3852_implementation.md).
- **Artifacts:** [`FaceCheck` test plugin](../../implementation/phase1/facecheck-plugin/) (source + build).

## Why this investigation

The implementation report established that the #3851 bug — `activateBlock`'s old
`UP` default silently failing on 2-block-tall doors — **does not reproduce on
stock vanilla or Paper** (1.21.1 or 1.21.11): the door opens regardless of the
clicked face, because a right-click *interaction* is processed server-side
largely independent of the face. The failure only appears on a server that
**validates the interaction packet's face/cursor against the player's eye
raytrace** — i.e. an anti-cheat. This doc pins down exactly which check that is,
whether a real anti-cheat reproduces it, and how to test against it.

## The precise check that triggers the bug

A `block_place` (use-item-on) packet carries a `location`, a `direction` (face),
and a `cursorPos`. The bug condition is a server that requires:

> the packet's claimed **face** (and cursor) to match the face the server gets by
> ray-tracing from the player's eyes along their look direction.

mineflayer's old default sent `direction = UP` while `lookAt` aimed at the block
**center** — so the eye ray hits a **side** face, not the top. Claimed `UP` ≠
ray-traced side face → the strict server drops the interaction. The PR #3852
heuristic and our raycast implementation both make the face match the look ray,
so they pass.

## Candidate real anti-cheats (investigation + results)

All tested on Paper 1.21.1, offline-mode, non-opped survival bot (so it can't
bypass checks via op permissions), door placed via server console.

### NoCheatPlus — exact check, but doesn't run on modern MC
NCP is the textbook match: its `checks.blockinteract.direction` *"forces players
to look at the block they want to interact with"* and `blockinteract.visible`
ray-traces line-of-sight; both fire on the interact event and **cancel** it (=
silent failure, matching #3851). The original NCP is abandoned; the maintained
fork **[Updated-NoCheatPlus](https://github.com/Updated-NoCheatPlus/NoCheatPlus)**
claims 1.5–1.21.

- **Result:** the latest build (v1.5) **fails to initialize on 1.21.1** —
  `NullPointerException: Material not present: long_grass, grass` (old material
  names). It never loaded, so it couldn't reject anything.
- Even if it loaded, its `direction` check validates "looking at the block," not
  the specific *face* — so it may not catch a center-look + UP-face click anyway.

### Grim — modern & loads, but doesn't reject this by default
[Grim](https://github.com/GrimAnticheat/Grim) (2.3.74) supports 1.8–26.1, loads
cleanly on Paper 1.21.1, works offline. It's prediction/movement-focused; its
interaction face validation (the "LineOfSightPlace"-style check) is not enabled
to reject this by default.

- **Result:** Grim loaded fine but **did not reject the UP-face interaction** —
  both the old default and the fix opened the door, no flags. Catching this would
  require digging into Grim's config and likely still wouldn't cancel the
  interaction deterministically.

### Paid anti-cheats (Spartan, Vulcan, Matrix, Polar, …)
Closed-source / paid — unusable in an open-source CI and not investigated.

### Summary table

| Server / plugin | Loads on 1.21.1 | Rejects old UP default | Allows the fix |
|---|---|---|---|
| Vanilla | — | ❌ no (opens) | ✅ |
| Paper (stock) | — | ❌ no (opens) | ✅ |
| Paper + Grim 2.3.74 (default) | ✅ | ❌ no (opens) | ✅ |
| Paper + Updated-NoCheatPlus v1.5 | ❌ crashes | n/a | n/a |
| **Paper + FaceCheck (custom)** | ✅ | ✅ **cancels, door stays shut** | ✅ opens |

**Conclusion:** no free, off-the-shelf anti-cheat reproduces this on modern
Minecraft out of the box — they either don't run (NCP) or don't reject it by
default (Grim). A purpose-built check does, deterministically.

## Recommended: a minimal custom validator plugin

Rather than wrangle a heavyweight, version-fragile, config-dependent anti-cheat,
encode the exact check in a ~40-line Paper plugin. It cancels a right-click whose
claimed face doesn't match the eye raytrace — precisely the #3851 trigger. Source
and build steps are in [`facecheck-plugin/`](../../implementation/phase1/facecheck-plugin/).

```java
@EventHandler
public void onInteract(PlayerInteractEvent e) {
    if (e.getAction() != Action.RIGHT_CLICK_BLOCK) return;
    Block clicked = e.getClickedBlock();
    if (clicked == null) return;
    BlockFace claimed = e.getBlockFace();
    RayTraceResult ray = e.getPlayer().rayTraceBlocks(6.0);
    Block hit = ray == null ? null : ray.getHitBlock();
    boolean ok = hit != null
            && hit.getX() == clicked.getX() && hit.getY() == clicked.getY() && hit.getZ() == clicked.getZ()
            && ray.getHitBlockFace() == claimed;
    if (!ok) e.setCancelled(true); // = #3851 silent failure
}
```

**Verified (Paper 1.21.1, offline):**
```
[A] explicit UP : open false -> false   FaceCheck: CANCELLED ... claimed face UP but eye-raytrace hit ... WEST
[B] auto-detect : open false -> true    FaceCheck: ALLOWED  ... face WEST
```

Pros: deterministic, version-stable, free, tiny, offline-friendly, cancels (no
flaky kick thresholds). Cons: it's our own check, not a literal third-party
anti-cheat — but it implements the same validation, and the point is to guard the
client behavior, not to test a specific vendor.

## Getting it into the test setup — options

The existing external-test harness boots **vanilla** servers via
`minecraft-wrap`. Any anti-cheat-style test needs **Paper** plus a plugin, which
is a different setup. Three tiers, cheapest first:

### Tier 1 (recommended default) — no server at all
The real invariant is *"the claimed face/cursor match the bot's own eye→block
raytrace."* That is fully checkable **client-side, deterministically, with no
server**, and the internal tests already assert face + cursor-on-face. This is
the de-facto anti-cheat guard and already runs in CI for free. **Keep/strengthen
this as the primary regression guard.**

### Tier 2 (optional integration job) — Paper + FaceCheck
A separate, non-matrix CI job (or a documented local script) that:
1. Downloads a Paper jar (+ extracts API once) and builds `facecheck.jar`.
2. Boots Paper offline with the plugin in `plugins/`.
3. Connects a non-opped bot, places a 2-tall door via console, and asserts the
   old UP face is cancelled while the auto-detected face opens the door.

This is the only tier that proves real end-to-end server acceptance under strict
validation. Cost: Paper boot (~30–60s) + a Java build step; heavier and Paper-
only, so it shouldn't run per-version in the main matrix.

### Tier 3 (manual / occasional) — real anti-cheat
Spin up Paper + Grim (configured) or a working NCP build to sanity-check against
a real product. Not worth automating given the fragility found above; useful as a
one-off when validating a specific user's failing environment.

## Recommendation

1. **Primary guard: Tier 1** — assert face/cursor-vs-eye-raytrace consistency in
   the internal tests (no server). This already exists for the raycast PR and is
   the cheapest, most reliable signal.
2. **Add Tier 2 as an optional/manual integration test** using the committed
   `FaceCheck` plugin, for true end-to-end confidence. Don't gate the main matrix
   on it.
3. **Skip real anti-cheats for automation** — Grim doesn't reject it by default;
   the maintained NCP build doesn't run on 1.21.1. Keep Tier 3 as a manual check.
4. When confirming a specific user report, reproduce with FaceCheck (or their
   actual anti-cheat) rather than assuming vanilla behavior.

## Open questions / follow-ups
- Identify the exact anti-cheat the #3851 reporter ran (their "Paper offline-mode"
  server) to confirm FaceCheck mirrors it.
- If Tier 2 is adopted: decide whether to build the plugin in CI vs commit a
  prebuilt jar (prefer building — avoid committing binaries).
- Consider whether `activateItem`/`placeBlock` paths warrant the same end-to-end
  check.
