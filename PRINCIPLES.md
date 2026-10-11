# PrismarineJS principles

Date: 2026-10-11. Source: rom1504's explicit principles and approved adoption plan
in the maintenance conversation. The explanatory guidance below was drafted by
Astra. [MATTER](https://rom1504.github.io/matter.png) provides related motivation;
it does not add requirements beyond the maintainer's principles.

PrismarineJS should make Minecraft capabilities easier to understand, extend and
compose into many applications. Individually reasonable changes do not ensure a
good system. Apply these principles to **existing code and the architecture that
changes accumulate into**, as well as to individual PRs.

These are the intended direction, not a claim that every package already follows
them. Preserve working knowledge, demonstrate improvements against existing
behavior, and make gaps and migration choices explicit.

<a id="p1"></a>

## P1 — Data-centric

**What can be shared Minecraft data belongs in `minecraft-data`, rather than
being scattered through code.**

Represent versioned facts, protocol descriptions and feature knowledge once,
with useful schemas, extraction provenance and validation. Consumers should
interpret shared data instead of maintaining competing tables or deriving the
same authoritative fact independently. Prefer data that serves PrismarineJS
capabilities over an unstructured dump of an extractor's implementation details.

Distinguish static Minecraft facts from negotiated registries and live world
state. A server's current registry or a bot's loaded columns is runtime state;
it must not be treated as a universal fact in `minecraft-data`. Computation can
remain an algorithm; data-centric does not mean a new configuration language
for every conditional.

**Look for:** duplicated version tables, scattered numeric IDs, consumer-specific
fallbacks becoming de facto shared facts, and extraction formats leaking into APIs.

<a id="p2"></a>

## P2 — Loosely coupled, independently tested modules

**Use modular packages with as loose coupling as possible. Each package must be
well tested independently so it can be reused.**

Put a coherent responsibility behind explicit inputs, outputs and dependencies.
A chunk model, codec or geometry operation should be usable without constructing
a bot, server or viewer. Tests should exercise each package's actual contract;
consumer integration tests establish that the packages also work together.
Follow existing repository harnesses rather than inventing fake application
objects to claim independence.

Package count is not the objective. An internal helper may be the right first
step when no independently useful package contract exists. Extraction must
reduce coupling, not relocate it into callback bundles or implicit shared state.

**Look for:** bot-dependent model helpers, circular responsibilities, duplicated
representations, and packages whose only meaningful validation lives downstream.

<a id="p3"></a>

## P3 — Separate computation from state

**Separate computation from mutable state and its management.** This is an
important direction that PrismarineJS does not yet follow consistently.

Make calculations and decisions usable with explicit inputs and results. Give
state storage, mutation, I/O and scheduling identifiable owners. For example,
decoding an update, deciding its effect on a model, applying that effect, and
notifying consumers are distinct responsibilities even if initially implemented
in one package. An explicit read interface or snapshot can support computation
without copying an entire world.

This does not prohibit mutable chunk storage, caches, classes or efficient
incremental updates. Require clear dependencies and mutation ownership; prefer
pure operations where practical. An extra object or event bus alone does not
separate computation from state.

**Look for:** calculations that silently modify bot state, multiple writers with
inconsistent update semantics, and logic that cannot run without network or timers.

<a id="p4"></a>

## P4 — All-version support keeps abstractions honest

**Support all Minecraft versions as a forcing function to keep code generic.**

Design shared algorithms around versioned data, capabilities and explicit format
adapters. Keep real protocol differences visible. Adding a version should usually
extend knowledge or an adapter rather than duplicate a subsystem. Establish the
actual Java/Bedrock and historical-version scope of each package; record gaps
rather than silently redefining the goal around whatever the newest version does.

Use established version matrices to exercise shared contracts and significant
representation boundaries. Supporting an old version does not require inventing
a mechanic absent from that version. A declaration of support is not evidence
that its implementation or tests are complete.

**Look for:** newest-version assumptions in generic code, unexplained version
branches, copied release-specific suites, and removal of old coverage to simplify a fix.

<a id="p5"></a>

## P5 — Expose capabilities through libraries

**Libraries should expose functionality so many applications can be built with it.**

Make underlying models and operations available through documented, usable APIs.
Keep application policy and orchestration at the application boundary. Consider
bots, servers, proxies, viewers, analysis tools and consumers not yet imagined;
distinguish verified reuse from hypothetical consumers.

A library contract should explain inputs, results, ownership and failure behavior.
An application can provide a convenient higher-level API without becoming the
only way to access a fundamental capability. Reuse does not require publishing
every internal helper or prematurely generalizing every application-specific action.

**Look for:** reusable behavior accessible only through a bot plugin, hidden
required setup, and library initialization that imports application-only effects.

<a id="p6"></a>

## P6 — Establish standards other languages can implement

**Try to establish standard implementations and contracts that other languages
can follow.**

Make shared schemas, semantics, formats and examples understandable independently
of JavaScript source. Where useful, provide portable input/output fixtures for
conformance: coordinate conventions, integer widths, missing-value behavior,
state transitions and serialization rules should be explicit.

A reference implementation should clarify a contract, not force other languages
to copy JavaScript classes, mutation tricks or dependency structure. Distinguish
PrismarineJS conventions from Mojang wire formats and from standards already
adopted elsewhere. Do not claim adoption or compatibility without evidence.

**Look for:** behavior specified only by JavaScript coercion, JSON that loses
required integer precision, and incompatible interpretations of the same shared data.

## Applying the principles

Use [system review](skills/prismarine-system-review/SKILL.md) to assess an existing
capability across its owning packages and consumers. Record evidence, what works,
what diverges, the concrete cost, and a coherent target with incremental steps.
Store dated proposals in `design/phaseN/` and investigation/outcome records in
`implementation/phaseN/`; these principles remain the stable reference.

For a PR, use [PR review](skills/prismarine-review/SKILL.md) to determine whether
the resulting system improves, preserves or worsens the relevant direction.
Separate newly introduced debt, debt the change amplifies, and unrelated existing
debt. A bounded repair can land while a broader migration remains explicit.
An assessment proposed by an agent is not an accepted maintainer design.

When principles conflict, describe the tradeoff and prefer a demonstrated,
bounded improvement over abstraction for its own sake. Record an accepted
exception with the maintainer decision, affected scope, reason and a condition
for revisiting it. Distinguish that from an unresolved gap or a proposed deferral.
Do not silently turn historical compromises into new principles, or use a
principle as a reason to rewrite working code without examining its constraints.
