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
| Connected mental model | `knowledge/overview.json` (or an existing equivalent), containing substantive ordinary findings about loop, progression, main systems and connections; register the topic in `game.json.topics` after verifying its file |
| Mechanics and interactions | `findings[].statement` explains what affects what and why it matters; `kind: fact` requires accessed supporting evidence |
| Published approaches and tradeoffs | `kind: sourced_strategy`, with evidence identifying the supported strategy and its conditions |
| Original synthesis | `kind: deduction`, with applicable supported premise references in `derived_from`; retain its untested nature |
| Evidence and coverage | Existing `evidence`, `checked_at`, `applicability`, `spoiler`, and source access/quality fields |
| Gaps and pass limits | Relevant `applicability.notes`; a compact overall coverage/deferred-gap note on an overview finding, clearly separate from its supported statement |
| Material player questions | Selected playthrough's `questions`; explanatory `text` can name why the detail affects the decision without revealing protected mechanics |
| Answers and advice | Reported `entries` and separate `plans` referencing supported findings and relevant run context |

The overview is a content role, not a second source of truth. Several findings may
express its connected model; split independently uncertain claims so one finding's
status/applicability is not misleading. A directly sourced relationship needs no
invented derivation. Use `derived_from` where the explanation actually depends on
other findings, not as a general network of every system interaction; this keeps
the reasoning graph acyclic even when game systems influence each other.

Notes explicitly identify unknown, deferred, disputed or version-limited areas and
what would justify targeted research. Do not store unknown mechanics as supported
facts or mark an otherwise supported claim disputed merely because an unrelated
area is unresearched. If all evidence is unavailable, save useful unresolved needs
as run questions and accurate source access observations; create no fake finding
just to hold a gap. Partial coverage is not a persisted completion flag.

Keep game-level notes independent of player state. A reusable mechanic can inform
questions, but a player's current resources/readiness belongs in their run. Source
links alone, empty categories and “researched the game” do not constitute an overview.

On resumption read the overview for broad coaching, follow only relevant premises
and topics, and respect each finding's applicability/status. A version/conflict
change uses existing `needs_review`/`disputed` transitions, traverses dependent
findings and selected-run plans before reuse, and retains superseded provenance.
Refresh affected overview claims along with their premises; unchanged facts remain
reusable. The [pass contract](contracts/game-understanding.md) defines adequacy;
JSON validity alone cannot establish it.
