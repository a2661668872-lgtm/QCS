import fs from "node:fs";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const vaultRoot = "D:/工作空间/Obsidian/AI第二大脑/AI第二大脑_内容创作系统";
const sourcePath = "D:/下载/表格/【安先生：新媒体导演课3.0版】65节.xlsx";
const outputRoot = path.join(vaultRoot, "01_学习对象", "安先生", "新增课程逐字稿");
const input = await FileBlob.load(sourcePath);
const workbook = await SpreadsheetFile.importXlsx(input);
const sheet = workbook.worksheets.getItem("Sheet1");
const rows = sheet.getRange("A68:B96").values;

const groupForRow = (row) => {
  if (row >= 69 && row <= 83) return "文案与创作系统课-15节";
  if (row >= 85 && row <= 87) return "内容时代的全域获客课-2026-01";
  if (row >= 89 && row <= 91) return "AI驱动的全域增长实战课-2026-03-12至03-14";
  if (row >= 93 && row <= 96) return "内容时代的全域获客课-2026-02-26至03-01";
  return null;
};
const cleanTitle = (raw) => String(raw ?? "")
  .replace(/[-_ ]*ev[-_ ]*笔记\s*$/iu, "")
  .replace(/[-_ ]*笔记\s*$/u, "")
  .replace(/[-_ ]*ev[-_ ]*$/iu, "")
  .trim();
const safeFilename = (title) => title.replace(/[<>:"/\\|?*]/g, "-").replace(/\s+/g, " ").trim();

fs.mkdirSync(outputRoot, { recursive: true });
const records = [];
let ordinal = 0;
for (let index = 0; index < rows.length; index += 1) {
  const sourceRow = index + 68;
  const group = groupForRow(sourceRow);
  const rawTitle = String(rows[index]?.[0] ?? "").trim();
  const transcript = String(rows[index]?.[1] ?? "").replace(/\r\n/g, "\n").trim();
  if (!group || !transcript) continue;
  ordinal += 1;
  const title = cleanTitle(rawTitle);
  const groupDir = path.join(outputRoot, group);
  fs.mkdirSync(groupDir, { recursive: true });
  const fileName = `${String(ordinal).padStart(3, "0")}-${safeFilename(title)}.md`;
  const absolutePath = path.join(groupDir, fileName);
  const relativePath = path.relative(vaultRoot, absolutePath).replace(/\\/g, "/");
  const atLimit = transcript.length >= 32767;
  const content = [
    "---",
    `课程组: "${group}"`,
    `表格行号: ${sourceRow}`,
    `原始课题: "${rawTitle.replace(/"/g, "\\\"")}"`,
    `正文字符数: ${transcript.length}`,
    `疑似Excel截断: ${atLimit ? "true" : "false"}`,
    `来源文件: "${sourcePath}"`,
    "用途: 专业知识与方法学习，不作为内容结构或表达风格对标",
    "---",
    "",
    `# ${title}`,
    "",
    "> [!warning] 原始逐字稿状态",
    atLimit
      ? "> 正文达到 Excel 单元格 32,767 字符上限，疑似在源表中被截断；不能视为完整逐字稿。"
      : "> 本文按源表原样归档，仅统一换行；仍可能包含 ASR 错字、口语重复和断句问题。",
    ">",
    `> 来源：${sourcePath}，Sheet1 第 ${sourceRow} 行。`,
    "",
    "## 原始逐字稿",
    "",
    transcript,
    "",
  ].join("\n");
  fs.writeFileSync(absolutePath, content, "utf8");
  records.push({ ordinal, sourceRow, group, rawTitle, title, characters: transcript.length, atLimit, relativePath });
}

fs.writeFileSync(path.join(import.meta.dirname, "new_manifest.json"), JSON.stringify(records, null, 2), "utf8");
console.log(JSON.stringify({
  records: records.length,
  groups: Object.fromEntries([...new Set(records.map((r) => r.group))].map((group) => [group, records.filter((r) => r.group === group).length])),
  atLimit: records.filter((r) => r.atLimit).length,
}, null, 2));
