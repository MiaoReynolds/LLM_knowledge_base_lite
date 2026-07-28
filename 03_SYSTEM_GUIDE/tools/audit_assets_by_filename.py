from __future__ import annotations

import json
import re
from pathlib import Path


TEXT_SUFFIXES = {".md", ".canvas", ".json", ".csv", ".txt", ".html", ".htm"}
ASSET_RE = re.compile(r"(?:\.\./)*assets[\\/]([^)\]\"'\r\n<>]+)")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None


def main() -> None:
    root = Path.cwd()
    actual = {p.name for p in (root / "assets").glob("*") if p.is_file()}
    refs: list[tuple[str, str]] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        parts = path.relative_to(root).parts
        if parts and parts[0] in {"assets", ".git", ".obsidian", "03_SYSTEM_GUIDE"}:
            continue
        text = read_text(path)
        if text is None:
            continue
        if path.suffix.lower() == ".canvas":
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                data = None
            if isinstance(data, dict):
                for node in data.get("nodes", []):
                    if isinstance(node, dict):
                        value = node.get("file")
                        if isinstance(value, str) and value.replace("\\", "/").startswith("assets/"):
                            refs.append((path.relative_to(root).as_posix(), Path(value).name))
                continue
        for match in ASSET_RE.finditer(text):
            name = Path(match.group(1).replace("\\", "/")).name
            if "==" not in name and not name.startswith("http"):
                refs.append((path.relative_to(root).as_posix(), name))

    missing = [(source, name) for source, name in refs if name not in actual]
    print(f"ActualAssetFiles={len(actual)}")
    print(f"AssetReferences={len(refs)}")
    print(f"MissingByFilename={len(missing)}")
    for source, name in missing[:40]:
        print(f"Missing={source} -> {name}")


if __name__ == "__main__":
    main()
