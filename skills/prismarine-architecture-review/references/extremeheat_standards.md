# Extremeheat review standards and their scope

Checked 2026-09-21. The maintainer explicitly instructed us to trust extremeheat's judgment. The decisions below therefore guide reviews in their applicable context, including maintainability concerns without a demonstrated runtime bug. Public account attribution is verified; explicitly Astra/Codex-authored reviews are excluded as independent evidence of his preferences. PR outcomes below describe this dated evidence, not perpetual readiness.

## Code quality and ownership

- [Mineflayer #4114](https://github.com/PrismarineJS/mineflayer/pull/4114#discussion_r3998188710), open: repeated interaction code across PRs prompted a request for a cleaner shared implementation. Review the actual producer/callers together and identify the smallest common operation, not a speculative general framework.
- [Mineflayer #4098](https://github.com/PrismarineJS/mineflayer/pull/4098#discussion_r3998208514), open: the observed-inventory implementation was asked to fit existing plugin structure. Passing behavioral tests would not answer that request. His separate one-word removal requests on test files do not establish a blanket objection to tests.
- [Mineflayer #4118](https://github.com/PrismarineJS/mineflayer/pull/4118#discussion_r3998184615), open: reusable entity behavior should be considered for prismarine-entity. Demonstrate which part is shared model computation and which part remains packet translation in Mineflayer.
- [Mineflayer #4085](https://github.com/PrismarineJS/mineflayer/pull/4085#discussion_r3998197704): extremeheat questioned whether a new plugin was necessary. Later [rom1504 required keeping loader.js generic](https://github.com/PrismarineJS/mineflayer/pull/4085#discussion_r4054393126), and the counter moved back into a plugin. Preserve that chronology: neither “always create a plugin” nor “never create a plugin” follows. The owner's explicit later instruction settles this instance.

## Tests that exercise the implementation we ship

- [Mineflayer #4118](https://github.com/PrismarineJS/mineflayer/pull/4118#discussion_r3998183658) and [#4116](https://github.com/PrismarineJS/mineflayer/pull/4116#discussion_r3998186145), open: prefer an NMP server/client fixture over reconstructing a bot and packet source in a bespoke test.
- [NMP #1521](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1521#pullrequestreview-5124257368), open: the project implements both client and server; check both sides of a changed acknowledgement/signing contract. Its [test comment](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1521#discussion_r3943062089) explicitly allows an NMP client/server pair as the alternative to a real server.
- [Data #747](https://github.com/PrismarineJS/minecraft-data/pull/747#pullrequestreview-1564292284), merged, 2023-08-06: extremeheat approved while explicitly noting absent semantic data tests. Do not turn the above preference into a demand for a new fixture on every edit.

## Source consistency and general validation

- [Mineflayer #4079](https://github.com/PrismarineJS/mineflayer/pull/4079#pullrequestreview-5129023740), closed unmerged: normalize data upstream instead of accumulating consumer flags for numeric/mapper inconsistencies. The [follow-up](https://github.com/PrismarineJS/mineflayer/pull/4079#issuecomment-5566561005) proposes cross-version consistency checking. This does not eliminate features for genuine protocol transitions.
- [Data #1298](https://github.com/PrismarineJS/minecraft-data/pull/1298#discussion_r4011940737), merged into a version branch: distinguish the same semantic packet renamed in vanilla from a genuinely new packet. [Preserve old names or backport consistently](https://github.com/PrismarineJS/minecraft-data/pull/1298#discussion_r4023520517) when changing exposed representations. A branch merge does not demonstrate release availability.
- [Data #1276](https://github.com/PrismarineJS/minecraft-data/pull/1276#discussion_r3964565152), merged: express uniqueness at schema level to catch the class of defect. [#1297](https://github.com/PrismarineJS/minecraft-data/pull/1297#discussion_r4030597820), open: the generic validation test should not be limited to blocks.
- [Data #1286](https://github.com/PrismarineJS/minecraft-data/pull/1286#discussion_r3964901882), merged: generic checks belong in protodef-validator, but the local check was explicitly accepted as a useful stopgap. This is a model for separating the architectural destination from today's landing condition.

## Costs and reproducible sources

- [NMP #1516](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1516#pullrequestreview-5061987167), closed unmerged: implicit disk caching breaks browser consumers and adds invalidation/storage concerns; investigate existing memory caching and the actual startup cost first. The conclusion concerns this design, not every optional cache.
- [ProtoDef #177](https://github.com/ProtoDef-io/node-protodef/pull/177#discussion_r3944772758), open: make sizing available to writing through compilation order, not per-call generation. [Sizing should not require writing](https://github.com/ProtoDef-io/node-protodef/pull/177#discussion_r3944795909); [algorithm support belongs in the portable specification](https://github.com/ProtoDef-io/node-protodef/pull/177#discussion_r3944759540), not whatever Node currently exposes. Check the latest implementation before repeating an old finding.
- [Generator #79](https://github.com/PrismarineJS/minecraft-data-generator/pull/79#issuecomment-5319158046), closed unmerged: an override layer of hardcoded corrections undermines extracting authoritative source data unless the disagreement is explained.
- Older corroboration: [data #1193](https://github.com/PrismarineJS/minecraft-data/pull/1193#issuecomment-4533234380), 2026-05-25, requires repairing the generator so the error does not return each version; [#1007](https://github.com/PrismarineJS/minecraft-data/pull/1007#issuecomment-2954213344), 2025-06-08, asks for documented generation instructions. Both were closed unmerged in the frozen survey.

## Do not promote brainstorming into policy

[Bedrock #810](https://github.com/PrismarineJS/bedrock-protocol/pull/810#discussion_r4052466063), merged, asks whether schema-driven validation could replace messy manual validation and suggests something like Zod. The actionable review question is duplication between schema and validation; it is not a requirement to add Zod. Likewise, a short request to remove a particular test file is insufficient to infer a repository-wide prohibition on fixtures. Apply direct decisions confidently while retaining their stated scope and later revisions.
