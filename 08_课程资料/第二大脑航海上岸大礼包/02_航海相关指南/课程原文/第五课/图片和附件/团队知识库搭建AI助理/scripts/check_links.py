#!/usr/bin/env python3
"""检查 Markdown 相对链接和 Obsidian wikilink 的本地目标。"""

import argparse
import json
import re
from pathlib import Path

MD_LINK = re.compile(r"\[[^\]]*\]\((?!https?://|mailto:|#)([^)]+)\)")
WIKI_LINK = re.compile(r"\[\[([^]|#]+)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    names = {}
    for path in root.rglob("*"):
        if path.is_file():
            names.setdefault(path.stem, []).append(path)
    issues = []
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for target in MD_LINK.findall(text):
            target = target.split("#", 1)[0].strip("<>")
            if target and not (path.parent / target).exists():
                issues.append({"file": str(path.relative_to(root)), "target": target,
                               "type": "markdown"})
        for target in WIKI_LINK.findall(text):
            if target not in names:
                issues.append({"file": str(path.relative_to(root)), "target": target,
                               "type": "wikilink"})
    text = json.dumps({"broken_links": issues}, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
