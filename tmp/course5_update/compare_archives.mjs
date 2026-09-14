import fs from "node:fs/promises";
import path from "node:path";

const workspace = "D:/工作空间/Obsidian/AI第二大脑/AI第二大脑_内容创作系统";
const dump = JSON.parse(await fs.readFile(path.join(workspace, "tmp/course5_update/workbook_dump.json"), "utf8"));
const rows = new Map(dump.sheets[0].rows.map((r) => [r.row, { title: String(r.values[0] ?? ""), body: String(r.values[1] ?? "") }]));

async function listMarkdown(dir) {
  const out = [];
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...await listMarkdown(full));
    else if (entry.name.endsWith(".md")) out.push(full);
  }
  return out;
}

function normalize(s) {
  return s.replace(/\r\n/g, "\n").trim();
}

const archiveDirs = [
  path.join(workspace, "01_学习对象/安先生/逐字稿原始归档"),
  path.join(workspace, "01_学习对象/安先生/新增课程逐字稿"),
  path.join(workspace, "01_学习对象/安先生/5.0课程逐字稿"),
];
const comparisons = [];
for (const dir of archiveDirs) {
  for (const file of await listMarkdown(dir)) {
    const text = await fs.readFile(file, "utf8");
    const rowMatch = text.match(/(?:表格行号|原表行号|原表行):\s*(\d+)/);
    if (!rowMatch) continue;
    const row = Number(rowMatch[1]);
    const marker = "## 原始逐字稿";
    const markerIndex = text.indexOf(marker);
    const archivedBody = markerIndex >= 0 ? text.slice(markerIndex + marker.length) : "";
    const current = rows.get(row);
    comparisons.push({
      row,
      file: path.relative(workspace, file).replaceAll("\\", "/"),
      existsInWorkbook: Boolean(current),
      sameBody: current ? normalize(archivedBody) === normalize(current.body) : false,
      archivedLength: normalize(archivedBody).length,
      currentLength: current ? normalize(current.body).length : null,
      title: current?.title ?? "",
    });
  }
}

comparisons.sort((a, b) => a.row - b.row);
const result = {
  compared: comparisons.length,
  exact: comparisons.filter((x) => x.sameBody).length,
  changed: comparisons.filter((x) => x.existsInWorkbook && !x.sameBody),
  missing: comparisons.filter((x) => !x.existsInWorkbook),
};
await fs.writeFile(path.join(workspace, "tmp/course5_update/archive_comparison.json"), JSON.stringify(result, null, 2), "utf8");
console.log(JSON.stringify(result, null, 2));
