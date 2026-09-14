#!/usr/bin/env python3
"""Create a knowledge-base directory structure from an approved blueprint."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Approved knowledge-base root to create or extend")
    parser.add_argument("blueprint", help="Approved knowledge-base structure JSON")
    parser.add_argument("--report")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    blueprint_path = Path(args.blueprint).expanduser().resolve()
    blueprint = json.loads(blueprint_path.read_text(encoding="utf-8"))

    created = []
    reused = []
    errors = []
    seen_ids = set()
    seen_paths = set()
    prefixes = defaultdict(list)

    for item in blueprint.get("directories", []):
        item_id = str(item.get("id", "")).strip()
        relative = str(item.get("path", "")).strip()
        relative_path = Path(relative)
        if not item_id or item_id in seen_ids:
            errors.append(f"invalid or duplicate directory id: {item_id}")
            continue
        if not relative or relative_path.is_absolute() or ".." in relative_path.parts:
            errors.append(f"unsafe directory path: {relative}")
            continue
        normalized = relative_path.as_posix().casefold()
        if normalized in seen_paths:
            errors.append(f"duplicate directory path: {relative}")
            continue
        seen_ids.add(item_id)
        seen_paths.add(normalized)
        match = re.match(r"^(\d+)_", relative_path.parts[0])
        if match:
            prefixes[match.group(1)].append(relative)

    for prefix, values in prefixes.items():
        if len(values) > 1:
            errors.append(f"duplicate top-level numeric prefix {prefix}: {', '.join(values)}")

    if not errors:
        root.mkdir(parents=True, exist_ok=True)
        for item in blueprint.get("directories", []):
            target = root / str(item["path"])
            if target.exists() and not target.is_dir():
                errors.append(f"path exists but is not a directory: {target}")
            elif target.exists():
                reused.append(str(target))
            else:
                target.mkdir(parents=True)
                created.append(str(target))

    report = {
        "root": str(root),
        "blueprint": str(blueprint_path),
        "created": created,
        "reused": reused,
        "errors": errors,
        "valid": not errors,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        output = Path(args.report).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
