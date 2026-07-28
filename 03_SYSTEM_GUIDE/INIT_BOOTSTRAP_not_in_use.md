# INIT_BOOTSTRAP

You are now initializing this Obsidian-based AI-managed knowledge system for first-time operation.

This file is a one-time bootstrap instruction set.
Your task is not to answer casually, but to help set up the long-term operating structure of this vault.

After initialization, future operations should follow `/03_SYSTEM_GUIDE/SYSTEM_RULES.md`.
The user may manually delete this file after successful initialization.

---

## 1. Purpose of this system

This vault is designed as a long-term human + AI knowledge system.

Core principles:

- The human should only need to add new content into `/00_RAW` with minimal friction.
- AI should take over organization, indexing, summarization, and retrieval support.
- Folder structure should remain simple and human-readable.
- Complexity should live in indexes, summaries, metadata, and relation layers.
- The system must remain usable even if the user forgets its structure years later.
- Retrieval efficiency and token efficiency matter.
- Do not rely on full-vault reading by default.
- Prefer layered retrieval: index → summary → original text.

---

## 2. Required folder roles

Interpret the vault using the following folder meanings:

- `/00_RAW`  
  Inbox for newly added, unprocessed notes.

- `/01_INDEX`  
  Machine-friendly indexes, metadata, relation maps, attention state, and retrieval support files.

- `/02_SUMMARY`  
  AI-generated compressed summaries for notes.

- `/02_SUMMARY`  
  Distilled long-term knowledge notes.  
  Only stable or reusable ideas should go here.

- `/02_SUMMARY`  
  Dynamic project-based materials.

- `/02_SUMMARY`  
  Low-priority, old, inactive, or cold documents.

- `/03_SYSTEM_GUIDE`  
  System operating manual, usage recovery guide, and command layer.

---

## 3. Initialization goals

During first-time setup, do the following as far as the current environment permits:

### A. Validate or create the operational structure
Ensure the following files exist or are proposed:

- `/03_SYSTEM_GUIDE/README.md`
- `/03_SYSTEM_GUIDE/capabilities.md`
- `/03_SYSTEM_GUIDE/workflows.md`
- `/03_SYSTEM_GUIDE/design_principles.md`
- `/03_SYSTEM_GUIDE/quick_commands.md`
- `/03_SYSTEM_GUIDE/SYSTEM_RULES.md`

### B. Create or propose index-layer foundations
Inside `/01_INDEX`, establish or propose:

- `master_index`
- `tag_index`
- `relation_map`
- `attention_state/current_focus`
- `attention_state/open_loops`
- `attention_state/weekly_focus`

### C. Process existing unprocessed notes if requested
When handling notes from `/00_RAW` or other unprocessed areas:

For each note, aim to produce:
- a concise summary
- keywords/tags
- rough type classification
- relation hints
- project linkage if obvious
- long-term knowledge value estimate

### D. Preserve human legibility
Do not create overly deep or fragile folder trees.
Prefer simple, stable, intuitive top-level organization.

### E. Preserve long-term recoverability
Assume the user may forget how the system works in the future.
Therefore system guide files must be self-explanatory.

---

## 4. Document handling rules during initialization

When encountering notes, apply the following logic:

### Type 1: Raw / temporary / unprocessed input
- Keep original note intact.
- Generate summary and index entries.
- Do not over-edit original content unless explicitly asked.

### Type 2: Stable reusable knowledge
- Suggest or place a distilled version under `/02_SUMMARY`.

### Type 3: Project-specific note
- Suggest or place under `/02_SUMMARY`.

### Type 4: Old inactive note
- Keep retrievable.
- Consider archive status without destroying access.

Do not force every note into exactly one conceptual category.
Use index/summary/relation layers to carry complexity.

---

## 5. Retrieval philosophy

This system should not depend on reading the whole vault for every question.

Preferred retrieval order:

1. Read index and metadata first
2. Narrow candidate notes
3. Read summaries
4. Only then read original note bodies if needed

The system should optimize for:
- token efficiency
- fast recall
- long-term maintainability
- tolerance for thousands of notes

---

## 6. Attention-state setup

This system should maintain a short-/mid-term attention layer so that future agent behavior is not context-blind.

Please establish or propose:

### `current_focus`
Should track:
- active themes
- active projects
- rising interests
- deprioritized areas
- recent keywords
- recent documents
- unresolved questions
- time window

### `open_loops`
Should track unresolved or recurring problems, decisions, and ongoing pursuits.

### `weekly_focus`
Should periodically summarize:
- what the user has recently focused on
- what new directions are emerging
- what older directions are cooling down

This attention layer must influence prioritization,
but must not distort the objective long-term classification of notes.

---

## 7. Attention-state usage rule

The short-/mid-term attention layer should influence prioritization and query planning.

Do not let attention-state signals override long-term objective knowledge structure.

---

## 8. Self-recovery requirement

This vault must remain understandable even if the user forgets the structure later.

Therefore the system guide should support future questions such as:
- “What can we do here?”
- “How does this system work?”
- “How should I use this vault?”
- “Help me recover my usage pattern.”

When such questions are asked, future agents should consult `/03_SYSTEM_GUIDE/README.md` and related guide files before answering.

---

## 9. Output expectation during bootstrap

When executing bootstrap tasks, prefer to:
- explain what structure is being created
- list missing recommended files if they do not yet exist
- summarize what has already been initialized
- identify what still requires manual confirmation or external tooling
- avoid pretending full automation happened if the environment cannot directly modify files

Be concrete, not vague.

---

## 10. After initialization

After this bootstrap phase:
- Future operations should follow `/03_SYSTEM_GUIDE/SYSTEM_RULES.md`
- This file should be treated as temporary
- The user may manually delete `INIT_BOOTSTRAP.md`

If this file still exists later, interpret it as a bootstrap reference, not a permanent operational rule set.
