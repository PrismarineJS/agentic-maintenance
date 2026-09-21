# Apply extremeheat's review standards

Date: 2026-09-21. Starting commit: `7a6980b`. Written before editing the skills.

The maintainer explicitly trusts extremeheat's judgment and requested stronger review skills after comparing his recent PR comments with our current guidance. The principal gap is that our architecture guidance permits required shared changes only for demonstrated correctness failures. That misses concrete maintenance costs which extremeheat treats as review concerns even when tests pass.

Keep the existing seven skills. Update the common workflow, architecture, protocol/data and lifecycle skills; link one focused architecture reference for the maintainer decisions, outcomes and scope boundaries. Preserve existing domain mechanisms, attribution requirements, authorization limits and withdrawn-findings records. Do not create a generic additional review skill.

## Decisions to encode

- Evaluate correctness, maintainability/package fit, and validation/release readiness separately. A concrete maintenance problem can justify a bounded pre-merge change without inventing a runtime bug.
- Prefer existing Mineflayer plugin structure and shared packet/model owners over repeated orchestration. Show the duplicated consumers and smallest repair; extraction alone is not progress.
- Normalize accidental data representation differences upstream before adding consumer feature flags. Preserve actual wire differences and consumer-facing semantic names. Check affected versions and both read/write callers.
- Prefer real NMP client/server fixtures for packet-driven plugin behavior; assess both NMP client and server implementations. Controlled model tests remain suitable for pure model behavior and supplementary fault isolation.
- Capture recurring defects in schema/category-wide validation and put generic protocol validation in protodef-validator. Preserve the explicitly accepted path of landing a bounded correction before moving a general checker.
- Evaluate performance against the real workload, existing caches, browser consumers and storage side effects. Make ProtoDef sizing/writing dependencies and language-independent contracts explicit.
- Preserve extraction provenance: repair active generators, document regeneration and distinguish source-derived corrections from hardcoded output overrides.

## Evidence and limits

Use the August–September 2026 discussion sample already fetched from 80 recently active PRs, plus a small older-comment check against the existing 500-PR survey. Re-read original comments before adding new historical evidence. Explicit Astra/Codex reviews are engineering evidence, not independent corroboration of extremeheat's preferences. Direct instructions are the trusted default in their applicable context; tentative suggestions and superseded requests do not become universal requirements. Existing user decisions continue to take precedence.

## Validation and delivery

Check all seven skill frontmatters, repository artifact accounting, relative links and patch whitespace. Walk realistic known cases through the revised decision rules, including passing-code maintenance concerns, fake-bot versus pure-model tests, normalization versus real wire changes, shared validation versus an accepted stopgap, and Node caching versus browser use. Record outcomes and limitations in `implementation/phase3/extremeheat_review_standards.md`. These are known-case consistency checks, not an independent accuracy benchmark or new application test runs.

Follow the established design → skills → report → commit/push workflow for this repository. Exclude the three pre-existing untracked phase2 drafts. Do not post new PR reviews or modify application repositories.
