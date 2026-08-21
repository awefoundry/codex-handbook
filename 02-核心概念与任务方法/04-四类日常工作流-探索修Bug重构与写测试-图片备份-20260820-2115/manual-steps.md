# 需要作者亲自截图

本文使用本地演示项目 `D:\codexguide_all\temp\workflow-demo`，总共只需要 4 张截图。第 1 张初始化图你已经完成，下面只执行后 3 步；不要求登录、注册、支付或发布操作。截图前先隐藏本地用户名、远程地址、令牌、Cookie、密钥、真实用户数据和私人仓库内容。

完整的真人式 Prompt 和对应截图内容保存在项目的 [PROMPTS.md](D:/codexguide_all/temp/workflow-demo/PROMPTS.md)。第 1 张沿用已发送的初始化 Prompt，后 3 张按该文件顺序执行。

1. `01-task-start.png`：保留你已经完成的初始化 Prompt 和 Codex 回复；画面显示项目目录、任务目标和只读起点。
2. `02-project-exploration.png`：发送“探索结论” Prompt；画面显示项目地图、文件职责、测试命令、当前疑点和未修改状态。
3. `03-bug-reproduce-and-fix.png`：发送“复现并修复 Bug” Prompt；画面显示检查 `python/python3`、确认当前运行时不可用、保留修复范围，不要把未执行的测试写成通过。
4. `04-refactor-test-summary.png`：发送“重构、写测试与收尾” Prompt；画面显示内部重构、风险场景、已编辑文件，以及“测试未执行，原因是 Python 不可用”的复盘。

如截图中出现账号、路径、密钥或用户数据，请立即删除该文件，不要放入 `manual/` 或 `online/`；重新截取脱敏版本。当前没有需要用户完成的登录、预览、发布或支付步骤。
