#!/bin/bash

# MCP Environment Loader
# This script loads MCP tokens from .cursor/mcp.json into environment variables

echo "🔧 Loading MCP Environment Variables"
echo "==================================="

# Check if .cursor/mcp.json exists
if [ ! -f ".cursor/mcp.json" ]; then
    echo "❌ .cursor/mcp.json not found!"
    exit 1
fi

# Use jq to parse the JSON and extract server names and tokens
if command -v jq &> /dev/null; then
    echo "✅ Using jq to parse configuration..."
    
    # Extract server names and tokens
    servers=$(jq -r '.mcpServers | keys[]' .cursor/mcp.json)
    
    for server in $servers; do
        # Convert server name to environment variable format
        env_var="MCP_$(echo $server | tr '[:lower:]' '[:upper:]' | sed 's/-/_/g')_TOKEN"
        
        # Extract token from JSON
        token=$(jq -r ".mcpServers[\"$server\"].headers.Authorization" .cursor/mcp.json | sed 's/Bearer //')
        
        # Set the environment variable
        export "$env_var"="$token"
        echo "🔐 Set $env_var"
    done
    
    echo ""
    echo "✅ Environment variables loaded successfully!"
    echo ""
    echo "📋 Current MCP environment variables:"
    env | grep MCP_ || echo "   No MCP environment variables found"
    
else
    echo "⚠️  jq not found. Using hardcoded values..."
    
    # Set hardcoded values
    export MCP_WIKIPEDIA_SEARCH_TOKEN="YOUR_TOKEN_HERE"
    export MCP_DOC_SEARCH_TOKEN="YOUR_TOKEN_HERE"
    
    echo "🔐 Set MCP_WIKIPEDIA_SEARCH_TOKEN"
    echo "🔐 Set MCP_DOC_SEARCH_TOKEN"
    echo ""
    echo "✅ Environment variables loaded successfully!"
fi

echo ""
echo "🚀 You can now run MCP commands:"
echo "   python code/mcp_cli.py list-servers"
echo "   python code/mcp_cli.py search 'your query'" 