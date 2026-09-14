from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader


SOURCE = Path(r"D:\下载\BaiduNetdiskDownload\资料包")
OUTPUT = Path(r"D:\工作空间\Obsidian\AI第二大脑\AI第二大脑_内容创作系统\tmp\pdfs\安先生课件文本")

KANGXI_FORMS = (
    "一丨丶丿乙亅二亠人儿入八冂冖冫几凵刀力勹匕匚匸十卜卩厂厶又口囗土士夂夊夕大女子宀寸小尢尸屮山巛工己巾干幺广廴廾弋弓彐彡彳"
    "心戈戶手支攴文斗斤方无日曰月木欠止歹殳毋比毛氏气水火爪父爻爿片牙牛犬玄玉瓜瓦甘生用田疋疒癶白皮皿目矛矢石示禸禾穴立竹米"
    "糸缶网羊羽老而耒耳聿肉臣自至臼舌舛舟艮色艸虍虫血行衣襾見角言谷豆豕豸貝赤走足身車辛辰辵邑酉釆里金長門阜隶隹雨靑非面革韋"
    "韭音頁風飛食首香馬骨高髟鬥鬯鬲鬼魚鳥鹵鹿麥麻黃黍黑黹黽鼎鼓鼠鼻齊齒龍龜龠"
)
KANGXI_MAP = {chr(0x2F00 + i): char for i, char in enumerate(KANGXI_FORMS)}


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans(KANGXI_MAP))
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for pdf_path in sorted(SOURCE.glob("*.pdf")):
        reader = PdfReader(pdf_path)
        pages = []
        total_chars = 0
        nonempty_pages = 0
        for page_number, page in enumerate(reader.pages, start=1):
            try:
                text = normalize_text(page.extract_text() or "")
            except Exception as exc:
                text = f"[提取失败：{exc}]"
            if text:
                nonempty_pages += 1
                total_chars += len(text)
            pages.append(f"--- PAGE {page_number} ---\n{text}\n")
        output_path = OUTPUT / f"{pdf_path.stem}.txt"
        output_path.write_text("\n".join(pages), encoding="utf-8")
        manifest.append(
            {
                "file": pdf_path.name,
                "pages": len(reader.pages),
                "nonempty_pages": nonempty_pages,
                "characters": total_chars,
                "text_file": str(output_path),
            }
        )
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
