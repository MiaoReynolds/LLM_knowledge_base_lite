from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt", ".html", ".htm", ".xml", ".yml", ".yaml", ".csv"}
REL_ATTACHMENT_RE = re.compile(r"(?<![A-Za-z0-9_-])(?P<prefix>(?:\.\.[\\/])*)Attachment(?P<slash>[\\/])")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def iter_text_files(root: Path):
    ignored_roots = {"Attachment", "assets", ".git", ".obsidian", "03_SYSTEM_GUIDE", "_merge_conflicts_Attachment_20260724"}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        parts = path.relative_to(root).parts
        if parts and parts[0] in ignored_roots:
            continue
        yield path


def normalized_prefix(root: Path, text_path: Path) -> str:
    target = root / "Attachment"
    import os

    path = os.path.relpath(target, text_path.parent).replace("\\", "/")
    return path + "/"


def normalize_text(root: Path, text_path: Path, text: str) -> tuple[str, int]:
    prefix = normalized_prefix(root, text_path)

    def repl(match: re.Match[str]) -> str:
        return prefix

    return REL_ATTACHMENT_RE.subn(repl, text)


def append_log(root: Path, rewrites: int, files_rewritten: int) -> None:
    log_path = root / "01_INDEX" / "system_log.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## [{now}] repair | Normalize attachment relative paths\n"
        f"Normalized {rewrites} `Attachment` relative path prefixes across {files_rewritten} text files.\n"
    )
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        fh.write(entry)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    updates: list[tuple[Path, str, int]] = []
    rewrites = 0
    for path in iter_text_files(root):
        text = read_text(path)
        if text is None:
            continue
        new_text, count = normalize_text(root, path, text)
        if count and new_text != text:
            updates.append((path, new_text, count))
            rewrites += count

    print(f"Mode={'APPLY' if args.apply else 'DRY_RUN'}")
    print(f"FilesWithAttachmentPrefixUpdates={len(updates)}")
    print(f"AttachmentPrefixUpdates={rewrites}")
    for path, _, count in updates[:20]:
        print(f"Update={path.relative_to(root).as_posix()} ({count})")

    if args.apply:
        for path, new_text, _ in updates:
            write_text(path, new_text)
        append_log(root, rewrites, len(updates))


if __name__ == "__main__":
    main()
