# Data Model: Wiki research through the official MediaWiki API

All changes are **optional, additive fields within JSON schema v1**. Existing
records stay valid without migration, and readers that do not know the fields
preserve them (existing additive-key rule). Decision rationale is in
[research.md](research.md#r8-record-representation).

## Wiki source (`games/<game-id>/sources.json` → `sources[]`)

The record is an existing source. The wiki as a whole is one source.

| Field | Use for a wiki |
| --- | --- |
| `locator` | Reader-facing wiki address, e.g. `https://tap-wizard-2.fandom.com/wiki/` |
| `title` | Spoiler-neutral wiki name, e.g. "Tap Wizard 2 Wiki (Fandom)" |
| `coverage` | Topic IDs the wiki has supported so far |
| `access_status` | Existing enum. `accessible` after a successful API read. `failed` after no API, a rate limit, a challenge or a block. `requires_access` when the API demands sign-in. Robots disallow is recorded as `failed` with that kind |
| `last_attempt_at` / `last_success_at` | Existing semantics. A later failure never clears an earlier success |
| `quality_notes` | Existing evaluation notes plus the licence from `rightsinfo` (e.g. "Licence: CC BY-SA") |
| **`mediawiki`** *(new, optional)* | Present only when Cid has probed or used the API |

### `mediawiki` object

| Field | Type | Rule |
| --- | --- | --- |
| `api` | string or null | Verified endpoint URL (`…/api.php` or `…/w/api.php`). `null` when no endpoint answered as MediaWiki |
| `robots` | `{checked_at, status}` | `status` ∈ `allowed` \| `disallowed` \| `unreadable` \| `absent`. It is informational: Cid rechecks at first use in each session |
| `last_failure` | object, optional | `{at, kind, detail}`. `kind` ∈ `no_api` \| `challenged` \| `blocked` \| `sign_in_required` \| `rate_limited` \| `lagged` \| `robots_disallowed` \| `error`. `detail` is a short plain-text reason, never a response body. It describes the most recent failure only: a later successful API read removes it, and the earlier success is kept in `last_success_at` |

Validation (when `mediawiki` is present):

- `api` is null or an `https://` URL ending in `/api.php`.
- `robots.checked_at` and `last_failure.at` are UTC stamps. The enums are as listed.
- A source with `last_failure.kind` of `robots_disallowed` and `robots.status`
  of `disallowed` must not be cited by evidence accessed after `robots.checked_at`.
- No `mediawiki` field holds headers, cookies, tokens or page text.

## Wiki evidence (`knowledge/<topic-id>.json` → `findings[].evidence[]`)

| Field | Use for a wiki read |
| --- | --- |
| `source_id` | The wiki source |
| `locator` | Reader-facing page address built from `articlepath`, e.g. `https://tap-wizard-2.fandom.com/wiki/Mana_Star`, with an optional `#Section` |
| `accessed_at` | Time of the API read. Must be ≤ the source's `last_success_at` (existing rule) |
| `summary` | Cid's own concise summary of what the page supports. No copied passages |
| **`page_title`** *(new, optional)* | Canonical title after redirects, used to batch revision checks |
| **`revision_id`** *(new, optional)* | Positive integer `revid` read. Required together with `page_title` when either is present |

No `integration_id` or `query` is used for wiki evidence. Those remain for real
integrations ([research R8](research.md#r8-record-representation)).

## State transitions (wiki source)

```text
(not indexed) ──discovered in search──▶ never_accessed
never_accessed / failed ──API read ok──▶ accessible  (mediawiki.api set; last_success_at)
accessible ──later failure──▶ failed                 (last_success_at kept; last_failure set)
any ──robots disallow──▶ failed (kind robots_disallowed; API not used)
any ──sign-in demanded──▶ requires_access
failed / requires_access ──later API read ok──▶ accessible (last_failure removed)
```

`api: null` (kind `no_api`) is not re-probed in later sessions unless conditions
change: a fresh pass, a player request, or a new reader address for the wiki.
This follows the existing rule that a failed attempt is repeated only after the
need or access conditions change.

A game may already index individual pages of the same wiki as separate sources
from earlier step-4 discovery. They stay valid and unchanged. API reads use one
wiki-level source; Cid notes the older page sources' IDs in the wiki source's
`quality_notes` and cites the wiki-level source for new API-read evidence, so
access status lives in one place without migrating old records.

Session-only state, which is not persisted: whether robots were checked this
session, whether the wiki is stopped for the session after a challenge, block or
second lag, and the time of the last lag response used to space a retry.

## Relationship to existing entities

- A **wiki page reference** (spec) is the evidence `locator` + `page_title` + `revision_id`.
- An **access outcome** (spec) is the source's `access_status`, timestamps and `mediawiki.last_failure`.
- Findings, overview, spoiler metadata, applicability and the playthrough
  records are unchanged.
