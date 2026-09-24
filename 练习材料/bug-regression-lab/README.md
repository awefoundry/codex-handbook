# Bug 修复与回归测试练习

这是根据“订单缺少金额字段导致 `NaN`”案例整理的独立教学示例，不是生产项目。它只覆盖本练习约定的三类金额输入：`12.5` 显示为 `¥12.50`，`0` 显示为 `¥0.00`，缺少 `amount` 或收到 `undefined` 时显示 `--`。

## 环境和目录

- Node.js 22 或更高版本；本练习使用 Node 内置 `node:test` 和 `node:assert/strict`，不需要安装依赖。
- 读者实际操作的是 `starter/` 的副本，不要直接修改包内的 `starter/`。
- `reference/` 只用于完成后对照，里面的修复和回归测试不属于起始项目。

```text
bug-regression-lab/
├── README.md
├── TASK.md
├── CHECKLIST.md
├── starter/
│   ├── src/formatAmount.mjs
│   ├── demo.mjs
│   └── test/formatAmount.test.mjs
└── reference/
    ├── formatAmount.fixed.mjs
    ├── formatAmount.regression.test.mjs
    └── 参考差异.md
```

## 先确认 Node，再复制起点

在解压后的 `bug-regression-lab/` 根目录运行：

```bash
node --version
cp -R starter bug-regression-work
cd bug-regression-work
```

Windows PowerShell：

```powershell
node --version
Copy-Item -Recurse starter bug-regression-work
Set-Location bug-regression-work
```

如果 `node --version` 低于 22，先按 Node 官方文档准备兼容环境；不要为了本练习修改网站项目的 Node 版本或锁文件。

## 运行起始测试和复现命令

在 `bug-regression-work/` 内运行：

```bash
node --test test/formatAmount.test.mjs
node demo.mjs
```

起始测试只覆盖正常金额和合法的 `0`，应通过 2 条测试。复现命令会输出：

```text
A-100: ¥12.50
A-101: ¥NaN
```

这说明现象可以稳定复现；它不说明所有金额输入都已经被测试。

接下来按文章正文完成只读调查、增加测试、观察失败、修改副本并再次验证。需要重新开始时，保留当前副本，把 ZIP 重新解压到一个全新目录，再复制其中的 `starter/`；不要清空真实工作区，也不要执行破坏性 Git 重置。
