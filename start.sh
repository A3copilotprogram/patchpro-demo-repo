#!/bin/bash
# Render Start Script - Enhanced AI Fixes Feature
set -e

echo "🚀 Starting PatchPro Demo with Enhanced AI Fixes..."
echo "=================================================="

# Verify deployment branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "📍 Running from branch: $CURRENT_BRANCH"
echo "✅ Enhanced AI features include: 'Analyze + Generate Fixes' button"

# Export environment variables for Flask
export FLASK_APP=app.py
export FLASK_ENV=production

# Start the application with gunicorn
echo "🌐 Starting Flask app with gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 60 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    app:app