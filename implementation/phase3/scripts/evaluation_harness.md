# Historical review evaluation harness

`prepare_evaluation.py` packages historical code and creates blinded paired review tasks. It does not review code or write to GitHub. Raw code and discussion caches stay outside Git; commit compact indices, hashes, predictions, scores and methodology instead.

## Accounting and evidence separation

The frozen selection contains 500 PRs: 400 discovery, 80 initial evaluation and 20 confirmation. All 500 receive corpus metadata, discussion collection and explicit merge/outcome accounting. Discovery lessons are derived only from the 400 discovery cases. Heldout discussions remain private until the relevant skill version and predictions have been frozen.

At preparation, 45 of 100 heldout cases have usable exact historical patches: 36 initial and 9 confirmation. The other 55 (44 initial, 11 confirmation) have no target review anchored to a recoverable exact revision. They remain in the 500-case corpus and receive a contextual discussion/outcome analysis after the relevant stage is frozen; they do not count as code-review predictions or score denominators. No final-head substitution or silent reserve replacement is permitted.

Of the 45 packets, 41 contain cumulative patches and 4 contain original inline hunks. The latter select locations discussed historically, so their scores must be reported separately. Conservative direct-link screening identifies 8 packets with possible discovery overlap; these are supplementary comparisons, excluded from strict aggregate metrics. The remaining 37 comprise 35 cumulative patches and 2 hunk-only packets. Strict initial counts are 27 cumulative plus 1 hunk; strict confirmation counts are 8 cumulative plus 1 hunk. Absence of a direct link does not establish independence. Screening includes links between initial and confirmation stages; no additional linked packets were found in this collection.

The custodian may process heldout text mechanically for packaging and leakage screening, but must not supply its findings to skill authors or reviewers. Answer-bearing files are under `evaluation/private/` and `heldout/`. Reference adjudication of initial cases may be disclosed after initial predictions freeze, for one skill revision. Confirmation answers remain withheld until confirmation predictions freeze. Analysis of the 11 untestable confirmation discussions also waits until then.

## Commands

Paths below assume execution from the repository root. The collector must already have populated `/tmp/prismarine-phase3/{discovery,heldout}/`.

```sh
python3 implementation/phase3/scripts/prepare_evaluation.py prepare \
  --input implementation/phase3/survey_manifest.json \
  --case-cache /tmp/prismarine-phase3/heldout \
  --output /tmp/prismarine-phase3/evaluation --fetch

python3 implementation/phase3/scripts/audit_cross_split_links.py \
  --manifest implementation/phase3/survey_manifest.json \
  --cache /tmp/prismarine-phase3 \
  --evaluation /tmp/prismarine-phase3/evaluation

python3 implementation/phase3/scripts/prepare_evaluation.py freeze \
  --skills "$PWD/skills" \
  --output /tmp/prismarine-phase3/skills-initial-freeze.json

python3 implementation/phase3/scripts/prepare_evaluation.py batches \
  --manifest /tmp/prismarine-phase3/evaluation/packet_manifest.json \
  --output /tmp/prismarine-phase3/evaluation/batches \
  --freeze /tmp/prismarine-phase3/skills-initial-freeze.json \
  --model 'ACTUAL_MATCHED_MODEL_CONFIGURATION'
```

The default batch size is nine and the declared review cap is 120 seconds per case, with no external requests. There are four initial batches per arm and one confirmation batch per arm. Reviewers inspect identical bounded packets sequentially; skills reviewers additionally inspect the frozen skills. Run each batch in a fresh agent with no inherited conversation. Match model, reasoning configuration, tools and caps between arms. The cap is declared, not an assertion that actual resource consumption was equal; record observable elapsed time/token usage separately. A cap of three actionable and one optional finding is not a target count.

Do not start either initial arm before the initial skill freeze. Do not start confirmation tasks until the revised skills are frozen. Preserve initial tasks/results and create confirmation tasks in a new output directory with the revised freeze. Review agents must not read other predictions or adjudication evidence. Shared-filesystem access controls are procedural rather than a security sandbox; disclose that limitation.

Each prediction JSONL records the opaque case, arm, matched model/budget, packet and skill digests, findings with path/line/scenario/evidence/requested change/validation, empty-result rationale, skills used and validation limits. Concatenate only the relevant stage outputs, then audit:

```sh
python3 implementation/phase3/scripts/prepare_evaluation.py audit \
  --manifest /tmp/prismarine-phase3/evaluation/batches/initial_evaluation-manifest.json \
  --predictions /tmp/prismarine-phase3/evaluation/initial-predictions.jsonl
```

Freeze prediction hashes before independent adjudication. The audit checks paired coverage and declarations; it cannot establish semantic validity, actual elapsed budgets, clean agent context or compliance with the no-history instruction.

## Adjudication

An independent adjudicator reads predictions plus private original discussions and the exact displayed patch. Judge concerns against that revision and bounded scope. Historical comments are incomplete references; later fixes, praise, approval or merge status are not automatic ground truth. Distinguish supported actionable concerns, optional maintenance suggestions, unsupported concerns and genuinely uncertain context. A valid new issue is not a false positive because no maintainer mentioned it. A historical objection already fixed before the displayed revision is not a missed finding. Exclude references outside displayed code from recall denominators.

Report matched actionable concern recovery, unsupported-comment burden and optional-suggestion usefulness with their exact denominators. Include per-case abstentions and scope limitations. Separate cumulative versus hunk-only results, strict versus overlap-sensitive results, and initial versus confirmation results. Small selected samples support directional evidence, not a claim of universal review improvement.

## Reconstruction limitations

The earliest explicit target-review SHA is selected, with original inline SHA preferred. Cumulative reconstruction requires that SHA in the retained PR commit list, a simple parent for its first commit, and established comparison ancestry. Otherwise only exact original inline hunks qualify. Conversational comments without an exact revision are not assigned a commit by timestamp guesswork. A review anchor can be later than an earlier conversational concern; adjudication must check which concerns still exist at the displayed revision.

Selection is deterministic filename order with 24,000 patch characters and 30,000 optional source characters. Omitted paths and missing full files are recorded. GitHub API patch omissions/truncations may still limit context; these packets are bounded source reviews, not complete repository checkouts or executed integration tests. Current PR descriptions are excluded because they can contain later answers; intended behavior unavailable from code remains a review limitation.
