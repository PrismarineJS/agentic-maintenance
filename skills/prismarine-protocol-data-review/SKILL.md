---
name: prismarine-protocol-data-review
description: Review Minecraft wire schemas, ProtoDef codecs, minecraft-data generation and feature releases through their real Node consumers. Use for packet representation, version support, native types or data-loader changes.
---

# Protocol, data and version support

Locate the installed `minecraft-protocol`, `minecraft-data` and `protodef` through the reviewed consumer's module resolution. Record their versions, edition, Minecraft release, state and packet direction. The npm package `minecraft-data` is published from **node-minecraft-data**, which wraps the separate **minecraft-data** repository. A merged data PR does not establish that a bot's allowed npm dependency contains it.

## Trace the schema actually selected

Follow the category entry in `minecraft-data/data/dataPaths.json`, its maintained input (protocol YAML where present), generated JSON, and the Node wrapper's generated `data.js`. In `node-minecraft-data/index.js`, inspect `toMajor`, protocol-version selection and the loader cache. Categories can reuse older directories; numeric protocol versions can identify several releases or snapshots. Review the selected category, not just a newly added version directory.

`node-minecraft-data/lib/supportsFeature.js` builds feature values from `data/{pc,bedrock}/common/features.json`. In the inspected wrapper releases, unknown names return **false**; values are not necessarily booleans. A newly invented positive gate can silently disable a legacy path on an otherwise allowed dependency. Compare the oldest dependency satisfying `package.json` with the candidate data release, and exercise one version on each side of the real transition. Mineflayer #4063 exposed this for `sneakUsesEntityAction`: data 3.114.0 and 3.116.0 lacked the flag. Preserve a valid fallback or coordinate a released minimum. Do not treat a feature flag as proof that the wire schema is present.

For extracted facts, identify the live generator and reproduce its output when that is the disputed contract. A historical correction need not change a generator that no longer produces it. For large protocol copies, compare the inherited baseline and semantic delta. Check all embeddings of shared slot, item-cost and position types: optionality, array counts and prefixes can corrupt the next field even when the first value looks right. Nine relative-position flags still used a four-byte field in data #1154; logical bit count cannot choose wire width.

## Exercise Minecraft's codec path

Start at `node-minecraft-protocol/src/transforms/serializer.js`, not an isolated ProtoDef instance. The inspected NMP 1.67.0/1.68.0 production path compiles by default and registers Minecraft native codecs plus big-endian NBT. A schema naming a native type is insufficient without its compiler/interpreter registration and a usable released dependency.

For a client-written packet, pair `createSerializer({ state, version, isServer: false })` with `createDeserializer({ state, version, isServer: true })`. Reverse both flags for server-written packets. Supply the entire `{ name, params }` packet, including fields selected by version-dependent containers/switches. Compare encoded bytes, parsed semantics and packet size; add an authoritative byte/source fixture when asserting vanilla compatibility. Round-tripping two implementations of the same wrong schema is not that oracle.

**Isolate candidate schemas.** The inspected serializer caches by state/direction/version/compiled mode, omitting `customPackets`, and merges custom definitions into the loaded protocol object. Two schemas tested sequentially in one process may reuse or mutate the baseline. Run each candidate in a fresh process. Verify this behavior against the dependency under review before adapting the harness.

## Preserve mapper and registry contracts

A mapper serves both symbolic consumers and raw numeric callers. With ProtoDef 1.19.0, NMP's compiled writer accepts numeric `hand` and `actionId` values that the isolated interpreted mapper rejects. This caused two withdrawn Astra findings. Conversely, removing a mapper can make named `off_hand` or `request_stats` writes encode the wrong ordinal. Test both forms and an intentional unknown numeric value when proxy passthrough is supported; an invalid symbolic string has a different contract. Cover read/write/size in both engines for a ProtoDef change, and production compiled behavior for an NMP/Mineflayer claim.

Use [the codec probe and version-qualified examples](references/codec_checks.md) for this distinction. Successful field encoding does not establish a whole action: the corresponding `use_entity` location gate, connection phase and packet container still need to agree.

Keep protocol IDs, runtime IDs, block state IDs and registry entries distinct. `prismarine-registry/lib/index.js` starts from static data but adds edition-specific registry behavior; a newly constructed registry is not proof of receiving negotiated session updates. Use the world skill for update ownership and the item skill for stack conversion. Backport only across versions where the type/defect existed; runtime-extensible registries and dimension names should not become closed vanilla enums incidentally.

## Choose the landing condition

Run the changed producer with the actual downstream candidate package: data → Node wrapper → NMP/model → affected bot/server path. A branch pin can demonstrate this before publishing; record the release prerequisite separately. For codec failures retain the failing packet and buffer before blaming compiler machinery. For hot codec changes benchmark equivalent workloads after checking semantic parity.

Read [historical decisions and exceptions](references/sources.md) when deciding ownership, generation or backport scope. They include merged changes with later objections and withdrawn requests. Use the common review skill for current-head checks and publication; this skill supplies no permission to post.
