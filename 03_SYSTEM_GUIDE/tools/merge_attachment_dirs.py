from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from datetime import datetime
from pathlib import Path


SOURCE_DIRS = ["Attachment", "Attachments"]
TARGET_DIR = "assets"
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def iter_attachment_files(root: Path):
    for source_dir in SOURCE_DIRS:
        base = root / source_dir
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*"), key=lambda item: item.as_posix().lower()):
            if path.is_file():
                yield source_dir, path, path.relative_to(base)


def iter_text_files(root: Path):
    ignored_root_names = {TARGET_DIR, *SOURCE_DIRS, ".git", ".obsidian"}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if rel_parts and rel_parts[0] in ignored_root_names:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


PATH_SEGMENT_RE = re.compile(r"(?<![A-Za-z0-9_-])(Attachment|Attachments)([\\/])")


def rewrite_attachment_paths(text: str) -> tuple[str, int]:
    return PATH_SEGMENT_RE.subn(lambda match: "assets" + match.group(2), text)


def remove_empty_dirs(path: Path, stop_at: Path) -> None:
    current = path
    while current != stop_at and current.exists():
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def append_log(root: Path, copied: int, skipped_same: int, rewrites: int, files_rewritten: int) -> None:
    log_path = root / "01_INDEX" / "system_log.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## [{now}] repair | Merge attachment directories\n"
        f"Merged `Attachment` and `Attachments` into `assets`; copied {copied} files, "
        f"skipped {skipped_same} duplicate-identical files, rewrote {rewrites} attachment path references "
        f"across {files_rewritten} text files.\n"
    )
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        fh.write(entry)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--fast-move", action="store_true", help="Use same-volume move for non-colliding files; hash only existing target collisions.")
    parser.add_argument("--rewrite-only", action="store_true", help="Only rewrite text references from assets/Attachments to Attachment/.")
    args = parser.parse_args()

    root = Path.cwd()

    if args.rewrite_only:
        text_updates: list[tuple[Path, str, int]] = []
        rewrite_count = 0
        for text_path in iter_text_files(root):
            text = read_text(text_path)
            if text is None:
                continue
            new_text, count = rewrite_attachment_paths(text)
            if count:
                text_updates.append((text_path, new_text, count))
                rewrite_count += count
        print(f"Mode={'APPLY' if args.apply else 'DRY_RUN'}")
        print("RewriteOnly=True")
        print(f"FilesWithTextRewrites={len(text_updates)}")
        print(f"TextReferencesToRewrite={rewrite_count}")
        if args.apply:
            files_rewritten = 0
            for text_path, new_text, _ in text_updates:
                write_text(text_path, new_text)
                files_rewritten += 1
            append_log(root, 0, 0, rewrite_count, files_rewritten)
            print(f"FilesRewritten={files_rewritten}")
        return

    target_root = root / TARGET_DIR
    files = list(iter_attachment_files(root))

    collisions: list[tuple[str, str, str]] = []
    copied = 0
    skipped_same = 0

    for source_dir, source_path, rel in files:
        target_path = target_root / rel
        if target_path.exists():
            if sha256(source_path) == sha256(target_path):
                skipped_same += 1
                continue
            collisions.append((source_dir, source_path.relative_to(root).as_posix(), target_path.relative_to(root).as_posix()))

    text_updates: list[tuple[Path, str, int]] = []
    rewrite_count = 0
    for text_path in iter_text_files(root):
        text = read_text(text_path)
        if text is None:
            continue
        new_text, count = rewrite_attachment_paths(text)
        if count:
            text_updates.append((text_path, new_text, count))
            rewrite_count += count

    print(f"Mode={'APPLY' if args.apply else 'DRY_RUN'}")
    print(f"SourceFiles={len(files)}")
    print(f"NameCollisions={len(collisions)}")
    print(f"DuplicateIdenticalFiles={skipped_same}")
    print(f"FilesWithTextRewrites={len(text_updates)}")
    print(f"TextReferencesToRewrite={rewrite_count}")
    for _, source_rel, target_rel in collisions[:20]:
        print(f"Collision={source_rel} -> {target_rel}")

    if collisions:
        print("ABORT=Name collisions with different content must be resolved before applying.")
        return
    if not args.apply:
        return

    target_root.mkdir(parents=True, exist_ok=True)
    for source_dir, source_path, rel in files:
        target_path = target_root / rel
        if target_path.exists() and sha256(source_path) == sha256(target_path):
            source_path.unlink()
            remove_empty_dirs(source_path.parent, root / source_dir)
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if args.fast_move:
            shutil.move(str(source_path), str(target_path))
        else:
            shutil.copy2(source_path, target_path)
            if sha256(source_path) != sha256(target_path):
                raise RuntimeError(f"Hash verification failed: {source_path} -> {target_path}")
            source_path.unlink()
        copied += 1
        remove_empty_dirs(source_path.parent, root / source_dir)

    for source_dir in SOURCE_DIRS:
        source_root = root / source_dir
        if source_root.exists():
            remove_empty_dirs(source_root, root)

    files_rewritten = 0
    for text_path, new_text, _ in text_updates:
        write_text(text_path, new_text)
        files_rewritten += 1

    append_log(root, copied, skipped_same, rewrite_count, files_rewritten)
    print(f"CopiedFiles={copied}")
    print(f"FilesRewritten={files_rewritten}")


if __name__ == "__main__":
    main()
