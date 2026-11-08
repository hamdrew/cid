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
the present work. Do not insist on the full pass or silently resume declined work.
Persist a lasting research preference only when requested, at the proper scope;
a one-off quick request need not change `research_depth`. Brief uses the current
need, normal aims for the bounded foundation, and thorough permits deeper relevant
research while retaining the same stopping and spoiler rules.

A new goal, stage, run or material question can make deferred knowledge relevant
again. Reassess that need within the effective preferences rather than restarting
the whole pass. Relevance alone does not override a refusal: ask neutrally before
resuming explicitly declined research. A skipped player question is not permission
to infer its answer; continue conditional help and revisit it only when material.

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
   For games without linear or persistent progression, explain changes within a
   match/run, skill, strategic position, resources or player-defined goals as
   applicable, and explicitly note the absence of persistent progression. Major
   systems are mechanics that materially affect that loop or the player's choices,
   not a required set of genre categories.
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
branches. Stop earlier at a player limit, protected boundary, inaccessible evidence,
unresolved conflict or diminishing useful returns; retain a partial model and its
specific limits. If player information is the blocker, ask or give supported
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
deduction. Retain coverage gaps/deferred areas in applicability notes; absent
coverage is unknown, not universal. Save selected-run questions and player answers
separately from game knowledge. Never create unsupported mechanics to fill a gap.
Split overview statements that combine claims with different support, applicability
or uncertainty; attach evidence to verified relationships, evidence and conditions
to sourced strategies, and retained premises to original deductions. If no claim
can be verified, keep useful unresolved needs in run questions and accurate source
access observations, without creating a fake finding. Unknown version coverage
remains an explicit applicability limit rather than presumed compatibility.

Broad coaching loads the saved overview/equivalent and relevant topics. Limited
lookups need not load the entire model. Reuse adequate research and reported context,
including across hosts and new runs, without repeating orientation or interview.
Deepen incrementally for a new goal, stage, interest or unanswered material question.
For a version change or conflicting evidence, reassess affected premises, overview
claims and dependent plans before reuse; preserve unaffected research and provenance.
Other runs reassess when loaded; no background recrawl or progress rewrite is required.

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
