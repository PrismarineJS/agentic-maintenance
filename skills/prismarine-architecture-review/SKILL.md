---
name: prismarine-architecture-review
description: Review PrismarineJS package boundaries, shared model ownership, CommonJS factories, declarations and domain abstractions. Use for cross-package refactoring, public API changes or duplicated protocol/model logic.
---

# Package architecture and public APIs

PrismarineJS deliberately provides independent packages that bots, servers, proxies and viewers can reuse. Review whether the proposed code preserves that reuse; extraction by itself is not an improvement. The [contribute package map](https://github.com/PrismarineJS/prismarine-contribute/blob/4317c201c884148c6263de2bdf487f6b6396ef20/info.md) explains the organization, and [contribute #15](https://github.com/PrismarineJS/prismarine-contribute/issues/15#issuecomment-1575661657) explicitly defends independent packages.

## Locate the owner using the actual consumer chain

| Responsibility | Usual owner and boundary to inspect |
|---|---|
| Versioned facts, protocol schemas, features | `minecraft-data`; its Node loading, indexing and npm releases belong to `node-minecraft-data`. A bot-specific fallback must not silently become the shared fact. |
| Generic read/write/size/compiler machinery | `node-protodef`; Minecraft native wire types and connection phases live in `node-minecraft-protocol`. Inspect existing type/context extension hooks before injecting special cases into compilation. |
| Static data plus negotiated registry state | `prismarine-registry`; identify who receives registry packets and whether models use the same registry. Reconstructing from a version string loses session additions. |
| Column storage and world access | `prismarine-chunk` and `prismarine-world`; providers and renderers need compatible coordinates and updates. A provider-specific world-coordinate convention must not leak into chunk-local APIs. |
| Reusable stack, entity and physical state | `prismarine-item`, `prismarine-entity`, `prismarine-physics`; Mineflayer translates packets/actions into those models. Viewer and pathfinder are consumers, not alternate authoritative stores. |
| Server-side behavior and persistent state | `flying-squid` and its model/provider dependencies; a Mineflayer implementation is one consumer, not necessarily a reusable server contract. |

Treat this as a map to verify, not a mandatory extraction tree. For a proposed helper write its inputs, output, mutable owner and actual consumers. A helper requiring a bot, its pending action queue and packet writer can reasonably stay inside the relevant Mineflayer plugin. A decoder usable independently of a bot should not require constructing one.

## Shared state must remain shared after construction

Trace registry/world identity through factories, packet handlers, world replacements and worker messages. `prismarine-registry/lib/index.js` creates a registry from static data; its loader's shallow copy does not establish an independently synchronized session. Passing only `bot.version` into a renderer/model factory can create a different view of negotiated data. Passing a registry once also fails if later updates never reach it.

The shared-world direction in [Mineflayer #334](https://github.com/PrismarineJS/mineflayer/issues/334) is useful context. Apply it to a concrete duplication: shadow entity maps need one update/access path, and a worker needs a defined propagation mechanism. [Viewer #307](https://github.com/PrismarineJS/prismarine-viewer/pull/307#discussion_r995182554) and [Mineflayer #3737](https://github.com/PrismarineJS/mineflayer/pull/3737#discussion_r2328984434) show these concerns. An unrelated entity repair need not complete the roadmap.

## Review code quality through domain costs

Prefer a shared producer fix when the same derived value feeds several consumers. A command-only checksum repair misses ordinary chat if both use the broken producer ([NMP #1442](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1442#discussion_r2726213801)). Name the missed consumer before requesting refactoring.

For stack/component accessors, distinguish a stable object, a decoded copy and a live view. A getter that repeatedly decodes NBT/components can make edits disappear and add work on every inventory/render tick. Ask whether construction-time normalization or a clear mutation method matches actual updates; do not ban getters or caching categorically. [Item #110](https://github.com/PrismarineJS/prismarine-item/pull/110#issuecomment-1660498932) and [#126](https://github.com/PrismarineJS/prismarine-item/pull/126#issuecomment-2683151129) motivate this distinction.

Keep meaningful wire-version branches but factor repeated setup when it obscures their only difference. Label settings snapshots, requested input, sent input and acknowledged state by their roles; an ambiguous `_session` object can conceal which lifecycle owns it. Cleanup was requested but the bounded repair still approved in [NMP #1277](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1277#pullrequestreview-1799704432).

For codec/compiler abstraction changes, trace read/write/size and native/context registration together. Datatype-specific precompile injection can invert the extension contract ([ProtoDef #177](https://github.com/ProtoDef-io/node-protodef/pull/177#discussion_r3944863074)); check the final revision before repeating an earlier objection. Benchmark hot-path claims on equivalent packet workloads rather than counting lines.

## Match the usable API, including factory exports

Inspect `package.json` main/types and the real CommonJS factory before editing declarations. Many models export version/registry factories returning constructors; changing `module.exports` merely to export a TypeScript interface can break JavaScript consumers. Compile a minimal consumer against the PR's actual declarations, then instantiate the runtime export. Avoid accidentally resolving an installed release instead of the candidate.

For a new required host/adapter method, test an object that satisfies the declared interface and pass it to the runtime consumer. Viewer #511's new `Host.loadText` call was absent from the declared Host and `createNodeHost` return type: the compiler accepted a host that then failed at runtime. Public options/events also need declarations and usable documentation; internal `_` helpers need not be promoted to public API. See [concrete API checks](references/api_checks.md).

## Decide whether refactoring is required to land

Require a shared change only when the local patch leaves the same demonstrated invariant broken elsewhere: configuration suppression beyond physics in [Mineflayer #3722](https://github.com/PrismarineJS/mineflayer/pull/3722#issuecomment-3314997503) is one example. Name the remaining paths and the smallest shared owner that covers them.

A component compatibility repair could land before data redesign ([Item #127](https://github.com/PrismarineJS/prismarine-item/pull/127#pullrequestreview-2686529666)); generic codec placement could remain follow-up ([NMP #1309](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1309#issuecomment-2408710582)). For coordinated releases, exercise the candidate dependency through the downstream consumer and state the required released minimum ([Mineflayer #3384](https://github.com/PrismarineJS/mineflayer/pull/3384#issuecomment-2156699400)). A package move without that migration is incomplete.
