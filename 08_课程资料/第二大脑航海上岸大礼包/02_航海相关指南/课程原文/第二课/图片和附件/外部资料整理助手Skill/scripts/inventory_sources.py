#!/usr/bin/env python3
"""Create a read-only inventory for one or more user-approved roots."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_EXCLUDES = {
    ".git", ".svn", ".hg", "node_modules", "__pycache__", ".venv", "venv",
    "$recycle.bin", "system volume information", "appdata", ".cache",
}


def scan(roots: list[Path], max_files: int, excludes: set[str]) -> dict:
    items = []
    errors = []
    type_counts: Counter[str] = Counter()
    directory_counts: Counter[str] = Counter()
    truncated = False

    for root in roots:
        if not root.exists():
            errors.append({"path": str(root), "reason": "not_found"})
            continue
        for current, dirnames, filenames in os.walk(root):
            dirnames[:] = [
                name for name in dirnames
                if name.lower() not in excludes and not name.startswith(".tmp")
            ]
            for name in filenames:
                path = Path(current) / name
                try:
                    stat = path.stat()
                except OSError as exc:
                    errors.append({"path": str(path), "reason": str(exc)})
                    continue
                suffix = path.suffix.lower() or "[no-extension]"
                item = {
                    "path": str(path),
                    "name": name,
                    "extension": suffix,
                    "size_bytes": stat.st_size,
                    "modified_at": datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(),
                }
                items.append(item)
                type_counts[suffix] += 1
                directory_counts[str(path.parent)] += 1
                if len(items) >= max_files:
                    truncated = True
                    break
            if truncated:
                break
        if truncated:
            break

    return {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "roots": [str(root) for root in roots],
        "file_count": len(items),
        "truncated": truncated,
        "type_counts": dict(type_counts.most_common()),
        "top_directories": [
            {"path": path, "file_count": count}
            for path, count in directory_counts.most_common(30)
        ],
        "items": items,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", help="User-approved directories to scan")
    parser.add_argument("--output", required=True, help="Output inventory JSON")
    parser.add_argument("--max-files", type=int, default=50000)
    parser.add_argument("--exclude", action="append", default=[])
    args = parser.parse_args()

    roots = [Path(value).expanduser().resolve() for value in args.roots]
    excludes = DEFAULT_EXCLUDES | {value.lower() for value in args.exclude}
    result = scan(roots, args.max_files, excludes)
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Inventory written: {output}")
    print(f"Files: {result['file_count']}; truncated: {result['truncated']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

