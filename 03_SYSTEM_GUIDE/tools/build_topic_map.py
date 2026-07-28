from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class TopicCategory:
    theme: str
    category: str
    description: str


TOPIC_CATEGORIES: list[TopicCategory] = []
CATEGORY_PROFILE_JSON = Path("01_INDEX") / "category_profile.json"
LEGACY_CATEGORY_PROFILE_JSON = Path("03_SYSTEM_GUIDE") / "local_rules" / "category_profile.json"
RAW_CATEGORY_INDEX_NAME = "_目录.md"
DEFAULT_THEME = "Unsorted Topics"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wiki(path: str, label: str | None = None) -> str:
    target = path.removesuffix(".md")
    return f"[[{target}|{label}]]" if label else f"[[{target}]]"


def load_topic_categories(root: Path) -> list[TopicCategory]:
    profile_path = root / CATEGORY_PROFILE_JSON
    if not profile_path.is_file() and (root / LEGACY_CATEGORY_PROFILE_JSON).is_file():
        profile_path = root / LEGACY_CATEGORY_PROFILE_JSON
    if profile_path.is_file():
        data = json.loads(read_text(profile_path))
        items: list[TopicCategory] = []
        for theme_block in data.get("themes", []):
            theme = str(theme_block.get("theme", DEFAULT_THEME)).strip() or DEFAULT_THEME
            for category_block in theme_block.get("categories", []):
                category = str(category_block.get("category", "")).strip()
                if not category:
                    continue
                description = str(category_block.get("description", "")).strip()
                items.append(TopicCategory(theme, category, description or "User-approved local category."))
        if items:
            return items

    raw_root = root / "00_RAW"
    if not raw_root.is_dir():
        return []
    return [
        TopicCategory(DEFAULT_THEME, category_dir.name, "Auto-discovered category. Generate a local profile to refine themes and descriptions.")
        for category_dir in sorted(raw_root.iterdir(), key=lambda p: p.name.lower())
        if category_dir.is_dir()
    ]


def source_notes(root: Path, category: str) -> list[Path]:
    category_dir = root / "00_RAW" / category
    if not category_dir.is_dir():
        return []
    return sorted(
        [
            p
            for p in category_dir.iterdir()
            if p.is_file() and p.suffix.lower() in {".md", ".canvas"} and p.name != RAW_CATEGORY_INDEX_NAME
        ],
        key=lambda p: p.name.lower(),
    )


def summary_path_for(root: Path, source: Path) -> Path:
    return root / "02_SUMMARY" / f"{source.stem}.summary.md"

def summary_preview(path: Path, limit: int = 180) -> str:
    if not path.is_file():
        return ""
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("- Original:") or line.startswith("- Source:") or line.startswith("- Topic:"):
            continue
        line = line.lstrip("- ").strip()
        if len(line) > limit:
            return line[: limit - 1].rstrip() + "..."
        return line
    return ""

def topic_page_rel(item: TopicCategory) -> str:
    return f"04_TOPIC_MAP/{item.theme}/{item.category}.md"


def grouped_categories(items: list[TopicCategory]) -> dict[str, list[TopicCategory]]:
    groups: dict[str, list[TopicCategory]] = {}
    for item in items:
        groups.setdefault(item.theme, []).append(item)
    return groups


def build_root_index(root: Path, items: list[TopicCategory]) -> None:
    now = datetime.now().strftime("%Y-%m-%d")
    groups = grouped_categories(items)
    lines = [
        "# 总主题目录",
        "",
        "这个目录是知识库的主题地图层，用来让 Obsidian 图谱从少数大星团变成可浏览的小主题网络。",
        "",
        "主链路规则：",
        "- source note -> summary",
        "- summary -> local topic page",
        "- local topic page -> theme index",
        "- theme index -> this root topic index",
        "",
        f"Last updated: {now}",
        "",
        "## 大主题入口",
        "",
    ]
    for theme in sorted(groups):
        lines.append(f"- {wiki(f'04_TOPIC_MAP/{theme}/index.md', theme)}")
    lines.extend(["", "## 维护入口", "", "- [[03_SYSTEM_GUIDE/SYSTEM_RULES#8.10 Topic Map Maintenance Rule]]", "- [[03_SYSTEM_GUIDE/tools/build_topic_map.py]]", ""])
    write_text(root / "04_TOPIC_MAP" / "README.md", "\n".join(lines))


def build_theme_index(root: Path, theme: str, items: list[TopicCategory]) -> None:
    lines = [
        f"# {theme}",
        "",
        f"- Up: {wiki('04_TOPIC_MAP/README.md', '总主题目录')}",
        "",
        "## 局部小目录",
        "",
    ]
    for item in items:
        count = len(source_notes(root, item.category))
        lines.append(f"- {wiki(topic_page_rel(item), item.category)} ({count}) - {item.description}")
    lines.append("")
    write_text(root / "04_TOPIC_MAP" / theme / "index.md", "\n".join(lines))


def build_category_page(root: Path, item: TopicCategory) -> None:
    notes = source_notes(root, item.category)
    with_summary = []
    without_summary = []
    for source in notes:
        summary = summary_path_for(root, source)
        if summary.is_file():
            with_summary.append((source, summary))
        else:
            without_summary.append(source)

    lines = [
        f"# {item.category}",
        "",
        f"- Up: {wiki(f'04_TOPIC_MAP/{item.theme}/index.md', item.theme)}",
        f"- Source folder: [[00_RAW/{item.category}/]]",
        f"- Summary count: {len(with_summary)}",
        f"- Source count: {len(notes)}",
        "",
        "## Source Links",
        "",
    ]
    if notes:
        for source, summary in with_summary:
            source_rel = source.relative_to(root).as_posix()
            summary_rel = summary.relative_to(root).as_posix()
            preview = summary_preview(summary)
            if preview:
                lines.append(f"- {wiki(source_rel, source.stem)} - Summary: {wiki(summary_rel, 'summary')} - {preview}")
            else:
                lines.append(f"- {wiki(source_rel, source.stem)} - Summary: {wiki(summary_rel, 'summary')}")
    else:
        lines.append("- No source notes found yet.")

    if without_summary:
        lines.extend(["", "## Missing Summary", ""])
        for source in without_summary[:100]:
            source_rel = source.relative_to(root).as_posix()
            lines.append(f"- {wiki(source_rel, source.stem)}")
        if len(without_summary) > 100:
            lines.append(f"- ... and {len(without_summary) - 100} more")
    lines.append("")
    write_text(root / topic_page_rel(item), "\n".join(lines))

def ensure_source_summary_link(root: Path, source: Path, summary: Path) -> bool:
    if source.suffix.lower() != ".md" or not summary.is_file():
        return False
    text = read_text(source)
    summary_rel = summary.relative_to(root).as_posix()
    marker = f"[[{summary_rel.removesuffix('.md')}"
    if marker in text or f"[[{summary_rel}" in text:
        return False
    block = [
        "",
        "## 知识图谱链接",
        "",
        f"- Summary: {wiki(summary_rel, source.stem + ' summary')}",
        "",
    ]
    write_text(source, text.rstrip() + "\n" + "\n".join(block))
    return True


def ensure_summary_topic_link(root: Path, summary: Path, item: TopicCategory) -> bool:
    text = read_text(summary)
    topic_rel = topic_page_rel(item)
    marker = f"[[{topic_rel.removesuffix('.md')}"
    if marker in text or f"[[{topic_rel}" in text:
        return False
    block = [
        "",
        "## 主题地图",
        "",
        f"- Topic: {wiki(topic_rel, item.category)}",
        "",
    ]
    write_text(summary, text.rstrip() + "\n" + "\n".join(block))
    return True


def apply_pilot_links(root: Path, items: list[TopicCategory], categories: set[str]) -> tuple[int, int]:
    source_updates = 0
    summary_updates = 0
    selected = categories or {item.category for item in items}
    for item in items:
        if item.category not in selected:
            continue
        for source in source_notes(root, item.category):
            summary = summary_path_for(root, source)
            if not summary.is_file():
                continue
            if ensure_source_summary_link(root, source, summary):
                source_updates += 1
            if ensure_summary_topic_link(root, summary, item):
                summary_updates += 1
    return source_updates, summary_updates


def append_log(root: Path, category_count: int, source_updates: int, summary_updates: int) -> None:
    log_path = root / "01_INDEX" / "system_log.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## [{now}] topic-map | Build topic-map layer\n"
        "Created/refreshed `/04_TOPIC_MAP` root, theme indexes, and local topic pages from the local category profile or auto-discovered RAW folders.\n"
        f"Topic categories: {category_count}.\n"
        f"Pilot source->summary links updated: {source_updates}; summary->topic links updated: {summary_updates}.\n"
    )
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        fh.write(entry)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-links", action="store_true", help="Add source->summary and summary->topic links for all loaded categories.")
    args = parser.parse_args()

    root = Path.cwd()
    topic_categories = load_topic_categories(root)
    build_root_index(root, topic_categories)
    for theme, theme_items in grouped_categories(topic_categories).items():
        build_theme_index(root, theme, theme_items)
        for item in theme_items:
            build_category_page(root, item)

    source_updates = 0
    summary_updates = 0
    if args.pilot_links:
        source_updates, summary_updates = apply_pilot_links(root, topic_categories, set())
    append_log(root, len(topic_categories), source_updates, summary_updates)
    print(f"TopicCategories={len(topic_categories)}")
    print(f"ProfilePath={CATEGORY_PROFILE_JSON}")
    print(f"ProfileLoaded={(root / CATEGORY_PROFILE_JSON).is_file()}")
    print(f"PilotSourceUpdates={source_updates}")
    print(f"PilotSummaryUpdates={summary_updates}")


if __name__ == "__main__":
    main()


