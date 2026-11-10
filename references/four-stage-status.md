# 四段闭环现状

> 本文件是 `SKILL.md` §2 的展开。只需快速判定请读主文档表格；需要逐段依据再读这里。

RSIFlow 的四段：**① 诊断瓶颈 → ② 动态选改进工作流 → ③ 蒸馏成技能/原则 → ④ 进化 harness**。

## 两条轨道

判定宣称时必须把两条轨道分开说：

- **轨道 A（LLM / GEPA）**：面向技能文档进化，有分类诊断器与工作流库。
- **轨道 B（确定性回归闸门）**：面向检测器 / 护栏的行为回归，原本只有第 ④ 段门禁，后来才补上 ①② 的**离线诊断**。随包 `scripts/gate_min.py` 是这一步的最小参考实现。

## 现状矩阵

| 段 | 轨道 A | 轨道 B | 人工介入 |
|---|---|---|---|
| ① 诊断 | 分类诊断器可跑（守卫 / 一致性 / 模型预算 / 能力 / 脆性 / 压缩） | 离线归因已接线，但只产出建议 | 低（诊断）→ 中（采纳） |
| ② 选流 | 工作流库给出候选 + 「禁止」项 | 无自动选流 | **高：最终决策由人确认** |
| ③ 蒸馏 | GEPA 产出候选技能文本 | 引擎改动靠手工写 fixture / 改判据 | **高：写回生产需人确认** |
| ④ 进化 harness | 任务集与判据靠人工迭代 | 回归基线由人工扩充 | **高：非自指自改** |

## 为什么不是「自动闭环」

1. 诊断器对另一条轨道的报告曾完全「失明」，接线后也只是**建议**，不自动决策。
2. ③ 的引擎能自动产出候选，但**写回生产**、**原则沉淀**都要人工确认。
3. ④ 的 harness 版本、任务集、判据都由人改，改进器**不能改自己**。
4. 门禁全绿只说明「冻结基线没退化」，**不判演化方向**；方向裁决需要独立指标与人类确认。
5. 随包参考门禁虽可反复执行且结果稳定，但只覆盖第 ④ 段的回归判定，刻意不自动批准、不自动写回，不构成闭环自动化。

因此准确表述是：**「确定性回归基线 + 外接 P0 闸门，辅以离线诊断建议」**，不是「RSIFlow 四段闭环自动落地」。

---

## English summary

Two tracks must be discussed separately: Track A (LLM/GEPA, evolves skill text) and Track B (deterministic regression gate, covers detector/guardrail behaviour, with offline diagnosis for stages ①② added later). Stages ① and ② only advise; stage ③ produces candidates automatically but write-back needs human confirmation; stage ④ iterates harness, task sets and criteria manually, so the improver cannot modify itself. A green gate says only "no regression" and does not judge direction. The bundled reference gate is a minimal, deterministic implementation of stage ④'s regression check and deliberately never auto-approves or auto-writes back. The accurate description is "deterministic regression baselines plus an external gate, assisted by offline diagnosis", not an automatically closed four-stage loop. Full per-stage matrix is in the Chinese sections above.
