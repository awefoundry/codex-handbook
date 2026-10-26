---
id: codex-composer-predictions
title: Codex Composer Predictions 怎么用：桌面端 Tab 接受下一步提示、Settings 开关，以及为什么不占用量额度
seo_title: Codex Composer Predictions：Tab 接受提示、开关与额度
description: Composer Predictions 会在 Codex 桌面端根据当前对话，在输入框里建议下一条消息。本文按官方文档说明使用条件、Tab 接受后怎么改、它用了哪些上下文、怎么在 Settings 里关掉，以及为什么生成建议本身不计入用量。
lede: 按 Tab 只是把建议放进输入框，不会替你发送。生成建议不花额度，发出去才算。
url: /guides/codex-composer-predictions
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 基础
order: 14
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-23
date_modified: 2026-10-23
models: [gpt-6-astra, gpt-6.1-sol]
official_ref: https://learn.chatgpt.com/docs/features/composer-predictions
keywords: [Codex Composer Predictions, Codex Tab 提示, Show predictions, Codex 下一步提示]
related: [usage-limits-credits]
faq:
  - q: 按了 Tab 会直接发出去吗？
    a: 不会。Tab 只把建议放进输入框，变成可编辑的草稿，要你自己检查后再发送。
  - q: 生成建议会消耗额度吗？
    a: 官方写明生成预测不计入 Codex 用量限制，也不消耗 credits。你发送消息（包括接受后的建议）时，才按正常用量和计费规则算。
  - q: 我是 Plus 或 Business 用户，为什么看不到？
    a: 官方目前只对年满 18 岁、使用个人 ChatGPT Pro 套餐、所在地区受支持的用户提供这个 beta。
---

# Codex Composer Predictions 怎么用：桌面端 Tab 接受下一步提示、Settings 开关，以及为什么不占用量额度

> 本文在线版：[codexguide.io/guides/codex-composer-predictions](https://codexguide.io/guides/codex-composer-predictions)

> 核对依据：learn.chatgpt.com《Composer Predictions》，2026-10-23 核对。功能目前是 beta，以官方文档为准。

和 Codex 来回做一个任务时，很多时间其实花在想下一句怎么说上：让它跑测试、让它解释某处改动、让它继续下一步。Composer Predictions 就是给这一步用的。Codex 回复完以后，它根据当前对话在输入框里给出一条建议，你按 Tab 就能拿来用。

> **先确认你能不能用**
>
> - 功能目前是 **beta**
> - Codex **桌面端已更新到最新版本**
> - 账号是**个人 ChatGPT Pro** 套餐
> - **年满 18 岁**，且所在**地区受支持**
> - 在桌面端的**本地线程或 SSH 线程**里使用
> - 模型是 **GPT-6 Astra** 或 **GPT-6.1 Sol**
> - 符合条件的用户**默认开启**
>
> 只要有一条不满足，Settings → General → Composer → Show predictions 这个开关通常不会出现。
>
> 中文界面的菜单名可能和上面的英文不同，按位置找：打开设置，在「通用」页里找 Composer 相关区域，里面控制是否显示预测建议的那个开关。

## 使用条件

官方列的条件比较严，先对一遍：

| 条件 | 官方要求 |
| --- | --- |
| 客户端 | Codex 桌面端（需更新到最新版本） |
| 账号 | 个人 ChatGPT Pro 套餐 |
| 年龄与地区 | 年满 18 岁，所在地区受支持 |
| 线程类型 | 桌面端的本地线程和 SSH 线程 |
| 模型 | GPT-6 Astra、GPT-6.1 Sol |
| 状态 | beta，符合条件的用户默认开启 |

CLI、IDE 扩展和网页端，官方文档里都没有提到。

## 怎么用

1. 在受支持的线程里发一条消息。
2. Codex 回复完后，看输入框里有没有出现建议。
3. 想用就按 **Tab**。建议文字会变成输入框里的草稿，可以编辑。
4. 检查、改好，再自己发送。

不想用就直接打字，不用等它出建议。接受建议只是往输入框里填文字，**不会替你发送**。

一个实用的习惯：建议里如果出现「运行」「部署」「删除」之类的动作，发送前读一遍。它只是根据对话猜你下一步想说什么，不代表这一步该做。

## 它用了哪些上下文

官方说明：

- 预测只用**当前线程**里的对话。
- 如果线程里已经有之前工作或已连接应用带进来的内容，这些内容会影响预测。
- 预测**不会自己去查 Memories**，也不会自己从已连接的应用里取数据。
- 开了 Memories 的话，线程里已经有的记忆内容会让预测更个性化；关掉 Memories 也能用预测。

所以，建议不准时，多半是当前对话里的信息不够，和你的历史记录关系不大。

## 怎么关，算不算额度

开关位置：**Settings → General → Composer**，里面的 **Show predictions**。

额度规则官方写得很清楚：

- **生成预测不计入 Codex 用量限制，也不消耗 credits。**
- 你**发送**消息时，包括发送接受过的建议，按正常的 Codex 用量和计费规则计算。

所以不用为了省额度去关它。想关通常是因为觉得干扰，或者在录屏、演示时不希望输入框里冒出东西。

## 和编辑器里的 Tab 补全有什么不同

| | Composer Predictions | 编辑器代码补全 |
| --- | --- | --- |
| 补的是什么 | 你要发给 Codex 的下一条消息 | 代码 |
| 出现位置 | Codex 桌面端输入框 | 编辑器里的代码 |
| 接受后 | 变成可编辑草稿，需手动发送 | 直接插入代码 |
| 依据 | 当前线程的对话 | 当前文件和项目上下文（视工具而定） |

它不会改你的代码文件，只是帮你写下一条提示。

## 没有出现建议，按这个顺序查

1. **版本**：桌面端是否已更新。
2. **账号**：是不是用个人 ChatGPT Pro 登录。官方文档只列了个人 ChatGPT Pro。
3. **线程**：是本地或 SSH 线程吗？
4. **模型**：当前线程用的是 GPT-6 Astra 或 GPT-6.1 Sol 吗？
5. **开关**：Settings → General → Composer → Show predictions 是否打开。
6. **时机**：建议在 Codex 回复结束后才出现，回复过程中没有。

都对上还是没有，可能是地区或 beta 资格的问题。官方文档另有一篇「Composer predictions in Codex」讲安装和排障，可以去看。

## 相关阅读

- [Codex 桌面端任务工作流](./08-Codex桌面端任务工作流.md)
- [Codex 设置检查清单](../10-配置模型与权限安全/08-Codex设置检查清单-让任务按预期执行.md)
- [App、CLI、IDE 和 Cloud 怎么选](https://codexguide.io/guides/app-cli-ide-he-cloud-zen-me-xuan)

## 参考

- [Composer Predictions（官方）](https://learn.chatgpt.com/docs/features/composer-predictions)
