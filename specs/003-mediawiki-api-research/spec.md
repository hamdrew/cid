# Feature Specification: Wiki research through the official MediaWiki API

**Feature Branch**: `main` (current Git branch; feature identifier: `003-mediawiki-api-research`)

**Created**: 2026-11-08

**Status**: Draft

**Input**: User description: "Wiki research through the official MediaWiki API.
Many game wikis (e.g. tap-wizard-2.fandom.com) put their normal pages behind a
browser challenge, so Cid's host fetch tool only receives the challenge page and
the player copies wiki text by hand. The same wikis' official API answers program
requests without a challenge. Cid should find and read relevant pages from a game's
MediaWiki wiki by itself, through that official API, choosing pages on demand,
read-only and anonymous, politely paced, without bypassing any challenge or block,
saving summaries with title and address rather than copied text, and falling back
honestly when the API is unavailable."

This feature extends the [local coach](../001-ai-game-coach/spec.md) and the
[bounded game understanding pass](../002-game-understanding/spec.md). It changes
only how Cid reads a wiki that runs MediaWiki (Fandom-hosted or independent).
Research order, evidence rules, spoiler protection, stop conditions and saved
record conventions stay as they are.

## User Scenarios & Testing *(mandatory)*

The observations below can guide ordinary use and optional feedback. They are not
a mandatory campaign, trial quota or scoring system. No development agent may
launch AI sessions, model APIs, automated players or graders for testing.
Deterministic, model-free checks of the policy text and of saved records remain
allowed; unobserved conversational behavior stays unverified.

### User Story 1 - Coach from a challenge-protected wiki without pasting (Priority: P1)

A player asks for help with a game whose main wiki shows a browser challenge to
Cid's ordinary page fetch. Cid recognizes that the wiki runs MediaWiki, uses the
wiki's official API to search it and read the few pages it needs, and coaches from
what it read. The player never has to copy wiki text into the conversation.

**Why this priority**: This is the problem the feature exists to solve; today the
player is the workaround.

**Independent Test**: During normal use, start or resume coaching for a game whose
wiki is Fandom-hosted. Observe whether Cid answers a mechanics question with
evidence from that wiki, and whether the saved finding names the wiki page title
and address it came from.

**Acceptance Scenarios**:

1. **Given** a game whose wiki returns a browser challenge to an ordinary page
   fetch, **When** Cid needs a fact that wiki is likely to cover, **Then** it reads
   the relevant page through the wiki's official API and uses it as accessed evidence.
2. **Given** a research need, **When** Cid uses the wiki, **Then** it searches the
   wiki for that need and reads only the pages that address it, not neighboring or
   linked pages without a named need.
3. **Given** a page read through the API, **When** Cid saves what it learned,
   **Then** the saved finding contains Cid's own concise summary and cites the
   page title and its normal reader-facing address; no stretch of page text is
   stored verbatim.
4. **Given** a successful API read, **When** Cid records source access, **Then**
   the source is marked accessible and notes that it was read through the official
   API, so later sessions do not mistake it for a failed or never-opened page.

---

### User Story 2 - Fail honestly and fall back (Priority: P1)

The wiki has no usable API, refuses anonymous reading, asks Cid to slow down or
stops answering. Cid says what happened in plain terms and continues with the
existing research steps instead of guessing or forcing access.

**Why this priority**: Unreliable access is normal; a wrong claim of access or an
attempt to push past a refusal would break the coach's evidence rules and the
wiki's terms.

**Independent Test**: During normal use, encounter or point Cid at a wiki whose
API is disabled or refusing. Observe the explanation, the fallback, and that the
saved source records the failure while preserving any earlier success.

**Acceptance Scenarios**:

1. **Given** a wiki whose API cannot be found or answers with an error, **When**
   Cid tries it, **Then** it tells the player the wiki could not be read this way
   and continues with the existing research steps (other sources, broad search,
   or asking the player).
2. **Given** a response that signals rate limiting, server lag or temporary
   refusal, **When** Cid receives it, **Then** it stops using that wiki for the
   current research need; a later need may try once more only after the advised
   delay has passed, and a second such response ends use of that wiki for the
   session.
3. **Given** a response that is a browser challenge, sign-in demand or block,
   **When** Cid receives it, **Then** it stops using that wiki for the session
   and makes no attempt to get past it by any other route.
4. **Given** the wiki's robots rules are readable and disallow the API for
   automated readers like Cid, **When** Cid considers using it, **Then** it does
   not use the API on that wiki and reports the restriction.
5. **Given** an earlier successful read and a later failure, **When** Cid updates
   the source record, **Then** the failure is recorded and the earlier success is
   preserved.

---

### User Story 3 - Reuse wiki research without re-reading (Priority: P2)

A player returns in a fresh conversation. Cid reuses findings already drawn from
the wiki and only re-reads a page when the wiki shows the page has changed since
Cid last read it, or when a new need requires a page Cid has not read.

**Why this priority**: Avoids needless load on volunteer-run wikis and repeated
research, building on the existing reuse rules.

**Independent Test**: Resume coaching on a game with saved wiki findings. Inspect
whether Cid asked the wiki only whether known pages changed, re-read none that
were unchanged, and recorded the page version it relied on.

**Acceptance Scenarios**:

1. **Given** a saved finding from a wiki page with a recorded page version,
   **When** the finding is needed again and the wiki reports the same version,
   **Then** Cid does not fetch the page content again.
2. **Given** the wiki reports a newer version of that page, **When** the
   finding is needed, **Then** Cid may re-read the page and reassesses affected
   findings using the existing conflict and version rules.
3. **Given** adequate saved findings for the current need, **When** Cid answers,
   **Then** it does not contact the wiki at all.

### Edge Cases

- A game has several wikis (e.g. Fandom and an independent wiki): Cid weighs them
  with the existing source-selection criteria; the API path does not make one
  wiki automatically preferred.
- The ordinary page fetch works for a wiki: Cid may use it as before; this
  feature does not force API use and does not change non-wiki research.
- A search on the wiki returns pages whose titles alone would reveal spoilers:
  existing spoiler protection applies to titles, snippets and addresses shown or saved.
- A page is a redirect or disambiguation page: Cid follows the wiki's own
  redirect once and treats disambiguation as a list of candidates, still choosing
  by need.
- A page is very long: Cid reads only the sections the need requires when the
  wiki allows section-level reading.
- The wiki's content licence is not the usual CC BY-SA: Cid still saves only its
  own summary with title and address, and notes the stated licence when visible.
- The host offers no way to identify Cid as an automated reader: Cid proceeds
  with the host's default identification and does not impersonate a browser.
- The player pastes wiki text anyway: Cid accepts it as before.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: When a game's wiki is likely to cover a research need and its
  ordinary pages are unreadable to Cid, Cid MUST attempt to read it through that
  wiki's official MediaWiki API, for Fandom-hosted and independent MediaWiki wikis alike.
- **FR-002**: Cid MUST choose pages on demand: search the wiki for a named need,
  then read only pages that address it. It MUST NOT enumerate, crawl or bulk-download
  a wiki or follow links without a named need.
- **FR-003**: Access MUST be read-only and anonymous. Cid MUST NOT create or use
  accounts, sign in, use keys or tokens, or store any credential.
- **FR-004**: When reading a wiki whose ordinary pages are unreadable, Cid MUST
  use only the wiki's official API. It MUST NOT work around unreadable pages by
  scraping ordinary page markup, and MUST NOT attempt to get past a browser
  challenge, sign-in demand, block or refusal by any route, including altered
  identification. An ordinary page fetch that works without any workaround stays
  allowed as before.
- **FR-005**: When the wiki's robots rules are readable, Cid MUST check them
  before first API use on that wiki in a session and MUST NOT use the API where
  they disallow it for Cid or where the site's published content signals refuse
  AI input. Unreadable robots rules MUST NOT block use by themselves.
- **FR-006**: Cid MUST send one request at a time to a wiki and MUST ask the wiki
  to refuse requests while its servers are lagged. A rate-limit, lag or
  temporary-refusal response MUST stop use of that wiki for the current need; a
  later need MAY retry once, only after at least the advised delay has elapsed;
  a second such response MUST stop use of that wiki for the session. A challenge,
  block or sign-in response MUST stop use of that wiki for the session.
- **FR-007**: Cid MUST identify itself as an automated reader with a descriptive
  identity where the host lets it set one, and MUST NOT present itself as a browser.
- **FR-008**: Cid MUST record which page version each wiki-derived finding relied
  on, and MUST NOT re-fetch a page's content when the wiki reports that version
  unchanged. It MAY ask the wiki for the current version cheaply before deciding.
- **FR-009**: Saved findings MUST contain Cid's own concise summaries and MUST cite
  the page title and its reader-facing address; saved records MUST NOT contain
  copied page text beyond short identifying labels such as the title.
- **FR-010**: Source records MUST distinguish reading through the official API from
  an ordinary fetch, and MUST record real failures (no API, challenged, blocked,
  sign-in required, rate limited, lagged, disallowed by robots rules, other error)
  separately while preserving earlier successes.
- **FR-011**: On any failure, Cid MUST tell the player plainly that the wiki could
  not be read and why, and MUST continue with the existing research order and
  fallbacks; it MUST NOT present unread content as evidence.
- **FR-012**: The feature MUST add nothing a player has to install or run: no
  helper program, extension, server or scripting runtime beyond the host's own
  existing tools.
- **FR-013**: This feature MUST NOT change the research steps for non-wiki
  sources, the existing evidence order, stop conditions, spoiler protection or
  record compatibility; any record addition MUST be optional and additive within
  the current version. The one exception is a general polite web-access rule
  that aligns all web reads with constitution Principle I (v1.4.0); it MAY only
  add restrictions on how sources are read, never new research steps.

### Key Entities *(include if feature involves data)*

- **Wiki source**: An indexed source that is a MediaWiki wiki, with its reader-facing
  address, the location of its official API when known, whether API reading works,
  robots status and the latest access outcome.
- **Wiki page reference**: The page title, reader-facing address and page version
  a finding relied on, enough to check later whether the page changed.
- **Access outcome**: A dated success or a specific failure (no API, challenged,
  blocked, sign-in required, rate limited, lagged, disallowed by robots rules,
  other error), preserved over time.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For a game with a Fandom-hosted wiki behind a browser challenge, the
  player can get a wiki-supported answer to a mechanics question in an ordinary
  session without pasting any wiki text.
- **SC-002**: Every finding drawn from a wiki names the page title and address;
  no saved record contains a copied passage of page text.
- **SC-003**: When the wiki cannot be read, the player is told so in the same
  reply and still receives the help the existing fallbacks allow; no reply claims
  wiki support that was not actually read.
- **SC-004**: In a fresh session with adequate saved wiki findings, no page whose
  recorded version is unchanged is fetched again.
- **SC-005**: A wiki research step touches only the pages tied to named needs —
  typically a search plus a handful of page reads — and never the bulk of a wiki.
- **SC-006**: Nothing in the delivered feature requires the player to install,
  configure or authenticate anything.

These are observable personal-use outcomes, not quotas or certification scores.
The owner may send bullet-point feedback and optionally share evidence for review
in the current conversation.

## Assumptions

- The host provides some way to make a plain web request (a fetch tool or a
  shell command already present). If it offers none that can reach the API, the
  feature degrades to the existing fallbacks.
- Fandom and most public MediaWiki wikis expose their official API anonymously
  for reading; this was observed for tap-wizard-2.fandom.com on 2026-11-08.
- Wiki content is commonly licensed CC BY-SA; saving short own-words summaries
  with title and address is consistent with that and with the existing
  "concise support, not full content" rule.
- "Robots rules" means the site's published robots file; Cid applies the
  rules that name it, its host's user-initiated agents, or all automated agents.
- The API is found by probing the two common locations (`/api.php`, `/w/api.php`).
  An independent wiki that serves its API elsewhere is recorded as having no
  usable API and handled by the existing fallbacks.
- The existing research order, source evaluation, spoiler and stop rules from
  the completed features remain the baseline.
- Constitution principles affected: I (evidence and polite, non-exhaustive
  access: FR-002/004/006/008/010/011), II (durable records and additive fields:
  FR-008/009/010/013), IV (spoilers in titles/snippets: edge cases), and MVP
  boundaries (no installed tool or service: FR-012).
