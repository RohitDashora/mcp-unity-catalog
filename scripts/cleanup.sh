#!/bin/bash

# MCP Client - Cleanup Script
# This script removes temporary files, cache, and other files that should be ignored by git

echo "🧹 MCP Client - Cleanup Script"
echo "=============================="

# Function to safely remove files/directories
safe_remove() {
    if [ -e "$1" ]; then
        echo "🗑️  Removing: $1"
        rm -rf "$1"
    else
        echo "ℹ️  Not found: $1"
    fi
}

# Python cache files
echo ""
echo "📁 Cleaning Python cache files..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*.pyd" -delete 2>/dev/null || true

# OS generated files
echo ""
echo "🖥️  Cleaning OS generated files..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true

# Log files
echo ""
echo "📝 Cleaning log files..."
find . -name "*.log" -delete 2>/dev/null || true

# IDE files
echo ""
echo "💻 Cleaning IDE files..."
safe_remove ".vscode"
safe_remove ".idea"
safe_remove "*.swp"
safe_remove "*.swo"

# Backup files
echo ""
echo "💾 Cleaning backup files..."
find . -name "*.bak" -delete 2>/dev/null || true
find . -name "*.backup" -delete 2>/dev/null || true
find . -name "*.old" -delete 2>/dev/null || true
find . -name "*.orig" -delete 2>/dev/null || true

# Test coverage files
echo ""
echo "🧪 Cleaning test coverage files..."
safe_remove ".coverage"
safe_remove ".pytest_cache"
safe_remove "htmlcov"
safe_remove ".tox"

# Node.js files (if any)
echo ""
echo "📦 Cleaning Node.js files..."
safe_remove "node_modules"
safe_remove "npm-debug.log*"
safe_remove "yarn-debug.log*"
safe_remove "yarn-error.log*"

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "💡 To see what files are currently tracked by git:"
echo "   git status"
echo ""
echo "💡 To see what files would be ignored:"
echo "   git status --ignored" 