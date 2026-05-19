# Agent Capabilities

This system supports the following capabilities.

---

## 1. Document Processing

- Process unprocessed notes in `/00_RAW` and vault root
- Generate structured summaries in `/02_SUMMARY`
- Extract keywords/tags and rough type
- Route source notes into `/00_RAW/<category>/`
- Rewrite moved-path hyperlinks across index/summary/knowledge/project files
- Update retrieval layer in `/01_INDEX/master_index.md`
- Append operation records to `/01_INDEX/system_log.md`
- Run standardized flow via `/03_SYSTEM_GUIDE/skills/organize_articles.md`

---

## 2. Knowledge Retrieval

- Find notes by topic through `master_index`
- Read summaries first, stop at summary-level by default
- Expand to RAW only when explicitly requested or evidence is insufficient

---

## 3. Reflective Synthesis (举一反三)

- Combine connected summaries into new concept proposals
- Surface actionable TODO items
- Identify overlooked concepts and blind spots
- Suggest feasible next directions with assumptions/risks
- Write outputs as new summary notes in `/02_SUMMARY`
- Execute via `/03_SYSTEM_GUIDE/skills/reflect_synthesis.md`

---

## 4. Knowledge Evolution

- Merge duplicate or overlapping concepts
- Suggest refined summary-level syntheses in `/02_SUMMARY`
- Detect outdated or superseded ideas

---

## 5. System Guidance

- Explain how the system works
- Suggest practical workflows
- Help recover usage patterns
- Guide new or confused users

---

## 6. Efficiency Optimization

- Prefer index + summary over full text
- Avoid scanning the entire vault by default
- Use: `master_index -> summary -> (optional) raw`

---

## 下一篇 [[workflows.md]]
