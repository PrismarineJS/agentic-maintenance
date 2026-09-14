# Survey historical reviews to build PrismarineJS review skills

Date: 2026-09-14. Status: survey, skill authoring, evaluation and the authorized U9G re-review executed; see the [phase3 report](../../implementation/phase3/report.md). This document preserves the plan and explicitly recorded execution adjustments.

Sources for this scoping investigation: the repository's phase2 review records, current PrismarineJS contribution documents, current pinned-issue metadata, and a small set of foundational issue discussions linked below. At the time of the scoping investigation, no historical PR corpus had been collected or classified and no skills had been written or installed. Execution results and deviations will be recorded under `implementation/phase3/`.

## Objective and scope

Survey 500 historical PRs and the relevant comments from **rom1504, extremeheat, and Karang** to build a few practical review skills. The skills should help an agent identify actionable problems, understand package ownership and compatibility, choose useful validation, and avoid unnecessary review demands. They should capture reasoning and exceptions rather than imitate a maintainer's writing style.

The working interpretation is **500 PRs total across repositories**, not 500 per repository. Use the four-year window **2022-09-14 through 2026-09-14**, frozen for this survey. Older foundational issues are a separate source of context and do not consume the 500-PR budget.

There is a selection tradeoff to make explicit: the literal 500 most recent PRs may be concentrated in the latest year. This design proposes a repository- and year-balanced selection of 500 so the survey actually covers the requested three to four years. Record that choice in the corpus manifest; do not describe the result as the literal latest 500. If the intended scope is instead 500 per repository or strictly the latest 500, revise this design before collection.

Primary repositories:

- `PrismarineJS/mineflayer`
- `PrismarineJS/minecraft-data`
- `PrismarineJS/node-minecraft-protocol`
- `ProtoDef-io/node-protodef`

Reserve roughly 400 PRs for those four repositories and 100 for adjacent packages. Choose the adjacent repositories after checking review activity and references: likely `prismarine-physics`, `prismarine-world`, `prismarine-chunk`, `prismarine-entity`, `prismarine-registry`, `prismarine-item`, `prismarine-chat`, `minecraft-data-generator`, `node-minecraft-data`, `mineflayer-pathfinder`, `prismarine-viewer`, and `flying-squid`. Include `ProtoDef-io/ProtoDef` when specification discussions explain implementation decisions. Do not assume these packages have equal review volume.

The survey does not change application code or merge PRs. The user separately authorized a subsequent re-review of pending U9G PRs with ten subagents, after the skills are evaluated and committed. That pass may publish justified, nonduplicate inline COMMENT reviews identifying Astra, the review skills used, and how they helped. A skill itself never grants publication permission.

## What the preliminary investigation establishes

These sources guide questions for the survey. They do not establish an exhaustive or unanimously agreed rulebook.

| Source inspected | Implication for the survey |
| --- | --- |
| [prismarine-contribute README](https://github.com/PrismarineJS/prismarine-contribute/blob/master/README.md) and [project/dependency overview](https://github.com/PrismarineJS/prismarine-contribute/blob/master/info.md) | Start with the division between language-independent data, its Node wrapper, protocol handling, reusable models, bots, and servers. Examine dependency release order and support for multiple Minecraft versions. Check dated tooling instructions against current repository practice. |
| [rom1504 on repository organization](https://github.com/PrismarineJS/prismarine-contribute/issues/15#issuecomment-1575661657) | Independent packages are an intentional design choice. Investigate the concrete reuse and dependency reasons behind ownership comments; do not turn that preference into a requirement to extract every helper. |
| Pinned [mineflayer #334](https://github.com/PrismarineJS/mineflayer/issues/334), especially the [2022 state-ownership proposal](https://github.com/PrismarineJS/mineflayer/issues/334#issuecomment-1030719439), and pinned [prismarine-world #64](https://github.com/PrismarineJS/prismarine-world/issues/64) | Shared state and independently testable world behavior are longstanding goals. The original async proposal and later sync direction also demonstrate why chronology matters. A roadmap is not automatically a prerequisite for every smaller fix. |
| Pinned [prismarine-physics #21](https://github.com/PrismarineJS/prismarine-physics/issues/21), [generator #13](https://github.com/PrismarineJS/minecraft-data-generator/issues/13), and [prismarine-contribute #2](https://github.com/PrismarineJS/prismarine-contribute/issues/2) | Investigate tests of missing/partial state and semantic validation of generated data, alongside ordinary success cases. |
| [minecraft-data #500](https://github.com/PrismarineJS/minecraft-data/issues/500) | Data extraction and repeatable updates are explicit maintenance goals. This is an authored issue, not a current pin. |
| [mineflayer #3271](https://github.com/PrismarineJS/mineflayer/issues/3271) and [prismarine-contribute #4](https://github.com/PrismarineJS/prismarine-contribute/issues/4) | Existing test infrastructure and support for different server implementations matter. Examine which test layer a particular review actually requires. |
| [minecraft-data #1294](https://github.com/PrismarineJS/minecraft-data/issues/1294), by extremeheat | Named-enum consistency is an explicit direction in this discussion. Study wire representation, consumer compatibility, and removal of representation-only version branches separately. |
| [prismarine-contribute #17](https://github.com/PrismarineJS/prismarine-contribute/issues/17) and pinned [mineflayer #3859](https://github.com/PrismarineJS/mineflayer/issues/3859) | AI assistance is welcomed, but account identity does not establish human authorship. The pinned roadmap explicitly identifies itself as Claude-generated. Use its links to find primary discussions, not as independent evidence of manually expressed preferences. |

The pin lookup also found rom1504's protocol issues [#372](https://github.com/PrismarineJS/node-minecraft-protocol/issues/372) and [#1337](https://github.com/PrismarineJS/node-minecraft-protocol/issues/1337), and flying-squid [#392](https://github.com/PrismarineJS/flying-squid/issues/392) and [#432](https://github.com/PrismarineJS/flying-squid/issues/432). Their discussion contents remain future survey work. No pinned issues were returned for `minecraft-data` or `node-protodef` at this lookup. Record authorship and pinned status separately, with retrieval time; a pin is a priority signal, not proof of a settled decision.

This scoping pass does not establish Karang's review patterns. The survey must retrieve and attribute that evidence rather than infer his views from the other maintainers.

## 1. Discover and freeze the corpus

Once the survey is explicitly started:

1. Perform a metadata-only inventory across the proposed repositories and time window. Keep PRs separate from issues. Include merged, closed-unmerged, and still-open PRs, with their states recorded at the cutoff. Record an explicit `merged` boolean, `merged_at`, `closed_at`, and the separate outcome `merged`, `closed_unmerged`, or `open`; retain retrieval time and report any later state changes separately.
2. Discover reviewer participation using both `reviewed-by:` and `commenter:` searches where available, then verify against review submissions, inline comments, and issue-conversation comments. Neither search alone is an adequate participation index. Normalize login casing and retain account IDs; mentions of a maintainer are not comments by that maintainer.
3. Split searches by repository and time interval when GitHub's result cap requires it; paginate every selected discussion. Log unavailable, deleted, and truncated records instead of silently treating them as empty.
4. Allocate the 500 slots after inspecting availability. Preserve representation of repositories, years, reviewers, change types, and outcomes. Include routine successful reviews and positive comments as well as objections, abandoned proposals, and revisions. Do not select only heavily discussed or rejected PRs. Give small repositories their available qualifying cases and document redistribution; do not silently extend the date window to fill a quota.
5. Use a deterministic selection within those groups, with a saved seed/order and inclusion reason for every PR. Report the candidate pool, selected counts, and gaps by repository/year/reviewer. If fewer than 500 suitable PRs exist, report the shortfall rather than inventing coverage.

Prefer substantive participation by at least one target maintainer, while explicitly reserving a comparison group of routine, low-comment or approval-only PRs. Those cases do not establish detailed principles, and absence of objections does not establish correctness. PRs whose only target-account participation is explicitly agent-generated belong in supplemental operational evidence, not the human-review learning group. Link dependent, stacked, cherry-picked, or reverted PRs into families so repeated discussion of one problem is not counted as several independent examples.

Freeze a manifest before detailed analysis. Separate **400 discovery cases** from **100 held-out evaluation cases**, keeping related PR families together. Reserve 80 of the held-out cases for the initial comparison and 20 for untouched confirmation after any revisions. Stratify these sets where the available history permits it. The synthesis process must not read the relevant held-out maintainer comments or later fixes before the skills and evaluation predictions are frozen.

## 2. Collect a complete review case, not isolated quotations

For every selected PR, collect its description, commit history, changed files, review submissions, inline threads, issue-conversation comments, and relevant CI/release information. Read replies from contributors and other reviewers when they explain acceptance, disagreement, or correction. Follow linked issues/PRs when necessary to understand the decision, with supplemental context labeled separately from the 500 selected cases.

Use the following evidence record:

| Field group | Required information |
| --- | --- |
| Identity | Repository, PR number/URL, dates, author, state, explicit merged boolean and merge date, closed date, outcome, corpus group, related PR family. |
| Revision | Relevant base/head SHAs, review commit, original inline commit/path/hunk, and later resolving revision when identifiable. |
| Source | Comment/review IDs and permalinks, account ID/login, timestamps, current resolution/dismissal state, authorship label. |
| Reasoning | Requested change or positive observation, triggering code/scenario, rationale, proposed validation, package/API/version scope. |
| Response and outcome | Contributor response, implementation change, unresolved disagreement, merge/closure/revert, dependency/release follow-up, uncertainty. |
| Candidate lesson | Conditional rule, counterexample or exception, supporting source IDs, confidence, and whether it appears local or ecosystem-wide. |

Read the code that the comment addressed. An objection that has already been fixed in the final diff must not become a complaint about that final diff. Conversely, a resolved thread or merged PR alone does not prove that every concern was addressed or that the code was correct. Mark outcomes as verified, partly verified, or unknown.

Historical reconstruction can be incomplete. Prefer review commit IDs and original diff hunks; for conversational comments, identify the relevant preceding revision where possible. If an accurate pre-review snapshot cannot be reconstructed, keep the case as contextual evidence and exclude it from code-based evaluation rather than substituting today's head.

## 3. Preserve authorship, disagreement, and changing decisions

Label sources as **confirmed human-written** only when independently supported, **explicitly agent-generated** when disclosed, and otherwise **undisclosed/uncertain**. Ordinary comments from a target account can be attributed to that account without claiming verified manual authorship. Do not guess from writing style or assume every comment posted by rom1504 was typed manually. Keep uncertainty when provenance is not established.

Our phase2 Astra comments are agent-generated operational evidence, not additional independent votes from rom1504. Likewise, the Claude-generated roadmap and the explicitly attributed proposals in #334 are navigation/context unless a later human statement clearly adopts a particular conclusion. Human endorsement of AI assistance does not imply endorsement of every generated recommendation.

For each candidate principle, retain who said what, in which package/version, and when. Distinguish an explicit decision from a question, a suggested option, a roadmap aspiration, and an analyst inference. Represent conflicting views and conditional tradeoffs directly; do not manufacture consensus through majority voting or comment frequency. Newer statements supersede older ones only when the evidence supports that interpretation.

Keep source permalinks and short relevant excerpts in tracked records. Cache bulk API responses separately and avoid committing quoted email tails, unsubscribe links, or unrelated personal information. Deduplicate quoted replies before counting evidence.

## 4. Pilot, then analyze in parallel

Start with **20 cases from the discovery set**, distributed across the primary repositories and the three reviewers where evidence exists. This pilot tests collection completeness, revision reconstruction, source attribution, and whether two analysts can apply the evidence schema consistently. Correct the process before scaling up; do not publish skills from the pilot alone.

Then analyze the remaining 380 discovery cases in bounded batches. A coordinator supplies every worker with this design, the package map, its exact assignment, prior evidence, and explicit instructions to seek counterexamples. Cache reads and persist progress after each PR. Use available concurrency honestly: the current environment permits three subagents alongside the coordinator, so ten batches do not imply ten simultaneous workers.

Each worker returns evidence records and candidate principles, not finished policy. Another reviewer checks a sample of ordinary cases plus disputed and high-impact generalizations. The coordinator reconciles differences, identifies coverage gaps, and prevents a prolific contributor or one long review from dominating the conclusions. Keep code defect findings, historical maintainer preferences, and analyst recommendations separate.

## 5. Turn repeated reasoning into a few skills

Store the actual skills in the repository’s top-level **`skills/`** directory, each in its own named folder containing `SKILL.md`. Execution evidence belongs under `implementation/phase3/`; skills do not. Aim initially for **five skills**, adjusting their boundaries after analysis while retaining explicit coverage of code quality and high-level architecture alongside correctness and domain specialties:

| Candidate skill | Intended responsibility |
| --- | --- |
| `prismarine-review` | Shared review workflow: understand the requested behavior and current revision; identify package ownership, public API and cross-version implications; check dependency releases; decide which comments are justified and how to communicate them. |
| `prismarine-code-quality-review` | Local clarity, duplication, state and error handling, API shape, and maintenance cost. Distinguish changes with a concrete readability or maintenance benefit from personal style preferences and unnecessary rewrites. |
| `prismarine-architecture-review` | Package responsibilities, reusable models versus packet adapters and applications, dependency direction and release coordination, public contracts, and proportionate refactoring. Explain when a local fix is sufficient and when an architectural change is necessary to make the proposed behavior sound. |
| `prismarine-protocol-data-review` | Wire codecs, schema/source agreement, enum compatibility, generated data, reproducibility, and version boundaries across generic ProtoDef and Minecraft-specific layers. |
| `prismarine-behavior-test-review` | Stateful bot/model/controller behavior, event ordering, lifecycle/cancellation, physics/geometry/rendering, and choosing tests that demonstrate the claimed behavior at the appropriate layer. |

These are hypotheses about useful packaging, not conclusions about the historical reviews. Avoid a separate skill per repository or per bug. Keep the common workflow in one place and give specialized skills clear activation conditions.

A candidate lesson becomes an instruction only with a traceable basis: an explicit scoped principle plus supporting application, or repeated reasoning across independent PR families. As an initial threshold, look for at least three independent cases for an inferred pattern; require evidence from multiple repositories before calling it ecosystem-wide. A strong single-source statement may remain an explicitly attributed, narrowly scoped policy. Sparse evidence, disagreements, and counterexamples stay visible rather than being hidden by a confidence label.

Each rule should describe **when it applies, what to inspect, what evidence would justify a comment, and when not to apply it**. Include positive examples and cases where no comment is warranted. A request to exercise a packet path does not mean all unit tests need a server; a preference for reusable modules does not make a global refactor a prerequisite for every fix.

Use phase2's corrected assessments as evaluation ideas, not historical human consensus: stale objections to already-improved tests, overestimated refactoring requirements, documented API changes mistaken for defects, and CI failures unrelated to the changed code. Preserve the user's explicit Astra attribution and publication-authorization requirements as operational instructions, separately from mined maintainer preferences.

Only after synthesis should we author actual `skills/<skill-name>/SKILL.md` files and concise supporting references, following the skill-authoring guidance available at that time. Use them explicitly in the authorized evaluations and subsequent U9G review pass; installation into a personal global skills directory is outside this task.

## 6. Evaluate before adopting the skills

Freeze the draft skills, then review the first 80 held-out PR snapshots without exposing their maintainer comments, later fixes, or outcomes to the reviewing agents. Run comparable reviews with and without the skills using the same model, snapshots, and validation budget. Reveal the historical discussion only after predictions are saved.

Evaluate:

- Precision and usefulness of proposed comments, including unsupported blockers and unnecessary refactor/test demands.
- Recovery of actionable issues documented by maintainers, while recognizing that historical comments are incomplete ground truth.
- Correct package ownership, version/API reasoning, validation choice, and inline location.
- Restraint on ordinary correct changes and concerns already addressed in the presented revision.
- Review time/tool cost and whether the skills remain small enough to use consistently.

Independently adjudicate disagreements: a valid newly found bug should not count as wrong merely because a historical reviewer missed it. Use a maintainer-readable sample of successes, misses, and false positives to assess improvement. Do not use merge status as the answer key.

After any revisions from that comparison, freeze the skills again and evaluate the remaining 20 unseen cases before revealing their historical reviews. All 500 cases are thus eventually accounted for. Further tuning after that confirmation requires a separately declared future evaluation; do not repeatedly tune on all 100 cases and continue calling the resulting score held-out performance.

## Deliverables and completion criteria

### Execution adjustment recorded before skill evaluation

The frozen 500-case corpus contains 400 discovery cases and 100 held-out cases as planned. Historical reconstruction yields **45 usable code-review packets**: 36 initial and nine confirmation. Forty-one contain a cumulative patch at an explicit historical review revision; four provide only the original inline hunk. The other 55 (44 initial, 11 confirmation) remain contextual/outcome cases, excluded from code-review scores. Do not replace them with final-head code or silently resample.

A mechanical check of direct PR relationships quarantines eight of the 45 packets from the strict comparison because of possible discovery overlap. The remaining 37 consist of 28 initial and nine confirmation cases; report cumulative-patch and hunk-only results separately. A lack of detected links does not prove independence: title-based family grouping and direct-reference screening can miss related work. Review all 45 in both arms, treating the eight quarantined cases as supplemental results. Reveal each stage's historical evidence only after its predictions are saved; contextual cases cannot supply tuning information before the corresponding freeze.

The actual search found no qualifying Karang PR participation in this four-year window across the 17 inventoried repositories. Attribute older foundational Karang comments separately; do not extend the window or manufacture three-reviewer coverage. Current merged/unmerged counts and complete collection limitations belong in the implementation report.

**Post-hoc exposure check during confirmation:** checking the prepared packets against the phase2 classification/review archive found Mineflayer #4087 and #4093 at revisions already reviewed before skill authoring. Both were in the original strict confirmation group. Preserve the original groups and scores, but additionally report a clean sensitivity comparison excluding those two: six cumulative confirmation packets plus one hunk-only packet. No initial packet matched the phase2 archive. This check should happen before future holdout selection; excluding explicitly agent-generated comments from policy induction alone does not prevent prior-review exposure. The implementation records disclose when this gap was found and retain both result sets.

### Artifacts

Execution records will belong under `implementation/phase3/`, following this repository's distinction between designs and work performed:

| Artifact | Purpose |
| --- | --- |
| `survey_manifest.json` | Frozen scope, selection method, 500 PR identities, splits, retrieval dates, and coverage gaps. |
| `review_cases.jsonl` and `principle_sources.jsonl` | Structured PR evidence and foundational issue/document evidence, with provenance and uncertainty. |
| `principles.md` | Concise findings, per-reviewer context, supporting examples, exceptions, superseded proposals, and open questions. |
| `../../skills/<skill-name>/SKILL.md` | Review skills at the repository root, with curated references and explicit activation boundaries; include code quality and high-level architecture. |
| `evaluation.md` and evaluation records | Baseline comparison, adjudicated examples, coverage limitations, and adoption recommendation. |
| `report.md` | What was surveyed, merged/unmerged counts, lessons, skill changes, validation results, limitations, and commit details. |
| `u9g_rereviews.md` and `.json` | Subsequent current-head reviews, skills used, duplicate checks, posted comment links, and justified skips. |

Completion means all selected PRs are accounted for, coverage and unavailable evidence are disclosed, every skill instruction is traceable or explicitly identified as a user operational requirement, and evaluation demonstrates useful reviews without increasing unsupported demands. The result is a set of review aids, not a claim to reproduce the maintainers' judgment perfectly.

**Authorized execution order:** update this design; survey with subagents; write the top-level skills; evaluate and improve them; write the phase3 implementation report; commit the design, skills, and execution artifacts. Then use the skills with ten subagents to re-review pending U9G PRs and publish appropriate nonduplicate inline comments under the user’s explicit authorization. Every published review and inline comment must identify Astra as the authoring agent rather than a manually written maintainer comment, and explain which skills contributed and how. The user allows up to six hours for the entire task, with earlier completion when done. Record incomplete coverage or evaluation limitations honestly rather than implying a full code audit of every historical PR.
