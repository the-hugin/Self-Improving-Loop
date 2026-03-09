# Differential Review — Adversarial Modeling

Framework for constructing attack scenarios for HIGH-risk findings.

---

## Attacker Model Template

For each HIGH finding, fill in:

```
## Finding: <short title>

### Attacker Model
- **Who:** [external user / authenticated user / insider / adjacent service]
- **Access level:** [unauthenticated / user role / admin / network access only]
- **Motivation:** [data exfiltration / privilege escalation / DoS / financial gain]

### Attack Vector
Step-by-step exploitation sequence:
1. Attacker does X
2. This triggers Y in the changed code
3. Because validation Z was removed/weakened
4. Attacker gains/causes W

### Exploitability
- **Rating:** EASY / MEDIUM / HARD
- **Justification:** [why — what prerequisites are needed, how detectable is it]
- **Preconditions:** [what must be true for this to work]

### Impact
- **Confidentiality:** [none / low / high]
- **Integrity:** [none / low / high]
- **Availability:** [none / low / high]
- **Business impact:** [what actually breaks for the user/organization]
```

---

## Exploitability Ratings

**EASY**
- No special access required
- Reproducible in < 5 steps
- No timing or race conditions
- Payload is trivial (e.g., empty string, null, negative number)

**MEDIUM**
- Requires authenticated account OR specific knowledge of internals
- Needs some setup (specific state, sequence of calls)
- Partially mitigated by other controls, but those can be bypassed

**HARD**
- Requires privileged access OR race condition OR complex multi-step setup
- Only exploitable in very specific deployment configurations
- High likelihood of detection before completing attack

---

## Common Attack Patterns by Category

### Auth & Session
- Token not invalidated after role change
- Session fixation (session ID reused after login)
- Privilege check removed from inner function but left on outer
- JWT `alg: none` or weak secret
- Password reset token not expiring

### Input Handling
- Validation moved from server to client only
- Whitelist replaced with blacklist
- Encoding step removed from output
- SQL query built with string concatenation
- Path traversal via `../` in file operations

### Configuration & Secrets
- Fallback to weak default when env var missing
- Secret logged in error message
- Credentials committed in config file
- CORS wildcard added
- Debug mode enabled in production path

### Data Flow
- User-controlled value used in privileged operation without sanitization
- Taint flows from HTTP input → DB query / file path / shell command
- Deserialization of user-controlled data without type checking

### Concurrency
- Check-then-act on shared state without lock
- TOCTOU (time-of-check to time-of-use) on file or DB record
- Counter/balance updated in non-atomic operation

---

## Red Flags That Auto-Escalate to HIGH

Found any of these in the diff? → Immediately HIGH, no further justification needed:

- `or "default"` / `or 'secret'` / `or None` on a security-critical env var
- `verify=False` in HTTP requests
- `allow_all = True` or equivalent
- `# nosec` or `# type: ignore` on security-relevant line
- Removed `raise` / `assert` from auth check
- Added `except: pass` around security operation
- `eval(`, `exec(`, `os.system(`, `subprocess.shell=True` on user input
- Removed CSRF token check
- Added `CORS_ORIGIN = "*"`
