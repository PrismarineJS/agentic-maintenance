# Review skills updated from extremeheat's judgments

Date: 2026-09-21. Starting commit: `7a6980b`. Implements the [design](../../design/phase3/extremeheat_review_standards.md) written before the skill edits.

## Changes

Strengthened four existing skills without adding another generic skill:

| Skill | Decision that changes |
|---|---|
| Common review | Assess correctness, maintainability/package fit and validation/release readiness separately. Treat extremeheat's applicable direct requests as the trusted standard selected by the maintainer. Passing tests or an earlier Astra review do not dismiss an unresolved design request. |
| Architecture | Concrete duplicated protocol work, misplaced ownership or unnecessary fixture complexity can require a bounded repair even without a reproduced runtime bug. Keep the loader generic, compare existing plugin structure, check ProtoDef sizing/writing dependencies, and evaluate optimizations against actual costs and browser consumers. |
| Protocol/data | Distinguish data inconsistency from real wire changes before adding flags; preserve semantic consumer names; generalize schema checks at the appropriate owner; repair active generators; check both NMP sides and coordinate version integration branches. |
| Lifecycle/actions | Prefer the existing real bot/NMP client-server fixture for packet-driven behavior while retaining pure-model tests and controlled fault isolation for the claims they actually establish. |

Two linked references supply the concrete maintainer examples and packet-test selection matrix. Existing domain probes, correction records and all 500 historical survey cases remain unchanged. README navigation points to this revision.

## Source basis

This is a targeted update, not another full survey. The preceding investigation fetched August–September 2026 extremeheat comments/reviews from 80 recently active candidate PRs across PrismarineJS and ProtoDef-io, then compared them with the current skills. It checked the code context of selected inline comments before generalizing them. The search is not an exhaustive census of all review-only participation.

For this implementation, six older comment/review records were fetched directly from GitHub after locating them in the existing survey. Three provided useful additional evidence: data #1007's request to document generation, #1193's requirement to repair the generator, and #747's explicit approval despite missing semantic tests. The other fetched records were tentative discussion or an acknowledgement and did not add a rule. Exact links and dated outcome qualifications are in [the standards reference](../../skills/prismarine-architecture-review/references/extremeheat_standards.md).

The user's explicit trust in extremeheat supplies the preference authority. We do not count clearly labeled Astra/Codex posts as independent evidence of his preferences. Questions such as whether Zod might help are retained as design questions, not dependencies that every PR must adopt. Later owner decisions, such as keeping Mineflayer's loader generic in #4085, retain their actual attribution and precedence.

## Validation

- All seven skill-creator frontmatter/name validators passed.
- The existing artifact validator passed the unchanged 500-case corpus and seven active skills: 250 merged, 183 closed-unmerged and 67 open in the frozen historical snapshot. These are not today's PR counts.
- Relative Markdown links in the active skills and this revision's design/report/navigation were checked; none missing.
- `git diff --check` passed.
- Reviewed the following known cases against the revised instructions. This is an author-performed decision/consistency walkthrough, not an independent agent evaluation, new application test run or held-out accuracy benchmark.

| Case / control | Result of applying the instructions |
|---|---|
| Mineflayer #4114: repeated interaction code, passing behavior hypothetically retained | Raise the concrete maintenance cost and smallest shared implementation; no need to invent a runtime failure or demand the entire interaction redesign. |
| Mineflayer #4085: question about a new plugin followed by the owner's loader constraint | Preserve the later owner decision and choose the actual shared plugin/helper boundary; no blanket ban on plugins. |
| Mineflayer #4118 fake-bot packet test versus a pure attribute arithmetic test | Prefer the real NMP fixture for plugin behavior; retain the small model test for arithmetic. No indiscriminate vanilla-server requirement. |
| NMP #1521 acknowledgement behavior | Check affected production client and server paths, not just a helper's output; distinguish shared-schema roundtrips from independent wire evidence. |
| Data #1298 semantic rename versus a genuinely new packet | Preserve existing consumer names or coordinate normalization; do not suppress a real protocol difference merely for uniformity. |
| Data #1297 generic uniqueness versus unrelated registries reusing IDs | Exercise every schema/category promising that property; do not impose one global namespace or stop at blocks. |
| Data #1286 accepted local validation stopgap | Identify protodef-validator as the destination while allowing the explicitly accepted bounded fix to land. |
| NMP #1516 implicit disk caching versus an explicit Node-only optional facility | Assess measured benefit, existing memory reuse, platform compatibility and storage ownership; reject the demonstrated shared-library contract problem without banning every cache. |
| Data #1193 active generation versus a historical typo with no active producer | Repair/document the current extractor when regeneration would restore the defect; avoid demanding a replacement generator for an unrelated old correction. |
| Data #747 missing semantic test and Bedrock #810 tentative Zod suggestion | Preserve explicit approval and the tentative nature of the suggestion; neither becomes an automatic new blocker. |
| ProtoDef #177 sizing available to writers versus sizing that calls writing | Trace the dependency direction and shared extension contract; prefer a bounded compiler fix over per-call generation or datatype-specific injection. |

## Delivery scope

The design, skill edits, references, navigation and this report are the complete revision. The three pre-existing untracked phase2 drafts are excluded. No application repository, global skill installation or GitHub review comment was changed. No claim of measured review-accuracy improvement is made; that would require a separate independent evaluation.
