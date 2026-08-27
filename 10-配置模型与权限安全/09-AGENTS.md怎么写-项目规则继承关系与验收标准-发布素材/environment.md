# 教程环境与版本记录

仅记录本轮实际影响输出的工具和环境。网页截图使用本机 Chromium，示意图使用内置 image_gen，成品边框使用 Pillow。

| 项目 | 版本/状态 | 获取方式 | 核验日期 |
| --- | --- | --- | --- |
| 操作系统 | Windows 11 专业版 24H2（Build 26100） | `Get-CimInstance Win32_OperatingSystem` | 2026-08-27 |
| PowerShell | 7.6.4 | `$PSVersionTable.PSVersion` | 2026-08-27 |
| Chromium | 1234（Playwright 浏览器运行时） | `C:\Users\666\AppData\Local\ms-playwright\chromium-1234\chrome-win64\chrome.exe` | 2026-08-27 |
| Python | 3.13.5 | `python --version` | 2026-08-27 |
| Pillow | 12.3.0 | `python -c "import PIL; print(PIL.__version__)"` | 2026-08-27 |
| image_gen | 内置图像生成工具；任务目录 `01a04222-fb50-77c2-878f-05c7944bb102` | 工具返回记录 | 2026-08-27 |
