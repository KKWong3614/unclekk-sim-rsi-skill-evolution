# 下一阶段研究课题

> 状态总览（2026-11-10，包版本 1.0.3）：**T1 / T2 均未启动，当前不可声称**。本文件把「想做到的」与「已做到的」隔开，防止对外描述把未来写成现在。1.0.1 新增的可运行门禁只覆盖回归判定，**不改变本文件任何状态**。

## 共同前置（两个课题都绕不开）

1. **自动选流的可信约束**：工作流建议要变成自动决策，必须先固化「禁止」项（例如禁止把不可用状态改判成已验证来过闸、禁止批量无差别批准来洗绿），并能证明约束在无人值守时不被绕过。随包 `scripts/gate_min.py` 把这两条做成机器可检查的负向用例，但只覆盖门禁一步，不等于完成该前置。
2. **自指改动的授权与回滚链**：任何「改判据 / 改任务集 / 改引擎」的动作都要有改前改后锚点、授权来源、独立复算与可回滚路径。缺这条，自动化程度越高越危险。
3. **方向裁决独立化**：门禁只判「基线没退化」，不能判「改得更好」。要支撑强宣称，需要独立指标棘轮 + 人类确认点，且两者都不能由被改进对象自己写。

---

## T1：RSIFlow 四段闭环自动落地（当前不可声称）

**目标**：从「诊断 → 选流 → 蒸馏 → 门禁」全程无人值守跑通一轮，且结果可独立复算。

**当前差距**

| 段 | 现状 | 缺口 |
|---|---|---|
| ① 诊断 | 已可跑，轨道 B 已接离线归因 | 只产出建议，不自动决策 |
| ② 选流 | 候选 + 禁止项 | 最终决策由人确认 |
| ③ 蒸馏 | GEPA 自动产出候选 | 写回生产、原则沉淀需人确认 |
| ④ 进化 harness | 人工迭代 | 不能自改任务集 / 判据 / harness |

**需要补齐**

- 带硬约束的自动选流决策器（禁止项必须机器可执行，不是文档建议）。
- 蒸馏产物的自动写回通道 + 授权链 + 回滚。
- harness 自迭代与版本棘轮，且自迭代结果可被独立交叉校验。
- 端到端无人值守复验脚本，逐段留痕，任何一段降级即 fail-closed。

**验收标准（建议）**

- 一次完整 run 从头到尾**零人工决策**，四段均有机器可验证的留痕。
- 门禁全绿 + 独立复算一致 + 未触发任何「禁止」项。
- 有负向用例证明：试图绕过禁止项或篡改判据时闭环会阻断，而不是放行。
- 达标后方可讨论把措辞升级为「四段闭环自动落地」；未达标一律使用「确定性回归基线 + 外接闸门，辅以离线诊断建议」。

**状态**：未启动 / 当前不可声称。

---

## T2：已实现递归自我改进 / RSI（当前不可声称）

**目标**：改进器能在**不改坏自身**的前提下改进自身，且每次自改可独立复算与回滚。

**当前差距**

- 改进对象是**技能文档（SKILL.md 文本）**，不是改进器自身；严格学术意义的 RSI 不成立。
- harness、任务集、判据由人工迭代（④ 属半自动）。
- 缺少自指改造的边界定义：哪些组件允许自改、改到什么程度必须停、由谁裁决方向。
- 信息论边界未澄清：判据与被改对象同源时存在「自我声明循环」，需要独立验证器。

**需要补齐**

- 自指改造白名单 / 黑名单与不可变内核（哪些东西永远不能自改）。
- meta-harness 可验证自改：改动前后哈希链、授权、独立复算、棘轮与回滚。
- 防误演化机制：双指标棘轮、人类确认点、异常自改自动冻结。
- 独立验证器与判据源分离，消除「自己判自己」。

**验收标准（建议）**

- 改进器对自身的一次改动能被第三方独立复算出完全相同的前后差异。
- 自改后系统能力不退化，且能在异常时自动回滚到已验证版本。
- 有负向用例证明：自改判据 / 自改任务集 / 自改验证器的尝试被阻断或留痕告警。
- 达标后方可讨论「实现 RSI」；未达标一律使用「参考 RSI 方法论的精简版技能文本进化」。

**状态**：未启动 / 当前不可声称。

---

## 口径纪律

- 两个课题在达标前，**只能作为「下一步 / 研究课题」出现**，不得写成「已完成」「已实现」「落地」。
- 每次对外发布前重新核对本文件状态；达标后需同步更新 `SKILL.md` §0/§6、`claim-boundary.md`、`faq.md` 与本文件，并保留升级依据与证据路径。
- 宁可被说保守，也不要把未做说成已做——这是整个体系的防洗绿底线。

---

## English summary

Status as of package version 1.0.3: **both T1 and T2 are not started and not claimable**; the newly added runnable gate changes no status here. Shared prerequisites are machine-enforced constraints for automatic workflow selection, an authorization/rollback chain for any self-modification, and independent direction judgement (a gate only detects regression, never "better"). T1 needs a zero-human-decision end-to-end run with per-stage traces, independent recomputation and negative cases proving bypass attempts are blocked; until accepted, use "deterministic regression baselines plus an external gate, assisted by offline diagnosis". T2 needs a third party to recompute an identical before/after diff of a self-change, no capability regression, automatic rollback on anomalies and blocked attempts to self-modify criteria, task sets or validators; until accepted, use "skill-text evolution referencing RSI methodology (Simplified RSI)". Before every release, recheck this file; after acceptance, update `SKILL.md` §0/§6, `claim-boundary.md` and `faq.md` together with the evidence path. Full gap tables and acceptance criteria are in the Chinese sections above.
