---
id: codex-web-search-settings
title: Codex 网页搜索设置：cached、indexed、live、disabled 怎么选，--search 单次联网，allowed_domains 限定站点
seo_title: Codex 网页搜索：cached、indexed、live 与 allowed_domains
description: Codex 默认用缓存索引做网页搜索，也可以改成实时联网、只走索引或者关掉。本文讲清四种模式的区别、--search 和 config.toml 怎么设、怎样只搜指定网站、为什么它和沙箱联网是两套规则，以及怎么防提示注入。
lede: 网页搜索是托管工具。默认 cached。--search 只让这一次交互会话走 live，codex exec 不接受这个旗标。
url: /guides/codex-web-search-settings
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 进阶
order: 18
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-05
date_modified: 2026-11-05
verified_on: 2026-11-05
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/web-search
keywords: [Codex 网页搜索, Codex web search, web_search config.toml, codex --search, Codex 联网搜索, allowed_domains]
related: [config-toml-guide, codex-sandbox-host-trust, codex-custom-model-provider, codex-amazon-bedrock, codex-config-toml-cheatsheet, codex-memories]
faq:
  - q: 默认会不会每次都去打开网页？
    a: 本地 Codex 默认是 cached。配置参考写 cached 使用 OpenAI 维护的索引，不访问外部网页。完全放开沙箱（例如 --yolo）时，默认改成 live。
  - q: codex exec --search 能用吗？
    a: 不能。0.166.0 里 codex exec --search 会报 unexpected argument '--search'。--search 写在 codex、codex resume、codex fork 的帮助里，官方示例也是 codex --search。
  - q: 把沙箱的网络关掉，网页搜索是不是也关了？
    a: 不是。网页搜索不走沙箱的网络代理和域名白名单。命令网络关掉之后，搜索工具仍可以按 web_search 的设置使用。
  - q: allowed_domains 能限制 MCP 和终端命令吗？
    a: 不能。它只过滤搜索。命令、App、连接器和 MCP 的流量不在这个列表里。
  - q: 自定义模型提供商写上 supports_standalone_web_search = true 就会搜索吗？
    a: 官方写不会。这个能力默认是 false，独立网页搜索仍在开发中。提供商、所选模型和运行时都要支持，工作区的搜索限制也仍然生效。
---

# Codex 网页搜索设置：cached、indexed、live、disabled 怎么选，--search 单次联网，allowed_domains 限定站点

> 本文在线版：[codexguide.io/guides/codex-web-search-settings](https://codexguide.io/guides/codex-web-search-settings)

> 核对依据：ChatGPT Learn [Web search](https://learn.chatgpt.com/docs/web-search)、[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 的 `web_search` 与 `tools.web_search`、[Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) 的 Web search modes、[Permissions](https://learn.chatgpt.com/docs/permissions)（2026-11-05）。配置能否被 0.166.0 接受，在独立 `CODEX_HOME` 里用 `codex --strict-config` 看过 `indexed`、`live` 加 `allowed_domains`，以及非法值 `nope`。没有登录，所以没有一次真实的搜索，也没有 `web_search` 事件样本。

Codex 可以在做事时查网页。这和沙箱里的 `curl` 不是同一条网络。默认走缓存索引；要查刚发布的内容，再改成 live，或给这一次运行加上 `--search`。

配置文件放在哪、`-c` 和 profile 谁覆盖谁，见 [config.toml 配置指南](./04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。字段一行速查见 [config.toml 速查](../16-图解与速查/02-Codex-config.toml常用字段与环境变量速查.md)。

## Codex 的网页搜索是什么

官方把它写成第一方、托管的搜索工具。ChatGPT 桌面端、网页、CLI 和 IDE 扩展都会用到，入口不一样：

- 桌面端和网页里，直接要当前信息。工作区设置可以限制搜索是否可用。
- CLI 里，`codex --search` 为这一次运行拉取 live 结果。
- IDE 扩展沿用所连接 Codex 主机的搜索模式。

搜索会以 `web_search` 条目出现在交互记录里，也会出现在 `codex exec --json` 的输出里。本文没有登录，没有贴出一条真实的 JSON 事件。

Deep research 是另一个插件或菜单入口，用来做多来源的调查报告。它不是 `web_search` 的第五种模式，这里不展开。

## 四种模式

配置参考里的取值是 `disabled`、`cached`、`indexed`、`live`。默认 `"cached"`。

| 模式 | 官方怎么描述 | 什么时候用 |
|---|---|---|
| `cached` | 使用 OpenAI 维护的索引，不访问外部网页。Web search 页写：这能降低、但不能消除提示注入风险 | 日常默认。不需要「刚才才发布」的页面时 |
| `indexed` | 只有搜索索引放行时，才允许外部网页访问 | 希望比缓存更接近来源，又不想做无限制的实时抓取 |
| `live` | 不做限制的实时检索。任务依赖最新信息时用它 | 查发布说明、今日变更、索引里还没有的页面 |
| `disabled` | 关掉这个工具 | 不希望模型看到网页结果 |

完全放开时默认会变。配置参考的原句是：若使用 `--yolo` 或其他 full access 沙箱设置，默认变成 `"live"`。Web search 页写：When Codex runs with full access, web search defaults to live results。想在完全放开时仍用缓存，要在配置里显式写 `web_search = "cached"`，并且管理员没有用下面的要求把 live 禁掉。

0.166.0 接受这四个字符串。把 `web_search = "nope"` 写进用户配置后，`codex exec` 在读配置时失败，原文是：

```text
Error loading config.toml: unknown variant `nope`, expected one of `disabled`, `cached`, `indexed`, `live`
in `web_search`
```

`web_search = "indexed"`，以及 `web_search = "live"` 再加上下一节的 `allowed_domains`，在 `--strict-config` 下都能把配置加载过去。当时没有登录，doctor 的失败项是 auth，不是这两个字段。

## 单次联网：codex --search

官方示例：

```bash
codex --search "Summarize the latest release notes for this dependency"
```

0.166.0 里，`codex --help`、`codex resume --help`、`codex fork --help` 对这个旗标的说明相同：Enable live web search. When enabled, the native Responses `web_search` tool is available to the model (no per-call approval)。也就是这一次运行可以实时搜索，开启后不再对每一次搜索单独审批。

`codex exec --help` 没有 `--search`。直接写会失败：

```text
error: unexpected argument '--search' found
```

退出码是 2。非交互任务要 live，把 `web_search = "live"` 写进配置。`-c` 可以临时覆盖配置，值按 TOML 解析：

```bash
codex exec -c web_search='"live"' "Summarize the latest release notes for this dependency"
```

0.166.0 能带着这个参数启动，并打印会话摘要。摘要里没有 `web_search` 一行，`--ephemeral` 也没有留下可以核对生效值的会话文件。未登录时，请求在连上 Responses 接口后返回 401，没有搜索结果。因此本文只确认命令被接受、配置阶段没有报未知取值，不把摘要里没出现的模式写成已经生效。

## 写进 config.toml

用户配置里：

```toml
web_search = "cached"
```

要改成实时或关闭，把值换成 `"live"` 或 `"disabled"`。profile 是叠在用户配置上的另一份文件，写法见配置指南。0.166.0 的 `-p` 会加载 `$CODEX_HOME/<名称>.config.toml`。本文没有另存一份 profile 再跑，所以 profile 是否覆盖 `web_search` 以配置层级为准，不另报一次实测。

旧的功能开关还在，配置参考标成弃用：

- `features.web_search`：改用顶层 `web_search`。
- `features.web_search_cached`：在没设置 `web_search` 时，`true` 映射为 `cached`。
- `features.web_search_request`：在没设置 `web_search` 时，`true` 映射为 `live`。

0.166.0 的 `codex features list` 里，`web_search_cached` 和 `web_search_request` 的阶段是 `deprecated`，`standalone_web_search` 是 `under development`，状态为 false。新配置写顶层的 `web_search`，不要再靠这两个旧开关。

## 只搜指定网站

`tools.web_search` 可以是布尔值，也可以是一张表。表里能写的，配置参考列了三样：`context_size`（`low`、`medium`、`high`）、`allowed_domains`（字符串数组）、`location`（`country`、`region`、`city`、`timezone`）。

限定站点：

```toml
web_search = "live"

[tools.web_search]
allowed_domains = ["example.com"]
context_size = "medium"
```

配置参考没有写通配符怎么匹配。本文只使用文档里的类型（字符串数组），不补 `*.example.com` 这种写法。上面的 `example.com` 能通过 0.166.0 的 `--strict-config` 加载；没有登录，所以没有验证搜索结果是不是只来自这个域名。

这个列表只过滤搜索结果。它不管沙箱里的命令、App、连接器和 MCP。

## 和沙箱联网不是一回事

Web search 页和 Permissions 页写的是同一件事：网页搜索是托管工具，不使用权限配置里的网络代理，也不使用沙箱命令的域名白名单。命令网络被关掉时，搜索仍可以按自己的模式使用。

因此：

- `sandbox_workspace_write.network_access = false` 限制的是沙箱里的命令，不是 `web_search`。
- 管理员的 `network_proxy.allowed_domains` 只管沙箱命令。配置参考写这些规则不适用于网页搜索、App 和 MCP。
- 想关掉搜索，写 `web_search = "disabled"`，或由管理员用下一节的要求限制模式。

沙箱本身管什么，见 [沙箱与主机权限风险](./05-Codex沙箱与主机权限风险.md)。

## 团队管控：allowed_web_search_modes

有托管配置的工作区，管理员在 Global → Requirements → Policy guardrails → Web search modes 里限制可选模式。文档里的界面步骤是：选 Cached，允许缓存搜索并且不允许 live；或选 Disabled，关掉网页搜索。对应的 TOML：

```toml
allowed_web_search_modes = ["cached"] # "disabled" 仍然隐式允许
```

`allowed_web_search_modes = []` 等于只允许 `"disabled"`。`["cached"]` 会在 `danger-full-access` 会话里也阻止 live。`disabled` 始终允许。要求留空，表示这条策略本身不设限；其他仍然适用的策略照旧。

这些限制和命令的网络规则分开配。本文没有企业工作区，没有在管理后台点过这个控件。

## 自定义模型提供商

自定义提供商要同时满足三件事，搜索才会走它自己的兼容端点。Web search 页的示例：

```toml
model_provider = "custom"
web_search = "live"

[model_providers.custom]
name = "Custom Responses provider"
base_url = "https://example.com/v1"
env_key = "CUSTOM_RESPONSES_API_KEY"
supports_standalone_web_search = true
```

`supports_standalone_web_search` 默认是 `false`。官方写明独立网页搜索仍在开发中，默认关闭。只把这个字段设为 `true` 不会打开功能：提供商、所选模型和运行时都要支持，工作区限制也仍然生效。提供商表本身怎么写，见 [自定义模型提供商](./11-Codex自定义模型提供商-model_providers与openai_base_url.md)。

Amazon Bedrock 有自己的搜索默认值，Runtime 与 Mantle 不一样。那篇文档要求的 `web_search` 取值，见 [接入 Amazon Bedrock](../12-官方工具与集成/16-Codex接入Amazon-Bedrock-登录向导与配置.md)，不要用本文的通用默认值盖过 Bedrock 那一页。

## 在哪看 Codex 搜了什么

官方写两处：

- 交互会话的记录里，搜索和其他工具调用记在一起，类型是 `web_search`。
- `codex exec --json` 的事件流里同样有 `web_search` 条目。

没有登录就看不到这些条目。判断某次回答是不是用了网页，先看记录里有没有这个条目，再核对它给出的来源。不要只凭回答里出现了 URL 就认为搜索打开过。

用了网页搜索的线程，还可能影响 Memories。`memories.disable_on_external_context = true` 时，用了 MCP、网页搜索或工具搜索的线程不参与记忆生成。默认是 `false`。见 [Memories](../11-自动化与高级工作流/12-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md)。

## 防提示注入

Web search 页的第一句是：Treat all web results as untrusted input。cached 用索引代替任意页面的实时抓取，能降低提示注入风险，官方同时写明不能消除。

能做的事都在现有开关里：

- 不需要最新页面时保持 `cached`，或直接 `disabled`。
- 用 `allowed_domains` 把搜索收在你指定的站点。文档没有说这样就能挡住注入。
- 工作区用 `allowed_web_search_modes` 禁止 live，包括完全放开的会话。
- 把搜索结果当成待核对的材料。项目规则和你刚写下的要求，不因为某条网页这么写就被替换。

本文没有一套额外的过滤程序，也没有用恶意页面做过实验。

## 参考资料

- [Web search](https://learn.chatgpt.com/docs/web-search)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
- [Permissions](https://learn.chatgpt.com/docs/permissions)
- [Command line options](https://learn.chatgpt.com/docs/developer-commands)
