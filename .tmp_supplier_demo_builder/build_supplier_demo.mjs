import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = "D:/工作空间/Obsidian/AI第二大脑/AI第二大脑_内容创作系统/outputs/supplier_demo_20260816";
await fs.mkdir(outputDir, { recursive: true });

const workbook = Workbook.create();
const summary = workbook.worksheets.add("概览");
const suppliers = workbook.worksheets.add("供应商清单");

const categories = [
  ["服饰内衣", "防滑袜"], ["家居日用", "折叠收纳箱"], ["个护清洁", "便携洗脸巾"],
  ["厨房用品", "硅胶保鲜盒"], ["数码配件", "磁吸手机支架"], ["宠物用品", "宠物清洁手套"],
  ["母婴用品", "婴儿防撞条"], ["运动户外", "弹力训练带"], ["办公文具", "桌面收纳架"],
  ["汽车用品", "车载香薰"], ["美容工具", "便携化妆镜"], ["旅行用品", "压缩收纳袋"],
  ["清洁工具", "免手洗拖把"], ["小家电", "迷你加湿器"], ["礼品包装", "节日礼盒"],
  ["五金工具", "多功能螺丝刀"], ["鞋靴配件", "防磨脚贴"], ["食品包装", "密封包装袋"],
  ["户外照明", "便携露营灯"], ["健康用品", "热敷眼罩"]
];

const regions = [
  "浙江义乌", "浙江宁波", "浙江温州", "浙江台州", "广东深圳", "广东广州", "广东东莞", "广东佛山",
  "福建泉州", "福建厦门", "江苏苏州", "江苏南通", "山东临沂", "河北白沟", "河南郑州", "江西南昌"
];
const platforms = ["1688", "义乌购", "中国制造网", "慧聪网", "企业官网"];
const surnames = ["陈", "林", "王", "李", "张", "刘", "黄", "赵", "周", "吴"];
const rows = [];

for (let i = 1; i <= 1200; i++) {
  const [category, product] = categories[(i - 1) % categories.length];
  const region = regions[(i * 3 + 1) % regions.length];
  const platform = platforms[(i * 7 + 2) % platforms.length];
  const minPrice = Number((2.8 + ((i * 17) % 460) / 10).toFixed(1));
  const maxPrice = Number((minPrice + 4 + ((i * 11) % 180) / 10).toFixed(1));
  const moqOptions = [20, 50, 100, 200, 300, 500];
  const moq = moqOptions[(i * 5) % moqOptions.length];
  const sample = i % 4 === 0 ? "否" : "是";
  const custom = i % 3 === 0 ? "否" : "是";
  const number = String(i).padStart(4, "0");
  const city = region.slice(2);
  const supplierName = `${city}${category}供应链${number}有限公司（演示）`;
  rows.push([
    `GYS-${number}`,
    supplierName,
    category,
    product,
    region,
    platform,
    `${surnames[i % surnames.length]}经理`,
    `000-0000-${number}`,
    `DEMO_GYS_${number}`,
    minPrice,
    maxPrice,
    moq,
    sample,
    custom,
    `supplier${number}@example.com`,
    `https://example.com/supplier/${number}`,
    null,
    null,
    null,
    "未联系",
    "虚构演示数据"
  ]);
}

suppliers.showGridLines = false;
suppliers.getRange("A1:U1").merge();
suppliers.getRange("A1").values = [["短视频带货供应商调研表｜1,200家演示数据"]];
suppliers.getRange("A2:U2").merge();
suppliers.getRange("A2").values = [["⚠ 本表仅用于录屏与剪辑展示；商家、联系方式和链接均为虚构演示数据，不可用于真实采购或联络。"]];

const headers = [[
  "编号", "供应商名称", "主营品类", "代表产品", "地区", "来源平台", "联系人", "公开电话（演示）", "微信（演示）",
  "最低价（元）", "最高价（元）", "起订量", "支持拿样", "支持定制", "邮箱（演示）", "来源链接（演示）",
  "优先级", "综合评分", "推荐理由", "跟进状态", "数据属性"
]];
suppliers.getRange("A4:U4").values = headers;
suppliers.getRange("A5:U1204").values = rows;

suppliers.getRange("R5").formulas = [["=MIN(100,50+IF(M5=\"是\",10,0)+IF(N5=\"是\",10,0)+IF(L5<=100,10,IF(L5<=300,5,0))+IF(J5<=20,10,IF(J5<=50,5,0))+IF(K5-J5<=20,5,0)+IF(F5=\"企业官网\",5,0))"]];
suppliers.getRange("R5:R1204").fillDown();
suppliers.getRange("Q5").formulas = [["=IF(R5>=85,\"A\",IF(R5>=70,\"B\",\"C\"))"]];
suppliers.getRange("Q5:Q1204").fillDown();
suppliers.getRange("S5").formulas = [["=IF(Q5=\"A\",\"价格与起订量有优势，建议优先询盘\",IF(Q5=\"B\",\"条件较均衡，可作为备选\",\"起订量或价格需要进一步确认\"))"]];
suppliers.getRange("S5:S1204").fillDown();

const supplierTable = suppliers.tables.add("A4:U1204", true, "SupplierDemoTable");
supplierTable.style = "TableStyleMedium2";
supplierTable.showFilterButton = true;

suppliers.freezePanes.freezeRows(4);
suppliers.freezePanes.freezeColumns(2);
suppliers.getRange("T5:T1204").dataValidation = { rule: { type: "list", values: ["未联系", "已联系", "待复核"] } };

suppliers.getRange("A1:U1").format = {
  fill: "#0F766E",
  font: { bold: true, color: "#FFFFFF", size: 18 },
  horizontalAlignment: "left",
  verticalAlignment: "center"
};
suppliers.getRange("A2:U2").format = {
  fill: "#FEF3C7",
  font: { color: "#92400E", italic: true, size: 10 },
  horizontalAlignment: "left",
  verticalAlignment: "center"
};
suppliers.getRange("A4:U4").format = {
  fill: "#134E4A",
  font: { bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true
};
suppliers.getRange("A5:U1204").format = {
  font: { color: "#1F2937", size: 10 },
  verticalAlignment: "center"
};
suppliers.getRange("J5:K1204").format.numberFormat = "¥0.0";
suppliers.getRange("L5:L1204").format.numberFormat = "#,##0";
suppliers.getRange("R5:R1204").format.numberFormat = "0";
suppliers.getRange("A1:U1").format.rowHeight = 34;
suppliers.getRange("A2:U2").format.rowHeight = 26;
suppliers.getRange("A4:U4").format.rowHeight = 32;
suppliers.getRange("A5:U1204").format.rowHeight = 22;

const widths = [78, 235, 105, 130, 95, 90, 75, 120, 120, 78, 78, 68, 68, 68, 185, 230, 58, 68, 225, 80, 105];
for (let c = 0; c < widths.length; c++) {
  suppliers.getRangeByIndexes(0, c, 1204, 1).format.columnWidthPx = widths[c];
}
suppliers.getRange("B5:B1204").format.wrapText = false;
suppliers.getRange("S5:S1204").format.wrapText = false;

suppliers.getRange("Q5:Q1204").conditionalFormats.add("containsText", {
  text: "A", format: { fill: "#DCFCE7", font: { bold: true, color: "#166534" } }
});
suppliers.getRange("Q5:Q1204").conditionalFormats.add("containsText", {
  text: "B", format: { fill: "#FEF3C7", font: { bold: true, color: "#92400E" } }
});
suppliers.getRange("Q5:Q1204").conditionalFormats.add("containsText", {
  text: "C", format: { fill: "#FEE2E2", font: { bold: true, color: "#991B1B" } }
});

summary.showGridLines = false;
summary.getRange("A1:H1").merge();
summary.getRange("A1").values = [["供应商调研结果概览（演示）"]];
summary.getRange("A2:H2").merge();
summary.getRange("A2").values = [["用于视频画面展示｜详细数据见“供应商清单”｜全部联系方式均为虚构占位"]];
summary.getRange("A4:H4").values = [["总供应商", null, "A级优先", null, "支持拿样", null, "支持定制", null]];
summary.getRange("A5:H5").formulas = [[
  "=COUNTA('供应商清单'!$A$5:$A$1204)", null,
  "=COUNTIF('供应商清单'!$Q$5:$Q$1204,\"A\")", null,
  "=COUNTIF('供应商清单'!$M$5:$M$1204,\"是\")", null,
  "=COUNTIF('供应商清单'!$N$5:$N$1204,\"是\")", null
]];
summary.getRange("A7:B7").values = [["来源平台", "供应商数量"]];
const platformRows = platforms.map((p) => [p, null]);
summary.getRange("A8:B12").values = platformRows;
for (let row = 8; row <= 12; row++) {
  summary.getRange(`B${row}`).formulas = [[`=COUNTIF('供应商清单'!$F$5:$F$1204,A${row})`]];
}
summary.getRange("D7:E7").values = [["主营品类", "供应商数量"]];
const categoryRows = categories.slice(0, 8).map(([c]) => [c, null]);
summary.getRange("D8:E15").values = categoryRows;
for (let row = 8; row <= 15; row++) {
  summary.getRange(`E${row}`).formulas = [[`=COUNTIF('供应商清单'!$C$5:$C$1204,D${row})`]];
}
summary.getRange("G7:H7").values = [["使用说明", "内容"]];
summary.getRange("G8:H12").values = [
  ["数据性质", "虚构演示"],
  ["适用场景", "录屏、剪辑、界面展示"],
  ["不可用于", "真实采购与商家联络"],
  ["建议画面", "先概览，再快速滚动清单"],
  ["隐私处理", "可由创作者后期统一打码"]
];

summary.getRange("A1:H1").format = {
  fill: "#0F766E", font: { bold: true, color: "#FFFFFF", size: 20 }, verticalAlignment: "center"
};
summary.getRange("A2:H2").format = {
  fill: "#CCFBF1", font: { color: "#115E59", size: 10 }, verticalAlignment: "center"
};
summary.getRange("A4:H4").format = {
  fill: "#134E4A", font: { bold: true, color: "#FFFFFF" }, horizontalAlignment: "center"
};
summary.getRange("A5:H5").format = {
  fill: "#F0FDFA", font: { bold: true, color: "#0F766E", size: 18 }, horizontalAlignment: "center",
  borders: { preset: "outside", style: "thin", color: "#99F6E4" }
};
summary.getRange("A7:B7").format = { fill: "#0F766E", font: { bold: true, color: "#FFFFFF" } };
summary.getRange("D7:E7").format = { fill: "#0F766E", font: { bold: true, color: "#FFFFFF" } };
summary.getRange("G7:H7").format = { fill: "#0F766E", font: { bold: true, color: "#FFFFFF" } };
summary.getRange("A8:B12").format.borders = { preset: "inside", style: "thin", color: "#D1FAE5" };
summary.getRange("D8:E15").format.borders = { preset: "inside", style: "thin", color: "#D1FAE5" };
summary.getRange("G8:H12").format.borders = { preset: "inside", style: "thin", color: "#D1FAE5" };
summary.getRange("A1:H1").format.rowHeight = 38;
summary.getRange("A2:H2").format.rowHeight = 24;
summary.getRange("A4:H4").format.rowHeight = 24;
summary.getRange("A5:H5").format.rowHeight = 36;
const summaryWidths = [110, 100, 110, 100, 110, 100, 110, 220];
for (let c = 0; c < summaryWidths.length; c++) {
  summary.getRangeByIndexes(0, c, 15, 1).format.columnWidthPx = summaryWidths[c];
}
summary.freezePanes.freezeRows(2);

const keyInspect = await workbook.inspect({
  kind: "table",
  range: "概览!A1:H15",
  include: "values,formulas",
  tableMaxRows: 20,
  tableMaxCols: 10,
  maxChars: 8000
});
console.log("KEY_INSPECT");
console.log(keyInspect.ndjson);

const dataInspect = await workbook.inspect({
  kind: "table",
  range: "供应商清单!A1:U12",
  include: "values,formulas",
  tableMaxRows: 12,
  tableMaxCols: 21,
  maxChars: 10000
});
console.log("DATA_INSPECT");
console.log(dataInspect.ndjson);

const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan"
});
console.log("FORMULA_ERRORS");
console.log(formulaErrors.ndjson);

const summaryPreview = await workbook.render({ sheetName: "概览", range: "A1:H15", scale: 1.4, format: "png" });
await fs.writeFile(`${outputDir}/preview_summary.png`, new Uint8Array(await summaryPreview.arrayBuffer()));
const listPreview = await workbook.render({ sheetName: "供应商清单", range: "A1:U18", scale: 1.1, format: "png" });
await fs.writeFile(`${outputDir}/preview_list.png`, new Uint8Array(await listPreview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outputDir}/供应商名单_虚构演示数据_1200家.xlsx`);
console.log(`OUTPUT=${outputDir}/供应商名单_虚构演示数据_1200家.xlsx`);
