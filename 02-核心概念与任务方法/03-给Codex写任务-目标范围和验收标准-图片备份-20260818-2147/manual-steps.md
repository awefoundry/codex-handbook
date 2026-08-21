# 需要作者亲自截图

## 演示项目

使用本机脱敏临时项目：`D:\codexguide_all\tmp\codex-task-card-demo`。

它只有 `README.md`、`package.json`、`src/login.js` 和 `test/login.test.js`，没有远端、账号、密钥或业务数据。打开终端后先运行：

```powershell
Set-Location 'D:\codexguide_all\tmp\codex-task-card-demo'
npm test
```

初始结果应为 1 个通过、1 个失败；失败断言是 `true !== false`，说明错误验证码后按钮状态没有复位。

## 四轮 prompt

### 01～04-四轮 prompt 截图

在 Codex CLI 或 Desktop 中打开上述项目，但先不要发送消息。把下面四版 prompt 依次放在编辑器或临时文本窗口中，展示信息如何逐步增加；截图中只保留项目相对路径和示例代码。

```text
1. 登录坏了，修一下。

2. 修复登录页验证码按钮：用户输入错误验证码后，按钮会一直转圈，无法再次提交。
先定位触发请求和 loading 状态的代码，说明原因和复现方式，暂时不要改文件。

3. 修复登录页验证码按钮：用户输入错误验证码后，按钮会一直转圈，无法再次提交。
请先查看 src/login.js、现有登录测试和 npm test 的失败输出，找出 loading 没有在失败分支复位的原因。
只改登录逻辑及其直接测试；不要改 package.json、测试命令或其他目录。先给出调查结论和最小改动计划，等待我确认后再编辑。

4. 修复登录页验证码按钮：用户输入错误验证码后，按钮会一直转圈，无法再次提交。
请先查看 src/login.js、现有登录测试和 npm test 的失败输出，找出 loading 没有在失败分支复位的原因。
只改登录逻辑及其直接测试；不要改 package.json、测试命令或其他目录。
完成标准：错误验证码请求结束后 loading 恢复为 false；补一条覆盖失败分支的回归测试；运行 npm test 并报告命令、结果和未覆盖风险；先展示 diff，不提交代码。
```

停在发送前。隐藏用户名、绝对路径、终端个人目录和任何真实项目名。当前收到的四张图分别保存为：`01-提示词-第一版.png`、`02-提示词-第二版.png`、`03-提示词-第三版.png`、`04-提示词-第四版.png`。

### 05-Codex首次调查-去提示.png

发送第 2 版 prompt。等待 Codex 显示它读取了 `src/login.js`、`test/login.test.js` 或提出澄清问题时截图。画面必须能看出“先调查、暂不修改”的状态，不要继续到执行阶段。

建议文件名：`05-Codex首次调查-去提示.png`。隐藏绝对路径和账号信息，只保留相对文件名、调查结论和问题。原始未处理图 `05-Codex首次调查.png` 仅作备份。

### 06-Codex调查边界-去提示.png

如果 Codex 报告当前目录不是 Git 仓库，但仍继续读取 `src/login.js` 和测试文件，可将该画面作为边界证据。它说明 Agent 会报告环境限制，但不应因此擅自改变任务范围。

建议文件名：`06-Codex调查边界-去提示.png`。保留 `fatal: not a git repository` 这类临时项目反馈；确认画面没有真实远端地址或个人文件名。原始未处理图 `06-Codex调查边界.png` 仅作备份。

### 07-Codex修改diff与测试通过.png

在 `D:\codexguide_all\tmp\codex-task-card-demo` 发送下面的任务：

```text
目标：修复验证码请求失败后按钮一直 loading、无法再次提交的问题。
上下文：查看 src/login.js 和 test/login.test.js。失败分支保留 invalid captcha 错误，同时把 loading 恢复为 false。
范围：只修改 src/login.js；不要改 API 参数、路由、错误文案、package.json 或其他目录。
执行：先展示最小 diff，再运行 node --test（不要使用 npm.ps1）。
验收：失败用例和成功用例都通过；报告修改文件、测试命令和结果；不要提交代码。
```

截图应同时包含修改后的 diff、`node --test` 命令和通过结果。不要保留 PowerShell `npm.ps1` 策略错误或 `Conversation interrupted`。

建议文件名：`07-Codex修改diff与测试通过.png`。不要截取提交、推送、发布或任何外部系统操作。

### 08-任务说明书与验收清单.png

在编辑器或 Markdown 文件中展示文章里的“可直接复制的任务说明书”，填入这个脱敏案例：目标是失败验证码后可重试；范围是 `src/login.js` 和 `test/login.test.js`；不改 `package.json`；验收是 `node --test` 通过并报告 diff。

建议文件名：`08-任务说明书与验收清单.png`。隐藏本机绝对路径，不要放真实业务名、内部链接、令牌或账号。

## 截图检查

- [ ] 画面显示的是临时项目，不含真实账号、客户资料、密钥、令牌、生产日志或内部远端地址。
- [ ] 01～04 图依次展示四轮 prompt，05 图展示首次调查，06 图展示环境边界反馈。
- [ ] 截图中的文件名、命令和结果与当前临时项目一致。
- [ ] 不把网页文档截图、视频封面或缩略图当作 Codex 操作证据。
- [ ] 截图完成后，将文件复制到本工作区的 `manual/`，再在 `manifest.tsv` 登记来源和用途。
