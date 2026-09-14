#!/usr/bin/env python3
"""按文件内容指纹发现完全重复文件；只报告，不修改。"""

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    groups = defaultdict(list)
    for path in (p for p in root.rglob("*") if p.is_file()):
        groups[digest(path)].append(str(path.relative_to(root)))
    duplicates = [{"sha256": key, "files": value}
                  for key, value in groups.items() if len(value) > 1]
    text = json.dumps({"duplicate_groups": duplicates}, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
