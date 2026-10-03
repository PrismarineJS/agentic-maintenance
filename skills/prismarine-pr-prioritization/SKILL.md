---
name: prismarine-pr-prioritization
description: Rank PrismarineJS and ProtoDef PRs for maintainer attention or merge batches using the maintainer's priorities for version support, Minecraft functionality, broad capabilities and abstraction quality. Use for requests such as most important PRs, next ten ready PRs, or what to work on next; pair with prismarine-review to establish readiness.
---

# Prioritize PrismarineJS work

This ordering records rom1504's explicit preference. Use it when selecting work, alongside the [common review skill](../prismarine-review/SKILL.md) and relevant domain skills.

## Lead with these four outcomes

These are one leading group, without a fixed internal order or invented numerical weights:

| Outcome | Evidence of value in PrismarineJS |
|---|---|
| New Minecraft version support | A coherent advance toward usable Java or Bedrock version support. Trace `minecraft-data` → `node-minecraft-data` publication → protocol/model packages → bots, servers, viewers or other consumers. Identify the missing link a PR supplies. A version alias alone does not prove full support. |
| New Minecraft functionality | A previously unsupported mechanic, interaction, packet, content format or game system becomes available. Describe what a consumer can now do, including any remaining consumer implementation. |
| Broad capabilities | Reusable behavior expands what multiple bots, servers, proxies, viewers or downstream applications can do. Name actual consumers or clearly label plausible ones; do not invent adoption. |
| Abstraction quality | Responsibilities move to the right package, shared models replace duplicated facts/state, or a consistent API reduces the cost of future versions and features. Name the duplication or boundary improved and who benefits. Extraction or extra layers alone do not earn priority. |

Correctness fixes, regression prevention, performance and routine maintenance normally follow this group. Raise them when they directly enable one of the leading outcomes, naming the dependency. An exceptional urgent outage, corruption or comparable serious risk can take precedence; explain the concrete urgency. Do not treat all bug fixes as emergencies.

Within the leading group, compare the significance of the capability, breadth of versions and consumers, and how much blocked work it unlocks. Avoid counting the same benefit repeatedly under several headings. Prefer concrete benefit over speculative roadmaps. Age, author, diff size, easy review and green CI are not measures of importance.

## Establish readiness separately

For a requested ready-to-merge batch, refresh open/merged/draft state, reviewed head, current base compatibility, CI and discussion. Recheck affected code when the head or relevant base changed. Apply the common skill's testing and maintainer-feedback gates; importance cannot waive a blocker. A required maintainer approval is distinct from an unresolved requested change.

After recent merges, verify the actual target branch tip: GitHub's recorded base and test-merge ref can lag. Check a test merge's parents before treating its results as current integration evidence.

For a work-priority queue, include valuable blocked work when useful, but label its blocker and next action. Never silently turn that queue into a merge recommendation. If fewer than the requested number are ready, say so rather than relaxing the gate.

Trace dependencies and overlapping PRs before ordering a batch. Generated data can sometimes land safely before its wrapper or consumer; a consumer that requires unavailable data without a compatible fallback cannot. Distinguish merge readiness from npm release and feature activation, recording the necessary order and minimum dependency where established. Group related PRs into a coherent landing sequence; do not select two superseding implementations as two independent improvements. Recheck later PRs after earlier merges affect their base.

## Present the recommendation

Give a ranked table with PR link, concrete benefit under the leading outcomes, and any essential landing or release condition. State the freshness and scope of the readiness check and link to the review evidence where useful. Explain exceptional overrides and important exclusions briefly. Carry validation limits forward: an earlier focused test is not a newly executed full integration test. Ranking does not itself authorize posting reviews, approving or merging PRs.
