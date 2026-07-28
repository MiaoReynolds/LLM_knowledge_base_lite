# Knowledge System Guide

This vault is an AI-assisted knowledge operating system.

If you are unsure how to use it, start here.

---

## What this system does

This system helps you:

- Capture ideas with minimal effort
- Organize notes automatically
- Generate summaries and indexes
- Retrieve knowledge efficiently
- Maintain a tree-shaped human browsing system
- Link source notes, summaries, topic category pages, and root indexes
- Perform summary-only reflective synthesis (举一反三)

---

## Core idea

You do NOT need to organize manually.

- You write -> `/00_RAW` (or vault root for quick capture)
- AI routes the note, summarizes it, indexes it, and links it into the tree
- Human quick entry is in `/README_HUMAN.md`
- Category generation is reusable: it can initialize a new vault or refactor an old vault

The main chain is:

- source note -> summary
- summary -> local topic page
- local topic page -> source note
- topic root -> theme index -> local topic page -> summaries + source notes

Humans should be able to browse top-down without asking AI to search every time.
Agents should retrieve through indexes and summaries before reading raw notes.

---

## Folder overview

- `/00_RAW` -> Unified source-note pool
- `/04_TOPIC_MAP/<theme>/<category>.md` -> Direct human-browse article index for that category, with source links and summary links
- `/01_INDEX` -> Metadata and system log
- `/02_SUMMARY` -> AI-generated summaries
- `/03_SYSTEM_GUIDE` -> System manual
- `/04_TOPIC_MAP` -> Tree-shaped topic map over categories, summaries, and source notes
- `/assets` -> Canonical folder for embedded images, PDFs, and other note assets

Category design rules:
- `/03_SYSTEM_GUIDE/category_design_rules.md`
- `/03_SYSTEM_GUIDE/skills/generate_category_system.md`

---

## How to use (simple)

You can ask:

- “整理文章”
- “检索 [topic]”
- “总结 [topic]”
- “反思 / 举一反三”

---

## If you feel lost

Ask:

- “这里能做什么？”
- “这个系统怎么用？”
- “帮我恢复使用方式”

The agent should read this folder and guide you.

---

## First-time setup

If `INIT_BOOTSTRAP.md` exists:

-> The system is not fully initialized
-> Ask the agent to run initialization

Otherwise:

-> The system is already active

---

## 下一篇 [[SYSTEM_RULES.md]]

