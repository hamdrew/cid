# Research: Cid local coaching MVP

**Date**: 2026-11-07 · **Feature**: [spec.md](spec.md)

Research combines the repository specification and constitution, independent research
of host setup and record/validation design, current official documentation, and local
CLI help. There is no existing product implementation to preserve. Decisions below
are planning choices, not claims of measured product behavior.

## 1. Delivery boundary

- **Decision**: Ship shared Markdown coaching instructions, two small host adapters,
  portable JSON record templates, setup documentation, and development-only tests.
  Do not introduce a companion executable, service, model API, or mandatory plugin.
- **Rationale**: The hosts already supply conversation and file/research tools. The
  specification and constitution explicitly require this local delivery boundary.
- **Alternatives considered**: A Python/Node companion could enforce writes but adds
  installation and runtime dependencies without a demonstrated MVP need. A hosted
  application contradicts the scope. Host-specific skill packages can be considered
  later, but are unnecessary for normal-language coaching in a selected workspace.

## 2. Host loading and capability discovery

- **Decision**: Install a short workspace-root `AGENTS.md` directing the host to read
  `.cid/COACH.md` and `.cid/workspace.json`. Install `CLAUDE.md` with `@AGENTS.md`.
  Launch from the workspace root. Keep one canonical coaching body in
  `coaching/COACH.md`, copied into the player's workspace during setup.
- **Rationale**: Codex discovers project instructions at startup, with nearer
  overrides and size limits. A small bootstrap explicitly reads the shared body
  rather than depending on Markdown links acting as imports. See the
  [official AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
  Claude documents relative imports and endorses `@AGENTS.md` for sharing instructions;
  this avoids depending on conditional native AGENTS discovery. See
  [Claude memory documentation](https://code.claude.com/docs/en/memory).
- **Alternatives considered**: Duplicated policy in both adapters drifts. Global
  installation affects unrelated workspaces. Launch-time system-prompt flags impose
  repeated setup and differ between hosts. Host conversation history and automatic
  memory cannot replace the required shared workspace records.
- **Capability rule**: Discover available local write, search, fetch, and integration
  tools in the running session. Permission, provider, and configuration differences
  can make them unavailable. A denied operation is not a successful read or save.
  [Claude tools reference](https://code.claude.com/docs/en/tools-reference) and
  [permissions documentation](https://code.claude.com/docs/en/permissions) describe
  these distinctions. Instructions guide behavior; observed tests must establish
  adherence, persistence, and spoiler protection.
- **Local baseline**: Read-only inspection found `codex-cli 0.167.0` and Claude Code
  `2.1.319`. These are inspected versions, not proven minimum supported versions.
  `codex --help` confirms `--cd`, workspace-write mode, and live `--search`;
  [official CLI documentation](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
  provides the corresponding reference. Certification records must name actual
  tested versions instead of promising compatibility with every release.
- **Refresh evidence**: Independent read-only checks again observed the same CLI
  versions and launch flags. The Codex validation command explicitly selects
  `--ask-for-approval on-request`, rather than depending on inherited configuration.
  Claude's local help identifies `--bare` and `--safe-mode` as instruction-loading
  limitations; managed-only settings or `claudeMdExcludes` can also prevent the
  shared policy from being included. Do not change a player's configuration
  automatically to work around this: observe policy loading or report incompatible
  setup. The linked host instruction documentation remains the source of truth.
- **Research capability boundary**: Codex's `--search` enables hosted search, not
  arbitrary network access for shell commands; see the [official search guide](https://learn.chatgpt.com/docs/search).
  Claude search results do not by themselves establish page contents, and a fetch
  extraction can omit information; absence from an extraction is not proof that
  the source contains no such fact. Use the
  [tools reference](https://code.claude.com/docs/en/tools-reference) when interpreting
  actual research traces.

## 3. Authoritative records

- **Decision**: Use UTF-8 JSON for structured state and researched findings; use
  Markdown for coaching instructions, setup, and human validation procedures.
  Keep workspace defaults in `.cid/workspace.json`; each game has its own directory,
  source/integration indexes, topic files, and separate playthrough files.
- **Rationale**: Plain files are portable, reviewable, and editable by both hosts.
  JSON has unambiguous nulls, booleans, IDs, and dependency lists, and needs no YAML
  parser. One playthrough file holds both state and dependent plans so a correction
  does not require a multi-file transaction. Knowledge is divided by relevant topic
  to avoid reading every game's accumulated material on each turn.
- **Alternatives considered**: All-Markdown state is easy to read but harder to check
  consistently for provenance and references. YAML frontmatter adds parsing rules.
  SQLite adds an access layer and is less convenient for direct assistant edits.
  A transcript/event store retains unnecessary detail and increases resumption cost.
- **Compatibility**: Every JSON document has `schema_version: 1`. Unknown schema
  versions are read conservatively and never silently rewritten. No migration
  engine is needed for the initial format.

## 4. Persistence and interruption recovery

- **Decision**: Save meaningful updates before moving past the relevant exchange.
  Read the current file, prepare a complete same-directory temporary replacement,
  check its contents, replace the target using available local tools, and read back
  the target before treating the update as persisted. A revision guards against
  overwriting unexpectedly changed content; simultaneous editing remains excluded.
- **Rationale**: This reduces partial-file risk without adding a runtime. It is a
  host workflow, not a promise of database transactions or crash-proof storage.
  Publish referenced records before indexes/referrers; a failed index update must
  not undo a successfully saved player correction. Unregistered records and leftover
  temporary files require reconciliation, not silent deletion or invented state.
- **Alternatives considered**: Direct partial edits risk malformed state after
  interruption. Multi-file transactions, locks, and background sync exceed the
  sequential-use scope. Git commits are neither required persistence nor automatic.
- **Failure behavior**: Identify the specific unsaved update. Continue with qualified
  in-session context, but never claim a fresh session will have an unsaved change.

## 5. Correctable assumptions and preference scope

- **Decision**: Store reported and assumed entries with stable IDs and explicit
  provenance. Store proposed plans separately. Both entries and plans may reference
  prerequisite entries, plans, or findings. Corrections supersede the affected
  entry and mark its transitive dependents for review in the same playthrough save.
- **Rationale**: This meets FR-016–FR-019 without a full game-state simulator. A
  recommendation can imply an attempted action under enabled follow-through, never
  victory, reward acquisition, or other uncertain success. Alternatives stay proposals.
- **Alternatives considered**: Unlabelled progress silently turns guesses into facts.
  Rechecking only a direct dependency misses assumption chains. Event sourcing and
  a separate graph database add no necessary capability for this small record set.
- **Preference rule**: Resolve explicit playthrough overrides, then game overrides,
  then workspace choices, then defaults. Hints is the spoiler default; follow-through
  remains unset/disabled until explicitly enabled. Changing a narrower choice must
  not overwrite the workspace default.
  Conversely, an unscoped change updates the workspace choice and, if necessary,
  supersedes a conflicting override for the active playthrough so subsequent advice
  honors it. Other contexts retain their scoped choices; an explicit default-only
  request preserves the current override. Disclose partial saves across these files.
- **Spoiler boundary rule**: Assumed follow-through is evidence of neither a known
  outcome nor player knowledge. Only current reported knowledge can establish the
  progress-based disclosure boundary; explicit permission authorizes only its
  requested disclosure. This connects FR-016–FR-019 to FR-025–FR-026 without adding
  a state simulator or requiring repeated confirmation of ordinary assumptions.

## 6. Evidence, source visibility, and spoilers

- **Decision**: Apply the research ladder exactly: applicable local findings → saved
  source index and relevant indexed material → relevant available integrations →
  broad search if still needed. Stop once sufficient applicable evidence is found.
  Store concise evidence summaries, access times, links/locators, applicability,
  and source-quality assessments. Separate discovery, accessibility, and query success.
- **Rationale**: This implements FR-005–FR-011 and constitution I. Search snippets,
  model familiarity, or discovering an integration do not prove a factual claim.
  Conflicts and version changes reopen the affected findings and advice.
- **Alternatives considered**: Search-first repeats work; bulk scraping violates scope;
  a fixed source-type ranking ignores specificity, maintenance, and version fit.
- **Visibility**: Keep supporting links in records and show them on request, subject
  to spoiler filtering. Higher-priority host instructions may constrain citation
  display; document unsolicited citations as failed FR-009 compatibility, or an
  unobserved path as untested, rather than silently
  overriding host policy or claiming full compatibility.
- **Citation evidence limit**: The [hosted web-search guide](https://developers.openai.com/api/docs/guides/tools-web-search)
  requires visible citations for search-derived information in that API. This does
  not prove that a particular CLI configuration behaves identically, nor establish
  a supported citation-suppression setting. Keep FR-009 unchanged and observe actual
  CLI output during acceptance. Do not introduce a model API to evade host policy.
- **Constitution interpretation**: Principle IV specifies default Hints behavior and
  does not explicitly prohibit a scoped express request. FR-025 and the recorded
  clarification define that exception: provide only the specifically requested
  spoiler, retain Hints, and protect subsequent answers. Strict still requires
  permission before crossing the known boundary. This is a documented interpretation
  of default behavior, not an amendment or permission to reveal unrelated spoilers.

## 7. Personal use and feedback

- **Decision**: Keep the standard-library record/template checks; use the owner's
  normal play and bullet-point feedback to guide behavioral improvements.
- **Rationale**: This is a personal tool. Trial quotas, a host/game matrix, ratings
  and recruited participants add overhead without helping the owner request a tweak.
- **Optional exploration**: Fresh-session memory, a corrected assumption/goal,
  preference persistence and separate runs are useful checks when convenient.
  They are not required gates. See the [README](../../README.md#optional-checks).
- **Evidence review**: When explicitly requested, review supplied transcripts and a
  test workspace in the current conversation. Separate observed behavior from
  uncertainty. Do not launch AI sessions, model APIs, test agents or graders.
- **Alternative retired**: The original formal acceptance campaign and result
  matrices are archived outside the active documentation. Earlier observations do
  not become passes merely because the process is lighter.

## 8. Record minimization and ownership

Save meaningful updates in the exchange that handles them, verify the actual target,
and disclose failed/unconfirmed saves. Keep finding derivations and progress/plan
references acyclic. Strict permission and specific Hints requests remain scoped to
the requested answer, not a lasting preference or a completed milestone.

Player records contain concise coaching notes and referenced provenance, not full
transcripts, credentials or integration datasets. The owner may separately choose
what to share for feedback. Local records do not imply on-device inference; host
processing still applies. No new validator runtime, transaction service, telemetry,
sync, retention or deletion service is introduced.

## Current governance

[Constitution v1.2.0](../../.specify/memory/constitution.md) and the owner's approved
lightweight workflow supersede the previous testing campaign. Core coaching
principles, the record format and the delivery boundary remain unchanged. The
original ratification-date TODO is preserved. Ordinary use and feedback do not
certify behavior that has not been observed.
