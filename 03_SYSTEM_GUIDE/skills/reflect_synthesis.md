# Skill: Reflective Synthesis (反思 / 举一反三)

This skill standardizes the command family:
- “反思”
- “举一反三”
- “从已有概念提出新概念”
- “基于已有 summary 生成新方向”

Use this skill to generate a new concept-level summary from existing linked summaries.

---

## 1. Trigger

Run this skill when the user intent is to:
- combine several existing concepts into a new concept
- extract overlooked ideas and next directions
- create a strategy / TODO-oriented synthesis note

Hard boundary:
- read from `/01_INDEX/master_index.md` and `/02_SUMMARY` first
- do NOT read `/00_RAW` unless user explicitly asks for raw-level verification

---

## 2. Fixed Execution Order

1. Scope and candidate selection
- locate candidate notes via `/01_INDEX/master_index.md`
- prioritize connected summaries via each summary's `## 相关文章`
- select a compact set (recommended 3-8 summaries)

2. Summary-only reading
- read only selected files under `/02_SUMMARY`
- stop at summary layer by default

3. Concept synthesis
- produce one new synthesis output that includes:
  - concept combinations (A + B -> new C)
  - actionable TODOs
  - possibly overlooked concepts
  - feasible forward directions
  - key assumptions and risks

4. Write as a new summary file
- create one new file in `/02_SUMMARY`
- recommended filename:
  - `反思-<topic>-YYYYMMDD.summary.md`
- required sections:
  - `## Source Summaries`
  - `## New Concept(s)`
  - `## TODO`
  - `## Overlooked Concepts`
  - `## Feasible Directions`
  - `## Assumptions / Risks`
  - `## 相关文章`

5. Update retrieval layer and operation log
- append this new summary path to `/01_INDEX/master_index.md` -> `## Summary Files`
- append one log entry to `/01_INDEX/system_log.md`:
  - `## [YYYY-MM-DD HH:MM] reflect | <topic>`

6. Link integrity pass
- ensure every file listed in `## Source Summaries` exists
- ensure every link in `## 相关文章` resolves to an existing summary path

---

## 3. Definition Of Done

A run is complete only when:
- a new reflection summary exists in `/02_SUMMARY`
- it cites source summaries (not RAW) in `## Source Summaries`
- `master_index` includes this summary under `## Summary Files`
- `system_log` contains one `reflect` entry
- link checks for the new reflection summary pass

---

## 4. Idempotency Rules

Repeated runs must:
- avoid creating duplicate reflection files for the same topic/time window
- prefer updating the latest matching reflection summary in place when user asks to “refresh”
- avoid duplicate `master_index` summary-file lines

---

## 5. Non-goals

Do NOT:
- deep-read large RAW notes by default
- force “final truth” conclusions
- resolve all thesis contradictions
- overwrite existing source summaries unless explicitly requested
