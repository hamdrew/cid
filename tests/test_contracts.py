"""Development-only record checks. These do not evaluate host coaching behavior."""
import json
import re
import tempfile
from copy import deepcopy
from datetime import datetime
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ContractError(ValueError):
    """An invalid record; callers must not silently repair it."""


def require(condition, message):
    if not condition:
        raise ContractError(message)


def string(value):
    require(isinstance(value, str) and bool(value.strip()), "expected nonempty string")


def ident(value):
    require(isinstance(value, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value), "unsafe ID")


def stamp(value):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", value), "timestamp must be full UTC Z")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ContractError("invalid timestamp") from exc


def strings(value, ids=False):
    require(isinstance(value, list), "expected array")
    for item in value:
        (ident if ids else string)(item)
    if ids:
        require(len(value) == len(set(value)), "duplicate IDs")


def fields(value, names):
    require(isinstance(value, dict), "expected object")
    require(set(names.split()) <= value.keys(), "missing fields: " + names)


def choice(value, values):
    require(value in values.split(), "invalid enum")


def common(d):
    fields(d, "schema_version revision updated_at")
    require(type(d["schema_version"]) is int and d["schema_version"] == 1, "unknown schema version")
    require(type(d["revision"]) is int and d["revision"] >= 0, "invalid revision")
    stamp(d["updated_at"])


def unique(items, key):
    require(isinstance(items, list), "expected array")
    found = set()
    for item in items:
        fields(item, key)
        ident(item[key])
        require(item[key] not in found, "duplicate " + key)
        found.add(item[key])


def preferences(p):
    require(isinstance(p, dict), "preferences object")
    allowed = {"spoiler_mode": "strict hints off", "follow_through": "enabled disabled",
               "research_depth": "brief normal thorough"}
    for key, item in p.items():
        # Additive unknown keys are preserved, but never interpreted by v1.
        if key not in (*allowed, "coaching_style"):
            continue
        fields(item, "value selected_at")
        stamp(item["selected_at"])
        if key == "coaching_style":
            string(item["value"])
        else:
            choice(item["value"], allowed[key])


def effective(key, workspace, game, playthrough):
    for owner in (playthrough, game, workspace):
        if key in owner.get("preferences", {}):
            return owner["preferences"][key]["value"]
    return {"spoiler_mode": "hints", "follow_through": None,
            "research_depth": "normal", "coaching_style": None}[key]


def applicability(a):
    fields(a, "notes")
    string(a["notes"])
    for key in ("editions", "platforms", "patches", "dlc", "mods"):
        if key in a:
            strings(a[key])


def reference(r, game_id=None, playthrough_id=None, research=False):
    fields(r, "game_id type id")
    ident(r["game_id"])
    ident(r["id"])
    choice(r["type"], "entry plan finding source integration")
    if game_id is not None:
        require(r["game_id"] == game_id, "cross-game dependency")
    if "playthrough_id" in r:
        ident(r["playthrough_id"])
    if r["type"] in ("entry", "plan"):
        fields(r, "playthrough_id")
        require(not research, "research depends on player state")
        if playthrough_id is not None:
            require(r["playthrough_id"] == playthrough_id, "cross-playthrough dependency")
    else:
        require("playthrough_id" not in r, "game reference has player scope")
    if r["type"] == "finding":
        fields(r, "topic_id")
        ident(r["topic_id"])


def refs(value, d, research=False):
    require(isinstance(value, list), "reference array")
    for r in value:
        reference(r, d["game_id"], d.get("playthrough_id"), research)


def acyclic(graph):
    visiting, done = set(), set()
    def visit(node):
        require(node not in visiting, "cyclic dependencies")
        if node in done:
            return
        visiting.add(node)
        for dep in graph.get(node, ()):
            require(dep in graph, "dangling dependency")
            visit(dep)
        visiting.remove(node)
        done.add(node)
    for node in graph:
        visit(node)


def validate_document(kind, d):
    common(d)
    if "preferences" in d:
        preferences(d["preferences"])
    if kind == "workspace":
        fields(d, "workspace_id games active preferences preference_prompts")
        ident(d["workspace_id"])
        unique(d["games"], "game_id")
        for item in d["games"]:
            fields(item, "label")
            string(item["label"])
        fields(d["preference_prompts"], "spoiler_modes_explained follow_through_offered")
        require(all(type(d["preference_prompts"][k]) is bool for k in
                    ("spoiler_modes_explained", "follow_through_offered")), "prompt flag boolean")
        if d["active"] is not None:
            fields(d["active"], "game_id playthrough_id")
            ident(d["active"]["game_id"])
            ident(d["active"]["playthrough_id"])
        return
    fields(d, "game_id")
    ident(d["game_id"])
    if kind == "game":
        fields(d, "title playthroughs topics")
        string(d["title"])
        if "identity_notes" in d:
            string(d["identity_notes"])
        unique(d["playthroughs"], "playthrough_id")
        for item in d["playthroughs"]:
            fields(item, "label")
            string(item["label"])
        strings(d["topics"], ids=True)
    elif kind == "playthrough":
        fields(d, "playthrough_id label context entries plans questions")
        ident(d["playthrough_id"])
        string(d["label"])
        require(isinstance(d["context"], dict), "context object")
        for k in ("edition", "platform", "patch"):
            if k in d["context"]:
                string(d["context"][k])
        for k in ("dlc", "mods"):
            if k in d["context"]:
                strings(d["context"][k])
        for collection in ("entries", "plans", "questions"):
            unique(d[collection], "id")
        for e in d["entries"]:
            fields(e, "topic statement kind status recorded_at depends_on")
            string(e["topic"])
            string(e["statement"])
            choice(e["kind"], "reported assumed")
            choice(e["status"], "current superseded retracted needs_review")
            stamp(e["recorded_at"])
            refs(e["depends_on"], d)
            if e["kind"] == "assumed":
                require(any(r["type"] == "plan" for r in e["depends_on"]), "assumption lacks originating plan")
        for p in d["plans"]:
            fields(p, "text status depends_on recorded_at reasoning_status")
            string(p["text"])
            choice(p["status"], "proposed accepted rejected completed_reported needs_review superseded")
            choice(p["reasoning_status"], "evidence_based untested_deduction")
            stamp(p["recorded_at"])
            refs(p["depends_on"], d)
        for q in d["questions"]:
            fields(q, "text status")
            string(q["text"])
            choice(q["status"], "open resolved")
        for collection, field in (("entries", "supersedes"), ("plans", "replaces")):
            ids = {i["id"] for i in d[collection]}
            graph = {i["id"]: [] for i in d[collection]}
            for i in d[collection]:
                if field in i:
                    ident(i[field])
                    require(i[field] in ids and i[field] != i["id"], "invalid replacement target")
                    graph[i["id"]].append(i[field])
            acyclic(graph)
    elif kind == "knowledge":
        fields(d, "topic_id findings")
        ident(d["topic_id"])
        unique(d["findings"], "id")
        for f in d["findings"]:
            fields(f, "statement kind status applicability evidence spoiler checked_at")
            string(f["statement"])
            choice(f["kind"], "fact sourced_strategy deduction")
            choice(f["status"], "supported needs_review disputed superseded")
            applicability(f["applicability"])
            stamp(f["checked_at"])
            fields(f["spoiler"], "sensitive")
            require(type(f["spoiler"]["sensitive"]) is bool, "spoiler boolean")
            if "boundary_notes" in f["spoiler"]:
                string(f["spoiler"]["boundary_notes"])
            require(isinstance(f["evidence"], list), "evidence array")
            if f["kind"] != "deduction":
                require(bool(f["evidence"]), "sourced claim needs accessed evidence")
            else:
                require(bool(f.get("derived_from")), "deduction needs premises")
            refs(f.get("derived_from", []), d, research=True)
            require(all(r["type"] == "finding" for r in f.get("derived_from", [])), "deduction premises must be findings")
            for e in f["evidence"]:
                fields(e, "source_id locator accessed_at summary")
                ident(e["source_id"])
                string(e["locator"])
                stamp(e["accessed_at"])
                string(e["summary"])
                if "integration_id" in e:
                    ident(e["integration_id"])
                    fields(e, "query")
                    fields(e["query"], "attempted_at outcome reference")
                    stamp(e["query"]["attempted_at"])
                    require(e["query"]["outcome"] == "success", "evidence query did not succeed")
                    string(e["query"]["reference"])
    elif kind == "sources":
        fields(d, "sources")
        unique(d["sources"], "id")
        for s in d["sources"]:
            fields(s, "locator title coverage applicability discovered_at access_status last_attempt_at last_success_at quality_notes")
            for k in ("locator", "title", "quality_notes"):
                string(s[k])
            strings(s["coverage"], ids=True)
            applicability(s["applicability"])
            stamp(s["discovered_at"])
            choice(s["access_status"], "never_accessed accessible failed requires_access")
            for k in ("last_attempt_at", "last_success_at"):
                if s[k] is not None:
                    stamp(s[k])
            if s["access_status"] == "never_accessed":
                require(s["last_attempt_at"] is None and s["last_success_at"] is None, "unaccessed source has access history")
            if s["access_status"] == "accessible":
                require(s["last_attempt_at"] is not None and s["last_success_at"] is not None, "accessible source lacks access")
            if s["access_status"] == "failed":
                require(s["last_attempt_at"] is not None, "failed source lacks attempt")
            if s["last_success_at"] is not None:
                require(s["last_attempt_at"] is not None and datetime.fromisoformat(s["last_success_at"].replace("Z", "+00:00")) <= datetime.fromisoformat(s["last_attempt_at"].replace("Z", "+00:00")), "success after last attempt")
            if "integration_id" in s:
                ident(s["integration_id"])
    elif kind == "integrations":
        fields(d, "integrations")
        unique(d["integrations"], "id")
        for i in d["integrations"]:
            fields(i, "name capabilities coverage access_requirements discovery_locator observations")
            for k in ("name", "access_requirements", "discovery_locator"):
                string(i[k])
            strings(i["capabilities"])
            strings(i["coverage"], ids=True)
            require(isinstance(i["observations"], list), "observations array")
            for o in i["observations"]:
                fields(o, "host checked_at availability reason")
                string(o["host"])
                stamp(o["checked_at"])
                choice(o["availability"], "available unavailable unknown")
                string(o["reason"])
                if "last_query" in o:
                    fields(o["last_query"], "attempted_at outcome reference")
                    stamp(o["last_query"]["attempted_at"])
                    choice(o["last_query"]["outcome"], "success failure")
                    string(o["last_query"]["reference"])
    else:
        raise ContractError("unknown document kind")


def validate_workspace(root):
    """Read-only validation; incomplete/orphaned publication is rejected for recovery."""
    root = Path(root).resolve()
    documents, nodes, graph = {}, {}, {}

    def read(relative, kind):
        path = root / relative
        require(path.resolve().is_relative_to(root), "path escapes workspace")
        try:
            d = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise ContractError("unreadable/corrupt record: " + relative) from exc
        validate_document(kind, d)
        documents[relative] = d
        return d

    def key(r):
        return (r["game_id"], r.get("playthrough_id"), r["type"], r.get("topic_id"), r["id"])

    def add(g, p, kind, item, topic=None, dependencies=()):
        k = (g, p, kind, topic, item["id"])
        require(k not in nodes, "duplicate scoped identity")
        nodes[k] = item
        graph[k] = [key(r) for r in dependencies]

    w = read(".cid/workspace.json", "workspace")
    games, runs = {}, set()
    for registration in w["games"]:
        gid = registration["game_id"]
        base = "games/" + gid + "/"
        g = read(base + "game.json", "game")
        require(g["game_id"] == gid, "game identity mismatch")
        require(g["title"] == registration["label"], "game label mismatch")
        games[gid] = g
        sources = read(base + "sources.json", "sources")
        ipath = root / (base + "integrations.json")
        integrations = read(base + "integrations.json", "integrations") if ipath.exists() else {"game_id": gid, "integrations": []}
        for d in (sources, integrations):
            require(d["game_id"] == gid, "index identity mismatch")
        for source in sources["sources"]:
            add(gid, None, "source", source)
        for integration in integrations["integrations"]:
            add(gid, None, "integration", integration)
        for topic in g["topics"]:
            d = read(base + "knowledge/" + topic + ".json", "knowledge")
            require(d["game_id"] == gid and d["topic_id"] == topic, "topic identity mismatch")
            for f in d["findings"]:
                add(gid, None, "finding", f, topic, f.get("derived_from", []))
        for registration in g["playthroughs"]:
            pid = registration["playthrough_id"]
            d = read(base + "playthroughs/" + pid + ".json", "playthrough")
            require(d["game_id"] == gid and d["playthrough_id"] == pid, "run identity mismatch")
            require(d["label"] == registration["label"], "run label mismatch")
            runs.add((gid, pid))
            for kind in ("entry", "plan"):
                for item in d[kind[:-1] + "ies" if kind == "entry" else "plans"]:
                    add(gid, pid, kind, item, dependencies=item["depends_on"])
    if w["active"] is not None:
        require((w["active"]["game_id"], w["active"]["playthrough_id"]) in runs, "invalid active pointer")
    for node, item in nodes.items():
        gid, _, kind, _, _ = node
        if kind == "finding":
            for e in item["evidence"]:
                source_key = (gid, None, "source", None, e["source_id"])
                require(source_key in nodes, "dangling evidence source")
                source = nodes[source_key]
                require(source["last_success_at"] is not None, "discovery is not accessed evidence")
                require(datetime.fromisoformat(e["accessed_at"].replace("Z", "+00:00")) <= datetime.fromisoformat(source["last_success_at"].replace("Z", "+00:00")), "evidence access after recorded success")
                if "integration_id" in source:
                    fields(e, "integration_id query")
                if "integration_id" in e:
                    integration = nodes.get((gid, None, "integration", None, e["integration_id"]))
                    require(integration is not None, "dangling evidence integration")
                    require(any(o.get("last_query") == e["query"] for o in integration["observations"]), "no observed successful evidence query")
                    require(source.get("integration_id") == e["integration_id"], "integration source mismatch")
        if kind == "source" and "integration_id" in item:
            require((gid, None, "integration", None, item["integration_id"]) in nodes, "dangling source integration")
    acyclic(graph)
    # Unregistered records are recovery candidates, never silently authoritative.
    actual = {str(p.relative_to(root)) for p in (root / "games").rglob("*.json")}
    expected = {path for path in documents if path.startswith("games/")}
    require(actual == expected, "unregistered/orphaned records require recovery")
    return documents


def fixture_documents(family="research", name="supported"):
    root = ROOT / "tests/fixtures/workspaces" / family / name
    return {str(p.relative_to(root)): json.loads(p.read_text()) for p in root.rglob("*.json")}


def check_snapshot(documents):
    with tempfile.TemporaryDirectory(prefix="cid-contract-") as temp:
        for relative, d in documents.items():
            path = Path(temp) / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(d))
        return validate_workspace(temp)


class TemplateTests(unittest.TestCase):
    def test_all_six_templates_are_present_objects(self):
        paths = [ROOT / "templates/workspace/.cid/workspace.json"] + [
            ROOT / "templates/records" / (name + ".json")
            for name in ("game", "playthrough", "knowledge", "sources", "integrations")]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file(), f"missing template: {path}")
                if path.is_file():
                    validate_document(path.stem, json.loads(path.read_text()))

class CommonContractTests(unittest.TestCase):
    def test_boolean_metadata_and_unknown_versions_are_rejected(self):
        for key, value in (("schema_version", True), ("schema_version", 2), ("revision", True), ("revision", -1)):
            d = {"schema_version": 1, "revision": 0, "updated_at": "2026-11-08T00:00:00Z"}
            d[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ContractError):
                common(d)

    def test_ids_cannot_inject_paths(self):
        for value in ("../a", "/a", "a/b", "A", "a..b", "a\\b", "", None):
            with self.subTest(value=value), self.assertRaises(ContractError):
                ident(value)

    def test_cycles_and_dangling_dependencies_rejected(self):
        acyclic({"a": [], "b": ["a"]})
        for graph in ({"a": ["a"]}, {"a": ["b"], "b": ["a"]}, {"a": ["missing"]}):
            with self.subTest(graph=graph), self.assertRaises(ContractError):
                acyclic(graph)

    def test_bad_common_fields_rejected(self):
        for d in ([], {}, {"schema_version": 1, "revision": 0, "updated_at": "yesterday"}):
            with self.subTest(d=d), self.assertRaises(ContractError):
                common(d)

class ResearchContractTests(unittest.TestCase):
    def test_complete_research_fixtures(self):
        for name in ("supported", "indexed-only", "conflicting", "patch-mismatch", "failed-access", "available-integration", "unavailable-integration", "deduction"):
            with self.subTest(name=name):
                validate_workspace(ROOT / "tests/fixtures/workspaces/research" / name)

    def test_facts_and_deductions_require_support(self):
        base = {"schema_version": 1, "revision": 0, "updated_at": "2026-11-08T00:00:00Z",
                "game_id": "synthetic-a", "topic_id": "mechanics", "findings": []}
        f = {"id": "finding-1", "statement": "Synthetic only", "kind": "fact", "status": "supported",
             "applicability": {"notes": "Unknown coverage"}, "evidence": [],
             "spoiler": {"sensitive": False}, "checked_at": "2026-11-08T00:00:00Z"}
        for kind in ("fact", "sourced_strategy", "deduction"):
            f["kind"] = kind
            with self.subTest(kind=kind), self.assertRaises(ContractError):
                validate_document("knowledge", base | {"findings": [f]})

    def test_applicability_and_reference_types(self):
        applicability({"notes": "Unknown; not universal"})
        for a in ({}, {"notes": "test", "patches": "all"}, {"notes": "test", "mods": [True]}):
            with self.subTest(a=a), self.assertRaises(ContractError):
                applicability(a)
        with self.assertRaises(ContractError):
            reference({"game_id": "a", "playthrough_id": "run-1", "type": "entry", "id": "e"}, "a", research=True)

class ResearchNegativeTests(unittest.TestCase):
    def test_invalid_research_items_rejected(self):
        documents = fixture_documents()
        cases = [
            ("knowledge", "kind", "guess"), ("knowledge", "status", "current"),
            ("knowledge", "evidence", []), ("knowledge", "spoiler", {}),
            ("knowledge", "spoiler", {"sensitive": 1}),
            ("knowledge", "applicability", {"notes": "unknown", "patches": "all"}),
            ("knowledge", "checked_at", None),
            ("sources", "access_status", "discovered"),
            ("sources", "last_attempt_at", None), ("sources", "last_success_at", None),
            ("sources", "quality_notes", None), ("sources", "coverage", "mechanics")]
        for kind, key, value in cases:
            d = deepcopy(documents[f"games/synthetic-a/{'knowledge/mechanics' if kind == 'knowledge' else 'sources'}.json"])
            d["findings" if kind == "knowledge" else "sources"][0][key] = value
            with self.subTest(kind=kind, key=key, value=value), self.assertRaises(ContractError):
                validate_document(kind, d)

    def test_discovery_cannot_support_a_claim(self):
        d = fixture_documents()
        d["games/synthetic-a/sources.json"]["sources"][0].update(
            access_status="never_accessed", last_success_at=None, last_attempt_at=None)
        with self.assertRaisesRegex(ContractError, "discovery"):
            check_snapshot(d)

    def test_successful_integration_evidence_must_match_observation(self):
        d = fixture_documents(name="available-integration")
        check_snapshot(d)
        for mutation in ("availability-only", "failed-query", "dangling-integration"):
            bad = deepcopy(d)
            observation = bad["games/synthetic-a/integrations.json"]["integrations"][0]["observations"][0]
            if mutation == "availability-only":
                del observation["last_query"]
            elif mutation == "failed-query":
                observation["last_query"]["outcome"] = "failure"
            else:
                bad["games/synthetic-a/integrations.json"]["integrations"] = []
            with self.subTest(mutation=mutation), self.assertRaises(ContractError):
                check_snapshot(bad)

    def test_invalid_integration_enums_and_query_shapes(self):
        base = fixture_documents(name="available-integration")["games/synthetic-a/integrations.json"]
        for key, value in (("availability", "installed"), ("checked_at", False), ("last_query", {}),
                           ("last_query", {"attempted_at": "2026-11-08T00:00:00Z", "outcome": "available", "reference": "r"})):
            d = deepcopy(base)
            d["integrations"][0]["observations"][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ContractError):
                validate_document("integrations", d)

    def test_finding_derivation_cycles_and_dangling_sources_rejected(self):
        base = fixture_documents(name="deduction")
        for mutation in ("cycle", "dangling-source", "cross-game", "missing-premise"):
            d = deepcopy(base)
            findings = d["games/synthetic-a/knowledge/mechanics.json"]["findings"]
            if mutation == "cycle":
                findings[0]["derived_from"] = [{"game_id": "synthetic-a", "type": "finding", "topic_id": "mechanics", "id": "finding-2"}]
            elif mutation == "dangling-source":
                findings[0]["evidence"][0]["source_id"] = "missing"
            elif mutation == "cross-game":
                findings[1]["derived_from"][0]["game_id"] = "other"
            else:
                findings[1]["derived_from"][0]["id"] = "missing"
            with self.subTest(mutation=mutation), self.assertRaises(ContractError):
                check_snapshot(d)

class ResumptionContractTests(unittest.TestCase):
    def test_complete_resumption_workspace(self):
        validate_workspace(ROOT / "tests/fixtures/workspaces/resumption/valid")

    def test_invalid_and_recovery_states_are_not_normally_valid(self):
        for name, reason in (("corrupt", "corrupt"), ("unknown-version", "unknown schema"),
                             ("invalid-pointer", "active pointer"), ("orphaned-record", "orphaned"),
                             ("partial-publication", "unreadable")):
            with self.subTest(name=name), self.assertRaisesRegex(ContractError, reason):
                validate_workspace(ROOT / "tests/fixtures/workspaces/resumption" / name)

    def test_scope_precedence_and_unset_defaults(self):
        w, g, p = {}, {}, {}
        self.assertEqual(effective("spoiler_mode", w, g, p), "hints")
        self.assertIsNone(effective("follow_through", w, g, p))
        ts = "2026-11-08T00:00:00Z"
        w["preferences"] = {"spoiler_mode": {"value": "off", "selected_at": ts}}
        g["preferences"] = {"spoiler_mode": {"value": "strict", "selected_at": ts}}
        p["preferences"] = {"spoiler_mode": {"value": "hints", "selected_at": ts}}
        self.assertEqual(effective("spoiler_mode", w, {}, {}), "off")
        self.assertEqual(effective("spoiler_mode", w, g, {}), "strict")
        self.assertEqual(effective("spoiler_mode", w, g, p), "hints")
        for value in ("yes", True, None):
            with self.subTest(value=value), self.assertRaises(ContractError):
                preferences({"follow_through": {"value": value, "selected_at": ts}})

    def test_omitted_context_differs_from_reported_none(self):
        d = fixture_documents()["games/synthetic-a/playthroughs/run-1.json"]
        d["context"] = {}
        validate_document("playthrough", d)
        self.assertNotIn("mods", d["context"])
        d["context"] = {"mods": [], "dlc": []}
        validate_document("playthrough", d)
        for context in ([], {"patch": True}, {"mods": "none"}):
            with self.subTest(context=context), self.assertRaises(ContractError):
                validate_document("playthrough", d | {"context": context})

    def test_registry_identity_duplicates_and_cross_run_dependencies(self):
        for mutation in ("duplicate-game", "duplicate-run", "identity", "cross-run", "bad-question"):
            d = fixture_documents()
            w = d[".cid/workspace.json"]
            g = d["games/synthetic-a/game.json"]
            p = d["games/synthetic-a/playthroughs/run-1.json"]
            if mutation == "duplicate-game": w["games"].append(deepcopy(w["games"][0]))
            elif mutation == "duplicate-run": g["playthroughs"].append(deepcopy(g["playthroughs"][0]))
            elif mutation == "identity": p["playthrough_id"] = "another"
            elif mutation == "cross-run": p["entries"][0]["depends_on"] = [{"game_id": "synthetic-a", "playthrough_id": "run-2", "type": "entry", "id": "goal-1"}]
            else: p["questions"] = [{"id": "q", "text": "Unknown?", "status": "maybe"}]
            with self.subTest(mutation=mutation), self.assertRaises(ContractError):
                check_snapshot(d)

class FollowThroughContractTests(unittest.TestCase):
    def test_complete_follow_through_snapshots(self):
        for name in ("initial", "assumed-chain", "corrected", "rejected", "disabled"):
            with self.subTest(name=name):
                validate_workspace(ROOT / "tests/fixtures/workspaces/follow-through" / name)

    def test_assumptions_need_originating_plans_and_valid_status(self):
        base = fixture_documents()["games/synthetic-a/playthroughs/run-1.json"]
        for mutation in ("missing-plan", "bad-entry-status", "bad-plan-status", "bad-supersedes", "bad-replaces"):
            d = deepcopy(base)
            if mutation == "missing-plan": d["entries"][0]["kind"] = "assumed"
            elif mutation == "bad-entry-status": d["entries"][0]["status"] = "accepted"
            elif mutation == "bad-supersedes": d["entries"][0]["supersedes"] = "missing"
            else:
                d["plans"] = [{"id": "plan-1", "text": "Synthetic proposal", "status": "proposed",
                               "reasoning_status": "untested_deduction", "recorded_at": "2026-11-08T00:00:00Z", "depends_on": []}]
                if mutation == "bad-plan-status": d["plans"][0]["status"] = "current"
                else: d["plans"][0]["replaces"] = "missing"
            with self.subTest(mutation=mutation), self.assertRaises(ContractError):
                validate_document("playthrough", d)

    def test_correction_retains_origin_and_transitive_review(self):
        before = fixture_documents("follow-through", "assumed-chain")["games/synthetic-a/playthroughs/run-1.json"]
        after = fixture_documents("follow-through", "corrected")["games/synthetic-a/playthroughs/run-1.json"]
        entries = {i["id"]: i for i in after["entries"]}
        plans = {i["id"]: i for i in after["plans"]}
        self.assertEqual(entries["attempt-1"]["status"], "retracted")
        self.assertEqual(entries["correction-1"]["kind"], "reported")
        self.assertEqual(entries["correction-1"]["supersedes"], "attempt-1")
        self.assertEqual(entries["attempt-2"]["status"], "needs_review")
        for id in ("plan-2", "plan-3"):
            self.assertEqual(plans[id]["status"], "needs_review")
        self.assertEqual(plans["plan-4"]["replaces"], "plan-3")
        self.assertEqual(entries["attempt-1"]["statement"], next(i["statement"] for i in before["entries"] if i["id"] == "attempt-1"))
        self.assertNotIn("completed_reported", [i["status"] for i in after["plans"]])
        self.assertGreater(after["revision"], before["revision"])

    def test_disabling_does_not_relabel_old_assumptions(self):
        d = fixture_documents("follow-through", "disabled")["games/synthetic-a/playthroughs/run-1.json"]
        self.assertEqual(d["preferences"]["follow_through"]["value"], "disabled")
        self.assertEqual(next(i for i in d["entries"] if i["id"] == "attempt-1")["kind"], "assumed")

class PresentationFixtureTests(unittest.TestCase):
    def test_spoiler_fixtures(self):
        for name in ("default", "strict-known", "hints", "off", "unknown-knowledge", "sensitive-sources", "assumed-outcome", "overrides"):
            with self.subTest(name=name):
                validate_workspace(ROOT / "tests/fixtures/workspaces/spoilers" / name)
        with self.assertRaises(ContractError):
            validate_workspace(ROOT / "tests/fixtures/workspaces/spoilers/unknown-metadata")

    def test_direction_fixtures(self):
        for name in ("contextual", "deduction", "material-question", "immaterial-question", "style"):
            with self.subTest(name=name):
                validate_workspace(ROOT / "tests/fixtures/workspaces/player-direction" / name)

class BoundaryTests(unittest.TestCase):
    def test_timestamps_require_full_utc_time(self):
        for value in ("2026-11-08Z", "2026-11-08T00:00Z", "2026-11-08T00:00:00+01:00Z", "2026-11-08T00:00:00Zjunk", "2026-13-08T00:00:00Z"):
            with self.subTest(value=value), self.assertRaises(ContractError):
                stamp(value)
        stamp("2026-11-08T00:00:00.123Z")

    def test_symlinks_cannot_escape_workspace(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as external:
            root = Path(temp)
            (root / ".cid").mkdir()
            outside = Path(external) / "workspace.json"
            outside.write_text(json.dumps(fixture_documents()[".cid/workspace.json"]))
            (root / ".cid/workspace.json").symlink_to(outside)
            with self.assertRaisesRegex(ContractError, "escapes"):
                validate_workspace(root)

class ReviewRegressionTests(unittest.TestCase):
    def test_integration_source_requires_query_provenance_on_each_evidence_item(self):
        d = fixture_documents(name="available-integration")
        e = d["games/synthetic-a/knowledge/mechanics.json"]["findings"][0]["evidence"][0]
        del e["integration_id"]
        del e["query"]
        del d["games/synthetic-a/integrations.json"]["integrations"][0]["observations"][0]["last_query"]
        with self.assertRaisesRegex(ContractError, "integration"):
            check_snapshot(d)

    def test_fractional_evidence_time_cannot_follow_source_success(self):
        d = fixture_documents()
        d["games/synthetic-a/knowledge/mechanics.json"]["findings"][0]["evidence"][0]["accessed_at"] = "2026-11-08T00:00:00.123Z"
        with self.assertRaisesRegex(ContractError, "after"):
            check_snapshot(d)

    def test_fractional_success_time_cannot_follow_attempt(self):
        d = fixture_documents()["games/synthetic-a/sources.json"]
        d["sources"][0]["last_success_at"] = "2026-11-08T00:00:00.123Z"
        with self.assertRaisesRegex(ContractError, "after"):
            validate_document("sources", d)

if __name__ == "__main__":
    unittest.main()
