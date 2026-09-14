#!/usr/bin/env python3
"""Read-only inventory for materials used by shengcai-topic-generator."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


EXCLUDED_FILENAMES = {"搜索关键词.md", "_入库检查报告.md"}
MISSING_VALUES = {"", "未提供", "未采集", "无", "暂无"}
TOPIC_POOL_RELATIVE_PATH = Path("04_选题库") / "选题池.md"


@dataclass
class ImageReference:
    reference: str
    relative_path: str
    absolute_path: str
    exists: bool


@dataclass
class Material:
    path: str
    title: str
    source_link: str
    material_id: str
    has_readable_body: bool
    missing_fields: list[str]
    is_valid: bool
    is_processed: bool
    image_references: list[ImageReference]


@dataclass
class TopicPool:
    path: str
    exists: bool
    has_read_section: bool
    format_error: bool
    topic_count: int
    max_topic_number: int
    read_material_count: int
    read_material_paths: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="盘点选题素材、有效性、增量状态和本地图片引用；不会修改任何文件。"
    )
    parser.add_argument(
        "--vault-root",
        default=".",
        help="Obsidian Vault 根目录，默认是当前目录。",
    )
    parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON。")
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8")


def normalized_relative(path: Path, root: Path) -> str:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        relative = path.resolve()
    return relative.as_posix()


def path_key(value: str) -> str:
    value = value.strip().strip("`\"'").replace("\\", "/")
    value = re.sub(r"^\./", "", value)
    return value.casefold()


def link_key(value: str) -> str:
    value = value.strip().strip("<>`\"'")
    value = value.rstrip(">)]}，,。；;")
    return value.casefold()


def is_missing(value: str) -> bool:
    return value.strip().strip("`\"'。；;：:") in MISSING_VALUES


def extract_title(text: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else ""


def extract_source_link(text: str) -> str:
    labeled = re.search(
        r"(?im)^\s*(?:-\s*)?(?:视频链接|笔记链接|来源链接)\s*[：:]\s*<?(https?://\S+)",
        text,
    )
    if labeled:
        return labeled.group(1).rstrip(">)]}，,。；;")
    generic = re.search(r"https?://[^\s<>]+", text)
    return generic.group(0).rstrip(">)]}，,。；;") if generic else ""


def extract_material_id(text: str, source_link: str, note_path: Path) -> str:
    labeled = re.search(
        r"(?im)^\s*(?:-\s*)?(?:视频ID|笔记ID|内容ID)\s*[：:]\s*([A-Za-z0-9_-]+)",
        text,
    )
    if labeled and not is_missing(labeled.group(1)):
        return labeled.group(1)
    from_link = re.search(r"/(?:video|note)/([A-Za-z0-9_-]+)", source_link)
    if from_link:
        return from_link.group(1)
    path_ids = re.findall(r"(?<!\d)(\d{10,})(?!\d)", note_path.as_posix())
    return path_ids[-1] if path_ids else ""


def extract_body(text: str) -> str:
    match = re.search(r"(?ms)^##\s+正文\s*$\s*(.*?)(?=^##\s+|\Z)", text)
    if not match:
        return ""
    body = match.group(1).strip()
    visible = re.sub(r"!\[\[[^\]]+\]\]", "", body)
    visible = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", visible)
    visible = re.sub(r"[`*_>#\-\s]", "", visible)
    return body if visible and not is_missing(visible) else ""


def clean_image_reference(raw: str) -> str:
    value = raw.strip().strip("<>")
    value = value.split("|", 1)[0].split("#", 1)[0].strip()
    return unquote(value)


def resolve_image_path(reference: str, note_path: Path, root: Path) -> Path:
    candidate = Path(reference.replace("/", "\\"))
    if candidate.is_absolute():
        return candidate.resolve()
    if reference.startswith("/"):
        return (root / reference.lstrip("/\\")).resolve()
    return (note_path.parent / candidate).resolve()


def extract_image_references(
    text: str, note_path: Path, root: Path
) -> list[ImageReference]:
    pattern = re.compile(r"!\[\[([^\]]+)\]\]|!\[[^\]]*\]\(([^)]+)\)")
    images: list[ImageReference] = []
    for match in pattern.finditer(text):
        raw = match.group(1) or match.group(2) or ""
        reference = clean_image_reference(raw)
        if not reference or re.match(r"(?i)^(?:https?://|data:)", reference):
            continue
        resolved = resolve_image_path(reference, note_path, root)
        images.append(
            ImageReference(
                reference=reference,
                relative_path=normalized_relative(resolved, root),
                absolute_path=str(resolved),
                exists=resolved.is_file(),
            )
        )
    return images


def candidate_markdown_files(material_root: Path) -> Iterable[Path]:
    for path in sorted(material_root.rglob("*.md"), key=lambda item: item.as_posix()):
        if path.name in EXCLUDED_FILENAMES or path.name.startswith("_"):
            continue
        yield path


def extract_read_section(text: str) -> tuple[bool, list[str]]:
    match = re.search(
        r"(?ms)^##\s+已读取素材\s*$\s*(.*?)(?=^##\s+|\Z)", text
    )
    if not match:
        return False, []
    paths: list[str] = []
    seen: set[str] = set()
    for item in re.finditer(r"(?m)^\s*-\s*`?(.+?\.md)`?\s*$", match.group(1)):
        raw_path = item.group(1).strip().strip("`\"'")
        if not path_key(raw_path).startswith("02_内容素材/"):
            continue
        key = path_key(raw_path)
        if key not in seen:
            paths.append(raw_path.replace("\\", "/"))
            seen.add(key)
    return True, paths


def load_topic_pool(
    pool_path: Path, root: Path
) -> tuple[TopicPool, set[str], set[str], set[str]]:
    if not pool_path.is_file():
        pool = TopicPool(
            path=normalized_relative(pool_path, root),
            exists=False,
            has_read_section=False,
            format_error=False,
            topic_count=0,
            max_topic_number=0,
            read_material_count=0,
            read_material_paths=[],
        )
        return pool, set(), set(), set()

    text = read_text(pool_path)
    topic_numbers = [
        int(value)
        for value in re.findall(r"(?m)^##\s+选题\s+(\d+)\s*[：:]", text)
    ]
    has_read_section, read_paths = extract_read_section(text)
    processed_paths = {path_key(value) for value in read_paths}
    processed_ids: set[str] = set()
    processed_links: set[str] = set()

    for raw_path in read_paths:
        processed_ids.update(re.findall(r"(?<!\d)(\d{10,})(?!\d)", raw_path))
        resolved = root / Path(raw_path.replace("/", "\\"))
        if not resolved.is_file():
            continue
        material_text = read_text(resolved)
        source_link = extract_source_link(material_text)
        material_id = extract_material_id(material_text, source_link, resolved)
        if source_link:
            processed_links.add(link_key(source_link))
        if material_id:
            processed_ids.add(material_id)

    pool = TopicPool(
        path=normalized_relative(pool_path, root),
        exists=True,
        has_read_section=has_read_section,
        format_error=not has_read_section,
        topic_count=len(topic_numbers),
        max_topic_number=max(topic_numbers, default=0),
        read_material_count=len(read_paths),
        read_material_paths=read_paths,
    )
    return pool, processed_paths, processed_ids, processed_links


def inspect_material(
    note_path: Path,
    root: Path,
    processed_paths: set[str],
    processed_ids: set[str],
    processed_links: set[str],
) -> Material:
    text = read_text(note_path)
    relative_path = normalized_relative(note_path, root)
    title = extract_title(text)
    source_link = extract_source_link(text)
    material_id = extract_material_id(text, source_link, note_path)
    body = extract_body(text)

    missing_fields: list[str] = []
    if not title or is_missing(title):
        missing_fields.append("标题")
    if not source_link or is_missing(source_link):
        missing_fields.append("来源链接")
    if not body:
        missing_fields.append("正文")

    is_processed = (
        path_key(relative_path) in processed_paths
        or bool(material_id and material_id in processed_ids)
        or bool(source_link and link_key(source_link) in processed_links)
    )
    return Material(
        path=relative_path,
        title=title or "未采集",
        source_link=source_link or "未采集",
        material_id=material_id or "未采集",
        has_readable_body=bool(body),
        missing_fields=missing_fields,
        is_valid=not missing_fields,
        is_processed=is_processed,
        image_references=extract_image_references(text, note_path, root),
    )


def main() -> int:
    args = parse_args()
    root = Path(args.vault_root).expanduser().resolve()
    material_root = root / "02_内容素材"
    if not material_root.is_dir():
        print(
            json.dumps(
                {
                    "error": "未找到 02_内容素材",
                    "vault_root": str(root),
                    "expected_path": str(material_root),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2

    pool_path = root / TOPIC_POOL_RELATIVE_PATH
    pool, processed_paths, processed_ids, processed_links = load_topic_pool(
        pool_path, root
    )
    materials = [
        inspect_material(
            path, root, processed_paths, processed_ids, processed_links
        )
        for path in candidate_markdown_files(material_root)
    ]
    valid = [material for material in materials if material.is_valid]
    invalid = [material for material in materials if not material.is_valid]
    processed = [material for material in valid if material.is_processed]
    new = [material for material in valid if not material.is_processed]
    image_reference_count = sum(len(item.image_references) for item in materials)
    missing_image_count = sum(
        not image.exists for item in materials for image in item.image_references
    )

    result = {
        "vault_root": str(root),
        "topic_pool": asdict(pool),
        "counts": {
            "candidate_count": len(materials),
            "valid_count": len(valid),
            "invalid_count": len(invalid),
            "processed_count": len(processed),
            "new_count": len(new),
            "image_reference_count": image_reference_count,
            "missing_image_count": missing_image_count,
        },
        "new_materials": [asdict(material) for material in new],
        "invalid_materials": [asdict(material) for material in invalid],
        "materials": [asdict(material) for material in materials],
    }
    indent = 2 if args.pretty else None
    print(json.dumps(result, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
