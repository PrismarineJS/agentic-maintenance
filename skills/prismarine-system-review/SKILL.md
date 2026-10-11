---
name: prismarine-system-review
description: Assess existing PrismarineJS capabilities across packages against the maintainer's principles and propose coherent incremental architectural improvements. Use for system assessments, architectural drift or shared refactoring plans; ordinary bounded PR reviews use prismarine-review.
---

# Review the existing system

Read [PRINCIPLES.md](../../PRINCIPLES.md). Assess a capability such as world state,
item conversion or entity interactions from its existing implementation, even
when no PR is open. The unit of review is the capability and its consumer chain,
not a list of independently plausible patches.

## Establish the actual system

Choose a bounded capability and trace data producer → interpretation/computation
→ mutable owner → public API → consumers. Record repository revisions, package
versions and version/edition scope. When using a dependency's current source,
check what the consumer actually declares or loads; distinguish a target-branch
assessment from an installed/released integration claim.

Read the relevant maintainer plans and later discussion. Label what is accepted,
proposed, superseded or uncertain, with source links. Identify applicable earlier
assessments under `design/` and `implementation/`; refresh their evidence rather
than treating a dated finding or an old review objection as current truth.

Use [architecture review](../prismarine-architecture-review/SKILL.md) for package
ownership and real consumer boundaries. Select only the domain skills routed by
[PR review](../prismarine-review/SKILL.md) that the capability needs. Their
regression/testing guidance applies to existing code too; pending-PR examples
are leads to verify, not findings about the current default branch.

For each boundary identify:

- Which facts are static Minecraft data, negotiated registry state or live state?
- Where does computation happen, and what does it read, mutate or emit?
- Which package owns each mutable value, including caches and asynchronous work?
- Can the package's contract be used and tested without its first application?
- What do older versions and other editions reveal about the abstraction?
- Could another language implement the behavior from the contract and fixtures?

## Judge direction with evidence

Map observations to stable P1–P6 anchors in the principles. Record conforming
behavior as well as gaps. Distinguish a demonstrated defect, an architectural
cost, a documentation/validation gap and an untested hypothesis. A principle
alone is not evidence of a runtime bug. Name the repeated change, hidden
ownership or lost capability that makes an architectural gap matter.

Inspect the existing tests and their discovery/version matrices. Independent
unit tests and consumer integration tests establish different claims; neither
substitutes for the other. Use the existing
[testing standards](../prismarine-review/references/testing_standards.md).
Only run/install what the assessment needs; source inspection must be reported
as such, and temporary dependencies/builds should be removed when no longer needed.

Compare contracts before consolidating similar implementations: sync and async
access, application convenience methods and lower-level queries can intentionally
have different loading or callback semantics. Name the differences to preserve
and the shared mechanics to extract; fewer lines alone do not establish improvement.

Shared state is not automatically bad state. Separate model truth from a
consumer's derived cache and from a worker's explicitly synchronized replica.
Likewise, a mutable storage implementation does not itself violate P3. Examine
the calculation/mutation boundary before prescribing immutable copies or events.

## Propose one coherent target and a bounded path

Describe the target ownership and contracts before listing edits. Tie each step
to that target and identify real consumers, compatibility constraints and evidence
that would demonstrate improvement. Consider extending an existing package or an
internal separation before introducing another package/framework. Preserve proven
behavior; make incompatible API or coordinate/serialization changes explicit.

Separate existing defects worth repairing now, bounded steps toward the target,
and decisions needing maintainer input. A new-version repair need not wait for
an entire architecture migration. Compare the combined result of proposed steps:
individually useful edits can still create competing sources of truth or APIs.

Record exceptions and deferred work with status, rationale, affected paths,
decision source and a revisit condition. An agent-proposed deferral is not a
maintainer-approved exception. Use explicit uncertainty when the source does not
settle the intended behavior.

## Produce a reusable assessment

Follow the repository's phase convention. The design contains the capability
scope, current ownership map, relevant P1–P6 findings with immutable source links,
target proposal, migration order and validation criteria. The implementation
record states what was inspected/executed, revisions, findings retained or
rejected, limitations, and whether any runtime changes actually landed.

Include a short **PR implications** section: changes that advance the target,
changes that would deepen a demonstrated problem, and bounded fixes that remain
reasonable before the migration. This lets later PR reviewers use the assessment
without repeating the whole audit. Do not invent compliance scores or imply that
all six principles were exhaustively assessed from a narrow sample.

Assessment does not authorize code changes, issue publication or PR comments.
Honor the current task's scope. When publication is authorized, use the established
Astra attribution and duplication checks in the common review skill.
