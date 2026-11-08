# Quickstart: Implementation validation

**Status**: Planned validation guide. This planning command creates design documents
only. The `coaching/`, `adapters/`, `templates/`, and `tests/` paths below must be
implemented before these product checks can run. No product test is claimed passing.

Use [data-model.md](data-model.md), [workspace contract](contracts/workspace.md),
and [coaching contract](contracts/coaching.md) as the expected behavior references.

## Prerequisites

- Authenticated Codex CLI and Claude Code CLI; record `codex --version` and
  `claude --version`. Local file read/write permission is needed for persistence.
- Research access for live new-game trials. Inspect tools actually available;
  having a discovered integration record is not access to that integration.
- Python 3.11+ for development checks only. Players do not need Python to coach.
- A disposable local workspace, controlled fixtures, and at least three evaluator-
  selected games with different coaching needs and applicable accessible evidence.
- At least five real players for SC-008. Agent simulation is not a substitute.

Do not use personal playthrough records for failure injection. Retain validation
evidence outside the source tree or in a deliberately selected local results folder;
no automatic upload, telemetry, or Git commit is part of this guide.
Use synthetic player details for controlled fixtures and omit credentials, private
paths, and unrelated personal content from retained traces. Anonymize human-review
results and publish them only by deliberate user choice. Cid's local record storage
does not change how the selected host processes conversations or external queries.
No automatic retention expiry or deletion service is provided.

## 1. Check record contracts

From the implemented repository root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: valid templates/fixtures pass; deliberately invalid versions, duplicate
IDs, dangling/cyclic references, invalid preferences, and mixed playthrough references
are rejected by the tests. A test suite containing expected rejection cases must
itself finish successfully. File checks do not replace the host trials below.

## 2. Install in a fresh disposable workspace

The following POSIX-shell example assumes the planned distribution paths exist.
Run it from the implemented repository root. `mktemp` deliberately creates a new
directory so these copies do not overwrite an existing player's instructions.

```sh
CID_REPO="$(pwd -P)"
CID_WORKSPACE="$(mktemp -d "${TMPDIR:-/tmp}/cid-validation.XXXXXX")"
cp -R "$CID_REPO/templates/workspace/." "$CID_WORKSPACE/"
cp "$CID_REPO/coaching/COACH.md" "$CID_WORKSPACE/.cid/COACH.md"
cp "$CID_REPO/adapters/codex/AGENTS.md" "$CID_WORKSPACE/AGENTS.md"
cp "$CID_REPO/adapters/claude/CLAUDE.md" "$CID_WORKSPACE/CLAUDE.md"
```

Expected: empty workspace registry, null active context, Hints effective by default,
and no enabled follow-through choice. For an existing workspace, use the documented
merge procedure instead of these copy commands. Check both adapters can read the
same policy, including when pre-existing host instruction files are present.
Include an overriding Codex instruction file or a Claude configuration that excludes
project instructions as a negative setup case. The outcome must identify the blocked
policy inclusion rather than claiming installation succeeded. Do not use Claude's
`--bare` or `--safe-mode` for ordinary acceptance trials; they suppress the needed
custom instruction discovery. Preserve user and managed configuration.

## 3. Start each host and check setup

Launch Codex with workspace writes and live research, retaining normal host approvals:

```sh
codex --cd "$CID_WORKSPACE" --sandbox workspace-write --ask-for-approval on-request --search
```

In a separate sequential trial, launch Claude from the same root:

```sh
cd "$CID_WORKSPACE"
claude
```

Start with “Help me with [selected game]. My goal is [goal].” Provide only necessary
context. Confirm the host reads the shared policy and records, asks relevant questions,
and gives a next action supported by observed evidence. Record setup replies, not
all conversational turns. Run ten fresh-workspace trials: five per host, at least
three games overall. Include skipped questions, relevant version ambiguity, a
resolvable title ambiguity, missing progress, and open-ended help. At least nine
must produce actionable guidance within three player replies to setup questions.
Native search availability does not imply permission for arbitrary shell networking.
Record actual research tools and denied fetches independently.

### Scoring definitions

Use these definitions consistently; they operationalize the specification's targets
without changing its numeric thresholds:

- **Setup reply**: One player message responding to setup questions, including a
  skipped question. The initial request is not a setup reply; a message answering
  several questions counts once. Count up to the first qualifying next step.
- **Actionable next step**: A specific feasible action or decision with a reason
  tied to the stated goal, supported by applicable evidence and permitted spoiler
  scope. Another clarification alone does not qualify. Qualified advice can qualify
  when its prerequisites are explicit and the proposed action remains feasible.
- **Broad search**: A general discovery query seeking new sources. Reading saved
  findings or consulting a known indexed source is reuse; actually accessing that
  source must still be observable when its content is needed.
- **Factual support**: Each material factual game claim maps to actually accessed
  evidence applicable to the known game context. An integration discovery record,
  an unopened search result, or model familiarity does not establish support.
- **Unauthorized disclosure**: Any protected detail beyond the effective spoiler
  mode and specifically granted current permission, including revealing labels,
  destinations, captions, or interactive states. Count each affected response as a
  failure and describe the disclosure; the target is zero.
- **Usable equivalent text**: Text carries the decision-relevant options, tradeoffs,
  and recommended action without requiring the visual or interactive aid. A visual's
  title or a statement that a comparison exists is insufficient.
- **Usefulness scale**: 1 = unusable; 2 = little practical help; 3 = partly helpful
  but needs substantial clarification; 4 = useful with only minor clarification;
  5 = directly useful without further clarification. Ask each player, “Could you
  redirect the coaching toward your own goal?” and retain their yes/no response
  separately. The same four of five players must meet both SC-008 conditions.

Before trials, freeze a scenario manifest with story/acceptance-scenario/SC IDs,
host, game context, fixtures, expected evidence, and permitted disclosure boundaries.
Cover every applicable scenario class named below in both hosts. Report every
scheduled trial, including failures and untested cases; do not remove difficult
cases from the denominator after observing results. Report ten setup outcomes and
both host-level counts, not an extrapolation to untested games or host versions.

## 4. Controlled behavior trials

Implementation must supply valid fixture workspaces under
`tests/fixtures/workspaces/` and scenario prompts under `tests/scenarios/` for the
cases below. Copy fixture state only into a fresh disposable workspace; keep the
installed policy/adapters. Mark synthetic evidence as test-only, never real game facts.
Separate controlled coverage tests from the three-real-game evaluation requirement.

| Criterion | Run and observe | Pass condition |
| --- | --- | --- |
| SC-001 | Ten new-game trials described above | ≥9/10 actionable within three setup replies; no forced unrelated setup |
| SC-002 | In both hosts: saved evidence, indexed source, available and unavailable integration, unfamiliar fact, source conflict, version mismatch, inaccessible evidence | Every asserted game fact maps to applicable accessed evidence; unresolved cases give specific uncertainty; no invented successful access |
| SC-003 | In both hosts: saved-knowledge question and indexed-source question; repeat each in fresh conversations | Zero broad searches for fully answered cases; indexed material is actually consulted when needed |
| SC-004 | Codex→Codex, Codex→Claude, Claude→Codex, Claude→Claude; in each pair switch A/run-1 → B/run-1 → A/run-2 | All four use persisted state without repeated history; distinct progress/goal/preference markers never mix |
| SC-005 | Both hosts: save progress, relevant character/equipment, goals, preferences, assumptions/plans, useful research; resume without closing command; inject real save and partial-publication failures | Every meaningful update is available fresh or its failed persistence was identified in the original conversation |
| SC-006 | Both hosts: default, Strict within/beyond boundary, ordinary Hints, specific Hints spoiler and protected follow-up, Off, uncertain progress, changed/resumed preference, requested spoiler-bearing sources, supported visuals and text fallback | Zero unauthorized disclosures across whole responses/artifacts; Hints exception stays scoped and does not change saved Hints |
| SC-007 | Both hosts: initially unset, preference offer, silence, explicit enablement, three successive recommendations, alternative discussion, strategy proposal, assumption chain, correction, rejection and disablement | Zero repeated preference confirmations after enablement; no false selection/success; correction changes persisted assumption and transitive dependent advice |
| SC-008 | At least five actual players distributed across both hosts and three games; each attempts goal redirection and rates usefulness | The same ≥4 players rate usefulness ≥4/5 and report successful redirection; every evaluated visual has usable text |

For FR-009 within Story 2, include both an unrequested-source reply and an explicit
source request, covering saved evidence and live research. Inspect actual output.
Unsolicited supporting citations fail FR-009 compatibility even if the answer is
otherwise supported; a mandatory host citation rule remains binding. Report a path
that cannot be observed as untested. Do not silently waive the requirement, suppress
mandatory citations, or claim full acceptance while this compatibility check fails.

Also check scope inheritance (workspace → game → playthrough overrides), malformed
and unknown-version records, unknown spoiler metadata, an invalid active pointer,
and pre-existing host instructions. These must produce targeted recovery or safe
fallback without resetting records, mixing state, or silently dropping user policy.
With a conflicting active override, request “switch to Hints” and “disable
follow-through” without specifying scope: both must change effective current behavior
and the workspace choice, preserving scoped choices in other playthroughs. Separately
request a default-only change and verify the current override remains effective.
Inject failure between active-choice and default saves and verify accurate disclosure.

Include a follow-through assumption that the player attempted a spoiler-sensitive
encounter but never reported its outcome. That assumption must not expand the known
spoiler boundary. Exercise request-specific Strict permission and then an unrelated
follow-up; the original permission must not authorize the later disclosure. Correct
a reported knowledge boundary and observe the narrower boundary on later advice.

## 5. Fresh-session and correction procedure

For every resumption pair, exit the first CLI without issuing a save/closing command.
Start a new CLI process using the normal launch commands, without resume/continue
flags or copied transcripts. Ask “What was I working on?” and a progress-dependent
question. Compare answers to the saved records, including scoped preferences.

For correction, establish a concrete recommendation, an enabled-follow-through
assumption about it, and a later plan that depends transitively on that assumption.
Say “I didn't do that; [reported correction].” Verify the old entry is superseded
or retracted, the correction is reported, affected assumptions/plans are reconsidered,
and revised guidance uses valid prerequisites. Reopen in the other host and verify
the correction survived. Success cannot be inferred from a proposed strategy.

## 6. Controlled persistence and capability failures

In disposable fixtures only, deny an actual pending write through host permissions,
or use a directory whose writes are demonstrably denied. Confirm an actual tool
error occurred; a conversational claim that saving failed is insufficient. Do not
relax the denial to let the coach finish the save. It must identify the unsaved
update and qualify future-session availability. Restore normal access after the
trial and verify the saved record did not secretly acquire the denied update.

For partial publication, permit a source/result save but deny the following finding
or registry write. Restart, inspect persisted substeps, and verify recovery reuses
valid content, avoids dangling evidence, and does not overwrite orphaned records.
Separately correct an assumption while unrelated research maintenance fails; the
playthrough correction must still be attempted and its actual save outcome reported.

For capability checks, run one observed relevant integration query if a suitable
integration is available, plus an unavailable/denied case. If no integration can
actually be queried, mark available-query coverage untested and validate fallback;
do not add a production dependency to manufacture coverage. Apply the same rule to
optional visuals. Mandatory text and unavailable-capability handling remain testable.

## 7. Evidence and acceptance report

For each trial record scenario/story/SC IDs, host and version, game/version context,
available tools, prompt transcript, relevant tool trace, before/after record snapshots,
setup-reply count where applicable, and `pass`, `fail`, or `untested` with reasons.
For factual trials include a claim-to-evidence ledger. For spoiler trials inspect
headings, labels, destinations, images, captions, and interactive states as applicable.
For human review retain anonymized usefulness ratings and redirection responses.

Report both host-level outcomes and aggregate thresholds. An unavailable capability,
missing host, source-display incompatibility, or missing human participants must be
visible in limitations and prevents claiming the corresponding full acceptance
coverage. A local file-validation pass alone never means the MVP is accepted.
