#!/usr/bin/env python3
"""
Generate PNG and SVG images from Mermaid diagram files.

This script converts .mmd files in the diagrams/ directory to high-resolution PNG 
and scalable SVG formats, saving them in the docs/images/ directory.

Requirements:
    - Node.js and npm installed
    - @mermaid-js/mermaid-cli package installed globally
    
Installation:
    npm install -g @mermaid-js/mermaid-cli

Usage:
    python generate_diagrams.py
"""

import os
import subprocess
import sys
from pathlib import Path

print("Script started")

def check_mermaid_cli():
    """Check if mermaid-cli is installed."""
    try:
        result = subprocess.run(['mmdc', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Mermaid CLI version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Mermaid CLI not found. Please install it with:")
        print("   npm install -g @mermaid-js/mermaid-cli")
        return False

def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = ['../images']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Ensured directory exists: {directory}")

def get_mermaid_files():
    """Get list of .mmd files in current directory."""
    diagrams_dir = Path('.')
    mmd_files = list(diagrams_dir.glob('*.mmd'))
    print(f"📋 Found {len(mmd_files)} Mermaid files:")
    for file in mmd_files:
        print(f"   - {file.name}")
    return mmd_files

def convert_to_images(mmd_file, output_dir):
    """Convert a single Mermaid file to PNG and SVG."""
    file_stem = mmd_file.stem
    png_output = output_dir / f"{file_stem}.png"
    svg_output = output_dir / f"{file_stem}.svg"
    
    success_count = 0
    
    # Convert to PNG
    try:
        cmd_png = [
            'mmdc',
            '-i', str(mmd_file),
            '-o', str(png_output),
            '-t', 'neutral',
            '--width', '2400',
            '--height', '1800',
            '--backgroundColor', 'white',
            '--scale', '2'
        ]
        subprocess.run(cmd_png, check=True)
        print(f"✅ Generated PNG: {png_output}")
        success_count += 1
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate PNG for {mmd_file}: {e}")
    
    # Convert to SVG
    try:
        cmd_svg = [
            'mmdc',
            '-i', str(mmd_file),
            '-o', str(svg_output),
            '-t', 'neutral',
            '--backgroundColor', 'white'
        ]
        subprocess.run(cmd_svg, check=True)
        print(f"✅ Generated SVG: {svg_output}")
        success_count += 1
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate SVG for {mmd_file}: {e}")
    
    return success_count > 0

def generate_all_diagrams():
    """Generate all diagram images."""
    print("🎨 Starting diagram generation...")
    
    # Check prerequisites
    if not check_mermaid_cli():
        return False
    
    # Ensure directories exist
    ensure_directories()
    
    # Get Mermaid files
    mmd_files = get_mermaid_files()
    if not mmd_files:
        print("❌ No Mermaid files found")
        return False
    
    # Convert each file
    output_dir = Path('../images')
    success_count = 0
    
    for mmd_file in mmd_files:
        print(f"\n🔄 Processing: {mmd_file.name}")
        if convert_to_images(mmd_file, output_dir):
            success_count += 1
    
    print(f"\n🎉 Successfully generated images for {success_count}/{len(mmd_files)} diagrams")
    return success_count == len(mmd_files)

def create_diagram_index():
    """Create an index file listing all generated diagrams."""
    output_dir = Path('../images')
    index_file = output_dir / 'README.md'
    
    png_files = sorted(output_dir.glob('*.png'))
    
    with open(index_file, 'w') as f:
        f.write("# Generated Diagrams\n\n")
        f.write("This directory contains automatically generated diagrams from Mermaid source files.\n\n")
        f.write("## Available Diagrams\n\n")
        
        for png_file in png_files:
            name = png_file.stem.replace('_', ' ').title()
            svg_file = png_file.with_suffix('.svg')
            
            f.write(f"### {name}\n\n")
            f.write(f"![{name}]({png_file.name})\n\n")
            
            # Check if both formats exist
            formats = []
            if png_file.exists():
                formats.append(f"[PNG ({png_file.stat().st_size // 1024}KB)]({png_file.name})")
            if svg_file.exists():
                formats.append(f"[SVG (Vector)]({svg_file.name})")
            
            if formats:
                f.write(f"**Formats:** {' | '.join(formats)}\n\n")
        
        f.write("## Format Benefits\n\n")
        f.write("- **PNG**: High-resolution raster images (2400x1800px) - ideal for viewing and embedding\n")
        f.write("- **SVG**: Vector graphics - infinitely scalable, perfect for printing and presentations\n\n")
        
        f.write("## Regenerating Diagrams\n\n")
        f.write("To regenerate these diagrams, run:\n\n")
        f.write("```bash\n")
        f.write("python generate_diagrams.py\n")
        f.write("```\n\n")
        f.write("**Prerequisites:**\n")
        f.write("- Node.js and npm\n")
        f.write("- Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli`\n")
    
    print(f"📝 Created diagram index: {index_file}")

def main():
    """Main function."""
    print("🚀 MCP Client - Diagram Generator")
    print("=" * 50)
    print("🎨 Generating PNG (high-resolution) and SVG (vector) diagrams...")
    
    if generate_all_diagrams():
        create_diagram_index()
        print("\n✨ All diagrams generated successfully in both PNG and SVG formats!")
        print("\n📂 Generated files are in: docs/images/")
        print("📋 View the index file: docs/images/README.md")
        print("\n🎯 Benefits:")
        print("   📷 PNG: High-resolution (2400x1800px) for viewing")
        print("   📐 SVG: Vector format for infinite scalability")
    else:
        print("\n❌ Some diagrams failed to generate")
        sys.exit(1)

if __name__ == "__main__":
    main() 