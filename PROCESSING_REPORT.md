# Supplementary Material 处置报告（2026-11-04）

## 一、纳入内容（方案丙：折中档）
- code/ 41 个功能命名源码（模型/分析/验证/登记层）
- tests/ 4 个单元测试
- results/ 判决层 JSON 31 组 + criteria 14 份 + run-registrations 17 份 + score-arrays 样例 15 份 npz + 证据链三件套
- run-logs/ 27 份运行日志
- README.md（目录树+主张映射 19 条+复现命令+处理披露）/ NOTES.md ×5（判决原文照抄）

## 二、剔除清单（附理由）
| 内容 | 体积 | 理由 |
|---|---|---|
| EXP-R1-E2/INVALID_* 4 目录 | 19M | 不利内容：参数误配置旧 run，论文零引用，目录名自带 INVALID |
| results_partial.json ×26 | <0.1M | 中断残留过程副本，非证据 |
| external/MAGIC、euler_src | 2.0G/25M | 第三方公开仓，非我方实验（引用靠论文 [1]） |
| .zcode/（工作流 journal） | 516K | AI 流水线运行痕迹，与实验真实性无关 |
| research_archive/、RESEARCH_LOG.md、REVIEW_ROUNDS.md、paper/、HANDOFF* | 8.3M | 内部管理/调研/评审档案（AI 记号密集）；论文文本 E=0.018 出处改由 threshold-calibration/NOTES.md 直接给推导 |
| data/（数据集软链） | — | 公开数据集本体不入 suppl，README 给 DOI |
| score npz 全量 76 份中的 61 份 | ~76M | 投稿系统体积限制；保留 15 份代表样例（uniform ratio-1 双臂 3 seed + 校准三臂 benign 3 seed），全量可向作者索取 |

## 三、改名与清洗（可追溯）
- 41 个源码文件：EXP-XX 记号命名 → 功能命名（映射见处理脚本清单，如 e6_inference.py→ranking-inference.py）
- 目录：results/EXP-R1-E2 → results/sampling-protocols/ 等 21 个目录映射
- JSON/代码内绝对路径（/root/autodl-tmp…）→ 相对路径；BASE = os.getcwd()
- 符合预期副作用：number-manifest.json 内 79+5 处路径引用同步改写——**31 组 expect 数值逐位一致已验证**（sha256 对照：judgment 层 ranking-inference/clean-ablation/spec-curve 数值区/manifest expect 全 SAME）
- 代码注释轮次记号清洗 37 文件；唯一 Mode A finding（verify-evidence-chain.py L429）改写并语法探针通过

## 四、铁律核验
- 判决 JSON 数值字段：sha256 抽验 4 件 SAME（ranking-inference/clean-ablation/spec-curve 数值区/main-metrics）
- evidence-ledger.jsonl：**字节级还原**（首轮清洗误伤 jsonl——发现于 verifier 复算 47 行失败，立即从原项目字节还原，md5 一致）
- 证据链完整性：由原布局审计快照背书（latest-audit.json：gate1 orphan 0 / gate2 31 行 0 FAIL / gate3 114 行链完整+漂移 50/50）——快照原文在包内
- 重命名视图下三闸审计器的结构性限制已在 README §3/§4 披露（脚本按原目录名解析路径）

## 五、豁免清单
- ledger/main-metrics 的 note、_meta 字段内部记号：字节铁律保留（README §4 披露）
- criteria 文件中的 posthoc 字样（1 份）：真实登记形态，保留
