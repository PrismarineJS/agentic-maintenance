# Review submitted tests against repository standards

Date: 2026-10-03. Requested by rom1504 after manually reviewing the recommended merge candidates.

## Problem and evidence

The review skills already preferred existing harnesses, but Astra still called PRs ready on the strength of passing bespoke fixtures. This is an application failure as well as a wording gap: review must inspect how a test constructs its subject, not merely count passing assertions or import a real plugin.

Three current maintainer comments establish the scope:

- [Mineflayer #4053](https://github.com/PrismarineJS/mineflayer/pull/4053#discussion_r4174311961): replace the fabricated bot/client inventory test with an internal or external test. Its no-op writer and directly emitted decoded objects bypass actual initialization and packet handling.
- [Pathfinder #386](https://github.com/PrismarineJS/mineflayer-pathfinder/pull/386#discussion_r4174313991): compare the completely mocked bot with existing tests. Real A* does not validate the fabricated world/control/physics interfaces surrounding the plugin.
- [Chunk #338](https://github.com/PrismarineJS/prismarine-chunk/pull/338#discussion_r4174319033): do not introduce a dedicated test file for the new version. Its factory, block access and JSON assertions fit the existing shared column version matrix.

Inspect exact candidate sources and current discussion before applying these precedents. They do not prohibit focused unit tests, controlled algorithm inputs or all version-specific assertions. Physics simulation and chunk palette tests already use legitimate synthetic inputs to real production algorithms.

## Changes to the skills

Keep the seven existing skills. Put the cross-repository test-construction gate and concrete harness map in a common reference linked from the main review skill and relevant domain skills. Strengthen architecture review of parallel fixtures. Correct recipe wording that made diagnostic fake-bot probes sound like recommended submitted integration tests.

Before a readiness decision, record: the claim under test; subject construction and replaced boundaries; existing repository harness/matrix; runner and CI discovery; what the assertions actually establish; and any remaining maintainer request. For bot/plugin integration, reuse the existing real bot and NMP server harness. For a new chunk version sharing behavior, extend `test/versions.js` and `test/ChunkColumn.test.js`, keeping captured-packet fixture matrices distinct. Pure model tests remain appropriate for model claims.

A useful failing probe may demonstrate a bug without being suitable maintained regression coverage. Head/base differentiation and green CI do not clear that distinction. Do not demand tests for every cosmetic change or claim a runtime defect when the issue is fixture maintenance or validation quality.

## Validation and application

Validate changed skill structure and independently evaluate raw examples including legitimate synthetic model tests. Audit the fresh inventory of all public pending PrismarineJS and ProtoDef-io PRs, including drafts, against the updated skills. Read diffs and existing discussion for every PR; investigate candidate test additions and changed test infrastructure in detail. Keep a per-PR coverage ledger and distinguish no applicable testing change, acceptable coverage, already-covered objection, and new finding.

Use disjoint agent batches and refresh head/state/discussion immediately before authorized publication. Publish only concrete, nonduplicated findings as COMMENT reviews with changed-line anchors where available. Every summary and inline must identify Astra authorship, name the skills used and explain their contribution. The three source comments already communicate the maintainer's requests and should not receive redundant reviews.

Write the implementation report and audit evidence under `implementation/phase3/`, then commit and push the design, skills and report using the established workflow. Exclude unrelated existing drafts. Record actual test execution and limits; a source/discussion audit is not a claim that all test suites ran.
