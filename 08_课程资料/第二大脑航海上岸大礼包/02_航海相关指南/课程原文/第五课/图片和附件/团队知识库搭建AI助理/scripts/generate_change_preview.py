#!/usr/bin/env python3
"""比较两个目录并生成只读变更预览。"""

import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def index(root):
    return {str(p.relative_to(root)): digest(p)
            for p in root.rglob("*") if p.is_file()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("current", type=Path)
    parser.add_argument("proposed", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    current = index(args.current.resolve())
    proposed = index(args.proposed.resolve())
    result = {
        "create": sorted(proposed.keys() - current.keys()),
        "modify": sorted(k for k in proposed.keys() & current.keys()
                         if proposed[k] != current[k]),
        "remove_or_archive_candidate": sorted(current.keys() - proposed.keys()),
        "unchanged_count": sum(current[k] == proposed[k]
                               for k in current.keys() & proposed.keys()),
        "warning": "本报告不执行任何修改；删除项仅作为归档候选，必须人工确认。",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
