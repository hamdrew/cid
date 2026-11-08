# Implementation Plan: Cid — Local AI Video Game Coach

**Branch**: `main` (actual Git branch) | **Date**: 2026-11-07 | **Spec**: [spec.md](spec.md)

**Feature context**: `001-ai-game-coach`; `setup-plan.sh --json` returns this as
`BRANCH` from the saved feature-directory context. No Git branch was created.

**Input**: `specs/001-ai-game-coach/spec.md`

## Summary

Deliver a local, conversational video game coach through shared Markdown instructions
and small portable JSON records. A workspace-root Codex adapter and Claude import
adapter load one coaching policy and the same game/playthrough records. The host
performs research, reasoning, and local updates; Cid adds no service, custom model
API, or companion runtime. Development-only contract checks and observed coaching
trials validate the format and acceptance behavior separately.

Use the instruction-and-record approach selected in [research.md](research.md).
Alternatives considered were host-specific duplicated packages and a companion
program; both add maintenance or installation without a demonstrated requirement.
These are planning decisions for review, not previously approved implementation.

## Technical Context

**Language/Version**: UTF-8 Markdown instructions and JSON v1 records; Python 3.11+
standard library for development tests only. No player-facing programming runtime.

**Primary Dependencies**: An authenticated Codex CLI or Claude Code CLI with local
file tools; whichever research tools the running host actually provides. Both CLIs
are needed for full validation. No pip/npm packages or mandatory game integrations.
Inspected baselines: Codex CLI 0.167.0 and Claude Code 2.1.319; compatibility is
certified by recorded trials rather than an unverified minimum version.

**Storage**: User-selected local workspace: `.cid/COACH.md`, `.cid/workspace.json`,
and `games/<game-id>/` containing game metadata, sources, integration observations,
topic knowledge, and distinct playthrough JSON files. Files are authoritative;
host chat history, automatic memory, and Git are not required for persistence.

**Testing**: Standard-library `unittest` for record/template invariants and negative
fixtures; manual fresh-process acceptance in both CLIs with tool traces and record
snapshots; five-player usability review. No API-backed evaluation framework.

**Target Platform**: Local CLI environments with readable/writable workspace files;
initial validation on macOS/Linux. Other host-supported environments require their
own evidence. Optional mobile use relies entirely on existing host facilities and
does not add a Cid deployment, guarantee, or independent execution path.

**Project Type**: Instruction-and-record distribution with thin host setup.

**Performance Goals**: Meet SC-001's ≥9/10 useful setup outcomes within three player
replies; zero broad searches when sufficient saved/indexed evidence exists; selective
record loading. No invented network latency or throughput target.

**Constraints**: One player and sequential editing; preserve existing workspace
instructions; only request version details that change advice; no exhaustive game
database, ingestion, telemetry, autonomous gameplay, cloud sync, hosted accounts,
or custom mobile infrastructure. Do not automatically commit player or project data.

**Scale/Scope**: Six stories, 27 requirements, eight success criteria. Support multiple
games and playthroughs without merging progress. Evaluate at least three games, ten
setup trials, all four host-resumption pairs, and at least five actual players.

## Constitution Check

Pre-research gate evaluated against constitution 1.0.0; post-design recheck evaluates
the artifacts linked below. PASS means the design meets the gate, not that the
unimplemented product has passed acceptance tests.

| Gate | Pre-research | Post-design evidence and observable validation |
| --- | --- | --- |
| I. Evidence before game facts | PASS: research order and provenance required | PASS: source/finding contracts, applicability and actual-access records; SC-002–003 inspect claim support and tool order, including conflict/unavailable cases |
| II. Durable, portable records | PASS: shared local files and separate playthroughs | PASS: workspace/record contract and verified-save protocol; SC-004–005 cover all host pairs, meaningful updates, interruption, failure, and separation |
| III. Correctable assumptions | PASS: explicit opt-in and provenance required | PASS: entry/plan IDs and transitive invalidation; SC-007 checks silent non-enable, three recommendations, no false success, correction and disablement |
| IV. Spoiler protection | PASS: default Hints and established boundaries | PASS: response contract covers all modes and presentation surfaces; SC-006 includes explicit one-time Hints exception without preference change |
| V. Player-directed coaching | PASS: relevant questions and flexible help | PASS: normal-language contract, skipped questions, personality and text fallback; SC-001/008 validate usefulness and real goal redirection |
| MVP boundary and simplicity | PASS: no service or custom API | PASS: instructions and files only; Python is development-only; integrations optional; exclusions unchanged |
| Quality and governance | PASS: observable validation and no unapproved commits | PASS: quickstart/results protocol distinguishes pass/fail/untested; no implementation, commit, or constitution amendment performed |

The Hints interpretation is explicit in research decision 6: default protection
continues, with only the specifically requested exception permitted by clarified
FR-025. Strict permission behavior is unchanged. The existing constitution
ratification-date TODO is not a technical uncertainty and remains untouched.
No unjustified design-gate violations or unresolved technical clarifications remain.
FR-009 host citation compatibility is an explicit implementation acceptance gate:
it is not established by CLI help or the API citation documentation. A host that
adds unrequested citations fails that requirement; higher-priority citation rules
must still be honored. Planning does not certify either host's product behavior.

### Planning refresh decisions

This refresh retains the existing delivery approach and resolves design details
without changing the specification or constitution. Assumed follow-through never
expands established spoiler knowledge. Strict permission is limited to the requested
answer. Meaningful updates are attempted and verified before concluding the response
that handles them; failed or inconclusive saves are identified there. Finding
derivations as well as progress/plan dependencies must be acyclic.

The validation guide defines setup-reply counting, actionable guidance, factual
support, broad searches, unauthorized disclosure, text equivalence, and usefulness
ratings. Trial coverage is fixed before evaluation. Local records do not imply
on-device inference; no new sharing, retention, or deletion service is introduced.
These are planning choices implementing the existing requirements, not new MVP
capabilities or claims of measured acceptance.

### Requirement-to-design traceability

| Requirements | Design obligation | Acceptance reference |
| --- | --- | --- |
| FR-001, FR-012–FR-015 | Shared policy and records, distinct contexts, selective state, verified saves and targeted recovery; workspace contract and data model | Story 3; SC-004–SC-005 |
| FR-002–FR-004 | Relevant identity/version questions, bounded initial research, skippable setup; coaching contract | Story 1; SC-001 |
| FR-005–FR-011 | Ordered reuse, actual-access evidence, applicability, source quality, optional integrations, source visibility; coaching contract and finding/source/integration records | Story 2; SC-002–SC-003 |
| FR-016–FR-019 | Explicit opt-in, reported/assumed/proposed provenance, transitive reconsideration, scoped preference changes; playthrough and preference model | Story 5; SC-007 |
| FR-020–FR-023, FR-027 | Contextual actions, material clarification, labelled deductions, player direction, usable text; coaching contract and scoring definitions | Stories 1 and 6; SC-001, SC-008 |
| FR-024–FR-026 | Default Hints, scoped permissions, reported-knowledge boundaries, complete-response protection; coaching contract and preferences | Story 4; SC-006 |

Setup preservation, revision checks, recovery ordering, and preference precedence
are design mechanisms for FR-001 and FR-012–FR-019 and the specification's scope
assumptions. They add no companion runtime or simultaneous-writer guarantee.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-game-coach/
├── spec.md
├── checklists/
│   ├── requirements.md
│   └── coaching.md              # reviewer-owned; markers unchanged by planning
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    ├── workspace.md
    └── coaching.md
```

`tasks.md` is a later `$speckit-tasks` output and is not generated by this command.

### Planned distribution source (repository root)

```text
README.md
coaching/COACH.md                   # single canonical coaching policy
adapters/
├── codex/AGENTS.md                 # short shared-policy/record bootstrap
└── claude/CLAUDE.md                # @AGENTS.md
templates/
├── workspace/.cid/workspace.json   # empty initialized workspace
└── records/
    ├── game.json
    ├── playthrough.json
    ├── knowledge.json
    ├── sources.json
    └── integrations.json
docs/
├── setup.md                        # fresh setup and existing-file merge
├── record-format.md
└── validation.md
tests/
├── test_contracts.py
├── fixtures/workspaces/            # valid/invalid controlled records
└── scenarios/                      # prompts, expected behavior, scoring rubric
```

### Installed player workspace

```text
AGENTS.md
CLAUDE.md
.cid/
├── COACH.md
└── workspace.json
games/<game-id>/
├── game.json
├── sources.json
├── integrations.json
├── knowledge/<topic-id>.json
└── playthroughs/<playthrough-id>.json
```

**Structure Decision**: Keep development/planning files separate from a player's
selected workspace. Copy the shared policy and adapters during setup, merge existing
host instructions, and never require a clone to hold personal records. Only relevant
topic files are created. Installing later policy updates must preserve all records
and user instructions; no automatic policy synchronization is required for the MVP.

## Phase 0 — Research outcome

[research.md](research.md) resolves delivery, current host loading, record format,
failure recovery, assumption dependencies, source access, spoilers, and validation.
No new runtime dependency or scope amendment is justified. Host capabilities are
observed per session and never inferred from an integration's discovery record.

## Phase 1 — Design outcome

- [data-model.md](data-model.md) defines entities, ownership, validation, preference
  precedence, provenance, correction transitions, and evidence invalidation.
- [contracts/workspace.md](contracts/workspace.md) defines the portable file/setup
  interface, normal resumption, writes, and recovery. No HTTP or custom CLI API exists.
- [contracts/coaching.md](contracts/coaching.md) defines the user-facing conversational
  contract, research ordering, response/source visibility, and spoiler permissions.
- [quickstart.md](quickstart.md) provides future implementation validation commands,
  controlled failure scenarios, all eight success-criterion checks, and honest reporting.

Post-design constitution gates pass as documented above. Planning ends here;
implementation and product evaluation have not been performed.

The reviewer-owned [coaching checklist](checklists/coaching.md) is preserved with
all review states unchanged. Planning supplies design detail; it does not mark that
requirements review complete or bypass any later implementation checklist gate.

## Resumption verification — 2026-11-08

Resumed after quota exhaustion using the saved artifacts rather than regenerating
them. `setup-plan.sh --json` preserved this plan and resolved the existing
`001-ai-game-coach` feature context; the actual Git branch remains `main`.

- Research revalidation found no material change to the host setup decisions.
  Local CLI versions remain Codex 0.167.0 and Claude Code 2.1.319; current local
  help and the official references in research decision 2 support the documented
  loading mechanisms and launch options. Product behavior still requires trials.
- Rechecked all 27 functional requirements and eight success criteria against the
  design and validation guide. The post-design constitution assessment above stands.
- Verified all six planning artifacts are nonempty, their local Markdown links
  resolve, code fences are balanced, and no template or technical-clarification
  placeholders remain. `check-prerequisites.sh --json --require-spec` succeeds
  and discovers research, data model, contracts, and quickstart.
- `.specify/extensions.yml` is absent at both pre-plan and post-plan checks;
  no extension hooks are registered for this run.
- The specification, constitution, and reviewer-owned checklists remain unchanged.
  No implementation, product acceptance trial, or Git commit was performed.

Phase 1 planning is complete. The next workflow is `$speckit-tasks`, using these
artifacts to generate the implementation task list. The separate coaching
requirements checklist remains pending reviewer evaluation before implementation.
