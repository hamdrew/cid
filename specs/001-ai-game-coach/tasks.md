# Tasks: Cid — Local AI Video Game Coach

**Input**: Design artifacts in `specs/001-ai-game-coach/`  
**Generated**: 2026-11-08  
**Feature context**: `001-ai-game-coach`; actual Git branch: `main`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md),
[research.md](research.md), [data-model.md](data-model.md),
[workspace contract](contracts/workspace.md), [coaching contract](contracts/coaching.md),
[quickstart.md](quickstart.md), and constitution 1.0.0 at
`.specify/memory/constitution.md`.

**Organization**: Setup → shared foundation → six stories in specification order
(US1–US4 P1; US5–US6 P2) → cross-cutting validation. Models shared by multiple
stories belong in the foundation. Later story tasks extend the common policy;
they do not create separate host implementations.

**Tests**: The specification explicitly requires controlled acceptance scenarios
and measured evaluation; the plan selects development-only Python 3.11+
standard-library contract checks. Include those checks and observed trials below.
Scenario preparation is not a passing trial. Write contract expectations and
scenario definitions before the corresponding implementation, observe failures
where executable, then verify the increment. No API evaluation service or player
runtime is introduced.

**Implementation gate**: The reviewer-owned [coaching checklist](checklists/coaching.md)
is still pending. Task generation does not change its markers or bypass the
checklist handling required by `$speckit-implement`. Preserve the specification,
constitution, and existing user changes. No task authorizes a Git commit or amendment;
each commit needs the user's explicit approval for that commit.

## Format: `[ID] [P?] [Story] Description`

- Every task has an unchecked checkbox, sequential ID, and exact repository path.
- `[P]` identifies disjoint-file work within the parallel waves defined below;
  complete each wave's prerequisites first. It does not authorize concurrent
  editing of player records or the common policy.
- Story-phase tasks use `[US1]` through `[US6]`; shared and polish tasks have no
  story label.
- Quoted field constraints below are taken verbatim from the data model, with
  prose line wrapping normalized. Apply the complete referenced entity contract,
  including common rules, rather than treating quotes as an alternative schema.

## Path Conventions

Paths are repository-relative unless explicitly describing an installed workspace.
The distribution uses `coaching/COACH.md`, `adapters/`, `templates/`, `docs/`, and
`tests/`. The installed player workspace contains `AGENTS.md`, `CLAUDE.md`,
`.cid/COACH.md`, `.cid/workspace.json`, and `games/<game-id>/` as designed.
Do not install the coaching adapter into this development repository's root.

Keep development validation logic in `tests/test_contracts.py`; it is not a
required coaching executable. Record sanitized aggregate outcomes and limitations
in `docs/validation.md`; retain transcripts, tool traces, and snapshots in an
evaluator-selected local results directory outside the repository. Do not publish
or commit private evidence. All controlled fixture facts must be labelled synthetic.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the distribution and evaluation conventions without a
companion application, dependency installation, or changes to user records.

- [ ] T001 Create the planned directories and describe the instruction-and-record distribution in `README.md`: `coaching/`, `adapters/codex/`, `adapters/claude/`, `templates/workspace/.cid/`, `templates/records/`, `docs/`, `tests/fixtures/workspaces/`, and `tests/scenarios/`; state Python is development-only and preserve all existing repository changes.
- [ ] T002 [P] Establish evaluation procedures in `docs/validation.md` and a scenario manifest format in `tests/scenarios/manifest.md`, copying the quickstart's scoring definitions, story/acceptance-scenario/SC traceability, host/version/context fields, evidence locations, frozen denominators, pass/fail/untested states, anonymization, and capability limitations; freeze each increment's selected trials before running it.
- [ ] T003 [P] Initialize the discoverable standard-library test module `tests/test_contracts.py` and fixture conventions in `tests/fixtures/workspaces/README.md`; distinguish valid documents, deliberately invalid documents, recoverable incomplete workspaces, and synthetic evidence without adding pip/npm dependencies or treating recovery fixtures as normally valid state.

**Checkpoint**: Distribution paths and evidence/reporting conventions are defined.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Supply the shared schemas, minimal policy, and host loading needed
by every story. Complete this phase before a story's implementation or live trial.

### Shared contract checks and record templates

- [ ] T004 [P] Add common record/template assertions and development-only validation helpers in `tests/test_contracts.py` for required fields, primitive types, enums, IDs/paths, references, and dependency graphs; reject booleans as numeric revisions/versions. Enforce: “Each JSON document is an object containing `schema_version` (integer `1`), `revision` (nonnegative integer), and `updated_at` (UTC timestamp).” Enforce: “IDs are stable, spoiler-neutral strings using lowercase letters, digits, and hyphens, unique in their owning scope.” Enforce: “Paths are derived from IDs, stay within the selected workspace, and never accept `..`, absolute components, or arbitrary source-supplied paths.” Initially demonstrate missing/invalid-template failures; the completed valid templates must later pass.
- [ ] T005 [P] Document common fields, ID ownership, reference syntax, compatibility, and selective loading in `docs/record-format.md`. Preserve: “Changing a display label does not rename an ID.” Preserve: “Cross-record references are objects: `game_id`, optional `playthrough_id`, `type` (`entry`, `plan`, `finding`, `source`, or `integration`), and `id`.” Preserve: “Findings additionally require `topic_id`.” Preserve: “Entry/plan references require a playthrough; a playthrough's dependencies cannot refer to another playthrough.” Preserve: “All dependencies must remain within the owning game; game research cannot depend on a player's progress or plans.” Preserve: “References resolve before their contents support advice.” Preserve: “Dependency edges on entries/plans and derivation edges between findings form acyclic graphs; dangling or cyclic dependencies require repair.” Preserve additive fields and never silently rewrite an unknown schema version.
- [ ] T006 [P] Create `templates/workspace/.cid/workspace.json` with an empty game registry, null active pointer, empty explicit preferences, and common metadata; document that setup supplies a stable `workspace_id`, not a new ID every session. Apply `workspace_id`: “Stable local workspace identity”; `games`: “Array of `{game_id, label}` registry entries; IDs unique”; `active`: “`null` or `{game_id, playthrough_id}` resolving to registered records”; `preferences`: “Workspace choices; see Preference below”; `preference_prompts`: “`spoiler_modes_explained` and `follow_through_offered` booleans, initially false”. Do not enable assumptions or store a selected spoiler preference on the player's behalf.
- [ ] T007 [P] Create the reusable record shape in `templates/records/game.json` with common metadata and fields `game_id`, `title`, optional `identity_notes`/`preferences`, `playthroughs`, and `topics`. Preserve `game_id`: “Matches directory and workspace registry”; `title`: “Resolved game identity; distinguish similarly named releases if relevant”; `identity_notes`: “Optional disambiguation context; no forced irrelevant edition fields”; `preferences`: “Optional game overrides”; `playthroughs`: “Array of `{playthrough_id, label}` registry entries, unique within game”; `topics`: “Existing knowledge topic IDs; no empty mandatory category catalog”. Use spoiler-neutral sample IDs and clearly distinguish template examples from player reports.
- [ ] T008 [P] Create `templates/records/playthrough.json` with common metadata, identities, selective entries/plans/questions, and no invented progress. Preserve `game_id`, `playthrough_id`, `label`: “Match the containing game and registry”; `context`: “Known relevant edition/platform/patch/DLC/mod details; omitted details are unknown”; `preferences`: “Optional playthrough overrides”; `questions`: “Concise unresolved coaching questions, each with ID, text, and `open`/`resolved` status”. Preserve: “`context` is an object with optional string fields `edition`, `platform`, and `patch`, plus optional string arrays `dlc` and `mods`.” Preserve: “Omission means unknown; an explicitly empty array means the player reported none.” Document entry/plan item shapes with the template without seeding a fictional milestone.
- [ ] T009 [P] Create `templates/records/knowledge.json` with common metadata, `game_id`, `topic_id`, and an initially empty `findings` array. Preserve the item contract: “Each finding contains `id`, `statement`, `kind` (`fact`, `sourced_strategy`, or `deduction`), `status` (`supported`, `needs_review`, `disputed`, or `superseded`), `applicability`, `evidence` (array), optional `derived_from` (finding references), `spoiler` (object with `sensitive` boolean and optional `boundary_notes`), and `checked_at`.” Preserve: “`applicability` is an object with optional arrays `editions`, `platforms`, `patches`, `dlc`, and `mods`, plus `notes` describing verified coverage and unresolved limitations.” Lists are coverage, not universal applicability; create topic files only when useful.
- [ ] T010 [P] Create `templates/records/sources.json` with common metadata, `game_id`, and empty `sources`. Preserve the item contract: “Each source contains `id`, `locator`, `title`, `coverage` (topics), `applicability`, `discovered_at`, `access_status` (`never_accessed`, `accessible`, `failed`, or `requires_access`), nullable `last_attempt_at` and `last_success_at`, and `quality_notes` covering relevance, maintenance, version compatibility, specificity, and credibility.” Preserve: “Unknown quality/access details remain explicitly unknown.” Preserve: “Optional `integration_id` identifies the integration supplying a result.” T012 documents item examples after the template wave.
- [ ] T011 [P] Create `templates/records/integrations.json` with common metadata, `game_id`, and empty `integrations`; preserve: “Each integration contains `id`, `name`, `capabilities`, `coverage`, `access_requirements` (descriptions, never credentials), `discovery_locator`, and `observations`.” Preserve: “Each observation records `host`, `checked_at`, `availability` (`available`, `unavailable`, or `unknown`), `reason`, and optional `last_query` with `attempted_at`, `outcome` (`success` or `failure`), and a concise result/error reference.” An empty collection is valid; never invent access or a query to fill it.
- [ ] T012 Complete entity item examples and preference rules in `docs/record-format.md` after T005–T011, keeping templates and documentation consistent. Preserve: “An **entry** has `id`, `topic`, `statement`, `kind` (`reported` or `assumed`), `status` (`current`, `superseded`, `retracted`, or `needs_review`), `recorded_at`, `depends_on` (reference array), and optional `supersedes` (entry ID).” Preserve: “An assumed entry additionally references its originating plan in `depends_on`.” Preserve: “A **plan** has `id`, `text`, `status` (`proposed`, `accepted`, `rejected`, `completed_reported`, `needs_review`, or `superseded`), `depends_on`, `recorded_at`, and `reasoning_status` (`evidence_based` or `untested_deduction`).” Preserve: “Optional `replaces` points to a prior plan.” Preserve preferences: “Each stored key contains `{value, selected_at}`. Missing keys inherit.” Quote allowed values/defaults: `spoiler_mode`: “`strict`, `hints`, `off`” / “`hints`”; `follow_through`: “`enabled`, `disabled`” / “unset, operationally disabled”; `research_depth`: “`brief`, `normal`, `thorough`” / “`normal`”; `coaching_style`: “Concise player-requested text” / “Preserve existing host/personality preferences”. Include evidence item fields: “Evidence items contain `source_id`, `locator` (URL or integration-result locator), `accessed_at`, and a concise `summary` supporting this claim.” Preserve: “Integration evidence also identifies `integration_id` and the observed successful query.” Run the completed template checks from T004.

### Canonical policy and thin host setup

- [ ] T013 Create the canonical baseline in `coaching/COACH.md` using the two contracts: capability discovery, workspace/record loading, evidence-before-facts research order and stopping rule, source-on-request behavior subject to host rules, safe spoiler handling for Strict/Hints/Off and unknown boundaries, explicit follow-through consent, scoped preferences, minimal actionable text, and verified per-response saves with precise failure disclosure. Include reported/assumed/proposed distinctions, corrections overriding assumptions with dependent advice reconsidered, common record invariants, acyclic references, source → finding → plan and record → registry publication order, user-instruction preservation, and external-source-as-evidence boundaries. This must make US1 safe without waiting for later story hardening; add no companion runtime or game facts from model familiarity.
- [ ] T014 [P] Create `adapters/codex/AGENTS.md` as a short explicit bootstrap to read installed `.cid/COACH.md` and `.cid/workspace.json`, then relevant records; preserve existing host/personality instructions and avoid duplicated coaching policy, global configuration changes, or assuming Markdown links import files.
- [ ] T015 [P] Create `adapters/claude/CLAUDE.md` importing `@AGENTS.md`, sharing the same installed policy and JSON records; keep host-specific content limited to loading instructions rather than a second coaching implementation.
- [ ] T016 Write fresh disposable-workspace installation, prerequisite checks, stable workspace identity initialization, and both CLI launch procedures in `docs/setup.md`, using the quickstart's copy/launch commands; confirm both adapters actually load the policy. Document Codex overrides/size limits, Claude instruction suppression, actual versus inspected versions, optional research capabilities, and that unavailable loading is incompatible setup rather than permission to change user/managed configuration. Do not install adapters into the development root or create records in a player's folder during development checks.

**Checkpoint**: Template checks pass; both adapters and shared baseline are ready
for observation. CLI help and valid JSON alone do not prove host behavior.

## Phase 3: User Story 1 — Get useful help with a new game (Priority: P1)

**Goal**: Turn a resolvable game and goal into an evidence-supported next action
without an exhaustive interview or game encyclopedia.

**Independent Test**: Use fresh installed workspaces, accessible evidence, and a
frozen ten-trial manifest (five trials per host, at least three games). At least
nine trials give an actionable step within three setup replies under the quickstart's
counting rules. Include ambiguous title/version, missing progress, skipped questions,
less research, open-ended help, and only relevant knowledge topics. (Story 1.1–1.5;
FR-002–FR-004, FR-020/023; SC-001.)

### Scenario definition and documentation

- [ ] T017 [P] [US1] Define all five US1 acceptance scenarios, ten trial slots, initial prompts, evaluator reply scripts, research/provenance observations, and actionable-step/setup-reply scoring in `tests/scenarios/us1-new-game.md`. Do not predetermine real game facts without accessible evidence or count clarification alone as an actionable step.
- [ ] T018 [P] [US1] Add a new-game walkthrough to `README.md` using ordinary language, selected-workspace setup, relevant optional version details, skippable progress questions, and a text next-action example labelled illustrative; explain where shared records live and link to `docs/setup.md` rather than adding custom start/end commands.

### Implementation and observed validation

- [ ] T019 [US1] Register the prepared US1 scenarios in `tests/scenarios/manifest.md`, then implement identity resolution and context creation in `coaching/COACH.md`: resolve similarly named releases, ask edition/platform/patch/DLC/mod questions only when material, initialize game/playthrough/source records from the templates, register existing records only after verified publication, and avoid empty mandatory topic catalogs.
- [ ] T020 [US1] Implement the bounded initial interview in `coaching/COACH.md`: ask a focused question when progress is missing, defer unrelated details, honor skipped questions and reduced research, and give conditional/common safe guidance rather than guessing a dependent fact.
- [ ] T021 [US1] Implement sufficient initial research and the first next-action response in `coaching/COACH.md`, reusing the foundation's research sequence, relevant mechanics/topics, source-quality assessment, and verified saves; explain how the action serves the known goal while applying effective spoiler preferences and reporting material uncertainty.
- [ ] T022 [US1] Execute `tests/scenarios/us1-new-game.md` against fresh processes in both hosts using the frozen manifest, recording ten outcomes and host-level counts in `docs/validation.md` with external evidence references; require ≥9/10 within three setup replies and inspect actual policy loading, research, and saved records. Report unavailable hosts/evidence as untested rather than a passing SC-001 result.

**Checkpoint**: US1 is a demonstrable first slice with foundational protections,
not acceptance of all Cid MVP requirements.

## Phase 4: User Story 2 — Receive an evidence-based answer (Priority: P1)

**Goal**: Reuse applicable research, obtain missing evidence in order, and preserve
source/access distinctions without fabricated facts or repeated broad searches.

**Independent Test**: Seed valid research records without a US1 conversation; test
all seven Story 2 scenarios in each host, inspect claim-to-evidence mappings and tool
order, and repeat saved/indexed-source questions in fresh sessions with zero broad
searches. Include source conflicts, version mismatch, inaccessible material, available
and unavailable integrations, and requested/unrequested source display. (FR-005–FR-011;
SC-002–SC-003.)

### Contract checks and controlled scenarios

- [ ] T023 [P] [US2] Add self-contained positive/negative research-contract cases to `tests/test_contracts.py` for finding kind/status, applicability types and unknown coverage, evidence required for facts/sourced strategies, deduction premises and derivation cycles, source timestamp nullability/access enums, and integration observation/query enums; discovery, availability, and successful claim-supporting access must remain distinct.
- [ ] T024 [P] [US2] Create the supported synthetic workspace rooted at `tests/fixtures/workspaces/research/supported/.cid/workspace.json` and complete sibling workspaces for indexed-only evidence, conflicting sources, patch mismatch, failed access preserving past success, available/unavailable integration observations, and a deduction from valid findings; use each workspace's full installed file layout. All game/source/topic references must resolve, and synthetic locators must never be presented as real evidence in live trials.
- [ ] T025 [P] [US2] Define the seven Story 2 acceptance scenarios plus fresh-session reuse and live/saved source-display checks in `tests/scenarios/us2-evidence.md`, including actual tool-trace order, claim-to-evidence ledger, conflicts, version changes, failed links, stale findings, and external content attempting to issue instructions.

### Implementation and observed validation

- [ ] T026 [US2] Register the prepared US2 scenarios in `tests/scenarios/manifest.md`, then complete the evidence ladder in `coaching/COACH.md`: applicable local finding → indexed relevant content → relevant available API/MCP query → broad search only for a remaining need; open evidence rather than trusting snippets, stop once sufficient, avoid exhaustive scraping, and reassess relevance, maintenance, version compatibility, specificity, and credibility.
- [ ] T027 [US2] Implement source/integration observation and finding publication in `coaching/COACH.md`, recording real access times and successful query context, failed/unavailable access without invented results, concise useful summaries, applicability, and source → finding ordering; give specific uncertainty and ask useful player questions when verification remains impossible.
- [ ] T028 [US2] Complete source visibility in `coaching/COACH.md`: preserve links locally, reveal supporting sources only on request after filtering labels/destinations, distinguish player context from universal game evidence, and honor higher-priority citation requirements while reporting FR-009 incompatibility rather than promising suppression.
- [ ] T029 [US2] Implement evidence invalidation in `coaching/COACH.md`: version changes, contradictions, and failed evidence reopen affected findings and transitive finding/plan dependencies before advice; reassess other playthroughs on load, retain provenance, and never silently rewrite progress or use review-needed/disputed claims as settled facts.
- [ ] T030 [US2] Run the research contract checks and `tests/scenarios/us2-evidence.md` in both hosts; record claim support, observed reuse/tool order, zero broad searches for sufficient saved/indexed evidence, conflict outcomes, and FR-009 behavior in `docs/validation.md`. Observe a real relevant integration query when available; otherwise mark that coverage untested without introducing a required integration or waiving host citation rules.

**Checkpoint**: US2 can be verified from seeded records independently of new-game
setup. Unsupported optional capabilities and citation incompatibilities stay visible.

## Phase 5: User Story 3 — Continue a playthrough in a fresh conversation (Priority: P1)

**Goal**: Preserve meaningful shared state across both hosts with separate games
and playthroughs, scoped preferences, verified writes, and targeted recovery.

**Independent Test**: Start with controlled records, save meaningful changes without
a closing command, and exercise Codex→Codex, Codex→Claude, Claude→Codex, and
Claude→Claude. In every pair switch A/run-1 → B/run-1 → A/run-2 without mixing
progress or requesting recorded history. Inject actual denied and partial writes,
corrupt/unknown-version state, invalid active pointers, and conflicting preferences.
(Story 3.1–3.5; FR-001, FR-012–FR-015; SC-004–SC-005.)

### Contract checks and controlled scenarios

- [ ] T031 [P] [US3] Extend `tests/test_contracts.py` with self-contained workspace/playthrough validation cases for registry/identity uniqueness, active-pointer resolution, selective entries/questions, scoped preferences, omitted versus empty context, invalid paths, mixed-playthrough references, unknown versions, corrupt documents, and recoverable orphan/registry states; classify recovery needs without silently repairing or accepting invalid state as authoritative.
- [ ] T032 [P] [US3] Create a complete synthetic two-game/two-playthrough workspace rooted at `tests/fixtures/workspaces/resumption/valid/.cid/workspace.json` and sibling corrupt, unknown-version, invalid-pointer, orphaned-record, and partial-publication variants, using each workspace's full installed layout, distinct progress/goals/preference markers, and preserved readable prior content; keep deliberately invalid variants explicitly identified.
- [ ] T033 [P] [US3] Define all four host pairs, all five Story 3 scenarios, scope inheritance, default-only/unscoped changes, actual denied writes, revision mismatch, interruption, partial publication, and minimal retention in `tests/scenarios/us3-resumption.md`; specify fresh processes without resume flags/copied transcripts.

### Implementation and observed validation

- [ ] T034 [US3] Register the prepared US3 scenarios in `tests/scenarios/manifest.md`, then complete session entry and context switching in `coaching/COACH.md`: read workspace then selected game/playthrough and only relevant knowledge, resolve explicitly named context before the last active pointer, clarify ambiguity, recheck dependencies/applicability, and never merge progress or rely on previous chat history.
- [ ] T035 [US3] Implement the verified-save workflow in `coaching/COACH.md`: read current target/revision, preserve unrelated content, prepare/check a same-directory complete temporary replacement, replace and read back actual contents, increment revision/update timestamp, publish referrers after records, and disclose the precise unsaved/unconfirmed update before ending the response that handles it. State the single-writer scope and absence of a multi-file transaction guarantee.
- [ ] T036 [US3] Complete recovery in `coaching/COACH.md`: reconcile revision mismatches and actual persisted substeps, preserve valid progress, inspect unregistered/orphan/temporary records before reuse, repair missing registry steps after identity checks, and request specific missing information for corrupt or unknown formats; never reset to an empty template, blindly replay, bypass denied access, or let unrelated research maintenance block a progress save.
- [ ] T037 [US3] Implement effective preference resolution and changes in `coaching/COACH.md`: “Precedence: explicit playthrough choice → game choice → workspace choice → default.” For an unscoped change update the workspace choice and any conflicting active playthrough key, preserving other scoped choices; save the effective active change first, then workspace default, and disclose partial saves. Honor explicit default-only/retain-override requests, prompt-history booleans, unset-versus-disabled follow-through, and existing personality preferences.
- [ ] T038 [US3] Extend `docs/setup.md` with existing-workspace merge and policy-update procedures preserving `AGENTS.md`, `CLAUDE.md`, overrides, personality, and every player record; include successful shared loading plus negative override/exclusion checks, manual policy replacement without template resets, capability discovery after host changes, and targeted recovery pointers.
- [ ] T039 [US3] Execute the resumption contract checks and `tests/scenarios/us3-resumption.md`, including all four pairs, meaningful-update categories, interrupted/denied/partial writes, and preference-save failures; record actual tool errors and before/after state comparisons in `docs/validation.md`, retaining raw evidence externally. Never mark a staged failure or agent-only save claim as observed persistence evidence.

**Checkpoint**: Shared records, separation, preference scope, and failure disclosures
work from prepared state independently of the new-game interview.

## Phase 6: User Story 4 — Protect discoveries while getting guidance (Priority: P1)

**Goal**: Apply the player's disclosure boundary to complete responses, preserve
mode selections, and keep one-time permission distinct from lasting preferences.

**Independent Test**: Seed known spoiler-bearing evidence and reported knowledge;
exercise all eight Story 4 scenarios in both hosts. Inspect complete responses and
supported artifacts for zero unauthorized disclosures, including a specific Hints
request followed by protected Hints and request-specific Strict permission followed
by unrelated advice. (FR-024–FR-026; SC-006.)

### Controlled scenarios

- [ ] T040 [P] [US4] Define default/Strict/Hints/Off, first explanation, changed/resumed settings, unknown boundaries/metadata, specific Hints exception, request-scoped Strict permission, spoiler-bearing source requests, and all supported presentation surfaces in `tests/scenarios/us4-spoilers.md`; include neutral permission wording, corrected reported knowledge, and an assumed attempt that cannot expand player knowledge.
- [ ] T041 [P] [US4] Create the default synthetic spoiler workspace rooted at `tests/fixtures/workspaces/spoilers/default/.cid/workspace.json` and complete sibling workspaces with current reported knowledge, unknown knowledge, contrasting modes and overrides, sensitive titles/locators, unknown metadata, and assumed-but-unreported outcomes; ensure fixtures distinguish disclosure permission from reported completion and contain no real unrequested spoilers.

### Implementation and observed validation

- [ ] T042 [US4] Register the prepared US4 scenarios in `tests/scenarios/manifest.md`, then complete mode/permission handling in `coaching/COACH.md`: briefly explain Strict/Hints/Off at the first sensitive interaction, persist actual choices, default to Hints, ask before Strict crosses reported knowledge, apply only a specifically requested Hints spoiler without extra confirmation, and retain the saved mode afterward; ambiguity requires neutral clarification or less revealing guidance.
- [ ] T043 [US4] Apply disclosure filtering throughout `coaching/COACH.md` to prose, headings, examples, reference labels/destinations/descriptions, images/captions, and interactive states; local access and source requests do not grant blanket disclosure, unknown metadata is conservative, assumptions never establish knowledge, and corrected knowledge narrows later advice.
- [ ] T044 [US4] Document spoiler modes, scoped changes, one-time Hints exceptions, Strict permission duration, and spoiler-safe source requests in `README.md`, keeping the explanation concise and consistent with preference precedence and FR-025's recorded clarification.
- [ ] T045 [US4] Execute `tests/scenarios/us4-spoilers.md` in both hosts and inspect every supported response surface/artifact, including changed-mode resumption and follow-ups after permission; record zero-disclosure checks, actual failures, and unsupported formats as untested in `docs/validation.md`. Preserve text fallback coverage even when optional visuals cannot run.

**Checkpoint**: Complete spoiler handling is independently demonstrable from seeded
records. US1–US4 form the P1 increment, subject to their observed results.

## Phase 7: User Story 5 — Use initiative while keeping assumptions correctable (Priority: P2)

**Goal**: Reduce repeated confirmation after explicit opt-in while preserving
reported/assumed/proposed distinctions and repairing transitive advice on correction.

**Independent Test**: In each host begin unset, observe the first relevant offer,
leave it unanswered, explicitly enable it, then receive at least three successive
recommendations without another preference confirmation. Discuss an alternative,
correct an assumption with transitive dependencies, reject advice, disable the
preference, and resume corrected state in the other host. (Story 5.1–5.5;
FR-016–FR-019; SC-007.)

### Contract checks and controlled scenarios

- [ ] T046 [P] [US5] Add self-contained provenance/dependency contract cases to `tests/test_contracts.py` for originating-plan references, entry/plan status enums, `supersedes`/`replaces` targets, proposal versus acceptance/completion, acyclic chains and invalidation snapshots; verify that reported corrections and transitive `needs_review` state coexist in one playthrough replacement without creating false success or cross-playthrough dependencies.
- [ ] T047 [P] [US5] Create the initial synthetic workspace rooted at `tests/fixtures/workspaces/follow-through/initial/.cid/workspace.json` and complete assumed-chain, corrected, rejected, and disabled sibling snapshots, retaining referenced old IDs/statements and a multi-hop entry→plan→assumed-entry→plan chain, plus an unrelated research-maintenance failure; ensure each snapshot respects the shared reference and graph rules.
- [ ] T048 [P] [US5] Define all five Story 5 scenarios and the complete opt-in/silence/three-recommendation/correction/rejection/disablement sequence in `tests/scenarios/us5-follow-through.md`, with expected saved snapshots, affected guidance, opposite-host resumption, and no inferred reward/win/knowledge.

### Implementation and observed validation

- [ ] T049 [US5] Register the prepared US5 scenarios in `tests/scenarios/manifest.md`, then complete follow-through offer and assumed-attempt handling in `coaching/COACH.md`: offer at the first useful concrete recommendation, track the offer without treating silence as consent, require explicit enablement, apply it without repeated preference announcements, link assumptions to their plans, and distinguish attempted actions from acceptance, victory, rewards, or discovered knowledge.
- [ ] T050 [US5] Implement correction traversal and plan revision in `coaching/COACH.md`: supersede/retract the old assumption, add the current reported correction, mark transitive active entries/plans `needs_review`, recompute/withdraw advice with valid prerequisites, and save correction plus invalidations/revision together. Preserve referenced provenance; failed registry or research updates cannot block the correction attempt.
- [ ] T051 [US5] Complete alternative discussion, rejection, and disablement in `coaching/COACH.md`: discussions remain proposed until explicit selection, only reports establish `completed_reported`, rejected advice informs relevant scoped preferences, and disabling prevents new assumptions without converting existing assumptions into facts or silently deleting them.
- [ ] T052 [US5] Add concise correction/state-transition examples to `docs/record-format.md`, quoting the data-model behavior: “Preserve the ID and short statement of the old entry while referenced.” and “Save the correction, invalidations, and revised guidance in one playthrough replacement.” Show the distinction between reported facts, assumed attempts, proposed/accepted plans, and disabling the preference without building an event store or full simulator.
- [ ] T053 [US5] Run the follow-through contract cases and `tests/scenarios/us5-follow-through.md` in both hosts, verify at least three recommendations with zero repeated preference confirmations, no false selection/success, the transitive saved correction, disablement, and opposite-host recovery; record actual outcomes and assumption/spoiler-boundary checks in `docs/validation.md`.

**Checkpoint**: Opt-in initiative and correction are independently testable with
seeded records; no new assumptions are enabled by setup or test convenience.

## Phase 8: User Story 6 — Direct the coaching conversation (Priority: P2)

**Goal**: Give contextual, flexible advice with honest reasoning and usable text,
respecting the player's style, skipped questions, and changing goals.

**Independent Test**: Seed a known playthrough and evidence, then ask about a loadout,
next steps, a changed goal, and a comparison with both material and immaterial
missing details. Cover all five Story 6 scenarios in both hosts. At least five real
players across both hosts and three games try goal redirection; the same ≥4 rate
usefulness ≥4/5 and report successful redirection. Every evaluated visual has usable
equivalent text. (FR-020–FR-023, FR-027; SC-008.)

### Controlled scenarios

- [ ] T054 [P] [US6] Define all five Story 6 acceptance scenarios, skipped/material-question alternatives, strategy deduction labelling, existing personality preferences, unsupported visuals, and the five-player usefulness/redirection protocol in `tests/scenarios/us6-player-direction.md`; preserve the quickstart's 1–5 scale, same-four-player rule, and equivalent-text criteria.
- [ ] T055 [P] [US6] Create the contextual synthetic workspace rooted at `tests/fixtures/workspaces/player-direction/contextual/.cid/workspace.json` and complete sibling variants with reported equipment, constraints, goals, sourced mechanics, valid deduction premises, unanswered material/immaterial questions, and style preferences; provide enough evidence for independent US6 trials without rerunning the new-game interview or inventing a game mechanic.

### Implementation and observed validation

- [ ] T056 [US6] Register the prepared US6 scenarios in `tests/scenarios/manifest.md`, then complete contextual advice and redirection in `coaching/COACH.md`: connect proposed actions/tradeoffs to known loadout, progress, goals, mechanics, and constraints; ask only materially relevant questions, honor skipped questions with safe/conditional alternatives, persist redirected goals/research depth, and preserve concise host/personality preferences without a required persona or rigid workflow.
- [ ] T057 [US6] Complete original-reasoning handling in `coaching/COACH.md`: derive strategies from applicable supported findings, record valid `derived_from`/`depends_on` premises and reasoning status, identify important untested deductions, and reconsider the advice when a premise or player assumption is corrected.
- [ ] T058 [US6] Complete optional comparison/visual handling in `coaching/COACH.md`, discovering actual capabilities and using an aid only when useful and permitted; provide equivalent decision-relevant options, tradeoffs, and actions in text and inspect spoiler-bearing labels, images, and interactive states. Unsupported visual tools must never block coaching or be claimed used.
- [ ] T059 [US6] Execute the controlled US6 scenarios in both hosts and conduct the at-least-five-real-player review across both hosts and three games; record anonymized ratings, separate redirection responses, same-player ≥4/5 threshold, text equivalence, and limitations in `docs/validation.md`. Missing participants or unsupported optional paths remain untested; agent simulations cannot complete the human-review obligation.

**Checkpoint**: All six stories have implementations and their own evidence; full
MVP acceptance still depends on the final coverage and constitution review.

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Reconcile the integrated policy, verify the complete acceptance set,
and report actual scope/compatibility without hiding failed or untested behavior.

- [ ] T060 [P] Finish the user documentation in `README.md`, `docs/setup.md`, and `docs/record-format.md`: verify install/update/merge instructions, shared-policy ownership, local records versus provider processing, no credentials/transcript retention, one-player sequential scope, optional integrations/mobile host facilities, required approvals, and excluded capabilities; align all examples with the final v1 templates and reviewed contracts.
- [ ] T061 [P] Review `coaching/COACH.md` against all 27 requirements, both contracts, and constitution principles I–V, removing duplication/contradictory story edits while preserving evidence ordering, prompt suppression, effective preferences, full-response spoiler checks, correction traversal, save timing, and player-directed text. Carry unresolved deviations into T064's final report; no silent scope/constitution amendment or duplicated host policy is allowed.
- [ ] T062 Run `python3 -m unittest discover -s tests -p 'test_*.py' -v` for final `tests/test_contracts.py`, verify every template and positive/negative/recovery fixture family, and record the command/result in `docs/validation.md`; ensure expected rejections yield a successful test suite and that tests require no coaching-time Python runtime, network, private records, or model API.
- [ ] T063 Validate the final integrated distribution with `specs/001-ai-game-coach/quickstart.md` and `tests/scenarios/manifest.md`, checking SC-001–SC-008, every story acceptance scenario, both hosts, all resumption pairs, setup/update preservation, actual write/integration failures, and optional presentation paths; reuse existing evidence only for unchanged behavior and rerun scenarios affected by later policy edits. Record host-level and aggregate pass/fail/untested outcomes in `docs/validation.md` without dropping failed trials or claiming unavailable coverage passed.
- [ ] T064 Complete the acceptance and constitution report in `docs/validation.md`, linking sanitized requirement/scenario/SC results to externally retained evidence, actual tested host versions, source-display compatibility, observed persistence/research/spoiler results, human-review thresholds, and remaining deviations or untested paths. Do not claim the MVP accepted with unmet requirements; leave unfinished execution tasks open and leave all changes uncommitted pending explicit approval for a specific commit.

## Dependencies & Execution Order

### Phase dependencies

1. T001 establishes paths; T002 and T003 can then run concurrently.
2. After Phase 1, T004 and T005 can run concurrently. After both complete,
   T006–T011 can prepare disjoint templates in parallel; keep shared
   documentation edits in T012. T012 → T013 → (T014 and T015) → T016 completes
   the shared foundation.
3. All six stories depend on the completed foundation. Their prepared fixtures
   make each story testable without a successful conversation from another story.
   Implement the story phases in priority/specification order by default.
4. Each story's preparation wave precedes its policy changes. Policy changes
   within a story are sequential, and the observed validation task comes last.
5. All `coaching/COACH.md`, `tests/test_contracts.py`, `docs/record-format.md`,
   `tests/scenarios/manifest.md`, and `docs/validation.md` edits are serialized
   across stories. Parallel markers never apply to shared-file follow-up edits.
6. T060 and T061 can perform disjoint document/policy work after all stories.
   T062 → T063 → T064 verifies the
   integrated result. Any policy correction requires rechecking affected scenarios.

### User story dependency graph

```text
Setup T001–T003
       |
Foundation T004–T016
       |
       +--> US1 T017–T022  (P1: new-game help)
       +--> US2 T023–T030  (P1: evidence/reuse)
       +--> US3 T031–T039  (P1: shared persistence)
       +--> US4 T040–T045  (P1: disclosure boundaries)
       +--> US5 T046–T053  (P2: correctable initiative)
       +--> US6 T054–T059  (P2: player direction)
                     |
         All desired story results joined
                     |
             Polish T060–T064
```

There is no hard story-to-story implementation prerequisite beyond the shared
foundation. US2 deepens the baseline research behavior, US3 hardens its persistence,
and US4 hardens its disclosure behavior; US5/US6 build on the same common record
contracts. These are overlapping policy sections, so **independent testability is
not permission to edit the common files concurrently**. Final acceptance exercises
their interactions, including assumptions versus spoilers and correction versus
failed research maintenance.

### Parallel execution examples per story

These are available work waves, not instructions to spawn agents automatically.
Complete the shared foundation before starting any of them. The first sequential
implementation task in each row registers its prepared scenarios in the shared
manifest; freeze trial details before observed validation.

| Story | Concurrent preparation examples | Required next sequence |
| --- | --- | --- |
| US1 | T017: `tests/scenarios/us1-new-game.md`; T018: `README.md` walkthrough | T019 → T020 → T021 → T022 |
| US2 | T023: self-contained cases in `tests/test_contracts.py`; T024: `tests/fixtures/workspaces/research/`; T025: `tests/scenarios/us2-evidence.md` | T026 → T027 → T028 → T029 → T030 |
| US3 | T031: self-contained cases in `tests/test_contracts.py`; T032: `tests/fixtures/workspaces/resumption/`; T033: `tests/scenarios/us3-resumption.md` | T034 → T035 → T036 → T037 → T038 → T039 |
| US4 | T040: `tests/scenarios/us4-spoilers.md`; T041: `tests/fixtures/workspaces/spoilers/` | T042 → T043 → T044 → T045 |
| US5 | T046: self-contained cases in `tests/test_contracts.py`; T047: `tests/fixtures/workspaces/follow-through/`; T048: `tests/scenarios/us5-follow-through.md` | T049 → T050 → T051 → T052 → T053 |
| US6 | T054: `tests/scenarios/us6-player-direction.md`; T055: `tests/fixtures/workspaces/player-direction/` | T056 → T057 → T058 → T059 |

Do not overlap two rows' edits to the test module, manifest, README, or common
policy. Independent fixture/scenario drafting across rows is possible after the
foundation, but host trials require the relevant policy increment to be installed.

## Requirement & Acceptance Coverage

| Requirement group | Implementation tasks | Observed validation |
| --- | --- | --- |
| FR-001 | T013–T016, T034, T038 | T022, T039, T063: both hosts, loading and shared records |
| FR-002–FR-004 | T019–T021 | T022: Story 1.1–1.5, SC-001 |
| FR-005–FR-008 | T013, T026–T029 | T030: Story 2.1–2.6, SC-002–SC-003 |
| FR-009–FR-011 | T009–T012, T026–T029 | T030: Story 2.2–2.7, actual access and FR-009 compatibility |
| FR-012–FR-015 | T006–T016, T034–T038 | T039: Story 3.1–3.5, SC-004–SC-005; T063 includes research/plan saves |
| FR-016–FR-019 | T008, T012–T013, T037, T049–T052 | T053: Story 5.1–5.5, SC-007; T039 covers partial preference saves |
| FR-020–FR-023 | T020–T021, T056–T057 | T022, T059: Story 6.1–6.4, SC-001/SC-008 |
| FR-024–FR-026 | T013, T037, T042–T044 | T045: Story 4.1–4.8, SC-006; T053 covers assumed-knowledge interaction |
| FR-027 | T013, T058 | T045/T059: Story 6.5, equivalent text and supported-surface checks |
| Constitution I–V and MVP boundary | Foundation, story policy tasks, T060–T061 | T062–T064: complete traceability, actual evidence, no unapproved commits |

All 35 acceptance scenarios in the current specification are assigned above:
US1 = 5, US2 = 7, US3 = 5, US4 = 8, US5 = 5, US6 = 5. Include the additional
edge/failure cases in the quickstart and task descriptions in the frozen manifest.
Neither fixture/schema validation nor preparing this task list establishes a
passing behavioral result.

## Implementation Strategy

### First usable slice

Complete Setup, Foundation, and US1 (T001–T022), then validate it independently.
This is the recommended first demonstration: useful new-game help with essential
evidence, persistence, disclosure, and consent rules already in the foundation.
It is not the complete MVP or a reason to remove the other acceptance obligations.

### Incremental delivery

Proceed through US2, US3, and US4, validating each from its own seeded workspace.
US1–US4 provide the P1 increment. Then add US5 and US6 in specification order.
The defined MVP includes all six stories and SC-001–SC-008; only the final evidence
report can establish whether those requirements have been met. Demo checkpoints
require no service deployment, publishing, or Git commit.

### Validation and task completion

Freeze relevant manifest entries before trials and keep all scheduled results,
including failures and untested cases. Use synthetic records for destructive failure
injection and fresh processes for resumption. Do not substitute simulations for real
players or discovered tools for actual queries. If required resources are absent,
record the limitation, continue independent implementation work, and leave the
unfinished observed-validation obligation open. Never silently reduce thresholds.

Use the standard-library suite for contracts and actual host activity for behavior.
After any later shared-policy edit, rerun the scenarios it can affect; avoid repeating
unchanged trials solely to produce more logs. Keep records concise and sources
traceable. Preserve all reviewer-owned checklist states and report unresolved
constitution deviations before acceptance.

## Generation Summary

64 tasks: Setup 3; Foundation 13; US1 6; US2 8; US3 9; US4 6; US5 8; US6 6;
Polish 5. Parallel opportunities are the bounded waves described above, with shared
file edits and player-workspace use kept sequential.

Pre-generation and post-generation hook checks found no
`.specify/extensions.yml`; no extension hooks are registered for this run.
This command generates the task list only and does not implement or certify Cid.
