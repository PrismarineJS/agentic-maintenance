---
name: prismarine-review
description: Review PrismarineJS and ProtoDef changes using concrete behavior, current revisions, package contracts, and proportionate validation. Use as the common workflow for PR reviews, including deciding whether an inline comment is justified and avoiding stale or duplicate findings.
---

# PrismarineJS review

Review the proposed behavior and its consequences. Historical discussions supply useful questions and exceptions; they do not replace checking the code. Read [evidence and exceptions](references/evidence.md) when a historical precedent affects the recommendation.

## Establish what is being reviewed

1. Record repository, PR URL, current base/head, open/closed state and **merged status separately**. Read the request, changed code, relevant callers, and existing discussion. Identify which revision each concern addressed. For a historical snapshot, use only the provided evidence; do not substitute a final diff for the code originally reviewed.
2. State the intended observable change and affected contract: public API, packet bytes, generated data, model state, timing, or application behavior. Identify the actual failure or benefit before proposing a fix. Distinguish a documented intentional contract change from an accidental regression.
3. Map the owner and consumers. `minecraft-data` holds shared language-independent data; `node-minecraft-data` exposes it to JavaScript; ProtoDef supplies generic codecs; `node-minecraft-protocol` handles Minecraft protocol connections; Prismarine model packages supply reusable state; Mineflayer and flying-squid apply it in bots and servers. Verify the actual call path and mutable registry ownership rather than assuming this map settles every boundary.
4. Check the dependency version that consumers will install, not just a sibling repository's master. For coordinated changes, an explicit candidate dependency can establish integration before release. Record the release prerequisite separately from an inline implementation defect.

## Select the useful specialist skills

Read the relevant sibling `SKILL.md` files, not every skill automatically:

- `prismarine-code-quality-review`: local complexity, duplication, error handling, API clarity, and unexplained indirection.
- `prismarine-architecture-review`: state ownership, package boundaries, extension points, consumer compatibility, and proposed refactors.
- `prismarine-protocol-data-review`: codecs, enum representation, generated data, protocol version boundaries, and extraction provenance.
- `prismarine-behavior-test-review`: lifecycle, asynchronous actions, geometry/physics/rendering, and tests of observable effects.

## Establish evidence before writing a finding

Trace a concrete input or event sequence through the changed code to a consequence. Inspect actual serializers, callers and tests where the premise depends on them. A small reproducer or focused test is useful when it distinguishes competing explanations. Never invent a passing test or turn an unavailable dependency into evidence of a bug.

A static counterexample can establish a defect when the supported input contract and failing path are clear; a runtime reproducer is not mandatory. Conversely, a failure conditional on unknown fixture contents or an unverified wire contract remains a question or limitation. Check retained paths affected by a changed shared contract, and name only the versions/files for which the alleged regression is established; a similar neighboring file may already have had that behavior.

Choose validation at the layer of the claim. A wire-format change needs real encoding/decoding evidence; an action claim may need a server-observed effect. Existing targeted coverage can be sufficient. Do not request an entire new fixture framework, every Minecraft version, or a broad test rewrite without showing the specific uncovered risk.

For red CI, identify the failing assertion and its relation to the change. Diagnose flaky infrastructure and pre-existing failures separately. Passing CI, a merged outcome, or silence from a maintainer does not establish correctness. Closed-unmerged may mean superseded or incorporated elsewhere rather than rejected.

Before keeping a finding, attempt to disprove it: check defaults, feature gates, supported-version boundaries, promise/event timing, later revisions, and replies correcting the premise. Separate an actionable defect, a necessary design change, and an optional improvement. A broader refactor is necessary only when a concrete contract or invariant cannot be preserved by the bounded fix. A supported local repair can land with follow-up work.

## Produce a useful review

For each finding, provide the triggering scenario, affected behavior, evidence and a bounded next step. Attach it to the smallest relevant changed range. Prefer one comment per root cause; do not scatter the same architectural concern across call sites. Label uncertainty and optional suggestions explicitly. If the available snapshot cannot establish the premise, record what remains unknown instead of asserting a defect.

Compare against existing inline threads and review summaries by **root cause and requested action**, not wording. Do not repost an unresolved prior finding, including an older Astra finding. A materially distinct issue on the same line can be new; explain the difference internally before publication. No new comment is a valid result and does not imply approval.

Publishing requires authorization from the task; this skill grants none. When authorized, refresh state, head and discussion immediately before posting, use a COMMENT review unless instructed otherwise, and verify the resulting review and inline locations. If the head changed, recheck affected findings. Check for successful partial publication before retrying an ambiguous error.

For this repository's Astra workflow, each review summary **and inline comment** must include:

> **Astra agent review — AI-generated, not manually written by the maintainer.**

Add a short truthful sentence naming the skills actually used and the check they contributed. This attribution/publication procedure is the user's operational requirement, not a mined historical maintainer preference. Never portray comments posted under a maintainer's account as manually authored without evidence.
