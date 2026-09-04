#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

REQUIRED = {
    "filename", "width", "height", "section", "purpose", "source_url",
    "author", "published_at", "timestamp", "provenance",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an article visual manifest.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--asset-dir", type=Path, required=True)
    args = parser.parse_args()

    errors = []
    with args.manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            errors.append(f"missing columns: {', '.join(sorted(missing))}")
        for line, row in enumerate(reader, start=2):
            filename = (row.get("filename") or "").strip()
            if not filename or not (args.asset_dir / filename).is_file():
                errors.append(f"line {line}: asset not found: {filename or '<empty>'}")
            for field in ("section", "purpose", "source_url", "author", "provenance"):
                if not (row.get(field) or "").strip():
                    errors.append(f"line {line}: {field} is empty")
            if not (row.get("source_url") or "").startswith(("https://", "http://")):
                errors.append(f"line {line}: source_url must be HTTP(S)")
            try:
                if int(row.get("width") or 0) < 1 or int(row.get("height") or 0) < 1:
                    raise ValueError
            except ValueError:
                errors.append(f"line {line}: invalid dimensions")

    if errors:
        print("Manifest validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Manifest validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
