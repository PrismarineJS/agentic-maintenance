# Rank PRs by ecosystem value

Date: 2026-10-03. Source: rom1504's explicit priorities and request to add the skill and select the next ten ready PRs.

The maintainer wants new Minecraft version support, new Minecraft functionality, broad capability improvements and better abstractions to lead merge recommendations. These form a leading group; no fixed order or numerical weights between them were requested. Correctness, regression coverage, performance and routine maintenance normally follow. A repair enabling a leading priority inherits that importance; an exceptional urgent failure can override the normal ordering with an explicit explanation.

Add `skills/prismarine-pr-prioritization/SKILL.md` and route prioritization requests to it from the common review skill. Keep importance separate from readiness: current code, discussion, testing conventions, CI and release dependencies still determine whether a PR can land. An important blocked PR belongs in a work queue, not a ready-to-merge list.

Make the instructions specific to PrismarineJS's modular organization. Follow version work through generated facts, the Node data wrapper, protocols and reusable models to consumers. Recognize shared capabilities in world/item/block/codec APIs, while requiring a concrete benefit from abstractions. Distinguish an independently mergeable producer from downstream release activation. Compare overlapping PRs and recommend coherent landing sequences rather than counting duplicate implementations as separate wins.

Validate structure and links, then apply the skill to the existing reviewed queue using fresh GitHub state. Exclude the previous ten merged recommendations, check current discussions and dependencies for shortlisted candidates, and explain each selected PR's value and remaining release conditions. This practical exercise checks whether recommendations actually favor the requested outcomes. Record scope, evidence and limitations under `implementation/phase3/`; commit and push only task files.
