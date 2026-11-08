# Quickstart: Game understanding validation

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md)

**Design status**: Planned expansion. These are validation instructions, not
evidence that the new behavior has been implemented or observed. The
[pass contract](contracts/game-understanding.md) defines behavior and bounds;
[data-model.md](data-model.md#game-understanding-in-existing-v1-records) defines
where the outputs belong.

### Prerequisites and setup

For model-free checks, use Python 3.11+ and the repository checkout; no packages or
model access are needed. Run from the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: the existing record/template/reference checks pass. During implementation,
extend them only with focused synthetic record cases for this design. They validate
record compatibility, not the quality of a mental model or any host conversation.

To check just existing research and resumption contracts:

```sh
PYTHONPATH=tests python3 -m unittest test_contracts.ResearchContractTests test_contracts.ResearchNegativeTests test_contracts.ResumptionContractTests -v
```

Expected: valid supported findings and run records are accepted; unsupported,
cross-game, dangling and cyclic evidence/dependency states are rejected. These
commands do not research a game, invoke a model or change player records.

For ordinary use, the owner can follow the [setup instructions](../../README.md#set-up-once)
and later [merge a policy update](../../README.md#existing-workspaces-and-updates).
Update the installed policy after implementation; preserve workspace identity,
preferences and `games/`. Never copy empty templates over existing records.
Only the owner starts or uses a coaching host; development agents must not launch
one to run the examples below.

### Optional end-to-end observations during normal use

These examples are selectable, not a campaign or required checklist. Use your
normal host and game; no fixed trial count, transcript or cross-host matrix is needed.

| Ordinary request or situation | Expected reply and persisted evidence |
| --- | --- |
| Introduce a game and current quest for ongoing coaching | Research explains loop/progression and actual systems relationships; questions distinguish readiness/goals rather than only asking where you are; topic findings and overview save substantive evidence and explicit limits |
| Discuss an open goal or ask why one approach fits | Explain concrete costs/benefits and useful options beyond quest advancement where relevant; sourced strategy and material untested reasoning remain distinct |
| Start a fresh conversation about the same game | Read saved overview/relevant topics and run context; avoid re-fetching adequate unchanged sources or repeating answered questions |
| Ask for a quick answer or decline a question | Give narrower supported/conditional help, retain material gaps and honor the limit; do not force the full pass or change a lasting preference without a request |
| Play a game without character builds or quest progression | Research and questions use its actual choice systems; no invented RPG categories or mandatory stat sheet |
| Encounter changed version or conflicting evidence | Reassess affected findings, derived overview and plans before reuse; keep unaffected knowledge, source history, preferences and progress |
| Have uncertain progress or strict spoiler boundaries | Broad understanding, questions and output avoid protected discoveries and revealing labels; a partial pass is allowed |

If useful, inspect saved `game.json.topics`, topic statements/evidence/limits,
overview premises and selected-run questions/plans. A fluent reply, generic facts,
links alone or an “overview complete” assertion does not establish success. Failure
to save must identify the specific unpersisted content. See the contract rather
than inventing a category/source quota to judge adequacy.

Send bullet points about what was useful or missing. You may explicitly request
review of a transcript/workspace in this conversation; no extra model calls or
review agents may be launched for that review. Unobserved behavior remains unknown.
