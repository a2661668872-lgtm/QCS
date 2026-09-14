import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const vaultRoot = "D:/工作空间/Obsidian/AI第二大脑/AI第二大脑_内容创作系统";
const sourcePath = "D:/下载/表格/【安先生：新媒体导演课3.0版】65节.xlsx";
const archiveDir = path.join(vaultRoot, "01_学习对象", "安先生", "逐字稿原始归档");
const input = await FileBlob.load(sourcePath);
const workbook = await SpreadsheetFile.importXlsx(input);
const sheet = workbook.worksheets.getItem("Sheet1");
const used = sheet.getUsedRange();
const rows = used.values;

const normalizeTitle = (raw) => String(raw ?? "")
  .replace(/[-_ ]*笔记\s*$/u, "")
  .replace(/[-_ ]*ev\s*$/iu, "")
  .replace(/[-_ ]*定[版板]\s*$/u, "")
  .replace(/[-_ ]*初版\s*$/u, "")
  .trim();
const hash = (text) => crypto.createHash("sha256").update(text, "utf8").digest("hex");
const commonPrefix = (a, b) => {
  let i = 0;
  while (i < a.length && i < b.length && a[i] === b[i]) i += 1;
  return i;
};
const commonSuffix = (a, b) => {
  let i = 0;
  while (i < a.length && i < b.length && a[a.length - 1 - i] === b[b.length - 1 - i]) i += 1;
  return i;
};

const oldFiles = fs.readdirSync(archiveDir).filter((name) => name.endsWith(".md")).sort();
const comparisons = [];
for (let i = 1; i < rows.length; i += 1) {
  const sourceRow = i + 1;
  const newTitleRaw = String(rows[i]?.[0] ?? "").trim();
  const newTitle = normalizeTitle(newTitleRaw);
  const newBody = String(rows[i]?.[1] ?? "").replace(/\r\n/g, "\n").trim();
  const oldFile = oldFiles[i - 1];
  let oldBody = "";
  let oldTitle = "";
  if (oldFile) {
    const oldText = fs.readFileSync(path.join(archiveDir, oldFile), "utf8");
    oldBody = (oldText.split("## 原始逐字稿")[1] ?? "").trim();
    oldTitle = (oldText.match(/^原始课题: "(.*)"$/m)?.[1] ?? "").replace(/\\"/g, '"');
  }
  comparisons.push({
    sourceRow,
    oldFile: oldFile ?? null,
    newTitleRaw,
    titleChanged: oldTitle !== newTitleRaw,
    newTitle,
    oldLength: oldBody.length,
    newLength: newBody.length,
    exactMatch: oldBody === newBody,
    oldHash: hash(oldBody),
    newHash: hash(newBody),
    commonPrefix: commonPrefix(oldBody, newBody),
    commonSuffix: commonSuffix(oldBody, newBody),
    oldAtLimit: oldBody.length >= 32767,
    newAtLimit: newBody.length >= 32767,
  });
}

const summary = {
  usedRows: rows.length,
  usedColumns: Math.max(...rows.map((r) => r.length)),
  records: comparisons.length,
  oldFiles: oldFiles.length,
  exactMatches: comparisons.filter((r) => r.exactMatch).length,
  changedBodies: comparisons.filter((r) => !r.exactMatch).length,
  changedTitles: comparisons.filter((r) => r.titleChanged).length,
  newAtLimit: comparisons.filter((r) => r.newAtLimit).length,
  resolvedLimit: comparisons.filter((r) => r.oldAtLimit && !r.newAtLimit && r.newLength > r.oldLength).length,
};
fs.writeFileSync(path.join(import.meta.dirname, "comparison.json"), JSON.stringify({ summary, comparisons }, null, 2), "utf8");
console.log(JSON.stringify(summary, null, 2));
console.log(JSON.stringify(comparisons.filter((r) => !r.exactMatch || r.titleChanged), null, 2));
