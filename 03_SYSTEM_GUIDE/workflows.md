# Workflows

This file describes how to interact with the system.

---

## 1. Add new notes

1. Write freely
2. Save into `/00_RAW` (new notes are unprocessed by default)
3. Ask: “整理文章” (or “Process unprocessed notes”)
4. After processing, move source note into the right `/00_RAW/<category>/` folder
5. Rewrite old hyperlinks to the new moved path
6. Update `/README_HUMAN.md` article update directory (latest-first)

You do NOT need to:
- classify
- rename perfectly
- organize folders

After processing, the agent should:
- classify into one existing category folder
- move the source note
- update links in `/01_INDEX` and `/02_SUMMARY`
- append latest source-note links to `/README_HUMAN.md` with date
- run integrity checks using `/03_SYSTEM_GUIDE/tools/validate_organize_articles.sh`

`“整理文章”` execution should follow:
- `/03_SYSTEM_GUIDE/skills/organize_articles.md`

---

## 2. Retrieve knowledge

Ask:

- “Do I have notes about [topic]?”
- “Summarize everything about [topic]”
- “Show key ideas related to [topic]”
The system should:
1. Check index
2. Read summaries
3. Only expand to full notes if needed

---

## 3. Build knowledge

Ask:

- “Turn my notes about [topic] into structured knowledge”
- “Extract key insights from these notes”
Output should go to `/02_SUMMARY` (as synthesis-style summary notes)

---

## 4. Project work

Store project-level tracking as summary notes in `/02_SUMMARY`

Ask:

- “Summarize project status”
- “What decisions have I made?”
- “What is still unresolved?”
---

## 5. Structural repair

Ask:

- “修复链接”
- “修复 RAW 和 Summary 对应关系”
- “检查并修复双向链接”
Agent should:
- run `/03_SYSTEM_GUIDE/skills/repair_links.md`
- repair mapping/link integrity only
- avoid resolving thesis/argument contradictions

---

## 6. System recovery

If unsure how to proceed:

Ask:

- “What can we do here?”
- “Guide me step by step”
Agent should read system guide files and assist.

---

## 7. Reflective synthesis (summary-only)

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

