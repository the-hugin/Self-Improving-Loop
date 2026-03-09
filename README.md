# Self-Improving Loop

> A self-improvement system for Claude Code — skills, hooks, templates, and federated knowledge sharing across users.

Claude Code is powerful out of the box, but it starts fresh every session. **Self-Improving Loop (SIL)** gives Claude persistent memory, structured reflection, and a mechanism to get measurably better at your specific workflows over time.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                   THE LOOP                                  │
│                                                             │
│   /intake          work           /reflect      /improve   │
│  ─────────►  ─────────────►  ──────────────►  ──────────►  │
│  Project        Claude         Session           Skills     │
│  context        helps          analysis          updated    │
│  loaded                        written                      │
│                                                             │
│                         ▲                          │        │
│                         └──── better next time ───┘        │
└─────────────────────────────────────────────────────────────┘
```

After each session, Claude reflects on what worked, what caused friction, and what should be automated. You provide a one-line correction. The system updates its own skills accordingly.

**Over time:** Claude learns your stack, your patterns, your preferences — and shares discoveries with the community via federation.

---

## Prerequisites

| Tool | Purpose | Required |
|------|---------|----------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | The AI CLI | ✅ |
| Python 3.x | Hook scripts | ✅ |
| `py` launcher (Windows) or `python3` (Mac/Linux) | Running hooks | ✅ |
| git | Version control | ✅ |
| [gh CLI](https://cli.github.com/) | Federation (export/sync) | Optional |

---

## Installation

### Option A — Automatic via Claude (recommended)

```bash
# 1. Clone to your Claude config directory
git clone https://github.com/the-hugin/Self-Improving-Loop.git ~/.claude

# 2. Open Claude Code anywhere
cd ~/any-project
claude

# 3. Tell Claude to set you up
# "Read ~/.claude/INSTALL.md and set me up"
```

Claude will detect your OS, adapt paths, configure hooks, and brief you on the workflow.

### Option B — Manual

```bash
# 1. Clone
git clone https://github.com/the-hugin/Self-Improving-Loop.git ~/.claude

# 2. Configure settings
cp ~/.claude/settings.example.json ~/.claude/settings.json
# Edit settings.json — replace ~/.claude/ with your absolute path
# Windows: C:/Users/YourName/.claude/
# Mac/Linux: /home/yourname/.claude/

# 3. Initialize federation state
cp template below → ~/.claude/skills/sync-state.json:
# { "base_repo": null, "last_export": null, "last_sync": null,
#   "exported_counts": { "hard_problems": 0, "best_practices": 0, "changelog_entries": 0 } }
```

---

## The Rhythm

### Every project

```
/intake          → Sets up project context (CLAUDE.md)
[do your work]   → Claude assists with full context
/reflect         → Claude analyzes the session, writes reflection.md
[add correction] → You write one line: what to do differently
/improve         → Skills updated based on reflection
```

### Every 7 days (federation)

```
/sil-export  → Packages your improvements → creates PR to base repo
             → Curator reviews and merges
/sil-sync    → Pulls community improvements → diff-by-diff approval
```

### Health check anytime

```
/sil  → Shows: project state, cycle phase, skill health, sync status, recommendations
```

---

## Skills

### Meta-Loop (the core three)

| Skill | What it does |
|-------|-------------|
| `intake` | Onboards a project → generates structured `CLAUDE.md` |
| `reflect` | Analyzes a session → writes `reflection.md` with 5-axis analysis |
| `improve` | Applies reflection → updates skills with diff-by-diff approval |

### Security

| Skill | What it does |
|-------|-------------|
| `differential-review` | Security review of PRs/diffs — Trail of Bits methodology |
| `insecure-defaults` | Finds fail-open vulnerabilities, hardcoded credentials |

### Domain

| Skill | What it does |
|-------|-------------|
| `design-master` | Full-stack design: landing pages, dashboards, posters |
| `ui-ux-pro-max` | 67 styles, 96 palettes, design system generator |
| `backend-code-review` | Code quality and security review for Python/API |
| `electron-dev` | Desktop apps with Electron + React + Vite |
| `data-analyst` | SQL, pandas, statistical analysis |
| `web-scraper` | Web scraping and data extraction |
| `api-endpoint-probe` | API endpoint reconnaissance before integration |
| `project-planner` | Project decomposition with dependencies |
| `multi-agent-patterns` | Multi-agent orchestration architectures |

### Federation

| Skill | What it does |
|-------|-------------|
| `sil-export` | Packages improvements → PR to base repo |
| `sil-sync` | Pulls community improvements with security scan + approval |
| `sil-security-scan` | Threat patterns for incoming/outgoing content |

---

## Federation Architecture

SIL uses a two-layer model:

```
Layer 1: Architecture (this repo)
  Clone once. Update rarely. Contains: skills, hooks, templates, CLAUDE.md.

Layer 2: Knowledge (federated)
  hard-problems.md  ─── sil-export ──► GitHub PR ──► curator merges
  best-practices.md                                        │
  skill changes                                            ▼
                    ◄── sil-sync ────── base repo ◄────────┘
```

Your research data and project names stay local — only anonymized technical patterns are shared.

**Security:** All incoming content is scanned for prompt injection, hidden unicode, malicious bash patterns, and suspicious URLs before being shown to you. Every change requires explicit approval.

---

## Slash Commands

| Command | Description |
|---------|-------------|
| `/sil` | Health check — cycle phase, skills, sync status |
| `/intake` | Start a new project |
| `/reflect` | End-of-session analysis |
| `/improve` | Apply reflection to skills |
| `/sil-export` | Export improvements to base repo |
| `/sil-sync` | Pull updates from base repo |
| `/diff-review` | Security review of a diff/PR |
| `/weekly-review` | Deep review every 10 sessions |

---

## Knowledge Base

| File | Purpose |
|------|---------|
| `skills/hard-problems.md` | Episodic memory — what was hard and how it was solved |
| `skills/best-practices.md` | Positive memory — patterns that worked well |
| `skills/changelog.md` | History of skill changes |
| `reflection.md` | Current pending reflection (session output) |

---

## Contributing

Your improvements automatically become contributions:

```
1. Use SIL normally across your projects
2. Run /sil-export when you have improvements
3. A PR is created automatically
4. Curator reviews and merges to base repo
5. Community gets your improvements via /sil-sync
```

No manual PR writing needed — `sil-export` handles everything.

---

## License

MIT
