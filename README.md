# 精简版 RSI 技能进化

> 版本 **1.0.3** ｜ 中文在前、英文在后 ｜ 包内所有文件版本标注与 `SKILL.md` frontmatter 一致

## 这是什么

一份**方法论 + 可运行最小门禁 + 宣称边界**的技能包。把 RSIFlow 的四段思路落成个人可负担的技能进化 SOP：以 GEPA 为引擎进化技能文本，用冻结任务集做回归护栏，用哈希锁定与授权链守住治理。

**它不是**：已实现递归自我改进（RSI）的系统，也不是「四段闭环自动落地」的成品。两项已登记为后续课题，见 `references/roadmap.md`。

## 30 秒上手

```bash
python scripts/gate_min.py              # 回归判定：5/5 示意数据，EXIT=0
python scripts/gate_min.py --self-test  # 6 组正负例自检，EXIT=0
```

零第三方依赖，无需安装、无需联网、无需账号。然后按需读：

1. 要对外写描述：先读 `SKILL.md` §0 防误读声明，再查 §6 宣称速查。
2. 要真正照做：读 `references/runnable-guide.md`（完整输入输出样例、退出码、换成自己任务集）；出错查 `references/failure-recovery.md`。
3. 有具体疑问：查 `references/faq.md`。

## 文件结构

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 主文档：定位、四段现状、SOP、前置清单、宣称速查、文档地图、可执行脚本一览 |
| `scripts/gate_min.py` | 零依赖回归门禁（哈希锁、覆盖度、禁止项、自检）；退出码 0/1/2/3 |
| `scripts/freeze_snapshot.py` | 辅助：登记 / 重算冻结基线哈希锁 |
| `scripts/diagnose_classify.py` | 辅助：失败轨迹归 6 桶，只给建议 |
| `scripts/coverage_diff.py` | 辅助：两次结果集逐条 diff |
| `scripts/claim_lint.py` | 辅助：宣称边界 linter（`--strict` 可当硬闸） |
| `scripts/test_all.py` | 聚合：一次跑遍全部脚本内置自检 |
| `scripts/fixtures/*.json` | 示意任务集 / 结果 / 哈希锁（demo only，非实测） |
| `references/runnable-guide.md` | 输入、输出、退出码、一致性验证、国内适配、引文核验 |
| `references/walkthrough.md` | 玩具级端到端走查（冻结→诊断→蒸馏→门禁→沉淀） |
| `references/failure-recovery.md` | 失败模式 → 现成提示 → 恢复路径 |
| `references/faq.md` | 集中高频问答与不适用清单 |
| `references/claim-boundary.md` | 可声称 / 不可声称的完整对照与依据 |
| `references/four-stage-status.md` | 四段 × 双轨道 × 自动 / 人工 明细 |
| `references/roadmap.md` | T1 / T2 差距、验收标准与状态 |
| `EXAMPLES.md` | 安全措辞、被否决反例、触发语句样例 |
| `CHANGELOG.md` | 版本记录（1.0.0 → 1.0.1 → 1.0.2 → 1.0.3） |

## 边界（务必随引用保留）

- `PASS / 全绿 / N/N` 只表示**冻结基线未退化**，不表示能力变强、语义质量达标或实时闭环已验证。
- 改进对象是技能文档，不是改进器自身；harness 迭代仍靠人工。
- 当前不可声称：「RSIFlow 四段闭环自动落地」「已实现递归自我改进 / RSI」。
- 包内 `5/5`、`22/22` 等数字均为**示意值，非实测**。

## 版本与参考来源

本包版本 1.0.3；参考 RSIFlow: *Adaptive Self-Improvement Workflows with an Evolving Meta-Agent*, arXiv:2610.21791v2（2026-11-02），https://arxiv.org/abs/2610.21791 。本包为独立方法论整理，非官方实现、未复现其实验、未使用其代码；许可：个人非商用。

---

## English summary

Version 1.0.3. A methodology guide plus six zero-dependency runnable scripts (one gate + five assistive tools), with explicit claim boundaries. Run `python scripts/test_all.py` then `python scripts/gate_min.py --self-test`; no install, network, account or vendor binding is required. The five assistive tools only analyse/classify/lint and never auto-edit. `PASS` means frozen baselines did not regress, not capability gain; "RSIFlow four-stage loop implemented automatically" and "recursive self-improvement / RSI achieved" remain prohibited (T1/T2, not started). All bundled numbers are demo values, not measurements; the reference (arXiv:2610.21791v2) is independently verifiable at https://arxiv.org/abs/2610.21791. Full operational detail is in the Chinese sections above.
