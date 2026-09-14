#!/usr/bin/env python3
"""检查 Markdown YAML 前置信息中的必填字段；只报告，不修改。"""

import argparse
import json
from pathlib import Path

REQUIRED = [
    "knowledge_id", "title", "knowledge_type", "business_domain",
    "applicable_users", "applicable_scenarios", "source_documents",
    "version", "effective_date", "review_date", "content_owner",
    "reviewer", "confidentiality", "status",
]


def frontmatter_keys(text):
    if not text.startswith("---"):
        return set()
    parts = text.split("---", 2)
    if len(parts) < 3:
        return set()
    keys = set()
    for line in parts[1].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            keys.add(line.split(":", 1)[0].strip())
    return keys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    issues = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        keys = frontmatter_keys(text)
        missing = [key for key in REQUIRED if key not in keys]
        if missing:
            issues.append({"file": str(path.relative_to(root)), "missing": missing})
    result = {"checked_markdown": len(list(root.rglob("*.md"))), "issues": issues}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
