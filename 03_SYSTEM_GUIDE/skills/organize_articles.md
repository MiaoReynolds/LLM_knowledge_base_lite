# Skill: Organize Articles

This skill standardizes the command family:
- “整理文章”
- “整理新文章”
- “处理未整理笔记”
- “更新索引”

Use this skill to minimize agent interpretation drift.

Core design:
- new notes become useful only after they enter the source -> summary -> tree-index chain
- humans browse through `README_HUMAN` -> `/04_TOPIC_MAP/<theme>/<category>.md` -> source notes
- agents retrieve through `master_index` and `/02_SUMMARY` before reading raw notes
- local topic pages are the canonical category directories; they list direct source links plus summary links/previews
- `/00_RAW/<category>` remains a shallow storage/category layer, not a separate directory-page layer

---

## 1. Trigger

Run this skill when the user intent is to:
- process newly added notes
- route notes into `/00_RAW/<category>/`
- refresh summary/index/topic pages and log the action
- repair path consistency after moves

---

## 2. Fixed Execution Order

1. Discover candidates
- scan vault root for note files (except `/README.md` and `/README_HUMAN.md`)
- scan `/00_RAW` for uncataloged notes
- ignore generated/navigation pages under `/03_SYSTEM_GUIDE`, `/01_INDEX`, `/02_SUMMARY`, and `/04_TOPIC_MAP`
- obsolete `/00_RAW/<category>/_目录.md` files, if encountered from old versions, are navigation artifacts and must not be summarized as source notes

2. Route and move
- assign exactly one category folder under `/00_RAW`
- discover available one-level category folders directly from the current `/00_RAW` directory
- allow user-created folders under `/00_RAW` to be used immediately without rule-file edits, then add a matching local topic page under `/04_TOPIC_MAP/<theme>/`
- prefer the human-browse categories documented in `/03_SYSTEM_GUIDE/SYSTEM_RULES.md` section 8.7.1 when title/summary evidence is clear
- keep personal/contact/philosophy/inspiration/TODO notes in their broad human categories unless user intent or note content clearly says otherwise
- move source notes to the target category

3. Summarize
- create or update summary files in `/02_SUMMARY`
- ensure each summary has `## 相关文章`
- each summary must contain a valid source link to the current `/00_RAW/<category>/<source>` path
- summaries are the default semantic retrieval layer; do not force future retrieval to read source notes first

4. Update tree indexes
- maintain `/04_TOPIC_MAP` according to `/03_SYSTEM_GUIDE/SYSTEM_RULES.md` section 8.10
- each local topic page should be the category's human-readable directory and must list direct source-note links
- each local topic page should also expose summary links or compact summary previews so AI can narrow candidates quickly
- theme index pages should link to local topic pages, and `/04_TOPIC_MAP/README.md` should link to theme indexes
- `README_HUMAN.md` should link to `/04_TOPIC_MAP/<theme>/<category>.md` pages, not `_目录.md` pages or bare raw folders
- run or follow `/03_SYSTEM_GUIDE/tools/build_topic_map.py` after category or summary changes
- run or follow `/03_SYSTEM_GUIDE/tools/build_raw_category_indexes.py` after moving notes or creating categories; despite its legacy name, it refreshes `README_HUMAN` topic links and must not create RAW `_目录.md` pages

5. Update source-summary-topic links
- source `.md` notes should link to their own summary using a `Summary:` link when a summary exists
- each summary should link to exactly one local topic page using a `Topic:` link when the source category is known
- run or follow `/03_SYSTEM_GUIDE/tools/link_summary_topic_graph.py --apply`

6. Update retrieval layer & System Log
- rebuild `/01_INDEX/master_index.md` with `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`
- keep `master_index` in fixed-schema quick-index mode: `## Retrieval Contract`, `## Table Schema`, and one `## Processed Notes` table
- the `Processed Notes` table must have exactly five columns: `Note`, `Location`, `Type`, `Summary`, `Status`
- do not manually append rows, add extra columns, or create a `## Summary Files` list
- `master_index` should explain that retrieval normally stops at summary-level, with raw notes used as evidence on demand
- append action log to `/01_INDEX/system_log.md` (e.g. `## [YYYY-MM-DD HH:MM] ingest | Article Name`)
- update related path references across generated notes

7. Update human entry
- keep `README_HUMAN.md` section `## 当前人眼浏览目录` synchronized with `/04_TOPIC_MAP/<theme>/<category>.md`
- update `README_HUMAN.md` section: `## 文章更新目录（最新在前）`
- use fixed line format: `- YYYY-MM-DD｜[[relative/path.ext]]` (`.md` or `.canvas`)

8. Validate integrity
- run available Python validators first on Windows; WSL/bash validation may fail in this vault and should not be the only validation path
- check that topic links in `README_HUMAN.md` resolve to existing files
- check that `link_summary_topic_graph.py --apply` is idempotent or reports only explicit residual items
- check that `master_index.md` has exactly five table columns, no empty `Note` cells, and no `## Summary Files` section

---

## 3. Definition Of Done

A run is complete only when:
- no newly added note files remain in vault root (except `README` files)
- every new processed note has a summary entry, unless explicitly logged as source-without-summary
- every new processed Markdown source note links to its summary when a summary exists
- every new summary links to its local topic page
- every new processed note is represented in `/04_TOPIC_MAP` through local topic page direct source links and source -> summary -> local topic links when summary and category are known
- `README_HUMAN` points to `/04_TOPIC_MAP/<theme>/<category>.md` pages for human browsing
- no new `/00_RAW/<category>/_目录.md` files are generated
- `master_index` is rebuilt by `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`
- `master_index` processed rows point to existing source files and use the fixed five-column schema
- retrieval can stop at summary-level using `master_index` -> `/02_SUMMARY` mapping
- `README_HUMAN` contains links to newly processed source notes in the update log
- moved paths are reflected in index/summary/topic files
- integrity validation returns success or logs explicit residual risk

---

## 4. Idempotency Rules

Repeated runs must:
- not duplicate `README_HUMAN` directory lines
- not duplicate summary files for the same source
- not reinsert identical index rows
- not rewrite unrelated files
- not recreate obsolete RAW `_目录.md` pages

When uncertain:
- prefer update-in-place
- avoid destructive operations unless the user explicitly asks for cleanup or migration

---

## 5. Non-goals

Do NOT:
- rewrite original source note content unless requested
- force deep folder taxonomy
- treat formatting perfection as higher priority than consistency and retrievability
