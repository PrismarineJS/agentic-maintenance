# Phase3: historical review survey and review skills

Date: 2026-09-14. Source: GitHub PRs and discussions retrieved for the frozen survey, plus separately recorded foundational issues and contribution documents. Status: all 500 cases accounted for; five skills written, evaluated and refined. The authorized U9G re-review is also complete, with ten distinct subagents and verified public comments.

## Scope and outcomes

Surveyed **500 selected PR discussions across 17 repositories** in the four-year window 2022-09-14 through 2026-09-14. Selection balanced repository, year and outcome within a 977-PR target-reviewer search pool. These are not the literal latest 500 or a random sample of all PRs.

| Captured outcome | PRs |
| --- | ---: |
| Merged | 250 |
| Closed without merge | 183 |
| Still open | 67 |
| Total | 500 |

The four primary repositories contribute 400 cases: Mineflayer 152, minecraft-data 140, node-minecraft-protocol 95, and node-protodef 13. Thirteen adjacent repositories contribute 100. The independent analysis split is 400 discovery and 100 heldout, not the same as the primary/adjacent allocation. Discovery contains 198 merged, 151 closed-unmerged, and 51 open cases.

The target-account participation counts are rom1504 298, extremeheat 308, and Karang zero; counts overlap. Both commenter and reviewed-by search qualifiers were checked. Older Karang architecture comments were read as separately dated foundational context, not silently added to the four-year PR sample. Thirty curated foundational source records include contribution guidance, current pins and other relevant authored issues.

Every selected PR has an explicit merged boolean, merge/closure dates, outcome, retrieval metadata and source links. A closed PR can have been superseded or incorporated elsewhere, and a merge does not establish that every concern was resolved. The [manifest](survey_manifest.json), [case records](review_cases.jsonl), and [collection summary](collection_summary.json) preserve those distinctions.

## What was produced

Five reusable skills live in the repository's top-level `skills/`:

| Skill | Purpose |
| --- | --- |
| [prismarine-review](../../skills/prismarine-review/SKILL.md) | Common workflow: contracts, evidence, current revisions, dependency readiness, proportional findings and nonduplicate publication. |
| [prismarine-code-quality-review](../../skills/prismarine-code-quality-review/SKILL.md) | Useful abstractions, clear public APIs, understandable branches, error/completion ownership, and measured performance claims. |
| [prismarine-architecture-review](../../skills/prismarine-architecture-review/SKILL.md) | Package responsibility, shared mutable state, consumer propagation, extension contracts, and when broader refactoring is necessary. |
| [prismarine-protocol-data-review](../../skills/prismarine-protocol-data-review/SKILL.md) | Source/generated data, codecs, named versus numeric representations, actual version boundaries, and consumer migration. |
| [prismarine-behavior-test-review](../../skills/prismarine-behavior-test-review/SKILL.md) | Observable behavior, test oracles, fixture provenance, synchronization/lifecycle, and appropriate validation layers. |

They are review aids with conditional checks and counterexamples. They are not installed globally and do not grant permission to publish reviews. [Principles and examples](principles.md) explain the source basis. The user's Astra attribution and nonduplicate-publication requirements are identified separately from mined historical preferences.

The strongest practical lessons are to trace an actual owner and consumer before proposing a refactor, test the claim with an appropriate observable result, preserve meaningful version/wire differences, and correct an objection when replies or implementation evidence disprove its premise. The corpus also shows explicit acceptance of limited fixes and follow-up tests. Broad architecture work is required when the local fix leaves the same invariant broken; it is not a default tax on every PR.

## Execution and validation

The 20-case discovery pilot exposed the need to add review-thread resolution metadata and preserve manual-authorship uncertainty. Work then proceeded with the coordinator and three subagents. The coordinator curated 125 cases; the other analysts curated 100, 100 and 75. Packet preparation work was balanced by transferring 25 discovery cases back to the coordinator. Nine consequential cases from the other analysts were independently checked against target comments, including retractions and disagreements. This was a targeted reconciliation check, not a formal inter-rater study.

The collector retrieved 802 review submissions, 833 inline comments, 1,702 issue-conversation comments, 3,049 changed-file records, 2,254 commits and 448 review threads. All selected endpoint requests completed after a GitHub rate-limit reset and recovery of missing fields. Fifty-seven cases have omitted/binary API patches, five have empty final changed-file lists, and large patches can be truncated. Current-head checks/status are not historical CI logs. These limits prevent claiming 500 complete executable code audits.

Account attribution is verified, while manual authorship is usually undisclosed. Forty-two target-account records explicitly disclose agent generation and three contain attributed agent material in mixed text. Fourteen PRs have only explicitly agent-attributed target content. They remain operational controls and do not supply independent human lessons. Bulk discussions, quoted email tails and raw executable historical packets remain outside Git; tracked evidence uses paraphrases and permalinks.

All five skill files pass the skill-creator validator. Referenced PR comment anchors were checked against the collected discussion metadata. The initial skill contents and hashes are frozen in [evaluation/skills-initial.json](evaluation/skills-initial.json). Evaluation uses fresh agents with matched inherited model configuration, identical code packets and declared limits, with source/history access restricted by task instructions. The exact serving-model identifier and token usage are not independently observable.

## Evaluation

Historical reconstruction produced 45 usable packets: 36 initial and nine confirmation. Forty-one have cumulative patches at explicit review revisions; four contain original inline hunks. The remaining 55 are contextual cases, excluded from code-review scores. Eight potentially related packets were quarantined before evaluation. A later audit found two confirmation PRs already reviewed during phase2; they are additionally excluded from a transparently post-hoc clean comparison. Original results are retained. This leaves 35 clean packets overall, with only six cumulative and one hunk-only case in confirmation. Title/direct-link screening can miss relationships; prior-review archives must also be checked before future selection.

Ten fresh review agents produced 90 paired predictions; four separate adjudicators then completed the 100 heldout case analyses. On 27 comparable initial cumulative snapshots, both arms produced 18 supported actionable concerns, while uncertain proposals fell from four to one with skills. The baseline found one additional valid issue in a separate hunk-only case. Initial feedback led to specific refinements in static-evidence calibration, version scope, fixtures/CI, numeric encoding evidence and validation exemptions.

After freezing the revised skills, both arms found the same three supported concerns in the six clean cumulative confirmation cases, all in one PR, and abstained on the clean hunk-only case. No independent actionable historical-reference denominator exists for confirmation. This is encouraging but limited evidence for review aids, not proof of universally better recall or faster reviews. The [evaluation report](evaluation.md) includes original and exposure-adjusted results, counterexamples, timing limits and the unchanged final skill hash.

Corpus/outcome checks pass for all 500 cases. Both paired prediction audits pass; all five final skills validate and match their frozen contents. A separate agent independently reproduced initial metric arithmetic and checked every prediction location across both stages. It found two adjacent context anchors and one baseline line outside a displayed hunk; historical predictions were never posted. The actual publication workflow must verify locations independently. All execution scripts were syntax-checked and exercised in the relevant collection, normalization, evaluation or audit pipeline; no application code changed or historical integration suite was claimed to run.

## U9G review pass and commits

Committed the design, 500-case survey, evaluated skills and report first as `cdfb9bf88c945d934176ecc873d4dc9e4d897820` on 2026-09-14 at 09:29:41 UTC. The subsequent authorized review used the frozen skills and ten distinct subagents, with up to three active workers. Nine workers covered ten domain batches; one handled both hashing and interactions after a transient worker-creation limit. The tenth independently re-reviewed five consequential findings/corrections. Those five overlap the 54 unique pending PRs.

| Publication outcome | PRs |
| --- | ---: |
| New inline COMMENT review | 8 |
| Corrective reply withdrawing an earlier finding | 2 |
| No additional public comment | 44 |
| Total reviewed | 54 |

All 54 were still open and unmerged in the final census. Eight new reviews contain eight inline findings: legacy sneak dependency compatibility, partial-block raycast geometry, effective interaction-range bounds, final-step bridge completion, protocol API declarations, flying in fluids, missing item-texture fallback, and the viewer Host declaration. Each review summary and inline comment identifies Astra and explains the actual skills used. The two corrective replies do the same in the original threads.

Production codec validation disproved the earlier Mineflayer #4086 and #4089 numeric-mapper objections: released NMP uses compiled ProtoDef, which accepts the numeric values that the isolated interpreter rejected. Both findings were explicitly withdrawn. This also exposed an execution gap: the initial interaction re-review retained the isolated-codec objection until cross-batch evidence corrected it. The skills already require checking the actual codec path; their evaluated contents were kept frozen. The live pass is operational evidence, not another blinded or causal comparison.

The coordinator independently checked selected reproductions and all eight new reviews' remote COMMENTED state, commit, inline path/line, attribution and skill names. Both corrective replies were verified against their original thread IDs and bodies. The tenth agent independently supported both withdrawals and three selected new findings using actual client packet paths, compiler resolution and real rendering objects. No further correction arose from those five cross-checks.

The [PR-by-PR report](u9g_rereviews.md), [complete records](u9g_rereviews.json), [execution metadata](u9g_execution.json), [publication audit](u9g_publication_audit.json), [corrections](u9g_corrections.json), [independent checks](u9g_independent_checks.json), and [final census](u9g_final_census.json) preserve details and validation limits. A [runnable codec-path example](reproductions/README.md) preserves the cause of the withdrawn findings. A no-new-comment decision is not an approval; existing unresolved concerns can remain. Application repositories were not changed, approved, merged or closed by this work.

The final execution records and report update are committed separately after the prerequisite commit. The [final validation record](u9g_validation.json) also confirms that all 54 remote heads remained unchanged at completion. Validation covers the unchanged 500-case accounting and frozen skill files, all 54 assigned PR identities, all 10 distinct participating subagents, all 8 newly published reviews and both corrective replies. The three pre-existing untracked phase2 design files remain outside these commits.
