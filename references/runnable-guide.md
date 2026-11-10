# 可运行配套内容使用指南

> 本包此前只有说明文档。本页与 `scripts/gate_min.py` 是**唯一可直接执行**的部分，用来把「冻结任务集回归门禁」这一步从文字变成能反复跑、结果可逐字节比对的最小闭环。

## 1. 它是什么、不是什么

- 是：零第三方依赖的**参考实现**，只做三件事——校验冻结任务集哈希、检查覆盖度与两条禁止项、逐条判定回归结果。
- 不是：任何生产工程的门禁代码副本；不含隐藏探针池、完整性账本、OS 级账户隔离、GEPA 引擎或 LLM 调用。**它不构成「四段闭环自动落地」，也不构成 RSI。**
- 输出里的 `5/5` 是随包附带的**示意数据（demo only，非实测）**；替换成你自己的任务集前，不得把该数字当作任何项目的实测结论。

## 2. 前置准备清单（开箱即用所需的最小集）

| 需要 | 具体要求 |
|---|---|
| Python | 3.9 及以上，仅用标准库（`argparse` / `hashlib` / `json` / `pathlib` / `tempfile`） |
| 终端编码 | UTF-8；脚本会尝试把 stdout 切到 UTF-8 |
| 文件 | `scripts/gate_min.py` + `scripts/fixtures/` 下 `tasks.json` / `results.json` / `manifest.json` |
| 不需要 | 联网、账号、API Key、模型服务、数据库、管理员权限、境外接口 |

不需要任何安装步骤。在本包根目录执行：

```bash
python scripts/gate_min.py
python scripts/gate_min.py --self-test
python scripts/gate_min.py --json
python scripts/gate_min.py --fixtures <你的 fixtures 目录>
```

Windows 下若 `python` 不可用，改用 `py -3` 或你的解释器全路径，其余不变。

## 3. 完整输入样例

`scripts/fixtures/tasks.json`（节选，完整文件随包提供）：

```json
{
  "suite": "demo-frozen-suite",
  "version": "1.0.3",
  "tasks": [
    {"id": "T01", "name": "guard behaviour", "expected": "pass"},
    {"id": "T02", "name": "consistency check", "expected": "pass"}
  ]
}
```

`scripts/fixtures/results.json`（节选）：

```json
{
  "suite": "demo-frozen-suite",
  "results": [
    {"id": "T01", "pass": true, "status": "validated", "reason": ""},
    {"id": "T02", "pass": true, "status": "validated", "reason": ""}
  ]
}
```

`scripts/fixtures/manifest.json`：

```json
{
  "suite": "demo-frozen-suite",
  "tasks_sha256": "6f5dee260d6e7daae6941bdfc3c8cdb23f038f708d34a031da35229ef7c87a08",
  "notice": "frozen baseline; any edit to tasks.json requires an authorized change chain and a recomputed hash"
}
```

哈希口径必须与脚本一致：对 `tasks.json` 解析后的对象按 `sort_keys=True, ensure_ascii=False, separators=(",", ":")` 序列化后取 UTF-8 字节的 SHA-256。**换成自己的任务集后必须重算**：

```bash
python -c "import json,sys;sys.path.insert(0,'scripts');import gate_min;print(gate_min._sha256(json.load(open('scripts/fixtures/tasks.json',encoding='utf-8'))))"
```

把打印结果填回 `manifest.json` 的 `tasks_sha256`。**禁止为了让门禁变绿而直接改哈希值**，那等于取消冻结基线。

## 4. 完整输出样例

成功（退出码 `0`）：

```text
[PASS] T01
[PASS] T02
[PASS] T03
[PASS] T04
[PASS] T05
SUMMARY: 5/5 passed | exit=0
NOTICE: PASS = frozen baselines did not regress, NOT capability gain; not evidence of RSI or an automatic RSIFlow four-stage loop.
```

失败（禁止项被拦，退出码 `1`，由 `--self-test` 的 S5 复现）：

```text
[PROHIBITED] whitewash attempt blocked (EXIT=1).
  - T01: status='unavailable' marked pass=true; relabelling unavailable as validated to pass a gate is forbidden.
[FIX] fix the underlying failure; do not edit the verdict.
...
SUMMARY: 2/2 passed | exit=1
```

注意最后一行的 `2/2` 与 `exit=1` 并存：任务逐条都标了 pass，但禁止项命中，整体仍判不通过。**禁止项优先于逐条结果**。

输入错误（退出码 `2`，由 `--self-test` 的 S3 复现）：

```text
[ERROR] frozen task set hash mismatch (EXIT=2, fail-closed).
[FIX] restore tasks.json, or go through an authorized baseline change.
[FIX] never edit manifest.json just to make the gate green.
```

退出码约定：`0` 全通过；`1` 回归失败或禁止项命中；`2` 输入/完整性错误；`3` 自检失败。`--json` 把同样的内容包成 `{"exit": ..., "lines": [...]}` 便于程序消费。

## 5. 重复运行一致性验证（对应「运行稳定性」）

输出刻意不含时间戳、路径与随机量：任务按 id 排序，哈希由内容决定。可直接比对两次运行：

```bash
python scripts/gate_min.py > run_a.txt
python scripts/gate_min.py > run_b.txt
diff run_a.txt run_b.txt    # Windows: fc run_a.txt run_b.txt
```

无差异即为一致。`--self-test` 每次也会用临时目录重跑 6 组固定用例，不写工作区、不留残留。`scripts/fixtures/` 之外的改动不应影响输出。

## 6. 国内环境适配说明（诚实披露）

- 本可运行部分**不调用任何外部服务**，无网络请求、无 SDK、无境外 API，因此不存在「接入国内服务」的兼容缺口；纯标准库实现，在国内常见 Windows / Linux 环境下可直接跑。
- 中文说明完整，主文档与参考文档均为中文在前；命令行输出用 ASCII，避免终端编码差异。
- SOP 中的 GEPA / LLM 环节属于**可选引擎**，本包只描述用法，不绑定任何具体模型或厂商。若改用国内模型服务，需自行按 OpenAI 兼容接口适配并自行验证效果。
- **未在特定国内平台、特定发行版或特定 Agent 宿主上做兼容性实测**；上述判断基于「零外部依赖」这一事实，实际落地仍请按第 5 节自行复验。此处不声称已适配任何具体产品。
- **引文可站内核验**：参照论文 *RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent*, arXiv:2610.21791v2（2026-11-02）可在 https://arxiv.org/abs/2610.21791 直接核验标题、版本与日期；本包为独立方法论整理，非官方实现、未复现其实验、未使用其代码。

## 7. 边界（以主文档为准）

本可运行部分**不改变任何宣称边界**。完整边界与口径以 `SKILL.md` §0 / §6 与 `references/claim-boundary.md` 为准；`PASS / 全绿 / N/N` 一律只表示**冻结基线回归未退化**，不代表能力变强、语义质量达标或实时闭环已验证，当前亦不可声称「RSIFlow 四段闭环自动落地」与「已实现递归自我改进 / RSI」。详见 `claim-boundary.md` 与 `faq.md`。

---

## English summary

A zero-dependency, runnable reference gate (`scripts/gate_min.py`) ships with fixtures, a six-case self-test, deterministic output and explicit exit codes 0/1/2/3. It checks a frozen-task SHA-256 lock, coverage and two prohibited whitewash patterns; it never auto-approves or auto-repairs. All `5/5` figures are demo data, not measurements. It makes no network calls and binds to no vendor; domestic-platform compatibility is untested. PASS means no regression, not capability gain, and is not RSI evidence. The five companion scripts (`claim_lint`, `freeze_snapshot`, `diagnose_classify`, `coverage_diff`, `test_all`) only analyse/classify/lint and never auto-edit. Full input/output examples and the hash-refresh procedure are in the Chinese sections above.
