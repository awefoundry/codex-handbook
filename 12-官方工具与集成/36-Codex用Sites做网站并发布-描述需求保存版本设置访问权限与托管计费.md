---
id: codex-sites-build-publish-website
title: "Codex 用 Sites 做网站并发布：一句话描述需求，先存版本再上线，设置谁能访问，托管怎么计费"
seo_title: "Codex Sites：描述需求、保存版本、访问权限与托管计费"
description: "在 ChatGPT 网页或桌面端里，用一段描述做出网站、网页应用或小游戏，再用 Sites 发布。本文按官方文档说明怎么触发、为什么先保存版本、新站点默认谁能访问，以及托管额度和计划中的计费。"
lede: "每个部署网址都是正式环境。想先看效果，就让它保存版本、先不要部署。"
url: /guides/codex-sites-build-publish-website
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [Chat, ChatGPT Work, App, CLI, IDE]
difficulty: 基础
order: 36
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-26
date_modified: 2026-11-26
verified_on: 2026-11-26
official_ref: https://learn.chatgpt.com/docs/sites
keywords: [Codex Sites, ChatGPT Sites, Codex 做网站, Codex 发布网站, Sites 托管计费]
related: [codex-webmcp-site-tools, codex-browser-e2e-acceptance, codex-desktop-task-workflow]
howto: true
faq:
  - q: "Codex CLI 里有没有 Sites 管理页？"
    a: "没有。官方写明 CLI 和 IDE 扩展没有独立的 Sites 管理视图。创建、保存、部署和分享要在 ChatGPT 网页或桌面应用里做。CLI 和 IDE 可以先改本地项目，再到网页或桌面端发布。"
  - q: "新站点默认谁能打开？"
    a: "官方写明，新站点只限所有者和工作区管理员，直到你改访问范围。访客能打开站点，并不等于能编辑。"
  - q: "现在就要为托管付钱吗？"
    a: "Usage and cost 页写的是计划：托管到 2027-01-31 免费，计划 2027-02-01 起对 Plus、Pro、Business 超出月度额度的部分收费。帮助中心 FAQ 同时写，Plus 和 Pro 的托管目前包含在套餐里，Enterprise 的运行和托管费用目前免除。构建和修改计入 Codex 用量。以 2026-11-26 打开的页面为准。"
  - q: "这和 WebMCP 的 Site tools 是一回事吗？"
    a: "不是。Sites 是把你描述的网站发布出去。WebMCP 是网站把操作交给内置浏览器里的 Codex。两篇不要混用命令。"
---

# Codex 用 Sites 做网站并发布：一句话描述需求，先存版本再上线，设置谁能访问，托管怎么计费

> 本文在线版：[codexguide.io/guides/codex-sites-build-publish-website](https://codexguide.io/guides/codex-sites-build-publish-website)

> 核对依据：2026-11-26 打开的官方文档 [Sites](https://learn.chatgpt.com/docs/sites)、[Create a site](https://learn.chatgpt.com/docs/sites/creating-a-site)、[Publish and share](https://learn.chatgpt.com/docs/sites/publishing-and-sharing)、[Data and connections](https://learn.chatgpt.com/docs/sites/data-and-connections)、[Manage a site](https://learn.chatgpt.com/docs/sites/managing-a-site)、[Usage and cost](https://learn.chatgpt.com/docs/sites/usage-and-cost)，以及帮助中心 [Creating and using ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites)（页面自标 Updated: 18 days ago）。没有登录 ChatGPT，没有创建站点，没有配图。按钮名只写这两处文档里出现过的。

Sites 是在 ChatGPT 或 Codex 里描述一个网站、网页应用或游戏，再把它发布出去。你可以先说一个想法，也可以改编同事已有的站点，或带上一个已经能构建的项目。发布出去的每个部署网址都是正式环境。想先看效果，要明确说保存版本、先不要部署。

它和 [WebMCP 的 Site tools](../09-MCP与外部工具/05-Codex-Site-tools-WebMCP网站工具入门.md) 不是一件事。那边讲的是网站怎样把操作交给内置浏览器里的 Codex。本文只讲 Sites 怎么做、怎么发、谁能看、托管怎么算。

## 先说结论

适合用 Sites 的，是官方举例的那一类网页体验：按主题找资料的资源站、带筛选的看板、任务表、申请表、按公式估算的计算器、分步骤的引导流程。文档把这些写成可以怎么做的例子，不是已经替你做好的模板。

不适合、文档写明不要拿来做的，包括：处理受保护健康信息（Protected Health Information）；面向 13 岁以下或当地数字同意年龄以下的儿童；散发恶意软件；钓鱼；冒充个人或组织；以及其他违反 OpenAI 政策的用途。售卖商品或服务、收款，只能走第三方支付处理方，卡数据必须只由该处理方采集和处理，不能由你的站点或 OpenAI 采集。你要自己负责接入、履约、退款、客服和适用的税。条款见 [Sites Terms](https://openai.com/policies/chatgpt-sites-terms/)（页面标注 Updated: November 6, 2026）。

运行时支持 HTTP、HTTPS 和 WebSockets。不支持原始的入站和出站 TCP。每个站点的 D1 数据库存储上限是 10 GB。R2 对象存储没有固定的存储上限。

## 哪些入口能用

帮助中心写的创建入口是：网页上选 **Work**；桌面应用里选 **ChatGPT** 再选 **Work**，或选 **Codex**。然后在对话里描述网站。提示里写上 website，或提及 `@Sites`，用来进入 Sites 流程。

可用范围，帮助中心写的是 ChatGPT Plus、Pro，以及 Business、Enterprise 工作区。Free 和 Go 不能用。ChatGPT Classic 应用里也没有 Sites。Enterprise 要管理员先为工作区或角色启用；看不到时，问管理员。公开到互联网在 Enterprise 里默认关闭，要管理员打开之后，符合条件的成员才能公开发布。管理入口见 [Managing ChatGPT Sites for your workspace](https://help.openai.com/en/articles/20001338-managing-chatgpt-sites-for-your-workspace) 和 [Sites administration](https://learn.chatgpt.com/docs/enterprise/sites)。

找到已有站点：桌面应用里打开 **sites**；网页上选 **More** > **sites**，或直接打开 [chatgpt.com/sites](https://chatgpt.com/sites)。

Codex CLI 和 IDE 扩展没有单独的管理页。官方写明，创建、保存、部署和管理要在网页或桌面应用里做。你仍然可以用 CLI 或 IDE 先改、先测本地项目，再去网页或桌面端发布。桌面端任务怎么排，见 [桌面端任务工作流](./08-Codex桌面端任务工作流.md)。

## 用 website 或 @Sites 描述需求

先说给谁用、让人做什么，再附上它要用的文件、数据和定义。文档要求：缺信息就让它标出来，不要自己补。空状态和错误状态也要写清，例如搜索没有结果、表单不完整、连接的应用不可用时显示什么，以及怎样重试。

下面是 Create a site 页上的例子，不是本文发送过的提示：

```text
Build a project request dashboard website for my operations team. Use my connected Google Drive plugin to find our request intake guide and suggest fields and status labels. Ask me to confirm them before building. Let team members submit requests, see who owns each one, update the status, and filter the list. Require people to sign in with their workspace account, and keep the request data saved between visits.
```

要用插件时，在提示里用 `@` 点名，并写它该贡献什么。不确定有哪些插件，就问 ChatGPT。想先审再上线，文档里的资源站例子以这句收尾：`Save a version without deploying it so I can review it.`

已有本地项目时，同一页的例子是：

```text
Deploy this project with sites. Check whether it is compatible, make any required changes, and give me the deployment URL.
```

需要记住分数或上传的头像时，把「访问之间要保留」写进需求。临时的界面状态，例如主题或关掉的横幅，文档说不要为它要持久存储。

另一种起点是 **Remix**。同事的站点已经接近你要的，就打开那个站点，在右下角工具栏选 **Remix**，或从工具栏菜单里找。继续到 ChatGPT；如果工具栏里打开了输入框，选 **Open ChatGPT**。输入框里会带上 **Remix** 和来源站点的名字。写明留给谁、保留什么、换掉什么。要一起维护同一个站点，用下面的协作，而不是 Remix。

## 先保存版本，再决定部署

Sites 的发布分成两步，Manage a site 页写得很明确：

1. **Save a version。** ChatGPT 做出一个可部署的版本。本地源项目会把这个版本和构建所用的 Git 提交连起来。这一步用来得到一份可以审的候选。
2. **Deploy a version。** 把已保存的版本发布出去，成功后给出正式网址。只有当你打算让选定的受众访问时才做这一步。

Create a site 页的原话是：每个 Sites 部署网址都是正式部署。想在上线前看构建，就让 ChatGPT 保存版本、不要部署。

帮助中心补充了两件开发文档正文里分开写的事：第一次部署时，ChatGPT 会给一个默认网址，里面可以带站点名，以及你的用户名或工作区名。个人账号默认用随机标识，而不是用户名。如果你把个人资料设为公开，或改了用户名，网址里可能会用上用户名。发布给别人，是让当前版本按你选的受众出现在那个网址上。对已有站点再次部署，会更新线上版本。

同一篇帮助中心还写：发布有可能在新版本上线之前就改了站点的数据库。发布失败时，有些数据库改动可能已经写上，重试前要先看数据库。恢复较早的版本，恢复的是代码，不是数据库或上传的文件。发布前要看数据库迁移。本地项目的源改动和迁移，Create a site 页让你在 Codex 的 [review pane](https://learn.chatgpt.com/docs/code-review) 里看。

改的时候一次只改一处，并写明要保留什么。例如只移动筛选器，不改已保存的记录、访问规则和已有动作。改完就试受影响的那一个交互。预览里的编辑，Create a site 页写的是：选 **Edit**，在 **Describe website edits** 下写改动，需要更多上下文时用 **Screenshot** 或 **Add files and more**。

帮助中心另有一条从已发布站点发起编辑的路径，仅在编辑控件可用、并且你是所有者或编辑者时：打开已发布站点，选 **Edit site**，在 **Describe your edits** 里写改动，再选 **Send edits**，回到 ChatGPT 继续。它写明，从站点发出说明只是开始编辑流程，不会立刻改已发布的站点。两页的按钮名不一样，以你当前界面上实际出现的为准，不要把两套名字拼成一个本文没见过的菜单。

## 保存记录和登录

保存站点版本，保留的是内容、设计和行为。访客提交的请求、状态更新、上传的文件和个人进度，要另有存储。你要告诉 ChatGPT 或 Codex 存什么、谁可以读、谁可以改。

Data and connections 页的对应关系是：

| 站点需要 | 向 Sites 要什么 |
| --- | --- |
| 内容站或落地页 | 除非体验需要，不要持久的应用状态 |
| 要留下的记录、进度或游戏分数 | D1，存放结构化数据的关系库 |
| 图片、文档、音频、视频或其他上传 | R2，文件的对象存储 |
| 上传文件还要能搜元数据 | 元数据用 D1，文件内容用 R2 |
| 内部站点要当前工作区用户的身份 | 工作区认证的用户身份 |
| 公开登录或外部身份 | 启用认证的站点 |

共享或个人记录要在服务端执行访问规则。藏起一个按钮，保护不了底下的记录。改完要重新加载，确认还在；用不同账号确认每个人只能看到该看的。提供的文件要说明是用一份副本，还是从源头刷新，并核对最后更新时间。

公开站点可以仍然对所有人开放，同时加上可选的 Sign in with ChatGPT，用来做进度、个性化，或属于某个人的记录。工作区限制的站点，本身就用 ChatGPT 身份执行分享设置。文档里的提示要求：未登录的人仍能访问；未登录时显示 Sign in with ChatGPT；登录后有全名就用全名打招呼，否则用邮箱；提供 Sign out；授权判断放在服务端代码里。

平台提供的路径是：

```html
<a href="/signin-with-chatgpt">Sign in with ChatGPT</a>
<a href="/signout-with-chatgpt">Sign out</a>
```

登录之后，身份通过请求头交给服务端：`oai-authenticated-user-email` 是已认证邮箱；`oai-authenticated-user-full-name` 可能有非空的资料名，要当成可选，没有就退回邮箱。不要依赖把名字拆开的请求头。

站点所有者可以让脚本在不打开浏览器的情况下，通过 Sign in with ChatGPT bypass token 经过登录门。文档写：在 ChatGPT Work 或 Codex 里让它为这个站点生成令牌；代理使用 `generate_siwc_bypass_token`，返回 `siwc_bypass_bearer_token`。再生成一次会换掉这个站点上已有的令牌。请求头是：

```text
OAI-Sites-Authorization: Bearer <siwc_bypass_bearer_token>
```

Sites 会在把请求转到你的站点之前吃掉这个头。站点自己的 API 凭证仍放在普通的 `Authorization` 头里，Sites 会保留它。绕过登录的请求没有访客身份，也拿不到上面的用户头，也不能用访客连上的应用。令牌是密钥：拿到它的人可以通过该站点的登录门。不要放进浏览器代码、URL 或源代码仓库。泄露后要重新生成。新令牌立刻有效，旧令牌可能在缓存配置过期前继续有效，最多五分钟。

用插件把每个访客自己的已连接应用读进站点，文档要求：工作区启用了插件，站点对该工作区保持私有，访客属于该工作区并使用自己已有的应用权限。分享站点不会把你的已连接账号交给别人。访客可以不授权继续看，但需要授权的功能不会工作。默认用 **Load more** 在连接器返回游标时再取一页。

## 发布前检查什么

Publish and share 页把发布前收成三步。

**先自己用一遍。** 看内容、生成的文字和图片、链接、上传的文件、表单和交互。按预期访客的身份试访问和登录。本地项目还要看源改动和数据库迁移。

**再看数据和权限。** 确认没有机密、敏感信息、密钥，以及你无权分享的第三方内容。收集个人信息或其他访客内容的功能，要决定该不该收集、分享或公开。用了 Sign in with ChatGPT，就要说明站点拿到访客的什么信息、用来做什么。处理个人数据要遵守适用的隐私和数据保护法律，帮助中心链到 [Complying with data protection laws for ChatGPT Sites](https://help.openai.com/en/articles/20001340-complying-with-data-protection-laws-for-chatgpt-sites)。

**最后选最小的受众。** 打开分享后的站点，确认预期的人打得开。上线前的页面检查，也可以对照 [上线前的端到端验收](../06-测试调试与质量保障/01-Codex做上线前端到端验收.md)，但那篇的浏览器断言不能代替这里的受众和密钥检查。

## 谁能访问

新站点只限所有者和工作区管理员，直到你改访问。文档列出的选项，视账号和工作区设置而定：

- **Owner and workspace admins**
- **Selected active users or groups**（在支持的地方）
- **Invited external viewers**（外部邀请可用时）
- **Anyone in the workspace**（在支持的地方）
- **Anyone on the internet**（只有公开已启用时）

访客访问只表示能打开，不表示能编辑。站点的受众设置，和站点内部做的登录功能，是两套控制。公开站点不需要 ChatGPT 工作区权限就能打开。

邀请工作区外的人，Publish and share 页的步骤是：打开你拥有的站点，选 **Share**；要保持私有，把 **Who has access** 设为 **Only those invited**；在 **Search for people or groups** 下输入邮箱，个人站点则是 **Enter an email address**；核对受众和对方的 **Viewer**，再选 **Invite**；确认对方出现在已保存的访问列表里。被邀请的人要用收到权限的那个账号登录。他们不会变成工作区成员或编辑者。外部邀请正在向 Plus、Pro、Business、Enterprise 上的 Sites 用户推出；看不到时，检查所选账号、站点所有权和推出范围。Enterprise 和 Business 要管理员看工作区里的 Sites 设置。

协作编辑需要工作区。所有者可以邀请同一工作区里的活跃成员当编辑。步骤是：选 **Share**；在 **Add people or groups** 里选中成员，对方先被加为访客；把旁边的 **Can view** 改成 **Can edit**，访问会自动保存。站点会出现在对方 sites 视图的 **Shared with you** 里。编辑者可以打开、修改、保存版本；所有者完成第一次发布之后，编辑者才能发布后续更新。编辑者不能改受众、不能邀请或移除别人、不能管设置或分析、不能转移所有权，也不能做第一次发布。把访客升成编辑，不会改变站点的受众设置。

帮助中心的分享步骤写的是选好受众后 **Save**，上线后用 **Visit** 打开或 **Copy link** 复制网址。和上面的 **Invite** 不是同一句。按你界面上出现的按钮做。

## 更新、改网址、自定义域名和下线

更新：在 ChatGPT 里打开站点，描述改动，看结果，保存版本，再部署。用预期受众里的一个账号打开正式网址试一遍。

改名称和网址在站点设置里，所有者可以管。帮助中心写：改网址后，只要工作区地址不变，旧网址会跳到新网址。这不包括工作区地址本身变了，也不包括自定义域名。个人站点地址里的账号名，会随 ChatGPT 用户名一起变：打开 Settings，选 **Account**，再选 **Username**。用户名会出现在站点地址里，分享前先看一遍地址。检查私有站点的完整地址时，帮助中心写：在网页的 Sites 里打开更多选项（**•••**），选 **Open site**。打开私有站点看地址，不会把它变成公开的。

自定义域名要你已经拥有，并能改 DNS。Sites 不替你注册域名。Manage a site 页写：上线时，Enterprise 工作区不能用自定义域名。帮助中心写的是「在自定义域名可用的地方」，所有者可以把域名接到站点，包括工作区站点，并给了域名一直停在 pending、返回 404 时的核对办法。两页没有写成同一句。本文不判断你的 Enterprise 工作区现在有没有这个控件，以设置页里是否出现 **Add domain** 为准。

出现该控件时，两页的步骤一致：

1. 打开站点设置，选 **Add domain**。
2. 输入要使用的顶级域名或子域名。
3. 复制 Sites 给出的 DNS 记录和值，到域名服务商处添加。
4. 等几分钟，回到站点设置刷新域名状态。

如果开了浏览或 Computer Use，也可以让 ChatGPT 在你登录域名服务商之后帮你点。域名注册费另计，不包含在下面的托管积分里。

环境变量和密钥：打开 **sites**，进入站点设置添加、更新或删除。网页上是找到站点后选 **More actions** > **Settings**。密钥不要写进提示、附件和站点内容。本地项目不要把这些值放进 `.openai/hosting.json`。本地 `.env` 和 `.env.example` 只对齐本地开发需要的键名，不要提交密钥值。

分析：Sites 自动记录访问，不用另装分析 SDK。视图里有独立访客数和页面浏览量，以及随时间的两条曲线，可以改日期范围和粒度。入口是 **More actions** > **Analytics**。文档写明，Enterprise 工作区拥有的站点目前没有这项分析。

不下线但收回访问：打开分享设置，把访问收回到自己或选定的人，并确认原来的受众打不开。

永久删除：

1. 打开 **sites**，找到站点。
2. 选 **Delete site**，按提示做。
3. 输入站点 slug，再选 **Permanently delete**。

删除不能恢复。帮助中心还写了站点的 Automations：在可用时，所有者可以为已发布站点建云端日程，选 **Create schedule**。本文没有工作区，没有看到这个入口，不把日程步骤写成已经试过。

本地源项目和托管的关联，以及可选的存储绑定名，写在 `.openai/hosting.json`。新建的本地 starter 可以先没有 `project_id`，Sites 配好托管项目后再写上。文档里的例子是用了关系库、没有文件存储：

```json
{
  "project_id": "<project-id>",
  "d1": "DB",
  "r2": null
}
```

站点会留在 ChatGPT 的 sites 列表里，创建它的那次 ChatGPT Work 对话结束也还在。网页上开始一个站点，不需要本地项目或这份清单。站点也不是 ChatGPT Project。

## 托管计费

这一节按 2026-11-26 打开的 [Usage and cost](https://learn.chatgpt.com/docs/sites/usage-and-cost) 转述。官方用了 plan（计划）和 approximate（约），下面保留这两个词，不把计划写成已经开始收费。

官方原意是：计划从 **2027-01-01** 起在应用里显示 Sites 托管用量。托管在 **2027-01-31** 之前免费。计划从 **2027-02-01** 起，对 Plus、Pro 和 Business 超出月度额度的托管用量收费。Enterprise 的账单按组织协议。

站点数量没有上限。构建和修改计入套餐的 [Codex 用量](https://learn.chatgpt.com/docs/pricing)。托管覆盖站点收到的流量和占用的存储。

Plus、Pro、Business 上，你的全部站点共用一份月度托管额度：

| 套餐 | 月度托管额度 |
| --- | --- |
| Plus | 125 积分 |
| Pro | 375 积分 |
| Business | 每个席位 125 积分 |
| Enterprise（按积分） | 从组织合同里的积分池扣 |

Enterprise 如果是美元承诺，Codex token 和 Sites 托管费率分开，从同一笔承诺里扣。文档的例子是：10 美元 Codex 用量加 2 美元托管，用掉承诺里的 12 美元。具体费率问客户团队。

估算用的是约数：

| 使用 | 计费单位 | 约合积分 |
| --- | --- | --- |
| 没有存储的站点 | 每月 1 个站点 | 0 |
| 有存储的站点，包括空数据库 | 每月 1 个站点 | 25 |
| 流量 | 10 万次请求 | 15 |
| 数据库存储（例如表单回复） | 存满一个月的 1 GiB | 150 |
| 文件存储（图片、PDF 等） | 存满一个月的 1 GiB | 3.75 |
| 自定义域名（域名注册另计） | 每月 1 个域名 | 25 |
| Site–tunnel 连到私有系统（仅 Enterprise） | 一条连接 30 天 | 125 |

一次请求是加载一个页面、一张图片或其他资源。一次页面访问通常产生约 30 到 50 次请求，视站点而定。带空数据库的站点，在产生流量之前大约每月 25 积分。如果记录存满一个月的 1 GiB，基础费和数据库存储合在一起大约 175 积分。1 GiB 大约是 1.07 GB。

Enterprise 的 Site–tunnel：大约 125 积分 / 30 天，按天分摊。每一对 Site 和 tunnel 在每个 UTC 日只计一次，即使站点未发布或没有流量。当天没有挂上任何 Site 的 tunnel 计为 0。三个 Site 共用一条 tunnel 计三次。一个 Site 挂两条 tunnel 计两次，包括从一条换到另一条。同一 UTC 日断开再连上同一对，仍计一次。

页面上的估算器假设存满一个月。选 **This Site has a database** 会把基础费算进去，即使保存的记录是 0。自定义域名和 Enterprise 的 tunnel 要按上表另加。本文没有在估算器里代填数字。

帮助中心 FAQ 和这一页要一起看，不要只记一句。FAQ 写：Plus 和 Pro 的 Sites 托管目前包含在套餐里，创建数量没有固定上限，构建或编辑仍计入 Codex 用量；Enterprise 的运行和托管费用目前免除，用量和存储上限仍然有效。这和「计划 2027-02-01 起对超额部分收费」不冲突：一个说的是今天，一个说的是计划中的起算日。Enterprise 将来按积分还是按美元，FAQ 写由工作区协议决定。

## 常见问题

**保存版本和部署有什么差别？** 保存得到一份可审的候选。部署才把选定版本放到正式网址上，给当前受众看。

**提示里写了不要改文件，站点就安全了吗？** 不够。受众、密钥、数据库和第三方内容要按上面的发布前检查单独看。隐藏按钮不等于服务端拒绝访问。

**CLI 里能不能直接看到分析或改域名？** 不能。这些在网页或桌面应用的 sites 里。

## 参考资料

- [Sites](https://learn.chatgpt.com/docs/sites)
- [Create a site](https://learn.chatgpt.com/docs/sites/creating-a-site)
- [Publish and share](https://learn.chatgpt.com/docs/sites/publishing-and-sharing)
- [Data and connections](https://learn.chatgpt.com/docs/sites/data-and-connections)
- [Manage a site](https://learn.chatgpt.com/docs/sites/managing-a-site)
- [Usage and cost](https://learn.chatgpt.com/docs/sites/usage-and-cost)（2026-11-26 核对）
- [Creating and using ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites)
- [ChatGPT Sites Terms](https://openai.com/policies/chatgpt-sites-terms/)
