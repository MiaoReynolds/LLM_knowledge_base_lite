# Workflows

This file describes how to interact with the system.

---

## 1. Add new notes

1. Write freely
2. Save into `/00_RAW` (new notes are unprocessed by default)
3. Ask: “整理文章” (or “Process unprocessed notes”)
4. Agent routes the source note into the right `/00_RAW/<category>/` folder
5. Agent creates or updates the summary in `/02_SUMMARY`
6. Agent links source -> summary and summary -> local topic page
7. Agent refreshes `/00_RAW/<category>/_目录.md`, `/04_TOPIC_MAP`, `/README_HUMAN.md`, and `/01_INDEX/master_index.md`
8. Agent rewrites old hyperlinks to the new moved path

You do NOT need to:
- classify
- rename perfectly
- organize folders

After processing, the agent should:
- classify into one existing category folder
- move the source note
- summarize into `/02_SUMMARY`
- link Markdown source notes to their summaries
- link summaries to local topic pages
- update links in `/01_INDEX`, `/02_SUMMARY`, `/README_HUMAN.md`, `/00_RAW/<category>/_目录.md`, and `/04_TOPIC_MAP`
- refresh category `_目录.md` pages so humans can browse article lists directly
- append latest source-note links to `/README_HUMAN.md` with date
- run integrity checks using `/03_SYSTEM_GUIDE/tools/validate_organize_articles.sh`

`“整理文章”` execution should follow:
- `/03_SYSTEM_GUIDE/skills/organize_articles.md`

---

## 2. Generate Or Refactor Categories

Ask:

- “初始化知识库”
- “根据我的笔记建立分类”
- “生成分类文件夹”
- “重构分类系统”
- “重新设计人眼浏览目录”
- “减少其它目录”

The agent should:
1. warn that large category analysis may consume many tokens
2. analyze folder names, titles, and summaries first
3. use raw-note snippets only when needed
4. propose a one-level `/00_RAW/<category>` system
5. estimate counts and ambiguous moves
6. wait for approval before large moves unless automatic execution was explicitly requested
7. rebuild `_目录.md`, `/04_TOPIC_MAP`, source-summary-topic links, `README_HUMAN`, and `master_index`

This workflow is reusable for both new users and existing vault refactors.
It should follow:
- `/03_SYSTEM_GUIDE/skills/generate_category_system.md`
- `/03_SYSTEM_GUIDE/category_design_rules.md`

---

## 3. Retrieve knowledge

Ask:

- “Do I have notes about [topic]?”
- “Summarize everything about [topic]”
- “Show key ideas related to [topic]”
The system should:
1. Use tree indexes first for broad browsing:
   - `/README_HUMAN.md`
   - `/04_TOPIC_MAP/README.md`
   - `/00_RAW/<category>/_目录.md`
2. Use `/01_INDEX/master_index.md` to narrow candidates
3. Read summaries
4. Only expand to full notes if needed

---

## 4. Build knowledge

Ask:

- “Turn my notes about [topic] into structured knowledge”
- “Extract key insights from these notes”
Output should go to `/02_SUMMARY` (as synthesis-style summary notes)

---

## 5. Project work

Store project-level tracking as summary notes in `/02_SUMMARY`

Ask:

- “Summarize project status”
- “What decisions have I made?”
- “What is still unresolved?”
---

## 6. Structural repair

Ask:

- “修复链接”
- “修复 RAW 和 Summary 对应关系”
- “检查并修复双向链接”
Agent should:
- run `/03_SYSTEM_GUIDE/skills/repair_links.md`
- repair mapping/link integrity and generated tree indexes
- refresh source -> summary -> topic links
- refresh `/00_RAW/<category>/_目录.md` and `/04_TOPIC_MAP`
- avoid resolving thesis/argument contradictions

---

## 7. System recovery

If unsure how to proceed:

Ask:

- “What can we do here?”
- “Guide me step by step”
Agent should read system guide files and assist.

---

## 8. Reflective synthesis (summary-only)

Ask:

- “反思”
- “举一反三”
- “从已有概念提出新概念”
- “基于已有 summary 生成新方向”

Agent should:
1. use `/01_INDEX/master_index.md` to narrow candidates
2. read only selected `/02_SUMMARY` files (default 3-8)
3. generate one new synthesis summary in `/02_SUMMARY`
4. emphasize concept combinations, TODO, overlooked concepts, and feasible directions
5. append the new summary path to `master_index` `## Summary Files`
6. append one `reflect` log entry to `/01_INDEX/system_log.md`

`“反思 / 举一反三”` execution should follow:
- `/03_SYSTEM_GUIDE/skills/reflect_synthesis.md`

---

## 下一篇 [[Design Principles.md]]
