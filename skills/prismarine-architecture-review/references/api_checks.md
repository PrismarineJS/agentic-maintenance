# Public API checks

Source snapshot: phase3 survey and U9G review, 2026-09-14. Pending-PR examples describe inspected candidates, not released APIs or independent human policy.

## Declared host accepted, runtime host rejected

Read the candidate `package.json` and resolve its declarations explicitly with TypeScript `--traceResolution`. Build the smallest consumer that supplies a structurally valid adapter. Then exercise the method that uses that adapter with the same object. Verify a complete adapter as a control. This tests the extension contract more directly than searching for an interface member.

[Astra's Viewer #511 finding](https://github.com/PrismarineJS/prismarine-viewer/pull/511#discussion_r4004102829) concerned `WorldRenderer` calling `host.loadText` while both `Host` and the declared `createNodeHost` return value omitted it. Compilation alone passed; runtime construction exposed the gap. The result was not a demand to expose every internal renderer method.

## New protocol options/events missing to TypeScript consumers

Compile documented example usage of the actual candidate package. Check option types, event overloads and the returned client shape separately. [Astra's NMP #1522 finding](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1522#discussion_r4004049893) found newly documented brand/cookies/knownPacks and transfer cookie access absent from `src/index.d.ts`. An existing broad event overload may accept an event name while losing its payload contract; inspect that consequence before claiming the event cannot compile.

## Factory shape and visibility controls

[World #115](https://github.com/PrismarineJS/prismarine-world/pull/115#issuecomment-1384653927) directed a type export into declarations rather than changing CommonJS runtime exports. [Mineflayer #2929](https://github.com/PrismarineJS/mineflayer/pull/2929#discussion_r1108945340) distinguishes internal underscore helpers from public methods. These are scope controls: mirror the existing runtime factory and documented consumer, rather than requiring all implementation details in the public API.

Historical merge status, revisions and discussion chronology remain in [the frozen survey records](../../../implementation/phase3/review_cases.jsonl). Prior Astra publication records are [separate](../../../implementation/phase3/u9g_rereviews.json); they are implementation evidence, not mined maintainer preferences.
