# Data model: Game understanding

**Feature**: [spec.md](spec.md) · **Baseline**: [portable v1 records](../001-ai-game-coach/data-model.md)

The baseline defines all entity fields, validation rules, relationships and state
transitions. This expansion reuses those definitions; the conventions below explain
its additional content without duplicating or changing the completed contract.

## Game understanding in existing v1 records

This planned expansion adds content conventions, not fields, enums or record types.
Existing files remain valid; no migration, reset or mandatory empty overview is needed.

| Output | Existing representation |
| --- | --- |
| Connected mental model | Substantive findings about loop, progression, main systems and connections in the topic selected by [Overview lookup](#overview-lookup). Register a new topic in `game.json.topics` after verifying its file. |
| Mechanics and interactions | `findings[].statement` explains what affects what and why it matters; `kind: fact` requires accessed supporting evidence |
| Published approaches and tradeoffs | `kind: sourced_strategy`, with evidence identifying the supported strategy and its conditions |
| Original synthesis | `kind: deduction`, with applicable supported premise references in `derived_from`; retain its untested nature |
| Evidence and coverage | Existing `evidence`, `checked_at`, `applicability`, `spoiler`, and source access/quality fields |
| Gaps and pass limits | Relevant `applicability.notes`, with a compact pass-wide note on an overview finding or, while the overview is missing, the most relevant supported topic finding |
| Material player questions | Selected playthrough's `questions`; explanatory `text` can name why the detail affects the decision without revealing protected mechanics |
| Answers and advice | Reported `entries` and separate `plans` referencing supported findings and relevant run context |
| Explicitly lasting run research restriction | Current reported constraint in that run's `entries`. Supersede or retract it when the player changes or lifts the restriction. |

The overview is a content role, not a second source of truth. Several findings may
express its connected model; split independently uncertain claims so one finding's
status/applicability is not misleading. A directly sourced relationship needs no
invented derivation. Use `derived_from` where the explanation actually depends on
other findings, not as a general network of every system interaction; this keeps
the reasoning graph acyclic even when game systems influence each other.

Notes explicitly identify unknown, deferred, disputed or version-limited areas and
what would justify targeted research. Label pass-wide limits separately from the
finding's own coverage. When saving an overview, verify that it retains any
still-relevant pass-wide note before removing the old copy. An unrelated gap leaves
the finding's support status intact. If all evidence is unavailable, save useful
unresolved needs as run questions and record accurate source access observations.
Create no fake finding just to hold a gap. Partial coverage is not a persisted
completion flag.

Keep game-level notes independent of player state. A reusable mechanic can inform
questions, but a player's current resources/readiness belongs in their run. Source
links alone, empty categories and “researched the game” do not constitute an overview.

## Overview lookup

For broad coaching, check the registered `overview` topic first. If it is absent
or lacks enough applicable content, check legacy candidates in registry order.
Candidates are registered topics named `foundation` or `basics`, IDs ending in
`-overview`, and registered topics already needed for the request. A candidate
qualifies by containing substantive, supported explanations connecting the loop,
progression and main systems. Reuse the first applicable equivalent in place and
follow only relevant premises. If
none qualifies, extend an existing valid `overview`, or create it when there is a
supported overview finding to save. Leave other topics in place and use the normal
recovery rules for missing registry targets or unpublished files. Narrow requests
can skip this lookup.

## Version applicability and evidence review

Reassess premises, overview findings and plans against the selected run's version.
A shared finding can remain supported within its verified coverage and be
inapplicable to the selected run. Mark affected plans in that run `needs_review`
when they cannot be reused as settled. When evidence undermines a shared claim
within its verified coverage, use the existing finding `needs_review`/`disputed`
transitions for that claim and dependent overview findings. Reassess dependent
plans before reuse and retain superseded provenance. The
[pass contract](contracts/game-understanding.md) defines adequacy.
