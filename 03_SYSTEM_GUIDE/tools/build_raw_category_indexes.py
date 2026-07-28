from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re


INDEX_NAME = "_目录.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def wiki(path: str, label: str | None = None) -> str:
    target = path.removesuffix(".md")
    return f"[[{target}|{label}]]" if label else f"[[{target}]]"


def is_source_note(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in {".md", ".canvas"} and path.name != INDEX_NAME


def source_notes(category_dir: Path) -> list[Path]:
    return sorted([p for p in category_dir.iterdir() if is_source_note(p)], key=lambda p: p.name.lower())


def topic_pages_by_category(root: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    topic_root = root / "04_TOPIC_MAP"
    if not topic_root.is_dir():
        return mapping
    for page in topic_root.glob("*/*.md"):
        if page.name != "index.md":
            mapping[page.stem] = page.relative_to(root).as_posix()
    return mapping


def find_human_browse_section(text: str) -> tuple[int, int, str] | None:
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith("## ")]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        body = "\n".join(lines[start + 1 : end])
        link_count = body.count("[[00_RAW/") + body.count("[[04_TOPIC_MAP/")
        if link_count >= 3:
            return start, end, lines[start]
    return None


def categories_in_human_order(root: Path) -> list[Path]:
    raw_root = root / "00_RAW"
    existing = {path.name: path for path in raw_root.iterdir() if path.is_dir()}
    ordered: list[Path] = []
    human = root / "README_HUMAN.md"
    if human.is_file():
        text = read_text(human)
        section = find_human_browse_section(text)
        if section:
            start, end, _heading = section
            body = "\n".join(text.splitlines()[start + 1 : end])
            candidates = []
            candidates.extend(re.findall(r"\[\[00_RAW/([^/\]\|]+)(?:/[^\]\|]*)?(?:\|[^\]]*)?\]\]", body))
            candidates.extend(re.findall(r"\[\[04_TOPIC_MAP/[^/\]\|]+/([^/\]\|]+)(?:\|[^\]]*)?\]\]", body))
            for category in candidates:
                category = category.removesuffix(".md")
                path = existing.pop(category, None)
                if path:
                    ordered.append(path)
    ordered.extend(existing[name] for name in sorted(existing, key=str.lower))
    return ordered


def update_human_readme(root: Path, categories: list[Path], topic_by_category: dict[str, str]) -> tuple[int, int]:
    human = root / "README_HUMAN.md"
    text = read_text(human) if human.is_file() else "# README_HUMAN\n"
    section = find_human_browse_section(text)
    heading = section[2] if section else "## 当前人眼浏览目录"

    lines = [heading]
    linked = 0
    missing = 0
    for category_dir in categories:
        category = category_dir.name
        topic_rel = topic_by_category.get(category)
        if topic_rel:
            lines.append(f"- {wiki(topic_rel, category)}")
            linked += 1
        else:
            lines.append(f"- [[00_RAW/{category}/|{category}]]")
            missing += 1
    replacement = "\n".join(lines)

    if section:
        start, end, _heading = section
        all_lines = text.splitlines()
        new_lines = all_lines[:start] + replacement.splitlines() + all_lines[end:]
        new_text = "\n".join(new_lines)
    else:
        new_text = text.rstrip() + "\n\n" + replacement
    write_text(human, new_text.rstrip() + "\n")
    return linked, missing


def append_log(root: Path, category_count: int, source_count: int, linked_count: int, missing_count: int) -> None:
    log_path = root / "01_INDEX" / "system_log.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## [{now}] human-index | Refresh human topic directory entries\n"
        "Refreshed `README_HUMAN.md` so the human browse tree points to `/04_TOPIC_MAP/<theme>/<category>.md` pages. "
        "This script no longer creates `/00_RAW/<category>/_目录.md`; topic pages are the canonical category directories.\n"
        f"Categories: {category_count}; source notes covered by category pages: {source_count}; topic-page links: {linked_count}; missing topic pages: {missing_count}.\n"
    )
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        fh.write(entry)


def main() -> None:
    root = Path.cwd()
    categories = categories_in_human_order(root)
    topic_by_category = topic_pages_by_category(root)
    source_count = sum(len(source_notes(category_dir)) for category_dir in categories)
    linked_count, missing_count = update_human_readme(root, categories, topic_by_category)
    append_log(root, len(categories), source_count, linked_count, missing_count)
    print(f"HumanTopicEntries={linked_count}")
    print(f"MissingTopicPages={missing_count}")
    print(f"SourceNotes={source_count}")
    print("RawCategoryIndexesCreated=0")


if __name__ == "__main__":
    main()
