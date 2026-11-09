# Contract test fixtures

These synthetic JSON snapshots support the model-free record contract tests in
`tests/test_contracts.py`. Some deliberately contain invalid or incomplete records
to exercise validation and recovery checks. They are not real game data.

The `game-understanding/` family contains synthetic workspaces only. `connected`
shows a supported overview and topic premises. `choices` shows run questions,
reported answers and an untested plan. `refreshed` separates two patches and
their advice. `partial` retains failed access and open questions when evidence
is unavailable. Assertions check record content and references. Useful
explanations, spoiler-safe replies and research adequacy require ordinary use.

The `research/wiki-api/` and `research/wiki-api-failed/` workspaces cover wiki
research through the official MediaWiki API. `wiki-api` has one wiki source read
through the API, with page-level evidence carrying `page_title` and `revision_id`.
`wiki-api-failed` records a later failure in `mediawiki.last_failure` while the
earlier success and its evidence are preserved. Both use `example.invalid`
addresses and contain no real wiki text. Their validity cannot show whether Cid
actually reads wikis politely or reports failures honestly; that requires
ordinary use.
