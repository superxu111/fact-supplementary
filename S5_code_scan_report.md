# Code-humanizer Mode A 扫描报告（2026-11-04）

## 扫描范围
code/ 全部 41 个 .py + tests/ 4 个 + scripts/；模式：营销词、调试残留（TODO/FIXME/XXX）、
复述式注释、版本化注释、AI 自指、内部轮次记号注释；领域约定豁免检测（expected FALSIFIED 极性标注）。

## 发现与处置
| # | 位置 | 类别 | severity | 处置 |
|---|---|---|---|---|
| 1 | verify-evidence-chain.py L429 | 内部轮次记号注释（R3 修复叙述） | 2 | 已改写为英文功能性注释（"action='append' is required: dict-store overwrote repeated flags…"），语法探针通过 |
| — | 全包 | 领域极性约定注释（expected FALSIFIED 类） | 1（豁免） | 扫描未命中；如有以原文保留 |

## 语法探针
全部 45 个 .py 文件 ast.parse 通过（清洗后全量复验）。

## 运行探针
- verify-evidence-chain.py：实跑执行至闸2（路径解析在重命名视图下按 README §4 声明的结构性限制报告路径不匹配——见该节披露）；
- 其余脚本为数据依赖脚本（需 LANL 数据集），静态语法探针通过。

## 豁免清单
- results/evidence-chain/evidence-ledger.jsonl 与 main-metrics.json：字节铁律文件，
  note/meta 字段保留原始运行记录（含内部阶段标签），README §4 已声明。
