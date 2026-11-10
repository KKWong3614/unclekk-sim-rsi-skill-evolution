---
name: unclekk-sim-rsi-skill-evolution
slug: unclekk-sim-rsi-skill-evolution
displayName: "UncleKK Simplified RSI Skill Evolution / 精简版 RSI 技能进化"
version: 1.0.3
summary: "参考 RSIFlow 方法论内核的精简版 RSI 技能进化工作流：SOP、可运行回归门禁、失败恢复与宣称边界。/ A Simplified RSI skill-evolution workflow: SOP, a runnable regression gate, failure recovery and explicit claim boundaries."
description: "把「诊断→选流→蒸馏→门禁」落成可复用 SOP，附零依赖最小门禁脚本；明确人工环节与当前不可声称项。/ A reusable diagnose-select-distill-gate SOP with a zero-dependency gate, disclosing human steps and prohibited claims."
license: "个人非商用 / personal non-commercial"
tags: [rsi, rsiflow, gepa, skill-evolution, regression-gate, claim-boundary, agent]
triggers:
  - 精简版 RSI / Simplified RSI
  - 技能进化 / skill evolution
  - RSIFlow 四段 / RSIFlow four stages
  - GEPA 进化 + 回归门禁 / GEPA + regression gate
  - 冻结任务集 / frozen task set
  - 回归门禁怎么过 / how to pass a regression gate
  - 防洗绿 / 禁止项 / anti-whitewash
  - 对外宣称口径 / claim boundary
  - 这句话能不能说 / is this claim allowed
  - 技能文档瘦身 / compress a SKILL.md
agent_created: true
---

# UncleKK Simplified RSI Skill Evolution / 精简版 RSI 技能进化

> 版本 **1.0.3** ｜ 中文在前、英文在后 ｜ 主文档只给要点，细节见第 8 节文档地图

## 0. 防误读声明（先读这一段）

本 skill 是**方法论与工作流指引**，不是「已实现递归自我改进」的系统。三点必须随任何对外引用一起保留：

1. **改进对象是技能文档（SKILL.md 文本），不是改进器自身**；harness 迭代仍靠人工，严格学术意义的 RSI 未实现。
2. **`PASS / 全绿 / N/N` 一律表示「冻结基线的回归未退化」**，不表示能力变强、语义质量达标或实时闭环已验证。
3. **当前不可声称**：「RSIFlow 四段闭环自动落地」「已实现递归自我改进 / RSI」。这两项是后续课题，不是当前能力。

可声称的限定式表述：**「基于 RSIFlow 方法论内核的精简版 RSI 技能进化」**——「方法论内核」与「精简版」两个限定词必须同时保留。

## 1. 定位与参考来源

RSIFlow 的四段闭环是：诊断瓶颈 → 动态选改进工作流 → 蒸馏成技能/原则 → 进化 harness。完整复现需要研究级预算与 meta-harness 自进化。本 skill 只取方法论内核（**诊断 → 改进 → 小样本验证 → 沉淀**），把技能文本作为进化对象，产出经回归验证后才入库的 SKILL.md。已实跑形态是**双目标进化**：能力不退前提下压缩篇幅，冻结任务集即回归护栏；目标是「不丢能力地把文档变瘦」，不是「把能力变强」。

**参考来源（可核对）**：RSIFlow: *Adaptive Self-Improvement Workflows with an Evolving Meta-Agent*, arXiv:2610.21791v2（2026-11-02），https://arxiv.org/abs/2610.21791 。本包是独立的方法论整理与工作流实践，**不是该论文的官方实现，未复现其实验，未使用其代码**；许可：个人非商用。包内所有版本号统一为 1.0.3，变更见 `CHANGELOG.md`。

## 2. 四段现状（诚实披露）

| 段 | 现状 | 说明 |
|---|---|---|
| ① 瓶颈诊断 | 部分自动 | 轨道 A 有分类诊断器；轨道 B 已接离线诊断，只产出建议 |
| ② 选工作流 | 人工 + 建议 | 候选工作流与「禁止」项由诊断器给出，最终选流由人确认 |
| ③ 蒸馏成技能 | 引擎自动 + 人工审核 | GEPA 产出候选 SKILL.md；写回生产与原则沉淀需人确认 |
| ④ 进化 harness | **半自动 / 人工** | 任务集、判据与 harness 版本靠人工迭代，不是自指自改 |

结论：**后两段有实盘能力，前两段只有辅助，闭环不是全自动**。准确表述是「确定性回归基线 + 外接 P0 闸门，辅以离线诊断建议」。逐段细节见 `references/four-stage-status.md`。

## 3. 可复用工作流（SOP）

1. **冻结基线**：固定确定性任务集与 fixtures 并纳入哈希锁定；未授权改动触发完整性告警。
2. **诊断**：跑基线，按失败轨迹归类瓶颈（守卫 / 一致性 / 模型预算 / 能力 / 脆性 / 压缩）。
3. **选流**：按瓶颈选工作流，逐条核对「禁止」项（禁止把 `unavailable` 改判成 `validated` 来过闸、禁止批量无差别批准来洗绿）。
4. **进化**：GEPA 反思式进化，双目标优先「能力保持 + 篇幅精简」，设 `max_metric_calls` 预算硬停，保留完整轨迹。
5. **门禁**：冻结任务集回归 + 独立交叉校验；PASS 只解释为「基线未退化」。本步可直接跑第 5 节的参考门禁。
6. **沉淀**：人工确认后写回；登记 from→to 变更链、授权来源与回滚路径。

## 4. 前置准备与不适用清单

**最小准备三样**：① 有稳定 id 与期望结果的确定性任务集；② 每个任务可复算的结果（含状态与失败原因）；③ 一次人工确认点（谁批准写回、如何回滚）。可运行部分另需 Python 3.9+ 与 UTF-8 终端，**不需要联网、账号、API Key 或模型服务**。详见 `references/runnable-guide.md` 第 2 节。

**不适用 / 请勿直接套用**：没有冻结任务集或任务集仍在频繁变动；目标是「让技能变聪明 / 语义质量达标」（门禁只判退化，不判方向）；需要无人值守自动写回或自动改判据（当前需人工确认，属 T1 课题）；寻找完整 RSI 系统或生产工程源码；需要「已在特定平台验证兼容」的承诺。展开见 `references/faq.md` Q7、Q10、Q14。

## 5. 直接跑起来（本包可执行部分）

本包共有 **6 个零依赖脚本**，分两类：① 门禁 `gate_min.py`（判定入口）；② 五个辅助工具，只做分析 / 分类 / 检查 / 快照 / 对比，**绝不自动改 verdict、绝不自动写回、绝不声称 T1/T2**。先跑聚合自检，确认全绿再分别用：

```bash
python scripts/test_all.py            # 聚合自检：6 个脚本内置用例全跑一遍
python scripts/gate_min.py            # 冻结任务集回归判定（门禁入口）
python scripts/gate_min.py --self-test  # 6 组正负例自检
python scripts/gate_min.py --json       # 机器可读的稳定输出
```

其余 5 个辅助脚本（均 `--self-test` 可自检）：

```bash
python scripts/freeze_snapshot.py --tasks scripts/fixtures/tasks.json   # 登记/重算冻结基线哈希锁
python scripts/diagnose_classify.py --input traces.json                 # 失败轨迹归 6 桶，只给建议
python scripts/coverage_diff.py --before r1.json --after r2.json        # 两次结果集逐条 diff
python scripts/claim_lint.py SKILL.md --strict                          # 宣称边界 linter
```

零第三方依赖，`gate_min.py` 退出码 `0/1/2/3`。随包 `5/5` 是**示意数据（demo only，非实测）**。完整输入、输出、退出码、换成自己任务集的哈希重算命令，以及重复运行一致性验证，见 `references/runnable-guide.md`；失败提示与恢复决策树见 `references/failure-recovery.md`；玩具级端到端走查见 `references/walkthrough.md`。

**刻意不自动恢复**：自动批准、自动改 verdict、自动重算哈希去匹配被改任务集，正是本门禁要拦的三类洗绿动作。辅助脚本同理——`diagnose_classify` 只产出建议、`claim_lint` 只报违规、`coverage_diff` 只做对比报告，均不代你决策或写回。提供的是现成提示、可重复自检与 fail-closed 拒判，而不是自动放行。

## 6. 宣称口径速查

| 措辞 | 判定 |
|---|---|
| 参考 / 借鉴 RSIFlow 方法论内核 | 可（须附可核对引文） |
| 「精简版 RSI」的技能文本进化 | 可 |
| GEPA 进化 + 冻结任务集回归门禁 | 可（须附防误读声明） |
| RSIFlow 四段闭环自动落地 | **不可** |
| 已实现递归自我改进 / RSI | **不可** |
| 技能能力变强 / 语义质量达标 | **不可** |
| 实时闭环已验证 | **不可** |

完整对照与依据见 `references/claim-boundary.md`，安全措辞与被否决反例见 `EXAMPLES.md`。

## 7. 交付检查清单

- [ ] 每个对外数字都附「PASS = 回归未退化，非能力提升」
- [ ] 示例数字已标注「示意值，非实测」，真实数字附证据路径
- [ ] 说明了哪些环节仍是人工，未把「后续课题」写成「当前能力」
- [ ] 引文可核对（标题 / 版本 / 出处），包内版本号一致
- [ ] 未出现本机绝对路径、口令、API Key 或账号信息
- [ ] 变更有授权记录与回滚路径

## 8. 文档地图（按需深入，不必连读）

| 你想做什么 | 读这个 |
|---|---|
| 立刻跑一遍、看输入输出样例 | `references/runnable-guide.md` |
| 出错了，找现成提示与恢复路径 | `references/failure-recovery.md` |
| 有具体疑问 | `references/faq.md` |
| 判断某句话能不能说 | `references/claim-boundary.md` / `EXAMPLES.md` |
| 查四段 × 双轨道细节 | `references/four-stage-status.md` |
| 查 T1/T2 差距与验收标准 | `references/roadmap.md` |
| 看玩具级端到端走查（冻结→诊断→蒸馏→门禁→沉淀） | `references/walkthrough.md` |
| 跑辅助工具（快照/分类/diff/宣称 lint） | `scripts/freeze_snapshot.py` / `diagnose_classify.py` / `coverage_diff.py` / `claim_lint.py` / `test_all.py` |

## 9. 下一阶段课题（当前不可声称）

- **T1**：RSIFlow 四段闭环自动落地 —— 未启动 / 当前不可声称
- **T2**：已实现递归自我改进 / RSI —— 未启动 / 当前不可声称

差距与验收标准见 `references/roadmap.md`；达标前只能作为「下一步 / 研究课题」出现。

---

# English summary

> Full detail is in the Chinese sections above; this is a condensed English digest.

This is a **methodology guide plus a runnable minimal gate**, not a system that achieved recursive self-improvement. The evolved object is skill text, not the improver; harness iteration stays human-driven. `PASS / all green / N/N` means only that frozen baselines did not regress — not capability gain, not semantic quality, not a validated live loop.

The safe qualified phrasing is **"skill evolution inspired by RSIFlow methodology (Simplified RSI)"**; keep both qualifiers. Currently prohibited: "RSIFlow four-stage loop implemented automatically" and "recursive self-improvement / RSI achieved". Both are logged as not-started research topics T1/T2.

Reference (verifiable): RSIFlow: *Adaptive Self-Improvement Workflows with an Evolving Meta-Agent*, arXiv:2610.21791v2, https://arxiv.org/abs/2610.21791 . This package is an independent, non-official methodology write-up; it does not reproduce the paper's experiments or use its code. Version 1.0.3 across all files.

The four stages are partly automated at best: stages ①② advise, ③ produces candidates with human review, ④ is manual/semi-automatic. The accurate description is "deterministic regression baselines plus an external gate, assisted by offline diagnosis". The reusable SOP is freeze → diagnose → select → evolve → gate → consolidate, with a from→to authorization chain and rollback.

`scripts/gate_min.py` is a zero-dependency reference implementation with fixtures, a six-case self-test, stable deterministic output and exit codes 0/1/2/3. All bundled `5/5` figures are demo data, not measurements. It deliberately never auto-approves or auto-repairs, because those are the whitewash patterns it exists to block. It makes no network calls and binds to no model vendor; compatibility with any specific domestic platform has not been tested.

See `references/runnable-guide.md` (inputs, outputs, hash refresh), `references/failure-recovery.md` (error prompts, recovery), `references/faq.md` (frequent questions, out-of-scope cases), `references/claim-boundary.md` and `EXAMPLES.md` (claim matrix), `references/four-stage-status.md` (per-stage detail), `references/roadmap.md` (T1/T2 acceptance criteria).
