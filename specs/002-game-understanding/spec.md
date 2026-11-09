# Feature Specification: Bounded game understanding pass

**Feature Branch**: `main` (current Git branch; feature identifier: `002-game-understanding`)

**Created**: 2026-11-08

**Status**: Draft specification and design complete; not implemented

**Input**: Expand Cid's initial research into a bounded, reusable understanding of
a game's loop, progression, systems and relationships, meaningful choices and
player-context needs. Save substantive sourced knowledge and a connecting overview,
then reuse and deepen it across conversations while preserving research preferences,
existing records and spoiler protections.

This feature extends the completed [local coach](../001-ai-game-coach/spec.md).
A few generic facts or the next quest objective can support a narrow answer but
cannot provide the mental model needed for an informed coaching conversation.
The player should be able to discuss why systems interact, compare concrete
tradeoffs and explore useful approaches beyond quest advancement.

## User Scenarios & Testing *(mandatory)*

The observations below can guide ordinary use and optional feedback. They are not
a mandatory campaign, trial quota or scoring system. No development agent may
launch AI sessions, model APIs, automated players or graders for testing. Record
validity and observed conversational quality remain separate kinds of evidence.

### User Story 1 - Establish useful game understanding (Priority: P1)

A player introduces a game for ongoing coaching. Cid develops a broad,
spoiler-safe picture of how it works before focusing on the player's situation.

**Why this priority**: Richer coaching needs connected knowledge rather than a
walkthrough of the immediate objective.

**Independent Test**: During normal use, introduce a game and goal. Inspect whether
Cid can explain its loop, progression and major system relationships, and whether
the saved knowledge contains substantive explanations with support and limits.

**Acceptance Scenarios**:

1. **Given** a new game and ongoing coaching, **When** initial research occurs,
   **Then** Cid learns the core loop, overall progression and major systems and
   explains how those systems affect each other and meaningful choices.
2. **Given** a current quest or objective, **When** Cid develops understanding,
   **Then** locating its next step does not substitute for learning the game.
3. **Given** a game without character builds, crafting or quests, **When** Cid
   researches, **Then** it chooses domains from that game's actual mechanics and
   does not impose an RPG checklist or create irrelevant empty categories.
4. **Given** useful research, **When** it is saved, **Then** concise topic findings
   and a connected overview retain actual explanations, evidence and applicability;
   a source list or generic statements alone do not satisfy this story.

---

### User Story 2 - Discuss informed choices (Priority: P1)

A player asks about a goal, difficulty or possible direction. Cid uses its game
understanding to ask informed questions and explain useful options and tradeoffs.

**Why this priority**: Understanding creates value through the conversation and
better decisions, rather than through collecting material alone.

**Independent Test**: Discuss a goal during ordinary use. Observe whether questions
and advice depend on researched mechanics and the player's answers, and whether
concrete benefits, costs and uncertainty are explained.

**Acceptance Scenarios**:

1. **Given** researched mechanics but missing material player details, **When** Cid
   prepares advice, **Then** it asks brief, skippable questions that distinguish
   plausible choices; a known quest location is not a complete readiness profile.
   The initial interview prioritizes the unknowns most likely to change coaching,
   based on the game understanding and the player’s goal and current situation.
   For example, level and loadout may be more useful than potion count, though
   consumables matter when they affect the immediate decision.
2. **Given** relevant progress, goals and interests, **When** Cid deepens research,
   **Then** it focuses on consequential decisions, readiness factors, tradeoffs and
   common bottlenecks rather than expanding every possible topic.
3. **Given** a goal with useful alternatives to quest advancement, **When** Cid
   coaches, **Then** it can explain feasible game-appropriate options and their
   concrete tradeoffs without forcing unrelated alternatives into a narrow answer.
4. **Given** an original strategy based on researched mechanics, **When** Cid saves
   or explains it, **Then** important deductions remain distinct from verified
   mechanics and sourced strategies, with their supporting premises retained.

---

### User Story 3 - Reuse and deepen understanding (Priority: P1)

A player returns later or starts another run. Cid reuses the saved game model,
collects only missing run context and deepens knowledge where it becomes useful.

**Why this priority**: A reusable model should prevent repeated setup and research
while remaining correctable as goals, versions and evidence change.

**Independent Test**: Resume ordinary coaching from saved records and discuss a
new interest. Inspect whether prior knowledge is reused and only affected gaps or
conflicting findings receive further research.

**Acceptance Scenarios**:

1. **Given** adequate applicable saved understanding, **When** a fresh conversation
   begins, **Then** Cid can reason from it without repeatedly fetching the same
   adequate sources or asking for already recorded player details.
2. **Given** a new run of the same game, **When** coaching begins, **Then** game
   knowledge is reused while progress, goals, questions and plans stay run-specific.
3. **Given** a thin legacy foundation, **When** broader understanding becomes
   relevant, **Then** Cid preserves valid material and incrementally adds missing
   relationships and decision context; file existence does not prove adequacy.
4. **Given** a changed version or conflicting evidence, **When** affected knowledge
   is reused, **Then** Cid revisits its applicability and dependent overview/advice,
   retains provenance and preserves unaffected knowledge and player records.
   A finding still supported for another run's version remains reusable there.

---

### User Story 4 - Keep research bounded and player-directed (Priority: P1)

A player can receive useful help without waiting for exhaustive research or
completing a questionnaire, and can request quick answers or reduced depth.

**Why this priority**: Research should enrich coaching without becoming a barrier
to it or revealing discoveries that the player wants protected.

**Independent Test**: During normal use, request a quick answer or skip a question.
Observe narrower supported help and explicit limits, without an enforced full pass.

**Acceptance Scenarios**:

1. **Given** sufficient understanding to explain the main systems and relationships,
   identify useful player questions and recognize targeted research needs, **When**
   Cid assesses further research, **Then** it stops the broad pass and helps.
2. **Given** a quick-answer request, reduced research preference or skipped question,
   **When** Cid responds, **Then** it honors that limit and gives narrower or
   conditional guidance without guessing or requiring setup completion.
   A later request for more depth can reopen a temporary deferral. An explicitly
   lasting restriction remains in effect within its stated scope until changed.
3. **Given** inaccessible evidence, unresolved conflict or an uncertain spoiler
   boundary, **When** full understanding cannot be established productively,
   **Then** Cid retains partial knowledge and explicit gaps, and asks a useful
   question or gives supported limited help rather than researching indefinitely.
4. **Given** spoiler-sensitive material in research or stored knowledge, **When**
   Cid explains systems, asks questions or presents sources, **Then** existing
   spoiler protections cover the whole output; access does not grant disclosure.

### Edge Cases

- Ambiguous game identity or consequential edition/version differences must be
  resolved before dependent factual claims; irrelevant setup questions are omitted.
- A single suitable source may explain several systems; numerous weak sources do
  not establish understanding. Fixed source/category quotas cannot prove adequacy.
- Circular influences among game systems do not justify circular reasoning or
  unsupported claims about their relationships.
- No verified finding is available: preserve useful unanswered needs and accurate
  access limitations without inventing mechanics to fill a knowledge record.
- Known mechanics but unknown player readiness: ask or give conditional help,
  rather than continue broad searches while waiting for player information.
- A one-off quick request does not change a lasting preference. Resume deferred
  research only when it serves a later request, within any standing limits.
- Failed or unconfirmed saving identifies the specific unpersisted knowledge or
  player update; existing valid records must not be reset to make setup succeed.
- Later discoveries, source labels and questions can themselves spoil content;
  a partial model is preferable to crossing an unapproved disclosure boundary.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: For a new game and ongoing coaching, Cid MUST establish a bounded,
  broad, spoiler-safe understanding rather than only solve the immediate objective.
- **FR-002**: Understanding MUST cover the core gameplay loop and overall
  progression structure in enough detail to explain how capability or progress changes.
  The core loop means the recurring player actions, feedback and decisions that
  sustain play. Progression can mean changing match/run state, skill, strategic
  position, resources or player-defined goals; it need not mean quests, levels or
  permanent unlocks. Describe what persists and whether there is a fixed path
  separately. If either is absent, explain the meaningful changes within play.
- **FR-003**: Cid MUST identify the actual game's major systems and explain their
  consequential relationships. Activities, skills, equipment, crafting, resources
  and exploration are examples, not mandatory categories or an RPG checklist.
- **FR-004**: Research MUST identify important decisions, concrete tradeoffs,
  readiness factors and common bottlenecks where supported by evidence.
  Distinguish documented gates from optional sourced preparation and inferred
  readiness advice; only an evidenced gate may be described as required.
- **FR-005**: Cid MUST use researched mechanics to identify material player details
  and ask informed, brief, skippable questions. In the initial interview, it MUST
  prioritize unknowns by their likely impact on coaching for the specific game,
  player goal and situation. It MUST omit known or irrelevant details and avoid a
  complete stat sheet or inventory requirement.
- **FR-006**: Cid MUST establish broad understanding first, then deepen relevant
  areas around the player's progress, goals and interests. It MUST use that
  understanding to identify useful approaches beyond quest advancement when relevant.
- **FR-007**: Cid MUST persist substantive, concise, sourced findings in existing
  knowledge records plus an overview connecting the topics. Saved explanations MUST
  support future reasoning; generic statements, category lists or source links alone
  MUST NOT satisfy this requirement.
  Topic findings retain relevant mechanics, conditions, effects and limits without
  requiring the original page to be reopened; the overview explains how those
  topics connect and why the relationships matter for choices.
- **FR-008**: Saved knowledge MUST distinguish verified mechanics, sourced strategies
  and deductions, retaining supporting evidence or premises and applicability.
  Model familiarity and player testimony alone MUST NOT verify universal mechanics.
  Overview claims follow the same rule: separate independently supported or uncertain
  claims so a verified component does not imply that the whole synthesis is verified.
- **FR-009**: Cid MUST retain explicit knowledge gaps, uncertainties, version limits
  and useful deferred needs, plus material unanswered player questions. Unknown
  mechanics MUST NOT be promoted to verified facts.
- **FR-010**: The normal pass MUST stop when Cid can explain the loop, progression
  and main system relationships, identify consequential choices, tradeoffs, readiness
  factors and bottlenecks where supported, and identify material player questions
  and gaps needing targeted research. It MUST stop earlier if a player limit or
  unavailable, conflicting, protected or unproductive evidence prevents useful further
  research. Retain partial coverage explicitly when an unmet material criterion remains.
- **FR-011**: The pass MUST NOT become an exhaustive encyclopedia, full website
  mirror or inspection of game code. Further research MUST address a material
  remaining understanding need or relevant decision rather than unrelated branches.
- **FR-012**: Cid MUST honor quick answers, reduced research, skipped questions and
  redirection, continuing supported narrower or conditional help. Reduced depth
  MUST NOT permit invented facts, and deferred research MUST NOT become mandatory.
  An ordinary quick request, deferral or refusal limits the current work. A later
  request can make that gap relevant again without another confirmation. Cid MUST
  carry forward a research restriction only when the player explicitly makes it
  lasting, and apply it within the player's stated scope. If a later request appears
  to conflict with that restriction, ask neutrally before crossing it unless the
  player explicitly changes it. Persist lasting depth preferences only on request,
  using the existing scope rules.
- **FR-013**: Cid MUST reuse and incrementally deepen applicable saved understanding
  across conversations and runs, without repeatedly fetching adequate unchanged
  sources or repeating answered questions. Game knowledge and run state MUST stay distinct.
- **FR-014**: Version changes or evidence conflicts MUST trigger reassessment of
  affected findings, overview dependencies and advice before reuse, retaining
  provenance and preserving unaffected records. A run's version change MUST NOT
  downgrade shared findings that remain supported within their verified coverage.
- **FR-015**: This expansion MUST preserve existing workspace records, preferences,
  spoiler protections, evidence-selection order, correctable assumptions and save/
  recovery behavior. Missing or failed research/saves MUST remain explicit limits,
  not reasons to guess, reset records or bypass the player's choices.

### Key Entities *(include if feature involves data)*

- **Game understanding overview**: A reusable explanation connecting the game's
  loop, progression, major systems and choices, with explicit coverage limits.
- **Knowledge finding**: A concise mechanic, sourced strategy or deduction, retaining
  evidence/premises, applicability, uncertainty and spoiler context.
- **Source reference**: Evidence location, coverage and access/quality context,
  sufficient to judge whether later consultation is needed.
- **Knowledge gap**: A specific unknown, conflict, version limit or deferred area
  and its relevance to further research; not an asserted mechanic.
- **Player-context question**: A material missing detail informed by researched
  mechanics; its answer informs the selected run rather than universal game facts.
- **Playthrough context and advice**: Reported progress/goals/preferences and
  proposed plans, distinct from reusable game knowledge and correctable assumptions.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For ordinary new-game coaching, the saved understanding supports an
  explanation of the core loop, overall progression and consequential relationships
  among the main systems. Generic facts, a quest step or a link collection alone fail.
- **SC-002**: In a relevant coaching decision, Cid can explain concrete benefits,
  costs and readiness considerations, identify useful game-appropriate options beyond
  quest advancement, and ask questions whose answers materially change the advice.
  A consequential option names a feasible action, its relevant benefit and cost
  (including time, resources, risk or opportunity cost), and a readiness factor
  that affects feasibility or value. A generic suggestion or the next objective
  alone does not meet this criterion; unsupported costs or thresholds cannot fill it.
- **SC-003**: A fresh conversation can use saved explanations and reported context
  without re-fetching adequate unchanged sources or requiring repeated answers.
- **SC-004**: Saved mechanics, sourced strategies and deductions remain distinguishable
  with supporting evidence/premises, applicability and explicit gaps or version limits.
- **SC-005**: A quick/reduced-research request or skipped question yields useful
  supported narrower/conditional help without forcing completion of the broad pass.
- **SC-006**: A consequential version/conflict change prevents affected knowledge
  from being reused as settled, while unaffected research, preferences, progress
  and spoiler protections remain intact.

These are observable personal-use outcomes, not numerical quotas, certification
scores or permission to launch AI testing. The owner may send bullet-point feedback
and optionally share evidence for review in the current conversation. Unobserved
conversational behavior remains unknown; deterministic record checks alone do not
establish that explanations or advice are useful.

## Assumptions

- The completed coach's existing shared behavior, source access, local persistence,
  context separation and preference handling remain the baseline, not new scope.
- The player supplies progress, goals and corrections; no save ingestion, telemetry
  or autonomous gameplay is introduced.
- Source access is not guaranteed. Partial understanding and explicit uncertainty
  are valid outcomes when research cannot productively continue.
- Main systems and sufficient depth depend on the game and coaching need; there is
  no fixed list of genres, categories, sources, questions or completion percentage.
- Broad understanding does not require later story details or every unlock; existing
  disclosure preferences and known player boundaries continue to govern output.
- The constitution's principles I–V apply: evidence and applicability (FR-008/014/015),
  durable records (FR-007/013/015), correctable advice (FR-014/015), spoilers
  (FR-001/010/015) and player-directed help (FR-005/006/010/012).
- No hosted service, custom model integration, exhaustive database, background
  recrawl, new mobile infrastructure or automatic destructive migration is in scope.
