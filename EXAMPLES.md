# 措辞实例、触发样例与可照用操作样例

> 两条说明：文中出现的强宣称句子**均为被否决的反例**，只用于说明「不能这么写」；文中所有数字（`22/22`、`5/5` 等）**均为示意值，非实测**，不得当作任何项目的能力证据。

## A. 触发语句样例（解决「不同说法是否都会触发」）

| 类型 | 用户可能怎么说 | 本 skill 该给什么 |
|---|---|---|
| 正例 | 「精简版 RSI 怎么落地」「技能进化怎么过回归门禁」 | 直接给 SOP + 可运行门禁 + 边界声明 |
| 正例 | 「GEPA 进化后怎么防止洗绿」「冻结任务集怎么锁」 | 给禁止项、哈希锁与 `runnable-guide.md` |
| 正例 | 「这句话能不能对外说」「帮我看宣称口径」 | 给速查表与 `claim-boundary.md` 判定 |
| 近似 | 「诊断→选流→蒸馏→门禁怎么做」「把 SKILL.md 瘦身又不丢能力」 | 同上，先确认是否已有冻结任务集 |
| 反例（先澄清） | 「帮我做个能自我进化的 Agent」「直接把模型调强」 | 先说明本包是方法论 + 最小门禁，不构成 RSI 或能力提升 |
| 反例（先澄清） | 「给我一套生产可用的完整闭环系统」 | 先说明需人工确认点，自动写回属 T1 未启动 |

**提问时建议提供的材料**：① 冻结任务集样例（含稳定 id 与期望结果）；② 当前结果 / 失败轨迹；③ 你打算对外写的那句话；④ 希望自动化到什么程度。缺材料时本 skill 会先给保守措辞，不会替你补造证据。

## B. 措辞实例

### 例 1：一句话介绍（安全）

> 本技能由**参考 RSIFlow 方法论内核的「精简版 RSI」流水线**产出——GEPA 反思式进化 + Pareto 双目标（能力保持、篇幅精简），经冻结任务集回归门禁验证后入库。PASS 仅表示冻结基线未退化，不代表能力提升；选流、蒸馏与 harness 迭代仍含人工环节。

判定：**可用**。两个限定词齐全，附防误读声明，说明了人工环节。

### 例 2：一句话介绍（禁止）

> 反例（被否决的写法，禁止对外使用）：「已实现递归自我改进，RSIFlow 四段闭环自动落地，技能能力持续变强。」

判定：**不可用**。三处越线：把后续课题写成当前能力、宣称全自动闭环、把「基线未退化」偷换成「能力变强」。

### 例 3：引用测试数字（安全 / 危险）

- 安全：`22/22 冻结任务通过（示意值，非实测；含义：基线未退化，非能力提升）`
- 反例（被否决）：`22/22 通过，证明技能更聪明了`

判定：数字本身中性，**解释决定性质**；脱离防误读声明与「示意 / 实测」标注的数字会被读成能力证明。

### 例 4：写「下一步」而不是「已做到」

- 安全：`下一阶段课题：把自动选流与 harness 自迭代补齐，届时再评估「四段闭环自动落地」是否成立。`
- 反例（被否决）：`已完成四段闭环，下一步优化性能。`

判定：前者把强宣称放在未来且带验收条件；后者把未做说成已做。

## C. 一次完整可照用操作（从输入到判定）

**输入**：`scripts/fixtures/tasks.json` 与 `results.json` 各 5 条示意任务；`manifest.json` 记录任务集 SHA-256。三个文件的完整内容见 `references/runnable-guide.md` 第 3 节，此处不重复。

**命令与成功输出**：

```bash
python scripts/gate_min.py
```

```text
[PASS] T01
[PASS] T02
[PASS] T03
[PASS] T04
[PASS] T05
SUMMARY: 5/5 passed | exit=0
NOTICE: PASS = frozen baselines did not regress, NOT capability gain; not evidence of RSI or an automatic RSIFlow four-stage loop.
```

`EXIT=0`。可写进报告的表述：「示意冻结任务集 5/5 未退化（示意值，非实测；PASS ≠ 能力提升）」。

**失败输出（把 `T01` 的 `status` 改成 `unavailable` 而仍标 `pass: true`，由 `--self-test` S5 复现）**：

```text
[PROHIBITED] whitewash attempt blocked (EXIT=1).
  - T01: status='unavailable' marked pass=true; relabelling unavailable as validated to pass a gate is forbidden.
[FIX] fix the underlying failure; do not edit the verdict.
SUMMARY: 2/2 passed | exit=1
```

`EXIT=1`。判定：**禁止项优先于逐条结果**，即使逐条都标了 pass 也不能放行。此时正确动作是修底层失败并重跑，不是改 `status`、改 `pass` 或改 manifest。完整失败模式表见 `references/failure-recovery.md`。

**确认结果稳定**：连跑两次比对输出，无差异即一致（`diff` / Windows `fc`），命令见 `references/runnable-guide.md` 第 5 节。

---

## English summary

Trigger examples cover direct, near-match and misleading phrasings, plus the four materials a user should supply. Four wording examples show the safe qualified intro, the rejected strong-claim counter-example, the neutral-numbers case (all figures are demo values, not measurements) and the "next step, not done" pattern. A full runnable round-trip (fixtures → `python scripts/gate_min.py` → `SUMMARY: 5/5 passed | exit=0` with the mandatory notice) and a prohibited-relabelling negative case (`exit=1` even when every task is marked pass) are included. All strong-claim sentences here are rejected counter-examples, never capability descriptions.
