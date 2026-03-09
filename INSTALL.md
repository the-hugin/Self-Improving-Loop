# SIL Installation — Instructions for Claude

**You are Claude Code, and you have been asked to set up the Self-Improving Loop system.**

The user has cloned this repository to `~/.claude`. Your job is to:
1. Detect their environment
2. Configure the system for their machine
3. Verify everything works
4. Brief them on the workflow

Read this file completely, then execute the steps below in order.
Do not skip steps. Confirm completion of each step to the user.

---

## Step 1 — Detect Environment

Run the following to understand the machine:

```bash
# Detect OS
uname -s 2>/dev/null || echo "Windows"

# Find home directory
echo $HOME

# Check Python
py --version 2>/dev/null || python3 --version 2>/dev/null || echo "Python not found"

# Verify ~/.claude exists
ls ~/.claude/settings.example.json
```

Determine:
- **OS**: Windows / macOS / Linux
- **Home path**: the absolute path that `~` expands to
- **Python command**: `py` (Windows) or `python3` (Mac/Linux)

Tell the user what you found in one line.

---

## Step 2 — Configure settings.json

```bash
# Copy example config
cp ~/.claude/settings.example.json ~/.claude/settings.json
```

Now edit `~/.claude/settings.json`:
- Replace every occurrence of `~/.claude/` with the **absolute path** you found in Step 1
- On Windows: use forward slashes, e.g. `C:/Users/YourName/.claude/`
- On Mac/Linux: e.g. `/home/yourname/.claude/`
- Replace `py` with `python3` if on Mac/Linux

Confirm: "settings.json configured for [OS] at [path]"

---

## Step 3 — Initialize Federation State

Create `~/.claude/skills/sync-state.json` with this content:

```json
{
  "base_repo": null,
  "last_export": null,
  "last_sync": null,
  "exported_counts": {
    "hard_problems": 0,
    "best_practices": 0,
    "changelog_entries": 0
  }
}
```

If the file already exists and has a `base_repo` set — leave it unchanged.

---

## Step 4 — Verify Hooks

Check that hook scripts exist and are executable:

```bash
ls ~/.claude/hooks/
# Should show: prompt_dispatch.py, post_tool_scan.py, pre_commit_check.py
```

If any file is missing — tell the user and stop.

Run a quick syntax check:

```bash
py ~/.claude/hooks/post_tool_scan.py --help 2>/dev/null || python3 ~/.claude/hooks/post_tool_scan.py --help 2>/dev/null || echo "Hook loaded (no --help flag is normal)"
```

---

## Step 5 — Run Health Check

Tell the user:
> "Setup complete. Let me run a health check."

Execute the `/sil` command by reading `~/.claude/commands/sil.md` and following its instructions.

All blocks should display data. If any block shows an error — diagnose and fix before continuing.

---

## Step 6 — Brief the User

After successful verification, explain the workflow clearly:

---

**The Loop:**

```
New project?    →  /intake         (sets up project context)
During work     →  Claude assists with full context loaded
End of session  →  /reflect        (Claude analyzes what happened)
Add correction  →  one line of feedback in reflection.md
                →  /improve        (skills updated based on your feedback)
```

**Health check anytime:** `/sil` — shows cycle phase, skill status, sync status

**The rhythm:** intake → work → reflect → improve → repeat

---

**Federation (optional, requires gh CLI):**

```
Every ~7 days:  /sil-export   →  sends your improvements to the community
                /sil-sync     →  receives improvements from others
```

To enable federation, you'll need:
1. `gh` CLI installed and authenticated: `gh auth login`
2. The base repo URL — run `/sil-export` and it will ask you

---

**Key files:**
- `~/.claude/skills/hard-problems.md` — what was hard and how it was solved
- `~/.claude/skills/best-practices.md` — patterns that worked well
- `CLAUDE.md` in any project directory — project-specific context

---

## Final Message

Tell the user:

> "SIL is installed and ready.
>
> Start your first project with `/intake` — Claude will set up a CLAUDE.md with your stack, architecture decisions, and session log.
>
> At the end of the session, run `/reflect` and I'll analyze what happened and suggest improvements."
