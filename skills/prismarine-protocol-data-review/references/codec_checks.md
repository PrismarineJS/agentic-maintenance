# Reusable codec checks

Verified 2026-09-14 against minecraft-protocol 1.67.0 / minecraft-data 3.114.0 and minecraft-protocol 1.68.0 / minecraft-data 3.116.0, both with ProtoDef 1.19.0. Recheck implementation paths for newer dependencies.

Run the [portable numeric/symbolic probe](../scripts/numeric_mapper_paths.cjs) with Node and an absolute package.json path from the runtime being reviewed:

```sh
node skills/prismarine-protocol-data-review/scripts/numeric_mapper_paths.cjs /absolute/consumer/package.json
```

It opens no connection, installs nothing, and prints resolved versions, complete packet bytes and decoded values. It checks three `client_command.actionId` and two `use_entity.hand` numeric/symbolic pairs on 26.1 through NMP's default compiler, then shows the isolated interpreter result. An assertion failure on a future release is a changed behavior to investigate, not automatic proof of a regression. Adapt the packet and version for the PR rather than treating this fixed regression probe as general codec coverage.

For schema edits, execute the baseline and candidate in separate processes. Record package resolution, selected `mcData.version` and the category's dataPaths entry alongside results. Compare at least one distinguishing nonzero value: zero often hides an enum/default error. Inspect a source-grounded expected byte sequence when choosing varint versus zigzag or integer width. For native types, use NMP registration, including Minecraft and NBT types; a bare compiler can fail before it reaches the proposed change.

## Why these checks exist

These are explicit **Astra findings/corrections**, not independent evidence of maintainer preferences:

- [Mineflayer #4086 correction](https://github.com/PrismarineJS/mineflayer/pull/4086#discussion_r4004019860) and [#4089 correction](https://github.com/PrismarineJS/mineflayer/pull/4089#discussion_r4004042201): numeric values encoded through the actual compiled path; interpreter rejection did not establish a production bug.
- In the archived candidate data #1278/#1284 probes, deleting mappings changed named `off_hand` bytes from `1a01010000` to `1a01000000`; named `request_stats` changed `0c01` to `0c00`. These bytes are tied to that 26.1 schema, not universal packet IDs. Full results remain in [the phase3 checks](../../../implementation/phase3/u9g_rereviews.json).
- [Mineflayer #4063](https://github.com/PrismarineJS/mineflayer/pull/4063#discussion_r4003932298): the feature-gated legacy sneak path failed with the allowed released wrapper even though the new data work existed elsewhere.

The historical maintainer discussion in [ProtoDef #176](https://github.com/ProtoDef-io/node-protodef/pull/176#issuecomment-5651567589) distinguishes unknown numeric proxy IDs from invalid symbolic input **after merge**. Keep that chronology; neither blanket strictness nor unlimited coercion follows.
