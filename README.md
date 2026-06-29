# ⚡ DevPulse

> Personal dev knowledge base — notes, snippets, journal, quotes, and auto-updating resources.

A structured, version-controlled second brain for my learning journey in CS, DSA, AI/ML, Python, and trading.
Automated maintenance runs on a schedule via GitHub Actions — adding new quotes and resources without touching hand-written content.

---

## 📂 Structure

```
DevPulse/
├── notes/              # Topic-based learning notes (hand-written)
│   ├── ai.md           # AI & ML concepts
│   ├── python.md       # Core Python
│   └── dsa.md          # Data Structures & Algorithms
├── snippets/           # Reusable, tested code snippets (C++)
│   └── dfs.cpp         # Depth-First Search (recursive + iterative)
├── quotes/             # Curated programming wisdom
│   └── tech_quotes.md
├── resources/          # Useful websites & tools
│   └── websites.md
├── journal/            # Monthly dev journal (hand-written)
│   └── 2026-07.md
├── scripts/            # Automation scripts
│   └── update.py       # Maintenance script (quotes + resources)
├── logs/
│   └── activity.log    # Auto-appended run history
└── .github/
    └── workflows/
        └── update.yml  # Scheduled GitHub Action
```

---

## 📝 Notes

Kept practical — things I actually use, not just syntax trivia.

| File | Topics |
|------|--------|
| [notes/ai.md](notes/ai.md) | LLMs, Prompt Engineering, RAG, Embeddings, Agents, Fine-tuning, Vector DBs |
| [notes/python.md](notes/python.md) | Data Types, OOP, File Handling, Decorators, Generators, Async |
| [notes/dsa.md](notes/dsa.md) | Arrays, Linked Lists, Trees, Graphs, DP, Greedy |

## ✏️ Snippets

Every snippet compiles and runs. Includes complexity notes and usage context.

| File | Description |
|------|-------------|
| [snippets/dfs.cpp](snippets/dfs.cpp) | DFS on a graph — recursive + iterative, O(V+E) |

## 📓 Journal

Monthly entries — written by hand. What I built, learned, and want to explore next.

## ⚙️ Automation

The GitHub Action (`update.yml`) runs on a schedule and calls `scripts/update.py`, which:
- Adds one new curated quote to `quotes/tech_quotes.md` (if pool not exhausted)
- Adds one new curated resource to `resources/websites.md` (if pool not exhausted)
- Refreshes the `Last updated` stamp in this README
- Logs every run to `logs/activity.log`
- Writes a conventional commit message to `.commitmessage.txt`

Notes and journal entries are **never** auto-generated — those stay hand-written.

---

*Last updated: 2026-06-29*

---
_Last updated 2026-06-29 18:00 UTC_
