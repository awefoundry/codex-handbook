#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


REQUIRED = {"filename", "kind", "width", "height", "article_section", "purpose", "source_url", "author", "published_at", "timestamp", "verification", "expiry_risk"}
FORBIDDEN_VISUAL_MARKERS = ("cover", "thumbnail", "封面", "缩略图")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a gzhstart workspace.")
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    root = args.workspace
    errors = []

    for path in (root / "manual", root / "online", root / "environment.md", root / "manifest.tsv", root / "manual-steps.md", root / "research-log.md"):
        if not path.exists():
            errors.append(f"missing: {path.name}")

    manifest = root / "manifest.tsv"
    if manifest.is_file():
        with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            missing = REQUIRED - set(reader.fieldnames or [])
            if missing:
                errors.append(f"manifest columns missing: {', '.join(sorted(missing))}")
            for line, row in enumerate(reader, start=2):
                filename = (row.get("filename") or "").strip()
                candidates = [root / "online" / filename, root / "manual" / filename]
                if filename and not any(path.is_file() for path in candidates):
                    errors.append(f"line {line}: file not found: {filename}")
                for field in ("kind", "article_section", "purpose", "verification"):
                    if not (row.get(field) or "").strip():
                        errors.append(f"line {line}: {field} is empty")
                visual_text = " ".join((row.get(field) or "").strip().lower() for field in ("filename", "kind", "purpose"))
                forbidden = next((marker for marker in FORBIDDEN_VISUAL_MARKERS if marker in visual_text), None)
                if forbidden:
                    errors.append(f"line {line}: disallowed cover/thumbnail candidate: {forbidden}")
                kind = (row.get("kind") or "").strip().lower()
                if "frame" in kind or "截帧" in kind:
                    if not (row.get("timestamp") or "").strip():
                        errors.append(f"line {line}: video frame requires timestamp")

    environment = root / "environment.md"
    if environment.is_file():
        content = environment.read_text(encoding="utf-8-sig")
        if "待填写" in content:
            errors.append("environment.md still contains placeholder values")
        for label in ("操作系统", "Codex", "插件"):
            if label not in content:
                errors.append(f"environment.md missing baseline item: {label}")

    if errors:
        print("Workspace validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Workspace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
