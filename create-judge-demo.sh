#!/bin/bash
# Trigger Real PatchPro CI Demo
# Creates a PR with security issues and lets judges watch the real CI workflow

set -e

echo "🛡️ Creating Real PatchPro CI Demo..."
echo ""

# Create a branch with timestamp
DEMO_BRANCH="demo/judge-test-$(date +%s)"
echo "📝 Creating branch: $DEMO_BRANCH"
git checkout -b "$DEMO_BRANCH"

# Add a file with real security vulnerabilities
echo "🔴 Adding vulnerable code..."
cat > judge_demo_vulnerable.py << 'EOF'
# PatchPro Judge Demo - Vulnerable Code
# This file contains REAL security issues that PatchPro will detect and fix

import sqlite3
import hashlib

# SECURITY ISSUE: Hardcoded database password
DB_PASSWORD = "super_secret_admin_password_123"

def authenticate_user(username, password):
    """VULNERABLE: SQL Injection"""
    conn = sqlite3.connect("users.db")
    # SECURITY ISSUE: Direct string interpolation = SQL injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor = conn.execute(query)
    return cursor.fetchone() is not None

def hash_password(password):
    """VULNERABLE: Weak hashing"""
    # SECURITY ISSUE: MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()

# SECURITY ISSUE: Hardcoded API key
API_KEY = "sk-1234567890abcdef"
API_SECRET = "secret-key-please-dont-share"

class UserSession:
    def __init__(self):
        # SECURITY ISSUE: Predictable session tokens
        self.session_token = "user_session_" + str(hash("admin"))
        
    def validate_input(self, user_input):
        """VULNERABLE: No input sanitization"""
        # SECURITY ISSUE: Direct eval() execution
        return eval(user_input)

# SECURITY ISSUE: Debug mode with sensitive info
DEBUG = True
if DEBUG:
    print(f"Database password: {DB_PASSWORD}")
    print(f"API key: {API_KEY}")
EOF

# Commit the vulnerable code
git add judge_demo_vulnerable.py
git commit -m "feat: add user authentication system (JUDGE DEMO)

This commit introduces authentication functionality but contains
deliberate security vulnerabilities for PatchPro to detect:

- SQL injection in authenticate_user()
- Hardcoded credentials (DB_PASSWORD, API_KEY)
- Weak MD5 hashing
- Dangerous eval() usage
- Debug info leakage

PatchPro should detect and fix all these issues automatically."

# Push the branch
echo "📤 Pushing branch to trigger CI..."
git push origin "$DEMO_BRANCH"

# Create the PR
echo "📝 Creating Pull Request..."
PR_URL=$(gh pr create \
  --title "🔴 JUDGE DEMO: Security vulnerabilities for PatchPro to fix" \
  --body "## 🛡️ PatchPro Judge Demonstration

This PR contains **real security vulnerabilities** for demonstration purposes.

### 🔴 Security Issues Included:
- **SQL Injection** (line 13): Direct string interpolation in SQL query
- **Hardcoded Credentials** (lines 8, 27-28): Database password and API keys in plaintext
- **Weak Hashing** (line 19): MD5 instead of secure hashing
- **Code Injection** (line 37): Dangerous \`eval()\` usage
- **Information Disclosure** (lines 42-44): Debug mode leaking sensitive data

### 🤖 Watch PatchPro in Action:

1. **Check the 'Actions' tab** to see PatchPro CI running
2. **View this PR** for automated comment with analysis
3. **Download artifacts** to see generated patches and telemetry

### ⏱️ Expected Timeline:
- **Analysis**: 30-60 seconds
- **AI Patch Generation**: 1-2 minutes  
- **PR Comment**: Within 3 minutes

PatchPro will automatically:
✅ Detect all security issues
✅ Generate production-ready patches
✅ Validate patches with git apply
✅ Post comprehensive analysis report
✅ Capture telemetry for self-learning

**This demonstrates the complete CI/CD integration that judges need to see!**" 2>/dev/null)

echo ""
echo "🎉 SUCCESS! Real PatchPro demo created:"
echo ""
echo "📋 What to do next:"
echo "1. 🔗 View PR: $PR_URL"
echo "2. 🔗 Watch CI: https://github.com/A3copilotprogram/patchpro-demo-repo-waigi-ci-test-demo/actions"
echo "3. ⏱️  Wait 2-3 minutes for PatchPro to analyze and comment"
echo "4. 📊 Download artifacts to see patches and telemetry"
echo ""
echo "🎯 This shows the REAL PatchPro workflow that judges need to see!"

# Return to original branch
git checkout main 2>/dev/null || git checkout -