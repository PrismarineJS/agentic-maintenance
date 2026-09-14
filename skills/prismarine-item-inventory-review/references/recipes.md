# Source map and regression recipes

These are 2026-09-14 verified engineering examples, with pending-branch APIs identified explicitly. Recent Astra findings are not manual maintainer policy. [Rereviews](../../../implementation/phase3/u9g_rereviews.json), [independent checks](../../../implementation/phase3/u9g_independent_checks.json) and [historical cases](../../../implementation/phase3/review_cases.jsonl) preserve the actual dependencies, revisions and inspection limits.

## Item/text models

Sources: [#188 index.js](https://github.com/PrismarineJS/prismarine-item/blob/45fd22d6348da326887bdc11e8f3ea4c459b467c/index.js), [#189 index.js](https://github.com/PrismarineJS/prismarine-item/blob/7cb3fc659f6e8565dcc09e7dd0a3ffae8936aa2a/index.js). Existing tests are `test/basic.test.js`; #188 also adds `test/displayName.test.js`.

Construct a 1.21.4 registry, its Item factory, `prismarine-nbt` and `prismarine-chat` factories. Feed `Item.fromNotch` an item with `itemCount: 1`, a valid `itemId`, `removeComponents: []`, and `components: [{ type: 'custom_name', data }]`.

- `data = nbt.comp({ translate: nbt.string('item.minecraft.diamond_sword') })`: the matching Chat renderer yields `Diamond Sword`; #188 produces empty display text.
- Set a new item's `customName` to `Shop`, then `null`; inspect fallback display name and serialize it. #188 retains `Shop` as display text. Keep display-state and serialization assertions separate.
- `data = nbt.string('{"text":"Hello"}')`: compare `Chat.fromNotch(data).toString()` with the getter's representation passed to Chat. #189 changes the literal characters into rendered `Hello`.
- Ordinary literal text and an NBT compound with a `text` field are controls. Compare pre-component versions using their actual NBT format rather than assuming all legacy versions require identical lore shapes.

The full suites passed 114 tests (#188) and 111 (#189) despite these focused failures. Existing setter/map-array synchronization problems predate the getter-only #189 diff.

## Hashed click integration

Candidate sources: [item #184](https://github.com/PrismarineJS/prismarine-item/tree/0e154a4f48a65f8364c57a691d755064b68f24c4), [Mineflayer #4027 inventory.js](https://github.com/PrismarineJS/mineflayer/blob/63bada466843c3eb701827518a6918ddc4a98afd/lib/plugins/inventory.js), [node-protodef #177](https://github.com/ProtoDef-io/node-protodef/tree/dde6ce755124e8f42b4fc1e53ce2d84c73acdb09), [ProtoDef #65](https://github.com/ProtoDef-io/ProtoDef/tree/a2b1cd2d84488012b7949fbe578d3781cc3329a4).

Use `test/hashedSlot.test.js` and `test/hashedSlot.vectors.json` at the candidate item head. Replay every frozen component vector on the actual candidate dependency: the recorded result was 89 matching and 12 failing from the existing anonymous-body integration issue. Damage-only success cannot validate all component shapes. Inspect `test/e2e/hashedSlot.js` and its version list when live claim/reconciliation behavior is at issue; the rereview did not execute that server test.

Through the actual inventory plugin and real window model, pick up a damaged sword, invoke `_syncWindow`, then place it. Compile/serialize/decode all three packets on 1.21.4, 1.21.5 and 1.21.11. The coordinated candidate stack passed nine packets: full damage components on 1.21.4, signed damage hash `-499649379` on the newer versions, and correct empty slot/cursor optionality. Those tests deliberately supplied all four candidate revisions; they do not prove that released item 1.18.0 provides `toHashedNotch`.

## Inventory re-entry and crafting

[Mineflayer #4103 inventory.js](https://github.com/PrismarineJS/mineflayer/blob/5d4dab47f3bfe1f414222cd6c1d39b8b234c6107/lib/plugins/inventory.js) provides concrete map/buffer ownership. In `test/internalTest.js`, open a container with a distinct state ID, update window 0, then click the container and inspect its outgoing ID and cursor. Close it, deliver a trailing player-region slot update, respawn and reopen the same ID with early `window_items`. Assert current inventory contents, one open event, consumed buffer and new ID state. `closeWindow(null)` and no-open-window relogin are controls. The recorded real-model checks passed; these scenarios are not evidence of an outstanding defect at that head.

`_syncWindow` subscribes before a no-op drag-end click (`stateId: -1`, `slot: -999`, `mouseButton: 2`, `mode: 5`, no changed slots) to solicit a full authoritative response on state-ID versions. Its cursor converter must match the click protocol. Trace pending waits if the window closes or is replaced before the reply.

[Data #1283](https://github.com/PrismarineJS/minecraft-data/pull/1283) and [generator #81](https://github.com/PrismarineJS/minecraft-data-generator/pull/81): construct real prismarine-recipe objects from candidate 1.10/1.11/1.12 outputs. Cake needs three bucket entries in `outShape` and positive bucket deltas. Those candidate outputs instead had `outShape: null`; Mineflayer `craft.js` consequently skips remainder collection. Mixed plank metadata and pickaxe orientation passed; an absent 1.11 registry item also occurred at base. This tests published output consumption, not Java regeneration or live crafting.
