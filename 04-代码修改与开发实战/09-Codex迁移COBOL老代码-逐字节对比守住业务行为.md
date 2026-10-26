---
id: cobol-legacy-migration
title: 用 Codex 迁移 COBOL 老代码：从 OpenAI 新评测看模型怎么选，再用逐字节对比守住业务行为
seo_title: Codex 迁移 COBOL：读懂 MultiLangBench，用逐字节对比守住行为
description: OpenAI 自测称 GPT-6.1 Sol 在 COBOL 迁移评测上低推理强度准确率 86.6%、调高后 97.9%。本文先讲清数字怎么测、能说明什么，再给出用 Codex 录行为基线、迁移到 Java／Python，并用逐字节对比守住业务行为的工作流。
lede: 老系统现代化最怕「跑得通但算不对」。先读懂官方评测在测什么，再用可复现的字节级对照，把迁移变成可验收的工程。
url: /guides/codex-cobol-legacy-migration
status: published
section: guides
category: D-project-dev
topic: 代码修改与开发实战
content_type: 教程
source_tag: 官方评测/实战
entry_tags: [App, CLI]
difficulty: 进阶
order: 9
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
models: [gpt-6.1-sol, gpt-6-astra, gpt-6-luna]
official_ref: https://openai.com/index/low-resource-programming-languages/
keywords: [Codex COBOL 迁移, MultiLangBench, GPT-6.1 Sol COBOL, 老代码现代化, 逐字节对比, GnuCOBOL]
related: [model-reasoning-effort, dead-code-cleanup-software-maintenance]
howto: true
faq:
  - q: 官方 97.9% 是不是说明可以直接把核心账务迁到生产？
    a: 不是。那是 OpenAI 自研 COBOL 迁移评测上的厂商自测分数，隐藏测试要求可观察输出逐字节一致。官方原文明确：用到生产仍需专家复核，并按业务规则与依赖做测试。评测近饱和不等于你的仓库近饱和。
  - q: MultiLangBench 和 COBOL 迁移评测是一回事吗？
    a: 不是。MultiLangBench 测「用指定语言从零实现兼容 SQLite 的引擎」；COBOL 迁移评测测「把已有 COBOL 迁到 C++／Java／Kotlin／Python／Rust 且行为不变」。前者已开源 openai/MultiLangBench，后者未公开题库。
  - q: 迁移时该优先选 GPT-6 Astra 还是 GPT-6.1 Sol？
    a: 官方迁移数字写在 GPT-6.1 Sol 上（低 effort 86.6%，更高 effort 97.9%）。Astra 在 MultiLangBench 平均通过率更高，适合难啃的跨语言构建与取证。成本敏感的批量迁移可先 Sol + 高 effort，卡壳再换 Astra。以 learn.chatgpt.com/docs/models 与你账号可用模型为准。
---

# 用 Codex 迁移 COBOL 老代码：从 OpenAI 新评测看模型怎么选，再用逐字节对比守住业务行为

> 本文在线版：[codexguide.io/guides/codex-cobol-legacy-migration](https://codexguide.io/guides/codex-cobol-legacy-migration)

> 核对依据：OpenAI 官方文章 [Advancing coding in low-resource programming languages](https://openai.com/index/low-resource-programming-languages/)（页面日期 2026-10-19）；开源评测 [openai/MultiLangBench](https://github.com/openai/MultiLangBench) README；模型入口 [learn.chatgpt.com/docs/models](https://learn.chatgpt.com/docs/models)；GnuCOBOL 官网编译器说明。**文中评测数字均为 OpenAI 厂商自测，已逐项标注。**「我的用法」是落地工作流，不是官方规定。本预览**未**在本机跑通 GnuCOBOL 端到端迁移，示例程序与命令仅作可照抄的流程模板。

把 COBOL 迁到 Java、Python 或 Rust，表面像「换语法」，实际风险在别处：定点数怎么截断、缺记录怎么处理、报表空格和换行是否一致。OpenAI 在 2026-10-19 的文章里强调：这类低资源语言训练语料少，但支撑大量关键业务；无论修 Bug 还是跨语言迁移，都要**保住系统依赖的行为**。

本文做两件事：

1. **读懂两项官方评测**——哪些数字能指导选模型，哪些不能外推到你的生产库。
2. **给出可复用的 Codex 工作流**——先录行为基线，再迁代码，最后用逐字节对比当「金标准」。

和同目录的「死代码清理」篇分工：那篇讲**在同语言仓库里维护**；这篇讲**跨语言迁移且行为不变**。

## OpenAI 这次发布了什么

官方文章标题为 *Advancing coding in low-resource programming languages*（2026-10-19）。背景一句：COBOL、Fortran、Visual Basic 等语言公开代码与文档相对少，模型历史上更弱；OpenAI 写到 COBOL 仍支撑大量银行相关场景（文中引用外部数据：线上银行系统超过 40%、面对面信用卡交易约 80%、ATM 交易约 95%——**这是文章引用的行业表述，不是迁移评测分数**）。

为衡量进展，他们做了**两项互补评测**：

| 评测 | 测什么 | 题库是否公开 |
|---|---|---|
| **MultiLangBench** | 用指定语言**从零**实现兼容 SQLite 的数据库引擎，用同一套数据库文件接口验收 | 是：`openai/MultiLangBench`（Apache-2.0） |
| **COBOL 迁移评测** | 把已有 COBOL 程序迁到 C++／Java／Kotlin／Python／Rust，**隐藏测试**要求可观察输出**逐字节一致**，全部通过才算成功 | **否**（文章未开源该套题） |

一句话：**一个测「会不会用稀缺语言新建复杂系统」，一个测「迁完了行为还在不在」。** 两套分数不能横向直接比大小。

### MultiLangBench：关键数字（厂商自测）

方法摘要（博客 + README）：

- 模型要实现接近 SQLite **3.40.1** 的引擎；候选程序吃初始库文件 + stdin SQL，写出修改后的库；用**真 SQLite 3.40.1** 跑校验查询，输出字符串必须与期望完全一致。
- 从 SQLite TCL Tests 约 **5.1 万**条里改写出约 **2.4 万**条；日常评测建议只跑名称以 `00`／`01`／`02` 开头的 **272** 条（跑全量应注明）。
- 分数是 `(api_cost, test_pass_rate)`；若未用目标语言实现，通过率应记为 0。环境应去掉系统里其他 SQLite 痕迹，且**无外网**。

官方公布（最高／最大推理强度设定下，除非另注）：

| 模型 | 平均通过率 | 备注 |
|---|---|---|
| GPT-6 Astra | **87.4%** | 20 种语言平均；相对 GPT-5.6 Sol 的 **26.8%** |
| GPT-6 Luna | **40.3%** | 估算 API 成本约 **$0.77**/样本，相对 GPT-5.6 Sol 的 **$3.48**，约低 **78%** |
| GPT-5.6 Sol（对照） | **26.8%** | 历史对照基线 |

语言切片（Astra，相对同语言的 GPT-5.6 Sol）：

| 语言 | GPT-5.6 Sol → GPT-6 Astra |
|---|---|
| COBOL | 10.9% → **72.1%**（20 语里最难；Astra 在 19／20 语超过 83%，COBOL 仍约 72%） |
| OCaml | 25.6% → 85.8% |
| Fortran | 21.4% → 83.5% |
| Visual Basic | 27.5% → 89.4% |

Luna 同表也有提升（例如 COBOL 10.9% → 17.1%），但幅度小于 Astra——适合成本优先、任务边界清晰的场景。

### COBOL 迁移评测：关键数字（厂商自测）

官方验收标准写得很硬：

> 隐藏测试要求可观察输出 **byte-for-byte parity**；一次迁移只有**全部**测试通过才算成功。

他们特别点出 COBOL 语义陷阱：例如**定点数默认丢弃多余小数位**，除非显式要求舍入（`ROUNDED`）。若重写时「好心」改成四舍五入，程序能跑、金额却已经错了。

公布结果（**GPT-6.1 Sol**）：

| 设定 | 准确率 | 成本表述（相对 GPT-5.6 Sol） |
|---|---|---|
| 低推理强度（low reasoning effort） | **86.6%** | 同设定下 GPT-5.6 Sol 为 **5.4%**；成本约为后者的 **61%**（文首亦写「便宜约 39%」，与 61% 成本等价） |
| 更高推理强度 | **97.9%** | 官方称评测接近饱和（nearly saturating） |

目标语言集合：C++、Java、Kotlin、Python、Rust。

**务必标清的边界（原文）：** 这类保行为能力对维护与现代化有用，但**用到生产软件仍需专家审查**，并对照该系统的业务规则与依赖做测试。

## 在 Codex 里怎么选模型

模型 ID 以 [Models](https://learn.chatgpt.com/docs/models) 为准，例如：

```bash
codex --model gpt-6.1-sol
# 或会话内 /model
```

结合官方评测 framing + 模型页建议，迁移场景可以这样分工（**我的用法**）：

| 场景 | 优先模型 | 推理强度 | 理由 |
|---|---|---|---|
| 批量、程序边界清晰、已有金样例 | `gpt-6.1-sol` | 先 Medium／High，难例再拉高 | 官方迁移分数写在 Sol 上；成本通常低于 Astra |
| 语义含糊、跨模块取证、要主动查文档／日志 | `gpt-6-astra` | Light～High 视任务 | MultiLangBench 最强；适合「先搞懂再迁」 |
| 抽夹具、对拍脚本、报表格式整理 | `gpt-6-luna` | High 或默认 | 官方定位：清晰、可重复、高吞吐任务 |
| Free／Go 桌面端 | `gpt-6-luna`（若可用） | 按客户端默认起步 | 模型页：Free／Go 在 GPT-5.5 退役后的桌面替代路径含 Luna |

注意：

1. **不要把 97.9% 当成你仓库的通过率预测。** 那是隐藏测试集上的厂商自测。
2. **effort 与代数不对齐。** 模型页写明：不同代模型的 Light／Medium／High 不能一一对应；先用熟悉任务试低档，再按结果上调。
3. **Max／Ultra** 适合最难单题或可拆分子任务的并行；多数「单程序迁移 + 对拍」用不到 Ultra。Luna 支持到 Max，不支持 Ultra。

更完整的 effort 说明见知识库模型选择文（`/guides/codex-model-reasoning-effort`，id：`model-reasoning-effort`）。

## 迁移前先录行为基线

OpenAI 迁移评测的核心验收是**可观察输出逐字节一致**。落到工程里，就是先把「旧世界」的输入／输出冻成金样例，再允许改语言。

### 工具：GnuCOBOL（流程模板）

[GnuCOBOL](https://gnucobol.sourceforge.io/) 是自由的 COBOL 编译器，官网推荐当前稳定版 **3.2**，可在 Linux／BSD／macOS／Windows 等环境生成本地可执行文件。典型命令形态：

```bash
cobc -x -o interest_legacy interest_legacy.cob
./interest_legacy < fixtures/case01.in > fixtures/case01.out
```

本预览环境**未安装／未实跑** GnuCOBOL；下面的小程序只作**教学夹具**。你本机装好 `cobc` 后，应按同样步骤录基线。

### 教学用小程序：利息截断 vs 舍入

下面这段刻意暴露官方文章提到的陷阱——**默认截断 vs `ROUNDED`**：

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. INTEREST-DEMO.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  PRINCIPAL       PIC 9(7)V99 VALUE 10000.00.
       01  RATE            PIC 9(1)V9999 VALUE 0.0325.
       01  INTEREST-CUT    PIC 9(7)V99.
       01  INTEREST-RND    PIC 9(7)V99.
       PROCEDURE DIVISION.
           COMPUTE INTEREST-CUT = PRINCIPAL * RATE
           COMPUTE INTEREST-RND ROUNDED = PRINCIPAL * RATE
           DISPLAY "CUT=" INTEREST-CUT
           DISPLAY "RND=" INTEREST-RND
           STOP RUN.
```

基线纪律：

1. **固定编译选项与方言**（`-std=`、源文件列格式），写进仓库 `README`／`AGENTS.md`。
2. **每个夹具**保存：输入文件、环境变量、预期 stdout／生成文件、编译命令、`cobc --version`。
3. **对比时用字节级工具**，不要只靠肉眼或「看起来差不多」：

```bash
cmp -s fixtures/case01.out migrate/out/case01.out && echo PASS || echo FAIL
# 或
diff -u fixtures/case01.out migrate/out/case01.out
sha256sum fixtures/case01.out migrate/out/case01.out
```

若目标语言侧有意改变换行（CRLF／LF）或尾随空格，必须在迁移规则里**显式声明**，并同步更新金样例——否则「修 diff」会把业务差异冲掉。

## 给 Codex 写迁移规则（AGENTS.md）

把 OpenAI 点名的语义，写成仓库级硬约束。可直接放进项目 `AGENTS.md`（或 Codex 的项目说明）：

```markdown
# COBOL → Python 迁移护栏（本仓库）

## 验收
- 每个迁移单元必须附带 fixtures/<id>.{in,out}；新实现 stdout／产物与 .out **字节级一致** 才算完成。
- 禁止「先让测试变绿再改金样例」。金样例只来自 GnuCOBOL 基线，除非业务方书面确认行为变更。

## COBOL 语义（默认）
- 定点数：未写 ROUNDED 的 COMPUTE／算术按 **截断** 多余小数，禁止默默改成银行家舍入或四舍五入。
- 显式 ROUNDED：必须在目标语言复现同等舍入规则，并在注释中引用源语句行号。
- 缺失记录／文件状态：按源程序 FILE STATUS／AT END 分支复现；不要改成「更合理」的默认值。
- 报表／DISPLAY：保留空格填充、符号、换行；不要 pretty-print。

## 工作方式
1. 只读调查：列出程序入口、COPY 依赖、文件 FD、关键算术与分支。
2. 生成／核对夹具，不改业务代码。
3. 按程序（或按批处理一步）迁移；每步跑 cmp／diff。
4. 失败时先修实现，不改 fixtures。
```

**我的用法：** 护栏越短越好记；把「截断 vs ROUNDED」「缺记录」「报表格式」三条置顶。长篇方言手册可以链到内部 wiki，但验收句必须出现在 AGENTS.md。

## 实操：只读 → 夹具 → 迁移 → 对拍

下列步骤按「可审查的小 PR」设计；在 App 或 CLI 均可。提示词保持可复制。

### 步骤 1：只读调查

```text
只读。不要修改任何文件，不要运行会写盘的命令。

目标：摸清 cobol/interest_legacy.cob（及 COPY 依赖）的业务行为。
请输出：
1) 入口与调用关系；2) 文件／报表 FD；3) 所有算术与是否 ROUNDED；
4) 缺记录／错误分支；5) 建议的 fixtures 输入清单（至少 5 个边界：零本金、最大位、恰好需截断、恰好需舍入、缺记录）。
把事实、推断、未知项分开写。
```

调查习惯可复用知识库「只读调查」文（`/guides/codex-zhi-du-diao-cha-xian-ba-xiang-mu-mo-qing-chu-zai-gai-dai-ma`）。大仓库多模块见「大仓库与历史代码」文（`/guides/codex-yue-du-da-cang-ku-duo-mo-kuai-yu-li-shi-dai-ma`）。

### 步骤 2：生成测试夹具（仍不改业务）

```text
在 fixtures/ 下为调查清单生成输入文件与录制脚本 record_baseline.sh：
- 用 cobc -x 编译现有 COBOL；
- 对每个 case 重定向 stdin／stdout；
- 记录 cobc --version 与完整命令到 fixtures/MANIFEST.md。
不要改 .cob 源文件。跑完后用 sha256sum 列出所有 .out。
```

### 步骤 3：按程序迁到目标语言

```text
把 cobol/interest_legacy.cob 迁到 python/interest_legacy.py。
约束见 AGENTS.md。交付：
1) 可执行入口（同样从 stdin 读、向 stdout 写）；
2) 简短注释标明每条 COMPUTE 对应的截断／ROUNDED；
3) 不要改 fixtures/。
完成后运行：bash scripts/byte_compare.sh
若有 FAIL，只改 Python，直到全部 PASS。
```

`byte_compare.sh` 骨架：

```bash
#!/usr/bin/env bash
set -euo pipefail
fail=0
for inn in fixtures/*.in; do
  id=$(basename "$inn" .in)
  python/interest_legacy.py < "$inn" > "migrate/out/${id}.out"
  if ! cmp -s "fixtures/${id}.out" "migrate/out/${id}.out"; then
    echo "FAIL $id"
    diff -u "fixtures/${id}.out" "migrate/out/${id}.out" || true
    fail=1
  else
    echo "PASS $id"
  fi
done
exit "$fail"
```

### 步骤 4：差异纪律

| 情况 | 正确反应 | 错误反应 |
|---|---|---|
| `CUT=` 行差 0.01 | 检查是否把截断写成了四舍五入 | 改金样例「迁就」新语言 |
| 仅换行符不同 | 统一 LF，或在规则里声明并重录基线 | 忽略 diff，合并 |
| 空格填充不同 | 按 PIC／报表子句复现填充 | 用 `.strip()`「方便对齐」 |
| 某边界从未覆盖 | 先补基线再迁 | 用生产流量碰运气 |

官方评测用**隐藏**测试逼出这类差异；你的仓库要用**可见金样例 + CI** 扮演同一角色。

## Fortran／Visual Basic 也能套用同一骨架

MultiLangBench 显示 Fortran、Visual Basic 随 GPT-6 Astra 同样大幅上升（厂商自测：Fortran 21.4%→83.5%，VB 27.5%→89.4%）。跨语言迁移时，把「逐字节可观察输出」骨架留下，把语义护栏换成该语言的高危点：

| 语言 | 额外核对 |
|---|---|
| Fortran | 浮点模型、隐式类型、数组下标约定、I/O 格式串与记录长度 |
| Visual Basic | 银行家舍入 vs 显式舍入、Option Strict、默认值与空值、区域设置影响的数字格式 |
| COBOL（再强调） | 定点数截断／`ROUNDED`、文件状态、报表空格与编辑符号 |

**不要**假设「模型在 MultiLangBench 分数高 → 迁移自动安全」。MultiLangBench 测的是**新建 SQLite 兼容引擎**，不是你的账务批处理。

## 边界：分数不等于可以上生产

汇总必须守住的边界：

1. **数字来源：** 本文所有通过率／成本均为 OpenAI **自研评测上的厂商自测**；COBOL 迁移题库未公开，无法第三方复现 97.9%。
2. **近饱和 ≠ 你的近饱和：** 官方写 nearly saturating 的是**该评测**；生产系统有中间件、JCL、编码页、联机协议与未文档化规则。
3. **专家复核不能省：** 原文明确要求 expert review，并按业务规则与依赖测试。
4. **金样例治理：** 谁有权改 fixtures，要走变更单；否则「对拍通过」会失去意义。
5. **本预览未实跑 GnuCOBOL：** 合并进知识库前，建议在真实小程序上走通「录基线 → 迁移 → `cmp`」并更新 `verified_on`。

## 接下来读什么

- 模型与推理强度 → `/guides/codex-model-reasoning-effort`（id：`model-reasoning-effort`）
- 同目录：清理死代码与过期实验 → `/guides/codex-dead-code-cleanup-software-maintenance`（id：`dead-code-cleanup-software-maintenance`）
- 只读调查习惯 → `/guides/codex-zhi-du-diao-cha-xian-ba-xiang-mu-mo-qing-chu-zai-gai-dai-ma`
- 大仓库与历史代码 → `/guides/codex-yue-du-da-cang-ku-duo-mo-kuai-yu-li-shi-dai-ma`

## 参考资料

- [Advancing coding in low-resource programming languages](https://openai.com/index/low-resource-programming-languages/)（OpenAI，2026-10-19）
- [openai/MultiLangBench](https://github.com/openai/MultiLangBench)（Apache-2.0；SQLite 3.40.1／272 条日常子集等以 README 为准）
- [Models｜ChatGPT Learn](https://learn.chatgpt.com/docs/models)（`gpt-6.1-sol`／`gpt-6-astra`／`gpt-6-luna`）
- [GnuCOBOL](https://gnucobol.sourceforge.io/)（当前稳定版说明：3.2）

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
