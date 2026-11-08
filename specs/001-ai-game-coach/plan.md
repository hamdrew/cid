# Implementation Plan: Cid — Local AI Video Game Coach

**Spec**: [spec.md](spec.md) · **Constitution**: [v1.2.0](../../.specify/memory/constitution.md)

## Approved design

Cid is a personal coaching tool. The owner uses it normally and sends bullet points
about behavior they want changed. A short optional checklist helps explore a few
less common situations when convenient. There are no trial quotas, participant
requirements, rating forms, mandatory transcripts or acceptance matrices.

The alternative was retaining the formal scenario campaign and its separate
reports. The owner chose the lightweight approach because it fits personal use and
keeps feedback inexpensive. The README is the single setup, usage and feedback guide;
the existing data model and contracts remain technical references.

An assistant may review transcripts and a test workspace the owner explicitly
shares or requests it inspect, in the current conversation. It must distinguish
what the supplied evidence shows from what is unknown. It must never launch AI
sessions, model APIs, test agents, automated players or AI graders for testing.

## Implementation boundary

Keep the existing shared Markdown policy, thin Codex/Claude adapters and portable
JSON v1 records. No companion runtime, hosted service or model API is introduced.
Python 3.11+ is only for the model-free development contract checks.

| Path | Responsibility |
|---|---|
| `README.md` | Setup, updates, normal use, optional checks and bullet-point feedback |
| `coaching/COACH.md` | Canonical installed coaching behavior and record shapes |
| `adapters/` | Host loading instructions |
| `templates/` | Empty workspace and record templates |
| `tests/test_contracts.py` and fixtures | Model-free schema/reference checks |
| `specs/001-ai-game-coach/` | Behavioral requirements, data model and technical contracts |

## Constraints and checks

- Preserve all 27 functional requirements, spoiler protections and record contracts.
- Preserve existing implementation files and reviewer-owned checklist edits.
- Retire the separate documentation directory and formal conversation-scenario suite.
- Keep historical reports in a local backup outside the active repository documents.
- Keep the ban on launching AI tools for testing, including unattended retries.
- Allow requested review of user-shared evidence in this conversation only; no extra
  model calls, test subagents or automated grading.
- Never claim unobserved behavior works. Feedback and known limitations are enough;
  the owner does not need to maintain a certification report.
- Do not create or amend a Git commit without approval for that specific commit.

## Documentation update steps

- [X] Clarify the constitution's user-requested evidence-review exception.
- [X] Consolidate setup, use and lightweight feedback into the README.
- [X] Replace numerical acceptance gates with personal-use success criteria.
- [X] Retire duplicate docs and formal scenario files; reconcile technical references
  and historical task records without inventing passing results.
- [X] Check links, preserve implementation files, and run only the model-free suite.

## Verification focus

Check that setup still protects existing workspaces; links resolve after removal;
old testing quotas are no longer active instructions; evidence review does not
permit launching AI tests; and policy/templates/contracts retain their behavior.
The owner will try any changed coaching behavior during ordinary use.

## Local verification of the documentation cleanup

For that documentation-only cleanup, the 29 standard-library contract tests passed
and active links resolved. At that point the functional requirements, policy,
adapters, templates, test code and reviewer-owned checklists were unchanged. Earlier docs/scenarios were copied
to a local backup before removal. No AI test tools, model APIs or test agents were
launched. Behavioral tweaks will be guided by the owner's ordinary use and feedback.

## Feedback update: basic orientation before tailored advice

The owner reported that coaching looked up the next quest step without general
research or a progress/stat interview. The old wording allowed a single focused
question and treated evidence for the immediate request as sufficient. FR-003,
FR-004, Story 1, its coaching contract and the canonical policy now make the broader
first-time coaching information need explicit.

Default to a small spoiler-safe game/progression/mechanics research pass and a
brief interview about missing progress, goals, relevant stats/build/equipment and
difficulties. Do not treat a known quest location as a complete player profile.
Keep questions skippable, honor quick-answer requests, reuse saved foundations and
avoid a full stat sheet or exhaustive game guide. No record schema change is needed.

The implementation is the revised policy, with matching specification, contract and
README guidance. Contract fixtures retain only the JSON needed for model-free checks. Verification is limited to local
record checks, link checks and file-preservation checks. The owner will observe the
new onboarding behavior in normal use; no AI test sessions may be launched.
