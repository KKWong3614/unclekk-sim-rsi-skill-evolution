# 实战样例：照着一个玩具技能走完一轮「诊断 → 蒸馏 → 门禁」

> 本页把 `SKILL.md` 的 SOP 落成一次**可照做的**最小闭环。它只演示「改进技能文档（SKILL.md 文本）」这一步——也就是本包真实能做到的范围。**四段闭环自动落地（T1）与递归自我改进 / RSI（T2）均不在本页范围内，当前不可声称。**

演示目标：把一个啰嗦的玩具 `weather-skill` 的 SKILL.md 压瘦、补上防误读声明，并用回归门禁确认「没把原有能力改坏」。

---

## 0. 准备：冻结基线（人工 + 锁）

先把「当前长什么样」作为冻结任务集登记下来，后面只比「回归未退化」。

```bash
# 把现有技能的文本要点抽成确定性任务集 tasks.json（示意）
python scripts/freeze_snapshot.py --tasks scripts/fixtures/tasks.json
# 生成 manifest.json，内含 tasks_sha256 锁
```

要点：任务集必须**稳定 id + 期望结果**，且可复算。换你自己的技能时，替换 `tasks.json` 后**必须重算哈希**（不要手改 `manifest.json` 去匹配被改的任务集）。

---

## 1. 诊断（辅助工具出建议，人确认）

把一次跑通的轨迹或失败记录整理成 traces，用分类诊断器归类瓶颈：

```bash
python scripts/diagnose_classify.py --input my-traces.json
```

输出示例：

```
DIAGNOSE: 3 classified, 0 unclassified
[compression] 2: T01,T03
    advice: 精简 SKILL.md 时保留要点、细节下沉 references；用文档地图降低主文档篇幅。
[capability] 1: T02
    advice: 确认是否超出当前方法论内核范围；属 T1/T2 后续课题的，登记为「下一步」而非当前能力。
```

这一步只产**建议**。是否采纳、选哪条工作流，由人确认（对应 `SKILL.md` ② 选流）。

---

## 2. 蒸馏（人工编辑，本包不代写）

下面是一次**人工**蒸馏的 before/after 文本 diff。本包**不自动改写**，这里展示的是人照着建议做的结果。

**Before（冗长、缺边界声明）：**
```markdown
# Weather Skill
This skill gets the weather. It can do a lot of things.
We made it really good and it improves itself over time.
Just call it and it works perfectly.
```

**After（精简版 + 限定式口径 + 防误读声明）：**
```markdown
# Weather Skill（精简版）

> 本技能只做天气查询的确定性调用；它不是自动进化系统，能力边界由人维护。

## 能做什么
- 按城市名返回当前天气（数据源需自行配置）。

## 不能做什么 / 当前不可声称
- 不声称「实时闭环已验证」「能力自我提升」。
- 输出依赖外部数据源，本技能不保证可用性。

## 回归口径
PASS = 本次改动未破坏既有天气查询能力，不代表能力变强。
```

要点（对应 `SKILL.md` ③ 蒸馏）：删掉「improves itself / works perfectly」这类夸大表述，补「不能做什么」与「PASS = 回归未退化」。**蒸馏产物由人写回并确认**——这正是 T1 的「写回生产需人确认」要求。

---

## 3. 门禁（可运行部分，直接跑）

把改动后的技能要点重新落成 tasks/results，跑回归门禁确认没把基线改坏：

```bash
python scripts/gate_min.py --self-test      # 先确认工具本身正常
python scripts/gate_min.py                 # 跑你的冻结任务集
python scripts/coverage_diff.py --before base-results.json --after new-results.json
```

判定口径（务必随结果一起保留）：

- `SUMMARY: N/N passed | exit=0` 只表示**冻结基线回归未退化**，不表示能力变强、语义质量达标或实时闭环已验证。
- 若 `coverage_diff` 出现 `REGRESSED` 列表，说明蒸馏误删了能力——回退并重做第 2 步。

---

## 4. 沉淀（人工确认后写回）

门禁全绿后，由人确认并把新 SKILL.md 写回生产，登记 from→to 变更链、授权来源与回滚路径。本包不自动写回。

---

## 诚实边界（本页不声称）

- 本页是**方法论演示**，玩具数据均为示意；真实技能请用你自己的确定性任务集。
- 诊断 → 建议、蒸馏 → 人工、写回 → 人工：三处人工环节一个都没省。
- T1（四段闭环自动落地）、T2（已实现 RSI）**未启动、当前不可声称**；达标前本页所述流程始终是「人主导 + 外接门禁」的形态。
