import fs from "node:fs";
import path from "node:path";

const vaultRoot = "D:/工作空间/Obsidian/AI第二大脑/AI第二大脑_内容创作系统";
const records = JSON.parse(fs.readFileSync(path.join(import.meta.dirname, "new_manifest.json"), "utf8"));
const outputPath = path.join(vaultRoot, "01_学习对象", "安先生", "新增课程逐字稿目录.md");
const sourcePath = "D:\\下载\\表格\\【安先生：新媒体导演课3.0版】65节.xlsx";

const lines = [
  "# 安先生新增课程逐字稿目录",
  "",
  "> 本目录记录新版表格在原65节导演课之后新增的课程。原有65节正式课＋1节序言没有发生正文变化，仍见 [[逐字稿目录]]。",
  "",
  "## 完整性说明",
  "",
  `- 来源：\`${sourcePath}\`，\`Sheet1!A68:B96\`。`,
  `- 新增有正文课程：${records.length} 条；其中 ${records.filter((r) => r.atLimit).length} 条达到 Excel 单元格 32,767 字符上限，疑似被截断。`,
  "- 源表另有4行课程组标题，正文为空，只用于确定课程归属，没有单独建立逐字稿。",
  "- 所有文本仍可能包含 ASR 错字、口语重复和断句问题。",
  "",
];

for (const group of [...new Set(records.map((r) => r.group))]) {
  lines.push(`## ${group}`, "", "| 序号 | 原表行 | 课程 | 字符数 | 状态 |", "|---:|---:|---|---:|---|");
  for (const r of records.filter((item) => item.group === group)) {
    const relativeFromAn = r.relativePath.replace(/^01_学习对象\/安先生\//, "");
    const stem = relativeFromAn.replace(/\.md$/, "");
    const state = r.atLimit ? "⚠️ 疑似截断" : "未人工校音";
    lines.push(`| ${String(r.ordinal).padStart(3, "0")} | ${r.sourceRow} | [[${stem}\|${r.title.replace(/\|/g, "-")}]] | ${r.characters} | ${state} |`);
  }
  lines.push("");
}

fs.writeFileSync(outputPath, `${lines.join("\n")}\n`, "utf8");
console.log(outputPath);
