# Feature Specification: Cid — Local AI Video Game Coach

**Feature Branch**: `main` (current branch)

**Created**: 2026-11-07

**Status**: Draft — ready for implementation planning

**Input**: Feature requirements consolidated in this specification.

Cid helps a player decide what to do in a video game using researched game knowledge, remembered playthrough context, and strategic reasoning. It addresses invented game facts, repeated research, and lost progress between conversations. Its primary user is a player seeking conversational help with their own games and playthroughs.

## Clarifications

### Session 2026-11-07

- Q: How should Cid show supporting sources in its coaching replies? → A: Keep sources in local records and show them only when requested.
- Q: When a player using Hints explicitly asks for a puzzle solution or another spoiler, how should Cid respond? → A: Answer the explicit request as a one-time exception; keep Hints afterward.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get useful help with a new game (Priority: P1)

A player introduces a game, shares as much progress as they wish, and gets help with a concrete question or a broad goal such as “What should I do next?”

**Why this priority**: A player must receive useful coaching before investing in a detailed progress record.

**Independent Test**: Start with an empty workspace and a new-game request. Verify that the coach identifies the game, researches enough to help, and provides an actionable response or a question needed to make one.

**Acceptance Scenarios**:

1. **Given** a named game and an immediate goal, **When** the player asks for help, **Then** Cid establishes game identity, researches relevant mechanics and dependable sources, and gives a next action with a reason tied to that goal.
2. **Given** an ambiguous game title or a version difference that could change the answer, **When** Cid prepares advice, **Then** it resolves that ambiguity before making dependent claims; it does not require edition, platform, patch, DLC, or mod details that do not affect the answer.
3. **Given** missing progress, **When** the player starts coaching, **Then** Cid asks a focused initial question, gathers only information needed for the current request, and defers unrelated questions.
4. **Given** the player skips a question or asks for less research, **When** coaching continues, **Then** Cid narrows or qualifies its advice and continues helping without requiring completion of an interview or guessing missing facts.
5. **Given** a game for which only a few coaching topics are relevant, **When** foundational knowledge is saved, **Then** it covers those topics without requiring empty categories or an exhaustive encyclopedia.

---

### User Story 2 - Receive an evidence-based answer (Priority: P1)

A player asks about a mechanic, build, item, or strategy and receives advice based on applicable evidence, with uncertainty made clear when verification is not possible.

**Why this priority**: Advice that invents mechanics can waste progress and undermine the entire coaching experience.

**Independent Test**: Use controlled questions with saved evidence, missing evidence, contradictory sources, and an unavailable integration. Inspect both the answers and research activity.

**Acceptance Scenarios**:

1. **Given** applicable local knowledge answers a question, **When** the player asks it, **Then** Cid reuses that knowledge without a broad search and preserves its source context.
2. **Given** local knowledge is insufficient but an indexed source covers the topic, **When** Cid researches, **Then** it consults the relevant source before considering a broad search.
3. **Given** local knowledge and indexed sources are insufficient, **When** a relevant information integration is available, **Then** Cid checks it before a broad search; an unavailable integration is recorded as unavailable, not as evidence it was queried.
4. **Given** an unfamiliar mechanic or potentially outdated information, **When** the player requests a factual answer, **Then** Cid researches before asserting a claim and saves useful findings with source links and applicability context.
5. **Given** sources disagree, **When** Cid evaluates them, **Then** it considers relevance, maintenance, version compatibility, specificity, and credibility; it either explains the supported conclusion or states the unresolved conflict.
6. **Given** evidence cannot be accessed or verified, **When** Cid responds, **Then** it identifies what remains unknown and requests useful player information rather than filling the gap from model familiarity.
7. **Given** an evidence-based answer, **When** the player has not requested sources, **Then** Cid retains supporting links in local records without adding them to the reply; when the player requests sources, it provides applicable references subject to the spoiler setting.

---

### User Story 3 - Continue a playthrough in a fresh conversation (Priority: P1)

A player returns later, using either supported assistant, and continues from saved progress, goals, plans, and preferences in their chosen workspace.

**Why this priority**: Durable context removes the need to reconstruct a playthrough each session.

**Independent Test**: Save meaningful updates, end the conversation without a closing command, and resume in each supported host. Include two games and two playthroughs of one game.

**Acceptance Scenarios**:

1. **Given** recorded progress and preferences, **When** a fresh conversation begins in Codex CLI or Claude Code CLI using the same workspace, **Then** Cid uses those records without requiring the player to repeat recorded history.
2. **Given** a player reports a milestone, changed equipment, a new goal, or a preference, **When** the conversation moves on, **Then** the meaningful update is saved during that conversation without requiring a session-ending command.
3. **Given** separate games and playthroughs, **When** the player switches between them, **Then** Cid applies the selected playthrough's progress and plans; when the selection is ambiguous, it asks which one to use.
4. **Given** a meaningful update cannot be saved, **When** the failure is detected, **Then** Cid identifies the unsaved update and tells the player that it will not be available from saved records.
5. **Given** a long conversation containing incidental details, **When** records are updated, **Then** they retain coaching-relevant facts and unresolved plans without requiring a transcript or complete inventory and game-state simulation.

---

### User Story 4 - Protect discoveries while getting guidance (Priority: P1)

A player receives useful help that respects how much they want revealed about the game.

**Why this priority**: An unintended spoiler cannot be undone; protection applies from the first interaction.

**Independent Test**: Use known spoiler-bearing material and a stated player knowledge boundary. Exercise Strict, Hints, Off, an unset preference, and uncertain progress, including links and visual aids when supported.

**Acceptance Scenarios**:

1. **Given** no saved setting, **When** the first spoiler-sensitive interaction occurs, **Then** Cid briefly explains Strict, Hints, and Off, uses Hints until the player chooses, and persists any selection without blocking help.
2. **Given** Strict, **When** an answer would go beyond established player knowledge, **Then** Cid requests permission without revealing the protected detail in the permission request and stays within the boundary until permission is granted.
3. **Given** Hints and no explicit request for a spoiler, **When** the player is stuck, **Then** Cid provides direction without revealing story developments, hidden rewards, surprise encounters, or puzzle solutions.
4. **Given** Off, **When** the player asks for an answer requiring spoilers, **Then** Cid may provide the spoilers relevant to that request.
5. **Given** progress is too uncertain to judge the boundary, **When** spoiler-sensitive advice is requested, **Then** Cid asks a targeted question or gives less revealing guidance.
6. **Given** stored knowledge or a source contains spoilers, **When** Cid responds, **Then** the chosen setting governs prose, headings, link labels and destinations, images, and source descriptions; access to stored knowledge does not authorize disclosure.
7. **Given** the player changes the setting, **When** subsequent advice is given and later resumed, **Then** the new setting is applied and remembered.
8. **Given** Hints, **When** the player explicitly requests a puzzle solution or another spoiler, **Then** Cid answers within the scope of that request without an additional confirmation and keeps Hints for subsequent advice; a general request for help does not grant this exception.

---

### User Story 5 - Use initiative while keeping assumptions correctable (Priority: P2)

A player can let Cid assume follow-through on recommendations, then correct an assumption without leaving later advice based on false progress.

**Why this priority**: This reduces repetitive confirmations while preserving an accurate distinction between plans, inferred actions, and reported outcomes.

**Independent Test**: Enable follow-through, receive multiple recommendations, discuss an alternative, then correct an assumed action on which a later plan depends. Inspect both saved state and revised guidance.

**Acceptance Scenarios**:

1. **Given** no follow-through preference has been chosen, **When** a strong actionable recommendation first makes it useful, **Then** Cid offers the persistent preference; silence does not enable it.
2. **Given** follow-through is enabled, **When** Cid recommends an action, **Then** it applies the preference without repeated confirmations or announcements and keeps inferred actions distinguishable from reported facts.
3. **Given** the player discusses alternatives or receives a strategy, **When** Cid updates progress, **Then** discussion is not recorded as a choice and recommending the strategy is not recorded as successful completion.
4. **Given** a later recommendation depends on an assumed action, **When** the player corrects that action, **Then** the correction overrides the assumption, is saved, and triggers reconsideration of affected guidance.
5. **Given** the player rejects a recommendation or disables follow-through, **When** further advice is given, **Then** Cid honors the change and records any relevant preference without treating the rejected action as completed.

---

### User Story 6 - Direct the coaching conversation (Priority: P2)

A player asks for advice in their preferred style, changes direction, and receives reasoning and presentation suited to the question.

**Why this priority**: Flexible coaching must serve the player's goals rather than require a prescribed sequence.

**Independent Test**: Use a prepared playthrough record to ask about a loadout, request next steps, change goals, and request a comparison. Check that missing information is requested only when it changes advice.

**Acceptance Scenarios**:

1. **Given** known progress, equipment, goals, and constraints, **When** the player asks “Is my loadout okay?” or “What should I do next?”, **Then** Cid gives specific actions and explains their relevance to that context.
2. **Given** a missing detail would materially change the recommendation, **When** Cid responds, **Then** it asks a focused question rather than presenting a dependent recommendation as settled.
3. **Given** an original strategy derived from researched mechanics, **When** the strategy has an important untested deduction, **Then** Cid identifies that uncertainty without presenting the deduction as an established game fact.
4. **Given** an existing assistant personality preference or a redirected goal, **When** Cid continues, **Then** it respects that preference and goal while remaining concise, conversational, and motivating without forced enthusiasm or a required character persona.
5. **Given** a visual or interactive aid would help and is supported, **When** Cid uses it, **Then** equivalent usable guidance is also available in text; lack of that capability does not prevent coaching.

### Edge Cases

- **Ambiguous context**: Resolve the active game or playthrough before applying its progress; do not merge state to avoid asking.
- **Version changes or contradictory evidence**: Reassess applicability and dependent advice instead of continuing to reuse the old finding as settled fact.
- **Failed links or unavailable integrations**: Seek alternative evidence when possible, retain accurate access status, and disclose remaining uncertainty.
- **Research declined or unavailable**: Continue with verified knowledge or qualified guidance; reduced research depth does not permit invented facts.
- **Unknown spoiler boundary**: Use a focused question or less revealing response. A protective heading or link must not itself reveal the spoiler.
- **Corrected assumption chain**: Reconsider downstream advice, not just the single corrected entry; do not infer unrelated outcomes.
- **Interrupted session or failed save**: Resumption relies on persisted updates; identify failed updates during the active conversation rather than claiming they were saved.
- **Unsupported presentation capability**: Supply usable text without requiring images, diagrams, or interactive controls.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Cid MUST operate in Codex CLI and Claude Code CLI with the same coaching behavior and shared records in a user-selected local folder or repository.
- **FR-002**: Cid MUST establish game identity and ask about edition, platform, patch, DLC, or mods only when they affect the requested advice.
- **FR-003**: Initial research MUST establish relevant mechanics, coaching topics, and dependable sources sufficient for the current help request; it MUST NOT require exhaustive coverage or irrelevant categories.
- **FR-004**: When progress is missing, Cid MUST use a conversational, skippable interview and defer questions not needed for the current request.
- **FR-005**: Factual game claims MUST be grounded in applicable previously researched knowledge or external evidence; model familiarity alone MUST NOT count as verification.
- **FR-006**: Before a broad web search, Cid MUST check local knowledge, the saved source index, and relevant available APIs or MCP tools, in that order, stopping when sufficient applicable evidence is found.
- **FR-007**: Cid MUST research missing, uncertain, conflicting, or potentially outdated facts before presenting them as facts. When verification fails, it MUST explain the specific uncertainty and request useful player information instead of guessing.
- **FR-008**: Cid MUST evaluate sources by relevance, maintenance, version compatibility, specificity, and credibility rather than source type alone.
- **FR-009**: Cid MUST retain useful findings with source links and applicability context, and maintain an index of discovered sources describing topic coverage. Supporting sources MUST remain in local records and appear in coaching replies only when the player requests them; omitting visible citations MUST NOT relax evidence requirements.
- **FR-010**: Cid MUST record useful integrations, their capabilities, access requirements, and actual availability; discovery MUST NOT imply installation, access, or a successful query.
- **FR-011**: Cid MUST query available integrations when relevant, without requiring their datasets to be copied locally. It MUST avoid exhaustive scraping and repeated broad searches without a new information need, and revisit sources when updates, contradictions, or failed links justify it.
- **FR-012**: Coaching instructions, researched knowledge, source references, progress, and preferences MUST persist in the selected workspace and remain usable across fresh conversations in both supported hosts.
- **FR-013**: Cid MUST keep game and playthrough progress distinct and ask the player to resolve ambiguous context before applying playthrough-specific information.
- **FR-014**: Progress records MUST selectively capture relevant location, milestones, goals, character details, equipment or inventory, constraints, difficulties, preferences, outstanding questions, and plans without requiring complete game-state simulation.
- **FR-015**: Cid MUST save meaningful updates during conversation rather than relying exclusively on a closing command. On failure, it MUST tell the player which update was not persisted.
- **FR-016**: Cid MUST distinguish player-reported facts, assumed actions, and proposed plans, and retain meaningful dependencies needed to reconsider advice after a correction.
- **FR-017**: At the first relevant opportunity, Cid MUST offer a persistent follow-through preference. It MUST assume follow-through only after the player enables that preference and MUST then apply it without repeated confirmations or announcements.
- **FR-018**: Cid MUST NOT treat discussion of alternatives as a selection or a recommendation as evidence of successful completion.
- **FR-019**: Player corrections MUST override assumptions, update the saved record, and trigger reconsideration of affected advice. Rejected advice MUST inform recorded preferences when relevant, and the player MUST be able to change the follow-through preference.
- **FR-020**: Cid MUST provide actionable guidance for specific and open-ended requests using known progress, goals, mechanics, and constraints; it MUST ask focused questions when missing information materially changes the recommendation.
- **FR-021**: Cid MAY combine researched strategies with original reasoning but MUST identify important untested deductions or suggestions as such.
- **FR-022**: Cid MUST respect existing assistant personality preferences and remain concise, conversational, and motivating without forced enthusiasm or a mandatory character persona.
- **FR-023**: Players MUST be able to skip questions, redirect goals, change research depth, and request unforeseen help without a fixed workflow blocking assistance.
- **FR-024**: Cid MUST default to Hints, briefly explain Strict, Hints, and Off at the first spoiler-sensitive interaction, and persist and honor the player's selection and later changes.
- **FR-025**: Strict MUST stay within established player knowledge and ask before crossing that boundary. Hints MUST provide useful direction without revealing story developments, hidden rewards, surprise encounters, or puzzle solutions, except when the player explicitly requests a specific spoiler. Such a request MUST authorize only the requested answer without an additional confirmation and MUST NOT change the saved Hints setting; general requests for help MUST NOT count as this authorization. Off MUST allow spoilers relevant to the request.
- **FR-026**: If progress cannot establish a spoiler boundary, Cid MUST ask a targeted question or provide less revealing guidance. Spoiler protection MUST apply to prose, headings, links, images, and source descriptions, including permission requests and material drawn from local knowledge.
- **FR-027**: Visual or interactive aids MAY supplement coaching when supported and useful; Cid MUST always provide a usable text alternative.

### Scope and Operating Constraints

Cid is an open-source local coach. Shared coaching instructions and portable local records, with thin setup for each supported host, are the constitution's required delivery boundary. A standalone companion program is optional and requires a documented need during planning. The MVP MUST NOT require a separately hosted coaching service or custom model API integration.

Mobile use may rely on a supported host's existing remote access to an always-on computer. Native mobile integrations, cloud synchronization, custom remote-access infrastructure, hosted accounts, and independently operating phone-only access are excluded. Automatic save-file ingestion, gameplay telemetry, autonomous gameplay, and exhaustive game databases are also excluded.

### Key Entities *(include if feature involves data)*

- **Workspace**: The player-selected local home for shared instructions, game knowledge, source records, playthroughs, and preferences.
- **Game**: An identified title with relevant edition or version context and reusable researched knowledge; it may have multiple playthroughs.
- **Playthrough**: A distinct record of progress, goals, character details, constraints, questions, and plans for one game.
- **Preference**: A persistent player choice, including spoiler level, follow-through, and coaching preferences, with its applicable scope.
- **Knowledge finding**: A researched fact or strategy with supporting sources and context indicating where it applies.
- **Source reference**: A discovered source, its coverage, and information needed to judge relevance and applicability later.
- **Integration record**: A game information integration with capabilities, access requirements, and known availability, distinct from evidence actually obtained through it.
- **Assumption and dependent plan**: An inferred action or state, its distinction from reported facts, and affected recommendations that must be reconsidered if it changes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

These are acceptance targets, not claims of measured performance. Evaluate the scenarios above using controlled evidence and playthrough records; include both supported hosts, at least three games with different coaching needs, and version-sensitive and unavailable-evidence cases. Record failed and untested scenarios explicitly.

- **SC-001**: In at least 10 new-game trials with a resolvable title and accessible evidence, at least 9 produce an actionable next step within three player replies to setup questions. Skipping unrelated questions does not prevent help. (Story 1)
- **SC-002**: In every evaluated factual-answer scenario, asserted game facts have applicable supporting evidence; inaccessible or unresolved evidence produces explicit uncertainty rather than an invented answer. Include at least one conflict and one version mismatch. (Story 2)
- **SC-003**: In every evaluated question fully answered by applicable saved knowledge or an indexed source, the player receives an answer without a repeated broad search. (Story 2)
- **SC-004**: All four resumption combinations between the two supported hosts preserve saved progress and preferences without asking the player to repeat recorded history. Switching among two games and two playthroughs of one game introduces zero cross-playthrough progress errors. (Story 3)
- **SC-005**: In all evaluated meaningful-update scenarios, the update is available in a fresh conversation without a closing command, or a deliberately failed save is clearly disclosed during the original conversation. (Story 3)
- **SC-006**: In every evaluated spoiler scenario, the complete response respects the selected mode. Cover all three modes, the default, uncertain progress, a changed preference, a specifically requested one-time Hints exception followed by continued Hints protection, and each supported presentation format; there are zero unauthorized disclosures in this set. (Story 4)
- **SC-007**: After follow-through is enabled, at least three successive recommendations require zero repeated preference confirmations. A correction to an assumed action changes both the saved assumption and dependent advice; alternatives and recommended strategies create zero false records of selection or success. (Story 5)
- **SC-008**: In a usability review with at least five players, at least four rate the advice at least 4 out of 5 for usefulness and report that they could redirect coaching toward their own goals. Every evaluated visual aid has usable equivalent text. (Story 6)

## Assumptions

- One player uses the selected workspace at a time. Simultaneous editing from multiple hosts is not an MVP acceptance requirement; sequential use across hosts is required.
- The player supplies progress and corrections conversationally. Unreported progress is unknown unless recorded as an assumption under an enabled follow-through preference.
- Unless the player specifies a narrower scope, spoiler and follow-through choices persist as workspace preferences across conversations. An explicitly scoped choice is recorded and honored for that scope.
- The supported hosts provide conversation, local record access, and any available research capabilities. Access to any particular external source or integration is not guaranteed; lack of access invokes the uncertainty behavior.
- “Meaningful update” means a change that affects future coaching: progress, relevant character details, goals, constraints, preferences, assumptions, outstanding questions, plans, or useful research. Incidental conversation does not require retention.
- The setup-turn and usability targets are proposed MVP evaluation thresholds where the brief provided no numeric threshold. They measure the coaching experience rather than external source response times.
- Constitution principles I–V apply without exceptions: Story 2 covers evidence, Story 3 portable records, Story 5 correctable assumptions, Story 4 spoilers, and Stories 1 and 6 player-directed coaching. Scope constraints above preserve the constitution's MVP boundary.
