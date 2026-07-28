# Agent Capabilities

This system supports the following capabilities.

---

## 1. Document Processing

- Process unprocessed notes in `/00_RAW` and vault root
- Generate structured summaries in `/02_SUMMARY`
- Extract keywords/tags and rough type
- Route source notes into `/00_RAW/<category>/`
- Link source notes to their summaries
- Link summaries to local topic pages
- Maintain `/00_RAW/<category>/_目录.md` category article indexes
- Maintain `/04_TOPIC_MAP` tree pages
- Rewrite moved-path hyperlinks across index/summary/knowledge/project files
- Update retrieval layer in `/01_INDEX/master_index.md`
- Append operation records to `/01_INDEX/system_log.md`
- Run standardized flow via `/03_SYSTEM_GUIDE/skills/organize_articles.md`

---

## 2. Category System Generation

- Generate an initial one-level `/00_RAW/<category>` folder system from a user's own notes
- Refactor an existing vault's category system
- Split oversized categories
- Merge tiny or redundant categories
- Reduce oversized `/00_RAW/其它` buckets
- Preserve stable user-approved categories when possible
- Warn the user that large category analysis may consume many tokens
- Default to proposal/dry-run before moving large batches
- Execute via `/03_SYSTEM_GUIDE/skills/generate_category_system.md`
- Follow `/03_SYSTEM_GUIDE/category_design_rules.md`

---

## 3. Knowledge Retrieval

- Find notes by topic through `master_index`
- Browse from `/README_HUMAN.md` to raw category indexes for human top-down retrieval
- Browse from `/04_TOPIC_MAP/README.md` to theme and local topic pages for topic-level retrieval
- Read summaries first, stop at summary-level by default
- Expand to RAW only when explicitly requested or evidence is insufficient

---

## 4. Reflective Synthesis (举一反三)

- Combine connected summaries into new concept proposals
- Surface actionable TODO items
- Identify overlooked concepts and blind spots
- Suggest feasible next directions with assumptions/risks
- Write outputs as new summary notes in `/02_SUMMARY`
- Execute via `/03_SYSTEM_GUIDE/skills/reflect_synthesis.md`

---

## 5. Knowledge Evolution

- Merge duplicate or overlapping concepts
- Suggest refined summary-level syntheses in `/02_SUMMARY`
- Detect outdated or superseded ideas

---

## 6. System Guidance

- Explain how the system works
- Suggest practical workflows
- Help recover usage patterns
- Guide new or confused users

---

## 7. Efficiency Optimization

- Prefer index + summary over full text
- Avoid scanning the entire vault by default
- Use AI retrieval: `master_index -> summary -> (optional) raw`
- Use human retrieval: `README_HUMAN -> 00_RAW/<category>/_目录.md -> source`
- Use topic retrieval: `04_TOPIC_MAP/README -> theme index -> local topic page -> summary`

---

## 下一篇 [[workflows.md]]
