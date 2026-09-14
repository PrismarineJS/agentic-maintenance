# U9G review with the revised domain skills

Date: 2026-09-14. Completed: `2026-09-14T15:55:26.832627+00:00`. Source: fresh GitHub heads, diffs and complete paginated discussions, exact-head/base application source and focused local probes. Skills frozen at [`74bea29`](https://github.com/PrismarineJS/agentic-maintenance/commit/74bea29).

**54 PRs reviewed by ten distinct agents: four new inline comments, 50 PRs with no additional comment.** Final GitHub checks confirm all 54 remain open and unmerged, with unchanged reviewed heads and bases. No PRs were missed or added during the pass. No-new-comment means no additional supported feedback; it does not mean approval or that earlier blockers are resolved.

## New comments

| PR and inline review | Finding | Evidence |
| --- | --- | --- |
| [mineflayer #4063](https://github.com/PrismarineJS/mineflayer/pull/4063#discussion_r4006809187) | Clearing controls with physics disabled leaves the server sprinting. | Actual 1.21.4 NMP client/server: head omits the stop action, base sends it. |
| [mineflayer-pathfinder #377](https://github.com/PrismarineJS/mineflayer-pathfinder/pull/377#discussion_r4006928824) | Stopping and immediately restarting the same walk returns the cancelled promise. | Actual controller with bot/planner adapter: head rejects; base restarts; active joins and later restarts work. |
| [prismarine-item #184](https://github.com/PrismarineJS/prismarine-item/pull/184#discussion_r4006823197) | A configured enchantment absent from static data throws before the zero-hash fallback. | Compiled registry/item packets on 1.21.5 and 1.21.11; ordinary enchantments hash successfully. |
| [prismarine-viewer #484](https://github.com/PrismarineJS/prismarine-viewer/pull/484#discussion_r4006969200) | A delayed old-world column removal deletes replacement-world geometry. | Production renderer and real THREE with controlled loads/replies: head disposes new mesh; base retains it. |

Each finding was sent to the coordinator for a source/evidence and semantic-duplicate check before publication. The coordinator reran the item, pathfinder and viewer probes, and inspected the actual movement test and its head/base logs. Every published review is `COMMENTED`, attached to the reviewed commit and a changed line, and verified to contain the exact Astra AI-authorship marker plus truthful new-skill contributions in both summary and inline text. No approvals, merges, closures or formal request-changes reviews were made.

## Coverage

The environment permits three concurrent review workers. Ten agents ran in batches with disjoint assignments; each read the common workflow and selected new domain skills. Prior phase2 and phase3 records, corrections and all current discussion were supplied explicitly. This is a maintenance review, not a blinded skill benchmark.

| Agent batch | Reviewed | New comments |
| --- | ---: | ---: |
| hashing | 4 | 1 |
| movement | 6 | 1 |
| viewer_core | 4 | 0 |
| interactions | 6 | 0 |
| bot_lifecycle | 7 | 0 |
| bot_tests_scoreboard | 6 | 0 |
| pathfinder_physics | 5 | 1 |
| protocol_diagnostics | 5 | 0 |
| data_generation | 5 | 0 |
| viewer_stack_items | 6 | 1 |

All PR heads were unchanged from the previous pass. The new domain skills directed additional checks at concrete boundaries: simulation versus sent state, static versus negotiated registries, cancellation versus pending promise cleanup, and world generations versus deferred work. Other focused checks covered supported-version selectors, real compiled mapper behavior, action sequences, window/cursor state, item text, effective reach, physics branches, geometry, Host contracts and mesher inputs. Exact checks and limitations are recorded per PR.

## Duplicate decisions and limits

The initial snapshots contained 106 inline comments. Agents compared findings against inline threads, review summaries and issue comments by root cause and requested action, including human feedback and both previous Astra passes. The four published inline IDs are new and were independently audited; new wording or skill attribution was never sufficient reason to repost.

- The old numeric-hand and numeric-respawn objections remain disproved by production compiled codecs and were not revived. Existing mapper-preservation comments remain applicable to named writes.
- Data #1278 also has a maintained-YAML/generated-JSON mismatch. That evidence was recorded without another inline comment: restoring the mapper as already requested also restores source agreement.
- Existing partial-shape, reach-clamp, world-load, invisible-entity, unsupported-item, Host-type, recipe-remainder and lifecycle concerns were checked and retained in the records without duplicating their threads.
- The data agent found a limitation in the skill recipe: installed `prismarine-recipe@1.5.0` reads `recipe.inShape` inside `applyShape` even for output shapes. Delta totals therefore cannot establish a newly introduced loss of bucket remainders. The review uses actual `outShape` and Mineflayer collection behavior; the existing public cake comments remain supported. Skills were not changed during this pass.

Tests used actual production code and available dependency versions, with controlled providers, clocks, packets or worker responses where appropriate. Real NMP client/server tests establish packet behavior, not vanilla-server acceptance. No live vanilla-server or browser/WebGL run was performed. The Java recipe generator was not executed; its generated outputs were exercised through consumers. Focused tests do not constitute a full application/version matrix. Passing focused tests and four additional findings do not establish a general skill accuracy rate.

## Records

- [Per-PR review records](u9g_domain_rereviews.json): current heads/outcomes, selected skills and their contributions, prior feedback, checks/limits, decisions and exact posted text/URLs.
- [Execution and coordinator checks](u9g_domain_execution.json): ten worker identities, result/skill hashes, counts and the withheld proposal.
- [Publication audit](u9g_domain_publication_audit.json): remote review state, commit, attribution, changed-line locations and zero verification errors.
- [Initial/final census](u9g_domain_census.json): baseline discussion IDs and final GitHub heads, bases and merge states.

The previous survey/review artifacts and the three pre-existing untracked phase2 drafts are preserved. Application source repositories and global skill installation were not changed.
