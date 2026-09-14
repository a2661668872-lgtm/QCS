#!/usr/bin/env python3
"""生成含 SHA-256 指纹的文件资产 CSV。"""

import argparse
import csv
import hashlib
from datetime import datetime
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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        stat = path.stat()
        rows.append({
            "文件路径": str(path.relative_to(root)),
            "文件名": path.name,
            "扩展名": path.suffix.lower(),
            "大小": stat.st_size,
            "修改时间": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            "SHA256": digest(path),
        })
    with args.output.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys() if rows else
                                ["文件路径", "文件名", "扩展名", "大小", "修改时间", "SHA256"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"已生成 {len(rows)} 条资产记录：{args.output}")


if __name__ == "__main__":
    main()
