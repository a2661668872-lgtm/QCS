#!/usr/bin/env python3
"""Run a lightweight keyword, vocabulary-expansion and metadata retrieval test."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_json(path: str) -> object:
    return json.loads(Path(path).resolve().read_text(encoding="utf-8"))


def expand(query: str, vocabulary: dict) -> list[str]:
    terms = {part for part in re.split(r"[\s,，。？、]+", query) if len(part) >= 2}
    for concept, rules in vocabulary.get("concepts", {}).items():
        candidates = [concept]
        for key in ("strict_synonyms", "user_expressions", "related_terms"):
            candidates.extend(rules.get(key, []))
        if any(value.lower() in query.lower() for value in candidates):
            terms.update(candidates)
    for phrase, intent_terms in vocabulary.get("intents", {}).items():
        if phrase.lower() in query.lower():
            terms.update(intent_terms)
    return sorted(terms)


def score(material: dict, terms: list[str]) -> int:
    title = str(material.get("title", ""))
    body = str(material.get("body", ""))
    metadata = json.dumps(material.get("metadata", {}), ensure_ascii=False)
    total = 0
    for term in terms:
        escaped = re.escape(term)
        total += len(re.findall(escaped, title, flags=re.I)) * 3
        total += len(re.findall(escaped, body, flags=re.I))
        total += len(re.findall(escaped, metadata, flags=re.I)) * 4
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--materials", required=True, help="JSON array with id/title/body/metadata")
    parser.add_argument("--tests", required=True, help="JSON array with id/query/expected_ids")
    parser.add_argument("--vocabulary", required=True, help="Vocabulary JSON")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output")
    args = parser.parse_args()

    materials = load_json(args.materials)
    tests = load_json(args.tests)
    vocabulary = load_json(args.vocabulary)
    results = []
    expected_total = recalled_total = 0
    for test in tests:
        terms = expand(test["query"], vocabulary)
        ranked = sorted(
            (
                {"id": item["id"], "score": score(item, terms)}
                for item in materials
            ),
            key=lambda item: item["score"],
            reverse=True,
        )
        ranked = [item for item in ranked if item["score"] > 0][: args.top_k]
        found = {item["id"] for item in ranked}
        expected = set(test.get("expected_ids", []))
        recalled = len(found & expected)
        expected_total += len(expected)
        recalled_total += recalled
        results.append({
            "id": test["id"],
            "query": test["query"],
            "expanded_terms": terms,
            "expected_ids": sorted(expected),
            "results": ranked,
            "recalled": recalled,
        })
    report = {
        "expected_total": expected_total,
        "recalled_total": recalled_total,
        "recall": recalled_total / expected_total if expected_total else 0,
        "tests": results,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).resolve().write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

