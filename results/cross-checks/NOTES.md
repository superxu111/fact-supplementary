# NOTES

来源文件：score-reproduction-check.json（原样归档的运行判决记录）

- 运行日期：2026-10-24
- exp: R1-verify-incase
- verdict: PASS：3 臂×3 seed 逐边 npz 复算与在案 JSON 一致（容差 5e-4），池计数逐位一致
- verdict_correction_r3b: {"status": "SUPERSEDES（R3 第二轮 R5B-M1：只增不改——verdict 原文保留）", "original_verdict_kept": "PASS：3 臂×3 seed 逐边 npz 复算与在案 JSON 一致（容差 5e-4），池计数逐位一致", "correction": "原判语「3 臂×3 seed 逐边 npz 复算与在案 JSON 一致」对 full 臂 AP 边过强：该边在案 JSON 侧（ap_logon_in）=null，match 判定实际只覆盖有值边+计数；AP 边逐位一致仅成立于 re 侧重算值之间（VERIFY ap_logon_re 与后续补算/E47B 锚三方逐位一致，见 protocol-grid-closure.json:regression_check_full_ap_anchor_r3b）", "producer": "src/r3_e2_anchor_r3b.py"}

---

以上判决文字为运行记录原文照抄，未做改写；数值字段见同目录 JSON（字节原样）。
