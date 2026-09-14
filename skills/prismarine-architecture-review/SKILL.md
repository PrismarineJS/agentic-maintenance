---
name: prismarine-architecture-review
description: Review PrismarineJS package ownership, shared state and data contracts, dependency integration, and the scope of necessary refactoring. Use for cross-package changes or changes to reusable models and public boundaries; distinguish a sound local fix from work that needs a coordinated design.
---

# PrismarineJS architecture review

Start with the concrete user behavior and trace its data, state, and consumers through the current implementation. Independent packages are intentional ([contribute15](https://github.com/PrismarineJS/prismarine-contribute/issues/15#issuecomment-1575661657)); their existence does not imply every helper deserves extraction. Treat the rules below as scoped review aids grounded in attributed discussions, with manual authorship generally undisclosed.

## Map responsibility before moving code

Use this map as a hypothesis to verify against actual callers:

- `minecraft-data` owns shared language-independent schemas and extracted facts; `node-minecraft-data` exposes them to Node consumers; generators own repeatable extraction.
- ProtoDef owns generic serialization machinery; `node-minecraft-protocol` owns Minecraft transport, protocol phases, and generic client/server packet mechanics.
- Registry/world/chunk/entity/item/physics packages own reusable state or domain models; Mineflayer and flying-squid adapt them into bot/server behavior. Viewer and pathfinder consume those models.

For a proposed move, identify inputs, outputs, mutable state, lifetime, and at least one actual consumer. A helper still coupled to bot state may belong in its plugin. A generic handshake fix may belong in protocol even when discovered in Mineflayer ([mineflayer3794](https://github.com/PrismarineJS/mineflayer/pull/3794#issuecomment-3695018711)). A chunk's coordinate convention must remain useful to every provider, not become global because one caller prefers it ([chunk241](https://github.com/PrismarineJS/prismarine-chunk/pull/241#issuecomment-2171893140)). Name the violated boundary before recommending a package change.

## Follow identity, representation, and updates

**A shared owner must receive every relevant update.** Trace construction, copies, transport between workers, resets, and reconnects. Replacing a data loader with a fresh registry does not propagate dynamic state: [viewer307](https://github.com/PrismarineJS/prismarine-viewer/pull/307#discussion_r995182554) exposes that failure, and [rom's follow-up](https://github.com/PrismarineJS/prismarine-viewer/pull/307#discussion_r996179349) calls for update propagation. A world integration that keeps shadow entity stores needs a coherent access/update path ([mineflayer3737](https://github.com/PrismarineJS/mineflayer/pull/3737#discussion_r2328984434)). Do not infer that an unrelated entity fix requires completing the whole world roadmap.

**Repair the producer when consumers share the same defect.** Trace all users of a derived value before adding another call-site shim. [Protocol1442](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1442#discussion_r2726213801) misses ordinary chat by fixing only command checksums. Generated output repairs need corresponding producer changes so regeneration preserves them ([minecraft-data1193](https://github.com/PrismarineJS/minecraft-data/pull/1193#issuecomment-4533234380)). First establish that the affected artifact is still produced by that generator: [minecraft-data1049](https://github.com/PrismarineJS/minecraft-data/pull/1049#issuecomment-3169607917) withdraws the generator requirement for a historical correction. Shared names can simplify consumers, but preserve wire widths, ordinals, actual version boundaries, and deliberately supported unknown values.

**Separate semantic state from its wire representation.** Identify effective values/defaults, network deltas, and public objects before merging them into one abstraction. Distinguish a codec error from an optional application policy. Do not turn strictness into a universal architecture rule: after [ProtoDef176](https://github.com/ProtoDef-io/node-protodef/pull/176#issuecomment-5651567589) merged, extremeheat objected to rejecting raw integer enums needed by proxy re-encoding while agreeing invalid symbolic strings should throw. Preserve this disagreement and test the specific read/write contract.

**Generic extensions should use the existing extension contract.** For compiler work, check dependency direction and normal type/context hooks before adding datatype-specific precompile injection; [ProtoDef177](https://github.com/ProtoDef-io/node-protodef/pull/177#discussion_r3944863074) identifies that design problem. Verify the current revision because several original objections were subsequently fixed.

**Public boundaries need deliberate compatibility.** Check constructor/export shapes, event meaning, default precedence, and which layer controls an option. A new undocumented internal helper need not become public ([mineflayer2929](https://github.com/PrismarineJS/mineflayer/pull/2929#discussion_r1108945340)). A local type fix should mirror the runtime factory rather than redesign its exports. If two layers write the same settings, explain lifecycle ordering and override behavior rather than assuming one default always wins.

## Decide the necessary scope

Require broader changes when a demonstrated invariant crosses multiple paths and the local patch leaves that same failure reachable. [Mineflayer3722](https://github.com/PrismarineJS/mineflayer/pull/3722#issuecomment-3314997503) explicitly requires configuration-phase suppression beyond physics. State the remaining paths and the smallest shared boundary that covers them; do not merely say the code needs refactoring.

Accept a local fix when it satisfies its contract and the larger change is independent. [Item127](https://github.com/PrismarineJS/prismarine-item/pull/127#pullrequestreview-2686529666) approves component compatibility before a shared-data redesign; [protocol1309](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1309#issuecomment-2408710582) questions generic codec placement without blocking the integration. Roadmaps and preferred future ownership are not automatic prerequisites. Nor must a new optional generator implement every older version without a consumer ([generator24](https://github.com/PrismarineJS/minecraft-data-generator/pull/24#issuecomment-2241091912)). Preserve existing support while scoping genuinely new capability.

When a change spans packages, identify candidate dependency revisions, the downstream path that exercises them, and the released minimum needed for landing ([mineflayer3384](https://github.com/PrismarineJS/mineflayer/pull/3384#issuecomment-2156699400)). Temporary branch pins can demonstrate integration; a successful isolated test or version-list edit does not establish the chain.

Return a concrete ownership finding, a bounded design requirement, an optional follow-up, or no finding. Explain the affected consumer and validation that would settle the concern. Keep discussion chronology: an initial objection may be corrected, an approved fix may retain architecture debt, and a merged PR may receive a later substantive objection. This skill grants no publication permission.
