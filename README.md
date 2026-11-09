# Cid

A personal video game coach for Codex CLI and Claude Code CLI. Introduce your game
and goal, ask for help, and correct or redirect the advice whenever you want.
Cid keeps useful research, progress, preferences and plans in your chosen folder
so you can continue in a fresh conversation.

## Set up once

You need an authenticated Codex CLI or Claude Code CLI with local file tools.
Research uses whatever tools your host actually provides. Python is not needed to use Cid.

From this repository, choose a **new** workspace directory:

```sh
CID_REPO="$(pwd -P)"
CID_WORKSPACE="$HOME/cid-games"
mkdir "$CID_WORKSPACE" &&
  cp -R "$CID_REPO/templates/workspace/." "$CID_WORKSPACE/" &&
  cp "$CID_REPO/coaching/COACH.md" "$CID_WORKSPACE/.cid/COACH.md" &&
  cp "$CID_REPO/adapters/codex/AGENTS.md" "$CID_WORKSPACE/AGENTS.md" &&
  cp "$CID_REPO/adapters/claude/CLAUDE.md" "$CID_WORKSPACE/CLAUDE.md"
```

The copies run only if the directory is new. If it already exists, use the merge
instructions below or choose another path.

Edit `.cid/workspace.json` once: replace `workspace-template` with a stable local
identity such as `my-games`, and set `updated_at` to the current UTC timestamp
(for example the output of `date -u +%Y-%m-%dT%H:%M:%SZ`). Leave games empty,
active null and preferences empty. Keep this identity across future sessions.

Start your preferred host yourself:

```sh
codex --cd "$CID_WORKSPACE" --sandbox workspace-write --ask-for-approval on-request --search
```

Or, from the same workspace in a separate session:

```sh
cd "$CID_WORKSPACE"
claude
```

Say something like “Help me with [game]. My goal is [goal].” Share whatever progress
is useful. You can skip questions, ask for less research or change direction.
No special start, save or closing commands are required.

For ongoing coaching in a new game, Cid researches how play repeats, how
progress works and how the main systems affect your choices. It uses those
mechanics to ask brief, skippable questions about details that could change the
advice. A current quest gives Cid context for that broader work. Cid saves
supported explanations and a connected overview for later conversations.

If the host cannot read the policy, check that you started at the workspace root.
Codex overrides or Claude instruction exclusions can prevent loading; Claude's
`--bare` and `--safe-mode` suppress custom instruction discovery. Preserve your
existing settings and permissions rather than bypassing them.

## Use it normally

- **Spoilers:** Hints is the default. Strict asks before crossing reported knowledge;
  Off allows relevant spoilers. A specific spoiler request in Hints covers just
  that answer, then protection continues. A request for sources still respects spoilers.
- **Follow-through:** disabled until you enable it. When enabled, Cid may assume an
  attempt, never a victory, reward or discovery. “I didn't do that” should correct
  the record and any dependent advice. You can disable it at any time.
- **Preferences:** choices apply across the workspace unless you name a game/run
  scope. An unscoped change takes effect in the current run too; other runs retain
  their explicit choices. You can request a default-only change.
- **Research:** ask for a quick answer, defer a topic, or skip a question at any
  time. Cid can give narrower or conditional help and explain gaps when evidence
  is limited. A fresh conversation reuses applicable saved knowledge and run
  context. You can request a lasting depth preference or a research restriction
  for a run, game or the whole workspace. Lasting game/workspace restrictions
  are saved in workspace/game JSON records; run restrictions stay with that run.
- **Records:** meaningful updates are saved during the conversation. Failed or
  unconfirmed saves should be identified. Start a fresh conversation whenever you like.

Your workspace holds the installed policy in `.cid/COACH.md`, settings and registry
in `.cid/workspace.json`, and research plus separate playthroughs under `games/`.
Use one editing host at a time. Normal host/provider processing still applies;
local records do not imply on-device inference. Keep credentials and full transcripts
out of coaching records. Supporting links are retained locally; host rules may still
require visible citations.

## Give feedback

Use Cid, then send bullet points of things you want tweaked. For example:

- “Ask fewer setup questions before helping.”
- “You forgot my current goal when I started a new conversation.”
- “I corrected that assumption, but the next suggestion still relied on it.”
- “Keep loadout advice shorter and explain the tradeoff.”

There is no required format, score, session count or list to complete. If an example
helps explain the problem, include it; you do not need to diagnose the cause.

You can explicitly ask me to review a transcript and a copy of your test workspace
or repository. I can compare the replies with saved records, identify issues and
suggest changes in this conversation. Include what bothered you or what you wanted
instead if helpful. Remove secrets or unrelated personal details before sharing.
I will not launch AI sessions, call model APIs, or run test agents to investigate.

## Optional checks

When convenient, pick one or two; a few minutes is enough. Your ordinary play covers
the happy path. These are prompts for exploration, not acceptance gates.

- **Fresh start:** open a new conversation and ask what you were working on.
- **Correction:** correct an assumption or goal and see whether the next advice adjusts.
- **Settings:** change a spoiler or follow-through preference and see whether it sticks.
- **Separate runs:** if you already use multiple games/runs, switch between them and
  check that goals and progress stay separate.

If research is unavailable or something cannot be saved during ordinary use, notice
whether Cid explains the limitation clearly. There is no need to manufacture failures.
Tell me what felt wrong; untried behavior simply remains unknown.

## Existing workspaces and updates

Merge the small bootstrap from `adapters/codex/AGENTS.md` into existing `AGENTS.md`
and `@AGENTS.md` into `CLAUDE.md`. Preserve existing instructions, overrides and
personality preferences. Put the shared policy in `.cid/COACH.md`. Do not recopy
the empty workspace template over existing records.

For updates, compare/merge the new `coaching/COACH.md` into the installed copy,
preserving deliberate local changes. If the bootstrap changed, merge those loading
lines too. Keep workspace identity, preferences and everything under `games/`.
Cid can reuse an existing overview or extend useful older knowledge in place.
Existing records stay in JSON v1. There is no automatic synchronization. Preserve
readable content and ask for targeted help with corrupt or unknown-version records.

## Development reference

The [data model](specs/001-ai-game-coach/data-model.md) and
[contracts](specs/001-ai-game-coach/contracts/workspace.md) describe record details.
The [baseline specification](specs/001-ai-game-coach/spec.md) describes the shared
coach. The [game understanding contract](specs/002-game-understanding/contracts/game-understanding.md)
covers the bounded research pass and reuse.

The model-free local contract suite uses Python 3.11+ and no pip/npm dependencies:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Agents may run these local checks. They must never launch AI tools for testing or
unattended evaluation. Requested review of material you share stays in this conversation;
see the [constitution](.specify/memory/constitution.md). Git commits require explicit
approval for that specific commit.
