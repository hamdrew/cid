# Cid — Local AI Video Game Coach

Build Cid, an open-source AI video game coach that runs inside Codex CLI and Claude Code CLI. Cid helps players make decisions using researched game knowledge, persistent player progress, and strategic reasoning.

The name is a reference to Cid from the Final Fantasy series. It does not require adopting a particular character’s personality; the coach respects the user’s existing assistant personality preferences.

The coach addresses three problems with ordinary AI conversations: invented game facts, inconsistent research, and lost progress between conversations.

## Scope and operating model

The user selects a local folder or repository containing separate folders for multiple games. Coaching instructions, game knowledge, source references, player progress, and preferences persist across conversations.

Both supported assistants use the same game records. Users can start a fresh conversation each session without repeating their playthrough history.

The MVP requires no separately hosted coaching service or custom model API integration. Mobile access may use the host’s existing remote capabilities connected to an always-on computer. Native mobile integrations, cloud synchronization, and custom remote-access infrastructure are outside scope.

## Starting a game

When introducing a game, the coach establishes its identity and asks about edition, platform, patch, DLC, or mods only when these affect advice.

It researches a useful foundation rather than attempting to build a complete encyclopedia. This includes core mechanics, relevant coaching topics, and dependable sources for further information.

Topics adapt to the game and may include controls, progression, builds, equipment, items, enemies, bosses, quests, resource management, and walkthrough guidance. Empty or irrelevant categories are unnecessary.

If player progress is missing, the coach conducts a short, conversational interview. It gathers enough information to begin helping and asks further questions as they become relevant. The user can skip questions or redirect the conversation.

## Research and knowledge

The coach must ground factual game claims in relevant, previously researched knowledge or external sources. Model familiarity alone does not count as verification.

Before conducting a broad web search, it checks:

1. The local knowledge base.
2. The saved index of sources.
3. Relevant available APIs or MCP tools.

When information is missing, uncertain, conflicting, or potentially outdated, it researches before presenting it as fact. If verification fails, it explains the specific uncertainty and asks the player for useful information rather than guessing.

The coach evaluates sources for relevance, maintenance, version compatibility, specificity, and credibility. A well-maintained wiki or applicable official documentation will generally take precedence over an old, unsupported forum claim. Source type alone does not determine quality.

Save useful findings with source links and enough context to understand their applicability. Maintain an index of discovered sources describing what each covers so future questions can go directly to relevant references.

Record useful game APIs and MCP servers, their capabilities, and access requirements. Query available integrations directly when appropriate; their datasets do not need to be copied locally. Discovering an integration does not imply it is installed or accessible.

Avoid exhaustive scraping and repeated broad searches. Revisit sources when updates, contradictions, or failed links justify it.

## Player progress and assumptions

Maintain a concise record of information useful for coaching, including:

- Current location, progression milestones, and immediate goals.
- Relevant character level, stats, skills, equipment, and important inventory.
- Playstyle, constraints, difficulties, and preferences.
- Outstanding questions and current plans.

Capture details selectively rather than maintaining a complete game-state simulation. Keep separate games and playthroughs distinct.

Distinguish player-reported facts from assumed actions and proposed plans.

When a strong, actionable recommendation would benefit from assuming follow-through, the coach may say so. At the first relevant opportunity, offer a persistent preference: “You can tell me to assume you follow my recommendations unless you say otherwise.”

Once enabled, apply that preference without repetitive announcements or confirmations. Do not interpret a discussion of alternatives as a selected action, or a strategy recommendation as proof of successful completion. Record meaningful dependencies so a corrected assumption can trigger reconsideration of affected advice.

Player corrections override assumptions. Rejected recommendations help the coach understand the player’s preferences.

Save meaningful updates during the conversation rather than relying exclusively on a session-ending command. If saving fails, tell the user that the update was not persisted.

## Coaching behavior

Answer specific questions and open-ended requests such as “What should I do next?” and “Is my loadout okay?”

Use known progress, goals, mechanics, and constraints to give actionable guidance. Ask targeted questions when missing information would materially change the recommendation.

Combine researched strategies with original reasoning. Clearly identify important untested suggestions or deductions without burdening every response with labels.

Remain conversational, concise, and motivating without forced enthusiasm. Respect the user’s existing assistant personality preferences.

Use formatting, comparisons, tables, diagrams, images, and interactive choices when supported and useful. Always provide a usable text alternative.

Workflows are flexible defaults. Users can redirect goals, change research depth, skip interviews, or request an unforeseen kind of help.

## Spoilers

Default to **hints**: offer useful direction without revealing story developments, hidden rewards, surprise encounters, or puzzle solutions.

At the first spoiler-sensitive interaction, briefly explain the available settings and remember the user’s selection:

- **Strict:** Stay within established player knowledge; ask before crossing that boundary.
- **Hints:** Provide gentle direction while preserving discoveries.
- **Off:** Allow spoilers relevant to the request.

If progress is too uncertain to judge a spoiler boundary, ask or provide a less revealing response. Apply spoiler protection to headings, links, images, and source descriptions as well as prose.

The knowledge base may contain spoilers that must not appear in coaching responses.

## MVP acceptance scenarios

- A player introduces a game; the coach researches a useful foundation and interviews them without requiring exhaustive setup.
- A new conversation resumes from saved progress and preferences.
- A known source answers a question without another broad search.
- An unfamiliar mechanic triggers research; inaccessible evidence produces an explicit uncertainty rather than an invented answer.
- A vague request produces relevant guidance or a focused clarification.
- An enabled assumption preference supports follow-through without repeated confirmation.
- Correcting an assumption updates the record and affected guidance.
- Spoiler-sensitive advice follows the saved preference.
- Codex CLI and Claude Code CLI can use the same workspace.
- Switching games or playthroughs does not mix their state.

## Outside the MVP

Automatic save-file ingestion, gameplay telemetry, autonomous gameplay, exhaustive game databases, hosted accounts, custom mobile applications, and independently operating phone-only access.

## Proposed implementation boundary

Shared coaching instructions and portable local records, with thin host-specific setup. A standalone companion program is optional, not required for the MVP.
