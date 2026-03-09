# Differential Review — Report Template

## Full Report Structure

```markdown
# Differential Review: <PR title / commit hash / description>

**Date:** <date>
**Scope:** <file count> files, <+additions> / <-deletions>
**Change size:** SMALL / MEDIUM / LARGE
**Coverage:** <X>% of changed files reviewed (state if < 100%)

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | X |
| 🟠 High     | X |
| 🟡 Medium   | X |
| 🟢 Low      | X |

**Recommendation:** BLOCK / CONDITIONAL MERGE / MERGE WITH NOTES

> One-sentence summary of the most important finding or overall assessment.

---

## What Changed

| File | Risk | Blast Radius | Notes |
|------|------|-------------|-------|
| path/to/file.py | HIGH | CRITICAL (67 callers) | Removed auth check |
| path/to/other.py | MEDIUM | LOW (3 callers) | New public API |

---

## Critical Findings

### 🔴 [C1] <Short title>

**File:** `path/to/file.py:42`
**Blast radius:** HIGH (23 callers)

**What changed:**
```diff
- if user.is_admin:
+ if user.is_admin or debug_mode:
```

**Attack scenario:**
> Attacker sets `debug_mode=True` via environment variable (accessible in staging),
> bypasses admin check, accesses privileged endpoint.

**Exploitability:** MEDIUM — requires env var access or knowledge of deployment config.

**Fix:**
Remove `debug_mode` escape hatch from auth check. If needed for debugging,
use a separate mechanism that cannot reach production.

---

## High Findings

### 🟠 [H1] <Short title>

... (same structure as Critical) ...

---

## Test Coverage Gaps

| Finding | Missing Test | Risk if Untested |
|---------|-------------|-----------------|
| Modified `validate_token()` | No test for expired token edge case | MEDIUM |

---

## Recommendations

### Immediate (block merge)
- [ ] Fix C1: remove debug_mode from auth path

### Pre-production
- [ ] Add test coverage for H1 edge cases

### Tech debt
- [ ] Refactor: validation logic is duplicated in 3 places, creating drift risk

---

## Analysis Limitations

- Files not reviewed: `migrations/`, `tests/` (out of scope)
- LARGE change: only HIGH-risk files analyzed in depth; MEDIUM files sampled
- No access to runtime environment — env var values assumed from code defaults
- External API behavior (third-party service X) not modeled
```

---

## Severity Definitions

| Level | When to use |
|-------|------------|
| 🔴 Critical | Exploitable by external attacker, direct impact on security/data |
| 🟠 High | Significant risk, requires specific conditions or insider access |
| 🟡 Medium | Risk is real but mitigated by other controls, or hard to exploit |
| 🟢 Low | Best practice violation, no immediate exploitability |

---

## Recommendation Definitions

| Recommendation | Meaning |
|---------------|---------|
| **BLOCK** | Critical/High findings that must be fixed before merge |
| **CONDITIONAL MERGE** | Merge only after specific fixes + may need follow-up PR |
| **MERGE WITH NOTES** | Low/Medium findings only; document as known tech debt |
