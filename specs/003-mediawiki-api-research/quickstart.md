# Quickstart: Validating MediaWiki API research

Validation has two kinds of evidence, kept separate. **Deterministic checks**
prove record shape and policy presence. **Ordinary use** shows conversational
behaviour. No AI sessions, model APIs or automated players may be launched to
test (constitution, development workflow).

## Prerequisites

- Repository checkout. Python 3.11+ for the development-only checks.
- For manual API checks: `curl`, network access, and patience between requests.

## 1. Deterministic checks (model-free)

**Baseline (T001, 2026-11-08)**: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
on the unchanged suite with Python 3.15.2: 39 tests, all passed, no pre-existing
failures. This is model-free evidence of record-contract validity only, not an
observation of coaching behaviour.

**After implementation (T022, 2026-11-08)**: the same command ran 45 tests, all
passed (after code-review fixes). That is the 39 existing tests plus 6 in `MediaWikiContractTests`, and
`wiki-api` and `wiki-api-failed` now appear in `test_complete_research_fixtures`.
This establishes record shape and fixture validity only. Whether Cid actually
reads wikis politely, reports failures honestly and reuses revisions stays
unobserved until ordinary use.

```sh
python3 -m unittest tests/test_contracts.py
```

Expected after implementation:

- Existing fixtures still pass, so records without `mediawiki`, `page_title` or
  `revision_id` stay valid.
- The new synthetic wiki fixtures under `tests/fixtures/workspaces/research/`
  pass: `wiki-api` has a wiki source with `mediawiki` and evidence with page title
  and revision; `wiki-api-failed` records a later failure while preserving the
  earlier success and its evidence.
- Mutations are rejected: a bad `robots.status` or `last_failure.kind`, a
  non-`https`/non-`api.php` endpoint, `revision_id` without `page_title`, a
  non-positive revision, and evidence accessed after a `robots_disallowed` check.
- A policy review, done by reading rather than keyword tests, confirms that
  `coaching/COACH.md` covers every row of the
  [contract](contracts/mediawiki-research.md). Data shapes are in
  [data-model.md](data-model.md).

## 2. Manual API sanity check (optional, by hand, serial)

Run one at a time, a few seconds apart:

```sh
UA='Cid-game-coach/1.0 (+https://github.com/hamdrew/cid)'
curl -sS -A "$UA" 'https://tap-wizard-2.fandom.com/api.php?action=query&meta=siteinfo&format=json&formatversion=2&maxlag=5&assert=anon'
curl -sS -A "$UA" 'https://tap-wizard-2.fandom.com/api.php?action=query&prop=info&titles=Mana%20Star&format=json&formatversion=2&maxlag=5&assert=anon'
```

Expected: JSON with `generator` "MediaWiki …" and a `lastrevid`. If either
returns an HTML challenge, the wiki now blocks API reads and Cid must fall back,
which is still correct behaviour.

## 3. Ordinary-use observations (optional, owner-driven)

Use the [contract](contracts/mediawiki-research.md) as the reference.

- **Story 1**: Coach on a Fandom-hosted game and ask a mechanics question. The
  answer should rely on wiki pages Cid read itself, and the saved evidence should
  show page address, title and revision with no copied passages.
- **Story 2**: Mention a wiki whose API is missing or blocked. Cid should say so
  plainly, fall back to other steps and record the failure without erasing an
  earlier success.
- **Story 3**: In a fresh session, ask about something already researched. Cid
  should make no wiki request. On a fresh pass, it should check revisions in one
  request and re-read only changed pages.

Send bullet-point feedback if anything is off. Unobserved behaviour stays unverified.

### Observed (2026-11-09, Claude Code session 2d842ea3, owner-shared)

- **Story 1, observed working:** on tap-wizard-2.fandom.com, robots.txt returned
  a challenge (recorded `unreadable`), and the `/api.php` probe succeeded. Requests
  were serial with the Cid user agent and the full parameter set. A batched
  revision check came first, then one search per need and 1–2 reads each, 18
  requests in total. One wiki-level source was saved with `mediawiki`, and all 15
  wiki evidence items have `page_title` + `revision_id`. Summaries were in Cid's
  own words, and the reply disclosed the request count and the wiki's 2022
  currency.
- **Issue found:** a per-page legacy source kept `last_success_at` later than
  `last_attempt_at`, because the "per-page sources stay unchanged" rule overrode
  the timestamp repair. Policy fixed to allow required record repairs.
- **Minor:** one extra request after truncating the probe output; section anchors
  kept trailing heading punctuation.
- **Not observed:** Stories 2 and 3 (failure paths, reuse in a fresh session).

