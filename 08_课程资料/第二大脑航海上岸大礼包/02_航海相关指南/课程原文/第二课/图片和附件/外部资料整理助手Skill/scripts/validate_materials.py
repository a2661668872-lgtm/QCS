#!/usr/bin/env python3
"""Validate required frontmatter fields in Markdown material cards."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED = [
    "material_id", "record_kind", "title", "type", "status", "created", "summary",
    "source_ids", "applicable_scenarios", "related_tools", "target_users",
    "timeliness", "verification_status", "keywords",
]


def frontmatter(text: str) -> dict[str, str] | None:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if not match:
        return None
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("--output")
    parser.add_argument("--expected-count", type=int)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    results = []
    unrecognized = []
    ids = {}
    for path in root.rglob("*.md"):
        data = frontmatter(path.read_text(encoding="utf-8-sig"))
        if not data or data.get("record_kind") != "atomic_material" or "material_id" not in data:
            unrecognized.append(str(path))
            continue
        if data["material_id"].startswith("MAT-X"):
            continue
        missing = [field for field in REQUIRED if not data.get(field)]
        material_id = data["material_id"]
        ids.setdefault(material_id, []).append(str(path))
        results.append({"path": str(path), "material_id": material_id, "missing": missing})
    duplicates = {key: value for key, value in ids.items() if len(value) > 1}
    report = {
        "material_count": len(results),
        "markdown_file_count": len(results) + len(unrecognized),
        "unrecognized_files": unrecognized,
        "incomplete": [item for item in results if item["missing"]],
        "duplicate_ids": duplicates,
        "expected_count": args.expected_count,
        "valid": (
            not duplicates
            and not unrecognized
            and not any(item["missing"] for item in results)
            and (args.expected_count is None or len(results) == args.expected_count)
        ),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).resolve().write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
