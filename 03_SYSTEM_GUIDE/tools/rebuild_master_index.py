from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re


SOURCE_SUFFIXES = {".md", ".canvas"}
LEGACY_RAW_INDEX = "_目录.md"


@dataclass
class SummaryInfo:
    path: Path
    source_rel: str | None
    type_tag: str
    description: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wiki_to_path(target: str) -> str:
    target = target.split("|", 1)[0].strip()
    if not target.endswith((".md", ".canvas")):
        target = f"{target}.md"
    return target


def clean_plain_cell(text: str, limit: int | None = None) -> str:
    text = text.replace("\\|", " / ").replace("|", " / ")
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        return text[: limit - 3].rstrip() + "..."
    return text


def clean_location_cell(text: str) -> str:
    text = text.replace("\\|", " / ").replace("|", " / ")
    return text.replace("\r", " ").replace("\n", " ").strip()


def clean_summary_cell(text: str, limit: int | None = None) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("**", "").replace("__", "")
    text = text.replace("\\|", " / ").replace("|", " / ")
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        return text[: limit - 3].rstrip() + "..."
    return text


def parse_summary(path: Path) -> SummaryInfo:
    text = read_text(path)
    type_tag = "note/general"
    description = ""
    source_rel = None

    type_match = re.search(r"\*\*Type tag\*\*:\s*(.+)", text)
    if type_match:
        type_tag = type_match.group(1).strip()

    desc_match = re.search(r"\*\*Description\*\*:\s*(.+)", text)
    if desc_match:
        description = desc_match.group(1).strip()
    else:
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#") or line.startswith("**Type tag**") or line.startswith("**Source category**"):
                continue
            if line.startswith(">") or line.startswith("##") or line.startswith("- Original:") or line.startswith("- Topic:"):
                continue
            description = line.lstrip("- ").strip()
            break

    original_match = re.search(r"-\s*Original:\s*\[\[([^\]]+)\]\]", text)
    if original_match:
        source_rel = wiki_to_path(original_match.group(1))

    return SummaryInfo(path=path, source_rel=source_rel, type_tag=type_tag, description=description)


def iter_sources(root: Path) -> list[Path]:
    raw_root = root / "00_RAW"
    sources: list[Path] = []
    for path in raw_root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == LEGACY_RAW_INDEX:
            continue
        if path.suffix.lower() in SOURCE_SUFFIXES:
            sources.append(path)
    return sorted(sources, key=lambda p: p.relative_to(root).as_posix().lower())


def summary_infos(root: Path) -> tuple[dict[str, SummaryInfo], dict[str, list[SummaryInfo]]]:
    by_source: dict[str, SummaryInfo] = {}
    by_stem: dict[str, list[SummaryInfo]] = {}
    for path in sorted((root / "02_SUMMARY").glob("*.summary.md"), key=lambda p: p.name.lower()):
        info = parse_summary(path)
        if info.source_rel:
            by_source.setdefault(info.source_rel, info)
        summary_stem = path.name.removesuffix(".summary.md")
        by_stem.setdefault(summary_stem, []).append(info)
    return by_source, by_stem


def info_for_source(source: Path, root: Path, by_source: dict[str, SummaryInfo], by_stem: dict[str, list[SummaryInfo]]) -> SummaryInfo | None:
    rel = source.relative_to(root).as_posix()
    if rel in by_source:
        return by_source[rel]
    matches = by_stem.get(source.stem, [])
    if len(matches) == 1:
        return matches[0]
    return None


def table_row(root: Path, source: Path, info: SummaryInfo | None) -> str:
    rel = source.relative_to(root).as_posix()
    note = clean_plain_cell(source.stem)
    location = clean_location_cell(f"/{rel}")
    if info:
        type_tag = clean_plain_cell(info.type_tag or "note/general", 80)
        summary = clean_summary_cell(info.description or "(summary file exists but description is empty)", 260)
        status = "processed + summarized" if info.description else "processed + summary-needs-description"
    else:
        type_tag = "note/general"
        summary = "(missing summary)"
        status = "source-only / missing-summary"
    return f"| {note} | {location} | {type_tag} | {summary} | {status} |"


def build_master_index(root: Path) -> tuple[str, int, int]:
    by_source, by_stem = summary_infos(root)
    sources = iter_sources(root)
    summarized = 0
    rows = []
    for source in sources:
        info = info_for_source(source, root, by_source, by_stem)
        if info:
            summarized += 1
        rows.append(table_row(root, source, info))

    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# Master Index",
        "",
        f"Last updated: {today}",
        "",
        "## Retrieval Contract",
        "- This is a quick retrieval index for LLM answering.",
        "- Tree-first browsing entries:",
        "  - Human category tree: [[README_HUMAN.md]] -> `/04_TOPIC_MAP/<theme>/<category>.md` -> source notes",
        "  - Topic map tree: [[04_TOPIC_MAP/README.md]] -> theme index -> local category page",
        "  - Summary layer: `/02_SUMMARY/<note>.summary.md`",
        "- For user retrieval requests: first use the tree entries above when the user is browsing by category/theme; otherwise locate candidates in `## Processed Notes`, then read the corresponding files in `/02_SUMMARY`.",
        "- Default stopping depth is summary-level; do NOT read raw source notes unless explicitly requested or summary-level evidence is insufficient.",
        "- Local topic pages are allowed to link directly to source notes because each page is bounded by one category and serves as the human directory.",
        "- Reflection summaries generated by synthesis workflows are stored in `/02_SUMMARY` and should be retrieved like normal summaries.",
        "- New article maintenance chain: route source -> create summary -> source links to summary -> summary links to local topic page -> local topic page links to source/summary -> rebuild topic map, README_HUMAN, and this master index.",
        "",
        "## Table Schema",
        "- `Note`: source title, never empty; use the source filename without extension.",
        "- `Location`: source path only, always `/00_RAW/<category>/<filename>.md` or `.canvas`.",
        "- `Type`: short semantic type tag only; never put a path here.",
        "- `Summary`: one compact summary sentence from `/02_SUMMARY`; use `(missing summary)` only when no summary exists.",
        "- `Status`: controlled value such as `processed + summarized`, `processed + summary-needs-description`, or `source-only / missing-summary`.",
        "- Do not add extra columns, raw summary-file lists, or free-form appendices below the table.",
        "",
        "## Processed Notes",
        "",
        "| Note | Location | Type | Summary | Status |",
        "| ---- | -------- | ---- | ------- | ------ |",
        *rows,
        "",
    ]
    return "\n".join(lines), len(sources), summarized


def append_log(root: Path, source_count: int, summarized: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    missing = source_count - summarized
    entry = (
        f"\n## [{now}] master-index | Rebuild fixed-schema master index\n"
        "Rebuilt `/01_INDEX/master_index.md` from `/00_RAW` sources and `/02_SUMMARY` metadata using the fixed 5-column schema.\n"
        f"Source rows: {source_count}; summarized rows: {summarized}; missing-summary rows: {missing}.\n"
    )
    with (root / "01_INDEX" / "system_log.md").open("a", encoding="utf-8", newline="") as fh:
        fh.write(entry)


def main() -> None:
    root = Path.cwd()
    text, source_count, summarized = build_master_index(root)
    write_text(root / "01_INDEX" / "master_index.md", text)
    append_log(root, source_count, summarized)
    print(f"MasterIndexRows={source_count}")
    print(f"SummarizedRows={summarized}")
    print(f"MissingSummaryRows={source_count - summarized}")


if __name__ == "__main__":
    main()
