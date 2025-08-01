#!/bin/bash

# Simple MCP Environment Loader
echo "🔧 Loading MCP Environment Variables (Simple)"
echo "============================================="

# Set environment variables directly
export MCP_WIKIPEDIA_SEARCH_TOKEN="YOUR_TOKEN_HERE"
export MCP_DOC_SEARCH_TOKEN="YOUR_TOKEN_HERE"

echo "🔐 Set MCP_WIKIPEDIA_SEARCH_TOKEN"
echo "🔐 Set MCP_DOC_SEARCH_TOKEN"

echo ""
echo "✅ Environment variables loaded successfully!"
echo ""
echo "📋 Current MCP environment variables:"
env | grep MCP_ || echo "   No MCP environment variables found"

echo ""
echo "🚀 You can now run MCP commands:"
echo "   python code/mcp_cli.py list-servers" 