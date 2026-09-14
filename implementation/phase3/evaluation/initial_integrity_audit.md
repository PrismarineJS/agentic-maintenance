# Initial evaluation integrity audit

Date: 2026-09-14. Scope: initial predictions, scores, adjudication and arm key; initial case metadata and only the corresponding 36 raw code packets. No confirmation packets, discussions or predictions were inspected. No skills, predictions, judgments or scores were changed.

All recorded score arithmetic agrees with an independent recomputation. There are 72 paired predictions, 57 findings with one-to-one anonymized judgments, and 80 initial adjudicated cases (36 paired plus 44 contextual-only). All 36 packet content hashes and prediction/manifest packet digests match. The initial prediction SHA-256 matches the documented freeze. Finding-count and reported elapsed-time caps pass.

The initial results table in `evaluation.md` agrees with the artifacts: on 27 strict cumulative cases, baseline/skills produced 23/20 findings, 18/18 supported actionable concerns, 1/1 supported optional concerns, 4/1 uncertain concerns, 0/0 unsupported concerns, and 11/12 abstentions. Actionable reference recovery is 4/9 versus 5/9; reported mean seconds round to 25.2/30.7. The single strict hunk-only baseline finding, overlap-sensitive totals, and paired examples also match adjudication. No numerical correction is required. Supported-actionable verdict counts include a baseline optional proposal; uncertainty remains separate from unsupported findings.

## Mechanical location check

Every predicted path, line and side was mapped through actual displayed unified-diff rows. Context rows advance both sides; additions advance RIGHT and deletions advance LEFT. Original inline hunks can stop before their header's advertised length, so header ranges alone were not treated as displayed evidence. Full supplied source was checked separately where available.

| Anchor class | Baseline | Skills |
| --- | ---: | ---: |
| Displayed added line | 30 | 25 |
| Displayed unchanged context | 0 | 1 |
| Outside displayed hunk | 1 | 0 |
| Missing path, null/invalid line, invalid side | 0 | 0 |

All 57 anchors specify RIGHT; none targets a deleted line. Two placement qualifications should accompany any claim that every finding is anchored to a changed line:

- `finding-af247f9b417a1248` (skills, viewer #408 / `case-2c1df8e6f116`): `package.json` RIGHT 9 is the unchanged `pretest` context line. The recursive `test` addition discussed in the finding is RIGHT 8. This is an imprecise but displayed context anchor, not a missing location.
- `finding-8ca663ecaebe7be0` (baseline optional, `case-705127eb8e43`, overlap-sensitive original-hunk packet): `lib/pc/index.js` RIGHT 26 exists in the supplied 145-line historical source, but the displayed hunk contains only RIGHT 20–23. It is outside displayed diff context, not outside the historical source. Preserve the frozen finding and report this distinction separately from semantic scores.

## Interpretation limits

Two unrecovered strict references, minecraft-data #749 (`R749-1`) and #784 (`R784-1`), depend on historical signed-wire-contract evidence unavailable in the review packets. Their recorded eligibility was not reconsidered; the reported recall cannot be read as nine equally demonstrable packet-only opportunities.

Location validity does not establish correctness or publication readiness. This audit preserves adjudicator semantics, including the generator #29 version-scope qualification. It does not verify fresh-agent isolation, serving model identity, actual total compute, skill-loading overhead, or compliance with procedural access restrictions. No historical integration tests or external requests were performed.

[Machine-readable checks, every finding location, source hashes and recomputed metrics](initial_integrity_audit.json) preserve the audit evidence.
