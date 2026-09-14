#!/usr/bin/env python3
"""根据文件名中的日期和版本词发现候选版本组；结果需要人工确认。"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

VERSION = re.compile(r"(?i)(?:v(?:ersion)?\s*)?\d+(?:\.\d+){0,2}|20\d{2}[-_.年]?\d{0,2}")


def normalized(stem):
    return re.sub(r"[\s_\-（）()\[\]]+", "", VERSION.sub("", stem)).lower()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    groups = defaultdict(list)
    for path in (p for p in root.rglob("*") if p.is_file()):
        key = normalized(path.stem)
        if key:
            groups[key].append(str(path.relative_to(root)))
    candidates = [{"normalized_name": key, "files": value}
                  for key, value in groups.items() if len(value) > 1]
    text = json.dumps({"candidate_version_groups": candidates,
                       "warning": "仅为候选关系，不能据此判断权威版本。"},
                      ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
