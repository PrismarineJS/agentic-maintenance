---
name: prismarine-protocol-data-review
description: Review PrismarineJS protocol schemas, generated Minecraft data, codecs, version support and their consumer migrations. Use when correctness depends on wire representation, data provenance, registry semantics or cross-package protocol compatibility.
---

# Protocol and data review

Identify the exact edition, release or snapshot, protocol state, packet direction and dependency revisions before judging a change. A folder label or shared numeric protocol version may not identify the selected schema. Follow the actual loader and candidate dependency; a version-list addition establishes support only when the relevant wire behavior already exists.

Use [historical decisions and exceptions](references/sources.md) when weighing review scope. They are scoped evidence, not permanent requirements. Read a source's replies and later revisions before using it to justify a current finding. Merge status does not prove a codec correct or settle later disagreement.

## Establish the maintained representation

Trace the changed value through maintained YAML or extraction code, generated JSON, dataPaths/loader mapping, Node wrapper, codec and actual consumer. Determine which artifacts are authoritative for this category and version. Correct a live generator when regeneration would reintroduce a defect; do not demand a generator change for an isolated historical typo it no longer produces. New files must be reachable through the loader. A native type declaration needs a registered implementation and available dependency, not merely a plausible type name.

For large version copies, ask for the unchanged baseline plus the semantic delta, or an equivalent focused comparison. Separate manual protocol review from unrelated generated output when that makes the real change inspectable. Obtain extraction commands, source version and tool revision where reproducibility matters. Generated output and another implementation using the same generator are not independent correctness oracles.

Check exact vanilla structures, attributable source or captured packets when documentation disagrees. Trace every embedding of a changed shared type: similar names such as item cost and item slot can encode different structures. Preserve wire width, signedness, endianness, count prefixes, optionality and branch selection. Logical flag count does not determine integer width. A malformed nested element can desynchronize all subsequent elements, which is materially different from an incomplete separately tracked data category.

For varint/zigzag or signed/unsigned changes, seek source-grounded expected bytes for distinguishing nonzero and, where permitted, negative values. Two packet paths made internally consistent can still share the wrong encoding. If the external contract is unavailable, identify the needed evidence without asserting which encoding vanilla requires.

## Separate wire values from public semantics

Compare named mapper values, raw ordinals, runtime IDs and model state IDs deliberately. Stable semantic names can remove version-specific consumer branches without changing wire bytes; deleting a mapper to accommodate one numeric caller changes that contract. Check all affected readers, writers, examples and public declarations before changing representation.

Do not generalize strict validation into rejection of every unknown value. An unknown symbolic name or unintended undefined value can be an error while an unknown numeric enum ID deliberately survives read→write through a proxy. Check the type's documented escape hatches and caller roles. Test interpreted and compiled implementations where both exist, including read, write and size calculations. Preserve intentional absent-value types. Validate an encoding with boundary and out-of-enum values when ordinary small values make distinct codecs appear equivalent.

For version scope, locate introduction and subsequent changes; the version where a bug was discovered is not its introduction. Fix other affected supported versions when evidence establishes the same defect. Do not invent backports before a type existed or require every historical version for a new optional data capability. Runtime-extensible dimensions and registries should not become closed vanilla enumerations without an explicit contract change.

## Follow the integration boundary

Prefer source normalization or an existing shared owner over compensating consumer branches when semantics permit it. Generic codec primitives suggest ProtoDef ownership; versioned Minecraft facts suggest data ownership; mutable negotiated values need the relevant session registry. Name concrete consumers and migration costs. A working local correction can land before a broader ownership move when that move is not necessary to preserve behavior.

Choose validation that distinguishes the alleged defect: a source-grounded byte fixture, encoder/decoder boundary case, registry lookup or a real client/server exchange. Symmetric loopback tests can share the same wrong assumption; record that limit. For authentication or signed chat, state online/offline configuration and verify the relevant post-login behavior. For dependency changes, show the candidate branch or revision actually exercised by protocol and affected model/bot/server tests, then check release readiness separately.

A review finding should connect one changed contract to a concrete input, affected version and observed or traced consequence. Label unexecuted reasoning and remaining uncertainty. Recheck the current head and existing discussion so already corrected historical concerns are not posted again; useful follow-up architecture work and a demonstrated landing blocker are separate decisions.
