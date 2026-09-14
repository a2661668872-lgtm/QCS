import fs from "node:fs/promises";
import path from "node:path";

const workspace = "D:/工作空间/Obsidian/AI第二大脑/AI第二大脑_内容创作系统";
const dump = JSON.parse(await fs.readFile(path.join(workspace, "tmp/course5_update/workbook_dump.json"), "utf8"));
const rows = dump.sheets[0].rows.map((r) => ({ row: r.row, title: String(r.values[0] ?? ""), body: String(r.values[1] ?? "") }));
const oldRows = rows.filter((r) => r.row <= 96 && r.body);
const newRows = rows.filter((r) => r.row >= 98 && r.body);

function normalized(text) {
  return text.replace(/\s+/g, "").replace(/[，。！？、；：“”‘’（）()\-—…]/g, "");
}

function shingles(text, size = 5) {
  const s = normalized(text);
  const set = new Set();
  for (let i = 0; i <= s.length - size; i += 2) set.add(s.slice(i, i + size));
  return set;
}

function dice(a, b) {
  let small = a, large = b;
  if (a.size > b.size) [small, large] = [b, a];
  let intersection = 0;
  for (const item of small) if (large.has(item)) intersection++;
  return (2 * intersection) / (a.size + b.size || 1);
}

const oldPrepared = oldRows.map((r) => ({ ...r, norm: normalized(r.body), set: shingles(r.body) }));
const matches = [];
for (const item of newRows) {
  const norm = normalized(item.body);
  const set = shingles(item.body);
  const ranked = oldPrepared.map((old) => ({
    row: old.row,
    title: old.title,
    exact: norm === old.norm,
    score: dice(set, old.set),
  })).sort((a, b) => b.score - a.score).slice(0, 3);
  matches.push({ row: item.row, title: item.title, length: item.body.length, topMatches: ranked });
}

await fs.writeFile(path.join(workspace, "tmp/course5_update/version_matches.json"), JSON.stringify(matches, null, 2), "utf8");
console.log(JSON.stringify(matches.map((m) => ({
  row: m.row,
  title: m.title,
  length: m.length,
  bestRow: m.topMatches[0].row,
  bestTitle: m.topMatches[0].title,
  similarity: Number(m.topMatches[0].score.toFixed(3)),
  exact: m.topMatches[0].exact,
})), null, 2));
