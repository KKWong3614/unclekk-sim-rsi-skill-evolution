# 高频问题解答（FAQ）

> 集中回答测评与上手中反复出现的问题。凡涉及宣称，答案都带边界声明。

## 一、定位与宣称

**Q1：这个 skill 能说「基于 RSI 的技能进化」吗？**
可以，但必须用限定式：**「基于 RSIFlow 方法论内核的精简版 RSI 技能进化」**。「方法论内核」与「精简版」两个限定词缺一不可，删掉任一个就会滑向夸大。不可说「已实现递归自我改进 / RSI」。

**Q2：`PASS / 全绿 / N/N` 到底证明什么？**
只证明**冻结基线的回归未退化**。不证明技能能力变强、不证明语义质量达标、不证明实时业务闭环已验证。引用任何数字都要同时附这句。

**Q3：为什么说改进对象不是改进器？**
GEPA 进化的是技能文档（SKILL.md 文本）；任务集、判据、harness 版本仍由人迭代。改进器不能改自己，因此严格学术意义的 RSI 不成立。

**Q4：包里 `5/5`、`22/22` 这类数字是实测吗？**
不是。`scripts/fixtures/` 的 `5/5` 是随包**示意数据（demo only）**；`EXAMPLES.md` 中的 `22/22` 是措辞示例中的**示意数字**。两者都不是任何项目的实测结论，不得当作能力证据。真实数字必须来自你自己的冻结任务集并附证据路径。

**Q5：为什么英文部分这么短？**
为减少中英全文对照造成的重复。按发布规范保留「中文在前、英文在后」，英文改为要点摘要，完整细节以中文正文为准。

## 二、上手与前置

**Q6：开始之前具体要准备什么？**
最小三样：① 一份确定性任务集（有稳定 id 与期望结果）；② 每个任务的可复算结果（含 `status` 与失败原因）；③ 一次人工确认点（谁批准写回、如何回滚）。可运行部分另需 Python 3.9+ 与 UTF-8 终端，不需要联网、账号或 API Key。清单见 `runnable-guide.md` 第 2 节。

**Q7：哪些情况不适合用这个 skill？**
- 没有冻结任务集，或任务集仍在频繁变动；
- 目标是「让技能变聪明 / 语义质量达标」——本门禁只判退化，不判方向；
- 需要无人值守自动写回生产、自动改判据或自动修复——当前需人工确认，属 T1 课题；
- 想找一套开箱即用的完整 RSI 系统或生产工程源码——本包是方法论 + 最小参考实现；
- 需要在特定平台 / Agent 宿主上「已验证兼容」的承诺——未做该实测，见 `runnable-guide.md` 第 6 节。

**Q8：说什么话会触发这个 skill？**
正例：「精简版 RSI 怎么落地」「技能进化怎么过回归门禁」「GEPA 进化后怎么防止洗绿」「这句话能不能对外说」。近似说法：「诊断→选流→蒸馏→门禁怎么做」「冻结任务集怎么锁」「宣称边界怎么把守」。反例（建议先澄清需求）：「帮我做个能自我进化的 Agent」「直接把模型调强」。触发词表在 `SKILL.md` frontmatter，语句样例见 `EXAMPLES.md`。

**Q9：向我提问时应该提供哪些材料？**
任务集样例、当前结果/失败轨迹、打算对外写的那句话，以及你希望自动化到什么程度。缺材料时本 skill 会先按边界判定给出保守措辞，不会替你补造证据。

## 三、运行与故障

**Q10：脚本能在生产环境直接用吗？**
它是零依赖的**参考实现**，只演示「冻结判定 + 两条禁止项」，不含隐藏探针、完整性账本、隔离区或 LLM 调用。生产使用前需替换为自己的任务集、补授权链与回滚，并自行做安全与兼容性验证。

**Q11：哈希不匹配怎么办？**
先恢复基线；若是确有理由的基线变更，走 `failure-recovery.md` 第 4 节的授权 from→to 链再重算。**禁止直接改 `manifest.json` 让门禁变绿**。

**Q12：退出码 `1` 但 SUMMARY 显示 `2/2 passed`，是不是 bug？**
不是。禁止项优先于逐条结果：任务都被标 pass，但命中「不可用改判为已验证」或「批量批准」时整体仍判不通过。设计说明见 `runnable-guide.md` 第 4 节。

**Q13：每次跑结果会变吗？**
不会。输出无时间戳、无路径、无随机量，任务按 id 排序。用 `runnable-guide.md` 第 5 节的两次运行比对即可确认。

**Q14：国内环境能用吗？**
可运行部分零外部依赖、无网络请求，纯标准库；GEPA / LLM 属可选引擎，不绑定任何厂商。**未在特定国内平台做兼容性实测**，请按第 5 节自行复验，不声称已适配具体产品。

## 四、课题与升级

**Q15：T1 / T2 什么时候能改成「已实现」？**
只有达到 `roadmap.md` 的验收标准（零人工决策且逐段留痕、独立复算一致、负向用例阻断绕过；自改可第三方复算并可回滚）后，才允许同步升级 `SKILL.md` §0/§4、`claim-boundary.md` 与本文件，并保留升级依据与证据路径。**当前状态：未启动 / 当前不可声称。**

**Q16：能不能为了对外好看，把「精简版」三个字去掉？**
不能。去掉限定词即构成幻影声明风险，也是历次审计明确要求降级的写法。宁可被说保守，也不能把未做说成已做。

---

## English summary

This FAQ centralises the recurring questions: qualified wording for RSI, the exact meaning of PASS (no regression only), the demo-only nature of all bundled numbers, the minimum inputs needed to start, explicit out-of-scope scenarios, trigger phrasing examples, hash-mismatch recovery, the deliberate precedence of prohibited items over per-task results, deterministic output, domestic-environment honesty, and the conditions under which T1/T2 could ever be upgraded from "not claimable". Full answers are in the Chinese sections above; see `claim-boundary.md` and `roadmap.md` for the authoritative matrices.
