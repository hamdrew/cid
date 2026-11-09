# Research: Bounded game understanding pass

**Feature**: [spec.md](spec.md) · **Baseline**: [existing coach research](../001-ai-game-coach/research.md)

## Game understanding design research — 2026-11-08

This expansion is based on the owner's request and the current local implementation,
not fresh claims about external host capabilities or any particular game. Read-only
research examined the [policy](../../coaching/COACH.md), [data model](data-model.md),
[baseline coaching contract](../001-ai-game-coach/contracts/coaching.md), [baseline workspace contract](../001-ai-game-coach/contracts/workspace.md),
[templates](../../templates/records/knowledge.json) and
[model-free validator](../../tests/test_contracts.py). Separate repository research
covered storage and bounded workflow; it did not simulate or evaluate coaching.
The following decisions resolve all technical unknowns for this expansion.

### 1. Connected understanding through existing findings

- **Decision**: Retain JSON v1. Create a useful `overview` topic on demand, or extend
  an existing equivalent using the [overview lookup order](data-model.md#overview-lookup).
  Save actual loop/progression explanations and relationships in findings, with
  substantive topic details where needed. Use evidence for sourced relationships
  and `derived_from` for actual reasoning dependencies.
- **Rationale**: Findings already distinguish `fact`, `sourced_strategy` and
  `deduction`, with applicability, spoiler metadata, evidence and review status.
  Statements can explain system interactions without a separate graph schema.
  An overview should carry enough explanation to orient future reasoning, not only
  links, topic names or a completion claim.
- **Alternatives considered**: A dedicated understanding object duplicates findings
  and their provenance. A completion boolean becomes stale. A graph database or
  companion runtime adds no required capability. Fixed topic/source quotas measure
  quantity rather than useful understanding.

### 2. Limits and questions without a migration

- **Decision**: Put finding-specific unknowns in `applicability.notes`; retain a
  compact pass-wide gap note on an overview finding or the most relevant supported
  topic finding while the overview is pending. If all evidence is unavailable,
  retain useful unanswered needs in the selected run's `questions` and accurate
  access observations in the relevant index. Mechanics-informed player questions
  also use `questions`. Answers become reported `entries`.
- **Rationale**: This preserves explicit gaps alongside the knowledge they limit and
  keeps unsupported ideas out of supported mechanics. Game-wide findings never
  depend on a run's state. Reusable questions can be generated from saved mechanics;
  a permanent question bank is unnecessary.
- **Alternatives considered**: A new `unknown` finding kind conflicts with the current
  support rules. Optional coverage metadata is possible but unnecessary while
  existing notes suffice. An independent research backlog would encourage collecting
  unrelated topics rather than answering the player.

### 3. Broad orientation followed by relevant depth

- **Decision**: Understand the actual game's core loop, progression and consequential
  systems broadly, then deepen only relevant choices, readiness factors and
  bottlenecks around progress/goals/interests. Use the existing evidence ladder at
  every unmet information need. Questions must discriminate between plausible actions.
- **Rationale**: Quest-only knowledge cannot support broader coaching; exhaustive
  breadth delays help and risks spoilers. Game-specific mechanics determine the
  domains and interview, rather than assuming equipment, crafting or skill trees.
- **Alternatives considered**: A fixed RPG checklist misses other game structures;
  researching only the immediate quest repeats the reported problem. A full interview
  before helping violates skippable setup. No new dependency or host API is needed.

### 4. Content-based bounds and honest partial coverage

- **Decision**: Stop when the adequacy criteria in the
  [pass contract](contracts/game-understanding.md#adequacy-and-stopping) are met.
  Stop earlier when a player limit, inaccessible or conflicting evidence, protected
  material, diminishing relevant returns or a missing player answer prevents useful
  further research. Save specific limitations. New searches must address a named
  unmet criterion or material decision.
- **Rationale**: Source counts, minutes and question quotas do not establish
  understanding. A partial stop bounds the pass even when full adequacy is impossible.
  Quick help stays within the current limit. A later request can reopen a temporary
  deferral. Explicitly lasting run restrictions use existing reported constraints.
- **Alternatives considered**: Fetch-until-complete has no safe bound. Arbitrary
  tool budgets can stop before useful evidence or reward redundant fetches. A fixed
  detailed encyclopedia violates scope. Thorough depth still stays relevant/bounded.

### 5. Reuse, refresh and validation

- **Decision**: Broad coaching loads the overview/equivalent plus relevant topics;
  narrow lookups load only what they need. Judge content adequacy even in legacy
  records. Reuse applicable supported explanations without reopening adequate sources.
  Reassess applicability for the selected run when its version changes. Keep shared
  findings supported within their verified coverage. Reopen shared findings and
  their dependents when evidence undermines that coverage, preserving provenance
  and unaffected records.
- **Rationale**: The existing registry, derivations, plan dependencies and per-file
  save/recovery ordering already support incremental improvement and targeted review.
- **Alternatives considered**: Full recrawls, automatic expiry and background updates
  have no demonstrated need. Resetting old records loses valid knowledge/preferences.
- **Validation decision**: Run deterministic local checks only. Focused fixture checks
  can show that explanatory findings, cross-topic premises, limits and questions fit
  v1 and survive record validation. They cannot prove that prose is substantive or
  coaching is informed. Optional ordinary-use feedback remains the behavioral evidence;
  no AI sessions, model APIs, simulation agents or graders may be launched for tests.
