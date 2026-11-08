# Tasks: Cid — personal-use feedback workflow

**Spec**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) ·
**Constitution**: [v1.2.0](../../.specify/memory/constitution.md)

## Current work

Use Cid normally and send bullet points of requested tweaks. There is no mandatory
behavioral test queue. The [README](../../README.md#give-feedback) explains optional
checks and sharing a transcript/test workspace for review in this conversation.
Agents may run model-free local checks; they must never launch AI tools for tests.
User-requested artifact review does not authorize extra model calls or test agents.

## Completed implementation history

These IDs preserve the prior implementation record. A checked item records work
already done, not proof that every host behavior works. The retired documents and
scenario campaign were backed up outside the active repository before removal.
The data model, contracts, templates and model-free fixtures remain available.

- [X] T001 Established the instruction-and-record distribution.
- [X] T002 Prepared the original evaluation procedure (archived; replaced by README feedback).
- [X] T003 Established model-free tests and synthetic fixture conventions.
- [X] T004 Implemented common record/template assertions.
- [X] T005 Documented record invariants (retained in data-model.md).
- [X] T006 Created the empty workspace template.
- [X] T007 Created the game template.
- [X] T008 Created the playthrough template.
- [X] T009 Created the knowledge template.
- [X] T010 Created the source-index template.
- [X] T011 Created the integration template.
- [X] T012 Documented entity items and preferences (retained in the data model and templates).
- [X] T013 Implemented the canonical coaching policy.
- [X] T014 Created the Codex bootstrap.
- [X] T015 Created the Claude import adapter.
- [X] T016 Documented setup and policy updates (now in README.md).
- [X] T017 Prepared original new-game scenarios (archived).
- [X] T018 Documented the ordinary-language new-game walkthrough.
- [X] T019 Implemented game identity and context creation.
- [X] T020 Implemented bounded, skippable setup.
- [X] T021 Implemented initial research and next-action guidance.
- [X] T023 Added research contract checks.
- [X] T024 Created synthetic research fixtures.
- [X] T025 Prepared original evidence scenarios (archived).
- [X] T026 Implemented ordered evidence reuse and research.
- [X] T027 Implemented source/integration observations and publication.
- [X] T028 Implemented source visibility rules.
- [X] T029 Implemented evidence invalidation.
- [X] T031 Added workspace/resumption contract checks.
- [X] T032 Created synthetic resumption/recovery fixtures.
- [X] T033 Prepared original resumption scenarios (archived).
- [X] T034 Implemented session entry and context switching.
- [X] T035 Implemented verified saves.
- [X] T036 Implemented targeted recovery.
- [X] T037 Implemented scoped preference resolution and changes.
- [X] T038 Documented existing-workspace merges and updates (now in README.md).
- [X] T040 Prepared original spoiler scenarios (archived).
- [X] T041 Created synthetic spoiler fixtures.
- [X] T042 Implemented spoiler modes and scoped permissions.
- [X] T043 Implemented whole-response disclosure filtering.
- [X] T044 Documented spoiler choices in the README.
- [X] T046 Added provenance/dependency contract checks.
- [X] T047 Created synthetic assumption/correction fixtures.
- [X] T048 Prepared original follow-through scenarios (archived).
- [X] T049 Implemented explicit opt-in and assumed attempts.
- [X] T050 Implemented transitive correction and plan revision.
- [X] T051 Implemented alternative discussion, rejection and disablement.
- [X] T052 Documented correction transitions (retained in the data model and fixtures).
- [X] T054 Prepared original player-direction scenarios (archived).
- [X] T055 Created contextual synthetic fixtures.
- [X] T056 Implemented contextual advice and goal redirection.
- [X] T057 Implemented original-reasoning provenance.
- [X] T058 Implemented optional aids with usable text.
- [X] T060 Completed user documentation (consolidated into README.md).
- [X] T061 Reviewed the shared policy against behavioral contracts.
- [X] T062 Ran the model-free local contract suite.
- [X] T064 Recorded historical results and limitations (archived).

## Retired campaign tasks

These previously open tasks are retired, not marked as passing. They are no longer
gates for personal use. Their intended behaviors remain in the specification and
can inform optional checks or feedback when relevant.

- **T022** — Original formal new-game campaign; replaced by normal use and optional feedback.
- **T030** — Original formal research campaign; replaced by normal use and optional feedback.
- **T039** — Original formal resumption campaign; replaced by normal use and optional feedback.
- **T045** — Original formal spoiler campaign; replaced by normal use and optional feedback.
- **T053** — Original formal follow-through campaign; replaced by normal use and optional feedback.
- **T059** — Original participant-based usability campaign; replaced by normal use and optional feedback.
- **T063** — Original integrated acceptance campaign; replaced by normal use and optional feedback.

No scores, fixed trial counts, participant recruitment or full host matrix are
required. Historical results are not upgraded to passes. Future work comes from
reported issues, with relevant model-free checks and the owner's normal use.
All Git commits still require explicit approval for the specific commit.


## Feedback improvements

- [X] T065 Strengthen first-time coaching orientation in the shared policy, Story 1,
  FR-003/FR-004, coaching contract and README: basic game/progression/mechanics
  research plus a brief relevant progress/stat interview; keep skips and narrow
  lookups usable. Fixture policy copies were later retired. No record schema change.

T065 records the instruction change, not a model-tested behavioral pass. The owner
can try introducing a game and current quest, then report whether the initial
research and questions provide the expected coaching foundation.
