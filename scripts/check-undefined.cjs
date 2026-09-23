/**
 * 地雷扫描器：找出「被引用但从未声明」的全大写标识符。
 *
 * 为什么需要它：整文件重写（write_to_file）最容易漏掉的不是逻辑，而是模块级常量定义，
 * 只留下引用。这类错误在打开对应面板时才会抛 ReferenceError，例如：
 *   推理调节组件异常: EFFORT_DESCRIPTIONS is not defined
 *   推理调节组件异常: CUSTOM_PARTICLES is not defined
 *
 * 用法：
 *   node scripts/check-undefined.cjs lib/client.js
 *   退出码 0 = 干净（只剩已知的全局名），1 = 发现可疑符号
 */
const fs = require("node:fs");

const target = process.argv[2];
if (!target) {
  console.error("用法: node scripts/check-undefined.cjs <文件路径>");
  process.exit(2);
}

let src = fs.readFileSync(target, "utf8");

// 剥掉注释、字符串字面量与长 base64 残块，避免文案/图片数据造成误报
src = src.replace(/\/\*[\s\S]*?\*\//g, " ");
src = src.replace(/(^|[^:])\/\/[^\n]*/g, "$1 ");
src = src.replace(/"(?:[^"\\\n]|\\.)*"/g, '""');
src = src.replace(/'(?:[^'\\\n]|\\.)*'/g, "''");
src = src.replace(/`(?:[^`\\]|\\.)*`/g, "``");
src = src.replace(/[A-Za-z0-9+/=]{80,}/g, " ");

/** JS 内置全局与宿主环境已知名字，不算缺失。 */
const KNOWN_GLOBALS = new Set([
  "JSON", "NaN", "Infinity", "URL", "API", "DOM", "CSS", "HTML", "SVG", "GPU", "CPU",
  "UTF", "RGB", "RGBA", "HSL", "OKLCH", "IIFE", "OS", "UI", "UX", "ID", "OK", "ARIA"
]);

const used = [...new Set(src.match(/\b[A-Z][A-Z0-9_]{2,}\b/g) || [])];

function declared(name) {
  const patterns = [
    new RegExp(`(?:const|let|var|function|class)\\s+${name}\\b`),
    new RegExp(`(?:const|let|var)\\s*\\{[^}]*\\b${name}\\b[^}]*\\}`),
    new RegExp(`(?:const|let|var)\\s*\\{[^}]*\\b${name}\\b[^}]*\\}\\s*=`, "s"),
    new RegExp(`(?:import|export)\\s*\\{[^}]*\\b${name}\\b[^}]*\\}`),
    new RegExp(`${name}\\s*[:=]\\s*(?:function|\\()`) // 赋值式定义
  ];
  return patterns.some((re) => re.test(src));
}

const missing = used.filter((name) => !KNOWN_GLOBALS.has(name) && !declared(name));

if (missing.length === 0) {
  console.log(`✅ 干净：扫描 ${used.length} 个全大写标识符，未发现未声明引用。`);
  process.exit(0);
}

console.log(`❌ 发现 ${missing.length} 个被引用但未声明的标识符：\n`);
for (const name of missing) {
  const lines = [];
  const re = new RegExp(`\\b${name}\\b`, "g");
  let m;
  while ((m = re.exec(src)) !== null && lines.length < 6) {
    lines.push(src.slice(0, m.index).split("\n").length);
  }
  console.log(`  ${name}  → 引用位置: 行 ${lines.join(", ")}`);
}
console.log("\n请在文件里补回定义，或修正引用名。");
process.exit(1);
