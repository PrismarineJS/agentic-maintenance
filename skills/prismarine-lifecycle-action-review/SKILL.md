---
name: prismarine-lifecycle-action-review
description: Review Mineflayer and node-minecraft-protocol login, configuration, respawn, transfer, input and action lifecycles. Use for settings synchronization, queued replies, prediction sequencing, cancellation and action completion; route geometric reach calculations to the geometry skill.
---

# Lifecycle and action review

Trace the affected operation through transport state, bot state and server observation. Mineflayer's `login`, `spawn`, `respawn`, `physicsTick` and NMP's packet events describe different readiness boundaries. A transition back to `play` does not establish that the entity, position and chunks needed by an action are initialized.

## Locate the owners

These are repository-relative navigation points, verified against the [dated source map and recipes](references/recipes.md); recheck at the reviewed revision. Branch additions below are examples, not promises about released APIs.

| Owner | Entry points and contract |
| --- | --- |
| NMP protocol state | `src/client/play.js`: `onLogin`, `enterConfigState`; `src/client.js`: serializer follows `client.state`. |
| Mineflayer settings | `lib/plugins/settings.js`: `setSettings`, `bot.settings`; #4065 adds `clientInformation` and passes `options.clientSettings` to NMP. |
| Movement/input lifetime | `lib/plugins/physics.js`: `tickPhysics`, `shouldUsePhysics`, control state, sent-state caches, position handler, timers and `cleanup`. |
| Actions | `inventory.js`: activation/release; `generic_place.js` and `place_entity.js`: placement; `digging.js`: task, block listener and cancellation; all under `lib/plugins/`. |

On configuration-capable versions, NMP acknowledges login, enters configuration, writes settings and returns to play through `finish_configuration`. A transfer sends `configuration_acknowledged` before changing state. Configuration settings and resource-pack responses are legitimate writes there; play movement, digging and inventory packets need their own readiness policy. A physics-only gate cannot establish safety for direct action calls. Preserve each action's documented reject/wait behavior rather than silently swallowing it. [Historical scope discussion](https://github.com/PrismarineJS/mineflayer/pull/3722#issuecomment-3209989774).

## Check reset ownership across re-entry

**Settings:** follow the live `bot.settings`, its serialized fields, and NMP's `options.clientSettings`. In #4065, the options value is a one-time object snapshot while `setSettings` changes the bot and immediately writes a new packet. Initial configuration → change view distance in play → configuration again can send `12, 8, 12`. Test the updated value on re-entry and explicit caller overrides; one correct initial packet does not establish synchronization. Keep the actual option defaults and field conversion in the trace.

**Inputs:** distinguish held user controls from the server's last acknowledged/sent state. #4063's `lastSentInputs`, `lastSentSneak` and `lastSentSprinting` suppress duplicate writes; inspect what resets them when a server-side player/session is replaced. Resetting a sent cache and clearing a held key have different effects. Check one held-input transfer/respawn followed by the same input, plus ordinary repeated ticks. `player_input` shift support and legacy `entity_action` sneaking differ across versions; `supportFeature('sneakUsesEntityAction')` was absent from allowed minecraft-data 3.114.0 and 3.116.0 in the dated validation. A merged data PR did not make the gate usable in those releases.

**Queued replies:** #4107's `pendingReplies`, `flushReplies`, `_replyOnNextTick` and fallback timer belong to a play-session/world lifetime; ping and teleport replies can share order. A state guard that returns without clearing a queue can replay old relative coordinates after transfer. Trace enqueue → login/respawn/configuration/end → drain, including work enqueued during a drain. Separately, #4099's delayed `respawnReply` has `cancelRespawnReply`; verify cancellation on a newer teleport and session exit. Do not assume those independently reviewed PRs are combined.

## Prediction and completion

For sequence-bearing use, placement and dig start/finish, follow one shared producer across plugins. #4085 introduces `sequence.js`/`bot._nextSequence`; interleave activation, generic placement and digging, and include entity placement/boats because they have separate send paths. Do not demand a new sequence on every packet: the reviewed release-use and dig-abort paths deliberately send zero. Confirm the target version's packet fields and feature availability with its real compiled NMP serializer.

Inspect synchronous event re-entry before changing cleanup: in #4094 an instant `diggingCompleted` handler can start a successor dig before the old call unwinds. Calling `stopDigging` must cancel that successor and remove its listener, without an older abort closure replacing its owner. Count the per-position `blockUpdate` listeners and observe promise settlement, not only `targetDigBlock`.

For asynchronous packet/event handlers, identify who consumes the returned promise: an EventEmitter callback returning a rejection is different from an awaited action rejecting to its caller. Trace the returned promise and any separate cleanup chain before alleging swallowed errors; the latter distinction caused a [withdrawn objection in Mineflayer #2833](https://github.com/PrismarineJS/mineflayer/pull/2833#discussion_r1027027866).

Choose the observation matching the claim. `usingHeldItem`, a swing or an encoded `use_item` proves local/packet behavior; activation success needs the resulting server block, entity or inventory change. Mineflayer already has `test/internalTest.js` (or the internalTests split at the candidate head) for real NMP client/server traces and `test/externalTests/activateItem.js`, `consume.js`, `placeBlock.js`, `placeEntity.js` for actions. Prefer that real bot/client fixture for packet-driven plugin behavior over rebuilding bot initialization with EventEmitters and stubbed writes. This exercises schema selection, injection and lifecycle together. Pure model tests and controlled fault-isolation probes remain useful, but do not replace an applicable maintainer request for integration coverage. Follow the [test-selection rules](../prismarine-protocol-data-review/references/packet_tests.md).

Build valid solid-target/load/reach preconditions and await the relevant update; `await bot.chat(...)` does not synchronize a server command. Existing model/codec evidence can suffice for a bounded change; require live server evidence for a claim that the local fixture cannot establish, not indiscriminately. [Server-observed activation precedent](https://github.com/PrismarineJS/mineflayer/pull/3743#discussion_r2365596080).
