#!/usr/bin/env python3
import argparse
from datetime import datetime
from pathlib import Path


MANIFEST = "filename\tkind\twidth\theight\tarticle_section\tpurpose\tsource_url\tauthor\tpublished_at\ttimestamp\tverification\texpiry_risk\n"

MANUAL = """# 需要作者亲自截图\n\n每个步骤写明起始网址、菜单路径、预期画面、文件名、脱敏字段和停止位置。\n\n- [ ] `01-example.png`：URL → 菜单 → 页面；隐藏账号信息；停在提交按钮之前。\n"""

LOG = """# 素材查找记录\n\n| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |\n|---|---|---|---|---|\n"""

ENVIRONMENT = """# 教程环境与版本记录

> 正文开头只写一行“测试环境”摘要，仅保留影响教程界面或操作结果的组件与核验日期。本文件保留完整版本、取值位置和核验依据；不要记录账号、密钥或私人工作区名称。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | 待填写 | 系统信息 | 待填写 | 记录版本与构建号 |
| IDE / 宿主应用 | 待填写 | About / `--version` | 待填写 | 不适用时明确标注 |
| Codex | 待填写 | About / `codex --version` | 待填写 | 区分桌面端、CLI、IDE 扩展 |
| 目标插件 / App / Connector | 待填写 | 插件详情或官方目录 | 待填写 | 无独立版本号时不要猜测 |
| 其他关键依赖 | 待填写 | `--version` 或官方来源 | 待填写 | 仅保留影响教程复现的依赖 |
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a gzhstart screenshot and research workspace.")
    parser.add_argument("base_dir", type=Path, nargs="?", help="Destination directory for topic-only initialization")
    parser.add_argument("--slug", help="Folder label for topic-only initialization")
    parser.add_argument("--article", type=Path, help="Existing Markdown article; workspace is created beside it")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M"))
    args = parser.parse_args()

    if args.article:
        article = args.article.resolve()
        if article.suffix.lower() not in {".md", ".markdown"}:
            parser.error("--article must point to a Markdown file")
        if not article.is_file():
            parser.error(f"article not found: {article}")
        if args.base_dir or args.slug:
            parser.error("do not combine --article with base_dir or --slug")

        existing = sorted(
            path for path in article.parent.glob(f"{article.stem}-图片备份*")
            if path.is_dir() and (
                path.name == f"{article.stem}-图片备份"
                or path.name.startswith(f"{article.stem}-图片备份-")
            )
        )
        if existing:
            root = existing[-1]
            environment = root / "environment.md"
            if not environment.exists():
                environment.write_text(ENVIRONMENT, encoding="utf-8")
            print(f"existing\t{root.resolve()}")
            return 0

        root = article.parent / f"{article.stem}-图片备份-{args.timestamp}"
    else:
        if not args.base_dir or not args.slug:
            parser.error("topic-only initialization requires base_dir and --slug")
        root = args.base_dir.resolve() / f"{args.slug}-图片备份-{args.timestamp}"

    (root / "manual").mkdir(parents=True, exist_ok=False)
    (root / "online").mkdir()
    (root / "manifest.tsv").write_text(MANIFEST, encoding="utf-8")
    (root / "environment.md").write_text(ENVIRONMENT, encoding="utf-8")
    (root / "manual-steps.md").write_text(MANUAL, encoding="utf-8")
    (root / "research-log.md").write_text(LOG, encoding="utf-8")
    print(f"created\t{root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
