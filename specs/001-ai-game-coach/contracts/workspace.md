# Workspace and host contract

**Version**: 1 · **Requirements**: FR-001, FR-010, FR-012–FR-019, FR-024

Cid exposes a local file/setup interface and a conversational interface. It does
not expose an HTTP service or new executable CLI. Field definitions and transitions
are authoritative in [data-model.md](../data-model.md).

## Installation interface

The player selects a local directory. Fresh installation places these files there:

| Path | Owner and role |
| --- | --- |
| `AGENTS.md` | Thin bootstrap: read `.cid/COACH.md` and `.cid/workspace.json` for coaching |
| `CLAUDE.md` | Claude adapter importing `@AGENTS.md` |
| `.cid/COACH.md` | Installed copy of the shared coaching policy |
| `.cid/workspace.json` | Player-owned registry, active context, defaults, prompt history |
| `games/<game-id>/` | Player-owned shared research and separate playthrough records |

Setup must preserve existing `AGENTS.md`, `CLAUDE.md`, overrides, records, and
personality instructions. Merge a small Cid bootstrap into existing instruction
files instead of overwriting them. Check whether an override prevents loading.
Test discovery from the selected root rather than assuming a successful copy means
successful loading. Global configuration changes, plugin installation, host-specific
memory, custom slash commands, and symlinks are not setup prerequisites.

In Codex, inspect same-directory `AGENTS.override.md` and instruction-size limits
when the bootstrap is absent. In Claude, `--bare`, `--safe-mode`, managed-only
instruction settings, or exclusion rules can suppress project instructions/imports.
Treat a configuration that prevents shared-policy loading as incompatible setup;
do not silently alter user or managed policy. See the verified host references in
[research.md](../research.md#2-host-loading-and-capability-discovery).

Source-of-truth policy updates come from `coaching/COACH.md`; reinstall only that
policy and deliberate adapter changes. Never replace player records with templates
on upgrade. Both hosts use exactly the same installed policy and records.

## Session entry and context selection

1. Start either CLI at the selected workspace root. Ordinary language invokes
   coaching; no special session-start or session-end command is required.
2. Read the bootstrap, shared policy, and workspace record. Resolve explicitly named
   context first; otherwise use an unambiguous saved active context. Ask a focused
   question if a title/playthrough, pointer, or changed request is ambiguous.
3. Load the selected `game.json` and playthrough. Resolve preferences by scope and
   read only relevant topic/source/integration files for the current request.
4. Recheck applicability and review-needed dependencies before giving affected
   advice. Saved progress must not depend on recovering a previous host transcript.
5. Save meaningful changes during the exchange. Changing hosts is sequential;
   observations of integration availability must be checked again in the new session.

Switching a game/playthrough changes the active pointer only after resolving its
identity and reading its own state. Do not copy progress from the previous context.
A pointer write failure is disclosed separately from any successfully saved progress.

## Write and recovery contract

For each meaningful update:

Attempt the save in the response that handles the update, before moving to an
unrelated coaching topic. Disclose a failed or inconclusive save in that response.
An unexpected interruption before a save completes supplies no persistence guarantee;
fresh-session recovery uses actual files, never an assumed completed write.

1. Read the target and its revision immediately before editing. Preserve unrelated
   valid fields and user content; do not overwrite unexpectedly changed records.
2. Prepare a complete temporary replacement beside the target. Check JSON syntax,
   required fields, references, and intended changes with available host tools.
   Keep enough prior content to recover if replacement fails; no backup service is
   required. Temporary files are never selected as normal records.
3. Replace the target, then read the actual target and verify the new revision and
   relevant contents. Only verified target contents count as persisted.
4. If a tool fails, permission is denied, or read-back is inconclusive, identify
   the particular unsaved/unconfirmed update in the conversation. Do not circumvent
   permissions, claim persistence, or imply the next host will know the update.

This is a per-file host workflow, not a multi-file transaction guarantee. Keep
assumption correction and dependent-plan reconsideration together in one playthrough
replacement. Research writes publish sources/integration results before findings,
and findings before plans that cite them. Game/playthrough records precede registry
entries and active pointers. Failed unrelated research/index maintenance cannot
prevent a player correction from being saved.

On interruption, inspect actual records and reconcile incomplete references before
using dependent advice. Offer recovery of readable prior content or ask for the
specific missing information when necessary. Preserve successfully saved substeps;
do not replay an entire update blindly. An unregistered record can be re-registered
after identity checks. A missing registry target must not be invented. Do not delete
or reuse orphaned records/temporary files without establishing their role.

An unknown schema version or corrupt file is a targeted recovery case. Do not
silently reset it to an empty template. The MVP provides no simultaneous-writer
guarantee; revision mismatches prompt reread/reconciliation, not forced overwrite.

If cross-file publication is interrupted, the already saved correction or progress
remains authoritative. Repair only the missing registry/reference step after identity
and content checks. Do not roll back valid player state merely to make an index
consistent. Temporary or orphaned content may inform targeted recovery, but must not
silently replace a registered record.

## Development contract checks

Planned `tests/test_contracts.py` validates templates and complete workspace fixtures
using the Python standard library. Include positive and deliberately invalid cases:

- JSON/document version, required field types, valid enum values, and ID/path rules.
- Scope precedence and unset-versus-disabled/enabled preferences.
- Unique IDs, registered identities, active-pointer resolution, and reference targets.
- Acyclic assumption/plan dependencies and no cross-playthrough state references.
- Evidence/access distinctions and required support for sourced findings.
- Correction snapshots retaining provenance and marking transitive dependents.
- Orphaned/index-failure records that trigger recovery without losing a correction.

These checks do not prove that a host actually saved, researched, resumed, or
protected spoilers. Those require the observed trials in [quickstart.md](../quickstart.md).
