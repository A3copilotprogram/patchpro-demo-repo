#!/bin/bash
# Render Build Script - Enhanced AI Fixes from feature/render-deployment
# This script ensures PatchPro Bot is properly installed during deployment

set -e  # Exit on any error

echo "🚀 Starting PatchPro Demo Build Process..."
echo "=================================================="

# Verify we're deploying from the correct branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "📍 Current branch: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "feature/render-deployment" ]; then
    echo "⚠️  WARNING: Not on feature/render-deployment branch!"
    echo "🔍 Branch check: Expected 'feature/render-deployment', got '$CURRENT_BRANCH'"
fi

echo "✅ Enhanced AI Fixes deployment from feature/render-deployment"
echo "🤖 This build includes: Analyze + Generate Fixes button"

# Upgrade pip first
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install main requirements
echo "📋 Installing main requirements..."
pip install -r requirements.txt

# Ensure gunicorn is explicitly installed and accessible
echo "🔧 Ensuring gunicorn is available..."
pip install gunicorn==21.2.0
which gunicorn || echo "❌ gunicorn not found in PATH"
gunicorn --version || echo "❌ gunicorn not executable"

# Install PatchPro Bot with multiple fallback strategies
echo "🤖 Installing PatchPro Bot..."

# Strategy 1: Direct git installation
echo "Attempt 1: Direct git installation"
if pip install --no-cache-dir git+https://github.com/A3copilotprogram/patchpro-bot.git@main; then
    echo "✅ PatchPro Bot installed successfully (git method)"
else
    echo "⚠️ Git method failed, trying alternative approaches..."
    
    # Strategy 2: Clone and install locally
    echo "Attempt 2: Clone and local install"
    if git clone https://github.com/A3copilotprogram/patchpro-bot.git /tmp/patchpro-bot; then
        cd /tmp/patchpro-bot
        if pip install .; then
            echo "✅ PatchPro Bot installed successfully (local method)"
            cd -
        else
            echo "❌ Local install failed"
            cd -
        fi
    else
        echo "❌ Git clone failed"
    fi
fi

# Verify installation
echo "🔍 Verifying PatchPro Bot installation..."
python -c "
try:
    import patchpro_bot
    print('✅ patchpro_bot module imported successfully')
    try:
        from patchpro_bot import AgentCore
        print('✅ AgentCore imported successfully')
        print('🎉 PatchPro Bot is ready for agentic operations!')
    except ImportError as e:
        print(f'⚠️ AgentCore import failed: {e}')
except ImportError as e:
    print(f'❌ patchpro_bot import failed: {e}')
    print('🔄 Will fall back to OpenAI direct mode')
"

echo "✅ Build process completed!"
echo "=================================================="