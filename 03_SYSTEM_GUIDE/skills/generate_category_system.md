# Skill: Generate Or Refactor Category System

This skill standardizes the command family:
- "初始化知识库"
- "生成分类文件夹"
- "根据我的笔记建立分类"
- "重构分类系统"
- "重新设计人眼浏览目录"
- "减少其它目录"
- "拆分过大的分类"
- "合并过碎的分类"

This is a reusable category-system generator.
It is not a one-time initialization file.

---

## 1. Trigger

Run this skill when the user intent is to:
- create an initial `/00_RAW/<category>` folder system for a new vault
- infer categories from imported notes in any user domain or industry
- refactor an existing category system
- split oversized categories
- merge tiny or redundant categories
- redesign the human-browse tree
- make `/README_HUMAN.md` and `/04_TOPIC_MAP` better fit the user's actual notes

Before acting, read:
- `/03_SYSTEM_GUIDE/SYSTEM_RULES.md`
- `/03_SYSTEM_GUIDE/category_design_rules.md`
- `/03_SYSTEM_GUIDE/skills/organize_articles.md`
- `/03_SYSTEM_GUIDE/skills/repair_links.md`

---

## 2. Mandatory User Warning

Before a large category generation or refactor, tell the user:
- this may consume many tokens if many titles, summaries, or raw notes are analyzed
- title + summary analysis is cheaper than raw-note analysis
- moving many notes can affect many links and indexes
- default mode is proposal/dry-run first
- apply mode should happen only after user approval unless the user explicitly requested automatic execution

Use concise language, but do not skip the warning.

---

## 3. Fixed Execution Order

1. Scope discovery
- determine whether this is a new vault, large import, or existing-vault refactor
- count current `/00_RAW` categories and note counts
- count summaries under `/02_SUMMARY`
- identify oversized, tiny, duplicate, stale, and catch-all categories such as `其它` or `Uncategorized`
- exclude legacy `/00_RAW/<category>/_目录.md` files if they exist; these are navigation artifacts, not notes

2. Low-cost analysis
- analyze folder names
- analyze note titles
- analyze existing summary filenames and summary text where available
- use raw-note snippets only when summaries are missing or classification evidence is weak

3. Category proposal
- propose a one-level `/00_RAW/<category>` folder system
- propose a `/04_TOPIC_MAP/<theme>/<category>.md` theme/category hierarchy
- preserve useful existing categories when possible
- propose splits for oversized categories
- propose merges for tiny or redundant categories
- explain ambiguous categories and risky moves
- estimate note counts per category
- explicitly state that the proposal is local to this user's vault and should not be blindly reused by another user

4. User approval
- wait for approval before moving large batches of existing notes
- if the user requests automatic execution, still report the assumed category design before applying

5. Apply category system
- create approved one-level `/00_RAW/<category>` folders
- move notes according to the approved mapping
- do not create deeper RAW subfolders
- write or update `/01_INDEX/category_profile.json`
- optionally write or update `/03_SYSTEM_GUIDE/local_rules/category_profile.md`
- rewrite affected links in `/01_INDEX`, `/02_SUMMARY`, `/README_HUMAN.md`, and `/04_TOPIC_MAP`

6. Rebuild retrieval trees
- run or follow `/03_SYSTEM_GUIDE/tools/build_topic_map.py`
- run or follow `/03_SYSTEM_GUIDE/tools/build_raw_category_indexes.py`
- run or follow `/03_SYSTEM_GUIDE/tools/link_summary_topic_graph.py --apply`
- run or follow `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`

7. Update retrieval and rules
- update `/README_HUMAN.md`
- append `/01_INDEX/system_log.md`
- document the active category profile in `/01_INDEX/category_profile.json`
- do not hard-code the generated category system into generic scripts

8. Validate
- verify every approved `/00_RAW/<category>` has a matching `/04_TOPIC_MAP/<theme>/<category>.md`
- verify `README_HUMAN.md` points to `/04_TOPIC_MAP/<theme>/<category>.md` pages
- verify source-summary-topic graph is idempotent
- verify `master_index.md` uses the fixed five-column schema
- verify affected links resolve or list residual failures
- report remaining uncategorized or summary-missing notes

---

## 4. Category Profile Output

For reusable deployments, the generated category system must be documented as a local category profile.

Required machine-readable location:
- `/01_INDEX/category_profile.json`

Optional human-readable location:
- `/03_SYSTEM_GUIDE/local_rules/category_profile.md`

Minimum JSON shape:

```json
{
  "profile_version": 1,
  "generated_date": "YYYY-MM-DD",
  "generated_by": "AI agent or user",
  "user_approved": true,
  "source_basis": "titles / summaries / raw snippets / mixed",
  "themes": [
    {
      "theme": "Theme name",
      "categories": [
        {
          "category": "Category name",
          "description": "Use-for guidance."
        }
      ]
    }
  ]
}
```

Open-source templates may keep only the template file.
User vaults should generate their own profile from their own notes.

---

## 5. Definition Of Done

A category-generation or refactor run is complete only when:
- the user has seen the token/time warning
- a category proposal or approved automatic assumption has been documented
- `/00_RAW` contains only approved one-level category folders
- `/01_INDEX/category_profile.json` exists and matches the active category system
- `/README_HUMAN.md` points to `/04_TOPIC_MAP/<theme>/<category>.md` category pages
- `/04_TOPIC_MAP` reflects the category profile
- source notes link to summaries when summaries exist
- summaries link to local topic pages when source categories are known
- `master_index` is rebuilt by `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`
- `system_log` records the operation

---

## 6. Idempotency And Safety

Repeated runs must:
- not duplicate category profile entries
- not duplicate source-summary-topic links
- not reclassify stable categories without evidence
- not move large batches without approval
- not treat legacy `_目录.md` files as raw notes
- not hard-code one user's category profile into generic tools
- preserve original source-note content

When uncertain:
- produce a proposal and residual ambiguity list
- ask for approval before applying high-impact moves

