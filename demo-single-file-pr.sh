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

# Close any existing PR from this branch to main for repeatability
echo "$ gh pr close --head demo/patchpro-ci-test --base main 2>/dev/null || echo 'No existing PR to close'"
gh pr close --head demo/patchpro-ci-test --base main 2>/dev/null || echo "No existing PR to close"
echo ""

echo "$ git status"
git status
echo ""

echo "$ git push origin demo/patchpro-ci-test"
git push origin demo/patchpro-ci-test || echo "✓ Branch pushed"
echo ""

echo "$ gh pr create --base main --title 'Security Demo: Authentication Module' --body 'Demo PR with vulnerabilities'"
PR_URL=$(gh pr create --base main --title "Security Demo: Authentication Module with Vulnerabilities" --body "This PR adds a new authentication system for demo purposes. Contains deliberate security vulnerabilities for PatchPro CI analysis:

- Hardcoded database credentials
- SQL injection vulnerabilities  
- Weak MD5 hashing
- Predictable session tokens
- Debug mode enabled

**This is a demo PR** - PatchPro will analyze and provide security fixes." 2>&1 | grep -o 'https://github.com/[^[:space:]]*')

if [ -n "$PR_URL" ]; then
    echo "✅ Pull Request created: $PR_URL"
    # Extract repo info for Actions URL
    REPO_URL=$(echo "$PR_URL" | sed 's|/pull/.*||')
    ACTIONS_URL="${REPO_URL}/actions"
else
    echo "✅ Pull Request created successfully"
    # Fallback - construct URLs from git remote
    REPO_URL=$(git remote get-url origin | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
    ACTIONS_URL="${REPO_URL}/actions"
    PR_URL="${REPO_URL}/pulls"
fi
echo ""
sleep 2

echo -e "${BLUE}Step 3: Watch PatchPro CI in Action${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎬 Now it's time to see PatchPro in action!"
echo ""
echo -e "${YELLOW}� CLICK THESE LINKS TO WATCH:${NC}"
echo ""
echo -e "${CYAN}1. 🔄 GitHub Actions (watch PatchPro CI running):${NC}"
echo "   $ACTIONS_URL"
echo ""
echo -e "${CYAN}2. 💬 Pull Request (see PatchPro comments):${NC}"  
echo "   $PR_URL"
echo ""
echo -e "${PURPLE}📋 STEP-BY-STEP INSTRUCTIONS:${NC}"
echo ""
echo "🔄 GitHub Actions Tab:"
echo "   1. Click the Actions link above"
echo "   2. Look for the workflow run that just started"
echo "   3. Click on the running workflow to see live logs"
echo "   4. Watch PatchPro analyze your vulnerable code in real-time"
echo ""
echo "💬 Pull Request Tab:"  
echo "   1. Click the PR link above"
echo "   2. Wait 1-2 minutes for PatchPro to complete analysis"
echo "   3. Refresh the page to see PatchPro's comment with:"
echo "      • Security vulnerabilities found"
echo "      • AI-generated patches for each issue"
echo "      • Cost estimate and fix recommendations"
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
echo -e "${GREEN}✨ Demo complete! PatchPro is working in the background.${NC}"
echo ""
echo -e "${YELLOW}🎯 Next Steps for Judges:${NC}"
echo "1. Click the GitHub Actions link above to watch live analysis"
echo "2. Click the PR link to see results when analysis completes"
echo "3. Experience the power of AI-driven security fixes!"
echo ""
echo -e "${CYAN}🔄 To run demo again:${NC}"
echo "   Simply run ./demo-single-file-pr.sh again - it will close the old PR and create a fresh one"