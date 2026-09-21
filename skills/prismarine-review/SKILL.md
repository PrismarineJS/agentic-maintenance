---
name: prismarine-review
description: Review PrismarineJS correctness, maintainability and integration readiness using domain skills and maintainer standards. Use for PR triage, code review and authorized Astra inline-review publication.
---

# PrismarineJS review

Record repository, PR, base/head, dependency versions, open/closed state and **merged status separately**. Read the current diff, callers and existing discussion. Closed-unmerged may mean superseded; merge or approval is not a correctness oracle. Historical concerns can refer to code already fixed. [Historical exceptions](references/evidence.md) help when a precedent changes the review's scope.

Select only the relevant domain skills:

| Changed contract | Skill |
|---|---|
| Packet bytes, data generation, version/features, compiled codecs | [Protocol and data](../prismarine-protocol-data-review/SKILL.md) |
| Configuration/play, input caches, action queues, prediction and completion | [Lifecycle and actions](../prismarine-lifecycle-action-review/SKILL.md) |
| NBT/components, stack serialization, cursor/windows, recipe remainders | [Items and inventory](../prismarine-item-inventory-review/SKILL.md) |
| Raycasts, partial shapes, reach, teleport/flight, path completion | [Geometry and movement](../prismarine-geometry-movement-review/SKILL.md) |
| Registries/world identity, dimensions, incremental rendering and disposal | [World and rendering](../prismarine-world-render-review/SKILL.md) |
| Package owners, factories, public APIs, abstractions and code quality | [Architecture](../prismarine-architecture-review/SKILL.md) |

Use architecture alongside the domain skill when a patch adds helpers, plugin state, repeated packet paths or a new testing abstraction. A bug-fix label and passing tests do not exempt its design from review.

The maintainer has explicitly adopted extremeheat's judgment as a trusted review standard. Apply his concrete requests in their relevant context, including code-quality requests; do not dismiss them because no runtime failure was demonstrated. Read later replies and the actual changed code. A tentative suggestion is not a mandatory dependency choice, and explicit current user decisions take precedence. The [standards and examples](../prismarine-architecture-review/references/extremeheat_standards.md) distinguish direct decisions, accepted follow-ups and agent-authored evidence.

Assess correctness, maintainability/package fit, and validation/release readiness separately before calling a PR ready. State whether an outstanding item is an author repair, maintainer design decision, or integration prerequisite. An unaddressed applicable maintainer request is not cleared by a green test run or an earlier Astra review.

Trace a concrete supported input/event sequence to a consequence. Validate at the layer of the claim: packet encoding, model updates, server-observed action, or rendered state. A static counterexample is sufficient when its input contract and consequence are established. An unavailable fixture or guessed wire rule is uncertainty, not a defect. Check candidate dependencies and release readiness separately.

Try to disprove each finding using retained behavior, defaults, version bounds and later replies. Separate a necessary repair/refactor from optional cleanup. For correctness, name the broken invariant and affected consumers. For maintainability, name the repeated logic, misplaced responsibility or unnecessarily complex fixture, its concrete maintenance cost, and the smallest change that addresses it. Do not invent a runtime failure to justify a design objection. Prefer the existing test harness over demanding a new framework; do not require a new test for every cosmetic change.

For each retained finding give the trigger or design problem, consequence, evidence and bounded next step. Compare prior threads by **root cause and requested action**, including old Astra comments. No new comment is a valid result and does not imply approval.

Publication needs task authorization. Immediately before posting, refresh head/state/discussion and recheck affected findings if changed. Use a COMMENT review unless instructed otherwise; anchor each finding to its smallest relevant changed range. Verify partial success before retrying an ambiguous publication error.

In this repository's authorized Astra workflow, each summary **and inline comment** includes:

> **Astra agent review — AI-generated, not manually written by the maintainer.**

Name the skills actually used and briefly say what check each contributed. This is the user's attribution requirement, not a mined historical maintainer preference.
