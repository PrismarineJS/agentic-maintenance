# Replace broad review advice with PrismarineJS operating knowledge

Date: 2026-09-14. Status at writing: design, before skill changes. Starting commit: `06251e0`. Sources: the phase3 historical survey, its original five skills and frozen evaluations, and the subsequent 54-PR U9G review with verified reproductions and two withdrawn findings.

## Problem and intended result

The first skills mostly described general review discipline and linked PrismarineJS examples. Their evaluation measured supported findings and restraint, without adequately testing whether the instructions supplied ecosystem knowledge. The replacement should let a reviewer locate the actual owner, understand its representation/lifecycle, construct a distinguishing check, and recognize the exception without rediscovering the subsystem from scratch.

Keep a short `prismarine-review` entry point for routing, revision/outcome recording, deduplication and the user's Astra attribution/publication requirements. Replace the broad specialist categories with six concrete skills at the repository's top-level `skills/`:

| Folder | Operating knowledge to encode |
| --- | --- |
| `prismarine-protocol-data-review` | Schema/dataPaths/Node-wrapper loading, released feature availability, NMP compiled codecs versus ProtoDef interpreter, semantic enums versus wire bytes, maintained sources/generators and downstream checks. |
| `prismarine-lifecycle-action-review` | Mineflayer/NMP configuration, login, respawn and transfer; ownership/reset of settings, input caches, queued replies, prediction sequences and action completion. |
| `prismarine-item-inventory-review` | NBT/component/text representations, item conversion and hashed claims, cursor/window state IDs, server reconciliation and crafting remainders. |
| `prismarine-geometry-movement-review` | Block shapes, eye/face/cursor conventions, entity bounds and attribute limits, teleport velocity, physics branches and pathfinder completion/cancellation. |
| `prismarine-world-render-review` | Registry/world identity, dimension bounds and chunk/section coordinates, partial entity updates, worker generations, asset readiness and resource ownership. |
| `prismarine-architecture-review` | Actual package responsibilities, shared-state boundaries, dependency release chains, model factories, public declarations and host/extension contracts; concrete reasons to extract or retain code. |

Delete `prismarine-code-quality-review` and `prismarine-behavior-test-review` after moving useful knowledge into the relevant domains. Code quality remains explicit in domain APIs/state/error handling and the architecture skill. Test selection belongs beside the actual subsystem and existing harness it exercises.

## Content standard

Each specialist needs verified file/symbol entry points, several non-obvious domain contracts, distinguishing inputs or event traces, appropriate existing test locations, version/dependency qualifications, and supporting source links. Put long runnable recipes and source detail in focused references. A principle that could be pasted unchanged into an unrelated project should normally leave the specialist.

Use the archived exact-head application sources and the already-collected maintainer discussion as evidence. Verify path/symbol claims against code; label branch-specific additions as review examples rather than APIs already available in every release. Preserve positive examples and retractions. The compiled mapper case must explain the production path and include a usable probe: numeric writes accepted by released compiled ProtoDef do not imply that removing a mapper preserves named writes.

Historical account attribution is usually undisclosed manual authorship. The recent Astra findings are validated engineering examples, not independent maintainer policy. Pending PRs and recorded merge outcomes are dated evidence, not perpetual current-state claims. Module locations are navigation aids to recheck at the reviewed revision.

## Implementation order and compatibility

1. Write this design before editing skills.
2. Author the six specialists and shorten the common entry point. Use bounded parallel authoring where it helps, with disjoint folders and this design as context.
3. Update the repository's current skill navigation and validator for the seven active folders. Preserve original survey/evaluation data and frozen skill snapshots. Repair historical links to removed or rewritten skills using the original committed versions, so the old report does not imply its scores apply to new content.
4. Validate frontmatter, local links, source entry points and any executable helpers. Exercise representative positive and negative cases with real available code/dependencies. Use an independent agent for a small realistic read-only use test without prescribing its answer; distinguish known-case exercises from a held-out benchmark.
5. Revise only where those checks expose a concrete problem. Write `implementation/phase3/domain_specific_review_skills.md` with the migration, source basis, checks, results and limits.
6. Commit and push the design, skills, navigation/validation changes and report to `PrismarineJS/agentic-maintenance`.

This task does not start another 500-PR survey, publish further PR comments, modify application repositories, install skills globally or include the three pre-existing untracked phase2 drafts.

## Acceptance criteria

- Seven active folders: one short common workflow and six domain specialists, discoverable through useful descriptions and routing links.
- A reader gets concrete PrismarineJS mechanisms, code entry points and distinguishing checks from each specialist, including code-quality and architecture decisions.
- Known errors from the last pass are addressed explicitly: interpreter/compiled mismatch, absent released feature flags, unit-cube ray assumptions, stale asynchronous world/entity state and missing public declarations.
- Relevant exceptions remain: bounded fixes can land before independent refactors; existing model/codec tests can suffice; documented representation changes and historical generator exceptions are not automatically defects.
- New helper scripts run, validators and links pass, and an independent use check is reported honestly. No claim of broader accuracy improvement follows from a few known examples.
- Historical evidence remains attributable to the skill version actually evaluated; the pushed commit contains the complete authorized change.
