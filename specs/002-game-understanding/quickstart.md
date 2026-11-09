# Quickstart: Game understanding validation

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md)

**Implementation status**: Shared policy and synthetic record examples implemented.
The
[pass contract](contracts/game-understanding.md) defines behavior and bounds;
[data-model.md](data-model.md#game-understanding-in-existing-v1-records) defines
where the outputs belong.

### Prerequisites and setup

For model-free checks, use Python 3.11+ and the repository checkout; no packages or
model access are needed. Run from the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: the existing record/template/reference checks and focused synthetic
record cases pass. They validate record compatibility. The quality of explanations
and advice requires ordinary-use observation.

To check just existing research and resumption contracts:

```sh
PYTHONPATH=tests python3 -m unittest test_contracts.ResearchContractTests test_contracts.ResearchNegativeTests test_contracts.ResumptionContractTests -v
```

Expected: valid supported findings and run records are accepted; unsupported,
cross-game, dangling and cyclic evidence/dependency states are rejected. These
commands do not research a game, invoke a model or change player records.

For ordinary use, the owner can follow the [setup instructions](../../README.md#set-up-once)
and later [merge a policy update](../../README.md#existing-workspaces-and-updates).
When installing the updated policy, preserve workspace identity,
preferences and `games/`. Never copy empty templates over existing records.
Only the owner starts or uses a coaching host; development agents must not launch
one to run the examples below.

### Model-free implementation baseline

`python3 -m unittest discover -s tests -p 'test_*.py' -v` passed all 29
tests against the unchanged suite. No pre-existing test failures were observed.
This run established record and template compatibility before the change.
Coaching behavior requires ordinary-use observation.

### Optional end-to-end observations during normal use

These examples are selectable, not a campaign or required checklist. Use your
normal host and game; no fixed trial count, transcript or cross-host matrix is needed.

| Ordinary request or situation | Expected reply and persisted evidence |
| --- | --- |
| Introduce a game and current quest for ongoing coaching | Research explains loop/progression and actual systems relationships; questions distinguish readiness/goals rather than only asking where you are; topic findings and overview save substantive evidence and explicit limits |
| Discuss an open goal or ask why one approach fits | Explain concrete costs/benefits and useful options beyond quest advancement where relevant; sourced strategy and material untested reasoning remain distinct |
| Start a fresh conversation about the same game | Read saved overview/relevant topics and run context; avoid re-fetching adequate unchanged sources or repeating answered questions |
| Ask for a quick answer or decline a question | Give narrower supported/conditional help, retain material gaps and honor the limit; do not force the full pass or change a lasting preference without a request |
| Return to a deferred topic, or set an explicit restriction for the run | Research a later relevant request after a temporary deferral. Reload a lasting run restriction and clarify a request that appears to cross it. |
| Play a game without character builds or a fixed progression path | Use the game's actual choice systems and distinguish what persists from whether progression is linear. |
| Use a different patch in another run, or encounter conflicting evidence | Reassess applicability and dependent plans for the selected run. Retain supported findings within their verified coverage and reopen shared claims when evidence undermines that coverage. |
| Set a lasting workspace or game topic restriction, then start a fresh conversation or another run | Load the restriction from its owning JSON record; narrower empty lists do not lift it, and only an explicit change removes it. This behavior remains an optional owner observation. |
| Have uncertain progress or strict spoiler boundaries | Broad understanding, questions and output avoid protected discoveries and revealing labels; a partial pass is allowed |

If useful, inspect saved `game.json.topics`, topic statements/evidence/limits,
overview premises and selected-run questions/plans. A fluent reply, generic facts,
links alone or an “overview complete” assertion does not establish success. Failure
to save must identify the specific unpersisted content. See the contract rather
than inventing a category/source quota to judge adequacy.

Send bullet points about what was useful or missing. You may explicitly request
review of a transcript/workspace in this conversation; no extra model calls or
review agents may be launched for that review. Unobserved behavior remains unknown.

### Implementation verification

| Command | Result |
| --- | --- |
| `python3 -B -m unittest discover -s tests -p 'test_*.py' -q` | 39 passed, including ten focused game-understanding checks and all four new workspaces |
| `PYTHONPATH=tests python3 -m unittest test_contracts.ResearchContractTests test_contracts.ResearchNegativeTests test_contracts.ResumptionContractTests -v` | 13 passed |
| `python3 /tmp/cid-002-check-links.py` | A temporary local script checked relative Markdown paths and heading fragments. All 30 references across eight changed Markdown files resolved. |
| `git diff --check` | No whitespace errors |
| `git diff --exit-code -- specs/001-ai-game-coach adapters templates` | Baseline history, host adapters and empty templates unchanged |

The full suite resolves the new fixtures' registry, evidence, derivation and
plan references and rejects the deliberately invalid variants. The existing
v1 validators now check optional workspace/game `research_restrictions` string
arrays and reject supported deductions with non-supported premises. Review-state
and historical deductions retain their references. Regression cases failed before
the validator fixes and passed afterward. Older v1 records remain valid.

### Specification and constitution review

| Requirements | Policy and record coverage |
| --- | --- |
| FR-001–FR-003, SC-001 | The policy scopes broad research to the actual loop and main relationships, separating persistence from a fixed progression path. The connected fixture retains sourced loop and checkpoint rules plus a cross-topic deduction. |
| FR-004–FR-006, SC-002 | The policy ties brief, skippable questions and concrete tradeoffs to the player's decision. The choices fixture separates the reported answer, optional sourced preparation and untested plan. |
| FR-007–FR-009, SC-004 | v1 findings retain explanations, evidence or premises, applicability and explicit gaps. Partial coverage can live on a topic or, with no supported findings, in run questions and actual access observations. |
| FR-010–FR-012, SC-005 | Stopping rules cover adequate and early partial outcomes. Quick requests and temporary deferrals narrow the work. Explicitly lasting run limits are represented as reported constraints. |
| FR-013–FR-014, SC-003 and SC-006 | The policy looks up applicable overview content and reassesses affected dependencies before reuse. Two-patch and same-coverage conflict cases preserve evidence, unaffected progress and preferences. |
| FR-015 | The evidence sequence, spoiler modes, preference precedence and correction rules are retained. Verified saves and targeted recovery cover topic registration, overview publication and dependent plans. |

The policy and records were reviewed against constitution principles I–V.
Evidence and applicability remain attached to claims. Shared research stays
separate from durable, correctable run context. Spoiler protection covers
questions, source labels and destinations as well as explanations and visuals.
Research scope, questions and advice remain player-directed. The review fixes retain lasting restrictions at workspace/game scope in optional
JSON arrays rather than narrowing them to one conversation. Run restrictions
remain reported constraints. Deterministic checks establish record retention and
shape validation; cross-session enforcement remains unobserved.

Conversational outcomes remain unobserved, including the usefulness of
explanations, questions and tradeoffs, spoiler-safe disclosure under actual host
citation rules, selective reuse in a fresh conversation and the quality of
partial-stop replies. Record validation establishes representation and
reference integrity for the tested cases. No coaching host, model API,
automated player or review agent was used.
