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

Do NOT use this skill to resolve argument-level contradictions or final-conclusion conflicts.

---

## 2. Fixed Execution Order

1. Build mapping baselines
- enumerate source notes under `/00_RAW` (`.md` and `.canvas`)
- enumerate summaries under `/02_SUMMARY` (`*.summary.md`)
- read each summary `## Source` block and parse `- Original: ...`

2. Validate one-to-one relation
- detect source-without-summary
- detect summary-without-source (orphan)
- detect duplicate summaries pointing to the same source

3. Validate bidirectional links
- in each summary, enforce `## 相关文章` contains exactly one valid source link to `/00_RAW/...`
- in source notes, repair path references if they still point to old moved paths
- update cross-file references in `/01_INDEX`, `/02_SUMMARY`, `/02_SUMMARY` when paths drifted

4. Repair index consistency
- ensure `/01_INDEX/master_index.md` processed rows point to existing source files
- ensure `/01_INDEX/master_index.md` `## Summary Files` points to existing summary files
- keep `master_index` in quick-index mode

5. Write operation log
- append action log to `/01_INDEX/system_log.md` (e.g. `## [YYYY-MM-DD HH:MM] repair | Link Integrity`)

6. Validate after repair
- re-check source/summary one-to-one mapping
- re-check broken links count is zero or reduced with explicit residual list

---

## 3. Definition Of Done

A run is complete only when:
- every processed source note has exactly one summary
- every summary points to an existing source path
- summary `## 相关文章` source link is valid
- `master_index` source rows and summary rows resolve to existing files
- `system_log` contains one repair entry for the run

If full repair is not possible, output explicit residual items and reasons.

---

## 4. Idempotency Rules

Repeated runs must:
- not duplicate summary files
- not duplicate index rows
- not duplicate the same link line within one note
- preserve existing content semantics while repairing structure

---

## 5. Non-goals

Do NOT:
- resolve thesis/argument contradictions across notes
- rewrite user's original claims for epistemic consistency
- force new conclusions or merged final viewpoints
