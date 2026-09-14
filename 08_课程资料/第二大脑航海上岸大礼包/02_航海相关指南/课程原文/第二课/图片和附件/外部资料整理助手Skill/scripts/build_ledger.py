#!/usr/bin/env python3
"""Build a generic source ledger from an inventory JSON."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


TYPE_MAP = {
    ".md": "markdown",
    ".txt": "text",
    ".pdf": "pdf",
    ".ppt": "presentation",
    ".pptx": "presentation",
    ".doc": "document",
    ".docx": "document",
    ".xls": "spreadsheet",
    ".xlsx": "spreadsheet",
    ".csv": "spreadsheet",
    ".mp3": "audio",
    ".wav": "audio",
    ".m4a": "audio",
    ".mp4": "video",
    ".mov": "video",
    ".mkv": "video",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory")
    parser.add_argument("--output", required=True)
    parser.add_argument("--purpose", default="")
    args = parser.parse_args()

    inventory = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    sources = []
    for index, item in enumerate(inventory.get("items", []), start=1):
        sources.append({
            "source_id": f"SRC-{index:05d}",
            "source_title": item.get("name", ""),
            "source_location": item.get("path", ""),
            "source_type": TYPE_MAP.get(item.get("extension", ""), "other"),
            "processing_status": "discovered",
            "purpose_value": "",
            "content_fingerprint": item.get("content_fingerprint", ""),
            "last_scanned_at": inventory.get("generated_at", ""),
            "last_processed_at": "",
            "generated_materials": [],
            "timeliness": "unknown",
            "verification_status": "unverified",
            "unprocessed_reason": "",
        })
    ledger = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": args.purpose,
        "sources": sources,
    }
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Ledger written: {output}; sources: {len(sources)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

