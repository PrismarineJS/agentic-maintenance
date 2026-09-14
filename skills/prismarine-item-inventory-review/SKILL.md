---
name: prismarine-item-inventory-review
description: Review PrismarineJS item models and Mineflayer inventory/crafting behavior across NBT, data components, text, hashed slots, window/cursor reconciliation and recipe remainders. Use for item representation or inventory state changes; route generic protocol generation to the protocol-data skill.
---

# Item and inventory review

Follow an item from the packet through `prismarine-item`, the window model, the changed operation and its outgoing representation. A correct getter or local click does not establish that the server receives the same item. Use the target registry/version; Java and Bedrock share model code but have different slot representations and stack-ID behavior.

## Representation boundaries

Start in prismarine-item `index.js`: `loader(registryOrVersion)`, `Item.fromNotch`, `Item.toNotch`, `customName`, `customLore`, `enchants` and `durabilityUsed`; inspect `index.d.ts` alongside runtime behavior. For Java before components, follow typed `nbt.value` and version-specific metadata/enchantment keys. With `itemsWithComponents` (1.20.5+), `components` and `removedComponents` are serialized arrays while `componentMap` supports lookup. `fromNotch` populates the map from the array. Updating only the map can change a getter without changing `toNotch`; determine whether the reviewed diff introduces that divergence or merely encounters an existing defect.

Distinguish three text contracts: typed NBT chat components, serialized JSON chat text and rendered display text. Legacy `display.Name`/`display.Lore` and modern `custom_name`/`lore` do not justify parsing every string as JSON. An NBT string containing `{"text":"Hello"}` can mean those literal characters; converting it to an unquoted JSON string lets a downstream chat parser render `Hello` instead. Test a translated component, styled text, a JSON-looking literal, and removal of a custom name. `prismarine-chat`'s `Chat.fromNotch(...).toString()` with the same registry provides a useful semantic comparison. In #188, translated names rendered empty and clearing a name retained stale `displayName`; #189 intentionally normalized getter return types, but lost the literal-string distinction. These are [dated examples](references/recipes.md), not a ban on normalization.

For computed item accessors, establish whether returned arrays/objects are live state or copies before recommending a mutation API. Re-read/serialize after editing and after clearing. [Item #110](https://github.com/PrismarineJS/prismarine-item/pull/110#issuecomment-1660498932) discusses this concrete confusion; [#127](https://github.com/PrismarineJS/prismarine-item/pull/127#pullrequestreview-2686529666) accepted component compatibility before a broader shared-data refactor.

## Full items versus hashed claims

The reviewed Mineflayer #4027 selects `Item.toHashedNotch` for 1.21.5+ state-ID clicks in `lib/plugins/inventory.js`; both `changedSlots[].item` and `cursorItem`, including `_syncWindow`, need the selected converter. Older action-ID and 1.17 branches retain full-item conversion. Inspect null slots: full component slots use an empty count object, while the candidate hashed converter returns `null` for the optional slot. Do not spread that conversion into unrelated full-item packets.

`toHashedNotch` is a **candidate API in item #184**; the verified allowed prismarine-item 1.18.0 lacks it. Its `lib/hashedSlot.js`, `hashedSlot.json` and `hashOps.js` convert network values to persistent codec form before CRC32C hashing: registry IDs may become names, nested text has typed boolean semantics, and defaults can disappear. Hashing raw packet bytes is a different contract. Inspect nonpersistent filtering, removed components and unsupported-component fallback separately. A deliberate zero-hash fallback requests server correction; a thrown hash conversion prevents the click entirely. Test against the actual ProtoDef dependency: a named-body-only implementation rejects anonymous bodies even when a simple damage component works. Coordinate candidate pins explicitly and report the released dependency prerequisite.

## Window, cursor and event lifetime

In Mineflayer `lib/plugins/inventory.js`, trace `clickWindow`, `confirmTransaction`, `prepareWindow`, `set_slot`, `window_items`, `closeWindow` and `_setSlot`. The `prismarine-windows` model owns `slots`, `selectedItem` (cursor), `acceptClick` and `updateSlot`; the plugin handles packet reconciliation. Older transactions acknowledge action IDs. Modern state IDs identify a particular window's last server state; a background player-inventory update must not replace an open container's state ID. A local accepted click and silence from modern servers do not prove server acceptance.

#4103's `stateIds`, `lastClosedWindow`, `windowItems` buffer and `_syncWindow` are branch-specific ownership examples. Exercise items arriving before open, close followed by trailing inventory updates, same-ID reopening after respawn, and relogin without `close_window`. Buffer consumption and slot-shape checks prevent stale contents being applied to a new window. Include authoritative `carriedItem`, and verify held-item events through direct `inventory.updateSlot` as well as packet entry. Newer `set_player_inventory` uses player indices: hotbar 0–8 maps to window slots 36–44, armor 36–39 maps to 8–5, offhand 40 to 45. Do not apply window indices directly.

## Crafting and regression selection

Follow minecraft-data recipes through prismarine-recipe `lib/recipe.js` (`outShape`, `computeDelta`) into Mineflayer `lib/plugins/craft.js`. Cake produces a cake **and three empty buckets**; missing `outShape` changes material accounting and bypasses remainder collection. Check metadata alternatives and mixed-plank recipes separately from dynamic recipes intentionally outside a generator's scope.

Use prismarine-item `test/basic.test.js` for representation contracts, Mineflayer `test/internalTest.js` for packet/model lifecycle, and existing `test/externalTests/heldItemChanged.js`, `playerInventory.js`, `crafting.js` when server observation is needed. The [focused recipes](references/recipes.md) give exact inputs and hash-vector harnesses. Existing model/codec evidence can be sufficient; require broader server evidence only for a claim those layers cannot establish.
