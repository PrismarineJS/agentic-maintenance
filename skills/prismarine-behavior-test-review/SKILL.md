---
name: prismarine-behavior-test-review
description: Review behavioral changes and regression tests across Mineflayer and PrismarineJS models, physics, protocol integrations and test infrastructure. Use to assess whether a test reproduces the user-visible failure, has a credible oracle and exercises the relevant lifecycle and dependencies.
---

# Behavior and test review

Start with the promised behavior and an observable failure, then choose the smallest existing test layer that can distinguish them. Mineflayer is one consumer of shared models and codecs; its external tests are not the default home for every regression. Read [precedents and scope exceptions](references/sources.md) when deciding how much evidence is necessary.

## Identify what the test actually establishes

Write down the trigger, required initial state, action, expected observation and why the prior implementation fails. A test calling a helper and asserting its own formula may repeat the implementation rather than test a contract. A test should exercise the relevant production path, with an expectation grounded in a public behavior, independent fixture or protocol/source evidence.

If a claim depends on a fixture containing multiple entries or a particular ordering, inspect that fixture and the relevant decoder before stating that the current test fails. A valid counterexample within an established public input contract can stand on its own; an assumed private fixture is a different evidentiary basis.

Match the layer to the claim:

- Model ownership or geometry: prefer the existing item/entity/chunk/world/physics suite when the public model behavior is sufficient. Include the real boundary, such as a ray starting inside a block or an entity detaching while its vehicle reference is updated.
- Packet shape, codec or lifecycle ordering: use the real parser/serializer or protocol client/server path as needed. A fake bot may bypass registry initialization, event delivery or state transitions that cause the defect.
- Server action: prove the server acted, such as changing the world or authoritative inventory. A chosen packet name, local flag or emitted event alone does not prove consumption, placement or movement succeeded.

These are decision criteria, not a required three-layer test suite. Existing evidence can suffice for a narrow change. An isolated helper test, real NMP loopback and vanilla server test provide different guarantees; report which was used. Loopback can miss a shared encoding mistake, and a modified downstream consumer does not establish compatibility with its released version.

## Audit fixtures and synchronization

Establish where fixtures came from: actual captured bytes, source-derived values, generator output or this same library's serializer. Record edition/version and applicable server configuration. Do not replace failing golden data until its provenance and intended invariant are understood. Byte-for-byte roundtrip is appropriate only if the contract preserves every encoded detail; documented canonicalization or discarded non-vanilla excess data can justify scoped semantic assertions instead.

Construct actual action preconditions: solid target face, loaded state, position/reach, inventory and version-appropriate world coordinates when relevant. Awaiting a synchronous chat call does not await server command completion. A delay cannot make an invalid scenario valid.

Prefer existing condition-aware waits that handle already-satisfied state, bound failure and clean up listeners. Subscribe before a possible synchronous event. Trace which promise callers receive before alleging swallowed errors; cleanup-chain rejection handling can differ from operation failure. For repeated configuration, respawn, reconnect or concurrent requests, check registration lifetime and authoritative state after re-entry, not just the first event. Add those scenarios when the changed lifecycle makes them reachable.

## Preserve the behavior the harness promises to test

Check that the test runs and reaches its assertion: version lists, ignore rules, filters, skipped branches and early exits can create false passes. Ensure the candidate dependency and matching data revision are actually installed. A temporary branch pin can demonstrate integration; its production release requirement is a separate landing check.

Trace the actual CI invocation and other jobs before calling a filtered-out suite missing coverage. A neighboring test's comment about a version filter does not establish that no unfiltered job runs the suite. Without the job configuration, keep that distinction explicit and frame the request proportionately.

Do not make tests pass by removing the default contract, such as bypassing auto-version detection, suppressing validation, patching away the server failure or testing a different dependency. Diagnose the actual failed operation before blaming timing or changing retries. Use a focused reproducer, packet/event trace and useful actual-versus-expected output. Separate an introduced regression from unrelated baseline, network or external-auth failures.

Retries can be justified for an identified transient problem when the restarted resource and residual uncertainty are clear; they are not a root-cause explanation. Use a targeted repeat only when it answers a reliability concern. Tests relying on external authentication should state configuration and constraints; mocking auth belongs at an appropriate auth boundary and does not automatically require private credentials for deterministic protocol tests.

## Make the review proportional

Ask for the missing evidence that could change the landing decision. Distinguish a demonstrated defect, an important validation gap and optional coverage debt. Historical maintainers sometimes accept smoke coverage, follow-up tests or incremental fixes; do not turn an expressed desire into an absolute blocker. Reuse a suitable existing harness before proposing a new framework or migration of all tests. A broad fixture redesign needs concrete recurring failures and a maintenance benefit of its own.

State what was inspected versus executed, the tested revision and the evidence's practical limit. Refresh the current head and previous discussion before commenting so a completed regression fix or already requested test is not posted again.
