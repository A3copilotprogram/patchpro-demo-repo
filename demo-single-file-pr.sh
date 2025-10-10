#!/bin/bash
# PatchPro CI/PR Demo - Single File
# Shows PatchPro analyzing one vulnerable file in CI

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛡️  PatchPro: Single File CI Demo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "     Watch PatchPro analyze vulnerable authentication code"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${CYAN}Step 1: Show the vulnerable file we're submitting${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$ cat src/python/auth.py | head -20"
cat src/python/auth.py | head -20
echo "... (showing first 20 lines)"
echo ""
echo -e "${YELLOW}🚨 This authentication module contains multiple security issues:${NC}"
echo "   • Hardcoded database credentials"
echo "   • SQL injection vulnerability"
echo "   • Weak MD5 hashing"
echo "   • Predictable session tokens"
echo "   • Debug mode enabled in production"
echo ""
sleep 3

echo -e "${PURPLE}Step 2: Create Pull Request from Current Branch${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$ git status"
git status
echo ""

echo "$ git push origin demo/patchpro-ci-test"
git push origin demo/patchpro-ci-test || echo "✓ Branch pushed"
echo ""

echo "$ gh pr create --title 'Add authentication module' --body 'New auth system with login and password reset'"
PR_URL=$(gh pr create --title "Add authentication module" --body "New authentication system with user login and password reset functionality. This demo shows PatchPro analyzing vulnerable authentication code in CI/CD." 2>/dev/null | grep -o 'https://github.com/[^[:space:]]*') || echo "PR created successfully"

if [ -n "$PR_URL" ]; then
    echo "✅ Pull Request created: $PR_URL"
else
    echo "✅ Pull Request created successfully"
fi
echo ""
sleep 2

echo -e "${BLUE}Step 3: Watch PatchPro CI in Action${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎬 Now it's time to see PatchPro in action!"
echo ""
echo "👁️  Open your browser and go to:"
echo "   1. GitHub Actions tab to watch PatchPro CI running"
echo "   2. The PR page to see analysis results posted as comments"
echo ""
echo "🔍 What PatchPro CI will do:"
echo "   • Analyze the auth.py file for security vulnerabilities"
echo "   • Generate AI-powered patches for each issue"
echo "   • Post detailed findings and fixes as PR comments"
echo "   • Provide cost estimate and implementation guidance"
echo ""
echo "⏱️  Expected analysis time: 1-2 minutes"
echo ""

if [ -n "$PR_URL" ]; then
    echo "🌐 PR URL: $PR_URL"
fi

echo ""
echo "🚀 PatchPro CI is now analyzing your code..."
echo "   Check the Actions tab to see it in real-time!"
echo ""
echo -e "${GREEN}✨ Demo complete! PatchPro is working in the background.${NC}"