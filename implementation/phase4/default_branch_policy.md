# Proposed default-branch settings diff

Date: 2026-10-06T02:50:13.127012+00:00. Source: GitHub GET-only audit.

No settings changed. The JSON companion contains the exact desired rulesets, current evidence, and per-repository diff.

## Scope

- 98 repositories inventoried; 94 public, unarchived repositories included.
- 3 archived and 1 private repositories excluded.
- 188 proposed ruleset creations after CI/automation prerequisites; 30 classic protections to reconcile.
- 64 default branches have no classic protection; 29 require a PR; 10 name required checks.
- 0 included repositories have read errors. Activation readiness is not certified for any repository by this settings audit.

## Intended behavior

All included repositories: `ci` from GitHub Actions, up-to-date branch, no force pushes/deletion, no CI bypass. PR plus one approval, with repository-admin bypass **for PRs only**. Two independent rulesets keep that exception out of CI.

Admins can merge a passing unapproved PR. They cannot use this exception to merge failing CI or push directly. Private repositories remain outside enforceable coverage on this plan.

## Per-repository proposal

These current PR/check columns describe classic protection; consult the JSON evidence for any additional rulesets. A ruleset creation/update is deferred until repository-specific CI and automation have been validated. Existing classic patterns must be inspected before retiring them.

| Repository | Default branch | Current PR / approvals | Current required checks | Proposed rulesets | Classic protection |
|---|---|---|---|---|---|
| [.github](https://github.com/PrismarineJS/.github/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [agentic-maintenance](https://github.com/PrismarineJS/agentic-maintenance/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [auto-alpaca](https://github.com/PrismarineJS/auto-alpaca/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [auto-sheep](https://github.com/PrismarineJS/auto-sheep/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [bedrock-protocol](https://github.com/PrismarineJS/bedrock-protocol/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [bedrock-provider](https://github.com/PrismarineJS/bedrock-provider/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [burger-extractor](https://github.com/PrismarineJS/burger-extractor/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [dazed-sheep](https://github.com/PrismarineJS/dazed-sheep/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [diamond-square](https://github.com/PrismarineJS/diamond-square/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [entity-model-extractor](https://github.com/PrismarineJS/entity-model-extractor/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [flying-squid](https://github.com/PrismarineJS/flying-squid/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [flying-squid-modpe](https://github.com/PrismarineJS/flying-squid-modpe/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [gdmc-challenge-2021](https://github.com/PrismarineJS/gdmc-challenge-2021/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [llm-guides](https://github.com/PrismarineJS/llm-guides/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [marketing-and-media](https://github.com/PrismarineJS/marketing-and-media/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [McDataExtracting](https://github.com/PrismarineJS/McDataExtracting/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mcdevs-wiki-extractor](https://github.com/PrismarineJS/mcdevs-wiki-extractor/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [minecraft-assets](https://github.com/PrismarineJS/minecraft-assets/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [minecraft-assets-pixel-perfection](https://github.com/PrismarineJS/minecraft-assets-pixel-perfection/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [minecraft-chunk-dumper](https://github.com/PrismarineJS/minecraft-chunk-dumper/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [minecraft-classic-protocol](https://github.com/PrismarineJS/minecraft-classic-protocol/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [minecraft-classic-protocol-extension](https://github.com/PrismarineJS/minecraft-classic-protocol-extension/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [minecraft-data](https://github.com/PrismarineJS/minecraft-data/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [minecraft-data-auto-updater](https://github.com/PrismarineJS/minecraft-data-auto-updater/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [minecraft-data-generator](https://github.com/PrismarineJS/minecraft-data-generator/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [minecraft-inventory-gui](https://github.com/PrismarineJS/minecraft-inventory-gui/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [minecraft-jar-extractor](https://github.com/PrismarineJS/minecraft-jar-extractor/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [minecraft-packets](https://github.com/PrismarineJS/minecraft-packets/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [minecraft-wiki-extractor](https://github.com/PrismarineJS/minecraft-wiki-extractor/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [mineflayer](https://github.com/PrismarineJS/mineflayer/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [mineflayer-builder](https://github.com/PrismarineJS/mineflayer-builder/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-cmd](https://github.com/PrismarineJS/mineflayer-cmd/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-collectblock](https://github.com/PrismarineJS/mineflayer-collectblock/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-gptj](https://github.com/PrismarineJS/mineflayer-gptj/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-navigate](https://github.com/PrismarineJS/mineflayer-navigate/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [mineflayer-pathfinder](https://github.com/PrismarineJS/mineflayer-pathfinder/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-pvp](https://github.com/PrismarineJS/mineflayer-pvp/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-radar](https://github.com/PrismarineJS/mineflayer-radar/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [mineflayer-scaffold](https://github.com/PrismarineJS/mineflayer-scaffold/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-statemachine](https://github.com/PrismarineJS/mineflayer-statemachine/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-test-api](https://github.com/PrismarineJS/mineflayer-test-api/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [mineflayer-tool](https://github.com/PrismarineJS/mineflayer-tool/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [MineflayerArmorManager](https://github.com/PrismarineJS/MineflayerArmorManager/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [net-browserify](https://github.com/PrismarineJS/net-browserify/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-canvas-webgl](https://github.com/PrismarineJS/node-canvas-webgl/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-minecraft-assets](https://github.com/PrismarineJS/node-minecraft-assets/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [node-minecraft-data](https://github.com/PrismarineJS/node-minecraft-data/settings/rules) | `master` | Yes / 1 | build (24.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [node-minecraft-extractor](https://github.com/PrismarineJS/node-minecraft-extractor/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-minecraft-packets](https://github.com/PrismarineJS/node-minecraft-packets/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-minecraft-protocol](https://github.com/PrismarineJS/node-minecraft-protocol/settings/rules) | `master` | Yes / 1 | test (1.12.2), test (1.13.2), test (1.14.4), test (1.15.2), test (1.11.2), test (1.16.5), test (1.7), test (1.17.1) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [node-minecraft-protocol-forge](https://github.com/PrismarineJS/node-minecraft-protocol-forge/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-minecraft-wrap](https://github.com/PrismarineJS/node-minecraft-wrap/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [node-mojangson](https://github.com/PrismarineJS/node-mojangson/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-nethernet](https://github.com/PrismarineJS/node-nethernet/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-process](https://github.com/PrismarineJS/node-process/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-vec3](https://github.com/PrismarineJS/node-vec3/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [node-yggdrasil](https://github.com/PrismarineJS/node-yggdrasil/settings/rules) | `master` | Yes / 1 | build (18.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [numerous-alpaca](https://github.com/PrismarineJS/numerous-alpaca/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-archiver](https://github.com/PrismarineJS/prismarine-archiver/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-auth](https://github.com/PrismarineJS/prismarine-auth/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-biome](https://github.com/PrismarineJS/prismarine-biome/settings/rules) | `master` | Yes / 1 | build (18.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-block](https://github.com/PrismarineJS/prismarine-block/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-chat](https://github.com/PrismarineJS/prismarine-chat/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-chunk](https://github.com/PrismarineJS/prismarine-chunk/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-contribute](https://github.com/PrismarineJS/prismarine-contribute/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-design](https://github.com/PrismarineJS/prismarine-design/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-entity](https://github.com/PrismarineJS/prismarine-entity/settings/rules) | `master` | Yes / 1 | build (18.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-gameplay](https://github.com/PrismarineJS/prismarine-gameplay/settings/rules) | `master` | Yes / 1 | build (12.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-item](https://github.com/PrismarineJS/prismarine-item/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-loottable](https://github.com/PrismarineJS/prismarine-loottable/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-meta](https://github.com/PrismarineJS/prismarine-meta/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-monotree](https://github.com/PrismarineJS/prismarine-monotree/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-nbt](https://github.com/PrismarineJS/prismarine-nbt/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-packet-dumper](https://github.com/PrismarineJS/prismarine-packet-dumper/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-physics](https://github.com/PrismarineJS/prismarine-physics/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-provider-anvil](https://github.com/PrismarineJS/prismarine-provider-anvil/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-provider-raw](https://github.com/PrismarineJS/prismarine-provider-raw/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-proxy](https://github.com/PrismarineJS/prismarine-proxy/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-realms](https://github.com/PrismarineJS/prismarine-realms/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-recipe](https://github.com/PrismarineJS/prismarine-recipe/settings/rules) | `master` | Yes / 1 | build (18.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-registry](https://github.com/PrismarineJS/prismarine-registry/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-repo-actions](https://github.com/PrismarineJS/prismarine-repo-actions/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-rng](https://github.com/PrismarineJS/prismarine-rng/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-schematic](https://github.com/PrismarineJS/prismarine-schematic/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-template](https://github.com/PrismarineJS/prismarine-template/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-updates](https://github.com/PrismarineJS/prismarine-updates/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-viewer](https://github.com/PrismarineJS/prismarine-viewer/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-web-client](https://github.com/PrismarineJS/prismarine-web-client/settings/rules) | `master` | Yes / 1 | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-windows](https://github.com/PrismarineJS/prismarine-windows/settings/rules) | `master` | Yes / 1 | build (18.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-world](https://github.com/PrismarineJS/prismarine-world/settings/rules) | `master` | Yes / 1 | build (18.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [prismarine-world-sync](https://github.com/PrismarineJS/prismarine-world-sync/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarine-xbox-services](https://github.com/PrismarineJS/prismarine-xbox-services/settings/rules) | `main` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
| [prismarinejs.github.io](https://github.com/PrismarineJS/prismarinejs.github.io/settings/rules) | `src` | Yes / 1 | build (14.x) | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | Reconcile after replacement |
| [speedrun-challenge-ssgp](https://github.com/PrismarineJS/speedrun-challenge-ssgp/settings/rules) | `master` | No | None | pjs-ci-and-history: create_after_prerequisites; pjs-pr-and-review: create_after_prerequisites | absent |
