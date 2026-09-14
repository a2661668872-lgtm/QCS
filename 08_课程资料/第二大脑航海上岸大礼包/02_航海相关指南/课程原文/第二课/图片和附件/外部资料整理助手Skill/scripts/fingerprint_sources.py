#!/usr/bin/env python3
"""Add SHA-256 fingerprints to a source inventory without modifying sources."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def fingerprint(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", help="Inventory JSON from inventory_sources.py")
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-size-mb", type=int, default=512)
    args = parser.parse_args()

    source = Path(args.inventory).resolve()
    data = json.loads(source.read_text(encoding="utf-8"))
    limit = args.max_size_mb * 1024 * 1024
    for item in data.get("items", []):
        path = Path(item["path"])
        if item.get("size_bytes", 0) > limit:
            item["fingerprint_status"] = "skipped_size_limit"
            continue
        try:
            item["content_fingerprint"] = fingerprint(path)
            item["fingerprint_status"] = "ok"
        except OSError as exc:
            item["fingerprint_status"] = "error"
            item["fingerprint_error"] = str(exc)

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fingerprint inventory written: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

