# Skill: Reorganize Processed Articles

This skill standardizes the command family:
- “重新整理已处理文章”
- “更新 [文章名] 的摘要”
- “重新总结这篇笔记”

Use this skill when an already processed article has been modified by the user and its summary/index needs to be refreshed.

---

## 1. Trigger

Run this skill when the user intent is to:
- re-process an existing note that has already been routed into `/00_RAW/<category>/`
- update its existing summary to reflect new edits
- update its tags and relations in the index

---

## 2. Fixed Execution Order

1. **Verify State**
- Ensure the target article is already located in a `/00_RAW/<category>/` folder.
- Ensure the target article already has a corresponding summary file in `/02_SUMMARY`.

2. **Re-Summarize (In-Place)**
- Read the updated source note.
- Overwrite the *existing* summary file in `/02_SUMMARY` with the new summary content.
- DO NOT create a new file. Keep the existing filename.
- Ensure the `## 相关文章` section is maintained or updated with the most relevant links.

3. **Update Retrieval Layer & System Log (In-Place)**
- Update the existing row for this article in `/01_INDEX/master_index.md`.
- Append action log to `/01_INDEX/system_log.md` (e.g. `## [YYYY-MM-DD HH:MM] reorganize | Article Name`).

4. **Human Entry Bypass**
- Do NOT append a new entry to `README_HUMAN.md`'s “文章更新目录” unless the file path actually changed.
- This prevents spamming the timeline with minor updates.

---

## 3. Definition Of Done

A run is complete only when:
- the existing summary file reflects the latest source content.
- no duplicate summary files were created.
- the master index contains the updated metadata for the existing row.
- the original source file remains in its correct folder.

---

## 4. Idempotency Rules

Repeated runs must:
- only overwrite the existing summary file.
- update index rows in-place (no duplication).

---

## 5. Non-goals

Do NOT:
- use this skill for newly added, unprocessed notes (use `organize_articles` instead).
- change the source note's path unless requested.
- duplicate logging.
