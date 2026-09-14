# Evaluation of the PrismarineJS review skills

Date: 2026-09-14. Status: paired evaluation, one skill revision, confirmation and adjudication complete.

## Design and denominators

The 400 discovery PRs supplied skill evidence. The other 100 were withheld: 80 initial and 20 confirmation. We could reconstruct 45 review packets at explicit historical revisions; 55 remain contextual discussions and never enter code-review scores.

| Group | Initial | Confirmation | Total |
| --- | ---: | ---: | ---: |
| Usable paired packets | 36 | 9 | 45 |
| Strict cumulative patches | 27 | 8 | 35 |
| Strict original-hunk packets | 1 | 1 | 2 |
| Potentially overlapping, supplemental packets | 8 | 0 | 8 |
| Contextual-only discussions | 44 | 11 | 55 |

The strict group excludes direct-link signals of related discovery work. Family grouping uses normalized titles and a subsequent direct-reference check; undetected overlap remains possible. Original-hunk packets indicate where a historical discussion happened, so they are reported separately from cumulative patches. These are selected, bounded source reviews rather than complete repository checkouts.

The table preserves the **predeclared** grouping. During confirmation, a [post-hoc audit against the phase2 review archive](evaluation/prior_review_overlap_audit.md) identified two more exposed cases: Mineflayer #4087 and #4093, both at exactly the previously reviewed revision. One had a posted Astra review and the other had been reviewed and validated without a new comment. Neither belongs in an independent confirmation comparison. Original results remain visible; a clean sensitivity group excludes both, leaving **six cumulative and one hunk-only confirmation case**. No initial packet overlaps the phase2 archive. This is a selection-process gap, not a reason to hide unfavorable results or retune the skills after confirmation.

Both arms use fresh agents with the same inherited coordinator model/reasoning configuration, the same code packets, a declared cap of 120 seconds per case, no external requests, and at most three actionable plus one optional finding. These are caps, not targets. The exact serving-model identifier and token usage are not independently exposed. Reported case timings do not necessarily include initial skill-loading overhead and are not proof of equal computational work.

The baseline receives ordinary review instructions; the other arm reads the frozen skills. Neither sees PR discussion, later fixes, outcome, another agent's predictions, or private evaluation evidence. Shared-filesystem separation is procedural, not an enforced filesystem security boundary. Fresh conversation contexts do not rule out prior model-training exposure to public PRs. Packet hashes, task declarations, predictions, skill contents and freeze hashes make the comparison auditable.

## Adjudication

After both arms' predictions are saved and hashed, separate agents read historical context and the displayed revision. They first identify eligible historical concerns, excluding stale or already fixed requests, omitted code, unsupported premises and merely optional preferences. They then assess anonymized, shuffled findings with arm labels and skill explanations removed. Wording may still reveal clues, and agent adjudication is not independent human ground truth.

Verdicts distinguish supported actionable findings, supported optional suggestions, unsupported findings and uncertain findings. A valid new bug can be supported even when the historical discussion did not mention it. Merge status is never an answer key. Recovery counts distinct eligible reference issues matched by a supported finding proposed as actionable. Uncertainty is reported separately rather than silently counted as either correctness or a false positive.

The initial results may inform one skill revision. Revised skills are frozen before either confirmation arm runs. Confirmation context and results are revealed only after both confirmation predictions are saved; they cannot be used to retune this same evaluated version.

## Artifacts

- [Initial skill contents and hashes](evaluation/skills-initial.json).
- [Packet inventory and reconstruction exclusions](evaluation/packet_manifest.json).
- [Cross-split overlap screening](evaluation/cross_split_link_summary.json).
- [Harness commands and limitations](scripts/evaluation_harness.md).
- [Independent adjudication instructions](scripts/adjudication_prompt.md).

## Initial results

Eight fresh reviewers produced 72 predictions for 36 packets, frozen at SHA-256 `60d9aa64f5e93f8099cc9ac5c76e89898d23ab0417e3e253a473fadac2379774`. Three separate adjudicators then judged all 57 proposed findings and individually curated all 80 initial heldout cases, including the 44 contextual-only discussions. [Scores](evaluation/initial-scores.json) preserve all groups and exact denominators; [predictions](evaluation/initial-predictions.jsonl) and [adjudications](evaluation/initial-adjudication) preserve the individual reasoning.

The main comparison uses the **27 strict cumulative-patch cases**:

| Measure | Baseline | Initial skills |
| --- | ---: | ---: |
| Proposed findings | 23 | 20 |
| Judged supported actionable | 18 | 18 |
| Judged supported optional | 1 | 1 |
| Judged uncertain | 4 | 1 |
| Judged unsupported | 0 | 0 |
| Cases with no proposed comment | 11 | 12 |
| Eligible historical issues recovered as actionable | 4 / 9 | 5 / 9 |
| Reported mean seconds per case | 25.2 | 30.7 |

“Supported actionable” describes the adjudicated concern, regardless of the predictor's label. The baseline labelled one such concern optional; the skills labelled one optional coverage suggestion actionable. Thus this table does not mean every proposed comment was ready to publish. Uncertain concerns are not proven false positives, and no unsupported findings were identified in either arm. Timing excludes some setup/skill-loading overhead and is affected by concurrent scheduling; no case exceeded its declared cap.

The single strict hunk-only case produced a supported null-dereference concern in the baseline and an abstention with skills. In the eight overlap-sensitive cases, baseline had five supported actionable, one optional and one uncertain finding; skills had six supported actionable findings. Across all 36 packets, each arm had 24 supported actionable findings. These strata should not be pooled into a claim that the skills always find more bugs.

A separate [integrity audit](evaluation/initial_integrity_audit.md) independently reproduced all score fields and checked locations. One baseline optional finding points outside the displayed hunk, although its line exists in the full supplied source. One skills finding uses an adjacent unchanged context line rather than the precise changed line. Semantic support and publication-ready positioning are different checks; none of these historical predictions was posted to GitHub.

The historical-reference comparison is sparse and diagnostic. Two of its nine strict references—minecraft-data #749 and #784—depend on signed-encoding contracts attested in the withheld discussions rather than independently available wire evidence in the review packets. Neither arm recovered them. This limits the interpretation of recall under the no-external-access constraint. Historical comments remain an incomplete reference, and most supported findings were independently adjudicated novel concerns.

Useful paired examples include:

- Viewer #408: both arms found the recursive `npm test` command, stairs matching an air substring, and browser-only error handling breaking a headless path. Historical optional questions were not substituted for those concrete defects.
- Flying-squid #691: three baseline protocol assertions remained uncertain without the actual schema; the skills found an independently supported timer-lifetime problem. Both missed the retained legacy latency branch identified in the historical review.
- Protocol #1498: both noticed a suite absent from a version-filtered job, but an unfiltered test command also exists and the workflow was omitted. The skills overstated this optional coverage concern.
- Chunk #278: both identified a conditional cache/fixture problem, but the missing fixture and decoder prevented establishing that the actual test fails.
- Minecraft-data #1086: both found the same-major audit exemption, but missed another exemption for prereleases/snapshots. Generator #29 also showed a version-scope overstatement: only the displayed 1.10.2 color change was newly introduced, despite the finding also naming 1.11.2.

## One revision before confirmation

The initial skill set hash is `37bf4e94850ab3bc9fdcd049c167a354052f3653c53025b3d2ee0d6db2442b09`. Based on the completed initial adjudication, four skills received small procedural changes:

1. The core workflow distinguishes a static counterexample within an established input contract from an assumed fixture/wire contract. It checks retained paths affected by shared-contract changes and limits claimed version scope to evidence.
2. Behavior/test review now verifies fixture contents/decoder behavior for fixture-dependent failures and traces actual CI jobs before asserting missing coverage.
3. Protocol/data review explicitly asks for distinguishing source-grounded bytes for signed/unsigned or varint/zigzag changes; internal consistency alone is insufficient, and unavailable evidence does not justify guessing the correct encoding.
4. Code-quality review checks every exemption or early return that suppresses a validator/audit failure, while preserving intentional supported exceptions.

Architecture guidance was left unchanged. These are evaluation-driven calibration refinements, not additional claims of historical maintainer consensus. The revised set was frozen at `ac1ab7b2585452ba9ffb5240582fa192149463b3ce56af5daeb2e11525cb05f0` before either confirmation reviewer started. [Revised contents and hashes](evaluation/skills-confirmation.json) preserve that version.

## Confirmation and adoption

Two fresh reviewers produced 18 confirmation predictions, frozen at `75a7d2d3060f7c2f520cbd5502e98119e05ecd991a73589b70f063e5ee41e362`. A separate adjudicator then individually analyzed all 20 confirmation cases, including 11 contextual-only discussions, and judged every anonymous finding. The final skill hash remains unchanged; no confirmation answers were used for retuning.

The **six clean cumulative-patch confirmation cases**, excluding the two phase2 exposures, give:

| Measure | Baseline | Revised skills |
| --- | ---: | ---: |
| Proposed findings | 3 | 3 |
| Judged supported actionable | 3 | 3 |
| Judged optional / uncertain / unsupported | 0 / 0 / 0 | 0 / 0 / 0 |
| Cases with no proposed comment | 5 | 5 |
| Reported mean seconds per case | 23.8 | 23.3 |

All three concerns occur in one prismarine-world change: an undeclared runtime dependency, failure-path timeout cleanup, and the public contract of shared cached block objects. The baseline called the last optional; the adjudicator considered the need to clarify that contract actionable. Both arms abstained on the separate clean hunk-only case. There are no eligible independent actionable historical references in this confirmation sample, so a recall percentage is undefined.

For transparency, the original nine-case confirmation grouping has four supported actionable concerns in each arm, plus one supported optional test suggestion in the skills arm. The extra case with findings is the previously reviewed Mineflayer #4093; #4087 is also excluded for prior exposure even though both arms abstained. [Full scores and clean sensitivity groups](evaluation/confirmation-scores.json), [predictions](evaluation/confirmation-predictions.jsonl), [adjudications](evaluation/confirmation-adjudication), and the [mechanical integrity audit](evaluation/confirmation_integrity_audit.md) retain these results. All nine finding locations exist in the supplied diff; one baseline anchor is an adjacent context line. No historical prediction was published.

**Adopt the five skills as review aids with an evidence and publication check.** The initial sample suggests better restraint with the same number of supported concerns, and the small clean confirmation sample shows no loss in supported concerns or increase in unsupported demands. It does not establish higher general bug recall, universal improvement, or a speed advantage. More representative unseen cases, prior-exposure screening before selection, richer context and independent human adjudication would be needed for stronger claims. The next authorized U9G pass uses full current code and discussion, appropriate focused validation, and duplicate/location checks; these historical scores are not permission to publish an unverified concern.
