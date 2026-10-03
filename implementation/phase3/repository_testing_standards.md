# Repository testing standards and pending-PR audit

2026-10-03. Design: [repository_testing_standards.md](../../design/phase3/repository_testing_standards.md).

## What changed and why

rom1504's comments on [Mineflayer #4053](https://github.com/PrismarineJS/mineflayer/pull/4053#discussion_r4174311961), [pathfinder #386](https://github.com/PrismarineJS/mineflayer-pathfinder/pull/386#discussion_r4174313991), and [chunk #338](https://github.com/PrismarineJS/prismarine-chunk/pull/338#discussion_r4174319033) exposed an error in the earlier readiness reviews: passing bespoke tests were accepted without adequately checking fixture construction and repository conventions. Existing skills said to prefer the real harness, but that guidance was not enforced as a readiness condition.

The seven existing skills now share a required [testing review gate](../../skills/prismarine-review/references/testing_standards.md). It checks the claim, actual subject construction, later overrides, repository harness/version matrices, runner/CI discovery, assertion sensitivity and outstanding maintainer requests. Architecture and domain entrypoints route to the gate. Lifecycle and geometry recipes now label isolated fake-bot probes as diagnostic evidence rather than recommended submitted integration regressions.

The concrete routes are Mineflayer's real-bot internal/external suites, pathfinder's real-bot event/control suite, and chunk's shared `test/versions.js` → `ChunkColumn.test.js` matrix. Captured network-fixture matrices remain separate. Pure physics, palette, helper and path-algorithm tests remain legitimate; the module being exposed through a plugin is not itself an integration claim.

## Coverage and results

Eight subagents assisted: seven disjoint audit batches, plus an independent skill evaluator who also checked large protocol cases. A completed reviewer additionally peer-checked disputed findings. The fresh public inventory contained **476 pending PRs across 77 repositories**, including drafts and old dependency PRs. A final census at 18:51 UTC found the same 476, with no newly opened or closed PRs since collection. Each record retains its reviewed head/base and scope.

| Testing-audit outcome | PRs |
|---|---:|
| New actionable feedback posted | 25 |
| Existing relevant feedback retained without duplication | 64 |
| Submitted tests appropriate for their bounded claim | 112 |
| No applicable testing change/problem in this audit scope | 275 |
| Total | 476 |

These are testing-scope outcomes, not 451 new merge recommendations. The audit examined diffs, discussion and test-related surfaces, then candidate test setup, adjacent harnesses and workflows where relevant. It did not rerun all suites or exhaustively re-audit production implementations, generated datasets or binaries. Large rewrites such as bedrock-protocol #784 retain explicit limits in the ledger.

We posted **26 COMMENT reviews containing 28 inline comments**. After peer correction, **25 PRs retain 27 new actionable inline findings**. Every summary and inline identifies Astra authorship, names the skills used and explains their contribution. Publication refreshed live head/state/discussion, checked existing root causes and requested actions, and verified the final posted text and anchors by API read-back. The three triggering maintainer comments were not duplicated.

## New actionable feedback

| PR | Testing repair |
|---|---|
| [minecraft-data #1075](https://github.com/PrismarineJS/minecraft-data/pull/1075#pullrequestreview-5402180264) | Run new helper-bot tests in PR CI. |
| [mineflayer #3902](https://github.com/PrismarineJS/mineflayer/pull/3902#pullrequestreview-5402189208) | Preserve server-driven inventory-clear synchronization in test helpers. |
| [mineflayer #4051](https://github.com/PrismarineJS/mineflayer/pull/4051#pullrequestreview-5402206890) | Use the existing resource-pack integration harness and include new cases in CI. |
| [mineflayer #4089](https://github.com/PrismarineJS/mineflayer/pull/4089#pullrequestreview-5402192215) | Observe real server-received interaction packets instead of discarding encoded bytes. |
| [mineflayer #4094](https://github.com/PrismarineJS/mineflayer/pull/4094#pullrequestreview-5402205355) | Preserve the actual packet writer in packet-order regressions. |
| [mineflayer #4115](https://github.com/PrismarineJS/mineflayer/pull/4115#pullrequestreview-5402208400) | Use the existing real-bot placement harness and include regressions in CI. |
| [mineflayer #4133](https://github.com/PrismarineJS/mineflayer/pull/4133#pullrequestreview-5402209607) | Include the focused algorithm regression in CI version filtering or an unfiltered unit job. |
| [mineflayer #4136](https://github.com/PrismarineJS/mineflayer/pull/4136#pullrequestreview-5402223701) | Repair the configuration regression that stays green with decoder errors and removed cleanup. |
| [mineflayer #4149](https://github.com/PrismarineJS/mineflayer/pull/4149#pullrequestreview-5402212677) | Include chat-pattern regression in the existing versioned CI harness. |
| [mineflayer #4150](https://github.com/PrismarineJS/mineflayer/pull/4150#pullrequestreview-5402176310) | Use the real-bot bed harness and include the timeout regression in CI. |
| [mineflayer #4151](https://github.com/PrismarineJS/mineflayer/pull/4151#pullrequestreview-5402211061) | Keep real writes and server-driven spawn events in boat regression coverage. |
| [mineflayer #4153](https://github.com/PrismarineJS/mineflayer/pull/4153#pullrequestreview-5402186178) | Use actual title packets in the versioned real-bot harness. |
| [mineflayer #4155](https://github.com/PrismarineJS/mineflayer/pull/4155#pullrequestreview-5402218040) | Use the established book/inventory harness and include new cases in CI. |
| [mineflayer #4156](https://github.com/PrismarineJS/mineflayer/pull/4156#pullrequestreview-5402187637) | Use the real-bot bed harness and include the timeout regression in CI if this duplicate is retained. |
| [mineflayer #4157](https://github.com/PrismarineJS/mineflayer/pull/4157#pullrequestreview-5402213976) | Exercise real registry/configuration initialization in time regressions. |
| [mineflayer-cmd #86](https://github.com/PrismarineJS/mineflayer-cmd/pull/86#pullrequestreview-5402193738) | Run new tests in CI and assert permitted-command execution before clearing observations. |
| [mineflayer-collectblock #145](https://github.com/PrismarineJS/mineflayer-collectblock/pull/145#pullrequestreview-5402198879) | Run new callback regressions in CI. |
| [node-minecraft-data #457](https://github.com/PrismarineJS/node-minecraft-data/pull/457#pullrequestreview-5402178973) | Assert tags preservation even when the loader output is absent; do not silently skip the regression. |
| [node-minecraft-protocol #1495](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1495#pullrequestreview-5402244938) | Include the new unversioned regression suite in CI. |
| [node-minecraft-protocol #1528](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1528#pullrequestreview-5402247641) | Include the new unversioned regression suite in CI. |
| [node-minecraft-protocol #1536](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1536#pullrequestreview-5402190476) | Make the index-zero regression distinguish broken dispatch and run the suite in CI. |
| [node-minecraft-protocol #1537](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1537#pullrequestreview-5402230669) | Repair current-base signedChat feature selection in fixtures and run the suite in CI. |
| [node-minecraft-protocol #1539](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1539#pullrequestreview-5402250663) | Include the new unversioned regression suite in CI. |
| [prismarine-registry #57](https://github.com/PrismarineJS/prismarine-registry/pull/57#pullrequestreview-5402224649) | Restore comparison of the complete item palette in the roundtrip test. |
| [prismarine-viewer #488](https://github.com/PrismarineJS/prismarine-viewer/pull/488#pullrequestreview-5402216449) | Ensure CI selects the new scheduling/meshing regressions. |

## Checks and refinements

All seven skills pass `quick_validate.py`; 36 local links in changed skill/design Markdown resolve; `git diff --check` passes. The initial independent evaluation covered seven cases: the three manual objections and four legitimate model/real-bot controls. A second evaluation checked pathfinder #384, NMP #1536 and registry #57 against raw source/runner evidence. These are regression/precision checks, not a measured unseen-case accuracy benchmark.

Peer review found and corrected two overgeneralizations:

- [Pathfinder #384](https://github.com/PrismarineJS/mineflayer-pathfinder/pull/384#pullrequestreview-5402200645): withdrew the real-bot migration request in place. Its actual `getPathFromTo` raw-versus-processed waypoint assertions are focused algorithm tests. The revised skill explicitly preserves this case. The withdrawal does not independently approve the entire PR.
- [NMP #1536](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1536#pullrequestreview-5402190476): removed the blanket network-fixture demand from the first inline and summary. Existing package conventions permit local decoded-dispatch unit tests. Its CI omission and ineffective index-zero assertion remain concrete findings.

Targeted execution strengthened several findings:

- Node-minecraft-data #457: the real candidate loader's output guard passes both with and without tags passthrough; an explicit preservation assertion distinguishes the broken control.
- NMP #1536: both submitted tests pass with the fixed guard and with broken `if (index)`, demonstrating the missed index-zero behavior.
- NMP #1495/#1528/#1539: focused suites pass 3/38/11 tests unfiltered; CI-style `-g 1.21.4v` selects zero in each.
- Mineflayer #4149/#4155: dry-run under the CI version filter selects zero new tests.
- Mineflayer #4136: the focused 1.21.4 case reports one passing test while logging a decoder error; removing the intended cleanup still passes. This was repeated with candidate-declared dependencies (minecraft-data 3.117.0, NMP 1.68.0, chunk 1.41.0), after checking the earlier reused dependency set. Production edits used for the control were restored.
- NMP #1537: retained the separately established current-base integration evidence that the stale feature stub misses `signedChat`; the review distinguishes test-fixture failure from production behavior.

Most other conclusions are exact-head source/discussion/runner inspections, not new test runs. The per-PR ledger records actual commands, dependencies, observations and limitations. Temporary workspace evidence paths in those records are provenance, not installed-skill dependencies or promised permanent artifacts.

## Tracking and artifacts

The [central table](https://github.com/PrismarineJS/prismarine-contribute/issues/18) was updated with testing follow-up links, seven formerly ready PRs requiring author changes, seven additional merges and one closure. Its original 491-row scope now contains 474 pending, 16 merged and one closed-unmerged PR. The fresh 476-PR audit additionally includes minecraft-data #1333 and pathfinder #395; neither warranted a new testing finding. The original table now has 137 ready entries under its prior overall assessments; this testing audit is not a fresh full approval of those entries.

- [Per-PR audit ledger](repository_testing_audit.json): all 476 rows, heads, evidence, execution limits and review links.
- [Skill evaluation and validation](repository_testing_skill_evaluation.json): structural validation, independent cases, peer checks, corrections and tracking counts.
- [Common testing guidance](../../skills/prismarine-review/references/testing_standards.md).

The design, skills and report follow the established commit/push workflow. Unrelated pre-existing `design/phase2/` drafts were excluded. No application code was committed, and no PR was merged, closed or formally approved by this audit.
