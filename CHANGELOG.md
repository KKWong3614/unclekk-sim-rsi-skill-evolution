# 更新记录

> 版本口径：本包当前版本 **1.0.3**；`SKILL.md` frontmatter、`README.md` 与本文件三处标注一致。更新已发布 Skill 需保持 slug 不变并递增补丁版本。

## 1.0.3（2026-11-10）—— 按 4.8/5 新版 TRACE 测评补齐可用功能与测试覆盖

新版 TRACE 综合评级「优秀」4.8/5（T 4.9 / 国内适配 4.8 / 安全 5.0 / R 4.8 / A 4.9 / C 5.0 / E 4.5）；相对上轮 4.3 提升。短板变为「自动化程度低」+「文件间有一定重复、篇幅偏长」，建议「在保持诚实表述的前提下继续扩充可用功能与测试覆盖」。本版只做**工具扩充、测试覆盖与去重瘦身**，不改变能力边界与宣称口径。

- **扩充可用功能（对应「自动化程度低」）**：新增 5 个零依赖辅助脚本——`claim_lint.py`（宣称边界 linter，可 `--strict` 当硬闸）、`freeze_snapshot.py`（登记 / 重算冻结基线哈希锁）、`diagnose_classify.py`（失败轨迹归 6 桶，只给建议）、`coverage_diff.py`（两次结果集逐条 diff）、`test_all.py`（聚合跑遍全部脚本内置自检）。五者均**只做分析 / 分类 / 检查 / 快照 / 对比，绝不自动改 verdict、绝不自动写回、绝不声称 T1/T2**。`SKILL.md` §5、§8 与 README 文件结构表已露出这 6 个脚本（含 `gate_min.py`）与 `references/walkthrough.md` 玩具级端到端走查。
- **扩充测试覆盖（对应「继续扩充测试覆盖」）**：`test_all.py` 一次跑遍全部脚本内置自检；`gate_min.py` 6 组、`claim_lint.py` 3 组、`freeze_snapshot.py` 1 组、`diagnose_classify.py` 7 组、`coverage_diff.py` 5 组正负例。全绿为发布门槛。
- **去重瘦身（对应「文件间重复、篇幅偏长」）**：压缩 `runnable-guide.md` §7 边界回声与英文镜像、README/claim-boundary/EXAMPLES 英文摘要；`runnable-guide.md` §6 新增「引文可站内核验」说明（arXiv:2610.21791v2 可在 https://arxiv.org/abs/2610.21791 直接核验标题、版本与日期），缓解 E 输出准确性 4.5「包内无法核实」扣分。
- **版本统一**：全包 1.0.2 引用统一改为 1.0.3（`SKILL.md` frontmatter 与正文、`CHANGELOG.md`、`README.md`、`references/roadmap.md`、`references/runnable-guide.md`、`scripts/fixtures/tasks.json`、`scripts/gate_min.py`），并据新 `tasks.json` 重算 `manifest.json` 哈希锁。
- **口径守门**：两限定词「方法论内核」+「精简版」、`PASS = 回归未退化，非能力提升`、T1/T2「当前不可声称」**一字未改**。本版属工具与文档改进，**不构成能力宣称升级**，不改变既有评级结论（维持「通过」）。

## 1.0.2（2026-11-10）—— 同步线上 displayName 改名、版本升 1.0.2

线上 Skill（`skillId=315617`、`slug=unclekk-sim-rsi-skill-evolution`，由 KK 手动改名）的展示名称已改为 **`UncleKK Simplified RSI Skill Evolution / 精简版 RSI 技能进化`**，平台显示版本为 1.0.1。本版把本地 `displayName` 与线上对齐（加 `UncleKK` 前缀、英文 UncleKK 名在前、中文在后），并把本地内容版本从 1.0.1 升到 **1.0.2**，使「平台显示版本」与「包内内容版本」统一为 1.0.2。

- **改名对齐**：`SKILL.md` frontmatter `displayName` 由 `精简版 RSI 技能进化 / Simplified RSI Skill Evolution` 改为 `UncleKK Simplified RSI Skill Evolution / 精简版 RSI 技能进化`；主文档 H1 同步更新。`slug` 不变，仍走同 Skill 更新（不新建）。
- **版本统一**：全包 1.0.1 引用统一改为 1.0.2（`SKILL.md` frontmatter 与正文、`CHANGELOG.md`、`README.md`、`references/roadmap.md`、`references/runnable-guide.md`、`scripts/fixtures/tasks.json`、`scripts/gate_min.py`）。
- **口径守门**：本次仅为「线上改名 + 补丁版本对齐」，**不构成任何能力宣称升级**。两限定词「方法论内核」+「精简版」、`PASS = 回归未退化，非能力提升`、T1/T2「当前不可声称」**一字未改**。

## 1.0.1（2026-11-10）—— 按 TRACE 测评报告逐项改进

测评综合评级「优秀」4.3/5；短板集中在可靠性 R 3.5、规范性 C 4.4、有效性 E 4.2。本版只做**文档准确性、配套可用性与结构精简**，不改变能力边界与宣称口径。

- **准确性（E 输出准确性 4.0）**：把论文引文从 `license` 字段移到正文「参考来源」，补全标题、arXiv 版本 v2、日期与链接，并声明非官方实现；缩短 frontmatter 超长字段以消除平台渲染截断；包内示例数字（`22/22`、`5/5`）统一标注「示意值，非实测」；三处版本标注统一为 1.0.1。
- **可靠性（R 3.5）**：新增 `scripts/gate_min.py` 与 `scripts/fixtures/*.json`——零第三方依赖、可反复执行、输出逐字节稳定的最小回归门禁；含冻结任务集 SHA-256 锁、覆盖度检查、两条禁止项、退出码 `0/1/2/3` 与 6 组内置正负例自检。新增 `references/failure-recovery.md`（失败模式 → 现成提示 → 恢复决策树），并如实说明「刻意不自动批准 / 不自动改 verdict」的防洗绿取舍。
- **适用性（A 4.8）**：`SKILL.md` 增补「前置准备三样」与「不适用 / 请勿直接套用」清单；frontmatter `triggers` 由 5 条扩到 10 条；`EXAMPLES.md` 补触发语句正例 / 近似 / 反例与「提问时应提供哪些材料」。
- **规范性（C 4.4）**：中英全文对照改为「中文正文 + 英文要点摘要」，消除重复；新增 `references/faq.md` 集中 16 条高频问答；`SKILL.md` 增加文档地图，主文档只留要点；`references/runnable-guide.md` 给出完整输入、完整 stdout、退出码与两次运行比对命令。
- **国内适配（T 4.5，诚实披露）**：明确可运行部分零外部依赖、无网络请求、不绑定模型厂商；GEPA / LLM 属可选引擎。**未在特定国内平台实测兼容性**，仅提供自行复验方法，不声称已适配任何具体产品。
- **口径守门**：「方法论内核」与「精简版」两个限定词、`PASS = 回归未退化，非能力提升`、两个强宣称「当前不可声称」、T1/T2「未启动」**一字未改**。本版属配套工具与文档改进，**不构成能力宣称升级**，不改变既有评级结论。

## 1.0.0（2026-11-10）

- 首次发布：把精简版 RSI 技能进化的方法论、SOP 与宣称边界打包成可复用技能。
- 对外命名：`精简版 RSI 技能进化 / Simplified RSI Skill Evolution`，slug `unclekk-sim-rsi-skill-evolution`；未使用早期内部术语。
- 同日曾因对外命名调整，从早期 slug 换到现行 slug 重新发布，内容版本仍为 1.0.0；早期包已由 KK 手动下架，平台侧状态采信 KK 自述。当时只有说明文档，无可执行配套内容。
- 主文档与 README 采用双语，中文在前、英文在后。
- 防幻影声明：主文档 §0 列出当前不可声称的两项强宣称，并登记为 T1 / T2 后续课题，未把「后续课题」写成「当前能力」。
- 明确 `PASS / 全绿 / N/N` 仅表示冻结基线回归未退化；明确四段现状（①② 仅辅助、③④ 引擎自动 + 人工审核、harness 迭代仍人工）。
- 包内不含任何本机绝对路径、口令、API Key、账号标识或隐藏探针相关内容。

---

## English summary

**1.0.1** addresses a TRACE evaluation (4.3/5, "Excellent"): fixes verifiable citation placement and version consistency, adds a zero-dependency runnable regression gate with fixtures and a six-case self-test, adds failure-recovery and FAQ references, condenses full bilingual duplication into Chinese detail plus English digests, and supplies complete input/output examples. All bundled numbers are marked as demo values. Claim boundaries, the two qualifiers, PASS semantics and the not-started status of T1/T2 are unchanged; this is a documentation and tooling improvement, not a capability upgrade. **1.0.0** was the first release of the methodology/SOP/claim-boundary package, later republished under the current slug with the same content version; the early package was manually delisted by the owner. Full history is in the Chinese sections above.
