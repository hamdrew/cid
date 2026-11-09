# Implementation Plan: Wiki research through the official MediaWiki API

**Branch**: `main` | **Date**: 2026-11-08 | **Spec**: [spec.md](spec.md)

**Input**: `specs/003-mediawiki-api-research/spec.md`
Spec Kit resolves feature identifier `003-mediawiki-api-research`. The actual Git
branch is `main`, and no branch was created.

## Summary

Teach the shared coaching policy to read MediaWiki wikis, Fandom and others,
through their official `api.php` when ordinary pages are hidden behind a browser
challenge. Cid searches the wiki for a named need, reads the one to three pages
that address it as compact wikitext, and saves its own summaries. Each summary
cites the page title, reader address and revision. Requests are serial,
anonymous, read-only, use `maxlag`, and stop on lag, rate-limit, challenge or
block. Cid respects readable robots rules and reports failures honestly before
falling back to the existing research steps. Records gain only optional additive
v1 fields. Nothing is installed: requests use the host's existing shell HTTP
client or fetch tool.

## Technical Context

**Language/Version**: Markdown coaching policy. UTF-8 JSON schema v1 records.
Python 3.11+ standard library for development-only deterministic checks.
**Primary Dependencies**: The host's existing capabilities: a shell with `curl`
where network is permitted, otherwise the host fetch tool. Wikis' MediaWiki
Action API (observed 1.43). No new packages, helpers, MCP servers or services.
**Storage**: Existing `sources.json` and knowledge topic files, with optional
`mediawiki` on sources and `page_title`/`revision_id` on evidence
([data model](data-model.md)).
**Testing**: Existing `unittest` contract suite, extended with optional-field
validation and two synthetic wiki fixtures (success and preserved-success failure). Conversational behaviour is
validated by ordinary owner use only.
**Target Platform**: Codex CLI and Claude Code CLI workspaces. Network
availability differs per host and is recorded, not assumed.
**Project Type**: Shared instruction-and-record distribution with natural-language UI.
**Performance Goals**: About six requests at most per named need, excluding the
per-session robots check and endpoint probes. Zero requests
when saved findings are adequate. One batched request for revision checks.
**Constraints**: Read-only and anonymous. Official API only. One request at a
time. `maxlag=5` and `assert=anon`. Readable robots rules honoured. No
circumvention of challenges or blocks. No copied page text. No bulk download.
Nothing installed for players. No AI-launched tests or unapproved commits.
**Scale/Scope**: One player's workspace and a handful of pages per need. The work
covers the policy subsection, record conventions, focused checks and a README note.

All unknowns were resolved in [research.md](research.md), with live observations
from 2026-11-08. The owner chose the strict
[robots group scope](research.md#r5-robots-rules), which includes the
user-initiated Claude and ChatGPT/Codex tokens.

## Constitution Check

Evaluated against [constitution v1.4.0](../../.specify/memory/constitution.md)
before research and again after design.

| Gate | Before research | After design |
| --- | --- | --- |
| I: Evidence before game facts | Pass: indexed wikis are read via the API in step 2, newly found ones in step 4; the ladder order is unchanged | Pass: only accessed pages become evidence with page and revision. Discovery is never cited. Selection is per named need, so there is no exhaustive scraping |
| II: Durable, portable records | Pass: existing source and evidence records | Pass: optional additive v1 fields are documented in the data model. No migration. Failures persist while earlier success is preserved. No credentials stored |
| III: Correctable advice | Pass: unchanged | Pass: revision changes feed the existing conflict and version reassessment |
| IV: Spoiler protection | Pass: unchanged | Pass: search titles, snippets and page addresses are spoiler-checked before display. Spoiler metadata is unchanged |
| V: Player-directed coaching | Pass: removes manual pasting | Pass: failures are reported in the same reply and coaching continues via fallbacks. Pasted text is still accepted |
| MVP boundaries and simplicity | Pass: no runtime or service | Pass: host's existing shell or fetch tool only. No helper, MCP server or Python for players |
| Personal-use workflow | Pass | Pass: deterministic record checks only. Planning probes were manual, serial and model-free. Behaviour is unverified until observed |
| Git approval | Pass | Pass: all changes left uncommitted pending explicit approval |

No violations and no amendment are required.

## Project Structure

### Documentation (this feature)

```text
specs/003-mediawiki-api-research/
├── spec.md                         # Requirements
├── plan.md                         # This file
├── research.md                     # Decisions R1–R10 and live observations
├── data-model.md                   # Optional additive v1 fields
├── quickstart.md                   # Deterministic checks and ordinary-use observations
├── contracts/
│   └── mediawiki-research.md       # Behaviour contract for the policy
├── checklists/
│   └── requirements.md             # Spec quality review
└── tasks.md                        # Created later by /speckit-tasks
```

### Implementation surface (repository root)

```text
coaching/COACH.md                    # Add "MediaWiki wikis" under Evidence before game facts; extend portable shapes
README.md                            # Short note: wiki API reading, ethics, no setup
tests/test_contracts.py              # Validate optional mediawiki/page_title/revision_id when present
tests/fixtures/workspaces/research/  # New synthetic wiki fixture (example.invalid locators)
templates/records/                   # No change (empty collections)
adapters/{codex,claude}/             # No change
```

**Structure Decision**: Keep one canonical policy and the existing record
ownership. The wiki is a source, and the API is how that source is read
([research R8](research.md#r8-record-representation)).

## Phase 0: Research

See [research.md](research.md). It covers the request mechanism per host (R1),
endpoint discovery (R2), etiquette and back-off without sleeping (R3),
identification (R4), robots scope (R5), page selection and reading (R6),
revision reuse (R7), record representation (R8), saving (R9) and where the
behaviour lives (R10).

## Phase 1: Design

- [Data model](data-model.md): wiki source `mediawiki {api, robots, last_failure}`
  and evidence `page_title` + `revision_id`. Everything is optional and existing
  records stay valid.
- [Contract](contracts/mediawiki-research.md): when the path applies, per-session
  preconditions, request rules, response handling table, selection, reuse,
  saving and the never-list.
- [Quickstart](quickstart.md): unittest expectations, an optional manual curl
  check and ordinary-use observations per story.

## Requirement coverage

| Requirement | Design coverage |
| --- | --- |
| FR-001 | Contract "When it applies", R1 and R2 |
| FR-002 | Contract "Selecting and reading", R6 |
| FR-003, FR-004 | `assert=anon`, read-only modules, the never-list, stop on challenge or block (R3) |
| FR-005 | R5 robots per session. Unreadable does not block |
| FR-006 | R3 serial requests, `maxlag`, `Retry-After` spacing, one retry, session stop |
| FR-007 | R4 user agent via shell. Host default otherwise. No browser imitation |
| FR-008 | R7 and evidence `revision_id`. Batched `prop=info` |
| FR-009 | R9 and the data model evidence rules |
| FR-010 | Source `access_status` plus `mediawiki.last_failure`. Success preserved |
| FR-011 | Contract response table: tell the player, then fall back |
| FR-012 | R1: existing shell or fetch only |
| FR-013 | Additive fields only. Step 2/4 pointers only. Non-wiki research steps untouched; one general polite-access paragraph (T021) adds restrictions only, per constitution v1.4.0 Principle I |

## Implementation handoff and review focus

- Write the policy subsection compactly in the existing COACH.md voice. Do not
  paste the full research or command lines, but give the exact query parameters
  and the response table.
- Extend `validate_document` for `sources` and `knowledge` so that the new
  optional fields are checked when present. Unknown keys elsewhere stay
  preserved. Add the cross-record rule about evidence after a robots disallow.
- Make the README note state that no setup is needed and that wiki failures are
  reported honestly.
- Review points: robots group merging and the token list (R5), Codex
  shell-network availability, fetch-tool summarisation of JSON, and spoilers in
  search snippets.
- Run `python3 -m unittest tests/test_contracts.py`. Report what it establishes
  and leave behaviour as unobserved.

## Complexity Tracking

No constitution violations or added infrastructure to justify.
