# SYSTEM RULES

This file defines how the AI agent should operate this knowledge system.

This is NOT a description.
This is a behavioral contract.

---

# 0. System Identity

This vault is a human + AI knowledge operating system.

- Human = low-friction input
- AI = structure, retrieval, summarization, linking, prioritization, refinement

The purpose of the system is NOT to create perfect folders.
The purpose is to create a long-term, searchable, recoverable, evolving knowledge system.

Do NOT treat this vault as a static archive.
Do NOT treat this vault as a generic file tree.

The current design goal is dual retrieval:
- human retrieval should work as a tree that can be browsed top-down without AI help
- AI retrieval should work through index and summary layers before reading source notes
- the graph should avoid a few giant hubs by distributing links through category indexes and topic pages

---

# 1. Architectural Separation

This system has two major layers:

## 1.1 Knowledge Layer
This contains the user's actual content, notes, summaries, projects, and long-term knowledge.

Examples:
- `/00_RAW`
- `/01_INDEX`
- `/02_SUMMARY`

## 1.2 Agent Behavior Layer
This contains the rules, guidance, workflows, and usage recovery logic that govern how the AI should operate.

Examples:
- `/README.md`
- `/03_SYSTEM_GUIDE/README.md`
- `/03_SYSTEM_GUIDE/SYSTEM_RULES.md`
- `/03_SYSTEM_GUIDE/capabilities.md`
- `/03_SYSTEM_GUIDE/workflows.md`
- `/03_SYSTEM_GUIDE/Design Principles.md`
- `/03_SYSTEM_GUIDE/Quick Commands.md`
- `/03_SYSTEM_GUIDE/skills/organize_articles.md`

Rule:
- Do NOT mix knowledge content with behavior rules unnecessarily.
- Do NOT store operational instructions inside normal knowledge notes unless explicitly intended.

## 1.3 Retrieval Architecture

This vault has three coordinated retrieval paths:

1. Human browse tree
- `/README_HUMAN.md`
- `/04_TOPIC_MAP/<theme>/<category>.md`
- `/00_RAW/<category>/<source note>`

2. Topic map tree
- `/04_TOPIC_MAP/README.md`
- `/04_TOPIC_MAP/<theme>/index.md`
- `/04_TOPIC_MAP/<theme>/<category>.md` as the canonical category directory
- `/02_SUMMARY/<note>.summary.md`
- `/00_RAW/<category>/<source note>`

3. AI quick retrieval
- `/01_INDEX/master_index.md`
- `/02_SUMMARY/<note>.summary.md`
- `/00_RAW/<category>/<source note>` only when summary evidence is insufficient

Rule:
- keep these three retrieval paths synchronized after every ingest, move, summary refresh, or link repair.
- the source note is the evidence layer, not the default browsing layer.
- the summary is the semantic middle layer between raw source material and tree indexes.

---

# 2. Core Folder Roles

The system is layered:

- `/00_RAW` → unified source-note pool (new notes + processed notes)
- `/` (vault root, excluding `/README.md`) → may contain newly added unprocessed notes
- `/01_INDEX` → metadata, master index, system log
- `/02_SUMMARY` → compressed representations of notes
- `/03_SYSTEM_GUIDE` → system operating manual and behavioral rules
- `/04_TOPIC_MAP` → tree-shaped topic directory for human and AI top-down retrieval
- `/assets` → canonical attachment folder for images, PDFs, canvas files, and other embedded note assets

Complexity belongs to:
- indexes
- summaries
- metadata
- system log

Complexity does NOT belong to:
- deep folder nesting
- rigid manual classification
- fragile directory logic

`/00_RAW` organization rule:
- allow one-level category subfolders under `/00_RAW`
- keep structure shallow (no deep nested taxonomy)
- folder names are also a human browse system, not only machine routing labels
- do not create `_目录.md` pages inside `/00_RAW/<category>`; local topic pages in `/04_TOPIC_MAP/<theme>/<category>.md` are the direct human-browse article indexes
- if legacy `_目录.md` files exist, treat them as obsolete navigation metadata, not source articles

Attachment rule:
- use `/assets` as the canonical attachment directory.
- do not create new top-level attachment folders such as `/Attachment`, `/Attachments`, `/images`, or `/files`.
- when importing or repairing notes, rewrite old attachment paths such as `Attachment/...` or `Attachments/...` to `assets/...`.
- attachment files are evidence/supporting media, not source notes; do not summarize or classify them as articles.

---

# 3. Entry Rule (Critical)

When operating this system:

1. Start from `/README.md` if present
2. Then read `/03_SYSTEM_GUIDE/README.md`
3. Then read this file (`SYSTEM_RULES.md`)
4. If user-facing operation is involved, consult `/README_HUMAN.md` as the human entry page
5. Do NOT scan the entire vault by default

Use layered access instead.

---

# 4. Memory Model

The system should operate with three memory layers:

## 4.1 Brain (Long-Term Knowledge)
This is the persistent knowledge layer.

Includes:
- summaries
- master index
- knowledge notes
- project history
- processed source material

Purpose:
- preserve what the user has written, learned, decided, and developed over time

## 4.2 Operational Memory (Short-/Mid-Term Attention)
This is the current attention layer, maintained purely chronologically.

Includes:
- `system_log.md` (append-only history of actions)

Purpose:
- help the agent stay context-aware by reading recent history
- prevent the agent from acting like it is starting from zero every time

## 4.3 Session Context
This is the current task or conversation context.

Purpose:
- handle the immediate request
- coordinate with long-term knowledge and operational memory

Rule:
- Do NOT confuse session context with long-term truth.
- Do NOT confuse short-term focus with permanent classification.

---

# 5. Read-Before-Answer Rule (Critical)

Before answering substantive questions, the agent should consult the system's knowledge layers.

Preferred order:

1. top-down tree indexes when the user is browsing by area:
   - `/README_HUMAN.md`
   - `/04_TOPIC_MAP/README.md`
   - `/04_TOPIC_MAP/<theme>/<category>.md` as the category directory
   - `/04_TOPIC_MAP/<theme>/<category>.md`
2. `/01_INDEX/master_index.md` for candidate narrowing + summary mapping
3. corresponding files in `/02_SUMMARY`
4. source notes in `/00_RAW/<category>` only when explicitly requested or summary-level evidence is insufficient
5. newly added notes in vault root (`/`, excluding `/README.md`) if relevant
6. uncataloged raw notes only if explicitly necessary

Rule:
- Do NOT answer from scratch if relevant internal knowledge exists.
- Do NOT default to memory-only behavior when the vault should be consulted.
- For normal retrieval tasks, default stop depth is summary-level; do NOT drill into raw notes unless needed.
- For human-browse or topic-overview requests, prefer tree indexes first instead of scanning many raw notes.

This system should behave as:
→ consult brain first, then answer

not:
→ improvise first, then forget

---

# 6. Write-Back Rule (Critical)

When meaningful new information appears, it should be written back into the system in the appropriate form.

Possible write-back targets include:
- summary updates
- index updates
- system log appends
- summary-level synthesis refinements

Examples of meaningful new information:
- new project direction
- clarified definition
- correction of an earlier interpretation
- important strategic shift
- repeated theme emerging across notes
- confirmed resolution of an open question

Rule:
- Valuable new information should not remain trapped only inside a single chat session.
- The system should compound over time.

---

# 7. Correction Priority Rule

User corrections are high-value signals.

When the user corrects:
- a factual statement
- a project status
- a definition
- a preference
- a structural interpretation
- a priority judgment

the correction should be treated as important update material.

Rule:
- prioritize updating the relevant summary, index, knowledge note, or operational memory
- do NOT leave corrections only inside ephemeral dialogue
- do NOT let outdated interpretations remain dominant if they have been clearly superseded

---

# 8. Note Processing Lifecycle (Critical)

`/00_RAW` is the unified source-note pool.
Vault root (`/`) may also contain newly added unprocessed notes (excluding `/README.md`).

Status is determined by system artifacts (not by title suffix):
- processed → summary exists + index entry exists + path is routed into `/00_RAW/<category>/`
- unprocessed → missing summary/index and/or still waiting for proper routing

Compatibility note:
- legacy suffixes like `-已处理` may exist historically
- do NOT require suffix changes for new processing

---

## 8.1 Processing Requirements

For each unprocessed note:

- assign a `/00_RAW` category folder per section 8.7
- move processed source note to the corresponding `/00_RAW/<category>/` path
- generate summary → `/02_SUMMARY`
- extract tags / keywords
- rebuild `/01_INDEX/master_index.md` with `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`
- append ingest action to `/01_INDEX/system_log.md`
- detect project linkage if relevant
- estimate long-term value
- link the source note to its summary
- link the summary to its local topic page
- refresh topic-map category pages, README_HUMAN, and master indexes

Discovery rule:
- when processing unprocessed notes, check both `/00_RAW` and vault root (`/`, excluding `/README.md`)
- exclude legacy navigation files such as `/00_RAW/<category>/_目录.md` from processing candidates if they exist

---

## 8.2 Completion Condition

A note is considered "processed" when:

- summary exists
- index entry exists
- tags are assigned
- generated notes include source and related-article links per section 8.5
- source note is routed into exactly one `/00_RAW/<category>/`
- source note links to its summary when it is a Markdown note
- summary links to the correct local topic page
- `/04_TOPIC_MAP`, `/README_HUMAN.md`, and `/01_INDEX/master_index.md` are refreshed

---

## 8.3 Mandatory Routing Update Rule

After processing:

→ move the source note into the corresponding `/00_RAW/<category>/` folder
→ if source note is in vault root (`/`), move it into `/00_RAW/<category>/` after processing
→ rewrite impacted links to the new real path

Do NOT leave a completed note outside the `/00_RAW/<category>/` structure.

---

## 8.4 Unprocessed Visibility Rule

During normal retrieval:

→ prioritize notes that already have index + summary
→ ignore uncataloged raw notes by default

Unless:
- explicitly requested
- processing is being performed
- initialization is underway

---

## 8.5 Related-Article Linking Rule (Critical)

After processing each new note, the system must enforce link-aware write-back for generated notes.

Scope:
- applies to newly generated notes after summarization (especially in `/02_SUMMARY`)

Mandatory output format:
- links must be placed at the end of the note
- section title must be exactly: `## 相关文章`

The `相关文章` section must include:
- one explicit source link to the original note in `/00_RAW`
- related note links selected using `/01_INDEX` and `/02_SUMMARY`

Linking behavior:
- the source note should link back to its own summary using a `Summary:` link when the source is a Markdown file
- the summary should link upward to exactly one local topic page using a `Topic:` link
- the local topic page should link upward to its theme index and downward to source notes plus summary links/previews
- the local topic page is the direct human-browse category directory and should link downward to source notes
- for each newly added note, create bidirectional links with strongly related notes where practical
- relation selection should prioritize high-relevance links first, then adjacent links
- avoid noisy over-linking; keep links meaningful and compact

Path rule:
- generated-note references should point to the current real path of the source note
- after moving a note, update existing links that reference the old path to the new path
- link updates apply at least to `/01_INDEX`, `/02_SUMMARY`, `/README_HUMAN.md`, and `/04_TOPIC_MAP`
- after path or category changes, run or follow:
  - `/03_SYSTEM_GUIDE/tools/build_raw_category_indexes.py`
  - `/03_SYSTEM_GUIDE/tools/build_topic_map.py`
  - `/03_SYSTEM_GUIDE/tools/link_summary_topic_graph.py --apply`

---

## 8.6 Orphan Summary Cleanup Rule

If a source note is manually deleted from the vault, its summary in `/02_SUMMARY` must not remain as an orphan.

Detection basis:
- read the `- Original: ...` path in each summary file
- if the source path no longer exists, mark that summary as orphan

Cleanup behavior:
- support batch detection (dry-run) and batch deletion (apply mode)
- default script path:
  - `/03_SYSTEM_GUIDE/tools/cleanup_orphan_summaries.sh`
- command examples:
  - dry-run: `bash ./03_SYSTEM_GUIDE/tools/cleanup_orphan_summaries.sh --dry-run`
  - apply: `bash ./03_SYSTEM_GUIDE/tools/cleanup_orphan_summaries.sh --apply`

Rule:
- orphan summaries should be removed in batch during maintenance runs
- do not remove summaries whose source still exists

---

## 8.7 RAW Category Routing Rule (Critical)

After a note is processed, route it into exactly one valid category folder under `/00_RAW`.

Valid category folders include:
- existing one-level subfolders already present under `/00_RAW`
- any new one-level subfolder manually created by the user under `/00_RAW`

Routing constraints:
- use one-level classification only (do not create deeper subfolders by default)
- the agent should discover available category folders from the current `/00_RAW` directory state at runtime
- user-created one-level folders under `/00_RAW` are immediately valid routing targets and do NOT require manual updates to rule files
- if category is unclear, use `/00_RAW/其它`
- do not create new category folders automatically unless explicitly approved by user
- if a note clearly belongs to a different category later, move it and rewrite links to the new path

### 8.7.1 Human Browse Category Rule

The `/00_RAW` folder system is intentionally used for human visual retrieval, but the category names are local to each user's vault.
Do not treat this repository author's categories as a universal taxonomy.

Local category authority:
- primary machine-readable profile: `/01_INDEX/category_profile.json`
- optional human-readable profile: `/03_SYSTEM_GUIDE/local_rules/category_profile.md`
- template only: `/03_SYSTEM_GUIDE/local_rules/category_profile.template.md`

Routing rules:
- when routing new notes, first read the active local category profile if it exists.
- if no local profile exists, infer provisional categories from existing one-level `/00_RAW` folders and the user's notes, then propose a profile before large moves.
- prefer a specific local human-browse category over a broad bucket whenever title/summary evidence is clear.
- if category is unclear, use the local catch-all category if one exists; otherwise use `/00_RAW/其它` or `/00_RAW/Uncategorized` and flag it for later refactor.
- preserve user-approved local category names unless there is clear evidence and user approval for a refactor.

Routing priority:
- Do not blindly reuse another user's category profile.
- Once a note is already inside a user-approved human-browse category, do not automatically move it during ordinary ingest; only do so when the user explicitly asks for reclassification or refactor.
- Avoid broad substring matches for short technical tokens; treat them as standalone terms and use summary/title evidence.
- If a note fits multiple categories, use the folder that best matches the user's likely manual retrieval intent.
- Do not create deeper subfolders automatically. Add a new one-level browse category only when the user approves it.

---
## 8.8 Category System Generation And Refactor Rule (Critical)

Category generation is a reusable operation, not a one-time initialization step.

It can be used for:
- first-time vault setup
- large note imports
- refactoring an existing vault
- splitting oversized folders
- merging tiny or redundant folders
- reducing `/00_RAW/其它`
- adapting an open-source template to a user's own knowledge distribution

Rule source:
- follow `/03_SYSTEM_GUIDE/category_design_rules.md`
- follow `/03_SYSTEM_GUIDE/skills/generate_category_system.md`

Mandatory warning:
- before category generation or refactor, warn the user that analyzing many titles, summaries, or raw notes may consume many tokens.
- explain that title + summary analysis is cheaper than raw-note analysis.
- explain that moving many notes can affect many links.

Default safety mode:
- produce a proposal/dry-run first.
- do not move large batches of existing notes until the user approves the proposed category system.
- if the user explicitly requests automatic execution, still document the assumed category design and residual ambiguities.

Design constraints:
- infer categories from the user's actual notes and retrieval needs.
- do not blindly reuse another user's category profile.
- keep `/00_RAW` one-level only.
- put hierarchy in `/04_TOPIC_MAP`, not in deeper RAW folders.
- every approved category must have `/04_TOPIC_MAP/<theme>/<category>.md` as its canonical category directory.
- do not create `/00_RAW/<category>/_目录.md`; if legacy copies exist, they are obsolete navigation pages, not raw notes.

After applying a generated or refactored category system:
- refresh `/04_TOPIC_MAP`, including local category pages with direct source links and summary links/previews.
- refresh source -> summary -> topic links.
- update `/README_HUMAN.md`.
- rebuild `/01_INDEX/master_index.md` with `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`.
- append `/01_INDEX/system_log.md`.

---

## 8.9 README_HUMAN Maintenance Rule (Critical)

`/README_HUMAN.md` is the mandatory human-readable entry page.

Maintenance triggers:
- processing new notes
- moving notes between paths
- restructuring categories
- generating/refactoring a category system
- repairing links

Required actions:
- update the section `## 文章更新目录（最新在前）`
- keep the section `## 当前人眼浏览目录` pointed at `/04_TOPIC_MAP/<theme>/<category>.md` category pages
- append latest source-note links at the top (latest-first)
- use fixed line format for source-note update entries: `- YYYY-MM-DD｜[[relative/path.ext]]` (`.md` or `.canvas`)

Consistency constraints:
- every newly processed article must appear in the latest-update directory
- if a note path changes, update its entry path in this directory
- every current `/00_RAW` category should be reachable from `README_HUMAN.md` through its local topic page under `/04_TOPIC_MAP`
- do NOT point `README_HUMAN.md` at obsolete `/00_RAW/<category>/_目录.md` pages
- do NOT leave `README_HUMAN.md` stale after operational updates

---

## 8.10 Topic Map Maintenance Rule (Critical)

`/04_TOPIC_MAP` is the mandatory human-browse and AI topic-map layer.
It exists to prevent the graph from becoming a few giant folder/index hubs while preserving fast top-down browsing.

Canonical graph chain:
- `README_HUMAN.md` -> local topic page
- `/04_TOPIC_MAP/README.md` -> theme index
- theme index -> local topic page
- local topic page -> source note and summary note
- source note -> summary note
- summary note -> local topic page

Directory layout:
- `/04_TOPIC_MAP/README.md` is the root topic directory.
- `/04_TOPIC_MAP/<theme>/index.md` is a major-theme directory.
- `/04_TOPIC_MAP/<theme>/<category>.md` is the canonical category directory mapped to one `/00_RAW/<category>` folder.
- `/00_RAW/<category>` stores source notes only; it should not need a generated `_目录.md` page.

Maintenance triggers:
- processing new notes
- creating or updating summaries
- adding/removing categories
- moving notes between categories
- restructuring/refactoring the category system

Required actions:
- each local topic page must list direct source-note links for the mapped category so humans can browse without opening Summary files first.
- each local topic page should also list the matching summary link and, when practical, a compact summary preview for each source note.
- source `.md` notes should link to their own summary using a `Summary:` link.
- each summary should link to exactly one local topic page using a `Topic:` link when the source category is known.
- each theme index should link to its local topic pages.
- `/04_TOPIC_MAP/README.md` should link to the theme indexes.
- `README_HUMAN.md` should link to `/04_TOPIC_MAP/<theme>/<category>.md` pages.
- run or follow `/03_SYSTEM_GUIDE/tools/build_topic_map.py` after category or summary changes.
- run or follow `/03_SYSTEM_GUIDE/tools/build_raw_category_indexes.py` after moving notes or creating categories; despite its legacy name, this script only refreshes `README_HUMAN` topic links and must not create RAW `_目录.md` pages.
- then run or follow `/03_SYSTEM_GUIDE/tools/link_summary_topic_graph.py --apply` to repair source -> summary -> local-topic links.
- if `link_summary_topic_graph.py` reports same-title source notes in multiple categories, keep one stable primary `Topic:` on the shared summary instead of repeatedly flipping it between categories.

Graph hygiene constraints:
- do not make `/04_TOPIC_MAP/README.md` link directly to hundreds or thousands of source notes.
- do not make theme index pages link directly to raw source-note lists by default.
- local topic pages may link directly to source notes because they are bounded by category and serve as the real human directory.
- summaries remain the semantic middle layer for AI retrieval; do not delete summary files merely because `master_index` also contains summary text.
- preserve the one-level `/00_RAW` folder rule; topic hierarchy lives in `/04_TOPIC_MAP`, not as deeper raw-note folders.
- obsolete `_目录.md` files are navigation pages, not source articles; do not summarize, move, classify, or count them as raw notes.
- if a category has no summary yet, list missing summaries on the local topic page and create summaries during normal ingest.

Idempotency:
- repeated maintenance must not duplicate `Summary:` or `Topic:` links.
- repeated maintenance must not recreate RAW `_目录.md` pages.
- generated topic pages may be overwritten by the topic-map builder.

---

## 8.11 Master Index Fixed-Schema Rule (Critical)

`/01_INDEX/master_index.md` is a generated quick retrieval index, not a free-form scratchpad.

Canonical maintenance command:
- run or follow `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`

Required structure:
- `# Master Index`
- `Last updated: YYYY-MM-DD`
- `## Retrieval Contract`
- `## Table Schema`
- `## Processed Notes`
- exactly one Markdown table under `## Processed Notes`

The `Processed Notes` table has exactly five columns, in this exact order:
- `Note`
- `Location`
- `Type`
- `Summary`
- `Status`

Column rules:
- `Note`: source title, never empty; use the source filename without extension.
- `Location`: source path only, always `/00_RAW/<category>/<filename>.md` or `.canvas`.
- `Type`: short semantic type tag only, such as `technical-note/fuel-cell`; never put a path here.
- `Summary`: one compact summary sentence from `/02_SUMMARY`; use `(missing summary)` only when no summary exists.
- `Status`: controlled value such as `processed + summarized`, `processed + summary-needs-description`, or `source-only / missing-summary`.

Hard prohibitions:
- do NOT add a sixth column.
- do NOT leave `Note` empty.
- do NOT put article titles in `Location`.
- do NOT put paths in `Type`.
- do NOT put type tags in `Summary`.
- do NOT put summary text in `Status`.
- do NOT append raw `/02_SUMMARY` file lists.
- do NOT create `## Summary Files` as a long-term section.
- do NOT append free-form notes, half table rows, or `|- /02_SUMMARY/...` fragments below the table.

After any ingest, move, summary refresh, category refactor, or link repair:
- rebuild `/01_INDEX/master_index.md` with `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`.
- then verify the table has exactly five columns, no empty `Note` cells, and no `## Summary Files` section.

---

## 8.12 "整理文章" Skill Contract (Critical)

When the user asks commands such as:
- “整理文章”
- “整理新文章”
- “处理未整理笔记”
- “更新索引”

the agent should follow:
- `/03_SYSTEM_GUIDE/skills/organize_articles.md`

Skill requirements:
- deterministic step order
- explicit Definition of Done
- idempotent behavior (safe on repeated runs)
- post-run integrity checks

Validation helper:
- `/03_SYSTEM_GUIDE/tools/validate_organize_articles.sh`

---

## 8.13 Re-processing Rule

Processed articles (with existing summaries and indexes) should generally NOT be processed again via the standard `organize_articles` skill.

However, if a user updates an existing article and explicitly asks to refresh its summary/index, you must use the specific re-organize skill:
- `/03_SYSTEM_GUIDE/skills/reorganize_article.md`

This skill enforces in-place updates and prevents duplicate files.

---

## 8.14 "修复链接" Skill Contract (Critical)

When the user asks commands such as:
- “修复链接”
- “修复 RAW 和 Summary 对应关系”
- “检查并修复双向链接”

the agent should follow:
- `/03_SYSTEM_GUIDE/skills/repair_links.md`

Skill boundary:
- scope is structural integrity only (source-summary mapping, path consistency, bidirectional links)
- do NOT resolve thesis-level contradictions or final-conclusion conflicts

---

## 8.14 "反思 / 举一反三" Skill Contract (Critical)

When the user asks commands such as:
- “反思”
- “举一反三”
- “从已有概念提出新概念”
- “基于已有 summary 生成新方向”
the agent should follow:
- `/03_SYSTEM_GUIDE/skills/reflect_synthesis.md`

Skill boundary:
- summary-first and summary-only by default: read `/01_INDEX/master_index.md` + selected `/02_SUMMARY` files
- do NOT read `/00_RAW` unless user explicitly asks for raw-level verification
- output should be a new synthesis summary in `/02_SUMMARY`
- rebuild `/01_INDEX/master_index.md` with `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`; do not append a `## Summary Files` list
- append one `reflect` operation record into `/01_INDEX/system_log.md`

---

# 9. Processing Strategy

When processing notes:

## 9.1 Preserve Original Content
- Do NOT overwrite original note content unless explicitly requested
- Do NOT impose unnecessary formatting on original input

## 9.2 Structural Enhancement
Instead:
- create summary
- create metadata
- create relation hints
- update retrieval layers

## 9.3 Type Detection
Infer rough note type where useful:
- idea
- knowledge
- project
- log
- question

Do NOT require manual classification before capture.

---

# 10. Retrieval Strategy (Critical)

Do NOT read the whole vault by default.

Use layered retrieval:

1. `/01_INDEX/master_index.md`
2. `/02_SUMMARY` (read first; default stopping depth)
3. full notes only if needed and only after summary-level pass

---

## 10.1 Efficiency Principle

Always minimize:
- token usage
- unnecessary reads
- repeated processing
- noisy retrieval

---

## 10.2 Candidate Narrowing

Before reading full text:
- identify likely candidates
- rank them
- read only the most relevant items first

---

# 11. Index Layer Responsibilities

`/01_INDEX` should maintain the system's machine-usable retrieval layer.

It should include or support:
- master index
- system log
- note status
- path tracking where useful

Rule:
- index and summary are primary retrieval interfaces
- full text is secondary

---

# 12. System Log Rule (Chronological Memory)

Maintain:
- `system_log.md`

Purpose:
- Provide an objective, chronological history of AI actions.
- Improve continuity without guessing subjective focus.

Constraint:
- Do NOT maintain subjective or brittle "attention state" files. Read recent logs instead.

## 12.1 Storage Contract (Critical)

System history has a single source of truth:
- `/01_INDEX/system_log.md`

Rules:
- Append every significant action (ingest, lint, query synthesis, etc.) to the top or bottom of `system_log.md`.
- Format: `## [YYYY-MM-DD] action_name | Target Name`
- Do NOT rewrite or overwrite historical entries. It is append-only.

---

# 13. Summary-Centric Knowledge Rule

The system now uses `/02_SUMMARY` as the primary distilled layer.

Rule:
- keep reusable ideas, synthesis notes, project-status abstractions, and framework-level distillations in summary form
- avoid creating parallel knowledge/project/archive folders unless explicitly reintroduced by user decision

---

# 14. Synthesis Page Rule (Important)

For important themes, major questions, or long-running projects, prefer a two-layer page structure:

## 14.1 Current Synthesis
Top section should describe the current best understanding.

Possible contents:
- current conclusion
- current model
- current state
- current framing
- current uncertainties

## 14.2 Timeline / Evidence Layer
Lower section should track:
- important updates
- dated changes
- historical developments
- evidence trail
- decision evolution

Purpose:
- preserve current clarity without losing history
- allow future reinterpretation
- avoid mixing stale history into current understanding

Use this pattern especially for:
- major projects
- evolving frameworks
- recurring strategic questions
- core themes

Do NOT force this structure on every note.
Use it selectively where it provides strong value.

---

# 15. Project and Archive Consolidation Rule

Project tracking and cold-history abstractions should be written as summary notes in `/02_SUMMARY`, with source evidence linked back to `/00_RAW`.

Rule:
- preserve project continuity through summary updates and system log entries
- keep retrieval centered on `master_index -> /02_SUMMARY`

---

# 17. Template Usage

Templates are:
- optional
- minimal
- assistive

Rule:
- do NOT require template usage before note capture
- AI may infer or impose light structure later if useful
- templates should reduce friction, not increase it

---

# 18. Folder Philosophy

Folders should remain:
- shallow
- stable
- human-readable

Folders should provide:
- coarse navigation
- intuitive browsing

Precision should live in:
- metadata
- summaries
- synthesis pages
- system log

Rule:
- do NOT overfit knowledge structure to folders
- do NOT build a heavy MECE-only entity encyclopedia unless explicitly intended

This system is not primarily:
- a CRM
- an entity directory
- a rigid taxonomy engine

It is primarily:
- a hybrid thinking system
- a project system
- a long-term reflective knowledge system

---

# 19. System Guidance Behavior

If the user asks:
- “what can we do here?”
- “how does this system work?”
- “I’m lost”
- “how should I use this?”

then:
- consult `/03_SYSTEM_GUIDE`
- explain available actions
- help recover usage patterns
- give practical next-step suggestions

---

# 20. Recovery Principle

Assume:
- the user may forget the structure
- the user’s habits may drift
- the system may go unused for long periods
- future agents may start without prior context

Therefore the system must remain:
- self-explanatory
- bootable
- recoverable
- interpretable

---

# 21. Anti-Patterns (Must Avoid)

Do NOT:
- scan the entire vault by default
- treat raw as long-term storage
- reprocess already processed notes (unless explicitly using the reorganize_article skill)
- duplicate summaries repeatedly
- over-classify into fragile folders
- force every note into a heavy entity hierarchy
- leave important corrections trapped only in chat
- leave valuable new knowledge unwritten back into the system

---

# 22. Long-Term Principle

This system must remain:

- evolving
- layered
- efficient
- recoverable
- reconstructible

Indexes, summaries, and logs may be rebuilt.
Original notes remain the ultimate source material.
Distilled knowledge remains the long-term cognitive asset.

---

# 23. Final Rule

Always prioritize:

- clarity
- continuity
- efficiency
- stability
- recoverability
- compounding knowledge value

over:

- perfection
- over-structuring
- rigid taxonomy
- unnecessary complexity

---

## 下一篇
[[capabilities.md]]






