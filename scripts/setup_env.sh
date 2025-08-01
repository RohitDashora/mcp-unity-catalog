#!/bin/bash

# MCP Environment Setup Script
# This script helps set up environment variables for MCP tokens

echo "🔧 MCP Environment Setup"
echo "========================"

# Check if .cursor/mcp.json exists
if [ ! -f ".cursor/mcp.json" ]; then
    echo "❌ .cursor/mcp.json not found!"
    exit 1
fi

# Extract tokens from mcp.json and create environment variables
echo "📋 Extracting tokens from .cursor/mcp.json..."

# Use jq to parse the JSON and extract server names and tokens
if command -v jq &> /dev/null; then
    echo "✅ Using jq to parse configuration..."
    
    # Extract server names and tokens
    servers=$(jq -r '.mcpServers | keys[]' .cursor/mcp.json)
    
    echo ""
    echo "🔐 Environment variables to set:"
    echo "================================"
    
    for server in $servers; do
        # Convert server name to environment variable format
        env_var="MCP_$(echo $server | tr '[:lower:]' '[:upper:]' | sed 's/-/_/g')_TOKEN"
        
        # Extract token from JSON
        token=$(jq -r ".mcpServers[\"$server\"].headers.Authorization" .cursor/mcp.json | sed 's/Bearer //')
        
        echo "export $env_var=\"$token\""
    done
    
    echo ""
    echo "💡 To set these variables for current session:"
    echo "   source scripts/setup_env.sh"
    echo ""
    echo "💡 To add to your shell profile (bash/zsh):"
    echo "   echo 'source scripts/setup_env.sh' >> ~/.bashrc"
    echo "   echo 'source scripts/setup_env.sh' >> ~/.zshrc"
    
else
    echo "⚠️  jq not found. Using basic parsing..."
    
    # Basic parsing without jq
    echo "🔐 Environment variables to set:"
    echo "================================"
    echo "export MCP_WIKIPEDIA_SEARCH_TOKEN=\"your-wikipedia-search-token-here\""
    echo "export MCP_DOC_SEARCH_TOKEN=\"your-doc-search-token-here\""
    
    echo ""
    echo "💡 To set these variables for current session:"
    echo "   export MCP_WIKIPEDIA_SEARCH_TOKEN=\"your-wikipedia-search-token-here\""
    echo "   export MCP_DOC_SEARCH_TOKEN=\"your-doc-search-token-here\""
fi

echo ""
echo "🔒 Security Note:"
echo "   - Environment variables are more secure than storing tokens in files"
echo "   - They won't be committed to version control"
echo "   - They can be easily rotated without changing code"
echo ""
echo "✅ Setup complete!" 