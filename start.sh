#!/bin/bash
# Render Start Script - Ensures gunicorn is available and starts the app

echo "🚀 Starting PatchPro Demo..."

# Check if gunicorn is available
if command -v gunicorn &> /dev/null; then
    echo "✅ gunicorn found, starting with gunicorn..."
    exec gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 1 --timeout 120
elif python -m gunicorn --version &> /dev/null; then
    echo "✅ gunicorn found via python -m, starting..."
    exec python -m gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 1 --timeout 120
else
    echo "⚠️ gunicorn not found, falling back to Flask development server..."
    echo "⚠️ This is not recommended for production"
    exec python app.py
fi