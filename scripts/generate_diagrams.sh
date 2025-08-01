#!/bin/bash

# MCP Client - Diagram Generator Wrapper
# This script runs the Python diagram generator from the project root

echo "🎨 MCP Client - Diagram Generator"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "docs/diagrams/generate_diagrms.py" ]; then
    echo "❌ Error: generate_diagrms.py not found!"
    echo "   Please run this script from the project root directory."
    exit 1
fi

# Run the Python script
echo "🔄 Running diagram generator..."
cd docs/diagrams && python generate_diagrms.py

# Check if generation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Diagrams generated successfully!"
    echo "📁 Output location: docs/images/"
    echo "📋 Index file: docs/images/README.md"
else
    echo ""
    echo "❌ Diagram generation failed!"
    exit 1
fi 