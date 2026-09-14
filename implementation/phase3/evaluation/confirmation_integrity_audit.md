# Confirmation evaluation integrity audit

Date: 2026-09-14. Mechanical audit after the prediction freeze at SHA-256 `75a7d2d3060f7c2f520cbd5502e98119e05ecd991a73589b70f063e5ee41e362`. Only the 18 frozen predictions, their nine historical code packets, corresponding compact metadata, task declarations and prediction freeze were inspected for these checks. Semantic adjudication and quality/adoption conclusions are outside this audit.

All 13 integrity checks pass: paired coverage, manifest/task coverage, matched model/budget declarations, prediction declarations matching tasks, expected revised skill digest declarations, raw packet content digests, prediction/manifest/task packet digest agreement, combined and individual prediction-file freezes, finding caps, reported elapsed-time caps, and empty-result rationales. The nine cases comprise eight cumulative packets and one original-hunk packet. Skill contents were not read or rehashed.

## Mechanical location check

Actual displayed unified-diff rows were mapped on RIGHT/LEFT. Unchanged context advances both sides, additions advance RIGHT and deletions advance LEFT. Hunk headers do not make omitted rows visible; full supplied source is checked separately when available.

| Anchor class | Baseline | Skills |
| --- | ---: | ---: |
| Displayed added line | 3 | 5 |
| Displayed unchanged context | 1 | 0 |
| Outside displayed hunk | 0 | 0 |
| Missing path, null/invalid line, invalid side | 0 | 0 |

All nine proposed findings specify RIGHT and have displayed locations. Baseline `case-ffb4575ce459`, finding index 0, anchors `lib/plugins/entities.js` RIGHT 898 to an unchanged closing brace. The adjacent added `bot.setControlState('sneak', false)` is RIGHT 897. This is an imprecise but displayed context anchor; the frozen prediction remains unchanged. No finding is outside the displayed hunk or outside an available historical source file.

Location existence does not establish correctness, severity or publication readiness. Matching model and budget declarations do not independently verify serving identity, token use, overhead, total compute, fresh-agent isolation or procedural access compliance. No runtime tests, external requests or semantic re-adjudication were performed. Scores were not yet available at this mechanical audit.

[Machine-readable checks, every finding location and source hashes](confirmation_integrity_audit.json) preserve the audit evidence.

## Prior-exposure addendum

A subsequent [all-packet phase2 overlap audit](prior_review_overlap_audit.md) identified confirmation cases `case-d03f269e7db8` (mineflayer #4087, reviewed/validated but publication skipped) and `case-ffb4575ce459` (mineflayer #4093, Astra review posted) in both phase2 registries, at exactly the same revisions. Both retain their original strict flags. Report a separate post-hoc exclusion of these two cases; passing mechanical checks does not establish confirmation independence.
