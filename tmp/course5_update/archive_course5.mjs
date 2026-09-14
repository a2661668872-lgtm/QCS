import fs from "node:fs/promises";
import path from "node:path";

const workspace = "D:/工作空间/Obsidian/AI第二大脑/AI第二大脑_内容创作系统";
const sourcePath = "D:/下载/表格/【安先生：新媒体导演课3.0版】65节.xlsx";
const dump = JSON.parse(await fs.readFile(path.join(workspace, "tmp/course5_update/workbook_dump.json"), "utf8"));
const rows = dump.sheets[0].rows.filter((r) => r.row >= 98 && String(r.values[1] ?? "").length > 0);
const base = path.join(workspace, "01_学习对象/安先生/5.0课程逐字稿");

function category(title) {
  if (title.includes("认知准备篇")) return "认知准备篇";
  if (title.includes("方向篇")) return "方向篇";
  if (title.includes("基本功篇")) return "基本功篇";
  if (title.includes("进阶篇")) return "进阶篇";
  if (title.includes("特殊专题篇") || title.includes("引流素材")) return "特殊专题篇";
  return "未分类";
}

function sanitize(title) {
  return title
    .replace(/_笔记$/u, "")
    .replace(/[\\/:*?"<>|]/g, "-")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 95);
}

function yamlString(value) {
  return JSON.stringify(String(value));
}

const manifest = [];
for (let i = 0; i < rows.length; i++) {
  const row = rows[i];
  const originalTitle = String(row.values[0] ?? "").trim();
  const body = String(row.values[1] ?? "").replace(/\r\n/g, "\n").trim();
  const group = category(originalTitle);
  const sequence = String(i + 1).padStart(3, "0");
  const cleanTitle = sanitize(originalTitle);
  const fileName = `${sequence}-${cleanTitle}.md`;
  const dir = path.join(base, group);
  const filePath = path.join(dir, fileName);
  const truncated = body.length === 32767;
  await fs.mkdir(dir, { recursive: true });
  const warning = truncated
    ? "> 正文达到 Excel 单元格 32,767 字符上限，疑似在源表中被截断；不能视为完整逐字稿。"
    : "> 本文件按源表原样归档；仍可能包含 ASR 错字、口语重复和断句问题，不能视为人工校订稿。";
  const note = `---\n课程版本: "5.0"\n课程组: ${yamlString(group)}\n表格行号: ${row.row}\n原始课题: ${yamlString(originalTitle)}\n正文字符数: ${body.length}\n疑似Excel截断: ${truncated}\n来源文件: ${yamlString(sourcePath)}\n用途: 专业知识与方法学习，不作为内容结构或表达风格对标\n---\n\n# ${cleanTitle}\n\n> [!warning] 原始逐字稿状态\n${warning}\n>\n> 来源：${sourcePath}，Sheet1 第 ${row.row} 行。\n\n## 原始逐字稿\n\n${body}\n`;
  await fs.writeFile(filePath, note, "utf8");
  manifest.push({ sequence: i + 1, row: row.row, originalTitle, cleanTitle, group, bodyLength: body.length, truncated, relativePath: path.relative(path.join(workspace, "01_学习对象/安先生"), filePath).replaceAll("\\", "/") });
}

await fs.writeFile(path.join(workspace, "tmp/course5_update/course5_manifest.json"), JSON.stringify(manifest, null, 2), "utf8");
console.log(JSON.stringify({ archived: manifest.length, truncated: manifest.filter((x) => x.truncated).length, groups: Object.fromEntries([...new Set(manifest.map((x) => x.group))].map((g) => [g, manifest.filter((x) => x.group === g).length])) }, null, 2));
