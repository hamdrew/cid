# Contract: Reading a MediaWiki wiki through its official API

Behaviour contract for `coaching/COACH.md`. It adds a way of reading a wiki,
reached from step 2 of *Evidence before game facts* for an indexed wiki and from
step 4 for a newly discovered one. It does not change the order of steps 1–5. Request details are in
[research.md](../research.md). Record fields are in [data-model.md](../data-model.md).

## When it applies

1. A research need remains after saved findings and the source index have been
   consulted, **and**
2. a relevant wiki is known or discovered whose ordinary page fetch returned a
   browser challenge, sign-in wall or other unreadable response, **or** an
   indexed wiki source already has a working `mediawiki.api`.

An indexed wiki with a working `mediawiki.api` is consulted through it in step 2,
before any broad search. A wiki first found in step 4 uses this path once its
ordinary pages prove unreadable. When an ordinary page fetch works without any
workaround, Cid MAY keep using it. Non-wiki research is unchanged.

## Preconditions per wiki, once per session

| Step | Outcome → action |
| --- | --- |
| Robots file | Applicable tokens: `*`, `Cid-game-coach`, and the host's user-initiated tokens (Claude Code: `Claude-User`, `Claude-Web`; Codex: `ChatGPT-User`, `Codex`). Training and search-indexing tokens do not apply. Read the whole file and merge every group for the same agent token, including repeated `*` groups. Within a group, the longest matching rule wins. If any applicable token is disallowed for the API path, or `ai-input=no` → do not use; record `robots_disallowed`; tell the player. Unreadable, absent or allowed → continue |
| Endpoint | Saved `mediawiki.api` → use it. Saved `api: null` → do not re-probe unless conditions changed (fresh pass, player request, new address); fall back. Otherwise probe `/api.php`, then `/w/api.php` with `meta=siteinfo`. Neither is MediaWiki JSON → record `no_api`; fall back |

The robots check and endpoint probes are per-session setup for a wiki and do not
count toward the per-need request budget below.

## Request rules (every request)

- Exactly one request in flight to a wiki. No parallel calls, loops, scripts or background jobs.
- Query string includes `format=json&formatversion=2&maxlag=5&assert=anon&errorformat=plaintext`.
- Read-only modules only: `query` (`siteinfo`, `search`, `info`) and `parse`. No
  `login`, tokens, cookies, `edit` or any write action.
- With a shell client, send the Cid user agent ([R4](../research.md#r4-identification)).
  Never imitate a browser.

## Response handling

| Response | Action |
| --- | --- |
| JSON success | Use it |
| `error.code` `maxlag` | Record `lagged` (not `rate_limited`). Stop, retry and session rules are as in the next row |
| `error.code` `ratelimited`, HTTP 429 or 503, or any other response with `Retry-After` | Record `rate_limited`. Stop for this need. A later need may retry **once** after ≥ `Retry-After` (default 5 s) has elapsed since the recorded failure. A second lag or rate-limit response ends the wiki for the session |
| Challenge page or other HTML instead of JSON | Stop the wiki for the session. Record `challenged`. **No other route is tried** |
| HTTP 401, `error.code` `readapidenied`, or an `assert` failure | Stop the wiki for the session. Record `sign_in_required`; set `access_status` `requires_access`. **No other route is tried** |
| HTTP 403 without a challenge page, or `error.code` `blocked` (or another `*blocked` code) | Stop the wiki for the session. Record `blocked`. **No other route is tried** |
| Other error or timeout | Record `error`. Fall back for this need |

A later successful read sets `access_status` `accessible`, updates
`last_success_at` and removes `mediawiki.last_failure`.

Every stop or failure is told to the player in the same reply in plain words,
such as "the wiki's API asked me to slow down" or "the wiki blocked automated
reading". Research then continues with the remaining existing steps. Unread
pages are never cited.

## Selecting and reading

1. One `list=search` per named need, using game and topic words.
2. Choose 1–3 results that address the need, judged by title, snippet and size.
   Search titles and snippets are spoiler-checked before any are shown.
3. Read with `action=parse … prop=wikitext|revid&redirects=1`. For long pages,
   list sections first and read only relevant sections.
4. A typical need costs one search plus one to three reads; requests beyond
   about six (excluding per-session setup) require a new named need. Never enumerate pages, follow links
   without a need, or read a whole category.

## Reuse

- Adequate saved findings → no request.
- Re-consulting known pages → one batched `prop=info` revision check. Content is
  read only for changed or unrecorded revisions.

## Saving

- Wiki source: one wiki-level source; accessible, endpoint, robots status and
  licence note. Existing per-page sources for the same wiki stay unchanged and are
  noted by ID in its `quality_notes`; new evidence cites the wiki-level source. Failures are
  recorded per the data model, with earlier success preserved.
- Findings: Cid's own concise statements. Evidence cites the page address,
  `page_title` and `revision_id`. No copied passages.
- Existing spoiler, applicability, conflict and version rules apply unchanged.

## Never

Accounts, keys, tokens, cookies, stored credentials, HTML scraping of ordinary
pages, challenge solving or circumvention, altered identity after a refusal,
bulk or whole-wiki download, installing anything, or claiming a read that did not happen.
