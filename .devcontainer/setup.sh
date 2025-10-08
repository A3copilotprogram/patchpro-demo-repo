#!/bin/bash

# PatchPro CI Demo Environment Setup
echo "🚀 Setting up PatchPro CI Demo environment..."

# Install PatchPro
echo "📦 Installing PatchPro..."
pip install patchpro-bot

# Verify installation
echo "✅ Verifying PatchPro installation..."
patchpro --version

# Configure git (required for CI demos)
echo "🔧 Configuring git..."
git config --global user.name "Judge Demo User"
git config --global user.email "judge@demo.patchpro"
git config --global init.defaultBranch main

# Set up GitHub CLI authentication hint
echo "🔑 GitHub CLI setup:"
echo "Run 'gh auth login' to authenticate with GitHub for PR demos"

# Make demo scripts executable
echo "🎬 Making demo scripts executable..."
chmod +x *.sh 2>/dev/null || true

echo "✨ Setup complete! Ready for PatchPro CI demos."
echo ""
echo "Available demo scripts:"
echo "  • ./create-judge-demo.sh - Quick CI trigger demo"
echo "  • ./demo-complete-pr-workflow.sh - Full PR workflow demo"
echo ""
echo "📖 See JUDGES_DEMO_GUIDE.md for detailed instructions"