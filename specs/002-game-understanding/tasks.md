---
description: "Implementation tasks for the bounded game understanding pass"
---

# Tasks: Bounded game understanding pass

**Input**: Design documents from `specs/002-game-understanding/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/game-understanding.md`, `quickstart.md`, and `.specify/memory/constitution.md` (v1.2.0).

**Tests**: Focused deterministic record checks implement the design's validation requirements for evidence, applicability, questions and dependency states. Reuse `validate_document`, `validate_workspace`, `fixture_documents` and `check_snapshot` in `tests/test_contracts.py`. Existing validators may already accept the new examples; do not manufacture a failure or add production behavior merely to make a test necessary. No AI sessions, model calls, test/review agents, automated players, behavioral scoring or policy-keyword tests are part of this work. Record validity does not prove explanatory or conversational quality.

**Organization**: Each of the four P1 user stories has its own phase, goal and independent acceptance criteria. Their shared policy edits are serialized in story order. Examples and assertions can be authored independently as indicated below; no parallel execution is being launched by this task list.

## Format: `[ID] [P?] [Story] Description`

- **[P]** identifies tasks that can run alongside the explicitly paired task, in separate files after their phase prerequisites.
- **[US1]–[US4]** map directly to the stories in `spec.md`; setup, foundational and polish tasks have no story label.
- All paths start at the repository root. Fixture paths represent synthetic workspaces, never the owner's game records.

## Path Conventions

- Shared runtime instructions: `coaching/COACH.md`.
- User setup and update guidance: `README.md`.
- Development-only checks: `tests/test_contracts.py`; synthetic records: `tests/fixtures/workspaces/`.
- Feature documentation and validation notes: `specs/002-game-understanding/`.
- Keep existing thin adapters, empty templates and JSON v1; no new application, dependency, installation prerequisite or record migration is needed.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the existing check baseline and document the small fixture extension, using the current repository rather than scaffolding another project.

- [ ] T001 [P] Run `python3 -m unittest discover -s tests -p 'test_*.py' -v` against the unchanged suite in `tests/test_contracts.py`; record the command, result and any pre-existing failure in `specs/002-game-understanding/quickstart.md`, identifying it as model-free baseline evidence rather than an observation of coaching behavior.
- [ ] T002 [P] Extend `tests/fixtures/workspaces/README.md` with the `game-understanding/` fixture family, its synthetic-only ownership and intended connected, choices, refreshed and partial snapshots; explain that assertions concern record content/references and cannot establish useful explanations, spoiler-safe replies or research adequacy.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the shared representation and persistence rules before story-specific policy changes.

**Prerequisite**: Complete Phase 1. These tasks block all story implementation.

- [ ] T003 Add the overview content convention to `coaching/COACH.md` under Portable JSON shapes: use `knowledge/overview.json` or an existing equivalent, preserve v1 and optional existing fields, and require the design constraints "This planned expansion adds content conventions, not fields, enums or record types." and "Partial coverage is not a persisted completion flag."; keep game research independent of run state and retain acyclic actual derivations even when game systems influence one another.
- [ ] T004 Extend Verified saves and recovery in `coaching/COACH.md` for source/result → topic premises → derived overview → dependent plan publication; verify each new topic file before `game.json.topics` registration, preserve per-file revision/read-back checks and unrelated data, and report separately which topic, overview, run answer, plan or preference update is unsaved/unconfirmed after a partial write.

**Checkpoint**: Existing v1 files remain usable without an empty overview, reset or migration; the shared save sequence covers overview dependencies and partial outcomes.

---

## Phase 3: User Story 1 — Establish useful game understanding (Priority: P1) — MVP

**Goal**: Learn the actual game's loop, progression and consequential systems, then save substantive supported topic explanations and a connecting overview rather than a quest answer or link list.

**Independent Test**: Model-free checks accept connected topic/overview records with resolved evidence and cross-topic premises, preserve explicit limits and reject dangling/cyclic/cross-game derivations. Separately, optional ordinary use can show whether Cid explains the game's relationships and saves useful substantive explanations, including for a game without RPG or persistent-progression systems. Do not launch a host to obtain that observation.

### Record checks and example for User Story 1

- [ ] T005 [P] [US1] Add focused cross-topic overview checks in `tests/test_contracts.py`, constructing small variants from `fixture_documents("research", "supported")` in memory: validate a directly sourced relationship and a deduction over a mechanics-topic premise, retain applicability/spoiler/evidence metadata, and reject missing-topic, cross-game and cyclic premise references; reuse existing negative checks where equivalent and do not assert prose quality, category counts or source quotas.
- [ ] T006 [P] [US1] Create the complete synthetic workspace `tests/fixtures/workspaces/game-understanding/connected/` with `.cid/workspace.json`, `games/synthetic-a/game.json`, `sources.json`, `knowledge/mechanics.json`, `knowledge/overview.json` and `playthroughs/run-1.json`, based on the existing supported fixture: show a recurring loop, meaningful within-play progression and a consequential system relationship, distinguish direct evidence from an original cross-topic deduction, register both verified topics and retain source access context, `checked_at`, `applicability` and `spoiler`; follow "split independently uncertain claims so one finding's status/applicability is not misleading" and keep unknown version coverage explicit in `applicability.notes`, without inventing real game facts.

### Implementation for User Story 1

- [ ] T007 [US1] Replace the basic-foundation workflow in New game and useful replies in `coaching/COACH.md` with the bounded understanding pass from `specs/002-game-understanding/contracts/game-understanding.md`: resolve consequential identity/version ambiguity, explain recurring actions/feedback/decisions, progression and actual major systems/relationships before relevant depth, distinguish what persists from whether progression has a fixed path, and avoid fixed RPG categories, future-unlock surveys, game-code inspection and next-objective-only onboarding.
- [ ] T008 [US1] Extend Evidence before game facts in `coaching/COACH.md` so each understanding need follows saved findings → indexed content → available integrations → broad discovery/opened evidence, preserving relevance/version/access checks; require explanatory `findings[].statement` content that "explains what affects what and why it matters", distinguish verified mechanics, published strategies and original synthesis, enforce that `kind: fact` "requires accessed supporting evidence", and never treat familiarity or player testimony alone as universal mechanic verification.
- [ ] T009 [US1] Add substantive topic/overview saving guidance in `coaching/COACH.md`: retain conditions, effects, support and limits sufficient for future reasoning without reopening source pages; implement the `data-model.md` constraints "A directly sourced relationship needs no invented derivation." and "Use `derived_from` where the explanation actually depends on other findings", attach accessed evidence to facts/strategies and supported premises to deductions ("with applicable supported premise references in `derived_from`"), retain a compact overall coverage/deferred-gap note in an overview finding's `applicability.notes` clearly separate from its supported statement, and validate the connected fixture from T006 with `validate_workspace` in `tests/test_contracts.py`.

**Checkpoint**: US1 can be reviewed and its records checked without the later player-choice or refresh examples. Quick requests and spoiler boundaries remain governed by the existing policy; the expanded stopping rules arrive in US4.

---

## Phase 4: User Story 2 — Discuss informed choices (Priority: P1)

**Goal**: Derive material skippable questions from researched mechanics, focus depth on the player and explain concrete options, costs and uncertainty.

**Independent Test**: Record checks retain open/resolved questions, reported answers and a separate deduction-based plan with valid same-run/game references; research cannot depend on player entries. Optional ordinary-use feedback can assess whether the highest-impact questions and concrete tradeoffs change with the player's goal and answers, whether non-quest options are useful, and whether only evidenced gates are described as required.

### Record checks and example for User Story 2

- [ ] T010 [P] [US2] Add focused question/advice checks in `tests/test_contracts.py` using in-memory variants of the existing player-direction/deduction fixture: retain question IDs/text and `open`/`resolved` states, reported answers and a plan's `untested_deduction` reasoning with supported finding/context references; reject cross-run plan prerequisites and game findings depending on run entries, reusing equivalent existing assertions rather than duplicating them.
- [ ] T011 [P] [US2] Create `tests/fixtures/workspaces/game-understanding/choices/` as a complete small workspace based on the existing `player-direction/deduction` fixture, including `games/synthetic-a/playthroughs/run-1.json`, `knowledge/mechanics.json`, `game.json`, `sources.json`, `integrations.json` if retained and `.cid/workspace.json`; show one material unresolved question, one resolved question with a separate reported answer, a sourced optional preparation strategy "with evidence identifying the supported strategy and its conditions", and an explicitly untested plan grounded in mechanic and run references; enforce "Keep game-level notes independent of player state." and preserve unrelated preferences and progress.

### Implementation for User Story 2

- [ ] T012 [US2] Revise the interview guidance in New game and useful replies in `coaching/COACH.md` to prioritize missing details by their effect on the current game/goal/decision, explain the decision a question changes when useful, omit known/declined/irrelevant details, remove the suggested two-or-three-question default and avoid treating quest location as readiness or requiring a full stat sheet/inventory.
- [ ] T013 [US2] Extend player-relevant deepening and advice in `coaching/COACH.md` to identify evidenced decisions, bottlenecks and readiness factors; distinguish documented mandatory gates from optional sourced preparation and inferred readiness, label deductions with premises/uncertainty, and give feasible actions with concrete benefits/costs and relevant non-quest approaches without forcing alternatives into narrow answers.
- [ ] T014 [US2] Specify question/answer/advice persistence in `coaching/COACH.md`: the selected run owns `questions`, explanatory `text` "can name why the detail affects the decision without revealing protected mechanics", answers are reported `entries`, and separate `plans` reference applicable findings and run context; retain unresolved questions without guessing answers, and validate the choices fixture from T011 in `tests/test_contracts.py` without claiming the example verifies interview quality.

**Checkpoint**: Informed advice and questions are expressible in existing records; no question bank, inferred player readiness or universal preparation threshold has been added.

---

## Phase 5: User Story 3 — Reuse and deepen understanding (Priority: P1)

**Goal**: Resume from retained explanations, deepen thin or newly relevant knowledge incrementally and reconsider only affected evidence/dependencies while preserving game/run separation.

**Independent Test**: Model-free checks preserve a shared old-version finding and overview alongside a newer-version run's plan awaiting review, and separately retain provenance and review states for a premise disputed within its verified coverage. The runs keep separate context, preferences and progress. Optional ordinary use can assess selective loading, source reuse, omission of answered questions, reuse of a legacy overview and reconsideration before advice.

### Record checks and example for User Story 3

- [ ] T015 [P] [US3] Extend `tests/test_contracts.py` with in-memory connected overview → selected-run plan dependency cases based on existing research/resumption fixtures: represent conflicting evidence within a premise's verified coverage, explicit `needs_review`/`disputed` states, retained superseded provenance and unaffected knowledge/preferences/progress. Exercise dangling overview registration/reference recovery with `check_snapshot`. Keep these checks at the record level.
- [ ] T016 [P] [US3] Create the complete synthetic workspace `tests/fixtures/workspaces/game-understanding/refreshed/` with `.cid/workspace.json`, `games/synthetic-a/game.json`, `sources.json`, `knowledge/mechanics.json`, `knowledge/overview.json`, `playthroughs/run-1.json` and `playthroughs/run-2.json`. Put the two runs on different patches. Keep a shared premise and derived overview supported for the original patch and mark the newer-patch run's dependent plan `needs_review`. Preserve distinct reported context, preferences and questions.

### Implementation for User Story 3

- [ ] T017 [US3] Update Session entry and reuse guidance in `coaching/COACH.md` to follow the [overview lookup order](data-model.md#overview-lookup) for broad coaching, checking registered `overview` first, then relevant legacy candidates by content before creating a topic. Load only necessary knowledge for narrow lookups. Extend thin records while preserving valid content, reuse adequate applicable evidence without re-fetching sources, and reuse game knowledge for new runs while asking only missing material run questions.
- [ ] T018 [US3] Revise evidence refresh guidance in `coaching/COACH.md` to check a changed version against each premise's applicability, keep shared findings and overview claims supported within valid coverage, and reassess affected plans for that run. Use existing `needs_review`/`disputed` transitions on shared findings and derived overview claims when evidence undermines their verified coverage. Retain provenance and unaffected records, reassess other runs on load, and validate the two-patch fixture from T016 in `tests/test_contracts.py`.
- [ ] T019 [US3] Extend interrupted-understanding recovery in `coaching/COACH.md` to inspect actual persisted topic, overview, registry and run substeps, preserve confirmed saves, reconcile only missing publication/reference steps and distinguish unsaved topics from an unconfirmed overview/answer/plan/preference; retain valid legacy records and prohibit replaying the entire pass, resetting templates or claiming a partially saved update succeeded as a whole.

**Checkpoint**: The same game model supports fresh conversations and separate runs, while a known affected dependency remains reviewable and cannot be represented as settled advice by the policy.

---

## Phase 6: User Story 4 — Keep research bounded and player-directed (Priority: P1)

**Goal**: Stop at useful adequacy or an honest partial limit, respect declined/reduced work and protect discoveries throughout research, questions and output.

**Independent Test**: Record checks preserve pass-wide limits on a supported topic without an overview, accept an all-evidence-unavailable workspace with accurate access observations and unanswered run questions, and retain a reported run research constraint alongside existing preferences. Optional ordinary use can assess temporary deferrals, lasting run limits, neutral questions at uncertain spoiler boundaries, conditional help and the distinction between an adequate stop and an early partial stop.

### Record checks and example for User Story 4

- [ ] T020 [P] [US4] Add focused partial-coverage checks in `tests/test_contracts.py` using in-memory variants of the existing failed-access and spoiler fixtures. Retain a separately labeled pass-wide gap in a supported topic finding's `applicability.notes` with no overview, preserve unrelated findings and unanswered run questions, accept zero findings with accurate failed-access history, and reject an unsupported fact used as a gap placeholder. Retain an explicitly lasting run restriction as a reported constraint alongside the existing depth and spoiler preferences.
- [ ] T021 [P] [US4] Create `tests/fixtures/workspaces/game-understanding/partial/` as a complete synthetic workspace based on `research/failed-access`, including `.cid/workspace.json`, `games/synthetic-a/game.json`, `sources.json`, `knowledge/mechanics.json`, `playthroughs/run-1.json` and any retained integration index. Use an empty findings array and unanswered material run questions with accurate failed-access observations. Follow the [v1 gap rules](data-model.md#game-understanding-in-existing-v1-records) for the all-evidence-unavailable case.

### Implementation for User Story 4

- [ ] T022 [US4] Add the FR-010 and contract stopping rules to `coaching/COACH.md`: judge supported loop, progression, relationships, consequential choices, tradeoffs, readiness factors, bottlenecks, material player questions and targeted gaps. Tie further research to a named unmet criterion or material decision. Stop at adequacy or when a limit prevents useful further research. For a partial stop, explain unmet criteria and preserve the pass-wide gap in a relevant supported topic when no overview is available. Avoid repeated failed searches without changed conditions and offer conditional help when player information is the blocker.
- [ ] T023 [US4] Integrate bounded research with session entry, Preferences and disclosure and useful-reply guidance in `coaching/COACH.md`. Apply the brief/normal/thorough bounds and give supported narrower or conditional help when the player defers or skips. Reopen a temporary deferral when a later request makes it relevant. Save and reload explicitly lasting run restrictions as reported constraints, honor broader restrictions in standing workspace instructions, and disclose when a broader limit is conversation-only. Clarify a later request that appears to conflict with an active restriction unless the player explicitly changes it. Persist depth preferences at the requested scope. Preserve spoiler checks for explanations, questions, headings, source labels/destinations and visuals, and register and validate the completed partial fixture from T021 after T020.

**Checkpoint**: Research can stop honestly with no findings, a partial model or an adequate model; neither a questionnaire nor completed broad research is a prerequisite for useful supported help.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Align user expectations, verify compatibility and record the limits of the available evidence.

- [ ] T024 Update new-game expectations, normal-use reuse/quick-help guidance and existing-workspace updates in `README.md` to describe the bounded connected understanding, mechanics-informed skippable questions and saved overview; preserve the existing thin host setup, policy-merge instructions, workspace identity/preferences/`games/`, optional ordinary-use feedback and absence of a Python/runtime requirement for players; never instruct copying empty templates over existing records.
- [ ] T025 Run `python3 -m unittest discover -s tests -p 'test_*.py' -v` and the focused research/resumption command in `specs/002-game-understanding/quickstart.md` after all new fixture registrations/assertions in `tests/test_contracts.py`; check changed Markdown links and fixture registry/evidence/derivation references with model-free local tools, fix actual introduced failures and record exact commands/results and remaining limitations in `specs/002-game-understanding/quickstart.md` without claiming conversational success.
- [ ] T026 Review `coaching/COACH.md`, `README.md`, `tests/test_contracts.py` and the four new fixture directories against FR-001–FR-015, SC-001–SC-006 and constitution principles I–V; record coverage, any unresolved deviation and unobserved behavioral outcomes in `specs/002-game-understanding/quickstart.md`, confirm baseline `specs/001-ai-game-coach/` history/adapters/empty templates remain intact, and leave all changes uncommitted pending explicit approval for a specific commit.

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup**: T001 and T002 have no implementation prerequisites and touch different documentation files.
2. **Foundational**: T003 follows setup; T004 follows T003 because both edit `coaching/COACH.md`. Complete both before user-story implementation.
3. **US1**: T005 and the fixture authoring in T006 can run together. Then apply T007 → T008 → T009; T009 also needs both the test work and the connected fixture.
4. **US2**: After US1, T010 and T011 can run together; then T012 → T013 → T014. T014 registers/checks the completed choices fixture.
5. **US3**: After US1/US2 policy changes, T015 and T016 can run together; then T017 → T018 → T019. T018 needs the refreshed fixture and checks.
6. **US4**: After prior policy edits, T020 and T021 can run together; then T022 → T023. T023 registers/checks the completed partial fixture after both inputs are ready.
7. **Polish**: T024 → T025 → T026 after the desired story phases; the complete feature requires all four stories.

### User Story Dependencies

```text
Setup (T001–T002)
        |
Foundation (T003–T004)
        |
US1: connected understanding (T005–T009)
        |
US2: informed choices (T010–T014)
        |
US3: reuse and refresh (T015–T019)
        |
US4: bounded/player-directed pass (T020–T023)
        |
Polish and evidence (T024–T026)
```

US2 and US3 consume the understanding introduced by US1. US4 refines the whole pass, retaining baseline quick-help/spoiler protections throughout earlier increments. US2, US3 and US4 have independent acceptance observations and record examples; their policy tasks are sequenced for the common file, rather than pretending the stories have no integration dependencies. All priorities are P1; the specification's story order supplies execution order.

### Within Each User Story

- Author focused checks and synthetic examples before the corresponding policy integration; existing v1 compatibility may make checks pass immediately.
- Keep test changes inside the existing development-only suite; no schema expansion or application runtime is implied.
- Apply policy edits sequentially and remove superseded basic-foundation wording so there is one canonical workflow.
- Use existing validators for data invariants and explicit fixture assertions for retained states; neither is an evaluator of mental-model quality.
- Register each finished fixture in the suite before the story checkpoint; run the full suite at T025.

### Parallel Opportunities

- Setup: T001 with T002.
- US1: T005's in-memory test authoring with T006's separate connected fixture files.
- US2: T010's in-memory test authoring with T011's separate choices fixture files.
- US3: T015's in-memory test authoring with T016's separate refreshed fixture files.
- US4: T020's in-memory test authoring with T021's separate partial fixture files.
- Do not run story policy edits together: they share `coaching/COACH.md`. Do not run separate stories' test edits together: they share `tests/test_contracts.py`.

## Parallel Example: User Story 1

```text
T005: Author in-memory cross-topic reference checks in tests/test_contracts.py.
T006: Author tests/fixtures/workspaces/game-understanding/connected/ JSON files.
Join: T009 registers/validates the completed fixture after T007–T008 policy edits.
```

## Parallel Example: User Story 2

```text
T010: Author in-memory question/advice checks in tests/test_contracts.py.
T011: Author tests/fixtures/workspaces/game-understanding/choices/ JSON files.
Join: T014 registers/validates the completed fixture after T012–T013 policy edits.
```

## Parallel Example: User Story 3

```text
T015: Author in-memory refresh/recovery checks in tests/test_contracts.py.
T016: Author tests/fixtures/workspaces/game-understanding/refreshed/ JSON files.
Join: T018 registers/validates the completed fixture after T017's reuse changes.
```

## Parallel Example: User Story 4

```text
T020: Author in-memory partial-coverage checks in tests/test_contracts.py.
T021: Author tests/fixtures/workspaces/game-understanding/partial/ JSON files.
Join: T023 registers/validates the completed fixture after T020 and T022;
      apply T022–T023 sequentially in coaching/COACH.md.
```

## Implementation Strategy

### MVP First (User Story 1)

Complete T001–T009 and validate the US1 record example. This is a reviewable minimum increment: useful broad understanding and connected persistence, with baseline player limits and spoilers still binding. It is not completion of the four-story feature, and it does not establish observed conversational quality. Before distributing even this increment, apply the relevant README guidance and model-free verification/review from T024–T026; leave US2–US4 explicitly outstanding.

### Incremental Delivery

1. Establish the existing check baseline and shared representation/save rules.
2. Add US1's actual-game understanding and supported overview.
3. Add US2's mechanics-informed questions and concrete choice/advice records.
4. Add US3's selective resumption, incremental legacy extension and affected-dependency refresh.
5. Add US4's explicit adequacy/partial stops and integrated player/spoiler limits.
6. Align README guidance, run deterministic checks and report only what their evidence establishes.

### Parallel Team Strategy

If multiple implementers are explicitly authorized later, pair test authoring with separate fixture authoring inside the current story using the examples above, then join before registration/integration. Keep one writer for the canonical policy and one writer for the shared test file at a time. This document does not authorize AI-driven testing or extra model calls for evaluation.

## Notes

- Data constraints quoted in tasks come from this feature's `data-model.md`; existing required fields/enums/reference rules remain defined by `specs/001-ai-game-coach/data-model.md` and enforced by the current validators.
- No fixed source/category/question quotas, mandatory interview, schema completion flag, research backlog service or new graph store is needed.
- Owner feedback during ordinary use is optional. No host session, transcript, trial quota or acceptance score is required or may be fabricated by development agents.
- Never create or amend a Git commit without the user's explicit approval for that specific commit.
