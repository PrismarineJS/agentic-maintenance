# Domain-specific review skills

Date: 2026-09-14. Source: the frozen phase3 historical survey and archived exact-head application sources, supplemented by fresh local checks described below. This implements [the design written before these skill changes](../../design/phase3/domain_specific_review_skills.md). Starting commit: `06251e0`.

## What changed

Replaced the broad five-skill set with **six domain specialists and one short common workflow**, all in top-level `skills/`. The specialists now supply concrete subsystem entry points, representations, lifecycle invariants, existing test harnesses and distinguishing inputs. Longer recipes and qualified examples live in linked references.

| Current skill | Examples of knowledge supplied |
| --- | --- |
| [Protocol/data](../../skills/prismarine-protocol-data-review/SKILL.md) | Data repository versus npm wrapper; dataPaths selection; unknown feature names returning false; NMP compiled/native/NBT registration; serializer cache contamination; numeric versus symbolic mapper contracts. |
| [Lifecycle/actions](../../skills/prismarine-lifecycle-action-review/SKILL.md) | NMP configuration versus Mineflayer readiness; settings snapshots; held versus sent input; queued reply cancellation; sequence producer and zero-sequence exceptions; synchronous dig re-entry. |
| [Items/inventory](../../skills/prismarine-item-inventory-review/SKILL.md) | NBT/components/text semantics; component array versus map; full versus hashed slot conversion; per-window state IDs, cursor and reconciliation; player slot index translation; crafting remainders. |
| [Geometry/movement](../../skills/prismarine-geometry-movement-review/SKILL.md) | Partial block shapes, face/cursor/eye conventions; model radians versus wire angles; effective attribute bounds; relative teleport velocity; air/fluid simulation branches; final-step pathfinder completion. |
| [World/rendering](../../skills/prismarine-world-render-review/SKILL.md) | Registry/world identity and update propagation; negative chunk coordinates and dimension bounds; stale loads and partial metadata; unsupported-item fallback; lazy texture readiness and disposal ownership. |
| [Architecture/public APIs](../../skills/prismarine-architecture-review/SKILL.md) | Actual package responsibility; shared producer versus call-site repairs; model factories and CommonJS exports; decoded-copy getter costs; compiler extension contracts; required Host methods and declarations; bounded fixes versus necessary refactors. |
| [Common review workflow](../../skills/prismarine-review/SKILL.md) | Routing, current revisions and merge outcomes, proportionate evidence, duplicate root causes, and the user's Astra attribution/publication requirements. |

Deleted `prismarine-code-quality-review` and `prismarine-behavior-test-review`. Their useful API, state, completion, test-layer and scope guidance now sits in the relevant specialist. Code quality remains an explicit architecture responsibility and is grounded in domain costs rather than general style preferences.

Added a portable [compiled/interpreted mapper probe](../../skills/prismarine-protocol-data-review/scripts/numeric_mapper_paths.cjs). It accepts an existing consumer runtime's package.json, opens no connection and prints actual dependency versions, bytes and parsed values. The original reproduction remains unchanged as historical evidence.

Updated README routing and the corpus/skill validator for seven active folders. The [original report](report.md) now links its five skills to immutable commit `06251e0` and points here. The original survey, outcome records, evaluation inputs/results, frozen skill snapshots and public-review records are preserved. Historical JSON skill names still describe the skills actually used at the time.

## Evidence and authorship

The replacement reuses the existing 500-PR corpus; it does not claim a second survey. Merge accounting remains **250 merged, 183 closed-unmerged, 67 open**, with dates/revisions/outcomes retained in the original records. These are the survey snapshot's outcomes, not a refreshed GitHub census.

The skill references distinguish historical attributed account discussion (manual authorship usually undisclosed) from recent explicit Astra findings. The latter demonstrate engineering mechanisms; they are not independent evidence of maintainer preferences. Pending helpers such as `toHashedNotch`, prediction sequence and controller APIs are labeled as candidate examples, with released dependency prerequisites and version limits. Positive cases, retractions and accepted follow-up scope remain part of the guidance.

Two authoring subagents owned disjoint specialist folders: lifecycle/items and geometry/rendering. The coordinator wrote protocol, architecture and common workflow and integrated navigation, migration and validation. A third independent agent then exercised selected skills on raw archived candidates without receiving intended findings or the earlier reviewer conclusions.

## Validation performed for this revision

All seven skill-creator frontmatter/name validators pass. Relative links in current skills and the design resolve. The updated artifact validator passes all 500 historical cases and the seven active names. The [validation record](domain_specific_skill_validation.json) stores the portable probe outputs and final skill file hashes.

The following are fresh local reruns during this revision. Some probes intentionally reproduce a known candidate failure: a successful probe process is not a passing candidate fix.

| Area | Observed result and control |
| --- | --- |
| Portable mapper helper | Five numeric/symbolic pairs produced identical compiled bytes and named decoded values on NMP 1.67.0/data 3.114.0 and NMP 1.68.0/data 3.116.0, both ProtoDef 1.19.0. The isolated interpreter rejected numeric zero. |
| Settings and inventory | #4065 repeated configuration trace reproduced view distances `12,8,12`; #4103 null close, per-window IDs, relogin and respawn checks passed. |
| Text and hashed slots | #188 translated-name/stale-name and #189 JSON-looking literal cases reproduced. Coordinated candidate inventory/item/ProtoDef stack encoded nine click/resync packets across 1.21.4, 1.21.5 and 1.21.11. |
| Placement and attributes | #4115's nine existing placement tests passed, while a direct ray hit a bottom slab that strict placement rejected and default placement missed. #4118 attribute-handler checks reproduced unclamped negative/upper totals with ordinary-value controls. |
| Physics and pathfinder | #142's five flight tests passed; real block fixtures distinguished air altitude from water/lava sinking. #382 reached radius on its final permitted bridge step, then rejected. |
| World and renderer | Ordinary lifecycle/listener controls passed. The new deferred-column recipe reproduced a stale load. #484 readiness resolved before delayed bounds registered 120 dirty entries; minimal meshing produced 24 vertices on three versions. #503 delayed atlas success waited, required rejection fulfilled, and entity loading began on first render. #506 unsupported items lost drawable fallback. |

The detailed sources, versions, inputs and adaptable recipes are linked from each specialist. Author checks used actual archived production code with available dependency caches; controlled providers, clocks, loaders and small model fixtures isolate the disputed behavior. Previously recorded full-suite counts and hash-vector totals are labeled as historical in references, not claimed as fresh runs here.

## Independent functional use check

The independent agent received the new skill entrypoint, raw data #1284 base/head schemas and viewer #511 source, plus dependency locations. It did not receive expected answers or adjacent old reports. The skills themselves contain related examples, so this is **known-case functional validation, not a blinded or held-out accuracy benchmark**.

- For data #1284, it used actual NMP's compiled codec in separate baseline/candidate processes. Numeric IDs `0,1,2,7` worked in both. Named `request_stats` changed `0c01` → `0c00`; `request_gamerule_values` changed `0c02` → `0c00`. This supported the mapper compatibility finding while counterchecking the mistaken premise that numeric callers need mapper removal. The skill contributed production-path selection, nonzero numeric/symbolic probes and process isolation.
- For viewer #511, TypeScript 5.9.3 accepted a custom Host implementing all declared required members, but the actual `WorldRenderer.updateTexturesData` method threw `this.host.loadText is not a function`. Supplying block states directly or adding `loadText` succeeded. A separate `createNodeHost().loadText(...)` consumer failed TS2339. The runtime check isolated the production method with VM and a controlled texture loader; it did not render pixels. TypeScript used `skipLibCheck` to isolate consumer checks. This independent viewer check lacked a baseline and did not independently establish introduction timing. The skills contributed the declared-adapter versus runtime-call comparison and positive controls.

The use check exposed one wording problem: the world skill instructed reviewers to extend tests, which could imply editing during a read-only review. It now recommends existing host tests and a temporary consumer probe, with coverage changes proposed only when needed. No technical or navigation error was reported in the material exercised.

These checks establish that the instructions can guide useful concrete probes and counterchecks. They do not establish a general review-quality improvement, recall rate or false-positive rate. The old evaluation scores apply only to the old frozen skills.

## Limits and completion scope

No live Minecraft server, browser/WebGL run, complete application test matrix, generator regeneration or new held-out benchmark was performed for this documentation revision. New probes ran locally; no new PR reviews were posted. Application source repositories and global skill installation were outside this revision. The three pre-existing untracked phase2 drafts were preserved and excluded from the commit.

The commit includes this report, the design, the seven-skill revision, the portable helper and validation record, and the navigation/historical-link/validator updates. Publication is to the existing agentic-maintenance master branch as requested.
