# FaceCheck — minimal interaction-face validator (test plugin)

A ~40-line Paper/Bukkit plugin that reproduces the strict server-side check
behind mineflayer issue #3851: on a right-click interaction it raytraces from
the player's eyes and **cancels** the interaction if the claimed (packet)
block+face doesn't match what the player is actually looking at.

This is a deterministic, version-stable stand-in for a real anti-cheat (see
[`../../../design/phase1/anticheat_testing.md`](../../../design/phase1/anticheat_testing.md)
for why we don't just use Grim/NoCheatPlus).

## Files
- `src/com/example/FaceCheckPlugin.java` — the plugin
- `plugin.yml` — Bukkit plugin descriptor

## Build (no Maven/Gradle needed)

Compile against a Paper server's bundled API. Extract it once with paperclip's
patch-only mode, then `javac` + `jar`:

```bash
PAPER=paper-1.21.1.jar          # any modern Paper jar
mkdir extract && cd extract && echo "eula=true" > eula.txt
java -Dpaperclip.patchonly=true -jar ../$PAPER     # extracts versions/ + libraries/
cd ..
CP="extract/versions/1.21.1/paper-1.21.1.jar:$(find extract/libraries -name '*.jar' | tr '\n' ':')"
mkdir -p out && javac --release 21 -cp "$CP" -d out src/com/example/FaceCheckPlugin.java
cp plugin.yml out/ && (cd out && jar cf ../facecheck.jar .)
```

Drop `facecheck.jar` into the server's `plugins/` folder. Works in offline mode.

## Verified behavior (Paper 1.21.1, offline, non-opped survival bot)

| Call | Packet face | Result |
|------|-------------|--------|
| `activateBlock(door, Vec3(0,1,0))` (old UP default) | UP | **cancelled** — door stays shut (`claimed face UP but eye-raytrace hit ... WEST`) |
| `activateBlock(door)` (raycast auto-detect) | WEST | **allowed** — door opens |
