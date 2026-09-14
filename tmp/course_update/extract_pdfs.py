from pathlib import Path
from pypdf import PdfReader

sources = {
    "100行业": Path(r"D:\下载\表格\安先生短视频创作系统课程\100+行业爆款深度分析 .pdf"),
    "内部案例": Path(r"D:\下载\表格\安先生短视频创作系统课程\内部案例精选揭秘.pdf"),
    "百问百答": Path(r"D:\下载\表格\安先生短视频创作系统课程\亲爱的安先生短视频百问百答.pdf"),
    "内部案例拆解": Path(r"D:\下载\表格\安先生短视频创作系统课程\内部案例拆解-内页水印版.pdf"),
    "自媒体AI指南": Path(r"D:\下载\表格\安先生短视频创作系统课程\自媒体AI指南-内页水印版.pdf"),
}
output_dir = Path(__file__).parent / "pdf_text"
output_dir.mkdir(parents=True, exist_ok=True)

for short_name, source in sources.items():
    target = output_dir / f"{short_name}.txt"
    if target.exists() and target.stat().st_size > 0:
        print({"name": short_name, "status": "already_extracted", "target": str(target)})
        continue
    reader = PdfReader(str(source))
    pages = []
    nonempty = 0
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            nonempty += 1
        pages.append(f"\n\n===== PAGE {index} =====\n\n{text}")
    combined = "".join(pages)
    target.write_text(combined, encoding="utf-8")
    print({"name": short_name, "pages": len(reader.pages), "nonempty_pages": nonempty, "characters": len(combined), "target": str(target)})
