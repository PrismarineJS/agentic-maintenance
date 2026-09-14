# Phase3 U9G re-review brief

Authorized by rom1504: after historical survey, skill evaluation and commit, use ten subagents to re-review all pending U9G PRs and publish appropriate nonduplicate inline COMMENT reviews. This brief is preparation; the coordinator explicitly starts publication after that prerequisite.

## Sources and purpose

Read the actual assigned current-head diff, relevant surrounding code, ALL existing discussion/reviews, and relevant skill files under `/home/ai/prismarinejs/agentic-maintenance/skills/`. Skills cover core review, code quality, architecture, protocol/data and behavior/tests. Select only those that help the specific change. They are evidence-based review aids, not a requirement to demand every possible refactor/test.

The previous review log is `/home/ai/prismarinejs/agentic-maintenance/implementation/phase2/u9g_inline_reviews.json`. Read your assigned rows, including actual comments and validation. Pilot mineflayer4104 has one additional review at https://github.com/PrismarineJS/mineflayer/pull/4104#discussion_r4002946527 about `once` resourcePack listeners declining but fallback then accepting. Current snapshots are under `/tmp/prismarine-phase3/u9g/current/OWNER--REPO--NUMBER.json`; root fetched them on2026-09-14 but you must refresh state/head/discussion before publishing. Prior repro caches live under `/tmp/astra-inline-reviews/`, helpful starting evidence, never substitute for fresh verification.

PrismarineJS separates language-independent minecraft-data, Node wrapper/releases, generic ProtoDef, Minecraft protocol clients/servers, reusable state/models, and bots/viewers/controllers. Cross-package data representation and minimum installed dependency versions matter. Small packages/flat APIs are deliberate; justify any required extraction with actual ownership/reuse or correctness problems. Roadmaps are context, not automatic merge blockers. Code-quality feedback needs a concrete comprehension, maintenance, or API benefit, rather than a personal rewrite preference.

## Review and publication

Use an isolated checkout or temporary source tree for your batch under `/tmp/prismarine-phase3/u9g/work/<group>/` when executing code. Do not switch branches or modify the existing shared Mineflayer checkout, other agents' worktrees, the committed skills, or application repositories. Reuse read-only caches where useful; install dependencies only in your isolated tree. Persist your own result file after each PR.

- Re-read current remote head and all discussions. Do not re-post an existing human or Astra concern, even with prettier wording or new skill names. Follow-up only when new evidence materially changes the issue, and prefer the existing thread when appropriate.
- Verify each suspected defect on actual current code. Use focused reproductions where they resolve uncertainty; synthetic stubs can misrepresent packet codecs, event ordering, geometry or lifecycle. Mark limits honestly; do not claim a suite/vanilla server ran if it did not.
- Review each PR against its actual base and declared dependencies. Do not invent a combined stack of other pending PRs; if a coordinated candidate stack is necessary, state exactly which revisions you exercised and keep its findings distinct from standalone behavior.
- A documented intentional API change, unrelated CI failure, already-merged dependency PR, small private helper or missing broad integration infrastructure alone is not a proved blocker.
- Assess current behavior, cross-version semantics and concrete code quality/architecture. A suggested design needs a specific failing invariant or substantial maintenance benefit; distinguish optional improvement from necessary change. There is no comment quota. A no-new-comment result with rationale is a successful review.
- Map the proposed inline line against both the current diff and source; prefer the exact changed line responsible for the finding over an adjacent unchanged line. A valid source line is not necessarily present in the PR diff.
- Publish only justified actionable findings, as GitHub inline `COMMENT` reviews at relevant changed lines and the reviewed commit. Do not approve, merge, close, request changes formally, or post general issue comments.
- Every review summary AND every inline comment begins exactly:
  **Astra agent review — AI-generated, not manually written by the maintainer.**
- Include a concise sentence identifying the actual skill(s) used and how they contributed. For example, `Skills used: prismarine-protocol-data-review helped check the decoded enum against the real writer; prismarine-review helped separate this finding from existing feedback.` Use only truthful specific descriptions, not boilerplate claims.
- Before posting, check again that the head is unchanged, PR is open, and no equivalent comment arrived. If an API write returns an ambiguous failure, inspect remote reviews/comments before retrying to avoid duplicates.
- GitHub connector can publish PrismarineJS reviews; ProtoDef-io may return403, where authenticated `gh api --method POST repos/.../pulls/N/reviews --input exact-payload.json` is the authorized fallback. Use structured arguments or exact JSON files. Never interpolate review prose into shell commands.
- Verify published review state `COMMENTED`, attribution, actual inline paths/positions, and comment URLs. Persist results after every PR.

## Required result per PR

Repository, number, title, URL, reviewed head, retrieval time, state, merged boolean; skills actually read/used and contribution; checks performed and limits; previous feedback considered; new findings or reason for no new comment; any posted review ID/URL and every inline comment path/line/body/URL. Save in your assigned result file. No silent skips or changes outside assigned PRs.

Use a JSON array for the assigned results file, with one object per PR. Keep exact keys `repo`, `number`, `head`, `status` (`posted`, `no_new_comment`, `not_open`, or `blocked`), `reason`, `skills_used` (array of actual skill names), `skill_contributions` (object), `validation`, `limits`, `previous_feedback`, `review_id`/`review_url` (null when none), and `inline_comments` (array with body/path/line/side/URL/id when posted), plus title/URL/state/merged/retrieved_at. Write atomically and persist after each PR. Do not delete a completed record when updating the array.
