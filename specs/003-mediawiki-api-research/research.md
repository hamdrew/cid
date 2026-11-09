# Research: Wiki research through the official MediaWiki API

**Date**: 2026-11-08 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

Evidence came from read-only repository inspection, MediaWiki Action API
documentation (mediawiki.org, via Context7) and a small number of manual,
serial, anonymous requests made during planning with a descriptive user agent
and `maxlag=5`. No AI tooling was launched to test behaviour.

## Live observations (2026-11-08)

| Request | Result |
| --- | --- |
| `tap-wizard-2.fandom.com/robots.txt` | HTTP 403, Cloudflare "Just a moment..." challenge page, so the robots file is **unreadable** |
| `…/api.php?action=query&meta=siteinfo&siprop=general\|rightsinfo` | 200 JSON; `generator` "MediaWiki 1.43.10", `articlepath` `/wiki/$1`, rights "CC-BY-SA" |
| `…/api.php?action=query&list=search&srsearch=mana` | 200 JSON; titles, page IDs, sizes and snippets |
| `…/api.php?action=query&prop=info&titles=Mana Star\|Nonexistent…` | 200 JSON; `lastrevid` 1073 and `length`; missing page flagged `missing:true` |
| `…/api.php?action=parse&page=Mana Star&prop=wikitext\|revid` | 200 JSON; 1.7 KB wikitext, `revid` 1073 |
| `…/api.php?action=query&prop=extracts` | Unrecognized: TextExtracts is **not installed** on Fandom |
| `…/api.php?…&maxlag=-1` (forced lag) | **HTTP 200** with JSON `error.code = "maxlag"` and header `Retry-After: 5` |
| `terraria.wiki.gg/robots.txt` | 200. Contains two `User-agent: *` groups. Cloudflare's group has `Allow: /` with `Content-Signal: search=yes,ai-train=no,use=reference`. wiki.gg's own group disallows `/index.php`, `/api.php` and `/rest.php`, including each language prefix. Named groups (`Claude-Web`, `anthropic-ai`, `ClaudeBot`, `GPTBot` and others) have `Disallow: /` |
| `terraria.wiki.gg/api.php?…meta=siteinfo` | 200 JSON, MediaWiki 1.43.6. The server answered, but robots rules are a request, not technical enforcement, so this does not grant permission |

## Decisions

### R1. How Cid sends a request

- **Decision**: Use a command-line HTTP client the host shell already provides
  (`curl` ships with macOS, most Linux and Windows 10+) when the host allows shell
  commands with network access. Make one request per command, with no loops,
  scripts, background jobs or saved files outside the workspace. Otherwise use the
  host's fetch tool on the same API URL. If neither can reach the API, use the
  existing fallbacks.
- **Rationale**: With the shell client Cid can set a descriptive user agent
  (FR-007), see the HTTP status and `Retry-After` (FR-006), and read exact JSON.
  Players install nothing (FR-012), and the host's normal permission prompts still
  apply. A fetch tool usually cannot set headers and may summarise the response,
  but it is still an official-API read.
- **Alternatives considered**: A bundled script or Python helper is excluded by
  the non-goals. An MCP server is also excluded. Using only the fetch tool would
  lose identification and back-off signals where a shell is available. Codex's
  default sandbox often blocks shell network access, so there the fetch or search
  tool or the fallback applies. This is recorded per host, not assumed.

### R2. Finding the API endpoint

- **Decision**: From a wiki's reader address, probe at most two candidates in
  order: `https://<host>/api.php` (Fandom, wiki.gg and most hosted wikis), then
  `https://<host>/w/api.php` (Wikimedia-style). The probe is
  `action=query&meta=siteinfo&siprop=general|rightsinfo`. Accept an endpoint only
  if it returns JSON with `query.general.generator` starting with "MediaWiki". Use
  `articlepath`/`server` to build reader addresses and `rightsinfo` to note the
  licence. Save the working endpoint so later sessions skip the probe. Save
  `api: null` when neither answers, and do not re-probe in later sessions unless
  conditions change (fresh pass, player request, new address). An independent
  wiki serving its API elsewhere is therefore treated as having no usable API.
- **Rationale**: Ordinary page HTML, which advertises `EditURI`, is exactly what
  the challenge hides. Two cheap probes cover the common layouts. A challenge or
  HTML response is not an API.
- **Alternatives considered**: Parsing a page's `<link rel="EditURI">` needs the
  challenged HTML. Guessing more paths would turn into probing.

### R3. Request etiquette

- **Decision**: Every API request carries `format=json&formatversion=2&maxlag=5&assert=anon&errorformat=plaintext`.
  Cid makes requests strictly one at a time and batches titles where the API
  allows it (`prop=info` takes up to 50). Treat as **lag or rate-limit**: an
  `error.code` of `maxlag` or `ratelimited` (both can arrive with HTTP 200), HTTP
  429 or 503, or any `Retry-After`. On that, stop for the current need. A later
  need may retry once, after at least `Retry-After` seconds (5 if none was given)
  have passed since the recorded failure. A second such response ends use of that
  wiki for the session. Treat as **stop for the session**: a challenge or HTML
  page, HTTP 401 or 403, `assert` failure, or a block error (`blocked`,
  `readapidenied`). Recorded kinds: `maxlag` → `lagged`; `ratelimited`, 429,
  503 or other `Retry-After` → `rate_limited`; challenge or HTML → `challenged`;
  401, `readapidenied` or `assert` failure → `sign_in_required` (source becomes
  `requires_access`); other 403 or `blocked` → `blocked`. A later successful read
  removes `last_failure` and keeps the earlier `last_success_at` history.
- **Rationale**: These follow MediaWiki's API etiquette: serial requests,
  `maxlag`, honouring `Retry-After`, and anonymous reads asserted with
  `assert=anon`. Hosts block foreground sleeping, so waiting is measured by
  elapsed time between needs rather than by sleeping. This meets FR-006 without
  busy-waiting.
- **Alternatives considered**: Retrying immediately within the same command
  could hammer a lagged server. `curl --retry` honours `Retry-After` only for
  HTTP errors, and maxlag arrives as HTTP 200.

### R4. Identification

- **Decision**: With a shell client, send the user agent
  `Cid-game-coach/1.0 (+https://github.com/hamdrew/cid)`, following the
  name/version-plus-contact form of Wikimedia's user-agent policy.
  Never send a browser-like user agent, cookies or credentials. With a fetch
  tool, accept the host's default identification.
- **Rationale**: FR-007 asks for this, and MediaWiki etiquette asks for a
  descriptive agent with a way to reach the operator. The public project
  repository serves as the contact address. The player's email or other personal
  details must not be used as contact information.

### R5. Robots rules

- **Decision**: Before the first API request to a wiki in a session, request
  `https://<host>/robots.txt` once. If it is readable (HTTP 200, plain text),
  apply the groups for `*`, for `Cid-game-coach`, and for the running host's
  **user-initiated** agent tokens:
  - Claude Code: `Claude-User` and `Claude-Web` (the latter is the older Anthropic
    user-fetch token, still named by many sites).
  - Codex: `ChatGPT-User`, OpenAI's only documented user-initiated token
    (developers.openai.com/api/docs/bots, read 2026-11-08), plus `Codex` if a
    site names it. OpenAI documents no Codex token, so this only ever adds
    restrictions.

  Robots token matching is case-insensitive. Following RFC 9309, groups naming the same
  agent token are merged, and within a group the longest matching path rule
  wins. Cid evaluates each applicable token this way. It must not use the API if
  any applicable evaluation disallows the API path, or if `Content-Signal` sets
  `ai-input=no`. Groups for training-only crawlers do not
  apply, because Cid neither trains nor builds an index. Examples are `GPTBot`,
  `ClaudeBot`, `anthropic-ai`, `Google-Extended` and `CCBot`. A challenge,
  403, 5xx or timeout means **unreadable**, which does not block use (spec
  FR-005). A 404 means no rules.
- **Rationale**: Cid is a user-directed, low-volume reader, closest to the
  hosts' "user" fetchers. Honouring those groups is the conservative honest
  reading. Ignoring a site's explicit reservation for the very agent class Cid
  belongs to would contradict the ethical requirements.
- **Consequence observed**: on terraria.wiki.gg, wiki.gg's own `*` group has
  `Disallow: /api.php`. That 8-character rule beats Cloudflare's `Allow: /`, so
  the API is off-limits to **every** automated agent, under either reading. Cid
  falls back to other sources there. The `Claude-Web` `Disallow: /` group
  disallows it again for Claude Code. Merging the two `*` groups is essential:
  reading only the first `*` group would have wrongly allowed the API.
- **Owner decision (2026-11-08)**: keep the strict reading. The host's
  user-initiated tokens above apply in addition to `*` and Cid's own token. This
  is deliberately stricter than OpenAI's own statement that robots rules "may
  not apply" to user-initiated `ChatGPT-User` fetches. Training- and
  search-indexing tokens (`GPTBot`, `OAI-SearchBot`, `ClaudeBot`,
  `Claude-SearchBot`, `anthropic-ai`) do not apply.
- **Alternatives considered**: Honouring every named AI group was rejected: it
  would include training crawlers and over-block. Honouring only `*` was rejected
  because it would ignore an explicit reservation aimed at user agents.

### R6. Choosing and reading pages

- **Decision**: For a named need, run one `list=search` (`srlimit` ≤ 10,
  `srprop=snippet|size`) with game and topic words. Choose the 1–3 results that
  address the need. Read each with
  `action=parse&page=<title>&prop=wikitext|revid&redirects=1`. If a page's
  `size` exceeds about 30 KB, first request `prop=sections`, then read only the
  relevant `section=N`. Read a page's rendered text (`prop=text`) only when its
  wikitext is mostly templates whose values are needed. Follow a redirect once
  via `redirects=1`. Treat a disambiguation page as candidate titles, still
  chosen by need. A typical need costs one search plus one to three reads.
  Requests beyond about six need a new named need. The per-session robots check
  and endpoint probes are setup and do not count toward this budget.
- **Rationale**: Wikitext is compact and keeps infobox values. TextExtracts is
  absent on Fandom. Section reads limit load on long pages. The budget makes
  FR-002 and SC-005 concrete without a quota.
- **Alternatives considered**: `prop=extracts` is not available on Fandom.
  `list=allpages` or link-following would be crawling. Full HTML is larger.

### R7. Revision reuse

- **Decision**: Each wiki-derived evidence item records the page title and the
  `revid` that was read. Ordinary reuse of adequate findings makes **zero**
  requests (existing rule). When a page must be consulted again, for a fresh
  pass, a version change, a conflict or a new need on a known page, Cid first
  sends a single batched `prop=info&titles=…` and compares `lastrevid`. It
  fetches content only for pages whose revision changed or was never recorded.
- **Rationale**: This satisfies FR-008 and SC-004 with one cheap request for many pages.
- **Alternatives considered**: Re-parsing every page on a fresh pass contradicts
  the requirement. `If-Modified-Since` caching is unreliable across hosts and
  fetch tools.

### R8. Record representation

- **Decision**: Model each wiki as **one source record**. Its `locator` is the
  reader-facing wiki address, and it has an optional additive `mediawiki` object
  holding the endpoint, robots status and latest specific failure. Wiki evidence
  keeps the existing `{source_id,locator,accessed_at,summary}`, with the page
  address as `locator`, plus optional additive `page_title` and `revision_id`.
  Do **not** model the API as an integration. Details are in
  [data-model.md](data-model.md).
- **Rationale**: Existing validation requires integration evidence to match an
  observation's single `last_query` (`tests/test_contracts.py` lines 374–380).
  Many page reads cannot each match it. A source with an access-route marker fits
  the evidence ladder: the wiki is a source, and the API is how it is read. It
  also keeps every existing record valid. Constitution II permits documented
  additive optional fields.
- **Alternatives considered**: An integration per wiki breaks evidence matching
  or needs a schema change. A source per page would bloat the index and duplicate
  wiki-level status. Existing per-page sources stay valid and need no migration:
  Cid adds one wiki-level source for API reads, notes the older page sources' IDs
  in its `quality_notes`, and cites the wiki-level source for new evidence.

### R9. Saving content

- **Decision**: Use the existing finding format. `statement` and evidence
  `summary` are Cid's own concise words. Short identifying labels (title, item
  names, numbers) are allowed. Copied sentences or tables are not. Record the
  licence from `rightsinfo` in the source's `quality_notes`.
- **Rationale**: This satisfies FR-009 and is consistent with CC BY-SA
  attribution (title and address) and the existing "concise support, not full
  fetched content" rule.

### R10. Where the behaviour lives

- **Decision**: Add a "MediaWiki wikis" subsection to `coaching/COACH.md` under
  *Evidence before game facts*, reached from step 2 for an indexed wiki with a
  working `mediawiki.api` (before any broad search, as Constitution I requires) and
  from step 4 when a newly discovered wiki's ordinary pages are unreadable. Extend the
  portable-shapes section with the optional fields. Extend
  `tests/test_contracts.py` to validate the optional fields when present and add a
  synthetic fixture. Add a README note.
- **Rationale**: The policy is the implementation (MVP boundary). The
  deterministic checks cover record shape. Behaviour remains an ordinary-use
  observation.
