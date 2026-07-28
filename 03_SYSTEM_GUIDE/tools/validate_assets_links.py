from __future__ import annotations

import json
import re
from pathlib import Path


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

OLD_PATH_RE = re.compile(r"(?<![A-Za-z0-9_-])(Attachment|Attachments)[\\/]")
URL_RE = re.compile(r"https?://[^\s)\]\"']+")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^\r\n)]*assets[\\/][^\r\n)]+)\)")
HTML_SRC_RE = re.compile(r"""src=["']([^"']*assets[\\/][^"']+)["']""")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None


def iter_text_files(root: Path):
    ignored_roots = {"assets", ".git", ".obsidian", "03_SYSTEM_GUIDE"}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        parts = path.relative_to(root).parts
        if parts and parts[0] in ignored_roots:
            continue
        yield path


def attachment_links_from_text(path: Path, text: str) -> list[tuple[str, bool]]:
    links: list[tuple[str, bool]] = []
    if path.suffix.lower() == ".canvas":
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = None
        if isinstance(data, dict):
            for node in data.get("nodes", []):
                if isinstance(node, dict):
                    value = node.get("file")
                    if isinstance(value, str) and "assets/" in value.replace("\\", "/"):
                        links.append((value, True))
            return links
    for pattern in (MARKDOWN_LINK_RE, HTML_SRC_RE):
        for match in pattern.finditer(text):
            links.append((match.group(1), False))
    return links


def resolve_link(root: Path, text_path: Path, link: str, vault_relative: bool = False) -> Path:
    normalized = link.replace("\\", "/")
    if vault_relative or normalized.startswith("assets/"):
        return (root / normalized).resolve()
    return (text_path.parent / normalized).resolve()


def main() -> None:
    root = Path.cwd()
    residual_files: list[str] = []
    missing_links: list[str] = []
    assets_links = 0

    for path in iter_text_files(root):
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(root).as_posix()
        local_text = URL_RE.sub("", text)
        if OLD_PATH_RE.search(local_text):
            residual_files.append(rel)
        for link, vault_relative in attachment_links_from_text(path, text):
            if link.startswith("http://") or link.startswith("https://"):
                continue
            if "==" in link:
                continue
            assets_links += 1
            target = resolve_link(root, path, link, vault_relative=vault_relative)
            if not target.exists():
                missing_links.append(f"{rel} -> {link}")

    print(f"ResidualOldPathFiles={len(residual_files)}")
    print(f"AssetsLinks={assets_links}")
    print(f"MissingAssetsLinks={len(missing_links)}")
    for item in residual_files[:30]:
        print(f"ResidualOldPathFile={item}")
    for item in missing_links[:30]:
        print(f"MissingAssetsLink={item}")


if __name__ == "__main__":
    main()
