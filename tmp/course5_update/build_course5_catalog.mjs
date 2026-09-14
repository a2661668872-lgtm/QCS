import fs from "node:fs/promises";
import path from "node:path";

const workspace = "D:/工作空间/Obsidian/AI第二大脑/AI第二大脑_内容创作系统";
const manifest = JSON.parse(await fs.readFile(path.join(workspace, "tmp/course5_update/course5_manifest.json"), "utf8"));
const outputPath = path.join(workspace, "01_学习对象/安先生/5.0课程逐字稿目录.md");
const groups = ["认知准备篇", "方向篇", "基本功篇", "进阶篇", "特殊专题篇"];

let md = `# 安先生 5.0 课程逐字稿目录\n\n> 本目录记录新版表格从“5.0课程内容”分组之后新增的课程。所有文本按源表归档，仍可能包含 ASR 错字、口语重复和断句问题。\n\n## 完整性说明\n\n- 来源：\`D:\\下载\\表格\\【安先生：新媒体导演课3.0版】65节.xlsx\`，\`Sheet1!A97:B135\`。\n- 第 97 行为课程组标题，正文为空；第 98—135 行共 38 条正文。\n- 其中 ${manifest.filter((x) => x.truncated).length} 条达到 Excel 单元格 32,767 字符上限，疑似在源表中被截断。\n- 与现有 91 条归档逐行核对后，旧课程正文没有变化；5.0 作为独立版本保留。\n\n`;

for (const group of groups) {
  const items = manifest.filter((x) => x.group === group);
  md += `## ${group}\n\n| 归档序号 | 原表行 | 课程 | 字符数 | 状态 |\n|---:|---:|---|---:|---|\n`;
  for (const item of items) {
    const target = item.relativePath.replace(/\.md$/u, "");
    const status = item.truncated ? "⚠️ 疑似截断" : "未人工校音";
    md += `| ${String(item.sequence).padStart(3, "0")} | ${item.row} | [[${target}|${item.cleanTitle}]] | ${item.bodyLength} | ${status} |\n`;
  }
  md += "\n";
}

await fs.writeFile(outputPath, md, "utf8");
console.log(outputPath);
