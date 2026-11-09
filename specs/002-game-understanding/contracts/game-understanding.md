# Bounded game understanding contract

**Design date**: 2026-11-08 · **Requirements**: FR-001–FR-015 of [this feature](../spec.md) · **Implementation status**: planned

This feature extends the [baseline conversational interface](../../001-ai-game-coach/contracts/coaching.md). The pass is an internal
research workflow invoked through ordinary coaching requests, not a new command,
service or mandatory setup screen. Existing preference and spoiler rules apply.

## Entry and scope

For a new game and ongoing coaching, establish broad understanding first, then
deepen relevant areas around the player's progress, goals and interests. For an
existing game, assess saved content and fill material gaps; file existence or a
prior quest answer is not proof of adequate understanding. A new run reuses game
research while collecting its own context.

A limited lookup, “quick answer,” “less research,” “skip that” or “later” narrows
the present work. Continue with supported help within that limit.
Persist a lasting research preference only when requested, at the proper scope;
a one-off quick request leaves `research_depth` as it was. Brief uses the current
need, normal aims for the bounded foundation, and thorough permits deeper relevant
research while retaining the same stopping and spoiler rules.

When a later request makes a temporary deferral relevant again, research just that
need within the effective preferences. A player can explicitly set a lasting
restriction, such as “for this run, don't look up puzzle solutions.” Save a run
restriction as a reported constraint and reload it with that run. Apply any
broader standing restriction stated in the player's workspace instructions within
its stated scope. If a broader topic restriction has no standing record, honor
it in the current conversation and disclose that it is currently conversation-only.
If a later request appears to conflict with an active restriction, ask neutrally
before crossing it unless the player explicitly changes it. A skipped player
question stays unanswered until the player supplies the detail. Continue conditional
help and revisit it only when material.

## Research and coaching behavior

1. Resolve identity and relevant version ambiguity, selected run, effective
   preferences and known spoiler boundary. Read applicable knowledge, indexed
   sources and available integrations in the established evidence order before
   broad search. Do not re-fetch sufficient unchanged saved evidence.
2. Read suitable overview/mechanics material to understand the core gameplay loop,
   overall progression and major systems. Explain how the systems affect each
   other and meaningful choices. Activities, skills, equipment, crafting, resources
   or exploration are possible domains only when the actual game supports them.
   Avoid exhaustive item lists, walkthroughs, later unlock surveys or game-code inspection.
   The core loop is the recurring actions, feedback and decisions sustaining play.
   Explain what persists and whether progress follows a fixed path as separate
   properties. If either is absent, describe the meaningful changes in match/run
   state, skill, strategic position, resources or player-defined goals, as
   applicable. Major systems are the mechanics that materially affect the loop or
   the player's choices.
3. Identify important decisions, tradeoffs, readiness factors and common bottlenecks
   from supported mechanics/strategies. Distinguish a documented requirement from
   a suggested preparation strategy; do not invent thresholds or universal builds.
   Label inferred readiness advice as a deduction, with premises and uncertainty;
   neither it nor optional sourced preparation establishes a mandatory gate.
4. Use those mechanics to ask only material missing player questions. Explain the
   decision the answer changes when helpful. Skip known or declined details; do not
   demand a complete inventory/stat sheet or infer readiness from a quest location.
5. Deepen areas made relevant by the player. Provide a feasible action or choice,
   its concrete benefit/cost and material uncertainty. Consider preparation,
   exploration, practice, resource choices or other game-appropriate approaches
   beyond quest advancement when they serve the goal. Do not force extra options
   into a narrow answer. Label important untested deductions.

## Adequacy and stopping

The normal pass is adequate when the saved understanding lets Cid:

- Explain the core loop and progression, including how the main systems connect.
- Recognize consequential choices, tradeoffs, readiness factors and bottlenecks
  where supported, and use them to identify useful approaches for coaching.
- Identify the player details needed to choose among those approaches, with
  questions informed by the researched mechanics.
- Name gaps, uncertainties and version limits, and recognize which need targeted
  research before dependent advice.

Assess these by actual explanatory content and evidence, not a fixed number of
sources, topics, findings, questions or words. Do not mark adequacy from a few
generic statements, category names, next-objective facts or source links alone.
This is not encyclopedic completeness: unneeded specifics can remain deferred.

Each additional research step must address a named unmet criterion or material
decision; stop once additional coverage would not improve the explanation, choice
or next useful question. Do not follow newly discovered links into unrelated
branches. Stop earlier when a player limit, protected boundary, inaccessible evidence,
unresolved conflict or diminishing useful returns prevents useful further research.
Retain a partial model and its specific limits when a material criterion remains
unmet. If player information is the blocker, ask or give supported
conditional help rather than continue general searching. Do not repeat failed
searches without a changed need or access condition.

An adequate stop can explain the main relationships and meaningful choices from
retained support, name material player questions and distinguish targeted gaps.
An early partial stop explicitly names what could not be explained, why research
stopped, and which question or changed condition could help. Give supported general
or conditional guidance in either case; do not describe a partial stop as adequate
merely because some findings were saved. A known objective with unknown readiness
calls for the missing decision-changing context, not more broad research.

## Saved output and reuse

Save concise explanatory findings in existing topic files and a connected overview
in `knowledge/overview.json` or an existing equivalent, using the
[v1 conventions](../data-model.md#game-understanding-in-existing-v1-records).
An overview states the relationships and their coaching implications, with actual
evidence or supported premises; it does not merely point to other topics. Topic
findings retain enough substantive detail to support later reasoning without
opening the original pages again. Keep source links, access context and applicability.

Verified mechanics use `fact`; published advice uses `sourced_strategy`; original
synthesis uses `deduction` and `derived_from`. A supported deduction remains a
deduction. Retain coverage gaps and deferred areas in applicability notes. If
there is a supported topic finding but no supported overview finding, put the
pass-wide gap in the most relevant topic finding's notes as a separate coverage
note. Move any still-relevant pass-wide gap to the overview when it is saved.
Absent coverage remains unknown. Save selected-run questions and player answers
separately from game knowledge. Never create unsupported mechanics to fill a gap.
Split overview statements that combine claims with different support, applicability
or uncertainty; attach evidence to verified relationships, evidence and conditions
to sourced strategies, and retained premises to original deductions. If no claim
can be verified, keep useful unresolved needs in run questions and accurate source
access observations, without creating a fake finding. Unknown version coverage
remains an explicit applicability limit rather than presumed compatibility.

For broad coaching, use the [overview lookup order](../data-model.md#overview-lookup)
and load only the relevant topics and premises. Limited lookups load only the
records needed for the request. Reuse adequate research and reported context,
including across hosts and new runs, without repeating orientation or interview.
Deepen incrementally for a new goal, stage, interest or unanswered material question.
When a run changes version, reassess applicability to that run before reusing
premises, overview claims or plans. Keep a shared finding supported for its
verified coverage if the evidence still holds there. Reassess or mark affected
plans in the selected run for review. If evidence calls an existing claim into
question within its verified coverage, mark the affected shared findings and
dependent overview claims for review or as disputed, and reassess dependent
plans before reuse. Retain provenance and unaffected research. Reassess other
runs when loaded.

All writes retain the [baseline revision, verified-save, publication and recovery rules](../../001-ai-game-coach/contracts/workspace.md#write-and-recovery-contract).
Publish sources/results and topic premises before a derived overview, verify a new
topic before registration, and persist findings before plans that cite them.
Preserve unrelated fields, preferences, records and spoiler protections. If saving
is incomplete, identify the particular unsaved understanding or context. Stored
spoilers grant no disclosure permission; check explanations, questions, headings,
source labels/destinations and any visuals before output.
If only topics are confirmed saved, report those separately from an unsaved or
unconfirmed overview, run answer, plan or preference update. On resumption inspect
actual files, preserve confirmed substeps and prior valid records, and reconcile
only missing publication/reference steps before using dependent advice. Never
claim that an incomplete multi-file update was saved as a whole. If the player's
knowledge boundary is uncertain, ask a neutral question or reveal less, including
in system explanations and source labels.

## Validation boundary

Model-free checks may establish compatible record shapes, evidence/derivation
references, explicit limits, question retention and dependency review states. They
cannot establish the quality of explanations, interviews or choices. Those remain
optional owner observations during ordinary use; no AI testing, fixed trial campaign
or automatic grading is authorized by this design.
