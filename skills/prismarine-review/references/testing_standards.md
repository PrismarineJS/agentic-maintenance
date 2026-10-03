# Submitted tests must fit the repository

Passing a regression test is not sufficient evidence of merge readiness. Inspect its setup, assertions, adjacent tests, package scripts and CI at the candidate revision. A real imported plugin, many version iterations, or a head/base failure comparison does not make a replacement bot fixture representative.

## Required review record

For each added or substantially changed test/fixture, establish:

1. **Claim and subject:** which production behavior is exercised, and how is the real subject constructed? Trace factories, plugin loading, dependency resolution and feature selection. Avoid accidentally testing an installed release instead of the candidate.
2. **Replaced boundaries:** enumerate substituted bot/client/world/control/clock/transport behavior, including overrides installed after setup. Is each a legitimate input to the algorithm, or does it replace the integration the test claims to cover? Being inside `internalTest.js` or initially calling `createBot` is not sufficient if the test then replaces the relevant production path. No-op packet writers and direct decoded-object emissions cannot establish codec or bot initialization behavior.
3. **Repository fit:** read the existing harness and shared version/edition matrices before accepting a new fixture or file. Name the existing location that should own the regression when requesting a move. Explain the maintenance or coverage consequence, not merely a stylistic preference.
4. **Execution and assertion:** verify normal runner/CI discovery, version-labelled filters, cleanup, awaited observations and a meaningful assertion on production behavior. A useful assertion should distinguish the relevant broken behavior; execute a fix-removal/base control when practical, and distinguish inspection from execution. Do not force a feature flag or reproduce the implementation as the expectation and then claim released integration coverage.
5. **Readiness:** record whether the submitted coverage meets these conventions and whether concrete maintainer test requests remain. Green CI, an earlier Astra review, or a correct source fix does not clear an unsuitable integration fixture. Identify this as a test-design repair without inventing a runtime failure.

Apply this gate before calling a PR ready. Do not require new tests for every small documentation or cosmetic change. Existing appropriate coverage can suffice.

For a successful protocol/lifecycle integration case, preserve valid peer codec states through the actual transition and observe unexpected parser/connection errors. A manual state switch that makes queued play bytes decode as configuration packets can clear state through an error/disconnect and falsely satisfy a cleanup assertion. Such errors must not silently count as success; keep deliberate malformed-packet tests separately scoped to their expected failure.

## Concrete repository routes

| Changed claim | Established route to inspect at the candidate revision |
|---|---|
| Mineflayer packet/plugin state, inventory events, controls | `test/internalTest.js`: actual `mineflayer.createBot` connected to the local `minecraft-protocol` server, existing version/login/chunk helpers. Send packets through the server writer and observe real bot events/state or server-received writes. Some revisions may split internal suites; follow that revision's organization. |
| Mineflayer server-authoritative action | `test/externalTest.js` and `test/externalTests/*` own Minecraft-wrap setup and action helpers. Internal coverage is sufficient for local packet/state claims; use external evidence when claiming actual accepted placement, consumption or other server behavior. |
| Pathfinder plugin events, cancellation and controls | `test/internalTest.js`, especially `pathfinder events`: actual Mineflayer bot, NMP server, serialized prismarine chunks and `bot.loadPlugin(pathfinder)`. Reuse world setup and cleanup. Assert after the event-producing tick finishes if the bug installs stale state after a callback returns. Real A* inside a fabricated bot does not replace this coverage. |
| Chunk factory/block access/JSON for another supported version | `test/versions.js` → `bedrockVersions`/`allVersions` → `test/ChunkColumn.test.js`. Extend the appropriate shared matrix and behavior cases instead of duplicating them in a release-named test file. |
| Chunk network/cache formats | `test/bedrock.test.js` has captured per-version fixture directories. Its matrix is separate from shared column model tests: do not append a version without the required packet fixtures, or treat JSON round-trips as wire evidence. |
| Physics simulation, chunk palettes, geometry or standalone helpers | Exercise the actual production algorithm with controlled inputs using the package's established unit fixtures. `prismarine-physics` fake players/worlds around real `Physics`, `PlayerState` and blocks, and chunk `ChunkSection`/`PalettedStorage` tests, are legitimate model tests. Their scope does not establish downstream bot/server integration. |

These paths are navigation examples, not immutable APIs. Check the current checkout. Mineflayer's CI can select suites by `${version}v`; a file discovered locally may still be skipped by those filters. Pathfinder and chunk run their Mocha suites through package scripts. Inspect scripts and workflows rather than hardcoding a remembered command.

An EventEmitter is the real input for a `onceWithCleanup` utility test. It becomes problematic when combined with invented bot state, no-op `_client.write`, substitute controls and manual plugin injection to stand in for Mineflayer's existing integration harness. Controlled clocks, providers and transport failures can be appropriate for isolated fault injection; keep the production boundary under test intact and do not replace an explicitly requested harness.

Distinguish observation from replacement: a `_client.write` wrapper that records arguments and delegates to the original writer preserves the real transport; a collector that never calls it does not. A controlled lifecycle trigger on an otherwise real bot can isolate an ordering case. Judge the boundary and claim actually bypassed, not the mere presence of an emitter, wrapper or manually triggered event.

Installing a plugin to expose an algorithm does not automatically turn its test into an integration claim. A `getPathFromTo` test comparing real raw and postprocessed waypoints with controlled blocks can be a focused path algorithm test; event-driven cancellation or control installation needs the real-bot harness. Likewise, NMP's existing injected-plugin unit fixtures can test local channel bookkeeping or decoded dispatch. Check their assertions and CI discovery, and require actual client/server coverage when the claim crosses that boundary. Inspect each package's own precedents before transferring Mineflayer's fixture requirements to it.

## Diagnostic probes are not automatically submitted regression tests

An isolated fake-bot probe can help reproduce a geometry or lifecycle defect. Describe it as diagnostic evidence, including what it bypasses. Recommend maintained coverage in the existing internal/external harness when the changed contract is bot/plugin integration. Do not request removal of useful focused algorithm cases merely because an integration regression is also needed. No new ecosystem-wide testing framework is necessary for the examples above.

## Maintainer evidence and limits

- [rom1504 on Mineflayer #4053](https://github.com/PrismarineJS/mineflayer/pull/4053#discussion_r4174311961): the fabricated inventory bot/client should be replaced by an internal or external test. A real registry and successful version loop did not resolve the objection.
- [rom1504 on pathfinder #386](https://github.com/PrismarineJS/mineflayer-pathfinder/pull/386#discussion_r4174313991): check existing tests instead of constructing a completely mocked bot. The existing NMP-backed event suite supplies the relevant integration.
- [rom1504 on chunk #338](https://github.com/PrismarineJS/prismarine-chunk/pull/338#discussion_r4174319033): no dedicated file for the new version's shared behavior checks. This does not prohibit focused format-boundary assertions or genuine versioned wire fixtures.

These are concrete manual comments from 2026-10-03. Existing comments with the same root cause and requested action should be linked and retained, not restated as another Astra finding. Recheck later replies and code before applying an outstanding-request gate.
