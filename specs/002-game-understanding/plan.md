# Implementation Plan: Bounded game understanding pass

**Branch**: `main` | **Date**: 2026-11-08 | **Spec**: [spec.md](spec.md)

**Input**: `specs/002-game-understanding/spec.md`, including the owner's game understanding requirements.
**Status**: Policy, documentation and model-free record checks implemented.
Spec Kit resolves feature identifier `002-game-understanding`; the actual Git branch is `main`.

## Summary

Expand the shared coaching policy from a basic orientation into a bounded game
understanding pass. Research the actual game's loop, progression, major systems
and relationships, then deepen relevant choices around the player's situation.
Save concise, explanatory topic findings and a connecting overview so future
conversations can reason about tradeoffs and options beyond the current quest.

Keep the Markdown policy, thin host adapters and portable JSON v1 records. No
runtime, schema migration, graph store, source quota or mandatory questionnaire is
needed. Lasting game/workspace restrictions use an optional additive v1
`research_restrictions` string array on the owning record; old records remain valid.
This feature extends the completed [coach baseline](../001-ai-game-coach/spec.md);
its specification, plan and implementation history remain unchanged.

## Technical Context

**Language/Version**: Markdown coaching instructions and UTF-8 JSON schema v1;
Python 3.11+ standard library for development-only deterministic checks.
**Primary Dependencies**: Existing host file/research capabilities; no new packages,
model API, service or installation prerequisite.
**Storage**: Existing local game topics, source/integration indexes and separate
playthrough files. Use the [overview lookup order](data-model.md#overview-lookup)
to reuse an existing topic or create `overview` when there is supported content.
**Testing**: Existing `unittest` contract suite and model-free record/link checks.
Ordinary owner use and optional feedback inform behavioral quality; no AI testing.
**Target Platform**: Existing Codex CLI and Claude Code CLI workspaces, used sequentially.
**Project Type**: Shared instruction-and-record distribution with natural-language UI.
**Performance Goals**: Reuse sufficient saved understanding without fetching its
sources again; load the overview and relevant topics rather than every record.
No invented latency or tool-count SLA.
**Constraints**: Evidence before factual claims, spoiler-safe disclosure, skippable
questions, quick-answer overrides, selective verified saves, no game-code inspection,
website mirroring, encyclopedia, automated model tests or unapproved commits.
**Scale/Scope**: One player's local multi-game/multi-run workspace. Work is policy
and documentation plus focused model-free fixture checks, not a new subsystem.

Research resolved the storage, workflow, stopping, reuse and validation questions
in [research.md](research.md#game-understanding-design-research--2026-11-08).
No unresolved technical clarifications remain.

## Constitution Check

Gate evaluated before research and again against the Phase 1 design, using
[constitution v1.2.0](../../.specify/memory/constitution.md).

| Gate | Before research | After design and observable acceptance |
| --- | --- | --- |
| I: Evidence before game facts | Pass: reuse existing evidence ladder | Pass: factual relationships retain accessed support, deductions retain premises, and version changes and evidence conflicts trigger separate applicability and support checks |
| II: Durable portable records | Pass: existing v1 files suffice | Pass: substantive findings, overview, limits and run questions survive resumption; no template reset or migration |
| III: Correctable advice | Pass: existing dependency model retained | Pass: overview derivations and plans reference premises; player state stays separate and correctable |
| IV: Spoiler protection | Pass: existing modes remain binding | Pass: broad research avoids unnecessary future details; overview, questions, source labels and output obey disclosure rules |
| V: Player-directed coaching | Pass: bounded scope and skippable interview | Pass: mechanics-informed questions and concrete options; quick requests and deferred gaps do not block help |
| MVP and simplicity | Pass: instruction/record boundary | Pass: no added service, runtime, schema, code inspection or exhaustive database |
| Personal-use workflow | Pass: no AI tests | Pass: deterministic checks prove record validity only; owner feedback remains optional and no behavioral pass is fabricated |
| Git approval | Pass: no commit authorized | Pass: leave planning and later implementation changes uncommitted pending approval for a specific commit |

These are design-compliance results, not observed conversational test results.
No exception or constitution amendment is required.

## Project Structure

### Documentation (this feature)

```text
specs/002-game-understanding/
├── spec.md                     # Expanded behavioral requirements
├── plan.md                     # This expansion's design
├── research.md                 # Decisions, rationale and alternatives
├── data-model.md               # Existing fields and understanding conventions
├── quickstart.md               # Validation guide, optional ordinary-use examples
├── contracts/
│   └── game-understanding.md   # Pass, stopping, persistence and reuse contract
├── checklists/
│   └── requirements.md         # Specification quality review
└── tasks.md                    # Dependency-ordered implementation and review tasks
```

### Implementation surface (repository root)

```text
coaching/COACH.md                # Canonical behavior to extend during implementation
README.md                        # Brief expectations and existing-workspace update guide
adapters/{codex,claude}/          # Existing loading adapters; no planned change
templates/records/knowledge.json # Existing empty v1 shape; no planned change
tests/test_contracts.py          # Focused deterministic record checks to extend
tests/fixtures/workspaces/       # Small synthetic record examples as needed
```

**Structure Decision**: Keep one canonical policy and existing file ownership.
The contract describes the user-visible behavior. The installed policy remains
`coaching/COACH.md`.

## Phase 0: Research decisions

Read-only repository research covered persistence and bounded workflow separately.
[Research decisions](research.md#game-understanding-design-research--2026-11-08)
resolve how to represent connected knowledge, retain unsupported gaps, find the
overview, stop research, honor reduced depth and revisit affected evidence.
Existing technology is retained; no new host API or dependency requires web research.

## Phase 1: Design

1. **Orient and reuse**: Resolve identity, selected run, preferences and disclosure
   boundary. Reload any explicit research constraint for that run. Use the overview
   lookup order and read relevant supported findings. Assess content for adequacy
   and extend thin legacy records.
2. **Understand broadly**: Follow the existing evidence ladder for the loop,
   progression and consequential systems and relationships. Describe persistent
   progress and fixed paths independently. Select domains from the actual game.
3. **Connect to the player**: Derive material, skippable questions from mechanics;
   omit answered details. Deepen only topics affecting goals, interests, readiness,
   decisions or bottlenecks. Do not wait on player details by doing more broad research.
4. **Save and use**: Save topic explanations plus a connected overview, preserving
   evidence, applicability and uncertainty. If the overview is pending, retain
   pass-wide gaps in a relevant supported topic finding. Save player questions,
   context and dependent recommendations in their run. Explain a feasible action
   and tradeoff, considering options beyond quest advancement when useful.
5. **Stop and resume selectively**: Use the adequacy and partial-stop rules in the
   [pass contract](contracts/game-understanding.md), including supported choices and
   readiness factors in the adequacy check. Resume temporary deferrals when a
   later request makes them relevant, within standing limits. Reassess run-specific
   applicability separately from conflicts affecting a shared finding's support.

[Data model conventions](data-model.md#game-understanding-in-existing-v1-records)
map every output to existing fields. The [quickstart](quickstart.md) defines
model-free checks and optional owner observations. A fixed source count cannot
prove understanding; prose quality remains a limitation of deterministic validation.

## Requirement coverage

Requirement IDs below are local to [this specification](spec.md).

| New requirement | Design coverage |
| --- | --- |
| FR-001–FR-004 | Broad orientation, actual-game domains, relationships and consequential choices |
| FR-005–FR-006 | Mechanics-informed questions and player-relevant depth/options |
| FR-007–FR-009 | Substantive topic findings, connected overview, evidence distinctions and explicit gaps |
| FR-010–FR-012 | Adequacy, partial stops, non-exhaustive scope and quick/skipped requests |
| FR-013–FR-014 | Saved-model reuse, incremental deepening and affected-dependency refresh |
| FR-015 | Baseline record, preference, spoiler, evidence, correction and recovery invariants |

## Implementation handoff and review focus

[Implementation tasks](tasks.md) cover these changes in dependency order:

- Extend `coaching/COACH.md` new-game, session-entry and evidence sections with the
  pass contract, overview loading, substantive saving, adequacy and partial stops.
- Add focused v1 fixture assertions to `tests/test_contracts.py` for cross-topic
  overview premises, explicit applicability limits, run questions and affected
  dependency states. Reuse synthetic evidence and existing fixtures where possible;
  do not create a conversational scenario suite or test wording with keyword checks.
- Update the README's onboarding expectations and policy-update guidance while
  preserving player records, preferences and existing host setup.
- Run the existing model-free suite and local reference checks. Report exactly
  what they establish; ordinary-use conversational outcomes remain unobserved.

Review thin legacy overviews, nonlinear and nonpersistent progression, partial
coverage without an overview, temporary deferrals and lasting run restrictions,
version applicability and evidence conflicts, and spoiler-bearing relationships
and questions. Record checks can exercise shapes, references, retained
limits and review states; they cannot establish whether a conversation explains
those relationships well. Do not add source-count or category-count assertions as
proxies for understanding. Preserve the completed baseline's task history.

## Complexity Tracking

No constitution violations or additional infrastructure to justify.

