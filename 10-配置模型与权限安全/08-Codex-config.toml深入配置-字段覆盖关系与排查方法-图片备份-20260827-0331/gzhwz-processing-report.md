# gzhwz 处理报告

## 处理环境

处理环境：Windows 11 24H2；Codex CLI 0.147.0；Python 3.13.5 + Pillow 12.3.0；2026-08-28 核验。完整版本和取值方法见 `environment.md`。

## 正文处理

- 保留文章关于配置层级、字段边界、Profile、临时覆盖、沙箱和回滚的事实与官方链接。
- 将导语改为更直接的排查视角，压缩模板化表达；修正 CLI 0.147.0 不再支持的 `--ask-for-approval` 示例，改为 `--sandbox read-only --skip-git-repo-check`。
- 移除 gzhstart 内部备用素材区，不把采集状态、AI 生成说明或作者操作记录带入发布正文。
- 正文图片各自独立成段，图片之间保留空段；正文现使用 2 张终端案例图，二维码不计入正文图号。

## 图片映射与验收

- `manual/01-config-paths-and-version.png` -> `正文配图/图一.png` -> `发布素材/正文配图/图一.png`：保留 `CODEX_HOME`、CLI 版本和 `config.toml` 状态；已检查用户名、完整用户路径、账号和配置内容，未发现敏感信息。
- `manual/02-status-readonly-probe.png` -> `正文配图/图二.png` -> `发布素材/正文配图/图二.png`：保留 `sandbox=read-only`、`READ=ALLOWED`、`WRITE=DENIED`；已检查临时目录、session ID、provider、网络日志、账号和令牌，输出图已裁除无关信息。

两张正文图均使用 imagegzh 一号样式：保留原始文字与布局，增加约 4 px 白色内边距、透明圆角、`#d9d9d9` 细边框和轻阴影；原始截图仍保留在 `manual/`，未覆盖。

## 链接与埋点

| event_id | stage | position | intent | target_type | target_title | url | utm_status | verification_status | copy_role | post_publish_metrics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `closing-website-01` | `closing` | 结语之后、微信区块之前 | `take-action` | 网站 CTA | CodexGuide 配置、模型与权限安全专题 | `https://codexguide.io/guides?utm_source=wechat&utm_medium=article&utm_campaign=codex-config-deep-dive&utm_content=closing-website-01` | 已添加 `utm_content=closing-website-01` | HTTP HEAD 200（2026-08-28） | 行动 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-wechat-01` | `closing` | 网站 CTA 之后、全文最后 | `ask-or-connect` | 微信 CTA | 微信交流 | 不适用 | 不适用 | 默认二维码源与发布副本 SHA-256 一致，正文引用存在 | 关系承接 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |

文首、正文中段和决策节点没有自然的历史文章或站内入口，未强行添加。历史文章目录没有与本篇高度匹配且已核验的标题，未写入标题式链接。

## 二维码验收

- 源文件：`D:\CodexHome\skills\gzhwz\assets\wechat-qr.png`
- 发布副本：`../08-Codex-config.toml深入配置-字段覆盖关系与排查方法-发布素材/wechat-qr.png`
- SHA-256：`E5A625D07A9C5C41F9860060045ECACFFD247A6FCA6D6CC20596383BD9BBE001`（源与副本一致）。
- 未调用 imagegzh，未裁切、加框、压缩或改写二维码。

## 验证与待确认

- `validate_gzh_workspace.py`：通过。
- `validate_manifest.py`：通过（合并 `online/` 与 `manual/` 的临时校验目录）。
- 正文图片引用、发布素材目录和备份映射：通过。
- 公众号标题：待作者确认；标题确认前不生成封面。
