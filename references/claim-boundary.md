# 宣称口径边界

> 本文件是「某句话能不能说」的权威对照。集中问答见 `faq.md`，措辞正例/反例见 `EXAMPLES.md`。包内所有数字均为示意值，非实测。

## 判定原则

一句宣称能否使用，取决于三件事：**改进对象是什么、哪些环节是人工、PASS 怎么解释**。三者任一被模糊，就会从「诚实披露」滑向「幻影声明」。独立审计把这类问题列为「宣称风险」，要求措辞降级与防误读声明。

## 可声称（有实盘支撑）

| 措辞 | 支撑 |
|---|---|
| 参考 / 借鉴 RSIFlow 方法论内核 | 定位即如此：只取「诊断 → 改进 → 小样本验证 → 沉淀」内核；须附可核对引文（arXiv:2610.21791v2） |
| 「精简版 RSI」的技能文本进化 | 有双目标 GEPA 实跑：能力不退前提下压缩篇幅 |
| GEPA 反思式进化 + Pareto 双目标 + 冻结任务集回归门禁 | 有流程与冻结基线证据 |
| 某版本「由精简版 RSI 流水线进化并过门禁」 | 可用，但须附证据路径、真实数字与防误读声明 |

## 不可声称（审计明令降级）

| 措辞 | 为什么不行 |
|---|---|
| RSIFlow 四段闭环**自动**落地（不可声称） | ②选流最终决策、③蒸馏写回、④ harness 迭代仍人工；「确定性回归基线 + 外接 P0 闸门，辅以离线诊断建议」才是准确表述 |
| 已实现递归自我改进 / RSI | 改进对象是技能文档，不是改进器自身；harness 靠人工迭代，属「半自动」 |
| 技能能力变强 / 语义质量达标 / 检测能力增强 | `PASS` 只证明冻结基线未退化；门禁是结构门禁，不判演化方向 |
| 实时自愈闭环已验证 | 相关基线为「离线完成 / 实时待验」 |
| 全面加固 / 所有技能已进化 | 实跑只覆盖少数技能 |
| 已适配某具体国内平台 / 某具体产品 | 可运行部分零外部依赖，但未做特定平台兼容性实测，见 `runnable-guide.md` 第 6 节 |

## 三条硬性纪律

1. **对外引用任何数字，必须附**「PASS = 回归未退化，非能力提升」，并区分示意值与实测值。
2. **禁止把「后续课题」写成「当前能力」**；两个强宣称见 `roadmap.md`，状态均为未启动。
3. **改进器自指改造未实现前，不得使用「RSI」作为完成态动词**（可作参照名词，须带限定词）。

## 常见误判

- 「门禁全绿，所以改得更好」——错。全绿只说明没退化，方向需独立指标与人类确认。
- 「加了可运行脚本，所以闭环自动落地了（不可声称）」——错。脚本只判冻结回归，且刻意不自动批准、不自动写回，见 `failure-recovery.md` 第 3 节。
- 「去掉『精简版』更简洁」——错。删限定词即构成宣称风险，见 `faq.md` Q16。

---

## English summary

A claim is acceptable only if it states what is evolved (skill text, not the improver), which steps stay human, and that PASS means no regression not capability gain. Allowed: qualified "Simplified RSI skill-text evolution inspired by RSIFlow methodology" with GEPA plus a frozen-task regression gate. Prohibited: an automatically closed four-stage loop, RSI achieved, capability/semantic gain, a validated live loop, blanket hardening, or verified compatibility with any specific platform. Full rationale and the common-misjudgement list are in the Chinese sections above.
