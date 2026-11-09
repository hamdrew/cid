---
description: "Implementation tasks for wiki research through the official MediaWiki API"
---

# Tasks: Wiki research through the official MediaWiki API

**Input**: Design documents from `specs/003-mediawiki-api-research/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/mediawiki-research.md`, `quickstart.md`, and `.specify/memory/constitution.md` (v1.4.0).

**Tests**: The plan and quickstart call for deterministic, model-free record checks: optional-field validation, one cross-record rule and synthetic wiki fixtures. Reuse `validate_document`, `validate_workspace`, `fixture_documents` and `check_snapshot` in `tests/test_contracts.py`. No AI sessions, model calls, automated players, live wiki requests from tests or policy-keyword tests. Record validity does not prove conversational behaviour; that stays an ordinary-use observation.

**Organization**: One phase per user story from `spec.md`. US1 and US2 are both P1 and together form the MVP: the reading path must not ship without its robots, stop and fallback rules. All policy edits touch `coaching/COACH.md` and are therefore serialized in task order.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run alongside other [P] tasks in the same phase (different files, no dependency on an incomplete task).
- **[US1]–[US3]** map to the user stories in `spec.md`. Setup, foundational and polish tasks have no story label.
- All paths are relative to the repository root.

## Path Conventions

- Shared runtime policy: `coaching/COACH.md` (the policy is the implementation).
- Player-facing guidance: `README.md`.
- Development-only checks: `tests/test_contracts.py`; synthetic records: `tests/fixtures/workspaces/research/`.
- Synthetic wiki addresses use the reserved `example.invalid` domain, never a real wiki.
- No change to `templates/records/`, `adapters/codex/` or `adapters/claude/`. No new dependency, helper, script, MCP server or record migration.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the baseline and document the new fixtures.

- [X] T001 [P] Run `python3 -m unittest discover -s tests -p 'test_*.py' -v` against the unchanged suite in `tests/test_contracts.py`; record the command, the pass/fail counts and any pre-existing failure in a "Baseline" note under section 1 of `specs/003-mediawiki-api-research/quickstart.md`, marked as model-free evidence, not an observation of coaching behaviour.
- [X] T002 [P] Add a paragraph to `tests/fixtures/workspaces/README.md` describing the two new synthetic fixtures `research/wiki-api/` (a wiki source read through the official API, with page-level evidence carrying `page_title` and `revision_id`) and `research/wiki-api-failed/` (a later failure recorded in `mediawiki.last_failure` while the earlier success and its evidence are preserved). State that they use `example.invalid` addresses, contain no real wiki text, and that their validity cannot show whether Cid actually reads wikis politely or honestly.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define and validate the optional additive v1 fields every story writes. See `specs/003-mediawiki-api-research/data-model.md`.

**⚠️ CRITICAL**: No story work can begin until this phase is complete.

- [X] T003 Extend the `sources.json` and evidence bullets in "Portable JSON shapes" of `coaching/COACH.md`, keeping the existing compact voice. Source: optional `mediawiki: {api, robots, last_failure}` present only once Cid has probed or used a wiki's API; `api` is "null or an `https://` URL ending in `/api.php`"; `robots: {checked_at, status}` with status `allowed|disallowed|unreadable|absent`, informational only because robots are rechecked at first use each session; optional `last_failure: {at, kind, detail}` with kind `no_api|challenged|blocked|sign_in_required|rate_limited|lagged|robots_disallowed|error` and `detail` "a short plain-text reason, never a response body", describing only the most recent failure and removed by a later successful read; `api: null` is not re-probed unless conditions change; "No `mediawiki` field holds headers, cookies, tokens or page text." Evidence: optional `page_title` (canonical title after redirects) and `revision_id` (positive integer `revid`), "Required together with `page_title` when either is present"; wiki evidence uses the reader-facing page address as `locator` and never `integration_id`/`query`. Add one sentence to the closing paragraph of that section stating these fields are additive within v1 and need no migration.
- [X] T004 Add a `MediaWikiContractTests` class to `tests/test_contracts.py` that builds in-memory variants from `fixture_documents("research", "supported")` and checks them with `validate_document` / `check_snapshot`. Positive: the unchanged `supported` fixture still validates (records without the new fields stay valid); a variant whose source gains `mediawiki: {"api": "https://wiki.example.invalid/api.php", "robots": {"checked_at": <stamp>, "status": "unreadable"}}` and whose evidence gains `page_title` + `revision_id` validates; `api: null` validates. Negative (each must raise `ContractError`): `robots.status` outside `allowed disallowed unreadable absent`; `last_failure.kind` outside the eight listed kinds; `api` using `http://`; `api` not ending in `/api.php`; `revision_id` without `page_title`; `page_title` without `revision_id`; `revision_id` of `0`, `-1`, `True` or `"12"`; empty `page_title`; wiki evidence (with `page_title`) also carrying `integration_id`; and evidence whose `accessed_at` is later than `robots.checked_at` on a source whose `last_failure.kind` is `robots_disallowed` and `robots.status` is `disallowed`. Add one more positive case: a source whose `robots.status` is `allowed` with a later `checked_at`, `access_status` `accessible` and no `last_failure` (recovery after an earlier disallow), cited by evidence accessed after `checked_at`, validates. Run the class and confirm the negative cases fail before T005–T007 exist.
- [X] T005 In `validate_document` for `kind == "sources"` in `tests/test_contracts.py`, when `"mediawiki" in s`: require an object; `api` is `None` or a string starting with `https://` and ending with `/api.php`; if `robots` is present require `fields(robots, "checked_at status")`, `stamp(checked_at)` and `choice(status, "allowed disallowed unreadable absent")`; if `last_failure` is present require `fields(..., "at kind detail")`, `stamp(at)`, `choice(kind, "no_api challenged blocked sign_in_required rate_limited lagged robots_disallowed error")` and `string(detail)`. Leave unknown additive keys untouched; do not invent a length limit for `detail`.
- [X] T006 In `validate_document` for `kind == "knowledge"` evidence in `tests/test_contracts.py`, when either `page_title` or `revision_id` is present: require both; `string(page_title)`; `revision_id` is an `int`, not a `bool`, and `> 0`; and require `"integration_id" not in e` with the message "wiki evidence is not integration evidence".
- [X] T007 In the cross-record loop of `validate_workspace` in `tests/test_contracts.py`, after the existing "evidence access after recorded success" check: if the cited source has `mediawiki.last_failure.kind == "robots_disallowed"`, `mediawiki.robots.status == "disallowed"` and `mediawiki.robots.checked_at` is present, require the evidence `accessed_at` to be no later than `robots.checked_at`, with the message "evidence accessed after robots disallow". Run `python3 -m unittest tests/test_contracts.py -v` and confirm `MediaWikiContractTests` and all existing tests pass.

**Checkpoint**: The new fields are documented in the policy, validated when present, and every existing fixture still passes.

---

## Phase 3: User Story 1 - Coach from a challenge-protected wiki without pasting (Priority: P1) 🎯 MVP (with US2)

**Goal**: Cid finds a MediaWiki wiki's official API, searches it for a named need, reads only the pages that address it, and saves its own summaries citing page title, address and revision.

**Independent Test**: `research/wiki-api/` validates as a complete workspace. In ordinary use (not launched by an agent), coaching on a Fandom-hosted game answers a mechanics question from wiki pages Cid read itself, and the saved evidence shows page address, title and revision with no copied passages (quickstart section 3, Story 1).

- [X] T008 [P] [US1] Create the synthetic workspace `tests/fixtures/workspaces/research/wiki-api/` by copying the file set of `tests/fixtures/workspaces/research/supported/` (`.cid/workspace.json`, `games/synthetic-a/game.json`, `sources.json`, `integrations.json`, `knowledge/mechanics.json`, `playthroughs/run-1.json`). Replace the source with one wiki source: `locator` `https://wiki.example.invalid/wiki/`, `title` "Synthetic Wiki (MediaWiki)", `access_status` `accessible`, `quality_notes` including "Licence: CC BY-SA" and "read through the official API", and `mediawiki: {"api": "https://wiki.example.invalid/api.php", "robots": {"checked_at": <stamp ≤ last_attempt_at>, "status": "unreadable"}}`. Give the finding one evidence item with `locator` `https://wiki.example.invalid/wiki/Synthetic_Page`, `page_title` "Synthetic Page", `revision_id` `1073`, `accessed_at` ≤ the source's `last_success_at`, and a summary written in plain own words. Keep all statements synthetic, with no real game facts. Add `"wiki-api"` to the name tuple in `ResearchContractTests.test_complete_research_fixtures` in `tests/test_contracts.py`.
- [X] T009 [US1] Add a "MediaWiki wikis" subsection to `coaching/COACH.md` directly after the numbered research list in "Evidence before game facts", and add one pointer sentence to each of steps 2 and 4 without changing their order. Step 2: an indexed wiki with a working `mediawiki.api` is consulted through it, before any broad search (Constitution I). Step 4: when a newly discovered wiki's ordinary page fetch returns a challenge, sign-in wall or other unreadable response, read it through its official API; if an ordinary fetch works without any workaround, Cid may keep using it. In the subsection, write the request mechanism and etiquette from `research.md` R1–R4 and the contract's "Request rules": prefer the host shell's existing `curl` (one request per command, no loops, scripts, background jobs or saved files) with user agent `Cid-game-coach/1.0 (+https://github.com/hamdrew/cid)`, otherwise the host fetch tool with its default identity, otherwise the existing fallbacks; endpoint discovery (skip when `mediawiki.api` is saved; when it is saved as `null`, do not re-probe unless conditions changed: a fresh pass, a player request or a new address) probing only `https://<host>/api.php` then `https://<host>/w/api.php` with `action=query&meta=siteinfo&siprop=general|rightsinfo`, accepting only JSON whose `query.general.generator` starts with "MediaWiki", saving the endpoint and building reader addresses from `server` + `articlepath`; every request carries `format=json&formatversion=2&maxlag=5&assert=anon&errorformat=plaintext`; strictly one request in flight; read-only modules only (`query` with `siteinfo`, `search`, `info`; `parse`); never a browser-like user agent, cookies, login, tokens or write actions. Give the exact parameters, not full command lines or the research prose.
- [X] T010 [US1] Add page selection and reading to the "MediaWiki wikis" subsection of `coaching/COACH.md` (contract "Selecting and reading", `research.md` R6): one `list=search` per named need with game and topic words (`srlimit` ≤ 10, `srprop=snippet|size`); choose 1–3 results that address the need; read with `action=parse&page=<title>&prop=wikitext|revid&redirects=1`; for pages whose `size` exceeds about 30 KB request `prop=sections` and read only relevant `section=N`; use `prop=text` only when the wikitext is mostly templates whose values are needed; follow a redirect once; treat disambiguation pages as candidate titles chosen by need; a typical need costs one search plus one to three reads, and requests beyond about six need a new named need (the per-session robots check and endpoint probes are setup and do not count); never enumerate pages, follow links without a need or read a whole category. Spoiler-check search titles, snippets and page addresses before showing or saving any. Several wikis for one game are weighed by the existing source-selection criteria; API access does not make a wiki preferred.
- [X] T011 [US1] Add saving rules to the "MediaWiki wikis" subsection of `coaching/COACH.md` (contract "Saving", `research.md` R8–R9): the wiki is one source record whose `locator` is the reader-facing wiki address; existing per-page sources for the same wiki stay unchanged, their IDs are noted in the wiki source's `quality_notes`, and new API-read evidence cites the wiki-level source; on a successful read set `access_status` `accessible`, timestamps and `mediawiki.api`, remove any `mediawiki.last_failure`, and note the `rightsinfo` licence and "read through the official API" in `quality_notes`; findings and evidence summaries are Cid's own concise words, with short identifying labels (titles, item names, numbers) allowed and copied sentences or tables not; evidence cites the page address (optionally `#Section`) as `locator` plus `page_title` and `revision_id`; existing spoiler, applicability, conflict and version rules apply unchanged; pasted wiki text from the player is still accepted as before.
- [X] T012 [US1] Run `python3 -m unittest tests/test_contracts.py -v`; confirm `wiki-api` passes in `test_complete_research_fixtures` and nothing else regressed.

**Checkpoint**: The reading path, saving rules and the success fixture exist. Do not treat US1 as shippable until Phase 4 is complete.

---

## Phase 4: User Story 2 - Fail honestly and fall back (Priority: P1) 🎯 MVP (with US1)

**Goal**: Cid respects robots rules, stops on lag, rate limits, challenges and blocks, tells the player plainly in the same reply, records the failure while preserving earlier success, and continues with the existing research steps.

**Independent Test**: `research/wiki-api-failed/` validates, and the robots-disallow negative case from T004 is rejected. In ordinary use, a wiki whose API is missing or blocked produces a plain explanation, a fallback and a recorded failure without erasing an earlier success (quickstart section 3, Story 2).

- [X] T013 [P] [US2] Create `tests/fixtures/workspaces/research/wiki-api-failed/` from the `wiki-api` file set (T008). Change the wiki source to `access_status` `failed`, keep its earlier `last_success_at`, set a later `last_attempt_at`, and add `mediawiki.last_failure: {"at": <same as last_attempt_at>, "kind": "rate_limited", "detail": "API answered ratelimited with Retry-After 5"}`. Keep the earlier finding and its evidence (accessed at or before `last_success_at`) unchanged so the preserved success remains valid support. Add `"wiki-api-failed"` to the name tuple in `ResearchContractTests.test_complete_research_fixtures` in `tests/test_contracts.py`.
- [X] T014 [US2] Add the per-session robots precondition to the "MediaWiki wikis" subsection of `coaching/COACH.md` (contract "Preconditions", `research.md` R5): before the first API request to a wiki in a session, request `https://<host>/robots.txt` once; applicable tokens are `*`, `Cid-game-coach`, and the running host's user-initiated tokens (Claude Code: `Claude-User`, `Claude-Web`; Codex: `ChatGPT-User`, `Codex`); training and search-indexing tokens (`GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `Claude-SearchBot`, `anthropic-ai`, `Google-Extended`, `CCBot`) do not apply; match tokens case-insensitively, read the whole file, merge every group naming the same token including repeated `*` groups, and let the longest matching path rule win within the merged group; do not use the API if any applicable token disallows the API path or a `Content-Signal` sets `ai-input=no`, and then record `robots_disallowed`, set `robots.status` `disallowed` and tell the player; a challenge, 403, 5xx or timeout means unreadable and does not block use; a 404 means absent.
- [X] T015 [US2] Add the response-handling table to the "MediaWiki wikis" subsection of `coaching/COACH.md` (contract "Response handling", `research.md` R3): `error.code` `maxlag` (often with HTTP 200) → record `lagged`; `error.code` `ratelimited`, HTTP 429 or 503, or any other `Retry-After` → record `rate_limited`; either way stop for this need; a later need may retry once after at least `Retry-After` seconds (5 if none) have elapsed since the recorded failure, measured by elapsed time rather than sleeping; a second such response ends the wiki for the session. Stop the wiki for the session and record: a challenge page or other HTML instead of JSON → `challenged`; HTTP 401, `readapidenied` or an `assert` failure → `sign_in_required` and set `access_status` `requires_access`; HTTP 403 without a challenge page or a `blocked`-type error code → `blocked`. No other route is tried, including altered identification or ordinary-page scraping. Probe failure → record `no_api` with `api: null`. Other error or timeout → record `error` and fall back for this need.
- [X] T016 [US2] Add honest reporting, fallback and the never-list to the "MediaWiki wikis" subsection of `coaching/COACH.md`: every stop or failure is told to the player in the same reply in plain words (for example "the wiki's API asked me to slow down", "the wiki blocked automated reading", "the wiki's robots rules exclude automated readers like me"); research then continues with the remaining existing steps (other sources, broad search, asking the player); unread pages are never cited; a failure updates `access_status`, `last_attempt_at` and `mediawiki.last_failure` while keeping `last_success_at` and earlier evidence, and a later successful read removes `last_failure`; a host with no shell network and no usable fetch tool degrades to the existing fallbacks; and the contract's "Never" list (accounts, keys, tokens, cookies, stored credentials, HTML scraping of ordinary pages, challenge solving or circumvention, altered identity after a refusal, bulk or whole-wiki download, installing anything, claiming a read that did not happen).
- [X] T017 [US2] Run `python3 -m unittest tests/test_contracts.py -v`; confirm `wiki-api-failed` passes and the T004 robots-disallow case is still rejected.

**Checkpoint**: MVP complete. US1 + US2 cover FR-001 to FR-007 and FR-009 to FR-013.

---

## Phase 5: User Story 3 - Reuse wiki research without re-reading (Priority: P2)

**Goal**: Cid reuses adequate wiki findings with zero requests and, when a known page must be consulted again, checks revisions in one batched request and re-reads only changed pages.

**Independent Test**: The `wiki-api` fixture records `page_title` and `revision_id` on every wiki evidence item, which is what the revision check needs. In ordinary use, a fresh session asking about something already researched makes no wiki request, and a fresh pass checks revisions in one request and re-reads only changed pages (quickstart section 3, Story 3).

- [X] T018 [US3] Add the reuse rules to the "MediaWiki wikis" subsection of `coaching/COACH.md` (contract "Reuse", `research.md` R7): adequate saved findings mean zero wiki requests (existing step 1 rule); when known pages must be consulted again (a fresh pass, a version change, a conflict, or a new need on a known page), first send one batched `action=query&prop=info&titles=<A>|<B>|…` (up to 50 titles) and compare each `lastrevid` with the saved `revision_id`; read content only for pages whose revision changed or was never recorded; after a re-read, save the new `revision_id`, and route changed content through the existing conflict and version reassessment rules rather than silently overwriting findings.
- [X] T019 [US3] Add a test to `MediaWikiContractTests` in `tests/test_contracts.py` that loads `fixture_documents("research", "wiki-api")` and `fixture_documents("research", "wiki-api-failed")` and asserts every evidence item citing a source with a non-null `mediawiki.api` carries both `page_title` and `revision_id` (the data the batched revision check needs). Fix the fixtures if it fails, then run `python3 -m unittest tests/test_contracts.py -v`.

**Checkpoint**: All three stories are covered; FR-008 is now addressed.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T020 [P] Add a short note to the "Use it normally" section of `README.md`: Cid can read MediaWiki wikis (Fandom and others) through their official API when ordinary pages show a browser challenge; it reads only what a question needs, anonymously and politely, respects robots rules, saves its own summaries with page links, and says plainly when a wiki cannot be read. Nothing needs installing or configuring. Note that a host whose shell has no network access (Codex's default sandbox often blocks it) falls back to its fetch tool or to other sources, and the player may approve the host's usual network prompt.
- [X] T021 Align `coaching/COACH.md` with constitution v1.4.0 Principle I and review the wiki subsection. (a) Add one compact "Polite web access" paragraph to "Evidence before game facts", directly before the "MediaWiki wikis" subsection, that applies to every web read: read-only and anonymous, no accounts, keys, cookies or stored credentials; prefer a site's official read interface over working around unreadable pages; never get past a challenge, sign-in demand, block, paywall or refusal by any route (altered or browser-like identification, evasive mirrors, other scraping), since a refusal ends that route; honest identification where the host lets Cid set it; honour readable robots rules and AI-input content signals for the same token groups as the wiki rules; one request at a time per site, only for named needs, no crawling or bulk download; honour lag and retry signals; no re-fetching unchanged content; plainly report failed or refused access and fall back. Then shorten the "MediaWiki wikis" subsection so it refers to this paragraph instead of repeating it, keeping only wiki-specific parameters, tokens and the response table. (b) Review the result against every section and table row of `specs/003-mediawiki-api-research/contracts/mediawiki-research.md`, against FR-001 to FR-013 in `spec.md` and against Principle I, by reading rather than keyword tests; tighten wording to the existing COACH.md voice and remove research prose or full command lines. (c) Confirm the paragraph only adds restrictions to how sources are read: no research step, evidence order, stop condition or spoiler rule changes (FR-013).
- [X] T022 Run `python3 -m unittest discover -s tests -p 'test_*.py' -v`; record the command and result next to the T001 baseline in `specs/003-mediawiki-api-research/quickstart.md`, stating that it establishes record shape and fixture validity only and that conversational behaviour remains unobserved until ordinary use.
- [X] T023 Report the changed files (`coaching/COACH.md`, `README.md`, `tests/test_contracts.py`, the two fixtures, the fixtures README, `quickstart.md`, `tasks.md`) to the owner and leave everything uncommitted; ask before any `git commit`.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)**: none.
- **Foundational (Phase 2)**: after Setup; blocks all stories. T004 (tests) precedes T005–T007 (validators); T003 is independent of T004–T007 but edits `coaching/COACH.md`, so it precedes every later policy edit.
- **US1 (Phase 3)**: after Phase 2.
- **US2 (Phase 4)**: after Phase 2; its `coaching/COACH.md` edits (T014–T016) follow T009–T011 because they extend the same subsection. T013 needs T008's file set.
- **US3 (Phase 5)**: after T009 (the subsection must exist); otherwise independent of US2.
- **Polish (Phase 6)**: after all desired stories.

### Story dependencies

- US1 → US2 share one subsection; ship them together as the MVP.
- US3 depends only on the US1 subsection and the foundational `revision_id` field.

### Within each phase

- Tests before validators (T004 before T005–T007).
- Fixtures before the test run that lists them.
- `coaching/COACH.md` edits strictly in task order: T003 → T009 → T010 → T011 → T014 → T015 → T016 → T018.

## Parallel Opportunities

- Phase 1: T001 and T002.
- Phase 3: T008 (fixture) alongside T009–T011 (policy).
- Phase 4: T013 (fixture) alongside T014–T016 (policy).
- Phase 6: T020 (README) alongside T021 (polite-access paragraph and policy review).

### Parallel example: User Story 1

```text
Task: "T008 [P] [US1] Create tests/fixtures/workspaces/research/wiki-api/ …"
Task: "T009 [US1] Add the MediaWiki wikis subsection to coaching/COACH.md …"   (then T010, T011 in order)
```

### Parallel example: User Story 2

```text
Task: "T013 [P] [US2] Create tests/fixtures/workspaces/research/wiki-api-failed/ …"
Task: "T014 [US2] Add the robots precondition to coaching/COACH.md …"   (then T015, T016 in order)
```

## Implementation Strategy

### MVP (US1 + US2)

1. Phase 1 and Phase 2: fields documented and validated.
2. Phase 3 then Phase 4: the reading path plus its robots, stop, report and fallback rules.
3. Stop and validate: run the suite; the owner may observe Stories 1 and 2 in ordinary use.

### Incremental delivery

1. MVP as above.
2. Add US3 (revision reuse), rerun the suite, and optionally observe Story 3.
3. Polish: README note, contract review, final run, report and ask before committing.

## Notes

- Requirement coverage: FR-001 (T009), FR-002 (T010), FR-003/FR-004 (T009, T015, T016), FR-005 (T014), FR-006 (T009, T015), FR-007 (T009), FR-008 (T006, T018), FR-009 (T011), FR-010 (T005, T011, T013, T016), FR-011 (T016), FR-012 (T009, T016, T020), FR-013 (T003, T021; T021 also adds the general polite-access paragraph that FR-013 permits).
- No task makes live wiki requests. The optional manual `curl` check in quickstart section 2 is for the owner only.
- Leave all changes uncommitted pending explicit owner approval.
