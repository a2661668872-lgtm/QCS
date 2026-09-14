import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath = "D:/下载/表格/【安先生：新媒体导演课3.0版】65节.xlsx";
const input = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(input);

const summary = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 8000,
  tableMaxRows: 5,
  tableMaxCols: 5,
  tableMaxCellChars: 120,
});

const sheets = [];
for (const sheet of workbook.worksheets.items) {
  const used = sheet.getUsedRange(true);
  const values = used ? used.values : [];
  const rows = values.map((row, index) => ({
    row: index + 1,
    values: row.map((value) => value ?? ""),
    lengths: row.map((value) => typeof value === "string" ? value.length : 0),
  }));
  sheets.push({ name: sheet.name, rowCount: values.length, colCount: values[0]?.length ?? 0, rows });
}

const output = { workbookPath, inspect: summary.ndjson, sheets };
await fs.writeFile("workbook_dump.json", JSON.stringify(output, null, 2), "utf8");
console.log(JSON.stringify({
  workbookPath,
  sheets: sheets.map((s) => ({ name: s.name, rowCount: s.rowCount, colCount: s.colCount })),
  tails: sheets.map((s) => ({ name: s.name, rows: s.rows.slice(-20).map((r) => ({ row: r.row, title: r.values[0], length: r.lengths[1] ?? 0 })) })),
}, null, 2));
