# Quickstart: Validating MediaWiki API research

Validation has two kinds of evidence, kept separate. **Deterministic checks**
prove record shape and policy presence. **Ordinary use** shows conversational
behaviour. No AI sessions, model APIs or automated players may be launched to
test (constitution, development workflow).

## Prerequisites

- Repository checkout. Python 3.11+ for the development-only checks.
- For manual API checks: `curl`, network access, and patience between requests.

## 1. Deterministic checks (model-free)

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
