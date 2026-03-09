# Differential Review — Methodology

Detailed techniques for each phase of the review workflow.

---

## Phase 0 — Intake Commands

```bash
# Git-based
git diff HEAD~1 --stat                      # file overview
git diff HEAD~1                             # full diff
git log --oneline -20                       # recent history
git log --oneline --follow <file>           # file history

# GitHub PR
gh pr view <number>                         # PR summary
gh pr diff <number>                         # full diff
gh pr view <number> --json files,additions,deletions

# Staged changes
git diff --cached                           # what's staged
git diff --cached --stat
```

**Triage checklist:**
- [ ] What is the stated purpose of the change?
- [ ] Does the diff match the stated purpose? (scope creep = risk signal)
- [ ] Are there files modified that aren't mentioned in the PR description?
- [ ] Are there binary files (could hide content)?

---

## Phase 1 — Deep Code Analysis Technique

### Git blame investigation
```bash
git blame <file> -L <start>,<end>           # blame specific lines
git log --all --full-history -- <file>      # full file history
git show <commit>                           # inspect specific commit
git log --grep="security\|fix\|vuln\|CVE" --oneline  # find security commits
```

**What to look for in history:**
- Commits that fixed a bug being reintroduced
- Rapid back-and-forth changes to the same area (instability signal)
- Security-keyword commits near the modified code

### Side-by-side analysis

For each modified function, document:

```
Function: <name> @ <file>:<line>

BEFORE:
  - What invariant was enforced?
  - What validation existed?
  - What was the trust assumption?

AFTER:
  - What changed?
  - Is the invariant still enforced?
  - Was any validation removed? If so, moved where?
  - What is the new trust assumption?

DELTA RISK:
  - What can happen now that couldn't before?
  - What is no longer guaranteed?
```

---

## Phase 4 — Deep Context Analysis

Use when a function/file is rated HIGH or CRITICAL.

### Step 1 — Map the call chain

```bash
# Find all callers
grep -rn "<function_name>" --include="*.py" .
grep -rn "<function_name>" --include="*.ts" .

# Find what this function calls
grep -n "def \|function \|const " <file>
```

Document: `caller → function → callee → callee` chain.

### Step 2 — Document invariants

For each function in the chain, write:
- **Pre-condition:** What must be true when function is entered?
- **Post-condition:** What is guaranteed when function returns?
- **Side effects:** What state does it modify?

Minimum 3 invariants per HIGH-risk function.

### Step 3 — Trust boundary map

Identify where untrusted data (user input, external API, file system, env vars) enters the system and trace its path through the changed code.

```
[untrusted source] → [entry point] → [transformation] → [sink]
```

Mark each transformation: does it sanitize, validate, or pass through raw?

### Step 4 — Shared mutable state

List all global/module-level variables or shared objects that the modified code reads or writes. Check if concurrent access is possible.

---

## Scope Adjustment by Change Size

### SMALL (< 20 files)
- Full Phase 1–5 on all HIGH/MEDIUM files
- Phase 4 on all HIGH files
- Expected time: thorough

### MEDIUM (20–200 files)
- Phase 1 on all HIGH files, sample of MEDIUM
- Phase 4 on top 3 HIGH files by blast radius
- Explicitly state which MEDIUM files were sampled vs fully reviewed

### LARGE (200+ files)
- Phase 1 on all HIGH files only
- Phase 3 (blast radius) on top 10 most-modified functions
- State coverage percentage explicitly in the report
- Recommend splitting the PR if possible
