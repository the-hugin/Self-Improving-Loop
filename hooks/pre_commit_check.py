#!/usr/bin/env python3
"""
PreToolUse hook: security gate before git commit.

Checks staged files for security-sensitive patterns:
1. Filename patterns (credentials, secrets)
2. Content patterns (OSINT data, API keys, hidden unicode)

Exit 0 + JSON output = structured decision (no exit code 2 needed).
"""
import sys
import json
import subprocess
import re


# --- Filename patterns (existing) ---
SECURITY_PATTERN = re.compile(
    r'(\.env$|\.env\.|'
    r'config\.(py|js|ts|yaml|yml|json|toml|ini|cfg)$|'
    r'settings\.(py|js|ts|yaml|yml|json|toml|ini|cfg)$|'
    r'secrets?\.|'
    r'(auth|cred|credential|password|passwd|token|apikey|api_key|'
    r'private.?key|secret.?key|jwt|oauth|hmac)\.(py|js|ts|yaml|yml|json)$|'
    r'\.(key|pem|p12|pfx|cert|crt|cer)$|'
    r'crypto\.(py|js|ts)$)',
    re.IGNORECASE
)

# --- Content patterns (new) ---
CONTENT_PATTERNS = [
    # OSINT / personal data indicators
    (r'PERSONS\s*=\s*\[', 'OSINT persons list detected'),
    (r'smtp_verify\s*\(', 'SMTP email enumeration code detected'),
    (r'email_permutation', 'Email permutation tool detected'),
    (r'def get_mx\s*\(', 'DNS MX lookup for OSINT detected'),

    # Credential patterns in content
    (r'sk-ant-[a-zA-Z0-9\-_]{20,}', 'Anthropic API key in content'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub token in content'),
    (r'AKIA[0-9A-Z]{16}', 'AWS access key in content'),
    (r'-----BEGIN (RSA |EC )?PRIVATE KEY-----', 'Private key in content'),

    # Hidden unicode
    (r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', 'Hidden unicode characters detected'),
]


def get_staged_content(cwd):
    """Get full diff of staged changes."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "-U0"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=cwd
        )
        return result.stdout
    except Exception:
        return ""


def scan_content(content):
    """Scan staged content for sensitive patterns. Returns list of (description, snippet)."""
    findings = []
    for pattern, description in CONTENT_PATTERNS:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            # Extract a short context snippet
            start = max(0, match.start() - 30)
            end = min(len(content), match.end() + 30)
            snippet = content[start:end].replace('\n', ' ').strip()
            findings.append((description, snippet[:80]))
    return findings


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")

    # Only act on git commit
    if "git commit" not in command:
        sys.exit(0)

    cwd = data.get("cwd", ".")

    # Get staged files
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd
        )
        staged_files = result.stdout.strip().splitlines()
    except Exception:
        sys.exit(0)

    if not staged_files:
        sys.exit(0)

    issues = []

    # 1. Check filenames
    security_files = [f for f in staged_files if SECURITY_PATTERN.search(f)]
    if security_files:
        files_str = ", ".join(security_files[:5])
        if len(security_files) > 5:
            files_str += f" (+{len(security_files) - 5} more)"
        issues.append(
            f"Sensitive filename(s): {files_str}. "
            f"Run `insecure-defaults` or `differential-review` to verify."
        )

    # 2. Scan content
    staged_content = get_staged_content(cwd)
    if staged_content:
        content_findings = scan_content(staged_content)
        for description, snippet in content_findings:
            issues.append(f"Content issue: {description} — «{snippet}»")

    if not issues:
        sys.exit(0)

    reason = (
        "Security gate blocked commit. Issues found:\n"
        + "\n".join(f"  • {i}" for i in issues)
        + "\nReview and fix before committing."
    )

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
