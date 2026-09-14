#!/usr/bin/env python3
"""只读扫描知识库目录，输出基础统计 JSON。"""

import argparse
import json
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    files = [p for p in root.rglob("*") if p.is_file()]
    extensions = Counter((p.suffix.lower() or "[无扩展名]") for p in files)
    unreadable = []
    total_size = 0
    for path in files:
        try:
            total_size += path.stat().st_size
            with path.open("rb") as stream:
                stream.read(1)
        except OSError:
            unreadable.append(str(path.relative_to(root)))
    result = {
        "root": str(root),
        "file_count": len(files),
        "directory_count": sum(1 for p in root.rglob("*") if p.is_dir()),
        "total_size_bytes": total_size,
        "extensions": dict(extensions.most_common()),
        "unreadable_files": unreadable,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
