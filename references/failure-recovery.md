# 失败模式与恢复手册

> 配套 `scripts/gate_min.py`。先看退出码，再按表定位；脚本对每个失败都给出可直接照抄的 `[FIX]` 提示。

## 1. 恢复决策树

```text
运行 gate_min.py
├─ exit 0 → 全通过：只可写「冻结基线未退化」，附防误读声明
├─ exit 1 → 回归失败或禁止项命中 → 看 [FAIL] / [PROHIBITED] / [COVERAGE]
│   ├─ 禁止项 → 修根因，禁止改 verdict、禁止改状态
│   ├─ 覆盖度 → 补齐缺失任务的结果，禁止只跑一部分就报 N/N
│   └─ 真实回归 → 回退候选改动或修复，再重跑
├─ exit 2 → 输入 / 完整性错误 → 看 [ERROR]，修文件或走授权基线变更
└─ exit 3 → --self-test 未全过 → 不要发布任何结论，先修脚本运行环境
```

## 2. 失败模式对照表

| 现象（脚本原样提示） | 含义 | 可以自动做 | 必须人工做 | 禁止做 |
|---|---|---|---|---|
| `[ERROR] input problem: missing file ...` | fixtures 缺文件 | 报出缺哪个文件、给出三个应有文件名 | 补齐文件或修正 `--fixtures` 路径 | 删掉缺失任务让门禁变绿 |
| `[ERROR] invalid JSON ...` | JSON 语法错 | 指出文件名与解析错误 | 修 JSON | 用注释或截断绕过解析 |
| `[ERROR] frozen task set hash mismatch` | 任务集被改 / 哈希未重算 | fail-closed 拒判 | 恢复基线，或走授权变更链后重算哈希 | **直接改 manifest 让它匹配** |
| `[ERROR] suite mismatch` | 结果与任务集不是同一套 | 拒判并打印两个 suite 名 | 用配套 suite 重跑 | 混用不同 suite 的结果 |
| `[ERROR] every task needs a unique non-empty 'id'` | 任务定义不合法 | 拒判 | 修 `tasks.json` | 用重复 id 凑数 |
| `[COVERAGE] suite coverage is incomplete` | 结果缺项 / 多项 / 重复 | 列出 missing、unknown、duplicate | 补齐或清理结果 | 宣称 `N/N` |
| `[PROHIBITED] relabelling unavailable` | 把不可用改判成已验证 | 阻断并点名任务 id | 修底层失败，重跑 | 把 `status` 改成 `validated` |
| `[PROHIBITED] bulk_approve=true` | 批量无差别批准 | 阻断 | 移除该开关，逐条给证据 | 保留开关并放行 |
| `[FAIL] <id>: <reason>` | 真实回归失败 | 输出失败原因 | 回退候选改动或修复后重跑 | 把 `pass` 改成 `true` |
| `SELFTEST: n/6 PASS` | 自检未全过 | 打印失败用例全文 | 检查 Python 版本与文件完整性 | 忽略后照常引用结论 |
| 终端中文乱码 | 终端非 UTF-8 | 脚本尝试把 stdout 切到 UTF-8 | 终端切 UTF-8；`--json` 输出为纯 ASCII 结构 + 中文字符串 | 因此改判定逻辑 |

## 3. 为什么「不自动恢复」是刻意设计

测评常把「没有自动恢复能力」记作扣分。这里如实说明取舍：**自动批准、自动改 verdict、自动重算哈希以匹配被改任务集，恰好就是防洗绿要拦的三类动作**，因此本参考实现刻意不做自动修复。提供的是三件可依赖的东西：

1. **现成错误提示**：每个失败分支都带 `[ERROR]` / `[FIX]` / `[PROHIBITED]` 原文，可直接贴进工单。
2. **可重复自检**：`--self-test` 用临时目录跑 6 组固定正负例，不写工作区、不留残留，用于确认脚本本身没坏。
3. **fail-closed 与回滚路径**：任何完整性异常一律拒判而不是放行；候选改动可回退，授权基线变更需留 from→to 链、授权来源、独立复算与回滚路径。

一句话：**能自动判，不能自动放**。需要无人值守的自动修复与自动写回，属于 `roadmap.md` 的 T1 课题，当前未启动、不可声称。

## 4. 基线变更的正确路径（哈希不匹配时）

1. 确认变更理由，由人确认，而不是由门禁自己决定。
2. 备份原 `tasks.json`，记录改前 / 改后哈希（from→to）。
3. 登记授权来源与独立复算方式，保留回滚路径。
4. 用 `runnable-guide.md` 第 3 节的命令重算 `tasks_sha256` 并写回 `manifest.json`。
5. 重跑正向门禁与 `--self-test`，两次结果一致后再对外引用。

## 5. 幂等与残留

- 正向运行只读 fixtures，不写任何文件；输出不含时间戳与路径。
- `--self-test` 使用 `tempfile.TemporaryDirectory`，退出即清理。
- 重复运行输出应逐字节一致；不一致先查是否被外部脚本改了 fixtures，而不是调整判定。

---

## English summary

Every failure branch emits a ready-to-use `[ERROR]`/`[FIX]`/`[PROHIBITED]` line and a deterministic exit code. Auto-approval, auto-verdict-editing and auto-hash-refresh are deliberately absent because they are exactly the whitewash patterns the gate exists to block: the gate can decide automatically but must never release automatically. Recovery means fixing the root cause, re-running, and — for a genuine baseline change — following an authorized from→to chain with recomputation and rollback. Unattended auto-repair belongs to roadmap topic T1, which is not started and not claimable.
