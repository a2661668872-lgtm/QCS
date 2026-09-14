#!/usr/bin/env python3
"""Validate a knowledge-base directory against its approved structure blueprint."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("blueprint")
    parser.add_argument("--output")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    blueprint_path = Path(args.blueprint).expanduser().resolve()
    blueprint = json.loads(blueprint_path.read_text(encoding="utf-8"))
    errors = []
    warnings = []
    paths = {}
    ids = set()
    prefixes = defaultdict(list)

    for item in blueprint.get("directories", []):
        item_id = str(item.get("id", "")).strip()
        relative = str(item.get("path", "")).strip()
        normalized = Path(relative).as_posix().casefold()
        if not item_id or item_id in ids:
            errors.append(f"invalid or duplicate directory id: {item_id}")
        ids.add(item_id)
        if not relative or normalized in paths:
            errors.append(f"invalid or duplicate directory path: {relative}")
        paths[normalized] = item_id
        target = root / relative
        if item.get("required") is True and not target.is_dir():
            errors.append(f"missing required directory: {relative}")
        match = re.match(r"^(\d+)_", Path(relative).parts[0])
        if match:
            prefixes[match.group(1)].append(relative)

    for prefix, values in prefixes.items():
        if len(values) > 1:
            errors.append(f"duplicate top-level numeric prefix {prefix}: {', '.join(values)}")

    if root.is_dir():
        actual_prefixes = defaultdict(list)
        for path in root.iterdir():
            if path.is_dir():
                match = re.match(r"^(\d+)_", path.name)
                if match:
                    actual_prefixes[match.group(1)].append(path.name)
        for prefix, values in actual_prefixes.items():
            if len(values) > 1:
                errors.append(f"existing duplicate top-level numeric prefix {prefix}: {', '.join(values)}")
        unexpected = [
            path.name for path in root.iterdir()
            if path.is_dir() and path.name.casefold() not in paths
        ]
        if unexpected:
            warnings.append("directories outside approved blueprint: " + ", ".join(sorted(unexpected)))
    else:
        errors.append(f"knowledge-base root does not exist: {root}")

    report = {
        "root": str(root),
        "blueprint": str(blueprint_path),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
