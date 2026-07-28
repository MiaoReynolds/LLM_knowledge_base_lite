from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


RAW_CATEGORY_INDEX_NAME = "_目录.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def wiki(path: str, label: str | None = None) -> str:
    target = path.removesuffix(".md")
    return f"[[{target}|{label}]]" if label else f"[[{target}]]"


def topic_pages_by_category(root: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    topic_root = root / "04_TOPIC_MAP"
    for page in topic_root.glob("*/*.md"):
        if page.name == "index.md":
            continue
        category = page.stem
        mapping[category] = page.relative_to(root).as_posix()
    return mapping


def source_has_summary_link(text: str, summary_rel: str) -> bool:
    no_ext = summary_rel.removesuffix(".md")
    return f"[[{no_ext}" in text or f"[[{summary_rel}" in text


def ensure_source_summary_link(root: Path, source: Path, summary: Path, apply: bool) -> bool:
    if source.suffix.lower() != ".md":
        return False
    text = read_text(source)
    summary_rel = summary.relative_to(root).as_posix()
    if source_has_summary_link(text, summary_rel):
        return False
    block = [
        "",
        "## Knowledge Graph Links",
        "",
        f"- Summary: {wiki(summary_rel, source.stem + ' summary')}",
        "",
    ]
    if apply:
        write_text(source, text.rstrip() + "\n" + "\n".join(block))
    return True


def replace_or_append_topic_link(text: str, topic_rel: str, category: str) -> tuple[str, bool]:
    desired = f"- Topic: {wiki(topic_rel, category)}"
    lines = text.rstrip().splitlines()
    changed = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("- Topic:") or stripped.startswith("Topic:"):
            if line != desired:
                lines[i] = desired
                changed = True
            return "\n".join(lines).rstrip() + "\n", changed

    block = [
        "",
        "## Topic Map",
        "",
        desired,
        "",
    ]
    return text.rstrip() + "\n" + "\n".join(block), True


def existing_topic_category(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("- Topic:") or stripped.startswith("Topic:")):
            continue
        if "|" in stripped and "]]" in stripped:
            return stripped.rsplit("|", 1)[1].split("]]", 1)[0]
    return None


def ensure_summary_topic_link(summary: Path, topic_rel: str, category: str, apply: bool) -> bool:
    text = read_text(summary)
    new_text, changed = replace_or_append_topic_link(text, topic_rel, category)
    if changed and apply:
        write_text(summary, new_text)
    return changed


def iter_raw_sources(root: Path):
    raw_root = root / "00_RAW"
    for category_dir in sorted(raw_root.iterdir(), key=lambda p: p.name.lower()):
        if not category_dir.is_dir():
            continue
        for source in sorted(category_dir.iterdir(), key=lambda p: p.name.lower()):
            if source.is_file() and source.suffix.lower() in {".md", ".canvas"} and source.name != RAW_CATEGORY_INDEX_NAME:
                yield category_dir.name, source


def categories_by_stem(root: Path) -> dict[str, set[str]]:
    mapping: dict[str, set[str]] = {}
    for category, source in iter_raw_sources(root):
        summary = root / "02_SUMMARY" / f"{source.stem}.summary.md"
        if summary.is_file():
            mapping.setdefault(source.stem, set()).add(category)
    return mapping


def primary_category_for_summary(summary: Path, categories: set[str]) -> str:
    existing = existing_topic_category(read_text(summary))
    if existing in categories:
        return existing
    return sorted(categories, key=str.lower)[0]


def append_log(root: Path, source_updates: int, summary_updates: int, missing_summaries: int) -> None:
    log_path = root / "01_INDEX" / "system_log.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## [{now}] topic-map | Link source-summary-topic graph\n"
        f"Source->summary links updated: {source_updates}; summary->topic links updated: {summary_updates}; "
        f"sources without summary skipped: {missing_summaries}.\n"
    )
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        fh.write(entry)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    topic_by_category = topic_pages_by_category(root)
    stem_categories = categories_by_stem(root)
    source_updates = 0
    summary_updates = 0
    sources_with_summary = 0
    missing_summaries = 0
    missing_topic_pages = 0
    source_samples: list[str] = []
    summary_samples: list[str] = []

    for category, source in iter_raw_sources(root):
        summary = root / "02_SUMMARY" / f"{source.stem}.summary.md"
        if not summary.is_file():
            missing_summaries += 1
            continue
        sources_with_summary += 1
        if ensure_source_summary_link(root, source, summary, args.apply):
            source_updates += 1
            if len(source_samples) < 20:
                source_samples.append(source.relative_to(root).as_posix())

        topic_rel = topic_by_category.get(category)
        if topic_rel:
            categories = stem_categories.get(source.stem, {category})
            if len(categories) > 1 and category != primary_category_for_summary(summary, categories):
                continue
            if ensure_summary_topic_link(summary, topic_rel, category, args.apply):
                summary_updates += 1
                if len(summary_samples) < 20:
                    summary_samples.append(summary.relative_to(root).as_posix())
        else:
            missing_topic_pages += 1

    print(f"Mode={'APPLY' if args.apply else 'DRY_RUN'}")
    print(f"SourcesWithSummary={sources_with_summary}")
    print(f"SourceSummaryUpdates={source_updates}")
    print(f"SummaryTopicUpdates={summary_updates}")
    print(f"SourcesWithoutSummary={missing_summaries}")
    print(f"SourcesMissingTopicPage={missing_topic_pages}")
    for sample in source_samples:
        print(f"SourceNeedsSummaryLink={sample}")
    for sample in summary_samples:
        print(f"SummaryNeedsTopicLink={sample}")

    if args.apply:
        append_log(root, source_updates, summary_updates, missing_summaries)


if __name__ == "__main__":
    main()
