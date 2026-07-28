# Skill: Repair Link Integrity

This skill standardizes the command family:
- “修复链接”
- “修复 RAW 和 Summary 对应关系”
- “修复索引与摘要链接完整性”
- “检查并修复双向链接”

Use this skill to repair structural consistency only.

---

## 1. Trigger

Run this skill when the user intent is to:
- audit RAW and SUMMARY one-to-one mapping integrity
- repair broken links between `/00_RAW` and `/02_SUMMARY`
- repair path drift in index/summary/project/knowledge references
- repair the human-browse tree (`README_HUMAN` -> topic category pages -> source notes)
- repair the topic-map tree (`04_TOPIC_MAP` -> local category page -> summaries/source notes)

Do NOT use this skill to resolve argument-level contradictions or final-conclusion conflicts.

---

## 2. Fixed Execution Order

1. Build mapping baselines
- enumerate source notes under `/00_RAW` (`.md` and `.canvas`)
- exclude obsolete `/00_RAW/<category>/_目录.md` files if they exist; these are legacy navigation pages, not source notes
- enumerate summaries under `/02_SUMMARY` (`*.summary.md`)
- read each summary `## Source` or `## 相关文章` block and parse its source link
- enumerate topic-map pages under `/04_TOPIC_MAP`
- enumerate `README_HUMAN.md` topic links

2. Validate one-to-one relation
- detect source-without-summary
- detect summary-without-source (orphan)
- detect duplicate summaries pointing to the same source

3. Validate bidirectional links
- in each summary, enforce `## 相关文章` contains exactly one valid source link to `/00_RAW/...`
- in each Markdown source note, enforce one valid `Summary:` link to its summary when a summary exists
- in each summary, enforce one valid `Topic:` link to the local topic page for its current source category
- in each local topic page, ensure source notes in its mapped category are directly listed, with summary links or compact summary previews when summaries exist
- in source notes, repair path references if they still point to old moved paths
- update cross-file references in `/01_INDEX`, `/02_SUMMARY`, `/README_HUMAN.md`, and `/04_TOPIC_MAP` when paths drifted

4. Repair index consistency
- ensure `/01_INDEX/master_index.md` processed rows point to existing source files
- rebuild `/01_INDEX/master_index.md` with `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`
- keep `master_index` in fixed-schema quick-index + tree-entry mode
- ensure the `Processed Notes` table has exactly five columns: `Note`, `Location`, `Type`, `Summary`, `Status`
- ensure there is no `## Summary Files` section, no raw `/02_SUMMARY` file list, and no free-form appendix below the table
- ensure `master_index` points agents toward `/README_HUMAN.md`, `/04_TOPIC_MAP/README.md`, and summary-level retrieval before raw-note reads

5. Rebuild generated tree pages
- run or follow `/03_SYSTEM_GUIDE/tools/build_topic_map.py`
- run or follow `/03_SYSTEM_GUIDE/tools/build_raw_category_indexes.py`; despite its legacy name, it refreshes `README_HUMAN` topic links and must not create RAW `_目录.md` pages
- run or follow `/03_SYSTEM_GUIDE/tools/link_summary_topic_graph.py --apply`
- run or follow `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`

6. Write operation log
- append action log to `/01_INDEX/system_log.md` (e.g. `## [YYYY-MM-DD HH:MM] repair | Link Integrity`)

7. Validate after repair
- re-check source/summary one-to-one mapping
- re-check broken links count is zero or reduced with explicit residual list
- re-check `README_HUMAN` category links point to existing `/04_TOPIC_MAP/<theme>/<category>.md` pages
- re-check source-summary-topic graph is idempotent (`SourceSummaryUpdates=0`, `SummaryTopicUpdates=0`) or report exact residual updates
- re-check no obsolete `/00_RAW/<category>/_目录.md` pages were recreated unless the user explicitly requested legacy compatibility
- re-check `master_index.md` has exactly five table columns, no empty `Note` cells, and no `## Summary Files` section

---

## 3. Definition Of Done

A run is complete only when:
- every processed source note has exactly one summary, unless explicitly logged as source-without-summary
- every summary points to an existing source path
- summary `## 相关文章` source link is valid
- Markdown source notes link to their summaries when summaries exist
- summaries link to local topic pages when source categories are known
- every `/04_TOPIC_MAP/<theme>/<category>.md` category page lists direct source-note links for its mapped category
- `README_HUMAN` links to category pages under `/04_TOPIC_MAP`, not `_目录.md` pages or bare folders
- `master_index` is rebuilt by `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`
- `master_index` source rows resolve to existing files and use the fixed five-column schema
- `system_log` contains one repair entry for the run

If full repair is not possible, output explicit residual items and reasons.

---

## 4. Idempotency Rules

Repeated runs must:
- not duplicate summary files
- not duplicate index rows
- not duplicate the same link line within one note
- not recreate legacy RAW `_目录.md` pages
- preserve existing content semantics while repairing structure

---

## 5. Non-goals

Do NOT:
- resolve thesis/argument contradictions across notes
- rewrite user's original claims for epistemic consistency
- force new conclusions or merged final viewpoints
