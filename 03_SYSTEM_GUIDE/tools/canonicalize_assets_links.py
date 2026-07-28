from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re


TEXT_SUFFIXES = {
    ".md",
    ".canvas",
    ".json",
    ".csv",
    ".txt",
    ".html",
    ".htm",
    ".xml",
    ".yml",
    ".yaml",
}

ATTACHMENT_PATH_RE = re.compile(r"(?<![A-Za-z0-9_-])(Attachment|Attachments)([\\/])")


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
    ignored_roots = {"assets", "Attachment", ".git", ".obsidian", "_merge_conflicts_Attachment_20260724"}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        parts = path.relative_to(root).parts
        if parts and parts[0] in ignored_roots:
            continue
        yield path


def rewrite_text(text: str) -> tuple[str, int]:
    return ATTACHMENT_PATH_RE.subn(lambda match: "assets" + match.group(2), text)


def append_log(root: Path, rewrites: int, files_rewritten: int) -> None:
    log_path = root / "01_INDEX" / "system_log.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## [{now}] repair | Canonicalize attachment directory to assets\n"
        f"Rewrote {rewrites} local `Attachment`/`Attachments` path references to `assets` "
        f"across {files_rewritten} text files.\n"
    )
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        fh.write(entry)


def main() -> None:
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
        new_text, count = rewrite_text(text)
        if count and new_text != text:
            updates.append((path, new_text, count))
            rewrites += count

    print(f"Mode={'APPLY' if args.apply else 'DRY_RUN'}")
    print(f"FilesWithTextRewrites={len(updates)}")
    print(f"TextReferencesToRewrite={rewrites}")
    for path, _, count in updates[:20]:
        print(f"Update={path.relative_to(root).as_posix()} ({count})")

    if args.apply:
        for path, new_text, _ in updates:
            write_text(path, new_text)
        append_log(root, rewrites, len(updates))


if __name__ == "__main__":
    main()
