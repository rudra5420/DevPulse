#!/usr/bin/env python3
"""
DevPulse Automation Script

Performs small, honest maintenance tasks on the DevPulse repository on a
schedule (invoked by .github/workflows/update.yml). Designed to be safe to
re-run repeatedly without producing duplicate or low-quality content.

What this script does:
  1. Picks one maintenance action at random:
       - add a new curated quote to quotes/tech_quotes.md, OR
       - add a new curated resource link to resources/websites.md
     Each action skips itself if its content pool is already exhausted
     (i.e. everything in the pool is already present in the file).
  2. Refreshes the 'Last updated' stamp in README.md.
  3. Appends a record of exactly what changed to logs/activity.log.
  4. Writes a one-line, conventional-commit-style message to
     .commitmessage.txt for the CI workflow to use when committing.

What this script intentionally does NOT do:
  - It never writes to notes/ or journal/. Those files represent genuine,
    first-person learning and are maintained by hand. Auto-generating
    learning content there would misrepresent the repository's history
    rather than maintain it.

Design principles:
  - Modular: each maintenance task is an independent, testable function.
  - Idempotent-friendly: re-running with no new content available is a
    harmless no-op, not an error.
  - Defensive: every file operation is wrapped in error handling so a
    single failure doesn't crash the whole run or corrupt a file.
"""
from __future__ import annotations

import random
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT    = Path(__file__).resolve().parent.parent
QUOTES_FILE  = REPO_ROOT / "quotes" / "tech_quotes.md"
WEBSITES_FILE = REPO_ROOT / "resources" / "websites.md"
README_FILE  = REPO_ROOT / "README.md"
LOG_FILE     = REPO_ROOT / "logs" / "activity.log"
COMMIT_MSG_FILE = REPO_ROOT / ".commitmessage.txt"

# ---------------------------------------------------------------------------
# Content pools
# ---------------------------------------------------------------------------
QUOTE_POOL: list[tuple[str, str]] = [
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("Code never lies; comments sometimes do.", "Ron Jeffries"),
    ("The best error message is the one that never shows up.", "Thomas Fuchs"),
    ("Walking on water and developing software from a specification are easy if both are frozen.", "Edward V. Berard"),
    ("It is not enough for code to work.", "Robert C. Martin"),
    ("Optimism is an occupational hazard of programming; feedback is the treatment.", "Kent Beck"),
    ("A good programmer looks both ways before crossing a one-way street.", "Doug Linder"),
]

RESOURCE_POOL: list[tuple[str, str, str]] = [
    ("Exercism", "https://exercism.org", "Hands-on coding exercises with mentor feedback across many languages."),
    ("Project Euler", "https://projecteuler.net", "Math/programming challenges that strengthen algorithmic thinking."),
    ("The Odin Project", "https://www.theodinproject.com", "Free, project-based full-stack web development curriculum."),
    ("Distill.pub", "https://distill.pub", "Visual, in-depth explanations of machine learning concepts."),
    ("Real Python", "https://realpython.com", "In-depth Python tutorials and best-practice write-ups."),
    ("Codeforces", "https://codeforces.com", "Competitive programming contests and a deep archive of rated problems."),
]

# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------
def now_str() -> str:
    """Current UTC time as a consistent display string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def read_text(path: Path) -> str:
    """Read a file's text, returning an empty string if it doesn't exist yet."""
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write_text(path: Path, content: str) -> None:
    """Write text to a file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def append_line(path: Path, line: str) -> None:
    """Append a single line to a file, creating it if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

# ---------------------------------------------------------------------------
# Maintenance actions
# ---------------------------------------------------------------------------
def add_quote() -> Optional[str]:
    """Append one new curated quote to quotes/tech_quotes.md, if any remain."""
    content = read_text(QUOTES_FILE)
    candidates = [q for q in QUOTE_POOL if q[0] not in content]
    if not candidates:
        return None
    quote_text, author = random.choice(candidates)
    entry = f"\n> {quote_text}\n> \u2014 {author}\n"
    write_text(QUOTES_FILE, content.rstrip() + "\n" + entry)
    return f"added a quote by {author} to quotes/tech_quotes.md"

def add_resource() -> Optional[str]:
    """Append one new curated resource link to resources/websites.md, if any remain."""
    content = read_text(WEBSITES_FILE)
    candidates = [r for r in RESOURCE_POOL if r[1] not in content]
    if not candidates:
        return None
    name, url, description = random.choice(candidates)
    entry = f"- **[{name}]({url})** \u2014 {description}\n"
    write_text(WEBSITES_FILE, content.rstrip() + "\n" + entry)
    return f"added resource {name} to resources/websites.md"

def refresh_readme_timestamp() -> str:
    """Update the 'Last updated ...' stamp at the bottom of README.md."""
    content = read_text(README_FILE)
    stamp_line = f"*Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}*"
    pattern = re.compile(r"\*Last updated:.*\*")
    if pattern.search(content):
        content = pattern.sub(stamp_line, content, count=1)
    else:
        content = content.rstrip() + f"\n\n---\n\n{stamp_line}\n"
    write_text(README_FILE, content)
    return "refreshed the README timestamp"

def log_activity(summary: str, touched_files: list[str]) -> None:
    """Append a single dated line to logs/activity.log describing this run."""
    files_str = ", ".join(touched_files) if touched_files else "none"
    line = f"{now_str()} | {files_str} | {summary}"
    append_line(LOG_FILE, line)

def write_commit_message(message: str) -> None:
    """Write the commit message the CI workflow should use for this run."""
    write_text(COMMIT_MSG_FILE, f"chore(auto): {message}\n")

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_action_safely(name: str, action: Callable[[], Optional[str]]) -> Optional[str]:
    """Run a single maintenance action, catching and reporting any error."""
    try:
        return action()
    except Exception:
        print(f"update.py: Action '{name}' raised an error:", file=sys.stderr)
        traceback.print_exc()
        return None

def main() -> int:
    random.seed()  # default time-based seed

    candidate_actions: list[tuple[str, Callable[[], Optional[str]], list[str]]] = [
        ("add_quote",    add_quote,    ["quotes/tech_quotes.md"]),
        ("add_resource", add_resource, ["resources/websites.md"]),
    ]
    random.shuffle(candidate_actions)

    summary: Optional[str] = None
    touched_files: list[str] = []

    for name, action, files in candidate_actions:
        result = run_action_safely(name, action)
        if result:
            summary = result
            touched_files = list(files)
            break

    if summary is None:
        print("update.py: No new content this run — all pools already present in their target files. Nothing to commit.")
        return 0  # not an error; a quiet run is a valid outcome

    # Refresh the README timestamp as part of the same run.
    timestamp_summary = run_action_safely("refresh_readme_timestamp", refresh_readme_timestamp)
    if timestamp_summary:
        touched_files.append("README.md")
        full_summary = f"{summary}; {timestamp_summary}"
    else:
        full_summary = summary

    touched_files.append("logs/activity.log")
    try:
        log_activity(full_summary, touched_files)
    except Exception:
        print("update.py: Failed to write to activity log.", file=sys.stderr)
        traceback.print_exc()

    try:
        write_commit_message(summary)
    except Exception:
        print("update.py: Failed to write commit message file.", file=sys.stderr)
        traceback.print_exc()

    print(f"update.py: Done — {full_summary}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
