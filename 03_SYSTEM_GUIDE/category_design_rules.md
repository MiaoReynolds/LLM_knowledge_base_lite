# Category Design Rules

This file defines how to generate or refactor the `/00_RAW/<category>` folder system.

The category system is not a universal taxonomy.
It is a human-browse retrieval interface generated from the user's own notes.

---

## 1. Purpose

Categories exist to help a human rediscover forgotten areas of knowledge without asking an AI to search from scratch.

Good categories are:
- natural to the user
- broad enough to contain a meaningful cluster
- specific enough to avoid giant "other" buckets
- stable enough for long-term maintenance
- shallow enough to keep `/00_RAW` one-level only

---

## 2. Reusable Operation

Category generation is reusable.

It may be used for:
- first-time vault setup
- importing a large archive
- periodically refactoring an old vault
- splitting oversized categories
- merging tiny or redundant categories
- reducing `/00_RAW/其它` or `/00_RAW/Uncategorized`

Do not call it a one-time initialization.
Do not require the user to delete this rule after setup.

---

## 3. Token And Time Warning

Before running category generation or refactoring, warn the user that:
- scanning many titles and summaries can consume many tokens
- reading raw notes can consume substantially more tokens
- large moves can affect many links
- the safest default is proposal/dry-run first, then apply after approval

Default analysis depth:
1. folder names and note titles
2. existing `/02_SUMMARY` files
3. raw note snippets only when summaries are missing or category evidence is weak

---

## 4. Design Heuristics

Initial category count:
- small vault: 8-15 categories
- medium vault: 15-30 categories
- large vault: 25-60 categories

Sizing rules:
- avoid categories with only 1-2 notes unless they are clearly important recurring domains
- split a category if it is much larger than peer categories and contains clear subclusters
- merge or keep under a broader category if the user would not naturally browse it alone
- catch-all categories should be temporary and should not remain much larger than ordinary categories

Naming rules:
- use names the user would naturally recognize while browsing
- prefer domain/task names over abstract academic taxonomy when the user's retrieval habit is practical
- avoid over-clever names
- preserve user-approved category names unless there is a clear reason to refactor

Structure rules:
- categories are one-level folders under `/00_RAW`
- do not create deeper RAW subfolders by default
- hierarchy belongs in `/04_TOPIC_MAP`, not in `/00_RAW`
- every approved category must have a local topic page under `/04_TOPIC_MAP/<theme>/<category>.md`
- `README_HUMAN.md` should point to local topic pages, not RAW folders or legacy `_目录.md` files

---

## 5. Local Category Profile

Each user vault should keep its own category system in:
- machine-readable: `/01_INDEX/category_profile.json`
- optional human-readable: `/03_SYSTEM_GUIDE/local_rules/category_profile.md`

Open-source templates should not hard-code one user's domains into system scripts.
Tools such as `/03_SYSTEM_GUIDE/tools/build_topic_map.py` must read the local profile first.

Minimum JSON shape:

```json
{
  "profile_version": 1,
  "generated_date": "YYYY-MM-DD",
  "user_approved": true,
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

---

## 6. Proposal Format

Before applying a new or refactored category system, present:
- proposed theme list
- proposed category list
- purpose of each category
- examples of notes that would go there
- estimated note count per category
- categories to split
- categories to merge
- ambiguous or risky moves
- token/time cost warning

Do not move large batches of notes without user approval unless the user explicitly requested automatic execution.

---

## 7. Apply Requirements

After approval:
- create approved `/00_RAW/<category>` folders
- move notes using the approved mapping
- write/update `/01_INDEX/category_profile.json`
- optionally write/update `/03_SYSTEM_GUIDE/local_rules/category_profile.md`
- rewrite affected links
- refresh `/04_TOPIC_MAP`
- refresh source -> summary -> topic links
- rebuild `/01_INDEX/master_index.md` with `/03_SYSTEM_GUIDE/tools/rebuild_master_index.py`
- update `/README_HUMAN.md`
- append `/01_INDEX/system_log.md`
- validate idempotency after the move

The final state must support:
- human tree browsing: `README_HUMAN -> 04_TOPIC_MAP/<theme>/<category>.md -> source`
- topic browsing: `04_TOPIC_MAP -> theme -> local category page -> source + summary`
- AI retrieval: `master_index -> summary -> optional source`

