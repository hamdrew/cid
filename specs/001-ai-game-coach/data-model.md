# Data model: Portable coaching records

**Format**: v1 · **Related**: [workspace contract](contracts/workspace.md),
[coaching contract](contracts/coaching.md)

These are record contracts to implement, not a database schema or an exhaustive
game simulator. Field names below are the v1 design. Optional game-specific details
are omitted until useful; unknown values are never invented to fill a template.

## Common rules

- Each JSON document is an object containing `schema_version` (integer `1`),
  `revision` (nonnegative integer), and `updated_at` (UTC timestamp).
- IDs are stable, spoiler-neutral strings using lowercase letters, digits, and
  hyphens, unique in their owning scope. Changing a display label does not rename an
  ID. Paths are derived from IDs, stay within the selected workspace, and never
  accept `..`, absolute components, or arbitrary source-supplied paths.
- Cross-record references are objects: `game_id`, optional `playthrough_id`,
  `type` (`entry`, `plan`, `finding`, `source`, or `integration`), and `id`.
  Findings additionally require `topic_id`. Entry/plan references require a
  playthrough; a playthrough's dependencies cannot refer to another playthrough.
  All dependencies must remain within the owning game; game research cannot depend
  on a player's progress or plans.
- References resolve before their contents support advice. Dependency edges on
  entries/plans and derivation edges between findings form acyclic graphs; dangling or cyclic dependencies require
  repair. They cannot be silently dropped by the coach to make validation pass.
- Additive unknown fields may be preserved, but unknown schema versions cannot be
  rewritten without a separately reviewed format change. No destructive migration
  or automatic deletion is defined in v1.

`context` is an object with optional string fields `edition`, `platform`, and
`patch`, plus optional string arrays `dlc` and `mods`. Omission means unknown;
an explicitly empty array means the player reported none. `applicability` is an
object with optional arrays `editions`, `platforms`, `patches`, `dlc`, and `mods`,
plus `notes` describing verified coverage and unresolved limitations. Lists describe
evidence coverage, not proof that every combination applies. Unspecified coverage
requires judgment or research when it materially changes the answer.

## Workspace

**File**: `.cid/workspace.json`

| Field | Meaning and validation |
| --- | --- |
| `workspace_id` | Stable local workspace identity |
| `games` | Array of `{game_id, label}` registry entries; IDs unique |
| `active` | `null` or `{game_id, playthrough_id}` resolving to registered records |
| `preferences` | Workspace choices; see Preference below |
| `preference_prompts` | `spoiler_modes_explained` and `follow_through_offered` booleans, initially false |

The registry locates records; it is not a second copy of progress. An active pointer
is the last resolved context, not authorization to apply it to a new ambiguous
request. A missing/invalid pointer prompts targeted selection before state-dependent
advice. New workspaces have no games, no active selection, and no enabled assumption
preference. Fresh sessions read this file before selecting game/playthrough records.

## Game

**File**: `games/<game-id>/game.json`

| Field | Meaning and validation |
| --- | --- |
| `game_id` | Matches directory and workspace registry |
| `title` | Resolved game identity; distinguish similarly named releases if relevant |
| `identity_notes` | Optional disambiguation context; no forced irrelevant edition fields |
| `preferences` | Optional game overrides |
| `playthroughs` | Array of `{playthrough_id, label}` registry entries, unique within game |
| `topics` | Existing knowledge topic IDs; no empty mandatory category catalog |

One game owns many playthroughs, findings, sources, and integration records.
Reusable research belongs to the game; an individual player's platform, patch,
DLC, mods, progress, and goals belong to that playthrough when relevant.

## Playthrough, progress entry, and plan

**File**: `games/<game-id>/playthroughs/<playthrough-id>.json`

| Field | Meaning and validation |
| --- | --- |
| `game_id`, `playthrough_id`, `label` | Match the containing game and registry |
| `context` | Known relevant edition/platform/patch/DLC/mod details; omitted details are unknown |
| `preferences` | Optional playthrough overrides |
| `entries` | Selective reported/assumed state entries described below |
| `plans` | Proposed or selected advice, separately described below |
| `questions` | Concise unresolved coaching questions, each with ID, text, and `open`/`resolved` status |

An **entry** has `id`, `topic`, `statement`, `kind` (`reported` or `assumed`),
`status` (`current`, `superseded`, `retracted`, or `needs_review`), `recorded_at`,
`depends_on` (reference array), and optional `supersedes` (entry ID). Topics can
represent location, milestones, goals, character, equipment, important inventory,
constraints, difficulties, or established player knowledge. Capture only useful
details. Reported entries record player testimony, not externally verified mechanics.
An assumed entry additionally references its originating plan in `depends_on`.

Established player knowledge is supported by current reported entries, not assumed
attempts or the mere presence of game research. An assumption may inform qualified
planning but cannot expand a spoiler boundary. A correction retracting reported
knowledge also requires reconsidering the affected boundary before later advice.
One-time disclosure permission is not evidence of completed progress.

A **plan** has `id`, `text`, `status` (`proposed`, `accepted`, `rejected`,
`completed_reported`, `needs_review`, or `superseded`), `depends_on`, `recorded_at`,
and `reasoning_status` (`evidence_based` or `untested_deduction`). Optional
`replaces` points to a prior plan. Discussion creates a proposal; only an explicit
player selection creates `accepted`. Follow-through may create an assumed action
without asserting that the player accepted or completed a plan. Only a player
report can establish `completed_reported`; recommendations never prove success.

### State and correction transitions

1. A reported update adds/revises a current entry; obsolete entries are superseded
   when their distinction matters. Do not retain every incidental conversation.
2. Explicitly enabled follow-through permits a current assumed entry for a concrete
   recommendation. It does not infer victory, rewards, or arbitrary downstream state.
3. A correction supersedes/retracts the incorrect entry and adds a current reported
   replacement. Preserve the ID and short statement of the old entry while referenced.
4. Follow `depends_on` transitively through entries and plans. Mark affected active
   items `needs_review` before reusing advice; recompute or withdraw them. A revised
   plan gets a new ID referencing its valid prerequisites and replacing the old plan.
5. Save the correction, invalidations, and revised guidance in one playthrough
   replacement. No unrelated registry/research update may block that save.
6. Disabling follow-through prevents new assumptions. Existing assumptions remain
   labelled and can be corrected; disabling alone does not establish false progress.

## Preference

Preferences are embedded in the workspace, game, or playthrough file defining their
scope. Each stored key contains `{value, selected_at}`. Missing keys inherit.

| Key | Allowed values | Effective default |
| --- | --- | --- |
| `spoiler_mode` | `strict`, `hints`, `off` | `hints` |
| `follow_through` | `enabled`, `disabled` | unset, operationally disabled |
| `research_depth` | `brief`, `normal`, `thorough` | `normal` |
| `coaching_style` | Concise player-requested text | Preserve existing host/personality preferences |

Precedence: explicit playthrough choice → game choice → workspace choice → default.
An unscoped change updates the workspace choice. If a conflicting narrower choice
would prevent it taking effect in the active playthrough, also supersede that key
in the active playthrough with the new choice, unless the player explicitly asked
to preserve the current override. Preserve scoped choices in other playthroughs and
games. Save the active effective change first, then the workspace default, and
disclose partial-save outcomes. A deliberately scoped default-only request leaves
overrides intact and must be acknowledged as a default change.

Explicitly selecting Hints differs from having no selection, but both protect the
same content. Prompt-history booleans prevent repeated preference pitches without
treating silence as consent. Research depth never relaxes evidence requirements.
The one-time Hints permission is scoped to the current requested answer and is not
a stored `off` preference or a lasting disclosure grant.

## Knowledge finding

**File**: `games/<game-id>/knowledge/<topic-id>.json`, containing `game_id`,
`topic_id`, and `findings`.

Each finding contains `id`, `statement`, `kind` (`fact`, `sourced_strategy`, or
`deduction`), `status` (`supported`, `needs_review`, `disputed`, or `superseded`),
`applicability`, `evidence` (array), optional `derived_from` (finding references),
`spoiler` (object with `sensitive` boolean and optional `boundary_notes`), and
`checked_at`. `applicability` records known edition/platform/version/DLC/mod coverage
and limitations; absent coverage is unspecified, never proof of universal validity.

Evidence items contain `source_id`, `locator` (URL or integration-result locator),
`accessed_at`, and a concise `summary` supporting this claim. Integration evidence
also identifies `integration_id` and the observed successful query. Facts and
sourced strategies require actual evidence. Deductions require applicable premises
in `derived_from` and must be communicated as untested where material. Disputed or
review-needed findings cannot be asserted as settled facts.

Version changes, contradictions, or failed evidence reopen review. Reconsider
dependent findings/plans in the selected playthrough before using them. Other
playthroughs reassess relevant applicability/dependencies on load; no background
rewrite or automatic player-progress change is required.

## Source reference

**File**: `games/<game-id>/sources.json`, containing `game_id` and `sources`.

Each source contains `id`, `locator`, `title`, `coverage` (topics), `applicability`,
`discovered_at`, `access_status` (`never_accessed`, `accessible`, `failed`, or
`requires_access`), nullable `last_attempt_at` and `last_success_at`, and `quality_notes`
covering relevance, maintenance, version compatibility, specificity, and credibility.
Unknown quality/access details remain explicitly unknown. Optional `integration_id`
identifies the integration supplying a result.

A discovered locator is not evidence of access. A previously accessible source can
later fail; preserve the earlier access context. Source titles and locators may
themselves spoil content and cannot be echoed without disclosure filtering.

## Integration record

**File**: `games/<game-id>/integrations.json`, containing `game_id` and `integrations`.

Each integration contains `id`, `name`, `capabilities`, `coverage`, `access_requirements`
(descriptions, never credentials), `discovery_locator`, and `observations`.
Each observation records `host`, `checked_at`, `availability` (`available`,
`unavailable`, or `unknown`), `reason`, and optional `last_query` with `attempted_at`,
`outcome` (`success` or `failure`), and a concise result/error reference.

Discovery creates unknown availability, not an installation or successful query.
Host/session changes require a new capability check. Availability does not establish
that a particular query succeeded; only accessed results support findings.

## Persistence validity

Increment a document's revision on a verified replacement and update its timestamp.
Use source → finding → dependent-plan publication order. Publish game/playthrough
files before registries and active pointers. Retry/reconcile a failed registry save
against actual files; never recreate or overwrite an unregistered record blindly.
Corrupt, unknown-version, or dangling records require recovery before dependent use.
Temporary replacement files are not authoritative records. See the
[write and recovery contract](contracts/workspace.md#write-and-recovery-contract).

## Record minimization and ownership

Keep only coaching-relevant summaries and referenced provenance; no full transcript,
credentials, authentication tokens, or copied integration datasets belong in records.
Player records remain in the chosen workspace. Cid adds no automatic upload,
telemetry, synchronization, or retention service. The host's normal processing and
provider policies still apply; local persistence is not a promise of on-device model
inference. No automatic expiry, destructive cleanup, or deletion workflow is part of
v1. Preserve referenced superseded entries concisely for correction traceability.
