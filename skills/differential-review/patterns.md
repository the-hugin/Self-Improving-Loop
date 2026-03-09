# Differential Review — Vulnerability Patterns

Quick reference for common patterns to look for during code review.
Each entry: pattern → what to check → why it matters.

---

## Authentication & Authorization

| Pattern | What to check | Risk |
|---------|--------------|------|
| `if user.role == "admin"` removed/loosened | Is the check still enforced elsewhere? | Privilege escalation |
| Function moved from protected to public scope | Any caller can now reach it | Auth bypass |
| `@require_auth` decorator removed | Endpoint now accessible without login | Unauth access |
| JWT decode without `verify=True` | Tokens not validated | Token forgery |
| Session not invalidated on role change | Old session retains old role | Privilege persistence |

---

## Input Validation & Injection

| Pattern | What to check | Risk |
|---------|--------------|------|
| String concatenation in SQL | `"SELECT * FROM " + table_name` | SQL injection |
| `subprocess` / `os.system` with user input | Shell injection possible | RCE |
| `eval()` / `exec()` on user data | Arbitrary code execution | RCE |
| File path from user input | `../` traversal, symlink attacks | Path traversal |
| XML/YAML parsing of user content | XXE, YAML deserialization | XXE / Deserialization |
| Removed `bleach` / `escape` / `sanitize` call | XSS in rendered output | XSS |

---

## Secrets & Configuration

| Pattern | What to check | Risk |
|---------|--------------|------|
| `os.environ.get('KEY') or 'default'` | Fail-open: runs with weak default | Insecure default |
| Hardcoded password/token/key in source | `SECRET = "abc123"` | Credential leak |
| `verify=False` in requests | TLS not validated | MITM |
| `DEBUG = True` in production config path | Leaks stack traces, disables security | Info disclosure |
| `CORS_ORIGINS = ["*"]` added | Any origin can make authenticated requests | CORS bypass |
| Removed HTTPS redirect | Downgrade to HTTP | MITM |

---

## Cryptography

| Pattern | What to check | Risk |
|---------|--------------|------|
| MD5 / SHA1 used for password hashing | Weak, rainbow-table vulnerable | Hash crack |
| AES-ECB mode | Identical blocks produce identical ciphertext | Pattern leakage |
| Hardcoded IV / nonce | Deterministic encryption | Crypto weakness |
| `random` instead of `secrets` for tokens | Predictable values | Token guessing |
| No salt in hash | Rainbow table attacks | Hash crack |

---

## Error Handling & Information Disclosure

| Pattern | What to check | Risk |
|---------|--------------|------|
| `except Exception as e: return str(e)` | Stack trace / internal details in response | Info disclosure |
| Stack trace sent to client | File paths, library versions exposed | Recon aid |
| Sensitive data logged | Passwords, tokens, PII in logs | Data leak |
| Removed try/except around security op | Unhandled exception crashes or skips logic | DoS / bypass |

---

## State & Concurrency

| Pattern | What to check | Risk |
|---------|--------------|------|
| Balance/counter updated without transaction | Race condition → inconsistent state | Data corruption |
| `if resource.exists(): resource.use()` | TOCTOU race window | Race condition |
| Shared mutable object accessed from threads | No lock → data race | Data corruption |
| Cache populated before auth check | Authenticated data served to anon user | Auth bypass |

---

## Supply Chain

| Pattern | What to check | Risk |
|---------|--------------|------|
| New package added to dependencies | Is it well-maintained? Any known CVEs? | Supply chain |
| Version pinned → unpinned | Auto-updates from untrusted source | Supply chain |
| `install_requires` loosened | Transitive dep can drift to vulnerable version | Supply chain |
| `setup.py` / `pyproject.toml` changed | Build-time code execution risk | Build poisoning |
